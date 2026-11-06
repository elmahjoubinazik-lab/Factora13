# Episode 012 - "US midterms explained: what happens with or without a majority?"
# Executed inside engine/render.py: helpers (W, H, U, CX, CY, VERT, colors, vgrad, circle, glow,
# text, rrect, stars, chip, prog, ease, mix...) are available.
# Neutrality rules (CLAUDE.md): Party A = gold, Party B = cyan, no politicians drawn, fictional bill.

PA = GOLD
PB = (0.30, 0.82, 0.96)
SEAT = (0.42, 0.47, 0.62)
MAJ = (0.42, 0.88, 0.58)
PAPER = (0.95, 0.93, 0.86)
INK = (0.10, 0.13, 0.25)
STONE = (0.90, 0.91, 0.96)
STONE_D = (0.62, 0.66, 0.78)
PANEL = (0.08, 0.12, 0.26)

def P(hx, hy, vx, vy):
    return (W * hx, H * hy) if not VERT else (W * vx, H * vy)

def bg(ctx, t, s=0.35, tint=(0.07, 0.10, 0.24)):
    vgrad(ctx, tint, NAVY); stars(ctx, t, s)
    random.seed(42)
    for i in range(36):
        x0, y0, sp, r = random.random(), random.random(), random.uniform(0.01, 0.03), random.uniform(1.5, 4.0)
        y = (y0 - t * sp) % 1.0
        circle(ctx, x0 * W + math.sin(t * 0.7 + i) * 12 * U, y * H, r * U, (0.7, 0.8, 1.0), 0.18)

def star5(ctx, x, y, r, c, a=1.0, rot=0.0):
    ctx.new_path()
    for i in range(10):
        ang = -math.pi / 2 + rot + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.42
        (ctx.move_to if i == 0 else ctx.line_to)(x + math.cos(ang) * rr, y + math.sin(ang) * rr)
    ctx.close_path(); rgba(ctx, c, a); ctx.fill()

def arrow(ctx, x1, y1, x2, y2, c=GOLD, a=1.0, w=6.0, head=22.0):
    ang = math.atan2(y2 - y1, x2 - x1)
    ctx.set_line_width(w * U); ctx.set_line_cap(cairo.LINE_CAP_ROUND); rgba(ctx, c, a)
    ctx.move_to(x1, y1); ctx.line_to(x2, y2); ctx.stroke()
    hs = head * U
    ctx.move_to(x2, y2); ctx.line_to(x2 - hs * math.cos(ang - 0.45), y2 - hs * math.sin(ang - 0.45))
    ctx.line_to(x2 - hs * math.cos(ang + 0.45), y2 - hs * math.sin(ang + 0.45)); ctx.close_path(); ctx.fill()

def pill(ctx, label, x, y, size, c=GOLD, a=1.0, fill=NAVY):
    if a <= 0: return
    font(ctx, size); w = ctx.text_extents(label).width + size * 1.4; h = size * 2.0
    rrect(ctx, x - w / 2, y - h / 2, w, h, h / 2); rgba(ctx, fill, 0.9 * a); ctx.fill()
    ctx.set_line_width(3 * U); rgba(ctx, c, a); rrect(ctx, x - w / 2, y - h / 2, w, h, h / 2); ctx.stroke()
    text(ctx, label, x, y, size, c, a)

def bigtext(ctx, s, x, y, size, c, a=1.0):
    if a <= 0: return
    glow(ctx, x, y, size * 1.6, c, 0.22 * a)
    ctx.save(); ctx.translate(x, y); k = 0.7 + 0.3 * a; ctx.scale(k, k)
    text(ctx, s, 4 * U, 6 * U, size, (0, 0, 0), 0.45 * a)
    text(ctx, s, 0, 0, size, c, a)
    ctx.restore()

def counter(ctx, val, x, y, size, c, a=1.0, suffix=""):
    bigtext(ctx, "{:,}".format(int(round(val))) + suffix, x, y, size, c, a)

def legend(ctx, x, y, a=1.0, size=None):
    if a <= 0: return
    size = size or 32 * U
    font(ctx, size); w1 = ctx.text_extents("PARTY A").width
    gap = 70 * U
    tot = size * 1.2 + w1 + gap + size * 1.2 + ctx.text_extents("PARTY B").width
    x0 = x - tot / 2
    circle(ctx, x0 + size * 0.4, y, size * 0.4, PA, a); text(ctx, "PARTY A", x0 + size * 1.1, y, size, PA, a, True, "l")
    x1 = x0 + size * 1.2 + w1 + gap
    circle(ctx, x1 + size * 0.4, y, size * 0.4, PB, a); text(ctx, "PARTY B", x1 + size * 1.1, y, size, PB, a, True, "l")

# ---------- hemicycle (seats) ----------
_SEATS = {}
def seat_layout(n, rows):
    key = (n, rows)
    if key in _SEATS: return _SEATS[key]
    rs = [0.42 + 0.58 * k / (rows - 1) for k in range(rows)]
    tot = sum(rs)
    counts = [max(2, int(round(n * r / tot))) for r in rs]
    counts[-1] += n - sum(counts)
    pts = []
    for r, c in zip(rs, counts):
        for j in range(c):
            ang = math.pi - j * math.pi / (c - 1)
            pts.append((ang, r))
    pts.sort(key=lambda p: (-p[0], p[1]))
    _SEATS[key] = (pts, math.pi * tot / n)
    return _SEATS[key]

def hemicycle(ctx, cx, cy, R, n, rows, colors, appear=1.0, a=1.0, t=0.0, pulse=None):
    """colors: function(i) -> color for seat i (0 = far left)."""
    pts, spacing = seat_layout(n, rows)
    dr = spacing * R * 0.36
    # floor
    ctx.new_path(); ctx.arc(cx, cy, R * 1.08, math.pi, 2 * math.pi); ctx.close_path()
    g = cairo.RadialGradient(cx, cy, R * 0.2, cx, cy, R * 1.1)
    g.add_color_stop_rgba(0, 0.16, 0.22, 0.42, 0.55 * a); g.add_color_stop_rgba(1, 0.08, 0.11, 0.24, 0.25 * a)
    ctx.set_source(g); ctx.fill()
    for i, (ang, r) in enumerate(pts):
        k = clamp((appear * n - i) / 6.0)
        if k <= 0: continue
        x = cx + math.cos(ang) * r * R; y = cy - math.sin(ang) * r * R
        c = colors(i)
        rr = dr * (0.6 + 0.4 * ease(k))
        if pulse is not None and pulse(i):
            glow(ctx, x, y, rr * 3.0, c, 0.35 * a)
            rr *= 1.0 + 0.12 * math.sin(t * 5 + i * 0.3)
        circle(ctx, x, y + rr * 0.18, rr, (0, 0, 0), 0.35 * a * k)
        circle(ctx, x, y, rr, c, a * k)
        circle(ctx, x - rr * 0.3, y - rr * 0.3, rr * 0.3, WHITE, 0.25 * a * k)

def split_colors(n, nA, nB=0, mid=SEAT):
    return lambda i: PA if i < nA else (PB if i >= n - nB else mid)

