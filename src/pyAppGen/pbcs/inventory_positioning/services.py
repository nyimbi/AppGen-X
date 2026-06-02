"""Stateful standalone service layer for the inventory_positioning PBC."""

from __future__ import annotations

from dataclasses import dataclass

from .permissions import ACTION_PERMISSIONS
from .runtime import INVENTORY_POSITIONING_OWNED_TABLES
from . import runtime


PBC_KEY = "inventory_positioning"
_TRANSACTION_BOUNDARY = "owned_datastore_plus_outbox"
_OPERATION_SPECS = (
    {"operation": "configure_runtime", "operation_kind": "command", "method": "POST", "path": "/inventory/configuration", "permission": ACTION_PERMISSIONS["configure_runtime"], "owned_tables": ("inventory_positioning_configuration",), "read_tables": (), "emitted_event": None},
    {"operation": "set_parameter", "operation_kind": "command", "method": "POST", "path": "/inventory/parameters", "permission": ACTION_PERMISSIONS["set_parameter"], "owned_tables": ("inventory_positioning_parameter",), "read_tables": (), "emitted_event": None},
    {"operation": "register_rule", "operation_kind": "command", "method": "POST", "path": "/inventory/rules", "permission": ACTION_PERMISSIONS["register_rule"], "owned_tables": ("inventory_positioning_rule",), "read_tables": (), "emitted_event": None},
    {"operation": "register_schema_extension", "operation_kind": "command", "method": "POST", "path": "/inventory/schema-extensions", "permission": ACTION_PERMISSIONS["register_schema_extension"], "owned_tables": ("inventory_positioning_schema_extension",), "read_tables": (), "emitted_event": None},
    {"operation": "register_item", "operation_kind": "command", "method": "POST", "path": "/inventory/items", "permission": ACTION_PERMISSIONS["register_item"], "owned_tables": ("inventory_positioning_item", "inventory_positioning_item_attribute", "inventory_positioning_item_substitution"), "read_tables": (), "emitted_event": "ItemRegistered"},
    {"operation": "register_node", "operation_kind": "command", "method": "POST", "path": "/inventory/nodes", "permission": ACTION_PERMISSIONS["register_node"], "owned_tables": ("inventory_positioning_node", "inventory_positioning_node_calendar", "inventory_positioning_node_capacity", "inventory_positioning_node_identity"), "read_tables": (), "emitted_event": "InventoryNodeRegistered"},
    {"operation": "post_goods_receipt", "operation_kind": "command", "method": "POST", "path": "/inventory/receipts", "permission": ACTION_PERMISSIONS["post_goods_receipt"], "owned_tables": ("inventory_positioning_receipt", "inventory_positioning_receipt_line", "inventory_positioning_inventory_position"), "read_tables": (), "emitted_event": "GoodsReceiptPosted"},
    {"operation": "post_adjustment", "operation_kind": "command", "method": "POST", "path": "/inventory/adjustments", "permission": ACTION_PERMISSIONS["post_adjustment"], "owned_tables": ("inventory_positioning_adjustment", "inventory_positioning_inventory_position"), "read_tables": (), "emitted_event": "InventoryAdjusted"},
    {"operation": "calculate_availability", "operation_kind": "query", "method": "GET", "path": "/inventory/availability", "permission": ACTION_PERMISSIONS["calculate_availability"], "owned_tables": (), "read_tables": ("inventory_positioning_inventory_position", "inventory_positioning_reservation", "inventory_positioning_quality_hold"), "emitted_event": None},
    {"operation": "allocate_inventory", "operation_kind": "command", "method": "POST", "path": "/inventory/allocations", "permission": ACTION_PERMISSIONS["allocate_inventory"], "owned_tables": ("inventory_positioning_allocation", "inventory_positioning_allocation_line", "inventory_positioning_inventory_position"), "read_tables": (), "emitted_event": "InventoryAllocated"},
    {"operation": "release_allocation", "operation_kind": "command", "method": "POST", "path": "/inventory/allocations/{id}/release", "permission": ACTION_PERMISSIONS["release_allocation"], "owned_tables": ("inventory_positioning_allocation", "inventory_positioning_allocation_expiry", "inventory_positioning_inventory_position"), "read_tables": (), "emitted_event": "InventoryReleased"},
    {"operation": "apply_quality_hold", "operation_kind": "command", "method": "POST", "path": "/inventory/quality-holds", "permission": ACTION_PERMISSIONS["apply_quality_hold"], "owned_tables": ("inventory_positioning_quality_hold", "inventory_positioning_inventory_position"), "read_tables": (), "emitted_event": "QualityHoldApplied"},
    {"operation": "receive_event", "operation_kind": "command", "method": "POST", "path": "/inventory/events/inbox", "permission": ACTION_PERMISSIONS["receive_event"], "owned_tables": ("inventory_positioning_appgen_inbox_event", "inventory_positioning_dead_letter_event"), "read_tables": (), "emitted_event": None},
    {"operation": "build_workbench_view", "operation_kind": "query", "method": "GET", "path": "/inventory/workbench", "permission": ACTION_PERMISSIONS["build_workbench_view"], "owned_tables": (), "read_tables": INVENTORY_POSITIONING_OWNED_TABLES, "emitted_event": None},
    {"operation": "generate_replenishment_signal", "operation_kind": "command", "method": "POST", "path": "/inventory/replenishment-signals", "permission": ACTION_PERMISSIONS["generate_replenishment_signal"], "owned_tables": ("inventory_positioning_replenishment_signal",), "read_tables": (), "emitted_event": None},
    {"operation": "reconcile_inventory", "operation_kind": "command", "method": "POST", "path": "/inventory/reconciliations", "permission": ACTION_PERMISSIONS["reconcile_inventory"], "owned_tables": ("inventory_positioning_reconciliation",), "read_tables": (), "emitted_event": None},
    {"operation": "generate_stock_proof", "operation_kind": "query", "method": "GET", "path": "/inventory/stock-proof", "permission": ACTION_PERMISSIONS["generate_stock_proof"], "owned_tables": (), "read_tables": ("inventory_positioning_stock_proof", "inventory_positioning_inventory_position"), "emitted_event": None},
)
_OPERATION_INDEX = {item["operation"]: item for item in _OPERATION_SPECS}


