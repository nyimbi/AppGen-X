import pytest

from pyAppGen.pbcs.global_inventory_visibility import (
    GLOBAL_INVENTORY_VISIBILITY_ALLOWED_DATABASE_BACKENDS,
    GLOBAL_INVENTORY_VISIBILITY_CONSUMED_EVENT_TYPES,
    GLOBAL_INVENTORY_VISIBILITY_EMITTED_EVENT_TYPES,
    GLOBAL_INVENTORY_VISIBILITY_OWNED_TABLES,
    GLOBAL_INVENTORY_VISIBILITY_REQUIRED_EVENT_TOPIC,
    GLOBAL_INVENTORY_VISIBILITY_RUNTIME_CAPABILITY_KEYS,
    GLOBAL_INVENTORY_VISIBILITY_RUNTIME_TABLES,
    global_inventory_visibility_build_api_contract,
    global_inventory_visibility_build_release_evidence,
    global_inventory_visibility_build_schema_contract,
    global_inventory_visibility_build_service_contract,
    global_inventory_visibility_build_workbench_view,
    global_inventory_visibility_configure_runtime,
    global_inventory_visibility_empty_state,
    global_inventory_visibility_ingest_event,
    global_inventory_visibility_project_availability,
    global_inventory_visibility_record_availability_snapshot,
    global_inventory_visibility_register_inventory_pool,
    global_inventory_visibility_register_rule,
    global_inventory_visibility_register_schema_extension,
    global_inventory_visibility_register_supply_node,
    global_inventory_visibility_permissions_contract,
    global_inventory_visibility_render_workbench,
    global_inventory_visibility_reserve_inventory,
    global_inventory_visibility_runtime_capabilities,
    global_inventory_visibility_runtime_smoke,
    global_inventory_visibility_set_parameter,
    global_inventory_visibility_ui_contract,
    global_inventory_visibility_verify_owned_table_boundary,
    implementation_contract,
)


def test_global_inventory_visibility_runtime_executes_standard_and_advanced_capabilities() -> None:
    runtime = global_inventory_visibility_runtime_capabilities()
    smoke = global_inventory_visibility_runtime_smoke()

    assert runtime["format"] == "appgen.global-inventory-visibility-runtime-capabilities.v1"
    assert runtime["ok"] is True
    assert runtime["implementation_directory"] == "src/pyAppGen/pbcs/global_inventory_visibility"
    assert runtime["owned_tables"] == GLOBAL_INVENTORY_VISIBILITY_OWNED_TABLES
    assert runtime["runtime_tables"] == GLOBAL_INVENTORY_VISIBILITY_RUNTIME_TABLES
    assert runtime["required_event_topic"] == GLOBAL_INVENTORY_VISIBILITY_REQUIRED_EVENT_TOPIC
    assert len(runtime["standard_features"]) >= 18
    assert "rule_engine" in runtime["standard_features"]
    assert "parameter_engine" in runtime["standard_features"]
    assert "configuration_schema" in runtime["standard_features"]
    assert {"build_schema_contract", "build_service_contract", "build_release_evidence", "run_control_tests"} <= set(
        runtime["operations"]
    )
    assert smoke["ok"] is True
    assert set(GLOBAL_INVENTORY_VISIBILITY_RUNTIME_CAPABILITY_KEYS) == {
        check["id"] for check in smoke["checks"]
    }
    assert not smoke["blocking_gaps"]

    contract = implementation_contract()
    assert contract["pbc"] == "global_inventory_visibility"
    assert contract["owned_tables"] == GLOBAL_INVENTORY_VISIBILITY_OWNED_TABLES
    assert contract["allowed_database_backends"] == GLOBAL_INVENTORY_VISIBILITY_ALLOWED_DATABASE_BACKENDS
    assert contract["api_contract"]["shared_table_access"] is False
    assert contract["schema_contract"]["ok"] is True
    assert contract["service_contract"]["ok"] is True
    assert contract["release_evidence_contract"]["ok"] is True
    assert contract["permissions_contract"]["ok"] is True
    assert contract["advanced_runtime"]["ok"] is True
    assert contract["ui_contract"]["ok"] is True
    assert "InventoryConfigurationPanel" in contract["ui_contract"]["fragments"]
    assert contract["runtime_tables"] == GLOBAL_INVENTORY_VISIBILITY_RUNTIME_TABLES
    assert set(contract["advanced_runtime"]["capabilities"]) == set(
        GLOBAL_INVENTORY_VISIBILITY_RUNTIME_CAPABILITY_KEYS
    )


