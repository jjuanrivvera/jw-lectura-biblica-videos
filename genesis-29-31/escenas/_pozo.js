// El pozo del campo cerca de Harán (Génesis 29:2, 3), en corte: se usa en las escenas 03 y 04.
// Coordenadas de pantalla (1920x1080). Suelo en y = 600.
function pozoEscena(o = {}) {
  const S = 600;
  let capas = "";
  for (let i = 0; i < 5; i++) {
    const y = S + 70 + i * 80;
    capas += '<path d="M 0 ' + y + ' C 400 ' + (y - 14) + ' 900 ' + (y + 16) + ' 1920 ' + (y - 6) + '" stroke="rgba(60,40,20,0.35)" stroke-width="3" fill="none"/>';
  }
  let piedritas = "";
  let sem = 11;
  const r = () => { sem = (sem * 9301 + 49297) % 233280; return sem / 233280; };
  for (let i = 0; i < 70; i++) {
    const x = r() * 1920, y = S + 40 + r() * 420;
    if (x > 700 && x < 960) continue;
    piedritas += '<ellipse cx="' + x.toFixed(0) + '" cy="' + y.toFixed(0) + '" rx="' + (4 + r() * 10).toFixed(1) + '" ry="' + (3 + r() * 6).toFixed(1) + '" fill="rgba(70,50,30,0.35)"/>';
  }
  const bloques = [];
  for (let fila = 0; fila < 3; fila++) for (let k = 0; k < 6; k++) {
    const w = 44, x = 700 + k * w + (fila % 2 ? 22 : 0);
    if (x + w > 972) continue;
    bloques.push('<rect x="' + x + '" y="' + (S - 84 + fila * 28) + '" width="' + (w - 3) + '" height="25" rx="5" fill="' + G("piedra") + '" stroke="#5d574e" stroke-width="2"/>');
  }
  return defsDibujos() +
    '<rect x="0" y="0" width="1920" height="' + S + '" fill="' + G("cielo") + '"/>' +
    '<path d="M 0 ' + (S - 60) + ' C 300 ' + (S - 110) + ' 520 ' + (S - 70) + ' 760 ' + (S - 96) + ' C 1100 ' + (S - 130) + ' 1400 ' + (S - 70) + ' 1920 ' + (S - 100) + ' L 1920 ' + S + ' L 0 ' + S + ' Z" fill="#c9c28a" opacity="0.8"/>' +
    '<g class="sol-g">' + sol(1500, 130, 64) + '</g>' +
    '<rect x="0" y="' + S + '" width="1920" height="' + (1080 - S) + '" fill="' + G("tierra") + '"/>' + capas + piedritas +
    '<rect x="0" y="' + (S - 8) + '" width="1920" height="16" fill="' + G("pasto") + '"/>' +
    // Agua de la capa subterránea que alimenta el pozo.
    '<path class="napa" d="M 0 960 C 300 940 600 975 830 955 C 1100 935 1500 975 1920 950 L 1920 1030 C 1500 1050 1100 1015 830 1035 C 600 1050 300 1020 0 1035 Z" fill="' + G("agua") + '" opacity="0.85"/>' +
    // El pozo: hoyo revestido de piedra hasta el agua.
    '<g class="hoyo"><rect x="760" y="' + S + '" width="140" height="' + (975 - S) + '" fill="#2a1d12"/>' +
    '<rect x="760" y="' + S + '" width="14" height="' + (975 - S) + '" fill="#6d6457"/><rect x="886" y="' + S + '" width="14" height="' + (975 - S) + '" fill="#6d6457"/>' +
    '<rect x="774" y="905" width="112" height="70" fill="' + G("agua") + '"/>' +
    '<path class="cuerda" d="M 830 ' + (S - 100) + ' L 830 870" stroke="#c8a36a" stroke-width="4"/>' +
    '<path class="pozal" d="M 812 870 L 848 870 L 842 898 L 818 898 Z" fill="#7a4a24" stroke="#4b2a12" stroke-width="3"/></g>' +
    // Brocal: muro bajo de piedra alrededor de la boca.
    '<g class="brocal">' + bloques.join("") + '</g>' +
    // Pilón para que beban los animales.
    '<g class="pilon"><rect x="1030" y="' + (S - 58) + '" width="260" height="58" rx="10" fill="' + G("piedra") + '" stroke="#4d473f" stroke-width="3"/>' +
    '<rect x="1046" y="' + (S - 48) + '" width="228" height="16" rx="6" fill="' + G("agua") + '"/></g>' +
    // La gran piedra sobre la boca.
    '<g class="tapa">' + piedra(836, S - 100, 170, 58) + '</g>' +
    // Tres rebaños echados cerca.
    '<g class="reb1">' + oveja(130, S + 4, 1.05) + oveja(280, S + 10, 1.0) + oveja(420, S + 2, 1.05, { izq: true }) + oveja(210, S + 34, 1.1) + '</g>' +
    '<g class="reb2">' + oveja(1390, S + 6, 1.05, { izq: true }) + oveja(1520, S + 12, 1.0) + oveja(1460, S + 36, 1.1, { izq: true }) + '</g>' +
    '<g class="reb3">' + oveja(1680, S + 4, 1.0, { izq: true }) + oveja(1820, S + 14, 1.05, { izq: true }) + oveja(1750, S + 38, 1.1, { izq: true }) + '</g>';
}
