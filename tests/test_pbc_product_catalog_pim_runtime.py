import pytest

from pyAppGen.pbcs.product_catalog_pim import PRODUCT_CATALOG_PIM_ALLOWED_DATABASE_BACKENDS
from pyAppGen.pbcs.product_catalog_pim import PRODUCT_CATALOG_PIM_CONSUMED_EVENT_TYPES
from pyAppGen.pbcs.product_catalog_pim import PRODUCT_CATALOG_PIM_EMITTED_EVENT_TYPES
from pyAppGen.pbcs.product_catalog_pim import PRODUCT_CATALOG_PIM_OWNED_TABLES
from pyAppGen.pbcs.product_catalog_pim import PRODUCT_CATALOG_PIM_REQUIRED_EVENT_TOPIC
from pyAppGen.pbcs.product_catalog_pim import PRODUCT_CATALOG_PIM_RUNTIME_CAPABILITY_KEYS
from pyAppGen.pbcs.product_catalog_pim import PRODUCT_CATALOG_PIM_RUNTIME_TABLES
from pyAppGen.pbcs.product_catalog_pim import implementation_contract
from pyAppGen.pbcs.product_catalog_pim import product_catalog_pim_add_compliance_claim
from pyAppGen.pbcs.product_catalog_pim import product_catalog_pim_add_localized_content
from pyAppGen.pbcs.product_catalog_pim import product_catalog_pim_add_price_metadata
from pyAppGen.pbcs.product_catalog_pim import product_catalog_pim_attach_product_media
from pyAppGen.pbcs.product_catalog_pim import product_catalog_pim_build_api_contract
from pyAppGen.pbcs.product_catalog_pim import product_catalog_pim_build_release_evidence
from pyAppGen.pbcs.product_catalog_pim import product_catalog_pim_build_schema_contract
from pyAppGen.pbcs.product_catalog_pim import product_catalog_pim_build_service_contract
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


def _configured_state() -> dict:
    state = product_catalog_pim_empty_state()
    state = product_catalog_pim_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": PRODUCT_CATALOG_PIM_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "allowed_channels": ("web", "marketplace"),
            "allowed_locales": ("en-US", "fr-FR"),
            "allowed_media_roles": ("hero", "gallery"),
            "allowed_regions": ("US",),
            "default_timezone": "UTC",
            "workbench_limit": 50,
        },
    )["state"]
    for name, value in (
        ("minimum_completeness", 0.8),
        ("minimum_margin", 0.1),
        ("max_missing_required_attributes", 0),
        ("content_quality_threshold", 0.75),
        ("publication_batch_size", 50),
    ):
        state = product_catalog_pim_set_parameter(state, name, value)["state"]
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
    return state


