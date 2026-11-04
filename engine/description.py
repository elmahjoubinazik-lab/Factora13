"""Construit la description YouTube (chapitres calculés depuis build/timeline.json).
Usage: python3 engine/description.py EPISODE_DIR  -> écrit build/description.txt"""
import sys, json
EP = sys.argv[1].rstrip("/")
meta = json.load(open(EP + "/meta.json", encoding="utf-8"))
tl = json.load(open(EP + "/build/timeline.json", encoding="utf-8"))
lines = []
for i, s in enumerate(tl):
    if s["scene"] in meta.get("chapters", {}):
        t = 0 if not lines else int(s["start"])
        lines.append(f"{t // 60:02d}:{t % 60:02d} {meta['chapters'][s['scene']]}")
d = meta["description"].replace("{CHAPITRES}", "\n".join(lines))
open(EP + "/build/description.txt", "w", encoding="utf-8").write(d)
print(d)
