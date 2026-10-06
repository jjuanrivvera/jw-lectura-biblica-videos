#!/usr/bin/env bash
# Uso: herramientas/hojas.sh NN [NN ...]   hoja de 6 instantáneas repartidas por toda la escena.
# De dos en dos; si una hoja sale vacía (el navegador de snapshot falla a veces sin avisar), se repite sola.
cd "$(dirname "$0")/.."
una() {
  local n=$1
  dur=$(jq -r ".[] | select(.num==\"$n\") | .dur" video/escenas.json)
  ts=$(awk -v d="$dur" 'BEGIN{for(i=1;i<=6;i++){printf "%s%.1f", (i>1?",":""), d*(i-0.5)/6}}')
  for intento in 1 2 3; do
    herramientas/fotos.sh "$n" "$ts" 2>/dev/null && return 0
  done
  echo "FALLÓ $n"
}
while [ $# -gt 0 ]; do
  for n in "${@:1:2}"; do una "$n" & done
  wait
  shift $(( $# < 2 ? $# : 2 ))
done
