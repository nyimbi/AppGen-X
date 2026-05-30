"""API route contracts for the federated_iam PBC."""

from __future__ import annotations

from . import permissions
from .services import FederatedIamService
from .services import create_seeded_service
from .services import service_operation_contracts


PBC_KEY = "federated_iam"


def _route_rows() -> tuple[dict, ...]:
    rows = []
    for contract in service_operation_contracts()["contracts"]:
        rows.append(
            {
                "method": contract["method"],
                "path": contract["path"],
                "handler": contract["operation"],
                "permission": contract["permission"],
                "idempotency_required": contract["idempotency_required"],
                "idempotency_key": contract["idempotency_key"],
                "shared_table_access": False,
                "stream_engine_picker_visible": False,
            }
        )
    return tuple(rows)


ROUTES = _route_rows()


def register_routes(app=None):
    """Return route metadata without mutating an application object."""
    return ROUTES


def api_route_contracts() -> dict:
    """Return executable API route contracts with policy and boundary evidence."""
    service_contracts = service_operation_contracts()["contracts"]
    operation_index = {item["operation"]: item for item in service_contracts}
    contracts = tuple(
        {
            **route,
            **(operation_index.get(route["handler"]) or {}),
            "service_operation": operation_index.get(route["handler"]),
            "route_id": f"{route['method']} {route['path']}",
        }
        for route in ROUTES
    )
    return {
        "ok": bool(contracts)
        and all(item["service_operation"] for item in contracts)
        and all(item["stream_engine_picker_visible"] is False for item in contracts)
        and all(item["shared_table_access"] is False for item in contracts),
        "pbc": PBC_KEY,
        "contracts": contracts,
        "routes": tuple(item["route_id"] for item in contracts),
        "workflow_routes": tuple(
            item["route_id"]
            for item in contracts
            if item["service_operation"]["operation"] in {
                "provision_tenant",
                "link_identity",
                "verify_credential",
                "assign_role",
                "grant_token",
                "approve_privileged_access",
            }
        ),
        "side_effects": (),
    }


def validate_api_route_contracts() -> dict:
    """Validate routes against service operations, permissions, idempotency, and table boundaries."""
    manifest = api_route_contracts()
    contracts = manifest["contracts"]
    service_mismatches = tuple(
        item["route_id"]
        for item in contracts
        if item["service_operation"]["method"] != item["method"]
        or item["service_operation"]["path"] != item["path"]
        or item["service_operation"]["permission"] != item["permission"]
    )
    missing_idempotency = tuple(
        item["route_id"]
        for item in contracts
        if item["service_operation"]["operation_kind"] == "command"
        and item["service_operation"]["operation"] not in {"run_control_tests", "verify_owned_table_boundary"}
        and not item["idempotency_key"]
    )
    invalid_table_scope = tuple(
        item["route_id"]
        for item in contracts
        for table in item["service_operation"]["owned_tables"] + item["service_operation"]["read_tables"]
        if not table.startswith(f"{PBC_KEY}_")
    )
    invalid_permissions = tuple(
        item["route_id"]
        for item in contracts
        if not permissions.resolve_required_permission(item["handler"])
    )
    return {
        "ok": manifest["ok"]
        and not service_mismatches
        and not missing_idempotency
        and not invalid_table_scope
        and not invalid_permissions,
        "pbc": PBC_KEY,
        "contracts": contracts,
        "service_mismatches": service_mismatches,
        "missing_idempotency": missing_idempotency,
        "invalid_table_scope": invalid_table_scope,
        "invalid_permissions": invalid_permissions,
        "side_effects": (),
    }


def dispatch_route(
    method: str,
    path: str,
    payload: dict | None = None,
    *,
    service: FederatedIamService | None = None,
    granted_permissions: tuple[str, ...] = (),
) -> dict:
    """Dispatch a route contract to its service command without side effects."""
    route = next((item for item in ROUTES if item["method"] == method and item["path"] == path), None)
    if route is None:
        return {"ok": False, "handled": False, "reason": "route_not_found", "side_effects": ()}
    active_service = service or create_seeded_service(granted_permissions)
    result = active_service.execute(route["handler"], payload or {})
    return {
        "ok": result.get("ok") is True,
        "handled": True,
        "route": route,
        "result": result,
        "state": active_service.state,
        "side_effects": (),
    }


def route_catalog_contract() -> dict:
    """Return a compact catalog view for standalone installers and docs."""
    manifest = api_route_contracts()
    return {
        "ok": manifest["ok"],
        "pbc": PBC_KEY,
        "routes": tuple(
            {
                "route": item["route_id"],
                "handler": item["handler"],
                "permission": item["permission"],
                "workflow": item["handler"] in {
                    "provision_tenant",
                    "link_identity",
                    "verify_credential",
                    "assign_role",
                    "grant_token",
                    "approve_privileged_access",
                },
            }
            for item in manifest["contracts"]
        ),
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Execute command and query route dispatch plus validation."""
    validation = validate_api_route_contracts()
    command = dispatch_route("POST", "/iam/parameters", {"name": "token_ttl_minutes", "value": 75})
    query = dispatch_route("GET", "/iam-workbench", {"tenant": "tenant_seed_alpha"})
    return {
        "ok": validation["ok"] and command["ok"] and query["ok"],
        "validation": validation,
        "dispatch": command,
        "query": query,
        "side_effects": (),
    }
