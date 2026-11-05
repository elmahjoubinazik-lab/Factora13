# Scenes for episode 005 "How can a 400-ton airplane fly?"
# Executed inside engine/render.py's namespace (W, H, U, CX, CY, VERT, colors, helpers...).

SKY_L = (0.45, 0.78, 1.0)
BODY = (0.93, 0.94, 0.97)
GREY = (0.62, 0.67, 0.78)
GREY_D = (0.42, 0.46, 0.58)
DIM = (0.55, 0.60, 0.75)

try:
    _TL = json.load(open(EP + "/build/timeline.json"))
except Exception:
    _TL = []

def ST(scene, i, default=0.0):
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
def jet(ctx, x, y, s, ang=0.0, a=1.0, flame=0.0):
    """Side view of an airliner facing right, length s, centered on (x, y)."""
    ctx.save(); ctx.translate(x, y); ctx.rotate(ang); ctx.scale(s, s)
    def poly(pts, c, al=1.0):
        ctx.move_to(*pts[0])
        for p in pts[1:]: ctx.line_to(*p)
        ctx.close_path(); rgba(ctx, c, a * al); ctx.fill()
    # far wing
    poly([(0.06, 0.0), (-0.14, -0.07), (-0.19, -0.07), (-0.06, 0.0)], GREY_D)
    # stabilizer far
    poly([(-0.40, -0.03), (-0.50, -0.07), (-0.53, -0.07), (-0.47, -0.03)], GREY_D)
    # fin
    poly([(-0.33, -0.045), (-0.44, -0.2), (-0.5, -0.2), (-0.49, -0.035)], GOLD)
    # fuselage
    ctx.move_to(-0.5, -0.03); ctx.line_to(0.36, -0.05)
    ctx.curve_to(0.46, -0.05, 0.52, -0.02, 0.52, 0.01)
    ctx.curve_to(0.52, 0.04, 0.46, 0.05, 0.38, 0.05)
    ctx.line_to(-0.26, 0.05); ctx.curve_to(-0.36, 0.05, -0.44, 0.02, -0.5, -0.005); ctx.close_path()
    rgba(ctx, BODY, a); ctx.fill()
    # belly stripe + windows
    ctx.rectangle(-0.42, 0.012, 0.86, 0.008); rgba(ctx, GOLD, a); ctx.fill()
    for i in range(30):
        circle(ctx, -0.33 + i * 0.022, -0.017, 0.0065, NAVY2, a)
    ctx.move_to(0.43, -0.03); ctx.line_to(0.48, -0.028); ctx.line_to(0.495, -0.012); ctx.line_to(0.44, -0.012); ctx.close_path()
    rgba(ctx, NAVY2, a); ctx.fill()
    # near wing
    poly([(0.1, 0.03), (-0.17, 0.13), (-0.23, 0.13), (-0.06, 0.03)], GREY)
    # engines
    for ex, ey in [(0.03, 0.085), (-0.09, 0.115)]:
        poly([(ex, ey - 0.02), (ex + 0.02, ey - 0.03), (ex + 0.03, ey - 0.02)], GREY_D)
        rrect(ctx, ex - 0.035, ey - 0.018, 0.09, 0.036, 0.018); rgba(ctx, GREY, a); ctx.fill()
        circle(ctx, ex + 0.052, ey, 0.016, NAVY2, a)
        if flame > 0: glow(ctx, ex - 0.05, ey, 0.05, GOLD, 0.6 * flame * a)
    # stabilizer near
    poly([(-0.38, -0.01), (-0.5, 0.03), (-0.54, 0.03), (-0.47, -0.012)], GREY)
    ctx.restore()

def foil_pts(c, aoa, m=0.045, p=0.4, th=0.12, n=60):
    """NACA 4-digit airfoil, chord c, centered at mid-chord, rotated (nose up for aoa > 0). Returns list of points."""
    up, lo = [], []
    for i in range(n + 1):
        b = i / n * math.pi; xn = (1 - math.cos(b)) / 2
        yt = 5 * th * (0.2969 * math.sqrt(xn) - 0.126 * xn - 0.3516 * xn ** 2 + 0.2843 * xn ** 3 - 0.1015 * xn ** 4)
        if xn < p: yc = m / p ** 2 * (2 * p * xn - xn ** 2); dy = 2 * m / p ** 2 * (p - xn)
        else: yc = m / (1 - p) ** 2 * (1 - 2 * p + 2 * p * xn - xn ** 2); dy = 2 * m / (1 - p) ** 2 * (p - xn)
        th_ = math.atan(dy)
        up.append((xn - yt * math.sin(th_), yc + yt * math.cos(th_)))
        lo.append((xn + yt * math.sin(th_), yc - yt * math.cos(th_)))
    pts = up + lo[::-1]
    out = []
    ca, sa = math.cos(aoa), math.sin(aoa)
    for (xx, yy) in pts:
        X = (xx - 0.5) * c; Y = -yy * c        # screen y down
        out.append((X * ca - Y * sa, X * sa + Y * ca))
    return out

