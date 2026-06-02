"""Standalone one-PBC app composition for insurance underwriting."""

from __future__ import annotations

from .agent import standalone_agent_workspace_contract
from .models import InsuranceUnderwritingStandaloneStore, standalone_model_contract, standalone_store_smoke_test
from .routes import dispatch_standalone_route, standalone_route_contracts
from .services import InsuranceUnderwritingStandaloneService, standalone_service_operation_contracts
from .ui import insurance_underwriting_render_standalone_workbench, insurance_underwriting_standalone_workbench_blueprint


def insurance_underwriting_standalone_app_contract() -> dict:
    models = standalone_model_contract()
    services = standalone_service_operation_contracts()
    routes = standalone_route_contracts()
    ui = insurance_underwriting_standalone_workbench_blueprint()
    agent = standalone_agent_workspace_contract()
    return {
        "format": "appgen.insurance-underwriting-standalone-app.v1",
        "ok": all(item.get("ok") is True for item in (models, services, routes, ui, agent)),
        "pbc": "insurance_underwriting",
        "models": models,
        "services": services,
        "routes": routes,
        "ui": ui,
        "agent": agent,
        "side_effects": (),
    }


def insurance_underwriting_bootstrap_standalone_app(database_path: str = ":memory:") -> dict:
    store = InsuranceUnderwritingStandaloneStore(database_path=database_path)
    service = InsuranceUnderwritingStandaloneService(store)
    return {
        "ok": True,
        "pbc": "insurance_underwriting",
        "store": store,
        "service": service,
        "contract": insurance_underwriting_standalone_app_contract(),
        "side_effects": (),
    }


def insurance_underwriting_standalone_app_smoke() -> dict:
    bundle = insurance_underwriting_bootstrap_standalone_app()
    service = bundle["service"]
    try:
        intake = dispatch_standalone_route(
            "POST",
            "/app/insurance-underwriting/workflows/intake",
            {
                "submission_id": "standalone-submission",
                "tenant": "tenant-standalone",
                "product_line": "property",
                "applicant_name": "Standalone Industries",
                "jurisdiction": "US-FL",
                "requested_limit": 900000.0,
                "declared_revenue": 2500000.0,
                "effective_date": "2026-06-01",
                "exposure_locations": ("Miami",),
                "documents": ("application.pdf",),
                "prior_losses": (),
            },
            service=service,
        )
        quote_to_bind = dispatch_standalone_route(
            "POST",
            "/app/insurance-underwriting/workflows/quote-to-bind",
            {
                "submission_id": "standalone-submission",
                "tenant": "tenant-standalone",
                "authority_level": "chief",
                "approved_by": "chief-underwriter",
            },
            service=service,
        )
        workbench = dispatch_standalone_route(
            "GET",
            "/app/insurance-underwriting/workbench",
            {"tenant": "tenant-standalone"},
            service=service,
        )
        rendered = insurance_underwriting_render_standalone_workbench(workbench["result"]["result"])
        detail = dispatch_standalone_route(
            "GET",
            "/app/insurance-underwriting/submissions/detail",
            {"submission_id": "standalone-submission"},
            service=service,
        )
        timeline = dispatch_standalone_route(
            "GET",
            "/app/insurance-underwriting/timeline",
            {"submission_id": "standalone-submission"},
            service=service,
        )
        return {
            "ok": bundle["contract"]["ok"] and standalone_store_smoke_test()["ok"] and intake["ok"] and quote_to_bind["ok"] and workbench["ok"] and rendered["ok"] and detail["ok"] and timeline["ok"],
            "contract": bundle["contract"],
            "intake": intake,
            "quote_to_bind": quote_to_bind,
            "workbench": workbench,
            "rendered": rendered,
            "detail": detail,
            "timeline": timeline,
            "side_effects": (),
        }
    finally:
        service.close()
