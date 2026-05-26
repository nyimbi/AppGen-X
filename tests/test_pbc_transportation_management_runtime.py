import pytest

from pyAppGen.pbc import TRANSPORTATION_MANAGEMENT_ADVANCED_CAPABILITY_KEYS
from pyAppGen.pbc import pbc_implemented_capability_audit
from pyAppGen.pbc import pbc_implementation_contract
from pyAppGen.pbc import pbc_implementation_release_audit
from pyAppGen.pbc import transportation_management_calculate_eta
from pyAppGen.pbc import transportation_management_build_workbench_view
from pyAppGen.pbc import transportation_management_configure_runtime
from pyAppGen.pbc import transportation_management_confirm_delivery
from pyAppGen.pbc import transportation_management_create_shipment
from pyAppGen.pbc import transportation_management_dispatch_shipment
from pyAppGen.pbc import transportation_management_empty_state
from pyAppGen.pbc import transportation_management_plan_route
from pyAppGen.pbc import transportation_management_record_tracking_event
from pyAppGen.pbc import transportation_management_register_carrier
from pyAppGen.pbc import transportation_management_register_rule
from pyAppGen.pbc import transportation_management_render_workbench
from pyAppGen.pbc import transportation_management_runtime_capabilities
from pyAppGen.pbc import transportation_management_runtime_smoke
from pyAppGen.pbc import transportation_management_select_carrier
from pyAppGen.pbc import transportation_management_set_parameter
from pyAppGen.pbc import transportation_management_ui_contract
from pyAppGen.pbcs.transportation_management import TRANSPORTATION_MANAGEMENT_ALLOWED_DATABASE_BACKENDS
from pyAppGen.pbcs.transportation_management import TRANSPORTATION_MANAGEMENT_CONSUMED_EVENT_TYPES
from pyAppGen.pbcs.transportation_management import TRANSPORTATION_MANAGEMENT_EMITTED_EVENT_TYPES
from pyAppGen.pbcs.transportation_management import TRANSPORTATION_MANAGEMENT_OWNED_TABLES
from pyAppGen.pbcs.transportation_management import TRANSPORTATION_MANAGEMENT_REQUIRED_EVENT_TOPIC
from pyAppGen.pbcs.transportation_management import transportation_management_build_api_contract
from pyAppGen.pbcs.transportation_management import transportation_management_build_release_evidence
from pyAppGen.pbcs.transportation_management import transportation_management_build_schema_contract
from pyAppGen.pbcs.transportation_management import transportation_management_build_service_contract
from pyAppGen.pbcs.transportation_management import transportation_management_permissions_contract
from pyAppGen.pbcs.transportation_management import transportation_management_receive_event
from pyAppGen.pbcs.transportation_management import transportation_management_register_schema_extension
from pyAppGen.pbcs.transportation_management import transportation_management_verify_owned_table_boundary


def test_transportation_management_runtime_executes_standard_and_advanced_capabilities() -> None:
    runtime = transportation_management_runtime_capabilities()
    smoke = transportation_management_runtime_smoke()

    assert runtime["format"] == "appgen.transportation-management-runtime-capabilities.v1"
    assert runtime["ok"] is True
    assert runtime["implementation_directory"] == "src/pyAppGen/pbcs/transportation_management"
    assert len(runtime["owned_tables"]) >= 40
    assert len(runtime["standard_features"]) >= 40
    assert "rule_engine" in runtime["standard_features"]
    assert "parameter_engine" in runtime["standard_features"]
    assert "configuration_schema" in runtime["standard_features"]
    assert "appgen_x_outbox" in runtime["standard_features"]
    assert "retry_dead_letter_evidence" in runtime["standard_features"]
    assert smoke["ok"] is True
    assert set(TRANSPORTATION_MANAGEMENT_ADVANCED_CAPABILITY_KEYS) == {check["id"] for check in smoke["checks"]}
    assert not smoke["blocking_gaps"]

    contract = pbc_implementation_contract("transportation_management")
    assert contract["source_package"]["ok"] is True
    assert contract["advanced_runtime"]["ok"] is True
    assert contract["source_package"]["ui_contract"]["ok"] is True
    assert "TransportationConfigurationPanel" in contract["source_package"]["ui_contract"]["fragments"]
    assert set(contract["advanced_runtime"]["capabilities"]) == set(TRANSPORTATION_MANAGEMENT_ADVANCED_CAPABILITY_KEYS)
    assert contract["source_package"]["api_contract"]["shared_table_access"] is False
    assert contract["source_package"]["api_contract"]["event_contract"] == "AppGen-X"
    assert contract["source_package"]["schema_contract"]["ok"] is True
    assert contract["source_package"]["service_contract"]["ok"] is True
    assert contract["source_package"]["release_evidence_contract"]["ok"] is True
    assert contract["source_package"]["permissions_contract"]["action_permissions"]["receive_event"] == "transportation_management.event"
    assert contract["source_package"]["owned_tables"] == TRANSPORTATION_MANAGEMENT_OWNED_TABLES
    assert contract["source_package"]["allowed_database_backends"] == TRANSPORTATION_MANAGEMENT_ALLOWED_DATABASE_BACKENDS
    assert contract["source_package"]["required_event_topic"] == TRANSPORTATION_MANAGEMENT_REQUIRED_EVENT_TOPIC
    assert contract["source_package"]["consumes"] == TRANSPORTATION_MANAGEMENT_CONSUMED_EVENT_TYPES
    assert contract["source_package"]["emits"] == TRANSPORTATION_MANAGEMENT_EMITTED_EVENT_TYPES
    assert pbc_implementation_release_audit(("transportation_management",))["ok"] is True
    assert pbc_implemented_capability_audit(("transportation_management",))["ok"] is True


