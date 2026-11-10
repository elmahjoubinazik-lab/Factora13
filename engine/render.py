"""Factora - moteur de rendu vidéo (illustrations vectorielles + sous-titres).
Usage: python3 engine/render.py long|short EPISODE_DIR [t1,t2,...]   (t = captures d'écran de contrôle)
L'épisode fournit scenes.py (fonctions de dessin + dict SCENES + SHORT_SCENES) et build/voice.wav + build/timeline.json (via tts.py).
"""
import sys, json, math, random, subprocess
import cairo
import numpy as np
import soundfile as sf

import os
MODE, EP = sys.argv[1], sys.argv[2].rstrip('/')
WD = EP + '/build'
os.makedirs(WD, exist_ok=True)
FPS = 30
W, H = {"long": (1920, 1080), "short": (1440, 2560), "thumb": (1280, 720)}[MODE]
U = min(W, H) / 1080.0          # unité d'échelle
CX, CY = W / 2, H / 2
VERT = H > W

# ---------- palette ----------
NAVY = (0.035, 0.05, 0.12)
NAVY2 = (0.08, 0.11, 0.24)
GOLD = (1.0, 0.78, 0.18)
MOON = (0.95, 0.93, 0.85)
SEA = (0.13, 0.45, 0.78)
SEA_D = (0.05, 0.22, 0.45)
EARTH_G = (0.25, 0.62, 0.38)
WHITE = (1, 1, 1)
CORAL = (1.0, 0.36, 0.38)
CYAN = (0.20, 0.85, 1.0)
GREEN = (0.30, 0.95, 0.55)
PINK = (1.0, 0.42, 0.75)
PURPLE = (0.66, 0.45, 1.0)

random.seed(7)
STARS = [(random.random(), random.random(), random.uniform(0.6, 2.4), random.random() * 6.28) for _ in range(260)]

# ---------- helpers ----------
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def ease(x): x = clamp(x); return x * x * (3 - 2 * x)
def prog(t, a, b): return ease((t - a) / (b - a)) if b > a else 1.0
def mix(c1, c2, k): return tuple(c1[i] + (c2[i] - c1[i]) * k for i in range(3))

def rgba(ctx, c, a=1.0): ctx.set_source_rgba(c[0], c[1], c[2], a)

def vgrad(ctx, top, bot, y0=0, y1=None):
    g = cairo.LinearGradient(0, y0, 0, y1 if y1 is not None else H)
    g.add_color_stop_rgb(0, *top); g.add_color_stop_rgb(1, *bot)
    ctx.set_source(g); ctx.rectangle(0, y0, W, (y1 or H) - y0); ctx.fill()

def circle(ctx, x, y, r, c, a=1.0):
    ctx.arc(x, y, r, 0, 2 * math.pi); rgba(ctx, c, a); ctx.fill()

def glow(ctx, x, y, r, c, a=0.5):
    g = cairo.RadialGradient(x, y, 0, x, y, r)
    g.add_color_stop_rgba(0, c[0], c[1], c[2], a); g.add_color_stop_rgba(1, c[0], c[1], c[2], 0)
    ctx.set_source(g); ctx.arc(x, y, r, 0, 2 * math.pi); ctx.fill()

def font(ctx, size, bold=True):
    ctx.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(size)

def text(ctx, s, x, y, size, c=WHITE, a=1.0, bold=True, align="c"):
    font(ctx, size, bold)
    e = ctx.text_extents(s)
    dx = {"c": -e.width / 2 - e.x_bearing, "l": -e.x_bearing, "r": -e.width - e.x_bearing}[align]
    ctx.move_to(x + dx, y + size * 0.35); rgba(ctx, c, a); ctx.show_text(s)
    return e.width

def rrect(ctx, x, y, w, h, r):
    ctx.new_sub_path()
    ctx.arc(x + w - r, y + r, r, -math.pi / 2, 0); ctx.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    ctx.arc(x + r, y + h - r, r, math.pi / 2, math.pi); ctx.arc(x + r, y + r, r, math.pi, 1.5 * math.pi)
    ctx.close_path()

def stars(ctx, t, a=1.0):
    for sx, sy, sr, ph in STARS:
        tw = 0.55 + 0.45 * math.sin(t * 1.7 + ph)
        circle(ctx, sx * W, sy * H, sr * U, WHITE, a * tw)

def moon(ctx, x, y, r, a=1.0):
    glow(ctx, x, y, r * 3.2, MOON, 0.28 * a)
    circle(ctx, x, y, r, MOON, a)
    for (dx, dy, rr) in [(-0.3, -0.2, 0.18), (0.25, 0.1, 0.12), (-0.05, 0.35, 0.1), (0.35, -0.3, 0.07)]:
        circle(ctx, x + dx * r, y + dy * r, rr * r, (0.82, 0.80, 0.72), a)

def earth(ctx, x, y, r, a=1.0):
    glow(ctx, x, y, r * 1.35, (0.4, 0.7, 1.0), 0.35 * a)
    circle(ctx, x, y, r, SEA, a)
    ctx.save(); ctx.arc(x, y, r, 0, 2 * math.pi); ctx.clip()
    for (dx, dy, rx, ry) in [(-0.35, -0.3, 0.38, 0.25), (0.3, 0.25, 0.3, 0.4), (-0.2, 0.5, 0.22, 0.15), (0.45, -0.45, 0.2, 0.15)]:
        ctx.save(); ctx.translate(x + dx * r, y + dy * r); ctx.scale(rx * r, ry * r)
        ctx.arc(0, 0, 1, 0, 2 * math.pi); ctx.restore(); rgba(ctx, EARTH_G, a); ctx.fill()
    ctx.restore()

