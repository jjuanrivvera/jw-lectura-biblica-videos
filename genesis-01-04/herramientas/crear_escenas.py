#!/usr/bin/env python3
"""Archivo histórico del primer boceto. Las fuentes finales viven en escenas/."""
import html
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'escenas'
if any(OUT.glob('[0-9][0-9].html')):
    raise SystemExit('Boceto histórico: no sobrescribe escenas existentes. Edite escenas/ y ejecute construir.py.')
C={}
G='#efbe66';B='#acd6d2';F='#f5efdf';M='#66858c'

def e(s):return html.escape(str(s))
def attr(p=None,cue=None):return f' data-p="{p}"' if p is not None else (f' data-cue="{e(cue)}"' if cue else '')
def box(x,y,w,h,content,p=None,cls='',cue=None,extra=''):
    return f'<div class="{cls}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px"{attr(p,cue)} {extra}>{content}</div>'
def text(x,y,content,p=None,cls='copy',w=600,h=140,cue=None):return box(x,y,w,h,content,p,cls,cue)
def line(x1,y1,x2,y2,p=None,color=G,dash=False):
    return f'<path d="M{x1},{y1} L{x2},{y2}" fill="none" stroke="{color}" stroke-width="5" stroke-linecap="round"'+(f' stroke-dasharray="10 10"' if dash else '')+attr(p)+(f' data-motion="draw"' if p is not None and not dash else '')+'/>'
def svg(content,w=1768,h=728):return f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" aria-label="Diagrama explicativo">{content}</svg>'
def st(x,y,content,size=34,color=F,anchor='start',p=None):return f'<text x="{x}" y="{y}" style="font-size:{size}px;fill:{color}" text-anchor="{anchor}"{attr(p)}>{e(content)}</text>'
def rect(x,y,w,h,fill='#24424a',stroke=M,p=None):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" stroke="{stroke}" stroke-width="2"{attr(p)}/>'
def circle(x,y,r=10,fill=G,p=None):return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}"{attr(p)}/>'
def node(x,y,w,label,detail='',p=None):return box(x,y,w,180,f'<strong>{label}</strong><p>{detail}</p>',p,'node')
def flow(items,ps=None,y=240):
    n=len(items);w=(1768-(n-1)*75)/n;out='';paths=''
    for i,(title,detail) in enumerate(items):
        x=i*(w+75);p=ps[i] if ps else i
        out+=node(x,y,w,title,detail,p)
        if i:paths+=line(x-58,y+88,x-15,y+88,p)+f'<path d="M{x-26},{y+77} L{x-15},{y+88} L{x-26},{y+99}" fill="none" stroke="{G}" stroke-width="5"{attr(p)}/>'
    return svg(paths)+out
def foot(s,p=None):return f'<div class="foot-callout"{attr(p)}>{s}</div>'
def save(n,body,chapter,source,shape,title=None,own=None):
    key=f'{n:02}';(OUT/f'{key}.html').write_text(body)
    C[key]={'chapter':chapter,'source':source,'shape':shape}
    if title:C[key]['title']=title
    if own:C[key]['own']=own
def phases(entries,kind='lesson'):
    result=''
    for i,(p,head,body,question) in enumerate(entries):
        end=f' data-until-p="{entries[i+1][0]}"' if i+1<len(entries) else ''
        content=f'<div class="lesson-number">{i+1:02}</div><div class="lesson-copy"><div class="display">{head}</div><div class="copy">{body}</div><div class="lesson-question">{question}</div></div>'
        result+=f'<div class="phase" data-p="{p}"{end}>{content}</div>'
    return result

# La apertura ocupa el ancho como un índice visual que se construye con la primera frase.
body=svg(line(120,300,1650,300,0))
for i,(num,label,sub) in enumerate([('1','La creación','Un hogar preparado'),('2','El jardín','La primera familia'),('3','La caída','Una promesa'),('4','Dos hermanos','Decisiones y motivos')]):
    x=i*448
    body+=text(x,10,num,0,'display gold',400,220).replace('class="display gold"','class="display gold"').replace('height:220px','height:220px;font-size:210px')
    body+=text(x,375,label,0,'display',415,120).replace('font-size:210px','font-size:68px')
    body+=text(x,545,sub,1,'small blue',400,90)
save(0,body,'Lectura familiar','Génesis 1:1 a 4:26 · Traducción del Nuevo Mundo, edición de estudio','índice panorámico',title='Génesis 1 al 4')

