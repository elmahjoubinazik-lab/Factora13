# Episode 026 (Short only) - "How many holes does a pair of pants have?" — holes debate #2 (answer to ep. 018, the straw)
# Executed inside engine/render.py (helpers available). Vertical layout. Original vector illustration. All sizes in U.
# Maths: a pair of pants = sphere minus 3 disks ("pair of pants" surface), first Betti number 2 -> 2 holes;
# straw = cylinder (sphere minus 2 disks) -> 1 hole; one-piece tube-like object: holes = openings - 1.
# A pocket is a dead end (a patch attached along part of its edge): it retracts onto the seam, so it adds no hole.

DENIM_L = (0.30, 0.58, 1.00)
DENIM_D = (0.07, 0.17, 0.55)
HOLE = (0.01, 0.01, 0.05)

def bg(ctx, t, tint=PURPLE):
    neon_bg(ctx, t, (0.10, 0.05, 0.26), (0.01, 0.02, 0.08), tint)

# ---------------------------------------------------------------- geometry (local units, 1 unit = s * U)
PANTS = [(-230, -300), (230, -300), (270, 330), (60, 330), (0, -40), (-60, 330), (-270, 330)]
WAIST = (0, -300, 230, 34)                     # cx, cy, rx, ry of the waist opening
CUFFS = [(-165, 330, 105, 26), (165, 330, 105, 26)]
HOLES2 = [(-200, 0, 95), (200, 0, 95)]          # the 2 holes of the flattened shape

def resample(pts, n=240):
    segs = [(pts[i], pts[(i + 1) % len(pts)]) for i in range(len(pts))]
    lens = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in segs]; tot = sum(lens)
    out, i, acc = [], 0, 0.0
    for k in range(n):
        s = tot * k / n
        while acc + lens[i] < s: acc += lens[i]; i += 1
        a, b = segs[i]; f = (s - acc) / lens[i]
        out.append((a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f))
    return out

def stadium_pts(hw=440, hh=220, n=240):
    r = hh; pts = [(-hw + r, -hh), (hw - r, -hh)]
    pts += [(hw - r + r * math.sin(a), -r * math.cos(a)) for a in [math.pi * i / 24 for i in range(1, 24)]]
    pts += [(hw - r, hh), (-hw + r, hh)]
    pts += [(-hw + r - r * math.sin(a), r * math.cos(a)) for a in [math.pi * i / 24 for i in range(1, 24)]]
    return resample(pts, n)

P_PANTS = resample(PANTS)
P_FLAT = stadium_pts()

def outline(ctx, pts):
    ctx.new_path(); ctx.move_to(*pts[0])
    for p in pts[1:]: ctx.line_to(*p)
    ctx.close_path()

def denim_fill(ctx, a, y0=-300, y1=330):
    g = cairo.LinearGradient(-280, 0, 280, 0)
    g.add_color_stop_rgba(0, *DENIM_D, a); g.add_color_stop_rgba(0.28, *DENIM_L, a); g.add_color_stop_rgba(0.5, *mix(DENIM_L, DENIM_D, 0.45), a)
    g.add_color_stop_rgba(0.72, *DENIM_L, a); g.add_color_stop_rgba(1, *DENIM_D, a)
    ctx.set_source(g)

def ellipse(ctx, cx, cy, rx, ry):
    ctx.save(); ctx.translate(cx, cy); ctx.scale(1, max(0.01, ry / rx)); ctx.new_path(); ctx.arc(0, 0, rx, 0, 2 * math.pi); ctx.restore()

def stitch(ctx, pts, a, col=GOLD, w=4):
    ctx.new_path(); ctx.move_to(*pts[0])
    for p in pts[1:]: ctx.line_to(*p)
    ctx.set_line_width(w); ctx.set_dash([14, 10]); rgba(ctx, col, 0.85 * a); ctx.stroke(); ctx.set_dash([])

