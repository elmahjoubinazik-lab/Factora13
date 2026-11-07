# Episode 013 (Short only) - "What really happens when you flush with the lid open?"
# Executed inside engine/render.py (helpers available). Vertical layout (1080x1920).

GREEN = (0.35, 1.0, 0.55)
PORC = (0.93, 0.95, 0.98)
PORC_D = (0.66, 0.72, 0.82)
TILE = (0.10, 0.14, 0.24)
FLOOR_Y = H * 0.66 if VERT else H * 0.8
MPX = 600 * U if VERT else 380 * U          # pixels per meter

def bg(ctx, t):
    vgrad(ctx, (0.05, 0.08, 0.17), NAVY)
    # tiled wall, faint
    ctx.set_line_width(1.5 * U); rgba(ctx, (0.4, 0.5, 0.8), 0.08)
    step = 120 * U
    x = 0
    while x < W: ctx.move_to(x, 0); ctx.line_to(x, FLOOR_Y); x += step
    y = FLOOR_Y
    while y > 0: ctx.move_to(0, y); ctx.line_to(W, y); y -= step
    ctx.stroke()
    g = cairo.LinearGradient(0, FLOOR_Y, 0, H); g.add_color_stop_rgb(0, 0.09, 0.12, 0.22); g.add_color_stop_rgb(1, 0.03, 0.04, 0.09)
    ctx.set_source(g); ctx.rectangle(0, FLOOR_Y, W, H - FLOOR_Y); ctx.fill()
    random.seed(11)
    for i in range(30):
        x0, y0, sp = random.random(), random.random(), random.uniform(0.01, 0.03)
        circle(ctx, x0 * W, ((y0 - t * sp) % 1) * FLOOR_Y, random.uniform(1.5, 3) * U, (0.7, 0.8, 1.0), 0.12)

def toilet(ctx, x, s, lid=0.0, a=1.0):
    """Side view, bowl on the left, tank on the right. x = center of bowl rim. lid: 0 open, 1 closed."""
    yf = FLOOR_Y
    rim_y = yf - 0.42 * MPX
    def fillg(x0, x1, c1, c2):
        g = cairo.LinearGradient(x0, 0, x1, 0)
        g.add_color_stop_rgba(0, c1[0], c1[1], c1[2], a); g.add_color_stop_rgba(1, c2[0], c2[1], c2[2], a); ctx.set_source(g); ctx.fill()
    # shadow
    ctx.save(); ctx.translate(x + 0.12 * MPX, yf); ctx.scale(0.42 * MPX, 0.05 * MPX); ctx.arc(0, 0, 1, 0, 2 * math.pi); ctx.restore(); rgba(ctx, (0, 0, 0), 0.4 * a); ctx.fill()
    # tank
    tx0, tx1 = x + 0.16 * MPX, x + 0.38 * MPX
    rrect(ctx, tx0, yf - 0.82 * MPX, tx1 - tx0, 0.4 * MPX, 10 * U); fillg(tx0, tx1, PORC, PORC_D)
    rrect(ctx, tx0 - 8 * U, yf - 0.85 * MPX, tx1 - tx0 + 16 * U, 0.05 * MPX, 6 * U); fillg(tx0, tx1, PORC, PORC_D)
    ctx.rectangle(tx0 + 14 * U, yf - 0.76 * MPX, 36 * U, 10 * U); rgba(ctx, (0.75, 0.78, 0.85), a); ctx.fill()   # handle
    # bowl body
    ctx.move_to(x - 0.32 * MPX, rim_y)
    ctx.curve_to(x - 0.32 * MPX, rim_y + 0.2 * MPX, x - 0.15 * MPX, rim_y + 0.25 * MPX, x - 0.1 * MPX, rim_y + 0.28 * MPX)
    ctx.line_to(x - 0.12 * MPX, yf); ctx.line_to(x + 0.18 * MPX, yf); ctx.line_to(x + 0.2 * MPX, rim_y); ctx.close_path()
    fillg(x - 0.32 * MPX, x + 0.2 * MPX, PORC, PORC_D)
    ctx.set_line_width(3 * U); rgba(ctx, PORC_D, 0.6 * a)
    ctx.move_to(x - 0.04 * MPX, rim_y + 0.12 * MPX); ctx.curve_to(x + 0.05 * MPX, rim_y + 0.15 * MPX, x + 0.1 * MPX, rim_y + 0.25 * MPX, x + 0.05 * MPX, yf - 0.03 * MPX); ctx.stroke()
    # seat
    rrect(ctx, x - 0.34 * MPX, rim_y - 0.035 * MPX, 0.56 * MPX, 0.035 * MPX, 6 * U); rgba(ctx, (0.98, 0.98, 1.0), a); ctx.fill()
    # lid (hinge at back of seat)
    hx, hy = x + 0.2 * MPX, rim_y - 0.035 * MPX
    th = -1.45 + (-math.pi + 1.45) * lid   # open: pointing up, leaning on the tank; closed: flat over the bowl
    ctx.save(); ctx.translate(hx, hy); ctx.rotate(th)
    rrect(ctx, 0, -0.03 * MPX, 0.55 * MPX, 0.03 * MPX, 6 * U); rgba(ctx, (0.97, 0.97, 1.0), a); ctx.fill()
    ctx.restore()
    return rim_y

