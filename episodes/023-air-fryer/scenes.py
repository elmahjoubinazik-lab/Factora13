# Episode 023 (Short only) - "What's hiding above your air fryer basket?" — sober NEON style
# Executed inside engine/render.py (helpers available). Vertical layout. Original vector animation. All sizes in U.
# Facts: Philips Airfryer support (turn upside down on a soft cloth, soft-to-medium bristle brush, no steel brush,
# dry with paper towel), CHOICE (residue can smoke and even catch alight), Ireland CCPC warning (fire hazard).

GRIME = (0.30, 0.17, 0.06)
HOT = (1.0, 0.45, 0.12)

def fryer(ctx, x, y, s, t, a=1.0, cut=0.0, grime=0.0, heat=1.0):
    """Front view of an air fryer (y = centre). cut > 0 opens an x-ray window on the heating coil."""
    if a <= 0: return
    S = U * s
    w, h = 600 * S, 700 * S
    glow(ctx, x, y, 520 * S, CYAN, 0.25 * a)
    body = lambda c: rrect(c, x - w / 2, y - h / 2, w, h, 120 * S)
    ctx.new_path(); body(ctx)
    g = cairo.LinearGradient(x - w / 2, 0, x + w / 2, 0)
    g.add_color_stop_rgba(0, 0.10, 0.12, 0.20, a); g.add_color_stop_rgba(0.5, 0.20, 0.23, 0.34, a); g.add_color_stop_rgba(1, 0.08, 0.09, 0.16, a)
    ctx.set_source(g); ctx.fill()
    neon_path(ctx, body, CYAN, 6 * S, a)
    # control panel
    rrect(ctx, x - 150 * S, y - h / 2 + 45 * S, 300 * S, 95 * S, 30 * S); rgba(ctx, (0.02, 0.03, 0.06), a); ctx.fill()
    text(ctx, "400°F", x, y - h / 2 + 92 * S, 56 * S, GOLD, a)
    # drawer + handle
    dy = y + 40 * S
    neon_path(ctx, lambda c: rrect(c, x - w / 2 + 40 * S, dy, w - 80 * S, h / 2 - 80 * S, 60 * S), CYAN, 4 * S, 0.6 * a)
    rrect(ctx, x - 130 * S, dy + 110 * S, 260 * S, 60 * S, 30 * S); rgba(ctx, (0.35, 0.38, 0.50), a); ctx.fill()
    # x-ray window on the heating coil (top inside)
    if cut > 0:
        wx, wy, ww, wh = x - w / 2 + 50 * S, y - h / 2 + 170 * S, w - 100 * S, 190 * S
        rrect(ctx, wx, wy, ww, wh, 30 * S); rgba(ctx, (0.02, 0.02, 0.05), 0.92 * cut * a); ctx.fill()
        neon_path(ctx, lambda c: rrect(c, wx, wy, ww, wh, 30 * S), GOLD, 4 * S, cut * a)
        # coil: zig-zag loops across the window
        cy = wy + wh / 2
        col = mix((0.55, 0.55, 0.6), HOT, heat)
        def coil(c):
            n = 9
            for i in range(n):
                cx = wx + 40 * S + i * (ww - 80 * S) / (n - 1)
                c.new_sub_path(); c.save(); c.translate(cx, cy); c.scale(1, 0.55); c.arc(0, 0, 30 * S, 0, 2 * math.pi); c.restore()
        neon_path(ctx, coil, col, 4 * S, cut * a)
        if heat > 0: glow(ctx, x, cy, 260 * S, HOT, 0.35 * heat * cut * a)
        # baked-on grease blobs
        if grime > 0:
            rnd = random.Random(31)
            for i in range(22):
                bx = wx + 50 * S + rnd.random() * (ww - 100 * S); by = cy + rnd.uniform(-22, 22) * S
                circle(ctx, bx, by, rnd.uniform(10, 20) * S, GRIME, 0.95 * grime * cut * a)
                circle(ctx, bx - 4 * S, by - 4 * S, 5 * S, (0.55, 0.35, 0.12), 0.7 * grime * cut * a)

def splatter(ctx, t, x0, y0, y1, a=1.0):
    """Grease droplets flying up from the basket towards the coil."""
    rnd = random.Random(5)
    for i in range(24):
        ph = rnd.random(); e = (t * 0.8 + ph) % 1.0
        px = x0 + rnd.uniform(-220, 220) * U + math.sin(e * 6 + i) * 10 * U
        py = y0 - (y0 - y1) * ease(e)
        circle(ctx, px, py, rnd.uniform(7, 13) * U, (1.0, 0.82, 0.35), 0.8 * a * (1 - e * 0.5))

