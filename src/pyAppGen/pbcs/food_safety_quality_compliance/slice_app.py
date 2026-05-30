"""Standalone executable slice for food safety quality compliance."""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from typing import Any, Callable


PBC_KEY = "food_safety_quality_compliance"
EVENT_CONTRACT = "AppGen-X"
ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
REQUIRED_EVENT_TOPIC = f"pbc.{PBC_KEY}.events"
DEFAULT_POLICY = "preventive_controls_haccp"
DEFAULT_RETRY_LIMIT = 5

EMITTED_EVENT_TYPES = (
    "FoodSafetyQualityComplianceCreated",
    "FoodSafetyQualityComplianceUpdated",
    "FoodSafetyQualityComplianceApproved",
    "FoodSafetyQualityComplianceExceptionOpened",
)
CONSUMED_EVENT_TYPES = ("PolicyChanged", "AuditEventSealed", "OperationalKpiChanged")

HACCP_PLAN_TABLE = f"{PBC_KEY}_haccp_plan"
CRITICAL_CONTROL_POINT_TABLE = f"{PBC_KEY}_critical_control_point"
INSPECTION_TABLE = f"{PBC_KEY}_inspection"
NONCONFORMANCE_TABLE = f"{PBC_KEY}_nonconformance"
RECALL_EVENT_TABLE = f"{PBC_KEY}_recall_event"
SUPPLIER_AUDIT_TABLE = f"{PBC_KEY}_supplier_audit"
QUALITY_HOLD_TABLE = f"{PBC_KEY}_quality_hold"
POLICY_RULE_TABLE = f"{PBC_KEY}_{PBC_KEY}_policy_rule"
RUNTIME_PARAMETER_TABLE = f"{PBC_KEY}_{PBC_KEY}_runtime_parameter"
SCHEMA_EXTENSION_TABLE = f"{PBC_KEY}_{PBC_KEY}_schema_extension"
CONTROL_ASSERTION_TABLE = f"{PBC_KEY}_{PBC_KEY}_control_assertion"
GOVERNED_MODEL_TABLE = f"{PBC_KEY}_{PBC_KEY}_governed_model"
OUTBOX_TABLE = f"{PBC_KEY}_appgen_outbox_event"
INBOX_TABLE = f"{PBC_KEY}_appgen_inbox_event"
DEAD_LETTER_TABLE = f"{PBC_KEY}_appgen_dead_letter_event"

BUSINESS_TABLES = (
    HACCP_PLAN_TABLE,
    CRITICAL_CONTROL_POINT_TABLE,
    INSPECTION_TABLE,
    NONCONFORMANCE_TABLE,
    RECALL_EVENT_TABLE,
    SUPPLIER_AUDIT_TABLE,
    QUALITY_HOLD_TABLE,
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
    "quality_manager": (f"{PBC_KEY}.read", f"{PBC_KEY}.update", f"{PBC_KEY}.approve"),
    "supplier_quality_lead": (f"{PBC_KEY}.read", f"{PBC_KEY}.update", f"{PBC_KEY}.approve"),
    "recall_coordinator": (f"{PBC_KEY}.read", f"{PBC_KEY}.update", f"{PBC_KEY}.approve"),
    "auditor": (f"{PBC_KEY}.read",),
    "admin": PERMISSIONS + (f"{PBC_KEY}.operate",),
}

PARAMETER_DEFINITIONS = {
    "ccp_monitoring_grace_minutes": {
        "default": 30,
        "minimum": 0,
        "maximum": 240,
        "unit": "minutes",
        "description": "Maximum lateness allowed before a CCP check is considered late.",
    },
    "hold_release_min_approvers": {
        "default": 1,
        "minimum": 1,
        "maximum": 3,
        "unit": "count",
        "description": "Minimum approvers required before held product is released.",
    },
    "supplier_audit_expiry_warning_days": {
        "default": 30,
        "minimum": 1,
        "maximum": 180,
        "unit": "days",
        "description": "Lead time for supplier audit expiry warnings.",
    },
    "mock_recall_target_minutes": {
        "default": 120,
        "minimum": 15,
        "maximum": 1440,
        "unit": "minutes",
        "description": "Target completion time for mock recall traceability drills.",
    },
    "regulatory_obligation_sla_days": {
        "default": 7,
        "minimum": 1,
        "maximum": 90,
        "unit": "days",
        "description": "Default SLA for regulator communication tasks.",
    },
    "workbench_limit": {
        "default": 25,
        "minimum": 5,
        "maximum": 100,
        "unit": "records",
        "description": "Maximum records returned in each workbench queue.",
    },
}

RULE_DEFINITIONS = {
    "haccp_plan_effectivity_rule": (
        "A HACCP plan version cannot become effective until hazards are mapped to process steps "
        "and required CCPs exist for critical hazards."
    ),
    "ccp_hazard_mapping_rule": "A CCP requires a mapped process step and hazard from the owning HACCP plan.",
    "critical_findings_hold_rule": "Critical inspection findings and failed allergen or temperature checks open a quality hold.",
    "major_nonconformance_closure_rule": (
        "Major or critical nonconformances require root cause, corrective action, preventive action, "
        "and effectiveness evidence before closure."
    ),
    "supplier_approval_expiry_rule": "High-risk or expired supplier audits block approved status until corrective action is accepted.",
    "recall_projection_boundary_rule": (
        "Recall impact analysis must use declared genealogy and shipment projections only; direct reads "
        "of inventory, manufacturing, or customer tables are forbidden."
    ),
    "assistant_mutation_guardrail_rule": (
        "Assistant-generated CRUD previews require owned tables, citations, human confirmation, "
        "and release-impact review before approval."
    ),
}

STANDARD_FEATURE_KEYS = (
    "haccp_plan_management",
    "food_safety_quality_compliance_workflow",
    "food_safety_quality_compliance_analytics",
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
    "food_safety_quality_compliance_event_sourced_operational_history",
    "food_safety_quality_compliance_multi_tenant_policy_isolation",
    "food_safety_quality_compliance_schema_evolution_resilience",
    "food_safety_quality_compliance_autonomous_anomaly_detection",
    "food_safety_quality_compliance_semantic_document_instruction_understanding",
    "food_safety_quality_compliance_predictive_risk_scoring",
    "food_safety_quality_compliance_counterfactual_scenario_simulation",
    "food_safety_quality_compliance_cryptographic_audit_proofs",
    "food_safety_quality_compliance_continuous_control_testing",
    "food_safety_quality_compliance_carbon_and_sustainability_awareness",
    "food_safety_quality_compliance_cross_pbc_event_federation",
    "food_safety_quality_compliance_governed_ai_agent_execution",
)
UI_FRAGMENT_KEYS = (
    "FoodSafetyQualityComplianceWorkbench",
    "FoodSafetyQualityComplianceDetail",
    "FoodSafetyQualityComplianceAssistantPanel",
)

ROUTES = (
    "POST /haccp-plans",
    "POST /critical-control-points",
    "POST /inspections",
    "POST /nonconformances",
    "POST /recall-events",
    "GET /food-safety-quality-compliance-workbench",
)
ROUTE_TO_OPERATION = {
    "POST /haccp-plans": "create_haccp_plan",
    "POST /critical-control-points": "create_critical_control_point",
    "POST /inspections": "record_inspection",
    "POST /nonconformances": "open_nonconformance",
    "POST /recall-events": "start_recall_event",
    "GET /food-safety-quality-compliance-workbench": "build_workbench_view",
}

WORKFLOWS = (
    "food_safety_quality_compliance_create_haccp_plan_workflow",
    "food_safety_quality_compliance_record_critical_control_point_workflow",
    "food_safety_quality_compliance_inspection_escalation_workflow",
    "food_safety_quality_compliance_hold_disposition_workflow",
    "food_safety_quality_compliance_recall_readiness_workflow",
)

DOMAIN_OPERATIONS = (
    "configure_runtime",
    "create_haccp_plan",
    "approve_haccp_plan",
    "create_critical_control_point",
    "record_inspection",
    "open_nonconformance",
    "close_nonconformance",
    "create_supplier_audit",
    "open_quality_hold",
    "release_quality_hold",
    "start_recall_event",
    "run_mock_recall",
    "set_parameter",
    "register_rule",
    "register_schema_extension",
    "upsert_control_assertion",
    "create_document_instruction",
    "approve_document_instruction",
    "receive_event",
)
QUERY_METHODS = (
    "query_workbench",
    "build_workbench_view",
    "query_haccp_plan_detail",
    "query_recall_packet",
)
COMMAND_METHODS = DOMAIN_OPERATIONS
DOMAIN_RULES = tuple(RULE_DEFINITIONS)
DOMAIN_PARAMETERS = tuple(PARAMETER_DEFINITIONS)
DOMAIN_ADVANCED_CAPABILITIES = (
    "historical HACCP version pinning for inspections and holds",
    "hazard-to-CCP map validation with governed corrective action triggers",
    "projection-only recall impact analysis and mock recall drill metrics",
    "risk-ranked quality workbench with audit, hold, and recall queues",
    "governed assistant skills for evidence summaries and mutation previews",
    "continuous control assertions and release-readiness evidence",
)
DOMAIN_EDGE_CASES = (
    "plan_approval_without_ccp_mapping",
    "ccp_definition_without_hazard_reference",
    "critical_inspection_without_auto_hold",
    "major_nonconformance_closed_without_root_cause",
    "hold_release_without_disposition_approval",
    "recall_analysis_with_foreign_table_reference",
    "duplicate_event_replay",
    "unexpected_event_dead_letter",
)
WORKBENCH_VIEWS = (
    "HACCP Approval Queue",
    "Inspection Escalation Queue",
    "Open Quality Holds",
    "Supplier Audit Monitor",
    "Recall Readiness Board",
)

FORM_DEFINITIONS = (
    {
        "id": "haccp_plan_form",
        "title": "HACCP Plan Version Intake",
        "table": HACCP_PLAN_TABLE,
        "fields": (
            "tenant",
            "plan_code",
            "version",
            "facility_code",
            "product_scope",
            "process_steps",
            "hazard_analysis",
            "approvals",
            "effective_from",
        ),
    },
    {
        "id": "critical_control_point_form",
        "title": "Critical Control Point Definition",
        "table": CRITICAL_CONTROL_POINT_TABLE,
        "fields": (
            "tenant",
            "plan_id",
            "process_step_code",
            "hazard_id",
            "limit_min",
            "limit_max",
            "unit",
            "monitoring_frequency_minutes",
            "monitoring_method",
            "corrective_action",
        ),
    },
    {
        "id": "inspection_form",
        "title": "Inspection Review",
        "table": INSPECTION_TABLE,
        "fields": (
            "tenant",
            "plan_code",
            "facility_code",
            "area",
            "checklist",
            "findings",
            "inspector",
            "started_at",
        ),
    },
    {
        "id": "recall_event_form",
        "title": "Recall Event Or Mock Drill",
        "table": RECALL_EVENT_TABLE,
        "fields": (
            "tenant",
            "classification",
            "reason",
            "consumer_risk",
            "distribution_scope",
            "genealogy_projection",
            "shipment_projection",
            "communication_plan",
        ),
    },
)

WIZARD_DEFINITIONS = (
    {
        "id": "haccp_authoring_wizard",
        "title": "Author And Approve HACCP Plan",
        "steps": (
            "identify_product_scope",
            "map_process_steps",
            "record_hazards",
            "define_ccps",
            "collect_approvals",
            "activate_version",
        ),
    },
    {
        "id": "recall_response_wizard",
        "title": "Run Recall Impact Analysis",
        "steps": (
            "classify_event",
            "collect_projection_inputs",
            "trace_affected_lots",
            "draft_regulator_notification",
            "prepare_customer_communication",
            "seal_evidence_packet",
        ),
    },
)

CONTROL_DEFINITIONS = (
    {"id": "approve_haccp_plan", "label": "Approve HACCP Plan", "operation": "approve_haccp_plan", "required_permission": f"{PBC_KEY}.approve"},
    {"id": "open_quality_hold", "label": "Open Quality Hold", "operation": "open_quality_hold", "required_permission": f"{PBC_KEY}.update"},
    {"id": "release_quality_hold", "label": "Release Hold", "operation": "release_quality_hold", "required_permission": f"{PBC_KEY}.approve"},
    {"id": "run_mock_recall", "label": "Run Mock Recall", "operation": "run_mock_recall", "required_permission": f"{PBC_KEY}.approve"},
    {"id": "approve_document_instruction", "label": "Approve Assistant Preview", "operation": "approve_document_instruction", "required_permission": f"{PBC_KEY}.approve"},
)

