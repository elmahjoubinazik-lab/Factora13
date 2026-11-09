# Episode 021 (Short only) - "Why you should never wash raw chicken" — sober NEON style
# Executed inside engine/render.py (helpers available). Vertical layout. Original vector animation. All sizes in U.
# Facts: USDA FSIS 2019 kitchen study (60 % of rinsers had bacteria in the sink), UK FSA (droplets ~50–70 cm),
# USDA/CDC: cook poultry to 165 °F (74 °C); vinegar / lemon do not make it safe.

RAW = (1.0, 0.62, 0.70)
COOKED = (0.95, 0.50, 0.16)
GERM = GREEN

def chicken(ctx, x, y, s, t, a=1.0, cook=0.0):
    """Whole chicken seen from the side (roast-chicken icon: dome body, tucked wing, drumsticks with bones).
    cook 0→1 turns it from raw pink to golden. (x, y) = centre of the body."""
    if a <= 0: return
    S = U * s
    col = mix(RAW, COOKED, cook); line = mix(PINK, GOLD, cook)
    glow(ctx, x, y, 430 * S, line, 0.30 * a)
    def ell(cx, cy, rx, ry, rot):
        def d(c):
            c.save(); c.translate(cx, cy); c.rotate(rot); c.scale(rx, ry); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
        return d
    def shape(draw, light=0.45, lw=5):
        ctx.new_path(); draw(ctx)
        g = cairo.RadialGradient(x - 90 * S, y - 90 * S, 20 * S, x, y, 360 * S)
        g.add_color_stop_rgba(0, *mix(col, WHITE, light), 0.97 * a); g.add_color_stop_rgba(1, *mix(col, (0.55, 0.12, 0.22), 0.25), 0.92 * a)
        ctx.set_source(g); ctx.fill()
        neon_path(ctx, draw, line, lw * S, a)
    def bone(cx, cy, rx, rot, sc=1.0):
        ex, ey = cx + math.cos(rot) * rx * 0.85, cy + math.sin(rot) * rx * 0.85
        bx, by = ex + math.cos(rot) * 85 * S * sc, ey + math.sin(rot) * 85 * S * sc
        ctx.move_to(ex, ey); ctx.line_to(bx, by); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.set_line_width(30 * S * sc); rgba(ctx, (0.98, 0.95, 0.90), a); ctx.stroke()
        px, py = -math.sin(rot), math.cos(rot)
        for sg in (-1, 1):
            circle(ctx, bx + px * sg * 18 * S * sc + math.cos(rot) * 8 * S, by + py * sg * 18 * S * sc + math.sin(rot) * 8 * S, 22 * S * sc, (0.98, 0.95, 0.90), a)
    ROT = -0.62
    # back drumstick (behind the body)
    bl = (x + 175 * S, y - 25 * S, 150 * S, 82 * S)
    bone(bl[0], bl[1], bl[2], ROT, 0.85); shape(ell(bl[0], bl[1], bl[2], bl[3], ROT), 0.3)
    # tail + body
    shape(ell(x - 255 * S, y - 45 * S, 75 * S, 55 * S, 0.5))
    shape(ell(x, y, 285 * S, 185 * S, 0.0))
    # skin texture + highlight
    rnd = random.Random(4)
    for i in range(45):
        ang = rnd.uniform(0, 2 * math.pi); rr = math.sqrt(rnd.random()) * 0.85
        circle(ctx, x + math.cos(ang) * rr * 270 * S, y + math.sin(ang) * rr * 170 * S, rnd.uniform(3, 6) * S, mix(col, WHITE, 0.6), 0.45 * a)
    ell(x - 90 * S, y - 105 * S, 110 * S, 32 * S, -0.25)(ctx); rgba(ctx, WHITE, 0.35 * a); ctx.fill()
    # tucked wing
    def wing(c):
        c.move_to(x - 175 * S, y + 5 * S)
        c.curve_to(x - 90 * S, y - 75 * S, x + 20 * S, y - 45 * S, x + 15 * S, y + 15 * S)
        c.curve_to(x - 40 * S, y + 70 * S, x - 130 * S, y + 65 * S, x - 175 * S, y + 5 * S); c.close_path()
    shape(wing, 0.6, 4)
    # front drumstick
    fl = (x + 120 * S, y + 75 * S, 165 * S, 92 * S)
    bone(fl[0], fl[1], fl[2], ROT); shape(ell(fl[0], fl[1], fl[2], fl[3], ROT), 0.55)

