# Episode 024 (Short only) - "Hand dryer or paper towel: which is cleaner?" — VERSION IA (2026-11-10)
# Images animées générées avec Runway (demande de Nazik : qualité d'image type ChatGPT, DA Factora : carrelage bleu-vert
# brillant, spots dorés, inox brossé, bactéries vert néon). Clips bruts : build/rw/*.mp4 ; découpe : prep_clips.sh.
# Le moteur ajoute par-dessus : accroche, sous-titres, titres et sources, musique « hype », whooshes, CTA chouette.
# >>> À la publication : containsSyntheticMedia = true + « Created with AI tools » (description et légendes). <<<
# Facts: UConn (AEM 2018: hot-air dryers deposit restroom bacteria on hands, HEPA ~4x fewer), Leeds (J Hosp Infect 2014,
# funded by the European Tissue Symposium: ~27x more airborne germs near jet dryers), CDC (towel or dryer both OK; dry hands fully).
# Ancienne version vectorielle : scenes_vector.py.
import numpy as _np
from PIL import Image as _Img

GERMC = (0.35, 0.95, 0.45)
CLIPS = os.path.join(EP, "build", "clips")
KEY2 = os.path.join(EP, "build", "rw", "key2.png")      # image fixe 1536x2752 (sèche-mains à gauche, distributeur à droite)
_IMG = {}
_NF = {}

def _load(path):
    if path in _IMG: return _IMG[path][0]
    if len(_IMG) > 12: _IMG.clear()
    a = _np.asarray(_Img.open(path).convert("RGB")); h, w = a.shape[:2]
    buf = _np.empty((h, w, 4), _np.uint8); buf[..., 0] = a[..., 2]; buf[..., 1] = a[..., 1]; buf[..., 2] = a[..., 0]; buf[..., 3] = 255
    surf = cairo.ImageSurface.create_for_data(memoryview(buf), cairo.FORMAT_ARGB32, w, h, w * 4)
    _IMG[path] = (surf, buf)
    return surf

def frame(name, t):
    """Image du clip `name` au temps local t (images déjà recalées à 30 i/s sur la durée de la scène)."""
    if name not in _NF: _NF[name] = len([f for f in os.listdir(os.path.join(CLIPS, name)) if f.endswith(".jpg")])
    i = max(1, min(_NF[name], int(t * 30) + 1))
    return _load(os.path.join(CLIPS, name, f"{i:04d}.jpg"))

def paint(ctx, surf, fx=0.5, fy=0.5, zoom=1.0, a=1.0):
    """Peint l'image pour couvrir tout le cadre ; (fx, fy) = point de l'image placé au centre (bornés : jamais de bord noir)."""
    sw, sh = surf.get_width(), surf.get_height()
    s = max(W / sw, H / sh) * zoom * 1.03
    fx = min(max(fx, CX / (sw * s)), 1 - CX / (sw * s)); fy = min(max(fy, CY / (sh * s)), 1 - CY / (sh * s))
    ctx.save(); ctx.translate(CX, CY); ctx.scale(s, s); ctx.translate(-fx * sw, -fy * sh)
    ctx.set_source_surface(surf, 0, 0); ctx.get_source().set_filter(cairo.FILTER_GOOD)
    ctx.paint_with_alpha(a); ctx.restore()

def scrim(ctx, y1=0.22, a=0.78):
    """Dégradé sombre en haut de l'image : titres lisibles sur la photo."""
    g = cairo.LinearGradient(0, 0, 0, H * y1); g.add_color_stop_rgba(0, 0, 0.01, 0.02, a); g.add_color_stop_rgba(1, 0, 0.01, 0.02, 0)
    ctx.rectangle(0, 0, W, H * y1); ctx.set_source(g); ctx.fill()

def label(ctx, s, x, y, size, col, a):
    if a <= 0: return
    font(ctx, size); e = ctx.text_extents(s)
    rrect(ctx, x - e.width / 2 - 30 * U, y - size * 0.75, e.width + 60 * U, size * 1.5, size * 0.5); rgba(ctx, (0.02, 0.02, 0.04), 0.80 * a); ctx.fill()
    text(ctx, s, x, y, size, col, a)

def check(ctx, x, y, s, a, col=GREEN):
    if a <= 0: return
    glow(ctx, x, y, 110 * s * U, col, 0.45 * a)
    circle(ctx, x, y, 62 * s * U, (0.02, 0.05, 0.03), 0.75 * a)
    ctx.move_to(x - 30 * s * U, y); ctx.line_to(x - 8 * s * U, y + 24 * s * U); ctx.line_to(x + 36 * s * U, y - 27 * s * U)
    ctx.set_line_width(13 * s * U); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_join(cairo.LINE_JOIN_ROUND); rgba(ctx, col, a); ctx.stroke()

