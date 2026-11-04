# Scenes for "How does the Internet actually work?"
# Executed inside engine/render.py: helpers (W, H, U, CX, CY, VERT, colors, vgrad, circle, glow, text, rrect,
# stars, earth, chip, prog, ease, mix...) are available.

CYAN = (0.35, 0.85, 1.0)
GREY = (0.55, 0.6, 0.72)
DARK = (0.06, 0.08, 0.17)

# art zone: keeps the caption area free
AY = H * 0.42 if VERT else H * 0.45


def bg(ctx, t, a=0.5):
    vgrad(ctx, NAVY2, NAVY); stars(ctx, t, a)


def phone(ctx, x, y, s, t=0, screen=None):
    w, h = 120 * s, 220 * s
    rrect(ctx, x - w / 2, y - h / 2, w, h, 18 * s); rgba(ctx, (0.13, 0.15, 0.28)); ctx.fill()
    rrect(ctx, x - w / 2, y - h / 2, w, h, 18 * s); rgba(ctx, GOLD); ctx.set_line_width(4 * s); ctx.stroke()
    rrect(ctx, x - w / 2 + 10 * s, y - h / 2 + 22 * s, w - 20 * s, h - 44 * s, 8 * s); rgba(ctx, (0.1, 0.25, 0.45)); ctx.fill()
    circle(ctx, x, y + h / 2 - 11 * s, 4 * s, GOLD)
    if screen == "play":
        ctx.move_to(x - 16 * s, y - 22 * s); ctx.line_to(x + 22 * s, y); ctx.line_to(x - 16 * s, y + 22 * s); ctx.close_path()
        rgba(ctx, WHITE); ctx.fill()


def laptop(ctx, x, y, s):
    w, h = 230 * s, 150 * s
    rrect(ctx, x - w / 2, y - h, w, h, 10 * s); rgba(ctx, (0.13, 0.15, 0.28)); ctx.fill()
    rrect(ctx, x - w / 2, y - h, w, h, 10 * s); rgba(ctx, GOLD); ctx.set_line_width(4 * s); ctx.stroke()
    ctx.rectangle(x - w / 2 + 12 * s, y - h + 12 * s, w - 24 * s, h - 24 * s); rgba(ctx, (0.1, 0.25, 0.45)); ctx.fill()
    ctx.move_to(x - w / 2 - 30 * s, y + 4 * s); ctx.line_to(x + w / 2 + 30 * s, y + 4 * s); ctx.line_to(x + w / 2 + 10 * s, y + 22 * s)
    ctx.line_to(x - w / 2 - 10 * s, y + 22 * s); ctx.close_path(); rgba(ctx, GOLD); ctx.fill()


def server(ctx, x, y, s, t=0, n=4):
    w, h = 150 * s, 62 * s
    for i in range(n):
        yy = y - n * h / 2 + i * h
        rrect(ctx, x - w / 2, yy + 3 * s, w, h - 6 * s, 8 * s); rgba(ctx, (0.13, 0.15, 0.28)); ctx.fill()
        rrect(ctx, x - w / 2, yy + 3 * s, w, h - 6 * s, 8 * s); rgba(ctx, GREY); ctx.set_line_width(3 * s); ctx.stroke()
        for j in range(3):
            on = 0.5 + 0.5 * math.sin(t * (4 + j) + i * 1.7 + j)
            circle(ctx, x + w / 2 - 22 * s - j * 20 * s, yy + h / 2, 5 * s, (0.3, 1.0, 0.5) if j else GOLD, 0.3 + 0.7 * on)
        ctx.rectangle(x - w / 2 + 16 * s, yy + h / 2 - 3 * s, 50 * s, 6 * s); rgba(ctx, GREY, 0.7); ctx.fill()


def packet(ctx, x, y, s, col=GOLD, a=1.0, label=None):
    w, h = 64 * s, 44 * s
    rrect(ctx, x - w / 2, y - h / 2, w, h, 8 * s); rgba(ctx, (0.1, 0.25, 0.45), a); ctx.fill()
    rrect(ctx, x - w / 2, y - h / 2, w, 14 * s, 6 * s); rgba(ctx, col, a); ctx.fill()
    rrect(ctx, x - w / 2, y - h / 2, w, h, 8 * s); rgba(ctx, col, a); ctx.set_line_width(3 * s); ctx.stroke()
    if label: text(ctx, label, x, y + 7 * s, 18 * s, WHITE, a)


def router(ctx, x, y, s, t=0, col=GOLD, a=1.0):
    glow(ctx, x, y, 70 * s, col, 0.25 * a)
    w, h = 96 * s, 40 * s
    ctx.set_line_width(4 * s); ctx.set_line_cap(cairo.LINE_CAP_ROUND); rgba(ctx, col, a)
    ctx.move_to(x - 28 * s, y - h / 2); ctx.line_to(x - 36 * s, y - h / 2 - 28 * s)
    ctx.move_to(x + 28 * s, y - h / 2); ctx.line_to(x + 36 * s, y - h / 2 - 28 * s); ctx.stroke()
    rrect(ctx, x - w / 2, y - h / 2, w, h, 10 * s); rgba(ctx, (0.13, 0.15, 0.28), a); ctx.fill()
    rrect(ctx, x - w / 2, y - h / 2, w, h, 10 * s); rgba(ctx, col, a); ctx.stroke()
    for j in range(4):
        on = 0.5 + 0.5 * math.sin(t * 5 + j * 1.3 + x * 0.01)
        circle(ctx, x - 30 * s + j * 20 * s, y, 5 * s, (0.3, 1.0, 0.5), a * (0.3 + 0.7 * on))


