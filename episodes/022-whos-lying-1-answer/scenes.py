# Episode 022 (Short only) - "Who's Lying? #1 — THE ANSWER" — same film-noir world as ep. 019.
# Executed inside engine/render.py (helpers available). Vertical layout. Original vector illustration. All sizes in U.
# Reuses the drawing helpers of ep. 019 (noir_bg, silhouette, badge, lamp, prop, board, bolt, rain...).
exec(open(os.path.join(os.path.dirname(EP.rstrip("/")), "019-whos-lying-1", "scenes.py"), encoding="utf-8").read())

LIAR = 2   # the gardener

def stamp(ctx, x, y, s, a, label="LIAR!"):
    if a <= 0: return
    ctx.save(); ctx.translate(x, y); ctx.rotate(-0.16); ctx.scale(s, s)
    font(ctx, 120 * U); w = ctx.text_extents(label).width + 80 * U
    rrect(ctx, -w / 2, -85 * U, w, 170 * U, 26 * U); rgba(ctx, (0, 0, 0), 0.45 * a); ctx.fill()
    rrect(ctx, -w / 2, -85 * U, w, 170 * U, 26 * U); ctx.set_line_width(12 * U); rgba(ctx, CORAL, a); ctx.stroke()
    text(ctx, label, 0, 0, 120 * U, CORAL, a)
    ctx.restore()

def sc_hook(ctx, t, d):
    f = noir_bg(ctx, t, (0.18, 0.20, 0.46), (0.04, 0.04, 0.12))
    bolt(ctx, W * 0.84, 0, H * 0.30, 4, max(f, 0.0))
    for i in range(4):
        x = W * (0.14 + 0.24 * i)
        liar = i == LIAR
        a = 1.0 if liar else 0.5
        if liar:
            glow(ctx, x, H * 0.50, 330 * U, CORAL, 0.45 + 0.1 * math.sin(t * 6))
        silhouette(ctx, x, H * 0.64, (0.95 if liar else 0.8) * U, COLS[i], i, a, t, 1.0 if liar else 0.3)
        badge(ctx, x, H * 0.64 + 80 * U, i + 1, COLS[i], a, 52 if liar else 40)
    k = prog(t, 0.35, 0.7)
    stamp(ctx, W * 0.62, H * 0.47, 1.0 + 0.6 * (1 - k), k)
    text(ctx, "CASE #1 · THE ANSWER", CX, H * 0.255, 70 * U, WHITE, prog(t, 0.0, 0.3))
    overlay_flash(ctx, f)

def waves(ctx, x, y, t, a, col=GOLD):
    for k in range(3):
        r = (40 + 34 * k) * U * (1 + 0.08 * math.sin(t * 8 - k))
        ctx.new_path(); ctx.arc(x, y, r, -0.7, 0.7); ctx.set_line_width(9 * U); rgba(ctx, col, (0.9 - 0.25 * k) * a); ctx.stroke()

def mini_bolt(ctx, x, y, s, a, col=(0.85, 0.9, 1.0)):
    ctx.save(); ctx.translate(x, y); ctx.scale(s * U, s * U)
    ctx.move_to(10, -70); ctx.line_to(-30, 5); ctx.line_to(0, 5); ctx.line_to(-15, 70); ctx.line_to(35, -15); ctx.line_to(5, -15); ctx.line_to(20, -70); ctx.close_path()
    rgba(ctx, col, a); ctx.fill(); ctx.restore()
    glow(ctx, x, y, 90 * s * U / 1.0, col, 0.35 * a)

