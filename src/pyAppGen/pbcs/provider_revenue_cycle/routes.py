"""API route contracts for provider_revenue_cycle."""

from __future__ import annotations

from .services import ProviderRevenueCycleService
from .services import ProviderRevenueCycleStandaloneService
from .services import service_operation_contracts

ROUTES = tuple(
    {
        "method": item["method"],
        "path": item["path"],
        "handler": item["operation"],
        "permission": item["permission"],
    }
    for item in service_operation_contracts()["contracts"]
)

API_ROUTE_CONTRACTS = tuple(
    {
        "method": item["method"],
        "path": item["path"],
        "handler": item["operation"],
        "permission": item["permission"],
        "operation": item["operation"],
        "service_method": item["service_method"],
        "operation_kind": item["operation_kind"],
        "owned_tables": item["owned_tables"],
        "read_tables": item["read_tables"],
        "emitted_event": item["emitted_event"],
        "event_contract": "AppGen-X",
        "transaction_boundary": item["transaction_boundary"],
        "idempotency_required": item["operation_kind"] == "command",
        "idempotency_key": f"provider_revenue_cycle:{item['operation']}:idempotency_key" if item["operation_kind"] == "command" else None,
        "shared_table_access": False,
        "stream_engine_picker_visible": False,
        "service_operation": item,
        "route_id": f"{item['method']} {item['path']}",
    }
    for item in service_operation_contracts()["contracts"]
)


def register_routes(app=None):
    return ROUTES


def api_route_contracts() -> dict:
    return {
        "ok": bool(API_ROUTE_CONTRACTS)
        and all(item["event_contract"] == "AppGen-X" for item in API_ROUTE_CONTRACTS)
        and all(item["stream_engine_picker_visible"] is False for item in API_ROUTE_CONTRACTS)
        and all(item["shared_table_access"] is False for item in API_ROUTE_CONTRACTS),
        "pbc": "provider_revenue_cycle",
        "contracts": API_ROUTE_CONTRACTS,
        "routes": tuple(item["route_id"] for item in API_ROUTE_CONTRACTS),
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
        if not table.startswith("provider_revenue_cycle_")
    )
    return {
        "ok": manifest["ok"] and not service_mismatches and not missing_idempotency and not invalid_table_scope,
        "pbc": "provider_revenue_cycle",
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
    service = ProviderRevenueCycleService()
    handler = getattr(service, route["handler"])
    result = handler(payload or {})
    return {"ok": result.get("ok") is True, "handled": True, "route": route, "result": result, "side_effects": ()}


def dispatch_standalone_route(service: ProviderRevenueCycleStandaloneService, method: str, path: str, payload: dict | None = None) -> dict:
    route = next((item for item in API_ROUTE_CONTRACTS if item["method"] == method and item["path"] == path), None)
    if route is None:
        return {"ok": False, "handled": False, "reason": "route_not_found"}
    handler = getattr(service, route["service_method"])
    data = dict(payload or {})
    service_method = route["service_method"]
    if service_method in {"intake_patient_account", "upsert_payer_contract", "assistant_preview"}:
        result = handler(data)
    elif service_method in {"review_eligibility_and_benefits", "link_prior_authorization", "capture_charge", "review_coding", "generate_patient_statement", "enroll_payment_plan", "issue_refund_or_credit", "evaluate_financial_assistance", "reconcile_close"}:
        result = handler(data["account_id"], data)
    elif service_method in {"create_claim"}:
        result = handler(data["account_id"])
    elif service_method in {"scrub_claim", "submit_claim", "detect_underpayment", "account_snapshot"}:
        result = handler(data["claim_id"] if "claim_id" in data else data["account_id"])
    elif service_method in {"post_remittance_era", "open_denial_case"}:
        result = handler(data["claim_id"], data)
    elif service_method in {"appeal_denial"}:
        result = handler(data["denial_case_id"], data)
    elif service_method in {"build_ar_workqueue", "control_center"}:
        result = handler(data.get("tenant"))
    else:
        result = handler(**data)
    return {"ok": result.get("ok") is True, "handled": True, "route": route, "result": result, "side_effects": ()}


def smoke_test() -> dict:
    validation = validate_api_route_contracts()
    first = ROUTES[0] if ROUTES else None
    dispatched = dispatch_route(first["method"], first["path"], {"smoke": True}) if first else {"ok": False}
    service = ProviderRevenueCycleStandaloneService(tenant="tenant_alpha")
    service.configure()
    service.register_defaults()
    executed = dispatch_standalone_route(
        service,
        "POST",
        "/patient-accounts",
        {
            "tenant": "tenant_alpha",
            "account_id": "acct_300",
            "patient_id": "patient_300",
            "encounter_id": "enc_300",
            "registration_status": "ready",
            "coverage_priority": "primary",
            "financial_class": "commercial",
            "guarantor": {"name": "Ada"},
        },
    )
    return {
        "ok": validation["ok"] and dispatched["ok"] and executed["ok"],
        "validation": validation,
        "dispatch": dispatched,
        "standalone": executed,
        "side_effects": (),
    }
