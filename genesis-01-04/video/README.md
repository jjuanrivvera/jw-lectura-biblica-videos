# Génesis 1 al 4

Composición lista para el render del Hub: **1920 × 1080**, **42 escenas**, **38:46.824**, voz **es-US-AlonsoNeural**.

- Entrada: `index.html`.
- Audio y VTT por escena: `audio/`.
- Subtítulos completos: `subtitulos.vtt`.
- Capítulos: `CAPITULOS.txt`.
- Evidencia visual: `snapshots/final/`.
- Revisión local con imágenes y audio: `../REVISION.html`.
- Método, fuentes, controles y reconstrucción: `../NOTAS.md`.

Las fuentes editables están en `../escenas/`. Para reconstruir, ejecutar `python herramientas/construir.py` desde la raíz superior. Para repetir los controles completos, `python herramientas/comprobar.py`.

`npm run dev` abre la revisión de HyperFrames en primer plano. `npm run check` ejecuta la comprobación general. El comando reservado al Hub para producir el MP4 es `npm run render`; no se ejecutó durante la preparación.
