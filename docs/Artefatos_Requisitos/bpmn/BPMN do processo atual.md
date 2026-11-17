# BPMN do processo atual (AS-IS)

Processo de feedback como acontece hoje, montado a partir das entrevistas E1 (líder) e E2 (colaborador). D1 a D7 são as dores.

![BPMN do processo atual](BPMN%20processo%20atual.svg)

## 1. Raias

| Raia | Quem é |
|------|--------|
| **Líder / Gestor** | Quem dá o feedback e acompanha a equipe |
| **Colaborador** | Quem recebe o feedback |

## 2. Etapas

| # | Raia | Etapa | Fonte |
|---|------|-------|-------|
| 1 | Líder | Percebe um problema ou um bom trabalho (evento de início) | E1-4 |
| 2 | Líder | Chama o colaborador para conversar | E1-3, E1-5 |
| 3 | Líder | Dá o feedback e combina mudanças | E1-3 |
| 4 | Colaborador | Recebe e interpreta o feedback | E2-3, E2-10 |
| 5 | Líder | **Decisão:** registra o feedback? Sim: anota em caderno ou documento. Não: guarda só na memória | E1-6 |
| 6 | Colaborador | Tenta aplicar o que entendeu | E2-7 |
| 7 | Líder | Observa o trabalho nos dias seguintes | E1-7 |
| 8 | Líder | **Decisão:** lembrou de retomar o assunto? Sim: conversa de novo com o colaborador (fim: acompanhamento feito). Não: fim, assunto esquecido | E1-7, E1-10 |

## 3. Dores

| # | Dor | Etapa | Fonte |
|---|-----|-------|-------|
| D1 | Feedback reativo, só quando surge um problema | 1 | E1-4, E1-9, E2-4 |
| D2 | Sem padrão de canal (presencial, Teams ou mensagem) | 2 | E1-5, E2-5 |
| D3 | Sem registro: muita coisa fica só na memória | 5 | E1-6, E2-9 |
| D4 | Sem histórico único para consultar | 5 e 6 | E1-8, E2-6 |
| D5 | Esquecer de retomar o que foi combinado | 8 | E1-7, E1-10, E2-9 |
| D6 | Sem retorno para saber se melhorou | 6 | E2-7, E2-8 |
| D7 | Feedback vago, sem clareza do que mudar | 4 | E2-8, E2-10 |

## 4. Como o FeedBerry atende cada dor

| Dor | Requisitos |
|-----|------------|
| D1 | RF06, RF14 (retornos e lembretes tornam o feedback periódico) |
| D2 | RF03, RF12 (um canal único para enviar feedback) |
| D3 | RF03, RF04 |
| D4 | RF10, RNF07 |
| D5 | RF06, RF14 |
| D6 | RF04, RF07, RF11 |
| D7 | RF04, RF05 (pontos de melhoria e metas explícitos) |
