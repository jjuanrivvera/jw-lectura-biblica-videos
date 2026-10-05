#!/usr/bin/env python3
"""Repite los controles de entrega, con muestras en cada escena y transición."""
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
timeline = json.loads((ROOT / 'video/timeline.json').read_text())
captures = json.loads((ROOT / 'trabajo/capturas-finales.json').read_text())
times = sorted(set([s['time'] for s in captures] + [round(s['start'] + s['duration'] * fraction, 3)
    for s in timeline['scenes'] for fraction in [.25, .86]]))
subprocess.run(['python', 'herramientas/verificar.py'], cwd=ROOT, check=True)
for name, args in [('lint', []), ('check-final', ['--at', ','.join(map(str, times)),
    '--at-transitions', '--max-transition-samples', '240'])]:
    command = 'check' if name == 'check-final' else 'lint'
    with (ROOT / 'trabajo' / f'{name}.json').open('w') as output, (ROOT / 'trabajo' / f'{name}.stderr').open('w') as errors:
        result = subprocess.run(['npx', '--yes', 'hyperframes@0.8.79', command, 'video', '--json', *args],
            cwd=ROOT, stdout=output, stderr=errors)
    report = json.loads((ROOT / 'trabajo' / f'{name}.json').read_text())
    print(f'{command}: salida {result.returncode}', flush=True)
    if result.returncode:
        raise SystemExit(f'Revisar trabajo/{name}.json')
