"""Focused package contract and standalone tests for streaming_analytics."""

from __future__ import annotations

from pyAppGen.pbc import pbc_generation_smoke_audit
from pyAppGen.pbc import pbc_implementation_release_audit
from pyAppGen.pbc import pbc_source_artifact_contract

from .. import PBC_KEY
from .. import capability_assurance
from .. import config
from .. import events
from .. import handlers
from .. import package_discovery_plan
from .. import package_metadata_manifest
from .. import permissions
from .. import register_pbc
from .. import registration_plan
from .. import validate_package_metadata
from .. import release_evidence
from .. import routes
from .. import runtime
from .. import schema_contract
from .. import seed_data
from .. import services
from .. import smoke_test
from .. import standalone
from .. import ui
from ..agent import composed_agent_contribution
from ..agent import datastore_crud_plan
from ..agent import document_instruction_plan
from ..agent import smoke_test as agent_smoke_test
from ..manifest import PBC_MANIFEST
from ..models import model_manifest
from ..service_contract import SERVICE_CONTRACT


def _configured_state() -> dict:
    state = runtime.streaming_analytics_empty_state()
    state = runtime.streaming_analytics_configure_runtime(state, seed_data.default_configuration())["state"]
    for name, value in seed_data.default_parameter_values().items():
        state = runtime.streaming_analytics_set_parameter(state, name, value)["state"]
    for rule in seed_data.default_rules():
        state = runtime.streaming_analytics_register_rule(state, rule)["state"]
    return state


def test_generated_schema_service_and_release_evidence():
    assert schema_contract.build_schema_contract()["pbc"] == PBC_KEY
    assert schema_contract.validate_schema_contract()["ok"] is True
    assert model_manifest()["ok"] is True
    assert SERVICE_CONTRACT["pbc"] == PBC_KEY
    assert SERVICE_CONTRACT["ok"] is True
    assert SERVICE_CONTRACT["shared_table_access"] is False
    assert release_evidence.build_release_evidence()["ok"] is True
    assert release_evidence.validate_release_evidence()["ok"] is True
    assert release_evidence.smoke_test()["ok"] is True


def test_agent_chatbot_skills_are_executable():
    document = document_instruction_plan(
        "stream_id=stream_test tenant=tenant_test event_type=operational metric_field=latency_ms aggregation=avg region=US",
        "create ingestion contract, replay plan, watermark controls and anomaly dashboard",
    )
    read_plan = datastore_crud_plan("read")
    create_plan = datastore_crud_plan("create", "streaming_analytics_metric_stream", {"status": "draft"})
    rejected_foreign = datastore_crud_plan("update", table="foreign_table", payload={"status": "draft"})
    contribution = composed_agent_contribution()
    smoke = agent_smoke_test()
    assert document["ok"] is True
    assert read_plan["ok"] is True
    assert create_plan["ok"] is True
    assert rejected_foreign["ok"] is False
    assert contribution["ok"] is True
    assert smoke["ok"] is True
    assert create_plan["event_contract"] == "AppGen-X"


def test_manifest_and_event_contract():
    manifest = events.event_contract_manifest()
    validation = events.validate_event_contract()
    metadata_validation = validate_package_metadata()
    readiness = release_evidence.release_readiness_manifest()
    assert PBC_MANIFEST["pbc"] == PBC_KEY
    assert manifest["ok"] is True
    assert validation["ok"] is True
    assert metadata_validation["ok"] is True
    assert readiness["pbc"] == PBC_KEY
    assert manifest["stream_engine_picker_visible"] is False


def test_registration_plan_is_side_effect_free():
    assert register_pbc()["pbc"] == PBC_KEY
    plan = registration_plan()
    metadata = package_metadata_manifest()
    discovery = package_discovery_plan()
    assert plan["ok"] is True
    assert plan["catalog_patch"]
    assert metadata["ok"] is True
    assert discovery["ok"] is True
    assert not validate_package_metadata()["missing_entrypoints"]


