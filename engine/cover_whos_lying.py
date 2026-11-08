# Couverture « affiche » pour la série Who's Lying? (modèle : ép. 019). Copier, adapter EP/textes, lancer depuis la racine du dépôt.
import sys
EP = "episodes/019-whos-lying-1"
sys.argv = ["render.py", "short", EP]
src = open("engine/render.py", encoding="utf-8").read()
src = src[:src.index("# ---------- scènes de l'épisode")]
__file__ = "/home/user/factora13/engine/render.py"
exec(src)
SFX_TIMES = []; TNOW = 0.0
exec(open(EP + "/scenes.py", encoding="utf-8").read())
surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); ctx = cairo.Context(surf)
t = 0.5
vgrad(ctx, (0.14, 0.15, 0.38), (0.01, 0.01, 0.05))
rgba(ctx, (0.55, 0.62, 0.95), 0.12); ctx.paint()
rain(ctx, t, 0.9)
bolt(ctx, W * 0.80, 0, H * 0.40, 4, 1.0)
bolt(ctx, W * 0.12, 0, H * 0.22, 9, 0.6)
glow(ctx, W * 0.80, H * 0.10, 500 * U, (0.7, 0.8, 1.0), 0.35)
# mansion in the back
ctx.save(); ctx.translate(0, 0)
mansion(ctx, CX, H * 0.50, 0.9 * U, 1.0, 0.4)
ctx.restore()
rgba(ctx, (0.01, 0.01, 0.05), 0.55); ctx.rectangle(0, H * 0.30, W, H); ctx.fill()
# title
for dx, dy, col, a in ((10, 12, (0, 0, 0), 0.6), (0, 0, GOLD, 1.0)):
    text(ctx, "WHO'S", CX + dx * U, H * 0.105 + dy * U, 210 * U, col, a)
    text(ctx, "LYING?", CX + dx * U, H * 0.205 + dy * U, 230 * U, col if col != GOLD else CORAL, a)
rrect(ctx, CX - 560 * U, H * 0.275 - 52 * U, 1120 * U, 104 * U, 52 * U); rgba(ctx, (0, 0, 0), 0.7); ctx.fill()
text(ctx, "ONLY ONE ALIBI IS IMPOSSIBLE", CX, H * 0.275, 60 * U, WHITE)
# suspects
for i in range(4):
    x = W * (0.14 + 0.24 * i)
    glow(ctx, x, H * 0.52, 260 * U, COLS[i], 0.35)
    silhouette(ctx, x, H * 0.66, 1.0 * U, COLS[i], i, 1.0, t, 0.9)
    badge(ctx, x, H * 0.66 + 90 * U, i + 1, COLS[i], 1.0, 58)
rrect(ctx, CX - 470 * U, H * 0.80 - 60 * U, 940 * U, 120 * U, 60 * U); rgba(ctx, CORAL, 0.95); ctx.fill()
text(ctx, "COMMENT 1, 2, 3 OR 4", CX, H * 0.80, 70 * U, WHITE)
text(ctx, "CASE #1", CX, H * 0.885, 64 * U, (0.8, 0.85, 1.0), 0.9)
surf.write_to_png("/tmp/claude-0/-home-user-factora13/11aedbc4-b7eb-5983-aca3-e47f0ca34886/scratchpad/cover19_raw.png")
print("ok")
