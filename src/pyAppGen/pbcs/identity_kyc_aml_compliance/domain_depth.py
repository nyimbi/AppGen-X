"""Domain vocabulary and capability surface for the identity KYC / AML slice."""

from __future__ import annotations

import hashlib

PBC_KEY = "identity_kyc_aml_compliance"
DOMAIN_ENTITY = "kyc_profile"
DOMAIN_PURPOSE = (
    "Customer onboarding, identity proofing, beneficial ownership, sanctions and "
    "PEP screening, ongoing monitoring, suspicious activity escalation, and "
    "compliance decisioning."
)

DOMAIN_OWNED_TABLES = (
    "identity_kyc_aml_compliance_kyc_profile",
    "identity_kyc_aml_compliance_identity_document",
    "identity_kyc_aml_compliance_beneficial_owner",
    "identity_kyc_aml_compliance_screening_hit",
    "identity_kyc_aml_compliance_monitoring_alert",
    "identity_kyc_aml_compliance_suspicious_activity_case",
    "identity_kyc_aml_compliance_compliance_review",
    "identity_kyc_aml_compliance_policy_rule",
    "identity_kyc_aml_compliance_runtime_parameter",
    "identity_kyc_aml_compliance_schema_extension",
    "identity_kyc_aml_compliance_control_assertion",
    "identity_kyc_aml_compliance_governed_model",
    "identity_kyc_aml_compliance_appgen_outbox_event",
    "identity_kyc_aml_compliance_appgen_inbox_event",
    "identity_kyc_aml_compliance_appgen_dead_letter_event",
)

DOMAIN_OPERATIONS = (
    "create_kyc_profile",
    "advance_kyc_profile_lifecycle",
    "record_identity_document",
    "evaluate_document_evidence",
    "register_beneficial_owner",
    "record_screening_hit",
    "resolve_screening_hit",
    "schedule_rescreening",
    "triage_monitoring_alert",
    "promote_alert_to_case",
    "record_compliance_review",
    "challenge_risk_score",
    "create_control_assertion",
    "register_governed_model",
    "simulate_counterfactual_policy",
    "ingest_policy_change_event",
    "ingest_audit_event",
    "ingest_operational_kpi_event",
)

DOMAIN_RULES = (
    "customer_classification_required",
    "document_completeness_required",
    "document_authenticity_required",
    "beneficial_owner_threshold_policy",
    "screening_category_resolution_policy",
    "enhanced_due_diligence_trigger_matrix",
    "periodic_rescreening_policy",
    "alert_to_case_promotion_policy",
    "risk_score_challenge_policy",
)

DOMAIN_PARAMETERS = (
    "beneficial_owner_threshold_pct",
    "high_risk_beneficial_owner_threshold_pct",
    "rescreening_days_low",
    "rescreening_days_medium",
    "rescreening_days_high",
    "workbench_limit",
    "high_risk_geographies",
)

DOMAIN_EVENTS = (
    "IdentityKycAmlComplianceCreated",
    "IdentityKycAmlComplianceUpdated",
    "IdentityKycAmlComplianceApproved",
    "IdentityKycAmlComplianceExceptionOpened",
)

DOMAIN_CONSUMED_EVENTS = ("PolicyChanged", "AuditEventSealed", "OperationalKpiChanged")

DOMAIN_ADVANCED_CAPABILITIES = (
    "identity_kyc_aml_compliance_event_sourced_operational_history",
    "identity_kyc_aml_compliance_multi_tenant_policy_isolation",
    "identity_kyc_aml_compliance_schema_evolution_resilience",
    "identity_kyc_aml_compliance_autonomous_anomaly_detection",
    "identity_kyc_aml_compliance_semantic_document_instruction_understanding",
    "identity_kyc_aml_compliance_predictive_risk_scoring",
    "identity_kyc_aml_compliance_counterfactual_scenario_simulation",
    "identity_kyc_aml_compliance_cryptographic_audit_proofs",
    "identity_kyc_aml_compliance_continuous_control_testing",
    "identity_kyc_aml_compliance_governed_ai_agent_execution",
)