def path_pt(pts, k):
    """point at fraction k along a polyline"""
    segs = [math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1]) for i in range(len(pts) - 1)]
    L = sum(segs) * clamp(k)
    for i, sl in enumerate(segs):
        if L <= sl or i == len(segs) - 1:
            f = L / sl if sl else 0
            return (pts[i][0] + (pts[i + 1][0] - pts[i][0]) * f, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * f)
        L -= sl


def dashed(ctx, pts, c=WHITE, a=0.45, w=3):
    ctx.set_dash([12 * U, 10 * U]); rgba(ctx, c, a); ctx.set_line_width(w * U)
    ctx.move_to(*pts[0])
    for p in pts[1:]: ctx.line_to(*p)
    ctx.stroke(); ctx.set_dash([])


# ---------------------------------------------------------------- scenes
def sc_hook(ctx, t, d):
    bg(ctx, t, 0.6)
    if VERT:
        P, S = (CX, H * 0.52), (CX, H * 0.18)
        pts = [P, (CX - 280 * U, H * 0.42), (CX + 280 * U, H * 0.29), S]
    else:
        P, S = (W * 0.2, AY + 40 * U), (W * 0.8, AY)
        pts = [P, (W * 0.4, AY - 220 * U), (W * 0.6, AY + 200 * U), S]
    dashed(ctx, pts)
    phone(ctx, P[0], P[1], 1.25 * U, t, "play")
    glow(ctx, S[0], S[1], 200 * U, CYAN, 0.18)
    server(ctx, S[0], S[1], 1.2 * U, t)
    go = prog(t, 0.8, 1.2)
    for i in range(5):
        k = ((t - 0.8) * 0.35 + i * 0.2) % 1.0
        if go: packet(ctx, *path_pt(pts, k), 0.8 * U, GOLD, go)
        k2 = ((t - 0.8) * 0.35 + i * 0.2 + 0.1) % 1.0
        if go: packet(ctx, *path_pt(pts, 1 - k2), 0.8 * U, CYAN, go)
    mid = path_pt(pts, 0.5)
    a = prog(t, 2.0, 2.8)
    if VERT:
        rrect(ctx, CX - 210 * U, H * 0.355 - 36 * U, 420 * U, 72 * U, 36 * U); rgba(ctx, NAVY, 0.85 * a); ctx.fill()
        text(ctx, "THOUSANDS OF KM", CX, H * 0.355, 44 * U, GOLD, a)
        text(ctx, "< 1 SECOND", CX, H * 0.645, 54 * U, WHITE, prog(t, 4.5, 5.2))
    else:
        text(ctx, "THOUSANDS OF KM", CX, AY - 300 * U, 50 * U, GOLD, a)
        text(ctx, "< 1 SECOND", CX, AY + 300 * U, 54 * U, WHITE, prog(t, 4.5, 5.2))
    q = prog(t, d - 2.6, d - 1.8)
    if q: text(ctx, "?", mid[0], mid[1], 200 * U, GOLD, q)


NODES = None
def net_nodes():
    random.seed(21)
    return [(random.random(), random.random()) for _ in range(46)]


def network(ctx, t, x0, y0, x1, y1, a=1.0, n=46):
    pts = [(x0 + (x1 - x0) * px, y0 + (y1 - y0) * py) for px, py in net_nodes()[:n]]
    ctx.set_line_width(2 * U)
    for i, p in enumerate(pts):
        for j in range(i + 1, len(pts)):
            q = pts[j]
            dd = math.hypot(p[0] - q[0], p[1] - q[1])
            if dd < 260 * U:
                rgba(ctx, CYAN, a * 0.22 * (1 - dd / (260 * U))); ctx.move_to(*p); ctx.line_to(*q); ctx.stroke()
    for i, p in enumerate(pts):
        pu = 0.5 + 0.5 * math.sin(t * 2 + i)
        glow(ctx, p[0], p[1], 22 * U, GOLD, 0.35 * a * pu)
        circle(ctx, p[0], p[1], 5 * U, GOLD, a * (0.6 + 0.4 * pu))


def sc_title(ctx, t, d):
    bg(ctx, t, 0.4)
    network(ctx, t, 0, 0, W, H * 0.78, 0.55)
    a = prog(t, 0, 0.5)
    y = H * 0.4 if VERT else H * 0.42
    sz = 96 * U if VERT else 100 * U
    rrect(ctx, CX - (480 if VERT else 820) * U, y - 110 * U, (960 if VERT else 1640) * U, 250 * U, 30 * U); rgba(ctx, NAVY, 0.7 * a); ctx.fill()
    if VERT:
        text(ctx, "HOW DOES THE", CX, y - 40 * U, 84 * U, WHITE, a)
        text(ctx, "INTERNET WORK?", CX, y + 70 * U, 96 * U, GOLD, a)
    else:
        text(ctx, "HOW DOES THE INTERNET", CX, y - 40 * U, sz * 0.9, WHITE, a)
        text(ctx, "ACTUALLY WORK?", CX, y + 70 * U, sz * 0.9, GOLD, a)


