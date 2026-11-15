#!/usr/bin/env python3
"""Série d'images pour l'AutoCut de TikTok (demande de Nazik, 2026-11-15) : « 5 RIDDLES — PAUSE ON EACH ONE ».
7 images 1080×1920 : accroche, 5 énigmes (question + dessin néon + 3 réponses numérotées), réponses.
Zones sûres TikTok : rien d'essentiel au-dessus de 11 % ni sous 78 % de la hauteur, ni dans la colonne des boutons à droite.
Énigmes différentes de la liste « Énigmes du jour » de topics.md. Usage : python3 social/autocut_riddles.py"""
import os, sys, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
sys.argv = ["render.py", "short", "episodes/033-seven-riddles-teaser"]
src = open("engine/render.py", encoding="utf-8").read(); src = src[:src.index("# ---------- scènes de l'épisode")]
__file__ = os.path.join(ROOT, "engine/render.py"); exec(src)
OUT = "social/autocut-01"; DARK = (0.03, 0.02, 0.08)
XC = W * 0.47            # centre un peu à gauche : la colonne de boutons TikTok est à droite

def fit(ctx, s, x, y, size, maxw, col, a=1.0):
    font(ctx, size); w_ = ctx.text_extents(s).width
    text(ctx, s, x, y, size * min(1.0, maxw / w_), col, a)

def nfit(ctx, s, x, y, size, maxw, col, col2, fill=0.3):
    font(ctx, size); w_ = ctx.text_extents(s).width
    neon_text(ctx, s, x, y, size * min(1.0, maxw / w_), col, 1.0, col2, fill=fill)

def pill(ctx, s, x, y, col, size=46, pad=60):
    font(ctx, size * U); w_ = ctx.text_extents(s).width + pad * U
    rrect(ctx, x - w_ / 2, y - size * 0.8 * U, w_, size * 1.6 * U, size * 0.8 * U); rgba(ctx, col, 0.96); ctx.fill()
    text(ctx, s, x, y, size * U, DARK)

def options_col(ctx, opts, y0, good=None):
    pw, ph, gap = 700 * U, 96 * U, 26 * U
    for j, s_ in enumerate(opts):
        y = y0 + j * (ph + gap); col = [CYAN, CORAL, PURPLE][j]
        if good == j: col = GREEN; glow(ctx, XC, y, pw * 0.7, GREEN, 0.4)
        rrect(ctx, XC - pw / 2, y - ph / 2, pw, ph, ph / 2); rgba(ctx, (0.04, 0.03, 0.10), 0.9); ctx.fill()
        rrect(ctx, XC - pw / 2, y - ph / 2, pw, ph, ph / 2); ctx.set_line_width(6 * U); rgba(ctx, col); ctx.stroke()
        circle(ctx, XC - pw / 2 + ph / 2, y, ph * 0.38, col)
        text(ctx, str(j + 1), XC - pw / 2 + ph / 2, y, 52 * U, DARK)
        fit(ctx, s_, XC + ph * 0.45, y, 52 * U, pw - ph * 1.6, WHITE)

def frame(i, tint, title_lines, draw, opts):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
    neon_bg(c, 0.6 + i, tint=tint)
    pill(c, f"RIDDLE {i}/5", XC, H * 0.135, tint, 50)
    for k, (line, col, sz) in enumerate(title_lines):
        nfit(c, line, XC, H * (0.195 + 0.052 * k), sz * U, W * 0.80, col, PURPLE if col != PURPLE else PINK, fill=0.3)
    draw(c)
    options_col(c, opts, H * 0.555)
    text(c, "PAUSE & COMMENT YOUR ANSWER", XC, H * 0.755, 44 * U, GOLD)
    return s

def save(surf, name):
    raw = f"{OUT}/{name}_raw.png"; surf.write_to_png(raw)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", raw, "-vf",
                    "eq=saturation=1.35:contrast=1.06,unsharp=5:5:0.4,scale=1080:1920:flags=lanczos", "-q:v", "2",
                    f"{OUT}/{name}.jpg"], check=True); os.remove(raw)

# ---------- dessins
def gear(c, x, y, r, col, rot=0.0):
    def p(cc):
        n = 10
        for k in range(2 * n + 1):
            a_ = rot + k * math.pi / n; rr = r if k % 2 == 0 else r * 0.80
            (cc.move_to if k == 0 else cc.line_to)(x + rr * math.cos(a_), y + rr * math.sin(a_))
        cc.close_path()
    glow(c, x, y, r * 1.5, col, 0.25)
    c.new_path(); p(c); rgba(c, mix(col, NAVY, 0.55)); c.fill()
    neon_path(c, p, col, 5 * U)
    neon_path(c, lambda cc: cc.arc(x, y, r * 0.32, 0, 2 * math.pi), col, 5 * U)

