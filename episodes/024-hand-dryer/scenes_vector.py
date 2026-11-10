# Episode 024 (Short only) - "Hand dryer or paper towel: which is cleaner?" — realistic shaded illustrations (v3)
# Executed inside engine/render.py (helpers available). Vertical layout. Original vector illustration. All sizes in U.
# Facts: UConn (AEM 2018: hot-air dryers deposit restroom bacteria on hands, HEPA ~4x fewer), Leeds (J Hosp Infect 2014,
# funded by the European Tissue Symposium: ~27x more airborne germs near jet dryers), CDC (towel or dryer both OK; dry hands fully).
# v3 (Nazik 2026-11-10: « ça manque de dynamisme, musique trop lente, dessins plus réalistes ») : mains réalistes (dos de la main,
# ongles, articulations), appareils métallisés, carrelage brillant, bactéries d'aspect microscopique, zooms et coups de caméra.

SKIN = (0.80, 0.73, 0.70)   # désaturé : la finition ffmpeg (+75 % de saturation) le rend orangé sinon
GERMC = (0.35, 0.95, 0.45)

def lin(x0, y0, x1, y1, stops):
    g = cairo.LinearGradient(x0, y0, x1, y1)
    for o, c, al in stops: g.add_color_stop_rgba(o, c[0], c[1], c[2], al)
    return g

def label(ctx, s, x, y, size, col, a):
    if a <= 0: return
    font(ctx, size); e = ctx.text_extents(s)
    rrect(ctx, x - e.width / 2 - 30 * U, y - size * 0.75, e.width + 60 * U, size * 1.5, size * 0.5); rgba(ctx, (0.02, 0.02, 0.04), 0.80 * a); ctx.fill()
    text(ctx, s, x, y, size, col, a)

# ---------------------------------------------------------------- camera
def with_cam(fn, push=0.06, punch=0.08, cy=0.45):
    """Push-in lent + « coup de zoom » à l'entrée de la scène (dynamisme)."""
    def sc(ctx, t, d):
        z = (1 + push * clamp(t / max(d, 0.1))) * (1 + punch * math.exp(-t * 9))
        ctx.save(); ctx.translate(CX, H * cy); ctx.scale(z, z); ctx.translate(-CX, -H * cy)
        fn(ctx, t, d)
        ctx.restore()
    return sc

# ---------------------------------------------------------------- set
def restroom(ctx, t, counter_y=None):
    counter_y = counter_y or H * 0.84
    ctx.set_source(lin(0, 0, 0, counter_y, [(0, (0.20, 0.30, 0.33), 1), (1, (0.12, 0.19, 0.22), 1)])); ctx.paint()
    tw, th = 180 * U, 90 * U
    for r in range(int(counter_y / th) + 1):
        off = (tw / 2) if r % 2 else 0
        for c in range(-1, int(W / tw) + 2):
            x = c * tw + off; y = r * th
            rrect(ctx, x + 3 * U, y + 3 * U, tw - 6 * U, th - 6 * U, 10 * U)
            ctx.set_source(lin(0, y, 0, y + th, [(0, (0.44, 0.58, 0.62), 1), (0.5, (0.34, 0.48, 0.52), 1), (1, (0.28, 0.40, 0.44), 1)])); ctx.fill()
            rrect(ctx, x + 14 * U, y + 10 * U, tw * 0.5, 10 * U, 5 * U); rgba(ctx, WHITE, 0.10); ctx.fill()
    # light from the ceiling + vignette
    g = cairo.RadialGradient(W * 0.5, -H * 0.1, 0, W * 0.5, -H * 0.1, H * 0.9)
    g.add_color_stop_rgba(0, 1, 1, 0.95, 0.20); g.add_color_stop_rgba(1, 0, 0, 0, 0.35); ctx.set_source(g); ctx.rectangle(0, 0, W, counter_y); ctx.fill()
    # granite counter
    ctx.rectangle(0, counter_y, W, H - counter_y)
    ctx.set_source(lin(0, counter_y, 0, H, [(0, (0.24, 0.24, 0.27), 1), (0.04, (0.12, 0.12, 0.14), 1), (1, (0.04, 0.04, 0.05), 1)])); ctx.fill()
    ctx.rectangle(0, counter_y, W, 6 * U); rgba(ctx, WHITE, 0.25); ctx.fill()
    rnd = random.Random(4)
    for i in range(80):
        circle(ctx, rnd.random() * W, counter_y + rnd.random() * (H - counter_y), rnd.uniform(2, 5) * U, WHITE, 0.06)

