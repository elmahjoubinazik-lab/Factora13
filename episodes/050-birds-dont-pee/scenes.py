exec(open("engine/photo.py", encoding="utf-8").read())   # poster_text, red_arrow (aucune image extérieure n'est chargée)
# Épisode 050 (Short seul, 9:16, ~32 s) — les oiseaux ne font pas pipi (sujet choisi par Nazik le 2026-11-24 d'après un
# Short à succès ; demande vérifiée : 18,4 M / 266 k / 128 k / 93 k vues en anglais ; Nazik : « pas de dinde, fais sur les
# oiseaux en général »). Stratégie 30 jours : image 1 = un pigeon en grand sur le capot d'une voiture (≥ 75 % de la
# largeur) + « BIRDS NEVER PEE » (3 mots) ; dessins 100 % faits ici ; un plan toutes les ~4–6 s ; fin = retour au pigeon
# de l'image 1 ; CTA texte « Follow Factora for more weird animal facts. ».
# Faits : les oiseaux n'émettent pas d'urine liquide : leurs déchets azotés sortent sous forme d'acide urique, une pâte
# blanche, avec les fèces par une seule ouverture (le cloaque) ; la partie blanche des fientes = l'« urine » ; la plupart
# des oiseaux n'ont pas de vessie (économie d'eau et de poids) ; l'autruche est l'exception connue (elle urine à part) ;
# dans l'œuf, l'embryon stocke ses déchets sous forme d'acide urique solide (cristaux) dans l'allantoïde, sans s'intoxiquer.
# Voix Kokoro (ElevenLabs épuisé) : pas d'horodatage par mot → WT() estime l'instant d'un mot dans sa phrase.
import json as _json, re as _re

_TLL = _json.load(open(EP + "/build/timeline.json", encoding="utf-8"))
_TL = {sg["scene"]: sg for sg in _TLL}
_FIRST = _TLL[0]["scene"]
_WT = []
for sg in _TLL:
    for se in sg["sents"]:
        txt = se["text"]; n = max(1, len(txt))
        for m in _re.finditer(r"\S+", txt):
            _WT.append((m.group().lower().strip(".,?!:;'\""), se["start"] + (se["end"] - se["start"]) * m.start() / n))
def WT(word, n=0):
    hits = [t for w, t in _WT if w == word.lower()]
    return hits[n] if n < len(hits) else 1e9
def SENT(scene, i=0): return _TL[scene]["sents"][i]["start"]
END_T = _TLL[-1]["end"] + 0.6

DARK = (0.03, 0.02, 0.08)
def lerp(a, b, k): return a + (b - a) * k

# ---------------------------------------------------------------- textes
def tag(ctx, s, y=0.083, a=1.0):
    if a <= 0: return
    font(ctx, 32 * U); w_ = ctx.text_extents(s).width + 40 * U
    x0, y0 = W * 0.055, H * y
    rrect(ctx, x0, y0 - 25 * U, w_, 50 * U, 25 * U); rgba(ctx, (0.0, 0.0, 0.0), 0.50 * a); ctx.fill()
    text(ctx, s, x0 + 20 * U, y0, 32 * U, (0.92, 0.94, 1.0), 0.92 * a, align="l")

def pill(ctx, s, x, y, col, size=50, a=1.0, k=1.0, fg=DARK):
    if a <= 0 or k <= 0: return
    sc_ = 0.6 + 0.4 * ease(k) + 0.08 * math.sin(math.pi * clamp(k))
    ctx.save(); ctx.translate(x, y); ctx.scale(sc_, sc_)
    font(ctx, size * U); w_ = ctx.text_extents(s).width + 64 * U; h_ = size * 1.6 * U
    glow(ctx, 0, 0, w_ * 0.7, col, 0.35 * a)
    rrect(ctx, -w_ / 2, -h_ / 2, w_, h_, h_ / 2); rgba(ctx, col, 0.97 * a); ctx.fill()
    text(ctx, s, 0, 0, size * U, fg, a)
    ctx.restore()

def leader(ctx, x0, y0, x1, y1, col, a=1.0, k=1.0):
    if a <= 0 or k <= 0: return
    xe, ye = x0 + (x1 - x0) * ease(k), y0 + (y1 - y0) * ease(k)
    for w_, al, c_ in ((9 * U, 0.35, DARK), (4.5 * U, 1.0, col)):
        ctx.new_path(); ctx.move_to(x0, y0); ctx.line_to(xe, ye); ctx.set_line_width(w_); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        rgba(ctx, c_, al * a); ctx.stroke()
    if k > 0.95: circle(ctx, x1, y1, 11 * U, col, a); circle(ctx, x1, y1, 5 * U, WHITE, a)

def cta_lines(ctx, lines, x, ys, size, a):
    sz = size * U; maxw = W * 0.74
    cap_font(ctx, sz)
    widest = max(ctx.text_extents(l).width for l in lines)
    if widest > maxw: sz *= maxw / widest; cap_font(ctx, sz)
    for l, y, col in zip(lines, ys, (WHITE, GOLD)):
        e = ctx.text_extents(l); x0 = x - e.width / 2 - e.x_bearing; y0 = y + sz * 0.35
        ctx.move_to(x0 + 3 * U, y0 + 5 * U); ctx.text_path(l); rgba(ctx, (0, 0, 0), 0.45 * a); ctx.fill()
        ctx.move_to(x0, y0); ctx.text_path(l); ctx.set_line_width(sz * 0.16); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        rgba(ctx, (0.01, 0.02, 0.06), a); ctx.stroke_preserve(); rgba(ctx, col, a); ctx.fill()

