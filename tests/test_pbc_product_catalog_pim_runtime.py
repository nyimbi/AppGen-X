import pytest

from pyAppGen.pbc import PRODUCT_CATALOG_PIM_ADVANCED_CAPABILITY_KEYS
from pyAppGen.pbc import pbc_implemented_capability_audit
from pyAppGen.pbc import pbc_implementation_contract
from pyAppGen.pbc import pbc_implementation_release_audit
from pyAppGen.pbc import product_catalog_pim_add_compliance_claim
from pyAppGen.pbc import product_catalog_pim_add_localized_content
from pyAppGen.pbc import product_catalog_pim_add_price_metadata
from pyAppGen.pbc import product_catalog_pim_attach_product_media
from pyAppGen.pbc import product_catalog_pim_build_workbench_view
from pyAppGen.pbc import product_catalog_pim_configure_runtime
from pyAppGen.pbc import product_catalog_pim_create_product_family
from pyAppGen.pbc import product_catalog_pim_define_attribute_schema
from pyAppGen.pbc import product_catalog_pim_empty_state
from pyAppGen.pbc import product_catalog_pim_publish_product
from pyAppGen.pbc import product_catalog_pim_register_product
from pyAppGen.pbc import product_catalog_pim_register_rule
from pyAppGen.pbc import product_catalog_pim_render_workbench
from pyAppGen.pbc import product_catalog_pim_runtime_capabilities
from pyAppGen.pbc import product_catalog_pim_runtime_smoke
from pyAppGen.pbc import product_catalog_pim_set_parameter
from pyAppGen.pbc import product_catalog_pim_set_product_attribute
from pyAppGen.pbc import product_catalog_pim_ui_contract


def test_product_catalog_pim_runtime_executes_standard_and_advanced_capabilities() -> None:
    runtime = product_catalog_pim_runtime_capabilities()
    smoke = product_catalog_pim_runtime_smoke()

    assert runtime["format"] == "appgen.product-catalog-pim-runtime-capabilities.v1"
    assert runtime["ok"] is True
    assert runtime["implementation_directory"] == "src/pyAppGen/pbcs/product_catalog_pim"
    assert len(runtime["standard_features"]) >= 25
    assert "rule_engine" in runtime["standard_features"]
    assert "parameter_engine" in runtime["standard_features"]
    assert "configuration_schema" in runtime["standard_features"]
    assert "workbench" in runtime["standard_features"]
    assert smoke["ok"] is True
    assert set(PRODUCT_CATALOG_PIM_ADVANCED_CAPABILITY_KEYS) == {check["id"] for check in smoke["checks"]}
    assert not smoke["blocking_gaps"]

    contract = pbc_implementation_contract("product_catalog_pim")
    assert contract["source_package"]["ok"] is True
    assert contract["advanced_runtime"]["ok"] is True
    assert contract["source_package"]["ui_contract"]["ok"] is True
    assert "ProductConfigurationPanel" in contract["source_package"]["ui_contract"]["fragments"]
    assert set(contract["advanced_runtime"]["capabilities"]) == set(PRODUCT_CATALOG_PIM_ADVANCED_CAPABILITY_KEYS)
    assert pbc_implementation_release_audit(("product_catalog_pim",))["ok"] is True
    assert pbc_implemented_capability_audit(("product_catalog_pim",))["ok"] is True


