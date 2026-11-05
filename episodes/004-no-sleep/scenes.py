# Scenes for episode 004 "What happens to your body when you don't sleep?"
# Executed inside engine/render.py's namespace (W, H, U, CX, CY, VERT, colors, helpers...).

PINK = (0.93, 0.62, 0.70)
PINK_D = (0.72, 0.40, 0.50)
BLUE_L = (0.45, 0.78, 1.0)
DIM = (0.55, 0.60, 0.75)

try:
    _TL = json.load(open(EP + "/build/timeline.json"))
except Exception:
    _TL = []

def ST(scene, i, default=0.0):
    """Start time of sentence i of a scene, in the scene's local time."""
    for k, s in enumerate(_TL):
        if s["scene"] == scene:
            off = 0.0 if k == 0 else s["start"]
            if i < len(s["sents"]): return s["sents"][i]["start"] - off
    return default

def L(h, v): return v if VERT else h

def bg(ctx, t, sa=0.5):
    vgrad(ctx, NAVY2, NAVY); stars(ctx, t, sa)

def label(ctx, s, x, y, size, c=WHITE, a=1.0, bold=True, align="c"):
    if a > 0.001: text(ctx, s, x, y, size * U, c, a, bold, align)

# ---------- drawing helpers ----------
def eye(ctx, x, y, r, open_k, tired=0.0, a=1.0):
    """Almond eye; open_k 0 (closed) .. 1 (open); tired adds red veins + heavy lid."""
    up = y - r * 0.85 * open_k; lo = y + r * 0.55 * max(open_k, 0.05)
    def almond():
        ctx.move_to(x - r, y)
        ctx.curve_to(x - r * 0.5, up, x + r * 0.5, up, x + r, y)
        ctx.curve_to(x + r * 0.5, lo, x - r * 0.5, lo, x - r, y)
        ctx.close_path()
    glow(ctx, x, y, r * 1.8, GOLD, 0.12 * a)
    almond(); rgba(ctx, (0.97, 0.95, 0.92), a); ctx.fill()
    ctx.save(); almond(); ctx.clip()
    if tired > 0:
        ctx.set_line_width(2.5 * U); rgba(ctx, CORAL, 0.8 * tired * a)
        for i in range(6):
            sx = x - r * 0.95 if i % 2 == 0 else x + r * 0.95
            dirx = 1 if i % 2 == 0 else -1
            yy = y + (i // 2 - 1) * r * 0.18
            ctx.move_to(sx, yy)
            ctx.curve_to(sx + dirx * r * 0.2, yy - r * 0.08, sx + dirx * r * 0.3, yy + r * 0.06, sx + dirx * r * 0.45, yy - r * 0.04)
            ctx.stroke()
    circle(ctx, x, y, r * 0.42, SEA, a)
    circle(ctx, x, y, r * 0.42 * 0.85, mix(SEA, SEA_D, 0.4), a)
    circle(ctx, x, y, r * 0.18, (0.02, 0.03, 0.06), a)
    circle(ctx, x - r * 0.12, y - r * 0.13, r * 0.07, WHITE, 0.9 * a)
    ctx.restore()
    # lid line + lashes
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.move_to(x - r, y); ctx.curve_to(x - r * 0.5, up, x + r * 0.5, up, x + r, y)
    rgba(ctx, NAVY, a); ctx.set_line_width(9 * U); ctx.stroke()
    ctx.move_to(x - r * 1.02, y); ctx.curve_to(x - r * 0.5, up - 8 * U, x + r * 0.5, up - 8 * U, x + r * 1.02, y)
    rgba(ctx, GOLD, 0.9 * a); ctx.set_line_width(5 * U); ctx.stroke()
    for i in range(7):
        s = 0.2 + i * 0.1
        # point on upper bezier
        p0, p1, p2, p3 = (x - r, y), (x - r * 0.5, up), (x + r * 0.5, up), (x + r, y)
        bx = (1 - s) ** 3 * p0[0] + 3 * (1 - s) ** 2 * s * p1[0] + 3 * (1 - s) * s * s * p2[0] + s ** 3 * p3[0]
        by = (1 - s) ** 3 * p0[1] + 3 * (1 - s) ** 2 * s * p1[1] + 3 * (1 - s) * s * s * p2[1] + s ** 3 * p3[1]
        ctx.move_to(bx, by - 4 * U); ctx.line_to(bx + (s - 0.5) * 30 * U, by - 26 * U)
    rgba(ctx, GOLD, 0.9 * a); ctx.set_line_width(4 * U); ctx.stroke()

def brain_path(ctx, x, y, r):
    for (dx, dy, rr) in [(-0.48, 0.0, 0.48), (-0.15, -0.32, 0.5), (0.3, -0.25, 0.48), (0.55, 0.08, 0.38),
                         (0.05, 0.12, 0.55), (-0.38, 0.22, 0.4), (0.3, 0.25, 0.4)]:
        ctx.new_sub_path(); ctx.arc(x + dx * r, y + dy * r, rr * r, 0, 2 * math.pi)

def brain(ctx, x, y, r, a=1.0, col=PINK, glow_a=0.25):
    glow(ctx, x, y, r * 1.6, col, glow_a * a)
    # stem + cerebellum
    rgba(ctx, PINK_D, a)
    ctx.move_to(x + 0.18 * r, y + 0.55 * r); ctx.line_to(x + 0.38 * r, y + 0.55 * r)
    ctx.line_to(x + 0.32 * r, y + 1.0 * r); ctx.line_to(x + 0.16 * r, y + 1.0 * r); ctx.close_path(); ctx.fill()
    circle(ctx, x + 0.58 * r, y + 0.55 * r, 0.26 * r, mix(col, PINK_D, 0.5), a)
    brain_path(ctx, x, y, r); rgba(ctx, col, a); ctx.fill()
    # folds
    ctx.save(); brain_path(ctx, x, y, r); ctx.clip()
    ctx.set_line_width(5 * U * r / (200 * U)); ctx.set_line_cap(cairo.LINE_CAP_ROUND); rgba(ctx, PINK_D, 0.85 * a)
    random.seed(21)
    for i in range(16):
        px = x + random.uniform(-0.9, 0.85) * r; py = y + random.uniform(-0.75, 0.55) * r
        ang = random.uniform(0, math.pi)
        ln = random.uniform(0.15, 0.32) * r
        ctx.move_to(px, py)
        ctx.curve_to(px + math.cos(ang) * ln * 0.4 + ln * 0.2, py + math.sin(ang) * ln * 0.4 - ln * 0.3,
                     px + math.cos(ang) * ln * 0.7 - ln * 0.2, py + math.sin(ang) * ln * 0.7 + ln * 0.3,
                     px + math.cos(ang) * ln, py + math.sin(ang) * ln)
        ctx.stroke()
    # central fissure
    ctx.move_to(x - 0.85 * r, y + 0.2 * r); ctx.curve_to(x - 0.3 * r, y + 0.05 * r, x + 0.2 * r, y + 0.35 * r, x + 0.75 * r, y + 0.2 * r)
    ctx.set_line_width(7 * U * r / (200 * U)); ctx.stroke()
    ctx.restore()

def glass(ctx, x, y, s, level, marks=(), a=1.0):
    """Tumbler centered on x, bottom at y, height s. level 0..1 of the height."""
    wt, wb = s * 0.42, s * 0.32
    def shape():
        ctx.move_to(x - wt, y - s); ctx.line_to(x + wt, y - s); ctx.line_to(x + wb, y); ctx.line_to(x - wb, y); ctx.close_path()
    ctx.save(); shape(); ctx.clip()
    rgba(ctx, WHITE, 0.06 * a); ctx.paint()
    ly = y - s * level
    g = cairo.LinearGradient(0, ly, 0, y); g.add_color_stop_rgba(0, 1.0, 0.78, 0.35, 0.95 * a); g.add_color_stop_rgba(1, 0.85, 0.5, 0.15, 0.95 * a)
    ctx.set_source(g); ctx.rectangle(x - s, ly, 2 * s, s * 1.2); ctx.fill()
    ctx.restore()
    shape(); rgba(ctx, WHITE, 0.85 * a); ctx.set_line_width(6 * U); ctx.stroke()
    for (lv, lab, col) in marks:
        yy = y - s * lv; xr = x + wb + (wt - wb) * lv
        ctx.set_dash([10 * U, 8 * U]); ctx.move_to(x - wb - (wt - wb) * lv - 10 * U, yy); ctx.line_to(xr + 40 * U, yy)
        rgba(ctx, col, a); ctx.set_line_width(4 * U); ctx.stroke(); ctx.set_dash([])
        text(ctx, lab, xr + 55 * U, yy, 34 * U, col, a, True, "l")

def clock(ctx, x, y, r, hours, a=1.0):
    glow(ctx, x, y, r * 1.5, GOLD, 0.15 * a)
    circle(ctx, x, y, r, NAVY2, a)
    ctx.arc(x, y, r, 0, 2 * math.pi); rgba(ctx, GOLD, a); ctx.set_line_width(8 * U); ctx.stroke()
    for i in range(12):
        an = i / 12 * 2 * math.pi
        ctx.move_to(x + math.sin(an) * r * 0.8, y - math.cos(an) * r * 0.8); ctx.line_to(x + math.sin(an) * r * 0.92, y - math.cos(an) * r * 0.92)
    rgba(ctx, WHITE, 0.8 * a); ctx.set_line_width(5 * U); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    ha = (hours % 12) / 12 * 2 * math.pi; ma = (hours % 1) * 2 * math.pi
    ctx.move_to(x, y); ctx.line_to(x + math.sin(ha) * r * 0.5, y - math.cos(ha) * r * 0.5)
    rgba(ctx, WHITE, a); ctx.set_line_width(11 * U); ctx.stroke()
    ctx.move_to(x, y); ctx.line_to(x + math.sin(ma) * r * 0.75, y - math.cos(ma) * r * 0.75)
    rgba(ctx, GOLD, a); ctx.set_line_width(6 * U); ctx.stroke()
    circle(ctx, x, y, 10 * U, GOLD, a)

def person(ctx, x, y, s, c, a=1.0):
    circle(ctx, x, y - s * 0.75, s * 0.22, c, a)
    ctx.move_to(x - s * 0.36, y); ctx.curve_to(x - s * 0.36, y - s * 0.55, x + s * 0.36, y - s * 0.55, x + s * 0.36, y)
    ctx.close_path(); rgba(ctx, c, a); ctx.fill()

def heart(ctx, x, y, s, c, a=1.0):
    ctx.move_to(x, y + s * 0.45)
    ctx.curve_to(x - s * 0.9, y - s * 0.15, x - s * 0.45, y - s * 0.75, x, y - s * 0.3)
    ctx.curve_to(x + s * 0.45, y - s * 0.75, x + s * 0.9, y - s * 0.15, x, y + s * 0.45)
    rgba(ctx, c, a); ctx.fill()

def drop(ctx, x, y, s, c, a=1.0):
    ctx.move_to(x, y - s * 0.6)
    ctx.curve_to(x + s * 0.15, y - s * 0.3, x + s * 0.45, y, x + s * 0.45, y + s * 0.2)
    ctx.arc(x, y + s * 0.2, s * 0.45, 0, math.pi)
    ctx.curve_to(x - s * 0.45, y, x - s * 0.15, y - s * 0.3, x, y - s * 0.6)
    rgba(ctx, c, a); ctx.fill()

def scale_icon(ctx, x, y, s, c, a=1.0):
    rrect(ctx, x - s * 0.5, y - s * 0.45, s, s * 0.9, s * 0.14); rgba(ctx, c, a); ctx.fill()
    ctx.arc(x, y - s * 0.1, s * 0.25, math.pi, 2 * math.pi); rgba(ctx, NAVY, a); ctx.set_line_width(s * 0.08); ctx.stroke()
    ctx.move_to(x, y - s * 0.1); ctx.line_to(x + s * 0.15, y - s * 0.28); ctx.set_line_width(s * 0.06); ctx.stroke()

def cloud(ctx, x, y, s, c, a=1.0, rain=0.0, t=0):
    for (dx, dy, rr) in [(-0.3, 0.05, 0.28), (0.0, -0.12, 0.36), (0.32, 0.05, 0.27)]:
        circle(ctx, x + dx * s, y + dy * s, rr * s, c, a)
    rrect(ctx, x - s * 0.58, y, s * 1.16, s * 0.3, s * 0.15); rgba(ctx, c, a); ctx.fill()
    if rain:
        ctx.set_line_width(s * 0.05); ctx.set_line_cap(cairo.LINE_CAP_ROUND); rgba(ctx, BLUE_L, a * rain)
        for i in range(4):
            xx = x + (i - 1.5) * s * 0.25; ph = (t * 1.5 + i * 0.37) % 1
            ctx.move_to(xx, y + s * (0.45 + ph * 0.3)); ctx.line_to(xx - s * 0.05, y + s * (0.6 + ph * 0.3))
        ctx.stroke()

# ---------- scenes ----------
def sc_hook(ctx, t, d):
    k = prog(t, 0, d)
    vgrad(ctx, mix(NAVY2, (0.12, 0.08, 0.2), k), NAVY); stars(ctx, t, 0.5)
    # window with moon
    wx, wy, ww, wh = L((W * 0.08, H * 0.16, 520 * U, 560 * U), (CX - 230 * U, 300 * U, 460 * U, 380 * U))
    rrect(ctx, wx, wy, ww, wh, 20 * U); rgba(ctx, (0.03, 0.04, 0.10)); ctx.fill()
    ctx.save(); rrect(ctx, wx, wy, ww, wh, 20 * U); ctx.clip()
    moon(ctx, wx + ww * 0.65, wy + wh * 0.32, 60 * U)
    random.seed(4)
    for _ in range(25): circle(ctx, wx + random.random() * ww, wy + random.random() * wh, random.uniform(1, 2.5) * U, WHITE, 0.7)
    ctx.restore()
    rrect(ctx, wx, wy, ww, wh, 20 * U); rgba(ctx, GOLD, 0.8); ctx.set_line_width(8 * U); ctx.stroke()
    ctx.move_to(wx + ww / 2, wy); ctx.line_to(wx + ww / 2, wy + wh); ctx.move_to(wx, wy + wh / 2); ctx.line_to(wx + ww, wy + wh / 2)
    ctx.set_line_width(6 * U); ctx.stroke()
    # eye: blinks get slower and heavier
    ex, ey = L((W * 0.64, H * 0.36), (CX, 960 * U))
    per = 2.6 - 1.2 * k
    ph = (t % per) / per
    blink = 1 - math.exp(-((ph - 0.5) / (0.06 + 0.12 * k)) ** 2)
    openk = (1 - 0.45 * k) * blink
    eye(ctx, ex, ey, L(230, 220) * U, openk, k)
    # counter
    hrs = int(24 * prog(t, 0.5, d - 1.2))
    cy = L(H * 0.68, 1210 * U)
    label(ctx, "HOURS AWAKE", ex, cy - 70 * U, 38, DIM)
    label(ctx, f"{hrs:02d} h", ex, cy + 10 * U, 96, GOLD)

def sc_need(ctx, t, d):
    bg(ctx, t, 0.4)
    rx, ry, R = L((W * 0.3, H * 0.45, 230 * U), (CX, 620 * U, 230 * U))
    # 24 h ring
    ctx.arc(rx, ry, R, 0, 2 * math.pi); rgba(ctx, WHITE, 0.12); ctx.set_line_width(46 * U); ctx.stroke()
    p = prog(t, ST("need", 1), ST("need", 1) + 2.5)
    a0 = -math.pi / 2 - 7 / 24 * 2 * math.pi * 0.5
    if p > 0:
        ctx.arc(rx, ry, R, a0, a0 + 7 / 24 * 2 * math.pi * p); rgba(ctx, GOLD); ctx.set_line_width(46 * U); ctx.stroke()
    for i in range(24):
        an = i / 24 * 2 * math.pi
        ctx.move_to(rx + math.cos(an) * (R + 32 * U), ry + math.sin(an) * (R + 32 * U))
        ctx.line_to(rx + math.cos(an) * (R + 44 * U), ry + math.sin(an) * (R + 44 * U))
    rgba(ctx, WHITE, 0.5); ctx.set_line_width(3 * U); ctx.stroke()
    moon(ctx, rx, ry - R - 110 * U, 34 * U, prog(t, 0, 1))
    label(ctx, "7+", rx, ry - 20 * U, 130, GOLD, prog(t, ST("need", 1), ST("need", 1) + 1))
    label(ctx, "HOURS A NIGHT", rx, ry + 80 * U, 34, WHITE, prog(t, ST("need", 1) + 0.5, ST("need", 1) + 1.5))
    # one in three
    q = prog(t, ST("need", 2), ST("need", 2) + 1)
    px, py = L((W * 0.7, H * 0.5), (CX, 1180 * U))
    sp = L(170, 170) * U
    for i in range(3):
        pop = prog(t, ST("need", 2) + i * 0.3, ST("need", 2) + i * 0.3 + 0.5)
        c = CORAL if i == 2 else WHITE
        person(ctx, px + (i - 1) * sp, py, 150 * U * (0.6 + 0.4 * pop), c, pop)
    label(ctx, "≈ 1 IN 3 U.S. ADULTS", px, py - L(250, 230) * U, 50, CORAL, q)
    label(ctx, "regularly sleeps less", px, py - L(190, 175) * U, 36, WHITE, q * 0.9, False)
    chip(ctx, "HOW MUCH DO WE NEED?", t)

def sc_hour18(ctx, t, d):
    bg(ctx, t, 0.4)
    cx_, cy_ = L((W * 0.28, H * 0.42), (CX, 560 * U))
    hrs = 6 + 12 * prog(t, 0.2, ST("hour18", 1) + 1)
    clock(ctx, cx_, cy_, 200 * U, hrs)
    label(ctx, "HOUR 18", cx_, cy_ + 270 * U, 64, GOLD, prog(t, ST("hour18", 1), ST("hour18", 1) + 0.6))
    # reaction-time bar (slows)
    if not VERT:
        rx0, ry0 = W * 0.52, H * 0.22
        label(ctx, "REACTION TIME", rx0, ry0, 34, DIM, prog(t, ST("hour18", 1), ST("hour18", 1) + 0.8), True, "l")
        slow = prog(t, ST("hour18", 1) + 0.5, ST("hour18", 2))
        rrect(ctx, rx0, ry0 + 35 * U, 700 * U, 26 * U, 13 * U); rgba(ctx, WHITE, 0.12); ctx.fill()
        rrect(ctx, rx0, ry0 + 35 * U, 700 * U * (0.35 + 0.45 * slow), 26 * U, 13 * U); rgba(ctx, mix(GOLD, CORAL, slow), 0.95); ctx.fill()
    # glass
    g = prog(t, ST("hour18", 2) + 2, ST("hour18", 2) + 5)
    gx, gy = L((W * 0.66, H * 0.75), (CX - 120 * U, 1260 * U))
    gs = L(330, 300) * U
    glass(ctx, gx, gy, gs, 0.4 * g, [(0.4, "≈ 0.05%", GOLD)] if g > 0.95 else [], prog(t, ST("hour18", 2), ST("hour18", 2) + 0.8))
    label(ctx, "SAME AS A BLOOD ALCOHOL LEVEL OF", L(gx + 80 * U, CX), L(gy - gs - 50 * U, gy - gs - 50 * U), L(30, 30), WHITE, prog(t, ST("hour18", 2) + 3, ST("hour18", 2) + 4), True)
    chip(ctx, "HOUR 18", t)

def road(ctx, x, y, w, h, t, blackout):
    ctx.save(); rrect(ctx, x, y, w, h, 24 * U); ctx.clip()
    vgrad(ctx, (0.02, 0.03, 0.08), (0.06, 0.08, 0.18), y, y + h)
    hz = y + h * 0.4
    for i in range(12):
        circle(ctx, x + w * ((i * 0.37) % 1), y + h * 0.05 + (i * 0.23 % 0.3) * h, 2 * U, WHITE, 0.6)
    rgba(ctx, (0.04, 0.06, 0.1)); ctx.rectangle(x, hz, w, h); ctx.fill()
    vx = x + w / 2
    ctx.move_to(vx - 6 * U, hz); ctx.line_to(vx + 6 * U, hz); ctx.line_to(x + w * 0.95, y + h); ctx.line_to(x + w * 0.05, y + h); ctx.close_path()
    rgba(ctx, (0.16, 0.17, 0.22)); ctx.fill()
    # headlight cone
    g = cairo.RadialGradient(vx, y + h, 0, vx, y + h, h * 0.8)
    g.add_color_stop_rgba(0, 1, 0.95, 0.7, 0.35); g.add_color_stop_rgba(1, 1, 0.95, 0.7, 0)
    ctx.set_source(g); ctx.move_to(vx, hz); ctx.line_to(x + w * 0.95, y + h); ctx.line_to(x + w * 0.05, y + h); ctx.close_path(); ctx.fill()
    # moving dashes
    for i in range(10):
        z = ((i / 10) + t * 0.5) % 1
        z2 = z ** 2.2; z3 = min(1, (z + 0.04)) ** 2.2
        y1, y2 = hz + (y + h - hz) * z2, hz + (y + h - hz) * z3
        ww = 3 * U + 14 * U * z2
        ctx.move_to(vx - ww, y1); ctx.line_to(vx + ww, y1); ctx.line_to(vx + ww * 1.2, y2); ctx.line_to(vx - ww * 1.2, y2); ctx.close_path()
        rgba(ctx, GOLD, 0.9); ctx.fill()
    if blackout > 0:
        rgba(ctx, (0, 0, 0), 0.94 * blackout); ctx.paint()
        text(ctx, "MICROSLEEP", x + w / 2, y + h * 0.45, 64 * U, CORAL, blackout)
        text(ctx, "a few seconds", x + w / 2, y + h * 0.45 + 70 * U, 34 * U, WHITE, 0.8 * blackout, False)
    ctx.restore()
    rrect(ctx, x, y, w, h, 24 * U); rgba(ctx, GOLD, 0.7); ctx.set_line_width(5 * U); ctx.stroke()

def sc_hour24(ctx, t, d):
    bg(ctx, t, 0.4)
    lv = 0.4 + 0.4 * prog(t, 0.6, 3.0)
    gx, gy = L((W * 0.22, H * 0.74), (CX - 170 * U, 760 * U))
    gs = L(400, 360) * U
    bac = 0.05 + 0.05 * prog(t, 0.6, 3.0)
    marks = [(0.64, "0.08% U.S. limit", CORAL)] if t > ST("hour24", 1) else []
    glass(ctx, gx, gy, gs, lv, marks)
    label(ctx, f"≈ {bac:.2f}%", gx, gy - gs - 50 * U, 60, GOLD)
    # road + microsleeps
    rx, ry, rw, rh = L((W * 0.48, H * 0.13, W * 0.46, H * 0.62), (90 * U, 820 * U, W - 180 * U, 440 * U))
    ra = prog(t, ST("hour24", 2) - 1, ST("hour24", 2))
    if ra > 0:
        ctx.save(); ctx.push_group()
        bo = 0.0
        for c0 in (ST("hour24", 2) + 2.0, ST("hour24", 2) + 4.8):
            bo = max(bo, prog(t, c0, c0 + 0.25) * (1 - prog(t, c0 + 1.6, c0 + 1.9)))
        road(ctx, rx, ry, rw, rh, t, bo)
        ctx.pop_group_to_source(); ctx.paint_with_alpha(ra); ctx.restore()
    chip(ctx, "HOUR 24", t)

def sc_clean(ctx, t, d):
    bg(ctx, t, 0.35)
    bx, by, br = L((W * 0.42, H * 0.43, 250 * U), (CX, 690 * U, 260 * U))
    brain(ctx, bx, by, br)
    sleep_k = prog(t, ST("clean", 1), ST("clean", 1) + 1)
    cut = prog(t, ST("clean", 2), ST("clean", 2) + 1)
    flow = sleep_k * (1 - 0.8 * cut)
    # waste specks
    random.seed(9)
    ctx.save(); brain_path(ctx, bx, by, br); ctx.clip()
    for i in range(70):
        wx = bx + random.uniform(-1, 1) * br; wy = by + random.uniform(-0.8, 0.6) * br
        tw = random.uniform(0, 1)
        washed = prog(t, ST("clean", 1) + 1 + tw * 5, ST("clean", 1) + 2 + tw * 5)
        back = prog(t, ST("clean", 2) + tw * 2.5, ST("clean", 2) + 0.5 + tw * 2.5)
        vis = max(1 - washed, back)
        drift = washed * (1 - back) * 300 * U
        circle(ctx, wx + drift, wy + drift * 0.2, random.uniform(5, 9) * U, (0.75, 0.68, 0.3), 0.9 * vis)
    # fluid channels
    if flow > 0:
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        for j in range(6):
            yy = by - 0.6 * br + j * 0.22 * br
            for i in range(18):
                ph = ((i / 18) + t * 0.18 + j * 0.13) % 1
                xx = bx - 1.1 * br + ph * 2.2 * br
                y2 = yy + 22 * U * math.sin(ph * 9 + j)
                circle(ctx, xx, y2, 7 * U, BLUE_L, 0.75 * flow)
    ctx.restore()
    # labels
    tx = L(W * 0.78, CX)
    moon(ctx, tx, L(H * 0.24, 280 * U), 38 * U, sleep_k * (1 - cut))
    label(ctx, "DURING SLEEP", tx, L(H * 0.38, 370 * U), 46, GOLD, sleep_k * (1 - cut))
    label(ctx, "fluid washes waste away", tx, L(H * 0.38, 370 * U) + 55 * U, 32, WHITE, 0.9 * sleep_k * (1 - cut), False)
    label(ctx, "(studies in mice)", tx, L(H * 0.38, 370 * U) + 100 * U, 28, DIM, 0.9 * sleep_k * (1 - cut), False)
    label(ctx, "NO SLEEP", tx, L(H * 0.38, 370 * U), 52, CORAL, cut)
    label(ctx, "cleaning cut short", tx, L(H * 0.38, 370 * U) + 58 * U, 34, WHITE, cut, False)
    label(ctx, "SLEEP IS NOT JUST REST", L(tx, CX), L(H * 0.38, 370 * U), 44, WHITE, prog(t, 0.3, 1) * (1 - sleep_k))
    chip(ctx, "THE BRAIN'S NIGHT SHIFT", t)

def card(ctx, x, y, s, kind, c, a=1.0, rot=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot)
    rrect(ctx, -s * 0.5, -s * 0.36, s, s * 0.72, s * 0.1); rgba(ctx, c, a); ctx.fill()
    rgba(ctx, NAVY, a)
    if kind == 0:   # star
        ctx.move_to(0, -s * 0.22)
        for i in range(1, 10):
            an = -math.pi / 2 + i * math.pi / 5; rr = s * (0.22 if i % 2 == 0 else 0.09)
            ctx.line_to(math.cos(an) * rr, math.sin(an) * rr)
        ctx.close_path(); ctx.fill()
    elif kind == 1:  # note
        circle(ctx, -s * 0.08, s * 0.12, s * 0.08, NAVY, a); ctx.rectangle(-s * 0.02, -s * 0.2, s * 0.05, s * 0.33); ctx.fill()
        ctx.rectangle(-s * 0.02, -s * 0.2, s * 0.2, s * 0.06); ctx.fill()
    else:            # text lines
        for i in range(3): ctx.rectangle(-s * 0.3, -s * 0.18 + i * s * 0.14, s * (0.6 if i < 2 else 0.35), s * 0.06)
        ctx.fill()
    ctx.restore()

def sc_memory(ctx, t, d):
    bg(ctx, t, 0.35)
    bx, by, br = L((W * 0.66, H * 0.44, 230 * U), (CX, 860 * U, 230 * U))
    px, py = L((W * 0.18, H * 0.44), (CX, 380 * U))
    brain(ctx, bx, by, br)
    label(ctx, "TODAY", px, py - L(150, 130) * U, 40, DIM)
    bad = prog(t, ST("memory", 1), ST("memory", 1) + 0.6)
    cols = [GOLD, WHITE, (0.6, 0.85, 1.0)]
    for i in range(8):
        st = 0.3 + i * 0.5 if i < 5 else ST("memory", 1) + 0.6 + (i - 5) * 0.9
        f = prog(t, st, st + 1.2)
        slot_x = bx + ((i % 4) - 1.5) * 0.36 * br; slot_y = by + (i // 4 - 0.5) * 0.4 * br - 0.1 * br
        if i < 5:
            x = px + (slot_x - px) * f; y = py + (slot_y - py) * f - math.sin(f * math.pi) * 120 * U
            card(ctx, x, y, 90 * U * (1 - 0.25 * f), i % 3, cols[i % 3], 1.0, (1 - f) * 0.3)
        else:
            # bounce off and fade
            g = clamp((t - st) / 1.6)
            if g <= 0:
                card(ctx, px, py, 90 * U, i % 3, cols[i % 3], 1.0, 0.3)
                continue
            if g < 0.6:
                k = g / 0.6; x = px + (bx - br * 1.05 - px) * k; y = py + (by - py) * k - math.sin(k * math.pi) * 100 * U
            else:
                k = (g - 0.6) / 0.4; x = bx - br * 1.05 - 200 * U * k; y = by + 260 * U * k * k
            card(ctx, x, y, 90 * U, i % 3, mix(cols[i % 3], CORAL, 0.6), 1 - clamp((g - 0.7) / 0.3), g * 3)
    label(ctx, "STORED DURING SLEEP", bx, by - br - 70 * U, 40, GOLD, prog(t, 2, 3) * (1 - bad))
    label(ctx, "WITHOUT SLEEP: WEAKER MEMORIES", L(CX, CX), L(H * 0.74, 1260 * U), L(42, 40), CORAL, bad)
    chip(ctx, "MEMORY", t)

def gauge(ctx, x, y, w, h, level, c, name, sub, arrow_up, a=1.0, t=0):
    rrect(ctx, x - w / 2, y - h, w, h, w / 2); rgba(ctx, WHITE, 0.12 * a); ctx.fill()
    lh = (h - 12 * U) * level
    rrect(ctx, x - w / 2 + 6 * U, y - 6 * U - lh, w - 12 * U, lh, (w - 12 * U) / 2); rgba(ctx, c, a); ctx.fill()
    text(ctx, name, x, y + 50 * U, 44 * U, c, a)
    text(ctx, sub, x, y + 98 * U, 30 * U, WHITE, 0.85 * a, False)
    ax = x + w / 2 + 70 * U; ay = y - h / 2 + (math.sin(t * 4) * 8 * U)
    s = 1 if arrow_up else -1
    ctx.move_to(ax, ay - s * 60 * U); ctx.line_to(ax + 40 * U, ay - s * 10 * U); ctx.line_to(ax + 15 * U, ay - s * 10 * U)
    ctx.line_to(ax + 15 * U, ay + s * 55 * U); ctx.line_to(ax - 15 * U, ay + s * 55 * U); ctx.line_to(ax - 15 * U, ay - s * 10 * U)
    ctx.line_to(ax - 40 * U, ay - s * 10 * U); ctx.close_path(); rgba(ctx, c, a); ctx.fill()

def donut(ctx, x, y, r, a=1.0):
    circle(ctx, x, y, r, (0.85, 0.6, 0.35), a); circle(ctx, x, y - 3 * U, r * 0.88, (1.0, 0.55, 0.7), a)
    circle(ctx, x, y, r * 0.32, NAVY, a)
    random.seed(int(x))
    for i in range(10):
        an = random.random() * 6.28; rr = r * random.uniform(0.45, 0.8)
        ctx.save(); ctx.translate(x + math.cos(an) * rr, y + math.sin(an) * rr); ctx.rotate(an * 2)
        rrect(ctx, -7 * U, -2.5 * U, 14 * U, 5 * U, 2.5 * U); rgba(ctx, [GOLD, WHITE, SEA][i % 3], a); ctx.fill(); ctx.restore()

def sc_hunger(ctx, t, d):
    bg(ctx, t, 0.35)
    g0 = ST("hunger", 2); l0 = g0 + 2.8
    gh = 0.35 + 0.5 * prog(t, g0 + 0.3, g0 + 2)
    le = 0.75 - 0.45 * prog(t, l0 + 0.3, l0 + 2)
    gx1, gx2 = L((W * 0.25, W * 0.48), (CX - 230 * U, CX + 190 * U))
    gy, gw, gh_ = L((H * 0.62, 90 * U, 430 * U), (1050 * U, 90 * U, 520 * U))
    a1 = prog(t, ST("hunger", 1), ST("hunger", 1) + 1)
    gauge(ctx, gx1, gy, gw, gh_, gh, CORAL, "GHRELIN", "hunger", True, a1 * (0.4 + 0.6 * prog(t, g0, g0 + 0.5)), t)
    gauge(ctx, gx2, gy, gw, gh_, le, GOLD, "LEPTIN", "fullness", False, a1 * (0.4 + 0.6 * prog(t, l0, l0 + 0.5)), t)
    label(ctx, "TWO HUNGER HORMONES", L(W * 0.37, CX), L(H * 0.17, 330 * U), 40, WHITE, a1)
    # cravings
    c = prog(t, ST("hunger", 3), ST("hunger", 3) + 0.8)
    if not VERT:
        for i in range(3):
            pp = prog(t, ST("hunger", 3) + i * 0.3, ST("hunger", 3) + i * 0.3 + 0.6)
            if pp: donut(ctx, W * 0.8 + (i - 1) * 60 * U, H * 0.25 + i * 170 * U, 75 * U * pp, pp)
        label(ctx, "MORE CRAVINGS", W * 0.8, H * 0.74, 44, GOLD, c)
    if VERT and c:
        # cravings shown over the top area
        for i in range(3):
            pp = prog(t, ST("hunger", 3) + i * 0.3, ST("hunger", 3) + i * 0.3 + 0.6)
            if pp: donut(ctx, CX + (i - 1) * 220 * U, 440 * U, 60 * U * pp, pp)
    chip(ctx, "HUNGER HORMONES", t)

def sc_mood(ctx, t, d):
    bg(ctx, t, 0.35)
    bx, by, br = L((W * 0.32, H * 0.44, 240 * U), (CX, 560 * U, 230 * U))
    brain(ctx, bx, by, br)
    on = prog(t, ST("mood", 1), ST("mood", 1) + 1.5)
    ax, ay = bx - 0.05 * br, by + 0.32 * br
    if on:
        for i in range(3):
            ph = ((t * 0.8 + i / 3) % 1)
            ctx.arc(ax, ay, 30 * U + ph * 220 * U * on, 0, 2 * math.pi)
            rgba(ctx, CORAL, 0.6 * (1 - ph) * on); ctx.set_line_width(6 * U); ctx.stroke()
    pulse = 1 + 0.25 * math.sin(t * 7) * on
    glow(ctx, ax, ay, 70 * U * pulse, CORAL, 0.8 * max(on, 0.3))
    circle(ctx, ax, ay, 26 * U * pulse, mix(PINK_D, CORAL, on))
    # pointer
    lx, ly = L((bx - br - 120 * U, by + 0.75 * br), (bx - 280 * U, by + br + 100 * U))
    la = prog(t, ST("mood", 1) + 0.5, ST("mood", 1) + 1.5)
    ctx.move_to(ax, ay); ctx.line_to(lx, ly - 40 * U); rgba(ctx, WHITE, 0.7 * la); ctx.set_line_width(3 * U); ctx.stroke()
    label(ctx, "AMYGDALA", lx, ly, 42, CORAL, la)
    label(ctx, "the brain's alarm", lx, ly + 48 * U, 30, WHITE, 0.85 * la, False)
    # small problem -> big problem
    g = prog(t, ST("mood", 2), ST("mood", 2) + 1.8)
    sx, sy = L((W * 0.74, H * 0.62), (CX + 150 * U, 1270 * U))
    if t > ST("mood", 2) - 1:
        r = L(30 + 180 * g, 25 + 120 * g) * U
        ctx.move_to(sx - r, sy)
        ctx.curve_to(sx - r, sy - r * 1.3, sx - r * 0.2, sy - r * 1.5, sx + r * 0.3, sy - r * 1.2)
        ctx.curve_to(sx + r * 0.9, sy - r * 1.0, sx + r * 1.1, sy - r * 0.4, sx + r, sy)
        ctx.close_path(); rgba(ctx, mix((0.5, 0.52, 0.62), CORAL, 0.3 * g)); ctx.fill()
        person(ctx, L(sx - 270 * U, sx - 330 * U), sy, 110 * U, WHITE, prog(t, ST("mood", 2) - 1, ST("mood", 2)))
        label(ctx, "SMALL PROBLEMS FEEL BIGGER", L(sx - 60 * U, CX), L(H * 0.18, 1070 * U) if not VERT else sy - 290 * U, L(38, 36), GOLD, g)
    chip(ctx, "EMOTIONS GET LOUDER", t)

def sc_days(ctx, t, d):
    bg(ctx, t, 0.4)
    cx_, cy_ = L((W * 0.3, H * 0.42), (CX, 560 * U))
    day = 1 + int(10 * prog(t, ST("days", 1) + 1.5, ST("days", 2) + 1))
    s = 300 * U
    # calendar
    rrect(ctx, cx_ - s / 2, cy_ - s / 2, s, s, 26 * U); rgba(ctx, (0.95, 0.94, 0.9)); ctx.fill()
    ctx.save(); rrect(ctx, cx_ - s / 2, cy_ - s / 2, s, s, 26 * U); ctx.clip()
    rgba(ctx, CORAL); ctx.rectangle(cx_ - s / 2, cy_ - s / 2, s, s * 0.26); ctx.fill(); ctx.restore()
    text(ctx, "DAY", cx_, cy_ - s * 0.37, 40 * U, WHITE)
    text(ctx, str(day), cx_, cy_ + s * 0.12, 160 * U, NAVY)
    for i in (-1, 1): circle(ctx, cx_ + i * s * 0.28, cy_ - s * 0.5, 14 * U, NAVY2)
    label(ctx, "1964", cx_, cy_ - s / 2 - 70 * U, 50, GOLD, prog(t, ST("days", 1), ST("days", 1) + 0.8))
    # day dots
    dy_ = cy_ + s / 2 + 70 * U
    for i in range(11):
        xx = cx_ + (i - 5) * 42 * U
        circle(ctx, xx, dy_, 14 * U, GOLD if i < day else WHITE, 1.0 if i < day else 0.2)
    label(ctx, "≈ 11 DAYS AWAKE", cx_, dy_ + 70 * U, 46, WHITE, prog(t, ST("days", 1) + 2, ST("days", 1) + 3))
    # symptoms
    sy0 = ST("days", 2)
    items = ["SPEECH", "MEMORY", "FOCUS", "HALLUCINATIONS"]
    for i, it in enumerate(items):
        a = prog(t, sy0 + 0.5 + i * 1.2, sy0 + 1.1 + i * 1.2) * (1 - prog(t, ST("days", 3), ST("days", 3) + 0.6))
        if VERT:
            xx, yy = CX + (-1 if i % 2 == 0 else 1) * 230 * U, 1060 * U + (i // 2) * 110 * U
        else:
            xx, yy = W * 0.72, H * 0.2 + i * 130 * U
        font(ctx, 36 * U); w = ctx.text_extents(it).width + 60 * U
        rrect(ctx, xx - w / 2, yy - 34 * U, w, 68 * U, 34 * U); rgba(ctx, CORAL, 0.9 * a); ctx.fill()
        text(ctx, it, xx, yy, 36 * U, WHITE, a)
    # recovery
    r = prog(t, ST("days", 3), ST("days", 3) + 0.8)
    if r:
        rx, ry = L((W * 0.72, H * 0.4), (CX, 1120 * U))
        moon(ctx, rx, ry - 40 * U, 60 * U, r)
        for i, z in enumerate("Zzz"):
            text(ctx, z, rx + 90 * U + i * 45 * U, ry - 110 * U - i * 40 * U + math.sin(t * 2 + i) * 6 * U, (50 - i * 8) * U, WHITE, r)
        label(ctx, "SLEPT, AND RECOVERED", rx, ry + 90 * U, 44, GOLD, r)
    chip(ctx, "AFTER SEVERAL DAYS", t)

def sc_longterm(ctx, t, d):
    bg(ctx, t, 0.35)
    # nights row
    x0, x1 = L((W * 0.1, W * 0.9), (W * 0.1, W * 0.9))
    yb = L(H * 0.5, 820 * U)
    n = 7
    sw = (x1 - x0) / n
    hmax = L(260, 300) * U
    ref = hmax * 7 / 9
    random.seed(13)
    fade = prog(t, ST("longterm", 2) - 0.5, ST("longterm", 2) + 0.5)
    for i in range(n):
        a = prog(t, 0.3 + i * 0.35, 0.8 + i * 0.35)
        hrs = random.uniform(4.8, 6.0)
        bh = hmax * hrs / 9
        x = x0 + sw * (i + 0.5)
        moon(ctx, x, yb - hmax - 40 * U, 18 * U, a * (1 - fade))
        rrect(ctx, x - sw * 0.28, yb - bh, sw * 0.56, bh, 10 * U); rgba(ctx, CORAL, 0.85 * a * (1 - fade)); ctx.fill()
    ctx.set_dash([12 * U, 10 * U]); ctx.move_to(x0, yb - ref); ctx.line_to(x1, yb - ref)
    rgba(ctx, GOLD, 0.9 * prog(t, 2, 3) * (1 - fade)); ctx.set_line_width(4 * U); ctx.stroke(); ctx.set_dash([])
    label(ctx, "7 h", x1 + 10 * U, yb - ref - 30 * U, 30, GOLD, prog(t, 2, 3) * (1 - fade), True, "r")
    label(ctx, "NIGHT AFTER NIGHT", CX, yb + 50 * U, 40, WHITE, prog(t, ST("longterm", 1), ST("longterm", 1) + 0.8) * (1 - fade))
    # risks
    if fade > 0:
        items = [("HEART DISEASE", heart), ("TYPE 2 DIABETES", drop), ("OBESITY", scale_icon), ("DEPRESSION", cloud)]
        for i, (nm, fn) in enumerate(items):
            a = prog(t, ST("longterm", 2) + 0.6 + i * 0.9, ST("longterm", 2) + 1.2 + i * 0.9)
            if VERT:
                xx, yy = CX + (-1 if i % 2 == 0 else 1) * 240 * U, 480 * U + (i // 2) * 400 * U
            else:
                xx, yy = W * (0.2 + i * 0.2), H * 0.42
            circle(ctx, xx, yy, 120 * U * (0.8 + 0.2 * a), NAVY2, a)
            ctx.arc(xx, yy, 120 * U * (0.8 + 0.2 * a), 0, 2 * math.pi); rgba(ctx, GOLD, a); ctx.set_line_width(4 * U); ctx.stroke()
            if fn is cloud: fn(ctx, xx, yy - 10 * U, 130 * U, (0.7, 0.75, 0.85), a, 1, t)
            else: fn(ctx, xx, yy + (8 if fn is heart else 0) * U, 120 * U, CORAL if fn is not scale_icon else WHITE, a)
            label(ctx, nm, xx, yy + 165 * U, 34, WHITE, a)
        label(ctx, "LINKED TO A HIGHER RISK OF", CX, L(H * 0.18, 300 * U) if not VERT else 300 * U, 40, GOLD, fade)
    chip(ctx, "THE REAL DANGER", t)

def sc_outro(ctx, t, d):
    vgrad(ctx, NAVY2, NAVY); stars(ctx, t, 0.6)
    yo = -80 * U if not VERT else -200 * U
    moon(ctx, CX, CY + yo - 190 * U, 70 * U)
    for i, z in enumerate("zzz"):
        text(ctx, z, CX + 100 * U + i * 36 * U, CY + yo - 250 * U - i * 34 * U + math.sin(t * 2 + i) * 5 * U, (42 - i * 6) * U, GOLD, 0.8)
    text(ctx, "FACTORA", CX, CY + yo, 140 * U, WHITE, prog(t, 0, 0.6))
    text(ctx, "fascinating facts, explained", CX, CY + yo + 100 * U, 38 * U, GOLD, prog(t, 0.4, 1.0), False)
    k = prog(t, ST("outro", 2), ST("outro", 2) + 0.6)
    if k:
        bw, bh = 520 * U, 110 * U
        pop = 1 + 0.05 * math.sin(t * 6)
        ctx.save(); ctx.translate(CX, CY + yo + 260 * U); ctx.scale(pop * k, pop * k)
        rrect(ctx, -bw / 2, -bh / 2, bw, bh, 22 * U); rgba(ctx, (0.85, 0.12, 0.12)); ctx.fill()
        text(ctx, "SUBSCRIBE", 0, 0, 52 * U, WHITE)
        ctx.restore()
    q = prog(t, ST("outro", 1), ST("outro", 1) + 0.6)
    if q and k < 1: text(ctx, "How many hours did you sleep?", CX, CY + yo + 260 * U, 44 * U, WHITE, q * (1 - k))

SHORT_SCENES = ["hook", "hour18", "hour24", "outro"]

SCENES = dict(hook=sc_hook, need=sc_need, hour18=sc_hour18, hour24=sc_hour24, clean=sc_clean, memory=sc_memory,
              hunger=sc_hunger, mood=sc_mood, days=sc_days, longterm=sc_longterm, outro=sc_outro)

def thumbnail(c):
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, .10, .08, .24); g.add_color_stop_rgb(1, .02, .03, .08); c.set_source(g); c.paint()
    random.seed(1)
    for _ in range(150):
        c.arc(random.random() * W, random.random() * H, random.uniform(.5, 1.8), 0, 6.3); c.set_source_rgba(1, 1, 1, random.uniform(.3, .9)); c.fill()
    # big tired eye on the right, with a clock
    eye(c, 1010, 330, 230, 0.55, 1.0)
    clock(c, 1110, 590, 95, 3.2)
    thumb_text(c, "NO SLEEP?", "YOUR BODY...", "HOUR BY HOUR")
