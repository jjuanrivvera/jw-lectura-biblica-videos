// Librería común de las escenas. El constructor la pega dentro de una función que ya
// define ID (id de la composición), DUR (duración de la escena), LEAD (silencio antes de la
// voz) y W (palabras de la voz con su tiempo, ya desplazadas por LEAD).
const root = document.getElementById(ID);
const $ = (s) => root.querySelector(s);
const $$ = (s) => Array.from(root.querySelectorAll(s));
// Acepta un selector, un elemento, una NodeList o una lista mezclada de cualquiera de ellos.
const el = (x) => (typeof x === "string" ? $$(x) : Array.isArray(x) ? x.flatMap((y) => el(y)) : x instanceof NodeList ? Array.from(x) : [x]);
const tl = gsap.timeline({ paused: true });

// ---------- sincronía con la voz ----------
const norm = (s) =>
  s.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/[^a-z0-9ñ]/g, "");
const WN = W.map((w) => norm(w.w));
const trozos = (frase) => frase.split(/[\s\-]+/).map(norm).filter(Boolean);
function buscar(frase, despues) {
  const p = trozos(frase);
  for (let i = 0; i < WN.length; i++) {
    if (W[i].t < (despues || 0) - 0.001) continue;
    let ok = true;
    for (let k = 0; k < p.length; k++) if (WN[i + k] !== p[k]) { ok = false; break; }
    if (ok) return i;
  }
  throw new Error(ID + ': no encuentro "' + frase + '" después de ' + despues);
}
// Momento en que la voz empieza a decir la frase (primera vez después de `despues`).
function at(frase, despues) { return W[buscar(frase, despues)].t; }
// Momento en que la voz termina de decir la frase.
function fin(frase, despues) {
  const i = buscar(frase, despues);
  const w = W[i + trozos(frase).length - 1];
  return w.t + w.d;
}
const FIN_VOZ = W.length ? W[W.length - 1].t + W[W.length - 1].d : DUR;

