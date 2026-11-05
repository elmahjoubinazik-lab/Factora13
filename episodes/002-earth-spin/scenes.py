# Scenes for "What if the Earth stopped spinning?"
# Executed inside engine/render.py: all helpers (W, H, U, CX, CY, VERT, colors, vgrad, circle, glow,
# text, rrect, stars, moon, earth, sun, chip, prog, ease, mix...) are available.

_text0 = text
def text(ctx, *a, **k):
    r = _text0(ctx, *a, **k); ctx.new_path(); return r

LAND = (0.30, 0.64, 0.40)
SAND = (0.78, 0.66, 0.42)
CONTS = [(0.0, 0.35, 0.45, 0.32), (0.9, -0.25, 0.32, 0.48), (2.1, 0.45, 0.55, 0.28),
         (3.2, -0.35, 0.38, 0.30), (4.3, 0.15, 0.48, 0.42), (5.3, 0.62, 0.30, 0.18), (1.6, -0.75, 0.5, 0.12)]

def fit(ctx, s, x, y, size, c=WHITE, a=1.0, bold=True, align="c", maxw=None):
    maxw = maxw or W * 0.9
    font(ctx, size, bold); w = ctx.text_extents(s).width
    if w > maxw: size *= maxw / w
    return text(ctx, s, x, y, size, c, a, bold, align)

def globe(ctx, x, y, r, rot, a=1.0, halo=True):
    """Spinning globe: continents slide across the disc (orthographic projection, vertical axis)."""
    if halo: glow(ctx, x, y, r * 1.35, (0.4, 0.7, 1.0), 0.35 * a)
    circle(ctx, x, y, r, SEA, a)
    ctx.save(); ctx.arc(x, y, r, 0, 2 * math.pi); ctx.clip()
    for lon, lat, w, h in CONTS:
        lam = lon + rot
        cl = math.cos(lam)
        if cl < -0.05: continue
        px = x + r * math.cos(lat) * math.sin(lam); py = y - r * math.sin(lat)
        ctx.save(); ctx.translate(px, py); ctx.scale(max(cl, 0.06) * w * r, h * r)
        ctx.arc(0, 0, 1, 0, 2 * math.pi); ctx.restore(); rgba(ctx, LAND, a); ctx.fill()
    # shading
    g = cairo.RadialGradient(x - r * 0.35, y - r * 0.35, r * 0.1, x, y, r * 1.05)
    g.add_color_stop_rgba(0, 1, 1, 1, 0.12 * a); g.add_color_stop_rgba(0.7, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0, 0, 0.05, 0.45 * a)
    ctx.set_source(g); ctx.paint()
    ctx.restore()

def spin_arrows(ctx, x, y, r, a=1.0, ph=0.0):
    """Gold arrows circling the equator (rotation towards the east)."""
    if a <= 0.01: return
    ctx.set_line_width(6 * U); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    for k in range(2):
        a0 = ph + k * math.pi
        ctx.save(); ctx.translate(x, y); ctx.scale(r * 1.28, r * 0.26)
        ctx.arc(0, 0, 1, a0, a0 + 1.6); ctx.restore()
        rgba(ctx, GOLD, a); ctx.stroke()
        e = a0 + 1.6
        hx, hy = x + r * 1.28 * math.cos(e), y + r * 0.26 * math.sin(e)
        tx, ty = -r * 1.28 * math.sin(e), r * 0.26 * math.cos(e)
        n = math.hypot(tx, ty); tx, ty = tx / n, ty / n
        ctx.move_to(hx + tx * 26 * U, hy + ty * 26 * U)
        ctx.line_to(hx - ty * 16 * U, hy + tx * 16 * U); ctx.line_to(hx + ty * 16 * U, hy - tx * 16 * U); ctx.close_path()
        rgba(ctx, GOLD, a); ctx.fill()

def rot_at(t, ts, D, w=1.0):
    """Rotation angle of a globe spinning at w rad/s that brakes to a stop between ts and ts + D."""
    if t < ts: return w * t
    u = min(t - ts, D)
    return w * (ts + u - u * u / (2 * D))

def sc_hook(ctx, t, d):
    vgrad(ctx, NAVY2, NAVY); stars(ctx, t, 0.8)
    ts = d * 0.62
    gx, gy, R = (CX, CY - 30 * U, 270 * U) if not VERT else (CX, CY - 250 * U, 300 * U)
    rot = rot_at(t, ts, 1.6, 1.3)
    spd = 1 - prog(t, ts, ts + 1.6)
    globe(ctx, gx, gy, R, rot)
    spin_arrows(ctx, gx, gy, R, 0.9 * spd, rot * 0.6)
    # traveller pin on the equator, front side
    lam = 0.0 + rot * 0.0
    circle(ctx, gx, gy, 14 * U, GOLD, 1); glow(ctx, gx, gy, 50 * U, GOLD, 0.5)
    a1 = prog(t, 0.5, 1.2) * (1 - prog(t, ts - 0.3, ts))
    if a1: fit(ctx, "UP TO 1,000 MPH", gx, gy - R - 70 * U, 64 * U, GOLD, a1)
    a2 = prog(t, ts + 0.6, ts + 1.4)
    if a2:
        fit(ctx, "WHAT IF IT STOPPED?", gx, gy - R - 70 * U, 70 * U, WHITE, a2)