def shadow(ctx, draw, dx, dy, a=0.35):
    for k, al in ((3, 0.25), (2, 0.35), (1, 0.4)):
        ctx.save(); ctx.translate(dx * k / 2, dy * k / 2); ctx.new_path(); draw(ctx); rgba(ctx, (0, 0, 0), a * al); ctx.fill(); ctx.restore()

# ---------------------------------------------------------------- microbes
def microbe(ctx, x, y, r, t, a=1.0, kind=0, ang=0.0):
    if a <= 0 or r <= 0: return
    glow(ctx, x, y, r * 2.6, GERMC, 0.22 * a)
    ctx.save(); ctx.translate(x, y); ctx.rotate(ang + 0.25 * math.sin(t * 2.2 + x * 0.01))
    def body_grad(cx, cy, rr):
        g = cairo.RadialGradient(cx - rr * 0.3, cy - rr * 0.3, rr * 0.1, cx, cy, rr * 1.2)
        g.add_color_stop_rgba(0, 0.70, 1.0, 0.75, 0.95 * a); g.add_color_stop_rgba(1, 0.10, 0.55, 0.30, 0.95 * a); return g
    if kind == 0:   # rod (bacillus) with a flagellum
        ctx.new_path()
        for k in range(16):
            px = 1.4 * r + k * r * 0.12; py = math.sin(k * 0.9 + t * 9) * r * 0.25
            (ctx.move_to if k == 0 else ctx.line_to)(px, py)
        ctx.set_line_width(max(1.0, r * 0.08)); rgba(ctx, (0.6, 1.0, 0.7), 0.8 * a); ctx.stroke()
        rrect(ctx, -1.4 * r, -0.55 * r, 2.8 * r, 1.1 * r, 0.55 * r); ctx.set_source(body_grad(0, 0, 1.4 * r)); ctx.fill()
        ctx.new_path(); ctx.move_to(-0.9 * r, 0)
        for k in range(1, 7): ctx.line_to(-0.9 * r + k * 0.3 * r, 0.15 * r * math.sin(k * 1.7))
        ctx.set_line_width(max(1.0, r * 0.12)); rgba(ctx, (0.05, 0.35, 0.15), 0.7 * a); ctx.stroke()
        rrect(ctx, -1.0 * r, -0.42 * r, 1.2 * r, 0.22 * r, 0.11 * r); rgba(ctx, WHITE, 0.55 * a); ctx.fill()
    else:           # cocci cluster
        for (dx, dy) in ((0, 0), (0.95, 0.15), (0.45, -0.8))[:2 + kind % 2]:
            cx, cy = dx * r, dy * r
            ctx.new_path(); ctx.arc(cx, cy, 0.62 * r, 0, 2 * math.pi); ctx.set_source(body_grad(cx, cy, 0.62 * r)); ctx.fill()
            circle(ctx, cx - 0.2 * r, cy - 0.22 * r, 0.15 * r, WHITE, 0.6 * a)
    ctx.restore()

def germ(ctx, x, y, r, t, a=1.0, col=None):   # compat: realistic microbe, kind chosen by position
    microbe(ctx, x, y, r * 1.15, t, a, int(abs(x * 7 + y * 3) / U) % 3, (x * 0.013) % 6.28)

