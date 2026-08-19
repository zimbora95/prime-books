/* =============================================================================
   Prime Books - AI assistant
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
    history: "/hermes/history",
    models: "/hermes/models",
  };
  var STORE = "pb.tutor.sessions.v1";
  var MODEL_STORE = "pb.tutor.model.v1";
  var PAGE_TEXT_CAP = 6000; /* characters per page sent to the model */
  /* True when the site is NOT being served from a developer machine, i.e. the
     Hermes behind the proxy is a remote VM or Hermes Cloud with no access to the
     MEGA masters. Drives whether we offer on-disk paths or public URLs.
     __PB_FORCE_REMOTE lets the verification harness exercise the deployed
     shape without deploying. __PB_ALLOW_EDITING overrides the hostname check
          so a deployment behind a tunnel can use the full editor. */
       var REMOTE =
         !!window.__PB_FORCE_REMOTE ||
         (!window.__PB_ALLOW_EDITING &&
           !/^(localhost|127\.0\.0\.1|\[::1\])$/.test(location.hostname));
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
    restored: {}, /* bookKey -> true once the server transcript was fetched */
    rawKey: null,
    attachments: [], /* [{name, dataUrl}] images attached to the next message */
  };

  /* ---------- session map ----------
     localStorage, NOT sessionStorage: the whole point is that closing the tab
     and coming back to the same book RESUMES that book's conversation. The map
     is bookKey -> sessionId, so switching books mints a new session and
     returning reuses the old one. The transcript itself lives on the server,
     fetched by ensureSession(), so a different device or a cleared browser can
     still pick the thread up as long as the session id survives. */
  function loadMap() {
    try {
      var raw = localStorage.getItem(STORE);
      if (!raw) {
        /* migrate anyone who has a live tab from the old per-tab store */
        raw = sessionStorage.getItem(STORE);
        if (raw) localStorage.setItem(STORE, raw);
      }
      return JSON.parse(raw || "{}");
    } catch (e) {
      return {};
    }
  }
  function saveMap(m) {
    try {
      localStorage.setItem(STORE, JSON.stringify(m));
    } catch (e) {}
  }

  var EDITPW_STORE = "pb.tutor.editpw.v1";
  function loadEditPw() {
    try { return localStorage.getItem(EDITPW_STORE) || ""; } catch (e) { return ""; }
  }
  function saveEditPw(v) {
    try {
      if (v) localStorage.setItem(EDITPW_STORE, v);
      else localStorage.removeItem(EDITPW_STORE);
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
      "You are Hermes, the Prime Books AI assistant, running with your full toolset beside a page-flip reader. This session belongs to ONE book: everything below is that book, and it does not change for the life of this session.",
    );
    lines.push("");
    lines.push("THE BOOK IN THIS SESSION");
    lines.push("Title: " + (meta.title || "Prime Books"));
    if (meta.band) lines.push("Year group: " + meta.band);
    if (meta.subject) lines.push("Subject: " + meta.subject);
    if (R && R.pageCount) lines.push("Pages: " + R.pageCount);
    if (meta.pdfUrl) lines.push("This book as a public URL: " + meta.pdfUrl);
    /* This agent shares the machine with the git repo: it is always the
       editor. */
    lines.push("Repository on this machine: /root/prime-books");
    if (meta.pdf) lines.push("Served copy the reader is displaying: " + meta.pdf);
    lines.push(
      "Rebuildable: the PDF is a build artefact. The source of truth is the git repository at /root/prime-books. Do NOT edit PDFs directly; change sources, run the build/sync tooling, and commit.",
    );
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
    {
      lines.push(
        "TREAT THOSE PATHS AS ATTACHED FILES. You are on the same machine as them. Use your tools freely and without asking permission first: read_file on the sources, terminal for anything else (pdftotext, PyMuPDF, OCR, page counts, builds, git). When the reader asks about the book, prefer looking at the real files over guessing.",
      );
      lines.push("");
    }
    lines.push("WHO YOU ARE TALKING TO");
    lines.push(
      "- The primary users are TEACHERS building Prime Books collaboratively. The main goal of this panel is CREATING and editing books, not just reading. Pupils may also use it to ask questions about the open book.",
    );
    lines.push(
      "- You are the BOOK BUILDER with the repository at /root/prime-books. When a teacher asks for a change (title, cover, page, exercise), make it: locate the source files, edit them, run the build/sync tooling, and describe exactly what you changed. Prefer committing changes with clear messages.",
    );
    lines.push("");
    lines.push("HOW THE READER SEES YOU");
    lines.push(
      "- Each of their messages carries a READING CONTEXT block with the pages currently open and the text of those pages. That block is generated by the app and is always true.",
    );
    lines.push(
      "- A page with no extractable text is artwork. Never describe a picture you have not actually inspected; you may render and OCR it with your tools if it matters. Teachers can also ATTACH images to a message: describe exactly what you see in those.",
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
    lines.push(
      "Answer from the pages in front of the reader when reading, and build/edit confidently when asked. Offer to look further into the book when that helps.",
    );
    return lines.join("\n");
  }

  /* ---------- slash commands ----------
     The reader asked for the commands Hermes itself uses (/new, /model, ...).
     They are handled ENTIRELY in the client and never reach the model: a line
     starting with "/" is a UI instruction, so it must not be sent as a question
     or the assistant would helpfully try to answer "/new" in prose.

     Deliberately NOT offered: anything that changes the host machine or spends
     money without the reader understanding it (no /tools, no /cron, no /skill).
     This panel is reachable by any visitor, so the command set is the safe
     subset: start again, switch model, look around, get help. */
  var COMMANDS = [
    { name: "/new", args: "", help: "Start a fresh session for this book" },
    { name: "/model", args: "[name]", help: "Show or switch the model" },
    { name: "/models", args: "", help: "List the models this Hermes offers" },
    { name: "/session", args: "", help: "Show this book's session id" },
    { name: "/clear", args: "", help: "Clear the panel, keep the session" },
    { name: "/pages", args: "", help: "What the assistant can see right now" },
    { name: "/help", args: "", help: "List these commands" },
  ];

  function loadModelChoice() {
    try {
      return JSON.parse(localStorage.getItem(MODEL_STORE) || "null");
    } catch (e) {
      return null;
    }
  }
  function saveModelChoice(choice) {
    try {
      if (choice) localStorage.setItem(MODEL_STORE, JSON.stringify(choice));
      else localStorage.removeItem(MODEL_STORE);
    } catch (e) {}
  }

  function note(text) {
    var body = addMsg("assistant", text);
    body.parentElement.classList.add("pbc-note");
    return body;
  }

  /* Forget this book's session and start a clean one. The NEXT question mints
     it, so clicking + never litters state.db with empty sessions. This is the
     "+ new session" the reader asked for: close the tab, come back, and the
     book resumes; press + and the same book starts empty. */
  function newSession(quiet) {
    var key = state.bookKey;
    if (key) {
      var map = loadMap();
      delete map[key];
      saveMap(map);
      state.history[key] = [];
      state.restored[key] = true; /* nothing on the server to restore */
      state.briefed[key] = false; /* a fresh session needs the briefing again */
    }
    state.sessionId = null;
    state.creating = null;
    state.lastPagesSent = null;
    el.log.textContent = "";
    if (!quiet) {
      var meta = state.meta || {};
      note(
        "New session started for " +
          (meta.title ? "\u201c" + meta.title + "\u201d" : "this book") +
          ". Nothing from the earlier conversation carries over.",
      );
    }
    suggestChips();
    updateSessionLabel();
  }

  async function listModels() {
    var r = await fetch(EP.models, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({}),
    });
    if (!r.ok) throw new Error("Could not read the model list.");
    return r.json();
  }

  /* Returns true when the input was a command and has been dealt with. */
  async function runCommand(line) {
    var m = line.match(/^\/([a-z]+)\s*(.*)$/i);
    if (!m) return false;
    var cmd = "/" + m[1].toLowerCase();
    var arg = (m[2] || "").trim();
    addMsg("user", line);

    if (cmd === "/help") {
      note(
        "Commands:\n" +
          COMMANDS.map(function (c) {
            return "- " + c.name + (c.args ? " " + c.args : "") + " \u2014 " + c.help;
          }).join("\n"),
      );
      return true;
    }
    if (cmd === "/new") {
      newSession(false);
      return true;
    }
    if (cmd === "/clear") {
      el.log.textContent = "";
      if (state.bookKey) state.history[state.bookKey] = [];
      note("Panel cleared. The session and its memory are intact: ask /new for a truly fresh start.");
      return true;
    }
    if (cmd === "/session") {
      note(
        state.sessionId
          ? "Session id: " + state.sessionId + "\nIt is stored against this book, so returning to the book resumes it."
          : "No session yet for this book. It is created when you ask your first question.",
      );
      return true;
    }
    if (cmd === "/pages") {
      var R = window.PBReading;
      if (!R || !R.ready) {
        note("The book is still loading.");
        return true;
      }
      var pages = R.spread();
      var txt = await R.pageText(pages[0]);
      note(
        "Open: " +
          pagesLabel(pages) +
          " of " +
          (R.pageCount || "?") +
          "\nSection: " +
          (R.sectionFor(pages[0]) || "not detected") +
          "\nText layer on this page: " +
          (txt && txt.length > 20
            ? txt.length + " characters, so I can read it"
            : "none, so this page is artwork and I will not describe it"),
      );
      return true;
    }
    if (cmd === "/models" || (cmd === "/model" && !arg)) {
      var chosen = loadModelChoice();
      setStatus("Reading the model list\u2026", true);
      try {
        var data = await listModels();
        setStatus("", false);
        var names = (data.models || []).map(function (x) {
          return x.model;
        });
        var uniq = names.filter(function (n, i) {
          return names.indexOf(n) === i;
        });
        var current = (chosen && chosen.model) || data.current || "the server default";
        if (cmd === "/model") {
          note(
            "Current model: " +
              current +
              "\nSwitch with /model <name>. " +
              uniq.length +
              " available; /models lists them.",
          );
        } else {
          note(
            "Current model: " +
              current +
              "\n\n" +
              uniq.slice(0, 60).join("\n") +
              (uniq.length > 60 ? "\n\u2026and " + (uniq.length - 60) + " more" : "") +
              "\n\nSwitch with /model <name>.",
          );
        }
      } catch (e) {
        setStatus("", false);
        note("I could not read the model list. " + (e.message || ""));
      }
      return true;
    }
    if (cmd === "/model") {
      setStatus("Checking that model\u2026", true);
      try {
        var d = await listModels();
        setStatus("", false);
        var match = (d.models || []).filter(function (x) {
          return x.model.toLowerCase() === arg.toLowerCase();
        })[0];
        if (!match) {
          /* Substring rescue: "opus" should find anthropic/claude-opus-5
             rather than being rejected as unknown. */
          var near = (d.models || []).filter(function (x) {
            return x.model.toLowerCase().indexOf(arg.toLowerCase()) !== -1;
          });
          if (near.length === 1) match = near[0];
          else if (near.length > 1) {
            note(
              "That matches " +
                near.length +
                " models. Did you mean one of these?\n" +
                near
                  .slice(0, 10)
                  .map(function (x) {
                    return "- " + x.model;
                  })
                  .join("\n"),
            );
            return true;
          }
        }
        if (!match) {
          note("I do not have a model called \u201c" + arg + "\u201d. Try /models.");
          return true;
        }
        saveModelChoice({ model: match.model, provider: match.provider });
        /* A session's model is pinned AT CREATION and the stored value wins
           over anything sent per turn, so the choice can only take effect on a
           NEW session. Say that plainly rather than appearing to switch and
           silently not switching. */
        newSession(true);
        note(
          "Model set to " +
            match.model +
            ".\nA session's model is fixed when it is created, so I have started a fresh session for this book to apply it.",
        );
      } catch (e) {
        setStatus("", false);
        note("I could not switch model. " + (e.message || ""));
      }
      return true;
    }
    note("Unknown command " + cmd + ". Try /help.");
    return true;
  }

  function updateSessionLabel() {
    if (!el.sessionTag) return;
    var chosen = loadModelChoice();
    var bits = [];
    if (state.sessionId) bits.push("session live");
    if (chosen && chosen.model) bits.push(chosen.model);
    el.sessionTag.textContent = bits.join(" \u00b7 ");
  }

  /* ---------- transport ---------- */
  /* Forget a session id that the server no longer knows (e.g. the backend
     was rebuilt or migrated) and mint a fresh one. Self-healing: the reader
     should never see a dead "Hermes 404" with no way forward. */
  function dropStaleSession(reason) {
    var key = state.bookKey;
    if (key) {
      var map = loadMap();
      delete map[key];
      saveMap(map);
      state.history[key] = [];
      state.restored[key] = true;
      state.briefed[key] = false; /* the fresh session needs the briefing */
    }
    state.sessionId = null;
    state.creating = null;
    if (reason) console.warn("[pb-chat] dropped stale session:", reason);
  }

  /* Validate a stored session id against the server (cheap GET). Returns the
     id when it exists, null when it is stale. */
  async function sessionExists(sid) {
    try {
      var r = await fetch(EP.history, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ sessionId: sid }),
      });
      /* 200 with any shape means the session exists; a 4xx from the upstream
         Hermes means it does not. The history endpoint returns 200 + empty
         list rather than 404 for unknown ids, so also accept that. */
      return r.ok ? sid : null;
    } catch (e) {
      return null;
    }
  }

  async function ensureSession() {
    if (state.sessionId) return state.sessionId;
    if (state.creating) return state.creating;
    var meta = state.meta || {};
    var key = state.bookKey;
    var map = loadMap();
    if (key && map[key]) {
      var stored = await sessionExists(map[key]);
      if (stored) {
        state.sessionId = stored;
        /* A known session means the reader has been in this book before, so
           the briefing already sits in server-side history. Do not resend. */
        state.briefed[key] = true;
        return state.sessionId;
      }
      /* The stored id is stale (server restart, migration, swap): forget it
         and fall through to creating a brand-new session below. The fresh
         session gets the full briefing again, so the agent knows the book. */
      dropStaleSession(map[key]);
    }
    state.creating = (async function () {
      var title =
        "Prime Books \u00b7 " +
        (meta.title || "Book") +
        (meta.band ? " \u00b7 " + meta.band : "");
      var chosen = loadModelChoice();
      var payload = {
        title: title,
        mode: "authoring",
        /* Bind every Prime Books session into one Hermes Project (the repo
           checkout is the project key on the authoring host). */
        cwd: "/root/prime-books",
      };
      var pw = loadEditPw();
      if (pw) payload.editPassword = pw;
      /* A session's model is pinned at creation, so a /model choice has to
         travel with the create call, not with a turn. */
      if (chosen && chosen.model) {
        payload.model = chosen.model;
        if (chosen.provider) payload.provider = chosen.provider;
      }
      var r = await fetch(EP.session, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      if (!r.ok) {
        if (r.status === 403) {
          var pw = prompt("Book editing is locked. Enter the edit password:");
          if (pw) {
            saveEditPw(pw.trim());
            throw new Error("Password saved - send your message again.");
          }
        }
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
      updateSessionLabel();
      return state.sessionId;
    })();
    return state.creating;
  }

  async function send(question) {
    if (state.busy) return;
    /* A slash command is a UI instruction, not a question: handle it here and
       never spend a model turn on it. Checked BEFORE the book-ready guard so
       /help and /model still work while a large PDF is loading. */
    if (/^\//.test(question)) {
      state.busy = true;
      el.send.disabled = true;
      el.input.value = "";
      try {
        var handled = await runCommand(question);
        if (handled) return;
      } catch (e) {
        note("That command failed: " + ((e && e.message) || "unknown error"));
        return;
      } finally {
        state.busy = false;
        el.send.disabled = false;
        scrollDown();
      }
    }
    var R = window.PBReading;
    if (!R || !R.ready) {
      setStatus("The book is still loading.", false);
      return;
    }
    state.busy = true;
    el.send.disabled = true;
    var pendingImages = state.attachments.map(function (a) {
      return a.dataUrl;
    });
    state.attachments = [];
    renderAttachments();
    el.input.value = "";
    if (pendingImages.length) {
      question +=
        " \n(" +
        pendingImages.length +
        (pendingImages.length === 1
          ? " image attached)"
          : " images attached)");
    }
    addMsg("user", question);
    remember("user", question);
    setStatus("Thinking\u2026", true);

    var bubble = null;
    var acc = "";
    var retried = false;
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
      var chatBody = {
        sessionId: sid,
        input: parts.join("\n\n"),
        mode: "authoring",
      };
      if (pendingImages.length) chatBody.images = pendingImages;
      var pw2 = loadEditPw();
      if (pw2) chatBody.editPassword = pw2;
      var res = await fetch(EP.chat, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(chatBody),
        signal: state.abort.signal,
      });
      if (!res.ok || !res.body) {
        var msg = "The assistant is unavailable.";
        var detail = "";
        try {
          var j = await res.json();
          if (j && j.error) msg = j.error;
          if (j && j.detail) detail = String(j.detail);
        } catch (e) {}
        /* Stale session on the server (404 / bad session id / session not
           found): drop it, mint a fresh one WITH the briefing, and retry the
           question once. The reader never has to know. */
        var stale =
          res.status === 404 ||
          /bad session/i.test(msg + " " + detail) ||
          /not found/i.test(msg + " " + detail);
        if (stale && !retried) {
          retried = true;
          dropStaleSession(sid);
          state.lastPagesSent = null; /* force page text into the retry */
          setStatus("Starting a fresh session\u2026", true);
          var sid2 = await ensureSession();
          var parts2 = [briefing()];
          var ctx2 = await readingBlock();
          if (ctx2) parts2.push(ctx2);
          parts2.push("Pupil's question: " + question);
          var retryBody = {
            sessionId: sid2,
            input: parts2.join("\n\n"),
            mode: "authoring",
          };
          if (pendingImages.length) retryBody.images = pendingImages;
          var res2 = await fetch(EP.chat, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(retryBody),
            signal: state.abort.signal,
          });
          if (res2.ok && res2.body) {
            res = res2;
            /* stream from res2 below via the shared reader */
          } else {
            var msg2 = "The assistant is unavailable.";
            try {
              var j2 = await res2.json();
              if (j2 && j2.error) msg2 = j2.error;
            } catch (e) {}
            throw new Error(msg2);
          }
        } else {
          throw new Error(msg);
        }
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
  /* Pull a returning reader's transcript back from the server. In-memory
     state.history only survives a book switch within one page load; after a
     reload or a new tab the messages live only in Hermes' own session store. */
  async function restoreFor(bookKey) {
    if (!bookKey || state.restored[bookKey]) return false;
    var map = loadMap();
    var sid = map[bookKey];
    if (!sid) return false;
    state.restored[bookKey] = true;
    try {
      var r = await fetch(EP.history, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ sessionId: sid }),
      });
      if (!r.ok) return false;
      var data = await r.json();
      var msgs = (data && data.messages) || [];
      if (!msgs.length) return false;
      state.history[bookKey] = msgs.map(function (m) {
        return { role: m.role, text: m.content };
      });
      if (state.bookKey === bookKey) repaintFor(bookKey);
      return true;
    } catch (e) {
      return false;
    }
  }

  function repaintFor(bookKey) {
    el.log.textContent = "";
    var hist = state.history[bookKey] || [];
    if (!hist.length) {
      var meta = state.meta || {};
      var known = !!loadMap()[bookKey];
      var intro = addMsg(
        "assistant",
        known
          ? "Welcome back to the " +
              (meta.title ? "\u201c" + meta.title + "\u201d" : "book") +
              " workshop. Carry on where you left off, or ask me something new."
          : "Hello. This is the " +
              (meta.title ? "\u201c" + meta.title + "\u201d" : "book") +
              " editing workshop: ask me to change a title, page or exercise and I will edit the sources, rebuild and commit. Pupils can also ask questions about the open pages.",
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
    state.rawKey = d.bookKey;
    state.bookKey = d.bookKey || null;
    state.meta = d.meta;
    if (changed) {
      /* New book: drop the old session handle so the next question mints a
         fresh Hermes session for THIS book. */
      state.sessionId = null;
      state.creating = null;
      state.lastPagesSent = null;
      var map = loadMap();
      if (d.bookKey && map[d.bookKey]) {
        state.sessionId = map[d.bookKey];
        /* Been here before: the briefing is already in server history. */
        state.briefed[d.bookKey] = true;
      }
      repaintFor(d.bookKey);
      /* Then pull the real transcript back, which repaints again when it lands. */
      restoreFor(d.bookKey);
      updateSessionLabel();
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

  /* ---------- attachments ---------- */
  /* Teachers attach images (a photo of a worksheet, a cover draft, a sketch).
     Read as data URLs (the api_server vision pipeline accepts data:image/
     URLs) and shown as removable chips above the input. */
  var MAX_ATTACH = 4;
  var MAX_IMAGE_BYTES = 4 * 1024 * 1024;

  function addAttachment(file) {
    if (!file || !/^image\//.test(file.type)) {
      note("Only image attachments are supported for now.");
      return;
    }
    if (state.attachments.length >= MAX_ATTACH) {
      note("Up to " + MAX_ATTACH + " images per message.");
      return;
    }
    if (file.size > MAX_IMAGE_BYTES) {
      note("That image is larger than 4 MB. Please attach a smaller one.");
      return;
    }
    var reader = new FileReader();
    reader.onload = function () {
      state.attachments.push({ name: file.name, dataUrl: reader.result });
      renderAttachments();
    };
    reader.readAsDataURL(file);
  }

  function renderAttachments() {
    if (!el.attachRow) return;
    el.attachRow.textContent = "";
    el.attachRow.style.display = state.attachments.length ? "flex" : "none";
    state.attachments.forEach(function (a, idx) {
      var chip = h("span", "pbc-attach-chip");
      var thumb = h("img", "pbc-attach-thumb");
      thumb.src = a.dataUrl;
      thumb.alt = a.name;
      var nm = h("span", "pbc-attach-name", a.name);
      var rm = h("button", "pbc-attach-rm", "\u00d7");
      rm.type = "button";
      rm.title = "Remove attachment";
      rm.setAttribute("aria-label", "Remove attachment " + a.name);
      rm.addEventListener("click", function () {
        state.attachments.splice(idx, 1);
        renderAttachments();
      });
      chip.appendChild(thumb);
      chip.appendChild(nm);
      chip.appendChild(rm);
      el.attachRow.appendChild(chip);
    });
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
    if (el.input) el.input.disabled = !state.online;
    if (el.send) el.send.disabled = !state.online;
    if (el.attachBtn) el.attachBtn.disabled = !state.online;
    if (!state.online && el.log) {
      el.log.textContent = "";
      var n = addMsg(
        "assistant",
        "The AI assistant is offline (the Prime Books build server is not reachable). Your message box stays ready; it will work again once the server is back.",
      );
      n.parentElement.classList.add("pbc-intro");
    }
  }

  /* ---------- build the panel ---------- */
  function mount() {
    var stage = document.getElementById("fbStage");
    if (!stage) return;

    var panel = h("aside", "pbc");
    panel.id = "pbChat";
    panel.setAttribute("aria-label", "AI assistant");

    var head = h("div", "pbc-head");
    var titles = h("div", "pbc-titles");
    titles.appendChild(h("div", "pbc-title", "AI assistant"));
    el.where = h("div", "pbc-where");
    titles.appendChild(el.where);
    el.sessionTag = h("div", "pbc-sess");
    titles.appendChild(el.sessionTag);
    head.appendChild(titles);
    /* + starts a fresh session for THIS book. The reader asked for exactly this:
       returning to a book resumes its conversation, and + gives them a clean one
       on the same book without touching any other book's thread. */
    var fresh = h("button", "pbc-new", "+");
    fresh.type = "button";
    fresh.title = "New session for this book";
    fresh.setAttribute("aria-label", "New session for this book");
    fresh.addEventListener("click", function () {
      if (!state.busy) newSession(false);
    });
    head.appendChild(fresh);
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
    el.attachRow = h("div", "pbc-attach");
    el.attachRow.style.display = "none";
    panel.appendChild(el.attachRow);
    el.input = h("textarea", "pbc-input");
    el.input.rows = 1;
    el.input.placeholder = "Ask about this page, or / for commands\u2026";
    el.input.setAttribute("aria-label", "Ask about this page");
    el.attachBtn = h("button", "pbc-attachbtn");
    el.attachBtn.type = "button";
    el.attachBtn.title = "Attach an image";
    el.attachBtn.setAttribute("aria-label", "Attach an image");
    el.attachBtn.textContent = "\u{1F4CE}";
    el.fileInput = h("input");
    el.fileInput.type = "file";
    el.fileInput.accept = "image/*";
    el.fileInput.multiple = true;
    el.fileInput.style.display = "none";
    el.fileInput.addEventListener("change", function () {
      Array.prototype.slice.call(el.fileInput.files || []).forEach(addAttachment);
      el.fileInput.value = "";
    });
    el.attachBtn.addEventListener("click", function () {
      el.fileInput.click();
    });
    /* Paste an image straight into the composer. */
    el.input.addEventListener("paste", function (ev) {
      var items = (ev.clipboardData && ev.clipboardData.items) || [];
      for (var i = 0; i < items.length; i++) {
        if (items[i].type && items[i].type.indexOf("image/") === 0) {
          ev.preventDefault();
          addAttachment(items[i].getAsFile());
        }
      }
    });
    el.send = h("button", "pbc-send", "Ask");
    el.send.type = "submit";
    form.appendChild(el.input);
    form.appendChild(el.attachBtn);
    form.appendChild(el.fileInput);
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
      t.title = "AI assistant";
      t.setAttribute("aria-label", "AI assistant");
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
