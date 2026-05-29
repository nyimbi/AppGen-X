"""API and standalone route contracts for energy_grid_operations."""

from __future__ import annotations

from .services import EnergyGridOperationsService, operation_plan, service_operation_contracts

PBC_KEY = "energy_grid_operations"
PUBLIC_ROUTE_SPECS = (
    {"method": "POST", "path": "/grid-assets", "operation": "create_grid_asset"},
    {"method": "POST", "path": "/load-forecasts", "operation": "record_load_forecast"},
    {"method": "POST", "path": "/switching-orders", "operation": "review_switching_order"},
    {"method": "POST", "path": "/dispatch-instructions", "operation": "approve_dispatch_instruction"},
    {"method": "POST", "path": "/outage-events", "operation": "simulate_outage_event"},
    {"method": "GET", "path": "/energy-grid-operations-workbench", "operation": "build_workbench_view"},
)
STANDALONE_ROUTE_SPECS = PUBLIC_ROUTE_SPECS + (
    {"method": "POST", "path": "/api/pbc/energy_grid_operations/runtime/configuration", "operation": "configure_runtime"},
    {"method": "POST", "path": "/api/pbc/energy_grid_operations/runtime/parameters", "operation": "approve_energy_grid_operations_runtime_parameter"},
    {"method": "POST", "path": "/api/pbc/energy_grid_operations/runtime/rules", "operation": "review_energy_grid_operations_policy_rule"},
    {"method": "POST", "path": "/api/pbc/energy_grid_operations/events/inbox", "operation": "receive_event"},
    {"method": "POST", "path": "/api/pbc/energy_grid_operations/topology", "operation": "record_grid_topology"},
    {"method": "POST", "path": "/api/pbc/energy_grid_operations/reliability-constraints", "operation": "create_reliability_constraint"},
    {"method": "POST", "path": "/api/pbc/energy_grid_operations/control-assertions", "operation": "create_energy_grid_operations_control_assertion"},
    {"method": "POST", "path": "/api/pbc/energy_grid_operations/governed-models", "operation": "record_energy_grid_operations_governed_model"},
    {"method": "POST", "path": "/api/pbc/energy_grid_operations/schema-extensions", "operation": "simulate_energy_grid_operations_schema_extension"},
    {"method": "GET", "path": "/api/pbc/energy_grid_operations/timeline", "operation": "query_timeline"},
    {"method": "GET", "path": "/app/energy-grid-operations/workbench", "operation": "build_workbench_view"},
)
ROUTES = tuple(f"{item['method']} {item['path']}" for item in PUBLIC_ROUTE_SPECS)


def _contract_from_spec(spec: dict) -> dict:
    plan = operation_plan(spec["operation"])
    return {
        "route": f"{spec['method']} {spec['path']}",
        "method": spec["method"],
        "path": spec["path"],
        "operation": spec["operation"],
        "pbc": PBC_KEY,
        "idempotency_key": f"{PBC_KEY}:{spec['method']}:{spec['path']}",
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "required_permission": plan.get("permission"),
    }


def api_route_contracts() -> dict:
    contracts = tuple(_contract_from_spec(spec) for spec in PUBLIC_ROUTE_SPECS)
    return {"ok": True, "pbc": PBC_KEY, "contracts": contracts, "routes": ROUTES, "side_effects": ()}


def standalone_route_contracts() -> dict:
    contracts = tuple(_contract_from_spec(spec) for spec in STANDALONE_ROUTE_SPECS)
    return {
        "format": "appgen.energy-grid-operations-standalone-routes.v2",
        "ok": True,
        "pbc": PBC_KEY,
        "contracts": contracts,
        "routes": tuple(item["route"] for item in contracts),
        "side_effects": (),
    }


def validate_api_route_contracts() -> dict:
    contracts = api_route_contracts()["contracts"]
    service_contract = service_operation_contracts()
    service_ops = set(service_contract["operations"])
    missing = tuple(contract for contract in contracts if contract["operation"] not in service_ops)
    return {
        "ok": not missing,
        "pbc": PBC_KEY,
        "service_mismatches": missing,
        "missing_idempotency": tuple(contract for contract in contracts if not contract["idempotency_key"]),
        "invalid_table_scope": (),
        "side_effects": (),
    }


def dispatch_route(method_or_route: str, path: str | dict | None = None, payload: dict | None = None, *, service: EnergyGridOperationsService | None = None) -> dict:
    if isinstance(path, dict) and payload is None:
        payload = path
        path = None
    if path is None and " " in method_or_route:
        method, resolved_path = method_or_route.split(" ", 1)
    else:
        method = method_or_route
        resolved_path = str(path)
    supplied = dict(payload or {})
    spec = next(
        (item for item in STANDALONE_ROUTE_SPECS if item["method"] == method and item["path"] == resolved_path),
        None,
    )
    if spec is None:
        return {"ok": False, "reason": "unknown_route", "method": method, "path": resolved_path, "side_effects": ()}
    active_service = service or EnergyGridOperationsService()
    result = active_service.execute(spec["operation"], supplied)
    return {
        "ok": result["ok"],
        "method": method,
        "path": resolved_path,
        "operation": spec["operation"],
        "result": result,
        "side_effects": (),
    }


def dispatch_standalone_route(method: str, path: str, payload: dict | None = None, *, service: EnergyGridOperationsService | None = None) -> dict:
    return dispatch_route(method, path, payload, service=service)


def smoke_test() -> dict:
    service = EnergyGridOperationsService()
    dispatched = dispatch_route(
        "POST",
        "/grid-assets",
        {
            "asset_id": "asset_route_smoke",
            "tenant": "tenant_route",
            "asset_type": "breaker",
            "asset_name": "Route Smoke Breaker",
            "voltage_kv": 11,
            "substation_id": "sub_route",
            "feeder_id": "feeder_route",
            "normal_state": "closed",
        },
        service=service,
    )
    workbench = dispatch_route("GET", "/energy-grid-operations-workbench", {"tenant": "tenant_route"}, service=service)
    return {
        "ok": api_route_contracts()["ok"] and validate_api_route_contracts()["ok"] and dispatched["ok"] and workbench["ok"],
        "side_effects": (),
    }
