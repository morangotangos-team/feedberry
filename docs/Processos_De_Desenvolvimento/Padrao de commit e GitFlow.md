# Padrão de commit e GitFlow

Este documento define como o grupo **Morangotangos** organiza branches, commits e pull requests no repositório do **FeedBerry**. O fluxo adotado é o **GitFlow**, e as mensagens de commit seguem o padrão **Conventional Commits**.

> 💡 Em caso de dúvida, consulte as tabelas de referência rápida ao longo do documento.

---

## 1. Visão geral do GitFlow

O GitFlow organiza o trabalho em branches com papéis bem definidos. Ninguém faz commit direto na `main` nem na `develop`: todo trabalho entra por meio de **pull request (PR)**.

```
main      ●───────────────────●─────────────────●──────
           \                 / \               /
hotfix      \               /   ●──●──────────●
             \             /                 /
release       \       ●──●──●               /
               \     /       \             /
develop         ●──●──●──●────●──●──●─────●──────
                    \    /        \     /
feature              ●──●          ●──●
```

### Branches do projeto

| Branch | Para que serve | Criada a partir de | Faz merge em | Vida útil |
|--------|----------------|--------------------|--------------|-----------|
| `main` | Código estável, pronto para entrega/apresentação | — | — | Permanente |
| `develop` | Integração do trabalho em andamento | `main` | `release/*` | Permanente |
| `feature/*` | Nova funcionalidade, documento ou artefato | `develop` | `develop` | Temporária |
| `release/*` | Preparar uma entrega (ajustes finais, versão) | `develop` | `main` **e** `develop` | Temporária |
| `hotfix/*` | Correção urgente de algo que já está na `main` | `main` | `main` **e** `develop` | Temporária |

---

## 2. Nomenclatura de branches

Formato:

```
<tipo>/<seu-usuario>-<descricao-curta>
```

- Use letras minúsculas, sem acentos e sem espaços;
- Separe palavras com hífen (`-`);
- A descrição deve ser curta e dizer **o que** a branch faz.

| Tipo | Exemplo |
|------|---------|
| `feature` | `feature/aimecouto-audio-entrevista` |
| `feature` | `feature/paula-diagrama-casos-de-uso` |
| `release` | `release/entrega-1` ou `release/v1.0.0` |
| `hotfix` | `hotfix/fernando-link-quebrado-readme` |

---

## 3. Padrão de mensagem de commit

Formato (Conventional Commits):

```
<tipo>(<escopo opcional>): <descrição no imperativo>

[corpo opcional: explica o porquê da mudança]

[rodapé opcional: ex. "Closes #12"]
```

### Regras

- A descrição começa com letra minúscula e **não** termina com ponto;
- Escreva em português, no imperativo ou presente: “adiciona”, “corrige”, “atualiza”;
- Mantenha a primeira linha com até **72 caracteres**;
- Um commit = uma mudança lógica. Evite commits do tipo “várias coisas”.

### Tipos de commit

| Tipo | Quando usar | Exemplo |
|------|-------------|---------|
| `feat` | Nova funcionalidade no código | `feat(feedback): adiciona envio de feedback anônimo` |
| `fix` | Correção de bug | `fix(login): corrige validação de e-mail` |
| `docs` | Somente documentação (README, requisitos, diagramas) | `docs: adiciona processo de levantamento de requisitos` |
| `style` | Formatação, espaços, ponto e vírgula (sem mudar lógica) | `style: padroniza indentação dos componentes` |
| `refactor` | Mudança de código que não corrige bug nem cria funcionalidade | `refactor(api): extrai serviço de notificações` |
| `test` | Adiciona ou ajusta testes | `test(feedback): cobre envio sem destinatário` |
| `chore` | Tarefas de manutenção (dependências, configs, arquivos auxiliares) | `chore: adiciona .gitignore` |
| `build` | Sistema de build ou dependências externas | `build: atualiza versão do node` |
| `ci` | Pipelines de integração contínua | `ci: adiciona workflow de testes` |
| `perf` | Melhoria de desempenho | `perf(historico): pagina lista de feedbacks` |
| `revert` | Desfaz um commit anterior | `revert: desfaz "feat: adiciona ranking"` |

### Exemplos bons x ruins

| ❌ Evite | ✅ Prefira |
|---------|-----------|
| `Add files via upload` | `docs: adiciona áudio da entrevista com stakeholder` |
| `ajustes` | `fix(readme): corrige link do questionário` |
| `Update README.md` | `docs(readme): atualiza papéis da equipe` |
| `feat: Adicionei a tela de login.` | `feat(login): adiciona tela de login` |

