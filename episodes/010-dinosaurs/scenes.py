# Episode 010 - "Why did the dinosaurs disappear?"
# Executed inside engine/render.py: helpers (W, H, U, CX, CY, VERT, colors, vgrad, circle, glow,
# text, rrect, stars, sun, chip, prog, ease, mix...) are available.

ROCK = (0.42, 0.30, 0.22)
FERN = (0.10, 0.30, 0.22)
LAVA = (1.0, 0.42, 0.12)
DUSK = (0.55, 0.25, 0.30)

def smooth(ctx, pts, closed=True):
    """Closed Catmull-Rom curve through pts."""
    n = len(pts)
    ctx.move_to(*pts[0])
    rng = range(n) if closed else range(n - 1)
    for i in rng:
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
        if not closed:
            p0 = pts[max(i - 1, 0)]; p3 = pts[min(i + 2, n - 1)]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        ctx.curve_to(c1[0], c1[1], c2[0], c2[1], p2[0], p2[1])
    if closed: ctx.close_path()

THERO = [(-1.35, -0.62), (-0.7, -0.76), (-0.15, -0.86), (0.25, -0.82), (0.42, -0.92), (0.55, -1.06), (0.78, -1.08),
         (0.98, -1.0), (1.0, -0.94), (0.86, -0.9), (0.66, -0.86), (0.5, -0.7), (0.32, -0.52), (0.2, -0.42),
         (0.2, -0.24), (0.27, -0.04), (0.36, 0.0), (0.12, 0.0), (0.08, -0.22), (0.0, -0.4), (-0.25, -0.46),
         (-0.7, -0.6)]
SAURO = [(-1.75, -0.5), (-1.1, -0.72), (-0.45, -0.98), (0.15, -0.95), (0.45, -1.15), (0.66, -1.6), (0.86, -1.9),
         (1.04, -1.92), (1.1, -1.84), (0.96, -1.8), (0.8, -1.6), (0.64, -1.1), (0.5, -0.76), (0.44, -0.4),
         (0.46, 0.0), (0.24, 0.0), (0.2, -0.42), (-0.25, -0.46), (-0.32, -0.3), (-0.3, 0.0), (-0.56, 0.0),
         (-0.6, -0.5), (-1.0, -0.56)]

def dino(ctx, kind, x, y, s, c, a=1.0, flip=False, t=0.0, eye=None):
    pts = THERO if kind == "t" else SAURO
    ctx.save(); ctx.translate(x, y); ctx.scale(-s if flip else s, s)
    if kind == "t":   # far leg + small arm
        rgba(ctx, mix(c, (0, 0, 0), 0.35), a)
        smooth(ctx, [(-0.1, -0.45), (0.0, -0.3), (-0.02, -0.04), (0.06, 0.0), (-0.12, 0.0), (-0.16, -0.3), (-0.25, -0.45)]); ctx.fill()
        ctx.set_line_width(0.045); ctx.set_line_cap(cairo.LINE_CAP_ROUND); rgba(ctx, c, a)
        ctx.move_to(0.5, -0.68); ctx.line_to(0.6, -0.6); ctx.line_to(0.64, -0.64); ctx.stroke()
    rgba(ctx, c, a); smooth(ctx, pts); ctx.fill()
    if eye:
        ex, ey = (0.78, -1.0) if kind == "t" else (0.98, -1.86)
        circle(ctx, ex, ey, 0.035, eye, a)
    ctx.restore()

