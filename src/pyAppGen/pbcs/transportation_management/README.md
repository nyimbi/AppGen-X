# transportation_management PBC

`transportation_management` is the standalone freight execution and transportation management packaged business capability. It owns shipment, carrier, route, tracking, ETA, delivery proof, exception, freight cost, policy, and AppGen-X event artifacts.

## Standalone Domain Coverage

- Configure PostgreSQL/MySQL/MariaDB-backed transportation boundaries and the fixed AppGen-X event topic.
- Register carriers with lanes, service levels, identity, cost, carbon, risk, and scorecard evidence.
- Create shipments, packages, references, parties, and mode/service constraints.
- Select carriers, tender loads, plan multi-stop routes, estimate cost/carbon, dispatch shipments, and ingest tracking events.
- Calculate ETA, confirm arrivals, confirm delivery, generate delivery proofs, and manage exceptions.
- Consume packed, purchase-order, return, transfer, and access-policy events into PBC-owned projections.
- Surface workbench forms, wizards, controls, repository read models, and agent skill integration for one-PBC operation.

## Executable Surfaces

- `runtime.py` contains side-effect-free TMS commands and advanced resilience/optimization/proof functions.
- `repository.py` backs shipment, carrier, route, tracking, and governance read models.
- `standalone.py` executes a complete shipment-to-delivery flow.
- `ui.py` exposes forms, wizards, controls, workbench cards, and standalone navigation.
- `seed_data.py` provides deterministic demo shipment, carrier, route, tracking, and governance data.
- `release_evidence.py` verifies runtime, repository, UI, agent, model, event, API, service, schema, and artifact evidence.
