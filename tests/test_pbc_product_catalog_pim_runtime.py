import pytest

from pyAppGen.pbcs.product_catalog_pim import PRODUCT_CATALOG_PIM_ALLOWED_DATABASE_BACKENDS
from pyAppGen.pbcs.product_catalog_pim import PRODUCT_CATALOG_PIM_CONSUMED_EVENT_TYPES
from pyAppGen.pbcs.product_catalog_pim import PRODUCT_CATALOG_PIM_EMITTED_EVENT_TYPES
from pyAppGen.pbcs.product_catalog_pim import PRODUCT_CATALOG_PIM_OWNED_TABLES
from pyAppGen.pbcs.product_catalog_pim import PRODUCT_CATALOG_PIM_REQUIRED_EVENT_TOPIC
from pyAppGen.pbcs.product_catalog_pim import PRODUCT_CATALOG_PIM_RUNTIME_CAPABILITY_KEYS
from pyAppGen.pbcs.product_catalog_pim import implementation_contract
from pyAppGen.pbcs.product_catalog_pim import product_catalog_pim_add_compliance_claim
from pyAppGen.pbcs.product_catalog_pim import product_catalog_pim_add_localized_content
from pyAppGen.pbcs.product_catalog_pim import product_catalog_pim_add_price_metadata
from pyAppGen.pbcs.product_catalog_pim import product_catalog_pim_attach_product_media
from pyAppGen.pbcs.product_catalog_pim import product_catalog_pim_build_api_contract
from pyAppGen.pbcs.product_catalog_pim import product_catalog_pim_build_workbench_view
from pyAppGen.pbcs.product_catalog_pim import product_catalog_pim_configure_runtime
from pyAppGen.pbcs.product_catalog_pim import product_catalog_pim_create_product_family
from pyAppGen.pbcs.product_catalog_pim import product_catalog_pim_define_attribute_schema
from pyAppGen.pbcs.product_catalog_pim import product_catalog_pim_empty_state
from pyAppGen.pbcs.product_catalog_pim import product_catalog_pim_permissions_contract
from pyAppGen.pbcs.product_catalog_pim import product_catalog_pim_publish_product
from pyAppGen.pbcs.product_catalog_pim import product_catalog_pim_receive_event
from pyAppGen.pbcs.product_catalog_pim import product_catalog_pim_register_product
from pyAppGen.pbcs.product_catalog_pim import product_catalog_pim_register_rule
from pyAppGen.pbcs.product_catalog_pim import product_catalog_pim_register_schema_extension
from pyAppGen.pbcs.product_catalog_pim import product_catalog_pim_render_workbench
from pyAppGen.pbcs.product_catalog_pim import product_catalog_pim_runtime_capabilities
from pyAppGen.pbcs.product_catalog_pim import product_catalog_pim_runtime_smoke
from pyAppGen.pbcs.product_catalog_pim import product_catalog_pim_set_parameter
from pyAppGen.pbcs.product_catalog_pim import product_catalog_pim_set_product_attribute
from pyAppGen.pbcs.product_catalog_pim import product_catalog_pim_ui_contract
from pyAppGen.pbcs.product_catalog_pim import product_catalog_pim_verify_owned_table_boundary
def test_product_catalog_pim_runtime_executes_standard_and_advanced_capabilities() -> None:
    runtime = product_catalog_pim_runtime_capabilities()
    smoke = product_catalog_pim_runtime_smoke()
    contract = implementation_contract()

    assert runtime["format"] == "appgen.product-catalog-pim-runtime-capabilities.v1"
    assert runtime["ok"] is True
    assert runtime["implementation_directory"] == "src/pyAppGen/pbcs/product_catalog_pim"
    assert runtime["owned_tables"] == PRODUCT_CATALOG_PIM_OWNED_TABLES
    assert len(runtime["standard_features"]) >= 25
    assert "rule_engine" in runtime["standard_features"]
    assert "parameter_engine" in runtime["standard_features"]
    assert "configuration_schema" in runtime["standard_features"]
    assert "appgen_x_outbox_inbox_eventing" in runtime["standard_features"]
    assert smoke["ok"] is True
    assert set(PRODUCT_CATALOG_PIM_RUNTIME_CAPABILITY_KEYS) == {check["id"] for check in smoke["checks"]}
    assert not smoke["blocking_gaps"]

    assert contract["pbc"] == "product_catalog_pim"
    assert contract["advanced_runtime"]["ok"] is True
    assert contract["owned_tables"] == PRODUCT_CATALOG_PIM_OWNED_TABLES
    assert contract["allowed_database_backends"] == PRODUCT_CATALOG_PIM_ALLOWED_DATABASE_BACKENDS
    assert contract["required_event_topic"] == PRODUCT_CATALOG_PIM_REQUIRED_EVENT_TOPIC
    assert contract["ui_contract"]["ok"] is True
    assert contract["api_contract"]["event_contract"] == "AppGen-X"
    assert contract["api_contract"]["shared_table_access"] is False
    assert contract["permissions_contract"]["action_permissions"]["receive_event"] == "product_catalog_pim.event"

    api = product_catalog_pim_build_api_contract()
    permissions = product_catalog_pim_permissions_contract()
    assert api["format"] == "appgen.product-catalog-pim-api-contract.v1"
    assert api["owned_tables"] == PRODUCT_CATALOG_PIM_OWNED_TABLES
    assert api["database_backends"] == PRODUCT_CATALOG_PIM_ALLOWED_DATABASE_BACKENDS
    assert api["emits"] == PRODUCT_CATALOG_PIM_EMITTED_EVENT_TYPES
    assert api["consumes"] == PRODUCT_CATALOG_PIM_CONSUMED_EVENT_TYPES
    assert api["shared_table_access"] is False
    assert api["stream_engine_picker_visible"] is False
    assert {route["route"] for route in api["routes"]} >= {"POST /product-catalog/events/inbox", "GET /product-catalog/workbench"}
    assert all(isinstance(route, dict) and (route.get("command") or route.get("query")) for route in api["routes"])
    assert permissions["action_permissions"]["verify_owned_table_boundary"] == "product_catalog_pim.audit"


