#!/usr/bin/env python3
"""Parte NARRACION.md ("## NN · título") en textos/escena-NN.txt para voz.py --textos.

Uso: herramientas/textos.py [NN ...]   (sin argumentos, todas las escenas)
"""
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
pedidas = set(sys.argv[1:])
salida = RAIZ / "textos"
salida.mkdir(exist_ok=True)
actual, lineas, escenas = None, [], {}
for l in (RAIZ / "NARRACION.md").read_text(encoding="utf-8").splitlines():
    if l.startswith("## "):
        if actual:
            escenas[actual] = lineas
        actual, lineas = l[3:].split(" · ")[0].strip(), []
    elif actual and l.strip() and not l.startswith((">", "#")):
        lineas.append(l.strip())
if actual:
    escenas[actual] = lineas
for num, ls in escenas.items():
    if pedidas and num not in pedidas:
        continue
    (salida / f"escena-{num}.txt").write_text("\n".join(ls) + "\n", encoding="utf-8")
    print(f"escena-{num}: {sum(len(x.split()) for x in ls)} palabras")
