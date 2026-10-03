import os
import sys
import pathlib
import traceback
import importlib

PORT = int(os.environ.get("PORT", "10000"))
HOST = "0.0.0.0"

import codeskulptor
BASE = pathlib.Path(codeskulptor.__file__).parent

print(f"=== package at {BASE} ===")
for p in BASE.iterdir():
    print(" ", p.name)

# 1. Make sure the editor files are downloaded (grabber)
try:
    import codeskulptor.grabber as grabber
    print(f"=== grabber module {grabber} dir={dir(grabber)} ===")
    # try common function names
    for fname in ["grab", "grab_all", "grab_py3", "download", "fetch", "main"]:
        if hasattr(grabber, fname):
            fn = getattr(grabber, fname)
            try:
                print(f"Trying grabber.{fname}()")
                fn()
                break
            except TypeError:
                try:
                    print(f"Trying grabber.{fname}('py3')")
                    fn("py3")
                    break
                except Exception as e:
                    print(f" {fname} failed: {e}")
except Exception as e:
    print(f"grabber step failed (will continue): {e}")
    traceback.print_exc()

# 2. Show server.py signature so we can see it in Render logs
try:
    server_path = BASE / "server.py"
    print("=== server.py first 4000 chars ===")
    print(server_path.read_text()[:4000])
except Exception as e:
    print(f"Can't read server.py: {e}")

# 3. Start the real server on 0.0.0.0:$PORT
print(f"=== Starting CodeSkulptor PY3 on {HOST}:{PORT} ===")

# Try the most likely entrypoints in order
tried = []
def try_call(mod_name, func_name, kwargs):
    try:
        mod = importlib.import_module(mod_name)
        if hasattr(mod, func_name):
            fn = getattr(mod, func_name)
            print(f"Calling {mod_name}.{func_name}({kwargs})")
            fn(**kwargs)
            return True
    except SystemExit:
        return True
    except Exception as e:
        tried.append(f"{mod_name}.{func_name}({kwargs}) -> {e}")
        traceback.print_exc()
    return False

# Most forks use server.main(host, port)
if try_call("codeskulptor.server", "main", {"host": HOST, "port": PORT}):
    sys.exit(0)
if try_call("codeskulptor.server", "main", {"port": PORT}):
    sys.exit(0)
if try_call("codeskulptor.server", "run", {"host": HOST, "port": PORT}):
    sys.exit(0)
if try_call("codeskulptor.server", "run_py3", {"host": HOST, "port": PORT}):
    sys.exit(0)
if try_call("codeskulptor.server", "serve_py3", {"host": HOST, "port": PORT}):
    sys.exit(0)

# Fallback to __main__ with CLI args (this is what `codeskulptor-py3` does)
print("Fallback to CLI args:", tried)
sys.argv = ["codeskulptor-py3", "--host", HOST, "--port", str(PORT)]
try:
    import codeskulptor.__main__
except SystemExit:
    pass
except Exception:
    traceback.print_exc()
    # Last resort: serve bin/py3 if it exists
    candidate = BASE / "bin" / "py3"
    if not candidate.exists():
        candidate = BASE / "bin"
    if candidate.exists():
        os.chdir(str(candidate))
        print(f"LAST RESORT serving static from {candidate}")
        import http.server, socketserver
        socketserver.TCPServer.allow_reuse_address = True
        with socketserver.ThreadingTCPServer((HOST, PORT), http.server.SimpleHTTPRequestHandler) as httpd:
            httpd.serve_forever()