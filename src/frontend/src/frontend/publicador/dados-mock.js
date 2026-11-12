/* ==========================================================================
   Dados de exemplo da home do PUBLICADOR (issue #15). Nada aqui vem do back-end.
   Quando a API existir, troque este arquivo por chamadas de rede que devolvam
   dados NESTE MESMO FORMATO — a home.js não precisa mudar.

   Datas: "AAAA-MM-DD". Aqui usamos dataRelativa(n) só para o exemplo ficar
   sempre "recente" (n negativo = passado, positivo = futuro).
   ========================================================================== */
import { dataRelativa } from '../utils/datas.js';

/** Quem está logado. */
export const usuario = { id: 1, nome: 'Fernando', papel: 'Gerente de Projetos' };

/**
 * Feedbacks que o usuário enviou (UC10).
 * tipo: 'elogio' | 'construtivo' | 'ideia'
 */
export const feedbacksEnviados = [
  { id: 1, destinatario: { nome: 'Paula' },   tipo: 'elogio',      competencias: ['Entrega', 'Criatividade'], mensagem: 'Sua proposta de tela inicial ficou linda e muito clara. Parabéns pelo capricho!', data: dataRelativa(-1), anonimo: false },
  { id: 2, destinatario: { nome: 'Enzo' },    tipo: 'construtivo', competencias: ['Comunicação'],             mensagem: 'Seus commits estão ótimos, mas faltam descrições nos pull requests. Isso ajudaria a revisão.', data: dataRelativa(-4), anonimo: false },
  { id: 3, destinatario: { nome: 'Samara' },  tipo: 'ideia',       competencias: ['Colaboração'],             mensagem: 'Que tal apresentar a sua solução de testes para o time na próxima sprint? Pode ajudar muita gente.', data: dataRelativa(-6), anonimo: false },
  { id: 4, destinatario: { nome: 'Aimê' },    tipo: 'elogio',      competencias: ['Autonomia'],               mensagem: 'Gostei de como você conduziu a decisão sobre a arquitetura da API sem precisar de ajuda.', data: dataRelativa(-9), anonimo: false },
  { id: 5, destinatario: { nome: 'Matheus' }, tipo: 'elogio',      competencias: ['Entrega'],                 mensagem: 'A organização do backlog ficou excelente. Dá para saber exatamente o que vem a seguir.', data: dataRelativa(-12), anonimo: false },
];

/** Retornos agendados e lembretes de acompanhamento (UC06, UC14). */
export const retornosAgendados = [
  { id: 1, titulo: 'Retorno com Enzo',    subtitulo: 'Descrições nos pull requests',        data: dataRelativa(2) },
  { id: 2, titulo: 'Retorno com Samara',  subtitulo: 'Apresentação da solução de testes',   data: dataRelativa(5) },
  { id: 3, titulo: 'Check-in com Matheus', subtitulo: 'Acompanhar o backlog da sprint',     data: dataRelativa(12) },
];

/**
 * Pontos de melhoria registrados nos feedbacks e o status de cada um (UC04, UC07).
 * status: 'em-aberto' | 'em-andamento' | 'concluido' | 'atrasado'
 */
export const pontosMelhoria = [
  { id: 1, titulo: 'Descrever os pull requests',            subtitulo: 'Enzo · feedback de há 4 dias',   status: 'em-andamento', prazo: dataRelativa(10) },
  { id: 2, titulo: 'Compartilhar o progresso nas dailies',  subtitulo: 'Samara · feedback de há 6 dias', status: 'em-aberto',    prazo: dataRelativa(20) },
  { id: 3, titulo: 'Documentar decisões de arquitetura',    subtitulo: 'Aimê · feedback de há 9 dias',   status: 'atrasado',     prazo: dataRelativa(-2) },
  { id: 4, titulo: 'Pedir ajuda mais cedo quando travar',   subtitulo: 'Matheus · feedback de há 12 dias', status: 'concluido',  prazo: dataRelativa(-5) },
];
