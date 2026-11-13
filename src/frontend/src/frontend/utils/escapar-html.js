/**
 * Escapa texto para ser colocado com segurança dentro de HTML (conteúdo e atributos).
 * Todo texto que vem dos dados (nomes, mensagens, títulos...) DEVE passar por aqui
 * antes de entrar em um template string.
 *
 * @param {unknown} valor  texto (ou qualquer valor, que vira texto). null/undefined viram "".
 * @returns {string}
 */
const MAPA = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' };

export function escaparHtml(valor) {
  if (valor === null || valor === undefined) return '';
  return String(valor).replace(/[&<>"']/g, (c) => MAPA[c]);
}
