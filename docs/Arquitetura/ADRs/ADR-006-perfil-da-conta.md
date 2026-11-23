# ADR-006: Perfil da conta: publicador é o líder e receptor é o colaborador

- **Status:** Proposto
- **Data:** 2026-11-18
- **Quem decidiu:** Fernando (gerente de projetos), no PR de origem, para o MVP da disciplina
- **Origem:** [#13](https://github.com/morangotangos-team/feedberry/issues/13) (banco de dados), ponto 1 de "Pontos para decidir"; [#16](https://github.com/morangotangos-team/feedberry/issues/16) (integração do login), seção "Dependências"; [PR #30](https://github.com/morangotangos-team/feedberry/pull/30)
- **Relacionados:** [ADR-003](ADR-003-backend-flask-em-camadas.md), [ADR-007](ADR-007-orm-e-banco-de-dados.md) (o banco guarda o papel)

## Contexto

Dois trabalhos do projeto usam ideias diferentes de "perfil":

| Onde | Como o perfil aparece |
|------|------------------------|
| Login (#6, #9, PR #12) e homes (#15) | A **conta** tem um perfil: `publicador` ou `receptor`. O `POST /auth/login` exige o perfil e só aceita o login se ele for igual ao do cadastro (RN02 e RN03 do `login.md`). Cada perfil tem a sua home. |
| Modelo de domínio (#13) | **Publicador** e **receptor** são papéis **dentro de um feedback** (autor e destinatário). A conta tem `papel = COLABORADOR \| LIDER`. |

No modelo da #13, a mesma pessoa pode escrever um feedback e receber outro. No login atual, ela só consegue entrar em um dos dois perfis.

A #13 pedia para alinhar isso **antes** de migrar o repositório de usuários para o banco. A #16 avisa que, se o perfil da conta mudar, o campo de perfil da tela de login muda junto.

Neste momento da disciplina, o foco do grupo é a **tela de login**. Mais para frente, a ideia é criar um **canal de comunicação entre o líder e o gestor**, o que coloca o líder também no lado de quem recebe.

## Decisão

**No MVP, publicador é o líder e receptor é o colaborador.**

1. **Na conta:** o banco guarda o papel do domínio, `LIDER` ou `COLABORADOR` (ADR-007). Cada conta tem um papel só.
2. **No login:** a tela continua com as abas **Publicador** e **Receptor**, e o `POST /auth/login` continua pedindo o `perfil`. O perfil de cada conta vem do papel:

   | Papel da conta | Perfil no login | Home |
   |----------------|-----------------|------|
   | `LIDER` | `publicador` | Home do publicador |
   | `COLABORADOR` | `receptor` | Home do receptor |

   Essa tradução fica só no mapa `PERFIL_POR_PAPEL`, em `src/backend/repositories/usuario_repository.py`.
3. **Depois do login:** a pessoa vai para a home do perfil devolvido pela API. Entrar pela aba do outro perfil dá a mesma mensagem genérica de credenciais inválidas (RN03 e RN04 do `login.md`).

**Fora do MVP (registrado para o futuro, ainda sem decisão):** um canal de comunicação entre o líder e o gestor. Quando ele entrar, o líder passa a **publicar** para os colaboradores e a **receber** do gestor. Como isso vai funcionar ainda não foi decidido e deve ser registrado em um ADR novo.

## Consequências

- **Positivas:**
  - A tela de login, a API e as homes que já existem continuam iguais. O foco atual (tela de login) não é bloqueado.
  - O banco já usa os papéis do domínio (`LIDER`/`COLABORADOR`), então a mudança futura começa pelo mapa `PERFIL_POR_PAPEL` e pelo enum `Papel`, sem refazer as tabelas de feedback.
  - Para o usuário, a regra é simples: o líder entra como publicador e o colaborador como receptor.
- **Negativas:**
  - Cada pessoa entra em um perfil só. No MVP, o líder não recebe feedback pela home e o colaborador não publica.
  - Os requisitos de o colaborador enviar feedback ao líder (RF12 e RF13) não têm tela no MVP: o botão **Enviar feedback** está só na home do publicador (pendência 3 da matriz de rastreabilidade).
- **A observar** (para quando o canal líder ↔ gestor entrar):
  - O enum `Papel` deve ganhar um valor para o gestor, com uma migração nova.
  - O líder vai ter **dois** perfis. O `PERFIL_POR_PAPEL` deixa de ser um para um, e o login precisa definir como a pessoa escolhe o lado (as abas atuais, uma escolha depois de entrar ou outra forma).
  - A relação entre gestor e líder precisa ser modelada no banco, por exemplo de forma parecida com `equipe.lider_id`.
  - A tela de login e o `login.md` (RN02 e RN03) mudam junto.

## Alternativas consideradas

As opções que aparecem nas fontes são estas:

| Opção | Onde aparece | Situação |
|-------|--------------|----------|
| Perfil da conta `publicador` ou `receptor`, escolhido no login, vindo do papel `LIDER`/`COLABORADOR` | Login atual (#9, PR #12), homes (#15) e PR #30 | **Escolhida para o MVP** |
| Papel da conta `COLABORADOR` ou `LIDER`, com publicador e receptor só como papéis dentro de cada feedback (a mesma pessoa escreve e recebe) | Modelo de domínio da #13 | Adiada: volta à discussão com o canal líder ↔ gestor |
| Login sem a escolha de perfil, com a home definida só pelo papel da conta | README do banco (PR #30), como caminho possível | Não avaliada pelo grupo |

Não há registro de uma avaliação comparando as opções além do que está acima.