def jeans(ctx, cx, cy, s, a=1.0, t=0.0, rings=0.0, pocket_hl=0.0):
    """Realistic jeans seen from the front: denim gradient, waistband, belt loops, button, gold stitching, front pockets,
    and the 3 openings (waist + 2 cuffs) drawn as dark ellipses; rings > 0 lights the openings in gold."""
    if a <= 0: return
    S = s * U
    ctx.save(); ctx.translate(cx, cy); ctx.scale(S, S)
    glow(ctx, 0, 20, 470, DENIM_L, 0.35 * a)
    outline(ctx, P_PANTS); denim_fill(ctx, a); ctx.fill()
    # shading: crease between legs + side shadows
    outline(ctx, P_PANTS); g = cairo.LinearGradient(0, -300, 0, 330); g.add_color_stop_rgba(0, 1, 1, 1, 0.10 * a); g.add_color_stop_rgba(1, 0, 0, 0.1, 0.30 * a); ctx.set_source(g); ctx.fill()
    for sx in (-1, 1):
        ctx.new_path(); ctx.move_to(sx * 150, -150); ctx.curve_to(sx * 140, 0, sx * 175, 150, sx * 165, 320)
        ctx.set_line_width(26); rgba(ctx, WHITE, 0.07 * a); ctx.stroke()
        for k in range(3):   # knee wrinkles
            yy = 110 + k * 26; ctx.new_path(); ctx.move_to(sx * 110, yy); ctx.curve_to(sx * 150, yy - 14, sx * 190, yy - 10, sx * 225, yy + 4)
            ctx.set_line_width(5); rgba(ctx, DENIM_D, 0.45 * a); ctx.stroke()
    # waistband, belt loops, button, fly
    ctx.new_path(); ctx.move_to(-230, -300); ctx.line_to(230, -300); ctx.line_to(233, -245); ctx.line_to(-233, -245); ctx.close_path()
    ctx.set_source(lin_g(-240, 240, [(0, mix(DENIM_D, (0, 0, 0), 0.2)), (0.3, DENIM_L), (1, DENIM_D)], a)); ctx.fill()
    stitch(ctx, [(-226, -253), (226, -253)], a)
    for bx in (-170, -60, 60, 170):
        rrect(ctx, bx - 11, -310, 22, 74, 6); rgba(ctx, mix(DENIM_D, DENIM_L, 0.5), a); ctx.fill()
        ctx.rectangle(bx - 11, -310, 22, 74); ctx.set_line_width(3); rgba(ctx, GOLD, 0.6 * a); ctx.stroke()
    circle(ctx, 0, -272, 15, (0.95, 0.80, 0.35), a); circle(ctx, -4, -276, 5, WHITE, 0.8 * a)
    stitch(ctx, [(0, -245), (0, -95)], a); stitch(ctx, [(34, -245), (34, -120), (0, -88)], a)
    # front pockets (curved openings) + small coin pocket
    for sx in (-1, 1):
        ctx.new_path(); ctx.move_to(sx * 200, -245); ctx.curve_to(sx * 190, -170, sx * 140, -150, sx * 95, -245)
        ctx.set_line_width(6); rgba(ctx, DENIM_D, a); ctx.stroke()
        stitch(ctx, [(sx * 205, -236), (sx * 198, -170), (sx * 150, -142), (sx * 104, -236)], a, w=3)
        if pocket_hl > 0 and sx == 1:
            def pk(c):
                c.move_to(200, -245); c.curve_to(190, -170, 140, -150, 95, -245)
            neon_path(ctx, pk, PINK, 9, pocket_hl)
    # side seams
    for sx in (-1, 1): stitch(ctx, [(sx * 232, -245), (sx * 268, 320)], a, w=3)
    # openings
    wx, wy, wrx, wry = WAIST
    ellipse(ctx, wx, wy, wrx - 6, wry); g = cairo.RadialGradient(0, wy + 10, 0, 0, wy, wrx); g.add_color_stop_rgba(0, 0.05, 0.03, 0.15, a); g.add_color_stop_rgba(1, *HOLE, a); ctx.set_source(g); ctx.fill()
    for (ux, uy, urx, ury) in CUFFS:
        ellipse(ctx, ux, uy, urx, ury); rgba(ctx, HOLE, a); ctx.fill()
        ellipse(ctx, ux, uy, urx, ury); ctx.set_line_width(8); rgba(ctx, mix(DENIM_L, WHITE, 0.3), a); ctx.stroke()
    if rings > 0:
        pulse = 1 + 0.06 * math.sin(t * 7)
        for (ox, oy, orx, ory) in [WAIST] + CUFFS:
            glow(ctx, ox, oy, orx * 1.5, GOLD, 0.35 * rings)
            neon_path(ctx, lambda c, ox=ox, oy=oy, orx=orx, ory=ory: ellipse(c, ox, oy, orx * pulse, ory * pulse + 6), GOLD, 7, rings)
    ctx.restore()

