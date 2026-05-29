"""UI contract and standalone workbench surface for the wms_core PBC."""

from __future__ import annotations

from .runtime import WMS_CORE_ALLOWED_DATABASE_BACKENDS
from .runtime import WMS_CORE_CONSUMED_EVENT_TYPES
from .runtime import WMS_CORE_EMITTED_EVENT_TYPES
from .runtime import WMS_CORE_OWNED_TABLES
from .runtime import WMS_CORE_REQUIRED_EVENT_TOPIC
from .runtime import wms_core_build_workbench_view
from .runtime import wms_core_permissions_contract


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
WMS_CORE_FORM_KEYS = (
    "warehouse_registration_form",
    "bin_slotting_form",
    "inbound_receipt_form",
    "putaway_policy_form",
    "pick_wave_release_form",
    "pack_confirmation_form",
)
WMS_CORE_WIZARD_KEYS = (
    "warehouse_readiness_wizard",
    "inbound_to_putaway_wizard",
    "wave_to_ship_wizard",
)
WMS_CORE_CONTROL_KEYS = (
    "tenant_scope_picker",
    "dock_board_timeline",
    "bin_capacity_heatmap",
    "event_reliability_drawer",
    "shipment_proof_banner",
    "assistant_skill_panel",
)


def wms_core_form_catalog() -> tuple[dict, ...]:
    return (
        {
            "key": "warehouse_registration_form",
            "title": "Warehouse Registration",
            "command": "register_warehouse",
            "owned_table": "warehouse",
            "fields": (
                "warehouse_id",
                "tenant",
                "name",
                "timezone",
                "zones",
                "dock_doors",
                "pack_stations",
                "calendar",
                "identity",
            ),
        },
        {
            "key": "bin_slotting_form",
            "title": "Bin Slotting",
            "command": "register_bin",
            "owned_table": "bin_location",
            "fields": (
                "bin_id",
                "tenant",
                "warehouse_id",
                "zone",
                "capacity",
                "current_load",
                "status",
                "temperature",
                "hazard",
                "pick_sequence",
            ),
        },
        {
            "key": "inbound_receipt_form",
            "title": "Inbound Receipt",
            "command": "receive_inbound",
            "owned_table": "inbound_receipt",
            "fields": (
                "receipt_id",
                "tenant",
                "warehouse_id",
                "dock_door",
                "item_id",
                "quantity",
                "lot_id",
            ),
        },
        {
            "key": "putaway_policy_form",
            "title": "Putaway Policy",
            "command": "register_rule",
            "owned_table": "wms_rule",
            "fields": (
                "rule_id",
                "tenant",
                "scope",
                "status",
                "preferred_zones",
                "pack_material",
                "hazard_compatible",
            ),
        },
        {
            "key": "pick_wave_release_form",
            "title": "Wave Release",
            "command": "create_pick_wave",
            "owned_table": "pick_wave",
            "fields": ("wave_id", "tenant", "warehouse_id", "orders", "method"),
        },
        {
            "key": "pack_confirmation_form",
            "title": "Pack Confirmation",
            "command": "confirm_pack",
            "owned_table": "pack_task",
            "fields": ("pack_id", "station", "label_id"),
        },
    )


def wms_core_wizard_catalog() -> tuple[dict, ...]:
    return (
        {
            "key": "warehouse_readiness_wizard",
            "steps": (
                "warehouse_registration_form",
                "bin_slotting_form",
                "putaway_policy_form",
            ),
            "goal": "Stand up one warehouse with governed topology, bin capacity, and release rules.",
        },
        {
            "key": "inbound_to_putaway_wizard",
            "steps": (
                "inbound_receipt_form",
                "putaway_policy_form",
                "bin_slotting_form",
            ),
            "goal": "Move inbound freight from dock receipt to directed putaway inside WMS-owned tables only.",
        },
        {
            "key": "wave_to_ship_wizard",
            "steps": (
                "pick_wave_release_form",
                "pack_confirmation_form",
            ),
            "goal": "Release a wave, pick, pack, and produce shipment-proof evidence from one workbench session.",
        },
    )


def wms_core_control_catalog() -> tuple[dict, ...]:
    return (
        {"key": "tenant_scope_picker", "type": "selector", "binds_to": "tenant"},
        {"key": "dock_board_timeline", "type": "timeline", "binds_to": "inbound_receipt"},
        {"key": "bin_capacity_heatmap", "type": "heatmap", "binds_to": "bin_location"},
        {"key": "event_reliability_drawer", "type": "drawer", "binds_to": "event_reliability"},
        {"key": "shipment_proof_banner", "type": "banner", "binds_to": "warehouse_shipment_proof"},
        {"key": "assistant_skill_panel", "type": "assistant", "binds_to": "wms_core_skills"},
    )