# ---------- buildings & objects ----------
def capitol(ctx, x, y, s, a=1.0, t=0.0):
    """Generic domed legislature, base centered at (x, y), width ~ 3.2 s."""
    if a <= 0: return
    glow(ctx, x, y - s * 1.2, s * 2.2, (0.6, 0.75, 1.0), 0.18 * a)
    def fillg(y0, y1):
        g = cairo.LinearGradient(0, y0, 0, y1)
        g.add_color_stop_rgba(0, STONE[0], STONE[1], STONE[2], a); g.add_color_stop_rgba(1, STONE_D[0], STONE_D[1], STONE_D[2], a)
        ctx.set_source(g); ctx.fill()
    # steps
    for i in range(4):
        ww = s * (3.2 - i * 0.12); ctx.rectangle(x - ww / 2, y - s * 0.06 * (i + 1), ww, s * 0.06); fillg(y - s * 0.3, y)
    yb = y - s * 0.24
    # wings
    for sgn in (-1, 1):
        wx = x + sgn * s * 1.05
        ctx.rectangle(wx - s * 0.5, yb - s * 0.62, s * 1.0, s * 0.62); fillg(yb - s * 0.7, yb)
        ctx.rectangle(wx - s * 0.54, yb - s * 0.7, s * 1.08, s * 0.08); fillg(yb - s * 0.7, yb)
        for j in range(6):
            cx_ = wx - s * 0.4 + j * s * 0.16
            ctx.rectangle(cx_ - s * 0.025, yb - s * 0.58, s * 0.05, s * 0.5); rgba(ctx, (0.55, 0.6, 0.74), a); ctx.fill()
        for j in range(5):  # windows
            ctx.rectangle(wx - s * 0.34 + j * s * 0.16, yb - s * 0.42, s * 0.05, s * 0.12); rgba(ctx, (1.0, 0.86, 0.5), a * (0.55 + 0.35 * math.sin(t * 1.3 + j + sgn)))
            ctx.fill()
    # central block + pediment
    ctx.rectangle(x - s * 0.55, yb - s * 0.85, s * 1.1, s * 0.85); fillg(yb - s * 0.9, yb)
    for j in range(8):
        cx_ = x - s * 0.45 + j * s * 0.128
        ctx.rectangle(cx_ - s * 0.025, yb - s * 0.75, s * 0.05, s * 0.68); rgba(ctx, (0.55, 0.6, 0.74), a); ctx.fill()
    ctx.move_to(x - s * 0.62, yb - s * 0.85); ctx.line_to(x, yb - s * 1.12); ctx.line_to(x + s * 0.62, yb - s * 0.85); ctx.close_path(); fillg(yb - s * 1.12, yb - s * 0.85)
    # drum
    ctx.rectangle(x - s * 0.46, yb - s * 1.45, s * 0.92, s * 0.36); fillg(yb - s * 1.45, yb - s * 1.1)
    for j in range(9):
        cx_ = x - s * 0.4 + j * s * 0.1
        ctx.rectangle(cx_ - s * 0.018, yb - s * 1.42, s * 0.036, s * 0.3); rgba(ctx, (0.55, 0.6, 0.74), a); ctx.fill()
    # dome
    ctx.save(); ctx.translate(x, yb - s * 1.45); ctx.scale(s * 0.44, s * 0.5)
    ctx.arc(0, 0, 1, math.pi, 2 * math.pi); ctx.restore(); fillg(yb - s * 1.95, yb - s * 1.45)
    ctx.set_line_width(2.5 * U); rgba(ctx, STONE_D, a)
    for j in range(1, 6):
        ang = math.pi + j * math.pi / 6
        ctx.save(); ctx.translate(x, yb - s * 1.45); ctx.scale(s * 0.44, s * 0.5)
        ctx.move_to(math.cos(ang), math.sin(ang)); ctx.restore()
        ctx.line_to(x, yb - s * 1.95); ctx.stroke()
    # lantern
    ctx.rectangle(x - s * 0.06, yb - s * 2.12, s * 0.12, s * 0.18); fillg(yb - s * 2.12, yb - s * 1.94)
    ctx.move_to(x - s * 0.08, yb - s * 2.12); ctx.line_to(x, yb - s * 2.24); ctx.line_to(x + s * 0.08, yb - s * 2.12); ctx.close_path(); fillg(yb - s * 2.24, yb - s * 2.1)
    glow(ctx, x, yb - s * 2.05, s * 0.25, GOLD, (0.35 + 0.2 * math.sin(t * 2)) * a)

def doc(ctx, x, y, w, a=1.0, ang=0.0, stamp=None, stamp_c=MAJ, sk=1.0, title="BRIDGE REPAIR ACT"):
    if a <= 0: return
    h = w * 1.3
    ctx.save(); ctx.translate(x, y); ctx.rotate(ang)
    rrect(ctx, -w / 2 + 6 * U, -h / 2 + 10 * U, w, h, w * 0.05); rgba(ctx, (0, 0, 0), 0.35 * a); ctx.fill()
    rrect(ctx, -w / 2, -h / 2, w, h, w * 0.05); rgba(ctx, PAPER, a); ctx.fill()
    text(ctx, "FICTIONAL BILL", 0, -h * 0.4, w * 0.065, (0.45, 0.45, 0.5), a, False)
    font(ctx, w * 0.1); tw = ctx.text_extents(title).width
    text(ctx, title, 0, -h * 0.3, w * 0.1 * min(1, w * 0.86 / max(tw, 1)), INK, a)
    # tiny bridge
    ctx.set_line_width(w * 0.025); rgba(ctx, (0.2, 0.4, 0.7), a)
    ctx.new_path(); ctx.arc(0, -h * 0.02, w * 0.28, math.pi * 1.1, math.pi * 1.9); ctx.stroke()
    ctx.move_to(-w * 0.36, -h * 0.08); ctx.line_to(w * 0.36, -h * 0.08); ctx.stroke()
    for j in range(5):
        xx = -w * 0.2 + j * w * 0.1
        ctx.move_to(xx, -h * 0.08); ctx.line_to(xx, -h * 0.02 - math.sqrt(max(0, (w * 0.28) ** 2 - xx * xx)) * 0.8 + w * 0.0); ctx.stroke()
    for j in range(4):
        ctx.rectangle(-w * 0.36, h * 0.06 + j * h * 0.08, w * (0.72 if j < 3 else 0.45), h * 0.02); rgba(ctx, (0.6, 0.62, 0.7), a); ctx.fill()
    if stamp and sk > 0:
        ctx.save(); ctx.rotate(-0.25); s = 1.6 - 0.6 * ease(sk); ctx.scale(s, s)
        font(ctx, w * 0.16); sw = ctx.text_extents(stamp).width + w * 0.12
        ctx.set_line_width(w * 0.03); rgba(ctx, stamp_c, a * ease(sk))
        rrect(ctx, -sw / 2, h * 0.12 - w * 0.13, sw, w * 0.26, w * 0.04); ctx.stroke()
        text(ctx, stamp, 0, h * 0.12, w * 0.16, stamp_c, a * ease(sk))
        ctx.restore()
    ctx.restore()

def door(ctx, x, y, w, h, label, c=WHITE, openk=0.0, a=1.0, lock=True):
    """Double door, base at (x, y)."""
    if a <= 0: return
    glow(ctx, x, y - h / 2, w * 1.1, c, 0.15 * a + 0.25 * openk * a)
    rrect(ctx, x - w / 2 - 14 * U, y - h - 14 * U, w + 28 * U, h + 14 * U, 16 * U); rgba(ctx, (0.25, 0.3, 0.48), a); ctx.fill()
    # light inside
    ctx.rectangle(x - w / 2, y - h, w, h); rgba(ctx, mix((0.03, 0.04, 0.1), (1.0, 0.9, 0.6), openk), a); ctx.fill()
    lw = (w / 2) * (1 - 0.85 * openk)
    for sgn in (-1, 1):
        x0 = x - w / 2 if sgn < 0 else x + w / 2 - lw
        g = cairo.LinearGradient(x0, 0, x0 + lw, 0)
        g.add_color_stop_rgba(0, 0.45, 0.32, 0.2, a); g.add_color_stop_rgba(1, 0.62, 0.45, 0.28, a)
        ctx.rectangle(x0, y - h, lw, h); ctx.set_source(g); ctx.fill()
        ctx.set_line_width(3 * U); rgba(ctx, (0.3, 0.2, 0.12), a)
        ctx.rectangle(x0 + lw * 0.15, y - h * 0.9, lw * 0.7, h * 0.35); ctx.stroke()
        ctx.rectangle(x0 + lw * 0.15, y - h * 0.48, lw * 0.7, h * 0.38); ctx.stroke()
    if lock and openk < 0.5:
        la = a * (1 - openk * 2)
        lx, ly = x, y - h * 0.52
        ctx.new_path(); ctx.arc(lx, ly - 22 * U, 20 * U, math.pi, 2 * math.pi); ctx.set_line_width(8 * U); rgba(ctx, GOLD, la); ctx.stroke()
        rrect(ctx, lx - 30 * U, ly - 22 * U, 60 * U, 50 * U, 8 * U); rgba(ctx, GOLD, la); ctx.fill()
        circle(ctx, lx, ly + 2 * U, 7 * U, (0.4, 0.3, 0.1), la)
    text(ctx, label, x, y + 44 * U, 36 * U, c, a)

def seal(ctx, x, y, r, c=GOLD, a=1.0, label="PRESIDENT", t=0.0):
    if a <= 0: return
    glow(ctx, x, y, r * 1.8, c, 0.25 * a)
    circle(ctx, x, y + r * 0.08, r, (0, 0, 0), 0.35 * a)
    circle(ctx, x, y, r, PANEL, a)
    ctx.new_path(); ctx.arc(x, y, r, 0, 2 * math.pi); ctx.set_line_width(r * 0.09); rgba(ctx, c, a); ctx.stroke()
    ctx.new_path(); ctx.arc(x, y, r * 0.8, 0, 2 * math.pi); ctx.set_line_width(r * 0.025); ctx.stroke()
    for i in range(12):
        ang = i / 12 * 2 * math.pi + t * 0.15
        star5(ctx, x + math.cos(ang) * r * 0.9, y + math.sin(ang) * r * 0.9, r * 0.05, c, a)
    star5(ctx, x, y - r * 0.08, r * 0.42, c, a)
    if label: text(ctx, label, x, y + r + 38 * U, 34 * U, c, a)

def check(ctx, x, y, s, c=MAJ, a=1.0):
    if a <= 0: return
    circle(ctx, x, y, s, c, a)
    ctx.set_line_width(s * 0.22); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_join(cairo.LINE_JOIN_ROUND); rgba(ctx, NAVY, a)
    ctx.move_to(x - s * 0.45, y); ctx.line_to(x - s * 0.1, y + s * 0.38); ctx.line_to(x + s * 0.5, y - s * 0.38); ctx.stroke()

