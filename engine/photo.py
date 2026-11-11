# Factora — aides pour les scènes filmées (clips générés avec Runway, mode Runway décidé par Nazik le 2026-11-11).
# À exécuter depuis le scenes.py d'un épisode : exec(open("engine/photo.py", encoding="utf-8").read())
# (scenes.py est lui-même exécuté dans render.py / cover.py : EP, W, H, U, CX, CY, cairo, os… sont disponibles).
# Les images des clips sont préparées par engine/clips.py dans build/clips/<scène>/0001.jpg… (30 i/s, recalées sur la scène).
import numpy as _np
from PIL import Image as _Img

CLIPS = os.path.join(EP, "build", "clips")
RW = os.path.join(EP, "build", "rw")
_IMG, _NF = {}, {}

def load_img(path):
    """Image (jpg/png) → surface cairo, avec un petit cache."""
    if path in _IMG: return _IMG[path][0]
    if len(_IMG) > 12: _IMG.clear()
    a = _np.asarray(_Img.open(path).convert("RGB")); h, w = a.shape[:2]
    buf = _np.empty((h, w, 4), _np.uint8); buf[..., 0] = a[..., 2]; buf[..., 1] = a[..., 1]; buf[..., 2] = a[..., 0]; buf[..., 3] = 255
    surf = cairo.ImageSurface.create_for_data(memoryview(buf), cairo.FORMAT_ARGB32, w, h, w * 4)
    _IMG[path] = (surf, buf)
    return surf

def frame(name, t):
    """Image du clip `name` au temps local t de la scène."""
    if name not in _NF: _NF[name] = len([f for f in os.listdir(os.path.join(CLIPS, name)) if f.endswith(".jpg")])
    i = max(1, min(_NF[name], int(t * 30) + 1))
    return load_img(os.path.join(CLIPS, name, f"{i:04d}.jpg"))

def paint(ctx, surf, fx=0.5, fy=0.5, zoom=1.0, a=1.0):
    """Peint l'image en couvrant tout le cadre ; (fx, fy) = point de l'image au centre (borné : jamais de bord noir)."""
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
    """Titre court sur un cartouche sombre arrondi."""
    if a <= 0: return
    font(ctx, size); e = ctx.text_extents(s)
    rrect(ctx, x - e.width / 2 - 30 * U, y - size * 0.75, e.width + 60 * U, size * 1.5, size * 0.5); rgba(ctx, (0.02, 0.02, 0.04), 0.80 * a); ctx.fill()
    text(ctx, s, x, y, size, col, a)

def with_cam(fn, push=0.04, punch=0.06):
    """Léger push-in + « coup de zoom » à l'entrée de la scène."""
    def sc(ctx, t, d):
        z = (1 + push * clamp(t / max(d, 0.1))) * (1 + punch * math.exp(-t * 9))
        ctx.save(); ctx.translate(CX, CY); ctx.scale(z, z); ctx.translate(-CX, -CY)
        fn(ctx, t, d)
        ctx.restore()
    return sc

def clip_scene(name, overlay=None, push=0.04, punch=0.06, top_scrim=0.0, cover_t=None):
    """Scène standard : le clip `name` en plein cadre (+ zoom), puis les titres `overlay(ctx, t, d)` par-dessus.
    cover_t : instant du clip montré sur les 2 premières images de la vidéo (vignette Instagram/TikTok)."""
    def bg(ctx, t, d):
        paint(ctx, frame(name, cover_t if (cover_t is not None and TNOW < 2.0 / FPS) else t))
        if top_scrim: scrim(ctx, top_scrim)
    cam = with_cam(bg, push, punch)
    def sc(ctx, t, d):
        cam(ctx, t, d)
        if overlay: overlay(ctx, t, d)
    return sc

def loop_outro(line1, line2, darken=0.55):
    """Conclusion : 1re image de l'accroche floutée (la fin renvoie au début → boucle) + CTA chouette du moteur."""
    def sc(ctx, t, d):
        paint(ctx, load_img(os.path.join(CLIPS, "outro_bg.jpg")), zoom=1.0 + 0.02 * t)
        rgba(ctx, (0.02, 0.03, 0.10), darken); ctx.paint()
        cta(ctx, t, d, line1, line2)
    return sc

def poster_text(ctx, s, x, y, size, col, maxw=None):
    """Titre d'affiche : lettres énormes, contour noir épais + ombre portée ; réduit si plus large que maxw."""
    font(ctx, size); w = ctx.text_extents(s).width
    if maxw and w > maxw: size *= maxw / w; font(ctx, size); w = ctx.text_extents(s).width
    e = ctx.text_extents(s); x0 = x - e.width / 2 - e.x_bearing; y0 = y + size * 0.35
    ctx.save(); ctx.translate(10 * U, 14 * U); ctx.move_to(x0, y0); ctx.text_path(s); rgba(ctx, (0, 0, 0), 0.75)
    ctx.set_line_width(size * 0.20); ctx.set_line_join(cairo.LINE_JOIN_ROUND); ctx.stroke_preserve(); ctx.fill(); ctx.restore()
    ctx.move_to(x0, y0); ctx.text_path(s); rgba(ctx, (0.01, 0.01, 0.02), 1); ctx.set_line_width(size * 0.16)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND); ctx.stroke_preserve(); rgba(ctx, col, 1); ctx.fill()
    return size, w

def red_arrow(ctx, x0, y0, x1, y1, bend=0.25, width=26):
    """Flèche rouge épaisse et courbe (pointe en (x1, y1)) pour les affiches."""
    mx, my = (x0 + x1) / 2 + (y1 - y0) * bend, (y0 + y1) / 2 - (x1 - x0) * bend
    ang = math.atan2(y1 - my, x1 - mx); hl = width * 3.2 * U
    ex, ey = x1 - math.cos(ang) * hl * 0.6, y1 - math.sin(ang) * hl * 0.6
    for col, lw, a in (((0, 0, 0), width * 1.7, 0.85), ((1.0, 0.16, 0.16), width, 1.0)):
        ctx.new_path(); ctx.move_to(x0, y0); ctx.curve_to(mx, my, mx, my, ex, ey)
        ctx.set_line_width(lw * U); ctx.set_line_cap(cairo.LINE_CAP_ROUND); rgba(ctx, col, a); ctx.stroke()
    for col, grow in (((0, 0, 0), 1.25), ((1.0, 0.16, 0.16), 1.0)):
        h = hl * grow; ctx.new_path(); ctx.move_to(x1 + math.cos(ang) * (grow - 1) * hl * 0.5, y1 + math.sin(ang) * (grow - 1) * hl * 0.5)
        ctx.line_to(x1 - math.cos(ang - 0.45) * h, y1 - math.sin(ang - 0.45) * h); ctx.line_to(x1 - math.cos(ang + 0.45) * h, y1 - math.sin(ang + 0.45) * h)
        ctx.close_path(); rgba(ctx, col, 1); ctx.fill()
