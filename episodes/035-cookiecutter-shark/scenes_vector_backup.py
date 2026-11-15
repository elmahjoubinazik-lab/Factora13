# Episode 035 (Short seul, 9:16, ~34 s) - "What makes these perfect circles on whales?" — le requin emporte-pièce.
# Sujet proposé par Nazik (2026-11-15), dossier validé ; règles du master prompt : quiz à 3 réponses, réponse dans la vidéo,
# 2e surprise (sous-marins), fin marquante (bioluminescence). Voix ElevenLabs « Jessica ». Dessins maison, sans IA.
# Faits : Isistius brasiliensis, ≈ 42–56 cm (≈ 20 in) ; se fixe avec des lèvres en ventouse, plante ses dents inférieures et
# tourne sur lui-même pour découper un morceau rond (Jones 1971) ; a endommagé les dômes de sonar en caoutchouc de
# sous-marins de l'US Navy (années 1970) ; photophores ventraux à lumière verte. Toutes les tailles en multiples de U.
import json as _json
_TL = {sg["scene"]: sg for sg in _json.load(open(EP + "/build/timeline.json", encoding="utf-8"))}
def ST(scene, k):
    sg = _TL.get(scene)
    return sg["sents"][k]["start"] - sg["start"] if sg and k < len(sg["sents"]) else 1e9
def EN(scene, k):
    sg = _TL.get(scene)
    return sg["sents"][k]["end"] - sg["start"] if sg and k < len(sg["sents"]) else 1e9

DEEP1, DEEP2 = (0.02, 0.08, 0.22), (0.0, 0.01, 0.05)
DARK = (0.03, 0.02, 0.08)

def bg(ctx, t, tint=CYAN, dark=0.0):
    neon_bg(ctx, t, mix(DEEP1, (0, 0, 0), dark), DEEP2, tint)
    for i in range(4):   # rayons de lumière venus de la surface
        x0 = W * (0.15 + 0.23 * i) + 40 * U * math.sin(t * 0.4 + i)
        ctx.new_path(); ctx.move_to(x0 - 30 * U, 0); ctx.line_to(x0 + 30 * U, 0); ctx.line_to(x0 + 260 * U, H * 0.75); ctx.line_to(x0 + 120 * U, H * 0.75); ctx.close_path()
        g = cairo.LinearGradient(0, 0, 0, H * 0.75); g.add_color_stop_rgba(0, 0.5, 0.85, 1.0, 0.10 * (1 - dark)); g.add_color_stop_rgba(1, 0.5, 0.85, 1.0, 0)
        ctx.set_source(g); ctx.fill()

def fit_neon(ctx, s, x, y, size, maxw, col, col2, a=1.0, fill=0.3):
    font(ctx, size); w_ = ctx.text_extents(s).width
    neon_text(ctx, s, x, y, size * min(1.0, maxw / w_), col, a, col2, fill=fill)

def pill(ctx, s, x, y, col, size=46, a=1.0):
    if a <= 0: return
    font(ctx, size * U); w_ = ctx.text_extents(s).width + 60 * U
    rrect(ctx, x - w_ / 2, y - size * 0.8 * U, w_, size * 1.6 * U, size * 0.8 * U); rgba(ctx, col, 0.96 * a); ctx.fill()
    text(ctx, s, x, y, size * U, DARK, a)

def ell(c, x, y, rx, ry):
    c.save(); c.translate(x, y); c.scale(rx, ry); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()

# ---------------------------------------------------------------- la baleine (vue de profil, tête à gauche)
SCARS = [(-262, -72, 26), (-120, -48, 22), (22, -98, 24), (150, -22, 28), (-55, 58, 20), (292, -52, 19), (-205, 36, 18), (85, 42, 22)]
def whale_body(c):
    c.move_to(-480, 10)
    c.curve_to(-482, -70, -420, -135, -300, -150); c.curve_to(-150, -168, 80, -150, 250, -100)
    c.curve_to(340, -72, 400, -45, 445, -30); c.curve_to(480, -60, 520, -110, 575, -125)
    c.curve_to(560, -80, 530, -30, 515, -12); c.curve_to(535, 15, 565, 60, 580, 85)
    c.curve_to(520, 70, 480, 30, 445, 8); c.curve_to(380, 30, 250, 90, 60, 128)
    c.curve_to(-120, 160, -330, 150, -420, 105); c.curve_to(-460, 80, -478, 50, -480, 10); c.close_path()
