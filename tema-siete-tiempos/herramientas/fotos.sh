#!/usr/bin/env bash
# Uso: herramientas/fotos.sh NN "t1,t2,..."   (segundos relativos al inicio de la escena NN)
# Toma snapshots con HyperFrames y arma una hoja de contacto en video/snapshots/NN.jpg
set -e
cd "$(dirname "$0")/../video"
n=$1; rel=$2
start=$(jq -r ".[] | select(.num==\"$n\") | .start" escenas.json)
abs=$(echo "$rel" | tr ',' '\n' | awk -v s="$start" '{printf "%s%.2f", (NR>1?",":""), s+$1}')
dir="snapshots/tmp-$n"
python3 -c "import pathlib,sys; [p.unlink() for p in pathlib.Path(sys.argv[1]).glob('frame-*.png')]" "$dir" 2>/dev/null || true
npx --yes hyperframes@0.8.127 snapshot --describe false --no-end --at "$abs" -o "$dir" >/dev/null 2>&1
cnt=$(ls $dir/frame-*.png | wc -l)
cols=$(( cnt < 3 ? cnt : 3 ))
rows=$(( (cnt + cols - 1) / cols ))
ffmpeg -v error -y -pattern_type glob -i "$dir/frame-*.png" -vf "scale=640:360,drawtext=text='%{n}':x=8:y=8:fontsize=28:fontcolor=yellow,tile=${cols}x${rows}:padding=6" -frames:v 1 "snapshots/$n.jpg"
echo "snapshots/$n.jpg ($cnt cuadros, desde $start s)"
