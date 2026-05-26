"""UI contract for the Inventory Positioning PBC."""

from __future__ import annotations

from .runtime import INVENTORY_POSITIONING_ALLOWED_DATABASE_BACKENDS
from .runtime import INVENTORY_POSITIONING_CONSUMED_EVENT_TYPES
from .runtime import INVENTORY_POSITIONING_EMITTED_EVENT_TYPES
from .runtime import INVENTORY_POSITIONING_OWNED_TABLES
from .runtime import INVENTORY_POSITIONING_REQUIRED_EVENT_TOPIC
from .runtime import inventory_positioning_permissions_contract


INVENTORY_POSITIONING_UI_FRAGMENT_KEYS = (
    "InventoryPositioningWorkbench",
    "ItemMasterConsole",
    "InventoryNodeConsole",
    "GoodsReceiptBoard",
    "InventoryAdjustmentConsole",
    "AvailabilityWorkbench",
    "AllocationConsole",
    "ReservationReleaseBoard",
    "QualityHoldPanel",
    "InTransitProjectionView",
    "LotSerialTraceabilityView",
    "ReplenishmentSignalConsole",
    "InventoryReconciliationBoard",
    "InventoryRiskPanel",
    "InventoryRuleStudio",
    "InventoryParameterConsole",
    "InventoryConfigurationPanel",
)


def inventory_positioning_ui_contract() -> dict:
    return {
        "format": "appgen.inventory-positioning-ui-contract.v1",
        "ok": True,
        "pbc": "inventory_positioning",
        "implementation_directory": "src/pyAppGen/pbcs/inventory_positioning",
        "fragments": INVENTORY_POSITIONING_UI_FRAGMENT_KEYS,
        "routes": (
            "/workbench/pbcs/inventory_positioning",
            "/workbench/pbcs/inventory_positioning/items",
            "/workbench/pbcs/inventory_positioning/nodes",
            "/workbench/pbcs/inventory_positioning/receipts",
            "/workbench/pbcs/inventory_positioning/adjustments",
            "/workbench/pbcs/inventory_positioning/availability",
            "/workbench/pbcs/inventory_positioning/allocations",
            "/workbench/pbcs/inventory_positioning/releases",
            "/workbench/pbcs/inventory_positioning/quality",
            "/workbench/pbcs/inventory_positioning/in-transit",
            "/workbench/pbcs/inventory_positioning/traceability",
            "/workbench/pbcs/inventory_positioning/replenishment",
            "/workbench/pbcs/inventory_positioning/reconciliation",
            "/workbench/pbcs/inventory_positioning/risk",
            "/workbench/pbcs/inventory_positioning/rules",
            "/workbench/pbcs/inventory_positioning/parameters",
            "/workbench/pbcs/inventory_positioning/configuration",
        ),
        "panels": (
            {
                "key": "master_data",
                "fragment": "ItemMasterConsole",
                "binds_to": ("item", "node", "identity"),
                "commands": ("register_item", "register_node", "verify_node_identity"),
            },
            {
                "key": "position",
                "fragment": "AvailabilityWorkbench",
                "binds_to": ("position", "receipt", "adjustment", "quality_hold"),
                "commands": ("post_goods_receipt", "post_adjustment", "calculate_availability", "apply_quality_hold"),
            },
            {
                "key": "allocation",
                "fragment": "AllocationConsole",
                "binds_to": ("allocation", "reservation", "outbox"),
                "commands": ("allocate_inventory", "release_allocation", "route_allocation", "optimize_allocation"),
            },
            {
                "key": "planning",
                "fragment": "ReplenishmentSignalConsole",
                "binds_to": ("in_transit", "replenishment_signal", "risk"),
                "commands": ("project_in_transit", "generate_replenishment_signal", "forecast_stockout", "score_stock_risk"),
            },
            {
                "key": "governance",
                "fragment": "InventoryRuleStudio",
                "binds_to": ("rule", "parameter", "configuration"),
                "commands": ("register_rule", "set_parameter", "configure_runtime"),
            },
        ),
        "action_permissions": inventory_positioning_permissions_contract()["action_permissions"],
        "configuration_editor": {
            "required_fields": ("database_backend", "event_topic", "retry_limit", "default_uom", "precision"),
            "allowed_database_backends": INVENTORY_POSITIONING_ALLOWED_DATABASE_BACKENDS,
            "required_event_topic": INVENTORY_POSITIONING_REQUIRED_EVENT_TOPIC,
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
            "user_selectable_event_contract": False,
        },
        "parameter_editor": {
            "numeric_parameters": (
                "safety_stock_percent",
                "partial_allocation_threshold",
                "reservation_ttl_minutes",
                "reconciliation_tolerance_units",
                "stockout_risk_threshold",
                "workbench_limit",
            ),
        },
        "rule_editor": {
            "rule_types": ("allocation", "availability", "reservation", "quality", "replenishment", "reconciliation", "release_gate"),
            "required_fields": ("rule_id", "tenant", "scope", "status"),
        },
        "event_surfaces": {
            "emits": INVENTORY_POSITIONING_EMITTED_EVENT_TYPES,
            "consumes": INVENTORY_POSITIONING_CONSUMED_EVENT_TYPES,
            "outbox_status": "visible",
            "inbox_status": "visible",
            "dead_letter_status": "visible",
        },
        "binding_evidence": {"owned_tables": INVENTORY_POSITIONING_OWNED_TABLES, "shared_table_access": False},
    }


