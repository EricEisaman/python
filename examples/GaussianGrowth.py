# gaussianGrowth.py
# SIGMA SCHOLARS - The Gaussian is not a ranking, it's a road
# Visualize moving right via intentional practice reps

import math
import random

def gaussian(x, mu=0, sigma=1):
    return (1/(sigma * math.sqrt(2*math.pi))) * math.exp(-0.5 * ((x-mu)/sigma)**2)

def growth_curve(start_pos=-2.0, reps=10, effort=0.3):
    """Simulate moving right on the gaussian with each rep"""
    pos = start_pos
    history = [pos]
    for _ in range(reps):
        # each rep = small right shift + randomness
        pos += effort + random.uniform(-0.05, 0.15)
        history.append(pos)
    return history

print("="*64)
print("  THE GAUSSIAN ROAD - MID -> SIG -> SIGSTER -> BIG SIG")
print("="*64)
print("")
print("  mean is a BEGINNING, not a ceiling. fr fr.")
print("")

# Simulate 3 students
students = {
    "MID at mew line": {"start": -2.0, "effort": 0.2},
    "SIG grinding": {"start": -0.5, "effort": 0.3},
    "SIGSTER locked in": {"start": 1.0, "effort": 0.25},
}

for name, cfg in students.items():
    path = growth_curve(cfg["start"], reps=8, effort=cfg["effort"])
    # ascii trail
    trail = ""
    for p in path:
        # map -3..3 to 0..30 chars
        col = int((p + 3) * 5)
        col = max(0, min(30, col))
        trail += " " * col + "●\n"
    
    print(f"- {name}:")
    print(f"  start {cfg['start']:.1f} -> end {path[-1]:.2f}  (delta +{path[-1]-path[0]:.2f})")
    print(f"  reps: {' -> '.join(f'{x:.1f}' for x in path)}")
    print("")

print("  Slogan: SIGS LOVE DEM MIDS! Growth > fixed rank")
