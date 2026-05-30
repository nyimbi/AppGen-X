"""Executable domain behavior checks for the DOM PBC."""

from __future__ import annotations

import pytest

from .. import runtime
from .. import ui
from ..services import DomStandaloneService
from ..services import service_operation_manifest
from ..services import standalone_service_manifest


TENANT = "tenant_dom"
CUSTOMER_ID = "cust_dom_001"
ORDER_ID = "order_dom_001"


def _service() -> DomStandaloneService:
    service = DomStandaloneService(tenant=TENANT)
    configured = service.configure(
        {
            "database_backend": "postgresql",
            "event_topic": runtime.DOM_REQUIRED_EVENT_TOPIC,
            "retry_limit": 2,
            "default_currency": "USD",
        }
    )
    defaults = service.register_defaults(tenant=TENANT)
    customer = service.upsert_customer_projection(
        {
            "tenant": TENANT,
            "customer_id": CUSTOMER_ID,
            "status": "active",
            "risk": 0.04,
            "identity": {
                "did": "did:appgen:customer:001",
                "issuer": "trusted_registry",
                "status": "active",
            },
        }
    )
    assert configured["ok"] is True
    assert defaults["ok"] is True
    assert customer["ok"] is True
    return service


def _order_payload(order_id: str = ORDER_ID) -> dict:
    return {
        "tenant": TENANT,
        "order_id": order_id,
        "customer_id": CUSTOMER_ID,
        "channel": "web",
        "destination": "NBO",
        "service_level": "express",
        "currency": "USD",
        "source_system": "standalone",
        "lines": (
            {"line_id": "line_1", "item_id": "sku_dom_1", "quantity": 2, "unit_price": 120.0},
            {"line_id": "line_2", "item_id": "sku_dom_2", "quantity": 1, "unit_price": 60.0},
        ),
    }


def _ship_order(service: DomStandaloneService, order_id: str = ORDER_ID) -> DomStandaloneService:
    assert service.capture_order(_order_payload(order_id))["ok"] is True
    assert service.apply_tax_projection(order_id, {"calculation_id": f"tax_{order_id}", "tax_total": 30.0, "status": "calculated"})["ok"] is True
    assert service.screen_fraud(order_id, signals={"ip_risk": 0.04, "velocity": 0.03, "customer_risk": 0.04})["decision"] == "clear"
    assert service.verify_order(order_id)["ok"] is True
    assert service.price_order(order_id)["order"]["total"] == 330.0
    allocation = service.apply_inventory_allocation(
        order_id,
        (
            {"allocation_id": f"alloc_{order_id}_1", "item_id": "sku_dom_1", "quantity": 2, "node_id": "node_east", "confidence": 0.93},
            {"allocation_id": f"alloc_{order_id}_2", "item_id": "sku_dom_2", "quantity": 1, "node_id": "node_west", "confidence": 0.88},
        ),
    )
    assert allocation["ok"] is True
    assert service.create_fulfillment_plan(order_id)["ok"] is True
    assert service.route_fulfillment(order_id)["route"] == "outbox"
    assert service.confirm_order_shipped(order_id, shipment_id=f"ship_{order_id}")["ok"] is True
    return service


def test_dom_one_pbc_order_orchestration_lifecycle_is_executable():
    service = _ship_order(_service())
    snapshot = service.get_order_snapshot(ORDER_ID)
    workbench = service.workbench(tenant=TENANT)
    runtime_workbench = runtime.dom_build_workbench_view(service.state, tenant=TENANT)

    assert snapshot["ok"] is True
    assert snapshot["order"]["status"] == "shipped"
    assert snapshot["order"]["total"] == 330.0
    assert runtime_workbench["shipped_count"] == 1
    assert runtime_workbench["open_order_count"] == 0
    assert workbench["ok"] is True
    assert {form["submit_action"] for form in workbench["forms"].values()} >= {
        "capture_order",
        "apply_inventory_allocation",
        "record_exception",
    }
    assert {wizard["completion_action"] for wizard in workbench["wizards"].values()} >= {
        "price_order",
        "confirm_order_shipped",
    }
    assert workbench["binding_evidence"]["configuration"]["event_topic"] == runtime.DOM_REQUIRED_EVENT_TOPIC
    assert workbench["binding_evidence"]["configuration"]["stream_engine_picker_visible"] is False


