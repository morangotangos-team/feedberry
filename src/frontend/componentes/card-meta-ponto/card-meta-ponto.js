import { escaparHtml } from '../../utils/escapar-html.js';
import { formatarData } from '../../utils/datas.js';
import { estadoVazio } from '../estado-vazio/estado-vazio.js';

/** Status conhecidos. A chave é o valor de `item.status`. */
export const STATUS = {
  'em-aberto': 'Em aberto',
  'em-andamento': 'Em andamento',
  'concluido': 'Concluído',
  'atrasado': 'Atrasado',
};

/**
 * Item com título, status e prazo. Serve para metas de desenvolvimento e para
 * pontos de melhoria.
 *
 * @param {object} item
 * @param {string} item.titulo
 * @param {'em-aberto'|'em-andamento'|'concluido'|'atrasado'} item.status
 * @param {string} [item.prazo]      "AAAA-MM-DD"
 * @param {string} [item.subtitulo]  linha de apoio (ex.: a pessoa a que o ponto se refere)
 * @returns {string} HTML
 */
export function cardMetaPonto({ titulo, status, prazo, subtitulo }) {
  const rotulo = STATUS[status] ?? status;
  const classe = STATUS[status] ? ` chip--${status}` : '';
  const apoio = subtitulo ? `<p class="meta-ponto__apoio">${escaparHtml(subtitulo)}</p>` : '';
  const dataPrazo = prazo
    ? `<p class="meta-ponto__prazo">Prazo: <time datetime="${escaparHtml(prazo)}">${formatarData(prazo)}</time></p>`
    : '';
  return `<article class="meta-ponto"><div class="meta-ponto__topo"><h3>${escaparHtml(titulo)}</h3><span class="chip${classe}">${escaparHtml(rotulo)}</span></div>${apoio}${dataPrazo}</article>`;
}

/**
 * Grade de cardMetaPonto, ou o estado vazio.
 * @param {Array} itens  mesmo formato de cardMetaPonto
 * @param {{ vazio?: { titulo: string, texto?: string } }} [opcoes]
 * @returns {string} HTML
 */
export function listaMetasPontos(itens, { vazio } = {}) {
  if (!itens.length) {
    return estadoVazio(vazio ?? { titulo: 'Nada por aqui', texto: 'Quando houver itens, eles aparecem aqui.' });
  }
  return `<div class="lista-metas">${itens.map(cardMetaPonto).join('')}</div>`;
}
