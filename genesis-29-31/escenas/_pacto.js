// El lugar del pacto (Génesis 31:44-54): dos campamentos, la columna y el montón de piedras.
function pactoEscena() {
  const tienda = (x, y, s, c) => '<g transform="translate(' + x + ' ' + y + ') scale(' + s + ')"><path d="M -90 0 L 0 -110 L 90 0 Z" fill="' + c + '" stroke="#3a2a1a" stroke-width="4"/><path d="M -14 0 L 0 -40 L 14 0 Z" fill="#2a1d12"/></g>';
  let piedras = "";
  // El montón se arma de abajo arriba: cada fila entra por separado (clases p0..p4).
  const filas = [[7, 900, 760], [6, 920, 718], [5, 940, 676], [4, 960, 636], [3, 980, 598]];
  filas.forEach(([n, x0, y], f) => {
    let fila = "";
    for (let i = 0; i < n; i++) fila += piedra(x0 + i * 46 - (n - 1) * 23 + (f % 2) * 8 - 960 + 960, y, 26, 18);
    piedras += '<g class="p' + f + '">' + fila + '</g>';
  });
  return defsDibujos() +
    '<rect x="0" y="0" width="1920" height="1080" fill="' + G("cielo") + '"/>' +
    '<path d="M 0 520 C 300 420 600 470 900 430 C 1200 390 1500 460 1920 420 L 1920 1080 L 0 1080 Z" fill="#8e9a5a"/>' +
    '<path d="M 0 640 C 400 600 900 660 1400 620 C 1650 600 1800 630 1920 610 L 1920 1080 L 0 1080 Z" fill="' + G("pasto") + '"/>' +
    '<g class="camp-l">' + tienda(260, 690, 1.0, "#6b4a8a") + tienda(420, 660, 0.8, "#7d5a9a") + tienda(140, 640, 0.7, "#5f447a") + '</g>' +
    '<g class="camp-j">' + tienda(1620, 700, 1.0, "#a07a3a") + tienda(1460, 670, 0.8, "#b58b4a") + tienda(1780, 650, 0.7, "#8c6a30") + '</g>' +
    '<g class="columna"><ellipse cx="740" cy="790" rx="70" ry="14" fill="rgba(0,0,0,0.3)"/><path d="M 700 790 L 692 520 C 692 494 712 478 738 478 C 764 478 784 494 782 522 L 776 790 Z" fill="' + G("piedra") + '" stroke="#4d473f" stroke-width="4"/></g>' +
    '<g class="monton">' + piedras + '</g>' +
    '<g class="comida"><ellipse cx="960" cy="584" rx="80" ry="14" fill="#d6b98c" stroke="#8c6541" stroke-width="3"/><circle cx="930" cy="570" r="18" fill="#c98f63"/><circle cx="970" cy="566" r="16" fill="#c98f63"/><circle cx="1000" cy="572" r="14" fill="#8a1c10"/></g>';
}