def cross(ctx, x, y, s, c=CORAL, a=1.0):
    if a <= 0: return
    circle(ctx, x, y, s, c, a)
    ctx.set_line_width(s * 0.22); ctx.set_line_cap(cairo.LINE_CAP_ROUND); rgba(ctx, NAVY, a)
    ctx.move_to(x - s * 0.4, y - s * 0.4); ctx.line_to(x + s * 0.4, y + s * 0.4); ctx.stroke()
    ctx.move_to(x + s * 0.4, y - s * 0.4); ctx.line_to(x - s * 0.4, y + s * 0.4); ctx.stroke()

def calendar(ctx, x, y, w, month, year, first_dow, ndays, mark, a=1.0, mk=1.0, c=GOLD, t=0.0):
    """Month page centered at (x, y). first_dow: 0 = Sunday."""
    if a <= 0: return
    h = w * 1.0
    rrect(ctx, x - w / 2 + 8 * U, y - h / 2 + 12 * U, w, h, w * 0.05); rgba(ctx, (0, 0, 0), 0.35 * a); ctx.fill()
    rrect(ctx, x - w / 2, y - h / 2, w, h, w * 0.05); rgba(ctx, PAPER, a); ctx.fill()
    ctx.save(); rrect(ctx, x - w / 2, y - h / 2, w, h, w * 0.05); ctx.clip()
    ctx.rectangle(x - w / 2, y - h / 2, w, h * 0.2); rgba(ctx, c, a); ctx.fill(); ctx.restore()
    text(ctx, month + " " + year, x, y - h * 0.4, w * 0.085, NAVY, a)
    cw = w * 0.86 / 7; x0 = x - w * 0.43 + cw / 2; y0 = y - h * 0.22
    for i, dn in enumerate("SMTWTFS"):
        text(ctx, dn, x0 + i * cw, y0, w * 0.045, (0.45, 0.45, 0.55), a)
    for dday in range(1, ndays + 1):
        idx = first_dow + dday - 1; r_, c_ = divmod(idx, 7)
        dx, dy = x0 + c_ * cw, y0 + (r_ + 1) * cw * 0.95
        if dday == mark and mk > 0:
            circle(ctx, dx, dy, cw * 0.46 * (0.6 + 0.4 * ease(mk)) * (1 + 0.05 * math.sin(t * 4)), CORAL, a * ease(mk))
            text(ctx, str(dday), dx, dy, w * 0.05, WHITE, a)
        else:
            text(ctx, str(dday), dx, dy, w * 0.05, INK, a, False)

def panel(ctx, x, y, w, h, a=1.0, border=(0.3, 0.4, 0.7)):
    if a <= 0: return
    rrect(ctx, x - w / 2, y - h / 2, w, h, 26 * U); rgba(ctx, PANEL, 0.82 * a); ctx.fill()
    ctx.set_line_width(3 * U); rgba(ctx, border, 0.9 * a); rrect(ctx, x - w / 2, y - h / 2, w, h, 26 * U); ctx.stroke()

def ballot_box(ctx, x, y, s, a=1.0, t=0.0):
    if a <= 0: return
    for j in range(3):
        k = (t * 0.7 + j / 3) % 1
        bx, by = x + (j - 1) * s * 0.12, y - s * 1.1 + k * s * 0.6
        ctx.save(); ctx.translate(bx, by); ctx.rotate(0.15 * math.sin(k * 6 + j))
        ctx.rectangle(-s * 0.2, -s * 0.13, s * 0.4, s * 0.26); rgba(ctx, PAPER, a * (1 - k)); ctx.fill()
        check(ctx, 0, 0, s * 0.07, MAJ, a * (1 - k)); ctx.restore()
    ctx.move_to(x - s * 0.55, y - s * 0.6); ctx.line_to(x + s * 0.55, y - s * 0.6); ctx.line_to(x + s * 0.5, y + s * 0.4); ctx.line_to(x - s * 0.5, y + s * 0.4); ctx.close_path()
    g = cairo.LinearGradient(x - s * 0.5, 0, x + s * 0.5, 0)
    g.add_color_stop_rgba(0, 0.22, 0.32, 0.6, a); g.add_color_stop_rgba(1, 0.12, 0.18, 0.4, a); ctx.set_source(g); ctx.fill()
    ctx.rectangle(x - s * 0.6, y - s * 0.7, s * 1.2, s * 0.12); rgba(ctx, (0.3, 0.42, 0.75), a); ctx.fill()
    ctx.rectangle(x - s * 0.25, y - s * 0.66, s * 0.5, s * 0.04); rgba(ctx, NAVY, a); ctx.fill()
    star5(ctx, x, y - s * 0.1, s * 0.2, WHITE, a)
    text(ctx, "VOTE", x, y + s * 0.2, s * 0.16, WHITE, a)

# ---------- scenes ----------
def sc_hook(ctx, t, d):
    bg(ctx, t)
    cx, cy = P(0.5, 0.78, 0.5, 0.62)
    s = 300 * U if not VERT else 290 * U
    capitol(ctx, cx, cy, s, prog(t, 0, 0.8), t)
    bx, by = P(0.12, 0.76, 0.2, 0.64)
    if not VERT: ballot_box(ctx, bx, by, 170 * U, prog(t, 0.3, 1.0), t)
    k1 = prog(t, 0.6, 1.4) * (1 - prog(t, d * 0.42, d * 0.5))
    if not VERT:
        text(ctx, "NO PRESIDENT ON THE BALLOT…", CX, H * 0.12, 64 * U, WHITE, k1)
    else:
        pass
    k2 = prog(t, d * 0.45, d * 0.55)
    if k2:
        lx, rx, py = (W * 0.17, W * 0.83, H * 0.3) if not VERT else (W * 0.27, W * 0.73, H * 0.62 - 0 * U)
        if VERT: py = cy + 70 * U
        pill(ctx, "NEW LAWS", lx, py, 52 * U if not VERT else 44 * U, MAJ, k2)
        if VERT: text(ctx, "or", CX, py, 40 * U, WHITE, k2)
        pill(ctx, "GRIDLOCK", rx, py, 52 * U if not VERT else 44 * U, CORAL, prog(t, d * 0.55, d * 0.65))
    chip(ctx, "US MIDTERMS EXPLAINED", t)

def sc_calendar(ctx, t, d):
    bg(ctx, t)
    # 4-year term bar
    x0, x1 = (W * 0.1, W * 0.9) if not VERT else (W * 0.08, W * 0.92)
    yb = H * 0.24 if not VERT else H * 0.2
    k = prog(t, 0.3, 2.5)
    rrect(ctx, x0, yb - 26 * U, (x1 - x0), 52 * U, 26 * U); rgba(ctx, (0.18, 0.24, 0.45)); ctx.fill()
    rrect(ctx, x0, yb - 26 * U, (x1 - x0) * k, 52 * U, 26 * U); rgba(ctx, PA, 0.9); ctx.fill()
    for i in range(5):
        xx = x0 + (x1 - x0) * i / 4
        ctx.rectangle(xx - 2 * U, yb - 40 * U, 4 * U, 80 * U); rgba(ctx, WHITE, 0.7); ctx.fill()
    for i in range(4):
        text(ctx, "YEAR %d" % (i + 1), x0 + (x1 - x0) * (i + 0.5) / 4, yb + 70 * U, 32 * U, WHITE, 0.85)
    text(ctx, "PRESIDENT'S 4-YEAR TERM", CX, yb - 80 * U, 40 * U, PA, prog(t, 0.2, 1.0))
    m = prog(t, d * 0.2, d * 0.3)
    if m:
        mx = x0 + (x1 - x0) * 0.5
        glow(ctx, mx, yb, 120 * U, CORAL, 0.5 * m)
        star5(ctx, mx, yb, 46 * U * m, CORAL, m, t * 0.5)
        pill(ctx, "MIDTERM", mx, yb + 140 * U, 40 * U, CORAL, m)
    c = prog(t, d * 0.38, d * 0.5)
    cx, cy = P(0.33, 0.6, 0.5, 0.5)
    cw = 470 * U if not VERT else 560 * U
    if not VERT: cy = H * 0.62
    calendar(ctx, cx, cy + (1 - c) * 60 * U, cw, "NOVEMBER", "2026", 0, 30, 3, c, prog(t, d * 0.55, d * 0.65), CORAL, t)
    r = prog(t, d * 0.6, d * 0.7)
    if r and not VERT:
        bigtext(ctx, "NOV 3", W * 0.72, H * 0.56, 150 * U, CORAL, r)
        text(ctx, "Tuesday after the first Monday", W * 0.72, H * 0.68, 36 * U, WHITE, r, False)
    chip(ctx, "WHY \"MIDTERMS\"?", t)

