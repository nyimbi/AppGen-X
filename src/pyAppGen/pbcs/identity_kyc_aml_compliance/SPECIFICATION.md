# Identity KYC AML Compliance PBC

## Purpose

`identity_kyc_aml_compliance` owns customer onboarding, identity proofing, beneficial ownership, sanctions and PEP screening, ongoing monitoring, suspicious activity escalation, and compliance decisioning. It remains standalone by owning its schema, migrations, runtime workflows, UI/assistant contracts, AppGen-X events, and release evidence inside this package.

## Core entities

- `identity_kyc_aml_compliance_kyc_profile`: onboarding classification, lifecycle status, risk tier, EDD flags, duplicate candidates, and next rescreen date.
- `identity_kyc_aml_compliance_identity_document`: document completeness, authenticity, expiry, liveness, and face-match evidence.
- `identity_kyc_aml_compliance_beneficial_owner`: threshold ownership, control-person roles, and screening requirements.
- `identity_kyc_aml_compliance_screening_hit`: sanctions, PEP, RCA, adverse media, and deny-list evidence with severity, confidence, and disposition.
- `identity_kyc_aml_compliance_monitoring_alert`: typology, severity, assignment, SLA, and triage state.
- `identity_kyc_aml_compliance_suspicious_activity_case`: escalated alert cases and suspicious activity handling.
- `identity_kyc_aml_compliance_compliance_review`: EDD packets, review outcomes, and risk score challenge lineage.

## Executable workflows

- Onboarding wizard: classification -> document capture -> screening -> beneficial ownership -> EDD packet -> approval gate.
- Rescreening cycle: risk-tier calendar plus event-driven follow-up from `PolicyChanged`, `AuditEventSealed`, and `OperationalKpiChanged`.
- Monitoring escalation: alert triage -> case promotion boundary -> review evidence capture.
- Risk challenge flow: factor-based score explanation, challenge note, supervisor approval, and persisted review lineage.

## Rules and parameters

Rules include classification requirements, document completeness/authenticity, beneficial owner threshold policy, EDD triggers, periodic rescreening, alert-to-case promotion, and risk score challenge controls.

Parameters include threshold owner percentages, high-risk threshold percentages, rescreening cadences for low/medium/high risk, workbench limits, and high-risk geography lists.

## Public contracts

- APIs: `POST /kyc-profiles`, `POST /identity-documents`, `POST /beneficial-owners`, `POST /screening-hits`, `POST /monitoring-alerts`, `GET /identity-kyc-aml-compliance-workbench`
- Emitted events: `IdentityKycAmlComplianceCreated`, `IdentityKycAmlComplianceUpdated`, `IdentityKycAmlComplianceApproved`, `IdentityKycAmlComplianceExceptionOpened`
- Consumed events: `PolicyChanged`, `AuditEventSealed`, `OperationalKpiChanged`
- UI fragments: `IdentityKycAmlComplianceWorkbench`, `IdentityKycAmlComplianceDetail`, `IdentityKycAmlComplianceAssistantPanel`, `IdentityKycAmlComplianceOnboardingWizard`, `IdentityKycAmlComplianceReviewPacket`

## Guardrails

- No foreign-table writes.
- No stream-engine selector.
- Mutating assistant actions require confirmation.
- Approval requires document, screening, ownership, duplicate-resolution, and EDD gates to pass.
