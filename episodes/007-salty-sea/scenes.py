# Scenes for "Why is the sea salty?"
# Executed inside engine/render.py: helpers (W, H, U, CX, CY, VERT, colors, vgrad, circle, glow, text, rrect,
# stars, sun, chip, prog, ease, mix...) are available.

ROCK = (0.45, 0.42, 0.50)
ROCK_D = (0.30, 0.28, 0.36)
LAND = (0.16, 0.30, 0.24)
SALT = (0.97, 0.97, 1.0)
NA = GOLD                      # sodium ions
CL = (0.45, 0.90, 0.80)        # chloride ions
RAIN = (0.55, 0.80, 1.0)
DEEP = (0.02, 0.07, 0.16)
LAVA = (1.0, 0.45, 0.15)

def ell(ctx, x, y, rx, ry, c, a=1.0, rot=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(max(rx, 0.01), max(ry, 0.01))
    ctx.arc(0, 0, 1, 0, 2 * math.pi); ctx.restore(); rgba(ctx, c, a); ctx.fill()

def line(ctx, pts, c, w, a=1.0):
    ctx.new_path(); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.move_to(*pts[0])
    for p in pts[1:]: ctx.line_to(*p)
    rgba(ctx, c, a); ctx.set_line_width(w); ctx.stroke()

def cloud(ctx, x, y, s, c=(0.85, 0.88, 0.95), a=1.0):
    for dx, dy, r in [(-70, 10, 50), (-20, -25, 65), (45, -10, 55), (85, 15, 40), (10, 20, 50)]:
        circle(ctx, x + dx * s, y + dy * s, r * s, c, a)

def drop(ctx, x, y, s, c=RAIN, a=1.0):
    ctx.new_path(); ctx.move_to(x, y - 16 * s); ctx.curve_to(x + 10 * s, y - 2 * s, x + 9 * s, y + 9 * s, x, y + 9 * s)
    ctx.curve_to(x - 9 * s, y + 9 * s, x - 10 * s, y - 2 * s, x, y - 16 * s); rgba(ctx, c, a); ctx.fill()

def rain(ctx, t, x0, x1, y0, y1, n=30, a=1.0, seed=3):
    random.seed(seed)
    for i in range(n):
        x = x0 + random.random() * (x1 - x0); sp = random.uniform(0.7, 1.0); ph = random.random()
        y = y0 + ((t * 0.9 * sp + ph) % 1) * (y1 - y0)
        line(ctx, [(x, y), (x - 4 * U, y + 26 * U)], RAIN, 4 * U, 0.8 * a)

def ion(ctx, x, y, s, kind, a=1.0):
    c = NA if kind else CL
    glow(ctx, x, y, 26 * s, c, 0.35 * a)
    circle(ctx, x, y, 13 * s, c, a)
    rgba(ctx, NAVY, a); ctx.set_line_width(3 * s)
    ctx.move_to(x - 6 * s, y); ctx.line_to(x + 6 * s, y)
    if kind: ctx.move_to(x, y - 6 * s); ctx.line_to(x, y + 6 * s)
    ctx.stroke()

def crystal(ctx, x, y, s, a=1.0, rot=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot)
    ctx.new_path(); ctx.move_to(-s, -0.5 * s); ctx.line_to(0, -s); ctx.line_to(s, -0.5 * s); ctx.line_to(0, 0); ctx.close_path(); rgba(ctx, WHITE, a); ctx.fill()
    ctx.move_to(-s, -0.5 * s); ctx.line_to(0, 0); ctx.line_to(0, s); ctx.line_to(-s, 0.5 * s); ctx.close_path(); rgba(ctx, (0.80, 0.84, 0.92), a); ctx.fill()
    ctx.move_to(s, -0.5 * s); ctx.line_to(0, 0); ctx.line_to(0, s); ctx.line_to(s, 0.5 * s); ctx.close_path(); rgba(ctx, (0.65, 0.70, 0.82), a); ctx.fill()
    ctx.restore()

def sparkle(ctx, x, y, r, a):
    rgba(ctx, WHITE, a); ctx.new_path()
    ctx.move_to(x, y - r); ctx.line_to(x + r * 0.2, y - r * 0.2); ctx.line_to(x + r, y); ctx.line_to(x + r * 0.2, y + r * 0.2)
    ctx.line_to(x, y + r); ctx.line_to(x - r * 0.2, y + r * 0.2); ctx.line_to(x - r, y); ctx.line_to(x - r * 0.2, y - r * 0.2); ctx.close_path(); ctx.fill()

def sea(ctx, t, y, x0=0, x1=None, top=SEA, bot=SEA_D, amp=8, a=1.0):
    x1 = W if x1 is None else x1
    g = cairo.LinearGradient(0, y, 0, H); g.add_color_stop_rgba(0, *top, a); g.add_color_stop_rgba(1, *bot, a)
    ctx.set_source(g); ctx.new_path(); ctx.move_to(x0, H); ctx.line_to(x0, y)
    for i in range(41):
        xx = x0 + (x1 - x0) * i / 40
        ctx.line_to(xx, y + amp * U * math.sin(i * 0.8 + t * 2.2))
    ctx.line_to(x1, H); ctx.close_path(); ctx.fill()
    for k in range(3):
        yy = y + (30 + 50 * k) * U; xo = ((t * 60 + k * 230) * U) % ((x1 - x0) * 0.6)
        line(ctx, [(x0 + xo + 40 * U, yy), (x0 + xo + 140 * U, yy)], WHITE, 3 * U, 0.15 * a)

def mountains(ctx, x0, x1, yb, hmax, c=ROCK, cap=True):
    pk = [(0.0, 0.3), (0.18, 0.85), (0.38, 0.55), (0.58, 1.0), (0.8, 0.5), (1.0, 0.0)]
    ctx.new_path(); ctx.move_to(x0, yb)
    for fx, fh in pk: ctx.line_to(x0 + (x1 - x0) * fx, yb - hmax * fh)
    ctx.line_to(x1, yb); ctx.close_path(); rgba(ctx, c); ctx.fill()
    if cap:
        for fx, fh in pk[1:-1]:
            if fh > 0.7:
                px, py = x0 + (x1 - x0) * fx, yb - hmax * fh; w = (x1 - x0) * 0.06
                ctx.move_to(px, py); ctx.line_to(px + w, py + w * 1.2); ctx.line_to(px - w, py + w * 1.2); ctx.close_path(); rgba(ctx, SALT, 0.9); ctx.fill()

def path_at(pts, u):
    n = len(pts) - 1; u = clamp(u) * n; i = min(int(u), n - 1); f = u - i
    (a0, b0), (a1, b1) = pts[i], pts[i + 1]
    return a0 + (a1 - a0) * f, b0 + (b1 - b0) * f

def world(ctx, t):
    """Mountains -> river -> sea. Returns river path and sea geometry."""
    if VERT:
        gy, sx, sy = H * 0.40, 0, H * 0.54
        vgrad(ctx, NAVY2, (0.14, 0.2, 0.38), 0, gy)
        rgba(ctx, LAND); ctx.rectangle(0, gy, W, H - gy); ctx.fill()
        mountains(ctx, -40 * U, W * 0.75, gy, 300 * U)
        river = [(W * 0.30, gy), (W * 0.48, gy + 40 * U), (W * 0.36, gy + 90 * U), (W * 0.60, sy + 10 * U)]
        sea(ctx, t, sy)
    else:
        gy, sx, sy = H * 0.56, W * 0.60, H * 0.52
        vgrad(ctx, NAVY2, (0.14, 0.2, 0.38), 0, gy)
        rgba(ctx, LAND); ctx.rectangle(0, gy, W, H - gy); ctx.fill()
        mountains(ctx, -40 * U, W * 0.50, gy, 360 * U)
        river = [(W * 0.28, gy), (W * 0.34, gy + 70 * U), (W * 0.44, gy + 50 * U), (W * 0.50, gy + 110 * U), (sx - 30 * U, gy + 90 * U)]
        sea(ctx, t, sy, sx - 40 * U)
    line(ctx, river, (0.35, 0.65, 0.95), 26 * U)
    line(ctx, river, (0.55, 0.80, 1.0), 10 * U, 0.6)
    return river, sx, sy

# ---------- scenes ----------
def sc_hook(ctx, t, d):
    river, sx, sy = world(ctx, t)
    gy_h = H * 0.56
    stars(ctx, t, 0.3)
    cx_, cy_ = (W * 0.24, H * 0.14) if not VERT else (W * 0.35, H * 0.10)
    cloud(ctx, cx_, cy_, 1.3 * U)
    rain(ctx, t, cx_ - 110 * U, cx_ + 110 * U, cy_ + 50 * U, cy_ + 300 * U, 20)
    a1 = prog(t, 0.5, 1.2); a2 = prog(t, 3.0, 3.8)
    if VERT:
        text(ctx, "FRESH", W * 0.80, H * 0.10, 52 * U, RAIN, a1)
        text(ctx, "SALTY", CX, sy + 90 * U, 64 * U, GOLD, a2)
    else:
        text(ctx, "FRESH", W * 0.40, gy_h + 185 * U, 52 * U, RAIN, a1)
        text(ctx, "SALTY", W * 0.80, sy + 110 * U, 64 * U, GOLD, a2)
    random.seed(8)
    for k in range(14):
        x = (sx + 20 * U) + random.random() * (W - sx - 40 * U); y = sy + 60 * U + random.random() * (H * 0.24)
        if VERT: y = sy + 150 * U + random.random() * 120 * U
        sparkle(ctx, x, y, 12 * U * (0.5 + 0.5 * math.sin(t * 3 + k)), a2)
    q = prog(t, d - 2.8, d - 2.0)
    if q: text(ctx, "?", W * 0.80 if not VERT else W * 0.80, H * 0.25 if not VERT else H * 0.25, 240 * U, GOLD, q)

def sc_title(ctx, t, d):
    vgrad(ctx, NAVY2, NAVY); stars(ctx, t, 0.7)
    yo = -40 * U if not VERT else -140 * U
    a = prog(t, 0, 0.5)
    by = CY + yo - 220 * U
    glow(ctx, CX, by, 160 * U, SALT, 0.25 * a)
    crystal(ctx, CX - 70 * U, by + 30 * U, 55 * U, a, 0.1)
    crystal(ctx, CX + 60 * U, by + 40 * U, 45 * U, a, -0.15)
    crystal(ctx, CX, by - 30 * U, 65 * U, a, 0.0)
    if VERT:
        text(ctx, "WHY IS", CX, CY + yo, 110 * U, WHITE, a)
        text(ctx, "THE SEA", CX, CY + yo + 125 * U, 110 * U, WHITE, a)
        text(ctx, "SALTY?", CX, CY + yo + 250 * U, 110 * U, GOLD, a)
    else:
        text(ctx, "WHY IS THE SEA", CX, CY + yo, 100 * U, WHITE, a)
        text(ctx, "SALTY?", CX, CY + yo + 120 * U, 100 * U, GOLD, a)

def boulder(ctx, x, y, r, erode, t):
    pts = []
    for i in range(14):
        an = i / 14 * 2 * math.pi
        rr = r * (0.85 + 0.15 * math.sin(i * 2.7)) * (1 - 0.18 * erode * (0.5 + 0.5 * math.sin(i * 1.3)))
        pts.append((x + math.cos(an) * rr * 1.35, y + math.sin(an) * rr * 0.8))
    ctx.new_path(); ctx.move_to(*pts[0])
    for p in pts[1:]: ctx.line_to(*p)
    ctx.close_path(); rgba(ctx, ROCK); ctx.fill_preserve(); rgba(ctx, ROCK_D); ctx.set_line_width(6 * U); ctx.stroke()
    for k, (dx, dy) in enumerate([(-0.4, -0.2), (0.3, -0.35), (0.1, 0.2)]):
        if erode > 0.2 + k * 0.2:
            line(ctx, [(x + dx * r, y + dy * r), (x + (dx + 0.15) * r, y + (dy + 0.12) * r), (x + (dx + 0.08) * r, y + (dy + 0.3) * r)], ROCK_D, 5 * U)

def sc_rain(ctx, t, d):
    vgrad(ctx, NAVY2, (0.12, 0.17, 0.33)); stars(ctx, t, 0.3)
    gy = H * 0.70 if not VERT else H * 0.64
    rgba(ctx, LAND); ctx.rectangle(0, gy, W, H - gy); ctx.fill()
    cx_, cy_ = (CX, H * 0.16) if not VERT else (CX, H * 0.20)
    cloud(ctx, cx_, cy_, 1.8 * U)
    rx, ry, rr = (CX, gy - 60 * U, 170 * U)
    if VERT: rx, ry, rr = CX, gy - 60 * U, 160 * U
    # raindrops with CO2 bubbles
    random.seed(12)
    for i in range(16):
        x = cx_ - 200 * U + random.random() * 400 * U; ph = random.random()
        u = (t * 0.5 + ph) % 1; y = cy_ + 80 * U + u * (ry - rr * 0.6 - cy_ - 80 * U)
        drop(ctx, x, y, 1.4 * U)
        co = prog(t, 3.0, 4.0)
        if co and i % 3 == 0:
            circle(ctx, x + 20 * U, y - 10 * U, 7 * U, WHITE, 0.8 * co)
            circle(ctx, x - 18 * U, y + 4 * U, 5 * U, WHITE, 0.8 * co)
    co = prog(t, 3.0, 4.0)
    if VERT:
        text(ctx, "+ CO₂ = SLIGHTLY ACIDIC", CX, H * 0.08 + 30 * U, 42 * U, GOLD, co)
    else:
        text(ctx, "RAIN + CO₂", W * 0.80, H * 0.14, 52 * U, WHITE, co)
        text(ctx, "→ VERY SLIGHTLY ACIDIC", W * 0.80, H * 0.14 + 62 * U, 36 * U, GOLD, co, False)
    er = prog(t, d * 0.55, d * 0.95)
    boulder(ctx, rx, ry, rr, er, t)
    # ions released
    if er > 0:
        random.seed(13)
        for k in range(16):
            st = k / 16 * 0.8
            u = clamp((er - st) / 0.4)
            if u <= 0: continue
            ang = random.uniform(-0.9, 0.9) + (math.pi if k % 2 else 0)
            dist = rr * 1.4 + u * 220 * U
            x = rx + math.cos(ang) * dist; y = ry - 40 * U + math.sin(ang) * dist * 0.4 - u * 60 * U
            ion(ctx, x, y, 1.1 * U, k % 2, u)
        text(ctx, "IONS", rx + (rr * 1.4 + 200 * U if not VERT else 0), ry - (130 * U if not VERT else 260 * U), 48 * U, GOLD, prog(t, d * 0.75, d * 0.85))

def sc_rivers(ctx, t, d):
    river, sx, sy = world(ctx, t)
    stars(ctx, t, 0.3)
    # ions travelling down the river and spreading into the sea
    for k in range(18):
        u = ((t * 0.12 + k / 18) % 1)
        if u < 0.75:
            x, y = path_at(river, u / 0.75)
        else:
            x0, y0 = river[-1]; f = (u - 0.75) / 0.25
            x = x0 + f * (W * 0.25 if not VERT else W * 0.2) * math.cos(k); y = y0 + f * 120 * U * (0.5 + 0.5 * math.sin(k * 1.7))
        ion(ctx, x, y - 4 * U, 0.8 * U, k % 2, prog(t, 0.5, 1.5))
    # glass of river water
    gk = prog(t, d * 0.33, d * 0.43)
    if gk:
        gx, gy2 = (W * 0.20, H * 0.18) if not VERT else (W * 0.80, H * 0.12)
        if VERT: gy2 = H * 0.10
        gw, gh = 110 * U, 150 * U
        ctx.new_path(); ctx.move_to(gx - gw / 2, gy2 - gh / 2); ctx.line_to(gx - gw * 0.4, gy2 + gh / 2); ctx.line_to(gx + gw * 0.4, gy2 + gh / 2); ctx.line_to(gx + gw / 2, gy2 - gh / 2)
        rgba(ctx, WHITE, 0.25 * gk); ctx.fill_preserve(); rgba(ctx, WHITE, 0.8 * gk); ctx.set_line_width(4 * U); ctx.stroke()
        ctx.new_path(); ctx.move_to(gx - gw * 0.46, gy2 - gh * 0.2); ctx.line_to(gx - gw * 0.4, gy2 + gh / 2); ctx.line_to(gx + gw * 0.4, gy2 + gh / 2); ctx.line_to(gx + gw * 0.46, gy2 - gh * 0.2); ctx.close_path()
        rgba(ctx, RAIN, 0.6 * gk); ctx.fill()
        ion(ctx, gx + 10 * U, gy2 + 30 * U, 0.6 * U, 1, gk)
        if VERT:
            text(ctx, "TASTES FRESH", gx, gy2 + gh / 2 + 40 * U, 32 * U, WHITE, gk)
        else:
            text(ctx, "A LITTLE SALT…", gx + gw / 2 + 30 * U, gy2 - 20 * U, 36 * U, WHITE, gk, True, "l")
            text(ctx, "STILL TASTES FRESH", gx + gw / 2 + 30 * U, gy2 + 30 * U, 32 * U, RAIN, gk, False, "l")
    k2 = prog(t, d * 0.70, d * 0.8)
    if VERT: text(ctx, "→ INTO THE OCEAN", CX, sy + 210 * U, 46 * U, GOLD, k2)
    else: text(ctx, "→ INTO THE OCEAN", W * 0.80, sy + 160 * U, 46 * U, GOLD, k2)

def sc_evaporate(ctx, t, d):
    vgrad(ctx, (0.10, 0.16, 0.34), (0.20, 0.28, 0.48)); stars(ctx, t, 0.2)
    sy = H * 0.55 if not VERT else H * 0.48
    sx_, sy_ = (W * 0.13, H * 0.17) if not VERT else (W * 0.2, H * 0.12)
    sun(ctx, sx_, sy_, 70 * U, t, prog(t, 0, 1))
    # water level slightly falls while salt accumulates
    sea(ctx, t, sy)
    p = prog(t, 0, d)
    random.seed(15)
    nsalt = int(12 + 38 * p)
    for k in range(nsalt):
        x = random.random() * W; y = sy + 50 * U + random.random() * (H - sy - 70 * U)
        if VERT and y > H * 0.68 and y < H * 0.8: y -= 150 * U
        crystal(ctx, x, y, 15 * U, 0.9 * clamp((nsalt - k) / 3), random.random() - 0.5)
    # vapor rising
    ev = prog(t, 2.5, 3.5)
    cx_, cy_ = (W * 0.62, H * 0.15) if not VERT else (W * 0.62, H * 0.18)
    random.seed(16)
    for k in range(16):
        x = W * (0.35 + 0.5 * random.random()) if not VERT else W * (0.25 + 0.6 * random.random())
        u = (t * 0.35 + random.random()) % 1
        y = sy - u * (sy - cy_ - 60 * U)
        xx = x + (cx_ - x) * u * 0.6
        circle(ctx, xx, y, (9 - 5 * u) * U, RAIN, ev * (1 - u) * 0.9)
    cloud(ctx, cx_, cy_, (0.8 + 0.6 * ev) * U)
    # rain falls again over far land
    if not VERT:
        mountains(ctx, W * 0.80, W + 60 * U, sy, 220 * U, ROCK, False)
        rain(ctx, t, cx_ + 60 * U, cx_ + 260 * U, cy_ + 60 * U, sy - 60 * U, 12, prog(t, d * 0.55, d * 0.65))
    a1 = prog(t, d * 0.25, d * 0.33)
    if VERT:
        text(ctx, "WATER RISES", W * 0.62, H * 0.33, 44 * U, RAIN, a1)
        rrect(ctx, CX - 210 * U, sy + 70 * U - 40 * U, 420 * U, 80 * U, 40 * U); rgba(ctx, NAVY, 0.7 * a1); ctx.fill()
        text(ctx, "SALT STAYS", CX, sy + 70 * U, 52 * U, GOLD, a1)
    else:
        text(ctx, "WATER EVAPORATES", W * 0.36, H * 0.36, 44 * U, RAIN, a1)
        rrect(ctx, W * 0.30 - 220 * U, sy + 90 * U - 42 * U, 440 * U, 84 * U, 42 * U); rgba(ctx, NAVY, 0.7 * a1); ctx.fill()
        text(ctx, "SALT STAYS", W * 0.30, sy + 90 * U, 54 * U, GOLD, a1)
    k = prog(t, d * 0.7, d * 0.8)
    if k:
        yrs = "OVER HUNDREDS OF MILLIONS OF YEARS"
        if VERT:
            rrect(ctx, CX - 200 * U, sy + 140 * U, 400 * U, 105 * U, 30 * U); rgba(ctx, NAVY, 0.7 * k); ctx.fill()
            text(ctx, "OVER HUNDREDS OF", CX, sy + 170 * U, 36 * U, WHITE, k, False)
            text(ctx, "MILLIONS OF YEARS", CX, sy + 215 * U, 36 * U, WHITE, k, False)
        else:
            font(ctx, 36 * U); tw = ctx.text_extents(yrs).width + 50 * U
            rrect(ctx, W * 0.62 - tw / 2, sy + 180 * U - 30 * U, tw, 60 * U, 30 * U); rgba(ctx, NAVY, 0.7 * k); ctx.fill()
            text(ctx, yrs, W * 0.62, sy + 180 * U, 36 * U, WHITE, k, False)

def chimney(ctx, x, yb, w, h):
    ctx.new_path(); ctx.move_to(x - w, yb); ctx.line_to(x - w * 0.45, yb - h); ctx.line_to(x - w * 0.3, yb - h - 10 * U)
    ctx.line_to(x + w * 0.3, yb - h - 10 * U); ctx.line_to(x + w * 0.45, yb - h); ctx.line_to(x + w, yb); ctx.close_path()
    rgba(ctx, (0.22, 0.18, 0.22)); ctx.fill()
    for k in range(3):
        yy = yb - h * (0.25 + 0.25 * k)
        line(ctx, [(x - w * (0.9 - 0.18 * k) + 6 * U, yy), (x - w * (0.6 - 0.2 * k), yy - 12 * U)], (0.38, 0.30, 0.30), 4 * U)

def sc_vents(ctx, t, d):
    vgrad(ctx, (0.04, 0.16, 0.32), DEEP)
    # light rays from far above, fading
    for i in range(5):
        x = W * (0.1 + 0.2 * i)
        g = cairo.LinearGradient(0, 0, 0, H * 0.4); g.add_color_stop_rgba(0, 0.6, 0.8, 1, 0.08); g.add_color_stop_rgba(1, 0.6, 0.8, 1, 0)
        ctx.set_source(g); ctx.new_path(); ctx.move_to(x - 30 * U, 0); ctx.line_to(x + 30 * U, 0); ctx.line_to(x + 90 * U, H * 0.4); ctx.line_to(x - 40 * U, H * 0.4); ctx.close_path(); ctx.fill()
    fy = H * 0.74 if not VERT else H * 0.66
    # volcano (right)
    vx = W * 0.80 if not VERT else W * 0.75
    vk = prog(t, d * 0.45, d * 0.6)
    glow(ctx, vx, fy - 230 * U, 220 * U, LAVA, 0.35 * vk)
    ctx.new_path(); ctx.move_to(vx - 330 * U, fy); ctx.line_to(vx - 70 * U, fy - 240 * U); ctx.line_to(vx + 70 * U, fy - 240 * U); ctx.line_to(vx + 330 * U, fy); ctx.close_path()
    rgba(ctx, (0.18, 0.14, 0.20)); ctx.fill()
    for sg, ln in ((-1, 0.75), (1, 0.5)):
        pts = [(vx + sg * (40 + 230 * f) * U + 12 * U * math.sin(f * 9), fy - 240 * U + 240 * f * U) for f in [i / 10 * ln for i in range(11)]]
        line(ctx, pts, LAVA, 9 * U, vk)
    ell(ctx, vx, fy - 240 * U, 70 * U, 14 * U, LAVA, vk)
    random.seed(18)
    for k in range(18):
        u = (t * 0.25 + random.random()) % 1
        x = vx + math.sin(k + u * 4) * 60 * U * u; y = fy - 260 * U - u * 280 * U
        circle(ctx, x, y, (10 + 18 * u) * U, (0.35, 0.33, 0.38), 0.6 * (1 - u) * vk)
        if k % 3 == 0: ion(ctx, x + 20 * U, y, 0.6 * U, k % 2, (1 - u) * vk)
    # seafloor
    rgba(ctx, (0.12, 0.10, 0.14)); ctx.new_path(); ctx.move_to(0, H); ctx.line_to(0, fy)
    for i in range(31): ctx.line_to(W * i / 30, fy + 12 * U * math.sin(i * 1.3))
    ctx.line_to(W, H); ctx.close_path(); ctx.fill()
    # black smokers (left)
    ck = prog(t, 0.8, 1.8)
    xs = [W * 0.14, W * 0.27, W * 0.40] if not VERT else [W * 0.16, W * 0.36]
    for i, x in enumerate(xs):
        h = (260 + 80 * (i % 2)) * U
        random.seed(20 + i)
        for k in range(16):
            u = (t * 0.3 + random.random()) % 1
            px = x + math.sin(k * 1.7 + u * 3) * 50 * U * u; py = fy - h - 10 * U - u * 300 * U
            circle(ctx, px, py, (14 + 28 * u) * U, (0.08, 0.07, 0.09), 0.85 * (1 - u) * ck)
            if k % 2 == 0: ion(ctx, px + 25 * U * u, py, 0.6 * U, k % 4 == 0, (1 - u) * ck)
        glow(ctx, x, fy - h, 50 * U, LAVA, 0.4 * ck)
        chimney(ctx, x, fy, 55 * U, h)
    if VERT:
        text(ctx, "HYDROTHERMAL VENTS", CX, H * 0.16, 48 * U, GOLD, ck)
        text(ctx, "+ UNDERWATER VOLCANOES", CX, H * 0.16 + 60 * U, 36 * U, WHITE, vk, False)
    else:
        text(ctx, "HYDROTHERMAL VENTS", W * 0.27, H * 0.10, 48 * U, GOLD, ck)
        text(ctx, "UNDERWATER VOLCANO", vx, H * 0.10, 44 * U, CORAL, vk)

def sc_recipe(ctx, t, d):
    vgrad(ctx, NAVY2, NAVY); stars(ctx, t, 0.3)
    if VERT: px, py, R = CX, H * 0.36, 220 * U
    else: px, py, R = W * 0.30, CY - 40 * U, 250 * U
    segs = [(0.55, CL, "CHLORIDE"), (0.31, NA, "SODIUM"), (0.14, (0.45, 0.48, 0.65), "OTHERS")]
    p = prog(t, 2.0, 5.0)
    a0 = -math.pi / 2; acc = 0
    for f, c, nm in segs:
        a1 = a0 + f * 2 * math.pi * p
        if a1 > a0:
            ctx.new_path(); ctx.move_to(px, py); ctx.arc(px, py, R, a0, a1); ctx.close_path(); rgba(ctx, c); ctx.fill()
        acc += f; a0 = a1
    circle(ctx, px, py, R * 0.55, NAVY)
    text(ctx, "≈ 85%", px, py - 18 * U, 72 * U, WHITE, prog(t, 5, 6))
    text(ctx, "Na⁺ + Cl⁻", px, py + 48 * U, 36 * U, GOLD, prog(t, 5, 6), False)
    # legend
    lgx, lgy = (px + R + 60 * U, py - 90 * U) if not VERT else (CX - 170 * U, py + R + 60 * U)
    for i, (f, c, nm) in enumerate(segs):
        k = prog(t, 3.0 + i * 0.6, 3.6 + i * 0.6)
        yy = lgy + i * 70 * U if not VERT else lgy + i * 56 * U
        circle(ctx, lgx + 20 * U, yy, 18 * U, c, k)
        text(ctx, nm, lgx + 55 * U, yy, 38 * U if not VERT else 34 * U, WHITE, k, True, "l")
    if not VERT:
        text(ctx, "TABLE-SALT INGREDIENTS", px, py - R - 60 * U, 40 * U, GOLD, prog(t, 4.5, 5.5))
    # beaker 1 L with 35 g
    bk = prog(t, d - 6.0, d - 5.0)
    if bk:
        bx, by = (W * 0.75, CY + 20 * U) if not VERT else (CX, H * 0.60)
        if VERT: bx, by = CX + 250 * U, H * 0.20
        bw, bh = (260 * U, 300 * U) if not VERT else (150 * U, 180 * U)
        ctx.new_path(); rrect(ctx, bx - bw / 2, by - bh / 2, bw, bh, 20 * U); rgba(ctx, WHITE, 0.15 * bk); ctx.fill()
        ctx.new_path(); rrect(ctx, bx - bw / 2, by - bh * 0.25, bw, bh * 0.75, 20 * U); rgba(ctx, SEA, 0.8 * bk); ctx.fill()
        ctx.new_path(); rrect(ctx, bx - bw / 2, by - bh / 2, bw, bh, 20 * U); rgba(ctx, WHITE, 0.8 * bk); ctx.set_line_width(5 * U); ctx.stroke()
        text(ctx, "1 L", bx, by + bh * 0.15, 60 * U if not VERT else 44 * U, WHITE, bk)
        # salt pile beside
        hx = bx + bw / 2 + (130 * U if not VERT else 0)
        if not VERT:
            random.seed(22)
            for k in range(14):
                row = k // 5
                crystal(ctx, hx - 60 * U + (k % 5) * 30 * U + row * 15 * U, by + bh / 2 - 20 * U - row * 28 * U, 16 * U, bk, random.random() * 0.4)
            text(ctx, "≈ 35 g", hx, by - bh / 2 + 60 * U, 60 * U, GOLD, bk)
            text(ctx, "OF SALT", hx, by - bh / 2 + 115 * U, 34 * U, WHITE, bk, False)
            text(ctx, "→", bx + bw / 2 + 35 * U, by, 50 * U, WHITE, bk)
        else:
            text(ctx, "≈ 35 g SALT", bx, by + bh / 2 + 45 * U, 38 * U, GOLD, bk)

def building(ctx, x, yb, w, h, a=1.0):
    rgba(ctx, (0.22, 0.27, 0.42), a); ctx.new_path(); ctx.rectangle(x - w / 2, yb - h, w, h); ctx.fill()
    floors = 40; fh = h / floors
    for f in range(floors):
        for c in range(4):
            on = (f * 7 + c * 3) % 5 != 0
            rgba(ctx, GOLD if on else NAVY, (0.85 if on else 0.6) * a)
            ctx.rectangle(x - w / 2 + 12 * U + c * (w - 24 * U) / 4, yb - h + f * fh + fh * 0.25, (w - 24 * U) / 4 - 8 * U, fh * 0.5); ctx.fill()

def sc_amount(ctx, t, d):
    vgrad(ctx, NAVY2, (0.12, 0.17, 0.33)); stars(ctx, t, 0.4)
    gy = H * 0.76 if not VERT else H * 0.66
    top = H * 0.22 if not VERT else H * 0.22
    hgt = gy - top
    rgba(ctx, LAND); ctx.new_path(); ctx.rectangle(0, gy, W, H - gy); ctx.fill()
    bx = W * 0.78 if not VERT else W * 0.78
    bk = prog(t, d * 0.72, d * 0.82)
    p = prog(t, 3.0, d * 0.7)
    # salt layer over land
    lx1 = W * 0.62 if not VERT else W * 0.58
    if p:
        y = gy - hgt * p
        ctx.new_path(); ctx.rectangle(0, y, lx1, gy - y); rgba(ctx, SALT, 0.95); ctx.fill()
        random.seed(25)
        for k in range(int(60 * p)):
            crystal(ctx, random.random() * lx1, y + random.random() * (gy - y), 10 * U, 0.5, random.random())
        for k in range(10):
            xx = lx1 * (k + 0.5) / 10
            crystal(ctx, xx, y - 6 * U, 14 * U, 1, 0.3 * math.sin(k))
        sparkle(ctx, lx1 * 0.3, y + 30 * U, 18 * U * abs(math.sin(t * 3)), 0.9)
        # measure arrow
        mx = lx1 + 50 * U
        line(ctx, [(mx, gy), (mx, y)], GOLD, 5 * U)
        line(ctx, [(mx - 16 * U, y + 20 * U), (mx, y), (mx + 16 * U, y + 20 * U)], GOLD, 5 * U)
        if p > 0.5:
            if VERT:
                text(ctx, "> 150 m", lx1 / 2, y - 60 * U, 64 * U, GOLD, prog(p, 0.5, 0.7))
            else:
                text(ctx, "> 150 m", lx1 / 2, y - 60 * U, 72 * U, GOLD, prog(p, 0.5, 0.7))
    # landmasses label
    text(ctx, "ALL THE OCEAN'S SALT, SPREAD OVER LAND", CX if not VERT else CX, H * 0.08 if not VERT else H * 0.10, 40 * U if not VERT else 30 * U, WHITE, prog(t, 1, 2))
    if bk:
        building(ctx, bx, gy, 160 * U if not VERT else 130 * U, hgt, bk)
        text(ctx, "≈ 40 STORIES", bx, top - 40 * U, 38 * U if not VERT else 32 * U, WHITE, bk)

def scale_pan(ctx, x, y, s, a=1.0):
    line(ctx, [(x, y), (x - 90 * s, y + 120 * s)], WHITE, 3 * s, 0.7 * a)
    line(ctx, [(x, y), (x + 90 * s, y + 120 * s)], WHITE, 3 * s, 0.7 * a)
    ctx.new_path(); ctx.move_to(x - 130 * s, y + 120 * s); ctx.curve_to(x - 100 * s, y + 175 * s, x + 100 * s, y + 175 * s, x + 130 * s, y + 120 * s); ctx.close_path()
    rgba(ctx, GOLD, a); ctx.fill()

def sc_balance(ctx, t, d):
    vgrad(ctx, NAVY2, NAVY); stars(ctx, t, 0.3)
    # seafloor sediments accumulating at bottom
    fy = H * 0.68 if not VERT else H * 0.64
    sea(ctx, t, fy - 40 * U, 0, W, (0.08, 0.20, 0.40), (0.05, 0.12, 0.26), 4, 0.6)
    layers = prog(t, d * 0.3, d * 0.75)
    cols = [(0.55, 0.45, 0.35), (0.65, 0.55, 0.42), (0.48, 0.40, 0.33), (0.70, 0.62, 0.50)]
    for k in range(4):
        th = 26 * U
        yk = fy + (3 - k) * th
        if k / 4 < layers + 0.25:
            rgba(ctx, cols[k], clamp((layers + 0.25 - k / 4) * 4)); ctx.new_path(); ctx.rectangle(0, yk, W, th); ctx.fill()
    rgba(ctx, (0.30, 0.24, 0.20)); ctx.new_path(); ctx.rectangle(0, fy + 4 * th, W, H); ctx.fill()
    # falling salt particles into sediments
    fall = prog(t, d * 0.3, d * 0.4)
    random.seed(27)
    for k in range(20):
        x = random.random() * W; u = (t * 0.3 + random.random()) % 1
        crystal(ctx, x, fy - 260 * U + u * 260 * U, 7 * U, fall * (1 - u * 0.5), u * 3)
    # balance scale
    sx, sy = CX, H * 0.20 if not VERT else H * 0.22
    sw = 380 * U if not VERT else 300 * U
    tilt = 0.18 * math.sin(t * 1.6) * (1 - prog(t, d * 0.55, d * 0.8))
    line(ctx, [(sx, sy), (sx, sy + 300 * U)], WHITE, 10 * U, 0.8)
    ctx.new_path(); ctx.move_to(sx - 70 * U, sy + 310 * U); ctx.line_to(sx + 70 * U, sy + 310 * U); ctx.line_to(sx, sy + 270 * U); ctx.close_path(); rgba(ctx, WHITE, 0.8); ctx.fill()
    lx, ly = sx - sw * math.cos(tilt), sy - sw * math.sin(tilt)
    rx, ry = sx + sw * math.cos(tilt), sy + sw * math.sin(tilt)
    line(ctx, [(lx, ly), (rx, ry)], WHITE, 10 * U)
    circle(ctx, sx, sy, 16 * U, GOLD)
    sp = 0.9 * U if not VERT else 0.75 * U
    scale_pan(ctx, lx, ly, sp); scale_pan(ctx, rx, ry, sp)
    a = prog(t, 0.5, 1.5)
    text(ctx, "IN", lx, ly + 200 * sp, 46 * U, WHITE, a)
    text(ctx, "rivers · vents", lx, ly + 250 * sp, 32 * U, RAIN, a, False)
    b = prog(t, d * 0.3, d * 0.4)
    text(ctx, "OUT", rx, ry + 200 * sp, 46 * U, WHITE, b)
    text(ctx, "sediments", rx, ry + 250 * sp, 32 * U, (0.85, 0.72, 0.55), b, False)
    for k in range(5):
        ion(ctx, lx - 50 * sp + k * 25 * sp, ly + 105 * sp - (k % 2) * 18 * sp, 0.7 * sp, k % 2, a)
    for k in range(4):
        crystal(ctx, rx - 40 * sp + k * 27 * sp, ry + 100 * sp, 14 * sp, b)
    st = prog(t, d * 0.75, d * 0.85)
    if VERT:
        text(ctx, "ROUGHLY STABLE", CX, H * 0.10, 52 * U, GOLD, st)
    else:
        text(ctx, "ROUGHLY STABLE", CX, H * 0.08, 52 * U, GOLD, st)

def swimmer(ctx, x, y, s, t, a=1.0):
    bob = math.sin(t * 2) * 4 * s
    ctx.save(); ctx.translate(x, y + bob)
    rrect(ctx, -50 * s, -12 * s, 80 * s, 24 * s, 12 * s); rgba(ctx, CORAL, a); ctx.fill()
    circle(ctx, 46 * s, 0, 15 * s, (0.95, 0.80, 0.65), a)
    line(ctx, [(-10 * s, -10 * s), (20 * s, -34 * s)], (0.95, 0.80, 0.65), 7 * s, a)
    line(ctx, [(-10 * s, 10 * s), (20 * s, 34 * s)], (0.95, 0.80, 0.65), 7 * s, a)
    line(ctx, [(-50 * s, -6 * s), (-90 * s, -12 * s)], (0.95, 0.80, 0.65), 8 * s, a)
    line(ctx, [(-50 * s, 6 * s), (-90 * s, 12 * s)], (0.95, 0.80, 0.65), 8 * s, a)
    ctx.restore()

def lake(ctx, t, x, y, rx, ry, outlet, salty, a=1.0, labs=True):
    # rivers
    inl = [(x - rx * 0.2, y - ry - 260 * U), (x - rx * 0.05, y - ry - 140 * U), (x - rx * 0.2, y - ry * 0.8)]
    line(ctx, inl, (0.35, 0.65, 0.95), 22 * U, a)
    out = [(x + rx * 0.2, y + ry * 0.8), (x + rx * 0.05, y + ry + 90 * U), (x + rx * 0.25, y + ry + 150 * U)]
    if outlet: line(ctx, out, (0.35, 0.65, 0.95), 22 * U, a)
    if salty:
        ell(ctx, x, y, rx * 1.12, ry * 1.18, SALT, a)
        ell(ctx, x, y, rx, ry, (0.30, 0.62, 0.75), a)
    else:
        ell(ctx, x, y, rx, ry, (0.20, 0.50, 0.90), a)
    # flowing ions
    for k in range(8):
        u = (t * 0.2 + k / 8) % 1
        if u < 0.4:
            px, py = path_at(inl, u / 0.4)
        elif outlet and u > 0.6:
            px, py = path_at(out, (u - 0.6) / 0.4)
        else:
            f = (u - 0.4) / 0.2 if outlet else 1
            px = x + rx * 0.5 * math.sin(k * 2.1) * clamp(f); py = y - ry * 0.6 + ry * 1.0 * clamp(f) * (0.5 + 0.4 * math.cos(k))
        ion(ctx, px, py, 0.6 * U, k % 2, a)
    if salty:
        random.seed(31)
        for k in range(30):
            an = random.random() * 6.28; rr = random.uniform(0.2, 0.9)
            crystal(ctx, x + math.cos(an) * rx * rr, y + math.sin(an) * ry * rr, 7 * U, 0.8 * a, an)

def sc_lakes(ctx, t, d):
    vgrad(ctx, (0.12, 0.20, 0.18), (0.08, 0.14, 0.13))
    p2 = prog(t, d * 0.30, d * 0.40)
    if VERT:
        p = (CX, H * 0.25); q = (CX, H * 0.55); rx, ry = 220 * U, 120 * U
    else:
        p = (W * 0.27, H * 0.47); q = (W * 0.72, H * 0.47); rx, ry = 270 * U, 150 * U
    lake(ctx, t, p[0], p[1], rx, ry, True, False, prog(t, 0.3, 1.0))
    text(ctx, "OUTLET → FRESH", p[0], p[1] - ry - 300 * U if not VERT else p[1] - ry - 50 * U, 40 * U, RAIN, prog(t, 1, 2))
    if p2:
        lake(ctx, t, q[0], q[1], rx, ry, False, True, p2)
        text(ctx, "NO OUTLET → SALTY", q[0], q[1] - ry - 300 * U if not VERT else q[1] - ry - 50 * U, 40 * U, GOLD, p2)
    k = prog(t, d * 0.68, d * 0.78)
    if k:
        swimmer(ctx, q[0] - 20 * U, q[1] + 10 * U, 1.0 * U, t, k)
        text(ctx, "DEAD SEA ≈ 10× SALTIER", q[0], q[1] + ry + 70 * U if not VERT else q[1] + ry + 60 * U, 44 * U, GOLD, k)

def sc_outro(ctx, t, d):
    vgrad(ctx, NAVY2, NAVY); stars(ctx, t, 0.6)
    yo = -80 * U if not VERT else -200 * U
    by = CY + yo - 200 * U
    glow(ctx, CX, by, 120 * U, SALT, 0.2)
    crystal(ctx, CX - 45 * U, by + 15 * U, 38 * U, 1, 0.1); crystal(ctx, CX + 45 * U, by + 20 * U, 32 * U, 1, -0.1); crystal(ctx, CX, by - 20 * U, 45 * U, 1, 0)
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
    if q and k < 1: text(ctx, "Did you expect rain to be the secret?", CX, CY + yo + 260 * U, 44 * U if not VERT else 40 * U, WHITE, q * (1 - k))

SHORT_SCENES = ["hook", "rain", "evaporate", "outro"]

SCENES = dict(hook=sc_hook, title=sc_title, rain=sc_rain, rivers=sc_rivers, evaporate=sc_evaporate, vents=sc_vents,
              recipe=sc_recipe, amount=sc_amount, balance=sc_balance, lakes=sc_lakes, outro=sc_outro)

def thumbnail(c):
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, .08, .11, .26); g.add_color_stop_rgb(1, .02, .03, .08); c.set_source(g); c.paint()
    random.seed(1)
    for _ in range(150):
        c.arc(random.random() * W, random.random() * H, random.uniform(.5, 1.8), 0, 6.3); c.set_source_rgba(1, 1, 1, random.uniform(.3, .9)); c.fill()
    # sea on the right
    sy = 470
    g = cairo.LinearGradient(0, sy, 0, H); g.add_color_stop_rgb(0, *SEA); g.add_color_stop_rgb(1, *SEA_D); c.set_source(g)
    c.new_path(); c.move_to(780, H); c.line_to(780, sy)
    for i in range(31): c.line_to(780 + 500 * i / 30, sy + 10 * math.sin(i * 0.9))
    c.line_to(W, H); c.close_path(); c.fill()
    # big salt pile rising from the sea
    glow(c, 1030, 330, 300, SALT, 0.35)
    random.seed(4)
    for row in range(5):
        n = 6 - row
        for k in range(n):
            crystal(c, 1030 - (n - 1) * 32 + k * 64 + random.uniform(-6, 6), 470 - row * 52, 40, 1, random.uniform(-0.15, 0.15))
    for (x, y, r) in [(880, 260, 22), (1180, 200, 28), (1220, 380, 16)]:
        sparkle(c, x, y, r, 0.95)
    thumb_text(c, "WHY IS THE SEA", "SALTY?", "BLAME THE RAIN")
