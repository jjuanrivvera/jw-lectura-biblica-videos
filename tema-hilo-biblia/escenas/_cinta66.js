// Cinta de los 66 libros al pie: dice en qué parte del recorrido estamos (escenas 14 a 14e).
// Cada libro es una marca del color de su grupo; el grupo del que habla la voz se enciende y los demás se apagan.
// Requiere _libros.js y un <svg class="cinta66" viewBox="0 0 1920 120"></svg> en el marcado.
function cinta66() {
  const X0 = 110, X1 = 1810, PAS = (X1 - X0) / 66, Y = 30;
  let sv = '<line x1="' + X0 + '" y1="' + (Y + 26) + '" x2="' + X1 + '" y2="' + (Y + 26) + '" stroke="#ebbd5c" stroke-width="4" stroke-opacity="0.7"/>';
  LIBROS.forEach((l, i) => {
    const x = X0 + i * PAS + 2;
    sv += '<rect class="c66 c66g' + l[2] + ' c66-' + l[0] + '" x="' + x + '" y="' + Y + '" width="' + (PAS - 5) + '" height="52" rx="4" fill="' + GRUPOS[l[2]].c + '"/>';
  });
  GRUPOS.forEach((g, r) => {
    const libs = LIBROS.map((l, i) => [l, i]).filter(([l]) => l[2] === r);
    const xa = X0 + libs[0][1] * PAS, xb = X0 + (libs[libs.length - 1][1] + 1) * PAS;
    // Evangelios, Hechos y Apocalipsis son grupos angostos: su rótulo se alinea a un borde para no pisarse.
    const [xm, anc] = r === 4 ? [xb - 4, "end"] : r === 5 ? [xa + 2, "start"] : r === 7 ? [xb, "end"] : [(xa + xb) / 2, "middle"];
    sv += '<text class="c66t c66t' + r + '" x="' + xm + '" y="' + (Y + 86) + '" text-anchor="' + anc + '" font-family="Montserrat" font-weight="700" font-size="24" fill="' + g.c + '">' + g.n + '</text>';
  });
  $(".cinta66").innerHTML = sv;
  gsap.set($$(".c66, .c66t"), { opacity: 0.28 });
}
// Enciende los grupos indicados desde el instante t.
function focoCinta(grupos, t) {
  for (let r = 0; r < 8; r++) {
    const on = grupos.includes(r);
    tl.to($$(".c66g" + r + ", .c66t" + r), { opacity: on ? 1 : 0.28, duration: 0.5 }, t);
  }
}
