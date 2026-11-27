exec(open("engine/photo.py", encoding="utf-8").read())   # poster_text, label (aucune image extérieure)
# Épisode 053 (vidéo longue 16:9, ≈ 11 min 35) — pourquoi certains ne s'endorment qu'avec la télé allumée.
# Sujet proposé par Nazik (2026-11-27) d'après une vidéo française d'une autre chaîne : rien n'en est repris (vidéo non vue,
# ni traduite) ; script, structure, chapitres et dessins 100 % Factora, faits vérifiés (sources dans meta_en.json).
# Voix : Matilda via Runway, découpée en phrases par align_voice.py (horodatage whisper.cpp) ; WT() = instant estimé d'un mot.
import json as _json, re as _re

_TLL = _json.load(open(EP + "/build/timeline.json", encoding="utf-8"))
_TL = {sg["scene"]: sg for sg in _TLL}
_WORDS = {}
for sg in _TLL:
    L = []
    for se in sg["sents"]:
        txt = se["text"]; n = max(1, len(txt))
        for m in _re.finditer(r"\S+", txt):
            L.append((m.group().lower().strip(".,?!:;'\"…"), se["start"] - sg["start"] + (se["end"] - se["start"]) * m.start() / n))
    _WORDS[sg["scene"]] = L
def ST(sc, k=0):
    s = _TL[sc]; k = min(k, len(s["sents"]) - 1); return s["sents"][k]["start"] - s["start"]
def WT(sc, word, n=0):
    hits = [t for w, t in _WORDS[sc] if w == word.lower()]
    return hits[n] if n < len(hits) else 1e9

DARK = (0.03, 0.02, 0.08)
TVB = (0.45, 0.78, 1.0)          # lueur bleutée de l'écran
SKIN = (0.95, 0.78, 0.64)
def pk(t, a, dur=0.5): return prog(t, a, a + dur)

# ---------------------------------------------------------------- textes
def pill(ctx, s, x, y, col, size=44, k=1.0, fg=DARK):
    if k <= 0: return
    sc_ = 0.6 + 0.4 * ease(k) + 0.08 * math.sin(math.pi * clamp(k))
    ctx.save(); ctx.translate(x, y); ctx.scale(sc_, sc_)
    font(ctx, size * U); w_ = ctx.text_extents(s).width + 56 * U; h_ = size * 1.6 * U
    glow(ctx, 0, 0, w_ * 0.7, col, 0.30 * k)
    rrect(ctx, -w_ / 2, -h_ / 2, w_, h_, h_ / 2); rgba(ctx, col, 0.97 * k); ctx.fill()
    text(ctx, s, 0, 0, size * U, fg, k)
    ctx.restore()

def big(ctx, s, x, y, size, col, k=1.0, maxw=None):
    if k <= 0: return
    ctx.save(); ctx.push_group()
    sc_ = 0.85 + 0.15 * ease(k); ctx.translate(x, y); ctx.scale(sc_, sc_); ctx.translate(-x, -y)
    poster_text(ctx, s, x, y, size * U, col, maxw or W * 0.9)
    ctx.pop_group_to_source(); ctx.paint_with_alpha(ease(k)); ctx.restore()

def kicker(ctx, s, k=1.0, y=0.075, col=(0.80, 0.85, 1.0)):
    if k <= 0: return
    font(ctx, 30 * U); w_ = ctx.text_extents(s).width + 44 * U
    rrect(ctx, CX - w_ / 2, H * y - 26 * U, w_, 52 * U, 26 * U); rgba(ctx, (0, 0, 0), 0.45 * k); ctx.fill()
    text(ctx, s, CX, H * y, 30 * U, col, k)

def note(ctx, s, k=1.0, y=0.745, col=(0.85, 0.88, 1.0), size=32):
    if k > 0: text(ctx, s, CX, H * y, size * U, col, 0.9 * k)

def tag(ctx, s="Simplified illustration", a=1.0):
    font(ctx, 26 * U); w_ = ctx.text_extents(s).width + 34 * U
    rrect(ctx, 30 * U, 26 * U, w_, 44 * U, 22 * U); rgba(ctx, (0, 0, 0), 0.45 * a); ctx.fill()
    text(ctx, s, 30 * U + 17 * U, 48 * U, 26 * U, (0.9, 0.92, 1.0), 0.9 * a, align="l")

# ---------------------------------------------------------------- décor
def night_bg(ctx, t, tint=PURPLE, c1=(0.07, 0.08, 0.22), c2=(0.01, 0.02, 0.07)):
    vgrad(ctx, c1, c2)
    glow(ctx, W * (0.5 + 0.12 * math.sin(t * 0.25)), H * 0.40, W * 0.55, tint, 0.16)
    rnd = random.Random(53)
    for i in range(40):
        x, y = rnd.random() * W, rnd.random() * H * 0.8
        circle(ctx, x, y, rnd.uniform(1.5, 3.5) * U, WHITE, 0.25 + 0.25 * math.sin(t * 1.5 + i))

