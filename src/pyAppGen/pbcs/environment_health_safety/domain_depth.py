"""World-class domain depth contract for the environment_health_safety PBC."""

from __future__ import annotations

from . import standalone

PBC_KEY = standalone.PBC_KEY
DOMAIN_ENTITY = "ehs_incident"
DOMAIN_PURPOSE = standalone.PBC_DESCRIPTION
DOMAIN_OWNED_TABLES = standalone.OWNED_TABLES
DOMAIN_OPERATIONS = standalone.DOMAIN_OPERATIONS
DOMAIN_RULES = tuple(standalone.RULE_DEFINITIONS.keys())
DOMAIN_PARAMETERS = tuple(standalone.PARAMETER_DEFINITIONS.keys())
DOMAIN_EVENTS = standalone.EMITTED_EVENT_TYPES
DOMAIN_CONSUMED_EVENTS = standalone.CONSUMED_EVENT_TYPES
DOMAIN_ADVANCED_CAPABILITIES = standalone.ADVANCED_CAPABILITY_KEYS
DOMAIN_WORKBENCH_VIEWS = (
    "incident_queue",
    "hazard_register",
    "inspection_due_queue",
    "permit_conflicts",
    "corrective_action_effectiveness",
    "release_evidence",
)
DOMAIN_EDGE_CASES = (
    "incident_closure_blocked",
    "serious_notification_overdue",
    "duplicate_inspection_sync",
    "permit_conflict_detected",
    "corrective_action_failed_effectiveness",
    "policy_change_re_evaluation",
    "audit_seal_requires_amendment",
    "kpi_priority_recalculation",
)
DOMAIN_SPECIALIST_CAPABILITIES = tuple(
    dict.fromkeys(
        standalone.ADVANCED_CAPABILITY_KEYS
        + tuple(f"specialist_{operation}" for operation in DOMAIN_OPERATIONS)
        + tuple(f"rule_driven_{rule}" for rule in DOMAIN_RULES)
    )
)


def domain_depth_contract() -> dict:
    return standalone.domain_depth_contract()


def execute_domain_operation(operation: str, payload: dict | None = None) -> dict:
    return standalone.execute_domain_operation(operation, payload)


def domain_depth_smoke_test() -> dict:
    smoke = standalone.smoke_test()
    return {
        "ok": smoke["ok"],
        "contract": standalone.domain_depth_contract(),
        "executions": tuple(
            standalone.execute_domain_operation(
                operation,
                {"tenant": "tenant-smoke", "incident_id": "INC-100", "new_status": "triaged"},
            )
            if operation == "advance_incident_lifecycle"
            else standalone.execute_domain_operation(operation, {"tenant": "tenant-smoke"})
            for operation in DOMAIN_OPERATIONS[:4]
        ),
        "side_effects": (),
    }


def domain_capability_surface_contract() -> dict:
    contract = standalone.domain_capability_surface_contract()
    contract["specialist_capabilities"] = DOMAIN_SPECIALIST_CAPABILITIES
    contract["edge_case_surfaces"] = tuple(
        {
            "edge_case": edge_case,
            "surface": f"{PBC_KEY}.ui.edge_case.{edge_case}",
            "triage_queue": True,
        }
        for edge_case in DOMAIN_EDGE_CASES
    )
    return contract
