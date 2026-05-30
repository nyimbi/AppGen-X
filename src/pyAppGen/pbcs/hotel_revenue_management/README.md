# Hotel Revenue Management

`hotel_revenue_management` is a standalone AppGen-X PBC for hotel room revenue
control. It owns sellable room-type inventory, rate-plan inheritance and BAR
fences, channel allotments and stop-sells, segmented demand forecasts,
overbooking guardrails, yield explanations, revenue snapshots, governance
rules, bounded parameters, governed models, and its AppGen-X event runtime
state.

## What The Package Provides

- Package-owned schema, models, migration evidence, and boundary validation.
- Executable runtime commands for inventory, pricing, distribution, forecast,
  overbooking, yield, snapshot, governance, and governed-model flows.
- A standalone one-PBC application composition in [standalone.py](./standalone.py).
- A workbench UI contract with forms, wizards, controls, queues, and release
  evidence panels.
- Agent/chatbot/document/CRUD planning surfaces for the composed application
  assistant.
- Dynamic release evidence that reads local contracts, smoke results,
  documentation, and focused tests.

## Standalone Flow

1. Bootstrap configuration, parameters, and rule evidence from the package seed
   bundle.
2. Register room types, rate plans, and channel inventory for controlled sellable
   availability.
3. Approve segmented forecasts, simulate overbooking limits, and create yield
   decisions with explanation trails.
4. Record revenue snapshots, publish readiness evidence, and expose the full
   workbench and assistant contract as a one-PBC app.

## Key Files

- [runtime.py](./runtime.py) — executable runtime, records, calculations, and
  release-facing contracts
- [standalone.py](./standalone.py) — standalone one-PBC app composition
- [ui.py](./ui.py) — workbench forms, wizards, controls, and render contract
- [seed_data.py](./seed_data.py) — deterministic standalone bootstrap bundle
- [release_evidence.py](./release_evidence.py) — dynamic release readiness proof
- [tests/test_contract.py](./tests/test_contract.py) — focused contract and
  runtime tests
- [tests/test_standalone.py](./tests/test_standalone.py) — standalone app and
  workflow validation
