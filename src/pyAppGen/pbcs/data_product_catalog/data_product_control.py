"""Executable improve1 controls for the Data Product Catalog PBC."""

from __future__ import annotations

from typing import Any

from .blueprint import ALLOWED_DATABASE_BACKENDS, EVENT_CONTRACT, OWNED_TABLES, PBC_KEY, REQUIRED_EVENT_TOPIC, digest
from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability

OUTBOX_TABLE = f"{PBC_KEY}_appgen_outbox_event"
INBOX_TABLE = f"{PBC_KEY}_appgen_inbox_event"
DEAD_LETTER_TABLE = f"{PBC_KEY}_appgen_dead_letter_event"
PRODUCT_TABLE = f"{PBC_KEY}_data_product"
OWNER_TABLE = f"{PBC_KEY}_data_product_owner"
CONTRACT_TABLE = f"{PBC_KEY}_data_contract"
SCHEMA_TABLE = f"{PBC_KEY}_data_schema_version"
QUALITY_TABLE = f"{PBC_KEY}_data_quality_signal"
LINEAGE_TABLE = f"{PBC_KEY}_data_lineage_edge"
ACCESS_REQUEST_TABLE = f"{PBC_KEY}_data_access_request"
ACCESS_GRANT_TABLE = f"{PBC_KEY}_data_access_grant"
SUBSCRIPTION_TABLE = f"{PBC_KEY}_data_subscription"
CERTIFICATION_TABLE = f"{PBC_KEY}_data_product_certification"
USAGE_TABLE = f"{PBC_KEY}_data_product_usage"
SLA_TABLE = f"{PBC_KEY}_data_product_sla"
INCIDENT_TABLE = f"{PBC_KEY}_data_product_incident"
CHANGE_TABLE = f"{PBC_KEY}_data_product_change"
RETENTION_TABLE = f"{PBC_KEY}_data_product_retention_policy"
EXCEPTION_TABLE = f"{PBC_KEY}_data_product_exception_case"
POLICY_TABLE = f"{PBC_KEY}_data_product_policy_rule"
PARAMETER_TABLE = f"{PBC_KEY}_data_product_runtime_parameter"
SCHEMA_EXTENSION_TABLE = f"{PBC_KEY}_data_product_schema_extension"
CONTROL_TABLE = f"{PBC_KEY}_data_product_control_assertion"
MODEL_TABLE = f"{PBC_KEY}_data_product_governed_model"

DATA_PRODUCT_CONTROL_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in DATA_PRODUCT_CONTROL_CAPABILITIES}
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in DATA_PRODUCT_CONTROL_CAPABILITIES}

