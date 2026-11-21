exec(open("engine/photo.py", encoding="utf-8").read())   # poster_text, red_arrow, scrim (aucune image n'est chargée)
# Episode 042 (Short seul, 9:16, ~29 s) - "Zebra Stripes: Why Do Zebras Have Stripes? | Animal Mystery #3"
# Choix de Nazik (2026-11-21) : « quelque chose de réaliste avec une musique un peu safari et mystérieuse » → dessin
# RÉALISTE fait maison (pas d'images IA : test de la grenouille, ép. 041, 263 vues en 9 h contre 6 pour le poisson IA).
# Deux changements seulement par rapport à l'ép. 041 : la question ET les 3 réponses à l'écran dès l'image 1 (comme le
# pantalon, 61 % « ont continué de regarder ») ; ~29 s au lieu de 37.
# Faits : Caro et al. (2019), PLOS ONE 14(2): e0210831 — les taons approchent autant les zèbres que les chevaux mais se
# posent beaucoup moins sur eux (ils ne ralentissent pas assez pour se poser) ; des chevaux en manteau rayé reçoivent
# beaucoup moins d'atterrissages que les mêmes en manteau noir ou blanc (sur la partie couverte ; tête et cou inchangés) ;
# Caro et al. (2014), Nature Communications : la répartition des rayures suit celle des mouches piqueuses ; la peau du
# zèbre est noire sous le pelage. Formulation prudente : « Studies point to biting flies ».
# Dessin : zèbre de profil en repère local (unités ≈ px) ; les rayures sont les lignes de niveau d'un champ continu
# (verticales sur le corps, en arcs autour de la cuisse, perpendiculaires au cou et à la tête, horizontales sur les
# pattes) : elles s'enchaînent sans jamais se croiser, comme un vrai pelage.
import json as _json
from PIL import ImageFilter as _IF
_TL = {sg["scene"]: sg for sg in _json.load(open(EP + "/build/timeline.json", encoding="utf-8"))}
def ST(scene, k):
    sg = _TL.get(scene)
    return sg["sents"][k]["start"] - sg["start"] if sg and k < len(sg["sents"]) else 1e9
def EN(scene, k):
    sg = _TL.get(scene)
    return sg["sents"][k]["end"] - sg["start"] if sg and k < len(sg["sents"]) else 1e9

DARK = (0.03, 0.02, 0.08)
SERIES = "ANIMAL MYSTERY #3"
FUR = (0.97, 0.95, 0.89)
INK = (0.055, 0.045, 0.05)
SUNC = (1.0, 0.80, 0.42)

# ---------------------------------------------------------------- interface (comme les ép. 040–041)
def pill(ctx, s, x, y, col, size=46, a=1.0):
    if a <= 0: return
    font(ctx, size * U); w_ = ctx.text_extents(s).width + 60 * U
    rrect(ctx, x - w_ / 2, y - size * 0.8 * U, w_, size * 1.6 * U, size * 0.8 * U); rgba(ctx, col, 0.96 * a); ctx.fill()
    text(ctx, s, x, y, size * U, DARK, a)

def note(ctx, s, y, a=1.0):
    if a <= 0: return
    font(ctx, 34 * U); w_ = ctx.text_extents(s).width + 40 * U
    rrect(ctx, CX - w_ / 2, y - 28 * U, w_, 56 * U, 28 * U); rgba(ctx, (0.0, 0.0, 0.0), 0.55 * a); ctx.fill()
    text(ctx, s, CX, y, 34 * U, (0.90, 0.92, 1.0), 0.9 * a)

OPTS = [("1", "HIDE FROM LIONS", CORAL), ("2", "CONFUSE BITING FLIES", CYAN), ("3", "STAY COOL", PURPLE)]
def option_card(ctx, n, s_, col, y, k=1.0, good=False, hi=0.0, w=0.80):
    if k <= 0: return
    pw, ph = W * w, 104 * U; x = CX + (1 - ease(k)) * W * 0.5
    if good: col = GREEN
    if good or hi > 0: glow(ctx, x, y, pw * 0.6, col, 0.45 * max(hi, 1.0 if good else 0))
    sc_ = 1 + 0.05 * hi
    ctx.save(); ctx.translate(x, y); ctx.scale(sc_, sc_)
    rrect(ctx, -pw / 2, -ph / 2, pw, ph, ph / 2); rgba(ctx, (0.04, 0.03, 0.08), 0.90 * k); ctx.fill()
    rrect(ctx, -pw / 2, -ph / 2, pw, ph, ph / 2); ctx.set_line_width((7 + 4 * hi) * U); rgba(ctx, col, k); ctx.stroke()
    circle(ctx, -pw / 2 + ph / 2, 0, ph * 0.38, col, k); text(ctx, n, -pw / 2 + ph / 2, 0, 58 * U, DARK, k)
    font(ctx, 52 * U); tw = ctx.text_extents(s_).width; sz = 52 * U * min(1.0, (pw - ph * 1.5) / tw)
    text(ctx, s_, ph * 0.40, 0, sz, WHITE, k)
    ctx.restore()

# ---------------------------------------------------------------- géométrie du zèbre (profil, tête à gauche)
def smooth_closed(c, pts):
    n = len(pts); c.move_to(*pts[0])
    for i in range(n):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
        c.curve_to(p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6, p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6, p2[0], p2[1])
    c.close_path()

def smooth_open(c, pts):
    q = [pts[0]] + list(pts) + [pts[-1]]; c.move_to(*pts[0])
    for i in range(1, len(q) - 2):
        p0, p1, p2, p3 = q[i - 1], q[i], q[i + 1], q[i + 2]
        c.curve_to(p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6, p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6, p2[0], p2[1])

TORSO = [(-175, -150), (-60, -141), (60, -137), (180, -149), (262, -136), (312, -90), (324, -22), (302, 48), (252, 94),
         (176, 112), (40, 124), (-90, 116), (-182, 92), (-246, 40), (-264, -40), (-236, -112)]