def draw_foil(ctx, x, y, c, aoa, col=BODY, a=1.0, **kw):
    pts = foil_pts(c, aoa, **kw)
    ctx.move_to(x + pts[0][0], y + pts[0][1])
    for (px, py) in pts[1:]: ctx.line_to(x + px, y + py)
    ctx.close_path()
    g = cairo.LinearGradient(0, y - c * 0.15, 0, y + c * 0.1)
    g.add_color_stop_rgba(0, col[0], col[1], col[2], a); g.add_color_stop_rgba(1, col[0] * 0.75, col[1] * 0.75, col[2] * 0.8, a)
    ctx.set_source(g); ctx.fill_preserve()
    rgba(ctx, GOLD, 0.9 * a); ctx.set_line_width(4 * U); ctx.stroke()

def stream_y(xn, y0n, lift=1.0):
    """Streamline displacement (in chord units) at normalized x for a line starting at y0n (negative = above)."""
    near = math.exp(-abs(y0n) / 0.7)
    above = 1.0 if y0n < 0 else 0.45
    bump = -0.12 * above * math.exp(-((xn + 0.05) / 0.55) ** 2)
    down = 0.32 * clamp((xn - 0.1) / 1.4) ** 1.2
    up_ahead = -0.06 * math.exp(-((xn + 0.7) / 0.35) ** 2)
    return y0n + near * lift * (bump + down + up_ahead)

def streamlines(ctx, x, y, c, t, lift=1.0, lines=(-0.95, -0.62, -0.36, -0.2, 0.2, 0.38, 0.65, 0.95),
                x0=None, x1=None, speed_top=1.0, a=1.0, dots=True):
    x0 = 0 if x0 is None else x0; x1 = W if x1 is None else x1
    for y0n in lines:
        ctx.move_to(x0, y + c * stream_y((x0 - x) / c, y0n, lift))
        n = 80
        for i in range(1, n + 1):
            xx = x0 + (x1 - x0) * i / n
            ctx.line_to(xx, y + c * stream_y((xx - x) / c, y0n, lift))
        rgba(ctx, SKY_L, 0.35 * a); ctx.set_line_width(3 * U); ctx.stroke()
        if dots:
            sp = speed_top if y0n < 0 else 1.0
            for k in range(7):
                ph = (t * 0.16 * sp + k / 7 + y0n * 0.37) % 1
                xx = x0 + (x1 - x0) * ph
                circle(ctx, xx, y + c * stream_y((xx - x) / c, y0n, lift), 7 * U, SKY_L if y0n < 0 or speed_top == 1 else WHITE, 0.9 * a)

def arrow(ctx, x0, y0, x1, y1, c, a=1.0, w=18, head=40):
    w *= U; head *= U
    ang = math.atan2(y1 - y0, x1 - x0); ln = math.hypot(x1 - x0, y1 - y0)
    if ln < 1: return
    ctx.save(); ctx.translate(x0, y0); ctx.rotate(ang)
    hl = min(head, ln * 0.6)
    ctx.move_to(0, -w / 2); ctx.line_to(ln - hl, -w / 2); ctx.line_to(ln - hl, -w * 1.4); ctx.line_to(ln, 0)
    ctx.line_to(ln - hl, w * 1.4); ctx.line_to(ln - hl, w / 2); ctx.line_to(0, w / 2); ctx.close_path()
    rgba(ctx, c, a); ctx.fill(); ctx.restore()

def car(ctx, x, y, s, c, a=1.0):
    rrect(ctx, x - s * 0.5, y - s * 0.22, s, s * 0.26, s * 0.08); rgba(ctx, c, a); ctx.fill()
    rrect(ctx, x - s * 0.28, y - s * 0.4, s * 0.5, s * 0.22, s * 0.08); rgba(ctx, c, a); ctx.fill()
    circle(ctx, x - s * 0.28, y + s * 0.05, s * 0.1, NAVY, a); circle(ctx, x + s * 0.28, y + s * 0.05, s * 0.1, NAVY, a)

def runway(ctx, y0, t, scroll=0.0):
    rgba(ctx, (0.05, 0.07, 0.12)); ctx.rectangle(0, y0, W, H - y0); ctx.fill()
    rgba(ctx, (0.14, 0.15, 0.2)); ctx.rectangle(0, y0, W, 70 * U); ctx.fill()
    for i in range(-1, 14):
        xx = ((i * 180 * U - scroll) % (W + 360 * U)) - 180 * U
        ctx.rectangle(xx, y0 + 32 * U, 90 * U, 8 * U)
    rgba(ctx, WHITE, 0.8); ctx.fill()
    for i in range(-1, 30):
        xx = ((i * 90 * U - scroll * 0.5) % (W + 180 * U)) - 90 * U
        circle(ctx, xx, y0 + 4 * U, 4 * U, GOLD, 0.8)

def cloud(ctx, x, y, s, a=1.0):
    for (dx, dy, rr) in [(-0.3, 0.05, 0.25), (0.0, -0.1, 0.33), (0.3, 0.05, 0.24)]:
        circle(ctx, x + dx * s, y + dy * s, rr * s, WHITE, a)
    rrect(ctx, x - s * 0.55, y, s * 1.1, s * 0.28, s * 0.14); rgba(ctx, WHITE, a); ctx.fill()

