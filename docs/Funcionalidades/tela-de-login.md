# Tela de login

| | |
|---|---|
| **Status** | Em revisão (integrada à API de login na #16) |
| **Perfis** | Publicador / Receptor |
| **Issue** | #6 · #16 (integração com a API) |
| **Última atualização** | 2026-11-17 |

---

## 👤 Para o usuário

### O que é

A tela de login é a porta de entrada do FeedBerry. Nela a pessoa escolhe o tipo de acesso (publicador ou receptor), digita o e-mail e a senha e clica em **Entrar**.

### Quem usa

- Publicador do feedback: entra para escrever e enviar feedbacks para o time.
- Receptor do feedback: entra para ler os feedbacks que recebeu e acompanhar as suas metas.

### Como usar

1. Abra o FeedBerry. A tela começa no **Acesso do publicador**.
2. Se você for receptor, clique na aba **Receptor**, no alto do formulário. O título muda para **Acesso do receptor**.
3. Digite o seu e-mail.
4. Digite a sua senha. Para conferir o que digitou, clique no olho (👁️) ao lado do campo; clique de novo para esconder.
5. Clique em **Entrar**. Se os dados conferirem, você vai para a home do seu perfil. O passo a passo completo, com "Manter conectado" e **Sair**, está em [Login](login.md).

O botão **🌙 Tema noturno**, no canto superior direito, troca entre o tema claro e o escuro. A escolha fica lembrada no navegador.

### Telas

| Tela | O que aparece |
|------|---------------|
| Acesso do publicador | Abas **Publicador** (selecionada) e **Receptor**, título "Acesso do publicador", campos de e-mail e senha, "Manter conectado", "Esqueci minha senha" e o botão **Entrar** |
| Acesso do receptor | Os mesmos campos, com a aba **Receptor** selecionada e o título "Acesso do receptor" |
| Mensagem de erro | O campo com problema fica com a borda destacada e a mensagem aparece logo abaixo da senha |
| Celular | A identidade visual (logo, morango e frase) vai para o topo e o formulário ocupa a largura da tela |

![Acesso do publicador](imagens/login/tela-login-publicador.png)

![Acesso do receptor](imagens/login/tela-login-receptor.png)

![Mensagem de erro no celular](imagens/login/tela-login-celular-erro.png)

### Dúvidas comuns

| Situação | O que fazer |
|----------|-------------|
| "Preencha e-mail e senha." | O e-mail ou a senha ficou em branco. Preencha os dois e tente de novo. |
| "E-mail inválido." | O e-mail está sem `@` ou sem domínio (ex.: `maria.com`). Confira o que foi digitado. |
| "E-mail ou senha inválidos." | Os dados não conferem, ou você está na aba do outro perfil. As demais mensagens vindas do servidor estão em [Login](login.md). |
| "Recuperação de senha em breve" | O link **Esqueci minha senha** ainda é só visual. |
| Não sei em qual acesso estou | Veja a aba destacada e o título do formulário ("Acesso do publicador" ou "Acesso do receptor"). |

---

## ⚙️ Funcionamento

### Objetivo

Dar ao publicador e ao receptor uma entrada clara e separada no FeedBerry, com a identidade visual do projeto, e barrar no navegador os erros de preenchimento mais comuns antes de qualquer envio.

A tela foi feita em HTML, CSS e JavaScript (#6) e, na #16, foi ligada à API de login: ela envia as credenciais para `POST /auth/login` e leva a pessoa para a home do perfil. As regras do back-end e da integração estão em [Login](login.md).

### Como rodar e testar

Com a API (login real), a partir de `src/backend/`:

```bash
python app.py
```

| Tela | Endereço |
|------|----------|
| Acesso do publicador | http://127.0.0.1:5000/ |
| Acesso do receptor | http://127.0.0.1:5000/#receptor |

Só as telas, sem API (o **Entrar** mostra erro de conexão), dentro de `src/frontend/`: `python -m http.server` e abra http://localhost:8000/. Os módulos ES não funcionam abrindo o HTML direto do disco (`file://`).

### Regras de negócio

| # | Regra |
|---|-------|
| RN01 | Há dois acessos, publicador e receptor, cada um com o seu formulário e o seu título. A tela abre no publicador. |
| RN02 | A troca entre os acessos é feita pelas abas, por clique ou pelo teclado (setas, Home e End). O acesso escolhido vai para o endereço (`#publicador` ou `#receptor`), o que permite abrir a tela direto em um deles. |
| RN03 | O título da aba do navegador acompanha o acesso selecionado. |
| RN04 | O e-mail é obrigatório e precisa ter formato válido, com a mesma regra do back-end. Espaços nas pontas são ignorados. |
| RN05 | A senha é obrigatória. Não há tamanho mínimo no login (essa é uma regra de cadastro). |
| RN06 | A validação mostra **um erro por vez**, na ordem e-mail → senha. O campo com erro recebe o foco e é marcado com `aria-invalid`. A mensagem some quando a pessoa volta a digitar. |
| RN07 | A senha começa oculta. O botão do olho mostra ou oculta a senha e atualiza o seu rótulo para leitores de tela. |
| RN08 | "Esqueci minha senha" é só visual: mostra o aviso "Recuperação de senha em breve". |
| RN09 | Com os campos válidos, a tela envia as credenciais para a API e segue as regras RN08 a RN13 de [Login](login.md). A senha nunca é guardada. |
| RN10 | Cores e fontes vêm de `estilos/tokens.css`. A tela funciona nos temas claro e escuro. |
| RN11 | Abaixo de 820 px de largura o layout passa de duas colunas para uma. |

### Arquivos envolvidos

| Arquivo | Responsabilidade |
|---------|------------------|
| `src/frontend/index.html` | Estrutura da tela: identidade visual, abas e os dois formulários |
| `src/frontend/login/login.css` | Layout da tela, abas, formulário e ajuste para celular |
| `src/frontend/login/login.js` | Troca de abas, mostrar/ocultar senha, validação, envio para a API e redirecionamento |
| `src/frontend/utils/validacao.js` | Regras de validação do login, iguais às do back-end |
| `src/frontend/servicos/` | Chamada à API e identidade de quem entrou (detalhes em [Login](login.md)) |
| `src/frontend/estilos/tokens.css` e `base.css` | Cores, fontes, temas e estilos gerais (botões, tipografia) |
| `src/frontend/componentes/berry/` | Ilustração do morango |
| `src/frontend/componentes/cabecalho/` | Marca (logo) do FeedBerry |
| `src/frontend/componentes/toast/` | Aviso temporário usado em "Esqueci minha senha" |
| `src/frontend/utils/tema.js` e `tema-inicial.js` | Tema claro/escuro e a escolha lembrada no navegador |

### Limitações conhecidas

- Não há sessão real no back-end: "Manter conectado" só lembra quem entrou no navegador e não protege as homes (ver [Login](login.md)).
- "Esqueci minha senha" não recupera a senha.
- O back-end responde a e-mail inexistente e a senha errada com uma mensagem só ("E-mail ou senha inválidos."). As mensagens "Usuário não encontrado" (CT04) e "Senha incorreta" (CT05) do fluxograma não serão usadas.
- Não há link para criar conta (UC02) nem bloqueio após 3 tentativas erradas (CT06).
- As fontes são carregadas do Google Fonts. Sem internet, a tela usa as fontes do sistema.
- A documentação do back-end e da integração fica em [Login](login.md). Este documento continua cuidando só da tela.
- Os prints acima são de antes da integração: ainda mostram a dica "Protótipo" e o placeholder "Mínimo de 6 caracteres", que saíram da tela. Os arquivos ficam em `docs/Funcionalidad/imagens/login/`, pasta com nome errado (#26).

### Rastreabilidade

| Issue | Requisito | Caso de uso |
|-------|-----------|-------------|
| #6 (tela) · relacionadas: #9 (back-end), #16 (integração) | [RF01](../Artefatos_Requisitos/requisitos/Requisitos%20funcionais.md) · RNF05, RNF06 | UC01 Fazer login · fluxograma de login (CT01 a CT05) |

### Histórico

| Data | Autor(a) | Alteração |
|------|----------|-----------|
| 2026-11-13 | Paula Silvério de Castro | Criação da documentação da tela de login (o código entrou pelos PRs #14 e #21) |
| 2026-11-16 | Paula Silvério de Castro | Rastreabilidade: requisito "A definir" trocado por RF01 (issue #24) |
| 2026-11-17 | Enzo | Integração com a API (issue #16): status, passo a passo, mensagens, como rodar, RN04, RN05, RN09, arquivos e limitações |