def with_cam(fn, push=0.04, punch=0.06):
    """Léger push-in + « coup de zoom » à l'entrée de la scène (dynamisme)."""
    def sc(ctx, t, d):
        z = (1 + push * clamp(t / max(d, 0.1))) * (1 + punch * math.exp(-t * 9))
        ctx.save(); ctx.translate(CX, CY); ctx.scale(z, z); ctx.translate(-CX, -CY)
        fn(ctx, t, d)
        ctx.restore()
    return sc

# ---------------------------------------------------------------- scenes (fonds filmés)
def _hook_bg(ctx, t, d):
    # 2 premières images (vignette Instagram/TikTok) : plan large, bactéries dans le jet, mains mouillées
    paint(ctx, frame("hook", 1.2 if TNOW < 2.0 / FPS else t))

def _vs_bg(ctx, t, d):
    paint(ctx, frame("vs", t), 0.5, 0.52, 1.0)

def _dryer_bg(ctx, t, d):
    paint(ctx, frame("dryer", t))
    scrim(ctx, 0.20)

J1 = 4.4    # jet : « But the paper industry funded it. » commence ici
def _jet_bg(ctx, t, d):
    if t < J1:
        paint(ctx, frame("jet", t))
    else:   # gros plan sur le distributeur de papier, le tampon tombe dessus
        k = clamp((t - J1) / (d - J1))
        paint(ctx, _load(KEY2), 0.80, 0.54, 2.1 + 0.3 * k)
        rgba(ctx, (0, 0, 0.02), 0.30); ctx.paint()
    scrim(ctx, 0.24, 0.85)

V1 = 1.7    # verdict : « The CDC says both work. » sur l'image fixe, puis le clip serviette
def _verdict_bg(ctx, t, d):
    if t < V1:
        paint(ctx, _load(KEY2), 0.5, 0.54, 1.0 + 0.03 * t)
    else:
        paint(ctx, frame("verdict", t - V1))
    scrim(ctx, 0.20)

# ---------------------------------------------------------------- overlays (titres, chiffres, sources)
def _vs_fx(ctx, t, d):
    s = 1 + 0.08 * math.sin(t * 8)
    ctx.save(); ctx.translate(CX, H * 0.47); ctx.scale(s, s); label(ctx, "VS", 0, 0, 110 * U, GOLD, prog(t, 0.3, 0.5)); ctx.restore()
    label(ctx, "WHICH IS CLEANER?", CX, H * 0.25, 78 * U, WHITE, prog(t, 0.5, 0.8))

def _dryer_fx(ctx, t, d):
    label(ctx, "BATHROOM AIR IN → ONTO YOUR HANDS", CX, H * 0.06, 44 * U, GERMC, prog(t, 0, 0.25))
    label(ctx, "UNIVERSITY OF CONNECTICUT, 2018", CX, H * 0.105, 36 * U, (0.9, 0.95, 1.0), prog(t, d * 0.3, d * 0.45))

def _jet_fx(ctx, t, d):
    k = prog(t, 0.1, d * 0.42)
    sc_ = 1 + 0.06 * math.sin(t * 8) + 0.25 * math.exp(-((t - d * 0.42) * 6) ** 2)
    ctx.save(); ctx.translate(CX, H * 0.085); ctx.scale(sc_, sc_)
    neon_text(ctx, f"{int(round(27 * k))}× MORE", 0, 0, 150 * U, GERMC, prog(t, 0.05, 0.25), CYAN, fill=0.35); ctx.restore()
    label(ctx, "AIRBORNE GERMS NEAR JET DRYERS", CX, H * 0.155, 46 * U, WHITE, prog(t, 0.2, 0.45))
    fk = prog(t, J1, J1 + 0.18)
    if fk:
        ctx.save(); ctx.translate(CX, H * 0.47); ctx.rotate(-0.08); ctx.scale(1 + 0.6 * (1 - fk), 1 + 0.6 * (1 - fk))
        font(ctx, 54 * U); w_ = ctx.text_extents("FUNDED BY THE PAPER INDUSTRY").width + 70 * U
        rrect(ctx, -w_ / 2, -56 * U, w_, 112 * U, 20 * U); rgba(ctx, (0, 0, 0), 0.72 * fk); ctx.fill()
        rrect(ctx, -w_ / 2, -56 * U, w_, 112 * U, 20 * U); ctx.set_line_width(8 * U); rgba(ctx, GOLD, fk); ctx.stroke()
        text(ctx, "FUNDED BY THE PAPER INDUSTRY", 0, 0, 54 * U, GOLD, fk); ctx.restore()
        label(ctx, "UNIVERSITY OF LEEDS, 2014", CX, H * 0.555, 38 * U, (0.9, 0.95, 1.0), fk)

