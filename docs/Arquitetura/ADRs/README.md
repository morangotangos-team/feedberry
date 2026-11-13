# 🏛️ Registros de decisões de arquitetura (ADRs)

Um ADR (*Architecture Decision Record*) registra **uma** decisão de arquitetura: o problema que existia, o que foi decidido, o que muda por causa disso e quais outras opções existiam. O objetivo é que quem entrar no projeto entenda **por que** o código é como é, sem precisar garimpar issues e PRs antigos.

- Modelo para copiar: [template.md](template.md)
- Formato: Nygard (Contexto, Decisão, Consequências), com a seção **Alternativas consideradas**

## Índice

| ADR | Decisão | Status | Origem |
|-----|---------|--------|--------|
| [ADR-001](ADR-001-frontend-sem-framework.md) | Front-end em HTML, CSS e JavaScript, sem framework | Aceito | [#6](https://github.com/morangotangos-team/feedberry/issues/6), [#15](https://github.com/morangotangos-team/feedberry/issues/15), [PR #14](https://github.com/morangotangos-team/feedberry/pull/14) |
| [ADR-002](ADR-002-componentes-compartilhados.md) | Componentes compartilhados entre os perfis | Aceito | [#15](https://github.com/morangotangos-team/feedberry/issues/15), [PR #14](https://github.com/morangotangos-team/feedberry/pull/14), [PR #21](https://github.com/morangotangos-team/feedberry/pull/21) |
| [ADR-003](ADR-003-backend-flask-em-camadas.md) | Back-end em Flask, organizado em camadas | Proposto | [#9](https://github.com/morangotangos-team/feedberry/issues/9), [PR #12](https://github.com/morangotangos-team/feedberry/pull/12) |
| [ADR-004](ADR-004-hash-scrypt.md) | Hash de senha com scrypt | Proposto | [#9](https://github.com/morangotangos-team/feedberry/issues/9), [PR #12](https://github.com/morangotangos-team/feedberry/pull/12) |
| [ADR-005](ADR-005-frontend-servido-pelo-flask.md) | Front-end servido pelo Flask, na mesma origem da API | Proposto | [#16](https://github.com/morangotangos-team/feedberry/issues/16) |
| [ADR-006](ADR-006-perfil-da-conta.md) | Perfil da conta: publicador/receptor ou colaborador/líder | Em aberto | [#13](https://github.com/morangotangos-team/feedberry/issues/13), [#16](https://github.com/morangotangos-team/feedberry/issues/16) |

> ℹ️ A [#13](https://github.com/morangotangos-team/feedberry/issues/13) pede um ADR da escolha do ORM e do banco em `docs/Arquitetura/ADR-001-orm-e-banco-de-dados.md`. Quando ele for escrito, deve ficar nesta pasta com o próximo número livre (ADR-007), porque o ADR-001 já existe.

## Quando criar um ADR

Crie um ADR quando a decisão se encaixar em pelo menos um destes casos:

| Caso | Exemplos |
|------|----------|
| **Escolha de tecnologia** | Adotar ou trocar linguagem, framework, biblioteca, banco de dados, ORM |
| **Estrutura do código** | Organização em camadas ou pastas, padrão de componentes, como o front-end e o back-end se comunicam |
| **Segurança e dados** | Autenticação, sessão, hash de senha, permissões, modelo de dados |
| **Difícil de reverter** | Decisões caras de desfazer depois ou que afetam o trabalho do grupo todo |

**Não** precisa de ADR:

- Nomes de variáveis, funções ou arquivos;
- Estilo visual e CSS de uma tela;
- Correções de bug que não mudam a arquitetura;
- Detalhes que já estão explicados na documentação da funcionalidade em [`docs/Funcionalidades/`](../../Funcionalidades/README.md).

> 💡 Na dúvida, pergunte: "daqui a seis meses, alguém vai querer saber **por que** fizemos assim?" Se a resposta for sim, escreva o ADR.

## Status

| Status | Significado |
|--------|-------------|
| **Em aberto** | O problema foi identificado, mas a decisão ainda não foi tomada. O ADR lista as opções em discussão |
| **Proposto** | A decisão foi tomada em uma issue ou PR que **ainda não foi mesclado** na `develop` |
| **Aceito** | A decisão está em uso: o código ou o documento que a aplica já está na `develop` |
| **Substituído** | Uma decisão mais nova tomou o lugar desta. O campo **Relacionados** aponta para o ADR que a substitui |

Um ADR **não é apagado** nem reescrito quando a decisão muda: o status passa a **Substituído** e um ADR novo registra a decisão nova. Correções pequenas (link quebrado, erro de digitação) podem ser feitas direto no arquivo.

## Como criar um ADR

1. Copie o [template.md](template.md) para `ADR-<número>-<titulo-curto>.md`, com o número seguinte ao último do índice (três dígitos: `007`, `008`...).
2. Preencha os metadados e as seções. Se as alternativas discutidas não foram registradas em lugar nenhum, **escreva isso** em vez de inventar.
3. Adicione a linha no índice acima.
4. Abra o PR seguindo o [padrão de commit e GitFlow](../../Processos_De_Desenvolvimento/Padrao%20de%20commit%20e%20GitFlow.md), com commit do tipo `docs(arquitetura): ...`.
5. Quando a issue ou o PR de origem for mesclado, mude o status de **Proposto** para **Aceito**.
