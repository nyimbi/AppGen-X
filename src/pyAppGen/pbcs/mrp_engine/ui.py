"""UI contract for the Material Requirements Planning PBC."""

from __future__ import annotations

from .runtime import MRP_ENGINE_ALLOWED_DATABASE_BACKENDS
from .runtime import MRP_ENGINE_CONSUMED_EVENT_TYPES
from .runtime import MRP_ENGINE_EMITTED_EVENT_TYPES
from .runtime import MRP_ENGINE_OWNED_TABLES
from .runtime import MRP_ENGINE_REQUIRED_EVENT_TOPIC


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
            "register_bom": "mrp_engine.master",
            "ingest_demand_projection": "mrp_engine.plan",
            "ingest_inventory_projection": "mrp_engine.plan",
            "create_mrp_run": "mrp_engine.plan",
            "calculate_material_plan": "mrp_engine.plan",
            "release_planned_order": "mrp_engine.release",
            "receive_event": "mrp_engine.event",
            "register_rule": "mrp_engine.configure",
            "register_schema_extension": "mrp_engine.configure",
            "set_parameter": "mrp_engine.configure",
            "configure_runtime": "mrp_engine.configure",
            "run_control_tests": "mrp_engine.audit",
        },
        "configuration_editor": {
            "required_fields": ("database_backend", "event_topic", "retry_limit", "default_planning_bucket"),
            "allowed_database_backends": MRP_ENGINE_ALLOWED_DATABASE_BACKENDS,
            "event_contract": "AppGen-X",
            "fixed_event_topic": MRP_ENGINE_REQUIRED_EVENT_TOPIC,
            "stream_engine_picker_visible": False,
            "user_selectable_event_contract": False,
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
            "emits": MRP_ENGINE_EMITTED_EVENT_TYPES,
            "consumes": MRP_ENGINE_CONSUMED_EVENT_TYPES,
            "outbox_status": "visible",
            "inbox_status": "visible",
            "dead_letter_status": "visible",
        },
        "binding_evidence": {
            "owned_tables": MRP_ENGINE_OWNED_TABLES,
            "outbox_table": "mrp_engine_appgen_outbox_event",
            "inbox_table": "mrp_engine_appgen_inbox_event",
            "dead_letter_table": "mrp_engine_dead_letter_event",
            "rbac_permissions": (
                "mrp_engine.read",
                "mrp_engine.master",
                "mrp_engine.plan",
                "mrp_engine.release",
                "mrp_engine.event",
                "mrp_engine.configure",
                "mrp_engine.audit",
            ),
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
        "event_inbox_count": len(state.get("inbox", ())),
        "dead_letter_count": len(state.get("dead_letter", state.get("dead_letters", ()))),
        "binding_evidence": {
            "owned_tables": MRP_ENGINE_OWNED_TABLES,
            "configuration": {
                "event_contract": state.get("configuration", {}).get("event_contract"),
                "event_topic": state.get("configuration", {}).get("event_topic"),
                "stream_engine_picker_visible": state.get("configuration", {}).get("stream_engine_picker_visible"),
            },
            "outbox_table": "mrp_engine_appgen_outbox_event",
            "inbox_table": "mrp_engine_appgen_inbox_event",
            "dead_letter_table": "mrp_engine_dead_letter_event",
        },
    }

class _AppGenSmokeState(dict):
    """Tolerant empty state for side-effect-free workbench smoke rendering."""

    def __missing__(self, key):
        value = _AppGenSmokeState()
        self[key] = value
        return value


def _appgen_smoke_state():
    """Return a deterministic state envelope understood by PBC workbench renderers."""
    return _AppGenSmokeState({
        "configuration": _AppGenSmokeState({"ok": True}),
        "rules": _AppGenSmokeState(),
        "parameters": _AppGenSmokeState(),
        "outbox": (),
        "inbox": (),
        "dead_letter": (),
        "dead_letters": (),
        "events": (),
    })


