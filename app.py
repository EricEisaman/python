import os
import json
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = int(os.environ.get("PORT", 10000))
EXAMPLES_DIR = "examples"

# read favicon files at startup
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

def ensure_examples():
    os.makedirs(EXAMPLES_DIR, exist_ok=True)
    defaults = {
        "isDuplicatedNumber.py": """# isDuplicatedNumber.py
# SIGMA SCHOLARS - Check if a number has duplicated digits
# e.g. 1123 -> True (1 repeats), 1234 -> False

def isDuplicatedNumber(n):
    \"\"\"Return True if any digit appears more than once.\"\"\"
    s = str(abs(int(n)))
    seen = set()
    for ch in s:
        if ch in seen:
            return True
        seen.add(ch)
    return False

def isDuplicatedNumberDetailed(n):
    s = str(abs(int(n)))
    counts = {}
    for ch in s:
        counts[ch] = counts.get(ch, 0) + 1
    dups = [d for d,c in counts.items() if c > 1]
    return (len(dups) > 0, dups)

test_numbers = [112, 1234, 1001, 9876543210, 122333, 101010, 2026]

print("="*48)
print("  isDuplicatedNumber - DITCH DEM SKIBs CHECK")
print("="*48)
for num in test_numbers:
    dup, digits = isDuplicatedNumberDetailed(num)
    status = "DUPLICATED ⚠️" if dup else "UNIQUE ✅"
    extra = f" -> repeats: {digits}" if dup else ""
    print(f"  {num:12} : {status}{extra}")

print("")
for n in [123, 1123, 5567]:
    print(f"  isDuplicatedNumber({n}) = {isDuplicatedNumber(n)}")
""",
        "gaussianGrowth.py": """# gaussianGrowth.py
# SIGMA SCHOLARS - The Gaussian is not a ranking, it's a road

import math
import random

def gaussian(x, mu=0, sigma=1):
    return (1/(sigma * math.sqrt(2*math.pi))) * math.exp(-0.5 * ((x-mu)/sigma)**2)

def growth_curve(start_pos=-2.0, reps=10, effort=0.3):
    pos = start_pos
    history = [pos]
    for _ in range(reps):
        pos += effort + random.uniform(-0.05, 0.15)
        history.append(pos)
    return history

print("="*64)
print("  THE GAUSSIAN ROAD - MID -> SIG -> SIGSTER -> BIG SIG")
print("="*64)
print("")
print("  mean is a BEGINNING, not a ceiling. fr fr.")
print("")

students = {
    "MID at mew line": {"start": -2.0, "effort": 0.2},
    "SIG grinding": {"start": -0.5, "effort": 0.3},
    "SIGSTER locked in": {"start": 1.0, "effort": 0.25},
}

for name, cfg in students.items():
    path = growth_curve(cfg["start"], reps=8, effort=cfg["effort"])
    print(f"- {name}:")
    print(f"  start {cfg['start']:.1f} -> end {path[-1]:.2f}  (delta +{path[-1]-path[0]:.2f})")
    print(f"  reps: {' -> '.join(f'{x:.1f}' for x in path)}")
    print("")

print("  Slogan: SIGS LOVE DEM MIDS! Growth > fixed rank")
""",
        "ditchDemSkibs.py": """# ditchDemSkibs.py
# SIGMA SCHOLARS - DITCH DEM SKIBs! (habits, not people)

import random

SKIBS = [
    "skipping work / putting it off indefinitely",
    "avoiding help from fear / pride / embarrassment",
    "giving up before attempting",
    "confusion = I'm not smart defeatism",
    "mocking effort to avoid vulnerability",
    "doomscrolling, drifting, no plan"
]

SIG_PLAN = [
    "1. Identify barriers without shame",
    "2. Simple repeatable study plan (25-min focus blocks)",
    "3. Break tasks into practice reps",
    "4. Normalize office hours / tutoring / revisions",
    "5. Celebrate small wins till confidence sustains",
    "6. Give new SIG a chance to help others"
]

print("="*64)
print("  DITCH DEM SKIBs! AUDIT")
print("="*64)
print("")
today = random.sample(SKIBS, k=2)
print(f"  Habits spotted today: {today}")
print(f"  SKIBs count: {len(today)}")
print("")
print("  Action: REPLACE with SIG plan:")
for step in SIG_PLAN:
    print(f"    {step}")
print("")
print("  Chant: WHO LET THE SKIBs OUT?! DITCH! DITCH! DITCH!")
"""
    }
    for name, content in defaults.items():
        p = os.path.join(EXAMPLES_DIR, name)
        if not os.path.exists(p):
            try:
                with open(p, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"Created example {p}")
            except Exception as e:
                print(f"Failed to create {p}: {e}")