# ---------- scenes ----------
def sc_hook(ctx, t, d):
    k = prog(t, ST("hook", 1), ST("hook", 1) + 4.0)
    vgrad(ctx, NAVY2, (0.18, 0.2, 0.38)); stars(ctx, t, 0.5)
    gy = L(H * 0.72, 1180 * U)
    speed = 200 * U * prog(t, ST("hook", 1) - 0.5, ST("hook", 1) + 2)
    runway(ctx, gy, t, t * speed * (1 - 0.8 * k))
    s = L(760, 820) * U
    px = CX + k * L(500, 260) * U
    py = gy - 0.13 * s - k * L(330, 520) * U
    jet(ctx, px, py, s * (1 - 0.35 * k), -0.22 * prog(t, ST("hook", 1) + 0.3, ST("hook", 1) + 1.2), 1.0, prog(t, ST("hook", 1) - 1, ST("hook", 1)))
    # weight tag
    wa = prog(t, 0.6, 1.4) * (1 - prog(t, ST("hook", 1), ST("hook", 1) + 0.6))
    tx, ty = px, py - L(200, 210) * U
    if wa:
        font(ctx, 64 * U); w = ctx.text_extents("≈ 400 TONS").width + 70 * U
        rrect(ctx, tx - w / 2, ty - 50 * U, w, 100 * U, 22 * U); rgba(ctx, GOLD, 0.95 * wa); ctx.fill()
        text(ctx, "≈ 400 TONS", tx, ty, 64 * U, NAVY, wa)
        ctx.move_to(tx, ty + 50 * U); ctx.line_to(tx, py - 0.08 * s); rgba(ctx, GOLD, wa); ctx.set_line_width(4 * U); ctx.stroke()
    # 200 cars
    ca = prog(t, 3.2, 4.2) * (1 - prog(t, ST("hook", 1) - 0.3, ST("hook", 1) + 0.3))
    if ca:
        cols, rows = (25, 8)
        cs = L(38, 34) * U
        gx0 = CX - cols * cs * 1.1 / 2; gy0 = L(H * 0.1, 260 * U)
        for i in range(200):
            r_, c_ = divmod(i, cols)
            pa = ca * prog(t, 3.2 + i * 0.006, 3.6 + i * 0.006)
            car(ctx, gx0 + (c_ + 0.5) * cs * 1.1, gy0 + r_ * cs * 0.8, cs, [WHITE, CORAL, SKY_L][i % 3], pa)
        label(ctx, "= ABOUT 200 CARS", CX, gy0 + rows * cs * 0.8 + L(15, 20) * U, L(46, 44), WHITE, ca)
    q = prog(t, ST("hook", 2), ST("hook", 2) + 0.6)
    label(ctx, "HOW DOES IT FLY?", L(W * 0.32, CX), L(H * 0.3, 420 * U), L(80, 72), GOLD, q)

def sc_forces(ctx, t, d):
    bg(ctx, t, 0.4)
    x, y = L((CX, CY - 80 * U), (CX, 720 * U))
    s = L(620, 640) * U
    jet(ctx, x, y, s)
    st = ST("forces", 1); st2 = ST("forces", 2)
    items = [(st, (0, 1), CORAL, "WEIGHT"), (st + 1.4, (0, -1), GOLD, "LIFT"), (st2, (1, 0), SKY_L, "THRUST"), (st2 + 1.6, (-1, 0), DIM, "DRAG")]
    eq = prog(t, ST("forces", 3), ST("forces", 3) + 0.8)
    for (t0, (dx, dy), c, nm) in items:
        a = prog(t, t0, t0 + 0.7)
        if not a: continue
        ln = (L(200, 230) if dy else L(200, 150)) * U * a
        pulse = 1 + (0.08 * math.sin(t * 6) if eq and nm in ("WEIGHT", "LIFT") else 0)
        ox = dx * s * 0.55; oy = dy * s * 0.13
        arrow(ctx, x + ox, y + oy, x + ox + dx * ln * pulse, y + oy + dy * ln * pulse, c, a)
        lx = x + ox + dx * (ln + 30 * U); ly = y + oy + dy * (ln + 45 * U)
        if dx: ly = y + oy - 60 * U; lx = x + ox + dx * ln * 0.5
        label(ctx, nm, lx, ly, 44, c, a)
    if eq:
        bx, by = L((W * 0.8, H * 0.6), (CX, 1210 * U))
        font(ctx, 46 * U); w = ctx.text_extents("LIFT = WEIGHT").width + 70 * U
        rrect(ctx, bx - w / 2, by - 45 * U, w, 90 * U, 20 * U); rgba(ctx, GOLD, eq); ctx.fill()
        text(ctx, "LIFT = WEIGHT", bx, by, 46 * U, NAVY, eq)
    chip(ctx, "FOUR FORCES", t)

