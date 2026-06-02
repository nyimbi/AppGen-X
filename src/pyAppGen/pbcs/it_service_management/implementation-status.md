# IT Service Management Implementation Status

Status: implemented in standalone PBC slice.

## Completed

- Added ITSM-specific forms, wizards, controls, and single-PBC application runtime.
- Covered major incidents, request catalog, access governance, change enablement, problem management, CMDB ownership/impact, knowledge, and SLA controls.
- Integrated forms/wizards/controls into the UI contract and release readiness manifest.
- Added tests for standalone execution, UI surfaces, domain blockers, assistant-owned CRUD preview, and release evidence.

## Evidence

- `PYTHONPATH=src python3 -m compileall -q src/pyAppGen/pbcs/it_service_management`: passed.
- `PYTHONPATH=src /Volumes/Media/src/pjs/appgen/.venv/bin/pytest -q src/pyAppGen/pbcs/it_service_management/tests`: 12 passed.
- `standalone_smoke_test()`: true.
- `validate_release_evidence()`: true.
- Focused source/package/spec/agent/implementation/capability audits: true.
- Focused generation smoke audit: true on rerun after dependency import warmup.
- Commit: pending.

## Improve1 ITSM control implementation

- Added `itsm_control.py` as the executable improve1 control surface for all 50 IT service management backlog features.
- Each feature now has an owned control table, required field set, UI panel name, service/API route, AppGen-X event evidence, PostgreSQL/MySQL/MariaDB backend boundary, dependency declaration, and side-effect-free evaluation payload.
- Domain-specific controls cover major incident declaration, priority matrices, duplicate correlation and outage rollup, frozen timelines, restoration milestones, resolver handoffs, service catalog structure, access entitlement validation, fulfillment orchestration, requester confirmation, change paths, blast-radius scoring, maintenance windows, CAB quorum, backout plans, PIR, problem linkage, RCA templates, known errors, recurrence detection, CI graph/ownership/drift, service impact previews, SLA/OLA/UC separation, calendar-aware pauses, role queues, attention routing, knowledge lifecycle, contextual suggestions, document intake, policy sandboxing, runtime guardrails, event replay, dead-letter triage, consumed-event lineage, predictive breach risk, counterfactual simulations, continuous controls, cryptographic evidence, tenant isolation, tenant calendars, carbon-aware scheduling, continuity checks, release assurance, metrics dictionary, audit exports, operator ergonomics, idempotent APIs, and end-to-end scenario harnesses.
- Runtime, UI, workbench, and release evidence now expose the ITSM control contract.
- `tests/test_domain_behavior.py` verifies the control contract and representative ITSM failure modes; `IMPROVE1_TRACEABILITY.md` maps each of the 50 features to `itsm_control.py`, UI, service/API, tests, and release evidence.
