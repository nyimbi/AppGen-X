"""Executable domain behavior tests for the wms_core PBC."""

from __future__ import annotations

import pytest

from .. import runtime
from .. import ui
from ..services import StatefulWmsCoreService
from ..services import runtime_service_manifest
from ..services import service_operation_manifest


TENANT = "tenant_wms"
WAREHOUSE_ID = "wh-east"
BIN_ID = "bin-fast-1"
ITEM_ID = "sku-100"


def _configuration() -> dict:
    return {
        "database_backend": "postgresql",
        "event_topic": runtime.WMS_CORE_REQUIRED_EVENT_TOPIC,
        "retry_limit": 2,
        "timezone": "UTC",
        "allowed_bin_statuses": ("available", "blocked", "maintenance"),
        "label_format": "zpl",
        "edge_device_mode": "managed",
        "workbench_limit": 100,
    }


def _prepared_service(*, ship: bool = False) -> StatefulWmsCoreService:
    service = StatefulWmsCoreService()
    service.configure_runtime(_configuration())
    service.set_parameter({"name": "bin_capacity_tolerance", "value": 0.95})
    service.set_parameter({"name": "pick_wave_size", "value": 20})
    service.set_parameter({"name": "partial_pick_threshold", "value": 0.5})
    service.set_parameter({"name": "dock_queue_warning", "value": 4})
    service.register_rule(
        {
            "rule_id": "rule_fast_putaway",
            "tenant": TENANT,
            "scope": "putaway",
            "preferred_zones": ("fast_pick", "bulk"),
            "pick_method": "wave",
            "pack_material": "carton_small",
            "hazard_compatible": True,
            "status": "active",
        }
    )
    service.register_schema_extension({"table": "bin_location", "fields": {"automation_profile": "jsonb"}})
    service.register_warehouse(
        {
            "warehouse_id": WAREHOUSE_ID,
            "tenant": TENANT,
            "name": "East DC",
            "zones": ("fast_pick", "bulk", "dock"),
            "dock_doors": ("door-1", "door-2"),
            "pack_stations": ("pack-1",),
            "calendar": "weekday",
            "identity": {"did": "did:appgen:warehouse-east", "issuer": "trusted_registry", "status": "active"},
        }
    )
    service.register_bin(
        {
            "bin_id": BIN_ID,
            "tenant": TENANT,
            "warehouse_id": WAREHOUSE_ID,
            "zone": "fast_pick",
            "capacity": 100.0,
            "current_load": 20.0,
            "status": "available",
            "temperature": "ambient",
            "hazard": "none",
            "pick_sequence": 10,
        }
    )
    service.receive_inbound(
        {
            "receipt_id": "in-001",
            "tenant": TENANT,
            "warehouse_id": WAREHOUSE_ID,
            "item_id": ITEM_ID,
            "quantity": 60.0,
            "dock_door": "door-1",
        }
    )
    putaway = service.create_putaway_task({"receipt_id": "in-001", "item_id": ITEM_ID, "quantity": 60.0})
    service.confirm_putaway({"task_id": putaway["task"]["task_id"], "confirmed_by": "operator-1"})
    service.create_pick_wave(
        {
            "wave_id": "wave-001",
            "tenant": TENANT,
            "warehouse_id": WAREHOUSE_ID,
            "orders": ({"order_id": "order-001", "item_id": ITEM_ID, "quantity": 20.0, "priority": "standard"},),
        }
    )
    service.execute_pick(
        {
            "wave_id": "wave-001",
            "order_id": "order-001",
            "picked_quantity": 20.0,
            "operator": "picker-1",
        }
    )
    service.create_pack_task({"pack_id": "pack-001", "order_id": "order-001", "weight": 8.0, "dimensions": (10, 8, 4)})
    service.confirm_pack({"pack_id": "pack-001", "station": "pack-1", "label_id": "lbl-001"})
    if ship:
        service.confirm_shipment({"shipment_id": "ship-001", "order_id": "order-001", "carrier": "carrier-a", "dock_door": "door-2"})
    return service


