# Épisode 049 — « Factora Quiz #1 : 20 animal questions » (demande de Nazik, 2026-11-22 : format quiz « culture G »
# en Short, 20 questions pour s'auto-évaluer, la chouette Factora en présentatrice animée qui lit les questions,
# assez de temps pour répondre + invitation à mettre pause).
# Mise en page continue : tout est dessiné par master(ctx, T) à partir du temps absolu T (timeline.json) :
# liste 1–20 qui se remplit (repère de progression), chouette animée (bec calé sur la voix, clignements, regard,
# aile qui montre la question, tête qui tourne à la question 7), carte question, chrono 3-2-1 (tics), réponse (ding).
# Icônes : emoji Noto Color Emoji (police libre, SIL OFL) rendus en PNG dans build/emoji/.
exec(open("engine/photo.py", encoding="utf-8").read())   # poster_text, load_img…
import json as _json
from PIL import Image as _PImg

_TLL = _json.load(open(EP + "/build/timeline.json", encoding="utf-8"))
_TL = {sg["scene"]: sg for sg in _TLL}
QZ = _json.load(open(EP + "/quiz.json", encoding="utf-8"))
NQ = len(QZ)
SPANS = [(se["start"], se["end"]) for sg in _TLL for se in sg["sents"]]
QD = []
for i in range(1, NQ + 1):
    q, a = _TL[f"q{i:02d}"], _TL[f"a{i:02d}"]
    QD.append(dict(qs=q["start"], qe=q["sents"][-1]["end"], a_s=a["start"], a_se=a["sents"][-1]["end"], a_e=a["end"]))
T_Q1 = QD[0]["qs"]
T_OUT = _TL["outro"]["start"]
INTRO = _TL["intro"]["sents"]
OUT = _TL["outro"]["sents"]
DARK = (0.02, 0.03, 0.09)
def S0(scene): return 0.0 if scene == _TLL[0]["scene"] else _TL[scene]["start"]
def lin(t, a, b): return clamp((t - a) / (b - a)) if b > a else 1.0
def lerp(a, b, k): return a + (b - a) * k
def pop(k): return 0.0 if k <= 0 else (1 + 0.22 * math.sin(math.pi * clamp(k)) if k < 1 else 1.0) * min(1.0, 0.55 + 0.45 * ease(k) / 1.0)

# ---------------------------------------------------------------- emoji
_EM = {}
def emoji_surf(ch):
    if ch in _EM: return _EM[ch][0]
    p = os.path.join(EP, "build", "emoji", "_".join(f"{ord(c):x}" for c in ch) + ".png")
    im = _PImg.open(p).convert("RGBA"); a = np.asarray(im).astype(np.float32); h, w = a.shape[:2]
    al = a[..., 3:4] / 255.0
    buf = np.empty((h, w, 4), np.uint8)
    buf[..., 0] = (a[..., 2] * al[..., 0]).astype(np.uint8); buf[..., 1] = (a[..., 1] * al[..., 0]).astype(np.uint8)
    buf[..., 2] = (a[..., 0] * al[..., 0]).astype(np.uint8); buf[..., 3] = a[..., 3].astype(np.uint8)
    s = cairo.ImageSurface.create_for_data(memoryview(buf), cairo.FORMAT_ARGB32, w, h, w * 4)
    _EM[ch] = (s, buf); return s

def draw_emoji(ctx, ch, x, y, size, a=1.0, k=1.0, rot=0.0):
    if not ch or a <= 0 or k <= 0: return
    s = emoji_surf(ch); sw, sh = s.get_width(), s.get_height(); sc = size / max(sw, sh) * k
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(sc, sc); ctx.translate(-sw / 2, -sh / 2)
    ctx.set_source_surface(s, 0, 0); ctx.get_source().set_filter(cairo.FILTER_GOOD); ctx.paint_with_alpha(a); ctx.restore()

# ---------------------------------------------------------------- textes
def wrap(ctx, s, size, maxw):
    font(ctx, size); out, cur = [], ""
    for w_ in s.split():
        t_ = (cur + " " + w_).strip()
        if ctx.text_extents(t_).width > maxw and cur: out.append(cur); cur = w_
        else: cur = t_
    out.append(cur); return out

def pill(ctx, s, x, y, col, size=46, a=1.0, k=1.0, fg=DARK):
    if a <= 0 or k <= 0: return
    sc_ = pop(k)
    ctx.save(); ctx.translate(x, y); ctx.scale(sc_, sc_)
    font(ctx, size * U); w_ = ctx.text_extents(s).width + 64 * U; h_ = size * 1.7 * U
    glow(ctx, 0, 0, w_ * 0.65, col, 0.30 * a)
    rrect(ctx, -w_ / 2, -h_ / 2, w_, h_, h_ / 2); rgba(ctx, col, 0.97 * a); ctx.fill()
    text(ctx, s, 0, 0, size * U, fg, a)
    ctx.restore()

def pause_icon(ctx, x, y, h, col, a=1.0):
    for dx in (-0.22, 0.22):
        rrect(ctx, x + dx * h - 0.13 * h, y - h / 2, 0.26 * h, h, 0.08 * h); rgba(ctx, col, a); ctx.fill()

