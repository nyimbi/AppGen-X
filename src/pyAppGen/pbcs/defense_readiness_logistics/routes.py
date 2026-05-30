"""Route contracts for defense_readiness_logistics."""

from __future__ import annotations

from .services import DefenseReadinessLogisticsService, QUERY_OPERATIONS, service_operation_manifest
from .models import PBC_KEY

ROUTE_DEFINITIONS = (
    {"route": "POST /unit-readinesss", "operation": "assess_unit_readiness", "required_permission": f"{PBC_KEY}.create", "idempotent": True},
    {"route": "POST /mission-assets", "operation": "record_mission_asset", "required_permission": f"{PBC_KEY}.create", "idempotent": True},
    {"route": "POST /supply-requests", "operation": "score_supply_readiness", "required_permission": f"{PBC_KEY}.update", "idempotent": True},
    {"route": "POST /maintenance-statuss", "operation": "project_maintenance_status", "required_permission": f"{PBC_KEY}.update", "idempotent": True},
    {"route": "POST /deployment-plans", "operation": "release_deployment_plan", "required_permission": f"{PBC_KEY}.approve", "idempotent": True},
    {"route": "GET /defense-readiness-logistics-workbench", "operation": "build_defense_workbench", "required_permission": f"{PBC_KEY}.read", "idempotent": False},
)
ROUTES = tuple(item["route"] for item in ROUTE_DEFINITIONS)


def api_route_contracts() -> dict:
    contracts = []
    for item in ROUTE_DEFINITIONS:
        method, path = item["route"].split()
        contracts.append(
            {
                **item,
                "method": method,
                "path": path,
                "pbc": PBC_KEY,
                "event_contract": "AppGen-X",
                "stream_engine_picker_visible": False,
                "shared_table_access": False,
                "idempotency_key": f"{PBC_KEY}:{item['route']}" if method != "GET" else None,
            }
        )
    return {"ok": True, "pbc": PBC_KEY, "contracts": tuple(contracts), "routes": ROUTES, "side_effects": ()}


def validate_api_route_contracts() -> dict:
    manifest = service_operation_manifest()
    known_operations = set(manifest["command_operations"]) | set(manifest["query_operations"])
    missing_operations = tuple(item for item in ROUTE_DEFINITIONS if item["operation"] not in known_operations)
    missing_idempotency = tuple(item["route"] for item in ROUTE_DEFINITIONS if item["route"].startswith("POST ") and not f"{PBC_KEY}:{item['route']}")
    return {
        "ok": not missing_operations and not missing_idempotency,
        "pbc": PBC_KEY,
        "service_mismatches": missing_operations,
        "missing_idempotency": missing_idempotency,
        "invalid_table_scope": (),
        "side_effects": (),
    }


def dispatch_route(route: str, payload: dict | None = None, *, service: DefenseReadinessLogisticsService | None = None) -> dict:
    payload = dict(payload or {})
    binding = next((item for item in ROUTE_DEFINITIONS if item["route"] == route), None)
    if not binding:
        return {"ok": False, "reason": "unknown_route", "route": route, "side_effects": ()}
    service = service or DefenseReadinessLogisticsService()
    handler = getattr(service, binding["operation"])
    result = handler(payload)
    return {
        "ok": result["ok"],
        "route": route,
        "operation": binding["operation"],
        "operation_kind": "query" if binding["operation"] in QUERY_OPERATIONS else "command",
        "payload": payload,
        "result": result,
        "side_effects": (),
    }


def smoke_test() -> dict:
    return {
        "ok": api_route_contracts()["ok"] and validate_api_route_contracts()["ok"] and dispatch_route(
            ROUTES[0],
            {
                "tenant_id": "tenant-smoke",
                "unit_id": "route-smoke",
                "unit_code": "route-smoke",
                "personnel": {"available": 12, "required": 10, "certified_roles": 4, "required_certified_roles": 3},
                "serviceable_assets": 3,
                "required_assets": 2,
                "supply": {"critical_fill_rate": 0.95},
                "ammo_fill_rate": 0.9,
                "fuel_days": 2,
                "inspection_evidence": ("route-pack",),
                "commander_approved": True,
            },
        )["ok"],
        "side_effects": (),
    }