def ellipse(ctx, x, y, rx, ry, rot=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(rx, ry); ctx.arc(0, 0, 1, 0, 2 * math.pi); ctx.restore()

def no_sign(ctx, x, y, r, a=1.0):
    ctx.new_path(); ctx.arc(x, y, r, 0, 2 * math.pi); ctx.set_line_width(r * 0.16); rgba(ctx, (0.92, 0.15, 0.18), a); ctx.stroke()
    ctx.new_path(); ctx.move_to(x - r * 0.7, y - r * 0.7); ctx.line_to(x + r * 0.7, y + r * 0.7); ctx.stroke()

def drop(ctx, x, y, r, col, a=1.0):
    ctx.new_path(); ctx.move_to(x, y - r * 1.6)
    ctx.curve_to(x + r * 0.4, y - r * 0.9, x + r, y - r * 0.2, x + r, y + r * 0.25)
    ctx.arc(x, y + r * 0.25, r, 0, math.pi)
    ctx.curve_to(x - r, y - r * 0.2, x - r * 0.4, y - r * 0.9, x, y - r * 1.6); ctx.close_path()
    rgba(ctx, col, a); ctx.fill()

# ---------------------------------------------------------------- le pigeon (image 1 et fin)
def pigeon(ctx, x, y, s, T, blink=0.0):
    """Pigeon de profil (tourné vers la gauche), centre du corps (x, y), s = demi-longueur du corps.
    La tête avance et recule (le hochement du pigeon)."""
    bob = 0.10 * s * math.sin(T * 5.0)
    for sx, dx in ((1, 0.10), (-1, -0.12)):   # pattes roses
        fx = x + dx * s
        ctx.new_path(); ctx.move_to(fx, y + 0.50 * s); ctx.line_to(fx - 0.04 * s, y + 0.78 * s); ctx.set_line_width(0.06 * s); ctx.set_line_cap(cairo.LINE_CAP_ROUND); rgba(ctx, (0.92, 0.45, 0.48), 1); ctx.stroke()
        for d in (-0.14, 0.0, 0.10):
            ctx.new_path(); ctx.move_to(fx - 0.04 * s, y + 0.78 * s); ctx.line_to(fx - 0.04 * s + d * s, y + 0.84 * s); ctx.set_line_width(0.045 * s); ctx.stroke()
    # queue
    ctx.new_path(); ctx.move_to(x + 0.70 * s, y + 0.05 * s); ctx.line_to(x + 1.35 * s, y + 0.30 * s); ctx.line_to(x + 1.30 * s, y + 0.48 * s); ctx.line_to(x + 0.62 * s, y + 0.32 * s); ctx.close_path()
    rgba(ctx, (0.36, 0.38, 0.46), 1); ctx.fill()
    ctx.rectangle(x + 1.12 * s, y + 0.24 * s, 0.10 * s, 0.22 * s); rgba(ctx, (0.18, 0.18, 0.24), 0.8); ctx.fill()
    # corps
    ctx.new_path(); ellipse(ctx, x, y + 0.08 * s, 0.82 * s, 0.50 * s, 0.10)
    g = cairo.LinearGradient(0, y - 0.45 * s, 0, y + 0.6 * s); g.add_color_stop_rgb(0, 0.66, 0.68, 0.76); g.add_color_stop_rgb(1, 0.50, 0.52, 0.60)
    ctx.set_source(g); ctx.fill_preserve(); ctx.set_line_width(5 * U); rgba(ctx, (0.25, 0.26, 0.32), 0.9); ctx.stroke()
    # aile + 2 barres sombres
    ctx.new_path(); ellipse(ctx, x + 0.22 * s, y + 0.02 * s, 0.58 * s, 0.30 * s, 0.18)
    g = cairo.LinearGradient(x - 0.3 * s, 0, x + 0.8 * s, 0); g.add_color_stop_rgb(0, 0.72, 0.74, 0.82); g.add_color_stop_rgb(1, 0.56, 0.58, 0.66)
    ctx.set_source(g); ctx.fill_preserve(); ctx.set_line_width(4 * U); rgba(ctx, (0.30, 0.31, 0.38), 0.8); ctx.stroke()
    for k in (0.0, 0.16):   # les 2 barres sombres de l'aile du pigeon
        ctx.new_path(); ellipse(ctx, x + (0.40 + k) * s, y + 0.05 * s, 0.05 * s, 0.22 * s, -0.35); rgba(ctx, (0.20, 0.20, 0.26), 0.92); ctx.fill()
    # cou irisé
    hx, hy = x - 0.70 * s + bob, y - 0.52 * s
    ctx.new_path(); ctx.move_to(x - 0.35 * s, y - 0.30 * s); ctx.curve_to(x - 0.50 * s, y - 0.55 * s, hx + 0.10 * s, hy + 0.20 * s, hx + 0.12 * s, hy)
    ctx.line_to(hx - 0.18 * s, hy + 0.05 * s); ctx.curve_to(hx - 0.15 * s, hy + 0.35 * s, x - 0.80 * s, y + 0.10 * s, x - 0.55 * s, y + 0.25 * s); ctx.close_path()
    g = cairo.LinearGradient(hx - 0.2 * s, hy, x - 0.3 * s, y + 0.2 * s)
    g.add_color_stop_rgb(0, 0.35, 0.65, 0.45); g.add_color_stop_rgb(0.5, 0.55, 0.35, 0.65); g.add_color_stop_rgb(1, 0.55, 0.57, 0.66)
    ctx.set_source(g); ctx.fill()
    # tête
    circle(ctx, hx, hy - 0.08 * s, 0.22 * s, (0.52, 0.54, 0.64), 1)
    ctx.new_path(); ctx.arc(hx, hy - 0.08 * s, 0.22 * s, 0, 2 * math.pi); ctx.set_line_width(4 * U); rgba(ctx, (0.25, 0.26, 0.32), 0.8); ctx.stroke()
    ex, ey = hx - 0.07 * s, hy - 0.13 * s
    circle(ctx, ex, ey, 0.065 * s, (0.95, 0.55, 0.15), 1); circle(ctx, ex, ey, 0.035 * s, (0.05, 0.04, 0.06), 1); circle(ctx, ex - 0.012 * s, ey - 0.015 * s, 0.012 * s, WHITE, 1)
    if blink > 0: ctx.rectangle(ex - 0.07 * s, ey - 0.07 * s, 0.14 * s, 0.14 * s * blink); rgba(ctx, (0.52, 0.54, 0.64), 1); ctx.fill()
    # bec (cire blanche)
    ctx.new_path(); ctx.move_to(hx - 0.18 * s, hy - 0.10 * s); ctx.line_to(hx - 0.40 * s, hy - 0.04 * s); ctx.line_to(hx - 0.18 * s, hy - 0.01 * s); ctx.close_path(); rgba(ctx, (0.25, 0.22, 0.25), 1); ctx.fill()
    ctx.new_path(); ellipse(ctx, hx - 0.21 * s, hy - 0.08 * s, 0.05 * s, 0.03 * s); rgba(ctx, (0.96, 0.95, 0.93), 1); ctx.fill()

def _blink(T, ph=0.0):
    u = (T + ph) % 3.1
    return math.sin(math.pi * u / 0.16) if u < 0.16 else 0.0

def pigeon_scene(ctx, T, title=("BIRDS", "NEVER PEE"), k_title=1.0):
    car_bg(ctx, T)
    pigeon(ctx, W * 0.455, H * 0.485 + 4 * U * math.sin(T * 2.5), W * 0.36, T, _blink(T))
    if k_title > 0:
        ctx.push_group()
        poster_text(ctx, title[0], W * 0.47, H * 0.105, 175 * U, WHITE, W * 0.86)
        poster_text(ctx, title[1], W * 0.47, H * 0.180, 175 * U, GOLD, W * 0.86)
        ctx.pop_group_to_source(); ctx.paint_with_alpha(k_title)

# ---------------------------------------------------------------- petits oiseaux (B)
def small_bird(ctx, x, y, s, body, belly, head, beak=(0.98, 0.75, 0.25), T=0.0, ph=0.0, penguin=False):
    hop = abs(math.sin(T * 2.4 + ph)) * 10 * U
    y -= hop
    if penguin:
        ctx.new_path(); ellipse(ctx, x, y, 0.55 * s, 0.95 * s); rgba(ctx, (0.08, 0.09, 0.12), 1); ctx.fill()
        ctx.new_path(); ellipse(ctx, x, y + 0.15 * s, 0.38 * s, 0.72 * s); rgba(ctx, (0.97, 0.97, 0.97), 1); ctx.fill()
        for sx in (-1, 1):
            ctx.new_path(); ellipse(ctx, x + sx * 0.5 * s, y + 0.1 * s, 0.13 * s, 0.5 * s, sx * 0.3); rgba(ctx, (0.08, 0.09, 0.12), 1); ctx.fill()
        for sx in (-1, 1):
            circle(ctx, x + sx * 0.14 * s, y - 0.55 * s, 0.07 * s, WHITE, 1); circle(ctx, x + sx * 0.14 * s, y - 0.55 * s, 0.04 * s, DARK, 1)
        ctx.new_path(); ctx.move_to(x - 0.1 * s, y - 0.42 * s); ctx.line_to(x + 0.1 * s, y - 0.42 * s); ctx.line_to(x, y - 0.28 * s); ctx.close_path(); rgba(ctx, beak, 1); ctx.fill()
        for sx in (-1, 1): ellipse(ctx, x + sx * 0.2 * s, y + 0.95 * s, 0.18 * s, 0.07 * s); rgba(ctx, beak, 1); ctx.fill()
        return
    for sx in (-1, 1):
        ctx.new_path(); ctx.move_to(x + sx * 0.18 * s, y + 0.6 * s); ctx.line_to(x + sx * 0.18 * s, y + 0.95 * s); ctx.set_line_width(0.07 * s); rgba(ctx, (0.85, 0.45, 0.35), 1); ctx.stroke()
    ctx.new_path(); ctx.move_to(x + 0.55 * s, y + 0.15 * s); ctx.line_to(x + 1.05 * s, y + 0.45 * s); ctx.line_to(x + 0.95 * s, y + 0.10 * s); ctx.close_path(); rgba(ctx, body, 1); ctx.fill()
    ctx.new_path(); ellipse(ctx, x, y + 0.15 * s, 0.70 * s, 0.55 * s); rgba(ctx, body, 1); ctx.fill()
    ctx.new_path(); ellipse(ctx, x - 0.15 * s, y + 0.30 * s, 0.40 * s, 0.34 * s); rgba(ctx, belly, 1); ctx.fill()
    ctx.new_path(); ellipse(ctx, x + 0.18 * s, y + 0.12 * s, 0.38 * s, 0.26 * s, -0.3); rgba(ctx, mix(body, DARK, 0.25), 1); ctx.fill()
    circle(ctx, x - 0.45 * s, y - 0.38 * s, 0.38 * s, head, 1)
    circle(ctx, x - 0.55 * s, y - 0.45 * s, 0.10 * s, WHITE, 1); circle(ctx, x - 0.57 * s, y - 0.45 * s, 0.06 * s, DARK, 1)
    ctx.new_path(); ctx.move_to(x - 0.80 * s, y - 0.42 * s); ctx.line_to(x - 1.08 * s, y - 0.32 * s); ctx.line_to(x - 0.80 * s, y - 0.25 * s); ctx.close_path(); rgba(ctx, beak, 1); ctx.fill()

def ostrich(ctx, x, y, s, T, k=1.0):
    """Autruche (exception : elle fait pipi). (x, y) = centre du corps."""
    for sx, ph in ((-1, 0), (1, 1.5)):
        ctx.new_path(); ctx.move_to(x + sx * 0.25 * s, y + 0.4 * s); ctx.line_to(x + sx * 0.32 * s, y + 1.25 * s); ctx.line_to(x + sx * 0.25 * s, y + 2.0 * s)
        ctx.set_line_width(0.13 * s); ctx.set_line_cap(cairo.LINE_CAP_ROUND); rgba(ctx, (0.93, 0.62, 0.58), 1); ctx.stroke()
        ellipse(ctx, x + sx * 0.25 * s - 0.12 * s, y + 2.02 * s, 0.22 * s, 0.07 * s); rgba(ctx, (0.85, 0.52, 0.50), 1); ctx.fill()
    for j in range(5):   # plumes blanches de la queue
        ctx.new_path(); ellipse(ctx, x + 0.75 * s, y - 0.25 * s + j * 0.12 * s, 0.35 * s, 0.11 * s, -0.5 + j * 0.25); rgba(ctx, (0.97, 0.96, 0.92), 1); ctx.fill()
    ctx.new_path(); ellipse(ctx, x, y, 0.85 * s, 0.55 * s); rgba(ctx, (0.12, 0.10, 0.10), 1); ctx.fill()
    ctx.new_path(); ellipse(ctx, x + 0.1 * s, y - 0.05 * s, 0.55 * s, 0.30 * s, -0.2); rgba(ctx, (0.22, 0.19, 0.18), 1); ctx.fill()
    sw = math.sin(T * 1.8) * 0.06 * s
    ctx.new_path(); ctx.move_to(x - 0.55 * s, y - 0.25 * s); ctx.curve_to(x - 0.75 * s, y - 0.9 * s, x - 0.45 * s + sw, y - 1.5 * s, x - 0.55 * s + sw, y - 1.95 * s)
    ctx.set_line_width(0.16 * s); ctx.set_line_cap(cairo.LINE_CAP_ROUND); rgba(ctx, (0.93, 0.70, 0.66), 1); ctx.stroke()
    hx, hy = x - 0.55 * s + sw, y - 2.0 * s
    circle(ctx, hx, hy, 0.17 * s, (0.88, 0.72, 0.68), 1)
    circle(ctx, hx - 0.06 * s, hy - 0.03 * s, 0.07 * s, WHITE, 1); circle(ctx, hx - 0.07 * s, hy - 0.03 * s, 0.045 * s, DARK, 1)
    ctx.new_path(); ctx.move_to(hx - 0.13 * s, hy + 0.02 * s); ctx.line_to(hx - 0.42 * s, hy + 0.06 * s); ctx.line_to(hx - 0.13 * s, hy + 0.10 * s); ctx.close_path(); rgba(ctx, (0.80, 0.62, 0.48), 1); ctx.fill()

def birds_scene(ctx, T, k_x, k_o):
    vgrad(ctx, (0.55, 0.80, 0.98), (0.88, 0.95, 1.0), 0, H)
    for (cx_, cy_, r) in ((0.2, 0.10, 90), (0.75, 0.07, 120), (0.55, 0.16, 70)):
        xx = (cx_ * W + T * 25 * U) % (W * 1.2) - W * 0.1
        for d in (-1, 0, 1): circle(ctx, xx + d * r * 0.8 * U, H * cy_ + abs(d) * 18 * U, r * U * (0.8 if d else 1), WHITE, 0.9)
    ctx.rectangle(0, H * 0.555, W, H); g = cairo.LinearGradient(0, H * 0.555, 0, H); g.add_color_stop_rgb(0, 0.55, 0.72, 0.35); g.add_color_stop_rgb(1, 0.36, 0.52, 0.22); ctx.set_source(g); ctx.fill()
    birds = [(0.11, (0.55, 0.58, 0.66), (0.70, 0.72, 0.78), (0.45, 0.50, 0.62), False),       # pigeon
             (0.30, (0.20, 0.70, 0.35), (0.95, 0.85, 0.25), (0.90, 0.25, 0.20), False),       # perroquet
             (0.49, (0.50, 0.33, 0.22), (0.95, 0.55, 0.25), (0.45, 0.30, 0.20), False),       # rouge-gorge
             (0.66, None, None, None, True)]                                                   # manchot
    for i, (bx, body, belly, head, peng) in enumerate(birds):
        y = H * 0.48
        if peng: small_bird(ctx, W * bx, y - 14 * U, 140 * U, None, None, None, T=T, ph=i, penguin=True)
        else: small_bird(ctx, W * bx, y, 132 * U, body, belly, head, T=T, ph=i)
        kk = prog(T, k_x + i * 0.12, k_x + i * 0.12 + 0.25)
        if kk > 0:
            ctx.save(); ctx.translate(W * bx, H * 0.33); ctx.scale(ease(kk), ease(kk))
            drop(ctx, 0, 0, 34 * U, (0.98, 0.88, 0.25)); no_sign(ctx, 0, 0, 58 * U); ctx.restore()
    # autruche (exception)
    ox, oy = W * 0.84, H * 0.405
    if k_o > 0: glow(ctx, ox, oy, W * 0.35, GOLD, 0.45 * k_o)
    ostrich(ctx, ox, oy, 118 * U, T)
    if k_o > 0:
        ctx.save(); ctx.translate(ox - 30 * U, H * 0.165); ctx.scale(ease(k_o), ease(k_o))
        drop(ctx, 0, 0, 34 * U, (0.98, 0.88, 0.25))
        ctx.new_path(); ctx.move_to(-22 * U, 52 * U); ctx.line_to(-6 * U, 70 * U); ctx.line_to(26 * U, 36 * U); ctx.set_line_width(12 * U); ctx.set_line_cap(cairo.LINE_CAP_ROUND); rgba(ctx, (0.15, 0.75, 0.30), 1); ctx.stroke()
        ctx.restore()
        pill(ctx, "OSTRICH", W * 0.70, H * 0.635, GOLD, 52, 1.0, k_o)

# ---------------------------------------------------------------- la fiente sur la voiture (C)
_RS = random.Random(9)
SPLAT_W = [(_RS.uniform(0, 2 * math.pi), _RS.uniform(0.75, 1.25)) for _ in range(14)]
def car_bg(ctx, T):
    vgrad(ctx, (0.55, 0.78, 0.97), (0.85, 0.93, 1.0), 0, H * 0.38)
    # pare-brise
    ctx.new_path(); ctx.move_to(W * 0.08, H * 0.40); ctx.line_to(W * 0.22, H * 0.10); ctx.line_to(W * 0.78, H * 0.10); ctx.line_to(W * 0.92, H * 0.40); ctx.close_path()
    g = cairo.LinearGradient(0, H * 0.10, 0, H * 0.40); g.add_color_stop_rgb(0, 0.30, 0.45, 0.62); g.add_color_stop_rgb(1, 0.14, 0.22, 0.34); ctx.set_source(g); ctx.fill()
    ctx.new_path(); ctx.move_to(W * 0.30, H * 0.12); ctx.line_to(W * 0.42, H * 0.12); ctx.line_to(W * 0.26, H * 0.38); ctx.line_to(W * 0.16, H * 0.38); ctx.close_path(); rgba(ctx, WHITE, 0.18); ctx.fill()
    # capot
    ctx.new_path(); ctx.move_to(W * 0.0, H * 0.42); ctx.line_to(W * 1.0, H * 0.42); ctx.line_to(W * 1.0, H); ctx.line_to(0, H); ctx.close_path()
    g = cairo.LinearGradient(0, H * 0.42, 0, H); g.add_color_stop_rgb(0, 0.92, 0.22, 0.24); g.add_color_stop_rgb(0.5, 0.75, 0.10, 0.14); g.add_color_stop_rgb(1, 0.45, 0.04, 0.08); ctx.set_source(g); ctx.fill()
    ctx.rectangle(0, H * 0.40, W, H * 0.025); rgba(ctx, (0.12, 0.12, 0.14), 1); ctx.fill()
    for (x0, x1) in ((0.15, 0.45), (0.55, 0.85)):   # essuie-glaces
        ctx.new_path(); ctx.move_to(W * x0, H * 0.405); ctx.line_to(W * x1, H * 0.36); ctx.set_line_width(10 * U); rgba(ctx, (0.08, 0.08, 0.09), 1); ctx.stroke()
    ctx.new_path(); ctx.move_to(W * 0.05, H * 0.47); ctx.curve_to(W * 0.4, H * 0.45, W * 0.6, H * 0.45, W * 0.95, H * 0.47); ctx.set_line_width(14 * U); rgba(ctx, WHITE, 0.22); ctx.stroke()

def car_scene(ctx, T, k_splat, k_lab):
    car_bg(ctx, T)
    # la fiente
    sx, sy = W * 0.48, H * 0.56
    if k_splat > 0:
        sc = 0.3 + 0.7 * ease(k_splat)
        ctx.save(); ctx.translate(sx, sy); ctx.scale(sc, sc * 0.75)
        ctx.new_path()
        for j in range(73):
            th = j / 72 * 2 * math.pi
            rr = 230 * U * (1 + 0.16 * math.sin(3 * th + 0.7) + 0.09 * math.sin(5 * th + 2.1) + 0.05 * math.sin(9 * th))
            (ctx.line_to if j else ctx.move_to)(math.cos(th) * rr, math.sin(th) * rr)
        ctx.close_path(); rgba(ctx, (0.97, 0.97, 0.94), 1); ctx.fill()
        for (a_, r_) in SPLAT_W[:7]:
            circle(ctx, math.cos(a_) * 300 * U * r_, math.sin(a_) * 300 * U * r_, 22 * U * r_, (0.97, 0.97, 0.94), 1)
        ctx.new_path(); ellipse(ctx, 25 * U, 10 * U, 95 * U, 75 * U, 0.4); rgba(ctx, (0.25, 0.28, 0.16), 1); ctx.fill()
        ctx.new_path(); ellipse(ctx, -40 * U, -30 * U, 45 * U, 35 * U); rgba(ctx, (0.32, 0.34, 0.20), 1); ctx.fill()
        ctx.restore()
        if k_splat < 1: glow(ctx, sx, sy, 260 * U, WHITE, 0.35 * (1 - k_splat))
    if k_lab > 0:
        leader(ctx, W * 0.17, H * 0.475, sx - 150 * U, sy - 20 * U, WHITE, 1.0, k_lab)
        pill(ctx, "PEE", W * 0.17, H * 0.465, WHITE, 64, 1.0, k_lab)
        kp = prog(T, WT("pee", 0) + 0.25, WT("pee", 0) + 0.6)
        leader(ctx, W * 0.80, H * 0.475, sx + 40 * U, sy + 5 * U, (0.55, 0.60, 0.30), 1.0, kp)
        pill(ctx, "POOP", W * 0.80, H * 0.465, (0.45, 0.50, 0.25), 52, 1.0, kp, fg=WHITE)

# ---------------------------------------------------------------- schéma : une seule sortie (D)
def _bird_outline(ctx, x, y, s):
    ctx.new_path(); ctx.move_to(x - 1.25 * s, y - 0.55 * s)
    ctx.curve_to(x - 1.0 * s, y - 1.05 * s, x - 0.45 * s, y - 1.0 * s, x - 0.35 * s, y - 0.55 * s)
    ctx.curve_to(x + 0.3 * s, y - 0.65 * s, x + 0.9 * s, y - 0.45 * s, x + 1.35 * s, y - 0.10 * s)
    ctx.line_to(x + 1.9 * s, y + 0.05 * s); ctx.line_to(x + 1.35 * s, y + 0.30 * s)
    ctx.curve_to(x + 0.8 * s, y + 0.75 * s, x - 0.2 * s, y + 0.85 * s, x - 0.6 * s, y + 0.35 * s)
    ctx.curve_to(x - 0.95 * s, y + 0.05 * s, x - 1.15 * s, y - 0.20 * s, x - 1.25 * s, y - 0.55 * s); ctx.close_path()

def _path_pts(pts, u):
    seg = [(math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1])) for i in range(len(pts) - 1)]
    tot = sum(seg); d = u * tot
    for i, L in enumerate(seg):
        if d <= L: k = d / max(L, 1e-6); return pts[i][0] + (pts[i + 1][0] - pts[i][0]) * k, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * k
        d -= L
    return pts[-1]

