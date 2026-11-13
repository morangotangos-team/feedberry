/**
 * Identidade visual: o morango (logo) e a ilustração com sementes.
 *
 * 1) Coloque berrySprite() UMA vez na página (o layout-home e o login já fazem isso).
 * 2) Use logoBerry() para o logo e berry(n) para o morango com n sementes.
 */
export const TOTAL_SEMENTES = 12;

const POSICOES = [[40, 52], [60, 48], [80, 52], [32, 74], [52, 70], [72, 70], [90, 74], [42, 94], [62, 90], [82, 94], [52, 110], [72, 110]];

/** Define o desenho do morango (símbolo #berry-shape). Invisível. */
export function berrySprite() {
  return `<svg class="berry-sprite" aria-hidden="true" focusable="false"><symbol id="berry-shape" viewBox="0 0 120 130">
    <path d="M60 28C30 24 10 46 18 78c8 30 32 46 42 48 10-2 34-18 42-48 8-32-12-54-42-50z" fill="var(--berry)"/>
    <ellipse cx="38" cy="54" rx="9" ry="16" transform="rotate(25 38 54)" fill="var(--brilho)" opacity=".18"/>
    <path d="M60 32C50 14 34 14 24 24c14 0 24 4 36 8zM60 32c10-18 26-18 36-8-14 0-24 4-36 8zM60 32c-3-12 0-22 5-28 3 10 2 20-5 28z" fill="var(--leaf)"/>
  </symbol></svg>`;
}

/** Morango pequeno, usado ao lado do nome FeedBerry. */
export function logoBerry() {
  return `<svg viewBox="0 0 120 130" class="berry-logo" aria-hidden="true"><use href="#berry-shape"/></svg>`;
}

/**
 * Morango grande com sementes preenchidas (cada semente = um feedback).
 *
 * @param {number} sementes  quantas sementes ficam amarelas (0 a 12)
 * @param {{ classe?: string }} [opcoes]  classe CSS extra, para o tamanho em cada tela
 * @returns {string} HTML
 */
export function berry(sementes, { classe = '' } = {}) {
  const n = Math.max(0, Math.min(TOTAL_SEMENTES, Math.floor(Number(sementes) || 0)));
  const elipses = POSICOES.map(([x, y], i) =>
    `<ellipse class="seed" style="--i:${i}" cx="${x}" cy="${y}" rx="2.8" ry="4.6" transform="rotate(${i % 2 ? -20 : 20} ${x} ${y})" fill="${i < n ? 'var(--seed)' : 'var(--brilho)'}" opacity="${i < n ? 1 : 0.35}"/>`
  ).join('');
  return `<svg viewBox="0 0 120 130" class="${classe}" role="img" aria-label="${n} de ${TOTAL_SEMENTES} sementes preenchidas"><use href="#berry-shape"/>${elipses}</svg>`;
}