body=text(0,30,'El principio',0,'display',710,125)+text(0,175,'Cielos y Tierra',0,'copy blue',660,70)
body+=text(970,30,'Seis días',1,'display gold',700,125)+text(970,175,'Preparación para la vida',1,'copy',740,75)
body+=svg(line(70,365,1660,365,0)+circle(150,365,15,p=0)+st(150,430,'Sin fecha indicada',31,B,p=0)+line(530,315,530,415,1,color=M,dash=True))
for i in range(6):body+=box(830+i*144,310,116,108,f'{i+1}',1,'node',extra='data-motion="rise" style-unused=""')
body+=foot('Ruaj · la fuerza activa de Jehová',2)
save(1,body,'Génesis 1 · Versículos 1 y 2','Perspicacia, «Creación», págs. 569-571; «Tierra», pág. 1123','línea temporal abierta')

body=text(0,20,'yohm',0,'display gold',630,140)+text(700,28,'Día · período',0,'display',1050,120)
body+=text(0,180,'La misma palabra puede abarcar duraciones distintas.',0,'copy',1700,100)
for i in range(6):body+=box(i*230,350,200,135,f'<div class="display" style="font-size:70px">{i+1}</div>',1,'node')
body+=box(1400,350,340,135,'<div class="display" style="font-size:70px">7 →</div>',1,'node')
body+=text(0,540,'Seis períodos creativos',1,'small',1000,55)+text(1400,540,'Descanso abierto',1,'small blue',365,80)
body+=foot('Duración exacta: no especificada',2)
save(2,body,'Génesis 1 y 2 · El tiempo','Perspicacia, «Día», págs. 676, 678; «Creación», pág. 572 · Hebreos 4:1-11','franja temporal')

body='<div class="duo">'
for day,label,desc,col in [('1','Luz difusa','ohr · luz en general',B),('4','Fuente visible','maor · lumbrera',G)]:
    drawing=f'<circle cx="415" cy="125" r="66" fill="{G}"/>'
    for j in range(7):drawing+=f'<path d="M{305+j*37},220 L{305+j*37},460" stroke="{col}" stroke-width="5" opacity=".65" data-p="1" data-motion="draw"/>'
    drawing+=f'<rect x="70" y="225" width="690" height="100" fill="{B}" opacity="{.86 if day=="1" else .15}"/>'
    drawing+=f'<path d="M30,505 Q220,480 400,505 T800,505" fill="none" stroke="{F}" stroke-width="7"/>'
    body+=f'<div><div class="eyebrow">Día {day}</div><div class="display" style="font-size:66px;margin-top:14px">{label}</div>{svg(drawing,820,535)}<div class="small">{desc}</div></div>'
body+='</div>'+box(670,535,430,130,'<div class="tag">Esquema explicativo</div>',None)
save(3,body,'Génesis 1 · Días 1 y 4','Perspicacia, «Creación», pág. 571 · jw.org, «¿Cuándo comenzó Dios a crear el universo?»','comparación atmosférica')

body=svg(rect(0,50,1768,170,'#335861',M,0)+rect(0,240,1768,200,'#223e48',M,0)+rect(0,460,850,165,'#477981',M,1)+rect(880,460,888,165,'#77644a',M,1)+st(60,140,'Aguas superiores',43,F,p=0)+st(60,350,'Expansión · espacio abierto',59,F,p=0)+st(60,555,'Aguas',44,F,p=1)+st(950,555,'Suelo seco y vegetación',42,F,p=1))
body+=text(1030,272,'Atmósfera',0,'hand',600,100)+foot('Fotosíntesis · las plantas aprovechan la luz para producir alimento',2)
save(4,body,'Génesis 1 · Días 2 y 3','Génesis 1:6-13 y nota · Perspicacia, «Creación», pág. 571 · jw.org, art. 82','corte de capas')

body=box(0,0,1768,270,'<img src="assets/creacion.jpg" style="width:1768px;height:931px;object-fit:contain;object-position:top" alt="Los seis días creativos, ilustración JW"/>',None,extra='style-unused=""')
body=body.replace('height:270px"','height:270px;overflow:hidden"')
body+=text(40,304,'PREPARAR',0,'eyebrow',700,50)+text(960,304,'LLENAR',0,'eyebrow',700,50)
for i,(a,b) in enumerate([('1 · Luz y oscuridad','4 · Lumbreras'),('2 · Aguas y espacio abierto','5 · Vida acuática y aves'),('3 · Suelo y vegetación','6 · Animales y humanidad')]):
    p=1 if i<2 else 2;y=372+i*101
    body+=text(40,y,a,p,'copy',745,65)+text(965,y,b,p,'copy gold',740,65)+svg(line(785,y+28,900,y+28,p))
