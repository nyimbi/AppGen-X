"""Standalone one-PBC app surface for the master_data_governance package."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sqlite3
from typing import Any

from .domain_depth import DOMAIN_ADVANCED_CAPABILITIES, DOMAIN_CONSUMED_EVENTS, DOMAIN_EVENTS
from .manifest import PBC_MANIFEST

PBC_KEY = "master_data_governance"
PACKAGE_DIR = Path(__file__).resolve().parent
APPGEN_X_TOPIC = f"pbc.{PBC_KEY}.events"
ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb", "sqlite")
AGENT_NAME = "MasterDataGovernanceAgent"
PERMISSIONS = tuple(PBC_MANIFEST["permissions"] + (f"{PBC_KEY}.operate", f"{PBC_KEY}.audit"))
LEGACY_EMITTED_EVENTS = tuple(PBC_MANIFEST["emits"])
LEGACY_CONSUMED_EVENTS = tuple(PBC_MANIFEST["consumes"])
EMITTED_EVENTS = tuple(dict.fromkeys(tuple(DOMAIN_EVENTS) + LEGACY_EMITTED_EVENTS + (
    "DomainRegistered",
    "SourceRecordLinked",
    "ReferenceDataPublished",
    "RemediationQueued",
    "PolicyApprovalRecorded",
    "AuditProofRecorded",
    "LineageLinked",
)))
CONSUMED_EVENTS = tuple(dict.fromkeys(tuple(DOMAIN_CONSUMED_EVENTS) + LEGACY_CONSUMED_EVENTS))
CRUD_ACTIONS = ("create", "read", "update", "delete")

DOMAIN_TABLE = f"{PBC_KEY}_domain_registry"
SOURCE_TABLE = f"{PBC_KEY}_source_record"
GOLDEN_TABLE = f"{PBC_KEY}_golden_record"
SURVIVORSHIP_TABLE = f"{PBC_KEY}_survivorship_rule"
MATCH_TABLE = f"{PBC_KEY}_match_candidate"
MERGE_TABLE = f"{PBC_KEY}_merge_decision"
STEWARDSHIP_TABLE = f"{PBC_KEY}_stewardship_task"
QUALITY_RULE_TABLE = f"{PBC_KEY}_data_quality_rule"
REMEDIATION_TABLE = f"{PBC_KEY}_remediation_issue"
HIERARCHY_TABLE = f"{PBC_KEY}_hierarchy_node"
REFERENCE_TABLE = f"{PBC_KEY}_reference_data_item"
LINEAGE_TABLE = f"{PBC_KEY}_lineage_link"
POLICY_TABLE = f"{PBC_KEY}_policy_approval"
AUDIT_TABLE = f"{PBC_KEY}_audit_proof"
OUTBOX_TABLE = f"{PBC_KEY}_appgen_outbox_event"
INBOX_TABLE = f"{PBC_KEY}_appgen_inbox_event"
DEAD_LETTER_TABLE = f"{PBC_KEY}_appgen_dead_letter_event"

BUSINESS_TABLES = (
    DOMAIN_TABLE,
    SOURCE_TABLE,
    GOLDEN_TABLE,
    SURVIVORSHIP_TABLE,
    MATCH_TABLE,
    MERGE_TABLE,
    STEWARDSHIP_TABLE,
    QUALITY_RULE_TABLE,
    REMEDIATION_TABLE,
    HIERARCHY_TABLE,
    REFERENCE_TABLE,
    LINEAGE_TABLE,
    POLICY_TABLE,
    AUDIT_TABLE,
)
EVENT_TABLES = (OUTBOX_TABLE, INBOX_TABLE, DEAD_LETTER_TABLE)
RUNTIME_TABLES = BUSINESS_TABLES + EVENT_TABLES
TABLE_DESCRIPTIONS = {
    DOMAIN_TABLE: "Governed master-data domains and stewardship ownership.",
    SOURCE_TABLE: "Raw source-system records linked into MDM curation.",
    GOLDEN_TABLE: "Golden records ready for downstream publication.",
    SURVIVORSHIP_TABLE: "Explainable survivorship rules and precedence logic.",
    MATCH_TABLE: "Potential duplicate candidates and confidence evidence.",
    MERGE_TABLE: "Human-approved or pending merge outcomes.",
    STEWARDSHIP_TABLE: "Steward workflow items and escalation status.",
    QUALITY_RULE_TABLE: "Data quality rules with thresholds and ownership.",
    REMEDIATION_TABLE: "Remediation queue for data-quality and policy breaches.",
    HIERARCHY_TABLE: "Parent-child hierarchy nodes and lineage anchors.",
    REFERENCE_TABLE: "Curated reference-data values and change state.",
    LINEAGE_TABLE: "Source-to-golden lineage evidence and provenance links.",
    POLICY_TABLE: "Policy approvals and governance decision evidence.",
    AUDIT_TABLE: "Cryptographic audit proofs and release assertions.",
    OUTBOX_TABLE: "AppGen-X outbox events emitted by the standalone slice.",
    INBOX_TABLE: "AppGen-X inbox events consumed idempotently by the standalone slice.",
    DEAD_LETTER_TABLE: "Dead-letter events captured for rejected or exhausted messages.",
}

FORM_DEFINITIONS = (
    {
        "key": "DomainRegistryForm",
        "table": DOMAIN_TABLE,
        "operation": "register_domain",
        "fields": ("tenant", "domain_code", "label", "steward", "matching_strategy", "survivorship_policy"),
        "keywords": ("domain", "registry", "steward"),
    },
    {
        "key": "SourceRecordIntakeForm",
        "table": SOURCE_TABLE,
        "operation": "ingest_source_record",
        "fields": ("tenant", "domain_code", "source_system", "source_record_id", "entity_key", "attributes"),
        "keywords": ("source", "ingest", "dedupe", "entity"),
    },
    {
        "key": "MatchCandidateForm",
        "table": MATCH_TABLE,
        "operation": "create_match_candidate",
        "fields": ("tenant", "domain_code", "candidate_code", "left_record_code", "right_record_code", "confidence", "explanation"),
        "keywords": ("match", "duplicate", "dedupe"),
    },
    {
        "key": "MergeDecisionForm",
        "table": MERGE_TABLE,
        "operation": "approve_merge_decision",
        "fields": ("tenant", "decision_code", "candidate_code", "winning_record_code", "losing_record_code", "decision", "approved_by"),
        "keywords": ("merge", "survivorship", "winning"),
    },
    {
        "key": "GoldenRecordForm",
        "table": GOLDEN_TABLE,
        "operation": "publish_golden_record",
        "fields": ("tenant", "golden_code", "domain_code", "business_key", "winning_record_code", "published_by", "attributes"),
        "keywords": ("golden", "publish", "master"),
    },
    {
        "key": "SurvivorshipRuleForm",
        "table": SURVIVORSHIP_TABLE,
        "operation": "define_survivorship_rule",
        "fields": ("tenant", "rule_code", "domain_code", "attribute_name", "precedence", "fallback", "explanation"),
        "keywords": ("survivorship", "precedence", "winning attribute"),
    },
    {
        "key": "StewardshipTaskForm",
        "table": STEWARDSHIP_TABLE,
        "operation": "open_stewardship_task",
        "fields": ("tenant", "task_code", "domain_code", "queue", "assignee", "due_at", "reason"),
        "keywords": ("stewardship", "workflow", "queue", "assignee"),
    },
    {
        "key": "DataQualityRuleForm",
        "table": QUALITY_RULE_TABLE,
        "operation": "define_data_quality_rule",
        "fields": ("tenant", "rule_code", "domain_code", "metric", "threshold", "severity", "owner"),
        "keywords": ("quality", "rule", "threshold"),
    },
    {
        "key": "RemediationQueueForm",
        "table": REMEDIATION_TABLE,
        "operation": "queue_remediation_issue",
        "fields": ("tenant", "issue_code", "domain_code", "queue", "severity", "record_code", "remediation_owner"),
        "keywords": ("remediation", "issue", "exception", "queue"),
    },
    {
        "key": "HierarchyNodeForm",
        "table": HIERARCHY_TABLE,
        "operation": "upsert_hierarchy_node",
        "fields": ("tenant", "node_code", "domain_code", "parent_code", "label", "node_type"),
        "keywords": ("hierarchy", "parent", "child"),
    },
    {
        "key": "ReferenceDataForm",
        "table": REFERENCE_TABLE,
        "operation": "register_reference_data",
        "fields": ("tenant", "value_code", "domain_code", "set_name", "label", "status"),
        "keywords": ("reference", "lookup", "taxonomy"),
    },
    {
        "key": "LineageLinkForm",
        "table": LINEAGE_TABLE,
        "operation": "capture_lineage_link",
        "fields": ("tenant", "lineage_code", "source_record_code", "golden_record_code", "transformation", "evidence"),
        "keywords": ("lineage", "provenance", "evidence"),
    },
    {
        "key": "PolicyApprovalForm",
        "table": POLICY_TABLE,
        "operation": "approve_policy",
        "fields": ("tenant", "approval_code", "policy_name", "status", "approved_by", "rationale"),
        "keywords": ("policy", "approval", "governance"),
    },
    {
        "key": "AuditProofForm",
        "table": AUDIT_TABLE,
        "operation": "record_audit_proof",
        "fields": ("tenant", "proof_code", "artifact_type", "artifact_code", "proof_hash", "attested_by"),
        "keywords": ("audit", "proof", "release", "evidence"),
    },
    {
        "key": "AgentDocumentPlanForm",
        "table": DOMAIN_TABLE,
        "operation": "document_instruction_plan",
        "fields": ("document", "instructions"),
        "keywords": ("document", "instruction", "plan", "crud"),
    },
)
FORM_KEYS = tuple(item["key"] for item in FORM_DEFINITIONS)

WIZARD_DEFINITIONS = (
    {
        "key": "DomainRegistryWizard",
        "title": "Domain registry onboarding",
        "steps": ("domain", "stewardship", "policy", "quality"),
        "forms": ("DomainRegistryForm", "PolicyApprovalForm", "DataQualityRuleForm"),
        "keywords": ("domain", "registry", "governance"),
    },
    {
        "key": "GoldenRecordCurationWizard",
        "title": "Golden record curation",
        "steps": ("source_intake", "matching", "survivorship", "publish"),
        "forms": ("SourceRecordIntakeForm", "MatchCandidateForm", "SurvivorshipRuleForm", "GoldenRecordForm"),
        "keywords": ("golden", "publish", "survivorship", "source"),
    },
    {
        "key": "MatchMergeResolutionWizard",
        "title": "Match and merge resolution",
        "steps": ("candidate_review", "merge_decision", "lineage", "audit"),
        "forms": ("MatchCandidateForm", "MergeDecisionForm", "LineageLinkForm", "AuditProofForm"),
        "keywords": ("match", "merge", "duplicate", "dedupe"),
    },
    {
        "key": "StewardshipRemediationWizard",
        "title": "Stewardship remediation",
        "steps": ("issue_intake", "task_assignment", "policy_check", "closure_proof"),
        "forms": ("RemediationQueueForm", "StewardshipTaskForm", "PolicyApprovalForm", "AuditProofForm"),
        "keywords": ("stewardship", "remediation", "issue", "exception"),
    },
    {
        "key": "HierarchyGovernanceWizard",
        "title": "Hierarchy governance",
        "steps": ("reference_data", "hierarchy", "lineage", "publish"),
        "forms": ("ReferenceDataForm", "HierarchyNodeForm", "LineageLinkForm", "GoldenRecordForm"),
        "keywords": ("hierarchy", "reference", "taxonomy", "lineage"),
    },
    {
        "key": "AgentDocumentIntakeWizard",
        "title": "Agent document intake",
        "steps": ("analyze_document", "select_routes", "preview_crud", "request_approval"),
        "forms": ("AgentDocumentPlanForm", "DomainRegistryForm", "GoldenRecordForm", "RemediationQueueForm"),
        "keywords": ("document", "instruction", "crud", "assistant"),
    },
)
WIZARD_KEYS = tuple(item["key"] for item in WIZARD_DEFINITIONS)

CONTROL_DEFINITIONS = (
    {"key": "WorkbenchSummaryCards", "type": "cards", "targets": (DOMAIN_TABLE, GOLDEN_TABLE, MATCH_TABLE, REMEDIATION_TABLE)},
    {"key": "MatchQueueControl", "type": "queue", "targets": (MATCH_TABLE, MERGE_TABLE)},
    {"key": "StewardshipWorkflowControl", "type": "queue", "targets": (STEWARDSHIP_TABLE, REMEDIATION_TABLE)},
    {"key": "HierarchyManagerControl", "type": "graph", "targets": (HIERARCHY_TABLE, REFERENCE_TABLE)},
    {"key": "LineageExplorerControl", "type": "lineage", "targets": (SOURCE_TABLE, GOLDEN_TABLE, LINEAGE_TABLE)},
    {"key": "PolicyApprovalControl", "type": "approval", "targets": (POLICY_TABLE, AUDIT_TABLE)},
    {"key": "AuditProofControl", "type": "evidence", "targets": (AUDIT_TABLE, OUTBOX_TABLE, DEAD_LETTER_TABLE)},
)
CONTROL_KEYS = tuple(item["key"] for item in CONTROL_DEFINITIONS)

ROUTE_DEFINITIONS = (
    {"method": "POST", "path": "/app/master-data-governance/domains", "handler": "register_domain", "operation": "register_domain", "operation_kind": "command", "table": DOMAIN_TABLE, "permission": f"{PBC_KEY}.create", "form": "DomainRegistryForm", "wizard": "DomainRegistryWizard", "keywords": ("domain", "registry")},
    {"method": "POST", "path": "/app/master-data-governance/source-records", "handler": "ingest_source_record", "operation": "ingest_source_record", "operation_kind": "command", "table": SOURCE_TABLE, "permission": f"{PBC_KEY}.create", "form": "SourceRecordIntakeForm", "wizard": "GoldenRecordCurationWizard", "keywords": ("source", "entity", "ingest")},
    {"method": "POST", "path": "/app/master-data-governance/match-candidates", "handler": "create_match_candidate", "operation": "create_match_candidate", "operation_kind": "command", "table": MATCH_TABLE, "permission": f"{PBC_KEY}.update", "form": "MatchCandidateForm", "wizard": "MatchMergeResolutionWizard", "keywords": ("match", "duplicate", "dedupe")},
    {"method": "POST", "path": "/app/master-data-governance/merge-decisions", "handler": "approve_merge_decision", "operation": "approve_merge_decision", "operation_kind": "command", "table": MERGE_TABLE, "permission": f"{PBC_KEY}.approve", "form": "MergeDecisionForm", "wizard": "MatchMergeResolutionWizard", "keywords": ("merge", "winning", "survivorship")},
    {"method": "POST", "path": "/app/master-data-governance/golden-records", "handler": "publish_golden_record", "operation": "publish_golden_record", "operation_kind": "command", "table": GOLDEN_TABLE, "permission": f"{PBC_KEY}.approve", "form": "GoldenRecordForm", "wizard": "GoldenRecordCurationWizard", "keywords": ("golden", "master", "publish")},
    {"method": "POST", "path": "/app/master-data-governance/survivorship-rules", "handler": "define_survivorship_rule", "operation": "define_survivorship_rule", "operation_kind": "command", "table": SURVIVORSHIP_TABLE, "permission": f"{PBC_KEY}.update", "form": "SurvivorshipRuleForm", "wizard": "GoldenRecordCurationWizard", "keywords": ("survivorship", "precedence")},
    {"method": "POST", "path": "/app/master-data-governance/stewardship-tasks", "handler": "open_stewardship_task", "operation": "open_stewardship_task", "operation_kind": "command", "table": STEWARDSHIP_TABLE, "permission": f"{PBC_KEY}.update", "form": "StewardshipTaskForm", "wizard": "StewardshipRemediationWizard", "keywords": ("stewardship", "task", "workflow")},
    {"method": "POST", "path": "/app/master-data-governance/quality-rules", "handler": "define_data_quality_rule", "operation": "define_data_quality_rule", "operation_kind": "command", "table": QUALITY_RULE_TABLE, "permission": f"{PBC_KEY}.update", "form": "DataQualityRuleForm", "wizard": "DomainRegistryWizard", "keywords": ("quality", "threshold", "rule")},
    {"method": "POST", "path": "/app/master-data-governance/remediation-issues", "handler": "queue_remediation_issue", "operation": "queue_remediation_issue", "operation_kind": "command", "table": REMEDIATION_TABLE, "permission": f"{PBC_KEY}.update", "form": "RemediationQueueForm", "wizard": "StewardshipRemediationWizard", "keywords": ("remediation", "issue", "exception")},
    {"method": "POST", "path": "/app/master-data-governance/hierarchy-nodes", "handler": "upsert_hierarchy_node", "operation": "upsert_hierarchy_node", "operation_kind": "command", "table": HIERARCHY_TABLE, "permission": f"{PBC_KEY}.update", "form": "HierarchyNodeForm", "wizard": "HierarchyGovernanceWizard", "keywords": ("hierarchy", "parent", "child")},
    {"method": "POST", "path": "/app/master-data-governance/reference-data", "handler": "register_reference_data", "operation": "register_reference_data", "operation_kind": "command", "table": REFERENCE_TABLE, "permission": f"{PBC_KEY}.update", "form": "ReferenceDataForm", "wizard": "HierarchyGovernanceWizard", "keywords": ("reference", "lookup", "taxonomy")},
    {"method": "POST", "path": "/app/master-data-governance/lineage-links", "handler": "capture_lineage_link", "operation": "capture_lineage_link", "operation_kind": "command", "table": LINEAGE_TABLE, "permission": f"{PBC_KEY}.update", "form": "LineageLinkForm", "wizard": "MatchMergeResolutionWizard", "keywords": ("lineage", "provenance", "audit")},
    {"method": "POST", "path": "/app/master-data-governance/policy-approvals", "handler": "approve_policy", "operation": "approve_policy", "operation_kind": "command", "table": POLICY_TABLE, "permission": f"{PBC_KEY}.approve", "form": "PolicyApprovalForm", "wizard": "DomainRegistryWizard", "keywords": ("policy", "approval", "governance")},
    {"method": "POST", "path": "/app/master-data-governance/audit-proofs", "handler": "record_audit_proof", "operation": "record_audit_proof", "operation_kind": "command", "table": AUDIT_TABLE, "permission": f"{PBC_KEY}.audit", "form": "AuditProofForm", "wizard": "StewardshipRemediationWizard", "keywords": ("audit", "proof", "release")},
    {"method": "POST", "path": "/app/master-data-governance/seed-bundle", "handler": "load_seed_bundle", "operation": "load_seed_bundle", "operation_kind": "command", "table": DOMAIN_TABLE, "permission": f"{PBC_KEY}.admin", "form": "DomainRegistryForm", "wizard": "DomainRegistryWizard", "keywords": ("seed", "demo", "bundle")},
    {"method": "POST", "path": "/app/master-data-governance/agent/document-plan", "handler": "document_instruction_plan", "operation": "document_instruction_plan", "operation_kind": "query", "table": DOMAIN_TABLE, "permission": f"{PBC_KEY}.read", "form": "AgentDocumentPlanForm", "wizard": "AgentDocumentIntakeWizard", "keywords": ("document", "instruction", "plan")},
    {"method": "POST", "path": "/app/master-data-governance/agent/crud-plan", "handler": "datastore_crud_plan", "operation": "datastore_crud_plan", "operation_kind": "query", "table": DOMAIN_TABLE, "permission": f"{PBC_KEY}.read", "form": "AgentDocumentPlanForm", "wizard": "AgentDocumentIntakeWizard", "keywords": ("crud", "mutation", "read")},
    {"method": "GET", "path": "/app/master-data-governance/workbench", "handler": "query_workbench", "operation": "query_workbench", "operation_kind": "query", "table": DOMAIN_TABLE, "permission": f"{PBC_KEY}.read", "form": None, "wizard": None, "keywords": ("workbench", "dashboard", "queue")},
)

SEED_BUNDLE = (
    {"operation": "register_domain", "payload": {"domain_code": "CUSTOMER_PARTY", "label": "Customer Party", "steward": "alice.mdm", "matching_strategy": "probabilistic", "survivorship_policy": "trusted_source_then_recency"}},
    {"operation": "ingest_source_record", "payload": {"domain_code": "CUSTOMER_PARTY", "source_system": "crm", "source_record_id": "crm-100", "entity_key": "CUST-100", "attributes": {"name": "Acme Holdings", "email": "ops@acme.example", "country": "KE"}}},
    {"operation": "ingest_source_record", "payload": {"domain_code": "CUSTOMER_PARTY", "source_system": "erp", "source_record_id": "erp-900", "entity_key": "CUST-100", "attributes": {"name": "ACME Holdings Ltd", "email": "finance@acme.example", "country": "KE"}}},
    {"operation": "create_match_candidate", "payload": {"domain_code": "CUSTOMER_PARTY", "candidate_code": "MATCH-ACME-100", "left_record_code": "CRM-100", "right_record_code": "ERP-900", "confidence": 0.94, "explanation": "same business key and jurisdiction"}},
    {"operation": "define_survivorship_rule", "payload": {"rule_code": "SURV-TRUST-RECENCY", "domain_code": "CUSTOMER_PARTY", "attribute_name": "email", "precedence": ("trusted_source", "recency"), "fallback": "steward_review", "explanation": "Prefer trusted source system, otherwise latest verified attribute."}},
    {"operation": "approve_merge_decision", "payload": {"decision_code": "MERGE-ACME-100", "candidate_code": "MATCH-ACME-100", "winning_record_code": "CRM-100", "losing_record_code": "ERP-900", "decision": "merge", "approved_by": "steward.alice"}},
    {"operation": "publish_golden_record", "payload": {"golden_code": "GOLD-ACME-100", "domain_code": "CUSTOMER_PARTY", "business_key": "CUST-100", "winning_record_code": "CRM-100", "published_by": "steward.alice", "attributes": {"name": "Acme Holdings", "email": "ops@acme.example", "country": "KE"}}},
    {"operation": "define_data_quality_rule", "payload": {"rule_code": "DQ-CUST-EMAIL", "domain_code": "CUSTOMER_PARTY", "metric": "email_completeness", "threshold": 0.98, "severity": "high", "owner": "quality.alice"}},
    {"operation": "queue_remediation_issue", "payload": {"issue_code": "ISSUE-EMAIL-100", "domain_code": "CUSTOMER_PARTY", "queue": "quality_remediation", "severity": "high", "record_code": "ERP-900", "remediation_owner": "quality.alice"}},
    {"operation": "open_stewardship_task", "payload": {"task_code": "TASK-ACME-VERIFY", "domain_code": "CUSTOMER_PARTY", "queue": "merge_review", "assignee": "steward.alice", "due_at": "2026-06-03T09:00:00+00:00", "reason": "verify merge before downstream sync"}},
    {"operation": "register_reference_data", "payload": {"value_code": "REF-CUST-TIER-GOLD", "domain_code": "CUSTOMER_PARTY", "set_name": "customer_tier", "label": "Gold", "status": "active"}},
    {"operation": "upsert_hierarchy_node", "payload": {"node_code": "NODE-ACME-GROUP", "domain_code": "CUSTOMER_PARTY", "parent_code": None, "label": "Acme Group", "node_type": "organization"}},
    {"operation": "capture_lineage_link", "payload": {"lineage_code": "LIN-ACME-100", "source_record_code": "CRM-100", "golden_record_code": "GOLD-ACME-100", "transformation": "merge_and_survive", "evidence": "rule SURV-TRUST-RECENCY"}},
    {"operation": "approve_policy", "payload": {"approval_code": "POLICY-MDM-001", "policy_name": "golden_record_publication", "status": "approved", "approved_by": "governance.council", "rationale": "evidence bundle satisfied"}},
    {"operation": "record_audit_proof", "payload": {"proof_code": "PROOF-ACME-100", "artifact_type": "golden_record_release", "artifact_code": "GOLD-ACME-100", "proof_hash": "sha256:acme-golden-proof", "attested_by": "audit.bot"}},
)


@dataclass(frozen=True)
class TableSpec:
    table: str
    category: str
    description: str


TABLE_SPECS = tuple(TableSpec(table=table, category=("event" if table in EVENT_TABLES else "business"), description=TABLE_DESCRIPTIONS[table]) for table in RUNTIME_TABLES)


_OPERATION_EVENTS = {
    "register_domain": "DomainRegistered",
    "ingest_source_record": "SourceRecordLinked",
    "create_match_candidate": "MatchCandidateGenerated",
    "approve_merge_decision": "MergeDecisionApproved",
    "publish_golden_record": "GoldenRecordPublished",
    "define_survivorship_rule": "DataQualityChanged",
    "open_stewardship_task": "StewardshipTaskOpened",
    "define_data_quality_rule": "DataQualityChanged",
    "queue_remediation_issue": "RemediationQueued",
    "upsert_hierarchy_node": "HierarchyChanged",
    "register_reference_data": "ReferenceDataPublished",
    "capture_lineage_link": "LineageLinked",
    "approve_policy": "PolicyApprovalRecorded",
    "record_audit_proof": "AuditProofRecorded",
}


def _utcnow() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _digest(value: Any) -> str:
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()


def _json_dump(value: Any) -> str:
    return json.dumps(value, sort_keys=True, default=str)


def _json_load(value: str | None) -> Any:
    if not value:
        return {}
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return {"raw": value}


def _slug(value: Any) -> str:
    text = str(value or "")
    cleaned = []
    for char in text:
        cleaned.append(char if char.isalnum() else "-")
    normalized = "".join(cleaned).strip("-")
    while "--" in normalized:
        normalized = normalized.replace("--", "-")
    return normalized.lower() or "item"


class SQLiteOwnedRepository:
    """Package-local SQLite store for standalone MDM workflows."""

    def __init__(self, database_url: str = ":memory:") -> None:
        self.database_url = database_url
        self.connection = sqlite3.connect(database_url)
        self.connection.row_factory = sqlite3.Row

    def bootstrap(self) -> None:
        for table in BUSINESS_TABLES:
            self.connection.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {table} (
                    id TEXT PRIMARY KEY NOT NULL,
                    tenant TEXT NOT NULL,
                    code TEXT NOT NULL,
                    status TEXT NOT NULL,
                    payload TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
                """
            )
        for table in EVENT_TABLES:
            self.connection.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {table} (
                    id TEXT PRIMARY KEY NOT NULL,
                    tenant TEXT NOT NULL,
                    code TEXT NOT NULL,
                    status TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    idempotency_key TEXT NOT NULL,
                    payload TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
                """
            )
            self.connection.execute(
                f"CREATE UNIQUE INDEX IF NOT EXISTS idx_{table}_idempotency ON {table} (idempotency_key)"
            )
        self.connection.commit()

    def insert_business(self, table: str, *, tenant: str, code: str, status: str, payload: dict[str, Any]) -> dict[str, Any]:
        now = _utcnow()
        record = {
            "id": f"{table}:{_slug(code)}:{_digest((tenant, code, payload))[:10]}",
            "tenant": tenant,
            "code": code,
            "status": status,
            "payload": _json_dump(payload),
            "created_at": now,
            "updated_at": now,
        }
        self.connection.execute(
            f"INSERT INTO {table} (id, tenant, code, status, payload, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
            tuple(record[field] for field in ("id", "tenant", "code", "status", "payload", "created_at", "updated_at")),
        )
        self.connection.commit()
        return self.fetch_by_id(table, record["id"])

    def insert_event(
        self,
        table: str,
        *,
        tenant: str,
        code: str,
        status: str,
        event_type: str,
        idempotency_key: str,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        now = _utcnow()
        record = {
            "id": f"{table}:{_slug(code)}:{_digest((event_type, idempotency_key))[:10]}",
            "tenant": tenant,
            "code": code,
            "status": status,
            "event_type": event_type,
            "idempotency_key": idempotency_key,
            "payload": _json_dump(payload),
            "created_at": now,
            "updated_at": now,
        }
        self.connection.execute(
            f"INSERT OR IGNORE INTO {table} (id, tenant, code, status, event_type, idempotency_key, payload, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            tuple(record[field] for field in ("id", "tenant", "code", "status", "event_type", "idempotency_key", "payload", "created_at", "updated_at")),
        )
        self.connection.commit()
        row = self.connection.execute(
            f"SELECT * FROM {table} WHERE idempotency_key = ? LIMIT 1",
            (idempotency_key,),
        ).fetchone()
        return self._row_to_dict(row) if row is not None else record

    def fetch_by_id(self, table: str, record_id: str) -> dict[str, Any]:
        row = self.connection.execute(f"SELECT * FROM {table} WHERE id = ?", (record_id,)).fetchone()
        if row is None:
            raise KeyError(record_id)
        return self._row_to_dict(row)

    def fetch_all(self, table: str, *, tenant: str | None = None, limit: int | None = None, status: str | None = None) -> tuple[dict[str, Any], ...]:
        sql = f"SELECT * FROM {table}"
        values: list[Any] = []
        clauses = []
        if tenant is not None:
            clauses.append("tenant = ?")
            values.append(tenant)
        if status is not None:
            clauses.append("status = ?")
            values.append(status)
        if clauses:
            sql += " WHERE " + " AND ".join(clauses)
        sql += " ORDER BY created_at DESC"
        if limit is not None:
            sql += f" LIMIT {int(limit)}"
        rows = self.connection.execute(sql, tuple(values)).fetchall()
        return tuple(self._row_to_dict(row) for row in rows)

    def count(self, table: str, *, tenant: str | None = None, status: str | None = None) -> int:
        sql = f"SELECT COUNT(1) AS total FROM {table}"
        values: list[Any] = []
        clauses = []
        if tenant is not None:
            clauses.append("tenant = ?")
            values.append(tenant)
        if status is not None:
            clauses.append("status = ?")
            values.append(status)
        if clauses:
            sql += " WHERE " + " AND ".join(clauses)
        row = self.connection.execute(sql, tuple(values)).fetchone()
        return int(row["total"]) if row is not None else 0

    def has_idempotency_key(self, idempotency_key: str) -> bool:
        for table in EVENT_TABLES:
            row = self.connection.execute(
                f"SELECT 1 FROM {table} WHERE idempotency_key = ? LIMIT 1",
                (idempotency_key,),
            ).fetchone()
            if row is not None:
                return True
        return False

    def close(self) -> None:
        self.connection.close()

    @staticmethod
    def _row_to_dict(row: sqlite3.Row) -> dict[str, Any]:
        record = dict(row)
        if "payload" in record:
            record["payload"] = _json_load(record["payload"])
        return record


class MasterDataGovernanceStandaloneService:
    """Executable service facade for standalone MDM workflows."""

    def __init__(self, store: SQLiteOwnedRepository | None = None, database_url: str = ":memory:") -> None:
        self._owns_store = store is None
        self.store = store or SQLiteOwnedRepository(database_url=database_url)
        self.store.bootstrap()
        self.configuration = {
            "database_backend": "sqlite",
            "database_url": database_url,
            "event_topic": APPGEN_X_TOPIC,
            "event_contract": "AppGen-X",
        }

    def close(self) -> None:
        if self._owns_store:
            self.store.close()

    def configure_runtime(self, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = dict(payload or {})
        backend = payload.get("database_backend", self.configuration["database_backend"])
        topic = payload.get("event_topic", self.configuration["event_topic"])
        ok = backend in ALLOWED_DATABASE_BACKENDS and topic == APPGEN_X_TOPIC
        if ok:
            self.configuration.update({"database_backend": backend, "event_topic": topic})
        return {"ok": ok, "configuration": dict(self.configuration), "side_effects": ()}

    def receive_event(self, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = dict(payload or {})
        tenant = str(payload.get("tenant") or "default")
        event_type = str(payload.get("event_type") or "UnknownEvent")
        event_id = str(payload.get("event_id") or _digest(payload)[:12])
        idempotency_key = str(payload.get("idempotency_key") or f"{PBC_KEY}:{event_type}:{event_id}")
        if self.store.has_idempotency_key(idempotency_key):
            return {"ok": True, "duplicate": True, "event_type": event_type, "idempotency_key": idempotency_key, "side_effects": ()}
        target_table = INBOX_TABLE if event_type in CONSUMED_EVENTS else DEAD_LETTER_TABLE
        status = "processed" if target_table == INBOX_TABLE else "dead_letter"
        record = self.store.insert_event(
            target_table,
            tenant=tenant,
            code=event_id,
            status=status,
            event_type=event_type,
            idempotency_key=idempotency_key,
            payload=payload,
        )
        return {
            "ok": target_table == INBOX_TABLE,
            "duplicate": False,
            "event_type": event_type,
            "record": record,
            "target_table": target_table,
            "side_effects": (),
        }

    def register_domain(self, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = dict(payload or {})
        record = self._insert_domain_record(
            DOMAIN_TABLE,
            payload,
            code=payload.get("domain_code"),
            status="active",
            event_type=_OPERATION_EVENTS["register_domain"],
        )
        return {"ok": True, "operation": "register_domain", "record": record, "side_effects": ()}

    def ingest_source_record(self, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = dict(payload or {})
        code = payload.get("source_record_id") or payload.get("entity_key") or payload.get("code")
        record = self._insert_domain_record(
            SOURCE_TABLE,
            payload,
            code=code,
            status="ingested",
            event_type=_OPERATION_EVENTS["ingest_source_record"],
        )
        return {"ok": True, "operation": "ingest_source_record", "record": record, "side_effects": ()}

    def create_match_candidate(self, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = dict(payload or {})
        record = self._insert_domain_record(
            MATCH_TABLE,
            payload,
            code=payload.get("candidate_code") or payload.get("code"),
            status="open",
            event_type=_OPERATION_EVENTS["create_match_candidate"],
        )
        return {"ok": True, "operation": "create_match_candidate", "record": record, "side_effects": ()}

    def approve_merge_decision(self, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = dict(payload or {})
        record = self._insert_domain_record(
            MERGE_TABLE,
            payload,
            code=payload.get("decision_code") or payload.get("candidate_code") or payload.get("code"),
            status=str(payload.get("decision") or "approved"),
            event_type=_OPERATION_EVENTS["approve_merge_decision"],
        )
        return {"ok": True, "operation": "approve_merge_decision", "record": record, "side_effects": ()}

    def publish_golden_record(self, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = dict(payload or {})
        record = self._insert_domain_record(
            GOLDEN_TABLE,
            payload,
            code=payload.get("golden_code") or payload.get("business_key") or payload.get("code"),
            status="published",
            event_type=_OPERATION_EVENTS["publish_golden_record"],
        )
        if payload.get("winning_record_code"):
            self.capture_lineage_link(
                {
                    "tenant": record["tenant"],
                    "lineage_code": f"lineage-{record['code']}",
                    "source_record_code": payload.get("winning_record_code"),
                    "golden_record_code": record["code"],
                    "transformation": payload.get("transformation", "publish_golden_record"),
                    "evidence": payload.get("published_by", "system"),
                }
            )
        return {"ok": True, "operation": "publish_golden_record", "record": record, "side_effects": ()}

    def define_survivorship_rule(self, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = dict(payload or {})
        record = self._insert_domain_record(
            SURVIVORSHIP_TABLE,
            payload,
            code=payload.get("rule_code") or payload.get("code"),
            status="active",
            event_type=_OPERATION_EVENTS["define_survivorship_rule"],
        )
        return {"ok": True, "operation": "define_survivorship_rule", "record": record, "side_effects": ()}

    def open_stewardship_task(self, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = dict(payload or {})
        record = self._insert_domain_record(
            STEWARDSHIP_TABLE,
            payload,
            code=payload.get("task_code") or payload.get("code"),
            status="open",
            event_type=_OPERATION_EVENTS["open_stewardship_task"],
        )
        return {"ok": True, "operation": "open_stewardship_task", "record": record, "side_effects": ()}

    def define_data_quality_rule(self, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = dict(payload or {})
        record = self._insert_domain_record(
            QUALITY_RULE_TABLE,
            payload,
            code=payload.get("rule_code") or payload.get("code"),
            status="active",
            event_type=_OPERATION_EVENTS["define_data_quality_rule"],
        )
        return {"ok": True, "operation": "define_data_quality_rule", "record": record, "side_effects": ()}

    def queue_remediation_issue(self, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = dict(payload or {})
        record = self._insert_domain_record(
            REMEDIATION_TABLE,
            payload,
            code=payload.get("issue_code") or payload.get("code"),
            status="open",
            event_type=_OPERATION_EVENTS["queue_remediation_issue"],
        )
        return {"ok": True, "operation": "queue_remediation_issue", "record": record, "side_effects": ()}

    def upsert_hierarchy_node(self, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = dict(payload or {})
        record = self._insert_domain_record(
            HIERARCHY_TABLE,
            payload,
            code=payload.get("node_code") or payload.get("code"),
            status="active",
            event_type=_OPERATION_EVENTS["upsert_hierarchy_node"],
        )
        return {"ok": True, "operation": "upsert_hierarchy_node", "record": record, "side_effects": ()}

    def register_reference_data(self, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = dict(payload or {})
        record = self._insert_domain_record(
            REFERENCE_TABLE,
            payload,
            code=payload.get("value_code") or payload.get("code"),
            status=str(payload.get("status") or "active"),
            event_type=_OPERATION_EVENTS["register_reference_data"],
        )
        return {"ok": True, "operation": "register_reference_data", "record": record, "side_effects": ()}

    def capture_lineage_link(self, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = dict(payload or {})
        record = self._insert_domain_record(
            LINEAGE_TABLE,
            payload,
            code=payload.get("lineage_code") or payload.get("code"),
            status="linked",
            event_type=_OPERATION_EVENTS["capture_lineage_link"],
        )
        return {"ok": True, "operation": "capture_lineage_link", "record": record, "side_effects": ()}

    def approve_policy(self, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = dict(payload or {})
        record = self._insert_domain_record(
            POLICY_TABLE,
            payload,
            code=payload.get("approval_code") or payload.get("policy_name") or payload.get("code"),
            status=str(payload.get("status") or "approved"),
            event_type=_OPERATION_EVENTS["approve_policy"],
        )
        return {"ok": True, "operation": "approve_policy", "record": record, "side_effects": ()}

    def record_audit_proof(self, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = dict(payload or {})
        record = self._insert_domain_record(
            AUDIT_TABLE,
            payload,
            code=payload.get("proof_code") or payload.get("artifact_code") or payload.get("code"),
            status="recorded",
            event_type=_OPERATION_EVENTS["record_audit_proof"],
        )
        return {"ok": True, "operation": "record_audit_proof", "record": record, "side_effects": ()}

    def query_workbench(self, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = dict(payload or {})
        tenant = str(payload.get("tenant") or "default")
        summary = {
            "domains": self.store.count(DOMAIN_TABLE, tenant=tenant),
            "source_records": self.store.count(SOURCE_TABLE, tenant=tenant),
            "golden_records": self.store.count(GOLDEN_TABLE, tenant=tenant),
            "match_queue": self.store.count(MATCH_TABLE, tenant=tenant, status="open"),
            "merge_decisions": self.store.count(MERGE_TABLE, tenant=tenant),
            "stewardship_open": self.store.count(STEWARDSHIP_TABLE, tenant=tenant, status="open"),
            "quality_rules": self.store.count(QUALITY_RULE_TABLE, tenant=tenant),
            "remediation_open": self.store.count(REMEDIATION_TABLE, tenant=tenant, status="open"),
            "hierarchy_nodes": self.store.count(HIERARCHY_TABLE, tenant=tenant),
            "reference_values": self.store.count(REFERENCE_TABLE, tenant=tenant),
            "lineage_links": self.store.count(LINEAGE_TABLE, tenant=tenant),
            "policy_pending": self.store.count(POLICY_TABLE, tenant=tenant, status="pending"),
            "audit_proofs": self.store.count(AUDIT_TABLE, tenant=tenant),
            "outbox_events": self.store.count(OUTBOX_TABLE, tenant=tenant),
            "dead_letters": self.store.count(DEAD_LETTER_TABLE, tenant=tenant),
        }
        workbench = {
            "tenant": tenant,
            "summary": summary,
            "queues": {
                "match_candidates": self.store.fetch_all(MATCH_TABLE, tenant=tenant, limit=5),
                "stewardship_tasks": self.store.fetch_all(STEWARDSHIP_TABLE, tenant=tenant, limit=5),
                "remediation_queue": self.store.fetch_all(REMEDIATION_TABLE, tenant=tenant, limit=5),
                "pending_policy_approvals": self.store.fetch_all(POLICY_TABLE, tenant=tenant, status="pending", limit=5),
            },
            "records": {
                "domains": self.store.fetch_all(DOMAIN_TABLE, tenant=tenant, limit=10),
                "golden_records": self.store.fetch_all(GOLDEN_TABLE, tenant=tenant, limit=10),
                "reference_data": self.store.fetch_all(REFERENCE_TABLE, tenant=tenant, limit=10),
                "hierarchy_nodes": self.store.fetch_all(HIERARCHY_TABLE, tenant=tenant, limit=10),
                "lineage_links": self.store.fetch_all(LINEAGE_TABLE, tenant=tenant, limit=10),
                "audit_proofs": self.store.fetch_all(AUDIT_TABLE, tenant=tenant, limit=10),
            },
            "controls": master_data_governance_control_catalog()["contracts"],
            "routes": tuple(f"{item['method']} {item['path']}" for item in ROUTE_DEFINITIONS),
            "forms": FORM_KEYS,
            "wizards": WIZARD_KEYS,
            "ui_fragments": (
                "MasterDataGovernanceWorkbench",
                "MasterDataGovernanceDetail",
                "MasterDataGovernanceAssistantPanel",
            ),
        }
        return {"ok": True, "operation": "query_workbench", "result": workbench, "side_effects": ()}

    def document_instruction_plan(self, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = dict(payload or {})
        return build_document_instruction_plan(payload.get("document"), payload.get("instructions"))

    def datastore_crud_plan(self, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = dict(payload or {})
        return build_datastore_crud_plan(payload.get("action", "read"), payload.get("table"), payload.get("payload"))

    def load_seed_bundle(self, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = dict(payload or {})
        tenant = str(payload.get("tenant") or "tenant_seed")
        executed = []
        for item in SEED_BUNDLE:
            handler = getattr(self, item["operation"])
            request = {"tenant": tenant, **dict(item["payload"])}
            executed.append(handler(request))
        return {"ok": all(item.get("ok") is True for item in executed), "tenant": tenant, "executed": tuple(executed), "side_effects": ()}

    def _insert_domain_record(
        self,
        table: str,
        payload: dict[str, Any],
        *,
        code: Any,
        status: str,
        event_type: str,
    ) -> dict[str, Any]:
        tenant = str(payload.get("tenant") or "default")
        record_code = str(code or f"{table.split('_')[-1]}-{_digest(payload)[:8]}").upper()
        record = self.store.insert_business(
            table,
            tenant=tenant,
            code=record_code,
            status=status,
            payload={**payload, "event_contract": "AppGen-X", "table": table},
        )
        self.store.insert_event(
            OUTBOX_TABLE,
            tenant=tenant,
            code=record_code,
            status="planned",
            event_type=event_type,
            idempotency_key=f"{PBC_KEY}:{event_type}:{record_code}",
            payload={"table": table, "record_code": record_code, "payload": record["payload"]},
        )
        return record


class MasterDataGovernanceStandaloneApp:
    """Live package-local app shell for the standalone slice."""

    def __init__(self, database_url: str = ":memory:") -> None:
        self.service = MasterDataGovernanceStandaloneService(database_url=database_url)

    def close(self) -> None:
        self.service.close()

    def load_seed_bundle(self, tenant: str = "tenant_seed") -> dict[str, Any]:
        return self.service.load_seed_bundle({"tenant": tenant})

    def render_workbench(self, tenant: str = "default") -> dict[str, Any]:
        state = self.service.query_workbench({"tenant": tenant})["result"]
        return master_data_governance_render_standalone_workbench(state)


def standalone_model_contract() -> dict:
    tables = tuple(
        {
            "table": item.table,
            "category": item.category,
            "description": item.description,
            "fields": (
                ("id", "tenant", "code", "status", "payload", "created_at", "updated_at")
                if item.category == "business"
                else ("id", "tenant", "code", "status", "event_type", "idempotency_key", "payload", "created_at", "updated_at")
            ),
        }
        for item in TABLE_SPECS
    )
    return {
        "format": f"appgen.{PBC_KEY}.standalone-model-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "database_backend": "sqlite",
        "table_keys": tuple(item.table for item in TABLE_SPECS),
        "business_tables": BUSINESS_TABLES,
        "event_tables": EVENT_TABLES,
        "tables": tables,
        "shared_table_access": False,
        "side_effects": (),
    }


def master_data_governance_form_contracts() -> dict:
    return {"format": f"appgen.{PBC_KEY}.form-contract.v1", "ok": True, "pbc": PBC_KEY, "contracts": FORM_DEFINITIONS, "side_effects": ()}


def master_data_governance_wizard_contracts() -> dict:
    return {"format": f"appgen.{PBC_KEY}.wizard-contract.v1", "ok": True, "pbc": PBC_KEY, "contracts": WIZARD_DEFINITIONS, "side_effects": ()}


def master_data_governance_control_catalog() -> dict:
    return {"format": f"appgen.{PBC_KEY}.control-contract.v1", "ok": True, "pbc": PBC_KEY, "contracts": CONTROL_DEFINITIONS, "side_effects": ()}


def standalone_service_operation_contracts() -> dict:
    contracts = tuple(
        {
            "method": route["method"],
            "path": route["path"],
            "handler": route["handler"],
            "operation": route["operation"],
            "operation_kind": route["operation_kind"],
            "table": route["table"],
            "permission": route["permission"],
            "form": route["form"],
            "wizard": route["wizard"],
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
            "shared_table_access": False,
            "transaction_boundary": "package_local_sqlite_plus_outbox" if route["operation_kind"] == "command" else "read_only_projection",
        }
        for route in ROUTE_DEFINITIONS
    )
    return {
        "format": f"appgen.{PBC_KEY}.standalone-service-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "contracts": contracts,
        "command_operations": tuple(item["operation"] for item in contracts if item["operation_kind"] == "command"),
        "query_operations": tuple(item["operation"] for item in contracts if item["operation_kind"] == "query"),
        "store_contract": standalone_model_contract(),
        "side_effects": (),
    }


def standalone_route_contracts() -> dict:
    return {
        "format": f"appgen.{PBC_KEY}.standalone-route-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "contracts": standalone_service_operation_contracts()["contracts"],
        "routes": tuple(f"{item['method']} {item['path']}" for item in ROUTE_DEFINITIONS),
        "side_effects": (),
    }


def master_data_governance_standalone_workbench_blueprint() -> dict:
    return {
        "format": f"appgen.{PBC_KEY}.standalone-workbench.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "fragments": (
            "MasterDataGovernanceWorkbench",
            "MasterDataGovernanceDetail",
            "MasterDataGovernanceAssistantPanel",
        ),
        "forms": FORM_KEYS,
        "wizards": WIZARD_KEYS,
        "controls": CONTROL_KEYS,
        "navigation": (
            {"route": "/app/master-data-governance/workbench", "label": "Workbench"},
            {"route": "/app/master-data-governance/domains", "label": "Domain Registry"},
            {"route": "/app/master-data-governance/match-candidates", "label": "Match Queue"},
            {"route": "/app/master-data-governance/golden-records", "label": "Golden Records"},
            {"route": "/app/master-data-governance/remediation-issues", "label": "Remediation"},
            {"route": "/app/master-data-governance/hierarchy-nodes", "label": "Hierarchy"},
            {"route": "/app/master-data-governance/audit-proofs", "label": "Audit Proof"},
        ),
        "panels": (
            {"key": "registry", "title": "Domain registry", "tables": (DOMAIN_TABLE, REFERENCE_TABLE, POLICY_TABLE)},
            {"key": "golden_record_studio", "title": "Golden record studio", "tables": (SOURCE_TABLE, MATCH_TABLE, MERGE_TABLE, GOLDEN_TABLE, SURVIVORSHIP_TABLE)},
            {"key": "quality_and_stewardship", "title": "Quality and stewardship", "tables": (QUALITY_RULE_TABLE, REMEDIATION_TABLE, STEWARDSHIP_TABLE)},
            {"key": "hierarchy_and_lineage", "title": "Hierarchy and lineage", "tables": (HIERARCHY_TABLE, LINEAGE_TABLE)},
            {"key": "release_and_audit", "title": "Release and audit", "tables": (AUDIT_TABLE, OUTBOX_TABLE, DEAD_LETTER_TABLE)},
        ),
        "routes": standalone_route_contracts()["routes"],
        "side_effects": (),
    }


def master_data_governance_render_standalone_workbench(workbench_state: dict[str, Any]) -> dict:
    blueprint = master_data_governance_standalone_workbench_blueprint()
    summary = dict(workbench_state.get("summary", {}))
    cards = (
        {"key": "domains", "value": summary.get("domains", 0), "control": "WorkbenchSummaryCards"},
        {"key": "golden_records", "value": summary.get("golden_records", 0), "control": "WorkbenchSummaryCards"},
        {"key": "match_queue", "value": summary.get("match_queue", 0), "control": "MatchQueueControl"},
        {"key": "remediation_open", "value": summary.get("remediation_open", 0), "control": "StewardshipWorkflowControl"},
        {"key": "lineage_links", "value": summary.get("lineage_links", 0), "control": "LineageExplorerControl"},
        {"key": "audit_proofs", "value": summary.get("audit_proofs", 0), "control": "AuditProofControl"},
    )
    return {
        "ok": blueprint["ok"],
        "pbc": PBC_KEY,
        "tenant": workbench_state.get("tenant"),
        "shell": blueprint,
        "summary_cards": cards,
        "queues": workbench_state.get("queues", {}),
        "records": workbench_state.get("records", {}),
        "configuration_bound": True,
        "release_evidence_ready": True,
        "binding_evidence": {
            "runtime_tables": RUNTIME_TABLES,
            "event_contract": "AppGen-X",
            "database_backend": "sqlite",
            "shared_table_access": False,
        },
        "side_effects": (),
    }


def build_document_instruction_plan(document: Any = None, instructions: Any = None) -> dict:
    document_text = str(document or "")
    instruction_text = str(instructions or "")
    combined = f"{document_text} {instruction_text}".lower()
    digest = _digest((document_text, instruction_text))
    wizard_candidates = tuple(
        wizard["key"]
        for wizard in WIZARD_DEFINITIONS
        if any(keyword in combined for keyword in wizard["keywords"])
    ) or ("AgentDocumentIntakeWizard",)
    route_candidates = tuple(
        f"{route['method']} {route['path']}"
        for route in ROUTE_DEFINITIONS
        if any(keyword in combined for keyword in route["keywords"])
    ) or ("GET /app/master-data-governance/workbench",)
    form_candidates = tuple(
        form["key"]
        for form in FORM_DEFINITIONS
        if any(keyword in combined for keyword in form["keywords"])
    ) or ("AgentDocumentPlanForm",)
    candidate_tables = tuple(
        form["table"]
        for form in FORM_DEFINITIONS
        if form["key"] in form_candidates
    ) or (DOMAIN_TABLE,)
    candidate_operations = tuple(
        route["operation"]
        for route in ROUTE_DEFINITIONS
        if f"{route['method']} {route['path']}" in route_candidates
    )
    return {
        "ok": bool(document_text or instruction_text),
        "pbc": PBC_KEY,
        "agent": AGENT_NAME,
        "document_digest": digest,
        "candidate_tables": tuple(dict.fromkeys(candidate_tables)),
        "candidate_operations": candidate_operations,
        "wizard_candidates": wizard_candidates,
        "form_candidates": form_candidates,
        "route_candidates": route_candidates,
        "requires_human_confirmation": True,
        "event_contract": "AppGen-X",
        "side_effects": (),
    }


def build_datastore_crud_plan(action: Any = "read", table: Any = None, payload: Any = None) -> dict:
    normalized_action = str(action or "read").lower()
    selected_table = str(table or DOMAIN_TABLE)
    payload_dict = dict(payload or {})
    owned_tables = standalone_model_contract()["table_keys"]
    if normalized_action == "read":
        route_candidates = ("GET /app/master-data-governance/workbench",)
    else:
        route_candidates = tuple(
            f"{item['method']} {item['path']}"
            for item in ROUTE_DEFINITIONS
            if item["table"] == selected_table and item["operation_kind"] == "command"
        )
    form_candidates = tuple(form["key"] for form in FORM_DEFINITIONS if form["table"] == selected_table)
    wizard_candidates = tuple(
        dict.fromkeys(
            route["wizard"]
            for route in ROUTE_DEFINITIONS
            if route["table"] == selected_table and route.get("wizard")
        )
    )
    return {
        "ok": normalized_action in CRUD_ACTIONS and selected_table in owned_tables and bool(route_candidates),
        "pbc": PBC_KEY,
        "action": normalized_action,
        "table": selected_table,
        "owned_tables": owned_tables,
        "payload_keys": tuple(sorted(payload_dict)),
        "route_candidates": route_candidates,
        "form_candidates": form_candidates,
        "wizard_candidates": wizard_candidates,
        "requires_confirmation": normalized_action != "read",
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def seed_bundle_contract() -> dict:
    return {
        "format": f"appgen.{PBC_KEY}.seed-bundle.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "rows": tuple(SEED_BUNDLE),
        "tables": tuple(dict.fromkeys(item["payload"].get("table", route["table"]) for item, route in zip(SEED_BUNDLE, ROUTE_DEFINITIONS[: len(SEED_BUNDLE)]))),
        "side_effects": (),
    }


def master_data_governance_standalone_app_contract() -> dict:
    agent_workspace = {
        "ok": True,
        "forms": FORM_KEYS,
        "wizards": WIZARD_KEYS,
        "routes": standalone_route_contracts()["routes"],
        "tables": standalone_model_contract()["table_keys"],
    }
    return {
        "format": f"appgen.{PBC_KEY}.standalone-app.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "models": standalone_model_contract(),
        "services": standalone_service_operation_contracts(),
        "routes": standalone_route_contracts(),
        "ui": master_data_governance_standalone_workbench_blueprint(),
        "seed_bundle": seed_bundle_contract(),
        "agent_workspace": agent_workspace,
        "side_effects": (),
    }


def build_standalone_app(database_url: str = ":memory:") -> MasterDataGovernanceStandaloneApp:
    return MasterDataGovernanceStandaloneApp(database_url=database_url)


def dispatch_standalone_route(
    method: str,
    path: str,
    payload: dict[str, Any] | None = None,
    *,
    service: MasterDataGovernanceStandaloneService | None = None,
) -> dict:
    route = next(
        (item for item in ROUTE_DEFINITIONS if item["method"] == method and item["path"] == path),
        None,
    )
    if route is None:
        return {"ok": False, "handled": False, "reason": "route_not_found", "side_effects": ()}
    local_service = service or MasterDataGovernanceStandaloneService()
    try:
        result = getattr(local_service, route["handler"])(payload or {})
        return {
            "ok": result.get("ok") is True,
            "handled": True,
            "route": route,
            "result": result,
            "side_effects": (),
        }
    finally:
        if service is None:
            local_service.close()


def standalone_store_smoke_test() -> dict:
    service = MasterDataGovernanceStandaloneService()
    try:
        seed = service.load_seed_bundle({"tenant": "tenant_smoke"})
        workbench = service.query_workbench({"tenant": "tenant_smoke"})
        render = master_data_governance_render_standalone_workbench(workbench["result"])
        document = service.document_instruction_plan(
            {
                "document": "Source system change request for customer party golden record publication.",
                "instructions": "merge duplicate customer records and publish the golden version with lineage proof",
            }
        )
        crud = service.datastore_crud_plan({"action": "create", "table": GOLDEN_TABLE, "payload": {"golden_code": "GOLD-SMOKE"}})
        return {
            "ok": seed["ok"] and workbench["ok"] and render["ok"] and document["ok"] and crud["ok"],
            "seed": seed,
            "workbench": workbench,
            "render": render,
            "document": document,
            "crud": crud,
            "side_effects": (),
        }
    finally:
        service.close()


def standalone_route_smoke_test() -> dict:
    service = MasterDataGovernanceStandaloneService()
    try:
        seed = dispatch_standalone_route("POST", "/app/master-data-governance/seed-bundle", {"tenant": "tenant_route"}, service=service)
        workbench = dispatch_standalone_route("GET", "/app/master-data-governance/workbench", {"tenant": "tenant_route"}, service=service)
        golden = dispatch_standalone_route(
            "POST",
            "/app/master-data-governance/golden-records",
            {
                "tenant": "tenant_route",
                "golden_code": "GOLD-ROUTE-1",
                "domain_code": "CUSTOMER_PARTY",
                "business_key": "CUST-ROUTE-1",
                "winning_record_code": "CRM-100",
                "published_by": "route.user",
                "attributes": {"name": "Route Customer"},
            },
            service=service,
        )
        return {
            "ok": seed["ok"] and workbench["ok"] and golden["ok"],
            "seed": seed,
            "workbench": workbench,
            "golden": golden,
            "side_effects": (),
        }
    finally:
        service.close()


def master_data_governance_standalone_app_smoke() -> dict:
    app = build_standalone_app()
    try:
        seed = app.load_seed_bundle("tenant_app")
        rendered = app.render_workbench("tenant_app")
        return {
            "ok": seed["ok"] and rendered["ok"],
            "contract": master_data_governance_standalone_app_contract(),
            "seed": seed,
            "rendered": rendered,
            "side_effects": (),
        }
    finally:
        app.close()
