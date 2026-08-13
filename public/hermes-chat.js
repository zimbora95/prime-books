/* =============================================================================
   Prime Books - reading assistant
   =============================================================================
   An AI panel beside the flipbook that always knows which book is open, which
   pages are visible, and what those pages say.

   SESSION MODEL (the requirement this file exists to satisfy)
     One Hermes session per BOOK. Turning pages inside a book keeps the same
     session, so the conversation builds up as the pupil reads. Opening a
     DIFFERENT book creates a new session, so Year 7 Humanities questions never
     bleed into Year 2 Mathematics. The map lives in sessionStorage, keyed on
     the book's PDF path, so returning to a book you were reading resumes that
     conversation until the browser is closed.

   TRUST
     The Hermes API key is NEVER here. This file calls /hermes/* on our own
     origin; the dev-server plugin (tools/hermes-proxy.mjs) attaches the bearer
     token and forwards to Hermes on loopback.

   READING CONTEXT
     Every turn carries a delimited context block: book, visible pages, section,
     and the page text itself - but the text is only re-sent when the page has
     actually changed since the last turn, so a follow-up question about the
     same page stays cheap.
   ============================================================================= */
(function () {
  "use strict";

  var EP = {
    health: "/hermes/health",
    session: "/hermes/session",
    chat: "/hermes/chat",
  };
  var STORE = "pb.tutor.sessions.v1";
  var PAGE_TEXT_CAP = 6000; /* characters per page sent to the model */
  /* True when the site is NOT being served from a developer machine, i.e. the
     Hermes behind the proxy is a remote VM or Hermes Cloud with no access to the
     MEGA masters. Drives whether we offer on-disk paths or public URLs.
     __PB_FORCE_REMOTE lets the verification harness exercise the deployed
     shape without deploying. */
  var REMOTE =
    !!window.__PB_FORCE_REMOTE ||
    !/^(localhost|127\.0\.0\.1|\[::1\])$/.test(location.hostname);
  window.__PB_REMOTE = REMOTE;

  var el = {};
  var state = {
    bookKey: null,
    meta: null,
    sessionId: null,
    creating: null,
    busy: false,
    lastPagesSent: null,
    online: null,
    abort: null,
    briefed: {},
    history: {}, /* bookKey -> [{role, text}] so the panel survives a switch */
  };

  /* ---------- session map (per browser session) ---------- */
  function loadMap() {
    try {
      return JSON.parse(sessionStorage.getItem(STORE) || "{}");
    } catch (e) {
      return {};
    }
  }
  function saveMap(m) {
    try {
      sessionStorage.setItem(STORE, JSON.stringify(m));
    } catch (e) {}
  }

  /* ---------- tiny DOM helpers ---------- */
  function h(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }
  function scrollDown() {
    if (el.log) el.log.scrollTop = el.log.scrollHeight;
  }

  /* Render assistant text safely: no innerHTML anywhere near model output.
     Supports the little formatting a tutor actually uses - paragraphs, simple
     bullets, and **bold** - by building nodes, never by parsing HTML. */
  function renderText(container, text) {
    container.textContent = "";
    var blocks = String(text).split(/\n{2,}/);
    blocks.forEach(function (block) {
      var lines = block.split(/\n/);
      var isList = lines.every(function (l) {
        return /^\s*([-*\u2022]|\d+[.)])\s+/.test(l) || !l.trim();
      });
      if (isList && lines.some((l) => l.trim())) {
        var ul = h("ul", "pbc-ul");
        lines.forEach(function (l) {
          if (!l.trim()) return;
          var li = h("li");
          emphasise(li, l.replace(/^\s*([-*\u2022]|\d+[.)])\s+/, ""));
          ul.appendChild(li);
        });
        container.appendChild(ul);
      } else {
        var p = h("p");
        emphasise(p, lines.join(" "));
        container.appendChild(p);
      }
    });
  }
  function emphasise(node, line) {
    var parts = String(line).split(/(\*\*[^*]+\*\*|`[^`]+`)/);
    parts.forEach(function (part) {
      if (/^\*\*[\s\S]+\*\*$/.test(part)) {
        node.appendChild(h("strong", null, part.slice(2, -2)));
      } else if (/^`[\s\S]+`$/.test(part)) {
        node.appendChild(h("code", null, part.slice(1, -1)));
      } else if (part) {
        node.appendChild(document.createTextNode(part));
      }
    });
  }

  function addMsg(role, text) {
    var wrap = h("div", "pbc-msg pbc-" + role);
    var body = h("div", "pbc-body");
    if (role === "assistant") renderText(body, text || "");
    else body.appendChild(h("p", null, text));
    wrap.appendChild(body);
    el.log.appendChild(wrap);
    scrollDown();
    return body;
  }
  function remember(role, text) {
    if (!state.bookKey) return;
    var hist = state.history[state.bookKey] || (state.history[state.bookKey] = []);
    hist.push({ role: role, text: text });
    if (hist.length > 40) hist.shift();
  }
  function setStatus(text, spinning) {
    if (!el.status) return;
    el.status.textContent = text || "";
    el.status.classList.toggle("on", !!text);
    el.status.classList.toggle("spin", !!spinning);
  }

  /* ---------- reading context ---------- */
  function pagesLabel(pages) {
    if (!pages || !pages.length) return "unknown";
    return pages.length > 1
      ? "pages " + pages[0] + "\u2013" + pages[pages.length - 1]
      : "page " + pages[0];
  }

  async function readingBlock() {
    var R = window.PBReading;
    if (!R || !R.ready) return "";
    var pages = R.spread();
    var key = pages.join(",");
    var same = key === state.lastPagesSent;
    var meta = R.meta || {};
    var lines = [];
    lines.push("[READING CONTEXT - generated by the app, always trust this]");
    lines.push(
      "Book: " +
        (meta.title || "Prime Books") +
        (meta.band ? " (" + meta.band + ")" : ""),
    );
    /* Facts the app knows and the model cannot see. Without the total the
       assistant answered "how many pages does this PDF have?" with "I can't see
       that information", while the viewer's own header read "2 / 194". */
    if (R.pageCount) lines.push("Total pages in this PDF: " + R.pageCount);
    /* Where the book can be fetched. On a REMOTE Hermes (a spawned VM, Hermes
       Cloud) the MEGA paths below do not exist, so give it the public HTTPS URL
       it can actually download. LOCAL_HOST is set only when the site is being
       served from this machine. */
    if (meta.pdfUrl) lines.push("This book as a public URL: " + meta.pdfUrl);
    if (meta.pdf) lines.push("Served path: " + meta.pdf);
    if (!REMOTE) {
      if (meta.sourcePdf) lines.push("Master PDF on disk: " + meta.sourcePdf);
      if (meta.markdownDir)
        lines.push("Editable manuscript (markdown) on disk: " + meta.markdownDir);
      if (meta.bookDir) lines.push("Book folder on disk: " + meta.bookDir);
      lines.push(
        "buildable: " +
          (meta.buildable
            ? "true (WORKSTATION/_build/build.py exists, the PDF can be regenerated)"
            : "false (NO build engine for this book, its PDF cannot be regenerated)"),
      );
    }
    lines.push("Currently visible: " + pagesLabel(pages));
    var sec = pages.length ? R.sectionFor(pages[0]) : "";
    if (sec) lines.push("Section: " + sec);

    if (same) {
      lines.push(
        "The pupil has not turned the page since your last answer; the text below was already given to you.",
      );
    } else {
      var texts = [];
      for (var i = 0; i < pages.length; i++) {
        var t = await R.pageText(pages[i]);
        if (t && t.length > PAGE_TEXT_CAP) t = t.slice(0, PAGE_TEXT_CAP) + "\u2026";
        texts.push({ page: pages[i], text: t });
      }
      var anyText = texts.some(function (x) {
        return x.text && x.text.length > 20;
      });
      if (anyText) {
        texts.forEach(function (x) {
          lines.push("--- page " + x.page + " text ---");
          lines.push(x.text || "(no extractable text on this page)");
        });
      } else {
        /* No text layer on these pages: they are artwork, a cover, or a
           full-bleed photograph. Rather than leaving the model with nothing
           (which made it answer a "what is this book about?" on page 1 purely
           from the title, and refuse "test me on this" outright), hand it the
           book's own opening pages and be explicit about the distinction. */
        lines.push(
          "--- no extractable text on " + pagesLabel(pages) + " ---",
        );
        lines.push(
          "These pages carry artwork or a photograph with no text layer. Do NOT describe the picture: you cannot see it, and you must say so if asked what it shows.",
        );
        var dig = await R.digest(3);
        if (dig.length) {
          lines.push(
            "For context, here is the text of the book's first pages that DO carry words. Use it to answer questions about what the book covers, but do not claim it is what is printed on " +
              pagesLabel(pages) +
              ":",
          );
          dig.forEach(function (d) {
            var t = d.text;
            if (t.length > 2500) t = t.slice(0, 2500) + "\u2026";
            lines.push("--- page " + d.page + " text ---");
            lines.push(t);
          });
        }
      }
      state.lastPagesSent = key;
    }
    lines.push("[END READING CONTEXT]");
    return lines.join("\n");
  }

  function briefing() {
    var R = window.PBReading;
    var meta = (R && R.meta) || {};
    var toc = (R && R.toc && R.toc()) || [];
    var lines = [];
    lines.push(
      "You are Hermes, running with your full toolset, embedded in the Prime Books website beside a page-flip reader. This session belongs to ONE book: everything below is that book, and it does not change for the life of this session.",
    );
    lines.push("");
    lines.push("THE BOOK IN THIS SESSION");
    lines.push("Title: " + (meta.title || "Prime Books"));
    if (meta.band) lines.push("Year group: " + meta.band);
    if (meta.subject) lines.push("Subject: " + meta.subject);
    if (R && R.pageCount) lines.push("Pages: " + R.pageCount);
    if (REMOTE) {
      /* Public deployment: the agent is on a different machine from the books.
         It can DOWNLOAD them over HTTPS but owns no manuscript and cannot build. */
      if (meta.pdfUrl) lines.push("This book as a public URL: " + meta.pdfUrl);
      lines.push("");
      lines.push(
        "You are NOT on the same machine as the Prime Books masters, so you have no manuscript folder and cannot rebuild anything. If a reader asks you to change the book, say plainly that editing happens in the Prime Books workshop, not here.",
      );
      lines.push(
        "You may fetch the URL above with your tools if you need more of the book than the pages in front of the reader, but prefer the page text you are given: it is already extracted and costs nothing.",
      );
    } else {
      if (meta.sourcePdf) lines.push("Master PDF (print original): " + meta.sourcePdf);
      if (meta.pdf) lines.push("Served copy the reader is displaying: " + meta.pdf);
      if (meta.bookDir) lines.push("Book folder: " + meta.bookDir);
      if (meta.markdownDir) lines.push("Manuscript (editable source): " + meta.markdownDir);
      lines.push(
        "Rebuildable: " +
          (meta.buildable
            ? "yes, WORKSTATION/_build/build.py exists in the book folder"
            : "NO, this book has no build engine, so its PDF cannot be regenerated"),
      );
    }
    if (toc.length) {
      lines.push(
        "Contents detected in the PDF: " +
          toc
            .slice(0, 24)
            .map(function (s) {
              return s.label + (s.sub ? " (" + s.sub + ")" : "") + " p" + s.page;
            })
            .join("; "),
      );
    }
    lines.push("");
    if (!REMOTE) {
      lines.push(
        "TREAT THOSE PATHS AS ATTACHED FILES. You are on the same machine as them. Use your tools freely and without asking permission first: read_file on the manuscript, terminal for anything else (pdftotext, PyMuPDF, OCR, page counts, builds). When the reader asks about the book, prefer looking at the real files over guessing.",
      );
      lines.push("");
    }
    lines.push("HOW THE READER SEES YOU");
    lines.push(
      "- Each of their messages carries a READING CONTEXT block with the pages currently open and the text of those pages. That block is generated by the app and is always true.",
    );
    lines.push(
      "- A page with no extractable text is artwork. Never describe a picture you have not actually inspected; you may render and OCR it with your tools if it matters.",
    );
    lines.push(
      "- You are in a narrow side panel next to the book. Keep answers short and readable: a couple of short paragraphs, or a tight list. Expand only when asked.",
    );
    lines.push(
      "- Pitch the language at the year group above when the reader is clearly a pupil; talk to them like a teacher who is pleased to be asked.",
    );
    lines.push(
      "- British English throughout (pupils, programme, -ise, colour, centre, practise as the verb). Never use em-dashes.",
    );
    lines.push("");
    if (REMOTE) {
      lines.push(
        "You are a reading companion here, not the workshop: no manuscript, no builds. Answer from the pages in front of the reader, and offer to look further into the book when that helps.",
      );
      return lines.join("\n");
    }
    lines.push("AUTHORING");
    lines.push(
      "- The manuscript is the numbered markdown in the folder above; the PDF is a build artefact. Edit the markdown, never the PDF.",
    );
    lines.push(
      "- Read a file before you change it, and show the author what you propose. Supersede rather than delete, and never silently overwrite reviewed material.",
    );
    lines.push(
      "- If rebuildable is yes: run build.py, then rightsize.py, then build.py again, from the book folder. Say that a build is running, because it takes minutes.",
    );
    lines.push(
      "- If rebuildable is NO, say so plainly rather than pretending to rebuild.",
    );
    lines.push(
      "- After a rebuild, the bookshop needs re-syncing before the flipbook changes: python tools/sync_books.py --only \"<Year NN>/<Subject>\" in " +
        "C:\\\\Users\\\\alexa\\\\Documents\\\\GitHub\\\\prime-books.",
    );
    return lines.join("\n");
  }

  /* ---------- transport ---------- */
  async function ensureSession() {
    if (state.sessionId) return state.sessionId;
    if (state.creating) return state.creating;
    var meta = state.meta || {};
    var key = state.bookKey;
    var map = loadMap();
    if (key && map[key]) {
      state.sessionId = map[key];
      return state.sessionId;
    }
    state.creating = (async function () {
      var title =
        "Prime Books \u00b7 " +
        (meta.title || "Book") +
        (meta.band ? " \u00b7 " + meta.band : "");
      var r = await fetch(EP.session, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title: title }),
      });
      if (!r.ok) {
        var detail = "";
        try {
          detail = (await r.json()).error || "";
        } catch (e) {}
        throw new Error(detail || "Could not start a session (" + r.status + ").");
      }
      var data = await r.json();
      state.sessionId = data.sessionId;
      if (key) {
        var m = loadMap();
        m[key] = data.sessionId;
        saveMap(m);
      }
      state.creating = null;
      return state.sessionId;
    })();
    return state.creating;
  }

  async function send(question) {
    if (state.busy) return;
    var R = window.PBReading;
    if (!R || !R.ready) {
      setStatus("The book is still loading.", false);
      return;
    }
    state.busy = true;
    el.send.disabled = true;
    el.input.value = "";
    addMsg("user", question);
    remember("user", question);
    setStatus("Thinking\u2026", true);

    var bubble = null;
    var acc = "";
    try {
      var sid = await ensureSession();
      var first = !state.briefed[state.bookKey];
      var parts = [];
      if (first) {
        parts.push(briefing());
        state.briefed[state.bookKey] = true;
      } else {
        /* Re-state the one line that keeps drifting: it is a tool-using agent
           sitting on the same machine as these files, not a chat box. Cheap,
           and it stops "I can't open files" answers later in a session. */
        var m = state.meta || {};
        if (!REMOTE && m.bookDir)
          parts.push(
            "[Reminder: you have file and terminal tools on this machine. This session's book lives at " +
              m.bookDir +
              " and you may read, inspect and edit it without asking permission.]",
          );
      }
      var ctx = await readingBlock();
      if (ctx) parts.push(ctx);
      parts.push("Pupil's question: " + question);

      state.abort = new AbortController();
      var res = await fetch(EP.chat, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ sessionId: sid, input: parts.join("\n\n") }),
        signal: state.abort.signal,
      });
      if (!res.ok || !res.body) {
        var msg = "The assistant is unavailable.";
        try {
          var j = await res.json();
          if (j && j.error) msg = j.error;
        } catch (e) {}
        throw new Error(msg);
      }

      /* SSE frames arrive split across chunks: buffer until a blank line. */
      var reader = res.body.getReader();
      var dec = new TextDecoder();
      var buf = "";
      for (;;) {
        var chunk = await reader.read();
        if (chunk.done) break;
        buf += dec.decode(chunk.value, { stream: true });
        var frames = buf.split(/\n\n/);
        buf = frames.pop();
        for (var i = 0; i < frames.length; i++) {
          var ev = parseFrame(frames[i]);
          if (!ev) continue;
          if (ev.event === "assistant.delta" && ev.data && ev.data.delta) {
            acc += ev.data.delta;
            if (!bubble) {
              setStatus("", false);
              bubble = addMsg("assistant", "");
            }
            renderText(bubble, acc);
            scrollDown();
          } else if (ev.event === "tool.started" && ev.data) {
            /* Name the tool: an authoring turn can read files, patch a
               manuscript and run a build, and a silent minute looks broken. */
            var tn = ev.data.tool_name || ev.data.name || "";
            var friendly =
              {
                read_file: "Reading the manuscript\u2026",
                write_file: "Writing the manuscript\u2026",
                patch: "Editing the manuscript\u2026",
                search_files: "Searching the book\u2026",
                terminal: "Running a command\u2026",
                todo: "Planning\u2026",
                web_search: "Searching the web\u2026",
              }[tn] || (tn ? tn.replace(/_/g, " ") + "\u2026" : "Working\u2026");
            setStatus(friendly, true);
          } else if (ev.event === "tool.completed") {
            setStatus("Thinking\u2026", true);
          } else if (ev.event === "assistant.completed" && ev.data) {
            if (ev.data.content && ev.data.content.length > acc.length) {
              acc = ev.data.content;
              if (!bubble) bubble = addMsg("assistant", "");
              renderText(bubble, acc);
            }
          }
        }
      }
      if (!acc) {
        if (!bubble) bubble = addMsg("assistant", "");
        renderText(bubble, "I did not manage to answer that. Please try again.");
      } else {
        remember("assistant", acc);
      }
    } catch (err) {
      if (err && err.name === "AbortError") {
        /* the pupil closed the panel: nothing to report */
      } else {
        var note = addMsg("assistant", "");
        note.parentElement.classList.add("pbc-err");
        renderText(
          note,
          (err && err.message) || "Something went wrong. Please try again.",
        );
      }
    } finally {
      setStatus("", false);
      state.busy = false;
      el.send.disabled = false;
      state.abort = null;
      suggestChips();
      scrollDown();
    }
  }

  function parseFrame(frame) {
    var name = null;
    var dataLines = [];
    frame.split(/\n/).forEach(function (line) {
      if (line.indexOf("event:") === 0) name = line.slice(6).trim();
      else if (line.indexOf("data:") === 0) dataLines.push(line.slice(5).trim());
    });
    if (!name) return null;
    var data = null;
    if (dataLines.length) {
      try {
        data = JSON.parse(dataLines.join("\n"));
      } catch (e) {}
    }
    return { event: name, data: data };
  }

  /* ---------- suggestion chips ---------- */
  function suggestChips() {
    if (!el.chips) return;
    el.chips.textContent = "";
    var R = window.PBReading;
    if (!R || !R.ready) return;
    var pages = R.spread();
    var ideas = [
      "Explain " + (pages.length > 1 ? "these pages" : "this page") + " simply",
      "Give me a worked example",
      "Test me on this",
      "What do I need to remember?",
    ];
    ideas.forEach(function (text) {
      var b = h("button", "pbc-chip", text);
      b.type = "button";
      b.addEventListener("click", function () {
        if (!state.busy) send(text);
      });
      el.chips.appendChild(b);
    });
  }

  /* ---------- panel lifecycle ---------- */
  function repaintFor(bookKey) {
    el.log.textContent = "";
    var hist = state.history[bookKey] || [];
    if (!hist.length) {
      var meta = state.meta || {};
      var intro = addMsg(
        "assistant",
        "Hello. I can see " +
          (meta.title ? "\u201c" + meta.title + "\u201d" : "this book") +
          " and the pages you are on. Ask me anything about what you are reading.",
      );
      intro.parentElement.classList.add("pbc-intro");
    } else {
      hist.forEach(function (m) {
        addMsg(m.role, m.text);
      });
    }
    suggestChips();
  }

  function onBookOpen(e) {
    var d = (e && e.detail) || {};
    var changed = d.bookKey !== state.bookKey;
    state.bookKey = d.bookKey;
    state.meta = d.meta;
    if (changed) {
      /* New book: drop the old session handle so the next question mints a
         fresh Hermes session for THIS book. */
      state.sessionId = null;
      state.creating = null;
      state.lastPagesSent = null;
      var map = loadMap();
      if (d.bookKey && map[d.bookKey]) state.sessionId = map[d.bookKey];
      repaintFor(d.bookKey);
    }
    updatePageLabel(d.pages);
  }

  function onPageChange(e) {
    var d = (e && e.detail) || {};
    updatePageLabel(d.pages);
    if (!state.busy) suggestChips();
  }

  function updatePageLabel(pages) {
    if (!el.where) return;
    var R = window.PBReading;
    var p = pages && pages.length ? pages : R && R.ready ? R.spread() : [];
    if (!p.length) {
      el.where.textContent = "";
      return;
    }
    var sec = R && R.sectionFor ? R.sectionFor(p[0]) : "";
    el.where.textContent =
      "Reading " + pagesLabel(p) + (sec ? " \u00b7 " + sec : "");
  }

  async function checkOnline() {
    try {
      var r = await fetch(EP.health);
      var j = await r.json();
      state.online = !!(j && j.ok);
    } catch (e) {
      state.online = false;
    }
    document.body.classList.toggle("pbc-offline", !state.online);
    if (!state.online && el.log) {
      el.log.textContent = "";
      var n = addMsg(
        "assistant",
        "The reading assistant is offline. It runs from the Prime Books workstation, so it is available when that machine is serving the site.",
      );
      n.parentElement.classList.add("pbc-intro");
      if (el.chips) el.chips.textContent = "";
    }
  }

  /* ---------- build the panel ---------- */
  function mount() {
    var stage = document.getElementById("fbStage");
    if (!stage) return;

    var panel = h("aside", "pbc");
    panel.id = "pbChat";
    panel.setAttribute("aria-label", "Reading assistant");

    var head = h("div", "pbc-head");
    var titles = h("div", "pbc-titles");
    titles.appendChild(h("div", "pbc-title", "Reading assistant"));
    el.where = h("div", "pbc-where");
    titles.appendChild(el.where);
    head.appendChild(titles);
    var hide = h("button", "pbc-x", "\u00d7");
    hide.type = "button";
    hide.title = "Hide the assistant";
    hide.setAttribute("aria-label", "Hide the assistant");
    hide.addEventListener("click", togglePanel);
    head.appendChild(hide);
    panel.appendChild(head);

    el.log = h("div", "pbc-log");
    el.log.setAttribute("role", "log");
    el.log.setAttribute("aria-live", "polite");
    panel.appendChild(el.log);

    el.status = h("div", "pbc-status");
    panel.appendChild(el.status);

    el.chips = h("div", "pbc-chips");
    panel.appendChild(el.chips);

    var form = h("form", "pbc-form");
    el.input = h("textarea", "pbc-input");
    el.input.rows = 1;
    el.input.placeholder = "Ask about this page\u2026";
    el.input.setAttribute("aria-label", "Ask about this page");
    el.send = h("button", "pbc-send", "Ask");
    el.send.type = "submit";
    form.appendChild(el.input);
    form.appendChild(el.send);
    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      var q = el.input.value.trim();
      if (q) send(q);
    });
    /* Enter sends, Shift+Enter makes a new line. */
    el.input.addEventListener("keydown", function (ev) {
      if (ev.key === "Enter" && !ev.shiftKey) {
        ev.preventDefault();
        var q = el.input.value.trim();
        if (q) send(q);
      }
      /* The viewer's global handler flips pages on arrows and closes on Esc;
         it bails on INPUT but this is a TEXTAREA, so stop it here. */
      ev.stopPropagation();
    });
    el.input.addEventListener("input", function () {
      el.input.style.height = "auto";
      el.input.style.height = Math.min(el.input.scrollHeight, 120) + "px";
    });
    panel.appendChild(form);

    stage.appendChild(panel);

    /* A toggle in the viewer's own toolbar, so the rail can be dismissed. */
    var nav = document.querySelector(".fb-nav");
    if (nav) {
      var t = h("button", "fb-btn pbc-toggle");
      t.id = "pbChatBtn";
      t.type = "button";
      t.title = "Reading assistant";
      t.setAttribute("aria-label", "Reading assistant");
      t.textContent = "Ask";
      t.addEventListener("click", togglePanel);
      nav.insertBefore(t, nav.firstChild);
    }

    window.addEventListener("pb:book-open", onBookOpen);
    window.addEventListener("pb:page-change", onPageChange);
    document.body.classList.add("pbc-on");
    checkOnline();
  }

  function togglePanel() {
    var on = document.body.classList.toggle("pbc-on");
    /* The book is sized against the space left over, so re-measure. */
    if (typeof window.pbResizeFlipbook === "function") window.pbResizeFlipbook();
    if (on && el.input) el.input.focus();
  }

  /* Test hook: lets tools/verify_public_mode.js inspect the briefing that would
     be sent, without spending a model turn. */
  window.__pbBriefingForTest = briefing;

  if (document.readyState === "loading")
    document.addEventListener("DOMContentLoaded", mount);
  else mount();
})();