NECK = [(-340, -318), (-292, -302), (-238, -252), (-188, -198), (-142, -152), (-175, -95), (-232, -38), (-262, -18),
        (-284, -70), (-320, -150), (-352, -206), (-372, -246)]
HEAD = [(-350, -335), (-385, -305), (-420, -266), (-455, -226), (-485, -192), (-500, -166), (-492, -146), (-464, -140),
        (-430, -156), (-395, -182), (-352, -212), (-322, -248), (-320, -298), (-334, -328)]
CREST = [(-340, -318), (-292, -302), (-238, -252), (-188, -198), (-142, -152)]
NFL = [(-244, 30), (-238, 110), (-232, 185), (-236, 210), (-228, 250), (-226, 300), (-230, 316), (-188, 316), (-192, 300),
       (-196, 250), (-192, 212), (-186, 175), (-168, 110), (-150, 50)]
NHL = [(170, 70), (196, 150), (212, 205), (220, 250), (224, 300), (220, 316), (266, 316), (264, 300), (262, 250), (272, 212),
       (292, 170), (306, 100), (304, 30)]
FFL = [(x + 58, y - 3) for x, y in NFL]
FHL = [(x - 52, y - 4) for x, y in NHL]
def hoof(c, x0, x1, y0=312, y1=334):
    c.new_path(); c.move_to(x0, y0); c.line_to(x1, y0); c.line_to(x1 + 4, y1); c.line_to(x0 - 4, y1); c.close_path()
HOOVES_NEAR = [(-232, -186), (218, 268)]
HOOVES_FAR = [(-232 + 58, -186 + 58), (218 - 52, 268 - 52)]

def mane_pts():
    out, n = [], len(CREST)
    for i, (x, y) in enumerate(CREST):
        a, b = CREST[max(0, i - 1)], CREST[min(n - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]; L = math.hypot(dx, dy); nx, ny = dy / L, -dx / L   # normale vers le haut
        h = 36 - 14 * i / (n - 1)
        out.append((x + nx * h, y + ny * h))
    return CREST + out[::-1]
MANE = mane_pts()

def path_poly(c, pts): c.new_path(); smooth_closed(c, pts)

# ---------------------------------------------------------------- pelage rayé (calculé une fois)
_ZR = 2.0
ZX0, ZY0, ZX1, ZY1 = -540, -450, 380, 360
ZW, ZH = int((ZX1 - ZX0) * _ZR), int((ZY1 - ZY0) * _ZR)

def _mask(draw, blur=0):
    s = cairo.ImageSurface(cairo.FORMAT_A8, ZW, ZH); c = cairo.Context(s)
    c.scale(_ZR, _ZR); c.translate(-ZX0, -ZY0); rgba(c, WHITE, 1); draw(c); s.flush()
    a = np.frombuffer(s.get_data(), np.uint8).reshape(ZH, s.get_stride())[:, :ZW].copy()
    if blur: a = np.asarray(_Img.fromarray(a).filter(_IF.GaussianBlur(blur * _ZR)))
    return a.astype(np.float32) / 255.0

def _fill(pts):
    def d(c): path_poly(c, pts); c.fill()
    return d

def _build_stripes():
    X, Y = np.meshgrid(ZX0 + (np.arange(ZW) + 0.5) / _ZR, ZY0 + (np.arange(ZH) + 0.5) / _ZR)
    B = 20
    mt = _mask(_fill(TORSO), B)
    mn = np.maximum(_mask(_fill(NECK), B), _mask(_fill(MANE), B))
    mh = _mask(_fill(HEAD), B)
    cut = np.clip((Y - 40) / 60, 0, 1)                           # les pattes ne « mordent » pas sur le ventre
    mlf = np.maximum(_mask(_fill(NFL), B), _mask(_fill(FFL), B)) * cut
    mlh = np.maximum(_mask(_fill(NHL), B), _mask(_fill(FHL), B)) * cut
    eps = 1e-4; ws = mt + mn + mh + mlf + mlh + eps
    # champs de phase (en nombre de rayures)
    wh = np.clip((X - 40) / 160, 0, 1); wh = wh * wh * (3 - 2 * wh)
    phi_t = (X + 0.16 * Y) / 46.0
    phi_h = np.hypot(X - 150, Y - 175) / 43.0
    ax, ay, dx, dy = -355.0, -280.0, 145.0, 220.0; L = math.hypot(dx, dy)
    phi_n = ((X - ax) * dx + (Y - ay) * dy) / L / 38.0
    hx, hy, ex, ey = -345.0, -330.0, -150.0, 170.0; L2 = math.hypot(ex, ey)
    phi_hd = ((X - hx) * ex + (Y - hy) * ey) / L2 / 19.0
    # raccords : chaque zone prend la phase de sa voisine au point de jonction (cou/épaule, tête/cou, pattes/corps)
    def at(f, x, y):
        i = int(np.clip((y - ZY0) * _ZR, 0, ZH - 1)); j = int(np.clip((x - ZX0) * _ZR, 0, ZW - 1)); return float(f[i, j])
    phi_n = phi_n + at(phi_t, -215, -95) - at(phi_n, -215, -95)
    phi_hd = phi_hd + at(phi_n, -345, -255) - at(phi_hd, -345, -255)
    phi_lf = Y / 23.0; phi_lf = phi_lf + at(phi_t, -200, 90) - at(phi_lf, -200, 90)
    phi_lh = Y / 23.0; phi_lh = phi_lh + at(phi_h, 240, 90) - at(phi_lh, 240, 90)
    phi = (mt * ((1 - wh) * phi_t + wh * phi_h) + mn * phi_n + mh * phi_hd + mlf * phi_lf + mlh * phi_lh) / ws
    noise = (0.16 * np.sin(X / 41 + 0.3) * np.sin(Y / 57 + 1.1) + 0.11 * np.sin((X - 1.7 * Y) / 33 + 2.0)
             + 0.07 * np.sin((2.3 * X + Y) / 19 + 0.5))
    s = np.sin(2 * np.pi * (phi + noise))
    dark = np.clip((s + 0.02) / 0.22, 0, 1)
    # raie dorsale, museau noir, dessous du museau
    def dorsal(c):
        c.new_path(); smooth_open(c, [(-170, -146), (-60, -137), (60, -133), (180, -145), (262, -132), (312, -100)])
        c.set_line_width(13); c.set_line_cap(cairo.LINE_CAP_ROUND); c.stroke()
    def muzzle(c):
        c.save(); c.translate(-474, -170); c.rotate(-0.86); c.scale(44, 30); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.fill()
    dark = np.maximum(dark, _mask(dorsal, 2))
    dark = np.maximum(dark, _mask(muzzle, 5) * 0.96)
    a = (dark * 255).astype(np.uint8)
    buf = np.empty((ZH, ZW, 4), np.uint8)
    for i, v in enumerate((INK[2], INK[1], INK[0])): buf[..., i] = (a.astype(np.float32) * v).astype(np.uint8)
    buf[..., 3] = a
    surf = cairo.ImageSurface.create_for_data(memoryview(buf), cairo.FORMAT_ARGB32, ZW, ZH, ZW * 4)
    return surf, buf
_STRIPES = _build_stripes()

def paint_stripes(ctx, a=1.0):
    ctx.save(); ctx.translate(ZX0, ZY0); ctx.scale(1 / _ZR, 1 / _ZR)
    ctx.set_source_surface(_STRIPES[0], 0, 0); ctx.get_source().set_filter(cairo.FILTER_GOOD)
    ctx.set_operator(cairo.OPERATOR_ATOP); ctx.paint_with_alpha(a); ctx.restore()

def shade(ctx, sun=1.0, base=(0, 0, 0)):
    """Volume et lumière du soleil couchant, posés seulement sur le pelage (opérateur ATOP)."""
    ctx.save(); ctx.set_operator(cairo.OPERATOR_ATOP)
    g = cairo.LinearGradient(0, -80, 0, 340); g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0.05, 0.02, 0.05, 0.50)
    ctx.set_source(g); ctx.paint()
    g = cairo.LinearGradient(-520, 0, 60, 0); g.add_color_stop_rgba(0, 0.25, 0.18, 0.45, 0.30); g.add_color_stop_rgba(1, 0.25, 0.18, 0.45, 0)
    ctx.set_source(g); ctx.paint()
    g = cairo.RadialGradient(460, -300, 40, 460, -300, 620); g.add_color_stop_rgba(0, 1.0, 0.62, 0.25, 0.55 * sun); g.add_color_stop_rgba(1, 1.0, 0.62, 0.25, 0)
    ctx.set_source(g); ctx.paint()
    g = cairo.RadialGradient(20, -70, 20, 20, -70, 280); g.add_color_stop_rgba(0, 1, 0.97, 0.9, 0.16); g.add_color_stop_rgba(1, 1, 1, 1, 0)
    ctx.set_source(g); ctx.paint()
    ctx.restore()

