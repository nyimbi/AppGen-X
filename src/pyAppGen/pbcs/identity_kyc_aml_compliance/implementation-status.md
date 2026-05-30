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
