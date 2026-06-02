"""Executable domain behavior tests for the order_routing_optimization PBC."""

from __future__ import annotations

import pytest

from .. import agent
from .. import release_evidence
from .. import routes
from .. import runtime
from .. import ui
from ..app_surface import app_surface_smoke_test
from ..app_surface import document_instruction_routing_plan
from ..app_surface import single_pbc_routing_app_contract
from ..services import OrderRoutingOptimizationService
from ..services import service_operation_manifest
from ..services import service_operation_contracts


TENANT = "tenant_alpha"
ORDER_ID = "order_100"
DECISION_ID = "route_req_domain"


def _configuration() -> dict:
    return {
        "database_backend": "postgresql",
        "event_topic": runtime.ORDER_ROUTING_OPTIMIZATION_REQUIRED_EVENT_TOPIC,
        "retry_limit": 3,
        "default_currency": "USD",
        "supported_regions": ("west", "central"),
        "supported_split_policies": ("forbid", "allow"),
        "supported_substitution_modes": ("exact", "equivalent"),
        "topology_systems": ("dom", "inventory", "tax", "wms", "transport"),
        "default_timezone": "UTC",
        "workbench_limit": 100,
    }


def _configured_state() -> dict:
    state = runtime.order_routing_optimization_empty_state()
    state = runtime.order_routing_optimization_configure_runtime(state, _configuration())["state"]
    for name, value in {
        "cost_weight": 0.25,
        "sla_weight": 0.35,
        "capacity_weight": 0.2,
        "risk_weight": 0.1,
        "carbon_weight": 0.1,
        "reservation_hold_minutes": 45,
        "forecast_horizon_hours": 24,
        "max_split_count": 2,
        "simulation_sample_size": 500,
        "confidence_floor": 0.5,
    }.items():
        state = runtime.order_routing_optimization_set_parameter(state, name, value)["state"]
    state = runtime.order_routing_optimization_register_rule(
        state,
        {
            "rule_id": "rule_domain",
            "tenant": TENANT,
            "rule_type": "routing",
            "regions": ("west",),
            "eligible_nodes": ("node_fast", "node_green"),
            "preferred_nodes": ("node_fast",),
            "capacity_floor": 2,
            "split_policy": "allow",
            "substitution_mode": "equivalent",
            "status": "active",
        },
    )["state"]
    return runtime.order_routing_optimization_register_schema_extension(
        state,
        "routing_decision",
        {"explainability_vector": "jsonb"},
    )["state"]


def _routed_state() -> tuple[dict, dict, tuple[dict, ...]]:
    state = _configured_state()
    for event in (
        {
            "event_id": "evt_order_verified_domain",
            "event_type": "OrderVerified",
            "payload": {"tenant": TENANT, "order_id": ORDER_ID},
        },
        {
            "event_id": "evt_availability_fast_domain",
            "event_type": "AvailabilityProjected",
            "payload": {"tenant": TENANT, "node_id": "node_fast", "available_units": 6},
        },
        {
            "event_id": "evt_tax_domain",
            "event_type": "TaxCalculated",
            "payload": {"tenant": TENANT, "order_id": ORDER_ID, "tax_total": 12.5},
        },
    ):
        state = runtime.order_routing_optimization_handle_event(state, event)["state"]
    for snapshot in (
        {
            "snapshot_id": "cap_fast_domain",
            "tenant": TENANT,
            "node_id": "node_fast",
            "available_units": 6,
            "reserved_units": 0,
            "forecast_load": 4,
        },
        {
            "snapshot_id": "cap_green_domain",
            "tenant": TENANT,
            "node_id": "node_green",
            "available_units": 6,
            "reserved_units": 0,
            "forecast_load": 3,
        },
    ):
        state = runtime.order_routing_optimization_ingest_capacity_snapshot(state, snapshot)["state"]
    for candidate in (
        {
            "candidate_id": "cand_fast_domain",
            "tenant": TENANT,
            "order_id": ORDER_ID,
            "node_id": "node_fast",
            "region": "west",
            "distance_km": 180,
            "base_cost": 118,
            "sla_hours": 10,
            "carbon_kg": 46,
            "risk_score": 0.08,
            "available_units": 6,
            "inventory_source": "fc_west_a",
            "split_supported": True,
            "substitution_eligible": True,
        },
        {
            "candidate_id": "cand_green_domain",
            "tenant": TENANT,
            "order_id": ORDER_ID,
            "node_id": "node_green",
            "region": "west",
            "distance_km": 220,
            "base_cost": 108,
            "sla_hours": 18,
            "carbon_kg": 18,
            "risk_score": 0.12,
            "available_units": 6,
            "inventory_source": "fc_west_b",
            "split_supported": True,
            "substitution_eligible": True,
        },
    ):
        state = runtime.order_routing_optimization_upsert_route_candidate(state, candidate)["state"]
    routed = runtime.order_routing_optimization_route_orders(
        state,
        {
            "request_id": "req_domain",
            "tenant": TENANT,
            "order_id": ORDER_ID,
            "region": "west",
            "requested_units": 10,
            "sla_target_hours": 24,
            "allow_split": True,
            "substitution_requested": False,
        },
    )
    return routed["state"], routed["decision"], routed["candidate_scores"]


