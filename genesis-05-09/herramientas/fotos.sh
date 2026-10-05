#!/usr/bin/env bash
# Uso: herramientas/fotos.sh NN "t1,t2,..."   (tiempos relativos al inicio de la escena NN)
# Toma snapshots y arma una hoja de contacto en $VIDEO/snapshots/NN.jpg (VIDEO=video por defecto;
# VIDEO=video-sub para el proyecto reducido de herramientas/sub.py).
cd "$(dirname "$0")/../${VIDEO:-video}"
n=$1; rel=$2
start=$(jq -r ".[] | select(.num==\"$n\") | .start" escenas.json)
abs=$(echo "$rel" | tr ',' '\n' | awk -v s="$start" '{printf "%s%.2f", (NR>1?",":""), s+$1}')
rm -rf "snapshots/tmp-$n"
# A veces la captura sale vacía sin error: se reintenta hasta tres veces.
for intento in 1 2 3; do
  npx --yes hyperframes@0.8.78 snapshot --describe false --no-end --at "$abs" -o "snapshots/tmp-$n" >/dev/null 2>&1 || true
  ls snapshots/tmp-$n/frame-*.png >/dev/null 2>&1 && break
done
cnt=$(ls snapshots/tmp-$n/frame-*.png 2>/dev/null | wc -l)
[ "$cnt" -gt 0 ] || { echo "FALLO $n"; exit 1; }
cols=$(( cnt < 3 ? cnt : 3 ))
rows=$(( (cnt + cols - 1) / cols ))
mkdir -p ../video/snapshots
ffmpeg -v error -y -pattern_type glob -i "snapshots/tmp-$n/frame-*.png" -vf "scale=640:360,drawtext=text='%{n}':x=8:y=8:fontsize=28:fontcolor=yellow,tile=${cols}x${rows}:padding=6" -frames:v 1 "../video/snapshots/$n.jpg"
echo "snapshots/$n.jpg ($cnt cuadros, desde $start s)"
