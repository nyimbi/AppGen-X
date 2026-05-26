import pytest

from pyAppGen.pbcs.dam_core import DAM_CORE_ALLOWED_DATABASE_BACKENDS
from pyAppGen.pbcs.dam_core import DAM_CORE_OWNED_TABLES
from pyAppGen.pbcs.dam_core import DAM_CORE_RUNTIME_CAPABILITY_KEYS
from pyAppGen.pbcs.dam_core import dam_core_add_metadata_tag
from pyAppGen.pbcs.dam_core import dam_core_attach_rights_policy
from pyAppGen.pbcs.dam_core import dam_core_build_workbench_view
from pyAppGen.pbcs.dam_core import dam_core_complete_rendition
from pyAppGen.pbcs.dam_core import dam_core_configure_runtime
from pyAppGen.pbcs.dam_core import dam_core_empty_state
from pyAppGen.pbcs.dam_core import dam_core_enforce_rights
from pyAppGen.pbcs.dam_core import dam_core_receive_event
from pyAppGen.pbcs.dam_core import dam_core_register_asset
from pyAppGen.pbcs.dam_core import dam_core_register_rule
from pyAppGen.pbcs.dam_core import dam_core_render_workbench
from pyAppGen.pbcs.dam_core import dam_core_request_rendition
from pyAppGen.pbcs.dam_core import dam_core_runtime_capabilities
from pyAppGen.pbcs.dam_core import dam_core_runtime_smoke
from pyAppGen.pbcs.dam_core import dam_core_set_parameter
from pyAppGen.pbcs.dam_core import dam_core_ui_contract
from pyAppGen.pbcs.dam_core import dam_core_verify_owned_table_boundary
from pyAppGen.pbcs.dam_core import implementation_contract


def test_dam_core_runtime_executes_standard_and_advanced_capabilities() -> None:
    runtime = dam_core_runtime_capabilities()
    smoke = dam_core_runtime_smoke()
    contract = implementation_contract()

    assert runtime["format"] == "appgen.dam-core-runtime-capabilities.v1"
    assert runtime["ok"] is True
    assert runtime["implementation_directory"] == "src/pyAppGen/pbcs/dam_core"
    assert runtime["owned_tables"] == DAM_CORE_OWNED_TABLES
    assert len(runtime["standard_features"]) >= 18
    assert "configuration_schema" in runtime["standard_features"]
    assert "rule_engine" in runtime["standard_features"]
    assert "workbench" in runtime["standard_features"]
    assert smoke["ok"] is True
    assert {check["id"] for check in smoke["checks"]} == set(DAM_CORE_RUNTIME_CAPABILITY_KEYS)
    assert not smoke["blocking_gaps"]
    assert contract["side_effect_free"] is True
    assert contract["advanced_runtime"]["ok"] is True
    assert contract["ui_contract"]["ok"] is True
    assert "DamConfigurationPanel" in contract["ui_contract"]["fragments"]


def test_dam_core_runtime_applies_rules_parameters_configuration_events_and_ui() -> None:
    state = _configured_state()
    state = dam_core_receive_event(
        state,
        {
            "event_id": "product_ops",
            "event_type": "ProductPublished",
            "idempotency_key": "product:sku_ops:v1",
            "payload": {"tenant": "tenant_ops", "product_id": "sku_ops", "name": "Catalog Hero"},
        },
    )["state"]
    asset = dam_core_register_asset(
        state,
        {
            "asset_id": "asset_ops",
            "tenant": "tenant_ops",
            "product_id": "sku_ops",
            "filename": "catalog-hero.png",
            "mime_type": "image/png",
            "size_mb": 12,
            "storage_uri": "object://dam/tenant_ops/asset_ops",
            "binary": b"catalog-hero",
            "locale": "en-US",
            "created_by": "ops",
        },
    )
    state = asset["state"]
    assert asset["asset"]["fingerprint"].startswith("sha256:")
    assert asset["asset"]["product_dependency"] is True

    state = dam_core_attach_rights_policy(
        state,
        {
            "policy_id": "rights_ops",
            "asset_id": "asset_ops",
            "tenant": "tenant_ops",
            "license_type": "commercial",
            "allowed_markets": ("US",),
            "blocked_markets": ("restricted",),
            "expires_at": "2027-01-01",
            "attribution_required": False,
            "approver": "legal",
        },
    )["state"]
    state = dam_core_add_metadata_tag(
        state,
        {
            "tag_id": "tag_ops",
            "asset_id": "asset_ops",
            "tenant": "tenant_ops",
            "taxonomy": "product",
            "value": "hero",
            "confidence": 0.92,
            "source": "human",
        },
    )["state"]
    state = dam_core_request_rendition(
        state,
        {
            "rendition_id": "rend_ops",
            "asset_id": "asset_ops",
            "tenant": "tenant_ops",
            "profile": "web_large",
            "target_mime_type": "image/png",
            "width": 1400,
            "height": 900,
        },
    )["state"]
    state = dam_core_complete_rendition(
        state,
        "rend_ops",
        {"uri": "object://dam/tenant_ops/asset_ops/web_large.png", "quality_score": 0.94, "duration_ms": 640},
    )["state"]

    allowed = dam_core_enforce_rights(state, "asset_ops", market="US", use_case="product_detail")
    blocked = dam_core_enforce_rights(state, "asset_ops", market="restricted", use_case="product_detail")
    assert allowed["decision"] == "allow"
    assert blocked["decision"] == "block"
    assert state["outbox"][-1]["idempotency_key"].startswith("dam_core:AssetRenditionReady")

    workbench = dam_core_build_workbench_view(state, tenant="tenant_ops")
    assert workbench["asset_count"] == 1
    assert workbench["ready_rendition_count"] == 1
    assert workbench["rights_policy_count"] == 1
    assert workbench["metadata_tag_count"] == 1
    assert workbench["configuration_bound"] is True
    assert workbench["rule_count"] == 1
    assert workbench["parameter_count"] == 10

    ui_contract = dam_core_ui_contract()
    assert ui_contract["configuration_editor"]["allowed_database_backends"] == DAM_CORE_ALLOWED_DATABASE_BACKENDS
    assert ui_contract["configuration_editor"]["stream_engine_picker_visible"] is False
    rendered = dam_core_render_workbench(
        state,
        tenant="tenant_ops",
        principal_permissions=(
            "dam_core.asset.write",
            "dam_core.rendition.write",
            "dam_core.rights.manage",
            "dam_core.rights.evaluate",
            "dam_core.metadata.write",
            "dam_core.event.consume",
            "dam_core.configure",
            "dam_core.audit",
        ),
    )
    assert rendered["ok"] is True
    assert not rendered["locked_actions"]
    assert rendered["binding_evidence"]["owned_tables"] == DAM_CORE_OWNED_TABLES