# ---------------------------------------------------------------- hands
def hand(ctx, x, y, s, ang, a=1.0, wet=0.0, mirror=1, sleeve=(0.18, 0.32, 0.60)):
    """Back of a right hand (mirror=-1: left hand), fingers up, wrist at (x, y). Realistic shading, nails, knuckles."""
    if a <= 0: return
    S = U * s
    ctx.save(); ctx.translate(x, y); ctx.rotate(ang); ctx.scale(mirror * S, S)
    sk = SKIN; dark = mix(SKIN, (0.45, 0.25, 0.18), 0.35); light = mix(SKIN, WHITE, 0.22)
    def across(w0, w1):
        return lin(w0, 0, w1, 0, [(0, dark, a), (0.45, light, a), (1, mix(dark, (0, 0, 0), 0.1), a)])
    # forearm + sleeve
    ctx.move_to(-72, 0); ctx.line_to(72, 0); ctx.line_to(84, 300); ctx.line_to(-84, 300); ctx.close_path(); ctx.set_source(across(-84, 84)); ctx.fill()
    rrect(ctx, -100, 175, 200, 140, 26); ctx.set_source(lin(-100, 0, 100, 0, [(0, mix(sleeve, (0, 0, 0), 0.4), a), (0.45, mix(sleeve, WHITE, 0.15), a), (1, mix(sleeve, (0, 0, 0), 0.5), a)])); ctx.fill()
    ctx.move_to(-100, 190); ctx.line_to(100, 190); ctx.set_line_width(5); rgba(ctx, (0, 0, 0), 0.25 * a); ctx.stroke()
    def finger(bx, by, L, w, an, thumb=False):
        ctx.save(); ctx.translate(bx, by); ctx.rotate(an)
        ctx.new_path(); ctx.move_to(-w / 2, 30); ctx.line_to(-w * 0.46, -L + w * 0.46)
        ctx.arc(0, -L + w * 0.46, w * 0.46, math.pi, 2 * math.pi); ctx.line_to(w / 2, 30); ctx.close_path()
        ctx.set_source(across(-w / 2, w / 2)); ctx.fill()
        for f in ((0.40, 0.55), (0.68, 0.45)) if not thumb else ((0.5, 0.5),):
            ctx.new_path(); ctx.move_to(-w * f[1] * 0.6, -L * f[0]); ctx.curve_to(-w * 0.1, -L * f[0] - 6, w * 0.1, -L * f[0] - 6, w * f[1] * 0.6, -L * f[0])
            ctx.set_line_width(2.5); rgba(ctx, (0.45, 0.28, 0.22), 0.35 * a); ctx.stroke()
        ny = -L + w * 0.14; nh = L * 0.27
        rrect(ctx, -w * 0.31, ny, w * 0.62, nh, w * 0.28); ctx.set_source(lin(0, ny, 0, ny + nh, [(0, (0.98, 0.86, 0.84), a), (1, (0.90, 0.68, 0.66), a)])); ctx.fill()
        rrect(ctx, -w * 0.18, ny + 4, w * 0.12, nh * 0.6, w * 0.06); rgba(ctx, WHITE, 0.7 * a); ctx.fill()
        ctx.restore()
    finger(-88, -92, 150, 54, -0.70, True)                  # thumb
    for (bx, by, L, w, an) in ((-55, -192, 178, 46, -0.07), (-15, -204, 198, 48, -0.015), (25, -201, 184, 45, 0.045), (62, -188, 142, 39, 0.12)):
        finger(bx, by, L, w, an)
    # back of the hand
    def back(c):
        c.move_to(-75, 0); c.curve_to(-90, -25, -100, -45, -96, -75); c.curve_to(-92, -110, -88, -140, -80, -175)
        c.curve_to(-74, -200, -40, -216, 0, -216); c.curve_to(40, -216, 75, -208, 95, -190); c.curve_to(102, -140, 96, -60, 76, 0); c.close_path()
    ctx.new_path(); back(ctx)
    g = cairo.RadialGradient(-15, -120, 10, 0, -100, 200); g.add_color_stop_rgba(0, *light, a); g.add_color_stop_rgba(0.7, *sk, a); g.add_color_stop_rgba(1, *dark, a)
    ctx.set_source(g); ctx.fill()
    for kx, ky in ((-55, -196), (-15, -207), (25, -204), (62, -190)):           # knuckles
        ctx.save(); ctx.translate(kx, ky); ctx.scale(1, 0.6); circle(ctx, 0, 0, 18, WHITE, 0.16 * a); ctx.restore()
    for kx in (-50, -15, 22, 55):                                              # tendons
        ctx.move_to(kx, -180); ctx.curve_to(kx * 0.8, -120, kx * 0.4, -60, kx * 0.25, -10)
    ctx.set_line_width(5); rgba(ctx, WHITE, 0.06 * a); ctx.stroke()
    if wet > 0:
        rnd = random.Random(6)
        for i in range(10):
            dx, dy = rnd.uniform(-75, 75), rnd.uniform(-330, -30); r = rnd.uniform(9, 15)
            ctx.save(); ctx.translate(dx, dy); ctx.scale(0.8, 1); ctx.arc(0, 0, r, 0, 2 * math.pi); ctx.restore()
            rgba(ctx, (0.55, 0.80, 1.0), 0.45 * wet * a); ctx.fill()
            circle(ctx, dx - r * 0.3, dy - r * 0.35, r * 0.32, WHITE, 0.9 * wet * a)
    ctx.restore()