# ---------------------------------------------------------------- fond
_RS = random.Random(49)
_STARS = [(_RS.random(), _RS.random(), _RS.uniform(1.5, 4.0), _RS.random() * 6.28) for _ in range(90)]
NEB = os.path.join(EP, "build", "rw", "nebula.png")   # fond Runway dans le style de la bannière YouTube (v2)
def background(ctx, T):
    if os.path.exists(NEB):
        paint(ctx, load_img(NEB), 0.5, 0.5, 1.0 + 0.04 * clamp(T / 160.0))
        ctx.rectangle(0, 0, W, H); rgba(ctx, (0.01, 0.01, 0.06), 0.18); ctx.fill()
    else:
        vgrad(ctx, (0.07, 0.04, 0.22), (0.01, 0.02, 0.09))
    for sx, sy, sr, ph in _STARS[:50]:
        circle(ctx, sx * W, sy * H, sr * U * 0.8, WHITE, 0.15 + 0.25 * math.sin(T * 1.3 + ph))

def header(ctx, T):
    poster_text(ctx, "ANIMAL QUIZ", W * 0.47, H * 0.083, 92 * U, GOLD, W * 0.80)
    text(ctx, "FACTORA QUIZ #1  ·  20 QUESTIONS", W * 0.47, H * 0.118, 27 * U, (0.80, 0.88, 1.0), 0.85)

# ---------------------------------------------------------------- la chouette Factora, v2 : images Runway dans le style du logo
# (demande de Nazik, 2026-11-22 : « le même graphisme que le logo et la bannière YouTube », Runway autorisé en partie).
# base = pose de référence ; talk / blink = mêmes images, bec ouvert / yeux fermés (superposés seulement sur la zone du bec
# ou des yeux, bords adoucis) ; happy = pose de joie (ailes levées) pour les réponses et la fin. Voir prep_owl.py.
OWLD = os.path.join(EP, "build", "rw", "owl")
_OS = {}
def _rgba_surf(arr):
    a = arr[..., 3:4].astype(np.float32) / 255.0; h, w = arr.shape[:2]
    buf = np.empty((h, w, 4), np.uint8)
    buf[..., 0] = (arr[..., 2] * a[..., 0]).astype(np.uint8); buf[..., 1] = (arr[..., 1] * a[..., 0]).astype(np.uint8)
    buf[..., 2] = (arr[..., 0] * a[..., 0]).astype(np.uint8); buf[..., 3] = arr[..., 3]
    return cairo.ImageSurface.create_for_data(memoryview(buf), cairo.FORMAT_ARGB32, w, h, w * 4), buf
def owl_sprites():
    if _OS: return _OS
    reg = _json.load(open(os.path.join(OWLD, "regions.json")))
    for n in ("base", "happy"):
        _OS[n] = _rgba_surf(np.asarray(_PImg.open(os.path.join(OWLD, n + "_rgba.png")).convert("RGBA")))
    for n, grow in (("talk", 26), ("blink", 22)):
        if n not in reg: continue
        x0, y0, x1, y1 = reg[n]; x0 -= grow; y0 -= grow; x1 += grow; y1 += grow
        im = np.asarray(_PImg.open(os.path.join(OWLD, n + "_crop.png")).convert("RGB"))[y0:y1, x0:x1]
        hh, ww = im.shape[:2]; yy, xx = np.mgrid[0:hh, 0:ww]
        d = np.minimum.reduce([xx, yy, ww - 1 - xx, hh - 1 - yy]).astype(np.float32)
        al = (np.clip(d / grow, 0, 1) * 255).astype(np.uint8)
        _OS[n] = _rgba_surf(np.dstack([im, al])) + ((x0, y0),)
    return _OS

def owl_sprite(ctx, x, y, h, st):
    """Chouette Factora (images Runway) centrée en (x, y), hauteur h. st : talk, blink, happy (0–1), tilt, spin, squash."""
    sp = owl_sprites(); b = sp["base"][0]; sw, sh = b.get_width(), b.get_height(); sc = h / sh
    sq = st.get("squash", 0.0); fx = math.cos(st.get("spin", 0.0)); fx = math.copysign(max(0.04, abs(fx)), fx)
    ctx.save(); ctx.translate(x, y)
    g = cairo.RadialGradient(0, h * 0.05, 0, 0, h * 0.05, h * 0.62)   # halo sombre : détache la chouette de la nébuleuse
    g.add_color_stop_rgba(0, 0.01, 0.01, 0.06, 0.55); g.add_color_stop_rgba(1, 0.01, 0.01, 0.06, 0)
    ctx.set_source(g); ctx.arc(0, h * 0.05, h * 0.62, 0, 2 * math.pi); ctx.fill()
    ctx.rotate(st.get("tilt", 0.0)); ctx.scale(sc * fx * (1 + 0.05 * sq), sc * (1 - 0.05 * sq)); ctx.translate(-sw / 2, -sh / 2)
    hap = clamp(st.get("happy", 0.0))
    if hap < 1:
        ctx.set_source_surface(b, 0, 0); ctx.get_source().set_filter(cairo.FILTER_GOOD); ctx.paint_with_alpha(1 - hap)
        for n, k in (("talk", clamp((st.get("talk", 0.0) - 0.35) / 0.30)), ("blink", st.get("blink", 0.0))):
            if k > 0 and n in sp:
                s_, _, (ox_, oy_) = sp[n]
                ctx.set_source_surface(s_, ox_, oy_); ctx.get_source().set_filter(cairo.FILTER_GOOD); ctx.paint_with_alpha(k * (1 - hap))
    if hap > 0:
        ctx.set_source_surface(sp["happy"][0], 0, 0); ctx.get_source().set_filter(cairo.FILTER_GOOD); ctx.paint_with_alpha(hap)
    ctx.restore()

