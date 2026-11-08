# Episode 019 (Short only) - "Who's Lying? #1" — film-noir science mystery (fictional story, no violence)
# Executed inside engine/render.py (helpers available). Vertical layout. Original vector illustration. All sizes in U.
# Uses the engine globals TNOW (absolute time) and SFX_TIMES (thunder events) to sync lightning flashes.

COLS = [GOLD, CYAN, CORAL, GREEN]
NAMES = ["THE BUTLER", "THE MAID", "THE GARDENER", "THE NIECE"]
QUOTES = ["“LIGHTING CANDLES IN THE HALL”", "“MAKING TEA IN THE KITCHEN”",
          "“I HEARD THE THUNDER, THEN SAW THE LIGHTNING”", "“READING BY MY PHONE'S LIGHT”"]
INK = (0.03, 0.035, 0.08)

def flash():
    f = 0.0
    for (t0, kind) in SFX_TIMES:
        if kind == "thunder" and 0 <= TNOW - t0 < 1.4:
            e = TNOW - t0
            fl = 1.0 if e < 0.08 else (0.35 if e < 0.16 else (0.9 if e < 0.24 else math.exp(-(e - 0.24) * 5)))
            f = max(f, fl)
    return f

def rain(ctx, t, a=1.0, n=140):
    rnd = random.Random(21)
    ctx.set_line_width(2.5 * U); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    for i in range(n):
        x0 = rnd.random() * W * 1.3; sp = rnd.uniform(1800, 2600) * U; ph = rnd.random() * H
        y = (ph + t * sp) % (H * 1.1) - 0.05 * H; x = x0 - (y / H) * 0.25 * W
        ctx.move_to(x, y); ctx.line_to(x - 18 * U, y + 70 * U)
        rgba(ctx, (0.6, 0.7, 1.0), 0.22 * a)
        ctx.stroke()

def bolt(ctx, x, y0, y1, seed, a):
    if a <= 0.02: return
    rnd = random.Random(seed)
    pts = [(x, y0)]; yy = y0; xx = x
    while yy < y1:
        yy += rnd.uniform(40, 90) * U; xx += rnd.uniform(-60, 60) * U; pts.append((xx, yy))
    for wdt, al in ((26, 0.25), (12, 0.6), (5, 1.0)):
        ctx.new_path(); ctx.move_to(*pts[0])
        for p in pts[1:]: ctx.line_to(*p)
        ctx.set_line_width(wdt * U); rgba(ctx, (0.85, 0.9, 1.0), al * a); ctx.stroke()

def noir_bg(ctx, t, top=(0.05, 0.05, 0.16), bot=(0.01, 0.01, 0.04), rain_a=1.0):
    vgrad(ctx, top, bot)
    f = flash()
    if f > 0:
        rgba(ctx, (0.55, 0.62, 0.95), 0.35 * f); ctx.paint()
    rain(ctx, t, rain_a)
    return f

def overlay_flash(ctx, f):
    if f > 0:
        rgba(ctx, (0.85, 0.9, 1.0), 0.18 * f); ctx.paint()

