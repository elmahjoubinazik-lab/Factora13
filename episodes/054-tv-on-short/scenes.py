exec(open("engine/photo.py", encoding="utf-8").read())   # load_img, paint, scrim, poster_text
# Épisode 054 (Short seul, 9:16, ≈ 33 s) — tiré de la vidéo longue 053 « Can't Sleep Without the TV On? Here's Why »
# (YouTube 69ZCE96ljgI), à la demande de Nazik (2026-11-27 : « un short de cette vidéo qu'on pourra relier sur YouTube et
# publier sur les réseaux sociaux »). Se comprend seul : le pourquoi (réseau du mode par défaut), la rediffusion sans
# suspense, le piège (lumière et bruit toute la nuit), une solution, renvoi vers la vidéo complète, retour à l'image 1.
# Images : Runway (nano-banana-2.1, 9:16), recadrages verticaux des illustrations de Maya (personnage fictif) de l'ép. 053.
# Voix : Jessica via Runway (eleven_v4), une réplique par scène. Musique : celle de la vidéo longue (lien entre les deux).
import json as _json, re as _re

_TLL = _json.load(open(EP + "/build/timeline.json", encoding="utf-8"))
_TL = {sg["scene"]: sg for sg in _TLL}
_FIRST = _TLL[0]["scene"]
END_T = _TLL[-1]["end"] + 0.6
def S0(sc): return 0.0 if sc == _FIRST else _TL[sc]["start"]
def S1(sc): return _TL[sc]["end"]
def WT(sc, word):
    """Instant estimé d'un mot (proportionnel aux caractères de la phrase : la voix « files » n'a pas d'horodatage par mot)."""
    for se in _TL[sc]["sents"]:
        m = _re.search(r"\b" + _re.escape(word) + r"\b", se["text"], _re.I)
        if m: return se["start"] + (se["end"] - se["start"]) * m.start() / max(1, len(se["text"]))
    return S0(sc)
def lerp(a, b, k): return a + (b - a) * k
DARK = (0.02, 0.03, 0.08)
IMG = os.path.join(RW, "img")

def still(ctx, name, t, d, z0=1.0, z1=1.07, fx=0.5, fy=0.5, a=1.0):
    paint(ctx, load_img(os.path.join(IMG, name)), fx, fy, lerp(z0, z1, clamp(t / max(d, 0.1))), a)

def tag(ctx, s="Illustration", y=0.083, a=1.0):
    if a <= 0: return
    font(ctx, 32 * U); w_ = ctx.text_extents(s).width + 40 * U
    x0, y0 = W * 0.055, H * y
    rrect(ctx, x0, y0 - 25 * U, w_, 50 * U, 25 * U); rgba(ctx, (0.0, 0.0, 0.0), 0.50 * a); ctx.fill()
    text(ctx, s, x0 + 20 * U, y0, 32 * U, (0.92, 0.94, 1.0), 0.92 * a, align="l")

def pill(ctx, s, x, y, col, size=50, k=1.0, fg=DARK):
    if k <= 0: return
    sc_ = 0.6 + 0.4 * ease(k) + 0.08 * math.sin(math.pi * clamp(k))
    ctx.save(); ctx.translate(x, y); ctx.scale(sc_, sc_)
    font(ctx, size * U); w_ = ctx.text_extents(s).width + 64 * U; h_ = size * 1.6 * U
    if w_ > W * 0.84:
        size *= W * 0.84 / w_; font(ctx, size * U); w_ = ctx.text_extents(s).width + 64 * U; h_ = size * 1.6 * U
    glow(ctx, 0, 0, w_ * 0.7, col, 0.35 * k)
    rrect(ctx, -w_ / 2, -h_ / 2, w_, h_, h_ / 2); rgba(ctx, col, 0.97 * k); ctx.fill()
    text(ctx, s, 0, 0, size * U, fg, k)
    ctx.restore()

def hook_title(ctx, a):
    if a <= 0: return
    ctx.push_group(); poster_text(ctx, "TOO QUIET?", W * 0.46, H * 0.150, 150 * U, GOLD, W * 0.76); ctx.pop_group_to_source(); ctx.paint_with_alpha(a)

def pk(T, a, dur=0.35): return prog(T, a, a + dur)

# ---------------------------------------------------------------- scènes (t local, T absolu)
def sc_hook(ctx, t, d):
    still(ctx, "v_hook.png", t, d, 1.0, 1.06, 0.5, 0.42)
    scrim(ctx, 0.24, 0.55)
    hook_title(ctx, 1.0)                                   # ≤ 3 mots dès la 1re image
    tag(ctx, "Illustration", y=0.235, a=prog(t, 1.2, 1.6))