def wms_core_standalone_app_contract() -> dict:
    return {
        "ok": True,
        "pbc": "wms_core",
        "app_id": "wms_core_one_pbc_app",
        "workbench_route": "/workbench/pbcs/wms_core",
        "navigation": (
            {"key": "masters", "route": "/workbench/pbcs/wms_core/warehouses"},
            {"key": "inbound", "route": "/workbench/pbcs/wms_core/inbound"},
            {"key": "outbound", "route": "/workbench/pbcs/wms_core/pick-waves"},
            {"key": "shipments", "route": "/workbench/pbcs/wms_core/shipments"},
            {"key": "exceptions", "route": "/workbench/pbcs/wms_core/exceptions"},
            {"key": "governance", "route": "/workbench/pbcs/wms_core/configuration"},
        ),
        "forms": WMS_CORE_FORM_KEYS,
        "wizards": WMS_CORE_WIZARD_KEYS,
        "controls": WMS_CORE_CONTROL_KEYS,
        "single_agent_namespace": "wms_core_skills",
        "side_effects": (),
    }


def wms_core_ui_contract() -> dict:
    shell = wms_core_standalone_app_contract()
    return {
        "format": "appgen.wms-core-ui-contract.v1",
        "ok": True,
        "pbc": "wms_core",
        "implementation_directory": "src/pyAppGen/pbcs/wms_core",
        "fragments": WMS_CORE_UI_FRAGMENT_KEYS,
        "routes": tuple(item["route"] for item in shell["navigation"]) + (shell["workbench_route"],),
        "panels": (
            {
                "key": "warehouse",
                "fragment": "WarehouseMasterConsole",
                "binds_to": ("warehouse", "bin_location", "warehouse_identity"),
                "commands": ("register_warehouse", "register_bin", "verify_warehouse_identity"),
            },
            {
                "key": "inbound",
                "fragment": "InboundReceiptBoard",
                "binds_to": ("inbound_receipt", "putaway_task", "dock_appointment"),
                "commands": ("receive_inbound", "create_putaway_task", "confirm_putaway"),
            },
            {
                "key": "outbound",
                "fragment": "PickWavePlanner",
                "binds_to": ("pick_wave", "pick_task", "pack_task", "shipment_confirmation"),
                "commands": (
                    "create_pick_wave",
                    "execute_pick",
                    "create_pack_task",
                    "confirm_pack",
                    "confirm_shipment",
                ),
            },
            {
                "key": "edge",
                "fragment": "EdgeDeviceReplayConsole",
                "binds_to": ("edge_device_command", "label_evidence", "wms_core_appgen_outbox_event"),
                "commands": ("route_edge_command", "generate_shipment_proof", "run_resilience_drill"),
            },
            {
                "key": "governance",
                "fragment": "WmsRuleStudio",
                "binds_to": ("wms_rule", "wms_parameter", "wms_configuration"),
                "commands": ("register_rule", "set_parameter", "configure_runtime", "run_control_tests"),
            },
        ),
        "forms": wms_core_form_catalog(),
        "wizards": wms_core_wizard_catalog(),
        "controls": wms_core_control_catalog(),
        "standalone_app": shell,
        "action_permissions": wms_core_permissions_contract()["action_permissions"],
        "configuration_editor": {
            "required_fields": (
                "database_backend",
                "event_topic",
                "retry_limit",
                "timezone",
                "label_format",
                "edge_device_mode",
                "workbench_limit",
            ),
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
            "bounded_supported_parameters": True,
        },
        "rule_editor": {
            "rule_types": (
                "putaway",
                "picking",
                "packing",
                "shipping",
                "cycle_count",
                "edge",
                "release_gate",
            ),
            "required_fields": (
                "rule_id",
                "tenant",
                "scope",
                "status",
                "preferred_zones",
            ),
            "compiled_evidence_required": True,
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
            "shared_table_access": False,
            "required_event_topic": WMS_CORE_REQUIRED_EVENT_TOPIC,
            "rbac_permissions": wms_core_permissions_contract()["permissions"],
        },
    }


