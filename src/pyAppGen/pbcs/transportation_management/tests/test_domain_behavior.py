"""Executable domain behavior tests for the transportation_management PBC."""

from __future__ import annotations

import pytest

from .. import agent
from .. import release_evidence
from .. import routes
from .. import runtime
from .. import ui
from ..repository import TransportationManagementRepository
from ..repository import transportation_management_repository_contract
from ..standalone import TransportationManagementStandaloneApp
from ..standalone import smoke_test as standalone_smoke_test
from ..standalone import standalone_app_manifest
from ..services import StatefulTransportationManagementService
from ..services import runtime_service_manifest
from ..services import service_operation_manifest


TENANT = "tenant_tms"
SHIPMENT_ID = "ship-001"


def _configuration() -> dict:
    return {
        "database_backend": "postgresql",
        "event_topic": runtime.TRANSPORTATION_MANAGEMENT_REQUIRED_EVENT_TOPIC,
        "retry_limit": 2,
        "default_currency": "USD",
        "allowed_modes": ("truckload", "ltl", "parcel"),
        "telematics_providers": ("carrier_api", "gps_feed"),
        "timezone": "UTC",
        "workbench_limit": 100,
    }


def _prepared_service(*, delivered: bool = False) -> StatefulTransportationManagementService:
    service = StatefulTransportationManagementService()
    service.configure_runtime(_configuration())
    service.set_parameter({"name": "max_cost_per_mile", "value": 3.0})
    service.set_parameter({"name": "on_time_weight", "value": 0.35})
    service.set_parameter({"name": "carbon_weight", "value": 0.15})
    service.set_parameter({"name": "eta_confidence_threshold", "value": 0.75})
    service.register_rule(
        {
            "rule_id": "rule-ground",
            "tenant": TENANT,
            "scope": "carrier_selection",
            "allowed_modes": ("truckload", "ltl"),
            "preferred_carriers": ("carrier-a",),
            "restricted_carriers": ("carrier-blocked",),
            "service_level": "expedited",
            "hazmat_allowed": False,
            "status": "active",
        }
    )
    service.register_schema_extension({"table": "tracking_event", "fields": {"telematics_payload": "jsonb"}})
    service.register_carrier(
        {
            "carrier_id": "carrier-a",
            "tenant": TENANT,
            "mode": "truckload",
            "service_levels": ("expedited", "standard"),
            "lanes": (("NYC", "BOS"),),
            "cost_per_mile": 2.1,
            "on_time_rate": 0.96,
            "carbon_per_mile": 120,
            "risk": 0.08,
            "identity": {"did": "did:appgen:carrier-a", "issuer": "trusted_registry", "status": "active"},
        }
    )
    service.register_carrier(
        {
            "carrier_id": "carrier-b",
            "tenant": TENANT,
            "mode": "ltl",
            "service_levels": ("standard", "expedited"),
            "lanes": (("NYC", "BOS"),),
            "cost_per_mile": 1.8,
            "on_time_rate": 0.83,
            "carbon_per_mile": 80,
            "risk": 0.16,
            "identity": {"did": "did:appgen:carrier-b", "issuer": "trusted_registry", "status": "active"},
        }
    )
    service.create_shipment(
        {
            "shipment_id": SHIPMENT_ID,
            "tenant": TENANT,
            "source_ref": "order-100",
            "origin": "NYC",
            "destination": "BOS",
            "weight": 1200.0,
            "mode": "truckload",
            "service_level": "expedited",
            "hazmat": False,
            "temperature_controlled": False,
        }
    )
    service.select_carrier({"shipment_id": SHIPMENT_ID})
    service.plan_route({"shipment_id": SHIPMENT_ID, "distance_miles": 215.0, "stops": ("NYC", "BOS")})
    service.dispatch_shipment({"shipment_id": SHIPMENT_ID, "tender_id": "tender-001"})
    service.record_tracking_event(
        {
            "shipment_id": SHIPMENT_ID,
            "event": {"event_id": "track-001", "location": "Hartford", "distance_remaining": 100.0, "delay_minutes": 15.0},
        }
    )
    if delivered:
        service.confirm_inbound_arrival({"shipment_id": SHIPMENT_ID, "facility": "BOS-DC"})
        service.confirm_delivery({"shipment_id": SHIPMENT_ID, "proof_id": "pod-001"})
    return service


