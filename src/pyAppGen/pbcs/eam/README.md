# Enterprise Asset Management PBC

## Purpose

The `eam` Packaged Business Capability owns enterprise maintenance operations for physical assets. It is designed to run as a standalone one-PBC AppGen-X application or as part of a composed application. The PBC covers equipment registration, asset hierarchy, criticality, maintenance strategies, preventive and predictive planning, condition and meter readings, work orders, scheduling, mobile execution, safety permits, spares, vendor service, downtime, failure analysis, reliability analytics, governance, AppGen-X eventing, and AI-assisted maintenance planning.

This package is intentionally executable. It is not only a manifest or documentation bundle: the runtime can configure itself, register equipment, release plans, record readings, approve permits, create and schedule work orders, issue spares, complete work, consume external events idempotently, emit AppGen-X events, render a workbench, and produce release evidence.

## Owned Boundary

EAM owns its operational tables and does not mutate production, quality, inventory, procurement, asset lifecycle, audit, or analytics tables. Integration happens through declared APIs, AppGen-X events, and package-local projections. The physical owned tables use the `eam_` prefix in schema evidence; the logical runtime tables include equipment, maintenance plans, work orders, spare usage, condition readings, meter readings, failure events, schedules, vendor events, safety permits, rules, parameters, configuration, outbox, inbox, and dead-letter evidence.

Supported ordinary datastore backends are PostgreSQL, MySQL, and MariaDB. EAM does not expose a user-selectable stream engine; ordinary eventing is fixed to the AppGen-X event contract.

## Domain Capabilities

The PBC implements the improve1 backlog as a standalone maintenance application surface:

- Equipment readiness, hierarchy integrity, location state, criticality, warranty, and decentralized identity evidence.
- Maintenance strategy portfolios, PM/PdM plan readiness, meter triggers, predictive signal handling, and condition reading validation.
- Work request triage, work-order state control, planning packages, skill/tool checks, scheduling optimization, and mobile execution controls.
- Safety permit readiness, lockout/isolation mapping, spare reservation/issue governance, repairable spare flows, and vendor service management.
- Downtime projection, failure classification, RCA, corrective action tracking, reliability analytics, failure forecasting, counterfactual strategy simulation, and backlog risk scoring.
- AppGen-X inbox/outbox reliability, owned-boundary proof, technician/planner workbenches, agent-safe planning, semantic instruction parsing, anomaly detection, governed reliability model evidence, resilience drills, continuous controls, readiness scoring, and end-to-end execution proof.

## Runtime and Services

The primary executable surface is `runtime.py`. It provides side-effect-free runtime contracts and deterministic smoke scenarios for:

- `eam_configure_runtime`
- `eam_register_equipment`
- `eam_create_maintenance_plan`
- `eam_record_condition_reading`
- `eam_record_meter_reading`
- `eam_create_safety_permit`
- `eam_create_work_order`
- `eam_schedule_work_order`
- `eam_issue_spare_part`
- `eam_complete_work_order`
- reliability, simulation, compliance, routing, model-governance, and control-test helpers

`services.py`, `routes.py`, `schema_contract.py`, `models.py`, `events.py`, `handlers.py`, `permissions.py`, and `release_evidence.py` expose the same PBC-owned boundary to generated applications and release audits.

## Standalone App Surface

`app_surface.py` is the one-PBC application contract. It exposes:

- Forms for equipment readiness, maintenance strategy, work request triage, planning packages, safety/isolation, mobile execution, spare/vendor service, and reliability controls.
- Wizards for equipment-to-strategy readiness, work planning, safety isolation, mobile execution, reliability improvement, vendor/repairable flows, and resilience release proof.
- Controls for equipment readiness, plan release, work-order lifecycle, scheduling, permits, spares/vendors, mobile execution, reliability model governance, AppGen-X event reliability, and owned-boundary scans.
- `single_pbc_eam_app_contract()` for generated single-PBC applications.
- `document_instruction_eam_plan()` for side-effect-free AI document/instruction planning.
- `end_to_end_maintenance_execution_proof()` for equipment registration through completed maintenance event evidence.

## UI and Agent

The UI contract exposes a maintenance workbench with equipment registry, hierarchy map, planning, condition monitoring, work orders, scheduling, spares, safety, reliability, vendor service, rules, parameters, configuration, AppGen-X events, and release evidence. The agent contributes EAM skills to the composed application assistant and can parse maintenance notes, manuals, inspection sheets, vendor reports, and instructions into governed CRUD previews. Mutations require human confirmation and remain restricted to EAM-owned tables.

## Events

EAM emits typed AppGen-X events including equipment registration, maintenance plan release, condition/meter readings, permit approval, work-order creation/scheduling/completion, spare usage, and vendor performance updates. It consumes downtime, nonconformance, inventory reservation, purchase order acknowledgement, and asset lifecycle events through idempotent inbox handling with retry/dead-letter evidence.

## Verification

Focused verification for this slice:

```bash
PYTHONPATH=src python3 -m compileall -q src/pyAppGen/pbcs/eam
PYTHONPATH=src /Volumes/Media/src/pjs/appgen/.venv/bin/pytest -q src/pyAppGen/pbcs/eam/tests
```

The PBC also passed focused AppGen-X audits for source artifacts, package-local assurance, specification depth, agent capability, implementation release, implemented capability, and generation smoke.
