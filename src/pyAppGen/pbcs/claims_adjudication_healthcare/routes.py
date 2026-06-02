"""API route contracts and dispatchers for the executable adjudication slice."""

from __future__ import annotations

from typing import Any

from .services import ClaimsAdjudicationHealthcareService
from .services import service_operation_contracts
from .standalone import standalone_route_contracts

PBC_KEY = "claims_adjudication_healthcare"

ROUTE_TO_OPERATION = {
    "POST /health-claims": "command_health_claim",
    "POST /claim-lines": "record_claim_line",
    "POST /coding-reviews": "review_coding_review",
    "POST /benefit-rules": "approve_benefit_rule",
    "POST /denials": "simulate_denial",
    "POST /appeals": "create_appeal",
    "POST /document-instructions": "create_document_instruction",
    "GET /claims-adjudication-healthcare-workbench": "query_workbench",
}

ROUTES = tuple(ROUTE_TO_OPERATION.keys())


def api_route_contracts() -> dict[str, Any]:
    contracts = tuple(
        {
            "route": route,
            "method": route.split()[0],
            "path": route.split()[1],
            "pbc": PBC_KEY,
            "operation": operation,
            "idempotency_key": f"{PBC_KEY}:{route}",
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
            "shared_table_access": False,
            "required_permission": f"{PBC_KEY}.read" if operation == "query_workbench" else f"{PBC_KEY}.update",
        }
        for route, operation in ROUTE_TO_OPERATION.items()
    )
    standalone = standalone_route_contracts()
    return {
        "ok": True and standalone["ok"],
        "pbc": PBC_KEY,
        "contracts": contracts,
        "routes": ROUTES + standalone["routes"],
        "standalone_routes": standalone,
        "side_effects": (),
    }


def validate_api_route_contracts() -> dict[str, Any]:
    service_ops = {contract["operation"] for contract in service_operation_contracts()["contracts"]}
    contracts = api_route_contracts()["contracts"]
    service_mismatches = tuple(contract["route"] for contract in contracts if contract["operation"] not in service_ops)
    missing_idempotency = tuple(contract["route"] for contract in contracts if not contract["idempotency_key"])
    return {
        "ok": not service_mismatches and not missing_idempotency,
        "pbc": PBC_KEY,
        "service_mismatches": service_mismatches,
        "missing_idempotency": missing_idempotency,
        "invalid_table_scope": (),
        "side_effects": (),
    }


def dispatch_route(
    route: str,
    payload: dict[str, Any] | None = None,
    *,
    service: ClaimsAdjudicationHealthcareService | None = None,
) -> dict[str, Any]:
    payload = dict(payload or {})
    operation = ROUTE_TO_OPERATION.get(route)
    if operation is None:
        return {"ok": False, "reason": "unknown_route", "route": route, "side_effects": ()}
    active_service = service or ClaimsAdjudicationHealthcareService()
    result = getattr(active_service, operation)(payload)
    return {
        "ok": result["ok"],
        "route": route,
        "operation": operation,
        "payload": payload,
        "result": result,
        "operation_contract": result["operation_contract"],
        "side_effects": (),
    }


def smoke_test() -> dict[str, Any]:
    service = ClaimsAdjudicationHealthcareService()
    service.approve_benefit_rule(
        {
            "plan_id": "plan-a",
            "service_code": "99213",
            "description": "Office visit",
            "effective_from": "2026-01-01",
            "effective_to": "2026-12-31",
        }
    )
    create = dispatch_route(
        "POST /health-claims",
        {
            "claim_number": "ROUTE-1",
            "member_id": "M-1",
            "provider_id": "P-1",
            "plan_id": "plan-a",
            "received_date": "2026-05-29",
        },
        service=service,
    )
    query = dispatch_route("GET /claims-adjudication-healthcare-workbench", {"tenant": "default"}, service=service)
    return {
        "ok": api_route_contracts()["ok"] and validate_api_route_contracts()["ok"] and create["ok"] and query["ok"] and "GET /claims-adjudication-healthcare/app" in api_route_contracts()["routes"],
        "side_effects": (),
    }