def test_order_routing_lifecycle_models_services_and_release_evidence_are_executable() -> None:
    state, decision, candidate_scores = _routed_state()
    simulated = runtime.order_routing_optimization_simulate_counterfactual(
        state,
        DECISION_ID,
        proposed_node="node_green",
    )
    state = simulated["state"]
    workbench = runtime.order_routing_optimization_build_workbench_view(state, tenant=TENANT)
    controls = runtime.order_routing_optimization_run_control_tests(state)
    schema = runtime.order_routing_optimization_build_schema_contract()
    service = runtime.order_routing_optimization_build_service_contract()
    release = runtime.order_routing_optimization_build_release_evidence()

    assert decision["status"] == "selected"
    assert decision["split"] is True
    assert decision["allocated_units"] == 10.0
    assert len(decision["reservation_ids"]) == 2
    assert len(candidate_scores) == 2
    assert state["routing_plans"][DECISION_ID]["selected_node_ids"] == decision["selected_node_ids"]
    assert state["routing_promises"][f"promise_{DECISION_ID}"]["status"] == "active"
    assert state["split_shipments"][DECISION_ID]["allocation_count"] == 2
    assert simulated["ok"] is True and simulated["proposed_node"] == "node_green"
    assert workbench["ok"] is True
    assert workbench["routing_plan_count"] == 1
    assert workbench["reservation_count"] == 2
    assert workbench["route_simulation_count"] == 1
    assert workbench["binding_evidence"]["configuration"]["event_contract"] == "AppGen-X"
    assert controls["ok"] is True and controls["hash_chain_valid"] is True
    assert schema["ok"] is True
    assert schema["datastore_backends"] == runtime.ORDER_ROUTING_OPTIMIZATION_ALLOWED_DATABASE_BACKENDS
    assert service["ok"] is True
    assert "route_orders" in service["command_methods"]
    assert release["ok"] is True
    assert not release["blocking_gaps"]