def faucet(ctx, x, y, a=1.0):
    """Neon tap coming from the right; spout opening at (x, y)."""
    neon_path(ctx, lambda c: (c.move_to(W + 40 * U, y - 110 * U), c.line_to(x + 120 * U, y - 110 * U),
                              c.curve_to(x + 30 * U, y - 110 * U, x, y - 80 * U, x, y)), CYAN, 9 * U, a)
    neon_path(ctx, lambda c: (c.move_to(W * 0.80, y - 110 * U), c.line_to(W * 0.80, y - 190 * U),
                              c.move_to(W * 0.80 - 70 * U, y - 190 * U), c.line_to(W * 0.80 + 70 * U, y - 190 * U)), CYAN, 8 * U, a)

def stream(ctx, t, x, y0, y1, a=1.0):
    for k, dx in enumerate((-14, 0, 14)):
        ctx.set_dash([60 * U, 40 * U], -t * 900 * U - k * 30 * U)
        ctx.move_to(x + dx * U, y0); ctx.line_to(x + dx * U, y1)
        ctx.set_line_width(10 * U); rgba(ctx, mix(CYAN, WHITE, 0.4), 0.55 * a); ctx.stroke()
    ctx.set_dash([])
    glow(ctx, x, y1, 90 * U, CYAN, 0.45 * a)

def germ(ctx, x, y, r, t, a=1.0, col=GERM):
    if a <= 0 or r <= 0: return
    glow(ctx, x, y, r * 3, col, 0.35 * a)
    ctx.set_line_width(max(1.0, r * 0.22)); rgba(ctx, col, a)
    for i in range(8):
        ang = i * math.pi / 4 + t * 1.5
        ctx.move_to(x + math.cos(ang) * r, y + math.sin(ang) * r); ctx.line_to(x + math.cos(ang) * r * 1.5, y + math.sin(ang) * r * 1.5); ctx.stroke()
    circle(ctx, x, y, r, col, 0.9 * a); circle(ctx, x - r * 0.3, y - r * 0.3, r * 0.3, WHITE, 0.6 * a)

def droplets(ctx, t, x0, y0, n=26, power=1.0, a=1.0, ground=None, seed=3):
    """Splash: droplets (each carrying a germ) thrown in arcs from the impact point; cycles every 1.1 s."""
    rnd = random.Random(seed)
    for i in range(n):
        ph = rnd.random(); ang = rnd.uniform(-math.pi * 0.95, -math.pi * 0.05)
        sp = rnd.uniform(450, 1050) * U * power; e = ((t * 0.9 + ph) % 1.0) * 1.1
        px = x0 + math.cos(ang) * sp * e; py = y0 + math.sin(ang) * sp * e + 1400 * U * e * e
        if ground is not None and py > ground: continue
        al = a * clamp(1.4 - e)
        circle(ctx, px, py, 16 * U, mix(CYAN, WHITE, 0.3), 0.55 * al)
        if i % 2 == 0: germ(ctx, px, py, 7 * U, t, al)

def sc_hook(ctx, t, d):
    neon_bg(ctx, t, tint=PINK)
    sp = H * 0.34; cy = H * 0.52; s = 1.2
    faucet(ctx, CX - 60 * U, sp)
    stream(ctx, t, CX - 60 * U, sp + 10 * U, cy - 175 * U * s)
    chicken(ctx, CX, cy, s, t)
    droplets(ctx, t + 0.6, CX - 60 * U, cy - 175 * U * s, 22, 0.8)

