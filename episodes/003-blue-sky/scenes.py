# Scenes for "Why is the sky blue (and sunsets orange)?"
# Executed inside engine/render.py: all helpers (W, H, U, CX, CY, VERT, colors, vgrad, circle, glow,
# text, rrect, stars, sun, chip, prog, ease, mix...) are available.

_text0 = text
def text(ctx, *a, **k):
    r = _text0(ctx, *a, **k); ctx.new_path(); return r

RAINBOW = [(0.93, 0.22, 0.22), (1.0, 0.55, 0.15), (1.0, 0.88, 0.25), (0.30, 0.80, 0.40), (0.25, 0.55, 1.0), (0.58, 0.35, 0.95)]
SKY_T, SKY_B = (0.14, 0.40, 0.84), (0.55, 0.78, 0.97)
DUSK_T, DUSK_M, DUSK_B = (0.10, 0.10, 0.30), (0.85, 0.40, 0.35), (1.0, 0.70, 0.30)
BLUE = (0.35, 0.65, 1.0)

def fit(ctx, s, x, y, size, c=WHITE, a=1.0, bold=True, align="c", maxw=None):
    maxw = maxw or W * 0.9
    font(ctx, size, bold); w = ctx.text_extents(s).width
    if w > maxw: size *= maxw / w
    return text(ctx, s, x, y, size, c, a, bold, align)

def sky(ctx, k, y1):
    """Sky gradient: k = 0 clear day → 1 sunset."""
    g = cairo.LinearGradient(0, 0, 0, y1)
    g.add_color_stop_rgb(0, *mix(SKY_T, DUSK_T, k))
    g.add_color_stop_rgb(0.6, *mix(mix(SKY_T, SKY_B, 0.6), DUSK_M, k))
    g.add_color_stop_rgb(1, *mix(SKY_B, DUSK_B, k))
    ctx.set_source(g); ctx.rectangle(0, 0, W, y1 + 2); ctx.fill()

def cloud(ctx, x, y, s, c=WHITE, a=1.0):
    for dx, dy, r in [(-60, 10, 45), (-15, -20, 60), (40, -5, 50), (80, 15, 38), (10, 20, 45)]:
        circle(ctx, x + dx * s, y + dy * s, r * s, c, a)

def hills(ctx, y, c, a=1.0, seed=0.0):
    ctx.move_to(0, H)
    for i in range(41):
        x = W * i / 40
        ctx.line_to(x, y - 40 * U * math.sin(i * 0.45 + seed) - 22 * U * math.sin(i * 1.3 + seed))
    ctx.line_to(W, H); ctx.close_path(); rgba(ctx, c, a); ctx.fill()

def arrow(ctx, x0, y0, x1, y1, c, a=1.0, w=5):
    ang = math.atan2(y1 - y0, x1 - x0)
    ctx.move_to(x0, y0); ctx.line_to(x1 - math.cos(ang) * 14 * U, y1 - math.sin(ang) * 14 * U)
    rgba(ctx, c, a); ctx.set_line_width(w * U); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    ctx.move_to(x1, y1)
    ctx.line_to(x1 - math.cos(ang - 0.45) * 22 * U, y1 - math.sin(ang - 0.45) * 22 * U)
    ctx.line_to(x1 - math.cos(ang + 0.45) * 22 * U, y1 - math.sin(ang + 0.45) * 22 * U)
    ctx.close_path(); ctx.fill()

def molecule(ctx, x, y, s, a=1.0):
    circle(ctx, x - 9 * s, y, 13 * s, (0.92, 0.95, 1.0), a); circle(ctx, x + 9 * s, y, 13 * s, (0.80, 0.86, 0.98), a)

