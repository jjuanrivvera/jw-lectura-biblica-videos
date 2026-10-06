# Guion: Génesis 10 al 13

Fuente única: `fuente/investigacion.html` ("Génesis 10 al 13: investigación para la lectura familiar"). Todo dato, cita y
cifra sale de ahí; los versículos, de la TNM de 2019 tal como los copia la investigación (comprobados con `jwlib
versiculo`, en `trabajo/tnm-10.txt` a `tnm-13.txt`). En pantalla se escribe **Sarái**, como la TNM de 2019 (la
investigación escribe "Sarai" en su prosa y avisa de la grafía de la TNM).

Reglas que aplica este guion:

- Lo que la investigación marca como observación propia o cálculo propio va rotulado así en pantalla (recuadro azul
  punteado, "observación propia", "cálculo propio"); la voz lo dice sin avisarlo (Juan, 25-sep).
- La voz enseña con seguridad lo que dicen la Biblia y las publicaciones; la fuente va al pie de cada bloque. La voz
  nombra una sola publicación en todo el video como mucho (Juan, 27-sep). La duda solo donde de verdad no se sabe
  (Akkad y Calné, las medidas de la torre, la ciudad de Egipto, el sitio de Hai, dónde estaba Sodoma), una vez y breve.
- Nada de frases de conclusión dentro de la explicación: los "Para la familia", los "Para nosotros" y las frases de las
  publicaciones que ya son consejo se pasaron a la sección final de lecciones (regla 3).
- Sin imágenes generadas. Personas: solo las de las ilustraciones de la JW; los dibujos propios son esquemas, objetos
  y mapas.

## Qué dicen los capítulos

- **Génesis 10.** La tabla de las naciones: de Sem, Cam y Jafet salen setenta familias (14, 30 y 26), "por familias y
  lenguas". Canaán y su territorio. Nemrod, bisnieto de Noé, "poderoso cazador en oposición a Jehová", funda el primer
  reino: Babel, Erec, Akkad y Calné en Sinar; Nínive, Rehobot-Ir, Cálah y Resen en Asiria. Péleg, "división".
- **Génesis 11.** Un solo idioma; la llanura de Sinar; ladrillos cocidos y betún; la ciudad y la torre "para hacerse
  famosos" y no dispersarse; Jehová confunde el idioma; Babel, "confusión". La historia de Sem: diez generaciones hasta
  Abrán, con la vida que se acorta. La historia de Taré: su familia sale de Ur hacia Canaán y se queda en Harán.
- **Génesis 12.** "Sal de tu país". La promesa (nación, bendición, nombre, "todas las familias de la tierra"). El pacto
  entra en vigor al cruzar el Éufrates (1943 a. e. c.). Siquem y "tu descendencia"; el altar; Betel y Hai; el Négueb.
  El hambre, Egipto, "diles que eres mi hermana", el faraón castigado.
- **Génesis 13.** De vuelta al altar entre Betel y Hai. La pelea de los pastores; "Por favor, somos hermanos"; Lot
  escoge el distrito del Jordán y acaba junto a Sodoma. "Levanta la vista": toda la tierra y una descendencia como el
  polvo. Abrán se instala en Hebrón, junto a Mamré, y levanta otro altar.

## Estructura (reglas 2 y 3)

57 escenas (00 a 56), 28:44 en total: 27:03 de voz más los silencios de entrada y salida de cada escena.

1. **Arranque directo** (00): "Vamos a analizar Génesis diez al trece. Estos capítulos cuentan...", una frase por
   capítulo, cada una encendiendo su lugar en el mapa B2. Sin pregunta gancho.
2. **Contexto** (01, 02): las tres "historias" (toledot) que dividen el tramo y la línea de tiempo de 427 años, del
   Diluvio al cruce del Éufrates.
3. **Los cuatro capítulos seguidos** (03 a 50), en el orden del texto, cada uno con su tarjeta y la pista 10 11 12 13.
   Las escenas "hoy" van donde el relato pasa por el lugar: las ciudades de Nemrod (11), Babilonia (17), Ur (31), Betel
   y Hai (39), Sodoma (47) y Hebrón (50).