def test_transportation_management_runtime_applies_rules_parameters_and_configuration() -> None:
    state = transportation_management_empty_state()
    state = transportation_management_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": TRANSPORTATION_MANAGEMENT_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "default_currency": "USD",
            "allowed_modes": ("truckload", "ltl"),
            "telematics_providers": ("carrier_api",),
            "timezone": "UTC",
            "workbench_limit": 50,
        },
    )["state"]
    state = transportation_management_set_parameter(state, "max_cost_per_mile", 3.0)["state"]
    state = transportation_management_set_parameter(state, "on_time_weight", 0.35)["state"]
    state = transportation_management_set_parameter(state, "carbon_weight", 0.15)["state"]
    state = transportation_management_set_parameter(state, "eta_confidence_threshold", 0.75)["state"]
    state = transportation_management_register_rule(
        state,
        {
            "rule_id": "rule_ops",
            "tenant": "tenant_ops",
            "rule_type": "carrier_selection",
            "allowed_modes": ("truckload", "ltl"),
            "preferred_carriers": ("carrier_fast",),
            "restricted_carriers": ("carrier_blocked",),
            "service_level": "expedited",
            "hazmat_allowed": False,
            "status": "active",
        },
    )["state"]
    state = transportation_management_register_carrier(
        state,
        {
            "carrier_id": "carrier_fast",
            "tenant": "tenant_ops",
            "mode": "truckload",
            "service_levels": ("expedited",),
            "lanes": (("LAX", "SFO"),),
            "cost_per_mile": 2.2,
            "on_time_rate": 0.96,
            "carbon_per_mile": 130,
            "risk": 0.08,
            "identity": {"did": "did:appgen:carrier-fast", "issuer": "trusted_registry", "status": "active"},
        },
    )["state"]
    state = transportation_management_register_carrier(
        state,
        {
            "carrier_id": "carrier_lowcarbon",
            "tenant": "tenant_ops",
            "mode": "ltl",
            "service_levels": ("expedited",),
            "lanes": (("LAX", "SFO"),),
            "cost_per_mile": 1.9,
            "on_time_rate": 0.82,
            "carbon_per_mile": 85,
            "risk": 0.18,
            "identity": {"did": "did:appgen:carrier-low", "issuer": "trusted_registry", "status": "active"},
        },
    )["state"]
    shipment = transportation_management_create_shipment(
        state,
        {
            "shipment_id": "ship_ops",
            "tenant": "tenant_ops",
            "source_ref": "order_ops",
            "origin": "LAX",
            "destination": "SFO",
            "weight": 800,
            "mode": "truckload",
            "service_level": "expedited",
            "hazmat": False,
            "temperature_controlled": False,
        },
    )
    state = shipment["state"]
    assert shipment["shipment"]["status"] == "created"

    selection = transportation_management_select_carrier(state, "ship_ops")
    state = selection["state"]
    assert selection["selection"]["carrier_id"] == "carrier_fast"

    state = transportation_management_plan_route(state, "ship_ops", distance_miles=380, stops=("LAX", "SFO"))["state"]
    state = transportation_management_dispatch_shipment(state, "ship_ops", tender_id="tender_ops")["state"]
    tracking = transportation_management_record_tracking_event(
        state,
        "ship_ops",
        {"event_id": "track_ops", "location": "Bakersfield", "distance_remaining": 180, "delay_minutes": 10},
    )
    state = tracking["state"]
    eta = transportation_management_calculate_eta(state, "ship_ops", average_speed_mph=60)
    assert eta["eta_hours"] > 0
    assert eta["confidence"] >= 0.75

    delivery = transportation_management_confirm_delivery(state, "ship_ops", proof_id="pod_ops")
    state = delivery["state"]
    assert delivery["shipment"]["status"] == "delivered"
    assert state["outbox"][-1]["idempotency_key"] == "transportation_management:ShipmentDelivered:transport_evt_000008"

    workbench = transportation_management_build_workbench_view(state, tenant="tenant_ops")
    assert workbench["shipment_count"] == 1
    assert workbench["delivered_count"] == 1
    assert workbench["carrier_count"] == 2
    assert workbench["route_count"] == 1
    assert workbench["tracking_count"] == 1
    assert workbench["configuration_bound"] is True
    assert workbench["rule_count"] == 1
    assert workbench["parameter_count"] == 4
    assert workbench["binding_evidence"]["owned_tables"] == TRANSPORTATION_MANAGEMENT_OWNED_TABLES
    assert workbench["binding_evidence"]["configuration"]["event_contract"] == "AppGen-X"
    assert workbench["binding_evidence"]["configuration"]["event_topic"] == TRANSPORTATION_MANAGEMENT_REQUIRED_EVENT_TOPIC
    assert workbench["binding_evidence"]["configuration"]["stream_engine_picker_visible"] is False

    ui_contract = transportation_management_ui_contract()
    assert ui_contract["configuration_editor"]["allowed_database_backends"] == TRANSPORTATION_MANAGEMENT_ALLOWED_DATABASE_BACKENDS
    assert ui_contract["configuration_editor"]["fixed_event_topic"] == TRANSPORTATION_MANAGEMENT_REQUIRED_EVENT_TOPIC
    assert ui_contract["configuration_editor"]["stream_engine_picker_visible"] is False
    assert "max_cost_per_mile" in ui_contract["parameter_editor"]["numeric_parameters"]
    assert "rule_id" in ui_contract["rule_editor"]["required_fields"]
    assert ui_contract["event_surfaces"]["emits"] == TRANSPORTATION_MANAGEMENT_EMITTED_EVENT_TYPES
    assert ui_contract["event_surfaces"]["consumes"] == TRANSPORTATION_MANAGEMENT_CONSUMED_EVENT_TYPES
    rendered = transportation_management_render_workbench(
        state,
        tenant="tenant_ops",
        principal_permissions=(
            "transportation_management.master",
            "transportation_management.plan",
            "transportation_management.tender",
            "transportation_management.dispatch",
            "transportation_management.track",
            "transportation_management.confirm",
            "transportation_management.event",
            "transportation_management.audit",
            "transportation_management.configure",
        ),
    )
    assert rendered["ok"] is True
    assert rendered["configuration_bound"] is True
    assert rendered["event_outbox_count"] == 8
    assert rendered["event_inbox_count"] == 0
    assert rendered["dead_letter_count"] == 0
    assert rendered["binding_evidence"]["owned_tables"] == TRANSPORTATION_MANAGEMENT_OWNED_TABLES
    assert set(rendered["visible_actions"]) == set(ui_contract["action_permissions"])
    assert not rendered["locked_actions"]


