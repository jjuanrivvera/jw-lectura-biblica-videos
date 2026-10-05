#!/usr/bin/env python3
"""Barrido del video entero: una captura cada PASO segundos, en hojas de 12 rotuladas con escena y segundo.

Uso: herramientas/barrido.py [PASO] [DESDE] [HASTA]  ->  video/snapshots/barrido/hNN.jpg

Las hojas por escena caen en instantes fijos y se saltan tramos; el barrido encuentra pantallas medio vacías
y rótulos encimados que ellas no muestran (notas de Génesis 37-41). El snapshot va en tandas para no pasar
de 10 minutos por comando. Las hojas las arma herramientas-comunes/revision.py.
"""
import bisect
import glob
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

VIDEO = Path(__file__).resolve().parent.parent / "video"
sys.path.insert(0, str(Path.home() / "jw-video/herramientas-comunes"))
from revision import hoja_de_contacto  # noqa: E402

TANDA = 150


def main():
    paso = float(sys.argv[1]) if len(sys.argv) > 1 else 8.0
    escenas = json.loads((VIDEO / "escenas.json").read_text())
    inicios = [float(e["start"]) for e in escenas]
    total = inicios[-1] + float(escenas[-1]["dur"])
    desde = float(sys.argv[2]) if len(sys.argv) > 2 else 0.0
    hasta = float(sys.argv[3]) if len(sys.argv) > 3 else total
    tiempos = [round(paso / 2 + i * paso, 2) for i in range(int((total - paso / 2) // paso) + 1)]
    tiempos = [t for t in tiempos if desde <= t < hasta]
    salida = VIDEO / "snapshots" / "barrido"
    tmp = salida / "tmp"
    shutil.rmtree(tmp, ignore_errors=True)
    for n, i in enumerate(range(0, len(tiempos), TANDA)):
        at = ",".join(f"{t:.2f}" for t in tiempos[i:i + TANDA])
        subprocess.run(["npx", "--yes", "hyperframes@0.8.96", "snapshot", "--describe", "false", "--no-end",
                        "--at", at, "-o", str(tmp / f"t{n}")], cwd=VIDEO, check=True,
                       stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # Los nombres pasan de dos cifras: ordenar por el tiempo, no por el texto.
    cuadros = sorted((float(re.search(r"at-([\d.]+)s", f).group(1)), f) for f in glob.glob(str(tmp / "t*" / "frame-*.png")))
    salida.mkdir(parents=True, exist_ok=True)
    for h in range(0, len(cuadros), 12):
        grupo = cuadros[h:h + 12]
        etq = []
        for t, _ in grupo:
            k = bisect.bisect_right(inicios, t) - 1
            etq.append(f"{escenas[k]['num']} · {t - inicios[k]:.0f}s")
        destino = salida / f"h{int(desde) // 100:02d}-{h // 12:02d}.jpg"
        hoja_de_contacto([f for _, f in grupo], etq, destino, cols=4, ancho_celda=480, alto_celda=270)
        print(destino)


if __name__ == "__main__":
    main()
