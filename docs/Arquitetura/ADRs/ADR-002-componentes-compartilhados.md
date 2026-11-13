# ADR-002: Componentes compartilhados entre os perfis

- **Status:** Aceito
- **Data:** 2026-11-12
- **Quem decidiu:** a confirmar
- **Origem:** [#15](https://github.com/morangotangos-team/feedberry/issues/15) (homes), [PR #14](https://github.com/morangotangos-team/feedberry/pull/14) e [PR #21](https://github.com/morangotangos-team/feedberry/pull/21)
- **Relacionados:** [ADR-001](ADR-001-frontend-sem-framework.md)

## Contexto

O FeedBerry tem duas homes, uma para o **publicador** e outra para o **receptor** do feedback. Boa parte delas é igual: cabeçalho, menu, saudação, cards de resumo, cards de feedback, listas de metas e de lembretes, estado vazio. Outra parte é exclusiva de um perfil, como o bloco "Próximos retornos", com a ação de agendar, que só existe para o publicador.

A #15 pede que cada perfil tenha a sua própria pasta, para que o código de um não se misture com o do outro, e que tudo o que for igual nas duas homes vire componente "em vez de ser copiado".

## Decisão

1. Cada perfil tem a sua pasta: `src/frontend/publicador/` e `src/frontend/receptor/`.
2. O que é igual nos dois perfis vira **componente** em `src/frontend/componentes/<nome>/`, com:
   - `<nome>.js`: função que recebe os dados e devolve uma string HTML;
   - `<nome>.css`: estilos do componente, usando as variáveis de `estilos/tokens.css`.
3. O que muda entre os perfis vai **por parâmetro**, por exemplo `cardFeedback(f, { modo: 'recebido' })`. O componente **nunca** testa o perfil (`if (perfil === 'receptor')`).
4. O que é exclusivo de um perfil fica na pasta dele.
5. `publicador/` e `receptor/` só importam de `componentes/`, `estilos/` e `utils/`, nunca um do outro.
6. Todo texto vindo dos dados passa por `utils/escapar-html.js`.
7. Ações do usuário são marcadas com `data-acao` (e `data-id`); quem usa o componente trata o clique.

As regras completas e a lista de componentes estão em `src/frontend/componentes/README.md`.

## Consequências

- **Positivas:**
  - Uma mudança em um bloco comum (por exemplo, o card de feedback) vale para as duas homes de uma vez.
  - As duas pastas de perfil podem ser feitas em paralelo por pessoas diferentes, sem conflito, como sugere a #15.
  - Componentes que não testam o perfil podem ser reaproveitados por perfis novos ou por outras telas.
- **Negativas:**
  - Quem cria uma tela precisa conhecer os componentes e as regras antes de começar.
  - Ao criar um componente novo, é preciso lembrar de incluir o `.css` dele em `componentes/componentes.css`.
  - Um componente muito genérico pode acabar com parâmetros demais.
- **A observar:** os componentes `layout-home`, `saudacao`, `secao`, `avatar`, `berry` e `toast` não estavam na lista da #15 e foram criados durante a implementação para evitar duplicação. Isso indica que a lista vai continuar crescendo; manter o `componentes/README.md` atualizado faz parte da decisão.

## Alternativas consideradas

Não há registro das alternativas discutidas. A #15 só cita, como o que deve ser evitado, copiar os blocos iguais para as duas pastas de perfil; não há registro de outras opções avaliadas.
