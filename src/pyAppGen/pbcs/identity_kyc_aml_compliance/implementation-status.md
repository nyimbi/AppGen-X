# Implementation Status

## Status

- Standalone slice implemented inside `src/pyAppGen/pbcs/identity_kyc_aml_compliance` only.
- Core runtime is package-local and domain-specific rather than generator-placeholder scaffolding.
- Schema, migration, service, route, handler, UI, agent, configuration, release evidence, README, and tests are aligned to the same owned domain model.

## Completed

- KYC lifecycle gates with approval-time evidence checks.
- Onboarding classification capture and duplicate-candidate detection.
- Identity document completeness, expiry, authenticity, and remote-verification evidence.
- Beneficial owner threshold policy and control-person handling.
- Screening category routing for sanctions, PEP, RCA, and adverse media.
- Event-driven alerting from policy, audit, and KPI events.
- Monitoring alert triage and alert-to-case promotion boundary.
- Risk score explainability, challenge flow, and rescreening scheduling.
- Standalone smoke and focused workflow tests.

## Remaining Gaps

- No real persistence adapter or HTTP server wiring in this package; routes remain executable contracts rather than network handlers.
- No binary document or OCR processing; document intake is governed metadata and evidence modeling only.
- No external sanctions provider integrations; screening hits are represented as package-owned evidence records.

## Improve1 Identity KYC/AML control implementation

- Added `identity_control.py` as the executable improve1 control surface for all 50 KYC/AML backlog features.
- Each feature now has an owned control table, required field set, UI panel name, service/API route, AppGen-X event evidence, PostgreSQL/MySQL/MariaDB backend boundary, dependency declaration, and side-effect-free evaluation payload.
- Domain-specific negative checks cover lifecycle evidence, onboarding obligations, duplicate identity resolution, document completeness/authenticity/liveness, sanctions/PEP/RCA screening, beneficial ownership, EDD packets, SAR/STR boundary, maker-checker segregation, privacy exports, API idempotency, document file safety, event contracts, inbound handler boundaries, agent guardrails, model governance, tenant isolation, and end-to-end release proof.
- Runtime, UI, workbench, and release evidence now expose the identity control contract.
- `tests/test_domain_behavior.py` verifies the control contract and the representative KYC/AML failure modes; `IMPROVE1_TRACEABILITY.md` maps each of the 50 features to `identity_control.py`, UI, service/API, tests, and release evidence.
