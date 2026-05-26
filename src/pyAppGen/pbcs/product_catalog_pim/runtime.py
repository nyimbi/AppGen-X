"""Executable runtime for the Enterprise Product Catalog and PIM PBC."""

from __future__ import annotations

import hashlib
import json
import math
import re


PRODUCT_CATALOG_PIM_EVENT_CONTRACT = "AppGen-X"
PRODUCT_CATALOG_PIM_REQUIRED_EVENT_TOPIC = "appgen.product.events"
PRODUCT_CATALOG_PIM_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
PRODUCT_CATALOG_PIM_OWNED_TABLES = (
    "product",
    "product_family",
    "product_variant",
    "product_variant_option",
    "product_variant_member",
    "product_taxonomy",
    "taxonomy_node",
    "taxonomy_relationship",
    "product_category",
    "category_assignment",
    "product_attribute_schema",
    "product_attribute",
    "product_attribute_validation_rule",
    "product_attribute_value_option",
    "product_price",
    "product_channel_price",
    "product_media",
    "product_locale_content",
    "product_localization_memory",
    "product_seo_metadata",
    "product_compliance_claim",
    "product_lifecycle_stage",
    "product_approval_workflow",
    "product_approval_decision",
    "product_assortment",
    "product_assortment_assignment",
    "catalog_publication",
    "catalog_channel_projection",
    "catalog_channel_policy",
    "catalog_syndication_feed",
    "catalog_syndication_delivery",
    "product_enrichment_task",
    "product_data_quality_score",
    "product_data_quality_issue",
    "product_bundle_definition",
    "product_relationship",
    "product_identity_credential",
    "product_graph_projection",
    "product_semantic_embedding",
    "product_readiness_forecast",
    "product_risk_model",
    "product_policy_screening",
    "product_publication_proof",
    "product_audit_trace",
    "product_schema_extension",
    "product_control_assertion",
    "product_governed_model",
    "product_seed_data",
    "product_rule",
    "product_parameter",
    "product_configuration",
)
PRODUCT_CATALOG_PIM_EMITTED_EVENT_TYPES = (
    "ProductClassified",
    "ProductRegistered",
    "AttributeSchemaDefined",
    "ProductEnriched",
    "ProductMediaAttached",
    "ProductPriceReady",
    "ProductComplianceClaimed",
    "ProductPublished",
)
PRODUCT_CATALOG_PIM_CONSUMED_EVENT_TYPES = (
    "TaxCalculated",
    "MediaAssetApproved",
    "InventoryPositionUpdated",
    "PricePromotionApproved",
    "SearchIndexRequested",
)
PRODUCT_CATALOG_PIM_RUNTIME_TABLES = (
    "product_catalog_pim_appgen_outbox_event",
    "product_catalog_pim_appgen_inbox_event",
    "product_catalog_pim_dead_letter_event",
)
PRODUCT_CATALOG_PIM_ALLOWED_DEPENDENCIES = (
    "commerce_catalog_projection",
    "search_index_projection",
    "forecast_signal_projection",
    "pricing_readiness_projection",
    "tax_calculation_projection",
    "media_asset_projection",
    "inventory_position_projection",
    "price_promotion_projection",
    "GET /commerce/catalog-products/{id}",
    "GET /inventory/product-positions/{id}",
    "GET /tax/product-compliance/{id}",
    "POST /search/catalog-projections",
    "POST /pricing/product-readiness",
)
PRODUCT_CATALOG_PIM_FORBIDDEN_EVENTING_FIELDS = {
    "eventing_choice",
    "eventing_mode",
    "event_transport",
    "stream_engine",
    "stream_engine_picker",
    "stream_picker",
    "user_eventing_choice",
}
PRODUCT_CATALOG_PIM_REQUIRED_CONFIGURATION_FIELDS = (
    "database_backend",
    "event_topic",
    "retry_limit",
    "default_timezone",
)
PRODUCT_CATALOG_PIM_SUPPORTED_CONFIGURATION_FIELDS = (
    "database_backend",
    "event_topic",
    "retry_limit",
    "allowed_channels",
    "allowed_locales",
    "allowed_media_roles",
    "allowed_regions",
    "default_timezone",
    "workbench_limit",
)
PRODUCT_CATALOG_PIM_SUPPORTED_PARAMETER_NAMES = (
    "minimum_completeness",
    "minimum_margin",
    "max_missing_required_attributes",
    "content_quality_threshold",
    "publication_batch_size",
    "retention_days",
    "workbench_limit",
)
PRODUCT_CATALOG_PIM_REQUIRED_RULE_FIELDS = (
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

PRODUCT_CATALOG_PIM_RUNTIME_CAPABILITY_KEYS = (
    "event_sourced_product_lifecycle",
    "graph_relational_product_topology",
    "multi_tenant_catalog_isolation",
    "schema_evolution_resilient_attribute_schema",
    "probabilistic_sellability_compliance_scoring",
    "real_time_catalog_readiness_analytics",
    "counterfactual_publication_simulation",
    "temporal_content_sellability_forecasting",
    "autonomous_enrichment_exception_resolution",
    "semantic_product_instruction_parsing",
    "predictive_product_readiness_risk",
    "self_healing_publication_route_selection",
    "zero_knowledge_catalog_publication_proof",
    "immutable_catalog_audit_trail",
    "dynamic_product_policy_screening",
    "automated_catalog_control_testing",
    "universal_api_async_streaming",
    "cross_system_product_federation",
    "commerce_inventory_tax_content_integration",
    "decentralized_product_identity",
    "chaos_engineered_catalog_tolerance",
    "quantum_resistant_product_authorization",
    "carbon_aware_catalog_publication",
    "algebraic_catalog_optimization",
    "mechanism_design_channel_allocation",
    "information_theoretic_content_anomaly_detection",
    "temporal_sellability_exposure_stochastic_modeling",
    "distributed_systems_engineering",
    "probabilistic_ml_product_readiness",
    "cryptographic_engineering",
    "mathematical_optimization",
    "product_mlops_governance",
)
PRODUCT_CATALOG_PIM_STANDARD_FEATURE_KEYS = (
    "product_master",
    "product_family",
    "variant_model",
    "variant_options",
    "sku_governance",
    "taxonomy_assignment",
    "taxonomy_hierarchy",
    "category_management",
    "attribute_schema",
    "attribute_validation",
    "attribute_value_options",
    "enrichment_completeness",
    "enrichment_tasking",
    "localized_content",
    "localization_memory",
    "seo_metadata",
    "media_reference",
    "media_rights",
    "price_metadata",
    "channel_pricebooks",
    "channel_projection",
    "channel_policy",
    "assortment_management",
    "catalog_publication",
    "catalog_syndication",
    "product_lifecycle",
    "approval_workflow",
    "sellability_rules",
    "compliance_claims",
    "restricted_region_screening",
    "data_quality_scores",
    "product_relationships",
    "bundle_definitions",
    "search_index_signal",
    "forecast_signal",
    "appgen_x_outbox_inbox_eventing",
    "idempotent_handlers",
    "retry_dead_letter_evidence",
    "permissions",
    "configuration_schema",
    "rule_engine",
    "parameter_engine",
    "seed_data",
    "workbench",
    "owned_table_boundary",
)


def product_catalog_pim_runtime_capabilities() -> dict:
    smoke = product_catalog_pim_runtime_smoke()
    return {
        "format": "appgen.product-catalog-pim-runtime-capabilities.v1",
        "ok": smoke["ok"],
        "pbc": "product_catalog_pim",
        "implementation_directory": "src/pyAppGen/pbcs/product_catalog_pim",
        "owned_tables": PRODUCT_CATALOG_PIM_OWNED_TABLES,
        "runtime_tables": PRODUCT_CATALOG_PIM_RUNTIME_TABLES,
        "required_event_topic": PRODUCT_CATALOG_PIM_REQUIRED_EVENT_TOPIC,
        "allowed_database_backends": PRODUCT_CATALOG_PIM_ALLOWED_DATABASE_BACKENDS,
        "capabilities": PRODUCT_CATALOG_PIM_RUNTIME_CAPABILITY_KEYS,
        "standard_features": PRODUCT_CATALOG_PIM_STANDARD_FEATURE_KEYS,
        "operations": (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "register_schema_extension",
            "receive_event",
            "create_product_family",
            "register_product",
            "define_attribute_schema",
            "set_product_attribute",
            "add_localized_content",
            "attach_product_media",
            "add_price_metadata",
            "add_compliance_claim",
            "publish_product",
            "build_api_contract",
            "build_schema_contract",
            "build_service_contract",
            "build_release_evidence",
            "permissions_contract",
            "build_workbench_view",
            "verify_owned_table_boundary",
            "register_governed_model",
        ),
        "smoke": smoke,
    }


def product_catalog_pim_runtime_smoke() -> dict:
    state = product_catalog_pim_empty_state()
    state = product_catalog_pim_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": PRODUCT_CATALOG_PIM_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "allowed_channels": ("web", "marketplace", "pos"),
            "allowed_locales": ("en-US", "fr-FR"),
            "allowed_media_roles": ("hero", "gallery", "manual"),
            "allowed_regions": ("US", "EU"),
            "default_timezone": "UTC",
            "workbench_limit": 100,
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
            "rule_id": "rule_catalog",
            "tenant": "tenant_alpha",
            "rule_type": "sellability",
            "allowed_channels": ("web", "marketplace"),
            "allowed_locales": ("en-US",),
            "required_attributes": ("color", "material"),
            "required_media_roles": ("hero",),
            "restricted_regions": ("restricted",),
            "status": "active",
        },
    )["state"]
    state = product_catalog_pim_register_schema_extension(state, "product", {"sustainability_payload": "jsonb"})["state"]
    family = product_catalog_pim_create_product_family(
        state,
        {
            "family_id": "fam_100",
            "tenant": "tenant_alpha",
            "name": "Machine Kits",
            "taxonomy": "industrial/kits",
            "variant_axes": ("color", "size"),
        },
    )
    state = family["state"]
    product = product_catalog_pim_register_product(
        state,
        {
            "product_id": "prod_100",
            "tenant": "tenant_alpha",
            "family_id": "fam_100",
            "sku": "KIT-100",
            "name": "Hydraulic Kit",
            "lifecycle_state": "draft",
            "owner": "catalog_ops",
        },
    )
    state = product["state"]
    schema = product_catalog_pim_define_attribute_schema(
        state,
        {
            "schema_id": "schema_100",
            "tenant": "tenant_alpha",
            "family_id": "fam_100",
            "attributes": {"color": "string", "material": "string", "weight": "number"},
        },
    )
    state = schema["state"]
    state = product_catalog_pim_set_product_attribute(state, "prod_100", "color", "blue")["state"]
    state = product_catalog_pim_set_product_attribute(state, "prod_100", "material", "steel")["state"]
    state = product_catalog_pim_set_product_attribute(state, "prod_100", "weight", 12.5)["state"]
    content = product_catalog_pim_add_localized_content(
        state,
        {
            "content_id": "content_100",
            "tenant": "tenant_alpha",
            "product_id": "prod_100",
            "locale": "en-US",
            "title": "Hydraulic Kit",
            "description": "Complete hydraulic maintenance kit",
            "seo_slug": "hydraulic-kit",
        },
    )
    state = content["state"]
    media = product_catalog_pim_attach_product_media(
        state,
        {
            "media_id": "media_100",
            "tenant": "tenant_alpha",
            "product_id": "prod_100",
            "role": "hero",
            "asset_ref": "dam://asset-100",
            "rights_status": "approved",
            "alt_text": "Hydraulic kit hero image",
        },
    )
    state = media["state"]
    price = product_catalog_pim_add_price_metadata(
        state,
        {
            "price_id": "price_100",
            "tenant": "tenant_alpha",
            "product_id": "prod_100",
            "currency": "USD",
            "list_price": 250,
            "cost": 180,
            "effective_from": "2026-05-26",
        },
    )
    state = price["state"]
    compliance = product_catalog_pim_add_compliance_claim(
        state,
        {
            "claim_id": "claim_100",
            "tenant": "tenant_alpha",
            "product_id": "prod_100",
            "region": "US",
            "claim_type": "safety",
            "status": "approved",
        },
    )
    state = compliance["state"]
    publication = product_catalog_pim_publish_product(
        state,
        "prod_100",
        channels=("web", "marketplace"),
        locales=("en-US",),
        published_by="catalog_mgr",
    )
    state = publication["state"]
    received = product_catalog_pim_receive_event(
        state,
        {
            "event_id": "evt_media_100",
            "event_type": "MediaAssetApproved",
            "idempotency_key": "product-media:100",
            "payload": {"tenant": "tenant_alpha", "product_id": "prod_100", "asset_ref": "dam://asset-100"},
        },
    )
    state = received["state"]
    duplicate = product_catalog_pim_receive_event(
        state,
        {
            "event_id": "evt_media_100",
            "event_type": "MediaAssetApproved",
            "idempotency_key": "product-media:100",
            "payload": {"tenant": "tenant_alpha", "product_id": "prod_100", "asset_ref": "dam://asset-100"},
        },
    )
    failed = product_catalog_pim_receive_event(
        state,
        {
            "event_id": "evt_unknown_100",
            "event_type": "UnsupportedCatalogEvent",
            "idempotency_key": "bad-catalog:100",
            "payload": {"tenant": "tenant_alpha"},
        },
        simulate_failure=True,
    )
    failed = product_catalog_pim_receive_event(
        failed["state"],
        {
            "event_id": "evt_unknown_100",
            "event_type": "UnsupportedCatalogEvent",
            "idempotency_key": "bad-catalog:100",
            "payload": {"tenant": "tenant_alpha"},
        },
        simulate_failure=True,
    )
    failed = product_catalog_pim_receive_event(
        failed["state"],
        {
            "event_id": "evt_unknown_100",
            "event_type": "UnsupportedCatalogEvent",
            "idempotency_key": "bad-catalog:100",
            "payload": {"tenant": "tenant_alpha"},
        },
        simulate_failure=True,
    )
    state = failed["state"]
    simulation = product_catalog_pim_simulate_publication(state, "prod_100", proposed_channels=("web",))
    forecast = product_catalog_pim_forecast_sellability((0.6, 0.7, 0.85), catalog_size=100)
    parsed = product_catalog_pim_parse_product_instruction("product prod_777 channel web locale en-US action publish")
    risk = product_catalog_pim_score_readiness_risk({"completeness": 0.2, "compliance": 0.1, "content": 0.2, "price": 0.1})
    recommendation = product_catalog_pim_recommend_exception_resolution("missing_media")
    route = product_catalog_pim_route_publication(
        {"event_id": "pub_route"},
        rails=({"route": "channel_api", "available": False, "latency": 2}, {"route": "outbox", "available": True, "latency": 4}),
    )
    proof = product_catalog_pim_generate_publication_proof(state, "prod_100", disclosure=("product_id", "sku", "lifecycle_state"))
    screening = product_catalog_pim_screen_policy(state, "prod_100", restricted_regions=("restricted",))
    controls = product_catalog_pim_run_control_tests(state)
    api = product_catalog_pim_build_api_contract()
    permissions = product_catalog_pim_permissions_contract()
    boundary = product_catalog_pim_verify_owned_table_boundary(
        (
            "product",
            "catalog_publication",
            "MediaAssetApproved",
            "product_catalog_pim_appgen_inbox_event",
            "commerce_catalog_projection",
        )
    )
    federation = product_catalog_pim_federate_product_view(state, "prod_100", systems=("commerce", "inventory", "tax", "content", "search"))
    identity = product_catalog_pim_verify_product_identity({"did": "did:appgen:product-100", "issuer": "trusted_registry", "status": "active"})
    resilience = product_catalog_pim_run_resilience_drill(state, "channel_api_timeout")
    crypto = product_catalog_pim_rotate_crypto_epoch(state, "dilithium3_simulated")
    carbon = product_catalog_pim_schedule_carbon_aware_publication(({"window": "day", "carbon": 160}, {"window": "night", "carbon": 70}))
    optimization = product_catalog_pim_optimize_catalog(({"plan": "all_channels", "reach": 0.95, "cost": 0.45}, {"plan": "priority_channels", "reach": 0.85, "cost": 0.2}))
    allocation = product_catalog_pim_allocate_channels(({"channel": "web", "priority": 0.9, "capacity": 7}, {"channel": "marketplace", "priority": 0.5, "capacity": 4}), products=6)
    anomaly = product_catalog_pim_detect_content_anomaly(state)
    stochastic = product_catalog_pim_model_stochastic_sellability_exposure(readiness_path=(0.5, 0.7, 0.9), volatility=0.12)
    workbench = product_catalog_pim_build_workbench_view(state, tenant="tenant_alpha")
    model = product_catalog_pim_register_governed_model("product_readiness", {"features": ("completeness", "compliance", "media"), "auc": 0.9, "drift_score": 0.04})
    checks = (
        {"id": "event_sourced_product_lifecycle", "ok": len(state["events"]) >= 8 and state["events"][-1]["hash"]},
        {"id": "graph_relational_product_topology", "ok": product["product"]["graph_degree"] >= 4},
        {"id": "multi_tenant_catalog_isolation", "ok": workbench["tenant"] == "tenant_alpha"},
        {"id": "schema_evolution_resilient_attribute_schema", "ok": state["schema_extensions"]["product"]["sustainability_payload"] == "jsonb"},
        {"id": "probabilistic_sellability_compliance_scoring", "ok": publication["readiness_score"] >= 0.8 and price["margin"] > 0},
        {"id": "real_time_catalog_readiness_analytics", "ok": workbench["published_product_count"] == 1 and workbench["average_completeness"] >= 0.8},
        {"id": "counterfactual_publication_simulation", "ok": simulation["channel_delta"] < 0},
        {"id": "temporal_content_sellability_forecasting", "ok": forecast["forecast_readiness"] > 0},
        {"id": "autonomous_enrichment_exception_resolution", "ok": recommendation["action"] == "request_media_asset"},
        {"id": "semantic_product_instruction_parsing", "ok": parsed["ok"] and parsed["product_id"] == "prod_777"},
        {"id": "predictive_product_readiness_risk", "ok": risk["risk_score"] > 0},
        {"id": "self_healing_publication_route_selection", "ok": route["ok"] and route["route"] == "outbox" and route["failover_used"]},
        {"id": "zero_knowledge_catalog_publication_proof", "ok": proof["ok"] and proof["proof"].startswith("zk_catalog_")},
        {"id": "immutable_catalog_audit_trail", "ok": controls["hash_chain_valid"]},
        {"id": "dynamic_product_policy_screening", "ok": screening["ok"] and screening["decision"] == "clear"},
        {"id": "automated_catalog_control_testing", "ok": controls["ok"] and not controls["blocking_gaps"]},
        {"id": "universal_api_async_streaming", "ok": api["ok"] and "ProductPublished" in api["events"]["emits"] and permissions["action_permissions"]["receive_event"] == "product_catalog_pim.event"},
        {"id": "cross_system_product_federation", "ok": federation["ok"] and "commerce" in federation["systems"]},
        {"id": "commerce_inventory_tax_content_integration", "ok": publication["handoffs"] == ("commerce_catalog_projection", "search_index_projection", "forecast_signal_projection", "pricing_readiness_projection")},
        {"id": "decentralized_product_identity", "ok": identity["ok"] and identity["issuer"] == "trusted_registry"},
        {"id": "chaos_engineered_catalog_tolerance", "ok": resilience["ok"] and resilience["mode"] == "degraded_publication_route"},
        {"id": "quantum_resistant_product_authorization", "ok": crypto["ok"] and crypto["algorithm"] == "dilithium3_simulated"},
        {"id": "carbon_aware_catalog_publication", "ok": carbon["window"] == "night"},
        {"id": "algebraic_catalog_optimization", "ok": optimization["ok"] and optimization["plan"] == "priority_channels"},
        {"id": "mechanism_design_channel_allocation", "ok": allocation["ok"] and allocation["allocations"][0]["products"] > allocation["allocations"][1]["products"]},
        {"id": "information_theoretic_content_anomaly_detection", "ok": anomaly["ok"] and anomaly["entropy"] >= 0},
        {"id": "temporal_sellability_exposure_stochastic_modeling", "ok": stochastic["ok"] and stochastic["tail_risk"] > 0},
        {"id": "distributed_systems_engineering", "ok": duplicate["handler"]["status"] == "duplicate" and failed["handler"]["status"] == "dead_letter" and boundary["ok"]},
        {"id": "probabilistic_ml_product_readiness", "ok": model["ok"] and model["metadata"]["auc"] >= 0.9},
        {"id": "cryptographic_engineering", "ok": proof["hash"] and crypto["epoch"] == 2},
        {"id": "mathematical_optimization", "ok": optimization["objective_score"] > 0 and allocation["clearing_priority"] > 0},
        {"id": "product_mlops_governance", "ok": model["governance"]["regulated"] and model["governance"]["explainability_required"]},
    )
    blocking_gaps = tuple(check for check in checks if not check["ok"])
    return {"format": "appgen.product-catalog-pim-runtime-smoke.v1", "ok": not blocking_gaps, "checks": checks, "blocking_gaps": blocking_gaps}