# ---------------------------------------------------------------- appliances
def hot_dryer(ctx, x, y, s, a=1.0):
    """Wall-mounted hot-air dryer (white enamel + chrome nozzle). Returns (nozzle tip), (side intake)."""
    S = U * s
    w, h = 440 * S, 330 * S
    body = lambda c: rrect(c, x - w / 2, y - h / 2, w, h, 90 * S)
    shadow(ctx, body, 14 * S, 22 * S, 0.5 * a)
    ctx.new_path(); body(ctx)
    ctx.set_source(lin(0, y - h / 2, 0, y + h / 2, [(0, (0.99, 0.99, 1.0), a), (0.55, (0.90, 0.91, 0.94), a), (1, (0.72, 0.74, 0.79), a)])); ctx.fill()
    ctx.new_path(); body(ctx); ctx.set_source(lin(x - w / 2, 0, x + w / 2, 0, [(0, (0, 0, 0), 0.18 * a), (0.25, (1, 1, 1), 0.0), (0.8, (1, 1, 1), 0.0), (1, (0, 0, 0), 0.22 * a)])); ctx.fill()
    rrect(ctx, x - w * 0.42, y - h * 0.44, w * 0.55, h * 0.10, h * 0.05); rgba(ctx, WHITE, 0.55 * a); ctx.fill()     # specular
    for k in range(6):                                                                                          # intake slots
        rrect(ctx, x - w * 0.40, y - h * 0.18 + k * 26 * S, w * 0.30, 12 * S, 6 * S)
        ctx.set_source(lin(0, 0, 0, 12 * S, [(0, (0.15, 0.16, 0.18), a), (1, (0.35, 0.36, 0.40), a)])); ctx.fill()
    rrect(ctx, x + w * 0.12, y - h * 0.05, w * 0.26, h * 0.20, 14 * S); rgba(ctx, (0.05, 0.06, 0.08), a); ctx.fill()     # sensor window
    circle(ctx, x + w * 0.31, y + h * 0.05, 7 * S, (1.0, 0.25, 0.2), a); glow(ctx, x + w * 0.31, y + h * 0.05, 30 * S, CORAL, 0.6 * a)
    for sx in (-1, 1): circle(ctx, x + sx * w * 0.42, y - h * 0.36, 7 * S, (0.6, 0.62, 0.66), a)
    # chrome nozzle
    ny0, ny1 = y + h / 2 - 10 * S, y + h / 2 + 95 * S
    ctx.move_to(x - 80 * S, ny0); ctx.line_to(x + 80 * S, ny0); ctx.line_to(x + 62 * S, ny1); ctx.line_to(x - 62 * S, ny1); ctx.close_path()
    ctx.set_source(lin(x - 80 * S, 0, x + 80 * S, 0, [(0, (0.35, 0.36, 0.40), a), (0.35, (0.95, 0.96, 0.98), a), (0.6, (0.60, 0.62, 0.66), a), (1, (0.30, 0.31, 0.34), a)])); ctx.fill()
    ctx.save(); ctx.translate(x, ny1); ctx.scale(1, 0.25); circle(ctx, 0, 0, 62 * S, (0.05, 0.05, 0.06), a); ctx.restore()
    return (x, ny1 + 6 * S), (x - w * 0.25, y)

def towel_box(ctx, x, y, s, a=1.0):
    S = U * s
    w, h = 320 * S, 400 * S
    body = lambda c: rrect(c, x - w / 2, y - h / 2, w, h, 40 * S)
    shadow(ctx, body, 12 * S, 20 * S, 0.5 * a)
    ctx.new_path(); body(ctx)
    ctx.set_source(lin(x - w / 2, 0, x + w / 2, 0, [(0, (0.80, 0.82, 0.86), a), (0.3, (1, 1, 1), a), (1, (0.70, 0.72, 0.77), a)])); ctx.fill()
    rrect(ctx, x - w * 0.38, y - h * 0.40, w * 0.76, h * 0.42, 24 * S); rgba(ctx, (0.10, 0.14, 0.18), 0.85 * a); ctx.fill()   # smoked window
    for k in range(3):                                                                                                 # paper stack
        rrect(ctx, x - w * 0.32, y - h * 0.10 - k * 22 * S, w * 0.64, 16 * S, 4 * S); rgba(ctx, (0.92, 0.88, 0.80), 0.55 * a); ctx.fill()
    rrect(ctx, x - w * 0.36, y - h * 0.38, w * 0.2, h * 0.36, 16 * S); rgba(ctx, WHITE, 0.10 * a); ctx.fill()
    rrect(ctx, x - w * 0.20, y + h * 0.16, w * 0.40, h * 0.10, 12 * S); rgba(ctx, (0.55, 0.57, 0.62), a); ctx.fill()     # lever
    py = y + h / 2 - 12 * S
    ctx.move_to(x - 95 * S, py); ctx.line_to(x + 95 * S, py); ctx.curve_to(x + 100 * S, py + 80 * S, x + 80 * S, py + 120 * S, x + 88 * S, py + 165 * S)
    ctx.curve_to(x + 30 * S, py + 178 * S, x - 30 * S, py + 152 * S, x - 92 * S, py + 170 * S); ctx.curve_to(x - 84 * S, py + 110 * S, x - 100 * S, py + 60 * S, x - 95 * S, py); ctx.close_path()
    ctx.set_source(lin(x - 95 * S, 0, x + 95 * S, 0, [(0, (0.85, 0.80, 0.70), a), (0.45, (0.99, 0.97, 0.92), a), (1, (0.80, 0.75, 0.64), a)])); ctx.fill()
    rnd = random.Random(1)
    for i in range(40): circle(ctx, x + rnd.uniform(-80, 80) * S, py + rnd.uniform(10, 150) * S, 2.5 * S, (0.7, 0.66, 0.58), 0.5 * a)

