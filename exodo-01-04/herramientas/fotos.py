#!/usr/bin/env python3
"""Hojas de contacto por escena, con una sola pasada de `hyperframes snapshot` para varias escenas.

Uso:
  herramientas/fotos.py 00 01 02            6 instantes repartidos por cada escena
  herramientas/fotos.py 04 --n 9            9 instantes
  herramientas/fotos.py 04 --t 3.5,12,20    instantes relativos al inicio de la escena
  herramientas/fotos.py 00-12               un rango

Salida: video/snapshots/hojas/NN.jpg (rejilla rotulada "NN · segundo"). La hoja la arma
herramientas-comunes/revision.py; aquí solo se decide qué instantes capturar.
"""
import argparse
import glob
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
VIDEO = RAIZ / "video"
sys.path.insert(0, str(Path.home() / "jw-video/herramientas-comunes"))
from revision import hoja_de_contacto  # noqa: E402


def escenas_pedidas(args):
    out = []
    for a in args:
        if "-" in a:
            i, j = a.split("-")
            out += [f"{k:02d}" for k in range(int(i), int(j) + 1)]
        else:
            out.append(f"{int(a):02d}")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("escenas", nargs="+")
    ap.add_argument("--n", type=int, default=6)
    ap.add_argument("--t", help="tiempos relativos, separados por coma (solo con una escena)")
    ap.add_argument("--cols", type=int, default=3)
    a = ap.parse_args()
    datos = {e["num"]: e for e in json.loads((VIDEO / "escenas.json").read_text())}
    pedidos = [n for n in escenas_pedidas(a.escenas) if n in datos]
    plan = []  # (num, relativo, absoluto)
    for n in pedidos:
        e = datos[n]
        rel = [float(x) for x in a.t.split(",")] if a.t else [round(e["dur"] * (i + 0.5) / a.n, 2) for i in range(a.n)]
        plan += [(n, r, round(e["start"] + r, 2)) for r in rel]
    # Una carpeta por tanda: un revisor puede estar leyendo los cuadros de otra.
    tmp = VIDEO / "snapshots" / f"tmp-{pedidos[0]}-{pedidos[-1]}"
    shutil.rmtree(tmp, ignore_errors=True)
    at = ",".join(f"{p[2]:.2f}" for p in plan)
    subprocess.run(["npx", "--yes", "hyperframes@0.8.127", "snapshot", "--describe", "false", "--no-end",
                    "--at", at, "-o", str(tmp)], cwd=VIDEO, check=True,
                   stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    cuadros = sorted((float(re.search(r"at-([\d.]+)s", f).group(1)), f) for f in glob.glob(str(tmp / "frame-*.png")))
    por_t = {round(t, 2): f for t, f in cuadros}
    destino = VIDEO / "snapshots" / "hojas"
    destino.mkdir(parents=True, exist_ok=True)
    for n in pedidos:
        mios = [(r, por_t.get(ab)) for (m, r, ab) in plan if m == n]
        mios = [(r, f) for r, f in mios if f]
        if not mios:
            print(f"{n}: sin cuadros")
            continue
        hoja_de_contacto([f for _, f in mios], [f"{n} · {r:.1f}s" for r, _ in mios], destino / f"{n}.jpg", cols=a.cols)
        print(destino / f"{n}.jpg")


if __name__ == "__main__":
    main()
