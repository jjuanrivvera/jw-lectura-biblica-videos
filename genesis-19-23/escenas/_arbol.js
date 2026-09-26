// Árbol de la familia de Taré en Génesis 19 a 24 (el de la investigación, redibujado en grande).
// viewBox 0 0 1000 880. Cada nodo lleva la clase n-<clave> y cada línea e-<clave>, para encender por partes.
const ARBOL_N = {
  tare: ["Taré", 500, 70], haran: ["Harán", 125, 250], nacor: ["Nacor", 365, 250], abrahan: ["Abrahán", 610, 250], sara: ["Sara", 900, 250],
  lot: ["Lot", 90, 440], milca: ["Milcá", 280, 440], agar: ["Agar", 540, 440],
  moab: ["Moab", 70, 630], benammi: ["Ben-Ammí", 240, 630], betuel: ["Betuel", 420, 630], ismael: ["Ismael", 620, 630], isaac: ["Isaac", 850, 630],
  rebeca: ["Rebeca", 420, 810],
};
function arbolSVG() {
  const N = ARBOL_N;
  const c = (a, b, dash) => { const [, x1, y1] = N[a], [, x2, y2] = N[b]; const ym = (y1 + y2) / 2 + 10;
    return `<path class="rama e-${a}-${b}" d="M ${x1} ${y1 + 42} C ${x1} ${ym} ${x2} ${ym} ${x2} ${y2 - 42}"${dash ? ' stroke-dasharray="16 12"' : ""}/>`; };
  let s = "";
  s += c("tare", "haran") + c("tare", "nacor") + c("tare", "abrahan") + c("tare", "sara", true);
  s += c("haran", "lot") + c("haran", "milca") + c("lot", "moab") + c("lot", "benammi") + c("abrahan", "ismael") + c("agar", "ismael");
  s += `<path class="boda e-abrahan-sara" d="M 735 250 L 825 250"/><text class="nota e-abrahan-sara" x="780" y="232" text-anchor="middle">casados</text>`;
  s += `<path class="rama e-pareja-isaac" d="M 780 250 C 780 460 850 440 850 588"/>`;
  s += `<path class="boda e-nacor-milca" d="M 365 292 L 300 398"/><text class="nota e-nacor-milca" x="352" y="360">casados</text>`;
  s += `<path class="rama e-pareja-betuel" d="M 332 345 C 332 540 420 520 420 588"/>`;
  s += `<path class="rama e-betuel-rebeca" d="M 420 672 L 420 768"/>`;
  s += `<path class="futuro e-rebeca-isaac" d="M 500 810 C 700 810 850 760 850 672"/><text class="nota futuro-t e-rebeca-isaac" x="690" y="846" text-anchor="middle">se casarán (Génesis 24)</text>`;
  s += `<text class="nota otra e-tare-sara" x="790" y="130" text-anchor="middle">otra madre (20:12)</text>`;
  for (const [k, [t, x, y]] of Object.entries(N)) {
    const w = Math.max(150, t.length * 30 + 40);
    s += `<g class="nodo n-${k}"><rect x="${x - w / 2}" y="${y - 42}" width="${w}" height="84" rx="20"/><text x="${x}" y="${y + 16}">${t}</text></g>`;
  }
  return s;
}
