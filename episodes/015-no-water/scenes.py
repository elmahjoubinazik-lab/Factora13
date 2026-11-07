# Episode 015 - "What happens to your body when you stop drinking water? Hour by hour"
# Executed inside engine/render.py (helpers available). Original vector illustrations, no real person, no face.

WATER = (0.30, 0.68, 1.0)
WATER_D = (0.12, 0.35, 0.75)
CYAN = (0.35, 0.85, 0.98)
GREEN = (0.42, 0.88, 0.58)
SKIN = (0.80, 0.84, 0.95)
URINE = [(0.98, 0.96, 0.75), (0.98, 0.90, 0.50), (0.96, 0.80, 0.30), (0.88, 0.62, 0.18), (0.70, 0.42, 0.10)]

def P(hx, hy, vx, vy):
    return (W * hx, H * hy) if not VERT else (W * vx, H * vy)

def SZ(a, b):
    return (a if not VERT else b) * U

def bg(ctx, t, tint=(0.05, 0.09, 0.20), warm=0.0):
    vgrad(ctx, mix(tint, (0.20, 0.08, 0.06), warm), NAVY); stars(ctx, t, 0.25)
    random.seed(15)
    for i in range(30):
        x0, y0, sp = random.random(), random.random(), random.uniform(0.01, 0.03)
        y = (y0 - t * sp) % 1.0
        r = random.uniform(3, 8) * U
        ctx.save(); ctx.translate(x0 * W, y * H); ctx.scale(r, r * 1.3)
        ctx.move_to(0, -1); ctx.curve_to(0.8, 0, 0.7, 1, 0, 1); ctx.curve_to(-0.7, 1, -0.8, 0, 0, -1); ctx.restore()
        rgba(ctx, mix(WATER, CORAL, warm), 0.12); ctx.fill()

def pill(ctx, label, x, y, size, c=GOLD, a=1.0, fill=NAVY):
    if a <= 0: return
    font(ctx, size); w = ctx.text_extents(label).width + size * 1.4; h = size * 2.0
    rrect(ctx, x - w / 2, y - h / 2, w, h, h / 2); rgba(ctx, fill, 0.9 * a); ctx.fill()
    ctx.set_line_width(3 * U); rgba(ctx, c, a); rrect(ctx, x - w / 2, y - h / 2, w, h, h / 2); ctx.stroke()
    text(ctx, label, x, y, size, c, a)

def bigtext(ctx, s, x, y, size, c, a=1.0):
    if a <= 0: return
    glow(ctx, x, y, size * 1.5, c, 0.22 * a)
    ctx.save(); ctx.translate(x, y); k = 0.7 + 0.3 * a; ctx.scale(k, k)
    text(ctx, s, 4 * U, 6 * U, size, (0, 0, 0), 0.45 * a); text(ctx, s, 0, 0, size, c, a)
    ctx.restore()

def drop(ctx, x, y, r, c=WATER, a=1.0):
    if r <= 0.1 or a <= 0: return
    ctx.save(); ctx.translate(x, y); ctx.scale(r, r)
    ctx.move_to(0, -1.4); ctx.curve_to(0.9, -0.2, 1.0, 1.0, 0, 1.0); ctx.curve_to(-1.0, 1.0, -0.9, -0.2, 0, -1.4); ctx.restore()
    rgba(ctx, c, a); ctx.fill()

def body_path(ctx, x, y, h):
    """Generic standing figure (no face), feet at (x, y), height h."""
    s = h / 10.0
    ctx.new_path()
    ctx.arc(x, y - h + s * 0.9, s * 0.9, 0, 2 * math.pi)                         # head
    ctx.new_sub_path(); rrect(ctx, x - s * 1.6, y - h + s * 2.1, s * 3.2, s * 3.9, s * 0.9)   # torso
    for sg in (-1, 1):
        ctx.new_sub_path(); rrect(ctx, x + sg * s * 1.75 - s * 0.45, y - h + s * 2.2, s * 0.9, s * 3.6, s * 0.45)  # arms
        ctx.new_sub_path(); rrect(ctx, x + sg * s * 0.75 - s * 0.6, y - h + s * 5.6, s * 1.2, s * 4.4, s * 0.55)   # legs

def body(ctx, x, y, h, level, t, a=1.0, col=WATER, glowc=None):
    if a <= 0: return
    glow(ctx, x, y - h * 0.5, h * 0.6, glowc or col, 0.18 * a)
    body_path(ctx, x, y, h)
    g = cairo.LinearGradient(0, y - h, 0, y); g.add_color_stop_rgba(0, 0.25, 0.3, 0.45, 0.9 * a); g.add_color_stop_rgba(1, 0.12, 0.15, 0.28, 0.9 * a)
    ctx.set_source(g); ctx.fill_preserve()
    ctx.save(); ctx.clip()
    wy = y - h * level
    ctx.move_to(x - h, wy)
    for i in range(41):
        xx = x - h * 0.5 + i * h / 40
        ctx.line_to(xx, wy + math.sin(t * 3 + i * 0.5) * h * 0.008)
    ctx.line_to(x + h, wy); ctx.line_to(x + h, y + 10); ctx.line_to(x - h, y + 10); ctx.close_path()
    g = cairo.LinearGradient(0, wy, 0, y); g.add_color_stop_rgba(0, col[0], col[1], col[2], 0.85 * a); g.add_color_stop_rgba(1, WATER_D[0], WATER_D[1], WATER_D[2], 0.9 * a)
    ctx.set_source(g); ctx.fill()
    random.seed(3)
    for i in range(18):
        bx = x + random.uniform(-0.15, 0.15) * h; by = y - ((random.random() + t * 0.12) % 1.0) * h * level
        circle(ctx, bx, by, h * 0.006, WHITE, 0.35 * a)
    ctx.restore()
    body_path(ctx, x, y, h); ctx.set_line_width(3 * U); rgba(ctx, mix(col, WHITE, 0.4), 0.9 * a); ctx.stroke()

def clock(ctx, x, y, r, hours, a=1.0, c=GOLD):
    if a <= 0: return
    glow(ctx, x, y, r * 1.6, c, 0.2 * a)
    circle(ctx, x, y, r, (0.95, 0.94, 0.88), a)
    ctx.new_path(); ctx.arc(x, y, r, 0, 2 * math.pi); ctx.set_line_width(r * 0.08); rgba(ctx, c, a); ctx.stroke()
    for i in range(12):
        an = i / 12 * 2 * math.pi
        ctx.move_to(x + math.cos(an) * r * 0.78, y + math.sin(an) * r * 0.78); ctx.line_to(x + math.cos(an) * r * 0.9, y + math.sin(an) * r * 0.9)
    ctx.set_line_width(r * 0.04); rgba(ctx, NAVY, a); ctx.stroke()
    for ln, k, wd in ((0.5, hours / 12, 0.07), (0.75, hours, 0.045)):
        an = k * 2 * math.pi - math.pi / 2
        ctx.set_line_width(r * wd); ctx.set_line_cap(cairo.LINE_CAP_ROUND); rgba(ctx, NAVY, a)
        ctx.move_to(x, y); ctx.line_to(x + math.cos(an) * r * ln, y + math.sin(an) * r * ln); ctx.stroke()
    circle(ctx, x, y, r * 0.06, c, a)