def test_order_routing_ui_agent_routes_and_single_pbc_app_are_executable() -> None:
    state, _, _ = _routed_state()
    permissions = tuple(set(ui.order_routing_optimization_ui_contract()["action_permissions"].values()))
    rendered = ui.order_routing_optimization_render_workbench(
        state,
        tenant=TENANT,
        principal_permissions=permissions,
    )
    app = single_pbc_routing_app_contract()
    app_smoke = app_surface_smoke_test()
    route_validation = routes.validate_api_route_contracts()
    command_dispatch = routes.dispatch_route(
        "POST",
        "/api/pbc/order_routing_optimization/route-orders",
        {"tenant": TENANT, "order_id": ORDER_ID},
    )
    query_dispatch = routes.dispatch_route(
        "GET",
        "/api/pbc/order_routing_optimization/route-candidates",
        {"tenant": TENANT, "order_id": ORDER_ID},
    )
    standalone_routes = routes.standalone_app_route_contracts()
    service = OrderRoutingOptimizationService()
    service_result = service.command_route_orders({"tenant": TENANT, "order_id": ORDER_ID})
    document_plan = document_instruction_routing_plan(
        "Node capacity ATP feed with candidate carriers and split shipment policy.",
        "Load capacity, generate candidates, optimize split route, and reserve capacity.",
    )
    skill_manifest = agent.agent_skill_manifest()
    chatbot = agent.chatbot_interface_contract()
    crud_plan = agent.datastore_crud_plan(
        "create",
        "order_routing_optimization_route_candidate",
        {"candidate_id": "cand_new"},
    )
    blocked_plan = agent.datastore_crud_plan("update", "foreign_route_table", {})
    contribution = agent.composed_agent_contribution()
    release_validation = release_evidence.validate_release_evidence()

    assert rendered["ok"] is True
    assert "OrderRoutingWorkbench" in rendered["fragments"]
    assert rendered["forms"] and rendered["wizards"] and rendered["controls"]
    assert rendered["single_pbc_app"]["database_backed"] is True
    assert app["ok"] is True
    assert app["allowed_database_backends"] == ("postgresql", "mysql", "mariadb")
    assert app["event_contract"] == "AppGen-X"
    assert app["stream_engine_picker_visible"] is False
    assert app_smoke["ok"] is True
    assert route_validation["ok"] is True
    assert all(contract["event_contract"] == "AppGen-X" for contract in route_validation["contracts"])
    assert all(contract["shared_table_access"] is False for contract in route_validation["contracts"])
    assert command_dispatch["ok"] is True and command_dispatch["result"]["read_only"] is False
    assert query_dispatch["ok"] is True and query_dispatch["result"]["read_only"] is True
    assert standalone_routes["ok"] is True and standalone_routes["stream_engine_picker_visible"] is False
    assert service_operation_manifest()["ok"] is True
    assert service_operation_contracts()["ok"] is True
    assert service_result["ok"] is True
    assert document_plan["target_table"] == "order_routing_optimization_capacity_snapshot"
    assert document_plan["requires_human_confirmation"] is True
    assert skill_manifest["ok"] is True
    assert chatbot["ok"] is True
    assert crud_plan["ok"] is True and crud_plan["requires_confirmation"] is True
    assert blocked_plan["ok"] is False
    assert contribution["ok"] is True
    assert "order_routing_optimization_crud" in contribution["dsl_tools"]
    assert release_validation["ok"] is True


