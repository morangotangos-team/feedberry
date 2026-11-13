# ADR-006: Perfil da conta: publicador/receptor ou colaborador/líder

- **Status:** Em aberto
- **Data:** 2026-11-12
- **Quem decidiu:** a confirmar (decisão ainda não tomada)
- **Origem:** [#13](https://github.com/morangotangos-team/feedberry/issues/13) (banco de dados), ponto 1 de "Pontos para decidir"; [#16](https://github.com/morangotangos-team/feedberry/issues/16) (integração do login), seção "Dependências"
- **Relacionados:** [ADR-003](ADR-003-backend-flask-em-camadas.md)

## Contexto

Dois trabalhos do projeto usam ideias diferentes de "perfil":

| Onde | Como o perfil aparece |
|------|------------------------|
| Login (#6, #9, PR #12) e homes (#15) | A **conta** tem um perfil: `publicador` ou `receptor`. O `POST /auth/login` exige o perfil e só aceita o login se ele for igual ao do cadastro (RN02 e RN03 do `login.md` do PR #12). Cada perfil tem a sua home. |
| Modelo de domínio (#13) | **Publicador** e **receptor** são papéis **dentro de um feedback** (autor e destinatário). A conta tem `papel = COLABORADOR \| LIDER`, e o líder também é colaborador. |

No modelo da #13, a mesma pessoa pode escrever um feedback e receber outro. No login atual, ela só consegue entrar em um dos dois perfis.

A #13 pede para alinhar isso com quem está na #9 **antes** de migrar o repositório de usuários para o banco. A #16 avisa que, se o perfil da conta mudar, o campo de perfil da tela de login muda junto.

## Decisão

**Ainda não decidido.** A discussão acontece na [#13](https://github.com/morangotangos-team/feedberry/issues/13), e este ADR será atualizado com a decisão e o status **Proposto** ou **Aceito** quando ela for tomada.

O que precisa ser decidido:

1. Qual é o perfil guardado na **conta**: `publicador`/`receptor`, `COLABORADOR`/`LIDER` ou outro.
2. Se o login continua pedindo o perfil e, se sim, qual.
3. Como a pessoa chega à home certa depois do login.

## Consequências

Enquanto a decisão estiver em aberto:

- A migração do `UsuarioRepository` para o banco (#13) fica bloqueada neste ponto.
- A integração do login (#16) segue com `perfil = publicador | receptor`, sabendo que pode mudar.
- Os componentes das homes não são afetados, porque não testam o perfil ([ADR-002](ADR-002-componentes-compartilhados.md)). As telas e o roteamento depois do login podem ser.

As consequências da decisão serão registradas quando ela for tomada.

## Alternativas consideradas

As opções que aparecem nas fontes são as duas formas de perfil descritas no Contexto:

| Opção | Onde aparece |
|-------|--------------|
| Perfil da conta `publicador` ou `receptor`, escolhido no login | Login atual (#9, PR #12) e homes (#15) |
| Papel da conta `COLABORADOR` ou `LIDER`; publicador e receptor como papéis dentro de cada feedback | Modelo de domínio da #13 |

Não há registro de uma avaliação comparando as duas opções, nem de outras opções.
