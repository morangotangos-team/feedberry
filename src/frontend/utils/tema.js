/**
 * Tema claro/escuro. O tema fica em <html data-theme="light|dark"> e é lembrado
 * no navegador (localStorage, chave "fb-theme"). A leitura inicial é feita por
 * utils/tema-inicial.js, carregado no <head>.
 *
 * Qualquer botão com data-acao="alternar-tema" tem o texto atualizado por aqui.
 */
const CHAVE = 'fb-theme';

export function temaAtual() {
  return document.documentElement.dataset.theme === 'dark' ? 'dark' : 'light';
}

export function definirTema(tema) {
  document.documentElement.dataset.theme = tema;
  try { localStorage.setItem(CHAVE, tema); } catch (e) { /* navegação privada: segue sem lembrar */ }
  atualizarBotoesTema();
}

export function alternarTema() {
  definirTema(temaAtual() === 'dark' ? 'light' : 'dark');
}

/** Atualiza o texto de todos os botões [data-acao="alternar-tema"] dentro de `raiz`. */
export function atualizarBotoesTema(raiz = document) {
  const escuro = temaAtual() === 'dark';
  raiz.querySelectorAll('[data-acao="alternar-tema"]').forEach((b) => {
    b.textContent = escuro ? '☀️ Tema claro' : '🌙 Tema noturno';
  });
}
