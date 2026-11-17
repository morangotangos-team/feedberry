# 🗄️ Banco de dados

Modelo de dados do **FeedBerry**, derivado do domínio levantado nos requisitos: atores, casos de uso UC01–UC14 e diagrama de contexto ([análise dos artefatos](../../Artefatos_Requisitos/analise/Analise%20dos%20artefatos.md)).

| | |
|---|---|
| **Issue** | [#13](https://github.com/morangotangos-team/feedberry/issues/13) |
| **Decisão de tecnologia** | [ADR-007: ORM e banco de dados](../ADRs/ADR-007-orm-e-banco-de-dados.md) |
| **Código** | `src/backend/models/`, `src/backend/migrations/`, `src/backend/seeds.py` |
| **Última atualização** | 2026-11-16 |

---

## 1. Como rodar

Na raiz do repositório:

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows (Linux/macOS: source .venv/bin/activate)
pip install -r requirements.txt
cd src/backend
flask db upgrade                # cria (ou atualiza) o banco em src/backend/instance/feedberry.db
```

> O Flask encontra o `app.py` sozinho quando o comando é rodado dentro de `src/backend`. Se aparecer *"Could not locate a Flask application"*, use `flask --app app db upgrade`.

### Usuários de teste (seed)

As senhas não ficam no código: são lidas de variáveis de ambiente e gravadas só como hash scrypt.

```powershell
# PowerShell
$env:SEED_SENHA_LIDER = "<escolha uma senha>"
$env:SEED_SENHA_COLABORADOR = "<escolha outra senha>"
python seeds.py
```

```bash
# Bash
SEED_SENHA_LIDER='<senha>' SEED_SENHA_COLABORADOR='<senha>' python seeds.py
```

O seed cria a **Equipe de Teste**, liderada por `lider@exemplo.com` (papel `LIDER`), com `colaborador@exemplo.com` (papel `COLABORADOR`) como membro. Rodar de novo não duplica nada. Sem as duas variáveis, o seed para com erro e não grava nada.

Enquanto o login usar perfil (ver [§ 6](#6-decisões-provisórias-e-pontos-em-aberto)), o líder entra como **publicador** e o colaborador como **receptor**.

### Mudei um modelo. E agora?

```bash
flask db migrate -m "descreve a mudança"   # gera o arquivo em migrations/versions/
# abra e confira o arquivo gerado antes de commitar
flask db upgrade                            # aplica no seu banco
python -m pytest                            # o teste de migração acusa se o modelo e a migração divergirem
```

A migração vai no **mesmo PR** da mudança do modelo. Nunca edite uma migração que já foi mesclada na `develop`: crie outra.

### Começar do zero

Apague `src/backend/instance/feedberry.db` e rode `flask db upgrade` de novo. Para desfazer todas as migrações sem apagar o arquivo: `flask db downgrade base`.

### Trocar para PostgreSQL

O acesso passa pelo ORM, então basta mudar a URL de conexão:

```powershell
pip install "psycopg[binary]"            # driver do PostgreSQL (não está no requirements.txt)
$env:DATABASE_URL = "postgresql://usuario:senha@localhost:5432/feedberry"
flask db upgrade
```

- O SQLAlchemy 2.1 usa o driver `psycopg` (versão 3) para `postgresql://`. Para usar o `psycopg2`, escreva `postgresql+psycopg2://`.
- URLs no formato antigo `postgres://` (comuns em serviços de hospedagem) são convertidas sozinhas para `postgresql://`.
- A migração inicial foi conferida em modo offline para PostgreSQL (`flask db upgrade --sql`): ela cria a FK circular entre `usuario` e `equipe` com `ALTER TABLE`, depois das duas tabelas existirem.
- Nunca commite a `DATABASE_URL` com senha. Use variável de ambiente ou um `.env` (já está no `.gitignore`).

---

## 2. Modelo entidade-relacionamento

Fonte editável: [`modelo-entidade-relacionamento.puml`](modelo-entidade-relacionamento.puml) (renderize com PlantUML ou a extensão PlantUML do VS Code).

![Modelo entidade-relacionamento](modelo-entidade-relacionamento.svg)

---

## 3. Dicionário de dados

Convenções:

- **Obrig.** ✅ = `NOT NULL`.
- Os **enums** são guardados como texto com `CHECK` (iguais no SQLite e no PostgreSQL). Para incluir um valor, mude `src/backend/models/enums.py` e gere uma migração.
- Todas as **datas e horas** são gravadas em **UTC**. A aplicação recusa datas sem fuso horário e sempre devolve as datas com fuso UTC.
- As constraints têm nomes previsíveis: `pk_`, `fk_`, `uq_`, `ck_`, `ix_` + tabela + coluna/regra.

### `usuario`

Conta de quem usa o sistema. O líder também é colaborador (herança no diagrama de casos de uso).

| Coluna | Tipo | Obrig. | Regra |
|--------|------|:------:|-------|
| `id` | INTEGER | ✅ | Chave primária |
| `nome` | VARCHAR(120) | ✅ | |
| `email` | VARCHAR(254) | ✅ | **Único**. Salvo em minúsculas e sem espaços nas pontas (`ck_usuario_email_minusculo`) |
| `senha_hash` | VARCHAR(255) | ✅ | Só o hash scrypt (`auth/security.py`). A senha nunca é guardada |
| `papel` | `COLABORADOR` \| `LIDER` | ✅ | Padrão `COLABORADOR` |
| `equipe_id` | INTEGER | | FK → `equipe.id`. Se a equipe for apagada, fica nulo (`SET NULL`) |
| `ativo` | BOOLEAN | ✅ | Padrão `true`. Usuário **não é apagado**, só desativado. Desativado não consegue entrar |
| `tentativas_login_falhas` | INTEGER | ✅ | Padrão `0`, nunca negativo. Base para o bloqueio após 3 tentativas do fluxograma de login |
| `criado_em` | DATETIME (UTC) | ✅ | Preenchido na criação |

### `equipe`

Define quem é líder de quem.

| Coluna | Tipo | Obrig. | Regra |
|--------|------|:------:|-------|
| `id` | INTEGER | ✅ | Chave primária |
| `nome` | VARCHAR(120) | ✅ | **Único** |
| `lider_id` | INTEGER | | FK → `usuario.id` (`RESTRICT`). **Único**: uma pessoa lidera no máximo uma equipe. Pode ficar vazio enquanto a equipe não tem líder |
| `criado_em` | DATETIME (UTC) | ✅ | Preenchido na criação |

### `feedback`

| Coluna | Tipo | Obrig. | Regra |
|--------|------|:------:|-------|
| `id` | INTEGER | ✅ | Chave primária |
| `tipo` | `LIDER_PARA_COLABORADOR` \| `COLABORADOR_PARA_LIDER` | ✅ | Separa o UC03 do UC12 |
| `autor_id` | INTEGER | | FK → `usuario.id` (`RESTRICT`). **Nulo se e somente se** `anonimo = true` (`ck_feedback_autor_conforme_anonimato`). Diferente de `destinatario_id` (`ck_feedback_autor_diferente_destinatario`) |
| `destinatario_id` | INTEGER | ✅ | FK → `usuario.id` (`RESTRICT`) |
| `conteudo` | TEXT | ✅ | Não pode ser vazio nem só espaços |
| `anonimo` | BOOLEAN | ✅ | Padrão `false`. Só pode ser `true` quando `tipo = COLABORADOR_PARA_LIDER` (`ck_feedback_anonimo_so_para_lider`) |
| `criado_em` | DATETIME (UTC) | ✅ | Preenchido na criação |

Índice `ix_feedback_destinatario_id_criado_em` em `(destinatario_id, criado_em)` para a consulta de histórico (UC09/UC10).

### `ponto_melhoria`

| Coluna | Tipo | Obrig. | Regra |
|--------|------|:------:|-------|
| `id` | INTEGER | ✅ | Chave primária |
| `feedback_id` | INTEGER | ✅ | FK → `feedback.id`. Se o feedback for apagado, o ponto vai junto (`CASCADE`). Indexado |
| `descricao` | TEXT | ✅ | Não pode ser vazia |
| `status` | `ABERTO` \| `EM_ANDAMENTO` \| `CONCLUIDO` | ✅ | Padrão `ABERTO`. Responde se a pessoa "melhorou no ponto apontado" (Q2-L) |
| `atualizado_em` | DATETIME (UTC) | ✅ | Atualizado sozinho a cada alteração |

### `meta_desenvolvimento`

| Coluna | Tipo | Obrig. | Regra |
|--------|------|:------:|-------|
| `id` | INTEGER | ✅ | Chave primária |
| `colaborador_id` | INTEGER | ✅ | FK → `usuario.id` (`RESTRICT`). Dono da meta. Indexado |
| `definida_por_id` | INTEGER | ✅ | FK → `usuario.id` (`RESTRICT`). Quem definiu (o líder, no UC05) |
| `ponto_melhoria_id` | INTEGER | | FK → `ponto_melhoria.id`. Se o ponto for apagado, a meta fica e o campo vira nulo (`SET NULL`) |
| `titulo` | VARCHAR(150) | ✅ | Não pode ser vazio |
| `descricao` | TEXT | | |
| `prazo` | DATE | | |
| `status` | `NAO_INICIADA` \| `EM_ANDAMENTO` \| `CONCLUIDA` \| `CANCELADA` | ✅ | Padrão `NAO_INICIADA` |
| `criada_em` | DATETIME (UTC) | ✅ | Preenchido na criação |
| `atualizada_em` | DATETIME (UTC) | ✅ | Atualizado sozinho a cada alteração |

### `lembrete`

| Coluna | Tipo | Obrig. | Regra |
|--------|------|:------:|-------|
| `id` | INTEGER | ✅ | Chave primária |
| `agendado_por_id` | INTEGER | ✅ | FK → `usuario.id` (`RESTRICT`) |
| `destinatario_id` | INTEGER | ✅ | FK → `usuario.id` (`RESTRICT`). Indexado |
| `feedback_id` | INTEGER | | FK → `feedback.id` (`CASCADE`) |
| `meta_id` | INTEGER | | FK → `meta_desenvolvimento.id` (`CASCADE`) |
| `data_agendada` | DATETIME (UTC) | ✅ | |
| `mensagem` | VARCHAR(500) | | |
| `status` | `PENDENTE` \| `ENVIADO` \| `CANCELADO` | ✅ | Padrão `PENDENTE` |
| `enviado_em` | DATETIME (UTC) | | Obrigatório quando `status = ENVIADO` (`ck_lembrete_enviado_tem_data`) |

Regra `ck_lembrete_tem_vinculo`: `feedback_id` **ou** `meta_id` precisa estar preenchido (pode ser os dois). Índice `ix_lembrete_status_data_agendada` em `(status, data_agendada)` para buscar os lembretes que vencem.

---

## 4. Regras de negócio e onde cada uma é garantida

| Regra | Onde | Teste |
|-------|------|-------|
| E-mail único | `UNIQUE` em `usuario.email` | `test_email_duplicado_e_rejeitado` |
| E-mail em minúsculas | Aplicação (`@validates`) **e** `CHECK` no banco | `test_email_e_salvo_em_minusculas_e_sem_espacos`, `test_email_com_maiusculas_por_sql_direto_e_rejeitado` |
| Só o hash da senha é salvo | `auth/security.py` (scrypt); seed lê a senha do ambiente | `test_banco_guarda_so_o_hash_da_senha`, `test_seed_guarda_so_o_hash_e_nao_loga_a_senha` |
| Ninguém dá feedback a si mesmo | `CHECK` | `test_feedback_para_si_mesmo_e_rejeitado` |
| Anônimo só do colaborador para o líder (UC13 estende UC12) | `CHECK` | `test_feedback_anonimo_do_lider_para_o_colaborador_e_rejeitado` |
| Anônimo não guarda o autor | `CHECK` | `test_feedback_anonimo_com_autor_e_rejeitado`, `test_feedback_anonimo_do_colaborador_para_o_lider_e_aceito_sem_autor` |
| Lembrete aponta para um feedback ou uma meta | `CHECK` | `test_lembrete_sem_feedback_e_sem_meta_e_rejeitado` |
| Usuários não são apagados, só desativados | Aplicação (evento `before_delete`) **e** `ON DELETE RESTRICT` nas FKs para `usuario` | `test_usuario_nao_pode_ser_apagado_so_desativado`, `test_banco_nao_apaga_usuario_que_tem_feedback` |
| Datas em UTC | Tipo `DataHoraUTC` (`models/tipos.py`) | `test_datas_sao_gravadas_e_lidas_em_utc`, `test_data_sem_fuso_horario_e_recusada` |
| Índice do histórico | `ix_feedback_destinatario_id_criado_em` | `test_indice_do_historico_existe` |
| Migração igual aos modelos | Alembic `compare_metadata` | `test_migracao_cria_o_banco_do_zero_igual_aos_modelos` |

Regras que ficam na **camada de serviço** (não no banco), porque dependem de mais de uma tabela ou de contexto:

- Todo feedback do líder tem ao menos um ponto de melhoria (UC03 `<<include>>` UC04).
- O `lider_id` de uma equipe aponta para alguém com `papel = LIDER`.
- No feedback `LIDER_PARA_COLABORADOR`, o autor é líder do destinatário (e vice-versa no `COLABORADOR_PARA_LIDER`).

> ⚠️ O SQLite só confere chaves estrangeiras com `PRAGMA foreign_keys=ON`. A aplicação liga isso em toda conexão (`extensions.py`). Quem abrir o arquivo `.db` em outra ferramenta (ex.: DB Browser for SQLite) precisa ligar o PRAGMA para ter as mesmas garantias.

---

## 5. Rastreabilidade: entidade → caso de uso

| Entidade | Casos de uso | Observação |
|----------|--------------|------------|
| `usuario` | UC01 Fazer login, UC02 Criar conta | O papel `LIDER` também é colaborador. `tentativas_login_falhas` atende o bloqueio após 3 tentativas do fluxograma de login |
| `equipe` | UC07 Acompanhar evolução da equipe, UC08 Gerar relatórios | Define "quem é líder de quem" (dúvida 3 da análise) |
| `feedback` | UC03, UC09, UC10, UC12, UC13 | `tipo` separa UC03 (líder → colaborador) de UC12 (colaborador → líder) |
| `ponto_melhoria` | UC04 (incluído em UC03), UC07, UC11 | O `status` permite saber se a pessoa "melhorou no ponto apontado" (Q2-L) |
| `meta_desenvolvimento` | UC05 Definir metas, UC11 Acompanhar metas | Pode nascer de um ponto de melhoria |
| `lembrete` | UC06 Agendar retorno, UC14 Receber lembretes | O envio real (e-mail) fica fora desta issue |
| _(sem tabela)_ | UC08 Gerar relatórios, UC10 Consultar histórico | São **consultas** sobre as tabelas acima, não entidades novas |

---

## 6. Decisões provisórias e pontos em aberto

Pontos da [#13](https://github.com/morangotangos-team/feedberry/issues/13) que ainda dependem do grupo ou do cliente. O modelo foi feito para que cada um mude pouco código.

| # | Ponto | Como está hoje | Se mudar |
|---|-------|----------------|----------|
| 1 | **Perfil do login × papel da conta** ([ADR-006](../ADRs/ADR-006-perfil-da-conta.md)) | O banco guarda só o `papel`. O `UsuarioRepository` traduz `LIDER` → `publicador` e `COLABORADOR` → `receptor`, e o login continua igual | Muda só o mapa `PERFIL_POR_PAPEL` em `repositories/usuario_repository.py` (ou o login deixa de pedir perfil) |
| 2 | **Líder vê o autor de feedback anônimo?** (dúvida 4) | Não: o autor **não é guardado** | Seria preciso guardar o autor criptografado ou em outra tabela, e revisar o `CHECK` de anonimato |
| 3 | **Feedback entre colegas** (dúvida 10) | Fora do modelo | Novo valor no enum `TipoFeedback` + migração |
| 4 | **Administrador / RH** (dúvida 2) | Fora do modelo | Novo valor no enum `Papel` + migração |
| 5 | **Um colaborador em só uma equipe?** | Sim: `usuario.equipe_id` | Tabela de associação `equipe_membro` no lugar de `equipe_id` |

---

## Histórico

| Data | Autor(a) | Alteração |
|------|----------|-----------|
| 2026-11-16 | Fernando | Criação do banco (issue #13): modelos, migração inicial, seed e documentação |
