# Episode 023 (Short only) - "What's hiding above your air fryer basket?" — realistic shaded illustrations (v2)
# Executed inside engine/render.py (helpers available). Vertical layout. Original vector illustration. All sizes in U.
# Facts: Philips Airfryer support (turn upside down on a soft cloth, soft-to-medium bristle brush, no steel brush,
# dry with paper towel), CHOICE (residue can smoke and even catch alight), Ireland CCPC warning (fire hazard).
# v2 (Nazik 2026-11-10: "plus réaliste"): cut-away air fryer with metal shading, glowing tube heating element with
# burnt crust, fan, basket of fries, kitchen counter; flipped unit on a towel for the cleaning steps.

CRUST = (0.10, 0.06, 0.03)
HOTC = (1.0, 0.36, 0.12)

def lin(x0, y0, x1, y1, stops):
    g = cairo.LinearGradient(x0, y0, x1, y1)
    for o, c, al in stops: g.add_color_stop_rgba(o, c[0], c[1], c[2], al)
    return g

def kitchen(ctx, t, counter_y):
    """Dark kitchen: tiled wall + stone counter, soft warm light."""
    ctx.set_source(lin(0, 0, 0, counter_y, [(0, (0.09, 0.10, 0.14), 1), (1, (0.16, 0.16, 0.20), 1)])); ctx.paint()
    ctx.set_line_width(2 * U)
    for i in range(1, 12):
        ctx.move_to(0, counter_y - i * 110 * U); ctx.line_to(W, counter_y - i * 110 * U)
    for j in range(0, 9):
        ctx.move_to(j * 180 * U, 0); ctx.line_to(j * 180 * U, counter_y)
    rgba(ctx, WHITE, 0.05); ctx.stroke()
    glow(ctx, W * 0.75, counter_y * 0.25, 700 * U, (1.0, 0.85, 0.6), 0.10)
    ctx.rectangle(0, counter_y, W, H - counter_y)
    ctx.set_source(lin(0, counter_y, 0, H, [(0, (0.30, 0.27, 0.25), 1), (0.08, (0.17, 0.15, 0.14), 1), (1, (0.06, 0.05, 0.05), 1)])); ctx.fill()
    rnd = random.Random(3)
    for i in range(60):
        circle(ctx, rnd.random() * W, counter_y + rnd.random() * (H - counter_y), rnd.uniform(2, 5) * U, WHITE, 0.05)

def spiral(c, cx, cy, r, k, turns=3.4, r0=0.16, n=320):
    for i in range(n + 1):
        th = i / n * turns * 2 * math.pi; rr = r * (r0 + (1 - r0) * i / n)
        px, py = cx + math.cos(th) * rr, cy + math.sin(th) * rr * k
        (c.move_to if i == 0 else c.line_to)(px, py)

def tube(ctx, draw, w, base, a=1.0):
    """Metal tube look: dark edge, body colour, specular line."""
    for ww, col, al, dy in ((w, mix(base, (0, 0, 0), 0.55), 1.0, 0), (w * 0.72, base, 1.0, 0), (w * 0.22, mix(base, WHITE, 0.65), 0.9, -w * 0.18)):
        ctx.save(); ctx.translate(0, dy); ctx.new_path(); draw(ctx)
        ctx.set_line_width(ww); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        rgba(ctx, col, al * a); ctx.stroke(); ctx.restore()

def crusts(ctx, cx, cy, r, k, amount, S, a, seed=11, turns=3.4, r0=0.16):
    if amount <= 0: return
    rnd = random.Random(seed)
    for i in range(int(46 * amount)):
        u = rnd.random(); th = u * turns * 2 * math.pi; rr = r * (r0 + (1 - r0) * u)
        px, py = cx + math.cos(th) * rr, cy + math.sin(th) * rr * k
        rx = rnd.uniform(9, 20) * S
        ctx.save(); ctx.translate(px, py); ctx.scale(1, 0.6)
        ctx.arc(0, 0, rx * 1.5, 0, 2 * math.pi); rgba(ctx, (0.35, 0.18, 0.05), 0.45 * a); ctx.fill()
        ctx.arc(0, 0, rx, 0, 2 * math.pi); rgba(ctx, CRUST, 0.95 * a); ctx.fill()
        ctx.restore()