def sc_speed(ctx, t, d):
    vgrad(ctx, NAVY2, NAVY); stars(ctx, t, 0.5)
    if VERT: gx, gy, R = CX, 560 * U, 240 * U
    else: gx, gy, R = W * 0.3, CY - 50 * U, 250 * U
    rot = t * 0.9
    globe(ctx, gx, gy, R, rot)
    # equator highlighted
    ctx.save(); ctx.arc(gx, gy, R, 0, 2 * math.pi); ctx.clip()
    ctx.save(); ctx.translate(gx, gy); ctx.scale(R, R * 0.12); ctx.arc(0, 0, 1, 0, math.pi); ctx.restore()
    rgba(ctx, GOLD, 0.9); ctx.set_line_width(5 * U); ctx.stroke(); ctx.restore()
    # a point on the equator sliding east
    lam = (t * 0.9) % (2 * math.pi) - math.pi
    if math.cos(lam) > 0:
        px = gx + R * math.sin(lam); py = gy + R * 0.12 * math.cos(lam)
        glow(ctx, px, py, 40 * U, GOLD, 0.6); circle(ctx, px, py, 11 * U, GOLD)
    spin_arrows(ctx, gx, gy, R, 0.8, t * 0.5)
    n = int(1670 * prog(t, 0.8, 3.5))
    if VERT: tx, ty = CX, 1000 * U
    else: tx, ty = W * 0.72, CY - 150 * U
    if n:
        fit(ctx, f"{n:,} km/h", tx, ty, 120 * U, GOLD, 1, maxw=W * 0.46 if not VERT else W * 0.9)
    a = prog(t, 3.5, 4.2)
    if a: text(ctx, "≈ 1,000 mph at the equator", tx, ty + 110 * U, 44 * U, WHITE, a, False)
    a = prog(t, 0.2, 0.8)
    # 24 h clock badge
    cx2, cy2 = (tx, ty - 230 * U)
    ctx.arc(cx2, cy2, 62 * U, 0, 2 * math.pi); rgba(ctx, NAVY2, a); ctx.fill_preserve()
    rgba(ctx, GOLD, a); ctx.set_line_width(5 * U); ctx.stroke()
    ang = t * 1.5
    ctx.move_to(cx2, cy2); ctx.line_to(cx2 + 44 * U * math.sin(ang), cy2 - 44 * U * math.cos(ang))
    ctx.move_to(cx2, cy2); ctx.line_to(cx2 + 28 * U * math.sin(ang / 12), cy2 - 28 * U * math.cos(ang / 12))
    rgba(ctx, WHITE, a); ctx.set_line_width(6 * U); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    text(ctx, "1 TURN ≈ 24 h", cx2 + (150 * U if not VERT else 0), cy2 + (0 if not VERT else 100 * U), 40 * U, WHITE, a, True, "l" if not VERT else "c")

def car(ctx, x, y, s, c):
    rrect(ctx, x - 70 * s, y - 55 * s, 140 * s, 38 * s, 12 * s); rgba(ctx, c); ctx.fill()
    rrect(ctx, x - 40 * s, y - 85 * s, 75 * s, 34 * s, 12 * s); rgba(ctx, c); ctx.fill()
    rrect(ctx, x - 32 * s, y - 79 * s, 28 * s, 22 * s, 5 * s); rgba(ctx, (0.75, 0.88, 1.0), 0.8); ctx.fill()
    rrect(ctx, x + 2 * s, y - 79 * s, 26 * s, 22 * s, 5 * s); rgba(ctx, (0.75, 0.88, 1.0), 0.8); ctx.fill()
    for wx in (-40, 40):
        circle(ctx, x + wx * s, y - 16 * s, 17 * s, (0.1, 0.1, 0.14)); circle(ctx, x + wx * s, y - 16 * s, 7 * s, (0.7, 0.7, 0.75))

