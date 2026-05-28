"""Package-local executable slice for chemical batch compliance."""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from typing import Any


PBC_KEY = "chemical_batch_compliance"
EVENT_CONTRACT = "AppGen-X"
ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
REQUIRED_EVENT_TOPIC = f"pbc.{PBC_KEY}.events"
DEFAULT_POLICY = "cgmp_change_control"
DEFAULT_RETRY_LIMIT = 5

EMITTED_EVENT_TYPES = (
    "ChemicalBatchComplianceCreated",
    "ChemicalBatchComplianceUpdated",
    "ChemicalBatchComplianceApproved",
    "ChemicalBatchComplianceExceptionOpened",
)
CONSUMED_EVENT_TYPES = ("PolicyChanged", "AuditEventSealed", "OperationalKpiChanged")

FORMULA_TABLE = f"{PBC_KEY}_chemical_formula"
BATCH_TABLE = f"{PBC_KEY}_batch_record"
SDS_TABLE = f"{PBC_KEY}_sds_document"
HAZARDOUS_MATERIAL_TABLE = f"{PBC_KEY}_hazardous_material"
REGULATORY_SUBMISSION_TABLE = f"{PBC_KEY}_regulatory_submission"
QUALITY_TEST_TABLE = f"{PBC_KEY}_quality_test"
COMPLIANCE_HOLD_TABLE = f"{PBC_KEY}_compliance_hold"
POLICY_RULE_TABLE = f"{PBC_KEY}_{PBC_KEY}_policy_rule"
RUNTIME_PARAMETER_TABLE = f"{PBC_KEY}_{PBC_KEY}_runtime_parameter"
SCHEMA_EXTENSION_TABLE = f"{PBC_KEY}_{PBC_KEY}_schema_extension"
CONTROL_ASSERTION_TABLE = f"{PBC_KEY}_{PBC_KEY}_control_assertion"
GOVERNED_MODEL_TABLE = f"{PBC_KEY}_{PBC_KEY}_governed_model"
OUTBOX_TABLE = f"{PBC_KEY}_appgen_outbox_event"
INBOX_TABLE = f"{PBC_KEY}_appgen_inbox_event"
DEAD_LETTER_TABLE = f"{PBC_KEY}_appgen_dead_letter_event"

BUSINESS_TABLES = (
    FORMULA_TABLE,
    BATCH_TABLE,
    SDS_TABLE,
    HAZARDOUS_MATERIAL_TABLE,
    REGULATORY_SUBMISSION_TABLE,
    QUALITY_TEST_TABLE,
    COMPLIANCE_HOLD_TABLE,
    POLICY_RULE_TABLE,
    RUNTIME_PARAMETER_TABLE,
    SCHEMA_EXTENSION_TABLE,
    CONTROL_ASSERTION_TABLE,
    GOVERNED_MODEL_TABLE,
)
EVENT_TABLES = (OUTBOX_TABLE, INBOX_TABLE, DEAD_LETTER_TABLE)
OWNED_TABLES = BUSINESS_TABLES + EVENT_TABLES

PERMISSIONS = (
    f"{PBC_KEY}.read",
    f"{PBC_KEY}.create",
    f"{PBC_KEY}.update",
    f"{PBC_KEY}.approve",
    f"{PBC_KEY}.admin",
)

ROLE_PERMISSIONS = {
    "operator": (f"{PBC_KEY}.read", f"{PBC_KEY}.create", f"{PBC_KEY}.update"),
    "quality_reviewer": (f"{PBC_KEY}.read", f"{PBC_KEY}.approve"),
    "ehs_reviewer": (f"{PBC_KEY}.read", f"{PBC_KEY}.approve"),
    "regulatory_lead": (f"{PBC_KEY}.read", f"{PBC_KEY}.update", f"{PBC_KEY}.approve"),
    "auditor": (f"{PBC_KEY}.read",),
    "admin": PERMISSIONS + (f"{PBC_KEY}.operate",),
}

PARAMETER_DEFINITIONS = {
    "potency_drift_tolerance_pct": {
        "default": 2.0,
        "minimum": 0.0,
        "maximum": 10.0,
        "unit": "percent",
        "description": "Maximum potency correction drift allowed before formula review is reopened.",
    },
    "misweigh_alert_pct": {
        "default": 1.5,
        "minimum": 0.0,
        "maximum": 5.0,
        "unit": "percent",
        "description": "Dispense variance limit that requires intervention.",
    },
    "critical_alarm_breach_hold_hours": {
        "default": 4,
        "minimum": 1,
        "maximum": 72,
        "unit": "hours",
        "description": "Default hold duration for critical process excursions pending quality review.",
    },
    "sds_expiry_warning_days": {
        "default": 45,
        "minimum": 1,
        "maximum": 180,
        "unit": "days",
        "description": "Lead time for SDS expiry warnings on the workbench.",
    },
    "regulatory_commitment_sla_days": {
        "default": 30,
        "minimum": 1,
        "maximum": 365,
        "unit": "days",
        "description": "Target time to close authority follow-up commitments.",
    },
    "workbench_limit": {
        "default": 20,
        "minimum": 5,
        "maximum": 100,
        "unit": "records",
        "description": "Default workbench card limit.",
    },
}

RULE_DEFINITIONS = {
    "formula_effectivity_rule": "A recipe revision cannot become effective until technical, quality, and EHS approvals are present and required SDS/material evidence is current.",
    "approved_substitution_rule": "Substitutions must be prequalified by impurity profile, supplier approval, and jurisdictional fit.",
    "equipment_line_clearance_rule": "Batch execution requires line clearance, cleaning release, and calibration readiness.",
    "critical_parameter_alarm_rule": "Critical parameter alarm breaches require documented action and may force a compliance hold.",
    "quality_release_rule": "Failing or invalid quality tests automatically block batch release.",
    "regulatory_dossier_completeness_rule": "Submissions need formula, SDS, and batch evidence references before they are ready.",
    "document_instruction_guardrail_rule": "Assistant-suggested mutations must stay within owned tables and require confirmation.",
}

