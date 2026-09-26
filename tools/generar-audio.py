#!/usr/bin/env python3
"""Genera MP3, subtítulos y tiempos por palabra a partir de la narración de un proyecto."""
import asyncio
import json
import re
import subprocess
import sys
from pathlib import Path

import edge_tts

PROJECTS = {"genesis-14-18", "genesis-19-23", "genesis-24-28"}
VOICE = "es-US-AlonsoNeural"
LEAD = 0.6

PRONUNCIATION = {
    "Beer-seba": "Beerseba",
    "Beer-Lahái-Roí": "Beer Lahái Roí",
    "Qohat": "Kohat",
    "tsa·jáq": "tsajác",
    "lo·guí·zo·mai": "loguízomai",
    "uadi el-Arish": "uadi el Arish",
    "Berekjyáhu": "Berekiyáhu",
}


def read_scenes(path):
    text = path.read_text(encoding="utf-8")
    blocks = re.split(r"^## ", text, flags=re.M)[1:]
    for block in blocks:
        heading, _, body = block.partition("\n")
        number, separator, title = heading.partition(" · ")
        if not separator or not number.strip().isdigit():
            continue
        lines = [line.strip() for line in body.splitlines()
                 if line.strip() and not line.startswith((">", "#"))]
        spoken = " \n".join(lines)
        for original, pronunciation in PRONUNCIATION.items():
            spoken = spoken.replace(original, pronunciation)
        spoken = spoken.replace('"', "").replace("“", "").replace("”", "")
        yield number.strip(), title.strip(), spoken


def timestamp(seconds):
    ms = round(seconds * 1000)
    hours, remainder = divmod(ms, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    seconds, millis = divmod(remainder, 1000)
    return f"{hours:02}:{minutes:02}:{seconds:02}.{millis:03}"


async def generate_one(audio_dir, number, title, text, semaphore):
    async with semaphore:
        communicator = edge_tts.Communicate(text, VOICE, boundary="WordBoundary")
        audio = bytearray()
        words = []
        async for chunk in communicator.stream():
            if chunk["type"] == "audio":
                audio.extend(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                start = chunk["offset"] / 10_000_000
                duration = chunk["duration"] / 10_000_000
                words.append({"w": chunk["text"], "t": round(start, 3), "d": round(duration, 3)})
        if not audio:
            raise RuntimeError(f"No se recibió audio para la escena {number}.")

        mp3 = audio_dir / f"escena-{number}.mp3"
        mp3.write_bytes(audio)
        (audio_dir / f"escena-{number}.txt").write_text(text + "\n", encoding="utf-8")
        (audio_dir / f"escena-{number}.words.json").write_text(
            json.dumps(words, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")

        end = max((word["t"] + word["d"] for word in words), default=0.0)
        cues = ["WEBVTT", ""]
        for index, word in enumerate(words, start=1):
            start = word["t"]
            finish = max(start + 0.08, start + word["d"])
            cues.extend([str(index), f"{timestamp(start)} --> {timestamp(finish)}", word["w"], ""])
        (audio_dir / f"escena-{number}.vtt").write_text("\n".join(cues), encoding="utf-8")

        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(mp3)],
            check=True, capture_output=True, text=True)
        duration = float(result.stdout.strip())
        print(f"Escena {number}: {duration:.2f} s, {len(words)} palabras, {title}")
        return {"id": number, "titulo": title, "dur": duration, "palabras": len(words)}


async def main():
    if len(sys.argv) != 2 or sys.argv[1] not in PROJECTS:
        raise SystemExit("Uso: python3 tools/generar-audio.py genesis-14-18|genesis-19-23|genesis-24-28")
    root = Path(__file__).resolve().parents[1] / sys.argv[1]
    audio_dir = root / "video" / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)
    semaphore = asyncio.Semaphore(4)
    tasks = [generate_one(audio_dir, number, title, text, semaphore)
             for number, title, text in read_scenes(root / "NARRACION.md")]
    results = sorted(await asyncio.gather(*tasks), key=lambda scene: scene["id"])
    (audio_dir / "escenas.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    total = sum(scene["dur"] for scene in results)
    print(f"Duración de voz: {total / 60:.1f} min; voz: {VOICE}")


if __name__ == "__main__":
    asyncio.run(main())