def sc_hook(ctx, t, d):
    k = prog(t, d * 0.5, d * 0.85)
    hz = H * 0.68 if not VERT else H * 0.62
    sky(ctx, k, H)
    sx = (W * 0.72 if not VERT else W * 0.70) + k * 60 * U
    sy = mix((H * 0.22, 0, 0), (hz - 10 * U, 0, 0), k)[0] if not VERT else mix((H * 0.30, 0, 0), (hz - 10 * U, 0, 0), k)[0]
    glow(ctx, sx, sy, 260 * U, mix((1, 1, 0.9), (1, 0.6, 0.2), k), 0.55)
    circle(ctx, sx, sy, 70 * U, mix((1, 0.97, 0.8), (1, 0.62, 0.25), k))
    for i, (fx, fy, s) in enumerate([(0.18, 0.20, 1.1), (0.45, 0.32, 0.8), (0.85, 0.12, 0.9)]):
        x = (W * fx + t * 18 * U * (1 + i * 0.3)) % (W + 300 * U) - 150 * U
        cloud(ctx, x, H * fy * (1 if not VERT else 1.2) + (60 * U if VERT else 0), s * U, mix(WHITE, (1, 0.75, 0.6), k), 0.9)
    hills(ctx, hz + 30 * U, mix((0.20, 0.42, 0.28), (0.10, 0.06, 0.12), k), 1, 0.5)
    hills(ctx, hz + 90 * U, mix((0.14, 0.32, 0.22), (0.06, 0.03, 0.08), k), 1, 2.0)
    ty = H * 0.12 if not VERT else H * 0.14
    a1 = prog(t, 0.6, 1.3) * (1 - prog(t, d * 0.5, d * 0.58))
    if a1: fit(ctx, "WHY BLUE?", CX, ty, 90 * U, WHITE, a1)
    a2 = prog(t, d * 0.62, d * 0.72)
    if a2: fit(ctx, "…AND WHY ORANGE?", CX, ty, 90 * U, (1, 0.85, 0.5), a2)

def sc_white(ctx, t, d):
    vgrad(ctx, NAVY2, NAVY); stars(ctx, t, 0.4)
    if VERT: px, py, h = CX - 120 * U, 760 * U, 230 * U
    else: px, py, h = CX - 160 * U, CY - 60 * U, 260 * U
    A = (px, py - h * 0.62); B = (px - h * 0.62, py + h * 0.45); C = (px + h * 0.62, py + h * 0.45)
    inp = ((A[0] + B[0]) / 2, (A[1] + B[1]) / 2); outp = ((A[0] + C[0]) / 2, (A[1] + C[1]) / 2)
    p1 = prog(t, 0.3, 1.8); p2 = prog(t, 2.0, 4.0)
    # white beam
    x0, y0 = -20 * U, inp[1] + 120 * U
    ctx.move_to(x0, y0); ctx.line_to(x0 + (inp[0] - x0) * p1, y0 + (inp[1] - y0) * p1)
    rgba(ctx, WHITE, 0.95); ctx.set_line_width(16 * U); ctx.stroke()
    glow(ctx, inp[0], inp[1], 70 * U, WHITE, 0.4 * p1)
    # rainbow fan
    ex = W - 60 * U
    spread = 300 * U if not VERT else 230 * U
    if p2:
        for i, c in enumerate(RAINBOW):
            yy = outp[1] + 40 * U + (-0.5 + i / 5) * spread * 1.0
            x1 = outp[0] + (ex - outp[0]) * p2; y1 = outp[1] + (yy - outp[1]) * p2
            ctx.move_to(outp[0], outp[1] + (i - 2.5) * 2 * U); ctx.line_to(x1, y1)
            rgba(ctx, c, 0.95); ctx.set_line_width(13 * U); ctx.stroke()
    # prism
    ctx.move_to(*A); ctx.line_to(*B); ctx.line_to(*C); ctx.close_path()
    rgba(ctx, (0.75, 0.88, 1.0), 0.22); ctx.fill_preserve(); rgba(ctx, (0.85, 0.95, 1.0), 0.9); ctx.set_line_width(5 * U); ctx.stroke()
    ctx.move_to(A[0] - 20 * U, A[1] + 50 * U); ctx.line_to(A[0] - 70 * U, A[1] + 140 * U); rgba(ctx, WHITE, 0.5); ctx.set_line_width(6 * U); ctx.stroke()
    ty = H * 0.13 if not VERT else 330 * U
    fit(ctx, "WHITE LIGHT = ALL COLORS", CX, ty, 64 * U, WHITE, prog(t, 0.5, 1.2))
    a = prog(t, 4.0, 4.8)
    if a:
        labs = ["red", "orange", "yellow", "green", "blue", "violet"]
        for i, c in enumerate(RAINBOW):
            yy = outp[1] + 40 * U + (-0.5 + i / 5) * spread
            text(ctx, labs[i], ex - 10 * U, yy - 26 * U, 28 * U, c, a, True, "r")

def wave(ctx, x0, x1, y, lam, amp, ph, c, w=8):
    for i in range(301):
        x = x0 + (x1 - x0) * i / 300
        yy = y + amp * math.sin(2 * math.pi * (x - x0) / lam - ph)
        (ctx.line_to if i else ctx.move_to)(x, yy)
    rgba(ctx, c); ctx.set_line_width(w * U); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()