def sc_packets(ctx, t, d):
    bg(ctx, t, 0.4)
    split = prog(t, 2.0, 4.0)
    fx, fy = (CX, H * 0.3) if VERT else (W * 0.27, AY)
    fw, fh = (560 * U, 330 * U)
    cols, rows = 6, 4
    tw, th = fw / cols, fh / rows
    # destination row of packets
    for r in range(rows):
        for c in range(cols):
            i = r * cols + c
            sx, sy = fx - fw / 2 + (c + 0.5) * tw, fy - fh / 2 + (r + 0.5) * th
            if VERT:
                dx, dy = CX - 410 * U + (i % 8) * 117 * U, H * 0.52 + (i // 8) * 62 * U
            else:
                dx, dy = W * 0.56 + (i % 6) * 96 * U, AY - 150 * U + (i // 6) * 70 * U
            k = prog(t, 2.0 + i * 0.06, 3.4 + i * 0.06)
            x, y = sx + (dx - sx) * k, sy + (dy - sy) * k - math.sin(k * math.pi) * 80 * U
            if k < 0.05:
                hue = mix((0.15, 0.4, 0.7), (0.9, 0.55, 0.3), (c + r) / 8)
                ctx.rectangle(sx - tw / 2, sy - th / 2, tw + 1, th + 1); rgba(ctx, hue); ctx.fill()
            else:
                packet(ctx, x, y, 1.15 * U, GOLD, 1, str(i + 1))
    if split < 0.05:
        ctx.move_to(fx - 40 * U, fy - 50 * U); ctx.line_to(fx + 55 * U, fy); ctx.line_to(fx - 40 * U, fy + 50 * U); ctx.close_path(); rgba(ctx, WHITE, 0.9); ctx.fill()
    z = prog(t, 6.5, 7.5)
    rrect(ctx, fx - fw / 2 - 8 * U, fy - fh / 2 - 8 * U, fw + 16 * U, fh + 16 * U, 14 * U); rgba(ctx, GOLD, (1 - 0.7 * split) * (1 - z)); ctx.set_line_width(4 * U); ctx.stroke()
    text(ctx, "YOUR VIDEO", fx, fy - fh / 2 - 45 * U, 38 * U, WHITE, (1 - 0.5 * split) * (1 - z))
    # zoom on one label
    if z:
        lx, ly = (CX, H * 0.3) if VERT else (W * 0.27, AY)
        lw, lh = 620 * U, 300 * U
        ctx.save(); ctx.translate(lx, ly); ctx.scale(0.6 + 0.4 * z, 0.6 + 0.4 * z); ctx.translate(-lx, -ly)
        rrect(ctx, lx - lw / 2, ly - lh / 2, lw, lh, 18 * U); rgba(ctx, (0.1, 0.22, 0.4), z); ctx.fill()
        rrect(ctx, lx - lw / 2, ly - lh / 2, lw, 60 * U, 18 * U); rgba(ctx, GOLD, z); ctx.fill()
        text(ctx, "PACKET #7", lx, ly - lh / 2 + 30 * U, 34 * U, NAVY, z)
        rows_ = [("FROM", "203.0.113.7"), ("TO", "198.51.100.24"), ("ORDER", "7 of 24")]
        for i, (k_, v) in enumerate(rows_):
            yy = ly - lh / 2 + 105 * U + i * 62 * U
            text(ctx, k_, lx - lw / 2 + 40 * U, yy, 32 * U, GOLD, z * prog(t, 7 + i * 0.6, 7.5 + i * 0.6), True, "l")
            text(ctx, v, lx + lw / 2 - 40 * U, yy, 32 * U, WHITE, z * prog(t, 7 + i * 0.6, 7.5 + i * 0.6), False, "r")
        ctx.restore()
    chip(ctx, "STEP 1 · PACKETS", t)


def sc_address(ctx, t, d):
    bg(ctx, t, 0.4)
    if VERT:
        items = [("phone", CX - 270 * U, H * 0.3, "192.0.2.15"), ("laptop", CX + 250 * U, H * 0.32, "192.0.2.88"),
                 ("server", CX, H * 0.55, "203.0.113.7")]
    else:
        items = [("phone", W * 0.2, AY, "192.0.2.15"), ("laptop", W * 0.5, AY + 60 * U, "192.0.2.88"), ("server", W * 0.8, AY, "203.0.113.7")]
    for i, (kind, x, y, ip) in enumerate(items):
        a = prog(t, 0.3 + i * 0.5, 0.9 + i * 0.5)
        glow(ctx, x, y, 170 * U, CYAN, 0.12 * a)
        if kind == "phone": phone(ctx, x, y, 1.0 * U)
        elif kind == "laptop": laptop(ctx, x, y + 40 * U, 1.0 * U)
        else: server(ctx, x, y, 0.95 * U, t)
        # address tag, typed out
        n = int(len(ip) * prog(t, 2.5 + i * 0.9, 3.6 + i * 0.9))
        ty = y + (175 if VERT else 190) * U
        if kind == "laptop" and VERT: ty = y + 150 * U
        if n:
            font(ctx, 34 * U); tw = ctx.text_extents(ip).width + 40 * U
            rrect(ctx, x - tw / 2, ty - 30 * U, tw, 60 * U, 14 * U); rgba(ctx, GOLD, 0.95); ctx.fill()
            text(ctx, ip[:n], x - tw / 2 + 20 * U, ty, 34 * U, NAVY, 1, True, "l")
    a = prog(t, 6.5, 7.3)
    text(ctx, "LIKE A POSTAL ADDRESS FOR EVERY DEVICE", CX, (H * 0.665 if VERT else AY - 260 * U), (34 if VERT else 42) * U, WHITE, a)
    chip(ctx, "STEP 2 · IP ADDRESSES", t)


def book(ctx, x, y, s, t, a=1.0):
    w, h = 300 * s, 210 * s
    open_ = 0.5 + 0.5 * math.sin(t * 1.5)
    glow(ctx, x, y, 260 * s, GOLD, 0.2 * a)
    for side in (-1, 1):
        ctx.move_to(x, y + h / 2); ctx.line_to(x + side * w / 2, y + h / 2 - 20 * s)
        ctx.line_to(x + side * w / 2, y - h / 2 - 20 * s); ctx.line_to(x, y - h / 2); ctx.close_path()
        rgba(ctx, MOON, a); ctx.fill()
        for k in range(5):
            yy = y - h / 2 + 30 * s + k * 32 * s
            ctx.move_to(x + side * 20 * s, yy); ctx.line_to(x + side * (w / 2 - 22 * s), yy - 12 * s)
            rgba(ctx, GREY, a); ctx.set_line_width(4 * s); ctx.stroke()
    ctx.move_to(x, y - h / 2 - 4 * s); ctx.line_to(x, y + h / 2 + 4 * s); rgba(ctx, GOLD, a); ctx.set_line_width(5 * s); ctx.stroke()
    text(ctx, "DNS", x, y + h / 2 + 50 * s, 48 * s, GOLD, a)


def sc_dns(ctx, t, d):
    bg(ctx, t, 0.4)
    name = "www.example.com"
    ip = "203.0.113.7"
    if VERT:
        bx, by = CX, H * 0.23; kx, ky = CX, H * 0.42; ox, oy = CX, H * 0.62
    else:
        bx, by = W * 0.2, AY; kx, ky = CX, AY - 30 * U; ox, oy = W * 0.8, AY
    # search bar with typed name
    n = int(len(name) * prog(t, 0.5, 3.0))
    bw = 470 * U
    rrect(ctx, bx - bw / 2, by - 40 * U, bw, 80 * U, 40 * U); rgba(ctx, WHITE, 0.95); ctx.fill()
    text(ctx, name[:n] + ("|" if int(t * 2) % 2 else ""), bx - bw / 2 + 36 * U, by, 34 * U, NAVY, 1, False, "l")
    text(ctx, "YOU TYPE A NAME", bx, by - 80 * U, 30 * U, WHITE, 0.8)
    book(ctx, kx, ky, 1.0 * U, t)
    # arrows
    a1 = prog(t, 3.0, 4.0); a2 = prog(t, 5.0, 6.0)
    def arrow(p, q, k):
        if not k: return
        ex, ey = p[0] + (q[0] - p[0]) * k, p[1] + (q[1] - p[1]) * k
        rgba(ctx, GOLD); ctx.set_line_width(6 * U); ctx.move_to(*p); ctx.line_to(ex, ey); ctx.stroke()
        ang = math.atan2(q[1] - p[1], q[0] - p[0])
        ctx.move_to(ex, ey); ctx.line_to(ex - 26 * U * math.cos(ang - 0.5), ey - 26 * U * math.sin(ang - 0.5))
        ctx.line_to(ex - 26 * U * math.cos(ang + 0.5), ey - 26 * U * math.sin(ang + 0.5)); ctx.close_path(); ctx.fill()
    if VERT:
        arrow((CX, by + 55 * U), (CX, ky - 150 * U), a1); arrow((CX, ky + 170 * U), (CX, oy - 55 * U), a2)
    else:
        arrow((bx + bw / 2 + 20 * U, by), (kx - 190 * U, by), a1); arrow((kx + 190 * U, oy), (ox - 200 * U, oy), a2)
    k = prog(t, 6.0, 6.8)
    if k:
        font(ctx, 40 * U); tw = ctx.text_extents(ip).width + 60 * U
        rrect(ctx, ox - tw / 2, oy - 40 * U, tw, 80 * U, 20 * U); rgba(ctx, GOLD, k); ctx.fill()
        text(ctx, ip, ox, oy, 40 * U, NAVY, k)
        text(ctx, "THE ADDRESS", ox, oy - 80 * U if not VERT else oy + 80 * U, 30 * U, WHITE, 0.8 * k)
    m = prog(t, 8.5, 9.2)
    if m: text(ctx, "≈ A FEW MILLISECONDS", CX, (H * 0.13 if not VERT else H * 0.665), 40 * U, CYAN, m) if VERT else text(ctx, "≈ A FEW MILLISECONDS", W * 0.8, AY + 160 * U, 36 * U, CYAN, m)
    chip(ctx, "STEP 3 · DNS", t)


def router_grid():
    if VERT:
        cols, rows = 3, 5
        xs = [CX - 330 * U + i * 330 * U for i in range(cols)]
        ys = [H * 0.16 + j * H * 0.12 for j in range(rows)]
    else:
        cols, rows = 6, 3
        xs = [W * 0.1 + i * W * 0.16 for i in range(cols)]
        ys = [AY - 230 * U + j * 230 * U for j in range(rows)]
    return xs, ys


def sc_routers(ctx, t, d):
    bg(ctx, t, 0.35)
    xs, ys = router_grid()
    nodes = {(i, j): (xs[i], ys[j]) for i in range(len(xs)) for j in range(len(ys))}
    ctx.set_line_width(3 * U)
    for (i, j), p in nodes.items():
        for q in [(i + 1, j), (i, j + 1)]:
            if q in nodes:
                rgba(ctx, GREY, 0.35); ctx.move_to(*p); ctx.line_to(*nodes[q]); ctx.stroke()
    # two routes
    if VERT:
        r1 = [(1, 0), (0, 0), (0, 1), (0, 2), (0, 3), (1, 3), (1, 4)]
        r2 = [(1, 0), (2, 0), (2, 1), (2, 2), (1, 2), (1, 3), (1, 4)]
        r2 = [(1, 0), (1, 1), (2, 1), (2, 2), (2, 3), (2, 4), (1, 4)]
    else:
        r1 = [(0, 1), (1, 1), (1, 0), (2, 0), (3, 0), (4, 0), (4, 1), (5, 1)]
        r2 = [(0, 1), (0, 2), (1, 2), (2, 2), (3, 2), (3, 1), (4, 1), (5, 1)]
    show = prog(t, 3.0, 4.0)
    for r, col in [(r1, GOLD), (r2, CYAN)]:
        if r is r2 and t < 8: continue
        pts = [nodes[n] for n in r]
        rgba(ctx, col, 0.7 * show); ctx.set_line_width(7 * U); ctx.move_to(*pts[0])
        for p in pts[1:]: ctx.line_to(*p)
        ctx.stroke()
    for (i, j), p in nodes.items():
        router(ctx, p[0], p[1], 0.85 * U, t, GOLD if (i, j) in (r1[0], r1[-1]) else GREY)
    a, b = nodes[r1[0]], nodes[r1[-1]]
    if VERT:
        text(ctx, "YOU", a[0], a[1] - 75 * U, 30 * U, WHITE)
        text(ctx, "SERVER", b[0], b[1] + 70 * U, 30 * U, WHITE)
    else:
        text(ctx, "YOU", a[0], a[1] - 80 * U, 32 * U, WHITE)
        text(ctx, "SERVER", b[0], b[1] - 80 * U, 32 * U, WHITE)
    # packets hopping
    for i in range(3):
        k = ((t - 3.5) * 0.18 + i * 0.33) % 1.0
        if t > 3.5: packet(ctx, *path_pt([nodes[n] for n in r1], k), 0.8 * U, GOLD)
        if t > 8.5:
            k2 = ((t - 8.5) * 0.18 + i * 0.33) % 1.0
            packet(ctx, *path_pt([nodes[n] for n in r2], k2), 0.8 * U, CYAN)
    if t > 8.5:
        text(ctx, "DIFFERENT ROADS, SAME DESTINATION", CX, (H * 0.665 if VERT else H * 0.12), (34 if VERT else 40) * U, CYAN, prog(t, 8.5, 9.3)) if VERT else \
            text(ctx, "DIFFERENT ROADS, SAME DESTINATION", W * 0.62, H * 0.1, 38 * U, CYAN, prog(t, 8.5, 9.3))
    chip(ctx, "STEP 4 · ROUTERS", t)


def fish(ctx, x, y, s, c, a):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s * 0.55)
    ctx.arc(0, 0, 1, 0, 2 * math.pi); ctx.restore(); rgba(ctx, c, a); ctx.fill()
    ctx.move_to(x - s * 0.9, y); ctx.line_to(x - s * 1.6, y - s * 0.5); ctx.line_to(x - s * 1.6, y + s * 0.5); ctx.close_path(); ctx.fill()


def seafloor_pts():
    if VERT:
        top, floor_ = H * 0.32, H * 0.6
    else:
        top, floor_ = H * 0.3, H * 0.7
    return top, floor_


def sc_cables(ctx, t, d):
    vgrad(ctx, (0.03, 0.05, 0.12), (0.06, 0.09, 0.2), 0, H * 0.3)
    stars(ctx, t, 0.4)
    top, floor_ = seafloor_pts()
    # satellite (not the main route)
    sx, sy = (CX + 250 * U, H * 0.2) if VERT else (W * 0.62, H * 0.15)
    sa = prog(t, 2.5, 3.3)
    ctx.save(); ctx.translate(sx, sy); ctx.rotate(0.3)
    ctx.rectangle(-30 * U, -18 * U, 60 * U, 36 * U); rgba(ctx, GREY, sa); ctx.fill()
    for side in (-1, 1):
        ctx.rectangle(side * 40 * U - (55 * U if side < 0 else 0), -14 * U, 55 * U, 28 * U); rgba(ctx, (0.2, 0.4, 0.8), sa); ctx.fill()
    ctx.restore()
    if t > 4.5:
        k = prog(t, 4.5, 5.0)
        ctx.set_line_width(8 * U); rgba(ctx, CORAL, k)
        ctx.move_to(sx - 80 * U, sy - 60 * U); ctx.line_to(sx + 80 * U, sy + 60 * U); ctx.stroke()
    # ocean
    g = cairo.LinearGradient(0, top, 0, H); g.add_color_stop_rgb(0, 0.08, 0.35, 0.62); g.add_color_stop_rgb(1, 0.01, 0.06, 0.16)
    ctx.set_source(g); ctx.move_to(0, top)
    for i in range(41): ctx.line_to(W * i / 40, top + 6 * U * math.sin(i * 0.8 + t * 2))
    ctx.line_to(W, H); ctx.line_to(0, H); ctx.close_path(); ctx.fill()
    # land on both sides + floor
    lw = W * (0.14 if not VERT else 0.08)
    rgba(ctx, (0.18, 0.32, 0.25))
    ctx.move_to(0, top - 30 * U); ctx.line_to(lw, top - 30 * U); ctx.line_to(lw + 60 * U, top + 30 * U); ctx.line_to(lw * 1.8, floor_); ctx.line_to(0, floor_); ctx.close_path(); ctx.fill()
    ctx.move_to(W, top - 30 * U); ctx.line_to(W - lw, top - 30 * U); ctx.line_to(W - lw - 60 * U, top + 30 * U); ctx.line_to(W - lw * 1.8, floor_); ctx.line_to(W, floor_); ctx.close_path(); ctx.fill()
    rgba(ctx, (0.35, 0.3, 0.22))
    ctx.move_to(0, H); ctx.line_to(0, floor_)
    for i in range(31): ctx.line_to(W * i / 30, floor_ + 10 * U * math.sin(i * 1.3))
    ctx.line_to(W, H); ctx.close_path()
    g = cairo.LinearGradient(0, floor_, 0, H); g.add_color_stop_rgb(0, 0.35, 0.3, 0.22); g.add_color_stop_rgb(1, 0.08, 0.07, 0.08)
    ctx.set_source(g); ctx.fill()
    random.seed(9)
    for i in range(14):
        rx = W * random.random(); ry = floor_ + (H - floor_) * random.uniform(0.08, 0.5)
        ctx.save(); ctx.translate(rx, ry); ctx.scale(random.uniform(20, 45) * U, random.uniform(10, 20) * U)
        ctx.arc(0, 0, 1, math.pi, 2 * math.pi); ctx.restore(); rgba(ctx, (0.22, 0.19, 0.16)); ctx.fill()
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    for i in range(9):
        sx_ = W * (0.12 + i * 0.1); ctx.set_line_width(6 * U); rgba(ctx, (0.2, 0.55, 0.4), 0.8)
        ctx.move_to(sx_, floor_ + 6 * U)
        for k in range(1, 6): ctx.line_to(sx_ + 10 * U * math.sin(t * 1.5 + k + i), floor_ + 6 * U - k * 16 * U)
        ctx.stroke()
    # the cable
    cab = [(lw * 0.6, top - 30 * U), (lw + 40 * U, top + 20 * U), (lw * 1.8, floor_ - 4 * U), (W - lw * 1.8, floor_ - 4 * U),
           (W - lw - 40 * U, top + 20 * U), (W - lw * 0.6, top - 30 * U)]
    rgba(ctx, (0.08, 0.08, 0.1)); ctx.set_line_width(12 * U); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.move_to(*cab[0])
    for p in cab[1:]: ctx.line_to(*p)
    ctx.stroke()
    on = prog(t, 0.5, 1.5)
    for i in range(14):
        k = (t * 0.12 + i / 14) % 1.0
        x, y = path_pt(cab, k)
        glow(ctx, x, y, 40 * U, GOLD, 0.6 * on); circle(ctx, x, y, 5 * U, WHITE, on)
    # fish
    for i in range(5):
        fx = (W * (0.2 + i * 0.17) + t * 40 * U * (1 + i % 2)) % W
        fy = top + (floor_ - top) * (0.25 + 0.12 * (i % 3))
        fish(ctx, fx, fy, 22 * U, (0.6, 0.85, 1.0), 0.35)
    a = prog(t, 7.0, 7.8)
    if VERT:
        text(ctx, "UNDER THE OCEAN", CX, top + (floor_ - top) * 0.45, 56 * U, GOLD, a)
        text(ctx, "THOUSANDS OF KM OF CABLE", CX, floor_ + 60 * U, 34 * U, WHITE, prog(t, 10, 10.8))
    else:
        text(ctx, "UNDER THE OCEAN", CX, top + (floor_ - top) * 0.42, 66 * U, GOLD, a)
        text(ctx, "THOUSANDS OF KILOMETERS OF CABLE", CX, top + (floor_ - top) * 0.62, 36 * U, WHITE, prog(t, 10, 10.8))
    chip(ctx, "STEP 5 · UNDERSEA CABLES", t)


def sc_light(ctx, t, d):
    bg(ctx, t, 0.3)
    # cable cross-section
    cx_, cy_ = (CX, H * 0.27) if VERT else (W * 0.22, AY)
    R = 200 * U
    for r, c in [(1.0, (0.08, 0.08, 0.1)), (0.85, (0.3, 0.32, 0.38)), (0.7, (0.75, 0.55, 0.25)), (0.55, (0.14, 0.18, 0.32)), (0.3, (0.6, 0.65, 0.75))]:
        circle(ctx, cx_, cy_, R * r, c)
    for i in range(8):
        ang = i / 8 * 2 * math.pi
        x, y = cx_ + math.cos(ang) * R * 0.17, cy_ + math.sin(ang) * R * 0.17
        pu = 0.5 + 0.5 * math.sin(t * 6 + i)
        glow(ctx, x, y, 22 * U, GOLD, 0.6 * pu); circle(ctx, x, y, 7 * U, WHITE)
    text(ctx, "GLASS FIBERS", cx_, cy_ + R + 45 * U, 32 * U, WHITE, 0.85)
    # long fiber with zigzag light
    if VERT:
        x0, x1, fy, fh = 60 * U, W - 60 * U, H * 0.52, 90 * U
    else:
        x0, x1, fy, fh = W * 0.4, W * 0.95, AY - 40 * U, 110 * U
    rrect(ctx, x0, fy - fh / 2, x1 - x0, fh, fh / 2); rgba(ctx, (0.5, 0.75, 0.95), 0.18); ctx.fill()
    rrect(ctx, x0, fy - fh / 2, x1 - x0, fh, fh / 2); rgba(ctx, (0.6, 0.85, 1.0), 0.6); ctx.set_line_width(3 * U); ctx.stroke()
    # zigzag (total internal reflection)
    zz = [(x0 + 20 * U + i * 70 * U, fy + (fh / 2 - 14 * U) * (1 if i % 2 else -1)) for i in range(int((x1 - x0 - 40 * U) / (70 * U)) + 1)]
    ctx.set_line_width(3 * U); rgba(ctx, GOLD, 0.35); ctx.move_to(*zz[0])
    for p in zz[1:]: ctx.line_to(*p)
    ctx.stroke()
    for i in range(4):
        k = (t * 0.25 + i * 0.25) % 1.0
        x, y = path_pt(zz, k)
        glow(ctx, x, y, 34 * U, GOLD, 0.8); circle(ctx, x, y, 7 * U, WHITE)
    # blinking bits
    bits = "1011001110100101"
    bx = (x0 + x1) / 2
    text(ctx, " ".join(bits[(int(t * 4) + i) % len(bits)] for i in range(12)), bx, fy - fh / 2 - 50 * U, 34 * U, CYAN, prog(t, 3.0, 3.8), False)
    a = prog(t, 8.0, 8.8)
    if VERT: text(ctx, "≈ 200,000 KM PER SECOND", CX, H * 0.64, 50 * U, GOLD, a)
    else: text(ctx, "≈ 200,000 KM PER SECOND", (x0 + x1) / 2, fy + fh / 2 + 110 * U, 58 * U, GOLD, a)
    chip(ctx, "DATA = LIGHT", t)


def sc_servers(ctx, t, d):
    bg(ctx, t, 0.3)
    if VERT:
        racks = [(CX - 300 * U + i * 200 * U, H * 0.24) for i in range(4)]; s = 0.8 * U
        P = (CX, H * 0.51)
    else:
        racks = [(W * 0.08 + i * 190 * U, AY - 40 * U) for i in range(4)]; s = 1.1 * U
        P = (W * 0.86, AY - 40 * U)
    for x, y in racks:
        server(ctx, x, y, s, t, 5)
    text(ctx, "DATA CENTER", racks[0][0] + (racks[-1][0] - racks[0][0]) / 2,
         racks[0][1] - (5 * 62 * s) / 2 - 40 * U, 34 * U, WHITE, 0.85)
    # slots on the phone side
    n = 8
    if VERT:
        slots = [(CX - 434 * U + i * 124 * U, H * 0.62) for i in range(n)]
    else:
        slots = [(W * 0.4 + i * 112 * U, AY + 250 * U) for i in range(n)]
    for i, (x, y) in enumerate(slots):
        rrect(ctx, x - 48 * U, y - 34 * U, 96 * U, 68 * U, 10 * U); rgba(ctx, WHITE, 0.25); ctx.set_line_width(2 * U); ctx.stroke()
    order = [2, 0, 5, 1, 7, 3, 6, 4]
    resend = prog(t, 10.5, 12.0)
    for j, i in enumerate(order):
        k = prog(t, 1.0 + j * 0.6, 2.2 + j * 0.6)
        if i == 4: k = resend
        if k <= 0: continue
        src = (racks[-1][0] + 80 * U, racks[-1][1]) if not VERT else (racks[-1][0], racks[-1][1] + 180 * U)
        x = src[0] + (slots[i][0] - src[0]) * k; y = src[1] + (slots[i][1] - src[1]) * k - math.sin(k * math.pi) * 90 * U
        packet(ctx, x, y, 1.35 * U, CYAN if i == 4 else GOLD, 1, str(i + 1))
    if t > 7.5 and resend < 0.3:
        x, y = slots[4]
        text(ctx, "?", x, y, 64 * U, CORAL, prog(t, 7.5, 8.0))
    if t > 9.5:
        x, y = slots[4]
        text(ctx, "RESEND #5", x, y + (-80 if VERT else 85) * U, 34 * U, CYAN, prog(t, 9.5, 10.0))
    phone(ctx, P[0], P[1], (0.9 if VERT else 1.4) * U, t, "play" if resend >= 1 else None)
    if VERT:
        pass
    chip(ctx, "BACK TO YOU", t)


def sc_history(ctx, t, d):
    bg(ctx, t, 0.4)
    if VERT:
        xs = [H * 0.2, H * 0.4, H * 0.6]; lx = CX - 250 * U
        rgba(ctx, GOLD, 0.6); ctx.set_line_width(5 * U); ctx.move_to(lx, xs[0] - 60 * U); ctx.line_to(lx, xs[2] + 60 * U); ctx.stroke()
    else:
        xs = [W * 0.2, W * 0.5, W * 0.8]; ly = AY + 150 * U
        rgba(ctx, GOLD, 0.6); ctx.set_line_width(5 * U); ctx.move_to(xs[0] - 150 * U, ly); ctx.line_to(xs[2] + 150 * U, ly); ctx.stroke()
    items = [("1969", "ARPANET"), ("1989", "THE WEB, AT CERN"), ("TODAY", "BILLIONS OF DEVICES")]
    starts = [2.5, 6.0, 9.5]
    for i, (yr, lab) in enumerate(items):
        a = prog(t, starts[i], starts[i] + 0.8)
        if VERT: px, py = lx, xs[i]; ix, iy = CX + 170 * U, xs[i]
        else: px, py = xs[i], ly; ix, iy = xs[i], AY - 120 * U
        circle(ctx, px, py, 16 * U, GOLD, max(0.3, a))
        if not a: continue
        if VERT:
            text(ctx, yr, px + 50 * U, py - 30 * U, 52 * U, GOLD, a, True, "l")
            text(ctx, lab, px + 50 * U, py + 30 * U, 30 * U, WHITE, a, False, "l")
            ix, iy = CX + 330 * U, py
        else:
            text(ctx, yr, px, py + 60 * U, 54 * U, GOLD, a)
            text(ctx, lab, px, py + 115 * U, 30 * U, WHITE, a, False)
        # icons
        if i == 0:
            n1, n2 = (ix - 70 * U, iy), (ix + 70 * U, iy)
            if VERT: n1, n2 = (ix, iy - 70 * U), (ix, iy + 70 * U)
            rgba(ctx, WHITE, a); ctx.set_line_width(4 * U); ctx.move_to(*n1); ctx.line_to(*n2); ctx.stroke()
            for n in (n1, n2): circle(ctx, n[0], n[1], 20 * U, GOLD, a)
            k = (t * 0.5) % 1
            circle(ctx, n1[0] + (n2[0] - n1[0]) * k, n1[1] + (n2[1] - n1[1]) * k, 8 * U, WHITE, a)
        elif i == 1:
            glow(ctx, ix, iy, 120 * U, CYAN, 0.25 * a)
            circle(ctx, ix, iy, 75 * U, (0.12, 0.3, 0.55), a)
            ctx.set_line_width(3 * U); rgba(ctx, CYAN, a)
            ctx.arc(ix, iy, 75 * U, 0, 2 * math.pi); ctx.stroke()
            ctx.save(); ctx.translate(ix, iy); ctx.scale(0.45, 1); ctx.arc(0, 0, 75 * U, 0, 2 * math.pi); ctx.restore(); ctx.stroke()
            ctx.move_to(ix - 75 * U, iy); ctx.line_to(ix + 75 * U, iy); ctx.stroke()
            text(ctx, "www", ix, iy, 40 * U, WHITE, a)
        else:
            random.seed(4)
            for j in range(40):
                ang = random.random() * 6.28; rr = random.random() ** 0.5 * 100 * U
                x, y = ix + math.cos(ang) * rr, iy + math.sin(ang) * rr
                circle(ctx, x, y, 5 * U, GOLD, a * (0.5 + 0.5 * math.sin(t * 3 + j)))
    chip(ctx, "A SHORT HISTORY", t)


def sc_outro(ctx, t, d):
    bg(ctx, t, 0.5)
    network(ctx, t, 0, 0, W, H * 0.78, 0.25)
    yo = -80 * U if not VERT else -200 * U
    glow(ctx, CX, CY + yo - 190 * U, 110 * U, GOLD, 0.5)
    for i in range(6):
        ang = i / 6 * 2 * math.pi + t * 0.5
        x, y = CX + math.cos(ang) * 60 * U, CY + yo - 190 * U + math.sin(ang) * 60 * U
        rgba(ctx, GOLD, 0.7); ctx.set_line_width(3 * U); ctx.move_to(CX, CY + yo - 190 * U); ctx.line_to(x, y); ctx.stroke()
        circle(ctx, x, y, 9 * U, GOLD)
    circle(ctx, CX, CY + yo - 190 * U, 16 * U, WHITE)
    text(ctx, "FACTORA", CX, CY + yo, 140 * U, WHITE, prog(t, 0, 0.6))
    text(ctx, "fascinating facts, explained", CX, CY + yo + 100 * U, 38 * U, GOLD, prog(t, 0.4, 1.0), False)
    k = prog(t, d * 0.62, d * 0.72)
    if k:
        bw, bh = 520 * U, 110 * U
        pop = 1 + 0.05 * math.sin(t * 6)
        ctx.save(); ctx.translate(CX, CY + yo + 260 * U); ctx.scale(pop * k, pop * k)
        rrect(ctx, -bw / 2, -bh / 2, bw, bh, 22 * U); rgba(ctx, (0.85, 0.12, 0.12)); ctx.fill()
        text(ctx, "SUBSCRIBE", 0, 0, 52 * U, WHITE)
        ctx.restore()
    q = prog(t, d * 0.33, d * 0.42)
    if q and k < 1: text(ctx, "Did you know it goes under the sea?", CX, CY + yo + 260 * U, (40 if not VERT else 36) * U, WHITE, q * (1 - k))


SHORT_SCENES = ["hook", "cables", "light", "outro"]

SCENES = dict(hook=sc_hook, title=sc_title, packets=sc_packets, address=sc_address, dns=sc_dns, routers=sc_routers,
              cables=sc_cables, light=sc_light, servers=sc_servers, history=sc_history, outro=sc_outro)


def thumbnail(c):
    """1280x720 thumbnail: undersea cable glowing on the right, text on the left."""
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, .08, .11, .26); g.add_color_stop_rgb(1, .02, .03, .08); c.set_source(g); c.paint()
    random.seed(1)
    for _ in range(120):
        c.arc(random.random() * W, random.random() * H * 0.35, random.uniform(.5, 1.8), 0, 6.3); c.set_source_rgba(1, 1, 1, random.uniform(.3, .9)); c.fill()
    top = 250
    g = cairo.LinearGradient(0, top, 0, H); g.add_color_stop_rgb(0, 0.08, 0.35, 0.62); g.add_color_stop_rgb(1, 0.01, 0.05, 0.14)
    c.set_source(g); c.rectangle(0, top, W, H - top); c.fill()
    # sea floor
    c.set_source_rgb(0.3, 0.26, 0.2); c.move_to(0, H)
    for i in range(21): c.line_to(W * i / 20, 600 + 12 * math.sin(i * 1.3))
    c.line_to(W, H); c.close_path(); c.fill()
    # cable rising to the right
    pts = [(560, 596), (900, 596), (1080, 420), (1180, 240), (1280, 220)]
    c.set_line_width(16); c.set_source_rgb(0.06, 0.06, 0.08); c.set_line_join(cairo.LINE_JOIN_ROUND)
    c.move_to(*pts[0])
    for p in pts[1:]: c.line_to(*p)
    c.stroke()
    for i in range(10):
        x, y = path_pt(pts, i / 10 + 0.03)
        rg = cairo.RadialGradient(x, y, 0, x, y, 50); rg.add_color_stop_rgba(0, 1, .8, .33, .9); rg.add_color_stop_rgba(1, 1, .8, .33, 0)
        c.set_source(rg); c.arc(x, y, 50, 0, 6.3); c.fill()
        c.arc(x, y, 7, 0, 6.3); c.set_source_rgb(1, 1, 1); c.fill()
    # cross-section bubble
    bx, by, R = 1010, 330, 105
    c.arc(bx, by, R + 8, 0, 6.3); c.set_source_rgb(1, .8, .33); c.fill()
    for r, col in [(1.0, (0.08, 0.08, 0.1)), (0.8, (0.3, 0.32, 0.38)), (0.62, (0.75, 0.55, 0.25)), (0.45, (0.14, 0.18, 0.32))]:
        c.arc(bx, by, R * r, 0, 6.3); c.set_source_rgb(*col); c.fill()
    for i in range(8):
        ang = i / 8 * 6.283
        x, y = bx + math.cos(ang) * R * 0.22, by + math.sin(ang) * R * 0.22
        rg = cairo.RadialGradient(x, y, 0, x, y, 22); rg.add_color_stop_rgba(0, 1, .9, .5, .9); rg.add_color_stop_rgba(1, 1, .9, .5, 0)
        c.set_source(rg); c.arc(x, y, 22, 0, 6.3); c.fill()
        c.arc(x, y, 6, 0, 6.3); c.set_source_rgb(1, 1, 1); c.fill()
    thumb_text(c, "THE INTERNET IS", "UNDER THE SEA", "HOW IT WORKS")
