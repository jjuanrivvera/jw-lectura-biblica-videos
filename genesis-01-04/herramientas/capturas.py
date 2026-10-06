#!/usr/bin/env python3
"""Capturas completas y momentos interiores de los movimientos, sin render de video."""
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
timeline = json.loads((ROOT / 'video/timeline.json').read_text())
samples = []
for scene in timeline['scenes']:
    samples.append({'scene': scene['id'], 'time': round(scene['start'] + scene['duration'] / 2, 3), 'kind': 'mitad de escena'})
    if scene['id'] in ['11', '16', '36', '37', '38', '39', '40']:
        for beat in scene['beats']:
            samples.append({'scene': scene['id'], 'time': round(scene['start'] + beat + 2, 3), 'kind': 'fase desarrollada'})

for ident, local, label in [
    ('00', .675, 'trazo inicial'), ('03', 18.417, 'luz y lumbreras'),
    ('10', 10.0, 'trazo de círculo'), ('10', 38.457, 'unión a mitad de movimiento'),
    ('10', 42.9, 'unión terminada'), ('11', 1.2, 'ríos a mitad de trazo'),
    ('14', 12.368, 'entrada del cotejo'), ('20', 19.315, 'cambio de observación'),
    ('27', 15.903, 'tienda a mitad de trazo'), ('27', 24.272, 'martillo a mitad de trazo'),
    ('30', .7, 'barras a mitad de crecimiento'), ('31', 20.496, 'parentesco a mitad de trazo'),
    ('32', 17.127, 'cubiertas a mitad de trazo'), ('38', 26.027, 'salida de fase'),
    ('38', 26.407, 'entrada de fase'), ('39', 24.342, 'entrada de lección')
]:
    scene = next(s for s in timeline['scenes'] if s['id'] == ident)
    samples.append({'scene': ident, 'time': round(scene['start'] + local, 3), 'kind': label})
samples.sort(key=lambda s: s['time'])
(ROOT / 'trabajo/capturas-finales.json').write_text(json.dumps(samples, ensure_ascii=False, indent=2))
args = ['npx', '--yes', 'hyperframes@0.8.79', 'snapshot', 'video', '--at',
        ','.join(str(s['time']) for s in samples), '--no-end', '--describe', 'false',
        '--output', str(ROOT / 'video/snapshots/final')]
with (ROOT / 'trabajo/capturas-finales.log').open('w') as output:
    subprocess.run(args, cwd=ROOT, stdout=output, stderr=subprocess.STDOUT, check=True)
print(f'{len(samples)} capturas de 1920×1080 en video/snapshots/final/')
