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
  main{display:flex;flex:1;overflow:hidden;transition:all 0.2s}
  #left{flex:1;display:flex;flex-direction:column;padding:8px;min-width:0;min-height:0}
  #right{flex:1;display:flex;flex-direction:column;border-left:1px solid #333;background:#000;min-width:0;min-height:0}
  textarea{flex:1;background:#1e1e1e;color:#d4d4d4;border:1px solid #333;padding:10px;font-size:14px;resize:none;line-height:1.5;border-radius:6px}
  #output{flex:1;overflow:auto;padding:10px;white-space:pre-wrap;background:#000;color:#0f0;font-size:13px;line-height:1.5}
  button{border:0;padding:8px 16px;cursor:pointer;border-radius:6px;font-weight:bold;font-family:monospace}
  #run-btn{background:#0a84ff;color:white}
  #run-btn:active{transform:scale(0.98)}
  
  /* view controls */
  .view-controls{display:flex;gap:6px;background:#1e1e1e;padding:4px;border-radius:8px;border:1px solid #333}
  .view-btn{background:#2a2a2a;color:#aaa;font-size:12px;padding:6px 12px}
  .view-btn.active{background:#0a84ff;color:white;box-shadow:0 0 0 1px #0a84ff}
  .view-btn:hover{color:#fff;background:#333}

  /* view states */
  main.view-editor #right{display:none !important}
  main.view-editor #left{flex:1;width:100%}
  main.view-console #left{display:none !important}
  main.view-console #right{flex:1;width:100%}
  main.view-split #left, main.view-split #right{display:flex}

  .toolbar{display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;gap:8px;flex-wrap:wrap}
  .console-title{padding:8px;border-bottom:1px solid #333;background:#111;display:flex;justify-content:space-between;align-items:center}

  /* mobile */
  @media (max-width: 768px){
    header{padding:8px 10px}
    main{flex-direction:column}
    main.view-split #left{flex:1 1 58%;min-height:0}
    main.view-split #right{flex:1 1 42%;min-height:180px;border-left:none;border-top:1px solid #333}
    textarea{font-size:16px} /* prevents iOS zoom */
    #output{font-size:13px}
    .view-btn{padding:8px 10px;font-size:13px}
  }
</style>
</head>
<body>
<header>
  <div><b>σπ</b> sigpy - Python 3 editor</div>
  <div class="view-controls" title="Switch layout - great for mobile">
    <button class="view-btn" id="btn-editor" onclick="setView('editor')">📝 Editor</button>
    <button class="view-btn active" id="btn-split" onclick="setView('split')">◫ Split</button>
    <button class="view-btn" id="btn-console" onclick="setView('console')">💻 Console</button>
  </div>
</header>
<main id="main" class="view-split">
  <div id="left">
    <div class="toolbar">
      <button id="run-btn" onclick="runCode()">▶ Run</button>
      <span style="font-size:11px;color:#666;display:none" id="hint-mobile">📱 tip: use ◫ buttons for full-width</span>
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
      // On mobile, auto-show console after run if in editor-only mode
      if(window.innerWidth < 769 && document.getElementById("main").classList.contains("view-editor")){
        setView('console');
      }
    });
}

function setView(mode){
  const main = document.getElementById("main");
  main.className = "view-" + mode;
  document.querySelectorAll(".view-btn").forEach(b=>b.classList.remove("active"));
  const activeBtn = document.getElementById("btn-"+mode);
  if(activeBtn) activeBtn.classList.add("active");
  try{ localStorage.setItem("sigpy_view", mode); }catch(e){}
}

// init
(function(){
  try{
    const saved = localStorage.getItem("sigpy_view");
    if(saved && ["editor","split","console"].includes(saved)){
      setView(saved);
    } else if(window.innerWidth < 769){
      // default mobile to editor for more typing space
      setView('editor');
      document.getElementById("hint-mobile").style.display = "inline";
    }
  }catch(e){}
  // show hint briefly on mobile
  if(window.innerWidth < 769){
    const h = document.getElementById("hint-mobile");
    if(h){ h.style.display="inline"; setTimeout(()=>h.style.display="none",4000); }
  }
})();
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