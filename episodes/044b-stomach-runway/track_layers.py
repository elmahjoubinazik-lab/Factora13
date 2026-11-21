#!/usr/bin/env python3
"""Suit la position des couches dans les plans Runway (ép. 044b) pour poser les légendes sur les bonnes couches.
Usage : python3 episodes/044b-stomach-runway/track_layers.py  → build/layers.json
Pour chaque image de build/clips/<scène>/ : centre de la bande bleue (mucus) et limite cellules / muscle, mesurés dans une
bande verticale à gauche du centre (là où sont les légendes), lissés dans le temps (médiane glissante)."""
import os, json, numpy as np
from PIL import Image
EP = os.path.dirname(os.path.abspath(__file__)); B = os.path.join(EP, "build", "clips")
def measure(path):
    a = np.asarray(Image.open(path).convert("RGB")).astype(np.float32) / 255.0; h, w, _ = a.shape
    s = a[:, int(w * 0.22):int(w * 0.46)].mean(axis=1)               # profil moyen par ligne
    R, G, Bc = s[:, 0], s[:, 1], s[:, 2]
    blue = (Bc > R + 0.12) & (Bc > 0.42) & (G > 0.30)
    best, cur, start = (0, 0, 0), 0, 0
    for i, v in enumerate(blue):
        if v:
            if cur == 0: start = i
            cur += 1
            if cur > best[0]: best = (cur, start, i)
        else: cur = 0
    if best[0] < h * 0.015: return None
    muc_top, muc_bot = best[1], best[2]
    red = (R > 0.40) & (G < R * 0.52) & (Bc < R * 0.75)              # muscle (rouge sombre) sous les cellules roses
    mus = None
    for i in range(muc_bot + int(h * 0.03), h - 20):
        if red[i:i + 20].mean() > 0.85: mus = i; break
    return {"muc": (muc_top + muc_bot) / 2 / h, "muc_top": muc_top / h, "muc_bot": muc_bot / h, "mus": (mus / h) if mus else None}
out = {}
for scene in sorted(os.listdir(B)):
    d = os.path.join(B, scene)
    if not os.path.isdir(d): continue
    rows = [measure(os.path.join(d, f)) for f in sorted(os.listdir(d)) if f.endswith(".jpg")]
    def series(key):
        v = np.array([r[key] if r and r.get(key) is not None else np.nan for r in rows], dtype=float)
        idx = np.arange(len(v)); ok = ~np.isnan(v)
        if ok.sum() == 0: return [None] * len(v)
        v = np.interp(idx, idx[ok], v[ok])
        k = 9; p = np.pad(v, k // 2, mode="edge"); v = np.array([np.median(p[i:i + k]) for i in range(len(v))])
        return [round(float(x), 4) for x in v]
    out[scene] = {"muc": series("muc"), "mus": series("mus"), "muc_top": series("muc_top"), "muc_bot": series("muc_bot"),
                  "missing": int(sum(1 for r in rows if r is None))}
    m = out[scene]
    print(scene, len(rows), "images | mucus", min(m["muc"] or [0]), "→", max(m["muc"] or [0]), "| muscle", m["mus"][0], "→", m["mus"][-1], "| sans détection:", m["missing"])
json.dump(out, open(os.path.join(EP, "build", "layers.json"), "w"))
