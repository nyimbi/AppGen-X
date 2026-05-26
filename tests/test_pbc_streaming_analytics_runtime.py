import pytest

from pyAppGen.pbcs.streaming_analytics import STREAMING_ANALYTICS_ALLOWED_DATABASE_BACKENDS
from pyAppGen.pbcs.streaming_analytics import STREAMING_ANALYTICS_OWNED_TABLES
from pyAppGen.pbcs.streaming_analytics import STREAMING_ANALYTICS_RUNTIME_CAPABILITY_KEYS
from pyAppGen.pbcs.streaming_analytics import implementation_contract
from pyAppGen.pbcs.streaming_analytics import streaming_analytics_build_api_contract
from pyAppGen.pbcs.streaming_analytics import streaming_analytics_build_release_evidence
from pyAppGen.pbcs.streaming_analytics import streaming_analytics_build_schema_contract
from pyAppGen.pbcs.streaming_analytics import streaming_analytics_build_service_contract
from pyAppGen.pbcs.streaming_analytics import streaming_analytics_build_workbench_view
from pyAppGen.pbcs.streaming_analytics import streaming_analytics_configure_runtime
from pyAppGen.pbcs.streaming_analytics import streaming_analytics_create_dashboard_projection
from pyAppGen.pbcs.streaming_analytics import streaming_analytics_define_window
from pyAppGen.pbcs.streaming_analytics import streaming_analytics_empty_state
from pyAppGen.pbcs.streaming_analytics import streaming_analytics_ingest_metric_event
from pyAppGen.pbcs.streaming_analytics import streaming_analytics_receive_event
from pyAppGen.pbcs.streaming_analytics import streaming_analytics_register_metric_stream
from pyAppGen.pbcs.streaming_analytics import streaming_analytics_register_rule
from pyAppGen.pbcs.streaming_analytics import streaming_analytics_register_schema_extension
from pyAppGen.pbcs.streaming_analytics import streaming_analytics_render_workbench
from pyAppGen.pbcs.streaming_analytics import streaming_analytics_runtime_capabilities
from pyAppGen.pbcs.streaming_analytics import streaming_analytics_runtime_smoke
from pyAppGen.pbcs.streaming_analytics import streaming_analytics_set_parameter
from pyAppGen.pbcs.streaming_analytics import streaming_analytics_permissions_contract
from pyAppGen.pbcs.streaming_analytics import streaming_analytics_ui_contract
from pyAppGen.pbcs.streaming_analytics import streaming_analytics_verify_owned_table_boundary


def test_streaming_analytics_runtime_executes_standard_and_advanced_capabilities() -> None:
    runtime = streaming_analytics_runtime_capabilities()
    smoke = streaming_analytics_runtime_smoke()

    assert runtime["format"] == "appgen.streaming-analytics-runtime-capabilities.v1"
    assert runtime["ok"] is True
    assert runtime["implementation_directory"] == "src/pyAppGen/pbcs/streaming_analytics"
    assert runtime["owned_tables"] == STREAMING_ANALYTICS_OWNED_TABLES
    assert runtime["runtime_tables"] == (
        "streaming_analytics_appgen_outbox_event",
        "streaming_analytics_appgen_inbox_event",
        "streaming_analytics_dead_letter_event",
    )
    assert {"build_schema_contract", "build_service_contract", "build_release_evidence"} <= set(runtime["operations"])
    assert len(runtime["standard_features"]) >= 20
    assert "configuration_schema" in runtime["standard_features"]
    assert "rule_engine" in runtime["standard_features"]
    assert "workbench" in runtime["standard_features"]
    assert smoke["ok"] is True
    assert {check["id"] for check in smoke["checks"]} == set(STREAMING_ANALYTICS_RUNTIME_CAPABILITY_KEYS)
    assert not smoke["blocking_gaps"]


