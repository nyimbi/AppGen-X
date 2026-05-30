# Food Safety Quality Compliance PBC

## Purpose

The `food_safety_quality_compliance` slice owns HACCP plan versions, critical control points, inspections, nonconformances, recall events, supplier audits, quality holds, rules, parameters, governed assistant previews, and release evidence. It does not read or mutate foreign inventory, manufacturing, supplier-master, or customer tables.

## Domain Model

### HACCP Plan Versions

- Plan identity: `plan_code`, `version`, `facility_code`, `product_scope`
- Governance: `approvals`, `effective_from`, `supersedes_plan_id`, `supersession_reason`
- Safety evidence: `process_steps`, `hazard_analysis`, `evidence_hash`
- Approval gate: required hazards with `requires_ccp=true` must be covered by CCP definitions and approvals from food safety, quality, and operations must be present.

### Critical Control Points

- Linkage: `plan_id`, `process_step_code`, `hazard_id`
- Limits: `limit_min`, `limit_max`, `unit`
- Monitoring: `monitoring_method`, `monitoring_frequency_minutes`, `verification_requirement`
- Corrective action: `corrective_action`, `responsible_role`

### Inspections, Nonconformances, and Holds

- Inspections pin `plan_id` and `plan_version` from the active approved plan.
- Critical or allergen/temperature/foreign-material findings open quality holds automatically.
- Major and critical findings also open nonconformances.
- Major or critical nonconformances cannot close without root cause, preventive action, and effectiveness evidence.
- Holds capture affected lots, quantity, location, release criteria, disposition, approvers, and linked HACCP version.

### Supplier Audits

- Supplier audits store supplier projections, commodity, audit type, findings, risk rating, corrective actions, and expiry tracking.
- High-risk, expired, or major-finding audits block approval status.
- Near-expiry audits are surfaced in the workbench.

### Recall Events

- Recall and mock recall flows use `genealogy_projection` and `shipment_projection` inputs only.
- Foreign table access attempts are rejected.
- Mock drills do not mutate live recall state and return evidence packets with elapsed time against the configured target.

### Governed Assistant Previews

- Assistant previews resolve to owned tables only.
- Citations are mandatory.
- Release-impacting previews require explicit release review before approval.
- Approved previews record approver identity and confirmation state.

## Public APIs

- `POST /haccp-plans`
- `POST /critical-control-points`
- `POST /inspections`
- `POST /nonconformances`
- `POST /recall-events`
- `GET /food-safety-quality-compliance-workbench`

## Workbench

- HACCP Approval Queue
- Inspection Escalation Queue
- Open Quality Holds
- Supplier Audit Monitor
- Recall Readiness Board

## Forms And Wizards

- Forms: HACCP plan version intake, CCP definition, inspection review, recall event or mock drill
- Wizards: HACCP authoring and recall response
- Controls: approve HACCP plan, open hold, release hold, run mock recall, approve assistant preview

## Eventing

- Emitted: `FoodSafetyQualityComplianceCreated`, `FoodSafetyQualityComplianceUpdated`, `FoodSafetyQualityComplianceApproved`, `FoodSafetyQualityComplianceExceptionOpened`
- Consumed: `PolicyChanged`, `AuditEventSealed`, `OperationalKpiChanged`
- Idempotency: required for all inbound event handling
- Dead-letter evidence: unexpected events land in `food_safety_quality_compliance_appgen_dead_letter_event`

## Rules And Parameters

### Rules

- `haccp_plan_effectivity_rule`
- `ccp_hazard_mapping_rule`
- `critical_findings_hold_rule`
- `major_nonconformance_closure_rule`
- `supplier_approval_expiry_rule`
- `recall_projection_boundary_rule`
- `assistant_mutation_guardrail_rule`

### Parameters

- `ccp_monitoring_grace_minutes`
- `hold_release_min_approvers`
- `supplier_audit_expiry_warning_days`
- `mock_recall_target_minutes`
- `regulatory_obligation_sla_days`
- `workbench_limit`
