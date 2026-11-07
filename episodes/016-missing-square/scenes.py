# Episode 016 (Short only) - "Where does the missing square come from?" (missing square puzzle)
# Executed inside engine/render.py (helpers available). Vertical layout. Original vector illustration.

BLUE = (0.35, 0.68, 1.0)
GREEN = (0.42, 0.88, 0.58)
GRIDC = (0.45, 0.55, 0.85)

# pieces in grid coordinates (x right, y up), configuration A, and translation to configuration B
PIECES = [
    ("red",    CORAL, [(0, 0), (8, 0), (8, 3)],                                   (5, 2)),
    ("blue",   BLUE,  [(8, 3), (13, 3), (13, 5)],                                 (-8, -3)),
    ("orange", GOLD,  [(8, 0), (13, 0), (13, 1), (11, 1), (11, 2), (8, 2)],       (-3, 0)),
    ("green",  GREEN, [(8, 2), (11, 2), (11, 1), (13, 1), (13, 3), (8, 3)],       (0, -1)),
]

def geom():
    c = (W * 0.9) / 13.0
    x0 = CX - 6.5 * c
    y0 = H * 0.5
    return c, x0, y0

def P(gx, gy):
    c, x0, y0 = geom()
    return x0 + gx * c, y0 - gy * c

def bg(ctx, t):
    vgrad(ctx, (0.06, 0.09, 0.21), NAVY); stars(ctx, t, 0.3)

def grid(ctx, a=1.0):
    c, x0, y0 = geom()
    ctx.set_line_width(1.5 * U); rgba(ctx, GRIDC, 0.28 * a)
    for i in range(14):
        ctx.move_to(x0 + i * c, y0); ctx.line_to(x0 + i * c, y0 - 5 * c)
    for j in range(6):
        ctx.move_to(x0, y0 - j * c); ctx.line_to(x0 + 13 * c, y0 - j * c)
    ctx.stroke()

def piece(ctx, pts, col, dx, dy, a=1.0, lift=0.0, ex=None):
    path = []
    for (gx, gy) in pts:
        gx2, gy2 = gx + dx, gy + dy
        if ex: gy2 = ex(gx2, gy2)
        path.append(P(gx2, gy2))
    c, _, _ = geom()
    # shadow
    ctx.new_path()
    for i, (x, y) in enumerate(path): (ctx.move_to if i == 0 else ctx.line_to)(x + 6 * U, y + 10 * U + lift)
    ctx.close_path(); rgba(ctx, (0, 0, 0), 0.35 * a); ctx.fill()
    ctx.new_path()
    for i, (x, y) in enumerate(path): (ctx.move_to if i == 0 else ctx.line_to)(x, y - lift)
    ctx.close_path()
    g = cairo.LinearGradient(0, path[0][1] - 5 * c, 0, path[0][1])
    g.add_color_stop_rgba(0, min(1, col[0] + 0.15), min(1, col[1] + 0.15), min(1, col[2] + 0.15), a); g.add_color_stop_rgba(1, col[0], col[1], col[2], a)
    ctx.set_source(g); ctx.fill_preserve()
    ctx.set_line_width(3 * U); rgba(ctx, mix(col, NAVY, 0.45), a); ctx.stroke()

def draw_config(ctx, k, a=1.0, t=0.0, ex=None):
    """k = 0 -> configuration A, 1 -> configuration B (pieces slide one after another)."""
    for i, (name, col, pts, (tx, ty)) in enumerate(PIECES):
        kk = ease(clamp(k * 4 - i * 0.75))
        lift = math.sin(kk * math.pi) * 40 * U
        piece(ctx, pts, col, tx * kk, ty * kk, a, lift, ex)

def hole(ctx, a, t):
    if a <= 0: return
    x1, y1 = P(10, 1); x2, y2 = P(11, 0)
    glow(ctx, (x1 + x2) / 2, (y1 + y2) / 2, 120 * U, WHITE, 0.4 * a * (0.7 + 0.3 * math.sin(t * 6)))
    ctx.rectangle(x1, y1, x2 - x1, y2 - y1); ctx.set_line_width(6 * U); rgba(ctx, WHITE, a); ctx.stroke()
    text(ctx, "?", (x1 + x2) / 2, (y1 + y2) / 2, 60 * U, WHITE, a)

def sc_hook(ctx, t, d):
    bg(ctx, t)
    grid(ctx)
    k = prog(t, d * 0.3, d * 0.62)
    draw_config(ctx, k, 1, t)
    hole(ctx, prog(t, d * 0.62, d * 0.7), t)
    if k < 0.05:
        text(ctx, "SAME 4 PIECES", CX, H * 0.6, 56 * U, WHITE, prog(t, 0.3, 1.0))
    pill_y = H * 0.6
    if k >= 1:
        text(ctx, "SAME PIECES… +1 HOLE", CX, pill_y, 56 * U, GOLD, prog(t, d * 0.7, d * 0.78))
    chip(ctx, "THE MISSING SQUARE", t)

def slope_tag(ctx, x, y, label, col, a):
    if a <= 0: return
    font(ctx, 46 * U); w = ctx.text_extents(label).width + 50 * U
    rrect(ctx, x - w / 2, y - 40 * U, w, 80 * U, 40 * U); rgba(ctx, NAVY, 0.9 * a); ctx.fill()
    ctx.set_line_width(4 * U); rgba(ctx, col, a); rrect(ctx, x - w / 2, y - 40 * U, w, 80 * U, 40 * U); ctx.stroke()
    text(ctx, label, x, y, 46 * U, col, a)

