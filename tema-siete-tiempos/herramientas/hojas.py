#!/usr/bin/env python3
"""Hojas de contacto de todas las escenas: un snapshot de HyperFrames con N instantes por escena
y una hoja por escena en video/snapshots/hojas/NN.jpg, rotulada con el segundo relativo."""
import json, subprocess, sys, pathlib
raiz = pathlib.Path(__file__).resolve().parent.parent
vid = raiz / "video"
escenas = json.loads((vid / "escenas.json").read_text())
solo = set(sys.argv[1:])
fr = [0.08, 0.22, 0.36, 0.5, 0.64, 0.78, 0.92]
marcas = []
for e in escenas:
    if solo and e["num"] not in solo: continue
    for f in fr:
        marcas.append((e["num"], round(e["dur"] * f, 2), round(e["start"] + e["dur"] * f, 2)))
out = vid / "snapshots" / "todo"
out.mkdir(parents=True, exist_ok=True)
for p in out.glob("frame-*.png"): p.unlink()
subprocess.run(["npx", "--yes", "hyperframes@0.8.127", "snapshot", "--describe", "false", "--no-end",
                "--at", ",".join(str(m[2]) for m in marcas), "-o", str(out)], cwd=vid, check=True,
               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
import re
# Los nombres son frame-NN-at-Xs.png con NN de dos cifras: el orden alfabético se rompe desde 100.
frames = sorted(out.glob("frame-*.png"), key=lambda p: int(re.match(r"frame-(\d+)", p.name).group(1)))
assert len(frames) == len(marcas), (len(frames), len(marcas))
hojas = vid / "snapshots" / "hojas"; hojas.mkdir(exist_ok=True)
por = {}
for (n, rel, _), f in zip(marcas, frames): por.setdefault(n, []).append((rel, f))
for n, lst in por.items():
    args = ["ffmpeg", "-v", "error", "-y"]
    for _, f in lst: args += ["-i", str(f)]
    filt = "".join(f"[{i}:v]scale=960:540,drawtext=text='{n} t={rel}s':x=8:y=8:fontsize=34:fontcolor=yellow:box=1:boxcolor=black@0.6[v{i}];" for i, (rel, _) in enumerate(lst))
    filt += "".join(f"[v{i}]" for i in range(len(lst))) + f"xstack=inputs={len(lst)}:layout=" + "|".join(f"{(i%2)*960}_{(i//2)*540}" for i in range(len(lst))) + ":fill=black[o]"
    args += ["-filter_complex", filt, "-map", "[o]", str(hojas / f"{n}.jpg")]
    subprocess.run(args, check=True)
print(f"{len(por)} hojas en {hojas}")
