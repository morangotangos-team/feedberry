# Requisitos não funcionais

Requisitos não funcionais do **FeedBerry**, tirados da entrevista, dos questionários e das decisões da equipe registradas no repositório. Os requisitos funcionais estão em [Requisitos funcionais](Requisitos%20funcionais.md), e a ligação com issue, documento e código está na [matriz de rastreabilidade](../rastreabilidade/Matriz%20de%20rastreabilidade.md).

| | |
|---|---|
| **Issue** | [#24](https://github.com/morangotangos-team/feedberry/issues/24) · [#31](https://github.com/morangotangos-team/feedberry/issues/31) |
| **Situação** | Proposta (ainda não validada com o cliente) |
| **Última atualização** | 2026-11-16 |

## 1. Fontes

| Código | Artefato |
|--------|----------|
| **Q1-x** | Formulário 1 (líderes, 4 respostas), pergunta da coluna x |
| **Q2-x** | Formulário 2 (colaboradores, 5 respostas), pergunta da coluna x |
| **FL** | Fluxograma da página de login (CT01 a CT06) |
| **E1-n** | Entrevista com o líder, pergunta n da transcrição (`entrevista/Entrevista com Lider/Entrevista-lider_transcricao.md`) |
| **DE** | Decisão da equipe, sem origem nos artefatos de levantamento |

As perguntas de cada coluna dos formulários estão na seção 6 da [análise dos artefatos](../analise/Analise%20dos%20artefatos.md). A gravação da reunião (E2) ainda não tem transcrição e não foi usada.

## 2. Requisitos não funcionais

| Código | Categoria | Requisito | Fonte |
|--------|-----------|-----------|-------|
| **RNF01** | Usabilidade | Registrar um feedback deve ser simples e rápido, para que o uso não seja abandonado. | E1-11, E1-13 |
| **RNF02** | Segurança | As senhas devem ser guardadas só como hash, nunca em texto puro. | DE ([#9](https://github.com/morangotangos-team/feedberry/issues/9)) |
| **RNF03** | Segurança | A resposta do login não deve revelar se um e-mail está cadastrado. | DE ([#9](https://github.com/morangotangos-team/feedberry/issues/9)) |
| **RNF04** | Privacidade | O autor de um feedback anônimo não deve ser guardado nem exibido. | Q2-L (imparcialidade, privacidade) |
| **RNF05** | Responsividade | As telas devem funcionar em computador e em celular. | DE ([#6](https://github.com/morangotangos-team/feedberry/issues/6), [#15](https://github.com/morangotangos-team/feedberry/issues/15)) |
| **RNF06** | Acessibilidade | As telas devem permitir navegação por teclado e uso com leitor de tela. | DE ([#6](https://github.com/morangotangos-team/feedberry/issues/6)) |
| **RNF07** | Integridade | O histórico de feedbacks não pode ser perdido: usuários são desativados, não apagados. | Q1-K (4/4) · E1-8 |
| **RNF08** | Portabilidade | O banco de dados deve poder ser trocado de SQLite para PostgreSQL só por configuração. | DE ([#13](https://github.com/morangotangos-team/feedberry/issues/13)) |

> ℹ️ O RNF01 ainda não tem critério de medição (por exemplo, número de passos ou tempo para registrar um feedback). Definir com o cliente.

## 3. Pontos que dependem do cliente

| Requisito | Dúvida da [análise dos artefatos](../analise/Analise%20dos%20artefatos.md) (seção 5) |
|-----------|-------------------|
| RNF03 | 9 (o que acontece após 3 tentativas erradas de login) |
| RNF04 | 4 (alcance do anonimato), 5 (quem vê os feedbacks) |

## Histórico

| Data | Autor(a) | Alteração |
|------|----------|-----------|
| 2026-11-16 | Paula Silvério de Castro | Criação dos requisitos não funcionais (issues #24 e #31) |
