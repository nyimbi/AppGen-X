"""API route contracts for the checkout_processing PBC."""

from __future__ import annotations

from .services import CheckoutProcessingService
from .services import service_operation_contracts


ROUTES = (
    {"method": "POST", "path": "/api/pbc/checkout_processing/carts", "handler": "command_carts", "permission": "checkout_processing.cart"},
    {"method": "POST", "path": "/api/pbc/checkout_processing/checkout", "handler": "command_checkout", "permission": "checkout_processing.checkout"},
    {"method": "POST", "path": "/api/pbc/checkout_processing/inventory-confirmations", "handler": "command_inventory_confirmations", "permission": "checkout_processing.inventory"},
    {"method": "POST", "path": "/api/pbc/checkout_processing/payment-authorizations", "handler": "command_payment_authorizations", "permission": "checkout_processing.payment"},
    {"method": "POST", "path": "/api/pbc/checkout_processing/payment-captures", "handler": "command_payment_captures", "permission": "checkout_processing.payment"},
    {"method": "POST", "path": "/api/pbc/checkout_processing/coupons", "handler": "command_coupons", "permission": "checkout_processing.promotion"},
    {"method": "GET", "path": "/api/pbc/checkout_processing/checkout-processing-workbench", "handler": "query_checkout_processing_workbench", "permission": "checkout_processing.audit"},
    {"method": "GET", "path": "/api/pbc/checkout_processing/controls", "handler": "query_checkout_processing_controls", "permission": "checkout_processing.audit"},
    {"method": "POST", "path": "/api/pbc/checkout_processing/assistant/document-preview", "handler": "query_checkout_processing_assistant_preview", "permission": "checkout_processing.audit"},
)


def _build_route_contracts() -> tuple[dict, ...]:
    service_contracts = service_operation_contracts()["contracts"]
    indexed = {item["operation"]: item for item in service_contracts}
    contracts = []
    for route in ROUTES:
        operation = route["handler"]
        service_operation = indexed.get(operation)
        contracts.append(
            {
                **route,
                "operation": operation,
                "operation_kind": service_operation["operation_kind"],
                "owned_tables": service_operation["owned_tables"],
                "read_tables": service_operation["read_tables"],
                "emitted_event": service_operation["emitted_event"],
                "event_contract": "AppGen-X",
                "transaction_boundary": "owned_datastore_plus_outbox",
                "idempotency_required": service_operation["operation_kind"] == "command",
                "idempotency_key": f"checkout_processing:{operation}:idempotency_key" if service_operation["operation_kind"] == "command" else None,
                "shared_table_access": False,
                "stream_engine_picker_visible": False,
                "service_operation": service_operation,
                "route_id": f"{route['method']} {route['path']}",
            }
        )
    return tuple(contracts)


API_ROUTE_CONTRACTS = _build_route_contracts()


def register_routes(app=None):
    """Return route metadata without mutating an application object."""
    return ROUTES


def api_route_contracts() -> dict:
    """Return executable API route contracts with policy and boundary evidence."""
    contracts = tuple(API_ROUTE_CONTRACTS)
    return {
        "ok": bool(contracts)
        and all(item["event_contract"] == "AppGen-X" for item in contracts)
        and all(item["transaction_boundary"] == "owned_datastore_plus_outbox" for item in contracts)
        and all(item["stream_engine_picker_visible"] is False for item in contracts)
        and all(item["shared_table_access"] is False for item in contracts),
        "pbc": "checkout_processing",
        "contracts": contracts,
        "routes": tuple(item["route_id"] for item in contracts),
        "side_effects": (),
    }


def validate_api_route_contracts() -> dict:
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
        if not table.startswith("checkout_processing_")
    )
    return {
        "ok": manifest["ok"]
        and not service_mismatches
        and not missing_idempotency
        and not invalid_table_scope,
        "pbc": "checkout_processing",
        "contracts": contracts,
        "service_mismatches": service_mismatches,
        "missing_idempotency": missing_idempotency,
        "invalid_table_scope": invalid_table_scope,
        "side_effects": (),
    }