def air_stream(ctx, t, x, y0, y1, a=1.0, spread=120):
    for k in range(11):
        e = (t * 2.2 + k / 11) % 1.0
        yy = y0 + (y1 - y0) * e; xx = x + (k - 5) * spread / 5 * U * (0.3 + e)
        ctx.move_to(xx, yy); ctx.line_to(xx + (k - 5) * 5 * U, yy + 80 * U)
        ctx.set_line_width(6 * U); rgba(ctx, (0.88, 0.96, 1.0), 0.5 * a * (1 - e)); ctx.stroke()

def jet_dryer(ctx, x, y, s, a=1.0, hands_k=0.0, t=0.0):
    """Hands-in jet dryer seen from the front: the hands dip into the top slot; the front wall hides their lower part."""
    S = U * s
    w, h = 460 * S, 720 * S
    top = y - h / 2
    body = lambda c: rrect(c, x - w / 2, top, w, h, 70 * S)
    shadow(ctx, body, 14 * S, 24 * S, 0.5 * a)
    ctx.new_path(); body(ctx)
    ctx.set_source(lin(x - w / 2, 0, x + w / 2, 0, [(0, (0.42, 0.44, 0.48), a), (0.28, (0.90, 0.91, 0.94), a), (0.6, (0.68, 0.70, 0.74), a), (1, (0.32, 0.34, 0.38), a)])); ctx.fill()
    # slot interior (seen through the top opening)
    sx0, sx1, sy0, sy1 = x - w * 0.40, x + w * 0.40, top + 30 * S, top + 260 * S
    rrect(ctx, sx0, sy0, sx1 - sx0, sy1 - sy0, 40 * S); ctx.set_source(lin(0, sy0, 0, sy1, [(0, (0.02, 0.03, 0.05), a), (1, (0.10, 0.12, 0.16), a)])); ctx.fill()
    for sx in (sx0 + 20 * S, sx1 - 20 * S):
        ctx.move_to(sx, sy0 + 40 * S); ctx.line_to(sx, sy1 - 20 * S); ctx.set_line_width(8 * S); rgba(ctx, CYAN, 0.8 * a); ctx.stroke()
        glow(ctx, sx, (sy0 + sy1) / 2, 90 * S, CYAN, 0.35 * a)
    # hands going down into the slot (fingers down)
    if hands_k > 0:
        ctx.save(); ctx.rectangle(sx0, 0, sx1 - sx0, sy1 - 10 * S); ctx.clip()
        hy = sy0 - 330 * S + hands_k * 210 * S
        hand(ctx, x - 55 * S, hy, 0.95 * s, math.pi + 0.05, a, wet=0.9)
        hand(ctx, x + 55 * S, hy, 0.95 * s, math.pi - 0.05, a, wet=0.9, mirror=-1)
        ctx.restore()
    # front wall + logo-less badge + drip tray
    ctx.move_to(x - w / 2, sy0 + 120 * S); ctx.line_to(x + w / 2, sy0 + 120 * S); ctx.line_to(x + w / 2, top + h - 70 * S)
    ctx.arc(x + w / 2 - 70 * S, top + h - 70 * S, 70 * S, 0, math.pi / 2); ctx.line_to(x - w / 2 + 70 * S, top + h)
    ctx.arc(x - w / 2 + 70 * S, top + h - 70 * S, 70 * S, math.pi / 2, math.pi); ctx.close_path()
    ctx.set_source(lin(x - w / 2, 0, x + w / 2, 0, [(0, (0.48, 0.50, 0.54), a), (0.3, (0.96, 0.97, 0.99), a), (0.62, (0.74, 0.76, 0.80), a), (1, (0.36, 0.38, 0.42), a)])); ctx.fill()
    ctx.move_to(x - w / 2, sy0 + 120 * S); ctx.line_to(x + w / 2, sy0 + 120 * S); ctx.set_line_width(4 * S); rgba(ctx, WHITE, 0.7 * a); ctx.stroke()
    for k in range(5):
        rrect(ctx, x - w * 0.30, top + h - 170 * S + k * 24 * S, w * 0.60, 10 * S, 5 * S); rgba(ctx, (0.25, 0.26, 0.30), 0.8 * a); ctx.fill()
    return (x, sy0 + 100 * S), (sx0, sx1)