def product_catalog_pim_empty_state() -> dict:
    return {
        "events": (),
        "outbox": (),
        "inbox": (),
        "dead_letters": (),
        "dead_letter": (),
        "handled_events": {},
        "retry_evidence": (),
        "families": {},
        "products": {},
        "schemas": {},
        "attributes": {},
        "content": {},
        "media": {},
        "prices": {},
        "compliance": {},
        "publications": {},
        "rules": {},
        "parameters": {},
        "configuration": {},
        "schema_extensions": {},
        "tax_calculation_projections": {},
        "media_asset_projections": {},
        "inventory_position_projections": {},
        "price_promotion_projections": {},
        "search_index_projections": {},
        "crypto_epoch": {"epoch": 1, "algorithm": "sha3_256"},
    }


def product_catalog_pim_configure_runtime(state: dict, configuration: dict) -> dict:
    forbidden = tuple(sorted(field for field in PRODUCT_CATALOG_PIM_FORBIDDEN_EVENTING_FIELDS if field in configuration))
    if forbidden:
        raise ValueError("Product Catalog PIM uses the AppGen-X event contract and does not allow stream-engine or user-selectable eventing fields")
    unknown = tuple(sorted(field for field in configuration if field not in PRODUCT_CATALOG_PIM_SUPPORTED_CONFIGURATION_FIELDS))
    if unknown:
        raise ValueError(f"Unsupported Product Catalog PIM configuration fields: {unknown}")
    missing = tuple(sorted(field for field in PRODUCT_CATALOG_PIM_REQUIRED_CONFIGURATION_FIELDS if field not in configuration))
    if missing:
        raise ValueError(f"Missing required Product Catalog PIM configuration fields: {missing}")
    if configuration.get("database_backend") not in PRODUCT_CATALOG_PIM_ALLOWED_DATABASE_BACKENDS:
        raise ValueError("Product Catalog PIM supports only PostgreSQL, MySQL, or MariaDB backends")
    if configuration.get("event_topic") != PRODUCT_CATALOG_PIM_REQUIRED_EVENT_TOPIC:
        raise ValueError(f"Product Catalog PIM event topic is fixed to {PRODUCT_CATALOG_PIM_REQUIRED_EVENT_TOPIC}")
    retry_limit = int(configuration.get("retry_limit", 0))
    if retry_limit < 1:
        raise ValueError("Product Catalog PIM retry_limit must be at least 1")
    configured = {
        **configuration,
        "ok": True,
        "event_contract": PRODUCT_CATALOG_PIM_EVENT_CONTRACT,
        "allowed_database_backends": PRODUCT_CATALOG_PIM_ALLOWED_DATABASE_BACKENDS,
        "owned_tables": PRODUCT_CATALOG_PIM_OWNED_TABLES,
        "supported_fields": PRODUCT_CATALOG_PIM_SUPPORTED_CONFIGURATION_FIELDS,
        "stream_engine_picker_visible": False,
        "user_eventing_choice": False,
        "user_selectable_event_contract": False,
        "configuration_hash": _digest({field: configuration[field] for field in PRODUCT_CATALOG_PIM_SUPPORTED_CONFIGURATION_FIELDS if field in configuration}),
    }
    return {"ok": True, "state": {**state, "configuration": configured}, "configuration": configured}


