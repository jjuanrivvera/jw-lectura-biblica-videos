#!/usr/bin/env bash
# Uso: herramientas/fotos.sh NN "t1,t2,..."   (tiempos relativos al inicio de la escena NN)
# Toma snapshots y arma una hoja de contacto en video/snapshots/NN.jpg
set -e
cd "$(dirname "$0")/../video"
n=$1; rel=$2
start=$(jq -r ".[] | select(.num==\"$n\") | .start" escenas.json)
abs=$(echo "$rel" | tr ',' '\n' | awk -v s="$start" '{printf "%s%.2f", (NR>1?",":""), s+$1}')
rm -rf "snapshots/tmp-$n"
npx --yes hyperframes@0.8.72 snapshot --describe false --no-end --at "$abs" -o "snapshots/tmp-$n" >/dev/null 2>&1
cnt=$(ls snapshots/tmp-$n/frame-*.png | wc -l)
cols=$(( cnt < 4 ? cnt : 4 ))
rows=$(( (cnt + cols - 1) / cols ))
ffmpeg -v error -y -pattern_type glob -i "snapshots/tmp-$n/frame-*.png" -vf "scale=432:768,drawtext=text='%{n}':x=8:y=8:fontsize=28:fontcolor=yellow,tile=${cols}x${rows}:padding=6" -frames:v 1 "snapshots/$n.jpg"
echo "snapshots/$n.jpg ($cnt cuadros, desde $start s)"
