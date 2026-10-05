#!/usr/bin/env bash
set -euo pipefail
project=${1:?Uso: tools/build.sh <proyecto>}
root=$(cd "$(dirname "$0")/.." && pwd)
project_root="$root/$project"
if [[ ! -d "$project_root/video" ]]; then
  echo "Proyecto desconocido: $project" >&2
  exit 2
fi

if [[ "$project" == "genesis-01-04" ]]; then
  python3 "$project_root/herramientas/construir.py"
elif [[ -f "$project_root/herramientas/construir.mjs" ]]; then
  node "$project_root/herramientas/construir.mjs"
else
  echo "No hay constructor registrado para $project" >&2
  exit 2
fi
