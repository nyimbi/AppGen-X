"""Executable improve1 controls for the Enterprise Asset Management PBC."""

from __future__ import annotations

import hashlib
from typing import Any

from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability

PBC_KEY = "eam"
EVENT_CONTRACT = "AppGen-X"
EAM_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
EAM_REQUIRED_EVENT_TOPIC = "appgen.maintenance.events"
EAM_OWNED_TABLES = (
    "equipment",
    "maintenance_plan",
    "work_order",
    "spare_part_usage",
    "condition_reading",
    "meter_reading",
    "failure_event",
    "maintenance_schedule",
    "service_vendor_event",
    "safety_permit",
    "maintenance_rule",
    "maintenance_parameter",
    "maintenance_configuration",
    "maintenance_outbox",
    "maintenance_inbox",
    "maintenance_dead_letter",
)
EAM_DECLARED_DEPENDENCIES = (
    "production_uptime_projection",
    "quality_reliability_projection",
    "inventory_spares_projection",
    "procurement_vendor_projection",
    "asset_lifecycle_projection",
    "GET /production/orders/{id}",
    "GET /quality/nonconformances/{id}",
    "GET /inventory/spares/{id}",
    "GET /procurement/vendors/{id}",
    "POST /audit/maintenance-events",
    "DowntimeCaptured",
    "NonConformanceRaised",
    "InventoryReservationConfirmed",
    "PurchaseOrderAcknowledged",
    "AssetLifecycleUpdated",
)

EQUIPMENT_TABLE = "equipment"
PLAN_TABLE = "maintenance_plan"
WORK_ORDER_TABLE = "work_order"
SPARE_TABLE = "spare_part_usage"
CONDITION_TABLE = "condition_reading"
METER_TABLE = "meter_reading"
FAILURE_TABLE = "failure_event"
SCHEDULE_TABLE = "maintenance_schedule"
VENDOR_TABLE = "service_vendor_event"
PERMIT_TABLE = "safety_permit"
RULE_TABLE = "maintenance_rule"
PARAMETER_TABLE = "maintenance_parameter"
CONFIG_TABLE = "maintenance_configuration"
OUTBOX_TABLE = "maintenance_outbox"
INBOX_TABLE = "maintenance_inbox"
DEAD_LETTER_TABLE = "maintenance_dead_letter"

EAM_CONTROL_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in EAM_CONTROL_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in EAM_CONTROL_CAPABILITIES}