def sc_waves(ctx, t, d):
    vgrad(ctx, NAVY2, NAVY); stars(ctx, t, 0.3)
    x0, x1 = W * 0.08, W * 0.92
    rows = [(RAINBOW[0], 380 * U, "RED · LONG WAVES", "≈ 700 nm", H * 0.27 if not VERT else 600 * U, 0.6),
            (RAINBOW[4], 245 * U, "BLUE · SHORT WAVES", "≈ 450 nm", H * 0.62 if not VERT else 1040 * U, 2.2)]
    for c, lam, lab, nm, y, ta in rows:
        a = prog(t, ta, ta + 0.7)
        if not a: continue
        ctx.save(); ctx.rectangle(x0 - 10 * U, 0, (x1 - x0 + 20 * U) * a, H); ctx.clip()
        glow(ctx, CX, y, 300 * U, c, 0.12)
        wave(ctx, x0, x1, y, lam, 70 * U, t * 3, c)
        ctx.restore()
        text(ctx, lab, x0, y - 115 * U, 44 * U, c, a, True, "l")
        # wavelength bracket
        bx = x0 + lam * 0.25 + (t * 3 / (2 * math.pi)) * lam % lam
        bx = x0 + ((lam * 0.25 + t * 3 / (2 * math.pi) * lam) % lam)
        by = y + 98 * U
        if bx + lam < x1:
            ctx.move_to(bx, by - 15 * U); ctx.line_to(bx, by + 15 * U); ctx.move_to(bx, by); ctx.line_to(bx + lam, by)
            ctx.move_to(bx + lam, by - 15 * U); ctx.line_to(bx + lam, by + 15 * U)
            rgba(ctx, WHITE, 0.8 * a); ctx.set_line_width(3 * U); ctx.stroke()
            text(ctx, nm, bx + lam / 2, by + 32 * U, 30 * U, WHITE, 0.9 * a, False)

def person(ctx, x, y, s, c):
    circle(ctx, x, y - 100 * s, 16 * s, c)
    ctx.set_line_width(10 * s); ctx.set_line_cap(cairo.LINE_CAP_ROUND); rgba(ctx, c)
    ctx.move_to(x, y - 82 * s); ctx.line_to(x, y - 42 * s)
    ctx.move_to(x, y - 42 * s); ctx.line_to(x - 16 * s, y); ctx.move_to(x, y - 42 * s); ctx.line_to(x + 16 * s, y)
    ctx.move_to(x, y - 72 * s); ctx.line_to(x - 24 * s, y - 50 * s); ctx.move_to(x, y - 72 * s); ctx.line_to(x + 24 * s, y - 50 * s)
    ctx.stroke()

