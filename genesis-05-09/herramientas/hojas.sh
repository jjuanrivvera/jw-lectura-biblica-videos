#!/usr/bin/env bash
# Uso: herramientas/hojas.sh NN [NN ...]   hoja de 6 instantáneas repartidas por toda la escena.
# De una en una: en paralelo, el navegador de snapshot a veces falla sin avisar.
cd "$(dirname "$0")/.."
for n in "$@"; do
  dur=$(jq -r ".[] | select(.num==\"$n\") | .dur" "${VIDEO:-video}/escenas.json")
  ts=$(awk -v d="$dur" 'BEGIN{for(i=1;i<=6;i++){printf "%s%.1f", (i>1?",":""), d*(i-0.5)/6}}')
  herramientas/fotos.sh "$n" "$ts" || echo "FALLO $n"
done
