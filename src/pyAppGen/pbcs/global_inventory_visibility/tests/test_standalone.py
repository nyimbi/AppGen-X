"""Focused standalone one-PBC tests for global_inventory_visibility."""

from pathlib import Path

from .. import agent, release_evidence, routes, services, standalone, ui
from ..repository import GlobalInventoryVisibilityRepository


def test_repository_persists_seeded_inventory_workspace():
    repository = GlobalInventoryVisibilityRepository()
    try:
        seeded = repository.seed_demo_workspace()
        workbench = repository.build_workbench("tenant_demo")
        primary_pool = repository.build_pool_read_model(pool_id="pool_global_primary", tenant="tenant_demo")
        aggregate = repository.get_global_availability(tenant="tenant_demo", item_id="sku_100")
        release = repository.build_release_read_model("tenant_demo")
        proof = repository.generate_pool_proof(
            pool_id="pool_global_primary",
            disclosure=("available_to_promise", "capable_to_promise", "freshness_score"),
        )
        assert seeded["ok"] is True
        assert workbench["ok"] is True
        assert primary_pool["ok"] is True
        assert aggregate["ok"] is True
        assert release["ok"] is True
        assert proof["ok"] is True
        assert workbench["pool_count"] == 2
        assert workbench["node_count"] == 3
        assert workbench["available_to_promise"] > 0
        assert primary_pool["latest_projection"]["available_to_promise"] > 0
        assert len(release["assertions"]) >= 4
    finally:
        repository.close()


def test_standalone_service_routes_ui_agent_and_release_surface():
    service = services.GlobalInventoryVisibilityStandaloneService()
    try:
        seeded = routes.dispatch_standalone_route(
            "POST",
            "/app/global-inventory-visibility/demo-workspace",
            {"tenant": "tenant_route_test"},
            service=service,
        )
        workbench = routes.dispatch_standalone_route(
            "GET",
            "/app/global-inventory-visibility/workbench",
            {"tenant": "tenant_route_test"},
            service=service,
        )
        pool_detail = routes.dispatch_standalone_route(
            "GET",
            "/app/global-inventory-visibility/pools/detail",
            {"tenant": "tenant_route_test", "pool_id": "pool_global_primary"},
            service=service,
        )
        rendered = ui.global_inventory_visibility_render_standalone_workbench(workbench["result"]["result"])
        document_plan = agent.document_instruction_plan(
            "carrier ASN and warehouse handoff",
            "bootstrap the standalone inventory workspace and capture a reservation",
        )
        crud_plan = agent.datastore_crud_plan(
            "create",
            "global_inventory_visibility_inventory_pool",
            {"pool_id": "pool_global_primary"},
        )
        app_contract = standalone.global_inventory_visibility_standalone_app_contract()
        smoke = standalone.global_inventory_visibility_standalone_app_smoke()
        evidence = release_evidence.build_release_evidence()
        assert seeded["ok"] is True
        assert workbench["ok"] is True
        assert pool_detail["ok"] is True
        assert rendered["ok"] is True
        assert app_contract["ok"] is True
        assert smoke["ok"] is True
        assert document_plan["wizard_candidates"]
        assert crud_plan["route_candidates"]
        assert evidence["documentation"]["ok"] is True
        assert evidence["standalone_app"]["ok"] is True
        assert evidence["standalone_repository"]["ok"] is True
    finally:
        service.close()


def test_package_local_docs_exist_for_release_evidence():
    base = Path(__file__).resolve().parent.parent
    for name in ("README.md", "RELEASE_EVIDENCE.md", "repository.py", "standalone.py"):
        assert (base / name).exists() is True