4. **Cómo se amarran los capítulos** (51): tres capítulos que parecen sueltos y un hilo que los cose, con tres
   parejas de textos: dos maneras de conseguir un nombre (11:4 y 12:2), quedarse contra la orden y salir por la orden
   (11:4, 8 y 12:1, 4), y dos hombres que levantan la vista (13:10 y 13:14). La investigación dice que ninguna
   publicación consultada pone esas parejas juntas, así que la pantalla las rotula como observación propia. Son lectura
   del texto, no lecciones, y van antes de ellas. Los demás hilos se cuentan en su sitio para no repetirlos: Péleg (04);
   Babel, Babilonia la Grande, Pentecostés y el idioma puro (20); Edén, Abrán y Cristo (36); la frontera de Canaán de
   10:19 (08); un altar en cada parada (38, 43, 49 y la lección de Génesis 12). La unión de la maldición de Canaán con
   la promesa de la tierra quedó fuera al recortar la narración a unos 27 minutos de voz.
5. **Una sola sección de lecciones al final** (52 a 55): portada y una escena por capítulo, tres lecciones cada una con
   su pregunta para pensar (las doce de la investigación). Cierre (56) con Génesis 12:1, la cita que abre la
   investigación, y Hebreos 11:10.

## Material por capítulo y por qué (regla 5)

No hay plantilla: cada capítulo tiene su material. Los mapas solo van donde el capítulo trata de lugares o de un
desplazamiento, y siempre sobre un mapa real de la JW, con su fuente al pie y "marcas añadidas". Tres mapas reales:

- **Apéndice B2 de la TNM**, "Génesis y los viajes de los patriarcas", en vector (el SVG de wol.jw.org de los videos
  anteriores, `mapas/b2.svg`). Es el único mapa de la JW que tiene a la vez Babel (Babilonia), Erec, Sinar, Asiria,
  Nínive, Cálah, Ur, Caldea, Harán, Carquemis, Damasco, Siquem, Betel, Hebrón, el Négueb, Gaza, Guerar, Sidón y Egipto;
  y su recuadro trae Betel y Hai, Mamré, Hebrón, el Jordán, el mar Salado, Zóar y "Sodoma, Gomorra, Admá, Zeboyim (?)".
  Con `rsvg-convert` sale nítido a cualquier escala. Sirve para cuatro de los cinco desplazamientos del tramo.
- **"El origen de las naciones"**, *Perspicacia*, vol. 1, pág. 329 (jwlib, docid 1200000759): el mapa de la JW con las
  tres flechas de Jafet, Cam y Sem. Es la figura de la investigación para Génesis 10, y encima se ponen, pueblo por
  pueblo, los puntos del mapa propio de la investigación (lleno, hueco o punteado según la certeza que da
  *Perspicacia*), georreferenciados sobre el mapa de la JW en vez de sobre costas esquemáticas.
- **"El mundo de los patriarcas"**, *Veamos "la buena tierra"*, págs. 6, 7 (jwlib, docid 1102003104): la ruta de
  Abrahán en rojo trazada por la propia JW. No se muestra entero (la investigación ya lo usaba con rótulos encima), pero
  la ruta que se dibuja sobre el B2 copia su trazado: Ur, Éufrates arriba, Harán, Damasco, Siquem, Betel, Hebrón,
  Beer-seba y Egipto.

### Apertura y contexto
- **Mapa de los cuatro capítulos** (00), sobre el B2 entero: 10 en Sinar y Asiria (Nemrod), 11 en Babel y en el camino
  de Ur a Harán, 12 de Harán a Canaán y a Egipto, 13 en Betel y Hebrón. La cámara hace el recorrido del relato.
- **Tres historias cosidas** (01): los tres "Esta es la historia de" (10:1; 11:10; 11:27) como tres documentos sobre la
  franja de los capítulos, con la palabra toledot explicada. Es la manera más clara de ver que el tramo tiene costuras.
- **Unos cuatrocientos treinta años** (02): la línea de tiempo de la investigación a todo el ancho, con el cursor que
  avanza de 2370 a 1943 y la franja de Péleg, en la que ocurrió Babel sin fecha.

### Génesis 10: la tabla de las naciones
Es una lista de nombres y de lugares: lo que la explica es un árbol (quién sale de quién, cuántos) y un mapa (adónde
fueron). Lo que no es obvio: qué cuenta la tabla (familias, no personas), por qué ya habla de lenguas si Babel viene
después, qué significa Péleg, qué quiere decir "en oposición a", qué era el sistema patriarcal y dónde están hoy las
ciudades de Nemrod.
- **Árbol de las setenta familias** (03), con contadores 14, 30 y 26: dibujo propio, porque la tabla es una genealogía.
- **El orden de los capítulos** (04): un esquema de "el mapa" (capítulo 10) y "cómo se llegó a él" (capítulo 11)
  cosidos por Péleg. Los continentes tachados: lo que se dividió fue la gente.