def box(c, x, y, s, col):
    rrect(c, x - s / 2, y - s / 2, s, s, s * 0.15); rgba(c, mix(col, NAVY, 0.5)); c.fill()
    neon_path(c, lambda cc: (rrect(cc, x - s / 2, y - s / 2, s, s, s * 0.15)), col, 4 * U)

def d1(c):
    cols = [CYAN, PINK, GOLD, GREEN, PURPLE]
    for k in range(5):
        x = XC + (k - 2) * 190 * U
        gear(c, x, H * 0.375, 78 * U, cols[k], rot=k * 0.4)
        box(c, x, H * 0.445, 70 * U, cols[k])

def d2(c):
    vals = ["2", "6", "12", "20", "30", "?"]
    for k, v in enumerate(vals):
        row, col_ = divmod(k, 3)
        x = XC + (col_ - 1) * 250 * U; y = H * (0.340 + 0.110 * row)
        col = GOLD if v == "?" else [CYAN, PINK, GREEN, PURPLE, CORAL][k]
        glow(c, x, y, 130 * U, col, 0.3)
        circle(c, x, y, 92 * U, mix(col, NAVY, 0.6))
        neon_path(c, lambda cc, x=x, y=y: cc.arc(x, y, 92 * U, 0, 2 * math.pi), col, 6 * U)
        neon_text(c, v, x, y, 92 * U, WHITE, 1.0, col, fill=0.35)

def d3(c):
    x, y, r = XC, H * 0.395, 215 * U
    glow(c, x, y, r * 1.6, CYAN, 0.30)
    circle(c, x, y, r, (0.05, 0.06, 0.16))
    neon_path(c, lambda cc: cc.arc(x, y, r, 0, 2 * math.pi), CYAN, 8 * U)
    for k in range(12):
        a_ = k * math.pi / 6; r0 = r * (0.80 if k % 3 == 0 else 0.87)
        c.new_path(); c.move_to(x + r0 * math.sin(a_), y - r0 * math.cos(a_)); c.line_to(x + r * 0.94 * math.sin(a_), y - r * 0.94 * math.cos(a_))
        c.set_line_width((7 if k % 3 == 0 else 4) * U); rgba(c, WHITE, 0.9); c.stroke()
    for n, k in ((12, 0), (3, 3), (6, 6), (9, 9)):
        a_ = k * math.pi / 6; text(c, str(n), x + r * 0.64 * math.sin(a_), y - r * 0.64 * math.cos(a_), 46 * U, WHITE, 0.9)
    def hand(ang, ln, wd, col):
        a_ = math.radians(ang)
        c.new_path(); c.move_to(x, y); c.line_to(x + ln * math.sin(a_), y - ln * math.cos(a_))
        c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_line_width(wd); rgba(c, col); c.stroke()
    hand(97.5, r * 0.55, 18 * U, GOLD)    # aiguille des heures à 3 h 15 (90° + 7,5°)
    hand(90.0, r * 0.82, 10 * U, PINK)    # aiguille des minutes sur le 3
    circle(c, x, y, 16 * U, WHITE)

def d4(c):
    x, y = XC - 150 * U, H * 0.40
    def tag(cc):
        cc.move_to(x - 210 * U, y - 115 * U); cc.line_to(x + 130 * U, y - 115 * U); cc.line_to(x + 230 * U, y)
        cc.line_to(x + 130 * U, y + 115 * U); cc.line_to(x - 210 * U, y + 115 * U); cc.close_path()
    glow(c, x, y, 330 * U, GOLD, 0.25)
    c.new_path(); tag(c); rgba(c, mix(GOLD, NAVY, 0.55)); c.fill(); neon_path(c, tag, GOLD, 7 * U)
    neon_path(c, lambda cc: cc.arc(x + 168 * U, y, 16 * U, 0, 2 * math.pi), WHITE, 4 * U)
    neon_text(c, "$100", x - 55 * U, y, 108 * U, WHITE, 1.0, GOLD, fill=0.4)
    pill(c, "+10%", XC + 260 * U, H * 0.36, GREEN, 60, 50)
    pill(c, "-10%", XC + 260 * U, H * 0.44, CORAL, 60, 50)