def ears(ctx, t, col=FUR, dark=INK, flick=0.0):
    specs = [((-353, -331), (-357, -406), 14, 0.72, 0.0), ((-329, -327), (-317, -413), 16, 1.0, flick)]
    for (bx, by), (tx, ty), w, k, rot in specs:
        ctx.save(); ctx.translate(bx, by); ctx.rotate(rot); tx_, ty_ = tx - bx, ty - by
        def leaf(c):
            c.new_path(); c.move_to(-w, 2); c.curve_to(-w * 1.3, ty_ * 0.45, tx_ - 6, ty_ * 0.85, tx_, ty_)
            c.curve_to(tx_ + 8, ty_ * 0.8, w * 1.2, ty_ * 0.4, w, 2); c.close_path()
        leaf(ctx); rgba(ctx, mix(INK, col, k), 1); ctx.fill()
        ctx.save(); leaf(ctx); ctx.clip()
        ctx.new_path(); ctx.arc(tx_, ty_, 26, 0, 2 * math.pi); rgba(ctx, dark, 1); ctx.fill()                 # pointe noire
        ctx.new_path(); ctx.move_to(-w * 0.3, -4); ctx.curve_to(-w * 0.4, ty_ * 0.4, tx_ * 0.5, ty_ * 0.7, tx_ * 0.8, ty_ * 0.8)
        ctx.set_line_width(w * 0.8); rgba(ctx, (0.35, 0.30, 0.32), 0.55); ctx.stroke()                        # creux de l'oreille
        ctx.restore(); ctx.restore()

def tail(ctx, t, swish=1.0, hair=FUR, tuft=INK, striped=True):
    ang = 0.07 * swish * math.sin(t * 1.9)
    ctx.save(); ctx.translate(316, -104); ctx.rotate(ang)
    pts = [(0, 0), (30, 44), (36, 130), (24, 208)]
    ctx.push_group()
    ctx.new_path(); smooth_open(ctx, pts); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_line_width(20); rgba(ctx, hair, 1); ctx.stroke()
    if striped:   # anneaux sombres, découpés dans la queue elle-même
        ctx.set_operator(cairo.OPERATOR_ATOP); rgba(ctx, tuft, 0.92)
        for k in range(6):
            ctx.rectangle(-40, 18 + 26 * k, 120, 11); ctx.fill()
    ctx.pop_group_to_source(); ctx.paint()
    ctx.new_path(); ctx.move_to(14, 170); ctx.curve_to(40, 200, 34, 250, 18 + 6 * math.sin(t * 2.3), 290)
    ctx.curve_to(4, 250, 0, 205, 14, 170); ctx.close_path(); rgba(ctx, tuft, 1); ctx.fill()
    ctx.restore()

