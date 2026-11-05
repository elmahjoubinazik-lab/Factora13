# Episode 011 - "How is money actually created?"
# Executed inside engine/render.py: helpers (W, H, U, CX, CY, VERT, colors, vgrad, circle, glow,
# text, rrect, stars, chip, prog, ease, mix...) are available.

GREEN = (0.35, 0.78, 0.55)
NOTE = (0.55, 0.80, 0.62)
NOTE_D = (0.25, 0.55, 0.38)
SCREEN = (0.10, 0.16, 0.32)

def bg(ctx, t, s=0.45):
    vgrad(ctx, NAVY2, NAVY); stars(ctx, t, s)

def banknote(ctx, x, y, w, ang=0.0, a=1.0, label="100"):
    h = w * 0.5
    ctx.save(); ctx.translate(x, y); ctx.rotate(ang)
    rrect(ctx, -w / 2, -h / 2, w, h, w * 0.05); rgba(ctx, NOTE, a); ctx.fill()
    ctx.set_line_width(w * 0.025); rgba(ctx, NOTE_D, a)
    rrect(ctx, -w / 2 + w * 0.06, -h / 2 + w * 0.06, w - w * 0.12, h - w * 0.12, w * 0.03); ctx.stroke()
    ctx.new_path(); ctx.arc(0, 0, h * 0.28, 0, 2 * math.pi); ctx.stroke()
    text(ctx, label, -w * 0.3, -h * 0.18, w * 0.11, NOTE_D, a)
    text(ctx, label, w * 0.3, h * 0.18, w * 0.11, NOTE_D, a)
    ctx.restore()

def coin(ctx, x, y, r, a=1.0):
    circle(ctx, x, y + r * 0.12, r, (0.75, 0.55, 0.15), a)
    circle(ctx, x, y, r, GOLD, a)
    ctx.new_path(); ctx.arc(x, y, r * 0.75, 0, 2 * math.pi); ctx.set_line_width(r * 0.08); rgba(ctx, (0.85, 0.62, 0.2), a); ctx.stroke()

def bank(ctx, x, y, s, c=WHITE, a=1.0, label=None, dome=False):
    """Classical bank building, base centered at (x, y), width ~ 2s."""
    rgba(ctx, c, a)
    ctx.move_to(x - s * 1.05, y - s * 1.15); ctx.line_to(x, y - s * 1.6); ctx.line_to(x + s * 1.05, y - s * 1.15); ctx.close_path(); ctx.fill()
    ctx.rectangle(x - s * 1.0, y - s * 1.15, s * 2.0, s * 0.14); ctx.fill()
    for i in range(5):
        cx_ = x - s * 0.8 + i * s * 0.4
        ctx.rectangle(cx_ - s * 0.09, y - s * 0.98, s * 0.18, s * 0.8); ctx.fill()
    ctx.rectangle(x - s * 1.1, y - s * 0.18, s * 2.2, s * 0.18); ctx.fill()
    if dome:
        ctx.new_path(); ctx.arc(x, y - s * 1.6, s * 0.35, math.pi, 2 * math.pi); ctx.fill()
    if label: text(ctx, label, x, y + s * 0.35, s * 0.28, c, a)

def account(ctx, x, y, w, value, a=1.0, title="YOUR ACCOUNT", hi=0.0):
    h = w * 0.55
    rrect(ctx, x - w / 2, y - h / 2, w, h, w * 0.06); rgba(ctx, SCREEN, a); ctx.fill()
    ctx.set_line_width(4 * U); rgba(ctx, mix((0.4, 0.5, 0.8), GOLD, hi), a)
    rrect(ctx, x - w / 2, y - h / 2, w, h, w * 0.06); ctx.stroke()
    text(ctx, title, x, y - h * 0.28, w * 0.065, (0.7, 0.75, 0.9), a, False)
    if hi: glow(ctx, x, y + h * 0.05, w * 0.45, GOLD, 0.25 * hi * a)
    text(ctx, "{:,}".format(int(round(value))), x, y + h * 0.08, w * 0.17, mix(WHITE, GOLD, hi), a)