def test_order_routing_event_idempotency_dead_letter_boundary_and_advanced_runtime_are_executable() -> None:
    state = _configured_state()
    event = {
        "event_id": "evt_duplicate_domain",
        "event_type": "OrderVerified",
        "payload": {"tenant": TENANT, "order_id": ORDER_ID},
    }
    first = runtime.order_routing_optimization_handle_event(state, event)
    duplicate = runtime.order_routing_optimization_handle_event(first["state"], event)
    failing_event = {
        "event_id": "evt_dead_domain",
        "event_type": "AvailabilityProjected",
        "payload": {"tenant": TENANT, "node_id": "node_fast", "available_units": 0},
    }
    failed_once = runtime.order_routing_optimization_handle_event(
        duplicate["state"],
        failing_event,
        simulate_failure=True,
    )
    failed_twice = runtime.order_routing_optimization_handle_event(
        failed_once["state"],
        failing_event,
        simulate_failure=True,
    )
    dead_letter = runtime.order_routing_optimization_handle_event(
        failed_twice["state"],
        failing_event,
        simulate_failure=True,
    )
    routed_state, decision, candidate_scores = _routed_state()

    forecast = runtime.order_routing_optimization_forecast_capacity(
        capacity_path=(9, 8, 7),
        demand_path=(3, 4, 5),
        horizon_hours=24,
    )
    parsed = runtime.order_routing_optimization_parse_route_request(
        "route order order_100 region west units 10 sla 24 split allow"
    )
    risk = runtime.order_routing_optimization_score_fulfillment_risk(
        {
            "stockout_probability": 0.2,
            "tax_variance": 0.06,
            "exception_rate": 0.12,
            "capacity_volatility": 0.08,
        }
    )
    healed = runtime.order_routing_optimization_self_heal_route_selection(
        decision,
        candidate_scores,
        unavailable_nodes=("node_fast",),
    )
    proof = runtime.order_routing_optimization_generate_routing_proof(
        routed_state,
        DECISION_ID,
        disclosure=("order_id", "selected_node_ids", "split"),
    )
    screening = runtime.order_routing_optimization_screen_policy(
        routed_state,
        DECISION_ID,
        blocked_nodes=("node_blocked",),
        carbon_budget=80,
    )
    federation = runtime.order_routing_optimization_federate_routing_view(
        routed_state,
        ORDER_ID,
        systems=("dom", "inventory", "tax"),
    )
    resilience = runtime.order_routing_optimization_run_resilience_drill(
        routed_state,
        "availability_projection_timeout",
    )
    crypto = runtime.order_routing_optimization_rotate_crypto_epoch(routed_state, "dilithium3_simulated")
    carbon = runtime.order_routing_optimization_schedule_carbon_aware_route(candidate_scores)
    optimized = runtime.order_routing_optimization_optimize_route_network(candidate_scores, demand_units=10)
    auction = runtime.order_routing_optimization_clear_capacity_auction(
        (
            {"node_id": "node_fast", "bid": 0.92, "available_units": 6},
            {"node_id": "node_green", "bid": 0.88, "available_units": 6},
        ),
        quantity=10,
    )
    anomaly = runtime.order_routing_optimization_detect_routing_anomaly(routed_state)
    exposure = runtime.order_routing_optimization_model_stochastic_exposure(
        score_path=(0.62, 0.67, 0.71),
        volatility=0.14,
    )
    model = runtime.order_routing_optimization_register_governed_model(
        "routing_risk",
        {"features": ("cost", "sla", "capacity"), "auc": 0.91, "drift_score": 0.03},
    )
    boundary = runtime.order_routing_optimization_verify_owned_table_boundary(
        ("routing_plan", "OrderVerified", "GET /wms-capacity", "foreign_route_table")
    )

    assert first["ok"] is True and first["duplicate"] is False
    assert duplicate["ok"] is True and duplicate["duplicate"] is True
    assert failed_once["ok"] is False
    assert failed_twice["ok"] is False
    assert dead_letter["ok"] is False
    assert dead_letter["dead_letter"]["reason"] == "simulated_failure"
    assert forecast["ok"] is True and forecast["expected_available_units"] >= 0
    assert parsed["ok"] is True and parsed["requested_units"] == 10
    assert risk["ok"] is True and risk["band"] == "low"
    assert healed["ok"] is True and healed["selected_node"] == "node_green"
    assert proof["ok"] is True and proof["proof"].startswith("zk_routing_")
    assert screening["decision"] == "clear"
    assert federation["ok"] is True and federation["projection"]["verified"] is True
    assert resilience["ok"] is True and resilience["mode"] == "degraded_outbox_replay"
    assert crypto["algorithm"] == "dilithium3_simulated"
    assert carbon["node_id"] == "node_green"
    assert optimized["ok"] is True and optimized["objective_score"] > 0
    assert auction["ok"] is True and auction["clearing_bid"] > 0
    assert anomaly["ok"] is True and anomaly["entropy"] >= 0
    assert exposure["ok"] is True and exposure["tail_risk"] > 0
    assert model["ok"] is True and model["governance"]["regulated"] is True
    assert boundary["ok"] is False
    assert boundary["violations"] == ("foreign_route_table",)

    with pytest.raises(ValueError, match="PostgreSQL, MySQL, or MariaDB"):
        runtime.order_routing_optimization_configure_runtime(
            runtime.order_routing_optimization_empty_state(),
            {**_configuration(), "database_backend": "sqlite"},
        )
    with pytest.raises(ValueError, match="Unsupported Order Routing Optimization configuration fields"):
        runtime.order_routing_optimization_configure_runtime(
            runtime.order_routing_optimization_empty_state(),
            {**_configuration(), "stream_engine": "user_selected_engine"},
        )