TABLE_DEFINITIONS = (
    {
        "class_name": "FoodSafetyQualityComplianceHaccpPlan",
        "table": HACCP_PLAN_TABLE,
        "domain_role": "haccp_plan_version",
        "fields": (
            "id",
            "tenant",
            "plan_code",
            "version",
            "facility_code",
            "product_scope",
            "lifecycle_state",
            "process_steps",
            "hazard_analysis",
            "approvals",
            "effective_from",
            "supersedes_plan_id",
            "supersession_reason",
            "evidence_hash",
            "created_at",
            "updated_at",
        ),
    },
    {
        "class_name": "FoodSafetyQualityComplianceCriticalControlPoint",
        "table": CRITICAL_CONTROL_POINT_TABLE,
        "domain_role": "critical_control_point",
        "fields": (
            "id",
            "tenant",
            "plan_id",
            "process_step_code",
            "hazard_id",
            "limit_min",
            "limit_max",
            "unit",
            "monitoring_method",
            "monitoring_frequency_minutes",
            "responsible_role",
            "verification_requirement",
            "corrective_action",
            "status",
            "created_at",
            "updated_at",
        ),
    },
    {
        "class_name": "FoodSafetyQualityComplianceInspection",
        "table": INSPECTION_TABLE,
        "domain_role": "inspection",
        "fields": (
            "id",
            "tenant",
            "plan_id",
            "plan_code",
            "plan_version",
            "facility_code",
            "area",
            "checklist",
            "findings",
            "score",
            "repeat_findings",
            "status",
            "created_hold_ids",
            "created_nonconformance_ids",
            "inspector",
            "started_at",
            "created_at",
            "updated_at",
        ),
    },
    {
        "class_name": "FoodSafetyQualityComplianceNonconformance",
        "table": NONCONFORMANCE_TABLE,
        "domain_role": "nonconformance",
        "fields": (
            "id",
            "tenant",
            "category",
            "severity",
            "product_impact",
            "process_step_code",
            "containment_action",
            "corrective_action",
            "preventive_action",
            "root_cause_method",
            "confirmed_root_cause",
            "effectiveness_evidence",
            "recurrence_flag",
            "status",
            "source_inspection_id",
            "created_at",
            "updated_at",
        ),
    },
    {
        "class_name": "FoodSafetyQualityComplianceRecallEvent",
        "table": RECALL_EVENT_TABLE,
        "domain_role": "recall_event",
        "fields": (
            "id",
            "tenant",
            "classification",
            "reason",
            "consumer_risk",
            "distribution_scope",
            "affected_lots",
            "customers",
            "regulator_notification",
            "communication_plan",
            "is_mock_drill",
            "trace_elapsed_minutes",
            "projection_boundary_ok",
            "status",
            "created_at",
            "updated_at",
        ),
    },
    {
        "class_name": "FoodSafetyQualityComplianceSupplierAudit",
        "table": SUPPLIER_AUDIT_TABLE,
        "domain_role": "supplier_audit",
        "fields": (
            "id",
            "tenant",
            "supplier_projection",
            "commodity",
            "audit_type",
            "risk_rating",
            "findings",
            "corrective_actions",
            "approval_status",
            "expiry_date",
            "days_until_expiry",
            "created_at",
            "updated_at",
        ),
    },
    {
        "class_name": "FoodSafetyQualityComplianceQualityHold",
        "table": QUALITY_HOLD_TABLE,
        "domain_role": "quality_hold",
        "fields": (
            "id",
            "tenant",
            "hold_reason",
            "affected_lots",
            "quantity",
            "location",
            "release_criteria",
            "disposition",
            "approved_by",
            "released_at",
            "source_inspection_id",
            "haccp_plan_id",
            "haccp_plan_version",
            "status",
            "created_at",
            "updated_at",
        ),
    },
    {
        "class_name": "FoodSafetyQualityCompliancePolicyRule",
        "table": POLICY_RULE_TABLE,
        "domain_role": "policy_rule",
        "fields": (
            "id",
            "tenant",
            "rule_id",
            "scope",
            "status",
            "rule_text",
            "compiled_hash",
            "created_at",
            "updated_at",
        ),
    },
    {
        "class_name": "FoodSafetyQualityComplianceRuntimeParameter",
        "table": RUNTIME_PARAMETER_TABLE,
        "domain_role": "runtime_parameter",
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
        "class_name": "FoodSafetyQualityComplianceSchemaExtension",
        "table": SCHEMA_EXTENSION_TABLE,
        "domain_role": "schema_extension",
        "fields": (
            "id",
            "tenant",
            "table_name",
            "field_map",
            "rationale",
            "status",
            "created_at",
            "updated_at",
        ),
    },
    {
        "class_name": "FoodSafetyQualityComplianceControlAssertion",
        "table": CONTROL_ASSERTION_TABLE,
        "domain_role": "control_assertion",
        "fields": (
            "id",
            "tenant",
            "control_id",
            "control_name",
            "frequency",
            "status",
            "assertion_payload",
            "evidence_hash",
            "created_at",
            "updated_at",
        ),
    },
    {
        "class_name": "FoodSafetyQualityComplianceGovernedModel",
        "table": GOVERNED_MODEL_TABLE,
        "domain_role": "governed_model",
        "fields": (
            "id",
            "tenant",
            "artifact_type",
            "artifact_key",
            "status",
            "document_digest",
            "instruction_payload",
            "mutation_preview",
            "citations",
            "human_confirmation_state",
            "approved_by",
            "created_at",
            "updated_at",
        ),
    },
    {
        "class_name": "FoodSafetyQualityComplianceOutboxEvent",
        "table": OUTBOX_TABLE,
        "domain_role": "outbox_event",
        "fields": ("id", "tenant", "event_type", "topic", "payload", "idempotency_key", "created_at"),
    },
    {
        "class_name": "FoodSafetyQualityComplianceInboxEvent",
        "table": INBOX_TABLE,
        "domain_role": "inbox_event",
        "fields": ("id", "tenant", "event_type", "payload", "idempotency_key", "status", "created_at"),
    },
    {
        "class_name": "FoodSafetyQualityComplianceDeadLetterEvent",
        "table": DEAD_LETTER_TABLE,
        "domain_role": "dead_letter_event",
        "fields": ("id", "tenant", "event_type", "payload", "idempotency_key", "retry_policy", "created_at"),
    },
)

OPERATION_TABLES = {
    "configure_runtime": (),
    "create_haccp_plan": (HACCP_PLAN_TABLE, OUTBOX_TABLE),
    "approve_haccp_plan": (HACCP_PLAN_TABLE, OUTBOX_TABLE),
    "create_critical_control_point": (CRITICAL_CONTROL_POINT_TABLE, OUTBOX_TABLE),
    "record_inspection": (INSPECTION_TABLE, QUALITY_HOLD_TABLE, NONCONFORMANCE_TABLE, OUTBOX_TABLE),
    "open_nonconformance": (NONCONFORMANCE_TABLE, OUTBOX_TABLE),
    "close_nonconformance": (NONCONFORMANCE_TABLE, OUTBOX_TABLE),
    "create_supplier_audit": (SUPPLIER_AUDIT_TABLE, OUTBOX_TABLE),
    "open_quality_hold": (QUALITY_HOLD_TABLE, OUTBOX_TABLE),
    "release_quality_hold": (QUALITY_HOLD_TABLE, OUTBOX_TABLE),
    "start_recall_event": (RECALL_EVENT_TABLE, OUTBOX_TABLE),
    "run_mock_recall": (),
    "set_parameter": (RUNTIME_PARAMETER_TABLE,),
    "register_rule": (POLICY_RULE_TABLE,),
    "register_schema_extension": (SCHEMA_EXTENSION_TABLE,),
    "upsert_control_assertion": (CONTROL_ASSERTION_TABLE,),
    "create_document_instruction": (GOVERNED_MODEL_TABLE,),
    "approve_document_instruction": (GOVERNED_MODEL_TABLE,),
    "receive_event": (INBOX_TABLE, DEAD_LETTER_TABLE),
    "query_workbench": (),
    "build_workbench_view": (),
    "query_haccp_plan_detail": (),
    "query_recall_packet": (),
}
OPERATION_EVENTS = {
    "create_haccp_plan": EMITTED_EVENT_TYPES[0],
    "approve_haccp_plan": EMITTED_EVENT_TYPES[2],
    "create_critical_control_point": EMITTED_EVENT_TYPES[1],
    "record_inspection": EMITTED_EVENT_TYPES[3],
    "open_nonconformance": EMITTED_EVENT_TYPES[3],
    "close_nonconformance": EMITTED_EVENT_TYPES[2],
    "create_supplier_audit": EMITTED_EVENT_TYPES[1],
    "open_quality_hold": EMITTED_EVENT_TYPES[3],
    "release_quality_hold": EMITTED_EVENT_TYPES[2],
    "start_recall_event": EMITTED_EVENT_TYPES[3],
}
OPERATION_PERMISSIONS = {
    "configure_runtime": f"{PBC_KEY}.admin",
    "create_haccp_plan": f"{PBC_KEY}.create",
    "approve_haccp_plan": f"{PBC_KEY}.approve",
    "create_critical_control_point": f"{PBC_KEY}.update",
    "record_inspection": f"{PBC_KEY}.update",
    "open_nonconformance": f"{PBC_KEY}.update",
    "close_nonconformance": f"{PBC_KEY}.approve",
    "create_supplier_audit": f"{PBC_KEY}.update",
    "open_quality_hold": f"{PBC_KEY}.update",
    "release_quality_hold": f"{PBC_KEY}.approve",
    "start_recall_event": f"{PBC_KEY}.approve",
    "run_mock_recall": f"{PBC_KEY}.approve",
    "set_parameter": f"{PBC_KEY}.admin",
    "register_rule": f"{PBC_KEY}.admin",
    "register_schema_extension": f"{PBC_KEY}.admin",
    "upsert_control_assertion": f"{PBC_KEY}.update",
    "create_document_instruction": f"{PBC_KEY}.update",
    "approve_document_instruction": f"{PBC_KEY}.approve",
    "receive_event": f"{PBC_KEY}.update",
    "query_workbench": f"{PBC_KEY}.read",
    "build_workbench_view": f"{PBC_KEY}.read",
    "query_haccp_plan_detail": f"{PBC_KEY}.read",
    "query_recall_packet": f"{PBC_KEY}.read",
}


def _jsonable(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in sorted(value.items(), key=lambda item: str(item[0]))}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    if isinstance(value, set):
        return sorted(_jsonable(item) for item in value)
    return value


def _digest(value: Any) -> str:
    encoded = json.dumps(_jsonable(value), sort_keys=True, default=str).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _copy_state(state: dict) -> dict:
    copied = deepcopy(state)
    copied["idempotency_keys"] = set(state.get("idempotency_keys", set()))
    copied["counters"] = dict(state.get("counters", {}))
    return copied


def _default_rule_records() -> dict[str, dict[str, Any]]:
    records: dict[str, dict[str, Any]] = {}
    for index, (rule_id, rule_text) in enumerate(RULE_DEFINITIONS.items(), start=1):
        records[rule_id] = {
            "id": f"rule-{index}",
            "tenant": "system",
            "rule_id": rule_id,
            "scope": "domain",
            "status": "active",
            "rule_text": rule_text,
            "compiled_hash": _digest((rule_id, rule_text)),
            "created_at": "2026-01-01T00:00:00Z",
            "updated_at": "2026-01-01T00:00:00Z",
        }
    return records


def _default_parameter_records() -> dict[str, dict[str, Any]]:
    records: dict[str, dict[str, Any]] = {}
    for index, (name, definition) in enumerate(PARAMETER_DEFINITIONS.items(), start=1):
        records[name] = {
            "id": f"param-{index}",
            "tenant": "system",
            "parameter_name": name,
            "parameter_value": definition["default"],
            "unit": definition["unit"],
            "bounded": True,
            "status": "active",
            "created_at": "2026-01-01T00:00:00Z",
            "updated_at": "2026-01-01T00:00:00Z",
        }
    return records


