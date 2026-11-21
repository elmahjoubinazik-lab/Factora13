exec(open("engine/photo.py", encoding="utf-8").read())   # frame(), paint(), poster_text()
# Épisode 044b — version Runway de « Why Doesn't Your Stomach Digest Itself? » (brief de Nazik, 2026-11-21).
# 3 plans Gen-4.5 image→vidéo générés À PARTIR de nos illustrations vérifiées (ép. 044, sans texte) ; même voix, même
# musique ; par-dessus : sous-titres (moteur), « Simplified illustration », légendes calées sur les couches suivies image par
# image (track_layers.py → build/layers.json), accroche écrite, nom FACTORA + CTA texte sur les 2,5 dernières secondes.
import json as _json
_TLL = _json.load(open(EP + "/build/timeline.json", encoding="utf-8"))
_TL = {sg["scene"]: sg for sg in _TLL}
_FIRST = _TLL[0]["scene"]
_WORDS = [w for sg in _TLL for se in sg["sents"] for w in se.get("words", [])]
END_T = _TLL[-1]["end"] + 0.6
def WT(word, n=0):
    hits = [w[1] for w in _WORDS if w[0].lower().strip(".,?!") == word.lower()]
    return hits[n] if n < len(hits) else 1e9
try:
    LAYERS = _json.load(open(EP + "/build/layers.json"))
except Exception:
    LAYERS = {}
DARK = (0.03, 0.02, 0.08)

def tag(ctx, s, a=1.0):
    font(ctx, 38 * U); w_ = ctx.text_extents(s).width + 48 * U
    x0, y0 = W * 0.055, H * 0.083
    rrect(ctx, x0, y0 - 30 * U, w_, 60 * U, 30 * U); rgba(ctx, (0.0, 0.0, 0.0), 0.55 * a); ctx.fill()
    text(ctx, s, x0 + 24 * U, y0, 38 * U, (0.94, 0.96, 1.0), 0.95 * a, align="l")

def label2(ctx, main, sub, x, y, col, k=1.0, a=1.0):
    if k <= 0 or a <= 0: return
    sc_ = 0.7 + 0.3 * ease(k) + 0.06 * math.sin(math.pi * clamp(k))
    ctx.save(); ctx.translate(x, y); ctx.scale(sc_, sc_)
    font(ctx, 46 * U); w1 = ctx.text_extents(main).width; font(ctx, 29 * U); w2 = ctx.text_extents(sub).width
    w_ = max(w1, w2) + 56 * U; h_ = 108 * U
    rrect(ctx, -w_ / 2, -h_ / 2, w_, h_, 24 * U); rgba(ctx, (0.02, 0.03, 0.09), 0.88 * a * ease(k)); ctx.fill()
    rrect(ctx, -w_ / 2, -h_ / 2, w_, h_, 24 * U); ctx.set_line_width(5 * U); rgba(ctx, col, a * ease(k)); ctx.stroke()
    text(ctx, main, 0, -17 * U, 46 * U, col, a * ease(k))
    text(ctx, sub, 0, 29 * U, 29 * U, (0.92, 0.94, 1.0), 0.9 * a * ease(k), bold=False)
    ctx.restore()

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

def layer_y(clip, key, t):
    """Position (fraction de H) d'une couche dans le plan `clip` au temps local t de ce plan (suivi image par image)."""
    v = LAYERS.get(clip, {}).get(key) or []
    if not v: return None
    i = max(0, min(len(v) - 1, int(t * 30)))
    return v[i]

T_ZOOM0 = WT("itself") - 0.05
T_CTA = END_T - 2.5
LAB_X = W * 0.34
def overlays(ctx, T, clip, tl):
    tag(ctx, "Simplified illustration")
    ka = 1 - prog(T, T_ZOOM0 + 0.1, T_ZOOM0 + 0.5)          # accroche écrite
    if ka > 0:
        g = cairo.LinearGradient(0, 0, 0, H * 0.25); g.add_color_stop_rgba(0, 0.01, 0.01, 0.04, 0.55 * ka); g.add_color_stop_rgba(1, 0, 0, 0, 0)
        ctx.set_source(g); ctx.rectangle(0, 0, W, H * 0.25); ctx.fill()
        ctx.push_group(); poster_text(ctx, "WHY NOT", W * 0.46, H * 0.140, 146 * U, WHITE, W * 0.80); poster_text(ctx, "ITSELF?", W * 0.46, H * 0.203, 146 * U, GOLD, W * 0.80)
        ctx.pop_group_to_source(); ctx.paint_with_alpha(ka)
    if clip in ("barrier", "mix"):                       # légendes posées sur les couches suivies
        k1 = prog(T, WT("mucus") - 0.05, WT("mucus") + 0.30); k2 = prog(T, WT("stomach", 1) - 0.05, WT("stomach", 1) + 0.30)
        ym = layer_y(clip, "muc", tl); ys = layer_y(clip, "mus", tl)
        if ym is not None: label2(ctx, "MUCUS BARRIER", "made by the lining", LAB_X, H * ym, CYAN, k1)
        if ys is not None: label2(ctx, "STOMACH WALL", "living tissue", LAB_X, H * ys, (1.0, 0.62, 0.70), k2)
    kc = prog(T, T_CTA, T_CTA + 0.35)                    # fin : petit nom + CTA texte (sans bouton)
    if kc > 0:
        font(ctx, 44 * U); txt = "FACTORA"; w_ = ctx.text_extents(txt).width + 56 * U
        rrect(ctx, W * 0.46 - w_ / 2, H * 0.127 - 32 * U, w_, 64 * U, 32 * U); rgba(ctx, (0, 0, 0), 0.45 * kc); ctx.fill()
        text(ctx, txt, W * 0.46, H * 0.127, 44 * U, GOLD, kc)
        cta_lines(ctx, ("Follow Factora for more", "body mysteries."), W * 0.46, (H * 0.168, H * 0.200), 54, kc)

def _abs(scene, t): return (0.0 if scene == _FIRST else _TL[scene]["start"]) + t
def _scene(scene, clip, off=0.0):
    def sc(ctx, t, d):
        tl = (1.0 if (scene == _FIRST and TNOW < 2.0 / FPS) else t) + off
        paint(ctx, frame(clip, tl), zoom=1.0 / 1.03)
        overlays(ctx, _abs(scene, t if not (scene == _FIRST and TNOW < 2.0 / FPS) else 1.0), clip, tl)
    return sc
SHORT_SCENES = ["hook", "barrier", "mix", "close"]
SCENES = dict(hook=_scene("hook", "hook"), barrier=_scene("barrier", "barrier"), mix=_scene("mix", "mix"),
              close=_scene("close", "mix", _TL["close"]["start"] - _TL["mix"]["start"]))
