"""Route contracts and dispatch for the cybersecurity_operations_center PBC."""

from __future__ import annotations

from typing import Any

from .services import CybersecurityOperationsCenterService, service_operation_contract

PBC_KEY = "cybersecurity_operations_center"
ROUTE_TO_OPERATION = {
    "POST /security-alerts": "command_security_alert",
    "POST /security-alerts/triage": "transition_alert",
    "POST /security-alerts/enrich": "enrich_security_alert",
    "POST /security-alerts/suppress": "suppress_security_alert",
    "POST /security-incidents": "record_security_incident",
    "POST /security-incidents/promote": "record_security_incident",
    "POST /asset-exposures": "review_asset_exposure",
    "POST /threat-intels": "approve_threat_intel",
    "POST /playbook-runs": "simulate_playbook_run",
    "POST /containment-actions": "create_containment_action",
    "POST /response-evidence": "record_response_evidence",
    "GET /cybersecurity-operations-center-workbench": "query_workbench",
    "GET /cybersecurity-operations-center/case-detail": "build_case_detail",
}
ROUTE_PERMISSIONS = {
    "POST /security-alerts": f"{PBC_KEY}.create",
    "POST /security-alerts/triage": f"{PBC_KEY}.update",
    "POST /security-alerts/enrich": f"{PBC_KEY}.update",
    "POST /security-alerts/suppress": f"{PBC_KEY}.approve",
    "POST /security-incidents": f"{PBC_KEY}.create",
    "POST /security-incidents/promote": f"{PBC_KEY}.create",
    "POST /asset-exposures": f"{PBC_KEY}.create",
    "POST /threat-intels": f"{PBC_KEY}.approve",
    "POST /playbook-runs": f"{PBC_KEY}.update",
    "POST /containment-actions": f"{PBC_KEY}.approve",
    "POST /response-evidence": f"{PBC_KEY}.update",
    "GET /cybersecurity-operations-center-workbench": f"{PBC_KEY}.read",
    "GET /cybersecurity-operations-center/case-detail": f"{PBC_KEY}.read",
}
ROUTES = tuple(ROUTE_TO_OPERATION)


def _route_contract(route: str, operation: str) -> dict[str, Any]:
    return {
        "route": route,
        "method": route.split()[0],
        "path": route.split()[1],
        "pbc": PBC_KEY,
        "operation": operation,
        "idempotency_key": f"{PBC_KEY}:{route}",
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "required_permission": ROUTE_PERMISSIONS[route],
    }


def api_route_contracts() -> dict[str, Any]:
    contracts = tuple(_route_contract(route, operation) for route, operation in ROUTE_TO_OPERATION.items())
    return {"ok": True, "pbc": PBC_KEY, "contracts": contracts, "routes": ROUTES, "side_effects": ()}


def validate_api_route_contracts() -> dict[str, Any]:
    contracts = api_route_contracts()["contracts"]
    missing_ops = tuple(contract["route"] for contract in contracts if not contract["operation"])
    missing_idempotency = tuple(contract for contract in contracts if not contract["idempotency_key"])
    missing_permissions = tuple(contract["route"] for contract in contracts if not contract["required_permission"])
    return {
        "ok": not missing_ops and not missing_idempotency and not missing_permissions,
        "pbc": PBC_KEY,
        "service_mismatches": missing_ops,
        "missing_idempotency": missing_idempotency,
        "missing_permissions": missing_permissions,
        "invalid_table_scope": (),
        "side_effects": (),
    }


def dispatch_route(
    route: str,
    payload: dict[str, Any] | None = None,
    service: CybersecurityOperationsCenterService | None = None,
) -> dict[str, Any]:
    payload = dict(payload or {})
    operation = ROUTE_TO_OPERATION.get(route)
    if not operation:
        return {"ok": False, "route": route, "payload": payload, "reason": "unknown_route", "side_effects": ()}
    local_service = service or CybersecurityOperationsCenterService()
    if route == "POST /security-alerts/triage":
        result = getattr(local_service, operation)(
            payload["alert_id"],
            payload.get("next_status", "triaged"),
            payload.get("actor", "analyst"),
            payload.get("reason", "triage"),
        )
    elif route == "POST /security-alerts/enrich":
        result = getattr(local_service, operation)(
            payload["alert_id"],
            payload.get("enrichment", {}),
            payload.get("actor", "analyst"),
        )
    elif route == "POST /security-alerts/suppress":
        result = getattr(local_service, operation)(
            payload["alert_id"],
            payload.get("suppression", {}),
            payload.get("actor", "analyst"),
        )
    elif route == "GET /cybersecurity-operations-center/case-detail":
        result = getattr(local_service, operation)(payload["case_id"])
    else:
        result = getattr(local_service, operation)(payload)
    return {
        "ok": result["ok"],
        "route": route,
        "payload": payload,
        "required_permission": ROUTE_PERMISSIONS[route],
        "operation_contract": service_operation_contract(operation),
        "result": result,
        "side_effects": (),
    }


def smoke_test() -> dict[str, Any]:
    service = CybersecurityOperationsCenterService()
    created = dispatch_route(
        "POST /security-alerts",
        {
            "tenant": "tenant-smoke",
            "severity": "medium",
            "asset_ref": "srv-route",
            "principal_ref": "route-user",
            "indicator_value": "203.0.113.10",
            "detection_context": {
                "source_event_id": "evt-route",
                "detection_timestamp": "2026-05-29T00:00:00+00:00",
                "detection_rule_id": "sigma-route",
                "evidence_checksum": "sha256:route",
            },
        },
        service=service,
    )
    workbench = dispatch_route("GET /cybersecurity-operations-center-workbench", {"tenant": "tenant-smoke"}, service=service)
    return {
        "ok": api_route_contracts()["ok"] and validate_api_route_contracts()["ok"] and created["ok"] and workbench["ok"],
        "side_effects": (),
    }