- **Las tres ramas** (05, 06, 07) sobre el mapa de *Perspicacia*, una rama por escena, con la leyenda de certeza. Así se
  ve cada nombre en su lugar sin amontonar setenta rótulos.
- **La tierra de Canaán** (08), sobre el B2: la frontera de 10:19 se traza de Sidón a Gaza y Guerar y hasta el mar
  Salado, con Sodoma y Gomorra marcadas con "(?)" como las marca el propio B2. En la misma escena, Cus y Put en África,
  para deshacer la idea de la maldición y la raza negra.
- **Nemrod** (09): árbol Cam, Cus, Nemrod y el contador de 70 que no lo incluye; la palabra lif·néh explicada.
- **El primer reino** (10), sobre el B2: las ciudades de Sinar y las de Asiria, con las cuatro que no tienen sitio en
  una lista aparte y el paso de Nemrod al territorio de Asur, hijo de Sem.
- **Las ciudades de Nemrod hoy** (11): el mismo mapa con los nombres de hoy (Babilonia junto a Hilla, Warka, los
  montículos frente a Mosul, Nimrud).

### Génesis 11: una torre, muchas lenguas y diez generaciones
Tiene un lugar (Babel en la llanura de Sinar), un objeto (la torre) y una lista de edades. Lo que no es obvio: qué es
Sinar, cómo se hacían ladrillos sin piedra, qué es el betún, qué era un zigurat, cuánto medían las torres conocidas, qué
significa "bajó para ver", cómo fue la confusión, por qué la vida se acorta y cómo se hace la cuenta de los años.
- **Sinar en el B2** (12): la llanura entre el Tigris y el Éufrates, con Babel.
- **Ladrillos y betún** (13): dibujo del barro, el molde, el horno y el muro con la mezcla negra, y las tres palabras
  hebreas (pez, betún, alquitrán) como tarjetas.