def person(ctx, x, y, s, c, sw=0.0):
    circle(ctx, x, y - 100 * s, 15 * s, c)
    ctx.set_line_width(10 * s); ctx.set_line_cap(cairo.LINE_CAP_ROUND); rgba(ctx, c)
    ctx.move_to(x, y - 82 * s); ctx.line_to(x, y - 42 * s)
    ctx.move_to(x, y - 42 * s); ctx.line_to(x - 18 * s - sw, y)
    ctx.move_to(x, y - 42 * s); ctx.line_to(x + 18 * s + sw, y)
    ctx.move_to(x, y - 72 * s); ctx.line_to(x + 30 * s, y - 88 * s - sw)
    ctx.move_to(x, y - 72 * s); ctx.line_to(x - 30 * s, y - 60 * s + sw)
    ctx.stroke()

def rock(ctx, x, y, s, c):
    pts = [(-40, 0), (-30, -35), (0, -50), (32, -38), (42, -5), (20, 8), (-20, 8)]
    for i, (px, py) in enumerate(pts): (ctx.line_to if i else ctx.move_to)(x + px * s, y + py * s)
    ctx.close_path(); rgba(ctx, c); ctx.fill()

def tree(ctx, x, y, s):
    rgba(ctx, (0.35, 0.24, 0.15)); ctx.rectangle(x - 10 * s, y - 90 * s, 20 * s, 90 * s); ctx.fill()
    circle(ctx, x, y - 130 * s, 60 * s, (0.16, 0.42, 0.26)); circle(ctx, x - 40 * s, y - 100 * s, 40 * s, (0.16, 0.42, 0.26))
    circle(ctx, x + 40 * s, y - 100 * s, 40 * s, (0.16, 0.42, 0.26))

def speedlines(ctx, x, y, s, ln, a):
    ctx.set_line_width(5 * s); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    for k, dy in enumerate((-70, -40, -10)):
        ctx.move_to(x - 90 * s - k * 20 * s, y + dy * s); ctx.line_to(x - 90 * s - ln - k * 20 * s, y + dy * s)
    rgba(ctx, WHITE, a); ctx.stroke()

def sc_stop(ctx, t, d):
    vgrad(ctx, (0.10, 0.16, 0.34), (0.30, 0.36, 0.55))
    stars(ctx, t, 0.25)
    gy = H * 0.68 if not VERT else H * 0.62
    rgba(ctx, (0.20, 0.30, 0.22)); ctx.rectangle(0, gy, W, H - gy); ctx.fill()
    rgba(ctx, (0.27, 0.40, 0.28)); ctx.rectangle(0, gy, W, 14 * U); ctx.fill()
    ts = 2.2
    s = 1.0 * U if not VERT else 0.95 * U
    # anchored things (stay put)
    tree(ctx, W * 0.12, gy, s * 1.1)
    hx = W * 0.30 if not VERT else W * 0.70
    rgba(ctx, (0.55, 0.42, 0.36)); ctx.rectangle(hx - 70 * s, gy - 110 * s, 140 * s, 110 * s); ctx.fill()
    rgba(ctx, CORAL); ctx.move_to(hx - 90 * s, gy - 110 * s); ctx.line_to(hx, gy - 180 * s); ctx.line_to(hx + 90 * s, gy - 110 * s); ctx.close_path(); ctx.fill()
    rgba(ctx, (0.25, 0.18, 0.15)); ctx.rectangle(hx - 18 * s, gy - 60 * s, 36 * s, 60 * s); ctx.fill()
    # loose things
    go = max(0.0, t - ts)
    items = [("car", 0.48, 1.0), ("person", 0.62, 1.25), ("rock", 0.74, 0.9), ("person", 0.86, 1.1), ("rock", 0.40, 1.15)]
    if VERT: items = [("car", 0.30, 1.0), ("person", 0.50, 1.25), ("rock", 0.85, 0.9), ("person", 0.12, 1.1)]
    for i, (kind, fx, v) in enumerate(items):
        dx = (go * go * 140 + go * 420) * v * U
        span = W + 500 * U
        x = (W * fx + dx) % span - 250 * U if go > 0 else W * fx
        lift = (18 * U * abs(math.sin(go * 3 + i))) if go > 0 else 0
        y = gy - lift - (40 * U if VERT and kind != "car" else 0) * 0
        ctx.save()
        if go > 0:
            speedlines(ctx, x, y, s, (60 + 120 * min(go, 1.5)) * U, 0.7)
            ctx.translate(x, y - 40 * s); ctx.rotate(0.25 * math.sin(go * 4 + i) * (kind != "car")); ctx.translate(-x, -(y - 40 * s))
        if kind == "car": car(ctx, x, y, s, (0.95, 0.75, 0.3))
        elif kind == "person": person(ctx, x, y, s, WHITE, 12 * s * math.sin(t * 8 + i) if go > 0 else 0)
        else: rock(ctx, x, y, s, (0.55, 0.52, 0.5))
        ctx.restore()
    # stop flash
    f = prog(t, ts - 0.3, ts) * (1 - prog(t, ts + 0.6, ts + 1.4))
    if f:
        rgba(ctx, WHITE, 0.35 * f); ctx.paint()
    a = prog(t, ts + 0.5, ts + 1.2)
    ty = H * 0.25 if not VERT else H * 0.20
    fit(ctx, "THE GROUND STOPS…", CX, ty, 64 * U, WHITE, prog(t, 0.6, 1.2) * (1 - a))
    if a:
        fit(ctx, "…EVERYTHING ELSE KEEPS GOING EAST", CX, ty, 56 * U, GOLD, a)
        ax = CX; ay = ty + 90 * U
        ctx.move_to(ax - 120 * U, ay); ctx.line_to(ax + 100 * U, ay); rgba(ctx, GOLD, a); ctx.set_line_width(8 * U); ctx.stroke()
        ctx.move_to(ax + 130 * U, ay); ctx.line_to(ax + 90 * U, ay - 26 * U); ctx.line_to(ax + 90 * U, ay + 26 * U); ctx.close_path(); ctx.fill()
    chip(ctx, "1 · THE SUDDEN STOP", t)

