// Dibujos compartidos (se incluyen con /*incluir:_dibujos.js*/ dentro del <script> de la escena).
// Devuelven marcado SVG. Los degradados llevan el ID de la escena en su nombre: si dos escenas
// compartieran un id, el navegador tomaría el de una escena oculta y no pintaría nada.
const G = (n) => "url(#" + n + "-" + ID + ")";
function defsDibujos() {
  const d = (n) => n + "-" + ID;
  return '<defs>' +
    '<radialGradient id="' + d("lana") + '" cx="40%" cy="35%" r="70%"><stop offset="0" stop-color="#fffdf6"/><stop offset="0.65" stop-color="#ece4d2"/><stop offset="1" stop-color="#bfb49c"/></radialGradient>' +
    '<radialGradient id="' + d("negra") + '" cx="40%" cy="30%" r="75%"><stop offset="0" stop-color="#5a4d43"/><stop offset="0.6" stop-color="#2e2621"/><stop offset="1" stop-color="#171210"/></radialGradient>' +
    '<radialGradient id="' + d("piel") + '" cx="40%" cy="30%" r="75%"><stop offset="0" stop-color="#7a6a5c"/><stop offset="1" stop-color="#3a302a"/></radialGradient>' +
    '<linearGradient id="' + d("piedra") + '" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#b9b1a3"/><stop offset="0.55" stop-color="#8d8577"/><stop offset="1" stop-color="#5d574e"/></linearGradient>' +
    '<linearGradient id="' + d("adobe") + '" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d6b98c"/><stop offset="1" stop-color="#a88457"/></linearGradient>' +
    '<linearGradient id="' + d("arcilla") + '" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#e2b48a"/><stop offset="0.5" stop-color="#c98f63"/><stop offset="1" stop-color="#9c6a45"/></linearGradient>' +
    '<linearGradient id="' + d("agua") + '" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6fb2e6"/><stop offset="1" stop-color="#1f5d96"/></linearGradient>' +
    '<linearGradient id="' + d("tierra") + '" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#b58b5a"/><stop offset="0.5" stop-color="#8c6541"/><stop offset="1" stop-color="#5a4029"/></linearGradient>' +
    '<linearGradient id="' + d("cielo") + '" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8fc0e8"/><stop offset="0.7" stop-color="#d9e9f0"/><stop offset="1" stop-color="#efe6cf"/></linearGradient>' +
    '<linearGradient id="' + d("pasto") + '" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#b9b36b"/><stop offset="1" stop-color="#8a8a4a"/></linearGradient>' +
    '<linearGradient id="' + d("madera") + '" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#7a5332"/><stop offset="0.5" stop-color="#a7784c"/><stop offset="1" stop-color="#6d4a2c"/></linearGradient>' +
    '<linearGradient id="' + d("oro") + '" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f6d98c"/><stop offset="1" stop-color="#b98a2e"/></linearGradient>' +
    '<radialGradient id="' + d("sol") + '" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#fff6c8"/><stop offset="0.45" stop-color="#ffd86a"/><stop offset="1" stop-color="#ffb13b" stop-opacity="0"/></radialGradient>' +
    '<filter id="' + d("sombra") + '" x="-20%" y="-20%" width="140%" height="160%"><feDropShadow dx="0" dy="8" stdDeviation="8" flood-color="#000" flood-opacity="0.35"/></filter>' +
    '</defs>';
}

// Oveja de lana blanca (o "oscura", 30:32), mirando a la derecha. (x, y) = punto entre las patas, en el suelo.
function oveja(x, y, s = 1, o = {}) {
  const lana = o.oscura ? G("piel") : G("lana");
  const borde = o.oscura ? "#221b17" : "#9d9380";
  const f = o.izq ? -1 : 1;
  const bolas = [[-38, -62, 24], [-14, -72, 26], [12, -70, 25], [34, -60, 22], [-46, -44, 20], [42, -42, 19], [-24, -40, 24], [4, -40, 26], [26, -44, 22]];
  return '<g class="' + (o.cls || "") + '" transform="translate(' + x + ' ' + y + ') scale(' + (s * f) + ' ' + s + ')">' +
    '<ellipse cx="0" cy="2" rx="58" ry="9" fill="rgba(0,0,0,0.22)"/>' +
    [[-30, 0], [-14, 2], [18, 2], [32, 0]].map(([lx, ly]) => '<rect x="' + (lx - 5) + '" y="-34" width="10" height="' + (34 + ly) + '" rx="5" fill="#3b312a"/>').join("") +
    bolas.map(([bx, by, r]) => '<circle cx="' + bx + '" cy="' + by + '" r="' + r + '" fill="' + lana + '" stroke="' + borde + '" stroke-width="2"/>').join("") +
    '<path d="M 50 -70 C 62 -82 84 -80 90 -66 C 95 -54 88 -44 76 -44 C 64 -44 54 -52 50 -60 Z" fill="#3e342d"/>' +
    '<path d="M 58 -74 C 52 -84 44 -86 40 -80 C 46 -76 50 -72 56 -70 Z" fill="#2c241f"/>' +
    '<circle cx="78" cy="-64" r="3.4" fill="#f4ecd8"/>' +
    '</g>';
}

