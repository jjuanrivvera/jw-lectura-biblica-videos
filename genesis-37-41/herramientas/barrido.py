#!/usr/bin/env python3
"""Barrido del video entero: una captura cada PASO segundos y hojas de 12 cuadros rotuladas con escena y segundo.

Uso: herramientas/barrido.py [PASO]   (por defecto 6)  ->  video/snapshots/barrido-PASO/hojas/hNN.jpg

Las hojas por escena (fotos.sh) caen en momentos fijos y se saltan bloques intermedios; este barrido encontró
pantallas medio vacías y rótulos encimados que ellas no mostraban. El snapshot se parte en tandas para no pasar
del límite de 10 minutos por comando.
"""
import bisect
import glob
import json
import os
import re
import subprocess
import sys
from pathlib import Path

VIDEO = Path(__file__).resolve().parent.parent / "video"
TANDA = 170  # ~2,5 min de snapshot por tanda en esta máquina


def main():
    paso = float(sys.argv[1]) if len(sys.argv) > 1 else 6.0
    escenas = json.loads((VIDEO / "escenas.json").read_text())
    inicios = [float(e["start"]) for e in escenas]
    total = inicios[-1] + float(escenas[-1]["dur"])
    tiempos = [round(paso / 2 + i * paso, 2) for i in range(int((total - paso / 2) // paso) + 1)]
    salida = VIDEO / "snapshots" / f"barrido-{paso:g}"
    subprocess.run(["rm", "-rf", str(salida)], check=True)
    env = dict(os.environ, PATH=f"{Path.home()}/npm/bin:{os.environ['PATH']}")
    for n, i in enumerate(range(0, len(tiempos), TANDA)):
        at = ",".join(map(str, tiempos[i:i + TANDA]))
        subprocess.run(["npx", "--yes", "hyperframes@0.8.91", "snapshot", "--describe", "false", "--no-end",
                        "--at", at, "-o", str(salida / f"t{n}")], cwd=VIDEO, env=env, check=True,
                       stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # Los nombres (frame-NN-at-T.png) pasan de dos cifras: ordenar por el tiempo, no por el texto.
    cuadros = sorted((float(re.search(r"at-([\d.]+)s", f).group(1)), f)
                     for f in glob.glob(str(salida / "t*" / "frame-*.png")))
    (salida / "hojas").mkdir(parents=True, exist_ok=True)
    for h in range(0, len(cuadros), 12):
        grupo = cuadros[h:h + 12]
        if len(grupo) < 2:
            break
        entradas, filtro = [], ""
        for k, (t, f) in enumerate(grupo):
            e = escenas[bisect.bisect_right(inicios, t) - 1]
            entradas += ["-i", f]
            filtro += (f"[{k}]scale=640:360,drawtext=text='{e['num']} +{t - float(e['start']):.0f}s':x=8:y=8:"
                       f"fontsize=28:fontcolor=yellow:box=1:boxcolor=black@0.6[v{k}];")
        filtro += "".join(f"[v{k}]" for k in range(len(grupo)))
        filtro += f"xstack=inputs={len(grupo)}:layout=" + "|".join(
            f"{(k % 3) * 640}_{(k // 3) * 360}" for k in range(len(grupo))) + ":fill=black"
        subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", *entradas, "-filter_complex", filtro,
                        "-frames:v", "1", str(salida / "hojas" / f"h{h // 12:02d}.jpg")], check=True)
    print(f"{len(cuadros)} cuadros en {salida / 'hojas'}")


if __name__ == "__main__":
    main()
