# __APP_NAME__ frontend

The single-page app for a generated AppGen application. It is a Vite + React +
TypeScript build served as static files by the Flask app next to it.

```bash
npm install
npm run dev     # proxies /api and /static to http://127.0.0.1:5000
npm run build   # writes dist/, which the Flask app serves
```

## What is generated and what is not

`src/appgen.generated.ts` is written by the generator from the app's own schema
and composition plan. It carries the table list and the PBC workbenches, and it
is the reason the shell cannot offer a screen the backend does not serve.

Everything else in `src/` is the shell: `App.tsx` renders the navigation and
the selected screen, `Workbench.tsx` renders a PBC workbench from the payload
the backend returns, and `api.ts` is the typed client.

`ui_kit/` is a copy of the shared component kit, emitted by the generator. The
Studio consumes the same source, so a button means the same thing in both. Do
not edit it here; change the kit and regenerate.

## Styling

The palette comes from `static/appgen-theme.css`, which the Flask app serves and
`index.html` links. The component kit reads only `--appgen-*` variables, so
changing the app's theme is a token change and nothing else.