# (ancienne chouette vectorielle, v1 — gardée pour mémoire, plus utilisée)
BODY_T, BODY_B = (0.20, 0.24, 0.78), (0.45, 0.16, 0.70)
HEAD_T, HEAD_B = (0.20, 0.42, 1.00), (0.33, 0.22, 0.85)
WING_T, WING_B = (0.25, 0.75, 1.00), (0.20, 0.30, 0.85)
BEAK = (1.0, 0.62, 0.12)

def _head_path(ctx):
    ctx.move_to(-0.95, -1.05)
    ctx.curve_to(-0.55, -0.70, -0.25, -0.62, 0.0, -0.62)
    ctx.curve_to(0.25, -0.62, 0.55, -0.70, 0.95, -1.05)
    ctx.curve_to(1.10, -0.70, 1.15, -0.25, 1.05, 0.10)
    ctx.curve_to(0.95, 0.50, 0.45, 0.72, 0.0, 0.72)
    ctx.curve_to(-0.45, 0.72, -0.95, 0.50, -1.05, 0.10)
    ctx.curve_to(-1.15, -0.25, -1.10, -0.70, -0.95, -1.05)
    ctx.close_path()

def _wing(ctx, side, rot):
    ctx.save(); ctx.translate(side * 0.86, 1.02); ctx.rotate(-side * rot); ctx.scale(-side, 1)
    ctx.new_path(); ctx.move_to(0.05, -0.05)
    ctx.curve_to(-0.42, 0.15, -0.46, 0.85, -0.22, 1.12)
    ctx.curve_to(0.02, 0.92, 0.22, 0.55, 0.22, 0.20)
    ctx.close_path()
    g = cairo.LinearGradient(0, 0, 0, 1.1); g.add_color_stop_rgb(0, *WING_T); g.add_color_stop_rgb(1, *WING_B)
    ctx.set_source(g); ctx.fill_preserve()
    ctx.set_line_width(0.035); rgba(ctx, (0.75, 0.95, 1.0), 0.75); ctx.stroke()
    for k in (0.45, 0.70, 0.92):
        ctx.move_to(-0.30 + 0.05 * k, 0.30 + 0.55 * k); ctx.line_to(0.05, 0.25 + 0.45 * k)
        ctx.set_line_width(0.022); rgba(ctx, (0.80, 0.95, 1.0), 0.45); ctx.stroke()
    ctx.restore()

def _dots(ctx, pts, a=1.0):
    ctx.new_path(); ctx.move_to(*pts[0])
    for p in pts[1:]: ctx.line_to(*p)
    ctx.set_line_width(0.018); rgba(ctx, (0.85, 0.95, 1.0), 0.55 * a); ctx.stroke()
    for p in pts:
        g = cairo.RadialGradient(p[0], p[1], 0, p[0], p[1], 0.07); g.add_color_stop_rgba(0, 1, 1, 1, 0.9 * a); g.add_color_stop_rgba(1, 1, 1, 1, 0)
        ctx.set_source(g); ctx.arc(p[0], p[1], 0.07, 0, 2 * math.pi); ctx.fill()
        ctx.arc(p[0], p[1], 0.022, 0, 2 * math.pi); rgba(ctx, WHITE, a); ctx.fill()