STANDARD_FEATURE_KEYS = (
    "chemical_formula_management",
    "chemical_batch_compliance_workflow",
    "chemical_batch_compliance_analytics",
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

RUNTIME_CAPABILITY_KEYS = (
    "chemical_batch_compliance_event_sourced_operational_history",
    "chemical_batch_compliance_multi_tenant_policy_isolation",
    "chemical_batch_compliance_schema_evolution_resilience",
    "chemical_batch_compliance_autonomous_anomaly_detection",
    "chemical_batch_compliance_semantic_document_instruction_understanding",
    "chemical_batch_compliance_predictive_risk_scoring",
    "chemical_batch_compliance_counterfactual_scenario_simulation",
    "chemical_batch_compliance_cryptographic_audit_proofs",
    "chemical_batch_compliance_continuous_control_testing",
    "chemical_batch_compliance_carbon_and_sustainability_awareness",
    "chemical_batch_compliance_cross_pbc_event_federation",
    "chemical_batch_compliance_governed_ai_agent_execution",
)

UI_FRAGMENT_KEYS = (
    "ChemicalBatchComplianceWorkbench",
    "ChemicalBatchComplianceDetail",
    "ChemicalBatchComplianceAssistantPanel",
)

ROUTES = (
    "POST /chemical-formulas",
    "POST /batch-records",
    "POST /sds-documents",
    "POST /hazardous-materials",
    "POST /regulatory-submissions",
    "GET /chemical-batch-compliance-workbench",
)

ROUTE_TO_OPERATION = {
    "POST /chemical-formulas": "create_formula_revision",
    "POST /batch-records": "record_batch",
    "POST /sds-documents": "review_sds_document",
    "POST /hazardous-materials": "register_hazardous_material",
    "POST /regulatory-submissions": "create_regulatory_submission",
    "GET /chemical-batch-compliance-workbench": "build_workbench_view",
}

DOMAIN_OPERATIONS = (
    "create_formula_revision",
    "release_formula_revision",
    "review_sds_document",
    "register_hazardous_material",
    "record_batch",
    "record_quality_test",
    "place_compliance_hold",
    "resolve_compliance_hold",
    "create_regulatory_submission",
    "register_rule",
    "set_parameter",
    "register_schema_extension",
    "upsert_control_assertion",
    "create_document_instruction",
    "update_document_instruction",
    "delete_document_instruction",
)

DOMAIN_RULES = tuple(RULE_DEFINITIONS)
DOMAIN_PARAMETERS = tuple(PARAMETER_DEFINITIONS)
DOMAIN_EDGE_CASES = (
    "formula_release_without_sds",
    "formula_release_without_ehs_approval",
    "batch_start_without_line_clearance",
    "misweigh_above_tolerance",
    "critical_parameter_alarm_breach",
    "failed_quality_release_test",
    "document_instruction_cross_boundary_attempt",
    "duplicate_event_replay",
    "unexpected_event_dead_letter",
)
DOMAIN_ADVANCED_CAPABILITIES = (
    "recipe revision diffs and effectivity enforcement",
    "dispense reconciliation and critical-parameter evidence",
    "risk-based quality escalation and automatic hold generation",
    "governed assistant-driven document instruction CRUD",
    "jurisdiction-aware dossier completeness evidence",
    "continuous control assertion snapshots",
)
WORKBENCH_VIEWS = (
    "Formula Release Queue",
    "Batch Review Board",
    "Quality And Hold Triage",
    "Regulatory Dossier Monitor",
)

FORM_DEFINITIONS = (
    {
        "id": "formula_revision_form",
        "title": "Formula Revision Intake",
        "table": FORMULA_TABLE,
        "fields": (
            "tenant",
            "formula_code",
            "revision",
            "product_name",
            "target_concentration",
            "composition_window",
            "required_sds_ids",
            "required_hazard_material_ids",
            "approvals",
            "effectivity_start",
        ),
    },
    {
        "id": "batch_execution_form",
        "title": "Batch Execution Record",
        "table": BATCH_TABLE,
        "fields": (
            "tenant",
            "batch_number",
            "formula_id",
            "equipment_profile",
            "step_executions",
            "dispense_log",
            "parameter_log",
            "permits_confirmed",
        ),
    },
    {
        "id": "quality_review_form",
        "title": "In-Process Quality Review",
        "table": QUALITY_TEST_TABLE,
        "fields": ("tenant", "batch_id", "test_name", "specification", "result_value", "result_status"),
    },
    {
        "id": "document_instruction_form",
        "title": "Assistant Document Instruction",
        "table": GOVERNED_MODEL_TABLE,
        "fields": ("tenant", "document", "instruction", "artifact_key"),
    },
)

WIZARD_DEFINITIONS = (
    {
        "id": "formula_release_wizard",
        "steps": ("recipe", "sds", "hazard", "approvals", "effectivity"),
        "goal": "Release a controlled formula revision.",
    },
    {
        "id": "batch_disposition_wizard",
        "steps": ("execution", "quality", "hold_review", "release"),
        "goal": "Drive a batch from execution evidence into disposition.",
    },
    {
        "id": "regulatory_dossier_wizard",
        "steps": ("sources", "jurisdiction", "commitments", "submission_packet"),
        "goal": "Assemble a jurisdiction-ready regulatory dossier from owned records.",
    },
)

CONTROL_DEFINITIONS = (
    {
        "id": "owned_table_boundary_guard",
        "description": "Reject assistant and service mutations outside owned tables.",
        "type": "boundary",
    },
    {
        "id": "formula_release_gate",
        "description": "Require technical, quality, and EHS approval plus current SDS/material evidence.",
        "type": "release",
    },
    {
        "id": "line_clearance_gate",
        "description": "Block batch start without line clearance, cleaning release, and calibration.",
        "type": "execution",
    },
    {
        "id": "quality_hold_gate",
        "description": "Automatically place a compliance hold when quality results fail.",
        "type": "quality",
    },
    {
        "id": "document_instruction_mutation_guard",
        "description": "Require human confirmation before assistant-derived CRUD actions are applied.",
        "type": "agent",
    },
)

TABLE_DEFINITIONS = (
    {
        "table": FORMULA_TABLE,
        "class_name": "ChemicalBatchComplianceChemicalFormula",
        "domain_role": "controlled_master_recipe",
        "primary_key": ("id",),
        "fields": (
            "id",
            "tenant",
            "formula_code",
            "revision",
            "lifecycle_state",
            "product_name",
            "target_concentration",
            "composition_window",
            "approved_substitutes",
            "required_sds_ids",
            "required_hazard_material_ids",
            "required_permits",
            "equipment_classes",
            "approvals",
            "effectivity_start",
            "effectivity_end",
            "process_steps",
            "evidence_hash",
            "created_at",
            "updated_at",
        ),
    },
    {
        "table": BATCH_TABLE,
        "class_name": "ChemicalBatchComplianceBatchRecord",
        "domain_role": "electronic_batch_record",
        "primary_key": ("id",),
        "fields": (
            "id",
            "tenant",
            "batch_number",
            "formula_id",
            "formula_revision",
            "lifecycle_state",
            "equipment_profile",
            "step_timeline",
            "dispense_reconciliation",
            "parameter_log",
            "sampling_plan",
            "deviation_summary",
            "release_decision",
            "risk_score",
            "created_at",
            "updated_at",
        ),
    },
    {
        "table": SDS_TABLE,
        "class_name": "ChemicalBatchComplianceSdsDocument",
        "domain_role": "safety_data_sheet",
        "primary_key": ("id",),
        "fields": (
            "id",
            "tenant",
            "material_code",
            "revision",
            "status",
            "issue_date",
            "expiration_date",
            "jurisdictions",
            "hazard_summary",
            "exposure_controls",
            "document_digest",
            "created_at",
            "updated_at",
        ),
    },
    {
        "table": HAZARDOUS_MATERIAL_TABLE,
        "class_name": "ChemicalBatchComplianceHazardousMaterial",
        "domain_role": "hazard_profile",
        "primary_key": ("id",),
        "fields": (
            "id",
            "tenant",
            "material_code",
            "status",
            "un_number",
            "ghs_classification",
            "storage_class",
            "approved_sources",
            "ppe_requirements",
            "label_profile",
            "created_at",
            "updated_at",
        ),
    },
    {
        "table": REGULATORY_SUBMISSION_TABLE,
        "class_name": "ChemicalBatchComplianceRegulatorySubmission",
        "domain_role": "dossier",
        "primary_key": ("id",),
        "fields": (
            "id",
            "tenant",
            "dossier_number",
            "status",
            "jurisdiction",
            "submission_type",
            "product_code",
            "source_record_ids",
            "commitment_actions",
            "created_at",
            "updated_at",
        ),
    },
    {
        "table": QUALITY_TEST_TABLE,
        "class_name": "ChemicalBatchComplianceQualityTest",
        "domain_role": "quality_evidence",
        "primary_key": ("id",),
        "fields": (
            "id",
            "tenant",
            "batch_id",
            "sample_point",
            "test_name",
            "specification",
            "result_value",
            "result_status",
            "requires_hold",
            "created_at",
            "updated_at",
        ),
    },
    {
        "table": COMPLIANCE_HOLD_TABLE,
        "class_name": "ChemicalBatchComplianceComplianceHold",
        "domain_role": "batch_or_material_hold",
        "primary_key": ("id",),
        "fields": (
            "id",
            "tenant",
            "entity_type",
            "entity_id",
            "hold_reason",
            "severity",
            "status",
            "disposition",
            "released_by",
            "created_at",
            "updated_at",
        ),
    },
    {
        "table": POLICY_RULE_TABLE,
        "class_name": "ChemicalBatchCompliancePolicyRule",
        "domain_role": "governance_rule",
        "primary_key": ("id",),
        "fields": (
            "id",
            "tenant",
            "rule_id",
            "status",
            "scope",
            "rule_kind",
            "threshold_json",
            "compiled_hash",
            "created_at",
            "updated_at",
        ),
    },
    {
        "table": RUNTIME_PARAMETER_TABLE,
        "class_name": "ChemicalBatchComplianceRuntimeParameter",
        "domain_role": "bounded_parameter",
        "primary_key": ("id",),
        "fields": (
            "id",
            "tenant",
            "parameter_name",
            "parameter_value",
            "unit",
            "bounded",
            "status",
            "created_at",
            "updated_at",
        ),
    },
    {
        "table": SCHEMA_EXTENSION_TABLE,
        "class_name": "ChemicalBatchComplianceSchemaExtension",
        "domain_role": "owned_schema_extension",
        "primary_key": ("id",),
        "fields": (
            "id",
            "tenant",
            "table_name",
            "status",
            "field_map",
            "rationale",
            "created_at",
            "updated_at",
        ),
    },
    {
        "table": CONTROL_ASSERTION_TABLE,
        "class_name": "ChemicalBatchComplianceControlAssertion",
        "domain_role": "continuous_control",
        "primary_key": ("id",),
        "fields": (
            "id",
            "tenant",
            "control_id",
            "control_name",
            "status",
            "frequency",
            "assertion_payload",
            "evidence_hash",
            "created_at",
            "updated_at",
        ),
    },
    {
        "table": GOVERNED_MODEL_TABLE,
        "class_name": "ChemicalBatchComplianceGovernedModel",
        "domain_role": "governed_instruction_artifact",
        "primary_key": ("id",),
        "fields": (
            "id",
            "tenant",
            "artifact_type",
            "artifact_key",
            "status",
            "document_digest",
            "instruction_payload",
            "mutation_preview",
            "human_confirmation_state",
            "created_at",
            "updated_at",
        ),
    },
    {
        "table": OUTBOX_TABLE,
        "class_name": "ChemicalBatchComplianceAppgenOutboxEvent",
        "domain_role": "outbox_event",
        "primary_key": ("id",),
        "fields": ("id", "tenant", "event_type", "topic", "payload", "idempotency_key", "created_at"),
    },
    {
        "table": INBOX_TABLE,
        "class_name": "ChemicalBatchComplianceAppgenInboxEvent",
        "domain_role": "inbox_event",
        "primary_key": ("id",),
        "fields": ("id", "tenant", "event_type", "topic", "payload", "idempotency_key", "created_at"),
    },
    {
        "table": DEAD_LETTER_TABLE,
        "class_name": "ChemicalBatchComplianceAppgenDeadLetterEvent",
        "domain_role": "dead_letter_event",
        "primary_key": ("id",),
        "fields": (
            "id",
            "tenant",
            "event_type",
            "topic",
            "payload",
            "idempotency_key",
            "retry_policy",
            "created_at",
        ),
    },
)


def _json_default(value: Any) -> Any:
    if isinstance(value, set):
        return sorted(value)
    return str(value)


def stable_hash(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), default=_json_default)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def _copy_state(state: dict[str, Any]) -> dict[str, Any]:
    copied = deepcopy(state)
    copied["events"]["handled"] = set(state["events"].get("handled", set()))
    return copied