def wms_core_render_workbench(
    state: dict,
    *,
    tenant: str,
    principal_permissions: tuple[str, ...],
) -> dict:
    contract = wms_core_ui_contract()
    shell = wms_core_standalone_app_contract()
    snapshot = wms_core_build_workbench_view(state, tenant=tenant)
    permissions = set(principal_permissions)
    visible_actions = tuple(
        action
        for action, required_permission in contract["action_permissions"].items()
        if required_permission in permissions
    )
    return {
        "format": "appgen.wms-core-workbench-render.v1",
        "ok": True,
        "tenant": tenant,
        "route": shell["workbench_route"],
        "fragments": contract["fragments"],
        "navigation": shell["navigation"],
        "forms": contract["forms"],
        "wizards": contract["wizards"],
        "controls": contract["controls"],
        "cards": (
            {"key": "warehouses", "value": snapshot["warehouse_count"], "fragment": "WarehouseMasterConsole"},
            {"key": "bins", "value": snapshot["bin_count"], "fragment": "BinLocationConsole"},
            {"key": "putaway", "value": snapshot["putaway_count"], "fragment": "PutawayTaskConsole"},
            {"key": "waves", "value": snapshot["wave_count"], "fragment": "PickWavePlanner"},
            {"key": "picked", "value": snapshot["picked_count"], "fragment": "PickExecutionBoard"},
            {"key": "packed", "value": snapshot["packed_count"], "fragment": "PackTaskConsole"},
            {"key": "shipments", "value": snapshot["shipment_count"], "fragment": "ShipmentConfirmationBoard"},
        ),
        "visible_actions": visible_actions,
        "locked_actions": tuple(action for action in contract["action_permissions"] if action not in visible_actions),
        "configuration_bound": snapshot["configuration_bound"],
        "rules_bound": tuple(sorted(state.get("rules", {}))),
        "parameters_bound": tuple(sorted(state.get("parameters", {}))),
        "event_outbox_count": len(state.get("outbox", ())),
        "event_inbox_count": snapshot["inbox_count"],
        "dead_letter_count": snapshot["dead_letter_count"],
        "binding_evidence": snapshot["binding_evidence"],
        "workbench": snapshot,
    }


def wms_core_render_standalone_app(
    state: dict,
    *,
    tenant: str,
    principal_permissions: tuple[str, ...] | None = None,
) -> dict:
    contract = wms_core_ui_contract()
    permissions = principal_permissions or tuple(sorted(set(contract["action_permissions"].values())))
    rendered = wms_core_render_workbench(
        state,
        tenant=tenant,
        principal_permissions=permissions,
    )
    return {
        "ok": rendered["ok"],
        "pbc": "wms_core",
        "shell": wms_core_standalone_app_contract(),
        "workbench": rendered,
        "side_effects": (),
    }


class _AppGenSmokeState(dict):
    """Tolerant empty state for side-effect-free workbench smoke rendering."""

    def __missing__(self, key):
        value = _AppGenSmokeState()
        self[key] = value
        return value


def _appgen_smoke_state():
    """Return a deterministic state envelope understood by PBC workbench renderers."""
    return _AppGenSmokeState(
        {
            "warehouses": _AppGenSmokeState(),
            "bins": _AppGenSmokeState(),
            "putaway_tasks": _AppGenSmokeState(),
            "waves": _AppGenSmokeState(),
            "picks": _AppGenSmokeState(),
            "pack_tasks": _AppGenSmokeState(),
            "shipments": _AppGenSmokeState(),
            "configuration": _AppGenSmokeState({"ok": True}),
            "rules": _AppGenSmokeState(),
            "parameters": _AppGenSmokeState(),
            "outbox": (),
            "inbox": (),
            "dead_letter": (),
            "dead_letters": (),
            "events": (),
        }
    )


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
        and bool(contract.get("forms"))
        and bool(contract.get("wizards"))
        and bool(contract.get("controls"))
        and bool(cards)
        and bool(contract.get("action_permissions"))
        and bool(configuration_editor)
        and configuration_editor.get(
            "stream_engine_picker_visible",
            configuration_editor.get("user_facing_stream_engine_picker", False),
        )
        is False
        and bool(contract.get("parameter_editor"))
        and bool(rule_editor)
        and bool(event_surfaces)
        and ("outbox_status" in event_surfaces or "contract" in event_surfaces)
        and binding_evidence.get("shared_table_access") is not True
        and not binding_evidence.get("shared_tables", ()),
        "manifest": {
            "fragments": contract.get("fragments", ()),
            "routes": contract.get("routes", ()),
            "forms": tuple(item["key"] for item in contract.get("forms", ())),
            "wizards": tuple(item["key"] for item in contract.get("wizards", ())),
            "controls": tuple(item["key"] for item in contract.get("controls", ())),
        },
        "contract": contract,
        "governance": governance,
        "rendered": rendered,
        "cards": cards,
        "side_effects": (),
    }