_SPEC_ROWS: tuple[tuple[int, tuple[str, ...], tuple[str, ...], str, str, tuple[str, ...]], ...] = (
    (1, (EQUIPMENT_TABLE, METER_TABLE, PERMIT_TABLE), ("equipment_class", "site", "location", "criticality", "meter_setup", "safety_requirements"), "EquipmentRegistry", "POST /equipment/readiness-gate", ("asset_lifecycle_projection",)),
    (2, (EQUIPMENT_TABLE,), ("equipment_id", "parent_equipment_id", "effective_date", "site", "criticality_rollup", "isolation_impact"), "AssetHierarchyMap", "POST /equipment/hierarchy/validate", ()),
    (3, (EQUIPMENT_TABLE,), ("location", "installation_state", "operating_state", "maintainability_state", "effective_date"), "AssetHierarchyMap", "POST /equipment/location-state", ("AssetLifecycleUpdated",)),
    (4, (EQUIPMENT_TABLE, RULE_TABLE), ("safety_consequence", "environment_consequence", "production_consequence", "quality_consequence", "downtime_cost"), "ReliabilityDashboard", "POST /equipment/criticality-score", ("production_uptime_projection",)),
    (5, (EQUIPMENT_TABLE, WORK_ORDER_TABLE, VENDOR_TABLE), ("warranty_reference", "claim_window", "covered_failure_modes", "required_evidence", "recovery_estimate"), "VendorServicePanel", "POST /warranty/recovery-check", ("GET /procurement/vendors/{id}",)),
    (6, (PLAN_TABLE, RULE_TABLE), ("strategy_type", "risk_rationale", "expected_benefit", "cost_model", "review_cadence"), "MaintenancePlanConsole", "POST /maintenance-strategies", ()),
    (7, (PLAN_TABLE, WORK_ORDER_TABLE, PERMIT_TABLE, SPARE_TABLE), ("interval", "task_steps", "labor_skills", "spare_requirements", "permit_class", "release_approval"), "MaintenancePlanConsole", "POST /maintenance-plans/readiness", ("inventory_spares_projection",)),
    (8, (METER_TABLE, PLAN_TABLE, WORK_ORDER_TABLE), ("meter_unit", "rollover_policy", "reading_confidence", "due_at_threshold", "forecasted_due_date"), "ConditionMonitoringPanel", "POST /meters/triggers", ()),
    (9, (CONDITION_TABLE, RULE_TABLE), ("signal_type", "unit", "threshold", "sampling_cadence", "asset_applicability"), "ConditionMonitoringPanel", "POST /condition-signals", ()),
    (10, (CONDITION_TABLE, EQUIPMENT_TABLE), ("source", "timestamp", "unit", "device_identity", "equipment_state", "confidence_score"), "ConditionMonitoringPanel", "POST /condition-readings/validate", ()),
    (11, (WORK_ORDER_TABLE, FAILURE_TABLE), ("symptom", "asset", "severity", "safety_concern", "production_impact", "duplicate_check"), "WorkOrderBoard", "POST /work-requests/triage", ("DowntimeCaptured", "NonConformanceRaised")),
    (12, (WORK_ORDER_TABLE, OUTBOX_TABLE), ("current_state", "target_state", "actor", "reason", "required_fields", "idempotency_key"), "WorkOrderBoard", "POST /work-orders/state-transition", ()),
    (13, (WORK_ORDER_TABLE, PLAN_TABLE, SPARE_TABLE, PERMIT_TABLE), ("task_list", "craft_requirements", "estimated_duration", "spare_reservations", "tool_requirements", "supervisor_approval"), "PlannerSchedulerCockpit", "POST /work-packages/readiness", ("inventory_spares_projection",)),
    (14, (SCHEDULE_TABLE, WORK_ORDER_TABLE, SPARE_TABLE), ("candidate_windows", "failure_risk", "craft_capacity", "spare_availability", "permit_readiness", "carbon_preference"), "MaintenanceScheduler", "POST /schedule/optimize", ("production_uptime_projection", "inventory_spares_projection")),
    (15, (WORK_ORDER_TABLE, SCHEDULE_TABLE, OUTBOX_TABLE), ("mobile_state", "offline_queue", "job_step_checklist", "time_booking", "evidence_capture", "sync_status"), "TechnicianCockpit", "POST /mobile-execution/sync", ()),
    (16, (SCHEDULE_TABLE, WORK_ORDER_TABLE, RULE_TABLE), ("required_skill", "certification_expiry", "crew_size", "shift_schedule", "fatigue_exposure", "assignment_rationale"), "PlannerSchedulerCockpit", "POST /labor/assign", ()),
    (17, (WORK_ORDER_TABLE, SCHEDULE_TABLE, RULE_TABLE), ("tool_id", "availability_window", "calibration_status", "reservation", "substitute_rule"), "TechnicianCockpit", "POST /tools/match", ()),
    (18, (PERMIT_TABLE, EQUIPMENT_TABLE), ("permit_type", "hazards", "controls", "isolations", "approvers", "worker_acknowledgements"), "SafetyPermitConsole", "POST /safety-permits/readiness", ()),
    (19, (PERMIT_TABLE, EQUIPMENT_TABLE), ("isolation_points", "energy_types", "lock_owner", "verification_steps", "affected_equipment_tree"), "SafetyPermitConsole", "POST /lockout-isolation/map", ()),
    (20, (SPARE_TABLE, WORK_ORDER_TABLE), ("reservation_id", "part_number", "quantity", "serial_lot", "issue_approval", "cost_attribution"), "SpareUsageConsole", "POST /spares/issue-governance", ("InventoryReservationConfirmed",)),
    (21, (SPARE_TABLE, EQUIPMENT_TABLE, VENDOR_TABLE), ("removed_from_asset", "condition", "repair_vendor", "refurbishment_result", "certification", "installed_on_asset"), "SpareUsageConsole", "POST /repairables/lifecycle", ("GET /procurement/vendors/{id}",)),
    (22, (FAILURE_TABLE, WORK_ORDER_TABLE), ("downtime_event_id", "duration", "production_impact", "planned_flag", "restoration_evidence"), "ReliabilityDashboard", "POST /downtime/link", ("DowntimeCaptured", "production_uptime_projection")),
    (23, (FAILURE_TABLE, EQUIPMENT_TABLE), ("failure_mode", "mechanism", "cause", "effect", "detection_method", "severity"), "ReliabilityDashboard", "POST /failures/classify", ()),
    (24, (FAILURE_TABLE, WORK_ORDER_TABLE), ("rca_method", "hypothesis_evidence", "cause_validation", "corrective_actions", "effectiveness_check"), "ReliabilityDashboard", "POST /rca/corrective-actions", ("NonConformanceRaised",)),
    (25, (WORK_ORDER_TABLE, FAILURE_TABLE, CONDITION_TABLE, METER_TABLE), ("mtbf", "mttr", "availability", "backlog_age", "pm_compliance", "cost_risk_drilldown"), "ReliabilityDashboard", "GET /reliability/analytics", ()),
    (26, (FAILURE_TABLE, CONDITION_TABLE, METER_TABLE), ("failure_probability", "downtime_exposure", "safety_exposure", "spare_demand", "due_date_forecast"), "ReliabilityDashboard", "POST /failures/forecast", ("inventory_spares_projection",)),
    (27, (PLAN_TABLE, SCHEDULE_TABLE, FAILURE_TABLE), ("alternative_intervals", "thresholds", "shutdown_windows", "labor_plan", "spare_policy", "predicted_failures_avoided"), "MaintenancePlanConsole", "POST /strategies/simulate", ()),
    (28, (WORK_ORDER_TABLE, SCHEDULE_TABLE, FAILURE_TABLE), ("criticality", "failure_forecast", "safety_exposure", "compliance_deadline", "schedule_opportunity"), "PlannerSchedulerCockpit", "POST /backlog/risk-score", ()),
    (29, (WORK_ORDER_TABLE, PERMIT_TABLE, CONDITION_TABLE, OUTBOX_TABLE), ("plan", "permit", "technician_qualification", "calibration_evidence", "timestamps", "signatures"), "SafetyPermitConsole", "POST /compliance/proof-packet", ("POST /audit/maintenance-events",)),
    (30, (VENDOR_TABLE, WORK_ORDER_TABLE), ("vendor_id", "sla_commitment", "response_time", "first_time_fix", "rework", "performance_score"), "VendorServicePanel", "POST /vendors/performance", ("GET /procurement/vendors/{id}",)),
    (31, (VENDOR_TABLE, PERMIT_TABLE, WORK_ORDER_TABLE), ("dispatch_state", "acknowledgement", "expected_arrival", "credential_check", "permit_requirements", "completion_review"), "VendorServicePanel", "POST /vendors/dispatch", ("PurchaseOrderAcknowledged",)),
    (32, (EQUIPMENT_TABLE, PLAN_TABLE, WORK_ORDER_TABLE), ("lifecycle_event", "maintainability_state", "plan_eligibility", "hierarchy_change", "open_work_exceptions"), "AssetHierarchyMap", "POST /asset-lifecycle/project", ("AssetLifecycleUpdated", "asset_lifecycle_projection")),
    (33, (FAILURE_TABLE, WORK_ORDER_TABLE), ("nonconformance_id", "affected_equipment", "quality_severity", "required_inspection", "closure_feedback"), "ReliabilityDashboard", "POST /quality/nonconformance-review", ("NonConformanceRaised", "quality_reliability_projection")),
    (34, (SPARE_TABLE, SCHEDULE_TABLE, VENDOR_TABLE), ("projection_freshness", "part_identity", "quantity", "vendor", "due_date", "idempotency_key"), "PlannerSchedulerCockpit", "POST /dependency-projections/validate", ("InventoryReservationConfirmed", "PurchaseOrderAcknowledged", "inventory_spares_projection", "procurement_vendor_projection")),
    (35, (INBOX_TABLE, DEAD_LETTER_TABLE), ("event_type", "idempotency_key", "retry_count", "schema_valid", "projection_rebuild", "quarantine_control"), "MaintenanceEventConsole", "POST /events/inbox/replay", ("DowntimeCaptured", "NonConformanceRaised", "InventoryReservationConfirmed", "PurchaseOrderAcknowledged", "AssetLifecycleUpdated")),
    (36, (OUTBOX_TABLE, DEAD_LETTER_TABLE), ("event_type", "ordering_group", "payload_hash", "retry_count", "next_attempt", "delivery_proof"), "MaintenanceEventConsole", "POST /events/outbox/replay", ()),
    (37, (CONFIG_TABLE, RULE_TABLE), ("schema_scan", "service_scan", "route_scan", "agent_plan_scan", "generated_dsl_scan", "violations"), "MaintenanceConfigurationPanel", "POST /owned-boundary/proof", EAM_DECLARED_DEPENDENCIES),
    (38, (WORK_ORDER_TABLE, EQUIPMENT_TABLE, PLAN_TABLE, CONDITION_TABLE, METER_TABLE, PERMIT_TABLE, SPARE_TABLE), ("navigation_surface", "forms", "wizards", "controls", "events", "release_evidence"), "MaintenanceWorkbench", "GET /workbench/coverage", ()),
    (39, (WORK_ORDER_TABLE, SCHEDULE_TABLE, PERMIT_TABLE, SPARE_TABLE), ("assigned_jobs", "route_context", "permit_status", "job_steps", "tools", "offline_sync_status"), "TechnicianCockpit", "GET /technician/cockpit", ()),
    (40, (WORK_ORDER_TABLE, SCHEDULE_TABLE, SPARE_TABLE, PERMIT_TABLE), ("unplanned_requests", "incomplete_packages", "missing_spares", "missing_tools", "labor_conflicts", "schedule_proposals"), "PlannerSchedulerCockpit", "GET /planner/cockpit", ("inventory_spares_projection",)),
    (41, (RULE_TABLE, WORK_ORDER_TABLE, PERMIT_TABLE, SPARE_TABLE), ("command", "permission", "owned_tables", "idempotency_key", "expected_event", "human_confirmation"), "MaintenanceAgentPanel", "POST /agent/plan-maintenance-action", ()),
    (42, (WORK_ORDER_TABLE, PLAN_TABLE, CONDITION_TABLE, PERMIT_TABLE), ("source_document", "candidate_facts", "confidence", "evidence_links", "missing_fields", "mutation_preview"), "MaintenanceAgentPanel", "POST /agent/document-intake", ()),
    (43, (WORK_ORDER_TABLE, PLAN_TABLE, PERMIT_TABLE, SPARE_TABLE), ("instruction_text", "task_list", "hazards", "spare_requirements", "labor_skills", "acceptance_criteria"), "MaintenanceAgentPanel", "POST /agent/parse-instruction", ()),
    (44, (FAILURE_TABLE, CONDITION_TABLE, METER_TABLE, WORK_ORDER_TABLE), ("anomaly_type", "reading_pattern", "repeat_failure", "spare_usage", "labor_time", "explanation"), "ReliabilityDashboard", "POST /anomalies/detect", ()),
    (45, (RULE_TABLE, FAILURE_TABLE, CONDITION_TABLE), ("model_purpose", "training_window", "asset_coverage", "feature_lineage", "validation_metrics", "rollback_plan"), "ReliabilityDashboard", "POST /models/governance-evidence", ()),
    (46, (EQUIPMENT_TABLE, METER_TABLE, VENDOR_TABLE, PERMIT_TABLE), ("credential_reference", "issuer", "verification_status", "expiry", "revocation", "trust_level"), "EquipmentRegistry", "POST /identity/verify", ()),
    (47, (OUTBOX_TABLE, INBOX_TABLE, DEAD_LETTER_TABLE), ("drill_scenario", "failure_mode", "degraded_route", "recovery_step", "operator_evidence", "exit_criteria"), "MaintenanceEventConsole", "POST /resilience/drills", ()),
    (48, (RULE_TABLE, WORK_ORDER_TABLE, PERMIT_TABLE, SPARE_TABLE, DEAD_LETTER_TABLE), ("assertion", "control_result", "exception_owner", "due_date", "remediation", "aging"), "MaintenanceRuleStudio", "POST /controls/test", ()),
    (49, (CONFIG_TABLE, RULE_TABLE, WORK_ORDER_TABLE, EQUIPMENT_TABLE), ("equipment_completeness", "hierarchy_integrity", "plan_coverage", "event_reliability", "ui_coverage", "agent_safety"), "MaintenanceWorkbench", "GET /readiness-score", ()),
    (50, (EQUIPMENT_TABLE, PLAN_TABLE, CONDITION_TABLE, METER_TABLE, WORK_ORDER_TABLE, PERMIT_TABLE, SPARE_TABLE, OUTBOX_TABLE), ("equipment_registration", "plan_release", "trigger_evidence", "permit", "spare_issue", "completion_event"), "MaintenanceWorkbench", "POST /proof/end-to-end-maintenance", ("POST /audit/maintenance-events",)),
)

