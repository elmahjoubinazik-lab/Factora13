# Episode 020 (Short only, 15–20 s test) - "You pass 2nd place. What place are you?" — sober NEON style
# (Nazik 2026-11-09: cleaner, prettier look: dark plain background, one central element, neon glow, clean titles.)
# Executed inside engine/render.py (helpers available). Vertical layout. Original vector animation. All sizes in U.

RUN = {"1": CYAN, "2": PINK, "YOU": GOLD, "4": PURPLE}

def bg(ctx, t, tint=PURPLE):
    neon_bg(ctx, t, tint=tint)

def lanes(ctx, t, a=1.0):
    # two neon lane lines + moving dashes (speed), nothing else
    for lx, col in ((W * 0.22, CYAN), (W * 0.78, PINK)):
        neon_path(ctx, lambda c, lx=lx: (c.move_to(lx, H * 0.18), c.line_to(lx, H * 0.70)), col, 5 * U, 0.8 * a)
    ctx.set_dash([50 * U, 60 * U], -t * 700 * U)
    ctx.move_to(CX, H * 0.18); ctx.line_to(CX, H * 0.70); ctx.set_line_width(4 * U); rgba(ctx, WHITE, 0.18 * a); ctx.stroke()
    ctx.set_dash([])

def runner(ctx, x, y, label, col, t, a=1.0, big=1.0):
    if a <= 0: return
    r = 100 * U * big
    pulse = 1 + 0.04 * math.sin(t * 10 + len(label))
    glow(ctx, x, y, r * 2.4, col, 0.30 * a)
    neon_path(ctx, lambda c: c.arc(x, y, r * pulse, 0, 2 * math.pi), col, 6 * U * big, a)
    neon_text(ctx, label, x, y, (58 if len(label) > 1 else 84) * U * big, col, a, fill=0.25)
    # speed streaks behind
    for k in range(3):
        yy = y + r + (30 + 34 * k) * U
        ctx.move_to(x - (40 - 10 * k) * U, yy); ctx.line_to(x + (40 - 10 * k) * U, yy)
        ctx.set_line_width(5 * U); rgba(ctx, col, (0.45 - 0.13 * k) * a * (0.6 + 0.4 * math.sin(t * 14 + k))); ctx.stroke()

def positions(k):
    e = ease(k)
    ys = {"1": H * 0.24, "2": H * (0.36 + 0.12 * e), "YOU": H * (0.48 - 0.12 * e), "4": H * 0.60}
    xs = {"1": CX, "2": CX + 60 * U * e, "YOU": CX - 170 * U * math.sin(math.pi * e), "4": CX}
    return xs, ys

def draw_race(ctx, t, k, a=1.0):
    xs, ys = positions(k)
    for lab in ("4", "2", "1", "YOU"):
        runner(ctx, xs[lab], ys[lab], lab, RUN[lab], t, a, 1.12 if lab == "YOU" else 1.0)

def sc_hook(ctx, t, d):
    bg(ctx, t)
    lanes(ctx, t, prog(t, 0, 0.4))
    draw_race(ctx, t, 0.0, prog(t, 0.0, 0.3))
    neon_text(ctx, "BRAIN TEST", CX, H * 0.095, 120 * U, CYAN, prog(t, 0, 0.25), PURPLE, fill=0.15)
    neon_text(ctx, "YOU PASS 2ND PLACE...", CX, H * 0.155, 64 * U, GOLD, prog(t, 0, 0.25))

def sc_race(ctx, t, d):
    bg(ctx, t)
    lanes(ctx, t)
    k = prog(t, d * 0.25, d * 0.6)
    draw_race(ctx, t, k)
    if 0.05 < k:
        a = min(1, k * 3) * (1 - prog(t, d * 0.7, d * 0.8))
        neon_path(ctx, lambda c: (c.move_to(CX - 280 * U, H * 0.50), c.curve_to(CX - 330 * U, H * 0.44, CX - 330 * U, H * 0.39, CX - 260 * U, H * 0.35)), GOLD, 5 * U, a)
    qa = prog(t, d * 0.62, d * 0.75)
    neon_text(ctx, "WHAT PLACE", CX, H * 0.085, 92 * U, WHITE, qa, PURPLE)
    neon_text(ctx, "ARE YOU NOW?", CX, H * 0.145, 92 * U, GOLD, qa, CORAL)

def sc_think(ctx, t, d):
    bg(ctx, t, PINK)
    # one central element: a giant neon question mark
    s = 1 + 0.05 * math.sin(t * 5)
    ctx.save(); ctx.translate(CX, H * 0.36); ctx.scale(s, s); ctx.translate(-CX, -H * 0.36)
    neon_text(ctx, "?", CX, H * 0.36, 620 * U, PINK, 1.0, PURPLE, fill=0.12)
    ctx.restore()
    for i, (lab, col) in enumerate((("1ST", CYAN), ("2ND", PINK), ("3RD", GOLD))):
        k = prog(t, i * d * 0.18, i * d * 0.18 + 0.3)
        neon_text(ctx, lab, CX + (i - 1) * 330 * U, H * 0.62, 96 * U, col, k)

def sc_reveal(ctx, t, d):
    bg(ctx, t, GOLD)
    lanes(ctx, t, 0.5)
    draw_race(ctx, t, 1.0, 0.55)
    k = prog(t, 0.0, 0.3)
    s = (1 + 0.3 * (1 - k)) * (1 + 0.04 * math.sin(t * 8))
    ctx.save(); ctx.translate(CX, H * 0.12); ctx.scale(s, s); ctx.translate(-CX, -H * 0.12)
    neon_text(ctx, "2ND!", CX, H * 0.12, 220 * U, GOLD, k, CORAL, fill=0.35)
    ctx.restore()
    xs, ys = positions(1.0)
    neon_text(ctx, "STILL 1ST", xs["1"] + 330 * U, ys["1"], 50 * U, CYAN, prog(t, d * 0.45, d * 0.6))

def sc_outro(ctx, t, d):
    bg(ctx, t)
    cta(ctx, t, d, "WHAT IF YOU PASS THE LAST?", "COMMENT YOUR ANSWER")

SHORT_SCENES = ["hook", "race", "think", "reveal", "outro"]
SCENES = dict(hook=sc_hook, race=sc_race, think=sc_think, reveal=sc_reveal, outro=sc_outro)

def thumbnail(c):
    vgrad(c, (0.10, 0.04, 0.22), (0.01, 0.02, 0.08))
    thumb_text(c, "YOU PASS 2ND.", "WHAT PLACE?", "BRAIN TEST")
