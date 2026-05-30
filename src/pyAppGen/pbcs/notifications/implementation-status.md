# notifications implementation status

## Improve1 executable controls

- Status: implemented for 50 of 50 improve1 backlog features.
- Control module: `notifications_control.py`.
- Runtime wiring: `notifications_runtime_capabilities()` exposes `notification_control` and `evaluate_notification_control`.
- UI wiring: `notifications_ui_contract()` and `notifications_render_workbench()` expose 50 notification control panels, service actions, and agent tools.
- Release evidence: `validate_release_evidence()` includes the notification control contract and blocks on failed improve1 controls.
- Tests: `tests/test_domain_behavior.py` validates ownership, AppGen-X eventing, database backend allowlist, projection-only dependencies, human approval gates, agent preview gates, non-mutating simulations, and delivery-risk evidence gates.

## Domain surface covered

The controls cover template governance, typed variables, localization, channel capabilities, recipient endpoint quality, preference timelines, consent conflicts, purpose taxonomy, quiet hours, delivery optimization, fatigue, campaign suppression, provider health and simulation, failover, idempotent send orchestration, delivery attempts, retries, dead letters, receipts, bounces, deliverability analytics, campaign readiness, pacing, experiments, transactional SLAs, payload validation, secure tokens, attachments, content safety, accessibility, dynamic variants, channel escalation, in-app inbox, preference UI, operations cockpit, recipient dossiers, anomaly detection, abuse guardrails, cost and carbon optimization, audit hash chains, AppGen-X hardening, cross-PBC boundary proof, agent skills, UI coverage, resilience drills, and end-to-end release proof.

## Boundary assertions

- Database backends remain limited to PostgreSQL, MySQL, and MariaDB.
- Eventing remains AppGen-X on the package notifications topic.
- No stream-engine picker is exposed.
- Cross-PBC facts are represented through declared APIs, events, or projections, not shared table mutation.
- All control evaluations are side-effect free and return release evidence.