def sc_scatter(ctx, t, d):
    vgrad(ctx, (0.05, 0.10, 0.28), (0.20, 0.42, 0.75))
    gy = H * 0.76 if not VERT else 1250 * U
    if VERT: sx, sy, gx, ox = W - 130 * U, 450 * U, CX + 60 * U, 170 * U
    else: sx, sy, gx, ox = W - 200 * U, 200 * U, W * 0.50, W * 0.17
    rgba(ctx, (0.12, 0.22, 0.16)); ctx.rectangle(0, gy, W, H - gy); ctx.fill()
    # background molecules
    random.seed(21)
    for j in range(40):
        mx = random.random() * W; my = random.uniform(0.25, 0.95) * gy
        molecule(ctx, mx + 6 * U * math.sin(t + j), my, 0.7 * U, 0.25)
    sun(ctx, sx, sy, 60 * U, t)
    pb = prog(t, 0.3, 1.8)
    # incoming beam (all colours)
    for i, c in enumerate(RAINBOW):
        off = (i - 2.5) * 5 * U
        ctx.move_to(sx, sy + off); ctx.line_to(sx + (gx - sx) * pb, sy + off + (gy - sy) * pb)
        rgba(ctx, c, 0.55); ctx.set_line_width(5 * U); ctx.stroke()
    # molecules on the beam, scattering blue
    ps = prog(t, 2.0, 3.0)
    for k, f in enumerate((0.3, 0.5, 0.7)):
        mx, my = sx + (gx - sx) * f, sy + (gy - sy) * f
        if ps:
            for n in range(3):
                rr = ((t * 140 * U + n * 90 * U + k * 40 * U) % (270 * U))
                fa = (1 - rr / (270 * U)) * ps
                for m in range(10):
                    an = m / 10 * 2 * math.pi + k
                    circle(ctx, mx + rr * math.cos(an), my + rr * math.sin(an), 7 * U, BLUE, 0.9 * fa)
                # a rare red one
                an = 0.7 + k + n
                circle(ctx, mx + rr * math.cos(an), my + rr * math.sin(an), 6 * U, RAINBOW[0], 0.6 * fa * (n == 0))
        glow(ctx, mx, my, 50 * U, WHITE, 0.4)
        molecule(ctx, mx, my, 1.4 * U)
    # observer and the blue reaching the eye from everywhere
    person(ctx, ox, gy, 1.3 * U, WHITE)
    ea = prog(t, d * 0.45, d * 0.55)
    if ea:
        ctx.set_dash([12 * U, 10 * U])
        for k, f in enumerate((0.3, 0.5, 0.7)):
            mx, my = sx + (gx - sx) * f, sy + (gy - sy) * f
            ctx.move_to(mx, my); ctx.line_to(ox + 8 * U, gy - 130 * U)
            rgba(ctx, BLUE, 0.9 * ea); ctx.set_line_width(4 * U); ctx.stroke()
        ctx.set_dash([])
    ty = H * 0.19 if not VERT else 300 * U
    a1 = prog(t, d * 0.25, d * 0.32) * (1 - prog(t, d * 0.72, d * 0.78))
    if a1:
        fit(ctx, "BLUE SCATTERS ≈ 5× MORE THAN RED", CX - (120 * U if not VERT else 0), ty, 54 * U, WHITE, a1, maxw=W * (0.62 if not VERT else 0.9))
    a2 = prog(t, d * 0.8, d * 0.86)
    if a2: fit(ctx, "RAYLEIGH SCATTERING", CX - (120 * U if not VERT else 0), ty, 64 * U, GOLD, a2)
    if VERT: text(ctx, "N₂ / O₂ molecules", sx + (gx - sx) * 0.5 - 60 * U, sy + (gy - sy) * 0.5 + 10 * U, 30 * U, WHITE, prog(t, 1.5, 2.2) * (1 - ea), False, "r")
    else: text(ctx, "N₂ / O₂ molecules", sx + (gx - sx) * 0.5 + 70 * U, sy + (gy - sy) * 0.5 - 50 * U, 30 * U, WHITE, prog(t, 1.5, 2.2) * (1 - ea), False, "l")
    chip(ctx, "THE SECRET: SCATTERING", t)

def bell(x, mu, sg): return math.exp(-((x - mu) / sg) ** 2 / 2)

def sc_violet(ctx, t, d):
    vgrad(ctx, NAVY2, NAVY); stars(ctx, t, 0.3)
    x0, x1 = W * 0.1, W * 0.9
    sy = H * 0.60 if not VERT else 900 * U
    top = sy - (300 * U if not VERT else 330 * U)
    # spectrum strip: violet → red
    g = cairo.LinearGradient(x0, 0, x1, 0)
    for i, c in enumerate(reversed(RAINBOW)): g.add_color_stop_rgb(i / 5, *c)
    rrect(ctx, x0, sy, x1 - x0, 46 * U, 23 * U); ctx.set_source(g); ctx.fill()
    text(ctx, "violet", x0, sy + 80 * U, 30 * U, RAINBOW[5], 1, True, "l")
    text(ctx, "red", x1, sy + 80 * U, 30 * U, RAINBOW[0], 1, True, "r")
    p = prog(t, 1.0, 3.5)
    curves = [("SUNLIGHT", GOLD, lambda u: 0.55 + 0.4 * bell(u, 0.42, 0.35) - 0.35 * bell(u, 0.0, 0.08)),
              ("EYE SENSITIVITY", WHITE, lambda u: bell(u, 0.55, 0.15))]
    for name, c, fn in curves:
        n = int(200 * p)
        for i in range(n + 1):
            u = i / 200
            (ctx.line_to if i else ctx.move_to)(x0 + (x1 - x0) * u, sy - 20 * U - fn(u) * (sy - 20 * U - top))
        rgba(ctx, c); ctx.set_line_width(6 * U); ctx.stroke()
    la = prog(t, 3.0, 3.6)
    text(ctx, "EYE SENSITIVITY", x0 + (x1 - x0) * 0.55, top - 30 * U, 32 * U, WHITE, la)
    text(ctx, "SUNLIGHT", x0 + (x1 - x0) * 0.86, sy - 20 * U - curves[0][2](0.86) * (sy - 20 * U - top) - 45 * U, 32 * U, GOLD, la)
    ty = H * 0.12 if not VERT else 300 * U
    fit(ctx, "WHY ISN'T THE SKY PURPLE?", CX, ty, 62 * U, (0.75, 0.6, 1.0), prog(t, 0.2, 0.8))
    reasons = ["LESS VIOLET IN SUNLIGHT", "SOME ABSORBED HIGH UP", "EYES PREFER BLUE"]
    for i, r in enumerate(reasons):
        a = prog(t, d * (0.35 + 0.22 * i), d * (0.35 + 0.22 * i) + 0.6)
        if not a: continue
        if VERT: bx, by, bw = CX - W * 0.4, 1060 * U + i * 85 * U, W * 0.8
        else: bx, by, bw = W * 0.07 + i * W * 0.29, sy + 125 * U, W * 0.27
        rrect(ctx, bx, by, bw, 64 * U, 32 * U); rgba(ctx, NAVY2, 0.95 * a); ctx.fill_preserve(); rgba(ctx, GOLD, a); ctx.set_line_width(3 * U); ctx.stroke()
        fit(ctx, f"{i + 1} · {r}", bx + bw / 2, by + 32 * U, 30 * U, WHITE, a, maxw=bw - 30 * U)

