"""Executable domain behavior tests for the inventory_positioning PBC."""

from __future__ import annotations

import pytest

from .. import runtime
from .. import ui
from ..permissions import permission_manifest
from ..services import InventoryPositioningService
from ..services import service_operation_manifest


TENANT = "tenant_inv"
ITEM_ID = "sku-100"
NODE_ID = "node-east"


def _configuration() -> dict:
    return {
        "database_backend": "postgresql",
        "event_topic": runtime.INVENTORY_POSITIONING_REQUIRED_EVENT_TOPIC,
        "retry_limit": 2,
        "default_uom": "EA",
        "precision": 2,
        "allowed_statuses": ("available", "reserved", "quarantine", "damaged", "in_transit"),
        "workbench_limit": 100,
    }


def _prepared_service() -> InventoryPositioningService:
    service = InventoryPositioningService()
    service.configure_runtime(_configuration())
    service.set_parameter({"name": "safety_stock_percent", "value": 0.1})
    service.set_parameter({"name": "partial_allocation_threshold", "value": 0.5})
    service.set_parameter({"name": "reservation_ttl_minutes", "value": 1440})
    service.set_parameter({"name": "reconciliation_tolerance_units", "value": 1})
    service.register_rule(
        {
            "rule_id": "rule_fefo_standard",
            "tenant": TENANT,
            "scope": "allocation_priority",
            "status": "active",
            "node_preference": (NODE_ID,),
            "allow_partial": True,
            "prevent_negative": True,
            "lot_policy": "fefo",
        }
    )
    service.register_schema_extension(
        {
            "table": "inventory_positioning_inventory_position",
            "fields": {"temperature_band": "jsonb", "regulatory_zone": "varchar"},
        }
    )
    service.register_item(
        {
            "tenant": TENANT,
            "item_id": ITEM_ID,
            "sku": "SKU-100",
            "uom": "EA",
            "lot_tracked": True,
            "serial_tracked": False,
            "substitution_group": "sku-100-core",
            "shelf_life_days": 365,
            "allocation_eligible": True,
            "identity": {"did": "did:appgen:item-sku-100", "issuer": "trusted_registry", "status": "active"},
        }
    )
    service.register_node(
        {
            "tenant": TENANT,
            "node_id": NODE_ID,
            "node_type": "warehouse",
            "country": "US",
            "region": "east",
            "calendar": "weekday",
            "carbon_intensity": 180,
            "identity": {"did": "did:appgen:node-east", "issuer": "trusted_registry", "status": "active"},
        }
    )
    service.post_goods_receipt(
        {
            "tenant": TENANT,
            "receipt_id": "rcpt-001",
            "node_id": NODE_ID,
            "item_id": ITEM_ID,
            "quantity": 100.0,
            "lot_id": "lot-001",
            "expires": "2030-12-31",
        }
    )
    service.post_adjustment(
        {
            "adjustment_id": "adj-cycle-001",
            "node_id": NODE_ID,
            "item_id": ITEM_ID,
            "quantity": -2.0,
            "reason": "cycle_count",
        }
    )
    return service


def test_inventory_receipt_adjustment_atp_allocation_and_release_lifecycle() -> None:
    service = _prepared_service()

    availability = service.calculate_availability({"tenant": TENANT, "item_id": ITEM_ID, "demand_class": "standard"})
    assert availability["available_to_promise"] == 88.2
    assert availability["operation_contract"]["event_contract"] == "AppGen-X"

    allocation = service.allocate_inventory(
        {
            "allocation_id": "alloc-001",
            "tenant": TENANT,
            "order_id": "order-001",
            "item_id": ITEM_ID,
            "quantity": 40.0,
            "demand_class": "standard",
        }
    )
    assert allocation["ok"] is True
    assert allocation["allocation"]["quantity_allocated"] == 40.0
    assert allocation["allocation"]["status"] == "allocated"
    assert allocation["operation_contract"]["owned_tables"] == (
        "inventory_positioning_allocation",
        "inventory_positioning_allocation_line",
        "inventory_positioning_inventory_position",
    )

    position = next(iter(service.state["positions"].values()))
    assert position["reserved"] == 40.0
    assert position["allocated"] == 40.0

    release = service.release_allocation({"allocation_id": "alloc-001", "reason": "order_cancelled"})
    assert release["allocation"]["status"] == "released"
    assert service.calculate_availability({"tenant": TENANT, "item_id": ITEM_ID})["available_to_promise"] == 88.2

    event_types = tuple(event["event_type"] for event in service.state["events"])
    assert event_types == (
        "ItemRegistered",
        "InventoryNodeRegistered",
        "GoodsReceiptPosted",
        "InventoryAdjusted",
        "InventoryAllocated",
        "InventoryReleased",
    )
    assert all(outbox["idempotency_key"].startswith("inventory_positioning:") for outbox in service.state["outbox"])


