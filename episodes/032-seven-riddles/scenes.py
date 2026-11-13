# Episode 032 (vidéo longue 16:9) - "Test Your Logic: 7 Riddles, 15 Seconds Each" (15 s de réflexion depuis la demande de Nazik du 2026-11-13)
# Demande de Nazik (2026-11-13) : vidéo longue d'énigmes avec 1 minute de réflexion entre chaque énigme (format « 7 riddles »,
# énigmes classiques du domaine public, textes et dessins 100 % originaux, style néon sobre, sans images d'IA).
# Scènes : intro, r{i}_q (énigme), r{i}_t (chrono 60 s + indice à 30 s), r{i}_a (réponse expliquée), outro.
# Exécuté dans engine/render.py (helpers du moteur). Toutes les tailles en multiples de U.

TINT = [PURPLE, CYAN, CORAL, PINK, GREEN, GOLD, PURPLE]
NAMES = ["THE BAT AND THE BALL", "THE LILY PADS", "THE BURNING ROPES", "THE T-SHIRT HOLES", "THE ROPE AROUND THE EARTH",
         "THE BIRTHDAY RIDDLE", "THE THREE DOORS"]
RECAP = [("A BAT + A BALL = $1.10", "THE BAT COSTS $1.00 MORE. THE BALL?"),
         ("LILY PADS DOUBLE EVERY DAY", "FULL LAKE ON DAY 48. HALF ON DAY...?"),
         ("2 ROPES, 1 HOUR EACH, UNEVEN BURN", "MEASURE EXACTLY 45 MINUTES"),
         ("PANTS = 2 HOLES", "HOW MANY HOLES IN A T-SHIRT?"),
         ("ROPE AROUND EARTH + 3 FEET", "HOW HIGH DOES IT FLOAT?"),
         ("HOW MANY PEOPLE FOR A 50% CHANCE", "THAT TWO SHARE A BIRTHDAY?"),
         ("YOU PICK DOOR 1, HOST OPENS DOOR 3: GOAT", "STAY OR SWITCH?")]
HINTS = ["HINT: CHECK IT. DOES BAT + BALL REALLY = $1.10?", "HINT: THINK ONE DAY BACKWARD", "HINT: A ROPE LIT AT BOTH ENDS BURNS TWICE AS FAST",
         "HINT: COUNT THE OPENINGS", "HINT: LENGTH = 2 × PI × RADIUS", "HINT: COUNT THE PAIRS, NOT THE PEOPLE",
         "HINT: THE HOST ALWAYS REVEALS A GOAT"]
VOTE = ["VOTE IN THE COMMENTS!", "COMMENT YOUR ANSWER!", "TYPE YOUR METHOD IN THE COMMENTS!", "COMMENT 1, 2 OR 3!",
        "COMMENT 1, 2 OR 3!", "LOCK IN YOUR VOTE: 1, 2 OR 3!", "FINAL VOTE: 1, 2 OR 3!"]
OPTIONS = {3: [("1", "FOUR"), ("2", "THREE"), ("3", "ZERO")], 4: [("1", "A HAIR"), ("2", "~6 INCHES"), ("3", "~1 MILE")],
           5: [("1", "23"), ("2", "183"), ("3", "366")], 6: [("1", "STAY"), ("2", "SWITCH"), ("3", "NO DIFFERENCE")]}

_TL = {sg["scene"]: sg for sg in json.load(open(EP + "/build/timeline.json", encoding="utf-8"))}
def ST(scene, k):
    """Début (temps local) de la k-ième phrase de la scène : synchronise les animations avec la voix."""
    sg = _TL.get(scene)
    if not sg or k >= len(sg["sents"]): return 1e9
    return sg["sents"][k]["start"] - sg["start"]

# ---------- éléments communs ----------
def bg(ctx, t, i=0):
    neon_bg(ctx, t, tint=TINT[i])

def header(ctx, i, a=1.0):
    """Pastille « RIDDLE i/7 » + nom de l'énigme en haut à gauche, progression (7 points) en haut à droite."""
    if a <= 0: return
    s_ = f"RIDDLE {i + 1}/7"; font(ctx, 38 * U); w_ = ctx.text_extents(s_).width + 50 * U
    rrect(ctx, 50 * U, 40 * U, w_, 64 * U, 32 * U); rgba(ctx, TINT[i], 0.95 * a); ctx.fill()
    text(ctx, s_, 50 * U + w_ / 2, 72 * U, 38 * U, (0.03, 0.02, 0.08), a)
    text(ctx, NAMES[i], 50 * U + w_ + 24 * U, 72 * U, 36 * U, WHITE, 0.85 * a, align="l")
    for k in range(7):
        x = W - 70 * U - (6 - k) * 40 * U
        circle(ctx, x, 72 * U, 12 * U, TINT[k] if k <= i else (0.3, 0.3, 0.4), a * (1.0 if k <= i else 0.6))

def options_row(ctx, t, opts, y, a=1.0, good=None, cx=None, sc=1.0):
    if a <= 0: return
    cx = CX if cx is None else cx
    pw, ph = 330 * U * sc, 84 * U * sc
    for j, (n, s_) in enumerate(opts):
        x = cx + (j - 1) * (pw + 30 * U * sc)
        col = [CYAN, CORAL, PURPLE][j]
        dim = 1.0 if good is None or good == j else 0.3
        if good == j: col = GREEN; glow(ctx, x, y, pw * 0.8, GREEN, 0.4 * a)
        rrect(ctx, x - pw / 2, y - ph / 2, pw, ph, ph / 2); rgba(ctx, (0.04, 0.03, 0.10), 0.88 * a * dim); ctx.fill()
        rrect(ctx, x - pw / 2, y - ph / 2, pw, ph, ph / 2); ctx.set_line_width(5 * U); rgba(ctx, col, a * dim); ctx.stroke()
        circle(ctx, x - pw / 2 + ph / 2, y, ph * 0.36, col, a * dim)
        text(ctx, n, x - pw / 2 + ph / 2, y, 46 * U * sc, (0.04, 0.03, 0.10), a * dim)
        font(ctx, 40 * U * sc); tw = ctx.text_extents(s_).width; sz = 40 * U * sc * min(1.0, (pw - ph * 1.3) / tw)
        text(ctx, s_, x + ph * 0.32, y, sz, WHITE, a * dim)

