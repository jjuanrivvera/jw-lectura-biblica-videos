#!/usr/bin/env python3
"""Cauces reales (Natural Earth 10m) en coordenadas del relieve recortado (mapas/relieve.png).

relieve.png = HYP_HR_SR_W (Natural Earth, 1/60 de grado por píxel) recortado a lon 26..60, lat 22..46 y escalado
1,6 en horizontal y 2,0 en vertical: x = (lon-26)*96, y = (46-lat)*120 (equirectangular con paralelo de ~37°).
Salida: escenas/_rios.js con los trazos del Éufrates, su brazo Murat, el Tigris y el contorno del lago Van.
"""
import json, math
from pathlib import Path

R = Path(__file__).resolve().parent
px = lambda lon, lat: ((lon - 26) * 96, (46 - lat) * 120)

rios = json.load(open(R / "rios.geojson"))
lagos = json.load(open(R / "lagos.geojson"))

def lineas(nombres):
    out = []
    for f in rios["features"]:
        if f["properties"]["name"] in nombres:
            g = f["geometry"]
            for l in (g["coordinates"] if g["type"] == "MultiLineString" else [g["coordinates"]]):
                if len(l) > 4:
                    out.append(l)
    return out

def encadena(segs, inicio):
    """Une los tramos siguiendo la corriente, desde el punto de nacimiento dado."""
    d = lambda a, b: math.hypot(a[0] - b[0], a[1] - b[1])
    segs = list(segs)
    cam = [inicio]
    while segs:
        fin = cam[-1]
        mejor = min(segs, key=lambda s: min(d(fin, s[0]), d(fin, s[-1])))
        if min(d(fin, mejor[0]), d(fin, mejor[-1])) > 0.08:
            break
        segs.remove(mejor)
        if d(fin, mejor[-1]) < d(fin, mejor[0]):
            mejor = mejor[::-1]
        cam += mejor[1:]
    return cam

def d_path(coords, paso=2):
    pts = [px(*c) for c in coords]
    pts = pts[::paso] + [pts[-1]]
    return "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts)

eufrates = encadena(lineas({"Firat", "Al Furat", "Euphrates", "Shatt al Arab"}), [41.46, 40.18])
tigris = encadena(lineas({"Dicle", "Tigris", "Shatt al Arab"}), [39.17, 38.42])
murat = encadena(lineas({"Murat"}), [43.58, 39.41])

def largo_km(coords):
    t = 0
    for a, b in zip(coords, coords[1:]):
        la = math.radians((a[1] + b[1]) / 2)
        t += math.hypot((b[0] - a[0]) * 111.32 * math.cos(la), (b[1] - a[1]) * 110.57)
    return t

def lago(nombre):
    g = next(f for f in lagos["features"] if f["properties"].get("name") == nombre)["geometry"]
    anillo = (g["coordinates"][0] if g["type"] == "Polygon" else max((p[0] for p in g["coordinates"]), key=len))
    return d_path(anillo, 1) + " Z"

van_d = lago("Lake Van")
urmia_d = lago("Lake Urmia")

js = f"""// Generado por mapas/generar.py (Natural Earth 10m). Coordenadas de assets/img/relieve.jpg (3264x2880).
const MAPA_W = 3264, MAPA_H = 2880;
const P = (lon, lat) => [(lon - 26) * 96, (46 - lat) * 120];
const RIO_EUFRATES = "{d_path(eufrates)}";
const RIO_TIGRIS = "{d_path(tigris)}";
const RIO_MURAT = "{d_path(murat)}";
const LAGO_VAN = "{van_d}";
const LAGO_URMIA = "{urmia_d}";
"""
(R.parent / "escenas" / "_rios.js").write_text(js)
print("Éufrates", len(eufrates), "puntos,", round(largo_km(eufrates)), "km trazados; fin", eufrates[-1])
print("Tigris", len(tigris), "puntos,", round(largo_km(tigris)), "km; fin", tigris[-1])
print("Murat", len(murat), round(largo_km(murat)), "km; fin", murat[-1])
