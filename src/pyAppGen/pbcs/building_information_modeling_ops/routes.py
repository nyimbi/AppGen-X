"""Route contracts for the single-PBC BIM federation app."""
from __future__ import annotations

from .services import service_operation_contracts

PBC_KEY = "building_information_modeling_ops"
ROUTES = (
    "POST /bim-models",
    "POST /model-versions",
    "POST /federations/project-coordinates",
    "POST /federations/model-packages",
    "POST /federations/assemblies",
    "GET /building-information-modeling-ops-workbench",
    "GET /building-information-modeling-ops/forms",
    "GET /building-information-modeling-ops/wizards",
    "GET /building-information-modeling-ops/controls",
)


def _route_operation(route: str) -> str:
    mapping = {
        "POST /bim-models": "command_bim_model",
        "POST /model-versions": "register_model_package",
        "POST /federations/project-coordinates": "configure_project_coordinates",
        "POST /federations/model-packages": "register_model_package",
        "POST /federations/assemblies": "assemble_federation",
        "GET /building-information-modeling-ops-workbench": "query_workbench",
        "GET /building-information-modeling-ops/forms": "build_forms_contract",
        "GET /building-information-modeling-ops/wizards": "build_wizard_contract",
        "GET /building-information-modeling-ops/controls": "build_controls_contract",
    }
    return mapping[route]


def api_route_contracts() -> dict:
    contracts = tuple(
        {
            "route": route,
            "method": route.split()[0],
            "path": route.split()[1],
            "pbc": PBC_KEY,
            "operation": _route_operation(route),
            "idempotency_key": f"{PBC_KEY}:{route}",
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
            "shared_table_access": False,
            "single_pbc_app": True,
            "required_permission": f"{PBC_KEY}.operate"
            if route.startswith("POST ")
            else f"{PBC_KEY}.read",
        }
        for route in ROUTES
    )
    return {"ok": True, "pbc": PBC_KEY, "contracts": contracts, "routes": ROUTES, "side_effects": ()}


def validate_api_route_contracts() -> dict:
    contracts = api_route_contracts()["contracts"]
    valid_operations = {
        contract["operation"]
        for contract in service_operation_contracts()["contracts"]
    }
    service_mismatches = tuple(
        contract["route"]
        for contract in contracts
        if contract["operation"] not in valid_operations
    )
    return {
        "ok": not service_mismatches,
        "pbc": PBC_KEY,
        "service_mismatches": service_mismatches,
        "missing_idempotency": tuple(c for c in contracts if not c["idempotency_key"]),
        "invalid_table_scope": (),
        "side_effects": (),
    }


def dispatch_route(route: str, payload: dict | None = None) -> dict:
    return {
        "ok": route in ROUTES,
        "route": route,
        "payload": dict(payload or {}),
        "operation": _route_operation(route) if route in ROUTES else None,
        "operation_contract": service_operation_contracts()["operation_contract"],
        "side_effects": (),
    }


def smoke_test() -> dict:
    return {
        "ok": api_route_contracts()["ok"]
        and validate_api_route_contracts()["ok"]
        and dispatch_route(ROUTES[0])["ok"],
        "side_effects": (),
    }
