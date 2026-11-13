# Home do receptor

Tela inicial de quem **recebe** feedbacks. Issue #15 · somente front-end (dados de exemplo).

- **Página:** `src/frontend/receptor/home.html`
- **Arquivos:** `home.js`, `home.css`, `dados-mock.js` (na mesma pasta)
- **Teste:** `python -m http.server` dentro de `src/frontend/` e abrir `http://localhost:8000/receptor/home.html`

## O que a tela mostra

| Bloco | O que mostra | Caso de uso | Componente |
| --- | --- | --- | --- |
| Saudação | "Olá, {nome}!" e o atalho **Ver histórico** | UC10 | `saudacao` |
| Resumo | Feedbacks recebidos, metas em andamento e pontos de melhoria em aberto | UC09, UC11 | `card-resumo` |
| Recebidos recentemente | Últimos 4 feedbacks recebidos, com link "Ver todos" e botão **Agradecer** | UC09 | `secao`, `card-feedback` (modo `recebido`) |
| Minhas metas | Metas de desenvolvimento com status e prazo | UC05, UC11 | `secao`, `card-meta-ponto` |
| Lembretes | Lembretes dos pontos combinados, por data | UC14 | `secao`, `lista-lembretes` |

**Feedback anônimo (UC13):** o card mostra "Anônimo", com avatar neutro, sem nome nem avatar do autor. O front não lê o autor quando `anonimo` é verdadeiro.

Quando uma lista está vazia, aparece o **estado vazio** com uma mensagem própria do bloco.

## Dados esperados (`dados-mock.js`)

| Export | Formato |
| --- | --- |
| `usuario` | `{ id, nome, papel }` |
| `feedbacksRecebidos` | `[{ id, autor: { nome } \| null, tipo, competencias[], mensagem, data, anonimo, agradecido }]` — para anônimo: `anonimo: true` e `autor: null` (a API não deve enviar o autor) |
| `metas` | `[{ id, titulo, status, prazo }]` — `status`: `em-aberto`, `em-andamento`, `concluido` ou `atrasado` |
| `pontosMelhoria` | `[{ id, titulo, status }]` (só a quantidade em aberto aparece, no resumo) |
| `lembretes` | `[{ id, titulo, subtitulo?, data }]` |

O mock inclui um feedback anônimo. Para trocar pelo back-end, devolva os mesmos formatos e substitua o import em `home.js`.

## Regras da implementação

- `receptor/` importa só de `componentes/`, `utils/` e `estilos/`; nada de `publicador/`.
- Nenhum componente testa o perfil: o que muda entre as homes vai por parâmetro (`modo: 'recebido'`, itens do menu, textos).
- Cores e fontes vêm de `estilos/tokens.css`.
- Links de telas ainda inexistentes usam `href="#"` e mostram "Tela em construção".

## Comportamento

- Tema claro e escuro (botão no alto, escolha lembrada no navegador).
- Layout responsivo: no celular a navegação vira uma barra fixa na parte de baixo.
- **Agradecer** marca o feedback como "Agradecido ✓" na tela (sem gravar em lugar nenhum; o registro real depende do back-end).
- **Sair** volta para `index.html` (sem encerrar sessão real).

## Fora do escopo

Integração com back-end/API/banco (#13), redirecionamento do login para a home (#9), telas de histórico completo, metas e lembretes, e relatórios (UC07, UC08).
