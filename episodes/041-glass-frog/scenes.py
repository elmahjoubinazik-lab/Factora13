exec(open("engine/photo.py", encoding="utf-8").read())   # poster_text, red_arrow, scrim (aucune image n'est chargée)
# Episode 041 (Short seul, 9:16, ~36 s) - "Glass Frog: Where Does Its Blood Go? | Animal Mystery #2"
# Test décidé avec Nazik le 2026-11-20 : même formule que l'Animal Mystery #1 (quiz, voix Jessica, musique originale
# Runway, nom de l'animal), mais en DESSINS MAISON (néon sobre) au lieu d'images IA — une seule variable changée
# (données du 20/11 : 15 Shorts dessinés depuis le 7/11, médiane 724 vues ; 11 Shorts en images IA, médiane 38).
# Faits : Taboada, Delia et al. (2022), Science 378:1315, « Glassfrogs conceal blood in their liver to maintain
# transparency » (Hyalinobatrachium fleischmanni) : au repos, ~89 % des globules rouges quittent la circulation et sont
# entassés dans le foie, qui est recouvert de cristaux de guanine réfléchissants (AMNH : « mirror-coated liver ») ; la
# transparence est multipliée par 2 à 3 ; le sang revient au réveil ; pas de caillots (mécanisme encore étudié).
# Toutes les tailles en multiples de U ; la grenouille est dessinée dans un repère local (unités ≈ px) puis mise à l'échelle.
import json as _json
_TL = {sg["scene"]: sg for sg in _json.load(open(EP + "/build/timeline.json", encoding="utf-8"))}
def ST(scene, k):
    sg = _TL.get(scene)
    return sg["sents"][k]["start"] - sg["start"] if sg and k < len(sg["sents"]) else 1e9
def EN(scene, k):
    sg = _TL.get(scene)
    return sg["sents"][k]["end"] - sg["start"] if sg and k < len(sg["sents"]) else 1e9

DARK = (0.03, 0.02, 0.08)
SERIES = "ANIMAL MYSTERY #2"
BLOOD = (1.0, 0.10, 0.20)
SILVER = (0.86, 0.93, 1.0)
PALE = (1.0, 0.80, 0.84)          # cœur sans globules rouges (liquide presque clair)
FROG_Y, FROG_S = 0.475, 0.98      # centre vertical (fraction de H) et échelle de la grenouille

# ---------------------------------------------------------------- petits éléments d'interface (comme l'ép. 040)
def pill(ctx, s, x, y, col, size=46, a=1.0):
    if a <= 0: return
    font(ctx, size * U); w_ = ctx.text_extents(s).width + 60 * U
    rrect(ctx, x - w_ / 2, y - size * 0.8 * U, w_, size * 1.6 * U, size * 0.8 * U); rgba(ctx, col, 0.96 * a); ctx.fill()
    text(ctx, s, x, y, size * U, DARK, a)

def note(ctx, s, y, a=1.0):
    """Petite mention discrète (« SIMPLIFIED ILLUSTRATION »)."""
    if a <= 0: return
    font(ctx, 34 * U); w_ = ctx.text_extents(s).width + 40 * U
    rrect(ctx, CX - w_ / 2, y - 28 * U, w_, 56 * U, 28 * U); rgba(ctx, (0.0, 0.0, 0.0), 0.55 * a); ctx.fill()
    text(ctx, s, CX, y, 34 * U, (0.85, 0.90, 1.0), 0.9 * a)

def ring(ctx, x, y, r, col, k):
    """Repère simple : cercle lumineux autour d'un détail."""
    if k <= 0: return
    rr = r * (1.5 - 0.5 * ease(k))
    neon_path(ctx, lambda c: c.arc(x, y, rr, 0, 2 * math.pi), col, 7 * U, k)