def stage(ctx, t, label, idx, c=GOLD):
    """Timeline header: HOUR 1 · HOUR 8 · HOUR 24 · DAY 2 · DAY 3."""
    labels = ["HOUR 1", "HOUR 8", "HOUR 24", "DAY 2", "DAY 3"]
    x0, x1 = (W * 0.08, W * 0.92)
    y = H * 0.09 if not VERT else H * 0.06 + 40 * U
    k = prog(t, 0, 0.8)
    ctx.set_line_width(6 * U); rgba(ctx, WHITE, 0.25 * k); ctx.move_to(x0, y); ctx.line_to(x1, y); ctx.stroke()
    xi = x0 + (x1 - x0) * idx / 4
    ctx.set_line_width(6 * U); rgba(ctx, c, k); ctx.move_to(x0, y); ctx.line_to(x0 + (xi - x0) * prog(t, 0.2, 1.2), y); ctx.stroke()
    for i, lb in enumerate(labels):
        x = x0 + (x1 - x0) * i / 4
        on = i <= idx
        circle(ctx, x, y, (16 if i == idx else 10) * U, c if on else (0.4, 0.45, 0.6), k)
        if i == idx: glow(ctx, x, y, 50 * U, c, 0.5 * k)
        text(ctx, lb, x, y + 42 * U, (28 if not VERT else 24) * U, c if i == idx else (0.6, 0.65, 0.8), k)

def kidney(ctx, x, y, s, c=CORAL, a=1.0):
    ctx.save(); ctx.translate(x, y)
    ctx.move_to(0, -s); ctx.curve_to(s * 0.9, -s * 1.1, s * 1.0, s * 1.0, 0, s)
    ctx.curve_to(-s * 0.5, s * 0.9, -s * 0.2, s * 0.2, -s * 0.35, 0); ctx.curve_to(-s * 0.2, -s * 0.2, -s * 0.5, -s * 0.9, 0, -s)
    ctx.restore(); rgba(ctx, c, a); ctx.fill()

def heart(ctx, x, y, s, c=CORAL, a=1.0):
    if s <= 0.5 or a <= 0: return
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.move_to(0, 0.9); ctx.curve_to(-1.4, -0.1, -0.9, -1.2, 0, -0.45); ctx.curve_to(0.9, -1.2, 1.4, -0.1, 0, 0.9)
    ctx.restore(); rgba(ctx, c, a); ctx.fill()

def brain(ctx, x, y, s, c=(1.0, 0.65, 0.75), a=1.0):
    if a <= 0: return
    ctx.save(); ctx.translate(x, y)
    for (dx, dy, r) in [(-0.45, -0.1, 0.55), (0.0, -0.35, 0.55), (0.45, -0.1, 0.55), (-0.25, 0.3, 0.5), (0.3, 0.3, 0.5)]:
        circle(ctx, dx * s, dy * s, r * s, c, a)
    ctx.set_line_width(s * 0.06); rgba(ctx, mix(c, NAVY, 0.4), a)
    ctx.move_to(0, -s * 0.8); ctx.curve_to(s * 0.1, -s * 0.3, -s * 0.1, s * 0.2, 0, s * 0.75); ctx.stroke()
    ctx.restore()

def urine_chart(ctx, x, y, w, k=1.0, mark=-1, a=1.0):
    n = len(URINE); cw = w / n
    for i, c in enumerate(URINE):
        kk = prog(k * n, i, i + 1)
        if kk <= 0: continue
        rrect(ctx, x - w / 2 + i * cw + 4 * U, y - 40 * U, cw - 8 * U, 80 * U, 14 * U); rgba(ctx, c, a * kk); ctx.fill()
    if mark >= 0:
        mx = x - w / 2 + (mark + 0.5) * cw
        ctx.set_line_width(6 * U); rgba(ctx, WHITE, a); rrect(ctx, mx - cw / 2 + 2 * U, y - 46 * U, cw - 4 * U, 92 * U, 16 * U); ctx.stroke()

def glass(ctx, x, y, w, h, level, a=1.0, t=0.0):
    ctx.move_to(x - w / 2, y - h); ctx.line_to(x - w * 0.4, y); ctx.line_to(x + w * 0.4, y); ctx.line_to(x + w / 2, y - h)
    ctx.set_line_width(5 * U); rgba(ctx, (0.85, 0.92, 1.0), a); ctx.stroke()
    ly = y - h * level
    ww = w * (0.4 + 0.1 * level)
    ctx.move_to(x - ww, ly + math.sin(t * 3) * 3 * U); ctx.line_to(x + ww, ly - math.sin(t * 3) * 3 * U); ctx.line_to(x + w * 0.4 - 3 * U, y - 3 * U); ctx.line_to(x - w * 0.4 + 3 * U, y - 3 * U); ctx.close_path()
    rgba(ctx, WATER, 0.7 * a); ctx.fill()

def cross_out(ctx, x, y, s, a=1.0):
    ctx.set_line_width(s * 0.12); ctx.set_line_cap(cairo.LINE_CAP_ROUND); rgba(ctx, CORAL, a)
    ctx.move_to(x - s, y - s); ctx.line_to(x + s, y + s); ctx.stroke(); ctx.move_to(x + s, y - s); ctx.line_to(x - s, y + s); ctx.stroke()

BX, BY = (W * 0.27, H * 0.76) if not VERT else (W * 0.5, H * 0.66)
BH = SZ(680, 760)

# ---------- scenes ----------
def sc_hook(ctx, t, d):
    bg(ctx, t)
    bx = BX if not VERT else W * 0.5
    body(ctx, bx, BY, BH, 0.6 - 0.02 * math.sin(t), t)
    # vapor leaving
    random.seed(2)
    for i in range(16):
        k = (t * 0.25 + i / 16) % 1
        x = bx + random.uniform(-0.25, 0.25) * BH + math.sin(t + i) * 20 * U
        y = BY - BH * (0.3 + 0.7 * random.random()) - k * 160 * U
        drop(ctx, x, y, 9 * U, CYAN, 0.6 * (1 - k))
    if not VERT:
        counter_v = 60 * prog(t, 0.5, 3.0)
        bigtext(ctx, "%d%%" % counter_v, W * 0.66, H * 0.36, 230 * U, CYAN, prog(t, 0.3, 1.0))
        text(ctx, "OF YOUR BODY IS WATER", W * 0.66, H * 0.52, 44 * U, WHITE, prog(t, 1.0, 1.8))
        clock(ctx, W * 0.66, H * 0.72, 90 * U, t * 0.6, prog(t, d * 0.55, d * 0.65))
    else:
        clock(ctx, W * 0.82, H * 0.4, 80 * U, t * 0.6, prog(t, 0.5, 1.2))
        bigtext(ctx, "60%", W * 0.2, H * 0.4, 110 * U, CYAN, prog(t, 0.5, 1.2))
    chip(ctx, "NO WATER · HOUR BY HOUR", t)

