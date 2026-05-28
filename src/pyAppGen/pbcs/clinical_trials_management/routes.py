"""API route contracts for the clinical_trials_management PBC."""

from __future__ import annotations

from .services import ClinicalTrialsManagementService
from .services import service_operation_contracts


ROUTES = (
    {"method": "POST", "path": "/api/pbc/clinical_trials_management/trial-protocols", "handler": "command_trial_protocols", "permission": "clinical_trials_management.protocol_admin"},
    {"method": "POST", "path": "/api/pbc/clinical_trials_management/study-sites", "handler": "command_study_sites", "permission": "clinical_trials_management.site_activation"},
    {"method": "POST", "path": "/api/pbc/clinical_trials_management/subjects", "handler": "command_subjects", "permission": "clinical_trials_management.subject_enrollment"},
    {"method": "POST", "path": "/api/pbc/clinical_trials_management/consent-records", "handler": "command_consent_records", "permission": "clinical_trials_management.consent_manage"},
    {"method": "POST", "path": "/api/pbc/clinical_trials_management/visit-schedules", "handler": "command_visit_schedules", "permission": "clinical_trials_management.visit_manage"},
    {"method": "POST", "path": "/api/pbc/clinical_trials_management/adverse-events", "handler": "command_adverse_events", "permission": "clinical_trials_management.safety_review"},
    {"method": "POST", "path": "/api/pbc/clinical_trials_management/monitoring-findings", "handler": "command_monitoring_findings", "permission": "clinical_trials_management.monitoring_manage"},
    {"method": "POST", "path": "/api/pbc/clinical_trials_management/policy-rules", "handler": "command_policy_rules", "permission": "clinical_trials_management.configure"},
    {"method": "POST", "path": "/api/pbc/clinical_trials_management/runtime-parameters", "handler": "command_runtime_parameters", "permission": "clinical_trials_management.configure"},
    {"method": "GET", "path": "/api/pbc/clinical_trials_management/clinical-trials-workbench", "handler": "query_clinical_trials_management_workbench", "permission": "clinical_trials_management.read"},
    {"method": "GET", "path": "/api/pbc/clinical_trials_management/controls", "handler": "query_clinical_trials_management_controls", "permission": "clinical_trials_management.audit"},
    {"method": "POST", "path": "/api/pbc/clinical_trials_management/assistant/document-preview", "handler": "query_clinical_trials_management_assistant_preview", "permission": "clinical_trials_management.audit"},
)


def _build_route_contracts() -> tuple[dict, ...]:
    service_contracts = service_operation_contracts()["contracts"]
    indexed = {item["operation"]: item for item in service_contracts}
    contracts = []
    for route in ROUTES:
        operation = route["handler"]
        service_operation = indexed.get(operation)
        contracts.append(
            {
                **route,
                "operation": operation,
                "operation_kind": service_operation["operation_kind"],
                "owned_tables": service_operation["owned_tables"],
                "read_tables": service_operation["read_tables"],
                "emitted_event": service_operation["emitted_event"],
                "event_contract": "AppGen-X",
                "transaction_boundary": service_operation["transaction_boundary"],
                "idempotency_required": service_operation["operation_kind"] == "command",
                "idempotency_key": f"clinical_trials_management:{operation}:idempotency_key" if service_operation["operation_kind"] == "command" else None,
                "shared_table_access": False,
                "stream_engine_picker_visible": False,
                "service_operation": service_operation,
                "route_id": f"{route['method']} {route['path']}",
            }
        )
    return tuple(contracts)


API_ROUTE_CONTRACTS = _build_route_contracts()


def register_routes(app=None):
    return ROUTES


def api_route_contracts() -> dict:
    contracts = tuple(API_ROUTE_CONTRACTS)
    return {
        "ok": bool(contracts)
        and all(item["event_contract"] == "AppGen-X" for item in contracts)
        and all(item["stream_engine_picker_visible"] is False for item in contracts)
        and all(item["shared_table_access"] is False for item in contracts),
        "pbc": "clinical_trials_management",
        "contracts": contracts,
        "routes": tuple(item["route_id"] for item in contracts),
        "side_effects": (),
    }


def validate_api_route_contracts() -> dict:
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
    missing_idempotency = tuple(item["route_id"] for item in contracts if item["idempotency_required"] and not item["idempotency_key"])
    invalid_table_scope = tuple(
        item["route_id"]
        for item in contracts
        for table in item["owned_tables"] + item["read_tables"]
        if not table.startswith("clinical_trials_management_")
    )
    return {
        "ok": manifest["ok"] and not service_mismatches and not missing_idempotency and not invalid_table_scope,
        "pbc": "clinical_trials_management",
        "contracts": contracts,
        "service_mismatches": service_mismatches,
        "missing_idempotency": missing_idempotency,
        "invalid_table_scope": invalid_table_scope,
        "side_effects": (),
    }


def dispatch_route(method: str, path: str, payload: dict | None = None) -> dict:
    route = next((item for item in ROUTES if item["method"] == method and item["path"] == path), None)
    if route is None:
        return {"ok": False, "handled": False, "reason": "route_not_found"}
    service = ClinicalTrialsManagementService()
    handler = getattr(service, route["handler"])
    result = handler(payload or {})
    return {"ok": result.get("ok") is True, "handled": True, "route": route, "result": result, "side_effects": ()}


def smoke_test() -> dict:
    validation = validate_api_route_contracts()
    first = ROUTES[0] if ROUTES else None
    dispatched = dispatch_route(first["method"], first["path"], {"smoke": True}) if first else {"ok": False}
    return {"ok": validation["ok"] and dispatched["ok"], "validation": validation, "dispatch": dispatched, "side_effects": ()}