def sun(ctx, x, y, r, t, a=1.0):
    glow(ctx, x, y, r * 3, GOLD, 0.45 * a)
    for i in range(16):
        ang = i / 16 * 2 * math.pi + t * 0.2
        ctx.move_to(x + math.cos(ang) * r * 1.15, y + math.sin(ang) * r * 1.15)
        ctx.line_to(x + math.cos(ang) * r * 1.45, y + math.sin(ang) * r * 1.45)
    rgba(ctx, GOLD, a); ctx.set_line_width(6 * U); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    circle(ctx, x, y, r, (1.0, 0.86, 0.45), a)

def chip(ctx, label, t, a=1.0):
    k = prog(t, 0.2, 0.8) * a
    font(ctx, 30 * U); w = ctx.text_extents(label).width + 50 * U
    x, y = (60 * U, 60 * U) if not VERT else (CX - w / 2, 150 * U)
    rrect(ctx, x, y, w, 60 * U, 30 * U); rgba(ctx, GOLD, 0.95 * k); ctx.fill()
    text(ctx, label, x + w / 2, y + 30 * U, 30 * U, NAVY, k)

_OWL = []
def mascot(ctx, cx, cy, size, a=1.0, t=0.0):
    """Mascotte Factora (chouette constellation, logo de la chaîne depuis le 2026-11-10) : engine/assets/owl.png."""
    if a <= 0: return
    if not _OWL:
        try: _OWL.append(cairo.ImageSurface.create_from_png(os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "owl.png")))
        except Exception: _OWL.append(None)
    img = _OWL[0]
    if img is None: return
    glow(ctx, cx, cy, size * 0.95, PURPLE, 0.40 * a)
    glow(ctx, cx, cy - size * 0.05, size * 0.45, GREEN, 0.18 * a * (0.6 + 0.4 * math.sin(t * 4)))
    k = size / max(img.get_width(), img.get_height())
    ctx.save(); ctx.translate(cx, cy); ctx.scale(k, k)
    ctx.set_source_surface(img, -img.get_width() / 2, -img.get_height() / 2); ctx.paint_with_alpha(a)
    ctx.restore()

def cta(ctx, t, d, line1="WANT MORE?", line2="MORE THINGS YOU NEVER NOTICED", y=None):
    """Appel à l'abonnement final (commun à toutes les vidéos) : bouton qui claque à l'écran avec rebond,
    curseur qui clique, bouton qui passe à SUBSCRIBED, cloche qui sonne, explosion de confettis.
    Placé au-dessus de la zone des sous-titres."""
    y = y if y is not None else (H * 0.42 if VERT else H * 0.5)
    S = (1.4 if VERT else 1.05) * U
    k_in = clamp((t - 0.15) / 0.35)
    sc = ease(k_in) * (1 + 0.3 * math.sin(k_in * math.pi) * (1 - k_in))       # arrivée avec rebond
    tc = d * 0.45                                                                # instant du clic
    clicked = t >= tc
    bw, bh = 560 * S, 130 * S
    # mascotte au-dessus du titre (demande de Nazik, 2026-11-10) : arrive avec un rebond, flotte, petit saut au clic
    mk = clamp(t / 0.45)
    msc = ease(mk) * (1 + 0.25 * math.sin(mk * math.pi) * (1 - mk))
    hop = -28 * S * math.exp(-((t - tc - 0.15) * 7) ** 2)
    msize = (210 if VERT else 170) * S
    mascot(ctx, CX, y - 230 * S - (175 if VERT else 150) * S + 8 * S * math.sin(t * 3) + hop, msize * msc, min(1.0, mk * 2), t)
    # titre
    tk = prog(t, 0.0, 0.3)
    font(ctx, 100 * S); tw = ctx.text_extents(line1).width
    ts = 100 * S * min(1.0, W * 0.9 / max(1, tw))
    text(ctx, line1, CX + 5 * S, y - 230 * S + 7 * S, ts, (0, 0, 0), 0.5 * tk)
    text(ctx, line1, CX, y - 230 * S, ts, GOLD, tk)
    # confettis au clic (derrière le bouton)
    if clicked:
        e = t - tc
        rnd = random.Random(11)
        for i in range(110):
            ang = rnd.uniform(0, 2 * math.pi); sp = rnd.uniform(500, 1500) * U
            px = CX + math.cos(ang) * sp * e; py = y + math.sin(ang) * sp * e * 0.8 + 900 * U * e * e
            c = [GOLD, CYAN, CORAL, GREEN, PINK, PURPLE][i % 6]
            a = clamp(1 - e / 1.8)
            if a > 0:
                ctx.save(); ctx.translate(px, py); ctx.rotate(e * 9 + i)
                ctx.rectangle(-12 * S, -6 * S, 24 * S, 12 * S); rgba(ctx, c, a); ctx.fill(); ctx.restore()
    if sc > 0:
        pulse = 1 + (0.05 * math.sin(t * 9) if not clicked else 0)
        press = 1 - 0.12 * math.exp(-((t - tc) * 14) ** 2)
        ctx.save(); ctx.translate(CX, y); ctx.scale(sc * pulse * press, sc * pulse * press)
        col = CORAL if not clicked else (0.30, 0.34, 0.46)
        glow(ctx, 0, 0, bw * 0.95, col if not clicked else GREEN, 0.5 if not clicked else 0.3)
        rrect(ctx, -bw / 2 + 8 * S, -bh / 2 + 12 * S, bw, bh, bh / 2); rgba(ctx, (0, 0, 0), 0.45); ctx.fill()
        rrect(ctx, -bw / 2, -bh / 2, bw, bh, bh / 2)
        g = cairo.LinearGradient(0, -bh / 2, 0, bh / 2)
        g.add_color_stop_rgb(0, *mix(col, WHITE, 0.25)); g.add_color_stop_rgb(1, *col); ctx.set_source(g); ctx.fill()
        if not clicked:
            text(ctx, "SUBSCRIBE", 0, 0, 66 * S, WHITE)
        else:
            text(ctx, "SUBSCRIBED", 35 * S, 0, 58 * S, WHITE)
            ctx.set_line_width(10 * S); ctx.set_line_cap(cairo.LINE_CAP_ROUND); rgba(ctx, GREEN)
            cx0 = -bw / 2 + 75 * S
            ctx.move_to(cx0 - 24 * S, 0); ctx.line_to(cx0 - 6 * S, 20 * S); ctx.line_to(cx0 + 28 * S, -22 * S); ctx.stroke()
        ctx.restore()
        # cloche en badge, au-dessus du coin droit du bouton ; elle sonne après le clic
        bx, by = CX + bw / 2 * sc - 30 * S, y - bh / 2 * sc - 30 * S
        sw = 0.55 * math.sin((t - tc) * 22) * math.exp(-(t - tc) * 2.2) if clicked else 0.1 * math.sin(t * 5)
        ctx.save(); ctx.translate(bx, by); ctx.rotate(sw); ctx.scale(S * sc * 0.9, S * sc * 0.9)
        glow(ctx, 0, 20, 110, GOLD, 0.5 if clicked else 0.2)
        circle(ctx, 0, 20, 62, NAVY, 0.9)
        ctx.move_to(-38, 50); ctx.curve_to(-38, -12, -30, -8, 0, -10)
        ctx.curve_to(30, -8, 38, -12, 38, 50); ctx.line_to(47, 60); ctx.line_to(-47, 60); ctx.close_path()
        rgba(ctx, GOLD); ctx.fill(); circle(ctx, 0, 70, 11, GOLD); circle(ctx, 0, -15, 8, GOLD)
        if clicked:
            ctx.set_line_width(6); rgba(ctx, GOLD, clamp(1 - (t - tc) / 1.5)); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
            for sgn in (-1, 1):
                for r in (70, 92):
                    ctx.new_path(); ctx.arc(0, 20, r, -math.pi / 2 + sgn * 0.5 - 0.3, -math.pi / 2 + sgn * 0.5 + 0.3); ctx.stroke()
        ctx.restore()
    # curseur qui arrive et clique
    if tc - 0.7 < t < tc + 0.6:
        k = ease(clamp((t - (tc - 0.7)) / 0.6))
        hx = CX + 110 * S + (1 - k) * 300 * S; hy = y + 20 * S + (1 - k) * 320 * S
        hs = 1.5 * S * (0.85 if abs(t - tc) < 0.08 else 1.0)
        ctx.save(); ctx.translate(hx, hy); ctx.scale(hs, hs)
        ctx.move_to(0, 0); ctx.line_to(0, 62); ctx.line_to(15, 48); ctx.line_to(27, 72); ctx.line_to(37, 67); ctx.line_to(25, 44); ctx.line_to(45, 44); ctx.close_path()
        rgba(ctx, WHITE); ctx.fill_preserve(); ctx.set_line_width(4); rgba(ctx, NAVY); ctx.stroke(); ctx.restore()
    # 2e ligne sous le bouton (reste au-dessus des sous-titres)
    lk = prog(t, d * 0.55, d * 0.7)
    if lk:
        font(ctx, 52 * S); lw = ctx.text_extents(line2).width
        ls = 52 * S * min(1.0, W * 0.88 / max(1, lw))
        text(ctx, line2, CX, y + 175 * S, ls, WHITE, lk)
        # signature de la marque (décision de Nazik, 2026-11-09)
        _sg = "THINK FAST. LEARN SOMETHING AMAZING."; font(ctx, 34 * S); _ss = 34 * S * min(1.0, W * 0.88 / max(1.0, ctx.text_extents(_sg).width))   # jamais coupée sur les bords
        text(ctx, _sg, CX, y + 265 * S, _ss, GOLD, 0.85 * lk)