def whale_flipper(c):
    c.move_to(-250, 95); c.curve_to(-210, 170, -150, 260, -95, 300); c.curve_to(-75, 300, -80, 280, -100, 250)
    c.curve_to(-140, 190, -160, 140, -170, 110); c.close_path()

def whale(ctx, cx, cy, s, a=1.0, t=0.0, scars=1.0, pulse=True):
    if a <= 0: return
    S = s * U
    ctx.save(); ctx.translate(cx, cy + 6 * U * math.sin(t * 1.3)); ctx.scale(S, S)
    glow(ctx, 0, 0, 640, CYAN, 0.22 * a)
    ctx.new_path(); whale_flipper(ctx); rgba(ctx, (0.16, 0.30, 0.52), a); ctx.fill()
    neon_path(ctx, whale_flipper, CYAN, 4, 0.8 * a)
    ctx.new_path(); whale_body(ctx); g = cairo.LinearGradient(0, -170, 0, 160)
    g.add_color_stop_rgba(0, 0.08, 0.18, 0.38, a); g.add_color_stop_rgba(0.55, 0.16, 0.32, 0.56, a); g.add_color_stop_rgba(1, 0.50, 0.68, 0.85, a)
    ctx.set_source(g); ctx.fill()
    ctx.save(); ctx.new_path(); whale_body(ctx); ctx.clip()        # sillons de la gorge
    for k in range(6):
        ctx.new_path(); ctx.move_to(-455, 52 + k * 12); ctx.curve_to(-380, 80 + k * 14, -300, 92 + k * 14, -230, 92 + k * 12)
        ctx.set_line_width(3); rgba(ctx, (0.85, 0.92, 1.0), 0.25 * a); ctx.stroke()
    ctx.restore()
    ctx.new_path(); ctx.move_to(118, -138); ctx.line_to(176, -176); ctx.line_to(205, -126); ctx.close_path(); rgba(ctx, (0.08, 0.18, 0.38), a); ctx.fill()
    neon_path(ctx, whale_body, CYAN, 5, a)
    ctx.new_path(); ctx.move_to(-478, 26); ctx.curve_to(-420, 42, -350, 46, -300, 34); ctx.set_line_width(4); rgba(ctx, (0.02, 0.05, 0.12), 0.9 * a); ctx.stroke()
    circle(ctx, -332, 6, 9, (0.02, 0.03, 0.08), a); circle(ctx, -329, 3, 3, WHITE, a)
    for i, (x, y, r) in enumerate(SCARS):     # cicatrices rondes (cicatrisées : pas de sang)
        k = scars * (0.75 + 0.25 * math.sin(t * 3 + i)) if pulse else scars
        if k <= 0: continue
        glow(ctx, x, y, r * 2.4, (0.75, 0.95, 1.0), 0.35 * k * a)
        circle(ctx, x, y, r, (0.80, 0.90, 0.98), 0.75 * k * a)
        circle(ctx, x, y, r * 0.62, (0.55, 0.68, 0.82), 0.85 * k * a)
        neon_path(ctx, lambda c, x=x, y=y, r=r: c.arc(x, y, r, 0, 2 * math.pi), WHITE, 3, k * a)
    ctx.restore()

def whale_pt(cx, cy, s, x, y, t=0.0):
    S = s * U; return cx + x * S, cy + 6 * U * math.sin(t * 1.3) + y * S

# ---------------------------------------------------------------- le requin emporte-pièce (tête à gauche)
def shark_body(c):
    c.move_to(-150, 2); c.curve_to(-152, -30, -120, -46, -70, -48); c.line_to(100, -40)
    c.curve_to(130, -37, 150, -30, 160, -20); c.line_to(200, -52); c.line_to(214, -42); c.line_to(192, -2)
    c.line_to(212, 34); c.line_to(198, 44); c.line_to(160, 16); c.curve_to(120, 30, 40, 42, -60, 44)
    c.curve_to(-115, 44, -148, 30, -150, 2); c.close_path()

