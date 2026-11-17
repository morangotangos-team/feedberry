import { escaparHtml } from '../../utils/escapar-html.js';

/**
 * Bloco da home: título (com link opcional, como "Ver todos") e o conteúdo.
 *
 * @param {object} dados
 * @param {string} dados.titulo
 * @param {{ texto: string, href: string }} [dados.link]  link no canto do título
 * @param {string} dados.conteudo  HTML já pronto (vindo de outros componentes)
 * @returns {string} HTML
 */
export function secao({ titulo, link = null, conteudo = '' }) {
  const verTodos = link
    ? `<a class="secao__link" href="${escaparHtml(link.href)}">${escaparHtml(link.texto)}</a>`
    : '';
  return `<section class="secao"><div class="secao__topo"><h2>${escaparHtml(titulo)}</h2>${verTodos}</div>${conteudo}</section>`;
}