def neon_path(ctx, draw, col, width, a=1.0, col2=None):
    """Trace « néon » : halo large et doux, puis trait coloré, puis cœur blanc. draw(ctx) construit le chemin."""
    if a <= 0: return
    c2 = col2 or col
    for w, al, c in ((width * 5.0, 0.10, c2), (width * 2.6, 0.22, col), (width * 1.4, 0.55, col), (width * 0.55, 0.95, mix(col, WHITE, 0.65))):
        ctx.new_path(); draw(ctx)
        ctx.set_line_width(w); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        rgba(ctx, c, al * a); ctx.stroke()

def neon_text(ctx, s, x, y, size, col, a=1.0, col2=None, fill=0.0):
    """Texte néon (contour lumineux) centré en (x, y) ; fill > 0 ajoute un remplissage doux."""
    if a <= 0: return
    font(ctx, size); e = ctx.text_extents(s)
    ox, oy = x - e.width / 2 - e.x_bearing, y + size * 0.35
    def d(c):
        c.move_to(ox, oy); c.text_path(s)
    if fill > 0:
        ctx.new_path(); d(ctx); rgba(ctx, col, fill * a); ctx.fill()
    neon_path(ctx, d, col, max(2.0, size * 0.045), a, col2)

def neon_bg(ctx, t, c1=(0.10, 0.04, 0.22), c2=(0.01, 0.02, 0.08), tint=PURPLE):
    """Fond sobre : dégradé sombre + grand halo coloré lent + quelques particules."""
    vgrad(ctx, c1, c2)
    glow(ctx, W * (0.5 + 0.15 * math.sin(t * 0.3)), H * 0.42, 0.85 * max(W, H), tint, 0.18)
    rnd = random.Random(8)
    for i in range(26):
        x = rnd.random() * W; y = (rnd.random() * H - t * rnd.uniform(10, 40) * U) % H
        circle(ctx, x, y, rnd.uniform(3, 8) * U, rnd.choice([PINK, CYAN, PURPLE]), 0.25 + 0.15 * math.sin(t * 2 + i))

def houses(ctx, ybase, c, a=1.0):
    rgba(ctx, c, a)
    x = -20
    random.seed(3)
    while x < W + 40:
        w = random.uniform(90, 170) * U; h = random.uniform(80, 170) * U
        ctx.rectangle(x, ybase - h, w, h + H)
        ctx.move_to(x - 8 * U, ybase - h); ctx.line_to(x + w / 2, ybase - h - 55 * U); ctx.line_to(x + w + 8 * U, ybase - h)
        ctx.close_path(); ctx.fill()
        x += w + random.uniform(10, 40) * U