def sc_capitol(ctx, t, d):
    bg(ctx, t)
    ph = prog(t, d * 0.58, d * 0.68)
    cx, cy = P(0.5, 0.74, 0.5, 0.5)
    s = (400 if not VERT else 300) * U * (1 - 0.35 * ph)
    capitol(ctx, cx, cy - ph * (60 * U), s, 1 - 0.75 * ph, t)
    a1 = prog(t, d * 0.15, d * 0.25) * (1 - ph)
    if a1:
        lx, rx = cx - s * 1.05, cx + s * 1.05
        ly = cy - s * 1.2
        pill(ctx, "HOUSE", lx, ly - 40 * U, 44 * U, PB, a1); arrow(ctx, lx, ly - 5 * U, lx, ly + 60 * U, PB, a1)
        pill(ctx, "SENATE", rx, ly - 40 * U, 44 * U, PA, prog(t, d * 0.22, d * 0.3) * (1 - ph)); arrow(ctx, rx, ly - 5 * U, rx, ly + 60 * U, PA, prog(t, d * 0.22, d * 0.3) * (1 - ph))
        text(ctx, "CONGRESS", CX, H * 0.12 if not VERT else H * 0.18, 70 * U, WHITE, a1)
        text(ctx, "WRITES THE LAWS · CONTROLS THE MONEY", CX, (H * 0.12 + 80 * U) if not VERT else H * 0.18 + 80 * U, 34 * U if not VERT else 30 * U, GOLD, prog(t, d * 0.12, d * 0.2) * (1 - ph))
    if ph:
        dw, dh = (300 * U, 420 * U) if not VERT else (300 * U, 420 * U)
        p1 = P(0.3, 0.72, 0.28, 0.62); p2 = P(0.7, 0.72, 0.72, 0.62)
        o1 = prog(t, d * 0.8, d * 0.88); o2 = prog(t, d * 0.88, d * 0.96)
        door(ctx, p1[0], p1[1], dw, dh, "HOUSE", PB, o1, ph)
        door(ctx, p2[0], p2[1], dw, dh, "SENATE", PA, o2, ph)
        # bill travelling between doors
        bx = p1[0] - 260 * U + (p2[0] - p1[0] + 260 * U) * prog(t, d * 0.72, d * 0.98)
        if not VERT: doc(ctx, bx, p1[1] - dh - 120 * U, 150 * U, ph, math.sin(t * 2) * 0.08)
        else: doc(ctx, bx, p1[1] - dh - 140 * U, 160 * U, ph, math.sin(t * 2) * 0.08)
        text(ctx, "TWO KEYS NEEDED", CX, H * 0.14 if not VERT else H * 0.16, 60 * U, WHITE, ph)

def sc_house(ctx, t, d):
    bg(ctx, t, tint=(0.05, 0.12, 0.24))
    cx, cy = P(0.5, 0.74, 0.5, 0.5)
    R = 560 * U if not VERT else 470 * U
    ap = prog(t, 0.2, d * 0.45)
    mk = prog(t, d * 0.78, d * 0.9)
    nM = int(218 * mk)
    hemicycle(ctx, cx, cy, R, 435, 11, lambda i: MAJ if i < nM else mix(SEAT, PB, 0.35), ap, 1, t,
              pulse=(lambda i: i < nM) if mk >= 1 else None)
    yc = cy - 110 * U
    if mk < 0.05:
        counter(ctx, 435 * ap, cx, yc, 170 * U if not VERT else 150 * U, WHITE, prog(t, 0.2, 1.0))
        text(ctx, "VOTING SEATS", cx, yc + 105 * U, 34 * U, (0.7, 0.8, 1.0), prog(t, 0.4, 1.2))
    else:
        counter(ctx, 218 * mk, cx, yc, 170 * U if not VERT else 150 * U, MAJ, mk)
        text(ctx, "SEATS FOR A MAJORITY", cx, yc + 105 * U, 34 * U, MAJ, mk)
    p = prog(t, d * 0.55, d * 0.62)
    py = H * 0.12 if not VERT else H * 0.18
    pill(ctx, "2-YEAR TERMS · ALL SEATS UP", CX, py, 40 * U if not VERT else 36 * U, PB, p)
    # state chips: big vs small states
    s = prog(t, d * 0.25, d * 0.33) * (1 - p)
    if s:
        pill(ctx, "CALIFORNIA: 52", CX - (300 * U if not VERT else 230 * U), py, 36 * U, WHITE, s)
        pill(ctx, "SMALL STATES: 1", CX + (300 * U if not VERT else 230 * U), py, 36 * U, WHITE, prog(t, d * 0.3, d * 0.38) * (1 - p))
    chip(ctx, "THE HOUSE", t)

def sc_senate(ctx, t, d):
    bg(ctx, t, tint=(0.12, 0.10, 0.22))
    cx, cy = P(0.5, 0.74, 0.5, 0.5)
    R = 540 * U if not VERT else 460 * U
    ap = prog(t, 0.2, d * 0.25)
    m = prog(t, d * 0.5, d * 0.6)
    tie = prog(t, d * 0.75, d * 0.82)
    if tie:
        cols = split_colors(100, 50, 50)
    else:
        nM = int(51 * m)
        cols = lambda i: MAJ if i < nM else mix(SEAT, PA, 0.3)
    hemicycle(ctx, cx, cy, R, 100, 5, cols, ap, 1, t)
    yc = cy - 100 * U
    if tie:
        rrect(ctx, cx - 210 * U, yc - 125 * U, 420 * U, 130 * U, 30 * U); rgba(ctx, NAVY, 0.85 * tie); ctx.fill()
        bigtext(ctx, "50 – 50", cx, yc - 60 * U, 100 * U, WHITE, tie)
        legend(ctx, CX, H * 0.2 if not VERT else H * 0.25, tie, 30 * U)
        vk = prog(t, d * 0.84, d * 0.92)
        seal(ctx, cx, cy - 50 * U, 50 * U, MAJ, vk, None, t)
        pill(ctx, "VICE PRESIDENT BREAKS THE TIE", CX, H * 0.12 if not VERT else H * 0.18, 40 * U if not VERT else 34 * U, MAJ, vk)
    elif m < 0.05:
        counter(ctx, 100 * ap, cx, yc, 170 * U, WHITE, prog(t, 0.2, 1.0))
        text(ctx, "SENATORS · 2 PER STATE", cx, yc + 100 * U, 34 * U, (0.9, 0.85, 1.0), prog(t, 0.4, 1.2))
        p = prog(t, d * 0.3, d * 0.38)
        pill(ctx, "6-YEAR TERMS · ~1/3 UP EACH TIME", CX, H * 0.12 if not VERT else H * 0.18, 40 * U if not VERT else 34 * U, PA, p)
    else:
        counter(ctx, 51 * m, cx, yc, 170 * U, MAJ, m)
        text(ctx, "FOR A CLEAR MAJORITY", cx, yc + 100 * U, 34 * U, MAJ, m)
    chip(ctx, "THE SENATE", t)