def shark(ctx, cx, cy, s, a=1.0, t=0.0, glow_k=0.0, roll=1.0, teeth=0.0):
    """Corps en cigare brun, collier sombre derrière la tête, grosses lèvres en ventouse, gros œil vert,
    petites nageoires dorsales très en arrière, ventre couvert de photophores (lueur verte si glow_k > 0)."""
    if a <= 0: return
    S = s * U
    ctx.save(); ctx.translate(cx, cy); ctx.scale(S, S * roll)
    if glow_k > 0:
        glow(ctx, 0, 60, 260, GREEN, 0.55 * glow_k * a); glow(ctx, 0, 40, 160, GREEN, 0.5 * glow_k * a)
    for tri in (((55, -45), (75, -68), (92, -43)), ((110, -39), (127, -57), (140, -35)), ((-55, 40), (-28, 68), (-14, 42))):
        ctx.new_path(); ctx.move_to(*tri[0]); ctx.line_to(*tri[1]); ctx.line_to(*tri[2]); ctx.close_path()
        rgba(ctx, (0.30, 0.22, 0.20), a); ctx.fill_preserve(); ctx.set_line_width(3); rgba(ctx, CORAL, 0.8 * a); ctx.stroke()
    ctx.new_path(); shark_body(ctx); g = cairo.LinearGradient(0, -50, 0, 46)
    g.add_color_stop_rgba(0, 0.30, 0.22, 0.20, a); g.add_color_stop_rgba(0.6, 0.48, 0.36, 0.32, a); g.add_color_stop_rgba(1, 0.62, 0.52, 0.46, a)
    ctx.set_source(g); ctx.fill()
    ctx.save(); ctx.new_path(); shark_body(ctx); ctx.clip()
    ctx.rectangle(-96, -60, 26, 120); rgba(ctx, (0.10, 0.07, 0.07), 0.92 * a); ctx.fill()           # le collier sombre
    for x in range(-128, 160, 13):                                                                  # photophores du ventre
        if -98 < x < -68: continue
        yb = 34 if x < 100 else 34 - (x - 100) * 0.35
        circle(ctx, x, yb, 3.4, mix((0.75, 0.70, 0.62), GREEN, glow_k), (0.5 + 0.5 * glow_k) * a)
    ctx.restore()
    neon_path(ctx, shark_body, CORAL, 4, a)
    ell(ctx, -139, 22, 17, 10); rgba(ctx, (0.95, 0.62, 0.62), a); ctx.fill()                       # lèvres en ventouse
    ctx.new_path(); ell(ctx, -139, 22, 17, 10); ctx.set_line_width(2.5); rgba(ctx, (0.6, 0.25, 0.25), a); ctx.stroke()
    if teeth > 0:
        for i in range(7):
            x = -152 + i * 5.5
            ctx.new_path(); ctx.move_to(x - 2.6, 26); ctx.line_to(x, 26 + 12 * teeth); ctx.line_to(x + 2.6, 26); ctx.close_path(); rgba(ctx, WHITE, a); ctx.fill()
    glow(ctx, -113, -14, 22, GREEN, 0.5 * a); circle(ctx, -113, -14, 10, GREEN, a); circle(ctx, -110, -15, 4.5, (0.02, 0.05, 0.03), a)
    ctx.restore()

# ---------------------------------------------------------------- le sous-marin (tête à gauche)
def sub_hull(c):
    c.move_to(-430, -90); c.line_to(400, -90); c.curve_to(470, -88, 520, -40, 560, -10); c.line_to(560, 10)
    c.curve_to(520, 40, 470, 88, 400, 90); c.line_to(-430, 90); c.close_path()
def sonar_dome(c):
    c.move_to(-430, -90); c.curve_to(-520, -88, -570, -45, -570, 0); c.curve_to(-570, 45, -520, 88, -430, 90); c.close_path()