def mansion(ctx, cx, base, s, lit, f):
    ctx.save(); ctx.translate(cx, base); ctx.scale(s, s)
    body = mix((0.02, 0.02, 0.05), (0.35, 0.40, 0.65), 0.6 * f)
    # main block, towers, roofs
    shapes = [(-330, -520, 660, 520), (-430, -700, 170, 700), (260, -760, 170, 760)]
    for (x, y, w, h) in shapes:
        ctx.rectangle(x, y, w, h); rgba(ctx, body); ctx.fill()
    for (x, y, w) in [(-450, -700, 210), (240, -760, 210)]:
        ctx.move_to(x, y); ctx.line_to(x + w / 2, y - 220); ctx.line_to(x + w, y); ctx.close_path(); rgba(ctx, body); ctx.fill()
    ctx.move_to(-360, -520); ctx.line_to(0, -760); ctx.line_to(360, -520); ctx.close_path(); rgba(ctx, body); ctx.fill()
    # windows
    for row in range(3):
        for col in range(5):
            x = -270 + col * 120; y = -460 + row * 150
            ctx.rectangle(x, y, 60, 90)
            if lit > 0:
                rgba(ctx, GOLD, 0.9 * lit); ctx.fill_preserve()
                glow(ctx, x + 30, y + 45, 90, GOLD, 0.25 * lit)
                ctx.rectangle(x, y, 60, 90)
            rgba(ctx, (0.15, 0.17, 0.30), 1 - lit if lit < 1 else 0); ctx.fill()
    for (x, y) in [(-380, -560), (310, -620)]:
        ctx.rectangle(x, y, 70, 100); rgba(ctx, GOLD if lit > 0 else (0.15, 0.17, 0.3), 0.85 * lit if lit > 0 else 1); ctx.fill()
    ctx.restore()

def eyes(ctx, x, y, s, a, t):
    blink = 0.15 if (t * 0.7) % 3 < 0.08 else 1.0
    for dx in (-17, 17):
        ctx.save(); ctx.translate(x + dx * s, y); ctx.scale(1, blink)
        glow(ctx, 0, 0, 22 * s, WHITE, 0.6 * a); circle(ctx, 0, 0, 8 * s, WHITE, a); ctx.restore()

def silhouette(ctx, x, y, s, col, kind, a=1.0, t=0.0, lit=0.0):
    """Shadowy suspect (feet at y): dark body, coloured rim light, glowing eyes. kind: 0 butler, 1 maid, 2 gardener, 3 niece."""
    if a <= 0: return
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    sway = 3 * math.sin(t * 1.3 + kind)
    body = mix(INK, col, 0.12 + 0.45 * lit)
    def shape():
        ctx.new_path()
        rrect(ctx, -70, -360 + sway, 140, 240, 60)
        ctx.new_sub_path(); ctx.arc(0, -410 + sway, 56, 0, 2 * math.pi)
        for lx in (-30, 30): ctx.new_sub_path(); rrect(ctx, lx - 18, -150, 36, 150, 14)
        if kind == 0:   # bowler hat
            ctx.new_sub_path(); rrect(ctx, -70, -462 + sway, 140, 20, 10)
            ctx.new_sub_path(); ctx.arc(0, -462 + sway, 44, math.pi, 2 * math.pi)
        elif kind == 1: # maid cap
            ctx.new_sub_path(); rrect(ctx, -48, -476 + sway, 96, 26, 12)
        elif kind == 2: # wide brim hat
            ctx.new_sub_path(); rrect(ctx, -100, -462 + sway, 200, 22, 11)
            ctx.new_sub_path(); rrect(ctx, -48, -510 + sway, 96, 56, 18)
        else:           # long hair
            ctx.new_sub_path(); rrect(ctx, -66, -458 + sway, 132, 150, 50)
    ctx.save(); ctx.scale(1, 0.22); circle(ctx, 0, 0, 110, (0, 0, 0), 0.5 * a); ctx.restore()
    shape(); rgba(ctx, body, a); ctx.fill()
    shape(); ctx.set_line_width(7); rgba(ctx, col, (0.55 + 0.45 * lit) * a); ctx.stroke()
    ctx.restore()
    eyes(ctx, x, y - (410 - sway) * s, s, a, t + kind)

def badge(ctx, x, y, n, col, a=1.0, r=44):
    if a <= 0: return
    glow(ctx, x, y, r * 2.2 * U, col, 0.45 * a)
    circle(ctx, x, y, r * U, col, a)
    text(ctx, str(n), x, y, r * 1.3 * U, INK, a)

