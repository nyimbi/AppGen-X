"""Executable domain behavior checks for the Product Catalog PIM PBC."""

from __future__ import annotations

import pytest

from .. import runtime
from .. import ui
from ..services import ProductCatalogPimStandaloneService
from ..services import standalone_service_operation_contracts


TENANT = "tenant_pim"
FAMILY_ID = "fam_pim_001"
PRODUCT_ID = "prod_pim_001"


def _configuration(retry_limit: int = 2) -> dict:
    return {
        "database_backend": "postgresql",
        "event_topic": runtime.PRODUCT_CATALOG_PIM_REQUIRED_EVENT_TOPIC,
        "retry_limit": retry_limit,
        "allowed_channels": ("web", "marketplace", "pos"),
        "allowed_locales": ("en-US", "fr-FR"),
        "allowed_media_roles": ("hero", "gallery", "manual"),
        "allowed_regions": ("US", "EU"),
        "default_timezone": "UTC",
        "workbench_limit": 100,
    }


def _rule() -> dict:
    return {
        "rule_id": "catalog.pim.sellability",
        "tenant": TENANT,
        "rule_type": "sellability",
        "allowed_channels": ("web", "marketplace"),
        "allowed_locales": ("en-US", "fr-FR"),
        "required_attributes": ("color", "material", "certification"),
        "required_media_roles": ("hero",),
        "restricted_regions": ("restricted",),
        "status": "active",
    }


def _service() -> ProductCatalogPimStandaloneService:
    service = ProductCatalogPimStandaloneService()
    assert service.configure_runtime(TENANT, _configuration())["ok"] is True
    for name, value in {
        "minimum_completeness": 0.8,
        "minimum_margin": 0.2,
        "max_missing_required_attributes": 0,
        "content_quality_threshold": 0.75,
        "publication_batch_size": 50,
        "retention_days": 365,
        "workbench_limit": 100,
    }.items():
        assert service.set_parameter(TENANT, name, value)["ok"] is True
    assert service.register_rule(TENANT, _rule())["ok"] is True
    return service


def _build_sellable_product(service: ProductCatalogPimStandaloneService) -> ProductCatalogPimStandaloneService:
    assert service.create_product_family(
        TENANT,
        {
            "family_id": FAMILY_ID,
            "tenant": TENANT,
            "name": "Industrial Safety Kits",
            "taxonomy": "industrial/safety/kits",
            "variant_axes": ("color", "size"),
        },
    )["ok"] is True
    assert service.register_product(
        TENANT,
        {
            "product_id": PRODUCT_ID,
            "tenant": TENANT,
            "family_id": FAMILY_ID,
            "sku": "SAFE-KIT-001",
            "name": "Industrial Safety Kit",
            "owner": "catalog_manager",
        },
    )["ok"] is True
    assert service.define_attribute_schema(
        TENANT,
        {
            "schema_id": "schema_pim_001",
            "tenant": TENANT,
            "family_id": FAMILY_ID,
            "attributes": ("color", "material", "certification"),
            "version": 1,
            "status": "active",
        },
    )["ok"] is True
    for name, value in {
        "color": "red",
        "material": "polycarbonate",
        "certification": "ANSI-Z89.1",
    }.items():
        assert service.set_product_attribute(TENANT, PRODUCT_ID, name, value)["ok"] is True
    assert service.add_localized_content(
        TENANT,
        {
            "content_id": "content_pim_001",
            "tenant": TENANT,
            "product_id": PRODUCT_ID,
            "locale": "en-US",
            "title": "Industrial Safety Kit",
            "description": "Certified safety kit with helmet, shield, gloves, and inspection-ready product documentation.",
            "seo_slug": "industrial-safety-kit",
        },
    )["ok"] is True
    assert service.attach_product_media(
        TENANT,
        {
            "media_id": "media_pim_001",
            "tenant": TENANT,
            "product_id": PRODUCT_ID,
            "role": "hero",
            "asset_ref": "dam://asset-pim-001",
            "rights_status": "approved",
            "alt_text": "Industrial safety kit hero image",
        },
    )["ok"] is True
    assert service.add_price_metadata(
        TENANT,
        {
            "price_id": "price_pim_001",
            "tenant": TENANT,
            "product_id": PRODUCT_ID,
            "currency": "USD",
            "list_price": 125.0,
            "cost": 75.0,
        },
    )["ok"] is True
    assert service.add_compliance_claim(
        TENANT,
        {
            "claim_id": "claim_pim_001",
            "tenant": TENANT,
            "product_id": PRODUCT_ID,
            "region": "US",
            "claim_type": "safety_certification",
            "status": "approved",
        },
    )["ok"] is True
    published = service.publish_product(
        TENANT,
        PRODUCT_ID,
        channels=("web", "marketplace"),
        locales=("en-US",),
        published_by="catalog_manager",
    )
    assert published["ok"] is True
    assert published["readiness_score"] == 1.0
    return service