def inside_scene(ctx, T, k_kid, k_uric, k_flow, k_exit):
    vgrad(ctx, (0.06, 0.09, 0.22), (0.02, 0.03, 0.10))
    glow(ctx, W * 0.5, H * 0.40, W * 0.7, (0.25, 0.45, 1.0), 0.20)
    x, y, s = W * 0.43, H * 0.40, W * 0.30
    for dx in (-0.05, 0.25):   # pattes
        ctx.new_path(); ctx.move_to(x + dx * s, y + 0.70 * s); ctx.line_to(x + dx * s - 0.05 * s, y + 1.10 * s); ctx.line_to(x + dx * s - 0.25 * s, y + 1.14 * s)
        ctx.set_line_width(9 * U); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_join(cairo.LINE_JOIN_ROUND); rgba(ctx, (0.75, 0.85, 1.0), 0.9); ctx.stroke()
    _bird_outline(ctx, x, y, s); rgba(ctx, (0.55, 0.65, 0.85), 0.22); ctx.fill_preserve(); ctx.set_line_width(7 * U); rgba(ctx, (0.75, 0.85, 1.0), 0.9); ctx.stroke()
    ctx.new_path(); ctx.move_to(x - 0.30 * s, y - 0.45 * s); ctx.curve_to(x + 0.30 * s, y - 0.55 * s, x + 0.95 * s, y - 0.35 * s, x + 1.45 * s, y - 0.05 * s)
    ctx.curve_to(x + 0.85 * s, y - 0.10 * s, x + 0.20 * s, y - 0.20 * s, x - 0.30 * s, y - 0.45 * s); ctx.close_path()
    rgba(ctx, (0.75, 0.85, 1.0), 0.18); ctx.fill_preserve(); ctx.set_line_width(4 * U); rgba(ctx, (0.75, 0.85, 1.0), 0.55); ctx.stroke()
    for k in (0.0, 0.10, 0.20):   # plumes de la queue
        ctx.new_path(); ctx.move_to(x + 1.35 * s, y + (0.0 + k) * s); ctx.line_to(x + 1.85 * s, y + (-0.05 + k * 1.4) * s); ctx.set_line_width(5 * U); rgba(ctx, (0.75, 0.85, 1.0), 0.55); ctx.stroke()
    circle(ctx, x - 0.82 * s, y - 0.70 * s, 0.07 * s, (0.75, 0.85, 1.0), 0.9)
    ctx.new_path(); ctx.move_to(x - 1.22 * s, y - 0.62 * s); ctx.line_to(x - 1.55 * s, y - 0.50 * s); ctx.line_to(x - 1.20 * s, y - 0.44 * s); ctx.close_path(); rgba(ctx, (0.98, 0.78, 0.30), 1); ctx.fill()
    cl = (x + 1.30 * s, y + 0.30 * s)                      # cloaque : une seule sortie
    # intestin (brun)
    gut = [(x - 0.30 * s, y - 0.05 * s), (x + 0.10 * s, y + 0.20 * s), (x - 0.10 * s, y + 0.42 * s), (x + 0.35 * s, y + 0.45 * s), (x + 0.75 * s, y + 0.35 * s), cl]
    ctx.new_path(); ctx.move_to(*gut[0])
    for p in gut[1:]: ctx.line_to(*p)
    ctx.set_line_width(26 * U); ctx.set_line_join(cairo.LINE_JOIN_ROUND); ctx.set_line_cap(cairo.LINE_CAP_ROUND); rgba(ctx, (0.55, 0.38, 0.22), 0.9); ctx.stroke()
    # reins (rouge sombre) + uretères (blancs)
    kid = [(x + 0.35 * s, y - 0.30 * s), (x + 0.62 * s, y - 0.22 * s)]
    ure = [(x + 0.50 * s, y - 0.20 * s), (x + 0.95 * s, y + 0.05 * s), cl]
    if k_kid > 0:
        for (kx, ky) in kid:
            ctx.save(); ctx.translate(kx, ky); ctx.scale(ease(k_kid), ease(k_kid)); ellipse(ctx, 0, 0, 0.16 * s, 0.09 * s, 0.3)
            rgba(ctx, (0.75, 0.15, 0.22), 1); ctx.fill(); ctx.restore()
        ctx.new_path(); ctx.move_to(*ure[0])
        for p in ure[1:]: ctx.line_to(*p)
        ctx.set_line_width(12 * U); rgba(ctx, (0.95, 0.95, 0.92), 0.85 * k_kid); ctx.stroke()
        pill(ctx, "KIDNEYS", x + 0.50 * s, y - 0.62 * s, (0.95, 0.45, 0.50), 42, 1.0, k_kid)
    if k_flow > 0:
        for j in range(6):
            u = ((T * 0.6 + j / 6) % 1.0)
            px, py = _path_pts(ure, u); circle(ctx, px, py, 13 * U, WHITE, k_flow)
            px, py = _path_pts(gut, u); circle(ctx, px, py, 15 * U, (0.35, 0.24, 0.12), k_flow)
    if k_uric > 0:
        pill(ctx, "URIC ACID", W * 0.50, H * 0.155, WHITE, 60, 1.0, k_uric)
    if k_exit > 0:
        glow(ctx, cl[0], cl[1], 110 * U, GOLD, 0.6 * k_exit)
        leader(ctx, W * 0.50, H * 0.575, cl[0] - 12 * U, cl[1] + 8 * U, GOLD, 1.0, k_exit)
        pill(ctx, "ONE EXIT", W * 0.45, H * 0.585, GOLD, 56, 1.0, k_exit)
        fy = cl[1] + (T * 260 * U) % (H * 0.18)
        circle(ctx, cl[0] + 10 * U, fy, 26 * U, WHITE, k_exit); circle(ctx, cl[0] + 14 * U, fy + 6 * U, 13 * U, (0.30, 0.32, 0.18), k_exit)
    tag(ctx, "Simplified illustration", 0.083)