def test_dom_service_ui_agent_and_repository_surface_work_as_one_pbc():
    service = _service()
    permissions = tuple(ui.dom_ui_contract()["binding_evidence"]["rbac_permissions"])
    form = service.app.submit_form("order_capture_form", _order_payload("order_form_001"), principal_permissions=permissions)
    intake = service.app.run_wizard(
        "order_intake_wizard",
        {
            "order": _order_payload("order_wizard_001"),
            "tax_projection": {"calculation_id": "tax_order_wizard_001", "tax_total": 15.0, "status": "calculated"},
            "fraud_signals": {"ip_risk": 0.01, "velocity": 0.02, "customer_risk": 0.01},
        },
        principal_permissions=permissions,
    )
    fulfillment = service.app.run_wizard(
        "fulfillment_wizard",
        {
            "order_id": "order_wizard_001",
            "allocations": (
                {"allocation_id": "alloc_wizard_1", "item_id": "sku_dom_1", "quantity": 2, "node_id": "node_east", "confidence": 0.91},
                {"allocation_id": "alloc_wizard_2", "item_id": "sku_dom_2", "quantity": 1, "node_id": "node_west", "confidence": 0.86},
            ),
            "shipment_id": "ship_wizard_001",
        },
        principal_permissions=permissions,
    )
    agent = service.app.run_agent_skill(
        "dom.document_instruction_intake",
        {
            "document": "Order order_wizard_001 customer cust_dom_001 channel web destination NBO amount 330",
            "instructions": "prepare the order verification and fulfillment tasks",
        },
        principal_permissions=permissions,
    )
    repository = service.repository_manifest()
    read_models = service.read_model_snapshot()

    assert form["ok"] is True
    assert intake["ok"] is True
    assert fulfillment["ok"] is True
    assert agent["ok"] is True
    assert repository["dashboard"]["counts"]["forms"] >= 1
    assert repository["dashboard"]["counts"]["workflows"] >= 2
    assert repository["dashboard"]["counts"]["agent_sessions"] >= 1
    assert read_models["orders"]
    assert standalone_service_manifest()["ok"] is True
    assert service_operation_manifest()["standalone_service"]["service_class"] == "DomStandaloneService"


def test_dom_events_are_idempotent_retryable_and_boundary_scoped():
    service = _service()
    event = {
        "event_id": "inv_evt_001",
        "event_type": "InventoryAllocated",
        "idempotency_key": "inventory:allocation:001",
        "payload": {"tenant": TENANT, "allocation_id": "alloc_external_001", "order_id": ORDER_ID, "node_id": "node_east"},
    }
    first = service.receive_event(event)
    duplicate = service.receive_event(event)
    failed = service.receive_event(
        {
            "event_id": "unknown_evt_001",
            "event_type": "UnmappedEvent",
            "idempotency_key": "unknown:event:001",
            "payload": {"tenant": TENANT},
        }
    )
    dead = service.receive_event(
        {
            "event_id": "unknown_evt_001",
            "event_type": "UnmappedEvent",
            "idempotency_key": "unknown:event:001",
            "payload": {"tenant": TENANT},
        }
    )
    allowed = runtime.dom_verify_owned_table_boundary(("sales_order", "InventoryAllocated", "GET /inventory/allocations/{id}"))
    blocked = runtime.dom_verify_owned_table_boundary(("foreign_inventory_table", "customer_profile"))

    assert first["ok"] is True
    assert duplicate["duplicate"] is True
    assert failed["ok"] is False
    assert failed["handler"]["status"] == "retrying"
    assert dead["ok"] is False
    assert dead["handler"]["status"] == "dead_letter"
    assert service.state["dead_letter"][-1]["reason"] == "unsupported_or_failed_dom_event"
    assert allowed["ok"] is True
    assert blocked["ok"] is False
    assert blocked["violations"] == ("foreign_inventory_table", "customer_profile")