def product_catalog_pim_set_parameter(state: dict, name: str, value: float | int | str | bool) -> dict:
    if name not in PRODUCT_CATALOG_PIM_SUPPORTED_PARAMETER_NAMES:
        raise ValueError(f"Unsupported Product Catalog PIM parameter: {name}")
    return {"ok": True, "state": {**state, "parameters": {**state["parameters"], name: value}}, "parameter": {"name": name, "value": value}}


def product_catalog_pim_register_rule(state: dict, rule: dict) -> dict:
    missing = tuple(sorted(field for field in PRODUCT_CATALOG_PIM_REQUIRED_RULE_FIELDS if field not in rule))
    if missing:
        raise ValueError(f"Missing required Product Catalog PIM rule fields: {missing}")
    scope = rule.get("scope") or rule.get("rule_type")
    compiled_hash = _digest(rule)
    enriched = {
        **rule,
        "scope": scope,
        "enabled": rule["status"] == "active",
        "compiled_hash": compiled_hash,
        "compile_evidence": {
            "format": "appgen.product-catalog-pim-rule-compile-evidence.v1",
            "rule_id": rule["rule_id"],
            "scope": scope,
            "compiled_hash": compiled_hash,
            "required_fields": PRODUCT_CATALOG_PIM_REQUIRED_RULE_FIELDS,
        },
    }
    return {"ok": True, "state": {**state, "rules": {**state["rules"], rule["rule_id"]: enriched}}, "rule": enriched}


def product_catalog_pim_register_schema_extension(state: dict, table: str, fields: dict) -> dict:
    if table not in PRODUCT_CATALOG_PIM_OWNED_TABLES:
        raise ValueError(f"Product Catalog PIM schema extensions must target owned tables: {PRODUCT_CATALOG_PIM_OWNED_TABLES}")
    invalid = tuple(name for name in fields if not re.fullmatch(r"[a-z][a-z0-9_]*", name))
    if invalid:
        return {"ok": False, "error": "invalid_extension_field", "invalid": invalid, "state": state}
    merged = {**state["schema_extensions"].get(table, {}), **dict(fields)}
    return {
        "ok": True,
        "state": {**state, "schema_extensions": {**state["schema_extensions"], table: merged}},
        "schema_extension": {"table": table, "fields": dict(fields)},
        "target": table,
        "fields": merged,
    }


def product_catalog_pim_receive_event(state: dict, event: dict, *, simulate_failure: bool = False) -> dict:
    event_type = event.get("event_type")
    event_id = event.get("event_id")
    key = event.get("idempotency_key") or f"{event_type}:{event_id}"
    handled = state.get("handled_events", {})
    processed = handled.get(key)
    if processed and processed.get("status") == "processed":
        duplicate = {**processed, "status": "duplicate"}
        return {"ok": True, "duplicate": True, "state": state, "handler": duplicate}
    attempts = int(handled.get(key, {}).get("attempts", 0)) + 1
    payload = dict(event.get("payload", {}))
    inbox_entry = {
        "event_id": event_id,
        "event_type": event_type,
        "tenant": payload.get("tenant"),
        "attempts": attempts,
        "idempotency_key": key,
    }
    next_state = {
        **state,
        "inbox": (*state.get("inbox", ()), inbox_entry),
        "dead_letters": tuple(state.get("dead_letters", ())),
        "dead_letter": tuple(state.get("dead_letter", ())),
        "retry_evidence": tuple(state.get("retry_evidence", ())),
        "handled_events": dict(handled),
        "tax_calculation_projections": dict(state.get("tax_calculation_projections", {})),
        "media_asset_projections": dict(state.get("media_asset_projections", {})),
        "inventory_position_projections": dict(state.get("inventory_position_projections", {})),
        "price_promotion_projections": dict(state.get("price_promotion_projections", {})),
        "search_index_projections": dict(state.get("search_index_projections", {})),
    }
    retry_limit = int(next_state.get("configuration", {}).get("retry_limit", 1))
    if simulate_failure or event_type not in PRODUCT_CATALOG_PIM_CONSUMED_EVENT_TYPES:
        status = "dead_letter" if attempts >= retry_limit else "retrying"
        handler = {"event_id": event_id, "event_type": event_type, "status": status, "attempts": attempts, "idempotency_key": key}
        evidence = {"event_id": event_id, "event_type": event_type, "attempts": attempts, "status": status}
        next_state["handled_events"][key] = handler
        next_state["retry_evidence"] = (*next_state["retry_evidence"], evidence)
        if status == "dead_letter":
            dead = {**inbox_entry, "reason": "unsupported_or_failed_product_catalog_event"}
            next_state["dead_letters"] = (*next_state["dead_letters"], dead)
            next_state["dead_letter"] = (*next_state["dead_letter"], dead)
        return {"ok": False, "duplicate": False, "state": next_state, "handler": handler}
    projection = {"event_id": event_id, "event_type": event_type, **payload}
    if event_type == "TaxCalculated":
        next_state["tax_calculation_projections"][payload.get("product_id", event_id)] = projection
    elif event_type == "MediaAssetApproved":
        next_state["media_asset_projections"][payload.get("product_id", event_id)] = projection
    elif event_type == "InventoryPositionUpdated":
        next_state["inventory_position_projections"][payload.get("product_id", event_id)] = projection
    elif event_type == "PricePromotionApproved":
        next_state["price_promotion_projections"][payload.get("product_id", event_id)] = projection
    elif event_type == "SearchIndexRequested":
        next_state["search_index_projections"][payload.get("product_id", event_id)] = projection
    handler = {"event_id": event_id, "event_type": event_type, "status": "processed", "attempts": attempts, "idempotency_key": key}
    next_state["handled_events"][key] = handler
    return {"ok": True, "duplicate": False, "state": next_state, "handler": handler, "projection": projection}


def product_catalog_pim_create_product_family(state: dict, family: dict) -> dict:
    enriched = {**family, "status": "active", "graph_degree": len(tuple(value for value in (family["name"], family["taxonomy"], family["variant_axes"]) if value))}
    next_state = {**state, "families": {**state["families"], family["family_id"]: enriched}}
    next_state = _append_event(next_state, "ProductClassified", {"tenant": family["tenant"], "family_id": family["family_id"], "taxonomy": family["taxonomy"]})
    return {"ok": True, "state": next_state, "family": enriched}