def test_product_catalog_pim_one_pbc_catalog_publication_lifecycle_is_executable():
    service = _build_sellable_product(_service())
    try:
        workbench = service.build_workbench(TENANT)
        rendered = ui.product_catalog_pim_render_standalone_workbench(workbench)
        controls = service.run_control_tests(TENANT)
        proof = service.generate_publication_proof(TENANT, PRODUCT_ID, ("product_id", "sku", "lifecycle_state", "completeness"))

        assert workbench["ok"] is True
        assert workbench["product_count"] == 1
        assert workbench["published_product_count"] == 1
        assert workbench["average_completeness"] == 1.0
        assert rendered["ok"] is True
        assert set(rendered["forms"]) >= {"ProductMasterForm", "LocalizedContentForm", "ProductPriceForm"}
        assert set(rendered["wizards"]) >= {"ProductLaunchIntakeWizard", "CatalogPublicationWizard"}
        assert "publication_proof" in proof["proof"] or proof["proof"].startswith("zk_catalog_")
        assert controls["ok"] is True
        assert controls["hash_chain_valid"] is True
    finally:
        service.close()


def test_product_catalog_pim_service_agent_repository_and_workbench_are_first_class():
    service = _build_sellable_product(_service())
    try:
        contract = standalone_service_operation_contracts()
        agent = service.run_agent_skill(
            TENANT,
            "product_catalog_pim.document_instruction_intake",
            {
                "document": "Supplier sheet for product prod_pim_001 with media, price, compliance, and web publication request.",
                "instructions": "enrich the SKU and prepare publication proof",
                "scope": "catalog_launch",
            },
        )
        read_model = service.repository.read_model(TENANT)
        counts = service.repository.activity_counts(TENANT)

        assert contract["ok"] is True
        assert set(contract["operations"]) >= {
            "configure_runtime",
            "create_product_family",
            "set_product_attribute",
            "attach_product_media",
            "publish_product",
            "run_agent_skill",
        }
        assert agent["ok"] is True
        assert "ProductEnrichmentWizard" in agent["plan"]["wizard_candidates"]
        assert read_model["ok"] is True
        assert read_model["published_product_count"] == 1
        assert counts["forms"] >= 12
        assert counts["workflows"] >= 1
        assert counts["agent_sessions"] >= 1
    finally:
        service.close()


def test_product_catalog_pim_events_are_idempotent_retryable_and_boundary_scoped():
    service = _service()
    try:
        event = {
            "event_id": "media_evt_pim_001",
            "event_type": "MediaAssetApproved",
            "idempotency_key": "pim:media:001",
            "payload": {"tenant": TENANT, "product_id": PRODUCT_ID, "asset_ref": "dam://asset-pim-001"},
        }
        first = service.receive_event(TENANT, event)
        duplicate = service.receive_event(TENANT, event)
        failed = service.receive_event(
            TENANT,
            {
                "event_id": "unknown_evt_pim_001",
                "event_type": "UnsupportedCatalogEvent",
                "idempotency_key": "pim:bad:001",
                "payload": {"tenant": TENANT},
            },
        )
        dead = service.receive_event(
            TENANT,
            {
                "event_id": "unknown_evt_pim_001",
                "event_type": "UnsupportedCatalogEvent",
                "idempotency_key": "pim:bad:001",
                "payload": {"tenant": TENANT},
            },
        )
        state = service.repository.load_state(TENANT)
        allowed = runtime.product_catalog_pim_verify_owned_table_boundary(
            ("product", "catalog_publication", "MediaAssetApproved", "GET /inventory/product-positions/{id}")
        )
        blocked = runtime.product_catalog_pim_verify_owned_table_boundary(("foreign_product_table", "shared_inventory_table"))

        assert first["ok"] is True
        assert duplicate["duplicate"] is True
        assert failed["ok"] is False
        assert failed["handler"]["status"] == "retrying"
        assert dead["ok"] is False
        assert dead["handler"]["status"] == "dead_letter"
        assert state["dead_letter"][-1]["reason"] == "unsupported_or_failed_product_catalog_event"
        assert allowed["ok"] is True
        assert blocked["ok"] is False
        assert blocked["violations"] == ("foreign_product_table", "shared_inventory_table")
    finally:
        service.close()


