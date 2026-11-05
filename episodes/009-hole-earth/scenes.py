# Scenes for "What if you dug a hole through the Earth?"
# Executed inside engine/render.py: helpers (W, H, U, CX, CY, VERT, colors, vgrad, circle, glow, text, rrect,
# stars, earth, sun, chip, prog, ease, mix...) are available.

CRUST = (0.42, 0.33, 0.24)
MANTLE_O = (0.62, 0.22, 0.12)
MANTLE_I = (0.92, 0.42, 0.14)
OCORE = (1.0, 0.66, 0.22)
ICORE = (1.0, 0.93, 0.62)
CYAN = (0.35, 0.85, 1.0)

AY = H * 0.42 if VERT else H * 0.45   # art centre, above the captions


def bg(ctx, t, a=0.5):
    vgrad(ctx, NAVY2, NAVY); stars(ctx, t, a)


def section(ctx, x, y, R, t=0, a=1.0, tunnel=True, glow_core=True):
    """Earth sliced in half: crust, mantle, liquid outer core, solid inner core (radii to scale, crust exaggerated)."""
    glow(ctx, x, y, R * 1.3, (0.4, 0.7, 1.0), 0.25 * a)
    circle(ctx, x, y, R, SEA, a)
    circle(ctx, x, y, R * 0.975, CRUST, a)
    g = cairo.RadialGradient(x, y, R * 0.3, x, y, R * 0.96)
    g.add_color_stop_rgba(0, *MANTLE_I, a); g.add_color_stop_rgba(1, *MANTLE_O, a)
    ctx.set_source(g); ctx.arc(x, y, R * 0.955, 0, 2 * math.pi); ctx.fill()
    if glow_core: glow(ctx, x, y, R * 0.75, OCORE, 0.35 * a * (0.85 + 0.15 * math.sin(t * 2)))
    circle(ctx, x, y, R * 0.546, OCORE, a)          # 3,480 / 6,371
    for i in range(3):   # swirls in the liquid outer core
        ctx.arc(x, y, R * (0.3 + 0.08 * i), t * (0.4 + 0.1 * i) + i * 2, t * (0.4 + 0.1 * i) + i * 2 + 1.6)
        rgba(ctx, (1, 0.8, 0.4), 0.5 * a); ctx.set_line_width(3 * U); ctx.stroke()
    circle(ctx, x, y, R * 0.19, ICORE, a)          # 1,220 / 6,371
    if tunnel:
        tw = max(10 * U, R * 0.05)
        ctx.rectangle(x - tw / 2, y - R - 4 * U, tw, 2 * R + 8 * U); rgba(ctx, (0.03, 0.03, 0.06), 0.92 * a); ctx.fill()
        ctx.set_line_width(2 * U); rgba(ctx, GOLD, 0.6 * a)
        ctx.move_to(x - tw / 2, y - R); ctx.line_to(x - tw / 2, y + R); ctx.move_to(x + tw / 2, y - R); ctx.line_to(x + tw / 2, y + R); ctx.stroke()


