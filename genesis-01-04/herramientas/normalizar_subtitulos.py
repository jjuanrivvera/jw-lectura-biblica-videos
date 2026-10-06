"""La versión instalada de edge-tts entrega SRT incluso con extensión .vtt."""
from pathlib import Path
import re

for path in (Path(__file__).resolve().parents[1] / 'video/audio').glob('*.vtt'):
    text = path.read_text()
    if not text.startswith('WEBVTT'):
        path.with_suffix('.srt').write_text(text)
        text = re.sub(r'(\d\d:\d\d:\d\d),(\d{3})', r'\1.\2', text)
        path.write_text('WEBVTT\n\n' + text)
