"""API route contracts for the cdp_segmentation PBC."""

from __future__ import annotations

from .runtime import cdp_segmentation_build_api_contract
from .services import CdpSegmentationService
from .services import service_operation_contracts


def _method_path(route: str) -> tuple[str, str]:
    method, path = route.split(" ", 1)
    return method, path


def _route_rows() -> tuple[dict, ...]:
    rows = []
    for route in cdp_segmentation_build_api_contract()["routes"]:
        operation = route.get("command") or route.get("query")
        if not operation:
            continue
        method, path = _method_path(route["route"])
        rows.append(
            {
                "method": method,
                "path": path,
                "handler": operation,
                "permission": route["requires_permission"],
            }
        )
    return tuple(rows)


ROUTES = _route_rows()


def _route_contracts() -> tuple[dict, ...]:
    operation_index = {item["operation"]: item for item in service_operation_contracts()["contracts"]}
    contracts = []
    for route in ROUTES:
        service_operation = operation_index[route["handler"]]
        idempotency_required = service_operation["operation_kind"] == "command"
        contracts.append(
            {
                **route,
                "operation": route["handler"],
                "operation_kind": service_operation["operation_kind"],
                "owned_tables": service_operation["owned_tables"],
                "read_tables": service_operation["read_tables"],
                "emitted_event": service_operation["emitted_event"],
                "consumed_event": service_operation["consumed_event"],
                "event_contract": "AppGen-X",
                "transaction_boundary": "owned_datastore_plus_outbox",
                "idempotency_required": idempotency_required,
                "idempotency_key": f"cdp_segmentation:{route['handler']}:request" if idempotency_required else None,
                "shared_table_access": False,
                "stream_engine_picker_visible": False,
            }
        )
    return tuple(contracts)


API_ROUTE_CONTRACTS = _route_contracts()


def register_routes(app=None):
    """Return route metadata without mutating an application object."""
    return ROUTES


def api_route_contracts() -> dict:
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
        "pbc": "cdp_segmentation",
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
        if not table.startswith("cdp_segmentation_")
    )
    return {
        "ok": manifest["ok"] and not service_mismatches and not missing_idempotency and not invalid_table_scope,
        "pbc": "cdp_segmentation",
        "contracts": contracts,
        "service_mismatches": service_mismatches,
        "missing_idempotency": missing_idempotency,
        "invalid_table_scope": invalid_table_scope,
        "side_effects": (),
    }


def dispatch_route(method: str, path: str, payload: dict | None = None) -> dict:
    """Dispatch a route contract to its service command."""
    route = next((item for item in ROUTES if item["method"] == method and item["path"] == path), None)
    if route is None:
        return {"ok": False, "handled": False, "reason": "route_not_found", "side_effects": ()}
    service = CdpSegmentationService()
    result = service.execute_operation(route["handler"], payload or {})
    return {
        "ok": result.get("ok") is True,
        "handled": True,
        "route": route,
        "result": result,
        "state": result.get("state"),
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Exercise route validation and one explicit-state dispatch."""
    from .runtime import CDP_SEGMENTATION_REQUIRED_EVENT_TOPIC
    from .runtime import cdp_segmentation_empty_state

    validation = validate_api_route_contracts()
    if not ROUTES:
        return {"ok": False, "reason": "no_routes", "side_effects": ()}
    dispatched = dispatch_route(
        "POST",
        "/events",
        {
            "state": {
                **cdp_segmentation_empty_state(),
                "configuration": {
                    "ok": True,
                    "database_backend": "postgresql",
                    "event_topic": CDP_SEGMENTATION_REQUIRED_EVENT_TOPIC,
                    "supported_regions": ("US",),
                    "supported_event_types": ("profile", "payment", "shipment", "engagement"),
                    "default_region": "US",
                    "retry_limit": 3,
                },
            },
            "event_id": "smoke_event",
            "tenant": "smoke",
            "customer_id": "cust_smoke",
            "event_type": "profile",
            "region": "US",
            "properties": {"customer_id": "cust_smoke", "email": "smoke@example.com", "opt_in": True},
        },
    )
    return {
        "ok": validation["ok"] and dispatched["ok"] and dispatched["state"]["customer_events"]["smoke_event"]["event_type"] == "profile",
        "validation": validation,
        "dispatch": dispatched,
        "side_effects": (),
    }