def sc_sunset(ctx, t, d):
    k = prog(t, d * 0.3, d * 0.8)
    vgrad(ctx, mix(NAVY2, (0.16, 0.08, 0.20), k), mix(NAVY, (0.30, 0.12, 0.10), k)); stars(ctx, t, 0.4)
    if VERT: gy, Rb, ha = 1080 * U, 1000 * U, 120 * U
    else: gy, Rb, ha = H * 0.62, 1600 * U, 140 * U
    pcx, pcy = CX, gy + Rb
    circle(ctx, pcx, pcy, Rb + ha, (0.30, 0.55, 0.95), 0.28)
    circle(ctx, pcx, pcy, Rb + ha * 0.5, (0.30, 0.55, 0.95), 0.15)
    circle(ctx, pcx, pcy, Rb, (0.13, 0.30, 0.22))
    text(ctx, "atmosphere", CX + (330 * U if not VERT else 260 * U), gy - ha * 0.45 + 10 * U, 28 * U, (0.7, 0.85, 1.0), 0.85, False)
    ox, oy = CX, gy
    person(ctx, ox, oy, 0.9 * U, WHITE)
    eye = (ox, oy - 90 * U)
    # noon: short path
    ny = 170 * U if not VERT else 420 * U
    sun(ctx, CX, ny, 45 * U, t, 1 - 0.6 * k)
    pn = prog(t, 0.5, 1.5)
    ctx.move_to(CX, ny + 70 * U); ctx.line_to(CX, ny + 70 * U + (eye[1] - 30 * U - ny - 70 * U) * pn)
    rgba(ctx, (1, 0.98, 0.9), 0.9 * (1 - 0.5 * k)); ctx.set_line_width(10 * U); ctx.stroke()
    text(ctx, "NOON: SHORT PATH", CX + 30 * U, (ny + gy) / 2 - 20 * U, 34 * U, WHITE, prog(t, 1, 1.6) * (1 - 0.5 * k), True, "l")
    # sunset: long path along the horizon
    L = math.sqrt((Rb + ha) ** 2 - Rb ** 2)
    ssx, ssy = (60 * U, gy - 30 * U) if VERT else (CX - L - 160 * U, gy - 40 * U)
    a = prog(t, d * 0.18, d * 0.26)
    if a:
        glow(ctx, ssx, ssy, 180 * U, (1, 0.6, 0.2), 0.5 * a)
        circle(ctx, ssx, ssy, 45 * U, (1, 0.7, 0.3), a)
        pl = prog(t, d * 0.22, d * 0.5)
        N = 60
        for i in range(N):
            u0, u1 = i / N, (i + 1) / N
            if u1 > pl: break
            c = mix((1, 0.98, 0.9), (1, 0.55, 0.2), clamp((u0 - 0.2) / 0.8))
            ctx.move_to(ssx + (eye[0] - ssx) * u0, ssy + (eye[1] - ssy) * u0)
            ctx.line_to(ssx + (eye[0] - ssx) * u1, ssy + (eye[1] - ssy) * u1)
            rgba(ctx, c, a); ctx.set_line_width(12 * U); ctx.stroke()
        # blue light knocked off to the sides
        random.seed(33)
        for j in range(26):
            u = random.uniform(0.15, 0.95)
            if u > pl: continue
            bx0, by0 = ssx + (eye[0] - ssx) * u, ssy + (eye[1] - ssy) * u
            ph = (t * 0.8 + random.random()) % 1.0
            dirn = -1 if j % 2 else 1
            circle(ctx, bx0 + ph * 30 * U, by0 + dirn * ph * 110 * U, 7 * U, BLUE, 0.9 * (1 - ph) * a)
        text(ctx, "SUNSET: LONG PATH", (ssx + eye[0]) / 2 + (40 * U if VERT else 0), gy - (150 if not VERT else 170) * U, 38 * U, (1, 0.75, 0.4), prog(t, d * 0.3, d * 0.38))
        glow(ctx, eye[0], eye[1], 160 * U, (1, 0.5, 0.2), 0.45 * prog(t, d * 0.5, d * 0.6))
    chip(ctx, "SUNSETS: MORE AIR, LESS BLUE", t)