def test_inventory_quality_hold_replenishment_reconciliation_proof_and_ui_are_bound() -> None:
    service = _prepared_service()
    service.apply_quality_hold(
        {
            "hold_id": "hold-001",
            "node_id": NODE_ID,
            "item_id": ITEM_ID,
            "quantity": 5.0,
            "reason": "inspection",
        }
    )

    availability = service.calculate_availability({"tenant": TENANT, "item_id": ITEM_ID, "demand_class": "premium"})
    assert availability["available_to_promise"] == 83.2

    signal = service.generate_replenishment_signal({"item_id": ITEM_ID, "reorder_point": 120.0, "forecast_demand": 40.0})
    assert signal["ok"] is True
    assert signal["recommended_quantity"] == 62.0

    reconciliation = service.reconcile_inventory({"item_id": ITEM_ID, "physical_count": 98.0})
    assert reconciliation["ok"] is True
    assert reconciliation["variance"] == 0.0

    proof = service.generate_stock_proof({"item_id": ITEM_ID, "disclosure": ("item_id", "available")})
    assert proof["proof"].startswith("zk_stock_")
    assert proof["public_claims"] == {"item_id": ITEM_ID, "available": 83.2}

    permissions = tuple(dict.fromkeys(permission_manifest()["action_permissions"].values()))
    rendered = ui.inventory_positioning_render_workbench(service.state, tenant=TENANT, principal_permissions=permissions)
    assert rendered["ok"] is True
    assert "InventoryAgentPanel" in rendered["fragments"]
    assert "allocation_preview_wizard" in {wizard["key"] for wizard in rendered["wizards"]}
    assert "quality_hold_form" in {form["key"] for form in rendered["forms"]}
    assert rendered["runtime_view"]["quarantine"] == 5.0
    assert rendered["binding_evidence"]["outbox_table"] == "inventory_positioning_appgen_outbox_event"


def test_inventory_advanced_stock_intelligence_and_governance_are_executable() -> None:
    service = _prepared_service()
    allocation = service.allocate_inventory(
        {
            "allocation_id": "alloc-route-001",
            "tenant": TENANT,
            "order_id": "order-route-001",
            "item_id": ITEM_ID,
            "quantity": 50.0,
            "demand_class": "standard",
        }
    )
    state = service.state

    transit = runtime.inventory_positioning_project_in_transit(state, item_id=ITEM_ID, quantity=20.0, confidence=0.8, eta_days=3)
    parsed = runtime.inventory_positioning_parse_inventory_event("receipt rcpt_77 sku sku_100 qty 12 node node_east")
    simulation = runtime.inventory_positioning_simulate_allocation_policy(
        state,
        item_id=ITEM_ID,
        requested_quantity=90.0,
        proposed_safety_stock_percent=0.2,
    )
    forecast = runtime.inventory_positioning_forecast_stockout((100.0, 82.0, 60.0), demand_rate=12.0)
    risk = runtime.inventory_positioning_score_stock_risk(state, item_id=ITEM_ID, demand_rate=12.0, spoilage_days=120)
    route = runtime.inventory_positioning_route_allocation(
        allocation["allocation"],
        rails=(
            {"route": "node_api", "available": False, "latency": 2},
            {"route": "outbox", "available": True, "latency": 4},
        ),
    )
    screening = runtime.inventory_positioning_screen_inventory_policy(state, item_id=ITEM_ID, restricted_nodes=("restricted-node",))
    controls = runtime.inventory_positioning_run_control_tests(state)
    federation = runtime.inventory_positioning_federate_inventory_view(state, item_id=ITEM_ID, systems=("warehouse", "commerce"))
    identity = runtime.inventory_positioning_verify_node_identity(state["nodes"][NODE_ID]["identity"])
    resilience = runtime.inventory_positioning_run_resilience_drill(state, "node_unavailable")
    crypto = runtime.inventory_positioning_rotate_crypto_epoch(state, "dilithium3_simulated")
    carbon = runtime.inventory_positioning_schedule_carbon_aware_fulfillment(
        (
            {"node_id": "node-east", "carbon_intensity": 180},
            {"node_id": "node-west", "carbon_intensity": 90},
        )
    )
    optimization = runtime.inventory_positioning_optimize_allocation(
        candidates=(
            {"node_id": "node-east", "available": 88.0, "distance": 20.0, "carbon": 180.0},
            {"node_id": "node-west", "available": 60.0, "distance": 35.0, "carbon": 90.0},
        ),
        quantity=50.0,
    )
    channels = runtime.inventory_positioning_allocate_competing_channels(
        channels=(
            {"channel": "commerce", "bid": 0.8, "priority": 0.7},
            {"channel": "store", "bid": 0.5, "priority": 0.4},
        ),
        quantity=50.0,
    )
    anomaly = runtime.inventory_positioning_detect_inventory_anomaly(state)
    stochastic = runtime.inventory_positioning_model_stochastic_stock_exposure(stock_path=(100.0, 90.0, 70.0), demand_volatility=0.12)
    invariants = runtime.inventory_positioning_verify_formal_invariants(state)
    model = runtime.inventory_positioning_register_governed_model(
        "stockout_risk",
        {"features": ("available", "demand", "age"), "auc": 0.91, "drift_score": 0.04},
    )

    assert transit["expected_quantity"] == 16.0
    assert parsed["ok"] is True and parsed["quantity"] == 12.0
    assert simulation["delta_available"] < 0
    assert forecast["stockout_in_periods"] == 5
    assert risk["risk_score"] > 0
    assert route["route"] == "outbox" and route["failover_used"] is True
    assert screening["decision"] == "clear"
    assert controls["ok"] is True and controls["hash_chain_valid"] is True
    assert federation["systems"] == ("warehouse", "commerce")
    assert identity["ok"] is True
    assert resilience["mode"] == "degraded_node_route"
    assert crypto["epoch"] == 2
    assert carbon["selected_node"] == "node-west"
    assert optimization["selected_node"] == "node-east"
    assert channels["allocations"][0]["quantity"] > channels["allocations"][1]["quantity"]
    assert anomaly["entropy"] >= 0
    assert stochastic["tail_risk"] > stochastic["expected_exposure"]
    assert invariants["ok"] is True
    assert model["ok"] is True and model["governance"]["explainability_required"] is True