def test_dam_core_rejects_invalid_inputs_and_proves_boundary_and_dead_letters() -> None:
    state = dam_core_empty_state()
    with pytest.raises(ValueError, match="PostgreSQL, MySQL, or MariaDB"):
        dam_core_configure_runtime(
            state,
            {
                "database_backend": "stream_store",
                "event_topic": "appgen.dam.events",
                "retry_limit": 3,
                "default_storage_tier": "warm",
                "allowed_mime_types": ("image/png",),
                "rendition_profiles": ("web_large",),
                "rights_default_decision": "review",
                "metadata_taxonomies": ("product",),
                "default_locale": "en-US",
                "workbench_limit": 50,
            },
        )

    state = _configured_state()
    with pytest.raises(ValueError, match="Unsupported DAM Core parameter"):
        dam_core_set_parameter(state, "stream_engine", 1)

    failed = dam_core_receive_event(
        state,
        {"event_id": "evt_fail", "event_type": "ProductPublished", "payload": {"tenant": "tenant_ops", "product_id": "sku_fail"}},
        simulate_failure=True,
    )
    assert failed["ok"] is False
    assert failed["handler"]["status"] == "dead_letter"
    assert len(failed["state"]["dead_letter"]) == 1

    boundary = dam_core_verify_owned_table_boundary()
    assert boundary["ok"] is True
    assert boundary["owned_tables"] == ("asset", "asset_rendition", "rights_policy", "metadata_tag")
    assert boundary["declared_dependencies"]["shared_tables"] == ()


def _configured_state() -> dict:
    state = dam_core_empty_state()
    state = dam_core_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": "appgen.dam.events",
            "retry_limit": 3,
            "default_storage_tier": "warm",
            "allowed_mime_types": ("image/png", "image/jpeg"),
            "rendition_profiles": ("web_large", "thumbnail"),
            "rights_default_decision": "review",
            "metadata_taxonomies": ("product", "campaign"),
            "default_locale": "en-US",
            "workbench_limit": 50,
        },
    )["state"]
    for name, value in (
        ("max_asset_size_mb", 1000),
        ("quality_threshold", 0.7),
        ("rights_risk_threshold", 0.6),
        ("transcode_retry_limit", 3),
        ("duplicate_similarity_threshold", 0.95),
        ("rendition_cost_weight", 0.3),
        ("carbon_cost_weight", 0.2),
        ("usage_forecast_horizon_days", 90),
        ("metadata_confidence_floor", 0.6),
        ("workbench_limit", 50),
    ):
        state = dam_core_set_parameter(state, name, value)["state"]
    return dam_core_register_rule(
        state,
        {
            "rule_id": "rule_ops",
            "tenant": "tenant_ops",
            "scope": "asset_governance",
            "status": "active",
            "mime_policy": {"allowed": ("image/png", "image/jpeg")},
            "rights_policy": {"blocked_markets": ("restricted",), "license_required": True},
            "rendition_policy": {"required_profiles": ("web_large",)},
            "metadata_policy": {"required_tags": ("product",)},
        },
    )["state"]