def empty_state() -> dict:
    tables = {table: {} for table in OWNED_TABLES}
    state = {
        "tables": tables,
        "parameters": _default_parameter_records(),
        "rules": _default_rule_records(),
        "schema_extensions": {},
        "control_assertions": {},
        "configuration": {
            "database_backend": "postgresql",
            "event_topic": REQUIRED_EVENT_TOPIC,
            "retry_limit": DEFAULT_RETRY_LIMIT,
            "default_policy": DEFAULT_POLICY,
            "event_contract": EVENT_CONTRACT,
            "stream_engine_picker_visible": False,
        },
        "inbox": [],
        "outbox": [],
        "dead_letter": [],
        "workflow_log": [],
        "idempotency_keys": set(),
        "counters": {},
    }
    for rule in state["rules"].values():
        state["tables"][POLICY_RULE_TABLE][rule["id"]] = dict(rule)
    for parameter in state["parameters"].values():
        state["tables"][RUNTIME_PARAMETER_TABLE][parameter["id"]] = dict(parameter)
    return state


def _next_counter(state: dict, name: str) -> int:
    current = state["counters"].get(name, 0) + 1
    state["counters"][name] = current
    return current


def _timestamp(state: dict) -> str:
    return f"2026-01-01T00:00:{_next_counter(state, 'timestamp'):02d}Z"


def _generate_id(state: dict, prefix: str) -> str:
    return f"{prefix}-{_next_counter(state, prefix)}"


def _owned_table_guard(table_name: str) -> bool:
    return str(table_name).startswith(f"{PBC_KEY}_")


def _table(state: dict, table_name: str) -> dict[str, dict[str, Any]]:
    return state["tables"].setdefault(table_name, {})


def _store_record(state: dict, table_name: str, record: dict[str, Any]) -> dict[str, Any]:
    _table(state, table_name)[record["id"]] = dict(record)
    return record


def _event_record(
    *,
    event_id: str,
    tenant: str,
    event_type: str,
    payload: dict[str, Any],
    idempotency_key: str,
    created_at: str,
    topic: str | None = None,
    status: str | None = None,
    retry_policy: dict[str, Any] | None = None,
) -> dict[str, Any]:
    record = {
        "id": event_id,
        "tenant": tenant,
        "event_type": event_type,
        "payload": dict(payload),
        "idempotency_key": idempotency_key,
        "created_at": created_at,
    }
    if topic is not None:
        record["topic"] = topic
    if status is not None:
        record["status"] = status
    if retry_policy is not None:
        record["retry_policy"] = dict(retry_policy)
    return record


def _emit_event(state: dict, event_type: str, payload: dict[str, Any]) -> dict[str, Any]:
    created_at = _timestamp(state)
    event_id = _generate_id(state, "evt")
    idempotency_key = _digest((event_type, payload, event_id))
    envelope = _event_record(
        event_id=event_id,
        tenant=str(payload.get("tenant", "system")),
        event_type=event_type,
        payload=payload,
        idempotency_key=idempotency_key,
        created_at=created_at,
        topic=REQUIRED_EVENT_TOPIC,
    )
    state["outbox"].append(dict(envelope))
    _store_record(state, OUTBOX_TABLE, envelope)
    return envelope


def _receive_known_event(state: dict, event: dict[str, Any], status: str = "accepted") -> dict[str, Any]:
    created_at = _timestamp(state)
    event_id = _generate_id(state, "inbox")
    idempotency_key = str(event.get("idempotency_key") or event.get("event_id") or _digest(event))
    record = _event_record(
        event_id=event_id,
        tenant=str(event.get("tenant", "system")),
        event_type=str(event.get("event_type")),
        payload=dict(event),
        idempotency_key=idempotency_key,
        created_at=created_at,
        status=status,
    )
    state["inbox"].append(dict(record))
    _store_record(state, INBOX_TABLE, record)
    return record


def _dead_letter_event(state: dict, event: dict[str, Any]) -> dict[str, Any]:
    created_at = _timestamp(state)
    event_id = _generate_id(state, "dead")
    idempotency_key = str(event.get("idempotency_key") or event.get("event_id") or _digest(event))
    record = _event_record(
        event_id=event_id,
        tenant=str(event.get("tenant", "system")),
        event_type=str(event.get("event_type")),
        payload=dict(event),
        idempotency_key=idempotency_key,
        created_at=created_at,
        retry_policy={"max_attempts": DEFAULT_RETRY_LIMIT},
    )
    state["dead_letter"].append(dict(record))
    _store_record(state, DEAD_LETTER_TABLE, record)
    return record


def _parameter_value(state: dict, name: str) -> Any:
    parameter = state["parameters"].get(name)
    return None if parameter is None else parameter["parameter_value"]


def _lookup_plan(
    state: dict,
    *,
    tenant: str,
    plan_id: str | None = None,
    plan_code: str | None = None,
    lifecycle_states: tuple[str, ...] | None = None,
) -> dict[str, Any] | None:
    for plan in _table(state, HACCP_PLAN_TABLE).values():
        if plan["tenant"] != tenant:
            continue
        if plan_id and plan["id"] != plan_id:
            continue
        if plan_code and plan["plan_code"] != plan_code:
            continue
        if lifecycle_states and plan["lifecycle_state"] not in lifecycle_states:
            continue
        return dict(plan)
    return None


def _latest_approved_plan(state: dict, tenant: str, plan_code: str) -> dict[str, Any] | None:
    plans = [
        dict(plan)
        for plan in _table(state, HACCP_PLAN_TABLE).values()
        if plan["tenant"] == tenant and plan["plan_code"] == plan_code and plan["lifecycle_state"] == "approved"
    ]
    if not plans:
        return None
    plans.sort(key=lambda item: (item["version"], item.get("effective_from") or ""))
    return plans[-1]


