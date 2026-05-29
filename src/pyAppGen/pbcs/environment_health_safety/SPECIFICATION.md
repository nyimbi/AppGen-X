# Environment Health and Safety PBC

## Purpose

`environment_health_safety` is a standalone package-local PBC for EHS incident response, hazard prevention, inspections, permits, corrective actions, training, audit evidence, and regulator-facing governance. The package owns its schema contracts, migration DDL, executable workflows, AppGen-X event contracts, UI/agent surfaces, and release evidence.

## Standalone operational slice

The implemented slice centers on six high-value loops:

1. Serious incident intake, classification, and notification clocks.
2. Investigation dossier completion with closure gating.
3. Near-miss cluster promotion into the hazard register.
4. Permit conflict detection for simultaneous operations.
5. Corrective action effectiveness review and reopen logic.
6. Policy, audit-seal, KPI, and control-assertion governance.

## Owned datastore boundary

Owned business tables:

- `environment_health_safety_ehs_incident`
- `environment_health_safety_hazard`
- `environment_health_safety_inspection`
- `environment_health_safety_permit`
- `environment_health_safety_corrective_action`
- `environment_health_safety_safety_training`
- `environment_health_safety_audit_finding`
- `environment_health_safety_policy_rule`
- `environment_health_safety_runtime_parameter`
- `environment_health_safety_schema_extension`
- `environment_health_safety_control_assertion`
- `environment_health_safety_governed_model`

Event tables:

- `environment_health_safety_appgen_outbox_event`
- `environment_health_safety_appgen_inbox_event`
- `environment_health_safety_appgen_dead_letter_event`

No foreign tables are mutated.

## Lifecycle and governance behavior

- Incident closure is blocked until required investigation fields, corrective action effectiveness, and required regulator notification acknowledgement are complete.
- Fatalities, hospitalizations, major releases, and fire events start jurisdiction-aware reporting clocks.
- Repeated near misses with the same unsafe condition and task create or update a hazard entry with incident lineage.
- Permit conflicts are detected across area, time window, and permit type.
- Consumed governance events are idempotent and either re-evaluate owned records or seal owned evidence bundles.
- Continuous control testing opens exceptions for overdue serious-incident notifications and expired permits.

## Workflow and UX coverage

The workbench exposes incident cards with severity, recordability, notification status, and priority. Forms and wizards cover incident intake, hazard registration, permit issue, inspection sync, dynamic risk assessment, and regulator export preparation. The assistant layer provides preview-only triage, investigation gap detection, hazard promotion explanation, permit conflict checking, and governed CRUD previews.