def test_transportation_ship_to_deliver_lifecycle_is_runtime_backed() -> None:
    service = _prepared_service(delivered=True)

    workbench = service.build_workbench_view({"tenant": TENANT})
    assert workbench["shipment_count"] == 1
    assert workbench["delivered_count"] == 1
    assert workbench["carrier_count"] == 2
    assert workbench["route_count"] == 1
    assert workbench["tracking_count"] == 1
    assert workbench["event_contract"] == "AppGen-X"

    shipment = service.state["shipments"][SHIPMENT_ID]
    route = service.state["routes"][f"route_{SHIPMENT_ID}"]
    assert shipment["status"] == "delivered"
    assert shipment["carrier_id"] == "carrier-a"
    assert shipment["proof_id"] == "pod-001"
    assert route["estimated_cost"] == 451.5
    assert route["estimated_carbon"] == 25800.0

    event_types = tuple(event["event_type"] for event in service.state["events"])
    assert event_types == (
        "CarrierRegistered",
        "CarrierRegistered",
        "ShipmentCreated",
        "CarrierSelected",
        "FreightRoutePlanned",
        "ShipmentDispatched",
        "EtaUpdated",
        "InboundArrived",
        "ShipmentDelivered",
    )
    assert all(event["idempotency_key"].startswith("transportation_management:") for event in service.state["outbox"])


def test_transportation_eta_policy_delivery_proof_and_ui_are_bound() -> None:
    service = _prepared_service(delivered=True)

    eta = service.calculate_eta({"shipment_id": SHIPMENT_ID, "average_speed_mph": 50.0})
    policy = service.screen_policy({"shipment_id": SHIPMENT_ID, "restricted_carriers": ("carrier-blocked",)})
    proof = service.generate_delivery_proof({"shipment_id": SHIPMENT_ID, "disclosure": ("shipment_id", "carrier_id", "status")})
    permissions = tuple(sorted(set(ui.transportation_management_ui_contract()["action_permissions"].values())))
    rendered = ui.transportation_management_render_workbench(service.state, tenant=TENANT, principal_permissions=permissions)

    assert eta["eta_hours"] == 2.25
    assert eta["confidence"] >= 0.75
    assert policy["decision"] == "clear"
    assert proof["proof"].startswith("zk_delivery_")
    assert proof["public_claims"] == {"shipment_id": SHIPMENT_ID, "carrier_id": "carrier-a", "status": "delivered"}
    assert rendered["ok"] is True
    assert "TransportationWorkbench" in rendered["fragments"]
    assert "ship_to_deliver_wizard" in {wizard["key"] for wizard in rendered["wizards"]}
    assert "delivery_proof_form" in {form["key"] for form in rendered["forms"]}
    assert rendered["event_outbox_count"] == 9
    assert rendered["binding_evidence"]["outbox_table"] == "transportation_management_appgen_outbox_event"
    assert rendered["binding_evidence"]["shared_table_access"] is False