CONTROL_SPECS: dict[int, dict[str, Any]] = {
    1: {"tables": (PRODUCT_TABLE, OWNER_TABLE), "fields": ("value_proposition", "target_consumers", "business_outcomes", "source_domain", "lifecycle_state"), "ui": "DataProductCatalogDetail", "route": "POST /data-products"},
    2: {"tables": (PRODUCT_TABLE, OUTBOX_TABLE), "fields": ("current_state", "target_state", "approval_gate", "access_impact", "consumer_notification"), "ui": "DataProductCatalogWorkbench", "route": "POST /data-products/lifecycle"},
    3: {"tables": (OWNER_TABLE,), "fields": ("owner_role", "delegate", "backup_owner", "effective_date", "review_cadence", "escalation_path"), "ui": "DataProductCatalogDetail", "route": "POST /data-products/owners"},
    4: {"tables": (PRODUCT_TABLE, SUBSCRIPTION_TABLE, ACCESS_REQUEST_TABLE), "fields": ("consumer_persona", "use_case", "workflow_type", "declared_impact"), "ui": "DataProductCatalogDetail", "route": "POST /data-products/use-cases"},
    5: {"tables": (CONTRACT_TABLE, POLICY_TABLE), "fields": ("clause_library", "required_clause_sets", "template_version", "policy_bindings"), "ui": "DataProductCatalogDetail", "route": "POST /data-contracts"},
    6: {"tables": (CONTRACT_TABLE, CHANGE_TABLE, SUBSCRIPTION_TABLE), "fields": ("compatibility_rule", "change_class", "affected_consumers", "required_approvals"), "ui": "DataProductCatalogWorkbench", "route": "POST /data-contracts/impact-simulation"},
    7: {"tables": (SCHEMA_TABLE, CONTRACT_TABLE), "fields": ("field_semantics", "compatibility_tests", "deprecation_window", "primary_business_keys"), "ui": "DataProductCatalogDetail", "route": "POST /schema-versions"},
    8: {"tables": (SCHEMA_TABLE,), "fields": ("glossary_entry", "calculation_definition", "units", "valid_range", "code_list", "semantic_owner"), "ui": "DataProductCatalogAssistantPanel", "route": "POST /schema-versions/glossary"},
    9: {"tables": (QUALITY_TABLE, CONTRACT_TABLE), "fields": ("dimension", "threshold", "observation_window", "affected_fields", "consumer_impact"), "ui": "DataProductCatalogWorkbench", "route": "POST /quality-signals"},
    10: {"tables": (QUALITY_TABLE, OUTBOX_TABLE), "fields": ("distribution_shift", "freshness_drift", "null_rate", "volume_change", "materiality"), "ui": "DataProductCatalogWorkbench", "route": "POST /quality-signals/drift"},
    11: {"tables": (INCIDENT_TABLE, QUALITY_TABLE, SLA_TABLE), "fields": ("incident_type", "impact_window", "affected_subscriptions", "root_cause", "consumer_communications"), "ui": "DataProductCatalogWorkbench", "route": "POST /product-incidents"},
    12: {"tables": (LINEAGE_TABLE,), "fields": ("edge_type", "transformation_description", "freshness", "trust_level", "fields_affected"), "ui": "DataProductCatalogDetail", "route": "POST /lineage-edges"},
    13: {"tables": (LINEAGE_TABLE, CONTRACT_TABLE, SUBSCRIPTION_TABLE), "fields": ("upstream_change", "affected_products", "affected_consumers", "required_notifications"), "ui": "DataProductCatalogWorkbench", "route": "POST /lineage-impact-simulations"},
    14: {"tables": (ACCESS_REQUEST_TABLE, POLICY_TABLE), "fields": ("access_purpose", "consumer_role", "data_elements", "sensitivity", "legal_basis", "risk_score"), "ui": "DataProductCatalogAssistantPanel", "route": "POST /access-requests"},
    15: {"tables": (ACCESS_REQUEST_TABLE, POLICY_TABLE, ACCESS_GRANT_TABLE), "fields": ("policy_results", "recommended_scope", "conditions", "denial_reasons", "human_approval"), "ui": "DataProductCatalogAssistantPanel", "route": "POST /access-requests/recommend"},
    16: {"tables": (ACCESS_GRANT_TABLE, OUTBOX_TABLE), "fields": ("field_scope", "row_scope", "purpose", "expiry", "review_date", "masking_policy"), "ui": "DataProductCatalogWorkbench", "route": "POST /access-grants"},
    17: {"tables": (SUBSCRIPTION_TABLE, SLA_TABLE), "fields": ("subscription_state", "use_case", "consumer_owner", "delivery_mode", "sla_tier"), "ui": "DataProductCatalogDetail", "route": "POST /subscriptions"},
    18: {"tables": (SLA_TABLE, INCIDENT_TABLE), "fields": ("commitment_type", "measurement_rule", "calendar", "threshold", "breach_definition"), "ui": "DataProductCatalogDetail", "route": "POST /product-slas"},
    19: {"tables": (CERTIFICATION_TABLE, PRODUCT_TABLE, QUALITY_TABLE, LINEAGE_TABLE), "fields": ("readiness_checklist", "evidence_requirements", "reviewer_roles", "quality_history", "lineage_completeness"), "ui": "DataProductCatalogWorkbench", "route": "POST /certifications"},
    20: {"tables": (CERTIFICATION_TABLE,), "fields": ("certification_level", "required_controls", "usage_limits", "trust_badge"), "ui": "DataProductCatalogDetail", "route": "POST /certifications/levels"},
    21: {"tables": (USAGE_TABLE, ACCESS_GRANT_TABLE, SUBSCRIPTION_TABLE), "fields": ("consumer", "use_case", "query_mode", "volume", "latency", "freshness_at_consumption"), "ui": "DataProductCatalogWorkbench", "route": "POST /usage"},
    22: {"tables": (USAGE_TABLE, INCIDENT_TABLE, ACCESS_REQUEST_TABLE), "fields": ("usage_signal", "approved_scope", "anomaly_reason", "review_route"), "ui": "DataProductCatalogWorkbench", "route": "POST /usage/anomalies"},
    23: {"tables": (USAGE_TABLE, PRODUCT_TABLE), "fields": ("operating_cost", "support_burden", "consumer_count", "decision_impact", "risk_reduction"), "ui": "DataProductCatalogDetail", "route": "POST /data-products/value-metrics"},
    24: {"tables": (PRODUCT_TABLE, CONTRACT_TABLE, SCHEMA_TABLE), "fields": ("quick_start", "sample_usage", "field_guide", "limitations", "known_issues", "steward_approval"), "ui": "DataProductCatalogAssistantPanel", "route": "POST /data-products/docs"},
    25: {"tables": (PRODUCT_TABLE, USAGE_TABLE, CERTIFICATION_TABLE), "fields": ("semantic_match", "certification", "freshness", "quality", "access_eligibility"), "ui": "DataProductCatalogWorkbench", "route": "GET /data-products/search"},
    26: {"tables": (PRODUCT_TABLE, SCHEMA_TABLE, ACCESS_GRANT_TABLE, POLICY_TABLE), "fields": ("sensitivity_class", "source_evidence", "reviewer_approval", "masking_rules"), "ui": "DataProductCatalogDetail", "route": "POST /data-products/classification"},
    27: {"tables": (RETENTION_TABLE, ACCESS_GRANT_TABLE, SUBSCRIPTION_TABLE), "fields": ("retention_period", "trigger", "legal_basis", "hold_constraints", "deletion_proof"), "ui": "DataProductCatalogDetail", "route": "POST /retention-policies"},
    28: {"tables": (CONTRACT_TABLE, ACCESS_GRANT_TABLE, USAGE_TABLE), "fields": ("allowed_channels", "downstream_registration", "masking_requirements", "audit_obligations"), "ui": "DataProductCatalogWorkbench", "route": "POST /data-sharing-controls"},
    29: {"tables": (CHANGE_TABLE, CONTRACT_TABLE, SUBSCRIPTION_TABLE), "fields": ("change_type", "compatibility_assessment", "notice_period", "migration_guide", "rollback_plan"), "ui": "DataProductCatalogWorkbench", "route": "POST /product-changes"},
    30: {"tables": (CHANGE_TABLE, SUBSCRIPTION_TABLE, PRODUCT_TABLE), "fields": ("deprecation_state", "migration_tracking", "alternative_product", "grace_period", "retirement_proof"), "ui": "DataProductCatalogWorkbench", "route": "POST /data-products/deprecate"},
    31: {"tables": (INCIDENT_TABLE, SUBSCRIPTION_TABLE, SLA_TABLE), "fields": ("communication_template", "affected_consumers", "notification_sla", "status_update", "postmortem"), "ui": "DataProductCatalogWorkbench", "route": "POST /product-incidents/communications"},
    32: {"tables": (OWNER_TABLE, ACCESS_REQUEST_TABLE, INCIDENT_TABLE, EXCEPTION_TABLE), "fields": ("task_type", "owner", "due_date", "severity", "required_evidence", "policy_basis"), "ui": "DataProductCatalogWorkbench", "route": "GET /stewardship-board"},
    33: {"tables": (CONTRACT_TABLE, CONTROL_TABLE), "fields": ("test_case", "sample_payload", "quality_assertion", "freshness_check", "consumer_acceptance"), "ui": "DataProductCatalogDetail", "route": "POST /data-contract-tests"},
    34: {"tables": (SUBSCRIPTION_TABLE, USAGE_TABLE, ACCESS_GRANT_TABLE), "fields": ("dependency_record", "field_usage", "criticality", "attestation_due"), "ui": "DataProductCatalogDetail", "route": "POST /consumer-impact-evidence"},
    35: {"tables": (CONTROL_TABLE, QUALITY_TABLE, CERTIFICATION_TABLE, INCIDENT_TABLE), "fields": ("quality_component", "freshness_component", "ownership_component", "trend", "confidence"), "ui": "DataProductCatalogWorkbench", "route": "GET /data-products/health"},
    36: {"tables": (EXCEPTION_TABLE,), "fields": ("exception_type", "scope", "approver_authority", "expiry", "compensating_controls"), "ui": "DataProductCatalogWorkbench", "route": "POST /product-exceptions"},
    37: {"tables": (POLICY_TABLE, PARAMETER_TABLE), "fields": ("rule_version", "simulation", "approval_workflow", "effective_date", "rollback_plan"), "ui": "DataProductCatalogWorkbench", "route": "POST /policy-studio"},
    38: {"tables": (SCHEMA_EXTENSION_TABLE, INBOX_TABLE, DEAD_LETTER_TABLE), "fields": ("source_pbc", "allowed_fields", "freshness", "idempotency", "fallback_behavior"), "ui": "DataProductCatalogDetail", "route": "POST /federated-projections"},
    39: {"tables": (MODEL_TABLE, PRODUCT_TABLE, ACCESS_GRANT_TABLE), "fields": ("allowed_ai_use_cases", "training_restrictions", "bias_indicators", "leakage_flags", "evaluation_evidence"), "ui": "DataProductCatalogAssistantPanel", "route": "POST /data-products/ai-readiness"},
    40: {"tables": (POLICY_TABLE, ACCESS_REQUEST_TABLE, RETENTION_TABLE), "fields": ("subject_categories", "purpose", "lawful_basis", "minimization", "cross_border_restrictions"), "ui": "DataProductCatalogDetail", "route": "POST /privacy-reviews"},
    41: {"tables": (LINEAGE_TABLE, CONTROL_TABLE), "fields": ("upstream_coverage", "downstream_coverage", "field_coverage", "confidence", "freshness"), "ui": "DataProductCatalogWorkbench", "route": "GET /lineage/completeness"},
    42: {"tables": (QUALITY_TABLE, LINEAGE_TABLE, INCIDENT_TABLE, CHANGE_TABLE), "fields": ("failure_signal", "root_cause", "remediation", "prevention"), "ui": "DataProductCatalogWorkbench", "route": "POST /quality/root-cause"},
    43: {"tables": (OWNER_TABLE, USAGE_TABLE, CONTROL_TABLE), "fields": ("producer_reliability", "incident_response", "consumer_hygiene", "policy_violations"), "ui": "DataProductCatalogWorkbench", "route": "GET /scorecards"},
    44: {"tables": (PRODUCT_TABLE, CERTIFICATION_TABLE, SUBSCRIPTION_TABLE), "fields": ("product_card", "trust_badges", "preview_samples", "access_requirements", "comparison_view"), "ui": "DataProductCatalogWorkbench", "route": "GET /marketplace"},
    45: {"tables": (MODEL_TABLE, PRODUCT_TABLE, CONTRACT_TABLE, SCHEMA_TABLE), "fields": ("source_citations", "confidence", "affected_tables", "event_plan", "human_confirmation"), "ui": "DataProductCatalogAssistantPanel", "route": "POST /assistant/stewardship-plan"},
    46: {"tables": (CONTROL_TABLE, CONTRACT_TABLE, CERTIFICATION_TABLE, ACCESS_GRANT_TABLE), "fields": ("evidence_packet", "hashes", "event_lineage", "policy_versions", "export_manifest"), "ui": "DataProductCatalogDetail", "route": "POST /evidence-packets"},
    47: {"tables": (CONTROL_TABLE, OUTBOX_TABLE, INBOX_TABLE, DEAD_LETTER_TABLE), "fields": ("schema_hashes", "route_contracts", "event_schemas", "handler_proofs", "ui_coverage"), "ui": "DataProductCatalogWorkbench", "route": "GET /release-evidence"},
    48: {"tables": (PRODUCT_TABLE, CONTRACT_TABLE, SCHEMA_TABLE, ACCESS_GRANT_TABLE, CERTIFICATION_TABLE), "fields": ("transaction_time", "valid_time", "publication_time", "historical_snapshot"), "ui": "DataProductCatalogDetail", "route": "GET /data-products/time-travel"},
    49: {"tables": (INBOX_TABLE, OUTBOX_TABLE, DEAD_LETTER_TABLE), "fields": ("idempotency_key", "replay_action", "quarantine_reason", "dependency_health", "lineage"), "ui": "DataProductCatalogWorkbench", "route": "POST /events/replay"},
    50: {"tables": tuple(OWNED_TABLES), "fields": ("product_manager_view", "steward_view", "consumer_view", "approver_view", "auditor_view", "agent_panel"), "ui": "DataProductCatalogWorkbench", "route": "GET /workbench/pbcs/data_product_catalog"},
}


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
            "current_state": "published",
            "target_state": "certified",
            "approval_gate": "steward_review",
            "legal_basis": "contract",
            "risk_score": 0.24,
            "human_approval": True,
            "human_confirmation": True,
            "foreign_table_access": False,
            "source_citations": ("contract://customer360/v1",),
            "schema_hashes": ("sha256:contract",),
            "handler_proofs": ("idempotent",),
            "agent_panel": "DataProductCatalogAssistantPanel",
            "allowed_dependency_mode": "projection",
        }
    )
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    number = capability.feature_number
    if number == 1 and not payload.get("value_proposition"):
        findings.append("data product identity requires a value proposition")
    if number == 2 and payload.get("current_state") == payload.get("target_state"):
        findings.append("product lifecycle transition must change state")
    if number == 3 and not payload.get("owner_role"):
        findings.append("ownership accountability requires a named role")
    if number == 6 and payload.get("change_class") == "breaking" and not payload.get("required_approvals"):
        findings.append("breaking contract changes require approvals")
    if number == 14 and not payload.get("legal_basis"):
        findings.append("access request risk scoring requires legal basis")
    if number == 15 and payload.get("human_approval") is not True:
        findings.append("policy-aware access recommendations require human approval")
    if number == 26 and not payload.get("reviewer_approval"):
        findings.append("sensitive data classification requires reviewer approval")
    if number == 37 and not payload.get("simulation"):
        findings.append("policy studio changes require simulation evidence")
    if number == 38 and payload.get("allowed_dependency_mode", "projection") not in {"api", "event", "projection"}:
        findings.append("cross-PBC federation must use api, event, or projection dependency modes")
    if number == 45 and payload.get("human_confirmation") is not True:
        findings.append("agent-assisted stewardship requires human confirmation")
    if number == 47:
        for field in ("schema_hashes", "route_contracts", "event_schemas", "handler_proofs", "ui_coverage"):
            if not payload.get(field):
                findings.append(f"release evidence requires {field}")
    if number == 50:
        for field in ("product_manager_view", "steward_view", "consumer_view", "approver_view", "auditor_view", "agent_panel"):
            if not payload.get(field):
                findings.append(f"complete workbench coverage requires {field}")
    return tuple(findings)


