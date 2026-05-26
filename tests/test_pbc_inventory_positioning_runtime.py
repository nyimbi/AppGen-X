import pytest

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
from pyAppGen.pbc import inventory_positioning_render_workbench
from pyAppGen.pbc import inventory_positioning_release_allocation
from pyAppGen.pbc import inventory_positioning_runtime_capabilities
from pyAppGen.pbc import inventory_positioning_runtime_smoke
from pyAppGen.pbc import inventory_positioning_set_parameter
from pyAppGen.pbc import inventory_positioning_ui_contract
from pyAppGen.pbc import pbc_implemented_capability_audit
from pyAppGen.pbc import pbc_implementation_contract
from pyAppGen.pbc import pbc_implementation_release_audit
from pyAppGen.pbcs.inventory_positioning import INVENTORY_POSITIONING_ALLOWED_DATABASE_BACKENDS
from pyAppGen.pbcs.inventory_positioning import INVENTORY_POSITIONING_CONSUMED_EVENT_TYPES
from pyAppGen.pbcs.inventory_positioning import INVENTORY_POSITIONING_EMITTED_EVENT_TYPES
from pyAppGen.pbcs.inventory_positioning import INVENTORY_POSITIONING_OWNED_TABLES
from pyAppGen.pbcs.inventory_positioning import INVENTORY_POSITIONING_REQUIRED_EVENT_TOPIC
from pyAppGen.pbcs.inventory_positioning import implementation_contract as inventory_positioning_package_contract
from pyAppGen.pbcs.inventory_positioning import inventory_positioning_build_api_contract
from pyAppGen.pbcs.inventory_positioning import inventory_positioning_permissions_contract
from pyAppGen.pbcs.inventory_positioning import inventory_positioning_receive_event
from pyAppGen.pbcs.inventory_positioning import inventory_positioning_register_schema_extension
from pyAppGen.pbcs.inventory_positioning import inventory_positioning_verify_owned_table_boundary


def test_inventory_positioning_runtime_executes_standard_and_advanced_capabilities() -> None:
    runtime = inventory_positioning_runtime_capabilities()
    smoke = inventory_positioning_runtime_smoke()

    assert runtime["format"] == "appgen.inventory-positioning-runtime-capabilities.v1"
    assert runtime["ok"] is True
    assert runtime["implementation_directory"] == "src/pyAppGen/pbcs/inventory_positioning"
    assert runtime["owned_tables"] == INVENTORY_POSITIONING_OWNED_TABLES
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
    assert contract["source_package"]["ui_contract"]["ok"] is True
    assert "InventoryConfigurationPanel" in contract["source_package"]["ui_contract"]["fragments"]
    assert set(contract["advanced_runtime"]["capabilities"]) == set(INVENTORY_POSITIONING_ADVANCED_CAPABILITY_KEYS)

    package_contract = inventory_positioning_package_contract()
    assert package_contract["api_contract"]["event_contract"] == "AppGen-X"
    assert package_contract["permissions_contract"]["action_permissions"]["receive_event"] == "inventory_positioning.event"
    assert package_contract["owned_tables"] == INVENTORY_POSITIONING_OWNED_TABLES
    assert package_contract["allowed_database_backends"] == INVENTORY_POSITIONING_ALLOWED_DATABASE_BACKENDS
    assert pbc_implementation_release_audit(("inventory_positioning",))["ok"] is True
    assert pbc_implemented_capability_audit(("inventory_positioning",))["ok"] is True


def test_inventory_positioning_runtime_applies_rules_parameters_and_configuration() -> None:
    state = inventory_positioning_empty_state()
    state = inventory_positioning_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": INVENTORY_POSITIONING_REQUIRED_EVENT_TOPIC,
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
    assert workbench["configuration_bound"] is True
    assert workbench["rule_count"] == 1
    assert workbench["parameter_count"] == 2
    assert workbench["owned_tables"] == INVENTORY_POSITIONING_OWNED_TABLES
    assert workbench["inbox_table"] == "inventory_positioning_appgen_inbox_event"

    ui_contract = inventory_positioning_ui_contract()
    assert ui_contract["configuration_editor"]["allowed_database_backends"] == INVENTORY_POSITIONING_ALLOWED_DATABASE_BACKENDS
    assert ui_contract["configuration_editor"]["required_event_topic"] == INVENTORY_POSITIONING_REQUIRED_EVENT_TOPIC
    assert ui_contract["configuration_editor"]["stream_engine_picker_visible"] is False
    assert ui_contract["event_surfaces"]["emits"] == INVENTORY_POSITIONING_EMITTED_EVENT_TYPES
    assert ui_contract["event_surfaces"]["consumes"] == INVENTORY_POSITIONING_CONSUMED_EVENT_TYPES
    assert ui_contract["binding_evidence"]["shared_table_access"] is False
    assert "safety_stock_percent" in ui_contract["parameter_editor"]["numeric_parameters"]
    assert "rule_id" in ui_contract["rule_editor"]["required_fields"]
    rendered = inventory_positioning_render_workbench(
        state,
        tenant="tenant_ops",
        principal_permissions=(
            "inventory_positioning.master",
            "inventory_positioning.receive",
            "inventory_positioning.adjust",
            "inventory_positioning.read",
            "inventory_positioning.allocate",
            "inventory_positioning.release",
            "inventory_positioning.quality",
            "inventory_positioning.reconcile",
            "inventory_positioning.event",
            "inventory_positioning.replenish",
            "inventory_positioning.audit",
            "inventory_positioning.configure",
        ),
    )
    assert rendered["ok"] is True
    assert rendered["configuration_bound"] is True
    assert rendered["event_outbox_count"] == 5
    assert rendered["inbox_count"] == 0
    assert rendered["dead_letter_count"] == 0
    assert rendered["binding_evidence"]["owned_tables"] == INVENTORY_POSITIONING_OWNED_TABLES
    assert set(rendered["visible_actions"]) == set(ui_contract["action_permissions"])
    assert not rendered["locked_actions"]