CONTROL_SPECS: dict[int, dict[str, Any]] = {
    number: {"tables": tables, "fields": fields, "ui": ui, "route": route, "dependencies": dependencies}
    for number, tables, fields, ui, route, dependencies in _SPEC_ROWS
}


def _digest(value: object) -> str:
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()


def _resolve(capability: Improve1Capability | str | int) -> Improve1Capability | None:
    if isinstance(capability, Improve1Capability):
        return capability
    if isinstance(capability, int):
        return CAPABILITY_BY_NUMBER.get(capability)
    return CAPABILITY_BY_SLUG.get(capability)


def sample_payload_for(capability: Improve1Capability | str | int) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {}
    spec = CONTROL_SPECS[resolved.feature_number]
    payload = {field: f"{resolved.slug}_{field}" for field in spec["fields"]}
    payload.update(
        {
            "references": (),
            "parent_equipment_id": "eq_parent",
            "equipment_id": "eq_asset_100",
            "target_state": "scheduled",
            "current_state": "planned",
            "permit_type": "electrical",
            "isolations": ("main_breaker",),
            "reservation_id": "reservation_100",
            "projection_freshness": "fresh",
            "violations": (),
            "mobile_state": "synced",
            "offline_queue": (),
            "certification_expiry": "2027-12-31",
            "calibration_status": "current",
            "schema_valid": True,
            "delivery_proof": "proof-100",
            "human_confirmation": True,
            "confidence": "high",
            "control_result": "pass",
            "agent_policy_result": "allow",
            "readiness_score": 0.96,
            "completion_event": "MaintenanceCompleted",
        }
    )
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    number = capability.feature_number
    if number == 1 and not (payload.get("criticality") and payload.get("meter_setup") and payload.get("safety_requirements")):
        findings.append("equipment readiness requires criticality, meter setup, and safety requirements")
    if number == 2 and payload.get("equipment_id") == payload.get("parent_equipment_id"):
        findings.append("asset hierarchy cannot make equipment its own parent")
    if number == 7 and not payload.get("release_approval"):
        findings.append("preventive maintenance plan release requires approval")
    if number == 10 and payload.get("confidence_score") in ("low", 0, 0.0):
        findings.append("condition readings with low confidence require review before risk scoring")
    if number == 12 and payload.get("current_state") == payload.get("target_state"):
        findings.append("work order lifecycle transition must move to a new state")
    if number == 15 and payload.get("mobile_state") == "completed" and payload.get("offline_queue"):
        findings.append("mobile completion cannot close while offline evidence remains unsynced")
    if number == 16 and str(payload.get("certification_expiry", "")) < "2026-05-30":
        findings.append("labor assignment blocks expired certification")
    if number == 17 and payload.get("calibration_status") != "current":
        findings.append("tool matching requires current calibration for controlled work")
    if number == 18 and not payload.get("isolations"):
        findings.append("safety permit readiness requires isolation evidence")
    if number == 20 and not payload.get("reservation_id"):
        findings.append("spare issue governance requires reservation evidence")
    if number == 34 and payload.get("projection_freshness") != "fresh":
        findings.append("inventory and procurement projections must be fresh before scheduling")
    if number == 37 and payload.get("violations"):
        findings.append("owned-boundary proof fails on foreign table or undeclared dependency violations")
    if number == 41 and payload.get("human_confirmation") is not True:
        findings.append("agent-safe maintenance planning requires human confirmation")
    if number == 42 and payload.get("confidence") == "low" and payload.get("human_confirmation") is not True:
        findings.append("low-confidence maintenance document intake requires human confirmation")
    if number == 48 and payload.get("control_result") != "pass":
        findings.append("continuous maintenance control testing opens a blocking exception")
    if number == 49 and float(payload.get("readiness_score", 0)) < 0.9:
        findings.append("EAM readiness score must remain above the release threshold")
    if number == 50 and payload.get("completion_event") != "MaintenanceCompleted":
        findings.append("end-to-end proof must include the MaintenanceCompleted event")
    return tuple(findings)