- **La torre** (14): la ilustración de *Mi libro de historias bíblicas*, historia 12, que es la de la investigación.
- **El zigurat** (15): la foto del zigurat de Ur de *Perspicacia* ("La torre que se erigió en Babel se parecía a este
  zigurat religioso"), mejor que un dibujo propio de un edificio antiguo.
- **La torre a escala** (16): la figura de la investigación rehecha a todo el ancho (Ur, Borsipa, diez pisos,
  Etemenanki y la de Babel punteada con "?"), con la persona de 1,70 m.
- **Babel hoy** (17): la foto de las ruinas de Babilonia de *Perspicacia*, "El Imperio babilonio".
- **"Bajemos" y la confusión** (18, 19): tarjetas de la nota de 11:5 y del plural de 11:7 y 1:26; el ejemplo de la araña
  de *La Atalaya* como dos globos de diálogo con una rosa de los vientos; la ilustración de *Lecciones que aprendo de la
  Biblia*, lección 7, con la obra parada.
- **De Babel a Pentecostés** (20): un esquema de tres pasos (Babel dispersa, Pentecostés reúne, el idioma puro une) y la
  línea Babel, Babilonia, Babilonia la Grande.
- **Una sola familia** (21): los setenta puntos del mapa de las naciones que vuelven a un solo tronco.
- **La vida que se acorta** (22): las veinte barras de la investigación (Adán a Abrahán) a todo el ancho, con la franja
  del Salmo 90:10 y los dos escalones marcados.
- **La cuenta** (23) y **¿setenta o ciento treinta?** (24): la suma que se escribe en la pizarra y la vida de Taré en
  una regla, porque se entienden haciendo la cuenta.
- **Vidas que se cruzan** (25): la figura de las once vidas encimadas, con el cálculo propio de Éber rotulado.
- **La familia de Taré** (26): árbol con Harán muerto en Ur, Lot huérfano y Sarái estéril.
- **De Ur a Harán** (27), sobre el B2: el viaje Éufrates arriba, con el contador de 960 km.

### Génesis 12: "Sal de tu país"
Es un capítulo de viaje, con una ciudad de partida, un pacto con fecha y una bajada a Egipto. Lo que no es obvio: cómo
era Ur, qué es un pacto, qué es Nisán, qué quiere decir "descendencia", qué eran Siquem, Betel, Hai y el Négueb, y por
qué Abrán dijo "mi hermana".
- **Abrán en Ur** (28, 29): ilustraciones de *Imitemos su fe*, cap. 3, en su versión limpia de jwlib (la investigación
  usaba una con rótulos añadidos): Abrán ante el zigurat y la salida de Ur.
- **Una casa de Ur** (30): planta dibujada (patio empedrado con desagüe, trece habitaciones, escalera al segundo piso),
  porque las cifras de Woolley solo se entienden viendo la casa.
- **Ur hoy** (31): esquema de las ruinas con el río de entonces junto a la muralla y el de hoy a 16 km, que explica
  "del otro lado del Río" (Josué 24:3).
- **La promesa y el pacto** (32, 33): cuatro tarjetas y una línea de tiempo de 1943 a 1513 y al año 33.
- **De Harán a Canaán** (34), sobre el B2, con las fotos de *Perspicacia* del Éufrates cerca de Carquemis y la
  caravana de *Lecciones que aprendo de la Biblia*, lección 8. Los tramos sin cifra publicada, rotulados como cálculo
  propio.
- **Siquem** (35): la foto de *Perspicacia* de los montes Guerizim y Ebal sobre Siquem, cuyo pie dice que en ese valle
  se hizo la promesa de 12:7.
- **Tu descendencia** (36): la cadena Génesis 3:15, 12:7, Gálatas 3:16 y 3:29, con la palabra zé·raʽ.
- **Betel y Hai** (38, 39), sobre el recuadro del B2 y con la foto de las ruinas de Betel de *Perspicacia*.
- **Egipto** (40 a 42): el B2 del Négueb al delta, con la ciudad de destino sin marcar porque no se sabe; la foto del
  Négueb de *Perspicacia*; un árbol de "hijos del mismo padre, de distintas madres"; la ilustración de Sarái en el
  palacio de *La Atalaya* núm. 3 de 2017.

### Génesis 13: "Somos hermanos"
Es un capítulo de lugares vistos desde un sitio alto: Betel, el valle del Jordán, Sodoma y Hebrón. Lo que no es obvio:
por qué "subió al Négueb" es ir al norte, qué es el kik·kár, dónde estaba Sodoma, qué costumbre puede haber detrás de
"levanta la vista" y "recorre la tierra", y cómo es Hebrón.
- **El regreso** (43): el recuadro del B2 con la ruta que sube del Négueb a Betel, la cámara siguiéndola y una flecha
  del norte; después, los 318 hombres de 14:14 como puntos que llegan a más de mil, y la vuelta al mismo altar.
- **Abrán y Lot** (44): la ilustración de *La Atalaya* de mayo de 2016, "Resolvamos los desacuerdos con amor", limpia.
- **Lo que vio Lot** (45): el recuadro del B2 desde Betel hacia el este: la vista de Lot como un cono, el kik·kár
  dibujado como una cuenca y rotulado "zona aproximada" (ningún mapa de la JW lo marca), Zóar, y los pasos de Lot de
  "cerca de Sodoma" (13:12) a "en Sodoma" (14:12).
- **¿Era Lot mala persona?** (46): dos tarjetas enfrentadas, "justo" (2 Pedro 2:7) y "pero escogió mal" (*La Atalaya*
  2001), y el rescate sin rencor. Es un juicio sobre una persona, así que va con texto y fuentes, sin imagen.
- **¿Dónde estaba Sodoma?** (47): la foto del mar Salado de *Perspicacia* y el "(?)" del mapa, con las dos opiniones
  (bajo el agua; al este y al sureste) marcadas como preguntas, sin elegir ninguna.
- **"Levanta la vista"** (48): el mismo mapa con los cuatro puntos cardinales que salen de Betel, el polvo como puntos,
  la tierra recorrida a lo largo y a lo ancho, y la costumbre legal de "la veo" con su "hay doctos que opinan".
- **Hebrón** (49, 50): el recuadro del B2 para Mamré y Hebrón, y las fotos de *Perspicacia*: "Hebrón en la actualidad"
  y una calle de Hebrón.

## Escenas

| N.º | Escena | Material |
|---|---|---|
| 00 | Apertura | B2 entero, un capítulo por lugar |
| 01 | Tres historias | los tres "Esta es la historia de" sobre la franja de capítulos |
| 02 | Unos cuatrocientos treinta años | línea de tiempo 2370-1943 |
| 03 | Setenta familias | tarjeta de Génesis 10; árbol con 14, 30 y 26 |
| 04 | Por familias y lenguas | el capítulo 10 y el 11 cosidos por Péleg |
| 05 | Jafet | mapa de *Perspicacia*, puntos azules |
| 06 | Cam | mapa de *Perspicacia*, puntos rojos |
| 07 | Sem | mapa de *Perspicacia*, puntos verdes y las setenta juntas |
| 08 | La tierra de Canaán | B2, la frontera de 10:19; Cus y Put |
| 09 | Nemrod | árbol y contador; lif·néh |
| 10 | El primer reino | B2, Sinar y Asiria |
| 11 | Las ciudades de Nemrod hoy | B2 con los nombres de hoy |
| 12 | Un solo idioma | tarjeta de Génesis 11; Sinar en el B2 |
| 13 | Ladrillos y betún | dibujo: barro, molde, horno, muro |
| 14 | "Así nos haremos famosos" | ilustración de la torre |
| 15 | Un zigurat | foto del zigurat de Ur |
| 16 | La torre, a escala | perfiles a escala |
| 17 | Babel hoy | foto de las ruinas de Babilonia |
| 18 | "Jehová bajó para ver" | tarjetas de 11:5-7 y 1:26 |
| 19 | "Confundamos su idioma" | ilustración de la obra parada; la araña |
| 20 | De Babel a Pentecostés | Babel, Pentecostés, idioma puro; Babilonia la Grande |
| 21 | Una sola familia | los setenta puntos vuelven al tronco |
| 22 | La vida se acorta | veinte barras |
| 23 | La cuenta | la suma de Génesis 11 |
| 24 | ¿Setenta o ciento treinta? | la vida de Taré en una regla |
| 25 | Vidas que se cruzan | once vidas encimadas |
| 26 | La familia de Taré | árbol |
| 27 | De Ur a Harán | B2, ruta Éufrates arriba |
| 28 | "Sal de tu país" | tarjeta de Génesis 12; salida de Ur |
| 29 | Ur | Abrán ante el zigurat; cifras de Ur |
| 30 | Una casa en Ur | planta dibujada |
| 31 | Ur hoy | esquema de las ruinas y el río |
| 32 | La promesa | cuatro tarjetas |
| 33 | El pacto y su fecha | línea 1943, 1513, 33 |
| 34 | De Harán a Canaán | B2, ruta; foto del Éufrates; caravana |
| 35 | Siquem | foto de Guerizim y Ebal |
| 36 | Tu descendencia | cadena de textos; zé·raʽ |
| 37 | ¿En qué idioma? | globos y el acadio |
| 38 | Entre Betel y Hai | recuadro del B2 |
| 39 | Betel y Hai hoy | foto de las ruinas de Betel |
| 40 | Hambre | B2 del Négueb a Egipto; foto del Négueb |
| 41 | ¿Mintió Abrán? | árbol de la media hermana |
| 42 | En la casa del faraón | ilustración de Sarái en el palacio |
| 43 | De vuelta al altar | tarjeta de Génesis 13; subir al Négueb; 318 |
| 44 | "Somos hermanos" | ilustración de Abrán y Lot |
| 45 | Lo que vio Lot | recuadro del B2, el kik·kár |
| 46 | ¿Era Lot mala persona? | 2 Pedro 2:7, 8 |
| 47 | ¿Dónde estaba Sodoma? | foto del mar Salado; "(?)" |
| 48 | "Levanta la vista" | los cuatro puntos cardinales sobre el mapa; el polvo; "la veo" |
| 49 | Hebrón | recuadro del B2, Mamré y Hebrón |
| 50 | Hebrón hoy | fotos de Hebrón |
| 51 | Cómo se amarran | tres capítulos cosidos; tres parejas de textos |
| 52 | Lecciones: Génesis 10 | portada y tres lecciones |
| 53 | Lecciones: Génesis 11 | tres lecciones |
| 54 | Lecciones: Génesis 12 | tres lecciones |
| 55 | Lecciones: Génesis 13 | tres lecciones |
| 56 | Cierre | Génesis 12:1; Hebreos 11:10 |
