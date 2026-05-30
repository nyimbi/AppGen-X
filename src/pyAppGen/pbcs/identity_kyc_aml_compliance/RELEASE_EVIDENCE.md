# Release Evidence - Identity KYC AML Compliance

Package directory: `pbcs/identity_kyc_aml_compliance`.

## Evidence Summary

- Owned datastore boundary is enforced: every table is prefixed `identity_kyc_aml_compliance_` and foreign-table mutation plans are rejected.
- KYC onboarding is classification-gated: customer type, jurisdiction, product exposure, channel, and expected activity are mandatory at profile creation.
- Lifecycle progression is guarded: approval is blocked when accepted documents are missing, blocking screening hits remain unresolved, EDD packets are incomplete, beneficial ownership coverage is incomplete, or duplicate identity resolution is pending.
- Document evidence is modeled explicitly: completeness, authenticity, expiry, liveness, and face-match confidence are captured in package-owned records.
- Screening is category-aware: sanctions, PEP, RCA, adverse media, and deny-list outcomes retain severity, confidence, and blocking disposition state.
- Ongoing monitoring is executable: periodic rescreening due dates, policy/audit/KPI-triggered follow-up, alert triage, and alert-to-case promotion are covered by the runtime and tests.
- Governed AI and UI surfaces are present: assistant plans, mutation previews, workbench queues, forms, wizards, and controls are all package-local contracts.

## Verification Artifacts

- `runtime.py` exposes executable smoke coverage for onboarding, screening, lifecycle approval, inbound-event idempotency, and workbench/detail projections.
- `tests/test_contract.py` validates package metadata, schema/service/release contracts, route dispatch, governance hooks, permissions, seed data, and standalone smoke.
- `tests/test_workflows.py` validates approval gating, PEP-triggered EDD, event-driven alerting, alert promotion, and risk score challenge controls.
