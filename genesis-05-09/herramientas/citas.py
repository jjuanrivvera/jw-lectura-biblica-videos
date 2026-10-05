#!/usr/bin/env python3
"""Coteja cada texto entre comillas “...” de las escenas con la investigación: si no aparece textual, lo lista.
Normaliza espacios y la etiqueta <b>; admite [...] como elisión (cada trozo debe aparecer, en orden)."""
import html, re, sys
from pathlib import Path

R = Path(__file__).resolve().parent.parent
fuente = (R / "trabajo/investigacion.txt").read_text()
norm = lambda s: re.sub(r"\s+", " ", s.replace("’", "'").replace("‘", "'")).strip().lower()
F = norm(fuente)
malas = 0
for p in sorted((R / "escenas").glob("[0-9][0-9].html")):
    t = re.sub(r"<script>[\s\S]*?</script>|<style>[\s\S]*?</style>", "", p.read_text())
    t = html.unescape(re.sub(r"<[^>]+>", "", t))
    for c in re.findall(r"“([^”]{12,})”", t):
        trozos = [norm(x).strip(" .,") for x in re.split(r"\[\s*(?:\.\.\.|…)\s*\]|…", c) if norm(x).strip(" .,")]
        pos, ok = 0, True
        for x in trozos:
            i = F.find(x, pos)
            if i < 0: ok = False; break
            pos = i + len(x)
        if not ok:
            malas += 1
            print(f"{p.name}: “{c[:110]}”")
print("citas no textuales:", malas)
