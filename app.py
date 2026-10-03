import os
import json
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = int(os.environ.get("PORT", 10000))
EXAMPLES_DIR = "examples"

def load_favicon(name, default=b""):
    try:
        with open(name, "rb") as f:
            return f.read()
    except:
        return default

FAVICON_ICO = load_favicon("favicon.ico")
FAVICON_32 = load_favicon("favicon-32.png")
FAVICON_180 = load_favicon("favicon-180.png")

def list_example_files():
    try:
        if not os.path.isdir(EXAMPLES_DIR):
            return []
        files = [f for f in os.listdir(EXAMPLES_DIR) if f.endswith(".py") and os.path.isfile(os.path.join(EXAMPLES_DIR, f))]
        return sorted(files)
    except:
        return []

HTML = r"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
<title>💪🏼</title>
<link rel="icon" type="image/x-icon" href="/favicon.ico">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="apple-touch-icon" href="/favicon-180.png">
<script src="https://cdn.jsdelivr.net/npm/skulpt@1.2.0/dist/skulpt.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/skulpt@1.2.0/dist/skulpt-stdlib.js"></script>
<style>
  *{box-sizing:border-box}
  body{margin:0;font-family:monospace;background:#1e1e1e;color:#eee;display:flex;flex-direction:column;height:100vh;height:100dvh}
  header{padding:10px 12px;background:#111;border-bottom:1px solid #333;display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap}
  header b{color:#fff}
  main{display:flex;flex:1;overflow:hidden}
  #left{flex:1;display:flex;flex-direction:column;padding:8px;min-width:0;min-height:0}
  #right{flex:1;display:flex;flex-direction:column;border-left:1px solid #333;background:#000;min-width:0;min-height:0}
  #output{flex:1;overflow:auto;padding:10px;white-space:pre-wrap;background:#000;color:#0f0;font-size:13px;line-height:1.5}
  button{border:0;padding:8px 16px;cursor:pointer;border-radius:6px;font-weight:bold;font-family:monospace}
  #run-btn{background:#0a84ff;color:white}
  #run-btn:active{transform:scale(0.98)}
  
  .header-right{display:flex;gap:8px;align-items:center;flex-wrap:wrap}
  .view-controls{display:flex;gap:6px;background:#1e1e1e;padding:4px;border-radius:8px;border:1px solid #333}
  .view-btn{background:#2a2a2a;color:#aaa;font-size:12px;padding:6px 12px}
  .view-btn.active{background:#0a84ff;color:white;box-shadow:0 0 0 1px #0a84ff}
  .view-btn:hover{color:#fff;background:#333}
  .examples-select{background:#2a2a2a;color:#fff;border:1px solid #333;padding:6px 12px;border-radius:8px;font-family:monospace;font-size:12px;cursor:pointer;min-width:170px}
  .examples-select:hover{border-color:#555;color:#fff}
  .examples-select:focus{outline:none;border-color:#0a84ff}

  /* view states - full width toggle for mobile */
  main.view-editor #right{display:none !important}
  main.view-editor #left{flex:1;width:100%}
  main.view-console #left{display:none !important}
  main.view-console #right{flex:1;width:100%}
  main.view-split #left, main.view-split #right{display:flex}

  .toolbar{display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;gap:8px;flex-wrap:wrap}
  .console-title{padding:8px;border-bottom:1px solid #333;background:#111;display:flex;justify-content:space-between;align-items:center}

  /* editor with bright green line numbers matching console #0f0 */
  #editor-wrapper{display:flex;flex:1;min-height:0;background:#1e1e1e;border:1px solid #333;border-radius:6px;overflow:hidden}
  #line-numbers{
    padding:10px 8px 10px 10px;
    text-align:right;
    color:#0f0;
    background:#111;
    user-select:none;
    font-size:14px;
    line-height:1.5;
    min-width:48px;
    border-right:1px solid #222;
    overflow:hidden;
    font-family:monospace;
    font-weight:bold;
    text-shadow:0 0 6px rgba(0,255,0,0.6);
  }
  #code{
    flex:1;
    background:#1e1e1e;
    color:#d4d4d4;
    border:0;
    padding:10px;
    font-size:14px;
    resize:none;
    line-height:1.5;
    outline:none;
    overflow:auto;
    white-space:pre;
    overflow-wrap:normal;
    overflow-x:auto;
    border-radius:0;
  }

  @media (max-width: 768px){
    header{padding:8px 10px}
    main{flex-direction:column}
    main.view-split #left{flex:1 1 58%;min-height:0}
    main.view-split #right{flex:1 1 42%;min-height:180px;border-left:none;border-top:1px solid #333}
    #code{font-size:16px}
    #line-numbers{font-size:16px;min-width:52px}
    #output{font-size:13px}
    .view-btn{padding:8px 10px;font-size:13px}
    .examples-select{min-width:130px;font-size:13px;padding:8px 10px}
  }
</style>
</head>
<body>
<header>
  <div><b>σπ</b> sigpy - Python 3 editor</div>
  <div class="header-right">
    <div class="view-controls">
      <button class="view-btn" id="btn-editor" onclick="setView('editor')">📝 Editor</button>
      <button class="view-btn active" id="btn-split" onclick="setView('split')">◫ Split</button>
      <button class="view-btn" id="btn-console" onclick="setView('console')">💻 Console</button>
    </div>
    <select id="examples-select" class="examples-select" title="Load an example">
      <option value="">📚 Examples</option>
    </select>
  </div>
</header>
<main id="main" class="view-split">
  <div id="left">
    <div class="toolbar">
      <button id="run-btn" onclick="runCode()">▶ Run</button>
      <span style="font-size:11px;color:#666;display:none" id="hint-mobile">📱 tip: use ◫ for full-width</span>
    </div>
    <div id="editor-wrapper">
      <div id="line-numbers">1</div>
      <textarea id="code" spellcheck="false"># sigpy - load an example from the dropdown or write your own
print("SIGS LOVE DEM MIDS! - ready")
</textarea>
    </div>
  </div>
  <div id="right">
    <div class="console-title">
      <span>Console</span>
      <span style="display:flex;gap:6px">
        <button class="view-btn" onclick="setView('editor')" style="font-size:11px">← Editor</button>
        <button class="view-btn" onclick="clearOutput()" style="font-size:11px">Clear</button>
      </span>
    </div>
    <div id="output"></div>
  </div>
</main>
<script>
function outf(t){document.getElementById("output").innerText+=t}
function builtinRead(x){if(Sk.builtinFiles===undefined||Sk.builtinFiles["files"][x]===undefined)throw "File not found: '"+x+"'";return Sk.builtinFiles["files"][x]}
function clearOutput(){document.getElementById("output").innerText=""}

function runCode(){
  clearOutput();
  Sk.configure({output:outf,read:builtinRead,__future__:Sk.python3});
  Sk.misceval.asyncToPromise(()=>Sk.importMainWithBody("<stdin>",false,document.getElementById("code").value,true))
    .catch(e=>outf(e.toString()+"\n"))
    .finally(()=>{
      if(window.innerWidth < 769 && document.getElementById("main").classList.contains("view-editor")){
        setView('console');
      }
    });
}

function setView(mode){
  const main = document.getElementById("main");
  main.className = "view-" + mode;
  document.querySelectorAll(".view-controls .view-btn").forEach(b=>b.classList.remove("active"));
  const activeBtn = document.getElementById("btn-"+mode);
  if(activeBtn) activeBtn.classList.add("active");
  try{ localStorage.setItem("sigpy_view", mode); }catch(e){}
}

// bright green line numbers matching console #0f0
function updateLineNumbers(){
  const ta = document.getElementById('code');
  const ln = document.getElementById('line-numbers');
  const lines = ta.value.split('\n').length;
  let html = '';
  for(let i=1;i<=lines;i++){ html += i + '<br>'; }
  ln.innerHTML = html;
}

function syncScroll(){
  const ta = document.getElementById('code');
  const ln = document.getElementById('line-numbers');
  ln.scrollTop = ta.scrollTop;
}

async function loadExamples(){
  try{
    const res = await fetch('/api/examples');
    if(!res.ok) return;
    const files = await res.json();
    const sel = document.getElementById('examples-select');
    files.forEach(f=>{
      const opt = document.createElement('option');
      opt.value = f;
      opt.textContent = f.replace('.py','');
      sel.appendChild(opt);
    });
  }catch(e){
    console.log("Failed to load examples list", e);
  }
}

async function loadExampleFile(name){
  if(!name) return;
  try{
    const res = await fetch('/api/examples/' + encodeURIComponent(name));
    if(!res.ok) throw new Error('not found');
    const text = await res.text();
    const ta = document.getElementById('code');
    ta.value = text;
    updateLineNumbers();
    if(window.innerWidth < 769){
      setView('editor');
    } else if(document.getElementById('main').classList.contains('view-console')){
      setView('split');
    }
    clearOutput();
    outf("Loaded example: " + name + "\n▶ Hit Run to execute\n\n");
  }catch(e){
    outf("Failed to load example: " + name + "\n");
  }
}

// init
(function(){
  const ta = document.getElementById('code');
  ta.addEventListener('input', updateLineNumbers);
  ta.addEventListener('scroll', syncScroll);
  ta.addEventListener('keydown', function(e){
    if(e.key === 'Tab'){
      e.preventDefault();
      const start = this.selectionStart;
      const end = this.selectionEnd;
      this.value = this.value.substring(0, start) + "    " + this.value.substring(end);
      this.selectionStart = this.selectionEnd = start + 4;
      updateLineNumbers();
    }
  });
  updateLineNumbers();

  loadExamples();
  document.getElementById('examples-select').addEventListener('change', (e)=>{
    loadExampleFile(e.target.value);
  });

  try{
    const saved = localStorage.getItem("sigpy_view");
    if(saved && ["editor","split","console"].includes(saved)){
      setView(saved);
    } else if(window.innerWidth < 769){
      setView('editor');
      const h=document.getElementById("hint-mobile");
      if(h){ h.style.display="inline"; setTimeout(()=>h.style.display="none",4000); }
    }
  }catch(e){}
})();
</script>
</body>
</html>
"""

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == "/favicon.ico":
            self.send_response(200)
            self.send_header("Content-type","image/x-icon")
            self.end_headers()
            self.wfile.write(FAVICON_ICO)
        elif path == "/favicon-32.png":
            self.send_response(200)
            self.send_header("Content-type","image/png")
            self.end_headers()
            self.wfile.write(FAVICON_32)
        elif path == "/favicon-180.png":
            self.send_response(200)
            self.send_header("Content-type","image/png")
            self.end_headers()
            self.wfile.write(FAVICON_180 if FAVICON_180 else FAVICON_32)
        elif path in ("/api/examples", "/api/examples/"):
            files = list_example_files()
            self.send_response(200)
            self.send_header("Content-type","application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin","*")
            self.end_headers()
            self.wfile.write(json.dumps(files).encode())
        elif path.startswith("/api/examples/"):
            raw = path[len("/api/examples/"):]
            fname = urllib.parse.unquote(raw)
            fname = os.path.basename(fname)
            if not fname.endswith(".py") or "/" in fname or "\\" in fname or fname.startswith(".") or ".." in fname:
                self.send_response(400)
                self.send_header("Content-type","text/plain")
                self.end_headers()
                self.wfile.write(b"Invalid filename")
                return
            fpath = os.path.join(EXAMPLES_DIR, fname)
            if not os.path.isfile(fpath):
                self.send_response(404)
                self.send_header("Content-type","text/plain")
                self.end_headers()
                self.wfile.write(b"Not found")
                return
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-type","text/plain; charset=utf-8")
                self.end_headers()
                self.wfile.write(content.encode())
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(str(e).encode())
        elif path in ("/", "/index.html"):
            self.send_response(200)
            self.send_header("Content-type","text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML.encode())
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        print("%s %s" % (self.client_address[0], format%args))

if __name__ == "__main__":
    os.makedirs(EXAMPLES_DIR, exist_ok=True)
    print(f"Serving σπ on 0.0.0.0:{PORT}")
    print(f"Examples dir: {EXAMPLES_DIR} -> {list_example_files()}")
    HTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