def plume(ctx, x, y0, t, t0, hmax, a=1.0, width=1.0, n=420, seed=3, escape=0.0):
    """Green aerosol particles rising from (x, y0) since t0, up to height hmax (px)."""
    if t < t0 or a <= 0: return
    random.seed(seed)
    el = t - t0
    for i in range(n):
        birth = random.uniform(0, 3.0)
        if el < birth: continue
        life = random.uniform(4.0, 9.0)
        age = (el - birth) % life if el - birth > life else el - birth
        k = age / life
        vy = random.uniform(0.6, 1.0)
        hgt = hmax * vy * (1 - math.exp(-age * 0.9)) * (1.0 + 0.1 * math.sin(i))
        side = random.gauss(0, 1) * width
        if escape:
            side = (1 if i % 2 else -1) * (0.25 * MPX + abs(random.gauss(0, 0.2)) * MPX)
        px = x + side * (30 * U + hgt * 0.35) + math.sin(t * 1.3 + i) * 10 * U
        py = y0 - hgt
        r = random.uniform(1.5, 4.5) * U
        al = a * (1 - k) * random.uniform(0.5, 1.0)
        if al <= 0.02: continue
        if r > 3.5 * U: glow(ctx, px, py, r * 4, GREEN, 0.18 * al)
        circle(ctx, px, py, r, GREEN, al)

def laser_sheet(ctx, x, t, a=1.0):
    if a <= 0: return
    g = cairo.LinearGradient(x - 40 * U, 0, x + 40 * U, 0)
    g.add_color_stop_rgba(0, 0.3, 1, 0.5, 0); g.add_color_stop_rgba(0.5, 0.3, 1, 0.5, 0.10 * a); g.add_color_stop_rgba(1, 0.3, 1, 0.5, 0)
    ctx.set_source(g); ctx.rectangle(x - 40 * U, 0, 80 * U, FLOOR_Y); ctx.fill()
    ctx.set_line_width(3 * U); rgba(ctx, GREEN, 0.5 * a * (0.7 + 0.3 * math.sin(t * 6)))
    ctx.move_to(x + 0.3 * MPX, 0); ctx.line_to(x + 0.3 * MPX, FLOOR_Y); ctx.stroke()

def ruler(ctx, x, a=1.0):
    if a <= 0: return
    ctx.set_line_width(3 * U); rgba(ctx, WHITE, 0.6 * a)
    ctx.move_to(x, FLOOR_Y); ctx.line_to(x, FLOOR_Y - 1.65 * MPX); ctx.stroke()
    for i in range(0, 17):
        y = FLOOR_Y - i * 0.1 * MPX
        L = 26 * U if i % 5 == 0 else 12 * U
        ctx.move_to(x, y); ctx.line_to(x + L, y); ctx.stroke()
    for m in (0.5, 1.0, 1.5):
        text(ctx, ("%.1f m" % m), x + 40 * U, FLOOR_Y - m * MPX, 30 * U, WHITE, 0.75 * a, True, "l")