def arrow(ctx, x1, y1, x2, y2, c=GOLD, a=1.0, w=6.0, head=22.0):
    ang = math.atan2(y2 - y1, x2 - x1)
    ctx.set_line_width(w * U); ctx.set_line_cap(cairo.LINE_CAP_ROUND); rgba(ctx, c, a)
    ctx.move_to(x1, y1); ctx.line_to(x2, y2); ctx.stroke()
    hs = head * U
    ctx.move_to(x2, y2); ctx.line_to(x2 - hs * math.cos(ang - 0.45), y2 - hs * math.sin(ang - 0.45))
    ctx.line_to(x2 - hs * math.cos(ang + 0.45), y2 - hs * math.sin(ang + 0.45)); ctx.close_path(); ctx.fill()

def pill(ctx, label, x, y, size, c=GOLD, a=1.0, fill=NAVY):
    font(ctx, size); w = ctx.text_extents(label).width + size * 1.4; h = size * 2.0
    rrect(ctx, x - w / 2, y - h / 2, w, h, h / 2); rgba(ctx, fill, 0.88 * a); ctx.fill()
    ctx.set_line_width(3 * U); rgba(ctx, c, a); rrect(ctx, x - w / 2, y - h / 2, w, h, h / 2); ctx.stroke()
    text(ctx, label, x, y, size, c, a)

# ---------- scenes ----------
def sc_hook(ctx, t, d):
    bg(ctx, t)
    ph2 = prog(t, d * 0.33, d * 0.42)
    # phase 1: printing press with notes flying out
    if ph2 < 1:
        a = 1 - ph2
        px, py = (CX, CY - 40 * U) if not VERT else (CX, H * 0.38)
        rrect(ctx, px - 260 * U, py - 160 * U, 520 * U, 260 * U, 30 * U); rgba(ctx, (0.3, 0.36, 0.55), a); ctx.fill()
        for i in range(3):
            ctx.new_path(); ctx.arc(px - 120 * U + i * 120 * U, py - 30 * U, 55 * U, 0, 2 * math.pi); rgba(ctx, (0.2, 0.25, 0.4), a); ctx.fill()
            ctx.save(); ctx.translate(px - 120 * U + i * 120 * U, py - 30 * U); ctx.rotate(t * 3)
            rgba(ctx, GOLD, a); ctx.rectangle(-50 * U, -5 * U, 100 * U, 10 * U); ctx.fill(); ctx.restore()
        for j in range(6):
            k = (t * 0.6 + j / 6) % 1
            banknote(ctx, px + 260 * U + k * 420 * U * (1 if not VERT else 0.6), py + 40 * U - math.sin(k * math.pi) * 200 * U, 150 * U, k * 2 + j, a * (1 - k))
        text(ctx, "THE GOVERNMENT PRINTS IT?", CX, py - 280 * U if not VERT else py - 300 * U, 60 * U if not VERT else 52 * U, WHITE, a)
    if ph2:
        sx, sy = (CX, CY - 60 * U) if not VERT else (CX, H * 0.38)
        v = 10000 * prog(t, d * 0.45, d * 0.62)
        account(ctx, sx, sy, 640 * U, v, ph2, hi=prog(t, d * 0.6, d * 0.65))
        # keyboard
        ky = sy + 260 * U
        for r in range(3):
            for c_ in range(10 - r):
                kx = sx - (9 - r) * 30 * U + c_ * 60 * U
                press = 1 if (int(t * 8) + c_ + r) % 7 == 0 and t < d * 0.62 else 0
                rrect(ctx, kx - 25 * U, ky + r * 60 * U - 25 * U + press * 5 * U, 50 * U, 50 * U, 8 * U); rgba(ctx, mix((0.3, 0.36, 0.55), GOLD, press), ph2); ctx.fill()
        q = prog(t, d * 0.75, d * 0.82)
        if q:
            if VERT:
                text(ctx, "HOW IS MONEY", CX, H * 0.12, 84 * U, WHITE, q)
                text(ctx, "REALLY CREATED?", CX, H * 0.12 + 100 * U, 84 * U, GOLD, q)
            else:
                text(ctx, "HOW IS MONEY REALLY CREATED?", CX, H * 0.12, 76 * U, WHITE, q)

