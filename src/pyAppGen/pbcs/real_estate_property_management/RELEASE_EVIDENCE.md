# Release Evidence - Real Estate Property Management

Package directory: `pbcs/real_estate_property_management`.

## Structural Evidence

- Owned schema contract includes `31` owned tables.
- Canonical API contract exposes `23` routes plus the legacy `/propertys` alias.
- Service contract exposes runtime configuration, governance, workbench query, and `22` domain commands.
- Eventing remains AppGen-X outbox/inbox/dead-letter only.

## Domain Scenario Evidence

- `move_in_flow`: record_tenant, create_lease, record_move_event, record_security_deposit
- `renewal_and_notice_flow`: manage_renewal, issue_notice
- `arrears_escalation_flow`: post_charge, escalate_delinquency
- `maintenance_closeout_flow`: open_maintenance_request, create_vendor_work_order, create_inspection
- `owner_reporting_flow`: publish_owner_report, capture_asset_performance
- `assistant_preview_flow`: preview_assistant_document_instruction

## Workbench and Analytics Evidence

- Queue rails: vacancies, renewals, delinquencies, maintenance, notices, compliance.
- KPI metrics: occupancy rate, annualized base rent, delinquency balance, open work orders, compliance backlog, CAM billed.
- Owner evidence: owner statements and asset performance snapshots.
- Assistant evidence: governed document/instruction CRUD previews plus control assertions.

## Verification Hooks

- `real_estate_property_management_runtime_smoke()` validates runtime configuration, events, workbench query, boundary checks, schema, API, and release evidence.
- `tests/test_contract.py` exercises end-to-end property, lease, collections, maintenance, compliance, owner-reporting, and assistant preview flows.
- `validate_release_evidence()` blocks release if required scenarios or structural checks are missing.