def test_global_inventory_visibility_package_schema_service_release_and_ui_contracts() -> None:
    schema = global_inventory_visibility_build_schema_contract()
    service = global_inventory_visibility_build_service_contract()
    release = global_inventory_visibility_build_release_evidence()
    api = global_inventory_visibility_build_api_contract()
    ui = global_inventory_visibility_ui_contract()

    assert schema["format"] == "appgen.global-inventory-visibility-owned-schema-contract.v1"
    assert schema["ok"] is True
    assert len(schema["tables"]) == len(GLOBAL_INVENTORY_VISIBILITY_OWNED_TABLES)
    assert len(schema["migrations"]) == len(GLOBAL_INVENTORY_VISIBILITY_OWNED_TABLES)
    assert tuple(item["table"] for item in schema["runtime_tables"]) == GLOBAL_INVENTORY_VISIBILITY_RUNTIME_TABLES
    assert schema["datastore_backends"] == GLOBAL_INVENTORY_VISIBILITY_ALLOWED_DATABASE_BACKENDS
    assert schema["required_event_topic"] == GLOBAL_INVENTORY_VISIBILITY_REQUIRED_EVENT_TOPIC
    assert schema["shared_table_access"] is False

    assert service["format"] == "appgen.global-inventory-visibility-service-contract.v1"
    assert service["ok"] is True
    assert service["transaction_boundary"] == "global_inventory_visibility_owned_datastore_plus_appgen_outbox"
    assert "ingest_event" in service["idempotent_handlers"]
    assert service["retry_dead_letter_evidence"]["dead_letter_table"] == GLOBAL_INVENTORY_VISIBILITY_RUNTIME_TABLES[2]
    assert service["eventing"]["contract"] == "AppGen-X"
    assert service["external_dependencies"]["shared_tables"] == ()
    assert service["rules_parameters_configuration"] == ("register_rule", "set_parameter", "configure_runtime")

    assert ui["binding_evidence"]["runtime_tables"] == GLOBAL_INVENTORY_VISIBILITY_RUNTIME_TABLES
    assert ui["binding_evidence"]["event_contract"] == "AppGen-X"
    assert ui["binding_evidence"]["required_event_topic"] == GLOBAL_INVENTORY_VISIBILITY_REQUIRED_EVENT_TOPIC
    assert ui["binding_evidence"]["shared_table_access"] is False

    assert {route["route"] for route in api["routes"]} >= {
        "PUT /inventory/configuration",
        "POST /inventory/parameters",
        "POST /inventory/rules",
        "POST /inventory/events/inbox",
        "GET /inventory/workbench",
        "GET /inventory/schema-contract",
        "GET /inventory/service-contract",
        "GET /inventory/release-evidence",
    }
    assert all(isinstance(route, dict) and (route.get("command") or route.get("query")) for route in api["routes"])
    assert all(route["event_contract"] == "AppGen-X" for route in api["routes"])
    assert all(route["shared_table_access"] is False for route in api["routes"])

    assert release["format"] == "appgen.global-inventory-visibility-release-evidence.v1"
    assert release["ok"] is True
    assert not release["blocking_gaps"]
    assert release["schema"]["format"] == schema["format"]
    assert release["service"]["format"] == service["format"]
    assert release["api"]["required_event_topic"] == GLOBAL_INVENTORY_VISIBILITY_REQUIRED_EVENT_TOPIC
    assert release["ui"]["binding_evidence"]["runtime_tables"] == GLOBAL_INVENTORY_VISIBILITY_RUNTIME_TABLES
    assert release["workbench"]["binding_evidence"]["outbox_table"] == GLOBAL_INVENTORY_VISIBILITY_RUNTIME_TABLES[0]
    assert release["boundary"]["declared_dependencies"]["shared_tables"] == ()


