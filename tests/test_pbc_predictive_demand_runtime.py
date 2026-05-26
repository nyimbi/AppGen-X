import pytest

from pyAppGen.pbcs.predictive_demand import PREDICTIVE_DEMAND_ALLOWED_DATABASE_BACKENDS
from pyAppGen.pbcs.predictive_demand import PREDICTIVE_DEMAND_CONSUMED_EVENT_TYPES
from pyAppGen.pbcs.predictive_demand import PREDICTIVE_DEMAND_EMITTED_EVENT_TYPES
from pyAppGen.pbcs.predictive_demand import PREDICTIVE_DEMAND_OWNED_TABLES
from pyAppGen.pbcs.predictive_demand import PREDICTIVE_DEMAND_REQUIRED_EVENT_TOPIC
from pyAppGen.pbcs.predictive_demand import PREDICTIVE_DEMAND_RUNTIME_CAPABILITY_KEYS
from pyAppGen.pbcs.predictive_demand import PREDICTIVE_DEMAND_RUNTIME_TABLES
from pyAppGen.pbcs.predictive_demand import implementation_contract
from pyAppGen.pbcs.predictive_demand import predictive_demand_build_api_contract
from pyAppGen.pbcs.predictive_demand import predictive_demand_build_release_evidence
from pyAppGen.pbcs.predictive_demand import predictive_demand_build_schema_contract
from pyAppGen.pbcs.predictive_demand import predictive_demand_build_service_contract
from pyAppGen.pbcs.predictive_demand import predictive_demand_build_workbench_view
from pyAppGen.pbcs.predictive_demand import predictive_demand_configure_runtime
from pyAppGen.pbcs.predictive_demand import predictive_demand_create_forecast_run
from pyAppGen.pbcs.predictive_demand import predictive_demand_empty_state
from pyAppGen.pbcs.predictive_demand import predictive_demand_ingest_demand_signal
from pyAppGen.pbcs.predictive_demand import predictive_demand_permissions_contract
from pyAppGen.pbcs.predictive_demand import predictive_demand_publish_forecast_result
from pyAppGen.pbcs.predictive_demand import predictive_demand_receive_event
from pyAppGen.pbcs.predictive_demand import predictive_demand_register_forecast_model
from pyAppGen.pbcs.predictive_demand import predictive_demand_register_rule
from pyAppGen.pbcs.predictive_demand import predictive_demand_register_schema_extension
from pyAppGen.pbcs.predictive_demand import predictive_demand_render_workbench
from pyAppGen.pbcs.predictive_demand import predictive_demand_runtime_capabilities
from pyAppGen.pbcs.predictive_demand import predictive_demand_runtime_smoke
from pyAppGen.pbcs.predictive_demand import predictive_demand_set_parameter
from pyAppGen.pbcs.predictive_demand import predictive_demand_ui_contract
from pyAppGen.pbcs.predictive_demand import predictive_demand_verify_owned_table_boundary


