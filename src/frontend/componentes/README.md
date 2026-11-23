# Componentes compartilhados

Partes da interface que são **iguais nas duas homes** (publicador e receptor) ou no login.
Cada componente fica em uma pasta própria com:

- `<nome>.js` — função que **recebe os dados e devolve uma string HTML**;
- `<nome>.css` — estilos do componente (cores e fontes vêm de `estilos/tokens.css`).

O CSS de todos os componentes é reunido em `componentes.css`, que as homes carregam.
Ao criar um componente novo, adicione o `.css` dele ali.

## Regras

1. **Igual nos dois perfis → componente.** Não copie um bloco para `publicador/` e `receptor/`.
2. **O que muda vai por parâmetro**, por exemplo `cardFeedback(f, { modo: 'recebido' })`.
   O componente **nunca** testa o perfil (`if (perfil === 'receptor')`).
3. **Exclusivo de um perfil → fica na pasta dele** (ex.: "Próximos retornos", com o botão de agendar, está em `publicador/`).
4. **Texto vindo dos dados sempre passa por `escaparHtml`** (`utils/escapar-html.js`). Os parâmetros `conteudo` aceitam apenas HTML que já saiu de outro componente.
5. `publicador/` e `receptor/` só importam de `componentes/`, `estilos/` e `utils/`. Nunca um do outro.
6. Ações do usuário são marcadas com `data-acao="..."` (e `data-id`); quem usa o componente trata o clique.

## Lista

| Componente | O que é | Função principal |
| --- | --- | --- |
| `cabecalho` | Logo, nome do usuário, botões de tema e Sair | `cabecalho({ usuario, href })`, `barraAcoes()`, `marca({ href })`, `ativarCabecalho(raiz, { aoSair })` |
| `menu` | Navegação (itens por parâmetro; barra fixa no celular) | `menu(itens, { atual })` |
| `layout-home` | Estrutura das homes: lateral + conteúdo, tema, Sair e links "em construção" | `layoutHome(...)`, `atualizarConteudo(raiz, html)`, `ativarLayoutHome(raiz, { urlLogin })` |
| `saudacao` | "Olá, {nome}!", texto, botões e morango com sementes | `saudacao({ nome, texto, acoes, sementes })` |
| `secao` | Título de bloco com link opcional ("Ver todos") | `secao({ titulo, link, conteudo })` |
| `card-resumo` | Número grande + rótulo; faixa de resumo | `cardResumo({ valor, rotulo })`, `blocoResumo(itens)` |
| `card-feedback` | Card de feedback, modo enviado ou recebido (anônimo mostra "Anônimo") | `cardFeedback(f, { modo })`, `listaFeedbacks(lista, { modo, limite, vazio })` |
| `card-meta-ponto` | Item com título, status e prazo (metas e pontos de melhoria) | `cardMetaPonto(item)`, `listaMetasPontos(itens, { vazio })` |
| `lista-lembretes` | Lembretes por data | `listaLembretes(itens, { vazio })` |
| `estado-vazio` | Mensagem quando a lista não tem itens | `estadoVazio({ titulo, texto, acao })` |
| `avatar` | Círculo com a inicial (cor definida pelo nome; sem nome = neutro com "?") | `avatar({ nome, tamanho })` |
| `berry` | Logo e morango com sementes | `berrySprite()`, `logoBerry()`, `berry(sementes, { classe })` |
| `toast` | Aviso rápido no rodapé | `mostrarToast(texto)` |

Os componentes `layout-home`, `saudacao`, `secao`, `avatar`, `berry` e `toast` não estavam na lista da issue #15: foram criados para que nada de igual fique duplicado entre as duas homes.

## Parâmetros e exemplos

### `cardFeedback(feedback, { modo })`

```js
import { cardFeedback } from '../componentes/card-feedback/card-feedback.js';

cardFeedback({
  id: 2,
  autor: null,                      // anônimo: a API não deve enviar o autor
  destinatario: { nome: 'Paula' },
  tipo: 'ideia',                    // 'elogio' | 'construtivo' | 'ideia'
  competencias: ['Colaboração'],
  mensagem: 'Que tal fazer uma demonstração do protótipo?',
  data: '2026-11-10',               // 'AAAA-MM-DD' ou data e hora
  anonimo: true,
  agradecido: false,                // só no modo 'recebido'
}, { modo: 'recebido' });           // 'enviado' | 'recebido'
```

- `modo: 'enviado'` → "Para {destinatário}" (e "enviado como anônimo" se `anonimo`).
- `modo: 'recebido'` → "De {autor}" e botão **Agradecer** (`data-acao="agradecer"`, `data-id`). Se `anonimo`, mostra **"Anônimo"** com avatar neutro e **não lê** o autor.
- `listaFeedbacks` ordena do mais novo para o mais antigo e mostra 4 por padrão (`limite: null` mostra todos).

### `cardMetaPonto({ titulo, status, prazo, subtitulo })`

`status`: `'em-aberto' | 'em-andamento' | 'concluido' | 'atrasado'`. `prazo` e `subtitulo` são opcionais.

### `listaLembretes(itens)`

Cada item: `{ id, titulo, subtitulo?, data: 'AAAA-MM-DD' }`. Mostra a data em um selo e "em 2 dias".

### `menu(itens, { atual })`

```js
menu([
  { id: 'painel', rotulo: 'Painel', icone: '🏡', href: 'home.html' },
  { id: 'enviar', rotulo: 'Enviar', icone: '✍️', href: '#' },   // '#' = tela ainda não existe
], { atual: 'painel' });
```

Links com `href="#"` mostram o aviso "Tela em construção" (tratado pelo `layout-home`). Troque pelo caminho real quando a tela existir.

### `estadoVazio({ titulo, texto, acao })`

`acao` é opcional: `{ texto, href }` mostra um botão. Os componentes de lista já chamam o estado vazio sozinhos; passe a mensagem em `vazio`.

### `saudacao`, `secao`, `cardResumo`

```js
saudacao({ nome: 'Fernando', texto: '...', acoes: [{ texto: 'Enviar feedback', href: '#' }], sementes: 5 });
secao({ titulo: 'Enviados recentemente', link: { texto: 'Ver todos', href: '#' }, conteudo: listaFeedbacks(...) });
blocoResumo([{ valor: 5, rotulo: 'enviados' }, { valor: 3, rotulo: 'retornos agendados' }]);
```

## Como montar uma home

```js
raiz.innerHTML = layoutHome({ usuario, itensMenu, paginaAtual: 'painel' });
atualizarConteudo(raiz, montarConteudo());   // seus blocos, feitos com os componentes
ativarLayoutHome(raiz);                      // tema, Sair e links "em construção"
```

Veja `publicador/home.js` e `receptor/home.js`.

## Utilitários (`utils/`)

| Arquivo | Para quê |
| --- | --- |
| `escapar-html.js` | `escaparHtml(texto)` evita injeção de HTML |
| `datas.js` | `tempoRelativo` ("há 2 dias"), `formatarData` ("12/11/2026"), `partesDoDia`, `dataRelativa` (só para mocks) |
| `plural.js` | `plural(n, 'feedback', 'feedbacks')` |
| `tema.js` | alternar tema claro/escuro e lembrar a escolha |
| `tema-inicial.js` | script comum, no `<head>`, que aplica o tema antes da página aparecer |