def sc_cash(ctx, t, d):
    bg(ctx, t)
    cols, rows = 10, 10
    cell = 46 * U if not VERT else 70 * U
    gx0 = (W * 0.36 if not VERT else CX) - (cols - 1) * cell / 2
    gy0 = (H * 0.44 if not VERT else H * 0.36) - (rows - 1) * cell / 2
    sp = prog(t, d * 0.35, d * 0.55)
    for i in range(100):
        r_, c_ = divmod(i, cols)
        x, y = gx0 + c_ * cell, gy0 + r_ * cell
        appear = prog(t, 0.3 + i * 0.012, 0.6 + i * 0.012)
        is_cash = i >= 97
        col = GOLD if (is_cash and sp > 0) else mix((0.55, 0.6, 0.8), (0.3, 0.6, 1.0), prog(t, d * 0.75, d * 0.85))
        rrect(ctx, x - cell * 0.42, y - cell * 0.42, cell * 0.84, cell * 0.84, cell * 0.15); rgba(ctx, col, appear); ctx.fill()
        if is_cash and sp: coin(ctx, x, y, cell * 0.3 * sp, appear)
    lx = W * 0.72 if not VERT else CX
    ly = H * 0.36 if not VERT else gy0 - 160 * U
    if VERT: ly = H * 0.36 + rows * cell / 2 + 60 * U
    if sp:
        banknote(ctx, lx - 70 * U if not VERT else CX - 300 * U, ly - (150 * U if not VERT else -40 * U), 150 * U, -0.15, sp)
        coin(ctx, lx + 70 * U if not VERT else CX + 300 * U, ly - (140 * U if not VERT else -40 * U), 40 * U, sp)
        if VERT:
            text(ctx, "COINS & NOTES ≈ 3%", CX, ly + 40 * U, 54 * U, GOLD, sp)
        else:
            text(ctx, "COINS & NOTES ≈ 3%", lx, ly, 54 * U, GOLD, sp)
    dg = prog(t, d * 0.75, d * 0.85)
    if dg:
        if VERT: text(ctx, "THE REST: BANK DEPOSITS", CX, gy0 - 110 * U, 50 * U, (0.5, 0.75, 1.0), dg)
        else: text(ctx, "THE REST: BANK DEPOSITS", lx, ly + 100 * U, 46 * U, (0.5, 0.75, 1.0), dg)
    chip(ctx, "UK · SOURCE: BANK OF ENGLAND", t)

def sc_loan(ctx, t, d):
    bg(ctx, t)
    if VERT: bx, by, ax, ay = CX, H * 0.3, CX, H * 0.56
    else: bx, by, ax, ay = W * 0.27, H * 0.62, W * 0.7, H * 0.42
    bank(ctx, bx, by, 170 * U if not VERT else 140 * U, WHITE, prog(t, 0, 0.6), "COMMERCIAL BANK")
    # no vault money moves: crossed-out savings
    s = prog(t, d * 0.32, d * 0.4) * (1 - prog(t, d * 0.55, d * 0.6))
    if s:
        vx, vy = (bx + 300 * U, by - 330 * U) if not VERT else (CX + 330 * U, by - 230 * U)
        for i in range(3): banknote(ctx, vx, vy - i * 14 * U, 140 * U, 0, s)
        ctx.set_line_width(10 * U); rgba(ctx, CORAL, s)
        ctx.move_to(vx - 90 * U, vy - 70 * U); ctx.line_to(vx + 90 * U, vy + 50 * U); ctx.stroke()
        text(ctx, "someone's savings", vx, vy + 85 * U, 30 * U, WHITE, s, False)
    k = prog(t, d * 0.6, d * 0.75)
    v = 10000 * k
    account(ctx, ax, ay, 560 * U if not VERT else 600 * U, v, prog(t, 0.5, 1.2), hi=prog(t, d * 0.72, d * 0.8))
    if k:
        if VERT: arrow(ctx, bx, by + 70 * U, ax, ay - 180 * U, GOLD, k)
        else: arrow(ctx, bx + 210 * U, by - 150 * U, ax - 300 * U, ay, GOLD, k)
    nm = prog(t, d * 0.8, d * 0.88)
    if nm: pill(ctx, "NEW MONEY", ax, ay - (230 * U if not VERT else 240 * U), 46 * U, GOLD, nm)
    chip(ctx, "STEP 1 · A LOAN", t)