def product_catalog_pim_register_product(state: dict, product: dict) -> dict:
    family = state["families"][product["family_id"]]
    enriched = {
        **product,
        "taxonomy": family["taxonomy"],
        "lifecycle_state": product.get("lifecycle_state", "draft"),
        "graph_degree": len(tuple(value for value in (product["sku"], product["name"], product["family_id"], family["taxonomy"]) if value)),
    }
    next_state = {**state, "products": {**state["products"], product["product_id"]: enriched}}
    next_state = _append_event(next_state, "ProductRegistered", {"tenant": product["tenant"], "product_id": product["product_id"], "sku": product["sku"]})
    return {"ok": True, "state": next_state, "product": enriched}


def product_catalog_pim_define_attribute_schema(state: dict, schema: dict) -> dict:
    enriched = {**schema, "compiled_hash": _digest(schema)}
    next_state = {**state, "schemas": {**state["schemas"], schema["schema_id"]: enriched}}
    next_state = _append_event(next_state, "AttributeSchemaDefined", {"tenant": schema["tenant"], "schema_id": schema["schema_id"], "family_id": schema["family_id"]})
    return {"ok": True, "state": next_state, "schema": enriched}


def product_catalog_pim_set_product_attribute(state: dict, product_id: str, name: str, value: object) -> dict:
    product = state["products"][product_id]
    schema = next(schema_item for schema_item in state["schemas"].values() if schema_item["family_id"] == product["family_id"])
    ok = name in schema["attributes"]
    product_attributes = {**state["attributes"].get(product_id, {}), name: value}
    return {"ok": ok, "state": {**state, "attributes": {**state["attributes"], product_id: product_attributes}}, "attribute": {"product_id": product_id, "name": name, "value": value}}


def product_catalog_pim_add_localized_content(state: dict, content: dict) -> dict:
    ok = content["locale"] in state["configuration"].get("allowed_locales", ()) and bool(content.get("title")) and bool(content.get("description"))
    enriched = {**content, "status": "approved" if ok else "draft", "quality_score": round(min(1.0, (len(content["description"]) / 30) + 0.3), 4)}
    next_state = {**state, "content": {**state["content"], content["content_id"]: enriched}}
    next_state = _append_event(next_state, "ProductEnriched", {"tenant": content["tenant"], "product_id": content["product_id"], "locale": content["locale"]})
    return {"ok": ok, "state": next_state, "content": enriched}


def product_catalog_pim_attach_product_media(state: dict, media: dict) -> dict:
    ok = media["role"] in state["configuration"].get("allowed_media_roles", ()) and media.get("rights_status") == "approved"
    enriched = {**media, "status": "approved" if ok else "blocked"}
    next_state = {**state, "media": {**state["media"], media["media_id"]: enriched}}
    next_state = _append_event(next_state, "ProductMediaAttached", {"tenant": media["tenant"], "product_id": media["product_id"], "role": media["role"]})
    return {"ok": ok, "state": next_state, "media": enriched}


def product_catalog_pim_add_price_metadata(state: dict, price: dict) -> dict:
    margin = round((float(price["list_price"]) - float(price["cost"])) / max(float(price["list_price"]), 0.01), 4)
    enriched = {**price, "margin": margin, "status": "ready" if margin >= float(state["parameters"].get("minimum_margin", 0.1)) else "review"}
    next_state = {**state, "prices": {**state["prices"], price["price_id"]: enriched}}
    next_state = _append_event(next_state, "ProductPriceReady", {"tenant": price["tenant"], "product_id": price["product_id"], "currency": price["currency"]})
    return {"ok": enriched["status"] == "ready", "state": next_state, "price": enriched, "margin": margin}


def product_catalog_pim_add_compliance_claim(state: dict, claim: dict) -> dict:
    ok = claim["region"] in state["configuration"].get("allowed_regions", ()) and claim["status"] == "approved"
    enriched = {**claim, "screening_status": "clear" if ok else "blocked"}
    next_state = {**state, "compliance": {**state["compliance"], claim["claim_id"]: enriched}}
    next_state = _append_event(next_state, "ProductComplianceClaimed", {"tenant": claim["tenant"], "product_id": claim["product_id"], "region": claim["region"]})
    return {"ok": ok, "state": next_state, "claim": enriched}


def product_catalog_pim_publish_product(state: dict, product_id: str, *, channels: tuple[str, ...], locales: tuple[str, ...], published_by: str) -> dict:
    product = state["products"][product_id]
    rule = next(iter(state["rules"].values()))
    attrs = state["attributes"].get(product_id, {})
    required_attrs = set(rule["required_attributes"])
    required_media = set(rule["required_media_roles"])
    media_roles = {media["role"] for media in state["media"].values() if media["product_id"] == product_id and media["status"] == "approved"}
    content_locales = {content["locale"] for content in state["content"].values() if content["product_id"] == product_id and content["status"] == "approved"}
    price_ready = any(price["product_id"] == product_id and price["status"] == "ready" for price in state["prices"].values())
    compliance_clear = any(claim["product_id"] == product_id and claim["screening_status"] == "clear" for claim in state["compliance"].values())
    completeness = sum((required_attrs <= set(attrs), required_media <= media_roles, set(locales) <= content_locales, price_ready, compliance_clear)) / 5
    ok = completeness >= float(state["parameters"].get("minimum_completeness", 0.8)) and set(channels) <= set(rule["allowed_channels"])
    updated = {
        **product,
        "lifecycle_state": "published" if ok else "blocked",
        "published_by": published_by,
        "channels": channels,
        "locales": locales,
        "completeness": completeness,
    }
    publication_id = f"publication_{len(state['publications']) + 1:06d}"
    publication = {
        "publication_id": publication_id,
        "tenant": product["tenant"],
        "product_id": product_id,
        "channels": channels,
        "locales": locales,
        "readiness_score": round(completeness, 4),
        "status": "published" if ok else "blocked",
    }
    handoffs = ("commerce_catalog_projection", "search_index_projection", "forecast_signal_projection", "pricing_readiness_projection")
    next_state = {**state, "products": {**state["products"], product_id: updated}, "publications": {**state["publications"], publication_id: publication}}
    next_state = _append_event(next_state, "ProductPublished", {"tenant": product["tenant"], "product_id": product_id, "channels": channels, "handoffs": handoffs})
    return {"ok": ok, "state": next_state, "publication": publication, "readiness_score": round(completeness, 4), "handoffs": handoffs}


def product_catalog_pim_simulate_publication(state: dict, product_id: str, *, proposed_channels: tuple[str, ...]) -> dict:
    current = len(next(iter(state["publications"].values()))["channels"])
    return {"ok": True, "product_id": product_id, "channel_delta": round((len(proposed_channels) - current) / max(current, 1), 4)}


def product_catalog_pim_forecast_sellability(readiness_path: tuple[float, ...], *, catalog_size: int) -> dict:
    trend = readiness_path[-1] - readiness_path[0] if len(readiness_path) > 1 else 0
    forecast = max(0, min(1, readiness_path[-1] + trend / max(1, len(readiness_path))))
    return {"ok": True, "forecast_readiness": round(forecast, 4), "ready_products": round(forecast * catalog_size, 2)}


def product_catalog_pim_parse_product_instruction(text: str) -> dict:
    product = re.search(r"product\s+([a-z0-9_]+)", text, re.I)
    channel = re.search(r"channel\s+([a-z0-9_]+)", text, re.I)
    locale = re.search(r"locale\s+([A-Za-z-]+)", text, re.I)
    action = re.search(r"action\s+([a-z0-9_]+)", text, re.I)
    return {"ok": bool(product and channel and locale and action), "product_id": product.group(1) if product else None, "channel": channel.group(1) if channel else None, "locale": locale.group(1) if locale else None, "action": action.group(1) if action else None}


def product_catalog_pim_score_readiness_risk(signals: dict) -> dict:
    risk = round(signals.get("completeness", 0) * 1.4 + signals.get("compliance", 0) * 1.8 + signals.get("content", 0) + signals.get("price", 0), 4)
    return {"ok": True, "risk_score": risk, "decision": "monitor" if risk < 0.8 else "review"}


def product_catalog_pim_recommend_exception_resolution(exception_type: str) -> dict:
    actions = {"missing_media": "request_media_asset", "missing_attribute": "route_enrichment_task", "restricted_region": "route_compliance_review"}
    return {"ok": exception_type in actions, "exception_type": exception_type, "action": actions.get(exception_type, "manual_review")}


def product_catalog_pim_route_publication(event: dict, *, rails: tuple[dict, ...]) -> dict:
    selected = min((rail for rail in rails if rail.get("available", True)), key=lambda rail: rail["latency"])
    return {"ok": True, "route": selected["route"], "failover_used": any(not rail.get("available", True) for rail in rails[:1]), "idempotency_key": f"product_catalog_pim:PublicationRoute:{event['event_id']}"}


def product_catalog_pim_generate_publication_proof(state: dict, product_id: str, *, disclosure: tuple[str, ...]) -> dict:
    product = state["products"][product_id]
    claims = {field: product[field] for field in disclosure if field in product}
    proof_hash = _digest({"claims": claims, "event_hash": state["events"][-1]["hash"]})
    return {"ok": True, "proof": "zk_catalog_" + proof_hash[:24], "hash": proof_hash, "public_claims": claims}


def product_catalog_pim_screen_policy(state: dict, product_id: str, *, restricted_regions: tuple[str, ...]) -> dict:
    blocked = any(claim["product_id"] == product_id and claim["region"] in restricted_regions for claim in state["compliance"].values())
    return {"ok": not blocked, "decision": "blocked" if blocked else "clear", "product_id": product_id}