// Cabra, mirando a la derecha: negra, o con manchas blancas; `portador` le pone el aro dorado.
function cabra(x, y, s = 1, o = {}) {
  const f = o.izq ? -1 : 1;
  const manchas = o.manchas ? '<path d="M -34 -60 C -24 -72 -8 -66 -10 -52 C -14 -42 -30 -44 -34 -60 Z" fill="#f4eee0"/>' +
    '<path d="M 6 -46 C 16 -58 34 -52 30 -40 C 26 -32 10 -34 6 -46 Z" fill="#f4eee0"/>' +
    '<circle cx="-20" cy="-36" r="6" fill="#f4eee0"/><circle cx="22" cy="-64" r="5" fill="#f4eee0"/><circle cx="56" cy="-82" r="4" fill="#f4eee0"/>' : "";
  const rayas = o.rayas ? '<path d="M -40 -58 L -30 -38 M -22 -66 L -12 -36 M -4 -68 L 6 -36 M 14 -66 L 22 -38" stroke="#efe6d2" stroke-width="5" stroke-linecap="round"/>' : "";
  const aro = o.portador ? '<ellipse class="aro" cx="4" cy="-44" rx="86" ry="66" fill="none" stroke="#f0c75e" stroke-width="7" stroke-dasharray="14 10"/>' : "";
  return '<g class="' + (o.cls || "") + '" transform="translate(' + x + ' ' + y + ') scale(' + (s * f) + ' ' + s + ')">' +
    aro +
    '<ellipse cx="0" cy="2" rx="56" ry="8" fill="rgba(0,0,0,0.22)"/>' +
    [[-32, -2], [-18, 0], [20, 0], [34, -2]].map(([lx, ly]) => '<path d="M ' + lx + ' -36 L ' + (lx + 2) + ' ' + ly + '" stroke="#1d1714" stroke-width="7" stroke-linecap="round"/>').join("") +
    '<path d="M -48 -58 C -50 -80 -20 -84 10 -80 C 36 -78 50 -70 52 -56 C 54 -38 36 -30 6 -30 C -26 -30 -46 -36 -48 -58 Z" fill="' + G("negra") + '"/>' +
    manchas + rayas +
    '<path d="M -46 -66 C -56 -80 -58 -88 -52 -92 C -48 -84 -44 -76 -40 -70 Z" fill="#221b17"/>' +
    '<path d="M 40 -70 C 46 -90 56 -100 66 -102 C 78 -104 86 -96 86 -86 C 86 -76 80 -70 72 -68 C 62 -66 52 -62 46 -56 Z" fill="' + G("negra") + '"/>' +
    '<path d="M 64 -100 C 58 -118 44 -126 34 -122 C 44 -118 52 -110 58 -98 Z" fill="#8b7a62"/>' +
    '<path d="M 70 -101 C 68 -118 58 -130 48 -130 C 58 -124 64 -114 66 -100 Z" fill="#a8977c"/>' +
    '<path d="M 80 -72 C 82 -62 78 -54 74 -50 C 72 -58 72 -66 74 -72 Z" fill="#2a221d"/>' +
    '<circle cx="74" cy="-90" r="3.2" fill="#e9bf60"/>' +
    '</g>';
}

// Piedra redondeada con luz desde arriba.
function piedra(cx, cy, rx, ry, cls = "") {
  return '<g class="' + cls + '"><ellipse cx="' + cx + '" cy="' + (cy + ry * 0.55) + '" rx="' + rx * 1.02 + '" ry="' + ry * 0.45 + '" fill="rgba(0,0,0,0.28)"/>' +
    '<path d="M ' + (cx - rx) + ' ' + cy + ' C ' + (cx - rx) + ' ' + (cy - ry * 1.1) + ' ' + (cx + rx) + ' ' + (cy - ry * 1.15) + ' ' + (cx + rx) + ' ' + cy +
    ' C ' + (cx + rx) + ' ' + (cy + ry * 0.6) + ' ' + (cx - rx) + ' ' + (cy + ry * 0.62) + ' ' + (cx - rx) + ' ' + cy + ' Z" fill="' + G("piedra") + '" stroke="#4d473f" stroke-width="3"/>' +
    '<path d="M ' + (cx - rx * 0.6) + ' ' + (cy - ry * 0.55) + ' C ' + (cx - rx * 0.2) + ' ' + (cy - ry * 0.85) + ' ' + (cx + rx * 0.3) + ' ' + (cy - ry * 0.8) + ' ' + (cx + rx * 0.55) + ' ' + (cy - ry * 0.5) + '" fill="none" stroke="rgba(255,255,255,0.35)" stroke-width="6" stroke-linecap="round"/></g>';
}