def eye(ctx, blink=0.0):
    ctx.save(); ctx.translate(-371, -279); ctx.rotate(-0.72)
    glow(ctx, 0, 0, 34, INK, 0.45)
    ctx.save(); ctx.scale(25, max(1.5, 15 * (1 - blink))); ctx.arc(0, 0, 1, 0, 2 * math.pi); ctx.restore()
    rgba(ctx, (0.03, 0.02, 0.02), 1); ctx.fill_preserve(); ctx.set_line_width(3); rgba(ctx, (0.55, 0.45, 0.40), 0.8); ctx.stroke()
    if blink < 0.6: circle(ctx, -8, -5, 5, WHITE, 0.95)
    ctx.restore()

def zebra_body(ctx, t, fur=FUR, stripes=True, sun=1.0, coat=0.0, hair=None, mane_col=None):
    """Corps complet (hors pattes lointaines) dans un groupe : remplissage, rayures, ombrage."""
    ctx.push_group()
    g = cairo.LinearGradient(0, -340, 0, 330); g.add_color_stop_rgb(0, *fur); g.add_color_stop_rgb(1, *mix(fur, (0.7, 0.66, 0.6), 0.35))
    for pts in (TORSO, NECK, MANE, HEAD, NFL, NHL):
        path_poly(ctx, pts); ctx.set_source(g); ctx.fill()
    if mane_col is not None:
        path_poly(ctx, MANE); rgba(ctx, mane_col, 1); ctx.fill()
    if stripes: paint_stripes(ctx)
    else:   # cheval : museau et bas des pattes plus sombres
        ctx.save(); ctx.set_operator(cairo.OPERATOR_ATOP)
        ctx.new_path(); ctx.save(); ctx.translate(-476, -168); ctx.rotate(-0.86); ctx.scale(42, 28); ctx.arc(0, 0, 1, 0, 2 * math.pi); ctx.restore()
        rgba(ctx, (0.12, 0.08, 0.06), 0.9); ctx.fill(); ctx.restore()
    shade(ctx, sun)
    ctx.pop_group_to_source(); ctx.paint()
    # crinière : franges sombres en brosse
    ctx.new_path(); smooth_open(ctx, MANE[len(CREST):]); ctx.set_line_width(7); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    rgba(ctx, mane_col or INK, 0.55); ctx.stroke()
    for (x0, x1) in HOOVES_NEAR:
        hoof(ctx, x0, x1); rgba(ctx, (0.08, 0.06, 0.06), 1); ctx.fill()
    eye(ctx, blink=1.0 if (t % 3.7) < 0.12 else 0.0)
    ctx.new_path(); ctx.save(); ctx.translate(-489, -176); ctx.rotate(-0.86); ctx.scale(9, 5); ctx.arc(0, 0, 1, 0, 2 * math.pi); ctx.restore()
    rgba(ctx, (0, 0, 0), 0.9); ctx.fill()                                                                         # naseau
    # liseré de lumière du soleil sur le dos et la croupe
    ctx.new_path(); smooth_open(ctx, [(-150, -152), (-40, -143), (80, -139), (180, -151), (262, -138), (312, -92), (324, -24)])
    ctx.set_line_width(4); ctx.set_line_cap(cairo.LINE_CAP_ROUND); rgba(ctx, SUNC, 0.55 * sun); ctx.stroke()

def far_legs(ctx, fur=FUR, stripes=True):
    ctx.push_group()
    for pts in (FFL, FHL):
        path_poly(ctx, pts); rgba(ctx, fur, 1); ctx.fill()
    if stripes: paint_stripes(ctx)
    ctx.set_operator(cairo.OPERATOR_ATOP); rgba(ctx, (0.08, 0.05, 0.10), 0.42); ctx.paint()
    ctx.pop_group_to_source(); ctx.paint()
    for (x0, x1) in HOOVES_FAR:
        hoof(ctx, x0, x1, 309, 330); rgba(ctx, (0.05, 0.04, 0.04), 1); ctx.fill()

def zebra(ctx, x, y, s, t, a=1.0, sun=1.0, flick=True):
    """Zèbre réaliste de profil ; (x, y) = position du sol sous le centre du corps ; s = échelle."""
    if a <= 0: return
    S = s * U
    ctx.save(); ctx.translate(x, y); ctx.scale(S, S); ctx.translate(0, -334)
    ctx.push_group()
    ctx.save(); ctx.translate(20, 334); ctx.scale(1, 0.12); glow(ctx, 0, 0, 420, (0.02, 0.01, 0.02), 0.65); ctx.restore()   # ombre au sol
    far_legs(ctx)
    tail(ctx, t)
    br = 1 + 0.006 * math.sin(t * 2.2)
    ctx.save(); ctx.translate(0, 120); ctx.scale(1, br); ctx.translate(0, -120)
    zebra_body(ctx, t, sun=sun)
    fl = 0.18 * max(0.0, math.sin(t * 4.0)) ** 8 if flick else 0.0
    ears(ctx, t, flick=fl)
    ctx.restore()
    ctx.pop_group_to_source(); ctx.paint_with_alpha(a)
    ctx.restore()

def zxy(lx, ly, x, y, s):
    """Point du repère du zèbre → écran (même transformation que zebra())."""
    S = s * U
    return x + lx * S, y + (ly - 334) * S