def test_inventory_event_handlers_retry_dead_letter_and_boundary_guards() -> None:
    service = _prepared_service()

    processed = service.receive_event(
        {
            "event_id": "order-verified-001",
            "event_type": "OrderVerified",
            "payload": {"tenant": TENANT, "order_id": "order-001", "item_id": ITEM_ID, "quantity": 12.0},
        }
    )
    duplicate = service.receive_event(
        {
            "event_id": "order-verified-001",
            "event_type": "OrderVerified",
            "payload": {"tenant": TENANT, "order_id": "order-001", "item_id": ITEM_ID, "quantity": 12.0},
        }
    )
    retrying = service.receive_event(
        {
            "event_id": "unknown-001",
            "event_type": "UnknownInventoryEvent",
            "payload": {"tenant": TENANT},
        }
    )
    dead_letter = service.receive_event(
        {
            "event_id": "unknown-001",
            "event_type": "UnknownInventoryEvent",
            "payload": {"tenant": TENANT},
        }
    )

    assert processed["handler"]["status"] == "processed"
    assert service.state["order_demand_projections"]["order-001"]["quantity"] == 12.0
    assert duplicate["duplicate"] is True
    assert retrying["handler"]["status"] == "retrying"
    assert dead_letter["handler"]["status"] == "dead_letter"
    assert service.state["dead_letters"][-1]["reason"] == "unsupported_or_failed_inventory_event"

    manifest = service_operation_manifest()
    assert manifest["ok"] is True
    assert manifest["transaction_boundary"] == "owned_datastore_plus_outbox"
    assert "receive_event" in manifest["operations"]
    assert all(contract["event_contract"] == "AppGen-X" for contract in manifest["operation_contracts"])

    boundary = runtime.inventory_positioning_verify_owned_table_boundary(
        (
            "inventory_positioning_inventory_position",
            "OrderVerified",
            "GET /identity/policies",
            "foreign_inventory_table",
        )
    )
    assert boundary["ok"] is False
    assert boundary["violations"] == ("foreign_inventory_table",)

    with pytest.raises(ValueError, match="PostgreSQL, MySQL, or MariaDB"):
        service.configure_runtime({**_configuration(), "database_backend": "sqlite"})
    with pytest.raises(ValueError, match="AppGen-X event contract"):
        service.configure_runtime({**_configuration(), "stream_engine_picker": "user_choice"})