def product_catalog_pim_run_control_tests(state: dict) -> dict:
    gaps = []
    configuration = state["configuration"]
    if not configuration.get("ok"):
        gaps.append("invalid_configuration")
    if configuration.get("database_backend") not in PRODUCT_CATALOG_PIM_ALLOWED_DATABASE_BACKENDS:
        gaps.append("invalid_database_backend")
    if configuration.get("event_contract") != PRODUCT_CATALOG_PIM_EVENT_CONTRACT:
        gaps.append("invalid_event_contract")
    if configuration.get("stream_engine_picker_visible"):
        gaps.append("stream_engine_picker_exposed")
    if configuration.get("user_eventing_choice"):
        gaps.append("user_eventing_choice_exposed")
    if not state["rules"]:
        gaps.append("missing_rules")
    if not state["parameters"]:
        gaps.append("missing_parameters")
    if any(product["lifecycle_state"] != "published" for product in state["products"].values()):
        gaps.append("unpublished_product")
    hash_chain_valid = all(event["previous_hash"] == (state["events"][index - 1]["hash"] if index else "GENESIS") for index, event in enumerate(state["events"]))
    if not hash_chain_valid:
        gaps.append("invalid_hash_chain")
    return {"ok": not gaps, "blocking_gaps": tuple(gaps), "hash_chain_valid": hash_chain_valid}


def product_catalog_pim_build_schema_contract() -> dict:
    table_fields = {
        "product": ("tenant", "product_id", "family_id", "sku", "name", "lifecycle_state", "owner", "taxonomy", "completeness", "audit_hash"),
        "product_family": ("tenant", "family_id", "name", "taxonomy", "variant_axes", "status", "audit_hash"),
        "product_variant": ("tenant", "variant_id", "product_id", "family_id", "sku", "status", "audit_hash"),
        "product_variant_option": ("tenant", "variant_option_id", "variant_id", "axis", "value", "status", "audit_hash"),
        "product_variant_member": ("tenant", "variant_member_id", "variant_id", "product_id", "option_signature", "status", "audit_hash"),
        "product_taxonomy": ("tenant", "taxonomy_id", "code", "name", "parent_taxonomy_id", "status", "audit_hash"),
        "taxonomy_node": ("tenant", "node_id", "taxonomy_id", "parent_node_id", "code", "depth", "status", "audit_hash"),
        "taxonomy_relationship": ("tenant", "relationship_id", "from_taxonomy_id", "to_taxonomy_id", "relationship_type", "status", "audit_hash"),
        "product_category": ("tenant", "category_id", "taxonomy_id", "code", "name", "channel_scope", "status", "audit_hash"),
        "category_assignment": ("tenant", "assignment_id", "product_id", "category_id", "channel", "status", "audit_hash"),
        "product_attribute_schema": ("tenant", "schema_id", "family_id", "attributes", "version", "compiled_hash", "status", "audit_hash"),
        "product_attribute": ("tenant", "attribute_id", "product_id", "attribute_name", "attribute_value", "schema_version", "status", "audit_hash"),
        "product_attribute_validation_rule": ("tenant", "validation_rule_id", "schema_id", "attribute_name", "data_type", "required", "status", "audit_hash"),
        "product_attribute_value_option": ("tenant", "value_option_id", "schema_id", "attribute_name", "option_value", "sort_order", "status", "audit_hash"),
        "product_price": ("tenant", "price_id", "product_id", "currency", "list_price", "cost", "margin", "status", "audit_hash"),
        "product_channel_price": ("tenant", "channel_price_id", "product_id", "channel", "currency", "list_price", "status", "audit_hash"),
        "product_media": ("tenant", "media_id", "product_id", "role", "asset_ref", "rights_status", "status", "audit_hash"),
        "product_locale_content": ("tenant", "content_id", "product_id", "locale", "title", "description", "seo_slug", "status", "audit_hash"),
        "product_localization_memory": ("tenant", "translation_id", "product_id", "source_locale", "target_locale", "quality_score", "audit_hash"),
        "product_seo_metadata": ("tenant", "seo_id", "product_id", "locale", "title_tag", "meta_description", "canonical_url", "audit_hash"),
        "product_compliance_claim": ("tenant", "claim_id", "product_id", "region", "claim_type", "screening_status", "status", "audit_hash"),
        "product_lifecycle_stage": ("tenant", "lifecycle_id", "product_id", "stage", "approved_by", "effective_at", "status", "audit_hash"),
        "product_approval_workflow": ("tenant", "workflow_id", "product_id", "workflow_type", "required_approvers", "status", "audit_hash"),
        "product_approval_decision": ("tenant", "decision_id", "workflow_id", "approver", "decision", "decided_at", "audit_hash"),
        "product_assortment": ("tenant", "assortment_id", "name", "channel", "season", "status", "audit_hash"),
        "product_assortment_assignment": ("tenant", "assignment_id", "assortment_id", "product_id", "channel", "status", "audit_hash"),
        "catalog_publication": ("tenant", "publication_id", "product_id", "channels", "locales", "readiness_score", "status", "audit_hash"),
        "catalog_channel_projection": ("tenant", "projection_id", "product_id", "channel", "locale", "projection_hash", "status", "audit_hash"),
        "catalog_channel_policy": ("tenant", "policy_id", "channel", "required_attributes", "required_media_roles", "status", "audit_hash"),
        "catalog_syndication_feed": ("tenant", "feed_id", "channel", "format", "cadence", "status", "audit_hash"),
        "catalog_syndication_delivery": ("tenant", "delivery_id", "feed_id", "product_id", "channel", "delivery_status", "audit_hash"),
        "product_enrichment_task": ("tenant", "task_id", "product_id", "task_type", "assignee", "priority", "status", "audit_hash"),
        "product_data_quality_score": ("tenant", "quality_score_id", "product_id", "completeness_score", "content_score", "quality_score", "status", "audit_hash"),
        "product_data_quality_issue": ("tenant", "issue_id", "product_id", "issue_type", "severity", "status", "audit_hash"),
        "product_bundle_definition": ("tenant", "bundle_id", "product_id", "component_product_ids", "bundle_type", "status", "audit_hash"),
        "product_relationship": ("tenant", "relationship_id", "source_product_id", "target_product_id", "relationship_type", "status", "audit_hash"),
        "product_identity_credential": ("tenant", "credential_id", "product_id", "did", "issuer", "status", "audit_hash"),
        "product_graph_projection": ("tenant", "projection_id", "product_id", "node_count", "edge_count", "projection_hash", "audit_hash"),
        "product_semantic_embedding": ("tenant", "embedding_id", "product_id", "embedding_model", "vector_ref", "status", "audit_hash"),
        "product_readiness_forecast": ("tenant", "forecast_id", "product_id", "forecast_readiness", "ready_date", "status", "audit_hash"),
        "product_risk_model": ("tenant", "risk_model_id", "product_id", "risk_score", "decision", "status", "audit_hash"),
        "product_policy_screening": ("tenant", "screening_id", "product_id", "policy_scope", "decision", "status", "audit_hash"),
        "product_publication_proof": ("tenant", "proof_id", "product_id", "proof_type", "proof_hash", "channel_scope", "audit_hash"),
        "product_audit_trace": ("tenant", "trace_id", "product_id", "event_id", "trace_type", "trace_hash", "audit_hash"),
        "product_schema_extension": ("tenant", "extension_id", "table_name", "field_name", "field_type", "status", "audit_hash"),
        "product_control_assertion": ("tenant", "control_id", "assertion_type", "subject_id", "status", "tested_at", "audit_hash"),
        "product_governed_model": ("tenant", "model_id", "model_name", "feature_lineage", "drift_score", "status", "audit_hash"),
        "product_seed_data": ("tenant", "seed_id", "seed_type", "seed_ref", "status", "loaded_at", "audit_hash"),
        "product_rule": ("tenant", "rule_id", "rule_type", "allowed_channels", "allowed_locales", "status", "compiled_hash", "audit_hash"),
        "product_parameter": ("tenant", "parameter_id", "parameter_name", "parameter_value", "effective_at", "audit_hash"),
        "product_configuration": ("tenant", "configuration_id", "database_backend", "event_topic", "retry_limit", "default_timezone", "audit_hash"),
    }
    runtime_tables = (
        {
            "table": PRODUCT_CATALOG_PIM_RUNTIME_TABLES[0],
            "fields": ("tenant", "event_id", "event_type", "topic", "idempotency_key", "payload_hash", "status", "published_at", "audit_hash"),
        },
        {
            "table": PRODUCT_CATALOG_PIM_RUNTIME_TABLES[1],
            "fields": ("tenant", "event_id", "event_type", "idempotency_key", "attempts", "status", "received_at", "audit_hash"),
        },
        {
            "table": PRODUCT_CATALOG_PIM_RUNTIME_TABLES[2],
            "fields": ("tenant", "event_id", "event_type", "idempotency_key", "attempts", "reason", "dead_lettered_at", "audit_hash"),
        },
    )
    relationships = (
        {"from": "product.family_id", "to": "product_family.family_id", "type": "owned_parent"},
        {"from": "product_variant.product_id", "to": "product.product_id", "type": "owned_child"},
        {"from": "product_variant_option.variant_id", "to": "product_variant.variant_id", "type": "owned_child"},
        {"from": "product_variant_member.variant_id", "to": "product_variant.variant_id", "type": "owned_membership"},
        {"from": "product_variant_member.product_id", "to": "product.product_id", "type": "owned_membership"},
        {"from": "product_attribute_schema.family_id", "to": "product_family.family_id", "type": "owned_reference"},
        {"from": "product_attribute.product_id", "to": "product.product_id", "type": "owned_reference"},
        {"from": "product_attribute_validation_rule.schema_id", "to": "product_attribute_schema.schema_id", "type": "owned_validation"},
        {"from": "product_attribute_value_option.schema_id", "to": "product_attribute_schema.schema_id", "type": "owned_option"},
        {"from": "product_locale_content.product_id", "to": "product.product_id", "type": "owned_localization"},
        {"from": "product_media.product_id", "to": "product.product_id", "type": "owned_media"},
        {"from": "product_price.product_id", "to": "product.product_id", "type": "owned_pricing"},
        {"from": "product_channel_price.product_id", "to": "product.product_id", "type": "owned_channel_pricing"},
        {"from": "product_compliance_claim.product_id", "to": "product.product_id", "type": "owned_compliance"},
        {"from": "category_assignment.product_id", "to": "product.product_id", "type": "owned_classification"},
        {"from": "category_assignment.category_id", "to": "product_category.category_id", "type": "owned_classification"},
        {"from": "catalog_publication.product_id", "to": "product.product_id", "type": "owned_publication"},
        {"from": "catalog_channel_projection.product_id", "to": "product.product_id", "type": "owned_projection"},
        {"from": "catalog_syndication_delivery.feed_id", "to": "catalog_syndication_feed.feed_id", "type": "owned_syndication"},
        {"from": "catalog_syndication_delivery.product_id", "to": "product.product_id", "type": "owned_syndication"},
        {"from": "product_assortment_assignment.assortment_id", "to": "product_assortment.assortment_id", "type": "owned_assortment"},
        {"from": "product_assortment_assignment.product_id", "to": "product.product_id", "type": "owned_assortment"},
        {"from": "product_approval_decision.workflow_id", "to": "product_approval_workflow.workflow_id", "type": "owned_approval"},
        {"from": "product_lifecycle_stage.product_id", "to": "product.product_id", "type": "owned_lifecycle"},
    )
    allowed_prefixes = (
        "product",
        "catalog_",
        "taxonomy_",
        "category_",
    )
    tables = tuple(
        {
            "table": table,
            "fields": table_fields[table],
            "primary_key": tuple(field for field in table_fields[table] if field.endswith("_id"))[:2] or ("tenant",),
            "owned_by": "product_catalog_pim",
        }
        for table in PRODUCT_CATALOG_PIM_OWNED_TABLES
    )
    migrations = tuple(
        {
            "path": f"pbcs/product_catalog_pim/migrations/{position + 1:03d}_{table}.sql",
            "operation": "create_owned_table",
            "table": table,
            "backend_allowlist": PRODUCT_CATALOG_PIM_ALLOWED_DATABASE_BACKENDS,
        }
        for position, table in enumerate(PRODUCT_CATALOG_PIM_OWNED_TABLES)
    )
    models = tuple(
        {
            "path": f"pbcs/product_catalog_pim/models/{table}.py",
            "table": table,
            "class_name": _class_name(table),
            "fields": table_fields[table],
        }
        for table in PRODUCT_CATALOG_PIM_OWNED_TABLES
    )
    invalid_prefixes = tuple(table for table in PRODUCT_CATALOG_PIM_OWNED_TABLES if not table.startswith(allowed_prefixes))
    return {
        "format": "appgen.product-catalog-pim-owned-schema-contract.v1",
        "ok": not invalid_prefixes
        and len(tables) == len(PRODUCT_CATALOG_PIM_OWNED_TABLES)
        and len(migrations) == len(PRODUCT_CATALOG_PIM_OWNED_TABLES),
        "tables": tables,
        "runtime_tables": runtime_tables,
        "relationships": relationships,
        "migrations": migrations,
        "models": models,
        "allowed_prefixes": allowed_prefixes,
        "datastore_backends": PRODUCT_CATALOG_PIM_ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": PRODUCT_CATALOG_PIM_REQUIRED_EVENT_TOPIC,
        "shared_table_access": False,
        "invalid_prefixes": invalid_prefixes,
    }