def counter_items(ctx, t, yc, k):
    """Cutting board (left), towel (right), salad bowl (right); turn green when hit."""
    # board
    bx = W * 0.15
    hit = clamp(k * 3)
    rrect(ctx, bx - 110 * U, yc - 40 * U, 220 * U, 40 * U, 14 * U); rgba(ctx, mix(GOLD, GERM, hit * 0.6), 0.35); ctx.fill()
    neon_path(ctx, lambda c: rrect(c, bx - 110 * U, yc - 40 * U, 220 * U, 40 * U, 14 * U), mix(GOLD, GERM, hit * 0.6), 4 * U)
    # towel
    tx = W * 0.86; hit2 = clamp(k * 3 - 1)
    neon_path(ctx, lambda c: rrect(c, tx - 70 * U, yc - 150 * U, 140 * U, 150 * U, 10 * U), mix(CYAN, GERM, hit2 * 0.6), 4 * U)
    for j in range(3):
        yy = yc - 120 * U + j * 40 * U
        ctx.move_to(tx - 60 * U, yy); ctx.line_to(tx + 60 * U, yy); ctx.set_line_width(5 * U); rgba(ctx, CYAN, 0.5); ctx.stroke()
    # salad bowl
    sx = W * 0.40; hit3 = clamp(k * 3 - 2)
    for j in range(5):
        circle(ctx, sx - 60 * U + j * 30 * U, yc - 70 * U - 12 * U * math.sin(j * 1.7), 32 * U, mix(GREEN, (0.4, 1.0, 0.4), 0.3), 0.75)
    neon_path(ctx, lambda c: (c.move_to(sx - 110 * U, yc - 70 * U), c.curve_to(sx - 100 * U, yc + 10 * U, sx + 100 * U, yc + 10 * U, sx + 110 * U, yc - 70 * U), c.close_path()), mix(CORAL, GERM, hit3 * 0.6), 4 * U)
    # germs sitting on the items
    for (gx, h) in ((bx, hit), (sx, hit3), (tx, hit2)):
        for m in range(3):
            germ(ctx, gx + (m - 1) * 45 * U, yc - (95 if gx == sx else (60 if gx == bx else 170)) * U - 10 * U * m, 9 * U, t, h)

def sc_splash(ctx, t, d):
    neon_bg(ctx, t, tint=CYAN)
    sp = H * 0.25; ground = H * 0.60
    cy = H * 0.43
    faucet(ctx, CX - 50 * U, sp)
    stream(ctx, t, CX - 50 * U, sp + 10 * U, cy - 180 * U)
    chicken(ctx, CX, cy, 0.95, t)
    droplets(ctx, t, CX - 50 * U, cy - 180 * U, 34, 1.15, 1.0, ground, seed=5)
    # counter
    neon_path(ctx, lambda c: (c.move_to(W * 0.04, ground), c.line_to(W * 0.96, ground)), WHITE, 3 * U, 0.6)
    k = prog(t, d * 0.45, d * 0.9)
    counter_items(ctx, t, ground, k)
    # "about 2 feet" measure
    ma = prog(t, d * 0.30, d * 0.42)
    if ma:
        yv = ground + 90 * U; x1 = CX + (W * 0.44) * ma
        neon_path(ctx, lambda c: (c.move_to(CX, yv), c.line_to(x1, yv), c.move_to(x1 - 30 * U, yv - 22 * U), c.line_to(x1, yv), c.line_to(x1 - 30 * U, yv + 22 * U),
                                  c.move_to(CX, yv - 30 * U), c.line_to(CX, yv + 30 * U)), GOLD, 5 * U, ma)
        neon_text(ctx, "ABOUT 2 FEET", CX + W * 0.22, yv + 70 * U, 58 * U, GOLD, ma, fill=0.2)
    neon_text(ctx, "IT SPREADS GERMS", CX, H * 0.085, 104 * U, GERM, prog(t, 0, 0.3), CYAN, fill=0.15)

