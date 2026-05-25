from pyAppGen.pbc import INVENTORY_POSITIONING_ADVANCED_CAPABILITY_KEYS
from pyAppGen.pbc import inventory_positioning_allocate_inventory
from pyAppGen.pbc import inventory_positioning_build_workbench_view
from pyAppGen.pbc import inventory_positioning_calculate_availability
from pyAppGen.pbc import inventory_positioning_configure_runtime
from pyAppGen.pbc import inventory_positioning_empty_state
from pyAppGen.pbc import inventory_positioning_post_goods_receipt
from pyAppGen.pbc import inventory_positioning_register_item
from pyAppGen.pbc import inventory_positioning_register_node
from pyAppGen.pbc import inventory_positioning_register_rule
from pyAppGen.pbc import inventory_positioning_release_allocation
from pyAppGen.pbc import inventory_positioning_runtime_capabilities
from pyAppGen.pbc import inventory_positioning_runtime_smoke
from pyAppGen.pbc import inventory_positioning_set_parameter
from pyAppGen.pbc import pbc_implemented_capability_audit
from pyAppGen.pbc import pbc_implementation_contract
from pyAppGen.pbc import pbc_implementation_release_audit


def test_inventory_positioning_runtime_executes_standard_and_advanced_capabilities() -> None:
    runtime = inventory_positioning_runtime_capabilities()
    smoke = inventory_positioning_runtime_smoke()

    assert runtime["format"] == "appgen.inventory-positioning-runtime-capabilities.v1"
    assert runtime["ok"] is True
    assert runtime["implementation_directory"] == "src/pyAppGen/pbcs/inventory_positioning"
    assert len(runtime["standard_features"]) >= 18
    assert "rule_engine" in runtime["standard_features"]
    assert "parameter_engine" in runtime["standard_features"]
    assert "configuration_schema" in runtime["standard_features"]
    assert smoke["ok"] is True
    assert set(INVENTORY_POSITIONING_ADVANCED_CAPABILITY_KEYS) == {check["id"] for check in smoke["checks"]}
    assert not smoke["blocking_gaps"]

    contract = pbc_implementation_contract("inventory_positioning")
    assert contract["source_package"]["ok"] is True
    assert contract["advanced_runtime"]["ok"] is True
    assert set(contract["advanced_runtime"]["capabilities"]) == set(INVENTORY_POSITIONING_ADVANCED_CAPABILITY_KEYS)
    assert pbc_implementation_release_audit(("inventory_positioning",))["ok"] is True
    assert pbc_implemented_capability_audit(("inventory_positioning",))["ok"] is True


def test_inventory_positioning_runtime_applies_rules_parameters_and_configuration() -> None:
    state = inventory_positioning_empty_state()
    state = inventory_positioning_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": "appgen.inventory.events",
            "retry_limit": 3,
            "default_uom": "EA",
            "precision": 2,
            "allowed_statuses": ("available", "reserved", "quarantine"),
            "workbench_limit": 50,
        },
    )["state"]
    state = inventory_positioning_set_parameter(state, "safety_stock_percent", 0.2)["state"]
    state = inventory_positioning_set_parameter(state, "partial_allocation_threshold", 0.5)["state"]
    state = inventory_positioning_register_rule(
        state,
        {
            "rule_id": "rule_priority",
            "tenant": "tenant_ops",
            "rule_type": "allocation",
            "priority": ("high", "standard"),
            "node_preference": ("node_ops",),
            "allow_partial": True,
            "prevent_negative": True,
            "lot_policy": "fifo",
            "status": "active",
        },
    )["state"]
    state = inventory_positioning_register_item(
        state,
        {
            "item_id": "sku_ops",
            "tenant": "tenant_ops",
            "sku": "SKU-OPS",
            "uom": "EA",
            "lot_tracked": True,
            "serial_tracked": False,
            "shelf_life_days": 120,
            "substitution_group": "ops_group",
            "identity": {"did": "did:appgen:item-ops", "issuer": "trusted_registry", "status": "active"},
        },
    )["state"]
    state = inventory_positioning_register_node(
        state,
        {
            "node_id": "node_ops",
            "tenant": "tenant_ops",
            "node_type": "warehouse",
            "country": "US",
            "region": "CENTRAL",
            "calendar": "weekday",
            "carbon_intensity": 120,
            "identity": {"did": "did:appgen:node-ops", "issuer": "trusted_registry", "status": "active"},
        },
    )["state"]
    state = inventory_positioning_post_goods_receipt(
        state,
        {
            "receipt_id": "rcpt_ops",
            "tenant": "tenant_ops",
            "node_id": "node_ops",
            "item_id": "sku_ops",
            "quantity": 100,
            "lot_id": "lot_ops",
            "expires": "2026-12-31",
        },
    )["state"]

    availability = inventory_positioning_calculate_availability(
        state,
        item_id="sku_ops",
        tenant="tenant_ops",
        demand_class="standard",
    )
    assert availability["on_hand"] == 100
    assert availability["safety_stock"] == 20
    assert availability["available_to_promise"] == 80

    allocation = inventory_positioning_allocate_inventory(
        state,
        {
            "allocation_id": "alloc_ops",
            "tenant": "tenant_ops",
            "order_id": "order_ops",
            "item_id": "sku_ops",
            "quantity": 60,
            "demand_class": "standard",
        },
    )
    state = allocation["state"]
    assert allocation["allocation"]["quantity_allocated"] == 60
    assert state["outbox"][-1]["idempotency_key"] == "inventory_positioning:InventoryAllocated:inventory_evt_000004"

    release = inventory_positioning_release_allocation(state, "alloc_ops", reason="customer_change")
    state = release["state"]
    assert release["allocation"]["status"] == "released"

    workbench = inventory_positioning_build_workbench_view(state, tenant="tenant_ops")
    assert workbench["item_count"] == 1
    assert workbench["node_count"] == 1
    assert workbench["on_hand"] == 100
    assert workbench["reserved"] == 0