def sc_wing(ctx, t, d):
    bg(ctx, t, 0.3)
    x, y = L((CX, CY - 60 * U), (CX, 760 * U))
    c = L(820, 700) * U
    aoa = math.radians(8) * prog(t, ST("wing", 1) + 1.5, ST("wing", 1) + 3.5)
    lift = prog(t, ST("wing", 2), ST("wing", 2) + 2.0)
    streamlines(ctx, x, y, c, t, 0.15 + 0.85 * lift, a=prog(t, 0, 0.8))
    draw_foil(ctx, x, y, c, aoa)
    # angle of attack marker
    aa = prog(t, ST("wing", 1) + 1.5, ST("wing", 1) + 2.5) * (1 - 0.6 * lift)
    if aa:
        ctx.set_dash([12 * U, 10 * U]); rgba(ctx, WHITE, 0.6 * aa); ctx.set_line_width(3 * U)
        ctx.move_to(x - c * 0.7, y); ctx.line_to(x + c * 0.7, y); ctx.stroke()
        ctx.move_to(x - c * 0.7 * math.cos(aoa), y - c * 0.7 * math.sin(aoa)); ctx.line_to(x + c * 0.7 * math.cos(aoa), y + c * 0.7 * math.sin(aoa))
        ctx.stroke(); ctx.set_dash([])
        ctx.new_path(); ctx.arc(x, y, c * 0.62, math.pi, math.pi + aoa); rgba(ctx, GOLD, aa); ctx.set_line_width(5 * U); ctx.stroke()
        label(ctx, "ANGLE OF ATTACK", x - c * 0.62, y - c * 0.62 * math.sin(aoa) - 60 * U, 36, GOLD, aa, True, "l")
    label(ctx, "CURVED", x - c * 0.1, y - L(190, 200) * U, 40, WHITE, prog(t, ST("wing", 1), ST("wing", 1) + 0.6) * (1 - lift))
    if lift:
        for i in range(3):
            ax = x + c * (L(0.75, 0.3) + i * L(0.12, 0.14)); ay = y + c * (L(0.12, 0.3) + i * 0.03)
            arrow(ctx, ax, ay, ax + 60 * U, ay + 90 * U, SKY_L, lift, 12, 30)
        label(ctx, "FLOW BENT DOWN", L(x + c * 0.68, CX), L(y - c * 0.05, y + c * 0.62), 44, SKY_L, lift)
    chip(ctx, "THE WING", t)

def sc_newton(ctx, t, d):
    bg(ctx, t, 0.3)
    x, y = L((CX, CY - 40 * U), (CX, 700 * U))
    c = L(640, 620) * U
    streamlines(ctx, x, y, c, t, 1.0, a=0.6)
    a1 = prog(t, ST("newton", 1), ST("newton", 1) + 0.8)
    a2 = prog(t, ST("newton", 1) + 1.8, ST("newton", 1) + 2.6)
    lift_up = 30 * U * a2 * (0.5 + 0.5 * math.sin(t * 3))
    draw_foil(ctx, x, y - lift_up, c, math.radians(8))
    for i in range(4):
        ax = x + c * (-0.15 + i * 0.25); ay = y + c * (0.14 + i * 0.02)
        arrow(ctx, ax, ay, ax + 30 * U, ay + L(150, 170) * U * a1, SKY_L, a1, 16, 36)
    label(ctx, "WING PUSHES AIR DOWN", L(x - c * 0.72, CX), L(y + c * 0.32, y + c * 0.62), 42, SKY_L, a1)
    arrow(ctx, x, y - c * 0.12 - lift_up, x, y - c * 0.12 - lift_up - L(190, 210) * U * a2, GOLD, a2, 26, 50)
    label(ctx, "AIR PUSHES WING UP", L(x + 320 * U, CX), L(y - c * 0.12 - 200 * U, y - c * 0.12 - 290 * U), 42, GOLD, a2)
    n = prog(t, ST("newton", 2), ST("newton", 2) + 0.8)
    if n:
        bx, by = L((W * 0.24, H * 0.24), (CX, 300 * U))
        font(ctx, 40 * U); w = ctx.text_extents("NEWTON'S THIRD LAW").width + 70 * U
        rrect(ctx, bx - w / 2, by - 40 * U, w, 80 * U, 20 * U); rgba(ctx, GOLD, n); ctx.fill()
        text(ctx, "NEWTON'S THIRD LAW", bx, by, 40 * U, NAVY, n)
        label(ctx, "action = reaction", bx, by + 70 * U, 34, WHITE, n, False)
    chip(ctx, "THE KEY", t)