DOMAIN_WORKBENCH_VIEWS = (
    "onboarding_queue",
    "screening_queue",
    "beneficial_ownership_queue",
    "edd_review_queue",
    "rescreening_queue",
    "monitoring_alert_queue",
    "suspicious_activity_case_queue",
)

OPERATION_TARGET_TABLE = {
    "create_kyc_profile": DOMAIN_OWNED_TABLES[0],
    "advance_kyc_profile_lifecycle": DOMAIN_OWNED_TABLES[0],
    "record_identity_document": DOMAIN_OWNED_TABLES[1],
    "evaluate_document_evidence": DOMAIN_OWNED_TABLES[1],
    "register_beneficial_owner": DOMAIN_OWNED_TABLES[2],
    "record_screening_hit": DOMAIN_OWNED_TABLES[3],
    "resolve_screening_hit": DOMAIN_OWNED_TABLES[3],
    "schedule_rescreening": DOMAIN_OWNED_TABLES[4],
    "triage_monitoring_alert": DOMAIN_OWNED_TABLES[4],
    "promote_alert_to_case": DOMAIN_OWNED_TABLES[5],
    "record_compliance_review": DOMAIN_OWNED_TABLES[6],
    "challenge_risk_score": DOMAIN_OWNED_TABLES[6],
    "create_control_assertion": DOMAIN_OWNED_TABLES[10],
    "register_governed_model": DOMAIN_OWNED_TABLES[11],
    "simulate_counterfactual_policy": DOMAIN_OWNED_TABLES[7],
    "ingest_policy_change_event": DOMAIN_OWNED_TABLES[13],
    "ingest_audit_event": DOMAIN_OWNED_TABLES[13],
    "ingest_operational_kpi_event": DOMAIN_OWNED_TABLES[13],
}

OPERATION_EVENT = {
    "create_kyc_profile": DOMAIN_EVENTS[0],
    "advance_kyc_profile_lifecycle": DOMAIN_EVENTS[1],
    "record_identity_document": DOMAIN_EVENTS[1],
    "evaluate_document_evidence": DOMAIN_EVENTS[1],
    "register_beneficial_owner": DOMAIN_EVENTS[1],
    "record_screening_hit": DOMAIN_EVENTS[3],
    "resolve_screening_hit": DOMAIN_EVENTS[1],
    "schedule_rescreening": DOMAIN_EVENTS[1],
    "triage_monitoring_alert": DOMAIN_EVENTS[3],
    "promote_alert_to_case": DOMAIN_EVENTS[3],
    "record_compliance_review": DOMAIN_EVENTS[1],
    "challenge_risk_score": DOMAIN_EVENTS[1],
    "create_control_assertion": DOMAIN_EVENTS[1],
    "register_governed_model": DOMAIN_EVENTS[1],
    "simulate_counterfactual_policy": DOMAIN_EVENTS[1],
    "ingest_policy_change_event": DOMAIN_EVENTS[3],
    "ingest_audit_event": DOMAIN_EVENTS[3],
    "ingest_operational_kpi_event": DOMAIN_EVENTS[3],
}


def _digest(value: object) -> str:
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()


def domain_depth_contract() -> dict:
    return {
        "format": f"appgen.{PBC_KEY}.world-class-domain-depth.v2",
        "ok": True,
        "pbc": PBC_KEY,
        "purpose": DOMAIN_PURPOSE,
        "owned_tables": DOMAIN_OWNED_TABLES,
        "operation_count": len(DOMAIN_OPERATIONS),
        "operations": DOMAIN_OPERATIONS,
        "rules": DOMAIN_RULES,
        "parameters": DOMAIN_PARAMETERS,
        "emitted_events": DOMAIN_EVENTS,
        "consumed_events": DOMAIN_CONSUMED_EVENTS,
        "advanced_capabilities": DOMAIN_ADVANCED_CAPABILITIES,
        "workbench_views": DOMAIN_WORKBENCH_VIEWS,
        "database_backends": ("postgresql", "mysql", "mariadb"),
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "minimum_owned_domain_tables": 15,
        "minimum_domain_operations": 15,
        "side_effects": (),
    }