@dataclass
class InventoryPositioningService:
    """In-memory standalone service for one-PBC execution."""

    state: dict | None = None

    def __post_init__(self) -> None:
        if self.state is None:
            self.state = runtime.inventory_positioning_empty_state()

    def _finalize(self, operation_name: str, result: dict, payload: dict | None = None) -> dict:
        contract = operation_plan(operation_name, payload)
        if "state" in result:
            self.state = result["state"]
        return {
            **result,
            "operation": operation_name,
            "operation_kind": contract["operation_kind"],
            "operation_contract": contract,
            "transaction_boundary": contract["transaction_boundary"],
            "side_effects": (),
        }

    def configure_runtime(self, payload: dict | None = None) -> dict:
        return self._finalize("configure_runtime", runtime.inventory_positioning_configure_runtime(self.state, payload or {}), payload)

    def set_parameter(self, payload: dict | None = None) -> dict:
        payload = dict(payload or {})
        result = runtime.inventory_positioning_set_parameter(self.state, payload["name"], payload["value"])
        return self._finalize("set_parameter", result, payload)

    def register_rule(self, payload: dict | None = None) -> dict:
        return self._finalize("register_rule", runtime.inventory_positioning_register_rule(self.state, payload or {}), payload)

    def register_schema_extension(self, payload: dict | None = None) -> dict:
        payload = dict(payload or {})
        result = runtime.inventory_positioning_register_schema_extension(self.state, payload["table"], payload["fields"])
        return self._finalize("register_schema_extension", result, payload)

    def register_item(self, payload: dict | None = None) -> dict:
        return self._finalize("register_item", runtime.inventory_positioning_register_item(self.state, payload or {}), payload)

    def register_node(self, payload: dict | None = None) -> dict:
        return self._finalize("register_node", runtime.inventory_positioning_register_node(self.state, payload or {}), payload)

    def post_goods_receipt(self, payload: dict | None = None) -> dict:
        return self._finalize("post_goods_receipt", runtime.inventory_positioning_post_goods_receipt(self.state, payload or {}), payload)

    def post_adjustment(self, payload: dict | None = None) -> dict:
        payload = dict(payload or {})
        result = runtime.inventory_positioning_post_adjustment(
            self.state,
            payload["adjustment_id"],
            node_id=payload["node_id"],
            item_id=payload["item_id"],
            quantity=payload["quantity"],
            reason=payload["reason"],
        )
        return self._finalize("post_adjustment", result, payload)

    def calculate_availability(self, payload: dict | None = None) -> dict:
        payload = dict(payload or {})
        result = runtime.inventory_positioning_calculate_availability(
            self.state,
            item_id=payload["item_id"],
            tenant=payload["tenant"],
            demand_class=payload.get("demand_class", "standard"),
        )
        return self._finalize("calculate_availability", result, payload)

    def allocate_inventory(self, payload: dict | None = None) -> dict:
        return self._finalize("allocate_inventory", runtime.inventory_positioning_allocate_inventory(self.state, payload or {}), payload)

    def release_allocation(self, payload: dict | None = None) -> dict:
        payload = dict(payload or {})
        result = runtime.inventory_positioning_release_allocation(self.state, payload["allocation_id"], reason=payload["reason"])
        return self._finalize("release_allocation", result, payload)

    def apply_quality_hold(self, payload: dict | None = None) -> dict:
        payload = dict(payload or {})
        result = runtime.inventory_positioning_apply_quality_hold(
            self.state,
            payload["hold_id"],
            node_id=payload["node_id"],
            item_id=payload["item_id"],
            quantity=payload["quantity"],
            reason=payload["reason"],
        )
        return self._finalize("apply_quality_hold", result, payload)

    def receive_event(self, payload: dict | None = None) -> dict:
        return self._finalize("receive_event", runtime.inventory_positioning_receive_event(self.state, payload or {}), payload)

    def build_workbench_view(self, payload: dict | None = None) -> dict:
        payload = dict(payload or {})
        result = runtime.inventory_positioning_build_workbench_view(self.state, tenant=payload["tenant"])
        return self._finalize("build_workbench_view", result, payload)

    def generate_replenishment_signal(self, payload: dict | None = None) -> dict:
        payload = dict(payload or {})
        result = runtime.inventory_positioning_generate_replenishment_signal(
            self.state,
            item_id=payload["item_id"],
            reorder_point=payload["reorder_point"],
            forecast_demand=payload["forecast_demand"],
        )
        return self._finalize("generate_replenishment_signal", result, payload)

    def reconcile_inventory(self, payload: dict | None = None) -> dict:
        payload = dict(payload or {})
        result = runtime.inventory_positioning_reconcile_inventory(self.state, item_id=payload["item_id"], physical_count=payload["physical_count"])
        return self._finalize("reconcile_inventory", result, payload)

    def generate_stock_proof(self, payload: dict | None = None) -> dict:
        payload = dict(payload or {})
        result = runtime.inventory_positioning_generate_stock_proof(
            self.state,
            item_id=payload["item_id"],
            disclosure=tuple(payload.get("disclosure", ("item_id", "available"))),
        )
        return self._finalize("generate_stock_proof", result, payload)