// ---------- movimientos ----------
// Todos los elementos que se revelan empiezan ocultos por CSS (.oc, .esc, trazos) y se
// animan con immediateRender:false, así cada cuadro depende solo del tiempo.
const IR = { immediateRender: false };
// El primer movimiento que revela un elemento lo deja oculto desde el cuadro cero.
const _ocultos = new WeakSet();
function inicial(els, props) {
  els.forEach((e) => { if (!_ocultos.has(e)) { _ocultos.add(e); gsap.set(e, props); } });
  return els;
}
function entra(x, t, o = {}) {
  tl.fromTo(inicial(el(x), { opacity: 0 }), { opacity: 0, y: o.y ?? 36, x: o.x ?? 0, scale: o.s ?? 1 },
    { opacity: 1, y: 0, x: 0, scale: 1, duration: o.d ?? 0.6, ease: o.ease ?? "power3.out", stagger: o.st ?? 0, ...IR }, t);
}
function sale(x, t, o = {}) {
  tl.fromTo(el(x), { opacity: 1 }, { opacity: 0, y: o.y ?? -24, duration: o.d ?? 0.45, ease: "power2.in", stagger: o.st ?? 0, ...IR }, t);
}
function aparece(x, t, d = 0.5, hasta = 1) {
  tl.fromTo(inicial(el(x), { opacity: 0 }), { opacity: 0 }, { opacity: hasta, duration: d, ease: "none", ...IR }, t);
}
function atenua(x, t, hasta = 0.25, d = 0.5) {
  tl.to(el(x), { opacity: hasta, duration: d, ease: "power1.inOut" }, t);
}
function desaparece(x, t, d = 0.45) {
  tl.to(el(x), { opacity: 0, duration: d, ease: "none" }, t);
}
function salta(x, t, o = {}) {
  tl.fromTo(inicial(el(x), { opacity: 0 }), { opacity: 0, scale: o.desde ?? 0.4, rotation: o.r ?? 0 },
    { opacity: 1, scale: 1, rotation: 0, duration: o.d ?? 0.55, ease: o.ease ?? "back.out(1.8)", stagger: o.st ?? 0, ...IR }, t);
}
// Escritura a mano: se descubre de izquierda a derecha, como si la tiza avanzara.
function escribe(x, t, d = 0.8, o = {}) {
  tl.fromTo(inicial(el(x), { clipPath: "inset(-30% 103% -30% -3%)" }), { opacity: 1, clipPath: "inset(-30% 103% -30% -3%)" },
    { clipPath: "inset(-30% -3% -30% -3%)", opacity: 1, duration: d, ease: "none", stagger: o.st ?? 0, ...IR }, t);
}
// Trazo de tiza: la línea se dibuja en vivo.
const _largos = new Map();
// Las escenas que no están en pantalla al cargar están ocultas, y ahí getTotalLength()
// devuelve 0. Se mide una copia del trazo dentro de un SVG auxiliar que sí se dibuja.
function sonda(p) {
  let s = document.getElementById("sonda-trazos");
  if (!s) {
    s = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    s.id = "sonda-trazos";
    s.setAttribute("style", "position:fixed;left:0;top:0;width:10px;height:10px;visibility:hidden;pointer-events:none");
    document.body.appendChild(s);
  }
  const c = p.cloneNode(false);
  s.appendChild(c);
  return c;
}
function largo(p) {
  const c = sonda(p);
  const L = c.getTotalLength();
  c.remove();
  return L;
}
function preparaTrazos(x) {
  el(x).forEach((p) => {
    if (_largos.has(p)) return;
    const L = largo(p);
    _largos.set(p, L);
    p.style.strokeDasharray = L + " " + (L + 2);
    p.style.strokeDashoffset = L;
  });
}
function traza(x, t, d = 1, o = {}) {
  const ps = inicial(el(x), { opacity: 0 });
  preparaTrazos(ps);
  tl.fromTo(ps, { strokeDashoffset: (i, p) => _largos.get(p), opacity: 1 },
    { strokeDashoffset: 0, opacity: 1, duration: d, ease: o.ease ?? "power1.inOut", stagger: o.st ?? 0, ...IR }, t);
}
// Un objeto que recorre un trazo mientras se dibuja (Agar, los reyes, Abrán).
// Los puntos del camino se miden una sola vez al construir; durante el render solo se interpola.
function medirCamino(path, N = 400) {
  const p = sonda(el(path)[0]);
  const L = p.getTotalLength();
  const pts = [];
  for (let i = 0; i <= N; i++) { const q = p.getPointAtLength((L * i) / N); pts.push([q.x, q.y]); }
  p.remove();
  return pts;
}
function ponEnCamino(objs, pts, k) {
  const N = pts.length - 1;
  const f = Math.min(N, Math.max(0, k * N)), i = Math.floor(f), r = f - i, j = Math.min(N, i + 1);
  const x = pts[i][0] + (pts[j][0] - pts[i][0]) * r, y = pts[i][1] + (pts[j][1] - pts[i][1]) * r;
  objs.forEach((e) => e.setAttribute("transform", "translate(" + x.toFixed(2) + " " + y.toFixed(2) + ")"));
}
// Solo el primer recorrido de un objeto fija su posición inicial; los siguientes
// arrancan donde terminó el anterior.
const _colocados = new WeakSet();
function recorre(obj, path, t, d, o = {}) {
  const pts = typeof path === "string" || path instanceof Element ? medirCamino(path) : path;
  const objs = el(obj);
  const st = { k: o.desde ?? 0 };
  if (!objs.some((e) => _colocados.has(e))) { objs.forEach((e) => _colocados.add(e)); ponEnCamino(objs, pts, st.k); }
  tl.to(st, { k: o.hasta ?? 1, duration: d, ease: o.ease ?? "power1.inOut", onUpdate: () => ponEnCamino(objs, pts, st.k) }, t);
}
function cuenta(x, desde, hasta, t, d, fmt = (v) => Math.round(v).toString()) {
  const e = el(x)[0];
  const st = { v: desde };
  if (!_colocados.has(e)) { _colocados.add(e); e.textContent = fmt(desde); }
  tl.to(st, { v: hasta, duration: d, ease: "power1.out", onUpdate: () => (e.textContent = fmt(st.v)) }, t);
}
function camara(x, t, d, props, ease = "power2.inOut") {
  tl.to(el(x), { ...props, duration: d, ease }, t);
}
// Paneo lento sobre una ilustración (Ken Burns), sin salirse del marco.
function kb(x, t0, t1, desde, hasta) {
  tl.fromTo(el(x), { scale: desde.s ?? 1.08, xPercent: desde.x ?? 0, yPercent: desde.y ?? 0 },
    { scale: hasta.s ?? 1.0, xPercent: hasta.x ?? 0, yPercent: hasta.y ?? 0, duration: Math.max(0.1, t1 - t0), ease: "none" }, t0);
}
const fmtMiles = (v) => Math.round(v).toLocaleString("es-CO");