def spiral(ctx, x, y, r, ph, a):
    ctx.set_line_width(7 * U); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    for arm in range(3):
        for i in range(60):
            u = i / 59
            ang = ph + arm * 2.094 + u * 4.0
            rr = r * (0.12 + 0.88 * u)
            (ctx.line_to if i else ctx.move_to)(x + rr * math.cos(ang), y + rr * 0.55 * math.sin(ang))
        rgba(ctx, WHITE, a * 0.75); ctx.stroke()
    circle(ctx, x, y, r * 0.1, (0.1, 0.14, 0.3), a)

def sc_winds(ctx, t, d):
    vgrad(ctx, NAVY2, NAVY); stars(ctx, t, 0.4)
    # curved planet surface
    pr = W * 1.6
    pcx, pcy = CX, (H * 0.62 if not VERT else H * 0.60) + pr
    glow(ctx, pcx, pcy, pr * 1.04, (0.4, 0.7, 1.0), 0.5)
    circle(ctx, pcx, pcy, pr, SEA_D)
    ctx.save(); ctx.arc(pcx, pcy, pr, 0, 2 * math.pi); ctx.clip()
    rgba(ctx, LAND, 0.8)
    for i in range(5):
        x = (W * (i * 0.27) - t * 30 * U) % (W * 1.35) - W * 0.15
        ctx.save(); ctx.translate(x, pcy - pr + 140 * U); ctx.scale(170 * U, 60 * U); ctx.arc(0, 0, 1, 0, 6.3); ctx.restore(); ctx.fill()
    ctx.restore()
    # storms over the surface
    sy = (H * 0.62 if not VERT else H * 0.60) - 40 * U
    xs = (0.22, 0.55, 0.85) if not VERT else (0.28, 0.75)
    for i, fx in enumerate(xs):
        spiral(ctx, W * fx, sy - (i % 2) * 50 * U, (120 + 30 * (i % 2)) * U, -t * 2.5 - i, prog(t, 1 + i * 0.5, 2 + i * 0.5))
    # wind streaks
    random.seed(4)
    for j in range(45):
        yy = random.uniform(0.32, 0.58) * H if not VERT else random.uniform(0.40, 0.58) * H
        v = random.uniform(900, 1600) * U; ln = random.uniform(80, 220) * U
        x = (random.random() * W + t * v) % (W + 400 * U) - 200 * U
        ctx.move_to(x, yy); ctx.line_to(x - ln, yy)
        rgba(ctx, (0.8, 0.9, 1.0), 0.35); ctx.set_line_width(3 * U); ctx.stroke()
    # comparison bars
    bx = W * 0.08; bw = W * 0.84
    by = H * 0.20 if not VERT else H * 0.17
    gap = 105 * U
    a = prog(t, 2.5, 3.2)
    if a:
        p1 = prog(t, 2.8, 4.0); p2 = prog(t, 4.0, 6.5)
        fit(ctx, "STRONGEST HURRICANE ON RECORD", bx, by - 6 * U, 34 * U, WHITE, a, True, "l", bw)
        rrect(ctx, bx, by + 22 * U, bw * 0.2 * p1 + 1, 30 * U, 15 * U); rgba(ctx, CORAL, a); ctx.fill()
        fit(ctx, "WINDS AFTER THE STOP (EQUATOR)", bx, by + gap - 6 * U, 34 * U, GOLD, a, True, "l", bw)
        rrect(ctx, bx, by + gap + 22 * U, bw * 0.95 * p2 + 1, 30 * U, 15 * U); rgba(ctx, GOLD, a); ctx.fill()
    chip(ctx, "2 · HURRICANE-FORCE WINDS", t)

