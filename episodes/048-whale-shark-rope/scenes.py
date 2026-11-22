exec(open("engine/photo.py", encoding="utf-8").read())
# Épisode 048, version Runway (demande de Nazik, 2026-11-22 : « utilise Runway pour illustrer la baleine et le plongeur…
# des images un peu plus réalistes… mets-y plus d'émotion » ; mention à l'écran : « Illustration » seulement).
# Images clés nano-banana-pro (requin-baleine pris dans la corde, nageoire entaillée, plongeur sans visage visible, gros plan
# sur l'œil, départ libre) ; clips gen-4.5 de 5 s. Faits : voir scenes_vector.py et meta_en.json → sources (Hawaii News Now,
# KHON2). Voix émotionnelle : indications de ton ElevenLabs entre crochets (retirées des sous-titres par tts.py).
import json as _json

_TLL = _json.load(open(EP + "/build/timeline.json", encoding="utf-8"))
_TL = {sg["scene"]: sg for sg in _TLL}
_FIRST = _TLL[0]["scene"]
_WORDS = [w for sg in _TLL for se in sg["sents"] for w in se.get("words", [])]
def WT(word, n=0):
    hits = [w[1] for w in _WORDS if w[0].lower().strip(".,?!:") == word.lower()]
    return hits[n] if n < len(hits) else 1e9
def S0(scene): return 0.0 if scene == _FIRST else _TL[scene]["start"]
END_T = _TLL[-1]["end"] + 0.6
DARK = (0.02, 0.03, 0.08)

def tag(ctx, s="Illustration", y=0.083, a=1.0):
    if a <= 0: return
    font(ctx, 32 * U); w_ = ctx.text_extents(s).width + 40 * U
    x0, y0 = W * 0.055, H * y
    rrect(ctx, x0, y0 - 25 * U, w_, 50 * U, 25 * U); rgba(ctx, (0.0, 0.0, 0.0), 0.50 * a); ctx.fill()
    text(ctx, s, x0 + 20 * U, y0, 32 * U, (0.92, 0.94, 1.0), 0.92 * a, align="l")

def pill(ctx, s, x, y, col, size=50, a=1.0, k=1.0):
    if a <= 0 or k <= 0: return
    sc_ = 0.6 + 0.4 * ease(k) + 0.08 * math.sin(math.pi * clamp(k))
    ctx.save(); ctx.translate(x, y); ctx.scale(sc_, sc_)
    font(ctx, size * U); w_ = ctx.text_extents(s).width + 64 * U; h_ = size * 1.6 * U
    glow(ctx, 0, 0, w_ * 0.7, col, 0.35 * a)
    rrect(ctx, -w_ / 2, -h_ / 2, w_, h_, h_ / 2); rgba(ctx, col, 0.97 * a); ctx.fill()
    text(ctx, s, 0, 0, size * U, DARK, a)
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

def still(ctx, name, t, d, z0=1.0, z1=1.08, fx=0.5, fy=0.5):
    """Image clé fixe avec un zoom lent (Ken Burns)."""
    paint(ctx, load_img(os.path.join(RW, name)), fx, fy, lerp(z0, z1, clamp(t / max(d, 0.1))))

def lerp(a, b, k): return a + (b - a) * k

# ---------------------------------------------------------------- scènes (temps local t, absolu T = S0 + t)
T_R0 = WT("came") - 0.05                      # début du sauvetage (le plongeur arrive)
T_R1 = WT("later") - 0.10                     # « Thirty minutes later » : le chronomètre s'arrête à 30:00
def rescue_clock(ctx, T):
    """Chronomètre du sauvetage (durée de toute l'intervention, pas une immobilité de 30 min) ; 0 → 30:00."""
    if T < T_R0 or T > WT("free", 1) + 0.2: return
    k = prog(T, T_R0, T_R1)
    secs = int(round(1800 * (k ** 1.15)))
    a = 1.0 - prog(T, WT("way") + 0.3, WT("free", 1))
    glow(ctx, W * 0.46, H * 0.60, 150 * U, GOLD, 0.28 * a)
    text(ctx, "RESCUE", W * 0.46, H * 0.555, 40 * U, WHITE, 0.9 * a)
    ctx.push_group(); poster_text(ctx, f"{secs // 60:02d}:{secs % 60:02d}", W * 0.46, H * 0.615, 120 * U, GOLD); ctx.pop_group_to_source(); ctx.paint_with_alpha(a)