OPTS = [("1", "ITS HEART STOPS", CORAL), ("2", "ITS BLOOD TURNS CLEAR", CYAN), ("3", "IT HIDES IN THE LIVER", PURPLE)]
def option_card(ctx, n, s_, col, y, k, good=False):
    if k <= 0: return
    pw, ph = W * 0.84, 120 * U; x = CX + (1 - ease(k)) * W * 0.5
    if good: col = GREEN; glow(ctx, x, y, pw * 0.6, GREEN, 0.45)
    rrect(ctx, x - pw / 2, y - ph / 2, pw, ph, ph / 2); rgba(ctx, (0.04, 0.03, 0.10), 0.92 * k); ctx.fill()
    rrect(ctx, x - pw / 2, y - ph / 2, pw, ph, ph / 2); ctx.set_line_width(7 * U); rgba(ctx, col, k); ctx.stroke()
    circle(ctx, x - pw / 2 + ph / 2, y, ph * 0.38, col, k); text(ctx, n, x - pw / 2 + ph / 2, y, 64 * U, DARK, k)
    font(ctx, 58 * U); tw = ctx.text_extents(s_).width; sz = 58 * U * min(1.0, (pw - ph * 1.5) / tw)
    text(ctx, s_, x + ph * 0.45, y, sz, WHITE, k)

def sparkle(ctx, x, y, r, a, col=WHITE):
    """Petit éclat à 4 branches (reflet des « miroirs » du foie)."""
    if a <= 0: return
    glow(ctx, x, y, r * 1.6, col, 0.5 * a)
    ctx.new_path(); ctx.move_to(x, y - r); ctx.line_to(x + r * 0.18, y - r * 0.18); ctx.line_to(x + r, y); ctx.line_to(x + r * 0.18, y + r * 0.18)
    ctx.line_to(x, y + r); ctx.line_to(x - r * 0.18, y + r * 0.18); ctx.line_to(x - r, y); ctx.line_to(x - r * 0.18, y - r * 0.18); ctx.close_path()
    rgba(ctx, col, a); ctx.fill()

# ---------------------------------------------------------------- géométrie de la grenouille (vue de dessous, repère local)
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

BODY_R = [(0, -300), (70, -294), (118, -266), (138, -228), (134, -188), (132, -150), (148, -90), (156, 0), (150, 90),
          (134, 160), (104, 214), (56, 244), (0, 252)]
BODY = BODY_R + [(-x, y) for x, y in reversed(BODY_R[1:-1])]
ARM = [(128, -140), (238, -120), (256, -228)]                 # épaule, coude, poignet (côté droit)
FINGERS = [(330, -262), (312, -312), (262, -332), (212, -312)]
LEG = [(112, 186), (326, 112), (206, 300), (286, 362)]         # hanche, genou, cheville, base du pied
TOES = [(404, 330), (404, 394), (352, 446), (286, 462), (222, 436)]
HEART = (0, -102)
LIVER = (0, 8)
EYE = (140, -228)

def mirror(pts, sx): return [(sx * x, y) for x, y in pts]

def poly(c, pts):
    c.new_path(); c.move_to(*pts[0])
    for p in pts[1:]: c.line_to(*p)

def limbs(c, extra=0.0):
    """Trace (stroke) les 4 pattes avec la source courante ; extra = épaisseur ajoutée (liseré)."""
    c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_line_join(cairo.LINE_JOIN_ROUND)
    for sx in (1, -1):
        A, L = mirror(ARM, sx), mirror(LEG, sx)
        for seg, w in (((A[0], A[1]), 42), ((A[1], A[2]), 34), ((L[0], L[1]), 66), ((L[1], L[2]), 50), ((L[2], L[3]), 36)):
            poly(c, seg); c.set_line_width(w + extra); c.stroke()
        for tip in mirror(FINGERS, sx):
            poly(c, [A[2], tip]); c.set_line_width(14 + extra); c.stroke()
            c.new_path(); c.arc(tip[0], tip[1], 17 + extra / 2, 0, 2 * math.pi); c.fill()
        for tip in mirror(TOES, sx):
            poly(c, [L[3], tip]); c.set_line_width(14 + extra); c.stroke()
            c.new_path(); c.arc(tip[0], tip[1], 17 + extra / 2, 0, 2 * math.pi); c.fill()

LIVER_PTS = [(-134, 2), (-122, -38), (-84, -58), (-34, -54), (0, -38), (40, -58), (96, -56), (134, -30), (140, 10),
             (112, 46), (54, 58), (0, 42), (-52, 58), (-108, 46)]   # foie à deux lobes, un seul contour
def liver_path(c, cx=0.0, cy=8.0, k=1.0):
    c.new_path(); smooth_closed(c, [(cx + x * k, cy + y * k) for x, y in LIVER_PTS])