def test_transportation_advanced_execution_intelligence_and_governance_are_executable() -> None:
    service = _prepared_service(delivered=True)
    state = service.state

    simulation = runtime.transportation_management_simulate_carrier_route(state, SHIPMENT_ID, proposed_carrier="carrier-b")
    forecast = runtime.transportation_management_forecast_eta_cost_delay((215.0, 100.0, 0.0), cost_per_mile=2.1)
    parsed = runtime.transportation_management_parse_transport_event("shipment ship_77 carrier carrier_a eta 4 delay 15")
    risk = runtime.transportation_management_score_transport_risk({"delay_rate": 0.08, "damage_rate": 0.01, "carrier_risk": 0.08})
    exception = runtime.transportation_management_recommend_exception_resolution("delay")
    edge_route = runtime.transportation_management_route_telematics_event(
        {"event_id": "telem-001"},
        rails=(
            {"route": "carrier_api", "available": False, "latency": 1},
            {"route": "outbox", "available": True, "latency": 3},
        ),
    )
    controls = runtime.transportation_management_run_control_tests(state)
    federation = runtime.transportation_management_federate_transportation_view(state, SHIPMENT_ID, systems=("wms", "procurement", "finance"))
    identity = runtime.transportation_management_verify_carrier_identity(state["carriers"]["carrier-a"]["identity"])
    resilience = runtime.transportation_management_run_resilience_drill(state, "carrier_api_timeout")
    crypto = runtime.transportation_management_rotate_crypto_epoch(state, "dilithium3_simulated")
    carbon = runtime.transportation_management_schedule_carbon_aware_route(tuple(state["carriers"].values()))
    optimization = runtime.transportation_management_optimize_route_carrier(tuple(state["carriers"].values()), distance_miles=215.0)
    tender = runtime.transportation_management_allocate_carrier_tender(tuple(state["carriers"].values()), load_count=10)
    anomaly = runtime.transportation_management_detect_tracking_anomaly(state)
    stochastic = runtime.transportation_management_model_stochastic_transit_exposure(delay_path=(5.0, 15.0, 25.0), volatility=0.08)
    model = runtime.transportation_management_register_governed_model(
        "transport_delay",
        {"features": ("distance", "carrier", "delay"), "auc": 0.9, "drift_score": 0.04},
    )

    assert simulation["cost_delta"] < 0
    assert forecast["remaining_distance"] == 0.0
    assert parsed["ok"] is True and parsed["delay_minutes"] == 15.0
    assert risk["decision"] == "monitor"
    assert exception["action"] == "notify_customer_and_resequence"
    assert edge_route["route"] == "outbox" and edge_route["failover_used"] is True
    assert controls["ok"] is True and controls["hash_chain_valid"] is True
    assert federation["systems"] == ("wms", "procurement", "finance")
    assert identity["ok"] is True
    assert resilience["mode"] == "degraded_telematics_route"
    assert crypto["epoch"] == 2
    assert carbon["carrier_id"] == "carrier-b"
    assert optimization["carrier_id"] == "carrier-b"
    assert tender["ok"] is True and tender["clearing_bid"] > 0
    assert anomaly["entropy"] >= 0
    assert stochastic["tail_risk"] > stochastic["expected_exposure"]
    assert model["ok"] is True and model["governance"]["regulated"] is True


def test_transportation_event_handlers_retry_dead_letter_service_and_boundary_guards() -> None:
    service = _prepared_service()

    processed = service.receive_event(
        {
            "event_id": "packed-evt-001",
            "event_type": "Packed",
            "payload": {"tenant": TENANT, "pack_id": "pack-001", "order_id": "order-100", "weight": 1200.0},
        }
    )
    duplicate = service.receive_event(
        {
            "event_id": "packed-evt-001",
            "event_type": "Packed",
            "payload": {"tenant": TENANT, "pack_id": "pack-001", "order_id": "order-100", "weight": 1200.0},
        }
    )
    retrying = service.receive_event({"event_id": "bad-evt-001", "event_type": "UnknownTransportationEvent", "payload": {"tenant": TENANT}})
    dead_letter = service.receive_event({"event_id": "bad-evt-001", "event_type": "UnknownTransportationEvent", "payload": {"tenant": TENANT}})

    assert processed["handler"]["status"] == "processed"
    assert service.state["packed_order_projections"]["pack-001"]["weight"] == 1200.0
    assert duplicate["duplicate"] is True
    assert retrying["handler"]["status"] == "retrying"
    assert dead_letter["handler"]["status"] == "dead_letter"
    assert service.state["dead_letters"][-1]["reason"] == "unsupported_or_failed_transportation_event"

    runtime_manifest = runtime_service_manifest()
    generated_manifest = service_operation_manifest()
    assert runtime_manifest["ok"] is True
    assert runtime_manifest["service_class"] == "StatefulTransportationManagementService"
    assert runtime_manifest["event_contract"] == "AppGen-X"
    assert generated_manifest["ok"] is True
    assert all(contract["event_contract"] == "AppGen-X" for contract in generated_manifest["operation_contracts"])

    boundary = runtime.transportation_management_verify_owned_table_boundary(
        ("shipment", "Packed", "GET /wms/packed-orders/{id}", "foreign_transportation_table")
    )
    assert boundary["ok"] is False
    assert boundary["violations"] == ("foreign_transportation_table",)

    with pytest.raises(ValueError, match="PostgreSQL, MySQL, or MariaDB"):
        service.configure_runtime({**_configuration(), "database_backend": "sqlite"})
    with pytest.raises(ValueError, match="AppGen-X event contract"):
        service.configure_runtime({**_configuration(), "stream_engine_picker": "user_choice"})