save(5,body,'Génesis 1 · La secuencia','Génesis 1:3-31 · Imagen: «La ciencia y el relato de Génesis», pág. 26 · Diagrama de la investigación','seis días emparejados')

body=text(0,5,'«Hagamos»',0,'display gold',1600,130)+text(0,160,'Jehová y su Hijo unigénito',0,'copy',1600,80)
body+=flow([('Amor','Cualidades morales'),('Justicia','Capacidad de decidir'),('Conocer a Dios','Capacidad espiritual')],[1,1,1],290)
body+=foot('Un encargo · llenar la Tierra y cuidarla',2)
save(6,body,'Génesis 1 · Versículos 26 al 31','Perspicacia, «Creación», pág. 570; «Hombre», págs. 1163-1164; «Tierra», págs. 1123-1124','cualidades y propósito')

body=text(0,10,'7',0,'display gold',440,360).replace('height:360px','height:360px;font-size:290px')
body+=text(430,70,'Cesa la obra creadora terrestre',0,'display',1280,230)
body+=text(440,330,'Descanso no significa inactividad',0,'hand',1250,75)
body+=svg(line(70,510,1690,510,1)+circle(470,510,15,p=1)+circle(1380,510,15,p=1)+st(470,585,'Génesis 1 · panorama',36,F,'middle',1)+st(1380,585,'Génesis 2 · detalles',36,F,'middle',1))
save(7,body,'Génesis 2 · Un acercamiento','Perspicacia, «Creación», págs. 570, 572-574; «Sábado», págs. 880-882','número y lupa narrativa')

body=text(0,0,'Jehová',0,'display gold',650,130)+text(930,20,'YHWH',0,'display blue',730,130)
body+=flow([('Polvo','Del suelo'),('Aliento','Vida recibida'),('Persona viva','Néfesh')],[1,1,1],270)
body+=foot('Adán · hombre terrestre     /     adamá · suelo',2)
save(8,body,'Génesis 2 · Nombre y vida','Génesis 2:4, 7 y notas · Perspicacia, «Alma», págs. 95-96; «Tierra», pág. 1123','diagrama polvo y aliento')

body=node(0,0,600,'Edén','La región · «Placer»',0)+node(890,0,875,'Jardín','Una parte cultivada y regada',0)+svg(line(630,90,850,90,0))
body+=text(0,255,'Cultivar y cuidar',1,'display gold',1600,105)
body+=box(0,425,1080,190,'<div class="eyebrow">Permiso amplio</div><div class="quote" style="margin-top:15px;font-size:43px">«Puedes comer de todos los árboles del jardín hasta quedar satisfecho»</div>',2,'paper',extra='data-motion="slide"')
body+=box(1130,425,635,190,'<div class="eyebrow">Un límite</div><div class="copy" style="margin-top:15px">Reconocer el derecho de Jehová a decidir</div>',3,'node')
save(9,body,'Génesis 2 · El jardín','Génesis 2:15-17 · Perspicacia, «Edén», págs. 731-733; «Jardín», pág. 18','permiso y límite')

body=svg(f'<circle cx="625" cy="290" r="195" fill="none" stroke="{B}" stroke-width="7" data-p="0" data-motion="draw"/><circle cx="1125" cy="290" r="195" fill="none" stroke="{G}" stroke-width="7" data-p="0" data-motion="draw"/>'+line(820,290,930,290,2)+st(625,308,'Hombre',51,F,'middle',0)+st(1125,308,'Mujer',51,F,'middle',0))
body+=text(0,5,'Una ayudante que lo complementa',0,'copy',1768,75)
body+=text(0,560,'Unirse · adherirse, como con pegamento',2,'hand',1768,90)
save(10,body,'Génesis 2 · El matrimonio','Génesis 2:18-25 y notas · La Atalaya, 1 de septiembre de 2009, págs. 13-14','unión gráfica')

body='<div class="phase" data-p="0" data-until-p="2"><div class="atlas"><div class="atlas-art"><!--ATLAS--></div><div class="atlas-key"><div class="eyebrow">Se identifican</div><div class="display">Éufrates y Tigris</div><p>Cursos actuales, sobre cartografía real.</p><p>Hidequel = Tigris</p></div></div></div>'
body+='<div class="phase" data-p="2"><div class="eyebrow">Relación textual · no es un mapa reconstruido</div>'
body+=svg(line(884,110,884,230,2)+line(210,230,1558,230,2))
body+=text(440,45,'Un río que regaba el jardín',2,'display',1110,120).replace('class="display"','class="copy"')
for i,(name,detail) in enumerate([('Pisón','Sin identificar'),('Guihón','Sin identificar'),('Hidequel','Tigris'),('Éufrates','≈ 2.700 km')]):
    x=i*449;body+=node(x,335,420,name,detail,2)+svg(line(x+210,230,x+210,315,2,color=B,dash=i<2))