def sc_books(ctx, t, d):
    bg(ctx, t)
    w = 1300 * U if not VERT else 960 * U
    x0 = CX - w / 2
    y0 = H * 0.2 if not VERT else H * 0.22
    hh = 520 * U if not VERT else 640 * U
    rrect(ctx, x0, y0, w, hh, 24 * U); rgba(ctx, (0.94, 0.92, 0.85)); ctx.fill()
    text(ctx, "THE BANK'S BOOKS", CX, y0 + 60 * U, 46 * U, NAVY)
    ctx.set_line_width(5 * U); rgba(ctx, NAVY)
    ctx.move_to(x0 + 40 * U, y0 + 110 * U); ctx.line_to(x0 + w - 40 * U, y0 + 110 * U); ctx.stroke()
    ctx.move_to(CX, y0 + 110 * U); ctx.line_to(CX, y0 + hh - 170 * U); ctx.stroke()
    cs = 38 * U if not VERT else 34 * U
    text(ctx, "THE BANK OWNS", x0 + w / 4, y0 + 160 * U, cs, (0.3, 0.35, 0.5), 1, False)
    text(ctx, "THE BANK OWES", x0 + 3 * w / 4, y0 + 160 * U, cs, (0.3, 0.35, 0.5), 1, False)
    a1 = prog(t, d * 0.35, d * 0.45); a2 = prog(t, d * 0.55, d * 0.65)
    yv = y0 + (300 * U if not VERT else 340 * U)
    if a2:
        ctx.save(); ctx.translate(x0 + 3 * w / 4, yv); ctx.scale(a2, a2)
        text(ctx, "your deposit", 0, -45 * U, cs, NAVY, 1, False); text(ctx, "10,000", 0, 25 * U, 72 * U, (0.15, 0.4, 0.8))
        ctx.restore()
    if a1:
        ctx.save(); ctx.translate(x0 + w / 4, yv); ctx.scale(a1, a1)
        text(ctx, "your loan", 0, -45 * U, cs, NAVY, 1, False); text(ctx, "10,000", 0, 25 * U, 72 * U, (0.15, 0.55, 0.35))
        ctx.restore()
    b = prog(t, d * 0.78, d * 0.86)
    if b:
        by_ = y0 + hh - 100 * U
        pill(ctx, "= BALANCED", CX, by_, 40 * U, (0.15, 0.45, 0.3), b, (0.85, 0.95, 0.88))
    chip(ctx, "STEP 2 · TWO ENTRIES", t)