# ---------------------------------------------------------------- en vol (E)
def flying_bird(ctx, x, y, s, T):
    """Pigeon en vol de profil (tourné vers la gauche) ; ailes qui battent (aile du fond, corps, aile de devant)."""
    flap = 0.5 + 0.5 * math.sin(T * 7.0)          # 0 = aile basse, 1 = aile haute (surtout vers le haut)
    def wing(front):
        tipx, tipy = x + 0.30 * s, y + 0.25 * s - (1.10 if front else 0.90) * s * flap
        ctx.new_path(); ctx.move_to(x - 0.22 * s, y - 0.06 * s)
        ctx.curve_to(x - 0.15 * s, y + (tipy - y) * 0.55, tipx - 0.30 * s, tipy + 0.08 * s, tipx, tipy)
        ctx.curve_to(tipx - 0.05 * s, tipy + 0.30 * s, x + 0.30 * s, y + (tipy - y) * 0.25, x + 0.28 * s, y + 0.0 * s); ctx.close_path()
        rgba(ctx, (0.62, 0.65, 0.74) if front else (0.44, 0.46, 0.56), 1); ctx.fill_preserve(); ctx.set_line_width(4 * U); rgba(ctx, (0.25, 0.26, 0.32), 0.8); ctx.stroke()
        for k in (0.35, 0.55, 0.75):   # rémiges
            ctx.new_path(); ctx.move_to(x + (0.05 + 0.1 * k) * s, y + (tipy - y) * k * 0.6); ctx.line_to(tipx + (k - 0.5) * 0.3 * s, tipy + (y - tipy) * 0.15)
            ctx.set_line_width(3 * U); rgba(ctx, (0.25, 0.26, 0.32), 0.45); ctx.stroke()
    wing(False)
    ctx.new_path(); ctx.move_to(x + 0.55 * s, y + 0.02 * s); ctx.line_to(x + 1.05 * s, y - 0.12 * s); ctx.line_to(x + 1.05 * s, y + 0.20 * s); ctx.close_path(); rgba(ctx, (0.40, 0.42, 0.50), 1); ctx.fill()
    ctx.new_path(); ellipse(ctx, x + 0.15 * s, y + 0.05 * s, 0.58 * s, 0.23 * s); rgba(ctx, (0.62, 0.65, 0.74), 1); ctx.fill_preserve(); ctx.set_line_width(4 * U); rgba(ctx, (0.25, 0.26, 0.32), 0.8); ctx.stroke()
    circle(ctx, x - 0.40 * s, y - 0.06 * s, 0.20 * s, (0.50, 0.54, 0.66), 1)
    circle(ctx, x - 0.47 * s, y - 0.10 * s, 0.055 * s, (0.95, 0.55, 0.15), 1); circle(ctx, x - 0.47 * s, y - 0.10 * s, 0.03 * s, DARK, 1)
    ctx.new_path(); ctx.move_to(x - 0.57 * s, y - 0.06 * s); ctx.line_to(x - 0.76 * s, y + 0.0 * s); ctx.line_to(x - 0.57 * s, y + 0.04 * s); ctx.close_path(); rgba(ctx, (0.25, 0.22, 0.25), 1); ctx.fill()
    wing(True)

