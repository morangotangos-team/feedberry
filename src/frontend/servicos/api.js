/* ==========================================================================
   Única porta de saída para a API do FeedBerry (issue #16).
   Toda chamada HTTP do front-end passa por aqui: monta o JSON, lê a resposta
   com segurança (nem toda resposta de erro vem em JSON) e transforma falhas
   em mensagens que podem ir direto para a tela.
   ========================================================================== */

export class ErroDeApi extends Error {
  /**
   * @param {string} mensagem  texto pronto para mostrar ao usuário
   * @param {number} status    status HTTP (0 quando nem chegou ao servidor)
   */
  constructor(mensagem, status) {
    super(mensagem);
    this.name = 'ErroDeApi';
    this.status = status;
  }
}

const SEM_CONEXAO = 'Não foi possível conectar ao FeedBerry. Verifique sua conexão.';
const GRANDE_DEMAIS = 'Os dados enviados são grandes demais.';
const ERRO_GENERICO = 'Não foi possível concluir agora. Tente novamente em instantes.';

/** Lê o corpo como JSON só quando o servidor disse que é JSON. */
async function lerJson(resposta) {
  const tipo = resposta.headers.get('Content-Type') || '';
  if (!tipo.includes('application/json')) return null;
  try {
    return await resposta.json();
  } catch {
    return null;
  }
}

/**
 * Faz uma requisição à API, na mesma origem da página (ADR-005).
 *
 * @param {string} caminho  ex.: '/auth/login'
 * @param {{ metodo?: string, corpo?: object }} [opcoes]
 * @returns {Promise<object>} o JSON da resposta de sucesso
 * @throws {ErroDeApi}
 */
export async function requisitar(caminho, { metodo = 'GET', corpo } = {}) {
  let resposta;
  try {
    resposta = await fetch(caminho, {
      method: metodo,
      headers: corpo === undefined ? {} : { 'Content-Type': 'application/json' },
      body: corpo === undefined ? undefined : JSON.stringify(corpo),
    });
  } catch {
    throw new ErroDeApi(SEM_CONEXAO, 0);
  }

  const json = await lerJson(resposta);
  if (resposta.ok && json) return json;

  // O back-end devolve "mensagem" pronta para o usuário nos erros que ele trata (400, 401).
  if (json && typeof json.mensagem === 'string') throw new ErroDeApi(json.mensagem, resposta.status);
  if (resposta.status === 413) throw new ErroDeApi(GRANDE_DEMAIS, 413);
  throw new ErroDeApi(ERRO_GENERICO, resposta.status);
}
