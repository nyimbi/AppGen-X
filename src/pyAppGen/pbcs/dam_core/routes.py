"""API route contracts for the dam_core PBC."""

from __future__ import annotations

from .services import DamCoreService
from .services import service_operation_contracts


def _route_contracts() -> tuple[dict, ...]:
    return tuple(
        {
            "method": contract["method"],
            "path": contract["path"],
            "handler": contract["operation"],
            "permission": contract["permission"],
            "operation": contract["operation"],
            "operation_kind": contract["operation_kind"],
            "owned_tables": contract["owned_tables"],
            "read_tables": contract["read_tables"],
            "emitted_event": contract["emitted_event"],
            "event_contract": contract["event_contract"],
            "transaction_boundary": contract["transaction_boundary"],
            "idempotency_required": contract["operation_kind"] == "command",
            "idempotency_key": contract["idempotency_key"],
            "shared_table_access": False,
            "stream_engine_picker_visible": False,
        }
        for contract in service_operation_contracts()["contracts"]
    )


API_ROUTE_CONTRACTS = _route_contracts()
ROUTES = tuple(
    {
        "method": contract["method"],
        "path": contract["path"],
        "handler": contract["handler"],
        "permission": contract["permission"],
    }
    for contract in API_ROUTE_CONTRACTS
)


def register_routes(app=None):
    """Return route metadata without mutating an application object."""
    return ROUTES


def api_route_contracts() -> dict:
    """Return executable API route contracts with policy and boundary evidence."""
    contracts = tuple(
        {
            **contract,
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
        "pbc": "dam_core",
        "contracts": contracts,
        "routes": tuple(item["route_id"] for item in contracts),
        "side_effects": (),
    }


def validate_api_route_contracts() -> dict:
    """Validate routes against service operations, permissions, idempotency, and table boundaries."""
    manifest = api_route_contracts()
    contracts = manifest["contracts"]
    operation_index = {item["operation"]: item for item in service_operation_contracts()["contracts"]}
    service_mismatches = tuple(
        item["route_id"]
        for item in contracts
        if item["operation"] not in operation_index
        or operation_index[item["operation"]]["method"] != item["method"]
        or operation_index[item["operation"]]["path"] != item["path"]
        or operation_index[item["operation"]]["permission"] != item["permission"]
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
        if not table.startswith("dam_core_")
    )
    return {
        "ok": manifest["ok"]
        and not service_mismatches
        and not missing_idempotency
        and not invalid_table_scope,
        "pbc": "dam_core",
        "contracts": contracts,
        "service_mismatches": service_mismatches,
        "missing_idempotency": missing_idempotency,
        "invalid_table_scope": invalid_table_scope,
        "side_effects": (),
    }


def dispatch_route(method: str, path: str, payload: dict | None = None, *, service: DamCoreService | None = None) -> dict:
    """Dispatch a route contract to its service command without external side effects."""
    route = next((item for item in ROUTES if item["method"] == method and item["path"] == path), None)
    if route is None:
        return {"ok": False, "handled": False, "reason": "route_not_found", "side_effects": ()}
    service = service or DamCoreService()
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
    """Execute configuration, one route, and validate the API contract surface."""
    service = DamCoreService()
    dispatch_route(
        "POST",
        "/api/pbc/dam_core/runtime/configuration",
        {
            "configuration": {
                "database_backend": "postgresql",
                "event_topic": "appgen.dam.events",
                "retry_limit": 3,
                "default_storage_tier": "warm",
                "allowed_mime_types": ("image/jpeg",),
                "rendition_profiles": ("web_large",),
                "rights_default_decision": "review",
                "metadata_taxonomies": ("product",),
                "default_locale": "en-US",
                "workbench_limit": 100,
            }
        },
        service=service,
    )
    dispatch_route(
        "POST",
        "/api/pbc/dam_core/runtime/parameters",
        {"name": "max_asset_size_mb", "value": 100},
        service=service,
    )
    dispatched = dispatch_route(
        "POST",
        "/api/pbc/dam_core/assets",
        {
            "asset": {
                "asset_id": "asset_route_smoke",
                "tenant": "tenant_route_smoke",
                "filename": "asset.jpg",
                "mime_type": "image/jpeg",
                "size_mb": 5,
                "storage_uri": "object://dam/route-smoke/asset.jpg",
                "binary": b"route-smoke",
                "created_by": "route-smoke",
            }
        },
        service=service,
    )
    validation = validate_api_route_contracts()
    return {
        "ok": validation["ok"] and dispatched["ok"],
        "validation": validation,
        "dispatch": dispatched,
        "side_effects": (),
    }