def lin_g(x0, x1, stops, a):
    g = cairo.LinearGradient(x0, 0, x1, 0)
    for o, c in stops: g.add_color_stop_rgba(o, c[0], c[1], c[2], a)
    return g

def morph_shape(ctx, cx, cy, s, k, t, a=1.0):
    """Pants -> flat shape with 2 holes (stretch, no tearing). k in [0, 1]. The waist opening becomes the outer rim,
    each leg cuff slides inward and becomes one hole."""
    S = s * U; e = ease(k)
    ctx.save(); ctx.translate(cx, cy); ctx.scale(S, S)
    pts = [(p[0] + (q[0] - p[0]) * e, p[1] + (q[1] - p[1]) * e) for p, q in zip(P_PANTS, P_FLAT)]
    glow(ctx, 0, 0, 520, mix(DENIM_L, PURPLE, e), 0.35 * a)
    outline(ctx, pts)
    g = cairo.LinearGradient(-440, -220, 440, 220)
    g.add_color_stop_rgba(0, *mix(DENIM_D, PURPLE, e * 0.6), a); g.add_color_stop_rgba(0.5, *mix(DENIM_L, PINK, e * 0.45), a); g.add_color_stop_rgba(1, *mix(DENIM_D, PURPLE, e * 0.6), a)
    ctx.set_source(g); ctx.fill()
    # rim: the waist opening "becomes" the outer edge (gold neon fades in)
    neon_path(ctx, lambda c: outline(c, pts), GOLD, 8, a * e)
    wx, wy, wrx, wry = WAIST
    if e < 1:
        ey = min(p[1] for p in pts); topx = [p[0] for p in pts if p[1] < ey + 6]
        erx, ery = max(20, (max(topx) - min(topx)) / 2), wry * (1 - e)
        fa = clamp(1 - e / 0.25) ** 2   # l'ouverture de la taille suit le bord du haut et disparaît vite : elle devient le bord doré
        ellipse(ctx, wx, ey, erx, ery); rgba(ctx, HOLE, a * fa); ctx.fill()
        neon_path(ctx, lambda c: ellipse(c, wx, ey, erx, ery + 4), GOLD, 7, a * fa)
    for (ux, uy, urx, ury), (hx, hy, hr) in zip(CUFFS, HOLES2):
        x = ux + (hx - ux) * e; y = uy + (hy - uy) * e; rx = urx + (hr - urx) * e; ry = ury + (hr - ury) * e
        ellipse(ctx, x, y, rx, ry); rgba(ctx, HOLE, a); ctx.fill()
        neon_path(ctx, lambda c, x=x, y=y, rx=rx, ry=ry: ellipse(c, x, y, rx, ry), CYAN, 7, a)
    ctx.restore()