def fit_neon(ctx, s, y, size, col, a=1.0, col2=None, fill=0.35, maxw=None):
    """Titre néon centré, réduit s'il dépasse maxw (jamais collé aux bords)."""
    if a <= 0: return
    font(ctx, size); w_ = ctx.text_extents(s).width; mw = maxw or W * 0.88
    neon_text(ctx, s, CX, y, size * min(1.0, mw / max(1.0, w_)), col, a, col2, fill=fill)

def heart_path(c, x, y, r):
    c.new_path(); c.move_to(x, y + r * 0.95)
    c.curve_to(x - r * 1.25, y + r * 0.15, x - r * 0.95, y - r * 0.95, x, y - r * 0.35)
    c.curve_to(x + r * 0.95, y - r * 0.95, x + r * 1.25, y + r * 0.15, x, y + r * 0.95)
    c.close_path()

def vessel_paths():
    """Vaisseaux (des extrémités vers le foie) : servent au dessin du sang et au flux des globules rouges."""
    out = [[(0, -70), (0, -20)], [(0, 230), (0, 60)]]
    for sx in (1, -1):
        A, L = mirror(ARM, sx), mirror(LEG, sx)
        out.append([A[2], A[1], A[0], (sx * 40, -40)])
        out.append([L[3], L[2], L[1], L[0], (sx * 45, 40)])
        for tip in (mirror(TOES, sx)[0], mirror(TOES, sx)[3]): out.append([tip, L[3]])
        out.append([mirror(FINGERS, sx)[1], A[2]])
    return out
VESSELS = vessel_paths()

def along(pts, u):
    """Point à la fraction u (0–1) de la polyligne."""
    lens = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:])]; tot = sum(lens); s = u * tot
    for (a, b), l in zip(zip(pts, pts[1:]), lens):
        if s <= l: f = s / max(l, 1e-6); return a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f
        s -= l
    return pts[-1]

def rbc(c, x, y, r, ang, a=1.0):
    """Globule rouge : disque biconcave (bord foncé, centre clair)."""
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(1.0, 0.62)
    c.new_path(); c.arc(0, 0, r, 0, 2 * math.pi); rgba(c, (0.72, 0.03, 0.10), a); c.fill()
    c.new_path(); c.arc(0, 0, r * 0.78, 0, 2 * math.pi); rgba(c, (0.95, 0.12, 0.20), a); c.fill()
    c.new_path(); c.arc(0, 0, r * 0.38, 0, 2 * math.pi); rgba(c, (1.0, 0.45, 0.50), a); c.fill()
    c.restore()