def ellipse(ctx, x, y, rx, ry, rot=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(max(rx, 0.01), max(ry, 0.01)); ctx.arc(0, 0, 1, 0, 2 * math.pi); ctx.restore()

def moon(ctx, x, y, r, a=1.0):
    glow(ctx, x, y, r * 2.4, (0.75, 0.75, 1.0), 0.35 * a)
    ctx.save(); ctx.push_group()
    circle(ctx, x, y, r, (1.0, 0.96, 0.78), 1)
    ctx.set_operator(cairo.OPERATOR_CLEAR); circle(ctx, x + r * 0.45, y - r * 0.25, r * 0.85, WHITE, 1)
    ctx.pop_group_to_source(); ctx.paint_with_alpha(a); ctx.restore()

def tv(ctx, x, y, w, t, on=1.0, content=None, flicker=True, stand=True):
    """Téléviseur centré en (x, y) (centre de l'écran), largeur w ; content(ctx, x0, y0, w, h, t) dessine l'image."""
    h = w * 0.58
    if stand:
        ctx.rectangle(x - w * 0.04, y + h / 2, w * 0.08, h * 0.16); rgba(ctx, (0.12, 0.12, 0.16), 1); ctx.fill()
        rrect(ctx, x - w * 0.22, y + h / 2 + h * 0.14, w * 0.44, h * 0.05, 6 * U); rgba(ctx, (0.12, 0.12, 0.16), 1); ctx.fill()
    if on > 0:
        f = 1.0 if not flicker else 0.82 + 0.18 * (0.5 + 0.5 * math.sin(t * 2.3) * math.sin(t * 0.9 + 1))
        glow(ctx, x, y, w * 0.9, TVB, 0.40 * on * f)
    rrect(ctx, x - w / 2 - 10 * U, y - h / 2 - 10 * U, w + 20 * U, h + 20 * U, 14 * U); rgba(ctx, (0.08, 0.08, 0.11), 1); ctx.fill()
    ctx.save(); rrect(ctx, x - w / 2, y - h / 2, w, h, 6 * U); ctx.clip()
    rgba(ctx, (0.02, 0.02, 0.04), 1); ctx.paint()
    if on > 0:
        ctx.push_group()
        g = cairo.LinearGradient(0, y - h / 2, 0, y + h / 2); g.add_color_stop_rgb(0, 0.30, 0.55, 0.95); g.add_color_stop_rgb(1, 0.12, 0.22, 0.55)
        ctx.set_source(g); ctx.paint()
        if content: content(ctx, x - w / 2, y - h / 2, w, h, t)
        ctx.pop_group_to_source(); ctx.paint_with_alpha(on)
        ctx.new_path(); ellipse(ctx, x - w * 0.25, y - h * 0.30, w * 0.25, h * 0.08, -0.2); rgba(ctx, WHITE, 0.07 * on); ctx.fill()
    ctx.restore()

def sitcom(ctx, x0, y0, w, h, t):
    """Image d'une série familière : un canapé et deux silhouettes (aucun personnage réel)."""
    ctx.rectangle(x0, y0 + h * 0.62, w, h * 0.38); rgba(ctx, (0.55, 0.35, 0.30), 1); ctx.fill()
    rrect(ctx, x0 + w * 0.15, y0 + h * 0.45, w * 0.70, h * 0.25, 10 * U); rgba(ctx, (0.85, 0.45, 0.35), 1); ctx.fill()
    for i, (px, col) in enumerate(((0.35, (1.0, 0.75, 0.30)), (0.65, (0.55, 0.85, 0.65)))):
        bob = 3 * U * math.sin(t * 3 + i * 2)
        circle(ctx, x0 + w * px, y0 + h * 0.30 + bob, h * 0.09, (0.98, 0.82, 0.68), 1)
        rrect(ctx, x0 + w * px - h * 0.11, y0 + h * 0.40 + bob, h * 0.22, h * 0.22, h * 0.06); rgba(ctx, col, 1); ctx.fill()

def bed(ctx, x, y, w, t, eyes=1.0, a=1.0, blanket=(0.32, 0.36, 0.72), face_light=0.0, zz=0.0):
    """Lit vu de côté (tête à gauche), (x, y) = centre du matelas, w = longueur ; eyes 1 = ouverts, 0 = fermés."""
    ctx.save(); ctx.push_group()
    h = w * 0.13
    rrect(ctx, x - w / 2 - w * 0.03, y - h * 2.6, w * 0.05, h * 3.8, 8 * U); rgba(ctx, (0.42, 0.28, 0.20), 1); ctx.fill()   # tête de lit
    rrect(ctx, x - w / 2, y + h * 0.3, w, h * 0.7, 8 * U); rgba(ctx, (0.40, 0.27, 0.19), 1); ctx.fill()                 # cadre
    rrect(ctx, x - w / 2, y - h * 0.4, w, h * 0.9, 14 * U); rgba(ctx, (0.92, 0.92, 0.96), 1); ctx.fill()                # matelas
    rrect(ctx, x - w * 0.47, y - h * 1.15, w * 0.20, h * 0.85, 30 * U); rgba(ctx, WHITE, 1); ctx.fill()                  # oreiller
    hx, hy, r = x - w * 0.36, y - h * 1.05, h * 0.62
    circle(ctx, hx, hy, r, SKIN, 1)
    ctx.new_path(); ctx.arc(hx - r * 0.05, hy - r * 0.10, r * 1.03, math.pi * 0.85, math.pi * 1.75); ctx.close_path(); rgba(ctx, (0.30, 0.20, 0.14), 1); ctx.fill()
    ex, ey = hx + r * 0.45, hy - r * 0.10
    if eyes > 0.5:
        circle(ctx, ex, ey, r * 0.14, DARK, 1); circle(ctx, ex + r * 0.04, ey - r * 0.04, r * 0.05, WHITE, 1)
    else:
        ctx.new_path(); ctx.arc(ex, ey - r * 0.05, r * 0.14, 0.15 * math.pi, 0.85 * math.pi); ctx.set_line_width(4 * U); rgba(ctx, DARK, 1); ctx.stroke()
    breath = 1 + 0.03 * math.sin(t * 1.6)
    ctx.new_path(); ctx.move_to(x - w * 0.30, y - h * 0.25)
    ctx.curve_to(x - w * 0.15, y - h * 1.6 * breath, x + w * 0.20, y - h * 1.3 * breath, x + w * 0.48, y - h * 0.5)
    ctx.line_to(x + w * 0.50, y + h * 0.45); ctx.line_to(x - w * 0.30, y + h * 0.45); ctx.close_path()
    g = cairo.LinearGradient(0, y - h * 1.6, 0, y + h * 0.5); g.add_color_stop_rgb(0, *mix(blanket, WHITE, 0.15)); g.add_color_stop_rgb(1, *mix(blanket, DARK, 0.3))
    ctx.set_source(g); ctx.fill()
    if face_light > 0: glow(ctx, hx, hy, r * 2.2, TVB, 0.35 * face_light)
    ctx.pop_group_to_source(); ctx.paint_with_alpha(a); ctx.restore()
    if zz > 0:
        for i in range(3):
            ph = (t * 0.4 + i / 3) % 1
            text(ctx, "Z", hx + r * 0.6 + ph * w * 0.12, hy - r - ph * h * 2.5, (26 + 34 * ph) * U, WHITE, zz * math.sin(math.pi * ph))
    return hx, hy, r

def light_cone(ctx, x0, y0, x1, y1, spread, col=TVB, a=0.25):
    if a <= 0: return
    dx, dy = x1 - x0, y1 - y0; L = math.hypot(dx, dy); nx, ny = -dy / L, dx / L
    ctx.new_path(); ctx.move_to(x0 + nx * spread * 0.15, y0 + ny * spread * 0.15); ctx.line_to(x1 + nx * spread, y1 + ny * spread)
    ctx.line_to(x1 - nx * spread, y1 - ny * spread); ctx.line_to(x0 - nx * spread * 0.15, y0 - ny * spread * 0.15); ctx.close_path()
    g = cairo.LinearGradient(x0, y0, x1, y1); g.add_color_stop_rgba(0, *col, a); g.add_color_stop_rgba(1, *col, 0); ctx.set_source(g); ctx.fill()

def bedroom(ctx, t, tv_on=1.0, eyes=1.0, zz=0.0, clock="12:00", content=sitcom, tv_x=0.76):
    vgrad(ctx, (0.09, 0.10, 0.24), (0.03, 0.03, 0.09))
    # fenêtre et lune
    rrect(ctx, W * 0.08, H * 0.10, W * 0.18, H * 0.26, 8 * U); rgba(ctx, (0.25, 0.22, 0.35), 1); ctx.fill()
    ctx.rectangle(W * 0.09, H * 0.12, W * 0.16, H * 0.22); rgba(ctx, (0.04, 0.05, 0.16), 1); ctx.fill()
    moon(ctx, W * 0.20, H * 0.18, 26 * U)
    ctx.rectangle(W * 0.17 - 3 * U, H * 0.12, 6 * U, H * 0.22); rgba(ctx, (0.25, 0.22, 0.35), 1); ctx.fill()
    # sol
    ctx.rectangle(0, H * 0.66, W, H * 0.34); rgba(ctx, (0.08, 0.07, 0.12), 1); ctx.fill()
    # commode + réveil
    rrect(ctx, W * (tv_x - 0.14), H * 0.52, W * 0.28, H * 0.15, 8 * U); rgba(ctx, (0.30, 0.22, 0.18), 1); ctx.fill()
    if clock:
        rrect(ctx, W * (tv_x + 0.07), H * 0.46, W * 0.07, H * 0.055, 8 * U); rgba(ctx, (0.05, 0.05, 0.08), 1); ctx.fill()
        text(ctx, clock, W * (tv_x + 0.105), H * 0.488, 30 * U, (1.0, 0.35, 0.35), 1)
    tv(ctx, W * tv_x, H * 0.35, W * 0.22, t, on=tv_on, content=content)
    light_cone(ctx, W * (tv_x - 0.08), H * 0.36, W * 0.28, H * 0.56, H * 0.16, a=0.20 * tv_on)
    return bed(ctx, W * 0.34, H * 0.60, W * 0.42, t, eyes=eyes, face_light=tv_on, zz=zz)

# ---------------------------------------------------------------- cerveau, bulles, icônes
def brain(ctx, x, y, s, t, hi=0.0, col=(0.96, 0.62, 0.74)):
    """Cerveau vu de profil (avant à gauche) ; hi > 0 : nœuds du réseau du mode par défaut qui s'allument."""
    lobes = ((-0.45, -0.05, 0.42), (-0.10, -0.32, 0.46), (0.32, -0.25, 0.44), (0.52, 0.05, 0.36), (0.10, 0.12, 0.44), (-0.30, 0.20, 0.34))
    for (dx, dy, r) in lobes: circle(ctx, x + dx * s, y + dy * s, r * s, mix(col, DARK, 0.25), 1)
    for (dx, dy, r) in lobes: circle(ctx, x + dx * s, y + dy * s, r * s * 0.94, col, 1)
    ctx.new_path(); ellipse(ctx, x + 0.48 * s, y + 0.42 * s, 0.28 * s, 0.17 * s); rgba(ctx, mix(col, DARK, 0.15), 1); ctx.fill()     # cervelet
    ctx.new_path(); ctx.move_to(x + 0.18 * s, y + 0.40 * s); ctx.line_to(x + 0.26 * s, y + 0.80 * s); ctx.set_line_width(0.14 * s); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    rgba(ctx, mix(col, DARK, 0.2), 1); ctx.stroke()
    rnd = random.Random(5)
    for i in range(16):   # circonvolutions
        cx_, cy_ = x + rnd.uniform(-0.75, 0.75) * s, y + rnd.uniform(-0.6, 0.35) * s
        ctx.new_path(); ctx.arc(cx_, cy_, rnd.uniform(0.08, 0.16) * s, rnd.uniform(0, 3), rnd.uniform(3.5, 6)); ctx.set_line_width(0.025 * s)
        rgba(ctx, mix(col, DARK, 0.35), 0.8); ctx.stroke()
    if hi > 0:
        nodes = ((-0.62, -0.05), (0.18, -0.12), (0.55, -0.30), (-0.05, 0.25))
        for i, (ax, ay) in enumerate(nodes):
            for (bx, by) in nodes[i + 1:]:
                ctx.new_path(); ctx.move_to(x + ax * s, y + ay * s); ctx.line_to(x + bx * s, y + by * s); ctx.set_line_width(0.02 * s); rgba(ctx, GOLD, 0.6 * hi); ctx.stroke()
        for i, (ax, ay) in enumerate(nodes):
            p = 0.75 + 0.25 * math.sin(t * 4 + i)
            glow(ctx, x + ax * s, y + ay * s, 0.30 * s, GOLD, 0.6 * hi * p); circle(ctx, x + ax * s, y + ay * s, 0.07 * s, (1.0, 0.9, 0.4), hi)

def bubble(ctx, x, y, r, k, icon=None, col=WHITE, tail=None):
    if k <= 0: return
    e = ease(k); ctx.save(); ctx.translate(x, y); ctx.scale(e, e)
    if tail:
        tx, ty = tail[0] - x, tail[1] - y
        for j, f in enumerate((0.55, 0.75, 0.9)): circle(ctx, tx * f, ty * f, r * (0.18 - j * 0.04), col, 0.9)
    circle(ctx, 0, 0, r, col, 0.95)
    if icon: icon(ctx, 0, 0, r * 0.62)
    ctx.restore()

def ic_text(s, col=DARK, size=None):
    def f(ctx, x, y, r): text(ctx, s, x, y, (size or r * 0.9), col, 1)
    return f
def ic_calendar(ctx, x, y, r):
    rrect(ctx, x - r, y - r * 0.8, 2 * r, 1.7 * r, r * 0.2); rgba(ctx, WHITE, 1); ctx.fill_preserve(); ctx.set_line_width(r * 0.1); rgba(ctx, DARK, 1); ctx.stroke()
    ctx.rectangle(x - r, y - r * 0.8, 2 * r, r * 0.5); rgba(ctx, CORAL, 1); ctx.fill()
    for i in range(3):
        for j in range(2): ctx.rectangle(x - r * 0.7 + i * r * 0.55, y - r * 0.05 + j * r * 0.45, r * 0.3, r * 0.25); rgba(ctx, DARK, 0.6); ctx.fill()
def ic_chat(ctx, x, y, r):
    rrect(ctx, x - r, y - r * 0.7, 2 * r, 1.2 * r, r * 0.4); rgba(ctx, CYAN, 1); ctx.fill()
    ctx.new_path(); ctx.move_to(x - r * 0.4, y + r * 0.45); ctx.line_to(x - r * 0.7, y + r * 0.9); ctx.line_to(x - r * 0.05, y + r * 0.45); ctx.close_path(); ctx.fill()
    for i in (-1, 0, 1): circle(ctx, x + i * r * 0.45, y - r * 0.1, r * 0.13, WHITE, 1)
def ic_lock(ctx, x, y, r):
    ctx.new_path(); ctx.arc(x, y - r * 0.2, r * 0.5, math.pi, 2 * math.pi); ctx.set_line_width(r * 0.22); rgba(ctx, (0.5, 0.5, 0.6), 1); ctx.stroke()
    rrect(ctx, x - r * 0.75, y - r * 0.2, r * 1.5, r * 1.1, r * 0.15); rgba(ctx, GOLD, 1); ctx.fill()
    text(ctx, "?", x, y + r * 0.35, r * 0.9, DARK, 1)
def ic_dollar(ctx, x, y, r):
    rrect(ctx, x - r, y - r * 0.6, 2 * r, 1.2 * r, r * 0.15); rgba(ctx, GREEN, 1); ctx.fill(); text(ctx, "$", x, y, r * 1.0, DARK, 1)
def ic_alert(ctx, x, y, r):
    ctx.new_path(); ctx.move_to(x, y - r); ctx.line_to(x + r, y + r * 0.8); ctx.line_to(x - r, y + r * 0.8); ctx.close_path(); rgba(ctx, CORAL, 1); ctx.fill()
    text(ctx, "!", x, y + r * 0.25, r * 1.1, WHITE, 1)

def pictogram(ctx, x, y, s, col, a=1.0):
    circle(ctx, x, y - s * 0.55, s * 0.22, col, a)
    rrect(ctx, x - s * 0.30, y - s * 0.28, s * 0.60, s * 0.70, s * 0.22); rgba(ctx, col, a); ctx.fill()

def heart(ctx, x, y, s, col=CORAL, a=1.0):
    ctx.new_path(); ctx.move_to(x, y + s * 0.9)
    ctx.curve_to(x - s * 1.4, y - s * 0.1, x - s * 0.9, y - s * 1.2, x, y - s * 0.45)
    ctx.curve_to(x + s * 0.9, y - s * 1.2, x + s * 1.4, y - s * 0.1, x, y + s * 0.9); ctx.close_path(); rgba(ctx, col, a); ctx.fill()

def arrow(ctx, x0, y0, x1, y1, col=WHITE, k=1.0, w=8):
    if k <= 0: return
    xe, ye = x0 + (x1 - x0) * ease(k), y0 + (y1 - y0) * ease(k)
    ctx.new_path(); ctx.move_to(x0, y0); ctx.line_to(xe, ye); ctx.set_line_width(w * U); ctx.set_line_cap(cairo.LINE_CAP_ROUND); rgba(ctx, col, 0.9); ctx.stroke()
    ang = math.atan2(ye - y0, xe - x0); hl = w * 3.2 * U
    ctx.new_path(); ctx.move_to(xe + math.cos(ang) * hl * 0.3, ye + math.sin(ang) * hl * 0.3)
    ctx.line_to(xe - math.cos(ang - 0.5) * hl, ye - math.sin(ang - 0.5) * hl); ctx.line_to(xe - math.cos(ang + 0.5) * hl, ye - math.sin(ang + 0.5) * hl); ctx.close_path(); ctx.fill()

def bar(ctx, x, ybot, w, hmax, frac, col, k, lab=None, val=None):
    rrect(ctx, x - w / 2, ybot - hmax, w, hmax, 12 * U); rgba(ctx, WHITE, 0.08); ctx.fill()
    h = hmax * frac * ease(k)
    if h > 2:
        rrect(ctx, x - w / 2, ybot - h, w, h, 12 * U)
        g = cairo.LinearGradient(0, ybot - h, 0, ybot); g.add_color_stop_rgb(0, *mix(col, WHITE, 0.25)); g.add_color_stop_rgb(1, *mix(col, DARK, 0.2)); ctx.set_source(g); ctx.fill()
    if val and k > 0: text(ctx, val, x, ybot - h - 34 * U, 44 * U, WHITE, ease(k))
    if lab: text(ctx, lab, x, ybot + 34 * U, 30 * U, (0.85, 0.88, 1.0), 0.95)

def wave(ctx, x0, x1, y, amp, t, spiky=False, col=CYAN, a=1.0, k=1.0):
    ctx.new_path(); n = 160
    for i in range(n + 1):
        f = i / n
        if f > k: break
        x = x0 + (x1 - x0) * f
        v = math.sin(f * 40 + t * 6) * 0.35 + math.sin(f * 17 - t * 3) * 0.25
        if spiky:
            for c_ in (0.18, 0.47, 0.78): v += 2.2 * math.exp(-((f - c_) / 0.015) ** 2) * math.sin(f * 300)
        (ctx.line_to if i else ctx.move_to)(x, y + amp * v)
    ctx.set_line_width(5 * U); ctx.set_line_join(cairo.LINE_JOIN_ROUND); rgba(ctx, col, a); ctx.stroke()

def chapter(ctx, t, d, n, title, col):
    night_bg(ctx, t, tint=col)
    k = pk(t, 0.0, 0.6)
    neon_text(ctx, f"PART {n}", CX, H * 0.34, 70 * U, col, k, WHITE, fill=0.2)
    big(ctx, title, CX, H * 0.50, 110, WHITE, pk(t, 0.25, 0.6))
    for i in range(4):
        circle(ctx, CX + (i - 1.5) * 46 * U, H * 0.64, 12 * U, col if i < n else WHITE, (0.9 if i < n else 0.25) * k)

# ================================================================ SCÈNES
def sc_intro(ctx, t, d):
    s1, s2, s3 = ST("intro", 1), ST("intro", 2), ST("intro", 3)
    on = pk(t, WT("intro", "remote") + 0.3, 0.6)
    eyes = 1.0 if t < s1 + 4.0 else 0.0
    hx, hy, r = bedroom(ctx, t, tv_on=on, eyes=eyes, zz=pk(t, s1 + 4.2, 0.8) * (1 - pk(t, s3, 0.6)))
    # le cerveau « s'allume » : bulles de pensées au-dessus de la tête
    kb = pk(t, WT("intro", "turns") - 0.2, 0.6) * (1 - pk(t, s1 + 2.5, 0.8))
    for i, (dx, dy, ic) in enumerate(((0.02, -0.20, ic_calendar), (0.12, -0.28, ic_dollar), (0.22, -0.20, ic_lock), (0.08, -0.12, ic_alert))):
        bubble(ctx, hx + W * dx, hy + H * dy + 6 * U * math.sin(t * 2 + i), 46 * U, clamp(kb * 1.4 - i * 0.12), ic, tail=(hx, hy - r))
    if t < 4.5:   # accroche écrite dès la 1re image
        big(ctx, "WHY YOU NEED", CX, H * 0.14, 110, WHITE, 1.0 - pk(t, 3.8, 0.6))
        big(ctx, "THE TV ON", CX, H * 0.27, 130, GOLD, 1.0 - pk(t, 3.8, 0.6))
    kn = pk(t, s2, 0.5) * (1 - pk(t, s3 - 0.3, 0.4))
    pill(ctx, "YOU'RE NOT ALONE", CX, H * 0.12, GOLD, 52, kn)
    if t > s3 - 0.3:   # les 4 parties de la vidéo
        rgba(ctx, (0.02, 0.02, 0.06), 0.55 * pk(t, s3 - 0.3, 0.5)); ctx.paint()
        items = (("THE DARK BRAIN", PURPLE, WT("intro", "brain", 1)), ("WHY A VOICE", CYAN, WT("intro", "voice")),
                 ("THE HIDDEN COST", CORAL, WT("intro", "costs")), ("WHAT HELPS", GREEN, WT("intro", "tested")))
        for i, (lab, col, tw) in enumerate(items):
            k = pk(t, min(tw, s3 + 1.0 + i * 2.0) - 0.3, 0.5); x = W * (0.17 + i * 0.22)
            if k <= 0: continue
            rrect(ctx, x - W * 0.095, H * 0.30, W * 0.19, H * 0.30, 24 * U); rgba(ctx, mix(col, NAVY, 0.65), 0.95 * k); ctx.fill()
            neon_text(ctx, str(i + 1), x, H * 0.40, 110 * U, col, k, WHITE, fill=0.3)
            text(ctx, lab, x, H * 0.54, 34 * U, WHITE, k)

def sc_poll(ctx, t, d):
    s1, s2, s3 = ST("poll", 1), ST("poll", 2), ST("poll", 3)
    night_bg(ctx, t, tint=CYAN)
    if t < s1:
        big(ctx, "HOW COMMON?", CX, H * 0.40, 150, GOLD, pk(t, 0.1))
    elif t < s2:
        kicker(ctx, "NATIONAL SLEEP FOUNDATION POLL · 2011", pk(t, s1))
        text(ctx, "Watch TV in the hour before bed, every night or almost", CX, H * 0.16, 38 * U, WHITE, pk(t, s1 + 0.4))
        data = (("BABY BOOMERS", 0.67, GOLD), ("GEN X", 0.63, CORAL), ("GEN Y", 0.49, CYAN), ("GEN Z", 0.50, GREEN))
        for i, (lab, v, col) in enumerate(data):
            bar(ctx, W * (0.26 + i * 0.16), H * 0.66, W * 0.10, H * 0.38, v, col, pk(t, s1 + 1.0 + i * 0.6, 0.8), lab, f"{int(round(v * 100 * ease(pk(t, s1 + 1.0 + i * 0.6, 0.8))))}%")
    else:
        def still(ctx, x0, y0, w, h, tt):
            sitcom(ctx, x0, y0, w, h, 0.0); rgba(ctx, (0, 0, 0), 0.55); ctx.paint()
            rrect(ctx, x0 + w * 0.18, y0 + h * 0.30, w * 0.64, h * 0.40, 12 * U); rgba(ctx, (0.08, 0.08, 0.12), 0.95); ctx.fill()
            text(ctx, "Are you still watching?", x0 + w / 2, y0 + h * 0.44, h * 0.08, WHITE, 1)
            rrect(ctx, x0 + w * 0.30, y0 + h * 0.54, w * 0.40, h * 0.10, 8 * U); rgba(ctx, WHITE, 0.9); ctx.fill()
            text(ctx, "CONTINUE", x0 + w / 2, y0 + h * 0.59, h * 0.05, DARK, 1)
        off = pk(t, s3 + 0.8, 1.0)
        bedroom(ctx, t, tv_on=1.0 - off, eyes=0.0 if t < s3 else 1.0, zz=(1 - pk(t, s3, 0.4)), clock="3:00", content=still)
        if t > s3: big(ctx, "SILENCE", CX, H * 0.15, 120, WHITE, pk(t, s3 + 1.2, 0.6))

def sc_ch1(ctx, t, d): chapter(ctx, t, d, 1, "THE LOUD SILENCE", PURPLE)
def sc_ch2(ctx, t, d): chapter(ctx, t, d, 2, "WHY A VOICE WORKS", CYAN)
def sc_ch3(ctx, t, d): chapter(ctx, t, d, 3, "WHAT THE TV COSTS YOU", CORAL)
def sc_ch4(ctx, t, d): chapter(ctx, t, d, 4, "WHAT ACTUALLY HELPS", GREEN)

def sc_dmn(ctx, t, d):
    s1, s2, s3 = ST("dmn", 1), ST("dmn", 2), ST("dmn", 3)
    night_bg(ctx, t, tint=PURPLE)
    bx, by, bs = CX, H * 0.42, H * 0.30
    if t < s3:
        brain(ctx, bx, by, bs, t, hi=pk(t, WT("dmn", "default") - 0.3, 0.8))
        if t < s1: big(ctx, "RESTING?", CX, H * 0.10, 90, WHITE, pk(t, 0.3))
        if s1 <= t < s2:
            kicker(ctx, "RAICHLE ET AL. · PNAS · 2001", pk(t, s1))
            pill(ctx, "DEFAULT MODE NETWORK", CX, H * 0.70, GOLD, 50, pk(t, WT("dmn", "default") - 0.2))
        if t >= s2:
            pill(ctx, "YOUR BRAIN'S SCREENSAVER", CX, H * 0.10, GOLD, 46, pk(t, s2))
            ics = ((ic_chat, "replaying", -0.30, -0.12), (ic_calendar, "planning", 0.30, -0.15), (ic_alert, "rehearsing", -0.33, 0.20), (ic_lock, "locked", 0.33, 0.18))
            for i, (ic, w_, dx, dy) in enumerate(ics):
                ang = t * 0.4 + i * 1.57
                bubble(ctx, bx + W * dx + 10 * U * math.cos(ang), by + H * dy + 10 * U * math.sin(ang), 62 * U, pk(t, WT("dmn", w_) - 0.3, 0.5), ic)
    else:
        # jour : le bruit couvre ; nuit : volume au maximum
        k = pk(t, s3, 0.5); kn = pk(t, WT("dmn", "night") - 0.2, 0.6)
        ctx.rectangle(0, 0, W / 2, H); g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, 0.45, 0.70, 0.98); g.add_color_stop_rgb(1, 0.85, 0.92, 1.0); ctx.set_source(g); ctx.fill()
        text(ctx, "DAY", W * 0.25, H * 0.10, 60 * U, DARK, k)
        for i, lab in enumerate(("TRAFFIC", "WORK", "PEOPLE")):
            pill(ctx, lab, W * 0.25, H * (0.24 + i * 0.12), (0.30, 0.45, 0.85), 40, pk(t, WT("dmn", lab.lower()) - 0.2), fg=WHITE)
        brain(ctx, W * 0.25, H * 0.62, H * 0.10, t, hi=0.15)
        text(ctx, "NIGHT", W * 0.75, H * 0.10, 60 * U, WHITE, kn)
        brain(ctx, W * 0.75, H * 0.42, H * 0.18 * (0.6 + 0.4 * kn), t, hi=kn)
        vol = pk(t, WT("dmn", "volume") - 0.6, 1.0)
        for i in range(10):
            on = i < 3 + 7 * vol
            rrect(ctx, W * 0.61 + i * W * 0.028, H * 0.68 - i * H * 0.012, W * 0.02, H * 0.03 + i * H * 0.012, 4 * U)
            rgba(ctx, CORAL if on and i > 6 else (GOLD if on else WHITE), 0.95 if on else 0.15 * kn); ctx.fill()
        if vol > 0.5: pill(ctx, "FULL VOLUME", W * 0.75, H * 0.22, CORAL, 44, pk(t, WT("dmn", "volume") - 0.1), fg=WHITE)

