#!/usr/bin/env python3
"""Genera las escenas de lecciones (escenas/NN.html) con el mismo molde.

Cada lección: número grande a la izquierda; la lección escrita a mano; la pregunta para pensar en dorado;
la referencia debajo. La primera escena lleva la portada "Lecciones y preguntas para pensar".
Las frases de anclaje ("ancla" y "preg") tienen que decirse tal cual en la voz de la escena.
"""
from pathlib import Path

ESC = Path(__file__).resolve().parent.parent / "escenas"

LECCIONES = {
    "47": ("Génesis 37", "Génesis treinta y siete", True, [
        ("Primera", "El favoritismo de Jacob <b>hirió a toda la familia</b>", "¿Sabe cada uno en casa que lo queremos?",
         "Sabe cada uno", "<i>La Atalaya</i>, 1 de agosto de 2014, pág. 12: “Los padres sabios hacen todo lo posible por confirmarles […] que los quieren”"),
        ("Segunda", "Los celos empezaron por no poder hablarle bien a un hermano, y <b>terminaron en una venta</b>", "¿Qué hacemos cuando a un hermano le va mejor que a nosotros?",
         "Qué hacemos", "37:4 · Romanos 12:15 · <i>La Atalaya</i>, 1 de agosto de 2014, pág. 12"),
        ("Tercera", "José fue a buscar a sus hermanos aunque no lo querían, y Rubén <b>habló</b> cuando los demás querían matar", "¿Nos atrevemos a hablar cuando otros hacen algo malo?",
         "Nos atrevemos", "37:13, 21, 22"),
    ]),
    "48": ("Génesis 38", "Génesis treinta y ocho", False, [
        ("Primera", "Judá prometió y <b>no cumplió</b>, por miedo", "¿Tengo pendiente alguna promesa que le hice a mi familia?",
         "Tengo pendiente", "38:11, 14"),
        ("Segunda", "Judá <b>reconoció su error</b> en voz alta", "¿Me cuesta admitir delante de otros que me equivoqué?",
         "Me cuesta admitir", "38:26 · <i>La Atalaya</i>, 15 de enero de 1983, pág. 29: “al menos admitió su error”"),
        ("Tercera", "Jehová bendijo a Judá aunque cometió errores graves: <b>se fija en lo bueno</b> de sus siervos", "¿Me quedo yo con lo bueno de los demás?",
         "Me quedo yo", "<i>La Atalaya</i> (estudio), junio de 2025, págs. 6, 7"),
    ]),
    "49": ("Génesis 39", "Génesis treinta y nueve", False, [
        ("Primera", "José ya había decidido <b>antes</b> de la tentación, y pudo decir que no, día tras día", "¿Qué haríamos si nos pasa en la escuela, en un viaje o con el teléfono?",
         "Qué haríamos", "39:10 · <i>La Atalaya</i> (estudio), agosto de 2025, pág. 24"),
        ("Segunda", "Jehová no evitó la injusticia, pero <b>estuvo con José</b> en la prisión", "¿Buscamos cada día al menos una bendición de Jehová?",
         "Buscamos cada día", "39:21 · <i>La Atalaya</i> (estudio), enero de 2023, pág. 19"),
        ("Tercera", "José <b>trabajó bien</b> como esclavo y como preso", "¿Hago bien el trabajo que me toca, aunque no sea el que quiero?",
         "Hago bien el trabajo", "39:4, 22 · <i>Seamos valientes al andar con Dios</i>, cap. 8, pág. 45"),
    ]),
    "50": ("Génesis 40", "Génesis cuarenta", False, [
        ("Primera", "José notó <b>las caras tristes</b> de otros cuando él mismo estaba preso", "¿Me doy cuenta de cuándo alguien a mi lado está mal?",
         "Me doy cuenta", "40:6, 7 · <i>La Atalaya</i>, 1 de febrero de 2015, pág. 13"),
        ("Segunda", "José dio <b>el mérito a Dios</b>, y dijo la verdad aunque fuera una mala noticia", "¿A quién le doy el mérito cuando algo me sale bien?",
         "A quién le doy", "40:8 · <i>La Atalaya</i>, 1 de febrero de 2015, pág. 14"),
        ("Tercera", "El copero se olvidó de quien lo había ayudado, pero <b>Jehová no se olvidó</b> de José", "¿Me acuerdo de agradecer a quien me ayudó?",
         "Me acuerdo de agradecer", "40:23 · <i>La Atalaya</i>, 1 de febrero de 2015, pág. 14"),
    ]),
    "51": ("Génesis 41", "Génesis cuarenta y uno", False, [
        ("Primera", "José esperó trece años y nunca perdió <b>la humildad, la fe ni su carácter amable</b>", "Si llevamos tiempo sufriendo una injusticia, ¿qué nos ayuda a no desesperarnos?",
         "Si llevamos tiempo", "<i>La Atalaya</i>, 1 de febrero de 2015, pág. 15"),
        ("Segunda", "Delante del hombre más poderoso de Egipto, José dijo: <b>“Yo no soy nadie”</b>", "¿Busco que me reconozcan a mí, o a Jehová?",
         "Busco que me reconozcan", "41:16 · <i>La Atalaya</i>, 1 de febrero de 2015, pág. 15"),
        ("Tercera", "José puso a sus hijos nombres que recordaban <b>lo que Dios había hecho</b> por él", "¿Repasamos en familia lo bueno que Jehová ha hecho por nosotros, aun en los años difíciles?",
         "Repasamos en familia", "41:51, 52"),
    ]),
}