def test_global_inventory_visibility_runtime_applies_rules_parameters_and_configuration() -> None:
    state = global_inventory_visibility_empty_state()
    state = global_inventory_visibility_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": "appgen.global_inventory_visibility.events",
            "retry_limit": 3,
            "default_currency": "USD",
            "projection_horizon_days": 10,
            "staleness_sla_minutes": 60,
            "workbench_limit": 50,
        },
    )["state"]
    state = global_inventory_visibility_set_parameter(state, "safety_stock_percent", 0.1)["state"]
    state = global_inventory_visibility_set_parameter(state, "freshness_half_life_hours", 48)["state"]
    state = global_inventory_visibility_set_parameter(state, "reservation_ttl_minutes", 240)["state"]
    registered_rule = global_inventory_visibility_register_rule(
        state,
        {
            "rule_id": "rule_ops",
            "tenant": "tenant_ops",
            "scope": "global_pool",
            "status": "active",
            "rule_type": "allocation",
            "preferred_nodes": ("node_ops",),
            "freshness_floor": 0.55,
            "policy": "balanced",
        },
    )
    state = registered_rule["state"]
    assert registered_rule["rule"]["compiled_evidence"]["deterministic"] is True
    assert registered_rule["rule"]["compiled_hash"]

    state = global_inventory_visibility_register_supply_node(
        state,
        {
            "node_id": "node_ops",
            "tenant": "tenant_ops",
            "node_type": "warehouse",
            "country": "US",
            "region": "CENTRAL",
            "health_score": 0.94,
            "latency_ms": 20,
            "carbon_intensity": 120,
            "federated_systems": ("wms",),
            "identity": {
                "did": "did:appgen:node-ops",
                "issuer": "trusted_registry",
                "status": "active",
            },
        },
    )["state"]
    state = global_inventory_visibility_register_inventory_pool(
        state,
        {
            "pool_id": "pool_ops",
            "tenant": "tenant_ops",
            "item_id": "sku_ops",
            "pool_type": "enterprise",
            "node_ids": ("node_ops",),
            "allocation_policy": "balanced",
            "safety_stock_units": 12,
            "lead_time_days": 2,
        },
    )["state"]
    state = global_inventory_visibility_record_availability_snapshot(
        state,
        {
            "snapshot_id": "snap_ops",
            "tenant": "tenant_ops",
            "pool_id": "pool_ops",
            "node_id": "node_ops",
            "on_hand": 100,
            "reserved": 5,
            "allocated": 10,
            "in_transit": 15,
            "safety_stock": 8,
            "freshness_age_hours": 4,
            "staleness_minutes": 15,
        },
    )["state"]

    projection = global_inventory_visibility_project_availability(
        state,
        tenant="tenant_ops",
        pool_id="pool_ops",
    )
    state = projection["state"]
    assert projection["projection"]["on_hand"] == 100
    assert projection["projection"]["reserved"] == 5
    assert projection["projection"]["allocated"] == 10
    assert projection["projection"]["safety_stock"] == 12
    assert projection["projection"]["available_to_promise"] == 76.1
    assert projection["projection"]["capable_to_promise"] == pytest.approx(86.48, rel=1e-6)
    assert projection["projection"]["supply_signal"]["net_supply"] == 103
    assert projection["projection"]["demand_signal"]["gross_demand"] == 15
    assert projection["projection"]["freshness_sla_minutes"] == 60
    assert projection["projection"]["sla_breached"] is False
    assert projection["projection"]["reconciliation_status"] == "reconciled"
    assert projection["projection"]["channel_projection"] == ()

    reservation = global_inventory_visibility_reserve_inventory(
        state,
        {
            "reservation_id": "resv_ops",
            "tenant": "tenant_ops",
            "pool_id": "pool_ops",
            "order_id": "order_ops",
            "quantity": 20,
            "channel": "web",
        },
    )
    state = reservation["state"]
    assert reservation["reservation"]["ttl_minutes"] == 240.0
    assert reservation["projection"]["reserved"] == 25
    assert reservation["projection"]["channel_projection"] == (
        {"channel": "web", "reserved_quantity": 20},
    )

    state = global_inventory_visibility_ingest_event(
        state,
        {
            "event_id": "evt_receipt_ops",
            "event_type": "GoodsReceiptPosted",
            "idempotency_key": "external:GoodsReceiptPosted:evt_receipt_ops",
            "tenant": "tenant_ops",
            "pool_id": "pool_ops",
            "node_id": "node_ops",
            "quantity": 10,
        },
    )["state"]
    duplicate = global_inventory_visibility_ingest_event(
        state,
        {
            "event_id": "evt_receipt_ops",
            "event_type": "GoodsReceiptPosted",
            "idempotency_key": "external:GoodsReceiptPosted:evt_receipt_ops",
            "tenant": "tenant_ops",
            "pool_id": "pool_ops",
            "node_id": "node_ops",
            "quantity": 10,
        },
    )
    assert duplicate["duplicate"] is True
    assert len(duplicate["state"]["inbox"]) == 1
    state = global_inventory_visibility_project_availability(
        state,
        tenant="tenant_ops",
        pool_id="pool_ops",
    )["state"]

    workbench = global_inventory_visibility_build_workbench_view(state, tenant="tenant_ops")
    assert workbench["pool_count"] == 1
    assert workbench["node_count"] == 1
    assert workbench["projection_count"] == 3
    assert workbench["reservation_count"] == 1
    assert workbench["available_to_promise"] == 202.36
    assert workbench["configuration_bound"] is True
    assert workbench["rule_count"] == 1
    assert workbench["parameter_count"] == 3
    assert workbench["rules_bound"] == ("rule_ops",)
    assert workbench["parameters_bound"] == (
        "freshness_half_life_hours",
        "reservation_ttl_minutes",
        "safety_stock_percent",
    )
    assert workbench["capable_to_promise"] == pytest.approx(233.49, rel=1e-6)
    assert workbench["channel_projection_count"] == 1
    assert workbench["outbox_count"] == 4
    assert workbench["inbox_count"] == 1
    assert workbench["dead_letter_count"] == 0
    assert workbench["binding_evidence"]["runtime_tables"] == GLOBAL_INVENTORY_VISIBILITY_RUNTIME_TABLES
    assert workbench["binding_evidence"]["ui_bindings"]["parameter_fragment"] == "InventoryParameterConsole"

    ui_contract = global_inventory_visibility_ui_contract()
    assert ui_contract["configuration_editor"]["allowed_database_backends"] == (
        "postgresql",
        "mysql",
        "mariadb",
    )
    assert ui_contract["configuration_editor"]["required_event_topic"] == GLOBAL_INVENTORY_VISIBILITY_REQUIRED_EVENT_TOPIC
    assert ui_contract["configuration_editor"]["user_facing_stream_engine_picker"] is False
    assert "safety_stock_percent" in ui_contract["parameter_editor"]["numeric_parameters"]
    assert "rule_id" in ui_contract["rule_editor"]["required_fields"]
    assert ui_contract["binding_evidence"]["runtime_tables"] == GLOBAL_INVENTORY_VISIBILITY_RUNTIME_TABLES
    rendered = global_inventory_visibility_render_workbench(
        state,
        tenant="tenant_ops",
        principal_permissions=(
            "global_inventory_visibility.read",
            "global_inventory_visibility.reserve",
            "global_inventory_visibility.configure",
            "global_inventory_visibility.audit",
        ),
    )
    assert rendered["ok"] is True
    assert rendered["configuration_bound"] is True
    assert rendered["rules_bound"] == ("rule_ops",)
    assert rendered["parameters_bound"] == (
        "freshness_half_life_hours",
        "reservation_ttl_minutes",
        "safety_stock_percent",
    )
    assert rendered["event_outbox_count"] == 4
    assert rendered["inbox_count"] == 1
    assert rendered["dead_letter_count"] == 0
    assert rendered["binding_evidence"]["outbox_table"] == GLOBAL_INVENTORY_VISIBILITY_RUNTIME_TABLES[0]
    assert rendered["binding_evidence"]["configuration_state"]["event_contract"] == "AppGen-X"
    assert rendered["binding_evidence"]["ui_bindings"]["parameter_fragment"] == "InventoryParameterConsole"
    assert set(rendered["visible_actions"]) <= set(ui_contract["action_permissions"])