def lineup(ctx, t, y, s=0.78, a=1.0, f=0.0, stagger=True):
    for i in range(4):
        x = W * (0.14 + 0.24 * i)
        k = (prog(t, 0.2 + i * 0.3, 0.6 + i * 0.3) if stagger else 1.0) * a
        silhouette(ctx, x, y, s * U, COLS[i], i, k, t, f * 0.8)
        badge(ctx, x, y + 70 * U, i + 1, COLS[i], k)

# ---------------- scenes ----------------
def sc_hook(ctx, t, d):
    f = noir_bg(ctx, t, (0.16, 0.18, 0.42), (0.04, 0.04, 0.12))
    bolt(ctx, W * 0.72, 0, H * 0.32, 4, f)
    lit = 1.0 - prog(t, d * 0.45, d * 0.55)          # the power goes out
    if (d * 0.45) < t < (d * 0.6) and int(t * 20) % 3 == 0: lit = 1.0   # flicker
    mansion(ctx, CX, H * 0.64, 1.0 * U, lit, f)
    rgba(ctx, INK); ctx.rectangle(0, H * 0.64, W, H); ctx.fill()
    overlay_flash(ctx, f)
    chip(ctx, "WHO'S LYING? #1", t)

def pedestal(ctx, cx, cy, a, t, empty=True):
    glow(ctx, cx, cy - 120 * U, 380 * U, (0.9, 0.9, 1.0), 0.35 * a)
    # spotlight cone
    g = cairo.LinearGradient(0, 0, 0, cy + 200 * U); g.add_color_stop_rgba(0, 1, 1, 0.9, 0.0); g.add_color_stop_rgba(1, 1, 1, 0.9, 0.22 * a)
    ctx.move_to(cx - 40 * U, 0); ctx.line_to(cx + 40 * U, 0); ctx.line_to(cx + 330 * U, cy + 200 * U); ctx.line_to(cx - 330 * U, cy + 200 * U); ctx.close_path()
    ctx.set_source(g); ctx.fill()
    rrect(ctx, cx - 150 * U, cy, 300 * U, 360 * U, 16 * U); rgba(ctx, (0.35, 0.10, 0.18), a); ctx.fill()
    rrect(ctx, cx - 190 * U, cy - 30 * U, 380 * U, 50 * U, 14 * U); rgba(ctx, (0.55, 0.14, 0.26), a); ctx.fill()
    # glass dome
    ctx.save(); ctx.translate(cx, cy - 30 * U); ctx.scale(1, 1.15)
    ctx.new_path(); ctx.arc(0, 0, 150 * U, math.pi, 2 * math.pi)
    rgba(ctx, CYAN, 0.10 * a); ctx.fill_preserve(); ctx.set_line_width(5 * U); rgba(ctx, CYAN, 0.7 * a); ctx.stroke(); ctx.restore()
    if not empty:
        ctx.save(); ctx.translate(cx, cy - 90 * U); ctx.rotate(t)
        for i in range(6):
            an = i / 6 * 2 * math.pi
            ctx.move_to(0, 0); ctx.line_to(math.cos(an) * 60 * U, math.sin(an) * 60 * U)
        ctx.set_line_width(4 * U); rgba(ctx, WHITE, a); ctx.stroke(); ctx.restore()
        glow(ctx, cx, cy - 90 * U, 120 * U, CYAN, 0.8 * a)

