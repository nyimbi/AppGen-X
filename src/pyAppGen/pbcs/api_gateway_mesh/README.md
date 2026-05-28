# API Gateway Mesh

`api_gateway_mesh` is the executable PBC for platform ingress and service-mesh control inside AppGen. The slice keeps all eventing on AppGen-X and owns its gateway registry, route publication, safety evidence, rate limiting, health/traffic telemetry, retry/dead-letter evidence, and release-gate projections.

## Implemented Execution Surface

- Runtime configuration with backend and AppGen-X contract enforcement
- Service registration, mTLS identity registration, route publication, rate limiting, health capture, and traffic sampling
- Deterministic route collision analysis for host/path/method/protocol overlap
- Route publication safety-case generation with rule, identity, service, collision, rollback, and event-contract checks
- Service/route facade execution when explicit runtime state is supplied
- Gateway incident triage and workbench rendering
- Release evidence with schema, service, API, permissions, UI, events, agent, and documentation sections

## Guardrails

- Event contract: `AppGen-X`
- Required topic: `appgen.gateway.events`
- Shared table access: disabled
- Dead-letter table: `api_gateway_mesh_dead_letter_event`
- Runtime/event/service/query surfaces stay inside owned tables plus declared dependency APIs/projections

## Key Files

- `runtime.py` — executable gateway behavior and release-time proofs
- `services.py` — service facade with plan mode and explicit-state execution mode
- `routes.py` — API route contracts and dispatch
- `ui.py` — workbench, safety-case, and incident-triage UI contract
- `agent.py` — readiness preview and incident-triage assistant surface
- `release_evidence.py` — release readiness aggregation
