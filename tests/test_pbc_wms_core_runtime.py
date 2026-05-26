import pytest

from pyAppGen.pbc import WMS_CORE_ADVANCED_CAPABILITY_KEYS
from pyAppGen.pbc import pbc_implemented_capability_audit
from pyAppGen.pbc import pbc_implementation_contract
from pyAppGen.pbc import pbc_implementation_release_audit
from pyAppGen.pbc import wms_core_build_workbench_view
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
from pyAppGen.pbc import wms_core_render_workbench
from pyAppGen.pbc import wms_core_runtime_capabilities
from pyAppGen.pbc import wms_core_runtime_smoke
from pyAppGen.pbc import wms_core_set_parameter
from pyAppGen.pbc import wms_core_ui_contract
from pyAppGen.pbcs.wms_core import WMS_CORE_ALLOWED_DATABASE_BACKENDS
from pyAppGen.pbcs.wms_core import WMS_CORE_CONSUMED_EVENT_TYPES
from pyAppGen.pbcs.wms_core import WMS_CORE_EMITTED_EVENT_TYPES
from pyAppGen.pbcs.wms_core import WMS_CORE_OWNED_TABLES
from pyAppGen.pbcs.wms_core import WMS_CORE_REQUIRED_EVENT_TOPIC
from pyAppGen.pbcs.wms_core import wms_core_build_api_contract
from pyAppGen.pbcs.wms_core import wms_core_build_release_evidence
from pyAppGen.pbcs.wms_core import wms_core_build_schema_contract
from pyAppGen.pbcs.wms_core import wms_core_build_service_contract
from pyAppGen.pbcs.wms_core import wms_core_permissions_contract
from pyAppGen.pbcs.wms_core import wms_core_receive_event
from pyAppGen.pbcs.wms_core import wms_core_register_schema_extension
from pyAppGen.pbcs.wms_core import wms_core_verify_owned_table_boundary


def test_wms_core_runtime_executes_standard_and_advanced_capabilities() -> None:
    runtime = wms_core_runtime_capabilities()
    smoke = wms_core_runtime_smoke()

    assert runtime["format"] == "appgen.wms-core-runtime-capabilities.v1"
    assert runtime["ok"] is True
    assert runtime["implementation_directory"] == "src/pyAppGen/pbcs/wms_core"
    assert len(runtime["owned_tables"]) >= 40
    assert len(runtime["standard_features"]) >= 40
    assert "rule_engine" in runtime["standard_features"]
    assert "parameter_engine" in runtime["standard_features"]
    assert "configuration_schema" in runtime["standard_features"]
    assert "appgen_x_outbox" in runtime["standard_features"]
    assert "retry_dead_letter_evidence" in runtime["standard_features"]
    assert smoke["ok"] is True
    assert set(WMS_CORE_ADVANCED_CAPABILITY_KEYS) == {check["id"] for check in smoke["checks"]}
    assert not smoke["blocking_gaps"]

    contract = pbc_implementation_contract("wms_core")
    assert contract["source_package"]["ok"] is True
    assert contract["advanced_runtime"]["ok"] is True
    assert contract["source_package"]["ui_contract"]["ok"] is True
    assert "WmsConfigurationPanel" in contract["source_package"]["ui_contract"]["fragments"]
    assert set(contract["advanced_runtime"]["capabilities"]) == set(WMS_CORE_ADVANCED_CAPABILITY_KEYS)
    assert contract["source_package"]["api_contract"]["shared_table_access"] is False
    assert contract["source_package"]["api_contract"]["event_contract"] == "AppGen-X"
    assert contract["source_package"]["schema_contract"]["ok"] is True
    assert contract["source_package"]["service_contract"]["ok"] is True
    assert contract["source_package"]["release_evidence_contract"]["ok"] is True
    assert contract["source_package"]["permissions_contract"]["action_permissions"]["receive_event"] == "wms_core.event"
    assert contract["source_package"]["owned_tables"] == WMS_CORE_OWNED_TABLES
    assert contract["source_package"]["allowed_database_backends"] == WMS_CORE_ALLOWED_DATABASE_BACKENDS
    assert contract["source_package"]["required_event_topic"] == WMS_CORE_REQUIRED_EVENT_TOPIC
    assert contract["source_package"]["consumes"] == WMS_CORE_CONSUMED_EVENT_TYPES
    assert contract["source_package"]["emits"] == WMS_CORE_EMITTED_EVENT_TYPES
    assert pbc_implementation_release_audit(("wms_core",))["ok"] is True
    assert pbc_implemented_capability_audit(("wms_core",))["ok"] is True