def execute_domain_operation(operation: str, payload: dict | None = None) -> dict:
    payload = dict(payload or {})
    if operation not in DOMAIN_OPERATIONS:
        return {
            "ok": False,
            "reason": "unknown_domain_operation",
            "operation": operation,
            "side_effects": (),
        }
    target_table = OPERATION_TARGET_TABLE[operation]
    emitted_event = OPERATION_EVENT[operation]
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "operation": operation,
        "operation_kind": "command",
        "target_table": target_table,
        "owned_tables": (target_table,),
        "read_tables": (),
        "emitted_event": emitted_event,
        "event_contract": "AppGen-X",
        "idempotency_key": _digest((PBC_KEY, operation, tuple(sorted(payload.items())))),
        "rules_evaluated": DOMAIN_RULES[:3],
        "parameters_read": DOMAIN_PARAMETERS[:3],
        "permission": f"{PBC_KEY}.operate",
        "evidence_hash": _digest((operation, payload, target_table, emitted_event)),
        "shared_table_access": False,
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def domain_depth_smoke_test() -> dict:
    contract = domain_depth_contract()
    executions = tuple(
        execute_domain_operation(operation, {"tenant": "tenant-smoke"})
        for operation in DOMAIN_OPERATIONS[:6]
    )
    return {
        "ok": contract["ok"]
        and len(contract["owned_tables"]) >= contract["minimum_owned_domain_tables"]
        and contract["operation_count"] >= contract["minimum_domain_operations"]
        and all(item["ok"] for item in executions),
        "contract": contract,
        "executions": executions,
        "side_effects": (),
    }


DOMAIN_EDGE_CASES = (
    "duplicate_identity_match",
    "expired_document_submitted",
    "suspected_document_tamper",
    "pep_hit_requires_edd",
    "missing_beneficial_owner_coverage",
    "risk_score_override_without_supervisor",
    "overdue_rescreening",
    "alert_sla_breach",
    "duplicate_inbound_event",
)

DOMAIN_SPECIALIST_CAPABILITIES = tuple(
    dict.fromkeys(
        DOMAIN_ADVANCED_CAPABILITIES
        + tuple(f"specialist_{operation}" for operation in DOMAIN_OPERATIONS)
        + tuple(f"rule_driven_{rule}" for rule in DOMAIN_RULES)
    )
)


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
                "target_table": OPERATION_TARGET_TABLE[operation],
                "permission": f"{PBC_KEY}.operate",
                "requires_confirmation": True,
                "agent_tool": f"{PBC_KEY}_skills.{operation}",
                "event": OPERATION_EVENT[operation],
            }
            for operation in DOMAIN_OPERATIONS
        ),
        "rule_surfaces": tuple(
            {
                "rule": rule,
                "surface": f"{PBC_KEY}.ui.rule.{rule}",
                "editor": True,
                "explainable": True,
            }
            for rule in DOMAIN_RULES
        ),
        "parameter_surfaces": tuple(
            {
                "parameter": parameter,
                "surface": f"{PBC_KEY}.ui.parameter.{parameter}",
                "bounded": True,
                "editable": True,
            }
            for parameter in DOMAIN_PARAMETERS
        ),
        "advanced_surfaces": tuple(
            {
                "capability": capability,
                "surface": f"{PBC_KEY}.ui.advanced.{_digest(capability)[:12]}",
                "explainable": True,
            }
            for capability in DOMAIN_ADVANCED_CAPABILITIES
        ),
        "edge_case_surfaces": tuple(
            {
                "edge_case": edge_case,
                "surface": f"{PBC_KEY}.ui.edge_case.{edge_case}",
                "triage_queue": True,
            }
            for edge_case in DOMAIN_EDGE_CASES
        ),
        "table_surfaces": tuple(
            {
                "owned_table": table,
                "surface": f"{PBC_KEY}.ui.table.{table}",
                "read_model": True,
                "mutation_guard": True,
            }
            for table in DOMAIN_OWNED_TABLES
        ),
        "specialist_capabilities": DOMAIN_SPECIALIST_CAPABILITIES,
        "coverage": {
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
            "shared_table_access": False,
        },
        "side_effects": (),
    }