def test_predictive_demand_runtime_exposes_complete_local_contract_surface() -> None:
    runtime = predictive_demand_runtime_capabilities()
    smoke = predictive_demand_runtime_smoke()
    schema = predictive_demand_build_schema_contract()
    service = predictive_demand_build_service_contract()
    release = predictive_demand_build_release_evidence()
    package_contract = implementation_contract()

    assert runtime["format"] == "appgen.predictive-demand-runtime-capabilities.v1"
    assert runtime["ok"] is True
    assert runtime["implementation_directory"] == "src/pyAppGen/pbcs/predictive_demand"
    assert runtime["owned_tables"] == PREDICTIVE_DEMAND_OWNED_TABLES
    assert runtime["runtime_tables"] == PREDICTIVE_DEMAND_RUNTIME_TABLES
    assert runtime["required_event_topic"] == PREDICTIVE_DEMAND_REQUIRED_EVENT_TOPIC
    assert runtime["event_contract"] == "AppGen-X"
    assert runtime["consumes"] == PREDICTIVE_DEMAND_CONSUMED_EVENT_TYPES
    assert runtime["emits"] == PREDICTIVE_DEMAND_EMITTED_EVENT_TYPES
    assert {
        "build_schema_contract",
        "build_service_contract",
        "build_release_evidence",
    } <= set(runtime["operations"])
    assert {"schema_contract", "service_contract", "release_evidence"} <= set(
        runtime["standard_features"]
    )

    assert smoke["ok"] is True
    assert {check["id"] for check in smoke["checks"]} == set(
        PREDICTIVE_DEMAND_RUNTIME_CAPABILITY_KEYS
    )
    assert not smoke["blocking_gaps"]

    assert schema["ok"] is True
    assert schema["owned_tables"] == PREDICTIVE_DEMAND_OWNED_TABLES
    assert len(schema["tables"]) == len(PREDICTIVE_DEMAND_OWNED_TABLES)
    assert len(schema["migrations"]) == len(PREDICTIVE_DEMAND_OWNED_TABLES)
    assert len(schema["models"]) == len(PREDICTIVE_DEMAND_OWNED_TABLES)
    assert tuple(item["table"] for item in schema["runtime_tables"]) == (
        PREDICTIVE_DEMAND_RUNTIME_TABLES
    )
    assert schema["database_backends"] == PREDICTIVE_DEMAND_ALLOWED_DATABASE_BACKENDS
    assert schema["shared_table_access"] is False

    assert service["ok"] is True
    assert service["mutates_only_owned_tables"] is True
    assert service["runtime_tables"] == PREDICTIVE_DEMAND_RUNTIME_TABLES
    assert service["event_contract"]["contract"] == "AppGen-X"
    assert service["event_contract"]["required_topic"] == PREDICTIVE_DEMAND_REQUIRED_EVENT_TOPIC
    assert service["event_contract"]["stream_engine_picker_visible"] is False
    assert service["configuration_contract"]["allowed_database_backends"] == (
        PREDICTIVE_DEMAND_ALLOWED_DATABASE_BACKENDS
    )
    assert service["configuration_contract"]["user_selectable_event_contract"] is False
    assert service["idempotent_handlers"] == ("receive_event",)
    assert "build_release_evidence" in service["query_methods"]

    assert release["ok"] is True
    assert not release["blocking_gaps"]

    assert package_contract["advanced_runtime"]["ok"] is True
    assert package_contract["api_contract"]["ok"] is True
    assert package_contract["schema_contract"]["ok"] is True
    assert package_contract["service_contract"]["ok"] is True
    assert package_contract["release_evidence_contract"]["ok"] is True
    assert package_contract["permissions_contract"]["ok"] is True
    assert package_contract["ui_contract"]["ok"] is True
    assert package_contract["owned_tables"] == PREDICTIVE_DEMAND_OWNED_TABLES
    assert package_contract["runtime_tables"] == PREDICTIVE_DEMAND_RUNTIME_TABLES
    assert package_contract["allowed_database_backends"] == (
        PREDICTIVE_DEMAND_ALLOWED_DATABASE_BACKENDS
    )
    assert package_contract["required_event_topic"] == PREDICTIVE_DEMAND_REQUIRED_EVENT_TOPIC
    assert package_contract["event_contract"] == "AppGen-X"
    assert package_contract["emits"] == PREDICTIVE_DEMAND_EMITTED_EVENT_TYPES
    assert package_contract["consumes"] == PREDICTIVE_DEMAND_CONSUMED_EVENT_TYPES
    assert package_contract["boundary_contract"]["ok"] is True
    assert package_contract["boundary_contract"]["declared_dependencies"]["shared_tables"] == ()
    assert package_contract["shared_table_access"] is False