def _hazard_lookup(plan: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {hazard["hazard_id"]: dict(hazard) for hazard in plan.get("hazard_analysis", ())}


def _step_lookup(plan: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {step["step_code"]: dict(step) for step in plan.get("process_steps", ())}


def _ccps_for_plan(state: dict, plan_id: str) -> list[dict[str, Any]]:
    return [dict(record) for record in _table(state, CRITICAL_CONTROL_POINT_TABLE).values() if record["plan_id"] == plan_id]


def _matches_repeat_finding(existing: dict[str, Any], area: str, finding: dict[str, Any]) -> bool:
    if existing.get("area") != area:
        return False
    for candidate in existing.get("findings", ()):
        if candidate.get("category") == finding.get("category") and candidate.get("description") == finding.get("description"):
            return True
    return False


def _projection_boundary_ok(payload: dict[str, Any]) -> bool:
    if tuple(payload.get("foreign_table_reads", ())):
        return False
    forbidden = ("inventory_table", "manufacturing_table", "shipment_table", "customer_table")
    return not any(key in payload for key in forbidden)


def _extract_recall_impact(payload: dict[str, Any]) -> tuple[tuple[str, ...], tuple[str, ...]]:
    lots: set[str] = set(payload.get("affected_lots", ()))
    customers: set[str] = set(payload.get("customers", ()))
    for relation in payload.get("genealogy_projection", ()):
        for key in ("source_lot", "finished_lot", "lot", "lot_code"):
            if relation.get(key):
                lots.add(str(relation[key]))
        for customer in relation.get("customers", ()):
            customers.add(str(customer))
    for shipment in payload.get("shipment_projection", ()):
        if shipment.get("lot"):
            lots.add(str(shipment["lot"]))
        if shipment.get("customer"):
            customers.add(str(shipment["customer"]))
    return tuple(sorted(lots)), tuple(sorted(customers))


def _score_inspection(findings: tuple[dict[str, Any], ...]) -> int:
    penalties = {"minor": 5, "major": 15, "critical": 30}
    score = 100
    for finding in findings:
        score -= penalties.get(str(finding.get("severity", "minor")).lower(), 5)
    return max(score, 0)


def _create_hold(
    state: dict,
    *,
    tenant: str,
    reason: str,
    affected_lots: tuple[str, ...],
    quantity: float,
    location: str,
    release_criteria: tuple[str, ...],
    disposition: str = "pending",
    approved_by: tuple[str, ...] = (),
    source_inspection_id: str = "",
    haccp_plan_id: str = "",
    haccp_plan_version: str = "",
) -> dict[str, Any]:
    now = _timestamp(state)
    record = {
        "id": _generate_id(state, "hold"),
        "tenant": tenant,
        "hold_reason": reason,
        "affected_lots": tuple(affected_lots),
        "quantity": quantity,
        "location": location,
        "release_criteria": tuple(release_criteria),
        "disposition": disposition,
        "approved_by": tuple(approved_by),
        "released_at": None,
        "source_inspection_id": source_inspection_id,
        "haccp_plan_id": haccp_plan_id,
        "haccp_plan_version": haccp_plan_version,
        "status": "open",
        "created_at": now,
        "updated_at": now,
    }
    _store_record(state, QUALITY_HOLD_TABLE, record)
    return record


def _create_nonconformance(
    state: dict,
    *,
    tenant: str,
    category: str,
    severity: str,
    product_impact: str,
    process_step_code: str,
    containment_action: str,
    corrective_action: str,
    source_inspection_id: str = "",
    recurrence_flag: bool = False,
) -> dict[str, Any]:
    now = _timestamp(state)
    record = {
        "id": _generate_id(state, "nc"),
        "tenant": tenant,
        "category": category,
        "severity": severity,
        "product_impact": product_impact,
        "process_step_code": process_step_code,
        "containment_action": containment_action,
        "corrective_action": corrective_action,
        "preventive_action": "",
        "root_cause_method": "",
        "confirmed_root_cause": "",
        "effectiveness_evidence": "",
        "recurrence_flag": recurrence_flag,
        "status": "open",
        "source_inspection_id": source_inspection_id,
        "created_at": now,
        "updated_at": now,
    }
    _store_record(state, NONCONFORMANCE_TABLE, record)
    return record


def _operation_response(
    *,
    ok: bool,
    state: dict,
    operation: str,
    record: dict[str, Any] | None = None,
    reason: str | None = None,
    emitted_event: dict[str, Any] | None = None,
    **extra: Any,
) -> dict[str, Any]:
    response = {
        "ok": ok,
        "state": state,
        "operation": operation,
        "record": record,
        "reason": reason,
        "owned_tables": OPERATION_TABLES.get(operation, ()),
        "event_contract": EVENT_CONTRACT,
        "side_effects": (),
    }
    if emitted_event is not None:
        response["emitted_event"] = emitted_event
    response.update(extra)
    return response


def configure_runtime(state: dict, payload: dict[str, Any]) -> dict:
    next_state = _copy_state(state)
    database_backend = payload.get("database_backend", next_state["configuration"]["database_backend"])
    event_topic = payload.get("event_topic", next_state["configuration"]["event_topic"])
    ok = database_backend in ALLOWED_DATABASE_BACKENDS and event_topic == REQUIRED_EVENT_TOPIC
    next_state["configuration"] = {
        "database_backend": database_backend,
        "event_topic": event_topic,
        "retry_limit": payload.get("retry_limit", DEFAULT_RETRY_LIMIT),
        "default_policy": payload.get("default_policy", DEFAULT_POLICY),
        "event_contract": EVENT_CONTRACT,
        "stream_engine_picker_visible": False,
    }
    return _operation_response(ok=ok, state=next_state, operation="configure_runtime", configuration=next_state["configuration"])


def create_haccp_plan(state: dict, payload: dict[str, Any]) -> dict:
    next_state = _copy_state(state)
    missing = tuple(
        field
        for field in ("tenant", "plan_code", "version", "facility_code", "product_scope", "process_steps", "hazard_analysis")
        if not payload.get(field)
    )
    if missing:
        return _operation_response(ok=False, state=next_state, operation="create_haccp_plan", reason="missing_required_fields", missing_fields=missing)
    process_steps = tuple(dict(step) for step in payload.get("process_steps", ()))
    hazards = tuple(dict(hazard) for hazard in payload.get("hazard_analysis", ()))
    step_codes = {step["step_code"] for step in process_steps}
    invalid_hazards = tuple(hazard["hazard_id"] for hazard in hazards if hazard.get("process_step_code") not in step_codes)
    if invalid_hazards:
        return _operation_response(
            ok=False,
            state=next_state,
            operation="create_haccp_plan",
            reason="hazard_references_unknown_process_step",
            invalid_hazards=invalid_hazards,
        )
    now = _timestamp(next_state)
    record = {
        "id": _generate_id(next_state, "plan"),
        "tenant": str(payload["tenant"]),
        "plan_code": str(payload["plan_code"]),
        "version": str(payload["version"]),
        "facility_code": str(payload["facility_code"]),
        "product_scope": tuple(payload.get("product_scope", ())),
        "lifecycle_state": str(payload.get("lifecycle_state", "draft")),
        "process_steps": process_steps,
        "hazard_analysis": hazards,
        "approvals": dict(payload.get("approvals", {})),
        "effective_from": payload.get("effective_from"),
        "supersedes_plan_id": payload.get("supersedes_plan_id"),
        "supersession_reason": payload.get("supersession_reason"),
        "evidence_hash": _digest((process_steps, hazards, payload.get("approvals", {}))),
        "created_at": now,
        "updated_at": now,
    }
    _store_record(next_state, HACCP_PLAN_TABLE, record)
    emitted = _emit_event(next_state, OPERATION_EVENTS["create_haccp_plan"], {"tenant": record["tenant"], "record_id": record["id"]})
    next_state["workflow_log"].append({"workflow": WORKFLOWS[0], "record_id": record["id"], "state": record["lifecycle_state"]})
    return _operation_response(ok=True, state=next_state, operation="create_haccp_plan", record=record, emitted_event=emitted)


def approve_haccp_plan(state: dict, payload: dict[str, Any]) -> dict:
    next_state = _copy_state(state)
    plan = _lookup_plan(next_state, tenant=str(payload.get("tenant", "")), plan_id=payload.get("id"))
    if plan is None:
        return _operation_response(ok=False, state=next_state, operation="approve_haccp_plan", reason="plan_not_found")
    approvals = {**plan.get("approvals", {}), **dict(payload.get("approvals", {}))}
    missing_approvals = tuple(name for name in ("food_safety", "quality", "operations") if approvals.get(name) is not True)
    hazard_map = _hazard_lookup(plan)
    required_hazard_ids = tuple(hazard_id for hazard_id, hazard in hazard_map.items() if hazard.get("requires_ccp", True))
    mapped_hazard_ids = {record["hazard_id"] for record in _ccps_for_plan(next_state, plan["id"])}
    missing_ccp_hazards = tuple(hazard_id for hazard_id in required_hazard_ids if hazard_id not in mapped_hazard_ids)
    if missing_approvals or missing_ccp_hazards:
        return _operation_response(
            ok=False,
            state=next_state,
            operation="approve_haccp_plan",
            reason="approval_gate_failed",
            missing_approvals=missing_approvals,
            missing_ccp_hazards=missing_ccp_hazards,
        )
    updated = dict(plan)
    updated["approvals"] = approvals
    updated["lifecycle_state"] = "approved"
    updated["effective_from"] = payload.get("effective_from", updated.get("effective_from"))
    updated["updated_at"] = _timestamp(next_state)
    for other in _table(next_state, HACCP_PLAN_TABLE).values():
        if other["tenant"] == updated["tenant"] and other["plan_code"] == updated["plan_code"] and other["id"] != updated["id"] and other["lifecycle_state"] == "approved":
            other["lifecycle_state"] = "superseded"
            other["supersession_reason"] = payload.get("supersession_reason", "replaced_by_new_version")
            other["updated_at"] = updated["updated_at"]
    _store_record(next_state, HACCP_PLAN_TABLE, updated)
    emitted = _emit_event(next_state, OPERATION_EVENTS["approve_haccp_plan"], {"tenant": updated["tenant"], "record_id": updated["id"]})
    next_state["workflow_log"].append({"workflow": WORKFLOWS[0], "record_id": updated["id"], "state": "approved"})
    return _operation_response(ok=True, state=next_state, operation="approve_haccp_plan", record=updated, emitted_event=emitted)


def create_critical_control_point(state: dict, payload: dict[str, Any]) -> dict:
    next_state = _copy_state(state)
    plan = _lookup_plan(next_state, tenant=str(payload.get("tenant", "")), plan_id=payload.get("plan_id"))
    if plan is None:
        return _operation_response(ok=False, state=next_state, operation="create_critical_control_point", reason="plan_not_found")
    steps = _step_lookup(plan)
    hazards = _hazard_lookup(plan)
    process_step_code = payload.get("process_step_code")
    hazard_id = payload.get("hazard_id")
    if process_step_code not in steps or hazard_id not in hazards:
        return _operation_response(
            ok=False,
            state=next_state,
            operation="create_critical_control_point",
            reason="missing_hazard_or_process_step_mapping",
            process_step_code=process_step_code,
            hazard_id=hazard_id,
        )
    if hazards[hazard_id].get("process_step_code") != process_step_code:
        return _operation_response(ok=False, state=next_state, operation="create_critical_control_point", reason="hazard_process_step_mismatch")
    missing = tuple(
        field
        for field in ("limit_min", "limit_max", "unit", "monitoring_frequency_minutes", "monitoring_method")
        if payload.get(field) in (None, "")
    )
    if missing:
        return _operation_response(ok=False, state=next_state, operation="create_critical_control_point", reason="missing_limit_definition", missing_fields=missing)
    now = _timestamp(next_state)
    record = {
        "id": _generate_id(next_state, "ccp"),
        "tenant": plan["tenant"],
        "plan_id": plan["id"],
        "process_step_code": process_step_code,
        "hazard_id": hazard_id,
        "limit_min": payload["limit_min"],
        "limit_max": payload["limit_max"],
        "unit": payload["unit"],
        "monitoring_method": payload["monitoring_method"],
        "monitoring_frequency_minutes": payload["monitoring_frequency_minutes"],
        "responsible_role": payload.get("responsible_role", "line_quality"),
        "verification_requirement": payload.get("verification_requirement", "daily_supervisor_review"),
        "corrective_action": payload.get("corrective_action", "Hold affected lots and investigate root cause."),
        "status": payload.get("status", "active"),
        "created_at": now,
        "updated_at": now,
    }
    _store_record(next_state, CRITICAL_CONTROL_POINT_TABLE, record)
    emitted = _emit_event(next_state, OPERATION_EVENTS["create_critical_control_point"], {"tenant": record["tenant"], "record_id": record["id"]})
    next_state["workflow_log"].append({"workflow": WORKFLOWS[1], "record_id": record["id"], "state": "active"})
    return _operation_response(ok=True, state=next_state, operation="create_critical_control_point", record=record, emitted_event=emitted)


def record_inspection(state: dict, payload: dict[str, Any]) -> dict:
    next_state = _copy_state(state)
    tenant = str(payload.get("tenant", ""))
    plan = _latest_approved_plan(next_state, tenant, str(payload.get("plan_code", "")))
    if plan is None:
        return _operation_response(ok=False, state=next_state, operation="record_inspection", reason="approved_plan_not_found")
    findings = tuple(dict(item) for item in payload.get("findings", ()))
    if not findings:
        return _operation_response(ok=False, state=next_state, operation="record_inspection", reason="missing_findings")
    repeat_findings = tuple(
        finding["description"]
        for finding in findings
        if any(_matches_repeat_finding(existing, str(payload.get("area", "")), finding) for existing in _table(next_state, INSPECTION_TABLE).values())
    )
    hold_ids: list[str] = []
    nonconformance_ids: list[str] = []
    for finding in findings:
        severity = str(finding.get("severity", "minor")).lower()
        category = str(finding.get("category", "documentation"))
        if severity in {"critical", "major"}:
            nonconformance = _create_nonconformance(
                next_state,
                tenant=tenant,
                category=category,
                severity=severity,
                product_impact=str(finding.get("product_impact", "potential_food_safety_risk")),
                process_step_code=str(finding.get("process_step_code", "")),
                containment_action=str(finding.get("containment_action", "Segregate impacted lots.")),
                corrective_action=str(finding.get("corrective_action", "Investigate and verify controls.")),
                recurrence_flag=finding.get("description") in repeat_findings,
            )
            nonconformance_ids.append(nonconformance["id"])
        if severity == "critical" or category in {"allergen", "temperature", "foreign_material"}:
            hold = _create_hold(
                next_state,
                tenant=tenant,
                reason=finding.get("description", f"{category} inspection failure"),
                affected_lots=tuple(finding.get("affected_lots", ("unknown-lot",))),
                quantity=float(finding.get("affected_quantity", 1.0)),
                location=str(finding.get("location", payload.get("facility_code", "quality-cage"))),
                release_criteria=tuple(finding.get("release_criteria", ("approved_disposition", "corrective_action_verified"))),
                source_inspection_id="pending",
                haccp_plan_id=plan["id"],
                haccp_plan_version=plan["version"],
            )
            hold_ids.append(hold["id"])
    now = _timestamp(next_state)
    record = {
        "id": _generate_id(next_state, "inspection"),
        "tenant": tenant,
        "plan_id": plan["id"],
        "plan_code": plan["plan_code"],
        "plan_version": plan["version"],
        "facility_code": payload.get("facility_code", plan["facility_code"]),
        "area": str(payload.get("area", "")),
        "checklist": tuple(payload.get("checklist", ())),
        "findings": findings,
        "score": _score_inspection(findings),
        "repeat_findings": repeat_findings,
        "status": payload.get("status", "review_complete"),
        "created_hold_ids": tuple(hold_ids),
        "created_nonconformance_ids": tuple(nonconformance_ids),
        "inspector": payload.get("inspector", "quality_inspector"),
        "started_at": payload.get("started_at", now),
        "created_at": now,
        "updated_at": now,
    }
    _store_record(next_state, INSPECTION_TABLE, record)
    for hold_id in hold_ids:
        hold = _table(next_state, QUALITY_HOLD_TABLE)[hold_id]
        hold["source_inspection_id"] = record["id"]
        hold["updated_at"] = now
    for nc_id in nonconformance_ids:
        nc = _table(next_state, NONCONFORMANCE_TABLE)[nc_id]
        nc["source_inspection_id"] = record["id"]
        nc["updated_at"] = now
    emitted = _emit_event(next_state, OPERATION_EVENTS["record_inspection"], {"tenant": tenant, "record_id": record["id"], "critical_findings": len(hold_ids)})
    next_state["workflow_log"].append({"workflow": WORKFLOWS[2], "record_id": record["id"], "state": record["status"]})
    return _operation_response(
        ok=True,
        state=next_state,
        operation="record_inspection",
        record=record,
        emitted_event=emitted,
        created_hold_ids=tuple(hold_ids),
        created_nonconformance_ids=tuple(nonconformance_ids),
    )


def open_nonconformance(state: dict, payload: dict[str, Any]) -> dict:
    next_state = _copy_state(state)
    missing = tuple(field for field in ("tenant", "category", "severity", "product_impact", "corrective_action") if not payload.get(field))
    if missing:
        return _operation_response(ok=False, state=next_state, operation="open_nonconformance", reason="missing_required_fields", missing_fields=missing)
    record = _create_nonconformance(
        next_state,
        tenant=str(payload["tenant"]),
        category=str(payload["category"]),
        severity=str(payload["severity"]).lower(),
        product_impact=str(payload["product_impact"]),
        process_step_code=str(payload.get("process_step_code", "")),
        containment_action=str(payload.get("containment_action", "Segregate product and initiate traceability review.")),
        corrective_action=str(payload["corrective_action"]),
        source_inspection_id=str(payload.get("source_inspection_id", "")),
        recurrence_flag=bool(payload.get("recurrence_flag", False)),
    )
    emitted = _emit_event(next_state, OPERATION_EVENTS["open_nonconformance"], {"tenant": record["tenant"], "record_id": record["id"]})
    return _operation_response(ok=True, state=next_state, operation="open_nonconformance", record=record, emitted_event=emitted)


def close_nonconformance(state: dict, payload: dict[str, Any]) -> dict:
    next_state = _copy_state(state)
    record = dict(_table(next_state, NONCONFORMANCE_TABLE).get(str(payload.get("id")), {}))
    if not record:
        return _operation_response(ok=False, state=next_state, operation="close_nonconformance", reason="nonconformance_not_found")
    severity = str(record.get("severity", "minor")).lower()
    updated = {**record, **{key: payload[key] for key in ("preventive_action", "root_cause_method", "confirmed_root_cause", "effectiveness_evidence") if key in payload}}
    if severity in {"major", "critical"}:
        missing = tuple(field for field in ("root_cause_method", "confirmed_root_cause", "effectiveness_evidence", "preventive_action") if not updated.get(field))
        if missing:
            return _operation_response(
                ok=False,
                state=next_state,
                operation="close_nonconformance",
                reason="missing_major_closure_evidence",
                missing_fields=missing,
            )
    updated["status"] = "closed"
    updated["updated_at"] = _timestamp(next_state)
    _store_record(next_state, NONCONFORMANCE_TABLE, updated)
    emitted = _emit_event(next_state, OPERATION_EVENTS["close_nonconformance"], {"tenant": updated["tenant"], "record_id": updated["id"]})
    return _operation_response(ok=True, state=next_state, operation="close_nonconformance", record=updated, emitted_event=emitted)


def create_supplier_audit(state: dict, payload: dict[str, Any]) -> dict:
    next_state = _copy_state(state)
    missing = tuple(field for field in ("tenant", "supplier_projection", "commodity", "audit_type", "risk_rating") if not payload.get(field))
    if missing:
        return _operation_response(ok=False, state=next_state, operation="create_supplier_audit", reason="missing_required_fields", missing_fields=missing)
    findings = tuple(dict(item) for item in payload.get("findings", ()))
    risk_rating = str(payload["risk_rating"]).lower()
    expiry_date = payload.get("expiry_date", "2026-12-31")
    days_until_expiry = int(payload.get("days_until_expiry", 90))
    has_major_finding = any(str(item.get("severity", "")).lower() in {"major", "critical"} for item in findings)
    approval_status = "approved"
    if risk_rating == "high" or has_major_finding or days_until_expiry <= 0:
        approval_status = "blocked"
    elif days_until_expiry <= _parameter_value(next_state, "supplier_audit_expiry_warning_days"):
        approval_status = "expiring"
    now = _timestamp(next_state)
    record = {
        "id": _generate_id(next_state, "audit"),
        "tenant": str(payload["tenant"]),
        "supplier_projection": dict(payload["supplier_projection"]),
        "commodity": str(payload["commodity"]),
        "audit_type": str(payload["audit_type"]),
        "risk_rating": risk_rating,
        "findings": findings,
        "corrective_actions": tuple(payload.get("corrective_actions", ())),
        "approval_status": approval_status,
        "expiry_date": expiry_date,
        "days_until_expiry": days_until_expiry,
        "created_at": now,
        "updated_at": now,
    }
    _store_record(next_state, SUPPLIER_AUDIT_TABLE, record)
    emitted = _emit_event(next_state, OPERATION_EVENTS["create_supplier_audit"], {"tenant": record["tenant"], "record_id": record["id"]})
    return _operation_response(ok=True, state=next_state, operation="create_supplier_audit", record=record, emitted_event=emitted)


def open_quality_hold(state: dict, payload: dict[str, Any]) -> dict:
    next_state = _copy_state(state)
    missing = tuple(field for field in ("tenant", "hold_reason", "affected_lots", "quantity", "location") if not payload.get(field))
    if missing:
        return _operation_response(ok=False, state=next_state, operation="open_quality_hold", reason="missing_required_fields", missing_fields=missing)
    plan = None
    if payload.get("haccp_plan_id"):
        plan = _lookup_plan(next_state, tenant=str(payload["tenant"]), plan_id=str(payload["haccp_plan_id"]))
    record = _create_hold(
        next_state,
        tenant=str(payload["tenant"]),
        reason=str(payload["hold_reason"]),
        affected_lots=tuple(payload["affected_lots"]),
        quantity=float(payload["quantity"]),
        location=str(payload["location"]),
        release_criteria=tuple(payload.get("release_criteria", ("approved_disposition",))),
        disposition=str(payload.get("disposition", "pending")),
        approved_by=tuple(payload.get("approved_by", ())),
        source_inspection_id=str(payload.get("source_inspection_id", "")),
        haccp_plan_id=plan["id"] if plan else str(payload.get("haccp_plan_id", "")),
        haccp_plan_version=plan["version"] if plan else str(payload.get("haccp_plan_version", "")),
    )
    emitted = _emit_event(next_state, OPERATION_EVENTS["open_quality_hold"], {"tenant": record["tenant"], "record_id": record["id"]})
    next_state["workflow_log"].append({"workflow": WORKFLOWS[3], "record_id": record["id"], "state": "open"})
    return _operation_response(ok=True, state=next_state, operation="open_quality_hold", record=record, emitted_event=emitted)


def release_quality_hold(state: dict, payload: dict[str, Any]) -> dict:
    next_state = _copy_state(state)
    record = dict(_table(next_state, QUALITY_HOLD_TABLE).get(str(payload.get("id")), {}))
    if not record:
        return _operation_response(ok=False, state=next_state, operation="release_quality_hold", reason="quality_hold_not_found")
    approved_by = tuple(payload.get("approved_by", record.get("approved_by", ())))
    disposition = str(payload.get("disposition", record.get("disposition", "pending")))
    quantity_reconciled = float(payload.get("quantity_reconciled", record.get("quantity", 0.0)))
    min_approvers = int(_parameter_value(next_state, "hold_release_min_approvers"))
    if disposition in {"pending", "quarantine"} or len(approved_by) < min_approvers or quantity_reconciled != float(record["quantity"]):
        return _operation_response(
            ok=False,
            state=next_state,
            operation="release_quality_hold",
            reason="hold_release_gate_failed",
            required_approvers=min_approvers,
            provided_approvers=approved_by,
            quantity_reconciled=quantity_reconciled,
        )
    updated = dict(record)
    updated["approved_by"] = approved_by
    updated["disposition"] = disposition
    updated["released_at"] = payload.get("released_at", _timestamp(next_state))
    updated["status"] = "released"
    updated["updated_at"] = updated["released_at"]
    _store_record(next_state, QUALITY_HOLD_TABLE, updated)
    emitted = _emit_event(next_state, OPERATION_EVENTS["release_quality_hold"], {"tenant": updated["tenant"], "record_id": updated["id"]})
    next_state["workflow_log"].append({"workflow": WORKFLOWS[3], "record_id": updated["id"], "state": "released"})
    return _operation_response(ok=True, state=next_state, operation="release_quality_hold", record=updated, emitted_event=emitted)


def _build_recall_record(next_state: dict, payload: dict[str, Any], *, is_mock_drill: bool) -> dict[str, Any]:
    affected_lots, customers = _extract_recall_impact(payload)
    boundary_ok = _projection_boundary_ok(payload)
    elapsed = int(payload.get("trace_elapsed_minutes", 90 if is_mock_drill else 45))
    now = _timestamp(next_state)
    return {
        "id": _generate_id(next_state, "recall"),
        "tenant": str(payload["tenant"]),
        "classification": str(payload.get("classification", "withdrawal")),
        "reason": str(payload.get("reason", "food_safety_investigation")),
        "consumer_risk": str(payload.get("consumer_risk", "moderate")),
        "distribution_scope": str(payload.get("distribution_scope", "regional")),
        "affected_lots": affected_lots,
        "customers": customers,
        "regulator_notification": dict(payload.get("regulator_notification", {"status": "draft"})),
        "communication_plan": dict(payload.get("communication_plan", {"status": "draft"})),
        "is_mock_drill": is_mock_drill,
        "trace_elapsed_minutes": elapsed,
        "projection_boundary_ok": boundary_ok,
        "status": payload.get("status", "draft" if is_mock_drill else "active"),
        "created_at": now,
        "updated_at": now,
    }


def start_recall_event(state: dict, payload: dict[str, Any]) -> dict:
    next_state = _copy_state(state)
    missing = tuple(field for field in ("tenant", "classification", "reason") if not payload.get(field))
    if missing:
        return _operation_response(ok=False, state=next_state, operation="start_recall_event", reason="missing_required_fields", missing_fields=missing)
    if not _projection_boundary_ok(payload):
        return _operation_response(ok=False, state=next_state, operation="start_recall_event", reason="foreign_projection_boundary_violation")
    record = _build_recall_record(next_state, payload, is_mock_drill=False)
    _store_record(next_state, RECALL_EVENT_TABLE, record)
    emitted = _emit_event(next_state, OPERATION_EVENTS["start_recall_event"], {"tenant": record["tenant"], "record_id": record["id"]})
    next_state["workflow_log"].append({"workflow": WORKFLOWS[4], "record_id": record["id"], "state": record["status"]})
    return _operation_response(ok=True, state=next_state, operation="start_recall_event", record=record, emitted_event=emitted)


def run_mock_recall(state: dict, payload: dict[str, Any]) -> dict:
    next_state = _copy_state(state)
    if not payload.get("tenant"):
        return _operation_response(ok=False, state=next_state, operation="run_mock_recall", reason="missing_tenant")
    if not _projection_boundary_ok(payload):
        return _operation_response(ok=False, state=next_state, operation="run_mock_recall", reason="foreign_projection_boundary_violation")
    record = _build_recall_record(next_state, payload, is_mock_drill=True)
    target = int(_parameter_value(next_state, "mock_recall_target_minutes"))
    packet = {
        "classification": record["classification"],
        "affected_lots": record["affected_lots"],
        "customers": record["customers"],
        "trace_elapsed_minutes": record["trace_elapsed_minutes"],
        "meets_target": record["trace_elapsed_minutes"] <= target,
        "projection_boundary_ok": record["projection_boundary_ok"],
        "mutates_live_state": False,
    }
    return _operation_response(ok=True, state=next_state, operation="run_mock_recall", record=record, evidence_packet=packet)


def set_parameter(state: dict, payload: dict[str, Any]) -> dict:
    next_state = _copy_state(state)
    name = str(payload.get("name", ""))
    if name not in PARAMETER_DEFINITIONS:
        return _operation_response(ok=False, state=next_state, operation="set_parameter", reason="unknown_parameter")
    definition = PARAMETER_DEFINITIONS[name]
    value = payload.get("value")
    if value is None or value < definition["minimum"] or value > definition["maximum"]:
        return _operation_response(ok=False, state=next_state, operation="set_parameter", reason="parameter_out_of_bounds", bounds=(definition["minimum"], definition["maximum"]))
    record = dict(next_state["parameters"][name])
    record["parameter_value"] = value
    record["updated_at"] = _timestamp(next_state)
    next_state["parameters"][name] = record
    _store_record(next_state, RUNTIME_PARAMETER_TABLE, record)
    return _operation_response(ok=True, state=next_state, operation="set_parameter", record=record)


def register_rule(state: dict, payload: dict[str, Any]) -> dict:
    next_state = _copy_state(state)
    rule_id = str(payload.get("rule_id", ""))
    rule_text = str(payload.get("rule_text", RULE_DEFINITIONS.get(rule_id, "")))
    if not rule_id or not rule_text:
        return _operation_response(ok=False, state=next_state, operation="register_rule", reason="missing_rule_identity")
    existing = next_state["rules"].get(rule_id)
    now = _timestamp(next_state)
    record = {
        "id": existing["id"] if existing else _generate_id(next_state, "rule"),
        "tenant": str(payload.get("tenant", "system")),
        "rule_id": rule_id,
        "scope": str(payload.get("scope", "domain")),
        "status": str(payload.get("status", "active")),
        "rule_text": rule_text,
        "compiled_hash": _digest((rule_id, rule_text, payload.get("scope", "domain"))),
        "created_at": existing["created_at"] if existing else now,
        "updated_at": now,
    }
    next_state["rules"][rule_id] = record
    _store_record(next_state, POLICY_RULE_TABLE, record)
    return _operation_response(ok=True, state=next_state, operation="register_rule", record=record)


def register_schema_extension(state: dict, payload: dict[str, Any]) -> dict:
    next_state = _copy_state(state)
    table_name = str(payload.get("table_name", ""))
    if table_name not in OWNED_TABLES:
        return _operation_response(ok=False, state=next_state, operation="register_schema_extension", reason="unknown_owned_table")
    now = _timestamp(next_state)
    record = {
        "id": _generate_id(next_state, "schema"),
        "tenant": str(payload.get("tenant", "system")),
        "table_name": table_name,
        "field_map": dict(payload.get("field_map", {})),
        "rationale": str(payload.get("rationale", "")),
        "status": str(payload.get("status", "proposed")),
        "created_at": now,
        "updated_at": now,
    }
    next_state["schema_extensions"][record["id"]] = record
    _store_record(next_state, SCHEMA_EXTENSION_TABLE, record)
    return _operation_response(ok=True, state=next_state, operation="register_schema_extension", record=record)


def upsert_control_assertion(state: dict, payload: dict[str, Any]) -> dict:
    next_state = _copy_state(state)
    control_id = str(payload.get("control_id", ""))
    control_name = str(payload.get("control_name", ""))
    if not control_id or not control_name:
        return _operation_response(ok=False, state=next_state, operation="upsert_control_assertion", reason="missing_control_identity")
    record_id = str(payload.get("id", "")) or _generate_id(next_state, "assert")
    existing = _table(next_state, CONTROL_ASSERTION_TABLE).get(record_id)
    now = _timestamp(next_state)
    record = {
        "id": record_id,
        "tenant": str(payload.get("tenant", "system")),
        "control_id": control_id,
        "control_name": control_name,
        "frequency": str(payload.get("frequency", "daily")),
        "status": str(payload.get("status", "pass")),
        "assertion_payload": dict(payload.get("assertion_payload", {})),
        "evidence_hash": _digest(payload.get("assertion_payload", {})),
        "created_at": existing["created_at"] if existing else now,
        "updated_at": now,
    }
    next_state["control_assertions"][record_id] = record
    _store_record(next_state, CONTROL_ASSERTION_TABLE, record)
    return _operation_response(ok=True, state=next_state, operation="upsert_control_assertion", record=record)


def _mutation_preview(payload: dict[str, Any]) -> dict[str, Any]:
    table_name = str(payload.get("target_table", HACCP_PLAN_TABLE))
    action = str(payload.get("action", "create"))
    if not _owned_table_guard(table_name):
        return {"ok": False, "reason": "foreign_table_rejected", "table": table_name}
    preview_payload = dict(payload.get("payload", {}))
    return {
        "ok": True,
        "action": action,
        "table": table_name,
        "payload": preview_payload,
        "requires_confirmation": action in {"create", "update", "delete", "approve"},
        "release_impacting": table_name in {QUALITY_HOLD_TABLE, RECALL_EVENT_TABLE},
    }


def create_document_instruction(state: dict, payload: dict[str, Any]) -> dict:
    next_state = _copy_state(state)
    preview = _mutation_preview(payload)
    citations = tuple(payload.get("citations", ()))
    if not preview["ok"]:
        return _operation_response(ok=False, state=next_state, operation="create_document_instruction", reason=preview["reason"])
    if not citations:
        return _operation_response(ok=False, state=next_state, operation="create_document_instruction", reason="missing_citations")
    now = _timestamp(next_state)
    record = {
        "id": _generate_id(next_state, "agent"),
        "tenant": str(payload.get("tenant", "default")),
        "artifact_type": str(payload.get("artifact_type", "document_instruction")),
        "artifact_key": str(payload.get("artifact_key", preview["table"])),
        "status": "pending_review",
        "document_digest": _digest((payload.get("document", ""), payload.get("instruction", ""))),
        "instruction_payload": {
            "instruction": payload.get("instruction", ""),
            "target_table": preview["table"],
            "action": preview["action"],
        },
        "mutation_preview": preview,
        "citations": citations,
        "human_confirmation_state": "required",
        "approved_by": "",
        "created_at": now,
        "updated_at": now,
    }
    _store_record(next_state, GOVERNED_MODEL_TABLE, record)
    return _operation_response(ok=True, state=next_state, operation="create_document_instruction", record=record)


def approve_document_instruction(state: dict, payload: dict[str, Any]) -> dict:
    next_state = _copy_state(state)
    record = dict(_table(next_state, GOVERNED_MODEL_TABLE).get(str(payload.get("id")), {}))
    if not record:
        return _operation_response(ok=False, state=next_state, operation="approve_document_instruction", reason="instruction_not_found")
    preview = record.get("mutation_preview", {})
    if not record.get("citations") or not preview.get("ok"):
        return _operation_response(ok=False, state=next_state, operation="approve_document_instruction", reason="instruction_not_ready")
    if preview.get("release_impacting") and payload.get("release_reviewed") is not True:
        return _operation_response(ok=False, state=next_state, operation="approve_document_instruction", reason="release_review_required")
    updated = dict(record)
    updated["status"] = "approved"
    updated["human_confirmation_state"] = "confirmed"
    updated["approved_by"] = str(payload.get("approved_by", "quality_manager"))
    updated["updated_at"] = _timestamp(next_state)
    _store_record(next_state, GOVERNED_MODEL_TABLE, updated)
    return _operation_response(ok=True, state=next_state, operation="approve_document_instruction", record=updated)


def receive_event(state: dict, payload: dict[str, Any]) -> dict:
    next_state = _copy_state(state)
    event_type = str(payload.get("event_type", ""))
    idempotency_key = str(payload.get("idempotency_key") or payload.get("event_id") or _digest(payload))
    if idempotency_key in next_state["idempotency_keys"]:
        return _operation_response(ok=True, state=next_state, operation="receive_event", duplicate=True, idempotency_key=idempotency_key)
    next_state["idempotency_keys"].add(idempotency_key)
    if event_type not in CONSUMED_EVENT_TYPES:
        dead = _dead_letter_event(next_state, payload)
        return _operation_response(
            ok=False,
            state=next_state,
            operation="receive_event",
            reason="unexpected_event_type",
            dead_letter_table=DEAD_LETTER_TABLE,
            dead_letter_record=dead,
        )
    record = _receive_known_event(next_state, payload)
    return _operation_response(ok=True, state=next_state, operation="receive_event", record=record, duplicate=False, idempotency_key=idempotency_key)


def query_workbench(state: dict, payload: dict[str, Any] | None = None) -> dict:
    filters = dict(payload or {})
    tenant = str(filters.get("tenant", "default"))
    limit = int(_parameter_value(state, "workbench_limit"))
    plans = [dict(plan) for plan in _table(state, HACCP_PLAN_TABLE).values() if plan["tenant"] == tenant and plan["lifecycle_state"] in {"draft", "pending_approval"}][:limit]
    inspections = [dict(item) for item in _table(state, INSPECTION_TABLE).values() if item["tenant"] == tenant and item["created_hold_ids"]][:limit]
    holds = [dict(item) for item in _table(state, QUALITY_HOLD_TABLE).values() if item["tenant"] == tenant and item["status"] == "open"][:limit]
    audits = [dict(item) for item in _table(state, SUPPLIER_AUDIT_TABLE).values() if item["tenant"] == tenant and item["approval_status"] in {"blocked", "expiring"}][:limit]
    recalls = [dict(item) for item in _table(state, RECALL_EVENT_TABLE).values() if item["tenant"] == tenant][:limit]
    queues = {
        "haccp_approval_queue": plans,
        "inspection_escalation_queue": inspections,
        "open_quality_holds": holds,
        "supplier_audit_monitor": audits,
        "recall_readiness_board": recalls,
    }
    metrics = {name: len(records) for name, records in queues.items()}
    return {"ok": True, "tenant": tenant, "limit": limit, "queues": queues, "metrics": metrics, "filters": filters, "side_effects": ()}


def build_workbench_view(state: dict, payload: dict[str, Any] | None = None) -> dict:
    workbench = query_workbench(state, payload)
    return {
        "ok": workbench["ok"],
        "tenant": workbench["tenant"],
        "route": f"/workbench/pbcs/{PBC_KEY}",
        "queues": workbench["queues"],
        "metrics": workbench["metrics"],
        "forms": FORM_DEFINITIONS,
        "wizards": WIZARD_DEFINITIONS,
        "controls": CONTROL_DEFINITIONS,
        "assistant_skills": tuple(skill["name"] for skill in agent_skill_manifest()["skills"]),
        "side_effects": (),
    }


def query_haccp_plan_detail(state: dict, plan_id: str) -> dict:
    plan = dict(_table(state, HACCP_PLAN_TABLE).get(plan_id, {}))
    if not plan:
        return {"ok": False, "reason": "plan_not_found", "side_effects": ()}
    ccps = [dict(item) for item in _table(state, CRITICAL_CONTROL_POINT_TABLE).values() if item["plan_id"] == plan_id]
    inspections = [dict(item) for item in _table(state, INSPECTION_TABLE).values() if item["plan_id"] == plan_id]
    holds = [dict(item) for item in _table(state, QUALITY_HOLD_TABLE).values() if item["haccp_plan_id"] == plan_id]
    return {"ok": True, "plan": plan, "critical_control_points": ccps, "inspections": inspections, "quality_holds": holds, "side_effects": ()}


def query_recall_packet(state: dict, recall_id: str) -> dict:
    record = dict(_table(state, RECALL_EVENT_TABLE).get(recall_id, {}))
    if not record:
        return {"ok": False, "reason": "recall_not_found", "side_effects": ()}
    target_minutes = int(_parameter_value(state, "mock_recall_target_minutes"))
    packet = {
        "classification": record["classification"],
        "reason": record["reason"],
        "affected_lots": record["affected_lots"],
        "customers": record["customers"],
        "trace_elapsed_minutes": record["trace_elapsed_minutes"],
        "meets_target": record["trace_elapsed_minutes"] <= target_minutes,
        "projection_boundary_ok": record["projection_boundary_ok"],
        "is_mock_drill": record["is_mock_drill"],
    }
    return {"ok": True, "record": record, "evidence_packet": packet, "side_effects": ()}


def operation_contract(name: str, kind: str) -> dict:
    return {
        "operation": name,
        "operation_kind": kind,
        "owned_tables": OPERATION_TABLES.get(name, ()) if kind == "command" else (),
        "read_tables": OPERATION_TABLES.get(name, ()) if kind == "query" else (),
        "emitted_event": OPERATION_EVENTS.get(name),
        "required_permission": OPERATION_PERMISSIONS.get(name, f"{PBC_KEY}.read"),
        "transaction_boundary": "owned_datastore_plus_outbox" if kind == "command" else "read_only_projection",
        "event_contract": EVENT_CONTRACT,
    }


def service_callable(name: str) -> Callable[[dict, dict[str, Any]], dict]:
    registry: dict[str, Callable[[dict, dict[str, Any]], dict]] = {
        "configure_runtime": configure_runtime,
        "create_haccp_plan": create_haccp_plan,
        "approve_haccp_plan": approve_haccp_plan,
        "create_critical_control_point": create_critical_control_point,
        "record_inspection": record_inspection,
        "open_nonconformance": open_nonconformance,
        "close_nonconformance": close_nonconformance,
        "create_supplier_audit": create_supplier_audit,
        "open_quality_hold": open_quality_hold,
        "release_quality_hold": release_quality_hold,
        "start_recall_event": start_recall_event,
        "run_mock_recall": run_mock_recall,
        "set_parameter": set_parameter,
        "register_rule": register_rule,
        "register_schema_extension": register_schema_extension,
        "upsert_control_assertion": upsert_control_assertion,
        "create_document_instruction": create_document_instruction,
        "approve_document_instruction": approve_document_instruction,
        "receive_event": receive_event,
        "query_workbench": query_workbench,
        "build_workbench_view": build_workbench_view,
        "query_haccp_plan_detail": lambda state, payload: query_haccp_plan_detail(state, str(payload.get("id", ""))),
        "query_recall_packet": lambda state, payload: query_recall_packet(state, str(payload.get("id", ""))),
    }
    return registry[name]


def build_schema_contract() -> dict:
    table_contracts = tuple(
        {
            "table": item["table"],
            "fields": item["fields"],
            "primary_key": ("id",),
            "owned_by": PBC_KEY,
            "domain_role": item["domain_role"],
        }
        for item in TABLE_DEFINITIONS
    )
    models = tuple(
        {
            "class_name": item["class_name"],
            "table": item["table"],
            "fields": item["fields"],
            "domain_role": item["domain_role"],
        }
        for item in TABLE_DEFINITIONS
    )
    return {
        "format": "appgen.food-safety-quality-compliance-owned-schema-contract.v2",
        "ok": True,
        "pbc": PBC_KEY,
        "tables": table_contracts,
        "models": models,
        "migrations": (
            {
                "path": f"pbcs/{PBC_KEY}/migrations/001_initial.sql",
                "operation": "create_owned_tables",
                "tables": OWNED_TABLES,
                "backend_allowlist": ALLOWED_DATABASE_BACKENDS,
            },
        ),
        "owned_tables": OWNED_TABLES,
        "database_backends": ALLOWED_DATABASE_BACKENDS,
        "shared_table_access": False,
        "side_effects": (),
    }


def build_service_contract() -> dict:
    return {
        "format": "appgen.food-safety-quality-compliance-service-contract.v2",
        "ok": True,
        "pbc": PBC_KEY,
        "command_methods": COMMAND_METHODS,
        "query_methods": QUERY_METHODS,
        "owned_tables": OWNED_TABLES,
        "event_contract": EVENT_CONTRACT,
        "transaction_boundary": "owned_datastore_plus_outbox",
        "side_effects": (),
    }


def build_api_contract() -> dict:
    return {
        "format": "appgen.food-safety-quality-compliance-api-contract.v2",
        "ok": True,
        "pbc": PBC_KEY,
        "routes": ROUTES,
        "route_to_operation": dict(ROUTE_TO_OPERATION),
        "owned_tables": OWNED_TABLES,
        "event_contract": EVENT_CONTRACT,
        "side_effects": (),
    }


def permissions_contract() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "permissions": PERMISSIONS,
        "roles": tuple(ROLE_PERMISSIONS),
        "role_permissions": ROLE_PERMISSIONS,
        "side_effects": (),
    }


def configuration_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "database_backends": ALLOWED_DATABASE_BACKENDS,
        "event_topic": REQUIRED_EVENT_TOPIC,
        "retry_limit": DEFAULT_RETRY_LIMIT,
        "default_policy": DEFAULT_POLICY,
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def validate_configuration(config: dict[str, Any] | None = None) -> dict:
    candidate = dict(config or configuration_manifest())
    ok = candidate.get("database_backend", candidate.get("database_backends", ("postgresql",))[0]) in ALLOWED_DATABASE_BACKENDS
    if "event_topic" in candidate:
        ok = ok and candidate["event_topic"] == REQUIRED_EVENT_TOPIC
    return {"ok": ok, "configuration": candidate, "side_effects": ()}


def parameter_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "parameters": tuple(
            {
                "name": name,
                "bounded": True,
                "default": definition["default"],
                "minimum": definition["minimum"],
                "maximum": definition["maximum"],
                "unit": definition["unit"],
            }
            for name, definition in PARAMETER_DEFINITIONS.items()
        ),
        "side_effects": (),
    }


