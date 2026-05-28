"""Typed owned-model contracts for the cybersecurity_operations_center PBC."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any
import hashlib

PBC_KEY = "cybersecurity_operations_center"
APPGEN_EVENT_CONTRACT = "AppGen-X"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def stable_digest(*parts: Any) -> str:
    return hashlib.sha256(repr(parts).encode("utf-8")).hexdigest()


ALERT_STATES = (
    "new",
    "deduplicated",
    "enriched",
    "triaged",
    "escalated",
    "suppressed",
    "contained",
    "closed",
    "reopened",
)

ALERT_TRANSITIONS = {
    "new": {"deduplicated", "enriched", "triaged", "suppressed", "closed"},
    "deduplicated": {"enriched", "triaged", "suppressed", "closed", "reopened"},
    "enriched": {"triaged", "escalated", "suppressed", "closed"},
    "triaged": {"escalated", "suppressed", "contained", "closed"},
    "escalated": {"contained", "suppressed", "closed"},
    "suppressed": {"reopened", "closed"},
    "contained": {"closed", "reopened"},
    "closed": {"reopened"},
    "reopened": {"enriched", "triaged", "escalated", "suppressed", "closed"},
}

PLAYBOOK_STAGES = (
    "preconditions",
    "evidence_collection",
    "analyst_approval",
    "containment",
    "validation",
    "communications",
    "closure_verification",
)

HIGH_RISK_CONTAINMENT_ACTIONS = {
    "host_isolation": "supervisor_approval",
    "user_lockout": "supervisor_approval",
    "credential_disablement": "supervisor_approval",
    "mass_suppression": "exception_approval",
    "evidence_deletion": "exception_approval",
}

PARAMETER_BOUNDS = {
    "quality_score_floor": (0.0, 1.0),
    "materiality_threshold": (1, 100),
    "approval_sla_hours": (1, 168),
    "risk_threshold": (0.0, 1.0),
    "forecast_horizon_days": (1, 90),
    "workbench_limit": (10, 500),
}

RULE_NAMES = (
    "security_alert_policy",
    "security_incident_policy",
    "asset_exposure_policy",
    "threat_intel_policy",
    "playbook_run_policy",
    "containment_action_policy",
)

PERMISSIONS = (
    "cybersecurity_operations_center.read",
    "cybersecurity_operations_center.create",
    "cybersecurity_operations_center.update",
    "cybersecurity_operations_center.approve",
    "cybersecurity_operations_center.admin",
)


@dataclass(slots=True)
class OwnedRecord:
    id: str
    tenant: str
    code: str
    status: str
    created_at: str = field(default_factory=utc_now)
    updated_at: str = field(default_factory=utc_now)
    version: int = 1

    def to_row(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class SecurityAlert(OwnedRecord):
    severity: str = "medium"
    confidence: float = 0.5
    asset_ref: str = "unknown"
    principal_ref: str = "unknown"
    indicator_value: str = "unknown"
    blast_radius: str = "single_asset"
    assignee: str | None = None
    lane: str = "backlog"
    previous_status: str | None = None
    incident_id: str | None = None
    duplicate_of: str | None = None
    cluster_id: str | None = None
    suppression: dict[str, Any] = field(default_factory=dict)
    false_positive: dict[str, Any] = field(default_factory=dict)
    detection_context: dict[str, Any] = field(default_factory=dict)
    enrichment: dict[str, Any] = field(default_factory=dict)
    evidence_ids: list[str] = field(default_factory=list)
    lineage: list[dict[str, Any]] = field(default_factory=list)


@dataclass(slots=True)
class SecurityIncident(OwnedRecord):
    title: str = ""
    severity: str = "medium"
    explainable_score: float = 0.5
    commander: str | None = None
    communications_owner: str | None = None
    evidence_owner: str | None = None
    containment_owner: str | None = None
    promotion_summary: dict[str, Any] = field(default_factory=dict)
    alert_ids: list[str] = field(default_factory=list)
    evidence_ids: list[str] = field(default_factory=list)
    containment_action_ids: list[str] = field(default_factory=list)
    timeline: list[dict[str, Any]] = field(default_factory=list)
    closure_checklist: dict[str, bool] = field(default_factory=dict)


@dataclass(slots=True)
class AssetExposure(OwnedRecord):
    asset_ref: str = "unknown"
    criticality: str = "medium"
    internet_exposed: bool = False
    open_alert_ids: list[str] = field(default_factory=list)
    open_incident_ids: list[str] = field(default_factory=list)
    containment_action_ids: list[str] = field(default_factory=list)


@dataclass(slots=True)
class ThreatIntel(OwnedRecord):
    indicator_value: str = ""
    observed_fact: dict[str, Any] = field(default_factory=dict)
    assessed_relationship: dict[str, Any] = field(default_factory=dict)
    campaign_context: dict[str, Any] = field(default_factory=dict)
    analyst_inference: dict[str, Any] = field(default_factory=dict)
    confidence: float = 0.5
    expires_at: str | None = None
    source_provenance: str = "internal"
    recommendation_preview: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class PlaybookRun(OwnedRecord):
    template_name: str = "containment"
    stage: str = PLAYBOOK_STAGES[0]
    status: str = "draft"
    checkpoint_statuses: dict[str, str] = field(default_factory=dict)
    breakpoint_required: bool = False
    requires_human_confirmation: bool = True
    related_incident_id: str | None = None
    related_alert_id: str | None = None
    notes: list[str] = field(default_factory=list)


@dataclass(slots=True)
class ContainmentAction(OwnedRecord):
    incident_id: str | None = None
    alert_id: str | None = None
    action_type: str = "investigate"
    approval_path: str = "no_approval"
    approved_by: str | None = None
    risk_level: str = "low"
    rollback_instructions: str = ""
    outcome_summary: str = ""


@dataclass(slots=True)
class ResponseEvidence(OwnedRecord):
    case_id: str = ""
    source_system: str = ""
    checksum: str = ""
    acquired_at: str = field(default_factory=utc_now)
    storage_reference: str = ""
    redaction_status: str = "needs_review"
    admissibility_notes: str = ""
    handling_history: list[dict[str, Any]] = field(default_factory=list)
    request_status: str = "collected"
    sealed_bundle_id: str | None = None


@dataclass(slots=True)
class PolicyRule(OwnedRecord):
    rule_name: str = ""
    policy: dict[str, Any] = field(default_factory=dict)
    simulation_preview: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class RuntimeParameter(OwnedRecord):
    parameter_name: str = ""
    value: Any = None
    minimum: float | int | None = None
    maximum: float | int | None = None
    rationale: str = ""


@dataclass(slots=True)
class SchemaExtension(OwnedRecord):
    target_table: str = ""
    fields: dict[str, str] = field(default_factory=dict)


@dataclass(slots=True)
class ControlAssertion(OwnedRecord):
    control_name: str = ""
    control_status: str = "passing"
    evidence: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class GovernedModel(OwnedRecord):
    model_name: str = ""
    intended_use: str = ""
    guardrails: dict[str, Any] = field(default_factory=dict)


def _owned_table(logical_name: str) -> str:
    return f"{PBC_KEY}_{logical_name}"


MODEL_REGISTRY = (
    {
        "class_name": "SecurityAlert",
        "logical_name": "security_alert",
        "table": _owned_table("security_alert"),
        "fields": (
            "id",
            "tenant",
            "code",
            "status",
            "severity",
            "confidence",
            "asset_ref",
            "principal_ref",
            "indicator_value",
            "blast_radius",
            "lane",
            "previous_status",
            "incident_id",
            "duplicate_of",
            "cluster_id",
            "suppression",
            "false_positive",
            "detection_context",
            "enrichment",
            "evidence_ids",
            "lineage",
            "created_at",
            "updated_at",
            "version",
        ),
        "description": "Owned alert lifecycle, detection context, enrichment, correlation, and queue state.",
    },
    {
        "class_name": "SecurityIncident",
        "logical_name": "security_incident",
        "table": _owned_table("security_incident"),
        "fields": (
            "id",
            "tenant",
            "code",
            "status",
            "title",
            "severity",
            "explainable_score",
            "commander",
            "communications_owner",
            "evidence_owner",
            "containment_owner",
            "promotion_summary",
            "alert_ids",
            "evidence_ids",
            "containment_action_ids",
            "timeline",
            "closure_checklist",
            "created_at",
            "updated_at",
            "version",
        ),
        "description": "Owned major-case record with explainable severity and ownership handoffs.",
    },
    {
        "class_name": "AssetExposure",
        "logical_name": "asset_exposure",
        "table": _owned_table("asset_exposure"),
        "fields": (
            "id",
            "tenant",
            "code",
            "status",
            "asset_ref",
            "criticality",
            "internet_exposed",
            "open_alert_ids",
            "open_incident_ids",
            "containment_action_ids",
            "created_at",
            "updated_at",
            "version",
        ),
        "description": "Owned asset exposure posture with case linkage.",
    },
    {
        "class_name": "ThreatIntel",
        "logical_name": "threat_intel",
        "table": _owned_table("threat_intel"),
        "fields": (
            "id",
            "tenant",
            "code",
            "status",
            "indicator_value",
            "observed_fact",
            "assessed_relationship",
            "campaign_context",
            "analyst_inference",
            "confidence",
            "expires_at",
            "source_provenance",
            "recommendation_preview",
            "created_at",
            "updated_at",
            "version",
        ),
        "description": "Owned intelligence record with provenance partitions and expiry.",
    },
    {
        "class_name": "PlaybookRun",
        "logical_name": "playbook_run",
        "table": _owned_table("playbook_run"),
        "fields": (
            "id",
            "tenant",
            "code",
            "status",
            "template_name",
            "stage",
            "checkpoint_statuses",
            "breakpoint_required",
            "requires_human_confirmation",
            "related_incident_id",
            "related_alert_id",
            "notes",
            "created_at",
            "updated_at",
            "version",
        ),
        "description": "Owned staged playbook execution with human breakpoints.",
    },
    {
        "class_name": "ContainmentAction",
        "logical_name": "containment_action",
        "table": _owned_table("containment_action"),
        "fields": (
            "id",
            "tenant",
            "code",
            "status",
            "incident_id",
            "alert_id",
            "action_type",
            "approval_path",
            "approved_by",
            "risk_level",
            "rollback_instructions",
            "outcome_summary",
            "created_at",
            "updated_at",
            "version",
        ),
        "description": "Owned containment request with approval boundaries and rollback guidance.",
    },
    {
        "class_name": "ResponseEvidence",
        "logical_name": "response_evidence",
        "table": _owned_table("response_evidence"),
        "fields": (
            "id",
            "tenant",
            "code",
            "status",
            "case_id",
            "source_system",
            "checksum",
            "acquired_at",
            "storage_reference",
            "redaction_status",
            "admissibility_notes",
            "handling_history",
            "request_status",
            "sealed_bundle_id",
            "created_at",
            "updated_at",
            "version",
        ),
        "description": "Owned evidence custody record with review and sealing state.",
    },
    {
        "class_name": "PolicyRule",
        "logical_name": "cybersecurity_operations_center_policy_rule",
        "table": _owned_table("cybersecurity_operations_center_policy_rule"),
        "fields": (
            "id",
            "tenant",
            "code",
            "status",
            "rule_name",
            "policy",
            "simulation_preview",
            "created_at",
            "updated_at",
            "version",
        ),
        "description": "Owned policy rule configuration and simulation preview state.",
    },
    {
        "class_name": "RuntimeParameter",
        "logical_name": "cybersecurity_operations_center_runtime_parameter",
        "table": _owned_table("cybersecurity_operations_center_runtime_parameter"),
        "fields": (
            "id",
            "tenant",
            "code",
            "status",
            "parameter_name",
            "value",
            "minimum",
            "maximum",
            "rationale",
            "created_at",
            "updated_at",
            "version",
        ),
        "description": "Owned bounded runtime parameter with rationale.",
    },
    {
        "class_name": "SchemaExtension",
        "logical_name": "cybersecurity_operations_center_schema_extension",
        "table": _owned_table("cybersecurity_operations_center_schema_extension"),
        "fields": (
            "id",
            "tenant",
            "code",
            "status",
            "target_table",
            "fields",
            "created_at",
            "updated_at",
            "version",
        ),
        "description": "Owned schema evolution request scoped to the PBC.",
    },
    {
        "class_name": "ControlAssertion",
        "logical_name": "cybersecurity_operations_center_control_assertion",
        "table": _owned_table("cybersecurity_operations_center_control_assertion"),
        "fields": (
            "id",
            "tenant",
            "code",
            "status",
            "control_name",
            "control_status",
            "evidence",
            "created_at",
            "updated_at",
            "version",
        ),
        "description": "Owned control-test projection and exception evidence.",
    },
    {
        "class_name": "GovernedModel",
        "logical_name": "cybersecurity_operations_center_governed_model",
        "table": _owned_table("cybersecurity_operations_center_governed_model"),
        "fields": (
            "id",
            "tenant",
            "code",
            "status",
            "model_name",
            "intended_use",
            "guardrails",
            "created_at",
            "updated_at",
            "version",
        ),
        "description": "Owned registry of AI/agent models allowed inside this PBC.",
    },
)

EVENT_TABLES = (
    {
        "class_name": "AppGenOutboxEvent",
        "logical_name": "appgen_outbox_event",
        "table": _owned_table("appgen_outbox_event"),
        "fields": (
            "id",
            "tenant",
            "event_type",
            "topic",
            "aggregate_id",
            "payload",
            "idempotency_key",
            "created_at",
            "status",
        ),
        "description": "AppGen-X outbox for case-affecting changes.",
    },
    {
        "class_name": "AppGenInboxEvent",
        "logical_name": "appgen_inbox_event",
        "table": _owned_table("appgen_inbox_event"),
        "fields": (
            "id",
            "tenant",
            "event_type",
            "topic",
            "payload",
            "idempotency_key",
            "created_at",
            "status",
        ),
        "description": "AppGen-X inbox for consumed upstream events.",
    },
    {
        "class_name": "AppGenDeadLetterEvent",
        "logical_name": "appgen_dead_letter_event",
        "table": _owned_table("appgen_dead_letter_event"),
        "fields": (
            "id",
            "tenant",
            "event_type",
            "topic",
            "payload",
            "idempotency_key",
            "created_at",
            "status",
            "failure_reason",
            "retry_policy",
        ),
        "description": "AppGen-X dead-letter queue for bounded recovery.",
    },
)

TABLE_SCHEMAS = tuple(MODEL_REGISTRY + EVENT_TABLES)
OWNED_TABLES = tuple(item["table"] for item in TABLE_SCHEMAS)
BUSINESS_TABLES = tuple(item["table"] for item in MODEL_REGISTRY)


def table_schema_map() -> dict[str, dict[str, Any]]:
    return {item["table"]: dict(item) for item in TABLE_SCHEMAS}


def model_contracts() -> tuple[dict[str, Any], ...]:
    return tuple(dict(item) for item in TABLE_SCHEMAS)


def table_sql_definitions() -> tuple[dict[str, Any], ...]:
    definitions = []
    for item in TABLE_SCHEMAS:
        columns = []
        for field_name in item["fields"]:
            if field_name == "id":
                columns.append("id TEXT PRIMARY KEY")
            elif field_name.endswith("_at"):
                columns.append(f"{field_name} TEXT")
            elif field_name in {"version"}:
                columns.append(f"{field_name} INTEGER")
            elif field_name in {"confidence", "explainable_score"}:
                columns.append(f"{field_name} REAL")
            elif field_name in {"internet_exposed", "breakpoint_required", "requires_human_confirmation"}:
                columns.append(f"{field_name} BOOLEAN")
            elif field_name in {"policy", "simulation_preview", "payload", "guardrails", "fields", "closure_checklist", "timeline", "promotion_summary", "evidence", "checkpoint_statuses", "handling_history", "recommendation_preview", "lineage", "enrichment", "suppression", "false_positive", "detection_context", "observed_fact", "assessed_relationship", "campaign_context", "analyst_inference", "retry_policy"}:
                columns.append(f"{field_name} JSON")
            elif field_name.endswith("_ids"):
                columns.append(f"{field_name} JSON")
            else:
                columns.append(f"{field_name} TEXT")
        definitions.append(
            {
                "table": item["table"],
                "sql": f"CREATE TABLE {item['table']} ({', '.join(columns)});",
                "fields": item["fields"],
            }
        )
    return tuple(definitions)


def default_policy_bundle() -> dict[str, Any]:
    return {
        "dedup_window_hours": 12,
        "promotion_cluster_threshold": 2,
        "high_severity_requires_incident": True,
        "suppression_review_days": 14,
        "redaction_required_statuses": ("needs_review", "pending_release"),
        "stale_alert_hours": 4,
    }


def default_parameter_records() -> tuple[dict[str, Any], ...]:
    defaults = {
        "quality_score_floor": 0.7,
        "materiality_threshold": 65,
        "approval_sla_hours": 8,
        "risk_threshold": 0.75,
        "forecast_horizon_days": 7,
        "workbench_limit": 50,
    }
    records = []
    for name, value in defaults.items():
        minimum, maximum = PARAMETER_BOUNDS[name]
        records.append(
            RuntimeParameter(
                id=f"param-{name}",
                tenant="default",
                code=name.upper(),
                status="active",
                parameter_name=name,
                value=value,
                minimum=minimum,
                maximum=maximum,
                rationale="Package default",
            ).to_row()
        )
    return tuple(records)