def sc_clouds(ctx, t, d):
    sky(ctx, 0, H)
    for i, (fx, fy, s) in enumerate([(0.15, 0.14, 1.3), (0.6, 0.10, 1.0), (0.9, 0.2, 1.2), (0.35, 0.93, 1.4), (0.8, 0.9, 1.1)]):
        x = (W * fx + t * 15 * U) % (W + 300 * U) - 150 * U
        cloud(ctx, x, H * fy, s * U, WHITE, 0.9)
    if VERT: panels = [(W * 0.08, 330 * U, W * 0.84, 470 * U), (W * 0.08, 850 * U, W * 0.84, 470 * U)]
    else: panels = [(W * 0.06, H * 0.22, W * 0.42, H * 0.54), (W * 0.52, H * 0.22, W * 0.42, H * 0.54)]
    p = prog(t, 0.2, 0.8)
    for idx, (px, py, pw, ph) in enumerate(panels):
        a = p if idx == 0 else prog(t, 1.5, 2.2)
        if not a: continue
        rrect(ctx, px, py, pw, ph, 30 * U); rgba(ctx, NAVY, 0.88 * a); ctx.fill()
        cx2, cy2 = px + pw / 2, py + ph * 0.52
        rr = ((t * 1.2) % 1.0)
        if idx == 0:
            for m in range(8):
                an = m / 8 * 2 * math.pi
                arrow(ctx, cx2 + 40 * U * math.cos(an), cy2 + 40 * U * math.sin(an), cx2 + (90 + 50 * rr) * U * math.cos(an), cy2 + (90 + 50 * rr) * U * math.sin(an), BLUE, a * (1 - rr * 0.6))
            molecule(ctx, cx2, cy2, 1.5 * U, a)
            text(ctx, "AIR MOLECULE", cx2, py + 45 * U, 38 * U, WHITE, a)
            text(ctx, "scatters mostly blue", cx2, py + ph - 40 * U, 32 * U, BLUE, a, False)
        else:
            for m in range(12):
                an = m / 12 * 2 * math.pi
                c = RAINBOW[m % 6]
                arrow(ctx, cx2 + 85 * U * math.cos(an), cy2 + 85 * U * math.sin(an), cx2 + (130 + 40 * rr) * U * math.cos(an), cy2 + (130 + 40 * rr) * U * math.sin(an), c, a * (1 - rr * 0.6))
            glow(ctx, cx2, cy2, 120 * U, WHITE, 0.5 * a)
            circle(ctx, cx2, cy2, 72 * U, (0.75, 0.88, 1.0), a)
            circle(ctx, cx2 - 22 * U, cy2 - 24 * U, 18 * U, WHITE, 0.8 * a)
            text(ctx, "WATER DROPLET", cx2, py + 45 * U, 38 * U, WHITE, a)
            text(ctx, "scatters all colors → white", cx2, py + ph - 40 * U, 32 * U, GOLD, a, False)

def rover(ctx, x, y, s, c):
    rgba(ctx, c)
    rrect(ctx, x - 90 * s, y - 95 * s, 180 * s, 50 * s, 8 * s); ctx.fill()
    ctx.rectangle(x - 110 * s, y - 108 * s, 220 * s, 12 * s); ctx.fill()
    ctx.rectangle(x + 50 * s, y - 210 * s, 12 * s, 120 * s); ctx.fill()
    rrect(ctx, x + 30 * s, y - 240 * s, 60 * s, 34 * s, 6 * s); ctx.fill()
    ctx.set_line_width(8 * s); rgba(ctx, c)
    for wx in (-75, 0, 75):
        ctx.move_to(x + wx * s, y - 45 * s); ctx.line_to(x + wx * s, y - 22 * s); ctx.stroke()
        circle(ctx, x + wx * s, y - 22 * s, 22 * s, c)