# ---------------------------------------------------------------- scenes
def dryer_closeup(ctx, t, scale=1.0, germ_a=1.0, dark=0.45, cx=None, top=None, gap=1000):
    """Dramatic close-up: big hot-air dryer above freshly washed (wet) hands, bacteria raining down."""
    cx = cx if cx is not None else CX
    top = top if top is not None else H * 0.30
    restroom(ctx, t)
    rgba(ctx, (0.0, 0.02, 0.03), dark); ctx.paint()
    (nx, ny), _ = hot_dryer(ctx, cx, top, 2.0 * scale)
    glow(ctx, nx, ny + 380 * U * scale, 700 * U * scale, GERMC, 0.20 * germ_a)
    air_stream(ctx, t, nx, ny, ny + 520 * U * scale, 1.0, spread=260)
    hy = ny + gap * U * scale
    hand(ctx, nx - 125 * U * scale, hy, 1.30 * scale, -0.10, 1.0, wet=0.9)
    hand(ctx, nx + 125 * U * scale, hy, 1.30 * scale, 0.10, 1.0, wet=0.9, mirror=-1)
    rnd = random.Random(21)
    for i in range(30):
        e = (t * 1.1 + rnd.random()) % 1.0
        microbe(ctx, nx + rnd.uniform(-330, 330) * U * scale * (0.4 + e), ny + 40 * U + e * (gap - 360) * U * scale, rnd.uniform(13, 22) * U * scale, t, germ_a * (0.6 + 0.4 * (1 - e)), i % 3, rnd.uniform(0, 6))
    for i in range(14):
        microbe(ctx, nx + rnd.uniform(-280, 280) * U * scale, hy - rnd.uniform(100, 400) * U * scale, rnd.uniform(10, 16) * U * scale, t, germ_a * 0.95, i % 3, rnd.uniform(0, 6))
    return nx, ny, hy

def _hook(ctx, t, d):
    dryer_closeup(ctx, t, 0.9, prog(t, 0, 0.3) * 0.6 + 0.4, top=H * 0.37, gap=820)

def _vs(ctx, t, d):
    restroom(ctx, t)
    k1 = prog(t, 0, 0.25); k2 = prog(t, 0.15, 0.4)
    (nx, ny), _ = hot_dryer(ctx, W * 0.29 - (1 - k1) * 300 * U, H * 0.38, 1.05)
    air_stream(ctx, t, nx, ny, ny + 260 * U, k1)
    towel_box(ctx, W * 0.76 + (1 - k2) * 300 * U, H * 0.37, 1.05)
    s = 1 + 0.08 * math.sin(t * 8)
    ctx.save(); ctx.translate(W * 0.53, H * 0.40); ctx.scale(s, s); label(ctx, "VS", 0, 0, 100 * U, GOLD, prog(t, 0.3, 0.5)); ctx.restore()
    text(ctx, "WHICH IS CLEANER?", CX, H * 0.62, 78 * U, WHITE, prog(t, 0.5, 0.8))

def _dryer(ctx, t, d):
    restroom(ctx, t)
    (nx, ny), (ix, iy) = hot_dryer(ctx, CX + 70 * U, H * 0.27, 1.4)
    rnd = random.Random(8)
    for i in range(18):                                  # bathroom air (with bacteria) pulled into the intake
        e = ((t * 0.7 + rnd.random()) % 1.0)
        sx, sy = rnd.uniform(-W * 0.05, W * 0.22), rnd.uniform(H * 0.12, H * 0.55)
        microbe(ctx, sx + (ix - sx) * e, sy + (iy - sy) * e, 13 * U, t, 0.9 * (1 - e * 0.7), i % 3, rnd.uniform(0, 6))
    air_stream(ctx, t, nx, ny, ny + 330 * U)
    hy = ny + 600 * U
    hand(ctx, nx - 85 * U, hy, 0.95, -0.10, 1.0)
    hand(ctx, nx + 85 * U, hy, 0.95, 0.10, 1.0, mirror=-1)
    k = prog(t, 0.2, d * 0.5); stuck = prog(t, d * 0.45, d * 0.85)
    for i in range(16):
        e = (t * 1.4 + rnd.random()) % 1.0
        microbe(ctx, nx + rnd.uniform(-160, 160) * U, ny + e * 340 * U, 13 * U, t, 0.9 * k, i % 3, rnd.uniform(0, 6))
    for i in range(12):
        microbe(ctx, nx + rnd.uniform(-190, 190) * U, hy - rnd.uniform(80, 330) * U, 11 * U, t, stuck, i % 3, rnd.uniform(0, 6))
    label(ctx, "BATHROOM AIR IN → ONTO YOUR HANDS", CX, H * 0.06, 50 * U, GERMC, prog(t, 0, 0.25))
    label(ctx, "UNIVERSITY OF CONNECTICUT, 2018", CX, H * 0.105, 36 * U, (0.9, 0.95, 1.0), prog(t, d * 0.3, d * 0.45))

