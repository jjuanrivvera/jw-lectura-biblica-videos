// Dibujos compartidos: el rollo, el brasero, la bula y el pan.
// Cada función devuelve el marcado SVG de un <g>; la escena lo pone con innerHTML antes de armar
// la línea de tiempo. Los degradados llevan el ID de la escena para no chocar en la página armada.
const G = (n) => n + "-" + ID;
const url = (n) => "url(#" + G(n) + ")";

// Azar con semilla: las líneas de texto del rollo salen iguales en cada cuadro del render.
function azar(seed) {
  let a = seed >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function defsDibujos() {
  return `<defs>
  <linearGradient id="${G("perg")}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f3e6c4"/><stop offset="0.55" stop-color="#e7d3a3"/><stop offset="1" stop-color="#c8ab70"/></linearGradient>
  <linearGradient id="${G("perg-h")}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#a88a55"/><stop offset="0.35" stop-color="#f1e2bb"/><stop offset="0.6" stop-color="#e2cb95"/><stop offset="1" stop-color="#8f7243"/></linearGradient>
  <linearGradient id="${G("perg-v")}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#a88a55"/><stop offset="0.35" stop-color="#f1e2bb"/><stop offset="0.6" stop-color="#e2cb95"/><stop offset="1" stop-color="#8f7243"/></linearGradient>
  <linearGradient id="${G("mad")}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#4a2a12"/><stop offset="0.45" stop-color="#a26a36"/><stop offset="0.62" stop-color="#bf884e"/><stop offset="1" stop-color="#3f230e"/></linearGradient>
  <linearGradient id="${G("bronce")}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e2ae62"/><stop offset="0.45" stop-color="#a8722f"/><stop offset="1" stop-color="#4f3212"/></linearGradient>
  <linearGradient id="${G("bronce-h")}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#5a3a16"/><stop offset="0.3" stop-color="#d49b52"/><stop offset="0.55" stop-color="#f0c27a"/><stop offset="1" stop-color="#4f3212"/></linearGradient>
  <radialGradient id="${G("brasa")}" cx="0.5" cy="0.5" r="0.6"><stop offset="0" stop-color="#fff0a0"/><stop offset="0.35" stop-color="#ff9b3d"/><stop offset="1" stop-color="#8e2410"/></radialGradient>
  <linearGradient id="${G("llama")}" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#fff2a6"/><stop offset="0.3" stop-color="#ffc34d"/><stop offset="0.7" stop-color="#ff7a26"/><stop offset="1" stop-color="#d9371a" stop-opacity="0.15"/></linearGradient>
  <linearGradient id="${G("llama2")}" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#ffffff"/><stop offset="0.5" stop-color="#ffe27a"/><stop offset="1" stop-color="#ffb13b" stop-opacity="0"/></linearGradient>
  <radialGradient id="${G("brillo")}"><stop offset="0" stop-color="#ffac40" stop-opacity="0.55"/><stop offset="0.6" stop-color="#ff8a2a" stop-opacity="0.15"/><stop offset="1" stop-color="#ff8a2a" stop-opacity="0"/></radialGradient>
  <radialGradient id="${G("pan")}" cx="0.42" cy="0.36" r="0.72"><stop offset="0" stop-color="#f6d08a"/><stop offset="0.55" stop-color="#cf9143"/><stop offset="1" stop-color="#7a461a"/></radialGradient>
  <radialGradient id="${G("arcilla")}" cx="0.4" cy="0.35" r="0.75"><stop offset="0" stop-color="#dba077"/><stop offset="0.7" stop-color="#a5643c"/><stop offset="1" stop-color="#6a381d"/></radialGradient>
  <radialGradient id="${G("piedra")}" cx="0.4" cy="0.3" r="0.8"><stop offset="0" stop-color="#8d9aa8"/><stop offset="1" stop-color="#3c4652"/></radialGradient>
  <filter id="${G("sombra")}" x="-20%" y="-20%" width="140%" height="160%"><feDropShadow dx="0" dy="12" stdDeviation="12" flood-color="#000" flood-opacity="0.45"/></filter>
  <filter id="${G("difusa")}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="14"/></filter>
  </defs>`;
}

// Columnas de texto: renglones alineados a la derecha, como el hebreo, que se escribe de derecha a izquierda.
function columnas(x, y, w, h, n, seed, clase = "col") {
  const r = azar(seed), cw = w / n;
  let s = "";
  for (let c = 0; c < n; c++) {
    s += `<g class="${clase}">`;
    const x2 = x + c * cw + cw * 0.88, ww = cw * 0.76;
    for (let yy = y + h * 0.1; yy < y + h * 0.9; yy += 15) {
      const L = ww * (0.55 + 0.45 * r());
      s += `<line x1="${(x2 - L).toFixed(1)}" y1="${yy.toFixed(1)}" x2="${x2.toFixed(1)}" y2="${yy.toFixed(1)}" stroke="#3f2c1a" stroke-width="4.5" stroke-linecap="round" opacity="0.78"/>`;
    }
    s += `</g>`;
  }
  return s;
}

// Una hoja de pergamino abierta, con costuras cada `cada` columnas (los pedazos pegados).
function hoja(x, y, w, h, n, seed, o = {}) {
  const cw = w / n;
  let costuras = "";
  const cada = o.cada ?? 2;
  for (let c = cada; c < n; c += cada)
    costuras += `<line x1="${x + c * cw}" y1="${y + 3}" x2="${x + c * cw}" y2="${y + h - 3}" stroke="#a88a55" stroke-width="3" opacity="0.7"/>`;
  return `<g class="${o.clase ?? "hoja"}">
    <rect x="${x}" y="${y}" width="${w}" height="${h}" rx="5" fill="${url("perg")}" filter="${url("sombra")}"/>
    <rect x="${x}" y="${y}" width="${w}" height="10" fill="#fff6dc" opacity="0.35"/>
    <rect x="${x}" y="${y + h - 12}" width="${w}" height="12" fill="#8f7243" opacity="0.35"/>
    ${costuras}
    ${o.sinTexto ? "" : columnas(x, y, w, h, n, seed, o.col ?? "col")}
  </g>`;
}

// El palo con la parte enrollada del pergamino: un cilindro de pergamino y las puntas de madera.
function palo(cx, y, h, grosor = 56, clase = "palo") {
  const r = grosor / 2;
  return `<g class="${clase}">
    <rect x="${cx - 9}" y="${y - 46}" width="18" height="${h + 92}" rx="9" fill="${url("mad")}"/>
    <ellipse cx="${cx}" cy="${y - 50}" rx="20" ry="11" fill="#8a5a2b"/><ellipse cx="${cx}" cy="${y + h + 50}" rx="20" ry="11" fill="#6b4220"/>
    <rect x="${cx - r}" y="${y - 6}" width="${grosor}" height="${h + 12}" rx="${r * 0.45}" fill="${url("perg-h")}" filter="${url("sombra")}"/>
    <line x1="${cx - r * 0.35}" y1="${y}" x2="${cx - r * 0.35}" y2="${y + h}" stroke="#fff8e0" stroke-width="3" opacity="0.5"/>
    <line x1="${cx + r * 0.5}" y1="${y}" x2="${cx + r * 0.5}" y2="${y + h}" stroke="#7a5c30" stroke-width="2" opacity="0.5"/>
  </g>`;
}

// Rollo abierto: dos palos y la hoja entre ellos.
function rollo(x, y, w, h, n, seed, o = {}) {
  return `<g class="${o.clase ?? "rollo"}">${hoja(x, y, w, h, n, seed, o)}${palo(x - 8, y, h, o.grosor ?? 56, "palo palo-i")}${palo(x + w + 8, y, h, o.grosor ?? 56, "palo palo-d")}</g>`;
}

// Rollo cerrado, visto de lado (para iconos y para "otro rollo").
function rolloCerrado(cx, cy, largo = 260, grosor = 70, clase = "rollo-c") {
  const r = grosor / 2;
  return `<g class="${clase}">
    <rect x="${cx - 7}" y="${cy - largo / 2 - 40}" width="14" height="${largo + 80}" rx="7" fill="${url("mad")}"/>
    <rect x="${cx - r}" y="${cy - largo / 2}" width="${grosor}" height="${largo}" rx="${r * 0.4}" fill="${url("perg-h")}" filter="${url("sombra")}"/>
    <path d="M ${cx + r} ${cy - largo / 2 + 20} q 26 12 20 60 l -20 0 z" fill="#e7d3a3"/>
    <line x1="${cx - r * 0.3}" y1="${cy - largo / 2 + 6}" x2="${cx - r * 0.3}" y2="${cy + largo / 2 - 6}" stroke="#fff8e0" stroke-width="3" opacity="0.55"/>
  </g>`;
}

// Llama: forma de gota con punta; `k` la escala. El origen está en la base.
function llama(x, y, k = 1, clase = "llama") {
  return `<g class="${clase}" transform="translate(${x} ${y})"><g class="ll">
    <path d="M0 0 C ${-44 * k} ${-24 * k} ${-34 * k} ${-84 * k} ${-6 * k} ${-128 * k} C ${-2 * k} ${-92 * k} ${22 * k} ${-86 * k} ${14 * k} ${-150 * k} C ${50 * k} ${-100 * k} ${46 * k} ${-26 * k} 0 0 Z" fill="${url("llama")}"/>
    <path d="M0 -4 C ${-20 * k} ${-18 * k} ${-16 * k} ${-52 * k} ${2 * k} ${-82 * k} C ${18 * k} ${-50 * k} ${22 * k} ${-18 * k} 0 -4 Z" fill="${url("llama2")}"/>
  </g></g>`;
}

// Brasero: recipiente redondo, poco profundo, sobre patas, de metal (Perspicacia, "Brasero").
function brasero(cx, cy, s = 1) {
  const L = (x, y) => `${cx + x * s} ${cy + y * s}`;
  let brasas = "";
  const r = azar(7);
  for (let i = 0; i < 16; i++) {
    const x = (r() * 2 - 1) * 115, y = (r() * 2 - 1) * 12;
    brasas += `<ellipse class="brasa" cx="${cx + x * s}" cy="${cy + y * s - 4 * s}" rx="${(14 + r() * 12) * s}" ry="${(8 + r() * 5) * s}" fill="${url("brasa")}"/>`;
  }
  const llamas = [[-80, 0.7], [-38, 1.0], [0, 1.35], [42, 1.05], [84, 0.75]]
    .map(([x, k], i) => llama(cx + x * s, cy - 6 * s, k * s, "llama l" + i)).join("");
  return `<g class="brasero">
    <ellipse class="resplandor" cx="${cx}" cy="${cy - 60 * s}" rx="${300 * s}" ry="${230 * s}" fill="${url("brillo")}"/>
    <ellipse cx="${cx}" cy="${cy + 205 * s}" rx="${190 * s}" ry="${22 * s}" fill="#000" opacity="0.35"/>
    <path d="M ${L(-110, 60)} L ${L(-150, 200)} L ${L(-128, 200)} L ${L(-84, 66)} Z" fill="${url("bronce-h")}"/>
    <path d="M ${L(110, 60)} L ${L(150, 200)} L ${L(128, 200)} L ${L(84, 66)} Z" fill="${url("bronce-h")}"/>
    <path d="M ${L(-12, 88)} L ${L(-14, 212)} L ${L(14, 212)} L ${L(12, 88)} Z" fill="${url("bronce-h")}"/>
    <path d="M ${L(-170, 0)} Q ${L(-160, 92)} ${L(0, 96)} Q ${L(160, 92)} ${L(170, 0)} Z" fill="${url("bronce")}"/>
    <path d="M ${L(-150, 26)} Q ${L(-120, 70)} ${L(-40, 82)}" fill="none" stroke="#f3c77f" stroke-width="${5 * s}" opacity="0.5" stroke-linecap="round"/>
    <ellipse cx="${cx}" cy="${cy}" rx="${170 * s}" ry="${28 * s}" fill="#5c3915"/>
    <ellipse cx="${cx}" cy="${cy}" rx="${158 * s}" ry="${22 * s}" fill="#2a1508"/>
    ${brasas}
    <g class="llamas">${llamas}</g>
    <ellipse cx="${cx}" cy="${cy}" rx="${170 * s}" ry="${28 * s}" fill="none" stroke="#e4b066" stroke-width="${4 * s}" opacity="0.8"/>
  </g>`;
}

// Las llamas bailan: escalas y giros pequeños, con repeticiones finitas.
function llamear(t0, t1, sel = ".llama .ll") {
  el(sel).forEach((f, i) => {
    const d = 0.32 + (i % 3) * 0.07;
    const n = Math.max(1, Math.floor((t1 - t0) / d));
    tl.fromTo(f, { scaleY: 0.86, scaleX: 1.04, rotation: -3 + (i % 2) * 6, transformOrigin: "50% 100%" },
      { scaleY: 1.14, scaleX: 0.94, rotation: 3 - (i % 2) * 6, transformOrigin: "50% 100%", duration: d, yoyo: true, repeat: n, ease: "sine.inOut", immediateRender: true }, t0 + i * 0.05);
  });
}

// Pan redondo, dorado, con cortes.
function pan(cx, cy, r = 90, clase = "pan") {
  return `<g class="${clase}">
    <ellipse cx="${cx}" cy="${cy + r * 0.78}" rx="${r * 1.02}" ry="${r * 0.2}" fill="#000" opacity="0.35"/>
    <ellipse cx="${cx}" cy="${cy + r * 0.12}" rx="${r}" ry="${r * 0.72}" fill="#6e3f17"/>
    <ellipse cx="${cx}" cy="${cy}" rx="${r}" ry="${r * 0.7}" fill="${url("pan")}"/>
    <path d="M ${cx - r * 0.55} ${cy - r * 0.18} Q ${cx} ${cy - r * 0.42} ${cx + r * 0.55} ${cy - r * 0.18}" fill="none" stroke="#8a5220" stroke-width="${r * 0.07}" stroke-linecap="round" opacity="0.75"/>
    <path d="M ${cx - r * 0.62} ${cy + r * 0.1} Q ${cx} ${cy - r * 0.12} ${cx + r * 0.62} ${cy + r * 0.1}" fill="none" stroke="#8a5220" stroke-width="${r * 0.07}" stroke-linecap="round" opacity="0.75"/>
    <path d="M ${cx - r * 0.5} ${cy + r * 0.36} Q ${cx} ${cy + r * 0.18} ${cx + r * 0.5} ${cy + r * 0.36}" fill="none" stroke="#8a5220" stroke-width="${r * 0.07}" stroke-linecap="round" opacity="0.75"/>
    <ellipse cx="${cx - r * 0.3}" cy="${cy - r * 0.34}" rx="${r * 0.3}" ry="${r * 0.12}" fill="#fff4d6" opacity="0.28"/>
  </g>`;
}

// Bula: pedacito de arcilla sobre el nudo del cordel, con la marca del sello.
function bula(cx, cy, s = 1, clase = "bula") {
  const P = (x, y) => `${cx + x * s} ${cy + y * s}`;
  return `<g class="${clase}">
    <path d="M ${P(-118, 6)} C ${P(-128, -70)} ${P(-40, -104)} ${P(18, -98)} C ${P(96, -92)} ${P(134, -40)} ${P(122, 18)} C ${P(112, 84)} ${P(40, 104)} ${P(-24, 98)} C ${P(-90, 92)} ${P(-112, 58)} ${P(-118, 6)} Z" fill="${url("arcilla")}" filter="${url("sombra")}"/>
    <g class="marca" opacity="0.9">
      <ellipse cx="${cx}" cy="${cy}" rx="${88 * s}" ry="${70 * s}" fill="none" stroke="#5a2c12" stroke-width="${4 * s}"/>
      <line x1="${cx - 78 * s}" y1="${cy - 16 * s}" x2="${cx + 78 * s}" y2="${cy - 16 * s}" stroke="#5a2c12" stroke-width="${3 * s}"/>
      <line x1="${cx - 78 * s}" y1="${cy + 18 * s}" x2="${cx + 78 * s}" y2="${cy + 18 * s}" stroke="#5a2c12" stroke-width="${3 * s}"/>
      ${[-40, 1, 38].map((yy) => [...Array(7)].map((_, i) => `<path d="M ${P(-54 + i * 18, yy - 9)} l ${6 * s} ${14 * s} l ${6 * s} ${-12 * s}" fill="none" stroke="#4c240f" stroke-width="${3.5 * s}" stroke-linecap="round"/>`).join("")).join("")}
    </g>
    <path d="M ${P(-80, -60)} Q ${P(-40, -84)} ${P(10, -80)}" fill="none" stroke="#f0c6a0" stroke-width="${6 * s}" opacity="0.35" stroke-linecap="round"/>
  </g>`;
}
