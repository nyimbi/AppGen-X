"""Standalone one-PBC application surface for global_inventory_visibility."""

from __future__ import annotations

from .agent import standalone_agent_workspace_contract
from .repository import GlobalInventoryVisibilityRepository
from .repository import standalone_repository_contract
from .repository import standalone_repository_smoke_test
from .routes import dispatch_standalone_route
from .routes import standalone_route_contracts
from .services import GlobalInventoryVisibilityStandaloneService
from .services import standalone_service_operation_contracts
from .ui import global_inventory_visibility_render_standalone_workbench
from .ui import global_inventory_visibility_standalone_workbench_blueprint


def global_inventory_visibility_standalone_app_contract() -> dict:
    """Return the composed standalone-app surface for this package."""
    repository = standalone_repository_contract()
    services = standalone_service_operation_contracts()
    routes = standalone_route_contracts()
    ui = global_inventory_visibility_standalone_workbench_blueprint()
    agent = standalone_agent_workspace_contract()
    return {
        "format": "appgen.global-inventory-visibility-standalone-app.v1",
        "ok": all(item.get("ok") is True for item in (repository, services, routes, ui, agent)),
        "pbc": "global_inventory_visibility",
        "repository": repository,
        "services": services,
        "routes": routes,
        "ui": ui,
        "agent": agent,
        "side_effects": (),
    }


def global_inventory_visibility_bootstrap_standalone_app(
    database_path: str = ":memory:",
    *,
    tenant: str = "tenant_demo",
    seed_demo: bool = True,
) -> dict:
    """Create a live standalone repository and service pair for local package use."""
    repository = GlobalInventoryVisibilityRepository(database_path=database_path)
    service = GlobalInventoryVisibilityStandaloneService(repository)
    seeded = repository.seed_demo_workspace(tenant=tenant) if seed_demo else {"ok": True, "tenant": tenant}
    return {
        "ok": seeded["ok"],
        "pbc": "global_inventory_visibility",
        "repository": repository,
        "service": service,
        "seeded": seeded,
        "contract": global_inventory_visibility_standalone_app_contract(),
        "side_effects": (),
    }


def global_inventory_visibility_standalone_app_smoke() -> dict:
    """Exercise the standalone app through its route surface."""
    bundle = global_inventory_visibility_bootstrap_standalone_app(seed_demo=False)
    service = bundle["service"]
    try:
        seed_route = dispatch_standalone_route(
            "POST",
            "/app/global-inventory-visibility/demo-workspace",
            {"tenant": "tenant_demo"},
            service=service,
        )
        workbench = dispatch_standalone_route(
            "GET",
            "/app/global-inventory-visibility/workbench",
            {"tenant": "tenant_demo"},
            service=service,
        )
        pool_detail = dispatch_standalone_route(
            "GET",
            "/app/global-inventory-visibility/pools/detail",
            {"tenant": "tenant_demo", "pool_id": "pool_global_primary"},
            service=service,
        )
        proof = dispatch_standalone_route(
            "POST",
            "/app/global-inventory-visibility/proofs",
            {
                "pool_id": "pool_global_primary",
                "disclosure": ("available_to_promise", "capable_to_promise", "freshness_score"),
            },
            service=service,
        )
        rendered = global_inventory_visibility_render_standalone_workbench(workbench["result"]["result"])
        release = dispatch_standalone_route(
            "GET",
            "/app/global-inventory-visibility/release-evidence",
            {"tenant": "tenant_demo"},
            service=service,
        )
        return {
            "ok": bundle["contract"]["ok"]
            and seed_route["ok"]
            and workbench["ok"]
            and pool_detail["ok"]
            and proof["ok"]
            and rendered["ok"]
            and release["ok"]
            and standalone_repository_smoke_test()["ok"],
            "contract": bundle["contract"],
            "seed_route": seed_route,
            "workbench": workbench,
            "pool_detail": pool_detail,
            "proof": proof,
            "rendered": rendered,
            "release": release,
            "side_effects": (),
        }
    finally:
        service.close()
