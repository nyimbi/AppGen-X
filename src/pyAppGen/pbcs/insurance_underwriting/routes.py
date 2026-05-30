"""Route contracts for insurance underwriting."""

from __future__ import annotations

from .services import (
    InsuranceUnderwritingService,
    InsuranceUnderwritingStandaloneService,
    service_operation_contracts,
    standalone_service_operation_contracts,
)


ROUTES = (
    {"method": "POST", "path": "/underwriting-submissions", "handler": "command_underwriting_submission", "permission": "insurance_underwriting.submission.write"},
    {"method": "POST", "path": "/risk-profiles", "handler": "command_risk_profile", "permission": "insurance_underwriting.submission.write"},
    {"method": "POST", "path": "/rating-factors", "handler": "command_rating_factor", "permission": "insurance_underwriting.quote.write"},
    {"method": "POST", "path": "/quotes", "handler": "command_quote", "permission": "insurance_underwriting.quote.write"},
    {"method": "POST", "path": "/underwriting-decisions", "handler": "command_underwriting_decision", "permission": "insurance_underwriting.decision.approve"},
    {"method": "GET", "path": "/insurance-underwriting-workbench", "handler": "query_workbench", "permission": "insurance_underwriting.read"},
)


def register_routes(app=None):
    return ROUTES


def api_route_contracts() -> dict:
    service_contract_index = {
        item["operation"]: item for item in service_operation_contracts()["contracts"]
    }
    route_to_operation = {
        "/underwriting-submissions": "command_underwriting_submission",
        "/risk-profiles": "command_risk_profile",
        "/rating-factors": "command_rating_factor",
        "/quotes": "command_quote",
        "/underwriting-decisions": "command_underwriting_decision",
        "/insurance-underwriting-workbench": "query_workbench",
    }
    contracts = tuple(
        {
            "route_id": f"{route['method']} {route['path']}",
            **route,
            "operation": route_to_operation[route["path"]],
            "service_operation": service_contract_index[route_to_operation[route["path"]]],
            "idempotency_required": route["method"] == "POST",
            "idempotency_key": f"insurance_underwriting:{route_to_operation[route['path']]}:idempotency_key" if route["method"] == "POST" else None,
            "shared_table_access": False,
            "stream_engine_picker_visible": False,
        }
        for route in ROUTES
    )
    return {
        "ok": bool(contracts),
        "pbc": "insurance_underwriting",
        "contracts": contracts,
        "routes": tuple(item["route_id"] for item in contracts),
        "side_effects": (),
    }


def validate_api_route_contracts() -> dict:
    manifest = api_route_contracts()
    service_mismatches = tuple(
        item["route_id"]
        for item in manifest["contracts"]
        if item["service_operation"]["method"] != item["method"]
        or item["service_operation"]["path"] != item["path"]
        or item["service_operation"]["permission"] != item["permission"]
    )
    missing_idempotency = tuple(
        item["route_id"]
        for item in manifest["contracts"]
        if item["idempotency_required"] and not item["idempotency_key"]
    )
    invalid_table_scope = tuple(
        item["route_id"]
        for item in manifest["contracts"]
        for table in item["service_operation"]["owned_tables"] + item["service_operation"]["read_tables"]
        if not table.startswith("insurance_underwriting_")
    )
    return {
        "ok": manifest["ok"] and not service_mismatches and not missing_idempotency and not invalid_table_scope,
        "pbc": "insurance_underwriting",
        "contracts": manifest["contracts"],
        "service_mismatches": service_mismatches,
        "missing_idempotency": missing_idempotency,
        "invalid_table_scope": invalid_table_scope,
        "side_effects": (),
    }


def dispatch_route(method: str, path: str, payload: dict | None = None) -> dict:
    route = next(
        (item for item in ROUTES if item["method"] == method and item["path"] == path),
        None,
    )
    if route is None:
        return {"ok": False, "handled": False, "reason": "route_not_found", "side_effects": ()}
    service = InsuranceUnderwritingService()
    result = getattr(service, route["handler"])(payload or {})
    return {"ok": result["ok"], "handled": True, "route": route, "result": result, "side_effects": ()}


def standalone_route_contracts() -> dict:
    contracts = tuple(
        {
            "route_id": f"{item['method']} {item['path']}",
            **item,
        }
        for item in standalone_service_operation_contracts()["contracts"]
    )
    return {
        "format": "appgen.insurance-underwriting-standalone-route-contract.v1",
        "ok": True,
        "pbc": "insurance_underwriting",
        "contracts": contracts,
        "routes": tuple(item["route_id"] for item in contracts),
        "side_effects": (),
    }


def dispatch_standalone_route(
    method: str,
    path: str,
    payload: dict | None = None,
    *,
    service: InsuranceUnderwritingStandaloneService | None = None,
) -> dict:
    manifest = standalone_route_contracts()
    route = next(
        (item for item in manifest["contracts"] if item["method"] == method and item["path"] == path),
        None,
    )
    if route is None:
        return {"ok": False, "handled": False, "reason": "route_not_found", "side_effects": ()}
    local_service = service or InsuranceUnderwritingStandaloneService()
    try:
        result = getattr(local_service, route["handler"])(payload or {})
        return {"ok": result.get("ok") is True, "handled": True, "route": route, "result": result, "side_effects": ()}
    finally:
        if service is None:
            local_service.close()


def smoke_test() -> dict:
    validation = validate_api_route_contracts()
    standard = dispatch_route("POST", "/underwriting-submissions", {"tenant": "tenant-smoke"})
    standalone = InsuranceUnderwritingStandaloneService()
    try:
        live = dispatch_standalone_route(
            "POST",
            "/app/insurance-underwriting/workflows/intake",
            {
                "submission_id": "route-smoke",
                "tenant": "tenant-smoke",
                "product_line": "property",
                "applicant_name": "Route Smoke",
                "jurisdiction": "US-TX",
                "requested_limit": 600000.0,
                "declared_revenue": 1200000.0,
                "effective_date": "2026-06-01",
                "exposure_locations": ("Houston",),
                "documents": ("app.pdf",),
                "prior_losses": (),
            },
            service=standalone,
        )
        workbench = dispatch_standalone_route(
            "GET",
            "/app/insurance-underwriting/workbench",
            {"tenant": "tenant-smoke"},
            service=standalone,
        )
        return {
            "ok": validation["ok"] and standard["ok"] and live["ok"] and workbench["ok"],
            "validation": validation,
            "standard": standard,
            "live": live,
            "workbench": workbench,
            "side_effects": (),
        }
    finally:
        standalone.close()