def sc_oceans(ctx, t, d):
    vgrad(ctx, NAVY2, NAVY); stars(ctx, t, 0.6)
    gx, gy, R = (CX, CY - 50 * U, 250 * U) if not VERT else (CX, 820 * U, 290 * U)
    k = prog(t, d * 0.35, d * 0.75)
    glow(ctx, gx, gy, R * 1.4, (0.4, 0.7, 1.0), 0.3)
    # water envelope: bulge at the equator → bulges at the poles
    rx = R * (1.07 - 0.09 * k); ry = R * (0.97 + 0.13 * k)
    ctx.save(); ctx.translate(gx, gy); ctx.scale(rx, ry); ctx.arc(0, 0, 1, 0, 2 * math.pi); ctx.restore()
    rgba(ctx, (0.35, 0.68, 1.0), 0.75); ctx.fill()
    globe(ctx, gx, gy, R, 0.6, 1, halo=False)
    # equatorial continent emerging
    if k > 0:
        ctx.save(); ctx.arc(gx, gy, R, 0, 2 * math.pi); ctx.clip()
        hh = R * 0.62 * k
        ctx.move_to(gx - R, gy - hh)
        for i in range(25): ctx.line_to(gx - R + 2 * R * i / 24, gy - hh - 12 * U * math.sin(i * 1.3) * k)
        ctx.line_to(gx + R, gy + hh)
        for i in range(25): ctx.line_to(gx + R - 2 * R * i / 24, gy + hh + 12 * U * math.sin(i * 1.1 + 1) * k)
        ctx.close_path(); rgba(ctx, mix(LAND, SAND, 0.45)); ctx.fill()
        ctx.restore()
        text(ctx, "ONE GIANT", gx, gy - 24 * U, 40 * U, NAVY, k)
        text(ctx, "CONTINENT", gx, gy + 26 * U, 40 * U, NAVY, k)
    a0 = prog(t, 0.5, 1.2) * (1 - prog(t, d * 0.3, d * 0.38))
    if a0:
        text(ctx, "TODAY: THE OCEANS BULGE", gx, gy - R - 70 * U, 46 * U, WHITE, a0)
        text(ctx, "AT THE EQUATOR", gx, gy + R + 60 * U, 46 * U, WHITE, a0)
        for sgn in (-1, 1):
            ax = gx + sgn * (rx + 30 * U)
            ctx.move_to(ax, gy); ctx.line_to(ax - sgn * 30 * U, gy - 20 * U); ctx.line_to(ax - sgn * 30 * U, gy + 20 * U); ctx.close_path()
            rgba(ctx, GOLD, a0); ctx.fill()
    if k > 0.3:
        b = prog(k, 0.3, 0.8)
        text(ctx, "POLAR OCEAN", gx, gy - ry - 50 * U, 46 * U, GOLD, b)
        text(ctx, "POLAR OCEAN", gx, gy + ry + 50 * U, 46 * U, GOLD, b)
        lx = (W - 40 * U, H * 0.12) if not VERT else (CX, 1300 * U)
        if not VERT: text(ctx, "simplified simulation", W - 60 * U, 90 * U, 30 * U, WHITE, 0.7 * b, False, "r")
        else: text(ctx, "simplified simulation", CX, gy + ry + 115 * U, 30 * U, WHITE, 0.7 * b, False)
    chip(ctx, "3 · OCEANS ON THE MOVE", t)

def lit_globe(ctx, x, y, r, sun_ang, rot=0.6):
    globe(ctx, x, y, r, rot, 1, halo=False)
    ctx.save(); ctx.arc(x, y, r + 1, 0, 2 * math.pi); ctx.clip()
    ctx.translate(x, y); ctx.rotate(sun_ang)
    ctx.rectangle(-r - 2, -r - 2, r + 2, 2 * r + 4); rgba(ctx, (0.0, 0.0, 0.03), 0.72); ctx.fill()
    ctx.restore()

