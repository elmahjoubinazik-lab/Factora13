# Episode 014 (Short only) - "Why a full washing machine leaves your clothes dirty"
# Executed inside engine/render.py (helpers available). Vertical layout (1080x1920). Original illustrations.

BODY = (0.92, 0.94, 0.97)
BODY_D = (0.70, 0.75, 0.84)
STEEL = (0.62, 0.68, 0.78)
WATER = (0.30, 0.62, 0.95)
CLOTH = [(1.0, 0.45, 0.45), (1.0, 0.80, 0.33), (0.35, 0.78, 0.95), (0.42, 0.88, 0.58), (0.75, 0.55, 1.0), (1.0, 0.62, 0.30)]
MAJ = (0.42, 0.88, 0.58)

def bg(ctx, t):
    vgrad(ctx, (0.06, 0.09, 0.19), NAVY)
    random.seed(21)
    for i in range(34):
        x0, y0, sp = random.random(), random.random(), random.uniform(0.01, 0.03)
        r = random.uniform(4, 12) * U
        y = (y0 - t * sp) % 1.0
        ctx.new_path(); ctx.arc(x0 * W, y * H, r, 0, 2 * math.pi); ctx.set_line_width(2 * U); rgba(ctx, (0.6, 0.8, 1.0), 0.12); ctx.stroke()

