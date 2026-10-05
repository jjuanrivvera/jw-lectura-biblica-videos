#!/usr/bin/env bash
set -euo pipefail
project=${1:?Uso: tools/render.sh <proyecto>}
root=$(cd "$(dirname "$0")/.." && pwd)
video="$root/$project/video"
if [[ ! -f "$video/package.json" ]]; then
  echo "Proyecto desconocido: $project" >&2
  exit 2
fi
cd "$video"
npm run check
npm run render
