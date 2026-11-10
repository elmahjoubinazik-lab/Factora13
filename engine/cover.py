#!/usr/bin/env python3
"""Affiche de couverture d'un Short (demande de Nazik, 2026-11-10 : couverture soignée qui attrape l'œil).
Usage : python3 engine/cover.py episodes/NNN-x
Le scenes.py de l'épisode doit définir cover(ctx) (dessin 1440×2560 avec les helpers du moteur).
Sorties : build/short_cover.jpg (1080×1920, finition couleurs) et build/short_cover_small.png (270×480, pour vérifier
la lisibilité à la taille d'une vignette dans le fil Shorts / TikTok)."""
import sys, os, subprocess
EP = sys.argv[1].rstrip("/")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.argv = ["render.py", "short", EP]
src = open("engine/render.py", encoding="utf-8").read()
src = src[:src.index("# ---------- scènes de l'épisode")]
__file__ = os.path.join(ROOT, "engine/render.py")
exec(src)
SFX_TIMES = []; TNOW = 0.0
exec(open(EP + "/scenes.py", encoding="utf-8").read())
if "cover" not in globals():
    sys.exit("scenes.py ne définit pas cover(ctx)")
surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); ctx = cairo.Context(surf)
cover(ctx)
raw = EP + "/build/short_cover_raw.png"; os.makedirs(EP + "/build", exist_ok=True); surf.write_to_png(raw)
import json as _json
_photo = os.path.exists(EP + "/meta_en.json") and _json.load(open(EP + "/meta_en.json", encoding="utf-8")).get("finish") == "photo"
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", raw, "-vf",
                ("eq=saturation=1.1:contrast=1.04" if _photo else "eq=saturation=1.4:contrast=1.08") + ",unsharp=5:5:0.4,scale=1080:1920:flags=lanczos", "-q:v", "2", EP + "/build/short_cover.jpg"], check=True)
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", EP + "/build/short_cover.jpg", "-vf", "scale=270:480", EP + "/build/short_cover_small.png"], check=True)
print("OK", EP + "/build/short_cover.jpg")
