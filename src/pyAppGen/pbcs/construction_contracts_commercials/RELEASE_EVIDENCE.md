# Release Evidence - Construction Contracts and Commercials

Package directory: `src/pyAppGen/pbcs/construction_contracts_commercials`

## What This Slice Proves

- Owned construction-commercial schema with domain-specific contract, pay application, retainage, variation, claim, waiver, subcontract, governance, and AppGen-X event tables.
- Executable package-local runtime that validates contract lifecycle transitions, schedule-of-values integrity, overclaim prevention, waiver-gated certification, notice timeliness, retainage blockers, and final-account readiness.
- Service, route, handler, UI, agent, RBAC, configuration, rules, parameters, and seed surfaces that remain inside the PBC-owned boundary.

## Behavioral Evidence

- Contract lifecycle:
  - Invalid direct transition to `closed` is rejected until the lifecycle progresses through allowed stages.
- Pay applications:
  - Overclaims against schedule-of-values balances are rejected.
  - Certification requires valid waiver evidence when the waiver gate is enabled.
- Variations and claims:
  - Unapproved variations do not increase contract value.
  - Late claims are classified as time-bar risks and surface in the workbench.
- Workbench:
  - Queues exist for pay apps awaiting certification, missing waivers, expiring guarantees, notice deadlines, disputed variations, active claims, retainage blockers, and final-account blockers.
- AppGen-X eventing:
  - Emitted/consumed contract is explicit.
  - Unknown events route to dead letter.
  - Handler idempotency is enforced.
- Agent governance:
  - Document-instruction plans require human confirmation and citations.
  - CRUD previews reject foreign tables.

## Release Simulation

The package-local release simulation covers:

1. Create contract `CCC-001` with schedule of values and expiring guarantee.
2. Intake pay application `APP-001`.
3. Register waiver `LW-001`.
4. Certify the pay application and create retainage hold.
5. Approve variation `VO-001`.
6. Register late commercial claim `CL-001`.
7. Generate workbench, cash-flow forecast, and contractor scorecard evidence.

## Verification Commands

- `pytest src/pyAppGen/pbcs/construction_contracts_commercials/tests/test_contract.py`
- `python -m compileall src/pyAppGen/pbcs/construction_contracts_commercials`
- Package-local smoke import/run via runtime, services, and routes entrypoints