def smoke_test():
    """Exercise the PBC workbench contract and render path without side effects."""
    contract = mrp_engine_ui_contract()
    permissions = tuple(dict.fromkeys(contract.get("action_permissions", {}).values()))
    rendered = mrp_engine_render_workbench(
        _appgen_smoke_state(),
        tenant="smoke",
        principal_permissions=permissions,
    )
    cards = tuple(rendered.get("cards") or contract.get("panels") or contract.get("fragments", ()))
    configuration_editor = contract.get("configuration_editor", {})
    event_surfaces = contract.get("event_surfaces", {})
    rule_editor = contract.get("rule_editor") or {
        "rule_types": ("configuration", "parameter", "release_gate"),
        "required_fields": ("rule_id", "scope", "status"),
    }
    binding_evidence = contract.get("binding_evidence") or {"shared_table_access": False}
    governance = {
        "configuration_editor": configuration_editor,
        "parameter_editor": contract.get("parameter_editor", {}),
        "rule_editor": rule_editor,
        "event_surfaces": event_surfaces,
        "binding_evidence": binding_evidence,
    }
    return {
        "format": "appgen.pbc-ui-smoke-test.v1",
        "ok": contract.get("ok") is True
        and rendered.get("ok") is True
        and bool(contract.get("fragments"))
        and bool(contract.get("routes"))
        and bool(cards)
        and bool(contract.get("action_permissions"))
        and bool(configuration_editor)
        and configuration_editor.get("stream_engine_picker_visible", configuration_editor.get("user_facing_stream_engine_picker", False)) is False
        and bool(contract.get("parameter_editor"))
        and bool(rule_editor)
        and bool(event_surfaces)
        and ("outbox_status" in event_surfaces or "contract" in event_surfaces)
        and binding_evidence.get("shared_table_access") is not True
        and not binding_evidence.get("shared_tables", ()),
        "manifest": {"fragments": contract.get("fragments", ()), "routes": contract.get("routes", ())},
        "contract": contract,
        "governance": governance,
        "rendered": rendered,
        "cards": cards,
        "side_effects": (),
    }



def mrp_engine_form_contracts() -> dict:
    contracts = (
        {'key': 'MrpConfigurationForm', 'operation': 'configure_runtime', 'table': 'mrp_engine_mrp_configuration', 'fields': ('database_backend', 'event_topic', 'retry_limit', 'allowed_sites', 'default_planning_bucket'), 'permission': 'mrp_engine.configure', 'keywords': ('configure', 'planning bucket', 'backend')},
        {'key': 'MrpRuleForm', 'operation': 'register_rule', 'table': 'mrp_engine_mrp_rule', 'fields': ('rule_id', 'tenant', 'rule_type', 'allowed_sites', 'allowed_bom_statuses', 'demand_sources', 'release_routes', 'status'), 'permission': 'mrp_engine.configure', 'keywords': ('rule', 'substitution', 'release route')},
        {'key': 'BomForm', 'operation': 'register_bom', 'table': 'mrp_engine_bill_of_material', 'fields': ('bom_id', 'tenant', 'parent_item', 'component_item', 'component_qty', 'scrap_percent', 'revision', 'status', 'site'), 'permission': 'mrp_engine.master', 'keywords': ('bom', 'component', 'scrap')},
        {'key': 'DemandProjectionForm', 'operation': 'ingest_demand_projection', 'table': 'mrp_engine_material_demand', 'fields': ('demand_id', 'tenant', 'item', 'site', 'quantity', 'source', 'need_date'), 'permission': 'mrp_engine.plan', 'keywords': ('demand', 'forecast', 'sales order')},
        {'key': 'InventoryProjectionForm', 'operation': 'ingest_inventory_projection', 'table': 'mrp_engine_inventory_projection', 'fields': ('inventory_id', 'tenant', 'item', 'site', 'available_qty', 'quality_status'), 'permission': 'mrp_engine.plan', 'keywords': ('inventory', 'released stock', 'quality status')},
        {'key': 'MrpRunForm', 'operation': 'create_mrp_run', 'table': 'mrp_engine_mrp_run', 'fields': ('run_id', 'tenant', 'site', 'horizon_days', 'scenario', 'planner'), 'permission': 'mrp_engine.plan', 'keywords': ('run', 'netting', 'scenario')},
    )
    return {'format': 'appgen.mrp-engine-standalone-forms.v1', 'ok': all(item['table'].startswith('mrp_engine_') for item in contracts), 'pbc': 'mrp_engine', 'contracts': contracts, 'side_effects': ()}


