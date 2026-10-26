#!/usr/bin/env bash
# Resize photos to fit 1024x1024 (keeping aspect ratio), convert them to .jpg,
# and sync the project to the photo frame.
#
# Usage: ./gallery-sync.sh [SOURCE_DIR] [IMAGES_DIR]
#   SOURCE_DIR  original photos  (default: ~/GoogleDrive/photo-frame)
#   IMAGES_DIR  resized output   (default: <this repo>/images)
set -euo pipefail
shopt -s nullglob nocaseglob

REPO_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
SRC=${1:-$HOME/GoogleDrive/photo-frame}
DEST=${2:-$REPO_DIR/images}

if command -v magick >/dev/null; then IM=magick; else IM=convert; fi

[[ -d $SRC ]] || { echo "Source dir not found: $SRC" >&2; exit 1; }
mkdir -p "$DEST"
SRC=$(cd "$SRC" && pwd)
DEST=$(cd "$DEST" && pwd)

declare -A seen
count=0
for f in "$SRC"/*.{jpg,jpeg,png,heic,webp,tif,tiff}; do
  out="$DEST/$(basename "${f%.*}").jpg"
  if [[ -n ${seen[$out]:-} ]]; then
    echo "skip: $(basename "$f") (another file already produced $(basename "$out"))" >&2
    continue
  fi
  seen[$out]=1
  "$IM" "$f" -auto-orient -resize '1024x1024>' -strip -quality 85 "$out"
  echo "converted: $(basename "$f") -> $(basename "$out")"
  count=$((count + 1))
done
echo "Converted $count photo(s)"
