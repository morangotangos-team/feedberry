# Organização do repositório

Localização dos artefatos do FeedBerry no repositório `morangotangos-team/feedberry`. Cada documento tem a versão em PDF, com o mesmo nome, na mesma pasta.

## 1. Estrutura da pasta `docs`

```
docs/
├── README ............................. índice da documentação
├── Organizacao do repositorio ......... este documento
├── Processos_De_Requisitos/ ........... processo de levantamento de requisitos
├── Processos_De_Desenvolvimento/ ...... padrão de commit, GitFlow e documentação de funcionalidades
├── Funcionalidades/ ................... documentação de cada tela
└── Artefatos_Requisitos/
    ├── pesquisa-documental/ ........... LGPD e ISO/IEC 25010
    ├── entrevista/
    │   ├── Entrevista com Lider/ ...... transcrição e áudio
    │   └── Entrevista com o Colaborador/ ... transcrição
    ├── questionario/ .................. formulários e respostas
    ├── sintese/ ....................... síntese das entrevistas e dos questionários
    ├── bpmn/ .......................... BPMN do processo atual (.bpmn e imagem)
    ├── sistema-analogo/ ............... análise do sistema análogo (Aba+)
    ├── analise/ ....................... análise dos artefatos (atores e casos de uso)
    ├── diagramas/ ..................... diagramas de contexto e de casos de uso
    ├── Diagrama_Fluxograma_PaginaLogin/ ... fluxograma e casos de teste do login
    ├── requisitos/ .................... requisitos funcionais e não funcionais
    ├── rastreabilidade/ ............... matriz de rastreabilidade
    ├── prototipos/ .................... protótipos das telas
    ├── visao/ ......................... documento visão e casos de uso (Larman)
    └── revisao/ ....................... revisão cruzada dos artefatos
```

## 2. Onde está cada artefato

| Artefato | Caminho |
|----------|---------|
| Processo de levantamento de requisitos | `docs/Processos_De_Requisitos/` |
| Pesquisa documental (LGPD e ISO/IEC 25010) | `docs/Artefatos_Requisitos/pesquisa-documental/` |
| Transcrição da entrevista com o líder | `docs/Artefatos_Requisitos/entrevista/Entrevista com Lider/` |
| Transcrição da entrevista com o colaborador | `docs/Artefatos_Requisitos/entrevista/Entrevista com o Colaborador/` |
| Questionários e respostas | `docs/Artefatos_Requisitos/questionario/` |
| Síntese das entrevistas e dos questionários | `docs/Artefatos_Requisitos/sintese/` |
| BPMN do processo atual | `docs/Artefatos_Requisitos/bpmn/` |
| Análise do sistema análogo (Aba+) | `docs/Artefatos_Requisitos/sistema-analogo/` |
| Análise dos artefatos | `docs/Artefatos_Requisitos/analise/` |
| Diagramas de contexto e de casos de uso | `docs/Artefatos_Requisitos/diagramas/` |
| Fluxograma e casos de teste da página de login | `docs/Artefatos_Requisitos/Diagrama_Fluxograma_PaginaLogin/` |
| Requisitos funcionais e não funcionais | `docs/Artefatos_Requisitos/requisitos/` |
| Matriz de rastreabilidade | `docs/Artefatos_Requisitos/rastreabilidade/` |
| Protótipos | `docs/Artefatos_Requisitos/prototipos/` |
| Documento visão e casos de uso (Larman) | `docs/Artefatos_Requisitos/visao/` |
| Revisão cruzada | `docs/Artefatos_Requisitos/revisao/` |
| Documentação das telas | `docs/Funcionalidades/` |
| Padrão de commit e GitFlow | `docs/Processos_De_Desenvolvimento/` |

## 3. Versionamento

- Todo artefato entra por **pull request** para a `develop`, a partir de uma branch `<tipo>/<usuario>-<descricao>`, com pelo menos **uma aprovação** de outro integrante.
- Os commits seguem o padrão **Conventional Commits** (ex.: `docs(requisitos): ...`).
- O PDF de cada documento fica **ao lado** do original, com o mesmo nome, para impressão.

## 4. Pendências

| Pendência | Situação |
|-----------|----------|
| Transcrição do colaborador em `.docx` | Só na branch `feature/aime` |