def inventory_positioning_render_workbench(
    state: dict,
    *,
    tenant: str,
    principal_permissions: tuple[str, ...],
) -> dict:
    contract = inventory_positioning_ui_contract()
    permissions = set(principal_permissions)
    visible_actions = tuple(action for action, required in contract["action_permissions"].items() if required in permissions)
    positions = tuple(position for position in state["positions"].values() if position["tenant"] == tenant)
    allocations = tuple(allocation for allocation in state["allocations"].values() if allocation["tenant"] == tenant)
    cards = (
        {"key": "items", "value": len(tuple(item for item in state["items"].values() if item["tenant"] == tenant)), "fragment": "ItemMasterConsole"},
        {"key": "nodes", "value": len(tuple(node for node in state["nodes"].values() if node["tenant"] == tenant)), "fragment": "InventoryNodeConsole"},
        {"key": "positions", "value": len(positions), "fragment": "AvailabilityWorkbench"},
        {"key": "on_hand", "value": round(sum(position["on_hand"] for position in positions), 2), "fragment": "AvailabilityWorkbench"},
        {"key": "reserved", "value": round(sum(position["reserved"] for position in positions), 2), "fragment": "AllocationConsole"},
        {"key": "allocations", "value": len(allocations), "fragment": "AllocationConsole"},
        {"key": "rules", "value": len(state.get("rules", {})), "fragment": "InventoryRuleStudio"},
    )
    return {
        "format": "appgen.inventory-positioning-workbench-render.v1",
        "ok": True,
        "tenant": tenant,
        "route": "/workbench/pbcs/inventory_positioning",
        "fragments": contract["fragments"],
        "cards": cards,
        "visible_actions": visible_actions,
        "locked_actions": tuple(action for action in contract["action_permissions"] if action not in visible_actions),
        "configuration_bound": bool(state.get("configuration", {}).get("ok")),
        "rules_bound": tuple(sorted(state.get("rules", {}))),
        "parameters_bound": tuple(sorted(state.get("parameters", {}))),
        "event_outbox_count": len(state.get("outbox", ())),
        "inbox_count": len(state.get("inbox", ())),
        "dead_letter_count": len(state.get("dead_letter", state.get("dead_letters", ()))),
        "binding_evidence": {
            "owned_tables": INVENTORY_POSITIONING_OWNED_TABLES,
            "outbox_table": "inventory_positioning_appgen_outbox_event",
            "inbox_table": "inventory_positioning_appgen_inbox_event",
            "dead_letter_table": "inventory_positioning_dead_letter_event",
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
    contract = inventory_positioning_ui_contract()
    permissions = tuple(dict.fromkeys(contract.get("action_permissions", {}).values()))
    rendered = inventory_positioning_render_workbench(
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