def sc_spend(ctx, t, d):
    bg(ctx, t)
    if VERT:
        nodes = [(CX, H * 0.16), (W * 0.2, H * 0.36), (W * 0.8, H * 0.36), (W * 0.28, H * 0.6), (W * 0.72, H * 0.6)]
    else:
        nodes = [(W * 0.5, H * 0.2), (W * 0.2, H * 0.42), (W * 0.8, H * 0.42), (W * 0.33, H * 0.68), (W * 0.67, H * 0.68)]
    names = ["YOU", "SHOP", "LANDLORD", "CAFÉ", "PLUMBER"]
    edges = [(0, 1), (0, 2), (1, 3), (2, 4), (3, 4), (1, 2), (4, 0)]
    for (i, j) in edges:
        (x1, y1), (x2, y2) = nodes[i], nodes[j]
        ctx.set_line_width(3 * U); rgba(ctx, WHITE, 0.2); ctx.move_to(x1, y1); ctx.line_to(x2, y2); ctx.stroke()
    for n, (i, j) in enumerate(edges):
        (x1, y1), (x2, y2) = nodes[i], nodes[j]
        k = ((t * 0.45 + n * 0.37) % 1)
        if t < 0.6 + n * 0.3: continue
        x, y = x1 + (x2 - x1) * k, y1 + (y2 - y1) * k
        glow(ctx, x, y, 40 * U, GOLD, 0.5); coin(ctx, x, y, 18 * U)
    for i, (x, y) in enumerate(nodes):
        circle(ctx, x, y, 78 * U, SCREEN); ctx.new_path(); ctx.arc(x, y, 78 * U, 0, 2 * math.pi)
        ctx.set_line_width(4 * U); rgba(ctx, GOLD if i == 0 else (0.5, 0.6, 0.9)); ctx.stroke()
        bank(ctx, x, y + 30 * U, 30 * U, WHITE, 0.9)
        text(ctx, names[i], x, y + 110 * U, 30 * U, WHITE, 0.9)
    chip(ctx, "IT CIRCULATES", t)

def sc_repay(ctx, t, d):
    bg(ctx, t)
    ax, ay = (W * 0.32, H * 0.42) if not VERT else (CX, H * 0.3)
    k = prog(t, d * 0.3, d * 0.55)
    account(ctx, ax, ay, 560 * U, 10000 * (1 - k), 1, title="LOAN BALANCE", hi=0)
    # dissolving particles
    random.seed(6)
    for i in range(70):
        ph = random.random(); ang = random.uniform(0, 2 * math.pi); sp = random.uniform(100, 320) * U
        if not (0 < k < 1): break
        kk = (k * 2 + ph) % 1
        x = ax + math.cos(ang) * sp * kk; y = ay - 40 * U + math.sin(ang) * sp * kk * 0.6 - kk * 80 * U
        circle(ctx, x, y, 7 * U * (1 - kk), GOLD, 0.9 * (1 - kk))
    if k >= 1:
        text(ctx, "MONEY GONE", ax, ay - 230 * U, 50 * U, CORAL, prog(t, d * 0.55, d * 0.62))
    r = prog(t, d * 0.65, d * 0.75)
    if r:
        if VERT: rx, ry, gap = CX, H * 0.5, 120 * U
        else: rx, ry, gap = W * 0.73, H * 0.36, 150 * U
        pill(ctx, "LENDING → CREATES", rx, ry, 46 * U, GOLD, r)
        pill(ctx, "REPAYING → DESTROYS", rx, ry + gap, 46 * U, CORAL, prog(t, d * 0.8, d * 0.88))
    chip(ctx, "STEP 3 · REPAYMENT", t)