def fly_scene(ctx, T, k_w, k_b):
    vgrad(ctx, (0.35, 0.65, 0.98), (0.80, 0.92, 1.0), 0, H)
    for (cx_, cy_, r, sp) in ((0.1, 0.55, 110, 120), (0.6, 0.62, 140, 90), (0.3, 0.70, 90, 150), (0.85, 0.50, 100, 110)):
        xx = W * 1.2 - ((cx_ * W + T * sp * U) % (W * 1.4))
        for d in (-1, 0, 1): circle(ctx, xx + d * r * 0.8 * U, H * cy_ + abs(d) * 20 * U, r * U * (0.8 if d else 1), WHITE, 0.95)
    flying_bird(ctx, W * 0.42, H * 0.40 + 25 * U * math.sin(T * 2.0), W * 0.44, T)
    if k_w > 0:
        ctx.save(); ctx.translate(W * 0.24, H * 0.155); ctx.scale(ease(k_w), ease(k_w))
        circle(ctx, 0, 0, 80 * U, WHITE, 0.9); drop(ctx, 0, 6 * U, 40 * U, (0.10, 0.45, 0.85)); no_sign(ctx, 0, 0, 78 * U); ctx.restore()
        pill(ctx, "NO WATER WASTED", W * 0.62, H * 0.155, (0.10, 0.45, 0.85), 46, 1.0, k_w, fg=WHITE)
    if k_b > 0:
        pill(ctx, "NO BLADDER", W * 0.47, H * 0.60, GOLD, 60, 1.0, k_b)