def d5(c):
    sun(c, XC - 250 * U, H * 0.372, 115 * U, 0.7)
    earth(c, XC + 280 * U, H * 0.372, 80 * U)
    for k in range(7):   # rayon de lumière en pointillés
        xa = XC - 70 * U + k * 42 * U
        c.new_path(); c.move_to(xa, H * 0.372); c.line_to(xa + 22 * U, H * 0.372); c.set_line_width(8 * U); rgba(c, GOLD, 0.9); c.stroke()
    pill(c, "93 MILLION MILES AWAY", XC, H * 0.494, CYAN, 42)

RIDDLES = [
    (CYAN, [("5 MACHINES · 5 WIDGETS · 5 MIN", GOLD, 70), ("100 MACHINES · 100 WIDGETS", CYAN, 70), ("HOW LONG?", WHITE, 96)], d1,
     ["100 MINUTES", "5 MINUTES", "20 MINUTES"]),
    (PINK, [("WHAT COMES NEXT?", WHITE, 104)], d2, ["42", "40", "36"]),
    (CYAN, [("IT'S 3:15.", GOLD, 104), ("ANGLE BETWEEN THE HANDS?", WHITE, 76)], d3, ["0°", "15°", "7.5°"]),
    (GOLD, [("$100 SHIRT: +10%, THEN -10%", WHITE, 74), ("NEW PRICE?", GOLD, 104)], d4, ["$100", "$99", "$101"]),
    (CORAL, [("HOW LONG DOES SUNLIGHT", WHITE, 80), ("TAKE TO REACH EARTH?", GOLD, 80)], d5, ["8 SECONDS", "8 MINUTES", "8 HOURS"]),
]

# ---------- 1. accroche
s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
neon_bg(c, 0.3, tint=PURPLE)
neon_text(c, "5", XC, H * 0.215, 400 * U, GOLD, 1.0, CORAL, fill=0.4)
neon_text(c, "RIDDLES", XC, H * 0.355, 200 * U, WHITE, 1.0, PURPLE, fill=0.3)
pill(c, "PAUSE ON EACH ONE", XC, H * 0.44, CYAN, 60)
nfit(c, "CAN YOU GET 5/5?", XC, H * 0.525, 110 * U, W * 0.78, GOLD, CORAL, fill=0.35)
mascot(c, XC, H * 0.655, 330 * U, 1.0, 0.3)
save(s, "1_hook")

# ---------- 2 à 6. les énigmes
for i, (tint, lines, draw, opts) in enumerate(RIDDLES, 1):
    save(frame(i, tint, lines, draw, opts), f"{i + 1}_riddle{i}")

# ---------- 7. réponses
s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
neon_bg(c, 9.0, tint=GREEN)
neon_text(c, "ANSWERS", XC, H * 0.145, 150 * U, GREEN, 1.0, CYAN, fill=0.35)
ANS = [("5 MINUTES", "each machine makes 1 widget in 5 min"), ("42", "the gaps grow by 2: +4 +6 +8 +10 +12"),
       ("7.5°", "the hour hand moves too: 1/4 of 30°"), ("$99", "10% of $110 is $11, not $10"),
       ("8 MINUTES", "about 8 min 20 s (NASA)")]
for k, (a_, why) in enumerate(ANS):
    y = H * (0.235 + 0.092 * k); col = [CYAN, PINK, GOLD, GREEN, CORAL][k]
    circle(c, XC - 360 * U, y, 46 * U, col); text(c, str(k + 1), XC - 360 * U, y, 52 * U, DARK)
    font(c, 70 * U); text(c, a_, XC - 290 * U, y - 18 * U, 70 * U, WHITE, align="l")
    text(c, why.upper(), XC - 290 * U, y + 40 * U, 32 * U, (0.80, 0.80, 0.92), 0.95, align="l")
pill(c, "COMMENT YOUR SCORE /5", XC, H * 0.71, GOLD, 60)
text(c, "MORE RIDDLES ON YOUTUBE: FACTORA", XC, H * 0.765, 40 * U, WHITE, 0.92)
save(s, "7_answers")
print("OK", OUT)

