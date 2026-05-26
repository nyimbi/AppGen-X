"""UI contract for the Material Requirements Planning PBC."""

from __future__ import annotations


MRP_ENGINE_UI_FRAGMENT_KEYS = (
    "MrpEngineWorkbench",
    "BomGraphExplorer",
    "DemandConsole",
    "MrpRunControl",
    "ShortageBoard",
    "PlannedOrderBoard",
    "MrpRuleStudio",
    "MrpParameterConsole",
    "MrpConfigurationPanel",
)


def mrp_engine_ui_contract() -> dict:
    return {
        "format": "appgen.mrp-engine-ui-contract.v1",
        "ok": True,
        "pbc": "mrp_engine",
        "implementation_directory": "src/pyAppGen/pbcs/mrp_engine",
        "fragments": MRP_ENGINE_UI_FRAGMENT_KEYS,
        "routes": (
            "/workbench/pbcs/mrp_engine",
            "/workbench/pbcs/mrp_engine/boms",
            "/workbench/pbcs/mrp_engine/demand",
            "/workbench/pbcs/mrp_engine/runs",
            "/workbench/pbcs/mrp_engine/shortages",
            "/workbench/pbcs/mrp_engine/planned-orders",
            "/workbench/pbcs/mrp_engine/rules",
            "/workbench/pbcs/mrp_engine/parameters",
            "/workbench/pbcs/mrp_engine/configuration",
        ),
        "panels": (
            {
                "key": "bom_graph",
                "fragment": "BomGraphExplorer",
                "binds_to": ("bill_of_material", "material_demand"),
                "commands": ("register_bom", "explode_bom"),
            },
            {
                "key": "planning_run",
                "fragment": "MrpRunControl",
                "binds_to": ("mrp_run", "material_demand", "planned_order"),
                "commands": ("create_mrp_run", "calculate_material_plan", "simulate_planning_policy"),
            },
            {
                "key": "planned_orders",
                "fragment": "PlannedOrderBoard",
                "binds_to": ("planned_order", "outbox", "dead_letter"),
                "commands": ("release_planned_order", "route_supply", "generate_supply_proof"),
            },
            {
                "key": "governance_studio",
                "fragment": "MrpRuleStudio",
                "binds_to": ("rule", "parameter", "configuration"),
                "commands": ("register_rule", "set_parameter", "configure_runtime", "run_control_tests"),
            },
        ),
        "action_permissions": {
            "register_bom": "mrp_engine.plan",
            "ingest_demand_projection": "mrp_engine.plan",
            "ingest_inventory_projection": "mrp_engine.plan",
            "create_mrp_run": "mrp_engine.plan",
            "calculate_material_plan": "mrp_engine.plan",
            "release_planned_order": "mrp_engine.release",
            "register_rule": "mrp_engine.configure",
            "set_parameter": "mrp_engine.configure",
            "configure_runtime": "mrp_engine.configure",
            "run_control_tests": "mrp_engine.audit",
        },
        "configuration_editor": {
            "required_fields": ("database_backend", "event_topic", "retry_limit", "default_planning_bucket"),
            "allowed_database_backends": ("postgresql", "mysql", "mariadb"),
            "event_contract": "AppGen-X",
        },
        "parameter_editor": {
            "numeric_parameters": (
                "planning_horizon_days",
                "bucket_size_days",
                "safety_stock_multiplier",
                "lot_size_minimum",
                "lead_time_days",
                "capacity_threshold",
                "shortage_severity_threshold",
            ),
        },
        "rule_editor": {
            "rule_types": ("planning", "shortage", "substitution", "release", "capacity", "exception"),
            "required_fields": ("rule_id", "tenant", "rule_type", "eligible_item_types", "allowed_sites", "status"),
        },
        "event_surfaces": {
            "emits": ("MaterialShortageDetected", "PlannedOrderReleased"),
            "consumes": ("InventoryReleased", "OrderVerified", "ForecastUpdated"),
            "outbox_status": "visible",
            "dead_letter_status": "visible",
        },
    }


def mrp_engine_render_workbench(
    state: dict,
    *,
    tenant: str,
    principal_permissions: tuple[str, ...],
) -> dict:
    contract = mrp_engine_ui_contract()
    permissions = set(principal_permissions)
    action_permissions = contract["action_permissions"]
    visible_actions = tuple(
        action
        for action, required_permission in action_permissions.items()
        if required_permission in permissions
    )
    tenant_boms = tuple(bom for bom in state["boms"].values() if bom["tenant"] == tenant)
    tenant_demands = tuple(demand for demand in state["demands"].values() if demand["tenant"] == tenant)
    tenant_runs = tuple(run for run in state["mrp_runs"].values() if run["tenant"] == tenant)
    tenant_orders = tuple(order for order in state["planned_orders"].values() if order["tenant"] == tenant)
    cards = (
        {"key": "bom_edges", "value": len(tenant_boms), "fragment": "BomGraphExplorer"},
        {"key": "demand_count", "value": len(tenant_demands), "fragment": "DemandConsole"},
        {"key": "mrp_runs", "value": len(tenant_runs), "fragment": "MrpRunControl"},
        {"key": "planned_orders", "value": len(tenant_orders), "fragment": "PlannedOrderBoard"},
        {"key": "shortage_total", "value": round(sum(order["shortage_qty"] for order in tenant_orders), 2), "fragment": "ShortageBoard"},
        {"key": "released_orders", "value": len(tuple(order for order in tenant_orders if order["status"] == "released")), "fragment": "PlannedOrderBoard"},
    )
    return {
        "format": "appgen.mrp-engine-workbench-render.v1",
        "ok": True,
        "tenant": tenant,
        "route": "/workbench/pbcs/mrp_engine",
        "fragments": contract["fragments"],
        "cards": cards,
        "visible_actions": visible_actions,
        "locked_actions": tuple(action for action in action_permissions if action not in visible_actions),
        "configuration_bound": bool(state["configuration"].get("ok")),
        "rules_bound": tuple(sorted(state["rules"])),
        "parameters_bound": tuple(sorted(state["parameters"])),
        "event_outbox_count": len(state["outbox"]),
    }