def owl(ctx, x, y, R, st):
    """Chouette Factora (dessin maison d'après le logo). (x, y) = centre de la tête, R = demi-largeur de tête.
    st : talk (0–1, ouverture du bec), look (dx, dy), blink (0–1), tilt (rad), wing (0–1, aile gauche levée),
    spin (rad, rotation de la tête), wide (0–1, yeux écarquillés), squash."""
    ctx.save(); ctx.translate(x, y); ctx.scale(R, R)
    sq = st.get("squash", 0.0); ctx.scale(1 + 0.06 * sq, 1 - 0.06 * sq)
    # halo
    g = cairo.RadialGradient(0, 0.8, 0, 0, 0.8, 2.3); g.add_color_stop_rgba(0, 0.30, 0.60, 1.0, 0.30); g.add_color_stop_rgba(1, 0.30, 0.60, 1.0, 0)
    ctx.set_source(g); ctx.arc(0, 0.8, 2.3, 0, 2 * math.pi); ctx.fill()
    # pattes
    for side in (-1, 1):
        for k in (-1, 0, 1):
            ctx.save(); ctx.translate(side * 0.32 + k * 0.10, 2.40); ctx.scale(0.07, 0.13)
            ctx.arc(0, 0, 1, 0, 2 * math.pi); ctx.restore(); rgba(ctx, BEAK, 1); ctx.fill()
    # corps
    ctx.save(); ctx.translate(0, 1.42); ctx.scale(0.95, 1.02); ctx.arc(0, 0, 1, 0, 2 * math.pi); ctx.restore()
    g = cairo.LinearGradient(0, 0.4, 0, 2.45); g.add_color_stop_rgb(0, *BODY_T); g.add_color_stop_rgb(1, *BODY_B)
    ctx.set_source(g); ctx.fill_preserve(); ctx.set_line_width(0.04); rgba(ctx, (0.55, 0.85, 1.0), 0.8); ctx.stroke()
    ctx.save(); ctx.translate(0, 1.62); ctx.scale(0.60, 0.70); ctx.arc(0, 0, 1, 0, 2 * math.pi); ctx.restore()
    g = cairo.RadialGradient(0, 1.5, 0.1, 0, 1.62, 0.75); g.add_color_stop_rgba(0, 0.85, 0.55, 1.0, 0.55); g.add_color_stop_rgba(1, 0.60, 0.30, 0.95, 0.25)
    ctx.set_source(g); ctx.fill()
    _dots(ctx, [(-0.32, 1.30), (-0.10, 1.55), (0.14, 1.36), (0.34, 1.72), (0.02, 1.98)], 0.9)
    # ailes
    _wing(ctx, -1, 0.15 + 0.95 * st.get("wing", 0.0) + 0.04 * math.sin(st.get("T", 0) * 3))
    _wing(ctx, 1, 0.15 + 0.25 * st.get("wing2", 0.0) + 0.04 * math.sin(st.get("T", 0) * 3 + 1))
    # tête
    ctx.save(); ctx.translate(0, 0.55); ctx.rotate(st.get("tilt", 0.0)); ctx.translate(0, -0.55)
    ctx.new_path(); _head_path(ctx)
    g = cairo.LinearGradient(0, -1.05, 0, 0.72); g.add_color_stop_rgb(0, *HEAD_T); g.add_color_stop_rgb(1, *HEAD_B)
    ctx.set_source(g); ctx.fill_preserve(); ctx.set_line_width(0.05); rgba(ctx, (0.60, 0.92, 1.0), 0.95); ctx.stroke()
    sp = st.get("spin", 0.0); cs, sn = math.cos(sp), math.sin(sp)
    if cs > -0.05:
        fx = 0.55 * sn; sx = max(0.05, cs)
        ctx.save(); ctx.translate(fx, 0); ctx.scale(sx, 1)
        # disques faciaux
        for side in (-1, 1):
            ctx.arc(side * 0.43, -0.05, 0.42, 0, 2 * math.pi); rgba(ctx, (0.50, 0.80, 1.0), 0.30); ctx.fill()
        wide = st.get("wide", 0.0); er = 0.28 * (1 + 0.10 * wide)
        lx, ly = st.get("look", (0.0, 0.0)); bl = st.get("blink", 0.0)
        for side in (-1, 1):
            ex, ey = side * 0.43, -0.05
            ctx.arc(ex, ey, er + 0.045, 0, 2 * math.pi); rgba(ctx, (0.03, 0.05, 0.16), 1); ctx.fill()
            g = cairo.RadialGradient(ex, ey, 0.02, ex, ey, er); g.add_color_stop_rgb(0, 0.85, 1.0, 0.35); g.add_color_stop_rgb(1, 0.22, 0.75, 0.10)
            ctx.set_source(g); ctx.arc(ex, ey, er, 0, 2 * math.pi); ctx.fill()
            px, py = ex + 0.10 * lx, ey + 0.09 * ly
            ctx.arc(px, py, 0.13 * (1 - 0.12 * wide), 0, 2 * math.pi); rgba(ctx, (0.01, 0.01, 0.03), 1); ctx.fill()
            ctx.arc(px - 0.05, py - 0.06, 0.045, 0, 2 * math.pi); rgba(ctx, WHITE, 0.95); ctx.fill()
            if bl > 0:   # paupière
                ctx.save(); ctx.arc(ex, ey, er + 0.05, 0, 2 * math.pi); ctx.clip()
                ctx.rectangle(ex - 0.4, ey - er - 0.06, 0.8, (2 * er + 0.12) * bl); rgba(ctx, HEAD_T, 1); ctx.fill()
                ctx.restore()
            # sourcil (relevé quand elle s'étonne)
            lift = 0.06 * wide
            ctx.new_path(); ctx.move_to(ex - side * 0.30, ey - 0.38 - lift - 0.03); ctx.curve_to(ex - side * 0.10, ey - 0.47 - lift, ex + side * 0.15, ey - 0.46 - lift, ex + side * 0.32, ey - 0.36 - lift)
            ctx.set_line_width(0.06); ctx.set_line_cap(cairo.LINE_CAP_ROUND); rgba(ctx, (0.80, 0.97, 1.0), 0.95); ctx.stroke()
        # bec (s'ouvre avec la voix)
        o = st.get("talk", 0.0)
        ctx.new_path(); ctx.move_to(-0.10, 0.25); ctx.line_to(0.10, 0.25); ctx.line_to(0.0, 0.31 + 0.10 * o); ctx.close_path(); rgba(ctx, (0.25, 0.04, 0.08), 1); ctx.fill()
        ctx.new_path(); ctx.move_to(0.0, 0.10); ctx.line_to(0.12, 0.24); ctx.line_to(0.0, 0.31); ctx.line_to(-0.12, 0.24); ctx.close_path()
        g = cairo.LinearGradient(0, 0.1, 0, 0.31); g.add_color_stop_rgb(0, 1.0, 0.80, 0.25); g.add_color_stop_rgb(1, *BEAK); ctx.set_source(g); ctx.fill()
        ctx.new_path(); ctx.move_to(-0.09, 0.27 + 0.12 * o); ctx.line_to(0.09, 0.27 + 0.12 * o); ctx.line_to(0.0, 0.42 + 0.12 * o); ctx.close_path(); rgba(ctx, (0.95, 0.50, 0.08), 1); ctx.fill()
        ctx.restore()
    else:   # vue de dos : plumes
        for k in range(4):
            yy = -0.35 + 0.22 * k
            ctx.new_path(); ctx.move_to(-0.45 + 0.05 * k, yy); ctx.curve_to(-0.15, yy + 0.12, 0.15, yy + 0.12, 0.45 - 0.05 * k, yy)
            ctx.set_line_width(0.04); rgba(ctx, (0.70, 0.90, 1.0), 0.5); ctx.stroke()
    _dots(ctx, [(-0.62, -0.78), (-0.30, -0.58), (0.05, -0.66), (0.40, -0.60), (0.70, -0.85)], 0.85)
    ctx.restore()
    ctx.restore()