body+=text(0,610,'Ubicación del jardín: conjetural',2,'hand',1768,100)+'</div>'
save(11,body,'Génesis 2 · Los cuatro ríos','Génesis 2:10-14 y nota · Perspicacia, «Edén», «Pisón», «Guihón», «Éufrates» · Mapa: Natural Earth','mapa y relación textual')

body='<div class="atlas"><div class="atlas-art"><!--ATLAS--></div><div class="atlas-key"><div class="eyebrow">Edén hoy</div><div class="display">Ubicación conjetural</div><p>La zona al sur del lago Van es tradicional.</p><p data-p="1">No es una localización comprobada.</p><p data-p="2">No hay un jardín identificado que se pueda visitar.</p></div></div>'
body+=box(26,632,1250,65,'<span class="tag" style="background:#172c33">Contorno discontinuo: región tradicional, límites imprecisos</span>',None)
save(12,body,'Génesis 2 · El lugar y el presente','Perspicacia, «Edén», pág. 733; «Pisón» · La Atalaya, 15 de enero de 1972, págs. 59-60 · Natural Earth','atlas de incertidumbre')

body=text(0,5,'Un medio de comunicación',0,'display',1750,120)
body+=flow([('Satanás','El responsable'),('Serpiente literal','El medio utilizado'),('Eva','La interlocutora')],[0,0,0],240)
body+=foot('Mecanismo exacto: no especificado',1)
save(13,body,'Génesis 3 · La serpiente','Perspicacia, «Serpiente, culebra», «Eva» · La Atalaya, 1 de septiembre de 1984, pág. 31 · Apocalipsis 12:9','diagrama de responsabilidad')

body='<div class="paper" style="height:625px;padding:34px 42px">'
body+='<div class="duo" style="height:75px"><div class="eyebrow">Jehová · Génesis 2:16, 17</div><div class="eyebrow">Eva · Génesis 3:2, 3</div></div>'
for i,(a,b) in enumerate([('«hasta quedar satisfecho»','Esa expresión no aparece'),('«el árbol del conocimiento de lo bueno y lo malo»','«el árbol que está en medio del jardín»'),('«no debes comer»','«no, no deben tocarlo»')]):
    body+=f'<div class="duo" style="height:150px;border-top:2px solid #afad9e;padding-top:22px" data-p="1"><div class="copy">{a}</div><div class="copy">{b}</div></div>'
body+='</div>'+text(0,645,'Después: «De ningún modo morirán»',3,'hand',1250,70)
save(14,body,'Génesis 3 · El diálogo','Génesis 2:16-17; 3:1-5 · Perspicacia, «Edén» y «Pecado»','cotejo literal',own='Observación propia · cotejo del texto')

body=flow([('Deseo','Eva mira el fruto'),('Acto','Ambos comen'),('Vergüenza','Se cubren y esconden')],[0,0,1],90)
body+=text(0,390,'Jehová pregunta',2,'display gold',800,120)+text(970,390,'Señalan a otros',2,'display',790,150)
body+=text(0,590,'La serpiente recibe la sentencia directamente.',3,'small',1220,70)
body+=box(1160,625,608,60,'<span class="tag">Observación propia · el contraste</span>',3)
save(15,body,'Génesis 3 · Decisiones y respuestas','Génesis 3:6-14 · Perspicacia, «Adán», «Pecado» · ¡Despertad!, 8 de septiembre de 1998, pág. 26','cadena de decisiones')

body=phases([(0,'Serpiente','Arrastrarse y comer polvo: humillación.','No se describe un cambio anatómico.'),(1,'Mujer','Dolor al dar a luz y deterioro de la relación.','Endíadis: dos términos expresan una idea.'),(2,'Adán y el suelo','Sustento con esfuerzo doloroso y retorno al polvo.','El trabajo ya existía antes del pecado.')])
save(16,body,'Génesis 3 · Las sentencias','Génesis 3:14-19 · Perspicacia, «Serpiente», «Dolores de parto» · La Atalaya, 15 de octubre de 1980, pág. 27','tres consecuencias por fases')