def phone(ctx, x, y, s, t, msg=None, k=1.0):
    rrect(ctx, x - s * 0.5, y - s, s, s * 2, s * 0.15); rgba(ctx, (0.1, 0.1, 0.14), k); ctx.fill()
    glow(ctx, x, y, s * 1.6, TVB, 0.35 * k)
    rrect(ctx, x - s * 0.44, y - s * 0.9, s * 0.88, s * 1.8, s * 0.1); rgba(ctx, (0.40, 0.65, 1.0), k); ctx.fill()
    if msg:
        rrect(ctx, x - s * 0.40, y - s * 0.55, s * 0.80, s * 0.55, s * 0.08); rgba(ctx, WHITE, 0.95 * k); ctx.fill()
        for j, l in enumerate(msg): text(ctx, l, x, y - s * (0.40 - j * 0.2), s * 0.11, DARK, k)

def sc_wander(ctx, t, d):
    s1, s2, s3 = ST("wander", 1), ST("wander", 2), ST("wander", 3)
    night_bg(ctx, t, tint=CYAN)
    kicker(ctx, "KILLINGSWORTH & GILBERT · HARVARD · SCIENCE · 2010", pk(t, 0.2))
    if t < s1:
        for i in range(5):
            x = W * (0.18 + i * 0.16); kk = pk(t, min(WT("wander", "pinged") - 0.4, 1.0) + i * 0.35, 0.4)
            phone(ctx, x, H * 0.42, H * 0.14, t, ("What are you", "thinking about?"), kk)
            if kk > 0: circle(ctx, x + H * 0.06, H * 0.42 - H * 0.15, 14 * U, CORAL, kk * (0.6 + 0.4 * math.sin(t * 6 + i)))
    elif t < s2:
        k = pk(t, s1, 1.2); v = 0.47 * ease(pk(t, WT("wander", "forty-seven") - 0.6, 1.2))
        r = H * 0.22; cx_, cy_ = CX, H * 0.42
        ctx.new_path(); ctx.arc(cx_, cy_, r, 0, 2 * math.pi); ctx.set_line_width(46 * U); rgba(ctx, WHITE, 0.12 * k); ctx.stroke()
        ctx.new_path(); ctx.arc(cx_, cy_, r, -math.pi / 2, -math.pi / 2 + 2 * math.pi * v); ctx.set_line_width(46 * U); rgba(ctx, PURPLE, k); ctx.stroke()
        big(ctx, f"{int(round(v * 100))}%", cx_, cy_, 120, WHITE, k)
        text(ctx, "of the time, minds were somewhere else", CX, H * 0.72, 40 * U, (0.9, 0.9, 1.0), k)
    elif t < s3:
        for i, (lab, x, mood, col) in enumerate((("FOCUSED", 0.32, 1.0, GREEN), ("WANDERING", 0.68, -0.6, PURPLE))):
            kk = pk(t, s2 + i * 0.8, 0.5); xx = W * x
            circle(ctx, xx, H * 0.40, H * 0.15 * ease(kk), (1.0, 0.82, 0.30), kk)
            for sx in (-1, 1): circle(ctx, xx + sx * H * 0.05, H * 0.37, H * 0.015, DARK, kk)
            ctx.new_path(); ctx.arc(xx, H * (0.45 if mood > 0 else 0.50), H * 0.06, (0.15 if mood > 0 else 1.15) * math.pi, (0.85 if mood > 0 else 1.85) * math.pi)
            ctx.set_line_width(7 * U); rgba(ctx, DARK, kk); ctx.stroke()
            pill(ctx, lab, xx, H * 0.66, col, 42, kk, fg=DARK)
        text(ctx, "Even pleasant daydreams didn't make people happier", CX, H * 0.12, 38 * U, WHITE, pk(t, WT("wander", "daydreams") - 0.2))
    else:
        k = pk(t, s3, 0.6)
        rrect(ctx, W * 0.14, H * 0.24, W * 0.72, H * 0.36, 28 * U); rgba(ctx, (0.02, 0.02, 0.06), 0.7 * k); ctx.fill()
        neon_text(ctx, "“A WANDERING MIND", CX, H * 0.36, 82 * U, GOLD, k, CORAL, fill=0.3)
        neon_text(ctx, "IS AN UNHAPPY MIND”", CX, H * 0.48, 82 * U, GOLD, pk(t, s3 + 0.8, 0.6), CORAL, fill=0.3)
        text(ctx, "title of the 2010 study", CX, H * 0.66, 34 * U, (0.85, 0.88, 1.0), k)