def sc_dark(ctx, t, d):
    vgrad(ctx, (0.0, 0.0, 0.02), (0.0, 0.0, 0.0))
    rain(ctx, t, 0.35)
    on = prog(t, d * 0.42, d * 0.5)
    if on < 1:
        # torch beam sweeping in the dark
        ang = -0.6 + 1.2 * (0.5 + 0.5 * math.sin(t * 1.6))
        ctx.save(); ctx.translate(CX, H * 0.95); ctx.rotate(ang)
        g = cairo.LinearGradient(0, 0, 0, -H * 0.8); g.add_color_stop_rgba(0, 1, 0.95, 0.7, 0.35 * (1 - on)); g.add_color_stop_rgba(1, 1, 0.95, 0.7, 0)
        ctx.move_to(-30 * U, 0); ctx.line_to(30 * U, 0); ctx.line_to(260 * U, -H * 0.8); ctx.line_to(-260 * U, -H * 0.8); ctx.close_path(); ctx.set_source(g); ctx.fill()
        ctx.restore()
        text(ctx, "...", CX, H * 0.36, 160 * U, WHITE, 0.5 * (1 - on))
    if on > 0:
        pedestal(ctx, CX, H * 0.40, on, t, empty=True)
        gk = prog(t, d * 0.58, d * 0.7)
        s = 1 + 0.06 * math.sin(t * 8)
        ctx.save(); ctx.translate(CX, H * 0.155); ctx.scale(s * (0.6 + 0.4 * gk), s * (0.6 + 0.4 * gk))
        text(ctx, "THE DIAMOND", 0, -60 * U, 96 * U, WHITE, gk)
        text(ctx, "IS GONE", 0, 50 * U, 120 * U, CORAL, gk); ctx.restore()

def sc_lineup(ctx, t, d):
    f = noir_bg(ctx, t, (0.06, 0.04, 0.14))
    z = 1 + 0.06 * prog(t, 0, d)
    ctx.save(); ctx.translate(CX, H * 0.55); ctx.scale(z, z); ctx.translate(-CX, -H * 0.55)
    lineup(ctx, t, H * 0.60, 0.85, 1.0, f)
    ctx.restore()
    lk = prog(t, d * 0.45, d * 0.6)
    text(ctx, "4 SUSPECTS", CX, H * 0.13, 110 * U, WHITE, prog(t, 0.1, 0.5))
    text(ctx, "1 LIAR", CX, H * 0.205, 110 * U, CORAL, lk)

def lamp(ctx, t, a=1.0):
    sw = 0.12 * math.sin(t * 1.4)
    ctx.save(); ctx.translate(CX, 0); ctx.rotate(sw)
    ctx.move_to(0, 0); ctx.line_to(0, H * 0.20); ctx.set_line_width(5 * U); rgba(ctx, (0.3, 0.3, 0.35), a); ctx.stroke()
    ctx.move_to(-90 * U, H * 0.25); ctx.line_to(90 * U, H * 0.25); ctx.line_to(40 * U, H * 0.20); ctx.line_to(-40 * U, H * 0.20); ctx.close_path()
    rgba(ctx, (0.25, 0.27, 0.32), a); ctx.fill()
    g = cairo.LinearGradient(0, H * 0.25, 0, H * 0.78); g.add_color_stop_rgba(0, 1, 0.92, 0.65, 0.42 * a); g.add_color_stop_rgba(1, 1, 0.92, 0.65, 0.0)
    ctx.move_to(-85 * U, H * 0.25); ctx.line_to(85 * U, H * 0.25); ctx.line_to(420 * U, H * 0.78); ctx.line_to(-420 * U, H * 0.78); ctx.close_path()
    ctx.set_source(g); ctx.fill()
    glow(ctx, 0, H * 0.255, 110 * U, (1, 0.9, 0.6), 0.8 * a)
    ctx.restore()

