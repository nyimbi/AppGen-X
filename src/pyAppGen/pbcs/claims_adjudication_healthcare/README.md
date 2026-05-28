# Claims Adjudication Healthcare

This package is a self-contained AppGen-X PBC slice for healthcare payer claims adjudication. It implements package-local claim intake, line adjudication, coding review, denial and appeal workflows, payment-integrity triage, AppGen-X outbox/inbox/dead-letter behavior, governed rules and runtime parameters, workbench UI metadata, and agent/document-instruction CRUD previews.

## Executable Slice

- `runtime.py` contains the in-memory domain runtime and release/schema/service contracts.
- `services.py` exposes a stateful service layer over the runtime.
- `routes.py` maps package-local HTTP routes to service operations.
- `ui.py` defines the workbench, forms, wizards, and controls for operators.
- `agent.py` provides chatbot/document-instruction planning and governed CRUD previews.
- `config.py`, `permissions.py`, and `seed_data.py` define governance for rules, parameters, RBAC, and seed artifacts.

## Core Behavior

- Claim intake canonicalizes required member, provider, plan, source, and projection evidence.
- Duplicate replay is blocked by canonical claim identity unless the submission is a correction.
- Claim lines adjudicate against approved benefit rules with line-level allowed amount, member cost share, payer responsibility, and pend/deny reasons.
- High-unit or suspicious lines open coding reviews; high-dollar lines open payment-integrity cases.
- Denials and appeals are executable package-local workflows, including appeal overturn handling.
- Consumed events are idempotent and unknown events land in the owned dead-letter table.
- Agent document instructions are parsed into owned-table CRUD previews with confirmation requirements.

## Validation

- `python3 -m compileall src/pyAppGen/pbcs/claims_adjudication_healthcare`
- `./.venv/bin/pytest src/pyAppGen/pbcs/claims_adjudication_healthcare/tests/test_contract.py src/pyAppGen/pbcs/claims_adjudication_healthcare/tests/test_executable_slice.py tests/test_pbc_claims_adjudication_healthcare_runtime.py`

## Limits

This is an executable reference slice, not a production persistence layer. It models owned tables and workflows in memory so the PBC can function coherently in isolation without editing shared AppGen-X infrastructure.