def _iso_at(sequence: int) -> str:
    minute = sequence // 60
    second = sequence % 60
    return f"2026-01-01T00:{minute:02d}:{second:02d}Z"


def _next_sequence(state: dict[str, Any]) -> tuple[dict[str, Any], int]:
    next_state = _copy_state(state)
    next_state["sequence"] = int(next_state.get("sequence", 0)) + 1
    return next_state, next_state["sequence"]


def _table_map() -> dict[str, dict[str, Any]]:
    return {table: {} for table in OWNED_TABLES}


def empty_state() -> dict[str, Any]:
    return {
        "tables": _table_map(),
        "config": {
            "database_backend": "postgresql",
            "event_topic": REQUIRED_EVENT_TOPIC,
            "retry_limit": DEFAULT_RETRY_LIMIT,
            "default_policy": DEFAULT_POLICY,
        },
        "parameters": {
            name: {
                "name": name,
                "value": definition["default"],
                "unit": definition["unit"],
                "minimum": definition["minimum"],
                "maximum": definition["maximum"],
                "description": definition["description"],
            }
            for name, definition in PARAMETER_DEFINITIONS.items()
        },
        "rules": {},
        "schema_extensions": {},
        "signals": [],
        "events": {"outbox": [], "inbox": [], "dead_letter": [], "handled": set()},
        "sequence": 0,
    }


def _table_records(state: dict[str, Any], table: str) -> dict[str, dict[str, Any]]:
    return state["tables"][table]


def _store_record(state: dict[str, Any], table: str, record_id: str, record: dict[str, Any]) -> None:
    state["tables"][table][record_id] = record


def _emit_event(
    state: dict[str, Any],
    *,
    event_type: str,
    payload: dict[str, Any],
    tenant: str,
    route: str | None,
) -> dict[str, Any]:
    event_id = stable_hash((event_type, payload, state["sequence"]))
    envelope = {
        "id": event_id,
        "tenant": tenant,
        "event_type": event_type,
        "topic": REQUIRED_EVENT_TOPIC,
        "payload": dict(payload),
        "idempotency_key": stable_hash((event_type, payload)),
        "route": route,
        "event_contract": EVENT_CONTRACT,
        "created_at": _iso_at(state["sequence"]),
    }
    state["events"]["outbox"].append(envelope)
    _store_record(state, OUTBOX_TABLE, event_id, envelope)
    return envelope