// ---------- piezas repetidas ----------
// Filtro de tiza para los trazos: borde levemente irregular.
root.insertAdjacentHTML("afterbegin",
  '<svg width="0" height="0" style="position:absolute"><defs>' +
  '<filter id="tz-' + ID + '" x="-5%" y="-5%" width="110%" height="110%">' +
  '<feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="3"/>' +
  '<feDisplacementMap in="SourceGraphic" scale="3"/></filter></defs></svg>');
const TIZA = "url(#tz-" + ID + ")";

// Tarjeta de capítulo: el número de capítulo y su subtítulo.
function capitulo(x, t0, t1) {
  const c = el(x)[0];
  entra(c.querySelector(".num"), t0, { y: 60, d: 0.8 });
  escribe(c.querySelector(".sub"), t0 + 0.5, 0.9);
  traza(c.querySelectorAll("path"), t0 + 0.3, 0.8);
  if (c.querySelector(".edad")) entra(c.querySelector(".edad"), t0 + 0.9, { y: 20 });
  sale(c, t1, { y: -60, d: 0.6 });
}

// Entrada y salida de toda la escena: el fondo es común, solo se funde el contenido.
function marco() {
  tl.fromTo($(".contenido"), { opacity: 0 }, { opacity: 1, duration: 0.5, ease: "none" }, 0);
  tl.to($(".contenido"), { opacity: 0, duration: 0.5, ease: "none" }, DUR - 0.55);
}

// Bloques de texto que se reemplazan en el mismo lugar: cada uno entra en su momento y sale
// justo antes del siguiente. Si `hasta` es null, el último se queda.
function secuencia(lista, hasta = null, o = {}) {
  lista.forEach(([s, t], i) => {
    entra(s, t, { y: o.y ?? 26, d: o.d ?? 0.55 });
    const sig = i < lista.length - 1 ? lista[i + 1][1] : hasta;
    if (sig != null) sale(s, sig - 0.4, { d: 0.35 });
  });
}
// Pone marcado SVG dentro de un elemento de la escena.
function pinta(sel, svg) { $(sel).innerHTML = svg; }

// ---------- mapas ----------
// Encuadre de cámara: lleva la región {x, y, w, h} de la imagen del mapa a la ventana
// {x, y, w, h} de la pantalla (relativa al contenedor .mapa), sin deformarla.
function encuadre(r, v) {
  const s = Math.min(v.w / r.w, v.h / r.h);
  return { scale: +s.toFixed(4), x: +(v.x + (v.w - r.w * s) / 2 - r.x * s).toFixed(1), y: +(v.y + (v.h - r.h * s) / 2 - r.y * s).toFixed(1) };
}
// Latido de un marcador: crece y vuelve, un número finito de veces.
function late(x, t, o = {}) {
  tl.fromTo(el(x), { scale: 1 }, { scale: o.s ?? 1.35, transformOrigin: "50% 50%", duration: o.d ?? 0.35, yoyo: true, repeat: o.n ?? 3, ease: "power1.inOut", immediateRender: false }, t);
}

// ---------- lecciones ----------
// Cada lección entra en su momento y sale antes de la siguiente; el número cuenta.
function lecciones(lista) {
  const cab = $(".seccion");
  if (cab) { entra(cab, 0.3, { y: -20 }); traza(".seccion-linea path", 0.6, 1.0); }
  secuencia(lista, null, { y: 30, d: 0.6 });
}