def test_predictive_demand_runtime_proves_commands_artifacts_permissions_and_ui() -> None:
    state = _configured_state()
    state = predictive_demand_register_forecast_model(
        state,
        {
            "model_id": "model_ops",
            "tenant": "tenant_ops",
            "sku": "SKU-OPS",
            "location": "DC-1",
            "algorithm": "ensemble",
            "version": "2026.05",
            "status": "active",
        },
    )["state"]
    extension = predictive_demand_register_schema_extension(
        state,
        "forecast_result",
        {"planner_commentary": "jsonb"},
    )
    state = extension["state"]
    assert extension["extension"]["version"] == 1
    assert extension["extension"]["table"] == "forecast_result"

    handled = predictive_demand_receive_event(
        state,
        {
            "event_id": "ship_ops",
            "event_type": "OrderShipped",
            "payload": {
                "tenant": "tenant_ops",
                "sku": "SKU-OPS",
                "location": "DC-1",
                "region": "US",
                "quantity": 60,
            },
        },
    )
    state = handled["state"]
    duplicate = predictive_demand_receive_event(
        state,
        {
            "event_id": "ship_ops",
            "event_type": "OrderShipped",
            "payload": {
                "tenant": "tenant_ops",
                "sku": "SKU-OPS",
                "location": "DC-1",
                "region": "US",
                "quantity": 60,
            },
        },
    )
    state = duplicate["state"]
    state = predictive_demand_receive_event(
        state,
        {
            "event_id": "ops_kpi",
            "event_type": "OperationalKpiChanged",
            "payload": {
                "tenant": "tenant_ops",
                "sku": "SKU-OPS",
                "location": "DC-1",
                "region": "US",
                "value": 18,
                "kpi_name": "order_intake_velocity",
            },
        },
    )["state"]
    state = predictive_demand_receive_event(
        state,
        {
            "event_id": "inv_ops",
            "event_type": "InventoryPoolChanged",
            "payload": {
                "tenant": "tenant_ops",
                "sku": "SKU-OPS",
                "location": "DC-1",
                "region": "US",
                "available_quantity": 45,
            },
        },
    )["state"]
    state = predictive_demand_ingest_demand_signal(
        state,
        {
            "signal_id": "manual_ops",
            "tenant": "tenant_ops",
            "signal_type": "manual",
            "sku": "SKU-OPS",
            "location": "DC-1",
            "region": "US",
            "quantity": 40,
            "signal_date": "2026-05-26",
            "source": "planner_override",
            "payload": {"reason": "customer launch"},
        },
    )["state"]
    state = predictive_demand_create_forecast_run(
        state,
        {
            "run_id": "run_ops",
            "model_id": "model_ops",
            "tenant": "tenant_ops",
            "sku": "SKU-OPS",
            "location": "DC-1",
            "horizon_days": 14,
            "initiated_by": "planner_ops",
            "status": "active",
        },
    )["state"]
    state = predictive_demand_publish_forecast_result(
        state,
        {
            "result_id": "result_ops",
            "run_id": "run_ops",
            "tenant": "tenant_ops",
            "status": "published",
        },
    )["state"]

    result = state["forecast_results"]["result_ops"]
    outbox_event_types = tuple(item["event_type"] for item in state["outbox"])
    assert handled["handler"]["status"] == "handled"
    assert duplicate["handler"]["status"] == "duplicate"
    assert result["forecast_quantity"] > 0.0
    assert result["shortage_quantity"] > 0.0
    assert outbox_event_types == (
        "ForecastUpdated",
        "MaterialShortageDetected",
    )
    assert all(item["contract"] == "AppGen-X" for item in state["outbox"])
    assert all(
        item["retry_policy"]["dead_letter"] == PREDICTIVE_DEMAND_RUNTIME_TABLES[2]
        for item in state["outbox"]
    )

    workbench = predictive_demand_build_workbench_view(state, tenant="tenant_ops")
    assert workbench["model_count"] == 1
    assert workbench["run_count"] == 1
    assert workbench["signal_count"] == 4
    assert workbench["result_count"] == 1
    assert workbench["shortage_count"] == 1
    assert workbench["inventory_position_count"] == 1
    assert workbench["configuration_bound"] is True
    assert workbench["rule_count"] == 1
    assert workbench["parameter_count"] == 10
    assert workbench["binding_evidence"]["owned_tables"] == PREDICTIVE_DEMAND_OWNED_TABLES
    assert workbench["binding_evidence"]["runtime_tables"] == PREDICTIVE_DEMAND_RUNTIME_TABLES
    assert workbench["binding_evidence"]["event_contract"] == "AppGen-X"
    assert workbench["binding_evidence"]["required_event_topic"] == (
        PREDICTIVE_DEMAND_REQUIRED_EVENT_TOPIC
    )
    assert workbench["binding_evidence"]["shared_table_access"] is False

    ui_contract = predictive_demand_ui_contract()
    assert ui_contract["configuration_editor"]["allowed_database_backends"] == (
        PREDICTIVE_DEMAND_ALLOWED_DATABASE_BACKENDS
    )
    assert ui_contract["configuration_editor"]["required_event_topic"] == (
        PREDICTIVE_DEMAND_REQUIRED_EVENT_TOPIC
    )
    assert ui_contract["configuration_editor"]["event_contract"] == "AppGen-X"
    assert ui_contract["configuration_editor"]["stream_engine_picker_visible"] is False
    assert ui_contract["configuration_editor"]["user_eventing_choice"] is False
    assert ui_contract["event_surfaces"]["event_contract"] == "AppGen-X"
    assert ui_contract["event_surfaces"]["required_event_topic"] == (
        PREDICTIVE_DEMAND_REQUIRED_EVENT_TOPIC
    )
    assert ui_contract["binding_evidence"]["runtime_tables"] == PREDICTIVE_DEMAND_RUNTIME_TABLES

    rendered = predictive_demand_render_workbench(
        state,
        tenant="tenant_ops",
        principal_permissions=(
            "predictive_demand.model.write",
            "predictive_demand.signal.write",
            "predictive_demand.run.write",
            "predictive_demand.result.write",
            "predictive_demand.event.consume",
            "predictive_demand.configure",
            "predictive_demand.audit",
        ),
    )
    assert rendered["ok"] is True
    assert not rendered["locked_actions"]
    assert rendered["binding_evidence"]["owned_tables"] == PREDICTIVE_DEMAND_OWNED_TABLES
    assert rendered["binding_evidence"]["runtime_tables"] == PREDICTIVE_DEMAND_RUNTIME_TABLES

    api_contract = predictive_demand_build_api_contract()
    assert api_contract["database_backends"] == PREDICTIVE_DEMAND_ALLOWED_DATABASE_BACKENDS
    assert api_contract["runtime_tables"] == PREDICTIVE_DEMAND_RUNTIME_TABLES
    assert api_contract["event_contract"] == "AppGen-X"
    assert api_contract["required_event_topic"] == PREDICTIVE_DEMAND_REQUIRED_EVENT_TOPIC
    assert api_contract["stream_engine_picker_visible"] is False
    assert api_contract["user_selectable_event_contract"] is False
    assert api_contract["shared_table_access"] is False
    assert {route["command"] for route in api_contract["routes"] if "command" in route} >= {
        "register_forecast_model",
        "ingest_demand_signal",
        "create_forecast_run",
        "publish_forecast_result",
        "receive_event",
    }
    assert {route["query"] for route in api_contract["routes"] if "query" in route} >= {
        "build_workbench_view",
        "build_schema_contract",
        "build_service_contract",
        "build_release_evidence",
    }

    permissions = predictive_demand_permissions_contract()
    assert permissions["action_permissions"]["register_schema_extension"] == (
        "predictive_demand.configure"
    )
    assert permissions["action_permissions"]["build_schema_contract"] == (
        "predictive_demand.audit"
    )
    assert permissions["action_permissions"]["build_service_contract"] == (
        "predictive_demand.audit"
    )
    assert permissions["action_permissions"]["build_release_evidence"] == (
        "predictive_demand.audit"
    )

    schema = predictive_demand_build_schema_contract()
    assert tuple(item["table"] for item in schema["tables"]) == PREDICTIVE_DEMAND_OWNED_TABLES
    assert all(
        migration["backend_allowlist"] == PREDICTIVE_DEMAND_ALLOWED_DATABASE_BACKENDS
        for migration in schema["migrations"]
    )
    assert all(model["class_name"] for model in schema["models"])

    service = predictive_demand_build_service_contract()
    assert service["generated_service_artifacts"]["events"]["emits"] == tuple(
        {
            "event_type": event_type,
            "topic": PREDICTIVE_DEMAND_REQUIRED_EVENT_TOPIC,
            "outbox_table": PREDICTIVE_DEMAND_RUNTIME_TABLES[0],
        }
        for event_type in PREDICTIVE_DEMAND_EMITTED_EVENT_TYPES
    )
    assert service["generated_service_artifacts"]["events"]["consumes"] == tuple(
        {
            "event_type": event_type,
            "topic": PREDICTIVE_DEMAND_REQUIRED_EVENT_TOPIC,
            "inbox_table": PREDICTIVE_DEMAND_RUNTIME_TABLES[1],
        }
        for event_type in PREDICTIVE_DEMAND_CONSUMED_EVENT_TYPES
    )
    assert len(service["generated_service_artifacts"]["services"]) >= 10
    assert len(service["generated_service_artifacts"]["routes"]) >= 9
    assert all(
        handler["idempotent"] is True
        and handler["dead_letter_table"] == PREDICTIVE_DEMAND_RUNTIME_TABLES[2]
        for handler in service["generated_service_artifacts"]["handlers"]
    )