def test_transportation_routes_repository_agent_standalone_and_release_surfaces_are_executable() -> None:
    route_validation = routes.validate_api_route_contracts()
    shipment_dispatch = routes.dispatch_route(
        "POST",
        "/api/pbc/transportation_management/transportation/shipments",
        {"tenant": TENANT, "shipment_id": "ship-route-001"},
    )
    workbench_dispatch = routes.dispatch_route(
        "GET",
        "/api/pbc/transportation_management/transportation/workbench",
        {"tenant": TENANT},
    )

    assert route_validation["ok"] is True
    assert all(contract["event_contract"] == "AppGen-X" for contract in route_validation["contracts"])
    assert all(contract["stream_engine_picker_visible"] is False for contract in route_validation["contracts"])
    assert all(contract["shared_table_access"] is False for contract in route_validation["contracts"])
    assert shipment_dispatch["ok"] is True
    assert shipment_dispatch["result"]["outbox_table"] == "transportation_management_appgen_outbox_event"
    assert workbench_dispatch["ok"] is True
    assert workbench_dispatch["result"]["read_only"] is True

    skills = agent.agent_skill_manifest()
    chatbot = agent.chatbot_interface_contract()
    document_plan = agent.document_instruction_plan(
        "Create a BOS shipment, select an expedited carrier, plan the route, and capture delivery proof.",
        "Validate carrier policy, ETA confidence, telematics events, and freight audit controls first.",
    )
    create_plan = agent.datastore_crud_plan(
        "create",
        "transportation_management_shipment",
        {"shipment_id": "ship-agent-001", "origin": "NYC", "destination": "BOS"},
    )
    blocked_plan = agent.datastore_crud_plan("delete", "wms_core_pick_task", {})
    contribution = agent.composed_agent_contribution()

    assert skills["ok"] is True
    assert chatbot["ok"] is True
    assert document_plan["ok"] is True
    assert create_plan["ok"] is True and create_plan["requires_confirmation"] is True
    assert blocked_plan["ok"] is False
    assert contribution["ok"] is True
    assert "transportation_management_crud" in contribution["dsl_tools"]

    app = TransportationManagementStandaloneApp()
    loaded = app.load_demo_workspace(tenant=TENANT)
    rendered = app.render_workbench(tenant=TENANT)
    read_model = TransportationManagementRepository(app.state).read_model(TENANT)
    binding = TransportationManagementRepository(app.state).form_binding_plan("shipment_creation_form")

    assert standalone_app_manifest()["ok"] is True
    assert standalone_smoke_test()["ok"] is True
    assert transportation_management_repository_contract()["ok"] is True
    assert loaded["ok"] is True
    assert rendered["ok"] is True
    assert rendered["shell"]["app_id"] == "transportation_management_one_pbc_app"
    assert read_model["shipment"]["shipment_count"] == 1
    assert read_model["carrier"]["carrier_count"] >= 2
    assert read_model["route"]["route_count"] == 1
    assert read_model["tracking"]["delivered_count"] == 1
    assert binding["ok"] is True
    assert binding["event_contract"] == "AppGen-X"

    release_validation = release_evidence.validate_release_evidence()
    release_smoke = release_evidence.smoke_test()
    assert release_validation["ok"] is True
    assert release_smoke["ok"] is True
    assert release_smoke["evidence"]["repository"]["shared_table_access"] is False
