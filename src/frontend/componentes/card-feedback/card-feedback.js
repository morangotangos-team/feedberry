import { escaparHtml } from '../../utils/escapar-html.js';
import { paraData, tempoRelativo } from '../../utils/datas.js';
import { avatar } from '../avatar/avatar.js';
import { estadoVazio } from '../estado-vazio/estado-vazio.js';

/** Tipos de feedback conhecidos. A chave é o valor de `feedback.tipo`. */
export const TIPOS = {
  elogio: { rotulo: 'Elogio', icone: '🍓' },
  construtivo: { rotulo: 'Construtivo', icone: '🌱' },
  ideia: { rotulo: 'Ideia', icone: '💡' },
};

/** Quantos cards a home mostra em "recentes" (a issue pede de 3 a 5). */
const LIMITE_PADRAO = 4;

/**
 * Card de um feedback.
 *
 * @param {object} feedback
 * @param {number|string} feedback.id
 * @param {{ nome: string }|null} [feedback.autor]          quem escreveu
 * @param {{ nome: string }|null} [feedback.destinatario]   quem recebeu
 * @param {'elogio'|'construtivo'|'ideia'} feedback.tipo
 * @param {string[]} [feedback.competencias]
 * @param {string} feedback.mensagem
 * @param {string} feedback.data                            "AAAA-MM-DD" ou data e hora
 * @param {boolean} [feedback.anonimo]
 * @param {boolean} [feedback.agradecido]                   só no modo "recebido"
 * @param {{ modo?: 'enviado'|'recebido' }} [opcoes]
 *   - "enviado": mostra "Para {destinatário}"
 *   - "recebido": mostra "{autor}" e o botão Agradecer. Se o feedback for anônimo,
 *     mostra "Anônimo" e NÃO usa nome nem avatar do autor.
 * @returns {string} HTML
 *
 * O botão Agradecer traz data-acao="agradecer" e data-id: quem usa o card trata o clique.
 */
export function cardFeedback(feedback, { modo = 'recebido' } = {}) {
  const recebido = modo === 'recebido';
  const nome = recebido
    ? (feedback.anonimo ? null : feedback.autor?.nome ?? null)
    : feedback.destinatario?.nome ?? null;

  const titulo = recebido
    ? (nome ? `De ${nome}` : 'Anônimo')
    : `Para ${nome ?? ''}`.trim();
  const avisoAnonimo = !recebido && feedback.anonimo
    ? '<span class="card-feedback__anonimo">enviado como anônimo</span>'
    : '';

  const tipo = TIPOS[feedback.tipo];
  const chip = tipo
    ? `<span class="chip chip--${feedback.tipo}">${tipo.icone} ${tipo.rotulo}</span>`
    : '';
  const tags = (feedback.competencias ?? [])
    .map((t) => `<span class="tag">${escaparHtml(t)}</span>`).join('');

  let acao = '';
  if (recebido) {
    acao = feedback.agradecido
      ? '<span class="card-feedback__ok">Agradecido ✓</span>'
      : `<button class="btn ghost sm" type="button" data-acao="agradecer" data-id="${escaparHtml(feedback.id)}">Agradecer</button>`;
  }

  return `<article class="card-feedback">${avatar({ nome })}<div class="card-feedback__corpo"><header><strong>${escaparHtml(titulo)}</strong>${avisoAnonimo}<time class="card-feedback__quando" datetime="${escaparHtml(feedback.data)}">${tempoRelativo(feedback.data)}</time></header><p>${escaparHtml(feedback.mensagem)}</p><footer>${chip}${tags}${acao}</footer></div></article>`;
}

/**
 * Lista de cards, do mais novo para o mais antigo, ou o estado vazio.
 *
 * @param {Array} feedbacks  mesmo formato de cardFeedback
 * @param {object} [opcoes]
 * @param {'enviado'|'recebido'} [opcoes.modo]
 * @param {number|null} [opcoes.limite]  quantos mostrar (padrão 4; null = todos)
 * @param {{ titulo: string, texto?: string }} [opcoes.vazio]  mensagem quando não há itens
 * @returns {string} HTML
 */
export function listaFeedbacks(feedbacks, { modo = 'recebido', limite = LIMITE_PADRAO, vazio } = {}) {
  if (!feedbacks.length) {
    return estadoVazio(vazio ?? { titulo: 'Nada por aqui', texto: 'Quando houver feedbacks, eles aparecem aqui.' });
  }
  const ordenados = [...feedbacks].sort((a, b) => paraData(b.data) - paraData(a.data));
  const mostrados = limite === null ? ordenados : ordenados.slice(0, limite);
  return `<div class="lista-feedbacks">${mostrados.map((f) => cardFeedback(f, { modo })).join('')}</div>`;
}