def _jet(ctx, t, d):
    restroom(ctx, t)
    (sx, sy), (x0, x1) = jet_dryer(ctx, CX, H * 0.53, 1.12, 1.0, prog(t, 0, 0.6), t)
    rnd = random.Random(12)
    for i in range(70):                                  # droplets + bacteria sprayed out of the slot
        ph = rnd.random(); e = (t * 1.1 + ph) % 1.0
        side = -1 if i % 2 else 1
        an = rnd.uniform(-1.0, 0.3); sp = rnd.uniform(550, 1150) * U
        px = CX + side * (230 * U + math.cos(an) * sp * e); py = sy + math.sin(an) * sp * e + 520 * U * e * e
        al = clamp(1.3 - e)
        circle(ctx, px, py, 13 * U, (0.70, 0.90, 1.0), 0.7 * al); circle(ctx, px - 4 * U, py - 4 * U, 5 * U, WHITE, 0.8 * al)
        if i % 2 == 0: microbe(ctx, px, py, 13 * U, t, al, i % 3, ph * 6)
    k = prog(t, 0.1, d * 0.42)
    sc_ = 1 + 0.06 * math.sin(t * 8) + 0.25 * math.exp(-((t - d * 0.42) * 6) ** 2)
    ctx.save(); ctx.translate(CX, H * 0.10); ctx.scale(sc_, sc_)
    neon_text(ctx, f"{int(round(27 * k))}× MORE", 0, 0, 150 * U, GERMC, prog(t, 0.05, 0.25), CYAN, fill=0.35); ctx.restore()
    label(ctx, "AIRBORNE GERMS NEAR JET DRYERS", CX, H * 0.165, 46 * U, WHITE, prog(t, 0.2, 0.45))
    fk = prog(t, d * 0.60, d * 0.68)
    if fk:
        ctx.save(); ctx.translate(CX, H * 0.62); ctx.rotate(-0.08); ctx.scale(1 + 0.6 * (1 - fk), 1 + 0.6 * (1 - fk))
        font(ctx, 50 * U); w_ = ctx.text_extents("FUNDED BY THE PAPER INDUSTRY").width + 70 * U
        rrect(ctx, -w_ / 2, -52 * U, w_, 104 * U, 20 * U); rgba(ctx, (0, 0, 0), 0.65 * fk); ctx.fill()
        rrect(ctx, -w_ / 2, -52 * U, w_, 104 * U, 20 * U); ctx.set_line_width(8 * U); rgba(ctx, GOLD, fk); ctx.stroke()
        text(ctx, "FUNDED BY THE PAPER INDUSTRY", 0, 0, 50 * U, GOLD, fk); ctx.restore()
        label(ctx, "UNIVERSITY OF LEEDS, 2014", CX, H * 0.545, 38 * U, (0.9, 0.95, 1.0), fk)

def check(ctx, x, y, s, a, col=GREEN):
    if a <= 0: return
    glow(ctx, x, y, 110 * s * U, col, 0.4 * a)
    ctx.move_to(x - 40 * s * U, y); ctx.line_to(x - 10 * s * U, y + 32 * s * U); ctx.line_to(x + 48 * s * U, y - 36 * s * U)
    ctx.set_line_width(16 * s * U); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_join(cairo.LINE_JOIN_ROUND); rgba(ctx, col, a); ctx.stroke()

