# CDP Segmentation

`cdp_segmentation` is a package-local executable PBC slice for customer data platform segmentation inside AppGen-X. The slice focuses on ingesting customer events, stitching profile attributes and consent state, defining segments, evaluating real-time membership, planning activations, and exposing analyst-facing workbench, governance, and release evidence surfaces without crossing package boundaries.

## Implemented Execution Surface

- Runtime configuration enforcing AppGen-X topic and allowed database backends
- Consent-aware customer event ingestion into governed profiles and properties
- Segment definition, membership scoring, transition ledger recording, and activation evidence
- Audience simulation, forecasting, lifecycle risk scoring, merge healing, consent screening, and anomaly detection
- Explicit-state service and route execution for package-local command/query flows
- Idempotent AppGen-X inbox handlers with dead-letter metadata
- Workbench UI contract with CDP forms, wizards, controls, and alert summaries
- Agent/chatbot guidance for document-instruction planning and governed CRUD selection
- Release readiness evidence spanning schema, service, API, permissions, UI, handlers, docs, and tests

## Guardrails

- Event contract: `AppGen-X`
- Required topic: `appgen.cdp_segmentation.events`
- Shared table access: disabled
- Runtime tables: `cdp_segmentation_appgen_outbox_event`, `cdp_segmentation_appgen_inbox_event`, `cdp_segmentation_dead_letter_event`
- Execution stays inside owned tables plus declared event/projection dependencies

## Key Files

- `runtime.py` — executable CDP behavior and release-time proofs
- `services.py` — plan mode plus explicit-state execution mode
- `routes.py` — API route contracts and dispatch
- `handlers.py` — idempotent AppGen-X inbox handlers
- `ui.py` — workbench, forms, wizards, and controls
- `agent.py` — document-instruction and governed CRUD guidance
- `release_evidence.py` — package-local readiness aggregation
- `tests/` — contract and execution-focused regression coverage
