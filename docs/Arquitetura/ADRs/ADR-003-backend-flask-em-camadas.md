# ADR-003: Back-end em Flask, organizado em camadas

- **Status:** Proposto
- **Data:** 2026-11-10
- **Quem decidiu:** a confirmar
- **Origem:** [#9](https://github.com/morangotangos-team/feedberry/issues/9) (back-end de login), [PR #12](https://github.com/morangotangos-team/feedberry/pull/12) (em rascunho)
- **Relacionados:** [ADR-004](ADR-004-hash-scrypt.md), [ADR-005](ADR-005-frontend-servido-pelo-flask.md), [ADR-006](ADR-006-perfil-da-conta.md)

## Contexto

O FeedBerry precisava de um back-end para o login. Ainda não havia banco de dados, então a #9 pede que os usuários fiquem guardados de forma temporária (em memória ou em arquivo JSON). A [#13](https://github.com/morangotangos-team/feedberry/issues/13) já prevê trocar esse armazenamento por um banco relacional depois.

O grupo precisava de uma organização em que essa troca não obrigasse a reescrever as rotas nem as regras de login.

## Decisão

O back-end é feito em **Python com Flask** e organizado em camadas, conforme a estrutura definida na #9 e implementada no PR #12:

```
src/backend/
├── app.py                         # cria a aplicação (create_app) e registra os blueprints
├── config.py                      # configurações
├── auth/
│   ├── routes.py                  # HTTP: recebe o JSON e devolve a resposta
│   ├── service.py                 # regras de negócio do login
│   └── security.py                # hash e verificação de senha
├── repositories/
│   └── usuario_repository.py      # acesso aos dados dos usuários
├── data/
│   └── usuarios.json              # armazenamento temporário
└── tests/
```

| Camada | Responsabilidade | Não deve |
|--------|------------------|----------|
| Rotas (`routes.py`) | Ler a requisição e montar a resposta HTTP | Ter regra de negócio ou ler arquivos de dados |
| Serviço (`service.py`) | Validar os dados e aplicar as regras de negócio | Conhecer detalhes de HTTP ou de onde os dados ficam guardados |
| Repositório (`repositories/`) | Buscar e gravar os dados | Ter regra de negócio |

A funcionalidade fica em um *blueprint* do Flask (`auth`), e a aplicação é criada pela função `create_app`, que aceita configurações extras para os testes.

## Consequências

- **Positivas:**
  - Trocar o `usuarios.json` pelo banco mexe só no repositório. A #13 já conta com isso: pede para reescrever o `UsuarioRepository` com o ORM mantendo o método `buscar_por_email`, para que as rotas e o `AuthService` não mudem.
  - As regras de negócio podem ser testadas sem subir o servidor HTTP.
  - Novas funcionalidades (feedbacks, metas, lembretes) podem seguir o mesmo padrão, cada uma no seu blueprint.
- **Negativas:**
  - Mais arquivos e mais indireção do que um único `app.py`, o que pesa em funcionalidades pequenas.
  - A separação só funciona se todo o grupo respeitar as responsabilidades da tabela acima; nada no código impede uma rota de acessar os dados direto.
- **A observar:** o PR #12 ainda está em rascunho. Se a estrutura mudar na revisão, este ADR deve ser atualizado antes de passar para **Aceito**.

## Alternativas consideradas

Não há registro das alternativas discutidas. A #9 já define Flask e a estrutura de pastas, sem citar outros frameworks ou outras organizações avaliadas.
