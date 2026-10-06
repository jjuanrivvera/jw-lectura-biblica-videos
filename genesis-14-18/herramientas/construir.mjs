#!/usr/bin/env node
// Construye el proyecto de HyperFrames a partir de las escenas escritas a mano.
//
//   escenas/NN.html            fuente de cada escena: <style>, marcado y <script> con la coreografía
//   escenas/_base.css          estilo común (se anida bajo #escena-NN)
//   escenas/_lib.js            librería común (sincronía con la voz, trazos, tablero...)
//   video/audio/escenas.json   duración real de cada audio (herramientas/voz.py)
//   video/audio/escena-NN.words.json  tiempos por palabra
//
// Salida: video/compositions/escena-NN.html y video/index.html.
// La duración de cada escena sale del audio: LEAD de silencio + voz + TAIL de respiro.
// Antes de escribir, comprueba que cada frase usada en at("...")/fin("...") exista en la voz.
import fs from "node:fs";
import path from "node:path";

const RAIZ = path.resolve(path.dirname(new URL(import.meta.url).pathname), "..");
const ESC = path.join(RAIZ, "escenas");
const VID = path.join(RAIZ, "video");
const LEAD = 0.6;
const TAIL = 1.2;
const W_ = 1080, H_ = 1920;

const resumen = JSON.parse(fs.readFileSync(path.join(VID, "audio/escenas.json"), "utf8"));
const base = fs.readFileSync(path.join(ESC, "_base.css"), "utf8");
const lib = fs.readFileSync(path.join(ESC, "_lib.js"), "utf8");

const FUENTES = ``;
const norm = (s) =>
  s.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/[^a-z0-9ñ]/g, "");

// Las palabras con guion ("Asterot-Carnaim") se parten en dos, repartiendo su tiempo,
// para que la coreografía pueda citar cualquiera de las dos mitades.
function palabras(id) {
  const crudo = JSON.parse(fs.readFileSync(path.join(VID, `audio/escena-${id}.words.json`), "utf8"));
  const out = [];
  for (const w of crudo) {
    const partes = w.w.split("-").filter(Boolean);
    const d = w.d / partes.length;
    partes.forEach((p, k) =>
      out.push({ w: p, t: +(w.t + LEAD + k * d).toFixed(3), d: +d.toFixed(3) }));
  }
  return out;
}

function comprueba(id, js, W) {
  const WN = W.map((w) => norm(w.w));
  const errores = [];
  for (const m of js.matchAll(/\b(?:at|fin)\(\s*"([^"]+)"/g)) {
    const p = m[1].split(/[\s\-]+/).map(norm).filter(Boolean);
    let ok = false;
    for (let i = 0; i < WN.length && !ok; i++) ok = p.every((x, k) => WN[i + k] === x);
    if (!ok) errores.push(m[1]);
  }
  if (errores.length) throw new Error(`escena ${id}: frases que la voz no dice: ${errores.join(" | ")}`);
}

function partes(src) {
  const style = [...src.matchAll(/<style>([\s\S]*?)<\/style>/g)].map((m) => m[1]).join("\n");
  const script = [...src.matchAll(/<script>([\s\S]*?)<\/script>/g)].map((m) => m[1]).join("\n");
  const html = src.replace(/<style>[\s\S]*?<\/style>/g, "").replace(/<script>[\s\S]*?<\/script>/g, "").trim();
  return { style, script, html };
}

