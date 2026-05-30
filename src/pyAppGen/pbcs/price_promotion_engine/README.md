# Price Promotion Engine PBC

This package is a standalone AppGen-X Packaged Business Capability for pricing, promotion, coupon, quote, campaign budget, accrual, settlement, and pricing decision governance.

Deployment database backends remain limited to PostgreSQL, MySQL, and MariaDB. The package-local SQLite repository is only a deterministic local harness for tests and demos.

## Standalone application surface

- `repository.py` persists runtime state, form submissions, workflow runs, controls, agent sessions, and a workbench read model.
- `standalone.py` bootstraps a one-PBC application and release snapshot.
- `services.py` and `routes.py` expose app-local pricing setup, quote, coupon redemption, settlement, and workbench operations.
- `ui.py` defines forms, wizards, controls, and renderable workbench cards.
- `agent.py` contributes pricing skills, document intake, governed CRUD planning, wizard matching, and route candidates to the composed assistant.

Focused verification:

```bash
PYTHONPATH=src python3 -m py_compile src/pyAppGen/pbcs/price_promotion_engine/*.py src/pyAppGen/pbcs/price_promotion_engine/tests/*.py
PYTHONPATH=src ./.venv/bin/pytest -q src/pyAppGen/pbcs/price_promotion_engine/tests
```