// Tablilla de arcilla con escritura cuneiforme (cuñas pequeñas en renglones).
function tablilla(x, y, w, h, cls = "") {
  let cunas = "";
  let semilla = 7;
  const rnd = () => { semilla = (semilla * 9301 + 49297) % 233280; return semilla / 233280; };
  for (let fila = 0; fila < 9; fila++) {
    const fy = y + h * 0.13 + fila * h * 0.085;
    let fx = x + w * 0.1;
    while (fx < x + w * 0.88) {
      const l = 10 + rnd() * 16;
      if (rnd() > 0.72) {
        cunas += '<path d="M ' + fx.toFixed(1) + ' ' + (fy - 9).toFixed(1) + ' l 8 5 l -8 5 z" fill="#7d5132"/>';
      } else {
        cunas += '<path d="M ' + fx.toFixed(1) + ' ' + (fy - 3).toFixed(1) + ' l ' + l.toFixed(1) + ' 3 l ' + (-l).toFixed(1) + ' 3 z" fill="#7d5132"/>';
      }
      fx += l + 6 + rnd() * 8;
    }
    cunas += '<path d="M ' + (x + w * 0.07) + ' ' + (fy + h * 0.04) + ' L ' + (x + w * 0.93) + ' ' + (fy + h * 0.04) + '" stroke="rgba(110,70,40,0.45)" stroke-width="2"/>';
  }
  return '<g class="' + cls + '" filter="' + G("sombra") + '">' +
    '<path d="M ' + (x + 18) + ' ' + y + ' L ' + (x + w - 14) + ' ' + (y + 4) + ' Q ' + (x + w) + ' ' + (y + 6) + ' ' + (x + w - 2) + ' ' + (y + 24) + ' L ' + (x + w + 4) + ' ' + (y + h - 20) + ' Q ' + (x + w + 2) + ' ' + (y + h) + ' ' + (x + w - 20) + ' ' + (y + h - 2) +
    ' L ' + (x + 16) + ' ' + (y + h + 3) + ' Q ' + (x - 2) + ' ' + (y + h) + ' ' + (x) + ' ' + (y + h - 20) + ' L ' + (x - 4) + ' ' + (y + 22) + ' Q ' + (x - 2) + ' ' + y + ' ' + (x + 18) + ' ' + y + ' Z" fill="' + G("arcilla") + '" stroke="#7b5033" stroke-width="3"/>' +
    cunas + '</g>';
}

// Sol con halo y luna creciente (día y noche, 31:40).
function sol(cx, cy, r, cls = "") {
  return '<g class="' + cls + '"><circle cx="' + cx + '" cy="' + cy + '" r="' + r * 2.2 + '" fill="' + G("sol") + '"/><circle cx="' + cx + '" cy="' + cy + '" r="' + r + '" fill="#ffe07a"/></g>';
}
function luna(cx, cy, r, cls = "") {
  return '<g class="' + cls + '"><circle cx="' + cx + '" cy="' + cy + '" r="' + r * 1.9 + '" fill="rgba(200,215,255,0.12)"/>' +
    '<path d="M ' + cx + ' ' + (cy - r) + ' A ' + r + ' ' + r + ' 0 1 0 ' + cx + ' ' + (cy + r) + ' A ' + r * 1.25 + ' ' + r * 1.25 + ' 0 0 1 ' + cx + ' ' + (cy - r) + ' Z" fill="#e8ecf6"/></g>';
}
// Rama pelada a trozos: corteza oscura con franjas de madera blanca (30:37).
function rama(x1, y1, x2, y2, cls = "") {
  const dx = x2 - x1, dy = y2 - y1, L = Math.hypot(dx, dy), ang = Math.atan2(dy, dx) * 180 / Math.PI;
  let franjas = "";
  for (let i = 0; i < 7; i++) {
    const a = 20 + i * (L - 40) / 7;
    franjas += '<rect x="' + a.toFixed(1) + '" y="-9" width="' + ((L - 40) / 14).toFixed(1) + '" height="18" rx="4" fill="#f2ead6"/>';
  }
  return '<g class="' + cls + '" transform="translate(' + x1 + ' ' + y1 + ') rotate(' + ang.toFixed(2) + ')">' +
    '<rect x="0" y="-11" width="' + L.toFixed(1) + '" height="22" rx="11" fill="#5b3d26" stroke="#3a2616" stroke-width="3"/>' + franjas +
    '<path d="M ' + (L * 0.3).toFixed(1) + ' -8 l 26 -30" stroke="#5b3d26" stroke-width="8" stroke-linecap="round"/>' +
    '<path d="M ' + (L * 0.3 + 26).toFixed(1) + ' -38 c 14 -8 26 -4 30 4 c -12 6 -22 4 -30 -4 z" fill="#7aa35a"/></g>';
}