def smoke(ctx, t, x, y, a):
    rnd = random.Random(2)
    for i in range(8):
        e = (t * 0.35 + i / 8) % 1.0
        sx = x + rnd.uniform(-200, 200) * U + math.sin(t * 2 + i) * 30 * U
        sy = y - e * 500 * U
        circle(ctx, sx, sy, (40 + 80 * e) * U, (0.55, 0.55, 0.6), 0.25 * a * (1 - e))

def flame(ctx, x, y, s, t, a):
    if a <= 0: return
    for k, (col, sc) in enumerate(((CORAL, 1.0), (GOLD, 0.62), ((1, 1, 0.8), 0.3))):
        h = (150 + 25 * math.sin(t * 17 + k)) * U * s * sc; w = 70 * U * s * sc
        ctx.move_to(x - w, y); ctx.curve_to(x - w, y - h * 0.5, x - w * 0.2, y - h * 0.7, x, y - h)
        ctx.curve_to(x + w * 0.2, y - h * 0.7, x + w, y - h * 0.5, x + w, y); ctx.close_path()
        rgba(ctx, col, 0.9 * a); ctx.fill()
    glow(ctx, x, y - 60 * U * s, 220 * U * s, CORAL, 0.5 * a)

def sc_hook(ctx, t, d):
    neon_bg(ctx, t, tint=CYAN)
    k = prog(t, d * 0.35, d * 0.7)
    fryer(ctx, CX, H * 0.50, 1.38, t, 1.0, cut=0.35 + 0.65 * k, grime=0.6 + 0.4 * k, heat=0.5)
    # arrow pointing at the hidden coil
    ya = H * 0.37 + 12 * U * math.sin(t * 6)
    neon_path(ctx, lambda c: (c.move_to(W * 0.90, ya - 120 * U), c.line_to(W * 0.80, ya - 20 * U),
                              c.move_to(W * 0.80, ya - 20 * U), c.line_to(W * 0.85, ya - 30 * U)), CORAL, 7 * U, 1.0)
    neon_text(ctx, "?", W * 0.90, ya - 190 * U, 150 * U, CORAL, 1.0, fill=0.3)

def sc_grease(ctx, t, d):
    neon_bg(ctx, t, tint=CORAL)
    g = prog(t, 0.2, d * 0.55)
    fryer(ctx, CX, H * 0.43, 1.2, t, 1.0, cut=1.0, grime=0.3 + 0.7 * g, heat=1.0)
    splatter(ctx, t, CX, H * 0.54, H * 0.33, 1 - prog(t, d * 0.6, d * 0.7))
    sa = prog(t, d * 0.5, d * 0.7)
    smoke(ctx, t, CX, H * 0.28, sa)
    flame(ctx, W * 0.66, H * 0.345, 0.8, t, prog(t, d * 0.78, d * 0.88))
    neon_text(ctx, "GREASE BURNS ON THE COIL", CX, H * 0.085, 70 * U, GOLD, prog(t, 0, 0.3), fill=0.15)
    rk = prog(t, d * 0.55, d * 0.7)
    for i, (lab, col) in enumerate((("SMOKE", WHITE), ("BURNT TASTE", GOLD), ("FIRE RISK", CORAL))):
        kk = prog(t, d * (0.55 + 0.12 * i), d * (0.65 + 0.12 * i))
        neon_text(ctx, lab, W * (0.17 + 0.33 * i), H * 0.68, 44 * U, col, kk, fill=0.2)

def spiral_coil(ctx, x, y, r, t, grime, a):
    """Heating element seen from below (air fryer flipped): flat spiral inside a round guard."""
    neon_path(ctx, lambda c: c.arc(x, y, r * 1.12, 0, 2 * math.pi), (0.6, 0.65, 0.8), 5 * U, 0.7 * a)
    def sp(c):
        n = 260
        for i in range(n + 1):
            th = i / n * 4.2 * 2 * math.pi; rr = r * (0.12 + 0.88 * i / n)
            px, py = x + math.cos(th) * rr, y + math.sin(th) * rr
            (c.move_to if i == 0 else c.line_to)(px, py)
    neon_path(ctx, sp, mix((0.75, 0.75, 0.8), CYAN, 0.4), 9 * U, a)
    if grime > 0:
        rnd = random.Random(17)
        for i in range(40):
            th = rnd.uniform(0, 4.2 * 2 * math.pi); rr = r * (0.12 + 0.88 * th / (4.2 * 2 * math.pi))
            circle(ctx, x + math.cos(th) * rr, y + math.sin(th) * rr, rnd.uniform(12, 24) * U, GRIME, 0.95 * grime * a)