body=text(0,0,'930',0,'display gold',740,235).replace('height:235px','height:235px;font-size:220px')+text(760,85,'años de vida',0,'display',970,130)
body+=svg(line(40,335,1730,335,0)+circle(40,335,11,p=0)+circle(1730,335,11,p=0)+st(40,398,'Perdió la perfección',32,B,p=0)+st(1730,398,'Volvió al polvo',32,B,'end',1))
body+=node(0,480,800,'Condición heredada','Vida afectada por pecado y muerte',2)+node(960,480,808,'Jesucristo','El último Adán',3)
save(17,body,'Génesis 3 · Muerte y descendencia','Perspicacia, «Adán», «Vida», «Pecado» · La Atalaya 2019, núm. 3, pág. 9; mayo de 1976, pág. 280','duración y transmisión')

body=node(0,0,765,'La serpiente','Satanás',1)+node(1000,0,765,'La mujer','La parte celestial de la organización de Jehová',1)
body+=svg(line(382,210,382,335,1,color=B)+line(1382,210,1382,335,2,color=G)+line(805,390,955,390,2))
body+=node(0,350,765,'Su descendencia','Quienes se oponen a Jehová',1)+node(1000,350,765,'Su descendencia','Jesucristo y los 144.000',2)
body+=foot('Talón · daño temporal        Cabeza · destrucción definitiva',3)
save(18,body,'Génesis 3:15 · La primera profecía','La Atalaya, julio de 2022, párrs. 4-12 · Génesis 3:15 y notas','cuatro participantes')

body=''
for row,items in enumerate([[('Abrahán','La promesa',0),('Judá','La línea',0),('Jesús','Parte principal',1)],[('33','Muerte y resurrección',1),('Pentecostés','Cristianos ungidos',2),('1914','Rey mesiánico',2)]]):
    for i,(name,detail,p) in enumerate(items):
        x=i*595;y=row*260;body+=node(x,y,550,name,detail,p)
        if i<2:body+=svg(line(x+555,y+90,x+581,y+90,p))
body+=foot('Desenlace: acabar con Satanás · fin del Reinado de Mil Años',3)
save(19,body,'Génesis 3:15 · Desarrollo de la promesa','La Atalaya, julio de 2022, párrs. 8-15 · Referencias marginales de Génesis 3:15','secuencia en dos franjas')

body=flow([('Eva','Viviente'),('Ropa','Bondad inmerecida'),('Acceso cerrado','Árbol de la vida')],[0,1,1],170)
body+=text(0,15,'Un nombre, una provisión y una salida',0,'copy',1700,100)
body+=text(0,455,'Querubín',2,'display gold',680,130)+text(720,460,'Ángel de alto rango con tareas especiales',2,'copy',1020,180)
body+=text(0,628,'Árbol de la vida · garantía concedida por Dios',2,'hand',1768,80)
save(20,body,'Génesis 3 · Versículos 20 al 24','Génesis 3:20-24 · Perspicacia, «Eva», «Vida», «Querubín» · Glosario de la TNM','secuencia de cierre',own='Observación propia · orden del nombre y la sentencia')

for n,title in [(21,'Dos personas y sus ofrendas'),(22,'La motivación de la fe')]:
    body='<div class="photo-pair"><div class="portrait"><img src="assets/cain.jpg" alt="Caín junto a su ofrenda, ilustración JW"/><div class="label">Caín</div></div><div class="portrait"><img src="assets/abel.jpg" alt="Abel junto a su ofrenda, ilustración JW"/><div class="label">Abel</div></div></div>'
    if n==21:body+=text(0,605,'Agricultor · productos de la tierra',1,'small',860,100)+text(905,605,'Pastor · primogénitos del rebaño',1,'small gold',860,100)
    else:body+=text(0,604,'Persona → motivos → ofrenda',1,'display gold',1768,130).replace('class="display gold"','class="copy gold"')+text(0,672,'Primogénitos = primeras crías',2,'small',1400,50)
    save(n,body,'Génesis 4 · Las ofrendas','«Dios aprobó sus ofrendas», págs. 16-19, párrs. 4-12 · Perspicacia, «Caín», pág. 387 · Hebreos 11:4','ilustración comparada',title=title)

body=node(0,245,540,'Enojo','Se le ve en el rostro',0)
body+=svg(line(560,335,845,335,1)+line(845,335,1100,125,1,color=B)+line(845,335,1100,545,1,color=G))
body+=node(1150,20,615,'Cambiar','Recuperar la aprobación',1)+node(1150,460,615,'Dejarse dominar','Ignorar la advertencia',1)
body+=text(590,250,'Una decisión',1,'hand',520,70)+text(0,640,'Jehová le habló antes del crimen.',2,'copy',1050,80)
save(23,body,'Génesis 4:6, 7 · La advertencia','La Atalaya, 1 de febrero de 1999, pág. 23 · Génesis 4:6, 7','bifurcación moral')

