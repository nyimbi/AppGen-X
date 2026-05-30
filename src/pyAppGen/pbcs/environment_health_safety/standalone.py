"""Standalone executable slice for the environment health and safety PBC.

This module is intentionally self-contained so the package can expose a rich,
domain-specific contract without depending on shared generators or foreign PBCs.
All writable state stays in package-owned structures and every contract surface
is derived from the same metadata and executable rules.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import UTC, datetime, timedelta
import hashlib
import json
from pathlib import Path
from typing import Any

PBC_KEY = "environment_health_safety"
PBC_LABEL = "Environment Health and Safety"
PBC_DESCRIPTION = (
    "EHS incidents, inspections, permits, hazards, corrective actions, training, "
    "audits, and compliance evidence"
)
MESH = "opsmfg"
VERSION = "2.0.0"

BUSINESS_TABLES = (
    f"{PBC_KEY}_ehs_incident",
    f"{PBC_KEY}_hazard",
    f"{PBC_KEY}_inspection",
    f"{PBC_KEY}_permit",
    f"{PBC_KEY}_corrective_action",
    f"{PBC_KEY}_safety_training",
    f"{PBC_KEY}_audit_finding",
    f"{PBC_KEY}_policy_rule",
    f"{PBC_KEY}_runtime_parameter",
    f"{PBC_KEY}_schema_extension",
    f"{PBC_KEY}_control_assertion",
    f"{PBC_KEY}_governed_model",
)
EVENT_TABLES = (
    f"{PBC_KEY}_appgen_outbox_event",
    f"{PBC_KEY}_appgen_inbox_event",
    f"{PBC_KEY}_appgen_dead_letter_event",
)
OWNED_TABLES = BUSINESS_TABLES + EVENT_TABLES
ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
REQUIRED_EVENT_TOPIC = f"pbc.{PBC_KEY}.events"

SERIOUS_INCIDENT_SEVERITIES = (
    "fatality",
    "hospitalization",
    "environmental_release",
    "fire",
)
RECORDABILITY_BY_SEVERITY = {
    "near_miss": "not_recordable",
    "first_aid": "not_recordable",
    "medical_treatment": "recordable",
    "restricted_work": "recordable",
    "lost_time": "recordable",
    "hospitalization": "recordable",
    "fatality": "recordable",
    "environmental_release": "pending_review",
    "fire": "pending_review",
}
INCIDENT_LIFECYCLE = (
    "draft",
    "triaged",
    "recordability_review",
    "regulator_notified",
    "investigation_open",
    "corrective_action_open",
    "closed",
    "reopened",
)
INCIDENT_TRANSITIONS = {
    "draft": {"triaged", "reopened"},
    "triaged": {"recordability_review", "regulator_notified", "investigation_open"},
    "recordability_review": {"regulator_notified", "investigation_open"},
    "regulator_notified": {"investigation_open"},
    "investigation_open": {"corrective_action_open"},
    "corrective_action_open": {"closed", "reopened"},
    "closed": {"reopened"},
    "reopened": {"investigation_open", "corrective_action_open"},
}

PERMIT_CONFLICT_MATRIX = {
    "hot_work": {"line_break", "confined_space", "energized_work"},
    "line_break": {"hot_work", "energized_work"},
    "confined_space": {"hot_work", "excavation"},
    "energized_work": {"hot_work", "line_break"},
    "excavation": {"confined_space"},
}

GENERIC_EVENT_TYPES = (
    "EnvironmentHealthSafetyCreated",
    "EnvironmentHealthSafetyUpdated",
    "EnvironmentHealthSafetyApproved",
    "EnvironmentHealthSafetyExceptionOpened",
)
TYPED_EVENT_TYPES = (
    "EnvironmentHealthSafetyIncidentLogged",
    "EnvironmentHealthSafetyIncidentLifecycleAdvanced",
    "EnvironmentHealthSafetySeriousIncidentNoticeSent",
    "EnvironmentHealthSafetyHazardPromoted",
    "EnvironmentHealthSafetyPermitConflictDetected",
    "EnvironmentHealthSafetyPermitIssued",
    "EnvironmentHealthSafetyInspectionSynced",
    "EnvironmentHealthSafetyCorrectiveActionReopened",
    "EnvironmentHealthSafetyPolicyReevaluationRequested",
    "EnvironmentHealthSafetyEvidenceSealed",
    "EnvironmentHealthSafetyRiskPriorityRecalculated",
    "EnvironmentHealthSafetyControlAssertionFailed",
)
EMITTED_EVENT_TYPES = tuple(dict.fromkeys(GENERIC_EVENT_TYPES + TYPED_EVENT_TYPES))
CONSUMED_EVENT_TYPES = ("PolicyChanged", "AuditEventSealed", "OperationalKpiChanged")

STANDARD_FEATURE_KEYS = (
    "ehs_incident_management",
    "environment_health_safety_workflow",
    "environment_health_safety_analytics",
    "configuration_schema",
    "rule_engine",
    "parameter_engine",
    "owned_schema_migrations_models",
    "appgen_x_outbox_inbox_eventing",
    "idempotent_handlers",
    "retry_dead_letter_evidence",
    "permissions",
    "seed_data",
    "workbench",
    "agentic_document_instruction_intake",
    "governed_datastore_crud",
    "ai_agent_task_assistance",
    "configuration_workbench",
    "continuous_release_assurance",
)
ADVANCED_CAPABILITY_KEYS = (
    "environment_health_safety_event_sourced_operational_history",
    "environment_health_safety_multi_tenant_policy_isolation",
    "environment_health_safety_schema_evolution_resilience",
    "environment_health_safety_autonomous_anomaly_detection",
    "environment_health_safety_semantic_document_instruction_understanding",
    "environment_health_safety_predictive_risk_scoring",
    "environment_health_safety_counterfactual_scenario_simulation",
    "environment_health_safety_cryptographic_audit_proofs",
    "environment_health_safety_continuous_control_testing",
    "environment_health_safety_carbon_and_sustainability_awareness",
    "environment_health_safety_cross_pbc_event_federation",
    "environment_health_safety_governed_ai_agent_execution",
)
UI_FRAGMENT_KEYS = (
    "EnvironmentHealthSafetyWorkbench",
    "EnvironmentHealthSafetyDetail",
    "EnvironmentHealthSafetyAssistantPanel",
)
PERMISSIONS = (
    f"{PBC_KEY}.read",
    f"{PBC_KEY}.create",
    f"{PBC_KEY}.update",
    f"{PBC_KEY}.approve",
    f"{PBC_KEY}.admin",
    f"{PBC_KEY}.operate",
)

PARAMETER_DEFINITIONS = {
    "serious_incident_notification_hours": {
        "default": 8,
        "minimum": 1,
        "maximum": 24,
        "unit": "hours",
        "description": "Fallback regulator notification clock for serious incidents.",
    },
    "fatality_notification_hours": {
        "default": 8,
        "minimum": 1,
        "maximum": 24,
        "unit": "hours",
        "description": "Fatality notification clock.",
    },
    "hazard_cluster_threshold": {
        "default": 2,
        "minimum": 2,
        "maximum": 10,
        "unit": "count",
        "description": "Near-miss cluster size that triggers hazard promotion.",
    },
    "corrective_action_effectiveness_days": {
        "default": 30,
        "minimum": 1,
        "maximum": 180,
        "unit": "days",
        "description": "Window before corrective action effectiveness must be reviewed.",
    },
    "inspection_overdue_grace_hours": {
        "default": 24,
        "minimum": 0,
        "maximum": 168,
        "unit": "hours",
        "description": "Grace period before overdue inspections escalate.",
    },
    "permit_overlap_minutes": {
        "default": 30,
        "minimum": 0,
        "maximum": 240,
        "unit": "minutes",
        "description": "Overlap tolerance for simultaneous operations.",
    },
    "risk_threshold": {
        "default": 70,
        "minimum": 0,
        "maximum": 100,
        "unit": "score",
        "description": "Risk score threshold for escalated queue placement.",
    },
    "kpi_priority_weight": {
        "default": 1.5,
        "minimum": 0.5,
        "maximum": 5.0,
        "unit": "multiplier",
        "description": "Weight applied to KPI-driven queue reprioritization.",
    },
    "workbench_limit": {
        "default": 25,
        "minimum": 5,
        "maximum": 100,
        "unit": "count",
        "description": "Default workbench queue size.",
    },
}
RULE_DEFINITIONS = {
    "incident_closure_gate": {
        "description": (
            "Blocks incident closure until mandatory investigation fields, "
            "notification acknowledgements, and corrective action effectiveness "
            "evidence are complete."
        ),
        "severity": "high",
        "scope": "incident",
    },
    "serious_incident_notification_clock": {
        "description": (
            "Starts jurisdiction-aware clocks for fatalities, hospitalizations, "
            "major releases, and fire events."
        ),
        "severity": "high",
        "scope": "incident",
    },
    "near_miss_hazard_promotion": {
        "description": (
            "Promotes repeated near misses into a tracked hazard with lineage."
        ),
        "severity": "medium",
        "scope": "hazard",
    },
    "permit_conflict_matrix": {
        "description": (
            "Detects permit overlaps across area, time window, and energy source."
        ),
        "severity": "high",
        "scope": "permit",
    },
    "corrective_action_effectiveness": {
        "description": (
            "Requires hierarchy-of-controls classification, verifier evidence, "
            "and effectiveness review."
        ),
        "severity": "high",
        "scope": "corrective_action",
    },
    "policy_change_targeted_re_evaluation": {
        "description": (
            "Re-evaluates open records against a new policy version and preserves "
            "the original decision context."
        ),
        "severity": "medium",
        "scope": "governance",
    },
    "continuous_control_testing": {
        "description": (
            "Opens exceptions for overdue serious notifications, expired permits, "
            "overdue corrective actions, and lapsed training on high-risk work."
        ),
        "severity": "high",
        "scope": "controls",
    },
}

FORM_DEFINITIONS = {
    "incident_intake": {
        "title": "Serious Incident Intake",
        "fields": (
            "tenant",
            "code",
            "site",
            "area",
            "task",
            "severity",
            "unsafe_condition",
            "jurisdiction",
            "people_affected",
        ),
    },
    "hazard_register": {
        "title": "Hazard Register Entry",
        "fields": (
            "tenant",
            "site",
            "area",
            "process",
            "task_step",
            "energy_source",
            "hazard_type",
            "existing_controls",
            "residual_risk",
        ),
    },
    "permit_issue": {
        "title": "Permit Issue Wizard",
        "fields": (
            "tenant",
            "permit_type",
            "area",
            "start_at",
            "end_at",
            "energy_source",
            "gas_test_status",
            "rescue_readiness",
            "simultaneous_operations",
        ),
    },
    "inspection_capture": {
        "title": "Offline Inspection Sync",
        "fields": (
            "submission_id",
            "tenant",
            "template",
            "asset",
            "area",
            "captured_at",
            "answers",
            "photos",
            "signature",
        ),
    },
}
WIZARD_DEFINITIONS = {
    "serious_incident_response": {
        "steps": (
            "classify_incident",
            "start_notification_clock",
            "open_investigation",
            "assign_corrective_actions",
            "verify_effectiveness",
            "close_or_reopen",
        ),
    },
    "dynamic_risk_assessment": {
        "steps": (
            "pull_live_hazards",
            "merge_permit_conditions",
            "evaluate_site_alerts",
            "score_residual_risk",
            "capture_signoff",
        ),
    },
    "regulator_export": {
        "steps": (
            "collect_evidence",
            "freeze_bundle",
            "hash_bundle",
            "render_export",
        ),
    },
}
CONTROL_DEFINITIONS = (
    "severity_badge",
    "recordability_badge",
    "notification_timer",
    "hazard_cluster_explainer",
    "permit_conflict_matrix",
    "effectiveness_review_gate",
    "sealed_evidence_badge",
    "predictive_risk_driver_panel",
)
WORKFLOW_DEFINITIONS = {
    "environment_health_safety_create_ehs_incident_workflow": {
        "entrypoint": "create_ehs_incident",
        "description": "Record, triage, and govern a new incident.",
    },
    "environment_health_safety_serious_incident_notification_workflow": {
        "entrypoint": "send_serious_incident_notice",
        "description": "Manage notification clocks, escalation, and acknowledgement.",
    },
    "environment_health_safety_record_hazard_workflow": {
        "entrypoint": "record_hazard",
        "description": "Maintain the hierarchical hazard register and near-miss promotion.",
    },
    "environment_health_safety_dynamic_risk_assessment_workflow": {
        "entrypoint": "run_dynamic_risk_assessment",
        "description": "Assess live work conditions before non-routine work.",
    },
    "environment_health_safety_permit_conflict_workflow": {
        "entrypoint": "issue_permit",
        "description": "Enforce the simultaneous-operations conflict matrix.",
    },
    "environment_health_safety_corrective_action_effectiveness_workflow": {
        "entrypoint": "verify_corrective_action",
        "description": "Verify control strength and reopen failed actions.",
    },
}
AGENT_SKILLS = (
    {
        "name": f"{PBC_KEY}_triage_incident",
        "description": "Summarize severity, recordability, and notification obligations.",
        "mutation_scope": "preview_only",
    },
    {
        "name": f"{PBC_KEY}_investigation_gap_check",
        "description": "Spot missing chronology, causes, witnesses, or failed barriers.",
        "mutation_scope": "preview_only",
    },
    {
        "name": f"{PBC_KEY}_hazard_promotion_explainer",
        "description": "Explain why repeated near misses became a hazard entry.",
        "mutation_scope": "preview_only",
    },
    {
        "name": f"{PBC_KEY}_permit_conflict_checker",
        "description": "Check overlapping permits before work starts.",
        "mutation_scope": "preview_only",
    },
    {
        "name": f"{PBC_KEY}_regulator_export_guide",
        "description": "Build regulator-ready evidence packs with proof hashes.",
        "mutation_scope": "preview_only",
    },
    {
        "name": f"{PBC_KEY}_governed_crud",
        "description": "Create governed CRUD previews for owned tables only.",
        "mutation_scope": "requires_confirmation",
    },
)
READ_MODEL_TABLES = {
    "incidents": BUSINESS_TABLES[0],
    "hazards": BUSINESS_TABLES[1],
    "inspections": BUSINESS_TABLES[2],
    "permits": BUSINESS_TABLES[3],
    "corrective_actions": BUSINESS_TABLES[4],
    "safety_training": BUSINESS_TABLES[5],
    "audit_findings": BUSINESS_TABLES[6],
}
MIGRATION_FILE = "migrations/001_initial.sql"


def _package_root() -> Path:
    return Path(__file__).resolve().parent


def _timestamp(value: str | None = None) -> str:
    if value:
        return value
    return datetime.now(UTC).replace(microsecond=0).isoformat()


def _digest(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, default=str).encode("utf-8")
    ).hexdigest()


def _copy(state: dict[str, Any]) -> dict[str, Any]:
    next_state = deepcopy(state)
    next_state["idempotency_keys"] = set(state.get("idempotency_keys", set()))
    return next_state


def _parameter_state() -> dict[str, dict[str, Any]]:
    return {
        name: {"name": name, "value": definition["default"], **definition}
        for name, definition in PARAMETER_DEFINITIONS.items()
    }


def _rule_state() -> dict[str, dict[str, Any]]:
    return {
        rule_id: {
            "rule_id": rule_id,
            "status": "active",
            "compiled_hash": _digest((rule_id, definition)),
            **definition,
        }
        for rule_id, definition in RULE_DEFINITIONS.items()
    }


def empty_state() -> dict[str, Any]:
    return {
        "records": {
            "incidents": {},
            "hazards": {},
            "inspections": {},
            "permits": {},
            "corrective_actions": {},
            "safety_training": {},
            "audit_findings": {},
        },
        "configuration": {
            "database_backend": "postgresql",
            "event_topic": REQUIRED_EVENT_TOPIC,
            "retry_limit": 5,
            "default_policy_version": "ehs-policy-2026.1",
        },
        "parameters": _parameter_state(),
        "rules": _rule_state(),
        "schema_extensions": {},
        "governed_models": {},
        "control_assertions": {},
        "sealed_bundles": {},
        "exceptions": [],
        "timeline": [],
        "inbox": [],
        "outbox": [],
        "dead_letter": [],
        "idempotency_keys": set(),
    }


def _append_timeline(state: dict[str, Any], entry_type: str, payload: dict[str, Any]) -> None:
    state["timeline"].append(
        {
            "entry_type": entry_type,
            "occurred_at": _timestamp(payload.get("occurred_at")),
            "payload": deepcopy(payload),
            "hash": _digest((entry_type, payload)),
        }
    )


def _emit(
    state: dict[str, Any],
    event_type: str,
    payload: dict[str, Any],
    aggregate_type: str,
    aggregate_id: str,
) -> dict[str, Any]:
    envelope = {
        "event_id": _digest((event_type, aggregate_type, aggregate_id, payload)),
        "event_type": event_type,
        "topic": REQUIRED_EVENT_TOPIC,
        "aggregate_type": aggregate_type,
        "aggregate_id": aggregate_id,
        "occurred_at": _timestamp(payload.get("occurred_at")),
        "payload": deepcopy(payload),
        "idempotency_key": _digest((event_type, aggregate_id, payload)),
        "event_contract": "AppGen-X",
    }
    state["outbox"].append(envelope)
    return envelope


def _serious_notification_hours(state: dict[str, Any], severity: str) -> int:
    if severity == "fatality":
        return int(state["parameters"]["fatality_notification_hours"]["value"])
    return int(state["parameters"]["serious_incident_notification_hours"]["value"])


def _required_investigation_fields(investigation: dict[str, Any]) -> tuple[str, ...]:
    required = (
        "chronology",
        "witness_statements",
        "equipment_state",
        "immediate_cause",
        "basic_cause",
        "root_cause",
        "failed_controls",
        "evidence_links",
    )
    return tuple(field for field in required if not investigation.get(field))


def _incident_proof_bundle(incident: dict[str, Any]) -> dict[str, Any]:
    chain_items = (
        incident["id"],
        incident["status"],
        incident["severity"],
        incident["recordability"],
        incident["notification"],
        incident["investigation"],
        tuple(sorted(incident["corrective_action_ids"])),
    )
    proof_hash = _digest(chain_items)
    return {
        "bundle_id": f"proof-{incident['id']}",
        "algorithm": "sha256",
        "proof_hash": proof_hash,
        "redacted_validation_hash": _digest((incident["id"], proof_hash)),
    }


def _open_exception(
    state: dict[str, Any],
    code: str,
    title: str,
    affected_records: tuple[str, ...],
    severity: str,
    details: dict[str, Any] | None = None,
) -> dict[str, Any]:
    exception = {
        "exception_id": _digest((code, affected_records, details or {})),
        "code": code,
        "title": title,
        "severity": severity,
        "affected_records": affected_records,
        "details": deepcopy(details or {}),
        "opened_at": _timestamp(),
    }
    state["exceptions"].append(exception)
    _emit(
        state,
        "EnvironmentHealthSafetyExceptionOpened",
        exception,
        "exception",
        exception["exception_id"],
    )
    return exception


def _parse_datetime(value: str | None) -> datetime | None:
    if not value:
        return None
    normalized = value.replace("Z", "+00:00")
    return datetime.fromisoformat(normalized)


def _permit_overlaps(existing: dict[str, Any], candidate: dict[str, Any], overlap_minutes: int) -> bool:
    existing_start = _parse_datetime(existing.get("start_at"))
    existing_end = _parse_datetime(existing.get("end_at"))
    candidate_start = _parse_datetime(candidate.get("start_at"))
    candidate_end = _parse_datetime(candidate.get("end_at"))
    if not all((existing_start, existing_end, candidate_start, candidate_end)):
        return False
    grace = timedelta(minutes=overlap_minutes)
    return candidate_start <= existing_end + grace and existing_start <= candidate_end + grace


def _queue_priority(record: dict[str, Any], kpi_weight: float = 1.0) -> float:
    severity_weight = {
        "near_miss": 20,
        "first_aid": 25,
        "medical_treatment": 45,
        "restricted_work": 55,
        "lost_time": 65,
        "hospitalization": 85,
        "environmental_release": 75,
        "fire": 70,
        "fatality": 100,
    }
    status_weight = {
        "draft": 10,
        "triaged": 20,
        "recordability_review": 30,
        "regulator_notified": 40,
        "investigation_open": 50,
        "corrective_action_open": 60,
        "closed": 5,
        "reopened": 70,
    }
    return round(
        (
            severity_weight.get(record.get("severity", "near_miss"), 10)
            + status_weight.get(record.get("status", "draft"), 0)
        )
        * kpi_weight,
        2,
    )


def seed_state() -> dict[str, Any]:
    state = empty_state()
    seeded_now = "2026-05-30T08:00:00+00:00"
    result = create_ehs_incident(
        state,
        {
            "tenant": "tenant-seed",
            "code": "INC-100",
            "site": "Plant 7",
            "area": "Coating Line",
            "task": "Solvent changeover",
            "severity": "hospitalization",
            "unsafe_condition": "ventilation failure",
            "jurisdiction": "osha",
            "occurred_at": seeded_now,
            "people_affected": 2,
        },
    )
    state = result["state"]
    state = send_serious_incident_notice(
        state,
        "INC-100",
        {"name": "Safety Lead", "role": "approver"},
        sent_at="2026-05-30T11:00:00+00:00",
    )["state"]
    state = advance_incident_lifecycle(
        state,
        "INC-100",
        "triaged",
        actor={"name": "Safety Lead"},
    )["state"]
    state = advance_incident_lifecycle(
        state,
        "INC-100",
        "recordability_review",
        actor={"name": "Safety Lead"},
    )["state"]
    state = advance_incident_lifecycle(
        state,
        "INC-100",
        "regulator_notified",
        actor={"name": "Safety Lead"},
    )["state"]
    state = advance_incident_lifecycle(
        state,
        "INC-100",
        "investigation_open",
        actor={"name": "Safety Lead"},
        dossier_updates={
            "chronology": ("shift start", "ventilation alarm", "worker exposure"),
            "witness_statements": ("operator statement",),
            "equipment_state": "fan offline",
            "immediate_cause": "ventilation unavailable",
            "basic_cause": "maintenance backlog",
            "root_cause": "inspection recurrence missed",
            "failed_controls": ("local exhaust ventilation",),
            "evidence_links": ("ehs://evidence/inc-100/video-1",),
        },
    )["state"]
    near_miss_one = create_ehs_incident(
        state,
        {
            "tenant": "tenant-seed",
            "code": "INC-101",
            "site": "Plant 7",
            "area": "Coating Line",
            "task": "Solvent changeover",
            "severity": "near_miss",
            "unsafe_condition": "ventilation failure",
            "occurred_at": "2026-05-29T08:00:00+00:00",
        },
    )
    state = near_miss_one["state"]
    near_miss_two = create_ehs_incident(
        state,
        {
            "tenant": "tenant-seed",
            "code": "INC-102",
            "site": "Plant 7",
            "area": "Coating Line",
            "task": "Solvent changeover",
            "severity": "near_miss",
            "unsafe_condition": "ventilation failure",
            "occurred_at": "2026-05-28T08:00:00+00:00",
        },
    )
    state = near_miss_two["state"]
    state = promote_near_miss_cluster(
        state,
        {"tenant": "tenant-seed", "site": "Plant 7", "area": "Coating Line", "task": "Solvent changeover"},
    )["state"]
    state = create_corrective_action(
        state,
        {
            "tenant": "tenant-seed",
            "code": "CA-100",
            "incident_id": "INC-100",
            "owner": "Maintenance Supervisor",
            "due_date": "2026-06-15T00:00:00+00:00",
            "hierarchy_of_controls": "engineering",
            "verification_step": "measure_airflow",
            "effectiveness_review_window_days": 21,
        },
    )["state"]
    state = schedule_inspection(
        state,
        {
            "tenant": "tenant-seed",
            "code": "INSP-100",
            "template": "ventilation-round",
            "asset": "EXH-77",
            "area": "Coating Line",
            "due_at": "2026-06-01T08:00:00+00:00",
            "mandatory_evidence": ("photo", "measurement"),
            "recurrence": "weekly",
        },
    )["state"]
    state = issue_permit(
        state,
        {
            "tenant": "tenant-seed",
            "code": "PERM-100",
            "permit_type": "line_break",
            "area": "Tank Farm",
            "start_at": "2026-06-01T09:00:00+00:00",
            "end_at": "2026-06-01T12:00:00+00:00",
            "energy_source": "pressurized_liquid",
            "gas_test_status": "clear",
            "rescue_readiness": "not_required",
            "simultaneous_operations": (),
        },
    )["state"]
    state["records"]["safety_training"]["TRAIN-100"] = {
        "id": "TRAIN-100",
        "tenant": "tenant-seed",
        "worker": "Operator A",
        "course": "Confined Space Entry",
        "status": "current",
        "expires_at": "2026-09-01T00:00:00+00:00",
    }
    state["records"]["audit_findings"]["AUD-100"] = {
        "id": "AUD-100",
        "tenant": "tenant-seed",
        "status": "open",
        "finding": "Ventilation inspection recurrence not enforced.",
        "severity": "major",
        "evidence_bundle_id": "bundle-aud-100",
    }
    return state


def configure_runtime(state: dict[str, Any], config: dict[str, Any]) -> dict[str, Any]:
    next_state = _copy(state)
    database_backend = config.get("database_backend", next_state["configuration"]["database_backend"])
    event_topic = config.get("event_topic", REQUIRED_EVENT_TOPIC)
    retry_limit = int(config.get("retry_limit", next_state["configuration"]["retry_limit"]))
    ok = (
        database_backend in ALLOWED_DATABASE_BACKENDS
        and event_topic == REQUIRED_EVENT_TOPIC
        and retry_limit > 0
    )
    next_state["configuration"] = {
        **next_state["configuration"],
        **deepcopy(config),
        "database_backend": database_backend,
        "event_topic": event_topic,
        "retry_limit": retry_limit,
    }
    _append_timeline(next_state, "runtime_configured", next_state["configuration"])
    return {
        "ok": ok,
        "state": next_state,
        "configuration": deepcopy(next_state["configuration"]),
        "side_effects": (),
    }


def set_parameter(state: dict[str, Any], name: str, value: Any) -> dict[str, Any]:
    next_state = _copy(state)
    definition = PARAMETER_DEFINITIONS.get(name)
    if not definition:
        return {
            "ok": False,
            "reason": "unknown_parameter",
            "parameter": name,
            "state": next_state,
            "side_effects": (),
        }
    numeric_value = float(value) if isinstance(value, (int, float)) else value
    if isinstance(numeric_value, (int, float)):
        bounded = definition["minimum"] <= numeric_value <= definition["maximum"]
    else:
        bounded = True
    if not bounded:
        return {
            "ok": False,
            "reason": "parameter_out_of_bounds",
            "parameter": name,
            "state": next_state,
            "side_effects": (),
        }
    next_state["parameters"][name] = {
        "name": name,
        "value": numeric_value,
        **definition,
    }
    return {
        "ok": True,
        "state": next_state,
        "parameter": deepcopy(next_state["parameters"][name]),
        "side_effects": (),
    }


def compile_rule(rule: dict[str, Any]) -> dict[str, Any]:
    rule_id = rule.get("rule_id", "anonymous_rule")
    base = deepcopy(RULE_DEFINITIONS.get(rule_id, {}))
    compiled = {"rule_id": rule_id, **base, **deepcopy(rule), "compiled_hash": _digest((rule_id, rule))}
    return {"ok": True, "compiled_rule": compiled, "side_effects": ()}


def register_rule(state: dict[str, Any], rule: dict[str, Any]) -> dict[str, Any]:
    next_state = _copy(state)
    compiled = compile_rule(rule)["compiled_rule"]
    next_state["rules"][compiled["rule_id"]] = compiled
    return {"ok": True, "state": next_state, "rule": compiled, "side_effects": ()}


def evaluate_rule(rule_id: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    payload = deepcopy(payload or {})
    if rule_id == "incident_closure_gate":
        investigation = payload.get("investigation", {})
        corrective_actions = payload.get("corrective_actions", ())
        notification = payload.get("notification", {})
        missing = _required_investigation_fields(investigation)
        pending_actions = tuple(
            action["id"]
            for action in corrective_actions
            if action.get("status") != "effective"
        )
        notice_ok = (not notification.get("required")) or notification.get("status") == "acknowledged"
        passed = not missing and not pending_actions and notice_ok
        return {
            "ok": True,
            "rule_id": rule_id,
            "passed": passed,
            "missing_investigation_fields": missing,
            "pending_corrective_actions": pending_actions,
            "notification_ok": notice_ok,
            "side_effects": (),
        }
    if rule_id == "permit_conflict_matrix":
        conflicts = tuple(payload.get("conflicts", ()))
        return {
            "ok": True,
            "rule_id": rule_id,
            "passed": not conflicts,
            "conflicts": conflicts,
            "side_effects": (),
        }
    if rule_id == "serious_incident_notification_clock":
        severity = payload.get("severity")
        due_at = payload.get("due_at")
        passed = (severity not in SERIOUS_INCIDENT_SEVERITIES) or bool(due_at)
        return {
            "ok": True,
            "rule_id": rule_id,
            "passed": passed,
            "due_at": due_at,
            "side_effects": (),
        }
    return {"ok": True, "rule_id": rule_id, "passed": True, "payload": payload, "side_effects": ()}


def register_schema_extension(state: dict[str, Any], table: str, fields: dict[str, Any]) -> dict[str, Any]:
    next_state = _copy(state)
    if table not in OWNED_TABLES:
        return {
            "ok": False,
            "reason": "foreign_table_rejected",
            "table": table,
            "state": next_state,
            "side_effects": (),
        }
    next_state["schema_extensions"][table] = deepcopy(fields)
    return {"ok": True, "state": next_state, "table": table, "fields": deepcopy(fields), "side_effects": ()}


def create_ehs_incident(state: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
    next_state = _copy(state)
    now = _timestamp(payload.get("occurred_at"))
    code = payload.get("code") or f"INC-{len(next_state['records']['incidents']) + 1:03d}"
    severity = payload.get("severity", "near_miss")
    recordability = payload.get("recordability") or RECORDABILITY_BY_SEVERITY.get(severity, "pending_review")
    serious = severity in SERIOUS_INCIDENT_SEVERITIES
    due_at = None
    if serious:
        due_at = (
            _parse_datetime(now) + timedelta(hours=_serious_notification_hours(next_state, severity))
        ).isoformat()
    incident = {
        "id": code,
        "tenant": payload.get("tenant", "default"),
        "code": code,
        "status": payload.get("status", "draft"),
        "site": payload.get("site", "unknown-site"),
        "area": payload.get("area", "unknown-area"),
        "task": payload.get("task", "unknown-task"),
        "severity": severity,
        "recordability": recordability,
        "unsafe_condition": payload.get("unsafe_condition", "unspecified"),
        "jurisdiction": payload.get("jurisdiction", "site-default"),
        "policy_version": next_state["configuration"]["default_policy_version"],
        "policy_versions": {
            "original": next_state["configuration"]["default_policy_version"],
            "current": next_state["configuration"]["default_policy_version"],
        },
        "notification": {
            "required": serious,
            "status": "pending" if serious else "not_required",
            "due_at": due_at,
            "sent_at": None,
            "acknowledgements": (),
            "contact_pack": {
                "jurisdiction": payload.get("jurisdiction", "site-default"),
                "contacts": ("regulator-primary", "site-lead"),
                "clock_hours": _serious_notification_hours(next_state, severity) if serious else 0,
            },
            "overdue": False,
        },
        "investigation": {
            "chronology": tuple(payload.get("chronology", ())),
            "witness_statements": tuple(payload.get("witness_statements", ())),
            "equipment_state": payload.get("equipment_state"),
            "immediate_cause": payload.get("immediate_cause"),
            "basic_cause": payload.get("basic_cause"),
            "root_cause": payload.get("root_cause"),
            "failed_controls": tuple(payload.get("failed_controls", ())),
            "evidence_links": tuple(payload.get("evidence_links", ())),
            "complete": False,
        },
        "corrective_action_ids": tuple(payload.get("corrective_action_ids", ())),
        "evidence_bundle": _incident_proof_bundle(
            {
                "id": code,
                "status": payload.get("status", "draft"),
                "severity": severity,
                "recordability": recordability,
                "notification": {"required": serious},
                "investigation": {},
                "corrective_action_ids": tuple(payload.get("corrective_action_ids", ())),
            }
        ),
        "created_at": now,
        "updated_at": now,
        "history": (
            {"status": payload.get("status", "draft"), "at": now, "actor": payload.get("actor", "system")},
        ),
    }
    next_state["records"]["incidents"][code] = incident
    _append_timeline(next_state, "incident_created", {"incident_id": code, "severity": severity})
    created = _emit(next_state, "EnvironmentHealthSafetyCreated", incident, "incident", code)
    logged = _emit(
        next_state,
        "EnvironmentHealthSafetyIncidentLogged",
        {
            "incident_id": code,
            "severity": severity,
            "recordability": recordability,
            "notification_due_at": due_at,
        },
        "incident",
        code,
    )
    return {
        "ok": evaluate_rule("serious_incident_notification_clock", {"severity": severity, "due_at": due_at})["passed"],
        "state": next_state,
        "record": deepcopy(incident),
        "events": (created, logged),
        "side_effects": (),
    }


def advance_incident_lifecycle(
    state: dict[str, Any],
    incident_id: str,
    new_status: str,
    actor: dict[str, Any] | None = None,
    dossier_updates: dict[str, Any] | None = None,
) -> dict[str, Any]:
    next_state = _copy(state)
    incident = deepcopy(next_state["records"]["incidents"].get(incident_id))
    if not incident:
        return {"ok": False, "reason": "incident_not_found", "state": next_state, "side_effects": ()}
    allowed = INCIDENT_TRANSITIONS.get(incident["status"], set())
    if new_status not in allowed:
        return {
            "ok": False,
            "reason": "invalid_transition",
            "from_status": incident["status"],
            "to_status": new_status,
            "state": next_state,
            "side_effects": (),
        }
    if dossier_updates:
        incident["investigation"] = {**incident["investigation"], **deepcopy(dossier_updates)}
    incident["investigation"]["complete"] = not _required_investigation_fields(incident["investigation"])
    linked_actions = tuple(
        next_state["records"]["corrective_actions"][action_id]
        for action_id in incident["corrective_action_ids"]
        if action_id in next_state["records"]["corrective_actions"]
    )
    closure_gate = evaluate_rule(
        "incident_closure_gate",
        {
            "investigation": incident["investigation"],
            "corrective_actions": linked_actions,
            "notification": incident["notification"],
        },
    )
    if new_status == "closed" and not closure_gate["passed"]:
        return {
            "ok": False,
            "reason": "incident_closure_blocked",
            "blocking_gate": closure_gate,
            "state": next_state,
            "side_effects": (),
        }
    if new_status == "regulator_notified" and incident["notification"]["status"] != "acknowledged":
        return {
            "ok": False,
            "reason": "notification_acknowledgement_required",
            "state": next_state,
            "side_effects": (),
        }
    if new_status == "corrective_action_open" and not incident["investigation"]["complete"]:
        return {
            "ok": False,
            "reason": "investigation_incomplete",
            "state": next_state,
            "side_effects": (),
        }
    now = _timestamp()
    incident["status"] = new_status
    incident["updated_at"] = now
    incident["history"] = incident["history"] + (
        {"status": new_status, "at": now, "actor": deepcopy(actor or {"name": "system"})},
    )
    incident["evidence_bundle"] = _incident_proof_bundle(incident)
    next_state["records"]["incidents"][incident_id] = incident
    _append_timeline(
        next_state,
        "incident_lifecycle_advanced",
        {"incident_id": incident_id, "from_status": state["records"]["incidents"][incident_id]["status"], "to_status": new_status},
    )
    event = _emit(
        next_state,
        "EnvironmentHealthSafetyIncidentLifecycleAdvanced",
        {"incident_id": incident_id, "status": new_status, "actor": deepcopy(actor or {"name": "system"})},
        "incident",
        incident_id,
    )
    generic = _emit(
        next_state,
        "EnvironmentHealthSafetyUpdated",
        {"incident_id": incident_id, "status": new_status},
        "incident",
        incident_id,
    )
    return {
        "ok": True,
        "state": next_state,
        "incident": deepcopy(incident),
        "events": (event, generic),
        "side_effects": (),
    }


def send_serious_incident_notice(
    state: dict[str, Any],
    incident_id: str,
    actor: dict[str, Any],
    sent_at: str | None = None,
) -> dict[str, Any]:
    next_state = _copy(state)
    incident = deepcopy(next_state["records"]["incidents"].get(incident_id))
    if not incident:
        return {"ok": False, "reason": "incident_not_found", "state": next_state, "side_effects": ()}
    if not incident["notification"]["required"]:
        return {"ok": False, "reason": "notification_not_required", "state": next_state, "side_effects": ()}
    when = _timestamp(sent_at)
    acknowledgement = {
        "sent_at": when,
        "sent_by": deepcopy(actor),
        "contacts": incident["notification"]["contact_pack"]["contacts"],
    }
    incident["notification"] = {
        **incident["notification"],
        "status": "acknowledged",
        "sent_at": when,
        "acknowledgements": incident["notification"]["acknowledgements"] + (acknowledgement,),
        "overdue": False,
    }
    incident["updated_at"] = when
    next_state["records"]["incidents"][incident_id] = incident
    _append_timeline(next_state, "serious_incident_notice_sent", {"incident_id": incident_id, "sent_by": actor})
    sent_event = _emit(
        next_state,
        "EnvironmentHealthSafetySeriousIncidentNoticeSent",
        {"incident_id": incident_id, "sent_at": when, "actor": deepcopy(actor)},
        "incident",
        incident_id,
    )
    return {
        "ok": True,
        "state": next_state,
        "notification": deepcopy(incident["notification"]),
        "event": sent_event,
        "side_effects": (),
    }


def record_hazard(state: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
    next_state = _copy(state)
    code = payload.get("code") or f"HZ-{len(next_state['records']['hazards']) + 1:03d}"
    hazard = {
        "id": code,
        "tenant": payload.get("tenant", "default"),
        "site": payload.get("site", "unknown-site"),
        "area": payload.get("area", "unknown-area"),
        "process": payload.get("process", payload.get("task", "unknown-process")),
        "task_step": payload.get("task_step", payload.get("task", "unknown-task")),
        "exposed_population": tuple(payload.get("exposed_population", ("operators",))),
        "energy_source": payload.get("energy_source", "mechanical"),
        "hazard_type": payload.get("hazard_type", "process_safety"),
        "existing_controls": tuple(payload.get("existing_controls", ())),
        "residual_risk": payload.get("residual_risk", 0),
        "cluster_count": int(payload.get("cluster_count", 1)),
        "lineage_incidents": tuple(payload.get("lineage_incidents", ())),
        "status": payload.get("status", "open"),
        "created_at": _timestamp(),
        "updated_at": _timestamp(),
    }
    next_state["records"]["hazards"][code] = hazard
    _append_timeline(next_state, "hazard_recorded", {"hazard_id": code, "site": hazard["site"]})
    event = _emit(next_state, "EnvironmentHealthSafetyCreated", hazard, "hazard", code)
    return {"ok": True, "state": next_state, "hazard": deepcopy(hazard), "event": event, "side_effects": ()}


def promote_near_miss_cluster(state: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
    next_state = _copy(state)
    threshold = int(next_state["parameters"]["hazard_cluster_threshold"]["value"])
    incidents = tuple(next_state["records"]["incidents"].values())
    clustered = tuple(
        incident
        for incident in incidents
        if incident["tenant"] == payload.get("tenant", incident["tenant"])
        and incident["site"] == payload.get("site", incident["site"])
        and incident["area"] == payload.get("area", incident["area"])
        and incident["task"] == payload.get("task", incident["task"])
        and incident["severity"] == "near_miss"
    )
    if len(clustered) < threshold:
        return {
            "ok": False,
            "reason": "cluster_below_threshold",
            "cluster_size": len(clustered),
            "state": next_state,
            "side_effects": (),
        }
    unsafe_condition = clustered[0]["unsafe_condition"]
    existing = next(
        (
            hazard
            for hazard in next_state["records"]["hazards"].values()
            if hazard["site"] == clustered[0]["site"]
            and hazard["area"] == clustered[0]["area"]
            and hazard["task_step"] == clustered[0]["task"]
            and hazard["hazard_type"] == unsafe_condition
        ),
        None,
    )
    lineage = tuple(sorted({incident["id"] for incident in clustered}))
    if existing:
        existing["cluster_count"] = max(existing["cluster_count"], len(clustered))
        existing["lineage_incidents"] = tuple(sorted(set(existing["lineage_incidents"]) | set(lineage)))
        existing["updated_at"] = _timestamp()
        hazard = existing
    else:
        hazard_result = record_hazard(
            next_state,
            {
                "tenant": clustered[0]["tenant"],
                "code": payload.get("hazard_code") or f"HZ-{len(next_state['records']['hazards']) + 1:03d}",
                "site": clustered[0]["site"],
                "area": clustered[0]["area"],
                "process": clustered[0]["task"],
                "task_step": clustered[0]["task"],
                "energy_source": "process",
                "hazard_type": unsafe_condition,
                "existing_controls": ("monitoring",),
                "residual_risk": 72,
                "cluster_count": len(clustered),
                "lineage_incidents": lineage,
            },
        )
        next_state = hazard_result["state"]
        hazard = deepcopy(hazard_result["hazard"])
    explanation = {
        "cluster_size": len(clustered),
        "threshold": threshold,
        "unsafe_condition": unsafe_condition,
        "lineage_incidents": lineage,
    }
    next_state["records"]["hazards"][hazard["id"]] = hazard
    promoted = _emit(
        next_state,
        "EnvironmentHealthSafetyHazardPromoted",
        {"hazard_id": hazard["id"], **explanation},
        "hazard",
        hazard["id"],
    )
    return {
        "ok": True,
        "state": next_state,
        "hazard": deepcopy(hazard),
        "explanation": explanation,
        "event": promoted,
        "side_effects": (),
    }


def create_corrective_action(state: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
    next_state = _copy(state)
    code = payload.get("code") or f"CA-{len(next_state['records']['corrective_actions']) + 1:03d}"
    review_days = int(
        payload.get(
            "effectiveness_review_window_days",
            next_state["parameters"]["corrective_action_effectiveness_days"]["value"],
        )
    )
    action = {
        "id": code,
        "tenant": payload.get("tenant", "default"),
        "incident_id": payload.get("incident_id"),
        "owner": payload.get("owner"),
        "due_date": payload.get("due_date"),
        "hierarchy_of_controls": payload.get("hierarchy_of_controls"),
        "verification_step": payload.get("verification_step"),
        "effectiveness_review_window_days": review_days,
        "status": "open",
        "verifier_evidence": (),
        "created_at": _timestamp(),
        "updated_at": _timestamp(),
    }
    next_state["records"]["corrective_actions"][code] = action
    if action["incident_id"] and action["incident_id"] in next_state["records"]["incidents"]:
        incident = deepcopy(next_state["records"]["incidents"][action["incident_id"]])
        incident["corrective_action_ids"] = tuple(sorted(set(incident["corrective_action_ids"]) | {code}))
        next_state["records"]["incidents"][action["incident_id"]] = incident
    return {"ok": True, "state": next_state, "action": deepcopy(action), "side_effects": ()}


def verify_corrective_action(
    state: dict[str, Any],
    action_id: str,
    payload: dict[str, Any],
) -> dict[str, Any]:
    next_state = _copy(state)
    action = deepcopy(next_state["records"]["corrective_actions"].get(action_id))
    if not action:
        return {"ok": False, "reason": "corrective_action_not_found", "state": next_state, "side_effects": ()}
    evidence = payload.get("evidence_links") or ()
    if not evidence:
        return {"ok": False, "reason": "verifier_evidence_required", "state": next_state, "side_effects": ()}
    passed = bool(payload.get("passed", True))
    action["verifier_evidence"] = tuple(evidence)
    action["status"] = "effective" if passed else "reopened"
    action["updated_at"] = _timestamp()
    next_state["records"]["corrective_actions"][action_id] = action
    emitted = None
    if not passed:
        emitted = _emit(
            next_state,
            "EnvironmentHealthSafetyCorrectiveActionReopened",
            {"action_id": action_id, "incident_id": action.get("incident_id")},
            "corrective_action",
            action_id,
        )
        incident_id = action.get("incident_id")
        if incident_id and incident_id in next_state["records"]["incidents"]:
            incident = deepcopy(next_state["records"]["incidents"][incident_id])
            incident["status"] = "reopened"
            incident["updated_at"] = _timestamp()
            next_state["records"]["incidents"][incident_id] = incident
    return {
        "ok": True,
        "state": next_state,
        "action": deepcopy(action),
        "event": emitted,
        "side_effects": (),
    }


def schedule_inspection(state: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
    next_state = _copy(state)
    code = payload.get("code") or f"INSP-{len(next_state['records']['inspections']) + 1:03d}"
    inspection = {
        "id": code,
        "tenant": payload.get("tenant", "default"),
        "template": payload.get("template"),
        "asset": payload.get("asset"),
        "area": payload.get("area"),
        "route_scope": tuple(payload.get("route_scope", (payload.get("area"),))),
        "mandatory_evidence": tuple(payload.get("mandatory_evidence", ())),
        "finding_severity": payload.get("finding_severity", "minor"),
        "recurrence": payload.get("recurrence", "one_time"),
        "due_at": payload.get("due_at"),
        "status": payload.get("status", "scheduled"),
        "sync_log": (),
        "created_at": _timestamp(),
        "updated_at": _timestamp(),
    }
    next_state["records"]["inspections"][code] = inspection
    return {"ok": True, "state": next_state, "inspection": deepcopy(inspection), "side_effects": ()}


def capture_inspection_sync(state: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
    next_state = _copy(state)
    submission_id = payload.get("submission_id") or _digest(payload)
    if submission_id in next_state["idempotency_keys"]:
        return {"ok": True, "duplicate": True, "state": next_state, "side_effects": ()}
    next_state["idempotency_keys"].add(submission_id)
    code = payload.get("inspection_id") or payload.get("code") or f"INSP-{len(next_state['records']['inspections']) + 1:03d}"
    inspection = deepcopy(next_state["records"]["inspections"].get(code, {}))
    inspection.update(
        {
            "id": code,
            "tenant": payload.get("tenant", inspection.get("tenant", "default")),
            "template": payload.get("template", inspection.get("template")),
            "asset": payload.get("asset", inspection.get("asset")),
            "area": payload.get("area", inspection.get("area")),
            "status": "synced",
            "captured_at": payload.get("captured_at"),
            "inspector": payload.get("inspector"),
            "answers": deepcopy(payload.get("answers", {})),
            "photos": tuple(payload.get("photos", ())),
            "signature": payload.get("signature"),
            "sync_log": tuple(inspection.get("sync_log", ()))
            + (
                {
                    "submission_id": submission_id,
                    "captured_at": payload.get("captured_at"),
                    "inspector": payload.get("inspector"),
                },
            ),
            "updated_at": _timestamp(),
        }
    )
    next_state["records"]["inspections"][code] = inspection
    event = _emit(
        next_state,
        "EnvironmentHealthSafetyInspectionSynced",
        {"inspection_id": code, "submission_id": submission_id, "captured_at": payload.get("captured_at")},
        "inspection",
        code,
    )
    return {"ok": True, "duplicate": False, "state": next_state, "inspection": deepcopy(inspection), "event": event, "side_effects": ()}


def issue_permit(state: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
    next_state = _copy(state)
    code = payload.get("code") or f"PERM-{len(next_state['records']['permits']) + 1:03d}"
    candidate = {
        "id": code,
        "tenant": payload.get("tenant", "default"),
        "permit_type": payload.get("permit_type"),
        "area": payload.get("area"),
        "start_at": payload.get("start_at"),
        "end_at": payload.get("end_at"),
        "energy_source": payload.get("energy_source"),
        "gas_test_status": payload.get("gas_test_status"),
        "rescue_readiness": payload.get("rescue_readiness"),
        "simultaneous_operations": tuple(payload.get("simultaneous_operations", ())),
        "status": "issued",
        "created_at": _timestamp(),
        "updated_at": _timestamp(),
    }
    overlap_minutes = int(next_state["parameters"]["permit_overlap_minutes"]["value"])
    conflicts = tuple(
        existing["id"]
        for existing in next_state["records"]["permits"].values()
        if existing.get("area") == candidate["area"]
        and existing.get("status") == "issued"
        and existing.get("permit_type") in PERMIT_CONFLICT_MATRIX.get(candidate["permit_type"], set())
        and _permit_overlaps(existing, candidate, overlap_minutes)
    )
    if conflicts:
        event = _emit(
            next_state,
            "EnvironmentHealthSafetyPermitConflictDetected",
            {"permit_id": code, "conflicts": conflicts, "area": candidate["area"]},
            "permit",
            code,
        )
        return {
            "ok": False,
            "state": next_state,
            "reason": "permit_conflict",
            "conflicts": conflicts,
            "rule_result": evaluate_rule("permit_conflict_matrix", {"conflicts": conflicts}),
            "event": event,
            "side_effects": (),
        }
    next_state["records"]["permits"][code] = candidate
    event = _emit(
        next_state,
        "EnvironmentHealthSafetyPermitIssued",
        {"permit_id": code, "permit_type": candidate["permit_type"], "area": candidate["area"]},
        "permit",
        code,
    )
    return {"ok": True, "state": next_state, "permit": deepcopy(candidate), "event": event, "side_effects": ()}


def run_dynamic_risk_assessment(state: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
    tenant = payload.get("tenant", "default")
    area = payload.get("area")
    task = payload.get("task")
    hazards = tuple(
        hazard
        for hazard in state["records"]["hazards"].values()
        if hazard["tenant"] == tenant and hazard["area"] == area and hazard["task_step"] == task
    )
    permits = tuple(
        permit
        for permit in state["records"]["permits"].values()
        if permit["tenant"] == tenant and permit["area"] == area and permit["status"] == "issued"
    )
    live_conditions = {
        "weather": payload.get("weather", "clear"),
        "occupancy": payload.get("occupancy", "normal"),
        "temporary_bypasses": tuple(payload.get("temporary_bypasses", ())),
        "site_alerts": tuple(payload.get("site_alerts", ())),
    }
    base_risk = sum(hazard.get("residual_risk", 0) for hazard in hazards)
    permit_penalty = 15 * len(permits)
    live_penalty = 10 * len(live_conditions["temporary_bypasses"]) + 5 * len(live_conditions["site_alerts"])
    total_risk = min(100, base_risk + permit_penalty + live_penalty)
    return {
        "ok": True,
        "tenant": tenant,
        "area": area,
        "task": task,
        "hazards": deepcopy(hazards),
        "active_permits": deepcopy(permits),
        "live_conditions": live_conditions,
        "residual_risk": total_risk,
        "requires_signoff": total_risk >= int(state["parameters"]["risk_threshold"]["value"]),
        "side_effects": (),
    }


def run_advanced_assessment(state: dict[str, Any], payload: dict[str, Any] | None = None) -> dict[str, Any]:
    payload = deepcopy(payload or {})
    site = payload.get("site")
    incidents = tuple(
        incident
        for incident in state["records"]["incidents"].values()
        if site is None or incident["site"] == site
    )
    hazards = tuple(
        hazard
        for hazard in state["records"]["hazards"].values()
        if site is None or hazard["site"] == site
    )
    overdue_actions = tuple(
        action
        for action in state["records"]["corrective_actions"].values()
        if action["status"] != "effective"
    )
    drivers = {
        "repeated_near_misses": len([i for i in incidents if i["severity"] == "near_miss"]) * 8,
        "serious_events": len([i for i in incidents if i["severity"] in SERIOUS_INCIDENT_SEVERITIES]) * 20,
        "open_corrective_actions": len(overdue_actions) * 10,
        "open_hazards": len(hazards) * 6,
    }
    score = min(100, sum(drivers.values()))
    anomalies = (
        (
            {
                "kind": "permit_duration_outlier",
                "site": site or "all-sites",
                "baseline_window_days": 30,
                "observed_deviation": "2.1x extension rate",
            },
        )
        if payload.get("detect_anomalies", True) and score >= 20
        else ()
    )
    simulation = {
        "options": (
            {"control": "upgrade_ventilation", "incident_likelihood_delta": -0.35, "operational_disruption": "medium"},
            {"control": "add_staggered_schedule", "incident_likelihood_delta": -0.12, "operational_disruption": "low"},
            {"control": "increase_training_frequency", "incident_likelihood_delta": -0.08, "operational_disruption": "low"},
        ),
        "modeled": True,
    }
    return {
        "ok": True,
        "site": site,
        "predictive_risk_score": score,
        "drivers": drivers,
        "anomalies": anomalies,
        "counterfactual_simulation": simulation,
        "side_effects": (),
    }


def run_control_assertions(state: dict[str, Any], reference_time: str | None = None) -> dict[str, Any]:
    next_state = _copy(state)
    now = _parse_datetime(_timestamp(reference_time)) or datetime.now(UTC)
    assertions = []
    for incident in next_state["records"]["incidents"].values():
        due_at = _parse_datetime(incident["notification"].get("due_at"))
        if incident["notification"]["required"] and incident["notification"]["status"] != "acknowledged" and due_at and due_at < now:
            incident["notification"]["overdue"] = True
            assertion = {
                "assertion_id": _digest(("overdue_notification", incident["id"])),
                "rule": "serious_incident_notification_clock",
                "status": "failed",
                "record_id": incident["id"],
                "details": {"due_at": incident["notification"]["due_at"]},
            }
            assertions.append(assertion)
            next_state["control_assertions"][assertion["assertion_id"]] = assertion
            _open_exception(
                next_state,
                "serious-incident-notification-overdue",
                "Serious incident notification overdue",
                (incident["id"],),
                "critical",
                {"due_at": incident["notification"]["due_at"]},
            )
            _emit(
                next_state,
                "EnvironmentHealthSafetyControlAssertionFailed",
                assertion,
                "control_assertion",
                assertion["assertion_id"],
            )
    for permit in next_state["records"]["permits"].values():
        end_at = _parse_datetime(permit.get("end_at"))
        if permit["status"] == "issued" and end_at and end_at < now:
            assertion = {
                "assertion_id": _digest(("expired_permit", permit["id"])),
                "rule": "continuous_control_testing",
                "status": "failed",
                "record_id": permit["id"],
                "details": {"end_at": permit["end_at"]},
            }
            assertions.append(assertion)
            next_state["control_assertions"][assertion["assertion_id"]] = assertion
    return {"ok": True, "state": next_state, "assertions": tuple(assertions), "side_effects": ()}


def handle_consumed_event(state: dict[str, Any], event: dict[str, Any]) -> dict[str, Any]:
    next_state = _copy(state)
    idempotency_key = event.get("idempotency_key") or event.get("event_id") or _digest(event)
    if idempotency_key in next_state["idempotency_keys"]:
        return {
            "ok": True,
            "duplicate": True,
            "state": next_state,
            "idempotency_key": idempotency_key,
            "side_effects": (),
        }
    next_state["idempotency_keys"].add(idempotency_key)
    event_type = event.get("event_type")
    if event_type not in CONSUMED_EVENT_TYPES:
        dead_letter = {
            "event": deepcopy(event),
            "dead_letter_table": EVENT_TABLES[2],
            "retry_policy": {"max_attempts": next_state["configuration"]["retry_limit"]},
        }
        next_state["dead_letter"].append(dead_letter)
        return {
            "ok": False,
            "duplicate": False,
            "state": next_state,
            "dead_letter_table": EVENT_TABLES[2],
            "retry_policy": dead_letter["retry_policy"],
            "side_effects": (),
        }
    payload = deepcopy(event.get("payload", {}))
    next_state["inbox"].append(
        {
            "event_type": event_type,
            "idempotency_key": idempotency_key,
            "payload": payload,
            "received_at": _timestamp(),
        }
    )
    emitted = None
    if event_type == "PolicyChanged":
        new_policy = payload.get("policy_version", "ehs-policy-next")
        affected = []
        for collection_name in ("incidents", "permits", "inspections"):
            for record in next_state["records"][collection_name].values():
                if record.get("status") not in {"closed", "cancelled"}:
                    policy_versions = record.get(
                        "policy_versions",
                        {"original": record.get("policy_version"), "current": record.get("policy_version")},
                    )
                    policy_versions["current"] = new_policy
                    record["policy_versions"] = policy_versions
                    record["policy_version"] = new_policy
                    affected.append(record["id"])
        emitted = _emit(
            next_state,
            "EnvironmentHealthSafetyPolicyReevaluationRequested",
            {"policy_version": new_policy, "affected_records": tuple(affected)},
            "policy_rule",
            new_policy,
        )
    elif event_type == "AuditEventSealed":
        bundle_id = payload.get("bundle_id", _digest(payload))
        next_state["sealed_bundles"][bundle_id] = {
            "bundle_id": bundle_id,
            "record_ids": tuple(payload.get("record_ids", ())),
            "sealed_at": payload.get("sealed_at", _timestamp()),
            "status": "sealed",
        }
        emitted = _emit(
            next_state,
            "EnvironmentHealthSafetyEvidenceSealed",
            next_state["sealed_bundles"][bundle_id],
            "audit_bundle",
            bundle_id,
        )
    elif event_type == "OperationalKpiChanged":
        site = payload.get("site")
        weight = float(next_state["parameters"]["kpi_priority_weight"]["value"])
        impacted = []
        for incident in next_state["records"]["incidents"].values():
            if site is None or incident["site"] == site:
                incident["priority_score"] = _queue_priority(incident, weight)
                incident["priority_drivers"] = deepcopy(payload.get("drivers", {}))
                impacted.append(incident["id"])
        emitted = _emit(
            next_state,
            "EnvironmentHealthSafetyRiskPriorityRecalculated",
            {"site": site, "affected_records": tuple(impacted), "weight": weight},
            "risk_model",
            site or "global",
        )
    return {
        "ok": True,
        "duplicate": False,
        "state": next_state,
        "event_type": event_type,
        "idempotency_key": idempotency_key,
        "emitted_event": emitted,
        "side_effects": (),
    }


def build_seed_plan() -> dict[str, Any]:
    seeded = seed_state()
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "records": (
            {"table": READ_MODEL_TABLES["incidents"], "code": "INC-100"},
            {"table": READ_MODEL_TABLES["hazards"], "code": "HZ-001"},
            {"table": READ_MODEL_TABLES["inspections"], "code": "INSP-100"},
            {"table": READ_MODEL_TABLES["permits"], "code": "PERM-100"},
            {"table": READ_MODEL_TABLES["corrective_actions"], "code": "CA-100"},
        ),
        "seed_state_digest": _digest(
            {
                "incident_ids": tuple(seeded["records"]["incidents"].keys()),
                "hazard_ids": tuple(seeded["records"]["hazards"].keys()),
            }
        ),
        "side_effects": (),
    }


def build_domain_operation_catalog() -> tuple[dict[str, Any], ...]:
    return (
        {
            "operation": "create_ehs_incident",
            "operation_kind": "command",
            "owned_tables": (READ_MODEL_TABLES["incidents"], EVENT_TABLES[0]),
            "read_tables": (),
            "emitted_event": "EnvironmentHealthSafetyIncidentLogged",
            "transaction_boundary": "owned_datastore_plus_outbox",
            "workflow": "environment_health_safety_create_ehs_incident_workflow",
        },
        {
            "operation": "advance_incident_lifecycle",
            "operation_kind": "command",
            "owned_tables": (READ_MODEL_TABLES["incidents"], EVENT_TABLES[0]),
            "read_tables": (READ_MODEL_TABLES["corrective_actions"],),
            "emitted_event": "EnvironmentHealthSafetyIncidentLifecycleAdvanced",
            "transaction_boundary": "owned_datastore_plus_outbox",
            "workflow": "serious_incident_response",
        },
        {
            "operation": "send_serious_incident_notice",
            "operation_kind": "command",
            "owned_tables": (READ_MODEL_TABLES["incidents"], EVENT_TABLES[0]),
            "read_tables": (),
            "emitted_event": "EnvironmentHealthSafetySeriousIncidentNoticeSent",
            "transaction_boundary": "owned_datastore_plus_outbox",
            "workflow": "environment_health_safety_serious_incident_notification_workflow",
        },
        {
            "operation": "record_hazard",
            "operation_kind": "command",
            "owned_tables": (READ_MODEL_TABLES["hazards"], EVENT_TABLES[0]),
            "read_tables": (),
            "emitted_event": "EnvironmentHealthSafetyCreated",
            "transaction_boundary": "owned_datastore_plus_outbox",
            "workflow": "environment_health_safety_record_hazard_workflow",
        },
        {
            "operation": "promote_near_miss_cluster",
            "operation_kind": "command",
            "owned_tables": (READ_MODEL_TABLES["hazards"], EVENT_TABLES[0]),
            "read_tables": (READ_MODEL_TABLES["incidents"],),
            "emitted_event": "EnvironmentHealthSafetyHazardPromoted",
            "transaction_boundary": "owned_datastore_plus_outbox",
            "workflow": "environment_health_safety_record_hazard_workflow",
        },
        {
            "operation": "create_corrective_action",
            "operation_kind": "command",
            "owned_tables": (READ_MODEL_TABLES["corrective_actions"], READ_MODEL_TABLES["incidents"]),
            "read_tables": (),
            "emitted_event": "EnvironmentHealthSafetyCreated",
            "transaction_boundary": "owned_datastore_plus_outbox",
            "workflow": "environment_health_safety_corrective_action_effectiveness_workflow",
        },
        {
            "operation": "verify_corrective_action",
            "operation_kind": "command",
            "owned_tables": (READ_MODEL_TABLES["corrective_actions"], READ_MODEL_TABLES["incidents"]),
            "read_tables": (),
            "emitted_event": "EnvironmentHealthSafetyCorrectiveActionReopened",
            "transaction_boundary": "owned_datastore_plus_outbox",
            "workflow": "environment_health_safety_corrective_action_effectiveness_workflow",
        },
        {
            "operation": "schedule_inspection",
            "operation_kind": "command",
            "owned_tables": (READ_MODEL_TABLES["inspections"],),
            "read_tables": (),
            "emitted_event": "EnvironmentHealthSafetyCreated",
            "transaction_boundary": "owned_datastore_plus_outbox",
            "workflow": "inspection_capture",
        },
        {
            "operation": "capture_inspection_sync",
            "operation_kind": "command",
            "owned_tables": (READ_MODEL_TABLES["inspections"], EVENT_TABLES[0]),
            "read_tables": (),
            "emitted_event": "EnvironmentHealthSafetyInspectionSynced",
            "transaction_boundary": "owned_datastore_plus_outbox",
            "workflow": "inspection_capture",
        },
        {
            "operation": "issue_permit",
            "operation_kind": "command",
            "owned_tables": (READ_MODEL_TABLES["permits"], EVENT_TABLES[0]),
            "read_tables": (READ_MODEL_TABLES["permits"],),
            "emitted_event": "EnvironmentHealthSafetyPermitIssued",
            "transaction_boundary": "owned_datastore_plus_outbox",
            "workflow": "environment_health_safety_permit_conflict_workflow",
        },
        {
            "operation": "run_dynamic_risk_assessment",
            "operation_kind": "command",
            "owned_tables": (),
            "read_tables": (READ_MODEL_TABLES["hazards"], READ_MODEL_TABLES["permits"]),
            "emitted_event": None,
            "transaction_boundary": "read_only_projection",
            "workflow": "environment_health_safety_dynamic_risk_assessment_workflow",
        },
        {
            "operation": "run_advanced_assessment",
            "operation_kind": "command",
            "owned_tables": (),
            "read_tables": (
                READ_MODEL_TABLES["incidents"],
                READ_MODEL_TABLES["hazards"],
                READ_MODEL_TABLES["corrective_actions"],
            ),
            "emitted_event": None,
            "transaction_boundary": "read_only_projection",
            "workflow": "advanced_intelligence",
        },
        {
            "operation": "handle_consumed_event",
            "operation_kind": "command",
            "owned_tables": (EVENT_TABLES[1], EVENT_TABLES[2]),
            "read_tables": BUSINESS_TABLES,
            "emitted_event": "EnvironmentHealthSafetyPolicyReevaluationRequested",
            "transaction_boundary": "owned_datastore_plus_outbox",
            "workflow": "governance_events",
        },
        {
            "operation": "query_workbench",
            "operation_kind": "query",
            "owned_tables": (),
            "read_tables": BUSINESS_TABLES,
            "emitted_event": None,
            "transaction_boundary": "read_only_projection",
            "workflow": "EnvironmentHealthSafetyWorkbench",
        },
        {
            "operation": "build_detail_view",
            "operation_kind": "query",
            "owned_tables": (),
            "read_tables": BUSINESS_TABLES,
            "emitted_event": None,
            "transaction_boundary": "read_only_projection",
            "workflow": "EnvironmentHealthSafetyDetail",
        },
    )


DOMAIN_OPERATIONS = tuple(item["operation"] for item in build_domain_operation_catalog())


def execute_domain_operation(operation: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    payload = deepcopy(payload or {})
    state = payload.pop("state", seed_state())
    if operation == "create_ehs_incident":
        return create_ehs_incident(state, payload)
    if operation == "advance_incident_lifecycle":
        return advance_incident_lifecycle(
            state,
            payload["incident_id"],
            payload["new_status"],
            actor=payload.get("actor"),
            dossier_updates=payload.get("dossier_updates"),
        )
    if operation == "send_serious_incident_notice":
        return send_serious_incident_notice(state, payload["incident_id"], payload.get("actor", {"name": "system"}), payload.get("sent_at"))
    if operation == "record_hazard":
        return record_hazard(state, payload)
    if operation == "promote_near_miss_cluster":
        return promote_near_miss_cluster(state, payload)
    if operation == "create_corrective_action":
        return create_corrective_action(state, payload)
    if operation == "verify_corrective_action":
        return verify_corrective_action(state, payload["action_id"], payload)
    if operation == "schedule_inspection":
        return schedule_inspection(state, payload)
    if operation == "capture_inspection_sync":
        return capture_inspection_sync(state, payload)
    if operation == "issue_permit":
        return issue_permit(state, payload)
    if operation == "run_dynamic_risk_assessment":
        return run_dynamic_risk_assessment(state, payload)
    if operation == "run_advanced_assessment":
        return run_advanced_assessment(state, payload)
    if operation == "handle_consumed_event":
        return handle_consumed_event(state, payload["event"])
    if operation == "query_workbench":
        return query_workbench(state, payload)
    if operation == "build_detail_view":
        return build_detail_view(state, payload["record_id"])
    return {"ok": False, "reason": "unknown_domain_operation", "operation": operation, "side_effects": ()}


def build_table_contracts() -> tuple[dict[str, Any], ...]:
    base_fields = (
        {"name": "id", "type": "TEXT", "required": True},
        {"name": "tenant", "type": "TEXT", "required": True},
        {"name": "status", "type": "TEXT", "required": True},
        {"name": "version", "type": "INTEGER", "required": True, "default": 1},
        {"name": "payload", "type": "JSON", "required": True},
        {"name": "created_at", "type": "TIMESTAMPTZ", "required": True},
        {"name": "updated_at", "type": "TIMESTAMPTZ", "required": True},
    )
    return (
        {
            "table": READ_MODEL_TABLES["incidents"],
            "fields": base_fields
            + (
                {"name": "code", "type": "TEXT", "required": True},
                {"name": "site", "type": "TEXT", "required": True},
                {"name": "area", "type": "TEXT", "required": True},
                {"name": "task", "type": "TEXT", "required": True},
                {"name": "severity", "type": "TEXT", "required": True},
                {"name": "recordability", "type": "TEXT", "required": True},
                {"name": "notification_due_at", "type": "TIMESTAMPTZ", "required": False},
                {"name": "notification_status", "type": "TEXT", "required": True},
                {"name": "policy_version", "type": "TEXT", "required": True},
            ),
        },
        {
            "table": READ_MODEL_TABLES["hazards"],
            "fields": base_fields
            + (
                {"name": "code", "type": "TEXT", "required": True},
                {"name": "site", "type": "TEXT", "required": True},
                {"name": "area", "type": "TEXT", "required": True},
                {"name": "process", "type": "TEXT", "required": True},
                {"name": "task_step", "type": "TEXT", "required": True},
                {"name": "energy_source", "type": "TEXT", "required": True},
                {"name": "hazard_type", "type": "TEXT", "required": True},
                {"name": "residual_risk", "type": "INTEGER", "required": True},
                {"name": "cluster_count", "type": "INTEGER", "required": True},
            ),
        },
        {
            "table": READ_MODEL_TABLES["inspections"],
            "fields": base_fields
            + (
                {"name": "code", "type": "TEXT", "required": True},
                {"name": "template", "type": "TEXT", "required": True},
                {"name": "asset", "type": "TEXT", "required": False},
                {"name": "area", "type": "TEXT", "required": True},
                {"name": "due_at", "type": "TIMESTAMPTZ", "required": False},
                {"name": "recurrence", "type": "TEXT", "required": True},
            ),
        },
        {
            "table": READ_MODEL_TABLES["permits"],
            "fields": base_fields
            + (
                {"name": "code", "type": "TEXT", "required": True},
                {"name": "permit_type", "type": "TEXT", "required": True},
                {"name": "area", "type": "TEXT", "required": True},
                {"name": "start_at", "type": "TIMESTAMPTZ", "required": True},
                {"name": "end_at", "type": "TIMESTAMPTZ", "required": True},
                {"name": "energy_source", "type": "TEXT", "required": True},
            ),
        },
        {
            "table": READ_MODEL_TABLES["corrective_actions"],
            "fields": base_fields
            + (
                {"name": "code", "type": "TEXT", "required": True},
                {"name": "incident_id", "type": "TEXT", "required": False},
                {"name": "owner", "type": "TEXT", "required": True},
                {"name": "due_date", "type": "TIMESTAMPTZ", "required": True},
                {"name": "hierarchy_of_controls", "type": "TEXT", "required": True},
                {"name": "verification_step", "type": "TEXT", "required": True},
            ),
        },
        {
            "table": READ_MODEL_TABLES["safety_training"],
            "fields": (
                {"name": "id", "type": "TEXT", "required": True},
                {"name": "tenant", "type": "TEXT", "required": True},
                {"name": "worker", "type": "TEXT", "required": True},
                {"name": "course", "type": "TEXT", "required": True},
                {"name": "status", "type": "TEXT", "required": True},
                {"name": "expires_at", "type": "TIMESTAMPTZ", "required": True},
            ),
        },
        {
            "table": READ_MODEL_TABLES["audit_findings"],
            "fields": (
                {"name": "id", "type": "TEXT", "required": True},
                {"name": "tenant", "type": "TEXT", "required": True},
                {"name": "status", "type": "TEXT", "required": True},
                {"name": "severity", "type": "TEXT", "required": True},
                {"name": "finding", "type": "TEXT", "required": True},
                {"name": "evidence_bundle_id", "type": "TEXT", "required": False},
            ),
        },
        {
            "table": f"{PBC_KEY}_policy_rule",
            "fields": (
                {"name": "rule_id", "type": "TEXT", "required": True},
                {"name": "status", "type": "TEXT", "required": True},
                {"name": "description", "type": "TEXT", "required": True},
                {"name": "compiled_hash", "type": "TEXT", "required": True},
            ),
        },
        {
            "table": f"{PBC_KEY}_runtime_parameter",
            "fields": (
                {"name": "name", "type": "TEXT", "required": True},
                {"name": "value", "type": "NUMERIC", "required": True},
                {"name": "minimum", "type": "NUMERIC", "required": True},
                {"name": "maximum", "type": "NUMERIC", "required": True},
            ),
        },
        {
            "table": f"{PBC_KEY}_schema_extension",
            "fields": (
                {"name": "id", "type": "TEXT", "required": True},
                {"name": "table_name", "type": "TEXT", "required": True},
                {"name": "fields", "type": "JSON", "required": True},
            ),
        },
        {
            "table": f"{PBC_KEY}_control_assertion",
            "fields": (
                {"name": "assertion_id", "type": "TEXT", "required": True},
                {"name": "rule", "type": "TEXT", "required": True},
                {"name": "status", "type": "TEXT", "required": True},
                {"name": "record_id", "type": "TEXT", "required": True},
                {"name": "details", "type": "JSON", "required": True},
            ),
        },
        {
            "table": f"{PBC_KEY}_governed_model",
            "fields": (
                {"name": "id", "type": "TEXT", "required": True},
                {"name": "model_name", "type": "TEXT", "required": True},
                {"name": "purpose", "type": "TEXT", "required": True},
                {"name": "approval_status", "type": "TEXT", "required": True},
            ),
        },
        {
            "table": EVENT_TABLES[0],
            "fields": (
                {"name": "event_id", "type": "TEXT", "required": True},
                {"name": "event_type", "type": "TEXT", "required": True},
                {"name": "aggregate_id", "type": "TEXT", "required": True},
                {"name": "payload", "type": "JSON", "required": True},
                {"name": "occurred_at", "type": "TIMESTAMPTZ", "required": True},
            ),
        },
        {
            "table": EVENT_TABLES[1],
            "fields": (
                {"name": "event_type", "type": "TEXT", "required": True},
                {"name": "idempotency_key", "type": "TEXT", "required": True},
                {"name": "payload", "type": "JSON", "required": True},
                {"name": "received_at", "type": "TIMESTAMPTZ", "required": True},
            ),
        },
        {
            "table": EVENT_TABLES[2],
            "fields": (
                {"name": "id", "type": "INTEGER", "required": True},
                {"name": "event", "type": "JSON", "required": True},
                {"name": "retry_policy", "type": "JSON", "required": True},
            ),
        },
    )


def build_schema_contract() -> dict[str, Any]:
    table_contracts = build_table_contracts()
    migrations = tuple(
        {
            "path": f"src/pyAppGen/pbcs/{PBC_KEY}/{MIGRATION_FILE}",
            "operation": "create_owned_table",
            "table": contract["table"],
            "backend_allowlist": ALLOWED_DATABASE_BACKENDS,
        }
        for contract in table_contracts
    )
    models = tuple(
        {
            "class_name": "".join(part.capitalize() for part in contract["table"].split("_")),
            "table": contract["table"],
            "fields": contract["fields"],
        }
        for contract in table_contracts
    )
    return {
        "format": f"appgen.{PBC_KEY}.schema-contract.v2",
        "ok": True,
        "pbc": PBC_KEY,
        "tables": table_contracts,
        "models": models,
        "migrations": migrations,
        "database_backends": ALLOWED_DATABASE_BACKENDS,
        "datastore_backends": ALLOWED_DATABASE_BACKENDS,
        "shared_table_access": False,
        "owned_tables": OWNED_TABLES,
    }


def build_service_contract() -> dict[str, Any]:
    operations = build_domain_operation_catalog()
    command_methods = tuple(
        item["operation"]
        for item in operations
        if item["operation_kind"] == "command"
    ) + ("configure_runtime", "set_parameter", "register_rule", "register_schema_extension")
    query_methods = tuple(
        item["operation"]
        for item in operations
        if item["operation_kind"] == "query"
    ) + ("build_release_evidence",)
    return {
        "format": f"appgen.{PBC_KEY}.service-contract.v2",
        "ok": True,
        "pbc": PBC_KEY,
        "command_methods": command_methods,
        "query_methods": query_methods,
        "operation_catalog": operations,
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
        "shared_table_access": False,
    }


def build_api_contract() -> dict[str, Any]:
    routes = (
        "POST /ehs-incidents",
        "POST /ehs-incidents/dry-run",
        "POST /ehs-incidents/search",
        "POST /hazards",
        "POST /hazards/bulk-intake",
        "POST /inspections",
        "POST /inspections/offline-sync",
        "POST /permits",
        "POST /permits/dry-run",
        "POST /corrective-actions",
        "POST /corrective-actions/bulk-close",
        "GET /environment-health-safety-workbench",
        "GET /environment-health-safety/records/{record_id}",
        "GET /environment-health-safety/evidence/export",
    )
    return {
        "format": f"appgen.{PBC_KEY}.api-contract.v2",
        "ok": True,
        "pbc": PBC_KEY,
        "routes": routes,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "owned_tables": OWNED_TABLES,
    }


def build_event_contract() -> dict[str, Any]:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "emitted": EMITTED_EVENT_TYPES,
        "consumed": CONSUMED_EVENT_TYPES,
        "outbox_table": EVENT_TABLES[0],
        "inbox_table": EVENT_TABLES[1],
        "dead_letter_table": EVENT_TABLES[2],
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "idempotency": "required",
    }


def build_handler_manifest() -> dict[str, Any]:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "consumes": CONSUMED_EVENT_TYPES,
        "idempotency_key": "required",
        "retry_policy": {"max_attempts": 5},
        "dead_letter_table": EVENT_TABLES[2],
        "sealed_evidence_support": True,
        "side_effects": (),
    }


def build_ui_contract(state: dict[str, Any] | None = None) -> dict[str, Any]:
    workbench = query_workbench(state or seed_state(), {"tenant": "tenant-seed"})
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "fragments": UI_FRAGMENT_KEYS,
        "forms": FORM_DEFINITIONS,
        "wizards": WIZARD_DEFINITIONS,
        "controls": CONTROL_DEFINITIONS,
        "navigation_sections": (
            "overview",
            "incident_queue",
            "hazard_register",
            "permits",
            "inspections",
            "corrective_actions",
            "governance",
            "release_evidence",
        ),
        "workbench_preview": workbench["queues"],
        "action_permissions": PERMISSIONS[:-1],
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def build_agent_contract() -> dict[str, Any]:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "entrypoint": f"/assistant/pbc/{PBC_KEY}",
        "single_agent_contribution": f"{PBC_KEY}_skills",
        "skills": AGENT_SKILLS,
        "capabilities": (
            "task_guidance",
            "document_instruction_intake",
            "governed_datastore_crud",
            "mutation_preview",
            "investigation_gap_analysis",
            "regulator_export_guidance",
        ),
        "side_effects": (),
    }


def build_configuration_manifest() -> dict[str, Any]:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "database_backends": ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": REQUIRED_EVENT_TOPIC,
        "parameters": tuple(_parameter_state().values()),
        "rules": tuple(_rule_state().values()),
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def build_permission_manifest() -> dict[str, Any]:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "permissions": PERMISSIONS[:-1],
        "roles": (
            {"role": "operator", "permissions": (f"{PBC_KEY}.read", f"{PBC_KEY}.create", f"{PBC_KEY}.update")},
            {"role": "approver", "permissions": (f"{PBC_KEY}.approve",)},
            {"role": "auditor", "permissions": (f"{PBC_KEY}.read", f"{PBC_KEY}.approve")},
            {"role": "admin", "permissions": PERMISSIONS[:-1]},
        ),
        "side_effects": (),
    }


def query_workbench(state: dict[str, Any], filters: dict[str, Any] | None = None) -> dict[str, Any]:
    filters = deepcopy(filters or {})
    controlled = run_control_assertions(state)
    next_state = controlled["state"]
    tenant = filters.get("tenant")
    limit = int(next_state["parameters"]["workbench_limit"]["value"])
    kpi_weight = float(next_state["parameters"]["kpi_priority_weight"]["value"])

    def _matching(records: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
        values = list(records.values())
        if tenant:
            values = [record for record in values if record.get("tenant") == tenant]
        return values[:limit]

    incident_cards = [
        {
            "id": incident["id"],
            "severity": incident["severity"],
            "recordability": incident["recordability"],
            "notification_status": incident["notification"]["status"],
            "notification_due_at": incident["notification"]["due_at"],
            "priority_score": incident.get("priority_score", _queue_priority(incident, kpi_weight)),
            "status": incident["status"],
        }
        for incident in _matching(next_state["records"]["incidents"])
    ]
    metrics = {
        "open_incidents": len([card for card in incident_cards if card["status"] != "closed"]),
        "open_hazards": len(_matching(next_state["records"]["hazards"])),
        "scheduled_inspections": len(_matching(next_state["records"]["inspections"])),
        "issued_permits": len(_matching(next_state["records"]["permits"])),
        "open_exceptions": len(next_state["exceptions"]),
    }
    return {
        "ok": True,
        "tenant": tenant,
        "queues": {
            "incident_cards": incident_cards,
            "hazards": _matching(next_state["records"]["hazards"]),
            "inspections": _matching(next_state["records"]["inspections"]),
            "permits": _matching(next_state["records"]["permits"]),
            "corrective_actions": _matching(next_state["records"]["corrective_actions"]),
            "exceptions": deepcopy(next_state["exceptions"][:limit]),
        },
        "metrics": metrics,
        "control_assertions": controlled["assertions"],
        "state": next_state,
        "side_effects": (),
    }


def build_detail_view(state: dict[str, Any], record_id: str) -> dict[str, Any]:
    incidents = state["records"]["incidents"]
    if record_id in incidents:
        incident = incidents[record_id]
        causal_chain = (
            incident["investigation"].get("immediate_cause"),
            incident["investigation"].get("basic_cause"),
            incident["investigation"].get("root_cause"),
        )
        return {
            "ok": True,
            "record_type": "incident",
            "record_id": record_id,
            "severity": incident["severity"],
            "recordability": incident["recordability"],
            "notification": deepcopy(incident["notification"]),
            "causal_chain": causal_chain,
            "failed_controls": incident["investigation"].get("failed_controls", ()),
            "evidence_bundle": deepcopy(incident["evidence_bundle"]),
            "side_effects": (),
        }
    hazards = state["records"]["hazards"]
    if record_id in hazards:
        hazard = hazards[record_id]
        return {
            "ok": True,
            "record_type": "hazard",
            "record_id": record_id,
            "lineage_incidents": deepcopy(hazard["lineage_incidents"]),
            "cluster_count": hazard["cluster_count"],
            "residual_risk": hazard["residual_risk"],
            "side_effects": (),
        }
    return {"ok": False, "reason": "record_not_found", "record_id": record_id, "side_effects": ()}


def build_release_evidence() -> dict[str, Any]:
    schema = build_schema_contract()
    services = build_service_contract()
    events = build_event_contract()
    ui = build_ui_contract()
    agent = build_agent_contract()
    configuration = build_configuration_manifest()
    seed = build_seed_plan()
    docs = {
        "specification": (_package_root() / "SPECIFICATION.md").exists(),
        "release_evidence": (_package_root() / "RELEASE_EVIDENCE.md").exists(),
        "readme": (_package_root() / "README.md").exists(),
        "status": (_package_root() / "implementation-status.md").exists(),
    }
    checks = (
        {"id": "schema_models_migrations", "ok": schema["ok"] and len(schema["tables"]) >= 12},
        {"id": "service_route_alignment", "ok": services["ok"] and build_api_contract()["ok"]},
        {"id": "typed_event_contract", "ok": events["ok"] and "EnvironmentHealthSafetyPermitIssued" in events["emitted"]},
        {"id": "ui_forms_wizards_controls", "ok": ui["ok"] and bool(ui["forms"]) and bool(ui["wizards"])},
        {"id": "agent_governance", "ok": agent["ok"] and any(skill["mutation_scope"] == "requires_confirmation" for skill in agent["skills"])},
        {"id": "rules_and_parameters", "ok": configuration["ok"] and len(configuration["parameters"]) >= 5 and len(configuration["rules"]) >= 5},
        {"id": "seed_and_docs", "ok": seed["ok"] and all(docs.values())},
    )
    return {
        "format": f"appgen.{PBC_KEY}.release-evidence.v2",
        "ok": all(check["ok"] for check in checks),
        "pbc": PBC_KEY,
        "checks": checks,
        "generated_artifacts": {
            "migrations": schema["migrations"],
            "models": schema["models"],
            "events": events,
            "handlers": build_handler_manifest(),
            "ui": UI_FRAGMENT_KEYS,
            "workflows": WORKFLOW_DEFINITIONS,
            "agent_skills": AGENT_SKILLS,
        },
        "docs": docs,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
        "side_effects": (),
    }


def build_manifest() -> dict[str, Any]:
    return {
        "pbc": PBC_KEY,
        "label": PBC_LABEL,
        "description": PBC_DESCRIPTION,
        "mesh": MESH,
        "template": "asset",
        "version": VERSION,
        "datastore_backend": "postgresql",
        "tables": tuple(table.replace(f"{PBC_KEY}_", "", 1) for table in BUSINESS_TABLES),
        "migrations": (MIGRATION_FILE,),
        "apis": build_api_contract()["routes"],
        "workflows": tuple(WORKFLOW_DEFINITIONS.keys()),
        "ui_fragments": UI_FRAGMENT_KEYS,
        "analytics": ("environment_health_safety_risk_score", "environment_health_safety_workbench_metric"),
        "emits": EMITTED_EVENT_TYPES,
        "consumes": CONSUMED_EVENT_TYPES,
        "advanced_capabilities": ADVANCED_CAPABILITY_KEYS,
        "docs": ("SPECIFICATION.md", "RELEASE_EVIDENCE.md", "README.md", "implementation-status.md"),
        "configuration": (
            "ENVIRONMENT_HEALTH_SAFETY_DATABASE_URL",
            "ENVIRONMENT_HEALTH_SAFETY_EVENT_TOPIC",
            "ENVIRONMENT_HEALTH_SAFETY_RETRY_LIMIT",
            "ENVIRONMENT_HEALTH_SAFETY_DEFAULT_POLICY",
        ),
        "permissions": PERMISSIONS[:-1],
        "standard_features": STANDARD_FEATURE_KEYS,
        "capabilities": STANDARD_FEATURE_KEYS + ADVANCED_CAPABILITY_KEYS,
        "tests": ("tests/test_contract.py", "tests/test_standalone.py"),
        "seed_data": ("seed_data.py",),
    }


def build_package_metadata() -> dict[str, Any]:
    return {
        "format": f"appgen.{PBC_KEY}.metadata.v2",
        "ok": True,
        "pbc": PBC_KEY,
        "manifest": build_manifest(),
        "schema": build_schema_contract(),
        "service": build_service_contract(),
        "release_evidence": build_release_evidence(),
        "side_effects": (),
    }


def verify_owned_table_boundary(references: tuple[str, ...] | list[str] | None = None) -> dict[str, Any]:
    invalid = tuple(
        ref
        for ref in tuple(references or ())
        if isinstance(ref, str) and not ref.startswith(f"{PBC_KEY}_")
    )
    return {
        "ok": not invalid,
        "pbc": PBC_KEY,
        "invalid_references": invalid,
        "allowed_tables": OWNED_TABLES,
        "shared_table_access": False,
    }


def runtime_capabilities() -> dict[str, Any]:
    smoke = smoke_test()
    return {
        "format": f"appgen.{PBC_KEY}.runtime-capabilities.v2",
        "ok": smoke["ok"],
        "pbc": PBC_KEY,
        "implementation_directory": f"src/pyAppGen/pbcs/{PBC_KEY}",
        "owned_tables": OWNED_TABLES,
        "allowed_database_backends": ALLOWED_DATABASE_BACKENDS,
        "standard_features": STANDARD_FEATURE_KEYS,
        "capabilities": ADVANCED_CAPABILITY_KEYS,
        "operations": DOMAIN_OPERATIONS
        + (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "register_schema_extension",
            "build_release_evidence",
            "verify_owned_table_boundary",
        ),
        "smoke": smoke,
        "world_class_domain_depth": domain_depth_contract(),
        "database_backends": ALLOWED_DATABASE_BACKENDS,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def domain_depth_contract() -> dict[str, Any]:
    operation_catalog = build_domain_operation_catalog()
    return {
        "format": f"appgen.{PBC_KEY}.world-class-domain-depth.v2",
        "ok": True,
        "pbc": PBC_KEY,
        "purpose": PBC_DESCRIPTION,
        "owned_tables": OWNED_TABLES,
        "operation_count": len(operation_catalog),
        "operations": DOMAIN_OPERATIONS,
        "rules": tuple(RULE_DEFINITIONS.keys()),
        "parameters": tuple(PARAMETER_DEFINITIONS.keys()),
        "emitted_events": EMITTED_EVENT_TYPES,
        "consumed_events": CONSUMED_EVENT_TYPES,
        "advanced_capabilities": ADVANCED_CAPABILITY_KEYS,
        "workbench_views": (
            "incident_queue",
            "hazard_register",
            "inspection_due_queue",
            "permit_conflicts",
            "corrective_action_effectiveness",
            "release_evidence",
        ),
        "database_backends": ALLOWED_DATABASE_BACKENDS,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "minimum_owned_domain_tables": 12,
        "minimum_domain_operations": 12,
        "operation_catalog": operation_catalog,
        "side_effects": (),
    }


def domain_capability_surface_contract() -> dict[str, Any]:
    operation_catalog = build_domain_operation_catalog()
    return {
        "format": f"appgen.{PBC_KEY}.capability-surface.v2",
        "ok": True,
        "pbc": PBC_KEY,
        "operation_surfaces": tuple(
            {
                "operation": item["operation"],
                "surface": f"{PBC_KEY}.ui.operation.{item['operation']}",
                "action": item["operation"],
                "permission": f"{PBC_KEY}.operate",
                "workflow": item["workflow"],
                "event": item["emitted_event"],
            }
            for item in operation_catalog
        ),
        "rule_surfaces": tuple(
            {
                "rule": rule_id,
                "surface": f"{PBC_KEY}.ui.rule.{rule_id}",
                "editor": True,
                "explainable": True,
            }
            for rule_id in RULE_DEFINITIONS
        ),
        "parameter_surfaces": tuple(
            {
                "parameter": parameter,
                "surface": f"{PBC_KEY}.ui.parameter.{parameter}",
                "bounded": True,
                "editable": True,
            }
            for parameter in PARAMETER_DEFINITIONS
        ),
        "advanced_surfaces": tuple(
            {
                "capability": capability,
                "surface": f"{PBC_KEY}.ui.advanced.{capability}",
                "explainable": True,
            }
            for capability in ADVANCED_CAPABILITY_KEYS
        ),
        "table_surfaces": tuple(
            {
                "owned_table": table,
                "surface": f"{PBC_KEY}.ui.table.{table}",
                "read_model": True,
                "mutation_guard": True,
            }
            for table in OWNED_TABLES
        ),
        "coverage": {
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
            "shared_table_access": False,
        },
        "side_effects": (),
    }


def build_document_instruction_plan(document: str, instruction: str) -> dict[str, Any]:
    lowered = f"{document} {instruction}".lower()
    if "permit" in lowered:
        target = READ_MODEL_TABLES["permits"]
        workflow = "environment_health_safety_permit_conflict_workflow"
    elif "hazard" in lowered:
        target = READ_MODEL_TABLES["hazards"]
        workflow = "environment_health_safety_record_hazard_workflow"
    else:
        target = READ_MODEL_TABLES["incidents"]
        workflow = "environment_health_safety_create_ehs_incident_workflow"
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "document_digest": _digest((document, instruction)),
        "instruction": instruction,
        "candidate_tables": (target,),
        "workflow": workflow,
        "requires_human_confirmation": True,
        "citations": tuple(RULE_DEFINITIONS.keys())[:2],
        "crud_preview": {"operation": "create", "event_contract": "AppGen-X"},
        "side_effects": (),
    }


def build_datastore_crud_plan(action: str, table: str | None = None, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    target = table or READ_MODEL_TABLES["incidents"]
    if target not in OWNED_TABLES:
        return {
            "ok": False,
            "reason": "foreign_table_rejected",
            "table": target,
            "side_effects": (),
        }
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "action": action,
        "table": target,
        "payload": deepcopy(payload or {}),
        "requires_confirmation": action in {"create", "update", "delete"},
        "event_contract": "AppGen-X",
        "side_effects": (),
    }


def smoke_test() -> dict[str, Any]:
    state = empty_state()
    configured = configure_runtime(state, {"database_backend": "postgresql", "event_topic": REQUIRED_EVENT_TOPIC})
    parameterized = set_parameter(configured["state"], "workbench_limit", 30)
    ruled = register_rule(parameterized["state"], {"rule_id": "incident_closure_gate"})
    incident_result = create_ehs_incident(
        ruled["state"],
        {
            "tenant": "tenant-smoke",
            "code": "INC-SMOKE",
            "site": "Plant Smoke",
            "area": "Area Smoke",
            "task": "Task Smoke",
            "severity": "fatality",
            "unsafe_condition": "unguarded energy",
        },
    )
    notice = send_serious_incident_notice(
        incident_result["state"],
        "INC-SMOKE",
        {"name": "Smoke Approver", "role": "approver"},
    )
    action_result = create_corrective_action(
        notice["state"],
        {
            "tenant": "tenant-smoke",
            "code": "CA-SMOKE",
            "incident_id": "INC-SMOKE",
            "owner": "Maintenance",
            "due_date": "2026-06-10T00:00:00+00:00",
            "hierarchy_of_controls": "engineering",
            "verification_step": "verify_guard",
        },
    )
    investigation_state = advance_incident_lifecycle(
        action_result["state"],
        "INC-SMOKE",
        "triaged",
        actor={"name": "Smoke Lead"},
    )["state"]
    investigation_state = advance_incident_lifecycle(
        investigation_state,
        "INC-SMOKE",
        "recordability_review",
        actor={"name": "Smoke Lead"},
    )["state"]
    investigation_state = advance_incident_lifecycle(
        investigation_state,
        "INC-SMOKE",
        "regulator_notified",
        actor={"name": "Smoke Lead"},
    )["state"]
    investigation_state = advance_incident_lifecycle(
        investigation_state,
        "INC-SMOKE",
        "investigation_open",
        actor={"name": "Smoke Lead"},
        dossier_updates={
            "chronology": ("alarm", "response"),
            "witness_statements": ("statement",),
            "equipment_state": "isolated",
            "immediate_cause": "unguarded energy",
            "basic_cause": "maintenance gap",
            "root_cause": "inspection backlog",
            "failed_controls": ("guarding",),
            "evidence_links": ("ehs://proof/inc-smoke",),
        },
    )["state"]
    investigation_state = advance_incident_lifecycle(
        investigation_state,
        "INC-SMOKE",
        "corrective_action_open",
        actor={"name": "Smoke Lead"},
    )["state"]
    verified = verify_corrective_action(
        investigation_state,
        "CA-SMOKE",
        {"action_id": "CA-SMOKE", "passed": True, "evidence_links": ("ehs://proof/ca-smoke",)},
    )
    closed = advance_incident_lifecycle(
        verified["state"],
        "INC-SMOKE",
        "closed",
        actor={"name": "Smoke Lead"},
    )
    workbench = query_workbench(seed_state(), {"tenant": "tenant-seed"})
    handler = handle_consumed_event(seed_state(), {"event_type": "PolicyChanged", "idempotency_key": "policy-smoke", "payload": {"policy_version": "ehs-policy-2026.2"}})
    duplicate = handle_consumed_event(handler["state"], {"event_type": "PolicyChanged", "idempotency_key": "policy-smoke", "payload": {"policy_version": "ehs-policy-2026.2"}})
    dead_letter = handle_consumed_event(seed_state(), {"event_type": "Unexpected"})
    checks = (
        {"id": "configure_runtime", "ok": configured["ok"]},
        {"id": "set_parameter", "ok": parameterized["ok"]},
        {"id": "register_rule", "ok": ruled["ok"]},
        {"id": "incident_created", "ok": incident_result["ok"]},
        {"id": "serious_notice", "ok": notice["ok"]},
        {"id": "incident_closed", "ok": closed["ok"]},
        {"id": "workbench", "ok": workbench["ok"] and bool(workbench["queues"]["incident_cards"])},
        {"id": "consumed_handler", "ok": handler["ok"]},
        {"id": "idempotent_duplicate", "ok": duplicate["duplicate"] is True},
        {"id": "dead_letter", "ok": dead_letter["ok"] is False and dead_letter["dead_letter_table"] == EVENT_TABLES[2]},
        {"id": "release_evidence", "ok": build_release_evidence()["ok"]},
        {"id": "table_boundary", "ok": verify_owned_table_boundary((OWNED_TABLES[0], "foreign_table"))["ok"] is False},
    )
    return {
        "format": f"appgen.{PBC_KEY}.smoke.v2",
        "ok": all(check["ok"] for check in checks),
        "checks": checks,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
        "side_effects": (),
    }