def test_dom_configuration_rules_and_advanced_order_intelligence_are_executable():
    service = _ship_order(_service())
    state = service.state
    plan = next(value for value in state["fulfillment_plans"].values() if value["order_id"] == ORDER_ID)
    api = runtime.dom_build_api_contract()
    schema = runtime.dom_build_schema_contract()
    contract = runtime.dom_build_service_contract()
    evidence = runtime.dom_build_release_evidence()

    assert runtime.dom_simulate_fulfillment_policy(state, ORDER_ID, proposed_node="node_central")["node_changed"] is True
    assert runtime.dom_forecast_promise_demand((10, 12, 18), service_days=3)["promise_load"] == 13.33
    assert runtime.dom_parse_order_event("order order_dom_001 customer cust_dom_001 channel web amount 330")["ok"] is True
    assert runtime.dom_score_order_risk({"fraud": 0.05, "allocation_gap": 0.1, "customer_risk": 0.04})["decision"] == "monitor"
    assert runtime.dom_recommend_exception_resolution("allocation_gap")["action"] == "reroute_fulfillment"
    assert runtime.dom_route_fulfillment(
        plan,
        rails=({"route": "slow_api", "available": False, "latency": 5}, {"route": "outbox", "available": True, "latency": 1}),
    )["failover_used"] is True
    assert runtime.dom_generate_order_verification_proof(state, ORDER_ID, disclosure=("order_id", "status", "total"))["proof"].startswith("zk_order_")
    assert runtime.dom_screen_order_policy(state, ORDER_ID, restricted_destinations=("embargoed_zone",))["decision"] == "clear"
    assert runtime.dom_run_control_tests(state)["hash_chain_valid"] is True
    assert runtime.dom_federate_order_view(state, ORDER_ID, systems=("commerce", "fulfillment"))["projection"]["status"] == "shipped"
    assert runtime.dom_verify_order_identity({"did": "did:appgen:customer:001", "issuer": "trusted_registry", "status": "active"})["ok"] is True
    assert runtime.dom_run_resilience_drill(state, "fulfillment_route_timeout")["ok"] is True
    assert runtime.dom_rotate_crypto_epoch(state, "CRYSTALS-Dilithium")["key_id"] == "dom_epoch_0002"
    assert runtime.dom_schedule_carbon_aware_fulfillment(({"node_id": "node_east", "carbon": 42}, {"node_id": "node_west", "carbon": 21}))["node_id"] == "node_west"
    assert runtime.dom_optimize_fulfillment(
        ({"node_id": "node_a", "available": 4, "distance": 5, "carbon": 4}, {"node_id": "node_b", "available": 4, "distance": 3, "carbon": 2}),
        quantity=3,
    )["node_id"] == "node_b"
    assert runtime.dom_allocate_nodes(({"node_id": "node_a", "bid": 1.0, "service": 0.9}, {"node_id": "node_b", "bid": 1.2, "service": 0.8}), quantity=10)["ok"] is True
    assert runtime.dom_detect_order_anomaly(state)["ok"] is True
    assert runtime.dom_model_stochastic_fulfillment_exposure(delay_path=(1, 2, 4), volatility=0.2)["simulation_count"] == 1000
    assert runtime.dom_register_governed_model("dom_eta_model", {"auc": 0.9, "drift_score": 0.03, "features": ("distance", "carbon")})["ok"] is True
    assert api["ok"] is True
    assert schema["ok"] is True
    assert contract["ok"] is True
    assert evidence["ok"] is True


def test_dom_rejects_nonstandard_backends_and_user_eventing_pickers():
    state = runtime.dom_empty_state()

    with pytest.raises(ValueError, match="PostgreSQL, MySQL, or MariaDB"):
        runtime.dom_configure_runtime(state, {"database_backend": "sqlite", "event_topic": runtime.DOM_REQUIRED_EVENT_TOPIC})

    with pytest.raises(ValueError, match="AppGen-X event contract"):
        runtime.dom_configure_runtime(
            state,
            {
                "database_backend": "postgresql",
                "event_topic": runtime.DOM_REQUIRED_EVENT_TOPIC,
                "stream_engine": "user_selected_engine",
            },
        )