body=text(0,40,'«¿Dónde está tu hermano Abel?»',1,'quote',1768,200)
body+=flow([('Caín','Respuesta mentirosa'),('El suelo','Testimonio de la vida derramada'),('Sentencia','Fugitivo; cultivo sin fruto')],[1,2,2],325)
body+=text(0,620,'Hebreos 12:24 · justicia y misericordia',2,'hand',1768,80)
save(24,body,'Génesis 4 · El asesinato y la sentencia','Génesis 4:8-12 · Perspicacia, «Caín», pág. 387; «Abel», pág. 17','pregunta y consecuencias')

body=node(0,0,830,'Una señal para Caín','Probablemente un decreto conocido',1)+node(940,0,828,'Nod','Región del Destierro',2)
body+=svg(line(950,350,1570,350,2)+st(1730,363,'ESTE',42,G,'end',2))
body+=text(0,280,'No se describe una marca en la piel.',0,'copy',780,180)+text(940,440,'Ubicación desconocida',2,'display gold',800,190)
body+=foot('Una dirección respecto a Edén no equivale a una ruta localizable.',2)
save(25,body,'Génesis 4 · Señal y destierro','Génesis 4:15, 16 y nota · Perspicacia, «Caín», pág. 387; «Condición de fugitivo, Tierra de la», pág. 521','decreto y orientación')

body=node(515,0,740,'Adán y Eva','Hijos e hijas',0)+svg(line(885,190,885,260,0)+line(350,260,1410,260,0)+line(350,260,350,335,0)+line(1410,260,1410,335,0))
body+=node(0,355,725,'Caín','Hijo de la primera pareja',0)+node(1040,355,725,'Su esposa','Hermana u otra pariente cercana',0)
body+=text(0,630,'La prohibición de la Ley mosaica llegó siglos después.',2,'hand',1768,90)
save(26,body,'Génesis 4 · La familia de Caín','jw.org, «¿Quién fue la esposa de Caín?» · La Atalaya, 1 de septiembre de 2010, pág. 25','árbol familiar abierto')

body=text(0,0,'Enoc',0,'display gold',700,150)+text(830,30,'Primera ciudad mencionada',0,'copy',900,100)
body+=flow([('Jabal','Tiendas y ganado'),('Jubal','Arpa y flauta'),('Tubal-Caín','Herramientas de metal')],[1,1,1],235)
body+=text(0,490,'Metalurgia · trabajar metales para hacer objetos',1,'hand',1700,80)
body+=foot('Dos Enoc distintos: hijo de Caín / hijo de Jared',2)
save(27,body,'Génesis 4 · Una civilización','Génesis 4:17-22 · Perspicacia, «Caín», «Enoc», «Jabal»','oficios y genealogía')

body=node(0,0,660,'Adá','Una esposa',0)+node(1105,0,660,'Zilá','Otra esposa',0)+svg(line(680,90,1080,90,0))
body+=text(690,36,'Lamec',0,'display gold',520,120).replace('class="display gold"','class="copy gold"')
body+=text(0,245,'Poligamia · dos esposas al mismo tiempo',0,'copy',1768,90)
body+=text(0,385,'7',2,'display blue',530,215).replace('height:215px','height:215px;font-size:185px')+text(1000,385,'77',2,'display gold',700,215).replace('height:215px','height:215px;font-size:185px')+svg(line(425,485,900,485,2))
body+=text(0,637,'Protección que Lamec reclamaba, no una concesión de Jehová.',2,'small',1768,80)
save(28,body,'Génesis 4 · Lamec','Génesis 4:19, 23, 24 · Perspicacia, «Lamec», pág. 183 · ¡Despertad!, 8 de marzo de 1985, pág. 11','comparación de reclamaciones')

body=flow([('Set','Nombrado; puesto'),('Enós','Hijo de Set'),('Noé → Jesús','La línea continúa')],[0,1,0],15)
body+=text(0,300,'«invocar el nombre de Jehová»',1,'quote',1768,155)
body+=node(0,485,820,'Lectura discutida','Adoración pública',2)+node(950,485,818,'Explicación seguida','Al parecer, uso irreverente',2)
save(29,body,'Génesis 4 · Set y Enós','Génesis 4:25, 26 · Perspicacia, «Set», pág. 1014 · Paraíso restaurado, págs. 67-68 · wcg (2025), pág. 16','sucesión y lectura del texto')