def test_wms_inbound_putaway_pick_pack_ship_lifecycle_is_runtime_backed() -> None:
    service = _prepared_service(ship=True)

    workbench = service.build_workbench_view({"tenant": TENANT})
    assert workbench["warehouse_count"] == 1
    assert workbench["bin_count"] == 1
    assert workbench["putaway_count"] == 1
    assert workbench["wave_count"] == 1
    assert workbench["picked_count"] == 1
    assert workbench["packed_count"] == 1
    assert workbench["shipment_count"] == 1
    assert workbench["event_contract"] == "AppGen-X"

    bin_location = service.state["bins"][BIN_ID]
    assert bin_location["current_load"] == 80.0
    assert service.state["putaway_tasks"]["putaway_in-001"]["status"] == "confirmed"
    assert service.state["picks"]["pick_wave-001_order-001"]["status"] == "picked"
    assert service.state["pack_tasks"]["pack-001"]["material"] == "carton_small"
    assert service.state["shipments"]["ship-001"]["status"] == "shipped"

    event_types = tuple(event["event_type"] for event in service.state["events"])
    assert event_types == (
        "WarehouseRegistered",
        "BinRegistered",
        "GoodsReceiptPosted",
        "PutawayTaskCreated",
        "PutawayConfirmed",
        "PickWaveReleased",
        "Picked",
        "PackTaskCreated",
        "Packed",
        "OrderShipped",
    )
    assert all(event["idempotency_key"].startswith("wms_core:") for event in service.state["outbox"])


def test_wms_replenishment_shipment_proof_and_ui_workbench_are_bound() -> None:
    service = _prepared_service(ship=True)

    replenishment = service.recommend_replenishment({"bin_id": BIN_ID, "minimum": 50.0, "forward_pick_demand": 40.0})
    proof = service.generate_shipment_proof({"shipment_id": "ship-001", "disclosure": ("shipment_id", "order_id", "carrier")})
    permissions = tuple(sorted(set(ui.wms_core_ui_contract()["action_permissions"].values())))
    rendered = ui.wms_core_render_workbench(service.state, tenant=TENANT, principal_permissions=permissions)

    assert replenishment["recommended_quantity"] == 10.0
    assert proof["proof"].startswith("zk_ship_")
    assert proof["public_claims"] == {"shipment_id": "ship-001", "order_id": "order-001", "carrier": "carrier-a"}
    assert rendered["ok"] is True
    assert "WarehouseExecutionWorkbench" in rendered["fragments"]
    assert "wave_to_ship_wizard" in {wizard["key"] for wizard in rendered["wizards"]}
    assert "pack_confirmation_form" in {form["key"] for form in rendered["forms"]}
    assert rendered["event_outbox_count"] == 10
    assert rendered["binding_evidence"]["outbox_table"] == "wms_core_appgen_outbox_event"
    assert rendered["binding_evidence"]["configuration"]["stream_engine_picker_visible"] is False