def heater(ctx, cx, cy, r, k, S, t, heat, grime, a=1.0):
    col = mix((0.62, 0.60, 0.58), HOTC, heat)
    if heat > 0: glow(ctx, cx, cy, r * 1.5, HOTC, 0.45 * heat * a)
    tube(ctx, lambda c: spiral(c, cx, cy, r, k), 20 * S, col, a)
    crusts(ctx, cx, cy, r, k, grime, S, a)

def fan(ctx, cx, cy, rx, k, S, t, a=1.0):
    ctx.save(); ctx.translate(cx, cy); ctx.scale(1, k)
    ctx.arc(0, 0, rx, 0, 2 * math.pi); rgba(ctx, (0.10, 0.10, 0.12), a); ctx.fill()
    for i in range(7):
        an = t * 10 + i * 2 * math.pi / 7
        ctx.move_to(0, 0); ctx.arc(0, 0, rx * 0.92, an, an + 0.5); ctx.close_path()
        rgba(ctx, (0.45, 0.46, 0.50), 0.9 * a); ctx.fill()
    ctx.arc(0, 0, rx * 0.18, 0, 2 * math.pi); rgba(ctx, (0.7, 0.7, 0.75), a); ctx.fill()
    ctx.restore()

def fries(ctx, cx, cy, rx, ry, S, a=1.0, seed=7):
    rnd = random.Random(seed); items = []
    for i in range(26):
        u, v = rnd.uniform(-1, 1), rnd.uniform(-1, 1)
        if u * u + v * v > 1: continue
        items.append((cy + v * ry, cx + u * rx * 0.85, rnd.uniform(-0.9, 0.9), rnd.uniform(110, 170) * S))
    for (py, px, ang, L) in sorted(items):
        ctx.save(); ctx.translate(px, py - 25 * S); ctx.rotate(ang)
        rrect(ctx, -L / 2, -13 * S, L, 26 * S, 8 * S)
        ctx.set_source(lin(0, -13 * S, 0, 13 * S, [(0, (1.0, 0.88, 0.50), a), (1, (0.85, 0.55, 0.18), a)])); ctx.fill_preserve()
        ctx.set_line_width(2.5 * S); rgba(ctx, (0.55, 0.32, 0.08), 0.8 * a); ctx.stroke()
        ctx.restore()

def basket(ctx, cx, rim_y, rx, h, S, a=1.0, with_fries=True):
    k = 0.2
    ctx.move_to(cx - rx, rim_y); ctx.line_to(cx - rx * 0.88, rim_y + h)
    ctx.save(); ctx.translate(cx, rim_y + h); ctx.scale(1, k); ctx.arc_negative(0, 0, rx * 0.88, math.pi, 0); ctx.restore()
    ctx.line_to(cx + rx, rim_y); ctx.close_path()
    ctx.set_source(lin(cx - rx, 0, cx + rx, 0, [(0, (0.10, 0.10, 0.11), a), (0.35, (0.30, 0.30, 0.33), a), (1, (0.08, 0.08, 0.09), a)])); ctx.fill()
    for j in range(4):
        for i in range(-6, 7):
            circle(ctx, cx + i * rx * 0.13 * (1 - j * 0.03), rim_y + 40 * S + j * h / 4.5, 5 * S, (0.02, 0.02, 0.03), 0.8 * a)
    ctx.save(); ctx.translate(cx, rim_y); ctx.scale(1, k); ctx.arc(0, 0, rx, 0, 2 * math.pi); ctx.restore()
    rgba(ctx, (0.05, 0.05, 0.06), a); ctx.fill()
    if with_fries: fries(ctx, cx, rim_y, rx, rx * k, S, a)
    ctx.save(); ctx.translate(cx, rim_y); ctx.scale(1, k); ctx.arc(0, 0, rx, 0, math.pi); ctx.restore()
    ctx.set_line_width(8 * S); rgba(ctx, (0.45, 0.45, 0.50), a); ctx.stroke()

