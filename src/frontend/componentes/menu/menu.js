import { escaparHtml } from '../../utils/escapar-html.js';

/**
 * Navegação principal. Os itens vêm por parâmetro, então cada tela monta o seu.
 * No celular vira a barra fixa de baixo da tela.
 *
 * @param {Array<{ id: string, rotulo: string, icone: string, href: string }>} itens
 * @param {{ atual?: string }} [opcoes]  id do item da página atual (ganha destaque)
 * @returns {string} HTML
 *
 * Enquanto uma tela não existir, use href "#": o layout-home avisa "tela em construção".
 */
export function menu(itens, { atual = '' } = {}) {
  const links = itens.map((item) => {
    const paginaAtual = item.id === atual ? ' aria-current="page"' : '';
    return `<a href="${escaparHtml(item.href)}"${paginaAtual}><span class="menu__icone" aria-hidden="true">${escaparHtml(item.icone)}</span>${escaparHtml(item.rotulo)}</a>`;
  }).join('');
  return `<nav class="menu" aria-label="Principal">${links}</nav>`;
}