def test_wms_core_runtime_applies_rules_parameters_and_configuration() -> None:
    state = wms_core_empty_state()
    state = wms_core_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": WMS_CORE_REQUIRED_EVENT_TOPIC,
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

    workbench = wms_core_build_workbench_view(state, tenant="tenant_ops")
    assert workbench["warehouse_count"] == 1
    assert workbench["bin_count"] == 1
    assert workbench["picked_count"] == 1
    assert workbench["packed_count"] == 1
    assert workbench["shipment_count"] == 1
    assert workbench["configuration_bound"] is True
    assert workbench["rule_count"] == 1
    assert workbench["parameter_count"] == 3
    assert workbench["binding_evidence"]["owned_tables"] == WMS_CORE_OWNED_TABLES
    assert workbench["binding_evidence"]["configuration"]["event_contract"] == "AppGen-X"
    assert workbench["binding_evidence"]["configuration"]["event_topic"] == WMS_CORE_REQUIRED_EVENT_TOPIC
    assert workbench["binding_evidence"]["configuration"]["stream_engine_picker_visible"] is False

    ui_contract = wms_core_ui_contract()
    assert ui_contract["configuration_editor"]["allowed_database_backends"] == WMS_CORE_ALLOWED_DATABASE_BACKENDS
    assert ui_contract["configuration_editor"]["fixed_event_topic"] == WMS_CORE_REQUIRED_EVENT_TOPIC
    assert ui_contract["configuration_editor"]["stream_engine_picker_visible"] is False
    assert "bin_capacity_tolerance" in ui_contract["parameter_editor"]["numeric_parameters"]
    assert "rule_id" in ui_contract["rule_editor"]["required_fields"]
    assert ui_contract["event_surfaces"]["emits"] == WMS_CORE_EMITTED_EVENT_TYPES
    assert ui_contract["event_surfaces"]["consumes"] == WMS_CORE_CONSUMED_EVENT_TYPES
    rendered = wms_core_render_workbench(
        state,
        tenant="tenant_ops",
        principal_permissions=(
            "wms_core.master",
            "wms_core.receive",
            "wms_core.putaway",
            "wms_core.pick",
            "wms_core.pack",
            "wms_core.ship",
            "wms_core.edge",
            "wms_core.event",
            "wms_core.audit",
            "wms_core.configure",
        ),
    )
    assert rendered["ok"] is True
    assert rendered["configuration_bound"] is True
    assert rendered["event_outbox_count"] == 10
    assert rendered["event_inbox_count"] == 0
    assert rendered["dead_letter_count"] == 0
    assert rendered["binding_evidence"]["owned_tables"] == WMS_CORE_OWNED_TABLES
    assert set(rendered["visible_actions"]) == set(ui_contract["action_permissions"])
    assert not rendered["locked_actions"]


def test_wms_core_rejects_unsupported_database_backends_and_unknown_parameters() -> None:
    state = wms_core_empty_state()

    with pytest.raises(ValueError, match="PostgreSQL, MySQL, or MariaDB"):
        wms_core_configure_runtime(
            state,
            {
                "database_backend": "stream_store",
                "event_topic": WMS_CORE_REQUIRED_EVENT_TOPIC,
                "retry_limit": 3,
                "timezone": "UTC",
                "label_format": "zpl",
            },
        )

    with pytest.raises(ValueError, match="Unsupported WMS Core parameter"):
        wms_core_set_parameter(state, "stream_engine", "hidden_picker")

    with pytest.raises(ValueError, match="requires AppGen-X event topic"):
        wms_core_configure_runtime(
            state,
            {
                "database_backend": "postgresql",
                "event_topic": "custom.wms.events",
                "retry_limit": 3,
                "timezone": "UTC",
                "label_format": "zpl",
            },
        )

    with pytest.raises(ValueError, match="unsupported eventing fields"):
        wms_core_configure_runtime(
            state,
            {
                "database_backend": "postgresql",
                "event_topic": WMS_CORE_REQUIRED_EVENT_TOPIC,
                "retry_limit": 3,
                "timezone": "UTC",
                "label_format": "zpl",
                "stream_engine_picker": "visible",
            },
        )


