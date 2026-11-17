# Matriz de rastreabilidade

Última atividade da **2ª etapa** do [Processo de levantamento de requisitos](../../Processos_De_Requisitos/Processo%20de%20levantamento%20de%20requisitos.md). Liga cada requisito à sua origem (artefato de levantamento), ao caso de uso, à issue, ao documento, ao código e à situação atual.

| | |
|---|---|
| **Issue** | [#24](https://github.com/morangotangos-team/feedberry/issues/24) · [#31](https://github.com/morangotangos-team/feedberry/issues/31) |
| **Requisitos** | [Requisitos funcionais](../requisitos/Requisitos%20funcionais.md) · [Requisitos não funcionais](../requisitos/Requisitos%20nao%20funcionais.md) |
| **Casos de uso** | [Análise dos artefatos](../analise/Analise%20dos%20artefatos.md) (UC01 a UC14) |
| **Base** | Branch `develop` em 2026-11-16, mais os PRs abertos [#12](https://github.com/morangotangos-team/feedberry/pull/12), [#29](https://github.com/morangotangos-team/feedberry/pull/29) e [#30](https://github.com/morangotangos-team/feedberry/pull/30) |
| **Última atualização** | 2026-11-16 |

> ⚠️ As prioridades e os requisitos saem como **proposta**: ainda não foram validados com o cliente.

## 1. Como ler

**Fontes** (códigos da [análise dos artefatos](../analise/Analise%20dos%20artefatos.md)):

| Código | Artefato |
|--------|----------|
| **Q1-x** | Formulário 1 (líderes), pergunta da coluna x |
| **Q2-x** | Formulário 2 (colaboradores), pergunta da coluna x |
| **FL** | Fluxograma da página de login (CT01 a CT06) |
| **E1-n** | Entrevista com o líder, pergunta n da transcrição (`entrevista/Entrevista com Lider/Entrevista-lider_transcricao.md`) |
| **E2** | Gravação da reunião, ainda sem transcrição (não usada) |
| **DE** | Decisão da equipe (sem origem nos artefatos de levantamento) |

**Situação:**

| Símbolo | Significado |
|---------|-------------|
| ✅ Atendido | Funciona de ponta a ponta na `develop` |
| 🟡 Parcial | Existe só uma parte (tela com dados de exemplo, modelo de dados ou back-end sem integração) |
| 🔵 Em revisão | O que existe está em PR aberto, ainda fora da `develop` |
| ⛔ Sem issue | Nenhuma issue cobre a implementação |

Caminhos de código marcados com *(PR #n)* ainda não estão na `develop`.

## 2. Requisitos funcionais

| Requisito | Caso de uso | Fonte | Issue | Documento | Código | Situação |
|-----------|-------------|-------|-------|-----------|--------|----------|
| **RF01** Fazer login com e-mail e senha | UC01 | FL (CT01–CT05) | [#6](https://github.com/morangotangos-team/feedberry/issues/6) (tela, fechada) · [#9](https://github.com/morangotangos-team/feedberry/issues/9) (back-end) · [#16](https://github.com/morangotangos-team/feedberry/issues/16) (integração) · [#13](https://github.com/morangotangos-team/feedberry/issues/13) (banco) | [tela-de-login.md](../../Funcionalidades/tela-de-login.md) · `Funcionalidades/login.md` *(PR #12)* | `src/frontend/index.html`, `src/frontend/login/` · `src/backend/auth/`, `src/backend/repositories/` *(PR #12)* · `src/backend/models/usuario.py` *(PR #30)* | 🟡 Parcial: tela pronta sem autenticação real; back-end 🔵 em revisão; integração (#16) não iniciada |
| **RF02** Criar conta | UC02 | FL (CT04) | — | — | Só o modelo `src/backend/models/usuario.py` *(PR #30)*; a tela não tem link "Criar conta" | ⛔ Sem issue |
| **RF03** Enviar feedback ao colaborador | UC03 | Q1-F, Q1-G, Q1-L · E1-6, E1-11 | [#15](https://github.com/morangotangos-team/feedberry/issues/15) (home, fechada) · [#13](https://github.com/morangotangos-team/feedberry/issues/13) | [home-publicador.md](../../Funcionalidades/home-publicador.md) | Botão **Enviar feedback** em `src/frontend/publicador/home.html` (sem tela de envio) · `src/backend/models/feedback.py` *(PR #30)* | 🟡 Parcial: só o ponto de entrada e o modelo; tela de envio ⛔ sem issue |
| **RF04** Registrar pontos de melhoria no feedback | UC04 | Q1-M, Q2-L · E1-12 | [#15](https://github.com/morangotangos-team/feedberry/issues/15) · [#13](https://github.com/morangotangos-team/feedberry/issues/13) | [home-publicador.md](../../Funcionalidades/home-publicador.md) | `src/frontend/componentes/card-meta-ponto/` (exibição) · `src/backend/models/ponto_melhoria.py` *(PR #30)* | 🟡 Parcial: exibição com dados de exemplo; registro ⛔ sem issue |
| **RF05** Definir metas de desenvolvimento | UC05 | Q1-K, Q2-I, Q2-K, Q2-M · E1-11, E1-12 | [#13](https://github.com/morangotangos-team/feedberry/issues/13) | [home-receptor.md](../../Funcionalidades/home-receptor.md) (só exibição) | `src/backend/models/meta_desenvolvimento.py` *(PR #30)* | 🔵 Em revisão (só o modelo); tela de cadastro ⛔ sem issue |
| **RF06** Agendar retorno / lembrete de acompanhamento | UC06 | Q1-K, Q1-L, Q1-M, Q2-M · E1-7, E1-10 | [#15](https://github.com/morangotangos-team/feedberry/issues/15) · [#13](https://github.com/morangotangos-team/feedberry/issues/13) | [home-publicador.md](../../Funcionalidades/home-publicador.md) | Botão **Agendar retorno** em `src/frontend/publicador/` (mostra só um aviso) · `src/backend/models/lembrete.py` *(PR #30)* | 🟡 Parcial: botão sem fluxo; agendamento ⛔ sem issue |
| **RF07** Acompanhar evolução da equipe | UC07 | Q1-I, Q1-L, Q1-M · E1-1, E1-7 | [#15](https://github.com/morangotangos-team/feedberry/issues/15) · [#13](https://github.com/morangotangos-team/feedberry/issues/13) | [home-publicador.md](../../Funcionalidades/home-publicador.md) | `src/frontend/componentes/card-resumo/`, `card-meta-ponto/` · `src/backend/models/equipe.py`, `ponto_melhoria.py` *(PR #30)* | 🟡 Parcial: resumo com dados de exemplo; tela de acompanhamento ⛔ sem issue |
| **RF08** Gerar relatórios | UC08 | Q1-K, Q2-K | — | Citado como fora do escopo nas duas homes | — (será consulta sobre as tabelas do PR #30) | ⛔ Sem issue |
| **RF09** Visualizar feedbacks recebidos | UC09 | Q2-F, Q2-G | [#15](https://github.com/morangotangos-team/feedberry/issues/15) · [#13](https://github.com/morangotangos-team/feedberry/issues/13) | [home-receptor.md](../../Funcionalidades/home-receptor.md) | `src/frontend/receptor/`, `src/frontend/componentes/card-feedback/` · `src/backend/models/feedback.py` *(PR #30)* | 🟡 Parcial: tela com dados de exemplo; API ⛔ sem issue |
| **RF10** Consultar histórico de feedbacks | UC10 | Q1-H, Q1-K (4/4), Q2-H, Q2-K, Q2-L, Q2-M · E1-6, E1-8, E1-11, E1-12 | [#15](https://github.com/morangotangos-team/feedberry/issues/15) · [#13](https://github.com/morangotangos-team/feedberry/issues/13) | [home-publicador.md](../../Funcionalidades/home-publicador.md) · [home-receptor.md](../../Funcionalidades/home-receptor.md) | Blocos "recentes" (últimos 4) e link "Ver todos" nas duas homes · índice de histórico em `src/backend/models/feedback.py` *(PR #30)* | 🟡 Parcial: só os 4 mais recentes; tela de histórico completo ⛔ sem issue |
| **RF11** Acompanhar metas e evolução pessoal | UC11 | Q2-I, Q2-L, Q2-M | [#15](https://github.com/morangotangos-team/feedberry/issues/15) · [#13](https://github.com/morangotangos-team/feedberry/issues/13) | [home-receptor.md](../../Funcionalidades/home-receptor.md) | Bloco "Minhas metas" em `src/frontend/receptor/`, `componentes/card-meta-ponto/` · `src/backend/models/meta_desenvolvimento.py` *(PR #30)* | 🟡 Parcial: exibição com dados de exemplo |
| **RF12** Enviar feedback ao líder | UC12 | Q2-J | [#13](https://github.com/morangotangos-team/feedberry/issues/13) | [home-publicador.md](../../Funcionalidades/home-publicador.md) (cita UC12 no botão **Enviar feedback**) | Tipo `COLABORADOR_PARA_LIDER` em `src/backend/models/enums.py` *(PR #30)* | 🔵 Em revisão (só o modelo); tela ⛔ sem issue. Ver pendência 3 da seção 6 |
| **RF13** Enviar feedback anônimo | UC13 | Q2-K (2), Q2-L | [#15](https://github.com/morangotangos-team/feedberry/issues/15) · [#13](https://github.com/morangotangos-team/feedberry/issues/13) | [home-receptor.md](../../Funcionalidades/home-receptor.md) | Exibição "Anônimo" em `src/frontend/componentes/card-feedback/` · regras de anonimato em `src/backend/models/feedback.py` *(PR #30)* | 🟡 Parcial: só a exibição e o modelo; envio ⛔ sem issue |
| **RF14** Receber lembretes | UC14 | Q1-K, Q2-K, Q2-L, Q2-M · E1-10, E1-11, E1-12 | [#15](https://github.com/morangotangos-team/feedberry/issues/15) · [#13](https://github.com/morangotangos-team/feedberry/issues/13) | [home-publicador.md](../../Funcionalidades/home-publicador.md) · [home-receptor.md](../../Funcionalidades/home-receptor.md) | `src/frontend/componentes/lista-lembretes/` · `src/backend/models/lembrete.py` *(PR #30)* | 🟡 Parcial: lista com dados de exemplo; envio real (Serviço de notificação) ⛔ sem issue |

## 3. Requisitos não funcionais

| Requisito | Fonte | Issue | Documento | Código | Situação |
|-----------|-------|-------|-----------|--------|----------|
| **RNF01** Usabilidade: registrar um feedback deve ser simples e rápido | E1-11, E1-13 | — | — | — | ⛔ Sem issue (sem critério de medição definido) |
| **RNF02** Segurança: senha guardada só como hash, nunca em texto puro | DE ([#9](https://github.com/morangotangos-team/feedberry/issues/9)) | [#9](https://github.com/morangotangos-team/feedberry/issues/9) | `Funcionalidades/login.md` (RN06) *(PR #12)* · ADR-004 *(PR #29)* | `src/backend/auth/security.py` *(PR #12)* | 🔵 Em revisão |
| **RNF03** Segurança: a resposta do login não revela se o e-mail está cadastrado | DE ([#9](https://github.com/morangotangos-team/feedberry/issues/9)) | [#9](https://github.com/morangotangos-team/feedberry/issues/9) | `Funcionalidades/login.md` (RN04) *(PR #12)* | `src/backend/auth/service.py` *(PR #12)* | 🔵 Em revisão. Diverge do FL (CT04, CT05) |
| **RNF04** Privacidade: o autor de um feedback anônimo não é guardado nem exibido | Q2-L (imparcialidade, privacidade) | [#15](https://github.com/morangotangos-team/feedberry/issues/15) · [#13](https://github.com/morangotangos-team/feedberry/issues/13) | [home-receptor.md](../../Funcionalidades/home-receptor.md) | `src/frontend/componentes/card-feedback/` · `src/backend/models/feedback.py` *(PR #30)* | 🟡 Parcial. Depende da dúvida 4 da análise |
| **RNF05** Responsividade: as telas funcionam em computador e celular | DE ([#6](https://github.com/morangotangos-team/feedberry/issues/6), [#15](https://github.com/morangotangos-team/feedberry/issues/15)) | [#6](https://github.com/morangotangos-team/feedberry/issues/6) · [#15](https://github.com/morangotangos-team/feedberry/issues/15) | [tela-de-login.md](../../Funcionalidades/tela-de-login.md) (RN11) · homes | `src/frontend/login/login.css`, `src/frontend/componentes/layout-home/` | ✅ Atendido nas telas existentes |
| **RNF06** Acessibilidade: navegação por teclado e suporte a leitor de tela no login | DE ([#6](https://github.com/morangotangos-team/feedberry/issues/6)) | [#6](https://github.com/morangotangos-team/feedberry/issues/6) | [tela-de-login.md](../../Funcionalidades/tela-de-login.md) (RN02, RN06, RN07) | `src/frontend/login/login.js` | ✅ Atendido na tela de login |
| **RNF07** Integridade: o histórico não pode sumir (usuários são desativados, não apagados) | Q1-K (4/4) · E1-8 | [#13](https://github.com/morangotangos-team/feedberry/issues/13) | `Arquitetura/banco-de-dados/README.md` · ADR-007 *(PR #30)* | `src/backend/models/usuario.py` *(PR #30)* | 🔵 Em revisão |
| **RNF08** Portabilidade: o banco pode trocar de SQLite para PostgreSQL por configuração | DE ([#13](https://github.com/morangotangos-team/feedberry/issues/13)) | [#13](https://github.com/morangotangos-team/feedberry/issues/13) | ADR-007 *(PR #30)* | `src/backend/config.py` *(PR #30)* | 🔵 Em revisão |

## 4. Requisitos sem issue

Requisitos (ou partes) que nenhuma issue aberta ou fechada cobre.

| Requisito | O que falta |
|-----------|-------------|
| RF02 | Tudo: tela de cadastro, API e decisão sobre quem cria as contas (dúvida 2 da análise) |
| RF03, RF12, RF13 | Tela e API de envio de feedback (líder → colaborador, colaborador → líder e anônimo) |
| RF04 | Registro e atualização de status dos pontos de melhoria |
| RF05 | Tela e API de cadastro de metas |
| RF06 | Fluxo de agendamento de retorno |
| RF07 | Tela de acompanhamento da equipe |
| RF08 | Tudo: conteúdo e formato do relatório (dúvida 8 da análise) |
| RF09, RF10, RF11 | API que troca os dados de exemplo (`dados-mock.js`) por dados reais; tela de histórico completo |
| RF14 | Envio real dos lembretes e definição do canal (dúvida 6 da análise) |
| RNF01 | Critério de medição e issue de validação com usuários |

## 5. Itens do código sem requisito de origem

Itens que existem no código (ou em PR aberto) e não vêm de nenhum requisito nem de artefato de levantamento.

| Item | Onde está | Observação |
|------|-----------|------------|
| Perfis **publicador / receptor** (abas do login e campo `perfil` da API) | `src/frontend/index.html`, `src/frontend/login/login.js` · `src/backend/auth/` *(PR #12)* | A análise usa os atores **Líder / Colaborador**. Decisão em aberto no ADR-006 *(PR #29)* |
| Tema claro / escuro | `src/frontend/utils/tema.js`, `tema-inicial.js` | Decisão da equipe; não aparece nos questionários nem na entrevista |
| "Manter conectado" | `src/frontend/index.html` | Só visual |
| "Esqueci minha senha" (recuperação de senha) | `src/frontend/index.html`, `src/frontend/login/login.js` | Só visual. Pode responder à dúvida 9 da análise |
| Botão **Agradecer** no feedback recebido | `src/frontend/receptor/home.js`, `src/frontend/componentes/card-feedback/` | Não há caso de uso de agradecer feedback |
| Tipo do feedback (elogio, construtivo, ideia) e competências | `src/frontend/publicador/dados-mock.js`, `src/frontend/receptor/dados-mock.js` | Não existem no modelo de dados do PR #30, que usa outro `tipo` (direção do feedback) |
| Senha com no mínimo 6 caracteres | `src/frontend/login/login.js` | Regra do protótipo; a #16 prevê retirar |
| Contador de tentativas de login | `tentativas_login_falhas` em `src/backend/models/usuario.py` *(PR #30)* | Vem do FL (CT06), que não virou caso de uso nem requisito (dúvida 9) |
| Equipes (quem é líder de quem) | `src/backend/models/equipe.py` *(PR #30)* | Sustenta RF07 e RF08, mas a gestão de equipes não tem caso de uso (dúvida 3) |
| Desativação de usuário | `ativo` em `src/backend/models/usuario.py` *(PR #30)* | Não há caso de uso de desativar conta |

## 6. Pendências e divergências

1. **E2 sem transcrição:** a gravação da reunião não foi usada como fonte. Quando for transcrita, a coluna **Fonte** deve ser complementada.
2. **FL × back-end:** o fluxograma prevê as mensagens "Usuário não encontrado" (CT04) e "Senha incorreta" (CT05); o back-end responde com uma mensagem única (RNF03). O fluxograma precisa ser atualizado ou a decisão registrada.
3. **RF12 × perfis:** o colaborador entra como **receptor**, mas o botão **Enviar feedback** está só na home do **publicador**. Com os perfis atuais, o colaborador não tem por onde enviar feedback ao líder (RF12, RF13). Depende do ADR-006.
4. **Rastreabilidade nos documentos de funcionalidade:** `home-publicador.md` e `home-receptor.md` não têm a tabela de rastreabilidade do template de funcionalidade; só `tela-de-login.md` tem a tabela (RF01).
5. **Dúvidas abertas com o cliente:** as 10 dúvidas da seção 5 da análise continuam sem resposta e afetam RF02, RF06, RF08, RF13 e RF14.

## Histórico

| Data | Autor(a) | Alteração |
|------|----------|-----------|
| 2026-11-16 | Paula Silvério de Castro | Criação da matriz de rastreabilidade (issues #24 e #31) |
