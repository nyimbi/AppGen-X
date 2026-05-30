"""Executable domain behavior tests for the global_inventory_visibility PBC."""

from __future__ import annotations

import pytest

from .. import agent
from .. import release_evidence
from .. import routes
from .. import runtime
from .. import standalone
from .. import ui
from ..repository import GlobalInventoryVisibilityRepository
from ..repository import standalone_repository_contract
from ..repository import standalone_repository_smoke_test
from ..services import GlobalInventoryVisibilityStandaloneService
from ..services import service_operation_manifest
from ..services import standalone_service_operation_contracts


TENANT = "tenant_giv"
POOL_ID = "pool_global_primary"
ITEM_ID = "sku_100"


def _seeded_repository() -> GlobalInventoryVisibilityRepository:
    repository = GlobalInventoryVisibilityRepository()
    seeded = repository.seed_demo_workspace(tenant=TENANT)
    assert seeded["ok"] is True
    return repository


def test_global_inventory_repository_availability_projection_and_release_models_are_executable() -> None:
    repository = _seeded_repository()
    try:
        workbench = repository.build_workbench(TENANT)
        primary_pool = repository.build_pool_read_model(pool_id=POOL_ID, tenant=TENANT)
        aggregate = repository.get_global_availability(tenant=TENANT, item_id=ITEM_ID)
        proof = repository.generate_pool_proof(
            pool_id=POOL_ID,
            disclosure=("available_to_promise", "capable_to_promise", "freshness_score"),
        )
        release = repository.build_release_read_model(TENANT)

        assert workbench["ok"] is True
        assert workbench["pool_count"] == 2
        assert workbench["node_count"] == 3
        assert workbench["available_to_promise"] > 0
        assert workbench["freshness_alert_count"] >= 0
        assert primary_pool["ok"] is True
        assert primary_pool["pool"]["pool_id"] == POOL_ID
        assert primary_pool["latest_projection"]["available_to_promise"] > 0
        assert set(primary_pool["aggregate"]["pools"]) == {POOL_ID}
        assert aggregate["ok"] is True
        assert aggregate["available_to_promise"] == primary_pool["aggregate"]["available_to_promise"]
        assert proof["ok"] is True
        assert proof["proof"].startswith("zk_availability_")
        assert set(proof["disclosure"]) == {"available_to_promise", "capable_to_promise", "freshness_score"}
        assert release["ok"] is True
        assert len(release["assertions"]) >= 4
        assert release["control_tests"]["hash_chain_valid"] is True
    finally:
        repository.close()


