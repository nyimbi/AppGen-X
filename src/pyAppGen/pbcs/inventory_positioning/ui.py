"""UI contract for the Inventory Positioning standalone PBC."""

from __future__ import annotations

from .permissions import permission_manifest
from .runtime import INVENTORY_POSITIONING_ALLOWED_DATABASE_BACKENDS
from .runtime import INVENTORY_POSITIONING_CONSUMED_EVENT_TYPES
from .runtime import INVENTORY_POSITIONING_EMITTED_EVENT_TYPES
from .runtime import INVENTORY_POSITIONING_OWNED_TABLES
from .runtime import INVENTORY_POSITIONING_REQUIRED_EVENT_TOPIC
from .runtime import inventory_positioning_build_workbench_view
from .runtime import inventory_positioning_configure_runtime
from .runtime import inventory_positioning_empty_state


INVENTORY_POSITIONING_UI_FRAGMENT_KEYS = (
    "InventoryPositioningWorkbench",
    "ItemMasterConsole",
    "InventoryNodeConsole",
    "GoodsReceiptBoard",
    "InventoryAdjustmentConsole",
    "AvailabilityWorkbench",
    "AllocationConsole",
    "QualityHoldPanel",
    "TraceabilityPanel",
    "ReplenishmentSignalConsole",
    "InventoryConfigurationPanel",
    "InventoryAgentPanel",
)