# ---------------------------------------------------------------- scenes
def sc_hook(ctx, t, d):
    bg(ctx, t, CYAN)
    cy = H * 0.55; s = 1.62 * (1 + 0.012 * math.sin(t * 2.5))
    jeans(ctx, CX, cy, s, 1.0, t, rings=1.0)
    S = s * U
    for i, (ox, oy) in enumerate([(0, -300), (-165, 330), (165, 330)]):     # 1, 2, 3 on the openings
        k = prog(t, 0.25 + 0.25 * i, 0.5 + 0.25 * i)
        if k:
            x, y = CX + ox * S, cy + oy * S
            glow(ctx, x, y, 110 * U * ease(k), GOLD, 0.5); circle(ctx, x, y, 58 * U * ease(k), GOLD, 1.0); text(ctx, str(i + 1), x, y, 76 * U * ease(k), NAVY)
    # "3?" then crossed out on "Look again"
    qk = prog(t, 2.25, 2.55)
    if qk:
        s2 = (1 + 0.5 * (1 - qk)) * (1 + 0.05 * math.sin(t * 9))
        ctx.save(); ctx.translate(CX, H * 0.44); ctx.scale(s2, s2)
        rrect(ctx, -190 * U, -150 * U, 380 * U, 300 * U, 50 * U); rgba(ctx, (0.02, 0.02, 0.06), 0.88 * qk); ctx.fill()
        rrect(ctx, -190 * U, -150 * U, 380 * U, 300 * U, 50 * U); ctx.set_line_width(7 * U); rgba(ctx, CORAL, qk); ctx.stroke()
        glow(ctx, 0, 0, 220 * U, CORAL, 0.45 * qk)
        neon_text(ctx, "3?", 0, 0, 220 * U, CORAL, qk, PINK, fill=0.55)
        xk = prog(t, 3.05, 3.3)
        if xk:
            for sgn in (-1, 1):
                ctx.new_path(); ctx.move_to(-120 * U, sgn * -110 * U); ctx.line_to(-120 * U + 240 * U * xk, sgn * -110 * U + sgn * 220 * U * xk)
                ctx.set_line_width(26 * U); ctx.set_line_cap(cairo.LINE_CAP_ROUND); rgba(ctx, (1.0, 0.15, 0.15), 1); ctx.stroke()
        ctx.restore()

def sc_morph(ctx, t, d):
    bg(ctx, t, PURPLE)
    k = prog(t, 0.35, d * 0.78)
    s = 1.55 - 0.15 * ease(k)
    if k <= 0:
        jeans(ctx, CX, H * 0.47, s, 1.0, t, rings=1.0)
    else:
        jeans(ctx, CX, H * 0.47, s, 1.0 - ease(min(1.0, k * 4)), t)
        morph_shape(ctx, CX, H * 0.47, s, k, t, min(1.0, k * 4))
    if k < 1:
        neon_text(ctx, "STRETCH. DON'T TEAR.", CX, H * 0.13, 84 * U, CYAN, prog(t, 0, 0.3), PURPLE, fill=0.3)
    fk = prog(t, d * 0.78, d * 0.9)
    if fk:
        sc_ = 1 + 0.3 * (1 - fk) + 0.04 * math.sin(t * 7)
        ctx.save(); ctx.translate(CX, H * 0.14); ctx.scale(sc_, sc_)
        neon_text(ctx, "2 HOLES", 0, 0, 190 * U, GOLD, fk, CORAL, fill=0.5); ctx.restore()
        S = s * U
        for i, (hx, hy, hr) in enumerate(HOLES2):
            text(ctx, str(i + 1), CX + hx * S, H * 0.47 + hy * S, 120 * U, WHITE, fk)