def test_global_inventory_routes_agent_ui_standalone_and_release_surfaces_are_executable() -> None:
    route_validation = routes.validate_api_route_contracts()
    query_dispatch = routes.dispatch_route(
        "GET",
        "/api/pbc/global_inventory_visibility/global-availability",
        {"tenant": TENANT, "item_id": ITEM_ID},
    )
    command_dispatch = routes.dispatch_route(
        "POST",
        "/api/pbc/global_inventory_visibility/pool-rules",
        {"tenant": TENANT, "rule_id": "rule-route"},
    )

    assert route_validation["ok"] is True
    assert all(contract["event_contract"] == "AppGen-X" for contract in route_validation["contracts"])
    assert all(contract["stream_engine_picker_visible"] is False for contract in route_validation["contracts"])
    assert all(contract["shared_table_access"] is False for contract in route_validation["contracts"])
    assert query_dispatch["ok"] is True and query_dispatch["result"]["read_only"] is True
    assert command_dispatch["ok"] is True
    assert command_dispatch["result"]["outbox_table"] == "global_inventory_visibility_appgen_outbox_event"

    service = GlobalInventoryVisibilityStandaloneService()
    try:
        seeded = routes.dispatch_standalone_route(
            "POST",
            "/app/global-inventory-visibility/demo-workspace",
            {"tenant": TENANT},
            service=service,
        )
        workbench = routes.dispatch_standalone_route(
            "GET",
            "/app/global-inventory-visibility/workbench",
            {"tenant": TENANT},
            service=service,
        )
        pool_detail = routes.dispatch_standalone_route(
            "GET",
            "/app/global-inventory-visibility/pools/detail",
            {"tenant": TENANT, "pool_id": POOL_ID},
            service=service,
        )
        proof = routes.dispatch_standalone_route(
            "POST",
            "/app/global-inventory-visibility/proofs",
            {"pool_id": POOL_ID, "disclosure": ("available_to_promise", "capable_to_promise")},
            service=service,
        )
        rendered = ui.global_inventory_visibility_render_standalone_workbench(workbench["result"]["result"])

        assert seeded["ok"] is True
        assert workbench["ok"] is True
        assert pool_detail["ok"] is True
        assert proof["ok"] is True
        assert rendered["ok"] is True
        assert "InventoryPoolForm" in rendered["forms"]
        assert "AvailabilityProjectionWizard" in rendered["wizards"]
        assert rendered["cards"]
    finally:
        service.close()

    skills = agent.agent_skill_manifest()
    chatbot = agent.chatbot_interface_contract()
    document_plan = agent.document_instruction_plan(
        "Global ATP file for sku_100 with carrier ASN and WMS receipt evidence.",
        "bootstrap the standalone inventory workspace, refresh projections, and prepare a reservation.",
    )
    create_plan = agent.datastore_crud_plan(
        "create",
        "global_inventory_visibility_inventory_pool",
        {"pool_id": POOL_ID, "item_id": ITEM_ID},
    )
    blocked_plan = agent.datastore_crud_plan("update", "wms_core_bin_location", {})
    contribution = agent.composed_agent_contribution()

    assert skills["ok"] is True
    assert chatbot["ok"] is True
    assert document_plan["ok"] is True
    assert document_plan["wizard_candidates"]
    assert create_plan["ok"] is True and create_plan["requires_confirmation"] is True
    assert create_plan["route_candidates"] == ("POST /app/global-inventory-visibility/pools",)
    assert blocked_plan["ok"] is False
    assert contribution["ok"] is True
    assert "global_inventory_visibility_crud" in contribution["dsl_tools"]

    app_contract = standalone.global_inventory_visibility_standalone_app_contract()
    app_smoke = standalone.global_inventory_visibility_standalone_app_smoke()
    repository_contract = standalone_repository_contract()
    repository_smoke = standalone_repository_smoke_test()
    release_validation = release_evidence.validate_release_evidence()
    release_smoke = release_evidence.smoke_test()

    assert app_contract["ok"] is True
    assert app_smoke["ok"] is True
    assert repository_contract["ok"] is True
    assert repository_contract["deployment_database_backends"] == ("postgresql", "mysql", "mariadb")
    assert repository_smoke["ok"] is True
    assert release_validation["ok"] is True
    assert release_smoke["ok"] is True
    assert release_smoke["evidence"]["standalone_app"]["ok"] is True
    assert service_operation_manifest()["ok"] is True
    assert standalone_service_operation_contracts()["ok"] is True