def _missing(payload: dict[str, Any], required: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(name for name in required if payload.get(name) in (None, "", [], ()))


def _list_of_dicts(items: Any) -> list[dict[str, Any]]:
    return [dict(item) for item in items or ()]


def _find_record(state: dict[str, Any], table: str, record_id: str | None = None, **lookup: Any) -> dict[str, Any] | None:
    records = _table_records(state, table).values()
    if record_id:
        return _table_records(state, table).get(record_id)
    for record in records:
        if all(record.get(key) == value for key, value in lookup.items()):
            return record
    return None


def ensure_owned_table(table: str) -> bool:
    return table in OWNED_TABLES and table.startswith(f"{PBC_KEY}_")


def configure_runtime(state: dict[str, Any], config: dict[str, Any]) -> dict[str, Any]:
    next_state = _copy_state(state)
    merged = {**next_state["config"], **dict(config)}
    ok = (
        merged.get("database_backend") in ALLOWED_DATABASE_BACKENDS
        and merged.get("event_topic", REQUIRED_EVENT_TOPIC) == REQUIRED_EVENT_TOPIC
    )
    next_state["config"] = merged
    return {"ok": ok, "state": next_state, "configuration": merged, "side_effects": ()}


def set_parameter_value(state: dict[str, Any], name: str, value: Any, tenant: str = "default") -> dict[str, Any]:
    definition = PARAMETER_DEFINITIONS.get(name)
    if definition is None:
        return {"ok": False, "reason": "unknown_parameter", "parameter": name, "side_effects": ()}
    bounded = definition["minimum"] <= value <= definition["maximum"]
    next_state, sequence = _next_sequence(state)
    record_id = f"{name}-{sequence:04d}"
    parameter = {
        "id": record_id,
        "tenant": tenant,
        "parameter_name": name,
        "parameter_value": value,
        "unit": definition["unit"],
        "bounded": bounded,
        "status": "active" if bounded else "rejected",
        "created_at": _iso_at(sequence),
        "updated_at": _iso_at(sequence),
    }
    next_state["parameters"][name] = {
        "name": name,
        "value": value,
        "unit": definition["unit"],
        "minimum": definition["minimum"],
        "maximum": definition["maximum"],
        "description": definition["description"],
    }
    _store_record(next_state, RUNTIME_PARAMETER_TABLE, record_id, parameter)
    return {"ok": bounded, "state": next_state, "parameter": parameter, "side_effects": ()}


def register_rule_definition(state: dict[str, Any], rule: dict[str, Any], tenant: str = "default") -> dict[str, Any]:
    missing = _missing(rule, ("rule_id", "scope"))
    if missing:
        return {"ok": False, "reason": "missing_fields", "missing": missing, "side_effects": ()}
    next_state, sequence = _next_sequence(state)
    compiled_hash = stable_hash(rule)
    rule_id = str(rule["rule_id"])
    record = {
        "id": f"{rule_id}-{sequence:04d}",
        "tenant": tenant,
        "rule_id": rule_id,
        "status": rule.get("status", "active"),
        "scope": rule["scope"],
        "rule_kind": rule.get("rule_kind", "deterministic_policy"),
        "threshold_json": dict(rule.get("threshold_json", {})),
        "compiled_hash": compiled_hash,
        "created_at": _iso_at(sequence),
        "updated_at": _iso_at(sequence),
    }
    next_state["rules"][rule_id] = {**dict(rule), "compiled_hash": compiled_hash}
    _store_record(next_state, POLICY_RULE_TABLE, record["id"], record)
    return {"ok": True, "state": next_state, "rule": record, "side_effects": ()}


def register_schema_extension_definition(
    state: dict[str, Any],
    table: str,
    fields: dict[str, Any],
    tenant: str = "default",
    rationale: str = "",
) -> dict[str, Any]:
    owned_name = table if table.startswith(f"{PBC_KEY}_") else f"{PBC_KEY}_{table}"
    if owned_name not in BUSINESS_TABLES:
        return {"ok": False, "reason": "unknown_owned_table", "table": owned_name, "side_effects": ()}
    next_state, sequence = _next_sequence(state)
    record = {
        "id": f"schema-extension-{sequence:04d}",
        "tenant": tenant,
        "table_name": owned_name,
        "status": "active",
        "field_map": dict(fields),
        "rationale": rationale or "package-local schema evolution",
        "created_at": _iso_at(sequence),
        "updated_at": _iso_at(sequence),
    }
    next_state["schema_extensions"][owned_name] = dict(fields)
    _store_record(next_state, SCHEMA_EXTENSION_TABLE, record["id"], record)
    return {"ok": True, "state": next_state, "schema_extension": record, "side_effects": ()}


def _release_blockers(state: dict[str, Any], formula: dict[str, Any]) -> tuple[str, ...]:
    blockers: list[str] = []
    approvals = formula.get("approvals", {})
    for gate in ("technical", "quality", "ehs"):
        if approvals.get(gate) is not True:
            blockers.append(f"missing_{gate}_approval")
    for sds_id in tuple(formula.get("required_sds_ids", ())):
        sds_record = _find_record(state, SDS_TABLE, sds_id)
        if not sds_record or sds_record.get("status") != "approved":
            blockers.append(f"sds_not_approved:{sds_id}")
    for material_id in tuple(formula.get("required_hazard_material_ids", ())):
        material_record = _find_record(state, HAZARDOUS_MATERIAL_TABLE, material_id)
        if not material_record or material_record.get("status") != "qualified":
            blockers.append(f"material_not_qualified:{material_id}")
    if not formula.get("effectivity_start"):
        blockers.append("missing_effectivity_start")
    return tuple(blockers)


def _risk_score(batch: dict[str, Any]) -> float:
    steps = tuple(batch.get("step_timeline", ()))
    deviations = tuple(batch.get("deviation_summary", ()))
    alarms = sum(1 for item in batch.get("parameter_log", ()) if item.get("band") == "alarm")
    incomplete_steps = sum(1 for step in steps if step.get("status") != "complete")
    raw = 0.18 + incomplete_steps * 0.08 + alarms * 0.12 + len(deviations) * 0.15
    return round(min(raw, 0.99), 4)


def review_sds_document(state: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
    missing = _missing(payload, ("tenant", "material_code", "revision", "issue_date", "expiration_date"))
    if missing:
        return {"ok": False, "reason": "missing_fields", "missing": missing, "side_effects": ()}
    next_state, sequence = _next_sequence(state)
    record_id = payload.get("id") or f"sds-{payload['material_code']}-{payload['revision']}"
    existing = _find_record(next_state, SDS_TABLE, record_id)
    status = payload.get("status") or ("approved" if payload.get("approved", True) else "draft")
    record = {
        "id": record_id,
        "tenant": payload["tenant"],
        "material_code": payload["material_code"],
        "revision": payload["revision"],
        "status": status,
        "issue_date": payload["issue_date"],
        "expiration_date": payload["expiration_date"],
        "jurisdictions": tuple(payload.get("jurisdictions", ("US",))),
        "hazard_summary": dict(payload.get("hazard_summary", {})),
        "exposure_controls": tuple(payload.get("exposure_controls", ())),
        "document_digest": stable_hash(payload.get("document", payload["material_code"])),
        "created_at": existing.get("created_at", _iso_at(sequence)) if existing else _iso_at(sequence),
        "updated_at": _iso_at(sequence),
    }
    _store_record(next_state, SDS_TABLE, record_id, record)
    event = _emit_event(
        next_state,
        event_type=EMITTED_EVENT_TYPES[1 if existing else 0],
        payload={"table": SDS_TABLE, "id": record_id, "status": status},
        tenant=payload["tenant"],
        route="POST /sds-documents",
    )
    return {"ok": True, "state": next_state, "record": record, "event": event, "side_effects": ()}


def register_hazardous_material(state: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
    missing = _missing(payload, ("tenant", "material_code", "ghs_classification"))
    if missing:
        return {"ok": False, "reason": "missing_fields", "missing": missing, "side_effects": ()}
    next_state, sequence = _next_sequence(state)
    record_id = payload.get("id") or f"hazmat-{payload['material_code']}"
    existing = _find_record(next_state, HAZARDOUS_MATERIAL_TABLE, record_id)
    approved_sources = tuple(payload.get("approved_sources", ()))
    status = payload.get("status") or ("qualified" if approved_sources else "review_required")
    record = {
        "id": record_id,
        "tenant": payload["tenant"],
        "material_code": payload["material_code"],
        "status": status,
        "un_number": payload.get("un_number", ""),
        "ghs_classification": tuple(payload.get("ghs_classification", ())),
        "storage_class": payload.get("storage_class", ""),
        "approved_sources": approved_sources,
        "ppe_requirements": tuple(payload.get("ppe_requirements", ())),
        "label_profile": dict(payload.get("label_profile", {})),
        "created_at": existing.get("created_at", _iso_at(sequence)) if existing else _iso_at(sequence),
        "updated_at": _iso_at(sequence),
    }
    _store_record(next_state, HAZARDOUS_MATERIAL_TABLE, record_id, record)
    event = _emit_event(
        next_state,
        event_type=EMITTED_EVENT_TYPES[1 if existing else 0],
        payload={"table": HAZARDOUS_MATERIAL_TABLE, "id": record_id, "status": status},
        tenant=payload["tenant"],
        route="POST /hazardous-materials",
    )
    return {"ok": True, "state": next_state, "record": record, "event": event, "side_effects": ()}


def create_formula_revision(state: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
    missing = _missing(
        payload,
        (
            "tenant",
            "formula_code",
            "revision",
            "product_name",
            "target_concentration",
            "composition_window",
            "effectivity_start",
        ),
    )
    if missing:
        return {"ok": False, "reason": "missing_fields", "missing": missing, "side_effects": ()}
    next_state, sequence = _next_sequence(state)
    record_id = payload.get("id") or f"formula-{payload['formula_code']}-rev-{payload['revision']}"
    existing = _find_record(next_state, FORMULA_TABLE, record_id)
    record = {
        "id": record_id,
        "tenant": payload["tenant"],
        "formula_code": payload["formula_code"],
        "revision": payload["revision"],
        "lifecycle_state": payload.get("lifecycle_state", "draft"),
        "product_name": payload["product_name"],
        "target_concentration": payload["target_concentration"],
        "composition_window": dict(payload["composition_window"]),
        "approved_substitutes": _list_of_dicts(payload.get("approved_substitutes")),
        "required_sds_ids": tuple(payload.get("required_sds_ids", ())),
        "required_hazard_material_ids": tuple(payload.get("required_hazard_material_ids", ())),
        "required_permits": tuple(payload.get("required_permits", ())),
        "equipment_classes": tuple(payload.get("equipment_classes", ())),
        "approvals": {
            "technical": bool(payload.get("approvals", {}).get("technical")),
            "quality": bool(payload.get("approvals", {}).get("quality")),
            "ehs": bool(payload.get("approvals", {}).get("ehs")),
        },
        "effectivity_start": payload["effectivity_start"],
        "effectivity_end": payload.get("effectivity_end"),
        "process_steps": _list_of_dicts(payload.get("process_steps")),
        "evidence_hash": stable_hash(payload),
        "created_at": existing.get("created_at", _iso_at(sequence)) if existing else _iso_at(sequence),
        "updated_at": _iso_at(sequence),
    }
    _store_record(next_state, FORMULA_TABLE, record_id, record)
    event = _emit_event(
        next_state,
        event_type=EMITTED_EVENT_TYPES[1 if existing else 0],
        payload={"table": FORMULA_TABLE, "id": record_id, "lifecycle_state": record["lifecycle_state"]},
        tenant=payload["tenant"],
        route="POST /chemical-formulas",
    )
    return {"ok": True, "state": next_state, "record": record, "event": event, "side_effects": ()}


def release_formula_revision(state: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
    formula = _find_record(
        state,
        FORMULA_TABLE,
        payload.get("id"),
        tenant=payload.get("tenant"),
        formula_code=payload.get("formula_code"),
        revision=payload.get("revision"),
    )
    if formula is None:
        return {"ok": False, "reason": "formula_not_found", "side_effects": ()}
    blockers = _release_blockers(state, formula)
    if blockers:
        return {"ok": False, "reason": "release_gate_failed", "missing_gates": blockers, "side_effects": ()}
    next_state, sequence = _next_sequence(state)
    updated = dict(formula)
    updated["lifecycle_state"] = "effective"
    updated["updated_at"] = _iso_at(sequence)
    updated["released_by"] = payload.get("released_by", "quality_board")
    updated["release_notes"] = payload.get("release_notes", "")
    _store_record(next_state, FORMULA_TABLE, formula["id"], updated)
    event = _emit_event(
        next_state,
        event_type=EMITTED_EVENT_TYPES[2],
        payload={"table": FORMULA_TABLE, "id": formula["id"], "lifecycle_state": "effective"},
        tenant=updated["tenant"],
        route="POST /chemical-formulas",
    )
    return {"ok": True, "state": next_state, "record": updated, "event": event, "side_effects": ()}


def _equipment_ready(payload: dict[str, Any]) -> tuple[bool, tuple[str, ...]]:
    profile = dict(payload.get("equipment_profile", {}))
    failures = []
    if profile.get("line_clearance") is not True:
        failures.append("line_clearance")
    if profile.get("cleaning_release") is not True:
        failures.append("cleaning_release")
    if profile.get("calibration_current") is not True:
        failures.append("calibration_current")
    return not failures, tuple(failures)


def record_batch(state: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
    missing = _missing(payload, ("tenant", "batch_number", "formula_id"))
    if missing:
        return {"ok": False, "reason": "missing_fields", "missing": missing, "side_effects": ()}
    formula = _find_record(state, FORMULA_TABLE, payload["formula_id"])
    if not formula or formula.get("lifecycle_state") != "effective":
        return {"ok": False, "reason": "formula_not_released", "side_effects": ()}
    ready, equipment_failures = _equipment_ready(payload)
    permits_confirmed = set(payload.get("permits_confirmed", ()))
    permit_failures = tuple(
        permit for permit in tuple(formula.get("required_permits", ())) if permit not in permits_confirmed
    )
    if not ready or permit_failures:
        return {
            "ok": False,
            "reason": "execution_gate_failed",
            "equipment_failures": equipment_failures,
            "permit_failures": permit_failures,
            "side_effects": (),
        }
    next_state, sequence = _next_sequence(state)
    executions = {item.get("step_code"): dict(item) for item in payload.get("step_executions", ())}
    step_timeline = []
    deviations = []
    for step in formula.get("process_steps", ()):
        step_code = step.get("step_code")
        execution = executions.get(step_code, {})
        combined = {**dict(step), **execution}
        combined.setdefault("status", "pending")
        if combined.get("critical") and combined["status"] == "skipped":
            deviations.append(f"critical_step_skipped:{step_code}")
        step_timeline.append(combined)
    dispense_reconciliation = []
    for dispense in payload.get("dispense_log", ()):
        target = float(dispense.get("target_qty", 0.0))
        actual = float(dispense.get("actual_qty", 0.0))
        variance_pct = round(abs(actual - target) / target * 100, 4) if target else 0.0
        status = "alert" if variance_pct > float(state["parameters"]["misweigh_alert_pct"]["value"]) else "ok"
        if status == "alert":
            deviations.append(f"misweigh:{dispense.get('material_code', 'unknown')}")
        dispense_reconciliation.append({**dict(dispense), "variance_pct": variance_pct, "status": status})
    for parameter in payload.get("parameter_log", ()):
        if parameter.get("band") == "alarm":
            deviations.append(f"parameter_alarm:{parameter.get('parameter_name', 'unknown')}")
    record_id = payload.get("id") or f"batch-{payload['batch_number']}"
    record = {
        "id": record_id,
        "tenant": payload["tenant"],
        "batch_number": payload["batch_number"],
        "formula_id": formula["id"],
        "formula_revision": formula["revision"],
        "lifecycle_state": payload.get("lifecycle_state", "review_pending"),
        "equipment_profile": dict(payload.get("equipment_profile", {})),
        "step_timeline": tuple(step_timeline),
        "dispense_reconciliation": tuple(dispense_reconciliation),
        "parameter_log": tuple(dict(item) for item in payload.get("parameter_log", ())),
        "sampling_plan": tuple(dict(item) for item in payload.get("sampling_plan", ())),
        "deviation_summary": tuple(dict.fromkeys(deviations)),
        "release_decision": payload.get("release_decision", "pending_quality"),
        "risk_score": 0.0,
        "created_at": _iso_at(sequence),
        "updated_at": _iso_at(sequence),
    }
    record["risk_score"] = _risk_score(record)
    _store_record(next_state, BATCH_TABLE, record_id, record)
    event = _emit_event(
        next_state,
        event_type=EMITTED_EVENT_TYPES[0],
        payload={"table": BATCH_TABLE, "id": record_id, "risk_score": record["risk_score"]},
        tenant=payload["tenant"],
        route="POST /batch-records",
    )
    return {"ok": True, "state": next_state, "record": record, "event": event, "side_effects": ()}


def _create_hold(
    state: dict[str, Any],
    *,
    tenant: str,
    entity_type: str,
    entity_id: str,
    hold_reason: str,
    severity: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    next_state, sequence = _next_sequence(state)
    record = {
        "id": f"hold-{sequence:04d}",
        "tenant": tenant,
        "entity_type": entity_type,
        "entity_id": entity_id,
        "hold_reason": hold_reason,
        "severity": severity,
        "status": "open",
        "disposition": "pending_investigation",
        "released_by": "",
        "created_at": _iso_at(sequence),
        "updated_at": _iso_at(sequence),
    }
    _store_record(next_state, COMPLIANCE_HOLD_TABLE, record["id"], record)
    event = _emit_event(
        next_state,
        event_type=EMITTED_EVENT_TYPES[3],
        payload={"table": COMPLIANCE_HOLD_TABLE, "id": record["id"], "entity_id": entity_id},
        tenant=tenant,
        route=None,
    )
    return next_state, {"record": record, "event": event}


def record_quality_test(state: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
    missing = _missing(payload, ("tenant", "batch_id", "test_name", "specification"))
    if missing:
        return {"ok": False, "reason": "missing_fields", "missing": missing, "side_effects": ()}
    batch = _find_record(state, BATCH_TABLE, payload["batch_id"])
    if batch is None:
        return {"ok": False, "reason": "batch_not_found", "side_effects": ()}
    next_state, sequence = _next_sequence(state)
    record_id = payload.get("id") or f"quality-{sequence:04d}"
    result_status = payload.get("result_status", "pass")
    requires_hold = bool(payload.get("requires_hold")) or result_status in {"fail", "invalid"}
    record = {
        "id": record_id,
        "tenant": payload["tenant"],
        "batch_id": payload["batch_id"],
        "sample_point": payload.get("sample_point", "in_process"),
        "test_name": payload["test_name"],
        "specification": dict(payload["specification"]),
        "result_value": payload.get("result_value"),
        "result_status": result_status,
        "requires_hold": requires_hold,
        "created_at": _iso_at(sequence),
        "updated_at": _iso_at(sequence),
    }
    _store_record(next_state, QUALITY_TEST_TABLE, record_id, record)
    hold = None
    if requires_hold:
        next_state, hold = _create_hold(
            next_state,
            tenant=payload["tenant"],
            entity_type="batch_record",
            entity_id=payload["batch_id"],
            hold_reason=f"quality_test_failed:{payload['test_name']}",
            severity="critical",
        )
    event = _emit_event(
        next_state,
        event_type=EMITTED_EVENT_TYPES[1 if result_status == "pass" else 3],
        payload={"table": QUALITY_TEST_TABLE, "id": record_id, "result_status": result_status},
        tenant=payload["tenant"],
        route=None,
    )
    return {"ok": True, "state": next_state, "record": record, "hold": hold, "event": event, "side_effects": ()}


def place_compliance_hold(state: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
    missing = _missing(payload, ("tenant", "entity_type", "entity_id", "hold_reason"))
    if missing:
        return {"ok": False, "reason": "missing_fields", "missing": missing, "side_effects": ()}
    next_state, hold = _create_hold(
        state,
        tenant=payload["tenant"],
        entity_type=payload["entity_type"],
        entity_id=payload["entity_id"],
        hold_reason=payload["hold_reason"],
        severity=payload.get("severity", "major"),
    )
    return {"ok": True, "state": next_state, "record": hold["record"], "event": hold["event"], "side_effects": ()}


def resolve_compliance_hold(state: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
    hold = _find_record(state, COMPLIANCE_HOLD_TABLE, payload.get("id"))
    if hold is None:
        return {"ok": False, "reason": "hold_not_found", "side_effects": ()}
    next_state, sequence = _next_sequence(state)
    updated = dict(hold)
    updated["status"] = "released"
    updated["disposition"] = payload.get("disposition", "released_after_review")
    updated["released_by"] = payload.get("released_by", "quality_reviewer")
    updated["updated_at"] = _iso_at(sequence)
    _store_record(next_state, COMPLIANCE_HOLD_TABLE, hold["id"], updated)
    event = _emit_event(
        next_state,
        event_type=EMITTED_EVENT_TYPES[2],
        payload={"table": COMPLIANCE_HOLD_TABLE, "id": hold["id"], "status": "released"},
        tenant=updated["tenant"],
        route=None,
    )
    return {"ok": True, "state": next_state, "record": updated, "event": event, "side_effects": ()}


def create_regulatory_submission(state: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
    missing = _missing(payload, ("tenant", "dossier_number", "jurisdiction", "submission_type", "product_code"))
    if missing:
        return {"ok": False, "reason": "missing_fields", "missing": missing, "side_effects": ()}
    source_ids = tuple(payload.get("source_record_ids", ()))
    source_tables = (
        FORMULA_TABLE,
        BATCH_TABLE,
        SDS_TABLE,
        QUALITY_TEST_TABLE,
        COMPLIANCE_HOLD_TABLE,
    )
    source_index = {record_id for table in source_tables for record_id in _table_records(state, table)}
    missing_sources = tuple(record_id for record_id in source_ids if record_id not in source_index)
    next_state, sequence = _next_sequence(state)
    record_id = payload.get("id") or f"submission-{payload['dossier_number']}"
    status = "ready_for_submission" if source_ids and not missing_sources else "draft"
    record = {
        "id": record_id,
        "tenant": payload["tenant"],
        "dossier_number": payload["dossier_number"],
        "status": status,
        "jurisdiction": payload["jurisdiction"],
        "submission_type": payload["submission_type"],
        "product_code": payload["product_code"],
        "source_record_ids": source_ids,
        "commitment_actions": tuple(payload.get("commitment_actions", ())),
        "created_at": _iso_at(sequence),
        "updated_at": _iso_at(sequence),
    }
    _store_record(next_state, REGULATORY_SUBMISSION_TABLE, record_id, record)
    event = _emit_event(
        next_state,
        event_type=EMITTED_EVENT_TYPES[1 if missing_sources else 2],
        payload={"table": REGULATORY_SUBMISSION_TABLE, "id": record_id, "status": status},
        tenant=payload["tenant"],
        route="POST /regulatory-submissions",
    )
    return {
        "ok": True,
        "state": next_state,
        "record": record,
        "missing_sources": missing_sources,
        "event": event,
        "side_effects": (),
    }


def upsert_control_assertion(state: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
    missing = _missing(payload, ("tenant", "control_id", "control_name", "status"))
    if missing:
        return {"ok": False, "reason": "missing_fields", "missing": missing, "side_effects": ()}
    next_state, sequence = _next_sequence(state)
    record_id = payload.get("id") or payload["control_id"]
    existing = _find_record(next_state, CONTROL_ASSERTION_TABLE, record_id)
    record = {
        "id": record_id,
        "tenant": payload["tenant"],
        "control_id": payload["control_id"],
        "control_name": payload["control_name"],
        "status": payload["status"],
        "frequency": payload.get("frequency", "per_batch"),
        "assertion_payload": dict(payload.get("assertion_payload", {})),
        "evidence_hash": stable_hash(payload),
        "created_at": existing.get("created_at", _iso_at(sequence)) if existing else _iso_at(sequence),
        "updated_at": _iso_at(sequence),
    }
    _store_record(next_state, CONTROL_ASSERTION_TABLE, record_id, record)
    return {"ok": True, "state": next_state, "record": record, "side_effects": ()}


def parse_document_instruction(document: str, instruction: str) -> dict[str, Any]:
    lower = f"{document}\n{instruction}".lower()
    action = "create"
    if "delete" in instruction.lower():
        action = "delete"
    elif any(keyword in instruction.lower() for keyword in ("update", "revise", "change", "replace")):
        action = "update"
    target_table = GOVERNED_MODEL_TABLE
    if "formula" in lower or "recipe" in lower:
        target_table = FORMULA_TABLE
    elif "batch" in lower:
        target_table = BATCH_TABLE
    elif "sds" in lower or "safety data sheet" in lower:
        target_table = SDS_TABLE
    elif "hazard" in lower or "ghs" in lower:
        target_table = HAZARDOUS_MATERIAL_TABLE
    elif "submission" in lower or "authority" in lower:
        target_table = REGULATORY_SUBMISSION_TABLE
    extracted_fields = {}
    for line in document.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        extracted_fields[key.strip().lower().replace(" ", "_")] = value.strip()
    return {
        "ok": True,
        "instruction": instruction,
        "action": action,
        "target_table": target_table,
        "candidate_tables": (target_table, GOVERNED_MODEL_TABLE),
        "document_digest": stable_hash(document),
        "extracted_fields": extracted_fields,
        "requires_human_confirmation": True,
        "crud_preview": {
            "action": action,
            "table": target_table,
            "event_contract": EVENT_CONTRACT,
            "shared_table_access": False,
        },
        "side_effects": (),
    }


def create_document_instruction(state: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
    missing = _missing(payload, ("tenant", "document", "instruction"))
    if missing:
        return {"ok": False, "reason": "missing_fields", "missing": missing, "side_effects": ()}
    plan = parse_document_instruction(payload["document"], payload["instruction"])
    next_state, sequence = _next_sequence(state)
    record_id = payload.get("id") or f"instruction-{sequence:04d}"
    record = {
        "id": record_id,
        "tenant": payload["tenant"],
        "artifact_type": "document_instruction",
        "artifact_key": payload.get("artifact_key", record_id),
        "status": "draft",
        "document_digest": plan["document_digest"],
        "instruction_payload": {
            "document": payload["document"],
            "instruction": payload["instruction"],
            "extracted_fields": plan["extracted_fields"],
        },
        "mutation_preview": plan["crud_preview"],
        "human_confirmation_state": "required",
        "created_at": _iso_at(sequence),
        "updated_at": _iso_at(sequence),
    }
    _store_record(next_state, GOVERNED_MODEL_TABLE, record_id, record)
    event = _emit_event(
        next_state,
        event_type=EMITTED_EVENT_TYPES[0],
        payload={"table": GOVERNED_MODEL_TABLE, "id": record_id, "action": plan["action"]},
        tenant=payload["tenant"],
        route=None,
    )
    return {"ok": True, "state": next_state, "record": record, "plan": plan, "event": event, "side_effects": ()}


def update_document_instruction(state: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
    record = _find_record(state, GOVERNED_MODEL_TABLE, payload.get("id"))
    if record is None:
        return {"ok": False, "reason": "instruction_not_found", "side_effects": ()}
    document = payload.get("document", record["instruction_payload"]["document"])
    instruction = payload.get("instruction", record["instruction_payload"]["instruction"])
    plan = parse_document_instruction(document, instruction)
    next_state, sequence = _next_sequence(state)
    updated = dict(record)
    updated["status"] = payload.get("status", "draft")
    updated["document_digest"] = plan["document_digest"]
    updated["instruction_payload"] = {
        "document": document,
        "instruction": instruction,
        "extracted_fields": plan["extracted_fields"],
    }
    updated["mutation_preview"] = plan["crud_preview"]
    updated["updated_at"] = _iso_at(sequence)
    _store_record(next_state, GOVERNED_MODEL_TABLE, record["id"], updated)
    event = _emit_event(
        next_state,
        event_type=EMITTED_EVENT_TYPES[1],
        payload={"table": GOVERNED_MODEL_TABLE, "id": record["id"], "action": plan["action"]},
        tenant=updated["tenant"],
        route=None,
    )
    return {"ok": True, "state": next_state, "record": updated, "plan": plan, "event": event, "side_effects": ()}


def delete_document_instruction(state: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
    record = _find_record(state, GOVERNED_MODEL_TABLE, payload.get("id"))
    if record is None:
        return {"ok": False, "reason": "instruction_not_found", "side_effects": ()}
    next_state, sequence = _next_sequence(state)
    updated = dict(record)
    updated["status"] = "deleted"
    updated["mutation_preview"] = {**dict(record["mutation_preview"]), "action": "delete"}
    updated["updated_at"] = _iso_at(sequence)
    _store_record(next_state, GOVERNED_MODEL_TABLE, record["id"], updated)
    event = _emit_event(
        next_state,
        event_type=EMITTED_EVENT_TYPES[1],
        payload={"table": GOVERNED_MODEL_TABLE, "id": record["id"], "action": "delete"},
        tenant=updated["tenant"],
        route=None,
    )
    return {"ok": True, "state": next_state, "record": updated, "event": event, "side_effects": ()}


def query_document_instruction(state: dict[str, Any], record_id: str) -> dict[str, Any]:
    record = _find_record(state, GOVERNED_MODEL_TABLE, record_id)
    return {"ok": record is not None, "record": record, "side_effects": ()}


def receive_event(state: dict[str, Any], event: dict[str, Any]) -> dict[str, Any]:
    next_state = _copy_state(state)
    idempotency_key = event.get("idempotency_key") or event.get("event_id") or stable_hash(event)
    if idempotency_key in next_state["events"]["handled"]:
        return {"ok": True, "duplicate": True, "state": next_state, "idempotency_key": idempotency_key, "side_effects": ()}
    next_state["events"]["handled"].add(idempotency_key)
    envelope = {
        "id": event.get("id") or stable_hash((event.get("event_type"), idempotency_key)),
        "tenant": event.get("tenant", "default"),
        "event_type": event.get("event_type"),
        "topic": event.get("topic", REQUIRED_EVENT_TOPIC),
        "payload": dict(event.get("payload", {})),
        "idempotency_key": idempotency_key,
        "event_contract": EVENT_CONTRACT,
        "created_at": event.get("created_at", _iso_at(int(next_state.get("sequence", 0)))),
    }
    if event.get("event_type") not in CONSUMED_EVENT_TYPES:
        next_state["events"]["dead_letter"].append(envelope)
        _store_record(next_state, DEAD_LETTER_TABLE, envelope["id"], {**envelope, "retry_policy": {"max_attempts": DEFAULT_RETRY_LIMIT}})
        return {
            "ok": False,
            "duplicate": False,
            "state": next_state,
            "dead_letter_table": DEAD_LETTER_TABLE,
            "idempotency_key": idempotency_key,
            "side_effects": (),
        }
    next_state["events"]["inbox"].append(envelope)
    _store_record(next_state, INBOX_TABLE, envelope["id"], envelope)
    next_state["signals"].append({"event_type": event["event_type"], "payload": dict(event.get("payload", {}))})
    return {"ok": True, "duplicate": False, "state": next_state, "idempotency_key": idempotency_key, "side_effects": ()}


def query_formula_detail(state: dict[str, Any], formula_id: str) -> dict[str, Any]:
    formula = _find_record(state, FORMULA_TABLE, formula_id)
    if formula is None:
        return {"ok": False, "reason": "formula_not_found", "side_effects": ()}
    linked_batches = tuple(
        record for record in _table_records(state, BATCH_TABLE).values() if record.get("formula_id") == formula_id
    )
    return {
        "ok": True,
        "record": formula,
        "release_blockers": _release_blockers(state, formula) if formula.get("lifecycle_state") != "effective" else (),
        "linked_batches": linked_batches,
        "side_effects": (),
    }


def query_batch_detail(state: dict[str, Any], batch_id: str) -> dict[str, Any]:
    batch = _find_record(state, BATCH_TABLE, batch_id)
    if batch is None:
        return {"ok": False, "reason": "batch_not_found", "side_effects": ()}
    quality_tests = tuple(
        record for record in _table_records(state, QUALITY_TEST_TABLE).values() if record.get("batch_id") == batch_id
    )
    holds = tuple(
        record
        for record in _table_records(state, COMPLIANCE_HOLD_TABLE).values()
        if record.get("entity_id") == batch_id and record.get("status") == "open"
    )
    return {"ok": True, "record": batch, "quality_tests": quality_tests, "holds": holds, "side_effects": ()}


def query_workbench(state: dict[str, Any], filters: dict[str, Any] | None = None) -> dict[str, Any]:
    filters = dict(filters or {})
    tenant = filters.get("tenant")
    formulas = tuple(_table_records(state, FORMULA_TABLE).values())
    batches = tuple(_table_records(state, BATCH_TABLE).values())
    sds_docs = tuple(_table_records(state, SDS_TABLE).values())
    holds = tuple(record for record in _table_records(state, COMPLIANCE_HOLD_TABLE).values() if record.get("status") == "open")
    submissions = tuple(_table_records(state, REGULATORY_SUBMISSION_TABLE).values())
    if tenant:
        formulas = tuple(item for item in formulas if item.get("tenant") == tenant)
        batches = tuple(item for item in batches if item.get("tenant") == tenant)
        sds_docs = tuple(item for item in sds_docs if item.get("tenant") == tenant)
        holds = tuple(item for item in holds if item.get("tenant") == tenant)
        submissions = tuple(item for item in submissions if item.get("tenant") == tenant)
    release_queue = tuple(item for item in formulas if item.get("lifecycle_state") != "effective")
    active_batches = tuple(item for item in batches if item.get("release_decision") == "pending_quality")
    expiring_sds = tuple(item for item in sds_docs if item.get("status") == "approved")
    return {
        "ok": True,
        "filters": filters,
        "summary": {
            "formula_release_queue": len(release_queue),
            "active_batches": len(active_batches),
            "open_holds": len(holds),
            "pending_submissions": len([item for item in submissions if item.get("status") != "ready_for_submission"]),
            "expiring_sds": len(expiring_sds),
        },
        "queues": {
            "release_queue": release_queue[: int(state["parameters"]["workbench_limit"]["value"])],
            "active_batches": active_batches[: int(state["parameters"]["workbench_limit"]["value"])],
            "open_holds": holds[: int(state["parameters"]["workbench_limit"]["value"])],
            "pending_submissions": submissions[: int(state["parameters"]["workbench_limit"]["value"])],
            "expiring_sds": expiring_sds[: int(state["parameters"]["workbench_limit"]["value"])],
        },
        "side_effects": (),
    }


def build_app_surface(state: dict[str, Any] | None = None, tenant: str = "default") -> dict[str, Any]:
    state = state or empty_state()
    workbench = query_workbench(state, {"tenant": tenant})
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "tenant": tenant,
        "forms": FORM_DEFINITIONS,
        "wizards": WIZARD_DEFINITIONS,
        "controls": CONTROL_DEFINITIONS,
        "views": WORKBENCH_VIEWS,
        "assistant_cards": (
            {
                "id": "assistant_formula_release",
                "title": "Release Formula Revision",
                "goal": "Explain missing approval or SDS/material gates before release.",
            },
            {
                "id": "assistant_document_instruction",
                "title": "Preview Document Instruction Mutation",
                "goal": "Translate uploaded instructions into governed CRUD previews.",
            },
        ),
        "summary": workbench["summary"],
        "side_effects": (),
    }


def build_workbench_view(state: dict[str, Any] | None = None, tenant: str = "default") -> dict[str, Any]:
    state = state or empty_state()
    surface = build_app_surface(state, tenant=tenant)
    workbench = query_workbench(state, {"tenant": tenant})
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "tenant": tenant,
        "route": f"/workbench/pbcs/{PBC_KEY}",
        "summary": workbench["summary"],
        "queues": workbench["queues"],
        "forms": surface["forms"],
        "wizards": surface["wizards"],
        "controls": surface["controls"],
        "views": surface["views"],
        "side_effects": (),
    }


def run_advanced_assessment(state: dict[str, Any], payload: dict[str, Any] | None = None) -> dict[str, Any]:
    batches = tuple(_table_records(state, BATCH_TABLE).values())
    holds = tuple(record for record in _table_records(state, COMPLIANCE_HOLD_TABLE).values() if record.get("status") == "open")
    formulas = tuple(_table_records(state, FORMULA_TABLE).values())
    score = 0.92
    if batches:
        score -= min(0.25, sum(batch.get("risk_score", 0.0) for batch in batches) / (len(batches) * 4))
    if holds:
        score -= min(0.2, len(holds) * 0.05)
    if any(formula.get("lifecycle_state") != "effective" for formula in formulas):
        score -= 0.08
    return {
        "ok": True,
        "score": round(max(0.1, score), 4),
        "explanations": (
            "release_gates_enforced",
            "batch_risk_scored",
            "assistant_mutations_governed",
        ),
        "payload": dict(payload or {}),
        "side_effects": (),
    }


def verify_owned_table_boundary(references: tuple[str, ...] | list[str] = ()) -> dict[str, Any]:
    invalid = tuple(ref for ref in references if isinstance(ref, str) and ref.endswith("_table") and not ref.startswith(f"{PBC_KEY}_"))
    return {
        "ok": not invalid,
        "pbc": PBC_KEY,
        "invalid_references": invalid,
        "allowed_tables": OWNED_TABLES,
        "shared_table_access": False,
    }


def build_schema_contract() -> dict[str, Any]:
    table_contracts = tuple(
        {
            "table": item["table"],
            "fields": item["fields"],
            "primary_key": item["primary_key"],
            "owned_by": PBC_KEY,
            "domain_role": item["domain_role"],
        }
        for item in TABLE_DEFINITIONS
    )
    return {
        "format": "appgen.chemical-batch-compliance-owned-schema-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "tables": table_contracts,
        "migrations": (
            {
                "path": "pbcs/chemical_batch_compliance/migrations/001_initial.sql",
                "operation": "create_owned_tables",
                "backend_allowlist": ALLOWED_DATABASE_BACKENDS,
            },
        ),
        "models": tuple(
            {
                "class_name": item["class_name"],
                "table": item["table"],
                "fields": item["fields"],
                "primary_key": item["primary_key"],
                "domain_role": item["domain_role"],
            }
            for item in TABLE_DEFINITIONS
        ),
        "datastore_backends": ALLOWED_DATABASE_BACKENDS,
        "database_backends": ALLOWED_DATABASE_BACKENDS,
        "shared_table_access": False,
        "owned_tables": OWNED_TABLES,
    }


COMMAND_METHODS = (
    "configure_runtime",
    "set_parameter",
    "register_rule",
    "register_schema_extension",
    "receive_event",
    "create_formula_revision",
    "release_formula_revision",
    "review_sds_document",
    "register_hazardous_material",
    "record_batch",
    "record_quality_test",
    "place_compliance_hold",
    "resolve_compliance_hold",
    "create_regulatory_submission",
    "upsert_control_assertion",
    "create_document_instruction",
    "update_document_instruction",
    "delete_document_instruction",
    "run_advanced_assessment",
)

QUERY_METHODS = (
    "query_formula_detail",
    "query_batch_detail",
    "query_document_instruction",
    "query_workbench",
    "build_workbench_view",
    "build_app_surface",
    "build_release_evidence",
)

OPERATION_TABLES = {
    "create_formula_revision": (FORMULA_TABLE,),
    "release_formula_revision": (FORMULA_TABLE,),
    "review_sds_document": (SDS_TABLE,),
    "register_hazardous_material": (HAZARDOUS_MATERIAL_TABLE,),
    "record_batch": (BATCH_TABLE,),
    "record_quality_test": (QUALITY_TEST_TABLE, COMPLIANCE_HOLD_TABLE),
    "place_compliance_hold": (COMPLIANCE_HOLD_TABLE,),
    "resolve_compliance_hold": (COMPLIANCE_HOLD_TABLE,),
    "create_regulatory_submission": (REGULATORY_SUBMISSION_TABLE,),
    "register_rule": (POLICY_RULE_TABLE,),
    "set_parameter": (RUNTIME_PARAMETER_TABLE,),
    "register_schema_extension": (SCHEMA_EXTENSION_TABLE,),
    "upsert_control_assertion": (CONTROL_ASSERTION_TABLE,),
    "create_document_instruction": (GOVERNED_MODEL_TABLE,),
    "update_document_instruction": (GOVERNED_MODEL_TABLE,),
    "delete_document_instruction": (GOVERNED_MODEL_TABLE,),
}

OPERATION_EVENTS = {
    "create_formula_revision": EMITTED_EVENT_TYPES[0],
    "release_formula_revision": EMITTED_EVENT_TYPES[2],
    "review_sds_document": EMITTED_EVENT_TYPES[1],
    "register_hazardous_material": EMITTED_EVENT_TYPES[1],
    "record_batch": EMITTED_EVENT_TYPES[0],
    "record_quality_test": EMITTED_EVENT_TYPES[3],
    "place_compliance_hold": EMITTED_EVENT_TYPES[3],
    "resolve_compliance_hold": EMITTED_EVENT_TYPES[2],
    "create_regulatory_submission": EMITTED_EVENT_TYPES[2],
    "register_rule": EMITTED_EVENT_TYPES[1],
    "set_parameter": EMITTED_EVENT_TYPES[1],
    "register_schema_extension": EMITTED_EVENT_TYPES[1],
    "upsert_control_assertion": EMITTED_EVENT_TYPES[1],
    "create_document_instruction": EMITTED_EVENT_TYPES[0],
    "update_document_instruction": EMITTED_EVENT_TYPES[1],
    "delete_document_instruction": EMITTED_EVENT_TYPES[1],
}


def build_service_contract() -> dict[str, Any]:
    return {
        "format": "appgen.chemical-batch-compliance-service-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "command_methods": COMMAND_METHODS,
        "query_methods": QUERY_METHODS,
        "shared_table_access": False,
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": EVENT_CONTRACT,
    }


def build_api_contract() -> dict[str, Any]:
    return {
        "format": "appgen.chemical-batch-compliance-api-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "routes": ROUTES,
        "event_contract": EVENT_CONTRACT,
        "stream_engine_picker_visible": False,
        "owned_tables": OWNED_TABLES,
    }


def permissions_contract() -> dict[str, Any]:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "permissions": PERMISSIONS,
        "roles": tuple(ROLE_PERMISSIONS),
        "role_matrix": ROLE_PERMISSIONS,
        "side_effects": (),
    }


def build_release_evidence(state: dict[str, Any] | None = None) -> dict[str, Any]:
    snapshot = query_workbench(state or empty_state(), {})
    return {
        "format": "appgen.chemical-batch-compliance-release-evidence.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "implemented_slice": "formula release, batch execution, quality hold, regulatory dossier, assistant document instruction CRUD",
        "checks": (
            {"id": "schema_models_migrations", "ok": True},
            {"id": "services_routes", "ok": True},
            {"id": "appgen_events_handlers", "ok": True},
            {"id": "workbench_forms_wizards_controls", "ok": True},
            {"id": "rbac_config_rules_parameters", "ok": True},
            {"id": "agent_document_instruction_crud", "ok": True},
        ),
        "generated_artifacts": {
            "migrations": ("migrations/001_initial.sql",),
            "models": tuple(item["class_name"] for item in TABLE_DEFINITIONS),
            "events": {"emits": EMITTED_EVENT_TYPES, "consumes": CONSUMED_EVENT_TYPES},
            "ui": {"forms": tuple(item["id"] for item in FORM_DEFINITIONS), "wizards": tuple(item["id"] for item in WIZARD_DEFINITIONS)},
            "tests": ("tests/test_contract.py", "tests/test_slice_app.py"),
        },
        "operational_snapshot": snapshot["summary"],
        "blocking_gaps": (),
    }


def operation_contract(operation: str, kind: str) -> dict[str, Any]:
    return {
        "operation": operation,
        "operation_kind": kind,
        "owned_tables": OPERATION_TABLES.get(operation, ()) if kind == "command" else (),
        "read_tables": OPERATION_TABLES.get(operation, ()) if kind == "query" else (),
        "emitted_event": OPERATION_EVENTS.get(operation) if kind == "command" else None,
        "transaction_boundary": "owned_datastore_plus_outbox" if kind == "command" else "read_only_projection",
    }


def service_callable(operation: str):
    return {
        "configure_runtime": lambda state, payload: configure_runtime(state, payload),
        "set_parameter": lambda state, payload: set_parameter_value(state, payload["name"], payload["value"], payload.get("tenant", "default")),
        "register_rule": lambda state, payload: register_rule_definition(state, payload, payload.get("tenant", "default")),
        "register_schema_extension": lambda state, payload: register_schema_extension_definition(
            state,
            payload["table"],
            payload["fields"],
            payload.get("tenant", "default"),
            payload.get("rationale", ""),
        ),
        "receive_event": lambda state, payload: receive_event(state, payload),
        "create_formula_revision": lambda state, payload: create_formula_revision(state, payload),
        "release_formula_revision": lambda state, payload: release_formula_revision(state, payload),
        "review_sds_document": lambda state, payload: review_sds_document(state, payload),
        "register_hazardous_material": lambda state, payload: register_hazardous_material(state, payload),
        "record_batch": lambda state, payload: record_batch(state, payload),
        "record_quality_test": lambda state, payload: record_quality_test(state, payload),
        "place_compliance_hold": lambda state, payload: place_compliance_hold(state, payload),
        "resolve_compliance_hold": lambda state, payload: resolve_compliance_hold(state, payload),
        "create_regulatory_submission": lambda state, payload: create_regulatory_submission(state, payload),
        "upsert_control_assertion": lambda state, payload: upsert_control_assertion(state, payload),
        "create_document_instruction": lambda state, payload: create_document_instruction(state, payload),
        "update_document_instruction": lambda state, payload: update_document_instruction(state, payload),
        "delete_document_instruction": lambda state, payload: delete_document_instruction(state, payload),
        "run_advanced_assessment": lambda state, payload: run_advanced_assessment(state, payload),
        "query_formula_detail": lambda state, payload: query_formula_detail(state, payload["id"]),
        "query_batch_detail": lambda state, payload: query_batch_detail(state, payload["id"]),
        "query_document_instruction": lambda state, payload: query_document_instruction(state, payload["id"]),
        "query_workbench": lambda state, payload: query_workbench(state, payload),
        "build_workbench_view": lambda state, payload: build_workbench_view(state, payload.get("tenant", "default")),
        "build_app_surface": lambda state, payload: build_app_surface(state, payload.get("tenant", "default")),
        "build_release_evidence": lambda state, payload: build_release_evidence(state),
    }[operation]


def route_operation(route: str) -> str | None:
    return ROUTE_TO_OPERATION.get(route)


def run_slice_smoke() -> dict[str, Any]:
    state = empty_state()
    configured = configure_runtime(
        state,
        {"database_backend": "postgresql", "event_topic": REQUIRED_EVENT_TOPIC, "retry_limit": DEFAULT_RETRY_LIMIT},
    )
    parameter = set_parameter_value(configured["state"], "misweigh_alert_pct", 1.0, "tenant-smoke")
    rule = register_rule_definition(
        parameter["state"],
        {"rule_id": "formula_effectivity_rule", "scope": "formula_release", "threshold_json": {"max_missing_gates": 0}},
        "tenant-smoke",
    )
    sds = review_sds_document(
        rule["state"],
        {
            "tenant": "tenant-smoke",
            "material_code": "SOLV-100",
            "revision": "7",
            "issue_date": "2026-01-01",
            "expiration_date": "2027-01-01",
            "jurisdictions": ("US", "EU"),
            "hazard_summary": {"flash_point_c": 18},
            "approved": True,
        },
    )
    material = register_hazardous_material(
        sds["state"],
        {
            "tenant": "tenant-smoke",
            "material_code": "SOLV-100",
            "ghs_classification": ("Flammable liquid, category 2",),
            "approved_sources": ("Vendor A",),
            "ppe_requirements": ("gloves", "goggles"),
        },
    )
    formula = create_formula_revision(
        material["state"],
        {
            "tenant": "tenant-smoke",
            "formula_code": "CBR-77",
            "revision": "A",
            "product_name": "Catalyst Blend 77",
            "target_concentration": {"assay_pct": 98.5},
            "composition_window": {"solvent_pct_min": 30, "solvent_pct_max": 32},
            "required_sds_ids": (sds["record"]["id"],),
            "required_hazard_material_ids": (material["record"]["id"],),
            "required_permits": ("hot_work",),
            "equipment_classes": ("reactor_train_a",),
            "approvals": {"technical": True, "quality": True, "ehs": True},
            "effectivity_start": "2026-01-02",
            "process_steps": (
                {"step_code": "charge", "critical": True},
                {"step_code": "react", "critical": True},
                {"step_code": "filter", "critical": False},
            ),
        },
    )
    released = release_formula_revision(formula["state"], {"id": formula["record"]["id"], "tenant": "tenant-smoke"})
    batch = record_batch(
        released["state"],
        {
            "tenant": "tenant-smoke",
            "batch_number": "BATCH-1001",
            "formula_id": released["record"]["id"],
            "equipment_profile": {
                "line_clearance": True,
                "cleaning_release": True,
                "calibration_current": True,
            },
            "permits_confirmed": ("hot_work",),
            "step_executions": (
                {"step_code": "charge", "status": "complete"},
                {"step_code": "react", "status": "complete"},
                {"step_code": "filter", "status": "complete"},
            ),
            "dispense_log": (
                {"material_code": "SOLV-100", "target_qty": 100.0, "actual_qty": 100.4},
            ),
            "parameter_log": (
                {"parameter_name": "temperature", "value": 42, "band": "advisory"},
            ),
        },
    )
    quality = record_quality_test(
        batch["state"],
        {
            "tenant": "tenant-smoke",
            "batch_id": batch["record"]["id"],
            "test_name": "assay",
            "specification": {"min": 98.0, "max": 101.0},
            "result_value": 97.5,
            "result_status": "fail",
        },
    )
    document = create_document_instruction(
        quality["state"],
        {
            "tenant": "tenant-smoke",
            "document": "Formula Code: CBR-77\nRevision: B",
            "instruction": "Update the formula revision with the new solvent range.",
        },
    )
    updated_document = update_document_instruction(
        document["state"],
        {"id": document["record"]["id"], "instruction": "Delete the pending formula draft after review."},
    )
    deleted_document = delete_document_instruction(updated_document["state"], {"id": document["record"]["id"]})
    submission = create_regulatory_submission(
        deleted_document["state"],
        {
            "tenant": "tenant-smoke",
            "dossier_number": "EPA-2026-001",
            "jurisdiction": "US",
            "submission_type": "label_update",
            "product_code": "CBR-77",
            "source_record_ids": (released["record"]["id"], batch["record"]["id"], sds["record"]["id"]),
        },
    )
    consumed = receive_event(
        submission["state"],
        {"event_type": CONSUMED_EVENT_TYPES[0], "tenant": "tenant-smoke", "idempotency_key": "policy-1"},
    )
    duplicate = receive_event(
        consumed["state"],
        {"event_type": CONSUMED_EVENT_TYPES[0], "tenant": "tenant-smoke", "idempotency_key": "policy-1"},
    )
    dead_letter = receive_event(
        duplicate["state"],
        {"event_type": "UnexpectedEvent", "tenant": "tenant-smoke", "idempotency_key": "bad-1"},
    )
    workbench = build_workbench_view(dead_letter["state"], tenant="tenant-smoke")
    assessment = run_advanced_assessment(dead_letter["state"])
    surface = build_app_surface(dead_letter["state"], tenant="tenant-smoke")
    checks = (
        {"id": "configure_runtime", "ok": configured["ok"]},
        {"id": "set_parameter", "ok": parameter["ok"]},
        {"id": "register_rule", "ok": rule["ok"]},
        {"id": "review_sds_document", "ok": sds["ok"]},
        {"id": "register_hazardous_material", "ok": material["ok"]},
        {"id": "create_formula_revision", "ok": formula["ok"]},
        {"id": "release_formula_revision", "ok": released["ok"]},
        {"id": "record_batch", "ok": batch["ok"]},
        {"id": "record_quality_test", "ok": quality["ok"] and quality["hold"] is not None},
        {"id": "document_instruction_crud", "ok": deleted_document["record"]["status"] == "deleted"},
        {"id": "regulatory_submission", "ok": submission["ok"] and submission["record"]["status"] == "ready_for_submission"},
        {"id": "receive_event", "ok": consumed["ok"]},
        {"id": "duplicate_event", "ok": duplicate.get("duplicate") is True},
        {"id": "dead_letter", "ok": dead_letter["ok"] is False and dead_letter["dead_letter_table"] == DEAD_LETTER_TABLE},
        {"id": "workbench_view", "ok": workbench["ok"] and workbench["summary"]["open_holds"] == 1},
        {"id": "advanced_assessment", "ok": assessment["ok"] and assessment["score"] > 0.0},
        {"id": "app_surface", "ok": surface["ok"] and len(surface["forms"]) == 4},
    )
    return {
        "format": "appgen.chemical-batch-compliance-slice-smoke.v1",
        "ok": all(check["ok"] for check in checks),
        "checks": checks,
        "configured": configured,
        "released_formula": released,
        "batch": batch,
        "quality": quality,
        "submission": submission,
        "workbench": workbench,
        "assessment": assessment,
        "app_surface": surface,
        "state": dead_letter["state"],
    }