def dispatch_route(method: str, path: str, payload: dict | None = None) -> dict:
    """Dispatch a route contract to its service operation without side effects."""
    route = next(
        (item for item in ROUTES if item["method"] == method and item["path"] == path),
        None,
    )
    if route is None:
        return {"ok": False, "handled": False, "reason": "route_not_found"}
    service = CheckoutProcessingService()
    handler = getattr(service, route["handler"])
    result = handler(payload or {})
    return {
        "ok": result.get("ok") is True,
        "handled": True,
        "route": route,
        "result": result,
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Execute the first route and validate the API contract surface."""
    validation = validate_api_route_contracts()
    first = ROUTES[0] if ROUTES else None
    dispatched = dispatch_route(first["method"], first["path"], {"smoke": True}) if first else {"ok": False}
    return {
        "ok": validation["ok"] and dispatched["ok"],
        "validation": validation,
        "dispatch": dispatched,
        "side_effects": (),
    }



STANDALONE_ROUTES = (
    {"method": "POST", "path": "/app/checkout-processing/demo-workspace", "handler": "seed_demo_workspace", "permission": "checkout_processing.configure"},
    {"method": "GET", "path": "/app/checkout-processing/workbench", "handler": "build_workbench", "permission": "checkout_processing.audit"},
    {"method": "POST", "path": "/app/checkout-processing/carts", "handler": "create_cart", "permission": "checkout_processing.cart"},
    {"method": "POST", "path": "/app/checkout-processing/sessions", "handler": "open_checkout_session", "permission": "checkout_processing.checkout"},
    {"method": "POST", "path": "/app/checkout-processing/checkouts/complete", "handler": "complete_checkout", "permission": "checkout_processing.checkout"},
    {"method": "POST", "path": "/app/checkout-processing/proofs", "handler": "generate_checkout_proof", "permission": "checkout_processing.audit"},
    {"method": "POST", "path": "/app/checkout-processing/assistant/sessions", "handler": "run_agent_skill", "permission": "checkout_processing.audit"},
)


def standalone_route_contracts() -> dict:
    from .services import standalone_service_operation_contracts

    service_contracts = {item["operation"]: item for item in standalone_service_operation_contracts()["contracts"]}
    contracts = tuple(
        {
            **route,
            "operation": route["handler"],
            "service_operation": service_contracts[route["handler"]],
            "owned_tables": service_contracts[route["handler"]]["owned_tables"],
            "read_tables": service_contracts[route["handler"]]["read_tables"],
            "emitted_event": service_contracts[route["handler"]]["emitted_event"],
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
            "shared_table_access": False,
            "route_id": f"{route['method']} {route['path']}",
        }
        for route in STANDALONE_ROUTES
    )
    return {
        "format": "appgen.checkout-processing-standalone-routes.v1",
        "ok": bool(contracts)
        and all(item["event_contract"] == "AppGen-X" for item in contracts)
        and all(item["shared_table_access"] is False for item in contracts)
        and all(item["stream_engine_picker_visible"] is False for item in contracts),
        "pbc": "checkout_processing",
        "routes": tuple(item["route_id"] for item in contracts),
        "contracts": contracts,
        "side_effects": (),
    }


def dispatch_standalone_route(method: str, path: str, payload: dict | None = None, *, service=None) -> dict:
    from .services import CheckoutProcessingStandaloneService

    route = next((item for item in STANDALONE_ROUTES if item["method"] == method and item["path"] == path), None)
    if route is None:
        return {"ok": False, "handled": False, "reason": "route_not_found", "side_effects": ()}
    owned_service = service is None
    if service is None:
        service = CheckoutProcessingStandaloneService()
    supplied = dict(payload or {})
    try:
        if route["handler"] == "seed_demo_workspace":
            result = service.seed_demo_workspace(tenant=supplied.get("tenant", "tenant_demo"))
        elif route["handler"] == "build_workbench":
            result = service.build_workbench(tenant=supplied.get("tenant", "tenant_demo"))
        elif route["handler"] == "create_cart":
            result = service.create_cart(supplied, tenant=supplied.get("tenant", "tenant_demo"))
        elif route["handler"] == "open_checkout_session":
            result = service.open_checkout_session(supplied, tenant=supplied.get("tenant", "tenant_demo"))
        elif route["handler"] == "complete_checkout":
            result = service.complete_checkout(supplied["session_id"], tenant=supplied.get("tenant", "tenant_demo"))
        elif route["handler"] == "generate_checkout_proof":
            result = service.generate_checkout_proof(
                supplied["session_id"],
                supplied.get("disclosure", ("session_id", "order_id", "status")),
                tenant=supplied.get("tenant", "tenant_demo"),
            )
        else:
            result = service.run_agent_skill(supplied, tenant=supplied.get("tenant", "tenant_demo"))
        return {"ok": result.get("ok") is True, "handled": True, "route": route, "result": result, "side_effects": ()}
    finally:
        if owned_service:
            service.close()