def sc_shock(ctx, t, d):
    s1, s2, s3, s4 = (ST("shock", i) for i in range(1, 5))
    if t < s4:
        vgrad(ctx, (0.88, 0.89, 0.92), (0.70, 0.72, 0.78))   # pièce blanche, vide
        kicker(ctx, "WILSON ET AL. · SCIENCE · 2014", pk(t, 0.2), col=WHITE)
        ctx.rectangle(0, H * 0.66, W, H * 0.34); rgba(ctx, (0.60, 0.62, 0.68), 1); ctx.fill()
        # chaise et silhouette
        x = W * 0.32
        rrect(ctx, x - 80 * U, H * 0.50, 160 * U, 24 * U, 8 * U); rgba(ctx, (0.35, 0.30, 0.28), 1); ctx.fill()
        for sx in (-1, 1): ctx.rectangle(x + sx * 64 * U - 6 * U, H * 0.52, 12 * U, H * 0.15); rgba(ctx, (0.35, 0.30, 0.28), 1); ctx.fill()
        ctx.rectangle(x + 60 * U, H * 0.30, 14 * U, H * 0.22); ctx.fill()
        pictogram(ctx, x, H * 0.44, H * 0.22, (0.25, 0.30, 0.55))
        if t < s2:
            k = pk(t, s1, 0.5); left = 15 - 15 * clamp((t - s1) / max(s2 - s1, 0.1))
            big(ctx, f"{int(left):02d}:00" if left >= 1 else "00:00", W * 0.68, H * 0.30, 120, CORAL, k)
            text(ctx, "MINUTES ALONE · JUST THINK", W * 0.68, H * 0.44, 40 * U, DARK, k)
            for i, lab in enumerate(("NO PHONE", "NO BOOK")):
                ki = pk(t, WT("shock", "phone") - 0.2 + i * 0.6)
                pill(ctx, lab, W * (0.60 + i * 0.17), H * 0.56, (0.15, 0.15, 0.20), 38, ki, fg=WHITE)
                if ki > 0: no_x(ctx, W * (0.60 + i * 0.17), H * 0.56, 70 * U, ki)
        elif t < s3:
            k = pk(t, s2, 0.5); bx_, by_ = W * 0.66, H * 0.42
            glow(ctx, bx_, by_, 220 * U, GOLD, 0.4 * k)
            circle(ctx, bx_, by_ + 14 * U, 110 * U * ease(k), (0.55, 0.08, 0.10), k); circle(ctx, bx_, by_, 110 * U * ease(k), (0.95, 0.20, 0.22), k)
            bolt(ctx, bx_, by_, 60 * U * ease(k), WHITE, k)
            pill(ctx, "MILD ELECTRIC SHOCK", bx_, H * 0.64, GOLD, 40, pk(t, WT("shock", "electric") - 0.2))
        else:
            k = pk(t, s3, 0.5)
            for g_, (lab, n, hit, x0) in enumerate((("MEN", 3, 2, 0.58), ("WOMEN", 4, 1, 0.58))):
                yy = H * (0.30 + g_ * 0.24)
                for i in range(n):
                    kk = pk(t, s3 + g_ * 1.5 + i * 0.15, 0.4)
                    col = CORAL if i < hit else (0.45, 0.48, 0.58)
                    pictogram(ctx, W * x0 + i * W * 0.07, yy, H * 0.14, col, kk)
                    if i < hit and kk > 0: bolt(ctx, W * x0 + i * W * 0.07 + 26 * U, yy - H * 0.11, 18 * U, GOLD, kk)
                pill(ctx, ("2 IN 3 " if g_ == 0 else "1 IN 4 ") + lab, W * 0.86, yy, CORAL, 38, pk(t, s3 + g_ * 1.5 + 0.6), fg=WHITE)
            kc = pk(t, WT("shock", "one", 2) - 0.2, 1.4)
            if kc > 0: pill(ctx, f"ONE MAN: {int(190 * ease(kc))}×", W * 0.72, H * 0.70, GOLD, 50, kc)
    else:
        bedroom(ctx, t, tv_on=pk(t, WT("shock", "fixes") - 0.5, 0.8), eyes=1.0, zz=0.0, clock="12:00")
        big(ctx, "MIDNIGHT", CX, H * 0.12, 100, WHITE, pk(t, s4, 0.5) * (1 - pk(t, WT("shock", "silence") - 0.2, 0.5)))
        pill(ctx, "THE TV FIXES THE SILENCE", CX, H * 0.12, GOLD, 46, pk(t, WT("shock", "silence") - 0.2))

def no_sign(ctx, x, y, r, k):
    if k <= 0: return
    ctx.new_path(); ctx.arc(x, y, r, 0, 2 * math.pi); ctx.set_line_width(r * 0.16); rgba(ctx, CORAL, k); ctx.stroke()
    ctx.new_path(); ctx.move_to(x - r * 0.7, y - r * 0.7); ctx.line_to(x + r * 0.7, y + r * 0.7); ctx.stroke()

def no_x(ctx, x, y, r, k):
    for s_ in (-1, 1):
        ctx.new_path(); ctx.move_to(x - r * 0.9, y - s_ * r * 0.35); ctx.line_to(x + r * 0.9, y + s_ * r * 0.35)
        ctx.set_line_width(8 * U); ctx.set_line_cap(cairo.LINE_CAP_ROUND); rgba(ctx, CORAL, 0.9 * k); ctx.stroke()

def bolt(ctx, x, y, s, col, a=1.0):
    ctx.new_path(); ctx.move_to(x + s * 0.15, y - s); ctx.line_to(x - s * 0.45, y + s * 0.1); ctx.line_to(x - s * 0.02, y + s * 0.1)
    ctx.line_to(x - s * 0.20, y + s); ctx.line_to(x + s * 0.45, y - s * 0.15); ctx.line_to(x + s * 0.02, y - s * 0.15); ctx.close_path(); rgba(ctx, col, a); ctx.fill()

def slots(ctx, t, items, k=1.0, y=0.46):
    """Les 4 cases de la mémoire de travail ; items = liste de (icône, couleur) ou None."""
    for i in range(4):
        x = W * (0.23 + i * 0.18)
        rrect(ctx, x - W * 0.075, H * y - H * 0.14, W * 0.15, H * 0.28, 22 * U); rgba(ctx, WHITE, 0.10 * k); ctx.fill()
        ctx.new_path(); rrect(ctx, x - W * 0.075, H * y - H * 0.14, W * 0.15, H * 0.28, 22 * U); ctx.set_line_width(4 * U); rgba(ctx, WHITE, 0.5 * k); ctx.stroke()
        it = items[i] if i < len(items) else None
        if it:
            ic, col, ki = it
            if ki > 0:
                circle(ctx, x, H * y, H * 0.10 * ease(ki), mix(col, NAVY, 0.5), ki)
                ic(ctx, x, H * y, H * 0.06 * ease(ki))

def ic_tv(ctx, x, y, r):
    rrect(ctx, x - r, y - r * 0.65, 2 * r, 1.3 * r, r * 0.15); rgba(ctx, (0.1, 0.1, 0.15), 1); ctx.fill()
    rrect(ctx, x - r * 0.85, y - r * 0.52, 1.7 * r, 1.04 * r, r * 0.08); rgba(ctx, TVB, 1); ctx.fill()
    for i in (-1, 1): circle(ctx, x + i * r * 0.35, y - r * 0.05, r * 0.18, (1.0, 0.85, 0.6), 1)

def sc_memory(ctx, t, d):
    s1, s2, s3 = (ST("memory", i) for i in range(1, 4))
    night_bg(ctx, t, tint=CYAN)
    if t < s1:
        big(ctx, "WHY A VOICE?", CX, H * 0.40, 130, CYAN, pk(t, 0.1))
        return
    kicker(ctx, "WORKING MEMORY · ABOUT 4 CHUNKS AT ONCE (COWAN, 2001)", pk(t, WT("memory", "cowan") - 0.3))
    big(ctx, "YOUR MENTAL DESK", CX, H * 0.17, 80, WHITE, pk(t, s1))
    worries = [(ic_alert, CORAL), (ic_dollar, GREEN), (ic_calendar, GOLD), (ic_lock, PURPLE)]
    tvk = pk(t, s2, 0.8)
    items = []
    for i in range(4):
        wk = pk(t, WT("memory", "four") - 0.5 + i * 0.3, 0.4)
        if i < 3 and tvk > 0:
            items.append((ic_tv if tvk > 0.5 else worries[i][0], CYAN if tvk > 0.5 else worries[i][1], 1.0))
        else:
            items.append((worries[i][0], worries[i][1], wk))
    slots(ctx, t, items, pk(t, s1 + 1.0))
    if tvk > 0:
        for i in range(3):   # les soucis sont poussés hors des cases
            x = W * (0.23 + i * 0.18); yy = H * 0.46 - H * 0.35 * ease(tvk)
            if tvk < 1: circle(ctx, x, yy, H * 0.05, worries[i][1], 1 - tvk)
        pill(ctx, "WORRIES HAVE LESS ROOM", CX, H * 0.72, GOLD, 44, pk(t, WT("memory", "worries") - 0.2))
    if t > s3: pill(ctx, "IT JUST TAKES UP SPACE", CX, H * 0.72, CYAN, 44, pk(t, s3 + 0.5), fg=DARK)

def sc_effort(ctx, t, d):
    s1, s2 = ST("effort", 1), ST("effort", 2)
    night_bg(ctx, t, tint=PURPLE)
    if t < s1:
        bed(ctx, W * 0.42, H * 0.58, W * 0.46, t, eyes=1.0)
        k = pk(t, WT("effort", "trying") - 0.2)
        pill(ctx, "TRY HARDER!", W * 0.72, H * 0.20, CORAL, 52, k, fg=WHITE)
        big(ctx, "THE MORE YOU TRY…", CX, H * 0.10, 70, WHITE, pk(t, WT("effort", "harder") - 0.3))
        # chronomètre qui s'emballe
        cx_, cy_ = W * 0.74, H * 0.42
        circle(ctx, cx_, cy_, 80 * U * ease(k), WHITE, 0.95 * k)
        ctx.new_path(); ctx.move_to(cx_, cy_); a_ = t * 6
        ctx.line_to(cx_ + 60 * U * math.sin(a_) * ease(k), cy_ - 60 * U * math.cos(a_) * ease(k)); ctx.set_line_width(8 * U); rgba(ctx, CORAL, k); ctx.stroke()
    elif t < s2:
        kicker(ctx, "ANSFIELD, WEGNER & BOWSER · 1996", pk(t, s1))
        for i, (lab, sub, frac, col) in enumerate((("“FALL ASLEEP FAST!”", "+ busy mind", 0.85, CORAL), ("NO PRESSURE", "", 0.55, GREEN))):
            y = H * (0.30 + i * 0.22); k = pk(t, s1 + 1.0 + i * 1.6, 0.8)
            text(ctx, lab, W * 0.22, y, 40 * U, WHITE, k)
            if sub: text(ctx, sub, W * 0.22, y + 44 * U, 30 * U, (0.85, 0.85, 1.0), k)
            rrect(ctx, W * 0.38, y - 30 * U, W * 0.50, 60 * U, 30 * U); rgba(ctx, WHITE, 0.10); ctx.fill()
            rrect(ctx, W * 0.38, y - 30 * U, W * 0.50 * frac * ease(k), 60 * U, 30 * U); rgba(ctx, col, 0.95); ctx.fill()
        text(ctx, "TIME TO FALL ASLEEP →", W * 0.63, H * 0.64, 34 * U, (0.85, 0.88, 1.0), pk(t, s1 + 1.0))
        pill(ctx, "TOOK LONGER", W * 0.80, H * 0.18, CORAL, 40, pk(t, WT("effort", "longer") - 0.2), fg=WHITE)
    else:
        bedroom(ctx, t, tv_on=1.0, eyes=1.0 if t < WT("effort", "sneaks") - 0.5 else 0.0, zz=pk(t, WT("effort", "sneaks") - 0.3, 0.8))
        pill(ctx, "NO PRESSURE · JUST WATCHING", CX, H * 0.10, GOLD, 44, pk(t, s2))

def thriller(ctx, x0, y0, w, h, t):
    vgrad(ctx, (0.08, 0.05, 0.12), (0.02, 0.02, 0.05), y0, y0 + h)
    ctx.rectangle(x0, y0, w, h); g = cairo.LinearGradient(0, y0, 0, y0 + h); g.add_color_stop_rgb(0, 0.12, 0.06, 0.16); g.add_color_stop_rgb(1, 0.02, 0.02, 0.05); ctx.set_source(g); ctx.fill()
    circle(ctx, x0 + w * 0.5, y0 + h * 0.35, h * 0.10, (0.15, 0.12, 0.2), 1)
    rrect(ctx, x0 + w * 0.42, y0 + h * 0.45, w * 0.16, h * 0.45, 10 * U); rgba(ctx, (0.15, 0.12, 0.2), 1); ctx.fill()
    text(ctx, "?", x0 + w * 0.80, y0 + h * 0.35, h * 0.35, CORAL, 0.6 + 0.4 * math.sin(t * 5))

def sc_rerun(ctx, t, d):
    s1, s2, s3 = (ST("rerun", i) for i in range(1, 4))
    night_bg(ctx, t, tint=GOLD)
    ka = pk(t, WT("rerun", "thriller") - 0.3); kb = pk(t, WT("rerun", "sitcom") - 0.3)
    hl_new = pk(t, s1, 0.5) * (1 - pk(t, s2, 0.5)); hl_old = pk(t, s2, 0.5)
    for i, (x, k, lab, fn, col, hl) in enumerate(((0.28, ka, "NEW THRILLER", thriller, CORAL, hl_new), (0.72, kb, "THE SITCOM YOU KNOW", sitcom, GREEN, hl_old))):
        if k <= 0: continue
        sc_ = 1.0 + 0.10 * hl
        ctx.save(); ctx.translate(W * x, H * 0.38); ctx.scale(sc_, sc_); ctx.translate(-W * x, -H * 0.38)
        tv(ctx, W * x, H * 0.38, W * 0.32, t, on=k, content=fn, stand=False)
        ctx.restore()
        pill(ctx, lab, W * x, H * 0.66, col, 40, k, fg=DARK)
    if s1 <= t < s2:
        for i, q in enumerate(("WHO DID IT?", "WHAT'S NEXT?")):
            pill(ctx, q, W * 0.28 + (i - 0.5) * W * 0.16, H * 0.12, CORAL, 34, pk(t, WT("rerun", "who" if i == 0 else "next") - 0.2), fg=WHITE)
        pill(ctx, "BRAIN STAYS ALERT", W * 0.28, H * 0.75, CORAL, 34, pk(t, WT("rerun", "alert") - 0.2), fg=WHITE)
    if t >= s2:
        for i, q in enumerate(("✓ EVERY JOKE", "✓ EVERY ENDING")):
            pill(ctx, q, W * 0.72 + (i - 0.5) * W * 0.17, H * 0.12, GREEN, 34, pk(t, WT("rerun", "joke" if i == 0 else "ending") - 0.2))
        if t > WT("rerun", "comfort") - 0.3: pill(ctx, "COMFORT", W * 0.72, H * 0.75, GOLD, 40, pk(t, WT("rerun", "comfort") - 0.2))
    if t >= s3: big(ctx, "NO SURPRISES", W * 0.28, H * 0.12, 70, WHITE, pk(t, s3))