def frog(ctx, x, y, s, t, blood=1.0, eyes=1.0, skin=0.62, mirror_k=0.0, pack=0.0, flow=0.0, a=1.0, bones=1.0):
    """Grenouille de verre vue de dessous. blood : sang dans les vaisseaux et le cœur (1 éveillée → ~0,08 endormie) ;
    pack : globules rouges entassés dans le foie ; mirror_k : couche « miroir » du foie ; flow : globules qui
    voyagent vers le foie ; skin : opacité de la peau translucide."""
    if a <= 0: return
    S = s * U; br = 1 + 0.012 * math.sin(t * 2.4)
    ctx.save(); ctx.translate(x, y); ctx.scale(S, S * br)
    glow(ctx, 0, 0, 560, GREEN, 0.22 * a)
    # --- peau translucide (groupe opaque, posé avec une opacité : pas de surépaisseur aux croisements)
    ctx.push_group()
    rim = cairo.RadialGradient(0, -40, 40, 0, -40, 520)
    rim.add_color_stop_rgb(0, 0.70, 1.0, 0.62); rim.add_color_stop_rgb(1, 0.42, 0.95, 0.50)
    ctx.set_source(rim); limbs(ctx, extra=10); ctx.new_path(); smooth_closed(ctx, BODY); ctx.set_line_width(10); ctx.stroke()
    g = cairo.RadialGradient(0, -40, 30, 0, -40, 480)
    g.add_color_stop_rgb(0, 0.66, 1.0, 0.56); g.add_color_stop_rgb(0.6, 0.38, 0.88, 0.44); g.add_color_stop_rgb(1, 0.22, 0.70, 0.36)
    ctx.set_source(g); limbs(ctx); ctx.new_path(); smooth_closed(ctx, BODY); ctx.fill()
    ctx.pop_group_to_source(); ctx.paint_with_alpha(skin * a)
    neon_path(ctx, lambda c: smooth_closed(c, BODY), GREEN, 3.5, 0.75 * a)
    # --- squelette (les os se voient à travers la peau)
    ba = 0.30 * bones * a
    if ba > 0:
        ctx.set_line_cap(cairo.LINE_CAP_ROUND); rgba(ctx, WHITE, ba)
        poly(ctx, [(0, -215), (0, 175)]); ctx.set_line_width(9); ctx.stroke()
        for k in range(9):
            yy = -190 + 40 * k; poly(ctx, [(-16, yy), (16, yy)]); ctx.set_line_width(6); ctx.stroke()
        for sx in (1, -1):
            A, L = mirror(ARM, sx), mirror(LEG, sx)
            poly(ctx, [(0, 175), (sx * 100, 192)]); ctx.set_line_width(8); ctx.stroke()
            poly(ctx, [(sx * 20, -150), A[0], A[1], A[2]]); ctx.set_line_width(6); ctx.stroke()
            poly(ctx, [L[0], L[1], L[2], L[3]]); ctx.set_line_width(7); ctx.stroke()
            for tip in mirror(TOES, sx) + mirror(FINGERS, sx):
                base = L[3] if tip in mirror(TOES, sx) else A[2]
                poly(ctx, [base, tip]); ctx.set_line_width(3.5); ctx.stroke()
    # --- intestin (pâle)
    ctx.new_path(); smooth_open(ctx, [(-62, 78), (36, 70), (72, 112), (-18, 134), (-74, 166), (8, 188), (64, 168)])
    ctx.set_line_width(24); ctx.set_line_cap(cairo.LINE_CAP_ROUND); rgba(ctx, (0.98, 0.94, 0.80), 0.30 * a); ctx.stroke()
    # --- vaisseaux sanguins
    if blood > 0.01:
        for pts in VESSELS:
            poly(ctx, pts); ctx.set_line_width(14); rgba(ctx, BLOOD, 0.20 * blood * a); ctx.stroke()
            poly(ctx, pts); ctx.set_line_width(6); rgba(ctx, BLOOD, 0.85 * blood * a); ctx.stroke()
    # --- foie : rouge (globules entassés) puis couche miroir
    lv = mix((0.75, 0.55, 0.55), (0.70, 0.04, 0.12), pack)
    liver_path(ctx, *LIVER); rgba(ctx, lv, (0.55 + 0.4 * pack) * a); ctx.fill()
    if pack > 0.02:
        ctx.save(); liver_path(ctx, *LIVER); ctx.clip()
        rnd = random.Random(4)
        for i in range(int(46 * pack)):
            px, py = rnd.uniform(-130, 135), rnd.uniform(-55, 62)
            rbc(ctx, px + 2 * math.sin(t * 3 + i), py, 16, rnd.uniform(0, 3.1), 0.95 * a)
        ctx.restore()
    if mirror_k > 0:
        mg = cairo.LinearGradient(-140, -60, 140, 60)
        for st_, cc in ((0, SILVER), (0.45, WHITE), (0.55, (0.70, 0.85, 1.0)), (1, SILVER)): mg.add_color_stop_rgba(st_, cc[0], cc[1], cc[2], 0.92 * mirror_k * a)
        liver_path(ctx, *LIVER); ctx.set_source(mg); ctx.fill()
        for i in range(7):
            ph = (t * 1.3 + i * 0.37) % 1.0
            sparkle(ctx, -110 + 37 * i, 8 + 34 * math.sin(i * 1.7), 18, mirror_k * a * math.sin(ph * math.pi))
    neon_path(ctx, lambda c: liver_path(c, *LIVER), mix((1.0, 0.55, 0.6), SILVER, mirror_k), 2.5, 0.7 * a)
    # --- cœur qui bat (rouge si plein de globules, presque clair sinon)
    beat = 1 + 0.10 * max(0.0, math.sin(t * 2 * math.pi * 1.6)) ** 3
    hc = mix(PALE, BLOOD, blood)
    glow(ctx, HEART[0], HEART[1], 120 * beat, hc, (0.25 + 0.35 * blood) * a)
    heart_path(ctx, HEART[0], HEART[1], 44 * beat); rgba(ctx, hc, (0.55 + 0.45 * blood) * a); ctx.fill()
    neon_path(ctx, lambda c: heart_path(c, HEART[0], HEART[1], 44 * beat), mix(WHITE, BLOOD, 0.5 * blood), 2.5, 0.8 * a)
    # --- globules rouges qui voyagent vers le foie
    if flow > 0:
        for j, pts in enumerate(VESSELS):
            n = 3 if len(pts) == 2 else 7
            for i in range(n):
                u = (t * 0.55 + i / n + j * 0.13) % 1.0
                px, py = along(pts, u)
                rbc(ctx, px, py, 13, t * 2 + i, flow * a * min(1.0, 4 * u, 4 * (1 - u)))
    # --- yeux (dorés, pupille horizontale) ; fermés pendant le sommeil
    for sx in (1, -1):
        ex, ey = sx * EYE[0], EYE[1]
        ctx.new_path(); ctx.arc(ex, ey, 46, 0, 2 * math.pi); rgba(ctx, (0.30, 0.75, 0.40), a); ctx.fill()
        if eyes > 0.02:
            ig = cairo.RadialGradient(ex, ey, 4, ex, ey, 42)
            ig.add_color_stop_rgba(0, 1.0, 0.92, 0.55, a * eyes); ig.add_color_stop_rgba(1, 0.85, 0.62, 0.15, a * eyes)
            ctx.new_path(); ctx.save(); ctx.translate(ex, ey); ctx.scale(1, max(0.05, eyes)); ctx.arc(0, 0, 40, 0, 2 * math.pi); ctx.restore()
            ctx.set_source(ig); ctx.fill()
            ctx.new_path(); ctx.save(); ctx.translate(ex, ey); ctx.scale(24, 11 * max(0.05, eyes)); ctx.arc(0, 0, 1, 0, 2 * math.pi); ctx.restore()
            rgba(ctx, (0.02, 0.02, 0.04), a * eyes); ctx.fill()
            circle(ctx, ex - 12, ey - 12 * eyes, 7, WHITE, 0.85 * a * eyes)
        if eyes < 0.98:   # paupière
            ctx.new_path(); ctx.arc(ex, ey, 40, math.pi * 0.05, math.pi * 0.95); rgba(ctx, (0.85, 1.0, 0.75), (1 - eyes) * 0.9 * a)
            ctx.set_line_width(5); ctx.stroke()
        neon_path(ctx, lambda c, ex=ex, ey=ey: c.arc(ex, ey, 46, 0, 2 * math.pi), GREEN, 3, 0.7 * a)
    ctx.restore()

