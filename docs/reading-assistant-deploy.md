# Deploying the reading assistant

The site works on Vercel with no Hermes at all: the rail simply shows "offline".
Everything below is only needed to make the AI answer on the public site.

## The shape

```
visitor's browser
  |  fetch /hermes/chat            (no key, ever)
  v
Vercel function  api/hermes.js     HERMES_BASE_URL + HERMES_API_KEY live here
  |  https://<your hermes>/api/sessions/...
  v
Hermes on a public host           (spawned VM, Hermes Cloud, tunnel)
```

The browser never sees the key and can only reach three verbs
(`health`, `session`, `chat`). The upstream path is derived server-side, so a
visitor cannot address any other Hermes endpoint.

## What you set in Vercel

Project → Settings → Environment Variables:

| Name | Value | Notes |
| --- | --- | --- |
| `HERMES_BASE_URL` | `https://your-hermes-host` | no trailing slash |
| `HERMES_API_KEY` | that instance's `API_SERVER_KEY` | secret |
| `HERMES_MODEL` | e.g. `z-ai/glm-5.2` | must be a real model id |
| `HERMES_PROVIDER` | e.g. `openrouter` | |

Redeploy after adding them. Until all four exist, `/hermes/health` reports
`configured:false` and the rail says offline. That is deliberate.

## On the Hermes host

The API server must be enabled and reachable:

```
API_SERVER_ENABLED=true
API_SERVER_HOST=0.0.0.0        # 127.0.0.1 is unreachable from Vercel
API_SERVER_PORT=8643
API_SERVER_KEY=<long random>
```

Do NOT set `API_SERVER_MODEL_NAME`: it defaults to the profile name and is sent
to the provider as a literal model id, which fails with
`HTTP 400: <profile> is not a valid model ID`. The model is pinned per session by
the proxy instead.

### Use a READ-ONLY profile for the public rail

The authoring profile has `file` and `terminal`. Publishing that is publishing a
remote shell. For the public instance:

```yaml
platform_toolsets:
  api_server:
    - safe
```

The rail degrades honestly: a reader asking for an edit is told that editing
happens in the workshop.

## REMOTE vs LOCAL mode, and why it matters

`public/hermes-chat.js` sets `REMOTE` from `location.hostname`. It changes what
the agent is told:

| | LOCAL (localhost) | REMOTE (deployed) |
| --- | --- | --- |
| Manuscript path | given | withheld |
| `buildable` flag | given | withheld |
| Authoring instructions | given | replaced by "reading companion" |
| Book reference | absolute MEGA path | public `https://.../books/...pdf` |

A remote Hermes has no `C:\Users\alexa\...`, so sending those paths would invite
it to hallucinate file reads. It gets a URL it can actually fetch.

The page text is always sent regardless, extracted by pdf.js in the browser, so
the agent usually needs no download at all.

## Two manifests

`tools/sync_books.py` writes both:

- `public/books-manifest.json` — deployed. `year, subject, pages, mb, pdf` only.
- `public/books-manifest.local.json` — gitignored. Adds `src`, `book_dir`,
  `markdown`, `buildable` for the local authoring assistant.

Never deploy the local one: it publishes the folder layout of the masters.
`index.html` tries the local file first and falls back, so the same build works
in both places.

## Verify

```
node tools/verify_public_mode.js    # deployed shape: no paths leak, no authoring
node tools/verify_art_year1.js      # local shape: reads the real manuscript
bash tools/probe_proxy_security.sh  # key never reaches the browser
curl -s https://<site>/hermes/health
```

`verify_public_mode.js` forces remote mode with `window.__PB_FORCE_REMOTE`, so it
proves the deployed behaviour without deploying.

## Pitfalls

- **A quick Cloudflare tunnel URL changes on every restart.** Measured: SSE and a
  75s silent gap DO pass through one (contradicting Cloudflare's own docs), but
  the churn means re-editing the Vercel variable constantly. A named tunnel needs
  a domain on Cloudflare DNS.
- **`hermes gateway run` in a shell dies with that shell.** Use
  `hermes -p <profile> gateway install` so it survives.
- Session titles must be unique per instance, or create returns
  `400 invalid_title`. The proxy appends a timestamp.
- The session id is at `session.id`, not `session_id`.
