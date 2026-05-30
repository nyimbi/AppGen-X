# Identity KYC AML Compliance

Standalone AppGen PBC slice for onboarding, identity proofing, beneficial ownership, sanctions and PEP screening, ongoing monitoring, suspicious activity escalation, and governed compliance decisioning.

## What this slice owns

- Owned schema, migration DDL, and schema/model contracts for KYC profiles, identity documents, beneficial owners, screening hits, monitoring alerts, suspicious activity cases, reviews, rules, parameters, control assertions, governed models, and AppGen-X event tables.
- Executable workflows for onboarding classification, document evidence evaluation, beneficial ownership threshold coverage, sanctions and PEP routing, EDD gating, rescreening, alert triage, alert-to-case escalation, and risk score challenge handling.
- Workbench/UI contracts with forms, wizards, controls, queue definitions, and assistant surfaces.
- Focused package tests and standalone smoke/audit entrypoints.

## Key domain behaviors

- KYC profiles require customer type, jurisdiction, product exposure, channel, and expected activity at intake.
- Identity documents block progression when mandatory capture fields are missing, expired, tampered, or low-confidence.
- Entity, trust, and correspondent onboarding activates beneficial ownership and control-person screening requirements.
- Sanctions, PEP, RCA, and adverse media hits route through distinct severity and escalation rules.
- High-risk profiles, PEP exposure, complex ownership, and adverse media activate EDD obligations.
- Approved profiles receive periodic rescreening due dates based on risk tier.
- `PolicyChanged`, `AuditEventSealed`, and `OperationalKpiChanged` are consumed through the owned inbox and trigger package-local follow-up actions.

## Verification entrypoints

- `pyAppGen.pbcs.identity_kyc_aml_compliance.smoke_test`
- `pyAppGen.pbcs.identity_kyc_aml_compliance.runtime.identity_kyc_aml_compliance_runtime_smoke`
- `pyAppGen.pbcs.identity_kyc_aml_compliance.standalone.standalone_smoke`