def sc_pressure(ctx, t, d):
    bg(ctx, t, 0.3)
    myth = prog(t, ST("pressure", 2), ST("pressure", 2) + 0.8)
    x, y = L((CX, CY - 20 * U + 60 * U * myth), (CX, 740 * U + 60 * U * myth))
    c = L(760, 680) * U
    streamlines(ctx, x, y, c, t, 1.0, speed_top=1.0 + 0.9 * prog(t, 1.5, 3.0))
    draw_foil(ctx, x, y, c, math.radians(7))
    p1 = prog(t, 1.0, 2.0) * (1 - myth); p2 = prog(t, ST("pressure", 1), ST("pressure", 1) + 0.8) * (1 - myth)
    label(ctx, "FASTER AIR · LOWER PRESSURE", x, y - L(310, 330) * U, L(44, 40), SKY_L, p1)
    label(ctx, "HIGHER PRESSURE", x, y + L(225, 300) * U, L(44, 40), GOLD, p2)
    if p2:
        for i in range(5):
            xx = x + (i - 2) * c * 0.17
            label(ctx, "+", xx, y + c * 0.16, 54, GOLD, p2)
            label(ctx, "−", xx, y - c * 0.2, 54, SKY_L, p2)
    if myth:
        bx, by = L((CX, H * 0.2), (CX, 360 * U))
        bw, bh = L(980, 940) * U, 150 * U
        rrect(ctx, bx - bw / 2, by - bh / 2, bw, bh, 24 * U); rgba(ctx, (0.25, 0.08, 0.1), 0.92 * myth); ctx.fill()
        rrect(ctx, bx - bw / 2, by - bh / 2, bw, bh, 24 * U); rgba(ctx, CORAL, myth); ctx.set_line_width(5 * U); ctx.stroke()
        label(ctx, "MYTH: \"top air must catch up\"", bx, by - 22 * U, L(46, 44), WHITE, myth)
        label(ctx, "NASA: the air over the top actually arrives first", bx, by + 38 * U, 30, CORAL, myth, False)
        st = prog(t, ST("pressure", 2) + 2.5, ST("pressure", 2) + 3.2)
        if st:
            ctx.move_to(bx - bw * 0.42, by - 22 * U); ctx.line_to(bx - bw * 0.42 + bw * 0.84 * st, by - 22 * U)
            rgba(ctx, CORAL, 0.75 * myth); ctx.set_line_width(5 * U); ctx.stroke()
    chip(ctx, "PRESSURE", t)

def sc_speed(ctx, t, d):
    bg(ctx, t, 0.3)
    # chart
    ox, oy, cw, ch = L((W * 0.08, H * 0.66, W * 0.36, H * 0.46), (W * 0.16, 870 * U, W * 0.72, 520 * U))
    ca = prog(t, ST("speed", 1) - 0.5, ST("speed", 1) + 0.3)
    rgba(ctx, WHITE, 0.8 * ca); ctx.set_line_width(4 * U)
    ctx.move_to(ox, oy - ch); ctx.line_to(ox, oy); ctx.line_to(ox + cw, oy); ctx.stroke()
    label(ctx, "SPEED →", ox + cw, oy + 85 * U, 32, WHITE, ca, True, "r")
    label(ctx, "LIFT", ox + 20 * U, oy - ch - 10 * U, 32, GOLD, ca, True, "l")
    p = prog(t, ST("speed", 1) + 0.5, ST("speed", 1) + 4.5)
    n = int(100 * p)
    for i in range(n + 1):
        u = i / 100
        (ctx.line_to if i else ctx.move_to)(ox + cw * u, oy - ch * u * u * 0.95)
    if n: rgba(ctx, GOLD, ca); ctx.set_line_width(7 * U); ctx.stroke()
    for (u, lab_s, lab_l, t0) in [(0.5, "1×", "1×", ST("speed", 1) + 2.0), (1.0, "2×", "4×", ST("speed", 1) + 3.8)]:
        m = prog(t, t0, t0 + 0.6)
        if not m: continue
        px_, py_ = ox + cw * u, oy - ch * u * u * 0.95
        ctx.set_dash([10 * U, 8 * U]); rgba(ctx, WHITE, 0.6 * m); ctx.set_line_width(3 * U)
        ctx.move_to(px_, oy); ctx.line_to(px_, py_); ctx.line_to(ox, py_); ctx.stroke(); ctx.set_dash([])
        circle(ctx, px_, py_, 12 * U, GOLD, m)
        label(ctx, lab_s, px_, oy + 40 * U, 36, WHITE, m)
        label(ctx, lab_l, ox - 40 * U, py_, 36, GOLD, m)
    # runway + takeoff
    ra = prog(t, ST("speed", 2) - 0.5, ST("speed", 2) + 0.3)
    if ra:
        rx0, ry0, rw, rh = L((W * 0.5, H * 0.14, W * 0.46, H * 0.6), (60 * U, 980 * U, W - 120 * U, 330 * U))
        ctx.save(); ctx.push_group(); ctx.save()
        rrect(ctx, rx0, ry0, rw, rh, 24 * U); ctx.clip()
        vgrad(ctx, (0.1, 0.13, 0.28), (0.2, 0.24, 0.42), ry0, ry0 + rh)
        gy = ry0 + rh * 0.78
        acc = prog(t, ST("speed", 2), d - 1.5)
        rgba(ctx, (0.12, 0.13, 0.18)); ctx.rectangle(rx0, gy, rw, rh); ctx.fill()
        for i in range(12):
            xx = rx0 + ((i * 120 * U - acc * acc * 2400 * U) % (rw + 120 * U)) - 60 * U
            ctx.rectangle(xx, gy + 25 * U, 60 * U, 7 * U)
        rgba(ctx, WHITE, 0.8); ctx.fill()
        lo = prog(t, d - 3.2, d - 1.4)
        js = L(520, 520) * U
        jet(ctx, rx0 + rw * 0.45 + lo * rw * 0.2, gy - 0.13 * js - lo * rh * 0.35, js, -0.2 * lo, 1, acc)
        mph = int(180 * prog(t, ST("speed", 2), d - 3.2))
        text(ctx, f"{mph} mph", rx0 + rw * 0.5, ry0 + L(80, 60) * U, L(64, 56) * U, GOLD)
        text(ctx, "≈ 290 km/h" if mph >= 180 else "", rx0 + rw * 0.5, ry0 + L(140, 115) * U, 30 * U, WHITE, 0.8, False)
        ctx.restore()
        rrect(ctx, rx0, ry0, rw, rh, 24 * U); rgba(ctx, GOLD, 0.7); ctx.set_line_width(5 * U); ctx.stroke()
        ctx.pop_group_to_source(); ctx.paint_with_alpha(ra); ctx.restore()
    chip(ctx, "SPEED", t)

