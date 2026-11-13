# Home do publicador

Tela inicial de quem **escreve e envia** feedbacks. Issue #15 · somente front-end (dados de exemplo).

- **Página:** `src/frontend/publicador/home.html`
- **Arquivos:** `home.js`, `home.css`, `dados-mock.js` (na mesma pasta)
- **Teste:** `python -m http.server` dentro de `src/frontend/` e abrir `http://localhost:8000/publicador/home.html`

## O que a tela mostra

| Bloco | O que mostra | Caso de uso | Componente |
| --- | --- | --- | --- |
| Saudação + ação principal | "Olá, {nome}!" e o botão **Enviar feedback** | UC03, UC12 | `saudacao` |
| Resumo | Feedbacks enviados, pontos de melhoria em aberto e retornos agendados | UC04, UC06, UC07 | `card-resumo` |
| Enviados recentemente | Últimos 4 feedbacks enviados, com link "Ver todos" | UC10 | `secao`, `card-feedback` (modo `enviado`) |
| Próximos retornos | Lembretes e retornos agendados, por data, com botão **Agendar retorno** | UC06, UC14 | `secao`, `lista-lembretes` + botão (exclusivo do publicador) |
| Pontos de melhoria em acompanhamento | Pontos registrados nos feedbacks e o status de cada um | UC04, UC07 | `secao`, `card-meta-ponto` |

Quando uma lista está vazia, aparece o **estado vazio** com uma mensagem própria do bloco.

## Dados esperados (`dados-mock.js`)

| Export | Formato |
| --- | --- |
| `usuario` | `{ id, nome, papel }` |
| `feedbacksEnviados` | `[{ id, destinatario: { nome }, tipo, competencias[], mensagem, data, anonimo }]` — `tipo`: `elogio`, `construtivo` ou `ideia`; `data`: `AAAA-MM-DD` |
| `retornosAgendados` | `[{ id, titulo, subtitulo?, data }]` |
| `pontosMelhoria` | `[{ id, titulo, subtitulo?, status, prazo? }]` — `status`: `em-aberto`, `em-andamento`, `concluido` ou `atrasado` |

Para trocar pelo back-end, devolva os mesmos formatos e substitua o import em `home.js`.

## Regras da implementação

- `publicador/` importa só de `componentes/`, `utils/` e `estilos/`; nada de `receptor/`.
- Nenhum componente testa o perfil: o que muda entre as homes vai por parâmetro (`modo: 'enviado'`, itens do menu, textos).
- Cores e fontes vêm de `estilos/tokens.css`.
- Links de telas ainda inexistentes usam `href="#"` e mostram "Tela em construção".

## Comportamento

- Tema claro e escuro (botão no alto, escolha lembrada no navegador).
- Layout responsivo: no celular a navegação vira uma barra fixa na parte de baixo.
- **Sair** volta para `index.html` (sem encerrar sessão real).
- **Agendar retorno** mostra um aviso; o fluxo de agendamento (UC06) é de outra issue.

## Fora do escopo

Integração com back-end/API/banco (#13), redirecionamento do login para a home (#9), telas de enviar feedback, histórico completo, retornos e pontos de melhoria, e relatórios (UC07, UC08).