def machine(ctx, cx, cy, s, shake=0.0, t=0.0):
    """Front-loading washer, porthole centered at (cx, cy); s = porthole radius. Returns drum radius."""
    dx = shake * math.sin(t * 40) * 8 * U; dy = shake * math.cos(t * 33) * 5 * U
    ctx.save(); ctx.translate(dx, dy)
    w, h = s * 2.9, s * 3.05
    x0, y0 = cx - w / 2, cy - s * 1.45
    # shadow
    ctx.save(); ctx.translate(cx, y0 + h + 10 * U); ctx.scale(w * 0.55, 22 * U); ctx.arc(0, 0, 1, 0, 2 * math.pi); ctx.restore(); rgba(ctx, (0, 0, 0), 0.4); ctx.fill()
    g = cairo.LinearGradient(x0, 0, x0 + w, 0); g.add_color_stop_rgb(0, *BODY); g.add_color_stop_rgb(1, *BODY_D)
    rrect(ctx, x0, y0, w, h, 36 * U); ctx.set_source(g); ctx.fill()
    # control panel
    ctx.rectangle(x0 + 20 * U, y0 + 20 * U, w - 40 * U, s * 0.32); rgba(ctx, (0.82, 0.85, 0.92)); ctx.fill()
    circle(ctx, x0 + w - s * 0.4, y0 + 20 * U + s * 0.16, s * 0.11, (0.55, 0.6, 0.72))
    ctx.save(); ctx.translate(x0 + w - s * 0.4, y0 + 20 * U + s * 0.16); ctx.rotate(t * 0.4)
    ctx.rectangle(-2 * U, -s * 0.1, 4 * U, s * 0.08); rgba(ctx, WHITE); ctx.fill(); ctx.restore()
    rrect(ctx, x0 + s * 0.2, y0 + 30 * U, s * 0.9, s * 0.2, 8 * U); rgba(ctx, (0.15, 0.2, 0.35)); ctx.fill()
    text(ctx, "%02d:%02d" % (int(t) // 60 + 1, int(t * 3) % 60), x0 + s * 0.65, y0 + 30 * U + s * 0.1, s * 0.12, (0.4, 1.0, 0.7))
    # door ring
    circle(ctx, cx, cy, s * 1.12, (0.55, 0.6, 0.72))
    circle(ctx, cx, cy, s * 1.04, (0.85, 0.88, 0.94))
    circle(ctx, cx, cy, s, (0.05, 0.07, 0.14))
    ctx.restore()
    return dx, dy

def drum(ctx, cx, cy, r, rot, a=1.0):
    """Perforated drum interior with 3 lifters, rotated by rot."""
    ctx.save(); ctx.arc(cx, cy, r, 0, 2 * math.pi); ctx.clip()
    g = cairo.RadialGradient(cx, cy, r * 0.1, cx, cy, r)
    g.add_color_stop_rgb(0, 0.30, 0.34, 0.44); g.add_color_stop_rgb(1, 0.16, 0.19, 0.27); ctx.set_source(g); ctx.paint()
    for ring in range(2, 9):
        rr = r * ring / 9
        n = int(ring * 7)
        for j in range(n):
            an = rot + j / n * 2 * math.pi
            circle(ctx, cx + math.cos(an) * rr, cy + math.sin(an) * rr, 3.2 * U, (0.10, 0.12, 0.18), 0.9 * a)
    ctx.restore()
    for k in range(3):
        an = rot + k * 2 * math.pi / 3
        ctx.save(); ctx.translate(cx + math.cos(an) * r * 0.9, cy + math.sin(an) * r * 0.9); ctx.rotate(an + math.pi / 2)
        ctx.move_to(-r * 0.12, 0); ctx.line_to(0, r * 0.16); ctx.line_to(r * 0.12, 0); ctx.close_path()
        rgba(ctx, STEEL, a); ctx.fill(); ctx.restore()

def water(ctx, cx, cy, r, level, t, a=1.0):
    ctx.save(); ctx.arc(cx, cy, r, 0, 2 * math.pi); ctx.clip()
    y = cy + r * (1 - 2 * level)
    ctx.move_to(cx - r, y)
    for i in range(41):
        x = cx - r + i * 2 * r / 40
        ctx.line_to(x, y + math.sin(t * 4 + i * 0.6) * 6 * U)
    ctx.line_to(cx + r, cy + r); ctx.line_to(cx - r, cy + r); ctx.close_path()
    rgba(ctx, WATER, 0.45 * a); ctx.fill()
    ctx.restore()

def cloth(ctx, x, y, sz, ang, c, a=1.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(ang)
    rrect(ctx, -sz, -sz * 0.55, sz * 2, sz * 1.1, sz * 0.4); rgba(ctx, c, a); ctx.fill()
    ctx.set_line_width(2 * U); rgba(ctx, (1, 1, 1), 0.25 * a)
    ctx.move_to(-sz * 0.7, -sz * 0.1); ctx.curve_to(-sz * 0.2, sz * 0.2, sz * 0.2, -sz * 0.3, sz * 0.7, 0); ctx.stroke()
    ctx.restore()

def tumbling(ctx, cx, cy, r, t, n=9, a=1.0, speed=0.35):
    """Clothes carried up by the drum then dropping back into the water."""
    for i in range(n):
        k = (t * speed + i / n) % 1.0
        c = CLOTH[i % len(CLOTH)]
        sz = r * 0.13
        if k < 0.62:
            q = k / 0.62
            an = math.pi / 2 - q * (math.pi * 0.85)          # from bottom, up the left side (counter-clockwise view)
            rr = r * 0.78
            x = cx - math.cos(an - math.pi / 2) * 0 + math.cos(an + math.pi / 2 * 0) * 0
            x = cx + math.cos(math.pi / 2 + q * math.pi * 0.85) * rr
            y = cy + math.sin(math.pi / 2 + q * math.pi * 0.85) * rr
        else:
            q = (k - 0.62) / 0.38
            x0 = cx + math.cos(math.pi / 2 + math.pi * 0.85) * r * 0.78
            y0 = cy + math.sin(math.pi / 2 + math.pi * 0.85) * r * 0.78
            x = x0 + (cx + r * 0.1 - x0) * q
            y = y0 + (cy + r * 0.62 - y0) * q * q
            if q > 0.85:
                for j in range(4):
                    circle(ctx, x + (j - 1.5) * 14 * U, y - (q - 0.85) * 300 * U * (1 + j % 2), 5 * U, (0.7, 0.9, 1.0), 0.8 * a)
        cloth(ctx, x, y, sz, t * 2 + i, c, a)

def packed(ctx, cx, cy, r, rot, a=1.0, dim_center=0.0):
    random.seed(4)
    items = []
    for i in range(70):
        rr = r * math.sqrt(random.random()) * 0.92
        an = random.random() * 2 * math.pi
        items.append((rr, an, random.random() * 3, CLOTH[i % len(CLOTH)]))
    items.sort(key=lambda p: -p[0])
    for rr, an, ang, c in items:
        x = cx + math.cos(an + rot) * rr; y = cy + math.sin(an + rot) * rr
        cc = mix(c, (0.35, 0.33, 0.30), dim_center * clamp(1 - rr / (r * 0.5)))
        cloth(ctx, x, y, r * 0.14, ang + rot, cc, a)

def pill(ctx, label, x, y, size, c=GOLD, a=1.0, fill=NAVY):
    if a <= 0: return
    font(ctx, size); w = ctx.text_extents(label).width + size * 1.4; h = size * 2.0
    rrect(ctx, x - w / 2, y - h / 2, w, h, h / 2); rgba(ctx, fill, 0.9 * a); ctx.fill()
    ctx.set_line_width(3 * U); rgba(ctx, c, a); rrect(ctx, x - w / 2, y - h / 2, w, h, h / 2); ctx.stroke()
    text(ctx, label, x, y, size, c, a)

MX, MY, MS = W * 0.5, H * 0.44, 265 * U

def sc_hook(ctx, t, d):
    bg(ctx, t)
    dx, dy = machine(ctx, MX, MY, MS, 0.4, t)
    drum(ctx, MX + dx, MY + dy, MS * 0.97, t * 0.5)
    packed(ctx, MX + dx, MY + dy, MS * 0.97, t * 0.5)
    # clothes bulging against the glass
    glow(ctx, MX, MY, MS * 1.2, CORAL, 0.18 + 0.08 * math.sin(t * 4))
    k = prog(t, d * 0.45, d * 0.6)
    if k:
        ctx.save(); ctx.translate(MX, MY); s = 1.4 - 0.4 * k; ctx.scale(s, s)
        ctx.set_line_width(26 * U); ctx.set_line_cap(cairo.LINE_CAP_ROUND); rgba(ctx, CORAL, 0.9 * k)
        ctx.move_to(-MS * 0.7, -MS * 0.7); ctx.line_to(MS * 0.7, MS * 0.7); ctx.stroke()
        ctx.move_to(MS * 0.7, -MS * 0.7); ctx.line_to(-MS * 0.7, MS * 0.7); ctx.stroke()
        ctx.restore()

def sc_lifters(ctx, t, d):
    bg(ctx, t)
    machine(ctx, MX, MY, MS, 0, t)
    rot = -t * 1.0
    drum(ctx, MX, MY, MS * 0.97, rot)
    water(ctx, MX, MY, MS * 0.97, 0.3, t)
    tumbling(ctx, MX, MY, MS * 0.97, t)
    k = prog(t, 0.8, 1.6)
    if k:
        an = rot + math.pi / 2
        lx, ly = MX + math.cos(an) * MS * 0.85, MY + math.sin(an) * MS * 0.85
        glow(ctx, lx, ly, 70 * U, GOLD, 0.6 * k)
    pill(ctx, "LIFTERS", W * 0.5, H * 0.12, 56 * U, GOLD, k)
    pill(ctx, "LIFT → DROP → WASH", W * 0.5, H * 0.2, 42 * U, MAJ, prog(t, d * 0.55, d * 0.65))

def sc_full(ctx, t, d):
    bg(ctx, t)
    machine(ctx, MX, MY, MS, 0, t)
    rot = -t * 0.8
    drum(ctx, MX, MY, MS * 0.97, rot)
    water(ctx, MX, MY, MS * 0.97, 0.18, t)
    packed(ctx, MX, MY, MS * 0.97, rot, 1, prog(t, d * 0.45, d * 0.6))
    k = prog(t, d * 0.2, d * 0.3)
    if k:
        ctx.new_path(); ctx.arc(MX, MY, MS * 0.92, 0, 2 * math.pi); ctx.set_line_width(8 * U); ctx.set_dash([20 * U, 14 * U], -t * 60 * U)
        rgba(ctx, GOLD, k); ctx.stroke(); ctx.set_dash([])
    pill(ctx, "ONE BIG BLOCK", W * 0.5, H * 0.12, 56 * U, GOLD, k)
    c = prog(t, d * 0.5, d * 0.6)
    if c:
        glow(ctx, MX, MY, MS * 0.45, CORAL, 0.35 * c)
        pill(ctx, "MIDDLE: BARELY WASHED", W * 0.5, H * 0.2, 42 * U, CORAL, c)

def sc_spin(ctx, t, d):
    bg(ctx, t)
    sh = prog(t, 1.0, 2.5)
    dx, dy = machine(ctx, MX, MY, MS, sh, t)
    rot = -t * (2 + 14 * sh)
    drum(ctx, MX + dx, MY + dy, MS * 0.97, rot)
    # clump stuck on one side
    for i in range(14):
        an = rot + (i - 7) * 0.09
        rr = MS * (0.8 - (i % 3) * 0.12)
        cloth(ctx, MX + dx + math.cos(an) * rr, MY + dy + math.sin(an) * rr, MS * 0.13, an, CLOTH[i % 6])
    # motion blur ring
    ctx.new_path(); ctx.arc(MX + dx, MY + dy, MS * 0.8, 0, 2 * math.pi); ctx.set_line_width(MS * 0.25); rgba(ctx, (1, 1, 1), 0.06 * sh); ctx.stroke()
    # bearing at the center
    b = prog(t, d * 0.45, d * 0.55)
    if b:
        glow(ctx, MX + dx, MY + dy, 110 * U, CORAL, (0.5 + 0.3 * math.sin(t * 8)) * b)
        circle(ctx, MX + dx, MY + dy, 46 * U, STEEL, b)
        for j in range(8):
            an = j / 8 * 2 * math.pi + rot
            circle(ctx, MX + dx + math.cos(an) * 30 * U, MY + dy + math.sin(an) * 30 * U, 9 * U, (0.9, 0.92, 0.96), b)
        circle(ctx, MX + dx, MY + dy, 16 * U, (0.2, 0.22, 0.3), b)
    pill(ctx, "UNEVEN SPIN", W * 0.5, H * 0.12, 56 * U, CORAL, prog(t, 0.6, 1.2))
    pill(ctx, "BEARINGS · SHOCK ABSORBERS", W * 0.5, H * 0.2, 38 * U, GOLD, prog(t, d * 0.55, d * 0.65))

def hand(ctx, x, y, s, a=1.0):
    """Flat hand seen from the side (pointing right), center (x, y)."""
    if a <= 0: return
    skin = (0.98, 0.80, 0.62)
    rrect(ctx, x - s * 1.0, y - s * 0.32, s * 1.1, s * 0.64, s * 0.2); rgba(ctx, skin, a); ctx.fill()
    for j in range(4):
        fy = y - s * 0.3 + j * s * 0.2
        rrect(ctx, x, fy, s * (0.95 - abs(j - 1.3) * 0.12), s * 0.17, s * 0.08); rgba(ctx, skin, a); ctx.fill()
    rrect(ctx, x - s * 0.45, y - s * 0.55, s * 0.55, s * 0.22, s * 0.1); rgba(ctx, (0.95, 0.74, 0.56), a); ctx.fill()

def sc_hand(ctx, t, d):
    bg(ctx, t)
    machine(ctx, MX, MY, MS, 0, t)
    rot = -t * 0.9
    drum(ctx, MX, MY, MS * 0.97, rot)
    water(ctx, MX, MY, MS * 0.97, 0.3, t)
    # laundry filling ~3/4 of the drum
    ctx.save(); ctx.rectangle(0, MY - MS * 0.42, W, H); ctx.clip()
    tumbling(ctx, MX, MY, MS * 0.97, t, n=7, speed=0.3)
    random.seed(7)
    for i in range(26):
        rr = MS * 0.85 * math.sqrt(random.random()); an = random.uniform(0.15, math.pi - 0.15)
        cloth(ctx, MX + math.cos(an + rot * 0.2) * rr * 0.9, MY + math.sin(an) * rr * 0.8 + MS * 0.05, MS * 0.13, an + t, CLOTH[i % 6])
    ctx.restore()
    k = prog(t, 0.6, 1.4)
    gy = MY - MS * 0.62
    hand(ctx, MX - MS * 0.05 + (1 - k) * 200 * U, gy, MS * 0.36, k)
    if k:
        ctx.set_line_width(5 * U); rgba(ctx, MAJ, k); ctx.set_dash([12 * U, 10 * U])
        ctx.move_to(MX - MS * 0.85, MY - MS * 0.42); ctx.line_to(MX + MS * 0.85, MY - MS * 0.42); ctx.stroke(); ctx.set_dash([])
    pill(ctx, "LEAVE ≈ 1 HAND OF SPACE", W * 0.5, H * 0.12, 48 * U, MAJ, prog(t, 1.0, 1.6))
    pill(ctx, "✓ CLEAN · ✓ RINSED · ✓ LASTS", W * 0.5, H * 0.2, 38 * U, GOLD, prog(t, d * 0.6, d * 0.7))

def sc_sub(ctx, t, d):
    bg(ctx, t)
    machine(ctx, MX, MY, MS, 0, t)
    drum(ctx, MX, MY, MS * 0.97, -t)
    water(ctx, MX, MY, MS * 0.97, 0.3, t)
    tumbling(ctx, MX, MY, MS * 0.97, t, n=6)
    text(ctx, "DID YOU KNOW?", W * 0.5, H * 0.11, 84 * U, GOLD, prog(t, 0.2, 0.8))
    sk = prog(t, d * 0.35, d * 0.45)
    if sk:
        pulse = 1 + 0.04 * math.sin(t * 5)
        ctx.save(); ctx.translate(W * 0.5, H * 0.2); ctx.scale(pulse * sk, pulse * sk)
        rrect(ctx, -260 * U, -55 * U, 520 * U, 110 * U, 22 * U); rgba(ctx, CORAL); ctx.fill()
        text(ctx, "SUBSCRIBE", 0, 0, 56 * U, WHITE); ctx.restore()

SHORT_SCENES = ["hook", "lifters", "full", "spin", "hand", "sub"]
SCENES = dict(hook=sc_hook, lifters=sc_lifters, full=sc_full, spin=sc_spin, hand=sc_hand, sub=sc_sub)

def thumbnail(c):
    bg(c, 0)
    X, Y, Sz = 1010, 340, 165
    glow(c, X, Y, 330, CORAL, 0.3)
    machine(c, X, Y, Sz, 0, 2)
    drum(c, X, Y, Sz * 0.97, 0.3)
    packed(c, X, Y, Sz * 0.97, 0.3)
    c.set_line_width(22); c.set_line_cap(cairo.LINE_CAP_ROUND); rgba(c, CORAL, 0.9)
    c.move_to(X - 110, Y - 110); c.line_to(X + 110, Y + 110); c.stroke()
    c.move_to(X + 110, Y - 110); c.line_to(X - 110, Y + 110); c.stroke()
    thumb_text(c, "STOP OVERLOADING", "YOUR WASHER", "CLOTHES STAY DIRTY")