def pill(ctx, label, x, y, size, c=GOLD, a=1.0, fill=NAVY):
    if a <= 0: return
    font(ctx, size); w = ctx.text_extents(label).width + size * 1.4; h = size * 2.0
    rrect(ctx, x - w / 2, y - h / 2, w, h, h / 2); rgba(ctx, fill, 0.9 * a); ctx.fill()
    ctx.set_line_width(3 * U); rgba(ctx, c, a); rrect(ctx, x - w / 2, y - h / 2, w, h, h / 2); ctx.stroke()
    text(ctx, label, x, y, size, c, a)

def bigtext(ctx, s, x, y, size, c, a=1.0):
    if a <= 0: return
    glow(ctx, x, y, size * 1.5, c, 0.22 * a)
    text(ctx, s, x + 4 * U, y + 6 * U, size, (0, 0, 0), 0.45 * a)
    text(ctx, s, x, y, size, c, a)

TX = W * 0.56   # toilet bowl center

def sc_hook(ctx, t, d):
    bg(ctx, t)
    laser_sheet(ctx, TX, t, prog(t, 0.2, 1.0))
    rim = toilet(ctx, TX, 1)
    plume(ctx, TX - 0.06 * MPX, rim, t, 1.2, 1.5 * MPX)
    k = prog(t, 0.8, 1.2)
    # flush pulse on the handle
    if k and t < 2.0: glow(ctx, TX + 0.2 * MPX, FLOOR_Y - 0.76 * MPX, 60 * U, GOLD, 0.6 * (1 - prog(t, 1.4, 2.0)))

def sc_plume(ctx, t, d):
    bg(ctx, t)
    laser_sheet(ctx, TX, t)
    ruler(ctx, W * 0.08, prog(t, 0, 0.8))
    rim = toilet(ctx, TX, 1)
    plume(ctx, TX - 0.06 * MPX, rim, t, 0.2, 1.5 * MPX, seed=4)
    hk = prog(t, 0.5, 8.5)
    hm = 1.5 * hk
    ctx.set_line_width(4 * U); ctx.set_dash([12 * U, 10 * U]); rgba(ctx, GOLD, 0.8)
    yl = rim - (rim - (FLOOR_Y - hm * MPX)) if hm > 0.42 else rim
    ctx.move_to(W * 0.08, FLOOR_Y - hm * MPX); ctx.line_to(W * 0.95, FLOOR_Y - hm * MPX); ctx.stroke(); ctx.set_dash([])
    bigtext(ctx, "%.1f m" % hm, W * 0.4, H * 0.145, 120 * U, GREEN, prog(t, 0.3, 1.0))
    text(ctx, "≈ 5 FT", W * 0.72, H * 0.145, 46 * U, WHITE, prog(t, d * 0.5, d * 0.6), True, "l")
    sec = min(8.0, max(0.0, (t - 0.5)))
    pill(ctx, "%d s" % int(sec), W * 0.84, H * 0.075 + 40 * U, 40 * U, GOLD, prog(t, 0.5, 1.2))
    chip(ctx, "UNIV. OF COLORADO · 2022", t)

