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
    ui_contract,
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
            "event": spec["emitted_event"],
        }
        for name, spec in OPERATION_SPECS.items()
    )
    rules = tuple(
        {"rule": item["rule_id"], "surface": f"{PBC_KEY}.ui.rule.{item['rule_id']}", "editor": True}
        for item in RULE_DEFINITIONS
    )
    parameters = tuple(
        {"parameter": item["key"], "surface": f"{PBC_KEY}.ui.parameter.{item['key']}", "bounded": True}
        for item in PARAMETER_DEFINITIONS
    )
    return {
        "format": f"appgen.{PBC_KEY}.domain-capability-surface.v2",
        "ok": True,
        "pbc": PBC_KEY,
        "operation_surfaces": operations,
        "rule_surfaces": rules,
        "parameter_surfaces": parameters,
        "coverage_counts": {
            "operations": len(operations),
            "rules": len(rules),
            "parameters": len(parameters),
            "owned_tables": len(DOMAIN_OWNED_TABLES),
        },
        "advanced_capabilities": DOMAIN_ADVANCED_CAPABILITIES,
    }


def ui_capability_surface_contract() -> dict:
    ui = ui_contract()
    coverage = domain_capability_surface_contract()
    return {
        "format": f"appgen.{PBC_KEY}.ui-capability-surface.v2",
        "ok": ui["ok"] and coverage["ok"],
        "pbc": PBC_KEY,
        "navigation_sections": ui["workbench_views"],
        "operation_actions": tuple(item["operation"] for item in coverage["operation_surfaces"]),
        "rule_editors": tuple(item["rule"] for item in coverage["rule_surfaces"]),
        "parameter_editors": tuple(item["parameter"] for item in coverage["parameter_surfaces"]),
        "advanced_panels": ui["advanced_capabilities"],
        "edge_case_queues": ("exceptions_and_events", "approval_queue", "obligation_command_center"),
        "table_browsers": DOMAIN_OWNED_TABLES,
        "agent_tools": tuple(f"{PBC_KEY}_{name}" for name in DOMAIN_OPERATIONS),
        "coverage": coverage,
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