HTML = r"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
<title>sigpy - σπ</title>
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
  textarea{flex:1;background:#1e1e1e;color:#d4d4d4;border:1px solid #333;padding:10px;font-size:14px;resize:none;line-height:1.5;border-radius:6px}
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

  /* view states */
  main.view-editor #right{display:none !important}
  main.view-editor #left{flex:1;width:100%}
  main.view-console #left{display:none !important}
  main.view-console #right{flex:1;width:100%}
  main.view-split #left, main.view-split #right{display:flex}

  .toolbar{display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;gap:8px;flex-wrap:wrap}
  .console-title{padding:8px;border-bottom:1px solid #333;background:#111;display:flex;justify-content:space-between;align-items:center}

  @media (max-width: 768px){
    header{padding:8px 10px}
    main{flex-direction:column}
    main.view-split #left{flex:1 1 58%;min-height:0}
    main.view-split #right{flex:1 1 42%;min-height:180px;border-left:none;border-top:1px solid #333}
    textarea{font-size:16px}
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
<textarea id="code">
# SIGMA SCHOLARS LORE TERMINAL v2026
# EDWARD LITTLE HIGH SCHOOL - WHO LET THE SKIBS OUT! EDITION
# People are never disposable. Bad habits are.

import random, math

def banner():
    print("="*64)
    print("  WHO LET THE SKIBS OUT! // SIGMA SCHOLARS // ELHS")
    print("  Maroon & White // Fisheye Album Cover Mode: ON")
    print("="*64)
    print("")
    print("  [BIG SIG]  +  [LIL SIGGY]  = ALLIANCE ACTIVATED")
    print("")

def gaussian():
    print("  THE GAUSSIAN IS NOT A RANKING. IT'S A ROAD:")
    print("")
    print("               .--._  glowing gold math  _.--.")
    print("            .-'      `'--.       .--'      '-.")
    print("         .-'   f(x)=1/σ√2π e^-½((x-μ)/σ)²  '-.")
    print("       .'                RIGHT-TAIL REPS        '.")
    print("     .'  MID ----------> SIG -> SIGSTER -> BIG SIG '.")
    print("  ---'------------------------------------------------'---")
    print("     ^                                                    ^")
    print("  mew line = starting point, baseline, real talk      far right = skills from practice, feedback, community")
    print("     mean is a beginning, not a ceiling. fr fr.")
    print("")

def big_sig():
    print("-"*64)
    print("  BIG SIG - Hype Captain / Co-Leader")
    print("-"*64)
    print("  Look: maroon varsity jacket Σ SIG, gold shades, backpack")
    print("        overflowing with A+ work, spare pencils, open seat")
    print("  Traits: charismatic, disciplined, funny, protective")
    print("  Core: strength = helping others gain confidence, not flexing")
    print("  Chant: 'Your starting point is real, but NOT your ceiling.'")
    print("  Flex: spare pencil, study guide, shared notes")
    print("")

def lil_siggy():
    print("-"*64)
    print("  LIL SIGGY - Commander / Mentor / Athlete-Scholar")
    print("-"*64)
    print("  Look: maroon & gold academic streetwear, elite but humble")
    print("  Arc: MID at mew line -> SIG -> SIGSTER -> BIG SIG")
    print("  Lore: saw a MID alone at lunch, teary, discouraged.")
    print("        Didn't judge. Sat down. Listened. Made a plan.")
    print("  Method:")
    steps = [
        "  1. Identify barriers without shame",
        "  2. Simple repeatable study plan",
        "  3. Break tasks into practice reps",
        "  4. Normalize office hours / tutoring / revisions",
        "  5. Celebrate small wins till confidence sustains",
        "  6. Give new SIG a chance to help others"
    ]
    for s in steps: print(s)
    print("")

def mids_and_skibs():
    print("-"*64)
    print("  MIDs vs SKIBs - IMPORTANT DISTINCTION")
    print("-"*64)
    print("  MIDs = students in middle, average, stuck, overlooked")
    print("       NOT an insult. It's 'in motion'. Reclaimable.")
    print("       uneven grades, missed work, weak routines = valid")
    print("       -> most important learner: chooses to improve")
    print("")
    print("  SKIBs = NOT PEOPLE. They are HABITS to ditch:")
    habits = [
        "  - skipping work / putting it off indefinitely",
        "  - avoiding help from fear / pride / embarrassment",
        "  - giving up before attempting",
        "  - 'confusion = I'm not smart' defeatism",
        "  - mocking effort to avoid vulnerability",
        "  - doomscrolling, drifting, no plan"
    ]
    for h in habits: print(h)
    print("")
    print("  -> DITCH DEM SKIBs! = ditch self-sabotage, not classmates")
    print("")

def alliance():
    print("-"*64)
    print("  SIGMA SCHOLAR ALLIANCE - Activities")
    print("-"*64)
    acts = [
        "  Sigma Sessions: focus blocks, whiteboards, peer tutoring",
        "  Mew-to-Mastery Onboarding: compassionate intake, no judgment",
        "  Right-Tail Reps: prep -> feedback -> revision -> reflection",
        "  Notebook Uplift: templates, planners, calculator tips",
        "  Scholar Spotlights: persistence, helpfulness, not just As",
        "  Community Knowledge Runs: tutor younger kids, bless block"
    ]
    for a in acts: print(a)
    print("")

def slogans():
    print("-"*64)
    print("  SIGNATURE SLOGANS - SAY IT LOUD")
    print("-"*64)
    chants = [
        "  SIGS LOVE DEM MIDS! = we see you trying, we celebrate growth",
        "  OOOH YEH... THEY DITCHED DEM BIBS! = leave passivity, own next step",
        "  Ditch dem SKIBs! = reject habits, not people",
        "  SIGGIN RIGHT! = move right via intentional practice",
        "  Go Sig or Go Home! = arrive ready to engage or reset & return",
        "  Build your mind. Bless your block. = skills have social value"
    ]
    for c in chants: print(c)
    print("")

def chant_final():
    print("="*64)
    print("  FINAL CHANT - ALLIANCE CHOIR")
    print("="*64)
    for i in range(2):
        print("  WHO LET THE SKIBS OUT?!  SKIB-SKIB-SKIB-SKIB!")
    print("  WHO LET THE SKIBS OUT?!  DITCH! DITCH! DITCH! DITCH!")
    print("")
    print("  Code: Show up prepared. Replace excuses with a plan.")
    print("        Ask without embarrassment. Share knowledge. Bless school.")
    print("")
    print(random.choice([
        "  Result: You are now 73% more SIGGIN. Aura +1000.",
        "  Result: Right-tail shift detected. Let's gooo.",
        "  Result: Notebook drippin, grades grippin. SIGGIN!",
        "  Result: Belonging unlocked. Welcome to Alliance."
    ]))
    print("="*64)

# RUN IT
banner()
gaussian()
big_sig()
lil_siggy()
mids_and_skibs()
alliance()
slogans()
chant_final()
</textarea>
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
    document.getElementById('code').value = text;
    // Switch to editor on mobile or if console was full-width
    if(window.innerWidth < 769){
      setView('editor');
    } else if(document.getElementById('main').classList.contains('view-console')){
      setView('split');
    }
    clearOutput();
    outf("Loaded example: " + name + "\\n▶ Hit Run to execute\\n\\n");
  }catch(e){
    outf("Failed to load example: " + name + "\\n");
  }
}

// init
(function(){
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
      document.getElementById("hint-mobile").style.display = "inline";
      setTimeout(()=>{ const h=document.getElementById("hint-mobile"); if(h) h.style.display="none"; },4000);
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
    ensure_examples()
    print(f"Serving σπ on 0.0.0.0:{PORT}")
    print(f"Examples dir: {EXAMPLES_DIR} -> {list_example_files()}")
    HTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