def frog_xy(lx, ly, s=FROG_S, y=None):
    """Point du repère de la grenouille → écran."""
    return CX + lx * s * U, (H * FROG_Y if y is None else y) + ly * s * U

def zzz(ctx, x, y, t, a):
    """« Z z » qui montent : la grenouille dort."""
    if a <= 0: return
    for i in range(3):
        ph = (t * 0.6 + i / 3) % 1.0
        neon_text(ctx, "Z", x + 50 * U * i + 30 * U * ph, y - 160 * U * ph, (44 + 18 * i) * U, CYAN, a * math.sin(ph * math.pi), PURPLE, fill=0.4)

def leaf(ctx, x, y, L, w, ang, a=1.0, veins=1.0):
    """Grande feuille de forêt tropicale (support de la grenouille endormie)."""
    if a <= 0: return
    ctx.save(); ctx.translate(x, y); ctx.rotate(ang)
    def shape(c):
        c.new_path(); c.move_to(-L / 2, 0); c.curve_to(-L / 4, -w, L / 4, -w * 0.9, L / 2, 0); c.curve_to(L / 4, w * 0.9, -L / 4, w, -L / 2, 0); c.close_path()
    g = cairo.LinearGradient(0, -w, 0, w)
    g.add_color_stop_rgba(0, 0.10, 0.42, 0.20, a); g.add_color_stop_rgba(0.5, 0.16, 0.58, 0.26, a); g.add_color_stop_rgba(1, 0.06, 0.30, 0.16, a)
    shape(ctx); ctx.set_source(g); ctx.fill()
    neon_path(ctx, shape, GREEN, 4 * U, 0.6 * a)
    if veins > 0:
        neon_path(ctx, lambda c: (c.move_to(-L / 2, 0), c.line_to(L / 2 - 20 * U, 0)), (0.70, 1.0, 0.55), 3 * U, 0.6 * a * veins)
        for i in range(1, 9):
            xx = -L / 2 + L * i / 9; hw = w * 0.85 * math.sin(math.pi * i / 9)
            for sg in (1, -1):
                neon_path(ctx, lambda c, xx=xx, hw=hw, sg=sg: (c.move_to(xx, 0), c.curve_to(xx + 40 * U, sg * hw * 0.4, xx + 70 * U, sg * hw * 0.8, xx + 90 * U, sg * hw * 0.92)),
                          (0.60, 0.95, 0.50), 2.2 * U, 0.45 * a * veins)
    ctx.restore()