def sc_water60(ctx, t, d):
    bg(ctx, t)
    body(ctx, BX, BY, BH, 0.55, t)
    # cells grid on the right
    if not VERT:
        cx0, cy0 = W * 0.52, H * 0.2
        bigtext(ctx, "50–60%", W * 0.7, H * 0.16, 130 * U, CYAN, prog(t, 0.3, 1.0))
        items = [("INSIDE YOUR CELLS", "most of it", CYAN), ("IN YOUR BLOOD", "", CORAL), ("BETWEEN TISSUES", "", GREEN)]
        for i, (lb, sub, c) in enumerate(items):
            k = prog(t, d * (0.3 + 0.08 * i), d * (0.36 + 0.08 * i))
            pill(ctx, lb, W * 0.7, H * (0.34 + 0.1 * i), 38 * U, c, k)
        roles = ["NUTRIENTS", "WASTE", "JOINTS", "TEMPERATURE"]
        for i, r in enumerate(roles):
            k = prog(t, d * (0.6 + 0.07 * i), d * (0.66 + 0.07 * i))
            x = W * (0.52 + 0.12 * i); y = H * 0.7
            circle(ctx, x, y, 62 * U, (0.1, 0.16, 0.32), k); ctx.new_path(); ctx.arc(x, y, 62 * U, 0, 2 * math.pi); ctx.set_line_width(3 * U); rgba(ctx, GOLD, k); ctx.stroke()
            drop(ctx, x, y - 8 * U, 20 * U, WATER, k)
            text(ctx, r, x, y + 92 * U, 26 * U, WHITE, k)
    else:
        bigtext(ctx, "50–60%", CX, H * 0.12, 120 * U, CYAN, prog(t, 0.3, 1.0))
        for i, (lb, c) in enumerate([("CELLS", CYAN), ("BLOOD", CORAL), ("TISSUES", GREEN)]):
            pill(ctx, lb, W * (0.2 + 0.3 * i), H * 0.2, 34 * U, c, prog(t, d * (0.3 + 0.08 * i), d * (0.36 + 0.08 * i)))
    chip(ctx, "YOUR BODY'S WATER", t)

def sc_ages(ctx, t, d):
    bg(ctx, t)
    data = [("BABY", 0.75, 0.55), ("ADULT", 0.60, 1.0), ("OLDER ADULT", 0.52, 0.95)]
    for i, (lb, lv, sc) in enumerate(data):
        k = prog(t, 0.3 + i * 0.8, 1.0 + i * 0.8)
        x = W * (0.2 + 0.18 * i) if not VERT else W * (0.2 + 0.3 * i)
        h = BH * sc * (0.8 if not VERT else 0.62)
        body(ctx, x, BY, h, lv * k, t, k)
        text(ctx, "≈%d%%" % int(lv * 100), x, BY - h - 50 * U, (56 if not VERT else 46) * U, CYAN, k)
        text(ctx, lb, x, BY + 34 * U, (30 if not VERT else 26) * U, WHITE, k)
    if not VERT:
        org = [("BRAIN ≈ 3/4", (1.0, 0.65, 0.75)), ("HEART ≈ 3/4", CORAL), ("BONES ≈ 1/5–1/3", (0.9, 0.9, 0.8))]
        for i, (lb, c) in enumerate(org):
            k = prog(t, d * (0.55 + 0.1 * i), d * (0.6 + 0.1 * i))
            y = H * (0.3 + 0.15 * i)
            if i == 0: brain(ctx, W * 0.72, y, 40 * U, c, k)
            elif i == 1: heart(ctx, W * 0.72, y, 40 * U, c, k)
            else:
                rrect(ctx, W * 0.72 - 50 * U, y - 12 * U, 100 * U, 24 * U, 12 * U); rgba(ctx, c, k); ctx.fill()
                for sg in (-1, 1): circle(ctx, W * 0.72 + sg * 50 * U, y, 22 * U, c, k)
            text(ctx, lb, W * 0.78, y, 40 * U, c, k, True, "l")
    chip(ctx, "WATER CHANGES WITH AGE", t)

def sc_losses(ctx, t, d):
    bg(ctx, t)
    body(ctx, BX, BY, BH, 0.55, t)
    head_y = BY - BH * 0.91
    # breath vapor
    for i in range(6):
        k = (t * 0.5 + i / 6) % 1
        circle(ctx, BX + BH * 0.12 + k * 160 * U, head_y - k * 60 * U, (12 + 18 * k) * U, (0.8, 0.9, 1.0), 0.35 * (1 - k) * prog(t, d * 0.15, d * 0.2))
    # skin
    random.seed(4)
    sk = prog(t, d * 0.3, d * 0.36)
    for i in range(14):
        k = (t * 0.4 + i / 14) % 1
        side = 1 if i % 2 else -1
        x = BX + side * (BH * 0.18 + k * 90 * U); y = BY - BH * random.uniform(0.3, 0.75) - k * 30 * U
        drop(ctx, x, y, 7 * U, CYAN, 0.6 * (1 - k) * sk)
    # kidneys -> urine
    kk = prog(t, d * 0.45, d * 0.52)
    kidney(ctx, BX - BH * 0.06, BY - BH * 0.48, BH * 0.035, CORAL, kk); kidney(ctx, BX + BH * 0.06, BY - BH * 0.48, BH * 0.035, CORAL, kk)
    if not VERT:
        labels = [("BREATH", d * 0.15), ("SKIN", d * 0.3), ("URINE", d * 0.45)]
        for i, (lb, t0) in enumerate(labels):
            pill(ctx, lb, W * 0.48, H * (0.3 + 0.12 * i), 36 * U, CYAN, prog(t, t0, t0 + 0.6))
        v = 2.5 * prog(t, d * 0.6, d * 0.75)
        bigtext(ctx, "%.1f L" % v, W * 0.75, H * 0.36, 170 * U, CYAN, prog(t, d * 0.6, d * 0.66))
        text(ctx, "LOST PER DAY, AT REST", W * 0.75, H * 0.5, 40 * U, WHITE, prog(t, d * 0.62, d * 0.7))
        pill(ctx, "HEAT / EXERCISE: ×2 OR MORE", W * 0.75, H * 0.62, 34 * U, CORAL, prog(t, d * 0.85, d * 0.92))
    else:
        v = 2.5 * prog(t, d * 0.6, d * 0.75)
        bigtext(ctx, "%.1f L / DAY" % v, CX, H * 0.14, 100 * U, CYAN, prog(t, d * 0.6, d * 0.66))
    chip(ctx, "WHERE THE WATER GOES", t)