def sc_engines(ctx, t, d):
    bg(ctx, t, 0.3)
    # cutaway side view: intake on the right, exhaust on the left
    ex, ey = L((W * 0.4, H * 0.45), (CX, 980 * U))
    ln, rad = L(760, 700) * U, L(150, 140) * U
    on = prog(t, ST("engines", 1), ST("engines", 1) + 1.0)
    # air particles
    random.seed(5)
    for i in range(70):
        lane = random.uniform(-0.8, 0.8); ph = random.random()
        u = (ph + t * (0.25 + 0.35 * on)) % 1
        xin = ex + ln * 0.9 - u * ln * 1.9
        if xin > ex + ln * 0.5: yy = ey + lane * rad * 1.2; sp = 1.0
        elif xin > ex - ln * 0.5: yy = ey + lane * rad * (0.8 - 0.25 * (ex + ln * 0.5 - xin) / ln); sp = 1.5
        else: yy = ey + lane * rad * 0.55; sp = 3.0
        hot = xin < ex - ln * 0.5
        ctx.move_to(xin, yy); ctx.line_to(xin + 14 * U * sp, yy)
        rgba(ctx, GOLD if hot else SKY_L, 0.85 * (0.3 + 0.7 * on)); ctx.set_line_width(6 * U); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    # nacelle
    for s_ in (-1, 1):
        ctx.move_to(ex + ln * 0.5, ey + s_ * rad * 1.05)
        ctx.curve_to(ex, ey + s_ * rad * 1.15, ex - ln * 0.3, ey + s_ * rad * 0.95, ex - ln * 0.5, ey + s_ * rad * 0.7)
        ctx.line_to(ex - ln * 0.5, ey + s_ * rad * 0.82)
        ctx.curve_to(ex - ln * 0.3, ey + s_ * rad * 1.15, ex, ey + s_ * rad * 1.35, ex + ln * 0.5, ey + s_ * rad * 1.22)
        ctx.close_path(); rgba(ctx, GREY); ctx.fill()
    # core
    rrect(ctx, ex - ln * 0.4, ey - rad * 0.35, ln * 0.7, rad * 0.7, rad * 0.35); rgba(ctx, GREY_D); ctx.fill()
    ctx.move_to(ex - ln * 0.4, ey - rad * 0.2); ctx.line_to(ex - ln * 0.62, ey); ctx.line_to(ex - ln * 0.4, ey + rad * 0.2); ctx.close_path(); ctx.fill()
    # fan (side view: blades)
    fx = ex + ln * 0.38
    for i in range(9):
        ph = (i / 9 + t * 1.5 * (0.3 + on)) % 1
        yy = ey + math.cos(ph * 2 * math.pi) * rad * 0.98
        wdt = abs(math.sin(ph * 2 * math.pi)) * 16 * U + 4 * U
        rgba(ctx, WHITE, 0.9); ctx.rectangle(fx - wdt / 2, min(ey, yy), wdt, abs(yy - ey)); ctx.fill()
    circle(ctx, fx + 10 * U, ey, rad * 0.22, BODY)
    # labels
    label(ctx, "AIR IN", ex + ln * 0.75, ey - rad * 1.6, 38, SKY_L, prog(t, 0.5, 1.2))
    label(ctx, "AIR BLASTED BACK", ex - ln * 0.6, ey - rad * 1.6, 38, GOLD, on)
    th = prog(t, ST("engines", 1) + 2.5, ST("engines", 1) + 3.3)
    arrow(ctx, ex + ln * 0.2, ey + rad * 1.75, ex + ln * 0.2 + 300 * U * th, ey + rad * 1.75, GOLD, th, 22, 48)
    label(ctx, "THRUST", ex + ln * 0.2 - 30 * U, ey + rad * 1.75, 42, GOLD, th, True, "r")
    big = prog(t, ST("engines", 2), ST("engines", 2) + 0.8)
    if big:
        bx, by = L((W * 0.82, H * 0.62), (CX, 400 * U))
        label(ctx, "EACH ENGINE:", bx, by - 60 * U, 36, WHITE, big)
        label(ctx, "TENS OF THOUSANDS", bx, by, L(46, 52), GOLD, big)
        label(ctx, "OF POUNDS OF THRUST", bx, by + 55 * U, L(36, 40), GOLD, big)
    chip(ctx, "THE ENGINES", t)

