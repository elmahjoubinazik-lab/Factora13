# Episode 017 (Short only) - "Why do officials say 72 hours?" (emergency kit)
# Executed inside engine/render.py (helpers available). Vertical layout. Original vector illustration.
# Calm, practical tone: no disaster drawn, no war imagery.

def bg(ctx, t, top=(0.10, 0.06, 0.30), bot=NAVY):
    vgrad(ctx, top, bot); stars(ctx, t, 0.35)

def dial(ctx, x, y, r, k, col, t, hand=True):
    """Clock ring filling up to k (0..1) with ticks."""
    glow(ctx, x, y, r * 1.6, col, 0.35)
    ctx.new_path(); ctx.arc(x, y, r, 0, 2 * math.pi); ctx.set_line_width(34 * U); rgba(ctx, (1, 1, 1), 0.10); ctx.stroke()
    if k > 0:
        ctx.new_path(); ctx.arc(x, y, r, -math.pi / 2, -math.pi / 2 + 2 * math.pi * k)
        ctx.set_line_width(34 * U); ctx.set_line_cap(cairo.LINE_CAP_ROUND); rgba(ctx, col); ctx.stroke()
    for i in range(24):
        a = i / 24 * 2 * math.pi
        r1, r2 = r - 50 * U, r - (70 if i % 6 == 0 else 60) * U
        ctx.move_to(x + math.cos(a) * r1, y + math.sin(a) * r1); ctx.line_to(x + math.cos(a) * r2, y + math.sin(a) * r2)
    ctx.set_line_width(5 * U); rgba(ctx, WHITE, 0.5); ctx.stroke()
    if not hand: return
    a = -math.pi / 2 + 2 * math.pi * k
    ctx.move_to(x, y); ctx.line_to(x + math.cos(a) * (r - 90 * U), y + math.sin(a) * (r - 90 * U))
    ctx.set_line_width(10 * U); ctx.set_line_cap(cairo.LINE_CAP_ROUND); rgba(ctx, WHITE, 0.85); ctx.stroke()
    circle(ctx, x, y, 14 * U, WHITE)

def sc_hook(ctx, t, d):
    bg(ctx, t)
    k = prog(t, 0.2, 2.4)
    cy = H * 0.47
    dial(ctx, CX, cy, 400 * U, k, GOLD, t, hand=False)
    hrs = int(round(72 * k))
    text(ctx, "%d" % hrs, CX + 6 * U, cy + 10 * U, 230 * U, (0, 0, 0), 0.4)
    text(ctx, "%d" % hrs, CX, cy, 230 * U, GOLD)
    text(ctx, "HOURS", CX, cy + 160 * U, 64 * U, WHITE, 0.9)
    # floating question marks
    for i in range(6):
        ang = i / 6 * 2 * math.pi + t * 0.5
        x, y = CX + math.cos(ang) * 440 * U, cy + math.sin(ang) * 420 * U
        text(ctx, "?", x, y, (60 + 15 * math.sin(t * 3 + i)) * U, [CORAL, CYAN, PINK][i % 3], 0.75 * prog(t, 0.5, 1.2))
    chip(ctx, "EMERGENCY KIT", t)

def house(ctx, x, y, s, lit, a=1.0):
    col = GOLD if lit else (0.22, 0.26, 0.42)
    if lit: glow(ctx, x, y, 90 * s, GOLD, 0.35 * a)
    ctx.move_to(x - 42 * s, y - 10 * s); ctx.line_to(x, y - 48 * s); ctx.line_to(x + 42 * s, y - 10 * s); ctx.close_path()
    rgba(ctx, mix(col, (0.9, 0.3, 0.3), 0.35), a); ctx.fill()
    ctx.rectangle(x - 34 * s, y - 12 * s, 68 * s, 52 * s); rgba(ctx, mix(col, WHITE, 0.15), a); ctx.fill()
    ctx.rectangle(x - 10 * s, y + 12 * s, 20 * s, 28 * s); rgba(ctx, NAVY, a); ctx.fill()

