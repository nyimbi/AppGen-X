"""Focused package contract and gate tests for dam_core."""

from __future__ import annotations

from pathlib import Path

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
from .. import ui
from ..agent import datastore_crud_plan
from ..agent import document_instruction_plan
from ..manifest import PBC_MANIFEST
from ..models import database_model_contract
from ..models import model_manifest
from ..service_contract import SERVICE_CONTRACT


PACKAGE_DIR = Path(__file__).resolve().parents[1]


def _configured_state() -> dict:
    state = runtime.dam_core_empty_state()
    state = runtime.dam_core_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": runtime.DAM_CORE_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "default_storage_tier": "warm",
            "allowed_mime_types": ("image/jpeg",),
            "rendition_profiles": ("web_large",),
            "rights_default_decision": "review",
            "metadata_taxonomies": ("product",),
            "default_locale": "en-US",
            "workbench_limit": 100,
        },
    )["state"]
    for name, value in (
        ("max_asset_size_mb", 1000),
        ("quality_threshold", 0.7),
        ("rights_risk_threshold", 0.6),
        ("transcode_retry_limit", 3),
        ("duplicate_similarity_threshold", 0.9),
        ("rendition_cost_weight", 0.35),
        ("carbon_cost_weight", 0.15),
        ("usage_forecast_horizon_days", 90),
        ("metadata_confidence_floor", 0.6),
        ("workbench_limit", 100),
    ):
        state = runtime.dam_core_set_parameter(state, name, value)["state"]
    return state


def test_generated_schema_service_and_release_evidence():
    assert schema_contract.build_schema_contract()["pbc"] == PBC_KEY
    assert schema_contract.validate_schema_contract()["ok"] is True
    assert model_manifest()["ok"] is True
    assert database_model_contract()["ok"] is True
    assert SERVICE_CONTRACT["pbc"] == PBC_KEY
    assert SERVICE_CONTRACT["ok"] is True
    assert SERVICE_CONTRACT["shared_table_access"] is False
    assert release_evidence.build_release_evidence()["ok"] is True
    assert release_evidence.validate_release_evidence()["ok"] is True
    assert release_evidence.smoke_test()["ok"] is True


def test_manifest_event_and_package_metadata_are_consistent():
    manifest = events.event_contract_manifest()
    validation = events.validate_event_contract()
    metadata = package_metadata_manifest()
    discovery = package_discovery_plan()
    assert PBC_MANIFEST["pbc"] == PBC_KEY
    assert manifest["ok"] is True
    assert validation["ok"] is True
    assert metadata["ok"] is True
    assert discovery["ok"] is True
    assert manifest["outbox_table"].startswith("dam_core_")
    assert manifest["inbox_table"].startswith("dam_core_")
    assert metadata["event_contract"] == "AppGen-X"
    assert metadata["stream_engine_picker_visible"] is False


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


def test_registration_plan_is_side_effect_free():
    assert register_pbc()["pbc"] == PBC_KEY
    plan = registration_plan()
    assert plan["ok"] is True
    assert plan["catalog_patch"]


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


def test_configuration_permissions_and_seed_hooks_are_executable():
    assert config.governance_smoke_test()["ok"] is True
    assert permissions.permission_manifest()["ok"] is True
    assert seed_data.validate_seed_data()["ok"] is True


def test_event_handlers_agent_and_capability_assurance_are_executable():
    handler_smoke = handlers.smoke_test()
    assurance = capability_assurance.smoke_test()
    document_plan = document_instruction_plan(
        "asset_id=asset_test tenant=tenant_test filename=asset.jpg mime_type=image/jpeg taxonomy=product value=launch",
        "register asset and tag product launch",
    )
    crud_plan = datastore_crud_plan("create", "dam_core_asset", {"status": "draft"})
    assert handler_smoke["ok"] is True
    assert assurance["ok"] is True
    assert document_plan["ok"] is True
    assert crud_plan["ok"] is True
    assert crud_plan["event_contract"] == "AppGen-X"


def test_event_handlers_are_idempotent_and_retryable():
    manifest = handlers.handler_manifest()
    first = handlers.dispatch_event(
        {
            "event_type": "ProductPublished",
            "event_id": "handler-idempotency",
            "payload": {"tenant": "tenant_handler", "product_id": "sku_handler"},
        },
    )
    second = handlers.dispatch_event(
        {
            "event_type": "ProductPublished",
            "event_id": "handler-idempotency",
            "payload": {"tenant": "tenant_handler", "product_id": "sku_handler"},
        },
    )
    assert manifest["ok"] is True
    assert manifest["retry_policies"][0]["max_attempts"] >= 3
    assert manifest["dead_letter_tables"][0].startswith("dam_core_")
    assert first["handled"] is True
    assert second["handled"] is True
    assert second["duplicate"] is True