def sc_clue(ctx, t, d):
    f = noir_bg(ctx, t, mix(COLS[LIAR], INK, 0.88), (0.0, 0.0, 0.02), 0.7)
    lamp(ctx, t, prog(t, 0, 0.3))
    k = prog(t, 0.05, 0.4)
    silhouette(ctx, W * 0.30, H * 0.66, 1.1 * U, COLS[LIAR], LIAR, k, t, 0.8)
    badge(ctx, W * 0.12, H * 0.115, LIAR + 1, COLS[LIAR], k, 56)
    text(ctx, NAMES[LIAR], W * 0.21, H * 0.115, 78 * U, WHITE, k, True, "l")
    q = "“I HEARD THE THUNDER, THEN SAW THE LIGHTNING”"
    font(ctx, 50 * U); qs = 50 * U * min(1, W * 0.84 / max(1, ctx.text_extents(q).width))
    rrect(ctx, CX - W * 0.46, H * 0.19 - 50 * U, W * 0.92, 100 * U, 50 * U); rgba(ctx, (0, 0, 0), 0.75 * k); ctx.fill()
    text(ctx, q, CX, H * 0.19, qs, COLS[LIAR], k)
    # his order of events: 1 thunder, 2 lightning
    x0 = W * 0.73
    a1 = prog(t, d * 0.25, d * 0.4); a2 = prog(t, d * 0.45, d * 0.6)
    waves(ctx, x0 - 40 * U, H * 0.36, t, a1)
    text(ctx, "1  THUNDER", x0, H * 0.43, 54 * U, GOLD, a1)
    mini_bolt(ctx, x0, H * 0.52, 1.4, a2)
    text(ctx, "2  LIGHTNING", x0, H * 0.59, 54 * U, (0.85, 0.9, 1.0), a2)
    xk = prog(t, d * 0.7, d * 0.8)
    if xk:
        r = 190 * U
        cx, cy = x0, H * 0.475
        for (sx, sy, ex, ey) in ((-r, -r, r, r), (r, -r, -r, r)):
            ctx.move_to(cx + sx, cy + sy); ctx.line_to(cx + sx + (ex - sx) * xk, cy + sy + (ey - sy) * xk)
            ctx.set_line_width(22 * U); ctx.set_line_cap(cairo.LINE_CAP_ROUND); rgba(ctx, CORAL, 0.95); ctx.stroke()
        text(ctx, "WRONG ORDER!", CX, H * 0.27, 96 * U, CORAL, xk)
    overlay_flash(ctx, f)

def cloud(ctx, x, y, s, a):
    for (dx, dy, r) in ((-130, 20, 95), (-40, -30, 125), (80, -10, 110), (160, 30, 80), (20, 45, 100)):
        circle(ctx, x + dx * s * U, y + dy * s * U, r * s * U, (0.30, 0.33, 0.48), a)
    for (dx, dy, r) in ((-60, -45, 70), (60, -35, 60)):
        circle(ctx, x + dx * s * U, y + dy * s * U, r * s * U, (0.45, 0.48, 0.62), 0.5 * a)

def head(ctx, x, y, a):
    """Observer seen from the side: big glowing eye + ear."""
    ctx.save(); ctx.translate(x, y)
    ctx.new_path(); ctx.arc(0, 0, 150 * U, 0, 2 * math.pi); rgba(ctx, mix(INK, CYAN, 0.25), a); ctx.fill()
    ctx.new_path(); ctx.arc(0, 0, 150 * U, 0, 2 * math.pi); ctx.set_line_width(6 * U); rgba(ctx, CYAN, 0.7 * a); ctx.stroke()
    ctx.restore()