def test_global_inventory_visibility_rejects_unsupported_backends_and_records_dead_letter_evidence() -> None:
    state = global_inventory_visibility_empty_state()

    with pytest.raises(ValueError, match="PostgreSQL, MySQL, or MariaDB"):
        global_inventory_visibility_configure_runtime(
            state,
            {
                "database_backend": "sqlite",
                "event_topic": "appgen.global_inventory_visibility.events",
                "retry_limit": 3,
                "default_currency": "USD",
                "projection_horizon_days": 10,
                "staleness_sla_minutes": 60,
                "workbench_limit": 50,
            },
        )

    with pytest.raises(ValueError, match="stream-engine selection is not supported"):
        global_inventory_visibility_configure_runtime(
            state,
            {
                "database_backend": "postgresql",
                "event_topic": "appgen.global_inventory_visibility.events",
                "retry_limit": 3,
                "default_currency": "USD",
                "projection_horizon_days": 10,
                "staleness_sla_minutes": 60,
                "workbench_limit": 50,
                "stream_engine": "kafka-picker",
            },
        )

    configured = global_inventory_visibility_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": "appgen.global_inventory_visibility.events",
            "retry_limit": 2,
            "default_currency": "USD",
            "projection_horizon_days": 10,
            "staleness_sla_minutes": 60,
            "workbench_limit": 50,
        },
    )["state"]

    with pytest.raises(ValueError, match="Unsupported Global Inventory Visibility parameter"):
        global_inventory_visibility_set_parameter(configured, "stream_engine", 1)

    with pytest.raises(ValueError, match="rules require fields"):
        global_inventory_visibility_register_rule(
            configured,
            {
                "rule_id": "rule_missing_scope",
                "tenant": "tenant_ops",
                "status": "active",
                "rule_type": "allocation",
            },
        )

    state = global_inventory_visibility_register_supply_node(
        configured,
        {
            "node_id": "node_ops",
            "tenant": "tenant_ops",
            "node_type": "warehouse",
            "country": "US",
            "region": "CENTRAL",
            "health_score": 0.94,
            "latency_ms": 20,
            "carbon_intensity": 120,
            "federated_systems": ("wms",),
            "identity": {
                "did": "did:appgen:node-ops",
                "issuer": "trusted_registry",
                "status": "active",
            },
        },
    )["state"]
    state = global_inventory_visibility_register_inventory_pool(
        state,
        {
            "pool_id": "pool_ops",
            "tenant": "tenant_ops",
            "item_id": "sku_ops",
            "pool_type": "enterprise",
            "node_ids": ("node_ops",),
            "allocation_policy": "balanced",
            "safety_stock_units": 12,
            "lead_time_days": 2,
        },
    )["state"]
    failed = global_inventory_visibility_ingest_event(
        state,
        {
            "event_id": "evt_retry_ops",
            "event_type": "GoodsReceiptPosted",
            "idempotency_key": "external:GoodsReceiptPosted:evt_retry_ops",
            "tenant": "tenant_ops",
            "pool_id": "pool_ops",
            "node_id": "node_ops",
            "quantity": 10,
            "retry_count": 3,
        },
    )

    assert failed["ok"] is False
    assert failed["dead_letter"]["reason"] == "retry_limit_exceeded"
    assert failed["state"]["retry_evidence"] == {
        "external:GoodsReceiptPosted:evt_retry_ops": 3
    }
    assert len(failed["state"]["dead_letters"]) == 1