def _talk(T):
    for s, e in SPANS:
        if s - 0.02 <= T <= e - 0.05:
            u = T - s
            return clamp(0.15 + 0.85 * abs(math.sin(math.pi * 5.2 * u)) * (0.75 + 0.25 * math.sin(11.0 * u + 1.3)))
    return 0.0

def _blink(T):
    u = (T + 0.7) % 3.3
    return math.sin(math.pi * u / 0.15) if u < 0.15 else 0.0

def owl_state(T, i, ph):
    st = {"T": T, "talk": _talk(T), "blink": _blink(T), "look": (0.0, 0.1)}
    if i >= 0:
        d = QD[i]
        if ph == "read":
            st["look"] = (-0.75, 0.75)
            st["wing"] = prog(T, d["qs"], d["qs"] + 0.30) - prog(T, d["qs"] + 1.4, d["qs"] + 1.8)
        elif ph == "timer":
            st["look"] = (-0.15, 0.95); st["tilt"] = 0.06 * math.sin(2 * math.pi * 0.55 * (T - d["qe"]))
        elif ph == "answer":
            k = lin(T, d["a_s"], d["a_s"] + 0.35)
            st["look"] = (0.0, 0.0); st["wide"] = 1.0 - prog(T, d["a_s"] + 0.6, d["a_s"] + 1.2)
            st["hop"] = math.sin(math.pi * k) if k < 1 else 0.0; st["squash"] = -0.8 * math.sin(math.pi * k) if k < 1 else 0.0
            st["wing2"] = math.sin(math.pi * k) if k < 1 else 0.0
            st["happy"] = prog(T, d["a_s"] - 0.02, d["a_s"] + 0.10) - prog(T, d["a_s"] + 0.95, d["a_s"] + 1.10)
            if i == 6:   # question 7 : « The owl! That's me. » → la tête fait un tour
                st["spin"] = 2 * math.pi * ease(lin(T, d["a_s"] + 0.25, d["a_s"] + 1.45)); st["blink"] = 0.0
    if ph == "outro":
        u = T - T_OUT
        st["hop"] = 0.5 * abs(math.sin(math.pi * 1.6 * u)); st["wing"] = 0.5 + 0.5 * math.sin(2 * math.pi * 0.8 * u); st["wing2"] = st["wing"]
        st["look"] = (0.0, 0.0); st["happy"] = 1.0
    return st

# ---------------------------------------------------------------- état du quiz
def phase(T):
    if T < T_Q1: return -1, "intro"
    if T >= T_OUT: return NQ - 1, "outro"
    i = max(k for k in range(NQ) if QD[k]["qs"] <= T)
    d = QD[i]
    return i, ("read" if T < d["qe"] else "timer" if T < d["a_s"] else "answer")

LIST_X0, LIST_X1, LIST_Y0, ROW = 0.035, 0.455, 0.152, 0.0205
def answer_list(ctx, T, i, ph, a=1.0):
    if a <= 0: return
    rrect(ctx, W * LIST_X0, H * (LIST_Y0 - 0.016), W * (LIST_X1 - LIST_X0), H * (ROW * NQ + 0.014), 26 * U)
    rgba(ctx, (0.01, 0.02, 0.08), 0.62 * a); ctx.fill_preserve(); ctx.set_line_width(2.5 * U); rgba(ctx, (0.45, 0.70, 1.0), 0.45 * a); ctx.stroke()
    for k in range(NQ):
        y = H * (LIST_Y0 + ROW * k)
        done = QD[k]["a_s"] <= T
        cur = (k == i and ph in ("read", "timer"))
        if cur:
            pul = 0.5 + 0.5 * math.sin(T * 6)
            rrect(ctx, W * (LIST_X0 + 0.008), y - H * ROW * 0.46, W * (LIST_X1 - LIST_X0 - 0.016), H * ROW * 0.92, 12 * U)
            rgba(ctx, CYAN, (0.22 + 0.12 * pul) * a); ctx.fill()
        ncol = GOLD if (done or cur) else (0.75, 0.80, 0.95)
        text(ctx, f"{k + 1}.", W * 0.088, y, 31 * U, ncol, (1.0 if (done or cur) else 0.45) * a, align="r")
        if done:
            kk = lin(T, QD[k]["a_s"], QD[k]["a_s"] + 0.25)
            s = QZ[k]["list"]; size = 31 * U; font(ctx, size)
            mw = W * (LIST_X1 - 0.11 - 0.012)
            if ctx.text_extents(s).width > mw: size *= mw / ctx.text_extents(s).width
            text(ctx, s, W * 0.105 + (1 - ease(kk)) * 30 * U, y, size, WHITE, a * ease(kk), align="l")
        elif cur:
            text(ctx, "?", W * 0.105, y, 33 * U, CYAN, a, align="l")