def test_streaming_analytics_builders_publish_complete_pbc_contracts() -> None:
    schema = streaming_analytics_build_schema_contract()
    service = streaming_analytics_build_service_contract()
    release = streaming_analytics_build_release_evidence()
    package = implementation_contract()

    assert schema["ok"] is True
    assert tuple(table["table"] for table in schema["tables"]) == STREAMING_ANALYTICS_OWNED_TABLES
    assert tuple(table["table"] for table in schema["runtime_tables"]) == (
        "streaming_analytics_appgen_outbox_event",
        "streaming_analytics_appgen_inbox_event",
        "streaming_analytics_dead_letter_event",
    )
    assert {migration["table"] for migration in schema["migrations"]} == set(STREAMING_ANALYTICS_OWNED_TABLES)
    assert {model["table"] for model in schema["models"]} == set(STREAMING_ANALYTICS_OWNED_TABLES)
    assert all(tuple(migration["backend_allowlist"]) == STREAMING_ANALYTICS_ALLOWED_DATABASE_BACKENDS for migration in schema["migrations"])
    assert schema["datastore_backends"] == STREAMING_ANALYTICS_ALLOWED_DATABASE_BACKENDS
    assert schema["shared_table_access"] is False

    assert service["ok"] is True
    assert {
        "configure_runtime",
        "register_metric_stream",
        "define_window",
        "receive_event",
        "ingest_metric_event",
        "create_dashboard_projection",
    } <= set(service["command_methods"])
    assert {"build_schema_contract", "build_service_contract", "build_release_evidence"} <= set(service["query_methods"])
    assert service["eventing"]["contract"] == "AppGen-X"
    assert service["eventing"]["outbox_table"] == "streaming_analytics_appgen_outbox_event"
    assert service["eventing"]["inbox_table"] == "streaming_analytics_appgen_inbox_event"
    assert service["eventing"]["dead_letter_table"] == "streaming_analytics_dead_letter_event"
    assert service["configuration"]["allowed_database_backends"] == STREAMING_ANALYTICS_ALLOWED_DATABASE_BACKENDS
    assert service["configuration"]["stream_engine_picker_visible"] is False
    assert service["permissions"]["build_release_evidence"] == "streaming_analytics.audit"
    assert service["idempotent_handlers"] == ("receive_event",)
    assert {handler["event_type"] for handler in service["handlers"]} == {
        "AuditEventSealed",
        "OrderShipped",
        "PaymentCaptured",
    }
    assert {route["route"] for route in service["routes"]} >= {
        "POST /metric-streams",
        "GET /streaming-analytics/schema-contract",
        "GET /streaming-analytics/service-contract",
        "GET /streaming-analytics/release-evidence",
    }
    assert {artifact["kind"] for artifact in service["service_artifacts"]} == {"command", "query"}
    assert len(service["ui_artifacts"]) >= 5
    assert service["external_dependencies"]["shared_tables"] == ()

    assert release["ok"] is True
    assert not release["blocking_gaps"]
    assert release["generated_artifacts"]["events"]["contract"] == "AppGen-X"
    assert release["generated_artifacts"]["events"]["consumes"] == (
        "AuditEventSealed",
        "OrderShipped",
        "PaymentCaptured",
    )
    assert len(release["generated_artifacts"]["handlers"]) == 3
    assert len(release["generated_artifacts"]["ui"]) >= 5
    assert release["control"]["summary"]["outbox_table"] == "streaming_analytics_appgen_outbox_event"
    assert release["control"]["summary"]["inbox_table"] == "streaming_analytics_appgen_inbox_event"
    assert release["control"]["summary"]["dead_letter_table"] == "streaming_analytics_dead_letter_event"
    assert release["control"]["summary"]["outbox_event_types"] == ("OperationalKpiChanged", "ForecastUpdated")
    assert release["control"]["summary"]["inbox_event_types"] == ("PaymentCaptured",)
    assert release["control"]["summary"]["dead_letter_event_types"] == ("OrderShipped",)
    assert release["control"]["summary"]["duplicate_status"] == "duplicate"
    assert release["control"]["summary"]["dead_letter_status"] == "dead_letter"
    assert release["control"]["artifacts"]["handled_inbox_record"]["contract"] == "AppGen-X"
    assert release["control"]["artifacts"]["handled_inbox_record"]["runtime_table"] == "streaming_analytics_appgen_inbox_event"
    assert all(record["contract"] == "AppGen-X" for record in release["control"]["artifacts"]["handled_outbox_records"])
    assert all(record["runtime_table"] == "streaming_analytics_appgen_outbox_event" for record in release["control"]["artifacts"]["handled_outbox_records"])
    assert release["control"]["artifacts"]["dead_letter_record"]["runtime_table"] == "streaming_analytics_dead_letter_event"
    assert release["schema"]["shared_table_access"] is False
    assert release["api"]["shared_table_access"] is False
    assert release["service"]["external_dependencies"]["shared_tables"] == ()

    assert package["schema_contract"]["ok"] is True
    assert package["service_contract"]["ok"] is True
    assert package["release_evidence_contract"]["ok"] is True
    assert package["required_event_topic"] == "appgen.streaming_analytics.events"
    assert package["consumes"] == ("AuditEventSealed", "OrderShipped", "PaymentCaptured")
    assert package["emits"] == ("ForecastUpdated", "OperationalKpiChanged")


