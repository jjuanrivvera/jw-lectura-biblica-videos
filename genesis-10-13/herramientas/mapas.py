#!/usr/bin/env python3
"""Recortes de los mapas reales y copias con cuadrícula para leer coordenadas.

  mapas.py b2 NOMBRE X Y W H ESCALA   recorte del apéndice B2 (vector) en unidades del SVG (648x468),
                                       rasterizado a ESCALA px por unidad -> mapas/NOMBRE.png y .jpg
  mapas.py rejilla IMAGEN PASO         copia con cuadrícula rotulada cada PASO px -> IMAGEN-grid.jpg
  mapas.py doble IMAGEN SALIDA         copia a 2x con Lanczos y un poco de nitidez (para mapas raster)
"""
import re
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

RAIZ = Path(__file__).resolve().parent.parent
MAPAS = RAIZ / "mapas"


def b2(nombre, x, y, w, h, escala):
    src = (MAPAS / "b2.svg").read_text()
    src = re.sub(r'viewBox="[^"]+"', f'viewBox="{x} {y} {w} {h}"', src, count=1)
    src = re.sub(r'width="100%"', f'width="{round(w * escala)}" height="{round(h * escala)}"', src, count=1)
    src = src.replace('preserveAspectRatio="xMinYMin slice"', 'preserveAspectRatio="xMinYMin meet"')
    svg = MAPAS / f"{nombre}.svg"
    svg.write_text(src)
    png = MAPAS / f"{nombre}.png"
    subprocess.run(["rsvg-convert", str(svg), "-o", str(png)], check=True)
    im = Image.open(png).convert("RGB")
    im.save(MAPAS / f"{nombre}.jpg", quality=90)
    print(nombre, im.size)


def rejilla(ruta, paso):
    im = Image.open(ruta).convert("RGB")
    d = ImageDraw.Draw(im)
    try:
        f = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", max(12, paso // 5))
    except OSError:
        f = ImageFont.load_default()
    for x in range(0, im.width, paso):
        d.line([(x, 0), (x, im.height)], fill=(255, 0, 0) if x % (paso * 5) == 0 else (255, 120, 120), width=1)
        for y in range(0, im.height, paso * 5):
            d.text((x + 2, y + 2), str(x), fill=(200, 0, 0), font=f)
    for y in range(0, im.height, paso):
        d.line([(0, y), (im.width, y)], fill=(255, 0, 0) if y % (paso * 5) == 0 else (255, 120, 120), width=1)
        for x in range(0, im.width, paso * 5):
            d.text((x + 2, y + 2), str(y), fill=(0, 0, 200), font=f)
    salida = Path(ruta).with_name(Path(ruta).stem + "-grid.jpg")
    im.save(salida, quality=85)
    print(salida, im.size)


def doble(ruta, salida):
    im = Image.open(ruta).convert("RGB")
    im = im.resize((im.width * 2, im.height * 2), Image.LANCZOS)
    im = im.filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))
    im.save(salida, quality=90)
    print(salida, im.size)


if __name__ == "__main__":
    cmd, *a = sys.argv[1:]
    if cmd == "b2":
        b2(a[0], *map(float, a[1:6]))
    elif cmd == "rejilla":
        rejilla(a[0], int(a[1]))
    elif cmd == "doble":
        doble(a[0], a[1])
