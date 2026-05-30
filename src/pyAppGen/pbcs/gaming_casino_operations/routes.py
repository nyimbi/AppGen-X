"""Route contracts and standalone dispatch for gaming_casino_operations."""

from __future__ import annotations

from typing import Any

from .permissions import ACTION_PERMISSIONS
from .services import (
    GamingCasinoOperationsStandaloneService,
    service_operation_contracts,
    standalone_service_operation_contracts,
)


PBC_KEY = "gaming_casino_operations"
ROUTES = (
    "POST /player-profiles",
    "POST /table-games",
    "POST /slot-machines",
    "POST /wager-sessions",
    "POST /payouts",
    "GET /gaming-casino-operations-workbench",
)
PUBLIC_ROUTE_MAP = {
    "POST /player-profiles": "create_player_profile",
    "POST /table-games": "handle_table_game",
    "POST /slot-machines": "handle_slot_machine",
    "POST /wager-sessions": "handle_wager_session",
    "POST /payouts": "handle_payout",
    "GET /gaming-casino-operations-workbench": "build_workbench_view",
}
STANDALONE_ROUTE_DEFINITIONS = (
    {"method": "POST", "path": "/app/gaming-casino-operations/player-profiles", "service_method": "create_player_profile"},
    {"method": "POST", "path": "/app/gaming-casino-operations/table-games", "service_method": "handle_table_game"},
    {"method": "POST", "path": "/app/gaming-casino-operations/slot-machines", "service_method": "handle_slot_machine"},
    {"method": "POST", "path": "/app/gaming-casino-operations/wager-sessions", "service_method": "handle_wager_session"},
    {"method": "POST", "path": "/app/gaming-casino-operations/payouts", "service_method": "handle_payout"},
    {"method": "POST", "path": "/app/gaming-casino-operations/responsible-gaming-cases", "service_method": "open_responsible_gaming_case"},
    {"method": "POST", "path": "/app/gaming-casino-operations/compliance-cases", "service_method": "record_compliance_case"},
    {"method": "POST", "path": "/app/gaming-casino-operations/workflows/player-enrollment", "service_method": "run_player_enrollment_workflow"},
    {"method": "POST", "path": "/app/gaming-casino-operations/workflows/table-shift-close", "service_method": "run_table_shift_close_workflow"},
    {"method": "POST", "path": "/app/gaming-casino-operations/workflows/jackpot-handpay", "service_method": "run_jackpot_handpay_workflow"},
    {"method": "GET", "path": "/app/gaming-casino-operations/workbench", "service_method": "build_workbench_view"},
)


def api_route_contracts() -> dict[str, Any]:
    operations = service_operation_contracts()["contracts"]
    operation_lookup = {contract["operation"]: contract for contract in operations}
    contracts = tuple(
        {
            "route": route,
            "method": route.split()[0],
            "path": route.split()[1],
            "pbc": PBC_KEY,
            "service_method": PUBLIC_ROUTE_MAP[route],
            "idempotency_key": f"{PBC_KEY}:{route}",
            "required_permission": ACTION_PERMISSIONS.get(PUBLIC_ROUTE_MAP[route]),
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
            "shared_table_access": False,
            "operation_contract": operation_lookup.get(PUBLIC_ROUTE_MAP[route]),
        }
        for route in ROUTES
    )
    return {"ok": True, "pbc": PBC_KEY, "contracts": contracts, "routes": ROUTES, "side_effects": ()}


def validate_api_route_contracts() -> dict[str, Any]:
    contracts = api_route_contracts()["contracts"]
    mismatches = tuple(contract for contract in contracts if contract["operation_contract"] is None)
    return {
        "ok": not mismatches,
        "pbc": PBC_KEY,
        "service_mismatches": mismatches,
        "missing_idempotency": (),
        "invalid_table_scope": (),
        "side_effects": (),
    }


def standalone_route_contracts() -> dict[str, Any]:
    service_contracts = standalone_service_operation_contracts()["contracts"]
    lookup = {contract["operation"]: contract for contract in service_contracts}
    routes = tuple(
        {
            **definition,
            "required_permission": ACTION_PERMISSIONS.get(definition["service_method"]),
            "service_contract": lookup.get(definition["service_method"]),
            "idempotency_key": f"{PBC_KEY}:{definition["method"]}:{definition["path"]}",
            "stream_engine_picker_visible": False,
        }
        for definition in STANDALONE_ROUTE_DEFINITIONS
    )
    return {"ok": True, "pbc": PBC_KEY, "contracts": routes, "side_effects": ()}


def dispatch_route(route: str, payload: dict[str, Any] | None = None, *, service: GamingCasinoOperationsStandaloneService | None = None) -> dict[str, Any]:
    if route not in PUBLIC_ROUTE_MAP:
        return {"ok": False, "route": route, "reason": "unknown_route", "side_effects": ()}
    local_service = service or GamingCasinoOperationsStandaloneService()
    method = getattr(local_service, PUBLIC_ROUTE_MAP[route])
    result = method(dict(payload or {}))
    return {"ok": result.get("ok") is True, "route": route, "result": result, "side_effects": ()}


def dispatch_standalone_route(method: str, path: str, payload: dict[str, Any] | None = None, *, service: GamingCasinoOperationsStandaloneService | None = None) -> dict[str, Any]:
    definition = next((item for item in STANDALONE_ROUTE_DEFINITIONS if item["method"] == method and item["path"] == path), None)
    if definition is None:
        return {"ok": False, "method": method, "path": path, "reason": "unknown_route", "side_effects": ()}
    local_service = service or GamingCasinoOperationsStandaloneService()
    handler = getattr(local_service, definition["service_method"])
    result = handler(dict(payload or {}))
    return {"ok": result.get("ok") is True, "method": method, "path": path, "result": result, "side_effects": ()}


def smoke_test() -> dict[str, Any]:
    service = GamingCasinoOperationsStandaloneService()
    create = dispatch_route(
        "POST /player-profiles",
        {
            "tenant": "tenant-smoke",
            "player_number": "P-ROUTE",
            "legal_name": "Route Patron",
            "date_of_birth": "1992-02-02",
            "identity_confidence": 0.98,
            "age_verified": True,
        },
        service=service,
    )
    workbench = dispatch_standalone_route(
        "GET",
        "/app/gaming-casino-operations/workbench",
        {"tenant": "tenant-smoke"},
        service=service,
    )
    return {
        "ok": api_route_contracts()["ok"] and standalone_route_contracts()["ok"] and create["ok"] and workbench["ok"],
        "create": create,
        "workbench": workbench,
        "side_effects": (),
    }