# ---------------------------------------------------------------- cheval de l'expérience (même silhouette, robe baie)
BAY = (0.50, 0.30, 0.16)
def horse(ctx, x, y, s, t, coat=0.0, a=1.0):
    S = s * U
    ctx.save(); ctx.translate(x, y); ctx.scale(S, S); ctx.translate(0, -334)
    ctx.save(); ctx.translate(20, 334); ctx.scale(1, 0.12); glow(ctx, 0, 0, 420, (0.02, 0.01, 0.02), 0.6); ctx.restore()
    ctx.push_group()
    for pts in (FFL, FHL): path_poly(ctx, pts); rgba(ctx, mix(BAY, INK, 0.35), 1); ctx.fill()
    ctx.pop_group_to_source(); ctx.paint()
    for (x0, x1) in HOOVES_FAR: hoof(ctx, x0, x1, 309, 330); rgba(ctx, (0.05, 0.04, 0.04), 1); ctx.fill()
    tail(ctx, t, hair=(0.16, 0.09, 0.06), tuft=(0.12, 0.07, 0.05), striped=False)
    zebra_body(ctx, t, fur=BAY, stripes=False, sun=1.0, mane_col=(0.14, 0.08, 0.05))
    ears(ctx, t, col=BAY, dark=(0.14, 0.08, 0.05), flick=0.0)
    if coat > 0:   # manteau rayé (comme dans l'expérience) qui descend sur le dos
        dy = -260 * (1 - ease(coat))
        ctx.save(); ctx.translate(0, dy)
        COAT = [(-205, -160), (-60, -151), (60, -147), (180, -159), (262, -146), (306, -100), (300, 20), (240, 70), (120, 88),
                (0, 96), (-120, 92), (-205, 70), (-238, 0), (-240, -90)]
        ctx.push_group()
        path_poly(ctx, COAT); rgba(ctx, (0.97, 0.96, 0.93), 1); ctx.fill()
        ctx.set_operator(cairo.OPERATOR_ATOP)
        for k in range(-8, 14):
            xx = -260 + 44 * k
            ctx.new_path(); ctx.move_to(xx, -200); ctx.line_to(xx - 26, 140); ctx.set_line_width(20); rgba(ctx, INK, 1); ctx.stroke()
        g = cairo.LinearGradient(0, -160, 0, 100); g.add_color_stop_rgba(0, 1, 0.7, 0.35, 0.18); g.add_color_stop_rgba(1, 0.05, 0.03, 0.05, 0.35)
        ctx.set_source(g); ctx.paint()
        ctx.pop_group_to_source(); ctx.paint_with_alpha(ease(min(1.0, coat * 3)))
        path_poly(ctx, COAT); ctx.set_line_width(7); rgba(ctx, (0.25, 0.20, 0.30), 0.9 * min(1.0, coat * 3)); ctx.stroke()
        ctx.restore()
    ctx.restore()

# ---------------------------------------------------------------- taons
def fly(ctx, x, y, r, ang, t, a=1.0, landed=False):
    if a <= 0: return
    ctx.save(); ctx.translate(x, y); ctx.rotate(ang)
    flap = 0.35 + 0.65 * abs(math.sin(t * 60)) if not landed else 0.25
    for sg in (1, -1):   # ailes translucides
        ctx.save(); ctx.translate(-r * 0.2, sg * r * 0.25); ctx.rotate(sg * (0.5 + 0.5 * flap)); ctx.scale(r * 1.15, r * 0.42 * (0.6 + 0.4 * flap))
        ctx.arc(0.6, 0, 1, 0, 2 * math.pi); ctx.restore(); rgba(ctx, (0.85, 0.92, 1.0), 0.40 * a); ctx.fill_preserve()
        ctx.set_line_width(1.2 * U); rgba(ctx, (0.9, 0.95, 1.0), 0.6 * a); ctx.stroke()
    ctx.save(); ctx.scale(r * 0.95, r * 0.42); ctx.arc(-0.5, 0, 1, 0, 2 * math.pi); ctx.restore()
    rgba(ctx, (0.24, 0.20, 0.18), a); ctx.fill()                                     # abdomen
    for k in range(3):
        ctx.new_path(); ctx.move_to(-r * (0.3 + 0.4 * k), -r * 0.38); ctx.line_to(-r * (0.3 + 0.4 * k), r * 0.38)
        ctx.set_line_width(r * 0.10); rgba(ctx, (0.55, 0.48, 0.38), 0.7 * a); ctx.stroke()
    circle(ctx, r * 0.35, 0, r * 0.38, (0.16, 0.14, 0.13), a)                      # thorax
    for sg in (1, -1): circle(ctx, r * 0.78, sg * r * 0.2, r * 0.3, (0.25, 0.75, 0.45), a)   # gros yeux irisés
    ctx.restore()

def fly_track(t, i, S0, T0, E0, P=2.1, off=0.0):
    """Taon qui fonce vers T sans ralentir, rebondit (« bonk ») et repart vers E. Renvoie x, y, angle, alpha, choc."""
    u = ((t + off) % P) / P
    if u < 0.55:
        k = (u / 0.55) ** 1.6; x = S0[0] + (T0[0] - S0[0]) * k; y = S0[1] + (T0[1] - S0[1]) * k + 18 * U * math.sin(u * 40 + i)
        ang = math.atan2(T0[1] - S0[1], T0[0] - S0[0]); hit = 0.0
    else:
        k = ease((u - 0.55) / 0.45); x = T0[0] + (E0[0] - T0[0]) * k; y = T0[1] + (E0[1] - T0[1]) * k + 26 * U * math.sin(k * 7 + i)
        ang = math.atan2(E0[1] - T0[1], E0[0] - T0[0]) + 0.6 * math.sin(u * 30); hit = max(0.0, 1 - (u - 0.55) / 0.12)
    a = min(1.0, u / 0.08, (1 - u) / 0.1)
    return x, y, ang, a, hit

def bonk(ctx, x, y, k):
    if k <= 0: return
    for j in range(6):
        an = j * math.pi / 3 + 0.3; r0, r1 = 20 * U, (20 + 34 * k) * U
        ctx.new_path(); ctx.move_to(x + math.cos(an) * r0, y + math.sin(an) * r0); ctx.line_to(x + math.cos(an) * r1, y + math.sin(an) * r1)
        ctx.set_line_width(5 * U); ctx.set_line_cap(cairo.LINE_CAP_ROUND); rgba(ctx, WHITE, 0.85 * k); ctx.stroke()

