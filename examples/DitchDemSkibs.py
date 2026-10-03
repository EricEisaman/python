# ditchDemSkibs.py
# SIGMA SCHOLARS - DITCH DEM SKIBs! (habits, not people)
# SKIBs = self-sabotaging habits to ditch

import random

SKIBS = [
    "skipping work / putting it off indefinitely",
    "avoiding help from fear / pride / embarrassment",
    "giving up before attempting",
    "confusion = I'm not smart defeatism",
    "mocking effort to avoid vulnerability",
    "doomscrolling, drifting, no plan"
]

MIDS_POWER = [
    "uneven grades but still showing up",
    "missed work but asking for plan",
    "weak routines but willing to rep",
    "in motion - reclaimable",
    "most important learner: chooses to improve"
]

SIG_PLAN = [
    "1. Identify barriers without shame",
    "2. Simple repeatable study plan (25-min focus blocks)",
    "3. Break tasks into practice reps",
    "4. Normalize office hours / tutoring / revisions",
    "5. Celebrate small wins till confidence sustains",
    "6. Give new SIG a chance to help others"
]

def alliance_check(habits_today):
    skib_count = sum(1 for h in habits_today if h in SKIBS)
    return skib_count

print("="*64)
print("  DITCH DEM SKIBs! AUDIT")
print("="*64)
print("")

# simulate today
today = random.sample(SKIBS, k=2)
print(f"  Habits spotted today: {today}")
print(f"  SKIBs count: {alliance_check(today)}")
print("")

if alliance_check(today) > 0:
    print("  Action: REPLACE with SIG plan:")
    for step in SIG_PLAN:
        print(f"    {step}")
else:
    print("  Clean run! Aura +1000. SIGGIN RIGHT!")

print("")
print("-"*64)
print("  MIDs are NOT an insult. Reclaim it:")
for p in MIDS_POWER:
    print(f"    • {p}")

print("")
print("  Chant: WHO LET THE SKIBs OUT?! DITCH! DITCH! DITCH!")