def test_streaming_analytics_runtime_applies_rules_parameters_events_and_ui() -> None:
    state = _configured_state()
    state = streaming_analytics_register_metric_stream(
        state,
        {"stream_id": "stream_ops", "tenant": "tenant_ops", "name": "Payments", "event_type": "payment", "metric_field": "amount", "aggregation": "sum", "region": "US", "status": "active"},
    )["state"]
    state = streaming_analytics_define_window(
        state,
        {"window_id": "window_ops", "tenant": "tenant_ops", "stream_id": "stream_ops", "window_minutes": 15, "status": "active"},
    )["state"]
    state = streaming_analytics_receive_event(
        state,
        {"event_id": "pay_ops", "event_type": "PaymentCaptured", "payload": {"tenant": "tenant_ops", "region": "US", "amount": 1200.0, "currency": "USD"}},
    )["state"]
    extension = streaming_analytics_register_schema_extension(state, "kpi_snapshot", {"risk_features": "jsonb"})
    state = extension["state"]
    assert extension["extension"]["version"] == 1
    state = streaming_analytics_ingest_metric_event(
        state,
        {"event_id": "metric_ops", "tenant": "tenant_ops", "event_type": "payment", "region": "US", "values": {"amount": 300.0}},
    )["state"]
    state = streaming_analytics_create_dashboard_projection(
        state,
        {"projection_id": "proj_ops", "tenant": "tenant_ops", "name": "Ops", "stream_ids": ("stream_ops",), "status": "active"},
    )["state"]
    assert state["kpi_snapshots"]["stream_ops:latest"]["value"] == 1500.0
    assert state["outbox"][-1]["idempotency_key"].startswith("streaming_analytics:ForecastUpdated")

    workbench = streaming_analytics_build_workbench_view(state, tenant="tenant_ops")
    assert workbench["stream_count"] == 1
    assert workbench["window_count"] == 1
    assert workbench["snapshot_count"] == 1
    assert workbench["projection_count"] == 1
    assert workbench["event_count"] == 2
    assert workbench["configuration_bound"] is True
    assert workbench["rule_count"] == 1
    assert workbench["parameter_count"] == 10

    ui_contract = streaming_analytics_ui_contract()
    assert ui_contract["configuration_editor"]["allowed_database_backends"] == STREAMING_ANALYTICS_ALLOWED_DATABASE_BACKENDS
    assert ui_contract["configuration_editor"]["stream_engine_picker_visible"] is False
    rendered = streaming_analytics_render_workbench(
        state,
        tenant="tenant_ops",
        principal_permissions=(
            "streaming_analytics.stream.write",
            "streaming_analytics.window.write",
            "streaming_analytics.event.write",
            "streaming_analytics.event.consume",
            "streaming_analytics.configure",
            "streaming_analytics.audit",
        ),
    )
    assert rendered["ok"] is True
    assert not rendered["locked_actions"]
    assert rendered["binding_evidence"]["owned_tables"] == STREAMING_ANALYTICS_OWNED_TABLES

    api_contract = streaming_analytics_build_api_contract()
    assert api_contract["stream_engine_picker_visible"] is False
    assert api_contract["shared_table_access"] is False
    assert api_contract["required_event_topic"] == "appgen.streaming_analytics.events"
    assert api_contract["runtime_tables"] == (
        "streaming_analytics_appgen_outbox_event",
        "streaming_analytics_appgen_inbox_event",
        "streaming_analytics_dead_letter_event",
    )
    assert {route["command"] for route in api_contract["routes"] if "command" in route} >= {
        "register_metric_stream",
        "define_window",
        "ingest_metric_event",
    }
    assert {route["query"] for route in api_contract["routes"] if "query" in route} >= {
        "build_workbench_view",
        "build_schema_contract",
        "build_service_contract",
        "build_release_evidence",
    }
    permissions = streaming_analytics_permissions_contract()
    assert "streaming_analytics_admin" in permissions["roles"]
    assert "shared_table_access_forbidden" in permissions["policy_controls"]
    assert permissions["action_permissions"]["build_release_evidence"] == "streaming_analytics.audit"


