#!/usr/bin/env bash
# Héberge les fichiers d'un épisode sur la branche durable « backlog » (ajout, jamais d'écrasement)
# et affiche leurs 3 URL publiques, figées sur le commit. Usage: bash engine/host.sh episodes/NNN-x NNN
set -e
EP="$(cd "$1" && pwd)"; N="$2"
REPO=$(python3 -c "import json;print(json.load(open('config.json'))['video_host_repo'])")
R="https://github.com/$REPO"
# Dossier temporaire supprimé à la fin (avant le 2026-11-10, chaque appel laissait ~1 Go dans /tmp → disque plein)
TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT; cd "$TMP"; git init -q -b backlog
# On récupère seulement l'historique (sans extraire les anciennes vidéos sur le disque) : index = arbre distant
if git fetch -q --depth 1 --filter=blob:none "$R" backlog 2>/dev/null || git fetch -q --depth 1 "$R" backlog 2>/dev/null; then
  git update-ref refs/heads/backlog FETCH_HEAD; git read-tree backlog
fi
# Fichiers vidéo nommés comme le titre de la vidéo (règle de Nazik, 2026-11-13) : build/<titre>.mp4 est aussi créé (pour TikTok/X)
slug() { python3 -c "import json,re,sys;m=json.load(open('$EP/meta_en.json',encoding='utf-8'));t=m.get(sys.argv[1]) or m.get('title') or 'video';t=re.sub(r'#\\w+','',t);t=re.sub(r'[^a-z0-9]+','-',t.lower()).strip('-');print(t[:90] or 'video')" "$1"; }
mkdir -p "ep$N"
[ -f "$EP/build/video_short.mp4" ] && S=$(slug short_title) && cp "$EP/build/video_short.mp4" "ep$N/$S.mp4" && cp "$EP/build/video_short.mp4" "$EP/build/$S.mp4"
[ -f "$EP/build/video_long.mp4" ] && L=$(slug title) && cp "$EP/build/video_long.mp4" "ep$N/$L.mp4" && cp "$EP/build/video_long.mp4" "$EP/build/$L.mp4"
for f in miniature.png short_cover.jpg short_cover_yt.jpg; do [ -f "$EP/build/$f" ] && cp "$EP/build/$f" "ep$N/"; done
git add "ep$N" && git -c user.name="Factora" -c user.email="noreply@anthropic.com" commit -qm "Fichiers épisode $N"
git push -q "$R" HEAD:backlog 2>&1 | grep -v "^remote:" >&2 || true
SHA=$(git rev-parse HEAD)
[ -n "$L" ] && echo "long: https://raw.githubusercontent.com/$REPO/$SHA/ep$N/$L.mp4"
[ -n "$S" ] && echo "short: https://raw.githubusercontent.com/$REPO/$SHA/ep$N/$S.mp4"
for f in miniature.png short_cover.jpg short_cover_yt.jpg; do [ -f "ep$N/$f" ] && echo "${f%%.*}: https://raw.githubusercontent.com/$REPO/$SHA/ep$N/$f"; done; true
