# Enterprise Asset Management Release Evidence

Directory: `src/pyAppGen/pbcs/eam`

## Evidence Areas

- Owned schema, models, and migration descriptors remain package-local to EAM.
- Runtime configuration locks allowed database backends and the AppGen-X event topic/contract.
- Services and routes expose standalone EAM commands and queries without shared-table access.
- Event contracts, handlers, retry policy, inbox/outbox/dead-letter tables, and idempotency keys are package-local.
- UI fragments cover workbench, forms, wizards, cockpit views, controls, event reliability, release evidence, and agent/document workflows.
- Permissions, rules, parameters, and seed descriptors are EAM-specific.
- Agent/chatbot/document/CRUD planning stays within owned tables and mutation-preview controls.
- Focused tests prove cross-module consistency and a package-local maintenance lifecycle.

## Executable Sources

- `runtime.py`
- `schema_contract.py`
- `models.py`
- `services.py`
- `routes.py`
- `events.py`
- `handlers.py`
- `config.py`
- `permissions.py`
- `seed_data.py`
- `ui.py`
- `agent.py`
- `release_evidence.py`
- `tests/test_contract.py`
