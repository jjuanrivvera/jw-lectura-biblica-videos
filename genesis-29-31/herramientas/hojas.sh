#!/usr/bin/env bash
# Uso: herramientas/hojas.sh NN [NN ...]   hoja de 6 instantáneas repartidas por toda la escena.
# Una escena a la vez y hasta tres intentos: con el proyecto completo (50 escenas) y la máquina
# cargada, `snapshot` supera a veces sus 10 s de carga y la hoja sale vacía.
cd "$(dirname "$0")/.."
for n in "$@"; do
  dur=$(jq -r ".[] | select(.num==\"$n\") | .dur" video/escenas.json)
  ts=$(awk -v d="$dur" 'BEGIN{for(i=1;i<=6;i++){printf "%s%.1f", (i>1?",":""), d*(i-0.5)/6}}')
  for intento in 1 2 3; do
    herramientas/fotos.sh "$n" "$ts" && break
    echo "reintento $n ($intento)"
  done
done
