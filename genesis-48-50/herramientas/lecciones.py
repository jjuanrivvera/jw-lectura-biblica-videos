#!/usr/bin/env python3
"""Genera escenas/54.html a 56.html: las lecciones de Génesis 48 a 50, una escena por capítulo.

Cada lección lleva el texto corto en pantalla, su pregunta para pensar (la que dice la voz), la
fuente cuando la lección cita una publicación, y el rótulo "observación propia" cuando la
investigación la marca así. Las anclas (Primera, Segunda, Tercera y el comienzo de cada pregunta)
las valida construir.mjs contra la voz.
"""
from pathlib import Path

ESC = Path(__file__).resolve().parent.parent / "escenas"

LECCIONES = {
    "54": ("Génesis 48", [
        ("Escuchar a los mayores <b>mientras aún podemos</b>", "José llevó a sus hijos cuando supo que su padre estaba débil · 48:1-4, 9-11", True,
         "¿Qué experiencia de confianza en Jehová nos gustaría que los niños escucharan de sus abuelos?", "Qué experiencia de"),
        ("No medir el valor de un hijo <b>por su posición</b>", "el menor recibió el primer lugar, y el mayor también fue bendecido · 48:19, 20", True,
         "¿Repartimos el cariño según quién nació primero, o según quién destaca más?", "Repartimos el cariño"),
        ("El dolor y la gratitud <b>pueden ir juntos</b>", "Jacob recordó a Raquel y dio gracias por los hijos de José · 48:7, 11", True,
         "¿Hablamos con cariño de los que ya no están?", "Hablamos con cariño"),
    ]),
    "55": ("Génesis 49", [
        ("Hablar claro de las consecuencias, <b>sin etiquetas para siempre</b>", "Rubén siguió en la familia; los levitas eligieron la lealtad · 49:3-7; Éxodo 32:26-29 · <i>La Atalaya</i>, junio de 2025, parte 1, págs.&nbsp;4 a 5", False,
         "¿Les dejamos espacio para elegir bien?", "Les dejamos espacio"),
        ("La indignación <b>no nos da permiso para herir</b>", "49:5-7; Santiago 1:19, 20 · <i>La Atalaya</i>, junio de 2025, parte 1, pág.&nbsp;5", False,
         "¿Cómo reaccionamos cuando le hacen daño a uno de los nuestros?", "Cómo reaccionamos"),
        ("Reconocer el cambio <b>con hechos concretos</b>", "Judá se ofreció por Benjamín · 44:30-34; 49:8, 9 · <i>La Atalaya</i>, junio de 2025, parte 1, págs.&nbsp;5 a 7", False,
         "¿Elogiamos el cambio de un familiar con la misma precisión con que le señalamos un error?", "Elogiamos el cambio"),
    ]),
    "56": ("Génesis 50", [
        ("Podemos llorar <b>y seguir confiando</b>", "José lloró y se ocupó del entierro de su padre · 50:1-3", True,
         "¿Cómo acompañamos a alguien de la familia que está de duelo?", "Cómo acompañamos"),
        ("El perdón necesita <b>seguridad y hechos</b>", "50:19-21 · <i>La Atalaya</i>, 1 de mayo de 2015, pág.&nbsp;15", False,
         "¿Mostramos con hechos que de verdad perdonamos?", "Mostramos con hechos"),
        ("Dejarles a los hijos <b>algo más que recuerdos</b>", "una tarea unida a una promesa de Dios · 50:24, 25; Hebreos 11:22", True,
         "¿Saben nuestros hijos qué esperanza nos sostiene, y en qué texto pueden leerla?", "Saben nuestros hijos"),
    ]),
}

ORD = ["Primera", "Segunda", "Tercera"]

