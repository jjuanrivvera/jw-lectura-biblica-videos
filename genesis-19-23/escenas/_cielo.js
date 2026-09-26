// Franja de cielo que marca la hora que da el relato (19:1, 15, 23): atardecer, noche, amanecer, sol.
// Uso: pinta(".cielo", cieloHTML()); hora("noche", t);
function cieloHTML() {
  const capa = (k, fondo, txt, astro) =>
    `<div class="c c-${k}" style="position:absolute;inset:0;border-radius:18px;background:${fondo};opacity:0">${astro}
      <div style="position:absolute;left:28px;top:50%;transform:translateY(-50%);font-family:Arial,sans-serif;font-weight:800;font-size:30px;letter-spacing:0.12em;text-transform:uppercase;color:#fff;text-shadow:0 2px 8px rgba(0,0,0,0.45)">${txt}</div></div>`;
  const estrellas = [[380, 22], [450, 70], [520, 30], [300, 80], [590, 60], [250, 30]]
    .map(([x, y]) => `<div style="position:absolute;left:${x}px;top:${y}px;width:5px;height:5px;border-radius:50%;background:#fff"></div>`).join("");
  return (
    capa("atardecer", "linear-gradient(180deg,#3d3a6b 0%,#c7607a 55%,#f2a65a 100%)", "Al atardecer",
      '<div style="position:absolute;right:60px;bottom:-26px;width:70px;height:70px;border-radius:50%;background:#ffd08a;box-shadow:0 0 40px #ffb45e"></div>') +
    capa("noche", "linear-gradient(180deg,#0b1224 0%,#1b2a4a 100%)", "De noche",
      estrellas + '<div style="position:absolute;right:60px;top:22px;width:62px;height:62px;border-radius:50%;box-shadow:-16px 8px 0 0 #f3ecd6"></div>') +
    capa("amanecer", "linear-gradient(180deg,#2d3f6e 0%,#8f7aa8 50%,#f0b48a 100%)", "Empieza a amanecer",
      '<div style="position:absolute;right:70px;bottom:-40px;width:70px;height:70px;border-radius:50%;background:#ffe0b0;box-shadow:0 0 30px #ffd39a"></div>') +
    capa("sol", "linear-gradient(180deg,#3f8fd6 0%,#8cc4ef 100%)", "Sale el sol",
      '<div style="position:absolute;right:56px;top:18px;width:72px;height:72px;border-radius:50%;background:#ffe27a;box-shadow:0 0 40px #ffd34a"></div>')
  );
}
let _horaActual = null;
function hora(k, t, d = 1.2) {
  if (_horaActual) tl.to($(".c-" + _horaActual), { opacity: 0, duration: d, ease: "none" }, t);
  if (!_horaActual) tl.set($(".c-" + k), { opacity: 1 }, t);
  else tl.to($(".c-" + k), { opacity: 1, duration: d, ease: "none" }, t);
  _horaActual = k;
}