# ---------------------------------------------------------------- dans l'œuf (F)
_RE = random.Random(23)
CRYST = [(_RE.uniform(-1, 1), _RE.uniform(-1, 1), _RE.uniform(0.6, 1.2), _RE.uniform(0, 1)) for _ in range(60)]
def egg_scene(ctx, T, k_cut, k_cr):
    vgrad(ctx, (0.98, 0.84, 0.60), (0.85, 0.62, 0.35), 0, H)
    ex, ey, rx, ry = W * 0.47, H * 0.40, W * 0.36, H * 0.25
    for j in range(60):   # nid de paille
        a = j / 60 * math.pi * 2
        ctx.new_path(); ctx.move_to(ex + math.cos(a) * rx * 1.15, ey + ry * 0.85 + math.sin(a) * 60 * U)
        ctx.line_to(ex + math.cos(a + 0.5) * rx * 1.25, ey + ry * 0.9 + math.sin(a + 0.5) * 70 * U)
        ctx.set_line_width(9 * U); rgba(ctx, (0.80, 0.60, 0.25) if j % 2 else (0.65, 0.45, 0.18), 1); ctx.stroke()
    ctx.new_path(); ellipse(ctx, ex, ey, rx, ry)
    g = cairo.RadialGradient(ex - rx * 0.3, ey - ry * 0.4, rx * 0.1, ex, ey, ry)
    g.add_color_stop_rgb(0, 1.0, 0.98, 0.93); g.add_color_stop_rgb(1, 0.90, 0.85, 0.76); ctx.set_source(g); ctx.fill()
    if k_cut > 0:   # coupe de l'œuf : l'intérieur apparaît
        ctx.save(); ctx.new_path(); ellipse(ctx, ex, ey, rx * 0.90, ry * 0.92); ctx.clip()
        rgba(ctx, (1.0, 0.95, 0.80), k_cut); ctx.paint()
        circle(ctx, ex + rx * 0.25, ey + ry * 0.30, rx * 0.36, (1.0, 0.78, 0.20), k_cut)          # jaune
        # poussin (embryon recroquevillé)
        ctx.new_path(); ellipse(ctx, ex - rx * 0.15, ey - ry * 0.05, rx * 0.42, ry * 0.36, -0.4); rgba(ctx, (0.98, 0.72, 0.62), k_cut); ctx.fill()
        circle(ctx, ex - rx * 0.38, ey - ry * 0.25, rx * 0.20, (0.98, 0.72, 0.62), k_cut)
        circle(ctx, ex - rx * 0.43, ey - ry * 0.28, rx * 0.06, (0.10, 0.08, 0.12), k_cut)
        ctx.new_path(); ctx.move_to(ex - rx * 0.55, ey - ry * 0.20); ctx.line_to(ex - rx * 0.64, ey - ry * 0.14); ctx.line_to(ex - rx * 0.54, ey - ry * 0.10); ctx.close_path(); rgba(ctx, (0.95, 0.70, 0.25), k_cut); ctx.fill()
        # sac à déchets (allantoïde) + cristaux
        sx_, sy_, sr = ex + rx * 0.38, ey - ry * 0.40, rx * 0.30
        circle(ctx, sx_, sy_, sr, (0.35, 0.50, 0.75), 0.85 * k_cut)
        ctx.new_path(); ctx.arc(sx_, sy_, sr, 0, 2 * math.pi); ctx.set_line_width(7 * U); rgba(ctx, (0.20, 0.30, 0.55), 0.9 * k_cut); ctx.stroke()
        nshow = int(len(CRYST) * k_cr)
        for (cx_, cy_, cs, ph) in CRYST[:nshow]:
            if cx_ * cx_ + cy_ * cy_ > 0.8: continue
            px, py, r = sx_ + cx_ * sr * 0.85, sy_ + cy_ * sr * 0.85, 17 * U * cs
            tw = 0.6 + 0.4 * math.sin(T * 6 + ph * 6)
            ctx.new_path(); ctx.move_to(px, py - r); ctx.line_to(px + r * 0.7, py); ctx.line_to(px, py + r); ctx.line_to(px - r * 0.7, py); ctx.close_path()
            rgba(ctx, WHITE, tw); ctx.fill()
        ctx.restore()
        ctx.new_path(); ellipse(ctx, ex, ey, rx * 0.90, ry * 0.92); ctx.set_line_width(10 * U); rgba(ctx, (0.85, 0.78, 0.66), k_cut); ctx.stroke()
        if k_cr > 0.2:
            leader(ctx, W * 0.62, H * 0.155, ex + rx * 0.38, ey - ry * 0.40 - rx * 0.30, GOLD, 1.0, prog(k_cr, 0.2, 0.6))
            pill(ctx, "SOLID CRYSTALS", W * 0.55, H * 0.150, GOLD, 52, 1.0, prog(k_cr, 0.2, 0.6))
    tag(ctx, "Simplified illustration", 0.083)

