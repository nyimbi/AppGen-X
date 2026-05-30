"""Canonical package-local blueprint for the data_product_catalog PBC."""
from __future__ import annotations

import hashlib

PBC_KEY = "data_product_catalog"
LABEL = "Data Product Catalog"
DESCRIPTION = (
    "Standalone data product governance capability for product identity, owners, "
    "contracts, schemas, quality, lineage, access, subscriptions, "
    "certifications, usage, SLAs, incidents, changes, retention, policy, and "
    "governed AI stewardship."
)
VERSION = "1.1.0"
ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
REQUIRED_EVENT_TOPIC = f"pbc.{PBC_KEY}.events"
EVENT_CONTRACT = "AppGen-X"

STANDARD_FEATURES = (
    "data_product_management",
    "data_product_catalog_workflow",
    "data_product_catalog_analytics",
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

ADVANCED_CAPABILITIES = (
    "contract-aware data discovery",
    "lineage impact simulation",
    "quality drift detection",
    "AI data product steward",
    "policy-aware access recommendation",
    "cryptographic contract evidence",
)

RUNTIME_CAPABILITIES = (
    "data_product_catalog_event_sourced_operational_history",
    "data_product_catalog_multi_tenant_policy_isolation",
    "data_product_catalog_schema_evolution_resilience",
    "data_product_catalog_autonomous_anomaly_detection",
    "data_product_catalog_semantic_document_instruction_understanding",
    "data_product_catalog_predictive_risk_scoring",
    "data_product_catalog_counterfactual_scenario_simulation",
    "data_product_catalog_cryptographic_audit_proofs",
    "data_product_catalog_continuous_control_testing",
    "data_product_catalog_carbon_and_sustainability_awareness",
    "data_product_catalog_cross_pbc_event_federation",
    "data_product_catalog_governed_ai_agent_execution",
)

PERMISSIONS = (
    f"{PBC_KEY}.read",
    f"{PBC_KEY}.create",
    f"{PBC_KEY}.update",
    f"{PBC_KEY}.approve",
    f"{PBC_KEY}.admin",
)
RBAC_ROLES = ("reader", "operator", "approver", "admin")
UI_FRAGMENTS = (
    "DataProductCatalogWorkbench",
    "DataProductCatalogDetail",
    "DataProductCatalogAssistantPanel",
)
WORKBENCH_VIEWS = (
    "data product catalog",
    "contract studio",
    "quality dashboard",
    "lineage graph",
    "access request queue",
    "certification panel",
    "usage analytics",
)
NAVIGATION_SECTIONS = (
    "command_center",
    "catalog_records",
    "forms",
    "wizards",
    "controls",
    "governance_rules",
    "analytics",
    "assistant",
    "release_evidence",
)

EMITTED_EVENTS = (
    "DataProductCreated",
    "DataContractPublished",
    "DataQualityChanged",
    "DataAccessGranted",
    "DataProductCertified",
    "DataProductIncidentOpened",
)
CONSUMED_EVENTS = (
    "PolicyChanged",
    "AccessPolicyChanged",
    "SchemaAccepted",
    "AuditProofGenerated",
)


def digest(value: object) -> str:
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()


def field(name: str, field_type: str, **metadata: object) -> dict:
    return {"name": name, "type": field_type, **metadata}


def _class_name(logical_name: str) -> str:
    return "DataProductCatalog" + "".join(part.capitalize() for part in logical_name.split("_"))


def _owned_table(logical_name: str) -> str:
    return f"{PBC_KEY}_{logical_name}"


BASE_FIELDS = (
    field("id", "text", primary_key=True, nullable=False, required=True),
    field("tenant", "string", required=True, indexed=True),
    field("code", "string", required=True, searchable=True),
    field("status", "string", required=True, default="draft"),
    field("lifecycle_state", "string", required=True, default="proposed"),
    field("version", "integer", required=True, default=1),
    field("payload", "json"),
    field("evidence_payload", "json"),
    field("effective_at", "datetime"),
    field("created_at", "datetime", required=True),
    field("updated_at", "datetime", required=True),
)

RELATION_FIELD = field(
    "data_product_id",
    "text",
    required=True,
    references=f"{_owned_table('data_product')}.id",
)

TABLE_INPUTS = (
    {
        "logical_table": "data_product",
        "extra_fields": (
            field("product_type", "string", required=True),
            field("value_proposition", "string", required=True),
            field("consumer_personas", "json"),
        ),
    },
    {
        "logical_table": "data_product_owner",
        "extra_fields": (
            RELATION_FIELD,
            field("owner_role", "string", required=True),
            field("owner_email", "string", required=True),
            field("review_cadence_days", "integer", required=True),
        ),
    },
    {
        "logical_table": "data_contract",
        "extra_fields": (
            RELATION_FIELD,
            field("compatibility_level", "string", required=True),
            field("clause_library", "json"),
            field("published_at", "datetime"),
        ),
    },
    {
        "logical_table": "data_schema_version",
        "extra_fields": (
            RELATION_FIELD,
            field("schema_version", "string", required=True),
            field("field_semantics", "json"),
            field("compatibility_result", "string", required=True),
        ),
    },
    {
        "logical_table": "data_quality_signal",
        "extra_fields": (
            RELATION_FIELD,
            field("quality_dimension", "string", required=True),
            field("threshold", "decimal", required=True),
            field("severity", "string", required=True),
            field("observed_at", "datetime", required=True),
        ),
    },
    {
        "logical_table": "data_lineage_edge",
        "extra_fields": (
            RELATION_FIELD,
            field("upstream_product_code", "string", required=True),
            field("edge_type", "string", required=True),
            field("freshness_minutes", "integer"),
        ),
    },
    {
        "logical_table": "data_access_request",
        "extra_fields": (
            RELATION_FIELD,
            field("requester", "string", required=True),
            field("use_case", "string", required=True),
            field("risk_score", "decimal", required=True),
            field("requested_at", "datetime", required=True),
        ),
    },
    {
        "logical_table": "data_access_grant",
        "extra_fields": (
            RELATION_FIELD,
            field("grantee", "string", required=True),
            field("grant_scope", "json", required=True),
            field("expires_at", "datetime"),
            field("approved_at", "datetime", required=True),
        ),
    },
    {
        "logical_table": "data_subscription",
        "extra_fields": (
            RELATION_FIELD,
            field("consumer_name", "string", required=True),
            field("delivery_mode", "string", required=True),
            field("subscribed_at", "datetime", required=True),
        ),
    },
    {
        "logical_table": "data_product_certification",
        "extra_fields": (
            RELATION_FIELD,
            field("certification_level", "string", required=True),
            field("certified_at", "datetime", required=True),
            field("expires_at", "datetime"),
        ),
    },
    {
        "logical_table": "data_product_usage",
        "extra_fields": (
            RELATION_FIELD,
            field("consumer_name", "string", required=True),
            field("request_volume", "integer", required=True),
            field("measured_at", "datetime", required=True),
        ),
    },
    {
        "logical_table": "data_product_sla",
        "extra_fields": (
            RELATION_FIELD,
            field("commitment_type", "string", required=True),
            field("threshold", "decimal", required=True),
            field("measurement_window", "string", required=True),
        ),
    },
    {
        "logical_table": "data_product_incident",
        "extra_fields": (
            RELATION_FIELD,
            field("severity", "string", required=True),
            field("incident_state", "string", required=True),
            field("opened_at", "datetime", required=True),
        ),
    },
    {
        "logical_table": "data_product_change",
        "extra_fields": (
            RELATION_FIELD,
            field("change_type", "string", required=True),
            field("notice_window_days", "integer", required=True),
            field("effective_on", "datetime"),
        ),
    },
    {
        "logical_table": "data_product_retention_policy",
        "extra_fields": (
            RELATION_FIELD,
            field("retention_period_days", "integer", required=True),
            field("legal_basis", "string", required=True),
            field("disposition_action", "string", required=True),
        ),
    },
    {
        "logical_table": "data_product_exception_case",
        "extra_fields": (
            RELATION_FIELD,
            field("case_type", "string", required=True),
            field("owner_code", "string", required=True),
            field("resolution_due_at", "datetime"),
        ),
    },
    {
        "logical_table": "data_product_policy_rule",
        "extra_fields": (
            RELATION_FIELD,
            field("rule_scope", "string", required=True),
            field("rule_hash", "string", required=True),
            field("compiled_at", "datetime"),
        ),
    },
    {
        "logical_table": "data_product_runtime_parameter",
        "extra_fields": (
            field("parameter_key", "string", required=True),
            field("parameter_value", "string", required=True),
            field("parameter_scope", "string", required=True),
            field("bounded", "boolean", required=True),
        ),
    },
    {
        "logical_table": "data_product_schema_extension",
        "extra_fields": (
            RELATION_FIELD,
            field("extension_kind", "string", required=True),
            field("applied_at", "datetime", required=True),
        ),
    },
    {
        "logical_table": "data_product_control_assertion",
        "extra_fields": (
            RELATION_FIELD,
            field("control_name", "string", required=True),
            field("assertion_outcome", "string", required=True),
            field("asserted_at", "datetime", required=True),
        ),
    },
    {
        "logical_table": "data_product_governed_model",
        "extra_fields": (
            RELATION_FIELD,
            field("model_name", "string", required=True),
            field("model_version", "string", required=True),
            field("approval_state", "string", required=True),
        ),
    },
    {
        "logical_table": "appgen_outbox_event",
        "extra_fields": (
            field("event_type", "string", required=True),
            field("event_topic", "string", required=True),
            field("idempotency_key", "string", required=True),
            field("published_at", "datetime", required=True),
        ),
    },
    {
        "logical_table": "appgen_inbox_event",
        "extra_fields": (
            field("event_type", "string", required=True),
            field("source_event_id", "string", required=True),
            field("idempotency_key", "string", required=True),
            field("received_at", "datetime", required=True),
        ),
    },
    {
        "logical_table": "appgen_dead_letter_event",
        "extra_fields": (
            field("event_type", "string", required=True),
            field("source_event_id", "string", required=True),
            field("idempotency_key", "string", required=True),
            field("retry_count", "integer", required=True),
            field("dead_lettered_at", "datetime", required=True),
        ),
    },
)

TABLE_BLUEPRINTS = tuple(
    {
        "logical_table": item["logical_table"],
        "owned_table": _owned_table(item["logical_table"]),
        "class_name": _class_name(item["logical_table"]),
        "fields": BASE_FIELDS + tuple(item["extra_fields"]),
        "relationships": (
            {
                "field": "data_product_id",
                "target_table": _owned_table("data_product"),
                "target_column": "id",
                "cardinality": "many-to-one",
                "ownership": "same_pbc",
            },
        )
        if any(field_def["name"] == "data_product_id" for field_def in item["extra_fields"])
        else (),
    }
    for item in TABLE_INPUTS
)

BUSINESS_TABLES = tuple(
    table["owned_table"]
    for table in TABLE_BLUEPRINTS
    if not table["logical_table"].startswith("appgen_")
)
OWNED_TABLES = tuple(table["owned_table"] for table in TABLE_BLUEPRINTS)
RUNTIME_TABLES = OWNED_TABLES
LOGICAL_TABLES = tuple(table["logical_table"] for table in TABLE_BLUEPRINTS)
MODELS = tuple(
    {
        "class_name": table["class_name"],
        "table": table["owned_table"],
        "fields": table["fields"],
        "relationships": table["relationships"],
    }
    for table in TABLE_BLUEPRINTS
)

DOMAIN_PURPOSE = (
    "Owns data products, ownership, contracts, schemas, quality, lineage, "
    "access, subscriptions, certifications, usage analytics, and productized "
    "data governance."
)
DOMAIN_OPERATIONS = (
    "create_data_product",
    "assign_data_owner",
    "publish_data_contract",
    "register_schema_version",
    "record_quality_signal",
    "map_lineage_edge",
    "request_data_access",
    "grant_data_access",
    "subscribe_to_data_product",
    "certify_data_product",
    "record_usage",
    "define_product_sla",
    "open_product_incident",
    "publish_product_change",
    "define_retention_policy",
    "resolve_data_product_exception",
    "compile_data_product_rule",
    "simulate_contract_change_impact",
)

RULE_BLUEPRINTS = (
    {
        "rule_id": "data_contract_policy",
        "scope": "contract",
        "condition": "required_clause_set_present",
        "description": "Reject contracts that omit executable clause coverage.",
    },
    {
        "rule_id": "quality_certification_policy",
        "scope": "quality",
        "condition": "quality_score_floor_met",
        "description": "Block certification when quality evidence is below floor.",
    },
    {
        "rule_id": "access_approval_policy",
        "scope": "access",
        "condition": "policy_recommendation_resolved",
        "description": "Require explainable policy approval for grants.",
    },
    {
        "rule_id": "lineage_policy",
        "scope": "lineage",
        "condition": "lineage_evidence_complete",
        "description": "Reject incomplete upstream or downstream lineage edges.",
    },
    {
        "rule_id": "sla_policy",
        "scope": "service",
        "condition": "consumer_tier_commitments_declared",
        "description": "Require measurable SLA commitments per tier.",
    },
    {
        "rule_id": "retention_policy",
        "scope": "retention",
        "condition": "retention_legal_basis_declared",
        "description": "Ensure legal basis exists for each retention policy.",
    },
)

PARAMETER_BLUEPRINTS = (
    {
        "key": "quality_score_floor",
        "scope": "quality",
        "default": 0.97,
        "minimum": 0.0,
        "maximum": 1.0,
        "control": "slider",
    },
    {
        "key": "access_review_days",
        "scope": "access",
        "default": 30,
        "minimum": 1,
        "maximum": 365,
        "control": "number",
    },
    {
        "key": "schema_compatibility_level",
        "scope": "schema",
        "default": "backward",
        "allowed_values": ("none", "backward", "forward", "full"),
        "control": "select",
    },
    {
        "key": "usage_anomaly_threshold",
        "scope": "usage",
        "default": 2.5,
        "minimum": 0.1,
        "maximum": 10.0,
        "control": "slider",
    },
    {
        "key": "sla_warning_minutes",
        "scope": "sla",
        "default": 45,
        "minimum": 1,
        "maximum": 1440,
        "control": "number",
    },
    {
        "key": "workbench_limit",
        "scope": "ui",
        "default": 25,
        "minimum": 5,
        "maximum": 250,
        "control": "number",
    },
)

OPERATION_BLUEPRINTS = (
    {
        "name": "create_data_product",
        "summary": "Create a data product with its value proposition and lifecycle state.",
        "target_table": _owned_table("data_product"),
        "emitted_event": "DataProductCreated",
        "required_fields": ("tenant", "code", "product_type", "value_proposition"),
        "route": {"method": "POST", "path": "/data-products"},
        "form_id": "data_product_intake_form",
        "wizard_id": "product_onboarding_wizard",
    },
    {
        "name": "assign_data_owner",
        "summary": "Assign accountable ownership and stewardship coverage.",
        "target_table": _owned_table("data_product_owner"),
        "emitted_event": "DataProductCreated",
        "required_fields": ("tenant", "code", "data_product_id", "owner_role", "owner_email"),
        "route": {"method": "POST", "path": "/data-products/owners"},
        "form_id": "owner_assignment_form",
        "wizard_id": "product_onboarding_wizard",
    },
    {
        "name": "publish_data_contract",
        "summary": "Publish a machine-readable data contract clause set.",
        "target_table": _owned_table("data_contract"),
        "emitted_event": "DataContractPublished",
        "required_fields": ("tenant", "code", "data_product_id", "compatibility_level"),
        "route": {"method": "POST", "path": "/data-contracts"},
        "form_id": "contract_publication_form",
        "wizard_id": "contract_publication_wizard",
    },
    {
        "name": "register_schema_version",
        "summary": "Register and validate a schema version against the active contract.",
        "target_table": _owned_table("data_schema_version"),
        "emitted_event": "DataContractPublished",
        "required_fields": ("tenant", "code", "data_product_id", "schema_version"),
        "route": {"method": "POST", "path": "/schema-versions"},
        "form_id": "schema_version_form",
        "wizard_id": "contract_publication_wizard",
    },
    {
        "name": "record_quality_signal",
        "summary": "Capture quality observations and drift evidence.",
        "target_table": _owned_table("data_quality_signal"),
        "emitted_event": "DataQualityChanged",
        "required_fields": ("tenant", "code", "data_product_id", "quality_dimension", "threshold"),
        "route": {"method": "POST", "path": "/quality-signals"},
        "form_id": "quality_signal_form",
        "wizard_id": "quality_triage_wizard",
    },
    {
        "name": "map_lineage_edge",
        "summary": "Register lineage between upstream and downstream products.",
        "target_table": _owned_table("data_lineage_edge"),
        "emitted_event": "DataQualityChanged",
        "required_fields": ("tenant", "code", "data_product_id", "upstream_product_code", "edge_type"),
        "route": {"method": "POST", "path": "/lineage-edges"},
        "form_id": "lineage_edge_form",
        "wizard_id": "change_impact_wizard",
    },
    {
        "name": "request_data_access",
        "summary": "Open a policy-aware access request with risk scoring.",
        "target_table": _owned_table("data_access_request"),
        "emitted_event": "DataAccessGranted",
        "required_fields": ("tenant", "code", "data_product_id", "requester", "use_case"),
        "route": {"method": "POST", "path": "/access-requests"},
        "form_id": "access_request_form",
        "wizard_id": "access_review_wizard",
    },
    {
        "name": "grant_data_access",
        "summary": "Grant scoped, time-bound access backed by policy evidence.",
        "target_table": _owned_table("data_access_grant"),
        "emitted_event": "DataAccessGranted",
        "required_fields": ("tenant", "code", "data_product_id", "grantee", "grant_scope"),
        "route": {"method": "POST", "path": "/access-grants"},
        "form_id": "access_grant_form",
        "wizard_id": "access_review_wizard",
    },
    {
        "name": "subscribe_to_data_product",
        "summary": "Record an active consumer subscription and commitment tier.",
        "target_table": _owned_table("data_subscription"),
        "emitted_event": "DataAccessGranted",
        "required_fields": ("tenant", "code", "data_product_id", "consumer_name", "delivery_mode"),
        "route": {"method": "POST", "path": "/subscriptions"},
        "form_id": "subscription_form",
        "wizard_id": "product_onboarding_wizard",
    },
    {
        "name": "certify_data_product",
        "summary": "Issue certification with trust badge and expiry evidence.",
        "target_table": _owned_table("data_product_certification"),
        "emitted_event": "DataProductCertified",
        "required_fields": ("tenant", "code", "data_product_id", "certification_level"),
        "route": {"method": "POST", "path": "/certifications"},
        "form_id": "certification_form",
        "wizard_id": "certification_readiness_wizard",
    },
    {
        "name": "record_usage",
        "summary": "Record usage and adoption telemetry for a product.",
        "target_table": _owned_table("data_product_usage"),
        "emitted_event": "DataQualityChanged",
        "required_fields": ("tenant", "code", "data_product_id", "consumer_name", "request_volume"),
        "route": {"method": "POST", "path": "/usage"},
        "form_id": "usage_record_form",
        "wizard_id": "usage_analytics_wizard",
    },
    {
        "name": "define_product_sla",
        "summary": "Define service commitments and breach rules.",
        "target_table": _owned_table("data_product_sla"),
        "emitted_event": "DataQualityChanged",
        "required_fields": ("tenant", "code", "data_product_id", "commitment_type", "threshold"),
        "route": {"method": "POST", "path": "/slas"},
        "form_id": "sla_definition_form",
        "wizard_id": "certification_readiness_wizard",
    },
    {
        "name": "open_product_incident",
        "summary": "Open a consumer-facing data product incident.",
        "target_table": _owned_table("data_product_incident"),
        "emitted_event": "DataProductIncidentOpened",
        "required_fields": ("tenant", "code", "data_product_id", "severity", "incident_state"),
        "route": {"method": "POST", "path": "/incidents"},
        "form_id": "incident_form",
        "wizard_id": "incident_response_wizard",
    },
    {
        "name": "publish_product_change",
        "summary": "Publish a governed change announcement and migration guidance.",
        "target_table": _owned_table("data_product_change"),
        "emitted_event": "DataContractPublished",
        "required_fields": ("tenant", "code", "data_product_id", "change_type", "notice_window_days"),
        "route": {"method": "POST", "path": "/changes"},
        "form_id": "change_publication_form",
        "wizard_id": "change_impact_wizard",
    },
    {
        "name": "define_retention_policy",
        "summary": "Define retention, disposition, and legal basis controls.",
        "target_table": _owned_table("data_product_retention_policy"),
        "emitted_event": "DataAccessGranted",
        "required_fields": ("tenant", "code", "data_product_id", "retention_period_days", "legal_basis"),
        "route": {"method": "POST", "path": "/retention-policies"},
        "form_id": "retention_policy_form",
        "wizard_id": "access_review_wizard",
    },
    {
        "name": "resolve_data_product_exception",
        "summary": "Resolve an exception with owner and due-date evidence.",
        "target_table": _owned_table("data_product_exception_case"),
        "emitted_event": "DataAccessGranted",
        "required_fields": ("tenant", "code", "data_product_id", "case_type", "owner_code"),
        "route": {"method": "POST", "path": "/exception-cases/resolve"},
        "form_id": "exception_resolution_form",
        "wizard_id": "incident_response_wizard",
    },
    {
        "name": "compile_data_product_rule",
        "summary": "Compile a package-local data product policy rule.",
        "target_table": _owned_table("data_product_policy_rule"),
        "emitted_event": "DataAccessGranted",
        "required_fields": ("tenant", "code", "data_product_id", "rule_scope", "rule_hash"),
        "route": {"method": "POST", "path": "/policy-rules/compile"},
        "form_id": "policy_rule_form",
        "wizard_id": "contract_publication_wizard",
    },
    {
        "name": "simulate_contract_change_impact",
        "summary": "Simulate downstream impact for a contract or schema change.",
        "target_table": _owned_table("data_product_governed_model"),
        "emitted_event": "DataContractPublished",
        "required_fields": ("tenant", "code", "data_product_id", "model_name", "model_version"),
        "route": {"method": "POST", "path": "/contract-impact-simulations"},
        "form_id": "change_impact_simulation_form",
        "wizard_id": "change_impact_wizard",
    },
)

QUERY_BLUEPRINTS = (
    {
        "name": "query_workbench",
        "summary": "Read-only workbench query for package state.",
        "route": {"method": "GET", "path": "/data-product-catalog-workbench"},
    },
    {
        "name": "list_forms",
        "summary": "List workbench forms.",
        "route": {"method": "GET", "path": "/data-product-catalog/forms"},
    },
    {
        "name": "list_wizards",
        "summary": "List workbench wizards.",
        "route": {"method": "GET", "path": "/data-product-catalog/wizards"},
    },
    {
        "name": "list_controls",
        "summary": "List workbench controls.",
        "route": {"method": "GET", "path": "/data-product-catalog/controls"},
    },
)

FORM_BLUEPRINTS = tuple(
    {
        "form_id": operation["form_id"],
        "operation": operation["name"],
        "title": operation["name"].replace("_", " ").title(),
        "required_fields": operation["required_fields"],
        "target_table": operation["target_table"],
        "event_preview": operation["emitted_event"],
    }
    for operation in OPERATION_BLUEPRINTS
)

WIZARD_BLUEPRINTS = (
    {
        "wizard_id": "product_onboarding_wizard",
        "title": "Product Onboarding",
        "steps": ("create_data_product", "assign_data_owner", "subscribe_to_data_product"),
    },
    {
        "wizard_id": "contract_publication_wizard",
        "title": "Contract Publication",
        "steps": ("publish_data_contract", "register_schema_version", "compile_data_product_rule"),
    },
    {
        "wizard_id": "quality_triage_wizard",
        "title": "Quality Triage",
        "steps": ("record_quality_signal", "define_product_sla", "open_product_incident"),
    },
    {
        "wizard_id": "access_review_wizard",
        "title": "Access Review",
        "steps": ("request_data_access", "grant_data_access", "define_retention_policy"),
    },
    {
        "wizard_id": "certification_readiness_wizard",
        "title": "Certification Readiness",
        "steps": ("define_product_sla", "certify_data_product"),
    },
    {
        "wizard_id": "change_impact_wizard",
        "title": "Change Impact",
        "steps": ("map_lineage_edge", "publish_product_change", "simulate_contract_change_impact"),
    },
    {
        "wizard_id": "incident_response_wizard",
        "title": "Incident Response",
        "steps": ("open_product_incident", "resolve_data_product_exception"),
    },
    {
        "wizard_id": "usage_analytics_wizard",
        "title": "Usage Analytics",
        "steps": ("record_usage",),
    },
)

CONTROL_BLUEPRINTS = tuple(
    {
        "control_id": f"{parameter['key']}_{parameter['control']}",
        "parameter": parameter["key"],
        "control_type": parameter["control"],
        "scope": parameter["scope"],
        "bounded": True,
    }
    for parameter in PARAMETER_BLUEPRINTS
) + (
    {
        "control_id": "agent_confirmation_toggle",
        "control_type": "toggle",
        "scope": "assistant",
        "setting": "requires_human_confirmation",
        "bounded": False,
    },
    {
        "control_id": "release_gate_status_badge",
        "control_type": "badge",
        "scope": "release",
        "setting": "release_gates",
        "bounded": False,
    },
)

AGENT_SKILL_BLUEPRINTS = tuple(
    {
        "name": f"{PBC_KEY}_{operation['name']}",
        "scope": PBC_KEY,
        "description": operation["summary"],
        "requires_confirmation_for_mutation": True,
        "uses_appgen_event_contract": True,
        "target_table": operation["target_table"],
    }
    for operation in OPERATION_BLUEPRINTS
) + (
    {
        "name": f"{PBC_KEY}_document_planner",
        "scope": PBC_KEY,
        "description": "Parse steward instructions and propose governed CRUD plans.",
        "requires_confirmation_for_mutation": True,
        "uses_appgen_event_contract": True,
        "target_table": _owned_table("data_product"),
    },
)

EXPECTED_ARTIFACT_FILES = (
    "__init__.py",
    "README.md",
    "SPECIFICATION.md",
    "RELEASE_EVIDENCE.md",
    "implementation-plan.md",
    "implementation-status.md",
    "manifest.py",
    "models.py",
    "config.py",
    "schema_contract.py",
    "service_contract.py",
    "services.py",
    "routes.py",
    "ui.py",
    "events.py",
    "handlers.py",
    "agent.py",
    "runtime.py",
    "release_evidence.py",
    "permissions.py",
    "seed_data.py",
    "capability_assurance.py",
    "domain_depth.py",
    "migrations/001_initial.sql",
    "tests/test_contract.py",
)


def table_blueprint(logical_table: str) -> dict:
    return next(item for item in TABLE_BLUEPRINTS if item["logical_table"] == logical_table)


def operation_blueprint(name: str) -> dict:
    return next(item for item in OPERATION_BLUEPRINTS if item["name"] == name)


def query_blueprint(name: str) -> dict:
    return next(item for item in QUERY_BLUEPRINTS if item["name"] == name)


def route_blueprints() -> tuple[dict, ...]:
    command_routes = tuple(
        {
            "method": operation["route"]["method"],
            "path": operation["route"]["path"],
            "operation": operation["name"],
            "kind": "command",
            "idempotency_key": f"{PBC_KEY}:{operation['name']}",
            "required_permission": f"{PBC_KEY}.operate",
            "target_table": operation["target_table"],
            "event_contract": EVENT_CONTRACT,
        }
        for operation in OPERATION_BLUEPRINTS
    )
    query_routes = tuple(
        {
            "method": query["route"]["method"],
            "path": query["route"]["path"],
            "operation": query["name"],
            "kind": "query",
            "idempotency_key": f"{PBC_KEY}:{query['name']}",
            "required_permission": f"{PBC_KEY}.read",
            "target_table": None,
            "event_contract": EVENT_CONTRACT,
        }
        for query in QUERY_BLUEPRINTS
    )
    return command_routes + query_routes