def sink(ctx, x, y, s, a=1.0, dots=0.0, t=0.0):
    if a <= 0: return
    # pedestal
    ctx.rectangle(x - s * 0.12, y, s * 0.24, FLOOR_Y - y); rgba(ctx, PORC_D, a); ctx.fill()
    ctx.move_to(x - s * 0.6, y - s * 0.1); ctx.line_to(x + s * 0.6, y - s * 0.1); ctx.curve_to(x + s * 0.5, y + s * 0.15, x - s * 0.5, y + s * 0.15, x - s * 0.6, y - s * 0.1)
    rgba(ctx, PORC, a); ctx.fill()
    ctx.rectangle(x + s * 0.3, y - s * 0.35, s * 0.06, s * 0.25); rgba(ctx, (0.75, 0.78, 0.85), a); ctx.fill()
    # cup with toothbrush
    cx = x - s * 0.35
    rrect(ctx, cx - s * 0.1, y - s * 0.38, s * 0.2, s * 0.28, 6 * U); rgba(ctx, (0.4, 0.7, 0.95), a); ctx.fill()
    ctx.save(); ctx.translate(cx, y - s * 0.38); ctx.rotate(-0.2)
    ctx.rectangle(-s * 0.02, -s * 0.38, s * 0.04, s * 0.4); rgba(ctx, CORAL, a); ctx.fill()
    ctx.rectangle(-s * 0.035, -s * 0.42, s * 0.07, s * 0.08); rgba(ctx, WHITE, a); ctx.fill()
    ctx.restore()
    if dots:
        random.seed(8)
        for i in range(26):
            px = x + random.uniform(-0.6, 0.6) * s; py = y - random.uniform(-0.05, 0.8) * s
            k = clamp(dots * 26 - i)
            if k <= 0: continue
            rr = (7 + 2 * math.sin(t * 4 + i)) * U
            circle(ctx, px, py, rr, GREEN, 0.8 * k)
            for j in range(6):
                an = j / 6 * 2 * math.pi
                circle(ctx, px + math.cos(an) * rr * 1.5, py + math.sin(an) * rr * 1.5, rr * 0.3, GREEN, 0.8 * k)

def sc_lid(ctx, t, d):
    bg(ctx, t)
    lid = prog(t, 0.8, 2.0)
    rim = toilet(ctx, TX, 1, lid)
    plume(ctx, TX - 0.06 * MPX, rim - 0.05 * MPX, t, 1.6, 0.5 * MPX, 0.8 * (1 - prog(t, d * 0.45, d * 0.55)), seed=5, n=200, escape=1.0)
    text(ctx, "CLOSE THE LID?", W * 0.5, H * 0.12, 72 * U, WHITE, prog(t, 0.2, 0.8) * (1 - prog(t, d * 0.4, d * 0.48)))
    pill(ctx, "IT HELPS ✓", W * 0.5, H * 0.21, 44 * U, MAJ if False else (0.42, 0.88, 0.58), prog(t, 2.2, 2.8) * (1 - prog(t, d * 0.4, d * 0.48)))
    s2 = prog(t, d * 0.45, d * 0.55)
    if s2:
        sink(ctx, W * 0.22, FLOOR_Y - 0.55 * MPX, 260 * U, s2, prog(t, d * 0.55, d * 0.85), t)
        text(ctx, "VIRUSES ON SURFACES?", W * 0.5, H * 0.15, 60 * U, WHITE, s2)
        pill(ctx, "NO CLEAR DIFFERENCE", W * 0.5, H * 0.22, 46 * U, CORAL, prog(t, d * 0.7, d * 0.8))
    chip(ctx, "UNIV. OF ARIZONA · 2024", t, prog(t, d * 0.45, d * 0.55))

def icon_card(ctx, i, label, t, k, draw):
    if k <= 0: return
    w, h = W * 0.86, 210 * U
    x = CX + (1 - k) * 200 * U; y = H * 0.17 + i * (h + 30 * U)
    rrect(ctx, x - w / 2, y, w, h, 30 * U); rgba(ctx, (0.08, 0.12, 0.26), 0.92 * k); ctx.fill()
    ctx.set_line_width(4 * U); rgba(ctx, (0.42, 0.88, 0.58), k); rrect(ctx, x - w / 2, y, w, h, 30 * U); ctx.stroke()
    draw(ctx, x - w / 2 + 120 * U, y + h / 2, k)
    font(ctx, 40 * U)
    lines = label.split("\n")
    for j, ln in enumerate(lines):
        text(ctx, ln, x - w / 2 + 230 * U, y + h / 2 + (j - (len(lines) - 1) / 2) * 52 * U, 40 * U, WHITE, k, True, "l")