def bg(ctx, t, tint=GREEN):
    """Fond sombre de forêt de nuit : dégradé teal, halo, feuilles lointaines estompées, particules."""
    neon_bg(ctx, t, c1=(0.02, 0.12, 0.12), c2=(0.0, 0.02, 0.05), tint=tint)
    for (lx, ly, L, w, an) in ((0.08, 0.30, 900, 170, 0.9), (0.95, 0.22, 800, 150, -0.8), (0.04, 0.86, 950, 180, -0.6), (0.98, 0.80, 850, 160, 0.7)):
        leaf(ctx, W * lx, H * ly + 12 * U * math.sin(t * 0.8 + lx * 5), L * U, w * U, an, 0.28, veins=0.5)

# ---------------------------------------------------------------- scènes
def title2(ctx, l1, l2, c1=WHITE, c2=GOLD, a=1.0):
    if a <= 0: return
    fit_neon(ctx, l1, H * 0.115, 120 * U, c1, a, PURPLE if c1 == WHITE else c1, fill=0.35)
    fit_neon(ctx, l2, H * 0.180, 132 * U, c2, a, CORAL, fill=0.45)

def sc_hook(ctx, t, d):
    """Image 1 : la grenouille transparente, son cœur qui bat (le mystère se voit) ; 2e phrase : elle s'endort et le
    rouge disparaît → « Where did its blood go? »."""
    bg(ctx, t)
    s1 = ST("hook", 1)
    sl = prog(t, s1, s1 + 0.6); fade = prog(t, s1 + 0.9, s1 + 2.6)
    frog(ctx, CX, H * FROG_Y, FROG_S, t, blood=1 - 0.92 * fade, eyes=1 - sl)
    pill(ctx, SERIES, CX, H * 0.055, GOLD, 40, 1.0)
    hx, hy = frog_xy(*HEART)
    if t < s1 + 0.1:
        title2(ctx, "YOU CAN SEE", "ITS HEART!", WHITE, CORAL)
        ring(ctx, hx, hy, 95 * U, CORAL, prog(t, 0.2, 0.6))
    else:
        title2(ctx, "WHERE DID", "ITS BLOOD GO?", WHITE, GOLD, prog(t, s1 + 0.1, s1 + 0.4))
        ex, ey = frog_xy(EYE[0], EYE[1])
        zzz(ctx, ex + 40 * U, ey - 30 * U, t, sl)

def sc_ask(ctx, t, d):
    bg(ctx, t)
    frog(ctx, CX, H * FROG_Y, FROG_S, t, blood=0.08, eyes=0.0, a=0.55)
    rgba(ctx, (0.0, 0.02, 0.04), 0.35); ctx.paint()
    for i, (n, s_, col) in enumerate(OPTS):
        s0 = ST("ask", i)
        option_card(ctx, n, s_, col, H * (0.38 + 0.095 * i), prog(t, s0 - 0.05, s0 + 0.30))
    e0 = EN("ask", 2)
    if t < e0 + 0.1:
        title2(ctx, "WHERE DID", "ITS BLOOD GO?", WHITE, GOLD)
    else:                                            # compte à rebours pendant la pause
        left = max(0.0, (d - 0.1) - t); n = max(1, min(3, int(math.ceil(left / max(0.3, (d - 0.1 - e0) / 3)))))
        xx, yy, r = CX, H * 0.15, 110 * U; frac = left / max(0.1, d - 0.1 - e0)
        glow(ctx, xx, yy, r * 1.6, GOLD, 0.35)
        neon_path(ctx, lambda c: c.arc(xx, yy, r, -math.pi / 2, -math.pi / 2 + 2 * math.pi * frac), GOLD, 12 * U)
        neon_text(ctx, str(n), xx, yy, 170 * U, WHITE, 1.0, GOLD, fill=0.4)