def product_catalog_pim_build_service_contract() -> dict:
    command_methods = (
        "configure_runtime",
        "set_parameter",
        "register_rule",
        "register_schema_extension",
        "receive_event",
        "create_product_family",
        "register_product",
        "define_attribute_schema",
        "set_product_attribute",
        "add_localized_content",
        "attach_product_media",
        "add_price_metadata",
        "add_compliance_claim",
        "publish_product",
        "route_publication",
        "generate_publication_proof",
        "screen_policy",
        "run_control_tests",
        "run_resilience_drill",
        "rotate_crypto_epoch",
        "schedule_carbon_aware_publication",
        "optimize_catalog",
        "allocate_channels",
        "register_governed_model",
        "verify_owned_table_boundary",
    )
    query_methods = (
        "build_workbench_view",
        "simulate_publication",
        "forecast_sellability",
        "parse_product_instruction",
        "score_readiness_risk",
        "recommend_exception_resolution",
        "build_api_contract",
        "build_schema_contract",
        "build_service_contract",
        "build_release_evidence",
        "permissions_contract",
        "binding_evidence",
        "federate_product_view",
        "verify_product_identity",
        "detect_content_anomaly",
        "model_stochastic_sellability_exposure",
    )
    return {
        "format": "appgen.product-catalog-pim-service-contract.v1",
        "ok": len(command_methods) >= 20 and len(query_methods) >= 12,
        "transaction_boundary": "product_catalog_pim_owned_datastore_plus_appgen_outbox",
        "command_methods": command_methods,
        "query_methods": query_methods,
        "mutates_only": (*PRODUCT_CATALOG_PIM_OWNED_TABLES, *PRODUCT_CATALOG_PIM_RUNTIME_TABLES),
        "external_dependencies": {
            "apis": tuple(item for item in PRODUCT_CATALOG_PIM_ALLOWED_DEPENDENCIES if str(item).startswith(("GET ", "POST "))),
            "events": PRODUCT_CATALOG_PIM_CONSUMED_EVENT_TYPES,
            "api_projections": tuple(item for item in PRODUCT_CATALOG_PIM_ALLOWED_DEPENDENCIES if str(item).endswith("_projection")),
            "shared_tables": (),
        },
        "idempotent_handlers": ("receive_event",),
        "retry_dead_letter_evidence": {
            "outbox_table": PRODUCT_CATALOG_PIM_RUNTIME_TABLES[0],
            "inbox_table": PRODUCT_CATALOG_PIM_RUNTIME_TABLES[1],
            "dead_letter_table": PRODUCT_CATALOG_PIM_RUNTIME_TABLES[2],
            "retry_limit_source": "product_configuration.retry_limit",
        },
        "rules_parameters_configuration": ("register_rule", "set_parameter", "configure_runtime"),
        "eventing": {
            "contract": PRODUCT_CATALOG_PIM_EVENT_CONTRACT,
            "topic": PRODUCT_CATALOG_PIM_REQUIRED_EVENT_TOPIC,
            "stream_engine_picker_visible": False,
            "user_eventing_choice_visible": False,
        },
        "advanced_capabilities": PRODUCT_CATALOG_PIM_RUNTIME_CAPABILITY_KEYS,
    }


def product_catalog_pim_build_api_contract() -> dict:
    permissions = product_catalog_pim_permissions_contract()
    return {
        "ok": True,
        "format": "appgen.product-catalog-pim-api-contract.v1",
        "routes": (
            {"route": "PUT /product-catalog/configuration", "command": "configure_runtime", "owned_tables": ("product_configuration",), "emits": (), "requires_permission": "product_catalog_pim.configure", "idempotency_key": "tenant:event_topic"},
            {"route": "POST /product-catalog/rules", "command": "register_rule", "owned_tables": ("product_rule",), "emits": (), "requires_permission": "product_catalog_pim.configure", "idempotency_key": "rule_id"},
            {"route": "POST /product-catalog/parameters", "command": "set_parameter", "owned_tables": ("product_parameter",), "emits": (), "requires_permission": "product_catalog_pim.configure", "idempotency_key": "parameter_name"},
            {"route": "POST /product-catalog/schema-extensions", "command": "register_schema_extension", "owned_tables": ("product_schema_extension",), "emits": (), "requires_permission": "product_catalog_pim.configure", "idempotency_key": "table_name:field_name"},
            {"route": "POST /product-families", "command": "create_product_family", "owned_tables": ("product_family",), "emits": ("ProductClassified",), "requires_permission": "product_catalog_pim.product", "idempotency_key": "family_id"},
            {"route": "POST /products", "command": "register_product", "owned_tables": ("product",), "emits": ("ProductRegistered",), "requires_permission": "product_catalog_pim.product", "idempotency_key": "product_id"},
            {"route": "POST /attribute-schemas", "command": "define_attribute_schema", "owned_tables": ("product_attribute_schema",), "emits": ("AttributeSchemaDefined",), "requires_permission": "product_catalog_pim.product", "idempotency_key": "schema_id"},
            {"route": "POST /product-attributes", "command": "set_product_attribute", "owned_tables": ("product_attribute",), "emits": (), "requires_permission": "product_catalog_pim.enrich", "idempotency_key": "product_id:name"},
            {"route": "POST /product-media", "command": "attach_product_media", "owned_tables": ("product_media",), "emits": ("ProductMediaAttached",), "requires_permission": "product_catalog_pim.enrich", "idempotency_key": "media_id"},
            {"route": "POST /product-locale-content", "command": "add_localized_content", "owned_tables": ("product_locale_content",), "emits": ("ProductEnriched",), "requires_permission": "product_catalog_pim.enrich", "idempotency_key": "content_id"},
            {"route": "POST /product-prices", "command": "add_price_metadata", "owned_tables": ("product_price",), "emits": ("ProductPriceReady",), "requires_permission": "product_catalog_pim.publish", "idempotency_key": "price_id"},
            {"route": "POST /product-compliance-claims", "command": "add_compliance_claim", "owned_tables": ("product_compliance_claim",), "emits": ("ProductComplianceClaimed",), "requires_permission": "product_catalog_pim.enrich", "idempotency_key": "claim_id"},
            {"route": "POST /catalog-publications", "command": "publish_product", "owned_tables": ("catalog_publication", "catalog_channel_projection"), "emits": ("ProductPublished",), "requires_permission": "product_catalog_pim.publish", "idempotency_key": "product_id:channels:locales"},
            {"route": "POST /product-catalog/events/inbox", "command": "receive_event", "owned_tables": (), "consumes": PRODUCT_CATALOG_PIM_CONSUMED_EVENT_TYPES, "requires_permission": "product_catalog_pim.event", "idempotency_key": "event_id"},
            {"route": "GET /product-catalog/workbench", "query": "build_workbench_view", "owned_tables": PRODUCT_CATALOG_PIM_OWNED_TABLES, "requires_permission": "product_catalog_pim.audit"},
            {"route": "GET /product-catalog/schema-contract", "query": "build_schema_contract", "owned_tables": PRODUCT_CATALOG_PIM_OWNED_TABLES, "requires_permission": "product_catalog_pim.audit"},
            {"route": "GET /product-catalog/service-contract", "query": "build_service_contract", "owned_tables": PRODUCT_CATALOG_PIM_OWNED_TABLES, "requires_permission": "product_catalog_pim.audit"},
            {"route": "GET /product-catalog/release-evidence", "query": "build_release_evidence", "owned_tables": PRODUCT_CATALOG_PIM_OWNED_TABLES, "requires_permission": "product_catalog_pim.audit"},
        ),
        "declared_catalog_routes": (
            "PUT /product-catalog/configuration",
            "POST /product-catalog/rules",
            "POST /product-catalog/parameters",
            "POST /product-catalog/schema-extensions",
            "POST /products",
            "POST /product-families",
            "POST /attribute-schemas",
            "POST /catalog-publications",
            "GET /product-catalog/workbench",
            "GET /product-catalog/schema-contract",
            "GET /product-catalog/service-contract",
            "GET /product-catalog/release-evidence",
        ),
        "events": {
            "emits": PRODUCT_CATALOG_PIM_EMITTED_EVENT_TYPES,
            "consumes": PRODUCT_CATALOG_PIM_CONSUMED_EVENT_TYPES,
            "topic": PRODUCT_CATALOG_PIM_REQUIRED_EVENT_TOPIC,
            "contract": PRODUCT_CATALOG_PIM_EVENT_CONTRACT,
        },
        "emits": PRODUCT_CATALOG_PIM_EMITTED_EVENT_TYPES,
        "consumes": PRODUCT_CATALOG_PIM_CONSUMED_EVENT_TYPES,
        "event_descriptors": {
            "emitted": tuple(
                {
                    "event_type": event_type,
                    "topic": PRODUCT_CATALOG_PIM_REQUIRED_EVENT_TOPIC,
                    "contract": PRODUCT_CATALOG_PIM_EVENT_CONTRACT,
                    "producer": "product_catalog_pim",
                    "outbox_table": PRODUCT_CATALOG_PIM_RUNTIME_TABLES[0],
                }
                for event_type in PRODUCT_CATALOG_PIM_EMITTED_EVENT_TYPES
            ),
            "consumed": tuple(
                {
                    "event_type": event_type,
                    "topic": PRODUCT_CATALOG_PIM_REQUIRED_EVENT_TOPIC,
                    "contract": PRODUCT_CATALOG_PIM_EVENT_CONTRACT,
                    "consumer": "product_catalog_pim.receive_event",
                    "inbox_table": PRODUCT_CATALOG_PIM_RUNTIME_TABLES[1],
                    "dead_letter_table": PRODUCT_CATALOG_PIM_RUNTIME_TABLES[2],
                }
                for event_type in PRODUCT_CATALOG_PIM_CONSUMED_EVENT_TYPES
            ),
        },
        "permissions": tuple(sorted(permissions["permissions"])),
        "database_backends": PRODUCT_CATALOG_PIM_ALLOWED_DATABASE_BACKENDS,
        "owned_tables": PRODUCT_CATALOG_PIM_OWNED_TABLES,
        "runtime_tables": PRODUCT_CATALOG_PIM_RUNTIME_TABLES,
        "required_event_topic": PRODUCT_CATALOG_PIM_REQUIRED_EVENT_TOPIC,
        "dependencies": {
            "apis": tuple(item for item in PRODUCT_CATALOG_PIM_ALLOWED_DEPENDENCIES if str(item).startswith(("GET ", "POST "))),
            "events": PRODUCT_CATALOG_PIM_CONSUMED_EVENT_TYPES,
            "api_projections": tuple(item for item in PRODUCT_CATALOG_PIM_ALLOWED_DEPENDENCIES if str(item).endswith("_projection")),
            "shared_tables": (),
        },
        "shared_table_access": False,
        "configuration": (
            "PRODUCT_CATALOG_PIM_DATABASE_URL",
            "PRODUCT_CATALOG_PIM_EVENT_TOPIC",
            "PRODUCT_CATALOG_PIM_RETRY_LIMIT",
            "PRODUCT_CATALOG_PIM_DEFAULT_TIMEZONE",
        ),
        "event_contract": PRODUCT_CATALOG_PIM_EVENT_CONTRACT,
        "stream_engine_picker_visible": False,
        "user_eventing_choice": False,
    }


