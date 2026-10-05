#!/usr/bin/env node
// Construye el proyecto de HyperFrames a partir de las escenas escritas a mano.
//
//   escenas/NN.html            fuente de cada escena: <style>, marcado y <script> con la coreografía
//   escenas/_base.css          estilo común (se anida bajo #escena-NN)
//   escenas/_lib.js            librería común (sincronía con la voz, trazos, mapas, retratos...)
//   NARRACION.md               títulos de las escenas ("## NN · título")
//   video/audio/escenas.json   duración real de cada audio (herramientas-comunes/voz.py)
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
const TAIL = 0.9;
const W_ = 1920, H_ = 1080;

const resumen = JSON.parse(fs.readFileSync(path.join(VID, "audio/escenas.json"), "utf8"));
const base = fs.readFileSync(path.join(ESC, "_base.css"), "utf8");
const lib = fs.readFileSync(path.join(ESC, "_lib.js"), "utf8");
const titulos = Object.fromEntries(
  [...fs.readFileSync(path.join(RAIZ, "NARRACION.md"), "utf8").matchAll(/^## (\d+) · (.+)$/gm)].map((m) => [m[1], m[2].trim()]));

const FUENTES = `
@font-face { font-family: "Fraunces"; src: url("assets/fonts/Fraunces.ttf") format("truetype"); font-weight: 100 900; font-style: normal; }
@font-face { font-family: "Fraunces"; src: url("assets/fonts/Fraunces-Italic.ttf") format("truetype"); font-weight: 100 900; font-style: italic; }
@font-face { font-family: "Caveat"; src: url("assets/fonts/Caveat.ttf") format("truetype"); font-weight: 400 700; }
@font-face { font-family: "Montserrat"; src: url("assets/fonts/Montserrat.ttf") format("truetype"); font-weight: 100 900; }
@font-face { font-family: "NotoHebrew"; src: url("assets/fonts/NotoSerifHebrew-Bold.ttf") format("truetype"); font-weight: 700; }
@font-face { font-family: "NotoSerif"; src: url("assets/fonts/NotoSerif-Regular.ttf") format("truetype"); font-weight: 400; font-style: normal; }
@font-face { font-family: "NotoSerif"; src: url("assets/fonts/NotoSerif-Bold.ttf") format("truetype"); font-weight: 700; font-style: normal; }
@font-face { font-family: "NotoSerif"; src: url("assets/fonts/NotoSerif-Italic.ttf") format("truetype"); font-weight: 400; font-style: italic; }`;

const norm = (s) =>
  s.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/[^a-z0-9ñ]/g, "");

// Las palabras con guion ("Beer-Seba") se parten en dos, repartiendo su tiempo,
// para que la coreografía pueda citar cualquiera de las dos mitades.
function palabras(id, lead) {
  const crudo = JSON.parse(fs.readFileSync(path.join(VID, `audio/${id}.words.json`), "utf8"));
  const out = [];
  for (const w of crudo) {
    const partes = w.w.split("-").filter(Boolean);
    const d = w.d / partes.length;
    partes.forEach((p, k) =>
      out.push({ w: p, t: +(w.t + lead + k * d).toFixed(3), d: +d.toFixed(3) }));
  }
  return out;
}

function comprueba(num, js, W) {
  const WN = W.map((w) => norm(w.w));
  const errores = [];
  for (const m of js.matchAll(/\b(?:at|fin)\(\s*"([^"]+)"\s*(,)?/g)) {
    const p = m[1].split(/[\s\-]+/).map(norm).filter(Boolean);
    let n = 0;
    for (let i = 0; i < WN.length; i++) if (p.every((x, k) => WN[i + k] === x)) n++;
    if (!n) errores.push(m[1]);
    // Una frase que la voz dice más de una vez ancla a la primera: casi nunca es lo que se quiere.
    else if (n > 1 && !m[2]) console.warn(`  aviso escena ${num}: "${m[1]}" aparece ${n} veces; se usa la primera`);
  }
  if (errores.length) throw new Error(`escena ${num}: frases que la voz no dice: ${errores.join(" | ")}`);
}

function partes(src) {
  const style = [...src.matchAll(/<style>([\s\S]*?)<\/style>/g)].map((m) => m[1]).join("\n");
  const script = [...src.matchAll(/<script>([\s\S]*?)<\/script>/g)].map((m) => m[1]).join("\n");
  const html = src.replace(/<style>[\s\S]*?<\/style>/g, "").replace(/<script>[\s\S]*?<\/script>/g, "").trim();
  return { style, script, html };
}

const soloUna = process.argv[2];
const escenas = [];
let t = 0;
for (const e of resumen) {
  const num = e.id.replace("escena-", "");
  const fuente = path.join(ESC, `${num}.html`);
  if (!fs.existsSync(fuente)) { console.warn(`  falta escenas/${num}.html`); continue; }
  // Piezas compartidas entre escenas (el mapa, los retratos): <!--incluir:x--> y /*incluir:x*/.
  const crudo = fs.readFileSync(fuente, "utf8").replace(/<!--incluir:([\w.\-]+)-->|\/\*incluir:([\w.\-]+)\*\//g,
    (_, a, b) => fs.readFileSync(path.join(ESC, a || b), "utf8"));
  // Las escenas que abren capítulo piden más silencio antes de la voz (<!--lead:2.0-->), para que la tarjeta se lea.
  const lead = +(crudo.match(/<!--lead:([\d.]+)-->/)?.[1] ?? LEAD);
  const W = palabras(e.id, lead);
  // La última escena se queda más en pantalla: es el cierre del video.
  const tail = e === resumen[resumen.length - 1] ? 4.0 : TAIL;
  const dur = +(lead + e.dur + tail).toFixed(3);
  const { style, script, html } = partes(crudo);
  comprueba(num, script, W);
  const id = `escena-${num}`;
  const titulo = titulos[num] ?? id;
  const comp = `<!doctype html>
<html lang="es">
<head><meta charset="UTF-8" /><title>${titulo}</title></head>
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
const LEAD = ${lead};
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
  if (!soloUna || soloUna === num) fs.writeFileSync(path.join(VID, "compositions", `${id}.html`), comp);
  escenas.push({ id, num, titulo, start: +t.toFixed(3), dur, voz: e.dur, lead });
  t += dur;
}
const TOTAL = +t.toFixed(3);

const hosts = escenas.map((e) => `      <div id="h-${e.num}" data-composition-id="${e.id}" data-composition-src="compositions/${e.id}.html" data-start="${e.start}" data-duration="${e.dur}" data-track-index="1" data-width="${W_}" data-height="${H_}"></div>`).join("\n");
const voces = escenas.map((e) => `      <audio id="voz-${e.num}" src="audio/${e.id}.mp3" data-start="${(e.start + e.lead).toFixed(3)}" data-duration="${e.voz.toFixed(3)}" data-track-index="10" data-volume="1"></audio>`).join("\n");

const index = `<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=${W_}, height=${H_}" />
    <title>Cómo identificar a los verdaderos cristianos</title>
    <script src="assets/gsap.min.js"></script>
    <style>${FUENTES}
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body { width: ${W_}px; height: ${H_}px; overflow: hidden; background: #16202a; }
      #root { position: relative; width: 100%; height: 100%; overflow: hidden; background: #16202a; }
      /* Pizarra: el fondo es común a todas las escenas para que los cortes no parpadeen. */
      #pizarra { position: absolute; inset: 0; background:
        radial-gradient(ellipse 65% 50% at 26% 20%, rgba(126, 156, 176, 0.11), transparent 70%),
        radial-gradient(ellipse 55% 45% at 78% 80%, rgba(176, 146, 106, 0.07), transparent 70%),
        radial-gradient(ellipse 120% 95% at 50% 50%, transparent 58%, rgba(4, 8, 13, 0.6) 100%),
        #16202a; }
      #grano { position: absolute; inset: -40px; opacity: 0.15; mix-blend-mode: screen;
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