def test_product_catalog_pim_runtime_applies_rules_parameters_configuration_ui_and_events() -> None:
    state = product_catalog_pim_empty_state()
    state = product_catalog_pim_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": PRODUCT_CATALOG_PIM_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "allowed_channels": ("web", "marketplace"),
            "allowed_locales": ("en-US",),
            "allowed_media_roles": ("hero", "gallery"),
            "allowed_regions": ("US",),
            "default_timezone": "UTC",
            "workbench_limit": 50,
        },
    )["state"]
    assert state["configuration"]["event_contract"] == "AppGen-X"
    assert state["configuration"]["event_topic"] == PRODUCT_CATALOG_PIM_REQUIRED_EVENT_TOPIC
    assert state["configuration"]["owned_tables"] == PRODUCT_CATALOG_PIM_OWNED_TABLES
    assert state["configuration"]["stream_engine_picker_visible"] is False
    assert state["configuration"]["user_eventing_choice"] is False
    state = product_catalog_pim_set_parameter(state, "minimum_completeness", 0.8)["state"]
    state = product_catalog_pim_set_parameter(state, "minimum_margin", 0.1)["state"]
    state = product_catalog_pim_set_parameter(state, "max_missing_required_attributes", 0)["state"]
    state = product_catalog_pim_set_parameter(state, "content_quality_threshold", 0.75)["state"]
    state = product_catalog_pim_set_parameter(state, "publication_batch_size", 50)["state"]
    rule = product_catalog_pim_register_rule(
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
    )
    state = rule["state"]
    assert rule["rule"]["compiled_hash"]
    assert rule["rule"]["compile_evidence"]["required_fields"] == (
        "rule_id",
        "tenant",
        "rule_type",
        "allowed_channels",
        "allowed_locales",
        "required_attributes",
        "required_media_roles",
        "restricted_regions",
        "status",
    )
    extension = product_catalog_pim_register_schema_extension(state, "product", {"sustainability_payload": "jsonb"})
    state = extension["state"]
    assert extension["fields"]["sustainability_payload"] == "jsonb"
    with pytest.raises(ValueError, match="schema extensions must target owned tables"):
        product_catalog_pim_register_schema_extension(state, "inventory_balance", {"foreign_payload": "jsonb"})

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

    received = product_catalog_pim_receive_event(
        state,
        {
            "event_id": "evt_media_ops",
            "event_type": "MediaAssetApproved",
            "idempotency_key": "media:ops:v1",
            "payload": {"tenant": "tenant_ops", "product_id": "prod_ops", "asset_ref": "dam://ops", "rights_status": "approved"},
        },
    )
    state = received["state"]
    assert received["handler"]["status"] == "processed"
    assert state["media_asset_projections"]["prod_ops"]["asset_ref"] == "dam://ops"

    duplicate = product_catalog_pim_receive_event(
        state,
        {
            "event_id": "evt_media_ops",
            "event_type": "MediaAssetApproved",
            "idempotency_key": "media:ops:v1",
            "payload": {"tenant": "tenant_ops", "product_id": "prod_ops", "asset_ref": "dam://ops", "rights_status": "approved"},
        },
    )
    assert duplicate["duplicate"] is True
    assert duplicate["handler"]["status"] == "duplicate"

    failed = product_catalog_pim_receive_event(
        state,
        {
            "event_id": "evt_bad_ops",
            "event_type": "UnsupportedCatalogEvent",
            "idempotency_key": "bad:ops:v1",
            "payload": {"tenant": "tenant_ops"},
        },
        simulate_failure=True,
    )
    failed = product_catalog_pim_receive_event(
        failed["state"],
        {
            "event_id": "evt_bad_ops",
            "event_type": "UnsupportedCatalogEvent",
            "idempotency_key": "bad:ops:v1",
            "payload": {"tenant": "tenant_ops"},
        },
        simulate_failure=True,
    )
    failed = product_catalog_pim_receive_event(
        failed["state"],
        {
            "event_id": "evt_bad_ops",
            "event_type": "UnsupportedCatalogEvent",
            "idempotency_key": "bad:ops:v1",
            "payload": {"tenant": "tenant_ops"},
        },
        simulate_failure=True,
    )
    state = failed["state"]
    assert failed["handler"]["status"] == "dead_letter"
    assert len(state["retry_evidence"]) == 3
    assert state["dead_letters"][-1]["reason"] == "unsupported_or_failed_product_catalog_event"

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
    assert workbench["inbox_count"] == 4
    assert workbench["dead_letter_count"] == 1
    assert workbench["binding_evidence"]["runtime_tables"]["inbox"] == "product_catalog_pim_appgen_inbox_event"
    assert workbench["binding_evidence"]["shared_table_access"] is False

    ui_contract = product_catalog_pim_ui_contract()
    assert ui_contract["configuration_editor"]["allowed_database_backends"] == ("postgresql", "mysql", "mariadb")
    assert ui_contract["configuration_editor"]["event_topic"] == PRODUCT_CATALOG_PIM_REQUIRED_EVENT_TOPIC
    assert ui_contract["configuration_editor"]["stream_engine_picker_visible"] is False
    assert "minimum_completeness" in ui_contract["parameter_editor"]["numeric_parameters"]
    assert "receive_event" in ui_contract["action_permissions"]
    rendered = product_catalog_pim_render_workbench(
        state,
        tenant="tenant_ops",
        principal_permissions=(
            "product_catalog_pim.product",
            "product_catalog_pim.enrich",
            "product_catalog_pim.publish",
            "product_catalog_pim.configure",
            "product_catalog_pim.event",
            "product_catalog_pim.audit",
        ),
    )
    assert rendered["ok"] is True
    assert rendered["configuration_bound"] is True
    assert rendered["event_outbox_count"] == 8
    assert rendered["event_inbox_count"] == 4
    assert rendered["dead_letter_count"] == 1
    assert set(rendered["visible_actions"]) == set(ui_contract["action_permissions"])
    assert not rendered["locked_actions"]
    assert rendered["binding_evidence"]["ui_bindings"]["inbox_table"] == "product_catalog_pim_appgen_inbox_event"
    assert rendered["binding_evidence"]["ui_bindings"]["rbac"]["receive_event"] == "product_catalog_pim.event"