def test_global_inventory_visibility_proves_owned_boundary_contracts() -> None:
    state = global_inventory_visibility_empty_state()
    state = global_inventory_visibility_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": GLOBAL_INVENTORY_VISIBILITY_REQUIRED_EVENT_TOPIC,
            "retry_limit": 2,
            "default_currency": "USD",
            "projection_horizon_days": 10,
            "staleness_sla_minutes": 60,
            "workbench_limit": 50,
        },
    )["state"]

    assert global_inventory_visibility_register_schema_extension(
        state,
        "inventory_projection",
        {"explainability_payload": "jsonb"},
    )["ok"] is True
    assert global_inventory_visibility_register_schema_extension(
        state,
        "order_line",
        {"order_payload": "jsonb"},
    )["error"] == "table_not_owned"
    assert global_inventory_visibility_register_schema_extension(
        state,
        "inventory_projection",
        {"InvalidField": "jsonb"},
    )["error"] == "invalid_extension_field"

    api = global_inventory_visibility_build_api_contract()
    assert api["owned_tables"] == GLOBAL_INVENTORY_VISIBILITY_OWNED_TABLES
    assert api["runtime_tables"] == GLOBAL_INVENTORY_VISIBILITY_RUNTIME_TABLES
    assert api["database_backends"] == GLOBAL_INVENTORY_VISIBILITY_ALLOWED_DATABASE_BACKENDS
    assert api["required_event_topic"] == GLOBAL_INVENTORY_VISIBILITY_REQUIRED_EVENT_TOPIC
    assert api["emits"] == GLOBAL_INVENTORY_VISIBILITY_EMITTED_EVENT_TYPES
    assert api["consumes"] == GLOBAL_INVENTORY_VISIBILITY_CONSUMED_EVENT_TYPES
    assert api["shared_table_access"] is False
    assert api["stream_engine_picker_visible"] is False
    assert api["dependencies"]["shared_tables"] == ()
    assert api["rules_parameters_configuration"] == ("register_rule", "set_parameter", "configure_runtime")
    assert any(route["command"] == "configure_runtime" for route in api["routes"])
    assert any(route["command"] == "set_parameter" for route in api["routes"])
    assert any(route["command"] == "register_rule" for route in api["routes"])
    assert any(route["command"] == "ingest_event" for route in api["routes"])
    assert any(route.get("query") == "build_schema_contract" for route in api["routes"])
    assert any(route.get("query") == "build_service_contract" for route in api["routes"])
    assert any(route.get("query") == "build_release_evidence" for route in api["routes"])

    permissions = global_inventory_visibility_permissions_contract()
    assert permissions["action_permissions"]["ingest_event"] == "global_inventory_visibility.configure"
    assert permissions["action_permissions"]["build_schema_contract"] == "global_inventory_visibility.audit"
    assert permissions["action_permissions"]["build_service_contract"] == "global_inventory_visibility.audit"
    assert permissions["action_permissions"]["build_release_evidence"] == "global_inventory_visibility.audit"

    allowed = global_inventory_visibility_verify_owned_table_boundary(
        (
            "inventory_pool",
            "inventory_projection",
            "global_inventory_visibility_appgen_inbox_event",
            "wms_stock_projection",
            "GET /transportation/shipments/{item_id}",
        )
    )
    assert allowed["ok"] is True
    assert allowed["declared_dependencies"]["shared_tables"] == ()
    rejected = global_inventory_visibility_verify_owned_table_boundary(("order_line", "wms_stock"))
    assert rejected["ok"] is False
    assert rejected["violations"] == ("order_line", "wms_stock")