def sc_company(ctx, t, d):
    s1, s2, s3 = (ST("company", i) for i in range(1, 4))
    if t < s1 or t >= s3:
        hx, hy, r = bedroom(ctx, t, tv_on=1.0, eyes=1.0 if t < s3 else 0.0, zz=pk(t, s3 + 2.0, 1.0))
        for i in range(4):   # bulles de voix qui flottent de la télé vers le lit
            ph = (t * 0.18 + i / 4) % 1
            x = W * 0.70 - ph * W * 0.30; y = H * 0.35 + math.sin(ph * 3.14) * -H * 0.06
            bubble(ctx, x, y, 34 * U, math.sin(math.pi * ph), ic_chat)
        if t < s1: pill(ctx, "VOICES = SOCIAL SIGNALS", CX, H * 0.08, CYAN, 42, pk(t, 0.4), fg=DARK)
        else:
            pill(ctx, "FAMILIAR VOICES FEEL LIKE COMPANY", CX, H * 0.08, GOLD, 40, pk(t, s3))
    elif t < s2:
        night_bg(ctx, t, tint=CYAN)
        kicker(ctx, "HORTON & WOHL · 1956", pk(t, s1))
        big(ctx, "PARASOCIAL", CX, H * 0.17, 100, CYAN, pk(t, WT("company", "parasocial") - 0.3))
        tv(ctx, W * 0.66, H * 0.45, W * 0.24, t, on=1.0, content=sitcom)
        pictogram(ctx, W * 0.30, H * 0.52, H * 0.22, (0.95, 0.72, 0.40))
        ka = pk(t, WT("company", "one-sided") - 0.3, 0.8)
        arrow(ctx, W * 0.36, H * 0.42, W * 0.52, H * 0.42, PINK, ka)
        heart(ctx, W * 0.44, H * 0.34, 22 * U, PINK, ka)
        text(ctx, "one-sided", W * 0.44, H * 0.50, 34 * U, PINK, ka)
    else:
        night_bg(ctx, t, tint=PINK)
        kicker(ctx, "DERRICK, GABRIEL & HUGENBERG · 2009", pk(t, s2))
        big(ctx, "SOCIAL SURROGATE", CX, H * 0.17, 90, PINK, pk(t, min(WT("company", "surrogates") - 0.3, s2 + 1.0)))
        k = pk(t, WT("company", "lonely") - 0.6, 1.4)
        text(ctx, "FEELING LONELY", W * 0.30, H * 0.40, 38 * U, WHITE, pk(t, s2 + 1.5))
        rrect(ctx, W * 0.42, H * 0.37, W * 0.40, 56 * U, 28 * U); rgba(ctx, WHITE, 0.10); ctx.fill()
        rrect(ctx, W * 0.42, H * 0.37, W * 0.40 * (0.9 - 0.45 * ease(k)), 56 * U, 28 * U); rgba(ctx, PURPLE, 0.95 * pk(t, s2 + 1.5)); ctx.fill()
        ic_tv(ctx, W * 0.36, H * 0.58, 90 * U); text(ctx, "+ A FAVORITE SHOW", W * 0.56, H * 0.58, 48 * U, GOLD, pk(t, WT("company", "favorite", 1) - 0.3))

def campfire(ctx, x, y, s, t, a=1.0):
    for i in range(3):
        f = 1 + 0.12 * math.sin(t * 7 + i * 2)
        ctx.new_path(); ctx.move_to(x - s * 0.35 * f, y); ctx.curve_to(x - s * 0.3, y - s * 0.6 * f, x + s * 0.1, y - s * 0.7 * f, x, y - s * (1.1 - i * 0.2) * f)
        ctx.curve_to(x + s * 0.3, y - s * 0.5 * f, x + s * 0.35, y - s * 0.2, x + s * 0.35 * f, y); ctx.close_path()
        rgba(ctx, ((1.0, 0.45, 0.15), (1.0, 0.70, 0.20), (1.0, 0.92, 0.55))[i], a); ctx.fill()
    glow(ctx, x, y - s * 0.4, s * 3.0, (1.0, 0.6, 0.25), 0.45 * a)

def sc_safety(ctx, t, d):
    s1, s2 = ST("safety", 1), ST("safety", 2)
    night_bg(ctx, t, tint=CORAL, c1=(0.10, 0.06, 0.16))
    if t < s1:
        kicker(ctx, "BROSSCHOT, VERKUIL & THAYER · 2018", pk(t, 0.3))
        big(ctx, "GENERALIZED UNSAFETY THEORY", CX, H * 0.17, 72, WHITE, pk(t, min(WT("safety", "generalized") - 0.3, 2.0)))
        k = pk(t, 1.0)
        # voyant d'alarme allumé par défaut, qui s'éteint quand les signes de sécurité arrivent
        safe = pk(t, WT("safety", "safe") - 0.5, 1.0)
        col = mix(CORAL, GREEN, safe)
        glow(ctx, W * 0.30, H * 0.45, 200 * U, col, 0.5 * k * (0.7 + 0.3 * math.sin(t * 5 * (1 - safe))))
        circle(ctx, W * 0.30, H * 0.45, 90 * U * ease(k), col, k)
        text(ctx, "STRESS ON" if safe < 0.5 else "SAFE", W * 0.30, H * 0.62, 42 * U, col, k)
        for i in range(4):
            pill(ctx, "✓ SAFETY SIGNAL", W * 0.66, H * (0.32 + i * 0.09), GREEN, 34, pk(t, WT("safety", "signs") - 0.3 + i * 0.4))
    else:
        # autour du feu : des voix = le groupe est là ; seul dans le silence = exposé
        ctx.rectangle(0, H * 0.62, W, H * 0.38); rgba(ctx, (0.05, 0.04, 0.08), 1); ctx.fill()
        k1 = pk(t, s1, 0.6)
        campfire(ctx, W * 0.30, H * 0.60, 70 * U, t, k1)
        for i, dx in enumerate((-0.12, -0.06, 0.06, 0.12)):
            pictogram(ctx, W * (0.30 + dx), H * 0.60, H * 0.16, (0.22, 0.16, 0.20), k1)
        for i in range(3):
            ph = (t * 0.3 + i / 3) % 1
            bubble(ctx, W * (0.22 + i * 0.08), H * (0.38 - ph * 0.10), 40 * U, k1 * math.sin(math.pi * ph), ic_chat)
        pill(ctx, "VOICES NEARBY = SAFE", W * 0.30, H * 0.16, GREEN, 40, pk(t, WT("safety", "voices") - 0.2))
        k2 = pk(t, WT("safety", "silence") - 0.3, 0.6)
        pictogram(ctx, W * 0.74, H * 0.60, H * 0.16, (0.30, 0.32, 0.50), k2)
        pill(ctx, "SILENCE = ALONE?", W * 0.74, H * 0.16, CORAL, 40, k2, fg=WHITE)
        if t >= s2: pill(ctx, "ONLY A THEORY", CX, H * 0.72, (0.85, 0.85, 0.95), 36, pk(t, s2))

def eye(ctx, x, y, s, t, k=1.0, cells=0.0):
    """Œil en coupe (schéma simplifié) : rétine + cellules sensibles à la lumière (ipRGC) en or."""
    ctx.save(); ctx.push_group()
    circle(ctx, x, y, s, (0.98, 0.96, 0.95), 1)
    ctx.new_path(); ctx.arc(x, y, s * 0.96, -math.pi * 0.72, math.pi * 0.72); ctx.set_line_width(s * 0.08); rgba(ctx, (0.92, 0.45, 0.45), 1); ctx.stroke()   # rétine
    ctx.new_path(); ellipse(ctx, x - s * 0.95, y, s * 0.12, s * 0.42); rgba(ctx, (0.55, 0.75, 1.0), 1); ctx.fill()          # cornée / cristallin
    circle(ctx, x - s * 0.72, y, s * 0.18, (0.25, 0.45, 0.80), 1)
    if cells > 0:
        for i in range(9):
            a_ = -math.pi * 0.6 + i * math.pi * 0.15
            px, py = x + math.cos(a_) * s * 0.96, y + math.sin(a_) * s * 0.96
            glow(ctx, px, py, s * 0.12, GOLD, 0.7 * cells * (0.7 + 0.3 * math.sin(t * 5 + i))); circle(ctx, px, py, s * 0.05, GOLD, cells)
    ctx.new_path(); ctx.move_to(x + s * 0.95, y); ctx.line_to(x + s * 1.5, y + s * 0.15); ctx.set_line_width(s * 0.14); rgba(ctx, (0.95, 0.75, 0.55), 1); ctx.stroke()   # nerf optique
    ctx.pop_group_to_source(); ctx.paint_with_alpha(k); ctx.restore()

def clock_face(ctx, x, y, r, t, k=1.0, col=GOLD):
    circle(ctx, x, y, r * ease(k), WHITE, 0.95 * k)
    for i in range(12):
        a_ = i * math.pi / 6; ctx.new_path(); ctx.move_to(x + math.sin(a_) * r * 0.8, y - math.cos(a_) * r * 0.8); ctx.line_to(x + math.sin(a_) * r * 0.9, y - math.cos(a_) * r * 0.9)
        ctx.set_line_width(4 * U); rgba(ctx, DARK, k); ctx.stroke()
    for (ln, sp, w_) in ((0.5, 0.15, 8), (0.75, 1.2, 5)):
        a_ = t * sp; ctx.new_path(); ctx.move_to(x, y); ctx.line_to(x + math.sin(a_) * r * ln, y - math.cos(a_) * r * ln); ctx.set_line_width(w_ * U); rgba(ctx, col, k); ctx.stroke()

def sc_light(ctx, t, d):
    s1, s2, s3, s4 = (ST("light", i) for i in range(1, 5))
    if t < s1:
        bedroom(ctx, t, tv_on=1.0, eyes=0.0, zz=1.0, clock="2:47")
        pill(ctx, "ASLEEP… AND THE TV PLAYS ON", CX, H * 0.08, GOLD, 40, pk(t, 0.4))
    elif t < s2:
        night_bg(ctx, t, tint=GOLD); tag(ctx)
        kicker(ctx, "BERSON, DUNN & TAKAO · SCIENCE · 2002", pk(t, s1))
        k = pk(t, s1 + 0.3, 0.6)
        for i in range(5): arrow(ctx, W * 0.08, H * (0.32 + i * 0.05), W * 0.20, H * (0.40 + (i - 2) * 0.02), (1.0, 0.95, 0.6), pk(t, s1 + 0.8 + i * 0.1, 0.5), 5)
        eye(ctx, W * 0.34, H * 0.42, H * 0.17, t, k, cells=pk(t, WT("light", "special") - 0.3, 0.8))
        pill(ctx, "LIGHT-SENSING CELLS", W * 0.34, H * 0.16, GOLD, 38, pk(t, WT("light", "special") - 0.2))
        ka = pk(t, WT("light", "report") - 0.6, 0.8)
        arrow(ctx, W * 0.48, H * 0.44, W * 0.62, H * 0.44, GOLD, ka)
        clock_face(ctx, W * 0.74, H * 0.42, H * 0.15, t, ka)
        pill(ctx, "BODY CLOCK", W * 0.74, H * 0.65, CYAN, 40, ka, fg=DARK)
    elif t < s3:
        night_bg(ctx, t, tint=CYAN)
        # paupière fermée : un peu de lumière passe ; l'écran alterne scènes sombres / claires
        f = 0.5 + 0.5 * math.sin(t * 1.7) * math.sin(t * 0.7 + 1)
        tv(ctx, W * 0.72, H * 0.40, W * 0.30, t, on=0.35 + 0.65 * f, content=sitcom, flicker=False)
        cx_, cy_ = W * 0.30, H * 0.42
        circle(ctx, cx_, cy_, 230 * U, SKIN, 1)
        ctx.new_path(); ctx.move_to(cx_ - 170 * U, cy_); ctx.curve_to(cx_ - 90 * U, cy_ + 70 * U, cx_ + 90 * U, cy_ + 70 * U, cx_ + 170 * U, cy_)
        ctx.set_line_width(12 * U); ctx.set_line_cap(cairo.LINE_CAP_ROUND); rgba(ctx, DARK, 1); ctx.stroke()
        for i in range(7):   # cils
            f = (i + 0.5) / 7; x_ = cx_ - 150 * U + 300 * U * f; y_ = cy_ + 55 * U * math.sin(math.pi * f)
            ctx.new_path(); ctx.move_to(x_, y_); ctx.line_to(x_ + (f - 0.5) * 40 * U, y_ + 40 * U); ctx.set_line_width(8 * U); rgba(ctx, DARK, 1); ctx.stroke()
        ctx.new_path(); ctx.arc(cx_, cy_ + 10 * U, 190 * U, 1.15 * math.pi, 1.85 * math.pi); ctx.set_line_width(6 * U); rgba(ctx, mix(SKIN, DARK, 0.3), 1); ctx.stroke()
        text(ctx, "CLOSED EYELID", cx_, cy_ - 130 * U, 34 * U, DARK, 0.8)
        for i in range(6): arrow(ctx, W * 0.58, H * (0.30 + i * 0.04), W * 0.44, H * (0.36 + i * 0.02), TVB, f * pk(t, s2 + 0.5), 4)
        glow(ctx, cx_, cy_, 160 * U, TVB, 0.35 * f)
        pill(ctx, "SOME LIGHT GETS THROUGH", cx_, H * 0.66, TVB, 38, pk(t, WT("light", "eyelids") - 0.3), fg=DARK)
        pill(ctx, "DARK → BRIGHT → DARK", W * 0.72, H * 0.72, GOLD, 36, pk(t, WT("light", "flickers") - 0.3))
    elif t < s4 + 0.5:
        night_bg(ctx, t, tint=CORAL); tag(ctx)
        kicker(ctx, "NORTHWESTERN UNIVERSITY · PNAS · 2022", pk(t, s3))
        for i, (lab, lux, lit) in enumerate((("DIM LIGHT", "< 3 lux", 0.0), ("ROOM LIGHTS ON", "100 lux", 1.0))):
            x = W * (0.28 + i * 0.44); k = pk(t, s3 + 0.6 + i * 0.8, 0.6)
            if lit: glow(ctx, x, H * 0.22, 220 * U, (1.0, 0.95, 0.7), 0.6 * k)
            circle(ctx, x, H * 0.14, 22 * U, (1.0, 0.95, 0.70) if lit else (0.3, 0.3, 0.4), k)
            bed(ctx, x, H * 0.40, W * 0.28, t, eyes=0.0, a=k)
            text(ctx, lab, x, H * 0.52, 38 * U, WHITE, k); text(ctx, lux, x, H * 0.57, 30 * U, (0.8, 0.85, 1.0), k)
        kh = pk(t, WT("light", "heart") - 0.3, 0.6); ks = pk(t, WT("light", "sugar") - 0.3, 0.6)
        heart(ctx, W * 0.66, H * 0.67, 26 * U, CORAL, kh); text(ctx, "HEART RATE ↑", W * 0.78, H * 0.67, 34 * U, CORAL, kh)
        text(ctx, "NEXT MORNING: SUGAR HANDLED LESS WELL", W * 0.72, H * 0.73, 30 * U, GOLD, ks)
    else:
        night_bg(ctx, t, tint=GOLD)
        k = pk(t, s4 + 0.5, 0.5)
        pill(ctx, "OVERHEAD LIGHT · NOT A TV", CX, H * 0.28, (0.85, 0.85, 0.95), 44, k)
        big(ctx, "THE SLEEPING BODY", CX, H * 0.44, 90, WHITE, pk(t, WT("light", "sleeping") - 0.3))
        big(ctx, "STILL REACTS TO LIGHT", CX, H * 0.57, 90, GOLD, pk(t, WT("light", "reacts") - 0.3))