def submarine(ctx, cx, cy, s, a=1.0, t=0.0, bites=1.0):
    S = s * U
    ctx.save(); ctx.translate(cx, cy + 5 * U * math.sin(t * 1.1)); ctx.scale(S, S)
    glow(ctx, 0, 0, 640, (0.4, 0.5, 0.7), 0.18 * a)
    ctx.new_path(); ctx.move_to(-170, -88); ctx.line_to(-150, -190); ctx.line_to(-20, -190); ctx.line_to(10, -88); ctx.close_path()   # kiosque
    rgba(ctx, (0.16, 0.18, 0.24), a); ctx.fill_preserve(); ctx.set_line_width(4); rgba(ctx, (0.7, 0.8, 0.95), 0.8 * a); ctx.stroke()
    ctx.new_path(); ctx.move_to(-200, -150); ctx.line_to(-150, -150); ctx.set_line_width(14); rgba(ctx, (0.16, 0.18, 0.24), a); ctx.stroke()
    for y0 in (-1, 1):                                                                                        # gouvernails arrière
        ctx.new_path(); ctx.move_to(470, y0 * 60); ctx.line_to(540, y0 * 140); ctx.line_to(565, y0 * 140); ctx.line_to(540, y0 * 30); ctx.close_path()
        rgba(ctx, (0.16, 0.18, 0.24), a); ctx.fill()
    ctx.new_path(); sub_hull(ctx); g = cairo.LinearGradient(0, -90, 0, 90)
    g.add_color_stop_rgba(0, 0.30, 0.34, 0.42, a); g.add_color_stop_rgba(0.5, 0.18, 0.20, 0.26, a); g.add_color_stop_rgba(1, 0.08, 0.09, 0.12, a)
    ctx.set_source(g); ctx.fill()
    neon_path(ctx, sub_hull, (0.75, 0.85, 1.0), 4, 0.8 * a)
    ctx.new_path(); sonar_dome(ctx); rgba(ctx, (0.10, 0.08, 0.06), a); ctx.fill()                            # dôme de sonar en caoutchouc
    neon_path(ctx, sonar_dome, GOLD, 6, a)
    for i, (x, y, r) in enumerate(((-505, -40, 16), (-470, 30, 14), (-540, 12, 12))):                       # morsures rondes
        k = bites * prog(t, 0.3 + 0.25 * i, 0.6 + 0.25 * i)
        if k: circle(ctx, x, y, r * k, (0.55, 0.45, 0.30), a); neon_path(ctx, lambda c, x=x, y=y, r=r, k=k: c.arc(x, y, r * k, 0, 2 * math.pi), CORAL, 3, a)
    for x in (300, 360, 420):
        circle(ctx, x, -20, 6, (0.4, 0.45, 0.55), a)
    ctx.restore()

# ---------------------------------------------------------------- scènes
WCX = CX - 50 * 0.95 * U        # centre de la baleine (le dessin est plus long côté queue)

def sc_hook(ctx, t, d):
    bg(ctx, t, CYAN)
    whale(ctx, WCX, H * 0.43, 0.95, 1.0, t, scars=1.0)
    fit_neon(ctx, "PERFECT CIRCLES", CX, H * 0.115, 112 * U, W * 0.86, GOLD, CORAL, 1.0, fill=0.35)
    fit_neon(ctx, "ON WHALES?", CX, H * 0.182, 150 * U, W * 0.80, WHITE, CYAN, 1.0, fill=0.3)
    s1 = ST("hook", 1)
    for i, si in enumerate((0, 3, 5)):           # « ? » sur 3 cicatrices quand la voix dit « no one knew »
        x, y = whale_pt(WCX, H * 0.43, 0.95, SCARS[si][0], SCARS[si][1] - 80, t)
        k = prog(t, s1 + 0.3 * i, s1 + 0.3 * i + 0.3)
        if k: neon_text(ctx, "?", x, y, 90 * U * (0.6 + 0.4 * k), GOLD, k, CORAL, fill=0.4)

OPTS = [("1", "A GIANT SHARK", CYAN), ("2", "A PARASITE", CORAL), ("3", "A FISH SHORTER THAN YOUR ARM", PURPLE)]
def option_card(ctx, n, s_, col, y, k, good=False, dim=False):
    if k <= 0: return
    pw, ph = W * 0.84, 120 * U; x = CX + (1 - ease(k)) * W * 0.5
    a = 0.35 if dim else 1.0
    if good: col = GREEN; glow(ctx, x, y, pw * 0.6, GREEN, 0.45)
    rrect(ctx, x - pw / 2, y - ph / 2, pw, ph, ph / 2); rgba(ctx, (0.04, 0.03, 0.10), 0.9 * k); ctx.fill()
    rrect(ctx, x - pw / 2, y - ph / 2, pw, ph, ph / 2); ctx.set_line_width(7 * U); rgba(ctx, col, k * a); ctx.stroke()
    circle(ctx, x - pw / 2 + ph / 2, y, ph * 0.38, col, k * a); text(ctx, n, x - pw / 2 + ph / 2, y, 64 * U, DARK, k)
    font(ctx, 58 * U); tw = ctx.text_extents(s_).width; sz = 58 * U * min(1.0, (pw - ph * 1.5) / tw)
    text(ctx, s_, x + ph * 0.45, y, sz, WHITE, k * a)

