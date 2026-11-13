import { berrySprite } from '../berry/berry.js';
import { cabecalho, barraAcoes, ativarCabecalho } from '../cabecalho/cabecalho.js';
import { menu } from '../menu/menu.js';
import { mostrarToast } from '../toast/toast.js';

/**
 * Estrutura comum das duas homes: lateral (logo, menu, usuário) + área de conteúdo
 * (botões de tema/sair e o conteúdo da página).
 *
 * @param {object} dados
 * @param {{ nome: string, papel: string }} dados.usuario
 * @param {Array<{ id: string, rotulo: string, icone: string, href: string }>} dados.itensMenu
 * @param {string} dados.paginaAtual  id do item do menu que fica em destaque
 * @param {string} [dados.homeHref]   link do logo (padrão: a própria home)
 * @param {string} [dados.conteudo]   HTML do conteúdo da página
 * @returns {string} HTML
 */
export function layoutHome({ usuario, itensMenu, paginaAtual, homeHref = 'home.html', conteudo = '' }) {
  return `${berrySprite()}<div class="layout-home"><aside class="lateral">${cabecalho({ usuario, href: homeHref })}${menu(itensMenu, { atual: paginaAtual })}</aside><main class="principal" id="principal" tabindex="-1">${barraAcoes()}<div data-conteudo>${conteudo}</div></main></div>`;
}

/**
 * Troca só o conteúdo da página, sem redesenhar a lateral.
 * @param {HTMLElement} raiz  o mesmo elemento onde o layoutHome foi colocado
 * @param {string} html
 */
export function atualizarConteudo(raiz, html) {
  raiz.querySelector('[data-conteudo]').innerHTML = html;
}

/**
 * Liga o que é comum às duas homes: tema, Sair e links de telas que ainda não existem.
 * Chame uma vez, depois de colocar o layoutHome na página.
 *
 * @param {HTMLElement} raiz
 * @param {{ urlLogin?: string }} [opcoes]  para onde o Sair leva (padrão: ../index.html)
 */
export function ativarLayoutHome(raiz, { urlLogin = '../index.html' } = {}) {
  // TODO(back-end): encerrar a sessão (chamar a API de logout) antes de ir para o login.
  ativarCabecalho(raiz, { aoSair: () => location.assign(urlLogin) });

  // Links com href="#" são telas que serão criadas em outras issues.
  raiz.addEventListener('click', (evento) => {
    const link = evento.target.closest('a[href="#"]');
    if (!link) return;
    evento.preventDefault();
    mostrarToast('Tela em construção: ela será criada em outra issue.');
  });
}