def sink(ctx, x, y, t, a=1.0):
    neon_path(ctx, lambda c: (c.move_to(x - 380 * U, y - 170 * U), c.line_to(x + 380 * U, y - 170 * U),
                              c.line_to(x + 300 * U, y + 160 * U), c.line_to(x - 300 * U, y + 160 * U), c.close_path()), CYAN, 7 * U, a)
    neon_path(ctx, lambda c: c.arc(x, y + 110 * U, 26 * U, 0, 2 * math.pi), CYAN, 4 * U, 0.7 * a)
    neon_path(ctx, lambda c: (c.move_to(x + 150 * U, y - 170 * U), c.line_to(x + 150 * U, y - 240 * U),
                              c.curve_to(x + 150 * U, y - 290 * U, x + 40 * U, y - 290 * U, x + 30 * U, y - 230 * U)), CYAN, 7 * U, a)

def sc_study(ctx, t, d):
    neon_bg(ctx, t, tint=GERM)
    k = prog(t, 0.1, 1.4)
    n = int(round(60 * k))
    s = 1 + 0.04 * math.sin(t * 6)
    ctx.save(); ctx.translate(CX, H * 0.20); ctx.scale(s, s); ctx.translate(-CX, -H * 0.20)
    neon_text(ctx, f"{n}%", CX, H * 0.20, 330 * U, GOLD, prog(t, 0, 0.25), CORAL, fill=0.3)
    ctx.restore()
    neon_text(ctx, "HAD GERMS IN THEIR SINK", CX, H * 0.30, 66 * U, WHITE, prog(t, 0.6, 1.0))
    sy = H * 0.49
    sink(ctx, CX, sy, t, prog(t, 0.2, 0.6))
    rnd = random.Random(9)
    for i in range(14):
        gx = CX + rnd.uniform(-250, 250) * U + 18 * U * math.sin(t * 2 + i)
        gy = sy + rnd.uniform(-120, 120) * U + 14 * U * math.cos(t * 2.3 + i)
        germ(ctx, gx, gy, rnd.uniform(12, 22) * U, t, prog(t, 0.5 + i * 0.08, 0.8 + i * 0.08))
    neon_text(ctx, "USDA KITCHEN STUDY, 2019", CX, H * 0.62, 46 * U, CYAN, prog(t, 0.8, 1.2))

def lemon(ctx, x, y, a):
    ctx.save(); ctx.translate(x, y); ctx.scale(1.35, 1.0)
    g = cairo.RadialGradient(-20 * U, -20 * U, 10 * U, 0, 0, 110 * U); g.add_color_stop_rgba(0, 1, 0.98, 0.6, a); g.add_color_stop_rgba(1, 1, 0.85, 0.1, a)
    ctx.arc(0, 0, 95 * U, 0, 2 * math.pi); ctx.set_source(g); ctx.fill(); ctx.restore()
    neon_path(ctx, lambda c: (c.save(), c.translate(x, y), c.scale(1.35, 1.0), c.arc(0, 0, 95 * U, 0, 2 * math.pi), c.restore()), GOLD, 4 * U, a)

def bottle(ctx, x, y, a):
    def d(c):
        c.move_to(x - 25 * U, y - 160 * U); c.line_to(x - 25 * U, y - 100 * U); c.curve_to(x - 75 * U, y - 80 * U, x - 75 * U, y - 60 * U, x - 75 * U, y - 30 * U)
        c.line_to(x - 75 * U, y + 120 * U); c.line_to(x + 75 * U, y + 120 * U); c.line_to(x + 75 * U, y - 30 * U)
        c.curve_to(x + 75 * U, y - 60 * U, x + 75 * U, y - 80 * U, x + 25 * U, y - 100 * U); c.line_to(x + 25 * U, y - 160 * U); c.close_path()
    ctx.new_path(); d(ctx); rgba(ctx, (0.85, 0.75, 0.55), 0.35 * a); ctx.fill()
    neon_path(ctx, d, WHITE, 4 * U, a)
    neon_text(ctx, "VINEGAR", x, y + 200 * U, 60 * U, GOLD, a)

def cross(ctx, x, y, r, a):
    neon_path(ctx, lambda c: (c.move_to(x - r, y - r), c.line_to(x + r, y + r), c.move_to(x + r, y - r), c.line_to(x - r, y + r)), CORAL, 9 * U, a)