def thumb_text(c, line1, line2, badge=None):
    """Texte standard des miniatures Factora (à gauche, 2 lignes + bandeau rouge)."""
    def t(txt, x, y, sz, col):
        c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(sz)
        c.move_to(x + 4, y + 4); c.set_source_rgba(0, 0, 0, .7); c.show_text(txt)
        c.move_to(x, y); c.set_source_rgb(*col); c.show_text(txt)
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(88)
    wmax = max(c.text_extents(line1).width, c.text_extents(line2).width)
    sz = 88 * min(1.0, 720 / wmax)          # le texte ne dépasse jamais 720 px (moitié gauche de la miniature)
    t(line1, 50, 250, sz, (1, 1, 1)); t(line2, 50, 250 + sz * 1.2, sz, (1, .8, .33))
    if badge:
        c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(48); w = c.text_extents(badge).width
        c.set_source_rgb(.85, .12, .12); c.rectangle(50, 415, w + 50, 80); c.fill(); t(badge, 75, 472, 48, (1, 1, 1))

# ---------- langue (config.json → langue) ----------
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LANG = json.load(open(ROOT + "/config.json", encoding="utf-8")).get("langue", "fr")
TR = {}
def T(txt):
    """Texte à l'écran : la clé est la version française ; traduction dans TR[LANG] (défini dans scenes.py)."""
    return TR.get(LANG, {}).get(txt, txt)

# ---------- réutiliser les scènes d'un autre épisode (récap hebdomadaire) ----------
def episode_scenes(path):
    """Charge le scenes.py d'un épisode déjà publié dans un espace de noms séparé et renvoie son dict SCENES.
    Usage dans le scenes.py du récap : A = episode_scenes("episodes/005-airplane"); SCENES = {"e005_wing": A["wing"], ...}"""
    path = path.rstrip("/")
    if not os.path.isabs(path): path = os.path.join(ROOT, path)
    ns = dict(globals()); ns["EP"] = path; ns["TR"] = {}
    exec(open(path + "/scenes.py", encoding="utf-8").read(), ns)
    tr = ns.get("TR", {})
    if tr:   # textes à l'écran traduits propres à cet épisode
        def _T(txt, _tr=tr): return _tr.get(LANG, {}).get(txt, txt)
        ns["T"] = _T
    return ns["SCENES"]

# ---------- scènes de l'épisode ----------
exec(open(EP + '/scenes.py', encoding='utf-8').read())

if MODE == "thumb":   # miniature 1280x720 dessinée par thumbnail(ctx) de l'épisode
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    thumbnail(cairo.Context(surf))
    surf.write_to_png(WD + "/miniature.png"); print("OK", WD + "/miniature.png"); sys.exit(0)

# ---------- sous-titres (style « Shorts » : gros texte contouré, mot prononcé surligné en or) ----------
def chunks(sent):
    words = sent["text"].split()
    n = 4 if VERT else 6
    groups = [words[i:i + n] for i in range(0, len(words), n)]
    if len(groups) > 1 and len(groups[-1]) <= 1: last = groups.pop(); groups[-1] += last
    total = sum(len(" ".join(g)) for g in groups); t = sent["start"]; out = []
    for g in groups:
        s = " ".join(g); dur = (sent["end"] - sent["start"]) * len(s) / total
        out.append((t, t + dur, s)); t += dur
    return out

