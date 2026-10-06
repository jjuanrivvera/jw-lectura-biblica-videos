# Videos de lectura bíblica

Monorepositorio de proyectos audiovisuales que recorren capítulos de la Biblia y explican su secuencia, contexto y aplicaciones con narración y recursos visuales. Cada carpeta contiene un proyecto editable de HyperFrames.

## Videos incluidos

El repositorio reúne **18 proyectos editables de HyperFrames**: once tramos de Génesis, tres de Jeremías y cuatro temas.

| Carpeta | Lectura o tema | Contenido |
| --- | --- | --- |
| `genesis-01-04` | Génesis 1 al 4 | Creación, Edén, Caín y Abel |
| `genesis-05-09` | Génesis 5 al 9 | Noé, el Diluvio y el pacto |
| `genesis-10-13` | Génesis 10 al 13 | Naciones, Babel y Abrahán |
| `genesis-14-18` | Génesis 14 al 18 | La promesa a Abrahán, el rescate de Lot, el pacto y el nacimiento de Ismael e Isaac. |
| `genesis-19-23` | Génesis 19 al 23 | Sodoma, la vida de Isaac, la muerte de Sara y la compra de Macpelá. |
| `genesis-24-28` | Génesis 24 al 28 | Rebeca e Isaac, Jacob y Esaú, la primogenitura y el sueño de Betel. |
| `genesis-29-31` | Génesis 29 al 31 | Jacob, Lea y Raquel |
| `genesis-32-36` | Génesis 32 al 36 | Jacob vuelve a Canaán |
| `genesis-37-41` | Génesis 37 al 41 | José en Egipto |
| `genesis-42-47` | Génesis 42 al 47 | José se reúne con su familia |
| `genesis-48-50` | Génesis 48 al 50 | Últimos días de Jacob y José |
| `jeremias-36-37` | Jeremías 36 al 37 | El rollo y el sitio de Jerusalén |
| `jeremias-38-39` | Jeremías 38 al 39 | Jeremías y la caída de Jerusalén |
| `jeremias-40-41` | Jeremías 40 al 41 | Los sobrevivientes después de la caída |
| `tema-hilo-biblia` | Tema | El hilo conductor de la Biblia |
| `tema-siete-tiempos` | Tema | Los siete tiempos |
| `tema-trinidad` | Tema | La Trinidad |
| `tema-verdaderos-cristianos` | Tema | Cómo identificar a los verdaderos cristianos |

## Flujo de producción

Cada video conserva el guion, la narración y las composiciones editables. Genera primero el audio y sus tiempos con `python3 tools/generar-audio.py <carpeta>`; después construye las composiciones con `tools/build.sh <carpeta>`. Luego descarga o localiza las imágenes y valida el proyecto con HyperFrames.

## Requisitos

- Node.js 22 o posterior y npm.
- Python 3.10 o posterior.
- `ffmpeg` con `ffprobe` disponible en el `PATH`.
- Conexión a internet para HyperFrames, la biblioteca GSAP del CDN y la voz Edge TTS.

Instala la dependencia de voz con `python3 -m pip install -r tools/requirements.txt`.

## Imágenes

Las ilustraciones de las publicaciones de los testigos de Jehová y las fotografías de terceros no se incluyen en este repositorio por derechos de autor. Cada proyecto mantiene `video/assets.json` con la ruta de destino, el título, la referencia y el titular de derechos. Las entradas pendientes de localizar están marcadas `manual: true`; se consultó `jwlib` y se conserva la referencia disponible para completar la localización. Las rutas vacías no se descargan automáticamente.

Desde la raíz, ejecuta:

```sh
node tools/fetch-assets
```

La herramienta descarga las entradas que tienen una URL directa y muestra las demás como **“Consíguela manualmente”**, con su referencia y enlace a la publicación cuando se conoce. Coloca cada archivo en la ruta indicada por su manifiesto. Las imágenes descargadas o copiadas quedan fuera del control de versiones. Sin ellas, el render falla con la lista de imágenes que faltan.

## Generar audio y renderizar

Desde la raíz del repositorio, usa el nombre de carpeta que corresponda:

```sh
python3 tools/generar-audio.py genesis-05-09
./tools/build.sh genesis-05-09
node tools/fetch-assets
cd genesis-05-09/video
npx --yes hyperframes@0.8.72 lint
npm run render
```

El audio y los renders quedan fuera del control de versiones. `tools/render.sh <carpeta>` ofrece un acceso directo para renderizar.

## Estructura

```text
.
├── genesis-*/           # Lecturas de Génesis
├── jeremias-*/          # Lecturas de Jeremías
├── tema-*/              # Videos temáticos
├── tools/               # Voz, descarga de recursos, construcción y render
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
