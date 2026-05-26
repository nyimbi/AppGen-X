"""UI contract for the Warehouse Management Core PBC."""

from __future__ import annotations

from .runtime import WMS_CORE_ALLOWED_DATABASE_BACKENDS
from .runtime import WMS_CORE_CONSUMED_EVENT_TYPES
from .runtime import WMS_CORE_EMITTED_EVENT_TYPES
from .runtime import WMS_CORE_OWNED_TABLES
from .runtime import WMS_CORE_REQUIRED_EVENT_TOPIC


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
            "receive_event": "wms_core.event",
            "generate_shipment_proof": "wms_core.audit",
            "register_rule": "wms_core.configure",
            "register_schema_extension": "wms_core.configure",
            "set_parameter": "wms_core.configure",
            "configure_runtime": "wms_core.configure",
            "run_control_tests": "wms_core.audit",
        },
        "configuration_editor": {
            "required_fields": ("database_backend", "event_topic", "retry_limit", "timezone", "label_format"),
            "allowed_database_backends": WMS_CORE_ALLOWED_DATABASE_BACKENDS,
            "event_contract": "AppGen-X",
            "fixed_event_topic": WMS_CORE_REQUIRED_EVENT_TOPIC,
            "stream_engine_picker_visible": False,
            "user_selectable_event_contract": False,
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
            "emits": WMS_CORE_EMITTED_EVENT_TYPES,
            "consumes": WMS_CORE_CONSUMED_EVENT_TYPES,
            "outbox_status": "visible",
            "inbox_status": "visible",
            "dead_letter_status": "visible",
        },
        "binding_evidence": {
            "owned_tables": WMS_CORE_OWNED_TABLES,
            "outbox_table": "wms_core_appgen_outbox_event",
            "inbox_table": "wms_core_appgen_inbox_event",
            "dead_letter_table": "wms_core_dead_letter_event",
            "rbac_permissions": (
                "wms_core.read",
                "wms_core.master",
                "wms_core.receive",
                "wms_core.putaway",
                "wms_core.pick",
                "wms_core.pack",
                "wms_core.ship",
                "wms_core.count",
                "wms_core.edge",
                "wms_core.event",
                "wms_core.configure",
                "wms_core.audit",
            ),
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
        "event_inbox_count": len(state.get("inbox", ())),
        "dead_letter_count": len(state.get("dead_letter", state.get("dead_letters", ()))),
        "binding_evidence": {
            "owned_tables": WMS_CORE_OWNED_TABLES,
            "configuration": {
                "event_contract": state.get("configuration", {}).get("event_contract"),
                "event_topic": state.get("configuration", {}).get("event_topic"),
                "stream_engine_picker_visible": state.get("configuration", {}).get("stream_engine_picker_visible"),
            },
            "outbox_table": "wms_core_appgen_outbox_event",
            "inbox_table": "wms_core_appgen_inbox_event",
            "dead_letter_table": "wms_core_dead_letter_event",
            "rbac_permissions": contract["binding_evidence"]["rbac_permissions"],
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
    contract = wms_core_ui_contract()
    permissions = tuple(dict.fromkeys(contract.get("action_permissions", {}).values()))
    rendered = wms_core_render_workbench(
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
