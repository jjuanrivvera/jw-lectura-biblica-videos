#!/usr/bin/env python3
"""Instantáneas de escenas en segundos relativos y una hoja de contacto.

  fotos.py 03 "5,20,41" 04 "10,30"   -> snapshots/hoja-03-04.jpg

Los tiempos son relativos al inicio de cada escena (video/escenas.json, que escribe construir.mjs).
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
VID = RAIZ / "video"
HC = Path.home() / "jw-video/herramientas-comunes/revision.py"

args = sys.argv[1:]
escenas = {e["num"]: e for e in json.loads((VID / "escenas.json").read_text())}
tiempos = []
for num, lista in zip(args[0::2], args[1::2]):
    e = escenas[num]
    for t in lista.split(","):
        tiempos.append(round(e["start"] + min(float(t), e["dur"] - 0.6), 2))

out = Path(tempfile.mkdtemp(prefix="fotos-"))
subprocess.run(["npx", "--yes", "hyperframes@0.8.124", "snapshot", "--at", ",".join(map(str, tiempos)),
                "--no-end", "--describe", "false", "-o", str(out), str(VID)],
               check=True, capture_output=True)
(out / "contact-sheet.jpg").unlink(missing_ok=True)
(RAIZ / "snapshots").mkdir(exist_ok=True)
hoja = RAIZ / "snapshots" / f"hoja-{'-'.join(args[0::2])}.jpg"
subprocess.run(["python3", str(HC), "hoja", "--imagenes", str(out), "--salida", str(hoja), "--cols", "3"], check=True,
               capture_output=True)
print(hoja)
