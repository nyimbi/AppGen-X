# Implementation Plan

## Goal

Ship `ap_automation` as a standalone AppGen-X PBC that is usable on its own with database-backed forms, guided workflows, controls, AI assistant skills, release evidence, and focused tests, without touching any path outside this package.

## Delivered workstreams

1. Runtime domain slice
   Vendor readiness, invoice capture, duplicate controls, payment scheduling, batching, execution, remittance, statement reconciliation, controls, and release evidence stay executable in `runtime.py`.

2. Repository-backed application surfaces
   Add `repository.py` to provide owned-table dataset bindings for vendor readiness, invoice intake, payment release, and statement reconciliation.

3. Database-backed forms and guided wizards
   Add `forms.py` and `wizards.py` so AP users can drive onboarding, intake, payment release, and reconciliation as governed workflows.

4. Control layer
   Add `controls.py` to encode release-safe AP checks for vendor readiness, duplicate holds, payment-batch integrity, statement visibility, and AppGen-X event-contract lock.

5. Package wiring and AI assistant exposure
   Update `__init__.py`, `ui.py`, `agent.py`, and `release_evidence.py` so the standalone surfaces are exported, rendered, and validated as part of the package contract.

6. Focused validation
   Keep existing contract/implementation tests passing and add a standalone-surface test module for repository/forms/wizards/controls.

## Guardrails

- Only modify `src/pyAppGen/pbcs/ap_automation`.
- Do not introduce shared-table access.
- Do not expose stream-engine choice or non-AppGen-X eventing.
- Keep the diff domain-specific and hand-crafted.