const escenas = [];
let t = 0;
for (const e of resumen) {
  const fuente = path.join(ESC, `${e.id}.html`);
  if (!fs.existsSync(fuente)) continue;
  const W = palabras(e.id);
  // La última escena se queda más en pantalla: es el cierre del video.
  const tail = e === resumen[resumen.length - 1] ? 4.0 : TAIL;
  const dur = +(LEAD + e.dur + tail).toFixed(3);
  // Piezas compartidas entre escenas (el mapa de Génesis 14): <!--incluir:x--> y /*incluir:x*/.
  const crudo = fs.readFileSync(fuente, "utf8").replace(/<!--incluir:([\w.\-]+)-->|\/\*incluir:([\w.\-]+)\*\//g,
    (_, a, b) => fs.readFileSync(path.join(ESC, a || b), "utf8"));
  const { style, script, html } = partes(crudo);
  comprueba(e.id, script, W);
  const id = `escena-${e.id}`;
  const comp = `<!doctype html>
<html lang="es">
<head><meta charset="UTF-8" /><title>${e.titulo}</title></head>
<body>
<template>
<style>${FUENTES}
#${id} {
${base}
${style}
}
</style>
<div id="${id}" data-composition-id="${id}" data-width="${W_}" data-height="${H_}">
<div class="contenido">
${html}
</div>
</div>
<script>
(function () {
const ID = ${JSON.stringify(id)};
const DUR = ${dur};
const LEAD = ${LEAD};
const W = ${JSON.stringify(W)};
${lib}
${script}
marco();
window.__timelines = window.__timelines || {};
window.__timelines[ID] = tl;
})();
</script>
</template>
</body>
</html>
`;
  fs.writeFileSync(path.join(VID, "compositions", `${id}.html`), comp);
  escenas.push({ ...e, id, num: e.id, start: +t.toFixed(3), dur, voz: e.dur });
  t += dur;
}
const TOTAL = +t.toFixed(3);

const hosts = escenas.map((e) => `      <div id="h-${e.num}" data-composition-id="${e.id}" data-composition-src="compositions/${e.id}.html" data-start="${e.start}" data-duration="${e.dur}" data-track-index="1" data-width="${W_}" data-height="${H_}"></div>`).join("\n");
const voces = escenas.map((e) => `      <audio id="voz-${e.num}" src="audio/escena-${e.num}.mp3" data-start="${(e.start + LEAD).toFixed(3)}" data-duration="${e.voz.toFixed(3)}" data-track-index="10" data-volume="1"></audio>`).join("\n");

const index = `<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=${W_}, height=${H_}" />
    <title>Génesis 14 al 18: una promesa que se va aclarando</title>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>${FUENTES}
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body { width: ${W_}px; height: ${H_}px; overflow: hidden; background: #17212b; }
      #root { position: relative; width: 100%; height: 100%; overflow: hidden; background: #17212b; }
      /* Pizarra: el fondo es común a todas las escenas para que los cortes no parpadeen. */
      #pizarra { position: absolute; inset: 0; background:
        radial-gradient(ellipse 70% 45% at 30% 22%, rgba(120, 150, 170, 0.10), transparent 70%),
        radial-gradient(ellipse 60% 40% at 75% 78%, rgba(120, 150, 170, 0.08), transparent 70%),
        radial-gradient(ellipse 120% 90% at 50% 50%, transparent 55%, rgba(5, 9, 14, 0.55) 100%),
        #17212b; }
      #grano { position: absolute; inset: -40px; opacity: 0.16; mix-blend-mode: screen;
        background-image: url("assets/grano.png"); background-size: 512px 512px; }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="${TOTAL}" data-width="${W_}" data-height="${H_}">
      <div id="pizarra"></div>
      <div id="grano"></div>
${hosts}
${voces}
    </div>
    <script>
      const tl = gsap.timeline({ paused: true });
      // El polvo de tiza deriva muy despacio durante todo el video.
      tl.fromTo("#grano", { x: 0, y: 0 }, { x: -30, y: -24, duration: ${TOTAL}, ease: "none" }, 0);
      window.__timelines = window.__timelines || {};
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
`;
fs.writeFileSync(path.join(VID, "index.html"), index);
fs.writeFileSync(path.join(VID, "escenas.json"), JSON.stringify(escenas.map(({ num, titulo, start, dur }) => ({ num, titulo, start, dur })), null, 1));
const mm = Math.floor(TOTAL / 60), ss = (TOTAL % 60).toFixed(1);
console.log(`${escenas.length} escenas, ${TOTAL}s (${mm}:${ss.padStart(4, "0")})`);