def sc_mars(ctx, t, d):
    k = prog(t, d * 0.45, d * 0.62)
    hz = H * 0.66 if not VERT else 1150 * U
    g = cairo.LinearGradient(0, 0, 0, hz)
    g.add_color_stop_rgb(0, *mix((0.72, 0.55, 0.40), (0.10, 0.08, 0.14), k))
    g.add_color_stop_rgb(1, *mix((0.93, 0.78, 0.58), (0.30, 0.25, 0.30), k))
    ctx.set_source(g); ctx.rectangle(0, 0, W, H); ctx.fill()
    stars(ctx, t, 0.5 * k)
    # small Martian sun
    sx = W * 0.62 if not VERT else W * 0.6
    sy = mix((H * 0.22 if not VERT else 480 * U, 0, 0), (hz - 30 * U, 0, 0), k)[0]
    if k > 0: glow(ctx, sx, sy, 330 * U, (0.45, 0.65, 1.0), 0.75 * k)
    glow(ctx, sx, sy, 120 * U, (1, 0.95, 0.85), 0.5)
    circle(ctx, sx, sy, 32 * U, mix((1, 0.97, 0.88), (0.85, 0.92, 1.0), k))
    # terrain
    hills(ctx, hz, mix((0.70, 0.36, 0.22), (0.30, 0.15, 0.10), k), 1, 1.0)
    hills(ctx, hz + 70 * U, mix((0.55, 0.26, 0.16), (0.22, 0.10, 0.07), k), 1, 3.0)
    random.seed(8)
    for j in range(14):
        rx = random.random() * W; ry = hz + random.uniform(100, 400) * U
        ctx.save(); ctx.translate(rx, ry); ctx.scale(random.uniform(20, 45) * U, random.uniform(10, 18) * U)
        ctx.arc(0, 0, 1, 0, 6.3); ctx.restore(); rgba(ctx, (0.25, 0.10, 0.06), 0.6); ctx.fill()
    rover(ctx, W * 0.25 if not VERT else W * 0.3, hz + 120 * U, 1.0 * U, mix((0.20, 0.12, 0.10), (0.05, 0.04, 0.06), k))
    ty = H * 0.13 if not VERT else 320 * U
    text(ctx, "MARS · DAYTIME", CX, ty, 60 * U, NAVY, prog(t, 0.3, 0.9) * (1 - k))
    if k: text(ctx, "MARS · BLUE SUNSET", CX, ty, 60 * U, (0.65, 0.82, 1.0), k)
    chip(ctx, "OTHER WORLDS, OTHER SKIES", t)

def sc_space(ctx, t, d):
    ctx.set_source_rgb(0.0, 0.0, 0.02); ctx.paint(); stars(ctx, t, 0.8)
    ly = H * 0.62 if not VERT else 1100 * U
    R = W * 1.4
    pcx, pcy = CX, ly + R
    glow(ctx, pcx, pcy, R + 90 * U, (0.35, 0.65, 1.0), 0.0)
    circle(ctx, pcx, pcy, R + 26 * U, (0.35, 0.65, 1.0), 0.55)
    circle(ctx, pcx, pcy, R + 12 * U, (0.55, 0.80, 1.0), 0.6)
    circle(ctx, pcx, pcy, R, SEA_D)
    ctx.save(); ctx.arc(pcx, pcy, R, 0, 2 * math.pi); ctx.clip()
    for i in range(5):
        x = (W * i * 0.3 - t * 20 * U) % (W * 1.5) - W * 0.2
        ctx.save(); ctx.translate(x, ly + 120 * U); ctx.scale(200 * U, 50 * U); ctx.arc(0, 0, 1, 0, 6.3); ctx.restore(); rgba(ctx, EARTH_G, 0.8); ctx.fill()
        cloud(ctx, x + 250 * U, ly + 60 * U, 0.6 * U, WHITE, 0.7)
    ctx.restore()
    sx, sy = (W * 0.82, H * 0.25) if not VERT else (W * 0.75, 520 * U)
    glow(ctx, sx, sy, 200 * U, WHITE, 0.6); circle(ctx, sx, sy, 45 * U, (1, 0.98, 0.9))
    # space station silhouette
    stx, sty = (W * 0.36, H * 0.36) if not VERT else (W * 0.35, 780 * U)
    stx += t * 8 * U
    rgba(ctx, (0.75, 0.78, 0.85)); ctx.rectangle(stx - 60 * U, sty - 6 * U, 120 * U, 12 * U); ctx.fill()
    rrect(ctx, stx - 22 * U, sty - 20 * U, 44 * U, 40 * U, 8 * U); ctx.fill()
    for sgn in (-1, 1):
        for k in (0, 1):
            rgba(ctx, (0.85, 0.65, 0.25)); ctx.rectangle(stx + sgn * (70 + k * 50) * U - 20 * U, sty - 55 * U, 40 * U, 110 * U); ctx.fill()
    a = prog(t, 0.6, 1.3)
    ty = H * 0.12 if not VERT else 330 * U
    text(ctx, "NO AIR = BLACK SKY", CX, ty, 64 * U, WHITE, a)
    a2 = prog(t, 2.0, 2.6)
    tx = W * 0.22 if not VERT else W * 0.3
    arrow(ctx, tx, ly - 110 * U, tx + 20 * U, ly - 30 * U, (0.55, 0.8, 1.0), a2)
    text(ctx, "thin blue atmosphere", tx, ly - 140 * U, 32 * U, (0.55, 0.8, 1.0), a2, False)

