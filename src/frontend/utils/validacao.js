/* ==========================================================================
   Validação do login no navegador, com as MESMAS regras do back-end
   (src/backend/services/auth_service.py). Assim a tela não deixa passar algo que o
   servidor recusaria, e as mensagens são as mesmas dos dois lados.
   ========================================================================== */

export const FORMATO_EMAIL = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;

/**
 * @param {{ email: string, senha: string }} dados  e-mail já sem espaços nas pontas
 * @returns {{ campo: 'email'|'senha', mensagem: string } | null}
 */
export function validarLogin({ email, senha }) {
  if (!email) return { campo: 'email', mensagem: 'Preencha e-mail e senha.' };
  if (!senha.trim()) return { campo: 'senha', mensagem: 'Preencha e-mail e senha.' };
  if (!FORMATO_EMAIL.test(email)) return { campo: 'email', mensagem: 'E-mail inválido.' };
  return null;
}
