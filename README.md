# Videos de lectura bíblica

Monorepositorio de proyectos audiovisuales que recorren capítulos de la Biblia y explican su secuencia, contexto y aplicaciones con narración y recursos visuales. Cada carpeta contiene un proyecto editable de HyperFrames.

## Videos incluidos

| Carpeta | Capítulos | Tema |
| --- | --- | --- |
| `genesis-14-18` | Génesis 14 al 18 | La promesa a Abrahán, el rescate de Lot, el pacto y el nacimiento de Ismael e Isaac. |
| `genesis-19-23` | Génesis 19 al 23 | Sodoma, la vida de Isaac, la muerte de Sara y la compra de Macpelá. |
| `genesis-24-28` | Génesis 24 al 28 | Rebeca e Isaac, Jacob y Esaú, la primogenitura y el sueño de Betel. |
| `jeremias-36-37` | Jeremías 36 y 37 | El rollo de Jeremías, la reacción del rey y el asedio de Jerusalén. |

## Flujo de producción

Cada video sigue este orden: `GUION.md` → `NARRACION.md` → audio por escena con `edge-tts` y la voz `es-US-AlonsoNeural` → composiciones HTML de HyperFrames → render. Las carpetas `escenas/` conservan las fuentes editables; `video/compositions/` contiene las composiciones que carga HyperFrames.

## Requisitos

- Node.js 22 o posterior y npm.
- Python 3.10 o posterior.
- `ffmpeg` con `ffprobe` disponible en el `PATH`.
- Conexión a internet para HyperFrames, la biblioteca GSAP del CDN y la voz Edge TTS.

Instala la dependencia de voz con `python3 -m pip install -r tools/requirements.txt`.

## Imágenes

Las ilustraciones y los mapas de las publicaciones de los testigos de Jehová, y las fotografías de terceros, no se incluyen en este repositorio por derechos de autor. Cada proyecto mantiene un `video/assets.json` con la ruta de destino, el título, la referencia bibliográfica, el enlace a la fuente cuando está disponible y el titular de derechos.

Desde la raíz, ejecuta:

```sh
node tools/fetch-assets
```

La herramienta descarga las entradas que tienen una URL directa y muestra las demás como **“Consíguela manualmente”**, con su referencia y enlace a la publicación. Coloca cada archivo en la ruta indicada por su manifiesto. Las imágenes descargadas o copiadas quedan fuera del control de versiones. Sin ellas, el render falla con la lista de imágenes que faltan y el video no se renderiza completo.

## Generar audio y renderizar

Desde la raíz del repositorio, genera el audio de un proyecto y reconstruye sus composiciones para actualizar la sincronización:

```sh
python3 tools/generar-audio.py genesis-14-18
node genesis-14-18/herramientas/construir.mjs
node tools/fetch-assets
cd genesis-14-18/video
npx --yes hyperframes@0.8.72 lint
npm run render
```

Para una narración manual de una escena, el comando base es `edge-tts --voice es-US-AlonsoNeural --text "Texto de la escena" --write-media video/audio/escena-00.mp3`. Cambia el número de escena según corresponda. El script común extrae el texto de `NARRACION.md`, genera un MP3 por escena y guarda los tiempos por palabra que necesita el constructor.

También puedes ejecutar el render con `tools/render.sh genesis-14-18`. Sustituye el nombre por cualquiera de las otras tres carpetas. Los renders y el audio quedan fuera del control de versiones.

## Estructura

```text
.
├── genesis-14-18/       # Guion, narración, escenas y proyecto HyperFrames
├── genesis-19-23/
├── genesis-24-28/
├── jeremias-36-37/
├── tools/               # Voz, descarga de recursos y render
├── .gitignore
├── LICENSE
├── METODO.md
└── README.md
```

## Método

El criterio editorial está resumido en [METODO.md](METODO.md): ordenar primero los hechos, explicar los detalles no obvios, señalar la incertidumbre y usar mapas reales para ubicar los lugares. Las lecciones se agrupan al final y se conectan con los capítulos.

## Licencias y derechos

El código de este repositorio se distribuye bajo la licencia MIT. El contenido bíblico y las publicaciones citadas pertenecen a sus respectivos titulares. La licencia MIT no se extiende a ese contenido.

## English

This repository contains four editable HyperFrames projects for educational Bible chapter videos. Code is MIT licensed; biblical content and cited publications remain the property of their respective rights holders.
