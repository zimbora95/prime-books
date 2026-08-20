/* Prime Books reading assistant - the trust boundary.
 *
 * The browser talks to this proxy; this proxy talks to Hermes. The bearer key
 * never leaves the server. Five verbs, chosen by an explicit switch: the
 * client cannot pass a path through, so it cannot reach any other Hermes
 * endpoint (/v1/runs, the jobs CRUD, terminal-capable surfaces) even if the
 * page is compromised or someone crafts a request by hand.
 *
 *   GET  /hermes/health            -> { ok, configured }
 *   POST /hermes/session           -> { sessionId }        body: { title }
 *   POST /hermes/chat              -> SSE passthrough      body: { sessionId, input }
 *   POST /hermes/history           -> { messages }         body: { sessionId }
 *   POST /hermes/models            -> { models, current }  for the /model command
 *
 * Every verb except health is POST, matching the guard below; a GET-only verb
 * added here would 405 on the shared `req.method !== "POST"` check.
 *
 * Used by vite.config.js in dev. The Vercel function for production is a thin
 * wrapper over the same handleHermes() so the contract cannot drift.
 */

const MAX_BODY = 36 * 1024 * 1024; /* 25 MB files arrive as ~34 MB base64 */

function readBody(req) {
  return new Promise((resolve, reject) => {
    let n = 0;
    const chunks = [];
    req.on("data", (c) => {
      n += c.length;
      if (n > MAX_BODY) {
        reject(new Error("body too large"));
        req.destroy();
        return;
      }
      chunks.push(c);
    });
    req.on("end", () => resolve(Buffer.concat(chunks).toString("utf8")));
    req.on("error", reject);
  });
}

function json(res, code, obj) {
  const body = JSON.stringify(obj);
  res.writeHead(code, {
    "Content-Type": "application/json; charset=utf-8",
    "Cache-Control": "no-store",
    "X-Content-Type-Options": "nosniff",
  });
  res.end(body);
}

/* Hermes rejects a duplicate session title with 400 invalid_title, so every
   title carries a timestamp. The book identity lives in the briefing message
   and in the title's readable prefix. */
function uniqueTitle(raw) {
  const clean = String(raw || "Prime Books")
    .replace(/[\r\n\t]+/g, " ")
    .trim()
    .slice(0, 80);
  return `${clean} · ${new Date().toISOString().slice(0, 19).replace("T", " ")}`;
}

