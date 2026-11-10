# Documentação de funcionalidades

Este documento define o processo de documentação das features do **FeedBerry**. A regra é simples:

> 📌 **Uma feature só está pronta quando o código e a documentação estão prontos.**

A documentação faz parte da **Definição de Pronto (Definition of Done)** e entra no **mesmo pull request** da feature. Ela não fica para uma issue “de documentação depois”.

---

## 1. Por que documentar cada feature

- **Para o usuário:** explica como usar a funcionalidade, sem precisar perguntar para quem desenvolveu;
- **Para a equipe:** registra regras de negócio, decisões e limitações, o que facilita manutenção e revisão;
- **Para a disciplina:** liga cada funcionalidade ao requisito e ao caso de uso de origem, o que alimenta a **matriz de rastreabilidade**.

---

## 2. Quando a documentação é obrigatória

| Tipo de mudança | Precisa documentar? | O que fazer |
|-----------------|---------------------|-------------|
| `feat`: nova funcionalidade | ✅ Sim | Criar o documento da funcionalidade |
| `feat`: mudança em funcionalidade existente | ✅ Sim | Atualizar o documento que já existe |
| `fix` que muda o comportamento para o usuário | ⚠️ Sim, se mudar algo | Atualizar o documento (regras, passo a passo ou limitações) |
| `fix` interno, `refactor`, `style`, `chore`, `test` | ❌ Não | Nada, a menos que algo do documento fique desatualizado |
| `docs` | ❌ Não | — |

> 💡 Na dúvida, pergunte: *“Depois dessa mudança, alguma informação do documento ficou errada?”* Se a resposta for sim, atualize o documento.

---

## 3. Onde fica a documentação

Cada funcionalidade tem **um único arquivo markdown** em `docs/Funcionalidades/`, com duas partes: **Para o usuário** e **Funcionamento**.

```
docs/
└── Funcionalidades/
    ├── README.md            # índice com todas as funcionalidades
    ├── login.md
    ├── envio-de-feedback.md
    └── imagens/
        └── login/
            └── tela-login-publicador.png
```

| Item | Padrão | Exemplo |
|------|--------|---------|
| Nome do arquivo | minúsculas, sem acento, palavras separadas por hífen | `envio-de-feedback.md` |
| Imagens | `docs/Funcionalidades/imagens/<nome-da-feature>/` | `imagens/login/tela-login-receptor.png` |
| Índice | Adicionar uma linha no `docs/Funcionalidades/README.md` | — |

---

## 4. O que cada parte deve conter

O modelo pronto para copiar está em [Template de documentacao de funcionalidade.md](Template%20de%20documentacao%20de%20funcionalidade.md).

### 👤 Parte 1: Para o usuário

Escrita em linguagem simples, sem termos técnicos.

| Seção | O que escrever |
|-------|----------------|
| O que é | Uma ou duas frases sobre o que a funcionalidade permite fazer |
| Quem usa | Perfil(is): publicador, receptor, líder etc. |
| Como usar | Passo a passo numerado |
| Telas | Prints das telas |
| Dúvidas comuns | Mensagens de erro e o que fazer em cada caso (opcional) |

### ⚙️ Parte 2: Funcionamento

Escrita para a equipe.

| Seção | O que escrever |
|-------|----------------|
| Objetivo | Qual problema a funcionalidade resolve |
| Regras de negócio | Regras e validações (ex.: “o receptor não acessa a tela do publicador”) |
| Arquivos envolvidos | Principais arquivos/pastas do `src/` |
| Limitações conhecidas | O que ainda não funciona ou foi deixado de fora |
| Rastreabilidade | Issue, requisito e caso de uso de origem |
| Histórico | Data, autor(a) e o que mudou em cada versão |

---

## 5. Fluxo no dia a dia

```
Issue ──► Branch feature/* ──► Código ──► Documentação ──► PR (checklist) ──► Revisão ──► Merge
                                              ▲                                   │
                                              └──── revisor pede ajuste ◄─────────┘
```

1. Pegue a issue e crie a branch `feature/*` a partir da `develop` (ver [Padrão de commit e GitFlow](Padrao%20de%20commit%20e%20GitFlow.md));
2. Desenvolva a funcionalidade;
3. Copie o template para `docs/Funcionalidades/<nome-da-feature>.md` e preencha;
4. Adicione a funcionalidade no índice `docs/Funcionalidades/README.md`;
5. Faça o commit da documentação separado do código:
   ```bash
   git commit -m "docs(login): adiciona documentação da tela de login"
   ```
6. Abra o PR. O template de PR já traz o checklist de documentação;
7. Quem revisa **só aprova** se a documentação estiver criada ou atualizada.

---

## 6. Responsabilidades

| Quem | Responsabilidade |
|------|------------------|
| Quem desenvolve a feature | Escrever ou atualizar a documentação no mesmo PR |
| Quem revisa o PR | Conferir se a documentação existe, está completa e bate com o que foi feito |
| Gerente de projetos | Garantir que o processo está sendo seguido e manter o índice organizado |

---

## 7. Tabela de dúvidas rápidas

| Situação | O que fazer |
|----------|-------------|
| A feature é só front-end (HTML/CSS/JS) | Documente do mesmo jeito; o documento fica menor |
| A feature ainda não está ligada ao back-end | Escreva em **Limitações conhecidas** (ex.: “login sem autenticação real”) |
| Não sei qual é o requisito ou caso de uso | Coloque a issue e deixe o restante como `A definir`; avise no PR |
| Mudei uma tela que já tinha print | Atualize o print |
| A feature foi dividida em várias issues | Use um único documento e liste todas as issues em **Rastreabilidade** |
| Removi uma funcionalidade | Apague o documento e a linha do índice no mesmo PR |
| O PR foi aprovado sem documentação | Abra uma issue `docs` na hora e trate como pendência da feature |
