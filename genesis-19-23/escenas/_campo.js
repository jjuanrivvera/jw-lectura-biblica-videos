// Plano esquemático del campo de Efrón (viewBox 0 0 1000 800), como la figura de la investigación:
// la Biblia no da su tamaño ni cuántos árboles tenía; solo que la cueva estaba "al final de su campo".
function campoSVG(p) {
  const arboles = [[170, 170], [300, 140], [440, 180], [590, 150], [730, 190], [210, 330], [370, 360], [520, 320], [680, 380], [180, 520], [340, 560], [500, 520], [640, 600]];
  let a = "";
  arboles.forEach(([x, y], i) => {
    a += `<g class="arbol a${i}"><ellipse cx="${x + 6}" cy="${y + 34}" rx="34" ry="10" fill="#000" opacity="0.25"/><circle cx="${x}" cy="${y}" r="38" fill="url(#${p}-copa)"/><circle cx="${x - 10}" cy="${y - 10}" r="14" fill="#b6d492" opacity="0.35"/></g>`;
  });
  return `
  <defs>
    <radialGradient id="${p}-copa" cx="40%" cy="35%" r="65%"><stop offset="0" stop-color="#8fb36f"/><stop offset="1" stop-color="#4f6e3d"/></radialGradient>
    <linearGradient id="${p}-roca" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#b3a78e"/><stop offset="1" stop-color="#6f6555"/></linearGradient>
    <pattern id="${p}-surcos" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M 0 20 L 40 20" stroke="#5f6b45" stroke-width="3"/></pattern>
  </defs>
  <rect class="suelo" x="80" y="80" width="840" height="640" rx="20" fill="#4a5638"/>
  <rect x="80" y="80" width="840" height="640" rx="20" fill="url(#${p}-surcos)" opacity="0.5"/>
  <g class="arboles">${a}</g>
  <g class="cueva"><path d="M 740 720 C 730 610 780 560 850 556 C 900 556 922 600 920 640 L 920 720 Z" fill="url(#${p}-roca)"/>
    <path d="M 792 720 C 792 668 816 640 846 640 C 876 640 892 668 892 720 Z" fill="#1d1812"/>
    <path class="doble" d="M 842 648 L 842 720" stroke="#3a3128" stroke-width="6"/></g>
  <rect class="limite" x="80" y="80" width="840" height="640" rx="20" fill="none" stroke="#e6bb5c" stroke-width="10" stroke-dasharray="30 18"/>
  <path class="marco-cueva" d="M 720 730 C 715 600 770 540 850 536 C 915 536 944 590 940 640 L 940 730 Z" fill="none" stroke="#e6bb5c" stroke-width="10"/>`;
}
