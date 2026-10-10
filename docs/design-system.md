# Design system

One token source and one component kit, consumed by both the generated apps and
the Studio. The point is that a colour or a button cannot mean two things in two
places, so a composed application looks like one product rather than a pile of
screens.

## Tokens

`src/pyAppGen/design/tokens.json` is the canonical definition. Everything else
reads it:

- `pyAppGen.design_tokens` loads it in Python. `_theme_css_text` in `gen.py`
  builds the generated app's stylesheet from it, so the Python contract and the
  CSS cannot disagree.
- `pyAppGen.design_tokens_export` renders `appgen-frontend/src/tokens.css` for
  the Studio.
- The component kit's stylesheet reads only `var(--appgen-*)`. It carries no
  literal colour, which a test enforces.

A repository checkout finds the file at the project root, which is a symlink to
the packaged copy. `python -m pyAppGen.design_tokens_export` regenerates the
Studio stylesheet after a token change; a test fails if it drifts.

Token groups:

| Group | Emitted as | Notes |
|-------|-----------|-------|
| `palette` | `--appgen-primary`, `--appgen-accent`, `--appgen-surface`, `--appgen-text`, `--appgen-muted` | Per theme: `appgen`, `sage`, `indigo`, `slate`. An unknown theme falls back to `appgen`. |
| `focus_ring` | `--appgen-focus-ring` | Built from the theme's primary as `0 0 0 {spread}px rgba(r, g, b, {alpha})`, with a literal fallback when the primary is not a six-digit hex. |
| `radius`, `space`, `shadow` | `--appgen-radius-*`, `--appgen-space-*`, `--appgen-shadow-*` | |
| `surface_detail` | `--appgen-border`, `--appgen-elevated` | Theme-independent neutrals for card edges and raised surfaces. |
| `state` | `--appgen-state-*` | `hover`, `selected`, `invalid`, `success`, `warning`, `scrim`. |
| `typography` | `--appgen-font-body`, `--appgen-font-size-*`, `--appgen-line-height` | |
| `content`, `density`, `touch_target` | `--appgen-content-max`, `--appgen-density-row`, `--appgen-touch-target` | |

Keys beginning with `$` are prose for whoever opens the JSON. They are
documentation, not tokens, and the emitter skips them, so a `$comment` never
becomes a CSS variable.

## Component kit

`src/pyAppGen/ui_kit/src/` holds the kit. One source, two consumers:

- The Studio aliases it in `appgen-frontend/vite.config.ts` and includes it in
  `tsconfig.json`, so the Studio type-checks and bundles the canonical copy.
- `pyAppGen.gen.write_ui_kit` copies it into every generated app at
  `app/ui_kit/`. The generated SPA resolves it through a sibling path, so both
  consumers render the same markup.

Components: `Button`, `Input`, `Select`, `Field`, `Card`, `Table`, `Badge`,
`Tabs`, `Dialog`, `Toast`, `Tooltip`, `EmptyState`, and the shell primitives
`AppShell`, `NavRail`, `PageHeader`, `WorkbenchLayout`.

Conventions the kit holds to:

- Every component takes `className` and appends it last, so a caller's utility
  class wins without `!important`.
- Interactive controls meet `--appgen-touch-target` and show the focus ring on
  `:focus-visible`.
- `Field` wires `aria-describedby` and the invalid state, so a control inside it
  needs no knowledge of its own validation.
- `Table` requires a `caption`; a table without an accessible name is announced
  as an unlabelled grid.
- `Dialog` uses the native `<dialog>` element, which supplies the top layer, the
  backdrop, and Escape-to-close without a focus-trap library. Focus moves in on
  open, stays inside while open, and returns to the opener on close.
- `useToast` throws outside a `ToastProvider`, so a missing provider fails at
  the call site rather than in a dead queue.

The kit is presentation only. It carries no data fetching, no routing, and no
application state, which is what lets the Studio and a generated app share it
without sharing an architecture.

## Generated SPA

A generated app ships a Vite + React + TypeScript frontend at its project root,
built from `src/pyAppGen/spa_templates/`:

```bash
npm install
npm run build   # tsc && vite build, writing dist/ for Flask to serve
```

`src/appgen.generated.ts` is the only generated file in the tree. It carries
`TABLES` from the app's schema and `WORKBENCHES` from the same composition plan
the Flask views are built from, so the shell cannot offer a screen the backend
does not serve. `src/api.ts` is the typed client and reads every route from that
module, which is why a hardcoded route fails the gate.

`Workbench.tsx` renders a PBC workbench from the payload the backend returns:
the package's owned tables, its command and query routes, its outbox and
dead-letter tables. A workbench that shows a placeholder instead of its own
contract is the defect that component exists to avoid.

The SPA is additive. The Flask cockpit templates remain until the SPA covers
them.

## Tests

- `tests/ci/test_design_tokens.py` — the token file is reachable, every theme is
  complete, an unknown theme falls back, the focus ring is derived, no `$` key
  reaches CSS, and the Studio stylesheet is in sync with the source.
- `tests/ci/test_ui_kit.py` — the barrel and the files agree, the stylesheet
  carries no literal colour, and the kit copies into a generated app intact.
- `tests/ci/test_generated_spa.py` — a generated app's SPA tree is emitted, it
  resolves the shared kit, its contract lists the composition's workbenches and
  the served table routes, its client hardcodes nothing, and the tree type-checks
  and builds with the real toolchain.

Every gate was canaried: the colour check fails when a literal hex is added to
the stylesheet, the sync check fails when the Studio stylesheet is edited by
hand, and the SPA gate fails when a route is hardcoded into the client.
