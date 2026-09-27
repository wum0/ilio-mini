#!/usr/bin/env python3
"""Kimi SessionHeartbeat hook. Heartbeat is observe-only, so the note is left for the Stop hook to inject."""
import json, os, sys, time
W = "/work"
try: json.load(sys.stdin)
except Exception: pass
if os.path.exists(f"{W}/FLAG") or not os.path.exists(f"{W}/.start"): sys.exit(0)
m = int((time.time() - float(open(f"{W}/.start").read())) / 60)
for t in (30, 10):
    if m >= t and not os.path.exists(f"{W}/.nudge{t}"):
        for u in (10, 30):
            if u <= t: open(f"{W}/.nudge{u}", "w").close()
        open(f"{W}/.nudge-msg", "w").write(
            f"HARNESS: {m} min and no correct flag yet. Split now with $explore-alternatives: update /work/notes.md, "
            "then spawn 2-3 subagents on genuinely different directions (each with one bounded question and its own "
            "/work/lanes/<name>/), keep your own lane moving, and merge their reports. Only you submit.\n")
        break
