/* ==========================================================================
   Home do RECEPTOR (issue #15) · só front-end, dados de dados-mock.js.
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
import { usuario, feedbacksRecebidos, metas, pontosMelhoria, lembretes } from './dados-mock.js';

/* Telas deste perfil. href "#" = tela que será criada em outra issue
   (o clique mostra "Tela em construção"). Troque pelo caminho real quando existir. */
const ROTAS = {
  painel: 'home.html',
  recebidos: '#',
  historico: '#',
  metas: '#',
  lembretes: '#',
};

const ITENS_MENU = [
  { id: 'painel',    rotulo: 'Painel',    icone: '🏡', href: ROTAS.painel },
  { id: 'recebidos', rotulo: 'Recebidos', icone: '💌', href: ROTAS.recebidos },
  { id: 'historico', rotulo: 'Histórico', icone: '🗂️', href: ROTAS.historico },
  { id: 'metas',     rotulo: 'Metas',     icone: '🎯', href: ROTAS.metas },
  { id: 'lembretes', rotulo: 'Lembretes', icone: '🔔', href: ROTAS.lembretes },
];

const raiz = document.getElementById('raiz');

function montarConteudo() {
  const recebidos = feedbacksRecebidos.length;
  const metasEmAndamento = metas.filter((m) => m.status === 'em-andamento').length;
  const pontosAbertos = pontosMelhoria.filter((p) => p.status !== 'concluido').length;

  return [
    saudacao({
      nome: usuario.nome,
      texto: `Você tem ${recebidos} ${plural(recebidos, 'feedback', 'feedbacks')} no seu cesto. Cada semente é um retorno que ajuda você a crescer.`,
      acoes: [{ texto: 'Ver histórico', href: ROTAS.historico }],
      sementes: recebidos,
    }),

    blocoResumo([
      { valor: recebidos, rotulo: 'recebidos' },
      { valor: metasEmAndamento, rotulo: 'metas em andamento' },
      { valor: pontosAbertos, rotulo: 'pontos de melhoria em aberto' },
    ]),

    `<div class="home__colunas">${
      secao({
        titulo: 'Recebidos recentemente',
        link: { texto: 'Ver todos', href: ROTAS.recebidos },
        conteudo: listaFeedbacks(feedbacksRecebidos, {
          modo: 'recebido',
          vazio: { titulo: 'Seu cesto está vazio', texto: 'Quando alguém enviar um feedback para você, ele aparece aqui.' },
        }),
      }) + secao({
        titulo: 'Lembretes',
        link: { texto: 'Ver todos', href: ROTAS.lembretes },
        conteudo: listaLembretes(lembretes, {
          vazio: { titulo: 'Nenhum lembrete', texto: 'Os lembretes dos pontos combinados aparecem aqui.' },
        }),
      })
    }</div>`,

    `<div class="home__linha">${
      secao({
        titulo: 'Minhas metas',
        link: { texto: 'Ver todas', href: ROTAS.metas },
        conteudo: listaMetasPontos(metas, {
          vazio: { titulo: 'Você ainda não tem metas', texto: 'As metas de desenvolvimento combinadas com o seu líder aparecem aqui, com status e prazo.' },
        }),
      })
    }</div>`,
  ].join('');
}

function desenhar() {
  atualizarConteudo(raiz, montarConteudo());
}

raiz.innerHTML = layoutHome({ usuario, itensMenu: ITENS_MENU, paginaAtual: 'painel', homeHref: ROTAS.painel });
desenhar();
ativarLayoutHome(raiz);

raiz.addEventListener('click', (evento) => {
  const botao = evento.target.closest('[data-acao="agradecer"]');
  if (!botao) return;
  const feedback = feedbacksRecebidos.find((f) => String(f.id) === botao.dataset.id);
  if (!feedback) return;
  // TODO(back-end): registrar o agradecimento na API; só então marcar como agradecido.
  feedback.agradecido = true;
  desenhar();
  mostrarToast('Agradecimento enviado');
});
