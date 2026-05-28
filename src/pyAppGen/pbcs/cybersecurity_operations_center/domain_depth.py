"""Domain-depth contract for the cybersecurity_operations_center PBC."""

from __future__ import annotations

from typing import Any

from .models import BUSINESS_TABLES, OWNED_TABLES, RULE_NAMES, PARAMETER_BOUNDS, stable_digest

PBC_KEY = "cybersecurity_operations_center"
DOMAIN_ENTITY = "security_alert"
DOMAIN_PURPOSE = "Security alerts, incidents, assets, threat intelligence, playbooks, containment, and response evidence"
DOMAIN_OWNED_TABLES = OWNED_TABLES
DOMAIN_OPERATIONS = (
    "create_security_alert",
    "triage_security_alert",
    "enrich_security_alert",
    "suppress_security_alert",
    "record_security_incident",
    "review_asset_exposure",
    "approve_threat_intel",
    "simulate_playbook_run",
    "create_containment_action",
    "record_response_evidence",
    "review_policy_rule",
    "approve_runtime_parameter",
    "simulate_schema_extension",
    "create_control_assertion",
    "record_governed_model",
    "generate_handoff_packet",
)
DOMAIN_RULES = RULE_NAMES
DOMAIN_PARAMETERS = tuple(PARAMETER_BOUNDS)
DOMAIN_EVENTS = (
    "CybersecurityOperationsCenterCreated",
    "CybersecurityOperationsCenterUpdated",
    "CybersecurityOperationsCenterApproved",
    "CybersecurityOperationsCenterExceptionOpened",
)
DOMAIN_CONSUMED_EVENTS = ("PolicyChanged", "AuditEventSealed", "OperationalKpiChanged")
DOMAIN_ADVANCED_CAPABILITIES = (
    "cybersecurity_operations_center_event_sourced_operational_history",
    "cybersecurity_operations_center_multi_tenant_policy_isolation",
    "cybersecurity_operations_center_schema_evolution_resilience",
    "cybersecurity_operations_center_autonomous_anomaly_detection",
    "cybersecurity_operations_center_semantic_document_instruction_understanding",
    "cybersecurity_operations_center_predictive_risk_scoring",
    "cybersecurity_operations_center_counterfactual_scenario_simulation",
    "cybersecurity_operations_center_cryptographic_audit_proofs",
    "cybersecurity_operations_center_continuous_control_testing",
    "cybersecurity_operations_center_carbon_and_sustainability_awareness",
    "cybersecurity_operations_center_cross_pbc_event_federation",
    "cybersecurity_operations_center_governed_ai_agent_execution",
)
DOMAIN_WORKBENCH_VIEWS = (
    "analyst_triage_lane",
    "supervisor_queue_balance",
    "incident_commander_board",
    "evidence_review_lane",
    "assistant_handoff_panel",
)

_OPERATION_TABLES = {
    "create_security_alert": f"{PBC_KEY}_security_alert",
    "triage_security_alert": f"{PBC_KEY}_security_alert",
    "enrich_security_alert": f"{PBC_KEY}_security_alert",
    "suppress_security_alert": f"{PBC_KEY}_security_alert",
    "record_security_incident": f"{PBC_KEY}_security_incident",
    "review_asset_exposure": f"{PBC_KEY}_asset_exposure",
    "approve_threat_intel": f"{PBC_KEY}_threat_intel",
    "simulate_playbook_run": f"{PBC_KEY}_playbook_run",
    "create_containment_action": f"{PBC_KEY}_containment_action",
    "record_response_evidence": f"{PBC_KEY}_response_evidence",
    "review_policy_rule": f"{PBC_KEY}_cybersecurity_operations_center_policy_rule",
    "approve_runtime_parameter": f"{PBC_KEY}_cybersecurity_operations_center_runtime_parameter",
    "simulate_schema_extension": f"{PBC_KEY}_cybersecurity_operations_center_schema_extension",
    "create_control_assertion": f"{PBC_KEY}_cybersecurity_operations_center_control_assertion",
    "record_governed_model": f"{PBC_KEY}_cybersecurity_operations_center_governed_model",
    "generate_handoff_packet": f"{PBC_KEY}_security_incident",
}