def _verdict(ctx, t, d):
    restroom(ctx, t)
    t2 = d * 0.42
    if t < t2:
        towel_box(ctx, W * 0.28, H * 0.36, 1.0)
        hot_dryer(ctx, W * 0.73, H * 0.34, 1.0)
        check(ctx, W * 0.28, H * 0.62, 1.4, prog(t, 0.2, 0.5)); check(ctx, W * 0.73, H * 0.62, 1.4, prog(t, 0.45, 0.75))
        label(ctx, "CDC: BOTH WORK", CX, H * 0.09, 72 * U, GREEN, prog(t, 0, 0.25))
    else:
        k = prog(t, t2, d * 0.92); wet = 1 - k
        hand(ctx, CX - 130 * U, H * 0.66, 1.25, -0.10, 1.0, wet=wet)
        hand(ctx, CX + 130 * U, H * 0.66, 1.25, 0.10, 1.0, wet=wet, mirror=-1)
        rnd = random.Random(3)
        for i in range(10):
            e = (t * 1.3 + rnd.random()) % 1.0
            px = CX + rnd.uniform(-260, 260) * U; py = H * 0.42 + e * H * 0.25
            circle(ctx, px, py, 11 * U, (0.70, 0.90, 1.0), 0.6 * wet); circle(ctx, px - 3 * U, py - 3 * U, 4 * U, WHITE, 0.7 * wet)
            if i % 2 == 0: microbe(ctx, px + 16 * U, py, 10 * U, t, 0.8 * wet, i % 3, e * 6)
        if k > 0.85: glow(ctx, CX, H * 0.48, 520 * U, GREEN, 0.3 * prog(t, d * 0.85, d * 0.95))
        label(ctx, "DRY THEM COMPLETELY", CX, H * 0.09, 68 * U, GOLD, prog(t, t2, t2 + 0.25))
        label(ctx, "WET HANDS SPREAD GERMS MORE EASILY", CX, H * 0.145, 42 * U, WHITE, prog(t, d * 0.62, d * 0.75))

def _outro(ctx, t, d):
    neon_bg(ctx, t, tint=CYAN)
    cta(ctx, t, d, "TEAM TOWEL OR TEAM DRYER?", "COMMENT BELOW")

sc_hook = with_cam(_hook, 0.05, 0.10, 0.40)
sc_vs = with_cam(_vs, 0.06, 0.08)
sc_dryer = with_cam(_dryer, 0.07, 0.08, 0.40)
sc_jet = with_cam(_jet, 0.06, 0.10)
sc_verdict = with_cam(_verdict, 0.05, 0.08)
sc_outro = _outro

SHORT_SCENES = ["hook", "vs", "dryer", "jet", "verdict", "outro"]
SCENES = dict(hook=sc_hook, vs=sc_vs, dryer=sc_dryer, jet=sc_jet, verdict=sc_verdict, outro=sc_outro)

def thumbnail(c):
    vgrad(c, (0.10, 0.20, 0.24), (0.02, 0.05, 0.07))
    thumb_text(c, "HAND DRYER", "OR PAPER TOWEL?", "SCIENCE")

def cover(ctx):
    """Poster cover (Nazik 2026-11-10: soignée, qui attrape l'œil, accroche intrigante, sans donner la réponse)."""
    nx, ny, hy = dryer_closeup(ctx, 0.6, 0.78, 1.0, 0.35, top=H * 0.415, gap=800)
    g = cairo.LinearGradient(0, 0, 0, H * 0.36); g.add_color_stop_rgba(0, 0, 0.02, 0.03, 0.92); g.add_color_stop_rgba(1, 0, 0.02, 0.03, 0)
    ctx.rectangle(0, 0, W, H * 0.36); ctx.set_source(g); ctx.fill()
    for dx, dy, col, a in ((9, 11, (0, 0, 0), 0.7), (0, 0, None, 1.0)):
        text(ctx, "IS YOUR DRYER", CX + dx * U, H * 0.085 + dy * U, 118 * U, col or WHITE, a)
        text(ctx, "BLOWING THIS", CX + dx * U, H * 0.16 + dy * U, 128 * U, col or GERMC, a)
        text(ctx, "ON YOU?", CX + dx * U, H * 0.235 + dy * U, 150 * U, col or GOLD, a)
    ctx.save(); ctx.translate(W * 0.82, H * 0.60); ctx.rotate(0.18)
    circle(ctx, 0, 0, 150 * U, CORAL, 1.0)
    ctx.new_path(); ctx.arc(0, 0, 150 * U, 0, 2 * math.pi); ctx.set_line_width(8 * U); rgba(ctx, WHITE, 0.9); ctx.stroke()
    text(ctx, "27×", 0, -25 * U, 110 * U, WHITE, 1.0); text(ctx, "MORE GERMS?", 0, 60 * U, 36 * U, WHITE, 1.0)
    ctx.restore()
    rrect(ctx, CX - 470 * U, H * 0.94 - 58 * U, 940 * U, 116 * U, 58 * U); rgba(ctx, (0.02, 0.03, 0.05), 0.88); ctx.fill()
    rrect(ctx, CX - 470 * U, H * 0.94 - 58 * U, 940 * U, 116 * U, 58 * U); ctx.set_line_width(6 * U); rgba(ctx, GOLD, 1); ctx.stroke()
    text(ctx, "TOWEL OR DRYER?", CX, H * 0.94, 66 * U, GOLD)