CARD = (0.035, 0.578, 0.855, 0.768)   # x0, y0, x1, y1 (fractions)
def card(ctx, T, i, ph, a=1.0):
    if a <= 0 or i < 0: return
    d, qz = QD[i], QZ[i]
    x0, y0, x1, y1 = W * CARD[0], H * CARD[1], W * CARD[2], H * CARD[3]
    cx = (x0 + x1) / 2
    glow(ctx, cx, (y0 + y1) / 2, W * 0.55, (0.55, 0.30, 1.0), 0.16 * a)
    rrect(ctx, x0, y0, x1 - x0, y1 - y0, 34 * U); rgba(ctx, (0.03, 0.03, 0.12), 0.90 * a); ctx.fill_preserve()
    ctx.set_line_width(4 * U); rgba(ctx, GOLD, 0.85 * a); ctx.stroke()
    kin = prog(T, d["qs"] - 0.02, d["qs"] + 0.22) if i > 0 else 1.0
    ox = (1 - kin) * W * 0.25; aa = a * kin
    ctx.save(); ctx.translate(ox, 0)
    text(ctx, f"QUESTION {i + 1}/{NQ}", x0 + 44 * U, y0 + 40 * U, 30 * U, CYAN, aa, align="l")
    draw_emoji(ctx, qz["q_icon"], x1 - 70 * U, y0 + 6 * U, 118 * U, aa, pop(prog(T, d["qs"], d["qs"] + 0.35)) if i > 0 else 1.0, 0.08 * math.sin(T * 2))
    ans = T >= d["a_s"]
    size = 62 * U; lines = wrap(ctx, qz["q"], size, (x1 - x0) * 0.86)
    if len(lines) > 2: size = 56 * U; lines = wrap(ctx, qz["q"], size, (x1 - x0) * 0.88)
    lh = size * 1.18; yc = lerp(H * 0.660, H * 0.640, prog(T, d["a_s"], d["a_s"] + 0.3)) if ans else H * 0.662
    for j, ln in enumerate(lines):
        text(ctx, ln, cx, yc + (j - (len(lines) - 1) / 2) * lh, size, WHITE, aa * (0.62 if ans else 1.0))
    if ans:
        k = lin(T, d["a_s"], d["a_s"] + 0.32); sc_ = pop(k)
        s = qz["a"]; fs = 84 * U; font(ctx, fs); tw = ctx.text_extents(s).width
        maxw = (x1 - x0) * 0.56
        if tw > maxw: fs *= maxw / tw; font(ctx, fs); tw = ctx.text_extents(s).width
        r_ = 34 * U; icon = 105 * U if qz["a_icon"] else 0
        tot = 2 * r_ + 22 * U + tw + (26 * U + icon if icon else 0)
        gx = cx - tot / 2; ya = H * 0.727
        ctx.save(); ctx.translate(cx, ya); ctx.scale(sc_, sc_); ctx.translate(-cx, -ya)
        glow(ctx, cx, ya, tot * 0.7, GREEN, 0.22 * aa)
        circle(ctx, gx + r_, ya, r_, GREEN, aa)
        ctx.new_path(); ctx.move_to(gx + r_ - 15 * U, ya + 1 * U); ctx.line_to(gx + r_ - 3 * U, ya + 13 * U); ctx.line_to(gx + r_ + 17 * U, ya - 13 * U)
        ctx.set_line_width(8 * U); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_join(cairo.LINE_JOIN_ROUND); rgba(ctx, DARK, aa); ctx.stroke()
        poster_text(ctx, s, gx + 2 * r_ + 22 * U + tw / 2, ya, fs, GOLD)
        if icon:
            n = 3 if i == 4 else 1
            for m in range(n):
                draw_emoji(ctx, qz["a_icon"], gx + 2 * r_ + 22 * U + tw + 26 * U + icon / 2 + (m - (n - 1) / 2) * icon * 0.42, ya + (m - (n - 1) / 2) * 0 * U,
                           icon * (0.7 if n > 1 else 1.0), aa, 1.0, -0.12 + 0.05 * math.sin(T * 3))
        ctx.restore()
    ctx.restore()

