import { defineConfig } from "vite";
import { readFileSync } from "node:fs";
import { hermesTutorProxy } from "./tools/hermes-proxy.mjs";

/* Prime Books - Vite config.
 *
 * The site itself is a static single-file app (index.html); Vite is only the
 * dev server and the build step. The one piece of real configuration here is
 * the reading-assistant proxy.
 *
 * WHY A PROXY AT ALL: the Hermes API server key grants the agent's FULL
 * toolset, which includes running terminal commands. Putting that key in
 * index.html would hand remote code execution to anyone who views source. So
 * the browser never sees it: it calls /hermes/<verb> on the dev server, and
 * this plugin attaches the bearer token server-side and forwards to Hermes on
 * loopback. The verb list is closed (see tools/hermes-proxy.mjs), so the
 * browser cannot address an arbitrary Hermes endpoint even if the page is
 * compromised.
 *
 * Config lives in .env.local at the repo root (gitignored):
 *   HERMES_BASE_URL=http://127.0.0.1:8643
 *   HERMES_API_KEY=<the API_SERVER_KEY of the primebooks-tutor profile>
 *   HERMES_MODEL=z-ai/glm-5.2
 *   HERMES_PROVIDER=openrouter
 */
function readEnvLocal() {
  const env = {};
  try {
    const text = readFileSync(new URL(".env.local", import.meta.url), "utf8");
    for (const line of text.split(/\r?\n/)) {
      const m = line.match(/^\s*([A-Z0-9_]+)\s*=\s*(.*)\s*$/);
      if (m) env[m[1]] = m[2].replace(/^["']|["']$/g, "");
    }
  } catch {
    /* no .env.local: the proxy replies 503 and the rail shows as offline */
  }
  return env;
}

export default defineConfig(() => {
  const env = readEnvLocal();
  return {
    /* mpa, not the default spa: the default makes Vite serve index.html for
       ANY missing path, so a typo in a PDF or cover URL returned HTML and
       pdf.js choked on it (InvalidPDFException) instead of a clean 404. With
       mpa, the ONLY path that falls back to index.html is /book/<slug>,
       handled explicitly by bookDeepLinkFallback() below. */
    appType: "mpa",
    plugins: [hermesTutorProxy(env), bookDeepLinkFallback()],
    server: {
      host: "127.0.0.1",
      port: 5173,
      allowedHosts: [".ngrok-free.dev", ".ngrok.app"],
      hmr: { protocol: "ws", clientPort: 5173 },
    },
  };
});

/* Serve index.html for /book/<slug> deep links.
 *
 * Every book has its own URL (public/pb-router.js). In-app navigation is
 * pushState so it always works, but a FIRST visit to /book/y01-art-and-design
 * is a real HTTP request for a file that does not exist. Without this the
 * feature looks perfect while developing and 404s for anyone you send a link
 * to. Vercel gets the same treatment in vercel.json.
 *
 * Scoped to /book/ only: a catch-all fallback would swallow genuine 404s for
 * missing PDFs and covers and turn them into HTML, which is what made pdf.js
 * report InvalidPDFException instead of "not found". */
function bookDeepLinkFallback() {
  return {
    name: "prime-books-deep-link-fallback",
    configureServer(server) {
      server.middlewares.use((req, res, next) => {
        const path = (req.url || "").split("?")[0];
        if (/^\/book\/[a-z0-9-]+\/?$/.test(path)) req.url = "/index.html";
        next();
      });
    },
  };
}