def evaluate_data_product_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "pbc": PBC_KEY, "reason": "unknown_data_product_control", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    active_payload = sample_payload_for(resolved) if payload is None else dict(payload)
    missing = tuple(field for field in spec["fields"] if field not in active_payload or active_payload[field] in (None, ""))
    invalid_tables = tuple(table for table in spec["tables"] if table not in OWNED_TABLES)
    invalid_references = tuple(ref for ref in active_payload.get("references", ()) if isinstance(ref, str) and ref.endswith("_table") and ref not in OWNED_TABLES)
    domain_findings = _domain_findings(resolved, active_payload)
    event_type = "DataProductIncidentOpened" if domain_findings else "DataProductCreated"
    if resolved.feature_number in {5, 6, 33, 46} and not domain_findings:
        event_type = "DataContractPublished"
    if resolved.feature_number in {9, 10, 35, 42} and not domain_findings:
        event_type = "DataQualityChanged"
    if resolved.feature_number in {14, 15, 16} and not domain_findings:
        event_type = "DataAccessGranted"
    if resolved.feature_number in {19, 20} and not domain_findings:
        event_type = "DataProductCertified"
    return {
        "ok": not missing and not invalid_tables and not invalid_references and not domain_findings,
        "pbc": PBC_KEY,
        "capability": resolved.slug,
        "feature_number": resolved.feature_number,
        "title": resolved.title,
        "status": "implemented",
        "target_tables": spec["tables"],
        "owned_tables": OWNED_TABLES,
        "read_tables": (),
        "invalid_references": invalid_references,
        "missing_required_fields": missing,
        "domain_findings": domain_findings,
        "event": {"contract": EVENT_CONTRACT, "topic": REQUIRED_EVENT_TOPIC, "type": event_type, "idempotency_key": digest((PBC_KEY, resolved.slug, active_payload)), "outbox_table": OUTBOX_TABLE, "inbox_table": INBOX_TABLE, "dead_letter_table": DEAD_LETTER_TABLE},
        "ui_surface": spec["ui"],
        "service_api": spec["route"],
        "permission": "data_product_catalog.approve" if resolved.feature_number in {15, 16, 19, 26, 36, 40, 45} else "data_product_catalog.write",
        "configuration": {"database_backends": ALLOWED_DATABASE_BACKENDS, "event_topic": REQUIRED_EVENT_TOPIC, "stream_engine_picker_visible": False, "rule_configurable": True, "parameter_configurable": True},
        "agent_skill": f"data_product_catalog_skills.{resolved.slug}",
        "requires_human_confirmation": resolved.feature_number in {15, 16, 19, 24, 26, 36, 40, 45},
        "retry_dead_letter_evidence": {"retry_policy": "bounded_retry_with_idempotency_key", "dead_letter_table": DEAD_LETTER_TABLE, "manual_replay_route": "POST /events/replay"},
        "release_evidence": {"code_artifact_model": resolved.model_artifacts, "ui_surface": resolved.ui_artifacts, "service_api": resolved.service_artifacts, "test": resolved.test_artifacts, "evidence": resolved.evidence_artifacts},
        "shared_table_access": False,
        "side_effects": (),
    }


def improve1_data_product_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_data_product_control(capability) for capability in DATA_PRODUCT_CONTROL_CAPABILITIES)
    return {"ok": len(evaluations) == 50 and all(item["ok"] for item in evaluations), "pbc": PBC_KEY, "capability_count": len(evaluations), "capabilities": evaluations, "owned_tables": OWNED_TABLES, "database_backends": ALLOWED_DATABASE_BACKENDS, "event_contract": EVENT_CONTRACT, "event_topic": REQUIRED_EVENT_TOPIC, "stream_engine_picker_visible": False, "side_effects": ()}


DATA_PRODUCT_CONTROL_FUNCTIONS = {capability.slug: (lambda payload=None, slug=capability.slug: evaluate_data_product_control(slug, payload)) for capability in DATA_PRODUCT_CONTROL_CAPABILITIES}
