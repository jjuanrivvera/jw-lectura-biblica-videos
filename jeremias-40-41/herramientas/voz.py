#!/usr/bin/env python3
"""Genera la voz de cada escena a partir de NARRACION.md.

Por cada escena NN:
  video/audio/escena-NN.txt   texto exacto que se manda a la voz
  video/audio/escena-NN.mp3   audio (comando edge-tts, como pide el encargo)
  video/audio/escena-NN.vtt   subtítulos por frase (mismo comando)
  video/audio/escena-NN.words.json  tiempos por palabra (segunda pasada con la API,
                                     porque el comando solo da frases)
Y un resumen video/audio/escenas.json con la duración medida de cada mp3.

Uso: herramientas/voz.py [NN ...]   (sin argumentos, todas las escenas)
"""
import asyncio
import json
import re
import subprocess
import sys
from pathlib import Path

import edge_tts

RAIZ = Path(__file__).resolve().parent.parent
AUDIO = RAIZ / "video" / "audio"
VOZ = "es-US-AlonsoNeural"
EDGE = str(Path.home() / ".local/bin/edge-tts")

# Solo cambia cómo se escribe para la voz; en pantalla se respeta la grafía de la TNM.
PRONUNCIA = {
    r"Tell en-Nasbeh": "Tel en Násbe",
}


def escenas():
    texto = (RAIZ / "NARRACION.md").read_text()
    partes = re.split(r"^## ", texto, flags=re.M)[1:]
    for p in partes:
        cab, _, cuerpo = p.partition("\n")
        num, _, titulo = cab.partition(" · ")
        parrafos = [
            l.strip() for l in cuerpo.splitlines()
            if l.strip() and not l.startswith(">") and not l.startswith("#")
        ]
        voz = " \n".join(parrafos)
        for a, b in PRONUNCIA.items():
            voz = re.sub(a, b, voz)
        voz = voz.replace('"', "").replace("“", "").replace("”", "")
        yield num.strip(), titulo.strip(), voz


def duracion(mp3):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(mp3)],
        capture_output=True, text=True, check=True,
    )
    return float(out.stdout.strip())


async def palabras(texto):
    com = edge_tts.Communicate(texto, VOZ, boundary="WordBoundary")
    res, bytes_audio = [], 0
    async for ch in com.stream():
        if ch["type"] == "audio":
            bytes_audio += len(ch["data"])
        elif ch["type"] == "WordBoundary":
            res.append({
                "w": ch["text"],
                "t": round(ch["offset"] / 1e7, 3),
                "d": round(ch["duration"] / 1e7, 3),
            })
    return res, bytes_audio


def vtt_inicios(vtt):
    inicios = []
    for m in re.finditer(r"(\d\d):(\d\d):(\d\d)[,.](\d\d\d) -->", vtt.read_text()):
        h, mi, s, ms = map(int, m.groups())
        inicios.append(h * 3600 + mi * 60 + s + ms / 1000)
    return inicios


async def una(num, titulo, texto, sem):
    async with sem:
        txt = AUDIO / f"escena-{num}.txt"
        mp3 = AUDIO / f"escena-{num}.mp3"
        vtt = AUDIO / f"escena-{num}.vtt"
        txt.write_text(texto + "\n")
        proc = await asyncio.create_subprocess_exec(
            EDGE, "--voice", VOZ, "--file", str(txt),
            "--write-media", str(mp3), "--write-subtitles", str(vtt),
        )
        if await proc.wait() != 0:
            raise RuntimeError(f"edge-tts falló en la escena {num}")
        pals, _ = await palabras(texto)
        dur = duracion(mp3)
        # Las dos pasadas deben coincidir: el inicio de cada frase del vtt tiene que caer
        # sobre una palabra de la pasada por palabras. Si no, los tiempos no sirven.
        inicios = vtt_inicios(vtt)
        peor = max(
            (min(abs(i - p["t"]) for p in pals) for i in inicios), default=0.0
        )
        (AUDIO / f"escena-{num}.words.json").write_text(
            json.dumps(pals, ensure_ascii=False, indent=0)
        )
        print(f"{num} {dur:7.2f}s  palabras={len(pals):4d}  desfase_max={peor:.3f}s  {titulo}")
        return {"id": num, "titulo": titulo, "dur": dur, "desfase": peor, "palabras": len(pals)}


async def main(filtro):
    AUDIO.mkdir(parents=True, exist_ok=True)
    sem = asyncio.Semaphore(4)
    lista = [e for e in escenas() if not filtro or e[0] in filtro]
    res = await asyncio.gather(*(una(n, t, x, sem) for n, t, x in lista))
    resumen_p = AUDIO / "escenas.json"
    previo = {e["id"]: e for e in json.loads(resumen_p.read_text())} if resumen_p.exists() else {}
    for r in res:
        previo[r["id"]] = r
    orden = sorted(previo.values(), key=lambda e: e["id"])
    resumen_p.write_text(json.dumps(orden, ensure_ascii=False, indent=1))
    total = sum(e["dur"] for e in orden)
    print(f"total voz: {total:.1f}s = {int(total // 60)}:{total % 60:04.1f}")


if __name__ == "__main__":
    asyncio.run(main(set(sys.argv[1:])))
