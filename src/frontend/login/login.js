/* ==========================================================================
   Tela de login (issue #6, integrada à API na issue #16).
   - alterna entre o acesso do publicador e o do receptor (abas);
   - mostra/oculta a senha;
   - valida e-mail e senha no navegador, com as mesmas regras do back-end;
   - envia as credenciais para POST /auth/login e, se der certo, leva para a
     home do perfil devolvido pela API.
   ========================================================================== */
import { berry, berrySprite } from '../componentes/berry/berry.js';
import { marca } from '../componentes/cabecalho/cabecalho.js';
import { mostrarToast } from '../componentes/toast/toast.js';
import { alternarTema, atualizarBotoesTema } from '../utils/tema.js';
import { validarLogin } from '../utils/validacao.js';
import { login } from '../servicos/auth.js';

const PERFIS = {
  publicador: { titulo: 'Acesso do publicador', home: 'publicador/home.html' },
  receptor: { titulo: 'Acesso do receptor', home: 'receptor/home.html' },
};
const PERFIL_PADRAO = 'publicador';

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

/* ---------- mensagens de erro ---------- */
function limparErro(form) {
  form.querySelector('[data-erro]').textContent = '';
  form.querySelectorAll('input').forEach((i) => i.removeAttribute('aria-invalid'));
}

function mostrarErro(form, mensagem, campo) {
  form.querySelector('[data-erro]').textContent = mensagem;
  if (!campo) return;
  const elemento = form.elements[campo];
  elemento.setAttribute('aria-invalid', 'true');
  elemento.focus();
}

/* ---------- envio para a API ---------- */
/**
 * Envia as credenciais para POST /auth/login.
 * Sucesso: guarda a identidade devolvida e leva para a home do perfil.
 * Falha: mostra a mensagem devolvida pela API (ou uma mensagem de conexão).
 *
 * @param {HTMLFormElement} form
 * @param {{ perfil: 'publicador'|'receptor', email: string, senha: string, lembrar: boolean }} dados
 */
async function aoEnviarLogin(form, { perfil, email, senha, lembrar }) {
  const botao = form.querySelector('button[type="submit"]');
  const textoOriginal = botao.textContent;
  botao.disabled = true; // evita enviar duas vezes enquanto a resposta não volta
  botao.textContent = 'Entrando...';
  try {
    const usuario = await login(email, senha, perfil, { lembrar });
    location.assign(PERFIS[usuario.perfil].home);
  } catch (erro) {
    if (erro.status === 401) form.elements.senha.value = ''; // credenciais inválidas: limpa a senha
    mostrarErro(form, erro.message, erro.status === 401 ? 'senha' : undefined);
    botao.disabled = false;
    botao.textContent = textoOriginal;
  }
}

document.querySelectorAll('form[data-perfil]').forEach((form) => {
  form.addEventListener('input', () => limparErro(form));

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    if (form.querySelector('button[type="submit"]').disabled) return;
    limparErro(form);
    const dados = new FormData(form);
    const entrada = {
      perfil: form.dataset.perfil,
      email: String(dados.get('email')).trim(),
      senha: String(dados.get('senha')),
      lembrar: dados.get('lembrar') === 'on',
    };
    const erro = validarLogin(entrada);
    if (erro) {
      mostrarErro(form, erro.mensagem, erro.campo);
      return;
    }
    aoEnviarLogin(form, entrada);
  });
});
