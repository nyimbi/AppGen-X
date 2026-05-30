# Inventory Positioning

`inventory_positioning` is a standalone AppGen-X PBC for inventory truth and
positioning workflows. The package owns item and node master data, inventory
positions, receipts, adjustments, allocations, releases, quality holds,
replenishment signals, reconciliation evidence, AppGen-X inbox/outbox handling,
permissions, rules, parameters, UI workbench metadata, and assistant planning.

## Standalone Surface

- Stateful in-memory service: `services.InventoryPositioningService`
- Standalone one-PBC app shell: `standalone.InventoryPositioningStandaloneApp`
- External route surface: `/inventory/items`, `/inventory/nodes`,
  `/inventory/receipts`, `/inventory/adjustments`, `/inventory/availability`,
  `/inventory/allocations`, `/inventory/allocations/{id}/release`,
  `/inventory/quality-holds`, `/inventory/events/inbox`,
  `/inventory/workbench`
- AppGen-X event contract: fixed topic `appgen.inventory.events`
- Database evidence: owned schema + migration coverage from
  `migrations/001_initial.sql`

## Main Modules

- `runtime.py`: domain workflow engine and capability smoke logic
- `schema_contract.py`, `models.py`: owned schema, models, migration coverage
- `services.py`, `routes.py`, `standalone.py`: executable standalone service
  and route dispatch
- `ui.py`: workbench fragments, forms, wizards, controls, and workflow lanes
- `events.py`, `handlers.py`: AppGen-X eventing and idempotent handler
  contracts
- `config.py`, `permissions.py`, `seed_data.py`: governance, access, bootstrap
  seed data
- `agent.py`: document intake, CRUD planning, and chatbot contribution
- `release_evidence.py`, `capability_assurance.py`: release gate evidence

## Focused Verification

Run the focused package checks with:

```bash
PYTHONPATH=src python3 src/pyAppGen/pbcs/inventory_positioning/tests/run_focused.py
```

Compile-check the package with:

```bash
python3 -m compileall src/pyAppGen/pbcs/inventory_positioning
```