def sc_reveal(ctx, t, d):
    """Les globules rouges quittent les pattes et le cœur et s'entassent dans le foie (vue « rayons X » simplifiée)."""
    bg(ctx, t)
    k = prog(t, 0.3, d - 0.6)
    frog(ctx, CX, H * FROG_Y, FROG_S, t, blood=1 - 0.92 * k, eyes=0.0, pack=k, flow=min(1.0, 3 * (1 - k)) * prog(t, 0.0, 0.3))
    option_card(ctx, "3", "IT'S NUMBER 3!", PURPLE, H * 0.07, 1.0, good=True)
    fit_neon(ctx, "THE LIVER!", H * 0.148, 140 * U, GOLD, prog(t, 0.1, 0.4), CORAL, fill=0.5)
    s1, s2 = ST("reveal", 1), ST("reveal", 2)   # le nom de l'animal, à l'oral ET à l'écran (règle de la série)
    pill(ctx, "THE GLASS FROG", CX, H * 0.222, GREEN, 54, prog(t, s1, s1 + 0.3))
    lx, ly = frog_xy(*LIVER)
    ring(ctx, lx, ly, 175 * U, GOLD, prog(t, 0.2, 0.6))
    if t > s2:
        kk = prog(t, s2, s2 + 0.35); sc_ = 1 + 0.3 * (1 - kk)
        ctx.save(); ctx.translate(CX, H * 0.635); ctx.scale(sc_, sc_)
        rrect(ctx, -330 * U, -78 * U, 660 * U, 156 * U, 40 * U); rgba(ctx, (0.03, 0.02, 0.08), 0.85 * kk); ctx.fill()
        neon_text(ctx, "≈ 90%", 0, -14 * U, 100 * U, WHITE, kk, CORAL, fill=0.5)
        text(ctx, "OF ITS RED BLOOD CELLS", 0, 50 * U, 34 * U, GOLD, kk)
        ctx.restore()
    note(ctx, "SIMPLIFIED ILLUSTRATION", H * 0.275, prog(t, 0.6, 0.9))

def sc_twist(ctx, t, d):
    """Le foie se couvre de « miroirs » : endormie sur sa feuille, la grenouille devient presque invisible."""
    bg(ctx, t, tint=CYAN)
    leaf(ctx, CX, H * FROG_Y + 20 * U, W * 1.35, 520 * U, -0.10 + 0.01 * math.sin(t), 1.0)
    L = EN("twist", 0)
    m = prog(t, 0.25 * L, 0.50 * L); fade = prog(t, 0.55 * L, 0.85 * L)
    frog(ctx, CX, H * FROG_Y, FROG_S, t, blood=0.06, eyes=0.0, pack=1.0, mirror_k=m, skin=0.62 - 0.47 * fade, a=1.0 - 0.45 * fade, bones=1 - 0.8 * fade)
    fit_neon(ctx, "TINY MIRRORS", H * 0.115, 130 * U, SILVER, prog(t, 0.2 * L, 0.2 * L + 0.3), CYAN, fill=0.45)
    fit_neon(ctx, "ON ITS LIVER", H * 0.180, 100 * U, CYAN, prog(t, 0.3 * L, 0.3 * L + 0.3), PURPLE, fill=0.35)
    pill(ctx, "PREDATORS CAN BARELY SPOT IT", CX, H * 0.25, GREEN, 44, prog(t, 0.62 * L, 0.62 * L + 0.3))
    lx, ly = frog_xy(*LIVER)
    ring(ctx, lx, ly, 175 * U, SILVER, prog(t, 0.25 * L, 0.45 * L) * (1 - fade))

