# Web editing (workshop mode)

Lets the deployed site edit books the way localhost already can: ask the
assistant to change a title, a page or an exercise and it edits the manuscript
and rebuilds.

## What changed

- `api/hermes.js` — a request tagged `mode: "authoring"` is routed to a second
  Hermes (the authoring/workshop instance) instead of the read-only one, gated
  by an optional `EDIT_PASSWORD`.
- `public/hermes-chat.js` — an **Edit** button and a `/workshop` command toggle
  workshop mode. When on, the panel sends the authoring briefing ("you CAN edit
  this book") and routes to the authoring backend. Reading and workshop sessions
  are namespaced so they never share a thread.

## The two Hermes instances

| | Reading assistant (public) | Authoring assistant (workshop) |
|---|---|---|
| Where | cloud VM (this host) | your Windows machine |
| Toolset | `safe` (web + vision only) | `file` + `terminal` |
| Has the book files? | no | yes (MEGA tree) |
| Key | `HERMES_API_KEY` | `AUTHORING_API_KEY` |

The whole point of workshop mode is to reach the authoring instance from the
deployed site.

## Activate it (3 steps)

### 1. Expose the authoring Hermes with a tunnel

On the Windows machine, run (any cloudflare tunnel tool):

```
cloudflared tunnel --url http://127.0.0.1:8643
```

It prints a URL like `https://some-name.trycloudflare.com`.

> The authoring Hermes lives at `C:\Users\alexa\AppData\Local\hermes\profiles\primebooks-tutor`
> and serves its API on `127.0.0.1:8643` (see `tools/probe_authoring.sh`).

### 2. Set the Vercel environment variables

```
AUTHORING_BASE_URL = https://some-name.trycloudflare.com
AUTHORING_API_KEY  = <the API_SERVER_KEY in that profile's .env>
EDIT_PASSWORD      = (optional) leave EMPTY for open editing; set it to lock
```

Redeploy (or `vercel env` + a new deploy) so the function picks them up.

### 3. Use it

On the site, open a book and either click **Edit** or type `/workshop`. The
panel announces "Workshop mode ON". Then:

```
change the cover title from "Global Perspectives" to "Global Perspectives Test"
```

The authoring assistant edits the manuscript and rebuilds. Re-sync and the new
title appears on the cover, the PDF and the catalogue.

`/workshop off` (or clicking Edit again) returns to the read-only companion.

## Security (read this)

- `EDIT_PASSWORD` empty = **anyone on the site can edit your books**. That is
  the requested default, but it is genuinely open: any visitor can type
  `/workshop` and start editing.
- To lock it, set `EDIT_PASSWORD` to a secret. The panel then prompts once for
  it and remembers it locally. This is the one-line lock that makes editing
  yours alone.
- The tunnel is the other gate: if you use `cloudflared tunnel --url` it is
  open to whoever has the URL; use Cloudflare Access (or a private tunnel) for a
  real login. Keep `AUTHORING_API_KEY` out of the browser bundle.

## Verification

- `node tools/verify_session_resume.js` still passes (reading path unchanged).
- `/workshop` on the deployed site routes to the authoring Hermes (check the
  tunnel logs) and a title change actually rebuilds.
- `node --check api/hermes.js` and `node --check public/hermes-chat.js` are
  clean.
