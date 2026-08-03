# CLAUDE.md — AppGen-X

Open-source application-composition platform: turns models, DB introspection,
DSL, or natural language into a working application package — web screens,
APIs, data models, mobile & desktop starters, deployment assets, ERP
templates, agentic systems, release audits.

Positioning: **"Most generators stop at scaffolding; AppGen-X keeps going."**

*Inherits `~/.claude/CLAUDE.md` and `~/src/pjs/CLAUDE.md`. Additions below only.*

## Stack

- Python package + CLI (`appgen`), published on PyPI as `appgen-x`
- Frontend: `appgen-frontend/` (React)
- License: open source (see `LICENSE`); community contribution flow in `CONTRIBUTING.md`

## Commands

```bash
# install (dev)
pip install -e .

# CLI
appgen --help

# tests
pytest tests/ci -vxs

# lint
ruff check .
ruff format .
```

## Composition sources — five, all first-class

1. **Model** — Python/SQLAlchemy or Pydantic model → CRUD + REST + admin
2. **DB introspection** — point at a live PostgreSQL/MySQL schema → app skeleton
3. **DSL** — the `.apg`-family compact declarative spec (see sibling `apg`)
4. **Natural language** — English/Kiswahili prompt → app package
5. **Composition** — combine any of the above; conflicts resolve per policy

## Public tech spec

`https://llocal.com/appgen-x/` (behind passcode). Tech-spec-only (no sales kit
— open-source products don't need one). Cited from `github.com/nyimbi/AppGen-X`
and PyPI. See [[project_kits_playbook]].

## Sibling projects

- `~/src/pjs/apg` — the DSL half; AppGen-X consumes `.apg` specs as one composition source
- `~/src/pjs/fab-ext/pgappforge` (Fabext) — the ERP-module catalog AppGen-X ships as templates

## Gotchas

- Release audits are a shipping feature, not a nice-to-have — every generator run writes evidence to a per-build audit dir. Do NOT skip when adding new templates.
- The natural-language source path uses LiteLLM at `62.169.25.77:4000`; treat cloud unavailability as a soft failure (fall back to DSL / model sources).