def ebook(ctx, x, y, s, glowing, k):
    if glowing:
        glow(ctx, x, y, s * 2.2, TVB, 0.5 * k)
        rrect(ctx, x - s * 0.6, y - s * 0.8, s * 1.2, s * 1.6, s * 0.1); rgba(ctx, (0.1, 0.1, 0.14), k); ctx.fill()
        rrect(ctx, x - s * 0.5, y - s * 0.7, s * 1.0, s * 1.4, s * 0.06); rgba(ctx, (0.85, 0.93, 1.0), k); ctx.fill()
    else:
        rrect(ctx, x - s * 0.7, y - s * 0.6, s * 1.4, s * 1.2, s * 0.06); rgba(ctx, (0.80, 0.35, 0.25), k); ctx.fill()
        rrect(ctx, x - s * 0.62, y - s * 0.52, s * 1.24, s * 1.04, s * 0.04); rgba(ctx, (0.98, 0.95, 0.86), k); ctx.fill()
        ctx.rectangle(x - 2 * U, y - s * 0.52, 4 * U, s * 1.04); rgba(ctx, (0.6, 0.5, 0.4), k); ctx.fill()
    for j in range(5):
        for sx in ((-1, 1) if not glowing else (0,)):
            w_ = s * (0.45 if not glowing else 0.75)
            ctx.rectangle(x + sx * s * 0.32 - w_ / 2, y - s * 0.38 + j * s * 0.17, w_, s * 0.05); rgba(ctx, (0.4, 0.4, 0.5), 0.7 * k); ctx.fill()

def sc_screens(ctx, t, d):
    s1, s2, s3 = (ST("screens", i) for i in range(1, 4))
    night_bg(ctx, t, tint=TVB)
    if t < s1:
        phone(ctx, W * 0.42, H * 0.40, H * 0.16, t, None, pk(t, 0.2))
        glow(ctx, W * 0.42, H * 0.40, 260 * U, TVB, 0.5 * pk(t, 0.2))
        tv(ctx, W * 0.78, H * 0.36, W * 0.14, t, on=pk(t, 0.6), content=sitcom)
        pill(ctx, "CLOSE TO YOUR FACE", W * 0.42, H * 0.70, TVB, 40, pk(t, WT("screens", "face") - 0.3), fg=DARK)
    elif t < s2 + 0.3:
        kicker(ctx, "CHANG ET AL. · HARVARD · PNAS · 2014", pk(t, s1))
        for i, (lab, gl) in enumerate((("PRINTED BOOK", False), ("E-READER", True))):
            x = W * (0.32 + i * 0.36); k = pk(t, min(WT("screens", "printed" if i == 0 else "e-reader") - 0.3, s1 + 0.3 + i * 0.6), 0.6)
            ebook(ctx, x, H * 0.38, H * 0.16, gl, k); text(ctx, lab, x, H * 0.62, 42 * U, WHITE, k)
        pill(ctx, "≈ 4 HOURS BEFORE BED · 5 NIGHTS", CX, H * 0.72, GOLD, 38, pk(t, WT("screens", "hours") - 0.3))
    elif t < s3:
        kicker(ctx, "WITH THE E-READER", pk(t, s2))
        res = (("TOOK LONGER TO FALL ASLEEP", "longer", CORAL), ("MELATONIN SUPPRESSED", "melatonin", PURPLE), ("LESS ALERT NEXT MORNING", "alert", GOLD))
        for i, (lab, w_, col) in enumerate(res):
            pill(ctx, lab, CX, H * (0.25 + i * 0.16), col, 52, pk(t, WT("screens", w_) - 0.3), fg=WHITE if col != GOLD else DARK)
    else:
        k = pk(t, s3, 0.6)
        phone(ctx, W * 0.30, H * 0.40, H * 0.14, t, None, k); tv(ctx, W * 0.70, H * 0.36, W * 0.16, t, on=k, content=sitcom)
        for i in range(7): arrow(ctx, W * 0.30, H * 0.40, W * (0.30 + math.cos(i * 0.9) * 0.10), H * (0.40 + math.sin(i * 0.9) * 0.18), TVB, k, 6)
        for i in range(3): arrow(ctx, W * 0.70, H * 0.42, W * (0.70 + math.cos(i * 2.1) * 0.05), H * (0.42 + math.sin(i * 2.1) * 0.09), TVB, k, 4)
        text(ctx, "MORE LIGHT IN YOUR EYES", W * 0.30, H * 0.66, 34 * U, WHITE, k); text(ctx, "LESS (FARTHER AWAY)", W * 0.70, H * 0.66, 34 * U, WHITE, k)
        pill(ctx, "BRIGHT LIGHT AT NIGHT = “IT'S STILL DAY”", CX, H * 0.10, GOLD, 40, pk(t, WT("screens", "bright") - 0.3))

def sc_weight(ctx, t, d):
    s1, s2 = ST("weight", 1), ST("weight", 2)
    night_bg(ctx, t, tint=PURPLE)
    kicker(ctx, "NIH · JAMA INTERNAL MEDICINE · 2019", pk(t, 0.3))
    if t < s1:
        n = int(43722 * ease(pk(t, 0.6, 2.5)))
        big(ctx, f"{n:,}", CX, H * 0.34, 150, GOLD, pk(t, 0.6))
        text(ctx, "WOMEN · FOLLOWED ABOUT 5 YEARS", CX, H * 0.50, 44 * U, WHITE, pk(t, WT("weight", "years") - 0.4))
    else:
        for i, (lab, on, col) in enumerate((("DARK ROOM", 0.0, GREEN), ("TV OR LIGHT ON", 1.0, CORAL))):
            x = W * (0.28 + i * 0.44); k = pk(t, s1 + 0.3 + i * 0.6, 0.6)
            if on: glow(ctx, x + W * 0.08, H * 0.26, 180 * U, TVB, 0.5 * k); ic_tv(ctx, x + W * 0.12, H * 0.24, 46 * U * ease(k))
            bed(ctx, x, H * 0.40, W * 0.26, t, eyes=0.0, a=k)
            text(ctx, lab, x, H * 0.52, 38 * U, WHITE, k)
        pill(ctx, "MORE LIKELY TO GAIN 11+ LB", W * 0.72, H * 0.62, CORAL, 40, pk(t, WT("weight", "eleven") - 0.3), fg=WHITE)
        if t >= s2:
            k = pk(t, s2, 0.4)
            ctx.save(); ctx.translate(CX, H * 0.17); ctx.rotate(-0.05)
            rrect(ctx, -W * 0.25, -60 * U, W * 0.50, 120 * U, 16 * U); ctx.set_line_width(8 * U); rgba(ctx, GOLD, k); ctx.stroke()
            text(ctx, "CORRELATION ≠ CAUSE", 0, 0, 62 * U, GOLD, k)
            ctx.restore()

def hypnogram(ctx, x0, x1, y, h, t, k, spikes=True):
    ctx.new_path(); n = 300
    for i in range(n + 1):
        f = i / n
        if f > k: break
        stage = 0.5 + 0.5 * math.sin(f * 9.5) * math.cos(f * 3.1)
        v = stage
        if spikes:
            for c_ in (0.12, 0.27, 0.41, 0.58, 0.70, 0.86): v -= 0.9 * math.exp(-((f - c_) / 0.006) ** 2)
        (ctx.line_to if i else ctx.move_to)(x0 + (x1 - x0) * f, y + h * (v - 0.5))
    ctx.set_line_width(5 * U); ctx.set_line_join(cairo.LINE_JOIN_ROUND); rgba(ctx, PURPLE, 1); ctx.stroke()

def sc_sound(ctx, t, d):
    s1, s2 = ST("sound", 1), ST("sound", 2)
    night_bg(ctx, t, tint=CORAL)
    if t < s1:
        wave(ctx, W * 0.10, W * 0.90, H * 0.42, 40 * U, t, spiky=True, col=CYAN, k=pk(t, 0.2, 2.0))
        for i, (lab, x, w_) in enumerate((("LAUGH TRACK", 0.24, "laugh"), ("DOOR SLAM", 0.48, "door"), ("LOUD AD", 0.73, "commercial"))):
            pill(ctx, lab, W * x, H * 0.24, CORAL, 38, pk(t, WT("sound", w_) - 0.3), fg=WHITE)
        big(ctx, "NOT A STEADY SOUND", CX, H * 0.64, 80, WHITE, pk(t, WT("sound", "steady") - 0.3))
    elif t < s2:
        kicker(ctx, "BASNER ET AL. · THE LANCET · 2014", pk(t, s1))
        text(ctx, "SLEEP", W * 0.07, H * 0.24, 34 * U, (0.85, 0.85, 1.0), pk(t, s1))
        hypnogram(ctx, W * 0.14, W * 0.90, H * 0.24, H * 0.18, t, pk(t, s1 + 0.3, 3.0))
        text(ctx, "HEART", W * 0.07, H * 0.48, 34 * U, CORAL, pk(t, s1))
        k = pk(t, s1 + 0.3, 3.0)
        ctx.new_path()
        for i in range(301):
            f = i / 300
            if f > k: break
            v = 0.0
            for c_ in (0.12, 0.27, 0.41, 0.58, 0.70, 0.86): v -= 0.8 * math.exp(-((f - c_) / 0.012) ** 2)
            v += 0.12 * math.sin(f * 120)
            (ctx.line_to if i else ctx.move_to)(W * 0.14 + W * 0.76 * f, H * 0.50 + H * 0.08 * v)
        ctx.set_line_width(5 * U); rgba(ctx, CORAL, 1); ctx.stroke()
        pill(ctx, "BRIEF AROUSALS · YOU DON'T REMEMBER THEM", CX, H * 0.68, GOLD, 38, pk(t, WT("sound", "arousals") - 0.3))
    else:
        bed(ctx, W * 0.36, H * 0.55, W * 0.42, t, eyes=1.0)
        big(ctx, "8 HOURS IN BED…", W * 0.66, H * 0.22, 70, WHITE, pk(t, s2))
        k = pk(t, WT("sound", "tired") - 0.3)
        x, y = W * 0.74, H * 0.44
        rrect(ctx, x - 110 * U, y - 50 * U, 220 * U, 100 * U, 16 * U); ctx.set_line_width(8 * U); rgba(ctx, WHITE, k); ctx.stroke()
        ctx.rectangle(x + 112 * U, y - 20 * U, 16 * U, 40 * U); rgba(ctx, WHITE, k); ctx.fill()
        rrect(ctx, x - 98 * U, y - 38 * U, 50 * U, 76 * U, 8 * U); rgba(ctx, CORAL, k * (0.6 + 0.4 * math.sin(t * 5))); ctx.fill()
        text(ctx, "STILL TIRED", x, H * 0.58, 46 * U, CORAL, k)

