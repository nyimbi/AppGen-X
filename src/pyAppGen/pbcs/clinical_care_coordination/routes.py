"""HTTP route contracts and executable dispatch for clinical_care_coordination."""

from __future__ import annotations

from .care_coordination_app import (
    care_coordination_controls_contract,
    care_coordination_forms_contract,
    care_coordination_wizards_contract,
)
from .services import ClinicalCareCoordinationService
from .services import service_operation_contracts
from .services import service_operation_manifest


PBC_KEY = "clinical_care_coordination"
ROUTE_TO_OPERATION = {
    "POST /patient-care-plans": "create_care_plan",
    "POST /care-teams": "add_care_team_member",
    "POST /referrals": "create_referral",
    "POST /encounters": "record_encounter_and_tasks",
    "POST /care-gaps": "open_care_gap",
    "POST /transition-plans": "create_transition_plan",
    "POST /outcome-measures": "record_outcome_measure",
    "GET /clinical-care-coordination-workbench": "query_workbench",
}
ROUTES = tuple(ROUTE_TO_OPERATION) + (
    "GET /clinical-care-coordination/forms",
    "GET /clinical-care-coordination/wizards",
    "GET /clinical-care-coordination/controls",
)


def api_route_contracts() -> dict:
    contracts = tuple(
        {
            "route": route,
            "method": route.split()[0],
            "path": route.split()[1],
            "pbc": PBC_KEY,
            "idempotency_key": f"{PBC_KEY}:{route}" if route.startswith("POST ") else None,
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
            "shared_table_access": False,
            "required_permission": f"{PBC_KEY}.operate" if route.startswith("POST ") else f"{PBC_KEY}.read",
            "operation": ROUTE_TO_OPERATION.get(route),
        }
        for route in ROUTES
    )
    return {"ok": True, "pbc": PBC_KEY, "contracts": contracts, "routes": ROUTES, "side_effects": ()}


def validate_api_route_contracts() -> dict:
    manifest = service_operation_manifest()
    contracts = api_route_contracts()["contracts"]
    service_operations = set(manifest["command_operations"] + manifest["query_operations"])
    mismatches = tuple(
        contract["route"]
        for contract in contracts
        if contract["operation"] is not None and contract["operation"] not in service_operations
    )
    return {
        "ok": not mismatches,
        "pbc": PBC_KEY,
        "service_mismatches": mismatches,
        "missing_idempotency": tuple(
            contract["route"] for contract in contracts if contract["route"].startswith("POST ") and not contract["idempotency_key"]
        ),
        "invalid_table_scope": (),
        "side_effects": (),
    }


def dispatch_route(route: str, payload: dict | None = None, service: ClinicalCareCoordinationService | None = None) -> dict:
    payload = dict(payload or {})
    if route not in ROUTES:
        return {"ok": False, "route": route, "reason": "route_not_found", "side_effects": ()}

    if route == "GET /clinical-care-coordination/forms":
        return {
            "ok": True,
            "route": route,
            "operation": "forms_contract",
            "result": care_coordination_forms_contract(),
            "side_effects": (),
        }
    if route == "GET /clinical-care-coordination/wizards":
        return {
            "ok": True,
            "route": route,
            "operation": "wizards_contract",
            "result": care_coordination_wizards_contract(),
            "side_effects": (),
        }
    if route == "GET /clinical-care-coordination/controls":
        return {
            "ok": True,
            "route": route,
            "operation": "controls_contract",
            "result": care_coordination_controls_contract(),
            "side_effects": (),
        }

    route_service = service or ClinicalCareCoordinationService()
    operation = ROUTE_TO_OPERATION[route]
    result = getattr(route_service, operation)(payload)
    return {
        "ok": result.get("ok", False),
        "route": route,
        "payload": payload,
        "operation": operation,
        "service_operations": service_operation_manifest()["command_operations"]
        + service_operation_manifest()["query_operations"],
        "operation_contract": next(
            contract
            for contract in service_operation_contracts()["contracts"]
            if contract["operation"] == operation
        ),
        "result": result,
        "side_effects": (),
    }


def smoke_test() -> dict:
    service = ClinicalCareCoordinationService()
    create = dispatch_route(
        "POST /patient-care-plans",
        {
            "patient_ref": "patient-smoke",
            "problem": "post discharge follow-up",
            "goal": "close referral loop",
            "responsible_role": "primary_coordinator",
            "review_cadence_days": 7,
        },
        service=service,
    )
    workbench = dispatch_route("GET /clinical-care-coordination-workbench", service=service)
    return {
        "ok": api_route_contracts()["ok"] and validate_api_route_contracts()["ok"] and create["ok"] and workbench["ok"],
        "side_effects": (),
    }