def prop(ctx, i, x, y, t, a):
    if a <= 0: return
    if i == 0:   # candelabra
        for k, dx in enumerate((-60, 0, 60)):
            rrect(ctx, x + (dx - 12) * U, y - 100 * U, 24 * U, 110 * U, 6 * U); rgba(ctx, (0.95, 0.92, 0.85), a); ctx.fill()
            fl = 1 + 0.15 * math.sin(t * 13 + k * 2)
            glow(ctx, x + dx * U, y - 130 * U, 80 * U, GOLD, 0.6 * a)
            ctx.save(); ctx.translate(x + dx * U, y - 125 * U); ctx.scale(1, fl)
            ctx.move_to(0, -30 * U); ctx.curve_to(16 * U, -8 * U, 12 * U, 10 * U, 0, 12 * U); ctx.curve_to(-12 * U, 10 * U, -16 * U, -8 * U, 0, -30 * U)
            rgba(ctx, (1, 0.8, 0.3), a); ctx.fill(); ctx.restore()
        rrect(ctx, x - 100 * U, y + 10 * U, 200 * U, 24 * U, 10 * U); rgba(ctx, GOLD, a); ctx.fill()
    elif i == 1: # teacup + steam
        rrect(ctx, x - 80 * U, y - 60 * U, 160 * U, 110 * U, 40 * U); rgba(ctx, WHITE, a); ctx.fill()
        ctx.new_path(); ctx.arc(x + 95 * U, y - 5 * U, 32 * U, -1.4, 1.4); ctx.set_line_width(14 * U); rgba(ctx, WHITE, a); ctx.stroke()
        for k in range(3):
            ph = t * 1.5 + k
            ctx.new_path(); ctx.move_to(x + (k - 1) * 40 * U, y - 80 * U)
            ctx.curve_to(x + ((k - 1) * 40 + 30 * math.sin(ph)) * U, y - 140 * U, x + ((k - 1) * 40 - 30 * math.sin(ph)) * U, y - 190 * U, x + (k - 1) * 40 * U, y - 240 * U)
            ctx.set_line_width(8 * U); rgba(ctx, WHITE, 0.35 * a); ctx.stroke()
    elif i == 2: # greenhouse in the rain
        ctx.move_to(x - 150 * U, y + 40 * U); ctx.line_to(x - 150 * U, y - 90 * U); ctx.line_to(x, y - 190 * U); ctx.line_to(x + 150 * U, y - 90 * U); ctx.line_to(x + 150 * U, y + 40 * U); ctx.close_path()
        rgba(ctx, GREEN, 0.18 * a); ctx.fill_preserve(); ctx.set_line_width(6 * U); rgba(ctx, GREEN, 0.9 * a); ctx.stroke()
        for dx in (-75, 0, 75):
            ctx.move_to(x + dx * U, y + 40 * U); ctx.line_to(x + dx * U, y - 140 * U + abs(dx) * 0.6 * U)
        ctx.set_line_width(4 * U); rgba(ctx, GREEN, 0.7 * a); ctx.stroke()
    else:        # phone torch
        ctx.save(); ctx.translate(x, y); ctx.rotate(-0.4)
        g = cairo.LinearGradient(0, 0, 0, -380 * U); g.add_color_stop_rgba(0, 1, 1, 1, 0.45 * a); g.add_color_stop_rgba(1, 1, 1, 1, 0)
        ctx.move_to(-10 * U, -60 * U); ctx.line_to(10 * U, -60 * U); ctx.line_to(170 * U, -380 * U); ctx.line_to(-170 * U, -380 * U); ctx.close_path(); ctx.set_source(g); ctx.fill()
        rrect(ctx, -45 * U, -70 * U, 90 * U, 160 * U, 18 * U); rgba(ctx, (0.12, 0.13, 0.2), a); ctx.fill()
        circle(ctx, 0, -50 * U, 10 * U, WHITE, a)
        ctx.restore()