def test_product_catalog_pim_runtime_exposes_package_local_contract_builders() -> None:
    runtime = product_catalog_pim_runtime_capabilities()
    smoke = product_catalog_pim_runtime_smoke()
    contract = implementation_contract()
    api = product_catalog_pim_build_api_contract()
    permissions = product_catalog_pim_permissions_contract()

    assert runtime["format"] == "appgen.product-catalog-pim-runtime-capabilities.v1"
    assert runtime["ok"] is True
    assert runtime["implementation_directory"] == "src/pyAppGen/pbcs/product_catalog_pim"
    assert runtime["owned_tables"] == PRODUCT_CATALOG_PIM_OWNED_TABLES
    assert runtime["runtime_tables"] == PRODUCT_CATALOG_PIM_RUNTIME_TABLES
    assert runtime["required_event_topic"] == PRODUCT_CATALOG_PIM_REQUIRED_EVENT_TOPIC
    assert runtime["allowed_database_backends"] == PRODUCT_CATALOG_PIM_ALLOWED_DATABASE_BACKENDS
    assert len(runtime["owned_tables"]) >= 45
    assert len(runtime["standard_features"]) >= 35
    assert {
        "taxonomy_hierarchy",
        "category_management",
        "assortment_management",
        "catalog_syndication",
        "product_lifecycle",
        "approval_workflow",
        "data_quality_scores",
        "appgen_x_outbox_inbox_eventing",
    } <= set(runtime["standard_features"])
    assert {"build_schema_contract", "build_service_contract", "build_release_evidence"} <= set(runtime["operations"])
    assert smoke["ok"] is True
    assert {check["id"] for check in smoke["checks"]} == set(PRODUCT_CATALOG_PIM_RUNTIME_CAPABILITY_KEYS)
    assert not smoke["blocking_gaps"]

    assert contract["pbc"] == "product_catalog_pim"
    assert contract["advanced_runtime"]["ok"] is True
    assert contract["owned_tables"] == PRODUCT_CATALOG_PIM_OWNED_TABLES
    assert contract["runtime_tables"] == PRODUCT_CATALOG_PIM_RUNTIME_TABLES
    assert contract["allowed_database_backends"] == PRODUCT_CATALOG_PIM_ALLOWED_DATABASE_BACKENDS
    assert contract["required_event_topic"] == PRODUCT_CATALOG_PIM_REQUIRED_EVENT_TOPIC
    assert contract["consumes"] == PRODUCT_CATALOG_PIM_CONSUMED_EVENT_TYPES
    assert contract["emits"] == PRODUCT_CATALOG_PIM_EMITTED_EVENT_TYPES
    assert contract["ui_contract"]["ok"] is True
    assert contract["api_contract"]["event_contract"] == "AppGen-X"
    assert contract["schema_contract"]["ok"] is True
    assert contract["service_contract"]["ok"] is True
    assert contract["release_evidence_contract"]["ok"] is True
    assert contract["permissions_contract"]["action_permissions"]["build_release_evidence"] == "product_catalog_pim.audit"

    assert api["format"] == "appgen.product-catalog-pim-api-contract.v1"
    assert api["owned_tables"] == PRODUCT_CATALOG_PIM_OWNED_TABLES
    assert api["runtime_tables"] == PRODUCT_CATALOG_PIM_RUNTIME_TABLES
    assert api["database_backends"] == PRODUCT_CATALOG_PIM_ALLOWED_DATABASE_BACKENDS
    assert api["required_event_topic"] == PRODUCT_CATALOG_PIM_REQUIRED_EVENT_TOPIC
    assert api["emits"] == PRODUCT_CATALOG_PIM_EMITTED_EVENT_TYPES
    assert api["consumes"] == PRODUCT_CATALOG_PIM_CONSUMED_EVENT_TYPES
    assert api["event_descriptors"]["emitted"][0]["contract"] == "AppGen-X"
    assert api["event_descriptors"]["consumed"][0]["dead_letter_table"] == PRODUCT_CATALOG_PIM_RUNTIME_TABLES[2]
    assert api["dependencies"]["shared_tables"] == ()
    assert api["shared_table_access"] is False
    assert api["stream_engine_picker_visible"] is False
    assert {
        "PUT /product-catalog/configuration",
        "POST /product-catalog/rules",
        "POST /product-catalog/parameters",
        "POST /product-catalog/schema-extensions",
        "POST /product-catalog/events/inbox",
        "GET /product-catalog/workbench",
        "GET /product-catalog/schema-contract",
        "GET /product-catalog/service-contract",
        "GET /product-catalog/release-evidence",
    } <= {route["route"] for route in api["routes"]}
    assert all(isinstance(route, dict) and (route.get("command") or route.get("query")) for route in api["routes"])

    assert permissions["action_permissions"]["build_schema_contract"] == "product_catalog_pim.audit"
    assert permissions["action_permissions"]["build_service_contract"] == "product_catalog_pim.audit"
    assert permissions["action_permissions"]["build_release_evidence"] == "product_catalog_pim.audit"


