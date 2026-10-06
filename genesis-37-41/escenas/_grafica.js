// Subidas y bajadas de José (figura de la investigación): ocho momentos, de 37:3 a 41:40.
// La altura no mide nada; la línea dorada es el estribillo de Génesis 39: “Jehová estaba con José”.
const GP = [
  ["37:3", "hijo preferido", 76.4], ["37:24", "en la cisterna", 193.0], ["37:36", "esclavo", 160.6],
  ["39:4", "encargado de la casa", 99.1], ["39:20", "preso, con grilletes", 196.3], ["39:22", "a cargo de los presos", 131.5],
  ["40:23", "olvidado", 170.4], ["41:40", "segundo en Egipto", 60.2],
];
const GX = (i) => 130 + i * 214, GY = (v) => 130 + (v - 55) * 3.0;
function grafica(sel) {
  let s = `<path d="M 60 110 V 600" stroke="rgba(241,233,216,0.25)" stroke-width="3"/>
    <text class="gr-ej" x="60" y="96" text-anchor="middle">mejor</text><text class="gr-ej" x="60" y="630" text-anchor="middle">peor</text>
    <g class="gr-oro"><path class="gr-orol" d="M 90 70 H 1700" stroke="#e9bf60" stroke-width="10" stroke-linecap="round"/><text class="gr-orot" x="110" y="52">“Jehová estaba con José”</text></g>`;
  GP.forEach(([v, t, y], i) => {
    if (i) s += `<path class="gr-s gr-s${i}" d="M ${GX(i - 1)} ${GY(GP[i - 1][2])} L ${GX(i)} ${GY(y)}" stroke="#93bbef" stroke-width="8" stroke-linecap="round"/>`;
  });
  GP.forEach(([v, t, y], i) => {
    const arriba = i === 0 || y < GP[i - 1][2] || GY(y) > 500;
    s += `<g class="gr-p gr-p${i}"><circle cx="${GX(i)}" cy="${GY(y)}" r="17" fill="#93bbef" stroke="#17212b" stroke-width="5"/>
      <text class="gr-t" x="${GX(i)}" y="${GY(y) + (arriba ? -34 : 62)}" text-anchor="middle">${t}</text>
      <text class="gr-v" x="${GX(i)}" y="630" text-anchor="middle">${v}</text></g>`;
  });
  $(sel).innerHTML = s;
  // Todo empieza oculto: cada escena revela solo los pasos que cuenta.
  $$(".gr-p, .gr-s").forEach((e) => gsap.set(e, { opacity: 0 }));
}
// Muestra el paso i (el punto y el tramo que llega a él) en t.
function paso(i, t, d = 0.7) {
  if (i) traza(".gr-s" + i, t, d);
  entra(".gr-p" + i, t + (i ? d * 0.8 : 0), { y: 14, d: 0.45 });
}
// Deja ya dibujados los pasos 0..n-1 desde el principio de la escena.
function pasosPrevios(n, t = 0.4) {
  for (let i = 0; i < n; i++) paso(i, t + i * 0.25, 0.3);
}
