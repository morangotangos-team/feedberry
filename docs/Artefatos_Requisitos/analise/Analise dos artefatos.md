# Análise dos artefatos de requisitos

Análise feita na **2ª etapa** do [Processo de levantamento de requisitos](../../Processos_De_Requisitos/Processo%20de%20levantamento%20de%20requisitos.md), a partir dos artefatos da 1ª etapa. Ela serve de base para o [diagrama de contexto](../diagramas/diagrama-de-contexto.svg) e para o [diagrama de casos de uso](../diagramas/diagrama-de-casos-de-uso.svg).

## 1. Artefatos analisados

| Código | Artefato | Onde está | Situação |
|--------|----------|-----------|----------|
| **Q1** | Formulário 1 — líderes (4 respostas) | [questionario/README.md](../questionario/README.md) | ✅ Analisado |
| **Q2** | Formulário 2 — colaboradores (5 respostas) | [questionario/README.md](../questionario/README.md) | ✅ Analisado |
| **FL** | Fluxograma da página de login | [Diagrama_Fluxograma_PaginaLogin](../Diagrama_Fluxograma_PaginaLogin/feedberry-login.drawio.pdf) | ✅ Analisado |
| **E1** | Entrevista com o líder (áudio, ~10 min) | `entrevista/Entrevista com Lider.rar` | ⏳ Pendente de transcrição |
| **E2** | Gravação da reunião (áudio, ~10 min) | `entrevista/Gravação-da-Reunião.mp3` | ⏳ Pendente de transcrição |

Nas tabelas abaixo, a referência `Q1-L` indica a pergunta da coluna L do Formulário 1 (ver seção 6), e `Q2-K` a coluna K do Formulário 2. A contagem entre parênteses é o número de respostas que citam o ponto.

> ⚠️ As entrevistas (E1 e E2) ainda não têm transcrição em texto no repositório. Os atores e casos de uso abaixo foram rastreados aos questionários e ao fluxograma; quando a transcrição for adicionada, a coluna **Fonte** deve ser complementada com E1/E2.

## 2. Resumo das respostas

**Líderes (Q1, 4 respostas)**
- Todos registram os feedbacks hoje **em planilha ou papel**.
- Metade acha **difícil lembrar** o que foi combinado em feedbacks anteriores, e metade acha **difícil acompanhar a evolução** de cada pessoa.
- Gastam de menos de 1h a 3h por semana com feedbacks.
- Funções mais pedidas: **Histórico (4/4)**, Metas de desenvolvimento (2), Lembretes (1), Relatórios (1).
- Dificuldades citadas: lembrar, não conseguir guardar o histórico, falta de tempo, muitos colaboradores para acompanhar e o feedback ser recebido como algo pessoal.

**Colaboradores (Q2, 5 respostas)**
- Recebem feedback “às vezes” ou “frequentemente”, mas a clareza é, em geral, média.
- **3 de 5 não conseguem consultar feedbacks antigos.**
- Nem todos sabem quais são suas metas de desenvolvimento.
- A maioria se sente confortável em dar feedback ao líder, mas há quem se sinta pouco confortável.
- Funções mais pedidas: Histórico (2), Metas de desenvolvimento (2), Relatórios (2), **Feedback anônimo (2)**, Lembretes (1).
- Dificuldades citadas: não ter histórico, não saber se melhorou no ponto apontado, esquecer o que foi dito, imparcialidade e falta de privacidade nas conversas “particulares”.

## 3. Atores

| Ator | Descrição | Fonte |
|------|-----------|-------|
| **Usuário** | Ator genérico: qualquer pessoa com conta no FeedBerry. Faz login, cria conta e recebe lembretes. | FL |
| **Colaborador** | Recebe feedbacks, consulta o histórico, acompanha as próprias metas e pode dar feedback ao líder. É um Usuário. | Q2 (todas as perguntas) |
| **Líder / Gestor** | Dá feedback aos colaboradores da equipe, registra pontos de melhoria, define metas e acompanha a evolução da equipe. Também é um Colaborador, pois recebe feedback e tem metas. | Q1 (todas as perguntas); Q2-J |
| **Serviço de notificação** *(entidade externa, a confirmar)* | Sistema externo (ex.: e-mail) que entrega lembretes e avisos de novo feedback. | Q1-K, Q1-M, Q2-K, Q2-M (pedidos de lembretes) |

## 4. Funcionalidades (casos de uso)