def person(ctx, x, y, s, ang=0.0, c=WHITE, a=1.0, arms=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(ang)
    circle(ctx, 0, -38 * s, 11 * s, c, a)
    ctx.set_line_width(7 * s); ctx.set_line_cap(cairo.LINE_CAP_ROUND); rgba(ctx, c, a)
    ctx.move_to(0, -26 * s); ctx.line_to(0, 6 * s)
    ctx.move_to(0, 6 * s); ctx.line_to(-12 * s, 34 * s); ctx.move_to(0, 6 * s); ctx.line_to(12 * s, 34 * s)
    ctx.move_to(0, -18 * s); ctx.line_to(-22 * s, -18 * s - 20 * s * arms); ctx.move_to(0, -18 * s); ctx.line_to(22 * s, -18 * s - 20 * s * arms)
    ctx.stroke(); ctx.restore()


def shovel(ctx, x, y, s, a=1.0):
    ctx.set_line_width(6 * s); ctx.set_line_cap(cairo.LINE_CAP_ROUND); rgba(ctx, (0.75, 0.6, 0.4), a)
    ctx.move_to(x, y); ctx.line_to(x + 30 * s, y - 70 * s); ctx.stroke()
    ctx.move_to(x - 12 * s, y + 4 * s); ctx.line_to(x + 8 * s, y - 8 * s); ctx.line_to(x + 2 * s, y + 24 * s); ctx.close_path()
    rgba(ctx, (0.75, 0.78, 0.85), a); ctx.fill()


def label(ctx, s, x, y, size, c=WHITE, a=1.0, align="c", bgc=True):
    if bgc and a > 0:
        font(ctx, size); w = ctx.text_extents(s).width + size
        x0 = {"c": x - w / 2, "l": x - size / 2, "r": x - w + size / 2}[align]
        rrect(ctx, x0, y - size * 0.75, w, size * 1.5, size * 0.4); rgba(ctx, NAVY, 0.75 * a); ctx.fill()
    text(ctx, s, x, y, size, c, a, True, align)


def leader(ctx, p, q, a, c=WHITE):
    rgba(ctx, c, 0.8 * a); ctx.set_line_width(3 * U); ctx.move_to(*p); ctx.line_to(*q); ctx.stroke()
    circle(ctx, p[0], p[1], 7 * U, c, a)


# ---------------------------------------------------------------- scenes
def sc_hook(ctx, t, d):
    bg(ctx, t, 0.6)
    R = (330 if VERT else 300) * U
    ex, ey = (CX, AY + 60 * U) if VERT else (CX, AY + 60 * U)
    dig = prog(t, 0.6, 3.0)
    section(ctx, ex, ey, R, t, 1, False, True)
    # tunnel being dug, then dashed route through
    if dig:
        tw = R * 0.05
        ctx.rectangle(ex - tw / 2, ey - R - 4 * U, tw, (2 * R + 8 * U) * dig); rgba(ctx, (0.03, 0.03, 0.06), 0.92); ctx.fill()
    jump = prog(t, 3.6, 4.4)
    py = ey - R - 40 * U - 60 * U * math.sin(jump * math.pi) + max(0.0, t - 4.4) * 70 * U
    py = min(py, ey - R * 0.4)
    person(ctx, ex, py, 1.3 * U, 0 if jump < 0.5 else math.pi * 0.0, WHITE, 1, jump)
    if t < 4: shovel(ctx, ex + 60 * U, ey - R - 6 * U, 1.3 * U, 1 - prog(t, 3.2, 3.8))
    q = prog(t, d - 2.8, d - 2.0)
    if q: text(ctx, "?", ex + R * (1.25 if not VERT else 0.7), ey - R * (0.3 if not VERT else 0.95), 170 * U, GOLD, q)


def sc_title(ctx, t, d):
    bg(ctx, t, 0.5)
    R = 230 * U
    ex, ey = (CX, H * 0.25) if VERT else (W * 0.78, AY)
    section(ctx, ex, ey, R, t)
    # falling dot in tunnel
    k = (t * 0.3) % 1
    circle(ctx, ex, ey - R * math.cos(k * math.pi), 9 * U, WHITE)
    glow(ctx, ex, ey - R * math.cos(k * math.pi), 30 * U, WHITE, 0.6)
    a = prog(t, 0, 0.5)
    if VERT:
        text(ctx, "WHAT IF YOU DUG", CX, H * 0.47, 84 * U, WHITE, a)
        text(ctx, "A HOLE THROUGH", CX, H * 0.47 + 100 * U, 84 * U, WHITE, a)
        text(ctx, "THE EARTH?", CX, H * 0.47 + 205 * U, 96 * U, GOLD, a)
    else:
        text(ctx, "WHAT IF YOU DUG A HOLE", W * 0.36, AY - 60 * U, 80 * U, WHITE, a)
        text(ctx, "THROUGH THE EARTH?", W * 0.36, AY + 50 * U, 88 * U, GOLD, a)


def derrick(ctx, x, y, s, t):
    rgba(ctx, GOLD); ctx.set_line_width(5 * s)
    ctx.move_to(x - 60 * s, y); ctx.line_to(x, y - 260 * s); ctx.line_to(x + 60 * s, y); ctx.stroke()
    for k in range(1, 6):
        yy = y - k * 45 * s; hw = 60 * s * (1 - k * 45 / 260)
        ctx.move_to(x - hw, yy); ctx.line_to(x + hw, yy); ctx.stroke()
    circle(ctx, x, y - 262 * s, 10 * s, GOLD)


def sc_deepest(ctx, t, d):
    bg(ctx, t, 0.4)
    if VERT:
        gx, gy, gw = CX, H * 0.2, W * 0.86     # ground strip for the borehole
        ex, ey, R = CX, H * 0.5, 210 * U
    else:
        gx, gy, gw = W * 0.27, AY - 80 * U, W * 0.4
        ex, ey, R = W * 0.72, AY - 30 * U, 250 * U
    # ground cross-section with borehole
    gh = (H * 0.16) if VERT else 330 * U
    ctx.rectangle(gx - gw / 2, gy, gw, gh); rgba(ctx, CRUST); ctx.fill()
    ctx.rectangle(gx - gw / 2, gy, gw, 12 * U); rgba(ctx, EARTH_G); ctx.fill()
    for i in range(4):
        ctx.rectangle(gx - gw / 2, gy + gh * (0.25 + 0.2 * i), gw, 3 * U); rgba(ctx, (0.3, 0.24, 0.18)); ctx.fill()
    derrick(ctx, gx, gy, (0.55 if VERT else 0.8) * U, t)
    k = prog(t, 1.0, 5.0)
    hd = gh * 0.85 * k
    ctx.rectangle(gx - 3 * U, gy, 6 * U, hd); rgba(ctx, (0.03, 0.03, 0.06)); ctx.fill()
    if k: glow(ctx, gx, gy + hd, 26 * U, GOLD, 0.8)
    a = prog(t, 3.5, 4.3)
    label(ctx, "DEEPEST HOLE: ~12 KM", gx + (180 if VERT else 0) * U, gy + gh * 0.55 if not VERT else gy + gh * 0.5, 36 * U, GOLD, a, "c")
    # Earth to compare
    b = prog(t, 7.0, 8.0)
    if b:
        section(ctx, ex, ey, R, t, b, False)
        rgba(ctx, WHITE, 0.9 * b); ctx.set_line_width(4 * U)
        ctx.move_to(ex - R, ey + R + 40 * U); ctx.line_to(ex + R, ey + R + 40 * U); ctx.stroke()
        for sx_ in (-1, 1):
            ctx.move_to(ex + sx_ * R, ey + R + 25 * U); ctx.line_to(ex + sx_ * R, ey + R + 55 * U); ctx.stroke()
        label(ctx, "EARTH: ~12,700 KM ACROSS", ex, ey + R + 90 * U if not VERT else ey - R - 60 * U, 38 * U, WHITE, b)
        # the pinprick at scale
        p = prog(t, 10.5, 11.3)
        if p:
            pr = R * 12 / 6371
            circle(ctx, ex, ey - R + pr, max(3 * U, pr), GOLD, p)
            ctx.arc(ex, ey - R, 46 * U, 0, 2 * math.pi); rgba(ctx, GOLD, p); ctx.set_line_width(4 * U); ctx.stroke()
            label(ctx, "12 KM AT SCALE", ex + (R * 0.62 if not VERT else R * 0.9), ey - R - 40 * U if not VERT else ey - R + 40 * U, 30 * U, GOLD, p, "l")
    chip(ctx, "THE DEEPEST HOLE EVER", t)


def sc_layers(ctx, t, d):
    bg(ctx, t, 0.4)
    R = (300 if VERT else 330) * U
    ex, ey = (CX, H * 0.36) if VERT else (W * 0.33, AY)
    section(ctx, ex, ey, R, t, 1, False)
    items = [("CRUST", 0.985, -2.5, 0.3, "THIN SHELL OF ROCK"), ("MANTLE", 0.75, -2.0, 1.2, "~2,900 KM OF HOT ROCK"),
             ("OUTER CORE", 0.38, -1.0, 5.0, "LIQUID IRON & NICKEL"), ("INNER CORE", 0.0, 0.0, 8.5, "SOLID METAL BALL")]
    for i, (name, rr, ang, st, sub) in enumerate(items):
        a = prog(t, st, st + 0.8)
        if not a: continue
        if VERT:
            p = (ex + math.cos(ang + 0.6) * R * rr, ey + math.sin(ang + 0.6) * R * rr) if rr else (ex, ey)
            lx, ly = (60 * U if i % 2 == 0 else W - 60 * U), H * 0.62 + (i // 2) * 0 * U
            ly = [H * 0.58, H * 0.58, H * 0.645, H * 0.645][i]
            lx = [60 * U, W * 0.53, 60 * U, W * 0.53][i]
            leader(ctx, p, (lx + 150 * U, ly - 40 * U), a, GOLD)
            text(ctx, name, lx, ly - 10 * U, 38 * U, GOLD, a, True, "l")
            text(ctx, sub, lx, ly + 30 * U, 24 * U, WHITE, a, False, "l")
        else:
            p = (ex + math.cos(ang * 0.25 - 0.5) * R * rr, ey + math.sin(ang * 0.25 - 0.5) * R * rr) if rr else (ex, ey)
            lx, ly = W * 0.6, AY - 260 * U + i * 165 * U
            leader(ctx, p, (lx - 30 * U, ly), a, GOLD)
            text(ctx, name, lx, ly - 18 * U, 48 * U, GOLD, a, True, "l")
            text(ctx, sub, lx, ly + 34 * U, 30 * U, WHITE, a, False, "l")
    chip(ctx, "INSIDE THE EARTH", t)


def sc_heat(ctx, t, d):
    bg(ctx, t, 0.3)
    if VERT:
        c1, c2 = (CX, H * 0.27), (CX, H * 0.53)
    else:
        c1, c2 = (W * 0.28, AY), (W * 0.72, AY)
    # core vs Sun
    x, y = c1
    r = 120 * U
    glow(ctx, x - 170 * U, y, r * 1.8, OCORE, 0.5)
    circle(ctx, x - 170 * U, y, r, OCORE); circle(ctx, x - 170 * U, y, r * 0.35, ICORE)
    text(ctx, "CORE", x - 170 * U, y + r + 40 * U, 32 * U, WHITE)
    text(ctx, "≈", x, y, 90 * U, GOLD, prog(t, 1.5, 2.2))
    a = prog(t, 2.0, 3.0)
    if a:
        sun(ctx, x + 180 * U, y, r * 0.75, t, a)
        text(ctx, "SUN'S SURFACE", x + 180 * U, y + r + 40 * U, 32 * U, WHITE, a)
    if not VERT: label(ctx, "ROUGHLY AS HOT", x, y - r - 90 * U, 44 * U, GOLD, prog(t, 2.5, 3.2))
    # pressure: crushing arrows on a cube
    x, y = c2
    b = prog(t, 5.0, 6.0)
    if b:
        sq = 120 * U * (1 - 0.15 * prog(t, 6.0, 8.0) * (0.8 + 0.2 * math.sin(t * 8)))
        rrect(ctx, x - sq / 2, y - sq / 2, sq, sq, 10 * U); rgba(ctx, (0.6, 0.65, 0.75), b); ctx.fill()
        for i in range(8):
            ang = i / 8 * 2 * math.pi
            ux, uy = math.cos(ang), math.sin(ang)
            r0, r1 = 230 * U - 20 * U * math.sin(t * 4), 120 * U
            rgba(ctx, CORAL, b); ctx.set_line_width(10 * U); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
            ctx.move_to(x + ux * r0, y + uy * r0); ctx.line_to(x + ux * r1, y + uy * r1); ctx.stroke()
            px, py = x + ux * (r1 - 10 * U), y + uy * (r1 - 10 * U)
            ctx.move_to(px, py); ctx.line_to(px + ux * 34 * U - uy * 22 * U, py + uy * 34 * U + ux * 22 * U)
            ctx.line_to(px + ux * 34 * U + uy * 22 * U, py + uy * 34 * U - ux * 22 * U); ctx.close_path(); ctx.fill()
        label(ctx, "PRESSURE: 3 MILLION× AIR", x, y + 300 * U if not VERT else y + 290 * U, 40 * U, CORAL, prog(t, 6.0, 6.8))
    chip(ctx, "HEAT AND PRESSURE", t)


def fall_pos(tau_min, period=84.0):
    """position along the tunnel (−1 top … +1 bottom) for a uniform-density Earth, tau in minutes"""
    return -math.cos(2 * math.pi * tau_min / period)


def sc_fall(ctx, t, d):
    bg(ctx, t, 0.4)
    R = (300 if VERT else 320) * U
    ex, ey = (CX, H * 0.37) if VERT else (W * 0.3, AY)
    section(ctx, ex, ey, R, t)
    run = prog(t, 6.0, 13.0)
    tau = 42 * run
    y = ey + R * fall_pos(tau) * 0.96
    if t < 6: y = ey - R - 50 * U
    person(ctx, ex, y, 1.0 * U, math.pi if 6 < t else 0, WHITE, 1, 1 if t > 6 else 0)
    glow(ctx, ex, y, 60 * U, WHITE, 0.3)
    # clock
    if VERT: cx_, cy_, cr = CX + 340 * U, H * 0.13 + 60 * U, 90 * U
    else: cx_, cy_, cr = W * 0.66, AY - 60 * U, 150 * U
    k = prog(t, 5.5, 6.2)
    if k:
        circle(ctx, cx_, cy_, cr, NAVY2, k)
        ctx.arc(cx_, cy_, cr, 0, 2 * math.pi); rgba(ctx, WHITE, 0.5 * k); ctx.set_line_width(4 * U); ctx.stroke()
        ctx.arc(cx_, cy_, cr - 12 * U, -math.pi / 2, -math.pi / 2 + 2 * math.pi * tau / 60)
        rgba(ctx, GOLD, k); ctx.set_line_width(14 * U); ctx.stroke()
        text(ctx, f"{int(tau)}", cx_, cy_ - 10 * U, cr * 0.7, WHITE, k)
        text(ctx, "MIN", cx_, cy_ + cr * 0.45, cr * 0.25, GOLD, k)
    r2 = prog(t, 13.5, 14.3)
    if r2:
        if VERT: label(ctx, "REALISTIC EARTH: ~38 MIN", CX, H * 0.66, 38 * U, CYAN, r2)
        else: label(ctx, "REALISTIC EARTH: ~38 MIN", W * 0.66, AY + 210 * U, 44 * U, CYAN, r2)
    if not VERT and t > 6.5:
        label(ctx, "NO AIR · NO HEAT · PERFECT TUBE", W * 0.66, AY - 300 * U, 34 * U, WHITE, prog(t, 0.5, 1.3))
    elif VERT:
        label(ctx, "PERFECT TUBE, NO AIR", CX - 150 * U, H * 0.13 + 60 * U, 30 * U, WHITE, prog(t, 0.5, 1.3))
    chip(ctx, "THE FALL", t)


def sc_speed(ctx, t, d):
    bg(ctx, t, 0.3)
    gx, gy = (CX, H * 0.33) if VERT else (W * 0.3, AY + 60 * U)
    R = (250 if VERT else 260) * U
    # gauge
    ctx.arc(gx, gy, R, math.pi, 2 * math.pi); rgba(ctx, (0.15, 0.18, 0.32)); ctx.set_line_width(40 * U); ctx.stroke()
    v = prog(t, 0.8, 4.0) * (1 + 0.01 * math.sin(t * 20))
    ctx.arc(gx, gy, R, math.pi, math.pi + math.pi * v * 0.85); rgba(ctx, GOLD); ctx.stroke()
    for i in range(11):
        ang = math.pi + math.pi * i / 10
        rgba(ctx, WHITE, 0.6); ctx.set_line_width(3 * U)
        ctx.move_to(gx + math.cos(ang) * (R - 40 * U), gy + math.sin(ang) * (R - 40 * U))
        ctx.line_to(gx + math.cos(ang) * (R - 60 * U), gy + math.sin(ang) * (R - 60 * U)); ctx.stroke()
    ang = math.pi + math.pi * v * 0.85
    rgba(ctx, CORAL); ctx.set_line_width(10 * U); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.move_to(gx, gy); ctx.line_to(gx + math.cos(ang) * (R - 70 * U), gy + math.sin(ang) * (R - 70 * U)); ctx.stroke()
    circle(ctx, gx, gy, 20 * U, WHITE)
    text(ctx, f"{8 * prog(t, 0.8, 4.0):.1f} KM/S".replace("8.0", "≈ 8"), gx, gy + 70 * U, 64 * U, GOLD)
    # city crossing
    if VERT: cx0, cx1, cy = 60 * U, W - 60 * U, H * 0.6
    else: cx0, cx1, cy = W * 0.56, W * 0.95, AY + 120 * U
    a = prog(t, 5.0, 5.8)
    if a:
        random.seed(6)
        x = cx0
        while x < cx1:
            bw = random.uniform(30, 60) * U; bh = random.uniform(60, 220) * U
            ctx.rectangle(x, cy - bh, min(bw, cx1 - x), bh); rgba(ctx, (0.15, 0.2, 0.38), a); ctx.fill()
            for wy in range(int(bh / (26 * U)) - 1):
                if random.random() < 0.5: ctx.rectangle(x + 8 * U, cy - bh + 12 * U + wy * 26 * U, 8 * U, 10 * U); rgba(ctx, GOLD, 0.6 * a); ctx.fill()
            x += bw + 6 * U
        k = ((t - 6.0) / 2.0) % 1.0 if t > 6 else 0
        if t > 6:
            sx_ = cx0 + (cx1 - cx0) * k; sy_ = cy - 280 * U
            g = cairo.LinearGradient(sx_ - 300 * U, 0, sx_, 0); g.add_color_stop_rgba(0, 1, 1, 1, 0); g.add_color_stop_rgba(1, 1, 1, 1, 0.8)
            ctx.set_source(g); ctx.rectangle(max(cx0, sx_ - 300 * U), sy_ - 5 * U, min(300 * U, sx_ - cx0), 10 * U); ctx.fill()
            circle(ctx, sx_, sy_, 12 * U, WHITE)
        label(ctx, "A WHOLE CITY IN ~2 SECONDS", (cx0 + cx1) / 2, cy + 50 * U, 34 * U, WHITE, prog(t, 7.0, 7.8))
    chip(ctx, "TOP SPEED AT THE CENTER", t)


def sc_center(ctx, t, d):
    bg(ctx, t, 0.2)
    x, y = CX, AY
    R = 330 * U
    glow(ctx, x, y, R * 1.4, OCORE, 0.5)
    circle(ctx, x, y, R, ICORE, 0.25)
    circle(ctx, x, y, R * 0.55, (0.05, 0.05, 0.1), 0.9)
    f = math.sin(t * 1.2) * 14 * U
    person(ctx, x, y + f, 1.6 * U, 0.3 * math.sin(t * 0.7), WHITE, 1, 0.6 + 0.4 * math.sin(t * 1.5))
    a = prog(t, 2.5, 3.3)
    for i in range(12):
        ang = i / 12 * 2 * math.pi
        r0, r1 = R * 0.62, R * 0.95
        ux, uy = math.cos(ang), math.sin(ang)
        rgba(ctx, GOLD, a); ctx.set_line_width(6 * U); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.move_to(x + ux * r0, y + uy * r0); ctx.line_to(x + ux * r1, y + uy * r1); ctx.stroke()
        ctx.move_to(x + ux * (r1 + 18 * U), y + uy * (r1 + 18 * U))
        ctx.line_to(x + ux * r1 - uy * 14 * U, y + uy * r1 + ux * 14 * U); ctx.line_to(x + ux * r1 + uy * 14 * U, y + uy * r1 - ux * 14 * U)
        ctx.close_path(); ctx.fill()
    label(ctx, "WEIGHTLESS", x, y - R - 70 * U if VERT else y - R + 20 * U, 60 * U, WHITE, prog(t, 0.5, 1.3))
    if not VERT: label(ctx, "EQUAL PULL FROM EVERY SIDE", W * 0.8, y, 34 * U, GOLD, a)
    else: label(ctx, "EQUAL PULL FROM EVERY SIDE", x, y + R + 70 * U, 34 * U, GOLD, a)
    chip(ctx, "THE CENTER", t)


def sc_rotation(ctx, t, d):
    bg(ctx, t, 0.4)
    R = (250 if VERT else 270) * U
    e1 = (CX, H * 0.33) if VERT else (W * 0.28, AY - 20 * U)
    section(ctx, *e1, R, t)
    damp = prog(t, 5.5, 10.0)
    amp = 0.96 * (1 - damp) + 0.0 * damp
    y = e1[1] + R * amp * math.sin(t * 1.4)
    for k in range(1, 6):   # trail
        circle(ctx, e1[0], e1[1] + R * amp * math.sin((t - k * 0.06) * 1.4), 8 * U, WHITE, 0.15 * (6 - k) / 5)
    person(ctx, e1[0], y, 0.8 * U, math.pi * (0.5 + 0.5 * math.sin(t * 1.4)), WHITE)
    lab = "LIKE A PENDULUM" if damp < 0.4 else "AIR STOPS YOU IN THE MIDDLE"
    if VERT:
        label(ctx, lab, CX, e1[1] + R + 60 * U, 36 * U, GOLD, prog(t, 1.0, 1.8))
    else:
        label(ctx, lab, e1[0], e1[1] + R + 55 * U, 36 * U, GOLD, prog(t, 1.0, 1.8))
    # spinning Earth: hole from the equator hits the walls
    b = prog(t, 10.5, 11.3)
    if b:
        e2 = (CX, H * 0.33) if VERT else (W * 0.72, AY)
        if VERT:
            ctx.rectangle(0, H * 0.12, W, H * 0.58); rgba(ctx, NAVY, 0.92 * b); ctx.fill()
        r2 = R * 0.9
        earth(ctx, e2[0], e2[1], r2, b)
        # spin arrow
        ctx.save(); ctx.translate(e2[0], e2[1]); ctx.scale(1, 0.3)
        ctx.arc(0, 0, r2 * 1.25, 0.2, math.pi - 0.2); ctx.restore()
        rgba(ctx, GOLD, b); ctx.set_line_width(6 * U); ctx.stroke()
        ax, ay = e2[0] - r2 * 1.25 * math.cos(0.2), e2[1] + r2 * 0.3 * 1.25 * math.sin(0.2)
        ctx.move_to(ax - 10 * U, ay - 20 * U); ctx.line_to(ax - 10 * U, ay + 18 * U); ctx.line_to(ax - 34 * U, ay - 4 * U); ctx.close_path(); ctx.fill()
        # pole-to-pole axis
        ctx.set_dash([12 * U, 10 * U]); rgba(ctx, WHITE, 0.8 * b); ctx.set_line_width(4 * U)
        ctx.move_to(e2[0], e2[1] - r2 * 1.2); ctx.line_to(e2[0], e2[1] + r2 * 1.2); ctx.stroke(); ctx.set_dash([])
        label(ctx, "POLE TO POLE: NO WALL HITS", e2[0], e2[1] - r2 - 70 * U, 34 * U, WHITE, prog(t, 12.5, 13.3))
    chip(ctx, "BACK AND FORTH", t)


def sc_antipode(ctx, t, d):
    bg(ctx, t, 0.4)
    R = (300 if VERT else 280) * U
    ex, ey = (CX, H * 0.38) if VERT else (W * 0.5, AY + 20 * U)
    earth(ctx, ex, ey, R)
    def route(ang, k, c, a):
        x0, y0 = ex + math.cos(ang) * R, ey + math.sin(ang) * R
        x1, y1 = ex - math.cos(ang) * R, ey - math.sin(ang) * R
        circle(ctx, x0, y0, 12 * U, c, a)
        ctx.set_dash([12 * U, 9 * U]); rgba(ctx, c, a); ctx.set_line_width(5 * U)
        ctx.move_to(x0, y0); ctx.line_to(x0 + (x1 - x0) * k, y0 + (y1 - y0) * k); ctx.stroke(); ctx.set_dash([])
        if k >= 1: circle(ctx, x1, y1, 12 * U, c, a)
        return (x0, y0), (x1, y1)
    k1 = prog(t, 6.0, 8.0)
    a1 = prog(t, 5.5, 6.0)
    if a1:
        p0, p1 = route(math.radians(-140), k1, GOLD, a1)
        label(ctx, "SPAIN", p0[0] - 20 * U, p0[1] - 40 * U, 32 * U, GOLD, a1, "r")
        label(ctx, "NEAR NEW ZEALAND", p1[0] + 20 * U, p1[1] + 40 * U, 32 * U, GOLD, k1 if k1 >= 1 else 0, "l" if not VERT else "r")
    k2 = prog(t, 10.0, 12.0)
    a2 = prog(t, 9.5, 10.0)
    if a2:
        p0, p1 = route(math.radians(-25), k2, CYAN, a2)
        label(ctx, "USA", p0[0] + 20 * U, p0[1] - 40 * U, 32 * U, CYAN, a2, "l" if not VERT else "r")
        if k2 >= 1:
            for i in range(5):   # splash
                ang = -math.pi / 2 + (i - 2) * 0.35
                circle(ctx, p1[0] + math.cos(ang) * 40 * U, p1[1] + math.sin(ang) * 40 * U - 10 * U, 8 * U, (0.7, 0.9, 1.0))
            label(ctx, "INDIAN OCEAN", p1[0] - 20 * U, p1[1] + 50 * U, 32 * U, CYAN, prog(t, 12.0, 12.6), "r" if not VERT else "l")
    m = prog(t, 2.0, 2.8)
    if VERT: label(ctx, "MOST LAND IS OPPOSITE AN OCEAN", CX, H * 0.665, 34 * U, WHITE, m * (1 - prog(t, 5.0, 5.5)))
    else: label(ctx, "MOST LAND IS OPPOSITE AN OCEAN", CX, ey - R - 45 * U, 36 * U, WHITE, m)
    chip(ctx, "WHERE WOULD YOU COME OUT?", t)


def sc_outro(ctx, t, d):
    bg(ctx, t, 0.6)
    yo = -80 * U if not VERT else -200 * U
    section(ctx, CX, CY + yo - 200 * U, 75 * U, t)
    k_ = (t * 0.4) % 1
    circle(ctx, CX, CY + yo - 200 * U - 75 * U * math.cos(k_ * math.pi), 6 * U, WHITE)
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
    if q and k < 1: text(ctx, "Where would your hole come out?", CX, CY + yo + 260 * U, (42 if not VERT else 38) * U, WHITE, q * (1 - k))


SHORT_SCENES = ["hook", "fall", "speed", "center", "outro"]

SCENES = dict(hook=sc_hook, title=sc_title, deepest=sc_deepest, layers=sc_layers, heat=sc_heat, fall=sc_fall,
              speed=sc_speed, center=sc_center, rotation=sc_rotation, antipode=sc_antipode, outro=sc_outro)


def thumbnail(c):
    """1280x720 thumbnail: Earth cut in half with a glowing tunnel and a falling figure."""
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, .08, .11, .26); g.add_color_stop_rgb(1, .02, .03, .08); c.set_source(g); c.paint()
    random.seed(1)
    for _ in range(180):
        c.arc(random.random() * W, random.random() * H, random.uniform(.5, 1.8), 0, 6.3); c.set_source_rgba(1, 1, 1, random.uniform(.3, .9)); c.fill()
    ex, ey, R = 1035, 370, 230
    section(c, ex, ey, R, 0.8)
    # glowing tunnel
    rg = cairo.LinearGradient(ex - 20, 0, ex + 20, 0)
    for s_, a_ in [(0, 0), (0.5, 0.55), (1, 0)]: rg.add_color_stop_rgba(s_, 1, .9, .5, a_)
    c.set_source(rg); c.rectangle(ex - 30, ey - R, 60, 2 * R); c.fill()
    person(c, ex, ey - 70, 1.6, math.pi, (1, 1, 1), 1, 1)
    thumb_text(c, "WHAT IF YOU DUG", "THROUGH EARTH?", "42 MINUTES")
