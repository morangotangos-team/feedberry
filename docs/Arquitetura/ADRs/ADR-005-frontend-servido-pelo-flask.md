# ADR-005: Front-end servido pelo Flask, na mesma origem da API

- **Status:** Proposto
- **Data:** 2026-11-12
- **Quem decidiu:** Fernando Felipe
- **Origem:** [#16](https://github.com/morangotangos-team/feedberry/issues/16) (integração do login com a API), ponto 7 da análise
- **Relacionados:** [ADR-001](ADR-001-frontend-sem-framework.md), [ADR-003](ADR-003-backend-flask-em-camadas.md)

## Contexto

Hoje o front-end e o back-end rodam separados:

- o front-end é aberto por um servidor de arquivos próprio (`python -m http.server` dentro de `src/frontend/`, em `http://localhost:8000`), porque os módulos ES não funcionam por `file://` ([ADR-001](ADR-001-frontend-sem-framework.md));
- o back-end do PR #12 sobe a API em `http://127.0.0.1:5000`.

São **origens diferentes**. Para o navegador deixar a tela chamar a API, o back-end precisaria liberar a origem do front-end (CORS), como a própria documentação do PR #12 avisa. A #16 compara os dois lados e registra esse ponto antes de integrar o login.

## Decisão

O Flask passa a **servir os arquivos de `src/frontend/`** como arquivos estáticos, na mesma origem da API.

- A tela e a API ficam no mesmo endereço (`http://127.0.0.1:5000/`).
- O front-end chama a API por **URL relativa**, por exemplo `fetch("/auth/login")`.
- Toda chamada HTTP passa por `src/frontend/servicos/api.js`, também definido na #16.

## Consequências

- **Positivas:**
  - Não é preciso configurar CORS nem adicionar a dependência `flask-cors`.
  - Para testar o sistema completo basta um comando (`python app.py` em `src/backend`).
  - As URLs relativas funcionam em qualquer endereço onde o Flask estiver rodando, sem trocar nada no front-end.
- **Negativas:**
  - O front-end passa a depender do back-end para ser aberto de forma integrada. O `python -m http.server` continua servindo para testar só as telas com dados *mock*, mas sem login real.
  - Os arquivos estáticos são entregues pelo servidor de desenvolvimento do Flask, que não é feito para produção. Deploy está fora do escopo do projeto até agora.
- **A observar:** se o front-end um dia for hospedado separado da API, esta decisão deve ser revista em um ADR novo (com CORS ou um proxy).

## Alternativas consideradas

| Alternativa | Por que não foi escolhida |
|-------------|---------------------------|
| Manter front-end e API em origens diferentes e liberar a origem do front-end no back-end (CORS, com `flask-cors`) | Exige configurar CORS e adicionar uma dependência nova, o que servir os arquivos pelo Flask evita (#16, ponto 7). |

Não há registro de outras alternativas discutidas.
