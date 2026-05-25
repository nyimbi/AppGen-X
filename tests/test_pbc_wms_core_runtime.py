from pyAppGen.pbc import WMS_CORE_ADVANCED_CAPABILITY_KEYS
from pyAppGen.pbc import pbc_implemented_capability_audit
from pyAppGen.pbc import pbc_implementation_contract
from pyAppGen.pbc import pbc_implementation_release_audit
from pyAppGen.pbc import wms_core_configure_runtime
from pyAppGen.pbc import wms_core_confirm_pack
from pyAppGen.pbc import wms_core_confirm_putaway
from pyAppGen.pbc import wms_core_confirm_shipment
from pyAppGen.pbc import wms_core_create_pack_task
from pyAppGen.pbc import wms_core_create_pick_wave
from pyAppGen.pbc import wms_core_create_putaway_task
from pyAppGen.pbc import wms_core_empty_state
from pyAppGen.pbc import wms_core_execute_pick
from pyAppGen.pbc import wms_core_receive_inbound
from pyAppGen.pbc import wms_core_register_bin
from pyAppGen.pbc import wms_core_register_rule
from pyAppGen.pbc import wms_core_register_warehouse
from pyAppGen.pbc import wms_core_runtime_capabilities
from pyAppGen.pbc import wms_core_runtime_smoke
from pyAppGen.pbc import wms_core_set_parameter


def test_wms_core_runtime_executes_standard_and_advanced_capabilities() -> None:
    runtime = wms_core_runtime_capabilities()
    smoke = wms_core_runtime_smoke()

    assert runtime["format"] == "appgen.wms-core-runtime-capabilities.v1"
    assert runtime["ok"] is True
    assert runtime["implementation_directory"] == "src/pyAppGen/pbcs/wms_core"
    assert len(runtime["standard_features"]) >= 18
    assert "rule_engine" in runtime["standard_features"]
    assert "parameter_engine" in runtime["standard_features"]
    assert "configuration_schema" in runtime["standard_features"]
    assert smoke["ok"] is True
    assert set(WMS_CORE_ADVANCED_CAPABILITY_KEYS) == {check["id"] for check in smoke["checks"]}
    assert not smoke["blocking_gaps"]

    contract = pbc_implementation_contract("wms_core")
    assert contract["source_package"]["ok"] is True
    assert contract["advanced_runtime"]["ok"] is True
    assert set(contract["advanced_runtime"]["capabilities"]) == set(WMS_CORE_ADVANCED_CAPABILITY_KEYS)
    assert pbc_implementation_release_audit(("wms_core",))["ok"] is True
    assert pbc_implemented_capability_audit(("wms_core",))["ok"] is True


def test_wms_core_runtime_applies_rules_parameters_and_configuration() -> None:
    state = wms_core_empty_state()
    state = wms_core_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": "appgen.wms.events",
            "retry_limit": 3,
            "timezone": "UTC",
            "allowed_bin_statuses": ("available", "blocked"),
            "label_format": "zpl",
            "edge_device_mode": "managed",
            "workbench_limit": 50,
        },
    )["state"]
    state = wms_core_set_parameter(state, "bin_capacity_tolerance", 0.9)["state"]
    state = wms_core_set_parameter(state, "pick_wave_size", 1)["state"]
    state = wms_core_set_parameter(state, "partial_pick_threshold", 0.5)["state"]
    state = wms_core_register_rule(
        state,
        {
            "rule_id": "rule_ops",
            "tenant": "tenant_ops",
            "rule_type": "putaway",
            "preferred_zones": ("fast_pick",),
            "pick_method": "wave",
            "pack_material": "carton_small",
            "hazard_compatible": True,
            "status": "active",
        },
    )["state"]
    state = wms_core_register_warehouse(
        state,
        {
            "warehouse_id": "wh_ops",
            "tenant": "tenant_ops",
            "name": "Ops DC",
            "zones": ("fast_pick", "bulk"),
            "dock_doors": ("door_ops",),
            "pack_stations": ("pack_ops",),
            "calendar": "weekday",
            "identity": {"did": "did:appgen:warehouse-ops", "issuer": "trusted_registry", "status": "active"},
        },
    )["state"]
    state = wms_core_register_bin(
        state,
        {
            "bin_id": "bin_ops",
            "tenant": "tenant_ops",
            "warehouse_id": "wh_ops",
            "zone": "fast_pick",
            "capacity": 100,
            "current_load": 10,
            "status": "available",
            "temperature": "ambient",
            "hazard": "none",
            "pick_sequence": 5,
        },
    )["state"]
    state = wms_core_receive_inbound(
        state,
        {
            "receipt_id": "in_ops",
            "tenant": "tenant_ops",
            "warehouse_id": "wh_ops",
            "item_id": "sku_ops",
            "quantity": 50,
            "dock_door": "door_ops",
        },
    )["state"]

    putaway = wms_core_create_putaway_task(state, "in_ops", item_id="sku_ops", quantity=50)
    state = putaway["state"]
    assert putaway["task"]["bin_id"] == "bin_ops"
    assert putaway["confidence"] >= 0.8

    state = wms_core_confirm_putaway(state, putaway["task"]["task_id"], confirmed_by="operator_ops")["state"]
    assert state["bins"]["bin_ops"]["current_load"] == 60

    wave = wms_core_create_pick_wave(
        state,
        {
            "wave_id": "wave_ops",
            "tenant": "tenant_ops",
            "warehouse_id": "wh_ops",
            "orders": (
                {"order_id": "order_ops", "item_id": "sku_ops", "quantity": 10, "priority": "standard"},
                {"order_id": "order_later", "item_id": "sku_ops", "quantity": 10, "priority": "standard"},
            ),
        },
    )
    state = wave["state"]
    assert len(wave["wave"]["orders"]) == 1

    pick = wms_core_execute_pick(state, "wave_ops", "order_ops", picked_quantity=10, operator="picker_ops")
    state = pick["state"]
    assert pick["pick"]["status"] == "picked"

    state = wms_core_create_pack_task(state, "pack_ops", order_id="order_ops", weight=5, dimensions=(10, 8, 4))["state"]
    state = wms_core_confirm_pack(state, "pack_ops", station="pack_ops", label_id="lbl_ops")["state"]
    shipped = wms_core_confirm_shipment(state, "ship_ops", order_id="order_ops", carrier="carrier_ops", dock_door="door_ops")
    state = shipped["state"]
    assert state["outbox"][-1]["idempotency_key"] == "wms_core:OrderShipped:wms_evt_000010"
    assert shipped["shipment"]["status"] == "shipped"
