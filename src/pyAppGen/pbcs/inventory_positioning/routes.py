"""API route contracts for the inventory_positioning PBC."""

from __future__ import annotations

import re

from .services import InventoryPositioningService
from .services import operation_plan
from .services import service_operation_contracts


PBC_KEY = "inventory_positioning"
ROUTES = (
    {"method": "POST", "path": "/inventory/items", "handler": "register_item", "permission": "inventory_positioning.master"},
    {"method": "POST", "path": "/inventory/nodes", "handler": "register_node", "permission": "inventory_positioning.master"},
    {"method": "POST", "path": "/inventory/receipts", "handler": "post_goods_receipt", "permission": "inventory_positioning.receive"},
    {"method": "POST", "path": "/inventory/adjustments", "handler": "post_adjustment", "permission": "inventory_positioning.adjust"},
    {"method": "GET", "path": "/inventory/availability", "handler": "calculate_availability", "permission": "inventory_positioning.read"},
    {"method": "POST", "path": "/inventory/allocations", "handler": "allocate_inventory", "permission": "inventory_positioning.allocate"},
    {"method": "POST", "path": "/inventory/allocations/{id}/release", "handler": "release_allocation", "permission": "inventory_positioning.release"},
    {"method": "POST", "path": "/inventory/quality-holds", "handler": "apply_quality_hold", "permission": "inventory_positioning.quality"},
    {"method": "POST", "path": "/inventory/events/inbox", "handler": "receive_event", "permission": "inventory_positioning.event"},
    {"method": "GET", "path": "/inventory/workbench", "handler": "build_workbench_view", "permission": "inventory_positioning.audit"},
)


def _contract_for_route(route: dict) -> dict:
    operation = operation_plan(route["handler"])
    return {
        "method": route["method"],
        "path": route["path"],
        "handler": route["handler"],
        "permission": route["permission"],
        "operation": route["handler"],
        "operation_kind": operation.get("operation_kind"),
        "owned_tables": operation.get("owned_tables", ()),
        "read_tables": operation.get("read_tables", ()),
        "emitted_event": operation.get("emitted_event"),
        "event_contract": "AppGen-X",
        "transaction_boundary": operation.get("transaction_boundary"),
        "idempotency_required": route["method"] == "POST",
        "idempotency_key": f"{PBC_KEY}:{route['handler']}:idempotency_key" if route["method"] == "POST" else None,
        "shared_table_access": False,
        "stream_engine_picker_visible": False,
    }


API_ROUTE_CONTRACTS = tuple(_contract_for_route(route) for route in ROUTES)


def register_routes(app=None):
    return ROUTES


def api_route_contracts() -> dict:
    indexed = {item["operation"]: item for item in service_operation_contracts()["contracts"]}
    contracts = tuple({**contract, "service_operation": indexed.get(contract["operation"]), "route_id": f"{contract['method']} {contract['path']}"} for contract in API_ROUTE_CONTRACTS)
    return {
        "ok": bool(contracts)
        and all(item["event_contract"] == "AppGen-X" for item in contracts)
        and all(item["stream_engine_picker_visible"] is False for item in contracts)
        and all(item["shared_table_access"] is False for item in contracts),
        "pbc": PBC_KEY,
        "contracts": contracts,
        "routes": tuple(item["route_id"] for item in contracts),
        "side_effects": (),
    }


def validate_api_route_contracts() -> dict:
    manifest = api_route_contracts()
    contracts = manifest["contracts"]
    service_mismatches = tuple(
        item["route_id"]
        for item in contracts
        if not item["service_operation"]
        or item["service_operation"]["method"] != item["method"]
        or item["service_operation"]["path"] != item["path"]
        or item["service_operation"]["permission"] != item["permission"]
    )
    missing_idempotency = tuple(item["route_id"] for item in contracts if item["idempotency_required"] and not item["idempotency_key"])
    invalid_table_scope = tuple(
        item["route_id"]
        for item in contracts
        for table in item["owned_tables"] + item["read_tables"]
        if not table.startswith(PBC_KEY + "_")
    )
    return {
        "ok": manifest["ok"] and not service_mismatches and not missing_idempotency and not invalid_table_scope,
        "pbc": PBC_KEY,
        "contracts": contracts,
        "service_mismatches": service_mismatches,
        "missing_idempotency": missing_idempotency,
        "invalid_table_scope": invalid_table_scope,
        "side_effects": (),
    }


def _match_route(method: str, path: str) -> tuple[dict | None, dict]:
    for route in ROUTES:
        pattern = "^" + re.escape(route["path"]).replace(re.escape("{id}"), r"(?P<id>[^/]+)") + "$"
        match = re.match(pattern, path)
        if route["method"] == method and match:
            return route, match.groupdict()
    return None, {}


def dispatch_route(method: str, path: str, payload: dict | None = None, *, service: InventoryPositioningService | None = None) -> dict:
    route, extracted = _match_route(method, path)
    if route is None:
        return {"ok": False, "handled": False, "reason": "route_not_found", "side_effects": ()}
    service = service or InventoryPositioningService()
    merged_payload = {**extracted, **dict(payload or {})}
    if route["handler"] == "release_allocation" and "allocation_id" not in merged_payload and "id" in merged_payload:
        merged_payload["allocation_id"] = merged_payload["id"]
    handler = getattr(service, route["handler"])
    result = handler(merged_payload)
    return {
        "ok": result.get("ok") is True,
        "handled": True,
        "route": route,
        "result": result,
        "service_state": service.state,
        "side_effects": (),
    }


def smoke_test() -> dict:
    service = InventoryPositioningService()
    service.configure_runtime(
        {
            "database_backend": "postgresql",
            "event_topic": "appgen.inventory.events",
            "retry_limit": 3,
            "default_uom": "EA",
            "precision": 2,
            "allowed_statuses": ("available", "reserved", "quarantine", "damaged", "in_transit"),
            "workbench_limit": 100,
        }
    )
    service.register_item({"tenant": "tenant_alpha", "item_id": "sku_100", "sku": "SKU-100", "uom": "EA", "lot_tracked": True, "serial_tracked": False, "substitution_group": "sku_100_core"})
    service.register_node({"tenant": "tenant_alpha", "node_id": "node_east", "node_type": "warehouse", "country": "US", "region": "east", "calendar": "weekday", "identity": {"did": "did:example:node-east", "issuer": "trusted_registry", "status": "active"}})
    service.post_goods_receipt({"tenant": "tenant_alpha", "receipt_id": "rcpt_route_001", "node_id": "node_east", "item_id": "sku_100", "quantity": 25.0, "lot_id": "lot_route_001", "expires": "2030-12-31"})
    validation = validate_api_route_contracts()
    dispatched = dispatch_route("GET", "/inventory/workbench", {"tenant": "tenant_alpha"}, service=service)
    return {
        "ok": validation["ok"] and dispatched["ok"],
        "validation": validation,
        "dispatch": dispatched,
        "side_effects": (),
    }