def brush(ctx, x, y, ang, a):
    ctx.save(); ctx.translate(x, y); ctx.rotate(ang)
    rrect(ctx, -40 * U, -260 * U, 80 * U, 230 * U, 30 * U); rgba(ctx, PURPLE, a); ctx.fill()
    rrect(ctx, -90 * U, -40 * U, 180 * U, 50 * U, 14 * U); rgba(ctx, (0.85, 0.85, 0.9), a); ctx.fill()
    for k in range(10):
        bx = -80 * U + k * 17.5 * U
        ctx.move_to(bx, 10 * U); ctx.line_to(bx, 55 * U)
    ctx.set_line_width(6 * U); rgba(ctx, (1, 0.95, 0.7), a); ctx.stroke()
    ctx.restore()

STEPS = [("UNPLUG", CYAN), ("LET IT COOL", CYAN), ("FLIP ONTO A TOWEL", GOLD), ("SOFT BRUSH + SOAPY WATER", GREEN), ("DRY IT", GREEN)]
STEP_T = [0.02, 0.10, 0.20, 0.47, 0.82]
WARN = "CHECK YOUR MANUAL  ·  NO STEEL WOOL"

def sc_clean(ctx, t, d):
    neon_bg(ctx, t, tint=GREEN)
    # checklist (top)
    for i, (lab, col) in enumerate(STEPS):
        k = prog(t, d * STEP_T[i], d * STEP_T[i] + 0.3)
        y = H * (0.05 + 0.042 * i)
        badge_x = W * 0.10
        circle(ctx, badge_x, y, 30 * U, col, k)
        text(ctx, str(i + 1), badge_x, y, 38 * U, (0.02, 0.03, 0.08), k)
        text(ctx, lab, badge_x + 60 * U, y, 52 * U, WHITE, k, True, "l")
    # flipped air fryer, coil facing up, being scrubbed
    text(ctx, WARN, W * 0.10 - 30 * U, H * 0.26, 44 * U, CORAL, prog(t, d * 0.25, d * 0.35), True, "l")
    cx, cy, r = CX, H * 0.475, 255 * U
    fa = prog(t, d * 0.18, d * 0.3)
    # towel
    rrect(ctx, W * 0.06, cy + r * 1.22, W * 0.88, 60 * U, 24 * U); rgba(ctx, GOLD, 0.35 * fa); ctx.fill()
    circle(ctx, cx, cy, r * 1.3, (0.12, 0.14, 0.22), fa)
    neon_path(ctx, lambda c: c.arc(cx, cy, r * 1.3, 0, 2 * math.pi), CYAN, 6 * U, fa)
    clean_k = prog(t, d * 0.5, d * 0.85)
    spiral_coil(ctx, cx, cy, r, t, 1 - clean_k, fa)
    if 0.45 * d < t < 0.88 * d:
        ang = 0.5 * math.sin(t * 9)
        bx = cx + 120 * U * math.sin(t * 4.5); by = cy - 40 * U + 60 * U * math.cos(t * 3)
        brush(ctx, bx, by, -0.4 + ang * 0.3, 1.0)
        rnd = random.Random(int(t * 6))
        for i in range(10):
            circle(ctx, bx + rnd.uniform(-160, 160) * U, by + rnd.uniform(0, 120) * U, rnd.uniform(10, 26) * U, (0.8, 0.95, 1.0), 0.35)
    if t >= 0.85 * d:
        k = prog(t, 0.85 * d, 0.95 * d)
        glow(ctx, cx, cy, r * 1.4, GREEN, 0.4 * k)
        neon_text(ctx, "CLEAN!", cx, cy, 130 * U, GREEN, k, fill=0.3)

def sc_outro(ctx, t, d):
    neon_bg(ctx, t, tint=CYAN)
    cta(ctx, t, d, "CHECKED YOURS LATELY?", "SEND THIS TO AN AIR FRYER LOVER")

SHORT_SCENES = ["hook", "grease", "clean", "outro"]
SCENES = dict(hook=sc_hook, grease=sc_grease, clean=sc_clean, outro=sc_outro)

def thumbnail(c):
    vgrad(c, (0.10, 0.04, 0.22), (0.01, 0.02, 0.08))
    thumb_text(c, "LOOK ABOVE", "THE BASKET", "AIR FRYER")
