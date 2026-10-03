import os
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = int(os.environ.get("PORT", 10000))

HTML = r"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>sigpy - CodeSkulptor Py3</title>
<script src="https://cdn.jsdelivr.net/npm/skulpt@1.2.0/dist/skulpt.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/skulpt@1.2.0/dist/skulpt-stdlib.js"></script>
<style>
  body{margin:0;font-family:monospace;background:#1e1e1e;color:#eee;display:flex;flex-direction:column;height:100vh}
  header{padding:10px 16px;background:#111;border-bottom:1px solid #333;display:flex;justify-content:space-between;align-items:center}
  header a{color:#6af;text-decoration:none}
  main{display:flex;flex:1;overflow:hidden}
  #left{flex:1;display:flex;flex-direction:column;padding:8px}
  #right{flex:1;display:flex;flex-direction:column;border-left:1px solid #333;background:#000}
  textarea{flex:1;background:#1e1e1e;color:#d4d4d4;border:1px solid #333;padding:10px;font-size:14px;resize:none;outline:none}
  #output{flex:1;overflow:auto;padding:10px;white-space:pre-wrap;background:#000;color:#0f0}
  button{background:#0a84ff;color:white;border:0;padding:8px 18px;cursor:pointer;border-radius:4px;font-weight:bold}
  button:hover{background:#0066cc}
</style>
</head>
<body>
<header>
  <div><b>sigpy</b> - Python 3 editor (CodeSkulptor Py3 compatible) - on Render</div>
  <div><a href="https://py3.codeskulptor.org/" target="_blank">original py3.codeskulptor.org</a></div>
</header>
<main>
  <div id="left">
    <div style="margin-bottom:6px"><button onclick="runCode()">▶ Run (Python 3)</button> <button onclick="clearOut()">Clear</button></div>
    <textarea id="code">print("Hello from sigpy.onrender.com!")
# Try CodeSkulptor style
for i in range(5):
    print(f"count {i}")

# simple input example
# name = input("name? ")
# print("hi", name)
</textarea>
  </div>
  <div id="right">
    <div style="padding:8px;border-bottom:1px solid #333;background:#111">Console</div>
    <div id="output"></div>
  </div>
</main>
<script>
function outf(text){ document.getElementById("output").innerText += text; }
function builtinRead(x){ if(Sk.builtinFiles===undefined||Sk.builtinFiles["files"][x]===undefined) throw "File not found: '"+x+"'"; return Sk.builtinFiles["files"][x]; }
function clearOut(){ document.getElementById("output").innerText=""; }
function runCode(){
  clearOut();
  Sk.configure({output:outf, read:builtinRead, __future__: Sk.python3});
  var prog = document.getElementById("code").value;
  Sk.misceval.asyncToPromise(function(){ return Sk.importMainWithBody("<stdin>", false, prog, true); })
  .catch(function(err){ outf(err.toString()+"\n"); });
}
</script>
</body>
</html>
"""

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self.send_response(200)
            self.send_header("Content-type","text/html")
            self.end_headers()
            self.wfile.write(HTML.encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not found - go to /")
    def log_message(self, format, *args):
        print("%s - - [%s] %s" % (self.client_address[0], self.log_date_time_string(), format%args))

print(f"Starting Py3 editor on 0.0.0.0:{PORT}")
HTTPServer(("0.0.0.0", PORT), Handler).serve_forever()