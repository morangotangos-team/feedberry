/* ==========================================================================
   Tela de login (issue #6) · só front-end.
   - alterna entre o acesso do publicador e o do receptor (abas);
   - mostra/oculta a senha;
   - valida e-mail e senha no navegador.
   Não há autenticação aqui: ela será ligada na issue #16 (API) / #9 (back-end).
   ========================================================================== */
import { berry, berrySprite } from '../componentes/berry/berry.js';
import { marca } from '../componentes/cabecalho/cabecalho.js';
import { mostrarToast } from '../componentes/toast/toast.js';
import { alternarTema, atualizarBotoesTema } from '../utils/tema.js';

const PERFIS = {
  publicador: { titulo: 'Acesso do publicador' },
  receptor: { titulo: 'Acesso do receptor' },
};
const PERFIL_PADRAO = 'publicador';
const SENHA_MINIMA = 6;
const FORMATO_EMAIL = /^\S+@\S+\.\S+$/;

/* ---------- identidade visual ---------- */
document.body.insertAdjacentHTML('afterbegin', berrySprite());
document.querySelector('[data-marca]').innerHTML = marca();
document.querySelector('[data-berry]').innerHTML = berry(12);

/* ---------- tema ---------- */
atualizarBotoesTema();
document.querySelector('[data-acao="alternar-tema"]').addEventListener('click', alternarTema);

/* ---------- abas: publicador / receptor ---------- */
const abas = [...document.querySelectorAll('[role="tab"]')];

function perfilDaUrl() {
  const perfil = location.hash.slice(1);
  return perfil in PERFIS ? perfil : PERFIL_PADRAO;
}

function selecionarPerfil(perfil, { foco = false } = {}) {
  abas.forEach((aba) => {
    const ativa = aba.dataset.perfil === perfil;
    aba.setAttribute('aria-selected', String(ativa));
    aba.tabIndex = ativa ? 0 : -1;
    document.getElementById(aba.getAttribute('aria-controls')).hidden = !ativa;
    if (ativa && foco) aba.focus();
  });
  document.title = `${PERFIS[perfil].titulo} · FeedBerry`;
}

abas.forEach((aba, i) => {
  aba.addEventListener('click', () => {
    selecionarPerfil(aba.dataset.perfil);
    history.replaceState(null, '', `#${aba.dataset.perfil}`); // permite abrir direto em index.html#receptor
  });
  aba.addEventListener('keydown', (e) => {
    const destino = { ArrowRight: i + 1, ArrowLeft: i - 1, Home: 0, End: abas.length - 1 }[e.key];
    if (destino === undefined) return;
    e.preventDefault();
    const proxima = abas[(destino + abas.length) % abas.length];
    selecionarPerfil(proxima.dataset.perfil, { foco: true });
    history.replaceState(null, '', `#${proxima.dataset.perfil}`);
  });
});
addEventListener('hashchange', () => selecionarPerfil(perfilDaUrl()));
selecionarPerfil(perfilDaUrl());

/* ---------- mostrar / ocultar senha ---------- */
document.querySelectorAll('[data-alternar-senha]').forEach((botao) => {
  botao.addEventListener('click', () => {
    const campo = document.getElementById(botao.getAttribute('aria-controls'));
    const mostrar = campo.type === 'password';
    campo.type = mostrar ? 'text' : 'password';
    botao.setAttribute('aria-label', mostrar ? 'Ocultar senha' : 'Mostrar senha');
    botao.setAttribute('aria-pressed', String(mostrar));
    botao.textContent = mostrar ? '🙈' : '👁️';
  });
});

/* ---------- "Esqueci minha senha" (só visual) ---------- */
document.querySelectorAll('[data-esqueci]').forEach((link) => {
  link.addEventListener('click', (e) => {
    e.preventDefault();
    mostrarToast('Recuperação de senha em breve');
  });
});

/* ---------- validação ---------- */
/** @returns {{ campo: 'email'|'senha', mensagem: string } | null} */
function validar({ email, senha }) {
  if (!email) return { campo: 'email', mensagem: 'Digite o seu e-mail.' };
  if (!FORMATO_EMAIL.test(email)) return { campo: 'email', mensagem: 'Digite um e-mail válido, como nome@empresa.com.' };
  if (!senha) return { campo: 'senha', mensagem: 'Digite a sua senha.' };
  if (senha.length < SENHA_MINIMA) return { campo: 'senha', mensagem: `A senha precisa ter pelo menos ${SENHA_MINIMA} caracteres.` };
  return null;
}

function limparErro(form) {
  form.querySelector('[data-erro]').textContent = '';
  form.querySelectorAll('input').forEach((i) => i.removeAttribute('aria-invalid'));
}

/**
 * Chamado quando e-mail e senha passam na validação.
 * TODO(#16): trocar este aviso pela chamada à API de autenticação (JavaScript, fetch).
 * TODO(#9 / #16): depois do login real, levar a pessoa para publicador/home.html ou
 *                 receptor/home.html, conforme o perfil devolvido pela API.
 *
 * @param {{ perfil: 'publicador'|'receptor', email: string, senha: string, lembrar: boolean }} dados
 */
function aoEnviarLogin({ perfil }) {
  mostrarToast(`Dados válidos (${perfil}). A API de login será ligada em outra issue.`);
}

document.querySelectorAll('form[data-perfil]').forEach((form) => {
  form.addEventListener('input', () => limparErro(form));

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    limparErro(form);
    const dados = new FormData(form);
    const entrada = {
      perfil: form.dataset.perfil,
      email: String(dados.get('email')).trim(),
      senha: String(dados.get('senha')),
      lembrar: dados.get('lembrar') === 'on',
    };
    const erro = validar(entrada);
    if (erro) {
      form.querySelector('[data-erro]').textContent = erro.mensagem;
      const campo = form.elements[erro.campo];
      campo.setAttribute('aria-invalid', 'true');
      campo.focus();
      return;
    }
    aoEnviarLogin(entrada);
  });
});
