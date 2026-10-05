#!/usr/bin/env python3
"""Proyecto reducido para instantáneas cuando la máquina está cargada: solo las escenas pedidas, una detrás de otra.
Uso: herramientas/sub.py NN [NN ...]  → video-sub/ (enlaces a assets, audio y compositions) con su index.html y
escenas.json. Luego: herramientas/hojas.sh con VIDEO=video-sub."""
import json, os, re, sys
from pathlib import Path

R = Path(__file__).resolve().parent.parent
V, S = R / "video", R / "video-sub"
S.mkdir(exist_ok=True)
for d in ("assets", "audio", "compositions"):
    if not (S / d).exists():
        os.symlink(V / d, S / d)
for f in ("package.json", "hyperframes.json", "meta.json"):
    (S / f).write_text((V / f).read_text())
esc = {e["num"]: e for e in json.loads((V / "escenas.json").read_text())}
idx = (V / "index.html").read_text()
t, hosts, out = 0.0, [], []
for n in sys.argv[1:]:
    e = esc[n]
    h = re.search(rf'<div id="h-{n}"[^>]*></div>', idx).group(0)
    hosts.append(re.sub(r'data-start="[\d.]+"', f'data-start="{t:.3f}"', h))
    out.append({**e, "start": round(t, 3)})
    t += e["dur"]
cuerpo = re.sub(r'(<div id="grano"></div>\n)[\s\S]*?(\n    </div>\n    <script>)', lambda m: m.group(1) + "\n".join(hosts) + m.group(2), idx)
cuerpo = re.sub(r'data-duration="[\d.]+"( data-width="1920" data-height="1080">\n      <div id="pizarra">)', f'data-duration="{t:.3f}"\\1', cuerpo)
cuerpo = re.sub(r'duration: [\d.]+, ease: "none" \}, 0\);', f'duration: {t:.3f}, ease: "none" }}, 0);', cuerpo)
(S / "index.html").write_text(cuerpo)
(S / "escenas.json").write_text(json.dumps(out, indent=1))
print(len(out), "escenas,", round(t, 1), "s")