PORTADA = """<div class="portada"><div class="r">al final, todas juntas</div><div class="t">Lecciones y preguntas para pensar</div></div>
"""
ESTILO = """<style>
.leccion .l { font-size: 100px; }
.leccion .p { font-size: 64px; }
.leccion .s { font-size: 30px; }
.portada { position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 20px; text-align: center; }
.portada .t { font-family: "Fraunces", serif; font-weight: 700; font-size: 110px; line-height: 1.05; }
.portada .r { font-family: "Montserrat", sans-serif; font-weight: 800; font-size: 34px; letter-spacing: 0.22em; color: var(--verde); text-transform: uppercase; }
</style>
"""


def escena(num, cap, ancla, portada, lista):
    h = ESTILO + "\n"
    if portada:
        h += PORTADA
    h += f"""<div class="seccion"><span class="r">Lecciones y preguntas para pensar</span><span class="t">{cap}</span></div>
<div class="seccion-linea"><svg viewBox="0 0 1740 20" preserveAspectRatio="none" style="width:100%;height:20px"><path d="M 4 10 C 400 4 900 16 1736 8"/></svg></div>
"""
    for i, (orden, l, p, _, ref) in enumerate(lista, 1):
        h += f"""<div class="leccion l{i}"><div class="n">{i}</div><div class="cuerpo"><div class="l">{l}</div><div class="p"><span class="k">PARA PENSAR</span>{p}</div><div class="s">{ref}</div></div></div>
"""
    h += "\n<script>\n"
    if portada:
        h += f"""entra(".portada .r", 0.3, {{ y: 20 }});
entra(".portada .t", 0.6, {{ y: 40, d: 0.8 }});
sale(".portada", at("{ancla}") - 0.6, {{ y: -40, d: 0.5 }});
const t0 = at("{ancla}");
"""
    else:
        h += "const t0 = 0.3;\n"
    h += """entra(".seccion", t0, { y: -20 });
traza(".seccion-linea path", t0 + 0.3, 1.0);
"""
    sec = ", ".join(f'[".l{i}", at("{o}")]' for i, (o, *_r) in enumerate(lista, 1))
    h += f"secuencia([{sec}], null, {{ y: 30, d: 0.6 }});\n"
    for i, (_, _, _, preg, _) in enumerate(lista, 1):
        h += f'entra(".l{i} .p", at("{preg}") - 0.2, {{ y: 20 }});\nentra(".l{i} .s", at("{preg}") + 0.2, {{ y: 10 }});\n'
    h += "</script>\n"
    (ESC / f"{num}.html").write_text(h)
    print("escenas/%s.html" % num)


if __name__ == "__main__":
    for num, (cap, ancla, portada, lista) in LECCIONES.items():
        escena(num, cap, ancla, portada, lista)
