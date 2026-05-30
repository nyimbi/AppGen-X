# Enterprise Risk Controls PBC

`enterprise_risk_controls` is a package-local AppGen-X enterprise risk and controls slice for risk registration, structured assessment, control governance, attestations, remediation tracking, assurance packet preparation, and governed assistant previews.

## What This Package Owns

- Enterprise-risk-owned schema, models, and migrations for risk registers, assessments, indicators, controls, attestations, exceptions, remediation, evidence packets, policy mappings, inbox, outbox, and dead letters.
- Executable package-local contracts for services, routes, events, handlers, permissions, rules, parameters, and workbench metadata.
- One-PBC app surfaces: forms, guided wizards, control-center evidence, and assistant document-to-CRUD previews that stay inside owned tables.

## Domain Shape

This PBC is optimized for risk, compliance, assurance, and internal control teams that need to:

- register and classify enterprise risks,
- assess inherent and residual posture,
- define controls and schedule testing,
- coordinate attestations and remediation,
- assemble assurance packets and committee material,
- review risk rules, parameters, and release readiness,
- use an assistant to turn uploaded policy notes or audit instructions into bounded mutation previews.

## Key Entry Points

- Runtime: `runtime.py`
- Services: `services.py`
- Routes: `routes.py`
- UI contract: `ui.py`
- Forms: `forms.py`
- Wizards: `wizards.py`
- Controls: `controls.py`
- Assistant support: `agent.py`
- Release evidence: `release_evidence.py`

## One-PBC App Surface

The package exposes:

- risk registration, assessment, control design, testing, attestation, remediation, and assurance packet forms,
- guided wizards for risk intake, control gap response, committee readiness, and assistant-guided change review,
- a control center for release readiness, appetite and evidence gates, boundary proof, and assistant guardrails,
- workbench metadata that binds routes, panels, forms, wizards, controls, and permissions to enterprise-risk-owned tables,
- assistant/chatbot previews that classify documents and instructions into safe, permissioned CRUD plans.

## Verification

Primary verification lives in package-local tests under `tests/`, the runtime smoke path in `runtime.py`, and the release/readiness checks in `release_evidence.py`.
