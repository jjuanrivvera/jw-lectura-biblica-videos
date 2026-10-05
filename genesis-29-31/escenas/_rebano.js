// Un rebaño sobre el pasto: posiciones fijas (semilla), de atrás hacia delante para que se tapen bien.
function rebano(lista, x0, y0, w, h, sem = 5) {
  const r = () => { sem = (sem * 9301 + 49297) % 233280; return sem / 233280; };
  const cols = Math.ceil(Math.sqrt(lista.length * w / h));
  const filas = Math.ceil(lista.length / cols);
  const pos = lista.map((a, i) => {
    const c = i % cols, f = Math.floor(i / cols);
    return { a, x: x0 + (c + 0.5) * w / cols + (r() - 0.5) * w / cols * 0.5, y: y0 + (f + 0.6) * h / filas + (r() - 0.5) * h / filas * 0.4, izq: r() > 0.5 };
  }).sort((p, q) => p.y - q.y);
  return pos.map((p) => {
    const s = 0.8 + (p.y - y0) / h * 0.35;
    // El envoltorio sin transform es el que se anima: GSAP y un transform de atributo se pelean.
    const o = { izq: p.izq };
    const a = p.a.t === "oveja" ? oveja(p.x, p.y, s, { ...o, oscura: p.a.oscura })
      : cabra(p.x, p.y, s, { ...o, manchas: p.a.manchas, rayas: p.a.rayas, portador: p.a.portador });
    return '<g class="' + (p.a.cls || "") + '">' + a + '</g>';
  }).join("");
}
