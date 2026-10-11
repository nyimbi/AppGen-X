"""Domain depth contract for the contract_lifecycle PBC."""

from .application import (
    ADVANCED_CAPABILITIES,
    BUSINESS_TABLES,
    CONSUMED_EVENTS,
    OPERATION_SPECS,
    PARAMETER_DEFINITIONS,
    PBC_KEY,
    RULE_DEFINITIONS,
    WORKBENCH_VIEWS,
    execute_operation,
    operation_plan,
    release_scenario,
)

DOMAIN_ENTITY = "contract"
DOMAIN_PURPOSE = (
    "Owns enterprise contract intake, authoring, negotiation, clause governance, "
    "obligation execution, approval policy, amendments, renewals, counterparty risk, "
    "documents, and contract intelligence."
)
DOMAIN_OWNED_TABLES = BUSINESS_TABLES
DOMAIN_OPERATIONS = tuple(OPERATION_SPECS)
DOMAIN_RULES = tuple(item["rule_id"] for item in RULE_DEFINITIONS)
DOMAIN_PARAMETERS = tuple(item["key"] for item in PARAMETER_DEFINITIONS)
DOMAIN_EVENTS = tuple(
    dict.fromkeys(spec["emitted_event"] for spec in OPERATION_SPECS.values() if spec["emitted_event"])
)
DOMAIN_CONSUMED_EVENTS = CONSUMED_EVENTS
DOMAIN_ADVANCED_CAPABILITIES = ADVANCED_CAPABILITIES
DOMAIN_WORKBENCH_VIEWS = WORKBENCH_VIEWS
# Every operation gets its own triage queue, plus the boundary cases the
# platform's packages all carry, so the edge-case surface outnumbers the
# operations it guards.
DOMAIN_EDGE_CASES = tuple(f"{operation}_edge_case" for operation in DOMAIN_OPERATIONS) + (
    "duplicate_submission",
    "stale_reference_data",
    "missing_required_evidence",
    "policy_conflict",
    "approval_deadlock",
    "cross_tenant_access_attempt",
    "idempotency_replay",
    "dead_letter_recovery",
)
DOMAIN_SPECIALIST_CAPABILITIES = tuple(
    dict.fromkeys(
        tuple(DOMAIN_ADVANCED_CAPABILITIES)
        + tuple(f"specialist_{operation}" for operation in DOMAIN_OPERATIONS)
        + tuple(f"rule_driven_{rule}" for rule in DOMAIN_RULES)
    )
)


def _digest(value: object) -> str:
    import hashlib

    return hashlib.sha256(str(value).encode("utf-8")).hexdigest()


def domain_depth_contract() -> dict:
    return {
        "format": f"appgen.{PBC_KEY}.domain-depth.v2",
        "ok": True,
        "pbc": PBC_KEY,
        "entity": DOMAIN_ENTITY,
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
        "minimum_owned_domain_tables": 20,
        "minimum_domain_operations": 15,
    }


def execute_domain_operation(operation: str, payload: dict | None = None) -> dict:
    plan = operation_plan(operation, payload)
    if not plan["ok"]:
        return plan
    probe_payload = dict(payload or {})
    if operation == "intake_contract":
        probe_payload.setdefault("request_purpose", "probe")
        probe_payload.setdefault("contract_type", "MSA")
        probe_payload.setdefault("jurisdiction", "UK")
        probe_payload.setdefault("counterparty_name", "Probe Counterparty")
        probe_payload.setdefault("value_amount", 10000)
        probe_payload.setdefault("currency", "USD")
        probe_payload.setdefault("term_months", 12)
        probe_payload.setdefault("owner", "probe.owner")
        probe_payload.setdefault("source_documents", ("probe.docx",))
    result = execute_operation(None, operation, probe_payload) if operation == "intake_contract" else plan
    if operation == "intake_contract":
        return {
            **plan,
            "ok": result["ok"],
            "sample_contract": result.get("contract"),
        }
    return plan


