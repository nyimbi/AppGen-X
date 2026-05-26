"""UI contract for the Warehouse Management Core PBC."""

from __future__ import annotations


WMS_CORE_UI_FRAGMENT_KEYS = (
    "WarehouseExecutionWorkbench",
    "WarehouseMasterConsole",
    "BinLocationConsole",
    "InboundReceiptBoard",
    "PutawayTaskConsole",
    "PickWavePlanner",
    "PickExecutionBoard",
    "PackTaskConsole",
    "CartonizationPanel",
    "ShipmentConfirmationBoard",
    "CrossDockFlowView",
    "CycleCountConsole",
    "WarehouseExceptionBoard",
    "LaborTaskPanel",
    "EdgeDeviceReplayConsole",
    "WmsRuleStudio",
    "WmsParameterConsole",
    "WmsConfigurationPanel",
)


def wms_core_ui_contract() -> dict:
    return {
        "format": "appgen.wms-core-ui-contract.v1",
        "ok": True,
        "pbc": "wms_core",
        "implementation_directory": "src/pyAppGen/pbcs/wms_core",
        "fragments": WMS_CORE_UI_FRAGMENT_KEYS,
        "routes": (
            "/workbench/pbcs/wms_core",
            "/workbench/pbcs/wms_core/warehouses",
            "/workbench/pbcs/wms_core/bins",
            "/workbench/pbcs/wms_core/inbound",
            "/workbench/pbcs/wms_core/putaway",
            "/workbench/pbcs/wms_core/pick-waves",
            "/workbench/pbcs/wms_core/picking",
            "/workbench/pbcs/wms_core/packing",
            "/workbench/pbcs/wms_core/cartonization",
            "/workbench/pbcs/wms_core/shipments",
            "/workbench/pbcs/wms_core/cross-dock",
            "/workbench/pbcs/wms_core/cycle-count",
            "/workbench/pbcs/wms_core/exceptions",
            "/workbench/pbcs/wms_core/labor",
            "/workbench/pbcs/wms_core/edge",
            "/workbench/pbcs/wms_core/rules",
            "/workbench/pbcs/wms_core/parameters",
            "/workbench/pbcs/wms_core/configuration",
        ),
        "panels": (
            {
                "key": "warehouse",
                "fragment": "WarehouseMasterConsole",
                "binds_to": ("warehouse", "bin", "identity"),
                "commands": ("register_warehouse", "register_bin", "verify_warehouse_identity"),
            },
            {
                "key": "inbound",
                "fragment": "PutawayTaskConsole",
                "binds_to": ("receipt", "putaway_task", "bin"),
                "commands": ("receive_inbound", "create_putaway_task", "confirm_putaway"),
            },
            {
                "key": "outbound",
                "fragment": "PickWavePlanner",
                "binds_to": ("wave", "pick", "pack_task", "shipment"),
                "commands": ("create_pick_wave", "execute_pick", "create_pack_task", "confirm_pack", "confirm_shipment"),
            },
            {
                "key": "edge",
                "fragment": "EdgeDeviceReplayConsole",
                "binds_to": ("edge_command", "label", "outbox"),
                "commands": ("route_edge_command", "generate_shipment_proof", "run_resilience_drill"),
            },
            {
                "key": "governance",
                "fragment": "WmsRuleStudio",
                "binds_to": ("rule", "parameter", "configuration"),
                "commands": ("register_rule", "set_parameter", "configure_runtime"),
            },
        ),
        "action_permissions": {
            "register_warehouse": "wms_core.master",
            "register_bin": "wms_core.master",
            "receive_inbound": "wms_core.receive",
            "create_putaway_task": "wms_core.putaway",
            "confirm_putaway": "wms_core.putaway",
            "create_pick_wave": "wms_core.pick",
            "execute_pick": "wms_core.pick",
            "create_pack_task": "wms_core.pack",
            "confirm_pack": "wms_core.pack",
            "confirm_shipment": "wms_core.ship",
            "route_edge_command": "wms_core.edge",
            "generate_shipment_proof": "wms_core.audit",
            "register_rule": "wms_core.configure",
            "set_parameter": "wms_core.configure",
            "configure_runtime": "wms_core.configure",
            "run_control_tests": "wms_core.audit",
        },
        "configuration_editor": {
            "required_fields": ("database_backend", "event_topic", "retry_limit", "timezone", "label_format"),
            "allowed_database_backends": ("postgresql", "mysql", "mariadb"),
            "event_contract": "AppGen-X",
        },
        "parameter_editor": {
            "numeric_parameters": (
                "bin_capacity_tolerance",
                "pick_wave_size",
                "partial_pick_threshold",
                "dock_queue_warning",
                "labor_utilization_target",
                "workbench_limit",
            ),
        },
        "rule_editor": {
            "rule_types": ("putaway", "picking", "packing", "shipping", "cycle_count", "edge", "release_gate"),
            "required_fields": ("rule_id", "tenant", "scope", "status"),
        },
        "event_surfaces": {
            "emits": ("WarehouseRegistered", "BinRegistered", "GoodsReceiptPosted", "PutawayTaskCreated", "Picked", "Packed", "OrderShipped"),
            "consumes": ("InventoryAllocated", "InboundArrived", "QualityHoldReleased", "CarrierBooked", "AccessPolicyChanged"),
            "outbox_status": "visible",
            "dead_letter_status": "visible",
        },
    }


def wms_core_render_workbench(
    state: dict,
    *,
    tenant: str,
    principal_permissions: tuple[str, ...],
) -> dict:
    contract = wms_core_ui_contract()
    permissions = set(principal_permissions)
    visible_actions = tuple(action for action, required in contract["action_permissions"].items() if required in permissions)
    warehouses = tuple(item for item in state["warehouses"].values() if item["tenant"] == tenant)
    bins = tuple(item for item in state["bins"].values() if item["tenant"] == tenant)
    cards = (
        {"key": "warehouses", "value": len(warehouses), "fragment": "WarehouseMasterConsole"},
        {"key": "bins", "value": len(bins), "fragment": "BinLocationConsole"},
        {"key": "putaway", "value": len(tuple(item for item in state["putaway_tasks"].values() if item["tenant"] == tenant)), "fragment": "PutawayTaskConsole"},
        {"key": "waves", "value": len(tuple(item for item in state["waves"].values() if item["tenant"] == tenant)), "fragment": "PickWavePlanner"},
        {"key": "picks", "value": len(tuple(item for item in state["picks"].values() if item["tenant"] == tenant)), "fragment": "PickExecutionBoard"},
        {"key": "shipments", "value": len(tuple(item for item in state["shipments"].values() if item["tenant"] == tenant)), "fragment": "ShipmentConfirmationBoard"},
        {"key": "rules", "value": len(state.get("rules", {})), "fragment": "WmsRuleStudio"},
    )
    return {
        "format": "appgen.wms-core-workbench-render.v1",
        "ok": True,
        "tenant": tenant,
        "route": "/workbench/pbcs/wms_core",
        "fragments": contract["fragments"],
        "cards": cards,
        "visible_actions": visible_actions,
        "locked_actions": tuple(action for action in contract["action_permissions"] if action not in visible_actions),
        "configuration_bound": bool(state.get("configuration", {}).get("ok")),
        "rules_bound": tuple(sorted(state.get("rules", {}))),
        "parameters_bound": tuple(sorted(state.get("parameters", {}))),
        "event_outbox_count": len(state.get("outbox", ())),
    }
