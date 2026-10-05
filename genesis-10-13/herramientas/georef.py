#!/usr/bin/env python3
"""Georreferencia del mapa "El origen de las naciones" (Perspicacia, vol. 1, pág. 329) a 2x (mapas/naciones.jpg).

Ajusta un polinomio de 2.º grado (lon, lat) -> (x, y) con puntos de control leídos en la copia con cuadrícula, y
dibuja encima las costas de Natural Earth para comprobar el ajuste (trabajo/naciones-chk.jpg). Los pueblos se colocan
en la posición del mapa propio de la investigación (su SVG usa x = (lon - 11,12) * 6,64 y y = (53,76 - lat) * 7,68).

Uso: herramientas/georef.py [comprobar]
"""
import json
import sys
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parent.parent

# (x, y) en naciones.jpg (2400x1840)  <->  (lon, lat)
CONTROL = [
    ((1005, 900), (32.27, 35.08)),   # Chipre, cabo Arnauti
    ((1122, 852), (34.59, 35.70)),   # Chipre, cabo Andreas
    ((644, 805), (24.90, 35.25)),    # Creta, centro
    ((798, 792), (28.00, 36.20)),    # Rodas
    ((1085, 1250), (34.95, 29.55)),  # golfo de Áqaba, punta
    ((980, 1200), (32.55, 29.97)),   # golfo de Suez, punta
    ((1768, 1172), (48.50, 29.95)),  # golfo Pérsico, Shatt al-Arab
    ((1800, 555), (50.30, 40.40)),   # Caspio, Absherón
    ((1905, 762), (51.50, 36.75)),   # Caspio, costa sur
    ((1612, 735), (45.50, 37.70)),   # lago Urmía
    ((1505, 692), (43.00, 38.60)),   # lago Van
    ((1595, 588), (45.30, 40.35)),   # lago Seván
    ((1190, 795), (36.17, 36.85)),   # golfo de Alejandreta
]


def terminos(lon, lat):
    lon = np.asarray(lon, float); lat = np.asarray(lat, float)
    return np.stack([np.ones_like(lon), lon, lat, lon * lat, lon ** 2, lat ** 2], axis=-1)


def ajusta(control=CONTROL):
    P = np.array([c[0] for c in control], float)
    G = np.array([c[1] for c in control], float)
    A = terminos(G[:, 0], G[:, 1])
    cx, *_ = np.linalg.lstsq(A, P[:, 0], rcond=None)
    cy, *_ = np.linalg.lstsq(A, P[:, 1], rcond=None)
    return cx, cy


CX, CY = ajusta()


def a_px(lon, lat):
    T = terminos(lon, lat)
    return T @ CX, T @ CY


def de_investigacion(x, y):
    """Punto del SVG de la investigación (viewBox 320x483) a (lon, lat)."""
    return 11.12 + x / 6.64, 53.76 - y / 7.68


def comprobar():
    from PIL import Image, ImageDraw
    im = Image.open(RAIZ / "mapas/naciones.jpg").convert("RGB")
    d = ImageDraw.Draw(im)
    geo = json.load(open(Path.home() / "jw-video/genesis-01-04/mapas/paises.geojson"))
    for f in geo["features"]:
        g = f["geometry"]
        polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
        for poly in polys:
            for ring in poly:
                r = np.array(ring)
                if r[:, 0].max() < 5 or r[:, 0].min() > 70 or r[:, 1].max() < 10 or r[:, 1].min() > 55:
                    continue
                x, y = a_px(r[:, 0], r[:, 1])
                d.line(list(zip(x, y)), fill=(220, 0, 0), width=2)
    for (px, py), _ in CONTROL:
        d.ellipse((px - 8, py - 8, px + 8, py + 8), outline=(0, 120, 0), width=3)
    im.save(RAIZ / "trabajo/naciones-chk.jpg", quality=85)
    res = []
    for (px, py), (lo, la) in CONTROL:
        x, y = a_px(lo, la)
        res.append(((x - px) ** 2 + (y - py) ** 2) ** 0.5)
    print("residuo medio %.1f px, máx %.1f px" % (np.mean(res), np.max(res)))


if __name__ == "__main__":
    if sys.argv[1:] == ["comprobar"]:
        comprobar()
