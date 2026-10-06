// Paisaje de Génesis 1 visto de lado, como lo vería alguien en la Tierra: cielo, capa de nubes, mar en corte
// (con el fondo visible para los peces), tierra que emerge a la derecha con su vegetación, astros y aves.
// Las escenas 02 y 05 a 09 y 11 lo incluyen y animan solo las capas que les tocan.
// Todo lo "aleatorio" sale de un generador con semilla fija: cada cuadro es idéntico en cada render.
function azar(semilla) {
  let s = semilla >>> 0;
  return () => ((s = (s * 1664525 + 1013904223) >>> 0) / 4294967296);
}
const HORIZ = 640;
// Perfil de la tierra (x, y) de izquierda a derecha; el borde izquierdo baja al fondo del mar.
const PERFIL = [[1010, 1080], [1090, 800], [1160, 690], [1240, 620], [1330, 585], [1420, 575], [1510, 548], [1600, 520],
  [1690, 530], [1780, 505], [1860, 520], [1940, 510]];
function alturaTierra(x) {
  for (let i = 0; i < PERFIL.length - 1; i++) {
    const [x0, y0] = PERFIL[i], [x1, y1] = PERFIL[i + 1];
    if (x >= x0 && x <= x1) { const k = (x - x0) / (x1 - x0), s = k * k * (3 - 2 * k); return y0 + (y1 - y0) * s; }
  }
  return PERFIL[PERFIL.length - 1][1];
}
function curva(pts) {
  // Catmull-Rom a Bézier: un contorno suave que pasa por todos los puntos.
  let d = `M ${pts[0][0]} ${pts[0][1]}`;
  for (let i = 0; i < pts.length - 1; i++) {
    const p0 = pts[i - 1] || pts[i], p1 = pts[i], p2 = pts[i + 1], p3 = pts[i + 2] || p2;
    d += ` C ${(p1[0] + (p2[0] - p0[0]) / 6).toFixed(1)} ${(p1[1] + (p2[1] - p0[1]) / 6).toFixed(1)} ${(p2[0] - (p3[0] - p1[0]) / 6).toFixed(1)} ${(p2[1] - (p3[1] - p1[1]) / 6).toFixed(1)} ${p2[0]} ${p2[1]}`;
  }
  return d;
}
function nube(cx, cy, ancho, alto, r, n, claro) {
  let s = "";
  for (let i = 0; i < n; i++) {
    const x = cx + (r() - 0.5) * ancho, y = cy + (r() - 0.5) * alto * 0.6, rr = alto * (0.35 + r() * 0.45);
    s += `<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="${rr.toFixed(1)}" fill="url(#${claro})"/>`;
  }
  return s;
}
function arbol(x, y, h, r, fruta) {
  const c = h * 0.42;
  let s = `<path d="M ${x - h * 0.035} ${y} L ${x - h * 0.02} ${y - h * 0.55} L ${x + h * 0.02} ${y - h * 0.55} L ${x + h * 0.035} ${y} Z" fill="#5b3e26"/>`;
  const copas = [[0, -0.62, 0.34], [-0.2, -0.5, 0.26], [0.2, -0.52, 0.27], [-0.08, -0.8, 0.26], [0.12, -0.76, 0.24]];
  copas.forEach(([dx, dy, rr], i) => {
    s += `<circle cx="${(x + dx * h).toFixed(1)}" cy="${(y + dy * h).toFixed(1)}" r="${(rr * h).toFixed(1)}" fill="url(#${ID}-copa${i % 2})"/>`;
  });
  s += `<circle cx="${(x - 0.06 * h).toFixed(1)}" cy="${(y - 0.72 * h).toFixed(1)}" r="${(0.13 * h).toFixed(1)}" fill="rgba(210,240,150,0.28)"/>`;
  if (fruta) for (let i = 0; i < 7; i++) {
    const a = r() * Math.PI * 2, d = r() * c * 0.8;
    s += `<circle cx="${(x + Math.cos(a) * d).toFixed(1)}" cy="${(y - 0.62 * h + Math.sin(a) * d * 0.8).toFixed(1)}" r="${(h * 0.035).toFixed(1)}" fill="#e2573a"/>`;
  }
  return s;
}
function pez(x, y, e, col) {
  return `<g transform="translate(${x.toFixed(1)} ${y.toFixed(1)}) scale(${e.toFixed(2)})"><path d="M -30 0 C -18 -14 10 -14 22 0 C 10 14 -18 14 -30 0 Z" fill="${col}"/><path d="M 20 0 L 36 -11 L 33 0 L 36 11 Z" fill="${col}"/><circle cx="-19" cy="-3" r="2.6" fill="#10202c"/></g>`;
}
function ave(x, y, e) {
  return `<path d="M ${x - 22 * e} ${y - 4 * e} Q ${x - 10 * e} ${y - 14 * e} ${x} ${y} Q ${x + 10 * e} ${y - 14 * e} ${x + 22 * e} ${y - 4 * e}" fill="none" stroke="#1b2733" stroke-width="${(3.4 * e).toFixed(1)}" stroke-linecap="round"/>`;
}

