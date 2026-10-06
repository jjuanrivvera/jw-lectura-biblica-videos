#!/usr/bin/env python3
"""Genera escenas/50.html a 55.html: las lecciones de Génesis 42 a 47, una escena por capítulo.

Cada lección lleva el texto corto en pantalla, su pregunta para pensar (la que dice la voz), la
fuente cuando la lección cita una publicación, y el rótulo "observación propia" cuando la
investigación la marca así. Las anclas (Primera, Segunda, Tercera y el comienzo de cada pregunta)
las valida construir.mjs contra la voz.
"""
from pathlib import Path

ESC = Path(__file__).resolve().parent.parent / "escenas"

LECCIONES = {
    "50": ("Génesis 42", [
        ("José tenía poder para vengarse, y <b>no se dejó llevar por sus impulsos</b>", "<i>La Atalaya</i>, 1 de mayo de 2015, pág.&nbsp;13", False,
         "¿Qué hacemos cuando alguien nos hiere?", "Qué hacemos cuando"),
        ("Un pecado sin arreglar <b>no se olvida solo</b>", "la conciencia de los hermanos despertó veinte años después · 42:21", False,
         "¿Hay algo que tengamos que arreglar, con Jehová o con alguien?", "Hay algo que"),
        ("Jacob creyó que todo estaba en su contra, y <b>Jehová estaba juntando a su familia</b>", "42:36", True,
         "¿Qué situación nuestra quizá todavía no ha llegado a su final?", "Qué situación nuestra"),
    ]),
    "51": ("Génesis 43", [
        ("Judá no prometió lo que harían otros, sino <b>lo que haría él</b>", "“Yo asumo la responsabilidad” · 43:9", False,
         "¿Cumplimos lo que prometemos en casa?", "Cumplimos lo que"),
        ("Jacob mandó devolver un dinero que <b>nadie reclamaba</b>", "43:12 · <i>Continúe en el amor de Dios</i>, cap.&nbsp;14, pág.&nbsp;190", False,
         "¿Somos honrados aunque nadie se vaya a dar cuenta?", "Somos honrados"),
        ("En la congregación, <b>nadie es algo detestable</b> para nadie", "José era extranjero y pastor, y dio de comer a todos · 43:32", True,
         "¿Tratamos a alguien como si valiera menos?", "Tratamos a alguien"),
    ]),
    "52": ("Génesis 44", [
        ("Pudieron irse, y <b>no dejaron solo a Benjamín</b>", "44:13", False,
         "¿Cómo apoyamos al que está en problemas, aunque parezca culpable?", "Cómo apoyamos"),
        ("Judá no se justificó: <b>reconoció el error</b>", "admitirlo sin excusas abre la puerta a la reconciliación · 44:16", False,
         "¿Nos cuesta decir: “me equivoqué”?", "Nos cuesta decir"),
        ("“Jehová siempre se fija en las <b>cosas buenas</b> de sus siervos”", "<i>La Atalaya</i> (estudio), junio de 2025, pág.&nbsp;6", False,
         "¿Qué cambio nos gustaría que Jehová viera en nosotros?", "Qué cambio nos"),
    ]),
    "53": ("Génesis 45", [
        ("José <b>no humilló</b> a sus hermanos delante de otros", "hizo salir a todos · 45:1", False,
         "¿Cuidamos la dignidad del otro cuando hay que corregir algo?", "Cuidamos la dignidad"),
        ("Perdonar al que se arrepiente <b>alivia nuestro dolor y el suyo</b>", "<i>La Atalaya</i>, 1 de mayo de 2015, pág.&nbsp;15", False,
         "¿Hay alguien a quien nos cuesta perdonar?", "Hay alguien a quien"),
        ("José vio la mano de Dios <b>al final</b>, no al principio", "veintidós años difíciles", True,
         "¿Confiamos en que Jehová sabe para qué servirá lo que hoy nos duele?", "Confiamos en que"),
    ]),
    "54": ("Génesis 46", [
        ("Jacob no dio un paso grande <b>sin consultar a Jehová</b>", "46:1-3", False,
         "¿Oramos en familia antes de una decisión importante?", "Oramos en familia"),
        ("“<b>Yo mismo bajaré contigo</b>”", "Dios no le prometió que Egipto sería fácil · 46:4", False,
         "¿Qué nos preocupa del futuro?", "Qué nos preocupa"),
        ("Podemos aceptar <b>ser distintos</b> si eso nos mantiene cerca de Jehová", "José usó el desprecio de Egipto para proteger a su familia · 46:34", True,
         "¿En qué nos cuesta ser distintos?", "En qué nos cuesta"),
    ]),
    "55": ("Génesis 47", [
        ("Años difíciles, y <b>no dejó de adorar a Dios</b>", "“En el nuevo mundo, sus años no serán pocos ni difíciles” · <i>Seamos valientes al andar con Dios</i>, cap.&nbsp;7, pág.&nbsp;41", False,
         "¿Qué nos ayuda a seguir adorando a Jehová en años difíciles?", "Qué nos ayuda"),
        ("Todo lo cobrado, <b>a la casa del faraón</b>", "47:14", False,
         "¿Cuidamos con honradez lo que se nos confía?", "Cuidamos con honradez"),
        ("Pidió ser enterrado <b>donde Dios había prometido</b>", "no donde estaba cómodo · 47:30", True,
         "¿Qué ven nuestros hijos en nuestras decisiones: que creemos en las promesas de Jehová?", "Qué ven nuestros"),
    ]),
}

ORD = ["Primera", "Segunda", "Tercera"]

CSS = """<style>
.leccion .l { font-size: 88px; }
.leccion .fu { font-family: "Montserrat", sans-serif; font-weight: 600; font-size: 26px; line-height: 1.3; color: #d5dbe1; margin-top: -18px; }
.leccion .fu i { color: var(--tiza); }
.leccion .p { font-size: 60px; }
.leccion .propio { font-size: 32px; margin-top: -16px; }
.portada { position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; }
.portada .t1 { font-family: "Fraunces", serif; font-weight: 700; font-size: 150px; line-height: 1; }
.portada .t2 { font-family: "Caveat", cursive; font-weight: 700; font-size: 84px; color: var(--verde); margin-top: 20px; }
.portada svg { width: 760px; height: 36px; margin-top: 14px; }
.portada svg path { fill: none; stroke: var(--verde); stroke-width: 7; stroke-linecap: round; }
.pista.lec { position: absolute; left: 0; right: 0; bottom: 60px; }
.pista.lec span.on { background: var(--verde); border-color: var(--verde); }
</style>
"""


def escena(num, cap, lecciones):
    portada = num == "50"
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
    caps = ["42", "43", "44", "45", "46", "47"]
    actual = cap.split()[-1]
    h.append('<div class="pista lec">' + "".join(
        f'<span class="{"on" if c == actual else ("hecho" if c < actual else "")}">{c}</span>' for c in caps) + '</div>')
    js = ["<script>"]
    if portada:
        js.append('const t0 = at("Génesis cuarenta y dos");')
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
    js.append("</script>")
    return "\n".join(h) + "\n\n" + "\n".join(js) + "\n"


for num, (cap, lecs) in LECCIONES.items():
    (ESC / f"{num}.html").write_text(escena(num, cap, lecs), encoding="utf-8")
    print(f"escenas/{num}.html")
