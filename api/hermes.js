/* Vercel serverless function for the AI assistant.
 *
 * Same three verbs as the dev proxy, same closed switch, same trust boundary:
 * the key lives in Vercel's environment, never in the browser.
 *
 * Routes: /hermes/health | /hermes/session | /hermes/chat
 * (see vercel.json for the rewrite that maps those onto this function).
 *
 * REQUIRED Vercel environment variables - WITHOUT THEM THIS RETURNS 503 AND THE
 * RAIL SHOWS AS OFFLINE, which is the intended behaviour until a publicly
 * reachable Hermes exists:
 *   HERMES_BASE_URL   e.g. https://hermes.example.com  (a tunnel or a VPS)
 *   HERMES_API_KEY    that instance's API_SERVER_KEY
 *   HERMES_MODEL      e.g. z-ai/glm-5.2
 *   HERMES_PROVIDER   e.g. openrouter
 *
 * WORKSHOP MODE (optional) - lets the site route "edit the book" requests to a
 * SECOND Hermes that owns the manuscript and build tools (the authoring
 * profile). Enabled by setting:
 *   AUTHORING_BASE_URL   e.g. https://your-tunnel.example.com
 *   AUTHORING_API_KEY    that instance's API_SERVER_KEY
 *   EDIT_PASSWORD        (optional) if set, authoring requests must include
 *                        `editPassword`; if left empty, authoring is OPEN.
 *
 * SECURITY NOTE: exposing a Hermes API server to the public internet exposes an
 * agent that can run terminal commands. Only point HERMES_BASE_URL at an
 * instance whose profile has a deliberately minimal toolset (the
 * primebooks-tutor profile uses `safe`), and keep the key secret. The authoring
 * endpoint has file + terminal tools by design - gate it with EDIT_PASSWORD or
 * keep it off the public internet.
 */
export const config = { runtime: "nodejs" };

const MAX_BODY = 10 * 1024 * 1024; /* images arrive as base64 data URLs */

function cfg() {
  return {
    base: (process.env.HERMES_BASE_URL || "").replace(/\/+$/, ""),
    key: process.env.HERMES_API_KEY || "",
    model: process.env.HERMES_MODEL || "",
    provider: process.env.HERMES_PROVIDER || "",
    authoringBase: (process.env.AUTHORING_BASE_URL || "").replace(/\/+$/, ""),
    authoringKey: process.env.AUTHORING_API_KEY || "",
    editPassword: process.env.EDIT_PASSWORD || "",
  };
}

function uniqueTitle(raw) {
  const clean = String(raw || "Prime Books")
    .replace(/[\r\n\t]+/g, " ")
    .trim()
    .slice(0, 80);
  return `${clean} · ${new Date().toISOString().slice(0, 19).replace("T", " ")}`;
}