def operation_plan(operation_name: str, payload: dict | None = None) -> dict:
    contract = _OPERATION_INDEX.get(operation_name)
    if contract is None:
        return {"ok": False, "reason": "unknown_operation", "operation": operation_name, "side_effects": ()}
    supplied = dict(payload or {})
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "operation": operation_name,
        "operation_kind": contract["operation_kind"],
        "route": {"method": contract["method"], "path": contract["path"]},
        "permission": contract["permission"],
        "owned_tables": tuple(contract["owned_tables"]),
        "read_tables": tuple(contract["read_tables"]),
        "emitted_event": contract["emitted_event"],
        "payload_keys": tuple(sorted(supplied)),
        "transaction_boundary": _TRANSACTION_BOUNDARY,
        "event_contract": "AppGen-X",
        "side_effects": (),
    }


def service_operation_contracts() -> dict:
    contracts = tuple(
        {
            **spec,
            "transaction_boundary": _TRANSACTION_BOUNDARY,
            "event_contract": "AppGen-X",
        }
        for spec in _OPERATION_SPECS
    )
    command_contracts = tuple(item for item in contracts if item["operation_kind"] == "command")
    query_contracts = tuple(item for item in contracts if item["operation_kind"] == "query")
    return {
        "ok": bool(contracts)
        and all(item["event_contract"] == "AppGen-X" for item in contracts)
        and all(item["transaction_boundary"] == _TRANSACTION_BOUNDARY for item in contracts)
        and all(item["owned_tables"] and not item["read_tables"] for item in command_contracts)
        and all(item["read_tables"] and not item["owned_tables"] for item in query_contracts),
        "pbc": PBC_KEY,
        "operations": tuple(item["operation"] for item in contracts),
        "command_operations": tuple(item["operation"] for item in command_contracts),
        "query_operations": tuple(item["operation"] for item in query_contracts),
        "contracts": contracts,
        "side_effects": (),
    }