def shell(ctx, x, y, w, h, S, a=1.0):
    ctx.save(); ctx.translate(x, y + h / 2 + 10 * S); ctx.scale(1, 0.12); circle(ctx, 0, 0, w * 0.62, (0, 0, 0), 0.55 * a); ctx.restore()
    body = lambda c: rrect(c, x - w / 2, y - h / 2, w, h, 100 * S)
    ctx.new_path(); body(ctx)
    ctx.set_source(lin(x - w / 2, 0, x + w / 2, 0, [(0, (0.05, 0.05, 0.06), a), (0.22, (0.24, 0.24, 0.27), a), (0.45, (0.11, 0.11, 0.13), a), (1, (0.04, 0.04, 0.05), a)])); ctx.fill()
    rrect(ctx, x - w / 2 + 40 * S, y - h / 2 + 20 * S, 36 * S, h - 40 * S, 18 * S); rgba(ctx, WHITE, 0.10 * a); ctx.fill()
    ctx.new_path(); body(ctx); ctx.set_line_width(3 * S); rgba(ctx, (0.45, 0.47, 0.55), 0.6 * a); ctx.stroke()

def fryer_cut(ctx, x, y, s, t, a=1.0, grime=0.8, heat=1.0, drops=0.0, smoke_a=0.0, fire=0.0):
    """Cut-away air fryer standing on the counter (y = centre of the body)."""
    S = U * s
    w, h = 640 * S, 760 * S
    shell(ctx, x, y, w, h, S, a)
    # control panel
    rrect(ctx, x - 160 * S, y - h / 2 + 30 * S, 320 * S, 80 * S, 24 * S); rgba(ctx, (0.01, 0.01, 0.02), a); ctx.fill()
    text(ctx, "400°F", x - 40 * S, y - h / 2 + 70 * S, 48 * S, (1.0, 0.45, 0.2), a)
    circle(ctx, x + 100 * S, y - h / 2 + 70 * S, 18 * S, (0.3, 0.8, 1.0), 0.8 * a)
    # cavity (perspective box)
    cx0, cy0, cw, ch = x - w / 2 + 50 * S, y - h / 2 + 140 * S, w - 100 * S, h - 300 * S
    ins = 55 * S
    bx0, by0, bw, bh = cx0 + ins, cy0 + ins * 0.8, cw - 2 * ins, ch - 2 * ins * 0.8
    ctx.rectangle(cx0, cy0, cw, ch); ctx.set_source(lin(0, cy0, 0, cy0 + ch, [(0, (0.32, 0.32, 0.35), a), (1, (0.16, 0.16, 0.18), a)])); ctx.fill()
    ctx.rectangle(bx0, by0, bw, bh); ctx.set_source(lin(0, by0, 0, by0 + bh, [(0, (0.22, 0.22, 0.25), a), (1, (0.10, 0.10, 0.12), a)])); ctx.fill()
    for (p, q, r_, s_) in (((cx0, cy0), (bx0, by0), (bx0, by0 + bh), (cx0, cy0 + ch)), ((cx0 + cw, cy0), (bx0 + bw, by0), (bx0 + bw, by0 + bh), (cx0 + cw, cy0 + ch))):
        ctx.move_to(*p); ctx.line_to(*q); ctx.line_to(*r_); ctx.line_to(*s_); ctx.close_path(); rgba(ctx, (0.40, 0.40, 0.44), 0.5 * a); ctx.fill()
    # ceiling: fan + heating element
    fan(ctx, x, cy0 + 45 * S, 170 * S, 0.22, S, t, a)
    hy = cy0 + 105 * S
    heater(ctx, x, hy, 215 * S, 0.20, S, t, heat, grime, a)
    # basket with fries
    basket(ctx, x, cy0 + ch * 0.55, 230 * S, 190 * S, S, a)
    # grease droplets rising
    if drops > 0:
        rnd = random.Random(5)
        for i in range(26):
            ph = rnd.random(); e = (t * 0.75 + ph) % 1.0
            px = x + rnd.uniform(-200, 200) * S + math.sin(e * 7 + i) * 8 * S
            py = (cy0 + ch * 0.52) - (cy0 + ch * 0.52 - hy) * ease(e)
            ctx.save(); ctx.translate(px, py); ctx.scale(0.7, 1)
            ctx.arc(0, 0, rnd.uniform(6, 11) * S, 0, 2 * math.pi); ctx.restore()
            rgba(ctx, (1.0, 0.80, 0.30), 0.85 * drops * (1 - 0.4 * e) * a); ctx.fill()
    # smoke
    if smoke_a > 0:
        rnd = random.Random(2)
        for i in range(10):
            e = (t * 0.3 + i / 10) % 1.0
            sx = x + rnd.uniform(-220, 220) * S + math.sin(t * 2 + i) * 25 * S; sy = hy - e * 330 * S
            g = cairo.RadialGradient(sx, sy, 0, sx, sy, (60 + 90 * e) * S)
            g.add_color_stop_rgba(0, 0.6, 0.6, 0.62, 0.35 * smoke_a * (1 - e) * a); g.add_color_stop_rgba(1, 0.6, 0.6, 0.62, 0)
            ctx.set_source(g); ctx.paint()
    if fire > 0:
        fx, fy = x + 120 * S, hy + 5 * S
        for k_, (col, sc) in enumerate(((HOTC, 1.0), ((1.0, 0.75, 0.2), 0.6), ((1, 1, 0.85), 0.28))):
            hh = (130 + 25 * math.sin(t * 17 + k_)) * S * sc; ww = 55 * S * sc
            ctx.move_to(fx - ww, fy); ctx.curve_to(fx - ww, fy - hh * 0.5, fx - ww * 0.2, fy - hh * 0.7, fx, fy - hh)
            ctx.curve_to(fx + ww * 0.2, fy - hh * 0.7, fx + ww, fy - hh * 0.5, fx + ww, fy); ctx.close_path()
            rgba(ctx, col, 0.9 * fire * a); ctx.fill()
        glow(ctx, fx, fy - 50 * S, 200 * S, HOTC, 0.5 * fire * a)
    # cut edge highlight + drawer front with handle
    ctx.rectangle(cx0, cy0, cw, ch); ctx.set_line_width(4 * S); rgba(ctx, (0.75, 0.75, 0.80), 0.7 * a); ctx.stroke()
    dy = cy0 + ch + 18 * S
    rrect(ctx, x - w / 2 + 40 * S, dy, w - 80 * S, 120 * S, 30 * S)
    ctx.set_source(lin(0, dy, 0, dy + 120 * S, [(0, (0.20, 0.20, 0.23), a), (1, (0.07, 0.07, 0.08), a)])); ctx.fill()
    rrect(ctx, x - 140 * S, dy + 35 * S, 280 * S, 50 * S, 25 * S)
    ctx.set_source(lin(0, dy + 35 * S, 0, dy + 85 * S, [(0, (0.55, 0.56, 0.62), a), (1, (0.18, 0.18, 0.2), a)])); ctx.fill()
    return hy

