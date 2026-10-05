#!/usr/bin/env python3
"""Genera las escenas de lecciones (una por capítulo) a partir de la tabla de abajo.

Cada lección: (ancla de la voz, lección, ancla de la pregunta o reflexión, pregunta o reflexión).
Las anclas tienen que ser palabras que la voz dice en NARRACION.md; construir.mjs lo comprueba.
Uso: herramientas/lecciones.py   (escribe escenas/45.html a 49.html)
"""
from pathlib import Path

ESC = Path(__file__).resolve().parent.parent / "escenas"
LECCIONES = {
    "45": ("Génesis 5", [
        ("Primera", "La vida larga no arregla el problema de fondo: <b>solo lo alarga</b>", "Qué haría", "¿Qué haría uno distinto si le dieran novecientos años?"),
        ("Segunda", "Enoc anduvo con Dios trescientos años, <b>sin congregación y sin Biblia</b>", "Te has sentido", "¿Te has sentido el único de tu salón o de tu trabajo que piensa así? Él estuvo ahí primero"),
        ("Tercera", "Lamec no alcanzó a ver lo que esperaba, <b>y sirvió igual</b>", "No todo lo que", "No todo lo que uno siembra da fruto dentro de su propia vida"),
    ]),
    "46": ("Génesis 6", [
        ("Primera", "A Jehová <b>le duele</b> el mal", "No es un juez", "No es un juez frío"),
        ("Segunda", "Noé hizo todo tal como Dios le había dicho: <b>ni un atajo ni una mejora propia</b>", "Dónde tiendo", "¿Dónde tiendo yo a cambiar las instrucciones?"),
        ("Tercera", "Noé predicó durante décadas, nadie de fuera le hizo caso, y la Biblia lo llama <b>fiel</b>", "Cómo medimos", "¿Cómo medimos el éxito: por los que hacen caso, o por la obediencia?"),
    ]),
    "47": ("Génesis 7", [
        ("Primera", "La puerta estuvo abierta siete días y <b>nadie más entró</b>", "El problema no", "El problema no fue la falta de pruebas"),
        ("Segunda", "<b>Jehová</b> cerró la puerta", "El que avisa", "El que avisa no es responsable de que le hagan caso: solo de avisar"),
        ("Tercera", "Comer, beber y casarse no eran pecados; fue <b>la indiferencia</b>", "Qué cosas buenas", "¿Qué cosas buenas nos están distrayendo?"),
    ]),
    "48": ("Génesis 8", [
        ("Primera", "Si Jehová se acordó de los animales del arca…", "se acuerda de su", "…se acuerda de su familia"),
        ("Segunda", "Noé vio tierra seca 56 días antes de pisarla, y <b>esperó la orden</b>", "Hay veces", "Hay veces en que lo correcto es esperar, aunque ya se pueda"),
        ("Tercera", "Lo primero fue <b>un altar</b>, no una casa", "Si nuestra familia", "Si nuestra familia empezara mañana de cero, ¿qué sería lo primero?"),
    ]),
    "49": ("Génesis 9", [
        ("Primera", "Un solo límite en toda la despensa: <b>la sangre</b>", "Conocemos el origen", "¿Conocemos el origen de lo que creemos, o solo la regla?"),
        ("Segunda", "El valor de una persona no está en lo que produce ni en su edad…", "sino en de quién", "…sino en de quién lleva la imagen"),
        ("Tercera", "Cuando a alguien respetado se le ve algo feo, hay <b>dos caminos</b>", "el manto o el chisme", "El manto o el chisme. ¿Cuál escogemos?"),
    ]),
}

PLANTILLA = """<style>
.tres {{ position: absolute; left: 90px; right: 90px; top: 175px; bottom: 25px; display: flex; flex-direction: column; justify-content: center; gap: 34px; }}
.pq {{ display: grid; grid-template-columns: 130px 1fr; column-gap: 36px; align-items: start; border-left: 10px solid var(--verde); padding: 12px 0 12px 32px; }}
.pq .n {{ font-family: "Fraunces", serif; font-weight: 700; font-size: 120px; line-height: 0.9; color: var(--verde); }}
.pq .c {{ font-family: "Caveat", cursive; font-weight: 700; font-size: 66px; line-height: 1.04; color: var(--tiza); }}
.pq .c b {{ color: var(--oro); }}
.pq .p {{ font-family: "Fraunces", serif; font-style: italic; font-weight: 500; font-size: 48px; line-height: 1.16; color: var(--oro); margin-top: 12px; }}
</style>

<div class="seccion"><div class="r">Lecciones y preguntas</div><div class="t">{cap}</div></div>
<svg class="seccion-linea" viewBox="0 0 1740 20" preserveAspectRatio="none"><path d="M 4 12 C 400 4 1200 18 1736 8"/></svg>
<div class="tres">
{filas}
</div>

<script>
entra(".seccion", 0.3, {{ y: -20 }});
traza(".seccion-linea path", 0.6, 1.0);
{js}
</script>
"""

for num, (cap, filas) in LECCIONES.items():
    html_f, js = [], []
    for i, (a, lec, b, pre) in enumerate(filas, 1):
        html_f.append(f'  <div class="pq q{i}"><div class="n">{i}</div><div><div class="c">{lec}</div><div class="p">{pre}</div></div></div>')
        desde = "" if i == 1 else f', at("{filas[i - 2][0]}")'
        js.append(f'aparece(".q{i}", at("{a}"{desde}) - 0.3, 0.3);\nentra(".q{i} .n", at("{a}"{desde}) - 0.2, {{ y: 20 }});\n'
                  f'entra(".q{i} .c", at("{a}"{desde}), {{ y: 20 }});\nentra(".q{i} .p", at("{b}"), {{ y: 20 }});')
    (ESC / f"{num}.html").write_text(PLANTILLA.format(cap=cap, filas="\n".join(html_f), js="\n".join(js)))
    print("escena", num)
