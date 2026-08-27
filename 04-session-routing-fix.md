# 04 - Session Routing Fix

Each book URL is its own resumable Hermes session. Book A maps to session A,
Book B to session B. Closing a tab and returning resumes that book's session; a
"+ new session" icon starts a fresh, empty one.

## The bug and its root cause

The original symptom: every visit minted a duplicate Hermes session, so a pupil
returning to a book lost the conversation. The root cause was the frontend
calling the Hermes api_server with no stable session id: nothing tied a book
back to the session it had already created, so each mount created a new one.

## The fix

This is implemented and shipped. The pieces and where they live:

### 1. A stable session key from the book's URL path

`public/pb-router.js` gives every book a slugged URL:

- `PREFIX = "/book/"` (line 31)
- `slugFromPath()` (line 34) derives the slug from `location.pathname`, and
  accepts only `^[a-z0-9-]{3,80}$` (lowercase, digits, hyphens), so the key is
  the slugified book path, never a hostile or hand-typed string.

### 2. sessionKey to sessionId in localStorage

`public/hermes-chat.js`:

- `STORE = "pb.tutor.sessions.v1"` (line 36)
- `loadMap()` / `saveMap()` (lines 71-88) read and write a JSON map
  `bookKey -> sessionId` in `localStorage` (deliberately not `sessionStorage`,
  so the mapping survives closing the tab).
- `onBookOpen()` (line 896) sets `state.bookKey` from the book-open event, and
  when the book changes it drops the old handle and loads the stored id for the
  new book.

### 3. Resume on mount, else create and store

`ensureSession()` (lines 601-651):

- If `state.sessionId` is set, return it.
- If `map[key]` holds an id, resume it (and mark the book already briefed).
- Otherwise POST `/hermes/session`, read the returned `sessionId`, and store it
  under the book key.

The server half is `api/hermes.js`, verb `session` (lines 103-135), which POSTs
to the Hermes backend's `/api/sessions` and returns the new session id.

### 4. Every chat call sends the id

`send()` (lines 653-717) resolves the id via `ensureSession()` and sends it in
the body `{ sessionId, input }` to `/hermes/chat`. The server half is
`api/hermes.js`, verb `chat` (lines 178-228), which forwards to the backend's
`/api/sessions/{id}/chat/stream` and relays the SSE stream back.

### 5. The "+ new session" icon clears and re-mints

`newSession()` (lines 406-430) deletes the stored mapping for this book, clears
the transcript, and nulls the handle, so the next question creates a fresh
session. The "+" button (line 980) and the `/new` command (line 459) both route
here. A `/model` change also calls `newSession()` because a session's model is
pinned at creation.

### 6. Returning readers rehydrate the transcript

`restoreFor()` (line 845) POSTs `/hermes/history`, whose server half is
`api/hermes.js`, verb `history` (lines 137-176), which reads the backend's
`/api/sessions/{id}/messages` and returns the trimmed transcript, so a reload
repaints the conversation rather than an empty rail.

## Endpoints, in one line each

- `/hermes/health`  checks the backend is configured and reachable.
- `/hermes/session`  create a session (POST /api/sessions).
- `/hermes/chat`  stream a turn (POST /api/sessions/{id}/chat/stream).
- `/hermes/history`  rehydrate one book's transcript (GET /api/sessions/{id}/messages).
- `/hermes/models`  feed the /model picker.

`vercel.json` rewrites these onto the single `api/hermes.js` function; the dev
proxy `tools/hermes-proxy.mjs` mirrors the same verbs and the same closed trust
boundary (the key never reaches the browser).

## Verification

`tools/verify_session_resume.js` and `tools/verify_assistant.js` exercise the
behaviour end to end: open a book, ask, switch books, confirm `bookKey` changed
(a new session), return, and confirm the transcript resumes.

A full session browser (listing every session via `GET /api/sessions`) is not
wired into the panel yet; the per-book resume and the "+ new session" flow are
the parts that satisfy the requirement above.
