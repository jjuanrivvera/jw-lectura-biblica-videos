// El arca dibujada de lado, con un poco de perspectiva para que se vea el ancho.
// Proporciones de Génesis 6:15: el largo es diez veces el alto (300 a 30 codos) y seis veces el ancho.
// arcaSVG(x, y, L, o) devuelve el marcado: (x, y) es la esquina superior izquierda del costado; L, el largo en px.
// Clases para animar: .ar-cubiertas (las dos cubiertas intermedias), .ar-puerta (la hoja de la puerta, gira sobre su
// borde izquierdo), .ar-hueco (el vano de la puerta), .ar-tsohar (la abertura corrida bajo el techo), .ar-sombra.
function arcaSVG(x, y, L, o = {}) {
  const H = L / 10, dx = L / 10, dy = -L / 18;
  const g = (n) => `${ID}-ar${o.k || ""}-${n}`;
  let tablas = "";
  for (let i = 1; i < 9; i++) {
    const yy = y + (H * i) / 9;
    tablas += `<path d="M ${x} ${yy.toFixed(1)} L ${x + L} ${yy.toFixed(1)}" stroke="rgba(40,24,12,0.55)" stroke-width="${Math.max(1.2, L / 700).toFixed(1)}"/>`;
  }
  let juntas = "";
  for (let i = 1; i < 14; i++) {
    const xx = x + (L * i) / 14 + ((i % 2) * L) / 60;
    const fila = i % 3;
    juntas += `<path d="M ${xx.toFixed(1)} ${(y + (H * fila) / 3 + 3).toFixed(1)} L ${xx.toFixed(1)} ${(y + (H * (fila + 1)) / 3 - 3).toFixed(1)}" stroke="rgba(40,24,12,0.35)" stroke-width="${Math.max(1, L / 900).toFixed(1)}"/>`;
  }
  const pX = x + L * 0.62, pW = L * 0.05, pY = y + H * 0.36, pH = H * 0.6;
  const ts = H * 0.07;
  return `<g class="ar ar${o.k || ""}">
  <defs>
    <linearGradient id="${g("fr")}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8a6440"/><stop offset="0.55" stop-color="#6d4b2c"/><stop offset="1" stop-color="#4a3019"/></linearGradient>
    <linearGradient id="${g("te")}" x1="0" y1="1" x2="0.3" y2="0"><stop offset="0" stop-color="#a47c53"/><stop offset="1" stop-color="#c49d6d"/></linearGradient>
    <linearGradient id="${g("ex")}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#4f341d"/><stop offset="1" stop-color="#3a2614"/></linearGradient>
    <radialGradient id="${g("so")}"><stop offset="0" stop-color="#000" stop-opacity="0.45"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>
  </defs>
  <ellipse class="ar-sombra" cx="${x + L * 0.55}" cy="${y + H + H * 0.18}" rx="${L * 0.6}" ry="${H * 0.28}" fill="url(#${g("so")})"/>
  <path d="M ${x} ${y} L ${x + L} ${y} L ${x + L + dx} ${y + dy} L ${x + dx} ${y + dy} Z" fill="url(#${g("te")})" stroke="#3a2614" stroke-width="${Math.max(1.5, L / 500).toFixed(1)}" stroke-linejoin="round"/>
  <path d="M ${x + L} ${y} L ${x + L + dx} ${y + dy} L ${x + L + dx} ${y + dy + H} L ${x + L} ${y + H} Z" fill="url(#${g("ex")})" stroke="#2c1c0e" stroke-width="${Math.max(1.5, L / 500).toFixed(1)}" stroke-linejoin="round"/>
  <rect x="${x}" y="${y}" width="${L}" height="${H}" fill="url(#${g("fr")})" stroke="#2c1c0e" stroke-width="${Math.max(1.5, L / 450).toFixed(1)}"/>
  <g>${tablas}${juntas}</g>
  <g class="ar-tsohar"><rect x="${x}" y="${y + 1}" width="${L}" height="${ts.toFixed(1)}" fill="#1c120a"/>
    <path d="M ${x + L} ${y + 1} L ${x + L + dx} ${y + dy + 1} L ${x + L + dx} ${y + dy + 1 + ts} L ${x + L} ${y + 1 + ts} Z" fill="#150d07"/></g>
  <g class="ar-cubiertas"><path d="M ${x} ${y + H / 3} L ${x + L} ${y + H / 3} M ${x} ${y + (2 * H) / 3} L ${x + L} ${y + (2 * H) / 3}" stroke="#e9bf60" stroke-width="${Math.max(2.5, L / 300).toFixed(1)}" stroke-dasharray="${(L / 60).toFixed(0)} ${(L / 90).toFixed(0)}"/></g>
  <rect class="ar-hueco" x="${pX}" y="${pY}" width="${pW}" height="${pH}" fill="#140c06"/>
  <rect class="ar-puerta" x="${pX}" y="${pY}" width="${pW}" height="${pH}" fill="#5a3b20" stroke="#2c1c0e" stroke-width="${Math.max(1.5, L / 500).toFixed(1)}"/>
</g>`;
}
// Medidas del arca en px para colocar rótulos: el costado, la puerta y la línea de flotación.
function arcaMedidas(x, y, L) {
  const H = L / 10;
  return { H, dx: L / 10, dy: -L / 18, puerta: { x: x + L * 0.62, y: y + H * 0.36, w: L * 0.05, h: H * 0.6 } };
}