def sc_fact(ctx, t, d):
    """Gros plan sur le foie : globules rouges entassés… sans caillot."""
    bg(ctx, t, tint=CORAL)
    k = 2.9 + 0.08 * t; cy = H * 0.47
    ctx.save(); ctx.translate(CX, cy); ctx.scale(U, U)
    glow(ctx, 0, 0, 640, CORAL, 0.30)
    liver_path(ctx, 0, 0, k); rgba(ctx, (0.55, 0.03, 0.10), 1.0); ctx.fill()
    ctx.save(); liver_path(ctx, 0, 0, k); ctx.clip()
    rnd = random.Random(11)
    for i in range(190):
        px, py = rnd.uniform(-410, 420), rnd.uniform(-180, 180)
        rbc(ctx, px + 3 * math.sin(t * 2.5 + i), py + 2 * math.cos(t * 2 + i), 34, rnd.uniform(0, 3.1), 1.0)
    ctx.restore()
    neon_path(ctx, lambda c: liver_path(c, 0, 0, k), mix(CORAL, SILVER, 0.5), 4, 0.9)
    ctx.restore()
    fit_neon(ctx, "PACKED TIGHT", H * 0.115, 124 * U, WHITE, prog(t, 0.05, 0.35), CORAL, fill=0.4)
    s1 = ST("fact", 1)
    c0 = 0.45 * EN("fact", 0)
    if t < s1 - 0.05:
        pill(ctx, "OUR BLOOD COULD CLOT", CX, H * 0.21, CORAL, 52, prog(t, c0, c0 + 0.3))
    else:
        kk = prog(t, s1 - 0.05, s1 + 0.25); sc_ = 1 + 0.5 * (1 - kk)
        ctx.save(); ctx.translate(CX, H * 0.215); ctx.rotate(-0.05); ctx.scale(sc_, sc_)
        font(ctx, 84 * U); w_ = ctx.text_extents("THEIRS DOESN'T!").width + 70 * U
        rrect(ctx, -w_ / 2, -72 * U, w_, 144 * U, 26 * U); rgba(ctx, (0.02, 0.06, 0.04), 0.9 * kk); ctx.fill()
        rrect(ctx, -w_ / 2, -72 * U, w_, 144 * U, 26 * U); ctx.set_line_width(8 * U); rgba(ctx, GREEN, kk); ctx.stroke()
        text(ctx, "THEIRS DOESN'T!", 0, 0, 84 * U, GREEN, kk); ctx.restore()
    pill(ctx, "GLASS FROG LIVER, ASLEEP", CX, H * 0.665, GOLD, 40, prog(t, 0.4, 0.7))

def sc_outro(ctx, t, d):
    """Retour à la grenouille de la 1re image (boucle naturelle), puis l'abonnement pour l'épisode suivant (~2 s)."""
    bg(ctx, t)
    frog(ctx, CX, H * FROG_Y, FROG_S, t, blood=1.0, eyes=1.0)
    c0 = EN("outro", 0) + 0.05
    if t < c0 + 0.2:
        a = 1 - prog(t, c0, c0 + 0.2)
        if a > 0: title2(ctx, "DID YOU GET", "IT RIGHT?", WHITE, GOLD, a)
    else:
        rgba(ctx, (0.0, 0.02, 0.04), 0.66 * prog(t, c0, c0 + 0.4)); ctx.paint()
        cta(ctx, t - c0, d - c0, "SUBSCRIBE FOR", "ANIMAL MYSTERY #3")

SHORT_SCENES = ["hook", "ask", "reveal", "twist", "fact", "outro"]
SCENES = dict(hook=sc_hook, ask=sc_ask, reveal=sc_reveal, twist=sc_twist, fact=sc_fact, outro=sc_outro)

def cover(ctx):
    """Affiche : la grenouille transparente (cœur et sang visibles), la question, sans la réponse ; zone sûre 14–86 %."""
    bg(ctx, 0.5)
    fy, fs = 0.585, 0.92
    frog(ctx, CX, H * fy, fs, 0.2, blood=1.0, eyes=1.0)
    pill(ctx, SERIES, CX, H * 0.165, GOLD, 50, 1.0)
    poster_text(ctx, "WHERE DOES", CX, H * 0.235, 150 * U, WHITE, W * 0.90)
    poster_text(ctx, "ITS BLOOD GO?", CX, H * 0.305, 150 * U, CORAL, W * 0.92)
    hx, hy = frog_xy(*HEART, s=fs, y=H * fy)
    ring(ctx, hx, hy, 90 * U, GOLD, 1.0)
    red_arrow(ctx, W * 0.93, H * 0.42, hx + 100 * U, hy + 12 * U, bend=-0.18)   # par le côté : ne passe pas sur l'œil
    rrect(ctx, CX - 430 * U, H * 0.82 - 60 * U, 860 * U, 120 * U, 60 * U); rgba(ctx, GOLD, 1); ctx.fill()
    rrect(ctx, CX - 430 * U, H * 0.82 - 60 * U, 860 * U, 120 * U, 60 * U); ctx.set_line_width(7 * U); rgba(ctx, (0.01, 0.01, 0.02), 1); ctx.stroke()
    text(ctx, "1, 2 OR 3?", CX, H * 0.82, 74 * U, (0.02, 0.03, 0.06))
