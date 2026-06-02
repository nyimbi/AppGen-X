# Enterprise Risk Controls Implementation Plan

## Goal

Turn `enterprise_risk_controls` into a coherent package-local one-PBC application slice for risk intake, assessment, control definition, attestation, remediation, assurance packet preparation, and governed assistant previews without changing any shared AppGen-X code.

## Scope

- Keep every edit inside `src/pyAppGen/pbcs/enterprise_risk_controls`.
- Preserve the owned-table boundary and AppGen-X outbox/inbox/dead-letter contract.
- Build executable app surfaces around the existing runtime and domain-depth contracts instead of broadening into framework or generator work.

## Backlog Focus From `improve1.md`

This implementation concentrates on the highest-leverage improvements already described in the backlog:

1. Risk intake and registration readiness
   - Add a risk registration form and guided wizard flow for structured cause-event-impact capture.

2. Inherent, residual, and target risk handling
   - Add a dedicated assessment form and service route so risk reviews are not collapsed into one generic action.

3. Control architecture and testing
   - Add control-definition and control-test forms, control-center metadata, and executable route/service contracts.

4. Attestation and remediation governance
   - Add attestation and remediation forms plus guided recovery and release-readiness wizards.

5. Assurance packet readiness and executive visibility
   - Add assurance-packet surfaces, control evidence aggregation, and workbench bindings.

6. Rules, parameters, and assistant guardrails
   - Replace generic governance wrappers with domain-specific rule/parameter/config contracts and assistant CRUD previews that stay inside enterprise-risk-owned tables.

## Work Items

1. Add package-local app surfaces
   - Create `forms.py`, `wizards.py`, and `controls.py`.
   - Bind those surfaces to enterprise risk operations, routes, permissions, and owned tables.

2. Tighten package-local governance
   - Rewrite `config.py` and `permissions.py` around risk appetite, evidence, attestation, and remediation concerns.

3. Rebuild the executable facade
   - Replace shallow `services.py`, `routes.py`, `ui.py`, `agent.py`, `events.py`, `handlers.py`, and `service_contract.py` wrappers with domain-specific executable contracts.

4. Strengthen release evidence
   - Update `release_evidence.py` so release readiness covers schema, service, API, handlers, UI, forms, wizards, controls, assistant, config, and required docs.

5. Add focused tests
   - Keep the existing contract tests.
   - Add app-surface tests for forms, wizards, controls, assistant preview, release evidence, service routes, and UI bindings.

6. Refresh package docs
   - Add `README.md` and `implementation-status.md`.
   - Refresh `RELEASE_EVIDENCE.md` so the written evidence matches the executable slice.

## Non-Goals

- No edits outside `src/pyAppGen/pbcs/enterprise_risk_controls`.
- No central framework, generator, or cross-PBC changes.
- No new third-party dependencies.
- No attempt to rewrite the full generated specification backlog into framework-mounted production views.

## Verification Plan

- Run Python compilation for `src/pyAppGen/pbcs/enterprise_risk_controls`.
- Run focused `pytest` for `src/pyAppGen/pbcs/enterprise_risk_controls/tests`.
- Run package-local release/readiness smoke checks through Python entry points when possible.
