"""Route contracts for the electronic_health_records_core PBC."""
from __future__ import annotations

from .services import ElectronicHealthRecordsCoreService, service_operation_contracts, service_operation_manifest

PBC_KEY = "electronic_health_records_core"
ROUTES = (
    "POST /patient-charts",
    "POST /clinical-encounters",
    "POST /clinical-orders",
    "POST /clinical-orders/transition",
    "POST /observations",
    "POST /observations/acknowledgements",
    "POST /allergies",
    "POST /allergys",
    "POST /medication-reconciliations",
    "POST /care-notes",
    "POST /care-notes/attestations",
    "GET /patient-summaries",
    "GET /electronic-health-records-core/forms",
    "GET /electronic-health-records-core/wizards",
    "GET /electronic-health-records-core/controls",
    "GET /electronic-health-records-core-workbench",
)
ROUTE_TO_OPERATION = {
    "POST /patient-charts": "create_patient_chart",
    "POST /clinical-encounters": "record_clinical_encounter",
    "POST /clinical-orders": "review_clinical_order",
    "POST /clinical-orders/transition": "transition_clinical_order",
    "POST /observations": "approve_observation",
    "POST /observations/acknowledgements": "acknowledge_critical_result",
    "POST /allergies": "simulate_allergy",
    "POST /allergys": "simulate_allergy",
    "POST /medication-reconciliations": "create_medication_list",
    "POST /care-notes": "record_care_note",
    "POST /care-notes/attestations": "attest_care_note",
    "GET /patient-summaries": "assemble_patient_summary",
    "GET /electronic-health-records-core-workbench": "query_workbench",
}


def api_route_contracts() -> dict:
    contracts = tuple(
        {
            "route": route,
            "method": route.split()[0],
            "path": route.split()[1],
            "pbc": PBC_KEY,
            "operation": ROUTE_TO_OPERATION.get(route),
            "idempotency_key": f"{PBC_KEY}:{route}",
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
            "shared_table_access": False,
            "required_permission": f"{PBC_KEY}.operate",
        }
        for route in ROUTES
    )
    return {"ok": True, "pbc": PBC_KEY, "contracts": contracts, "routes": ROUTES, "side_effects": ()}


def validate_api_route_contracts() -> dict:
    contracts = api_route_contracts()["contracts"]
    manifest = service_operation_manifest()
    service_ops = set(manifest["command_operations"] + manifest["query_operations"])
    mismatches = tuple(contract for contract in contracts if contract.get("operation") and contract["operation"] not in service_ops)
    return {
        "ok": not mismatches,
        "pbc": PBC_KEY,
        "service_mismatches": mismatches,
        "missing_idempotency": tuple(contract for contract in contracts if not contract["idempotency_key"]),
        "invalid_table_scope": (),
        "side_effects": (),
    }


def dispatch_route(route: str, payload: dict | None = None, service: ElectronicHealthRecordsCoreService | None = None) -> dict:
    payload = dict(payload or {})
    operation = ROUTE_TO_OPERATION.get(route)
    result = None
    if route in ROUTES and service is not None and operation:
        result = getattr(service, operation)(payload)
    return {
        "ok": route in ROUTES,
        "route": route,
        "payload": payload,
        "operation": operation,
        "service_operations": service_operation_manifest()["command_operations"] + service_operation_manifest()["query_operations"],
        "operation_contract": service_operation_contracts()["operation_contract"],
        "result": result,
        "side_effects": (),
    }


def smoke_test() -> dict:
    return {
        "ok": api_route_contracts()["ok"] and validate_api_route_contracts()["ok"] and dispatch_route(ROUTES[0])["ok"],
        "side_effects": (),
    }