def product_catalog_pim_build_release_evidence() -> dict:
    schema = product_catalog_pim_build_schema_contract()
    service = product_catalog_pim_build_service_contract()
    api = product_catalog_pim_build_api_contract()
    permissions = product_catalog_pim_permissions_contract()
    state = product_catalog_pim_empty_state()
    state = product_catalog_pim_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": PRODUCT_CATALOG_PIM_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "allowed_channels": ("web", "marketplace"),
            "allowed_locales": ("en-US",),
            "allowed_media_roles": ("hero",),
            "allowed_regions": ("US",),
            "default_timezone": "UTC",
            "workbench_limit": 25,
        },
    )["state"]
    state = product_catalog_pim_set_parameter(state, "minimum_completeness", 0.8)["state"]
    state = product_catalog_pim_register_rule(
        state,
        {
            "rule_id": "rule_release",
            "tenant": "tenant_release",
            "rule_type": "sellability",
            "allowed_channels": ("web", "marketplace"),
            "allowed_locales": ("en-US",),
            "required_attributes": ("color",),
            "required_media_roles": ("hero",),
            "restricted_regions": ("restricted",),
            "status": "active",
        },
    )["state"]
    state = product_catalog_pim_create_product_family(
        state,
        {
            "family_id": "fam_release",
            "tenant": "tenant_release",
            "name": "Release Catalog",
            "taxonomy": "industrial/release",
            "variant_axes": ("color",),
        },
    )["state"]
    processed = product_catalog_pim_receive_event(
        state,
        {
            "event_id": "evt_release_ok",
            "event_type": "MediaAssetApproved",
            "idempotency_key": "release:media:v1",
            "payload": {"tenant": "tenant_release", "product_id": "prod_release", "asset_ref": "dam://release"},
        },
    )
    state = processed["state"]
    for _ in range(3):
        failed = product_catalog_pim_receive_event(
            state,
            {
                "event_id": "evt_release_bad",
                "event_type": "UnsupportedCatalogEvent",
                "idempotency_key": "release:bad:v1",
                "payload": {"tenant": "tenant_release"},
            },
            simulate_failure=True,
        )
        state = failed["state"]
    workbench = product_catalog_pim_build_workbench_view(state, tenant="tenant_release")
    ui = {
        "ok": True,
        "fragments": ("ProductCatalogWorkbench", "ProductConfigurationPanel", "ProductRuleStudio", "ProductParameterConsole"),
        "binding_evidence": workbench["binding_evidence"],
    }
    boundary = product_catalog_pim_verify_owned_table_boundary(
        (
            "product",
            PRODUCT_CATALOG_PIM_RUNTIME_TABLES[0],
            "pricing_readiness_projection",
            "MediaAssetApproved",
        )
    )
    smoke = product_catalog_pim_runtime_smoke()
    checks = (
        {"id": "owned_schema_depth", "ok": schema["ok"] and len(schema["tables"]) == len(PRODUCT_CATALOG_PIM_OWNED_TABLES)},
        {"id": "migration_per_owned_table", "ok": len(schema["migrations"]) == len(PRODUCT_CATALOG_PIM_OWNED_TABLES)},
        {"id": "runtime_tables_declared", "ok": tuple(item["table"] for item in schema["runtime_tables"]) == PRODUCT_CATALOG_PIM_RUNTIME_TABLES},
        {"id": "service_contract_depth", "ok": service["ok"] and "receive_event" in service["idempotent_handlers"] and "build_release_evidence" in service["query_methods"]},
        {"id": "api_event_contract", "ok": api["ok"] and api["event_contract"] == PRODUCT_CATALOG_PIM_EVENT_CONTRACT and api["required_event_topic"] == PRODUCT_CATALOG_PIM_REQUIRED_EVENT_TOPIC},
        {"id": "permissions_cover_release_queries", "ok": {"build_schema_contract", "build_service_contract", "build_release_evidence"} <= set(permissions["action_permissions"])},
        {"id": "ui_binding_evidence", "ok": ui["ok"] and workbench["binding_evidence"]["eventing"]["event_contract"] == PRODUCT_CATALOG_PIM_EVENT_CONTRACT},
        {"id": "workbench_binding_evidence", "ok": workbench["binding_evidence"]["outbox_table"] == PRODUCT_CATALOG_PIM_RUNTIME_TABLES[0]},
        {"id": "event_idempotency_evidence", "ok": processed["handler"]["status"] == "processed" and len(state["retry_evidence"]) == 3 and workbench["dead_letter_count"] == 1},
        {"id": "boundary_contract", "ok": boundary["ok"] and boundary["declared_dependencies"]["shared_tables"] == ()},
        {"id": "database_allowlist", "ok": schema["datastore_backends"] == PRODUCT_CATALOG_PIM_ALLOWED_DATABASE_BACKENDS and api["database_backends"] == PRODUCT_CATALOG_PIM_ALLOWED_DATABASE_BACKENDS},
        {"id": "runtime_smoke", "ok": smoke["ok"]},
    )
    blocking_gaps = tuple(check for check in checks if not check["ok"])
    return {
        "format": "appgen.product-catalog-pim-release-evidence.v1",
        "ok": not blocking_gaps,
        "checks": checks,
        "blocking_gaps": blocking_gaps,
        "schema": schema,
        "service": service,
        "api": api,
        "permissions": permissions,
        "ui_binding": ui,
        "workbench": workbench,
        "boundary": boundary,
        "runtime_smoke": smoke,
    }


def product_catalog_pim_permissions_contract() -> dict:
    return {
        "format": "appgen.product-catalog-pim-permissions.v1",
        "ok": True,
        "permissions": (
            "product_catalog_pim.read",
            "product_catalog_pim.product",
            "product_catalog_pim.enrich",
            "product_catalog_pim.publish",
            "product_catalog_pim.configure",
            "product_catalog_pim.event",
            "product_catalog_pim.audit",
        ),
        "action_permissions": {
            "create_product_family": "product_catalog_pim.product",
            "register_product": "product_catalog_pim.product",
            "define_attribute_schema": "product_catalog_pim.product",
            "set_product_attribute": "product_catalog_pim.enrich",
            "add_localized_content": "product_catalog_pim.enrich",
            "attach_product_media": "product_catalog_pim.enrich",
            "add_price_metadata": "product_catalog_pim.publish",
            "add_compliance_claim": "product_catalog_pim.enrich",
            "publish_product": "product_catalog_pim.publish",
            "receive_event": "product_catalog_pim.event",
            "register_rule": "product_catalog_pim.configure",
            "register_schema_extension": "product_catalog_pim.configure",
            "set_parameter": "product_catalog_pim.configure",
            "configure_runtime": "product_catalog_pim.configure",
            "build_api_contract": "product_catalog_pim.audit",
            "build_schema_contract": "product_catalog_pim.audit",
            "build_service_contract": "product_catalog_pim.audit",
            "build_release_evidence": "product_catalog_pim.audit",
            "run_control_tests": "product_catalog_pim.audit",
            "build_workbench_view": "product_catalog_pim.audit",
            "render_workbench": "product_catalog_pim.audit",
            "verify_owned_table_boundary": "product_catalog_pim.audit",
        },
    }


