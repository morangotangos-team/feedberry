import { escaparHtml } from '../../utils/escapar-html.js';
import { berry } from '../berry/berry.js';

/**
 * Topo da home: "Olá, {nome}!", um texto, botões de ação e o morango com sementes.
 *
 * @param {object} dados
 * @param {string} dados.nome
 * @param {string} dados.texto
 * @param {Array<{ texto: string, href: string, variante?: 'ghost' }>} [dados.acoes]
 *        a primeira é a ação principal; use variante 'ghost' para as secundárias
 * @param {number} [dados.sementes]  0 a 12 sementes preenchidas no morango
 * @returns {string} HTML
 */
export function saudacao({ nome, texto, acoes = [], sementes = 0 }) {
  const botoes = acoes.map((a) =>
    `<a class="btn${a.variante === 'ghost' ? ' ghost' : ''}" href="${escaparHtml(a.href)}">${escaparHtml(a.texto)}</a>`
  ).join('');
  return `<section class="saudacao"><div><h1>Olá, ${escaparHtml(nome)}!</h1><p>${escaparHtml(texto)}</p><div class="saudacao__acoes">${botoes}</div></div>${berry(sementes, { classe: 'saudacao__arte' })}</section>`;
}