def sc_sweat(ctx, t, d):
    bg(ctx, t, warm=0.6)
    sun(ctx, W * 0.85 if not VERT else W * 0.82, H * 0.2 if not VERT else H * 0.18, 70 * U, t)
    body(ctx, BX, BY, BH, 0.5, t, 1, WATER, CORAL)
    random.seed(9)
    for i in range(30):
        k = (t * 0.6 + i / 30) % 1
        x = BX + random.uniform(-0.2, 0.2) * BH; y = BY - BH * random.uniform(0.25, 0.85) + k * 120 * U
        drop(ctx, x, y, 8 * U, CYAN, 0.8 * (1 - k))
    # heat waves
    for j in range(3):
        y = BY - BH - 30 * U - j * 26 * U
        ctx.move_to(BX - 80 * U, y)
        for i in range(17): ctx.line_to(BX - 80 * U + i * 10 * U, y + math.sin(t * 5 + i * 0.8 + j) * 6 * U)
        ctx.set_line_width(3 * U); rgba(ctx, CORAL, 0.5); ctx.stroke()
    if not VERT:
        bigtext(ctx, "> 1 L", W * 0.62, H * 0.4, 180 * U, CYAN, prog(t, d * 0.35, d * 0.45))
        text(ctx, "OF SWEAT IN ONE HOUR", W * 0.62, H * 0.55, 42 * U, WHITE, prog(t, d * 0.4, d * 0.5))
        pill(ctx, "SWEAT TAKES SALT TOO", W * 0.62, H * 0.68, 36 * U, GOLD, prog(t, d * 0.85, d * 0.92))
    else:
        bigtext(ctx, "> 1 L / HOUR", CX, H * 0.14, 96 * U, CYAN, prog(t, d * 0.35, d * 0.45))
    chip(ctx, "YOUR AIR CONDITIONER", t)

def sc_hour1(ctx, t, d):
    bg(ctx, t)
    stage(ctx, t, "HOUR 1", 0, CYAN)
    body(ctx, BX, BY, BH * 0.9, 0.58, t)
    bpx, bpy = BX, BY - BH * 0.9 * 0.91
    brain(ctx, bpx, bpy, 30 * U, (1.0, 0.65, 0.75), prog(t, d * 0.1, d * 0.2))
    s = prog(t, d * 0.15, d * 0.25)
    for j in range(3):
        k = (t * 0.8 + j / 3) % 1
        ctx.new_path(); ctx.arc(bpx, bpy, (40 + 120 * k) * U, 0, 2 * math.pi); ctx.set_line_width(3 * U); rgba(ctx, GOLD, 0.6 * (1 - k) * s); ctx.stroke()
    if not VERT:
        bigtext(ctx, "−1 to 2%", W * 0.68, H * 0.3, 120 * U, GOLD, prog(t, d * 0.35, d * 0.42))
        text(ctx, "→ YOU FEEL THIRSTY", W * 0.68, H * 0.42, 44 * U, WHITE, prog(t, d * 0.4, d * 0.48))
        vk = prog(t, d * 0.6, d * 0.68)
        pill(ctx, "VASOPRESSIN → KIDNEYS SAVE WATER", W * 0.68, H * 0.55, 32 * U, CORAL, vk)
        kidney(ctx, W * 0.68, H * 0.65, 34 * U, CORAL, vk)
        urine_chart(ctx, W * 0.68, H * 0.76, 560 * U, prog(t, d * 0.75, d * 0.82), int(1 + 2 * prog(t, d * 0.82, d * 0.95)))
    else:
        bigtext(ctx, "−1 to 2% → THIRST", CX, H * 0.17, 72 * U, GOLD, prog(t, d * 0.35, d * 0.42))
        urine_chart(ctx, CX, H * 0.25, 700 * U, prog(t, d * 0.75, d * 0.82), int(1 + 2 * prog(t, d * 0.82, d * 0.95)))