def test_product_catalog_pim_runtime_applies_rules_parameters_configuration_and_ui() -> None:
    state = product_catalog_pim_empty_state()
    state = product_catalog_pim_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": "appgen.product.events",
            "retry_limit": 3,
            "allowed_channels": ("web", "marketplace"),
            "allowed_locales": ("en-US",),
            "allowed_media_roles": ("hero", "gallery"),
            "allowed_regions": ("US",),
            "default_timezone": "UTC",
            "workbench_limit": 50,
        },
    )["state"]
    state = product_catalog_pim_set_parameter(state, "minimum_completeness", 0.8)["state"]
    state = product_catalog_pim_set_parameter(state, "minimum_margin", 0.1)["state"]
    state = product_catalog_pim_set_parameter(state, "max_missing_required_attributes", 0)["state"]
    state = product_catalog_pim_set_parameter(state, "content_quality_threshold", 0.75)["state"]
    state = product_catalog_pim_set_parameter(state, "publication_batch_size", 50)["state"]
    state = product_catalog_pim_register_rule(
        state,
        {
            "rule_id": "rule_ops",
            "tenant": "tenant_ops",
            "rule_type": "sellability",
            "allowed_channels": ("web", "marketplace"),
            "allowed_locales": ("en-US",),
            "required_attributes": ("color", "material"),
            "required_media_roles": ("hero",),
            "restricted_regions": ("restricted",),
            "status": "active",
        },
    )["state"]

    family = product_catalog_pim_create_product_family(
        state,
        {"family_id": "fam_ops", "tenant": "tenant_ops", "name": "Machine Kits", "taxonomy": "industrial/kits", "variant_axes": ("color", "size")},
    )
    state = family["state"]
    assert family["family"]["status"] == "active"

    product = product_catalog_pim_register_product(
        state,
        {"product_id": "prod_ops", "tenant": "tenant_ops", "family_id": "fam_ops", "sku": "KIT-OPS", "name": "Hydraulic Kit", "lifecycle_state": "draft", "owner": "catalog_ops"},
    )
    state = product["state"]
    assert product["product"]["sku"] == "KIT-OPS"

    schema = product_catalog_pim_define_attribute_schema(
        state,
        {"schema_id": "schema_ops", "tenant": "tenant_ops", "family_id": "fam_ops", "attributes": {"color": "string", "material": "string", "weight": "number"}},
    )
    state = schema["state"]
    assert schema["schema"]["compiled_hash"]

    state = product_catalog_pim_set_product_attribute(state, "prod_ops", "color", "blue")["state"]
    state = product_catalog_pim_set_product_attribute(state, "prod_ops", "material", "steel")["state"]
    state = product_catalog_pim_set_product_attribute(state, "prod_ops", "weight", 12.5)["state"]

    content = product_catalog_pim_add_localized_content(
        state,
        {"content_id": "content_ops", "tenant": "tenant_ops", "product_id": "prod_ops", "locale": "en-US", "title": "Hydraulic Kit", "description": "Complete hydraulic maintenance kit", "seo_slug": "hydraulic-kit"},
    )
    state = content["state"]
    assert content["content"]["status"] == "approved"

    media = product_catalog_pim_attach_product_media(
        state,
        {"media_id": "media_ops", "tenant": "tenant_ops", "product_id": "prod_ops", "role": "hero", "asset_ref": "dam://asset-ops", "rights_status": "approved", "alt_text": "Hydraulic kit hero image"},
    )
    state = media["state"]
    assert media["media"]["status"] == "approved"

    price = product_catalog_pim_add_price_metadata(
        state,
        {"price_id": "price_ops", "tenant": "tenant_ops", "product_id": "prod_ops", "currency": "USD", "list_price": 250, "cost": 180, "effective_from": "2026-05-26"},
    )
    state = price["state"]
    assert price["price"]["status"] == "ready"

    compliance = product_catalog_pim_add_compliance_claim(
        state,
        {"claim_id": "claim_ops", "tenant": "tenant_ops", "product_id": "prod_ops", "region": "US", "claim_type": "safety", "status": "approved"},
    )
    state = compliance["state"]
    assert compliance["claim"]["screening_status"] == "clear"

    publication = product_catalog_pim_publish_product(
        state,
        "prod_ops",
        channels=("web", "marketplace"),
        locales=("en-US",),
        published_by="catalog_mgr",
    )
    state = publication["state"]
    assert publication["publication"]["status"] == "published"
    assert publication["handoffs"] == (
        "commerce_catalog_projection",
        "search_index_projection",
        "forecast_signal_projection",
        "pricing_readiness_projection",
    )
    assert state["outbox"][-1]["idempotency_key"] == "product_catalog_pim:ProductPublished:product_evt_000008"

    workbench = product_catalog_pim_build_workbench_view(state, tenant="tenant_ops")
    assert workbench["product_count"] == 1
    assert workbench["family_count"] == 1
    assert workbench["published_product_count"] == 1
    assert workbench["publication_count"] == 1
    assert workbench["media_count"] == 1
    assert workbench["average_completeness"] >= 0.8
    assert workbench["configuration_bound"] is True
    assert workbench["rule_count"] == 1
    assert workbench["parameter_count"] == 5

    ui_contract = product_catalog_pim_ui_contract()
    assert ui_contract["configuration_editor"]["allowed_database_backends"] == ("postgresql", "mysql", "mariadb")
    assert "minimum_completeness" in ui_contract["parameter_editor"]["numeric_parameters"]
    assert "rule_id" in ui_contract["rule_editor"]["required_fields"]
    rendered = product_catalog_pim_render_workbench(
        state,
        tenant="tenant_ops",
        principal_permissions=(
            "product_catalog_pim.product",
            "product_catalog_pim.enrich",
            "product_catalog_pim.publish",
            "product_catalog_pim.configure",
            "product_catalog_pim.audit",
        ),
    )
    assert rendered["ok"] is True
    assert rendered["configuration_bound"] is True
    assert rendered["event_outbox_count"] == 8
    assert set(rendered["visible_actions"]) == set(ui_contract["action_permissions"])
    assert not rendered["locked_actions"]


def test_product_catalog_pim_rejects_unsupported_database_backends_and_unknown_parameters() -> None:
    state = product_catalog_pim_empty_state()

    with pytest.raises(ValueError, match="PostgreSQL, MySQL, or MariaDB"):
        product_catalog_pim_configure_runtime(
            state,
            {
                "database_backend": "stream_store",
                "event_topic": "appgen.product.events",
                "retry_limit": 3,
                "default_timezone": "UTC",
            },
        )

    with pytest.raises(ValueError, match="Unsupported Product Catalog PIM parameter"):
        product_catalog_pim_set_parameter(state, "stream_engine", "hidden_picker")