export async function handleHermes(req, res, verb, cfg) {
  const base = (cfg.HERMES_BASE_URL || "").replace(/\/+$/, "");
  const key = cfg.HERMES_API_KEY || "";
  const model = cfg.HERMES_MODEL || "";
  const provider = cfg.HERMES_PROVIDER || "";

  if (verb === "health") {
    if (!base || !key) return json(res, 200, { ok: false, configured: false });
    try {
      const r = await fetch(`${base}/health`, {
        headers: { Authorization: `Bearer ${key}` },
        signal: AbortSignal.timeout(4000),
      });
      return json(res, 200, { ok: r.ok, configured: true });
    } catch {
      return json(res, 200, { ok: false, configured: true });
    }
  }

  if (!base || !key) {
    return json(res, 503, {
      error: "The AI assistant is not configured on this server.",
    });
  }
  if (req.method !== "POST") return json(res, 405, { error: "POST only" });

  let body;
  try {
    body = JSON.parse((await readBody(req)) || "{}");
  } catch {
    return json(res, 400, { error: "malformed JSON" });
  }

  if (verb === "models") {
    /* Feed the /model command. Read-only: it lists what this Hermes offers and
       which model is current. /v1/models is NOT the right surface (it advertises
       the agent as a single model); /api/model/options is the rich picker
       payload. Flattened to <=200 "provider/model" strings so a compromised page
       learns nothing but names it could read off the picker anyway. */
    try {
      const r = await fetch(`${base}/api/model/options`, {
        headers: { Authorization: `Bearer ${key}` },
        signal: AbortSignal.timeout(10000),
      });
      if (!r.ok) return json(res, 200, { models: [], current: model });
      const data = await r.json();
      const out = [];
      for (const p of (data && data.providers) || []) {
        for (const m of p.models || []) {
          out.push({ provider: p.slug, model: m, current: !!p.is_current });
          if (out.length >= 200) break;
        }
        if (out.length >= 200) break;
      }
      return json(res, 200, {
        models: out,
        current: model,
        currentProvider: provider,
      });
    } catch {
      return json(res, 200, { models: [], current: model });
    }
  }

  if (verb === "session") {
    /* Pin model + provider AT CREATION. Hermes stores the session's model and
       that stored value wins over anything sent per-turn (session_model_lock).
       Left unset it defaults to the PROFILE NAME, which is then sent to the
       provider as a literal model id and fails with
       "primebooks-tutor is not a valid model ID". */
    const payload = { title: uniqueTitle(body.title) };
    /* A reader may pick a model with /model, so honour an explicit choice from
       the client. It is validated against the names /hermes/models advertised,
       which is why that verb exists: a free-text model id would be passed
       straight to the provider. */
    const wantModel = typeof body.model === "string" ? body.model.trim() : "";
    const wantProvider =
      typeof body.provider === "string" ? body.provider.trim() : "";
    const okId = (s) => /^[A-Za-z0-9._\/:-]{2,80}$/.test(s);
    if (wantModel && okId(wantModel)) payload.model = wantModel;
    else if (model) payload.model = model;
    if (wantProvider && okId(wantProvider)) payload.provider = wantProvider;
    else if (provider) payload.provider = provider;
    let r;
    try {
      r = await fetch(`${base}/api/sessions`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${key}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
        signal: AbortSignal.timeout(20000),
      });
    } catch {
      return json(res, 502, { error: "Hermes is not reachable." });
    }
    const text = await r.text();
    if (!r.ok) return json(res, 502, { error: `Hermes ${r.status}`, detail: text.slice(0, 400) });
    let data;
    try {
      data = JSON.parse(text);
    } catch {
      return json(res, 502, { error: "Hermes returned a non-JSON session." });
    }
    const sessionId = data && data.session && data.session.id;
    if (!sessionId) return json(res, 502, { error: "No session id in response." });
    return json(res, 200, { sessionId, title: data.session.title });
  }

  if (verb === "upload") {
    /* Non-image attachments: stage the bytes on the agent's machine (same
       as the desktop file.attach) and return the stored path. */
    const name = String(body.name || "attachment").replace(/[^A-Za-z0-9._ -]/g, "_").slice(0, 120);
    const dataUrl = String(body.dataUrl || "");
    const m = /^data:[^;,]*;base64,(.*)$/s.exec(dataUrl);
    const b64 = m ? m[1].replace(/\s+/g, "") : "";
    if (!b64) return json(res, 400, { error: "dataUrl (base64) required" });
    let bytes;
    try {
      bytes = Buffer.from(b64, "base64");
    } catch {
      return json(res, 400, { error: "invalid base64" });
    }
    if (!bytes.length || bytes.length > 25 * 1024 * 1024)
      return json(res, 413, { error: "file must be 1 byte to 25 MB" });
    const filename = `${Date.now()}-${name}`;
    try {
      const r = await fetch(`${base}/api/upload`, {
        method: "POST",
        headers: { Authorization: `Bearer ${key}`, "Content-Type": "application/json" },
        body: JSON.stringify({ filename, data: b64 }),
        signal: AbortSignal.timeout(60000),
      });
      const text = await r.text();
      if (!r.ok) return json(res, 502, { error: `Hermes ${r.status}`, detail: text.slice(0, 300) });
      const data = JSON.parse(text);
      return json(res, 200, { path: data.path, name: filename });
    } catch {
      return json(res, 502, { error: "Hermes is not reachable." });
    }
  }

  if (verb === "history") {
    /* Rehydrate a returning reader's panel from the SERVER transcript. Same
       closed-verb rule: the client sends only a session id. */
    const sessionId = String(body.sessionId || "");
    if (!/^[A-Za-z0-9_-]{6,80}$/.test(sessionId))
      return json(res, 400, { error: "bad session id" });
    try {
      const r = await fetch(
        `${base}/api/sessions/${encodeURIComponent(sessionId)}/messages`,
        {
          headers: { Authorization: `Bearer ${key}` },
          signal: AbortSignal.timeout(15000),
        },
      );
      if (!r.ok) return json(res, 200, { messages: [] });
      const data = await r.json();
      /* The API returns the transcript under `data`, NOT `messages`: reading
         the wrong field silently yielded 0 messages and an empty panel while
         the session itself had resumed correctly. Accept either. */
      const raw = Array.isArray(data && data.data)
        ? data.data
        : Array.isArray(data && data.messages)
          ? data.messages
          : [];
      const messages = raw
        .filter((m) => m && (m.role === "user" || m.role === "assistant"))
        .map((m) => ({
          role: m.role,
          content: typeof m.content === "string" ? m.content : "",
        }))
        .filter((m) => m.content && !m.content.startsWith("[READING CONTEXT"))
        .filter((m) => !m.content.startsWith("You are Hermes,"))
        .filter((m) => !m.content.startsWith("[Reminder:"))
        .slice(-40);
      return json(res, 200, { messages });
    } catch {
      return json(res, 200, { messages: [] });
    }
  }

  if (verb === "chat") {
    const sessionId = String(body.sessionId || "");
    const input = String(body.input || "");
    const images = Array.isArray(body.images)
      ? body.images.filter((s) => typeof s === "string" && s.startsWith("data:image/")).slice(0, 4)
      : [];
    /* Session ids are Hermes-minted (api_<epoch>_<hex>); anything else is a
       path-traversal attempt, not a session. */
    if (!/^[A-Za-z0-9_-]{6,80}$/.test(sessionId)) {
      return json(res, 400, { error: "bad session id" });
    }
    if (!input.trim() && !images.length) return json(res, 400, { error: "empty input" });

    /* Multimodal: attached images travel as OpenAI vision content parts. */
    const messagePayload = images.length
      ? [
          { type: "text", text: input },
          ...images.map((url) => ({ type: "image_url", image_url: { url } })),
        ]
      : input;

    let upstream;
    try {
      upstream = await fetch(
        `${base}/api/sessions/${encodeURIComponent(sessionId)}/chat/stream`,
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${key}`,
            "Content-Type": "application/json",
            Accept: "text/event-stream",
          },
          body: JSON.stringify({ message: messagePayload }),
        },
      );
    } catch {
      return json(res, 502, { error: "Hermes is not reachable." });
    }
    if (!upstream.ok || !upstream.body) {
      const detail = upstream.body ? (await upstream.text()).slice(0, 400) : "";
      return json(res, 502, { error: `Hermes ${upstream.status}`, detail });
    }

    res.writeHead(200, {
      "Content-Type": "text/event-stream; charset=utf-8",
      "Cache-Control": "no-cache, no-transform",
      Connection: "keep-alive",
      "X-Accel-Buffering": "no",
    });
    /* Abort the upstream turn if the reader closes the panel or navigates. */
    const reader = upstream.body.getReader();
    let closed = false;
    res.on("close", () => {
      closed = true;
      reader.cancel().catch(() => {});
    });
    try {
      for (;;) {
        const { done, value } = await reader.read();
        if (done || closed) break;
        res.write(Buffer.from(value));
      }
    } catch {
      /* upstream died mid-stream: the client sees the stream end and recovers */
    }
    if (!closed) res.end();
    return undefined;
  }

  return json(res, 404, { error: "unknown verb" });
}

/* Vite dev-server plugin. Production uses api/hermes.js over the same handler. */
export function hermesTutorProxy(env) {
  return {
    name: "prime-books-hermes-proxy",
    configureServer(server) {
      server.middlewares.use((req, res, next) => {
        const m = (req.url || "").match(/^\/hermes\/([a-z]+)(?:\?|$)/);
        if (!m) return next();
        handleHermes(req, res, m[1], env).catch((err) => {
          if (!res.headersSent) json(res, 500, { error: String(err && err.message) });
          else
            try {
              res.end();
            } catch {}
        });
      });
    },
  };
}
