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
mkdir -p "ep$N"; for f in video_long.mp4 video_short.mp4 miniature.png short_cover.jpg; do [ -f "$EP/build/$f" ] && cp "$EP/build/$f" "ep$N/"; done
git add "ep$N" && git -c user.name="Factora" -c user.email="noreply@anthropic.com" commit -qm "Fichiers épisode $N"
git push -q "$R" HEAD:backlog 2>&1 | grep -v "^remote:" >&2 || true
SHA=$(git rev-parse HEAD)
for f in video_long.mp4 video_short.mp4 miniature.png short_cover.jpg; do [ -f "ep$N/$f" ] && echo "https://raw.githubusercontent.com/$REPO/$SHA/ep$N/$f"; done