def test_streaming_analytics_rejects_invalid_inputs_and_proves_boundary_and_dead_letters() -> None:
    state = streaming_analytics_empty_state()
    with pytest.raises(ValueError, match="PostgreSQL, MySQL, or MariaDB"):
        streaming_analytics_configure_runtime(
            state,
            {
                "database_backend": "stream_store",
                "event_topic": "appgen.streaming_analytics.events",
                "retry_limit": 3,
                "default_timezone": "UTC",
                "supported_event_types": ("payment",),
                "supported_regions": ("US",),
                "retention_days": 90,
                "watermark_seconds": 120,
                "aggregation_mode": "policy",
                "workbench_limit": 50,
            },
        )

    state = _configured_state()
    with pytest.raises(ValueError, match="Unsupported Streaming Analytics parameter"):
        streaming_analytics_set_parameter(state, "stream_engine", 1)

    failed = streaming_analytics_receive_event(
        state,
        {"event_id": "evt_fail", "event_type": "PaymentCaptured", "payload": {"tenant": "tenant_ops", "region": "US"}},
        simulate_failure=True,
    )
    assert failed["ok"] is False
    assert failed["handler"]["status"] == "dead_letter"
    assert len(failed["state"]["dead_letter"]) == 1
    assert failed["state"]["dead_letter"][0]["contract"] == "AppGen-X"
    assert failed["state"]["dead_letter"][0]["runtime_table"] == "streaming_analytics_dead_letter_event"

    boundary = streaming_analytics_verify_owned_table_boundary(
        (
            "metric_stream",
            "kpi_snapshot",
            "streaming_analytics_appgen_outbox_event",
            "audit_ledger.AuditEventSealed",
            "GET /kpis",
        )
    )
    assert boundary["ok"] is True
    assert boundary["owned_tables"] == ("metric_stream", "aggregation_window", "kpi_snapshot", "dashboard_projection")
    assert boundary["runtime_tables"] == (
        "streaming_analytics_appgen_outbox_event",
        "streaming_analytics_appgen_inbox_event",
        "streaming_analytics_dead_letter_event",
    )
    assert boundary["declared_dependencies"]["shared_tables"] == ()
    violated = streaming_analytics_verify_owned_table_boundary(("payment_intent",))
    assert violated["ok"] is False
    assert violated["violations"] == ("payment_intent",)

    with pytest.raises(ValueError, match="cannot extend non-owned table"):
        streaming_analytics_register_schema_extension(state, "payment_intent", {"amount": "numeric"})


def _configured_state() -> dict:
    state = streaming_analytics_empty_state()
    state = streaming_analytics_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": "appgen.streaming_analytics.events",
            "retry_limit": 3,
            "default_timezone": "UTC",
            "supported_event_types": ("audit", "order", "payment", "operational"),
            "supported_regions": ("US",),
            "retention_days": 90,
            "watermark_seconds": 120,
            "aggregation_mode": "policy",
            "workbench_limit": 50,
        },
    )["state"]
    for name, value in (
        ("default_window_minutes", 15),
        ("late_event_tolerance_seconds", 120),
        ("quality_score_threshold", 0.9),
        ("forecast_horizon_minutes", 240),
        ("alert_threshold_multiplier", 1.5),
        ("replay_batch_limit", 5000),
        ("kpi_confidence_threshold", 0.75),
        ("projection_refresh_seconds", 30),
        ("max_events_per_window", 100000),
        ("workbench_limit", 50),
    ):
        state = streaming_analytics_set_parameter(state, name, value)["state"]
    state = streaming_analytics_register_rule(
        state,
        {
            "rule_id": "rule_ops",
            "tenant": "tenant_ops",
            "scope": "streaming_analytics",
            "status": "active",
            "allowed_event_types": ("audit", "order", "payment", "operational"),
            "allowed_regions": ("US",),
            "quality_policy": {"minimum_score": 0.9, "drop_invalid": True},
            "aggregation_policy": {"default_function": "sum", "watermark_seconds": 120},
            "alert_policy": {"emit_on_threshold": True, "severity": "medium"},
        },
    )["state"]
    return state