# ---------------------------------------------------------------- savane au crépuscule
GROUND_Y = 0.705
def acacia(ctx, x, y, s, col, a=1.0):
    S = s * U
    ctx.save(); ctx.translate(x, y); ctx.scale(S, S)
    rgba(ctx, col, a)
    ctx.new_path(); ctx.move_to(-8, 0); ctx.curve_to(-6, -60, -20, -110, -60, -150); ctx.line_to(-48, -156); ctx.curve_to(-14, -120, 0, -90, 4, -70)
    ctx.curve_to(10, -110, 40, -140, 80, -160); ctx.line_to(86, -150); ctx.curve_to(40, -120, 14, -70, 10, 0); ctx.close_path(); ctx.fill()
    for (cx_, cy_, rx, ry) in ((-70, -168, 120, 26), (40, -182, 150, 30), (120, -164, 80, 20), (-10, -196, 110, 22)):
        ctx.save(); ctx.translate(cx_, cy_); ctx.scale(rx, ry); ctx.arc(0, 0, 1, 0, 2 * math.pi); ctx.restore(); ctx.fill()
    ctx.restore()

def savanna(ctx, t, dim=0.0, sun_x=0.80, sun_y=0.50):
    gy = H * GROUND_Y; hz = H * 0.585
    g = cairo.LinearGradient(0, 0, 0, hz)
    for st_, c in ((0, (0.07, 0.05, 0.16)), (0.45, (0.30, 0.12, 0.32)), (0.78, (0.85, 0.36, 0.24)), (1, (1.0, 0.68, 0.32))):
        g.add_color_stop_rgb(st_, *c)
    ctx.set_source(g); ctx.rectangle(0, 0, W, hz + 2); ctx.fill()
    rnd = random.Random(5)
    for i in range(40):   # premières étoiles
        sx, sy = rnd.random() * W, rnd.random() * H * 0.30
        circle(ctx, sx, sy, rnd.uniform(1.5, 3.5) * U, WHITE, (0.25 + 0.25 * math.sin(t * 1.5 + i)) * (1 - sy / (H * 0.3)))
    sx, sy = W * sun_x, H * sun_y
    glow(ctx, sx, sy, 900 * U, (1.0, 0.55, 0.25), 0.40); glow(ctx, sx, sy, 380 * U, SUNC, 0.55)
    circle(ctx, sx, sy, 150 * U, (1.0, 0.86, 0.55), 1.0)
    # collines lointaines et acacias
    ctx.new_path(); ctx.move_to(0, hz)
    for i in range(0, 41):
        xx = W * i / 40; ctx.line_to(xx, hz - (30 + 22 * math.sin(i * 0.7) + 14 * math.sin(i * 1.9 + 1)) * U)
    ctx.line_to(W, hz + 4); ctx.line_to(0, hz + 4); ctx.close_path(); rgba(ctx, (0.28, 0.13, 0.22), 1); ctx.fill()
    for (ax_, s_, c_) in ((0.12, 1.25, (0.13, 0.06, 0.12)), (0.42, 0.55, (0.24, 0.11, 0.20)), (0.93, 0.95, (0.15, 0.07, 0.13)), (0.66, 0.42, (0.26, 0.12, 0.21))):
        acacia(ctx, W * ax_, hz + 6 * U, s_, c_)
    g = cairo.LinearGradient(0, hz, 0, H)
    for st_, c in ((0, (0.62, 0.38, 0.17)), (0.35, (0.42, 0.24, 0.11)), (1, (0.12, 0.07, 0.05))): g.add_color_stop_rgb(st_, *c)
    ctx.set_source(g); ctx.rectangle(0, hz, W, H - hz); ctx.fill()
    glow(ctx, sx, hz + 30 * U, 700 * U, (1.0, 0.62, 0.3), 0.30)       # reflet du soleil sur la plaine
    # herbes du plan moyen
    rnd = random.Random(9)
    for i in range(140):
        bx = rnd.random() * W; by = hz + (rnd.random() ** 1.5) * (gy - hz + 30 * U); h = (16 + 30 * (by - hz) / (gy - hz + 1)) * U
        sw = 6 * U * math.sin(t * 1.6 + bx * 0.01)
        ctx.new_path(); ctx.move_to(bx, by); ctx.curve_to(bx, by - h * 0.5, bx + sw, by - h * 0.8, bx + sw * 1.4, by - h)
        ctx.set_line_width(2.2 * U); rgba(ctx, mix((0.95, 0.70, 0.35), (0.35, 0.20, 0.10), rnd.random() * 0.6), 0.8); ctx.stroke()
    if dim: rgba(ctx, (0.02, 0.01, 0.04), dim); ctx.paint()

def foreground_grass(ctx, t):
    rnd = random.Random(21); gy = H * GROUND_Y
    for i in range(170):
        bx = rnd.random() * W; by = gy + rnd.random() * (H - gy) * 0.95; h = (60 + 140 * rnd.random()) * U * (0.6 + 0.6 * (by - gy) / (H - gy))
        sw = (14 + 10 * rnd.random()) * U * math.sin(t * 1.3 + bx * 0.006 + i)
        ctx.new_path(); ctx.move_to(bx - 5 * U, by); ctx.curve_to(bx, by - h * 0.5, bx + sw * 0.6, by - h * 0.8, bx + sw, by - h)
        ctx.curve_to(bx + sw * 0.5, by - h * 0.75, bx + 4 * U, by - h * 0.4, bx + 5 * U, by); ctx.close_path()
        rgba(ctx, mix((0.85, 0.58, 0.25), (0.22, 0.12, 0.06), 0.35 + 0.5 * rnd.random()), 0.95); ctx.fill()
    rnd = random.Random(33)
    for i in range(24):   # poussière dorée dans la lumière
        px = (rnd.random() * W + t * rnd.uniform(8, 25) * U) % W; py = H * (0.35 + 0.4 * rnd.random()) + 20 * U * math.sin(t + i)
        circle(ctx, px, py, rnd.uniform(2, 5) * U, SUNC, 0.35 + 0.25 * math.sin(t * 2 + i))

def vignette(ctx):
    g = cairo.RadialGradient(CX, H * 0.48, H * 0.30, CX, H * 0.48, H * 0.75)
    g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0.02, 0.0, 0.04, 0.55)
    ctx.set_source(g); ctx.paint()

