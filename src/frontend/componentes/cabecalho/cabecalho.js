import { escaparHtml } from '../../utils/escapar-html.js';
import { logoBerry } from '../berry/berry.js';
import { avatar } from '../avatar/avatar.js';
import { alternarTema, atualizarBotoesTema } from '../../utils/tema.js';

/**
 * Nome FeedBerry com o logo. Com `href` vira link; sem `href`, é só a marca (ex.: no login).
 * @param {{ href?: string }} [opcoes]
 * @returns {string} HTML
 */
export function marca({ href = '' } = {}) {
  const conteudo = `${logoBerry()}<span class="marca__nome">Feed<span>Berry</span></span>`;
  return href
    ? `<a class="marca" href="${escaparHtml(href)}" aria-label="FeedBerry, ir para o início">${conteudo}</a>`
    : `<div class="marca">${conteudo}</div>`;
}

/**
 * Parte de cima da lateral: logo e dados de quem está logado.
 * @param {{ usuario: { nome: string, papel: string }, href?: string }} dados
 * @returns {string} HTML
 */
export function cabecalho({ usuario, href = '' }) {
  return `<header class="cabecalho">${marca({ href })}<div class="cabecalho__usuario">${avatar({ nome: usuario.nome, tamanho: 'sm' })}<div><strong>${escaparHtml(usuario.nome)}</strong><small>${escaparHtml(usuario.papel)}</small></div></div></header>`;
}

/**
 * Botões "Tema noturno" e "Sair", no alto da área de conteúdo.
 * @returns {string} HTML
 */
export function barraAcoes() {
  return `<div class="barra-acoes"><button class="btn ghost sm" type="button" data-acao="alternar-tema"></button><button class="btn ghost sm" type="button" data-acao="sair">Sair</button></div>`;
}

/**
 * Liga os botões de tema e de sair. Chame uma vez, depois de colocar o HTML na página.
 * @param {HTMLElement} raiz  elemento que contém o cabeçalho e a barra de ações
 * @param {{ aoSair: () => void }} opcoes  o que fazer ao clicar em Sair
 */
export function ativarCabecalho(raiz, { aoSair }) {
  atualizarBotoesTema(raiz);
  raiz.addEventListener('click', (evento) => {
    const botao = evento.target.closest('[data-acao]');
    if (!botao) return;
    if (botao.dataset.acao === 'alternar-tema') alternarTema();
    if (botao.dataset.acao === 'sair') aoSair();
  });
}