def test_transportation_management_rejects_unsupported_database_backends_and_unknown_parameters() -> None:
    state = transportation_management_empty_state()

    with pytest.raises(ValueError, match="PostgreSQL, MySQL, or MariaDB"):
        transportation_management_configure_runtime(
            state,
            {
                "database_backend": "stream_store",
                "event_topic": TRANSPORTATION_MANAGEMENT_REQUIRED_EVENT_TOPIC,
                "retry_limit": 3,
                "default_currency": "USD",
            },
        )

    with pytest.raises(ValueError, match="Unsupported Transportation Management parameter"):
        transportation_management_set_parameter(state, "stream_engine", "hidden_picker")

    with pytest.raises(ValueError, match="requires AppGen-X event topic"):
        transportation_management_configure_runtime(
            state,
            {
                "database_backend": "postgresql",
                "event_topic": "custom.transportation.events",
                "retry_limit": 3,
                "default_currency": "USD",
            },
        )

    with pytest.raises(ValueError, match="unsupported eventing fields"):
        transportation_management_configure_runtime(
            state,
            {
                "database_backend": "postgresql",
                "event_topic": TRANSPORTATION_MANAGEMENT_REQUIRED_EVENT_TOPIC,
                "retry_limit": 3,
                "default_currency": "USD",
                "stream_engine_picker": "visible",
            },
        )