def test_product_catalog_pim_schema_service_release_and_ui_binding_contracts() -> None:
    schema = product_catalog_pim_build_schema_contract()
    service = product_catalog_pim_build_service_contract()
    release = product_catalog_pim_build_release_evidence()
    ui_contract = product_catalog_pim_ui_contract()

    assert schema["format"] == "appgen.product-catalog-pim-owned-schema-contract.v1"
    assert schema["ok"] is True
    assert len(schema["tables"]) == len(PRODUCT_CATALOG_PIM_OWNED_TABLES)
    assert len(schema["migrations"]) == len(PRODUCT_CATALOG_PIM_OWNED_TABLES)
    assert tuple(item["table"] for item in schema["runtime_tables"]) == PRODUCT_CATALOG_PIM_RUNTIME_TABLES
    assert {
        "product_variant_option",
        "product_taxonomy",
        "product_assortment_assignment",
        "catalog_syndication_delivery",
        "product_data_quality_score",
        "product_governed_model",
    } <= {item["table"] for item in schema["tables"]}
    assert schema["datastore_backends"] == PRODUCT_CATALOG_PIM_ALLOWED_DATABASE_BACKENDS
    assert schema["required_event_topic"] == PRODUCT_CATALOG_PIM_REQUIRED_EVENT_TOPIC
    assert schema["shared_table_access"] is False
    assert not schema["invalid_prefixes"]

    assert service["format"] == "appgen.product-catalog-pim-service-contract.v1"
    assert service["ok"] is True
    assert service["transaction_boundary"] == "product_catalog_pim_owned_datastore_plus_appgen_outbox"
    assert "receive_event" in service["idempotent_handlers"]
    assert "build_release_evidence" in service["query_methods"]
    assert service["retry_dead_letter_evidence"]["dead_letter_table"] == PRODUCT_CATALOG_PIM_RUNTIME_TABLES[2]
    assert service["eventing"]["contract"] == "AppGen-X"
    assert service["eventing"]["topic"] == PRODUCT_CATALOG_PIM_REQUIRED_EVENT_TOPIC
    assert service["external_dependencies"]["shared_tables"] == ()

    assert ui_contract["format"] == "appgen.product-catalog-pim-ui-contract.v1"
    assert ui_contract["ok"] is True
    assert "TaxonomyAssignmentStudio" in ui_contract["fragments"]
    assert "ChannelSyndicationConsole" in ui_contract["fragments"]
    assert "DataQualityBoard" in ui_contract["fragments"]
    assert ui_contract["binding_evidence"]["runtime_tables"] == PRODUCT_CATALOG_PIM_RUNTIME_TABLES
    assert ui_contract["binding_evidence"]["required_event_topic"] == PRODUCT_CATALOG_PIM_REQUIRED_EVENT_TOPIC
    assert ui_contract["binding_evidence"]["shared_table_access"] is False

    assert release["format"] == "appgen.product-catalog-pim-release-evidence.v1"
    assert release["ok"] is True
    assert not release["blocking_gaps"]
    assert release["schema"]["format"] == schema["format"]
    assert release["service"]["format"] == service["format"]
    assert release["api"]["required_event_topic"] == PRODUCT_CATALOG_PIM_REQUIRED_EVENT_TOPIC
    assert release["ui_binding"]["binding_evidence"]["outbox_table"] == PRODUCT_CATALOG_PIM_RUNTIME_TABLES[0]
    assert release["workbench"]["binding_evidence"]["inbox_table"] == PRODUCT_CATALOG_PIM_RUNTIME_TABLES[1]
    assert {check["id"] for check in release["checks"]} >= {
        "owned_schema_depth",
        "service_contract_depth",
        "event_idempotency_evidence",
        "runtime_smoke",
    }