CSS = """<style>
.leccion .l { font-size: 100px; }
.seccion { gap: 52px; }
.leccion .fu { font-family: "Montserrat", sans-serif; font-weight: 600; font-size: 34px; line-height: 1.3; color: #f1f4f7; margin-top: -10px; }
.leccion .fu i { color: var(--tiza); }
.leccion .p { font-size: 60px; }
.leccion .propio { font-size: 32px; margin-top: -16px; }
.portada { position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; }
.portada .t1 { font-family: "Fraunces", serif; font-weight: 700; font-size: 150px; line-height: 1; }
.portada .t2 { font-family: "Caveat", cursive; font-weight: 700; font-size: 84px; color: var(--verde); margin-top: 20px; }
.portada svg { width: 760px; height: 36px; margin-top: 14px; }
.portada svg path { fill: none; stroke: var(--verde); stroke-width: 7; stroke-linecap: round; }
.pista.lec { position: absolute; left: 0; right: 0; bottom: 60px; }
.pista.lec span { color: rgba(241, 233, 216, 0.88); border-color: rgba(241, 233, 216, 0.5); }
.pista.lec span.hecho { color: rgba(233, 191, 96, 0.95); border-color: rgba(233, 191, 96, 0.6); }
.pista.lec span.on { color: #17212b; background: var(--verde); border-color: var(--verde); }
</style>
"""


def escena(num, cap, lecciones):
    portada = num == "54"
    h = [CSS]
    if portada:
        h.append('<div class="portada pt"><div class="t1">Lecciones</div><svg viewBox="0 0 760 36"><path d="M 10 20 C 200 6 480 30 750 14" /></svg>'
                 '<div class="t2">y preguntas para pensar, capítulo por capítulo</div></div>')
    h.append(f'<div class="seccion"><span class="r">Lecciones</span><span class="t">{cap}</span></div>')
    h.append('<svg class="seccion-linea" viewBox="0 0 1740 20" preserveAspectRatio="none"><path d="M 4 10 C 400 4 1200 16 1736 8" /></svg>')
    for i, (l, fu, propia, preg, _) in enumerate(lecciones):
        h.append(f'<div class="leccion le{i}"><div class="n">{i + 1}</div><div class="cuerpo">'
                 f'<div class="l">{l}</div>'
                 + (f'<div class="fu">{fu}</div>' if fu else "")
                 + ('<span class="propio chico">observación propia</span>' if propia else "")
                 + f'<div class="p pr{i}"><span class="k">PREGUNTA PARA PENSAR</span>{preg}</div></div></div>')
    caps = ["48", "49", "50"]
    actual = cap.split()[-1]
    h.append('<div class="pista lec">' + "".join(
        f'<span class="{"on" if c == actual else ("hecho" if c < actual else "")}">{c}</span>' for c in caps) + '</div>')
    js = ["<script>"]
    if portada:
        js.append('const t0 = at("Primera") - 0.3;')
        js.append('entra(".pt .t1", 0.3, { y: 40, d: 0.8 });')
        js.append('traza(".pt svg path", 0.8, 0.9);')
        js.append('escribe(".pt .t2", 1.2, 1.2);')
        js.append('sale(".pt", t0 - 0.6, { y: -40 });')
        js.append('entra(".seccion", t0 - 0.2, { y: -20 });')
        js.append('traza(".seccion-linea path", t0, 1.0);')
    else:
        js.append('entra(".seccion", 0.3, { y: -20 });')
        js.append('traza(".seccion-linea path", 0.6, 1.0);')
    js.append('entra(".pista.lec", 0.8, { y: 16 });' if not portada else 'entra(".pista.lec", t0, { y: 16 });')
    lista = ", ".join(f'[".le{i}", at("{ORD[i]}") - 0.2]' for i in range(3))
    js.append(f"secuencia([{lista}], null, {{ y: 30, d: 0.6 }});")
    for i, (_, _, _, _, ancla) in enumerate(lecciones):
        js.append(f'entra(".pr{i}", at("{ancla}") - 0.3, {{ x: -30, y: 0 }});')
        # Empieza centrado sin la pregunta y sube cuando ella entra.
        js.append(f'centra([".le{i} .cuerpo", ".le{i} .n"], 110, at("{ancla}") - 0.9, 0.7);')
    js.append("</script>")
    return "\n".join(h) + "\n\n" + "\n".join(js) + "\n"


for num, (cap, lecs) in LECCIONES.items():
    (ESC / f"{num}.html").write_text(escena(num, cap, lecs), encoding="utf-8")
    print(f"escenas/{num}.html")