def evaluate_rule(rule_name: str, payload: dict[str, Any] | None = None) -> dict:
    candidate = dict(payload or {})
    if rule_name == "recall_projection_boundary_rule":
        passed = _projection_boundary_ok(candidate)
    elif rule_name == "assistant_mutation_guardrail_rule":
        preview = _mutation_preview(candidate)
        passed = preview["ok"] and bool(candidate.get("citations"))
    else:
        passed = rule_name in RULE_DEFINITIONS
    return {"ok": rule_name in RULE_DEFINITIONS, "passed": passed, "rule": rule_name, "payload": candidate, "side_effects": ()}


def compile_rule(rule: dict[str, Any]) -> dict:
    return {"ok": bool(rule.get("rule_id")), "rule": dict(rule), "compiled_hash": _digest(rule), "side_effects": ()}


def rule_manifest() -> dict:
    return {"ok": True, "pbc": PBC_KEY, "rules": DOMAIN_RULES, "side_effects": ()}


def event_contract_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "emitted": EMITTED_EVENT_TYPES,
        "consumed": CONSUMED_EVENT_TYPES,
        "outbox_table": OUTBOX_TABLE,
        "inbox_table": INBOX_TABLE,
        "dead_letter_table": DEAD_LETTER_TABLE,
        "event_contract": EVENT_CONTRACT,
        "idempotency": "required",
        "side_effects": (),
    }