def bird(ctx, x, y, s, c, a=1.0, flap=0.0):
    """Simple side-view perched bird (pigeon-like), facing left."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rgba(ctx, c, a)
    smooth(ctx, [(-0.55, -0.95), (-0.35, -1.12), (-0.15, -1.05), (-0.05, -0.8), (0.25, -0.72), (0.75, -0.62),
                 (1.05, -0.62), (0.75, -0.45), (0.35, -0.28), (-0.1, -0.3), (-0.4, -0.55), (-0.5, -0.8)]); ctx.fill()
    ctx.move_to(-0.55, -1.0); ctx.line_to(-0.75, -0.94); ctx.line_to(-0.53, -0.9); ctx.close_path(); rgba(ctx, GOLD, a); ctx.fill()
    rgba(ctx, mix(c, (0, 0, 0), 0.3), a)
    smooth(ctx, [(-0.05, -0.75), (0.45, -0.95 - 0.25 * flap), (0.85, -0.75), (0.4, -0.55)]); ctx.fill()
    ctx.set_line_width(0.06); rgba(ctx, CORAL, a)
    ctx.move_to(0.05, -0.3); ctx.line_to(0.0, 0.0); ctx.move_to(0.2, -0.3); ctx.line_to(0.2, 0.0); ctx.stroke()
    circle(ctx, -0.36, -0.98, 0.05, WHITE, a); circle(ctx, -0.37, -0.98, 0.025, NAVY, a)
    ctx.restore()

def fern(ctx, x, y, s, c, a=1.0, sway=0.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rgba(ctx, c, a); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    for i in range(7):
        ang = -math.pi / 2 + (i - 3) * 0.32 + sway
        ln = 1.0 - abs(i - 3) * 0.12
        ex, ey = math.cos(ang) * ln, math.sin(ang) * ln
        ctx.set_line_width(0.06); ctx.move_to(0, 0); ctx.curve_to(ex * 0.4, ey * 0.6, ex * 0.8, ey * 0.95, ex, ey); ctx.stroke()
        for j in range(1, 6):
            k = j / 6; px, py = ex * k, ey * k + 0.08 * k * k
            nx, ny = -math.sin(ang) * 0.14 * (1 - k * 0.5), math.cos(ang) * 0.14 * (1 - k * 0.5)
            ctx.set_line_width(0.035); ctx.move_to(px - nx, py - ny); ctx.line_to(px + nx, py + ny); ctx.stroke()
    ctx.restore()

def hills(ctx, ybase, amp, c, a=1.0, seed=0.0):
    rgba(ctx, c, a); ctx.move_to(0, H)
    for i in range(41):
        x = W * i / 40
        ctx.line_to(x, ybase - amp * (0.5 + 0.5 * math.sin(i * 0.37 + seed)) - amp * 0.3 * math.sin(i * 1.1 + seed * 2))
    ctx.line_to(W, H); ctx.close_path(); ctx.fill()

def asteroid(ctx, x, y, r, t, a=1.0, trail=0.0, ang=-0.6):
    if trail > 0:   # glowing trail toward upper-left by default
        dx, dy = -math.cos(ang), math.sin(ang)
        g = cairo.LinearGradient(x, y, x + dx * r * 14 * trail, y + dy * r * 14 * trail)
        g.add_color_stop_rgba(0, 1, 0.75, 0.4, 0.85 * a); g.add_color_stop_rgba(1, 1, 0.5, 0.2, 0)
        ctx.set_source(g); nx, ny = -dy, dx
        ctx.move_to(x + nx * r, y + ny * r); ctx.line_to(x + dx * r * 14 * trail, y + dy * r * 14 * trail)
        ctx.line_to(x - nx * r, y - ny * r); ctx.close_path(); ctx.fill()
        glow(ctx, x, y, r * 3, (1, 0.6, 0.3), 0.6 * a)
    pts = [(math.cos(i / 9 * 6.283) * r * (0.85 + 0.15 * math.sin(i * 2.7)), math.sin(i / 9 * 6.283) * r * (0.85 + 0.15 * math.cos(i * 1.9))) for i in range(9)]
    ctx.save(); ctx.translate(x, y); ctx.rotate(t * 0.5)
    rgba(ctx, (0.45, 0.38, 0.34), a); smooth(ctx, pts); ctx.fill()
    for (cx_, cy_, cr) in [(-0.3, -0.2, 0.22), (0.3, 0.25, 0.16), (0.25, -0.35, 0.1)]:
        circle(ctx, cx_ * r, cy_ * r, cr * r, (0.33, 0.27, 0.25), a)
    ctx.restore()

def prehistoric(ctx, t, dark=0.0, herd=True):
    top = mix((0.10, 0.10, 0.26), (0.03, 0.03, 0.06), dark)
    bot = mix(DUSK, (0.08, 0.06, 0.07), dark)
    vgrad(ctx, top, bot)
    stars(ctx, t, 0.35 * (1 - dark))
    hy = H * (0.70 if not VERT else 0.66)
    hills(ctx, hy, 90 * U, mix((0.16, 0.12, 0.2), (0.05, 0.04, 0.05), dark), 1, 1.0)
    hills(ctx, hy + 70 * U, 50 * U, mix((0.07, 0.10, 0.12), (0.03, 0.03, 0.04), dark), 1, 3.0)
    sil = mix((0.02, 0.04, 0.06), (0.01, 0.01, 0.02), dark)
    gy = hy + 110 * U
    if herd:
        if VERT:
            dino(ctx, "s", W * 0.66, gy, 200 * U, sil)
            dino(ctx, "t", W * 0.22, gy + 10 * U, 150 * U, sil)
        else:
            dino(ctx, "s", W * 0.66, gy, 230 * U, sil)
            dino(ctx, "s", W * 0.85, gy + 5 * U, 140 * U, sil)
            dino(ctx, "t", W * 0.28, gy + 10 * U, 170 * U, sil)
    for i, fx in enumerate([0.05, 0.42, 0.95] if not VERT else [0.06, 0.94]):
        fern(ctx, W * fx, gy + 20 * U, 150 * U, sil, 1, 0.05 * math.sin(t + i))
    rgba(ctx, sil); ctx.rectangle(0, gy, W, H - gy); ctx.fill()
    return gy

# ---------- scenes ----------
def sc_hook(ctx, t, d):
    k = prog(t, 2.0, 6.5)
    gy = prehistoric(ctx, t, 0.0)
    ax = W * 0.78 - k * W * 0.18 if not VERT else W * 0.72 - k * W * 0.12
    ay = H * 0.12 + k * H * 0.12 if VERT else H * 0.08 + k * H * 0.06
    asteroid(ctx, ax, ay, (18 + 30 * k) * U, t, prog(t, 1.2, 2.2), 0.4 + 0.6 * k)
    # sky turns orange when it approaches
    glow(ctx, ax, ay, 500 * U * k, (1, 0.5, 0.2), 0.25 * k)
    q = prog(t, d - 4.5, d - 3.5)
    if q:
        if VERT:
            text(ctx, "WHY DID THE", CX, H * 0.40, 84 * U, WHITE, q)
            text(ctx, "DINOSAURS VANISH?", CX, H * 0.40 + 100 * U, 84 * U, GOLD, q)
        else:
            text(ctx, "WHY DID THE DINOSAURS VANISH?", CX, H * 0.30, 84 * U, WHITE, q)

def sc_reign(ctx, t, d):
    vgrad(ctx, NAVY2, NAVY); stars(ctx, t, 0.5)
    x0, x1 = (W * 0.1, W * 0.9)
    y = H * 0.5 if not VERT else H * 0.45
    total = 230.0
    def X(mya): return x0 + (x1 - x0) * (1 - mya / total)
    p = prog(t, 0.3, 3.0)
    # base bar
    rrect(ctx, x0, y - 18 * U, (x1 - x0), 36 * U, 18 * U); rgba(ctx, WHITE, 0.15); ctx.fill()
    xa, xb = X(230), X(230 - 164 * p)
    rrect(ctx, xa, y - 18 * U, max(36 * U, xb - xa), 36 * U, 18 * U); rgba(ctx, GOLD, 0.95); ctx.fill()
    sz = 30 * U if not VERT else 34 * U
    text(ctx, "230 MILLION", X(230), y + 75 * U, sz, WHITE, 0.85, False, "l")
    text(ctx, "YEARS AGO", X(230), y + 75 * U + sz * 1.2, sz, WHITE, 0.85, False, "l")
    text(ctx, "TODAY", X(0), y + 75 * U, sz, WHITE, 0.85, False, "r")
    lab = prog(t, 2.5, 3.5)
    if lab:
        text(ctx, "DINOSAURS", (X(230) + X(66)) / 2, y - 160 * U, 64 * U, GOLD, lab)
        text(ctx, "~165 million years", (X(230) + X(66)) / 2, y - 90 * U, 40 * U, WHITE, lab, False)
        # small walking dino on bar
        dx = X(230) + (X(66) - X(230)) * (0.5 + 0.4 * math.sin(t * 0.4))
        dino(ctx, "t", dx, y - 18 * U, 45 * U, GOLD, lab)
    h = prog(t, 5.5, 6.5)
    if h:
        xh = X(0.3)
        rgba(ctx, CORAL, h); ctx.rectangle(xh - 3 * U, y - 26 * U, 6 * U, 52 * U); ctx.fill()
        ctx.set_line_width(3 * U); ctx.move_to(xh, y + 30 * U); ctx.line_to(xh, y + 50 * U); ctx.move_to(xh - 30 * U, y + 125 * U); ctx.line_to(xh - 80 * U, y + 180 * U); ctx.stroke()
        text(ctx, "HUMANS", xh - 80 * U, y + 215 * U, 46 * U, CORAL, h, True, "r")
        text(ctx, "~300,000 years", xh - 80 * U, y + 265 * U, 34 * U, WHITE, h, False, "r")
    chip(ctx, "THE AGE OF DINOSAURS", t)

def sc_clue(ctx, t, d):
    vgrad(ctx, NAVY2, NAVY)
    # rock strata, layered cliff
    top = H * (0.18 if not VERT else 0.2); bot = H * (0.78 if not VERT else 0.68)
    cols = [(0.55, 0.40, 0.28), (0.48, 0.34, 0.24), (0.60, 0.46, 0.32), (0.44, 0.31, 0.22), (0.52, 0.38, 0.27)]
    n = 9; lh = (bot - top) / n
    for i in range(n):
        y0 = top + i * lh
        rgba(ctx, cols[i % 5]); ctx.move_to(0, y0)
        for j in range(21): ctx.line_to(W * j / 20, y0 + 8 * U * math.sin(j * 0.9 + i))
        ctx.line_to(W, y0 + lh + 10 * U); ctx.line_to(0, y0 + lh + 10 * U); ctx.close_path(); ctx.fill()
    # labels: older / younger
    ly = top + lh * 4.55
    hl = prog(t, 2.0, 3.5)
    rgba(ctx, (0.92, 0.88, 0.75)); ctx.move_to(0, ly)
    for j in range(21): ctx.line_to(W * j / 20, ly + 8 * U * math.sin(j * 0.9 + 4.5))
    ctx.line_to(W, ly + 16 * U); ctx.line_to(0, ly + 16 * U); ctx.close_path(); ctx.fill()
    if hl:
        ctx.set_line_width(5 * U); rgba(ctx, GOLD, hl)
        ctx.move_to(0, ly - 6 * U)
        for j in range(21): ctx.line_to(W * j / 20, ly - 6 * U + 8 * U * math.sin(j * 0.9 + 4.5))
        ctx.stroke()
        ctx.move_to(0, ly + 22 * U)
        for j in range(21): ctx.line_to(W * j / 20, ly + 22 * U + 8 * U * math.sin(j * 0.9 + 4.5))
        ctx.stroke()
    # fossils in lower layers, none above
    for (fx, fy) in ([(0.18, 6.5), (0.62, 7.4), (0.85, 5.6)] if not VERT else [(0.2, 6.5), (0.75, 7.3)]):
        dino(ctx, "t", W * fx, top + lh * fy, 55 * U, (0.75, 0.68, 0.55), 0.7)
    # magnifier
    m = prog(t, 6.0, 7.2)
    if m:
        mx, my, mr = (W * 0.66, ly, 190 * U) if not VERT else (W * 0.5, ly, 200 * U)
        ctx.save(); ctx.new_path(); ctx.arc(mx, my, mr * m, 0, 2 * math.pi); ctx.clip()
        rgba(ctx, (0.94, 0.9, 0.78)); ctx.paint()
        random.seed(4)
        for i in range(28):
            px = mx + random.uniform(-1, 1) * mr; py = my + random.uniform(-1, 1) * mr
            circle(ctx, px, py, 22 * U, (0.75, 0.75, 0.82))
            circle(ctx, px - 5 * U, py - 5 * U, 7 * U, WHITE, 0.6)
        for (ox, oy) in [(-0.35, -0.2), (0.3, 0.35), (0.1, -0.45), (-0.2, 0.45)]:
            glow(ctx, mx + ox * mr, my + oy * mr, 55 * U, GOLD, 0.8)
            circle(ctx, mx + ox * mr, my + oy * mr, 30 * U, GOLD)
            text(ctx, "Ir", mx + ox * mr, my + oy * mr, 30 * U, NAVY)
        ctx.restore()
        ctx.new_path(); ctx.set_line_width(14 * U); rgba(ctx, NAVY, m); ctx.arc(mx, my, mr * m, 0, 2 * math.pi); ctx.stroke()
        ctx.set_line_width(26 * U); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.move_to(mx + mr * 0.72 * m, my + mr * 0.72 * m); ctx.line_to(mx + mr * 1.15 * m, my + mr * 1.15 * m); ctx.stroke()
        tx = mx if VERT else W * 0.28
        ty = top - 0 if VERT else ly - 120 * U
        bw = 520 * U
        rrect(ctx, tx - bw / 2, ty - 45 * U, bw, 90 * U, 20 * U); rgba(ctx, NAVY, 0.85 * m); ctx.fill()
        text(ctx, "IRIDIUM-RICH CLAY", tx, ty, 44 * U, GOLD, m)
    chip(ctx, "CLUE · A STRANGE LAYER", t)

def globe_region(ctx, x, y, r, t, a=1.0):
    glow(ctx, x, y, r * 1.35, (0.4, 0.7, 1.0), 0.3 * a)
    circle(ctx, x, y, r, SEA, a)
    ctx.save(); ctx.arc(x, y, r, 0, 2 * math.pi); ctx.clip()
    rgba(ctx, EARTH_G, a)
    # stylized North America + peninsula (simple blobs)
    smooth(ctx, [(x - 0.9 * r, y - 0.6 * r), (x - 0.2 * r, y - 0.9 * r), (x + 0.5 * r, y - 0.7 * r), (x + 0.45 * r, y - 0.25 * r),
                 (x + 0.1 * r, y - 0.05 * r), (x - 0.1 * r, y + 0.25 * r), (x - 0.25 * r, y + 0.45 * r), (x - 0.5 * r, y + 0.2 * r), (x - 0.8 * r, y - 0.1 * r)]); ctx.fill()
    smooth(ctx, [(x + 0.02 * r, y + 0.2 * r), (x + 0.2 * r, y + 0.12 * r), (x + 0.24 * r, y + 0.3 * r), (x + 0.05 * r, y + 0.38 * r)]); ctx.fill()
    smooth(ctx, [(x + 0.1 * r, y + 0.65 * r), (x + 0.5 * r, y + 0.55 * r), (x + 0.75 * r, y + 0.9 * r), (x + 0.3 * r, y + 1.2 * r)]); ctx.fill()
    ctx.restore()
    return x + 0.14 * r, y + 0.24 * r

def sc_impact(ctx, t, d):
    vgrad(ctx, NAVY2, NAVY); stars(ctx, t, 0.6)
    ph2 = prog(t, d * 0.62, d * 0.68)
    a1 = 1 - ph2
    if a1 > 0:
        gx, gy = (W * 0.36, H * 0.46) if not VERT else (CX, H * 0.38)
        px, py = globe_region(ctx, gx, gy, 300 * U, t, a1)
        pin = prog(t, 1.0, 2.0)
        ring = 60 * U * (1 + 0.15 * math.sin(t * 4))
        ctx.set_line_width(6 * U); rgba(ctx, GOLD, pin * a1); ctx.arc(px, py, ring, 0, 2 * math.pi); ctx.stroke()
        circle(ctx, px, py, 12 * U, CORAL, pin * a1)
        lk = prog(t, 4.0, 5.0) * a1
        if lk:
            lx, ly = (W * 0.72, H * 0.36) if not VERT else (CX, H * 0.08 + 40 * U)
            if not VERT:
                ctx.set_line_width(3 * U); rgba(ctx, GOLD, lk); ctx.move_to(px + ring, py); ctx.line_to(lx - 260 * U, ly + 60 * U); ctx.stroke()
            text(ctx, "CHICXULUB", lx, ly if not VERT else H * 0.64, 72 * U, GOLD, lk)
            text(ctx, "crater ≈ 180 km wide", lx, (ly if not VERT else H * 0.64) + 80 * U, 42 * U, WHITE, lk, False)
            text(ctx, "Yucatán Peninsula, Mexico", lx, (ly if not VERT else H * 0.64) + 135 * U, 34 * U, WHITE, 0.7 * lk, False)
    if ph2:
        gy = H * (0.72 if not VERT else 0.64)
        rgba(ctx, (0.12, 0.14, 0.24), ph2); ctx.rectangle(0, gy, W, H - gy); ctx.fill()
        sc_ = 34 * U   # pixels per km
        mx = W * 0.62 if not VERT else W * 0.68
        # Everest 8.8 km
        rgba(ctx, (0.55, 0.6, 0.75), ph2)
        ctx.move_to(mx - 6 * sc_, gy); ctx.line_to(mx - 1.2 * sc_, gy - 6.2 * sc_); ctx.line_to(mx - 0.6 * sc_, gy - 6.0 * sc_)
        ctx.line_to(mx, gy - 8.8 * sc_); ctx.line_to(mx + 2 * sc_, gy - 6.5 * sc_); ctx.line_to(mx + 6 * sc_, gy); ctx.close_path(); ctx.fill()
        rgba(ctx, WHITE, ph2); ctx.move_to(mx - 0.8 * sc_, gy - 7.0 * sc_); ctx.line_to(mx, gy - 8.8 * sc_); ctx.line_to(mx + 1.0 * sc_, gy - 7.2 * sc_)
        ctx.line_to(mx + 0.3 * sc_, gy - 7.5 * sc_); ctx.close_path(); ctx.fill()
        ax = W * 0.3 if not VERT else W * 0.27
        asteroid(ctx, ax, gy - 5 * sc_ - 4 * U, 5 * sc_, t * 0.2, ph2)
        lab = 40 * U if not VERT else 38 * U
        text(ctx, "ASTEROID ≈ 10 km", ax, gy - 10 * sc_ - 40 * U, lab, GOLD, ph2)
        text(ctx, "EVEREST ≈ 8.8 km", mx, gy - 8.8 * sc_ - 50 * U, lab, WHITE, ph2)
    chip(ctx, "THE IMPACT SITE", t)

def sc_blast(ctx, t, d):
    vgrad(ctx, (0.25, 0.08, 0.06), (0.06, 0.03, 0.05))
    hy = H * (0.62 if not VERT else 0.55)
    ix = CX
    f = prog(t, 0, 0.6)
    glow(ctx, ix, hy, 900 * U * f, LAVA, 0.55)
    glow(ctx, ix, hy, 350 * U, (1, 0.9, 0.6), 0.8 * (1 - prog(t, 0.5, 3)))
    # shock rings
    for i in range(4):
        rr = ((t * 260 + i * 220) % 900) * U
        ctx.save(); ctx.translate(ix, hy); ctx.scale(1, 0.28)
        ctx.arc(0, 0, rr, 0, 2 * math.pi); ctx.restore()
        ctx.set_line_width(6 * U); rgba(ctx, (1, 0.8, 0.5), 0.6 * (1 - rr / (900 * U))); ctx.stroke()
    # ground
    rgba(ctx, (0.08, 0.04, 0.04)); ctx.rectangle(0, hy, W, H - hy); ctx.fill()
    # fire silhouettes along horizon
    for i in range(14):
        x = W * (i + 0.5) / 14
        fh = (60 + 40 * math.sin(i * 1.7 + t * 6)) * U
        rgba(ctx, LAVA, 0.9)
        ctx.move_to(x - 30 * U, hy); ctx.curve_to(x - 20 * U, hy - fh * 0.6, x, hy - fh * 0.8, x + 5 * U * math.sin(t * 8 + i), hy - fh)
        ctx.curve_to(x + 10 * U, hy - fh * 0.6, x + 25 * U, hy - fh * 0.4, x + 30 * U, hy); ctx.close_path(); ctx.fill()
    # three icons
    labels = ["TSUNAMIS", "EARTHQUAKES", "WILDFIRES"]
    for i, lab in enumerate(labels):
        k = prog(t, 0.8 + i * 1.0, 1.6 + i * 1.0)
        if not k: continue
        if VERT: bx, by = CX, H * 0.12 + i * 120 * U + 140 * U
        else: bx, by = W * (0.22 + 0.28 * i), H * 0.22
        bw = 420 * U if not VERT else 520 * U
        rrect(ctx, bx - bw / 2, by - 45 * U, bw, 90 * U, 45 * U); rgba(ctx, NAVY, 0.85 * k); ctx.fill()
        ctx.set_line_width(3 * U); rgba(ctx, GOLD, k); rrect(ctx, bx - bw / 2, by - 45 * U, bw, 90 * U, 45 * U); ctx.stroke()
        text(ctx, lab, bx, by, 44 * U, GOLD, k)
    w = prog(t, 0.5, 4.5)
    # tsunami wave rolling at right (horizontal) / bottom-left (vertical)
    wx = W * (1.05 - 0.25 * w) if not VERT else W * (1.05 - 0.3 * w)
    rgba(ctx, SEA, 0.9); ctx.move_to(wx, hy)
    ctx.curve_to(wx - 40 * U, hy - 140 * U, wx + 60 * U, hy - 220 * U, wx + 160 * U, hy - 160 * U)
    ctx.curve_to(wx + 100 * U, hy - 160 * U, wx + 100 * U, hy - 90 * U, wx + 180 * U, hy - 60 * U)
    ctx.line_to(W + 40 * U, hy - 60 * U); ctx.line_to(W + 40 * U, hy); ctx.close_path(); ctx.fill()

def sc_winter(ctx, t, d):
    k = prog(t, 0.5, d * 0.7)
    vgrad(ctx, mix((0.3, 0.32, 0.45), (0.06, 0.06, 0.09), k), mix((0.55, 0.45, 0.4), (0.12, 0.12, 0.15), k))
    sx, sy = (W * 0.7, H * 0.2) if not VERT else (W * 0.7, H * 0.16)
    sun(ctx, sx, sy, 70 * U, t, 1 - 0.85 * k)
    # dust clouds drifting in
    random.seed(9)
    for i in range(26):
        cx_ = (random.random() * 1.4 - 0.2) * W + t * random.uniform(10, 40) * U
        cy_ = random.uniform(0.0, 0.42) * H
        rr = random.uniform(90, 200) * U
        circle(ctx, cx_, cy_, rr, mix((0.35, 0.3, 0.3), (0.14, 0.13, 0.15), k), 0.75 * prog(t, i * 0.12, i * 0.12 + 1.2))
    gy = H * (0.70 if not VERT else 0.64)
    hills(ctx, gy, 60 * U, mix((0.2, 0.32, 0.22), (0.25, 0.27, 0.3), k), 1, 2.0)
    rgba(ctx, mix((0.12, 0.22, 0.15), (0.18, 0.2, 0.22), k)); ctx.rectangle(0, gy + 40 * U, W, H); ctx.fill()
    # ferns wilting
    for i, fx in enumerate([0.12, 0.3, 0.5, 0.88] if not VERT else [0.12, 0.88]):
        fern(ctx, W * fx, gy + 50 * U, 130 * U * (1 - 0.35 * k), mix(EARTH_G, (0.38, 0.33, 0.25), k), 1, 0.4 * k * (1 if i % 2 else -1))
    # thermometer
    tx, ty, th = (W * 0.84, H * 0.36, 300 * U) if not VERT else (W * 0.84, H * 0.26, 260 * U)
    rrect(ctx, tx - 22 * U, ty - th / 2, 44 * U, th, 22 * U); rgba(ctx, WHITE, 0.9); ctx.fill()
    circle(ctx, tx, ty + th / 2 + 10 * U, 40 * U, WHITE, 0.9)
    lvl = th * (0.85 - 0.6 * k)
    col = mix(CORAL, (0.4, 0.7, 1.0), k)
    rrect(ctx, tx - 12 * U, ty + th / 2 - lvl, 24 * U, lvl + 10 * U, 12 * U); rgba(ctx, col); ctx.fill()
    circle(ctx, tx, ty + th / 2 + 10 * U, 30 * U, col)
    lab = prog(t, d * 0.55, d * 0.7)
    if lab:
        yy = H * 0.45 if not VERT else H * 0.5
        text(ctx, "IMPACT WINTER", CX if VERT else W * 0.42, yy, 86 * U, WHITE, lab)
        text(ctx, "less sunlight · colder planet", CX if VERT else W * 0.42, yy + 80 * U, 38 * U, GOLD, lab, False)

def sc_food(ctx, t, d):
    vgrad(ctx, NAVY2, NAVY); stars(ctx, t, 0.4)
    ph2 = prog(t, d * 0.62, d * 0.7)
    a1 = 1 - ph2
    if a1:
        if VERT: pos = [(CX, H * 0.12 + 40 * U), (CX, H * 0.28 + 20 * U), (CX, H * 0.44), (CX, H * 0.6 - 20 * U)]
        else: pos = [(W * 0.14, H * 0.45), (W * 0.38, H * 0.45), (W * 0.62, H * 0.45), (W * 0.86, H * 0.45)]
        fades = [prog(t, 1.0, 2.0) * 0.8, prog(t, 1.5, 3.0), prog(t, 3.5, 5.0), prog(t, 5.0, 6.5)]
        s = 1.0 if not VERT else 0.8
        for i in range(3):
            (x1_, y1_), (x2_, y2_) = pos[i], pos[i + 1]
            ctx.set_line_width(5 * U); rgba(ctx, GOLD, 0.7 * a1 * (1 - fades[i + 1] * 0.7))
            if VERT:
                ctx.move_to(x1_, y1_ + 85 * U * s); ctx.line_to(x2_, y2_ - 95 * U * s); ctx.stroke()
                ctx.move_to(x2_ - 14 * U, y2_ - 112 * U * s); ctx.line_to(x2_, y2_ - 95 * U * s); ctx.line_to(x2_ + 14 * U, y2_ - 112 * U * s); ctx.stroke()
            else:
                ctx.move_to(x1_ + 120 * U, y1_); ctx.line_to(x2_ - 120 * U, y2_); ctx.stroke()
                ctx.move_to(x2_ - 136 * U, y2_ - 14 * U); ctx.line_to(x2_ - 120 * U, y2_); ctx.line_to(x2_ - 136 * U, y2_ + 14 * U); ctx.stroke()
        # sun
        x, y = pos[0]; sun(ctx, x, y, 55 * U * s, t, a1 * (1 - fades[0]))
        x, y = pos[1]; fern(ctx, x, y + 80 * U * s, 150 * U * s, mix(EARTH_G, (0.35, 0.3, 0.25), fades[1]), a1 * (1 - 0.6 * fades[1]))
        x, y = pos[2]; dino(ctx, "s", x - 10 * U, y + 80 * U * s, 85 * U * s, mix(GOLD, (0.4, 0.4, 0.45), fades[2]), a1 * (1 - 0.6 * fades[2]))
        x, y = pos[3]; dino(ctx, "t", x, y + 80 * U * s, 130 * U * s, mix(CORAL, (0.4, 0.4, 0.45), fades[3]), a1 * (1 - 0.6 * fades[3]))
        names = ["SUNLIGHT", "PLANTS", "PLANT EATERS", "MEAT EATERS"]
        for i, (x, y) in enumerate(pos):
            if VERT: text(ctx, names[i], x + 230 * U, y, 32 * U, WHITE, 0.85 * a1, True, "c")
            else: text(ctx, names[i], x, y + 140 * U, 32 * U, WHITE, 0.85 * a1)
    if ph2:
        cols, rows = (10, 4) if not VERT else (5, 8)
        cw = 120 * U
        gx0 = CX - (cols - 1) * cw / 2
        gy0 = (H * 0.22) if not VERT else H * 0.2
        n = cols * rows
        for i in range(n):
            r_, c_ = divmod(i, cols)
            x, y = gx0 + c_ * cw, gy0 + r_ * cw
            lost = (i * 7) % 4 != 0   # 3 out of 4
            fade = prog(t, d * 0.72 + (i % 10) * 0.08, d * 0.8 + (i % 10) * 0.08) if lost else 0
            col = mix(GOLD, (0.25, 0.27, 0.35), fade)
            if i % 3 == 0: dino(ctx, "t", x, y + 35 * U, 50 * U, col, ph2)
            elif i % 3 == 1: dino(ctx, "s", x, y + 35 * U, 32 * U, col, ph2)
            else: fern(ctx, x, y + 40 * U, 70 * U, col, ph2)
        yy = gy0 + rows * cw + (20 * U if not VERT else 10 * U)
        text(ctx, "≈ 3 in 4 species lost", CX, yy, 64 * U, CORAL, prog(t, d * 0.8, d * 0.88))
    chip(ctx, "A COLLAPSING FOOD CHAIN", t)

def volcano(ctx, x, y, w, h, t, a=1.0, ph=0.0):
    rgba(ctx, (0.18, 0.12, 0.12), a)
    ctx.move_to(x - w / 2, y); ctx.line_to(x - w * 0.09, y - h); ctx.line_to(x + w * 0.09, y - h); ctx.line_to(x + w / 2, y); ctx.close_path(); ctx.fill()
    # lava streams
    rgba(ctx, LAVA, a)
    for s_ in (-1, 1):
        ctx.move_to(x + w * 0.09 * s_, y - h); ctx.curve_to(x + w * 0.1 * s_, y - h * 0.6, x + w * 0.16 * s_, y - h * 0.3, x + w * 0.24 * s_, y)
        ctx.line_to(x + w * 0.17 * s_, y); ctx.curve_to(x + w * 0.1 * s_, y - h * 0.3, x + w * 0.04 * s_, y - h * 0.6, x + w * 0.03 * s_, y - h); ctx.close_path(); ctx.fill()
    glow(ctx, x, y - h, w * 0.4, LAVA, 0.7 * a)
    # gas plume
    for i in range(7):
        k = ((t * 0.35 + i / 7 + ph) % 1)
        circle(ctx, x + math.sin(i * 2.1 + ph * 5) * w * 0.12 * k + k * w * 0.25, y - h - k * h * 1.3, w * (0.06 + 0.14 * k), (0.45, 0.42, 0.45), a * 0.65 * (1 - k))

def sc_volcano(ctx, t, d):
    vgrad(ctx, (0.12, 0.07, 0.10), (0.30, 0.12, 0.10)); stars(ctx, t, 0.25)
    gy = H * (0.72 if not VERT else 0.66)
    if VERT: vs = [(W * 0.25, 360, 380, 0.0), (W * 0.72, 460, 470, 0.3), (W * 0.5, 280, 260, 0.6)]
    else: vs = [(W * 0.22, 420, 340, 0.0), (W * 0.52, 560, 440, 0.3), (W * 0.8, 380, 300, 0.6), (W * 0.38, 300, 220, 0.8)]
    for i, (x, w, h, ph) in enumerate(vs):
        volcano(ctx, x, gy, w * U, h * U, t, prog(t, 0.3 + i * 0.4, 1.0 + i * 0.4), ph)
    # flood basalt layers (steps)
    for i in range(4):
        rgba(ctx, mix((0.22, 0.14, 0.12), (0.12, 0.08, 0.08), i / 4))
        ctx.rectangle(0, gy + i * 30 * U, W, 30 * U + 2); ctx.fill()
    rgba(ctx, (0.1, 0.06, 0.06)); ctx.rectangle(0, gy + 120 * U, W, H); ctx.fill()
    k = prog(t, 2.5, 3.5)
    yy = H * 0.12 if VERT else H * 0.2
    if VERT: yy = H * 0.14
    xx = W * 0.62 if not VERT else CX
    text(ctx, "DECCAN TRAPS · INDIA", xx, yy if not VERT else H * 0.15, 56 * U, GOLD, k)
    q = prog(t, d * 0.62, d * 0.72)
    if q:
        bw = 640 * U
        by = H * 0.3 if not VERT else H * 0.22
        rrect(ctx, xx - bw / 2, by - 50 * U, bw, 100 * U, 50 * U); rgba(ctx, NAVY, 0.88 * q); ctx.fill()
        text(ctx, "ROLE STILL DEBATED", xx, by, 46 * U, WHITE, q)
    chip(ctx, "A SECOND SUSPECT?", t)

def sc_birds(ctx, t, d):
    vgrad(ctx, NAVY2, NAVY); stars(ctx, t, 0.5)
    gy = H * (0.70 if not VERT else 0.62)
    rgba(ctx, (0.1, 0.13, 0.24)); ctx.rectangle(0, gy, W, H - gy); ctx.fill()
    k1 = prog(t, 0.3, 1.2)
    if VERT:
        tx, ts, bx, bs = W * 0.36, 300 * U, W * 0.78, 120 * U
    else:
        tx, ts, bx, bs = W * 0.3, 360 * U, W * 0.74, 150 * U
    dino(ctx, "t", tx, gy, ts, CORAL, k1, eye=NAVY)
    k2 = prog(t, 3.0, 4.2)
    if k2:
        # dashed family link
        ctx.set_dash([14 * U, 12 * U]); ctx.set_line_width(4 * U); rgba(ctx, GOLD, k2)
        top = gy - ts * 1.25
        ctx.move_to(tx + 0.3 * ts, top); ctx.curve_to(tx + 0.6 * ts, top - 120 * U, bx - 80 * U, top - 120 * U, bx, gy - bs * 1.4); ctx.stroke(); ctx.set_dash([])
        bird(ctx, bx, gy, bs, (0.6, 0.65, 0.78), k2, max(0, math.sin(t * 3)) * 0.0)
    lab = prog(t, 4.5, 5.5)
    if lab:
        y1 = gy + 70 * U
        text(ctx, "T. REX", tx, y1, 46 * U, CORAL, lab)
        text(ctx, "PIGEON", bx, y1, 46 * U, (0.7, 0.75, 0.9), lab)
        if VERT:
            text(ctx, "BIRDS ARE", CX, H * 0.12 + 40 * U, 72 * U, WHITE, prog(t, 6, 7))
            text(ctx, "LIVING DINOSAURS", CX, H * 0.12 + 125 * U, 72 * U, GOLD, prog(t, 6, 7))
        else:
            text(ctx, "BIRDS ARE LIVING DINOSAURS", CX + 120 * U, H * 0.12, 64 * U, GOLD, prog(t, 6, 7))
    chip(ctx, "THE TWIST", t)

def mammal(ctx, x, y, s, c, a=1.0, t=0.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rgba(ctx, c, a)
    smooth(ctx, [(-0.6, -0.15), (-0.45, -0.42), (-0.05, -0.5), (0.3, -0.42), (0.55, -0.3), (0.75, -0.2), (0.6, -0.08), (0.3, -0.02), (-0.4, -0.02)]); ctx.fill()
    circle(ctx, 0.3, -0.48, 0.08, c, a)
    ctx.set_line_width(0.05); ctx.move_to(-0.58, -0.12); ctx.curve_to(-0.9, -0.1, -1.0, -0.3, -1.1, -0.25 + 0.05 * math.sin(t * 3)); ctx.stroke()
    circle(ctx, 0.52, -0.3, 0.04, NAVY, a)
    ctx.set_line_width(0.07); ctx.move_to(-0.3, -0.05); ctx.line_to(-0.32, 0.0); ctx.move_to(0.25, -0.05); ctx.line_to(0.27, 0.0); ctx.stroke()
    ctx.restore()

def sc_mammals(ctx, t, d):
    vgrad(ctx, NAVY2, NAVY); stars(ctx, t, 0.5)
    gy = H * (0.66 if not VERT else 0.56)
    # soil cross-section with burrow
    rgba(ctx, (0.25, 0.18, 0.14)); ctx.rectangle(0, gy, W, H - gy); ctx.fill()
    rgba(ctx, (0.15, 0.32, 0.2)); ctx.rectangle(0, gy - 6 * U, W, 14 * U); ctx.fill()
    bx = W * 0.3 if not VERT else W * 0.32
    rgba(ctx, (0.1, 0.07, 0.06))
    smooth(ctx, [(bx - 60 * U, gy), (bx - 30 * U, gy + 60 * U), (bx + 60 * U, gy + 110 * U), (bx + 220 * U, gy + 120 * U), (bx + 260 * U, gy + 90 * U),
                 (bx + 200 * U, gy + 60 * U), (bx + 80 * U, gy + 60 * U), (bx + 10 * U, gy + 30 * U), (bx + 10 * U, gy)]); ctx.fill()
    pk = prog(t, 0.8, 2.0)
    mammal(ctx, bx + 160 * U, gy + 112 * U, 80 * U, (0.75, 0.6, 0.45), 1, t)
    mammal(ctx, bx - 20 * U + 240 * U * pk, gy, 110 * U, (0.85, 0.7, 0.5), pk, t)
    # tree of descendants
    g = prog(t, d * 0.35, d * 0.85)
    if g:
        rx, ry = (W * 0.72, gy - 10 * U) if not VERT else (W * 0.72, gy - 10 * U)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        def branch(x, y, ang, ln, depth, w):
            if depth == 0: return
            kk = clamp(g * 5 - (5 - depth))
            if kk <= 0: return
            x2, y2 = x + math.cos(ang) * ln * kk, y + math.sin(ang) * ln * kk
            ctx.set_line_width(w); rgba(ctx, GOLD, 0.9); ctx.move_to(x, y); ctx.line_to(x2, y2); ctx.stroke()
            if kk >= 1:
                branch(x2, y2, ang - 0.42, ln * 0.74, depth - 1, w * 0.72)
                branch(x2, y2, ang + 0.38, ln * 0.74, depth - 1, w * 0.72)
        branch(rx, ry, -math.pi / 2, 150 * U if not VERT else 130 * U, 5, 14 * U)
        if g > 0.95:
            tip = (rx + 155 * U, ry - 385 * U) if not VERT else (rx + 135 * U, ry - 335 * U)
            glow(ctx, tip[0], tip[1], 50 * U, GOLD, 0.8)
    k = prog(t, 1.5, 2.5)
    if VERT:
        text(ctx, "SMALL SURVIVORS", CX, H * 0.15, 66 * U, WHITE, k)
    else:
        text(ctx, "SMALL SURVIVORS", W * 0.3, H * 0.25, 60 * U, WHITE, k)
    l2 = prog(t, d * 0.8, d * 0.9)
    if l2:
        if VERT: text(ctx, "… one branch led to us", CX, H * 0.15 + 85 * U, 44 * U, GOLD, l2, False)
        else: text(ctx, "… one branch led to us", W * 0.3, H * 0.25 + 75 * U, 42 * U, GOLD, l2, False)
    chip(ctx, "THE RISE OF MAMMALS", t)

def sc_outro(ctx, t, d):
    vgrad(ctx, NAVY2, NAVY); stars(ctx, t, 0.6)
    yo = -80 * U if not VERT else -200 * U
    asteroid(ctx, CX + 200 * U, CY + yo - 230 * U, 40 * U, t, 1, 0.6)
    dino(ctx, "t", CX - 160 * U, CY + yo - 120 * U, 90 * U, GOLD, 1, eye=NAVY)
    text(ctx, "FACTORA", CX, CY + yo, 140 * U, WHITE, prog(t, 0, 0.6))
    text(ctx, "fascinating facts, explained", CX, CY + yo + 100 * U, 38 * U, GOLD, prog(t, 0.4, 1.0), False)
    k = prog(t, d * 0.7, d * 0.78)
    if k:
        bw, bh = 520 * U, 110 * U
        pop = 1 + 0.05 * math.sin(t * 6)
        ctx.save(); ctx.translate(CX, CY + yo + 260 * U); ctx.scale(pop * k, pop * k)
        rrect(ctx, -bw / 2, -bh / 2, bw, bh, 22 * U); rgba(ctx, (0.85, 0.12, 0.12)); ctx.fill()
        text(ctx, "SUBSCRIBE", 0, 0, 52 * U, WHITE)
        ctx.restore()
    q = prog(t, d * 0.3, d * 0.4)
    if q and k < 1: text(ctx, "What if it had missed?", CX, CY + yo + 260 * U, 48 * U, WHITE, q * (1 - k))

SHORT_SCENES = ["hook", "winter", "birds", "outro"]

SCENES = dict(hook=sc_hook, reign=sc_reign, clue=sc_clue, impact=sc_impact, blast=sc_blast, winter=sc_winter,
              food=sc_food, volcano=sc_volcano, birds=sc_birds, mammals=sc_mammals, outro=sc_outro)

def thumbnail(c):
    """Thumbnail 1280x720."""
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, .08, .08, .22); g.add_color_stop_rgb(1, .45, .18, .2); c.set_source(g); c.paint()
    random.seed(1)
    for _ in range(120):
        c.arc(random.random() * W, random.random() * H * 0.6, random.uniform(.5, 1.6), 0, 6.3); c.set_source_rgba(1, 1, 1, random.uniform(.3, .8)); c.fill()
    # asteroid + trail
    rg = cairo.RadialGradient(1000, 330, 0, 1000, 330, 420); rg.add_color_stop_rgba(0, 1, .55, .2, .55); rg.add_color_stop_rgba(1, 1, .55, .2, 0)
    c.set_source(rg); c.arc(1000, 330, 420, 0, 6.3); c.fill()
    asteroid(c, 1040, 170, 55, 0.3, 1, 1.0, ang=-0.7)
    # ground + T. rex silhouette (right half)
    c.set_source_rgb(.03, .03, .06); c.rectangle(0, 610, W, 110); c.fill()
    dino(c, "s", 1150, 615, 105, (.06, .05, .09))
    dino(c, "t", 990, 615, 255, (.03, .03, .06))
    c.set_source_rgba(1, .8, .33, .9); c.arc(990 + 0.78 * 255, 615 - 1.0 * 255, 7, 0, 6.3); c.fill()
    thumb_text(c, "WHY DID THE", "DINOSAURS DIE?", "THE REAL STORY")