def sc_science(ctx, t, d):
    vgrad(ctx, (0.05, 0.05, 0.16), (0.01, 0.01, 0.04)); rain(ctx, t, 0.6)
    tl, ts = d * 0.10, d * 0.55          # light arrives / sound arrives
    cy, oy = H * 0.13, H * 0.50          # cloud / observer
    fl = 0.0
    if t > tl:
        e = t - tl; fl = 1.0 if e < 0.08 else (0.4 if e < 0.16 else (0.9 if e < 0.24 else math.exp(-(e - 0.24) * 4)))
    if fl > 0:
        rgba(ctx, (0.55, 0.62, 0.95), 0.30 * fl); ctx.paint()
    cloud(ctx, CX, cy, 1.0, 1.0)
    bolt(ctx, CX + 20 * U, cy + 60 * U, cy + 300 * U, 7, fl)
    # LIGHT: instant beam to the observer (left lane)
    lx, sx = W * 0.25, W * 0.75
    y0 = H * 0.31
    la = prog(t, tl, tl + 0.15)
    ctx.move_to(lx, y0); ctx.line_to(lx, y0 + (oy - 60 * U - y0) * la)
    ctx.set_line_width(14 * U); rgba(ctx, CYAN, 0.9); ctx.stroke(); glow(ctx, lx, oy - 40 * U, 120 * U, CYAN, 0.6 * la)
    text(ctx, "LIGHT", lx, H * 0.245, 70 * U, CYAN, prog(t, 0, 0.3))
    text(ctx, "186,000 MI/SEC", lx, H * 0.28, 44 * U, WHITE, prog(t, 0, 0.3))
    # SOUND: rings creeping down (right lane)
    sk = clamp((t - tl) / (ts - tl)) if t > tl else 0
    for j in range(4):
        yy = y0 + (oy - 60 * U - y0) * clamp(sk - j * 0.08)
        if sk - j * 0.08 > 0:
            ctx.new_path(); ctx.arc(sx, yy, (60 - 8 * j) * U, 0.3, math.pi - 0.3)
            ctx.set_line_width(10 * U); rgba(ctx, GOLD, 0.9 - 0.2 * j); ctx.stroke()
    text(ctx, "SOUND", sx, H * 0.245, 70 * U, GOLD, prog(t, 0, 0.3))
    text(ctx, "0.2 MI/SEC", sx, H * 0.28, 44 * U, WHITE, prog(t, 0, 0.3))
    # observer + order
    head(ctx, CX, oy + 60 * U, 1.0)
    circle(ctx, CX - 50 * U, oy + 40 * U, 30 * U, WHITE, 1.0); circle(ctx, CX - 50 * U, oy + 40 * U, 14 * U, INK, 1.0)
    glow(ctx, CX - 50 * U, oy + 40 * U, 80 * U, CYAN, 0.6 * la)
    ctx.new_path(); ctx.arc(CX + 70 * U, oy + 60 * U, 38 * U, -1.6, 1.6); ctx.set_line_width(12 * U); rgba(ctx, GOLD, 0.9); ctx.stroke()
    b1 = prog(t, tl + 0.1, tl + 0.4); b2 = prog(t, ts, ts + 0.3)
    badge(ctx, W * 0.25, oy + 60 * U, 1, CYAN, b1, 48)
    text(ctx, "FLASH", W * 0.25, oy + 150 * U, 56 * U, CYAN, b1)
    badge(ctx, W * 0.75, oy + 60 * U, 2, GOLD, b2, 48)
    text(ctx, "BOOM", W * 0.75, oy + 150 * U, 56 * U, GOLD, b2)
    fk = prog(t, ts + 0.2, ts + 0.6)
    s = 1 + 0.05 * math.sin(t * 7)
    ctx.save(); ctx.translate(CX, H * 0.625); ctx.scale(s, s)
    text(ctx, "~1,000,000× FASTER", 0, 0, 84 * U, CYAN, fk); ctx.restore()