TIM = (0.675, 0.455)
def timer(ctx, T, i, ph):
    if i < 0 or ph != "timer": return
    d = QD[i]; x, y, r = W * TIM[0], H * TIM[1], 80 * U
    kin = pop(lin(T, d["qe"], d["qe"] + 0.25))
    left = d["a_s"] - T; frac = clamp(left / (d["a_s"] - d["qe"]))
    digit = 3 if left > 2 else 2 if left > 1 else 1
    tk = d["a_s"] - digit   # tic du chiffre affiché : le chiffre « claque » à cet instant
    kp = lin(T, tk, tk + 0.2) if T >= tk else 1.0
    col = mix(GOLD, CORAL, 1 - frac)
    ctx.save(); ctx.translate(x, y); ctx.scale(kin, kin)
    glow(ctx, 0, 0, r * 2.0, col, 0.30)
    circle(ctx, 0, 0, r * 1.08, (0.02, 0.03, 0.10), 0.95)
    ctx.new_path(); ctx.arc(0, 0, r, 0, 2 * math.pi); ctx.set_line_width(14 * U); rgba(ctx, WHITE, 0.15); ctx.stroke()
    ctx.new_path(); ctx.arc(0, 0, r, -math.pi / 2, -math.pi / 2 + 2 * math.pi * frac); ctx.set_line_width(14 * U); ctx.set_line_cap(cairo.LINE_CAP_ROUND); rgba(ctx, col, 1); ctx.stroke()
    sc_ = 1 + 0.25 * (1 - ease(kp))
    ctx.save(); ctx.scale(sc_, sc_); neon_text(ctx, str(digit), 0, 0, 104 * U, col, 1.0, fill=0.9); ctx.restore()
    ctx.restore()
    a = lin(T, d["qe"] + 0.1, d["qe"] + 0.4)
    yh = H * 0.518
    font(ctx, 27 * U); s = "PAUSE = MORE TIME"; tw = ctx.text_extents(s).width
    pause_icon(ctx, x - tw / 2 - 26 * U, yh, 28 * U, WHITE, 0.85 * a)
    text(ctx, s, x + 10 * U, yh, 27 * U, WHITE, 0.85 * a)

# ---------------------------------------------------------------- intro / fin
def intro_texts(ctx, T):
    s1, s2, s3 = INTRO[0], INTRO[1], INTRO[2]
    out = 1 - prog(T, T_Q1 - 0.70, T_Q1 - 0.25)
    if out <= 0: return
    a12 = out * (1 - prog(T, s3["start"] - 0.25, s3["start"]))
    pill(ctx, "20 QUESTIONS", W * 0.5, H * 0.672, CYAN, 62, a12, lin(T, 0.25, 0.6))
    pill(ctx, "15/20 = GENIUS", W * 0.5, H * 0.748, GOLD, 62, a12, lin(T, s2["start"], s2["start"] + 0.35))
    a3 = out * lin(T, s3["start"] - 0.1, s3["start"] + 0.2)
    if a3 > 0:
        x, y, r = W * 0.5, H * 0.655, 74 * U
        circle(ctx, x, y, r * 1.08, (0.02, 0.03, 0.10), 0.95 * a3)
        ctx.new_path(); ctx.arc(x, y, r, -math.pi / 2, 1.5 * math.pi); ctx.set_line_width(13 * U); rgba(ctx, GOLD, a3); ctx.stroke()
        neon_text(ctx, "3", x, y, 96 * U, GOLD, a3, fill=0.9)
        text(ctx, "SECONDS EACH", W * 0.5, H * 0.716, 42 * U, WHITE, a3)
        k4 = lin(T, s3["start"] + 1.2, s3["start"] + 1.5)
        pill(ctx, "PAUSE = MORE TIME", W * 0.5, H * 0.768, CORAL, 46, a3 * k4, k4)

def outro_card(ctx, T):
    k = prog(T, T_OUT, T_OUT + 0.35)
    if k <= 0: return
    x0, y0, x1, y1 = W * CARD[0], H * CARD[1], W * CARD[2], H * CARD[3]; cx = (x0 + x1) / 2
    rrect(ctx, x0, y0, x1 - x0, y1 - y0, 34 * U); rgba(ctx, (0.03, 0.03, 0.12), 0.95 * k); ctx.fill_preserve()
    ctx.set_line_width(4 * U); rgba(ctx, GOLD, 0.85 * k); ctx.stroke()
    neon_text(ctx, "WHAT'S YOUR SCORE?", cx, y0 + 52 * U, 54 * U, GOLD, k, fill=0.85)
    rows = [("0–7", "ROOKIE", (0.75, 0.80, 0.95)), ("8–14", "NATURE LOVER", GREEN), ("15–19", "GENIUS", CYAN), ("20/20", "LEGEND", GOLD)]
    for j, (sc, lab, col) in enumerate(rows):
        kj = lin(T, T_OUT + 0.25 + 0.18 * j, T_OUT + 0.55 + 0.18 * j)
        yy = y0 + (106 + 44 * j) * U
        text(ctx, sc, cx - 40 * U, yy, 40 * U, col, kj, align="r")
        text(ctx, lab, cx - 10 * U, yy, 40 * U, WHITE, kj, align="l")
    kc = lin(T, OUT[1]["start"] - 0.1, OUT[1]["start"] + 0.25)
    pill(ctx, "COMMENT YOUR SCORE!", cx, H * 0.745, GOLD, 40, kc, kc)