def _verdict_fx(ctx, t, d):
    if t < V1:
        check(ctx, W * 0.17, H * 0.37, 1.5, prog(t, 0.15, 0.4)); check(ctx, W * 0.83, H * 0.37, 1.5, prog(t, 0.45, 0.7))
        label(ctx, "CDC: BOTH WORK", CX, H * 0.09, 76 * U, GREEN, prog(t, 0, 0.25))
    else:
        label(ctx, "DRY THEM COMPLETELY", CX, H * 0.07, 70 * U, GOLD, prog(t, V1, V1 + 0.25))
        label(ctx, "WET HANDS SPREAD GERMS MORE EASILY", CX, H * 0.125, 42 * U, WHITE, prog(t, d * 0.62, d * 0.75))

def scene(bg, fx, push=0.04, punch=0.06):
    cam = with_cam(bg, push, punch)
    def sc(ctx, t, d):
        cam(ctx, t, d)
        if fx: fx(ctx, t, d)
    return sc

def _outro(ctx, t, d):
    paint(ctx, _load(os.path.join(CLIPS, "outro_bg.jpg")), zoom=1.0 + 0.02 * t)   # rappel flou de la 1re image (boucle)
    rgba(ctx, (0.02, 0.03, 0.10), 0.55); ctx.paint()
    cta(ctx, t, d, "TEAM TOWEL OR TEAM DRYER?", "COMMENT BELOW")

SHORT_SCENES = ["hook", "vs", "dryer", "jet", "verdict", "outro"]
SCENES = dict(hook=scene(_hook_bg, None, 0.05, 0.08), vs=scene(_vs_bg, _vs_fx), dryer=scene(_dryer_bg, _dryer_fx),
              jet=scene(_jet_bg, _jet_fx, 0.04, 0.08), verdict=scene(_verdict_bg, _verdict_fx), outro=_outro)

def thumbnail(c):
    vgrad(c, (0.10, 0.20, 0.24), (0.02, 0.05, 0.07))
    thumb_text(c, "HAND DRYER", "OR PAPER TOWEL?", "SCIENCE")

def cover(ctx):
    """Affiche : l'image IA de l'accroche (sèche-mains, jet de bactéries, mains mouillées) + titre en 3 couleurs, pastille, bandeau."""
    paint(ctx, _load(os.path.join(EP, "build", "rw", "key1.png")))
    scrim(ctx, 0.34, 0.92)
    for dx, dy, col, a in ((9, 11, (0, 0, 0), 0.7), (0, 0, None, 1.0)):
        text(ctx, "IS YOUR DRYER", CX + dx * U, H * 0.075 + dy * U, 118 * U, col or WHITE, a)
        text(ctx, "BLOWING THIS", CX + dx * U, H * 0.15 + dy * U, 128 * U, col or GERMC, a)
        text(ctx, "ON YOU?", CX + dx * U, H * 0.225 + dy * U, 150 * U, col or GOLD, a)
    ctx.save(); ctx.translate(W * 0.83, H * 0.46); ctx.rotate(0.18)
    circle(ctx, 0, 0, 140 * U, CORAL, 1.0)
    ctx.new_path(); ctx.arc(0, 0, 140 * U, 0, 2 * math.pi); ctx.set_line_width(8 * U); rgba(ctx, WHITE, 0.9); ctx.stroke()
    text(ctx, "27×", 0, -22 * U, 104 * U, WHITE, 1.0); text(ctx, "MORE GERMS?", 0, 58 * U, 34 * U, WHITE, 1.0)
    ctx.restore()
    rrect(ctx, CX - 470 * U, H * 0.94 - 58 * U, 940 * U, 116 * U, 58 * U); rgba(ctx, (0.02, 0.03, 0.05), 0.88); ctx.fill()
    rrect(ctx, CX - 470 * U, H * 0.94 - 58 * U, 940 * U, 116 * U, 58 * U); ctx.set_line_width(6 * U); rgba(ctx, GOLD, 1); ctx.stroke()
    text(ctx, "TOWEL OR DRYER?", CX, H * 0.94, 66 * U, GOLD)