body='';s='';xmin=4026;xmax=2850;scale=1450/(xmin-xmax)
for i,(name,born,died,years,p) in enumerate([('Adán',4026,3096,930,0),('Set',3896,2984,912,1),('Enós',3791,2886,905,1)]):
    y=110+i*157;x=240+(4026-born)*scale;width=(born-died)*scale
    s+=st(0,y+38,name,42,F,p=p)+f'<rect x="{x}" y="{y}" width="{width}" height="66" rx="4" fill="{G if i==0 else B}" data-p="{p}" data-motion="bar"/>'+st(x,y+115,f'{born} a {died} a. e. c. · {years} años',28,F,p=p)
s+=line(240,645,1690,645,0,color=M)
for year in [4000,3500,3000]:
    x=240+(4026-year)*scale;s+=line(x,632,x,658,0,color=M)+st(x,704,str(year),28,F,'middle',0)
body+=svg(s)
save(30,body,'Cronología · Tres vidas','Génesis 5:3-11 · Perspicacia, «Adán», «Set», «Vida», «Cronología»','barras temporales a escala',own='Cálculo propio · fechas de Enós a partir de Génesis 5')

body=flow([('Ángeles','Se materializan'),('Mujeres','Tienen hijos'),('Nefilim','Derribadores')],[0,0,1],120)
body+=text(0,415,'El nombre no significa por sí solo «gigantes».',1,'copy',1768,100)
body+=foot('La investigación los describe como intimidadores y tiranos.',2)
save(31,body,'Preguntas complementarias · Génesis 6','Génesis 6:2, 4 y notas · Perspicacia, «Nefilim»','diagrama sin reconstrucción física')

s=f'<path d="M100,265 L1330,265 L1500,155 L270,155 Z" fill="#8f7956" stroke="{G}" stroke-width="5" data-p="0"/><path d="M100,265 L1330,265 L1330,535 L100,535 Z" fill="#61523e" stroke="{G}" stroke-width="5" data-p="0"/><path d="M1330,265 L1500,155 L1500,425 L1330,535 Z" fill="#4b4336" stroke="{G}" stroke-width="5" data-p="0"/>'
s+=line(100,355,1330,355,1)+line(100,445,1330,445,1)+line(100,595,1330,595,1)+st(710,649,'≈ 134 m de largo',45,G,'middle',1)+st(1520,330,'≈ 13,5 m',32,G,p=1)+st(1540,180,'≈ 22,5 m',30,G,'end',1)
body=svg(s)+text(0,0,'Hermético y capaz de flotar',0,'copy',1768,100)+text(0,685,'Tres cubiertas · volumen y superficie son medidas distintas',2,'small',1768,60)
save(32,body,'Preguntas complementarias · El arca','Génesis 6:14-16 y notas · Perspicacia, «Arca» · Dimensiones aproximadas publicadas','cofre en corte')

body=text(0,15,'40 o 50 años',0,'display gold',1768,130)+text(0,155,'Construcción probable · la Biblia no fija el plazo',0,'copy',1768,110)
body+=svg(rect(0,335,1720,65,'#2b4b55',M,1)+f'<rect x="0" y="335" width="186" height="65" fill="{G}" data-p="1" data-motion="bar"/>'+st(0,463,'40 días de lluvia',35,G,p=1)+st(1720,530,'370 días y parte del 371 en el arca',41,F,'end',1))
body+=text(0,610,'Agua de abajo y de arriba · mecanismo físico no especificado',2,'small blue',1768,95)
save(33,body,'Preguntas complementarias · Los tiempos','Génesis 6:3; 7:11, 12; 8:13, 14 · Perspicacia, «Diluvio», «Noé» · jw.org, «El Diluvio de Noé»','barras de lluvia y estancia')

body='<div class="phase" data-p="0" data-until-p="2"><div class="atlas"><div class="atlas-art"><!--ATLAS--></div><div class="atlas-key"><div class="display">Montañas de Ararat</div><p>Región, no una cumbre identificada.</p><p data-p="1">Restos del arca: sin confirmación.</p></div></div></div>'
body+='<div class="phase" data-p="2">'+text(0,0,'El arcoíris',None,'display gold',1768,130)
arcs=''
for j,color in enumerate(['#efbe66','#d28b75','#acd6d2']):
    r=330-j*35;arcs+=f'<path d="M{884-r},555 A{r},{r} 0 0 1 {884+r},555" stroke="{color}" stroke-width="23" fill="none" data-p="2" data-motion="draw"/>'