def straw_icon(ctx, cx, cy, s, a, t):
    S = s * U
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(-0.35); ctx.scale(S, S)
    rrect(ctx, -40, -170, 80, 340, 20)
    g = cairo.LinearGradient(-40, 0, 40, 0); g.add_color_stop_rgba(0, 0.75, 0.80, 0.95, a); g.add_color_stop_rgba(0.4, 1, 1, 1, a); g.add_color_stop_rgba(1, 0.55, 0.60, 0.80, a)
    ctx.set_source(g); ctx.fill()
    ctx.save(); rrect(ctx, -40, -170, 80, 340, 20); ctx.clip()
    for i in range(-6, 7):
        ctx.new_path(); ctx.move_to(-60, i * 60 - 30 + (t * 30) % 60); ctx.line_to(60, i * 60 - 70 + (t * 30) % 60); ctx.set_line_width(22); rgba(ctx, CORAL, 0.85 * a); ctx.stroke()
    ctx.restore()
    for yy in (-170, 170):
        ellipse(ctx, 0, yy, 40, 13); rgba(ctx, HOLE, a); ctx.fill()
        neon_path(ctx, lambda c, yy=yy: ellipse(c, 0, yy, 44, 16), GOLD, 5, a)
    ctx.restore()

def eq_card(ctx, y, icon, eq, label, col, k, t):
    if k <= 0: return
    x0 = CX + (1 - ease(k)) * W * 0.6
    rrect(ctx, x0 - W * 0.45, y - 150 * U, W * 0.90, 300 * U, 50 * U); rgba(ctx, (0.03, 0.03, 0.10), 0.80 * k); ctx.fill()
    rrect(ctx, x0 - W * 0.45, y - 150 * U, W * 0.90, 300 * U, 50 * U); ctx.set_line_width(5 * U); rgba(ctx, col, 0.9 * k); ctx.stroke()
    glow(ctx, x0 - W * 0.30, y, 200 * U, col, 0.3 * k)
    icon(x0 - W * 0.30, y)
    neon_text(ctx, eq, x0 + W * 0.12, y - 25 * U, 130 * U, col, k, None, fill=0.6)
    text(ctx, label, x0 + W * 0.12, y + 95 * U, 44 * U, WHITE, k)

def sc_rule(ctx, t, d):
    bg(ctx, t, CYAN)
    fk = prog(t, 0.05, 0.4)
    sc_ = 1 + 0.25 * (1 - fk)
    ctx.save(); ctx.translate(CX, H * 0.12); ctx.scale(sc_, sc_)
    neon_text(ctx, "HOLES =", 0, -55 * U, 110 * U, WHITE, fk, CYAN, fill=0.4)
    neon_text(ctx, "OPENINGS − 1", 0, 75 * U, 120 * U, GOLD, fk, CORAL, fill=0.5)
    ctx.restore()
    eq_card(ctx, H * 0.36, lambda x, y: straw_icon(ctx, x, y, 0.75, 1.0, t), "2 − 1 = 1", "STRAW: 1 HOLE", CYAN, prog(t, 2.1, 2.5), t)
    eq_card(ctx, H * 0.56, lambda x, y: jeans(ctx, x, y, 0.36, 1.0, t, rings=1.0), "3 − 1 = 2", "PANTS: 2 HOLES", GOLD, prog(t, 4.2, 4.6), t)

def arrow_path(ctx, pts, col, k, w=10, head=True):
    """Neon arrow along a polyline, drawn up to fraction k."""
    if k <= 0: return
    lens = [math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1]) for i in range(len(pts) - 1)]; tot = sum(lens) * k
    path = [pts[0]]; acc = 0
    for i, L in enumerate(lens):
        if acc + L >= tot:
            f = (tot - acc) / max(L, 1e-6); path.append((pts[i][0] + (pts[i + 1][0] - pts[i][0]) * f, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * f)); break
        path.append(pts[i + 1]); acc += L
    def dr(c):
        c.move_to(*path[0])
        for p in path[1:]: c.line_to(*p)
    neon_path(ctx, dr, col, w * U)
    if head and len(path) > 1:
        (x0, y0), (x1, y1) = path[-2], path[-1]; an = math.atan2(y1 - y0, x1 - x0); h = 46 * U
        ctx.new_path(); ctx.move_to(x1 + math.cos(an) * h * 0.5, y1 + math.sin(an) * h * 0.5)
        ctx.line_to(x1 - math.cos(an - 0.5) * h, y1 - math.sin(an - 0.5) * h); ctx.line_to(x1 - math.cos(an + 0.5) * h, y1 - math.sin(an + 0.5) * h)
        ctx.close_path(); rgba(ctx, mix(col, WHITE, 0.4), 1); ctx.fill()