def sc_ask(ctx, t, d):
    bg(ctx, t, PURPLE)
    whale(ctx, WCX, H * 0.29, 0.62, 0.45, t, scars=0.8)
    s0, e0 = ST("ask", 0), EN("ask", 0); L = e0 - s0
    for i, (n, s_, col) in enumerate(OPTS):
        option_card(ctx, n, s_, col, H * (0.455 + 0.085 * i), prog(t, s0 + L * [0.0, 0.27, 0.48][i], s0 + L * [0.0, 0.27, 0.48][i] + 0.35))
    if t < e0 + 0.1:
        fit_neon(ctx, "WHAT MADE THEM?", CX, H * 0.11, 120 * U, W * 0.86, GOLD, CORAL, prog(t, 0, 0.3), fill=0.35)
    else:                                       # compte à rebours pendant la pause
        left = max(0.0, (d - 0.1) - t); n = max(1, min(3, int(math.ceil(left / max(0.3, (d - 0.1 - e0) / 3)))))
        x, y, r = CX, H * 0.12, 120 * U; frac = left / max(0.1, d - 0.1 - e0)
        glow(ctx, x, y, r * 1.6, GOLD, 0.35)
        neon_path(ctx, lambda c: c.arc(x, y, r, -math.pi / 2, -math.pi / 2 + 2 * math.pi * frac), GOLD, 12 * U)
        neon_text(ctx, str(n), x, y, 170 * U, WHITE, 1.0, GOLD, fill=0.4)

def sc_reveal(ctx, t, d):
    bg(ctx, t, GREEN)
    wy = H * 0.30
    whale(ctx, WCX, wy, 0.80, 1.0, t, scars=0.6)
    sx, sy = whale_pt(WCX, wy, 0.80, 300, 175, t)            # le requin minuscule près du ventre de la baleine (échelle ≈ réelle)
    sx += 30 * U * math.sin(t * 1.5)
    shark(ctx, sx, sy, 0.085, 1.0, t)
    k = prog(t, 0.6, 1.1)
    if k:
        neon_path(ctx, lambda c: c.arc(sx, sy, 34 * U, 0, 2 * math.pi), GOLD, 5 * U, k)
        mx, my, mr = CX, H * 0.575, 250 * U                     # loupe
        ctx.new_path(); ctx.move_to(sx, sy + 34 * U); ctx.line_to(mx + mr * 0.3, my - mr * 0.95); ctx.set_line_width(4 * U); rgba(ctx, GOLD, 0.8 * k); ctx.stroke()
        ctx.save(); ctx.new_path(); ctx.arc(mx, my, mr * ease(k), 0, 2 * math.pi); ctx.clip()
        bg(ctx, t, CYAN); shark(ctx, mx + 20 * U, my, 1.15 * ease(k), 1.0, t)
        ctx.restore()
        neon_path(ctx, lambda c: c.arc(mx, my, mr * ease(k), 0, 2 * math.pi), GOLD, 8 * U, k)
        pill(ctx, "ABOUT 20 INCHES", mx, my + mr * 0.66, GOLD, 46, prog(t, 1.2, 1.5))
    option_card(ctx, "3", "IT'S NUMBER 3!", PURPLE, H * 0.095, 1.0, good=True)
    fit_neon(ctx, "COOKIECUTTER SHARK", CX, H * 0.165, 110 * U, W * 0.84, CORAL, GOLD, prog(t, 0.2, 0.5), fill=0.35)

