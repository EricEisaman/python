import os
import pathlib
import http.server
import socketserver

# Render injects PORT, free tier needs 0.0.0.0
PORT = int(os.environ.get("PORT", "10000"))

# Locate the static files that come with the package
try:
    import codeskulptor
    base = pathlib.Path(codeskulptor.__file__).parent
    # try to find index.html - handles both py2 and py3 layouts
    indexes = list(base.rglob("index.html"))
    if indexes:
        # prefer the py3 folder if both exist
        py3 = [p for p in indexes if "py3" in str(p).lower() or "python3" in str(p).lower()]
        serve_dir = str((py3[0] if py3 else indexes[0]).parent)
    else:
        serve_dir = str(base)
    os.chdir(serve_dir)
    print(f"Serving CodeSkulptor from: {serve_dir}")
except Exception as e:
    print(f"Could not auto-locate codeskulptor files: {e}")
    print(f"Serving from current dir: {os.getcwd()}")

class Handler(http.server.SimpleHTTPRequestHandler):
    # quiet the logs a bit, but keep 200s
    def log_message(self, format, *args):
        print("%s - - [%s] %s" % (self.client_address[0],
                                  self.log_date_time_string(),
                                  format%args))

socketserver.TCPServer.allow_reuse_address = True
with socketserver.ThreadingTCPServer(("0.0.0.0", PORT), Handler) as httpd:
    print(f"Listening on 0.0.0.0:{PORT}")
    httpd.serve_forever()