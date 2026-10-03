import os
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = int(os.environ.get("PORT", 10000))

# read favicon files at startup
def load_favicon(name, default=b""):
    try:
        with open(name, "rb") as f:
            return f.read()
    except:
        return default

FAVICON_ICO = load_favicon("favicon.ico")
FAVICON_32 = load_favicon("favicon-32.png")

HTML = r"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>sigpy - σπ</title>
<link rel="icon" type="image/x-icon" href="/favicon.ico">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="apple-touch-icon" href="/favicon-180.png">
<script src="https://cdn.jsdelivr.net/npm/skulpt@1.2.0/dist/skulpt.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/skulpt@1.2.0/dist/skulpt-stdlib.js"></script>
<style>
  body{margin:0;font-family:monospace;background:#1e1e1e;color:#eee;display:flex;flex-direction:column;height:100vh}
  header{padding:10px 16px;background:#111;border-bottom:1px solid #333;display:flex;justify-content:space-between}
  main{display:flex;flex:1;overflow:hidden}
  #left{flex:1;display:flex;flex-direction:column;padding:8px}
  #right{flex:1;display:flex;flex-direction:column;border-left:1px solid #333;background:#000}
  textarea{flex:1;background:#1e1e1e;color:#d4d4d4;border:1px solid #333;padding:10px;font-size:14px;resize:none}
  #output{flex:1;overflow:auto;padding:10px;white-space:pre-wrap;background:#000;color:#0f0}
  button{background:#0a84ff;color:white;border:0;padding:8px 18px;cursor:pointer;border-radius:4px;font-weight:bold}
</style>
</head>
<body>
<header><div><b>σπ</b> sigpy - Python 3 editor</div><div>favicon = σπ</div></header>
<main>
  <div id="left"><div style="margin-bottom:6px"><button onclick="runCode()">▶ Run</button></div>
    <textarea id="code">print("σπ favicon works!")
for i in range(3): print(f"σπ {i}")</textarea>
  </div>
  <div id="right"><div style="padding:8px;border-bottom:1px solid #333;background:#111">Console</div><div id="output"></div></div>
</main>
<script>
function outf(t){document.getElementById("output").innerText+=t}
function builtinRead(x){if(Sk.builtinFiles===undefined||Sk.builtinFiles["files"][x]===undefined)throw "File not found: '"+x+"'";return Sk.builtinFiles["files"][x]}
function runCode(){document.getElementById("output").innerText="";Sk.configure({output:outf,read:builtinRead,__future__:Sk.python3});Sk.misceval.asyncToPromise(()=>Sk.importMainWithBody("<stdin>",false,document.getElementById("code").value,true)).catch(e=>outf(e.toString()+"\n"))}
</script>
</body>
</html>
"""

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/favicon.ico":
            self.send_response(200)
            self.send_header("Content-type","image/x-icon")
            self.end_headers()
            self.wfile.write(FAVICON_ICO)
        elif self.path == "/favicon-32.png":
            self.send_response(200)
            self.send_header("Content-type","image/png")
            self.end_headers()
            self.wfile.write(FAVICON_32)
        elif self.path in ("/", "/index.html"):
            self.send_response(200)
            self.send_header("Content-type","text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML.encode())
        else:
            self.send_response(404)
            self.end_headers()
    def log_message(self, format, *args):
        print("%s %s" % (self.client_address[0], format%args))

print(f"Serving σπ on 0.0.0.0:{PORT}")
HTTPServer(("0.0.0.0", PORT), Handler).serve_forever()