STEPS = [("SUCTION", CYAN), ("BITE", CORAL), ("SPIN", GOLD)]
def sc_bite(ctx, t, d):
    bg(ctx, t, CORAL, dark=0.2)
    s0, e0 = ST("bite", 0), EN("bite", 0); L = e0 - s0
    t1, t2 = s0 + 0.33 * L, s0 + 0.50 * L            # « sinks in its teeth », « then spins… »
    step = 0 if t < t1 else (1 if t < t2 else 2)
    for i, (s_, col) in enumerate(STEPS):           # 3 étapes en haut
        x = CX + (i - 1) * 330 * U
        pill(ctx, s_, x, H * 0.115, col if i <= step else (0.35, 0.35, 0.45), 48)
        if i < 2: text(ctx, "→", x + 168 * U, H * 0.115, 52 * U, WHITE, 0.8)
    text(ctx, "SIMPLIFIED DIAGRAM", CX, H * 0.165, 34 * U, (0.75, 0.80, 0.92), 0.85)
    # la peau de la baleine (vue de dessus)
    y0, y1 = H * 0.24, H * 0.64
    rrect(ctx, W * 0.04, y0, W * 0.92, y1 - y0, 60 * U)
    g = cairo.LinearGradient(0, y0, 0, y1); g.add_color_stop_rgba(0, 0.16, 0.30, 0.52, 1); g.add_color_stop_rgba(1, 0.30, 0.46, 0.66, 1); ctx.set_source(g); ctx.fill()
    for k in range(9):
        ctx.new_path(); yy = y0 + (y1 - y0) * (k + 0.5) / 9; ctx.move_to(W * 0.06, yy); ctx.curve_to(W * 0.35, yy - 12 * U, W * 0.65, yy + 12 * U, W * 0.94, yy)
        ctx.set_line_width(2 * U); rgba(ctx, WHITE, 0.08); ctx.stroke()
    text(ctx, "WHALE SKIN", W * 0.80, y1 - 40 * U, 34 * U, WHITE, 0.6)
    P = (W * 0.27, H * 0.47); sc = 1.9; S = sc * U
    done = prog(t, e0 - 1.0, e0 - 0.2)              # le morceau rond est découpé
    r_cut = 74 * U
    if t >= t2:                                      # cercle découpé progressivement pendant la rotation
        kc = prog(t, t2, e0 - 1.0)
        neon_path(ctx, lambda c: c.arc(P[0], P[1], r_cut, -math.pi / 2, -math.pi / 2 + 2 * math.pi * kc), GOLD, 8 * U)
    if done:
        circle(ctx, P[0], P[1], r_cut, (0.05, 0.07, 0.16), done); neon_path(ctx, lambda c: c.arc(P[0], P[1], r_cut, 0, 2 * math.pi), GOLD, 8 * U, done)
    if t < t1:                                       # ventouse : ondes concentriques
        for i in range(3):
            ph = ((t * 1.6 + i / 3) % 1.0)
            neon_path(ctx, lambda c, ph=ph: c.arc(P[0], P[1], (30 + 120 * ph) * U, 0, 2 * math.pi), CYAN, 5 * U, 1 - ph)
    roll = 1.0
    if t >= t2 and not done: roll = 0.25 + 0.75 * abs(math.cos((t - t2) * 5.0))    # le corps qui tourne sur lui-même
    away = ease(done) * 260 * U
    shark(ctx, P[0] + 150 * S + away, P[1] - 22 * S - away * 0.6, sc, 1.0, t, roll=roll, teeth=prog(t, t1, t1 + 0.3))
    if t >= t2 and not done:                         # flèche de rotation autour du corps
        ang = (t - t2) * 4.0
        cxr, cyr = P[0] + 150 * S, P[1] - 22 * S
        neon_path(ctx, lambda c: c.arc(cxr, cyr, 140 * U, ang, ang + 4.6), GOLD, 7 * U)
    if done:                                         # le petit morceau rond emporté
        circle(ctx, P[0] + away * 0.55, P[1] - away * 0.35, r_cut * 0.8, (0.30, 0.46, 0.66), done)
        neon_path(ctx, lambda c: c.arc(P[0] + away * 0.55, P[1] - away * 0.35, r_cut * 0.8, 0, 2 * math.pi), WHITE, 4 * U, done)