def sc_slopes(ctx, t, d):
    bg(ctx, t)
    grid(ctx)
    draw_config(ctx, 0, 1, t)
    # the "straight" line
    lk = prog(t, 0.5, 2.0)
    x1, y1 = P(0, 0); x2, y2 = P(13, 5)
    ctx.set_line_width(4 * U); ctx.set_dash([16 * U, 10 * U], -t * 40 * U); rgba(ctx, WHITE, 0.9 * lk)
    ctx.move_to(x1, y1); ctx.line_to(x1 + (x2 - x1) * lk, y1 + (y2 - y1) * lk); ctx.stroke(); ctx.set_dash([])
    # rise / run markers
    rk = prog(t, d * 0.35, d * 0.45)
    if rk:
        ax, ay = P(8, 0); bx, by = P(8, 3)
        ctx.set_line_width(6 * U); rgba(ctx, CORAL, rk); ctx.move_to(ax, ay); ctx.line_to(bx, by); ctx.stroke()
        slope_tag(ctx, CX - 170 * U, H * 0.25, "3 / 8 = 0.375", CORAL, rk)
    bk = prog(t, d * 0.55, d * 0.65)
    if bk:
        ax, ay = P(13, 3); bx, by = P(13, 5)
        ctx.set_line_width(6 * U); rgba(ctx, BLUE, bk); ctx.move_to(ax, ay); ctx.line_to(bx, by); ctx.stroke()
        slope_tag(ctx, CX + 170 * U, H * 0.32, "2 / 5 = 0.400", BLUE, bk)
    nk = prog(t, d * 0.78, d * 0.88)
    text(ctx, "NOT THE SAME SLOPE!", CX, H * 0.6, 60 * U, GOLD, nk)
    chip(ctx, "LOOK AT THE LONG EDGE", t)

def sc_sliver(ctx, t, d):
    bg(ctx, t)
    grid(ctx, 0.6)
    # exaggerate the deviation from the true diagonal so the bend becomes visible
    amp = 1 + 7 * prog(t, 0.5, d * 0.35)
    def ex(gx, gy):
        line = gx * 5.0 / 13.0
        return line + (gy - line) * amp if gy > 1.5 else gy
    a = 1.0
    pa = [P(0, 0), P(8, ex(8, 3)), P(13, 5)]
    pb = [P(0, 0), P(5, ex(5, 2)), P(13, 5)]
    fk = prog(t, d * 0.55, d * 0.65)
    if fk:
        ctx.new_path(); ctx.move_to(*pa[0]); ctx.line_to(*pa[1]); ctx.line_to(*pa[2]); ctx.line_to(*pb[1]); ctx.close_path()
        rgba(ctx, GOLD, 0.55 * fk); ctx.fill()
        glow(ctx, CX, (pa[1][1] + pb[1][1]) / 2, 260 * U, GOLD, 0.25 * fk)
    for path, col, t0, lb, ly in ((pa, CORAL, 0.05, "VERSION 1: BENDS IN", 0.27), (pb, BLUE, 0.3, "VERSION 2: BULGES OUT", 0.32)):
        k = prog(t, d * t0, d * (t0 + 0.15))
        if not k: continue
        ctx.set_line_width(7 * U); ctx.set_line_cap(cairo.LINE_CAP_ROUND); rgba(ctx, col, k)
        ctx.move_to(*path[0]); ctx.line_to(*path[1]); ctx.line_to(*path[2]); ctx.stroke()
        circle(ctx, path[1][0], path[1][1], 12 * U, col, k)
        text(ctx, lb, CX, H * ly, 40 * U, col, k)
    if True:
        ok = prog(t, d * 0.75, d * 0.85)
        if ok:
            c, _, _ = geom()
            sx, sy = CX - c / 2, H * 0.62
            ctx.rectangle(sx, sy, c, c); rgba(ctx, GOLD, ok); ctx.fill()
            text(ctx, "SLIVER AREA = 1 SQUARE", CX, sy - 50 * U, 50 * U, GOLD, ok)
    text(ctx, "(BEND EXAGGERATED)", CX, H * 0.18, 34 * U, (0.7, 0.75, 0.9), prog(t, 0.6, 1.2))
    chip(ctx, "NOT A REAL TRIANGLE", t)

def sc_outro(ctx, t, d):
    bg(ctx, t)
    grid(ctx, 0.6)
    k = (t / 1.6) % 2
    kk = clamp(k) if k < 1 else clamp(2 - k)
    draw_config(ctx, kk, 0.9, t)
    if kk > 0.95: hole(ctx, 1, t)
    text(ctx, "DID IT FOOL YOU?", CX, H * 0.2, 80 * U, GOLD, prog(t, 0.2, 0.8))
    sk = prog(t, d * 0.45, d * 0.55)
    if sk:
        pulse = 1 + 0.04 * math.sin(t * 5)
        ctx.save(); ctx.translate(CX, H * 0.62); ctx.scale(pulse * sk, pulse * sk)
        rrect(ctx, -260 * U, -55 * U, 520 * U, 110 * U, 22 * U); rgba(ctx, CORAL); ctx.fill()
        text(ctx, "SUBSCRIBE", 0, 0, 56 * U, WHITE); ctx.restore()

SHORT_SCENES = ["hook", "slopes", "sliver", "outro"]
SCENES = dict(hook=sc_hook, slopes=sc_slopes, sliver=sc_sliver, outro=sc_outro)

def thumbnail(c):
    vgrad(c, (0.06, 0.09, 0.21), NAVY)
    thumb_text(c, "WHERE DID", "THIS SQUARE GO?", "MATH ILLUSION")