def test_inventory_positioning_rejects_unsupported_database_backends_and_unknown_parameters() -> None:
    state = inventory_positioning_empty_state()

    with pytest.raises(ValueError, match="PostgreSQL, MySQL, or MariaDB"):
        inventory_positioning_configure_runtime(
            state,
            {
                "database_backend": "stream_store",
                "event_topic": INVENTORY_POSITIONING_REQUIRED_EVENT_TOPIC,
                "retry_limit": 3,
                "default_uom": "EA",
                "precision": 2,
            },
        )

    with pytest.raises(ValueError, match="Unsupported Inventory Positioning parameter"):
        inventory_positioning_set_parameter(state, "stream_engine", "hidden_picker")

    with pytest.raises(ValueError, match=INVENTORY_POSITIONING_REQUIRED_EVENT_TOPIC):
        inventory_positioning_configure_runtime(
            state,
            {
                "database_backend": "postgresql",
                "event_topic": "appgen.inventory.custom",
                "retry_limit": 3,
                "default_uom": "EA",
                "precision": 2,
            },
        )

    with pytest.raises(ValueError, match="unsupported eventing fields"):
        inventory_positioning_configure_runtime(
            state,
            {
                "database_backend": "postgresql",
                "event_topic": INVENTORY_POSITIONING_REQUIRED_EVENT_TOPIC,
                "retry_limit": 3,
                "default_uom": "EA",
                "precision": 2,
                "stream_engine": "user_picker",
            },
        )


def test_inventory_positioning_hardened_contract_handles_schema_events_and_boundaries() -> None:
    state = inventory_positioning_empty_state()
    state = inventory_positioning_configure_runtime(
        state,
        {
            "database_backend": "mariadb",
            "event_topic": INVENTORY_POSITIONING_REQUIRED_EVENT_TOPIC,
            "retry_limit": 2,
            "default_uom": "EA",
            "precision": 2,
            "allowed_statuses": ("available", "reserved", "quarantine"),
        },
    )["state"]

    extension = inventory_positioning_register_schema_extension(
        state,
        "inventory_positioning_inventory_position",
        {"temperature_band": "jsonb", "confidence": "decimal"},
    )
    assert extension["ok"] is True
    state = extension["state"]
    assert state["schema_extensions"]["inventory_positioning_inventory_position"]["temperature_band"] == "jsonb"

    with pytest.raises(ValueError, match="owned tables"):
        inventory_positioning_register_schema_extension(state, "wms_inventory", {"external_field": "text"})

    invalid = inventory_positioning_register_schema_extension(state, "inventory_positioning_inventory_position", {"BadField": "text"})
    assert invalid["ok"] is False
    assert invalid["error"] == "invalid_extension_field"

    event = {
        "event_id": "evt_order_001",
        "event_type": "OrderVerified",
        "payload": {"tenant": "tenant_ops", "order_id": "order_ops", "item_id": "sku_ops", "quantity": 20},
    }
    received = inventory_positioning_receive_event(state, event)
    assert received["ok"] is True
    assert received["handler"]["status"] == "processed"
    state = received["state"]
    assert state["order_demand_projections"]["order_ops"]["quantity"] == 20
    assert len(state["inbox"]) == 1

    duplicate = inventory_positioning_receive_event(state, event)
    assert duplicate["ok"] is True
    assert duplicate["duplicate"] is True
    assert duplicate["state"] is state

    failed = inventory_positioning_receive_event(
        state,
        {"event_id": "evt_bad_001", "event_type": "UnsupportedEvent", "payload": {"tenant": "tenant_ops"}},
    )
    assert failed["ok"] is False
    assert failed["handler"]["status"] == "retrying"
    failed = inventory_positioning_receive_event(
        failed["state"],
        {"event_id": "evt_bad_001", "event_type": "UnsupportedEvent", "payload": {"tenant": "tenant_ops"}},
    )
    assert failed["handler"]["status"] == "dead_letter"
    assert failed["state"]["dead_letter"][0]["reason"] == "unsupported_or_failed_inventory_event"

    api = inventory_positioning_build_api_contract()
    assert api["event_contract"] == "AppGen-X"
    assert api["stream_engine_picker_visible"] is False
    assert api["shared_table_access"] is False
    assert api["database_backends"] == INVENTORY_POSITIONING_ALLOWED_DATABASE_BACKENDS
    assert api["emits"] == INVENTORY_POSITIONING_EMITTED_EVENT_TYPES
    assert api["consumes"] == INVENTORY_POSITIONING_CONSUMED_EVENT_TYPES
    assert any(route.get("command") == "receive_event" for route in api["routes"])

    permissions = inventory_positioning_permissions_contract()
    assert permissions["action_permissions"]["register_schema_extension"] == "inventory_positioning.configure"
    assert permissions["action_permissions"]["receive_event"] == "inventory_positioning.event"

    valid_boundary = inventory_positioning_verify_owned_table_boundary(
        ("inventory_positioning_inventory_position", "inventory_positioning_appgen_outbox_event", "OrderVerified", "demand_forecast_projection")
    )
    assert valid_boundary["ok"] is True
    invalid_boundary = inventory_positioning_verify_owned_table_boundary(("gl_journal_entry",))
    assert invalid_boundary["ok"] is False
    assert invalid_boundary["violations"] == ("gl_journal_entry",)