body+=svg(arcs)+text(0,600,'Señal del pacto · Génesis 9:13',2,'copy',1768,95)+'</div>'
save(34,body,'Preguntas complementarias · Límites y certeza','Génesis 8:4; 9:13 · Perspicacia, «Ararat», «Arca», «Arco iris», «Diluvio» · Natural Earth','mapa y señal')

body=text(0,0,'La palabra · lo bueno y lo malo',0,'display gold',1768,130).replace('class="display gold"','class="copy gold"')
body+=flow([('Génesis 2','Del suelo sale el hombre'),('Génesis 3','El suelo queda maldito'),('Génesis 4','Recibe la sangre; deja de dar fruto')],[1,1,1],230)
body+=text(0,565,'La descendencia · promesa → Set → Noé → Jesús',2,'hand',1768,110)
save(35,body,'Los hilos · Una sola historia','Génesis 1:3; 2:7, 17; 3:15, 17-19; 4:10, 12, 25 · Investigación, «Relaciones»','hilos narrativos',own='Observación propia · relaciones entre los capítulos')

save(36,phases([(0,'Una etapa terminada','Escoger algo pendiente y completar una etapa.','¿Qué vamos a terminar esta semana?'),(2,'Cuidar el lugar donde vivimos','Reparar, sembrar o limpiar un espacio compartido.','¿Qué cuidado concreto se va a notar?')]),'Lecciones y preguntas · Génesis 1','Génesis 1:4, 10, 12, 18, 21, 25, 28 · Investigación, «Qué nos llevamos a casa»','lecciones por fases')
save(37,phases([(0,'Una unión firme','Tomar una decisión pensando como un equipo.','¿Cómo podemos favorecer nuestra unidad?'),(2,'La norma completa','Explicar el permiso, el límite y su motivo.','¿Transmitimos también el cuidado que hay detrás?')]),'Lecciones y preguntas · Génesis 2','Génesis 2:16, 17, 24 y nota · Investigación, «Qué nos llevamos a casa»','lecciones por fases')
save(38,phases([(0,'Reconocer el engaño','Observar qué está debilitando la confianza en Jehová.','¿Qué efecto está teniendo en nosotros?'),(2,'Asumir la responsabilidad','Reconocer lo que hicimos antes de buscar una excusa.','¿Qué nos cuesta admitir?'),(3,'Corregir con cariño','Dejar claro el afecto y la posibilidad de avanzar.','¿Cómo se notará en nuestra conversación?')]),'Lecciones y preguntas · Génesis 3','Génesis 3:1-5, 12, 13, 15, 21 · Investigación, «Qué nos llevamos a casa»','lecciones por fases')
save(39,phases([(0,'Hablar a tiempo','Escuchar el disgusto antes de que crezca.','¿Estamos dejando algo en silencio?'),(2,'Mirar la motivación','Interesarse por el ánimo, además de la cantidad.','¿Qué había en el corazón al hacerlo?'),(3,'Corregir con confianza','Preguntar y mostrar que cambiar es posible.','¿Nuestra manera de hablar lo comunica?')]),'Lecciones y preguntas · Génesis 4','Génesis 4:4-7 · La Atalaya, 1 de febrero de 1999, págs. 22-23','lecciones por fases')
save(40,phases([(0,'Escuchar primero','Jehová preguntó antes de corregir.','¿Qué cambiaría en nuestra casa?'),(1,'Aceptar lo que no sabemos','La fuente distingue certeza e incertidumbre.','¿Cómo nos sentimos cuando no hay una respuesta?'),(2,'Decidir personalmente','Caín y Abel tuvieron un mismo punto de partida.','¿Qué decisiones están formando nuestro corazón?')]),'Conversación en familia','Investigación, «Tres preguntas para la mesa» · Génesis 3:9; 4:4-9','preguntas por turnos')
body=text(0,40,'Una creación buena',0,'display',1768,140)+text(0,240,'Decisiones que importan',0,'display',1768,140)+text(0,440,'Una promesa que sigue',0,'display gold',1768,140)
body+=text(0,640,'Génesis 1 al 4 · Lectura en familia',0,'hand',1768,85)
save(41,body,'Lectura familiar','Génesis 1:31; 3:15 · Traducción del Nuevo Mundo, edición de estudio','cierre de tres ideas')
(OUT/'contenido.json').write_text(json.dumps(C,ensure_ascii=False,indent=2))
print(f'{len(C)} fuentes de escena escritas')
