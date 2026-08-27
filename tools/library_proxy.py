"""Prime Books single-port proxy.

Serves two things on one port (default 8765):

  /library/<path>  -> static files from public/library/ (the live flipbook PDFs
                      and covers, straight from disk, so a rebuild shows on
                      refresh with no deploy)
  everything else  -> streamed through to the local Hermes API on 127.0.0.1:8643

The ngrok tunnel points at THIS port, so one stable public URL serves both the
assistant API and the live book files.
"""
import http.client
import mimetypes
import os
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ROOT = r"C:\Users\alexa\Documents\GitHub\prime-books"
LIBRARY = os.path.join(ROOT, "public", "library")
HERMES_HOST = "127.0.0.1"
HERMES_PORT = 8643

mimetypes.add_type("application/pdf", ".pdf")
mimetypes.add_type("image/webp", ".webp")
mimetypes.add_type("application/json", ".json")


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *args):
        pass  # quiet

    def _serve_file(self, relpath):
        # /library.json maps to public/library.json (the manifest), not
        # public/library/library.json
        base = ROOT + os.sep + "public" if relpath == "library.json" else LIBRARY
        full = os.path.normpath(os.path.join(base, relpath))
        allowed = os.path.normpath(LIBRARY)
        if not (full.startswith(allowed) or full == os.path.normpath(os.path.join(ROOT, "public", "library.json"))):
            self.send_error(403)
            return
        if not os.path.isfile(full):
            self.send_error(404)
            return
        ctype = mimetypes.guess_type(full)[0] or "application/octet-stream"
        size = os.path.getsize(full)
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(size))
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        with open(full, "rb") as f:
            while True:
                chunk = f.read(65536)
                if not chunk:
                    break
                self.wfile.write(chunk)

    def _forward(self):
        # build upstream request
        body_len = int(self.headers.get("Content-Length") or 0)
        body = self.rfile.read(body_len) if body_len else b""
        conn = http.client.HTTPConnection(HERMES_HOST, HERMES_PORT, timeout=300)
        headers = {k: v for k, v in self.headers.items() if k.lower() not in ("host", "connection", "content-length")}
        try:
            conn.request(self.command, self.path, body=body, headers=headers)
            resp = conn.getresponse()
        except Exception as e:
            try:
                self.send_response(502)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(('{"error":"upstream unreachable: %s"}' % e).encode())
            except Exception:
                pass
            return
        # stream response back (works for SSE chat streaming)
        self.send_response(resp.status)
        for k, v in resp.getheaders():
            if k.lower() not in ("transfer-encoding", "connection"):
                self.send_header(k, v)
        self.send_header("Connection", "keep-alive")
        self.end_headers()
        try:
            while True:
                chunk = resp.read(65536)
                if not chunk:
                    break
                self.wfile.write(chunk)
        except Exception:
            pass
        finally:
            conn.close()

    def _handle(self):
        path = self.path.split("?")[0]
        if path.startswith("/library") and (len(path) == len("/library") or path[len("/library")] in ("/", ".")):
            if path.startswith("/library/"):
                rel = path[len("/library/"):]
            else:
                # /library.json -> serve library.json
                rel = path[1:]
            if self.command == "GET" and rel:
                self._serve_file(rel)
                return
        self._forward()

    def do_GET(self):
        self._handle()

    def do_POST(self):
        self._handle()

    def do_PUT(self):
        self._handle()

    def do_DELETE(self):
        self._handle()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,PUT,DELETE,OPTIONS")
        self.end_headers()


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    srv = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print(f"proxy on 127.0.0.1:{port}  library={LIBRARY}  hermes={HERMES_HOST}:{HERMES_PORT}")
    srv.serve_forever()