def sc_central(ctx, t, d):
    bg(ctx, t)
    if VERT: cx_, cy_ = CX, H * 0.3
    else: cx_, cy_ = CX, H * 0.45
    glow(ctx, cx_, cy_ - 120 * U, 340 * U, GOLD, 0.25)
    bank(ctx, cx_, cy_, 170 * U if not VERT else 150 * U, GOLD, prog(t, 0, 0.6), None, dome=True)
    text(ctx, "CENTRAL BANK", cx_, cy_ + 60 * U, 46 * U, GOLD, prog(t, 0, 0.6))
    n1 = prog(t, d * 0.3, d * 0.45)
    if VERT:
        p1, p2, p3 = (W * 0.22, H * 0.5), (W * 0.78, H * 0.5), (CX, H * 0.62)
    else:
        p1, p2, p3 = (W * 0.17, H * 0.32), (W * 0.83, H * 0.32), (W * 0.83, H * 0.66)
    if n1:
        for j in range(3): banknote(ctx, p1[0] + (j - 1) * 30 * U, p1[1] - j * 12 * U, 170 * U, -0.1 + j * 0.1, n1)
        text(ctx, "BANKNOTES", p1[0], p1[1] + 100 * U, 38 * U, WHITE, n1)
        if not VERT: arrow(ctx, cx_ - 230 * U, cy_ - 150 * U, p1[0] + 140 * U, p1[1], GOLD, n1)
    n2 = prog(t, d * 0.42, d * 0.52)
    if n2:
        mx_, my_ = (W * 0.17, H * 0.64) if not VERT else (W * 0.78, H * 0.5)
        for j in range(4): coin(ctx, mx_ - 60 * U + j * 40 * U, my_ - j * 6 * U, 32 * U, n2)
        text(ctx, "COINS: GOVERNMENT MINT", mx_, my_ + 80 * U, 32 * U, WHITE, n2, False)
    n3 = prog(t, d * 0.65, d * 0.75)
    if n3:
        q = p2 if not VERT else p3
        if not VERT: q = (W * 0.8, H * 0.48)
        # two small banks exchanging digital reserves
        b1x, b2x = q[0] - 140 * U, q[0] + 140 * U
        bank(ctx, b1x, q[1] + 60 * U, 55 * U, WHITE, n3); bank(ctx, b2x, q[1] + 60 * U, 55 * U, WHITE, n3)
        k = (t * 0.8) % 1
        glow(ctx, b1x + (b2x - b1x) * k, q[1] - 50 * U, 30 * U, (0.5, 0.8, 1.0), 0.9 * n3)
        text(ctx, "01", b1x + (b2x - b1x) * k, q[1] - 50 * U, 26 * U, WHITE, n3)
        text(ctx, "RESERVES", q[0], q[1] + 120 * U, 40 * U, (0.5, 0.8, 1.0), n3)
        text(ctx, "digital money between banks", q[0], q[1] + 165 * U, 28 * U, WHITE, 0.8 * n3, False)
    chip(ctx, "THE CENTRAL BANK", t)

def sc_rate(ctx, t, d):
    bg(ctx, t)
    # rate dial
    gx, gy = (W * 0.3, H * 0.55) if not VERT else (CX, H * 0.36)
    R = 230 * U
    ctx.new_path(); ctx.set_line_width(28 * U); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.arc(gx, gy, R, math.pi, 2 * math.pi); rgba(ctx, (0.25, 0.3, 0.5)); ctx.stroke()
    ctx.new_path(); ctx.arc(gx, gy, R, math.pi, math.pi * 1.33); rgba(ctx, GREEN); ctx.stroke()
    ctx.new_path(); ctx.arc(gx, gy, R, math.pi * 1.67, 2 * math.pi); rgba(ctx, CORAL); ctx.stroke()
    low = prog(t, d * 0.15, d * 0.3); high = prog(t, d * 0.78, d * 0.88)
    rate = 0.5 - 0.35 * low + 0.7 * high   # 0..1 position on dial
    ang = math.pi + math.pi * rate
    ctx.set_line_width(10 * U); rgba(ctx, WHITE)
    ctx.move_to(gx, gy); ctx.line_to(gx + math.cos(ang) * R * 0.85, gy + math.sin(ang) * R * 0.85); ctx.stroke()
    circle(ctx, gx, gy, 22 * U, WHITE)
    text(ctx, "INTEREST RATE", gx, gy + 70 * U, 42 * U, GOLD)
    text(ctx, "low", gx - R, gy + 50 * U, 30 * U, GREEN, 1, False); text(ctx, "high", gx + R, gy + 50 * U, 30 * U, CORAL, 1, False)
    # lending bars
    bx0, by0 = (W * 0.58, H * 0.68) if not VERT else (W * 0.2, H * 0.66)
    bw = 70 * U; n = 6
    lvl = 0.45 + 0.45 * low - 0.6 * high
    for i in range(n):
        hh = (120 + 300 * clamp(lvl) * (0.6 + 0.4 * i / n) + 10 * math.sin(t * 2 + i)) * U * (0.8 if VERT else 1)
        rrect(ctx, bx0 + i * bw * 1.4, by0 - hh, bw, hh, 10 * U); rgba(ctx, mix(CORAL, GREEN, clamp(lvl)), 0.9); ctx.fill()
    text(ctx, "NEW LOANS", bx0 + (n - 1) * bw * 0.7 + bw / 2, by0 + 40 * U, 38 * U, WHITE)
    chip(ctx, "THE MAIN LEVER", t)