def sc_why(ctx, t, d):
    T = S0("why") + t; tw = WT("why", "replays") - 0.15
    if T < tw:
        still(ctx, "v_brain.png", T - S0("why"), tw - S0("why"), 1.0, 1.08, 0.5, 0.45)
        scrim(ctx, 0.22, 0.45)
        pill(ctx, "DEFAULT MODE NETWORK", W * 0.46, H * 0.120, GOLD, 52, pk(T, WT("why", "daydream") - 0.2))
        pill(ctx, "= YOUR BRAIN'S DAYDREAM MODE", W * 0.46, H * 0.180, WHITE, 38, pk(T, WT("why", "network") - 0.1))
    else:
        still(ctx, "v_worries.png", T - tw, S1("why") - tw, 1.04, 1.0, 0.5, 0.40)
    tag(ctx, a=0.9)

def sc_tv(ctx, t, d):
    T = S0("tv") + t
    still(ctx, "v_rerun.png", t, d, 1.0, 1.07, 0.5, 0.45)
    scrim(ctx, 0.22, 0.40)
    pill(ctx, "A RERUN = NO SURPRISES", W * 0.46, H * 0.120, CYAN, 50, pk(T, WT("tv", "rerun") - 0.2) * (1 - pk(T, WT("tv", "cliffhanger") - 0.4, 0.25)))
    pill(ctx, "NO CLIFFHANGER = LET GO", W * 0.46, H * 0.120, GREEN, 50, pk(T, WT("tv", "cliffhanger") - 0.2))
    tag(ctx, y=0.185)

def sc_catch(ctx, t, d):
    T = S0("catch") + t
    still(ctx, "v_eyes.png", t, d, 1.06, 1.0, 0.5, 0.45)
    scrim(ctx, 0.22, 0.45)
    pill(ctx, "ON ALL NIGHT", W * 0.46, H * 0.120, CORAL, 56, pk(T, WT("catch", "night") - 0.4), fg=WHITE)
    pill(ctx, "LIGHT + NOISE DISTURB SLEEP", W * 0.46, H * 0.185, WHITE, 40, pk(T, WT("catch", "disturb") - 0.3))
    tag(ctx, y=0.245)

def sc_fix(ctx, t, d):
    T = S0("fix") + t
    still(ctx, "v_podcast.png", t, d, 1.0, 1.07, 0.5, 0.45)
    scrim(ctx, 0.24, 0.50)
    pill(ctx, "KEEP THE VOICE, LOSE THE LIGHT", W * 0.46, H * 0.120, GREEN, 46, pk(T, S0("fix") + 0.1))
    pill(ctx, "+ A SLEEP TIMER", W * 0.46, H * 0.180, WHITE, 42, pk(T, WT("fix", "timer") - 0.4))
    pill(ctx, "MORE TRICKS IN THE FULL VIDEO", W * 0.46, H * 0.245, GOLD, 40, pk(T, WT("fix", "More") - 0.2))
    tag(ctx, y=0.305)

def sc_end(ctx, t, d):
    T = S0("end") + t
    still(ctx, "v_hook.png", t, d, 1.06, 1.0, 0.5, 0.42)       # retour à l'image 1 (la boucle se referme)
    scrim(ctx, 0.24, 0.55)
    hook_title(ctx, pk(T, WT("end", "silence") - 0.2, 0.5))
    k = pk(T, END_T - 1.6, 0.4)
    if k > 0:
        font(ctx, 40 * U); text(ctx, "FACTORA", W * 0.46, H * 0.235, 40 * U, (0.92, 0.94, 1.0), 0.9 * k)

SCENES = dict(hook=sc_hook, why=sc_why, tv=sc_tv, catch=sc_catch, fix=sc_fix, end=sc_end)
SHORT_SCENES = ["hook", "why", "tv", "catch", "fix", "end"]

def cover(ctx):
    """Affiche TikTok/Instagram : Maya éveillée, « TOO QUIET? », bandeau « WHY YOU NEED THE TV ON », mention « Illustration »."""
    paint(ctx, load_img(os.path.join(IMG, "v_hook.png")), 0.5, 0.45, 1.0)
    scrim(ctx, 0.32, 0.62)
    poster_text(ctx, "TOO", W * 0.46, H * 0.175, 220 * U, WHITE, W * 0.86)
    poster_text(ctx, "QUIET?", W * 0.46, H * 0.265, 220 * U, GOLD, W * 0.86)
    txt = "WHY YOU NEED THE TV ON"; fs = 62 * U; font(ctx, fs)
    if ctx.text_extents(txt).width > W * 0.74: fs *= W * 0.74 / ctx.text_extents(txt).width; font(ctx, fs)
    w_ = ctx.text_extents(txt).width + 80 * U; h_ = fs * 1.9; y_ = H * 0.775
    glow(ctx, W * 0.46, y_, w_ * 0.6, CYAN, 0.30)
    rrect(ctx, W * 0.46 - w_ / 2, y_ - h_ / 2, w_, h_, h_ / 2); rgba(ctx, CYAN, 0.97); ctx.fill()
    text(ctx, txt, W * 0.46, y_, fs, DARK)
    tag(ctx, y=0.335)
