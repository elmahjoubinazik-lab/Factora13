#!/usr/bin/env python3
"""Factora — prépare les clips Runway d'un épisode (mode Runway, 2026-11-11).
Usage : python3 engine/clips.py episodes/NNN-x
Lit meta_en.json → "clips" : liste de {"name": scène, "file": "xxx.mp4" (dans build/rw/), "from": s, "to": s, "dur": s (facultatif)}.
Sans "dur", le passage [from, to] du clip est étiré/compressé sur la durée de la scène du même nom (build/timeline.json,
comme render.py : la 1re scène du Short commence à 0). Sortie : build/clips/<name>/0001.jpg… en 1440×2560 à 30 i/s,
et build/clips/outro_bg.jpg (1re image du 1er clip, floutée : fond de la conclusion qui boucle sur le début)."""
import sys, os, json, subprocess, shutil
EP = sys.argv[1].rstrip("/")
B = os.path.join(EP, "build")
meta = json.load(open(os.path.join(EP, "meta_en.json"), encoding="utf-8"))
tl = json.load(open(os.path.join(B, "timeline.json")))
first = tl[0]["scene"]
dur = {s["scene"]: s["end"] - (0.0 if s["scene"] == first else s["start"]) for s in tl}
for c in meta["clips"]:
    name, src = c["name"], os.path.join(B, "rw", c["file"])
    a, b = float(c.get("from", 0.0)), float(c["to"]); d = float(c.get("dur", dur[name]))
    out = os.path.join(B, "clips", name); shutil.rmtree(out, ignore_errors=True); os.makedirs(out)
    vf = f"setpts=PTS*{d / (b - a):.5f},framerate=fps=30,scale=1440:2560:flags=lanczos"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(a), "-t", str(b - a), "-i", src, "-vf", vf, "-q:v", "2", f"{out}/%04d.jpg"], check=True)
    print(f"{name}: {len(os.listdir(out))} images, {d:.2f} s (vitesse ×{(b - a) / d:.2f})")
c0 = meta["clips"][0]
subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(c0.get("from", 0.0)), "-i", os.path.join(B, "rw", c0["file"]), "-frames:v", "1",
                "-vf", "scale=1440:2560:flags=lanczos,gblur=sigma=28", "-q:v", "2", os.path.join(B, "clips", "outro_bg.jpg")], check=True)
print("OK clips →", os.path.join(B, "clips"))
