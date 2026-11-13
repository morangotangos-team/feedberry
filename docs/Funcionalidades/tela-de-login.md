# Tela de login

| | |
|---|---|
| **Status** | Em revisão (somente front-end, sem autenticação real) |
| **Perfis** | Publicador / Receptor |
| **Issue** | #6 |
| **Última atualização** | 2026-11-13 |

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
5. Clique em **Entrar**.

O botão **🌙 Tema noturno**, no canto superior direito, troca entre o tema claro e o escuro. A escolha fica lembrada no navegador.

### Telas

| Tela | O que aparece |
|------|---------------|
| Acesso do publicador | Abas **Publicador** (selecionada) e **Receptor**, título "Acesso do publicador", campos de e-mail e senha, "Manter conectado", "Esqueci minha senha" e o botão **Entrar** |
| Acesso do receptor | Os mesmos campos, com a aba **Receptor** selecionada e o título "Acesso do receptor" |
| Mensagem de erro | O campo com problema fica com a borda destacada e a mensagem aparece logo abaixo da senha |
| Celular | A identidade visual (logo, morango e frase) vai para o topo e o formulário ocupa a largura da tela |

> 🖼️ Os prints das telas entram em `imagens/login/` (pendência registrada no PR desta documentação).

### Dúvidas comuns

| Situação | O que fazer |
|----------|-------------|
| "Digite o seu e-mail." | O campo de e-mail ficou em branco. Preencha e tente de novo. |
| "Digite um e-mail válido, como nome@empresa.com." | O e-mail está sem `@` ou sem domínio (ex.: `maria.com`). Confira o que foi digitado. |
| "Digite a sua senha." | O campo de senha ficou em branco. |
| "A senha precisa ter pelo menos 6 caracteres." | A senha digitada é curta demais. |
| Cliquei em **Entrar** e não fui para outra tela | É o esperado nesta versão: a tela só confere os campos e mostra um aviso. A entrada de verdade chega com a integração (#16). |
| "Recuperação de senha em breve" | O link **Esqueci minha senha** ainda é só visual. |
| Não sei em qual acesso estou | Veja a aba destacada e o título do formulário ("Acesso do publicador" ou "Acesso do receptor"). |

---

## ⚙️ Funcionamento

### Objetivo

Dar ao publicador e ao receptor uma entrada clara e separada no FeedBerry, com a identidade visual do projeto, e barrar no navegador os erros de preenchimento mais comuns antes de qualquer envio.

Esta entrega é **somente front-end** (HTML, CSS e JavaScript). Não há back-end, API, banco de dados nem autenticação real.

### Como rodar e testar

Os arquivos usam módulos ES, que não funcionam abrindo o HTML direto do disco (`file://`). Dentro de `src/frontend/`:

```bash
python -m http.server
```

| Tela | Endereço |
|------|----------|
| Acesso do publicador | http://localhost:8000/ |
| Acesso do receptor | http://localhost:8000/#receptor |

### Regras de negócio

| # | Regra |
|---|-------|
| RN01 | Há dois acessos, publicador e receptor, cada um com o seu formulário e o seu título. A tela abre no publicador. |
| RN02 | A troca entre os acessos é feita pelas abas, por clique ou pelo teclado (setas, Home e End). O acesso escolhido vai para o endereço (`#publicador` ou `#receptor`), o que permite abrir a tela direto em um deles. |
| RN03 | O título da aba do navegador acompanha o acesso selecionado. |
| RN04 | O e-mail é obrigatório e precisa ter formato válido. Espaços nas pontas são ignorados. |
| RN05 | A senha é obrigatória e precisa ter pelo menos 6 caracteres. |
| RN06 | A validação mostra **um erro por vez**, na ordem e-mail → senha. O campo com erro recebe o foco e é marcado com `aria-invalid`. A mensagem some quando a pessoa volta a digitar. |
| RN07 | A senha começa oculta. O botão do olho mostra ou oculta a senha e atualiza o seu rótulo para leitores de tela. |
| RN08 | "Esqueci minha senha" é só visual: mostra o aviso "Recuperação de senha em breve". |
| RN09 | Com os campos válidos, a tela mostra um aviso e **não envia nada**: nenhuma requisição é feita e a senha não é guardada. |
| RN10 | Cores e fontes vêm de `estilos/tokens.css`. A tela funciona nos temas claro e escuro. |
| RN11 | Abaixo de 820 px de largura o layout passa de duas colunas para uma. |

### Arquivos envolvidos

| Arquivo | Responsabilidade |
|---------|------------------|
| `src/frontend/index.html` | Estrutura da tela: identidade visual, abas e os dois formulários |
| `src/frontend/login/login.css` | Layout da tela, abas, formulário e ajuste para celular |
| `src/frontend/login/login.js` | Troca de abas, mostrar/ocultar senha, validação e avisos |
| `src/frontend/estilos/tokens.css` e `base.css` | Cores, fontes, temas e estilos gerais (botões, tipografia) |
| `src/frontend/componentes/berry/` | Ilustração do morango |
| `src/frontend/componentes/cabecalho/` | Marca (logo) do FeedBerry |
| `src/frontend/componentes/toast/` | Aviso temporário usado em "Entrar" e em "Esqueci minha senha" |
| `src/frontend/utils/tema.js` e `tema-inicial.js` | Tema claro/escuro e a escolha lembrada no navegador |

### Limitações conhecidas

- Não há autenticação real: qualquer e-mail em formato válido com senha de 6 ou mais caracteres passa na validação, e a tela só mostra um aviso. A ligação com a API é da #16; o back-end é da #9.
- Depois de **Entrar**, a pessoa ainda não é levada para a home do seu perfil (#15 / #16).
- "Manter conectado" é só visual: nada é guardado.
- "Esqueci minha senha" não recupera a senha.
- As regras de validação são do protótipo. A #16 alinha o front com o back-end (#9): tira o mínimo de 6 caracteres, que é regra de cadastro, e passa a usar o mesmo formato de e-mail do back-end.
- O back-end responde a e-mail inexistente e a senha errada com uma mensagem só ("E-mail ou senha inválidos."). As mensagens "Usuário não encontrado" (CT04) e "Senha incorreta" (CT05) do fluxograma não serão usadas.
- Não há link para criar conta (UC02) nem bloqueio após 3 tentativas erradas (CT06).
- As fontes são carregadas do Google Fonts. Sem internet, a tela usa as fontes do sistema.
- A documentação do back-end do login fica em `login.md`, criado pela #9. As duas partes devem virar um documento só quando a tela for integrada (#16).

### Rastreabilidade

| Issue | Requisito | Caso de uso |
|-------|-----------|-------------|
| #6 (tela) · relacionadas: #9 (back-end), #16 (integração) | A definir | UC01 Fazer login · fluxograma de login (CT01 a CT05) |

### Histórico

| Data | Autor(a) | Alteração |
|------|----------|-----------|
| 2026-11-13 | Paula Silvério de Castro | Criação da documentação da tela de login (o código entrou pelos PRs #14 e #21) |
