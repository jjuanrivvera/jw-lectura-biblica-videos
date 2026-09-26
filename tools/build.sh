#!/usr/bin/env bash
set -euo pipefail
project=${1:?Uso: tools/build.sh <proyecto>}
case "$project" in
  genesis-14-18|genesis-19-23|genesis-24-28) ;;
  *) echo "Proyecto desconocido: $project" >&2; exit 2 ;;
esac
root=$(cd "$(dirname "$0")/.." && pwd)
node "$root/$project/herramientas/construir.mjs"
