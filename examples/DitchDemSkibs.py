# ditchDemSkibs.py
# SIGMA SCHOLARS - DITCH DEM SKIBs! (habits, not people)
# Skulpt-safe - no keyword args, no random.sample with kwargs

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

def pick_two_random(arr):
    # Skulpt-safe pick without random.sample
    a = random.choice(arr)
    b = random.choice(arr)
    # ensure different if possible
    tries = 0
    while b == a and tries < 10 and len(arr) > 1:
        b = random.choice(arr)
        tries = tries + 1
    return [a, b]

def count_skibs(habits_today):
    c = 0
    for h in habits_today:
        if h in SKIBS:
            c = c + 1
    return c

print("================================================================")
print("  DITCH DEM SKIBs! AUDIT")
print("================================================================")
print("")

# simulate today - no k= keyword
today = pick_two_random(SKIBS)
print("  Habits spotted today: " + str(today))
print("  SKIBs count: " + str(count_skibs(today)))
print("")

if count_skibs(today) > 0:
    print("  Action: REPLACE with SIG plan:")
    for step in SIG_PLAN:
        print("    " + step)
else:
    print("  Clean run! Aura +1000. SIGGIN RIGHT!")

print("")
print("----------------------------------------------------------------")
print("  MIDs are NOT an insult. Reclaim it:")
for p in MIDS_POWER:
    print("    - " + p)

print("")
print("  Chant: WHO LET THE SKIBs OUT?! DITCH! DITCH! DITCH!")