def sc_flaps(ctx, t, d):
    bg(ctx, t, 0.3)
    x, y = L((CX - 60 * U, CY - 60 * U), (CX, 760 * U))
    c = L(760, 640) * U
    dep = prog(t, ST("flaps", 1) + 0.8, ST("flaps", 1) + 3.0)
    streamlines(ctx, x, y, c, t, 0.7 + 0.6 * dep, a=0.8)
    aoa = math.radians(5)
    # main wing body (front 75 %)
    ctx.save(); ctx.rectangle(x - c, y - c, c * 1.25, 2 * c); ctx.clip()
    draw_foil(ctx, x, y, c, aoa)
    ctx.restore()
    # flap: rear element slides back and rotates down
    ca, sa = math.cos(aoa), math.sin(aoa)
    hx, hy = x + 0.25 * c * ca, y + 0.25 * c * sa
    fl = foil_pts(c * 0.32, 0, m=0.04, th=0.13)
    rot = -aoa - math.radians(25) * dep
    off = 0.04 * c * dep
    fa = -rot; fr = 0.16 * c + off
    ctx.save(); ctx.translate(hx + fr * math.cos(fa), hy + fr * math.sin(fa) + 0.025 * c * dep); ctx.rotate(fa)
    ctx.move_to(*fl[0])
    for pp in fl[1:]: ctx.line_to(*pp)
    ctx.close_path(); rgba(ctx, mix(BODY, GOLD, 0.35)); ctx.fill_preserve(); rgba(ctx, GOLD); ctx.set_line_width(4 * U); ctx.stroke()
    ctx.restore()
    # slat: front element slides forward and down
    lx, ly = x - 0.5 * c * ca - 0.07 * c * dep, y - 0.5 * c * sa + 0.06 * c * dep
    sl = foil_pts(c * 0.18, math.radians(5 - 30 * dep), m=0.06, th=0.14)
    ctx.move_to(lx + sl[0][0], ly + sl[0][1])
    for pp in sl[1:]: ctx.line_to(lx + pp[0], ly + pp[1])
    ctx.close_path(); rgba(ctx, mix(BODY, GOLD, 0.35), dep); ctx.fill()
    la = prog(t, ST("flaps", 1) + 2.0, ST("flaps", 1) + 2.8)
    label(ctx, "SLAT", lx - 40 * U, ly - L(110, 130) * U, 40, GOLD, la)
    label(ctx, "FLAP", hx + c * 0.5, hy + c * 0.1, 40, GOLD, la)
    e = prog(t, ST("flaps", 2), ST("flaps", 2) + 0.8)
    label(ctx, "EXTRA LIFT AT LOW SPEED", L(CX, CX), L(H * 0.17, 380 * U), L(50, 46), WHITE, e)
    if e: arrow(ctx, x, y - c * 0.15, x, y - c * 0.15 - L(90, 150) * U * e, GOLD, e, 22, 46)
    label(ctx, "TAKEOFF & LANDING", L(W * 0.8, CX), L(H * 0.2, 1240 * U), 36, DIM, prog(t, ST("flaps", 1), ST("flaps", 1) + 0.8) * (1 - e))
    chip(ctx, "SHAPE-SHIFTING WINGS", t)

def sc_cruise(ctx, t, d):
    y_top, y_gnd = L((H * 0.12, H * 0.74), (300 * U, 1290 * U))
    vgrad(ctx, (0.02, 0.03, 0.09), (0.16, 0.24, 0.45), 0, y_gnd)
    stars(ctx, t, 0.3)
    rgba(ctx, (0.06, 0.12, 0.1)); ctx.rectangle(0, y_gnd, W, H - y_gnd); ctx.fill()
    # air density dots: dense low, sparse high
    random.seed(17)
    for i in range(700):
        yy = y_top + (y_gnd - y_top) * (1 - random.random() ** 0.45)
        xx = random.random() * W + (t * 20 * U) % 40
        circle(ctx, xx, yy, 3 * U, SKY_L, 0.35)
    for (cx_, cy_, s_) in [(0.2, 0.86, 160), (0.6, 0.9, 200), (0.9, 0.84, 140)]:
        cloud(ctx, W * cx_, y_top + (y_gnd - y_top) * cy_, s_ * U, 0.8)
    # altitude axis
    axx = L(W * 0.07, 70 * U)
    yc = y_top + (y_gnd - y_top) * 0.12
    rgba(ctx, WHITE, 0.7); ctx.set_line_width(4 * U); ctx.move_to(axx, y_gnd); ctx.line_to(axx, y_top); ctx.stroke()
    ctx.move_to(axx - 15 * U, yc); ctx.line_to(axx + 15 * U, yc); ctx.stroke()
    label(ctx, "35,000 ft", axx + 30 * U, yc - 25 * U, 40, GOLD, 1, True, "l")
    label(ctx, "≈ 11 km", axx + 30 * U, yc + 25 * U, 30, WHITE, 0.85, False, "l")
    # plane cruising
    ph = (t * 0.07) % 1
    jx = L(W * 0.35, W * 0.3) + ph * 0 + 200 * U * prog(t, 0, d)
    jet(ctx, jx + L(250, 120) * U, yc + 10 * U, L(520, 480) * U)
    a1 = prog(t, 1.0, 2.0)
    label(ctx, "THIN AIR", L(W * 0.72, CX), L(H * 0.36, y_top + (y_gnd - y_top) * 0.4), 54, WHITE, a1)
    label(ctx, "less drag", L(W * 0.72, CX), L(H * 0.36, y_top + (y_gnd - y_top) * 0.4) + 55 * U, 36, SKY_L, a1, False)
    a2 = prog(t, ST("cruise", 1) + 1.5, ST("cruise", 1) + 2.3)
    label(ctx, "500+ mph", L(W * 0.72, CX), L(H * 0.52, y_top + (y_gnd - y_top) * 0.57), 64, GOLD, a2)
    label(ctx, "≈ 900 km/h", L(W * 0.72, CX), L(H * 0.52, y_top + (y_gnd - y_top) * 0.57) + 55 * U, 32, WHITE, a2 * 0.85, False)
    chip(ctx, "CRUISING", t)

