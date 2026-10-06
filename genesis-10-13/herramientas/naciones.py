#!/usr/bin/env python3
"""Puntos de los pueblos de Génesis 10 sobre "El origen de las naciones" (mapas/naciones.jpg, 2400x1840).

Cada punto sale del mapa propio de la investigación (su SVG, fig-1), pasado a longitud y latitud y luego al mapa de la
JW con la georreferencia de herramientas/georef.py. Certeza, como en la investigación: "f" firme (punto lleno),
"p" probable (hueco), "q" posibilidad (punteado con "?").

Salida: escenas/_naciones.js con la lista PUEBLOS [rama, nombre, x, y, certeza, nota] lista para pintar.
"""
import json
from pathlib import Path

from georef import a_px, de_investigacion

RAIZ = Path(__file__).resolve().parent.parent

# rama, nombre, x, y (SVG de la investigación), certeza, pueblo o región (tabla de la investigación)
FIG = [
    ("J", "Gómer", 160.0, 57.0, "p", "cimerios"),
    ("J", "Magog", 253.7, 51.6, "q", "¿escitas?"),
    ("J", "Madái", 270.5, 141.8, "p", "medos"),
    ("J", "Javán", 77.0, 114.8, "p", "griegos"),
    ("J", "Tubal", 170.0, 116.3, "p", ""),
    ("J", "Mesec", 136.6, 110.2, "p", "frigios"),
    ("J", "Tirás", 97.1, 102.5, "p", "tirrenos"),
    ("J", "Askenaz", 220.3, 91.7, "p", ""),
    ("J", "Togarmá", 210.2, 108.6, "p", "armenios"),
    ("J", "Kitim", 147.9, 143.3, "f", "Chipre"),
    ("J", "Rodanim", 113.1, 134.9, "p", "Rodas"),
    ("C", "Cus", 183.4, 298.4, "p", "etíopes"),
    ("C", "Mizraim", 133.2, 205.8, "f", "Egipto"),
    ("C", "Put", 59.6, 182.7, "p", "libios"),
    ("C", "Canaán", 161.3, 170.3, "f", ""),
    ("C", "Caftorim", 91.7, 142.6, "p", "Creta"),
    ("C", "Sebá", 150.0, 282.9, "p", ""),
    ("C", "Havilá", 223.6, 288.3, "p", ""),
    ("S", "Elam", 251.7, 170.3, "f", "elamitas"),
    ("S", "Asur", 214.9, 140.3, "f", "asirios"),
    ("S", "Aram", 177.4, 150.3, "f", "arameos"),
    ("S", "Lud", 117.1, 117.9, "p", "¿lidios?"),
    ("S", "Joctán", 233.7, 263.7, "p", "Arabia"),
]

if __name__ == "__main__":
    out = []
    for rama, nombre, x, y, c, nota in FIG:
        lon, lat = de_investigacion(x, y)
        borde = ""
        if lat < 20.5:
            # Más al sur que el borde del mapa de la JW: se ponen en el borde, a la longitud que les toca
            # (a la latitud 20, dentro del mapa), con una flecha hacia el sur.
            px, _ = a_px(lon, 20.0)
            py, borde = 1778, "s"
        else:
            px, py = a_px(lon, lat)
        out.append([rama, nombre, round(float(px)), round(float(py)), c, nota, borde])
        print(f"{rama} {nombre:9s} lon {lon:5.1f} lat {lat:5.1f} -> {px:6.0f} {py:6.0f} {borde}")
    # Tarsis: España o Cerdeña, las dos fuera del mapa por el oeste; flecha en el borde izquierdo.
    out.append(["J", "Tarsis", 40, 200, "q", "¿España o Cerdeña?", "o"])
    (RAIZ / "escenas/_naciones.js").write_text(
        "// Generado por herramientas/naciones.py: [rama, nombre, x, y, certeza, nota] sobre naciones.jpg (2400x1840).\n"
        "const PUEBLOS = " + json.dumps(out, ensure_ascii=False) + ";\n")