def sc_limits(ctx, t, d):
    bg(ctx, t)
    items = [("BORROWERS WHO CAN REPAY", 0.18), ("STRICT RULES (CAPITAL)", 0.42), ("RISK OF LOSSES", 0.7)]
    y0 = H * 0.26 if not VERT else H * 0.3
    gap = 150 * U if not VERT else 160 * U
    ttl = prog(t, 0, 0.5)
    text(ctx, "UNLIMITED MONEY?", CX, H * 0.11 if not VERT else H * 0.18, 72 * U, WHITE, ttl)
    nk = prog(t, d * 0.08, d * 0.15)
    if nk:
        text(ctx, "NO", CX, (H * 0.11 + 85 * U if not VERT else H * 0.18 + 85 * U), 72 * U, CORAL, nk)
    for i, (lab, st) in enumerate(items):
        k = prog(t, d * st, d * st + 0.6)
        if not k: continue
        y = y0 + 80 * U + i * gap
        bw = 1000 * U if not VERT else 920 * U
        x = CX - bw / 2 + (1 - k) * 60 * U
        rrect(ctx, x, y - 55 * U, bw, 110 * U, 26 * U); rgba(ctx, SCREEN, 0.95 * k); ctx.fill()
        # lock icon
        lx, ly = x + 75 * U, y
        ctx.new_path(); ctx.arc(lx, ly - 14 * U, 20 * U, math.pi, 2 * math.pi); ctx.set_line_width(7 * U); rgba(ctx, GOLD, k); ctx.stroke()
        rrect(ctx, lx - 30 * U, ly - 14 * U, 60 * U, 44 * U, 8 * U); rgba(ctx, GOLD, k); ctx.fill()
        text(ctx, lab, x + 140 * U, y, 44 * U if not VERT else 40 * U, WHITE, k, True, "l")
    chip(ctx, "THE LIMITS", t)

def sc_trust(ctx, t, d):
    bg(ctx, t)
    gx, gy = (W * 0.3, H * 0.42) if not VERT else (CX, H * 0.24)
    a1 = 1 - prog(t, d * 0.55, d * 0.62)
    if a1:
        # gold bar
        ctx.move_to(gx - 170 * U, gy + 60 * U); ctx.line_to(gx + 170 * U, gy + 60 * U); ctx.line_to(gx + 120 * U, gy - 40 * U); ctx.line_to(gx - 120 * U, gy - 40 * U); ctx.close_path()
        rgba(ctx, GOLD, a1); ctx.fill()
        ctx.move_to(gx - 120 * U, gy - 40 * U); ctx.line_to(gx + 120 * U, gy - 40 * U); ctx.line_to(gx + 100 * U, gy - 70 * U); ctx.line_to(gx - 100 * U, gy - 70 * U); ctx.close_path()
        rgba(ctx, (1, 0.9, 0.55), a1); ctx.fill()
        text(ctx, "GOLD", gx, gy + 12 * U, 40 * U, (0.6, 0.42, 0.1), a1)
        c = prog(t, d * 0.12, d * 0.2)
        if c:
            ctx.set_line_width(14 * U); rgba(ctx, CORAL, c * a1)
            ctx.move_to(gx - 200 * U, gy - 120 * U); ctx.line_to(gx - 200 * U + 400 * U * c, gy - 120 * U + 260 * U * c); ctx.stroke()
        y71 = prog(t, d * 0.25, d * 0.35)
        if y71:
            tx_, ty_ = (W * 0.68, gy) if not VERT else (CX, gy + 220 * U)
            text(ctx, "1971", tx_, ty_ - 20 * U, 130 * U, WHITE, y71 * a1)
            text(ctx, "dollar no longer tied to gold", tx_, ty_ + 70 * U, 38 * U, GOLD, y71 * a1, False)
    a2 = prog(t, d * 0.6, d * 0.68)
    if a2:
        if VERT: c1, c2 = (CX, H * 0.22), (CX, H * 0.5)
        else: c1, c2 = (W * 0.3, H * 0.42), (W * 0.7, H * 0.42)
        # trust: two hands shape -> simple heart-like handshake replaced by two linked rings
        for dx in (-45, 45):
            ctx.new_path(); ctx.arc(c1[0] + dx * U, c1[1] - 20 * U, 70 * U, 0, 2 * math.pi); ctx.set_line_width(16 * U); rgba(ctx, GOLD, a2); ctx.stroke()
        text(ctx, "PEOPLE TRUST IT", c1[0], c1[1] + 110 * U, 46 * U, WHITE, a2)
        b = prog(t, d * 0.78, d * 0.86)
        if b:
            rrect(ctx, c2[0] - 85 * U, c2[1] - 120 * U, 170 * U, 210 * U, 14 * U); rgba(ctx, (0.94, 0.92, 0.85), b); ctx.fill()
            for i in range(5):
                rgba(ctx, (0.5, 0.5, 0.6), b); ctx.rectangle(c2[0] - 60 * U, c2[1] - 85 * U + i * 32 * U, 120 * U * (0.6 + 0.4 * (i % 2)), 10 * U); ctx.fill()
            coin(ctx, c2[0] + 70 * U, c2[1] + 70 * U, 40 * U, b)
            text(ctx, "ACCEPTED FOR TAXES", c2[0], c2[1] + 150 * U, 46 * U, WHITE, b)
    chip(ctx, "WHAT BACKS MONEY?", t)