def test_wms_core_contracts_events_schema_and_boundaries_are_package_local() -> None:
    state = wms_core_configure_runtime(
        wms_core_empty_state(),
        {
            "database_backend": "mariadb",
            "event_topic": WMS_CORE_REQUIRED_EVENT_TOPIC,
            "retry_limit": 2,
            "timezone": "UTC",
            "label_format": "zpl",
        },
    )["state"]

    extension = wms_core_register_schema_extension(
        state,
        "bin_location",
        {"automation_profile": "jsonb", "slotting_score": "numeric"},
    )
    state = extension["state"]
    assert extension["ok"] is True
    assert state["schema_extensions"]["bin_location"]["slotting_score"] == "numeric"

    with pytest.raises(ValueError, match="owned tables"):
        wms_core_register_schema_extension(state, "inventory_balance", {"foreign_stock": "numeric"})

    invalid = wms_core_register_schema_extension(state, "bin_location", {"BadField": "text"})
    assert invalid["ok"] is False
    assert invalid["error"] == "invalid_extension_field"

    api = wms_core_build_api_contract()
    assert api["format"] == "appgen.wms-core-api-contract.v1"
    assert api["database_backends"] == WMS_CORE_ALLOWED_DATABASE_BACKENDS
    assert api["owned_tables"] == WMS_CORE_OWNED_TABLES
    assert api["events"]["emits"] == WMS_CORE_EMITTED_EVENT_TYPES
    assert api["events"]["consumes"] == WMS_CORE_CONSUMED_EVENT_TYPES
    assert api["shared_table_access"] is False
    assert api["stream_engine_picker_visible"] is False
    assert any(route["command"] == "receive_event" for route in api["routes"])

    schema = wms_core_build_schema_contract()
    service = wms_core_build_service_contract()
    release = wms_core_build_release_evidence()
    assert schema["format"] == "appgen.wms-core-owned-schema-contract.v1"
    assert schema["ok"] is True
    assert len(schema["tables"]) == len(WMS_CORE_OWNED_TABLES)
    assert len(schema["migrations"]) == len(WMS_CORE_OWNED_TABLES)
    assert {
        "warehouse_zone",
        "inbound_receipt_line",
        "pick_exception",
        "shipment_label",
        "wms_governed_model",
    } <= {item["table"] for item in schema["tables"]}
    assert schema["shared_table_access"] is False
    assert service["format"] == "appgen.wms-core-service-contract.v1"
    assert service["ok"] is True
    assert len(service["command_methods"]) >= 30
    assert service["external_dependencies"]["shared_tables"] == ()
    assert release["format"] == "appgen.wms-core-release-evidence.v1"
    assert release["ok"] is True
    assert not release["blocking_gaps"]

    permissions = wms_core_permissions_contract()
    assert permissions["ok"] is True
    assert permissions["action_permissions"]["receive_event"] == "wms_core.event"
    assert "wms_core.configure" in permissions["permissions"]

    processed = wms_core_receive_event(
        state,
        {
            "event_id": "evt_alloc_1",
            "event_type": "InventoryAllocated",
            "payload": {"tenant": "tenant_ops", "allocation_id": "alloc_1", "item_id": "sku_ops", "quantity": 10},
        },
    )
    state = processed["state"]
    assert processed["ok"] is True
    assert state["inventory_allocation_projections"]["alloc_1"]["quantity"] == 10
    duplicate = wms_core_receive_event(
        state,
        {
            "event_id": "evt_alloc_1",
            "event_type": "InventoryAllocated",
            "payload": {"tenant": "tenant_ops", "allocation_id": "alloc_1"},
        },
    )
    assert duplicate["duplicate"] is True
    assert len(duplicate["state"]["inbox"]) == 1

    retry = wms_core_receive_event(
        state,
        {
            "event_id": "evt_bad",
            "event_type": "UnknownWarehouseEvent",
            "payload": {"tenant": "tenant_ops"},
        },
    )
    assert retry["ok"] is False
    assert retry["handler"]["status"] == "retrying"
    dead = wms_core_receive_event(retry["state"], {"event_id": "evt_bad", "event_type": "UnknownWarehouseEvent", "payload": {"tenant": "tenant_ops"}})
    assert dead["handler"]["status"] == "dead_letter"
    assert dead["state"]["dead_letters"][-1]["reason"] == "unsupported_or_failed_wms_event"

    boundary = wms_core_verify_owned_table_boundary(("warehouse", "InventoryAllocated", "inventory_allocation_projection", "wms_core_custom_projection"))
    assert boundary["ok"] is True
    assert boundary["declared_dependencies"]["shared_tables"] == ()
    violation = wms_core_verify_owned_table_boundary(("inventory_balance", "customer_profile"))
    assert violation["ok"] is False
    assert violation["violations"] == ("inventory_balance", "customer_profile")