def label(ctx, s, x, y, size, col, a):
    if a <= 0: return
    font(ctx, size); e = ctx.text_extents(s)
    rrect(ctx, x - e.width / 2 - 30 * U, y - size * 0.75, e.width + 60 * U, size * 1.5, size * 0.5); rgba(ctx, (0.02, 0.02, 0.04), 0.75 * a); ctx.fill()
    text(ctx, s, x, y, size, col, a)

def sc_hook(ctx, t, d):
    cy = H * 0.50; s = 1.22
    kitchen(ctx, t, cy + 380 * U * s)
    k = prog(t, d * 0.3, d * 0.8)
    hy = fryer_cut(ctx, CX, cy, s, t, 1.0, grime=0.7 + 0.3 * k, heat=0.8, drops=0.3)
    # pointer to the dirty element
    ya = hy - 10 * U + 10 * U * math.sin(t * 6)
    neon_path(ctx, lambda c: (c.move_to(W * 0.95, ya - 150 * U), c.line_to(W * 0.84, ya - 25 * U), c.move_to(W * 0.84, ya - 25 * U), c.line_to(W * 0.88, ya - 60 * U),
                              c.move_to(W * 0.84, ya - 25 * U), c.line_to(W * 0.89, ya - 22 * U)), CORAL, 7 * U, 1.0)

