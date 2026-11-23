/* ==========================================================================
   Autenticação no front-end (issue #16).
   - login(): envia as credenciais para POST /auth/login;
   - guarda só a identidade devolvida pela API (nome, e-mail, perfil), nunca a senha;
   - usuarioLogado() / sair(): leem e apagam essa identidade.
   Limitação: ainda não há sessão nem token no back-end. O que fica guardado
   aqui só serve para a tela saber quem entrou; não protege páginas.
   ========================================================================== */
import { requisitar } from './api.js';

const CHAVE = 'fb-usuario';

/** Executa a ação em cada armazenamento, ignorando os que o navegador bloquear. */
function emCadaArmazenamento(acao) {
  for (const nome of ['sessionStorage', 'localStorage']) {
    try {
      const resultado = acao(window[nome]);
      if (resultado !== undefined) return resultado;
    } catch {
      /* navegação privada ou armazenamento bloqueado: segue sem guardar */
    }
  }
  return undefined;
}

/**
 * @param {string} email
 * @param {string} senha
 * @param {'publicador'|'receptor'} perfil
 * @param {{ lembrar?: boolean }} [opcoes]  "Manter conectado": guarda no localStorage
 * @returns {Promise<{ nome: string, email: string, perfil: string }>}
 * @throws {import('./api.js').ErroDeApi}
 */
export async function login(email, senha, perfil, { lembrar = false } = {}) {
  const { usuario } = await requisitar('/auth/login', { metodo: 'POST', corpo: { email, senha, perfil } });
  sair();
  try {
    (lembrar ? localStorage : sessionStorage).setItem(CHAVE, JSON.stringify(usuario));
  } catch {
    /* sem armazenamento: o login funciona, só não é lembrado */
  }
  return usuario;
}

/** @returns {{ nome: string, email: string, perfil: string } | null} */
export function usuarioLogado() {
  const salvo = emCadaArmazenamento((armazenamento) => armazenamento.getItem(CHAVE) ?? undefined);
  if (!salvo) return null;
  try {
    return JSON.parse(salvo);
  } catch {
    return null;
  }
}

export function sair() {
  emCadaArmazenamento((armazenamento) => {
    armazenamento.removeItem(CHAVE);
  });
}