def sc_sub(ctx, t, d):
    bg(ctx, t, (0.5, 0.6, 0.9), dark=0.35)
    sx, sy = CX + 10 * U, H * 0.44; SS = 0.82
    for i in range(3):                               # ondes du sonar
        ph = ((t * 0.7 + i / 3) % 1.0); x0 = sx - 575 * SS * U
        neon_path(ctx, lambda c, ph=ph, x0=x0: c.arc(x0 + 40 * U, sy, (60 + 260 * ph) * U, 0, 2 * math.pi), CYAN, 5 * U, 0.6 * (1 - ph))
    submarine(ctx, sx, sy, SS, 1.0, t, bites=1.0)
    fit_neon(ctx, "U.S. NAVY SUBMARINES", CX, H * 0.12, 112 * U, W * 0.90, WHITE, CYAN, prog(t, 0.0, 0.3))
    pill(ctx, "1970s", CX, H * 0.185, GOLD, 52, prog(t, 0.3, 0.6))
    dx, dy = sx - 520 * SS * U, sy + 95 * SS * U
    k = prog(t, 1.4, 1.8)
    if k:
        ctx.new_path(); ctx.move_to(dx, dy); ctx.line_to(dx + 40 * U, H * 0.58); ctx.set_line_width(4 * U); rgba(ctx, GOLD, k); ctx.stroke()
        pill(ctx, "RUBBER SONAR DOME", CX, H * 0.60, CORAL, 50, k)

def sc_outro(ctx, t, d):
    bg(ctx, t, GREEN, dark=0.75)
    c0 = 1.6                                         # le CTA démarre ici
    sh_a = 1.0 if t < c0 else 0.35
    shark(ctx, CX + 20 * U + 20 * U * math.sin(t), H * 0.42, 2.3, sh_a, t, glow_k=prog(t, 0.0, 0.8))
    if t < c0 + 0.2:
        fit_neon(ctx, "GLOWS IN THE DARK", CX, H * 0.14, 110 * U, W * 0.86, GREEN, CYAN, 1 - prog(t, c0, c0 + 0.2), fill=0.4)
    if t >= c0: cta(ctx, t - c0, d - c0, "DID YOU GET IT RIGHT?", "SEND THIS TO AN OCEAN LOVER")

SHORT_SCENES = ["hook", "ask", "reveal", "bite", "sub", "outro"]
SCENES = dict(hook=sc_hook, ask=sc_ask, reveal=sc_reveal, bite=sc_bite, sub=sc_sub, outro=sc_outro)

def poster_text(ctx, s, x, y, size, col, maxw=None):
    font(ctx, size); w = ctx.text_extents(s).width
    if maxw and w > maxw: size *= maxw / w; font(ctx, size)
    e = ctx.text_extents(s); x0 = x - e.width / 2 - e.x_bearing; y0 = y + size * 0.35
    ctx.save(); ctx.translate(10 * U, 14 * U); ctx.move_to(x0, y0); ctx.text_path(s); rgba(ctx, (0, 0, 0), 0.75)
    ctx.set_line_width(size * 0.20); ctx.set_line_join(cairo.LINE_JOIN_ROUND); ctx.stroke_preserve(); ctx.fill(); ctx.restore()
    ctx.move_to(x0, y0); ctx.text_path(s); rgba(ctx, (0.01, 0.01, 0.02), 1); ctx.set_line_width(size * 0.16)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND); ctx.stroke_preserve(); rgba(ctx, col, 1); ctx.fill()

def cover(ctx):
    """Affiche : la baleine en grand avec ses cercles lumineux, la question, sans la réponse (pas de requin) ;
    titre et bandeau entre 14 % et 86 % de la hauteur (grilles de profil)."""
    bg(ctx, 0.5, CYAN)
    whale(ctx, WCX, H * 0.52, 0.95, 1.0, 0.3, scars=1.0, pulse=False)
    poster_text(ctx, "WHAT MADE", CX, H * 0.21, 160 * U, WHITE, W * 0.86)
    poster_text(ctx, "THESE CIRCLES?", CX, H * 0.285, 150 * U, GOLD, W * 0.88)
    rrect(ctx, CX - 470 * U, H * 0.79 - 60 * U, 940 * U, 120 * U, 60 * U); rgba(ctx, GOLD, 1); ctx.fill()
    rrect(ctx, CX - 470 * U, H * 0.79 - 60 * U, 940 * U, 120 * U, 60 * U); ctx.set_line_width(7 * U); rgba(ctx, (0.01, 0.01, 0.02), 1); ctx.stroke()
    text(ctx, "CAN YOU GUESS?", CX, H * 0.79, 70 * U, (0.02, 0.03, 0.06))
