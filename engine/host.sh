#!/usr/bin/env bash
# Dépose les fichiers d'un épisode sur la branche « media » (remplacée à chaque épisode, pour rester légère)
# et affiche leurs URL publiques. Usage: bash engine/host.sh episodes/NNN-x NNN
set -e
EP="$1"; N="$2"; REPO=$(python3 -c "import json;print(json.load(open('config.json'))['video_host_repo'])")
TMP=$(mktemp -d); mkdir -p "$TMP/ep$N"
cp "$EP/build/video_long.mp4" "$EP/build/video_short.mp4" "$EP/build/miniature.png" "$TMP/ep$N/"
cd "$TMP" && git init -q -b media && git add -A
git -c user.name="Factora" -c user.email="noreply@anthropic.com" commit -qm "Fichiers épisode $N"
git push -q -f "$(git -C "$OLDPWD" remote get-url origin)" media:media
for f in video_long.mp4 video_short.mp4 miniature.png; do
  echo "https://raw.githubusercontent.com/$REPO/media/ep$N/$f"
done