def ov_hook(ctx, t, d):
    scrim(ctx, 0.26, 0.55)
    poster_text(ctx, "TRAPPED", W * 0.46, H * 0.145, 190 * U, CORAL, W * 0.80)
    tag(ctx)
_hook = clip_scene("hook", ov_hook, push=0.03, punch=0.0, cover_t=0.4)

def sc_wound(ctx, t, d):
    T = S0("wound") + t
    if T < WT("she", 0) - 0.12:                  # la nageoire entaillée
        still(ctx, "key_wound.png", t, d, 1.02, 1.12, 0.45, 0.42)
        scrim(ctx, 0.20, 0.45)
        pill(ctx, "AS THICK AS A LEG", W * 0.46, H * 0.120, GOLD, 50, 1.0, prog(T, WT("rope") - 0.1, WT("rope") + 0.3))
        tag(ctx, y=0.175)
    else:                                         # « She couldn't free herself. »
        still(ctx, "key_hook.png", t, d, 1.15, 1.30, 0.52, 0.56)
        tag(ctx)

def ov_cut(ctx, t, d): rescue_clock(ctx, S0("cut") + t); tag(ctx)
_cut = clip_scene("cut", ov_cut, push=0.04, punch=0.0)

def ov_stay(ctx, t, d): rescue_clock(ctx, S0("stay") + t); tag(ctx)
_stay = clip_scene("stay", ov_stay, push=0.06, punch=0.0)

def ov_snap(ctx, t, d):
    T = S0("snap") + t
    rescue_clock(ctx, T)
    kb = prog(T, WT("gave") - 0.1, WT("way") + 0.5)
    if kb > 0: glow(ctx, W * 0.50, H * 0.42, W * 0.9 * ease(kb), (1.0, 1.0, 0.95), 0.40 * (1 - 0.5 * kb))
    tag(ctx)
_snap = clip_scene("snap", ov_snap, push=0.05, punch=0.0)

def ov_free(ctx, t, d):
    T = S0("free") + t
    kb = prog(T, WT("free", 1) - 0.15, WT("free", 1) + 0.8)
    if kb > 0: glow(ctx, W * 0.50, H * 0.25, W * 0.9 * ease(kb), (0.9, 1.0, 1.0), 0.30 * (1 - 0.6 * kb))
    tag(ctx)
_free = clip_scene("free", ov_free, push=0.03, punch=0.0)

def sc_count(ctx, t, d):
    still(ctx, "key_free.png", t, d, 1.10, 1.0, 0.55, 0.40)
    T = S0("count") + t
    scrim(ctx, 0.24, 0.50)
    pill(ctx, "ENDANGERED", W * 0.46, H * 0.120, CORAL, 56, 1.0, prog(T, WT("endangered") - 0.2, WT("endangered") + 0.2))
    T_CTA = END_T - 2.5
    kc = prog(T, T_CTA, T_CTA + 0.35)
    if kc > 0:
        cta_lines(ctx, ("Follow Factora for more", "animal mysteries."), W * 0.46, (H * 0.205, H * 0.237), 54, kc)
    tag(ctx, y=0.290 if kc > 0 else 0.175)

SCENES = dict(hook=_hook, wound=sc_wound, cut=_cut, stay=_stay, snap=_snap, free=_free, count=sc_count)
SHORT_SCENES = ["hook", "wound", "cut", "stay", "snap", "free", "count"]

def cover(ctx):
    """Miniature : l'image de l'accroche, « TRAPPED », le bandeau « SHE DIDN'T SWIM AWAY », la mention « Illustration »."""
    paint(ctx, load_img(os.path.join(RW, "key_hook.png")), 0.5, 0.48, 1.0)
    scrim(ctx, 0.30, 0.65)
    poster_text(ctx, "TRAPPED", W * 0.46, H * 0.185, 210 * U, CORAL, W * 0.86)
    txt = "SHE DIDN'T SWIM AWAY"; fs = 62 * U; font(ctx, fs)
    if ctx.text_extents(txt).width > W * 0.74: fs *= W * 0.74 / ctx.text_extents(txt).width; font(ctx, fs)
    w_ = ctx.text_extents(txt).width + 80 * U; h_ = fs * 1.9; y_ = H * 0.775
    glow(ctx, W * 0.46, y_, w_ * 0.6, GOLD, 0.30)
    rrect(ctx, W * 0.46 - w_ / 2, y_ - h_ / 2, w_, h_, h_ / 2); rgba(ctx, GOLD, 0.97); ctx.fill()
    text(ctx, txt, W * 0.46, y_, fs, DARK)
    tag(ctx, y=0.255)
