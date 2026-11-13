/* ==========================================================================
   Dados de exemplo da home do RECEPTOR (issue #15). Nada aqui vem do back-end.
   Quando a API existir, troque este arquivo por chamadas de rede que devolvam
   dados NESTE MESMO FORMATO — a home.js não precisa mudar.

   Feedback anônimo (UC13): a API NÃO deve enviar o autor. Por isso o item
   anônimo abaixo tem "anonimo: true" e "autor: null".

   Datas: "AAAA-MM-DD". Aqui usamos dataRelativa(n) só para o exemplo ficar
   sempre "recente" (n negativo = passado, positivo = futuro).
   ========================================================================== */
import { dataRelativa } from '../utils/datas.js';

/** Quem está logado. */
export const usuario = { id: 2, nome: 'Paula', papel: 'Desenvolvedora' };

/**
 * Feedbacks que o usuário recebeu (UC09, UC10).
 * tipo: 'elogio' | 'construtivo' | 'ideia'
 */
export const feedbacksRecebidos = [
  { id: 1, autor: { nome: 'Fernando' }, tipo: 'elogio',      competencias: ['Entrega', 'Criatividade'], mensagem: 'Sua proposta de tela inicial ficou linda e muito clara. Parabéns pelo capricho!', data: dataRelativa(-1), anonimo: false, agradecido: false },
  { id: 2, autor: null,                 tipo: 'ideia',       competencias: ['Colaboração'],             mensagem: 'Que tal fazer uma demonstração rápida do seu protótipo para o time todo? Todo mundo ia aprender com o seu processo.', data: dataRelativa(-2), anonimo: true,  agradecido: false },
  { id: 3, autor: { nome: 'Samara' },   tipo: 'construtivo', competencias: ['Comunicação'],             mensagem: 'Nas últimas revisões, compartilhar a tela antes da reunião ajudaria a gente a acompanhar melhor o que você mostra.', data: dataRelativa(-4), anonimo: false, agradecido: true },
  { id: 4, autor: { nome: 'Matheus' },  tipo: 'elogio',      competencias: ['Autonomia'],               mensagem: 'Valeu por resolver o problema do layout sem precisar de ninguém. Aprendi bastante olhando a sua solução.', data: dataRelativa(-7), anonimo: false, agradecido: true },
  { id: 5, autor: { nome: 'Enzo' },     tipo: 'ideia',       competencias: ['Criatividade'],            mensagem: 'Podemos pensar em um mural de conquistas da equipe na página inicial. Combina com o seu estilo!', data: dataRelativa(-10), anonimo: false, agradecido: false },
];

/**
 * Metas de desenvolvimento do usuário (UC05, UC11).
 * status: 'em-aberto' | 'em-andamento' | 'concluido' | 'atrasado'
 */
export const metas = [
  { id: 1, titulo: 'Apresentar a arquitetura da API ao time', status: 'em-andamento', prazo: dataRelativa(14) },
  { id: 2, titulo: 'Cobrir o login com testes automatizados', status: 'em-andamento', prazo: dataRelativa(7) },
  { id: 3, titulo: 'Estudar acessibilidade em formulários',   status: 'em-aberto',    prazo: dataRelativa(30) },
  { id: 4, titulo: 'Concluir o curso de UX writing',          status: 'concluido',    prazo: dataRelativa(-3) },
];

/**
 * Pontos de melhoria combinados com o líder (UC09, UC11). A home só mostra a
 * quantidade em aberto, no resumo.
 */
export const pontosMelhoria = [
  { id: 1, titulo: 'Compartilhar a tela antes das reuniões', status: 'em-andamento' },
  { id: 2, titulo: 'Avisar mudanças de prazo com antecedência', status: 'em-aberto' },
  { id: 3, titulo: 'Escrever descrições nos pull requests', status: 'concluido' },
];

/** Lembretes dos pontos combinados (UC14). */
export const lembretes = [
  { id: 1, titulo: 'Retomar o ponto: compartilhar a tela', subtitulo: 'Combinado com Fernando', data: dataRelativa(2) },
  { id: 2, titulo: 'Revisar a meta de testes automatizados', subtitulo: 'Meta em andamento',     data: dataRelativa(6) },
  { id: 3, titulo: 'Conversa de acompanhamento mensal',      subtitulo: 'Combinado com Fernando', data: dataRelativa(15) },
];
