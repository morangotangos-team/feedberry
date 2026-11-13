import { escaparHtml } from '../../utils/escapar-html.js';

const QUANTIDADE_DE_CORES = 6; // --avatar-1 ... --avatar-6 em estilos/tokens.css

/** Mesma pessoa, mesma cor: a cor vem de uma conta simples sobre o nome. */
function indiceDaCor(nome) {
  let h = 0;
  for (const c of nome) h = (h * 31 + c.codePointAt(0)) >>> 0;
  return (h % QUANTIDADE_DE_CORES) + 1;
}

/**
 * Círculo com a inicial da pessoa.
 * Sem nome (ex.: feedback anônimo), mostra um círculo neutro com "?".
 *
 * @param {{ nome?: string|null, tamanho?: 'sm'|'md'|'lg' }} [opcoes]
 * @returns {string} HTML
 */
export function avatar({ nome = '', tamanho = 'md' } = {}) {
  const temNome = Boolean(nome);
  const inicial = temNome ? [...nome][0].toUpperCase() : '?';
  const cor = temNome ? indiceDaCor(nome) : 0;
  return `<span class="avatar avatar--${tamanho} avatar--cor-${cor}" aria-hidden="true">${escaparHtml(inicial)}</span>`;
}
