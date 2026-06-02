# Humanitarian Relief Operations PBC

`humanitarian_relief_operations` is a standalone AppGen-X PBC for field assessments, beneficiary registration, warehouse lots, last-mile shipments, distributions, cash/voucher exceptions, partners, protection referrals, incidents, donor accountability, and governed relief assistance.

## Standalone Application Surface

`HumanitarianReliefOperationsStandaloneApp` proves the PBC can run alone. It configures humanitarian rules, captures verified assessments, detects duplicate households, manages aid lots, blocks quarantined stock, onboards partners, dispatches shipments, reconciles distributions, opens confidential protection referrals, builds donor-safe packs, and generates assistant drafts that require confirmation and redaction.

## UI, Controls, and Agent

The workbench surfaces assessment queues, beneficiary duplicate review, warehouse lots, shipment proof, distribution reconciliation, protection referrals, partner readiness, donor packs, dead-letter triage, and agent drafts. Continuous controls cover assessment completeness, duplicate households, lot safety, site capacity, variance reconciliation, payout recovery, partner readiness, protection confidentiality, donor earmarks, dead-letter closure, and agent guardrails.

## Verification

- `PYTHONPATH=src python3 -m compileall -q src/pyAppGen/pbcs/humanitarian_relief_operations`
- `PYTHONPATH=src ./.venv/bin/pytest -q src/pyAppGen/pbcs/humanitarian_relief_operations/tests`
- `standalone_smoke_test()` and `validate_release_evidence()`
- focused AppGen-X PBC audits where available