def test_product_catalog_pim_rejects_invalid_configuration_unknown_parameters_and_foreign_boundary_refs() -> None:
    state = product_catalog_pim_empty_state()

    with pytest.raises(ValueError, match="PostgreSQL, MySQL, or MariaDB"):
        product_catalog_pim_configure_runtime(
            state,
            {
                "database_backend": "sqlite",
                "event_topic": PRODUCT_CATALOG_PIM_REQUIRED_EVENT_TOPIC,
                "retry_limit": 3,
                "default_timezone": "UTC",
            },
        )

    with pytest.raises(ValueError, match="does not allow stream-engine or user-selectable eventing fields"):
        product_catalog_pim_configure_runtime(
            state,
            {
                "database_backend": "postgresql",
                "event_topic": PRODUCT_CATALOG_PIM_REQUIRED_EVENT_TOPIC,
                "retry_limit": 3,
                "default_timezone": "UTC",
                "stream_engine": "kafka",
            },
        )

    with pytest.raises(ValueError, match="event topic is fixed"):
        product_catalog_pim_configure_runtime(
            state,
            {
                "database_backend": "postgresql",
                "event_topic": "appgen.custom.product.events",
                "retry_limit": 3,
                "default_timezone": "UTC",
            },
        )

    with pytest.raises(ValueError, match="Unsupported Product Catalog PIM parameter"):
        product_catalog_pim_set_parameter(state, "unexpected_parameter", 1)

    boundary = product_catalog_pim_verify_owned_table_boundary(
        (
            "product",
            "catalog_publication",
            "MediaAssetApproved",
            "product_catalog_pim_appgen_outbox_event",
            "pricing_readiness_projection",
        )
    )
    assert boundary["ok"] is True
    assert boundary["declared_dependencies"]["shared_tables"] == ()

    violation = product_catalog_pim_verify_owned_table_boundary(("inventory_balance", "customer_profile"))
    assert violation["ok"] is False
    assert violation["violations"] == ("inventory_balance", "customer_profile")
