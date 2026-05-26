"""UI contract for the Inventory Positioning PBC."""

from __future__ import annotations


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
        "action_permissions": {
            "register_item": "inventory_positioning.master",
            "register_node": "inventory_positioning.master",
            "post_goods_receipt": "inventory_positioning.receive",
            "post_adjustment": "inventory_positioning.adjust",
            "calculate_availability": "inventory_positioning.read",
            "allocate_inventory": "inventory_positioning.allocate",
            "release_allocation": "inventory_positioning.release",
            "apply_quality_hold": "inventory_positioning.quality",
            "reconcile_inventory": "inventory_positioning.reconcile",
            "generate_stock_proof": "inventory_positioning.audit",
            "register_rule": "inventory_positioning.configure",
            "set_parameter": "inventory_positioning.configure",
            "configure_runtime": "inventory_positioning.configure",
            "run_control_tests": "inventory_positioning.audit",
        },
        "configuration_editor": {
            "required_fields": ("database_backend", "event_topic", "retry_limit", "default_uom", "precision"),
            "allowed_database_backends": ("postgresql", "mysql", "mariadb"),
            "event_contract": "AppGen-X",
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
            "emits": ("ItemRegistered", "InventoryNodeRegistered", "GoodsReceiptPosted", "InventoryAdjusted", "InventoryAllocated", "InventoryReleased", "QualityHoldApplied"),
            "consumes": ("OrderVerified", "ShipmentDelivered", "QualityHoldReleased", "PurchaseReceiptPosted", "DemandForecastChanged"),
            "outbox_status": "visible",
            "dead_letter_status": "visible",
        },
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
    }
