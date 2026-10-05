#!/usr/bin/env python3
"""Compara cada cita bíblica en pantalla con el texto de la TNM (jwlib), tramo por tramo.

Toma cada texto entre comillas “...” seguido de su referencia (<span class="ref">... GÉNESIS 42:6</span>),
aunque la referencia lleve delante quién habla ("JUDÁ · GÉNESIS 44:16"). Los "[...]" parten la cita en
tramos; cada tramo tiene que aparecer tal cual (sin tildes ni signos) en los versículos citados.
Adaptado de genesis-42-47/herramientas/verifica_citas.py, con los libros de este video.
Juan 8 se pide con 11 versículos menos: jwlib desplaza ese capítulo (la TNM 2019 omite 7:53 a 8:11).
"""
import html
import re
import subprocess
import unicodedata
from pathlib import Path

ESC = Path(__file__).resolve().parent.parent / "escenas"
LIBROS = {"GÉNESIS": "Génesis", "LEVÍTICO": "Levítico", "SALMO": "Salmo", "ECLESIASTÉS": "Eclesiastés", "ISAÍAS": "Isaías",
          "EZEQUIEL": "Ezequiel", "MIQUEAS": "Miqueas", "MATEO": "Mateo", "MARCOS": "Marcos", "LUCAS": "Lucas", "JUAN": "Juan",
          "HECHOS": "Hechos", "ROMANOS": "Romanos", "COLOSENSES": "Colosenses", "1 TIMOTEO": "1 Timoteo", "HEBREOS": "Hebreos",
          "1 PEDRO": "1 Pedro", "2 TESALONICENSES": "2 Tesalonicenses"}
cache = {}


def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9ñ]+", " ", s).strip()


def versos(libro, cap, lista):
    out = []
    for v in lista:
        ref = f"{libro} {cap}:{v - 11 if (libro, cap) == ("Juan", "8") else v}"
        if ref not in cache:
            r = subprocess.run([str(Path.home() / ".local/bin/jwlib"), "-q", "--offline", "versiculo", ref],
                               capture_output=True, text=True)
            lin = [l for l in r.stdout.splitlines() if re.match(r"^\S+ \d+:\d+ ", l) and "Traducción del Nuevo Mundo" not in l]
            cache[ref] = lin[0].split(" ", 2)[2] if lin else ""
        out.append(cache[ref])
    return " ".join(out)


def expande(txt):
    vs = []
    for parte in re.split(r",\s*", txt):
        m = re.match(r"(\d+)(?:-(\d+))?", parte.strip())
        if m:
            a, b = int(m.group(1)), int(m.group(2) or m.group(1))
            vs += list(range(a, b + 1))
    return vs


malos = total = 0
for f in sorted(ESC.glob("[0-9][0-9].html")):
    s = f.read_text(encoding="utf-8")
    for m in re.finditer(r"“((?:(?!“).){6,}?)”(?:(?!“).){0,160}?<span class=\"ref\"[^>]*>([^<]+)</span>", s, re.S):
        cita, ref = m.group(1), html.unescape(m.group(2))
        rm = re.search(r"(1 TIMOTEO|1 PEDRO|2 TESALONICENSES|GÉNESIS|LEVÍTICO|SALMO|ECLESIASTÉS|ISAÍAS|EZEQUIEL|MIQUEAS|MATEO|MARCOS|LUCAS|JUAN|HECHOS|ROMANOS|COLOSENSES|HEBREOS) (\d+):([\d,\s\-]+)", ref)
        if not rm:
            continue
        total += 1
        texto = versos(LIBROS[rm.group(1)], rm.group(2), expande(rm.group(3)))
        limpio = re.sub(r"<[^>]+>", "", cita)
        segs = [x for x in re.split(r"\[\s*(?:\.\.\.|…)\s*\]", limpio) if norm(x)]
        for sg in segs:
            for trozo in re.split(r"”[^“]*“", sg):
                if norm(trozo) and norm(trozo) not in norm(texto):
                    malos += 1
                    print(f"{f.name} {ref.strip()}: «{trozo.strip()[:90]}»\n    TNM: {texto[:240]}")
print(f"{malos} diferencias en {total} citas ({len(cache)} versículos consultados)")