| ID | Caso de uso | Ator principal | Fonte |
|----|-------------|----------------|-------|
| UC01 | Fazer login (e-mail e senha) | Usuário | FL (CT01–CT05) |
| UC02 | Criar conta | Usuário | FL (CT04 oferece “Criar conta”) |
| UC03 | Enviar feedback ao colaborador | Líder | Q1-F, Q1-G, Q1-L |
| UC04 | Registrar pontos de melhoria *(incluído em UC03)* | Líder | Q1-M, Q2-L |
| UC05 | Definir metas de desenvolvimento | Líder | Q1-K (2), Q2-I, Q2-K (2), Q2-M |
| UC06 | Agendar retorno / lembrete de acompanhamento | Líder | Q1-K, Q1-L (“lembrar”), Q1-M, Q2-M (retorno semanal/mensal/trimestral) |
| UC07 | Acompanhar evolução da equipe | Líder | Q1-I, Q1-M (3), Q1-L |
| UC08 | Gerar relatórios *(estende UC07)* | Líder | Q1-K, Q2-K (2) |
| UC09 | Visualizar feedbacks recebidos | Colaborador | Q2-F, Q2-G |
| UC10 | Consultar histórico de feedbacks | Colaborador / Líder | Q1-K (4/4), Q1-H, Q2-H, Q2-K, Q2-L, Q2-M |
| UC11 | Acompanhar metas e evolução pessoal | Colaborador | Q2-I, Q2-L, Q2-M |
| UC12 | Enviar feedback ao líder | Colaborador | Q2-J |
| UC13 | Enviar feedback anônimo *(estende UC12)* | Colaborador | Q2-K (2), Q2-L (imparcialidade, privacidade) |
| UC14 | Receber lembretes | Usuário | Q1-K, Q2-K, Q2-L, Q2-M |

### Relações entre casos de uso

| Relação | Justificativa |
|---------|---------------|
| UC03 `<<include>>` UC04 | Todo feedback do líder registra os pontos de melhoria, que depois são acompanhados. |
| UC06 `<<include>>` UC14 | Agendar um retorno gera o lembrete que o usuário vai receber. |
| UC07 `<<include>>` UC10 | Acompanhar a evolução da equipe depende de consultar o histórico. |
| UC11 `<<include>>` UC10 | Acompanhar a evolução pessoal depende de consultar o histórico. |
| UC08 `<<extend>>` UC07 | O relatório é opcional, a partir do acompanhamento da equipe. |
| UC13 `<<extend>>` UC12 | O anonimato é uma opção ao enviar feedback ao líder. |
| UC02 `<<extend>>` UC01 | “Criar conta” é oferecido no login quando o usuário não é encontrado (CT04). |

## 5. Dúvidas para confirmar com o cliente

1. **Entrevistas:** o que foi dito em E1 e E2 confirma os atores e as funcionalidades acima? (Falta transcrever os áudios.)
2. **Quem cria as contas?** O fluxograma oferece “Criar conta” ao usuário, mas não fica claro se é cadastro livre ou feito por um administrador/RH. Se houver administrador, ele entra como novo ator.
3. **Equipes:** o README fala em feedback “entre pessoas e equipes”. Quem monta as equipes e define quem é líder de quem? Existe feedback para a equipe inteira?
4. **Feedback anônimo:** vale só do colaborador para o líder ou também entre colegas? O líder pode ver quem enviou?
5. **Privacidade:** quem pode ver os feedbacks de um colaborador (só ele e o líder, ou também RH/diretoria)?
6. **Lembretes:** serão por e-mail, notificação dentro do sistema ou ambos? Isso define se o Serviço de notificação é uma entidade externa.
7. **Metas e promoção:** um colaborador pediu para ver “o quão perto” está de uma promoção. Isso entra no escopo?
8. **Relatórios:** que informações o relatório precisa mostrar e em que formato (tela, PDF, planilha)?
9. **Bloqueio de login:** o fluxograma prevê ação após 3 tentativas erradas. É bloqueio da conta, espera ou recuperação de senha?
10. **Feedback entre colegas:** o colaborador pode dar feedback a outro colaborador (sem ser o líder)?

## 6. Perguntas dos questionários (referência das colunas)

**Formulário 1 — líderes**

| Col. | Pergunta |
|------|----------|
| F | Com que frequência você dá feedback à sua equipe? |
| G | Você registra esses feedbacks em algum lugar? |
| H | É fácil lembrar o que foi combinado em feedbacks anteriores? |
| I | É fácil acompanhar a evolução de cada pessoa da equipe? |
| J | Quanto tempo você gasta por semana com feedbacks? |
| K | Quais funções seriam mais úteis numa ferramenta de feedback? |
| L | Qual é a maior dificuldade hoje para dar feedback? |
| M | O que você gostaria que a ferramenta fizesse? |

**Formulário 2 — colaboradores**

| Col. | Pergunta |
|------|----------|
| F | Com que frequência você recebe feedback? |
| G | O feedback que você recebe é claro e útil? |
| H | Você consegue consultar feedbacks antigos? |
| I | Você sabe quais são suas metas de desenvolvimento? |
| J | Você se sente confortável em dar feedback ao seu líder? |
| K | Quais funções seriam mais úteis numa ferramenta de feedback? |
| L | Qual é a maior dificuldade hoje para receber feedback? |
| M | O que você gostaria que a ferramenta fizesse? |

## 7. Diagramas

| Diagrama | Imagem | Fonte editável |
|----------|--------|----------------|
| Contexto | [diagrama-de-contexto.svg](../diagramas/diagrama-de-contexto.svg) | [diagrama-de-contexto.puml](../diagramas/diagrama-de-contexto.puml) |
| Casos de uso | [diagrama-de-casos-de-uso.svg](../diagramas/diagrama-de-casos-de-uso.svg) | [diagrama-de-casos-de-uso.puml](../diagramas/diagrama-de-casos-de-uso.puml) |

Os arquivos `.puml` são PlantUML: para editar, use a extensão PlantUML do VS Code ou o site [plantuml.com](https://plantuml.com) e exporte de novo em `.svg`.