def sc_outro(ctx, t, d):
    sky(ctx, 0.35 + 0.65 * prog(t, 0, d), H)
    stars(ctx, t, 0.3 * prog(t, d * 0.5, d))
    yo = -80 * U if not VERT else -200 * U
    glow(ctx, CX, CY + yo - 210 * U, 160 * U, (1, 0.8, 0.4), 0.6)
    circle(ctx, CX, CY + yo - 210 * U, 60 * U, (1, 0.85, 0.5))
    text(ctx, "FACTORA", CX, CY + yo, 140 * U, WHITE, prog(t, 0, 0.6))
    text(ctx, "fascinating facts, explained", CX, CY + yo + 100 * U, 38 * U, GOLD, prog(t, 0.4, 1.0), False)
    k = prog(t, d * 0.55, d * 0.65)
    if k:
        bw, bh = 520 * U, 110 * U
        pop = 1 + 0.05 * math.sin(t * 6)
        ctx.save(); ctx.translate(CX, CY + yo + 260 * U); ctx.scale(pop * k, pop * k)
        rrect(ctx, -bw / 2, -bh / 2, bw, bh, 22 * U); rgba(ctx, (0.85, 0.12, 0.12)); ctx.fill()
        text(ctx, "SUBSCRIBE", 0, 0, 52 * U, WHITE)
        ctx.restore()
    q = prog(t, d * 0.3, d * 0.4)
    if q and k < 1: text(ctx, "Did you already know?", CX, CY + yo + 260 * U, 44 * U, WHITE, q * (1 - k))

SHORT_SCENES = ["hook", "waves", "scatter", "outro"]

SCENES = dict(hook=sc_hook, white=sc_white, waves=sc_waves, scatter=sc_scatter, violet=sc_violet, sunset=sc_sunset,
              clouds=sc_clouds, mars=sc_mars, space=sc_space, outro=sc_outro)

def thumbnail(c):
    """1280x720 thumbnail (render.py thumb mode)."""
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, .08, .11, .26); g.add_color_stop_rgb(1, .02, .03, .08); c.set_source(g); c.paint()
    # right half: sky going from blue to sunset
    c.save(); c.move_to(830, 0); c.line_to(W, 0); c.line_to(W, H); c.line_to(770, H); c.close_path(); c.clip()
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgb(0, .14, .40, .84); g.add_color_stop_rgb(.45, .45, .70, .95); g.add_color_stop_rgb(.72, .98, .55, .30); g.add_color_stop_rgb(1, 1, .75, .3)
    c.set_source(g); c.paint()
    rg = cairo.RadialGradient(1050, 560, 0, 1050, 560, 300); rg.add_color_stop_rgba(0, 1, .8, .4, .9); rg.add_color_stop_rgba(1, 1, .6, .2, 0)
    c.set_source(rg); c.arc(1050, 560, 300, 0, 6.3); c.fill()
    c.arc(1050, 575, 85, 0, 6.3); c.set_source_rgb(1, .9, .55); c.fill()
    for (x, y, s) in [(1000, 140, 1.0), (1190, 270, 0.75)]:
        for dx, dy, r in [(-60, 10, 45), (-15, -20, 60), (40, -5, 50), (80, 15, 38), (10, 20, 45)]:
            c.arc(x + dx * s, y + dy * s, r * s, 0, 6.3); c.set_source_rgba(1, 1, 1, .92); c.fill()
    c.move_to(740, H)
    for i in range(31):
        x = 740 + 540 * i / 30
        c.line_to(x, 620 - 30 * math.sin(i * 0.5) - 15 * math.sin(i * 1.4))
    c.line_to(W, H); c.close_path(); c.set_source_rgb(.12, .06, .12); c.fill()
    c.restore()
    thumb_text(c, "WHY IS THE SKY", "BLUE?", "AND SUNSETS ORANGE")
