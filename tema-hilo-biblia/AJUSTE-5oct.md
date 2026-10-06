# Ajuste pedido por Juan (5-oct-2026, voz) al video "El hilo de la Biblia"

"Está muy bueno, me gusta. Pero hay un punto en el que estás explicando de los 66 libros cómo se empiezan a conectar,
y solo se explican los primeros del Viejo Testamento. Luego se desvía el tema y no se vuelve a explicar cómo siguen
los 66 libros juntos, en armonía con el mismo tema. No pasa nada si se alarga el video. Los evangelios no se
explican; de las cartas no se dice qué son, a quiénes fueron dirigidas ni por qué; y otros libros tampoco. Iba bien
(estos libros son proféticos, estos otros cuentan la vida de los reyes...), pero luego empieza a explicar otras cosas
y se olvida de retomar por donde iba con los libros y su relación."

## Qué hacer
1. Lee GUION.md, NARRACION.md y NOTAS.md de este proyecto, y mira el video actual (video/) para ubicar el tramo de los
   66 libros y el punto donde se desvía.
2. Completa el recorrido de los 66 libros, en orden y por grupos, SIN dejar ninguno fuera, y cada grupo atado al hilo
   (Génesis 3:15, la descendencia, el Reino):
   - Escrituras Hebreas: Pentateuco, históricos, poéticos y de sabiduría, profetas mayores y menores (lo que ya está
     se conserva si está bien; completa lo que falte).
   - Escrituras Griegas: los cuatro evangelios (quién escribió cada uno, a quién apunta y qué aporta de Jesús como la
     descendencia prometida); Hechos; las cartas (qué es una carta inspirada, quién las escribió, a qué congregación o
     persona fue cada grupo y por qué: Romanos, Corintios, Gálatas... las de Pablo, Hebreos, las de Santiago, Pedro,
     Juan y Judas); y Revelación como el cierre del hilo.
   - Puede ir agrupado (no un libro por escena), pero que se entienda qué es cada grupo y cómo se conecta.
3. Después del recorrido completo, retoma el resto del video como estaba, con transiciones que no rompan el hilo.
   Mismo estilo visual y la misma voz (edge-tts es-US-AlonsoNeural), horizontal 1920x1080, sin sección de lecciones,
   cierre interesante. Verifica con jwlib (~/.local/bin/jwlib) cada dato nuevo (escritor, destinatarios, fechas): la
   fuente es fuente/investigacion.html y las publicaciones de la JW; nada de memoria.
4. Duración: la que pida el contenido (puede subir de 22 a 30 minutos o más).
5. NO renderices: deja el proyecto listo y avisa con
   ssh VPS "~/bin/inject-event.sh JW_VIDEO tema_hilo_biblia_ajustado \"<duración nueva y qué grupos se añadieron>\""
6. Anota en NOTAS.md cuánto tiempo y cuántos turnos te tomó (es la primera prueba de Opus con esfuerzo bajo para
   video; Juan quiere comparar calidad y costo).