def test_predictive_demand_release_evidence_proves_boundary_retry_dead_letter_and_allowlist() -> None:
    state = predictive_demand_empty_state()
    with pytest.raises(ValueError, match="PostgreSQL, MySQL, or MariaDB"):
        predictive_demand_configure_runtime(
            state,
            {
                "database_backend": "stream_store",
                "event_topic": PREDICTIVE_DEMAND_REQUIRED_EVENT_TOPIC,
                "retry_limit": 3,
                "default_uom": "EA",
                "supported_regions": ("US",),
                "supported_signal_types": ("shipment", "inventory"),
                "planning_granularity": "daily",
                "default_timezone": "UTC",
                "shortage_policy": "service_level",
                "workbench_limit": 50,
            },
        )

    state = _configured_state()
    with pytest.raises(ValueError, match="Unsupported Predictive Demand parameter"):
        predictive_demand_set_parameter(state, "stream_engine", 1)
    with pytest.raises(ValueError, match="cannot extend non-owned table"):
        predictive_demand_register_schema_extension(
            state, "inventory_pool", {"quantity": "numeric"}
        )

    failed = predictive_demand_receive_event(
        state,
        {
            "event_id": "evt_fail",
            "event_type": "OrderShipped",
            "payload": {
                "tenant": "tenant_ops",
                "sku": "SKU-OPS",
                "location": "DC-1",
                "region": "US",
                "quantity": 10,
            },
        },
        simulate_failure=True,
    )
    assert failed["ok"] is False
    assert failed["handler"]["status"] == "dead_letter"
    assert len(failed["state"]["dead_letter"]) == 1

    boundary = predictive_demand_verify_owned_table_boundary(
        (
            "forecast_model",
            "forecast_run",
            "demand_signal",
            "forecast_result",
            PREDICTIVE_DEMAND_RUNTIME_TABLES[0],
            PREDICTIVE_DEMAND_RUNTIME_TABLES[1],
            PREDICTIVE_DEMAND_RUNTIME_TABLES[2],
            "OrderShipped",
            "shipment_projection",
            "GET /predictive-demand/release-evidence",
        )
    )
    assert boundary["ok"] is True
    assert boundary["owned_tables"] == PREDICTIVE_DEMAND_OWNED_TABLES
    assert boundary["declared_dependencies"]["shared_tables"] == ()
    violated = predictive_demand_verify_owned_table_boundary(("inventory_pool",))
    assert violated["ok"] is False
    assert violated["violations"] == ("inventory_pool",)

    release = predictive_demand_build_release_evidence()
    assert release["ok"] is True
    assert not release["blocking_gaps"]
    assert {check["id"] for check in release["checks"]} >= {
        "runtime_event_tables_declared",
        "appgen_x_eventing_only",
        "retry_dead_letter_and_idempotency",
        "generated_artifacts_present",
        "backend_allowlist_and_boundary",
        "no_shared_table_access",
    }
    assert all(check["ok"] for check in release["checks"])
    assert release["schema_contract"]["database_backends"] == (
        PREDICTIVE_DEMAND_ALLOWED_DATABASE_BACKENDS
    )
    assert release["api_contract"]["database_backends"] == (
        PREDICTIVE_DEMAND_ALLOWED_DATABASE_BACKENDS
    )
    assert release["service_contract"]["retry_dead_letter_evidence"]["dead_letter_table"] == (
        PREDICTIVE_DEMAND_RUNTIME_TABLES[2]
    )
    assert release["permissions_contract"]["action_permissions"]["build_release_evidence"] == (
        "predictive_demand.audit"
    )
    assert release["generated_artifacts"]["migrations"][0]["path"].endswith(
        "001_forecast_model.sql"
    )
    assert release["generated_artifacts"]["models"][0]["module_path"].startswith(
        "pyAppGen.pbcs.predictive_demand.models."
    )
    assert len(release["generated_artifacts"]["services"]) >= 10
    assert len(release["generated_artifacts"]["routes"]) >= 9
    assert release["generated_artifacts"]["events"]["emits"][0]["topic"] == (
        PREDICTIVE_DEMAND_REQUIRED_EVENT_TOPIC
    )
    assert release["generated_artifacts"]["handlers"][0]["handler"] == "receive_event"
    assert any(
        artifact["fragment"] == "PredictiveDemandWorkbench"
        for artifact in release["generated_artifacts"]["ui"]
    )
    assert release["control_evidence"]["handled"]["status"] == "handled"
    assert release["control_evidence"]["duplicate"]["status"] == "duplicate"
    assert release["control_evidence"]["failed"]["status"] == "dead_letter"
    assert release["control_evidence"]["workbench"]["binding_evidence"]["runtime_tables"] == (
        PREDICTIVE_DEMAND_RUNTIME_TABLES
    )
    assert release["control_evidence"]["rendered"]["binding_evidence"]["runtime_tables"] == (
        PREDICTIVE_DEMAND_RUNTIME_TABLES
    )