def stamp(ctx, s, x, y, col, k, ang=-0.12, size=78):
    if k <= 0: return
    ctx.save(); ctx.translate(x, y); ctx.rotate(ang); sc_ = 1 + 0.6 * (1 - k); ctx.scale(sc_, sc_)
    font(ctx, size * U); w_ = ctx.text_extents(s).width + 60 * U
    rrect(ctx, -w_ / 2, -size * 0.85 * U, w_, size * 1.7 * U, 18 * U); rgba(ctx, (0.02, 0.02, 0.05), 0.85 * k); ctx.fill()
    rrect(ctx, -w_ / 2, -size * 0.85 * U, w_, size * 1.7 * U, 18 * U); ctx.set_line_width(8 * U); rgba(ctx, col, k); ctx.stroke()
    text(ctx, s, 0, 0, size * U, col, k); ctx.restore()

def sc_pockets(ctx, t, d):
    bg(ctx, t, PINK)
    s = 1.55; cy = H * 0.50; S = s * U
    jeans(ctx, CX, cy, s, 1.0, t, pocket_hl=prog(t, 0.1, 0.4))
    P = lambda x, y: (CX + x * S, cy + y * S)
    # 1) into the pocket: dead end (arrow goes in, stops at the bottom of the pocket)
    k1 = prog(t, 0.3, 1.3)
    arrow_path(ctx, [P(150, -420), P(150, -250), P(150, -175)], CORAL, k1)
    stamp(ctx, "DEAD END", CX + W * 0.18, H * 0.235, CORAL, prog(t, 1.25, 1.45), 0.10)
    # 2) through a leg: a real tunnel (in at the waist, out at the cuff)
    k2 = prog(t, d * 0.42, d * 0.68)
    arrow_path(ctx, [P(-165, -420), P(-160, -250), P(-165, 0), P(-165, 330), P(-165, 430)], GREEN, k2)
    stamp(ctx, "TUNNEL = HOLE", CX - W * 0.05, H * 0.80, GREEN, prog(t, d * 0.66, d * 0.76), -0.06, 66)
    neon_text(ctx, "POCKETS: 0 HOLES", CX, H * 0.10, 96 * U, PINK, prog(t, 0, 0.3), PURPLE, fill=0.4)

def tshirt(ctx, cx, cy, s, a, t, rings=0.0):
    S = s * U
    ctx.save(); ctx.translate(cx, cy); ctx.scale(S, S)
    def body(c):
        c.move_to(-90, -300); c.curve_to(-40, -250, 40, -250, 90, -300); c.line_to(300, -220); c.line_to(380, -40); c.line_to(230, 10)
        c.line_to(220, 330); c.line_to(-220, 330); c.line_to(-230, 10); c.line_to(-380, -40); c.line_to(-300, -220); c.close_path()
    glow(ctx, 0, 0, 480, PINK, 0.3 * a)
    ctx.new_path(); body(ctx); g = cairo.LinearGradient(-380, 0, 380, 0)
    g.add_color_stop_rgba(0, *mix(PINK, NAVY, 0.4), a); g.add_color_stop_rgba(0.5, *mix(PINK, WHITE, 0.15), a); g.add_color_stop_rgba(1, *mix(PINK, NAVY, 0.4), a)
    ctx.set_source(g); ctx.fill()
    if rings > 0:
        for (ox, oy, orx, ory, an) in ((0, -268, 95, 28, 0), (0, 330, 220, 30, 0), (-305, -12, 80, 24, 1.2), (305, -12, 80, 24, -1.2)):
            ctx.save(); ctx.translate(ox, oy); ctx.rotate(an)
            neon_path(ctx, lambda c, orx=orx, ory=ory: ellipse(c, 0, 0, orx, ory), GOLD, 7, rings * a)
            ctx.restore()
    ctx.restore()

