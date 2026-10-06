/*incluir:_naciones.js*/
// Pueblos de Génesis 10 sobre el mapa de Perspicacia (2400x1840). Colores oscuros para leerse sobre el mapa claro.
const COLR = { J: "#2d56c4", C: "#c2372a", S: "#1f7a35" };
// Dónde va cada rótulo respecto a su punto: [dx, dy, anclaje].
const OFF = {
  "Javán": [-30, 16, "end"], "Canaán": [-30, 16, "end"], "Caftorim": [-30, 16, "end"], "Lud": [-30, 16, "end"],
  "Tirás": [0, -34, "middle"], "Cus": [0, -34, "middle"], "Sebá": [0, -34, "middle"],
  "Havilá": [-14, -34, "end"], "Joctán": [14, -34, "start"],
};
function pintaPueblos() {
  let s = "";
  for (const [r, n, x, y, c, nota, borde] of PUEBLOS) {
    const col = COLR[r], [dx, dy, a] = OFF[n] ?? [30, 16, "start"];
    const id = "pb-" + n.normalize("NFD").replace(/[̀-ͯ]/g, "");
    let punto;
    if (borde === "o") {
      // Tarsis: flecha hacia el oeste, fuera del mapa.
      punto = `<path d="M 118 ${y} L 18 ${y} M 50 ${y - 26} L 16 ${y} L 50 ${y + 26}" fill="none" stroke="${col}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="1 0"/>`;
      s += `<g class="pb r-${r} ${id}">${punto}<text class="rot" x="24" y="${y + 70}" font-size="46" stroke-width="12" fill="${col}">Tarsis ?</text><text class="rot" x="24" y="${y + 116}" font-size="34" stroke-width="10" fill="${col}">¿España o Cerdeña?</text></g>`;
      continue;
    }
    if (c === "f") punto = `<circle cx="${x}" cy="${y}" r="19" fill="${col}" stroke="#fff" stroke-width="6"/>`;
    else if (c === "p") punto = `<circle cx="${x}" cy="${y}" r="16" fill="#fff" stroke="${col}" stroke-width="9"/>`;
    else punto = `<circle cx="${x}" cy="${y}" r="17" fill="rgba(255,255,255,0.7)" stroke="${col}" stroke-width="7" stroke-dasharray="7 6"/>`;
    const sur = borde === "s" ? `<path d="M ${x - 16} ${y + 30} L ${x} ${y + 50} L ${x + 16} ${y + 30}" fill="none" stroke="${col}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>` : "";
    const nom = c === "q" ? n + " ?" : n;
    s += `<g class="pb r-${r} ${id}">${punto}${sur}<text class="rot" x="${x + dx}" y="${y + dy}" font-size="48" stroke-width="12" fill="${col}" text-anchor="${a}">${nom}</text></g>`;
  }
  pinta(".pueblos", s);
}
const pb = (n) => ".pb-" + n.normalize("NFD").replace(/[̀-ͯ]/g, "");
// Muestra los pueblos de una rama uno tras otro a partir de t.
function rama(r, t, paso = 0.28) {
  const ns = PUEBLOS.filter((p) => p[0] === r).map((p) => pb(p[1]));
  ns.forEach((s, i) => salta(s, t + i * paso, { desde: 0.3, d: 0.45 }));
}
// Rama ya vista: presente desde el principio, apagada.
function ramaVista(r, op = 0.45) {
  PUEBLOS.filter((p) => p[0] === r).forEach((p) => tl.set($(pb(p[1])), { opacity: op }, 0));
}
const VN = { x: 0, y: 0, w: 1380, h: 1080 };