ZS = 1.12                        # échelle du zèbre dans le plan principal
ZX = CX + 78 * ZS * U            # zèbre centré (sa tête dépasse à gauche)
def scene_base(ctx, t, zs=ZS, zx=None, dim=0.0):
    savanna(ctx, t)
    zebra(ctx, zx if zx is not None else ZX, H * GROUND_Y, zs, t)
    foreground_grass(ctx, t)
    vignette(ctx)
    if dim: rgba(ctx, (0.01, 0.0, 0.03), dim); ctx.paint()

def title2(ctx, l1, l2, c1=WHITE, c2=GOLD, a=1.0, y1=0.105, y2=0.160, size=140):
    if a <= 0: return
    poster_text(ctx, l1, CX, H * y1, size * U, c1, W * 0.88)
    poster_text(ctx, l2, CX, H * y2, size * U, c2, W * 0.90)

CARD_Y = (0.218, 0.272, 0.326)

# ---------------------------------------------------------------- scènes
def sc_hook(ctx, t, d):
    """Image 1 : le zèbre en grand + la question + les 3 réponses numérotées (formule du pantalon, 61 %)."""
    scene_base(ctx, t)
    pill(ctx, SERIES, CX, H * 0.048, GOLD, 40, 1.0)
    title2(ctx, "WHY THE", "STRIPES?", WHITE, GOLD)
    for i, (n, s_, col) in enumerate(OPTS):
        option_card(ctx, n, s_, col, H * CARD_Y[i])

def sc_ask(ctx, t, d):
    scene_base(ctx, t + 2.4)
    for i, (n, s_, col) in enumerate(OPTS):
        s0, e0 = ST("ask", i), EN("ask", i)
        hi = prog(t, s0 - 0.05, s0 + 0.2) * (1 - prog(t, e0 + 0.1, e0 + 0.4))
        option_card(ctx, n, s_, col, H * CARD_Y[i], hi=hi)
    e2 = EN("ask", 2)
    if t < e2 + 0.1:
        pill(ctx, SERIES, CX, H * 0.048, GOLD, 40, 1.0)
        title2(ctx, "WHY THE", "STRIPES?", WHITE, GOLD)
    else:                                            # compte à rebours pendant la pause
        left = max(0.0, (d - 0.1) - t); n = max(1, min(3, int(math.ceil(left / max(0.3, (d - 0.1 - e2) / 3)))))
        xx, yy, r = CX, H * 0.115, 105 * U; frac = left / max(0.1, d - 0.1 - e2)
        glow(ctx, xx, yy, r * 1.6, GOLD, 0.35)
        neon_path(ctx, lambda c: c.arc(xx, yy, r, -math.pi / 2, -math.pi / 2 + 2 * math.pi * frac), GOLD, 12 * U)
        neon_text(ctx, str(n), xx, yy, 160 * U, WHITE, 1.0, GOLD, fill=0.4)

FLY_TARGETS = [(-60, -40), (120, -60), (-180, -60), (40, 60), (230, -20), (-300, -160)]
def sc_reveal(ctx, t, d):
    """Les taons foncent sur le zèbre, ne ralentissent pas, se cognent aux rayures et repartent (« bonk »)."""
    scene_base(ctx, t + 11)
    rnd = random.Random(3)
    for i, (lx, ly) in enumerate(FLY_TARGETS):
        T0 = zxy(lx, ly, ZX, H * GROUND_Y, ZS)
        side = -1 if i % 2 else 1
        S0 = (T0[0] + side * W * (0.45 + 0.1 * rnd.random()), T0[1] - H * (0.08 + 0.08 * rnd.random()))
        E0 = (T0[0] + side * W * (0.25 + 0.2 * rnd.random()), T0[1] - H * (0.12 + 0.06 * rnd.random()))
        x, y, ang, a, hit = fly_track(t, i, S0, T0, E0, P=1.9 + 0.25 * i, off=0.37 * i)
        fly(ctx, x, y, 30 * U, ang, t + i, a * prog(t, 0.1 + 0.15 * i, 0.3 + 0.15 * i))
        bonk(ctx, T0[0], T0[1], hit * a * prog(t, 0.1 + 0.15 * i, 0.3 + 0.15 * i))
    option_card(ctx, "2", "IT'S NUMBER 2!", CYAN, H * 0.065, 1.0, good=True, w=0.74)
    poster_text(ctx, "BITING FLIES!", CX, H * 0.135, 140 * U, GOLD, W * 0.90)
    s1 = ST("reveal", 1)
    pill(ctx, "THEY STRUGGLE TO LAND ON STRIPES", CX, H * 0.205, GREEN, 42, prog(t, s1, s1 + 0.3))
    note(ctx, "FLIES ENLARGED · SIMPLIFIED ILLUSTRATION", H * 0.26, prog(t, 0.6, 0.9))