def test_transportation_management_contracts_events_schema_and_boundaries_are_package_local() -> None:
    state = transportation_management_configure_runtime(
        transportation_management_empty_state(),
        {
            "database_backend": "mariadb",
            "event_topic": TRANSPORTATION_MANAGEMENT_REQUIRED_EVENT_TOPIC,
            "retry_limit": 2,
            "default_currency": "USD",
            "allowed_modes": ("truckload", "ltl", "parcel"),
        },
    )["state"]

    extension = transportation_management_register_schema_extension(
        state,
        "tracking_event",
        {"telematics_payload": "jsonb", "eta_confidence": "numeric"},
    )
    state = extension["state"]
    assert extension["ok"] is True
    assert state["schema_extensions"]["tracking_event"]["eta_confidence"] == "numeric"

    with pytest.raises(ValueError, match="owned tables"):
        transportation_management_register_schema_extension(state, "inventory_balance", {"foreign_stock": "numeric"})

    invalid = transportation_management_register_schema_extension(state, "tracking_event", {"BadField": "text"})
    assert invalid["ok"] is False
    assert invalid["error"] == "invalid_extension_field"

    api = transportation_management_build_api_contract()
    assert api["format"] == "appgen.transportation-management-api-contract.v1"
    assert api["database_backends"] == TRANSPORTATION_MANAGEMENT_ALLOWED_DATABASE_BACKENDS
    assert api["owned_tables"] == TRANSPORTATION_MANAGEMENT_OWNED_TABLES
    assert api["events"]["emits"] == TRANSPORTATION_MANAGEMENT_EMITTED_EVENT_TYPES
    assert api["events"]["consumes"] == TRANSPORTATION_MANAGEMENT_CONSUMED_EVENT_TYPES
    assert api["shared_table_access"] is False
    assert api["stream_engine_picker_visible"] is False
    assert any(route["command"] == "receive_event" for route in api["routes"])

    schema = transportation_management_build_schema_contract()
    service = transportation_management_build_service_contract()
    release = transportation_management_build_release_evidence()
    assert schema["format"] == "appgen.transportation-management-owned-schema-contract.v1"
    assert schema["ok"] is True
    assert len(schema["tables"]) == len(TRANSPORTATION_MANAGEMENT_OWNED_TABLES)
    assert len(schema["migrations"]) == len(TRANSPORTATION_MANAGEMENT_OWNED_TABLES)
    assert {
        "shipment_line",
        "carrier_identity",
        "route_leg",
        "transportation_telematics_event",
        "transportation_governed_model",
    } <= {item["table"] for item in schema["tables"]}
    assert schema["shared_table_access"] is False
    assert service["format"] == "appgen.transportation-management-service-contract.v1"
    assert service["ok"] is True
    assert len(service["command_methods"]) >= 25
    assert service["external_dependencies"]["shared_tables"] == ()
    assert release["format"] == "appgen.transportation-management-release-evidence.v1"
    assert release["ok"] is True
    assert not release["blocking_gaps"]

    permissions = transportation_management_permissions_contract()
    assert permissions["ok"] is True
    assert permissions["action_permissions"]["receive_event"] == "transportation_management.event"
    assert "transportation_management.configure" in permissions["permissions"]

    processed = transportation_management_receive_event(
        state,
        {
            "event_id": "evt_pack_1",
            "event_type": "Packed",
            "payload": {"tenant": "tenant_ops", "pack_id": "pack_1", "order_id": "order_ops", "weight": 10},
        },
    )
    state = processed["state"]
    assert processed["ok"] is True
    assert state["packed_order_projections"]["pack_1"]["order_id"] == "order_ops"
    duplicate = transportation_management_receive_event(
        state,
        {
            "event_id": "evt_pack_1",
            "event_type": "Packed",
            "payload": {"tenant": "tenant_ops", "pack_id": "pack_1"},
        },
    )
    assert duplicate["duplicate"] is True
    assert len(duplicate["state"]["inbox"]) == 1

    retry = transportation_management_receive_event(
        state,
        {
            "event_id": "evt_bad",
            "event_type": "UnknownTransportationEvent",
            "payload": {"tenant": "tenant_ops"},
        },
    )
    assert retry["ok"] is False
    assert retry["handler"]["status"] == "retrying"
    dead = transportation_management_receive_event(
        retry["state"],
        {"event_id": "evt_bad", "event_type": "UnknownTransportationEvent", "payload": {"tenant": "tenant_ops"}},
    )
    assert dead["handler"]["status"] == "dead_letter"
    assert dead["state"]["dead_letters"][-1]["reason"] == "unsupported_or_failed_transportation_event"

    boundary = transportation_management_verify_owned_table_boundary(
        ("shipment", "Packed", "packed_order_projection", "transportation_management_custom_projection")
    )
    assert boundary["ok"] is True
    assert boundary["declared_dependencies"]["shared_tables"] == ()
    violation = transportation_management_verify_owned_table_boundary(("inventory_balance", "customer_profile"))
    assert violation["ok"] is False
    assert violation["violations"] == ("inventory_balance", "customer_profile")