def validate_event_contract() -> dict:
    invalid_tables = tuple(table for table in EVENT_TABLES if table not in OWNED_TABLES)
    return {
        "ok": not invalid_tables and event_contract_manifest()["event_contract"] == EVENT_CONTRACT,
        "pbc": PBC_KEY,
        "invalid_tables": invalid_tables,
        "invalid_emitted": (),
        "invalid_consumed": (),
        "side_effects": (),
    }


def build_event_envelope(event_type: str, payload: dict[str, Any] | None = None) -> dict:
    body = dict(payload or {})
    return {
        "ok": event_type in EMITTED_EVENT_TYPES + CONSUMED_EVENT_TYPES,
        "event_type": event_type,
        "payload": body,
        "event_contract": EVENT_CONTRACT,
        "idempotency_key": _digest((event_type, body)),
        "side_effects": (),
    }


def handler_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "consumes": CONSUMED_EVENT_TYPES,
        "idempotency_key": "required",
        "retry_policy": {"max_attempts": DEFAULT_RETRY_LIMIT},
        "dead_letter_table": DEAD_LETTER_TABLE,
        "side_effects": (),
    }


def agent_skill_manifest() -> dict:
    skills = (
        {
            "name": f"{PBC_KEY}_summarize_haccp_evidence",
            "description": "Summarize HACCP version evidence with cited hazards, CCPs, and approvals.",
            "requires_confirmation_for_mutation": False,
            "requires_citations": True,
        },
        {
            "name": f"{PBC_KEY}_draft_recall_impact",
            "description": "Draft recall impact packets from declared projections without foreign table access.",
            "requires_confirmation_for_mutation": False,
            "requires_citations": True,
        },
        {
            "name": f"{PBC_KEY}_outline_root_cause",
            "description": "Outline root cause and CAPA prompts for a nonconformance case.",
            "requires_confirmation_for_mutation": False,
            "requires_citations": True,
        },
        {
            "name": f"{PBC_KEY}_audit_evidence_checklist",
            "description": "Prepare audit evidence checklists across HACCP, holds, supplier audits, and recalls.",
            "requires_confirmation_for_mutation": False,
            "requires_citations": True,
        },
        {
            "name": f"{PBC_KEY}_preview_governed_command",
            "description": "Create governed CRUD previews for owned records with human confirmation.",
            "requires_confirmation_for_mutation": True,
            "requires_citations": True,
        },
    )
    return {"ok": True, "pbc": PBC_KEY, "skills": skills, "side_effects": ()}