def ic_spray(ctx, x, y, k):
    rrect(ctx, x - 35 * U, y - 30 * U, 70 * U, 100 * U, 14 * U); rgba(ctx, (0.3, 0.75, 0.95), k); ctx.fill()
    ctx.rectangle(x - 20 * U, y - 70 * U, 50 * U, 40 * U); rgba(ctx, WHITE, k); ctx.fill()
    for j in range(5): circle(ctx, x + 55 * U + j * 8 * U, y - 60 * U + (j - 2) * 9 * U, 5 * U, (0.6, 0.9, 1.0), k)

def ic_brush(ctx, x, y, k):
    rrect(ctx, x - 40 * U, y - 20 * U, 80 * U, 90 * U, 12 * U); rgba(ctx, (0.4, 0.7, 0.95), k); ctx.fill()
    ctx.save(); ctx.translate(x, y - 20 * U); ctx.rotate(-0.15)
    ctx.rectangle(-6 * U, -80 * U, 12 * U, 90 * U); rgba(ctx, CORAL, k); ctx.fill()
    rrect(ctx, -22 * U, -100 * U, 44 * U, 36 * U, 10 * U); rgba(ctx, GOLD, k); ctx.fill()   # cap
    ctx.restore()

def ic_air(ctx, x, y, k, t=0.0):
    rrect(ctx, x - 60 * U, y - 60 * U, 120 * U, 120 * U, 10 * U); rgba(ctx, (0.55, 0.75, 1.0), 0.3 * k); ctx.fill()
    ctx.set_line_width(6 * U); rgba(ctx, WHITE, k); rrect(ctx, x - 60 * U, y - 60 * U, 120 * U, 120 * U, 10 * U); ctx.stroke()
    ctx.move_to(x, y - 60 * U); ctx.line_to(x, y + 60 * U); ctx.stroke()
    for j in range(3):
        ctx.move_to(x + 70 * U, y - 30 * U + j * 30 * U); ctx.curve_to(x + 100 * U, y - 45 * U + j * 30 * U, x + 120 * U, y - 15 * U + j * 30 * U, x + 150 * U, y - 30 * U + j * 30 * U)
    ctx.stroke()

def sc_tips(ctx, t, d):
    bg(ctx, t)
    text(ctx, "WHAT TO DO", CX, H * 0.1, 76 * U, (0.42, 0.88, 0.58), prog(t, 0, 0.5))
    icon_card(ctx, 0, "Clean the bowl\nand the handle", t, prog(t, 0.2, 0.8), ic_spray)
    icon_card(ctx, 1, "Toothbrush: covered,\nfar from the toilet", t, prog(t, d * 0.3, d * 0.3 + 0.6), ic_brush)
    icon_card(ctx, 2, "Air out the room", t, prog(t, d * 0.65, d * 0.65 + 0.6), lambda c, x, y, k: ic_air(c, x, y, k, t))

def sc_sub(ctx, t, d):
    bg(ctx, t)
    rim = toilet(ctx, TX, 1, 1.0)
    q = prog(t, 0.2, 0.8)
    bigtext(ctx, "LID DOWN?", CX, H * 0.12, 110 * U, GOLD, q)
    sk = prog(t, d * 0.4, d * 0.5)
    if sk:
        bx, by = CX, H * 0.23
        pulse = 1 + 0.04 * math.sin(t * 5)
        ctx.save(); ctx.translate(bx, by); ctx.scale(pulse * sk, pulse * sk)
        rrect(ctx, -260 * U, -55 * U, 520 * U, 110 * U, 22 * U); rgba(ctx, CORAL); ctx.fill()
        text(ctx, "SUBSCRIBE", 0, 0, 56 * U, WHITE)
        ctx.restore()

SHORT_SCENES = ["hook", "plume", "lid", "tips", "sub"]
SCENES = dict(hook=sc_hook, plume=sc_plume, lid=sc_lid, tips=sc_tips, sub=sc_sub)

def thumbnail(c):
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, .08, .11, .26); g.add_color_stop_rgb(1, .02, .03, .08); c.set_source(g); c.paint()
    thumb_text(c, "LID OPEN?", "THINK AGAIN", "SCIENCE")