def test_product_catalog_pim_advanced_catalog_intelligence_and_release_evidence_are_executable():
    service = _build_sellable_product(_service())
    try:
        state = service.repository.load_state(TENANT)
        api = runtime.product_catalog_pim_build_api_contract()
        schema = runtime.product_catalog_pim_build_schema_contract()
        service_contract = runtime.product_catalog_pim_build_service_contract()
        release = runtime.product_catalog_pim_build_release_evidence()

        assert runtime.product_catalog_pim_simulate_publication(state, PRODUCT_ID, proposed_channels=("web",))["channel_delta"] < 0
        assert runtime.product_catalog_pim_forecast_sellability((0.6, 0.72, 0.9), catalog_size=50)["ready_products"] > 0
        assert runtime.product_catalog_pim_parse_product_instruction("product prod_pim_001 channel web locale en-US action publish")["ok"] is True
        assert runtime.product_catalog_pim_score_readiness_risk({"completeness": 0.2, "compliance": 0.1, "content": 0.1, "price": 0.1})["decision"] == "monitor"
        assert runtime.product_catalog_pim_recommend_exception_resolution("missing_media")["action"] == "request_media_asset"
        assert runtime.product_catalog_pim_route_publication(
            {"event_id": "pub_route_001"},
            rails=({"route": "channel_api", "available": False, "latency": 5}, {"route": "outbox", "available": True, "latency": 1}),
        )["failover_used"] is True
        assert runtime.product_catalog_pim_generate_publication_proof(state, PRODUCT_ID, disclosure=("product_id", "sku", "lifecycle_state"))["proof"].startswith("zk_catalog_")
        assert runtime.product_catalog_pim_screen_policy(state, PRODUCT_ID, restricted_regions=("restricted",))["decision"] == "clear"
        assert runtime.product_catalog_pim_federate_product_view(state, PRODUCT_ID, systems=("commerce", "inventory", "search"))["boundary"] == "read_only_projection"
        assert runtime.product_catalog_pim_verify_product_identity({"did": "did:appgen:product:001", "issuer": "trusted_registry", "status": "active"})["ok"] is True
        assert runtime.product_catalog_pim_run_resilience_drill(state, "channel_api_timeout")["ok"] is True
        assert runtime.product_catalog_pim_rotate_crypto_epoch(state, "dilithium3_simulated")["key_id"] == "product_catalog_epoch_0002"
        assert runtime.product_catalog_pim_schedule_carbon_aware_publication(({"window": "day", "carbon": 140}, {"window": "night", "carbon": 70}))["window"] == "night"
        assert runtime.product_catalog_pim_optimize_catalog(({"plan": "all", "reach": 0.95, "cost": 0.5}, {"plan": "priority", "reach": 0.82, "cost": 0.2}))["plan"] == "priority"
        assert runtime.product_catalog_pim_allocate_channels(({"channel": "web", "priority": 0.9, "capacity": 8}, {"channel": "marketplace", "priority": 0.5, "capacity": 4}), products=10)["ok"] is True
        assert runtime.product_catalog_pim_detect_content_anomaly(state)["ok"] is True
        assert runtime.product_catalog_pim_model_stochastic_sellability_exposure(readiness_path=(0.5, 0.7, 0.9), volatility=0.12)["simulation_count"] == 1000
        assert runtime.product_catalog_pim_register_governed_model("catalog_readiness", {"features": ("media", "price"), "auc": 0.91, "drift_score": 0.04})["ok"] is True
        assert api["ok"] is True
        assert schema["ok"] is True
        assert service_contract["ok"] is True
        assert release["ok"] is True
    finally:
        service.close()


def test_product_catalog_pim_rejects_nonstandard_backends_and_user_eventing_pickers():
    state = runtime.product_catalog_pim_empty_state()

    with pytest.raises(ValueError, match="PostgreSQL, MySQL, or MariaDB"):
        runtime.product_catalog_pim_configure_runtime(
            state,
            {
                "database_backend": "sqlite",
                "event_topic": runtime.PRODUCT_CATALOG_PIM_REQUIRED_EVENT_TOPIC,
                "retry_limit": 2,
                "default_timezone": "UTC",
            },
        )

    with pytest.raises(ValueError, match="AppGen-X event contract"):
        runtime.product_catalog_pim_configure_runtime(
            state,
            {
                "database_backend": "postgresql",
                "event_topic": runtime.PRODUCT_CATALOG_PIM_REQUIRED_EVENT_TOPIC,
                "retry_limit": 2,
                "default_timezone": "UTC",
                "stream_engine": "user_selected_engine",
            },
        )
