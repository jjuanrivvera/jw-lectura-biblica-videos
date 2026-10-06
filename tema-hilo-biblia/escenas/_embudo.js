// La línea de la descendencia como una franja de oro que se estrecha hasta una sola persona y se vuelve a abrir.
// Se dibuja grande en la escena 06 y como cinta de "dónde estamos" en las escenas 07 a 11.
const NODOS = [["la mujer", 0.03], ["Abrahán", 0.19], ["Isaac", 0.28], ["Jacob", 0.37], ["Judá", 0.47],
  ["David", 0.58], ["Jesús", 0.72], ["144.000", 0.85], ["las naciones", 0.97]];
const ANGOSTO = 0.72;
function mitadEn(f, mitad) {
  const m = f < ANGOSTO ? Math.pow(1 - f / ANGOSTO, 1.25) : Math.pow((f - ANGOSTO) / (1 - ANGOSTO), 0.9);
  return Math.max(4, mitad * (0.03 + 0.97 * m));
}
// Devuelve el marcado SVG de la franja, sus puntos y (si se pide) los rótulos. Prefijo de clases: "em".
function embudo(o) {
  const { x0, w, cy, mitad, id = "em", fs = 30, rotulos = "abajo" } = o;
  const N = 140, sup = [], inf = [];
  for (let i = 0; i <= N; i++) {
    const f = i / N, x = x0 + f * w, h = mitadEn(f, mitad);
    sup.push(x.toFixed(1) + " " + (cy - h).toFixed(1));
    inf.push(x.toFixed(1) + " " + (cy + h).toFixed(1));
  }
  const d = "M " + sup.join(" L ") + " L " + inf.reverse().join(" L ") + " Z";
  let s = '<defs><linearGradient id="' + id + '-g" x1="0" y1="0" x2="0" y2="1">' +
    '<stop offset="0" stop-color="#f6d98f" stop-opacity="0.55"/><stop offset="0.5" stop-color="#ebbd5c" stop-opacity="0.85"/>' +
    '<stop offset="1" stop-color="#c8963a" stop-opacity="0.55"/></linearGradient>' +
    '<clipPath id="' + id + '-c"><rect class="' + id + '-rev" x="' + (x0 - 20) + '" y="' + (cy - mitad - 60) + '" width="0" height="' + (2 * mitad + 120) + '"/></clipPath></defs>' +
    '<path d="' + d + '" fill="#ebbd5c" fill-opacity="0.07" stroke="#ebbd5c" stroke-opacity="0.18" stroke-width="2"/>' +
    '<g clip-path="url(#' + id + '-c)"><path d="' + d + '" fill="url(#' + id + '-g)" stroke="#f6d98f" stroke-width="2" stroke-opacity="0.6"/>' +
    '<path d="M ' + x0 + ' ' + cy + ' L ' + (x0 + w) + ' ' + cy + '" stroke="#10162a" stroke-opacity="0.35" stroke-width="2" stroke-dasharray="6 10"/></g>';
  NODOS.forEach(([n, f], i) => {
    const x = x0 + f * w;
    s += '<g class="' + id + '-n ' + id + '-n' + i + '">';
    s += '<circle cx="' + x.toFixed(1) + '" cy="' + cy + '" r="' + (fs * 0.42).toFixed(1) + '" fill="#10162a" stroke="#f6d98f" stroke-width="4"/>';
    if (rotulos === "abajo") {
      const yb = cy + mitad + fs * 1.6;
      s += '<path d="M ' + x.toFixed(1) + ' ' + (cy + fs * 0.5).toFixed(1) + ' L ' + x.toFixed(1) + ' ' + (yb - fs * 1.05).toFixed(1) + '" stroke="#f3ead8" stroke-opacity="0.35" stroke-width="2"/>';
      s += '<text x="' + x.toFixed(1) + '" y="' + yb.toFixed(1) + '" text-anchor="middle" font-family="Montserrat" font-weight="700" font-size="' + fs + '" fill="#f3ead8">' + n + '</text>';
    } else if (rotulos === "arriba") {
      s += '<text class="' + id + '-t" x="' + x.toFixed(1) + '" y="' + (cy - mitad - fs * 0.6).toFixed(1) + '" text-anchor="middle" font-family="Montserrat" font-weight="700" font-size="' + fs + '" fill="#aab4c8">' + n + '</text>';
    }
    s += "</g>";
  });
  return s;
}
// x de un nodo (por nombre) para alinear otras piezas.
function xNodo(o, nombre) { return o.x0 + NODOS.find((n) => n[0] === nombre)[1] * o.w; }
// Cinta pequeña al pie de las escenas 07 a 11: la franja entera, el nodo activo encendido.
function cinta(sel, activos) {
  const o = { x0: 110, w: 1700, cy: 1000, mitad: 34, id: "ci" + ID.replace(/\W/g, ""), fs: 24, rotulos: "arriba" };
  pinta(sel, '<svg viewBox="0 0 1920 1080" style="position:absolute;inset:0;width:1920px;height:1080px">' + embudo(o) + "</svg>");
  gsap.set($(sel + " ." + o.id + "-rev"), { attr: { width: o.w + 40 } });
  activos.forEach((n) => {
    const i = NODOS.findIndex((x) => x[0] === n);
    const t = $(sel + " ." + o.id + "-n" + i + " text");
    t.setAttribute("fill", "#f6d98f");
    t.setAttribute("font-size", "28");
  });
}