def sc_heat(ctx, t, d):
    neon_bg(ctx, t, tint=CORAL)
    t1 = d * 0.38                          # vinegar / lemon part, then heat
    if t < t1 + 0.3:
        fa = 1 - prog(t, t1, t1 + 0.3)
        bottle(ctx, W * 0.30, H * 0.36, fa * prog(t, 0, 0.3))
        lemon(ctx, W * 0.70, H * 0.38, fa * prog(t, 0.2, 0.5))
        neon_text(ctx, "LEMON", W * 0.70, H * 0.36 + 200 * U, 60 * U, GOLD, fa * prog(t, 0.2, 0.5))
        cross(ctx, W * 0.30, H * 0.36, 120 * U, fa * prog(t, 0.6, 0.8))
        cross(ctx, W * 0.70, H * 0.38, 120 * U, fa * prog(t, 0.8, 1.0))
        neon_text(ctx, "NOT SAFE", CX, H * 0.12, 120 * U, CORAL, fa * prog(t, 0.6, 0.9), fill=0.2)
    if t > t1:
        k = prog(t, t1 + 0.2, d * 0.85)
        ka = prog(t, t1, t1 + 0.3)
        temp = int(round(40 + 125 * k))
        chicken(ctx, CX, H * 0.47, 1.05, t, ka, cook=k)
        # thermometer stuck in the chicken
        tx, ty = CX - 40 * U, H * 0.47 - 120 * U
        dx, dy = tx - 110 * U, ty - 175 * U
        neon_path(ctx, lambda c: (c.move_to(tx, ty), c.line_to(dx, dy)), WHITE, 6 * U, ka)
        circle(ctx, dx, dy - 40 * U, 60 * U, NAVY, 0.9 * ka)
        neon_path(ctx, lambda c: c.arc(dx, dy - 40 * U, 60 * U, 0, 2 * math.pi), WHITE, 4 * U, ka)
        ang = -math.pi * 0.8 + k * math.pi * 1.4
        neon_path(ctx, lambda c: (c.move_to(dx, dy - 40 * U), c.line_to(dx + math.cos(ang) * 45 * U, dy - 40 * U + math.sin(ang) * 45 * U)), CORAL, 4 * U, ka)
        # germs pop as the temperature rises
        rnd = random.Random(12)
        for i in range(10):
            gx = CX + rnd.uniform(-220, 200) * U; gy = H * 0.49 + rnd.uniform(-110, 130) * U
            kill = clamp(k * 1.6 - i * 0.06)
            germ(ctx, gx, gy, 16 * U * (1 - kill), t, ka * (1 - kill))
            if 0.05 < kill < 0.6: glow(ctx, gx, gy, 60 * U, GOLD, 0.5 * (0.6 - kill) * ka)
        s = 1 + (0.25 * (1 - prog(t, d * 0.85, d * 0.95)) if k >= 1 else 0)
        col = mix(CYAN, GOLD, k)
        ctx.save(); ctx.translate(CX, H * 0.15); ctx.scale(s, s); ctx.translate(-CX, -H * 0.15)
        neon_text(ctx, f"{temp}°F", CX, H * 0.15, 250 * U, col, ka, CORAL, fill=0.3)
        ctx.restore()
        neon_text(ctx, "74°C  ·  INSIDE THE MEAT", CX, H * 0.225, 46 * U, WHITE, prog(t, d * 0.85, d * 0.95))

def sc_outro(ctx, t, d):
    neon_bg(ctx, t, tint=GOLD)
    cta(ctx, t, d, "DO YOU WASH YOURS?", "SEND THIS TO SOMEONE WHO WASHES CHICKEN")

SHORT_SCENES = ["hook", "splash", "study", "heat", "outro"]
SCENES = dict(hook=sc_hook, splash=sc_splash, study=sc_study, heat=sc_heat, outro=sc_outro)

def thumbnail(c):
    vgrad(c, (0.10, 0.04, 0.22), (0.01, 0.02, 0.08))
    thumb_text(c, "STOP WASHING", "RAW CHICKEN", "FOOD SAFETY")
