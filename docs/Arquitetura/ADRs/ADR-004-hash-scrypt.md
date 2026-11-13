# ADR-004: Hash de senha com scrypt

- **Status:** Proposto
- **Data:** 2026-11-11
- **Quem decidiu:** a confirmar
- **Origem:** [#9](https://github.com/morangotangos-team/feedberry/issues/9) (back-end de login), [PR #12](https://github.com/morangotangos-team/feedberry/pull/12) (em rascunho)
- **Relacionados:** [ADR-003](ADR-003-backend-flask-em-camadas.md)

## Contexto

A #9 tem como foco "pesquisar e implementar uma forma segura de armazenar e verificar senhas" e deixa a técnica a critério de quem pegasse a issue, com a justificativa documentada. Os critérios de aceite exigem que nenhuma senha fique em texto puro (no código, no arquivo de dados ou em logs) e que e-mail inexistente e senha errada devolvam a mesma mensagem genérica.

Os usuários ficam em `src/backend/data/usuarios.json`, um arquivo que está no repositório. Por isso a proteção precisa valer mesmo se esse arquivo for lido por outra pessoa.

## Decisão

As senhas são guardadas apenas como hash **scrypt**, gerado por `generate_password_hash(senha, method="scrypt")` do **Werkzeug**, que já vem com o Flask. O código fica em `src/backend/auth/security.py`.

- Cada senha recebe um **salt aleatório**. O hash guardado leva o método e os parâmetros (`scrypt:32768:8:1$<salt>$<hash>`).
- A verificação usa `check_password_hash`, que compara em **tempo constante**.
- Quando o e-mail não existe, a senha é verificada contra um **hash fictício**, para que o tempo de resposta não revele quais e-mails estão cadastrados.

A justificativa completa está em `docs/Funcionalidades/login.md`, no PR #12.

## Consequências

- **Positivas:**
  - Nenhuma dependência nova: o Werkzeug já é instalado com o Flask.
  - Se o arquivo de usuários (ou, depois, o banco) vazar, quem tiver os dados não consegue reverter o hash, não consegue usar tabelas pré-calculadas e precisa testar senha por senha, gastando CPU e cerca de 32 MiB de memória em cada tentativa.
  - Como o hash guarda os parâmetros, eles podem ser aumentados no futuro sem invalidar os hashes antigos.
  - A #13 reaproveita o `auth/security.py` no banco de dados, sem mudar a técnica.
- **Negativas:**
  - Cada verificação é propositalmente lenta e usa memória, o que aumenta o custo de cada login no servidor.
  - Senhas fracas ou muito comuns continuam fáceis de adivinhar. Exigir senha forte fica para o cadastro, que está fora do escopo da #9.
- **A observar:** o PR #12 ainda está em rascunho. Se a técnica mudar na revisão, este ADR deve ser atualizado antes de passar para **Aceito**.

## Alternativas consideradas

Alternativas registradas no `docs/Funcionalidades/login.md` do PR #12:

| Alternativa | Por que não foi escolhida |
|-------------|---------------------------|
| Senha em texto puro | Qualquer vazamento expõe todas as senhas. Proibido pelos critérios de aceite. |
| Criptografia reversível (ex.: AES) | Quem tiver a chave recupera todas as senhas. Para login, basta conferir a senha, não recuperá-la. |
| Hash rápido (MD5, SHA-1, SHA-256), mesmo com salt | São feitos para serem rápidos: uma GPU testa bilhões de senhas por segundo. Sem salt, ainda há as tabelas pré-calculadas (*rainbow tables*). |
| Argon2id (`argon2-cffi`) | É a primeira recomendação da OWASP, mas exige dependência nova. O scrypt dá proteção equivalente com o que o projeto já tem. |
| bcrypt (`bcrypt`) | Também é seguro, mas exige dependência nova e considera só os primeiros 72 bytes da senha. |
| PBKDF2 (também disponível no Werkzeug) | É seguro com muitas iterações, mas usa pouca memória, o que facilita ataques com GPU em comparação com o scrypt. |