def test_wms_advanced_execution_intelligence_and_governance_are_executable() -> None:
    service = _prepared_service(ship=True)
    state = service.state

    parsed = runtime.wms_core_parse_warehouse_event("receipt in_777 sku sku_100 qty 12 dock door_1")
    simulation = runtime.wms_core_simulate_wave_policy(state, orders=12, proposed_wave_size=6)
    forecast = runtime.wms_core_forecast_throughput((40.0, 45.0, 50.0), labor_hours=6.0)
    risk = runtime.wms_core_score_congestion_risk(state, dock_queue=2, active_waves=1)
    resolution = runtime.wms_core_recommend_exception_resolution("short_pick")
    route = runtime.wms_core_route_edge_command(
        {"command_id": "cmd-001", "kind": "print_label"},
        rails=(
            {"route": "printer_direct", "available": False, "latency": 1},
            {"route": "edge_outbox", "available": True, "latency": 3},
        ),
    )
    screening = runtime.wms_core_screen_warehouse_policy(state, bin_id=BIN_ID, restricted_bins=("restricted-bin",))
    controls = runtime.wms_core_run_control_tests(state)
    federation = runtime.wms_core_federate_warehouse_view(state, WAREHOUSE_ID, systems=("inventory", "transportation", "quality"))
    identity = runtime.wms_core_verify_warehouse_identity(state["warehouses"][WAREHOUSE_ID]["identity"])
    resilience = runtime.wms_core_run_resilience_drill(state, "printer_unavailable")
    crypto = runtime.wms_core_rotate_crypto_epoch(state, "dilithium3_simulated")
    carbon = runtime.wms_core_schedule_carbon_aware_wave(
        ({"window": "09:00", "carbon_intensity": 240}, {"window": "02:00", "carbon_intensity": 110})
    )
    path = runtime.wms_core_optimize_pick_path(
        ({"bin_id": BIN_ID, "sequence": 10}, {"bin_id": "bin-bulk-1", "sequence": 30}),
        start_sequence=0,
    )
    labor = runtime.wms_core_allocate_labor_tasks(
        workers=({"worker": "picker-1", "bid": 0.8, "skill": 0.9}, {"worker": "picker-2", "bid": 0.6, "skill": 0.5}),
        tasks=10,
    )
    anomaly = runtime.wms_core_detect_warehouse_anomaly(state)
    stochastic = runtime.wms_core_model_stochastic_throughput(throughput_path=(40.0, 42.0, 50.0), volatility=0.08)
    invariants = runtime.wms_core_verify_formal_invariants(state)
    model = runtime.wms_core_register_governed_model(
        "wms_risk",
        {"features": ("dock_queue", "waves", "exceptions"), "auc": 0.9, "drift_score": 0.04},
    )

    assert parsed["ok"] is True and parsed["quantity"] == 12.0
    assert simulation["waves_required"] == 2
    assert forecast["units_per_labor_hour"] == 22.5
    assert risk["decision"] == "monitor"
    assert resolution["action"] == "replenish_forward_pick"
    assert route["route"] == "edge_outbox" and route["failover_used"] is True
    assert screening["decision"] == "clear"
    assert controls["ok"] is True and controls["hash_chain_valid"] is True
    assert federation["systems"] == ("inventory", "transportation", "quality")
    assert identity["ok"] is True
    assert resilience["mode"] == "degraded_edge_route"
    assert crypto["epoch"] == 2
    assert carbon["selected_window"] == "02:00"
    assert path["path"] == (BIN_ID, "bin-bulk-1")
    assert labor["allocations"][0]["tasks"] > labor["allocations"][1]["tasks"]
    assert anomaly["entropy"] >= 0
    assert stochastic["tail_risk"] > stochastic["expected_exposure"]
    assert invariants["ok"] is True
    assert model["ok"] is True and model["governance"]["regulated"] is True


def test_wms_event_handlers_retry_dead_letter_service_and_boundary_guards() -> None:
    service = _prepared_service()

    processed = service.receive_event(
        {
            "event_id": "alloc-evt-001",
            "event_type": "InventoryAllocated",
            "payload": {"tenant": TENANT, "allocation_id": "alloc-001", "item_id": ITEM_ID, "quantity": 20.0},
        }
    )
    duplicate = service.receive_event(
        {
            "event_id": "alloc-evt-001",
            "event_type": "InventoryAllocated",
            "payload": {"tenant": TENANT, "allocation_id": "alloc-001", "item_id": ITEM_ID, "quantity": 20.0},
        }
    )
    retrying = service.receive_event({"event_id": "bad-evt-001", "event_type": "UnknownWmsEvent", "payload": {"tenant": TENANT}})
    dead_letter = service.receive_event({"event_id": "bad-evt-001", "event_type": "UnknownWmsEvent", "payload": {"tenant": TENANT}})

    assert processed["handler"]["status"] == "processed"
    assert service.state["inventory_allocation_projections"]["alloc-001"]["quantity"] == 20.0
    assert duplicate["duplicate"] is True
    assert retrying["handler"]["status"] == "retrying"
    assert dead_letter["handler"]["status"] == "dead_letter"
    assert service.state["dead_letters"][-1]["reason"] == "unsupported_or_failed_wms_event"

    runtime_manifest = runtime_service_manifest()
    generated_manifest = service_operation_manifest()
    assert runtime_manifest["ok"] is True
    assert runtime_manifest["service_class"] == "StatefulWmsCoreService"
    assert runtime_manifest["event_contract"] == "AppGen-X"
    assert generated_manifest["ok"] is True
    assert all(contract["event_contract"] == "AppGen-X" for contract in generated_manifest["operation_contracts"])

    boundary = runtime.wms_core_verify_owned_table_boundary(
        ("warehouse", "InventoryAllocated", "GET /inventory/allocations/{id}", "foreign_wms_table")
    )
    assert boundary["ok"] is False
    assert boundary["violations"] == ("foreign_wms_table",)

    with pytest.raises(ValueError, match="PostgreSQL, MySQL, or MariaDB"):
        service.configure_runtime({**_configuration(), "database_backend": "sqlite"})
    with pytest.raises(ValueError, match="AppGen-X event contract"):
        service.configure_runtime({**_configuration(), "stream_engine_picker": "user_choice"})