def sc_grease(ctx, t, d):
    cy = H * 0.44; s = 1.18
    kitchen(ctx, t, cy + 380 * U * s)
    g = prog(t, 0.2, d * 0.55)
    fryer_cut(ctx, CX, cy, s, t, 1.0, grime=0.5 + 0.5 * g, heat=1.0, drops=1 - prog(t, d * 0.6, d * 0.75),
              smoke_a=prog(t, d * 0.45, d * 0.65), fire=prog(t, d * 0.78, d * 0.88))
    label(ctx, "GREASE BURNS ON THE HEATING COIL", CX, H * 0.07, 54 * U, GOLD, prog(t, 0, 0.3))
    for i, (lab, col) in enumerate((("SMOKE", WHITE), ("BURNT TASTE", GOLD), ("FIRE RISK", CORAL))):
        kk = prog(t, d * (0.55 + 0.12 * i), d * (0.65 + 0.12 * i))
        label(ctx, lab, W * (0.17 + 0.33 * i), H * 0.685, 44 * U, col, kk)

def towel(ctx, y, a):
    ctx.rectangle(W * 0.03, y, W * 0.94, 150 * U)
    ctx.set_source(lin(0, y, 0, y + 150 * U, [(0, (0.80, 0.84, 0.90), a), (1, (0.55, 0.60, 0.70), a)])); ctx.fill()
    for i in range(6):
        ctx.rectangle(W * 0.03 + (i * 0.17 + 0.04) * W * 0.94, y, 34 * U, 150 * U); rgba(ctx, (0.20, 0.42, 0.85), 0.7 * a); ctx.fill()
    for j in range(3):
        ctx.move_to(W * 0.03, y + 40 * U + j * 40 * U); ctx.curve_to(W * 0.3, y + 30 * U + j * 40 * U, W * 0.7, y + 55 * U + j * 40 * U, W * 0.97, y + 42 * U + j * 40 * U)
    ctx.set_line_width(2 * U); rgba(ctx, (0, 0, 0), 0.12 * a); ctx.stroke()

def brush(ctx, x, y, ang, a):
    ctx.save(); ctx.translate(x, y); ctx.rotate(ang)
    rrect(ctx, -34 * U, -300 * U, 68 * U, 260 * U, 30 * U)
    ctx.set_source(lin(-34 * U, 0, 34 * U, 0, [(0, (0.45, 0.30, 0.75), a), (0.4, (0.70, 0.55, 1.0), a), (1, (0.35, 0.22, 0.60), a)])); ctx.fill()
    rrect(ctx, -95 * U, -55 * U, 190 * U, 60 * U, 16 * U)
    ctx.set_source(lin(0, -55 * U, 0, 5 * U, [(0, (0.9, 0.9, 0.92), a), (1, (0.6, 0.6, 0.65), a)])); ctx.fill()
    for kq in range(16):
        bx = -85 * U + kq * 11.3 * U
        ctx.move_to(bx, 5 * U); ctx.line_to(bx + 3 * U * math.sin(kq), 62 * U)
    ctx.set_line_width(5 * U); rgba(ctx, (0.98, 0.93, 0.75), a); ctx.stroke()
    ctx.restore()

STEPS = [("UNPLUG", CYAN), ("LET IT COOL", CYAN), ("FLIP ONTO A TOWEL", GOLD), ("SOFT BRUSH + SOAPY WATER", GREEN), ("DRY IT", GREEN)]
STEP_T = [0.02, 0.10, 0.20, 0.47, 0.82]
WARN = "CHECK YOUR MANUAL  ·  NO STEEL WOOL"

