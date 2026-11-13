# ADR-001: Front-end em HTML, CSS e JavaScript, sem framework

- **Status:** Aceito
- **Data:** 2026-11-10
- **Quem decidiu:** a confirmar
- **Origem:** [#6](https://github.com/morangotangos-team/feedberry/issues/6) (tela de login), [#15](https://github.com/morangotangos-team/feedberry/issues/15) (homes), [PR #14](https://github.com/morangotangos-team/feedberry/pull/14) e [PR #21](https://github.com/morangotangos-team/feedberry/pull/21)
- **Relacionados:** [ADR-002](ADR-002-componentes-compartilhados.md), [ADR-005](ADR-005-frontend-servido-pelo-flask.md)

## Contexto

As primeiras telas do FeedBerry (login, na #6, e as homes do publicador e do receptor, na #15) foram pedidas como **somente front-end**, sem back-end, API nem banco de dados. A #6 define que a pessoa responsável faria "apenas HTML e CSS, e JavaScript se for necessário". A #15 mantém "HTML, CSS e JavaScript", com os dados vindo de arquivos *mock* em cada pasta de perfil.

Nenhuma das issues cita framework, biblioteca de interface, gerenciador de pacotes ou etapa de build.

## Decisão

O front-end é feito em **HTML, CSS e JavaScript puros**, sem framework (React, Vue, Angular etc.), sem `npm` e sem etapa de build.

- O JavaScript usa **módulos ES** (`<script type="module">`, `import`/`export`).
- As cores, fontes e temas ficam centralizados em `src/frontend/estilos/tokens.css`.
- A interface é montada por funções que recebem dados e devolvem uma string HTML (veja o [ADR-002](ADR-002-componentes-compartilhados.md)).

A decisão está em uso em `src/frontend/` desde o PR #14, com a estrutura corrigida pelo PR #21.

## Consequências

- **Positivas:**
  - Não há dependências de front-end para instalar nem para manter atualizadas.
  - Qualquer pessoa do grupo consegue ler e alterar o código sabendo só HTML, CSS e JavaScript.
  - O código que chega ao navegador é o mesmo que está no repositório, sem build.
- **Negativas:**
  - Módulos ES não funcionam abrindo o HTML direto do disco (`file://`). Para testar é preciso um servidor, por exemplo `python -m http.server` dentro de `src/frontend/` (documentado no `src/frontend/README.md`).
  - Sem framework, a proteção contra injeção de HTML não é automática: todo texto vindo dos dados precisa passar por `utils/escapar-html.js`. Esquecer essa chamada abre brecha de XSS.
  - Atualizar a tela é manual (`innerHTML` e funções como `atualizarConteudo`). Telas com muito estado ou muita interação dão mais trabalho do que dariam com um framework.
- **A observar:** se as próximas telas (enviar feedback, histórico, metas) ficarem muito interativas, vale reabrir esta decisão em um ADR novo.

## Alternativas consideradas

Não há registro das alternativas discutidas. As issues #6 e #15 já definem HTML, CSS e JavaScript como escopo, sem citar frameworks avaliados nem o motivo de não usá-los.