def sc_day(ctx, t, d):
    vgrad(ctx, NAVY2, NAVY); stars(ctx, t, 0.7)
    if VERT: ox, oy, rx, ry = CX, 830 * U, 400 * U, 230 * U
    else: ox, oy, rx, ry = CX, CY - 10 * U, 640 * U, 215 * U
    ctx.set_dash([12 * U, 12 * U]); ctx.save(); ctx.translate(ox, oy); ctx.scale(rx, ry); ctx.arc(0, 0, 1, 0, 2 * math.pi); ctx.restore()
    rgba(ctx, WHITE, 0.35); ctx.set_line_width(3 * U); ctx.stroke(); ctx.set_dash([])
    sun(ctx, ox, oy, 80 * U, t)
    th = math.pi + 2 * math.pi * prog(t, 1.0, d - 0.8)   # one orbit = one year
    ex, ey = ox + rx * math.cos(th), oy + ry * math.sin(th)
    sun_ang = math.atan2(oy - ey, ox - ex)
    r = 62 * U
    lit_globe(ctx, ex, ey, r, sun_ang)
    # a fixed spot on the planet (facing right, never turns)
    mx, my = ex + r * 0.75, ey
    is_day = math.cos(sun_ang) > 0
    circle(ctx, mx, my, 10 * U, GOLD); glow(ctx, mx, my, 30 * U, GOLD, 0.6)
    lab = "DAY" if is_day else "NIGHT"
    text(ctx, lab, ex, ey - r - 40 * U, 38 * U, GOLD if is_day else (0.6, 0.7, 1.0))
    month = 1 + int(12 * prog(t, 1.0, d - 0.8) * 0.999)
    ty = 95 * U if not VERT else 380 * U
    text(ctx, "1 DAY = 1 YEAR", CX, ty, 70 * U, WHITE, prog(t, 0.3, 1.0))
    by = oy + ry + 95 * U
    if not VERT:
        text(ctx, f"MONTH {month} / 12", W - 70 * U, 95 * U, 40 * U, GOLD, prog(t, 1.0, 1.5), True, "r")
        text(ctx, "≈ 6 months of daylight  ·  ≈ 6 months of night", CX, 165 * U, 36 * U, WHITE, prog(t, 4, 5), False)
    else:
        text(ctx, f"MONTH {month} / 12", CX, ty + 95 * U, 44 * U, GOLD, prog(t, 1.0, 1.5))
        text(ctx, "≈ 6 months of daylight", CX, by, 40 * U, WHITE, prog(t, 4, 5), False)
        text(ctx, "≈ 6 months of night", CX, by + 55 * U, 40 * U, WHITE, prog(t, 4, 5), False)
    chip(ctx, "4 · A YEAR-LONG DAY", t)

def field_lines(ctx, x, y, R, a, dash=False):
    ctx.set_line_width(4 * U)
    if dash: ctx.set_dash([10 * U, 14 * U])
    for L in (1.5, 2.1, 2.8):
        for sgn in (-1, 1):
            for i in range(80):
                th = 0.25 + (math.pi - 0.5) * i / 79
                r = L * R * math.sin(th) ** 2
                if r < R: r = R
                px, py = x + sgn * r * math.sin(th), y - r * math.cos(th)
                (ctx.line_to if i else ctx.move_to)(px, py)
            rgba(ctx, (0.55, 0.85, 1.0), a); ctx.stroke()
    ctx.set_dash([])

def sc_magnet(ctx, t, d):
    vgrad(ctx, NAVY2, NAVY); stars(ctx, t, 0.6)
    gx, gy, R = (CX + 60 * U, CY - 40 * U, 165 * U) if not VERT else (CX, 820 * U, 150 * U)
    weak = prog(t, d * 0.55, d * 0.72)
    field_lines(ctx, gx, gy, R, 0.85 * (1 - 0.75 * weak), weak > 0.5)
    # cross-section of the Earth
    circle(ctx, gx, gy, R, (0.40, 0.28, 0.22))
    circle(ctx, gx, gy, R * 0.92, (0.80, 0.38, 0.18))
    circle(ctx, gx, gy, R * 0.55, (1.0, 0.62, 0.22))
    ctx.set_line_width(4 * U); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    for i in range(5):
        a0 = t * 1.2 + i * 1.256
        ctx.arc(gx, gy, R * (0.38 + 0.03 * (i % 2)), a0, a0 + 0.8); rgba(ctx, (1, 0.9, 0.6), 0.9); ctx.stroke()
    glow(ctx, gx, gy, R * 0.5, GOLD, 0.6)
    circle(ctx, gx, gy, R * 0.22, GOLD)
    # solar wind
    random.seed(9)
    for j in range(40):
        yy = gy + random.uniform(-1, 1) * R * 2.2
        v = random.uniform(250, 420) * U
        x0 = -50 * U
        x = x0 + (random.random() * W * 0.6 + t * v) % (W * 0.55)
        stopx = gx - (2.6 * R) * (1 - weak) - R * weak
        if abs(yy - gy) > R * 1.4 * (1 - weak) + R * weak: stopx = W
        if x > stopx: continue
        ctx.move_to(x, yy); ctx.line_to(x - 40 * U, yy); rgba(ctx, GOLD, 0.8); ctx.set_line_width(4 * U); ctx.stroke()
    wx = W * 0.12 if not VERT else W * 0.2
    la = prog(t, 1, 1.6); ly = gy + R * (2.0 if not VERT else 2.6) + 10 * U
    rrect(ctx, wx + 40 * U - 140 * U, ly - 30 * U, 280 * U, 60 * U, 30 * U); rgba(ctx, NAVY, 0.9 * la); ctx.fill()
    text(ctx, "SOLAR WIND →", wx + 40 * U, ly, 34 * U, GOLD, la)
    ty = gy - R * 2.3 if not VERT else 380 * U
    text(ctx, "MAGNETIC SHIELD", CX, ty, 56 * U, WHITE, prog(t, 0.3, 1.0) * (1 - weak))
    if weak: text(ctx, "NO SPIN: IT COULD WEAKEN", CX, ty, 56 * U, CORAL, weak)
    lab_y = gy + R + 50 * U
    text(ctx, "liquid iron core", gx, gy, 28 * U, NAVY, prog(t, 2, 2.6) * (1 - weak), True)
    chip(ctx, "5 · A HIDDEN DANGER", t)

