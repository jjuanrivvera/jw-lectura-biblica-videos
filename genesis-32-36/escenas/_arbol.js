// Un árbol grande (encina), con suelo en corte opcional. viewBox 0 0 800 820; suelo en y = 600.
function arbolSVG(p, conSuelo) {
  const verdes = ["#3f6b35", "#4f7d3f", "#5d8b48", "#6a9a52", "#46743a"];
  // Copa: círculos en posiciones fijas que forman una masa redondeada.
  const C = [[400, 190, 120], [290, 230, 100], [510, 230, 100], [220, 310, 80], [580, 310, 80], [330, 320, 95], [470, 320, 95], [400, 110, 85], [310, 140, 75], [490, 140, 75], [400, 280, 110], [250, 390, 55], [550, 390, 55], [400, 380, 70]];
  let copa = "";
  C.forEach(([x, y, r], i) => { copa += `<circle cx="${x}" cy="${y}" r="${r}" fill="${verdes[i % 5]}"/>`; });
  C.forEach(([x, y, r], i) => { copa += `<circle cx="${x - r * 0.25}" cy="${y - r * 0.3}" r="${r * 0.45}" fill="#86b067" opacity="0.35"/>`; });
  let s = `<defs><linearGradient id="${p}-tronco" x1="0" x2="1"><stop offset="0" stop-color="#4a3322"/><stop offset="0.5" stop-color="#7a5636"/><stop offset="1" stop-color="#3d2a1b"/></linearGradient></defs>`;
  if (conSuelo) s += `<rect x="0" y="600" width="800" height="220" fill="#5a4330"/><rect x="0" y="600" width="800" height="14" fill="#6d8a45"/>`;
  else s += `<ellipse cx="400" cy="604" rx="300" ry="26" fill="#000" opacity="0.25"/>`;
  s += `<path d="M 370 606 C 372 520 360 440 330 380 L 360 372 C 385 420 392 460 398 500 C 405 450 420 410 450 370 L 478 382 C 445 440 432 520 436 606 Z" fill="url(#${p}-tronco)"/>`;
  s += `<g class="copa">${copa}</g>`;
  if (conSuelo) {
    s += `<path d="M 400 606 C 380 650 340 680 300 700 M 420 606 C 440 660 500 690 540 700" stroke="#3d2a1b" stroke-width="10" fill="none" stroke-linecap="round"/>`;
    s += `<g class="enterrado"><g transform="translate(-230 -700) scale(2) translate(115 350)"><path d="M 150 700 C 180 660 280 660 310 700 C 300 760 160 760 150 700 Z" fill="#3b2c1f"/>` +
      `<g transform="translate(200 700)"><circle cx="0" cy="-26" r="11" fill="#b99a6a"/><path d="M -14 -14 L 14 -14 L 10 22 L -10 22 Z" fill="#a8895a"/></g>` +
      `<g transform="translate(250 706)"><circle cx="0" cy="-22" r="10" fill="#9c7f55"/><path d="M -12 -12 L 12 -12 L 9 18 L -9 18 Z" fill="#8c7049"/></g>` +
      `<circle cx="282" cy="712" r="10" fill="none" stroke="#e9bf60" stroke-width="5"/><circle cx="172" cy="716" r="9" fill="none" stroke="#e9bf60" stroke-width="5"/></g></g>`;
  }
  return s;
}