def truck(ctx, x, y, s, t):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -90, -55, 120, 70, 10); rgba(ctx, WHITE); ctx.fill()
    rrect(ctx, 30, -40, 55, 55, 10); rgba(ctx, CORAL); ctx.fill()
    ctx.rectangle(42, -32, 30, 20); rgba(ctx, CYAN); ctx.fill()
    ctx.rectangle(-45, -40, 14, 40); rgba(ctx, CORAL); ctx.fill(); ctx.rectangle(-58, -27, 40, 14); ctx.fill()
    for wx in (-60, 50):
        circle(ctx, wx, 18, 17, (0.1, 0.1, 0.15)); circle(ctx, wx, 18, 7, (0.6, 0.6, 0.7))
    on = int(t * 6) % 2
    glow(ctx, -70, -62, 45, CORAL if on else CYAN, 0.8); circle(ctx, -70, -62, 9, CORAL if on else CYAN)
    ctx.restore()

def sc_rescue(ctx, t, d):
    bg(ctx, t, (0.05, 0.14, 0.26))
    # map: road snake through a grid of houses
    rows = [H * 0.27, H * 0.40, H * 0.53]
    road_y = [H * 0.335, H * 0.465, H * 0.595]
    for ry in road_y:
        ctx.rectangle(0, ry - 26 * U, W, 52 * U); rgba(ctx, (0.18, 0.2, 0.32)); ctx.fill()
        ctx.set_dash([30 * U, 26 * U], -t * 60 * U); ctx.move_to(0, ry); ctx.line_to(W, ry)
        ctx.set_line_width(5 * U); rgba(ctx, GOLD, 0.6); ctx.stroke(); ctx.set_dash([])
    # hospital (top right) = worst emergency, lit first
    hx, hy = W * 0.80, rows[0]
    glow(ctx, hx, hy, 170 * U, CORAL, 0.45 * (0.8 + 0.2 * math.sin(t * 5)))
    rrect(ctx, hx - 85 * U, hy - 70 * U, 170 * U, 110 * U, 12 * U); rgba(ctx, WHITE); ctx.fill()
    ctx.rectangle(hx - 12 * U, hy - 55 * U, 24 * U, 70 * U); rgba(ctx, CORAL); ctx.fill()
    ctx.rectangle(hx - 35 * U, hy - 32 * U, 70 * U, 24 * U); ctx.fill()
    text(ctx, "WORST FIRST", hx, hy - 110 * U, 34 * U, CORAL, prog(t, 0.3, 0.9))
    # truck progresses slowly along the roads (zigzag)
    p = clamp(t / d) * 2.6
    seg = min(2, int(p)); f = p - seg
    tx = (W * 0.08 + f * W * 0.84) if seg % 2 == 0 else (W * 0.92 - f * W * 0.84)
    houses_xy = [(W * (0.12 + 0.19 * i), rows[r]) for r in range(3) for i in range(5) if not (r == 0 and i >= 3)]
    for (x, y) in houses_xy:
        r = rows.index(y)
        # a house lights up once the truck has passed it
        passed = (r < seg) or (r == seg and ((x < tx) if seg % 2 == 0 else (x > tx)))
        house(ctx, x, y + 10 * U, 1.35 * U, passed)
    truck(ctx, tx, road_y[seg] - 8 * U, 1.0 * U, t)
    # blocked road sign on last road
    bx, by = W * 0.5, road_y[2]
    if seg < 2:
        ctx.save(); ctx.translate(bx, by); ctx.rotate(0.05 * math.sin(t * 3))
        rrect(ctx, -70 * U, -28 * U, 140 * U, 56 * U, 10 * U); rgba(ctx, GOLD); ctx.fill()
        for i in range(4):
            ctx.move_to(-60 * U + i * 36 * U, 24 * U); ctx.line_to(-40 * U + i * 36 * U, -24 * U)
        ctx.set_line_width(12 * U); rgba(ctx, NAVY); ctx.stroke(); ctx.restore()
    # big 72 H tag
    k = prog(t, d * 0.65, d * 0.8)
    if k:
        s = 0.8 + 0.2 * ease(k)
        ctx.save(); ctx.translate(CX, H * 0.155); ctx.scale(s, s)
        rrect(ctx, -420 * U, -70 * U, 840 * U, 140 * U, 70 * U); rgba(ctx, NAVY, 0.92 * k); ctx.fill()
        ctx.set_line_width(6 * U); rgba(ctx, GOLD, k); rrect(ctx, -420 * U, -70 * U, 840 * U, 140 * U, 70 * U); ctx.stroke()
        text(ctx, "ON YOUR OWN: 72 H", 0, 0, 66 * U, GOLD, k); ctx.restore()
    else:
        chip(ctx, "HELP TAKES TIME", t)

