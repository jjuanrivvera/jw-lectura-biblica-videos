#!/usr/bin/env python3
"""Genera escenas/27.html a 30.html: las lecciones de Éxodo 1 a 4, una escena por capítulo.

Cada lección lleva el texto corto en pantalla, su pregunta para pensar (la que dice la voz) y la
referencia que la sostiene. La investigación marca estas aplicaciones como "observación propia":
va rotulado en pantalla, la voz no lo dice. Las anclas (Primera, Segunda, Tercera y el comienzo de
cada pregunta) las valida construir.mjs contra la voz.
"""
from pathlib import Path

ESC = Path(__file__).resolve().parent.parent / "escenas"

LECCIONES = {
    "27": ("Éxodo 1", [
        ("El temor a Dios <b>puede requerir valor</b>", "¿Cómo respondería yo si un grupo presiona a alguien para hacer daño?", "cómo respondería yo",
         "Sifrá y Puá midieron la orden del rey por lo que era: quitar una vida inocente · Éxodo 1:15-17 · Hechos 5:29"),
        ("Una política injusta <b>no define el valor de sus víctimas</b>", "¿Cómo miro a quienes otros tratan como una carga?", "cómo miro a quienes",
         "El faraón llamó amenaza a una familia que solo crecía; Jehová vio personas y escuchó su sufrimiento · Éxodo 1:9-14; 2:23-25"),
        ("La bondad <b>puede sobrevivir</b> en un ambiente hostil", "¿Quién necesita protección concreta esta semana?", "quién necesita protección",
         "Las parteras y después la hija del faraón eligen preservar una vida · Éxodo 1:17; 2:5, 6"),
    ]),
    "28": ("Éxodo 2", [
        ("El valor puede expresarse <b>con cuidado, no con imprudencia</b>", "¿Cuál sería una manera segura de proteger a alguien vulnerable?", "cuál sería una manera segura",
         "Jokébed protegió a su hijo con una canasta preparada; Míriam observó y habló en el momento oportuno · Éxodo 2:3-8"),
        ("La buena intención necesita <b>buen juicio y tiempo</b>", "Antes de intervenir, ¿pido consejo y pienso en las consecuencias?", "antes de intervenir",
         "Moisés quería defender a su pueblo, pero la muerte del egipcio lo obligó a huir · Éxodo 2:11-15"),
        ("Una etapa que parece pequeña <b>puede prepararnos</b>", "¿Qué estoy aprendiendo hoy sirviendo sin protagonismo?", "qué estoy aprendiendo hoy",
         "El trabajo de pastor fue parte de los cuarenta años previos a su misión · Hechos 7:30"),
    ]),
    "29": ("Éxodo 3", [
        ("Jehová <b>no trata el sufrimiento</b> como algo invisible", "Cuando alguien me cuenta su carga, ¿lo escucho primero, sin minimizarla?", "cuando alguien me cuenta",
         "Dice que ve, oye y conoce bien lo que vive su pueblo · Éxodo 3:7-9"),
        ("Una tarea difícil puede empezar con <b>una promesa de apoyo</b>", "¿Cómo puedo dividir una responsabilidad en pasos y pedir ayuda?", "cómo puedo dividir",
         "Jehová responde a la inseguridad de Moisés: “Yo estaré contigo” · Éxodo 3:11, 12"),
        ("El nombre de Dios <b>da razones para confiar</b>", "Al estudiar una promesa, ¿qué revela del carácter de quien la hizo?", "al estudiar una promesa",
         "Jehová puede hacer lo necesario para cumplir sus promesas · Éxodo 3:14, 15"),
    ]),
    "30": ("Éxodo 4", [
        ("Podemos reconocer una limitación y <b>aceptar apoyo</b>", "En casa, ¿cómo repartimos una tarea según las habilidades de cada uno?", "en casa, cómo repartimos",
         "Jehová le dio a Moisés un portavoz sin quitarle su responsabilidad · Éxodo 4:10-16"),
        ("La obediencia incluye <b>la propia vida familiar</b>", "¿Obedezco por convicción?", "obedezco por convicción",
         "Quien lleva un encargo también debe cuidar lo que Jehová pide en su hogar · Éxodo 4:24-26"),
        ("Escuchar que alguien ve nuestro dolor <b>puede devolver esperanza</b>", "¿Escucho sin distraerme y actúo con cariño?", "escucho sin distraerme",
         "Los israelitas creyeron al saber que Jehová se había fijado en ellos · Éxodo 4:31"),
    ]),
}

PLANTILLA = """<style>
.leccion .l {{ font-size: 126px; }}
.leccion .p {{ font-size: 70px; }}
.leccion .cuerpo {{ gap: 40px; }}
.leccion .s {{ font-size: 36px; }}
.leccion .n {{ font-size: 270px; }}
.leccion {{ grid-template-columns: 260px 1fr; }}
.pro-l {{ position: absolute; right: 90px; top: 74px; font-size: 34px; }}
</style>

<div class="seccion"><span class="r">Lecciones y preguntas para pensar</span><span class="t">{cap}</span></div>
<div class="seccion-linea"><svg viewBox="0 0 1740 20" preserveAspectRatio="none" style="width:100%;height:20px"><path d="M 4 10 C 400 4 900 16 1736 8"/></svg></div>
<div class="propio chico pro-l">observación propia</div>
{lecs}
<script>
entra(".seccion", 0.3, {{ y: -20 }});
traza(".seccion-linea path", 0.6, 1.0);
secuencia([[".l1", at("Primera")], [".l2", at("Segunda")], [".l3", at("Tercera")]], null, {{ y: 30, d: 0.6 }});
{anclas}
</script>
"""

for num, (cap, lecs) in LECCIONES.items():
    html, anclas = [], []
    for i, (texto, preg, ancla, src) in enumerate(lecs, 1):
        html.append(f'<div class="leccion l{i}"><div class="n">{i}</div><div class="cuerpo"><div class="l">{texto}</div>'
                    f'<div class="p"><span class="k">PARA PENSAR</span>{preg}</div><div class="s">{src}</div></div></div>')
        anclas.append(f'entra(".l{i} .p", at("{ancla}") - 0.2, {{ y: 20 }});\nentra(".l{i} .s", at("{ancla}") + 0.3, {{ y: 10 }});')
    (ESC / f"{num}.html").write_text(PLANTILLA.format(cap=cap, lecs="\n".join(html), anclas="\n".join(anclas)))
    print(num, cap)
