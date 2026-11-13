/*
 * Aplica o tema (claro/escuro) ANTES da página aparecer, para não piscar.
 * Script comum (sem "module"): carregue no <head>, antes dos CSS.
 * A chave "fb-theme" é a mesma usada em utils/tema.js.
 */
(function () {
  var tema = null;
  try { tema = localStorage.getItem('fb-theme'); } catch (e) {}
  if (tema !== 'dark' && tema !== 'light') {
    tema = window.matchMedia('(prefers-color-scheme:dark)').matches ? 'dark' : 'light';
  }
  document.documentElement.dataset.theme = tema;
})();