def suspect(i):
    def sc(ctx, t, d):
        f = noir_bg(ctx, t, mix(COLS[i], INK, 0.88), (0.0, 0.0, 0.02), 0.7)
        lamp(ctx, t, prog(t, 0, 0.3))
        k = prog(t, 0.05, 0.5)
        silhouette(ctx, W * 0.36, H * 0.66 + (1 - k) * 60 * U, 1.12 * U, COLS[i], i, k, t, 0.55 + 0.45 * f)
        prop(ctx, i, W * 0.74, H * 0.56, t, prog(t, 0.3, 0.8))
        badge(ctx, W * 0.12, H * 0.115, i + 1, COLS[i], k, 56)
        text(ctx, NAMES[i], W * 0.21, H * 0.115, 78 * U, WHITE, k, True, "l")
        qk = prog(t, d * 0.3, d * 0.45)
        if qk:
            font(ctx, 50 * U); qw = ctx.text_extents(QUOTES[i]).width
            qs = 50 * U * min(1, W * 0.84 / max(1, qw))
            rrect(ctx, CX - W * 0.46, H * 0.19 - 50 * U, W * 0.92, 100 * U, 50 * U); rgba(ctx, (0, 0, 0), 0.75 * qk); ctx.fill()
            ctx.set_line_width(3 * U); rgba(ctx, COLS[i], 0.8 * qk); rrect(ctx, CX - W * 0.46, H * 0.19 - 50 * U, W * 0.92, 100 * U, 50 * U); ctx.stroke()
            text(ctx, QUOTES[i], CX, H * 0.19, qs, COLS[i], qk)
        overlay_flash(ctx, f)
    return sc

def board(ctx, t, a=1.0):
    # cork-style evidence board with 4 polaroids linked by red strings
    rrect(ctx, W * 0.05, H * 0.27, W * 0.9, H * 0.40, 24 * U); rgba(ctx, (0.20, 0.13, 0.10), a); ctx.fill()
    pts = []
    for i in range(4):
        x = W * (0.22 + 0.56 * (i % 2)); y = H * (0.36 + 0.19 * (i // 2))
        pts.append((x, y))
    ctx.set_line_width(5 * U)
    for (p, q) in [(0, 3), (1, 2), (0, 1), (2, 3)]:
        ctx.move_to(*pts[p]); ctx.line_to(*pts[q]); rgba(ctx, CORAL, 0.8 * a); ctx.stroke()
    for i, (x, y) in enumerate(pts):
        ctx.save(); ctx.translate(x, y); ctx.rotate((-0.08, 0.06, 0.07, -0.05)[i])
        rrect(ctx, -150 * U, -150 * U, 300 * U, 330 * U, 8 * U); rgba(ctx, (0.95, 0.94, 0.9), a); ctx.fill()
        ctx.rectangle(-130 * U, -130 * U, 260 * U, 240 * U); rgba(ctx, INK, a); ctx.fill()
        ctx.restore()
        silhouette(ctx, x, y + 95 * U, 0.42 * U, COLS[i], i, a, t, 0.7)
        badge(ctx, x, y + 150 * U, i + 1, COLS[i], a, 30)
        circle(ctx, x, y - 140 * U, 14 * U, CORAL, a)

def sc_think(ctx, t, d):
    f = noir_bg(ctx, t, (0.10, 0.03, 0.08))
    z = 1 + 0.10 * prog(t, 0, d)
    ctx.save(); ctx.translate(CX, H * 0.47); ctx.scale(z, z); ctx.translate(-CX, -H * 0.47)
    board(ctx, t)
    ctx.restore()
    pulse = 1 + 0.10 * abs(math.sin(t * 5))
    ctx.save(); ctx.translate(CX, H * 0.155); ctx.scale(pulse, pulse)
    text(ctx, "WHO'S LYING?", 0, 0, 120 * U, CORAL); ctx.restore()

def sc_outro(ctx, t, d):
    noir_bg(ctx, t, (0.06, 0.03, 0.12))
    board(ctx, t, 0.25)
    cta(ctx, t, d, "WHO'S LYING? 1, 2, 3 OR 4?", "COMMENT THE NUMBER")

SHORT_SCENES = ["hook", "dark", "lineup", "s1", "s2", "s3", "s4", "think", "outro"]
SCENES = dict(hook=sc_hook, dark=sc_dark, lineup=sc_lineup, s1=suspect(0), s2=suspect(1), s3=suspect(2), s4=suspect(3), think=sc_think, outro=sc_outro)

def thumbnail(c):
    vgrad(c, (0.06, 0.05, 0.16), (0.01, 0.01, 0.04))
    thumb_text(c, "WHO'S", "LYING?", "CAN YOU SOLVE IT?")
