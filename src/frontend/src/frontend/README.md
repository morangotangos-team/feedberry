# FeedBerry · front-end

Só HTML, CSS e JavaScript (módulos ES). Sem back-end, sem API.

## Como testar

Módulos ES não funcionam abrindo o HTML direto do disco (`file://`). Dentro de `src/frontend/`:

```bash
python -m http.server
```

| Tela | Endereço |
| --- | --- |
| Login (publicador e receptor) | http://localhost:8000/ — abre direto no receptor com `/#receptor` |
| Home do publicador | http://localhost:8000/publicador/home.html |
| Home do receptor | http://localhost:8000/receptor/home.html |

O login ainda **não** leva para a home (depende da autenticação real: issues #9 e #16).

## Estrutura

```
src/frontend/
├── index.html            login (issue #6)
├── login/                login.css, login.js
├── estilos/              tokens.css (cores, fontes, temas) e base.css
├── componentes/          partes compartilhadas (veja componentes/README.md)
├── utils/                escapar-html, datas, plural, tema
├── publicador/           home.html, home.css, home.js, dados-mock.js
└── receptor/             home.html, home.css, home.js, dados-mock.js
```

## Para quem vai fazer o back-end

- O formato dos dados esperado está documentado em `publicador/dados-mock.js` e `receptor/dados-mock.js`. Se a API devolver o mesmo formato, as telas não mudam.
- Pontos de integração estão marcados com `TODO(...)` no código (`login/login.js`, `layout-home.js`, `receptor/home.js`, `publicador/home.js`).
- Feedback anônimo: a API **não deve enviar o autor**; o front só mostra "Anônimo".
