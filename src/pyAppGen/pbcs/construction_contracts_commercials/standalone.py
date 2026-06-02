"""Standalone one-PBC app composition for the construction_contracts_commercials package."""

from __future__ import annotations

from .agent import standalone_agent_workspace_contract
from .models import ConstructionContractsCommercialsStandaloneStore
from .models import standalone_model_contract, standalone_store_smoke_test
from .routes import dispatch_standalone_route, standalone_route_contracts
from .services import ConstructionContractsCommercialsStandaloneService, standalone_service_operation_contracts
from .ui import construction_contracts_commercials_render_standalone_workbench
from .ui import construction_contracts_commercials_standalone_workbench_blueprint


def construction_contracts_commercials_standalone_app_contract() -> dict:
    """Return the composed standalone-app surface for this one-PBC package."""
    models = standalone_model_contract()
    services = standalone_service_operation_contracts()
    routes = standalone_route_contracts()
    ui = construction_contracts_commercials_standalone_workbench_blueprint()
    agent = standalone_agent_workspace_contract()
    return {
        "format": "appgen.construction-contracts-commercials-standalone-app.v1",
        "ok": all(item.get("ok") is True for item in (models, services, routes, ui, agent)),
        "pbc": "construction_contracts_commercials",
        "models": models,
        "services": services,
        "routes": routes,
        "ui": ui,
        "agent": agent,
        "side_effects": (),
    }


def construction_contracts_commercials_bootstrap_standalone_app() -> dict:
    """Create a live standalone store and service pair for local package use."""
    store = ConstructionContractsCommercialsStandaloneStore()
    service = ConstructionContractsCommercialsStandaloneService(store)
    return {
        "ok": True,
        "pbc": "construction_contracts_commercials",
        "store": store,
        "service": service,
        "contract": construction_contracts_commercials_standalone_app_contract(),
        "side_effects": (),
    }


def construction_contracts_commercials_standalone_app_smoke() -> dict:
    """Exercise the standalone app through its route surface."""
    bundle = construction_contracts_commercials_bootstrap_standalone_app()
    service = bundle["service"]
    try:
        create = dispatch_standalone_route(
            "POST",
            "/app/construction-contracts-commercials/contracts",
            {
                "tenant": "tenant-standalone",
                "contract_code": "CCC-APP-001",
                "title": "Standalone Commercial Hub",
                "contract_value": 150000.0,
                "pricing_basis": "lump_sum",
                "jurisdiction": "KE",
                "schedule_of_values": (
                    {"line_code": "SOV-01", "work_package": "Concrete", "original_value": 80000.0},
                    {"line_code": "SOV-02", "work_package": "Steel", "original_value": 70000.0},
                ),
            },
            service=service,
        )
        pay_application = dispatch_standalone_route(
            "POST",
            "/app/construction-contracts-commercials/pay-applications",
            {
                "contract_code": "CCC-APP-001",
                "application_number": "APP-APP-001",
                "period_start": "2026-05-01",
                "period_end": "2026-05-30",
                "attachments": ("payapp.pdf", "inspection.zip"),
                "lines": (
                    {"line_code": "SOV-01", "current_claimed": 35000.0, "evidence_refs": ("inspection-001",)},
                ),
            },
            service=service,
        )
        waiver = dispatch_standalone_route(
            "POST",
            "/app/construction-contracts-commercials/lien-waivers",
            {
                "contract_code": "CCC-APP-001",
                "pay_application_id": pay_application["result"]["record"]["id"],
                "waiver_number": "LW-APP-001",
                "covered_amount": 35000.0,
                "signed_date": "2026-05-30",
            },
            service=service,
        )
        certified = dispatch_standalone_route(
            "POST",
            "/app/construction-contracts-commercials/pay-applications/certify",
            {"pay_application_id": pay_application["result"]["record"]["id"]},
            service=service,
        )
        workbench = dispatch_standalone_route(
            "GET",
            "/app/construction-contracts-commercials/workbench",
            {"tenant": "tenant-standalone"},
            service=service,
        )
        rendered = construction_contracts_commercials_render_standalone_workbench(workbench["result"]["result"])
        return {
            "ok": bundle["contract"]["ok"]
            and standalone_store_smoke_test()["ok"]
            and create["ok"]
            and pay_application["ok"]
            and waiver["ok"]
            and certified["ok"]
            and workbench["ok"]
            and rendered["ok"],
            "contract": bundle["contract"],
            "create": create,
            "pay_application": pay_application,
            "waiver": waiver,
            "certified": certified,
            "workbench": workbench,
            "rendered": rendered,
            "side_effects": (),
        }
    finally:
        service.close()