def big_answer(ctx, t, s_, col, a=1.0, y=None, size=150):
    if a <= 0: return
    y = H * 0.22 if y is None else y
    sc = (1 + 0.3 * (1 - a)) * (1 + 0.03 * math.sin(t * 5))
    ctx.save(); ctx.translate(CX, y); ctx.scale(sc, sc)
    neon_text(ctx, s_, 0, 0, size * U, col, a, WHITE, fill=0.35); ctx.restore()

def card(ctx, s_, x, y, col, a=1.0, size=44):
    if a <= 0: return
    font(ctx, size * U); w_ = ctx.text_extents(s_).width + 60 * U; h_ = size * 1.9 * U
    rrect(ctx, x - w_ / 2, y - h_ / 2, w_, h_, 18 * U); rgba(ctx, (0.03, 0.02, 0.08), 0.88 * a); ctx.fill()
    rrect(ctx, x - w_ / 2, y - h_ / 2, w_, h_, 18 * U); ctx.set_line_width(4 * U); rgba(ctx, col, a); ctx.stroke()
    text(ctx, s_, x, y, size * U, col, a)

def cross(ctx, x, y, s, a=1.0):
    neon_path(ctx, lambda c: (c.move_to(x - s, y - s * 0.6), c.line_to(x + s, y + s * 0.6), c.move_to(x - s, y + s * 0.6), c.line_to(x + s, y - s * 0.6)), CORAL, 7 * U, a)