LANDED = [(-120, -60), (-20, -90), (90, -40), (180, -80), (30, 20), (-180, 0), (250, 0), (140, 50)]
NECK_FLIES = [(-300, -200), (-420, -230)]
def sc_twist(ctx, t, d):
    """L'expérience : un cheval couvert de taons ; on lui met un manteau rayé → les taons repartent ou rebondissent."""
    savanna(ctx, t + 16)
    L = EN("twist", 0); c0 = 0.28 * L
    hx = ZX; hs = ZS
    coat = prog(t, c0, c0 + 0.55)
    horse(ctx, hx, H * GROUND_Y, hs, t, coat=coat)
    for i, (lx, ly) in enumerate(LANDED):   # taons posés sur le dos du cheval, qui s'envolent quand le manteau arrive
        x0, y0 = zxy(lx, ly, hx, H * GROUND_Y, hs)
        k = prog(t, c0 + 0.05 * i, c0 + 0.6 + 0.05 * i)
        x = x0 + k * (W * 0.6 * (1 if i % 2 else -1)); y = y0 - k * H * (0.18 + 0.03 * i)
        fly(ctx, x, y, 24 * U, -0.4 + 0.8 * (i % 3) if k <= 0 else (-0.6 if i % 2 else 3.7), t * (0.3 if k <= 0 else 1) + i, 1 - k, landed=k <= 0)
    for i, (lx, ly) in enumerate(NECK_FLIES):   # sur la tête et le cou (non couverts), ils restent (fidèle à l'étude)
        x0, y0 = zxy(lx, ly, hx, H * GROUND_Y, hs); fly(ctx, x0, y0, 24 * U, 0.5 + i, t + i, 1.0, landed=True)
    if coat > 0.9:
        for i, (lx, ly) in enumerate(FLY_TARGETS[:4]):
            T0 = zxy(lx, ly, hx, H * GROUND_Y, hs); side = -1 if i % 2 else 1
            S0 = (T0[0] + side * W * 0.5, T0[1] - H * 0.12); E0 = (T0[0] + side * W * 0.3, T0[1] - H * 0.16)
            x, y, ang, a, hit = fly_track(t - c0, i, S0, T0, E0, P=1.6 + 0.2 * i, off=0.4 * i)
            fly(ctx, x, y, 24 * U, ang, t + i, a); bonk(ctx, T0[0], T0[1], hit * a)
    foreground_grass(ctx, t + 16); vignette(ctx)
    pill(ctx, "REAL EXPERIMENT · UK, 2019", CX, H * 0.055, GOLD, 40, 1.0)
    if coat < 0.5:
        title2(ctx, "PLAIN COAT:", "FLIES LAND", WHITE, CORAL, 1.0)
    else:
        title2(ctx, "STRIPED COAT:", "FAR FEWER!", WHITE, GREEN, 1.0)
    note(ctx, "HEAD AND NECK STAYED UNCOVERED", H * 0.215, prog(t, c0 + 0.9, c0 + 1.2))

def sc_fact(ctx, t, d):
    """Une loupe sur le flanc : sous les rayures, la peau est noire."""
    scene_base(ctx, t + 20)
    cx_, cy_ = zxy(20, -20, ZX, H * GROUND_Y, ZS)
    k = prog(t, 0.6, 1.6); r = 210 * U * ease(k)
    if r > 2:
        ctx.save(); ctx.new_path(); ctx.arc(cx_, cy_, r, 0, 2 * math.pi); ctx.clip()
        g = cairo.RadialGradient(cx_ - r * 0.3, cy_ - r * 0.4, r * 0.1, cx_, cy_, r * 1.1)
        g.add_color_stop_rgb(0, 0.30, 0.27, 0.30); g.add_color_stop_rgb(1, 0.07, 0.06, 0.07)
        ctx.set_source(g); ctx.paint()
        rnd = random.Random(2)
        for i in range(90):   # grain de la peau
            circle(ctx, cx_ + (rnd.random() - 0.5) * 2 * r, cy_ + (rnd.random() - 0.5) * 2 * r, rnd.uniform(1, 3) * U, (0.45, 0.42, 0.45), 0.35)
        ctx.restore()
        neon_path(ctx, lambda c: c.arc(cx_, cy_, r, 0, 2 * math.pi), GOLD, 7 * U, 1.0)
        ctx.new_path(); ctx.move_to(cx_ + r * 0.71, cy_ + r * 0.71); ctx.line_to(cx_ + r * 0.71 + 120 * U * k, cy_ + r * 0.71 + 120 * U * k)
        ctx.set_line_width(26 * U); ctx.set_line_cap(cairo.LINE_CAP_ROUND); rgba(ctx, GOLD, k); ctx.stroke()
    pill(ctx, SERIES, CX, H * 0.048, GOLD, 40, 1.0)
    title2(ctx, "UNDER THE STRIPES:", "BLACK SKIN!", WHITE, GOLD, prog(t, 0.1, 0.4), size=120)

def sc_outro(ctx, t, d):
    """Retour au zèbre de la 1re image (boucle naturelle), puis l'abonnement pour l'épisode suivant (~2 s)."""
    scene_base(ctx, t)
    c0 = EN("outro", 0) + 0.05
    if t < c0 + 0.2:
        a = 1 - prog(t, c0, c0 + 0.2)
        if a > 0: title2(ctx, "DID YOU GET", "IT RIGHT?", WHITE, GOLD, a)
    else:
        rgba(ctx, (0.0, 0.0, 0.03), 0.62 * prog(t, c0, c0 + 0.4)); ctx.paint()
        cta(ctx, t - c0, d - c0, "SUBSCRIBE FOR", "ANIMAL MYSTERY #4")

SHORT_SCENES = ["hook", "ask", "reveal", "twist", "fact", "outro"]
SCENES = dict(hook=sc_hook, ask=sc_ask, reveal=sc_reveal, twist=sc_twist, fact=sc_fact, outro=sc_outro)

def cover(ctx):
    """Affiche : le zèbre au crépuscule, la question, sans la réponse ; zone sûre 14–86 %."""
    savanna(ctx, 0.5, sun_y=0.52)
    zebra(ctx, CX + 78 * 1.22 * U, H * 0.775, 1.22, 0.3)
    foreground_grass(ctx, 0.5); vignette(ctx)
    pill(ctx, SERIES, CX, H * 0.165, GOLD, 50, 1.0)
    poster_text(ctx, "WHY THE", CX, H * 0.232, 170 * U, WHITE, W * 0.88)
    poster_text(ctx, "STRIPES?", CX, H * 0.305, 190 * U, GOLD, W * 0.92)
    rrect(ctx, CX - 430 * U, H * 0.825 - 60 * U, 860 * U, 120 * U, 60 * U); rgba(ctx, GOLD, 1); ctx.fill()
    rrect(ctx, CX - 430 * U, H * 0.825 - 60 * U, 860 * U, 120 * U, 60 * U); ctx.set_line_width(7 * U); rgba(ctx, (0.01, 0.01, 0.02), 1); ctx.stroke()
    text(ctx, "1, 2 OR 3?", CX, H * 0.825, 74 * U, (0.02, 0.03, 0.06))
