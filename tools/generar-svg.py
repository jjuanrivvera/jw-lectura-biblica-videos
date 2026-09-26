#!/usr/bin/env python3
"""Genera los gráficos vectoriales esquemáticos que usan las escenas."""
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECTS = ("genesis-14-18", "genesis-19-23", "genesis-24-28", "jeremias-36-37")
LABELS = {
    "abrahan-sodoma": "Abrán rescata a Lot", "agar-ismael-se-van": "Agar e Ismael",
    "ataque-noche": "Un rescate nocturno", "estrellas": "La promesa de las estrellas",
    "hospitalidad": "Hospitalidad en Mamré", "lot-zoar": "La huida hacia Zóar",
    "mapa-agar": "Ruta de Agar", "mapa-rutas": "Rutas de los patriarcas",
    "melquisedec-diezmo": "Melquisedec bendice a Abrán", "sara-escucha": "Sara escucha",
    "sara-princesa": "El nombre de Sara", "agar-se-va": "Agar parte al desierto",
    "altar-isaac": "El altar en Moriá", "carnero": "El carnero", "duelo-sara": "Duelo por Sara",
    "esposa-lot": "La esposa de Lot", "hebron-hoy": "Hebrón", "mapa-recuadro": "Mapa de Hebrón y Mamré",
    "mapa-sur": "El sur de Canaán", "mapa-recorrido": "Cinco etapas del relato",
    "nace-isaac": "El nacimiento de Isaac", "negueb": "El Négueb", "pesas-lakis": "Pesas antiguas",
    "subida-moria": "El camino a Moriá", "tamarisco": "El tamarisco", "betel-ruinas": "Betel",
    "camello": "Un viaje en camello", "escalera": "El sueño de Jacob", "guisado": "El guisado",
    "haran-hoy": "Harán", "jacob-esau-historia": "Jacob y Esaú", "jacob-esau": "Jacob y Esaú",
    "mapa-capitulos": "Génesis 24 al 28", "mapa-pozos": "Pozos de Isaac",
    "rebeca-isaac": "Rebeca e Isaac", "rebeca-pozo": "Rebeca en el pozo",
    "jehoiaquim": "El rey quema el rollo", "plano": "Un plano de Jerusalén",
    "sedequias": "Sedequías", "tabla": "Una bula de arcilla", "templo": "El templo",
}


def main():
    references = set()
    pattern = re.compile(r"assets/img/([A-Za-z0-9_-]+)\.svg", re.I)
    for project in PROJECTS:
        for folder in (ROOT / project / "escenas", ROOT / project / "video" / "compositions"):
            if folder.exists():
                for source in folder.glob("*"):
                    if source.is_file() and source.suffix.lower() in {".html", ".css", ".js"}:
                        references.update(match.group(1) for match in pattern.finditer(source.read_text(errors="replace")))
    for name in sorted(references):
        label = html.escape(LABELS.get(name, name.replace("-", " ").title()))
        if "mapa" in name or name == "plano":
            art = '''<path d="M160 910 C300 780 260 560 445 460 S690 300 1010 180" fill="none" stroke="#e7bd69" stroke-width="13" stroke-linecap="round" stroke-dasharray="2 22"/><path d="M110 1040 Q360 860 650 920 T1110 700" fill="none" stroke="#82b5b0" stroke-width="8" opacity=".8"/><circle cx="445" cy="460" r="23" fill="#e7bd69"/><circle cx="1010" cy="180" r="23" fill="#e7bd69"/>'''
        else:
            art = '''<path d="M0 710 Q210 560 390 700 T780 680 T1200 700 V1200 H0Z" fill="#344b48"/><path d="M0 850 Q270 690 520 830 T1200 790 V1200 H0Z" fill="#24383a"/><circle cx="930" cy="280" r="90" fill="#e7bd69" opacity=".78"/><path d="M210 770 Q260 560 310 770 M520 760 Q575 500 630 760 M790 770 Q850 565 910 770" fill="none" stroke="#b7c99a" stroke-width="16" stroke-linecap="round"/>'''
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 1200" role="img" aria-labelledby="title desc"><title id="title">{label}</title><desc id="desc">Gráfico vectorial esquemático original.</desc><defs><linearGradient id="fondo" x2="0" y2="1"><stop stop-color="#1b2935"/><stop offset="1" stop-color="#52615b"/></linearGradient></defs><rect width="1200" height="1200" fill="url(#fondo)"/><g opacity=".2" fill="none" stroke="#c3c3a4" stroke-width="2"><path d="M0 180H1200M0 300H1200M0 420H1200M0 540H1200M0 660H1200M0 780H1200M0 900H1200"/><path d="M160 0V1200M320 0V1200M480 0V1200M640 0V1200M800 0V1200M960 0V1200"/></g>{art}<rect x="64" y="64" width="1072" height="1072" rx="26" fill="none" stroke="#e8dfc7" stroke-opacity=".4" stroke-width="3"/><text x="78" y="1090" fill="#f1e9d8" font-family="Georgia,serif" font-size="42">{label}</text></svg>'''
        for project in PROJECTS:
            dest = ROOT / project / "video" / "assets" / "img" / f"{name}.svg"
            files = list((ROOT / project / "escenas").glob("*")) + list((ROOT / project / "video" / "compositions").glob("*.html"))
            if any(pattern.search(source.read_text(errors="replace")) and f"assets/img/{name}.svg" in source.read_text(errors="replace") for source in files if source.is_file()):
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_text(svg + "\n", encoding="utf-8")
    print(f"Gráficos vectoriales listos: {len(references)}")


if __name__ == "__main__":
    main()
