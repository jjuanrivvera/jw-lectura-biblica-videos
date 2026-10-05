// El árbol de Daniel 4, dibujado en un viewBox de 1000x1000. Lo usan varias escenas.
// Partes con clase propia para animarlas por separado:
//   .suelo  .raices  .alto (tronco alto + copa)  .copa  .hojas-n  .fruto  .ave  .animal
//   .tocon  .cara (cara del corte, con anillos)  .corte (línea del hachazo)
//   .banda-h (hierro)  .banda-c (cobre)  .brote  .rayo (luz del vigilante)
// p: prefijo único para los ids de los degradados (cada escena lleva el suyo).
function arbolSVG(p) {
  const copas = [
    [500, 300, 250, 0], [330, 380, 170, 1], [670, 380, 170, 1], [400, 220, 160, 2], [610, 215, 165, 2],
    [500, 160, 150, 0], [250, 470, 120, 2], [750, 470, 120, 2], [420, 450, 150, 0], [590, 450, 150, 1],
  ];
  const tonos = [["#6fae5c", "#2f6b3a"], ["#5f9f52", "#285e33"], ["#80bd68", "#357545"]];
  const frutos = [[380, 300], [560, 250], [640, 400], [450, 420], [300, 450], [700, 300], [520, 360], [430, 200], [760, 470], [240, 400], [600, 140], [500, 480]];
  const aves = [[420, 120], [600, 90], [700, 200], [300, 240], [520, 60]];
  const anillos = [56, 44, 32, 20, 9].map((r) => `<ellipse cx="500" cy="760" rx="${r}" ry="${(r * 0.28).toFixed(1)}" fill="none" stroke="#9a6a3c" stroke-width="2.4" opacity="0.8"/>`).join("");
  return `
<svg viewBox="0 0 1000 1000" xmlns="http://www.w3.org/2000/svg">
<defs>
  <linearGradient id="${p}-tr" x1="0" x2="1"><stop offset="0" stop-color="#4a2f1c"/><stop offset="0.45" stop-color="#8a5a35"/><stop offset="1" stop-color="#3b2416"/></linearGradient>
  <linearGradient id="${p}-su" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4f7d3c"/><stop offset="1" stop-color="#22371f"/></linearGradient>
  <linearGradient id="${p}-fe" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e3e8ec"/><stop offset="0.35" stop-color="#9aa4ad"/><stop offset="0.7" stop-color="#5d6770"/><stop offset="1" stop-color="#3b434a"/></linearGradient>
  <linearGradient id="${p}-cu" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f5c28f"/><stop offset="0.35" stop-color="#cf7d45"/><stop offset="0.7" stop-color="#8f4a22"/><stop offset="1" stop-color="#5e2e14"/></linearGradient>
  <radialGradient id="${p}-cara" cx="0.5" cy="0.45" r="0.6"><stop offset="0" stop-color="#f0cf96"/><stop offset="1" stop-color="#b98450"/></radialGradient>
  <radialGradient id="${p}-luz" cx="0.5" cy="0" r="1"><stop offset="0" stop-color="#fff6d8" stop-opacity="0.9"/><stop offset="1" stop-color="#fff6d8" stop-opacity="0"/></radialGradient>
  ${tonos.map(([a, b], i) => `<radialGradient id="${p}-h${i}" cx="0.38" cy="0.32" r="0.75"><stop offset="0" stop-color="${a}"/><stop offset="1" stop-color="${b}"/></radialGradient>`).join("")}
  <linearGradient id="${p}-mg" x1="0" x2="1"><stop offset="0" stop-color="#000"/><stop offset="0.18" stop-color="#fff"/><stop offset="0.82" stop-color="#fff"/><stop offset="1" stop-color="#000"/></linearGradient>
  <mask id="${p}-ms"><rect x="-10" y="0" width="1020" height="1010" fill="url(#${p}-mg)"/></mask>
  <linearGradient id="${p}-bro" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#5c8f3e"/><stop offset="1" stop-color="#b5e07f"/></linearGradient>
</defs>
<g class="rayo"><ellipse cx="500" cy="-40" rx="520" ry="560" fill="url(#${p}-luz)" opacity="0.75"/></g>
<g class="suelo" mask="url(#${p}-ms)">
  <path d="M 0 900 C 220 870 380 880 500 875 C 650 870 800 880 1000 895 L 1000 1000 L 0 1000 Z" fill="url(#${p}-su)"/>
  ${[60, 140, 230, 330, 640, 720, 820, 920].map((x, i) => `<path d="M ${x} ${905 - (i % 3) * 4} l 8 -26 l 6 24 l 8 -30 l 6 32" fill="none" stroke="#7fb05f" stroke-width="4" stroke-linecap="round"/>`).join("")}
</g>
<g class="raices" fill="none" stroke="#5a3a22" stroke-width="16" stroke-linecap="round">
  <path d="M 450 900 C 420 930 370 935 330 960"/><path d="M 550 900 C 590 930 640 930 680 958"/><path d="M 485 905 C 480 940 470 960 455 985"/><path d="M 520 905 C 528 945 540 965 560 985"/>
</g>
<g class="alto">
  <path d="M 452 770 C 456 640 448 560 430 470 L 392 400 L 412 392 L 452 452 C 462 400 470 330 476 260 L 524 260 C 530 330 538 400 548 452 L 588 392 L 608 400 L 570 470 C 552 560 544 640 548 770 Z" fill="url(#${p}-tr)"/>
  <g class="copa">
    <ellipse cx="500" cy="545" rx="300" ry="55" fill="#0b1a12" opacity="0.35"/>
    ${copas.map(([x, y, r, k], i) => `<circle class="hojas-${i}" cx="${x}" cy="${y}" r="${r}" fill="url(#${p}-h${k})"/>`).join("")}
    ${copas.map(([x, y, r], i) => `<circle cx="${x - r * 0.25}" cy="${y - r * 0.3}" r="${r * 0.35}" fill="#a6d684" opacity="0.18"/>`).join("")}
    ${frutos.map(([x, y]) => `<g class="fruto"><circle cx="${x}" cy="${y}" r="13" fill="#e8a33c"/><circle cx="${x - 4}" cy="${y - 4}" r="4" fill="#fde2a6"/></g>`).join("")}
  </g>
  <g class="aves" fill="none" stroke="#f4ecd8" stroke-width="9" stroke-linecap="round" stroke-linejoin="round">
    ${aves.map(([x, y]) => `<path class="ave" d="M ${x - 34} ${y} q 17 -22 34 0 q 17 -22 34 0"/>`).join("")}
  </g>
</g>
<g class="animales">
  <g class="animal a1" fill="#c9a77c"><ellipse cx="230" cy="852" rx="62" ry="30"/><circle cx="292" cy="826" r="20"/><path d="M 282 812 q -10 -14 4 -22 M 300 812 q 12 -12 0 -22" fill="none" stroke="#efe2c8" stroke-width="6" stroke-linecap="round"/><rect x="186" y="868" width="10" height="34" rx="4"/><rect x="262" y="868" width="10" height="34" rx="4"/></g>
  <g class="animal a2" fill="#e6dccb"><ellipse cx="770" cy="858" rx="52" ry="30"/><circle cx="716" cy="838" r="19"/><rect x="738" y="874" width="10" height="28" rx="4"/><rect x="796" y="874" width="10" height="28" rx="4"/></g>
</g>
<g class="tocon">
  <path d="M 446 760 L 554 760 C 552 820 556 870 566 905 L 434 905 C 444 870 448 820 446 760 Z" fill="url(#${p}-tr)"/>
  <g class="cara"><ellipse cx="500" cy="760" rx="54" ry="15" fill="url(#${p}-cara)"/>${anillos}</g>
</g>
<g class="banda-h"><rect x="436" y="800" width="128" height="30" rx="8" fill="url(#${p}-fe)" stroke="#2b3136" stroke-width="3"/>${[456, 484, 516, 544].map((x) => `<circle cx="${x}" cy="815" r="4.5" fill="#2b3136"/>`).join("")}</g>
<g class="banda-c"><rect x="432" y="850" width="136" height="30" rx="8" fill="url(#${p}-cu)" stroke="#4a230f" stroke-width="3"/>${[452, 482, 518, 548].map((x) => `<circle cx="${x}" cy="865" r="4.5" fill="#4a230f"/>`).join("")}</g>
<path class="corte" d="M 380 762 L 620 758" fill="none" stroke="#ef7b4f" stroke-width="8" stroke-linecap="round" stroke-dasharray="4 18"/>
<g class="brote">
  <path class="tallo" d="M 500 758 C 498 700 506 650 500 590 C 496 540 504 500 500 455" fill="none" stroke="url(#${p}-bro)" stroke-width="14" stroke-linecap="round"/>
  <path d="M 500 650 C 540 630 580 640 600 610 C 560 600 520 610 500 650 Z" fill="#8fcf6a"/>
  <path d="M 502 590 C 460 575 430 585 404 555 C 450 545 485 560 502 590 Z" fill="#7fc25d"/>
  <path d="M 500 520 C 535 500 565 505 585 478 C 548 470 515 485 500 520 Z" fill="#a3dc7c"/>
  <path d="M 500 470 C 470 450 470 420 488 398 C 508 420 512 448 500 470 Z" fill="#b8e88c"/>
</g>
</svg>`;
}