def service_operation_manifest() -> dict:
    contracts = service_operation_contracts()
    return {
        "ok": contracts["ok"],
        "pbc": PBC_KEY,
        "service_class": InventoryPositioningService.__name__,
        "operations": contracts["operations"],
        "command_operations": contracts["command_operations"],
        "query_operations": contracts["query_operations"],
        "operation_contracts": contracts["contracts"],
        "transaction_boundary": _TRANSACTION_BOUNDARY,
        "outbox_table": "inventory_positioning_appgen_outbox_event",
        "side_effects": (),
    }


def smoke_test() -> dict:
    service = InventoryPositioningService()
    service.configure_runtime(
        {
            "database_backend": "postgresql",
            "event_topic": runtime.INVENTORY_POSITIONING_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "default_uom": "EA",
            "precision": 2,
            "allowed_statuses": ("available", "reserved", "quarantine", "damaged", "in_transit"),
            "workbench_limit": 100,
        }
    )
    service.set_parameter({"name": "safety_stock_percent", "value": 0.1})
    service.register_rule({"rule_id": "service.smoke.rule", "tenant": "tenant_alpha", "scope": "allocation_priority", "status": "active"})
    service.register_item({"tenant": "tenant_alpha", "item_id": "sku_100", "sku": "SKU-100", "uom": "EA", "lot_tracked": True, "serial_tracked": False, "substitution_group": "sku_100_core"})
    service.register_node({"tenant": "tenant_alpha", "node_id": "node_east", "node_type": "warehouse", "country": "US", "region": "east", "calendar": "weekday", "identity": {"did": "did:example:node-east", "issuer": "trusted_registry", "status": "active"}})
    service.post_goods_receipt({"tenant": "tenant_alpha", "receipt_id": "rcpt_smoke_001", "node_id": "node_east", "item_id": "sku_100", "quantity": 100.0, "lot_id": "lot_smoke_001", "expires": "2030-12-31"})
    availability = service.calculate_availability({"tenant": "tenant_alpha", "item_id": "sku_100", "demand_class": "standard"})
    workbench = service.build_workbench_view({"tenant": "tenant_alpha"})
    return {
        "ok": availability["ok"] and workbench["ok"] and service_operation_manifest()["ok"],
        "availability": availability,
        "workbench": workbench,
        "manifest": service_operation_manifest(),
        "side_effects": (),
    }
