# Scenes for "What if all insects disappeared?"
# Executed inside engine/render.py: helpers (W, H, U, CX, CY, VERT, colors, vgrad, circle, glow, text, rrect,
# stars, sun, chip, prog, ease, mix...) are available.

LEAF = (0.30, 0.66, 0.40)
LEAF_D = (0.12, 0.34, 0.24)
SOIL = (0.36, 0.24, 0.15)
SOIL_D = (0.22, 0.14, 0.09)
GREY = (0.45, 0.47, 0.55)
PINK = (0.95, 0.55, 0.75)
VIOLET = (0.62, 0.45, 0.95)

def ell(ctx, x, y, rx, ry, c, a=1.0, rot=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(max(rx, 0.01), max(ry, 0.01))
    ctx.arc(0, 0, 1, 0, 2 * math.pi); ctx.restore(); rgba(ctx, c, a); ctx.fill()

def line(ctx, pts, c, w, a=1.0):
    ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.move_to(*pts[0])
    for p in pts[1:]: ctx.line_to(*p)
    rgba(ctx, c, a); ctx.set_line_width(w); ctx.stroke()

# ---------- insects ----------
def bee(ctx, x, y, s, t, a=1.0, ang=0.0):
    if a <= 0: return
    ctx.save(); ctx.translate(x, y); ctx.rotate(ang)
    fl = 0.55 + 0.45 * math.sin(t * 40)
    for sgn in (-1, 1):
        ell(ctx, -6 * s, -22 * s * fl, 16 * s, 26 * s * fl + 2 * s, (0.85, 0.93, 1.0), 0.55 * a, sgn * 0.5)
    ell(ctx, 0, 0, 34 * s, 22 * s, GOLD, a)
    ctx.save(); ctx.translate(0, 0); ctx.scale(34 * s, 22 * s); ctx.arc(0, 0, 1, 0, 2 * math.pi); ctx.restore(); ctx.save(); ctx.clip()
    for k in (-0.35, 0.05, 0.45):
        ctx.rectangle(k * 34 * s - 5 * s, -30 * s, 10 * s, 60 * s)
    rgba(ctx, NAVY, a); ctx.fill(); ctx.restore(); ctx.new_path()
    circle(ctx, 36 * s, -2 * s, 13 * s, NAVY, a)
    circle(ctx, 40 * s, -5 * s, 3.5 * s, WHITE, a)
    line(ctx, [(42 * s, -12 * s), (52 * s, -26 * s)], NAVY, 3 * s, a)
    ctx.move_to(-34 * s, -4 * s); ctx.line_to(-46 * s, 0); ctx.line_to(-34 * s, 4 * s); rgba(ctx, NAVY, a); ctx.fill()
    ctx.restore()

def butterfly(ctx, x, y, s, t, c=PINK, a=1.0):
    if a <= 0: return
    f = 0.35 + 0.65 * abs(math.sin(t * 6))
    ctx.save(); ctx.translate(x, y)
    for sgn in (-1, 1):
        ctx.save(); ctx.scale(sgn * f, 1)
        ell(ctx, 30 * s, -18 * s, 30 * s, 24 * s, c, a, -0.4)
        ell(ctx, 24 * s, 18 * s, 20 * s, 16 * s, mix(c, WHITE, 0.25), a, 0.5)
        circle(ctx, 34 * s, -20 * s, 7 * s, GOLD, a)
        ctx.restore()
    ell(ctx, 0, 0, 5 * s, 30 * s, NAVY, a)
    line(ctx, [(0, -28 * s), (-10 * s, -46 * s)], NAVY, 2.5 * s, a)
    line(ctx, [(0, -28 * s), (10 * s, -46 * s)], NAVY, 2.5 * s, a)
    ctx.restore()

def beetle(ctx, x, y, s, ang=0.0, c=(0.25, 0.75, 0.6), a=1.0, t=0.0):
    if a <= 0: return
    ctx.save(); ctx.translate(x, y); ctx.rotate(ang)
    for i in (-1, 0, 1):
        w = math.sin(t * 12 + i) * 5 * s
        line(ctx, [(i * 16 * s, -14 * s), (i * 16 * s + w - 4 * s, -34 * s)], NAVY, 4 * s, a)
        line(ctx, [(i * 16 * s, 14 * s), (i * 16 * s - w - 4 * s, 34 * s)], NAVY, 4 * s, a)
    ell(ctx, -4 * s, 0, 34 * s, 24 * s, c, a)
    line(ctx, [(-36 * s, 0), (24 * s, 0)], NAVY, 3 * s, a * 0.7)
    circle(ctx, 32 * s, 0, 13 * s, NAVY, a)
    ell(ctx, -12 * s, -9 * s, 12 * s, 5 * s, WHITE, 0.35 * a, -0.2)
    ctx.restore()

def ant(ctx, x, y, s, ang=0.0, t=0.0, c=(0.12, 0.08, 0.06), a=1.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(ang)
    for i in (-1, 0, 1):
        w = math.sin(t * 14 + i * 2) * 4 * s
        line(ctx, [(i * 8 * s, 0), (i * 10 * s + w, -18 * s)], c, 2.5 * s, a)
        line(ctx, [(i * 8 * s, 0), (i * 10 * s - w, 18 * s)], c, 2.5 * s, a)
    ell(ctx, -18 * s, 0, 13 * s, 9 * s, c, a); ell(ctx, 0, 0, 9 * s, 6 * s, c, a); circle(ctx, 15 * s, 0, 8 * s, c, a)
    line(ctx, [(20 * s, -3 * s), (30 * s, -12 * s)], c, 2 * s, a)
    ctx.restore()

def firefly(ctx, x, y, s, t, ph, a=1.0):
    b = (0.5 + 0.5 * math.sin(t * 3 + ph)) * a
    glow(ctx, x, y, 26 * s, (0.8, 1.0, 0.4), 0.6 * b)
    circle(ctx, x, y, 5 * s, (0.9, 1.0, 0.6), b)

def flower(ctx, x, y, s, c, stem=120, droop=0.0, a=1.0, t=0.0):
    sw = math.sin(t * 1.3 + x * 0.01) * 6 * s
    tx, ty = x + sw + droop * 50 * s, y - stem * s * (1 - 0.35 * droop)
    ctx.move_to(x, y); ctx.curve_to(x, y - stem * s * 0.5, tx, ty + stem * s * 0.4, tx, ty)
    rgba(ctx, mix(LEAF, GREY, droop), a); ctx.set_line_width(7 * s); ctx.stroke()
    ell(ctx, x + 18 * s, y - stem * s * 0.4, 20 * s, 8 * s, mix(LEAF, GREY, droop), a, -0.5)
    col = mix(c, GREY, droop)
    for i in range(6):
        an = i / 6 * 2 * math.pi + droop * 0.3
        ell(ctx, tx + math.cos(an) * 20 * s, ty + math.sin(an) * 20 * s, 17 * s, 11 * s, col, a, an)
    circle(ctx, tx, ty, 13 * s, mix(GOLD, GREY, droop), a)
    return tx, ty

def meadow(ctx, t, yb, dim=0.0):
    rgba(ctx, mix((0.10, 0.22, 0.20), (0.08, 0.09, 0.12), dim))
    ctx.move_to(0, H); ctx.line_to(0, yb)
    for i in range(25): ctx.line_to(W * i / 24, yb - 26 * U * math.sin(i * 0.7) - 14 * U * math.sin(i * 1.9))
    ctx.line_to(W, H); ctx.close_path(); ctx.fill()

def dashed_ring(ctx, x, y, r, a):
    ctx.set_dash([10 * U, 10 * U]); ctx.arc(x, y, r, 0, 2 * math.pi)
    rgba(ctx, WHITE, a); ctx.set_line_width(3 * U); ctx.stroke(); ctx.set_dash([])

# ---------- scenes ----------
def sc_hook(ctx, t, d):
    gone = prog(t, d * 0.42, d * 0.62)
    vgrad(ctx, mix(NAVY2, NAVY, gone), mix((0.16, 0.24, 0.36), (0.05, 0.06, 0.10), gone))
    stars(ctx, t, 0.6)
    yb = H * 0.80 if not VERT else H * 0.66
    meadow(ctx, t, yb, gone)
    n = 9 if not VERT else 5
    cols = [PINK, GOLD, VIOLET, CORAL, WHITE]
    heads = []
    for i in range(n):
        x = W * (i + 0.5) / n
        heads.append(flower(ctx, x, yb + 30 * U, 1.0 * U / U, cols[i % 5], 150 + 50 * (i % 3), gone, 1, t))
    random.seed(4)
    m = 14 if not VERT else 10
    for j in range(m):
        ph = random.random() * 6.28
        bx = W * (0.08 + 0.84 * random.random()) + math.sin(t * 0.8 + ph) * 60 * U
        by = H * (0.18 + 0.38 * random.random()) * (1 if not VERT else 1.1) + math.cos(t * 1.1 + ph) * 30 * U
        own = clamp((gone * 1.4) - j / m * 0.4)
        a = 1 - own
        kind = j % 3
        if kind == 0: bee(ctx, bx, by, 1.1 * U, t + ph, a, 0.15 * math.sin(t + ph))
        elif kind == 1: butterfly(ctx, bx, by, 1.0 * U, t + ph, cols[j % 5], a)
        else: firefly(ctx, bx, by, 1.4 * U, t, ph, a)
        if 0 < own < 1: dashed_ring(ctx, bx, by, 50 * U, 0.6 * (1 - abs(own - 0.5) * 2))
    q = prog(t, d - 3.0, d - 2.2)
    if q: text(ctx, "?", CX, H * 0.36 if not VERT else H * 0.30, 280 * U, GOLD, q)

def sc_title(ctx, t, d):
    vgrad(ctx, NAVY2, NAVY); stars(ctx, t, 0.7)
    yo = -40 * U if not VERT else -140 * U
    a = prog(t, 0, 0.5)
    bee(ctx, CX, CY + yo - 210 * U, 2.0 * U, t, a * (1 - 0.6 * prog(t, 1.5, d)))
    dashed_ring(ctx, CX, CY + yo - 210 * U, 120 * U, 0.6 * a)
    if VERT:
        text(ctx, "WHAT IF ALL", CX, CY + yo, 100 * U, WHITE, a)
        text(ctx, "INSECTS", CX, CY + yo + 120 * U, 100 * U, WHITE, a)
        text(ctx, "DISAPPEARED?", CX, CY + yo + 240 * U, 100 * U, GOLD, a)
    else:
        text(ctx, "WHAT IF ALL INSECTS", CX, CY + yo, 96 * U, WHITE, a)
        text(ctx, "DISAPPEARED?", CX, CY + yo + 120 * U, 96 * U, GOLD, a)

def sc_count(ctx, t, d):
    vgrad(ctx, NAVY2, NAVY); stars(ctx, t, 0.4)
    if VERT: px, py, R = CX, H * 0.48, 230 * U
    else: px, py, R = W * 0.68, CY - 20 * U, 250 * U
    p = prog(t, 4.0, 7.0)
    frac = 0.58 * p
    # pie: all known animal species
    circle(ctx, px, py, R, (0.18, 0.22, 0.38))
    if frac > 0:
        ctx.move_to(px, py); ctx.arc(px, py, R, -math.pi / 2, -math.pi / 2 + frac * 2 * math.pi); ctx.close_path()
        rgba(ctx, GOLD); ctx.fill()
    circle(ctx, px, py, R * 0.55, NAVY)
    bee(ctx, px - 10 * U, py, 1.5 * U, t, 1)
    text(ctx, "ALL KNOWN ANIMALS", px, py - R - 50 * U, 38 * U, WHITE, prog(t, 3.5, 4.2))
    k = prog(t, 6.5, 7.5)
    if k:
        ang = -math.pi / 2 + frac * math.pi
        lx = px + math.cos(ang) * R * 1.25; ly = py + math.sin(ang) * R * 1.25
        text(ctx, "INSECTS: MORE", lx + (40 if not VERT else 0) * U, ly - 26 * U if not VERT else py + R + 50 * U, 36 * U, GOLD, k, True, "l" if not VERT else "c")
        text(ctx, "THAN HALF", lx + (40 if not VERT else 0) * U, ly + 20 * U if not VERT else py + R + 95 * U, 36 * U, GOLD, k, True, "l" if not VERT else "c")
    # counter
    n = int(1000000 * prog(t, 0.8, 4.0))
    cx_, cy_ = (W * 0.27, CY - 60 * U) if not VERT else (CX, H * 0.20)
    text(ctx, f"{n:,}", cx_, cy_, 120 * U, GOLD, prog(t, 0.5, 1.0))
    text(ctx, "DESCRIBED SPECIES", cx_, cy_ + 95 * U, 40 * U, WHITE, prog(t, 0.5, 1.0))
    if not VERT:
        m = prog(t, d - 4.5, d - 3.0)
        if m:
            text(ctx, "+ MANY STILL UNKNOWN", cx_, cy_ + 175 * U, 36 * U, WHITE, 0.8 * m, False)
            for i in range(5):
                beetle(ctx, cx_ - 220 * U + i * 110 * U, cy_ + 270 * U, 0.8 * U, -math.pi / 2, (0.3, 0.3, 0.45), m * 0.9, t)
    else:
        m = prog(t, d - 4.5, d - 3.0)
        if m: text(ctx, "+ MANY STILL UNKNOWN", CX, H * 0.20 + 150 * U, 36 * U, WHITE, 0.8 * m, False)

def sc_pollen(ctx, t, d):
    vgrad(ctx, (0.10, 0.15, 0.32), (0.05, 0.08, 0.16)); stars(ctx, t, 0.35)
    yb = H * 0.78 if not VERT else H * 0.66
    meadow(ctx, t, yb)
    n = 4 if not VERT else 3
    heads = []
    cols = [PINK, VIOLET, CORAL, WHITE]
    for i in range(n):
        x = W * (0.16 + 0.68 * i / (n - 1))
        heads.append((x, yb + 30 * U - 230 * U))
    # bee path
    T0, T1 = 1.0, d - 1.5
    u = clamp((t - T0) / (T1 - T0)) * (n - 1)
    i0 = min(int(u), n - 2); f = ease(u - i0)
    (x0, y0), (x1, y1) = heads[i0], heads[i0 + 1]
    bx = x0 + (x1 - x0) * f; by = y0 + (y1 - y0) * f - math.sin(f * math.pi) * 200 * U - 70 * U
    # pollen trail
    random.seed(9)
    for k in range(80):
        uu = u - k * 0.02
        if uu < 0: break
        j = min(int(uu), n - 2); ff = ease(uu - j)
        (a0, b0), (a1, b1) = heads[j], heads[j + 1]
        px = a0 + (a1 - a0) * ff + random.uniform(-10, 10) * U; py = b0 + (b1 - b0) * ff - math.sin(ff * math.pi) * 200 * U - 50 * U + random.uniform(-10, 10) * U
        circle(ctx, px, py, 4 * U, GOLD, 0.8 * (1 - k / 80))
    for i in range(n):
        x = W * (0.16 + 0.68 * i / (n - 1))
        visited = clamp((u - i) * 2 + (1 if i == 0 else 0)) if i > 0 else clamp(u * 2)
        hx, hy = flower(ctx, x, yb + 30 * U, U * 1.3, cols[i % 4], 175, 0, 1, t * 0.3)
        if visited > 0:   # fruit forms
            r = 26 * U * ease(visited)
            circle(ctx, hx + 45 * U, hy + 40 * U, r, CORAL)
            ell(ctx, hx + 45 * U, hy + 40 * U - r, 8 * U, 4 * U, LEAF)
    bee(ctx, bx, by, 1.6 * U, t, 1, 0.2 * math.cos(f * math.pi))
    text(ctx, "POLLEN", heads[0][0], heads[0][1] - 150 * U if not VERT else heads[0][1] - 360 * U, 40 * U, GOLD, prog(t, 2, 3) * (1 if not VERT else 0))
    if VERT: text(ctx, "FLOWER → FLOWER → FRUIT", CX, H * 0.25, 44 * U, GOLD, prog(t, 2, 3))
    else: text(ctx, "FLOWER → FLOWER → FRUIT", W * 0.62, H * 0.12, 44 * U, GOLD, prog(t, 2, 3))
    chip(ctx, "CONSEQUENCE 1 · POLLINATION", t)

# food icons
def apple(ctx, x, y, s, a=1):
    circle(ctx, x - 10 * s, y, 30 * s, (0.92, 0.25, 0.3), a); circle(ctx, x + 10 * s, y, 30 * s, (0.92, 0.25, 0.3), a)
    line(ctx, [(x, y - 26 * s), (x + 4 * s, y - 44 * s)], (0.4, 0.25, 0.12), 5 * s, a); ell(ctx, x + 18 * s, y - 40 * s, 13 * s, 6 * s, LEAF, a, -0.4)

def strawberry(ctx, x, y, s, a=1):
    ctx.move_to(x - 30 * s, y - 18 * s); ctx.curve_to(x - 34 * s, y + 20 * s, x - 6 * s, y + 40 * s, x, y + 42 * s)
    ctx.curve_to(x + 6 * s, y + 40 * s, x + 34 * s, y + 20 * s, x + 30 * s, y - 18 * s); ctx.close_path(); rgba(ctx, (0.95, 0.2, 0.3), a); ctx.fill()
    for i in range(7):
        circle(ctx, x + (-18 + (i % 4) * 12) * s + (i // 4) * 6 * s, y + (-4 + (i // 4) * 18) * s, 2.6 * s, GOLD, a)
    for k in (-1, 0, 1): ell(ctx, x + k * 13 * s, y - 22 * s, 12 * s, 6 * s, LEAF, a, k * 0.5)

def almond(ctx, x, y, s, a=1):
    ell(ctx, x, y, 22 * s, 34 * s, (0.75, 0.52, 0.32), a, 0.3)
    line(ctx, [(x - 6 * s, y - 18 * s), (x + 4 * s, y + 18 * s)], (0.6, 0.4, 0.24), 3 * s, a)

def coffee(ctx, x, y, s, a=1):
    rrect(ctx, x - 30 * s, y - 24 * s, 60 * s, 54 * s, 10 * s); rgba(ctx, WHITE, a); ctx.fill()
    ctx.arc(x + 32 * s, y + 2 * s, 12 * s, -1.4, 1.4); rgba(ctx, WHITE, a); ctx.set_line_width(6 * s); ctx.stroke()
    ell(ctx, x, y - 20 * s, 26 * s, 6 * s, (0.4, 0.24, 0.12), a)
    for k in (-1, 1): line(ctx, [(x + k * 10 * s, y - 34 * s), (x + k * 10 * s + 6 * s, y - 50 * s), (x + k * 10 * s, y - 62 * s)], WHITE, 3 * s, 0.5 * a)

def choco(ctx, x, y, s, a=1):
    rrect(ctx, x - 34 * s, y - 26 * s, 68 * s, 52 * s, 6 * s); rgba(ctx, (0.42, 0.24, 0.14), a); ctx.fill()
    for i in range(3):
        for j in range(2):
            rrect(ctx, x - 30 * s + i * 21 * s, y - 22 * s + j * 23 * s, 18 * s, 20 * s, 3 * s); rgba(ctx, (0.52, 0.32, 0.2), a); ctx.fill()

def wheat(ctx, x, y, s, a=1):
    line(ctx, [(x, y + 40 * s), (x, y - 30 * s)], GOLD, 4 * s, a)
    for k in range(4):
        for sg in (-1, 1): ell(ctx, x + sg * 8 * s, y - 24 * s + k * 14 * s, 7 * s, 11 * s, GOLD, a, sg * 0.5)
    ell(ctx, x, y - 34 * s, 6 * s, 10 * s, GOLD, a)

def corn(ctx, x, y, s, a=1):
    ell(ctx, x, y, 18 * s, 38 * s, (1.0, 0.85, 0.3), a)
    for k in range(5): line(ctx, [(x - 14 * s, y - 26 * s + k * 13 * s), (x + 14 * s, y - 26 * s + k * 13 * s)], (0.85, 0.65, 0.2), 2 * s, a)
    ell(ctx, x - 16 * s, y + 18 * s, 10 * s, 30 * s, LEAF, a, 0.4); ell(ctx, x + 16 * s, y + 18 * s, 10 * s, 30 * s, LEAF, a, -0.4)

def rice(ctx, x, y, s, a=1):
    ctx.move_to(x, y + 40 * s); ctx.curve_to(x, y, x + 10 * s, y - 20 * s, x + 30 * s, y - 30 * s)
    rgba(ctx, (0.75, 0.8, 0.45), a); ctx.set_line_width(4 * s); ctx.stroke()
    for k in range(5): ell(ctx, x + 8 * s + k * 5 * s, y - 6 * s - k * 6 * s, 5 * s, 3 * s, (0.95, 0.92, 0.75), a, -0.6)

def sc_plate(ctx, t, d):
    vgrad(ctx, NAVY2, NAVY); stars(ctx, t, 0.3)
    loss = prog(t, d * 0.62, d * 0.75)
    pol = [apple, strawberry, almond, coffee, choco]
    wnd = [wheat, rice, corn]
    if VERT:
        a1x, a1y, a2y = CX, H * 0.33, H * 0.56
        circle(ctx, CX, a1y, 330 * U, (0.9, 0.92, 0.96), 0.12); circle(ctx, CX, a1y, 270 * U, (0.9, 0.92, 0.96), 0.08)
        pos = [(CX - 170 * U, a1y - 80 * U), (CX, a1y - 120 * U), (CX + 170 * U, a1y - 80 * U), (CX - 100 * U, a1y + 80 * U), (CX + 100 * U, a1y + 80 * U)]
        wpos = [(CX - 180 * U, a2y + 30 * U), (CX, a2y + 30 * U), (CX + 180 * U, a2y + 30 * U)]
        lab1 = (CX, H * 0.165); lab2 = (CX, a2y - 70 * U)
    else:
        a1y = CY - 30 * U
        circle(ctx, W * 0.33, a1y, 300 * U, (0.9, 0.92, 0.96), 0.12); circle(ctx, W * 0.33, a1y, 240 * U, (0.9, 0.92, 0.96), 0.08)
        pos = [(W * 0.33 - 160 * U, a1y - 80 * U), (W * 0.33, a1y - 120 * U), (W * 0.33 + 160 * U, a1y - 80 * U), (W * 0.33 - 90 * U, a1y + 90 * U), (W * 0.33 + 90 * U, a1y + 90 * U)]
        wpos = [(W * 0.70 + k * 170 * U, a1y + 20 * U) for k in range(3)]
        lab1 = (W * 0.33, a1y - 340 * U + 40 * U); lab2 = (W * 0.87, a1y - 150 * U)
        lab2 = (W * 0.87, a1y - 130 * U)
    for i, (fn, (x, y)) in enumerate(zip(pol, pos)):
        ap = prog(t, 6.0 + i * 0.7, 6.6 + i * 0.7)
        fn(ctx, x, y, 1.4 * U, ap * (1 - 0.8 * loss))
        if loss: dashed_ring(ctx, x, y, 62 * U, 0.6 * loss)
    w = prog(t, d * 0.42, d * 0.52)
    for fn, (x, y) in zip(wnd, wpos): fn(ctx, x, y, 1.5 * U, w)
    if VERT:
        text(ctx, "≈ 3/4 OF LEADING CROPS", CX, lab1[1], 44 * U, GOLD, prog(t, 1, 2))
        text(ctx, "RELY PARTLY ON POLLINATORS", CX, lab1[1] + 55 * U, 36 * U, WHITE, prog(t, 1.5, 2.5), False)
        text(ctx, "WIND-POLLINATED", CX, lab2[1], 40 * U, WHITE, w)
    else:
        text(ctx, "≈ 3/4 OF LEADING CROPS", W * 0.33, 150 * U + 40 * U, 48 * U, GOLD, prog(t, 1, 2))
        text(ctx, "RELY PARTLY ON POLLINATORS", W * 0.33, 205 * U + 40 * U, 34 * U, WHITE, prog(t, 1.5, 2.5), False)
        text(ctx, "WIND-POLLINATED", W * 0.87 - 170 * U, a1y - 130 * U, 42 * U, WHITE, w)
        for k in range(3):
            yy = a1y + 150 * U + k * 26 * U; xo = (t * 200 * U + k * 120 * U) % (520 * U)
            line(ctx, [(W * 0.60 + xo, yy), (W * 0.60 + xo + 80 * U, yy)], WHITE, 3 * U, 0.4 * w)
    if loss:
        text(ctx, "MUCH POORER PLATES", CX if VERT else W * 0.33, (H * 0.165 + 115 * U) if VERT else a1y + 260 * U, 40 * U, CORAL, loss)

# animals for the food web
def bird(ctx, x, y, s, c=(0.55, 0.75, 0.95), a=1.0, t=0.0):
    ell(ctx, x, y, 34 * s, 24 * s, c, a)
    circle(ctx, x + 28 * s, y - 16 * s, 16 * s, c, a)
    ctx.move_to(x + 42 * s, y - 20 * s); ctx.line_to(x + 60 * s, y - 14 * s); ctx.line_to(x + 42 * s, y - 8 * s); rgba(ctx, GOLD, a); ctx.fill()
    circle(ctx, x + 32 * s, y - 20 * s, 3.5 * s, NAVY, a)
    fl = math.sin(t * 8) * 0.4
    ell(ctx, x - 6 * s, y - 6 * s, 24 * s, 12 * s, mix(c, NAVY, 0.3), a, -0.3 + fl)
    ctx.move_to(x - 30 * s, y - 4 * s); ctx.line_to(x - 56 * s, y - 16 * s); ctx.line_to(x - 52 * s, y + 6 * s); rgba(ctx, c, a); ctx.fill()

def frog(ctx, x, y, s, a=1.0):
    c = (0.35, 0.8, 0.4)
    ell(ctx, x, y, 40 * s, 26 * s, c, a)
    for sg in (-1, 1):
        circle(ctx, x + sg * 20 * s, y - 24 * s, 12 * s, c, a); circle(ctx, x + sg * 20 * s, y - 24 * s, 6 * s, WHITE, a); circle(ctx, x + sg * 20 * s, y - 24 * s, 3 * s, NAVY, a)
        ell(ctx, x + sg * 38 * s, y + 18 * s, 18 * s, 8 * s, mix(c, NAVY, 0.2), a)
    line(ctx, [(x - 14 * s, y + 2 * s), (x + 14 * s, y + 2 * s)], NAVY, 3 * s, a)

def fish(ctx, x, y, s, a=1.0):
    c = (0.4, 0.7, 1.0)
    ell(ctx, x, y, 44 * s, 22 * s, c, a)
    ctx.move_to(x - 38 * s, y); ctx.line_to(x - 66 * s, y - 22 * s); ctx.line_to(x - 66 * s, y + 22 * s); ctx.close_path(); rgba(ctx, c, a); ctx.fill()
    circle(ctx, x + 24 * s, y - 6 * s, 4 * s, NAVY, a)

def bat(ctx, x, y, s, a=1.0, t=0.0):
    c = (0.55, 0.45, 0.7); f = 0.7 + 0.3 * math.sin(t * 7)
    for sg in (-1, 1):
        ctx.move_to(x, y - 8 * s); ctx.line_to(x + sg * 60 * s, y - 22 * s * f); ctx.line_to(x + sg * 50 * s, y + 8 * s)
        ctx.line_to(x + sg * 36 * s, y); ctx.line_to(x + sg * 24 * s, y + 12 * s); ctx.line_to(x + sg * 10 * s, y + 4 * s); ctx.close_path(); rgba(ctx, c, a); ctx.fill()
    ell(ctx, x, y, 12 * s, 18 * s, c, a)
    for sg in (-1, 1):
        ctx.move_to(x + sg * 4 * s, y - 14 * s); ctx.line_to(x + sg * 11 * s, y - 28 * s); ctx.line_to(x + sg * 11 * s, y - 12 * s); ctx.fill()

def hawk(ctx, x, y, s, a=1.0, t=0.0):
    c = (0.75, 0.55, 0.35); f = math.sin(t * 2) * 0.15
    for sg in (-1, 1):
        ctx.move_to(x, y); ctx.curve_to(x + sg * 40 * s, y - 40 * s * (1 + f), x + sg * 90 * s, y - 30 * s, x + sg * 110 * s, y - 10 * s)
        ctx.curve_to(x + sg * 70 * s, y + 4 * s, x + sg * 30 * s, y + 10 * s, x, y + 14 * s); rgba(ctx, c, a); ctx.fill()
    ell(ctx, x, y + 10 * s, 16 * s, 30 * s, c, a)
    circle(ctx, x, y - 20 * s, 13 * s, (0.95, 0.92, 0.85), a)
    ctx.move_to(x - 4 * s, y - 14 * s); ctx.line_to(x, y - 4 * s); ctx.line_to(x + 4 * s, y - 14 * s); rgba(ctx, GOLD, a); ctx.fill()

def cross(ctx, x, y, r, a):
    line(ctx, [(x - r, y - r), (x + r, y + r)], CORAL, 10 * U, a)
    line(ctx, [(x + r, y - r), (x - r, y + r)], CORAL, 10 * U, a)

def sc_foodweb(ctx, t, d):
    vgrad(ctx, NAVY2, NAVY); stars(ctx, t, 0.35)
    kill1 = prog(t, d * 0.55, d * 0.65); kill2 = prog(t, d * 0.70, d * 0.80); kill3 = prog(t, d * 0.84, d * 0.92)
    if VERT:
        ly = [H * 0.60, H * 0.43, H * 0.25]; xs = [W * 0.2, W * 0.4, W * 0.6, W * 0.8]
    else:
        ly = [H * 0.66, H * 0.43, H * 0.18]; xs = [W * 0.26, W * 0.42, W * 0.58, W * 0.74]
    R = 70 * U
    # links
    for xx in xs:
        line(ctx, [(CX + (xx - CX) * 0.4, ly[0] - R), (xx, ly[1] + R)], WHITE, 3 * U, 0.3 * (1 - kill2 * 0.7))
        line(ctx, [(xx, ly[1] - R), (CX, ly[2] + R)], WHITE, 3 * U, 0.3 * (1 - kill3 * 0.7))
    # level 0: insects
    circle(ctx, CX, ly[0], R * 1.6, (0.2, 0.25, 0.45), 1 - 0.6 * kill1)
    bee(ctx, CX - 60 * U, ly[0] - 10 * U, 1.0 * U, t, 1 - kill1)
    beetle(ctx, CX + 60 * U, ly[0] + 20 * U, 0.8 * U, 0.3, (0.25, 0.75, 0.6), 1 - kill1, t)
    butterfly(ctx, CX + 10 * U, ly[0] - 50 * U, 0.7 * U, t, PINK, 1 - kill1)
    text(ctx, "INSECTS", CX, ly[0] + R * 1.6 + 40 * U, 36 * U, GOLD, 1 - kill1 * 0.5)
    if kill1: cross(ctx, CX, ly[0], 70 * U, kill1)
    # level 1
    fns = [lambda x, y, a: bird(ctx, x, y, 1.0 * U, (0.55, 0.75, 0.95), a, t), lambda x, y, a: bat(ctx, x, y, 1.0 * U, a, t),
           lambda x, y, a: frog(ctx, x, y, 1.0 * U, a), lambda x, y, a: fish(ctx, x + 10 * U, y, 1.0 * U, a)]
    for xx, fn in zip(xs, fns):
        circle(ctx, xx, ly[1], R, (0.2, 0.25, 0.45), 1 - 0.5 * kill2)
        fn(xx, ly[1], 1 - 0.7 * kill2)
    if VERT: text(ctx, "BIRDS · BATS · FROGS · FISH", CX, ly[1] + R + 45 * U, 34 * U, WHITE, 0.9 * (1 - kill2 * 0.5))
    else: text(ctx, "BIRDS · BATS · FROGS · FISH", CX, ly[1] + R + 42 * U, 32 * U, WHITE, 0.9 * (1 - kill2 * 0.5))
    if kill2:
        for xx in xs: cross(ctx, xx, ly[1], 40 * U, kill2)
    # level 2
    circle(ctx, CX, ly[2], R * 1.15, (0.2, 0.25, 0.45), 1 - 0.5 * kill3)
    hawk(ctx, CX, ly[2], 0.62 * U, 1 - 0.7 * kill3, t)
    text(ctx, "PREDATORS", CX + (R * 1.15 + 30 * U) * (1 if not VERT else 0), ly[2] + (0 if not VERT else R * 1.15 + 40 * U), 34 * U, WHITE, 0.9, True, "l" if not VERT else "c")
    if kill3: cross(ctx, CX, ly[2], 46 * U, kill3)
    chip(ctx, "CONSEQUENCE 2 · THE FOOD CHAIN", t)

def dung(ctx, x, y, s, a=1.0):
    for k, (rx, ry, dy) in enumerate([(60, 20, 0), (44, 16, -18), (28, 13, -32)]):
        ell(ctx, x, y + dy * s, rx * s, ry * s, mix((0.38, 0.26, 0.16), (0.28, 0.18, 0.1), k / 2), a)

def leafshape(ctx, x, y, s, rot, c, a=1.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot)
    ctx.move_to(-30 * s, 0); ctx.curve_to(-10 * s, -22 * s, 18 * s, -18 * s, 32 * s, 0); ctx.curve_to(18 * s, 18 * s, -10 * s, 22 * s, -30 * s, 0)
    rgba(ctx, c, a); ctx.fill(); line(ctx, [(-30 * s, 0), (30 * s, 0)], mix(c, NAVY, 0.4), 2 * s, a); ctx.restore()

def sc_cleanup(ctx, t, d):
    vgrad(ctx, (0.08, 0.12, 0.26), (0.05, 0.08, 0.16)); stars(ctx, t, 0.3)
    gy = H * 0.66 if not VERT else H * 0.60
    rgba(ctx, (0.18, 0.30, 0.18)); ctx.rectangle(0, gy, W, H - gy); ctx.fill()
    rgba(ctx, (0.24, 0.40, 0.22)); ctx.move_to(0, gy)
    for i in range(41): ctx.line_to(W * i / 40, gy - 10 * U * abs(math.sin(i * 1.3)))
    ctx.line_to(W, gy + 10 * U); ctx.line_to(0, gy + 10 * U); ctx.close_path(); ctx.fill()
    eat = prog(t, 2.0, d * 0.45)
    # log
    lx = W * 0.22 if not VERT else W * 0.30
    lw = 380 * U if not VERT else 300 * U
    rrect(ctx, lx - lw / 2, gy - 90 * U, lw * (1 - 0.45 * eat), 90 * U, 40 * U); rgba(ctx, (0.45, 0.30, 0.18)); ctx.fill()
    for k in range(3): line(ctx, [(lx - lw / 2 + 50 * U + k * 70 * U, gy - 60 * U), (lx - lw / 2 + 110 * U + k * 70 * U, gy - 60 * U)], (0.32, 0.2, 0.12), 4 * U)
    # leaves shrinking
    random.seed(21)
    for k in range(8):
        x = lx - lw / 2 + random.random() * lw * 1.2; y = gy + 30 * U + random.random() * 60 * U
        leafshape(ctx, x, y, 1.2 * U * (1 - 0.8 * eat), random.random() * 3, random.choice([(0.85, 0.55, 0.2), (0.8, 0.35, 0.2), GOLD]))
    beetle(ctx, lx + 80 * U, gy - 120 * U, 0.8 * U, 0.1, (0.25, 0.75, 0.6), 1, t)
    beetle(ctx, lx - 120 * U, gy + 70 * U, 0.7 * U, 2.8, (0.6, 0.4, 0.8), 1, t)
    ant(ctx, lx + 10 * U + 30 * U * math.sin(t), gy + 100 * U, 1.0 * U, 0.2, t)
    # dung beetle rolling a ball
    p = prog(t, d * 0.45, d * 0.95)
    dx = W * 0.74 if not VERT else W * 0.72
    dung(ctx, dx, gy + 20 * U, 1.2 * U, prog(t, d * 0.4, d * 0.5))
    if p > 0:
        bx = dx - 140 * U - 260 * U * p * (1 if not VERT else 0.6); by = gy + 170 * U if not VERT else gy + 260 * U
        if VERT: bx = dx - 160 * U - 180 * U * p
        rb = 34 * U
        ctx.save(); ctx.translate(bx, by - rb); ctx.rotate(-p * 8)
        circle(ctx, 0, 0, rb, (0.38, 0.26, 0.16)); line(ctx, [(-rb * 0.5, -rb * 0.3), (rb * 0.3, rb * 0.5)], (0.28, 0.18, 0.1), 3 * U)
        ctx.restore()
        ctx.save(); ctx.translate(bx + rb + 34 * U, by - 30 * U); ctx.rotate(-2.6); beetle(ctx, 0, 0, 0.75 * U, 0, (0.15, 0.15, 0.2), 1, t * 2); ctx.restore()
        text(ctx, "AUSTRALIA · 1960s", dx if not VERT else CX, H * 0.20 if not VERT else H * 0.26, 46 * U, GOLD, prog(t, d * 0.55, d * 0.62))
        text(ctx, "DUNG BEETLES BROUGHT IN", dx if not VERT else CX, H * 0.20 + 58 * U if not VERT else H * 0.26 + 58 * U, 34 * U, WHITE, prog(t, d * 0.6, d * 0.67), False)
    text(ctx, "NATURE'S RECYCLERS", lx if not VERT else CX, H * 0.30 if not VERT else H * 0.18 + 90 * U, 42 * U, WHITE, prog(t, 1, 2) * (1 - prog(t, d * 0.5, d * 0.55) * (1 if VERT else 0)))
    chip(ctx, "CONSEQUENCE 3 · THE CLEANUP", t)

def sc_soil(ctx, t, d):
    vgrad(ctx, (0.12, 0.18, 0.36), (0.08, 0.12, 0.25), 0, H * 0.3)
    gy = H * 0.30 if not VERT else H * 0.22
    vgrad(ctx, (0.12, 0.18, 0.36), (0.18, 0.28, 0.45), 0, gy)
    g = cairo.LinearGradient(0, gy, 0, H); g.add_color_stop_rgb(0, *SOIL); g.add_color_stop_rgb(1, SOIL_D[0] * 0.6, SOIL_D[1] * 0.6, SOIL_D[2] * 0.6)
    ctx.set_source(g); ctx.rectangle(0, gy, W, H - gy); ctx.fill()
    random.seed(30)
    for _ in range(90):
        circle(ctx, random.random() * W, gy + random.random() * (H - gy), random.uniform(3, 9) * U, (0.45, 0.32, 0.22), 0.5)
    # grass + plants
    rgba(ctx, LEAF); ctx.rectangle(0, gy - 10 * U, W, 14 * U); ctx.fill()
    grow = 1 - 0.35 * prog(t, d * 0.65, d * 0.85)
    for i, x in enumerate([W * 0.15, W * 0.5, W * 0.85]):
        hh = 140 * U * grow
        line(ctx, [(x, gy), (x, gy - hh)], LEAF, 8 * U)
        for k in range(3): ell(ctx, x + (-1) ** k * 28 * U, gy - hh * (0.4 + k * 0.2), 30 * U * grow, 12 * U * grow, LEAF, 1, (-1) ** k * 0.4)
        line(ctx, [(x, gy), (x - 30 * U, gy + 120 * U), (x - 50 * U, gy + 200 * U * grow)], (0.85, 0.75, 0.55), 4 * U, 0.8)
        line(ctx, [(x, gy), (x + 25 * U, gy + 140 * U * grow)], (0.85, 0.75, 0.55), 4 * U, 0.8)
    # tunnels dug progressively
    p = prog(t, 0.5, d * 0.55)
    tunnels = [[(W * 0.33, gy), (W * 0.30, gy + 150 * U), (W * 0.36, gy + 280 * U), (W * 0.28, gy + 420 * U)],
               [(W * 0.67, gy), (W * 0.70, gy + 120 * U), (W * 0.63, gy + 260 * U), (W * 0.72, gy + 380 * U), (W * 0.66, gy + 470 * U)]]
    if VERT:
        tunnels = [[(x, y + (y - gy) * 0.6) for (x, y) in tt] for tt in tunnels]
    for tt in tunnels:
        n = len(tt) - 1; m = p * n
        pts = [tt[0]]
        for i in range(n):
            if m <= i: break
            f = min(1, m - i); a0, b0 = tt[i]; a1, b1 = tt[i + 1]
            pts.append((a0 + (a1 - a0) * f, b0 + (b1 - b0) * f))
        if len(pts) > 1:
            line(ctx, pts, (0.10, 0.06, 0.04), 34 * U)
            for (x, y) in pts[1:-1]: circle(ctx, x, y, 30 * U, (0.10, 0.06, 0.04))
            hx, hy = pts[-1]; px_, py_ = pts[-2]
            ant(ctx, hx, hy, 1.0 * U, math.atan2(hy - py_, hx - px_), t, (0.75, 0.35, 0.2))
        # air bubbles and water drops flowing down once dug
        fl = prog(t, d * 0.45, d * 0.55)
        if fl:
            for k in range(6):
                u = ((t * 0.25 + k / 6) % 1) * n
                i = int(u); f = u - i; a0, b0 = tt[i]; a1, b1 = tt[i + 1]
                x, y = a0 + (a1 - a0) * f, b0 + (b1 - b0) * f
                if k % 2: circle(ctx, x, y, 8 * U, (0.4, 0.75, 1.0), fl)
                else:
                    ctx.arc(x, y, 8 * U, 0, 2 * math.pi); rgba(ctx, WHITE, 0.8 * fl); ctx.set_line_width(3 * U); ctx.stroke()
    a = prog(t, d * 0.4, d * 0.5)
    if VERT:
        text(ctx, "AIR + WATER", CX, H * 0.12, 56 * U, GOLD, a)
        text(ctx, "INTO THE SOIL", CX, H * 0.12 + 66 * U, 40 * U, WHITE, a, False)
    else:
        text(ctx, "AIR + WATER INTO THE SOIL", W * 0.62, H * 0.12, 52 * U, GOLD, a)

def mushroom(ctx, x, y, s, c=(0.9, 0.35, 0.3), a=1):
    rrect(ctx, x - 9 * s, y - 40 * s, 18 * s, 40 * s, 6 * s); rgba(ctx, MOON, a); ctx.fill()
    ctx.arc(x, y - 38 * s, 32 * s, math.pi, 0); ctx.close_path(); rgba(ctx, c, a); ctx.fill()
    for dx in (-14, 4, 16): circle(ctx, x + dx * s, y - 52 * s + abs(dx) * 0.5 * s, 4 * s, WHITE, a)

def sc_winners(ctx, t, d):
    dull = prog(t, d * 0.6, d * 0.85)
    vgrad(ctx, mix((0.12, 0.18, 0.36), (0.12, 0.13, 0.17), dull), mix((0.18, 0.28, 0.42), (0.16, 0.17, 0.2), dull))
    stars(ctx, t, 0.3)
    gy = H * 0.70 if not VERT else H * 0.64
    rgba(ctx, mix((0.18, 0.32, 0.18), (0.25, 0.27, 0.25), dull)); ctx.rectangle(0, gy, W, H - gy); ctx.fill()
    # grass blades swaying in the wind
    random.seed(40)
    gc = mix((0.55, 0.78, 0.35), (0.55, 0.58, 0.5), dull)
    for i in range(70 if not VERT else 45):
        x = random.random() * W; hgt = random.uniform(120, 260) * U * (0.6 + 0.4 * prog(t, 0, 3))
        sway = math.sin(t * 2 + x * 0.01) * 30 * U
        ctx.move_to(x - 6 * U, gy + 8 * U); ctx.curve_to(x, gy - hgt * 0.5, x + sway * 0.6, gy - hgt * 0.8, x + sway, gy - hgt)
        ctx.curve_to(x + sway * 0.5, gy - hgt * 0.7, x + 6 * U, gy - hgt * 0.4, x + 6 * U, gy + 8 * U); rgba(ctx, gc, 0.9); ctx.fill()
        if i % 6 == 0:
            for k in range(4): ell(ctx, x + sway + (k - 1.5) * 2 * U, gy - hgt + k * 12 * U, 5 * U, 9 * U, mix(GOLD, (0.6, 0.6, 0.55), dull), 1, 0.3)
    # wind lines
    for k in range(4):
        yy = H * (0.25 + 0.07 * k); xo = (t * 300 * U + k * 400 * U) % (W + 400 * U) - 200 * U
        line(ctx, [(xo, yy), (xo + 160 * U, yy - 8 * U), (xo + 220 * U, yy + 4 * U)], WHITE, 4 * U, 0.35)
    m = prog(t, 4.0, 5.5)
    for i, (fx, sc) in enumerate([(0.12, 1.4), (0.2, 1.0), (0.82, 1.6), (0.9, 1.1), (0.5, 1.2)]):
        mushroom(ctx, W * fx, gy + 70 * U + (i % 2) * 30 * U, sc * U * m, mix((0.9, 0.35, 0.3), (0.6, 0.55, 0.55), dull), m)
    a1 = prog(t, 0.6, 1.4)
    ty = H * 0.13 if not VERT else H * 0.20
    text(ctx, "WINNERS?", CX, ty, 60 * U, GOLD, a1 * (1 - dull))
    text(ctx, "GRASSES · FUNGI · BACTERIA", CX, ty + 70 * U, 38 * U, WHITE, prog(t, 4, 5) * (1 - dull), False)
    if dull:
        text(ctx, "QUIETER · DULLER · LESS DIVERSE", CX, ty + 30 * U, 46 * U if not VERT else 40 * U, WHITE, dull)

def sc_decline(ctx, t, d):
    vgrad(ctx, NAVY2, NAVY); stars(ctx, t, 0.3)
    if VERT: bx, by0, bw, bh = CX - 110 * U, H * 0.62, 220 * U, 620 * U
    else: bx, by0, bw, bh = W * 0.30 - 120 * U, H * 0.74, 240 * U, 560 * U
    p = prog(t, 4.5, 9.0)
    v = 1 - 0.76 * p
    rgba(ctx, WHITE, 0.25); ctx.set_line_width(3 * U); ctx.move_to(bx - 60 * U, by0); ctx.line_to(bx + bw + 60 * U, by0); ctx.stroke()
    ctx.set_dash([10 * U, 10 * U]); rrect(ctx, bx, by0 - bh, bw, bh, 14 * U); rgba(ctx, WHITE, 0.4 * p); ctx.stroke(); ctx.set_dash([])
    rrect(ctx, bx, by0 - bh * v, bw, bh * v, 14 * U); rgba(ctx, GOLD); ctx.fill()
    # insects on bar fading
    random.seed(50)
    for k in range(12):
        x = bx + 30 * U + random.random() * (bw - 60 * U); y = by0 - bh * random.random()
        alive = 1 if y > by0 - bh * v else 1 - p
        bee(ctx, x, y, 0.55 * U, t + k, alive * 0.9)
    pct = int(round(76 * p))
    text(ctx, f"−{pct}%" if pct else "100%", bx + bw / 2, by0 - bh * v - 50 * U, 72 * U, CORAL if pct else WHITE, prog(t, 4, 4.5))
    if VERT:
        text(ctx, "FLYING INSECTS · GERMANY", CX, H * 0.16, 42 * U, GOLD, prog(t, 3.5, 4.5))
        text(ctx, "UNDER 30 YEARS (ONE STUDY)", CX, H * 0.16 + 52 * U, 32 * U, WHITE, prog(t, 3.5, 4.5), False)
        tags = ["HABITAT LOSS", "PESTICIDES", "CLIMATE CHANGE"]
        for i, tg in enumerate(tags):
            k = prog(t, d - 5.5 + i * 0.6, d - 5.0 + i * 0.6)
            text(ctx, tg, CX, H * 0.83 + i * 60 * U, 40 * U, WHITE, k)
    else:
        text(ctx, "FLYING INSECTS", bx + bw / 2, H * 0.08, 44 * U, GOLD, prog(t, 3.5, 4.5))
        text(ctx, "GERMAN RESERVES · UNDER 30 YEARS", bx + bw / 2, H * 0.08 + 54 * U, 30 * U, WHITE, prog(t, 3.5, 4.5), False)
        tags = ["HABITAT LOSS", "PESTICIDES", "CLIMATE CHANGE"]
        text(ctx, "SUSPECTED CAUSES", W * 0.70, H * 0.26, 40 * U, GOLD, prog(t, d - 6.5, d - 5.8))
        for i, tg in enumerate(tags):
            k = prog(t, d - 5.5 + i * 0.6, d - 5.0 + i * 0.6)
            font(ctx, 40 * U); w = ctx.text_extents(tg).width + 70 * U
            rrect(ctx, W * 0.70 - w / 2, H * 0.34 + i * 110 * U, w, 80 * U, 40 * U); rgba(ctx, (0.2, 0.25, 0.45), 0.9 * k); ctx.fill()
            text(ctx, tg, W * 0.70, H * 0.34 + i * 110 * U + 40 * U, 40 * U, WHITE, k)

def sc_outro(ctx, t, d):
    vgrad(ctx, NAVY2, NAVY); stars(ctx, t, 0.6)
    yo = -80 * U if not VERT else -200 * U
    bee(ctx, CX + 160 * math.sin(t * 0.7) * U, CY + yo - 200 * U + 20 * U * math.sin(t * 1.6), 1.5 * U, t, 1, 0.15 * math.cos(t * 0.7))
    text(ctx, "FACTORA", CX, CY + yo, 140 * U, WHITE, prog(t, 0, 0.6))
    text(ctx, "fascinating facts, explained", CX, CY + yo + 100 * U, 38 * U, GOLD, prog(t, 0.4, 1.0), False)
    k = prog(t, d * 0.6, d * 0.7)
    if k:
        bw, bh = 520 * U, 110 * U
        pop = 1 + 0.05 * math.sin(t * 6)
        ctx.save(); ctx.translate(CX, CY + yo + 260 * U); ctx.scale(pop * k, pop * k)
        rrect(ctx, -bw / 2, -bh / 2, bw, bh, 22 * U); rgba(ctx, (0.85, 0.12, 0.12)); ctx.fill()
        text(ctx, "SUBSCRIBE", 0, 0, 52 * U, WHITE)
        ctx.restore()
    q = prog(t, d * 0.3, d * 0.4)
    if q and k < 1: text(ctx, "Which insect would you miss most?", CX, CY + yo + 260 * U, 44 * U, WHITE, q * (1 - k))

SHORT_SCENES = ["hook", "pollen", "foodweb", "outro"]

SCENES = dict(hook=sc_hook, title=sc_title, count=sc_count, pollen=sc_pollen, plate=sc_plate, foodweb=sc_foodweb,
              cleanup=sc_cleanup, soil=sc_soil, winners=sc_winners, decline=sc_decline, outro=sc_outro)

def thumbnail(c):
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, .08, .11, .26); g.add_color_stop_rgb(1, .02, .03, .08); c.set_source(g); c.paint()
    random.seed(1)
    for _ in range(150):
        c.arc(random.random() * W, random.random() * H, random.uniform(.5, 1.8), 0, 6.3); c.set_source_rgba(1, 1, 1, random.uniform(.3, .9)); c.fill()
    glow(c, 1010, 330, 330, GOLD, 0.30)
    flower(c, 1060, 720, 1.5, PINK, 230, 0.0, 1, 0)
    flower(c, 880, 720, 1.1, VIOLET, 200, 0.6, 1, 0)
    bee(c, 1000, 260, 3.3, 0.37, 1, -0.15)
    c.set_dash([18, 14]); c.arc(1000, 260, 190, 0, 2 * math.pi); c.set_source_rgba(1, 1, 1, .6); c.set_line_width(5); c.stroke(); c.set_dash([])
    thumb_text(c, "WHAT IF INSECTS", "VANISHED?", "CHAIN REACTION")
