"""API route contracts for the standalone aviation maintenance repair slice."""
from __future__ import annotations

from .services import service_operation_contracts
from .ui import aviation_maintenance_repair_form_contracts, aviation_maintenance_repair_wizard_contracts

PBC_KEY = "aviation_maintenance_repair"
ROUTE_DEFINITIONS = (
    {"route": "POST /aviation-maintenance-repair/aircrafts", "operation": "record_aircraft", "permission": f"{PBC_KEY}.create", "form": "aircraft_intake_form"},
    {"route": "POST /aviation-maintenance-repair/components", "operation": "record_component", "permission": f"{PBC_KEY}.create", "form": "component_installation_form"},
    {"route": "POST /aviation-maintenance-repair/work-cards", "operation": "record_work_card", "permission": f"{PBC_KEY}.update", "form": "work_card_closeout_form"},
    {"route": "POST /aviation-maintenance-repair/deferred-defects", "operation": "record_deferred_defect", "permission": f"{PBC_KEY}.update", "form": "work_card_closeout_form"},
    {"route": "POST /aviation-maintenance-repair/airworthiness-directives", "operation": "record_airworthiness_directive", "permission": f"{PBC_KEY}.update", "form": "work_card_closeout_form"},
    {"route": "POST /aviation-maintenance-repair/document-instructions:plan", "operation": "plan_document_instruction", "permission": f"{PBC_KEY}.update", "wizard": "document_instruction_wizard"},
    {"route": "POST /aviation-maintenance-repair/release-plans", "operation": "assess_release_to_service", "permission": f"{PBC_KEY}.approve", "wizard": "release_to_service_wizard"},
    {"route": "GET /aviation-maintenance-repair/workbench", "operation": "query_workbench", "permission": f"{PBC_KEY}.read"},
)
ROUTES = tuple(item["route"] for item in ROUTE_DEFINITIONS)


def api_route_contracts():
    form_ids = {item["form_id"] for item in aviation_maintenance_repair_form_contracts()}
    wizard_ids = {item["wizard_id"] for item in aviation_maintenance_repair_wizard_contracts()}
    contracts = []
    for route in ROUTE_DEFINITIONS:
        method, path = route["route"].split(" ", 1)
        contract = {
            "route": route["route"],
            "method": method,
            "path": path,
            "pbc": PBC_KEY,
            "operation": route["operation"],
            "idempotency_key": f"{PBC_KEY}:{route['operation']}:{method}",
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
            "shared_table_access": False,
            "required_permission": route["permission"],
            "form": route.get("form") if route.get("form") in form_ids else None,
            "wizard": route.get("wizard") if route.get("wizard") in wizard_ids else None,
        }
        contracts.append(contract)
    return {"ok": True, "pbc": PBC_KEY, "contracts": tuple(contracts), "routes": ROUTES, "side_effects": ()}


def validate_api_route_contracts():
    service_operations = {contract["operation"] for contract in service_operation_contracts()["contracts"]}
    contracts = api_route_contracts()["contracts"]
    missing_operations = tuple(contract["operation"] for contract in contracts if contract["operation"] not in service_operations)
    missing_idempotency = tuple(contract for contract in contracts if not contract["idempotency_key"])
    return {"ok": not missing_operations and not missing_idempotency, "pbc": PBC_KEY, "service_mismatches": missing_operations, "missing_idempotency": missing_idempotency, "invalid_table_scope": (), "side_effects": ()}


def dispatch_route(route, payload=None):
    contract = next((item for item in api_route_contracts()["contracts"] if item["route"] == route), None)
    return {"ok": contract is not None, "route": route, "payload": dict(payload or {}), "contract": contract, "operation_contract": service_operation_contracts()["operation_contract"], "side_effects": ()}


def smoke_test():
    contracts = api_route_contracts()
    return {"ok": contracts["ok"] and validate_api_route_contracts()["ok"] and dispatch_route(ROUTES[0])["ok"], "side_effects": ()}
