"""Description YouTube optimisée SEO d'un Short ou d'une vidéo longue (règles de Nazik, 2026-11-13).
Usage : python3 engine/seo.py episodes/NNN-x [short|long]  ->  build/description_<mode>.txt (et affichage)
Champs de meta_en.json utilisés :
  seo_intro   : 2 lignes rédigées à la main — ligne 1 = la question telle qu'on la tape dans la recherche,
                ligne 2 = la réponse résumée en une phrase avec les mots-clés (objet, phénomène, lieu)
  theme       : clé de config.json → playlists (brain, whos_lying, hygiene, what_if, how, why)
  related     : ids YouTube de vidéos proches de la chaîne (vidéos longues d'abord), 2 à 4
  hashtags    : 3 à 5 hashtags DU SUJET, les plus proches du titre, différents d'une vidéo à l'autre
  sources_text (sources nommées) ou sources, ai_generated
La transcription complète vient de script_en.json (segments gardés dans le Short en mode short)."""
import sys, json, os, glob, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EP = sys.argv[1].rstrip("/"); MODE = sys.argv[2] if len(sys.argv) > 2 else "short"
cfg = json.load(open(os.path.join(ROOT, "config.json"), encoding="utf-8"))
meta = json.load(open(EP + "/meta_en.json", encoding="utf-8"))
script = json.load(open(EP + "/script_en.json", encoding="utf-8"))
keep = None
if MODE == "short" and os.path.exists(EP + "/scenes.py"):
    m = re.search(r"SHORT_SCENES\s*=\s*\[([^\]]*)\]", open(EP + "/scenes.py", encoding="utf-8").read())
    if m: keep = re.findall(r"[\"']([\w-]+)[\"']", m.group(1))
seen, words = set(), []
for seg in script:
    if keep and seg["scene"] not in keep: continue
    for s in seg["text"]:
        if s not in seen: seen.add(s); words.append(s)
transcript = " ".join(words)
# titres des vidéos de la chaîne (id → titre), d'après les meta des épisodes et published.json
titles, vtheme = {}, {}   # vtheme : id → thème (playlist qui contient la vidéo ; published.json → theme, sinon meta.playlist)
pub = json.load(open(os.path.join(ROOT, "published.json"), encoding="utf-8"))
pub = pub if isinstance(pub, list) else pub.get("episodes", [])
for e in pub:
    try: m_ = json.load(open(os.path.join(ROOT, e["dir"], "meta_en.json"), encoding="utf-8"))
    except Exception: m_ = {}
    if e.get("short_id"): titles[e["short_id"]] = re.sub(r"\s*#shorts\s*$", "", m_.get("short_title") or e.get("topic", ""))
    if e.get("long_id"): titles[e["long_id"]] = m_.get("title") or e.get("topic", "")
    th = e.get("theme") or m_.get("theme") or m_.get("playlist")
    for vid in (e.get("short_id"), e.get("long_id")):
        if vid and th: vtheme[vid] = th
pl = cfg["playlists"].get(meta.get("theme", ""), {})
out = [meta["seo_intro"].strip(), ""]
if pl:
    out += [f"▶ Watch the whole playlist, {pl['titre']}: https://www.youtube.com/playlist?list={pl['id']}",
            "Click the playlist link above to binge every video on this topic, one after another.", ""]
rel = [r for r in meta.get("related", []) if r]
if rel:
    out.append("More videos like this:")
    for r in rel:
        rp = cfg["playlists"].get(vtheme.get(r, ""), {})     # deep link dans la playlist qui contient vraiment la vidéo
        url = f"https://www.youtube.com/watch?v={r}" + (f"&list={rp['id']}" if rp else "")
        out.append(f"• {titles.get(r, 'Watch next')}: {url}")
    out.append("")
if meta.get("yesterday"):   # série « Can you solve it? » : lien vers l'énigme de la veille
    out += [f"Yesterday's riddle: https://youtube.com/shorts/{meta['yesterday']}", ""]
out += ["Full transcript:", transcript, ""]
src = meta.get("sources_text") or meta.get("sources")   # sources_text : sources nommées (plus lisibles que des URL)
if src:
    out.append("Sources: " + (src if isinstance(src, str) else "; ".join(src))); out.append("")
out.append("Think fast. Learn something amazing.")
if meta.get("ai_generated"): out.append("Created with AI tools. Synthetic voice.")   # sinon : aucune mention (décision de Nazik, 2026-11-13)
tags = meta.get("hashtags", [])
assert 3 <= len(tags) <= 5, "hashtags : 3 à 5 (règle de Nazik)"
out += ["", " ".join(t if t.startswith("#") else "#" + t for t in tags)]
d = "\n".join(out)
assert len(d) <= 5000, f"description trop longue ({len(d)} > 5000)"
open(EP + f"/build/description_{MODE}.txt", "w", encoding="utf-8").write(d)
print(d)