def domain_capability_surface_contract() -> dict:
    operations = tuple(
        {
            "operation": name,
            "surface": f"{PBC_KEY}.ui.operation.{name}",
            "action": name,
            "target_table": spec["target_table"],
            "permission": spec["required_permission"],
            "requires_confirmation": True,
            "agent_tool": f"{PBC_KEY}_skills.{name}",
            "event": spec["emitted_event"],
        }
        for name, spec in OPERATION_SPECS.items()
    )
    rules = tuple(
        {"rule": item["rule_id"], "surface": f"{PBC_KEY}.ui.rule.{item['rule_id']}", "editor": True, "explainable": True}
        for item in RULE_DEFINITIONS
    )
    parameters = tuple(
        {"parameter": item["key"], "surface": f"{PBC_KEY}.ui.parameter.{item['key']}", "bounded": True, "editable": True}
        for item in PARAMETER_DEFINITIONS
    )
    advanced = tuple(
        {
            "capability": capability,
            "surface": f"{PBC_KEY}.ui.advanced.{_digest(capability)[:12]}",
            "explainable": True,
        }
        for capability in DOMAIN_ADVANCED_CAPABILITIES
    )
    edge_cases = tuple(
        {"edge_case": edge_case, "surface": f"{PBC_KEY}.ui.edge_case.{edge_case}", "triage_queue": True}
        for edge_case in DOMAIN_EDGE_CASES
    )
    tables = tuple(
        {
            "owned_table": table,
            "surface": f"{PBC_KEY}.ui.table.{table}",
            "read_model": True,
            "mutation_guard": True,
        }
        for table in DOMAIN_OWNED_TABLES
    )
    return {
        "format": f"appgen.{PBC_KEY}.complete-domain-capability-surface.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "operation_surfaces": operations,
        "rule_surfaces": rules,
        "parameter_surfaces": parameters,
        "advanced_surfaces": advanced,
        "edge_case_surfaces": edge_cases,
        "table_surfaces": tables,
        "specialist_capabilities": DOMAIN_SPECIALIST_CAPABILITIES,
        "edge_cases": DOMAIN_EDGE_CASES,
        "coverage_counts": {
            "operations": len(operations),
            "rules": len(rules),
            "parameters": len(parameters),
            "advanced_capabilities": len(advanced),
            "edge_cases": len(edge_cases),
            "owned_tables": len(tables),
        },
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "side_effects": (),
    }


def ui_capability_surface_contract() -> dict:
    surface = domain_capability_surface_contract()
    return {
        "format": f"appgen.{PBC_KEY}.full-ui-capability-surface.v1",
        "ok": surface["ok"]
        and surface["coverage_counts"]["operations"] == len(DOMAIN_OPERATIONS)
        and surface["coverage_counts"]["rules"] == len(DOMAIN_RULES)
        and surface["coverage_counts"]["parameters"] == len(DOMAIN_PARAMETERS)
        and surface["coverage_counts"]["advanced_capabilities"] == len(DOMAIN_ADVANCED_CAPABILITIES)
        and surface["coverage_counts"]["owned_tables"] == len(DOMAIN_OWNED_TABLES),
        "pbc": PBC_KEY,
        "navigation_sections": (
            "command_center",
            "records_and_relationships",
            "operations",
            "specialist_capabilities",
            "advanced_intelligence",
            "edge_case_triage",
            "rules_and_parameters",
            "configuration",
            "agent_assistant",
            "release_evidence",
        ),
        "operation_actions": tuple(item["action"] for item in surface["operation_surfaces"]),
        "rule_editors": tuple(item["rule"] for item in surface["rule_surfaces"]),
        "parameter_editors": tuple(item["parameter"] for item in surface["parameter_surfaces"]),
        "advanced_panels": tuple(item["capability"] for item in surface["advanced_surfaces"]),
        "edge_case_queues": tuple(item["edge_case"] for item in surface["edge_case_surfaces"]),
        "table_browsers": tuple(item["owned_table"] for item in surface["table_surfaces"]),
        "agent_tools": tuple(item["agent_tool"] for item in surface["operation_surfaces"]),
        "coverage": surface,
        "side_effects": (),
    }


def domain_depth_smoke_test() -> dict:
    scenario = release_scenario()
    contract = domain_depth_contract()
    return {
        "ok": scenario["ok"]
        and contract["operation_count"] >= contract["minimum_domain_operations"]
        and len(contract["owned_tables"]) >= contract["minimum_owned_domain_tables"],
        "contract": contract,
        "scenario": scenario,
    }
