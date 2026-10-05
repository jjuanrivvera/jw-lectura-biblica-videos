#!/usr/bin/env python3
"""Comprueba la continuidad audiovisual y la integridad del texto entregado."""
import hashlib
import json
import re
import subprocess
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def words(text):
    return re.sub(r'[^a-z0-9]', '', unicodedata.normalize('NFD', text.casefold()))

def timestamp(seconds):
    milliseconds = round(seconds * 1000)
    hours, milliseconds = divmod(milliseconds, 3600000)
    minutes, milliseconds = divmod(milliseconds, 60000)
    seconds, milliseconds = divmod(milliseconds, 1000)
    return f'{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:03}'

def main():
    audio = json.loads((ROOT / 'video/audio/escenas.json').read_text())
    timeline = json.loads((ROOT / 'video/timeline.json').read_text())
    narration = (ROOT / 'NARRACION.md').read_text()
    chapters = re.split(r'^## ', narration, flags=re.M)[1:]
    assert len(audio) == len(timeline['scenes']) == len(chapters) == 42
    cursor = 0
    full_vtt = ['WEBVTT', '']
    reports = []
    for a, scene, chapter in zip(audio, timeline['scenes'], chapters):
        ident = a['id']
        text = chapter.split('\n', 1)[1].strip()
        assert a['voice'] == 'es-US-AlonsoNeural'
        assert words(text) == words(' '.join(a['paragraphs']))
        assert words(text) == words(' '.join(c['text'] for c in a['cues'])), ident
        digest = hashlib.sha256((a['voice'] + '\n\n'.join(a['paragraphs'])).encode()).hexdigest()
        assert a['hash'] == digest, ident
        stem = ROOT / 'video/audio' / f'escena-{ident}'
        assert stem.with_suffix('.vtt').read_text().startswith('WEBVTT\n')
        duration = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries',
            'format=duration', '-of', 'csv=p=0', str(stem.with_suffix('.mp3'))], text=True))
        assert abs(duration - a['duration']) < .001, ident
        assert abs(scene['duration'] - duration) < .001, ident
        assert abs(scene['start'] - cursor) < .001, ident
        assert all(0 <= c['start'] < c['end'] <= duration + .2 for c in a['cues']), ident
        composition = (ROOT / 'video/compositions' / f'escena-{ident}.html').read_text()
        assert not re.search(r'data-(?:p|cue|until-p|move-cue)=', composition), ident
        assert all(0 <= beat < duration for beat in scene['beats']), ident
        for i, cue in enumerate(a['cues']):
            # Edge solapa algunas frases unos milisegundos; el VTT global usa el inicio siguiente.
            end = min(cue['end'], a['cues'][i + 1]['start']) if i + 1 < len(a['cues']) else cue['end']
            full_vtt.extend([f'{ident}-{i+1}', f'{timestamp(cursor+cue["start"])} --> {timestamp(cursor+end)}', cue['text'], ''])
        reports.append({'id': ident, 'duration': duration, 'cues': len(a['cues']), 'text_complete': True})
        cursor += duration
    assert abs(cursor - timeline['duration']) < .001
    assert not re.search(r'observación propia|cálculo propio|—', '\n'.join(c.split('\n', 1)[1] for c in chapters), re.I)
    (ROOT / 'video/subtitulos.vtt').write_text('\n'.join(full_vtt))
    result = {'ok': True, 'duration': round(cursor, 3), 'scene_count': len(audio), 'scenes': reports}
    (ROOT / 'trabajo/verificacion-integridad.json').write_text(json.dumps(result, ensure_ascii=False, indent=2))
    print(f'Integridad correcta: {len(audio)} escenas, {cursor:.3f} s, texto completo y audio continuo.')

if __name__ == '__main__':
    main()
