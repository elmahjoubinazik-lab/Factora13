#!/usr/bin/env python3
"""Images de la page Facebook Factora (demande de Nazik, 2026-11-14) : photo de profil 1080×1080 et photo de couverture
1640×856, dans le style néon de la chaîne. Usage : python3 brand/facebook.py → brand/facebook/*.jpg
Zone sûre de la couverture : Facebook la recadre en 2,63:1 sur ordinateur (bandes haut/bas coupées) et en 16:9 sur
téléphone (côtés coupés) ; la photo de profil chevauche le bas à gauche → tout l'essentiel au centre."""
import os, sys, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
sys.argv = ["render.py", "short", "episodes/033-seven-riddles-teaser"]
src = open("engine/render.py", encoding="utf-8").read(); src = src[:src.index("# ---------- scènes de l'épisode")]
__file__ = os.path.join(ROOT, "engine/render.py"); exec(src)
OUT = "brand/facebook"

def size(w, h):
    global W, H, U, CX, CY
    W, H = w, h; U = min(W, H) / 1080.0; CX, CY = W / 2, H / 2

def save(surf, name):
    raw = f"{OUT}/{name}_raw.png"; surf.write_to_png(raw)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", raw, "-vf", "eq=saturation=1.35:contrast=1.06,unsharp=5:5:0.4",
                    "-q:v", "2", f"{OUT}/{name}.jpg"], check=True); os.remove(raw)

def qmark(ctx, x, y, s, col, a=1.0):
    neon_text(ctx, "?", x, y, s, col, a, WHITE, fill=0.25)

def ring(ctx, x, y, r, n, col):
    glow(ctx, x, y, r * 1.6, col, 0.30)
    circle(ctx, x, y, r, mix(col, NAVY, 0.6), 1.0)
    neon_path(ctx, lambda c: c.arc(x, y, r, 0, 2 * math.pi), col, 5 * U)
    neon_text(ctx, str(n), x, y, r * 1.1, WHITE, 1.0, col, fill=0.3)

# ---- photo de profil (affichée en cercle) : la chouette seule, grande, centrée
size(1080, 1080)
s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
neon_bg(c, 0.8, tint=PURPLE)
glow(c, CX, CY, 520 * U, CYAN, 0.18)
mascot(c, CX, CY + 10 * U, 820 * U, 1.0, 0.4)
save(s, "facebook_profil")

# ---- photo de couverture 1640×856
size(1640, 856)
s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
neon_bg(c, 1.2, tint=PURPLE)
glow(c, CX, H * 0.45, 700 * U, GOLD, 0.10)
# décor latéral (dans la zone sûre 16:9 : x entre 60 et 1580)
qmark(c, W * 0.115, H * 0.40, 260 * U, CYAN); qmark(c, W * 0.885, H * 0.40, 260 * U, PINK)
ring(c, W * 0.215, H * 0.66, 52 * U, 1, GREEN); ring(c, W * 0.785, H * 0.66, 52 * U, 3, CORAL)
ring(c, W * 0.175, H * 0.22, 40 * U, 2, GOLD); ring(c, W * 0.825, H * 0.22, 40 * U, 7, PURPLE)
# titre + signature + promesse
neon_text(c, "FACTORA", CX, H * 0.36, 230 * U, GOLD, 1.0, CORAL, fill=0.35)
text(c, "THINK FAST. LEARN SOMETHING AMAZING.", CX, H * 0.555, 50 * U, WHITE, 0.95)
label = "RIDDLES  ·  LOGIC TESTS  ·  SCIENCE QUIZZES"
font(c, 40 * U); w_ = c.text_extents(label).width + 80 * U
rrect(c, CX - w_ / 2, H * 0.665 - 36 * U, w_, 72 * U, 36 * U); rgba(c, CYAN, 0.95); c.fill()
text(c, label, CX, H * 0.665, 40 * U, (0.03, 0.02, 0.08), 1.0)
text(c, "FULL VIDEOS ON YOUTUBE: FACTORA", CX, H * 0.765, 30 * U, (0.85, 0.85, 0.95), 0.9)
save(s, "facebook_couverture")
print("OK", OUT)