def loop_ring(ctx, x, y, r, a, b, col, k, t):
    if k <= 0: return
    ctx.new_path(); ctx.arc(x, y, r, 0, 2 * math.pi * ease(k)); ctx.set_line_width(10 * U); rgba(ctx, col, 0.9); ctx.stroke()
    ang = t * 1.2; circle(ctx, x + math.cos(ang) * r, y + math.sin(ang) * r, 14 * U, col, k)
    pill(ctx, a, x, y - r, col, 36, k, fg=DARK); pill(ctx, b, x, y + r, col, 36, k, fg=DARK)

def sc_habit(ctx, t, d):
    s1, s2 = ST("habit", 1), ST("habit", 2)
    night_bg(ctx, t, tint=GREEN)
    kicker(ctx, "STIMULUS CONTROL · BOOTZIN · 1972", pk(t, 0.3))
    if t < s1:
        big(ctx, "THE BRAIN LEARNS", CX, H * 0.30, 100, WHITE, pk(t, 0.8))
        big(ctx, "WHAT THE BED IS FOR", CX, H * 0.45, 90, GOLD, pk(t, WT("habit", "bed") - 0.4))
    else:
        loop_ring(ctx, W * 0.30, H * 0.42, H * 0.17, "BED", "SLEEP", GREEN, pk(t, s1 + 0.2), t)
        loop_ring(ctx, W * 0.70, H * 0.42, H * 0.17, "BED", "TV", CORAL, pk(t, WT("habit", "tv") - 0.4), t)
        if t >= s2: big(ctx, "SILENCE FEELS WRONG", CX, H * 0.72, 70, CORAL, pk(t, WT("habit", "wrong") - 0.3))

def sc_lonely(ctx, t, d):
    s1, s2, s3 = (ST("lonely", i) for i in range(1, 4))
    if t < s1:
        bedroom(ctx, t, tv_on=1.0, eyes=1.0)
        pill(ctx, "COVERING SILENCE?", W * 0.30, H * 0.10, (0.85, 0.85, 0.95), 40, pk(t, 0.5))
        pill(ctx, "OR LONELINESS?", W * 0.70, H * 0.10, PINK, 40, pk(t, WT("lonely", "loneliness") - 0.3))
    elif t < s2:
        night_bg(ctx, t, tint=PURPLE)
        kicker(ctx, "CACIOPPO ET AL. · PSYCHOLOGICAL SCIENCE · 2002", pk(t, s1))
        for i, (lab, gaps, col) in enumerate((("NOT LONELY", (), GREEN), ("LONELY", (0.22, 0.47, 0.63, 0.81), PURPLE))):
            y = H * (0.32 + i * 0.20); k = pk(t, s1 + 0.8 + i * 1.0, 1.2)
            text(ctx, lab, W * 0.16, y, 40 * U, WHITE, pk(t, s1 + 0.8 + i * 1.0))
            x0, w_ = W * 0.28, W * 0.60 * ease(k)
            rrect(ctx, x0, y - 30 * U, w_, 60 * U, 30 * U); rgba(ctx, col, 0.95); ctx.fill()
            for gx in gaps:
                if gx * W * 0.60 < w_: ctx.rectangle(x0 + gx * W * 0.60, y - 32 * U, 14 * U, 64 * U); rgba(ctx, (0.05, 0.05, 0.12), 1); ctx.fill()
        pill(ctx, "SAME HOURS · MORE BROKEN SLEEP", CX, H * 0.70, GOLD, 40, pk(t, WT("lonely", "broken") - 0.3))
    elif t < s3:
        night_bg(ctx, t, tint=GOLD)
        kicker(ctx, "KURINA ET AL. · SLEEP · 2011 · SOUTH DAKOTA", pk(t, s2))
        for i in range(6):   # communauté soudée : maisons et habitants rapprochés
            x = W * (0.20 + i * 0.12); k = pk(t, s2 + 0.3 + i * 0.15)
            ctx.new_path(); ctx.move_to(x - 60 * U, H * 0.42); ctx.line_to(x, H * 0.34); ctx.line_to(x + 60 * U, H * 0.42); ctx.close_path(); rgba(ctx, CORAL, k); ctx.fill()
            ctx.rectangle(x - 50 * U, H * 0.42, 100 * U, 80 * U); rgba(ctx, (0.95, 0.85, 0.65), k); ctx.fill()
            pictogram(ctx, x, H * 0.62, H * 0.10, GOLD if i != 3 else PURPLE, k)
        pill(ctx, "EVEN THERE: LONELY → MORE FRAGMENTED SLEEP", CX, H * 0.76, PURPLE, 34, pk(t, WT("lonely", "fragmented") - 0.3), fg=WHITE)
    else:
        night_bg(ctx, t, tint=PINK)
        big(ctx, "WHAT COMPANY", CX, H * 0.30, 100, WHITE, pk(t, s3))
        big(ctx, "DO YOU REALLY MISS?", CX, H * 0.44, 100, PINK, pk(t, WT("lonely", "miss") - 0.4))
        for i, ic in enumerate((ic_chat, ic_calendar)):
            bubble(ctx, W * (0.30 + i * 0.40), H * 0.64, 50 * U, pk(t, WT("lonely", "company", 1) - 0.2 + i * 0.3), ic)

def child_bed(ctx, t, tv_on, k=1.0):
    bed(ctx, W * 0.36, H * 0.58, W * 0.44, t, eyes=1.0 if tv_on else 0.0, blanket=(0.95, 0.55, 0.45), face_light=tv_on, a=k, zz=0.0 if tv_on else k)

def sc_kids(ctx, t, d):
    s1, s2 = ST("kids", 1), ST("kids", 2)
    if t < s1:
        vgrad(ctx, (0.10, 0.10, 0.26), (0.03, 0.03, 0.09))
        child_bed(ctx, t, 1.0)
        tv(ctx, W * 0.78, H * 0.36, W * 0.24, t, on=1.0, content=sitcom)
        light_cone(ctx, W * 0.70, H * 0.38, W * 0.26, H * 0.52, H * 0.14, a=0.22)
        pill(ctx, "TV IN THE BEDROOM", W * 0.78, H * 0.64, TVB, 38, pk(t, WT("kids", "bedroom") - 0.3), fg=DARK)
        pill(ctx, "LINKED TO SHORTER SLEEP", CX, H * 0.10, CORAL, 40, pk(t, WT("kids", "shorter") - 0.3), fg=WHITE)
    elif t < s2:
        night_bg(ctx, t, tint=GREEN)
        kicker(ctx, "AMERICAN ACADEMY OF PEDIATRICS", pk(t, s1))
        for i, (ic, lab) in enumerate(((ic_tv, "TV"), (None, "PHONE"), (None, "COMPUTER"))):
            x = W * (0.28 + i * 0.22); k = pk(t, WT("kids", ("tvs", "phones", "computers")[i]) - 0.3)
            circle(ctx, x, H * 0.36, 80 * U * ease(k), mix(CORAL, NAVY, 0.4), k)
            if ic: ic(ctx, x, H * 0.36, 44 * U * ease(k))
            elif lab == "PHONE": phone(ctx, x, H * 0.36, 40 * U * ease(k), t, None, k)
            else: rrect(ctx, x - 48 * U, H * 0.36 - 32 * U, 96 * U, 64 * U, 8 * U); rgba(ctx, TVB, k); ctx.fill()
            no_sign(ctx, x, H * 0.36, 95 * U, k)
            text(ctx, lab, x, H * 0.50, 34 * U, WHITE, k)
        pill(ctx, "OUT OF KIDS' BEDROOMS", CX, H * 0.14, GREEN, 42, pk(t, WT("kids", "bedrooms") - 0.3))
        pill(ctx, "SCREENS OFF ≈ 1 HOUR BEFORE BED", CX, H * 0.64, GOLD, 40, pk(t, WT("kids", "hour") - 0.3))
    else:
        vgrad(ctx, (0.14, 0.10, 0.24), (0.04, 0.03, 0.09))
        glow(ctx, W * 0.62, H * 0.34, 260 * U, (1.0, 0.8, 0.45), 0.5)
        child_bed(ctx, t, 0.0)
        pictogram(ctx, W * 0.66, H * 0.48, H * 0.22, (0.55, 0.45, 0.75))
        ebook(ctx, W * 0.62, H * 0.42, H * 0.06, False, 1.0)
        bubble(ctx, W * 0.72, H * 0.20, 46 * U, pk(t, WT("kids", "voice") - 0.3), ic_chat)
        pill(ctx, "A BEDTIME STORY", CX, H * 0.10, GOLD, 44, pk(t, s2))

def tip_head(ctx, n, title, col, k):
    neon_text(ctx, str(n), W * 0.08, H * 0.12, 90 * U, col, k, WHITE, fill=0.3)
    text(ctx, title, W * 0.13, H * 0.12, 54 * U, WHITE, k, align="l")

def timer(ctx, x, y, r, frac, label, k, col=GREEN):
    circle(ctx, x, y, r * ease(k), (0.08, 0.10, 0.20), k)
    ctx.new_path(); ctx.arc(x, y, r * 0.86, -math.pi / 2, -math.pi / 2 + 2 * math.pi * frac); ctx.set_line_width(18 * U); rgba(ctx, col, k); ctx.stroke()
    text(ctx, label, x, y, r * 0.42, WHITE, k)

def sc_tips_light(ctx, t, d):
    s1, s2 = ST("tips_light", 1), ST("tips_light", 2)
    night_bg(ctx, t, tint=GREEN)
    if t < s1:
        big(ctx, "WHAT HELPS?", CX, H * 0.36, 120, GREEN, pk(t, 0.4))
        pill(ctx, "NOT MEDICAL ADVICE", CX, H * 0.56, (0.85, 0.85, 0.95), 40, pk(t, WT("tips_light", "medical") - 0.3))
        return
    tip_head(ctx, 1, "KEEP THE VOICE, LOSE THE LIGHT", GREEN, pk(t, s1))
    if t < s2:
        for i, (lab, w_) in enumerate((("AUDIOBOOK", "audiobook"), ("PODCAST", "podcast"), ("SCREEN OFF", "screen"))):
            x = W * (0.24 + i * 0.26); k = pk(t, WT("tips_light", w_) - 0.3)
            if i < 2:
                circle(ctx, x, H * 0.42, 110 * U * ease(k), mix(GREEN, NAVY, 0.5), k)
                ctx.new_path(); ctx.arc(x, H * 0.42, 60 * U * ease(k), math.pi, 2 * math.pi); ctx.set_line_width(14 * U); rgba(ctx, WHITE, k); ctx.stroke()
                for sx in (-1, 1): rrect(ctx, x + sx * 60 * U - 16 * U, H * 0.42 - 10 * U, 32 * U, 54 * U, 10 * U); rgba(ctx, WHITE, k); ctx.fill()
            else:
                tv(ctx, x, H * 0.40, W * 0.16, t, on=0.0, stand=False)
                for j in range(3): bubble(ctx, x + (j - 1) * 50 * U, H * 0.25 - j * 10 * U, 22 * U, k * (0.6 + 0.4 * math.sin(t * 3 + j)), ic_chat)
            text(ctx, lab, x, H * 0.62, 40 * U, WHITE, k)
    else:
        k = pk(t, s2, 0.6); left = 30 - 30 * clamp((t - s2) / 6.0)
        timer(ctx, W * 0.36, H * 0.44, H * 0.20, left / 30, f"{int(left):02d}:00", k)
        pill(ctx, "SLEEP TIMER", W * 0.36, H * 0.72, GREEN, 42, k)
        for i, lab in enumerate(("FEWER HOURS OF LIGHT", "FEWER SUDDEN NOISES")):
            pill(ctx, lab, W * 0.72, H * (0.36 + i * 0.16), GOLD, 38, pk(t, WT("tips_light", "light", 1) - 0.4 + i * 0.6))

def fan(ctx, x, y, r, t, k):
    circle(ctx, x, y, r * ease(k), (0.85, 0.88, 0.95), k)
    for i in range(3):
        a_ = t * 9 + i * 2.094
        ctx.new_path(); ellipse(ctx, x + math.cos(a_) * r * 0.45, y + math.sin(a_) * r * 0.45, r * 0.42, r * 0.18, a_); rgba(ctx, (0.35, 0.55, 0.85), k); ctx.fill()
    circle(ctx, x, y, r * 0.12, (0.2, 0.2, 0.3), k)

def sc_tips_sound(ctx, t, d):
    s1 = ST("tips_sound", 1)
    night_bg(ctx, t, tint=CYAN)
    tip_head(ctx, 2, "IF YOU NEED SOUND: KEEP IT STEADY", CYAN, pk(t, 0.1))
    k1 = pk(t, 0.6); k2 = pk(t, s1 - 0.3)
    text(ctx, "TV", W * 0.12, H * 0.34, 40 * U, CORAL, k1)
    wave(ctx, W * 0.20, W * 0.66, H * 0.34, 34 * U, t, spiky=True, col=CORAL, k=k1)
    text(ctx, "FAN · RAIN · WHITE NOISE", W * 0.43, H * 0.50, 36 * U, CYAN, k2)
    wave(ctx, W * 0.20, W * 0.66, H * 0.60, 14 * U, t, spiky=False, col=CYAN, k=k2)
    fan(ctx, W * 0.82, H * 0.46, 110 * U, t, k2)
    pill(ctx, "MASKS SUDDEN SOUNDS", W * 0.43, H * 0.72, GOLD, 38, pk(t, WT("tips_sound", "mask") - 0.3))