def _configured_state() -> dict:
    state = predictive_demand_empty_state()
    state = predictive_demand_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": PREDICTIVE_DEMAND_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "default_uom": "EA",
            "supported_regions": ("US",),
            "supported_signal_types": (
                "shipment",
                "inventory",
                "operational",
                "manual",
                "promotion",
            ),
            "planning_granularity": "daily",
            "default_timezone": "UTC",
            "shortage_policy": "service_level",
            "workbench_limit": 50,
        },
    )["state"]
    for name, value in (
        ("forecast_horizon_days", 14),
        ("history_window_days", 180),
        ("service_level_target", 0.95),
        ("promotion_lift_default", 15.0),
        ("causal_weight", 0.4),
        ("anomaly_threshold", 2.5),
        ("retrain_cadence_days", 14),
        ("shortage_alert_days", 21),
        ("bias_tolerance_percent", 10.0),
        ("workbench_limit", 50),
    ):
        state = predictive_demand_set_parameter(state, name, value)["state"]
    state = predictive_demand_register_rule(
        state,
        {
            "rule_id": "rule_ops",
            "tenant": "tenant_ops",
            "scope": "predictive_demand",
            "status": "active",
            "allowed_signal_types": (
                "shipment",
                "inventory",
                "operational",
                "manual",
                "promotion",
            ),
            "allowed_regions": ("US",),
            "consensus_policy": {
                "planner_override_limit_percent": 20.0,
                "consensus_required": True,
            },
            "forecast_policy": {
                "default_algorithm": "ensemble",
                "allow_causal_inputs": True,
            },
            "shortage_policy": {
                "emit_material_shortage": True,
                "minimum_shortage_quantity": 1.0,
            },
        },
    )["state"]
    return state