def sc_clean(ctx, t, d):
    base = H * 0.62
    kitchen(ctx, t, base - 40 * U)
    # checklist (top)
    rrect(ctx, W * 0.04, H * 0.025, W * 0.92, H * 0.255, 30 * U); rgba(ctx, (0.02, 0.02, 0.05), 0.72); ctx.fill()
    for i, (lab, col) in enumerate(STEPS):
        k = prog(t, d * STEP_T[i], d * STEP_T[i] + 0.3)
        y = H * (0.055 + 0.04 * i)
        circle(ctx, W * 0.10, y, 30 * U, col, k)
        text(ctx, str(i + 1), W * 0.10, y, 38 * U, (0.02, 0.03, 0.08), k)
        text(ctx, lab, W * 0.10 + 60 * U, y, 50 * U, WHITE, k, True, "l")
    text(ctx, WARN, W * 0.10 - 30 * U, H * 0.255, 42 * U, CORAL, prog(t, d * 0.25, d * 0.35), True, "l")
    # flipped air fryer on a towel: the opening where the drawer was now shows the element at its bottom
    fa = prog(t, d * 0.18, d * 0.32)
    towel(ctx, base - 30 * U, 1.0)
    S = U * 1.0
    w, h = 820 * S, 600 * S
    x, y = CX, base - h / 2 - 20 * U + (1 - fa) * 40 * U
    shell(ctx, x, y, w, h, S, 1.0)
    # (control panel now at the bottom, upside down)
    rrect(ctx, x - 150 * S, y + h / 2 - 105 * S, 300 * S, 70 * S, 22 * S); rgba(ctx, (0.01, 0.01, 0.02), 1.0); ctx.fill()
    # opening (perspective) with the heating element lying at its bottom
    ox0, oy0, ow, oh = x - w / 2 + 70 * S, y - h / 2 + 45 * S, w - 140 * S, h - 185 * S
    ctx.rectangle(ox0, oy0, ow, oh); ctx.set_source(lin(0, oy0, 0, oy0 + oh, [(0, (0.10, 0.10, 0.12), 1), (1, (0.26, 0.26, 0.29), 1)])); ctx.fill()
    ctx.rectangle(ox0, oy0, ow, oh); ctx.set_line_width(4 * S); rgba(ctx, (0.6, 0.6, 0.66), 0.8); ctx.stroke()
    hx, hy, hr, hk = x, oy0 + oh * 0.60, 290 * S, 0.36
    ctx.save(); ctx.translate(hx, hy); ctx.scale(1, hk); ctx.arc(0, 0, hr * 1.12, 0, 2 * math.pi); ctx.restore()
    rgba(ctx, (0.07, 0.07, 0.08), 1.0); ctx.fill()
    clean_k = prog(t, d * 0.5, d * 0.85)
    tube(ctx, lambda c: spiral(c, hx, hy, hr, hk), 20 * S, (0.66, 0.64, 0.62), 1.0)
    crusts(ctx, hx, hy, hr, hk, 1 - clean_k, S, 1.0)
    if 0.45 * d < t < 0.88 * d:
        bx = hx + 150 * U * math.sin(t * 4.5); by = hy - 20 * U + 25 * U * math.cos(t * 3)
        rnd = random.Random(int(t * 6))
        for i in range(12):
            px, py = bx + rnd.uniform(-170, 170) * U, by + rnd.uniform(-10, 60) * U
            g = cairo.RadialGradient(px - 5 * U, py - 5 * U, 1, px, py, 22 * U)
            g.add_color_stop_rgba(0, 1, 1, 1, 0.8); g.add_color_stop_rgba(1, 0.75, 0.9, 1.0, 0.15)
            ctx.arc(px, py, rnd.uniform(10, 22) * U, 0, 2 * math.pi); ctx.set_source(g); ctx.fill()
        brush(ctx, bx, by - 30 * U, -0.35 + 0.15 * math.sin(t * 9), 1.0)
    if t >= 0.85 * d:
        k = prog(t, 0.85 * d, 0.95 * d)
        glow(ctx, hx, hy, hr * 1.3, GREEN, 0.35 * k)
        label(ctx, "CLEAN!", hx, oy0 + oh * 0.25, 90 * U, GREEN, k)

def sc_outro(ctx, t, d):
    neon_bg(ctx, t, tint=CYAN)
    cta(ctx, t, d, "CHECKED YOURS LATELY?", "SEND THIS TO AN AIR FRYER LOVER")

SHORT_SCENES = ["hook", "grease", "clean", "outro"]
SCENES = dict(hook=sc_hook, grease=sc_grease, clean=sc_clean, outro=sc_outro)

def thumbnail(c):
    vgrad(c, (0.10, 0.04, 0.22), (0.01, 0.02, 0.08))
    thumb_text(c, "LOOK ABOVE", "THE BASKET", "AIR FRYER")
