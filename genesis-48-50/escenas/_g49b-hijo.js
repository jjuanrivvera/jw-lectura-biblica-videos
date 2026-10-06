// Patrón de los hijos (escenas 25 a 32). El retrato (620 px en 110,200) pasa a medallón de 230 px
// en 1130,96 cuando entra el mapa; el nombre grande se queda junto al medallón.
function hijoEntra(t = 0.3) {
  entra(".hijo.gh", t, { y: 30, s: 0.94, d: 0.8 });
  entra(".pres .nhijo", t + 0.3, { x: -24, y: 0 });
  kb(".hijo.gh img", 0, DUR, { s: 1.0 }, { s: 1.07 });
}
function hijoAMapa(t, d = 1.1) {
  tl.to($(".hijo.gh"), { x: 1020, y: -104, scale: 230 / 620, duration: d, ease: "power2.inOut" }, t);
  sale(".pres", t - 0.15, { y: -20, d: 0.4 });
  aparece(".fmapa", t + 0.45, 0.7);
  entra(".mini", t + 0.5, { x: -24, y: 0 });
}
// Flecha recta con punta, en coordenadas del mapa. La punta es un <path> aparte (clase cls + "-p").
function flecha(x1, y1, x2, y2, cls, o = {}) {
  const c = o.color ?? "#b8430f", w = o.w ?? 14, L = Math.hypot(x2 - x1, y2 - y1), ux = (x2 - x1) / L, uy = (y2 - y1) / L;
  const h = w * 2.6, bx = x2 - ux * h, by = y2 - uy * h, px = -uy * w * 1.6, py = ux * w * 1.6;
  const dash = o.punt ? ` stroke-dasharray="${w * 2} ${w * 1.6}"` : "";
  return `<path class="${cls}" d="M ${x1} ${y1} L ${bx.toFixed(1)} ${by.toFixed(1)}" stroke="${c}" stroke-width="${w}" fill="none" stroke-linecap="round"${dash}/>` +
    `<path class="${cls}-p" d="M ${x2} ${y2} L ${(bx + px).toFixed(1)} ${(by + py).toFixed(1)} L ${(bx - px).toFixed(1)} ${(by - py).toFixed(1)} Z" fill="${c}"/>`;
}