def sc_myth(ctx, t, d):
    bg(ctx, t)
    cx, cy = P(0.3, 0.7, 0.5, 0.4)
    R = 400 * U if not VERT else 400 * U
    up = prog(t, d * 0.3, d * 0.4)
    random.seed(9); upset = set(random.sample(range(100), 34))
    hemicycle(ctx, cx, cy, R, 100, 5, lambda i: (WHITE if i in upset else (0.25, 0.28, 0.4)) if up else SEAT, 1, 1, t,
              pulse=(lambda i: i in upset) if up else None)
    if up:
        text(ctx, "~1/3 OF THE SENATE", cx, cy + 50 * U, 36 * U, WHITE, up)
        text(ctx, "~2/3 KEEP THEIR SEATS", cx, cy + 100 * U, 30 * U, (0.6, 0.65, 0.8), up, False)
    mk = prog(t, 0.3, 1.2) * (1 - prog(t, d * 0.28, d * 0.33))
    if mk:
        ty = H * 0.14 if not VERT else H * 0.15
        text(ctx, "\"THE WHOLE CONGRESS IS REPLACED\"", CX, ty, 48 * U if not VERT else 38 * U, WHITE, mk)
        st = prog(t, 1.6, 2.2)
        if st:
            ctx.save(); ctx.translate(CX, ty + 90 * U); ctx.rotate(-0.12); sc = 1.5 - 0.5 * st; ctx.scale(sc, sc)
            ctx.set_line_width(6 * U); rgba(ctx, CORAL, mk * st); rrect(ctx, -130 * U, -45 * U, 260 * U, 90 * U, 12 * U); ctx.stroke()
            text(ctx, "MYTH", 0, 0, 64 * U, CORAL, mk * st); ctx.restore()
    items = ["GOVERNORS", "STATE LAWMAKERS", "JUDGES", "LOCAL OFFICIALS"]
    lx, ly = P(0.74, 0.3, 0.5, 0.52)
    for i, it in enumerate(items):
        k = prog(t, d * 0.5 + i * 0.6, d * 0.5 + i * 0.6 + 0.6)
        if not k: continue
        if VERT:
            x = W * (0.28 if i % 2 == 0 else 0.72); y = ly + (i // 2) * 90 * U
            pill(ctx, it, x + (1 - k) * 40 * U, y, 30 * U, [PA, PB, MAJ, CORAL][i], k)
        else:
            y = ly + i * 110 * U
            pill(ctx, it, lx + (1 - k) * 60 * U, y, 40 * U, [PA, PB, MAJ, CORAL][i], k)
    tk = prog(t, d * 0.82, d * 0.9)
    if tk and not VERT:
        text(ctx, "SAME DAY, SAME BALLOT", lx, ly + 470 * U, 34 * U, WHITE, tk)
    chip(ctx, "COMMON MISCONCEPTION", t)

def bill_path_nodes():
    if VERT:
        return [(CX, H * 0.2), (CX, H * 0.36), (CX, H * 0.52)]
    return [(W * 0.25, H * 0.5), (W * 0.5, H * 0.5), (W * 0.76, H * 0.5)]

def sc_bill(ctx, t, d):
    bg(ctx, t)
    nodes = bill_path_nodes()
    labels = ["1 · HOUSE", "2 · SENATE", "3 · PRESIDENT"]
    cols = [PB, PA, MAJ]
    for i in range(2):
        (x1, y1), (x2, y2) = nodes[i], nodes[i + 1]
        k = prog(t, d * 0.25 + i * d * 0.15, d * 0.35 + i * d * 0.15)
        ctx.set_line_width(6 * U); ctx.set_dash([14 * U, 12 * U], -t * 40 * U); rgba(ctx, WHITE, 0.3)
        ctx.move_to(x1, y1); ctx.line_to(x2, y2); ctx.stroke(); ctx.set_dash([])
    for i, (x, y) in enumerate(nodes):
        a = prog(t, d * (0.2 + 0.15 * i), d * (0.26 + 0.15 * i))
        if i < 2:
            nd = 140 if not VERT else 110
            hemicycle(ctx, x, y + nd * 0.45 * U, nd * U, 60 if i == 0 else 30, 4 if i == 0 else 3, lambda j, c=cols[i]: c, a, a, t)
        else:
            seal(ctx, x, y, (95 if not VERT else 75) * U, MAJ, a, None, t)
        if not VERT: text(ctx, labels[i], x, y + 170 * U, 38 * U, cols[i], a)
        else: text(ctx, labels[i], x + 300 * U, y, 34 * U, cols[i], a, True, "c")
    # the bill travels
    st = prog(t, d * 0.15, d * 0.22)
    pos = [nodes[0], nodes[0], nodes[1], nodes[2]]
    seg = clamp((t - d * 0.3) / (d * 0.3)) * 2
    i = min(int(seg), 1); f = ease(seg - i) if seg < 2 else 1
    if seg <= 0: bx, by = nodes[0][0] - (0 if VERT else 260 * U), nodes[0][1] - (0 if not VERT else 0)
    else:
        (x1, y1), (x2, y2) = nodes[i], nodes[i + 1] if seg < 2 else nodes[2]
        if seg >= 2: x1, y1 = nodes[2]
        bx, by = x1 + (x2 - x1) * f, y1 + (y2 - y1) * f
    if not VERT: by -= 230 * U
    else: bx -= 300 * U
    fin = prog(t, d * 0.72, d * 0.8)
    doc(ctx, bx, by, 160 * U if not VERT else 140 * U, st * (1 - 0.6 * fin), math.sin(t * 2.2) * 0.06)
    for i in range(2):
        ck = prog(t, d * (0.38 + 0.15 * i), d * (0.42 + 0.15 * i))
        x, y = nodes[i]
        check(ctx, x + (110 if not VERT else 120) * U, y - (110 if not VERT else 40) * U, 30 * U, MAJ, ck)
    if fin:
        if VERT: y = H * 0.64; xs = (W * 0.27, W * 0.73)
        else: y = H * 0.14; xs = (W * 0.32, W * 0.68)
        pill(ctx, "SIGN → LAW", xs[0], y, 44 * U if not VERT else 36 * U, MAJ, fin)
        pill(ctx, "VETO → BACK", xs[1], y, 44 * U if not VERT else 36 * U, CORAL, prog(t, d * 0.85, d * 0.92))
    chip(ctx, "AN IMAGINARY LAW", t)

def sc_filibuster(ctx, t, d):
    bg(ctx, t, tint=(0.12, 0.08, 0.2))
    px, py = P(0.36, 0.72, 0.5, 0.6)
    s = 1.0 if not VERT else 0.9
    # podium
    ctx.move_to(px - 170 * U * s, py); ctx.line_to(px + 170 * U * s, py); ctx.line_to(px + 130 * U * s, py - 320 * U * s); ctx.line_to(px - 130 * U * s, py - 320 * U * s); ctx.close_path()
    g = cairo.LinearGradient(px - 170 * U, 0, px + 170 * U, 0); g.add_color_stop_rgb(0, .45, .3, .2); g.add_color_stop_rgb(1, .3, .2, .13); ctx.set_source(g); ctx.fill()
    ctx.rectangle(px - 180 * U * s, py - 345 * U * s, 360 * U * s, 30 * U * s); rgba(ctx, (0.55, 0.38, 0.25)); ctx.fill()
    star5(ctx, px, py - 170 * U * s, 50 * U * s, GOLD, 0.9)
    # microphone
    ctx.set_line_width(8 * U); rgba(ctx, (0.7, 0.72, 0.8)); ctx.move_to(px, py - 345 * U * s); ctx.line_to(px + 20 * U, py - 430 * U * s); ctx.stroke()
    circle(ctx, px + 22 * U, py - 450 * U * s, 22 * U, (0.8, 0.82, 0.9))
    # growing stack of speech pages
    n = int(3 + 14 * prog(t, 0.5, d * 0.95))
    for i in range(n):
        ctx.rectangle(px - 100 * U * s + math.sin(i * 1.7) * 8 * U, py - 345 * U * s - (i + 1) * 9 * U, 150 * U * s, 8 * U); rgba(ctx, PAPER, 0.95); ctx.fill()
    # speech bubbles
    for j in range(3):
        k = (t * 0.35 + j / 3) % 1
        bx = px + (180 + 160 * k) * U * (1 if not VERT else 0.8); by = py - 500 * U * s - k * 220 * U
        a = math.sin(k * math.pi)
        rrect(ctx, bx - 120 * U, by - 40 * U, 240 * U, 80 * U, 40 * U); rgba(ctx, WHITE, 0.9 * a); ctx.fill()
        text(ctx, ["DEBATE…", "MORE…", "STILL…"][j], bx, by, 32 * U, NAVY, a)
    # clock spinning
    kx, ky = P(0.62, 0.42, 0.78, 0.22)
    r = 130 * U if not VERT else 110 * U
    glow(ctx, kx, ky, r * 1.6, CORAL, 0.25)
    circle(ctx, kx, ky, r, PAPER); ctx.new_path(); ctx.arc(kx, ky, r, 0, 2 * math.pi); ctx.set_line_width(10 * U); rgba(ctx, CORAL); ctx.stroke()
    for i in range(12):
        ang = i / 12 * 2 * math.pi
        ctx.move_to(kx + math.cos(ang) * r * 0.8, ky + math.sin(ang) * r * 0.8); ctx.line_to(kx + math.cos(ang) * r * 0.9, ky + math.sin(ang) * r * 0.9)
    ctx.set_line_width(4 * U); rgba(ctx, INK); ctx.stroke()
    for (ln, sp, wd) in [(0.5, 1.2, 10), (0.75, 9.0, 6)]:
        ang = t * sp - math.pi / 2
        ctx.set_line_width(wd * U); ctx.set_line_cap(cairo.LINE_CAP_ROUND); rgba(ctx, INK)
        ctx.move_to(kx, ky); ctx.line_to(kx + math.cos(ang) * r * ln, ky + math.sin(ang) * r * ln); ctx.stroke()
    # bill stuck at a barrier
    bk = prog(t, d * 0.55, d * 0.65)
    if bk:
        gx, gy = P(0.86, 0.5, 0.5, 0.15)
        if VERT: gx, gy = W * 0.26, H * 0.24
        doc(ctx, gx - 60 * U, gy, 130 * U, bk, -0.1 + 0.03 * math.sin(t * 8))
        ctx.save(); ctx.translate(gx + 40 * U, gy);
        for i in range(5):
            ctx.rectangle(-150 * U + i * 60 * U, -14 * U, 60 * U, 28 * U); rgba(ctx, CORAL if i % 2 == 0 else WHITE, bk); ctx.fill()
        ctx.restore()
        text(ctx, "NO FINAL VOTE", gx, gy + 140 * U if not VERT else gy + 130 * U, 38 * U, CORAL, bk)
    tk = prog(t, d * 0.25, d * 0.35)
    if not VERT: bigtext(ctx, "FILIBUSTER", W * 0.76, H * 0.13, 96 * U, CORAL, tk)
    else: bigtext(ctx, "FILIBUSTER", CX, H * 0.36 + 30 * U, 90 * U, CORAL, tk)
    chip(ctx, "THE SENATE'S TWIST", t)

def sc_sixty(ctx, t, d):
    bg(ctx, t, tint=(0.12, 0.08, 0.2))
    cx, cy = P(0.5, 0.76, 0.5, 0.5)
    R = 560 * U if not VERT else 470 * U
    k51 = prog(t, 0.2, d * 0.2)
    k60 = prog(t, d * 0.3, d * 0.45)
    n = 51 * k51 + 9 * k60
    hemicycle(ctx, cx, cy, R, 100, 5, lambda i: (MAJ if i < 51 else GOLD) if i < n else SEAT, 1, 1, t,
              pulse=(lambda i: i < 60) if k60 >= 1 else None)
    yc = cy - 150 * U
    if k60 < 0.02:
        counter(ctx, 51 * k51, cx, yc, 180 * U, MAJ, k51)
        cross(ctx, cx + 210 * U, yc - 60 * U, 44 * U, CORAL, prog(t, d * 0.18, d * 0.24))
        text(ctx, "NOT ENOUGH", cx, yc + 105 * U, 36 * U, CORAL, prog(t, d * 0.18, d * 0.24))
    else:
        counter(ctx, 51 + 9 * k60, cx, yc, 190 * U, GOLD, 1)
        text(ctx, "VOTES FOR MOST LAWS", cx, yc + 105 * U, 34 * U, GOLD, k60)
    e = prog(t, d * 0.55, d * 0.65)
    pill(ctx, "EXCEPTION: SOME BUDGET BILLS", CX, H * 0.12 if not VERT else H * 0.18, 38 * U if not VERT else 32 * U, MAJ, e)
    chip(ctx, "THE MAGIC NUMBER", t)

def gov_panels(ctx, t, d, cP, cH, cS, title, a=1.0):
    """Three panels: President, House, Senate, colored by controlling party."""
    if VERT:
        pos = [(CX, H * 0.2), (W * 0.27, H * 0.43), (W * 0.73, H * 0.43)]
        pw, ph = 460 * U, 300 * U
    else:
        pos = [(W * 0.2, H * 0.47), (W * 0.5, H * 0.47), (W * 0.8, H * 0.47)]
        pw, ph = 520 * U, 420 * U
    names = ["PRESIDENT", "HOUSE", "SENATE"]
    cs = [cP, cH, cS]
    for i, (x, y) in enumerate(pos):
        k = prog(t, 0.2 + i * 0.4, 0.8 + i * 0.4) * a
        if not k: continue
        w_ = pw if not VERT else (pw if i == 0 else 470 * U)
        panel(ctx, x, y + (1 - k) * 40 * U, w_, ph, k, cs[i])
        yy = y + (1 - k) * 40 * U
        if i == 0:
            seal(ctx, x, yy - 20 * U, (110 if not VERT else 80) * U, cs[i], k, None, t)
        else:
            r = (200 if not VERT else 170) * U
            hemicycle(ctx, x, yy + (60 if not VERT else 50) * U, r, 80 if i == 1 else 40, 5 if i == 1 else 3, lambda j, c=cs[i]: c, k, k, t)
        text(ctx, names[i], x, yy + ph / 2 - 40 * U, 34 * U, cs[i], k)
    return pos

def scen_title(ctx, t, title, sub, a=1.0):
    if VERT:
        text(ctx, title, CX, H * 0.07 + 40 * U, 40 * U, WHITE, prog(t, 0, 0.6) * a)
    else:
        text(ctx, title, CX, H * 0.12, 54 * U, WHITE, prog(t, 0, 0.6) * a)
    chip(ctx, sub, t)

def balance(ctx, t, d, left, right, a0, y=None):
    k = prog(t, d * a0, d * a0 + 0.8)
    if not k: return
    y = y or (H * 0.8 - 40 * U if not VERT else H * 0.62)
    if not VERT: y = H * 0.76
    xs = (W * 0.3, W * 0.7) if not VERT else (W * 0.27, W * 0.73)
    sz = 40 * U if not VERT else 32 * U
    pill(ctx, left, xs[0], y, sz, WHITE, k)
    pill(ctx, right, xs[1], y, sz, WHITE, prog(t, d * a0 + 1.2, d * a0 + 2.0))

def sc_unified(ctx, t, d):
    bg(ctx, t)
    pos = gov_panels(ctx, t, d, PA, PA, PA, "")
    scen_title(ctx, t, "UNIFIED GOVERNMENT", "SCENARIO 1")
    lk = prog(t, d * 0.15, d * 0.22)
    if not VERT: legend(ctx, CX, H * 0.2, lk)
    else: legend(ctx, CX, H * 0.07 + 100 * U, lk)
    # bill zooms through
    f = prog(t, d * 0.3, d * 0.55)
    if 0 < f:
        order = [pos[1], pos[2], pos[0]]
        sg = min(int(f * 2), 1); ff = (f * 2) - sg if f < 1 else 1
        (x1, y1), (x2, y2) = order[sg], order[sg + 1]
        bx, by = x1 + (x2 - x1) * ff, y1 + (y2 - y1) * ff - (190 if not VERT else 150) * U
        doc(ctx, bx, by, 110 * U, 1 - prog(t, d * 0.6, d * 0.65), math.sin(t * 3) * 0.1)
    hk = prog(t, d * 0.5, d * 0.58)
    if hk:
        x, y = pos[2]
        pill(ctx, "60-VOTE RULE", x, y - (250 if not VERT else 190) * U, 34 * U if not VERT else 28 * U, CORAL, hk)
    balance(ctx, t, d, "+ DELIVERS PROMISES", "− FEWER CHECKS", 0.75)

def sc_househ(ctx, t, d):
    bg(ctx, t)
    pos = gov_panels(ctx, t, d, PA, PB, PA, "")
    scen_title(ctx, t, "THE HOUSE CHANGES HANDS", "SCENARIO 2")
    lk = prog(t, d * 0.12, d * 0.2)
    if not VERT: legend(ctx, CX, H * 0.2, lk)
    else: legend(ctx, CX, H * 0.07 + 100 * U, lk)
    x, y = pos[1]
    sk = prog(t, d * 0.3, d * 0.36)
    if sk:
        doc(ctx, x, y - (200 if not VERT else 170) * U, 120 * U, sk * (1 - prog(t, d * 0.55, d * 0.6)), 0.05 * math.sin(t * 6), "NOT SCHEDULED", CORAL, prog(t, d * 0.36, d * 0.42))
    ik = prog(t, d * 0.55, d * 0.62)
    if ik:
        mx, my = pos[0]
        mx += math.sin(t * 1.5) * 30 * U
        rr = (70 if not VERT else 55) * U
        ctx.new_path(); ctx.arc(mx + 40 * U, my - 40 * U, rr, 0, 2 * math.pi); ctx.set_line_width(12 * U); rgba(ctx, PB, ik); ctx.stroke()
        ctx.set_line_width(18 * U); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.move_to(mx + 40 * U + rr * 0.7, my - 40 * U + rr * 0.7); ctx.line_to(mx + 40 * U + rr * 1.5, my - 40 * U + rr * 1.5); ctx.stroke()
        pill(ctx, "INVESTIGATIONS", pos[0][0], pos[0][1] - (250 if not VERT else 195) * U, 34 * U if not VERT else 28 * U, PB, ik)
    balance(ctx, t, d, "COMPROMISE?", "GRIDLOCK?", 0.78)

def sc_senateflip(ctx, t, d):
    bg(ctx, t)
    pos = gov_panels(ctx, t, d, PA, PA, PB, "")
    scen_title(ctx, t, "THE SENATE CHANGES HANDS", "SCENARIO 3")
    lk = prog(t, d * 0.12, d * 0.2)
    if not VERT: legend(ctx, CX, H * 0.2, lk)
    else: legend(ctx, CX, H * 0.07 + 100 * U, lk)
    roles = ["JUDGE", "CABINET", "AMBASSADOR"]
    sx, sy = pos[2]
    for i, rl in enumerate(roles):
        k = prog(t, d * 0.3 + i * 0.8, d * 0.3 + i * 0.8 + 1.5)
        if not k: continue
        x0, y0 = pos[0]
        x = x0 + (sx - x0) * k * 0.85; y = y0 - (210 if not VERT else 175) * U - (i - 1) * (0 if VERT else 0) + math.sin(k * math.pi) * -60 * U

        cw, ch = (190 * U, 64 * U) if not VERT else (170 * U, 56 * U)
        yy = y - (2 - i) * (ch + 14 * U)
        rrect(ctx, x - cw / 2, yy - ch / 2, cw, ch, 12 * U); rgba(ctx, PAPER, 0.95 * k); ctx.fill()
        text(ctx, rl, x, yy, 26 * U, INK, k)
    hk = prog(t, d * 0.6, d * 0.68)
    if hk:
        # hourglass (slowed)
        hx, hy = sx + (190 if not VERT else 150) * U, sy - (60 if not VERT else 40) * U
        ctx.save(); ctx.translate(hx, hy); ctx.rotate(math.sin(t * 2) * 0.1)
        ctx.move_to(-40 * U, -60 * U); ctx.line_to(40 * U, -60 * U); ctx.line_to(-40 * U, 60 * U); ctx.line_to(40 * U, 60 * U); ctx.close_path()
        rgba(ctx, GOLD, hk); ctx.set_line_width(7 * U); ctx.stroke(); ctx.restore()
    tk = prog(t, d * 0.82, d * 0.9)
    yb = H * 0.76 if not VERT else H * 0.62
    pill(ctx, "CONFIRMATIONS: SLOWED, CHANGED OR REJECTED", CX, yb - (0 if not VERT else 0), 36 * U if not VERT else 26 * U, PB, prog(t, d * 0.62, d * 0.7) * (1 - tk))
    pill(ctx, "TREATIES NEED 2/3 OF THE SENATE", CX, yb, 40 * U if not VERT else 30 * U, GOLD, tk)

def override_bar(ctx, x, y, w, h, label, need, total, fillk, a=1.0, c=PB):
    if a <= 0: return
    rrect(ctx, x - w / 2, y - h / 2, w, h, h / 2); rgba(ctx, (0.15, 0.2, 0.38), a); ctx.fill()
    fw = w * 0.55 * fillk
    if fw > 1: rrect(ctx, x - w / 2, y - h / 2, max(fw, h), h, h / 2); rgba(ctx, c, a); ctx.fill()
    lx = x - w / 2 + w * 2 / 3
    ctx.set_line_width(5 * U); rgba(ctx, GOLD, a); ctx.move_to(lx, y - h); ctx.line_to(lx, y + h); ctx.stroke()
    text(ctx, "2/3 = %d" % need, lx, y - h - 26 * U, 32 * U, GOLD, a)
    text(ctx, label, x - w / 2, y + h + 30 * U, 30 * U, WHITE, a, True, "l")

def sc_both(ctx, t, d):
    bg(ctx, t)
    ph = prog(t, d * 0.55, d * 0.62)
    pos = gov_panels(ctx, t, d, PA, PB, PB, "", 1 - ph)
    scen_title(ctx, t, "PARTY B WINS BOTH CHAMBERS", "SCENARIO 4", 1 - ph)
    lk = prog(t, d * 0.1, d * 0.18) * (1 - ph)
    if not VERT: legend(ctx, CX, H * 0.2, lk)
    else: legend(ctx, CX, H * 0.07 + 100 * U, lk)
    f = prog(t, d * 0.15, d * 0.3)
    if f and ph < 1:
        (x1, y1), (x2, y2) = pos[2], pos[0]
        vk = prog(t, d * 0.3, d * 0.36)
        bx = x1 + (x2 - x1) * f; by = y1 + (y2 - y1) * f - (200 if not VERT else 170) * U
        doc(ctx, bx, by, 130 * U, 1 - ph, math.sin(t * 3) * 0.08, "VETO", CORAL, vk, "B'S BRIDGE PLAN")
    if ph:
        if VERT: x, y1_, y2_, w = CX, H * 0.36, H * 0.5, 860 * U
        else: x, y1_, y2_, w = CX, H * 0.38, H * 0.6, 1300 * U
        fk = prog(t, d * 0.65, d * 0.85)
        override_bar(ctx, x, y1_, w, 54 * U, "HOUSE (OF 435)", 290, 435, fk, ph)
        override_bar(ctx, x, y2_, w, 54 * U, "SENATE (OF 100)", 67, 100, fk, ph)
        bigtext(ctx, "2/3", x, (H * 0.2 if not VERT else H * 0.22), 140 * U, GOLD, ph)
        pill(ctx, "MOST VETOES STAND", CX, H * 0.76 if not VERT else H * 0.62, 40 * U if not VERT else 34 * U, WHITE, prog(t, d * 0.86, d * 0.93))

def sc_budget(ctx, t, d):
    bg(ctx, t, tint=(0.06, 0.12, 0.2))
    # generic federal building with lights going off
    bx, by = P(0.62, 0.74, 0.5, 0.6)
    s = 1.0 if not VERT else 0.8
    off = prog(t, d * 0.45, d * 0.65)
    ctx.rectangle(bx - 380 * U * s, by - 360 * U * s, 760 * U * s, 360 * U * s); rgba(ctx, (0.75, 0.78, 0.88)); ctx.fill()
    ctx.move_to(bx - 420 * U * s, by - 360 * U * s); ctx.line_to(bx, by - 480 * U * s); ctx.line_to(bx + 420 * U * s, by - 360 * U * s); ctx.close_path(); rgba(ctx, (0.85, 0.87, 0.95)); ctx.fill()
    ctx.rectangle(bx - 440 * U * s, by, 880 * U * s, 30 * U); rgba(ctx, (0.6, 0.63, 0.75)); ctx.fill()
    for r in range(3):
        for c in range(8):
            i = r * 8 + c
            lit = 1 - clamp(off * 26 - (i * 7 % 24))
            x = bx - 330 * U * s + c * 90 * U * s; y = by - 320 * U * s + r * 100 * U * s
            ctx.rectangle(x, y, 50 * U * s, 70 * U * s); rgba(ctx, mix((0.12, 0.15, 0.25), (1.0, 0.88, 0.5), lit)); ctx.fill()
    ck = prog(t, d * 0.65, d * 0.75)
    if ck:
        sx, sy = (bx + 300 * U, by - 30 * U) if not VERT else (bx + 250 * U, by + 10 * U)
        ctx.save(); ctx.translate(sx, sy); ctx.rotate(-0.08 + 0.03 * math.sin(t * 3))
        rrect(ctx, -150 * U, -50 * U, 300 * U, 100 * U, 14 * U); rgba(ctx, CORAL, ck); ctx.fill()
        text(ctx, "CLOSED", 0, 0, 50 * U, WHITE, ck); ctx.restore()
    # Oct 1 calendar
    cx, cy = P(0.2, 0.42, 0.25, 0.2)
    calendar(ctx, cx, cy, 380 * U if not VERT else 360 * U, "OCTOBER", "", 0, 31, 1, prog(t, 0.2, 1.0), prog(t, d * 0.15, d * 0.25), CORAL, t)
    hk = prog(t, d * 0.25, d * 0.32)
    if not VERT: bigtext(ctx, "OCT 1", W * 0.2, H * 0.7, 110 * U, CORAL, hk)
    else: bigtext(ctx, "OCT 1", W * 0.72, H * 0.2, 110 * U, CORAL, hk)
    lk = prog(t, d * 0.8, d * 0.88)
    pill(ctx, "A FEW HOURS → MORE THAN A MONTH", bx if not VERT else CX, H * 0.13 if not VERT else H * 0.35, 36 * U if not VERT else 30 * U, WHITE, lk)
    chip(ctx, "THE BUDGET DEADLINE", t)

def sc_history(ctx, t, d):
    bg(ctx, t)
    x0, x1 = (W * 0.08, W * 0.92) if not VERT else (W * 0.06, W * 0.94)
    y0 = H * 0.42 if not VERT else H * 0.36
    ctx.set_line_width(4 * U); rgba(ctx, WHITE, 0.7); ctx.move_to(x0, y0); ctx.line_to(x1, y0); ctx.stroke()
    n = 40
    random.seed(5)
    hs = [random.uniform(0.25, 1.0) for _ in range(n)]
    exc = {17: "1934", 33: "1998", 34: "2002"}
    bw = (x1 - x0) / n
    for i in range(n):
        k = prog(t, 0.3 + i * 0.08, 0.8 + i * 0.08)
        if not k: continue
        x = x0 + i * bw + bw * 0.15
        if i in exc:
            hh = 90 * U * k
            rgba(ctx, GOLD, 1); ctx.rectangle(x, y0 - hh, bw * 0.7, hh); ctx.fill()
            ek = prog(t, d * 0.45, d * 0.55)
            if ek:
                glow(ctx, x + bw * 0.35, y0 - hh, 60 * U, GOLD, 0.6 * ek)
                off = {17: 0, 33: -1, 34: 1}[i]
                text(ctx, exc[i], x + bw * 0.35 + off * (30 if not VERT else 34) * U, y0 - hh - 40 * U - (abs(off) * 0) , 30 * U if not VERT else 24 * U, GOLD, ek)
        else:
            hh = hs[i] * (300 if not VERT else 250) * U * k
            rgba(ctx, (0.6, 0.66, 0.85), 0.9); ctx.rectangle(x, y0, bw * 0.7, hh); ctx.fill()
    text(ctx, "SEATS GAINED", x0, y0 - 140 * U, 30 * U, GOLD, prog(t, d * 0.45, d * 0.55), True, "l")
    text(ctx, "SEATS LOST", x0, y0 + 330 * U if not VERT else y0 + 290 * U, 30 * U, (0.6, 0.66, 0.85), prog(t, 2, 3), True, "l")
    text(ctx, "PRESIDENT'S PARTY IN THE HOUSE, MIDTERM AFTER MIDTERM", CX, H * 0.14 if not VERT else H * 0.18, 40 * U if not VERT else 28 * U, WHITE, prog(t, 0.2, 1.0))
    tk = prog(t, d * 0.82, d * 0.9)
    pill(ctx, "A PATTERN, NOT A LAW", CX if not VERT else CX, H * 0.78 - 30 * U if not VERT else H * 0.64, 40 * U if not VERT else 34 * U, MAJ, tk)
    chip(ctx, "STYLIZED · NOT TO SCALE", t)

def duck(ctx, x, y, s, a=1.0, t=0.0):
    if a <= 0: return
    bob = math.sin(t * 3) * 6 * U
    ctx.save(); ctx.translate(x, y + bob)
    ctx.save(); ctx.scale(s * 1.2, s * 0.75); ctx.arc(0, 0, 1, 0, 2 * math.pi); ctx.restore(); rgba(ctx, (0.98, 0.86, 0.35), a); ctx.fill()
    ctx.save(); ctx.translate(-s * 0.2, -s * 0.1); ctx.rotate(-0.3); ctx.scale(s * 0.6, s * 0.35); ctx.arc(0, 0, 1, 0, 2 * math.pi); ctx.restore(); rgba(ctx, (0.92, 0.75, 0.25), a); ctx.fill()
    circle(ctx, s * 0.85, -s * 0.75, s * 0.48, (0.98, 0.86, 0.35), a)
    ctx.move_to(s * 1.25, -s * 0.8); ctx.line_to(s * 1.75, -s * 0.68); ctx.line_to(s * 1.25, -s * 0.56); ctx.close_path(); rgba(ctx, (1.0, 0.55, 0.2), a); ctx.fill()
    circle(ctx, s * 1.0, -s * 0.88, s * 0.07, NAVY, a)
    # water ripples
    ctx.restore()
    for i in range(3):
        k = (t * 0.5 + i / 3) % 1
        ctx.save(); ctx.translate(x, y + s * 0.7); ctx.scale(s * (1.2 + k * 1.4), s * (0.2 + k * 0.2))
        ctx.arc(0, 0, 1, 0, 2 * math.pi); ctx.restore(); ctx.set_line_width(3 * U); rgba(ctx, PB, a * (1 - k) * 0.7); ctx.stroke()

def sc_january(ctx, t, d):
    bg(ctx, t)
    cx, cy = P(0.24, 0.45, 0.28, 0.24)
    calendar(ctx, cx, cy, 440 * U if not VERT else 380 * U, "JANUARY", "2027", 5, 31, 3, prog(t, 0.2, 1.0), prog(t, d * 0.2, d * 0.3), PB, t)
    jk = prog(t, d * 0.22, d * 0.3)
    if not VERT: bigtext(ctx, "JAN 3", W * 0.24, H * 0.75, 110 * U, PB, jk)
    else: bigtext(ctx, "JAN 3", W * 0.73, H * 0.2, 110 * U, PB, jk)
    dk = prog(t, d * 0.4, d * 0.5) * (1 - prog(t, d * 0.68, d * 0.74))
    dx, dy = P(0.66, 0.55, 0.5, 0.52)
    duck(ctx, dx, dy, 120 * U, dk, t)
    pill(ctx, "LAME DUCK SESSION", dx, dy - 260 * U if not VERT else dy - 210 * U, 42 * U if not VERT else 36 * U, GOLD, dk)
    nk = prog(t, d * 0.72, d * 0.85)
    if nk:
        R = 380 * U if not VERT else 330 * U
        hx, hy = P(0.66, 0.68, 0.5, 0.6)
        hemicycle(ctx, hx, hy, R, 100, 5, lambda i: MAJ, nk, nk, t)
        text(ctx, "NEW CONGRESS", hx, hy - R - 50 * U, 50 * U, MAJ, nk)
    chip(ctx, "WHEN DOES IT CHANGE?", t)

def stat_card(ctx, x, y, w, h, big, small, c, k, t):
    if k <= 0: return
    yy = y + (1 - k) * 50 * U
    panel(ctx, x, yy, w, h, k, c)
    glow(ctx, x, yy - h * 0.12, w * 0.45, c, 0.2 * k)
    text(ctx, big, x, yy - h * 0.12, h * 0.36, c, k)
    font(ctx, h * 0.1); sw = ctx.text_extents(small).width
    text(ctx, small, x, yy + h * 0.27, h * 0.1 * min(1.0, w * 0.86 / max(sw, 1)), WHITE, k)

def sc_outro(ctx, t, d):
    bg(ctx, t)
    cards = [("2", "CHAMBERS", WHITE), ("218", "HOUSE MAJORITY", PB), ("51", "SENATE MAJORITY", PA), ("60", "MOST LAWS (SENATE)", CORAL), ("2/3", "VETO OVERRIDE", MAJ)]
    if VERT:
        pos = [(W * 0.27, H * 0.2), (W * 0.73, H * 0.2), (W * 0.27, H * 0.38), (W * 0.73, H * 0.38), (CX, H * 0.56)]
        w, h = 440 * U, 290 * U
    else:
        pos = [(W * (0.12 + 0.19 * i), H * 0.48) for i in range(5)]
        w, h = 330 * U, 380 * U
    for i, (b, s, c) in enumerate(cards):
        k = prog(t, d * (0.3 + i * 0.1), d * (0.35 + i * 0.1))
        stat_card(ctx, pos[i][0], pos[i][1] + math.sin(t * 1.2 + i) * 6 * U, w, h, b, s, c, k, t)
    if not VERT: text(ctx, "MIDTERMS DECIDE HOW MUCH A PRESIDENT CAN DO", CX, H * 0.14, 48 * U, WHITE, prog(t, 0.2, 1.2))
    else: text(ctx, "THE KEY NUMBERS", CX, H * 0.08 + 30 * U, 56 * U, WHITE, prog(t, 0.2, 1.2))

def sc_sub(ctx, t, d):
    bg(ctx, t)
    if VERT:
        p1, p2, w, h = (W * 0.27, H * 0.3), (W * 0.73, H * 0.3), 440 * U, 520 * U
    else:
        p1, p2, w, h = (W * 0.3, H * 0.44), (W * 0.7, H * 0.44), 620 * U, 480 * U
    for i, (p, c, lab) in enumerate([(p1, PA, "UNIFIED POWER"), (p2, PB, "DIVIDED POWER")]):
        k = prog(t, 0.2 + i * 0.4, 0.9 + i * 0.4)
        if not k: continue
        yy = p[1] + math.sin(t * 1.5 + i * 2) * 8 * U
        panel(ctx, p[0], yy, w, h, k, c)
        glow(ctx, p[0], yy - h * 0.1, w * 0.5, c, 0.25 * k)
        text(ctx, "?", p[0], yy - h * 0.12, h * 0.42, c, k)
        text(ctx, lab, p[0], yy + h * 0.3, (44 if not VERT else 36) * U, WHITE, k)
    if not VERT: text(ctx, "or", CX, H * 0.44, 50 * U, WHITE, prog(t, 1, 1.6))
    sk = prog(t, d * 0.5, d * 0.6)
    if sk:
        bx, by = (CX, H * 0.76 - 20 * U) if not VERT else (CX, H * 0.58)
        bw_, bh_ = 520 * U, 110 * U
        pulse = 1 + 0.04 * math.sin(t * 5)
        ctx.save(); ctx.translate(bx, by); ctx.scale(pulse * sk, pulse * sk)
        rrect(ctx, -bw_ / 2, -bh_ / 2, bw_, bh_, 22 * U); rgba(ctx, CORAL); ctx.fill()
        text(ctx, "SUBSCRIBE", 0, 0, 56 * U, WHITE)
        ctx.restore()
    chip(ctx, "YOUR TURN", t)

SHORT_SCENES = ["hook", "sixty", "sub"]

SCENES = dict(hook=sc_hook, calendar=sc_calendar, capitol=sc_capitol, house=sc_house, senate=sc_senate, myth=sc_myth,
              bill=sc_bill, filibuster=sc_filibuster, sixty=sc_sixty, unified=sc_unified, househ=sc_househ,
              senateflip=sc_senateflip, both=sc_both, budget=sc_budget, history=sc_history, january=sc_january,
              outro=sc_outro, sub=sc_sub)

def thumbnail(c):
    """Thumbnail 1280x720."""
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, .08, .11, .26); g.add_color_stop_rgb(1, .02, .03, .08); c.set_source(g); c.paint()
    random.seed(1)
    for _ in range(140):
        c.arc(random.random() * W, random.random() * H, random.uniform(.5, 1.6), 0, 6.3); c.set_source_rgba(1, 1, 1, random.uniform(.3, .8)); c.fill()
    glow(c, 1000, 420, 360, (0.6, 0.75, 1.0), 0.3)
    hemicycle(c, 1000, 640, 300, 100, 5, split_colors(100, 50, 50), 1, 1, 0)
    capitol(c, 1000, 470, 95, 1, 0)
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    c.set_font_size(44); c.set_source_rgb(*PA); c.move_to(760, 120); c.show_text("PARTY A")
    c.set_source_rgb(*PB); c.move_to(1050, 120); c.show_text("PARTY B")
    thumb_text(c, "WHO CONTROLS", "CONGRESS?", "MIDTERMS EXPLAINED")