# ---------------------------------------------------------------- montage
T_B0 = SENT("none") - 0.08
T_C0 = SENT("car") - 0.08
T_D0 = SENT("inside") - 0.08
T_E0 = SENT("fly") - 0.08
T_F0 = SENT("egg") - 0.08
T_G0 = SENT("close") - 0.08
T_H0 = SENT("close", 1) - 0.08
T_CTA = END_T - 2.4

def master(ctx, T):
    if T < T_B0:                                         # A — le pigeon sur la voiture (image 1)
        pigeon_scene(ctx, T)
        if T > 1.2: tag(ctx, "Illustration", 0.250)
    elif T < T_C0:                                       # B — presque aucun oiseau… sauf l'autruche
        birds_scene(ctx, T, T_B0 + 0.1, prog(T, WT("ostrich") - 0.35, WT("ostrich") + 0.05))
        tag(ctx, "Illustration", 0.083)
    elif T < T_D0:                                       # C — la fiente sur la voiture
        car_scene(ctx, T, prog(T, T_C0 + 0.05, T_C0 + 0.35), prog(T, WT("white", 0) - 0.15, WT("white", 0) + 0.25))
        tag(ctx, "Illustration", 0.083)
    elif T < T_E0:                                       # D — acide urique, une seule sortie (schéma)
        inside_scene(ctx, T, prog(T, T_D0 + 0.05, T_D0 + 0.5), prog(T, WT("uric") - 0.15, WT("uric") + 0.25),
                     prog(T, WT("paste") - 0.2, WT("paste") + 0.3), prog(T, WT("exit") - 0.35, WT("exit") + 0.05))
    elif T < T_F0:                                       # E — pas d'eau perdue, pas de vessie en vol
        fly_scene(ctx, T, prog(T, WT("water") - 0.15, WT("water") + 0.2), prog(T, WT("bladder") - 0.2, WT("bladder") + 0.15))
        tag(ctx, "Illustration", 0.083)
    elif T < T_G0:                                       # F — dans l'œuf : des cristaux solides
        egg_scene(ctx, T, prog(T, T_F0 + 0.05, T_F0 + 0.6), prog(T, WT("crystals") - 0.6, WT("crystals") + 0.6))
    elif T < T_H0:                                       # G — « that white splat on your car? Bird pee. »
        car_scene(ctx, T, 1.0, 0.0)
        pill(ctx, "BIRD PEE", W * 0.48, H * 0.62, WHITE, 76, 1.0, prog(T, WT("bird", 1) - 0.15, WT("bird", 1) + 0.2))
        tag(ctx, "Illustration", 0.083)
    else:                                                # H — retour au pigeon de l'image 1
        pigeon_scene(ctx, T, ("STILL", "NEVER PEED"), 1.0)
        tag(ctx, "Illustration", 0.250)
        kc = prog(T, T_CTA, T_CTA + 0.35)
        if kc > 0:
            font(ctx, 42 * U); txt = "FACTORA"; w_ = ctx.text_extents(txt).width + 56 * U
            rrect(ctx, W * 0.46 - w_ / 2, H * 0.265 - 31 * U, w_, 62 * U, 31 * U); rgba(ctx, (0, 0, 0), 0.45 * kc); ctx.fill()
            text(ctx, txt, W * 0.46, H * 0.265, 42 * U, GOLD, kc)
            cta_lines(ctx, ("Follow Factora for more", "weird animal facts."), W * 0.46, (H * 0.765, H * 0.797), 50, kc)

