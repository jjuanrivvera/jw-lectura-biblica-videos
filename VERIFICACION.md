# Verificación del repositorio

Revisión del contenido: 2026-09-26.

## Imágenes y fuentes

Las referencias de imagen de `escenas/` y `video/compositions/` coinciden, en nombre y orden, con las del proyecto original correspondiente en `~/jw-video`. Los archivos binarios de las publicaciones no están incluidos ni se versionan.

Cada `video/assets.json` enumera una entrada por archivo e incluye ruta, título, referencia, enlace a la publicación y titular de derechos:

| Proyecto | Entradas | URL directa de imagen | Consíguelas manualmente |
| --- | ---: | ---: | ---: |
| `genesis-14-18` | 11 | 0 | 11 |
| `genesis-19-23` | 15 | 0 | 15 |
| `genesis-24-28` | 14 | 0 | 14 |
| `jeremias-36-37` | 5 | 0 | 5 |
| **Total** | **45** | **0** | **45** |

Las investigaciones dan enlaces a las publicaciones y alojan sus copias en rutas locales `/media/`; no se encontró una URL pública directa al archivo de imagen. Por eso las entradas incluyen la referencia WOL como fuente bibliográfica, pero no una URL de descarga inventada. Las 45 imágenes se obtienen manualmente según la ruta y la cita del manifiesto. Las fuentes de este conjunto son publicaciones de los testigos de Jehová; el titular indicado es Watch Tower Bible and Tract Society of Pennsylvania. No hay fotografías externas de Wikimedia u otros proveedores entre las imágenes referenciadas.

`node tools/fetch-assets` descarga solo entradas con URL directa. Enumera las demás con **“Consíguela manualmente”** y su cita. Las imágenes JPG/JPEG se ignoran en Git. `npm run render` ejecuta primero `tools/verify-assets.mjs`, que detiene el render con la lista de archivos ausentes o vacíos y comprueba que cada imagen de composición esté en el manifiesto. Sin esos archivos el proyecto no produce el video completo.

Se eliminaron los 45 SVG de relleno y `tools/generar-svg.py`, que los generaba. Se conservó el mapa SVG propio `genesis-14-18/escenas/_mapa14.svg` y las ilustraciones vectoriales, mapas y animaciones que forman parte de las escenas originales.

## Barrido de datos personales y secretos

El 2026-09-26 se revisaron los archivos de texto del repositorio en busca de direcciones de correo o teléfonos, rutas personales, direcciones IPv4, claves privadas, tokens conocidos y secretos asignados a variables. No hubo coincidencias. El correo de autoría de los commits se conserva en los metadatos Git y no se trata como contenido del proyecto.
