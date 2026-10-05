#!/usr/bin/env python3
"""Genera las escenas de lecciones (escenas/NN.html) con el mismo molde.

Cada lección: número grande a la izquierda; la lección escrita a mano; la pregunta para pensar en dorado;
la referencia debajo. La primera escena lleva la portada "Lecciones y preguntas para pensar".
Las frases de anclaje ("ancla" y "preg") tienen que decirse tal cual en la voz de la escena.
"""
from pathlib import Path

ESC = Path(__file__).resolve().parent.parent / "escenas"

LECCIONES = {
    "52": ("Génesis 10", "Génesis diez", True, [
        ("Primera", "Todos venimos de <b>la misma familia</b>", "¿Qué decimos cuando salen chistes racistas en la escuela o en el trabajo?",
         "Qué decimos", "10:32 · Hechos 17:26: “De un solo hombre creó todas las naciones humanas”"),
        ("Segunda", "Nemrod fue famoso, pero <b>en oposición a Jehová</b>", "¿A quién admiramos en casa, y por qué?",
         "A quién admiramos", "10:9"),
        ("Tercera", "A Jehová le importan los pueblos, <b>uno por uno</b>", "¿De cuál de las tres ramas venimos? No se puede saber, y da igual.",
         "De cuál de las tres", "la tabla guarda setenta familias con nombre · 10:32"),
    ]),
    "53": ("Génesis 11", "Génesis once", False, [
        ("Primera", "“Así nos <b>haremos famosos</b>”", "¿Trabajamos para que nos vean, o para Jehová?",
         "Trabajamos para", "11:4"),
        ("Segunda", "Estar unidos <b>no basta</b>: en Babel lo estaban, y contra Dios", "Si cada uno en casa hablara un idioma distinto, ¿qué dejaríamos de poder hacer? ¿Y qué nos une en la congregación?",
         "Si cada uno", "11:6 · Sofonías 3:9: “un idioma puro”"),
        ("Tercera", "La vida se acorta: “<b>Enséñanos a contar nuestros días</b>”", "¿En qué se nos va el tiempo?",
         "En qué se nos va", "11:10-32 · Salmo 90:12"),
    ]),
    "54": ("Génesis 12", "Génesis doce", False, [
        ("Primera", "Abrán dejó una casa de dos pisos para <b>vivir en tiendas</b>", "¿Qué comodidad nos cuesta soltar por Jehová?",
         "Qué comodidad", "12:1, 8 · Hebreos 11:9"),
        ("Segunda", "Un <b>altar en cada parada</b>", "En viajes, mudanzas o vacaciones, ¿la adoración en familia sigue primero?",
         "En viajes", "12:7, 8"),
        ("Tercera", "Abrán pidió <b>por favor</b>, y Sarái colaboró", "En casa, ¿buscamos la colaboración del otro, o damos órdenes?",
         "En casa buscamos", "12:11-13 · <i>La Atalaya</i>, 15 de agosto de 2001"),
    ]),
    "55": ("Génesis 13", "Génesis trece", False, [
        ("Primera", "Abrán cedió su derecho, y <b>no salió perdiendo</b>", "¿Qué podemos ceder esta semana en casa para que haya paz?",
         "Qué podemos ceder", "13:8, 9, 14-17 · 1 Corintios 10:24: “Que nadie busque su propio beneficio, sino el de los demás”"),
        ("Segunda", "Lot escogió por <b>lo que se veía verde</b>", "Al escoger trabajo, estudios o casa, ¿qué pesa más?",
         "Al escoger", "13:10-13"),
        ("Tercera", "Después del mal rato en Egipto, Abrán <b>volvió al altar</b>", "¿Son prioritarios en nuestro hogar el estudio y la oración en familia, y las reuniones?",
         "Son prioritarios", "13:3, 4 · la pregunta es de <i>La Atalaya</i>, 15 de agosto de 2001, pág. 23"),
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