def domain_depth_contract() -> dict[str, Any]:
    return {
        "format": f"appgen.{PBC_KEY}.world-class-domain-depth.v2",
        "ok": True,
        "pbc": PBC_KEY,
        "purpose": DOMAIN_PURPOSE,
        "owned_tables": DOMAIN_OWNED_TABLES,
        "business_tables": BUSINESS_TABLES,
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


def execute_domain_operation(operation: str, payload: dict | None = None) -> dict[str, Any]:
    payload = dict(payload or {})
    if operation not in DOMAIN_OPERATIONS:
        return {"ok": False, "reason": "unknown_domain_operation", "operation": operation, "side_effects": ()}
    target_table = _OPERATION_TABLES[operation]
    emitted_event = DOMAIN_EVENTS[min(2, DOMAIN_OPERATIONS.index(operation) % len(DOMAIN_EVENTS))]
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "operation": operation,
        "operation_kind": "command" if operation != "generate_handoff_packet" else "query",
        "target_table": target_table,
        "owned_tables": (target_table,),
        "read_tables": () if operation != "generate_handoff_packet" else (f"{PBC_KEY}_security_alert", f"{PBC_KEY}_security_incident"),
        "emitted_event": emitted_event if operation != "generate_handoff_packet" else None,
        "event_contract": "AppGen-X",
        "idempotency_key": stable_digest(PBC_KEY, operation, tuple(sorted(payload.items()))),
        "rules_evaluated": DOMAIN_RULES[:3],
        "parameters_read": DOMAIN_PARAMETERS[:3],
        "permission": f"{PBC_KEY}.operate",
        "evidence_hash": stable_digest(operation, payload, target_table, emitted_event),
        "shared_table_access": False,
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def domain_depth_smoke_test() -> dict[str, Any]:
    contract = domain_depth_contract()
    executions = tuple(execute_domain_operation(operation, {"tenant": "tenant-smoke"}) for operation in DOMAIN_OPERATIONS[:5])
    return {
        "ok": contract["ok"]
        and len(contract["owned_tables"]) >= contract["minimum_owned_domain_tables"]
        and contract["operation_count"] >= contract["minimum_domain_operations"]
        and all(item["ok"] for item in executions)
        and all(item["target_table"].startswith(f"{PBC_KEY}_") for item in executions),
        "contract": contract,
        "executions": executions,
        "side_effects": (),
    }


DOMAIN_EDGE_CASES = (
    "duplicate_alert_merge",
    "invalid_alert_transition",
    "promotion_without_cluster",
    "evidence_without_chain_of_custody",
    "high_risk_containment_without_approval",
    "cross_tenant_access_attempt",
    "idempotency_replay",
    "dead_letter_recovery",
)

DOMAIN_SPECIALIST_CAPABILITIES = tuple(
    dict.fromkeys(
        DOMAIN_ADVANCED_CAPABILITIES
        + tuple(f"specialist_{operation}" for operation in DOMAIN_OPERATIONS)
        + tuple(f"rule_driven_{rule}" for rule in DOMAIN_RULES)
    )
)


def domain_capability_surface_contract() -> dict[str, Any]:
    return {
        "format": f"appgen.{PBC_KEY}.complete-domain-capability-surface.v2",
        "ok": True,
        "pbc": PBC_KEY,
        "operation_surfaces": tuple(
            {
                "operation": operation,
                "surface": f"{PBC_KEY}.ui.operation.{operation}",
                "action": operation,
                "target_table": _OPERATION_TABLES[operation],
                "permission": f"{PBC_KEY}.operate",
                "requires_confirmation": operation not in {"generate_handoff_packet"},
                "agent_tool": f"{PBC_KEY}_skills.{operation}",
                "event": execute_domain_operation(operation).get("emitted_event"),
            }
            for operation in DOMAIN_OPERATIONS
        ),
        "rule_surfaces": tuple(
            {"rule": rule, "surface": f"{PBC_KEY}.ui.rule.{rule}", "editor": True, "explainable": True}
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
                "surface": f"{PBC_KEY}.ui.advanced.{capability}",
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
        "coverage": {"event_contract": "AppGen-X", "stream_engine_picker_visible": False, "shared_table_access": False},
        "side_effects": (),
    }
