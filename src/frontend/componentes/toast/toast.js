/**
 * Aviso rápido no rodapé da tela ("Agradecimento enviado").
 * Não precisa de HTML na página: o elemento é criado aqui.
 */
let elemento = null;
let temporizador = null;

function garantirElemento() {
  if (!elemento) {
    elemento = document.createElement('div');
    elemento.className = 'toast';
    elemento.setAttribute('role', 'status');
    elemento.setAttribute('aria-live', 'polite');
    document.body.append(elemento);
  }
  return elemento;
}

/**
 * @param {string} texto
 * @param {{ duracao?: number }} [opcoes]  tempo na tela, em milissegundos
 */
export function mostrarToast(texto, { duracao = 2600 } = {}) {
  const el = garantirElemento();
  el.textContent = texto;
  el.classList.add('on');
  clearTimeout(temporizador);
  temporizador = setTimeout(() => el.classList.remove('on'), duracao);
}

// Cria o elemento já na carga, para o leitor de tela reconhecer a região de avisos.
if (document.body) garantirElemento();
