# Requisitos funcionais

Requisitos funcionais do **FeedBerry**, um para cada caso de uso (UC01 a UC14) da [análise dos artefatos](../analise/Analise%20dos%20artefatos.md). Os requisitos não funcionais estão em [Requisitos não funcionais](Requisitos%20nao%20funcionais.md), e a ligação com issue, documento e código está na [matriz de rastreabilidade](../rastreabilidade/Matriz%20de%20rastreabilidade.md).

| | |
|---|---|
| **Issue** | [#24](https://github.com/morangotangos-team/feedberry/issues/24) · [#31](https://github.com/morangotangos-team/feedberry/issues/31) |
| **Situação** | Proposta (ainda não validada com o cliente) |
| **Última atualização** | 2026-11-16 |

> ⚠️ Este documento é uma **proposta**. As prioridades foram sugeridas pela equipe a partir da quantidade de pedidos nos questionários e na entrevista, e precisam ser validadas com o cliente.

## 1. Fontes

| Código | Artefato |
|--------|----------|
| **Q1-x** | Formulário 1 (líderes, 4 respostas), pergunta da coluna x |
| **Q2-x** | Formulário 2 (colaboradores, 5 respostas), pergunta da coluna x |
| **FL** | Fluxograma da página de login (CT01 a CT06) |
| **E1-n** | Entrevista com o líder, pergunta n da transcrição (`entrevista/Entrevista com Lider/Entrevista-lider_transcricao.md`) |
| **DE** | Decisão da equipe, sem origem nos artefatos de levantamento |

As perguntas de cada coluna dos formulários estão na seção 6 da [análise dos artefatos](../analise/Analise%20dos%20artefatos.md). A gravação da reunião (E2) ainda não tem transcrição e não foi usada.

## 2. Requisitos funcionais

| Código | Requisito | Ator | Caso de uso | Fonte | Prioridade (proposta) |
|--------|-----------|------|-------------|-------|-----------------------|
| **RF01** | O sistema deve permitir que o usuário entre com e-mail e senha. | Usuário | UC01 | FL (CT01–CT05) | Alta |
| **RF02** | O sistema deve permitir a criação de uma conta de usuário. | Usuário | UC02 | FL (CT04) | Média |
| **RF03** | O sistema deve permitir que o líder registre e envie um feedback a um colaborador da sua equipe. | Líder | UC03 | Q1-F, Q1-G, Q1-L · E1-6, E1-11 | Alta |
| **RF04** | O sistema deve permitir que o líder registre os pontos de melhoria de um feedback e acompanhe a situação de cada um. | Líder | UC04 | Q1-M, Q2-L · E1-12 | Alta |
| **RF05** | O sistema deve permitir que o líder defina metas de desenvolvimento para um colaborador. | Líder | UC05 | Q1-K, Q2-I, Q2-K, Q2-M · E1-11, E1-12 | Média |
| **RF06** | O sistema deve permitir que o líder agende um retorno (lembrete de acompanhamento) sobre um feedback ou uma meta. | Líder | UC06 | Q1-K, Q1-L, Q1-M, Q2-M · E1-7, E1-10 | Alta |
| **RF07** | O sistema deve permitir que o líder acompanhe a evolução dos colaboradores da sua equipe. | Líder | UC07 | Q1-I, Q1-L, Q1-M · E1-1, E1-7 | Média |
| **RF08** | O sistema deve permitir que o líder gere relatórios a partir do acompanhamento da equipe. | Líder | UC08 | Q1-K, Q2-K | Baixa |
| **RF09** | O sistema deve permitir que o colaborador visualize os feedbacks que recebeu. | Colaborador | UC09 | Q2-F, Q2-G | Alta |
| **RF10** | O sistema deve manter e permitir consultar o histórico de feedbacks de cada colaborador. | Colaborador / Líder | UC10 | Q1-H, Q1-K (4/4), Q2-H, Q2-K, Q2-L, Q2-M · E1-6, E1-8, E1-11, E1-12 | Alta |
| **RF11** | O sistema deve permitir que o colaborador acompanhe as suas metas e a sua evolução. | Colaborador | UC11 | Q2-I, Q2-L, Q2-M | Média |
| **RF12** | O sistema deve permitir que o colaborador envie um feedback ao seu líder. | Colaborador | UC12 | Q2-J | Média |
| **RF13** | O sistema deve permitir que o colaborador envie o feedback ao líder de forma anônima. | Colaborador | UC13 | Q2-K (2), Q2-L | Média |
| **RF14** | O sistema deve avisar o usuário dos lembretes e retornos agendados. | Usuário | UC14 | Q1-K, Q2-K, Q2-L, Q2-M · E1-10, E1-11, E1-12 | Alta |

### Dependências entre requisitos

Seguem as relações entre os casos de uso da análise.

| Relação | Significado |
|---------|-------------|
| RF03 inclui RF04 | Todo feedback do líder registra pontos de melhoria |
| RF06 inclui RF14 | Agendar um retorno gera o lembrete |
| RF07 e RF11 dependem de RF10 | Acompanhar a evolução depende do histórico |
| RF08 estende RF07 | O relatório é opcional |
| RF13 estende RF12 | O anonimato é uma opção do envio ao líder |
| RF02 estende RF01 | "Criar conta" é oferecido no login (CT04) |

## 3. Pontos que dependem do cliente

As dúvidas da seção 5 da [análise dos artefatos](../analise/Analise%20dos%20artefatos.md) continuam abertas e podem mudar estes requisitos:

| Requisito | Dúvida da análise |
|-----------|-------------------|
| RF01 | 9 (o que acontece após 3 tentativas erradas) |
| RF02 | 2 (quem cria as contas) |
| RF03, RF07 | 3 (quem monta as equipes), 10 (feedback entre colegas) |
| RF05, RF11 | 7 (metas e promoção) |
| RF08 | 8 (conteúdo e formato do relatório) |
| RF13 | 4 (alcance do anonimato), 5 (quem vê os feedbacks) |
| RF06, RF14 | 6 (canal dos lembretes) |

## Histórico

| Data | Autor(a) | Alteração |
|------|----------|-----------|
| 2026-11-16 | Paula Silvério de Castro | Criação dos requisitos funcionais (issues #24 e #31) |