---

## 4. Passo a passo do dia a dia

### Criando uma feature

```bash
git checkout develop
git pull origin develop
git checkout -b feature/seu-usuario-descricao
```

### Trabalhando e commitando

```bash
git add <arquivos>
git commit -m "docs: adiciona diagrama de contexto"
git push -u origin feature/seu-usuario-descricao
```

### Abrindo o pull request

1. No GitHub, abra um PR da sua `feature/*` para a **`develop`**;
2. Dê um título no mesmo padrão dos commits (ex.: `docs: adiciona diagrama de contexto`);
3. Descreva o que foi feito e marque pelo menos **1 integrante** para revisar;
4. Após aprovação, faça o merge e apague a branch.

### Regra de revisão obrigatória

A `main` e a `develop` são **branches protegidas** no GitHub:

| Regra | Como funciona |
|-------|---------------|
| Merge só via pull request | Ninguém consegue fazer push direto na `main` nem na `develop` |
| **1 aprovação** obrigatória | O botão de merge fica bloqueado até alguém aprovar o PR |
| Não vale aprovar o próprio PR | A aprovação tem que ser de **outro integrante** |
| Force push e exclusão bloqueados | Não dá para reescrever o histórico nem apagar essas branches |
| Exceção do admin | O admin pode dar merge sem aprovação, marcando *“Merge without waiting for requirements to be met”*. **Use só em emergência** (ex.: entrega da disciplina no prazo e ninguém disponível para revisar) e avise o grupo |

### Fazendo uma entrega (release)

```bash
git checkout develop
git pull origin develop
git checkout -b release/entrega-1
# ajustes finais, revisão de documentos...
```

Abra um PR de `release/entrega-1` para a **`main`**. Depois do merge, crie a tag e leve as alterações de volta para a `develop`:

```bash
git checkout main
git pull origin main
git tag -a v1.0.0 -m "Entrega 1"
git push origin v1.0.0
```

### Corrigindo algo urgente (hotfix)

```bash
git checkout main
git pull origin main
git checkout -b hotfix/seu-usuario-descricao
```

Abra o PR para a **`main`** e, depois, outro para a **`develop`**, para que a correção não se perca.

---

## 5. Tabela de dúvidas rápidas

| Situação | O que fazer |
|----------|-------------|
| Vou começar algo novo | Crie uma `feature/*` a partir da `develop` |
| Só vou mexer em documentação | Também é `feature/*`; use commits do tipo `docs` |
| Achei um erro no que já foi entregue (`main`) | Crie um `hotfix/*` a partir da `main` |
| Vamos fechar uma entrega da disciplina | Crie uma `release/*` a partir da `develop` |
| Posso fazer commit direto na `main` ou `develop`? | **Não.** Sempre via pull request, e o GitHub bloqueia o push direto |
| O botão de merge do meu PR está bloqueado | Falta a aprovação de 1 integrante. Peça revisão para alguém do grupo |
| Posso aprovar meu próprio PR? | **Não.** A aprovação tem que ser de outra pessoa |
| Para onde vai o PR da minha feature? | Para a `develop` |
| Para onde vai o PR de release/hotfix? | Para a `main` (e depois sincronize a `develop`) |
| Minha branch ficou desatualizada | `git checkout develop && git pull`, depois `git checkout sua-branch && git merge develop` |
| Errei a mensagem do último commit (ainda não dei push) | `git commit --amend -m "nova mensagem"` |
| Já dei push com mensagem errada | Deixe como está e capriche nos próximos; não reescreva histórico compartilhado |
| Não sei qual tipo de commit usar | Mudou só texto/doc → `docs`; corrigiu algo → `fix`; algo novo → `feat`; manutenção → `chore` |
| Meu commit mistura várias coisas | Separe em commits menores, um para cada mudança |

---

## 6. Versionamento

As versões marcadas na `main` seguem o **Versionamento Semântico** (`MAJOR.MINOR.PATCH`):

| Parte | Quando incrementar | Exemplo |
|-------|--------------------|---------|
| `MAJOR` | Mudança grande, que quebra compatibilidade | `1.0.0` → `2.0.0` |
| `MINOR` | Nova funcionalidade ou nova entrega | `1.0.0` → `1.1.0` |
| `PATCH` | Correção (hotfix) | `1.1.0` → `1.1.1` |

---

## Referências

- [A successful Git branching model (GitFlow)](https://nvie.com/posts/a-successful-git-branching-model/)
- [Conventional Commits](https://www.conventionalcommits.org/pt-br/v1.0.0/)
- [Versionamento Semântico](https://semver.org/lang/pt-BR/)