def jug(ctx, x, y, s, fill, a=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    glow(ctx, 0, 0, 150, CYAN, 0.3 * a)
    rrect(ctx, -70, -90, 140, 180, 28); rgba(ctx, (0.85, 0.95, 1.0), 0.25 * a); ctx.fill()
    ctx.save(); rrect(ctx, -70, -90, 140, 180, 28); ctx.clip()
    lvl = 90 - 180 * fill
    g = cairo.LinearGradient(0, lvl, 0, 90); g.add_color_stop_rgba(0, *CYAN, a); g.add_color_stop_rgba(1, 0.1, 0.45, 1.0, a)
    ctx.set_source(g); ctx.rectangle(-70, lvl, 140, 180); ctx.fill(); ctx.restore()
    ctx.set_line_width(6); rgba(ctx, WHITE, 0.8 * a); rrect(ctx, -70, -90, 140, 180, 28); ctx.stroke()
    rrect(ctx, -22, -122, 44, 36, 8); rgba(ctx, CYAN, a); ctx.fill()
    rrect(ctx, 30, -70, 26, 70, 13); ctx.set_line_width(8); rgba(ctx, WHITE, 0.6 * a); ctx.stroke()
    ctx.restore()

def sc_water(ctx, t, d):
    bg(ctx, t, (0.03, 0.18, 0.30))
    # bubbles
    random.seed(5)
    for _ in range(40):
        x = random.random() * W; sp = random.uniform(40, 120); ph = random.random() * 10
        y = H * 0.68 - ((t * sp + ph * 80) % (H * 0.5))
        circle(ctx, x, y, random.uniform(4, 12) * U, CYAN, 0.25)
    # 3 jugs = 3 days, appearing one after another
    for i in range(3):
        k = prog(t, d * (0.42 + 0.12 * i), d * (0.5 + 0.12 * i))
        if k <= 0: continue
        x = CX + (i - 1) * 300 * U
        y = H * 0.50 - (1 - k) * 200 * U
        jug(ctx, x, y, 1.45 * U, ease(k), k)
        text(ctx, "DAY %d" % (i + 1), x, H * 0.62, 44 * U, WHITE, k)
    # big figure
    fk = prog(t, d * 0.75, d * 0.88)
    if fk:
        text(ctx, "1 GALLON", CX, H * 0.25, 130 * U, CYAN, fk)
        text(ctx, "PER PERSON, PER DAY", CX, H * 0.315, 52 * U, WHITE, fk)
    else:
        # ~3 days without water (rough)
        k = prog(t, 0.2, 0.8)
        dk = 1 - prog(t, d * 0.3, d * 0.42)
        if dk > 0:
            r = 170 * U * (0.7 + 0.3 * k) * (0.92 + 0.08 * math.sin(t * 3))
            x, y = CX, H * 0.50
            glow(ctx, x, y, r * 2.2, CYAN, 0.45 * dk)
            ctx.save(); ctx.translate(x, y); ctx.scale(r, r)
            ctx.move_to(0, -1.5); ctx.curve_to(0.95, -0.25, 1.05, 1.0, 0, 1.0); ctx.curve_to(-1.05, 1.0, -0.95, -0.25, 0, -1.5); ctx.restore()
            g = cairo.LinearGradient(0, y - 1.5 * r, 0, y + r); g.add_color_stop_rgba(0, *CYAN, dk); g.add_color_stop_rgba(1, 0.1, 0.4, 1.0, dk)
            ctx.set_source(g); ctx.fill()
            circle(ctx, x - 0.35 * r, y - 0.1 * r, 0.18 * r, WHITE, 0.5 * dk)
        text(ctx, "~3 DAYS", CX, H * 0.25, 130 * U, GOLD, k)
        text(ctx, "WITHOUT WATER (ROUGHLY)", CX, H * 0.315, 50 * U, WHITE, k)
    chip(ctx, "WATER COMES FIRST", t)

def sc_minimum(ctx, t, d):
    bg(ctx, t, (0.16, 0.05, 0.28))
    x0, x1, y = W * 0.10, W * 0.90, H * 0.47
    rrect(ctx, x0, y - 40 * U, x1 - x0, 80 * U, 40 * U); rgba(ctx, (1, 1, 1), 0.10); ctx.fill()
    k = prog(t, 0.3, d * 0.7)
    xe = x0 + (x1 - x0) * (0.43 * min(1, k * 2.2) + 0.57 * clamp((k - 0.45) / 0.55))
    g = cairo.LinearGradient(x0, 0, x1, 0); g.add_color_stop_rgb(0, *GOLD); g.add_color_stop_rgb(0.43, *CORAL); g.add_color_stop_rgb(1, *PURPLE)
    rrect(ctx, x0, y - 40 * U, max(80 * U, xe - x0), 80 * U, 40 * U); ctx.set_source(g); ctx.fill()
    glow(ctx, xe, y, 120 * U, PINK, 0.5)
    mx = x0 + (x1 - x0) * 0.43
    a1 = prog(t, 0.3, 0.9)
    text(ctx, "72 H", x0, y - 120 * U, 100 * U, GOLD, a1, True, "l")
    text(ctx, "MINIMUM", x0, y + 100 * U, 44 * U, WHITE, a1, True, "l")
    ctx.move_to(mx, y - 60 * U); ctx.line_to(mx, y + 60 * U); ctx.set_line_width(8 * U); rgba(ctx, WHITE, a1); ctx.stroke()
    a2 = prog(t, d * 0.55, d * 0.75)
    text(ctx, "1 WEEK", x1, y - 120 * U, 100 * U, PINK, a2, True, "r")
    text(ctx, "SWITZERLAND · SWEDEN", x1, y + 170 * U, 42 * U, WHITE, a2, True, "r")
    for i in range(8):
        xx = x0 + (x1 - x0) * i / 7
        ctx.move_to(xx, y + 48 * U); ctx.line_to(xx, y + 62 * U)
    ctx.set_line_width(4 * U); rgba(ctx, WHITE, 0.5); ctx.stroke()
    chip(ctx, "ONLY THE MINIMUM", t)

def sc_outro(ctx, t, d):
    bg(ctx, t)
    dial(ctx, CX, H * 0.42, 420 * U, (t / 6) % 1, PURPLE, t)
    ctx.set_source_rgba(0.02, 0.03, 0.12, 0.55); ctx.paint()
    cta(ctx, t, d, "COULD YOU LAST 72 HOURS?", "COMMENT YES OR NO")

SHORT_SCENES = ["hook", "rescue", "water", "minimum", "outro"]
SCENES = dict(hook=sc_hook, rescue=sc_rescue, water=sc_water, minimum=sc_minimum, outro=sc_outro)

def thumbnail(c):
    vgrad(c, (0.10, 0.06, 0.30), NAVY)
    thumb_text(c, "WHY", "72 HOURS?", "EMERGENCY KIT")
