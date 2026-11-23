# ADR-008: Cada camada do back-end em uma pasta própria

- **Status:** Proposto
- **Data:** 2026-11-18
- **Quem decidiu:** Fernando (gerente de projetos), no PR de origem
- **Origem:** [#13](https://github.com/morangotangos-team/feedberry/issues/13) (banco de dados), [PR #30](https://github.com/morangotangos-team/feedberry/pull/30)
- **Relacionados:** [ADR-003](ADR-003-backend-flask-em-camadas.md) (mantém as camadas e muda só a organização das pastas), [ADR-007](ADR-007-orm-e-banco-de-dados.md)

## Contexto

O [ADR-003](ADR-003-backend-flask-em-camadas.md) organiza o back-end em camadas (rotas, serviço e repositório). No PR #12, as rotas e o serviço do login ficavam juntos na pasta `auth/`, e só o repositório tinha uma pasta própria (`repositories/`).

Com o banco de dados ([ADR-007](ADR-007-orm-e-banco-de-dados.md)), o PR #30 criou também a pasta `models/`. A parte de dados passou a ter uma pasta por camada (`models/` e `repositories/`), mas a parte de cima não: `auth/` continuava misturando o controller HTTP com as regras de negócio.

As próximas funcionalidades (feedbacks, metas, lembretes) vão criar mais controllers e serviços. Se cada uma ganhar uma pasta como `auth/`, o mesmo tipo de código fica espalhado em várias pastas e a separação das camadas fica mais difícil de ver.

## Decisão

Cada camada do back-end fica em uma pasta própria, no mesmo nível:

```
src/backend/
├── app.py                         # cria a aplicação (create_app) e registra os blueprints
├── config.py                      # configurações
├── extensions.py                  # instâncias do SQLAlchemy e do Flask-Migrate
├── controllers/
│   └── auth_controller.py         # HTTP: blueprint, lê o JSON e monta a resposta
├── services/
│   ├── auth_service.py            # regras de negócio do login
│   └── security.py                # hash e verificação de senha
├── repositories/
│   └── usuario_repository.py      # consultas e gravações no banco
├── models/                        # tabelas (ORM)
├── migrations/                    # migrações do banco (Flask-Migrate)
└── tests/
```

| Camada | Pasta | Responsabilidade | Não deve |
|--------|-------|------------------|----------|
| Controller | `controllers/` | Definir o blueprint e as rotas, ler a requisição e montar a resposta HTTP | Ter regra de negócio ou acessar o banco |
| Serviço | `services/` | Validar os dados e aplicar as regras de negócio | Conhecer detalhes de HTTP ou do banco (usa o repositório) |
| Repositório | `repositories/` | Buscar e gravar os dados pelo ORM | Ter regra de negócio |
| Modelo | `models/` | Descrever as tabelas e as regras que valem no próprio banco (ADR-007) | Conhecer HTTP ou as regras que cruzam tabelas |

As dependências vão sempre para baixo: controller → serviço → repositório → modelo.

Cada funcionalidade nova cria um arquivo em cada camada, com o nome dela: `feedback_controller.py`, `feedback_service.py`, `feedback_repository.py`. O blueprint é exportado em `controllers/__init__.py` e registrado no `create_app`.

As URLs não mudam: o login continua em `POST /auth/login`.

## Consequências

- **Positivas:**
  - Cada pasta tem um tipo de código só, e fica fácil ver em que camada um arquivo está.
  - As novas funcionalidades têm um lugar certo para cada parte, sem precisar decidir a estrutura de novo.
  - Código usado por mais de uma funcionalidade (como o `security.py`) fica em `services/`, sem depender da pasta de uma funcionalidade específica.
- **Negativas:**
  - Os arquivos de uma mesma funcionalidade ficam em pastas diferentes. Para entender o login inteiro, é preciso abrir `controllers/`, `services/` e `repositories/`.
  - Os imports mudaram (`auth.security` → `services.security`, `auth.service` → `services.auth_service`). Código fora de `src/backend/` que use os caminhos antigos precisa ser atualizado.
  - Como no ADR-003, nada no código impede um controller de acessar o banco direto; a separação depende do grupo e da revisão dos PRs.
- **A observar:** se algum serviço crescer muito, a pasta `services/` pode ganhar subpastas por funcionalidade. Isso deve ser registrado em um ADR novo.

## Alternativas consideradas

| Alternativa | Por que não foi escolhida |
|-------------|---------------------------|
| Manter uma pasta por funcionalidade (`auth/` com `routes.py`, `service.py` e `security.py`), como no PR #12 | A parte de dados já tinha uma pasta por camada; manter as duas formas deixa a estrutura inconsistente |
| Separar a rota do controller (`routes/` só com as URLs e `controllers/` com o tratamento da requisição) | Com o blueprint do Flask, a rota e o tratamento ficam no mesmo lugar; uma camada a mais só repassaria a chamada |
| Mover só o controller para `controllers/` e deixar o serviço em `auth/` | `auth/` ficaria só com o serviço, e as regras de negócio continuariam sem uma pasta própria |
