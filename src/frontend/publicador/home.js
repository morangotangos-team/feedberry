/* ==========================================================================
   Home do PUBLICADOR (issue #15) · só front-end, dados de dados-mock.js.
   Regra: este arquivo importa apenas de ../componentes, ../utils e do próprio
   dados-mock.js. Nunca da pasta de outro perfil.
   ========================================================================== */
import { layoutHome, ativarLayoutHome, atualizarConteudo } from '../componentes/layout-home/layout-home.js';
import { saudacao } from '../componentes/saudacao/saudacao.js';
import { blocoResumo } from '../componentes/card-resumo/card-resumo.js';
import { secao } from '../componentes/secao/secao.js';
import { listaFeedbacks } from '../componentes/card-feedback/card-feedback.js';
import { listaLembretes } from '../componentes/lista-lembretes/lista-lembretes.js';
import { listaMetasPontos } from '../componentes/card-meta-ponto/card-meta-ponto.js';
import { mostrarToast } from '../componentes/toast/toast.js';
import { plural } from '../utils/plural.js';
import { usuario, feedbacksEnviados, retornosAgendados, pontosMelhoria } from './dados-mock.js';

/* Telas deste perfil. href "#" = tela que será criada em outra issue
   (o clique mostra "Tela em construção"). Troque pelo caminho real quando existir. */
const ROTAS = {
  painel: 'home.html',
  enviar: '#',
  enviados: '#',
  retornos: '#',
  melhorias: '#',
};

const ITENS_MENU = [
  { id: 'painel',    rotulo: 'Painel',    icone: '🏡', href: ROTAS.painel },
  { id: 'enviar',    rotulo: 'Enviar',    icone: '✍️', href: ROTAS.enviar },
  { id: 'enviados',  rotulo: 'Enviados',  icone: '🚀', href: ROTAS.enviados },
  { id: 'retornos',  rotulo: 'Retornos',  icone: '⏰', href: ROTAS.retornos },
  { id: 'melhorias', rotulo: 'Melhorias', icone: '🌱', href: ROTAS.melhorias },
];

const raiz = document.getElementById('raiz');

/* Bloco exclusivo do publicador: lista de retornos + ação de agendar (UC06, UC14). */
function blocoProximosRetornos() {
  const botaoAgendar = '<div class="retornos__acoes"><button class="btn ghost sm" type="button" data-acao="agendar-retorno">Agendar retorno</button></div>';
  return secao({
    titulo: 'Próximos retornos',
    conteudo: listaLembretes(retornosAgendados, {
      vazio: { titulo: 'Nenhum retorno agendado', texto: 'Agende um retorno para não esquecer de acompanhar o que foi combinado.' },
    }) + botaoAgendar,
  });
}

function montarConteudo() {
  const enviados = feedbacksEnviados.length;
  const pontosAbertos = pontosMelhoria.filter((p) => p.status !== 'concluido').length;

  return [
    saudacao({
      nome: usuario.nome,
      texto: `Você já enviou ${enviados} ${plural(enviados, 'feedback', 'feedbacks')}. Cada semente é um retorno que ajuda alguém do time a crescer.`,
      acoes: [{ texto: 'Enviar feedback', href: ROTAS.enviar }],
      sementes: enviados,
    }),

    blocoResumo([
      { valor: enviados, rotulo: 'enviados' },
      { valor: pontosAbertos, rotulo: 'pontos de melhoria em aberto' },
      { valor: retornosAgendados.length, rotulo: 'retornos agendados' },
    ]),

    `<div class="home__colunas">${
      secao({
        titulo: 'Enviados recentemente',
        link: { texto: 'Ver todos', href: ROTAS.enviados },
        conteudo: listaFeedbacks(feedbacksEnviados, {
          modo: 'enviado',
          vazio: { titulo: 'Você ainda não enviou feedbacks', texto: 'Quando enviar, os últimos aparecem aqui.', acao: { texto: 'Enviar o primeiro', href: ROTAS.enviar } },
        }),
      }) + blocoProximosRetornos()
    }</div>`,

    `<div class="home__linha">${
      secao({
        titulo: 'Pontos de melhoria em acompanhamento',
        link: { texto: 'Ver todos', href: ROTAS.melhorias },
        conteudo: listaMetasPontos(pontosMelhoria, {
          vazio: { titulo: 'Nenhum ponto em acompanhamento', texto: 'Os pontos registrados nos seus feedbacks aparecem aqui, com o status de cada um.' },
        }),
      })
    }</div>`,
  ].join('');
}

raiz.innerHTML = layoutHome({ usuario, itensMenu: ITENS_MENU, paginaAtual: 'painel', homeHref: ROTAS.painel });
atualizarConteudo(raiz, montarConteudo());
ativarLayoutHome(raiz);

raiz.addEventListener('click', (evento) => {
  if (!evento.target.closest('[data-acao="agendar-retorno"]')) return;
  // TODO(back-end): abrir o fluxo de agendamento (UC06) quando a tela existir.
  mostrarToast('Agendar retorno estará disponível em breve.');
});