def test_product_catalog_pim_runtime_applies_rules_parameters_publication_events_and_workbench_bindings() -> None:
    state = _configured_state()

    extension = product_catalog_pim_register_schema_extension(
        state,
        "product",
        {"sustainability_payload": "jsonb", "semantic_keywords": "jsonb"},
    )
    state = extension["state"]
    assert extension["ok"] is True
    assert state["schema_extensions"]["product"]["semantic_keywords"] == "jsonb"

    family = product_catalog_pim_create_product_family(
        state,
        {
            "family_id": "fam_ops",
            "tenant": "tenant_ops",
            "name": "Machine Kits",
            "taxonomy": "industrial/kits",
            "variant_axes": ("color", "size"),
        },
    )
    state = family["state"]
    assert family["family"]["status"] == "active"

    product = product_catalog_pim_register_product(
        state,
        {
            "product_id": "prod_ops",
            "tenant": "tenant_ops",
            "family_id": "fam_ops",
            "sku": "KIT-OPS",
            "name": "Hydraulic Kit",
            "lifecycle_state": "draft",
            "owner": "catalog_ops",
        },
    )
    state = product["state"]
    assert product["product"]["graph_degree"] >= 4

    schema = product_catalog_pim_define_attribute_schema(
        state,
        {
            "schema_id": "schema_ops",
            "tenant": "tenant_ops",
            "family_id": "fam_ops",
            "attributes": {"color": "string", "material": "string", "weight": "number"},
        },
    )
    state = schema["state"]
    assert schema["schema"]["compiled_hash"]

    for name, value in (("color", "blue"), ("material", "steel"), ("weight", 12.5)):
        state = product_catalog_pim_set_product_attribute(state, "prod_ops", name, value)["state"]

    content = product_catalog_pim_add_localized_content(
        state,
        {
            "content_id": "content_ops",
            "tenant": "tenant_ops",
            "product_id": "prod_ops",
            "locale": "en-US",
            "title": "Hydraulic Kit",
            "description": "Complete hydraulic maintenance kit",
            "seo_slug": "hydraulic-kit",
        },
    )
    state = content["state"]
    assert content["content"]["status"] == "approved"

    media = product_catalog_pim_attach_product_media(
        state,
        {
            "media_id": "media_ops",
            "tenant": "tenant_ops",
            "product_id": "prod_ops",
            "role": "hero",
            "asset_ref": "dam://asset-ops",
            "rights_status": "approved",
            "alt_text": "Hydraulic kit hero image",
        },
    )
    state = media["state"]
    assert media["media"]["status"] == "approved"

    price = product_catalog_pim_add_price_metadata(
        state,
        {
            "price_id": "price_ops",
            "tenant": "tenant_ops",
            "product_id": "prod_ops",
            "currency": "USD",
            "list_price": 250,
            "cost": 180,
            "effective_from": "2026-05-26",
        },
    )
    state = price["state"]
    assert price["price"]["status"] == "ready"

    compliance = product_catalog_pim_add_compliance_claim(
        state,
        {
            "claim_id": "claim_ops",
            "tenant": "tenant_ops",
            "product_id": "prod_ops",
            "region": "US",
            "claim_type": "safety",
            "status": "approved",
        },
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

    for _ in range(3):
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
    assert workbench["outbox_count"] == 8
    assert workbench["inbox_count"] == 4
    assert workbench["dead_letter_count"] == 1
    assert workbench["binding_evidence"]["outbox_table"] == PRODUCT_CATALOG_PIM_RUNTIME_TABLES[0]
    assert workbench["binding_evidence"]["inbox_table"] == PRODUCT_CATALOG_PIM_RUNTIME_TABLES[1]
    assert workbench["binding_evidence"]["dead_letter_table"] == PRODUCT_CATALOG_PIM_RUNTIME_TABLES[2]
    assert workbench["binding_evidence"]["api_descriptors"]["release_evidence_route"] == "GET /product-catalog/release-evidence"
    assert workbench["binding_evidence"]["shared_table_access"] is False

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
    assert "build_release_evidence" in rendered["visible_actions"]
    assert "ProductConfigurationPanel" in rendered["fragments"]
    assert rendered["binding_evidence"]["ui_bindings"]["publication_fragment"] == "PublicationConsole"
    assert rendered["binding_evidence"]["ui_bindings"]["quality_fragment"] == "DataQualityBoard"
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
                "stream_engine": "forbidden_engine",
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

    state = _configured_state()
    with pytest.raises(ValueError, match="schema extensions must target owned tables"):
        product_catalog_pim_register_schema_extension(state, "inventory_balance", {"foreign_payload": "jsonb"})

    boundary = product_catalog_pim_verify_owned_table_boundary(
        (
            "product",
            "catalog_publication",
            "MediaAssetApproved",
            "ProductPublished",
            PRODUCT_CATALOG_PIM_RUNTIME_TABLES[0],
            "pricing_readiness_projection",
        )
    )
    assert boundary["ok"] is True
    assert boundary["declared_dependencies"]["shared_tables"] == ()

    violation = product_catalog_pim_verify_owned_table_boundary(("inventory_balance", "customer_profile"))
    assert violation["ok"] is False
    assert violation["violations"] == ("inventory_balance", "customer_profile")
