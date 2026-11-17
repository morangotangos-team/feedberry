# ADR-007: ORM e banco de dados: SQLAlchemy, Flask-Migrate e SQLite

- **Status:** Proposto
- **Data:** 2026-11-12
- **Quem decidiu:** Fernando (gerente de projetos), na issue de origem
- **Origem:** [#13](https://github.com/morangotangos-team/feedberry/issues/13) (banco de dados), seção "Tecnologia escolhida"
- **Relacionados:** [ADR-003](ADR-003-backend-flask-em-camadas.md) (depende), [ADR-004](ADR-004-hash-scrypt.md), [ADR-006](ADR-006-perfil-da-conta.md)

## Contexto

Até a #13, os usuários do login ficavam em `src/backend/data/usuarios.json` ([#9](https://github.com/morangotangos-team/feedberry/issues/9), [PR #12](https://github.com/morangotangos-team/feedberry/pull/12)). As próximas funcionalidades (feedbacks, pontos de melhoria, metas, lembretes, histórico) precisam de um armazenamento relacional, com relacionamentos e regras de integridade.

Restrições:

- O back-end é **Flask** ([ADR-003](ADR-003-backend-flask-em-camadas.md)), organizado em camadas; trocar o armazenamento deve mexer só no repositório.
- O grupo tem seis pessoas, cada uma na sua máquina, e precisa chegar ao **mesmo esquema** sem combinar scripts SQL à mão.
- Não há servidor de banco disponível para o grupo nem deploy em produção nesta fase.
- O histórico de feedbacks é a função mais pedida (4/4 líderes) e não pode sumir.

## Decisão

| Item | Escolha |
|------|---------|
| ORM | **SQLAlchemy 2.x** via **Flask-SQLAlchemy**, com mapeamento declarativo tipado (`Mapped[...]`) |
| Migrações | **Flask-Migrate** (Alembic), com os arquivos versionados em `src/backend/migrations/` |
| Banco | **SQLite** em desenvolvimento e nos testes (`instance/feedberry.db`; SQLite em memória nos testes), trocável por **PostgreSQL** pela variável `DATABASE_URL` |

Como a decisão foi aplicada:

- As regras de negócio que só dependem de uma linha ficam no banco, em `CHECK`, `UNIQUE` e `ON DELETE RESTRICT`, para valerem mesmo para quem acessa o banco sem passar pela aplicação. As regras que cruzam tabelas ficam na camada de serviço.
- Enums são guardados como texto com `CHECK` (`native_enum=False`), iguais no SQLite e no PostgreSQL.
- Datas e horas são gravadas sempre em UTC, por um tipo próprio (`DataHoraUTC`).
- As constraints seguem uma convenção de nomes (`pk_`, `fk_`, `uq_`, `ck_`, `ix_`), para as migrações conseguirem alterá-las depois.
- O `UsuarioRepository` passou a usar o ORM, mantendo o método `buscar_por_email` e o mesmo formato de retorno, então as rotas e o `AuthService` não mudaram.
- **Decisão provisória ligada ao [ADR-006](ADR-006-perfil-da-conta.md):** a conta guarda `papel = COLABORADOR | LIDER`, e o repositório traduz para o perfil que o login usa hoje (`LIDER` → `publicador`, `COLABORADOR` → `receptor`). Se o grupo decidir outra coisa, muda só esse mapa.

O modelo, o dicionário de dados e o passo a passo estão em [`docs/Arquitetura/banco-de-dados/`](../banco-de-dados/README.md).

## Consequências

- **Positivas:**
  - Cada mudança no modelo vira uma migração revisável no PR, e todos chegam ao mesmo banco com `flask db upgrade`.
  - Não é preciso instalar servidor de banco: o SQLite é um arquivo local, e os testes rodam em memória, sem tocar no banco de quem desenvolve.
  - Trocar para PostgreSQL é mudar a `DATABASE_URL` e instalar o driver; a migração inicial já foi conferida para PostgreSQL em modo offline.
  - As regras críticas (anonimato, feedback para si mesmo, histórico que não some) são garantidas pelo banco, não só pelo código.
  - Um teste compara a migração com os modelos e falha se alguém mudar um modelo sem gerar a migração.
- **Negativas:**
  - Mais dependências (Flask-SQLAlchemy, Flask-Migrate, SQLAlchemy, Alembic) e mais conceitos para o grupo aprender (sessão, migração, relacionamentos).
  - O SQLite tem diferenças do PostgreSQL: não confere chaves estrangeiras sem `PRAGMA foreign_keys=ON` (a aplicação liga em toda conexão), não guarda fuso horário (o tipo `DataHoraUTC` compensa) e não altera colunas com `ALTER TABLE` (as migrações usam o modo *batch*, que recria a tabela).
  - As tabelas `usuario` e `equipe` apontam uma para a outra (membro e líder), o que exige cuidado na migração e `post_update` nos relacionamentos.
- **A observar:**
  - Testar contra um PostgreSQL de verdade antes de qualquer deploy; até agora só o SQL gerado foi conferido.
  - O SQLite não aguenta muitas escritas simultâneas; se o FeedBerry for usado por várias pessoas ao mesmo tempo, migrar para PostgreSQL.
  - Quando o [PR #12](https://github.com/morangotangos-team/feedberry/pull/12) e o PR da #13 forem mesclados, mudar este ADR para **Aceito**.

## Alternativas consideradas

Registradas na [#13](https://github.com/morangotangos-team/feedberry/issues/13):

| Alternativa | Por que não foi escolhida |
|-------------|---------------------------|
| Django ORM | Só funciona dentro do Django, e o projeto é Flask |
| SQLModel | Pensado para FastAPI/Pydantic; no Flask não traz vantagem sobre o SQLAlchemy puro |
| Peewee / Pony ORM | Mais simples, mas com menos material, menos integrações com Flask e migrações menos maduras |

A #13 também justifica o banco escolhido, sem listar as opções como alternativas formais:

| Opção implícita na #13 | Por que não foi escolhida |
|------------------------|---------------------------|
| Continuar com o `usuarios.json` | A issue o trata como armazenamento temporário: não tem relacionamentos nem integridade para feedbacks, metas e lembretes |
| PostgreSQL desde já | Exigiria um servidor instalado em cada máquina; fica como destino, trocando só a `DATABASE_URL` |