def test_runtime_smoke_and_one_asset_lifecycle_are_executable():
    runtime_smoke = runtime.dam_core_runtime_smoke()
    state = _configured_state()
    state = runtime.dam_core_register_rule(
        state,
        {
            "rule_id": "dam_core.asset_governance",
            "tenant": "tenant_test",
            "scope": "asset_governance",
            "status": "active",
            "mime_policy": {"allowed": ("image/jpeg",)},
            "rights_policy": {"blocked_markets": ("restricted",)},
            "rendition_policy": {"required_profiles": ("web_large",)},
            "metadata_policy": {"required_tags": ("product",)},
        },
    )["state"]
    state = runtime.dam_core_receive_event(
        state,
        {
            "event_type": "ProductPublished",
            "event_id": "product_test",
            "payload": {
                "tenant": "tenant_test",
                "product_id": "sku_test",
                "name": "Launch Backpack",
            },
        },
    )["state"]
    state = runtime.dam_core_register_asset(
        state,
        {
            "asset_id": "asset_test",
            "tenant": "tenant_test",
            "filename": "asset.jpg",
            "mime_type": "image/jpeg",
            "size_mb": 12,
            "storage_uri": "object://dam/test/asset.jpg",
            "binary": b"asset-test",
            "created_by": "tester",
            "product_id": "sku_test",
        },
    )["state"]
    state = runtime.dam_core_attach_rights_policy(
        state,
        {
            "policy_id": "policy_test",
            "asset_id": "asset_test",
            "tenant": "tenant_test",
            "license_type": "commercial",
            "allowed_markets": ("ke",),
            "blocked_markets": ("restricted",),
            "expires_at": "2027-01-01",
            "attribution_required": True,
            "approver": "legal",
        },
    )["state"]
    state = runtime.dam_core_add_metadata_tag(
        state,
        {
            "tag_id": "tag_test",
            "asset_id": "asset_test",
            "tenant": "tenant_test",
            "taxonomy": "product",
            "value": "launch-backpack",
            "confidence": 0.91,
            "source": "manual",
        },
    )["state"]
    state = runtime.dam_core_request_rendition(
        state,
        {
            "rendition_id": "rendition_test",
            "asset_id": "asset_test",
            "tenant": "tenant_test",
            "profile": "web_large",
            "target_mime_type": "image/jpeg",
            "width": 1600,
            "height": 1200,
        },
    )["state"]
    workbench = runtime.dam_core_build_workbench_view(state, tenant="tenant_test")
    rights = runtime.dam_core_enforce_rights(state, "asset_test", market="ke", use_case="web")
    assert runtime_smoke["ok"] is True
    assert workbench["asset_count"] == 1
    assert workbench["rendition_count"] == 1
    assert rights["decision"] == "allow"


def test_package_smoke_test_entrypoint_is_side_effect_free():
    entrypoint_smoke = smoke_test()
    assert entrypoint_smoke["ok"] is True
    assert not entrypoint_smoke["side_effects"]


def test_pbc_source_artifact_contract():
    expected = (
        "README.md",
        "SPECIFICATION.md",
        "implementation-plan.md",
        "implementation-status.md",
        "RELEASE_EVIDENCE.md",
        "migrations/001_initial.sql",
        "tests/test_contract.py",
        "tests/test_standalone.py",
    )
    missing = tuple(path for path in expected if not (PACKAGE_DIR / path).exists())
    evidence = release_evidence.build_release_evidence()
    assert not missing
    assert evidence["repo_gate_results"]["pbc_source_artifact_contract"] is True


def test_pbc_implementation_release_audit():
    validation = release_evidence.validate_release_evidence()
    evidence = release_evidence.build_release_evidence()
    assert validation["ok"] is True
    assert evidence["repo_gate_results"]["pbc_implementation_release_audit"] is True


def test_pbc_generation_smoke_audit():
    from .. import standalone

    smoke = standalone.smoke_test()
    evidence = release_evidence.build_release_evidence()
    assert smoke["ok"] is True
    assert evidence["repo_gate_results"]["pbc_generation_smoke_audit"] is True
