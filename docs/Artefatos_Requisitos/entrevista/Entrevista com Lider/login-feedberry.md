# Login do FeedBerry

**FeedBerry · Issue #9 · Back-end**

Como o back-end confere e-mail, senha e perfil, como as senhas ficam protegidas e o que falta para a issue #9 ser entregue.

- Back-end: **Enzo**
- Testes e documentação: **Matheus**
- PR: [#12 (rascunho)](https://github.com/morangotangos-team/feedberry/pull/12)
- Data: 11/11/2026

## Resumo

- A tela de login manda **e-mail, senha e perfil** (publicador ou receptor) e o back-end responde se a pessoa pode entrar.
- As senhas **nunca** ficam guardadas como são: só um código embaralhado e sem volta (hash **scrypt**).
- O código está pronto e testado. Falta o Matheus validar os **testes** e a **documentação** antes da revisão.

## 1. A ideia geral

O back-end é a parte do sistema que não aparece na tela e decide quem pode entrar. A tela de login (issue #6) só coleta os dados e mostra a resposta.

| Etapa | O que acontece |
| --- | --- |
| **Tela de login** | Issue #6. Coleta e-mail, senha e perfil. |
| ↓ **Back-end** | Issue #9. Confere tudo em `POST /auth/login`. |
| ↓ **Resposta** | "Pode entrar" com o perfil, ou uma mensagem de erro. |

## 2. As partes do código

Cada arquivo tem uma função só. Pense na recepção de uma empresa:

| Arquivo | Na recepção seria | O que faz |
| --- | --- | --- |
| `auth/routes.py` | O balcão | Recebe o pedido da tela e devolve a resposta. |
| `auth/service.py` | O recepcionista | Confere as regras: campos preenchidos, e-mail válido, senha certa, perfil igual ao do cadastro. |
| `auth/security.py` | O cofre | Transforma a senha em hash e compara senhas. |
| `repositories/usuario_repository.py` | O arquivo de fichas | Busca o usuário pelo e-mail. |
| `data/usuarios.json` | As fichas | Usuários de teste, enquanto não há banco de dados. |
| `app.py` e `config.py` | A abertura da empresa | Ligam o sistema e guardam as configurações. |

**Por que separar o "arquivo de fichas"?** Quando o banco de dados chegar, troca-se só `usuario_repository.py`. O balcão e o recepcionista continuam iguais. Esse era o ponto de arquitetura pedido na issue.

## 3. Como a senha fica protegida

No lugar da senha guardamos um **hash**: um código embaralhado que não tem volta. É isto que fica no `usuarios.json`:

```text
# senha digitada
"minhaSenha123"
#      │ scrypt
#      ▼  hash guardado = método : parâmetros $ salt $ hash
"scrypt:32768:8:1$9WebvM90r1hK5gbd$805d1b8f61f1…"
```

- **Não tem volta.** Pelo código não dá para descobrir a senha.
- **Tempero aleatório (salt).** Cada senha ganha um salt próprio. Duas pessoas com a mesma senha ficam com códigos diferentes.
- **Lento de propósito.** Cada tentativa gasta tempo e cerca de 32 MiB de memória. Testar milhões de senhas fica caro demais.
- **Como confere.** Embaralha a senha digitada do mesmo jeito e compara com o código guardado.

Usamos o **scrypt do Werkzeug**, que já vem com o Flask. Assim o projeto não ganha dependência nova. A comparação das alternativas (Argon2id, bcrypt, PBKDF2, SHA-256) está em `docs/Funcionalidades/login.md`.

## 4. Cuidados extras de segurança

- **Mensagem de erro igual para tudo.** E-mail errado, senha errada ou perfil trocado mostram sempre "E-mail ou senha inválidos.". Quem tenta invadir não descobre quais e-mails existem.
- **Tempo de resposta igual.** Se o e-mail não existe, o sistema confere a senha contra um hash falso mesmo assim. Sem isso, a resposta mais rápida entregaria que o e-mail não está cadastrado.
- **Nenhuma senha em log.** Os testes confirmam que a senha não aparece nos registros.
- **Modo debug desligado no código.** Ele permite executar comandos pelo navegador, então só é ligado de propósito, com `FLASK_DEBUG=1`.
- **Limite de 16 KB por pedido.** Ninguém trava o servidor mandando dados gigantes.

## 5. Respostas possíveis

| Situação | Status | O que volta |
| --- | --- | --- |
| Tudo certo | 200 | Nome, e-mail e perfil |
| E-mail, senha ou perfil errado | 401 | "E-mail ou senha inválidos." |
| Campo vazio | 400 | "Preencha e-mail e senha." |
| E-mail mal escrito (ex.: `maria.com`) | 400 | "E-mail inválido." |
| Perfil diferente de publicador/receptor | 400 | "Perfil inválido." |
| Pedido maior que 16 KB | 413 | Recusado pelo Flask |

> **Para quem faz a tela (#6):** o fluxograma de login previa as mensagens "Usuário não encontrado" (CT04) e "Senha incorreta" (CT05). Por segurança, a issue #9 pediu que as duas virassem uma mensagem só. O bloqueio após 3 tentativas erradas (CT06) ficou fora do escopo e está anotado como limitação.

## 6. Usuários de teste

O `usuarios.json` tem um **publicador** (`publicador@exemplo.com`) e um **receptor** (`receptor@exemplo.com`), só com o hash da senha. As senhas reais **não ficam no GitHub**: peça ao Enzo por mensagem.

Para rodar e testar, na raiz do repositório:

```bat
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
cd src/backend
python app.py          # sobe a API em http://127.0.0.1:5000
python -m pytest       # roda os 24 testes
```

## 7. Do código até o merge

1. **Branch e código** (Enzo · feito)
   Branch `feature/enzoghislotti-backend-login` criada a partir da `develop`, como no nosso GitFlow. Back-end pronto, com 24 testes passando e teste no servidor de verdade.
2. **Commits e PR em rascunho** (Enzo · feito)
   Quatro commits no padrão Conventional Commits e o [PR #12](https://github.com/morangotangos-team/feedberry/pull/12) aberto como rascunho para a `develop`, com `Closes #9`.
3. **Testes e documentação** (Matheus · agora)
   Revisar e completar a base que já está na branch (veja a lista abaixo).
4. **Tirar o PR do rascunho** (Enzo)
   Quando o Matheus avisar que terminou.
5. **Revisão e merge** (outro integrante)
   Alguém que não escreveu o código nem os testes revisa e aprova. Depois do merge, a issue #9 fecha sozinha.

## 8. O que o Matheus vai validar

```bash
git fetch origin
git checkout feature/enzoghislotti-backend-login
```

- [ ] Rodar `python -m pytest` e conferir se os testes cobrem login válido e inválido. Completar o que faltar.
- [ ] Revisar `docs/Funcionalidades/login.md`: técnica escolhida, alternativas descartadas e o que acontece se o arquivo vazar.
- [ ] Conferir que nenhuma senha aparece em texto puro: código, `usuarios.json` e logs.
- [ ] Colocar o nome dele no Histórico do `login.md`.
- [ ] Commitar no padrão (`test(auth): …`, `docs(login): …`) e enviar na mesma branch.

---

Issue: [#9 · back-end de login](https://github.com/morangotangos-team/feedberry/issues/9) · Tela: [#6 · tela de login](https://github.com/morangotangos-team/feedberry/issues/6)

Grupo Morangotangos · Arquitetura de Software · PUC GO