def sc_glide(ctx, t, d):
    bg(ctx, t, 0.3)
    x0, y0 = L((W * 0.12, H * 0.22), (90 * U, 400 * U))
    x1, y1 = L((W * 0.9, H * 0.68), (W - 90 * U, 1150 * U))
    p = prog(t, 0.5, d - 0.5)
    # glide path
    ctx.set_dash([14 * U, 12 * U]); rgba(ctx, WHITE, 0.5); ctx.set_line_width(4 * U)
    ctx.move_to(x0, y0); ctx.line_to(x1, y1); ctx.stroke(); ctx.set_dash([])
    ang = math.atan2(y1 - y0, x1 - x0) * 0.6
    jx, jy = x0 + (x1 - x0) * p * 0.85, y0 + (y1 - y0) * p * 0.85
    jet(ctx, jx, jy - 30 * U, L(360, 300) * U, ang)
    label(ctx, "ENGINES OFF", jx, jy - L(120, 110) * U, 34, CORAL, prog(t, 0.5, 1.2) * (1 - prog(t, ST("glide", 1), ST("glide", 1) + 0.5)))
    # ratio triangle
    r = prog(t, ST("glide", 1) + 1.0, ST("glide", 1) + 2.0)
    if r:
        rgba(ctx, GOLD, r); ctx.set_line_width(6 * U)
        ctx.move_to(x0, y0); ctx.line_to(x0, y1); ctx.line_to(x1, y1); ctx.stroke()
        label(ctx, "1 mile down", x0 + 20 * U, (y0 + y1) / 2, 36, GOLD, r, True, "l")
        label(ctx, "≈ 15 miles forward", (x0 + x1) / 2, y1 + 45 * U, 40, GOLD, r)
        label(ctx, "(not to scale)", x1, y1 + 45 * U + L(0, 50) * U, 26, DIM, r, False, "r" if not VERT else "r")
    label(ctx, "AN AIRLINER IS A GLIDER", L(W * 0.62, CX), L(H * 0.2, 280 * U), L(50, 46), WHITE, prog(t, ST("glide", 1), ST("glide", 1) + 0.8))
    chip(ctx, "IF THE ENGINES STOP", t)

def sc_outro(ctx, t, d):
    vgrad(ctx, NAVY2, NAVY); stars(ctx, t, 0.6)
    yo = -80 * U if not VERT else -200 * U
    ph = t / d
    jet(ctx, CX - 260 * U + 520 * U * ph, CY + yo - 200 * U - 30 * U * math.sin(ph * 3), 300 * U, -0.08)
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
    if q and k < 1: text(ctx, "Which fact surprised you most?", CX, CY + yo + 260 * U, 44 * U, WHITE, q * (1 - k))

SHORT_SCENES = ["hook", "wing", "newton", "outro"]

SCENES = dict(hook=sc_hook, forces=sc_forces, wing=sc_wing, newton=sc_newton, pressure=sc_pressure, speed=sc_speed,
              engines=sc_engines, flaps=sc_flaps, cruise=sc_cruise, glide=sc_glide, outro=sc_outro)

def thumbnail(c):
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, .08, .11, .26); g.add_color_stop_rgb(1, .16, .2, .4); c.set_source(g); c.paint()
    random.seed(1)
    for _ in range(140):
        c.arc(random.random() * W, random.random() * H * 0.7, random.uniform(.5, 1.8), 0, 6.3); c.set_source_rgba(1, 1, 1, random.uniform(.3, .9)); c.fill()
    glow(c, 1010, 400, 300, GOLD, 0.25)
    jet(c, 1010, 420, 470, -0.25)
    arrow(c, 1010, 330, 1010, 110, GOLD, 1.0, 24, 50)
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(56)
    w = c.text_extents("400 t").width
    rrect(c, 1080 - 20, 560, w + 40, 80, 16); c.set_source_rgb(*CORAL); c.fill()
    c.move_to(1080, 620); c.set_source_rgb(1, 1, 1); c.show_text("400 t")
    thumb_text(c, "400 TONS...", "HOW DOES IT FLY?", "PHYSICS OF LIFT")
