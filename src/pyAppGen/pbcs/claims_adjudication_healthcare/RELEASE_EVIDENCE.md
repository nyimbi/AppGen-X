# Release Evidence - Healthcare Claims Adjudication

Package directory: `src/pyAppGen/pbcs/claims_adjudication_healthcare`

## Release Scope

This release turns the PBC into a coherent, executable one-PBC healthcare claims adjudication slice with:

- owned models and migration DDL
- executable runtime/services/routes
- AppGen-X event envelopes, inbox handlers, and dead-letter behavior
- workbench/forms/wizards/controls metadata
- RBAC, rules, runtime parameters, and seed artifacts
- agent/chatbot document-instruction CRUD planning
- focused package-local tests

## Evidence Collected

- Import/syntax validation:
  - `python3 -m compileall src/pyAppGen/pbcs/claims_adjudication_healthcare`
  - Result: passed
- Focused test execution:
  - `./.venv/bin/pytest src/pyAppGen/pbcs/claims_adjudication_healthcare/tests/test_contract.py src/pyAppGen/pbcs/claims_adjudication_healthcare/tests/test_executable_slice.py tests/test_pbc_claims_adjudication_healthcare_runtime.py`
  - Result: `13 passed in 0.51s`

## Functional Evidence

- Claim intake validates required identifiers and prevents duplicate replay unless the request is a correction.
- Line adjudication uses approved benefit rules to compute allowed amount, member responsibility, payer responsibility, and pend/deny reasons.
- High-unit or suspicious lines create coding reviews; material-dollar lines create payment-integrity cases.
- Manual denials and appeal overturns update claim state inside the package-local runtime.
- Consumed AppGen-X events are idempotent and invalid event types are written to the owned dead-letter surface.
- Document instructions are parsed into governed CRUD previews against owned tables only.

## Boundary Evidence

- All owned business and event tables begin with `claims_adjudication_healthcare_`.
- No route, service, or datastore plan writes foreign tables.
- Cross-PBC collaboration remains event/API based.

## Remaining Risks

- The runtime is intentionally in-memory, so this slice demonstrates package-local behavior rather than durable production storage.
- Projection freshness logic depends on supplied payload evidence rather than live external projections.