T_COVER = 0.6
def _abs_t(scene, t):
    if TNOW < 2.0 / FPS: return T_COVER
    return (0.0 if scene == _FIRST else _TL[scene]["start"]) + t
def _scene(name):
    def f(ctx, t, d): master(ctx, _abs_t(name, t))
    return f
SCENES = {sg["scene"]: _scene(sg["scene"]) for sg in _TLL}
SHORT_SCENES = [sg["scene"] for sg in _TLL]

def cover(ctx):
    """Affiche : le pigeon en grand sur le capot, « BIRDS / NEVER PEE », bandeau « SO WHERE DOES IT GO? » (sans la
    réponse) ; tout l'essentiel entre 14 % et 86 % de la hauteur."""
    car_bg(ctx, 1.0)
    pigeon(ctx, W * 0.455, H * 0.52, W * 0.37, 0.0)
    poster_text(ctx, "BIRDS", W * 0.47, H * 0.175, 175 * U, WHITE, W * 0.86)
    poster_text(ctx, "NEVER PEE", W * 0.47, H * 0.250, 175 * U, GOLD, W * 0.86)
    font(ctx, 62 * U); txt = "SO WHERE DOES IT GO?"; w_ = ctx.text_extents(txt).width + 80 * U; h_ = 116 * U; y_ = H * 0.815
    glow(ctx, W * 0.47, y_, w_ * 0.6, GOLD, 0.30)
    rrect(ctx, W * 0.47 - w_ / 2, y_ - h_ / 2, w_, h_, h_ / 2); rgba(ctx, GOLD, 0.97); ctx.fill()
    text(ctx, txt, W * 0.47, y_, 62 * U, DARK)