def sc_hour8(ctx, t, d):
    bg(ctx, t)
    stage(ctx, t, "HOUR 8", 1, GOLD)
    body(ctx, BX, BY, BH * 0.9, 0.55, t)
    if not VERT:
        bigtext(ctx, "−2%", W * 0.68, H * 0.32, 170 * U, GOLD, prog(t, d * 0.3, d * 0.4))
        items = [("DRY MOUTH", CYAN), ("TIRED · IRRITABLE", GOLD), ("FOCUS ↓", CORAL), ("HEADACHE", (1.0, 0.65, 0.75))]
        for i, (lb, c) in enumerate(items):
            k = prog(t, d * (0.15 + 0.15 * i), d * (0.2 + 0.15 * i))
            pill(ctx, lb, W * (0.56 + 0.24 * (i % 2)), H * (0.52 + 0.12 * (i // 2)), 34 * U, c, k)
    else:
        bigtext(ctx, "−2%", W * 0.2, H * 0.2, 90 * U, GOLD, prog(t, d * 0.3, d * 0.4))
        pill(ctx, "FOCUS ↓", W * 0.7, H * 0.2, 36 * U, CORAL, prog(t, d * 0.45, d * 0.55))
    # battery draining
    bx, by = P(0.88, 0.32, 0.8, 0.32)
    bk = prog(t, d * 0.25, d * 0.35)
    if bk:
        rrect(ctx, bx - 40 * U, by - 80 * U, 80 * U, 160 * U, 12 * U); ctx.set_line_width(5 * U); rgba(ctx, WHITE, bk); ctx.stroke()
        lv = 0.8 - 0.5 * prog(t, d * 0.3, d)
        ctx.rectangle(bx - 30 * U, by + 70 * U - 140 * U * lv, 60 * U, 140 * U * lv); rgba(ctx, mix(CORAL, GREEN, lv), bk); ctx.fill()

def ecg(ctx, x0, x1, y, t, speed, c=CORAL, a=1.0, amp=60.0):
    ctx.move_to(x0, y)
    n = 120
    for i in range(n + 1):
        x = x0 + (x1 - x0) * i / n
        ph = ((i / n) * speed * 4 - t * speed) % 1.0
        v = 0
        if 0.40 < ph < 0.44: v = -1.0
        elif 0.44 < ph < 0.48: v = 0.6
        elif 0.30 < ph < 0.36: v = -0.15
        ctx.line_to(x, y + v * amp * U)
    ctx.set_line_width(4 * U); rgba(ctx, c, a); ctx.stroke()

def sc_day1(ctx, t, d):
    bg(ctx, t, warm=0.2)
    stage(ctx, t, "HOUR 24", 2, CORAL)
    body(ctx, BX, BY, BH * 0.9, 0.5, t)
    beat = 1 + 0.12 * max(0, math.sin(t * (6 + 4 * prog(t, 0, d))))
    hx, hy = P(0.68, 0.36, 0.5, 0.22)
    heart(ctx, hx, hy, 70 * U * beat * prog(t, d * 0.2, d * 0.3), CORAL)
    glow(ctx, hx, hy, 160 * U, CORAL, 0.3)
    if not VERT:
        ecg(ctx, W * 0.5, W * 0.92, H * 0.56, t, 1 + 1.5 * prog(t, d * 0.3, d), CORAL, prog(t, d * 0.25, d * 0.35))
        pill(ctx, "BLOOD VOLUME ↓", W * 0.58, H * 0.7, 34 * U, CYAN, prog(t, d * 0.1, d * 0.2))
        pill(ctx, "HEART RATE ↑", W * 0.82, H * 0.7, 34 * U, CORAL, prog(t, d * 0.3, d * 0.4))
        pill(ctx, "LESS SWEAT → HARDER TO COOL", W * 0.7, H * 0.8 - 20 * U, 30 * U, GOLD, prog(t, d * 0.55, d * 0.65))
    else:
        ecg(ctx, W * 0.1, W * 0.9, H * 0.3, t, 1 + 1.5 * prog(t, d * 0.3, d), CORAL, prog(t, d * 0.25, d * 0.35), 40)
    chip(ctx, "", t, 0)

def sc_strange(ctx, t, d):
    bg(ctx, t)
    for i, (lb, lv, al) in enumerate([("YOUNGER", 0.55, 1.0), ("OLDER", 0.45, 0.4)]):
        x = W * (0.2 + 0.2 * i) if not VERT else W * (0.28 + 0.44 * i)
        k = prog(t, 0.3 + i * 0.6, 1.0 + i * 0.6)
        body(ctx, x, BY, BH * 0.8, lv, t, k)
        # thirst meter
        mx, my = x, BY - BH * 0.8 - 90 * U
        rrect(ctx, mx - 90 * U, my - 18 * U, 180 * U, 36 * U, 18 * U); rgba(ctx, (0.15, 0.2, 0.35), k); ctx.fill()
        fl = al * prog(t, d * 0.3, d * 0.5) if i else prog(t, d * 0.2, d * 0.35)
        rrect(ctx, mx - 90 * U, my - 18 * U, max(36 * U, 180 * U * fl), 36 * U, 18 * U); rgba(ctx, GOLD, k); ctx.fill()
        text(ctx, "THIRST", mx, my - 44 * U, 26 * U, GOLD, k)
        text(ctx, lb, x, BY + 34 * U, 30 * U, WHITE, k)
    if not VERT:
        bigtext(ctx, "THIRST IS NOT", W * 0.72, H * 0.32, 72 * U, WHITE, prog(t, 0.5, 1.2))
        bigtext(ctx, "A PERFECT ALARM", W * 0.72, H * 0.42, 72 * U, GOLD, prog(t, 0.8, 1.5))
        pill(ctx, "HEAT WAVES: HIGHER RISK", W * 0.72, H * 0.6, 36 * U, CORAL, prog(t, d * 0.65, d * 0.75))
    else:
        bigtext(ctx, "THIRST WEAKENS", CX, H * 0.14, 70 * U, GOLD, prog(t, 0.5, 1.2))
    chip(ctx, "BUT HERE'S WHERE IT GETS STRANGE", t)

def sc_day2(ctx, t, d):
    bg(ctx, t, warm=0.35)
    stage(ctx, t, "DAY 2", 3, CORAL)
    body(ctx, BX, BY, BH * 0.9, 0.44, t, 1, WATER, CORAL)
    kk = prog(t, d * 0.1, d * 0.2)
    kx, ky = BX, BY - BH * 0.9 * 0.48
    glow(ctx, kx, ky, 120 * U, CORAL, (0.4 + 0.2 * math.sin(t * 5)) * kk)
    kidney(ctx, kx - 30 * U, ky, 30 * U, CORAL, kk); kidney(ctx, kx + 30 * U, ky, 30 * U, CORAL, kk)
    # blood flow arrows toward brain & heart
    fk = prog(t, d * 0.65, d * 0.75)
    for j in range(5):
        k = (t * 0.6 + j / 5) % 1
        y = BY - BH * 0.9 * (0.15 + 0.7 * k)
        circle(ctx, BX, y, 9 * U, CORAL, fk * (1 - k * 0.3))
    if not VERT:
        items = [("VERY LITTLE URINE", GOLD, 0.1), ("CRAMPS · NAUSEA", CORAL, 0.35), ("POUNDING HEADACHE", (1.0, 0.65, 0.75), 0.45), ("BLOOD → BRAIN & HEART", CYAN, 0.68)]
        for i, (lb, c, t0) in enumerate(items):
            pill(ctx, lb, W * 0.68, H * (0.3 + 0.12 * i), 36 * U, c, prog(t, d * t0, d * t0 + 0.6))
    else:
        pill(ctx, "KIDNEYS SAVE EVERY DROP", CX, H * 0.18, 36 * U, GOLD, prog(t, d * 0.1, d * 0.2))

def sc_day3(ctx, t, d):
    bg(ctx, t, warm=0.7)
    stage(ctx, t, "DAY 3", 4, CORAL)
    body(ctx, BX, BY, BH * 0.9, 0.36, t, 1, WATER, CORAL)
    blink = 0.5 + 0.5 * math.sin(t * 6)
    glow(ctx, BX, BY - BH * 0.45, BH * 0.6, CORAL, 0.25 * blink)
    if not VERT:
        x0, x1, y = W * 0.5, W * 0.92, H * 0.5
        ctx.set_line_width(26 * U); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        g = cairo.LinearGradient(x0, 0, x1, 0); g.add_color_stop_rgb(0, *GREEN); g.add_color_stop_rgb(0.45, *GOLD); g.add_color_stop_rgb(1, *CORAL)
        ctx.set_source(g); ctx.move_to(x0, y); ctx.line_to(x1, y); ctx.stroke()
        marks = [(0.1, "−2%"), (0.5, "−10%"), (0.9, "−15–20%")]
        for f, lb in marks:
            x = x0 + (x1 - x0) * f
            text(ctx, lb, x, y - 60 * U, 40 * U, WHITE, prog(t, 0.3, 1.0))
        mk = prog(t, d * 0.2, d * 0.7)
        circle(ctx, x0 + (x1 - x0) * (0.1 + 0.8 * mk), y, 26 * U, WHITE)
        pill(ctx, "CONFUSION · DELIRIUM", W * 0.71, H * 0.64, 36 * U, GOLD, prog(t, d * 0.3, d * 0.4))
        pill(ctx, "KIDNEYS CAN FAIL", W * 0.71, H * 0.74, 36 * U, CORAL, prog(t, d * 0.5, d * 0.6))
        bigtext(ctx, "MEDICAL EMERGENCY", W * 0.71, H * 0.3, 64 * U, CORAL, prog(t, d * 0.8, d * 0.88))
    else:
        bigtext(ctx, "DANGER ZONE", CX, H * 0.18, 90 * U, CORAL, prog(t, 0.5, 1.2))

def sc_rule3(ctx, t, d):
    bg(ctx, t)
    cards = [("3 MIN", "AIR", CYAN), ("3 DAYS", "WATER", WATER), ("3 WEEKS", "FOOD", GOLD)]
    for i, (big, small, c) in enumerate(cards):
        k = prog(t, 0.3 + i * 0.7, 0.9 + i * 0.7)
        if VERT: x, y, w, h = CX, H * (0.18 + 0.15 * i), 760 * U, 230 * U
        else: x, y, w, h = W * (0.2 + 0.3 * i), H * 0.38, 480 * U, 380 * U
        yy = y + (1 - k) * 50 * U + math.sin(t * 1.3 + i) * 6 * U
        rrect(ctx, x - w / 2, yy - h / 2, w, h, 30 * U); rgba(ctx, (0.08, 0.12, 0.26), 0.92 * k); ctx.fill()
        ctx.set_line_width(5 * U if i == 1 else 3 * U); rgba(ctx, c, k); rrect(ctx, x - w / 2, yy - h / 2, w, h, 30 * U); ctx.stroke()
        if i == 1: glow(ctx, x, yy, w * 0.6, c, 0.2 * k)
        text(ctx, big, x, yy - h * 0.1, h * 0.28, c, k)
        text(ctx, "WITHOUT " + small, x, yy + h * 0.25, h * 0.09, WHITE, k)
    if not VERT:
        sk = prog(t, d * 0.55, d * 0.65)
        sun(ctx, W * 0.32, H * 0.72, 46 * U, t, sk)
        text(ctx, "HOT DESERT: MUCH LESS", W * 0.32, H * 0.82 - 10 * U, 34 * U, CORAL, sk)
        ck = prog(t, d * 0.75, d * 0.85)
        circle(ctx, W * 0.68, H * 0.72, 40 * U, (0.6, 0.75, 1.0), ck)
        text(ctx, "COOL & RESTING: LONGER", W * 0.68, H * 0.82 - 10 * U, 34 * U, CYAN, ck)
    chip(ctx, "THE RULE OF THREE · A ROUGH GUIDE", t)

def sc_record(ctx, t, d):
    bg(ctx, t, tint=(0.08, 0.08, 0.14))
    # cell wall with condensation and bars window
    wx, wy = P(0.3, 0.45, 0.5, 0.36)
    ww, wh = SZ(560, 700), SZ(600, 520)
    rrect(ctx, wx - ww / 2, wy - wh / 2, ww, wh, 20 * U); rgba(ctx, (0.3, 0.33, 0.42)); ctx.fill()
    for r in range(8):
        for c in range(6):
            ctx.rectangle(wx - ww / 2 + c * ww / 6 + (r % 2) * ww / 12, wy - wh / 2 + r * wh / 8, ww / 6 - 4 * U, wh / 8 - 4 * U)
    rgba(ctx, (0.36, 0.39, 0.48)); ctx.fill()
    rrect(ctx, wx - 90 * U, wy - wh / 2 + 40 * U, 180 * U, 140 * U, 10 * U); rgba(ctx, (0.55, 0.7, 0.95), 0.6); ctx.fill()
    for i in range(5):
        ctx.rectangle(wx - 80 * U + i * 38 * U, wy - wh / 2 + 40 * U, 10 * U, 140 * U); rgba(ctx, (0.15, 0.17, 0.22)); ctx.fill()
    random.seed(12)
    for i in range(22):
        x = wx + random.uniform(-0.45, 0.45) * ww; y0 = wy + random.uniform(-0.1, 0.4) * wh
        k = (t * 0.15 + random.random()) % 1
        drop(ctx, x, y0 + k * 60 * U, 7 * U, CYAN, 0.8 * (1 - k))
    days = int(18 * prog(t, d * 0.35, d * 0.7))
    if not VERT:
        bigtext(ctx, "%d DAYS" % days, W * 0.72, H * 0.38, 150 * U, GOLD, prog(t, d * 0.35, d * 0.42))
        text(ctx, "(REPORTED)", W * 0.72, H * 0.5, 36 * U, WHITE, prog(t, d * 0.4, d * 0.5))
        pill(ctx, "AN EXTREME EXCEPTION", W * 0.72, H * 0.64, 36 * U, CORAL, prog(t, d * 0.8, d * 0.88))
    else:
        bigtext(ctx, "%d DAYS" % days, CX, H * 0.62, 110 * U, GOLD, prog(t, d * 0.35, d * 0.42))
    chip(ctx, "AUSTRIA · 1979", t)

def camel(ctx, x, y, s, a=1.0, t=0.0):
    c = (0.85, 0.65, 0.38)
    ctx.save(); ctx.translate(x, y)
    for i, lx in enumerate((-0.55, -0.35, 0.35, 0.55)):
        sw = math.sin(t * 3 + i * 1.6) * 0.06
        ctx.save(); ctx.translate(lx * s, -0.9 * s); ctx.rotate(sw)
        rrect(ctx, -0.07 * s, 0, 0.14 * s, 0.9 * s, 0.06 * s); rgba(ctx, mix(c, NAVY, 0.15), a); ctx.fill(); ctx.restore()
    ctx.save(); ctx.translate(0, -1.1 * s); ctx.scale(0.78 * s, 0.27 * s); ctx.arc(0, 0, 1, 0, 2 * math.pi); ctx.restore(); rgba(ctx, c, a); ctx.fill()
    ctx.save(); ctx.translate(-0.08 * s, -1.25 * s); ctx.scale(0.36 * s, 0.38 * s); ctx.arc(0, 0, 1, math.pi, 2 * math.pi); ctx.restore(); rgba(ctx, c, a); ctx.fill()
    ctx.move_to(0.7 * s, -1.25 * s); ctx.curve_to(1.0 * s, -1.4 * s, 0.95 * s, -1.9 * s, 1.1 * s, -2.05 * s); ctx.set_line_width(0.16 * s); rgba(ctx, c, a); ctx.stroke()
    ctx.save(); ctx.translate(1.22 * s, -2.05 * s); ctx.scale(0.2 * s, 0.12 * s); ctx.arc(0, 0, 1, 0, 2 * math.pi); ctx.restore(); rgba(ctx, c, a); ctx.fill()
    ctx.restore()

def sc_camel(ctx, t, d):
    bg(ctx, t, warm=0.3)
    gy = BY
    g = cairo.LinearGradient(0, gy, 0, H); g.add_color_stop_rgb(0, 0.55, 0.42, 0.25); g.add_color_stop_rgb(1, 0.25, 0.18, 0.12)
    ctx.set_source(g); ctx.rectangle(0, gy, W, H - gy); ctx.fill()
    cx = W * 0.32 if not VERT else W * 0.45
    s = SZ(300, 260)
    camel(ctx, cx, gy, s, 1, t)
    hk = prog(t, d * 0.25, d * 0.35)
    if hk:
        hx, hy = cx - 0.05 * s, gy - 1.6 * s
        cross_out(ctx, hx - 40 * U, hy - 120 * U, 30 * U, hk); drop(ctx, hx - 40 * U, hy - 120 * U, 24 * U, WATER, hk * 0.8)
        pill(ctx, "HUMP = FAT, NOT WATER", hx + (60 if not VERT else 0) * U, hy - 200 * U, 34 * U, GOLD, prog(t, d * 0.35, d * 0.42))
    v = 100 * prog(t, d * 0.75, d * 0.92)
    if not VERT:
        bigtext(ctx, "≈ %d L" % v, W * 0.74, H * 0.38, 160 * U, CYAN, prog(t, d * 0.72, d * 0.78))
        text(ctx, "IN A FEW MINUTES", W * 0.74, H * 0.5, 40 * U, WHITE, prog(t, d * 0.78, d * 0.85))
    else:
        bigtext(ctx, "≈ %d L" % v, CX, H * 0.16, 110 * U, CYAN, prog(t, d * 0.72, d * 0.78))
    chip(ctx, "THE CHAMPION OF THIRST", t)

def sc_myth(ctx, t, d):
    bg(ctx, t)
    # 8 glasses
    for i in range(8):
        k = prog(t, 0.2 + i * 0.15, 0.6 + i * 0.15)
        x = (W * (0.1 + 0.055 * i)) if not VERT else (W * (0.08 + 0.12 * i))
        y = H * 0.4 if not VERT else H * 0.2
        glass(ctx, x, y, 70 * U, 110 * U, 0.8 * k, k, t + i)
    mk = prog(t, d * 0.22, d * 0.3)
    if mk:
        mx = W * 0.3 if not VERT else CX
        my = H * 0.33 if not VERT else H * 0.17
        ctx.save(); ctx.translate(mx, my); ctx.rotate(-0.12); sc = 1.5 - 0.5 * mk; ctx.scale(sc, sc)
        ctx.set_line_width(7 * U); rgba(ctx, CORAL, mk); rrect(ctx, -170 * U, -55 * U, 340 * U, 110 * U, 14 * U); ctx.stroke()
        text(ctx, "MYTH?", 0, 0, 70 * U, CORAL, mk); ctx.restore()
    text(ctx, "\"8 GLASSES A DAY\"", W * 0.3 if not VERT else CX, H * 0.55 if not VERT else H * 0.28, 44 * U, WHITE, prog(t, 0.2, 0.8))
    if not VERT:
        items = [("YOUR SIZE", GOLD), ("THE WEATHER", CORAL), ("YOUR ACTIVITY", GREEN)]
        for i, (lb, c) in enumerate(items):
            pill(ctx, lb, W * 0.72, H * (0.22 + 0.1 * i), 34 * U, c, prog(t, d * (0.38 + 0.06 * i), d * (0.42 + 0.06 * i)))
        fk = prog(t, d * 0.6, d * 0.7)
        # watermelon slice, soup bowl, tea cup
        fx, fy = W * 0.62, H * 0.62
        ctx.move_to(fx - 70 * U, fy); ctx.arc_negative(fx, fy, 70 * U, math.pi, 0); ctx.close_path(); rgba(ctx, GREEN, fk); ctx.fill()
        ctx.move_to(fx - 58 * U, fy); ctx.arc_negative(fx, fy, 58 * U, math.pi, 0); ctx.close_path(); rgba(ctx, CORAL, fk); ctx.fill()
        ctx.move_to(fx + 130 * U, fy - 20 * U); ctx.arc(fx + 200 * U, fy - 20 * U, 70 * U, 0, math.pi); ctx.close_path(); rgba(ctx, (0.9, 0.9, 0.95), fk); ctx.fill()
        ctx.rectangle(fx + 135 * U, fy - 32 * U, 130 * U, 14 * U); rgba(ctx, GOLD, fk); ctx.fill()
        tk = prog(t, d * 0.82, d * 0.9)
        rrect(ctx, fx + 330 * U, fy - 60 * U, 90 * U, 90 * U, 14 * U); rgba(ctx, (0.85, 0.6, 0.4), tk); ctx.fill()
        ctx.new_path(); ctx.arc(fx + 430 * U, fy - 15 * U, 24 * U, -math.pi / 2, math.pi / 2); ctx.set_line_width(8 * U); rgba(ctx, (0.85, 0.6, 0.4), tk); ctx.stroke()
        text(ctx, "FOOD, TEA & COFFEE COUNT TOO", W * 0.72, H * 0.74, 34 * U, WHITE, fk)
    chip(ctx, "COMMON MISCONCEPTION", t)

def bottle(ctx, x, y, w, h, level, c=WATER, a=1.0, t=0.0):
    rrect(ctx, x - w / 2, y - h, w, h, w * 0.25); ctx.set_line_width(5 * U); rgba(ctx, (0.85, 0.92, 1.0), a); ctx.stroke()
    rrect(ctx, x - w * 0.18, y - h - w * 0.35, w * 0.36, w * 0.4, 6 * U); rgba(ctx, GOLD, a); ctx.fill()
    ly = y - h * level
    ctx.save(); rrect(ctx, x - w / 2 + 5 * U, y - h + 5 * U, w - 10 * U, h - 10 * U, w * 0.22); ctx.clip()
    ctx.rectangle(x - w / 2, ly + math.sin(t * 3) * 3 * U, w, h); rgba(ctx, c, 0.75 * a); ctx.fill(); ctx.restore()

def sc_howmuch(ctx, t, d):
    bg(ctx, t)
    data = [("WOMEN", 2.0, CORAL), ("MEN", 2.5, CYAN)]
    for i, (lb, v, c) in enumerate(data):
        k = prog(t, 0.3 + i * 0.5, 1.0 + i * 0.5)
        x = W * (0.2 + 0.2 * i) if not VERT else W * (0.3 + 0.4 * i)
        y = H * 0.66 if not VERT else H * 0.42
        bottle(ctx, x, y, SZ(150, 150), SZ(320 * v / 2.5, 260 * v / 2.5), prog(t, 0.6 + i * 0.5, 2.0 + i * 0.5), c, k, t)
        text(ctx, "≈ %.1f L" % v, x, y - SZ(320 * v / 2.5, 260 * v / 2.5) - 100 * U, (70 if not VERT else 56) * U, c, k)
        text(ctx, lb, x, y + 40 * U, 32 * U, WHITE, k)
    if not VERT:
        text(ctx, "TOTAL WATER PER DAY, FOOD INCLUDED · EFSA", W * 0.3, H * 0.76, 28 * U, (0.7, 0.75, 0.9), prog(t, 1.0, 1.6))
        uk = prog(t, d * 0.5, d * 0.6)
        urine_chart(ctx, W * 0.72, H * 0.42, 600 * U, uk, -1)
        if uk:
            pill(ctx, "PALE: WELL HYDRATED", W * 0.62, H * 0.56, 30 * U, GREEN, prog(t, d * 0.65, d * 0.72))
            pill(ctx, "DARK: DRINK", W * 0.84, H * 0.56, 30 * U, CORAL, prog(t, d * 0.75, d * 0.82))
            text(ctx, "THE COLOR CLUE", W * 0.72, H * 0.3, 48 * U, GOLD, uk)
    else:
        urine_chart(ctx, CX, H * 0.14, 760 * U, prog(t, d * 0.5, d * 0.6), -1)
    chip(ctx, "HOW MUCH DO YOU NEED?", t)

def sc_toomuch(ctx, t, d):
    bg(ctx, t)
    gx, gy = P(0.3, 0.75, 0.5, 0.62)
    gw, gh = SZ(260, 240), SZ(380, 340)
    over = prog(t, d * 0.2, d * 0.5)
    glass(ctx, gx, gy, gw, gh, 0.6 + 0.4 * over, 1, t)
    if over > 0.9:
        for i in range(10):
            k = (t * 0.7 + i / 10) % 1
            side = 1 if i % 2 else -1
            drop(ctx, gx + side * (gw * 0.5 + 10 * U), gy - gh + k * gh, 10 * U, WATER, 0.8 * (1 - k))
    # sodium dots diluting
    sk = prog(t, d * 0.4, d * 0.5)
    random.seed(6)
    for i in range(24):
        sp = 1 + 1.6 * prog(t, d * 0.5, d * 0.8)
        x = gx + random.uniform(-0.3, 0.3) * gw * sp * 0.6; y = gy - gh * 0.35 + random.uniform(-0.25, 0.25) * gh * sp * 0.6
        circle(ctx, x, y, 8 * U, (1, 1, 1), 0.85 * sk)
    text(ctx, "Na+", gx, gy - gh * 0.35, 40 * U, GOLD, sk)
    if not VERT:
        bigtext(ctx, "TOO MUCH, TOO FAST", W * 0.7, H * 0.3, 70 * U, CORAL, prog(t, d * 0.1, d * 0.2))
        pill(ctx, "HYPONATREMIA", W * 0.7, H * 0.45, 48 * U, GOLD, prog(t, d * 0.45, d * 0.55))
        text(ctx, "rare · seen in endurance events", W * 0.7, H * 0.56, 34 * U, WHITE, prog(t, d * 0.6, d * 0.7), False)
        pill(ctx, "BALANCE IS THE GOAL", W * 0.7, H * 0.7, 40 * U, GREEN, prog(t, d * 0.85, d * 0.92))
    else:
        bigtext(ctx, "TOO MUCH, TOO FAST", CX, H * 0.15, 72 * U, CORAL, prog(t, d * 0.1, d * 0.2))
    chip(ctx, "THE FINAL TWIST", t)

def sc_recap(ctx, t, d):
    bg(ctx, t)
    steps = [("HOURS", "THIRST · DARK URINE", GOLD, 0.58), ("1 DAY", "HEADACHE · RACING HEART", CORAL, 0.48), ("3 DAYS", "DANGER", (1.0, 0.3, 0.3), 0.34)]
    for i, (big, small, c, lv) in enumerate(steps):
        k = prog(t, d * (0.05 + 0.3 * i), d * (0.12 + 0.3 * i))
        if VERT:
            x, y = W * (0.2 + 0.3 * i), H * 0.6
            body(ctx, x, y, 600 * U, lv, t, k, WATER, c)
            text(ctx, big, x, y - 660 * U, 60 * U, c, k)
            text(ctx, small.split(" · ")[0], x, y + 40 * U, 26 * U, WHITE, k)
        else:
            x, y = W * (0.2 + 0.3 * i), H * 0.72
            body(ctx, x, y, 500 * U, lv, t, k, WATER, c)
            text(ctx, big, x, y - 560 * U, 72 * U, c, k)
            text(ctx, small, x + 210 * U, y - 260 * U, 30 * U, WHITE, k, True, "l") if False else None
            pill(ctx, small, x, y - 650 * U + 0 * U, 30 * U, c, k) if False else None
            text(ctx, small, x, y + 40 * U, 28 * U, WHITE, k)
    chip(ctx, "IN SHORT", t)

def sc_outro(ctx, t, d):
    bg(ctx, t)
    gx, gy = P(0.5, 0.78, 0.5, 0.62)
    glass(ctx, gx, gy, SZ(300, 300), SZ(420, 420), 0.15 + 0.7 * prog(t, 0.2, d * 0.6), 1, t)
    for i in range(6):
        k = (t * 1.2 + i / 6) % 1
        drop(ctx, gx + math.sin(i) * 20 * U, gy - SZ(420, 420) - 200 * U + k * 200 * U, 10 * U, CYAN, 0.8 * (1 - k))
    text(ctx, "HOW MUCH DO YOU DRINK?", CX, H * 0.14 if not VERT else H * 0.12, (70 if not VERT else 60) * U, GOLD, prog(t, 0.2, 0.8))
    sk = prog(t, d * 0.35, d * 0.45)
    if sk:
        pulse = 1 + 0.04 * math.sin(t * 5)
        ctx.save(); ctx.translate(CX, H * 0.26 if not VERT else H * 0.2); ctx.scale(pulse * sk, pulse * sk)
        rrect(ctx, -260 * U, -55 * U, 520 * U, 110 * U, 22 * U); rgba(ctx, CORAL); ctx.fill()
        text(ctx, "SUBSCRIBE", 0, 0, 56 * U, WHITE); ctx.restore()

SHORT_SCENES = ["hook", "recap", "outro"]
SCENES = dict(hook=sc_hook, water60=sc_water60, ages=sc_ages, losses=sc_losses, sweat=sc_sweat, hour1=sc_hour1, hour8=sc_hour8,
              day1=sc_day1, strange=sc_strange, day2=sc_day2, day3=sc_day3, rule3=sc_rule3, record=sc_record, camel=sc_camel,
              myth=sc_myth, howmuch=sc_howmuch, toomuch=sc_toomuch, recap=sc_recap, outro=sc_outro)

def thumbnail(c):
    bg(c, 2.0, warm=0.5)
    glow(c, 1000, 380, 330, CORAL, 0.35)
    body(c, 1000, 680, 600, 0.3, 1.0, 1, WATER, CORAL)
    clock(c, 1170, 170, 80, 3.0, 1, CORAL)
    thumb_text(c, "NO WATER", "HOUR BY HOUR", "DAY 3 = DANGER")