# ---------------------------------------------------------------- image complète
OWL_INTRO = (0.50, 0.400, 0.400)   # x, y du centre, hauteur (fractions de W, H, H)
OWL_QUIZ = (0.675, 0.262, 0.250)
def master(ctx, T):
    background(ctx, T)
    i, ph = phase(T)
    kt = prog(T, T_Q1 - 0.70, T_Q1 - 0.05)              # passage intro → quiz
    header(ctx, T)
    answer_list(ctx, T, i, ph, kt)
    card(ctx, T, i, ph, kt if ph != "outro" else 1 - prog(T, T_OUT, T_OUT + 0.25))
    outro_card(ctx, T)
    timer(ctx, T, i, ph)
    ox, oy, os_ = (lerp(a, b, kt) for a, b in zip(OWL_INTRO, OWL_QUIZ))
    st = owl_state(T, i, ph)
    if ph == "intro":
        k0 = lin(T, 0.0, 0.35); st["hop"] = math.sin(math.pi * k0) * 0.6 if T > 0.1 else 0.0; st["look"] = (0.0, 0.0)
    py = H * oy - st.get("hop", 0.0) * 120 * U * os_ + 6 * U * math.sin(T * 2 * math.pi * 0.6)
    owl_sprite(ctx, W * ox, py, H * os_, st)
    if ph == "intro": intro_texts(ctx, T)
    if ph == "outro":
        kf = lin(T, OUT[1]["start"] + 1.2, OUT[1]["start"] + 1.5)
        text(ctx, "FOLLOW FACTORA", W * TIM[0], H * 0.448, 34 * U, WHITE, 0.95 * kf)
        text(ctx, "FOR MORE QUIZZES", W * TIM[0], H * 0.478, 34 * U, GOLD, 0.95 * kf)

def _scene(name):
    def f(ctx, t, d): master(ctx, S0(name) + t)
    return f
SCENES = {sg["scene"]: _scene(sg["scene"]) for sg in _TLL}
SHORT_SCENES = [sg["scene"] for sg in _TLL]

def medal(ctx, x, y, r, label="GENIUS", rot=0.0):
    """Médaille d'or « GENIUS » (la récompense du défi 15/20) : rubans, disque doré, étoile, texte."""
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot)
    for sx, col in ((-1, (0.10, 0.55, 1.0)), (1, (0.95, 0.25, 0.55))):   # rubans
        ctx.new_path(); ctx.move_to(sx * r * 0.20, r * 0.55); ctx.line_to(sx * r * 0.62, r * 1.75)
        ctx.line_to(sx * r * 0.40, r * 1.55); ctx.line_to(sx * r * 0.22, r * 1.85); ctx.line_to(sx * r * -0.12, r * 0.65); ctx.close_path()
        rgba(ctx, col, 1); ctx.fill_preserve(); ctx.set_line_width(r * 0.04); rgba(ctx, (0.02, 0.02, 0.08), 0.9); ctx.stroke()
    glow(ctx, 0, 0, r * 2.2, GOLD, 0.45)
    g = cairo.RadialGradient(-r * 0.3, -r * 0.35, r * 0.1, 0, 0, r)
    g.add_color_stop_rgb(0, 1.0, 0.95, 0.60); g.add_color_stop_rgb(0.55, 1.0, 0.78, 0.18); g.add_color_stop_rgb(1, 0.80, 0.50, 0.05)
    ctx.arc(0, 0, r, 0, 2 * math.pi); ctx.set_source(g); ctx.fill_preserve()
    ctx.set_line_width(r * 0.07); rgba(ctx, (0.55, 0.32, 0.02), 1); ctx.stroke()
    ctx.arc(0, 0, r * 0.80, 0, 2 * math.pi); ctx.set_line_width(r * 0.035); rgba(ctx, (1.0, 0.95, 0.65), 0.9); ctx.stroke()
    ctx.new_path()
    for k in range(10):   # étoile
        a = -math.pi / 2 + k * math.pi / 5; rr = r * (0.36 if k % 2 == 0 else 0.15)
        (ctx.move_to if k == 0 else ctx.line_to)(rr * math.cos(a), -r * 0.20 + rr * math.sin(a))
    ctx.close_path(); rgba(ctx, (0.55, 0.32, 0.02), 1); ctx.fill()
    font(ctx, r * 0.30); w_ = ctx.text_extents(label).width
    fs = r * 0.30 * min(1.0, r * 1.35 / max(w_, 1))
    text(ctx, label, 0, r * 0.38, fs, (0.40, 0.20, 0.0))
    ctx.restore()

def cover(ctx):
    """Affiche (demande de Nazik, 2026-11-22 : annoncer la récompense pour donner envie de relever le défi) :
    « ANIMAL QUIZ », la chouette, la médaille « GENIUS », « GET 15/20 » / « = YOU'RE A GENIUS », bandeau « 20 QUESTIONS · PROVE IT! »
    (zone sûre 14–86 % de la hauteur)."""
    background(ctx, 1.0)
    owl_sprite(ctx, W * 0.43, H * 0.445, H * 0.315, {"happy": 1.0})
    medal(ctx, W * 0.765, H * 0.505, 118 * U, "GENIUS", 0.16)
    poster_text(ctx, "ANIMAL QUIZ", W * 0.5, H * 0.185, 150 * U, WHITE, W * 0.88)
    poster_text(ctx, "GET 15/20", W * 0.5, H * 0.668, 150 * U, WHITE, W * 0.86)
    poster_text(ctx, "= YOU'RE A GENIUS", W * 0.5, H * 0.742, 96 * U, GOLD, W * 0.88)
    pill(ctx, "20 QUESTIONS · PROVE IT!", W * 0.5, H * 0.815, CYAN, 54, 1.0, 1.0)