def stove(ctx, x, y, t, a):
    # stove top + burner with blue gas flames + kettle
    rrect(ctx, x - 230 * U, y, 460 * U, 70 * U, 14 * U); rgba(ctx, (0.25, 0.27, 0.33), a); ctx.fill()
    rrect(ctx, x - 230 * U, y + 70 * U, 460 * U, 200 * U, 10 * U); rgba(ctx, (0.15, 0.16, 0.22), a); ctx.fill()
    for kx in (-130, 0, 130):
        circle(ctx, x + kx * U, y + 160 * U, 26 * U, (0.4, 0.42, 0.5), a)
    for i in range(9):
        fx = x + (i - 4) * 34 * U; h = (60 + 18 * math.sin(t * 14 + i * 1.7)) * U
        ctx.move_to(fx - 14 * U, y); ctx.curve_to(fx - 10 * U, y - h * 0.6, fx, y - h, fx, y - h)
        ctx.curve_to(fx, y - h, fx + 10 * U, y - h * 0.6, fx + 14 * U, y); ctx.close_path()
        rgba(ctx, (0.30, 0.55, 1.0), 0.85 * a); ctx.fill()
    glow(ctx, x, y - 30 * U, 200 * U, (0.3, 0.55, 1.0), 0.5 * a)
    # kettle
    ky = y - 95 * U
    rrect(ctx, x - 150 * U, ky - 200 * U, 300 * U, 200 * U, 90 * U); rgba(ctx, (0.85, 0.87, 0.92), a); ctx.fill()
    ctx.move_to(x + 130 * U, ky - 110 * U); ctx.line_to(x + 230 * U, ky - 190 * U); ctx.set_line_width(30 * U); ctx.set_line_cap(cairo.LINE_CAP_ROUND); rgba(ctx, (0.85, 0.87, 0.92), a); ctx.stroke()
    ctx.new_path(); ctx.arc(x, ky - 200 * U, 90 * U, math.pi, 2 * math.pi); ctx.set_line_width(16 * U); rgba(ctx, (0.6, 0.62, 0.7), a); ctx.stroke()
    for k in range(3):
        ph = t * 1.6 + k
        ctx.new_path(); ctx.move_to(x + 240 * U, ky - 210 * U - k * 10 * U)
        ctx.curve_to(x + (250 + 30 * math.sin(ph)) * U, ky - 280 * U, x + (230 - 30 * math.sin(ph)) * U, ky - 330 * U, x + 250 * U, ky - 390 * U)
        ctx.set_line_width(9 * U); rgba(ctx, WHITE, 0.35 * a); ctx.stroke()

def check(ctx, x, y, s, a, col=GREEN):
    if a <= 0: return
    glow(ctx, x, y, 120 * s * U, col, 0.4 * a)
    ctx.move_to(x - 50 * s * U, y); ctx.line_to(x - 12 * s * U, y + 40 * s * U); ctx.line_to(x + 60 * s * U, y - 45 * s * U)
    ctx.set_line_width(20 * s * U); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_join(cairo.LINE_JOIN_ROUND); rgba(ctx, col, a); ctx.stroke()

def sc_tea(ctx, t, d):
    f = noir_bg(ctx, t, mix(COLS[1], INK, 0.86), (0.0, 0.0, 0.02), 0.5)
    lamp(ctx, t, prog(t, 0, 0.3))
    k = prog(t, 0.05, 0.4)
    silhouette(ctx, W * 0.25, H * 0.66, 1.0 * U, COLS[1], 1, k, t, 0.7)
    badge(ctx, W * 0.12, H * 0.115, 2, COLS[1], k, 56)
    text(ctx, "THE MAID'S TEA?", W * 0.21, H * 0.115, 78 * U, WHITE, k, True, "l")
    sa = prog(t, d * 0.45, d * 0.6)
    stove(ctx, W * 0.68, H * 0.52, t, sa)
    text(ctx, "GAS STOVE", W * 0.68, H * 0.63, 64 * U, (0.45, 0.7, 1.0), sa)
    ck = prog(t, d * 0.65, d * 0.8)
    check(ctx, CX - 330 * U, H * 0.215, 1.0, ck)
    text(ctx, "NO POWER NEEDED", CX - 230 * U, H * 0.215, 70 * U, GREEN, ck, True, "l")
    overlay_flash(ctx, f)

def sc_outro(ctx, t, d):
    noir_bg(ctx, t, (0.06, 0.03, 0.12))
    board(ctx, t, 0.22)
    cta(ctx, t, d, "DID YOU SOLVE IT?", "NEW CASE THIS SATURDAY")

SHORT_SCENES = ["hook", "clue", "science", "tea", "outro"]
SCENES = dict(hook=sc_hook, clue=sc_clue, science=sc_science, tea=sc_tea, outro=sc_outro)

def thumbnail(c):
    vgrad(c, (0.06, 0.05, 0.16), (0.01, 0.01, 0.04))
    thumb_text(c, "WHO'S LYING?", "THE ANSWER", "CASE #1")
