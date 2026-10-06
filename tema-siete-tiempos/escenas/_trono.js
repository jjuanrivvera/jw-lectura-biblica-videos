// Un trono dorado en un viewBox de 400x480. Clases: .tr-cuerpo, .tr-cinta (cadena con candado: reservado), .tr-borde (contorno punteado).
function tronoSVG(p) {
  return `
<svg viewBox="0 0 400 480" xmlns="http://www.w3.org/2000/svg">
<defs>
  <linearGradient id="${p}-or" x1="0" x2="1"><stop offset="0" stop-color="#8a6420"/><stop offset="0.45" stop-color="#f1cf72"/><stop offset="1" stop-color="#7a5418"/></linearGradient>
  <linearGradient id="${p}-te" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8e2f3a"/><stop offset="1" stop-color="#4f1720"/></linearGradient>
</defs>
<g class="tr-cuerpo">
  <path d="M 90 250 L 90 70 C 90 30 130 12 200 12 C 270 12 310 30 310 70 L 310 250 Z" fill="url(#${p}-or)" stroke="#5a3d10" stroke-width="5"/>
  <path d="M 120 240 L 120 84 C 120 56 150 42 200 42 C 250 42 280 56 280 84 L 280 240 Z" fill="url(#${p}-te)"/>
  <circle cx="200" cy="40" r="16" fill="#e8bd5f" stroke="#5a3d10" stroke-width="4"/>
  <rect x="50" y="232" width="300" height="56" rx="12" fill="url(#${p}-or)" stroke="#5a3d10" stroke-width="5"/>
  <rect x="40" y="190" width="40" height="110" rx="12" fill="url(#${p}-or)" stroke="#5a3d10" stroke-width="5"/>
  <rect x="320" y="190" width="40" height="110" rx="12" fill="url(#${p}-or)" stroke="#5a3d10" stroke-width="5"/>
  <path d="M 70 288 L 82 460 L 112 460 L 116 288 Z M 330 288 L 318 460 L 288 460 L 284 288 Z" fill="url(#${p}-or)" stroke="#5a3d10" stroke-width="5"/>
  <rect x="100" y="380" width="200" height="22" rx="8" fill="url(#${p}-or)" stroke="#5a3d10" stroke-width="4"/>
</g>
<g class="tr-cinta"><path d="M 44 214 Q 200 300 356 214" fill="none" stroke="#3b434a" stroke-width="22" stroke-linecap="round"/><path d="M 44 214 Q 200 300 356 214" fill="none" stroke="#c4ccd3" stroke-width="14" stroke-dasharray="26 10" stroke-linecap="round"/><rect x="170" y="236" width="60" height="64" rx="10" fill="#8f979e" stroke="#3b434a" stroke-width="5"/><path d="M 182 238 L 182 222 C 182 200 218 200 218 222 L 218 238" fill="none" stroke="#3b434a" stroke-width="8"/></g>
<path class="tr-borde" d="M 90 250 L 90 70 C 90 30 130 12 200 12 C 270 12 310 30 310 70 L 310 250 L 350 250 L 350 288 L 330 288 L 318 460 L 82 460 L 70 288 L 50 288 L 50 250 Z" fill="none" stroke="#e8bd5f" stroke-width="6" stroke-dasharray="14 12"/>
</svg>`;
}
