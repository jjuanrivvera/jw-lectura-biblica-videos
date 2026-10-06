// Una cabaña de ramas para el ganado (Sucot), vista de lado. viewBox 0 0 700 430.
function cabanaSVG(p) {
  let hojas = "";
  // Hojas del techo: filas de óvalos verdes con distintos tonos, en posiciones fijas.
  const tonos = ["#5f8f4a", "#739f55", "#4d7a3c", "#86ad62", "#679550"];
  for (let f = 0; f < 5; f++) {
    for (let i = 0; i < 17; i++) {
      const x = 60 + i * 35 + (f % 2 ? 17 : 0), y = 48 + f * 15 + ((i * 7) % 6) - Math.sin((i / 16) * Math.PI) * 18;
      const r = (i * 13 + f * 29) % 50 - 25;
      hojas += `<ellipse cx="${x}" cy="${y}" rx="32" ry="15" fill="${tonos[(i + f) % 5]}" transform="rotate(${r} ${x} ${y})"/>`;
    }
  }
  const oveja = (x, y, s) => `<g transform="translate(${x} ${y}) scale(${s})">
    <ellipse cx="0" cy="0" rx="58" ry="34" fill="#efe7d6"/>
    <circle cx="-38" cy="-18" r="18" fill="#f5eee0"/><circle cx="-10" cy="-26" r="20" fill="#f5eee0"/><circle cx="22" cy="-24" r="19" fill="#f5eee0"/><circle cx="44" cy="-10" r="16" fill="#f5eee0"/>
    <ellipse cx="66" cy="-14" rx="18" ry="14" fill="#3b3129"/><ellipse cx="60" cy="-26" rx="7" ry="4" fill="#3b3129"/>
    <rect x="-36" y="26" width="9" height="30" rx="4" fill="#3b3129"/><rect x="-14" y="28" width="9" height="28" rx="4" fill="#3b3129"/><rect x="18" y="28" width="9" height="28" rx="4" fill="#3b3129"/><rect x="38" y="26" width="9" height="30" rx="4" fill="#3b3129"/></g>`;
  return `<defs><linearGradient id="${p}-palo" x1="0" x2="1"><stop offset="0" stop-color="#6d4c2f"/><stop offset="0.5" stop-color="#9a7048"/><stop offset="1" stop-color="#5b3e25"/></linearGradient>
    <radialGradient id="${p}-sombra" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#000" stop-opacity="0.45"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient></defs>
  <g class="sol"><circle cx="640" cy="40" r="30" fill="#f3c65a"/><g stroke="#f3c65a" stroke-width="6" stroke-linecap="round"><path d="M 640 -8 L 640 0"/><path d="M 588 40 L 596 40"/><path d="M 604 4 L 610 10"/></g></g>
  <path d="M 0 380 L 700 380 L 700 430 L 0 430 Z" fill="#8a6a45"/>
  <ellipse cx="350" cy="386" rx="300" ry="30" fill="url(#${p}-sombra)" class="sombra"/>
  <g class="palos"><rect x="80" y="100" width="18" height="285" rx="5" fill="url(#${p}-palo)"/><rect x="330" y="92" width="18" height="293" rx="5" fill="url(#${p}-palo)"/><rect x="590" y="100" width="18" height="285" rx="5" fill="url(#${p}-palo)"/>
  <rect x="60" y="88" width="570" height="14" rx="6" fill="url(#${p}-palo)" transform="rotate(-1 345 95)"/></g>
  <g class="techo">${hojas}</g>
  <g class="ovejas">${oveja(200, 320, 1)}${oveja(440, 330, 0.9)}${oveja(330, 350, 0.55)}</g>`;
}