def sc_outro(ctx, t, d):
    bg(ctx, t, PINK)
    tshirt(ctx, CX, H * 0.47, 1.5, 0.30, t, rings=0.45)
    cta(ctx, t, d, "HOW MANY HOLES IN A T-SHIRT?", "COMMENT YOUR ANSWER")

SHORT_SCENES = ["hook", "morph", "rule", "pockets", "outro"]
SCENES = dict(hook=sc_hook, morph=sc_morph, rule=sc_rule, pockets=sc_pockets, outro=sc_outro)

def thumbnail(c):
    vgrad(c, (0.12, 0.05, 0.32), NAVY)
    thumb_text(c, "HOW MANY HOLES", "IN A PAIR OF PANTS?", "TOPOLOGY")

def poster_text(ctx, s, x, y, size, col, maxw=None):
    font(ctx, size); w = ctx.text_extents(s).width
    if maxw and w > maxw: size *= maxw / w; font(ctx, size)
    e = ctx.text_extents(s); x0 = x - e.width / 2 - e.x_bearing; y0 = y + size * 0.35
    ctx.save(); ctx.translate(10 * U, 14 * U); ctx.move_to(x0, y0); ctx.text_path(s); rgba(ctx, (0, 0, 0), 0.75)
    ctx.set_line_width(size * 0.20); ctx.set_line_join(cairo.LINE_JOIN_ROUND); ctx.stroke_preserve(); ctx.fill(); ctx.restore()
    ctx.move_to(x0, y0); ctx.text_path(s); rgba(ctx, (0.01, 0.01, 0.02), 1); ctx.set_line_width(size * 0.16)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND); ctx.stroke_preserve(); rgba(ctx, col, 1); ctx.fill()

def cover(ctx):
    """Affiche (règles 2026-11-10/11) : jean en très grand, 3 ouvertures numérotées et lumineuses, titre énorme dans la
    zone sûre 3:4 (12–88 % de la hauteur), pastille de série, bandeau d'action ; ne donne pas la réponse."""
    bg(ctx, 1.0, CYAN)
    cy = H * 0.54; s = 1.42; S = s * U
    jeans(ctx, CX, cy, s, 1.0, 0.3, rings=1.0)
    for i, (ox, oy) in enumerate([(0, -300), (-165, 330), (165, 330)]):
        x, y = CX + ox * S, cy + oy * S
        glow(ctx, x, y, 110 * U, GOLD, 0.5); circle(ctx, x, y, 50 * U, GOLD, 1.0)
        ctx.new_path(); ctx.arc(x, y, 50 * U, 0, 2 * math.pi); ctx.set_line_width(6 * U); rgba(ctx, NAVY, 1); ctx.stroke()
        text(ctx, str(i + 1), x, y, 66 * U, NAVY)
    poster_text(ctx, "HOW MANY", CX, H * 0.155, 150 * U, WHITE, W * 0.80)
    poster_text(ctx, "HOLES?", CX, H * 0.235, 210 * U, GOLD, W * 0.80)
    rrect(ctx, CX - 480 * U, H * 0.855 - 58 * U, 960 * U, 116 * U, 58 * U); rgba(ctx, GOLD, 1); ctx.fill()
    rrect(ctx, CX - 480 * U, H * 0.855 - 58 * U, 960 * U, 116 * U, 58 * U); ctx.set_line_width(7 * U); rgba(ctx, (0.01, 0.01, 0.02), 1); ctx.stroke()
    text(ctx, "1, 2 OR 3? COMMENT!", CX, H * 0.855, 66 * U, (0.02, 0.03, 0.06))
