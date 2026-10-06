// Marcador de hijos por lados. `antes` son los que ya nacieron al empezar la escena;
// `nuevos` entran con la voz: [[".h-dan", t, "raq"], ...]. Solo cuentan los varones.
function marcador(antes, nuevos) {
  const todos = ["rub", "sim", "lev", "jud", "gad", "ase", "isa", "zab", "din", "dan", "nef", "jos"];
  const ya = new Set(antes);
  const futuros = new Set(nuevos.map((n) => n[0].replace(".h-", "")));
  todos.forEach((h) => { if (!ya.has(h) && !futuros.has(h)) $(".h-" + h).style.display = "none"; });
  const cuentaLado = (lado) => antes.filter((h) => h !== "din" && (lado === "lea" ? ["rub", "sim", "lev", "jud", "gad", "ase", "isa", "zab"] : ["dan", "nef", "jos"]).includes(h)).length;
  let n = { lea: cuentaLado("lea"), raq: cuentaLado("raq") };
  $(".n-lea").textContent = n.lea;
  $(".n-raq").textContent = n.raq;
  nuevos.forEach(([s, t, lado]) => {
    entra(s, t, { x: lado === "lea" ? -30 : 30, y: 0 });
    if (s === ".h-din") return;
    cuenta(".n-" + lado, n[lado], n[lado] + 1, t + 0.2, 0.4);
    late(".n-" + lado, t + 0.2, { s: 1.25, n: 1 });
    n[lado]++;
  });
}
