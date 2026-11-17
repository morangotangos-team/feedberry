# Login

| | |
|---|---|
| **Status** | Em revisão |
| **Perfis** | Publicador / Receptor |
| **Issue** | #9 (back-end) · #6 (tela, front-end) · #13 (banco de dados) |
| **Última atualização** | 2026-11-16 |

---

## 👤 Para o usuário

### O que é

O login permite que a pessoa entre no FeedBerry com o seu e-mail e a sua senha, no perfil em que ela está cadastrada.

### Quem usa

- Publicador do feedback: entra para escrever e enviar feedbacks.
- Receptor do feedback: entra para ver os feedbacks que recebeu.

### Como usar

1. Na tela de login, escolha o seu perfil: **publicador** ou **receptor**.
2. Digite o seu e-mail e a sua senha.
3. Clique em **Entrar**.

### Telas

Esta parte (issue #9) cobre só o back-end. As telas são da issue #6 e entram aqui quando forem integradas.

### Dúvidas comuns

| Situação | O que fazer |
|----------|-------------|
| "Preencha e-mail e senha." | Algum campo ficou em branco. Preencha os dois. |
| "E-mail inválido." | O e-mail está sem `@` ou sem domínio (ex.: `maria.com`). Confira o que foi digitado. |
| "E-mail ou senha inválidos." | O e-mail, a senha ou o perfil escolhido não conferem. Confira os dados e se você está na aba do seu perfil. |

---

## ⚙️ Funcionamento

### Objetivo

Conferir o e-mail, a senha e o perfil de quem quer entrar, sem nunca guardar a senha em texto puro. Os usuários ficam na tabela `usuario` do banco de dados (issue #13; ver [Banco de dados](../Arquitetura/banco-de-dados/README.md)).

### Como rodar e testar

Na raiz do repositório:

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows (no Linux/macOS: source .venv/bin/activate)
pip install -r requirements.txt
cd src/backend
flask db upgrade              # cria o banco em src/backend/instance/feedberry.db
python seeds.py               # cria os usuários de teste (ver abaixo)
python app.py                 # sobe a API em http://127.0.0.1:5000
python -m pytest              # roda os testes
```

Para ligar o modo debug na sua máquina, defina `FLASK_DEBUG=1` antes de `python app.py` (PowerShell: `$env:FLASK_DEBUG=1`). Ele não fica ligado no código porque o depurador permite executar código Python pelo navegador.

**Requisição**: `POST /auth/login` com corpo JSON:

```json
{ "email": "publicador@exemplo.com", "senha": "<senha>", "perfil": "publicador" }
```

**Respostas**:

| Situação | Status | Corpo |
|----------|--------|-------|
| Login válido | `200` | `{"sucesso": true, "usuario": {"nome": "...", "email": "...", "perfil": "publicador"}}` |
| E-mail, senha ou perfil não conferem | `401` | `{"sucesso": false, "mensagem": "E-mail ou senha inválidos."}` |
| Campo vazio | `400` | `{"sucesso": false, "mensagem": "Preencha e-mail e senha."}` |
| E-mail em formato inválido | `400` | `{"sucesso": false, "mensagem": "E-mail inválido."}` |
| Perfil ausente ou diferente de `publicador`/`receptor` | `400` | `{"sucesso": false, "mensagem": "Perfil inválido. Use 'publicador' ou 'receptor'."}` |
| Corpo que não é JSON | `400` | `{"sucesso": false, "mensagem": "Envie e-mail, senha e perfil em JSON."}` |
| Requisição maior que 16 KB | `413` | Resposta padrão do Flask |

**Usuários de teste**: o `seeds.py` cria `lider@exemplo.com` (entra como **publicador**) e `colaborador@exemplo.com` (entra como **receptor**). Cada pessoa escolhe as senhas da sua máquina pelas variáveis de ambiente, que nunca vão para o repositório:

```powershell
$env:SEED_SENHA_LIDER = "<senha>"; $env:SEED_SENHA_COLABORADOR = "<senha>"; python seeds.py
```

Detalhes (Bash, PostgreSQL, começar do zero) em [Banco de dados § Como rodar](../Arquitetura/banco-de-dados/README.md#1-como-rodar).

### Regras de negócio

| # | Regra |
|---|-------|
| RN01 | O login usa e-mail e senha. O e-mail não diferencia maiúsculas de minúsculas e os espaços nas pontas são ignorados. |
| RN02 | Cada usuário tem **um único perfil**: publicador ou receptor. O perfil vem do papel da conta: `LIDER` entra como publicador e `COLABORADOR` como receptor (decisão provisória, ver ADR-007 e ADR-006). |
| RN03 | O front-end informa o perfil escolhido. O login só é aceito se esse perfil for o mesmo do cadastro. |
| RN04 | E-mail inexistente, senha errada e perfil diferente do cadastrado retornam **a mesma mensagem genérica** ("E-mail ou senha inválidos."), para não revelar quais e-mails estão cadastrados. |
| RN05 | Campos vazios e e-mail sem formato válido são recusados antes de consultar os usuários. |
| RN06 | Nenhuma senha é guardada em texto puro (nem no código, nem no banco, nem no seed, nem nas migrações, nem em logs). Só o hash é guardado. |
| RN07 | A resposta de sucesso devolve nome, e-mail e perfil, nunca o hash da senha. |
| RN08 | Usuário desativado (`ativo = false`) não consegue entrar e recebe a mesma mensagem genérica da RN04. Usuários não são apagados, só desativados. |

### Segurança das senhas

**Qual técnica foi escolhida e por quê?**

**scrypt**, pela função `generate_password_hash` do **Werkzeug**, que já vem instalado com o Flask. Os motivos:

- É um algoritmo feito para senhas e recomendado pela OWASP. Ele é propositalmente **lento** e usa bastante **memória** (cerca de 32 MiB por verificação com os parâmetros atuais), o que encarece muito um ataque de força bruta com GPU ou hardware dedicado.
- Gera um **salt aleatório para cada senha**. Duas pessoas com a mesma senha ficam com hashes diferentes.
- O hash guardado já leva o método e os parâmetros (`scrypt:32768:8:1$<salt>$<hash>`). Se um dia os parâmetros mudarem, os hashes antigos continuam sendo verificados.
- A comparação é feita em **tempo constante** (`check_password_hash`).
- **Não adiciona dependência nova** ao projeto e usa só o que o Flask já traz.

Além disso, quando o e-mail não existe, o sistema verifica a senha contra um hash fictício. Assim a resposta leva o mesmo tempo nos dois casos, e o tempo não revela se o e-mail está cadastrado.

**Que alternativas foram consideradas e por que foram descartadas?**

| Alternativa | Por que foi descartada |
|-------------|------------------------|
| Senha em texto puro | Qualquer vazamento expõe todas as senhas. Proibido pelos critérios de aceite. |
| Criptografia reversível (ex.: AES) | Quem tiver a chave consegue recuperar todas as senhas. Para login não é preciso recuperar a senha, só conferir. |
| Hash rápido (MD5, SHA-1, SHA-256), mesmo com salt | São feitos para ser rápidos: uma GPU testa bilhões de senhas por segundo. Sem salt, ainda há as tabelas pré-calculadas (*rainbow tables*). |
| Argon2id (`argon2-cffi`) | É a primeira recomendação da OWASP e seria uma ótima escolha, mas exige uma dependência nova. O scrypt dá uma proteção equivalente com o que o projeto já tem. |
| bcrypt (`bcrypt`) | Também é seguro, mas exige dependência nova e considera só os primeiros 72 bytes da senha. |
| PBKDF2 (também disponível no Werkzeug) | É seguro com muitas iterações, mas usa pouca memória, o que facilita ataques com GPU em comparação com o scrypt. |

**Como a escolha protege as senhas se o banco de dados vazar?**

A coluna `usuario.senha_hash` guarda só o hash scrypt e o salt de cada usuário, nunca a senha. Quem obtiver uma cópia do banco:

1. **não consegue reverter o hash**: scrypt é uma função de mão única;
2. **não consegue usar tabelas pré-calculadas**: cada senha tem um salt único;
3. **precisa testar senha por senha**, pagando o custo de CPU e de cerca de 32 MiB de memória em cada tentativa, o que torna o ataque lento e caro;
4. **não descobre quem usa a mesma senha**, porque hashes da mesma senha são diferentes.

A proteção é menor contra senhas fracas ou muito comuns, que podem ser adivinhadas mesmo assim. Por isso, no cadastro (fora do escopo desta issue) vale exigir senhas fortes.

### Arquivos envolvidos

| Arquivo | Responsabilidade |
|---------|------------------|
| `src/backend/app.py` | Cria a aplicação Flask e registra as rotas |
| `src/backend/config.py` | Configurações (conexão com o banco pela `DATABASE_URL`) |
| `src/backend/auth/routes.py` | Rota `POST /auth/login`: recebe o JSON e devolve a resposta HTTP |
| `src/backend/auth/service.py` | Regras do login: validação dos campos, conferência de senha e perfil |
| `src/backend/auth/security.py` | Geração e verificação do hash das senhas (scrypt) |
| `src/backend/repositories/usuario_repository.py` | Busca o usuário ativo no banco e traduz o papel da conta para o perfil do login |
| `src/backend/models/usuario.py` | Tabela `usuario` (ORM) |
| `src/backend/seeds.py` | Usuários de teste, com as senhas vindas de variáveis de ambiente |
| `src/backend/tests/test_auth.py` | Testes de login válido, inválido e do armazenamento seguro, com um banco SQLite em memória |

### Limitações conhecidas

- O perfil do login (publicador/receptor) é derivado do papel da conta (líder/colaborador) por uma decisão provisória, até o grupo fechar o ADR-006.
- Não há cadastro de usuários nem recuperação de senha.
- Não há sessão nem token: o login só responde se as credenciais conferem e qual é o perfil.
- O bloqueio após 3 tentativas erradas (CT06 do fluxograma de login) ainda não foi implementado. A coluna `usuario.tentativas_login_falhas` já existe para isso.
- As mensagens separadas "Usuário não encontrado" (CT04) e "Senha incorreta" (CT05) do fluxograma foram trocadas por uma única mensagem genérica (RN04). Por isso, a opção "Criar conta" também não é oferecida a partir do erro.
- O scrypt usa os parâmetros padrão do Werkzeug (N = 2¹⁵). A OWASP sugere N = 2¹⁷ para produção. Dá para aumentar mudando o `METODO_HASH` em `auth/security.py` (ex.: `scrypt:131072:8:1`).
- A tela de login (issue #6) ainda não está ligada a esta API.

### Rastreabilidade

| Issue | Requisito | Caso de uso |
|-------|-----------|-------------|
| #9 | A definir | UC01 Fazer login |
| #6 | A definir | UC01 Fazer login |
| #13 | A definir | UC01 Fazer login, UC02 Criar conta (tabela `usuario`) |

### Histórico

| Data | Autor(a) | Alteração |
|------|----------|-----------|
| 2026-11-11 | Enzo | Criação da documentação do back-end de login |
| 2026-11-16 | Fernando | Usuários passam a vir do banco de dados (#13): seed, perfil derivado do papel (RN02), usuário desativado não entra (RN08) |
