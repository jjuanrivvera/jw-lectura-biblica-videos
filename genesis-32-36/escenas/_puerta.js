// La puerta de una ciudad amurallada, vista de frente (viewBox 0 0 1100 860).
// Se usa en Génesis 19 (Lot sentado a la puerta) y en Génesis 23 (la compra ante testigos).
// `p` es un prefijo para que los ids de degradados no choquen entre escenas.
function puertaSVG(p) {
  const bloques = (x0, y0, w, h, alto = 34, ancho = 78) => {
    let s = "";
    for (let y = y0, fila = 0; y < y0 + h - 2; y += alto, fila++) {
      const off = fila % 2 ? ancho / 2 : 0;
      for (let x = x0 - off; x < x0 + w; x += ancho) {
        const xa = Math.max(x, x0), xb = Math.min(x + ancho, x0 + w);
        if (xb - xa > 6) s += `<rect x="${xa + 2}" y="${y + 2}" width="${xb - xa - 4}" height="${Math.min(alto, y0 + h - y) - 4}" rx="3"/>`;
      }
    }
    return s;
  };
  const almenas = (x0, x1, y, paso = 44) => {
    let s = "";
    for (let x = x0; x < x1 - 10; x += paso) s += `<rect x="${x}" y="${y - 26}" width="${paso * 0.58}" height="28" rx="2"/>`;
    return s;
  };
  const toldo = (x, y, w, c1, c2) => {
    let s = `<g class="toldo"><rect x="${x + 8}" y="${y + 40}" width="8" height="${86}" fill="#5b4631"/><rect x="${x + w - 16}" y="${y + 40}" width="8" height="86" fill="#5b4631"/>`;
    const n = 6;
    for (let i = 0; i < n; i++) s += `<path d="M ${x + (i * w) / n} ${y} L ${x + ((i + 1) * w) / n} ${y} L ${x + ((i + 1) * w) / n + 6} ${y + 44} L ${x + (i * w) / n + 6} ${y + 44} Z" fill="${i % 2 ? c2 : c1}"/>`;
    s += `<rect x="${x + 10}" y="${y + 104}" width="${w - 14}" height="22" rx="4" fill="#7a5c3c"/>`;
    s += `<circle cx="${x + 34}" cy="${y + 98}" r="10" fill="#d9a441"/><circle cx="${x + 56}" cy="${y + 99}" r="9" fill="#a8c46a"/><circle cx="${x + w - 40}" cy="${y + 97}" r="11" fill="#c96a3c"/></g>`;
    return s;
  };
  return `
  <defs>
    <linearGradient id="${p}-muro" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9c8d73"/><stop offset="1" stop-color="#6d624f"/></linearGradient>
    <linearGradient id="${p}-torre" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#a99a7e"/><stop offset="0.7" stop-color="#8d7f66"/><stop offset="1" stop-color="#6f644f"/></linearGradient>
    <linearGradient id="${p}-hueco" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#15110d"/><stop offset="0.75" stop-color="#3a2b1c"/><stop offset="1" stop-color="#e2b565" stop-opacity="0.85"/></linearGradient>
    <linearGradient id="${p}-suelo" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4a4235"/><stop offset="1" stop-color="#2b2a28"/></linearGradient>
    <linearGradient id="${p}-hoja" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#6b4a2c"/><stop offset="1" stop-color="#4a321d"/></linearGradient>
  </defs>
  <path d="M 0 640 L 1100 640 L 1100 860 L 0 860 Z" fill="url(#${p}-suelo)"/>
  <g stroke="#5a5244" stroke-width="2" opacity="0.5"><line x1="550" y1="640" x2="80" y2="860"/><line x1="550" y1="640" x2="1020" y2="860"/><line x1="0" y1="720" x2="1100" y2="720"/><line x1="0" y1="800" x2="1100" y2="800"/></g>
  <rect x="0" y="210" width="1100" height="430" fill="url(#${p}-muro)"/>
  <g fill="#000" opacity="0.13">${bloques(0, 210, 300, 430)}${bloques(800, 210, 300, 430)}</g>
  <g fill="#9c8d73">${almenas(0, 300, 210)}${almenas(800, 1100, 210)}</g>
  <rect x="290" y="120" width="190" height="520" fill="url(#${p}-torre)"/>
  <rect x="620" y="120" width="190" height="520" fill="url(#${p}-torre)"/>
  <g fill="#000" opacity="0.12">${bloques(290, 120, 190, 520, 36, 64)}${bloques(620, 120, 190, 520, 36, 64)}</g>
  <g fill="#a99a7e">${almenas(290, 480, 120, 40)}${almenas(620, 810, 120, 40)}</g>
  <g fill="#1d1812"><rect x="372" y="200" width="18" height="54" rx="9"/><rect x="702" y="200" width="18" height="54" rx="9"/><rect x="372" y="330" width="18" height="54" rx="9"/><rect x="702" y="330" width="18" height="54" rx="9"/></g>
  <rect x="480" y="250" width="140" height="390" fill="url(#${p}-muro)"/>
  <path d="M 488 640 L 488 400 A 62 62 0 0 1 612 400 L 612 640 Z" fill="url(#${p}-hueco)"/>
  <path d="M 488 400 A 62 62 0 0 1 612 400" fill="none" stroke="#5e5443" stroke-width="10"/>
  <path d="M 488 640 L 488 404 L 446 420 L 446 648 Z" fill="url(#${p}-hoja)" stroke="#2e1f12" stroke-width="3"/>
  <path d="M 612 640 L 612 404 L 654 420 L 654 648 Z" fill="url(#${p}-hoja)" stroke="#2e1f12" stroke-width="3"/>
  <g fill="#3a2a1a"><circle cx="466" cy="530" r="5"/><circle cx="634" cy="530" r="5"/></g>
  <g class="bancos"><rect x="180" y="604" width="104" height="30" rx="6" fill="#b8aa8e"/><rect x="186" y="632" width="92" height="12" fill="#7d725e"/>
  <rect x="816" y="604" width="104" height="30" rx="6" fill="#b8aa8e"/><rect x="822" y="632" width="92" height="12" fill="#7d725e"/></g>
  ${toldo(24, 500, 150, "#c96a3c", "#e8c79a")}
  ${toldo(930, 500, 150, "#4f7aa8", "#e8c79a")}`;
}