def notepad(ctx, x, y, w, h, t, lines, k):
    rrect(ctx, x - w / 2, y - h / 2, w, h, 16 * U); rgba(ctx, (1.0, 0.96, 0.70), k); ctx.fill()
    for i in range(6): ctx.rectangle(x - w / 2, y - h / 2 + h * (0.22 + i * 0.13), w, 2 * U); rgba(ctx, (0.6, 0.7, 0.9), 0.6 * k); ctx.fill()
    for i, (s_, kk) in enumerate(lines):
        if kk <= 0: continue
        yy = y - h / 2 + h * (0.17 + i * 0.15)
        ctx.new_path(); rrect(ctx, x - w / 2 + 34 * U, yy - 16 * U, 32 * U, 32 * U, 6 * U); ctx.set_line_width(4 * U); rgba(ctx, DARK, kk); ctx.stroke()
        text(ctx, s_, x - w / 2 + 84 * U, yy, 40 * U, DARK, kk, align="l")

def sc_tips_list(ctx, t, d):
    s1, s2 = ST("tips_list", 1), ST("tips_list", 2)
    night_bg(ctx, t, tint=GOLD)
    tip_head(ctx, 3, "WRITE TOMORROW'S TO-DO LIST", GOLD, pk(t, 0.1))
    if t < s1:
        kicker(ctx, "SCULLIN ET AL. · BAYLOR UNIVERSITY · 2018", pk(t, WT("tips_list", "baylor") - 0.4), y=0.22)
        items = ("Call the dentist", "Email Sam the report", "Buy milk + eggs", "Book flights for May")
        notepad(ctx, W * 0.34, H * 0.48, W * 0.34, H * 0.42, t, [(s_, pk(t, min(WT("tips_list", "to-do"), 3.0) + i * 0.6, 0.4)) for i, s_ in enumerate(items)], pk(t, 0.6))
        pill(ctx, "5 MINUTES", W * 0.72, H * 0.40, GOLD, 50, pk(t, WT("tips_list", "five") - 0.3))
        pill(ctx, "VS. A LIST OF THINGS ALREADY DONE", W * 0.72, H * 0.56, (0.85, 0.85, 0.95), 32, pk(t, WT("tips_list", "already") - 0.3))
    else:
        for i, (lab, frac, col) in enumerate((("“DONE” LIST", 1.0, (0.6, 0.62, 0.75)), ("TO-DO LIST", 0.62, GOLD))):
            y = H * (0.34 + i * 0.18); k = pk(t, s1 + 0.3 + i * 0.6, 0.8)
            text(ctx, lab, W * 0.18, y, 40 * U, WHITE, k)
            rrect(ctx, W * 0.30, y - 30 * U, W * 0.50 * frac * ease(k), 60 * U, 30 * U); rgba(ctx, col, 0.95); ctx.fill()
        text(ctx, "TIME TO FALL ASLEEP →", W * 0.55, H * 0.56, 32 * U, (0.85, 0.88, 1.0), pk(t, s1 + 1.0))
        big(ctx, "≈ 9 MIN FASTER", W * 0.70, H * 0.20, 80, GOLD, pk(t, WT("tips_list", "nine") - 0.3))
        if t >= s2: pill(ctx, "“IT'S HANDLED.”", CX, H * 0.70, GREEN, 46, pk(t, WT("tips_list", "handled") - 0.3))

def sc_tips_breath(ctx, t, d):
    s1, s2 = ST("tips_breath", 1), ST("tips_breath", 2)
    night_bg(ctx, t, tint=PURPLE)
    tip_head(ctx, 4, "CALM THE BODY: CYCLIC SIGHING", PURPLE, pk(t, 0.1))
    if t < s2:
        kicker(ctx, "BALBAN ET AL. · STANFORD · CELL REPORTS MEDICINE · 2023", pk(t, 0.6), y=0.22)
        # cycle : 2 inspirations (nez) puis une longue expiration
        cyc = 8.0; ph = (t % cyc) / cyc
        if ph < 0.18: r = 0.55 + 0.30 * ease(ph / 0.18); lab = "INHALE"
        elif ph < 0.30: r = 0.85 + 0.15 * ease((ph - 0.18) / 0.12); lab = "+ A 2ND SIP"
        else: r = 1.0 - 0.45 * ease((ph - 0.30) / 0.70); lab = "LONG, SLOW EXHALE"
        k = pk(t, 0.8)
        glow(ctx, W * 0.34, H * 0.48, H * 0.30 * r, PURPLE, 0.45 * k)
        circle(ctx, W * 0.34, H * 0.48, H * 0.20 * r, mix(PURPLE, WHITE, 0.25), 0.9 * k)
        text(ctx, lab, W * 0.34, H * 0.74, 44 * U, WHITE, k)
        pill(ctx, "5 MIN A DAY", W * 0.72, H * 0.38, GOLD, 46, pk(t, WT("tips_breath", "five") - 0.3))
        if t >= s1:
            pill(ctx, "BETTER MOOD", W * 0.72, H * 0.52, GREEN, 40, pk(t, WT("tips_breath", "mood") - 0.3))
            pill(ctx, "SLOWER BREATHING", W * 0.72, H * 0.64, CYAN, 40, pk(t, WT("tips_breath", "breathing") - 0.3), fg=DARK)
    else:
        k = pk(t, s2, 0.6)
        for i in range(6):
            x = W * (0.20 + i * 0.12); y = H * (0.44 + 0.06 * math.sin(i * 1.3 + t * 0.8))
            circle(ctx, x, y, 26 * U, GOLD, k); ctx.new_path(); ctx.move_to(x + 24 * U, y); ctx.line_to(x + 24 * U, y - 90 * U); ctx.set_line_width(7 * U); rgba(ctx, GOLD, k); ctx.stroke()
        pill(ctx, "SLOW, STEADY MUSIC", CX, H * 0.24, GOLD, 46, k)
        pill(ctx, "SLOWER BREATHING & HEART RATE", CX, H * 0.68, CORAL, 40, pk(t, WT("tips_breath", "heart") - 0.3), fg=WHITE)

def lamp(ctx, x, y, s, k):
    glow(ctx, x, y - s * 0.6, s * 2.6, (1.0, 0.78, 0.40), 0.45 * k)
    ctx.new_path(); ctx.move_to(x - s * 0.5, y - s * 0.3); ctx.line_to(x + s * 0.5, y - s * 0.3); ctx.line_to(x + s * 0.3, y - s); ctx.line_to(x - s * 0.3, y - s); ctx.close_path(); rgba(ctx, (1.0, 0.86, 0.60), k); ctx.fill()
    ctx.rectangle(x - s * 0.05, y - s * 0.3, s * 0.1, s * 0.9); rgba(ctx, (0.4, 0.3, 0.25), k); ctx.fill()

def sc_tips_bed(ctx, t, d):
    s1, s2 = ST("tips_bed", 1), ST("tips_bed", 2)
    night_bg(ctx, t, tint=GREEN)
    tip_head(ctx, 5, "PROTECT THE BED", GREEN, pk(t, 0.1))
    if t < s1:
        bed(ctx, W * 0.30, H * 0.52, W * 0.34, t, eyes=1.0)
        pill(ctx, "BED = SLEEP ONLY", W * 0.30, H * 0.26, GREEN, 40, pk(t, WT("tips_bed", "only") - 0.3))
        k = pk(t, WT("tips_bed", "twenty") - 0.4)
        timer(ctx, W * 0.64, H * 0.42, H * 0.12, ease(k) * 0.33, "20 MIN", k, CORAL)
        k2 = pk(t, WT("tips_bed", "dim") - 0.4)
        lamp(ctx, W * 0.84, H * 0.56, 90 * U, k2)
        pictogram(ctx, W * 0.78, H * 0.62, H * 0.16, (0.85, 0.75, 0.55), k2)
        pill(ctx, "GET UP · CALM · DIM LIGHT", W * 0.74, H * 0.74, GOLD, 34, k2)
    elif t < s2:
        for i, mn in enumerate((60, 45, 30)):
            k = pk(t, s1 + 0.1 + i * 0.8, 0.5)
            timer(ctx, W * (0.26 + i * 0.24), H * 0.42, H * 0.12, mn / 60, f"{mn} MIN", k, (GOLD, CYAN, GREEN)[i])
            if i < 2: arrow(ctx, W * (0.33 + i * 0.24), H * 0.42, W * (0.43 + i * 0.24), H * 0.42, WHITE, k)
        pill(ctx, "NO COLD TURKEY: GO STEP BY STEP", CX, H * 0.66, GOLD, 40, pk(t, WT("tips_bed", "turkey") - 0.3))
    else:
        k = pk(t, s2, 0.6)
        rrect(ctx, W * 0.16, H * 0.26, W * 0.68, H * 0.38, 28 * U); rgba(ctx, (0.02, 0.03, 0.08), 0.7 * k); ctx.fill()
        text(ctx, "AWAKE MOST NIGHTS FOR WEEKS?", CX, H * 0.36, 52 * U, WHITE, k)
        big(ctx, "TALK TO A DOCTOR", CX, H * 0.48, 80, GREEN, pk(t, WT("tips_bed", "doctor") - 0.4))
        text(ctx, "Insomnia is common, and it's treatable.", CX, H * 0.58, 38 * U, (0.85, 0.9, 1.0), pk(t, WT("tips_bed", "treatable") - 0.5))

def sc_outro(ctx, t, d):
    s1, s2, s3, s4 = (ST("outro", i) for i in range(1, 5))
    if t < s3:
        bedroom(ctx, t, tv_on=1.0 - pk(t, s2 + 4.0, 1.5), eyes=0.0, zz=1.0, content=sitcom)
        if t < s1: pill(ctx, "NOT THE PROBLEM · A SOLUTION", CX, H * 0.08, GOLD, 42, pk(t, 0.3))
        elif t < s2: pill(ctx, "SILENCE = LOUD THOUGHTS · VOICE = COMPANY", CX, H * 0.08, CYAN, 38, pk(t, s1), fg=DARK)
        else:
            pill(ctx, "KEEP: THE VOICE, THE COMFORT", W * 0.30, H * 0.08, GREEN, 36, pk(t, WT("outro", "keep") - 0.3))
            pill(ctx, "DROP: LIGHT, NOISE, HOURS", W * 0.72, H * 0.08, CORAL, 36, pk(t, WT("outro", "drop") - 0.3), fg=WHITE)
    elif t < s4:
        night_bg(ctx, t, tint=PURPLE)
        big(ctx, "DO YOU SLEEP", CX, H * 0.30, 110, WHITE, pk(t, s3))
        big(ctx, "WITH THE TV ON?", CX, H * 0.45, 110, GOLD, pk(t, s3 + 0.5))
        pill(ctx, "WHAT DO YOU WATCH? TELL ME BELOW", CX, H * 0.64, CYAN, 42, pk(t, WT("outro", "watch") - 0.3), fg=DARK)
    else:
        night_bg(ctx, t, tint=GOLD)
        cta(ctx, t - s4, d - s4, "WHAT DO YOU WATCH?", "TELL ME IN THE COMMENTS")

SCENES = {k[3:]: v for k, v in list(globals().items()) if k.startswith("sc_") and callable(v)}
SHORT_SCENES = ["intro"]   # (pas de Short tiré de cette vidéo pour l'instant)

def thumbnail(c):
    """Miniature 1280×720 : le dormeur éveillé éclairé par l'écran (à droite) + « WHY YOU NEED THE TV ON » (à gauche)."""
    vgrad(c, (0.09, 0.10, 0.26), (0.03, 0.03, 0.09))
    c.rectangle(0, H * 0.80, W, H * 0.20); rgba(c, (0.07, 0.06, 0.11), 1); c.fill()
    moon(c, W * 0.60, H * 0.14, 26 * U)
    tv(c, W * 0.83, H * 0.30, W * 0.28, 1.0, on=1.0, content=sitcom, flicker=False)
    light_cone(c, W * 0.74, H * 0.33, W * 0.54, H * 0.62, H * 0.18, a=0.32)
    bed(c, W * 0.72, H * 0.72, W * 0.50, 1.0, eyes=1.0, face_light=1.0)
    g = cairo.LinearGradient(0, 0, W * 0.55, 0); g.add_color_stop_rgba(0, 0.01, 0.01, 0.05, 0.85); g.add_color_stop_rgba(1, 0.01, 0.01, 0.05, 0.0)
    c.rectangle(0, 0, W, H); c.set_source(g); c.fill()
    def tx(s_, x, y, sz, col):
        c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(sz)
        c.move_to(x + 6, y + 7); c.set_source_rgba(0, 0, 0, 0.85); c.show_text(s_)
        c.move_to(x, y); c.set_source_rgb(*col); c.show_text(s_)
    tx("WHY YOU", 50, 185, 118, (1, 1, 1))
    tx("NEED THE", 50, 318, 118, (1, 1, 1))
    tx("TV ON", 50, 470, 158, GOLD)
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(44)
    w_ = c.text_extents("THE PSYCHOLOGY").width
    c.set_source_rgb(0.85, 0.12, 0.12); c.rectangle(50, 548, w_ + 50, 76); c.fill(); tx("THE PSYCHOLOGY", 75, 602, 44, (1, 1, 1))
