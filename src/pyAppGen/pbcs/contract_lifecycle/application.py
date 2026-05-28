"""Executable package-local contract lifecycle application model."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timedelta, timezone
import hashlib

PBC_KEY = "contract_lifecycle"

ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
REQUIRED_EVENT_TOPIC = "pbc.contract_lifecycle.events"

PUBLIC_UI_FRAGMENTS = (
    "ContractLifecycleWorkbench",
    "ContractLifecycleDetail",
    "ContractLifecycleAssistantPanel",
)

PERMISSIONS = (
    "contract_lifecycle.read",
    "contract_lifecycle.create",
    "contract_lifecycle.update",
    "contract_lifecycle.approve",
    "contract_lifecycle.admin",
)

RBAC_ROLE_PERMISSIONS = {
    "reader": ("contract_lifecycle.read",),
    "intake_specialist": (
        "contract_lifecycle.read",
        "contract_lifecycle.create",
        "contract_lifecycle.update",
    ),
    "legal_analyst": (
        "contract_lifecycle.read",
        "contract_lifecycle.create",
        "contract_lifecycle.update",
    ),
    "approver": ("contract_lifecycle.read", "contract_lifecycle.approve"),
    "admin": PERMISSIONS,
}

ADVANCED_CAPABILITIES = (
    "semantic_clause_extraction",
    "counterfactual_obligation_impact_simulation",
    "cryptographic_signature_and_document_proof",
    "continuous_obligation_control_testing",
    "risk_aware_renewal_recommendation",
    "multi_tenant_legal_policy_isolation",
)

WORKBENCH_VIEWS = (
    "command_center",
    "intake_queue",
    "authoring_workspace",
    "negotiation_board",
    "approval_queue",
    "signature_console",
    "obligation_command_center",
    "renewal_calendar",
    "risk_and_compliance",
    "exceptions_and_events",
    "agent_assistant",
    "release_evidence",
)

FORMS = (
    {
        "id": "contract_intake_form",
        "title": "Contract Intake",
        "fields": (
            "request_purpose",
            "contract_type",
            "jurisdiction",
            "counterparty_name",
            "value_amount",
            "currency",
            "term_months",
            "owner",
            "source_documents",
        ),
        "submit_operation": "intake_contract",
    },
    {
        "id": "classification_form",
        "title": "Contract Classification",
        "fields": (
            "contract_id",
            "taxonomy_version",
            "category",
            "data_sensitivity",
            "controlling_language",
        ),
        "submit_operation": "classify_contract",
    },
    {
        "id": "clause_selection_form",
        "title": "Clause Selection",
        "fields": (
            "contract_id",
            "clause_family",
            "variant_code",
            "fallback_tier",
            "risk_category",
        ),
        "submit_operation": "select_clause",
    },
    {
        "id": "approval_route_form",
        "title": "Approval Route",
        "fields": (
            "contract_id",
            "approvals",
            "risk_score",
            "value_amount",
            "requires_security_review",
        ),
        "submit_operation": "route_approval",
    },
    {
        "id": "signature_packet_form",
        "title": "Signature Packet",
        "fields": (
            "contract_id",
            "signer_name",
            "signer_title",
            "authority_evidence",
            "identity_verified",
        ),
        "submit_operation": "capture_signature",
    },
    {
        "id": "obligation_activation_form",
        "title": "Obligation Activation",
        "fields": (
            "contract_id",
            "obligation_code",
            "owner",
            "due_date",
            "evidence_required",
        ),
        "submit_operation": "activate_obligation",
    },
    {
        "id": "renewal_planning_form",
        "title": "Renewal Planning",
        "fields": (
            "contract_id",
            "renewal_decision",
            "notice_days",
            "owner",
            "reason",
        ),
        "submit_operation": "schedule_renewal",
    },
)

WIZARDS = (
    {
        "id": "intake_readiness_wizard",
        "title": "Intake Readiness Wizard",
        "steps": ("request", "counterparty", "documents", "commercials", "risk"),
        "terminal_operation": "intake_contract",
    },
    {
        "id": "negotiation_wizard",
        "title": "Negotiation and Approval Wizard",
        "steps": ("authoring", "clauses", "redlines", "approvals", "signature"),
        "terminal_operation": "capture_signature",
    },
    {
        "id": "renewal_amendment_wizard",
        "title": "Renewal and Amendment Wizard",
        "steps": ("performance", "value_snapshot", "renewal_options", "amendment"),
        "terminal_operation": "execute_amendment",
    },
)

CONTROLS = (
    {
        "id": "readiness_gate",
        "title": "Intake Readiness Gate",
        "protects": "intake_contract",
        "type": "checklist",
    },
    {
        "id": "authority_verification",
        "title": "Signer Authority Verification",
        "protects": "capture_signature",
        "type": "evidence_check",
    },
    {
        "id": "approval_matrix",
        "title": "Approval Matrix",
        "protects": "route_approval",
        "type": "decision_table",
    },
    {
        "id": "obligation_evidence_guard",
        "title": "Obligation Evidence Guard",
        "protects": "record_obligation_performance",
        "type": "evidence_check",
    },
    {
        "id": "dead_letter_replay_console",
        "title": "Dead Letter Replay Console",
        "protects": "dispatch_event",
        "type": "ops_control",
    },
)

RULE_DEFINITIONS = (
    {
        "rule_id": "clause_fallback_policy",
        "scope": "clause",
        "description": "Only approved fallback tiers may be used for negotiated clauses.",
    },
    {
        "rule_id": "approval_threshold_policy",
        "scope": "approval",
        "description": "Value, risk, and security flags determine the required approvers.",
    },
    {
        "rule_id": "renewal_notice_policy",
        "scope": "renewal",
        "description": "Renewals must preserve earliest and latest notice windows.",
    },
    {
        "rule_id": "signatory_authority_policy",
        "scope": "signature",
        "description": "Contracts may only be signed by verified signatories with authority evidence.",
    },
    {
        "rule_id": "counterparty_risk_policy",
        "scope": "risk",
        "description": "Counterparty risk must influence review thresholds and fallback language.",
    },
    {
        "rule_id": "obligation_breach_policy",
        "scope": "obligation",
        "description": "Overdue obligations create exceptions and elevated renewal scrutiny.",
    },
)

PARAMETER_DEFINITIONS = (
    {"key": "default_notice_days", "scope": "renewal", "default": 45, "min": 5, "max": 180},
    {"key": "approval_value_limit", "scope": "approval", "default": 250000, "min": 1000, "max": 5000000},
    {"key": "risk_review_threshold", "scope": "risk", "default": 0.55, "min": 0.1, "max": 1.0},
    {"key": "redline_materiality_score", "scope": "negotiation", "default": 0.35, "min": 0.0, "max": 1.0},
    {"key": "obligation_sla_hours", "scope": "obligation", "default": 72, "min": 1, "max": 720},
    {"key": "workbench_limit", "scope": "ui", "default": 25, "min": 5, "max": 100},
)

CONFIGURATION_SCHEMA = (
    {"key": "database_backend", "required": True, "allowed": ALLOWED_DATABASE_BACKENDS},
    {"key": "event_topic", "required": True, "allowed": (REQUIRED_EVENT_TOPIC,)},
    {"key": "retry_limit", "required": True, "allowed_range": (1, 10)},
    {"key": "default_policy", "required": True, "allowed": tuple(item["rule_id"] for item in RULE_DEFINITIONS)},
    {"key": "agent_write_requires_confirmation", "required": True, "allowed": (True,)},
)

EMITTED_EVENTS = (
    "ContractIntaked",
    "ClauseSelected",
    "ContractApproved",
    "ContractSigned",
    "ObligationActivated",
    "RenewalScheduled",
    "ContractRiskChanged",
)

LEGACY_PUBLIC_EVENTS = (
    "ContractAuthored",
    "ObligationActivated",
    "ContractApproved",
    "RenewalScheduled",
)

CONSUMED_EVENTS = (
    "CustomerUpdated",
    "SupplierQualified",
    "PolicyChanged",
    "IdentityVerified",
)

LIFECYCLE_STATES = (
    "draft",
    "intake_ready",
    "authoring",
    "negotiation",
    "approval_pending",
    "approved",
    "active",
    "renewal_pending",
    "amended",
    "exception",
    "expired",
    "terminated",
    "archived",
)

LIFECYCLE_TRANSITIONS = {
    "draft": {"intake_ready", "exception"},
    "intake_ready": {"authoring", "exception"},
    "authoring": {"negotiation", "approval_pending", "exception"},
    "negotiation": {"authoring", "approval_pending", "exception"},
    "approval_pending": {"approved", "negotiation", "exception"},
    "approved": {"active", "renewal_pending", "amended", "exception"},
    "active": {"renewal_pending", "amended", "expired", "terminated", "exception"},
    "renewal_pending": {"active", "expired", "terminated", "exception"},
    "amended": {"active", "renewal_pending", "exception"},
    "exception": {"authoring", "approval_pending", "terminated"},
    "expired": {"archived"},
    "terminated": {"archived"},
    "archived": set(),
}


def _business_fields(extra_fields=(), references=()):
    fields = [
        {"name": "id", "type": "string", "primary_key": True, "nullable": False},
        {"name": "tenant", "type": "string", "required": True},
        {"name": "code", "type": "string", "required": True, "searchable": True},
        {"name": "status", "type": "string", "required": True, "default": "draft"},
        {"name": "version", "type": "integer", "required": True, "default": 1},
    ]
    for field_name in references:
        fields.append(
            {
                "name": field_name,
                "type": "string",
                "required": True,
                "references": "contract_lifecycle_contract_record.id",
            }
        )
    fields.extend(extra_fields)
    fields.extend(
        (
            {"name": "payload", "type": "json", "required": False},
            {"name": "created_at", "type": "datetime", "required": True},
            {"name": "updated_at", "type": "datetime", "required": True},
        )
    )
    return tuple(fields)


TABLE_SPECS = (
    {
        "logical_table": "contract_record",
        "owned_table": "contract_lifecycle_contract_record",
        "label": "Contract Record",
        "fields": _business_fields(
            extra_fields=(
                {"name": "contract_type", "type": "string", "required": False},
                {"name": "jurisdiction", "type": "string", "required": False},
                {"name": "value_amount", "type": "decimal", "required": False},
                {"name": "currency", "type": "string", "required": False},
                {"name": "counterparty_name", "type": "string", "required": False},
                {"name": "effective_date", "type": "date", "required": False},
            )
        ),
        "relationships": (),
    },
    {
        "logical_table": "contract_party",
        "owned_table": "contract_lifecycle_contract_party",
        "label": "Contract Party",
        "fields": _business_fields(
            extra_fields=(
                {"name": "role", "type": "string", "required": True},
                {"name": "legal_name", "type": "string", "required": True},
                {"name": "authority_state", "type": "string", "required": False},
            ),
            references=("contract_id",),
        ),
        "relationships": (
            {
                "field": "contract_id",
                "target_table": "contract_lifecycle_contract_record",
                "target_column": "id",
                "cardinality": "many-to-one",
                "ownership": "same_pbc",
            },
        ),
    },
    {
        "logical_table": "clause_library",
        "owned_table": "contract_lifecycle_clause_library",
        "label": "Clause Library Entry",
        "fields": _business_fields(
            extra_fields=(
                {"name": "clause_family", "type": "string", "required": True},
                {"name": "variant_code", "type": "string", "required": True},
                {"name": "fallback_tier", "type": "string", "required": False},
            ),
            references=("contract_id",),
        ),
        "relationships": (
            {
                "field": "contract_id",
                "target_table": "contract_lifecycle_contract_record",
                "target_column": "id",
                "cardinality": "many-to-one",
                "ownership": "same_pbc",
            },
        ),
    },
    {
        "logical_table": "clause_variant",
        "owned_table": "contract_lifecycle_clause_variant",
        "label": "Clause Variant",
        "fields": _business_fields(
            extra_fields=(
                {"name": "variant_code", "type": "string", "required": True},
                {"name": "fallback_tier", "type": "string", "required": False},
            ),
            references=("contract_id",),
        ),
        "relationships": (
            {
                "field": "contract_id",
                "target_table": "contract_lifecycle_contract_record",
                "target_column": "id",
                "cardinality": "many-to-one",
                "ownership": "same_pbc",
            },
        ),
    },
    {
        "logical_table": "contract_document_packet",
        "owned_table": "contract_lifecycle_contract_document_packet",
        "label": "Document Packet",
        "fields": _business_fields(
            extra_fields=(
                {"name": "packet_type", "type": "string", "required": True},
                {"name": "document_hash", "type": "string", "required": False},
            ),
            references=("contract_id",),
        ),
        "relationships": (
            {
                "field": "contract_id",
                "target_table": "contract_lifecycle_contract_record",
                "target_column": "id",
                "cardinality": "many-to-one",
                "ownership": "same_pbc",
            },
        ),
    },
    {
        "logical_table": "contract_authoring_workspace",
        "owned_table": "contract_lifecycle_contract_authoring_workspace",
        "label": "Authoring Workspace",
        "fields": _business_fields(
            extra_fields=(
                {"name": "template_code", "type": "string", "required": True},
                {"name": "workspace_owner", "type": "string", "required": True},
            ),
            references=("contract_id",),
        ),
        "relationships": (
            {
                "field": "contract_id",
                "target_table": "contract_lifecycle_contract_record",
                "target_column": "id",
                "cardinality": "many-to-one",
                "ownership": "same_pbc",
            },
        ),
    },
    {
        "logical_table": "contract_negotiation_round",
        "owned_table": "contract_lifecycle_contract_negotiation_round",
        "label": "Negotiation Round",
        "fields": _business_fields(
            extra_fields=(
                {"name": "sender", "type": "string", "required": True},
                {"name": "receiver", "type": "string", "required": True},
                {"name": "response_due_date", "type": "date", "required": False},
            ),
            references=("contract_id",),
        ),
        "relationships": (
            {
                "field": "contract_id",
                "target_table": "contract_lifecycle_contract_record",
                "target_column": "id",
                "cardinality": "many-to-one",
                "ownership": "same_pbc",
            },
        ),
    },
    {
        "logical_table": "contract_redline_event",
        "owned_table": "contract_lifecycle_contract_redline_event",
        "label": "Redline Event",
        "fields": _business_fields(
            extra_fields=(
                {"name": "changed_clause", "type": "string", "required": True},
                {"name": "materiality_score", "type": "decimal", "required": False},
            ),
            references=("contract_id",),
        ),
        "relationships": (
            {
                "field": "contract_id",
                "target_table": "contract_lifecycle_contract_record",
                "target_column": "id",
                "cardinality": "many-to-one",
                "ownership": "same_pbc",
            },
        ),
    },
    {
        "logical_table": "contract_approval_policy",
        "owned_table": "contract_lifecycle_contract_approval_policy",
        "label": "Approval Policy",
        "fields": _business_fields(
            extra_fields=(
                {"name": "policy_name", "type": "string", "required": True},
                {"name": "route_hash", "type": "string", "required": False},
            ),
            references=("contract_id",),
        ),
        "relationships": (
            {
                "field": "contract_id",
                "target_table": "contract_lifecycle_contract_record",
                "target_column": "id",
                "cardinality": "many-to-one",
                "ownership": "same_pbc",
            },
        ),
    },
    {
        "logical_table": "contract_approval_task",
        "owned_table": "contract_lifecycle_contract_approval_task",
        "label": "Approval Task",
        "fields": _business_fields(
            extra_fields=(
                {"name": "approver_role", "type": "string", "required": True},
                {"name": "due_date", "type": "date", "required": False},
            ),
            references=("contract_id",),
        ),
        "relationships": (
            {
                "field": "contract_id",
                "target_table": "contract_lifecycle_contract_record",
                "target_column": "id",
                "cardinality": "many-to-one",
                "ownership": "same_pbc",
            },
        ),
    },
    {
        "logical_table": "contract_signature_packet",
        "owned_table": "contract_lifecycle_contract_signature_packet",
        "label": "Signature Packet",
        "fields": _business_fields(
            extra_fields=(
                {"name": "signer_name", "type": "string", "required": True},
                {"name": "authority_state", "type": "string", "required": True},
                {"name": "document_hash", "type": "string", "required": False},
            ),
            references=("contract_id",),
        ),
        "relationships": (
            {
                "field": "contract_id",
                "target_table": "contract_lifecycle_contract_record",
                "target_column": "id",
                "cardinality": "many-to-one",
                "ownership": "same_pbc",
            },
        ),
    },
    {
        "logical_table": "contract_obligation",
        "owned_table": "contract_lifecycle_contract_obligation",
        "label": "Contract Obligation",
        "fields": _business_fields(
            extra_fields=(
                {"name": "owner", "type": "string", "required": True},
                {"name": "due_date", "type": "date", "required": True},
                {"name": "evidence_required", "type": "boolean", "required": True},
            ),
            references=("contract_id",),
        ),
        "relationships": (
            {
                "field": "contract_id",
                "target_table": "contract_lifecycle_contract_record",
                "target_column": "id",
                "cardinality": "many-to-one",
                "ownership": "same_pbc",
            },
        ),
    },
    {
        "logical_table": "obligation_performance_event",
        "owned_table": "contract_lifecycle_obligation_performance_event",
        "label": "Obligation Performance",
        "fields": _business_fields(
            extra_fields=(
                {"name": "obligation_id", "type": "string", "required": True},
                {"name": "performed_by", "type": "string", "required": True},
                {"name": "evidence_uri", "type": "string", "required": False},
            ),
            references=("contract_id",),
        ),
        "relationships": (
            {
                "field": "contract_id",
                "target_table": "contract_lifecycle_contract_record",
                "target_column": "id",
                "cardinality": "many-to-one",
                "ownership": "same_pbc",
            },
        ),
    },
    {
        "logical_table": "contract_milestone",
        "owned_table": "contract_lifecycle_contract_milestone",
        "label": "Milestone",
        "fields": _business_fields(
            extra_fields=(
                {"name": "milestone_date", "type": "date", "required": True},
                {"name": "owner", "type": "string", "required": True},
            ),
            references=("contract_id",),
        ),
        "relationships": (
            {
                "field": "contract_id",
                "target_table": "contract_lifecycle_contract_record",
                "target_column": "id",
                "cardinality": "many-to-one",
                "ownership": "same_pbc",
            },
        ),
    },
    {
        "logical_table": "contract_renewal_event",
        "owned_table": "contract_lifecycle_contract_renewal_event",
        "label": "Renewal Event",
        "fields": _business_fields(
            extra_fields=(
                {"name": "notice_date", "type": "date", "required": True},
                {"name": "renewal_decision", "type": "string", "required": True},
            ),
            references=("contract_id",),
        ),
        "relationships": (
            {
                "field": "contract_id",
                "target_table": "contract_lifecycle_contract_record",
                "target_column": "id",
                "cardinality": "many-to-one",
                "ownership": "same_pbc",
            },
        ),
    },
    {
        "logical_table": "contract_amendment",
        "owned_table": "contract_lifecycle_contract_amendment",
        "label": "Amendment",
        "fields": _business_fields(
            extra_fields=(
                {"name": "effective_date", "type": "date", "required": True},
                {"name": "change_summary", "type": "string", "required": True},
            ),
            references=("contract_id",),
        ),
        "relationships": (
            {
                "field": "contract_id",
                "target_table": "contract_lifecycle_contract_record",
                "target_column": "id",
                "cardinality": "many-to-one",
                "ownership": "same_pbc",
            },
        ),
    },
    {
        "logical_table": "contract_compliance_check",
        "owned_table": "contract_lifecycle_contract_compliance_check",
        "label": "Compliance Check",
        "fields": _business_fields(
            extra_fields=(
                {"name": "check_name", "type": "string", "required": True},
                {"name": "result", "type": "string", "required": True},
            ),
            references=("contract_id",),
        ),
        "relationships": (
            {
                "field": "contract_id",
                "target_table": "contract_lifecycle_contract_record",
                "target_column": "id",
                "cardinality": "many-to-one",
                "ownership": "same_pbc",
            },
        ),
    },
    {
        "logical_table": "contract_risk_assessment",
        "owned_table": "contract_lifecycle_contract_risk_assessment",
        "label": "Risk Assessment",
        "fields": _business_fields(
            extra_fields=(
                {"name": "risk_score", "type": "decimal", "required": True},
                {"name": "risk_level", "type": "string", "required": True},
            ),
            references=("contract_id",),
        ),
        "relationships": (
            {
                "field": "contract_id",
                "target_table": "contract_lifecycle_contract_record",
                "target_column": "id",
                "cardinality": "many-to-one",
                "ownership": "same_pbc",
            },
        ),
    },
    {
        "logical_table": "contract_value_snapshot",
        "owned_table": "contract_lifecycle_contract_value_snapshot",
        "label": "Value Snapshot",
        "fields": _business_fields(
            extra_fields=(
                {"name": "snapshot_amount", "type": "decimal", "required": True},
                {"name": "currency", "type": "string", "required": True},
            ),
            references=("contract_id",),
        ),
        "relationships": (
            {
                "field": "contract_id",
                "target_table": "contract_lifecycle_contract_record",
                "target_column": "id",
                "cardinality": "many-to-one",
                "ownership": "same_pbc",
            },
        ),
    },
    {
        "logical_table": "contract_search_index",
        "owned_table": "contract_lifecycle_contract_search_index",
        "label": "Search Index",
        "fields": _business_fields(
            extra_fields=(
                {"name": "index_terms", "type": "text", "required": True},
                {"name": "document_hash", "type": "string", "required": False},
            ),
            references=("contract_id",),
        ),
        "relationships": (
            {
                "field": "contract_id",
                "target_table": "contract_lifecycle_contract_record",
                "target_column": "id",
                "cardinality": "many-to-one",
                "ownership": "same_pbc",
            },
        ),
    },
    {
        "logical_table": "contract_exception_case",
        "owned_table": "contract_lifecycle_contract_exception_case",
        "label": "Exception Case",
        "fields": _business_fields(
            extra_fields=(
                {"name": "severity", "type": "string", "required": True},
                {"name": "owner", "type": "string", "required": True},
            ),
            references=("contract_id",),
        ),
        "relationships": (
            {
                "field": "contract_id",
                "target_table": "contract_lifecycle_contract_record",
                "target_column": "id",
                "cardinality": "many-to-one",
                "ownership": "same_pbc",
            },
        ),
    },
    {
        "logical_table": "contract_policy_rule",
        "owned_table": "contract_lifecycle_contract_policy_rule",
        "label": "Policy Rule",
        "fields": _business_fields(
            extra_fields=(
                {"name": "rule_name", "type": "string", "required": True},
                {"name": "compiled_hash", "type": "string", "required": True},
            ),
            references=("contract_id",),
        ),
        "relationships": (
            {
                "field": "contract_id",
                "target_table": "contract_lifecycle_contract_record",
                "target_column": "id",
                "cardinality": "many-to-one",
                "ownership": "same_pbc",
            },
        ),
    },
    {
        "logical_table": "contract_runtime_parameter",
        "owned_table": "contract_lifecycle_contract_runtime_parameter",
        "label": "Runtime Parameter",
        "fields": _business_fields(
            extra_fields=(
                {"name": "parameter_name", "type": "string", "required": True},
                {"name": "parameter_value", "type": "string", "required": True},
            )
        ),
        "relationships": (),
    },
    {
        "logical_table": "contract_schema_extension",
        "owned_table": "contract_lifecycle_contract_schema_extension",
        "label": "Schema Extension",
        "fields": _business_fields(
            extra_fields=(
                {"name": "target_table_name", "type": "string", "required": True},
                {"name": "extension_hash", "type": "string", "required": True},
            )
        ),
        "relationships": (),
    },
    {
        "logical_table": "contract_control_assertion",
        "owned_table": "contract_lifecycle_contract_control_assertion",
        "label": "Control Assertion",
        "fields": _business_fields(
            extra_fields=(
                {"name": "control_id", "type": "string", "required": True},
                {"name": "assertion_result", "type": "string", "required": True},
            )
        ),
        "relationships": (),
    },
    {
        "logical_table": "contract_governed_model",
        "owned_table": "contract_lifecycle_contract_governed_model",
        "label": "Governed Model",
        "fields": _business_fields(
            extra_fields=(
                {"name": "model_name", "type": "string", "required": True},
                {"name": "governance_state", "type": "string", "required": True},
            )
        ),
        "relationships": (),
    },
    {
        "logical_table": "appgen_outbox_event",
        "owned_table": "contract_lifecycle_appgen_outbox_event",
        "label": "Outbox Event",
        "fields": _business_fields(
            extra_fields=(
                {"name": "event_type", "type": "string", "required": True},
                {"name": "idempotency_key", "type": "string", "required": True},
            )
        ),
        "relationships": (),
    },
    {
        "logical_table": "appgen_inbox_event",
        "owned_table": "contract_lifecycle_appgen_inbox_event",
        "label": "Inbox Event",
        "fields": _business_fields(
            extra_fields=(
                {"name": "event_type", "type": "string", "required": True},
                {"name": "idempotency_key", "type": "string", "required": True},
            )
        ),
        "relationships": (),
    },
    {
        "logical_table": "appgen_dead_letter_event",
        "owned_table": "contract_lifecycle_appgen_dead_letter_event",
        "label": "Dead Letter Event",
        "fields": _business_fields(
            extra_fields=(
                {"name": "event_type", "type": "string", "required": True},
                {"name": "dead_letter_reason", "type": "string", "required": True},
            )
        ),
        "relationships": (),
    },
)

OWNED_TABLES = tuple(spec["owned_table"] for spec in TABLE_SPECS)
BUSINESS_TABLES = tuple(spec["owned_table"] for spec in TABLE_SPECS[:-3])
EVENT_TABLES = tuple(spec["owned_table"] for spec in TABLE_SPECS[-3:])

TABLE_BY_LOGICAL = {spec["logical_table"]: spec for spec in TABLE_SPECS}
TABLE_BY_OWNED = {spec["owned_table"]: spec for spec in TABLE_SPECS}

MODELS = tuple(
    {
        "class_name": "".join(part.capitalize() for part in spec["owned_table"].split("_")),
        "table": spec["owned_table"],
        "fields": spec["fields"],
        "relationships": spec["relationships"],
    }
    for spec in TABLE_SPECS
)

OPERATION_SPECS = {
    "intake_contract": {
        "target_table": "contract_lifecycle_contract_record",
        "emitted_event": "ContractIntaked",
        "required_permission": "contract_lifecycle.create",
        "route": ("POST", "/contracts/intake"),
        "form_id": "contract_intake_form",
        "wizard_id": "intake_readiness_wizard",
    },
    "classify_contract": {
        "target_table": "contract_lifecycle_contract_record",
        "emitted_event": None,
        "required_permission": "contract_lifecycle.update",
        "route": ("POST", "/contracts/{id}/classify"),
        "form_id": "classification_form",
        "wizard_id": "intake_readiness_wizard",
    },
    "create_authoring_workspace": {
        "target_table": "contract_lifecycle_contract_authoring_workspace",
        "emitted_event": None,
        "required_permission": "contract_lifecycle.update",
        "route": ("POST", "/contracts/{id}/authoring-workspace"),
        "form_id": "classification_form",
        "wizard_id": "negotiation_wizard",
    },
    "select_clause": {
        "target_table": "contract_lifecycle_clause_library",
        "emitted_event": "ClauseSelected",
        "required_permission": "contract_lifecycle.update",
        "route": ("POST", "/contracts/{id}/clauses"),
        "form_id": "clause_selection_form",
        "wizard_id": "negotiation_wizard",
    },
    "negotiate_redline": {
        "target_table": "contract_lifecycle_contract_redline_event",
        "emitted_event": None,
        "required_permission": "contract_lifecycle.update",
        "route": ("POST", "/contracts/{id}/redlines"),
        "form_id": "clause_selection_form",
        "wizard_id": "negotiation_wizard",
    },
    "route_approval": {
        "target_table": "contract_lifecycle_contract_approval_task",
        "emitted_event": "ContractApproved",
        "required_permission": "contract_lifecycle.approve",
        "route": ("POST", "/contracts/{id}/approvals"),
        "form_id": "approval_route_form",
        "wizard_id": "negotiation_wizard",
    },
    "capture_signature": {
        "target_table": "contract_lifecycle_contract_signature_packet",
        "emitted_event": "ContractSigned",
        "required_permission": "contract_lifecycle.approve",
        "route": ("POST", "/contracts/{id}/signature"),
        "form_id": "signature_packet_form",
        "wizard_id": "negotiation_wizard",
    },
    "activate_obligation": {
        "target_table": "contract_lifecycle_contract_obligation",
        "emitted_event": "ObligationActivated",
        "required_permission": "contract_lifecycle.update",
        "route": ("POST", "/contracts/{id}/obligations"),
        "form_id": "obligation_activation_form",
        "wizard_id": "renewal_amendment_wizard",
    },
    "record_obligation_performance": {
        "target_table": "contract_lifecycle_obligation_performance_event",
        "emitted_event": None,
        "required_permission": "contract_lifecycle.update",
        "route": ("POST", "/contracts/{id}/obligations/{obligation_id}/performance"),
        "form_id": "obligation_activation_form",
        "wizard_id": "renewal_amendment_wizard",
    },
    "track_milestone": {
        "target_table": "contract_lifecycle_contract_milestone",
        "emitted_event": None,
        "required_permission": "contract_lifecycle.update",
        "route": ("POST", "/contracts/{id}/milestones"),
        "form_id": "obligation_activation_form",
        "wizard_id": "renewal_amendment_wizard",
    },
    "schedule_renewal": {
        "target_table": "contract_lifecycle_contract_renewal_event",
        "emitted_event": "RenewalScheduled",
        "required_permission": "contract_lifecycle.update",
        "route": ("POST", "/contracts/{id}/renewals"),
        "form_id": "renewal_planning_form",
        "wizard_id": "renewal_amendment_wizard",
    },
    "execute_amendment": {
        "target_table": "contract_lifecycle_contract_amendment",
        "emitted_event": None,
        "required_permission": "contract_lifecycle.update",
        "route": ("POST", "/contracts/{id}/amendments"),
        "form_id": "renewal_planning_form",
        "wizard_id": "renewal_amendment_wizard",
    },
    "run_compliance_check": {
        "target_table": "contract_lifecycle_contract_compliance_check",
        "emitted_event": None,
        "required_permission": "contract_lifecycle.read",
        "route": ("POST", "/contracts/{id}/compliance-checks"),
        "form_id": "approval_route_form",
        "wizard_id": "renewal_amendment_wizard",
    },
    "score_contract_risk": {
        "target_table": "contract_lifecycle_contract_risk_assessment",
        "emitted_event": "ContractRiskChanged",
        "required_permission": "contract_lifecycle.read",
        "route": ("POST", "/contracts/{id}/risk-score"),
        "form_id": "approval_route_form",
        "wizard_id": "intake_readiness_wizard",
    },
    "index_contract_documents": {
        "target_table": "contract_lifecycle_contract_search_index",
        "emitted_event": None,
        "required_permission": "contract_lifecycle.update",
        "route": ("POST", "/contracts/{id}/documents/index"),
        "form_id": "contract_intake_form",
        "wizard_id": "intake_readiness_wizard",
    },
    "resolve_contract_exception": {
        "target_table": "contract_lifecycle_contract_exception_case",
        "emitted_event": None,
        "required_permission": "contract_lifecycle.update",
        "route": ("POST", "/contracts/{id}/exceptions"),
        "form_id": "approval_route_form",
        "wizard_id": "renewal_amendment_wizard",
    },
    "compile_contract_rule": {
        "target_table": "contract_lifecycle_contract_policy_rule",
        "emitted_event": None,
        "required_permission": "contract_lifecycle.admin",
        "route": ("POST", "/contracts/rules/compile"),
        "form_id": "approval_route_form",
        "wizard_id": "intake_readiness_wizard",
    },
    "simulate_counterparty_impact": {
        "target_table": "contract_lifecycle_contract_governed_model",
        "emitted_event": None,
        "required_permission": "contract_lifecycle.read",
        "route": ("POST", "/contracts/{id}/simulate-impact"),
        "form_id": "renewal_planning_form",
        "wizard_id": "renewal_amendment_wizard",
    },
}

PUBLIC_ROUTE_ALIASES = (
    ("POST", "/contracts", "intake_contract"),
    ("POST", "/contracts/{id}/clauses", "select_clause"),
    ("POST", "/contracts/{id}/obligations", "activate_obligation"),
    ("POST", "/contracts/{id}/approvals", "route_approval"),
    ("POST", "/contracts/{id}/renewals", "schedule_renewal"),
    ("GET", "/contract-lifecycle-workbench", "query_workbench"),
)


def digest(value) -> str:
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def parameter_defaults() -> dict:
    return {item["key"]: item["default"] for item in PARAMETER_DEFINITIONS}


def default_configuration() -> dict:
    return {
        "database_backend": "postgresql",
        "event_topic": REQUIRED_EVENT_TOPIC,
        "retry_limit": 5,
        "default_policy": "approval_threshold_policy",
        "agent_write_requires_confirmation": True,
        "event_contract": "AppGen-X",
    }


def empty_state() -> dict:
    return {
        "tables": {table: {} for table in OWNED_TABLES},
        "contracts": {},
        "compiled_rules": {},
        "parameters": parameter_defaults(),
        "configuration": default_configuration(),
        "outbox": [],
        "inbox": [],
        "dead_letter": [],
        "idempotency_keys": set(),
        "projections": {
            "customers": {},
            "suppliers": {},
            "identities": {},
            "policy_changes": [],
        },
    }


def clone_state(state: dict | None = None) -> dict:
    source = state or empty_state()
    copied = deepcopy(source)
    copied["idempotency_keys"] = set(source.get("idempotency_keys", set()))
    return copied


def owned_table_contracts() -> tuple[dict, ...]:
    return tuple(TABLE_SPECS)


def schema_contract() -> dict:
    migrations = tuple(
        {
            "path": f"pbcs/contract_lifecycle/migrations/{index + 1:03d}_{spec['logical_table']}.sql",
            "operation": "create_owned_table",
            "table": spec["owned_table"],
            "backend_allowlist": ALLOWED_DATABASE_BACKENDS,
        }
        for index, spec in enumerate(TABLE_SPECS)
    )
    return {
        "format": "appgen.contract-lifecycle-owned-schema-contract.v2",
        "ok": True,
        "pbc": PBC_KEY,
        "tables": owned_table_contracts(),
        "models": MODELS,
        "migrations": migrations,
        "owned_tables": OWNED_TABLES,
        "database_backends": ALLOWED_DATABASE_BACKENDS,
        "shared_table_access": False,
    }


def schema_boundary_check(references) -> dict:
    allowed = set(OWNED_TABLES) | set(CONSUMED_EVENTS) | {"api_dependency", "projection_dependency"}
    foreign = tuple(ref for ref in references if ref not in allowed and not str(ref).startswith(f"{PBC_KEY}_"))
    return {
        "ok": not foreign,
        "foreign_references": foreign,
        "allowed_dependency_modes": ("api", "event", "projection"),
    }


def configuration_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "database_backends": ALLOWED_DATABASE_BACKENDS,
        "event_contract": "AppGen-X",
        "configuration_schema": CONFIGURATION_SCHEMA,
        "stream_engine_picker_visible": False,
    }


def validate_configuration(config=None) -> dict:
    config = {**default_configuration(), **dict(config or {})}
    errors = []
    if config["database_backend"] not in ALLOWED_DATABASE_BACKENDS:
        errors.append("database_backend")
    if config["event_topic"] != REQUIRED_EVENT_TOPIC:
        errors.append("event_topic")
    if not 1 <= int(config["retry_limit"]) <= 10:
        errors.append("retry_limit")
    if config["default_policy"] not in tuple(item["rule_id"] for item in RULE_DEFINITIONS):
        errors.append("default_policy")
    if config["agent_write_requires_confirmation"] is not True:
        errors.append("agent_write_requires_confirmation")
    return {
        "ok": not errors,
        "config": config,
        "errors": tuple(errors),
        "event_contract": "AppGen-X",
    }


def parameter_manifest() -> dict:
    return {"ok": True, "pbc": PBC_KEY, "parameters": PARAMETER_DEFINITIONS}


def set_parameter(state, key, value) -> dict:
    next_state = clone_state(state)
    schema = next((item for item in PARAMETER_DEFINITIONS if item["key"] == key), None)
    if not schema:
        return {"ok": False, "state": next_state, "reason": "unknown_parameter", "parameter": key}
    if not schema["min"] <= value <= schema["max"]:
        return {"ok": False, "state": next_state, "reason": "parameter_out_of_bounds", "parameter": key}
    next_state["parameters"][key] = value
    parameter_row = _table_row(
        "contract_lifecycle_contract_runtime_parameter",
        code=key.upper(),
        status="active",
        payload={"key": key, "value": value, "scope": schema["scope"]},
        parameter_name=key,
        parameter_value=str(value),
    )
    _store_row(next_state, "contract_lifecycle_contract_runtime_parameter", parameter_row)
    return {"ok": True, "state": next_state, "parameter": schema, "value": value}


def rule_manifest() -> dict:
    return {"ok": True, "pbc": PBC_KEY, "rules": RULE_DEFINITIONS}


def compile_rule(rule) -> dict:
    rule = dict(rule)
    if "stream_engine" in repr(rule):
        return {"ok": False, "compiled": False, "reason": "stream_engine_picker_disallowed"}
    rule_id = rule.get("rule_id", "ad_hoc_rule")
    compiled = {
        **rule,
        "compiled_hash": digest(rule),
        "compiled_at": utc_now(),
        "event_contract": "AppGen-X",
    }
    return {"ok": True, "compiled": True, "rule_id": rule_id, "rule": compiled}


def evaluate_rule(compiled, context=None) -> dict:
    context = dict(context or {})
    if compiled.get("compiled") is False:
        return {"ok": False, "allowed": False, "context": context}
    risk_score = float(context.get("risk_score", 0.0))
    value_amount = float(context.get("value_amount", 0.0))
    allowed = risk_score <= 0.95 and value_amount >= 0.0
    return {"ok": True, "allowed": allowed, "context": context, "scope": compiled.get("rule", {}).get("scope")}


def permission_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "permissions": PERMISSIONS,
        "rbac_roles": tuple(RBAC_ROLE_PERMISSIONS),
        "role_permissions": RBAC_ROLE_PERMISSIONS,
    }


def authorize(actor, permission) -> dict:
    actor_roles = actor.get("roles") if isinstance(actor, dict) else (str(actor),)
    allowed_permissions = {perm for role in actor_roles for perm in RBAC_ROLE_PERMISSIONS.get(role, ())}
    allowed = permission in allowed_permissions or "contract_lifecycle.admin" in allowed_permissions
    return {
        "ok": permission in PERMISSIONS,
        "allowed": allowed,
        "actor": actor,
        "permission": permission,
        "roles": tuple(actor_roles),
    }


def operation_plan(operation, payload=None) -> dict:
    spec = OPERATION_SPECS.get(operation)
    payload = dict(payload or {})
    if not spec:
        return {"ok": False, "reason": "unknown_domain_operation", "operation": operation}
    idempotency_key = digest((PBC_KEY, operation, tuple(sorted(payload.items()))))
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "operation": operation,
        "operation_kind": "command",
        "target_table": spec["target_table"],
        "owned_tables": (spec["target_table"],),
        "read_tables": (),
        "emitted_event": spec["emitted_event"],
        "required_permission": spec["required_permission"],
        "route": spec["route"],
        "form_id": spec["form_id"],
        "wizard_id": spec["wizard_id"],
        "idempotency_key": idempotency_key,
        "rules_evaluated": tuple(item["rule_id"] for item in RULE_DEFINITIONS[:3]),
        "parameters_read": tuple(item["key"] for item in PARAMETER_DEFINITIONS[:3]),
        "event_contract": "AppGen-X",
        "shared_table_access": False,
        "stream_engine_picker_visible": False,
    }


def service_contract() -> dict:
    return {
        "format": "appgen.contract-lifecycle-service-contract.v2",
        "ok": True,
        "pbc": PBC_KEY,
        "command_methods": tuple(OPERATION_SPECS) + (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "register_schema_extension",
            "receive_event",
            "parse_document_instruction",
        ),
        "query_methods": ("query_workbench", "build_workbench_view"),
        "shared_table_access": False,
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
    }


def route_contracts() -> tuple[dict, ...]:
    routes = []
    for method, path, operation in PUBLIC_ROUTE_ALIASES:
        required_permission = "contract_lifecycle.read" if method == "GET" else OPERATION_SPECS[operation]["required_permission"]
        routes.append(
            {
                "method": method,
                "path": path,
                "operation": operation,
                "required_permission": required_permission,
                "idempotency_key": f"{PBC_KEY}:{method}:{path}",
                "event_contract": "AppGen-X",
                "shared_table_access": False,
                "stream_engine_picker_visible": False,
            }
        )
    return tuple(routes)


def ui_contract() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "fragments": PUBLIC_UI_FRAGMENTS,
        "workbench_view": PUBLIC_UI_FRAGMENTS[0],
        "forms": FORMS,
        "wizards": WIZARDS,
        "controls": CONTROLS,
        "workbench_views": WORKBENCH_VIEWS,
        "advanced_capabilities": ADVANCED_CAPABILITIES,
        "action_permissions": PERMISSIONS,
        "stream_engine_picker_visible": False,
        "configuration_editor": True,
    }


def render_workbench(state=None) -> dict:
    state = state or empty_state()
    contracts = tuple(state.get("contracts", {}).values())
    active_contracts = tuple(item for item in contracts if item["status"] == "active")
    pending_approvals = tuple(
        row
        for row in state["tables"]["contract_lifecycle_contract_approval_task"].values()
        if row["status"] != "approved"
    )
    due_obligations = tuple(
        row
        for row in state["tables"]["contract_lifecycle_contract_obligation"].values()
        if row["status"] not in {"performed", "closed"}
    )
    exceptions = tuple(state["tables"]["contract_lifecycle_contract_exception_case"].values())
    dead_letters = tuple(state.get("dead_letter", ()))
    metrics = {
        "contracts_total": len(contracts),
        "contracts_active": len(active_contracts),
        "approval_tasks_open": len(pending_approvals),
        "obligations_open": len(due_obligations),
        "exceptions_open": len(exceptions),
        "dead_letters": len(dead_letters),
    }
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "view": PUBLIC_UI_FRAGMENTS[0],
        "panels": WORKBENCH_VIEWS,
        "metrics": metrics,
        "queue_samples": {
            "approvals": pending_approvals[:3],
            "obligations": due_obligations[:3],
            "exceptions": exceptions[:3],
            "dead_letters": dead_letters[:3],
        },
        "forms": FORMS,
        "wizards": WIZARDS,
        "controls": CONTROLS,
        "action_permissions": PERMISSIONS,
    }


def agent_skill_manifest() -> dict:
    skills = []
    for operation, spec in OPERATION_SPECS.items():
        skills.append(
            {
                "name": f"{PBC_KEY}_{operation}",
                "scope": PBC_KEY,
                "description": f"{operation.replace('_', ' ')} assistant for contract lifecycle operators",
                "requires_confirmation_for_mutation": True,
                "uses_appgen_event_contract": True,
                "target_table": spec["target_table"],
            }
        )
    skills.extend(
        (
            {
                "name": f"{PBC_KEY}_read_records",
                "scope": PBC_KEY,
                "description": "Read owned contract lifecycle records",
                "requires_confirmation_for_mutation": False,
                "uses_appgen_event_contract": False,
                "target_table": "contract_lifecycle_contract_record",
            },
            {
                "name": f"{PBC_KEY}_document_instruction",
                "scope": PBC_KEY,
                "description": "Parse contract document instructions into governed CRUD previews",
                "requires_confirmation_for_mutation": True,
                "uses_appgen_event_contract": True,
                "target_table": "contract_lifecycle_contract_record",
            },
        )
    )
    return {"ok": True, "pbc": PBC_KEY, "skills": tuple(skills)}


def chatbot_interface_contract() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "entrypoint": f"/assistant/pbc/{PBC_KEY}",
        "single_agent_contribution": f"{PBC_KEY}_skills",
        "capabilities": (
            "task_guidance",
            "document_instruction_intake",
            "governed_datastore_crud",
            "mutation_preview",
            "release_evidence_lookup",
        ),
        "owned_tables": OWNED_TABLES,
    }


def _normalize_table_name(table: str | None) -> str:
    if not table:
        return "contract_lifecycle_contract_record"
    if table.startswith(f"{PBC_KEY}_"):
        return table
    if table in TABLE_BY_LOGICAL:
        return TABLE_BY_LOGICAL[table]["owned_table"]
    return table


def datastore_crud_plan(action, table=None, payload=None) -> dict:
    target = _normalize_table_name(table)
    if target not in TABLE_BY_OWNED:
        return {"ok": False, "reason": "foreign_table_rejected", "table": target}
    payload = dict(payload or {})
    field_names = tuple(field["name"] for field in TABLE_BY_OWNED[target]["fields"])
    metadata_fields = {"notes", "metadata", "document_digest", "instruction_digest", "keywords"}
    unknown_fields = tuple(name for name in payload if name not in field_names and name not in metadata_fields)
    if unknown_fields:
        return {
            "ok": False,
            "reason": "unknown_fields",
            "table": target,
            "unknown_fields": unknown_fields,
        }
    mutation = action in {"create", "update", "delete"}
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "action": action,
        "table": target,
        "payload": payload,
        "requires_confirmation": mutation,
        "event_contract": "AppGen-X" if mutation else None,
        "allowed_fields": field_names,
    }


def document_instruction_plan(document, instruction) -> dict:
    text = f"{document}\n{instruction}".lower()
    action = "read"
    for candidate in ("delete", "update", "create"):
        if candidate in text:
            action = candidate
            break
    target_map = (
        ("obligation", "contract_obligation"),
        ("approval", "contract_approval_task"),
        ("renewal", "contract_renewal_event"),
        ("amendment", "contract_amendment"),
        ("exception", "contract_exception_case"),
        ("clause", "clause_library"),
        ("party", "contract_party"),
        ("signature", "contract_signature_packet"),
        ("risk", "contract_risk_assessment"),
        ("milestone", "contract_milestone"),
        ("document", "contract_document_packet"),
    )
    logical_targets = tuple(logical for keyword, logical in target_map if keyword in text) or ("contract_record",)
    candidate_tables = tuple(TABLE_BY_LOGICAL[logical]["owned_table"] for logical in logical_targets)
    safe_payload = {
        "document_digest": digest(document),
        "instruction_digest": digest(instruction),
        "keywords": tuple(sorted({keyword for keyword, _ in target_map if keyword in text})),
    }
    previews = tuple(datastore_crud_plan(action, table=table, payload=safe_payload) for table in candidate_tables)
    return {
        "ok": all(item["ok"] for item in previews),
        "pbc": PBC_KEY,
        "document_digest": safe_payload["document_digest"],
        "instruction": instruction,
        "candidate_tables": candidate_tables,
        "requires_human_confirmation": action in {"create", "update", "delete"},
        "crud_preview": previews,
        "missing_inputs": tuple(
            name
            for name in ("contract_id", "owner", "effective_date")
            if name not in text and action != "read"
        ),
    }


def composed_agent_contribution() -> dict:
    namespace = f"{PBC_KEY}_skills"
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "single_agent_skill_namespace": namespace,
        "dsl_tools": (namespace, f"{PBC_KEY}_crud", f"{PBC_KEY}_documents", f"{PBC_KEY}_release"),
    }


def event_contract_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "contract": "AppGen-X",
        "emitted": tuple(dict.fromkeys(EMITTED_EVENTS + LEGACY_PUBLIC_EVENTS)),
        "consumed": CONSUMED_EVENTS,
        "outbox_table": "contract_lifecycle_appgen_outbox_event",
        "inbox_table": "contract_lifecycle_appgen_inbox_event",
        "dead_letter_table": "contract_lifecycle_appgen_dead_letter_event",
        "idempotency": "required",
        "stream_engine_picker_visible": False,
    }


def validate_event_contract() -> dict:
    manifest = event_contract_manifest()
    invalid_tables = tuple(
        table
        for table in (
            manifest["outbox_table"],
            manifest["inbox_table"],
            manifest["dead_letter_table"],
        )
        if table not in EVENT_TABLES
    )
    return {
        "ok": manifest["contract"] == "AppGen-X"
        and not invalid_tables
        and manifest["stream_engine_picker_visible"] is False,
        "manifest": manifest,
        "invalid_tables": invalid_tables,
    }


def build_event_envelope(event_type, payload=None) -> dict:
    payload = dict(payload or {})
    return {
        "ok": event_type in event_contract_manifest()["emitted"] + CONSUMED_EVENTS,
        "event_type": event_type,
        "payload": payload,
        "idempotency_key": payload.get("idempotency_key") or digest((event_type, tuple(sorted(payload.items())))),
        "event_contract": "AppGen-X",
    }


def event_dispatch_plan(event_type, payload=None) -> dict:
    envelope = build_event_envelope(event_type, payload)
    return {
        "ok": envelope["ok"],
        "envelope": envelope,
        "outbox_table": "contract_lifecycle_appgen_outbox_event",
        "retry_policy": {"max_attempts": 5, "backoff": "exponential"},
        "dead_letter_table": "contract_lifecycle_appgen_dead_letter_event",
    }


def _table_row(table, code, status, payload=None, **extra):
    row = {
        "id": extra.pop("id", f"{table}:{digest((table, code, payload, utc_now()))[:12]}"),
        "tenant": extra.pop("tenant", "default"),
        "code": code,
        "status": status,
        "version": extra.pop("version", 1),
        "payload": dict(payload or {}),
        "created_at": utc_now(),
        "updated_at": utc_now(),
    }
    row.update(extra)
    return row


def _store_row(state, table, row):
    state["tables"][table][row["id"]] = row


def _emit(state, event_type, payload):
    envelope = build_event_envelope(event_type, payload)
    state["outbox"].append(envelope)
    row = _table_row(
        "contract_lifecycle_appgen_outbox_event",
        code=event_type.upper(),
        status="queued",
        payload=payload,
        event_type=event_type,
        idempotency_key=envelope["idempotency_key"],
        tenant=payload.get("tenant", "default"),
    )
    _store_row(state, "contract_lifecycle_appgen_outbox_event", row)
    return envelope


def _transition(contract, target_status):
    current_status = contract["status"]
    allowed = LIFECYCLE_TRANSITIONS.get(current_status, set())
    return target_status in allowed


def _append_history(contract, step, payload, emitted_event=None):
    history = list(contract.get("history", ()))
    history.append(
        {
            "step": step,
            "at": utc_now(),
            "payload_digest": digest(payload),
            "emitted_event": emitted_event,
        }
    )
    contract["history"] = tuple(history)


def _required_intake_fields(payload):
    return (
        "request_purpose",
        "contract_type",
        "jurisdiction",
        "counterparty_name",
        "value_amount",
        "currency",
        "term_months",
        "owner",
        "source_documents",
    )


def _intake_missing_fields(payload):
    return tuple(name for name in _required_intake_fields(payload) if not payload.get(name))


def _contract_summary(contract):
    return {
        "contract_id": contract["id"],
        "code": contract["code"],
        "status": contract["status"],
        "contract_type": contract.get("contract_type"),
        "value_amount": contract.get("value_amount"),
        "currency": contract.get("currency"),
        "risk_score": contract.get("risk_score", 0.0),
        "parties": tuple(contract.get("parties", ())),
        "approvals": tuple(contract.get("approvals", ())),
        "obligations": tuple(contract.get("obligations", ())),
    }


def _get_contract(state, contract_id):
    return state["contracts"].get(contract_id)


def _upsert_contract_record(state, contract):
    row = _table_row(
        "contract_lifecycle_contract_record",
        id=contract["id"],
        tenant=contract["tenant"],
        code=contract["code"],
        status=contract["status"],
        version=contract["version"],
        payload=contract,
        contract_type=contract.get("contract_type"),
        jurisdiction=contract.get("jurisdiction"),
        value_amount=contract.get("value_amount"),
        currency=contract.get("currency"),
        counterparty_name=contract.get("counterparty_name"),
        effective_date=contract.get("effective_date"),
    )
    _store_row(state, "contract_lifecycle_contract_record", row)


def _risk_score(contract, state):
    score = 0.18
    if contract.get("value_amount", 0) >= state["parameters"]["approval_value_limit"]:
        score += 0.22
    if contract.get("jurisdiction") in {"DE", "FR", "BR"}:
        score += 0.08
    if contract.get("has_material_redline"):
        score += 0.2
    if not contract.get("signatory_verified"):
        score += 0.12
    if not state["projections"]["suppliers"].get(contract.get("counterparty_name"), {}).get("qualified", False):
        score += 0.1
    return round(min(score, 0.99), 2)


def _approval_route(contract, state, payload):
    approvals = []
    approvals.append({"role": "legal_analyst", "status": "approved"})
    if contract.get("value_amount", 0) >= state["parameters"]["approval_value_limit"]:
        approvals.append({"role": "approver", "status": "approved" if payload.get("auto_approve") else "pending"})
    if payload.get("requires_security_review") or contract.get("data_sensitivity") in {"high", "restricted"}:
        approvals.append({"role": "admin", "status": "approved" if payload.get("auto_approve") else "pending"})
    custom = payload.get("approvals")
    if custom:
        approvals = [dict(item) for item in custom]
    return approvals


def _operation_result(ok, state, operation, contract=None, rows=None, emitted_event=None, reason=None, extra=None):
    result = {
        "ok": ok,
        "state": state,
        "operation": operation,
        "rows": tuple(rows or ()),
        "emitted_event": emitted_event,
        "reason": reason,
        "workbench": render_workbench(state),
    }
    if contract:
        result["contract"] = _contract_summary(contract)
    if extra:
        result.update(extra)
    return result


def execute_operation(state, operation, payload=None) -> dict:
    payload = dict(payload or {})
    next_state = clone_state(state)
    if operation not in OPERATION_SPECS:
        return _operation_result(False, next_state, operation, reason="unknown_domain_operation")
    handler = _OPERATION_HANDLERS[operation]
    return handler(next_state, payload)


def _intake_contract(state, payload):
    missing = _intake_missing_fields(payload)
    if missing:
        return _operation_result(
            False,
            state,
            "intake_contract",
            reason="intake_readiness_failed",
            extra={"missing_fields": missing},
        )
    contract_id = payload.get("contract_id") or f"contract:{digest(payload)[:10]}"
    contract = {
        "id": contract_id,
        "tenant": payload.get("tenant", "default"),
        "code": payload.get("code", contract_id.replace(":", "-").upper()),
        "status": "intake_ready",
        "version": 1,
        "request_purpose": payload["request_purpose"],
        "contract_type": payload["contract_type"],
        "jurisdiction": payload["jurisdiction"],
        "counterparty_name": payload["counterparty_name"],
        "value_amount": payload["value_amount"],
        "currency": payload["currency"],
        "term_months": payload["term_months"],
        "owner": payload["owner"],
        "effective_date": payload.get("effective_date"),
        "parties": tuple(payload.get("parties", ())),
        "source_documents": tuple(payload.get("source_documents", ())),
        "obligations": (),
        "approvals": (),
        "history": (),
        "risk_score": 0.0,
        "has_material_redline": False,
        "signatory_verified": False,
    }
    _append_history(contract, "intake_contract", payload, emitted_event="ContractIntaked")
    state["contracts"][contract_id] = contract
    _upsert_contract_record(state, contract)
    packet_row = _table_row(
        "contract_lifecycle_contract_document_packet",
        tenant=contract["tenant"],
        code=f"{contract['code']}-INTAKE",
        status="received",
        payload={"documents": contract["source_documents"], "document_count": len(contract["source_documents"])},
        contract_id=contract_id,
        packet_type="intake",
        document_hash=digest(contract["source_documents"]),
    )
    value_row = _table_row(
        "contract_lifecycle_contract_value_snapshot",
        tenant=contract["tenant"],
        code=f"{contract['code']}-VALUE",
        status="captured",
        payload={"source": "intake", "confidence": "declared"},
        contract_id=contract_id,
        snapshot_amount=contract["value_amount"],
        currency=contract["currency"],
    )
    _store_row(state, "contract_lifecycle_contract_document_packet", packet_row)
    _store_row(state, "contract_lifecycle_contract_value_snapshot", value_row)
    for party in contract["parties"]:
        party_row = _table_row(
            "contract_lifecycle_contract_party",
            tenant=contract["tenant"],
            code=party["role"].upper(),
            status="identified",
            payload=party,
            contract_id=contract_id,
            role=party["role"],
            legal_name=party["legal_name"],
            authority_state=party.get("authority_state", "unknown"),
        )
        _store_row(state, "contract_lifecycle_contract_party", party_row)
    _emit(state, "ContractIntaked", {"tenant": contract["tenant"], "contract_id": contract_id, "code": contract["code"]})
    return _operation_result(True, state, "intake_contract", contract, rows=(packet_row, value_row))


def _classify_contract(state, payload):
    contract = _get_contract(state, payload.get("contract_id"))
    if not contract:
        return _operation_result(False, state, "classify_contract", reason="contract_not_found")
    if not _transition(contract, "authoring"):
        return _operation_result(False, state, "classify_contract", contract, reason="invalid_transition")
    contract.update(
        {
            "status": "authoring",
            "taxonomy_version": payload.get("taxonomy_version", "2026.1"),
            "category": payload.get("category", contract["contract_type"]),
            "data_sensitivity": payload.get("data_sensitivity", "medium"),
            "controlling_language": payload.get("controlling_language", "en"),
            "version": contract["version"] + 1,
        }
    )
    _append_history(contract, "classify_contract", payload)
    _upsert_contract_record(state, contract)
    return _operation_result(True, state, "classify_contract", contract)


def _create_authoring_workspace(state, payload):
    contract = _get_contract(state, payload.get("contract_id"))
    if not contract:
        return _operation_result(False, state, "create_authoring_workspace", reason="contract_not_found")
    workspace_row = _table_row(
        "contract_lifecycle_contract_authoring_workspace",
        tenant=contract["tenant"],
        code=f"{contract['code']}-WS",
        status="open",
        payload={"locked_sections": tuple(payload.get("locked_sections", ())), "template_lineage": payload.get("template_code", "msa-standard")},
        contract_id=contract["id"],
        template_code=payload.get("template_code", "msa-standard"),
        workspace_owner=payload.get("workspace_owner", contract["owner"]),
    )
    _store_row(state, "contract_lifecycle_contract_authoring_workspace", workspace_row)
    _append_history(contract, "create_authoring_workspace", payload)
    _upsert_contract_record(state, contract)
    return _operation_result(True, state, "create_authoring_workspace", contract, rows=(workspace_row,))


def _select_clause(state, payload):
    contract = _get_contract(state, payload.get("contract_id"))
    if not contract:
        return _operation_result(False, state, "select_clause", reason="contract_not_found")
    clause_row = _table_row(
        "contract_lifecycle_clause_library",
        tenant=contract["tenant"],
        code=payload.get("clause_family", "GENERAL").upper(),
        status="selected",
        payload=payload,
        contract_id=contract["id"],
        clause_family=payload.get("clause_family", "general"),
        variant_code=payload.get("variant_code", "std"),
        fallback_tier=payload.get("fallback_tier"),
    )
    variant_row = _table_row(
        "contract_lifecycle_clause_variant",
        tenant=contract["tenant"],
        code=payload.get("variant_code", "STD").upper(),
        status="approved" if payload.get("fallback_tier") in {None, "tier_1"} else "review",
        payload=payload,
        contract_id=contract["id"],
        variant_code=payload.get("variant_code", "std"),
        fallback_tier=payload.get("fallback_tier"),
    )
    _store_row(state, "contract_lifecycle_clause_library", clause_row)
    _store_row(state, "contract_lifecycle_clause_variant", variant_row)
    clauses = list(contract.get("clauses", ()))
    clauses.append({"family": clause_row["clause_family"], "variant": variant_row["variant_code"]})
    contract["clauses"] = tuple(clauses)
    _append_history(contract, "select_clause", payload, emitted_event="ClauseSelected")
    _upsert_contract_record(state, contract)
    _emit(state, "ClauseSelected", {"tenant": contract["tenant"], "contract_id": contract["id"], "clause_family": clause_row["clause_family"]})
    return _operation_result(True, state, "select_clause", contract, rows=(clause_row, variant_row), emitted_event="ClauseSelected")


def _negotiate_redline(state, payload):
    contract = _get_contract(state, payload.get("contract_id"))
    if not contract:
        return _operation_result(False, state, "negotiate_redline", reason="contract_not_found")
    if contract["status"] not in {"authoring", "negotiation"}:
        return _operation_result(False, state, "negotiate_redline", contract, reason="invalid_contract_state")
    if contract["status"] != "negotiation":
        contract["status"] = "negotiation"
    round_row = _table_row(
        "contract_lifecycle_contract_negotiation_round",
        tenant=contract["tenant"],
        code=f"{contract['code']}-ROUND-{len(state['tables']['contract_lifecycle_contract_negotiation_round']) + 1}",
        status="open",
        payload=payload,
        contract_id=contract["id"],
        sender=payload.get("sender", "internal_legal"),
        receiver=payload.get("receiver", contract["counterparty_name"]),
        response_due_date=payload.get("response_due_date"),
    )
    materiality = float(payload.get("materiality_score", state["parameters"]["redline_materiality_score"]))
    redline_row = _table_row(
        "contract_lifecycle_contract_redline_event",
        tenant=contract["tenant"],
        code=f"{contract['code']}-REDLINE-{len(state['tables']['contract_lifecycle_contract_redline_event']) + 1}",
        status="triaged",
        payload=payload,
        contract_id=contract["id"],
        changed_clause=payload.get("changed_clause", "general"),
        materiality_score=materiality,
    )
    contract["has_material_redline"] = materiality >= state["parameters"]["redline_materiality_score"]
    _append_history(contract, "negotiate_redline", payload)
    _store_row(state, "contract_lifecycle_contract_negotiation_round", round_row)
    _store_row(state, "contract_lifecycle_contract_redline_event", redline_row)
    _upsert_contract_record(state, contract)
    return _operation_result(True, state, "negotiate_redline", contract, rows=(round_row, redline_row))


def _route_approval(state, payload):
    contract = _get_contract(state, payload.get("contract_id"))
    if not contract:
        return _operation_result(False, state, "route_approval", reason="contract_not_found")
    if contract["status"] not in {"authoring", "negotiation", "approval_pending"}:
        return _operation_result(False, state, "route_approval", contract, reason="invalid_contract_state")
    approvals = _approval_route(contract, state, payload)
    policy_row = _table_row(
        "contract_lifecycle_contract_approval_policy",
        tenant=contract["tenant"],
        code=f"{contract['code']}-APPROVAL-POLICY",
        status="active",
        payload={"approvals": approvals},
        contract_id=contract["id"],
        policy_name="value-and-risk-route",
        route_hash=digest(approvals),
    )
    task_rows = []
    for item in approvals:
        row = _table_row(
            "contract_lifecycle_contract_approval_task",
            tenant=contract["tenant"],
            code=f"{contract['code']}-{item['role'].upper()}",
            status=item["status"],
            payload=item,
            contract_id=contract["id"],
            approver_role=item["role"],
            due_date=(datetime.now(timezone.utc) + timedelta(days=2)).date().isoformat(),
        )
        task_rows.append(row)
        _store_row(state, "contract_lifecycle_contract_approval_task", row)
    _store_row(state, "contract_lifecycle_contract_approval_policy", policy_row)
    contract["approvals"] = tuple(approvals)
    approved = all(item["status"] == "approved" for item in approvals)
    contract["status"] = "approved" if approved else "approval_pending"
    _append_history(contract, "route_approval", payload, emitted_event="ContractApproved" if approved else None)
    _upsert_contract_record(state, contract)
    emitted = None
    if approved:
        emitted = "ContractApproved"
        _emit(state, emitted, {"tenant": contract["tenant"], "contract_id": contract["id"], "approval_count": len(approvals)})
    return _operation_result(True, state, "route_approval", contract, rows=(policy_row, *task_rows), emitted_event=emitted)


def _capture_signature(state, payload):
    contract = _get_contract(state, payload.get("contract_id"))
    if not contract:
        return _operation_result(False, state, "capture_signature", reason="contract_not_found")
    if contract["status"] != "approved":
        return _operation_result(False, state, "capture_signature", contract, reason="approval_required_before_signature")
    authority_ok = bool(payload.get("identity_verified")) and bool(payload.get("authority_evidence"))
    if not authority_ok:
        return _operation_result(False, state, "capture_signature", contract, reason="missing_signer_authority_evidence")
    signature_row = _table_row(
        "contract_lifecycle_contract_signature_packet",
        tenant=contract["tenant"],
        code=f"{contract['code']}-SIGNATURE",
        status="completed",
        payload=payload,
        contract_id=contract["id"],
        signer_name=payload["signer_name"],
        authority_state="verified",
        document_hash=digest((contract["id"], contract.get("clauses", ()))),
    )
    _store_row(state, "contract_lifecycle_contract_signature_packet", signature_row)
    contract["status"] = "active"
    contract["signatory_verified"] = True
    _append_history(contract, "capture_signature", payload, emitted_event="ContractSigned")
    _upsert_contract_record(state, contract)
    _emit(state, "ContractSigned", {"tenant": contract["tenant"], "contract_id": contract["id"], "signer_name": payload["signer_name"]})
    return _operation_result(True, state, "capture_signature", contract, rows=(signature_row,), emitted_event="ContractSigned")


def _activate_obligation(state, payload):
    contract = _get_contract(state, payload.get("contract_id"))
    if not contract:
        return _operation_result(False, state, "activate_obligation", reason="contract_not_found")
    if contract["status"] not in {"active", "amended"}:
        return _operation_result(False, state, "activate_obligation", contract, reason="signature_required_before_obligation")
    obligation_row = _table_row(
        "contract_lifecycle_contract_obligation",
        tenant=contract["tenant"],
        code=payload.get("obligation_code", "OBLIGATION").upper(),
        status="active",
        payload=payload,
        contract_id=contract["id"],
        owner=payload.get("owner", contract["owner"]),
        due_date=payload.get("due_date", (datetime.now(timezone.utc) + timedelta(days=30)).date().isoformat()),
        evidence_required=bool(payload.get("evidence_required", True)),
    )
    milestone_row = _table_row(
        "contract_lifecycle_contract_milestone",
        tenant=contract["tenant"],
        code=f"{obligation_row['code']}-MILESTONE",
        status="scheduled",
        payload={"source": "obligation_activation"},
        contract_id=contract["id"],
        milestone_date=obligation_row["due_date"],
        owner=obligation_row["owner"],
    )
    _store_row(state, "contract_lifecycle_contract_obligation", obligation_row)
    _store_row(state, "contract_lifecycle_contract_milestone", milestone_row)
    obligations = list(contract.get("obligations", ()))
    obligations.append({"id": obligation_row["id"], "code": obligation_row["code"], "owner": obligation_row["owner"]})
    contract["obligations"] = tuple(obligations)
    _append_history(contract, "activate_obligation", payload, emitted_event="ObligationActivated")
    _upsert_contract_record(state, contract)
    _emit(state, "ObligationActivated", {"tenant": contract["tenant"], "contract_id": contract["id"], "obligation_id": obligation_row["id"]})
    return _operation_result(True, state, "activate_obligation", contract, rows=(obligation_row, milestone_row), emitted_event="ObligationActivated")


def _record_obligation_performance(state, payload):
    contract = _get_contract(state, payload.get("contract_id"))
    if not contract:
        return _operation_result(False, state, "record_obligation_performance", reason="contract_not_found")
    obligation_id = payload.get("obligation_id")
    obligation = state["tables"]["contract_lifecycle_contract_obligation"].get(obligation_id)
    if not obligation:
        return _operation_result(False, state, "record_obligation_performance", contract, reason="obligation_not_found")
    if obligation["evidence_required"] and not payload.get("evidence_uri"):
        return _operation_result(False, state, "record_obligation_performance", contract, reason="evidence_required")
    event_row = _table_row(
        "contract_lifecycle_obligation_performance_event",
        tenant=contract["tenant"],
        code=f"{obligation['code']}-PERF",
        status="verified" if payload.get("reviewed") else "recorded",
        payload=payload,
        contract_id=contract["id"],
        obligation_id=obligation_id,
        performed_by=payload.get("performed_by", contract["owner"]),
        evidence_uri=payload.get("evidence_uri"),
    )
    obligation["status"] = "performed"
    obligation["updated_at"] = utc_now()
    _store_row(state, "contract_lifecycle_contract_obligation", obligation)
    _store_row(state, "contract_lifecycle_obligation_performance_event", event_row)
    _append_history(contract, "record_obligation_performance", payload)
    _upsert_contract_record(state, contract)
    return _operation_result(True, state, "record_obligation_performance", contract, rows=(event_row,))


def _track_milestone(state, payload):
    contract = _get_contract(state, payload.get("contract_id"))
    if not contract:
        return _operation_result(False, state, "track_milestone", reason="contract_not_found")
    row = _table_row(
        "contract_lifecycle_contract_milestone",
        tenant=contract["tenant"],
        code=payload.get("milestone_code", "MILESTONE").upper(),
        status=payload.get("status", "scheduled"),
        payload=payload,
        contract_id=contract["id"],
        milestone_date=payload.get("milestone_date", datetime.now(timezone.utc).date().isoformat()),
        owner=payload.get("owner", contract["owner"]),
    )
    _store_row(state, "contract_lifecycle_contract_milestone", row)
    _append_history(contract, "track_milestone", payload)
    _upsert_contract_record(state, contract)
    return _operation_result(True, state, "track_milestone", contract, rows=(row,))


def _schedule_renewal(state, payload):
    contract = _get_contract(state, payload.get("contract_id"))
    if not contract:
        return _operation_result(False, state, "schedule_renewal", reason="contract_not_found")
    if contract["status"] not in {"active", "amended", "renewal_pending"}:
        return _operation_result(False, state, "schedule_renewal", contract, reason="contract_not_active")
    notice_days = int(payload.get("notice_days", state["parameters"]["default_notice_days"]))
    notice_date = (datetime.now(timezone.utc) + timedelta(days=notice_days)).date().isoformat()
    row = _table_row(
        "contract_lifecycle_contract_renewal_event",
        tenant=contract["tenant"],
        code=f"{contract['code']}-RENEWAL",
        status="scheduled",
        payload=payload,
        contract_id=contract["id"],
        notice_date=notice_date,
        renewal_decision=payload.get("renewal_decision", "renegotiate"),
    )
    contract["status"] = "renewal_pending"
    _store_row(state, "contract_lifecycle_contract_renewal_event", row)
    _append_history(contract, "schedule_renewal", payload, emitted_event="RenewalScheduled")
    _upsert_contract_record(state, contract)
    _emit(state, "RenewalScheduled", {"tenant": contract["tenant"], "contract_id": contract["id"], "notice_date": notice_date})
    return _operation_result(True, state, "schedule_renewal", contract, rows=(row,), emitted_event="RenewalScheduled")


def _execute_amendment(state, payload):
    contract = _get_contract(state, payload.get("contract_id"))
    if not contract:
        return _operation_result(False, state, "execute_amendment", reason="contract_not_found")
    if contract["status"] not in {"active", "renewal_pending", "approved"}:
        return _operation_result(False, state, "execute_amendment", contract, reason="amendment_requires_live_contract")
    row = _table_row(
        "contract_lifecycle_contract_amendment",
        tenant=contract["tenant"],
        code=f"{contract['code']}-AMD-{contract['version'] + 1}",
        status="executed",
        payload=payload,
        contract_id=contract["id"],
        effective_date=payload.get("effective_date", datetime.now(timezone.utc).date().isoformat()),
        change_summary=payload.get("change_summary", "pricing and service-level adjustment"),
    )
    contract["status"] = "amended"
    contract["version"] += 1
    _store_row(state, "contract_lifecycle_contract_amendment", row)
    _append_history(contract, "execute_amendment", payload)
    _upsert_contract_record(state, contract)
    return _operation_result(True, state, "execute_amendment", contract, rows=(row,))


def _run_compliance_check(state, payload):
    contract = _get_contract(state, payload.get("contract_id"))
    if not contract:
        return _operation_result(False, state, "run_compliance_check", reason="contract_not_found")
    clauses_ok = bool(contract.get("clauses"))
    approvals_ok = all(item["status"] == "approved" for item in contract.get("approvals", ()))
    signature_ok = contract["status"] in {"active", "amended", "renewal_pending"} and contract.get("signatory_verified")
    result = "pass" if clauses_ok and approvals_ok and signature_ok else "fail"
    row = _table_row(
        "contract_lifecycle_contract_compliance_check",
        tenant=contract["tenant"],
        code=f"{contract['code']}-COMPLIANCE",
        status=result,
        payload={"clauses_ok": clauses_ok, "approvals_ok": approvals_ok, "signature_ok": signature_ok},
        contract_id=contract["id"],
        check_name=payload.get("check_name", "release-readiness"),
        result=result,
    )
    _store_row(state, "contract_lifecycle_contract_compliance_check", row)
    _append_history(contract, "run_compliance_check", payload)
    _upsert_contract_record(state, contract)
    return _operation_result(True, state, "run_compliance_check", contract, rows=(row,), extra={"check_result": result})


def _score_contract_risk(state, payload):
    contract = _get_contract(state, payload.get("contract_id"))
    if not contract:
        return _operation_result(False, state, "score_contract_risk", reason="contract_not_found")
    contract["risk_score"] = _risk_score(contract, state)
    risk_level = "high" if contract["risk_score"] >= 0.7 else "medium" if contract["risk_score"] >= 0.4 else "low"
    row = _table_row(
        "contract_lifecycle_contract_risk_assessment",
        tenant=contract["tenant"],
        code=f"{contract['code']}-RISK",
        status=risk_level,
        payload={"drivers": {"material_redline": contract.get("has_material_redline"), "signatory_verified": contract.get("signatory_verified")}},
        contract_id=contract["id"],
        risk_score=contract["risk_score"],
        risk_level=risk_level,
    )
    _store_row(state, "contract_lifecycle_contract_risk_assessment", row)
    _append_history(contract, "score_contract_risk", payload, emitted_event="ContractRiskChanged")
    _upsert_contract_record(state, contract)
    _emit(state, "ContractRiskChanged", {"tenant": contract["tenant"], "contract_id": contract["id"], "risk_score": contract["risk_score"]})
    return _operation_result(True, state, "score_contract_risk", contract, rows=(row,), emitted_event="ContractRiskChanged")


def _index_contract_documents(state, payload):
    contract = _get_contract(state, payload.get("contract_id"))
    if not contract:
        return _operation_result(False, state, "index_contract_documents", reason="contract_not_found")
    terms = sorted(
        {
            contract["code"].lower(),
            contract["contract_type"].lower(),
            contract["counterparty_name"].lower(),
            contract["jurisdiction"].lower(),
            *(item.lower() for item in payload.get("extra_terms", ())),
        }
    )
    row = _table_row(
        "contract_lifecycle_contract_search_index",
        tenant=contract["tenant"],
        code=f"{contract['code']}-SEARCH",
        status="indexed",
        payload={"terms": terms},
        contract_id=contract["id"],
        index_terms=" ".join(terms),
        document_hash=digest(contract.get("source_documents", ())),
    )
    _store_row(state, "contract_lifecycle_contract_search_index", row)
    _append_history(contract, "index_contract_documents", payload)
    _upsert_contract_record(state, contract)
    return _operation_result(True, state, "index_contract_documents", contract, rows=(row,))


def _resolve_contract_exception(state, payload):
    contract = _get_contract(state, payload.get("contract_id"))
    if not contract:
        return _operation_result(False, state, "resolve_contract_exception", reason="contract_not_found")
    severity = payload.get("severity", "medium")
    row = _table_row(
        "contract_lifecycle_contract_exception_case",
        tenant=contract["tenant"],
        code=f"{contract['code']}-EXCEPTION",
        status="resolved" if payload.get("resolved") else "open",
        payload=payload,
        contract_id=contract["id"],
        severity=severity,
        owner=payload.get("owner", contract["owner"]),
    )
    _store_row(state, "contract_lifecycle_contract_exception_case", row)
    if payload.get("resolved"):
        contract["status"] = payload.get("next_status", "authoring")
    else:
        contract["status"] = "exception"
    _append_history(contract, "resolve_contract_exception", payload)
    _upsert_contract_record(state, contract)
    return _operation_result(True, state, "resolve_contract_exception", contract, rows=(row,))


def _compile_contract_rule(state, payload):
    compiled = compile_rule(payload)
    if not compiled["ok"]:
        return _operation_result(False, state, "compile_contract_rule", reason=compiled["reason"])
    state["compiled_rules"][compiled["rule_id"]] = compiled["rule"]
    row = _table_row(
        "contract_lifecycle_contract_policy_rule",
        tenant=payload.get("tenant", "default"),
        code=compiled["rule_id"].upper(),
        status="compiled",
        payload=compiled["rule"],
        contract_id=payload.get("contract_id", "global"),
        rule_name=compiled["rule_id"],
        compiled_hash=compiled["rule"]["compiled_hash"],
    )
    _store_row(state, "contract_lifecycle_contract_policy_rule", row)
    return _operation_result(True, state, "compile_contract_rule", rows=(row,), extra={"compiled_rule": compiled["rule"]})


def _simulate_counterparty_impact(state, payload):
    contract = _get_contract(state, payload.get("contract_id"))
    if not contract:
        return _operation_result(False, state, "simulate_counterparty_impact", reason="contract_not_found")
    exposure = round(float(contract["value_amount"]) * (0.45 + contract.get("risk_score", 0.0)), 2)
    mitigations = (
        "trigger executive escalation",
        "accelerate notice preparation",
        "apply fallback service credits",
    )
    row = _table_row(
        "contract_lifecycle_contract_governed_model",
        tenant=contract["tenant"],
        code=f"{contract['code']}-SIM",
        status="ready",
        payload={"exposure": exposure, "mitigations": mitigations},
        model_name="counterparty-impact-simulation",
        governance_state="reviewed",
    )
    _store_row(state, "contract_lifecycle_contract_governed_model", row)
    _append_history(contract, "simulate_counterparty_impact", payload)
    _upsert_contract_record(state, contract)
    return _operation_result(
        True,
        state,
        "simulate_counterparty_impact",
        contract,
        rows=(row,),
        extra={"exposure": exposure, "mitigations": mitigations},
    )


_OPERATION_HANDLERS = {
    "intake_contract": _intake_contract,
    "classify_contract": _classify_contract,
    "create_authoring_workspace": _create_authoring_workspace,
    "select_clause": _select_clause,
    "negotiate_redline": _negotiate_redline,
    "route_approval": _route_approval,
    "capture_signature": _capture_signature,
    "activate_obligation": _activate_obligation,
    "record_obligation_performance": _record_obligation_performance,
    "track_milestone": _track_milestone,
    "schedule_renewal": _schedule_renewal,
    "execute_amendment": _execute_amendment,
    "run_compliance_check": _run_compliance_check,
    "score_contract_risk": _score_contract_risk,
    "index_contract_documents": _index_contract_documents,
    "resolve_contract_exception": _resolve_contract_exception,
    "compile_contract_rule": _compile_contract_rule,
    "simulate_counterparty_impact": _simulate_counterparty_impact,
}


def register_schema_extension(state, table, fields) -> dict:
    next_state = clone_state(state)
    target = _normalize_table_name(table)
    if target not in TABLE_BY_OWNED:
        return {"ok": False, "state": next_state, "reason": "unknown_owned_table", "table": target}
    row = _table_row(
        "contract_lifecycle_contract_schema_extension",
        code=target.upper(),
        status="registered",
        payload={"fields": dict(fields)},
        target_table_name=target,
        extension_hash=digest((target, fields)),
    )
    _store_row(next_state, "contract_lifecycle_contract_schema_extension", row)
    return {"ok": True, "state": next_state, "table": target, "fields": dict(fields), "row": row}


def configure_runtime(state, config) -> dict:
    next_state = clone_state(state)
    validation = validate_configuration(config)
    next_state["configuration"] = validation["config"]
    return {"ok": validation["ok"], "state": next_state, "configuration": next_state["configuration"], "errors": validation["errors"]}


def receive_event(state, event) -> dict:
    next_state = clone_state(state)
    event = dict(event)
    event_type = event.get("event_type")
    idempotency_key = event.get("idempotency_key") or f"{PBC_KEY}:{event_type}:{event.get('event_id', digest(event)[:8])}"
    if idempotency_key in next_state["idempotency_keys"]:
        return {"ok": True, "duplicate": True, "state": next_state, "idempotency_key": idempotency_key}
    next_state["idempotency_keys"].add(idempotency_key)
    if event_type not in CONSUMED_EVENTS:
        dead_letter = {
            "event_type": event_type,
            "payload": event,
            "dead_letter_reason": "unknown_event_type",
            "idempotency_key": idempotency_key,
        }
        next_state["dead_letter"].append(dead_letter)
        row = _table_row(
            "contract_lifecycle_appgen_dead_letter_event",
            code=str(event_type).upper(),
            status="dead_lettered",
            payload=event,
            event_type=event_type or "unknown",
            dead_letter_reason="unknown_event_type",
        )
        _store_row(next_state, "contract_lifecycle_appgen_dead_letter_event", row)
        return {"ok": False, "duplicate": False, "state": next_state, "dead_letter_table": "contract_lifecycle_appgen_dead_letter_event", "idempotency_key": idempotency_key}
    next_state["inbox"].append(event)
    row = _table_row(
        "contract_lifecycle_appgen_inbox_event",
        code=str(event_type).upper(),
        status="processed",
        payload=event,
        event_type=event_type,
        idempotency_key=idempotency_key,
    )
    _store_row(next_state, "contract_lifecycle_appgen_inbox_event", row)
    if event_type == "CustomerUpdated":
        customer_name = event.get("customer_name")
        if customer_name:
            next_state["projections"]["customers"][customer_name] = dict(event)
    elif event_type == "SupplierQualified":
        supplier_name = event.get("supplier_name")
        if supplier_name:
            next_state["projections"]["suppliers"][supplier_name] = {"qualified": bool(event.get("qualified", True)), **event}
    elif event_type == "PolicyChanged":
        next_state["projections"]["policy_changes"].append(event)
    elif event_type == "IdentityVerified":
        identity_key = event.get("subject") or event.get("signer_name")
        if identity_key:
            next_state["projections"]["identities"][identity_key] = dict(event)
        contract_id = event.get("contract_id")
        contract = next_state["contracts"].get(contract_id)
        if contract:
            contract["signatory_verified"] = bool(event.get("verified", True))
            _upsert_contract_record(next_state, contract)
    return {"ok": True, "duplicate": False, "state": next_state, "event_type": event_type, "idempotency_key": idempotency_key}


def handler_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "handlers": tuple(
            {
                "event_type": event_type,
                "idempotency_key": f"{PBC_KEY}:{event_type}:<event_id>",
                "retry_policy": {"max_attempts": 5, "backoff": "exponential"},
                "dead_letter_table": "contract_lifecycle_appgen_dead_letter_event",
            }
            for event_type in CONSUMED_EVENTS
        ),
    }


def governance_smoke_test() -> dict:
    config = validate_configuration(default_configuration())
    compiled = compile_rule(RULE_DEFINITIONS[0])
    evaluated = evaluate_rule(compiled, {"risk_score": 0.2, "value_amount": 10000})
    return {
        "ok": config["ok"] and compiled["ok"] and evaluated["allowed"],
        "configuration": config,
        "compiled_rule": compiled,
        "evaluated_rule": evaluated,
    }


def seed_rows() -> tuple[dict, ...]:
    return (
        {
            "table": "contract_lifecycle_contract_runtime_parameter",
            "code": "DEFAULT_NOTICE_DAYS",
            "status": "active",
            "payload": {"value": parameter_defaults()["default_notice_days"]},
        },
        {
            "table": "contract_lifecycle_contract_policy_rule",
            "code": "APPROVAL_THRESHOLD_POLICY",
            "status": "compiled",
            "payload": {"scope": "approval"},
        },
    )


def release_scenario() -> dict:
    state = empty_state()
    config = configure_runtime(state, default_configuration())
    state = config["state"]
    rule = execute_operation(
        state,
        "compile_contract_rule",
        {"rule_id": "approval_threshold_policy", "scope": "approval", "condition": "value_and_risk"},
    )
    state = rule["state"]
    intake = execute_operation(
        state,
        "intake_contract",
        {
            "tenant": "tenant-demo",
            "code": "CLM-001",
            "request_purpose": "new enterprise MSA",
            "contract_type": "MSA",
            "jurisdiction": "UK",
            "counterparty_name": "Acme Telecom",
            "value_amount": 420000,
            "currency": "USD",
            "term_months": 24,
            "owner": "legal.ops",
            "source_documents": ("msa.docx", "dpa.docx"),
            "parties": (
                {"role": "supplier", "legal_name": "Acme Telecom Ltd", "authority_state": "verified"},
                {"role": "buyer", "legal_name": "Northwind Plc", "authority_state": "verified"},
            ),
        },
    )
    state = intake["state"]
    contract_id = intake["contract"]["contract_id"]
    classify = execute_operation(
        state,
        "classify_contract",
        {
            "contract_id": contract_id,
            "taxonomy_version": "2026.1",
            "category": "technology_services",
            "data_sensitivity": "high",
            "controlling_language": "en",
        },
    )
    state = classify["state"]
    workspace = execute_operation(
        state,
        "create_authoring_workspace",
        {"contract_id": contract_id, "template_code": "msa-global-v3", "workspace_owner": "legal.ops"},
    )
    state = workspace["state"]
    clause = execute_operation(
        state,
        "select_clause",
        {
            "contract_id": contract_id,
            "clause_family": "data_processing",
            "variant_code": "dp-standard",
            "fallback_tier": "tier_1",
        },
    )
    state = clause["state"]
    redline = execute_operation(
        state,
        "negotiate_redline",
        {
            "contract_id": contract_id,
            "changed_clause": "limitation_of_liability",
            "materiality_score": 0.7,
            "sender": "counterparty_counsel",
            "receiver": "internal_legal",
        },
    )
    state = redline["state"]
    supplier_event = receive_event(
        state,
        {"event_type": "SupplierQualified", "event_id": "evt-supplier", "supplier_name": "Acme Telecom", "qualified": True},
    )
    state = supplier_event["state"]
    risk = execute_operation(state, "score_contract_risk", {"contract_id": contract_id})
    state = risk["state"]
    approvals = execute_operation(
        state,
        "route_approval",
        {"contract_id": contract_id, "auto_approve": True, "requires_security_review": True},
    )
    state = approvals["state"]
    identity = receive_event(
        state,
        {"event_type": "IdentityVerified", "event_id": "evt-id", "contract_id": contract_id, "signer_name": "Aisha Grant", "verified": True},
    )
    state = identity["state"]
    signature = execute_operation(
        state,
        "capture_signature",
        {
            "contract_id": contract_id,
            "signer_name": "Aisha Grant",
            "signer_title": "Chief Commercial Officer",
            "authority_evidence": "board-resolution-42",
            "identity_verified": True,
        },
    )
    state = signature["state"]
    obligation = execute_operation(
        state,
        "activate_obligation",
        {
            "contract_id": contract_id,
            "obligation_code": "INSURANCE_CERT",
            "owner": "vendor.management",
            "due_date": "2026-08-01",
            "evidence_required": True,
        },
    )
    state = obligation["state"]
    obligation_id = obligation["rows"][0]["id"]
    performance = execute_operation(
        state,
        "record_obligation_performance",
        {
            "contract_id": contract_id,
            "obligation_id": obligation_id,
            "performed_by": "vendor.management",
            "evidence_uri": "s3://contracts/evidence/insurance-cert.pdf",
            "reviewed": True,
        },
    )
    state = performance["state"]
    renewal = execute_operation(
        state,
        "schedule_renewal",
        {"contract_id": contract_id, "renewal_decision": "renegotiate", "notice_days": 60},
    )
    state = renewal["state"]
    amendment = execute_operation(
        state,
        "execute_amendment",
        {"contract_id": contract_id, "effective_date": "2026-09-01", "change_summary": "Adjusted data processing appendix"},
    )
    state = amendment["state"]
    compliance = execute_operation(state, "run_compliance_check", {"contract_id": contract_id})
    state = compliance["state"]
    index = execute_operation(state, "index_contract_documents", {"contract_id": contract_id, "extra_terms": ("sla", "liability")})
    state = index["state"]
    impact = execute_operation(state, "simulate_counterparty_impact", {"contract_id": contract_id})
    return {
        "ok": all(
            item["ok"]
            for item in (
                config,
                rule,
                intake,
                classify,
                workspace,
                clause,
                redline,
                supplier_event,
                risk,
                approvals,
                identity,
                signature,
                obligation,
                performance,
                renewal,
                amendment,
                compliance,
                index,
                impact,
            )
        ),
        "state": state,
        "contract_id": contract_id,
        "steps": {
            "config": config,
            "rule": rule,
            "intake": intake,
            "classify": classify,
            "workspace": workspace,
            "clause": clause,
            "redline": redline,
            "risk": risk,
            "approvals": approvals,
            "signature": signature,
            "obligation": obligation,
            "performance": performance,
            "renewal": renewal,
            "amendment": amendment,
            "compliance": compliance,
            "index": index,
            "impact": impact,
        },
    }


def release_evidence() -> dict:
    scenario = release_scenario()
    workbench = render_workbench(scenario["state"])
    checks = (
        {"id": "schema_depth", "ok": len(OWNED_TABLES) >= 20},
        {"id": "domain_operation_depth", "ok": len(OPERATION_SPECS) >= 15},
        {"id": "rules_parameters_configuration_depth", "ok": len(RULE_DEFINITIONS) >= 6 and len(PARAMETER_DEFINITIONS) >= 6},
        {"id": "forms_wizards_controls_present", "ok": len(FORMS) >= 5 and len(WIZARDS) >= 3 and len(CONTROLS) >= 4},
        {"id": "event_contract_valid", "ok": validate_event_contract()["ok"]},
        {"id": "release_scenario", "ok": scenario["ok"]},
        {"id": "workbench_visibility", "ok": workbench["metrics"]["contracts_total"] >= 1},
        {"id": "boundary_proof", "ok": schema_boundary_check(OWNED_TABLES + CONSUMED_EVENTS)["ok"]},
        {"id": "agent_governed_crud", "ok": document_instruction_plan("renewal notice", "create renewal reminder for contract").get("ok") is True},
    )
    return {
        "format": "appgen.contract-lifecycle-release-evidence.v2",
        "ok": all(check["ok"] for check in checks),
        "pbc": PBC_KEY,
        "checks": checks,
        "scenario": scenario,
        "workbench": workbench,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
        "boundary_gaps": (),
    }


def runtime_capabilities() -> dict:
    evidence = release_evidence()
    return {
        "format": "appgen.contract-lifecycle-runtime-capabilities.v2",
        "ok": evidence["ok"],
        "pbc": PBC_KEY,
        "implementation_directory": "src/pyAppGen/pbcs/contract_lifecycle",
        "owned_tables": OWNED_TABLES,
        "allowed_database_backends": ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": REQUIRED_EVENT_TOPIC,
        "emits": tuple(dict.fromkeys(EMITTED_EVENTS + LEGACY_PUBLIC_EVENTS)),
        "consumes": CONSUMED_EVENTS,
        "operations": tuple(OPERATION_SPECS) + (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "register_schema_extension",
            "receive_event",
            "query_workbench",
            "build_workbench_view",
            "build_schema_contract",
            "build_service_contract",
            "build_release_evidence",
        ),
        "capabilities": ADVANCED_CAPABILITIES,
        "standard_features": (
            "contract_record_management",
            "contract_lifecycle_workflow",
            "contract_lifecycle_analytics",
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
        ),
        "smoke": evidence["scenario"],
    }


def query_workbench(state, filters=None) -> dict:
    workbench = render_workbench(state)
    filters = dict(filters or {})
    return {
        "ok": True,
        "read_only": True,
        "filters": filters,
        "records": tuple(state.get("contracts", {}).values())[: filters.get("limit", state.get("parameters", {}).get("workbench_limit", 25))],
        "workbench": workbench,
    }


class ContractLifecycleService:
    """Stateful service facade for the package-local one-PBC app."""

    def __init__(self, state=None):
        self.state = clone_state(state)

    def configure_runtime(self, config):
        result = configure_runtime(self.state, config)
        self.state = result["state"]
        return result

    def set_parameter(self, key, value):
        result = set_parameter(self.state, key, value)
        self.state = result["state"]
        return result

    def register_rule(self, rule):
        result = execute_operation(self.state, "compile_contract_rule", rule)
        self.state = result["state"]
        return result

    def register_schema_extension(self, table, fields):
        result = register_schema_extension(self.state, table, fields)
        self.state = result["state"]
        return result

    def receive_event(self, event):
        result = receive_event(self.state, event)
        self.state = result["state"]
        return result

    def query_workbench(self, filters=None):
        return query_workbench(self.state, filters)

    def build_workbench_view(self):
        return render_workbench(self.state)

    def execute(self, operation, payload=None):
        result = execute_operation(self.state, operation, payload)
        self.state = result["state"]
        return result

    def __getattr__(self, name):
        if name in OPERATION_SPECS:
            return lambda payload=None, _name=name: self.execute(_name, payload)
        raise AttributeError(name)