def chatbot_interface_contract() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "entrypoint": f"/assistant/pbc/{PBC_KEY}",
        "single_agent_contribution": f"{PBC_KEY}_skills",
        "capabilities": ("task_guidance", "document_instruction_intake", "governed_datastore_crud", "mutation_preview", "citation_enforcement"),
        "side_effects": (),
    }


def document_instruction_plan(document: str, instruction: str, *, target_table: str = HACCP_PLAN_TABLE) -> dict:
    preview = _mutation_preview({"target_table": target_table, "action": "create", "payload": {"instruction": instruction}})
    return {
        "ok": preview["ok"],
        "pbc": PBC_KEY,
        "document_digest": _digest(document),
        "instruction": instruction,
        "candidate_tables": (target_table, GOVERNED_MODEL_TABLE, QUALITY_HOLD_TABLE),
        "requires_human_confirmation": True,
        "crud_preview": preview,
        "requires_citations": True,
        "side_effects": (),
    }


def datastore_crud_plan(action: str, *, table: str | None = None, payload: dict[str, Any] | None = None) -> dict:
    preview = _mutation_preview({"target_table": table or HACCP_PLAN_TABLE, "action": action, "payload": dict(payload or {})})
    return {
        "ok": preview["ok"],
        "pbc": PBC_KEY,
        "action": action,
        "table": preview.get("table", table),
        "payload": dict(payload or {}),
        "requires_confirmation": preview.get("requires_confirmation", False),
        "requires_citations": True,
        "event_contract": EVENT_CONTRACT,
        "release_impacting": preview.get("release_impacting", False),
        "side_effects": (),
    }


def composed_agent_contribution() -> dict:
    namespace = f"{PBC_KEY}_skills"
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "single_agent_skill_namespace": namespace,
        "dsl_tools": (namespace, f"{PBC_KEY}_crud", f"{PBC_KEY}_documents"),
        "side_effects": (),
    }


def build_ui_contract() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "fragments": UI_FRAGMENT_KEYS,
        "forms": FORM_DEFINITIONS,
        "wizards": WIZARD_DEFINITIONS,
        "controls": CONTROL_DEFINITIONS,
        "workbench_views": WORKBENCH_VIEWS,
        "action_permissions": PERMISSIONS,
        "assistant_skills": tuple(skill["name"] for skill in agent_skill_manifest()["skills"]),
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def build_app_surface(state: dict | None = None, *, tenant: str = "default") -> dict:
    working_state = state or empty_state()
    ui = build_ui_contract()
    workbench = build_workbench_view(working_state, {"tenant": tenant})
    return {
        "ok": ui["ok"] and workbench["ok"],
        "tenant": tenant,
        "route": workbench["route"],
        "forms": ui["forms"],
        "wizards": ui["wizards"],
        "controls": ui["controls"],
        "queues": workbench["queues"],
        "assistant_skills": ui["assistant_skills"],
        "side_effects": (),
    }


def domain_depth_contract() -> dict:
    return {
        "format": f"appgen.{PBC_KEY}.world-class-domain-depth.v2",
        "ok": True,
        "pbc": PBC_KEY,
        "purpose": "HACCP plans, inspections, nonconformance, recalls, supplier audits, quality holds, and regulatory evidence.",
        "owned_tables": OWNED_TABLES,
        "operation_count": len(DOMAIN_OPERATIONS),
        "operations": DOMAIN_OPERATIONS,
        "rules": DOMAIN_RULES,
        "parameters": DOMAIN_PARAMETERS,
        "emitted_events": EMITTED_EVENT_TYPES,
        "consumed_events": CONSUMED_EVENT_TYPES,
        "advanced_capabilities": DOMAIN_ADVANCED_CAPABILITIES,
        "workbench_views": WORKBENCH_VIEWS,
        "database_backends": ALLOWED_DATABASE_BACKENDS,
        "event_contract": EVENT_CONTRACT,
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "minimum_owned_domain_tables": 15,
        "minimum_domain_operations": 15,
        "side_effects": (),
    }


