#!/bin/bash
# Episode 024 (version IA, 2026-11-10) : découpe les clips Runway (build/rw/*.mp4, 720x1280, 24 i/s) en images 1440x2560 à 30 i/s,
# recalées sur la durée de chaque scène (build/timeline.json). Usage : bash episodes/024-hand-dryer/prep_clips.sh
set -e
cd "$(dirname "$0")/build"
python3 - <<'PY'
import json, subprocess, os, shutil
tl = {s["scene"]: s for s in json.load(open("timeline.json"))}
d = {k: tl[k]["end"] - (0.0 if k == "hook" else tl[k]["start"]) for k in tl}
V1 = 1.7   # verdict : « The CDC says both work. » sur l'image fixe, puis le clip serviette
uses = [("hook", "hook", 0.0, 3.05, d["hook"]), ("vs", "vs", 0.0, 1.9, d["vs"]), ("dryer", "dryer", 0.0, 5.04, d["dryer"]),
        ("jet", "jet", 0.0, 4.74, 4.4), ("verdict", "verdict", 0.0, 4.9, d["verdict"] - V1)]
for name, clip, a, src, dur in uses:
    out = f"clips/{name}"; shutil.rmtree(out, ignore_errors=True); os.makedirs(out)
    vf = f"setpts=PTS*{dur / src:.5f},framerate=fps=30,scale=1440:2560:flags=lanczos"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(a), "-t", str(src), "-i", f"rw/{clip}.mp4", "-vf", vf, "-q:v", "2", f"{out}/%04d.jpg"], check=True)
    print(name, len(os.listdir(out)), "images", f"{dur:.2f}s")
# fond de la conclusion : 1re image de l'accroche, floutée (la fin renvoie au début → boucle)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "rw/hook.mp4", "-frames:v", "1", "-vf", "scale=1440:2560:flags=lanczos,gblur=sigma=28", "-q:v", "2", "clips/outro_bg.jpg"], check=True)
PY