def clockface(ctx, x, y, r, t, a=1.0):
    ctx.arc(x, y, r, 0, 2 * math.pi); rgba(ctx, NAVY2, a); ctx.fill_preserve(); rgba(ctx, GOLD, a); ctx.set_line_width(7 * U); ctx.stroke()
    for i in range(12):
        an = i / 12 * 2 * math.pi
        ctx.move_to(x + 0.8 * r * math.sin(an), y - 0.8 * r * math.cos(an)); ctx.line_to(x + 0.92 * r * math.sin(an), y - 0.92 * r * math.cos(an))
    rgba(ctx, WHITE, a); ctx.set_line_width(5 * U); ctx.stroke()
    ang = t * 0.9
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.move_to(x, y); ctx.line_to(x + 0.7 * r * math.sin(ang), y - 0.7 * r * math.cos(ang)); ctx.set_line_width(7 * U); rgba(ctx, WHITE, a); ctx.stroke()
    ctx.move_to(x, y); ctx.line_to(x + 0.45 * r * math.sin(ang / 12 + 1), y - 0.45 * r * math.cos(ang / 12 + 1)); ctx.set_line_width(10 * U); ctx.stroke()
    circle(ctx, x, y, 10 * U, GOLD, a)
    text(ctx, "24 h", x, y + r * 0.45, r * 0.26, GOLD, a)

def dino(ctx, x, y, s, c, a=1.0):
    """Long-necked dinosaur silhouette (original flat drawing)."""
    rgba(ctx, c, a)
    ctx.save(); ctx.translate(x, y); ctx.scale(150 * s, 70 * s); ctx.arc(0, 0, 1, 0, 2 * math.pi); ctx.restore(); ctx.fill()
    ctx.move_to(x + 100 * s, y - 40 * s)
    ctx.curve_to(x + 170 * s, y - 120 * s, x + 180 * s, y - 230 * s, x + 230 * s, y - 250 * s)
    ctx.line_to(x + 270 * s, y - 238 * s); ctx.line_to(x + 238 * s, y - 215 * s)
    ctx.curve_to(x + 210 * s, y - 190 * s, x + 200 * s, y - 80 * s, x + 140 * s, y + 10 * s); ctx.close_path(); ctx.fill()
    circle(ctx, x + 245 * s, y - 238 * s, 26 * s, c, a)
    ctx.move_to(x - 120 * s, y - 30 * s)
    ctx.curve_to(x - 220 * s, y - 20 * s, x - 290 * s, y + 10 * s, x - 340 * s, y + 40 * s)
    ctx.curve_to(x - 280 * s, y + 30 * s, x - 200 * s, y + 40 * s, x - 120 * s, y + 35 * s); ctx.close_path(); ctx.fill()
    for lx in (-95, -45, 55, 105):
        rrect(ctx, x + lx * s - 18 * s, y + 20 * s, 36 * s, 95 * s, 12 * s); ctx.fill()