def test_service_and_route_surface_are_executable():
    service_smoke = services.smoke_test()
    route_validation = routes.validate_api_route_contracts()
    route_smoke = routes.smoke_test()
    assert service_smoke["ok"] is True
    assert services.service_operation_contracts()["ok"] is True
    assert route_validation["ok"] is True
    assert route_smoke["ok"] is True
    assert not route_validation["service_mismatches"]
    assert not route_validation["missing_idempotency"]
    assert not route_validation["invalid_table_scope"]


def test_configuration_permissions_seed_and_ui_are_executable():
    assert config.smoke_test()["ok"] is True
    assert config.governance_smoke_test()["ok"] is True
    assert permissions.smoke_test()["ok"] is True
    assert seed_data.smoke_test()["ok"] is True
    assert ui.smoke_test()["ok"] is True
    assert standalone.smoke_test()["ok"] is True
    assert smoke_test()["ok"] is True


def test_configuration_permissions_and_seed_hooks_are_executable():
    assert config.governance_smoke_test()["ok"] is True
    assert permissions.permission_manifest()["ok"] is True
    assert seed_data.validate_seed_data()["ok"] is True


def test_event_handlers_are_idempotent_and_retryable():
    manifest = handlers.handler_manifest()
    first = handlers.dispatch_event(
        {
            "event_type": "PaymentCaptured",
            "event_id": "handler-idempotency",
            "payload": {"tenant": "tenant_handler", "amount": 25.0, "region": "US"},
        },
    )
    second = handlers.dispatch_event(
        {
            "event_type": "PaymentCaptured",
            "event_id": "handler-idempotency",
            "payload": {"tenant": "tenant_handler", "amount": 25.0, "region": "US"},
        },
    )
    assert manifest["ok"] is True
    assert manifest["retry_policies"][0]["max_attempts"] >= 3
    assert manifest["dead_letter_tables"][0].startswith("streaming_analytics_")
    assert first["handled"] is True
    assert second["handled"] is True
    assert second["duplicate"] is True


def test_event_handlers_and_capability_assurance_are_executable():
    handler_smoke = handlers.smoke_test()
    assurance = capability_assurance.smoke_test()
    assert handler_smoke["ok"] is True
    assert assurance["ok"] is True


def test_runtime_smoke_and_streaming_workspace_are_executable():
    runtime_smoke = runtime.streaming_analytics_runtime_smoke()
    state = _configured_state()
    state = runtime.streaming_analytics_register_metric_stream(
        state,
        {
            "stream_id": "stream_contract",
            "tenant": "tenant_test",
            "name": "Contract Stream",
            "event_type": "operational",
            "metric_field": "latency_ms",
            "aggregation": "avg",
            "region": "US",
            "status": "active",
        },
    )["state"]
    state = runtime.streaming_analytics_define_window(
        state,
        {
            "window_id": "window_contract",
            "tenant": "tenant_test",
            "stream_id": "stream_contract",
            "window_minutes": 15,
            "status": "active",
        },
    )["state"]
    state = runtime.streaming_analytics_ingest_metric_event(
        state,
        {
            "event_id": "event_contract",
            "tenant": "tenant_test",
            "event_type": "operational",
            "region": "US",
            "values": {"latency_ms": 250.0},
        },
    )["state"]
    state = runtime.streaming_analytics_create_dashboard_projection(
        state,
        {
            "projection_id": "projection_contract",
            "tenant": "tenant_test",
            "name": "Contract Dashboard",
            "stream_ids": ("stream_contract",),
            "status": "active",
        },
    )["state"]
    workbench = runtime.streaming_analytics_build_workbench_view(state, tenant="tenant_test")
    assert runtime_smoke["ok"] is True
    assert workbench["stream_count"] == 1
    assert workbench["projection_count"] == 1
    assert workbench["event_contract"] == "AppGen-X"


def test_release_and_generation_audits_for_streaming_analytics_only():
    source = pbc_source_artifact_contract(PBC_KEY)
    implementation = pbc_implementation_release_audit((PBC_KEY,))
    generation = pbc_generation_smoke_audit((PBC_KEY,))
    assert source["ok"] is True
    assert implementation["ok"] is True
    assert generation["ok"] is True
