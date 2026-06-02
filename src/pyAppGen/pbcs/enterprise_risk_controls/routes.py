"""API route contracts for the enterprise_risk_controls PBC."""

from __future__ import annotations

from .services import EnterpriseRiskControlsService
from .services import service_operation_contracts

ROUTES = (
    {"method": "POST", "path": "/api/pbc/enterprise_risk_controls/risks", "handler": "register_risk", "permission": "enterprise_risk_controls.register_risk"},
    {"method": "POST", "path": "/api/pbc/enterprise_risk_controls/risk-assessments", "handler": "assess_inherent_risk", "permission": "enterprise_risk_controls.assess_risk"},
    {"method": "POST", "path": "/api/pbc/enterprise_risk_controls/controls", "handler": "define_control", "permission": "enterprise_risk_controls.manage_controls"},
    {"method": "POST", "path": "/api/pbc/enterprise_risk_controls/control-tests", "handler": "schedule_control_test", "permission": "enterprise_risk_controls.manage_controls"},
    {"method": "POST", "path": "/api/pbc/enterprise_risk_controls/attestations", "handler": "record_attestation", "permission": "enterprise_risk_controls.attest_controls"},
    {"method": "POST", "path": "/api/pbc/enterprise_risk_controls/remediations", "handler": "open_remediation", "permission": "enterprise_risk_controls.manage_remediation"},
    {"method": "POST", "path": "/api/pbc/enterprise_risk_controls/assurance-packets", "handler": "generate_assurance_packet", "permission": "enterprise_risk_controls.compile_assurance"},
    {"method": "GET", "path": "/api/pbc/enterprise_risk_controls/workbench", "handler": "query_enterprise_risk_controls_workbench", "permission": "enterprise_risk_controls.read"},
    {"method": "GET", "path": "/api/pbc/enterprise_risk_controls/controls", "handler": "query_enterprise_risk_controls_controls", "permission": "enterprise_risk_controls.audit"},
    {"method": "POST", "path": "/api/pbc/enterprise_risk_controls/assistant/document-preview", "handler": "query_enterprise_risk_controls_assistant_preview", "permission": "enterprise_risk_controls.audit"},
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
                "transaction_boundary": "owned_datastore_plus_outbox",
                "idempotency_required": service_operation["operation_kind"] == "command",
                "idempotency_key": f"enterprise_risk_controls:{operation}:idempotency_key" if service_operation["operation_kind"] == "command" else None,
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
        and all(item["transaction_boundary"] == "owned_datastore_plus_outbox" for item in contracts)
        and all(item["stream_engine_picker_visible"] is False for item in contracts)
        and all(item["shared_table_access"] is False for item in contracts),
        "pbc": "enterprise_risk_controls",
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
    missing_idempotency = tuple(
        item["route_id"] for item in contracts if item["idempotency_required"] and not item["idempotency_key"]
    )
    invalid_table_scope = tuple(
        item["route_id"]
        for item in contracts
        for table in item["owned_tables"] + item["read_tables"]
        if not table.startswith("enterprise_risk_controls_")
    )
    return {
        "ok": manifest["ok"] and not service_mismatches and not missing_idempotency and not invalid_table_scope,
        "pbc": "enterprise_risk_controls",
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
    service = EnterpriseRiskControlsService()
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
    validation = validate_api_route_contracts()
    first = ROUTES[0] if ROUTES else None
    dispatched = dispatch_route(first["method"], first["path"], {"smoke": True}) if first else {"ok": False}
    return {
        "ok": validation["ok"] and dispatched["ok"],
        "validation": validation,
        "dispatch": dispatched,
        "side_effects": (),
    }