# ---------- couverture (demande de Nazik, 2026-11-15) : un grand « 5/5 » au centre, les 5 énigmes en icônes autour,
# sans aucune réponse ; titre et éléments entre 14 % et 86 % de la hauteur (recadrage 3:4 de la grille du profil TikTok)
def mini_clock(c, x, y, r, col):
    glow(c, x, y, r * 1.6, col, 0.3); circle(c, x, y, r, (0.05, 0.06, 0.16))
    neon_path(c, lambda cc: cc.arc(x, y, r, 0, 2 * math.pi), col, 6 * U)
    for k in range(4):
        a_ = k * math.pi / 2; c.new_path(); c.move_to(x + r * 0.72 * math.sin(a_), y - r * 0.72 * math.cos(a_))
        c.line_to(x + r * 0.9 * math.sin(a_), y - r * 0.9 * math.cos(a_)); c.set_line_width(6 * U); rgba(c, WHITE, 0.9); c.stroke()
    for ang, ln, wd, cl in ((97.5, 0.55, 12, GOLD), (90.0, 0.82, 7, PINK)):
        a_ = math.radians(ang); c.new_path(); c.move_to(x, y); c.line_to(x + r * ln * math.sin(a_), y - r * ln * math.cos(a_))
        c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_line_width(wd * U); rgba(c, cl); c.stroke()
    circle(c, x, y, 9 * U, WHITE)

def mini_tag(c, x, y, s, col):
    def p(cc):
        cc.move_to(x - s, y - s * 0.55); cc.line_to(x + s * 0.55, y - s * 0.55); cc.line_to(x + s, y)
        cc.line_to(x + s * 0.55, y + s * 0.55); cc.line_to(x - s, y + s * 0.55); cc.close_path()
    glow(c, x, y, s * 1.6, col, 0.3); c.new_path(); p(c); rgba(c, mix(col, NAVY, 0.55)); c.fill(); neon_path(c, p, col, 5 * U)
    text(c, "$", x - s * 0.2, y, s * 0.9, WHITE)

def qcircle(c, x, y, r, col, s_="?"):
    glow(c, x, y, r * 1.5, col, 0.3); circle(c, x, y, r, mix(col, NAVY, 0.6))
    neon_path(c, lambda cc: cc.arc(x, y, r, 0, 2 * math.pi), col, 5 * U)
    neon_text(c, s_, x, y, r * 1.05, WHITE, 1.0, col, fill=0.35)

s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
neon_bg(c, 2.0, tint=PURPLE)
glow(c, CX, H * 0.45, 900 * U, GOLD, 0.10)
nfit(c, "CAN YOU", CX, H * 0.175, 150 * U, W * 0.86, WHITE, PURPLE, fill=0.3)
nfit(c, "SOLVE ALL 5?", CX, H * 0.25, 170 * U, W * 0.88, GOLD, CORAL, fill=0.35)
cx_, cy_, R = CX, H * 0.455, 255 * U
glow(c, cx_, cy_, R * 1.7, CYAN, 0.35)
circle(c, cx_, cy_, R, (0.05, 0.04, 0.14))
neon_path(c, lambda cc: cc.arc(cx_, cy_, R, 0, 2 * math.pi), CYAN, 12 * U)
neon_text(c, "5/5", cx_, cy_ - 10 * U, 230 * U, WHITE, 1.0, CYAN, fill=0.4)
text(c, "OR LESS?", cx_, cy_ + 135 * U, 46 * U, GOLD)
D = 400 * U   # les 5 énigmes en icônes autour du cercle (sans réponse)
for k, ang in enumerate((-150, -30, 15, 165, 90)):
    x = cx_ + D * math.cos(math.radians(ang)); y = cy_ + D * math.sin(math.radians(ang)) * (0.80 if ang == 90 else 0.92)
    if k == 0: gear(c, x, y, 82 * U, PINK, 0.3)
    elif k == 1: mini_clock(c, x, y, 82 * U, CYAN)
    elif k == 2: mini_tag(c, x, y, 85 * U, GOLD)
    elif k == 3: qcircle(c, x, y, 78 * U, GREEN)
    else: sun(c, x, y, 62 * U, 0.4)
pill(c, "PAUSE ON EACH ONE", CX, H * 0.722, CYAN, 66)
mascot(c, CX - 300 * U, H * 0.80, 180 * U, 1.0, 0.2)
neon_text(c, "FACTORA", CX + 110 * U, H * 0.80, 90 * U, GOLD, 1.0, CORAL, fill=0.3)
save(s, "0_cover")
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", f"{OUT}/0_cover.jpg", "-vf", "crop=1080:1440:0:240,scale=270:360",
                f"{OUT}/0_cover_grille.png"], check=True)   # aperçu de la vignette de la grille du profil (3:4)
print("OK couverture")