# ---------- 1. la batte et la balle ----------
def bat(ctx, x, y, s, ang, a=1.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(ang); S = s * U
    def path(c):
        c.move_to(-260 * S, -10 * S); c.curve_to(-80 * S, -14 * S, 60 * S, -38 * S, 230 * S, -40 * S)
        c.curve_to(270 * S, -40 * S, 270 * S, 40 * S, 230 * S, 40 * S); c.curve_to(60 * S, 38 * S, -80 * S, 14 * S, -260 * S, 10 * S); c.close_path()
    ctx.new_path(); path(ctx); g = cairo.LinearGradient(0, -40 * S, 0, 40 * S)
    g.add_color_stop_rgba(0, 0.95, 0.72, 0.42, a); g.add_color_stop_rgba(1, 0.60, 0.35, 0.15, a); ctx.set_source(g); ctx.fill()
    neon_path(ctx, path, GOLD, 4 * U, a)
    rrect(ctx, -290 * S, -18 * S, 34 * S, 36 * S, 8 * S); rgba(ctx, (0.3, 0.2, 0.1), a); ctx.fill()
    ctx.restore()

def ball(ctx, x, y, r, a=1.0, t=0.0):
    glow(ctx, x, y, r * 1.8, WHITE, 0.25 * a)
    g = cairo.RadialGradient(x - r * 0.3, y - r * 0.3, r * 0.1, x, y, r)
    g.add_color_stop_rgba(0, 1, 1, 1, a); g.add_color_stop_rgba(1, 0.75, 0.78, 0.85, a)
    ctx.new_path(); ctx.arc(x, y, r, 0, 2 * math.pi); ctx.set_source(g); ctx.fill()
    for sgn in (-1, 1):
        ctx.new_path(); ctx.arc(x + sgn * r * 1.25, y, r * 0.95, math.pi * (0.78 if sgn > 0 else -0.22), math.pi * (1.22 if sgn > 0 else 0.22))
        ctx.set_line_width(3 * U); rgba(ctx, CORAL, a); ctx.stroke()

def ill_1(ctx, t, a=1.0):
    bat(ctx, CX - 170 * U, H * 0.47, 1.25, -0.25 + 0.03 * math.sin(t * 1.5), a)
    ball(ctx, CX + 360 * U, H * 0.52 + 10 * U * math.sin(t * 3), 70 * U, a, t)
    card(ctx, "TOTAL: $1.10", CX - 150 * U, H * 0.70, GOLD, a)
    card(ctx, "BAT = BALL + $1.00", CX + 330 * U, H * 0.70, CYAN, a)

def ans_1(ctx, t, d, a=1.0):
    s1, s2 = ST("r1_a", 1), ST("r1_a", 2); s3 = s2 + 1.8
    if t < s2:
        big_answer(ctx, t, "10¢ ?", CORAL, prog(t, 1.0, 1.6), size=170)
        if t > s1:
            card(ctx, "BALL 10¢ + BAT $1.10 = $1.20", CX, H * 0.48, CORAL, prog(t, s1, s1 + 0.5), 46)
            cross(ctx, CX, H * 0.22, 140 * U, prog(t, s1 + 3.0, s1 + 3.4))
    else:
        big_answer(ctx, t, "5¢", GREEN, prog(t, s2, s2 + 0.6), size=200)
        k3 = prog(t, s3, s3 + 0.6)
        card(ctx, "BALL 5¢", CX - 360 * U, H * 0.50, GREEN, k3, 50)
        card(ctx, "BAT $1.05", CX, H * 0.50, GOLD, k3, 50)
        card(ctx, "= $1.10", CX + 340 * U, H * 0.50, CYAN, k3, 50)
        ball(ctx, CX - 360 * U, H * 0.66, 42 * U, k3, t)
        bat(ctx, CX, H * 0.66, 0.6, -0.1, k3)

# ---------- 2. les nénuphars ----------
def lake(ctx, cx, cy, rx, ry, cover, t, a=1.0):
    ctx.save(); ctx.translate(cx, cy); ctx.scale(1, ry / rx)
    ctx.new_path(); ctx.arc(0, 0, rx, 0, 2 * math.pi)
    g = cairo.RadialGradient(0, 0, rx * 0.1, 0, 0, rx); g.add_color_stop_rgba(0, 0.15, 0.55, 0.85, 0.9 * a); g.add_color_stop_rgba(1, 0.04, 0.18, 0.45, 0.9 * a)
    ctx.set_source(g); ctx.fill_preserve(); ctx.restore()
    neon_path(ctx, lambda c: (c.save(), c.translate(cx, cy), c.scale(1, ry / rx), c.arc(0, 0, rx, 0, 2 * math.pi), c.restore()), CYAN, 4 * U, a)
    rnd = random.Random(4); pads = []
    for i in range(160):
        ang = rnd.uniform(0, 2 * math.pi); r = math.sqrt(rnd.random()) * 0.9
        pads.append((math.cos(ang) * r, math.sin(ang) * r, rnd.uniform(0.07, 0.11)))
    pads.sort(key=lambda p: p[0])                       # le tapis s'étend de la gauche vers la droite
    n = int(len(pads) * clamp(cover))
    for (px, py, pr) in pads[:n]:
        x, y = cx + px * rx, cy + py * ry; r = pr * rx * 0.55
        ctx.new_path(); ctx.move_to(x, y); ctx.arc(x, y, r, 0.35, 2 * math.pi - 0.05); ctx.close_path()
        rgba(ctx, mix(GREEN, (0.1, 0.5, 0.2), 0.3), 0.95 * a); ctx.fill()
        ctx.new_path(); ctx.arc(x, y, r, 0.35, 2 * math.pi - 0.05); ctx.set_line_width(2 * U); rgba(ctx, GREEN, 0.9 * a); ctx.stroke()

def ill_2(ctx, t, a=1.0, cover=None, day=None):
    day = day if day is not None else 40 + int(clamp(t / 6) * 8)
    cov = cover if cover is not None else 2.0 ** (day - 48)
    lake(ctx, CX, H * 0.52, 520 * U, 230 * U, cov, t, a)
    card(ctx, f"DAY {day}", CX + 640 * U, H * 0.30, GOLD, a, 48)
    card(ctx, "×2 EVERY DAY", CX - 640 * U, H * 0.30, GREEN, a, 40)

def ans_2(ctx, t, d, a=1.0):
    k = prog(t, 1.0, 1.6); s1, s2 = ST("r2_a", 1), ST("r2_a", 2)
    day = 47 if t < s1 + 2.5 else 48
    cov = 0.5 if t < s1 + 2.5 else 0.5 + 0.5 * prog(t, s1 + 2.5, s1 + 4.0)
    lake(ctx, CX, H * 0.55, 470 * U, 200 * U, cov, t)
    big_answer(ctx, t, "DAY 47", GREEN, k, y=H * 0.20, size=150)
    card(ctx, f"DAY {day}: {'HALF' if day == 47 else 'FULL'}", CX + 600 * U, H * 0.36, GOLD, 1.0, 44)
    if t > s2:
        card(ctx, "DAY 24? ONLY 1/16,777,216 OF THE LAKE!", CX, H * 0.80 - 50 * U, CORAL, prog(t, s2, s2 + 0.6), 38)

# ---------- 3. les cordes qui brûlent ----------
def flame(ctx, x, y, s, t, a=1.0):
    if a <= 0: return
    f = 1 + 0.15 * math.sin(t * 17 + x)
    glow(ctx, x, y - 20 * s * U, 70 * s * U, CORAL, 0.5 * a)
    for col, sc in ((CORAL, 1.0), (GOLD, 0.62), (WHITE, 0.3)):
        h = 70 * s * U * sc * f; w_ = 26 * s * U * sc
        ctx.new_path(); ctx.move_to(x, y - h); ctx.curve_to(x + w_, y - h * 0.5, x + w_, y, x, y); ctx.curve_to(x - w_, y, x - w_, y - h * 0.5, x, y - h)
        rgba(ctx, col, 0.95 * a); ctx.fill()

def rope(ctx, x0, x1, y, t, burnt_l=0.0, burnt_r=0.0, a=1.0, col=GOLD):
    """Corde de x0 à x1 ; burnt_l / burnt_r : fraction déjà brûlée depuis chaque bout (avec flamme au front)."""
    L = x1 - x0; xa = x0 + L * burnt_l; xb = x1 - L * burnt_r
    if xb > xa + 2:
        neon_path(ctx, lambda c: [c.move_to(xa, y)] + [c.line_to(xa + (xb - xa) * i / 40, y + 8 * U * math.sin(i * 1.3 + x0 / 50)) for i in range(41)], col, 9 * U, a)
        if burnt_l > 0: flame(ctx, xa, y, 1.0, t, a)
        if burnt_r > 0: flame(ctx, xb, y, 1.0, t + 1.3, a)
    ctx.move_to(x0, y); ctx.line_to(xa, y); ctx.move_to(xb, y); ctx.line_to(x1, y)
    ctx.set_dash([10 * U, 14 * U]); ctx.set_line_width(4 * U); rgba(ctx, (0.4, 0.4, 0.45), 0.6 * a); ctx.stroke(); ctx.set_dash([])

def ill_3(ctx, t, a=1.0):
    rope(ctx, CX - 560 * U, CX + 560 * U, H * 0.42, t, a=a)
    rope(ctx, CX - 560 * U, CX + 560 * U, H * 0.58, t, a=a, col=PINK)
    card(ctx, "1 HOUR EACH", CX - 520 * U, H * 0.28, GOLD, a, 40)
    card(ctx, "UNEVEN BURN!", CX + 520 * U, H * 0.28, CORAL, a, 40)
    card(ctx, "GOAL: 45 MIN", CX, H * 0.71, CYAN, a, 44)

def ans_3(ctx, t, d, a=1.0):
    # minuterie animée : 0 → 30 min (corde A des 2 bouts, B d'un bout) puis 30 → 45 (B des 2 bouts)
    s1, s3, s4 = 1.2, ST("r3_a", 2), ST("r3_a", 3)
    m = 0.0 if t < s1 else (30 * clamp((t - s1) / max(1.0, s3 - s1)) if t < s3 else 30 + 15 * clamp((t - s3) / max(1.0, s4 - s3)))
    a_l = a_r = min(0.5, m / 60)
    b_l = min(0.5, m / 60) if m <= 30 else 0.5 + (m - 30) / 15 * 0.25
    b_r = 0.0 if m <= 30 else (m - 30) / 15 * 0.25
    y1, y2 = H * 0.40, H * 0.56
    rope(ctx, CX - 560 * U, CX + 560 * U, y1, t, a_l if m > 0 else 0, a_r if m > 0 else 0)
    rope(ctx, CX - 560 * U, CX + 560 * U, y2, t, b_l if m > 0 else 0, b_r, col=PINK)
    text(ctx, "A", CX - 620 * U, y1, 50 * U, GOLD); text(ctx, "B", CX - 620 * U, y2, 50 * U, PINK)
    big_answer(ctx, t, f"{int(m):02d} MIN", GREEN if m >= 45 else WHITE, prog(t, 0.5, 1.0), y=H * 0.19, size=120)
    if m >= 30: card(ctx, "A IS GONE: LIGHT B'S OTHER END", CX, H * 0.70, GOLD, prog(t, s3, s3 + 0.5), 40)
    elif m > 0: card(ctx, "A: BOTH ENDS   B: ONE END", CX, H * 0.70, CYAN, prog(t, s1, s1 + 0.5), 40)

# ---------- 4. le T-shirt ----------
def ellipse(c, cx, cy, rx, ry):
    c.save(); c.translate(cx, cy); c.scale(rx, ry); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()

def tshirt(ctx, cx, cy, s, a, t, rings=0.0):
    S = s * U
    ctx.save(); ctx.translate(cx, cy); ctx.scale(S, S)
    def body(c):
        c.move_to(-90, -300); c.curve_to(-40, -250, 40, -250, 90, -300); c.line_to(300, -220); c.line_to(380, -40); c.line_to(230, 10)
        c.line_to(220, 330); c.line_to(-220, 330); c.line_to(-230, 10); c.line_to(-380, -40); c.line_to(-300, -220); c.close_path()
    glow(ctx, 0, 0, 480, PINK, 0.3 * a)
    ctx.new_path(); body(ctx); g = cairo.LinearGradient(-380, 0, 380, 0)
    g.add_color_stop_rgba(0, *mix(PINK, NAVY, 0.4), a); g.add_color_stop_rgba(0.5, *mix(PINK, WHITE, 0.15), a); g.add_color_stop_rgba(1, *mix(PINK, NAVY, 0.4), a)
    ctx.set_source(g); ctx.fill()
    neon_path(ctx, body, PINK, 5, a)
    if rings > 0:
        for (ox, oy, orx, ory, an) in ((0, -268, 95, 28, 0), (0, 330, 220, 30, 0), (-305, -12, 80, 24, 1.2), (305, -12, 80, 24, -1.2)):
            ctx.save(); ctx.translate(ox, oy); ctx.rotate(an)
            neon_path(ctx, lambda c, orx=orx, ory=ory: ellipse(c, 0, 0, orx, ory), GOLD, 7, rings * a)
            ctx.restore()
    ctx.restore()

def three_holes(ctx, cx, cy, s, a=1.0, t=0.0):
    """La forme aplatie à 3 trous (le T-shirt étiré sans le déchirer)."""
    S = s * U
    ctx.save(); ctx.translate(cx, cy); ctx.scale(S, S)
    ctx.new_path(); rrect(ctx, -460, -150, 920, 300, 150); g = cairo.LinearGradient(-460, 0, 460, 0)
    g.add_color_stop_rgba(0, *mix(PINK, NAVY, 0.4), a); g.add_color_stop_rgba(1, *mix(PINK, WHITE, 0.2), a); ctx.set_source(g); ctx.fill()
    for hx in (-270, 0, 270):
        ctx.new_path(); ellipse(ctx, hx, 0, 85, 70); rgba(ctx, (0.02, 0.01, 0.06), a); ctx.fill()
        neon_path(ctx, lambda c, hx=hx: ellipse(c, hx, 0, 85, 70), GOLD, 6, a)
    neon_path(ctx, lambda c: rrect(c, -460, -150, 920, 300, 150), PINK, 5, a)
    ctx.restore()

def ill_4(ctx, t, a=1.0):
    tshirt(ctx, CX, H * 0.47, 0.62, a, t, rings=0.5 + 0.5 * math.sin(t * 2))

def ans_4(ctx, t, d, a=1.0):
    s1, s2, s3 = ST("r4_a", 1), ST("r4_a", 2), ST("r4_a", 3)
    big_answer(ctx, t, "3 HOLES", GREEN, prog(t, 1.0, 1.6), y=H * 0.17, size=120)
    k = prog(t, s3 + 0.5, s3 + 2.3)
    if k < 1: tshirt(ctx, CX - 330 * U * k, H * 0.52, 0.55 * (1 - 0.3 * k), 1 - k, t, rings=prog(t, s1, s1 + 1.0))
    if k > 0: three_holes(ctx, CX, H * 0.52, 0.8, k, t)
    if t > s2 and k < 0.5:
        card(ctx, "4 OPENINGS − 1 = 3 HOLES", CX + 520 * U, H * 0.70, GOLD, prog(t, s2, s2 + 0.6) * (1 - 2 * k), 40)

# ---------- 5. la corde autour de la Terre ----------
def earth(ctx, cx, cy, r, t, a=1.0):
    glow(ctx, cx, cy, r * 1.4, CYAN, 0.35 * a)
    g = cairo.RadialGradient(cx - r * 0.35, cy - r * 0.35, r * 0.1, cx, cy, r)
    g.add_color_stop_rgba(0, 0.30, 0.65, 1.0, a); g.add_color_stop_rgba(1, 0.05, 0.20, 0.55, a)
    ctx.new_path(); ctx.arc(cx, cy, r, 0, 2 * math.pi); ctx.set_source(g); ctx.fill()
    rnd = random.Random(2)
    ctx.save(); ctx.new_path(); ctx.arc(cx, cy, r, 0, 2 * math.pi); ctx.clip()
    for i in range(7):   # continents stylisés qui défilent lentement
        ox = cx + ((rnd.uniform(-1, 1) * r + t * 18 * U) % (2.4 * r)) - 1.2 * r; oy = cy + rnd.uniform(-0.7, 0.7) * r
        ctx.new_path(); ctx.save(); ctx.translate(ox, oy); ctx.scale(rnd.uniform(0.6, 1.4) * r * 0.22, rnd.uniform(0.4, 0.9) * r * 0.16)
        ctx.arc(0, 0, 1, 0, 2 * math.pi); ctx.restore(); rgba(ctx, GREEN, 0.75 * a); ctx.fill()
    ctx.restore()
    neon_path(ctx, lambda c: c.arc(cx, cy, r, 0, 2 * math.pi), CYAN, 3 * U, 0.8 * a)

def ill_5(ctx, t, a=1.0, gap=0.0):
    r = 260 * U
    earth(ctx, CX, H * 0.50, r, t, a)
    neon_path(ctx, lambda c: c.arc(CX, H * 0.50, r + 6 * U + gap, 0, 2 * math.pi), GOLD, 5 * U, a)
    card(ctx, "≈ 25,000 MILES", CX - 560 * U, H * 0.36, GOLD, a, 42)
    card(ctx, "+ 3 FEET", CX + 560 * U, H * 0.36, GREEN, a, 48)

def mouse(ctx, x, y, s, a=1.0):
    S = s * U
    ctx.new_path(); ctx.save(); ctx.translate(x, y); ctx.scale(S * 1.4, S); ctx.arc(0, 0, 30, 0, 2 * math.pi); ctx.restore(); rgba(ctx, (0.75, 0.75, 0.8), a); ctx.fill()
    circle(ctx, x + 38 * S, y - 10 * S, 17 * S, (0.78, 0.78, 0.84), a); circle(ctx, x + 32 * S, y - 30 * S, 10 * S, PINK, a)
    circle(ctx, x + 48 * S, y - 13 * S, 3 * S, (0.05, 0.05, 0.1), a)
    ctx.move_to(x - 40 * S, y); ctx.curve_to(x - 80 * S, y - 10 * S, x - 90 * S, y + 25 * S, x - 120 * S, y + 10 * S); ctx.set_line_width(3 * S); rgba(ctx, PINK, a); ctx.stroke()

def ans_5(ctx, t, d, a=1.0):
    s1, s2m, s3b = ST("r5_a", 1), ST("r5_a", 2), ST("r5_a", 3)
    big_answer(ctx, t, "≈ 6 INCHES", GREEN, prog(t, 1.0, 1.6), y=H * 0.15, size=110)
    gap = 40 * U * prog(t, 1.5, 3.5)
    ill_5(ctx, t, 0.9, gap)
    if t > s1:
        card(ctx, "RISE = 3 FT ÷ (2 × PI) ≈ 5.7 IN", CX, H * 0.75, GOLD, prog(t, s1, s1 + 0.6), 40)
    if t > s2m:
        mouse(ctx, CX, H * 0.50 - 260 * U - 20 * U, 0.6, prog(t, s2m, s2m + 0.7))
        kb = prog(t, s3b, s3b + 0.6)
        ball(ctx, CX + 650 * U, H * 0.63, 80 * U, kb)
        if kb > 0:
            neon_path(ctx, lambda c: c.arc(CX + 650 * U, H * 0.63, 80 * U + 40 * U, 0, 2 * math.pi), GOLD, 4 * U, kb)
            card(ctx, "SAME GAP!", CX + 650 * U, H * 0.455, GREEN, kb, 40)

# ---------- 6. les anniversaires ----------
def person(ctx, x, y, s, col, a=1.0):
    S = s * U
    circle(ctx, x, y - 30 * S, 16 * S, col, a)
    ctx.new_path(); ctx.move_to(x - 22 * S, y + 28 * S); ctx.curve_to(x - 22 * S, y - 10 * S, x + 22 * S, y - 10 * S, x + 22 * S, y + 28 * S); ctx.close_path()
    rgba(ctx, col, a); ctx.fill()

def crowd(ctx, n, t, a=1.0, match=False):
    cols = [CYAN, PINK, GOLD, GREEN, PURPLE, CORAL]
    for i in range(n):
        r_, c_ = divmod(i, 8)
        x = CX - 3.5 * 120 * U + c_ * 120 * U; y = H * 0.36 + r_ * 125 * U
        col = cols[i % 6]
        if match and i in (5, 17): col = GOLD; glow(ctx, x, y, 80 * U, GOLD, 0.5 * a)
        person(ctx, x, y + 4 * U * math.sin(t * 3 + i), 1.4, col, a)
    if match:
        neon_path(ctx, lambda c: (c.move_to(CX - 3.5 * 120 * U + 5 * 120 * U, H * 0.36 - 60 * U),
                                  c.curve_to(CX + 600 * U, H * 0.25, CX + 600 * U, H * 0.36 + 2 * 125 * U, CX - 3.5 * 120 * U + 1 * 120 * U, H * 0.36 + 2 * 125 * U - 60 * U)), GOLD, 4 * U, a)

def ill_6(ctx, t, a=1.0):
    n = 1 + int(22 * clamp(t / 5.0))
    crowd(ctx, n, t, a)
    card(ctx, f"{n} PEOPLE", CX + 690 * U, H * 0.30, GOLD, a, 44)
    card(ctx, "365 DAYS", CX - 690 * U, H * 0.30, CYAN, a, 44)

def ans_6(ctx, t, d, a=1.0):
    big_answer(ctx, t, "JUST 23", GREEN, prog(t, 1.2, 1.8), y=H * 0.17, size=120)
    sp, s2, s3 = ST("r6_a", 1) + 3.5, ST("r6_a", 2), ST("r6_a", 3)
    crowd(ctx, 23, t, 0.9, match=t > sp)
    if t > sp: card(ctx, "23 PEOPLE = 253 PAIRS", CX - 560 * U, H * 0.72, GOLD, prog(t, sp, sp + 0.6), 40)
    if t > s2: card(ctx, "23 → 50.7%", CX + 200 * U, H * 0.72, GREEN, prog(t, s2, s2 + 0.6), 40)
    if t > s3: card(ctx, "70 → 99.9%", CX + 600 * U, H * 0.72, CYAN, prog(t, s3, s3 + 0.6), 40)

# ---------- 7. les trois portes ----------
def goat(ctx, x, y, s, a=1.0):
    S = s * U; col = (0.85, 0.85, 0.9)
    ctx.new_path(); ctx.save(); ctx.translate(x, y); ctx.scale(S * 1.5, S); ctx.arc(0, 0, 40, 0, 2 * math.pi); ctx.restore(); rgba(ctx, col, a); ctx.fill()
    circle(ctx, x + 60 * S, y - 40 * S, 22 * S, col, a)
    for lx in (-35, -12, 15, 38):
        ctx.move_to(x + lx * S, y + 25 * S); ctx.line_to(x + lx * S, y + 70 * S); ctx.set_line_width(7 * S); rgba(ctx, col, a); ctx.stroke()
    for hx in (52, 68):
        ctx.move_to(x + hx * S, y - 58 * S); ctx.curve_to(x + (hx - 10) * S, y - 85 * S, x + (hx - 25) * S, y - 85 * S, x + (hx - 30) * S, y - 75 * S)
        ctx.set_line_width(4 * S); rgba(ctx, GOLD, a); ctx.stroke()

def car(ctx, x, y, s, a=1.0):
    S = s * U
    glow(ctx, x, y, 160 * S, GOLD, 0.5 * a)
    ctx.new_path(); ctx.move_to(x - 110 * S, y + 20 * S); ctx.line_to(x - 100 * S, y - 15 * S); ctx.line_to(x - 50 * S, y - 25 * S); ctx.line_to(x - 25 * S, y - 60 * S)
    ctx.line_to(x + 45 * S, y - 60 * S); ctx.line_to(x + 75 * S, y - 25 * S); ctx.line_to(x + 110 * S, y - 15 * S); ctx.line_to(x + 115 * S, y + 20 * S); ctx.close_path()
    rgba(ctx, CORAL, a); ctx.fill()
    for wx in (-60, 65): circle(ctx, x + wx * S, y + 22 * S, 22 * S, (0.08, 0.08, 0.12), a); circle(ctx, x + wx * S, y + 22 * S, 9 * S, (0.7, 0.7, 0.75), a)
    rrect(ctx, x - 15 * S, y - 52 * S, 50 * S, 26 * S, 5 * S); rgba(ctx, CYAN, 0.8 * a); ctx.fill()

def door(ctx, x, y, n, a=1.0, open_k=0.0, content=None, hl=None):
    w_, h_ = 230 * U, 360 * U
    if content and open_k > 0.3:
        (goat if content == "goat" else car)(ctx, x, y + 60 * U, 1.0 if content == "goat" else 1.05, a * prog(open_k, 0.3, 0.9))
    col = hl or [CYAN, PINK, PURPLE][n - 1]
    ww = w_ * (1 - 0.85 * open_k)
    ctx.new_path(); ctx.rectangle(x - w_ / 2, y - h_ / 2, ww, h_)
    g = cairo.LinearGradient(x - w_ / 2, 0, x + w_ / 2, 0); g.add_color_stop_rgba(0, *mix(col, NAVY, 0.55), a); g.add_color_stop_rgba(1, *mix(col, NAVY, 0.25), a)
    ctx.set_source(g); ctx.fill()
    neon_path(ctx, lambda c: c.rectangle(x - w_ / 2, y - h_ / 2, w_, h_), col, 5 * U, a)
    if open_k < 0.5: text(ctx, str(n), x - w_ / 2 + ww / 2, y - 40 * U, 110 * U, WHITE, a * (1 - open_k * 2))
    if open_k < 0.5: circle(ctx, x - w_ / 2 + ww - 30 * U, y + 30 * U, 10 * U, GOLD, a * (1 - open_k * 2))

def ill_7(ctx, t, a=1.0):
    for n, x in ((1, CX - 330 * U), (2, CX), (3, CX + 330 * U)):
        s2 = ST("r7_q", 3)
        ok = prog(t, s2 + 2.4, s2 + 3.8) if n == 3 else 0.0
        door(ctx, x, H * 0.52, n, a, ok, "goat" if n == 3 else None, GOLD if n == 1 and t > s2 else None)
    if t > ST("r7_q", 3): card(ctx, "YOUR PICK", CX - 330 * U, H * 0.25, GOLD, prog(t, ST("r7_q", 3), ST("r7_q", 3) + 0.5), 36)

def ans_7(ctx, t, d, a=1.0):
    big_answer(ctx, t, "SWITCH!", GREEN, prog(t, 1.2, 1.8), y=H * 0.15, size=120)
    # trois cas possibles (voiture derrière la porte 1, 2 ou 3) : rester gagne 1 fois, changer gagne 2 fois
    s1, s2, s3 = ST("r7_a", 1), ST("r7_a", 2), ST("r7_a", 3)
    if t < s2:
        for n, x in ((1, CX - 330 * U), (2, CX), (3, CX + 330 * U)):
            door(ctx, x, H * 0.50, n, 1.0, 0.0, None, GOLD if n == 1 else None)
        card(ctx, "YOUR DOOR: 1/3", CX - 330 * U, H * 0.75, GOLD, prog(t, s1 + 0.5, s1 + 1.0), 36)
        card(ctx, "THE OTHER TWO: 2/3", CX + 165 * U, H * 0.75 - 0 * U, GREEN, prog(t, s1 + 2.5, s1 + 3.0), 36)
    else:
        rows = [("CAR BEHIND 1", "STAY WINS", GOLD), ("CAR BEHIND 2", "SWITCH WINS", GREEN), ("CAR BEHIND 3", "SWITCH WINS", GREEN)]
        for j, (l, r, col) in enumerate(rows):
            k = prog(t, s2 + j * 1.2, s2 + 0.6 + j * 1.2)
            card(ctx, l, CX - 300 * U, H * (0.34 + 0.12 * j), WHITE, k, 40)
            card(ctx, r, CX + 300 * U, H * (0.34 + 0.12 * j), col, k, 40)
        if t > s2 + 4.0 and t < s3: card(ctx, "STAY: 1/3   SWITCH: 2/3", CX, H * 0.73, GREEN, prog(t, s2 + 4.0, s2 + 4.6), 44)
        if t >= s3: card(ctx, "1990: THOUSANDS OF READERS SAID IT WAS WRONG", CX, H * 0.73, CORAL, prog(t, s3, s3 + 0.6), 38)

ILL = [ill_1, ill_2, ill_3, ill_4, ill_5, ill_6, ill_7]
ANS = [ans_1, ans_2, ans_3, ans_4, ans_5, ans_6, ans_7]

# ---------- scènes génériques ----------
def mk_q(i):
    def sc(ctx, t, d):
        bg(ctx, t, i); header(ctx, i)
        k = prog(t, 0.0, 0.5)
        neon_text(ctx, RECAP[i][0], CX, H * 0.18, 52 * U, WHITE, k, TINT[i], fill=0.2)
        ILL[i](ctx, t, k)
        if i in OPTIONS:
            so = ST(f"r{i + 1}_q", len(_TL[f"r{i + 1}_q"]["sents"]) - 1)
            options_row(ctx, t, OPTIONS[i], H * 0.77 - 30 * U, prog(t, so, so + 0.5))
    return sc

def mk_t(i):
    def sc(ctx, t, d):
        bg(ctx, t, i); header(ctx, i)
        DUR = 15.0   # temps de réflexion (Nazik, 2026-11-13 : 60 s trop long → 15 s + « pause the video »)
        start = max(0.0, d - DUR - 0.3); left = DUR if t < start else max(0.0, DUR - (t - start))
        # rappel de l'énigme (à gauche) + chrono (à droite)
        neon_text(ctx, RECAP[i][0], CX - 300 * U, H * 0.24, 42 * U, WHITE, 1.0, TINT[i], fill=0.2)
        neon_text(ctx, RECAP[i][1], CX - 300 * U, H * 0.31, 40 * U, GOLD, 1.0, TINT[i], fill=0.2)
        ctx.save(); ctx.translate(CX - 330 * U, H * 0.53); ctx.scale(0.5, 0.5); ctx.translate(-CX, -H * 0.55)
        ILL[i](ctx, 20.0 + t * 0.2, 0.75); ctx.restore()
        if i in OPTIONS: options_row(ctx, t, OPTIONS[i], H * 0.755, 0.9, cx=CX - 330 * U, sc=0.8)
        x, y, r = CX + 560 * U, H * 0.45, 190 * U
        frac = left / DUR; col = GREEN if left > 8 else (GOLD if left > 3 else CORAL)
        glow(ctx, x, y, r * 1.6, col, 0.35)
        ctx.new_path(); ctx.arc(x, y, r, 0, 2 * math.pi); ctx.set_line_width(22 * U); rgba(ctx, (0.2, 0.2, 0.3), 0.6); ctx.stroke()
        neon_path(ctx, lambda c: c.arc(x, y, r, -math.pi / 2, -math.pi / 2 + 2 * math.pi * frac), col, 11 * U)
        pulse = 1 + 0.06 * math.exp(-((left % 1.0) - 0.98) ** 2 * 400) if left > 0 else 1
        ctx.save(); ctx.translate(x, y); ctx.scale(pulse, pulse); neon_text(ctx, str(int(math.ceil(left))), 0, 0, 170 * U, col, 1.0, WHITE, fill=0.35); ctx.restore()
        vk = 0.85 + 0.15 * math.sin(t * 4)
        font(ctx, 36 * U); vw = ctx.text_extents(VOTE[i]).width + 60 * U
        xb = min(x, W - vw / 2 - 30 * U)        # le bandeau reste entièrement dans l'image
        rrect(ctx, xb - vw / 2, H * 0.19 - 34 * U, vw, 68 * U, 34 * U); rgba(ctx, GOLD, vk); ctx.fill()
        text(ctx, VOTE[i], xb, H * 0.19, 36 * U, (0.03, 0.02, 0.08), 1.0)
        text(ctx, "PAUSE THE VIDEO", x, y + r + 70 * U, 40 * U, WHITE, 0.9)
        text(ctx, "IF YOU NEED MORE TIME", x, y + r + 118 * U, 32 * U, (0.8, 0.8, 0.9), 0.9)
        if t >= start + DUR / 2:   # indice à mi-temps
            card(ctx, HINTS[i], CX - 330 * U, H * 0.11 + 70 * U, CYAN, prog(t, start + DUR / 2, start + DUR / 2 + 0.5), 34)
    return sc

def mk_a(i):
    def sc(ctx, t, d):
        bg(ctx, t, i); header(ctx, i)
        ANS[i](ctx, t, d)
        if i in (0, 1, 2):
            sl = ST(f"r{i + 1}_a", len(_TL[f"r{i + 1}_a"]["sents"]) - 1); kp = prog(t, sl, sl + 0.4)
            if kp:
                ctx.save(); ctx.translate(W - 200 * U, H * 0.22); sc_ = 1 + 0.3 * (1 - kp); ctx.scale(sc_, sc_)
                glow(ctx, 0, 0, 120 * U, GOLD, 0.5 * kp); circle(ctx, 0, 0, 80 * U, GOLD, kp)
                text(ctx, "+1", 0, -8 * U, 64 * U, (0.03, 0.02, 0.08), kp); text(ctx, "POINT", 0, 40 * U, 22 * U, (0.03, 0.02, 0.08), kp)
                ctx.restore()
        if i in OPTIONS and i != 6:
            good = {3: 1, 4: 1, 5: 0}[i]
            s1 = ST(f"r{i + 1}_a", 1)
            options_row(ctx, t, OPTIONS[i], H * 0.74, prog(t, 0.6, 1.1) * (1 - prog(t, s1, s1 + 0.5)), good=good)
    return sc

def sc_intro(ctx, t, d):
    neon_bg(ctx, t, tint=PURPLE)
    k = prog(t, 0.0, 0.6)
    neon_text(ctx, "THE 7/7 CHALLENGE", CX, H * 0.20, 150 * U, GOLD, k, CORAL, fill=0.35)
    neon_text(ctx, "7 RIDDLES · 15 SECONDS EACH", CX, H * 0.36, 66 * U, CYAN, prog(t, ST("intro", 1), ST("intro", 1) + 0.6), PURPLE, fill=0.25)
    # vignettes des 7 énigmes qui apparaissent une à une
    for j in range(7):
        kk = prog(t, 1.0 + j * 0.35, 1.5 + j * 0.35)
        x = CX + (j - 3) * 230 * U; y = H * 0.62
        circle(ctx, x, y, 90 * U * kk, mix(TINT[j], NAVY, 0.6), kk)
        neon_path(ctx, lambda c, x=x, kk=kk: c.arc(x, y, 90 * U * max(kk, 0.01), 0, 2 * math.pi), TINT[j], 4 * U, kk)
        neon_text(ctx, str(j + 1), x, y, 90 * U, WHITE, kk, TINT[j], fill=0.3)
    text(ctx, "GRAB A PEN · COMMENT YOUR SCORE!", CX, H * 0.76, 44 * U, GOLD, prog(t, ST("intro", 2), ST("intro", 2) + 0.6))

SCALE = [("0–2", "BRAIN WARMING UP", CYAN), ("3–4", "SOLID LOGIC", GREEN), ("5–6", "SHARP MIND", GOLD), ("7/7", "GENIUS LEVEL", PINK)]
def sc_outro(ctx, t, d):
    neon_bg(ctx, t, tint=GOLD)
    s1, s2 = ST("outro", 1), ST("outro", 2)
    if t < s2:
        neon_text(ctx, "COUNT YOUR POINTS!", CX, H * 0.14, 90 * U, GOLD, prog(t, 0.0, 0.5), CORAL, fill=0.3)
        for j, (sc_, lab, col) in enumerate(SCALE):
            k = prog(t, s1 + j * 2.3, s1 + j * 2.3 + 0.5)
            y = H * (0.30 + 0.13 * j)
            card(ctx, sc_, CX - 380 * U, y, col, k, 66)
            card(ctx, lab, CX + 170 * U, y, col, k, 66)
    else:
        cta(ctx, t - s2, d - s2, "WHAT'S YOUR SCORE?", "COMMENT YOUR SCORE /7")

SCENES = {"intro": sc_intro, "outro": sc_outro}
for _i in range(7):
    SCENES[f"r{_i + 1}_q"] = mk_q(_i); SCENES[f"r{_i + 1}_t"] = mk_t(_i); SCENES[f"r{_i + 1}_a"] = mk_a(_i)
SHORT_SCENES = ["r7_q", "r7_t"]   # (pas de Short pour la vidéo longue du samedi)

def thumbnail(c):
    """Miniature 1280×720 : « 7 RIDDLES » + « 60 SECONDS EACH » + les 3 portes (une entrouverte) + « CAN YOU SOLVE THEM? »."""
    vgrad(c, (0.10, 0.04, 0.22), (0.01, 0.02, 0.08))
    glow(c, 900, 360, 600, PURPLE, 0.35)
    def tx(s_, x, y, sz, col):
        c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(sz)
        c.move_to(x + 6, y + 6); c.set_source_rgba(0, 0, 0, 0.75); c.show_text(s_)
        c.move_to(x, y); c.set_source_rgb(*col); c.show_text(s_)
    tx("7 RIDDLES", 50, 190, 150, GOLD)
    tx("15 SECONDS EACH", 55, 290, 70, CYAN)
    tx("TEST YOUR LOGIC: CAN YOU GET 7/7?", 55, 640, 58, WHITE)
    for n, x in ((1, 830), (2, 990), (3, 1150)):
        c.rectangle(x - 70, 250, 140, 220); c.set_source_rgba(*mix([CYAN, PINK, PURPLE][n - 1], NAVY, 0.4), 1); c.fill()
        c.rectangle(x - 70, 250, 140, 220); c.set_line_width(6); c.set_source_rgb(*[CYAN, PINK, PURPLE][n - 1]); c.stroke()
        c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(90)
        c.move_to(x - 26, 395); c.set_source_rgb(1, 1, 1); c.show_text(str(n) if n != 2 else "?")
    c.arc(1180, 130, 70, 0, 2 * math.pi); c.set_source_rgb(*CORAL); c.fill()
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(48)
    c.move_to(1142, 147); c.set_source_rgb(1, 1, 1); c.show_text("15s")