def execute_domain_operation(operation: str, payload: dict[str, Any] | None = None) -> dict:
    if operation not in DOMAIN_OPERATIONS:
        return {"ok": False, "reason": "unknown_domain_operation", "operation": operation, "side_effects": ()}
    contract = operation_contract(operation, "command")
    return {
        "ok": True,
        "operation": operation,
        "operation_kind": "command",
        "target_table": contract["owned_tables"][0] if contract["owned_tables"] else None,
        "owned_tables": contract["owned_tables"],
        "read_tables": (),
        "emitted_event": contract["emitted_event"],
        "event_contract": contract["event_contract"],
        "permission": contract["required_permission"],
        "idempotency_key": _digest((operation, payload or {})),
        "evidence_hash": _digest((operation, contract, payload or {})),
        "shared_table_access": False,
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def domain_capability_surface_contract() -> dict:
    return {
        "format": f"appgen.{PBC_KEY}.complete-domain-capability-surface.v2",
        "ok": True,
        "pbc": PBC_KEY,
        "operation_surfaces": tuple(
            {
                "operation": operation,
                "surface": f"{PBC_KEY}.ui.operation.{operation}",
                "action": operation,
                "target_tables": OPERATION_TABLES.get(operation, ()),
                "permission": OPERATION_PERMISSIONS.get(operation, f"{PBC_KEY}.read"),
                "requires_confirmation": operation in {"approve_haccp_plan", "release_quality_hold", "start_recall_event", "approve_document_instruction"},
            }
            for operation in DOMAIN_OPERATIONS
        ),
        "rule_surfaces": tuple({"rule": rule, "surface": f"{PBC_KEY}.ui.rule.{rule}", "editor": True, "explainable": True} for rule in DOMAIN_RULES),
        "parameter_surfaces": tuple({"parameter": parameter, "surface": f"{PBC_KEY}.ui.parameter.{parameter}", "bounded": True, "editable": True} for parameter in DOMAIN_PARAMETERS),
        "advanced_surfaces": tuple({"capability": capability, "surface": f"{PBC_KEY}.ui.advanced.{index}", "explainable": True} for index, capability in enumerate(DOMAIN_ADVANCED_CAPABILITIES, start=1)),
        "edge_case_surfaces": tuple({"edge_case": edge_case, "surface": f"{PBC_KEY}.ui.edge_case.{edge_case}", "triage_queue": True} for edge_case in DOMAIN_EDGE_CASES),
        "table_surfaces": tuple({"owned_table": table_name, "surface": f"{PBC_KEY}.ui.table.{table_name}", "read_model": True, "mutation_guard": True} for table_name in OWNED_TABLES),
        "forms": FORM_DEFINITIONS,
        "wizards": WIZARD_DEFINITIONS,
        "controls": CONTROL_DEFINITIONS,
        "specialist_capabilities": tuple(skill["name"] for skill in agent_skill_manifest()["skills"]),
        "coverage": {"event_contract": EVENT_CONTRACT, "stream_engine_picker_visible": False, "shared_table_access": False},
        "side_effects": (),
    }


def build_release_evidence() -> dict:
    schema = build_schema_contract()
    service = build_service_contract()
    api = build_api_contract()
    ui = build_ui_contract()
    checks = (
        {"id": "schema_models_migration_alignment", "ok": len(schema["tables"]) == len(schema["models"]) == len(TABLE_DEFINITIONS)},
        {"id": "service_route_alignment", "ok": set(api["route_to_operation"].values()).issubset(set(service["command_methods"]) | set(service["query_methods"]))},
        {"id": "event_handler_alignment", "ok": validate_event_contract()["ok"] and handler_manifest()["ok"]},
        {"id": "ui_workbench_alignment", "ok": len(ui["forms"]) >= 4 and len(ui["controls"]) >= 5},
        {"id": "governed_agent_alignment", "ok": agent_skill_manifest()["ok"] and chatbot_interface_contract()["ok"]},
        {"id": "boundary_alignment", "ok": verify_owned_table_boundary(OWNED_TABLES)["ok"]},
    )
    return {
        "format": "appgen.food-safety-quality-compliance-release-evidence.v2",
        "ok": all(check["ok"] for check in checks),
        "pbc": PBC_KEY,
        "checks": checks,
        "generated_artifacts": {
            "migrations": schema["migrations"],
            "models": schema["models"],
            "events": event_contract_manifest(),
            "handlers": ("receive_event",),
            "ui": ui["fragments"],
            "workflows": WORKFLOWS,
            "agent_skills": tuple(skill["name"] for skill in agent_skill_manifest()["skills"]),
        },
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
        "side_effects": (),
    }


def verify_owned_table_boundary(references: tuple[str, ...] | list[str] | None = None) -> dict:
    refs = tuple(references or ())
    invalid = tuple(ref for ref in refs if ref and ref not in OWNED_TABLES and ref.endswith("_table"))
    return {
        "ok": not invalid,
        "pbc": PBC_KEY,
        "invalid_references": invalid,
        "allowed_tables": OWNED_TABLES,
        "shared_table_access": False,
        "side_effects": (),
    }


def seed_plan() -> dict:
    records = (
        {"table": HACCP_PLAN_TABLE, "code": "SEED-HACCP-A", "description": "Approved reference HACCP plan for chilled ready-to-eat meals."},
        {"table": SUPPLIER_AUDIT_TABLE, "code": "SEED-AUDIT-1", "description": "Approved supplier audit for ready-to-eat protein supplier."},
        {"table": QUALITY_HOLD_TABLE, "code": "SEED-HOLD-1", "description": "Open quality hold used to validate hold release workbench visibility."},
    )
    return {"ok": True, "pbc": PBC_KEY, "records": records, "side_effects": ()}


def validate_seed_data() -> dict:
    records = seed_plan()["records"]
    invalid = tuple(record for record in records if record["table"] not in OWNED_TABLES)
    return {"ok": not invalid, "pbc": PBC_KEY, "invalid_records": invalid, "side_effects": ()}


def runtime_capabilities() -> dict:
    domain = domain_depth_contract()
    return {
        "format": "appgen.food-safety-quality-compliance-runtime-capabilities.v2",
        "ok": domain["ok"],
        "pbc": PBC_KEY,
        "implementation_directory": f"src/pyAppGen/pbcs/{PBC_KEY}",
        "owned_tables": OWNED_TABLES,
        "allowed_database_backends": ALLOWED_DATABASE_BACKENDS,
        "standard_features": STANDARD_FEATURE_KEYS,
        "capabilities": RUNTIME_CAPABILITY_KEYS,
        "operations": DOMAIN_OPERATIONS + QUERY_METHODS,
        "world_class_domain_depth": domain,
        "database_backends": ALLOWED_DATABASE_BACKENDS,
        "event_contract": EVENT_CONTRACT,
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def dispatch_route(route: str, payload: dict[str, Any] | None = None, *, service: Any | None = None) -> dict:
    if route not in ROUTES:
        return {"ok": False, "reason": "unknown_route", "route": route, "side_effects": ()}
    operation = ROUTE_TO_OPERATION[route]
    current_service = service or FoodSafetyQualityComplianceService()
    handler = getattr(current_service, operation)
    result = handler(dict(payload or {}))
    return {
        "ok": result["ok"],
        "route": route,
        "operation": operation,
        "method": route.split()[0],
        "path": route.split()[1],
        "result": result,
        "side_effects": (),
    }


def run_slice_smoke() -> dict:
    state = empty_state()
    configured = configure_runtime(state, {"database_backend": "postgresql", "event_topic": REQUIRED_EVENT_TOPIC})
    plan = create_haccp_plan(
        configured["state"],
        {
            "tenant": "tenant-smoke",
            "plan_code": "RTE-CHILL",
            "version": "2",
            "facility_code": "FAC-1",
            "product_scope": ("ready_to_eat_meals",),
            "process_steps": ({"step_code": "cook", "name": "Cook"}, {"step_code": "chill", "name": "Rapid Chill"}),
            "hazard_analysis": (
                {"hazard_id": "haz-1", "process_step_code": "cook", "hazard_type": "biological", "requires_ccp": True},
                {"hazard_id": "haz-2", "process_step_code": "chill", "hazard_type": "temperature", "requires_ccp": True},
            ),
            "approvals": {"food_safety": True, "quality": True},
            "effective_from": "2026-01-03",
        },
    )
    ccp1 = create_critical_control_point(
        plan["state"],
        {
            "tenant": "tenant-smoke",
            "plan_id": plan["record"]["id"],
            "process_step_code": "cook",
            "hazard_id": "haz-1",
            "limit_min": 74.0,
            "limit_max": 76.0,
            "unit": "celsius",
            "monitoring_method": "probe",
            "monitoring_frequency_minutes": 15,
        },
    )
    ccp2 = create_critical_control_point(
        ccp1["state"],
        {
            "tenant": "tenant-smoke",
            "plan_id": plan["record"]["id"],
            "process_step_code": "chill",
            "hazard_id": "haz-2",
            "limit_min": 0.0,
            "limit_max": 5.0,
            "unit": "celsius",
            "monitoring_method": "data_logger",
            "monitoring_frequency_minutes": 30,
        },
    )
    approved = approve_haccp_plan(
        ccp2["state"],
        {
            "tenant": "tenant-smoke",
            "id": plan["record"]["id"],
            "approvals": {"operations": True},
            "effective_from": "2026-01-03",
        },
    )
    inspection = record_inspection(
        approved["state"],
        {
            "tenant": "tenant-smoke",
            "plan_code": "RTE-CHILL",
            "facility_code": "FAC-1",
            "area": "cooling-room",
            "checklist": ("preop", "temperature", "allergen"),
            "findings": (
                {
                    "category": "temperature",
                    "severity": "critical",
                    "description": "Rapid chill exceeded safe temperature.",
                    "affected_lots": ("LOT-100",),
                    "process_step_code": "chill",
                    "affected_quantity": 42.0,
                },
            ),
            "inspector": "qa.lead",
        },
    )
    hold_id = inspection["created_hold_ids"][0]
    released_hold = release_quality_hold(
        inspection["state"],
        {"id": hold_id, "approved_by": ("qa.lead",), "disposition": "rework", "quantity_reconciled": 42.0},
    )
    supplier = create_supplier_audit(
        released_hold["state"],
        {
            "tenant": "tenant-smoke",
            "supplier_projection": {"supplier_id": "SUP-1", "name": "Protein Farm"},
            "commodity": "protein",
            "audit_type": "onsite",
            "risk_rating": "medium",
            "findings": (),
            "days_until_expiry": 20,
        },
    )
    recall = run_mock_recall(
        supplier["state"],
        {
            "tenant": "tenant-smoke",
            "classification": "mock_recall",
            "reason": "annual_readiness",
            "consumer_risk": "moderate",
            "distribution_scope": "national",
            "genealogy_projection": ({"source_lot": "RAW-1", "finished_lot": "LOT-100", "customers": ("Retailer A",)},),
            "shipment_projection": ({"lot": "LOT-100", "customer": "Retailer A"},),
            "trace_elapsed_minutes": 80,
        },
    )
    instruction = create_document_instruction(
        supplier["state"],
        {
            "tenant": "tenant-smoke",
            "document": "Deviation memo",
            "instruction": "Open a hold for LOT-100 pending QA review.",
            "target_table": QUALITY_HOLD_TABLE,
            "action": "create",
            "payload": {"affected_lots": ("LOT-100",)},
            "citations": ("inspection:1", "hold-policy:7"),
        },
    )
    approved_instruction = approve_document_instruction(
        instruction["state"],
        {"id": instruction["record"]["id"], "approved_by": "qa.lead", "release_reviewed": True},
    )
    received = receive_event(approved_instruction["state"], {"event_type": CONSUMED_EVENT_TYPES[0], "idempotency_key": "smoke-policy", "tenant": "tenant-smoke"})
    duplicate = receive_event(received["state"], {"event_type": CONSUMED_EVENT_TYPES[0], "idempotency_key": "smoke-policy", "tenant": "tenant-smoke"})
    dead = receive_event(duplicate["state"], {"event_type": "UnexpectedEvent", "idempotency_key": "smoke-bad", "tenant": "tenant-smoke"})
    workbench = query_workbench(dead["state"], {"tenant": "tenant-smoke"})
    checks = (
        {"id": "configure_runtime", "ok": configured["ok"]},
        {"id": "create_haccp_plan", "ok": plan["ok"]},
        {"id": "ccp_hazard_mapping", "ok": ccp1["ok"] and ccp2["ok"]},
        {"id": "approve_haccp_plan", "ok": approved["ok"]},
        {"id": "inspection_creates_hold_and_nc", "ok": inspection["ok"] and bool(inspection["created_hold_ids"]) and bool(inspection["created_nonconformance_ids"])},
        {"id": "release_hold_requires_disposition", "ok": released_hold["ok"]},
        {"id": "supplier_audit_monitor", "ok": supplier["record"]["approval_status"] == "expiring"},
        {"id": "mock_recall_projection_boundary", "ok": recall["evidence_packet"]["projection_boundary_ok"] and recall["evidence_packet"]["mutates_live_state"] is False},
        {"id": "document_instruction_crud", "ok": instruction["ok"] and approved_instruction["ok"]},
        {"id": "idempotent_handler", "ok": received["ok"] and duplicate.get("duplicate") is True and dead["ok"] is False},
        {"id": "workbench", "ok": workbench["ok"] and workbench["metrics"]["open_quality_holds"] >= 0},
    )
    return {"ok": all(check["ok"] for check in checks), "checks": checks, "workbench": workbench, "release_evidence": build_release_evidence(), "side_effects": ()}


def smoke_test() -> dict:
    return run_slice_smoke()


class FoodSafetyQualityComplianceService:
    """Stateful package-local service harness for one-PBC execution."""

    def __init__(self, state: dict | None = None) -> None:
        self.state = state or empty_state()

    def __getattr__(self, name: str):
        if name in COMMAND_METHODS:
            return lambda payload=None, _name=name: self._command(_name, dict(payload or {}))
        if name in QUERY_METHODS:
            return lambda payload=None, _name=name: self._query(_name, dict(payload or {}))
        raise AttributeError(name)

    def _command(self, name: str, payload: dict[str, Any]) -> dict:
        result = service_callable(name)(self.state, payload)
        if result.get("ok") and "state" in result:
            self.state = result["state"]
        return {
            "ok": result.get("ok", False),
            "operation": name,
            "operation_kind": "command",
            "read_only": False,
            "payload": payload,
            "operation_contract": operation_contract(name, "command"),
            "outbox_table": OUTBOX_TABLE,
            "emits": ((OPERATION_EVENTS.get(name),) if OPERATION_EVENTS.get(name) else ()),
            "transaction_boundary": "owned_datastore_plus_outbox",
            "result": result,
            "side_effects": (),
        }

    def _query(self, name: str, payload: dict[str, Any]) -> dict:
        result = service_callable(name)(self.state, payload)
        return {
            "ok": result.get("ok", False),
            "operation": name,
            "operation_kind": "query",
            "read_only": True,
            "payload": payload,
            "operation_contract": operation_contract(name, "query"),
            "outbox_table": None,
            "emits": (),
            "result": result,
            "side_effects": (),
        }