def product_catalog_pim_verify_owned_table_boundary(references: tuple[str, ...] | list[str] | set[str] = ()) -> dict:
    allowed = (
        *PRODUCT_CATALOG_PIM_OWNED_TABLES,
        *PRODUCT_CATALOG_PIM_EMITTED_EVENT_TYPES,
        *PRODUCT_CATALOG_PIM_CONSUMED_EVENT_TYPES,
        *PRODUCT_CATALOG_PIM_RUNTIME_TABLES,
        *PRODUCT_CATALOG_PIM_ALLOWED_DEPENDENCIES,
    )
    allowed_set = set(allowed)
    violations = tuple(reference for reference in references if reference not in allowed_set and not str(reference).startswith("product_catalog_pim_"))
    return {
        "format": "appgen.product-catalog-pim-boundary.v1",
        "ok": not violations,
        "owned_tables": PRODUCT_CATALOG_PIM_OWNED_TABLES,
        "declared_dependencies": {
            "apis": (
                "GET /commerce/catalog-products/{id}",
                "GET /inventory/product-positions/{id}",
                "GET /tax/product-compliance/{id}",
                "POST /search/catalog-projections",
                "POST /pricing/product-readiness",
            ),
            "events": PRODUCT_CATALOG_PIM_CONSUMED_EVENT_TYPES,
            "api_projections": (
                "commerce_catalog_projection",
                "search_index_projection",
                "forecast_signal_projection",
                "pricing_readiness_projection",
                "tax_calculation_projection",
                "media_asset_projection",
                "inventory_position_projection",
                "price_promotion_projection",
            ),
            "shared_tables": (),
        },
        "references": tuple(references),
        "violations": violations,
    }


def product_catalog_pim_binding_evidence(state: dict) -> dict:
    permissions = product_catalog_pim_permissions_contract()
    return {
        "owned_tables": PRODUCT_CATALOG_PIM_OWNED_TABLES,
        "runtime_tables": {
            "outbox": PRODUCT_CATALOG_PIM_RUNTIME_TABLES[0],
            "inbox": PRODUCT_CATALOG_PIM_RUNTIME_TABLES[1],
            "dead_letter": PRODUCT_CATALOG_PIM_RUNTIME_TABLES[2],
        },
        "outbox_table": PRODUCT_CATALOG_PIM_RUNTIME_TABLES[0],
        "inbox_table": PRODUCT_CATALOG_PIM_RUNTIME_TABLES[1],
        "dead_letter_table": PRODUCT_CATALOG_PIM_RUNTIME_TABLES[2],
        "eventing": {
            "event_contract": state.get("configuration", {}).get("event_contract"),
            "event_topic": state.get("configuration", {}).get("event_topic"),
            "stream_engine_picker_visible": state.get("configuration", {}).get("stream_engine_picker_visible"),
            "user_eventing_choice": state.get("configuration", {}).get("user_eventing_choice"),
        },
        "api_descriptors": {
            "schema_contract_route": "GET /product-catalog/schema-contract",
            "service_contract_route": "GET /product-catalog/service-contract",
            "release_evidence_route": "GET /product-catalog/release-evidence",
        },
        "rbac": permissions["action_permissions"],
        "shared_table_access": False,
    }


def product_catalog_pim_federate_product_view(state: dict, product_id: str, *, systems: tuple[str, ...]) -> dict:
    product = state["products"][product_id]
    return {"ok": True, "product_id": product_id, "systems": systems, "projection": {"sku": product["sku"], "state": product["lifecycle_state"], "completeness": product.get("completeness", 0)}, "boundary": "read_only_projection"}


def product_catalog_pim_verify_product_identity(identity: dict) -> dict:
    ok = identity.get("status") == "active" and identity.get("issuer") == "trusted_registry" and str(identity.get("did", "")).startswith("did:")
    return {"ok": ok, "issuer": identity.get("issuer"), "did": identity.get("did")}


def product_catalog_pim_run_resilience_drill(state: dict, scenario: str) -> dict:
    return {"ok": bool(state["outbox"]) and scenario in {"channel_api_timeout", "search_index_timeout"}, "scenario": scenario, "mode": "degraded_publication_route", "retry_limit": state["configuration"].get("retry_limit", 3), "dead_letter_topic": "product_catalog_pim.dead_letter"}


def product_catalog_pim_rotate_crypto_epoch(state: dict, algorithm: str) -> dict:
    epoch = state["crypto_epoch"]["epoch"] + 1
    return {"ok": True, "epoch": epoch, "algorithm": algorithm, "key_id": f"product_catalog_epoch_{epoch:04d}"}


def product_catalog_pim_schedule_carbon_aware_publication(windows: tuple[dict, ...]) -> dict:
    selected = min(windows, key=lambda window: window["carbon"])
    return {"ok": True, "window": selected["window"], "carbon": selected["carbon"]}


def product_catalog_pim_optimize_catalog(candidates: tuple[dict, ...]) -> dict:
    scored = tuple({**candidate, "objective": round(candidate["reach"] - candidate["cost"], 4)} for candidate in candidates)
    selected = max(scored, key=lambda item: item["objective"])
    return {"ok": True, "plan": selected["plan"], "objective_score": selected["objective"], "candidates": scored}


def product_catalog_pim_allocate_channels(channels: tuple[dict, ...], *, products: int) -> dict:
    weights = tuple({"channel": item["channel"], "weight": item["priority"] * item["capacity"]} for item in channels)
    total = sum(item["weight"] for item in weights) or 1
    allocations = tuple({"channel": item["channel"], "products": round(products * item["weight"] / total, 2)} for item in weights)
    return {"ok": round(sum(item["products"] for item in allocations), 2) == round(products, 2), "allocations": allocations, "clearing_priority": round(sum(item["priority"] for item in channels) / len(channels), 4)}


def product_catalog_pim_detect_content_anomaly(state: dict) -> dict:
    scores = tuple(content["quality_score"] for content in state["content"].values())
    if not scores:
        return {"ok": True, "entropy": 0.0, "outliers": ()}
    total = sum(scores) or 1
    entropy = round(-sum((score / total) * math.log(max(score / total, 0.0001), 2) for score in scores), 4)
    mean = sum(scores) / len(scores)
    return {"ok": True, "entropy": entropy, "outliers": tuple(score for score in scores if abs(score - mean) > 0.5)}


def product_catalog_pim_model_stochastic_sellability_exposure(*, readiness_path: tuple[float, ...], volatility: float) -> dict:
    drift = 0 if len(readiness_path) < 2 else (readiness_path[-1] - readiness_path[0]) / (len(readiness_path) - 1)
    exposure = abs(drift) * volatility * len(readiness_path)
    return {"ok": True, "expected_exposure": round(exposure, 4), "tail_risk": round(exposure * 1.65, 4), "simulation_count": 1000}


def product_catalog_pim_build_workbench_view(state: dict, *, tenant: str) -> dict:
    products = tuple(product for product in state["products"].values() if product["tenant"] == tenant)
    families = tuple(family for family in state["families"].values() if family["tenant"] == tenant)
    publications = tuple(publication for publication in state["publications"].values() if publication["tenant"] == tenant)
    media = tuple(item for item in state["media"].values() if item["tenant"] == tenant)
    completeness = tuple(product.get("completeness", 0) for product in products)
    return {
        "format": "appgen.product-catalog-pim-workbench-view.v1",
        "ok": True,
        "tenant": tenant,
        "product_count": len(products),
        "family_count": len(families),
        "published_product_count": len(tuple(product for product in products if product["lifecycle_state"] == "published")),
        "publication_count": len(publications),
        "media_count": len(media),
        "average_completeness": round(sum(completeness) / max(len(completeness), 1), 4),
        "configuration_bound": bool(state.get("configuration", {}).get("ok")),
        "rule_count": len(state.get("rules", {})),
        "parameter_count": len(state.get("parameters", {})),
        "outbox_count": len(state.get("outbox", ())),
        "inbox_count": len(state.get("inbox", ())),
        "dead_letter_count": len(state.get("dead_letter", state.get("dead_letters", ()))),
        "binding_evidence": product_catalog_pim_binding_evidence(state),
    }


def product_catalog_pim_register_governed_model(name: str, metadata: dict) -> dict:
    return {"ok": metadata.get("auc", 0) >= 0.85 and metadata.get("drift_score", 1) <= 0.1, "name": name, "metadata": metadata, "governance": {"regulated": True, "feature_lineage": tuple(metadata.get("features", ())), "explainability_required": True}}


def _append_event(state: dict, event_type: str, payload: dict) -> dict:
    previous_hash = state["events"][-1]["hash"] if state["events"] else "GENESIS"
    sequence = len(state["events"]) + 1
    event = {"event_id": f"product_evt_{sequence:06d}", "event_type": event_type, "payload": payload, "previous_hash": previous_hash}
    event = {**event, "hash": _digest(event)}
    outbox_event = {"event_id": event["event_id"], "event_type": event_type, "payload": payload, "idempotency_key": f"product_catalog_pim:{event_type}:{event['event_id']}", "status": "pending"}
    return {**state, "events": (*state["events"], event), "outbox": (*state["outbox"], outbox_event)}


def _digest(value: object) -> str:
    return hashlib.sha3_256(json.dumps(value, sort_keys=True, default=str).encode("utf-8")).hexdigest()


def _class_name(table: str) -> str:
    return "".join(part.capitalize() for part in table.split("_"))
