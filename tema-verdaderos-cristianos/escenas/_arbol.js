// Árboles de Mateo 7:17, 18: uno bueno con frutos y uno seco. Se usan en la escena 03 (la prueba) y en la 16
// (las seis señales juntas). Coordenadas en una caja de 600x720; el pie del tronco está en (300, 700).
const COPA = [[300, 250, 175], [175, 315, 125], [425, 315, 125], [225, 175, 115], [375, 175, 115], [300, 120, 105], [300, 360, 120]];
// Huecos para frutos dentro de la copa (en orden de aparición).
const HUECOS = [[205, 300], [395, 290], [300, 190], [250, 395], [365, 395], [300, 300]];
function arbolDefs(p) {
  return `<defs>
  <linearGradient id="${p}-tronco" x1="0" x2="1"><stop offset="0" stop-color="#5a3d26"/><stop offset="0.55" stop-color="#8a6240"/><stop offset="1" stop-color="#4a3220"/></linearGradient>
  <radialGradient id="${p}-hoja" cx="0.38" cy="0.32" r="0.75"><stop offset="0" stop-color="#7fb069"/><stop offset="0.6" stop-color="#4c8a45"/><stop offset="1" stop-color="#2f5e33"/></radialGradient>
  <radialGradient id="${p}-sombra" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#000" stop-opacity="0.45"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>
  <radialGradient id="${p}-brillo" cx="0.35" cy="0.3" r="0.7"><stop offset="0" stop-color="#fff" stop-opacity="0.55"/><stop offset="0.35" stop-color="#fff" stop-opacity="0"/></radialGradient>
  </defs>`;
}
const TRONCO = "M 270 700 C 278 610 282 540 268 470 C 250 420 210 400 180 380 M 330 700 C 322 610 318 540 330 470 C 345 420 390 400 420 380";
function tronco(p) {
  return `<ellipse cx="300" cy="704" rx="190" ry="22" fill="url(#${p}-sombra)"/>
  <path d="M 262 704 C 274 610 280 530 262 470 C 240 425 200 405 168 386 L 186 372 C 226 392 262 410 290 446 L 300 430 L 310 446 C 338 410 374 392 414 372 L 432 386 C 400 405 360 425 338 470 C 320 530 326 610 338 704 Z" fill="url(#${p}-tronco)"/>
  <path d="M 288 690 C 292 620 292 560 286 500" fill="none" stroke="#a87d55" stroke-width="5" stroke-linecap="round" opacity="0.6"/>`;
}
// Árbol bueno. `frutos` es una lista de colores (uno por hueco); cada fruto lleva la clase fr fr<i>.
function arbolBueno(p, frutos = []) {
  const copa = COPA.map(([x, y, r]) => `<circle cx="${x}" cy="${y}" r="${r}" fill="url(#${p}-hoja)"/>`).join("");
  const luces = COPA.map(([x, y, r]) => `<circle cx="${x - r * 0.25}" cy="${y - r * 0.3}" r="${r * 0.5}" fill="#9fcd7c" opacity="0.18"/>`).join("");
  const fr = frutos.map((c, i) => {
    const [x, y] = HUECOS[i];
    return `<g class="fr fr${i + 1}" transform="translate(${x} ${y})"><circle r="30" fill="${c}" stroke="rgba(0,0,0,0.35)" stroke-width="3"/>` +
      `<circle r="30" fill="url(#${p}-brillo)"/><path d="M 0 -30 C 2 -40 8 -46 14 -48" fill="none" stroke="#4a3220" stroke-width="4" stroke-linecap="round"/></g>`;
  }).join("");
  return `${arbolDefs(p)}<g class="arbol">${tronco(p)}<g class="copa">${copa}${luces}</g>${fr}</g>`;
}
// Árbol seco: el mismo tronco, ramas peladas y grises.
function arbolSeco(p) {
  const ramas = "M 180 380 C 140 340 120 300 110 250 M 150 350 C 110 345 80 330 60 300 M 420 380 C 460 340 480 290 485 240 M 450 350 C 500 350 530 330 548 300 " +
    "M 300 430 C 300 340 290 260 300 150 M 298 300 C 250 260 230 220 225 170 M 300 260 C 350 220 370 180 378 130 M 115 270 C 95 240 98 210 90 190 M 480 270 C 505 240 515 215 520 190";
  return `${arbolDefs(p)}<g class="arbol seco">${tronco(p).replace(`url(#${p}-tronco)`, "#5c5048")}` +
    `<path d="${ramas}" fill="none" stroke="#5c5048" stroke-width="16" stroke-linecap="round"/>` +
    `<path d="${ramas}" fill="none" stroke="#7a6c62" stroke-width="5" stroke-linecap="round" opacity="0.6"/></g>`;
}
