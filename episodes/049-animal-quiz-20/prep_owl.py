"""Prépare les images de la chouette Factora (Runway, ép. 049 v2) pour l'animation.
Entrées (build/rw/owl/) : base.png, talk.png, blink.png, wing.png, happy.png (fond noir) + base_cut.png, wing_cut.png,
happy_cut.png (détourages : canal alpha). Sorties : <nom>_rgba.png recadrés sur la même boîte (alignement conservé),
le halo néon gardé en semi-transparence, et regions.json (zones du bec et des yeux, trouvées par différence avec base)."""
import sys, os, json
import numpy as np
from PIL import Image, ImageFilter

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "build", "rw", "owl")
def rgb(n): return np.asarray(Image.open(os.path.join(D, n + ".png")).convert("RGB")).astype(np.float32)
def cut_alpha(n):
    p = os.path.join(D, n + "_cut.png")
    return np.asarray(Image.open(p).convert("RGBA"))[..., 3].astype(np.float32) / 255.0

def matte(img, mask):
    """alpha = détourage (intérieur opaque) ∪ halo lumineux (luminance) à l'extérieur : le néon garde sa lueur."""
    lum = img.max(axis=2) / 255.0
    glow = np.clip((lum - 0.04) * 1.5, 0, 1)
    m = np.asarray(Image.fromarray((mask * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))).astype(np.float32) / 255
    a = np.maximum(m, glow)
    col = np.where(a[..., None] > 1e-3, np.clip(img / np.maximum(a[..., None], 1e-3), 0, 255), 0)
    col = np.where(m[..., None] > 0.5, img, col)   # à l'intérieur : couleurs d'origine
    return col, a

base = rgb("base")
out = {}
for n in ("base", "wing", "happy"):
    if not os.path.exists(os.path.join(D, n + ".png")): continue
    im = rgb(n); col, a = matte(im, cut_alpha(n))
    out[n] = (col, a)
# boîte commune (union des alphas > 0,02) + marge
ys, xs = np.where(np.maximum.reduce([v[1] for v in out.values()]) > 0.02)
pad = 24
y0, y1 = max(0, ys.min() - pad), min(base.shape[0], ys.max() + pad)
x0, x1 = max(0, xs.min() - pad), min(base.shape[1], xs.max() + pad)
for n, (col, a) in out.items():
    rgba = np.dstack([col, a * 255]).astype(np.uint8)[y0:y1, x0:x1]
    Image.fromarray(rgba, "RGBA").save(os.path.join(D, n + "_rgba.png"))
regions = {"box": [int(x0), int(y0), int(x1), int(y1)]}
for n in ("talk", "blink"):
    if not os.path.exists(os.path.join(D, n + ".png")): continue
    im = rgb(n)
    Image.fromarray(im.astype(np.uint8)[y0:y1, x0:x1], "RGB").save(os.path.join(D, n + "_crop.png"))
    diff = np.abs(im - base).max(axis=2)
    diff = np.asarray(Image.fromarray(np.clip(diff, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(6))).astype(np.float32)
    # zone du visage seulement (bec : centre ; yeux : haut du corps)
    H_, W_ = base.shape[:2]
    zy0, zy1 = (int(H_ * 0.18), int(H_ * 0.48))
    sub = diff[zy0:zy1, int(W_ * 0.15):int(W_ * 0.85)]
    yy, xx = np.where(sub > 30)
    if len(yy) == 0: continue
    bx0, bx1 = xx.min() + int(W_ * 0.15), xx.max() + int(W_ * 0.15)
    by0, by1 = yy.min() + zy0, yy.max() + zy0
    regions[n] = [int(bx0 - x0), int(by0 - y0), int(bx1 - x0), int(by1 - y0)]
    print(n, "zone", regions[n], "pixels changés hors zone :", int((diff > 30).sum() - (sub > 30).sum()))
json.dump(regions, open(os.path.join(D, "regions.json"), "w"))
print("box", regions["box"], "sprites", list(out))
