"""Standalone one-PBC app composition for the customer_360 package."""

from __future__ import annotations

from .agent import standalone_agent_workspace_contract
from .models import Customer360StandaloneStore
from .models import standalone_model_contract, standalone_store_smoke_test
from .routes import dispatch_standalone_route, standalone_route_contracts
from .services import Customer360StandaloneService, standalone_service_operation_contracts
from .ui import customer_360_render_standalone_workbench
from .ui import customer_360_standalone_workbench_blueprint


def customer_360_standalone_app_contract() -> dict:
    """Return the composed standalone-app surface for this one-PBC package."""
    models = standalone_model_contract()
    services = standalone_service_operation_contracts()
    routes = standalone_route_contracts()
    ui = customer_360_standalone_workbench_blueprint()
    agent = standalone_agent_workspace_contract()
    return {
        "format": "appgen.customer-360-standalone-app.v1",
        "ok": all(
            item.get("ok") is True
            for item in (models, services, routes, ui, agent)
        ),
        "pbc": "customer_360",
        "models": models,
        "services": services,
        "routes": routes,
        "ui": ui,
        "agent": agent,
        "side_effects": (),
    }


def customer_360_bootstrap_standalone_app(database_path: str = ":memory:") -> dict:
    """Create a live standalone store and service pair for local package use."""
    store = Customer360StandaloneStore(database_path=database_path)
    service = Customer360StandaloneService(store)
    return {
        "ok": True,
        "pbc": "customer_360",
        "store": store,
        "service": service,
        "contract": customer_360_standalone_app_contract(),
        "side_effects": (),
    }


def customer_360_standalone_app_smoke() -> dict:
    """Exercise the standalone app through its route surface."""
    bundle = customer_360_bootstrap_standalone_app()
    store = bundle["store"]
    service = bundle["service"]
    try:
        create = dispatch_standalone_route(
            "POST",
            "/app/customer-360/profiles",
            {
                "profile_id": "cust_standalone",
                "tenant": "tenant_standalone",
                "display_name": "Standalone Customer",
                "region": "US",
            },
            service=service,
        )
        identity = dispatch_standalone_route(
            "POST",
            "/app/customer-360/identities",
            {
                "identity_id": "id_standalone",
                "tenant": "tenant_standalone",
                "profile_id": "cust_standalone",
                "identity_type": "email",
                "value": "standalone@example.com",
                "confidence": 0.98,
                "verified": True,
            },
            service=service,
        )
        preference = dispatch_standalone_route(
            "POST",
            "/app/customer-360/preferences",
            {
                "preference_id": "pref_standalone",
                "tenant": "tenant_standalone",
                "profile_id": "cust_standalone",
                "channel": "email",
                "topic": "offers",
                "status": "opt_in",
            },
            service=service,
        )
        workbench = dispatch_standalone_route(
            "GET",
            "/app/customer-360/workbench",
            {"tenant": "tenant_standalone"},
            service=service,
        )
        rendered = customer_360_render_standalone_workbench(workbench["result"]["result"])
        timeline = dispatch_standalone_route(
            "GET",
            "/app/customer-360/timeline",
            {"profile_id": "cust_standalone"},
            service=service,
        )
        return {
            "ok": bundle["contract"]["ok"]
            and standalone_store_smoke_test()["ok"]
            and create["ok"]
            and identity["ok"]
            and preference["ok"]
            and workbench["ok"]
            and rendered["ok"]
            and timeline["ok"],
            "contract": bundle["contract"],
            "create": create,
            "identity": identity,
            "preference": preference,
            "workbench": workbench,
            "rendered": rendered,
            "timeline": timeline,
            "side_effects": (),
        }
    finally:
        service.close()