def sc_outro(ctx, t, d):
    bg(ctx, t, 0.6)
    yo = -80 * U if not VERT else -200 * U
    for i in range(3): coin(ctx, CX - 60 * U + i * 60 * U, CY + yo - 190 * U - i * 10 * U, 50 * U)
    banknote(ctx, CX - 210 * U, CY + yo - 200 * U, 160 * U, -0.2)
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
    if q and k < 1: text(ctx, "Did you know this?", CX, CY + yo + 260 * U, 48 * U, WHITE, q * (1 - k))

SHORT_SCENES = ["hook", "loan", "repay", "outro"]

SCENES = dict(hook=sc_hook, cash=sc_cash, loan=sc_loan, books=sc_books, spend=sc_spend, repay=sc_repay,
              central=sc_central, rate=sc_rate, limits=sc_limits, trust=sc_trust, outro=sc_outro)

def thumbnail(c):
    """Thumbnail 1280x720."""
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, .08, .11, .26); g.add_color_stop_rgb(1, .02, .03, .08); c.set_source(g); c.paint()
    random.seed(1)
    for _ in range(140):
        c.arc(random.random() * W, random.random() * H, random.uniform(.5, 1.6), 0, 6.3); c.set_source_rgba(1, 1, 1, random.uniform(.3, .8)); c.fill()
    rg = cairo.RadialGradient(1010, 360, 0, 1010, 360, 330); rg.add_color_stop_rgba(0, 1, .8, .33, .4); rg.add_color_stop_rgba(1, 1, .8, .33, 0)
    c.set_source(rg); c.arc(1010, 360, 330, 0, 6.3); c.fill()
    # screen with a balance, notes and coins (right half)
    rrect(c, 800, 200, 420, 240, 26); c.set_source_rgb(*SCREEN); c.fill()
    c.set_line_width(6); c.set_source_rgb(*GOLD); rrect(c, 800, 200, 420, 240, 26); c.stroke()
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    c.set_font_size(30); c.set_source_rgb(.7, .75, .9); c.move_to(860, 265); c.show_text("NEW DEPOSIT")
    c.set_font_size(80); c.set_source_rgb(*GOLD); c.move_to(845, 375); c.show_text("+10,000")
    banknote(c, 880, 540, 220, -0.25); banknote(c, 1110, 560, 200, 0.2)
    for i in range(3): coin(c, 990 + i * 46, 600 - i * 8, 40)
    thumb_text(c, "WHO REALLY", "CREATES MONEY?", "NOT WHAT YOU THINK")