def mrp_engine_wizard_contracts() -> dict:
    contracts = (
        {'key': 'PlanningDocumentIntakeWizard', 'steps': ('parse_document', 'map_bom_demand_inventory', 'preview_mutations', 'require_confirmation'), 'forms': ('BomForm', 'DemandProjectionForm', 'InventoryProjectionForm'), 'keywords': ('document', 'instruction', 'demand', 'bom')},
        {'key': 'MrpRunWizard', 'steps': ('validate_configuration', 'create_run', 'explode_bom', 'net_supply_demand'), 'forms': ('MrpRunForm',), 'keywords': ('run', 'mrp', 'planning')},
        {'key': 'NettingAndPeggingWizard', 'steps': ('explode_bom', 'calculate_shortage', 'peg_shortage', 'create_planned_orders'), 'forms': ('DemandProjectionForm', 'InventoryProjectionForm'), 'keywords': ('netting', 'pegging', 'shortage')},
        {'key': 'PlannedOrderReleaseWizard', 'steps': ('screen_policy', 'generate_supply_proof', 'release_order', 'publish_appgen_event'), 'forms': ('MrpRunForm',), 'keywords': ('release', 'planned order', 'purchase suggestion')},
    )
    return {'format': 'appgen.mrp-engine-standalone-wizards.v1', 'ok': all(item['steps'] for item in contracts), 'pbc': 'mrp_engine', 'contracts': contracts, 'side_effects': ()}


def mrp_engine_control_catalog() -> dict:
    contracts = (
        {'key': 'mrp_backend_event_contract', 'operation': 'run_control_tests', 'table': 'mrp_engine_mrp_control_assertion', 'permission': 'mrp_engine.audit'},
        {'key': 'mrp_shortage_netting_control', 'operation': 'run_control_tests', 'table': 'mrp_engine_mrp_control_assertion', 'permission': 'mrp_engine.audit'},
        {'key': 'supply_availability_proof', 'operation': 'generate_supply_proof', 'table': 'mrp_engine_supply_availability_proof', 'permission': 'mrp_engine.audit'},
    )
    return {'format': 'appgen.mrp-engine-standalone-controls.v1', 'ok': all(item['table'].startswith('mrp_engine_') for item in contracts), 'pbc': 'mrp_engine', 'contracts': contracts, 'side_effects': ()}


def mrp_engine_standalone_workbench_blueprint() -> dict:
    forms = mrp_engine_form_contracts(); wizards = mrp_engine_wizard_contracts(); controls = mrp_engine_control_catalog()
    return {'format': 'appgen.mrp-engine-standalone-workbench.v1', 'ok': forms['ok'] and wizards['ok'] and controls['ok'], 'pbc': 'mrp_engine', 'forms': forms['contracts'], 'wizards': wizards['contracts'], 'controls': controls['contracts'], 'panels': mrp_engine_ui_contract()['panels'], 'side_effects': ()}


def mrp_engine_render_standalone_workbench(workbench: dict) -> dict:
    blueprint = mrp_engine_standalone_workbench_blueprint()
    cards = (
        {'key': 'boms', 'value': workbench.get('bom_count', workbench.get('bom_edge_count', 0)), 'fragment': 'BomGraphExplorer'},
        {'key': 'demands', 'value': workbench.get('demand_count', 0), 'fragment': 'DemandConsole'},
        {'key': 'runs', 'value': workbench.get('run_count', workbench.get('mrp_run_count', 0)), 'fragment': 'MrpRunControl'},
        {'key': 'planned_orders', 'value': workbench.get('planned_order_count', 0), 'fragment': 'PlannedOrderBoard'},
        {'key': 'shortage_total', 'value': workbench.get('shortage_total', 0), 'fragment': 'ShortageBoard'},
    )
    return {'format': 'appgen.mrp-engine-standalone-render.v1', 'ok': blueprint['ok'] and bool(cards), 'pbc': 'mrp_engine', 'tenant': workbench.get('tenant'), 'cards': cards, 'forms': tuple(item['key'] for item in blueprint['forms']), 'wizards': tuple(item['key'] for item in blueprint['wizards']), 'controls': tuple(item['key'] for item in blueprint['controls']), 'side_effects': ()}
