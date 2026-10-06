#!/usr/bin/env python3
"""Genera audios en serie y conserva los tiempos del VTT del mismo audio."""
import hashlib
import json
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIO = ROOT / 'video/audio'
VOICE = 'es-US-AlonsoNeural'

def scenes():
    for chunk in re.split(r'^## ', (ROOT / 'NARRACION.md').read_text(), flags=re.M)[1:]:
        heading, body = chunk.split('\n', 1)
        number, title = heading.split(' · ', 1)
        paragraphs = [p.strip() for p in body.strip().split('\n\n') if p.strip()]
        yield number, title, paragraphs

def seconds(s):
    h, m, sec = s.split(':')
    return int(h) * 3600 + int(m) * 60 + float(sec.replace(',', '.'))

def cues(path):
    result = []
    for match in re.finditer(r'(\d\d:\d\d:\d\d[.,]\d+) --> (\d\d:\d\d:\d\d[.,]\d+)\n([^\n]+)', path.read_text()):
        result.append({'start': seconds(match[1]), 'end': seconds(match[2]), 'text': match[3]})
    if not result:
        raise ValueError(f'No hay subtítulos: {path}')
    return result

if __name__ == '__main__':
    AUDIO.mkdir(parents=True, exist_ok=True)
    manifest = AUDIO / 'escenas.json'
    records = {s['id']: s for s in json.loads(manifest.read_text())} if manifest.exists() else {}
    selected = set(sys.argv[1:])
    for number, title, paragraphs in scenes():
        if selected and number not in selected:
            continue
        text = '\n\n'.join(paragraphs)
        stem = AUDIO / f'escena-{number}'
        digest = hashlib.sha256((VOICE + text).encode()).hexdigest()
        if records.get(number, {}).get('hash') == digest and stem.with_suffix('.mp3').exists():
            print(number, 'ya verificada', flush=True)
            continue
        stem.with_suffix('.txt').write_text(text + '\n')
        for attempt in range(3):
            run = subprocess.run(['edge-tts', '--voice', VOICE, '--file', str(stem.with_suffix('.txt')),
                                  '--write-media', str(stem.with_suffix('.mp3')),
                                  '--write-subtitles', str(stem.with_suffix('.vtt'))], capture_output=True, text=True)
            if run.returncode == 0:
                break
            if attempt == 2:
                raise RuntimeError(f'edge-tts escena {number}: {run.stderr[-1800:]}')
            time.sleep(2)
        duration = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                        '-of', 'csv=p=0', str(stem.with_suffix('.mp3'))], text=True))
        subtitles = cues(stem.with_suffix('.vtt'))
        if subtitles[-1]['end'] > duration + 0.2:
            raise ValueError(f'Subtítulo fuera de audio: {number}')
        records[number] = {'id': number, 'title': title, 'duration': duration, 'voice': VOICE,
                           'hash': digest, 'paragraphs': paragraphs, 'cues': subtitles}
        manifest.write_text(json.dumps(sorted(records.values(), key=lambda r:r['id']), ensure_ascii=False, indent=2))
        print(f'{number} {duration:.3f}s · {len(subtitles)} subtítulos · {title}', flush=True)
    total = sum(r['duration'] for r in records.values())
    print(f'TOTAL {total:.3f}s = {int(total//60)}:{total%60:05.2f}', flush=True)
