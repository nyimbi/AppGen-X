"""API route contracts for the dom PBC."""

from __future__ import annotations

from .services import DomService
from .services import DomStandaloneService
from .services import service_operation_contracts


ROUTES = tuple(
    {
        "method": item["method"],
        "path": item["path"],
        "handler": item["operation"],
        "permission": item["permission"],
    }
    for item in service_operation_contracts()["contracts"]
)

API_ROUTE_CONTRACTS = tuple(
    {
        "method": item["method"],
        "path": item["path"],
        "handler": item["operation"],
        "permission": item["permission"],
        "operation": item["operation"],
        "service_method": item["service_method"],
        "operation_kind": item["operation_kind"],
        "owned_tables": item["owned_tables"],
        "read_tables": item["read_tables"],
        "emitted_event": item["emitted_event"],
        "event_contract": item["event_contract"],
        "transaction_boundary": item["transaction_boundary"],
        "idempotency_required": item["operation_kind"] == "command",
        "idempotency_key": f"dom:{item['operation']}:idempotency_key" if item["operation_kind"] == "command" else None,
        "shared_table_access": False,
        "stream_engine_picker_visible": False,
    }
    for item in service_operation_contracts()["contracts"]
)


def register_routes(app=None):
    """Return route metadata without mutating an application object."""
    return ROUTES


def api_route_contracts():
    """Return executable API route contracts with policy and boundary evidence."""
    service_contracts = service_operation_contracts()["contracts"]
    operation_index = {item["operation"]: item for item in service_contracts}
    contracts = tuple(
        {
            **contract,
            "service_operation": operation_index.get(contract["operation"]),
            "route_id": f"{contract['method']} {contract['path']}",
        }
        for contract in API_ROUTE_CONTRACTS
    )
    return {
        "ok": bool(contracts)
        and all(item["event_contract"] == "AppGen-X" for item in contracts)
        and all(item["transaction_boundary"] == "owned_datastore_plus_outbox" for item in contracts)
        and all(item["stream_engine_picker_visible"] is False for item in contracts)
        and all(item["shared_table_access"] is False for item in contracts),
        "pbc": "dom",
        "contracts": contracts,
        "routes": tuple(item["route_id"] for item in contracts),
        "side_effects": (),
    }


def validate_api_route_contracts():
    """Validate routes against service operations, permissions, idempotency, and table boundaries."""
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
    missing_idempotency = tuple(
        item["route_id"]
        for item in contracts
        if item["idempotency_required"] and not item["idempotency_key"]
    )
    invalid_table_scope = tuple(
        item["route_id"]
        for item in contracts
        for table in item["owned_tables"] + item["read_tables"]
        if not table.startswith("dom_")
    )
    return {
        "ok": manifest["ok"]
        and not service_mismatches
        and not missing_idempotency
        and not invalid_table_scope,
        "pbc": "dom",
        "contracts": contracts,
        "service_mismatches": service_mismatches,
        "missing_idempotency": missing_idempotency,
        "invalid_table_scope": invalid_table_scope,
        "side_effects": (),
    }


def dispatch_route(method, path, payload=None):
    """Dispatch a route contract to its descriptor handler without side effects."""
    route = next((item for item in ROUTES if item["method"] == method and item["path"] == path), None)
    if route is None:
        return {"ok": False, "handled": False, "reason": "route_not_found"}
    service = DomService()
    handler = getattr(service, route["handler"])
    result = handler(payload or {})
    return {
        "ok": result.get("ok") is True,
        "handled": True,
        "route": route,
        "result": result,
        "side_effects": (),
    }


def dispatch_standalone_route(service: DomStandaloneService, method: str, path: str, payload=None):
    """Dispatch a route into the standalone service implementation."""
    route = next((item for item in API_ROUTE_CONTRACTS if item["method"] == method and item["path"] == path), None)
    if route is None:
        return {"ok": False, "handled": False, "reason": "route_not_found"}
    handler = getattr(service, route["service_method"])
    data = dict(payload or {})
    if route["service_method"] in {"capture_order"}:
        result = handler(data)
    elif route["service_method"] in {"apply_tax_projection"}:
        result = handler(data["order_id"], data)
    elif route["service_method"] in {"screen_fraud"}:
        result = handler(data["order_id"], signals=data.get("signals", {}))
    elif route["service_method"] in {"verify_order", "price_order", "create_fulfillment_plan"}:
        result = handler(data["order_id"])
    elif route["service_method"] in {"apply_inventory_allocation"}:
        result = handler(data["order_id"], data.get("allocations") or data.get("allocation"))
    elif route["service_method"] in {"release_hold"}:
        result = handler(order_id=data["order_id"], hold_id=data["hold_id"], released_by=data["released_by"], note=data.get("note", ""))
    elif route["service_method"] in {"request_cancellation"}:
        result = handler(order_id=data["order_id"], reason=data["reason"], actor=data.get("actor", "user"))
    elif route["service_method"] in {"apply_substitution"}:
        result = handler(order_id=data["order_id"], line_id=data["line_id"], substitute_item_id=data["substitute_item_id"], reason=data.get("reason", "equivalent_inventory"))
    elif route["service_method"] in {"confirm_order_shipped"}:
        result = handler(data["order_id"], shipment_id=data["shipment_id"])
    elif route["service_method"] in {"receive_event"}:
        result = handler(data)
    elif route["service_method"] in {"workbench"}:
        result = handler(tenant=data.get("tenant"))
    else:
        result = handler(**data)
    return {
        "ok": result.get("ok") is True,
        "handled": True,
        "route": route,
        "result": result,
        "side_effects": (),
    }


def smoke_test():
    """Execute the first descriptor route and validate the standalone route surface."""
    validation = validate_api_route_contracts()
    if not ROUTES:
        return {"ok": False, "reason": "no_routes"}
    first = ROUTES[0]
    dispatched = dispatch_route(first["method"], first["path"], {"smoke": True})
    standalone = DomStandaloneService(tenant="tenant_alpha")
    standalone.configure()
    standalone.register_defaults()
    standalone.upsert_customer_projection({"tenant": "tenant_alpha", "customer_id": "cust_100", "status": "active", "risk": 0.05})
    executed = dispatch_standalone_route(
        standalone,
        "POST",
        "/dom/orders",
        {
            "tenant": "tenant_alpha",
            "order_id": "order_100",
            "customer_id": "cust_100",
            "channel": "web",
            "destination": "BOS",
            "service_level": "standard",
            "lines": ({"line_id": "line_1", "item_id": "sku_100", "quantity": 1, "unit_price": 100},),
        },
    )
    return {
        "ok": validation["ok"] and dispatched["ok"] and executed["ok"],
        "validation": validation,
        "dispatch": dispatched,
        "standalone": executed,
        "side_effects": (),
    }
