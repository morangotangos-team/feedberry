import { escaparHtml } from '../../utils/escapar-html.js';
import { paraData, partesDoDia, tempoRelativo } from '../../utils/datas.js';
import { estadoVazio } from '../estado-vazio/estado-vazio.js';

/**
 * Lista de lembretes por data (a mais próxima primeiro).
 *
 * @param {Array<{ id: number|string, titulo: string, subtitulo?: string, data: string }>} itens
 *        `data` no formato "AAAA-MM-DD"
 * @param {{ vazio?: { titulo: string, texto?: string } }} [opcoes]  mensagem quando não há itens
 * @returns {string} HTML
 */
export function listaLembretes(itens, { vazio } = {}) {
  if (!itens.length) {
    return estadoVazio(vazio ?? { titulo: 'Nenhum lembrete', texto: 'Quando houver, eles aparecem aqui.' });
  }
  const ordenados = [...itens].sort((a, b) => paraData(a.data) - paraData(b.data));
  const linhas = ordenados.map((item) => {
    const { dia, mes } = partesDoDia(item.data);
    const apoio = item.subtitulo ? `<div class="lembrete__apoio">${escaparHtml(item.subtitulo)}</div>` : '';
    return `<li class="lembrete"><time class="lembrete__data" datetime="${escaparHtml(item.data)}"><span class="lembrete__dia">${dia}</span><span class="lembrete__mes">${mes}</span></time><div class="lembrete__texto"><div class="lembrete__titulo">${escaparHtml(item.titulo)}</div>${apoio}</div><span class="lembrete__quando">${tempoRelativo(item.data)}</span></li>`;
  }).join('');
  return `<ul class="lembretes">${linhas}</ul>`;
}