def test_global_inventory_event_idempotency_dead_letter_boundary_and_advanced_runtime_are_executable() -> None:
    repository = _seeded_repository()
    try:
        first_event = {
            "event_id": "evt_domain_receipt",
            "event_type": "GoodsReceiptPosted",
            "tenant": TENANT,
            "pool_id": POOL_ID,
            "node_id": "node_us_east",
            "quantity": 7.0,
        }
        first = repository.receive_event(first_event)
        duplicate = repository.receive_event(first_event)
        dead_letter = repository.receive_event({**first_event, "event_id": "evt_domain_dead", "retry_count": 9})
        state = repository._load_state()
        projection = repository.build_pool_read_model(pool_id=POOL_ID, tenant=TENANT)["latest_projection"]

        assert first["ok"] is True and first["duplicate"] is False
        assert duplicate["ok"] is True and duplicate["duplicate"] is True
        assert dead_letter["ok"] is False
        assert dead_letter["dead_letter"]["reason"] == "retry_limit_exceeded"

        parsed = runtime.global_inventory_visibility_parse_semantic_query("show sku 100 availability for tenant giv east")
        counterfactual = runtime.global_inventory_visibility_simulate_counterfactual_allocation(
            state,
            pool_id=POOL_ID,
            requested_quantity=5.0,
            proposed_safety_stock_percent=0.2,
        )
        forecast = runtime.global_inventory_visibility_forecast_temporal_availability((80.0, 88.0, 95.0), horizon_days=2)
        risk = runtime.global_inventory_visibility_score_stockout_risk(
            state,
            pool_id=POOL_ID,
            demand_rate=12.0,
            volatility=0.2,
        )
        exception = runtime.global_inventory_visibility_resolve_exception("stockout_risk")
        routed = runtime.global_inventory_visibility_route_projection(
            projection,
            routes=(
                {"route": "direct_api", "available": False, "latency": 1},
                {"route": "appgen_outbox", "available": True, "latency": 3},
            ),
        )
        policy = runtime.global_inventory_visibility_screen_allocation_policy(
            state,
            pool_id=POOL_ID,
            restricted_nodes=("blocked_node",),
        )
        controls = runtime.global_inventory_visibility_run_control_tests(state)
        federation = runtime.global_inventory_visibility_federate_inventory_view(
            state,
            tenant=TENANT,
            item_id=ITEM_ID,
            systems=("wms", "transportation", "orders"),
        )
        identity = runtime.global_inventory_visibility_verify_supply_identity(
            state["supply_nodes"]["node_us_east"]["identity"]
        )
        resilience = runtime.global_inventory_visibility_run_resilience_drill(
            state,
            disruption="projection_route_timeout",
        )
        crypto = runtime.global_inventory_visibility_rotate_crypto_epoch(state, "dilithium3_simulated")
        carbon = runtime.global_inventory_visibility_schedule_carbon_aware_sourcing(tuple(state["supply_nodes"].values()))
        optimized = runtime.global_inventory_visibility_optimize_allocation(
            (
                {"node_id": "node_us_east", "available": 20.0, "health": 0.92, "distance": 3.0, "carbon": 80.0},
                {"node_id": "node_rotterdam_port", "available": 15.0, "health": 0.86, "distance": 8.0, "carbon": 45.0},
            ),
            quantity=10.0,
        )
        allocation = runtime.global_inventory_visibility_allocate_competing_pools(
            (
                {"pool_id": POOL_ID, "bid": 1.2, "priority": 0.9, "capacity": 8.0},
                {"pool_id": "pool_transit_import", "bid": 0.9, "priority": 0.7, "capacity": 6.0},
            ),
            quantity=10.0,
        )
        anomaly = runtime.global_inventory_visibility_detect_inventory_anomaly(state)
        model = runtime.global_inventory_visibility_register_governed_model(
            "availability_risk",
            {"features": ("atp", "freshness", "in_transit"), "auc": 0.91, "drift_score": 0.03},
        )
        invariants = runtime.global_inventory_visibility_verify_formal_invariants(state)
        boundary = runtime.global_inventory_visibility_verify_owned_table_boundary(
            ("inventory_pool", "GoodsReceiptPosted", "GET /wms/stock/{item_id}", "foreign_inventory_table")
        )

        assert parsed["ok"] is True and parsed["item_id"] == ITEM_ID
        assert counterfactual["ok"] is True
        assert forecast["projected_available"] > 0
        assert risk["ok"] is True and risk["risk_score"] >= 0
        assert exception["action"] == "raise_replenishment_signal"
        assert routed["route"] == "appgen_outbox" and routed["failover_used"] is True
        assert policy["decision"] == "clear"
        assert controls["ok"] is True and controls["hash_chain_valid"] is True
        assert federation["systems"] == ("wms", "transportation", "orders")
        assert identity["ok"] is True
        assert resilience["ok"] is True
        assert crypto["crypto_epoch"]["algorithm"] == "dilithium3_simulated"
        assert carbon["node_id"] == "node_rotterdam_port"
        assert optimized["node_id"] in state["supply_nodes"]
        assert allocation["ok"] is True and allocation["clearing_bid"] > 0
        assert anomaly["ok"] is True
        assert model["ok"] is True and model["governance"]["regulated"] is True
        assert invariants["ok"] is True
        assert boundary["ok"] is False
        assert boundary["violations"] == ("GoodsReceiptPosted", "foreign_inventory_table")

        with pytest.raises(ValueError, match="PostgreSQL, MySQL, or MariaDB"):
            runtime.global_inventory_visibility_configure_runtime(
                runtime.global_inventory_visibility_empty_state(),
                {"database_backend": "sqlite", "event_topic": runtime.GLOBAL_INVENTORY_VISIBILITY_REQUIRED_EVENT_TOPIC},
            )
        with pytest.raises(ValueError, match="AppGen-X eventing only"):
            runtime.global_inventory_visibility_configure_runtime(
                runtime.global_inventory_visibility_empty_state(),
                {
                    "database_backend": "postgresql",
                    "event_topic": runtime.GLOBAL_INVENTORY_VISIBILITY_REQUIRED_EVENT_TOPIC,
                    "stream_engine": "user_selected_engine",
                },
            )
    finally:
        repository.close()