function paisaje(sel) {
  const r = azar(7);
  const g = (id) => `${ID}-${id}`;
  let estrellas = "";
  for (let i = 0; i < 140; i++) {
    const x = r() * 1920, y = r() * 600, rr = 0.8 + r() * 2.2;
    estrellas += `<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="${rr.toFixed(2)}" fill="#fff8e6" opacity="${(0.35 + r() * 0.6).toFixed(2)}"/>`;
  }
  let nubesAltas = "", manto = "";
  for (let i = 0; i < 9; i++) nubesAltas += nube(100 + i * 220, 150 + (i % 3) * 40, 260, 110, r, 7, g("nubeb"));
  // El manto: un techo continuo de nubes con los bordes de arriba y de abajo abultados.
  for (let x = -60; x < 2000; x += 46) {
    manto += `<circle cx="${x + (r() - 0.5) * 30}" cy="${(158 + r() * 26).toFixed(1)}" r="${(40 + r() * 38).toFixed(1)}" fill="#2b3239"/>`;
    manto += `<circle cx="${x + (r() - 0.5) * 30}" cy="${(424 + r() * 30).toFixed(1)}" r="${(44 + r() * 46).toFixed(1)}" fill="#2b3239"/>`;
  }
  let pliegues = "";
  for (let i = 0; i < 26; i++) {
    const x = r() * 1920, y = 210 + r() * 200;
    pliegues += `<ellipse cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" rx="${(120 + r() * 160).toFixed(1)}" ry="${(26 + r() * 30).toFixed(1)}" fill="${r() > 0.5 ? "#3a434b" : "#20272d"}" opacity="0.8"/>`;
  }
  let rayos = "";
  for (let i = 0; i < 7; i++) {
    const x0 = 1560 + i * 18, x1 = 520 + i * 210;
    rayos += `<path d="M ${x0} 140 L ${x0 + 26} 140 L ${x1 + 130} 520 L ${x1} 520 Z" fill="#fff3cf" opacity="${(0.10 + r() * 0.08).toFixed(2)}"/>`;
  }
  let hierba = "", plantas = "", arboles = "";
  for (let x = 1200; x < 1930; x += 9) {
    const y = alturaTierra(x) + 2, h = 10 + r() * 16;
    hierba += `<path d="M ${x} ${y} q ${(r() * 6 - 3).toFixed(1)} ${(-h / 2).toFixed(1)} ${(r() * 8 - 4).toFixed(1)} ${(-h).toFixed(1)}" stroke="${r() > 0.5 ? "#79b957" : "#5e9e44"}" stroke-width="3.2" fill="none" stroke-linecap="round"/>`;
  }
  [1275, 1390, 1470, 1560, 1655, 1745, 1830, 1900].forEach((x, i) => {
    const y = alturaTierra(x) + 4;
    plantas += `<g class="pz-mata"><ellipse cx="${x}" cy="${y - 14}" rx="${26 + (i % 3) * 6}" ry="18" fill="url(#${g("copa1")})"/><ellipse cx="${x - 10}" cy="${y - 22}" rx="14" ry="10" fill="rgba(200,240,140,0.3)"/>` +
      (i % 2 ? `<circle cx="${x + 8}" cy="${y - 20}" r="3.4" fill="#f4e3a0"/><circle cx="${x - 12}" cy="${y - 12}" r="3.4" fill="#f4e3a0"/>` : "") + `</g>`;
  });
  [[1330, 150, 0], [1520, 200, 1], [1610, 160, 1], [1720, 230, 0], [1850, 180, 1]].forEach(([x, h, f]) => {
    arboles += `<g class="pz-arbol">${arbol(x, alturaTierra(x) + 6, h, r, f)}</g>`;
  });
  let peces = "";
  const colores = ["#f2b35a", "#7cc6d8", "#f08a6a", "#c9e27a"];
  for (let k = 0; k < 4; k++) {
    let banco = "";
    const cx = 160 + k * 230, cy = 760 + (k % 2) * 120;
    for (let i = 0; i < 9; i++) banco += pez(cx + (r() - 0.5) * 180, cy + (r() - 0.5) * 70, 0.7 + r() * 0.4, colores[k]);
    peces += `<g class="pz-banco pz-banco${k}">${banco}</g>`;
  }
  peces += `<g class="pz-ballena"><path d="M 610 930 C 660 880 820 880 900 915 C 930 928 960 930 990 912 L 1010 890 L 1004 930 L 1024 960 L 990 944 C 950 962 900 972 820 972 C 720 972 640 960 610 930 Z" fill="#3f6a8a"/><path d="M 640 944 C 720 962 820 966 900 950" stroke="#b9d4e0" stroke-width="5" fill="none" opacity="0.6"/><circle cx="660" cy="920" r="4" fill="#10202c"/></g>`;
  let aves = "";
  for (let k = 0; k < 3; k++) {
    let bandada = "";
    for (let i = 0; i < 7; i++) bandada += ave(260 + k * 330 + (r() - 0.5) * 220, 250 + k * 40 + (r() - 0.5) * 90, 0.8 + r() * 0.6);
    aves += `<g class="pz-bandada pz-bandada${k}">${bandada}</g>`;
  }
  const tierra = curva(PERFIL) + " L 1940 1080 Z";
  let olas = "";
  for (let i = 0; i < 4; i++) {
    let d = `M -60 ${HORIZ + 8 + i * 26}`;
    for (let x = -60; x < 2000; x += 80) d += ` q 20 -${(9 - i * 2).toFixed(0)} 40 0 t 40 0`;
    olas += `<path class="pz-ola" d="${d}" fill="none" stroke="rgba(220,240,255,${(0.42 - i * 0.08).toFixed(2)})" stroke-width="${4 - i * 0.7}" stroke-linecap="round"/>`;
  }
  $(sel).innerHTML = `<svg viewBox="0 0 1920 1080" width="1920" height="1080" style="position:absolute;left:0;top:0">
  <defs>
    <linearGradient id="${g("cnoche")}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#05080d"/><stop offset="1" stop-color="#101820"/></linearGradient>
    <linearGradient id="${g("cgris")}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6f7880" stop-opacity="0"/><stop offset="0.3" stop-color="#7d868c"/><stop offset="1" stop-color="#a3abae"/></linearGradient>
    <linearGradient id="${g("cazul")}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3f7fc4"/><stop offset="0.7" stop-color="#9cc7ea"/><stop offset="1" stop-color="#e4eef2"/></linearGradient>
    <linearGradient id="${g("mar")}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2c6f9a" stop-opacity="0.82"/><stop offset="1" stop-color="#0b2436" stop-opacity="0.96"/></linearGradient>
    <linearGradient id="${g("maroscuro")}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0d1a24"/><stop offset="1" stop-color="#03070b"/></linearGradient>
    <linearGradient id="${g("tierra")}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8a6a45"/><stop offset="0.35" stop-color="#6b4f33"/><stop offset="1" stop-color="#3b2a1c"/></linearGradient>
    <radialGradient id="${g("nubeb")}"><stop offset="0" stop-color="#ffffff" stop-opacity="0.95"/><stop offset="0.7" stop-color="#e7eef3" stop-opacity="0.85"/><stop offset="1" stop-color="#d4dde4" stop-opacity="0"/></radialGradient>
    <radialGradient id="${g("mantog")}"><stop offset="0" stop-color="#3b434b"/><stop offset="0.75" stop-color="#2a3138" stop-opacity="0.95"/><stop offset="1" stop-color="#20262c" stop-opacity="0"/></radialGradient>
    <radialGradient id="${g("copa0")}" cx="0.4" cy="0.35"><stop offset="0" stop-color="#8fcf5e"/><stop offset="1" stop-color="#3d7a33"/></radialGradient>
    <radialGradient id="${g("copa1")}" cx="0.4" cy="0.35"><stop offset="0" stop-color="#a6d86a"/><stop offset="1" stop-color="#4f8c3a"/></radialGradient>
    <radialGradient id="${g("sol")}"><stop offset="0" stop-color="#fffbe6"/><stop offset="0.45" stop-color="#ffe7a0"/><stop offset="1" stop-color="#ffc54d"/></radialGradient>
    <radialGradient id="${g("halo")}"><stop offset="0" stop-color="#fff2c0" stop-opacity="0.8"/><stop offset="1" stop-color="#fff2c0" stop-opacity="0"/></radialGradient>
    <linearGradient id="${g("difusa")}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f4ecd6" stop-opacity="0"/><stop offset="0.28" stop-color="#f4ecd6" stop-opacity="0.55"/><stop offset="0.55" stop-color="#f4ecd6" stop-opacity="0.18"/><stop offset="1" stop-color="#f4ecd6" stop-opacity="0"/></linearGradient>
    <filter id="${g("blur")}" x="-10%" y="-40%" width="120%" height="180%"><feGaussianBlur stdDeviation="14"/></filter>
    <filter id="${g("blur2")}" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="3"/></filter>
    <clipPath id="${g("agua")}"><rect x="0" y="${HORIZ}" width="1920" height="${1080 - HORIZ}"/></clipPath>
  </defs>
  <rect class="pz-cielo-noche" width="1920" height="1080" fill="url(#${g("cnoche")})"/>
  <g class="pz-espacio"><rect width="1920" height="1080" fill="#04070c"/><g>${estrellas}</g>
    <circle cx="1620" cy="120" r="150" fill="url(#${g("halo")})"/><circle cx="1620" cy="120" r="50" fill="url(#${g("sol")})"/></g>
  <rect class="pz-cielo-gris" y="330" width="1920" height="750" fill="url(#${g("cgris")})"/>
  <rect class="pz-cielo-azul" width="1920" height="1080" fill="url(#${g("cazul")})"/>
  <g class="pz-estrellas">${estrellas}</g>
  <g class="pz-sol"><circle cx="1620" cy="120" r="170" fill="url(#${g("halo")})"/><circle cx="1620" cy="120" r="50" fill="url(#${g("sol")})"/></g>
  <g class="pz-luna"><circle cx="420" cy="170" r="46" fill="#eef0ea"/><circle cx="406" cy="160" r="9" fill="#d4d8d0"/><circle cx="434" cy="184" r="6" fill="#d4d8d0"/><circle cx="428" cy="152" r="4" fill="#d4d8d0"/></g>
  <g class="pz-nubes-altas" filter="url(#${g("blur2")})">${nubesAltas}</g>
  <g class="pz-bandadas">${aves}</g>
  <g class="pz-tierra"><path d="${tierra}" fill="url(#${g("tierra")})"/><path d="${curva(PERFIL)}" fill="none" stroke="#a3845a" stroke-width="5"/>
    <g class="pz-hierba">${hierba}</g><g class="pz-matas">${plantas}</g><g class="pz-arboles">${arboles}</g></g>
  <g class="pz-mar"><rect x="0" y="${HORIZ}" width="1920" height="${1080 - HORIZ}" fill="url(#${g("mar")})"/>
    <rect class="pz-mar-oscuro" x="0" y="${HORIZ}" width="1920" height="${1080 - HORIZ}" fill="url(#${g("maroscuro")})"/>
    <g clip-path="url(#${g("agua")})"><g class="pz-peces">${peces}</g></g>
    <g class="pz-olas">${olas}</g></g>
  <g class="pz-manto"><g class="pz-manto-cuerpo" filter="url(#${g("blur")})"><rect x="-60" y="170" width="2040" height="270" fill="#2b3239"/>${manto}${pliegues}</g>
    <g class="pz-rayos" filter="url(#${g("blur")})">${rayos}</g></g>
  <rect class="pz-difusa" y="300" width="1920" height="780" fill="url(#${g("difusa")})"/>
</svg>`;
}