def cap_font(ctx, size):
    ctx.select_font_face("Inter ExtraBold", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(size)

def draw_caption(ctx, s, k=1.0):
    """s = texte du groupe, k = avancement (0..1) dans le groupe → mot actif surligné."""
    size = (76 if VERT else 58) * U
    cap_font(ctx, size)
    words = s.split()
    # mot actif : proportionnel à la longueur des mots
    lens = [len(w) + 1 for w in words]; acc, act = 0, len(words) - 1
    for i, L in enumerate(lens):
        acc += L
        if k * sum(lens) < acc: act = i; break
    maxw = W * 0.88
    lines, cur = [], []
    for i, w in enumerate(words):
        test = " ".join(words[j] for j in cur + [i])
        if cur and ctx.text_extents(test).width > maxw: lines.append(cur); cur = [i]
        else: cur.append(i)
    lines.append(cur)
    lh = size * 1.2
    y0 = (H * 0.86 if not VERT else H * 0.73) - lh * (len(lines) - 1) / 2
    sp = ctx.text_extents("a a").x_advance - 2 * ctx.text_extents("a").x_advance
    for li, idxs in enumerate(lines):
        wid = [ctx.text_extents(words[i]).x_advance for i in idxs]
        x = CX - (sum(wid) + sp * (len(idxs) - 1)) / 2
        y = y0 + li * lh + size * 0.35
        for i, wd in zip(idxs, wid):
            on = (i == act)
            z = 1.0
            ctx.save(); ctx.translate(x + wd / 2, y - size * 0.35); ctx.scale(z, z); ctx.translate(-(x + wd / 2), -(y - size * 0.35))
            # ombre portée douce
            ctx.move_to(x + 4 * U, y + 6 * U); ctx.text_path(words[i]); ctx.set_source_rgba(0, 0, 0, 0.45); ctx.fill()
            # contour épais
            ctx.move_to(x, y); ctx.text_path(words[i])
            ctx.set_source_rgba(0.01, 0.02, 0.06, 1); ctx.set_line_width(size * 0.16); ctx.set_line_join(cairo.LINE_JOIN_ROUND); ctx.stroke_preserve()
            rgba(ctx, GOLD if on else WHITE); ctx.fill()
            ctx.restore()
            x += wd + sp

# ---------- montage ----------
timeline = json.load(open(WD + "/timeline.json"))
if MODE == "short":
    segs = [s for s in timeline if s["scene"] in SHORT_SCENES]
else:
    segs = timeline
voice, SR = sf.read(WD + "/voice.wav", dtype="float32")
pieces, plan, t0 = [], [], 0.0
for i, s in enumerate(segs):
    a, b = (0.0 if i == 0 else s["start"]), s["end"]
    pieces.append(voice[int(a * SR):int(b * SR)])
    off = t0 - a
    caps = [(x + off, y + off, txt) for sent in s["sents"] for (x, y, txt) in chunks(sent)]
    plan.append(dict(scene=s["scene"], start=t0, end=t0 + (b - a), caps=caps))
    t0 += b - a
# vidéo longue : la conclusion dure au moins 20 s (durée minimale de l'écran de fin YouTube)
if MODE == "long" and plan[-1]["end"] - plan[-1]["start"] < 20:
    extra = 20 - (plan[-1]["end"] - plan[-1]["start"])
    pieces.append(np.zeros(int(extra * SR), np.float32)); plan[-1]["end"] += extra; t0 += extra
TOTAL = t0 + 0.6
vo = np.concatenate(pieces + [np.zeros(int(0.6 * SR), np.float32)])

# Short : accroche écrite en grand dès la première image (meta « hook_text », sinon short_title sans emoji ni #shorts)
HOOK, HOOK_Y = "", 0.16   # hook_y (meta) : hauteur du bandeau d'accroche, en fraction de H
if MODE == "short":
    _mp = EP + f"/meta_{LANG}.json"
    _mp = _mp if os.path.exists(_mp) else EP + "/meta.json"
    try:
        _m = json.load(open(_mp, encoding="utf-8"))
        HOOK = _m.get("hook_text") or _m.get("short_title", "")
        HOOK_Y = float(_m.get("hook_y", HOOK_Y))
    except Exception:
        HOOK = ""
    HOOK = "".join(ch for ch in HOOK.replace("#shorts", "") if ord(ch) < 0x2190).strip().upper()

def draw_hook(ctx, a):
    if not HOOK or a <= 0: return
    size = 78 * U; font(ctx, size)
    words, lines, cur = HOOK.split(), [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if ctx.text_extents(test).width > W * 0.84 and cur: lines.append(cur); cur = w
        else: cur = test
    lines.append(cur)
    if len(lines) == 2:   # 2 lignes équilibrées (évite un mot seul en 2e ligne, ex. « THINK / AGAIN »)
        best = min(((max(ctx.text_extents(" ".join(words[:k])).width, ctx.text_extents(" ".join(words[k:])).width), k) for k in range(1, len(words))))
        if best[0] <= W * 0.84: lines = [" ".join(words[:best[1]]), " ".join(words[best[1]:])]
    lh = size * 1.18; y0 = H * HOOK_Y
    bw = max(ctx.text_extents(l).width for l in lines) + 70 * U
    rrect(ctx, CX - bw / 2, y0 - lh * 0.75, bw, lh * len(lines) + lh * 0.5, 28 * U); rgba(ctx, (0.02, 0.03, 0.10), (0.97 if TNOW < 2.0 / FPS else 0.82) * a); ctx.fill()
    rrect(ctx, CX - bw / 2, y0 - lh * 0.75, bw, lh * len(lines) + lh * 0.5, 28 * U); rgba(ctx, GOLD, 0.95 * a); ctx.set_line_width(5 * U); ctx.stroke()
    for i, l in enumerate(lines): text(ctx, l, CX, y0 + i * lh, size, GOLD if i == len(lines) - 1 else WHITE, a)

# musique d'ambiance générée (libre de droits) : nappe douce Am - F - C - G
def music(total, sr=SR):
    n = int(total * sr); tt = np.arange(n) / sr; out = np.zeros(n, np.float32)
    chords = [[220.0, 261.63, 329.63], [174.61, 220.0, 261.63], [196.0, 261.63, 329.63], [196.0, 246.94, 293.66]]
    L = 4.0
    for ci in range(int(total / L) + 2):
        c = chords[ci % 4]; st = ci * L
        idx = (tt >= st - 0.5) & (tt < st + L + 1.5)
        loc = tt[idx] - st
        env = np.clip((loc + 0.5) / 1.5, 0, 1) * np.clip((L + 1.5 - loc) / 2.0, 0, 1)
        sig = sum(np.sin(2 * np.pi * f * tt[idx]) + 0.5 * np.sin(2 * np.pi * f * 1.003 * tt[idx]) + 0.15 * np.sin(2 * np.pi * f * 2 * tt[idx]) for f in c)
        sig += 0.8 * np.sin(2 * np.pi * c[0] / 2 * tt[idx])
        out[idx] += (sig * env).astype(np.float32)
    out /= np.max(np.abs(out)) + 1e-9
    fade = np.clip(tt / 2, 0, 1) * np.clip((total - tt) / 2.5, 0, 1)
    return out * fade * 0.08
def music_mystery(total, sr=SR):
    """Ambiance « enquête » : drone grave en ré mineur qui respire, horloge, pluie douce."""
    n = int(total * sr); tt = np.arange(n) / sr; out = np.zeros(n, np.float32)
    for f, a in [(73.42, 1.0), (87.31, 0.5), (110.0, 0.6), (146.83, 0.25)]:
        out += (a * np.sin(2 * np.pi * f * tt + 0.3 * np.sin(2 * np.pi * 0.1 * tt))).astype(np.float32)
    out *= (0.5 + 0.5 * np.sin(2 * np.pi * 0.07 * tt - 1.5) ** 2).astype(np.float32)
    out /= np.max(np.abs(out)) + 1e-9
    L = int(0.03 * sr); tk = np.sin(2 * np.pi * 2400 * np.arange(L) / sr) * np.exp(-np.arange(L) / (0.004 * sr))
    for s0 in np.arange(0.5, total, 0.5):
        i = int(s0 * sr)
        if i + L < n: out[i:i + L] += (0.35 if int(s0 * 2) % 2 else 0.22) * tk
    # pulsation de basse (croches ~100 bpm) qui donne de l'élan, plus forte vers la fin
    beat = 60 / 100 / 2; Lb = int(0.16 * sr)
    for j, s0 in enumerate(np.arange(0.0, total, beat)):
        i = int(s0 * sr)
        if i + Lb < n:
            f0 = 73.42 if (j // 8) % 2 == 0 else 65.41
            env = np.exp(-np.arange(Lb) / (0.05 * sr)) * (0.55 + 0.45 * min(1.0, s0 / max(1.0, total * 0.8)))
            out[i:i + Lb] += (0.55 if j % 2 == 0 else 0.35) * (np.sin(2 * np.pi * f0 * np.arange(Lb) / sr) * env).astype(np.float32)
    rng = np.random.default_rng(3); rain = rng.standard_normal(n).astype(np.float32)
    rain = np.convolve(rain, np.ones(24) / 24, mode="same"); out += 0.25 * rain / (np.max(np.abs(rain)) + 1e-9)
    out /= np.max(np.abs(out)) + 1e-9
    fade = np.clip(tt / 1.0, 0, 1) * np.clip((total - tt) / 1.5, 0, 1)
    return out * fade * 0.16

def music_upbeat(total, sr=SR, bpm=122):
    """Musique énergique originale (générée, libre de droits) : kick sur chaque temps, clap sur 2 et 4,
    charleston en contretemps, basse en croches et arpège pluck en doubles-croches sur La m - Fa - Do - Sol."""
    n = int(total * sr); tt = np.arange(n) / sr; out = np.zeros(n, np.float32)
    rng = np.random.default_rng(9)
    beat = 60.0 / bpm
    roots = [110.0, 87.31, 130.81, 98.0]                       # A2 F2 C3 G2
    chords = [[440.0, 523.25, 659.25], [349.23, 440.0, 523.25], [523.25, 659.25, 783.99], [392.0, 493.88, 587.33]]
    def add(t0, sig, g):
        i = int(t0 * sr); j = min(n, i + len(sig))
        if 0 <= i < n: out[i:j] += (g * sig[:j - i]).astype(np.float32)
    Lk = int(0.28 * sr); tk = np.arange(Lk) / sr
    kick = np.sin(2 * np.pi * (45 * tk + 75 * (1 - np.exp(-tk / 0.035)) * 0.035 * 10)) * np.exp(-tk / 0.11)
    Lc = int(0.18 * sr); clap = rng.standard_normal(Lc) * np.exp(-np.arange(Lc) / (0.035 * sr))
    clap = np.convolve(clap, [1, -0.9], mode="same")
    Lh = int(0.05 * sr); hat = np.diff(rng.standard_normal(Lh + 1)) * np.exp(-np.arange(Lh) / (0.012 * sr))
    nb = int(total / beat) + 1
    for b in range(nb):
        t0 = b * beat; bar = (b // 4) % 4
        add(t0, kick, 0.9)
        if b % 4 in (1, 3): add(t0, clap, 0.35)
        add(t0 + beat / 2, hat, 0.22)
        for e in (0, 1):                                          # basse en croches
            Lb = int(beat / 2 * 0.9 * sr); tb = np.arange(Lb) / sr; f = roots[bar]
            bass = (np.sin(2 * np.pi * f * tb) + 0.4 * np.sin(2 * np.pi * 2 * f * tb) + 0.2 * np.sin(2 * np.pi * 3 * f * tb)) * np.exp(-tb / 0.18)
            add(t0 + e * beat / 2, bass, 0.32 if e == 0 else 0.22)
        for q in range(4):                                        # arpège pluck en doubles-croches
            f = chords[bar][(b * 4 + q) % 3] * (2 if q == 3 else 1)
            Lp = int(0.16 * sr); tp = np.arange(Lp) / sr
            pl = (np.sin(2 * np.pi * f * tp) + 0.3 * np.sin(2 * np.pi * 2 * f * tp)) * np.exp(-tp / 0.06)
            add(t0 + q * beat / 4, pl, 0.10)
    out /= np.max(np.abs(out)) + 1e-9
    fade = np.clip(tt / 0.3, 0, 1) * np.clip((total - tt) / 1.5, 0, 1)
    return out * fade * 0.25   # ~14 dB sous la voix : présente mais sans gêner

def music_hype(total, sr=SR, bpm=140):
    """Musique très énergique originale (générée, libre de droits ; demande de Nazik 2026-11-10 : « plus de dynamisme ») :
    140 bpm, kick à chaque temps + basse « pompée » (sidechain), clap sur 2 et 4, charleston en doubles-croches,
    stabs de synthé en contretemps, montée (riser) toutes les 4 mesures et crash au début de chaque phrase."""
    n = int(total * sr); tt = np.arange(n) / sr; out = np.zeros(n, np.float32); rng = np.random.default_rng(5)
    beat = 60.0 / bpm; bar = 4 * beat
    roots = [110.0, 87.31, 130.81, 98.0]
    chords = [[440.0, 523.25, 659.25], [349.23, 440.0, 523.25], [523.25, 659.25, 783.99], [392.0, 493.88, 587.33]]
    def add(t0, sig, g):
        i = int(t0 * sr); j = min(n, i + len(sig))
        if 0 <= i < n: out[i:j] += (g * sig[:j - i]).astype(np.float32)
    Lk = int(0.22 * sr); tk = np.arange(Lk) / sr
    kick = np.sin(2 * np.pi * (50 * tk + 2.6 * (1 - np.exp(-tk / 0.03)))) * np.exp(-tk / 0.09)
    Lc = int(0.16 * sr); clap = np.convolve(rng.standard_normal(Lc) * np.exp(-np.arange(Lc) / (0.03 * sr)), [1, -0.95], mode="same")
    Lh = int(0.035 * sr); hat = np.diff(rng.standard_normal(Lh + 1)) * np.exp(-np.arange(Lh) / (0.008 * sr))
    Lo = int(0.12 * sr); ohat = np.diff(rng.standard_normal(Lo + 1)) * np.exp(-np.arange(Lo) / (0.04 * sr))
    # basse continue « pompée » par le kick (effet sidechain)
    bass = np.zeros(n, np.float32)
    for b in range(int(total / beat) + 1):
        f = roots[(b // 4) % 4]; i0 = int(b * beat * sr); L = int(beat * sr); i1 = min(n, i0 + L)
        if i0 >= n: break
        tb = np.arange(i1 - i0) / sr
        env = np.clip(tb / (beat * 0.45), 0, 1) ** 1.5                                   # remonte après chaque kick
        bass[i0:i1] = (np.sign(np.sin(2 * np.pi * f * tb)) * 0.35 + np.sin(2 * np.pi * f * tb)) * env
    bass = np.convolve(bass, np.ones(12) / 12, mode="same")
    out += 0.30 * bass
    for b in range(int(total / beat) + 1):
        t0 = b * beat; ci = (b // 4) % 4
        add(t0, kick, 1.0)
        if b % 4 in (1, 3): add(t0, clap, 0.45)
        for q in range(4): add(t0 + q * beat / 4, hat, 0.20 if q % 2 else 0.12)
        add(t0 + beat / 2, ohat, 0.18)
        Ls = int(0.11 * sr); ts = np.arange(Ls) / sr
        stab = sum(np.sign(np.sin(2 * np.pi * f * ts)) for f in chords[ci]) / 3 * np.exp(-ts / 0.05)
        add(t0 + beat / 2, stab, 0.16)
    # riser (bruit qui monte) sur la dernière mesure de chaque phrase de 4 mesures, crash au début de la suivante
    Lcr = int(1.2 * sr); crash = rng.standard_normal(Lcr) * np.exp(-np.arange(Lcr) / (0.35 * sr))
    for ph in range(int(total / (4 * bar)) + 1):
        t0 = ph * 4 * bar
        add(t0, crash, 0.20)
        Lr = int(bar * sr); tr = np.arange(Lr) / sr
        riser = rng.standard_normal(Lr) * (tr / bar) ** 2
        add(t0 + 3 * bar, np.convolve(riser, np.ones(4) / 4, mode="same"), 0.16)
    out /= np.max(np.abs(out)) + 1e-9
    fade = np.clip(tt / 0.05, 0, 1) * np.clip((total - tt) / 1.2, 0, 1)
    return out * fade * 0.30   # ~12 dB sous la voix

def sfx_track(total, events, sr=SR):
    """Bruitages : thunder (coup de tonnerre), heartbeat (battements qui accélèrent, dur), hit (impact grave)."""
    n = int(total * sr); out = np.zeros(n, np.float32); rng = np.random.default_rng(11)
    for ev in events:
        i0 = int(ev["t"] * sr); kind = ev["type"]
        if kind == "thunder":
            L = int(3.0 * sr); x = rng.standard_normal(L).astype(np.float32)
            x = np.convolve(x, np.ones(60) / 60, mode="same")
            env = np.exp(-np.arange(L) / (0.9 * sr)); env[:int(0.05 * sr)] *= np.linspace(0, 1, int(0.05 * sr))
            crack = rng.standard_normal(L).astype(np.float32) * np.exp(-np.arange(L) / (0.08 * sr)) * 0.5
            seg = (x / (np.max(np.abs(x)) + 1e-9) * env + crack) * 0.9 * float(ev.get("vol", 1.0))
        elif kind == "heartbeat":
            dur = ev.get("dur", 3.0); L = int(dur * sr); seg = np.zeros(L, np.float32); s0 = 0.0; per = 0.9
            while s0 < dur - 0.3:
                for off, amp in [(0, 1.0), (0.2, 0.7)]:
                    j = int((s0 + off) * sr); m = int(0.18 * sr)
                    if j + m < L: seg[j:j + m] += amp * np.sin(2 * np.pi * 55 * np.arange(m) / sr) * np.exp(-np.arange(m) / (0.05 * sr))
                s0 += per; per = max(0.45, per * 0.88)
            seg *= 0.9
        elif kind == "riser":   # montée de tension (bruit filtré + glissando) avant une question
            dur = ev.get("dur", 2.0); L = int(dur * sr); tl = np.arange(L) / sr
            x = rng.standard_normal(L).astype(np.float32); x = np.convolve(x, np.ones(8) / 8, mode="same")
            sweep = np.sin(2 * np.pi * (200 * tl + 400 * tl ** 2 / dur))
            seg = ((0.5 * x / (np.max(np.abs(x)) + 1e-9) + 0.4 * sweep) * (tl / dur) ** 2 * 0.8).astype(np.float32)
        elif kind == "whoosh":   # transition rapide (bruit filtré qui monte puis retombe)
            dur = ev.get("dur", 0.45); L = int(dur * sr); tl = np.arange(L) / sr
            x = rng.standard_normal(L).astype(np.float32)
            x = np.convolve(x, np.ones(6) / 6, mode="same") - np.convolve(x, np.ones(40) / 40, mode="same")
            env = np.sin(np.pi * np.clip(tl / dur, 0, 1)) ** 2
            seg = (x / (np.max(np.abs(x)) + 1e-9) * env * 0.55 * float(ev.get("vol", 1.0))).astype(np.float32)
        else:  # hit
            L = int(1.5 * sr); seg = (np.sin(2 * np.pi * 45 * np.arange(L) / sr) * np.exp(-np.arange(L) / (0.35 * sr))).astype(np.float32)
        j1 = min(n, i0 + len(seg))
        if j1 > i0: out[i0:j1] += seg[:j1 - i0]
    return out

_MOOD, _SFX, _mm = "", [], {}
try:
    _mm = json.load(open(EP + f"/meta_{LANG}.json", encoding="utf-8")) if os.path.exists(EP + f"/meta_{LANG}.json") else {}
    _MOOD = _mm.get("music", "")
    for ev in _mm.get("sfx", []):
        seg0 = next((sg for sg in plan if sg["scene"] == ev["scene"]), None)
        if seg0: _SFX.append({**ev, "t": seg0["start"] + ev.get("at", 0.0)})
except Exception:
    pass
SFX_TIMES = [(e["t"], e["type"]) for e in _SFX]
_FD = max(0.01, float(_mm.get("fade", 0.3)))   # durée du fondu au noir entre scènes (meta « fade » ; 0.06 ≈ cut sec)
mus = music_mystery(len(vo) / SR) if _MOOD == "mystery" else (music_upbeat(len(vo) / SR) if _MOOD == "upbeat" else (music_hype(len(vo) / SR) if _MOOD == "hype" else music(len(vo) / SR)))
if _SFX: mus = mus + sfx_track(len(vo) / SR, _SFX)
mixd = vo * 0.95 + mus[:len(vo)]
mixd /= max(1.0, np.max(np.abs(mixd)) / 0.97)
sf.write(WD + f"/audio_{MODE}.wav", mixd, SR)

out = WD + f"/video_{MODE}.mp4"
STILLS = [float(x) for x in sys.argv[3].split(",")] if len(sys.argv) > 3 else None
# finition « cinéma » appliquée par ffmpeg : halo lumineux (bloom) sur les zones claires, vignette, grain très léger ;
# la vidéo longue est agrandie en 1440p (YouTube attribue alors un meilleur codec/débit, image nettement plus nette).
FINISH = ("format=gbrp,split[a][b];[b]colorlevels=rimin=0.5:gimin=0.5:bimin=0.5,gblur=sigma=%d[g];[a][g]blend=all_mode=screen:all_opacity=0.55,"
          "colorbalance=rs=0.03:bs=0.07:bm=0.03:rh=0.02,eq=saturation=1.75:contrast=1.1:brightness=0.025:gamma=1.06,vibrance=intensity=0.35,vignette=angle=PI/5,noise=alls=2:allf=t" % int(18 * U))
if MODE == "long" and TOTAL <= 330: FINISH += ",scale=2560:1440:flags=lanczos"   # > 5 min 30 : reste en 1080p (fichier < 100 Mo)   # (pas de grain : il alourdit trop le fichier, limite GitHub 100 Mo)
elif MODE == "long": FINISH += ",noise=alls=2:allf=t"
if MODE == "short": FINISH += ",unsharp=5:5:0.5:5:5:0.0"
# séquences filmées (clips générés par IA, meta « finish » = "photo") : finition légère, sinon la peau devient orange
if _mm.get("finish") == "photo":
    FINISH = "eq=saturation=1.12:contrast=1.04,vibrance=intensity=0.18,vignette=angle=PI/5" + (",unsharp=5:5:0.6:5:5:0.0" if MODE == "short" else "")   # Short rendu nativement en 1440×2560, sans grain, léger piqué (demande de Nazik 2026-11-08)
class _N:
    def write(self, b): pass
    def close(self): pass
class _P:
    stdin=_N()
    def wait(self): pass
ff = _P() if STILLS else subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                       "-i", WD + f"/audio_{MODE}.wav", "-vf", FINISH, "-c:v", "libx264", "-preset", "slow", "-tune", "animation", "-crf", ("19" if MODE == "long" else "18"), *(["-maxrate", "1500k", "-bufsize", "3000k"] if MODE == "long" else []), "-pix_fmt", "yuv420p", "-r", str(FPS),
                       "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
nf = int(TOTAL * FPS)
for f in (STILLS or range(nf)):
    TNOW = f if STILLS else f / FPS
    seg = next((p for p in plan if p["start"] <= TNOW < p["end"]), plan[-1])
    ctx = cairo.Context(surf)
    ctx.set_source_rgb(0, 0, 0); ctx.paint()   # repartir d'une image vide (évite les restes de la scène précédente)
    lt, d = TNOW - seg["start"], seg["end"] - seg["start"]
    # Short : les 2 premières images servent de couverture (Instagram/TikTok prennent la 1re image) :
    # on y montre la scène d'accroche déjà bien avancée (illustration complète) + l'accroche écrite.
    if MODE == "short" and seg is plan[0] and TNOW < 2.0 / FPS: lt = min(d * 0.6, 2.4)
    # mouvement de caméra (zoom lent + léger panoramique, sens alterné d'une scène à l'autre)
    si = plan.index(seg); z = 1 + 0.045 * ease(lt / d); px = (1 if si % 2 else -1) * 14 * U * (lt / d - 0.5)
    ctx.save(); ctx.translate(CX + px, CY); ctx.scale(z, z); ctx.translate(-CX, -CY)
    SCENES[seg["scene"]](ctx, lt, d)
    ctx.restore()
    for (a, b, s) in seg["caps"]:
        if a <= TNOW < b: draw_caption(ctx, s, (TNOW - a) / max(b - a, 1e-6)); break
    # fondu entre scènes
    fade = min(clamp(lt / _FD), clamp((d - lt) / _FD)) if seg is not plan[0] or lt > _FD else clamp(lt / _FD)
    if MODE == "short" and seg is plan[0]: fade = clamp((d - lt) / _FD)   # Short : pas d'écran noir au départ
    if MODE == "short": draw_hook(ctx, 1 - prog(TNOW, 2.6, 3.2))
    if fade < 1: ctx.set_source_rgba(0, 0, 0, 1 - fade); ctx.paint()
    surf.flush()
    ff.stdin.write(surf.get_data())
    if STILLS: surf.write_to_png(WD + f"/still_{MODE}_{TNOW:05.1f}.png")
    if not STILLS and f % 300 == 0: print(MODE, f, "/", nf, flush=True)
ff.stdin.close(); ff.wait()
print("OK", out, TOTAL)
