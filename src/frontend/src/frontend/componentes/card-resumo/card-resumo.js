import { escaparHtml } from '../../utils/escapar-html.js';

/**
 * Um número grande com o rótulo embaixo.
 * @param {{ valor: number|string, rotulo: string }} dados
 * @returns {string} HTML
 */
export function cardResumo({ valor, rotulo }) {
  return `<div class="card-resumo"><b class="card-resumo__valor">${escaparHtml(valor)}</b><span>${escaparHtml(rotulo)}</span></div>`;
}

/**
 * Faixa com vários cardResumo lado a lado (o bloco "Resumo" da home).
 * @param {Array<{ valor: number|string, rotulo: string }>} itens
 * @returns {string} HTML
 */
export function blocoResumo(itens) {
  return `<div class="resumo" role="group" aria-label="Resumo">${itens.map(cardResumo).join('')}</div>`;
}