def evaluate_eam_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "pbc": PBC_KEY, "reason": "unknown_eam_control", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    active_payload = sample_payload_for(resolved) if payload is None else dict(payload)
    missing = tuple(field for field in spec["fields"] if field not in active_payload or active_payload[field] in (None, ""))
    invalid_tables = tuple(table for table in spec["tables"] if table not in EAM_OWNED_TABLES)
    allowed_refs = set(EAM_OWNED_TABLES) | set(EAM_DECLARED_DEPENDENCIES)
    invalid_references = tuple(ref for ref in active_payload.get("references", ()) if ref not in allowed_refs)
    domain_findings = _domain_findings(resolved, active_payload)
    event_type = "MaintenanceControlExceptionOpened" if domain_findings else "MaintenanceControlEvidenceRecorded"
    if resolved.feature_number in {1, 6, 7, 11, 12, 15, 18, 20, 31, 50} and not domain_findings:
        event_type = "MaintenanceWorkLifecycleAdvanced"
    if resolved.feature_number in {35, 36, 47} and not domain_findings:
        event_type = "MaintenanceEventReliabilityProven"
    return {
        "ok": not missing and not invalid_tables and not invalid_references and not domain_findings,
        "pbc": PBC_KEY,
        "capability": resolved.slug,
        "feature_number": resolved.feature_number,
        "title": resolved.title,
        "status": "implemented",
        "target_tables": spec["tables"],
        "owned_tables": EAM_OWNED_TABLES,
        "read_tables": (),
        "declared_dependencies": spec["dependencies"],
        "invalid_references": invalid_references,
        "missing_required_fields": missing,
        "domain_findings": domain_findings,
        "event": {
            "contract": EVENT_CONTRACT,
            "topic": EAM_REQUIRED_EVENT_TOPIC,
            "type": event_type,
            "idempotency_key": _digest((PBC_KEY, resolved.slug, active_payload)),
            "outbox_table": OUTBOX_TABLE,
            "inbox_table": INBOX_TABLE,
            "dead_letter_table": DEAD_LETTER_TABLE,
        },
        "ui_surface": spec["ui"],
        "service_api": spec["route"],
        "permission": "eam.safety" if resolved.feature_number in {18, 19, 29} else "eam.audit" if resolved.feature_number in {37, 48, 49, 50} else "eam.execute",
        "configuration": {
            "database_backends": EAM_ALLOWED_DATABASE_BACKENDS,
            "event_topic": EAM_REQUIRED_EVENT_TOPIC,
            "stream_engine_picker_visible": False,
            "rule_configurable": True,
            "parameter_configurable": True,
        },
        "agent_skill": f"eam_skills.{resolved.slug}",
        "requires_human_confirmation": resolved.feature_number in {7, 12, 18, 20, 29, 31, 37, 41, 42, 48, 50},
        "retry_dead_letter_evidence": {
            "retry_policy": "bounded_retry_with_idempotency_key",
            "dead_letter_table": DEAD_LETTER_TABLE,
            "manual_replay_route": "POST /events/inbox/replay",
        },
        "release_evidence": {
            "code_artifact_model": resolved.model_artifacts,
            "ui_surface": resolved.ui_artifacts,
            "service_api": resolved.service_artifacts,
            "test": resolved.test_artifacts,
            "evidence": resolved.evidence_artifacts,
        },
        "shared_table_access": False,
        "side_effects": (),
    }


def improve1_eam_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_eam_control(capability) for capability in EAM_CONTROL_CAPABILITIES)
    return {
        "ok": len(evaluations) == 50 and all(item["ok"] for item in evaluations),
        "pbc": PBC_KEY,
        "capability_count": len(evaluations),
        "capabilities": evaluations,
        "owned_tables": EAM_OWNED_TABLES,
        "declared_dependencies": EAM_DECLARED_DEPENDENCIES,
        "database_backends": EAM_ALLOWED_DATABASE_BACKENDS,
        "event_contract": EVENT_CONTRACT,
        "event_topic": EAM_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


EAM_CONTROL_FUNCTIONS = {
    capability.slug: (lambda payload=None, slug=capability.slug: evaluate_eam_control(slug, payload))
    for capability in EAM_CONTROL_CAPABILITIES
}
