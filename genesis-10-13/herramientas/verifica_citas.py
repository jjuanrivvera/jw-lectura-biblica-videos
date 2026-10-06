#!/usr/bin/env python3
"""Compara cada cita bíblica en pantalla con el texto de la TNM (jwlib), segmento por segmento."""
import html, json, re, subprocess, sys, unicodedata
from pathlib import Path

ESC = Path(__file__).resolve().parent.parent / "escenas"
LIBROS = {"GÉNESIS": "Génesis", "GÁLATAS": "Gálatas", "HEBREOS": "Hebreos", "HECHOS": "Hechos", "2 PEDRO": "2 Pedro",
          "SALMO": "Salmos", "SOFONÍAS": "Sofonías", "JOSUÉ": "Josué", "NÚMEROS": "Números", "APOCALIPSIS": "Apocalipsis",
          "1 CORINTIOS": "1 Corintios", "ÉXODO": "Éxodo", "MATEO": "Mateo", "ROMANOS": "Romanos"}
cache = {}

def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9ñ]+", " ", s).strip()

def versos(libro, cap, lista):
    out = []
    for v in lista:
        ref = f"{libro} {cap}:{v}"
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

malos = 0
for f in sorted(ESC.glob("[0-9][0-9].html")):
    s = f.read_text()
    for m in re.finditer(r"“((?:(?!“).){6,}?)”(?:(?!“).){0,160}?<span class=\"ref\">([^<]+)</span>", s, re.S):
        cita, ref = m.group(1), html.unescape(m.group(2))
        rm = re.match(r"(\d? ?[A-ZÁÉÍÓÚÑ]+) (\d+):([\d,\s\-]+)", ref)
        if not rm or rm.group(1) not in LIBROS:
            continue
        texto = versos(LIBROS[rm.group(1)], rm.group(2), expande(rm.group(3)))
        limpio = re.sub(r"<[^>]+>", "", cita)
        # Solo el tramo entre comillas: lo que va fuera (por ejemplo "Lot “…”") no es cita.
        segs = [x for x in re.split(r"\[\s*(?:\.\.\.|…)\s*\]", limpio) if norm(x)]
        for sg in segs:
            for trozo in re.split(r"”[^“]*“", sg):
                if norm(trozo) and norm(trozo) not in norm(texto):
                    malos += 1
                    print(f"{f.name} {ref.strip()}: «{trozo.strip()[:90]}»\n    TNM: {texto[:220]}")
print(f"{malos} diferencias en {len(cache)} versículos consultados")