def sc_slowing(ctx, t, d):
    vgrad(ctx, NAVY2, NAVY); stars(ctx, t, 0.6)
    if VERT: ex, ey, R = CX, 470 * U, 120 * U
    else: ex, ey, R = W * 0.22, CY - 60 * U, 130 * U
    bul = 1 + 0.03 * math.sin(t * 2)
    ma = t * 0.35
    ctx.save(); ctx.translate(ex, ey); ctx.rotate(ma); ctx.scale(R * 1.22 * bul, R * 1.03); ctx.arc(0, 0, 1, 0, 2 * math.pi); ctx.restore()
    rgba(ctx, (0.35, 0.7, 1.0), 0.5); ctx.fill()
    globe(ctx, ex, ey, R, t * 0.4)
    md = 220 * U
    moon(ctx, ex + md * math.cos(ma), ey + md * math.sin(ma), 40 * U)
    sw = prog(t, d * 0.66, d * 0.74)
    text(ctx, "MOON'S TIDES = A BRAKE", ex, ey - 300 * U if not VERT else ey + 290 * U, 34 * U, WHITE, prog(t, 1, 1.6) * (1 - sw if VERT else 1))
    if VERT: cx2, cy2 = CX, 1080 * U
    else: cx2, cy2 = W * 0.66, CY - 80 * U
    if sw < 1:
        ca = prog(t, 0.3, 0.9) * (1 - sw)
        clockface(ctx, cx2 - (0 if VERT else 120 * U), cy2, 150 * U if not VERT else 130 * U, t, ca)
        if not VERT:
            text(ctx, "+ ≈ 2 ms", cx2 + 230 * U, cy2 - 40 * U, 80 * U, GOLD, prog(t, d * 0.3, d * 0.38) * (1 - sw))
            text(ctx, "per century", cx2 + 230 * U, cy2 + 40 * U, 44 * U, WHITE, prog(t, d * 0.3, d * 0.38) * (1 - sw), False)
        else:
            text(ctx, "+ ≈ 2 ms per century", CX, cy2 - 175 * U, 56 * U, GOLD, prog(t, d * 0.3, d * 0.38) * (1 - sw))
    if sw > 0:
        dy = 130 * U if not VERT else 60 * U
        dino(ctx, cx2 + (0 if VERT else 20 * U), cy2 + dy, 0.9 * U, (0.55, 0.75, 0.45), sw)
        ty = cy2 - 270 * U if not VERT else cy2 - 330 * U
        text(ctx, "DINOSAUR ERA:", cx2, ty, 48 * U, WHITE, sw)
        text(ctx, "SLIGHTLY SHORTER DAYS", cx2, ty + 65 * U, 48 * U, GOLD, sw)
    chip(ctx, "GOOD NEWS: NO SUDDEN STOP", t)

def sc_outro(ctx, t, d):
    vgrad(ctx, NAVY2, NAVY); stars(ctx, t, 0.6)
    yo = -80 * U if not VERT else -200 * U
    globe(ctx, CX, CY + yo - 210 * U, 80 * U, t * 0.8)
    text(ctx, "FACTORA", CX, CY + yo, 140 * U, WHITE, prog(t, 0, 0.6))
    text(ctx, "fascinating facts, explained", CX, CY + yo + 100 * U, 38 * U, GOLD, prog(t, 0.4, 1.0), False)
    k = prog(t, d * 0.55, d * 0.65)
    if k:
        bw, bh = 520 * U, 110 * U
        pop = 1 + 0.05 * math.sin(t * 6)
        ctx.save(); ctx.translate(CX, CY + yo + 260 * U); ctx.scale(pop * k, pop * k)
        rrect(ctx, -bw / 2, -bh / 2, bw, bh, 22 * U); rgba(ctx, (0.85, 0.12, 0.12)); ctx.fill()
        text(ctx, "SUBSCRIBE", 0, 0, 52 * U, WHITE)
        ctx.restore()
    q = prog(t, d * 0.3, d * 0.4)
    if q and k < 1: text(ctx, "Which one surprised you most?", CX, CY + yo + 260 * U, 44 * U, WHITE, q * (1 - k))

SHORT_SCENES = ["hook", "stop", "day", "outro"]

SCENES = dict(hook=sc_hook, speed=sc_speed, stop=sc_stop, winds=sc_winds, oceans=sc_oceans, day=sc_day,
              magnet=sc_magnet, slowing=sc_slowing, outro=sc_outro)

def thumbnail(c):
    """1280x720 thumbnail (render.py thumb mode)."""
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, .08, .11, .26); g.add_color_stop_rgb(1, .02, .03, .08); c.set_source(g); c.paint()
    random.seed(1)
    for _ in range(180):
        c.arc(random.random() * W, random.random() * H, random.uniform(.5, 1.8), 0, 6.3); c.set_source_rgba(1, 1, 1, random.uniform(.3, .9)); c.fill()
    gx, gy, r = 1050, 340, 190
    globe(c, gx, gy, r, 0.5)
    c.set_line_width(10); c.set_line_cap(cairo.LINE_CAP_ROUND)
    for a0 in (2.6, -0.4):
        c.save(); c.translate(gx, gy); c.scale(r * 1.18, r * 0.28); c.arc(0, 0, 1, a0, a0 + 1.4); c.restore()
        c.set_source_rgb(1, .8, .33); c.stroke()
    # stop sign
    sx, sy, sr = 1120, 560, 95
    c.save(); c.translate(sx, sy)
    for i in range(8):
        an = math.pi / 8 + i * math.pi / 4
        (c.line_to if i else c.move_to)(sr * math.cos(an), sr * math.sin(an))
    c.close_path(); c.set_source_rgb(.85, .12, .12); c.fill_preserve(); c.set_source_rgb(1, 1, 1); c.set_line_width(7); c.stroke()
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(52)
    e = c.text_extents("STOP"); c.move_to(-e.width / 2 - e.x_bearing, 18); c.show_text("STOP")
    c.restore()
    thumb_text(c, "WHAT IF EARTH", "STOPPED SPINNING?", "1,000 MPH → 0")