def inventory_positioning_ui_contract() -> dict:
    permissions = permission_manifest()
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
            "/workbench/pbcs/inventory_positioning/quality",
            "/workbench/pbcs/inventory_positioning/replenishment",
            "/workbench/pbcs/inventory_positioning/configuration",
            "/workbench/pbcs/inventory_positioning/agent",
        ),
        "panels": (
            {"key": "master_data", "fragment": "ItemMasterConsole", "commands": ("register_item", "register_node"), "binds_to": ("item", "node", "identity")},
            {"key": "inventory_flow", "fragment": "GoodsReceiptBoard", "commands": ("post_goods_receipt", "post_adjustment", "apply_quality_hold"), "binds_to": ("receipt", "adjustment", "quality_hold")},
            {"key": "allocation", "fragment": "AllocationConsole", "commands": ("calculate_availability", "allocate_inventory", "release_allocation"), "binds_to": ("allocation", "reservation", "position")},
            {"key": "planning", "fragment": "ReplenishmentSignalConsole", "commands": ("generate_replenishment_signal", "reconcile_inventory"), "binds_to": ("replenishment", "reconciliation", "risk")},
            {"key": "governance", "fragment": "InventoryConfigurationPanel", "commands": ("configure_runtime", "set_parameter", "register_rule", "register_schema_extension"), "binds_to": ("configuration", "parameter", "rule", "schema_extension")},
            {"key": "assistant", "fragment": "InventoryAgentPanel", "commands": ("generate_stock_proof",), "binds_to": ("agent", "documents", "crud_plan")},
        ),
        "forms": (
            {"key": "item_master_form", "fields": ("tenant", "item_id", "sku", "uom", "lot_tracked", "serial_tracked", "substitution_group")},
            {"key": "node_master_form", "fields": ("tenant", "node_id", "node_type", "country", "region", "calendar", "identity.did", "identity.issuer")},
            {"key": "goods_receipt_form", "fields": ("tenant", "receipt_id", "node_id", "item_id", "quantity", "lot_id", "expires")},
            {"key": "allocation_form", "fields": ("allocation_id", "tenant", "order_id", "item_id", "quantity", "demand_class")},
            {"key": "quality_hold_form", "fields": ("hold_id", "node_id", "item_id", "quantity", "reason")},
        ),
        "wizards": (
            {"key": "inventory_readiness_wizard", "steps": ("configure_runtime", "register_rule", "seed_master_data", "post_initial_receipt", "verify_workbench")},
            {"key": "allocation_preview_wizard", "steps": ("lookup_availability", "apply_rule_context", "preview_allocation", "review_risk", "confirm")},
            {"key": "reconciliation_wizard", "steps": ("select_item", "load_ledger", "enter_physical_count", "variance_review", "resolution_plan")},
        ),
        "controls": (
            {"key": "demand_class_selector", "type": "segmented_control", "options": ("premium", "standard", "backorder")},
            {"key": "safety_stock_slider", "type": "number", "min": 0.0, "max": 1.0, "step": 0.01},
            {"key": "reservation_ttl_input", "type": "integer", "min": 1, "max": 10080},
            {"key": "lot_trace_toggle", "type": "toggle"},
            {"key": "agent_mutation_preview", "type": "approval_gate"},
        ),
        "workflow_lanes": (
            "master_data",
            "receiving",
            "availability",
            "allocation",
            "quality",
            "replenishment",
            "reconciliation",
            "governance",
            "assistant",
        ),
        "agent_surfaces": {
            "panels": ("availability_explainer", "allocation_preview", "adjustment_draft", "document_intake"),
            "requires_human_confirmation_for_mutation": True,
        },
        "action_permissions": permissions["action_permissions"],
        "configuration_editor": {
            "required_fields": ("database_backend", "event_topic", "retry_limit", "default_uom", "precision", "allowed_statuses", "workbench_limit"),
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
            "rule_types": (
                "allocation_priority",
                "safety_stock",
                "quality_release",
                "substitution",
                "replenishment",
                "reconciliation",
                "channel_protection",
                "negative_inventory_prevention",
            ),
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


def inventory_positioning_render_workbench(state: dict, *, tenant: str, principal_permissions: tuple[str, ...]) -> dict:
    contract = inventory_positioning_ui_contract()
    runtime_view = inventory_positioning_build_workbench_view(state, tenant=tenant)
    permissions = set(principal_permissions)
    visible_actions = tuple(action for action, required in contract["action_permissions"].items() if required in permissions)
    return {
        "format": "appgen.inventory-positioning-workbench-render.v1",
        "ok": runtime_view["ok"],
        "tenant": tenant,
        "route": "/workbench/pbcs/inventory_positioning",
        "fragments": contract["fragments"],
        "cards": (
            {"key": "items", "value": runtime_view["item_count"], "fragment": "ItemMasterConsole"},
            {"key": "nodes", "value": runtime_view["node_count"], "fragment": "InventoryNodeConsole"},
            {"key": "positions", "value": runtime_view["position_count"], "fragment": "AvailabilityWorkbench"},
            {"key": "allocations", "value": runtime_view["allocation_count"], "fragment": "AllocationConsole"},
            {"key": "on_hand", "value": runtime_view["on_hand"], "fragment": "AvailabilityWorkbench"},
            {"key": "reserved", "value": runtime_view["reserved"], "fragment": "AllocationConsole"},
            {"key": "quarantine", "value": runtime_view["quarantine"], "fragment": "QualityHoldPanel"},
        ),
        "visible_actions": visible_actions,
        "locked_actions": tuple(action for action in contract["action_permissions"] if action not in visible_actions),
        "forms": contract["forms"],
        "wizards": contract["wizards"],
        "controls": contract["controls"],
        "workflow_lanes": contract["workflow_lanes"],
        "configuration_bound": runtime_view["configuration_bound"],
        "binding_evidence": {
            "owned_tables": INVENTORY_POSITIONING_OWNED_TABLES,
            "outbox_table": "inventory_positioning_appgen_outbox_event",
            "inbox_table": "inventory_positioning_appgen_inbox_event",
            "dead_letter_table": "inventory_positioning_dead_letter_event",
        },
        "runtime_view": runtime_view,
    }


def smoke_test() -> dict:
    state = inventory_positioning_empty_state()
    configured = inventory_positioning_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": INVENTORY_POSITIONING_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "default_uom": "EA",
            "precision": 2,
            "allowed_statuses": ("available", "reserved", "quarantine", "damaged", "in_transit"),
            "workbench_limit": 100,
        },
    )["state"]
    permissions = tuple(dict.fromkeys(permission_manifest()["action_permissions"].values()))
    rendered = inventory_positioning_render_workbench(configured, tenant="tenant_alpha", principal_permissions=permissions)
    contract = inventory_positioning_ui_contract()
    return {
        "format": "appgen.pbc-ui-smoke-test.v1",
        "ok": contract["ok"]
        and rendered["ok"]
        and bool(contract["fragments"])
        and bool(contract["forms"])
        and bool(contract["wizards"])
        and bool(contract["controls"])
        and contract["configuration_editor"]["stream_engine_picker_visible"] is False,
        "manifest": {"fragments": contract["fragments"], "routes": contract["routes"]},
        "contract": contract,
        "rendered": rendered,
        "side_effects": (),
    }
