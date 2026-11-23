import { escaparHtml } from '../../utils/escapar-html.js';

/**
 * Mensagem para quando uma lista não tem itens.
 * Diga o que aconteceu e, se der, o que a pessoa pode fazer.
 *
 * @param {{ titulo: string, texto?: string, acao?: { texto: string, href: string } }} dados
 * @returns {string} HTML
 */
export function estadoVazio({ titulo, texto = '', acao = null }) {
  const botao = acao
    ? `<div class="estado-vazio__acao"><a class="btn" href="${escaparHtml(acao.href)}">${escaparHtml(acao.texto)}</a></div>`
    : '';
  return `<div class="estado-vazio"><b>${escaparHtml(titulo)}</b>${escaparHtml(texto)}${botao}</div>`;
}