export default async function handler(req, res) {
  const { base, key, model, provider, authoringBase, authoringKey, editPassword } = cfg();
  const verb = String((req.query && req.query.verb) || "")
    .toLowerCase()
    .replace(/[^a-z]/g, "");

  res.setHeader("Cache-Control", "no-store");
  res.setHeader("X-Content-Type-Options", "nosniff");

  if (verb === "health") {
    if (!base || !key) return res.status(200).json({ ok: false, configured: false });
    try {
      const r = await fetch(`${base}/health`, {
        headers: { Authorization: `Bearer ${key}` },
        signal: AbortSignal.timeout(4000),
      });
      return res.status(200).json({ ok: r.ok, configured: true });
    } catch {
      return res.status(200).json({ ok: false, configured: true });
    }
  }

  if (!base || !key)
    return res
      .status(503)
      .json({ error: "The AI assistant is not configured on this server." });
  if (req.method !== "POST") return res.status(405).json({ error: "POST only" });

  const body = typeof req.body === "object" && req.body ? req.body : {};
  if (JSON.stringify(body).length > MAX_BODY)
    return res.status(413).json({ error: "body too large" });

  /* Workshop routing: a request tagged mode=authoring/workshop goes to the
     authoring Hermes instead of the reading one. Gated by EDIT_PASSWORD when
     that env var is set; open when it is not. */
  const mode = String((body.mode || "")).toLowerCase();
  const authoring = mode === "authoring" || mode === "workshop";
  if (authoring) {
    if (!authoringBase || !authoringKey)
      return res.status(503).json({ error: "Editing is not configured on this server." });
    if (editPassword && body.editPassword !== editPassword)
      return res.status(403).json({ error: "Editing is locked. Provide the edit password." });
  }
  const upBase = authoring ? authoringBase : base;
  const upKey = authoring ? authoringKey : key;

  if (verb === "models") {
    /* Feed the /model command. Mirrors the dev proxy's `models` verb exactly:
       /api/model/options is the rich picker payload (/v1/models advertises the
       agent as a single model and is the wrong surface). Flattened and capped so
       the browser gets names only. */
    try {
      const r = await fetch(`${base}/api/model/options`, {
        headers: { Authorization: `Bearer ${key}` },
        signal: AbortSignal.timeout(10000),
      });
      if (!r.ok) return res.status(200).json({ models: [], current: model });
      const data = await r.json();
      const out = [];
      for (const p of (data && data.providers) || []) {
        for (const m of p.models || []) {
          out.push({ provider: p.slug, model: m, current: !!p.is_current });
          if (out.length >= 200) break;
        }
        if (out.length >= 200) break;
      }
      return res
        .status(200)
        .json({ models: out, current: model, currentProvider: provider });
    } catch {
      return res.status(200).json({ models: [], current: model });
    }
  }

  if (verb === "session") {
    const payload = { title: uniqueTitle(body.title) };
    /* Optional workspace binding: groups the session under a Project in the
       Hermes desktop/TUI sidebar (cwd -> git repo root is the project key). */
    if (typeof body.cwd === "string" && body.cwd.trim()) payload.cwd = body.cwd.trim();
    if (typeof body.project === "string" && body.project.trim()) payload.project = body.project.trim();
    /* Honour a model chosen in the panel with /model, validated by shape. Kept
       identical to tools/hermes-proxy.mjs so dev and prod cannot diverge. */
    const wantModel = typeof body.model === "string" ? body.model.trim() : "";
    const wantProvider =
      typeof body.provider === "string" ? body.provider.trim() : "";
    const okId = (s) => /^[A-Za-z0-9._\/:-]{2,80}$/.test(s);
    if (wantModel && okId(wantModel)) payload.model = wantModel;
    else if (model) payload.model = model;
    if (wantProvider && okId(wantProvider)) payload.provider = wantProvider;
    else if (provider) payload.provider = provider;
    try {
      const r = await fetch(`${upBase}/api/sessions`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${upKey}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
        signal: AbortSignal.timeout(20000),
      });
      const text = await r.text();
      if (!r.ok)
        return res.status(502).json({ error: `Hermes ${r.status}`, detail: text.slice(0, 400) });
      const data = JSON.parse(text);
      const sessionId = data && data.session && data.session.id;
      if (!sessionId) return res.status(502).json({ error: "No session id in response." });
      return res.status(200).json({ sessionId, title: data.session.title });
    } catch {
      return res.status(502).json({ error: "Hermes is not reachable." });
    }
  }

  if (verb === "history") {
    /* Rehydrate a returning reader's panel from the SERVER transcript, so
       coming back to a book shows the conversation rather than an empty rail.
       Read-only, and the reply is trimmed to what the panel renders. */
    const sessionId = String(body.sessionId || "");
    if (!/^[A-Za-z0-9_-]{6,80}$/.test(sessionId))
      return res.status(400).json({ error: "bad session id" });
    try {
      const r = await fetch(
        `${upBase}/api/sessions/${encodeURIComponent(sessionId)}/messages`,
        {
          headers: { Authorization: `Bearer ${upKey}` },
          signal: AbortSignal.timeout(15000),
        },
      );
      if (!r.ok) return res.status(200).json({ messages: [] });
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
      return res.status(200).json({ messages });
    } catch {
      return res.status(200).json({ messages: [] });
    }
  }

  if (verb === "chat") {
    const sessionId = String(body.sessionId || "");
    const input = String(body.input || "");
    const images = Array.isArray(body.images)
      ? body.images.filter((s) => typeof s === "string" && s.startsWith("data:image/")).slice(0, 4)
      : [];
    if (!/^[A-Za-z0-9_-]{6,80}$/.test(sessionId))
      return res.status(400).json({ error: "bad session id" });
    if (!input.trim() && !images.length)
      return res.status(400).json({ error: "empty input" });

    /* Multimodal: when images are attached, send OpenAI vision content parts
       instead of a plain string. The Hermes API server accepts both shapes on
       /api/sessions/{id}/chat/stream. Text parts carry the full composed
       prompt (briefing + reading context + question). */
    const messagePayload = images.length
      ? [
          { type: "text", text: input },
          ...images.map((url) => ({ type: "image_url", image_url: { url } })),
        ]
      : input;

    let upstream;
    try {
      upstream = await fetch(
        `${upBase}/api/sessions/${encodeURIComponent(sessionId)}/chat/stream`,
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${upKey}`,
            "Content-Type": "application/json",
            Accept: "text/event-stream",
          },
          body: JSON.stringify({ message: messagePayload }),
        },
      );
    } catch {
      return res.status(502).json({ error: "Hermes is not reachable." });
    }
    if (!upstream.ok || !upstream.body)
      return res.status(502).json({ error: `Hermes ${upstream.status}` });

    res.writeHead(200, {
      "Content-Type": "text/event-stream; charset=utf-8",
      "Cache-Control": "no-cache, no-transform",
      Connection: "keep-alive",
      "X-Accel-Buffering": "no",
    });
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
      /* upstream ended: the client sees the stream close and recovers */
    }
    if (!closed) res.end();
    return undefined;
  }

  return res.status(404).json({ error: "unknown verb" });
}
