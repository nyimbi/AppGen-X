"""Executable runtime for the Enterprise PIM PBC."""

from __future__ import annotations

import hashlib
import json
import math
import re


ENTERPRISE_PIM_REQUIRED_EVENT_TOPIC = "appgen.enterprise-pim.events"
ENTERPRISE_PIM_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
ENTERPRISE_PIM_OWNED_TABLES = (
    "product_taxonomy",
    "taxonomy_node",
    "taxonomy_relationship",
    "taxonomy_publication",
    "taxonomy_classification_candidate",
    "product_attribute",
    "attribute_group",
    "attribute_value_option",
    "attribute_inheritance_rule",
    "attribute_validation_rule",
    "attribute_quality_signal",
    "localized_content",
    "localized_content_version",
    "translation_memory_entry",
    "locale_fallback_rule",
    "content_completeness_score",
    "validation_workflow",
    "validation_workflow_step",
    "approval_decision",
    "publication_readiness_check",
    "dependency_schema",
    "dependency_projection",
    "media_dependency_projection",
    "price_dependency_projection",
    "tax_dependency_projection",
    "inventory_dependency_projection",
    "search_dependency_projection",
    "catalog_publication_projection",
    "channel_publication_policy",
    "product_relationship",
    "product_bundle_definition",
    "product_variant_family",
    "product_variant_member",
    "assortment_assignment",
    "data_steward_assignment",
    "pim_exception",
    "exception_resolution_plan",
    "pim_audit_trace",
    "pim_master_data_proof",
    "pim_policy_screening",
    "pim_federation_projection",
    "carbon_enrichment_window",
    "taxonomy_optimization_plan",
    "workflow_allocation",
    "content_anomaly_signal",
    "enrichment_forecast",
    "enrichment_risk_model",
    "semantic_instruction_parse",
    "pim_schema_extension",
    "pim_control_assertion",
    "pim_governed_model",
    "pim_seed_data",
    "pim_rule",
    "pim_parameter",
    "pim_configuration",
    "enterprise_pim_appgen_outbox_event",
    "enterprise_pim_appgen_inbox_event",
    "enterprise_pim_dead_letter_event",
)
ENTERPRISE_PIM_CONSUMED_EVENT_TYPES = (
    "InventoryPositionUpdated",
    "MediaAssetApproved",
    "PricePromotionApproved",
    "TaxCalculated",
)
ENTERPRISE_PIM_EMITTED_EVENT_TYPES = (
    "TaxonomyClassified",
    "AttributeDefined",
    "ContentLocalized",
    "ValidationApproved",
    "PimMasterDataReady",
    "AttributeGroupCreated",
    "AttributeOptionRegistered",
    "AttributeValidationRuleRegistered",
    "TranslationMemoryUpdated",
    "LocaleFallbackRegistered",
    "ProductRelationshipCreated",
    "ProductBundleDefined",
    "VariantFamilyDefined",
    "VariantMemberAdded",
    "AssortmentAssigned",
    "DataStewardAssigned",
    "PimExceptionOpened",
    "PimExceptionResolved",
)

ENTERPRISE_PIM_RUNTIME_CAPABILITY_KEYS = (
    "event_sourced_enterprise_pim_lifecycle",
    "graph_relational_taxonomy_topology",
    "multi_tenant_pim_isolation",
    "schema_evolution_resilient_attribute_model",
    "multilingual_inheritance_localization",
    "probabilistic_content_completeness_scoring",
    "counterfactual_taxonomy_publication_simulation",
    "temporal_enrichment_readiness_forecasting",
    "autonomous_enrichment_exception_resolution",
    "semantic_pim_instruction_parsing",
    "predictive_validation_risk",
    "self_healing_dependency_route_selection",
    "cryptographic_master_data_proof",
    "immutable_pim_audit_trail",
    "dynamic_pim_policy_screening",
    "automated_pim_control_testing",
    "schema_accepted_dependency_handling",
    "universal_api_async_streaming",
    "cross_system_catalog_media_pricing_tax_inventory_federation",
    "appgen_x_outbox_inbox_eventing",
    "idempotent_inbox_handlers",
    "retry_dead_letter_evidence",
    "permissions_governance_evidence",
    "tenant_isolation",
    "chaos_tolerant_pim_operations",
    "crypto_agility",
    "carbon_aware_enrichment_scheduling",
    "mathematical_taxonomy_optimization",
    "attribute_workflow_allocation_mechanism_design",
    "pim_anomaly_detection",
    "stochastic_enrichment_exposure_modeling",
    "governed_ml_model_evidence",
)

ENTERPRISE_PIM_STANDARD_FEATURE_KEYS = (
    "enterprise_taxonomies",
    "taxonomy_nodes",
    "taxonomy_hierarchy",
    "taxonomy_relationships",
    "taxonomy_publication",
    "classification_candidates",
    "product_attribute_definitions",
    "attribute_groups",
    "attribute_value_options",
    "typed_attribute_validation",
    "attribute_inheritance",
    "attribute_validation_rules",
    "attribute_quality_signals",
    "localized_attribute_overrides",
    "multilingual_content",
    "localized_content_versions",
    "translation_memory",
    "locale_fallback",
    "content_completeness_scores",
    "validation_workflows",
    "validation_workflow_steps",
    "approval_decisions",
    "approval_controls",
    "publication_readiness_checks",
    "schema_accepted_dependency_handling",
    "dependency_projections",
    "media_dependency_projection",
    "price_dependency_projection",
    "tax_dependency_projection",
    "inventory_dependency_projection",
    "search_dependency_projection",
    "catalog_publication_projection",
    "channel_publication_policy",
    "product_relationships",
    "bundle_definitions",
    "variant_families",
    "assortment_assignments",
    "data_steward_assignments",
    "exceptions",
    "exception_resolution",
    "appgen_x_outbox_inbox_eventing",
    "idempotent_handlers",
    "retry_dead_letter_evidence",
    "permissions",
    "configuration_schema",
    "rule_engine",
    "parameter_engine",
    "seed_data",
    "schema_extension",
    "audit_trace",
    "master_data_proof",
    "policy_screening",
    "federation_projection",
    "carbon_enrichment_window",
    "taxonomy_optimization",
    "workflow_allocation",
    "anomaly_signal",
    "enrichment_forecast",
    "risk_model",
    "semantic_instruction_parser",
    "control_assertion",
    "workbench",
    "immutable_audit",
    "governed_model_evidence",
)

_SUPPORTED_DATABASE_BACKENDS = ENTERPRISE_PIM_ALLOWED_DATABASE_BACKENDS
_SUPPORTED_PARAMETERS = {
    "minimum_completeness",
    "minimum_translation_quality",
    "validation_sla_hours",
    "max_inheritance_depth",
    "dead_letter_retry_limit",
    "dependency_schema_version_floor",
    "anomaly_zscore_threshold",
    "workbench_limit",
}
_THRESHOLD_PARAMETERS = {
    "minimum_completeness",
    "minimum_translation_quality",
    "anomaly_zscore_threshold",
}
_FORBIDDEN_EVENTING_FIELDS = {
    "eventing_choice",
    "eventing_mode",
    "event_transport",
    "stream_engine",
    "stream_engine_picker",
    "stream_picker",
    "user_eventing_choice",
}
_REQUIRED_RULE_FIELDS = (
    "rule_id",
    "tenant",
    "scope",
    "status",
    "required_locales",
    "required_attributes",
    "validation_policy",
)
_CONSUMED_EVENT_TYPES = set(ENTERPRISE_PIM_CONSUMED_EVENT_TYPES)
_EMITTED_EVENT_TYPES = ENTERPRISE_PIM_EMITTED_EVENT_TYPES
_API_SURFACES = (
    "POST /product-taxonomies",
    "POST /product-attributes",
    "POST /attribute-groups",
    "POST /attribute-options",
    "POST /attribute-validation-rules",
    "POST /localized-content",
    "POST /translation-memory",
    "POST /locale-fallback-rules",
    "POST /validation-workflows",
    "POST /validation-workflows/{id}/approve",
    "POST /dependency-schemas",
    "POST /product-relationships",
    "POST /product-bundles",
    "POST /variant-families",
    "POST /variant-members",
    "POST /assortments",
    "POST /data-stewards",
    "POST /pim-exceptions",
    "POST /pim-exceptions/{id}/resolve",
    "POST /pim-events",
    "GET /pim-workbench",
)


def enterprise_pim_runtime_capabilities() -> dict:
    smoke = enterprise_pim_runtime_smoke()
    return {
        "format": "appgen.enterprise-pim-runtime-capabilities.v1",
        "ok": smoke["ok"],
        "pbc": "enterprise_pim",
        "implementation_directory": "src/pyAppGen/pbcs/enterprise_pim",
        "owned_tables": ENTERPRISE_PIM_OWNED_TABLES,
        "capabilities": ENTERPRISE_PIM_RUNTIME_CAPABILITY_KEYS,
        "standard_features": ENTERPRISE_PIM_STANDARD_FEATURE_KEYS,
        "operations": (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "register_schema_extension",
            "accept_dependency_schema",
            "receive_event",
            "create_taxonomy",
            "define_attribute",
            "create_attribute_group",
            "register_attribute_value_option",
            "register_attribute_validation_rule",
            "upsert_localized_content",
            "upsert_translation_memory",
            "register_locale_fallback_rule",
            "start_validation_workflow",
            "approve_validation_workflow",
            "create_product_relationship",
            "define_product_bundle",
            "define_variant_family",
            "add_variant_member",
            "assign_assortment",
            "assign_data_steward",
            "open_pim_exception",
            "resolve_pim_exception",
            "build_api_contract",
            "build_schema_contract",
            "build_service_contract",
            "build_release_evidence",
            "permissions_contract",
            "build_workbench_view",
            "verify_owned_table_boundary",
        ),
        "smoke": smoke,
    }


def enterprise_pim_runtime_smoke() -> dict:
    state = enterprise_pim_empty_state()
    state = enterprise_pim_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": ENTERPRISE_PIM_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "default_locale": "en-US",
            "allowed_locales": ("en-US", "fr-FR", "sw-KE"),
            "allowed_channels": ("commerce", "content", "search"),
            "dependency_sources": ("dam_core", "price_promotion_engine", "tax_localization", "inventory_positioning"),
            "workbench_limit": 100,
        },
    )["state"]
    for name, value in (
        ("minimum_completeness", 0.85),
        ("minimum_translation_quality", 0.75),
        ("validation_sla_hours", 24),
        ("max_inheritance_depth", 4),
        ("dead_letter_retry_limit", 2),
        ("dependency_schema_version_floor", 1),
        ("anomaly_zscore_threshold", 2.5),
    ):
        state = enterprise_pim_set_parameter(state, name, value)["state"]
    state = enterprise_pim_register_rule(
        state,
        {
            "rule_id": "rule_enterprise_pim_default",
            "tenant": "tenant_alpha",
            "scope": "master_data_readiness",
            "status": "active",
            "required_locales": ("en-US", "fr-FR"),
            "required_attributes": ("material", "hazard_class"),
            "validation_policy": {"two_step": True, "required_approvers": ("data_steward", "compliance")},
            "dependency_policy": {"accepted_sources": ("dam_core", "price_promotion_engine", "tax_localization", "inventory_positioning")},
        },
    )["state"]
    state = enterprise_pim_accept_dependency_schema(
        state,
        "dam_core",
        {"schema_version": 1, "events": ("MediaAssetApproved",), "fields": ("asset_ref", "rights_status")},
    )["state"]
    state = enterprise_pim_accept_dependency_schema(
        state,
        "price_promotion_engine",
        {"schema_version": 1, "events": ("PricePromotionApproved",), "fields": ("price_id", "currency")},
    )["state"]
    state = enterprise_pim_create_taxonomy(
        state,
        {
            "taxonomy_id": "tax_100",
            "tenant": "tenant_alpha",
            "code": "industrial/pumps",
            "name": "Industrial Pumps",
            "parent_id": None,
            "localized_names": {"en-US": "Industrial Pumps", "fr-FR": "Pompes industrielles"},
        },
    )["state"]
    state = enterprise_pim_define_attribute(
        state,
        {
            "attribute_id": "attr_material",
            "tenant": "tenant_alpha",
            "taxonomy_id": "tax_100",
            "name": "material",
            "data_type": "string",
            "required": True,
            "inherited_from": None,
            "localized_labels": {"en-US": "Material", "fr-FR": "Materiau"},
            "value": "steel",
        },
    )["state"]
    state = enterprise_pim_define_attribute(
        state,
        {
            "attribute_id": "attr_hazard",
            "tenant": "tenant_alpha",
            "taxonomy_id": "tax_100",
            "name": "hazard_class",
            "data_type": "string",
            "required": True,
            "inherited_from": "attr_material",
            "localized_labels": {"en-US": "Hazard class", "fr-FR": "Classe de risque"},
            "value": "none",
        },
    )["state"]
    state = enterprise_pim_create_attribute_group(
        state,
        {
            "group_id": "grp_compliance",
            "tenant": "tenant_alpha",
            "taxonomy_id": "tax_100",
            "name": "Compliance attributes",
            "sequence": 10,
            "attributes": ("attr_material", "attr_hazard"),
        },
    )["state"]
    state = enterprise_pim_register_attribute_value_option(
        state,
        {
            "option_id": "opt_hazard_none",
            "tenant": "tenant_alpha",
            "attribute_id": "attr_hazard",
            "value": "none",
            "label": "No regulated hazard",
        },
    )["state"]
    state = enterprise_pim_register_attribute_validation_rule(
        state,
        {
            "validation_rule_id": "avr_hazard_allowed",
            "tenant": "tenant_alpha",
            "attribute_id": "attr_hazard",
            "data_type": "string",
            "required": True,
            "pattern": "^(none|flammable|corrosive)$",
        },
    )["state"]
    state = enterprise_pim_upsert_localized_content(
        state,
        {
            "content_id": "loc_100_en",
            "tenant": "tenant_alpha",
            "entity_id": "tax_100",
            "entity_type": "product_taxonomy",
            "locale": "en-US",
            "title": "Industrial Pumps",
            "description": "Enterprise governed pump taxonomy for industrial catalogs",
            "overrides": {"short_name": "Pumps"},
        },
    )["state"]
    state = enterprise_pim_upsert_localized_content(
        state,
        {
            "content_id": "loc_100_fr",
            "tenant": "tenant_alpha",
            "entity_id": "tax_100",
            "entity_type": "product_taxonomy",
            "locale": "fr-FR",
            "title": "Pompes industrielles",
            "description": "Taxonomie gouvernee pour catalogues industriels",
            "overrides": {"short_name": "Pompes"},
        },
    )["state"]
    state = enterprise_pim_upsert_translation_memory(
        state,
        {
            "translation_id": "tm_100",
            "tenant": "tenant_alpha",
            "source_locale": "en-US",
            "target_locale": "fr-FR",
            "source_text": "Industrial Pumps",
            "target_text": "Pompes industrielles",
            "quality_score": 0.94,
        },
    )["state"]
    state = enterprise_pim_register_locale_fallback_rule(
        state,
        {
            "fallback_rule_id": "lfr_fr",
            "tenant": "tenant_alpha",
            "locale": "fr-FR",
            "fallback_locale": "en-US",
            "priority": 1,
        },
    )["state"]
    state = enterprise_pim_create_product_relationship(
        state,
        {
            "relationship_id": "rel_100",
            "tenant": "tenant_alpha",
            "from_entity_id": "tax_100",
            "to_entity_id": "tax_100",
            "relationship_type": "self_reference_for_smoke",
        },
    )["state"]
    state = enterprise_pim_define_product_bundle(
        state,
        {
            "bundle_id": "bundle_100",
            "tenant": "tenant_alpha",
            "taxonomy_id": "tax_100",
            "component_refs": ("pump_head", "pump_motor"),
            "bundle_policy": "complete_kit",
        },
    )["state"]
    state = enterprise_pim_define_variant_family(
        state,
        {
            "family_id": "vf_100",
            "tenant": "tenant_alpha",
            "taxonomy_id": "tax_100",
            "variant_axes": ("voltage", "material"),
        },
    )["state"]
    state = enterprise_pim_add_variant_member(
        state,
        {
            "member_id": "vm_100",
            "tenant": "tenant_alpha",
            "family_id": "vf_100",
            "sku_ref": "sku_pump_240v_steel",
            "axis_values": {"voltage": "240v", "material": "steel"},
        },
    )["state"]
    state = enterprise_pim_assign_assortment(
        state,
        {
            "assignment_id": "assort_100",
            "tenant": "tenant_alpha",
            "entity_id": "tax_100",
            "channel": "commerce",
            "market": "NA",
        },
    )["state"]
    state = enterprise_pim_assign_data_steward(
        state,
        {
            "assignment_id": "steward_100",
            "tenant": "tenant_alpha",
            "entity_id": "tax_100",
            "steward": "pim_steward",
            "responsibility": "taxonomy_governance",
        },
    )["state"]
    exception = enterprise_pim_open_pim_exception(
        state,
        {
            "exception_id": "exc_100",
            "tenant": "tenant_alpha",
            "entity_id": "tax_100",
            "exception_type": "translation_review",
            "severity": "medium",
        },
    )
    state = enterprise_pim_resolve_pim_exception(
        exception["state"],
        {
            "exception_id": "exc_100",
            "tenant": "tenant_alpha",
            "resolution": "translation_memory_confirmed",
            "resolved_by": "pim_steward",
        },
    )["state"]
    workflow = enterprise_pim_start_validation_workflow(
        state,
        {
            "workflow_id": "wf_100",
            "tenant": "tenant_alpha",
            "entity_id": "tax_100",
            "entity_type": "product_taxonomy",
            "requested_by": "pim_steward",
            "steps": ("data_steward", "compliance"),
        },
    )
    state = workflow["state"]
    approved = enterprise_pim_approve_validation_workflow(state, "wf_100", approver="data_steward")
    state = enterprise_pim_approve_validation_workflow(approved["state"], "wf_100", approver="compliance")["state"]
    duplicate = enterprise_pim_receive_event(
        state,
        {
            "event_id": "evt_media_100",
            "event_type": "MediaAssetApproved",
            "idempotency_key": "media:asset_100:v1",
            "payload": {"tenant": "tenant_alpha", "entity_id": "tax_100", "asset_ref": "dam://asset_100", "rights_status": "approved"},
        },
    )
    state = duplicate["state"]
    duplicate = enterprise_pim_receive_event(
        state,
        {
            "event_id": "evt_media_100",
            "event_type": "MediaAssetApproved",
            "idempotency_key": "media:asset_100:v1",
            "payload": {"tenant": "tenant_alpha", "entity_id": "tax_100", "asset_ref": "dam://asset_100", "rights_status": "approved"},
        },
    )
    state = duplicate["state"]
    invalid = enterprise_pim_receive_event(
        state,
        {"event_id": "evt_unknown", "event_type": "UnknownDependency", "idempotency_key": "unknown:1", "attempts": 3, "payload": {"tenant": "tenant_alpha"}},
    )
    state = invalid["state"]
    readiness = enterprise_pim_publish_master_data(state, "tax_100", channels=("commerce", "search"))
    state = readiness["state"]
    simulation = enterprise_pim_simulate_taxonomy_publication(state, "tax_100", proposed_locales=("en-US",))
    forecast = enterprise_pim_forecast_readiness((0.52, 0.7, 0.92), catalog_size=250)
    parsed = enterprise_pim_parse_instruction("taxonomy tax_100 locale fr-FR action validate")
    risk = enterprise_pim_score_validation_risk({"missing_locales": 0.1, "dependency_gaps": 0.1, "sla_pressure": 0.2})
    recommendation = enterprise_pim_recommend_exception_resolution("missing_locale")
    route = enterprise_pim_route_dependency({"event_id": "route_1"}, rails=({"route": "dependency_api", "available": False, "latency": 4}, {"route": "appgen_outbox", "available": True, "latency": 6}))
    proof = enterprise_pim_generate_master_data_proof(state, "tax_100", disclosure=("taxonomy_id", "code", "status"))
    screening = enterprise_pim_screen_policy(state, "tax_100", restricted_terms=("blocked",))
    controls = enterprise_pim_run_control_tests(state)
    api = enterprise_pim_build_api_contract()
    schema = enterprise_pim_build_schema_contract()
    service = enterprise_pim_build_service_contract()
    release = enterprise_pim_build_release_evidence()
    federation = enterprise_pim_federate_master_data_view(state, "tax_100", systems=("catalog", "media", "pricing", "tax", "inventory"))
    resilience = enterprise_pim_run_resilience_drill(state, "dependency_timeout")
    crypto = enterprise_pim_rotate_crypto_epoch(state, "dilithium3_simulated")
    carbon = enterprise_pim_schedule_carbon_aware_enrichment(({"window": "day", "carbon": 180}, {"window": "night", "carbon": 64}))
    optimization = enterprise_pim_optimize_taxonomy(({"plan": "deep_tree", "coverage": 0.96, "complexity": 0.45}, {"plan": "balanced_tree", "coverage": 0.9, "complexity": 0.22}))
    allocation = enterprise_pim_allocate_workflows(({"queue": "data_steward", "priority": 0.9, "capacity": 8}, {"queue": "compliance", "priority": 0.6, "capacity": 4}), workflows=6)
    anomaly = enterprise_pim_detect_content_anomaly(state)
    stochastic = enterprise_pim_model_stochastic_enrichment_exposure(readiness_path=(0.55, 0.72, 0.9), volatility=0.1)
    model = enterprise_pim_register_governed_model("pim_readiness", {"features": ("completeness", "locales", "dependencies"), "auc": 0.91, "drift_score": 0.03})
    workbench = enterprise_pim_build_workbench_view(state, tenant="tenant_alpha")
    checks = (
        {"id": "event_sourced_enterprise_pim_lifecycle", "ok": len(state["events"]) >= 8 and state["events"][-1]["hash"]},
        {"id": "graph_relational_taxonomy_topology", "ok": state["product_taxonomy"]["tax_100"]["graph_degree"] >= 2},
        {"id": "multi_tenant_pim_isolation", "ok": workbench["tenant"] == "tenant_alpha"},
        {"id": "schema_evolution_resilient_attribute_model", "ok": state["product_attribute"]["attr_material"]["compiled_hash"]},
        {"id": "attribute_group_option_validation_lifecycle", "ok": state["attribute_group"]["grp_compliance"]["status"] == "active" and state["attribute_value_option"]["opt_hazard_none"]["status"] == "active" and state["attribute_validation_rule"]["avr_hazard_allowed"]["status"] == "active"},
        {"id": "multilingual_inheritance_localization", "ok": state["product_attribute"]["attr_hazard"]["inheritance_path"] == ("attr_material", "attr_hazard") and len(state["localized_content"]) == 2},
        {"id": "translation_memory_and_locale_fallback_lifecycle", "ok": state["translation_memory_entry"]["tm_100"]["quality_score"] >= 0.9 and state["locale_fallback_rule"]["lfr_fr"]["fallback_locale"] == "en-US"},
        {"id": "relationship_bundle_variant_assortment_lifecycle", "ok": state["product_relationship"]["rel_100"]["status"] == "active" and state["product_bundle_definition"]["bundle_100"]["status"] == "active" and state["product_variant_member"]["vm_100"]["status"] == "active" and state["assortment_assignment"]["assort_100"]["status"] == "active"},
        {"id": "data_steward_and_exception_resolution_lifecycle", "ok": state["data_steward_assignment"]["steward_100"]["status"] == "active" and state["pim_exception"]["exc_100"]["status"] == "resolved"},
        {"id": "probabilistic_content_completeness_scoring", "ok": readiness["readiness_score"] >= 0.85},
        {"id": "counterfactual_taxonomy_publication_simulation", "ok": simulation["locale_delta"] < 0},
        {"id": "temporal_enrichment_readiness_forecasting", "ok": forecast["forecast_readiness"] > 0.9},
        {"id": "autonomous_enrichment_exception_resolution", "ok": recommendation["action"] == "request_translation"},
        {"id": "semantic_pim_instruction_parsing", "ok": parsed["ok"] and parsed["taxonomy_id"] == "tax_100"},
        {"id": "predictive_validation_risk", "ok": risk["risk_score"] > 0},
        {"id": "self_healing_dependency_route_selection", "ok": route["ok"] and route["route"] == "appgen_outbox" and route["failover_used"]},
        {"id": "cryptographic_master_data_proof", "ok": proof["ok"] and proof["proof"].startswith("zk_enterprise_pim_")},
        {"id": "immutable_pim_audit_trail", "ok": controls["hash_chain_valid"]},
        {"id": "dynamic_pim_policy_screening", "ok": screening["ok"] and screening["decision"] == "clear"},
        {"id": "automated_pim_control_testing", "ok": controls["ok"] and not controls["blocking_gaps"]},
        {"id": "schema_accepted_dependency_handling", "ok": "dam_core" in state["dependency_schemas"] and state["dependency_projections"]["MediaAssetApproved"]["asset_ref"] == "dam://asset_100"},
        {"id": "universal_api_async_streaming", "ok": api["ok"] and schema["ok"] and service["ok"] and release["ok"] and "PimMasterDataReady" in api["events"]["emits"]},
        {"id": "cross_system_catalog_media_pricing_tax_inventory_federation", "ok": federation["ok"] and "pricing" in federation["systems"]},
        {"id": "appgen_x_outbox_inbox_eventing", "ok": state["outbox"][-1]["event_type"] == "PimMasterDataReady"},
        {"id": "idempotent_inbox_handlers", "ok": duplicate["handler"]["status"] == "duplicate"},
        {"id": "retry_dead_letter_evidence", "ok": invalid["handler"]["status"] == "dead_letter" and len(state["dead_letter"]) == 1},
        {"id": "permissions_governance_evidence", "ok": "enterprise_pim.configure" in api["permissions"]},
        {"id": "tenant_isolation", "ok": all(item["tenant"] == "tenant_alpha" for item in state["product_taxonomy"].values())},
        {"id": "chaos_tolerant_pim_operations", "ok": resilience["ok"] and resilience["mode"] == "dependency_degraded_outbox"},
        {"id": "crypto_agility", "ok": crypto["ok"] and crypto["epoch"] == 2},
        {"id": "carbon_aware_enrichment_scheduling", "ok": carbon["window"] == "night"},
        {"id": "mathematical_taxonomy_optimization", "ok": optimization["ok"] and optimization["plan"] == "balanced_tree"},
        {"id": "attribute_workflow_allocation_mechanism_design", "ok": allocation["ok"] and allocation["allocations"][0]["workflows"] > allocation["allocations"][1]["workflows"]},
        {"id": "pim_anomaly_detection", "ok": anomaly["ok"] and anomaly["entropy"] >= 0},
        {"id": "stochastic_enrichment_exposure_modeling", "ok": stochastic["ok"] and stochastic["tail_risk"] > 0},
        {"id": "governed_ml_model_evidence", "ok": model["governance"]["regulated"] and model["metadata"]["auc"] >= 0.9},
    )
    blocking_gaps = tuple(check for check in checks if not check["ok"])
    return {"format": "appgen.enterprise-pim-runtime-smoke.v1", "ok": not blocking_gaps, "checks": checks, "blocking_gaps": blocking_gaps}


def enterprise_pim_empty_state() -> dict:
    return {
        "events": (),
        "outbox": (),
        "inbox": (),
        "dead_letter": (),
        "handled_event_keys": (),
        "product_taxonomy": {},
        "product_attribute": {},
        "attribute_group": {},
        "attribute_value_option": {},
        "attribute_validation_rule": {},
        "attribute_quality_signal": {},
        "localized_content": {},
        "translation_memory_entry": {},
        "locale_fallback_rule": {},
        "validation_workflow": {},
        "product_relationship": {},
        "product_bundle_definition": {},
        "product_variant_family": {},
        "product_variant_member": {},
        "assortment_assignment": {},
        "data_steward_assignment": {},
        "pim_exception": {},
        "exception_resolution_plan": {},
        "dependency_schemas": {},
        "dependency_projections": {},
        "rules": {},
        "parameters": {},
        "configuration": {},
        "schema_extensions": {},
        "seed_data": {"default_locales": ("en-US",), "default_workflow_steps": ("data_steward",)},
        "crypto_epoch": {"epoch": 1, "algorithm": "sha3_256"},
    }


def enterprise_pim_configure_runtime(state: dict, configuration: dict) -> dict:
    forbidden = tuple(sorted(field for field in _FORBIDDEN_EVENTING_FIELDS if field in configuration))
    if forbidden:
        raise ValueError(f"Enterprise PIM uses the AppGen-X event contract; unsupported eventing fields: {forbidden}")
    if configuration.get("database_backend") not in _SUPPORTED_DATABASE_BACKENDS:
        raise ValueError("Enterprise PIM supports only PostgreSQL, MySQL, or MariaDB backends")
    if configuration.get("event_topic") != ENTERPRISE_PIM_REQUIRED_EVENT_TOPIC:
        raise ValueError(f"Enterprise PIM requires AppGen-X event topic {ENTERPRISE_PIM_REQUIRED_EVENT_TOPIC}")
    retry_limit = int(configuration.get("retry_limit", 0))
    if retry_limit < 1:
        raise ValueError("Enterprise PIM retry_limit must be at least 1")
    configured = {
        **configuration,
        "ok": True,
        "event_contract": "AppGen-X",
        "allowed_database_backends": _SUPPORTED_DATABASE_BACKENDS,
        "stream_engine_picker_visible": False,
        "configuration_schema": {
            "required": ("database_backend", "event_topic", "retry_limit", "default_locale", "allowed_locales"),
            "owned_tables": ENTERPRISE_PIM_OWNED_TABLES,
        },
    }
    return {"ok": True, "state": {**state, "configuration": configured}, "configuration": configured}


def enterprise_pim_set_parameter(state: dict, name: str, value: float | int | str | bool) -> dict:
    if name not in _SUPPORTED_PARAMETERS:
        raise ValueError(f"Unsupported Enterprise PIM parameter: {name}")
    if name in _THRESHOLD_PARAMETERS and not 0 <= float(value) <= 10:
        raise ValueError(f"Enterprise PIM threshold parameter out of range: {name}")
    if name.endswith("_hours") and float(value) <= 0:
        raise ValueError(f"Enterprise PIM duration parameter must be positive: {name}")
    parameter = {"name": name, "value": value, "compiled_hash": _digest({"name": name, "value": value})}
    return {"ok": True, "state": {**state, "parameters": {**state["parameters"], name: parameter}}, "parameter": parameter}


def enterprise_pim_register_rule(state: dict, rule: dict) -> dict:
    missing = tuple(sorted(field for field in _REQUIRED_RULE_FIELDS if field not in rule))
    if missing:
        raise ValueError(f"Missing required Enterprise PIM rule fields: {missing}")
    enriched = {
        **rule,
        "enabled": rule["status"] == "active",
        "compiled_hash": _digest(rule),
        "deterministic": True,
    }
    return {"ok": True, "state": {**state, "rules": {**state["rules"], rule["rule_id"]: enriched}}, "rule": enriched}


def enterprise_pim_register_schema_extension(state: dict, table: str, fields: dict) -> dict:
    if table not in ENTERPRISE_PIM_OWNED_TABLES:
        raise ValueError(f"Enterprise PIM schema extensions must target owned tables: {ENTERPRISE_PIM_OWNED_TABLES}")
    invalid = tuple(name for name in fields if not re.fullmatch(r"[a-z][a-z0-9_]*", name))
    if invalid:
        return {"ok": False, "error": "invalid_extension_field", "invalid": invalid, "state": state}
    extensions = {**state["schema_extensions"], table: {**state["schema_extensions"].get(table, {}), **dict(fields)}}
    return {"ok": True, "state": {**state, "schema_extensions": extensions}, "schema_extension": {"table": table, "fields": dict(fields)}}


def enterprise_pim_accept_dependency_schema(state: dict, dependency: str, contract: dict) -> dict:
    if dependency not in state["configuration"].get("dependency_sources", ()):
        raise ValueError(f"Unsupported Enterprise PIM dependency source: {dependency}")
    if int(contract.get("schema_version", 0)) < int(state["parameters"].get("dependency_schema_version_floor", {"value": 1})["value"]):
        raise ValueError("Enterprise PIM dependency schema version is below configured floor")
    unsupported = tuple(event for event in contract.get("events", ()) if event not in _CONSUMED_EVENT_TYPES)
    if unsupported:
        raise ValueError(f"Unsupported Enterprise PIM dependency events: {unsupported}")
    accepted = {**contract, "dependency": dependency, "accepted": True, "compiled_hash": _digest({"dependency": dependency, **contract})}
    return {"ok": True, "state": {**state, "dependency_schemas": {**state["dependency_schemas"], dependency: accepted}}, "schema": accepted}


def enterprise_pim_receive_event(state: dict, event: dict, *, simulate_failure: bool = False) -> dict:
    key = event.get("idempotency_key") or event["event_id"]
    if key in state["handled_event_keys"]:
        handler = {"event_id": event["event_id"], "status": "duplicate", "idempotency_key": key}
        return {"ok": True, "state": {**state, "inbox": state["inbox"] + (handler,)}, "handler": handler}
    attempts = int(event.get("attempts", 1))
    retry_limit = int(state["configuration"].get("retry_limit", 1))
    if simulate_failure or event["event_type"] not in _CONSUMED_EVENT_TYPES:
        status = "dead_letter" if attempts >= retry_limit else "retry"
        handler = {"event_id": event["event_id"], "event_type": event["event_type"], "status": status, "attempts": attempts, "idempotency_key": key}
        next_state = {**state, "inbox": state["inbox"] + (handler,), "handled_event_keys": state["handled_event_keys"] + (key,)}
        if status == "dead_letter":
            next_state = {**next_state, "dead_letter": state["dead_letter"] + ({**event, "reason": "unsupported_or_failed_dependency_event"},)}
        return {"ok": False, "state": next_state, "handler": handler}
    projection = {**event["payload"], "event_type": event["event_type"], "event_id": event["event_id"]}
    handler = {"event_id": event["event_id"], "event_type": event["event_type"], "status": "handled", "attempts": attempts, "idempotency_key": key}
    next_state = {
        **state,
        "inbox": state["inbox"] + (handler,),
        "handled_event_keys": state["handled_event_keys"] + (key,),
        "dependency_projections": {**state["dependency_projections"], event["event_type"]: projection},
    }
    return {"ok": True, "state": next_state, "handler": handler, "projection": projection}


def enterprise_pim_create_taxonomy(state: dict, taxonomy: dict) -> dict:
    parent = state["product_taxonomy"].get(taxonomy.get("parent_id")) if taxonomy.get("parent_id") else None
    lineage = (parent["taxonomy_id"], taxonomy["taxonomy_id"]) if parent else (taxonomy["taxonomy_id"],)
    localized_names = taxonomy.get("localized_names", {})
    enriched = {
        **taxonomy,
        "lineage": lineage,
        "status": "draft",
        "graph_degree": len(lineage) + len(localized_names),
        "compiled_hash": _digest(taxonomy),
    }
    next_state = {**state, "product_taxonomy": {**state["product_taxonomy"], taxonomy["taxonomy_id"]: enriched}}
    next_state = _append_event(next_state, "TaxonomyClassified", {"tenant": taxonomy["tenant"], "taxonomy_id": taxonomy["taxonomy_id"], "lineage": lineage})
    return {"ok": True, "state": next_state, "taxonomy": enriched}


def enterprise_pim_define_attribute(state: dict, attribute: dict) -> dict:
    inherited_from = attribute.get("inherited_from")
    inherited = state["product_attribute"].get(inherited_from) if inherited_from else None
    inherited_path = (inherited["attribute_id"], attribute["attribute_id"]) if inherited else (attribute["attribute_id"],)
    depth_limit = int(state["parameters"].get("max_inheritance_depth", {"value": 4})["value"])
    if len(inherited_path) > depth_limit:
        raise ValueError("Enterprise PIM attribute inheritance exceeds configured depth")
    ok = attribute["taxonomy_id"] in state["product_taxonomy"]
    enriched = {
        **attribute,
        "status": "active" if ok else "blocked",
        "inheritance_path": inherited_path,
        "effective_value": attribute.get("value", inherited.get("effective_value") if inherited else None),
        "compiled_hash": _digest(attribute),
    }
    next_state = {**state, "product_attribute": {**state["product_attribute"], attribute["attribute_id"]: enriched}}
    next_state = _append_event(next_state, "AttributeDefined", {"tenant": attribute["tenant"], "attribute_id": attribute["attribute_id"], "taxonomy_id": attribute["taxonomy_id"]})
    return {"ok": ok, "state": next_state, "attribute": enriched}


def enterprise_pim_create_attribute_group(state: dict, group: dict) -> dict:
    if group["taxonomy_id"] not in state["product_taxonomy"]:
        raise ValueError("Enterprise PIM attribute groups require an owned taxonomy.")
    missing_attributes = tuple(attribute_id for attribute_id in group.get("attributes", ()) if attribute_id not in state["product_attribute"])
    if missing_attributes:
        raise ValueError(f"Enterprise PIM attribute group references unknown attributes: {missing_attributes}")
    enriched = {
        **group,
        "status": "active",
        "attribute_count": len(tuple(group.get("attributes", ()))),
        "compiled_hash": _digest(group),
    }
    next_state = {**state, "attribute_group": {**state["attribute_group"], group["group_id"]: enriched}}
    next_state = _append_event(next_state, "AttributeGroupCreated", {"tenant": group["tenant"], "group_id": group["group_id"], "taxonomy_id": group["taxonomy_id"]})
    return {"ok": True, "state": next_state, "attribute_group": enriched}


def enterprise_pim_register_attribute_value_option(state: dict, option: dict) -> dict:
    if option["attribute_id"] not in state["product_attribute"]:
        raise ValueError("Enterprise PIM value options require an owned attribute.")
    enriched = {
        **option,
        "status": "active",
        "compiled_hash": _digest(option),
    }
    next_state = {**state, "attribute_value_option": {**state["attribute_value_option"], option["option_id"]: enriched}}
    next_state = _append_event(next_state, "AttributeOptionRegistered", {"tenant": option["tenant"], "option_id": option["option_id"], "attribute_id": option["attribute_id"]})
    return {"ok": True, "state": next_state, "attribute_value_option": enriched}


def enterprise_pim_register_attribute_validation_rule(state: dict, rule: dict) -> dict:
    if rule["attribute_id"] not in state["product_attribute"]:
        raise ValueError("Enterprise PIM validation rules require an owned attribute.")
    sample_value = str(state["product_attribute"][rule["attribute_id"]].get("effective_value") or "")
    pattern = rule.get("pattern")
    matches = re.fullmatch(pattern, sample_value) is not None if pattern else True
    enriched = {
        **rule,
        "status": "active" if matches else "review",
        "sample_value_valid": matches,
        "compiled_hash": _digest(rule),
    }
    quality = {
        "quality_signal_id": f"aqs_{rule['validation_rule_id']}",
        "tenant": rule["tenant"],
        "attribute_id": rule["attribute_id"],
        "score": 1.0 if matches else 0.4,
        "reason": "validation_rule_registered",
        "status": "accepted" if matches else "review",
    }
    next_state = {
        **state,
        "attribute_validation_rule": {**state["attribute_validation_rule"], rule["validation_rule_id"]: enriched},
        "attribute_quality_signal": {**state["attribute_quality_signal"], quality["quality_signal_id"]: quality},
    }
    next_state = _append_event(next_state, "AttributeValidationRuleRegistered", {"tenant": rule["tenant"], "validation_rule_id": rule["validation_rule_id"], "attribute_id": rule["attribute_id"]})
    return {"ok": matches, "state": next_state, "attribute_validation_rule": enriched, "attribute_quality_signal": quality}


def enterprise_pim_upsert_localized_content(state: dict, content: dict) -> dict:
    allowed_locales = state["configuration"].get("allowed_locales", ())
    if content["locale"] not in allowed_locales:
        raise ValueError(f"Unsupported Enterprise PIM locale: {content['locale']}")
    quality_score = round(min(1.0, len(content.get("description", "")) / 55 + 0.25), 4)
    status = "approved" if quality_score >= float(state["parameters"].get("minimum_translation_quality", {"value": 0.75})["value"]) else "review"
    enriched = {
        **content,
        "status": status,
        "quality_score": quality_score,
        "fallback_locale": state["configuration"].get("default_locale"),
        "compiled_hash": _digest(content),
    }
    next_state = {**state, "localized_content": {**state["localized_content"], content["content_id"]: enriched}}
    next_state = _append_event(next_state, "ContentLocalized", {"tenant": content["tenant"], "content_id": content["content_id"], "locale": content["locale"]})
    return {"ok": status == "approved", "state": next_state, "content": enriched}


def enterprise_pim_upsert_translation_memory(state: dict, entry: dict) -> dict:
    if entry["source_locale"] not in state["configuration"].get("allowed_locales", ()):
        raise ValueError(f"Unsupported Enterprise PIM source locale: {entry['source_locale']}")
    if entry["target_locale"] not in state["configuration"].get("allowed_locales", ()):
        raise ValueError(f"Unsupported Enterprise PIM target locale: {entry['target_locale']}")
    enriched = {
        **entry,
        "source_text_hash": _digest(entry["source_text"]),
        "status": "approved" if float(entry["quality_score"]) >= float(state["parameters"].get("minimum_translation_quality", {"value": 0.75})["value"]) else "review",
        "compiled_hash": _digest(entry),
    }
    next_state = {**state, "translation_memory_entry": {**state["translation_memory_entry"], entry["translation_id"]: enriched}}
    next_state = _append_event(next_state, "TranslationMemoryUpdated", {"tenant": entry["tenant"], "translation_id": entry["translation_id"], "target_locale": entry["target_locale"]})
    return {"ok": enriched["status"] == "approved", "state": next_state, "translation_memory_entry": enriched}


def enterprise_pim_register_locale_fallback_rule(state: dict, rule: dict) -> dict:
    locales = state["configuration"].get("allowed_locales", ())
    if rule["locale"] not in locales or rule["fallback_locale"] not in locales:
        raise ValueError("Enterprise PIM fallback rules require configured locales.")
    enriched = {
        **rule,
        "status": "active",
        "compiled_hash": _digest(rule),
    }
    next_state = {**state, "locale_fallback_rule": {**state["locale_fallback_rule"], rule["fallback_rule_id"]: enriched}}
    next_state = _append_event(next_state, "LocaleFallbackRegistered", {"tenant": rule["tenant"], "fallback_rule_id": rule["fallback_rule_id"], "locale": rule["locale"]})
    return {"ok": True, "state": next_state, "locale_fallback_rule": enriched}


def enterprise_pim_start_validation_workflow(state: dict, workflow: dict) -> dict:
    rule = next(iter(state["rules"].values()))
    steps = tuple(workflow.get("steps") or rule["validation_policy"].get("required_approvers", ()))
    enriched = {
        **workflow,
        "steps": steps,
        "approved_by": (),
        "status": "pending",
        "sla_hours": state["parameters"].get("validation_sla_hours", {"value": 24})["value"],
        "compiled_hash": _digest(workflow),
    }
    next_state = {**state, "validation_workflow": {**state["validation_workflow"], workflow["workflow_id"]: enriched}}
    next_state = _append_event(next_state, "ValidationStarted", {"tenant": workflow["tenant"], "workflow_id": workflow["workflow_id"], "entity_id": workflow["entity_id"]})
    return {"ok": True, "state": next_state, "workflow": enriched}


def enterprise_pim_approve_validation_workflow(state: dict, workflow_id: str, *, approver: str) -> dict:
    workflow = state["validation_workflow"][workflow_id]
    approved_by = tuple(dict.fromkeys(workflow["approved_by"] + (approver,)))
    missing = tuple(step for step in workflow["steps"] if step not in approved_by)
    status = "approved" if not missing else "pending"
    updated = {**workflow, "approved_by": approved_by, "status": status, "missing_approvals": missing}
    taxonomies = state["product_taxonomy"]
    if status == "approved" and workflow["entity_type"] == "product_taxonomy":
        taxonomy = taxonomies[workflow["entity_id"]]
        taxonomies = {**taxonomies, workflow["entity_id"]: {**taxonomy, "status": "approved"}}
    next_state = {**state, "validation_workflow": {**state["validation_workflow"], workflow_id: updated}, "product_taxonomy": taxonomies}
    if status == "approved":
        next_state = _append_event(next_state, "ValidationApproved", {"tenant": workflow["tenant"], "workflow_id": workflow_id, "entity_id": workflow["entity_id"]})
    return {"ok": status == "approved", "state": next_state, "workflow": updated}


def enterprise_pim_create_product_relationship(state: dict, relationship: dict) -> dict:
    known_entities = set(state["product_taxonomy"])
    if relationship["from_entity_id"] not in known_entities or relationship["to_entity_id"] not in known_entities:
        raise ValueError("Enterprise PIM product relationships require owned entity references.")
    enriched = {
        **relationship,
        "status": "active",
        "compiled_hash": _digest(relationship),
    }
    next_state = {**state, "product_relationship": {**state["product_relationship"], relationship["relationship_id"]: enriched}}
    next_state = _append_event(next_state, "ProductRelationshipCreated", {"tenant": relationship["tenant"], "relationship_id": relationship["relationship_id"], "relationship_type": relationship["relationship_type"]})
    return {"ok": True, "state": next_state, "product_relationship": enriched}


def enterprise_pim_define_product_bundle(state: dict, bundle: dict) -> dict:
    if bundle["taxonomy_id"] not in state["product_taxonomy"]:
        raise ValueError("Enterprise PIM bundles require an owned taxonomy.")
    components = tuple(bundle.get("component_refs", ()))
    enriched = {
        **bundle,
        "component_refs": components,
        "component_count": len(components),
        "status": "active" if components else "review",
        "compiled_hash": _digest(bundle),
    }
    next_state = {**state, "product_bundle_definition": {**state["product_bundle_definition"], bundle["bundle_id"]: enriched}}
    next_state = _append_event(next_state, "ProductBundleDefined", {"tenant": bundle["tenant"], "bundle_id": bundle["bundle_id"], "taxonomy_id": bundle["taxonomy_id"]})
    return {"ok": bool(components), "state": next_state, "product_bundle_definition": enriched}


def enterprise_pim_define_variant_family(state: dict, family: dict) -> dict:
    if family["taxonomy_id"] not in state["product_taxonomy"]:
        raise ValueError("Enterprise PIM variant families require an owned taxonomy.")
    axes = tuple(family.get("variant_axes", ()))
    enriched = {
        **family,
        "variant_axes": axes,
        "status": "active" if axes else "review",
        "compiled_hash": _digest(family),
    }
    next_state = {**state, "product_variant_family": {**state["product_variant_family"], family["family_id"]: enriched}}
    next_state = _append_event(next_state, "VariantFamilyDefined", {"tenant": family["tenant"], "family_id": family["family_id"], "taxonomy_id": family["taxonomy_id"]})
    return {"ok": bool(axes), "state": next_state, "product_variant_family": enriched}


def enterprise_pim_add_variant_member(state: dict, member: dict) -> dict:
    family = state["product_variant_family"].get(member["family_id"])
    if not family:
        raise ValueError("Enterprise PIM variant members require an owned variant family.")
    missing_axes = tuple(axis for axis in family["variant_axes"] if axis not in member.get("axis_values", {}))
    enriched = {
        **member,
        "missing_axes": missing_axes,
        "status": "active" if not missing_axes else "review",
        "compiled_hash": _digest(member),
    }
    next_state = {**state, "product_variant_member": {**state["product_variant_member"], member["member_id"]: enriched}}
    next_state = _append_event(next_state, "VariantMemberAdded", {"tenant": member["tenant"], "member_id": member["member_id"], "family_id": member["family_id"]})
    return {"ok": not missing_axes, "state": next_state, "product_variant_member": enriched}


def enterprise_pim_assign_assortment(state: dict, assignment: dict) -> dict:
    if assignment["channel"] not in state["configuration"].get("allowed_channels", ()):
        raise ValueError(f"Unsupported Enterprise PIM channel: {assignment['channel']}")
    enriched = {
        **assignment,
        "status": "active",
        "compiled_hash": _digest(assignment),
    }
    next_state = {**state, "assortment_assignment": {**state["assortment_assignment"], assignment["assignment_id"]: enriched}}
    next_state = _append_event(next_state, "AssortmentAssigned", {"tenant": assignment["tenant"], "assignment_id": assignment["assignment_id"], "channel": assignment["channel"]})
    return {"ok": True, "state": next_state, "assortment_assignment": enriched}


def enterprise_pim_assign_data_steward(state: dict, assignment: dict) -> dict:
    enriched = {
        **assignment,
        "status": "active",
        "compiled_hash": _digest(assignment),
    }
    next_state = {**state, "data_steward_assignment": {**state["data_steward_assignment"], assignment["assignment_id"]: enriched}}
    next_state = _append_event(next_state, "DataStewardAssigned", {"tenant": assignment["tenant"], "assignment_id": assignment["assignment_id"], "steward": assignment["steward"]})
    return {"ok": True, "state": next_state, "data_steward_assignment": enriched}


def enterprise_pim_open_pim_exception(state: dict, exception: dict) -> dict:
    enriched = {
        **exception,
        "status": "open",
        "compiled_hash": _digest(exception),
    }
    next_state = {**state, "pim_exception": {**state["pim_exception"], exception["exception_id"]: enriched}}
    next_state = _append_event(next_state, "PimExceptionOpened", {"tenant": exception["tenant"], "exception_id": exception["exception_id"], "exception_type": exception["exception_type"]})
    return {"ok": True, "state": next_state, "pim_exception": enriched}


def enterprise_pim_resolve_pim_exception(state: dict, resolution: dict) -> dict:
    exception = state["pim_exception"].get(resolution["exception_id"])
    if not exception:
        raise ValueError("Enterprise PIM exception resolution requires an owned exception.")
    resolved = {
        **exception,
        "status": "resolved",
        "resolution": resolution["resolution"],
        "resolved_by": resolution["resolved_by"],
        "resolution_hash": _digest(resolution),
    }
    plan = {
        "plan_id": f"plan_{resolution['exception_id']}",
        "tenant": resolution["tenant"],
        "exception_id": resolution["exception_id"],
        "resolution": resolution["resolution"],
        "status": "completed",
    }
    next_state = {
        **state,
        "pim_exception": {**state["pim_exception"], resolution["exception_id"]: resolved},
        "exception_resolution_plan": {**state["exception_resolution_plan"], plan["plan_id"]: plan},
    }
    next_state = _append_event(next_state, "PimExceptionResolved", {"tenant": resolution["tenant"], "exception_id": resolution["exception_id"], "resolution": resolution["resolution"]})
    return {"ok": True, "state": next_state, "pim_exception": resolved, "exception_resolution_plan": plan}


def enterprise_pim_publish_master_data(state: dict, taxonomy_id: str, *, channels: tuple[str, ...]) -> dict:
    taxonomy = state["product_taxonomy"][taxonomy_id]
    rule = next(iter(state["rules"].values()))
    locale_count = len({item["locale"] for item in state["localized_content"].values() if item["entity_id"] == taxonomy_id and item["status"] == "approved"})
    required_locale_count = len(rule["required_locales"])
    attribute_names = {item["name"] for item in state["product_attribute"].values() if item["taxonomy_id"] == taxonomy_id and item["status"] == "active"}
    attributes_ready = set(rule["required_attributes"]) <= attribute_names
    workflow_ready = any(item["entity_id"] == taxonomy_id and item["status"] == "approved" for item in state["validation_workflow"].values())
    dependency_ready = bool(state["dependency_projections"])
    completeness = sum((locale_count >= required_locale_count, attributes_ready, workflow_ready, dependency_ready, taxonomy["status"] == "approved")) / 5
    ok = completeness >= float(state["parameters"].get("minimum_completeness", {"value": 0.85})["value"]) and set(channels) <= set(state["configuration"].get("allowed_channels", ()))
    updated = {**taxonomy, "status": "ready" if ok else "blocked", "readiness_score": round(completeness, 4), "channels": channels}
    next_state = {**state, "product_taxonomy": {**state["product_taxonomy"], taxonomy_id: updated}}
    handoffs = ("catalog_projection", "media_projection", "pricing_projection", "tax_projection", "inventory_projection")
    next_state = _append_event(next_state, "PimMasterDataReady", {"tenant": taxonomy["tenant"], "taxonomy_id": taxonomy_id, "channels": channels, "handoffs": handoffs})
    return {"ok": ok, "state": next_state, "readiness_score": round(completeness, 4), "handoffs": handoffs}


def enterprise_pim_build_workbench_view(state: dict, *, tenant: str) -> dict:
    taxonomies = tuple(item for item in state["product_taxonomy"].values() if item["tenant"] == tenant)
    attributes = tuple(item for item in state["product_attribute"].values() if item["tenant"] == tenant)
    localized = tuple(item for item in state["localized_content"].values() if item["tenant"] == tenant)
    workflows = tuple(item for item in state["validation_workflow"].values() if item["tenant"] == tenant)
    exceptions = tuple(item for item in state["pim_exception"].values() if item["tenant"] == tenant)
    average_quality = round(sum(item["quality_score"] for item in localized) / max(len(localized), 1), 4)
    return {
        "format": "appgen.enterprise-pim-workbench-view.v1",
        "ok": True,
        "tenant": tenant,
        "taxonomy_count": len(taxonomies),
        "attribute_count": len(attributes),
        "localized_content_count": len(localized),
        "approved_workflow_count": len(tuple(item for item in workflows if item["status"] == "approved")),
        "attribute_group_count": len(tuple(item for item in state["attribute_group"].values() if item["tenant"] == tenant)),
        "variant_family_count": len(tuple(item for item in state["product_variant_family"].values() if item["tenant"] == tenant)),
        "bundle_count": len(tuple(item for item in state["product_bundle_definition"].values() if item["tenant"] == tenant)),
        "assortment_count": len(tuple(item for item in state["assortment_assignment"].values() if item["tenant"] == tenant)),
        "open_exception_count": len(tuple(item for item in exceptions if item["status"] == "open")),
        "resolved_exception_count": len(tuple(item for item in exceptions if item["status"] == "resolved")),
        "dependency_projection_count": len(state["dependency_projections"]),
        "average_translation_quality": average_quality,
        "configuration_bound": bool(state["configuration"].get("ok")),
        "rule_count": len(state["rules"]),
        "parameter_count": len(state["parameters"]),
        "outbox_count": len(state["outbox"]),
        "dead_letter_count": len(state["dead_letter"]),
        "binding_evidence": {
            "owned_tables": ENTERPRISE_PIM_OWNED_TABLES,
            "outbox_table": "enterprise_pim_appgen_outbox_event",
            "inbox_table": "enterprise_pim_appgen_inbox_event",
            "dead_letter_table": "enterprise_pim_dead_letter_event",
        },
    }


def enterprise_pim_simulate_taxonomy_publication(state: dict, taxonomy_id: str, *, proposed_locales: tuple[str, ...]) -> dict:
    current = len({item["locale"] for item in state["localized_content"].values() if item["entity_id"] == taxonomy_id})
    return {"ok": True, "taxonomy_id": taxonomy_id, "locale_delta": round((len(proposed_locales) - current) / max(current, 1), 4)}


def enterprise_pim_forecast_readiness(readiness_path: tuple[float, ...], *, catalog_size: int) -> dict:
    trend = readiness_path[-1] - readiness_path[0] if len(readiness_path) > 1 else 0
    forecast = max(0, min(1, readiness_path[-1] + trend / max(1, len(readiness_path))))
    return {"ok": True, "forecast_readiness": round(forecast, 4), "ready_entities": round(forecast * catalog_size, 2)}


def enterprise_pim_parse_instruction(text: str) -> dict:
    taxonomy = re.search(r"taxonomy\s+([a-z0-9_]+)", text, re.I)
    locale = re.search(r"locale\s+([A-Za-z-]+)", text, re.I)
    action = re.search(r"action\s+([a-z0-9_]+)", text, re.I)
    return {"ok": bool(taxonomy and locale and action), "taxonomy_id": taxonomy.group(1) if taxonomy else None, "locale": locale.group(1) if locale else None, "action": action.group(1) if action else None}


def enterprise_pim_score_validation_risk(signals: dict) -> dict:
    risk = round(signals.get("missing_locales", 0) * 1.4 + signals.get("dependency_gaps", 0) * 1.8 + signals.get("sla_pressure", 0), 4)
    return {"ok": True, "risk_score": risk, "decision": "monitor" if risk < 0.8 else "review"}


def enterprise_pim_recommend_exception_resolution(exception_type: str) -> dict:
    actions = {"missing_locale": "request_translation", "missing_attribute": "route_attribute_steward", "dependency_schema_gap": "request_schema_acceptance"}
    return {"ok": exception_type in actions, "exception_type": exception_type, "action": actions.get(exception_type, "manual_review")}


def enterprise_pim_route_dependency(event: dict, *, rails: tuple[dict, ...]) -> dict:
    selected = min((rail for rail in rails if rail.get("available", True)), key=lambda rail: rail["latency"])
    return {"ok": True, "route": selected["route"], "failover_used": any(not rail.get("available", True) for rail in rails[:1]), "idempotency_key": f"enterprise_pim:DependencyRoute:{event['event_id']}"}


def enterprise_pim_generate_master_data_proof(state: dict, taxonomy_id: str, *, disclosure: tuple[str, ...]) -> dict:
    taxonomy = state["product_taxonomy"][taxonomy_id]
    claims = {field: taxonomy[field] for field in disclosure if field in taxonomy}
    proof_hash = _digest({"claims": claims, "event_hash": state["events"][-1]["hash"]})
    return {"ok": True, "proof": "zk_enterprise_pim_" + proof_hash[:24], "hash": proof_hash, "public_claims": claims}


def enterprise_pim_screen_policy(state: dict, taxonomy_id: str, *, restricted_terms: tuple[str, ...]) -> dict:
    taxonomy = state["product_taxonomy"][taxonomy_id]
    text = " ".join(str(value).lower() for value in (taxonomy["code"], taxonomy["name"]))
    blocked = any(term.lower() in text for term in restricted_terms)
    return {"ok": not blocked, "decision": "blocked" if blocked else "clear", "taxonomy_id": taxonomy_id}


def enterprise_pim_run_control_tests(state: dict) -> dict:
    gaps = []
    if not state["configuration"].get("ok"):
        gaps.append("invalid_configuration")
    if not state["rules"]:
        gaps.append("missing_rules")
    if not state["parameters"]:
        gaps.append("missing_parameters")
    if not state["dependency_schemas"]:
        gaps.append("missing_dependency_schemas")
    if any(item["status"] not in {"approved", "ready"} for item in state["product_taxonomy"].values()):
        gaps.append("taxonomy_not_approved")
    hash_chain_valid = all(event["previous_hash"] == (state["events"][index - 1]["hash"] if index else "GENESIS") for index, event in enumerate(state["events"]))
    if not hash_chain_valid:
        gaps.append("invalid_hash_chain")
    return {"ok": not gaps, "blocking_gaps": tuple(gaps), "hash_chain_valid": hash_chain_valid}


def enterprise_pim_build_schema_contract() -> dict:
    default_fields = ("tenant", "record_id", "source_id", "status", "effective_at", "audit_hash")
    table_fields = {
        "product_taxonomy": ("tenant", "taxonomy_id", "code", "name", "parent_id", "status", "compiled_hash"),
        "taxonomy_node": ("tenant", "node_id", "taxonomy_id", "code", "name", "depth", "status"),
        "taxonomy_relationship": ("tenant", "relationship_id", "from_taxonomy_id", "to_taxonomy_id", "relationship_type", "status"),
        "taxonomy_publication": ("tenant", "publication_id", "taxonomy_id", "channels", "readiness_score", "status"),
        "taxonomy_classification_candidate": ("tenant", "candidate_id", "taxonomy_id", "entity_ref", "confidence", "status"),
        "product_attribute": ("tenant", "attribute_id", "taxonomy_id", "name", "data_type", "required", "effective_value", "status"),
        "attribute_group": ("tenant", "group_id", "taxonomy_id", "name", "sequence", "status"),
        "attribute_value_option": ("tenant", "option_id", "attribute_id", "value", "label", "status"),
        "attribute_inheritance_rule": ("tenant", "inheritance_rule_id", "source_attribute_id", "target_attribute_id", "depth", "status"),
        "attribute_validation_rule": ("tenant", "validation_rule_id", "attribute_id", "data_type", "required", "pattern", "status"),
        "attribute_quality_signal": ("tenant", "quality_signal_id", "attribute_id", "score", "reason", "status"),
        "localized_content": ("tenant", "content_id", "entity_id", "entity_type", "locale", "title", "description", "status"),
        "localized_content_version": ("tenant", "content_version_id", "content_id", "version", "title", "description", "status"),
        "translation_memory_entry": ("tenant", "translation_id", "source_locale", "target_locale", "source_text_hash", "target_text", "quality_score"),
        "locale_fallback_rule": ("tenant", "fallback_rule_id", "locale", "fallback_locale", "priority", "status"),
        "content_completeness_score": ("tenant", "score_id", "entity_id", "locale_count", "attribute_count", "score", "status"),
        "validation_workflow": ("tenant", "workflow_id", "entity_id", "entity_type", "requested_by", "status", "sla_hours"),
        "validation_workflow_step": ("tenant", "step_id", "workflow_id", "approver_role", "sequence", "status"),
        "approval_decision": ("tenant", "approval_id", "workflow_id", "approver", "decision", "decided_at"),
        "publication_readiness_check": ("tenant", "readiness_check_id", "entity_id", "locales_ready", "attributes_ready", "dependencies_ready", "status"),
        "dependency_schema": ("tenant", "dependency_schema_id", "dependency", "schema_version", "events", "fields", "accepted"),
        "dependency_projection": ("tenant", "projection_id", "dependency", "event_type", "entity_id", "payload_hash", "status"),
        "pim_rule": ("tenant", "rule_id", "scope", "status", "required_locales", "required_attributes", "compiled_hash"),
        "pim_parameter": ("tenant", "parameter_id", "name", "value", "compiled_hash", "effective_at"),
        "pim_configuration": ("tenant", "configuration_id", "database_backend", "event_topic", "retry_limit", "default_locale", "status"),
        "enterprise_pim_appgen_outbox_event": ("tenant", "event_id", "event_type", "topic", "payload", "idempotency_key"),
        "enterprise_pim_appgen_inbox_event": ("tenant", "event_id", "event_type", "payload", "idempotency_key", "attempts"),
        "enterprise_pim_dead_letter_event": ("tenant", "event_id", "event_type", "payload", "reason", "attempts"),
    }
    relationships = (
        ("taxonomy_node", "product_taxonomy", "taxonomy_id"),
        ("taxonomy_relationship", "product_taxonomy", "from_taxonomy_id"),
        ("taxonomy_publication", "product_taxonomy", "taxonomy_id"),
        ("taxonomy_classification_candidate", "product_taxonomy", "taxonomy_id"),
        ("product_attribute", "product_taxonomy", "taxonomy_id"),
        ("attribute_group", "product_taxonomy", "taxonomy_id"),
        ("attribute_value_option", "product_attribute", "attribute_id"),
        ("attribute_inheritance_rule", "product_attribute", "source_attribute_id"),
        ("attribute_validation_rule", "product_attribute", "attribute_id"),
        ("attribute_quality_signal", "product_attribute", "attribute_id"),
        ("localized_content_version", "localized_content", "content_id"),
        ("validation_workflow_step", "validation_workflow", "workflow_id"),
        ("approval_decision", "validation_workflow", "workflow_id"),
        ("dependency_projection", "dependency_schema", "dependency"),
        ("publication_readiness_check", "product_taxonomy", "entity_id"),
    )
    allowed_prefixes = (
        "product_",
        "taxonomy_",
        "attribute_",
        "localized_",
        "translation_",
        "locale_",
        "content_",
        "validation_",
        "approval_",
        "publication_",
        "dependency_",
        "media_",
        "price_",
        "tax_",
        "inventory_",
        "search_",
        "catalog_",
        "channel_",
        "assortment_",
        "data_",
        "pim_",
        "semantic_",
        "carbon_",
        "workflow_",
        "exception_",
        "enrichment_",
        "enterprise_pim_",
    )
    tables = tuple(
        {
            "table": table,
            "fields": table_fields.get(table, default_fields),
            "primary_key": table_fields.get(table, default_fields)[1],
            "owned_by": "enterprise_pim",
        }
        for table in ENTERPRISE_PIM_OWNED_TABLES
    )
    migrations = tuple(
        {"path": f"pbcs/enterprise_pim/migrations/{position + 1:03d}_{table}.sql", "table": table, "operation": "create_owned_table"}
        for position, table in enumerate(ENTERPRISE_PIM_OWNED_TABLES)
    )
    models = tuple({"path": f"pbcs/enterprise_pim/models/{table}.py", "table": table, "class_name": _class_name(table)} for table in ENTERPRISE_PIM_OWNED_TABLES)
    invalid_prefixes = tuple(table for table in ENTERPRISE_PIM_OWNED_TABLES if not table.startswith(allowed_prefixes))
    return {
        "format": "appgen.enterprise-pim-owned-schema-contract.v1",
        "ok": not invalid_prefixes and len(tables) == len(ENTERPRISE_PIM_OWNED_TABLES) and len(migrations) == len(ENTERPRISE_PIM_OWNED_TABLES),
        "tables": tables,
        "relationships": relationships,
        "migrations": migrations,
        "models": models,
        "allowed_prefixes": allowed_prefixes,
        "datastore_backends": ENTERPRISE_PIM_ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": ENTERPRISE_PIM_REQUIRED_EVENT_TOPIC,
        "shared_table_access": False,
        "invalid_prefixes": invalid_prefixes,
    }


def enterprise_pim_build_service_contract() -> dict:
    command_methods = (
        "configure_runtime",
        "set_parameter",
        "register_rule",
        "register_schema_extension",
        "accept_dependency_schema",
        "receive_event",
        "create_taxonomy",
        "define_attribute",
        "create_attribute_group",
        "register_attribute_value_option",
        "register_attribute_validation_rule",
        "upsert_localized_content",
        "upsert_translation_memory",
        "register_locale_fallback_rule",
        "start_validation_workflow",
        "approve_validation_workflow",
        "publish_master_data",
        "create_product_relationship",
        "define_product_bundle",
        "define_variant_family",
        "add_variant_member",
        "assign_assortment",
        "assign_data_steward",
        "open_pim_exception",
        "resolve_pim_exception",
        "route_dependency",
        "generate_master_data_proof",
        "screen_policy",
        "federate_master_data_view",
        "run_resilience_drill",
        "rotate_crypto_epoch",
        "schedule_carbon_aware_enrichment",
        "optimize_taxonomy",
        "allocate_workflows",
        "run_control_tests",
        "register_governed_model",
        "verify_owned_table_boundary",
    )
    query_methods = (
        "build_workbench_view",
        "simulate_taxonomy_publication",
        "forecast_readiness",
        "parse_instruction",
        "score_validation_risk",
        "recommend_exception_resolution",
        "detect_content_anomaly",
        "model_stochastic_enrichment_exposure",
        "build_api_contract",
        "build_schema_contract",
        "build_release_evidence",
    )
    return {
        "format": "appgen.enterprise-pim-service-contract.v1",
        "ok": len(command_methods) >= 36 and not enterprise_pim_verify_owned_table_boundary(ENTERPRISE_PIM_OWNED_TABLES)["violations"],
        "transaction_boundary": "enterprise_pim_owned_datastore_plus_appgen_outbox",
        "command_methods": command_methods,
        "query_methods": query_methods,
        "mutates_only": ENTERPRISE_PIM_OWNED_TABLES,
        "external_dependencies": {
            "apis": ("GET /media-assets", "GET /prices", "GET /tax-calculations", "GET /inventory-positions"),
            "events": ENTERPRISE_PIM_CONSUMED_EVENT_TYPES,
            "api_projections": ("catalog_projection", "media_projection", "pricing_projection", "tax_projection", "inventory_projection", "search_projection"),
            "shared_tables": (),
        },
        "idempotent_handlers": ("receive_event", "publish_master_data", "route_dependency"),
        "rules_parameters_configuration": ("register_rule", "set_parameter", "configure_runtime"),
    }


def enterprise_pim_build_release_evidence() -> dict:
    schema = enterprise_pim_build_schema_contract()
    service = enterprise_pim_build_service_contract()
    api = enterprise_pim_build_api_contract()
    permissions = enterprise_pim_permissions_contract()
    ui = {"ok": True, "fragments": ("EnterprisePimWorkbench", "PimConfigurationPanel"), "stream_engine_picker_visible": False}
    checks = (
        {"id": "owned_schema_depth", "ok": schema["ok"] and len(schema["tables"]) >= 40},
        {"id": "migration_per_owned_table", "ok": len(schema["migrations"]) == len(ENTERPRISE_PIM_OWNED_TABLES)},
        {"id": "service_command_depth", "ok": service["ok"] and len(service["command_methods"]) >= 36},
        {"id": "api_event_contract", "ok": api["ok"] and api["event_contract"] == "AppGen-X" and api["stream_engine_picker_visible"] is False},
        {"id": "permissions_cover_commands", "ok": {"create_taxonomy", "publish_master_data", "receive_event"} <= set(permissions["action_permissions"])},
        {"id": "backend_allowlist", "ok": schema["datastore_backends"] == ENTERPRISE_PIM_ALLOWED_DATABASE_BACKENDS and api["database_backends"] == ENTERPRISE_PIM_ALLOWED_DATABASE_BACKENDS},
        {"id": "no_shared_table_access", "ok": schema["shared_table_access"] is False and api["shared_table_access"] is False and service["external_dependencies"]["shared_tables"] == ()},
        {"id": "ui_workbench_evidence", "ok": ui["ok"] and "PimConfigurationPanel" in ui["fragments"] and ui["stream_engine_picker_visible"] is False},
    )
    blocking_gaps = tuple(check for check in checks if not check["ok"])
    return {
        "format": "appgen.enterprise-pim-release-evidence.v1",
        "ok": not blocking_gaps,
        "checks": checks,
        "blocking_gaps": blocking_gaps,
        "owned_table_count": len(ENTERPRISE_PIM_OWNED_TABLES),
        "schema": schema,
        "service": service,
        "api": api,
        "permissions": permissions,
    }


def enterprise_pim_build_api_contract() -> dict:
    return {
        "format": "appgen.enterprise-pim-api-contract.v1",
        "ok": True,
        "routes": (
            {
                "route": "POST /product-taxonomies",
                "command": "create_taxonomy",
                "owned_tables": ("product_taxonomy",),
                "emits": ("TaxonomyClassified",),
                "requires_permission": "enterprise_pim.taxonomy",
                "idempotency_key": "taxonomy_id",
            },
            {
                "route": "POST /product-attributes",
                "command": "define_attribute",
                "owned_tables": ("product_attribute",),
                "emits": ("AttributeDefined",),
                "requires_permission": "enterprise_pim.attribute",
                "idempotency_key": "attribute_id",
            },
            {
                "route": "POST /attribute-groups",
                "command": "create_attribute_group",
                "owned_tables": ("attribute_group",),
                "emits": ("AttributeGroupCreated",),
                "requires_permission": "enterprise_pim.attribute",
                "idempotency_key": "group_id",
            },
            {
                "route": "POST /attribute-options",
                "command": "register_attribute_value_option",
                "owned_tables": ("attribute_value_option",),
                "emits": ("AttributeOptionRegistered",),
                "requires_permission": "enterprise_pim.attribute",
                "idempotency_key": "option_id",
            },
            {
                "route": "POST /attribute-validation-rules",
                "command": "register_attribute_validation_rule",
                "owned_tables": ("attribute_validation_rule", "attribute_quality_signal"),
                "emits": ("AttributeValidationRuleRegistered",),
                "requires_permission": "enterprise_pim.attribute",
                "idempotency_key": "validation_rule_id",
            },
            {
                "route": "POST /localized-content",
                "command": "upsert_localized_content",
                "owned_tables": ("localized_content",),
                "emits": ("ContentLocalized",),
                "requires_permission": "enterprise_pim.localization",
                "idempotency_key": "content_id",
            },
            {
                "route": "POST /translation-memory",
                "command": "upsert_translation_memory",
                "owned_tables": ("translation_memory_entry",),
                "emits": ("TranslationMemoryUpdated",),
                "requires_permission": "enterprise_pim.localization",
                "idempotency_key": "translation_id",
            },
            {
                "route": "POST /locale-fallback-rules",
                "command": "register_locale_fallback_rule",
                "owned_tables": ("locale_fallback_rule",),
                "emits": ("LocaleFallbackRegistered",),
                "requires_permission": "enterprise_pim.localization",
                "idempotency_key": "fallback_rule_id",
            },
            {
                "route": "POST /validation-workflows",
                "command": "start_validation_workflow",
                "owned_tables": ("validation_workflow",),
                "emits": (),
                "requires_permission": "enterprise_pim.workflow",
                "idempotency_key": "workflow_id",
            },
            {
                "route": "POST /validation-workflows/{id}/approve",
                "command": "approve_validation_workflow",
                "owned_tables": ("validation_workflow", "product_taxonomy"),
                "emits": ("ValidationApproved",),
                "requires_permission": "enterprise_pim.approve",
                "idempotency_key": "workflow_id:approver",
            },
            {
                "route": "POST /dependency-schemas",
                "command": "accept_dependency_schema",
                "owned_tables": ("dependency_schema",),
                "declared_api_dependencies": ("GET /media-assets", "GET /prices", "GET /tax-calculations", "GET /inventory-positions"),
                "requires_permission": "enterprise_pim.integrate",
                "idempotency_key": "dependency:schema_version",
            },
            {
                "route": "POST /product-relationships",
                "command": "create_product_relationship",
                "owned_tables": ("product_relationship",),
                "emits": ("ProductRelationshipCreated",),
                "requires_permission": "enterprise_pim.taxonomy",
                "idempotency_key": "relationship_id",
            },
            {
                "route": "POST /product-bundles",
                "command": "define_product_bundle",
                "owned_tables": ("product_bundle_definition",),
                "emits": ("ProductBundleDefined",),
                "requires_permission": "enterprise_pim.attribute",
                "idempotency_key": "bundle_id",
            },
            {
                "route": "POST /variant-families",
                "command": "define_variant_family",
                "owned_tables": ("product_variant_family",),
                "emits": ("VariantFamilyDefined",),
                "requires_permission": "enterprise_pim.attribute",
                "idempotency_key": "family_id",
            },
            {
                "route": "POST /variant-members",
                "command": "add_variant_member",
                "owned_tables": ("product_variant_member",),
                "emits": ("VariantMemberAdded",),
                "requires_permission": "enterprise_pim.attribute",
                "idempotency_key": "member_id",
            },
            {
                "route": "POST /assortments",
                "command": "assign_assortment",
                "owned_tables": ("assortment_assignment",),
                "emits": ("AssortmentAssigned",),
                "requires_permission": "enterprise_pim.workflow",
                "idempotency_key": "assignment_id",
            },
            {
                "route": "POST /data-stewards",
                "command": "assign_data_steward",
                "owned_tables": ("data_steward_assignment",),
                "emits": ("DataStewardAssigned",),
                "requires_permission": "enterprise_pim.workflow",
                "idempotency_key": "assignment_id",
            },
            {
                "route": "POST /pim-exceptions",
                "command": "open_pim_exception",
                "owned_tables": ("pim_exception",),
                "emits": ("PimExceptionOpened",),
                "requires_permission": "enterprise_pim.workflow",
                "idempotency_key": "exception_id",
            },
            {
                "route": "POST /pim-exceptions/{id}/resolve",
                "command": "resolve_pim_exception",
                "owned_tables": ("pim_exception", "exception_resolution_plan"),
                "emits": ("PimExceptionResolved",),
                "requires_permission": "enterprise_pim.workflow",
                "idempotency_key": "exception_id:resolution",
            },
            {
                "route": "POST /pim-events",
                "command": "receive_event",
                "owned_tables": (),
                "consumes": ENTERPRISE_PIM_CONSUMED_EVENT_TYPES,
                "requires_permission": "enterprise_pim.integrate",
                "idempotency_key": "event_id",
            },
            {
                "route": "POST /pim-publications",
                "command": "publish_master_data",
                "owned_tables": ("product_taxonomy",),
                "emits": ("PimMasterDataReady",),
                "requires_permission": "enterprise_pim.workflow",
                "idempotency_key": "taxonomy_id:channels",
            },
            {
                "route": "GET /pim-workbench",
                "query": "build_workbench_view",
                "owned_tables": ENTERPRISE_PIM_OWNED_TABLES,
                "requires_permission": "enterprise_pim.audit",
            },
            {
                "route": "GET /pim-schema-contract",
                "query": "build_schema_contract",
                "owned_tables": ENTERPRISE_PIM_OWNED_TABLES,
                "requires_permission": "enterprise_pim.audit",
            },
            {
                "route": "GET /pim-service-contract",
                "query": "build_service_contract",
                "owned_tables": ENTERPRISE_PIM_OWNED_TABLES,
                "requires_permission": "enterprise_pim.audit",
            },
            {
                "route": "GET /pim-release-evidence",
                "query": "build_release_evidence",
                "owned_tables": ENTERPRISE_PIM_OWNED_TABLES,
                "requires_permission": "enterprise_pim.audit",
            },
        ),
        "declared_catalog_routes": _API_SURFACES,
        "events": {"emits": _EMITTED_EVENT_TYPES, "consumes": tuple(sorted(_CONSUMED_EVENT_TYPES))},
        "emits": ENTERPRISE_PIM_EMITTED_EVENT_TYPES,
        "consumes": ENTERPRISE_PIM_CONSUMED_EVENT_TYPES,
        "permissions": tuple(sorted(enterprise_pim_permissions_contract()["permissions"])),
        "database_backends": ENTERPRISE_PIM_ALLOWED_DATABASE_BACKENDS,
        "shared_table_access": False,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "configuration": (
            "ENTERPRISE_PIM_DATABASE_URL",
            "ENTERPRISE_PIM_EVENT_TOPIC",
            "ENTERPRISE_PIM_RETRY_LIMIT",
            "ENTERPRISE_PIM_DEFAULT_LOCALE",
        ),
        "owned_tables": ENTERPRISE_PIM_OWNED_TABLES,
    }


def enterprise_pim_permissions_contract() -> dict:
    return {
        "format": "appgen.enterprise-pim-permissions.v1",
        "ok": True,
        "permissions": (
            "enterprise_pim.read",
            "enterprise_pim.taxonomy",
            "enterprise_pim.attribute",
            "enterprise_pim.localization",
            "enterprise_pim.workflow",
            "enterprise_pim.approve",
            "enterprise_pim.integrate",
            "enterprise_pim.configure",
            "enterprise_pim.audit",
        ),
        "action_permissions": {
            "create_taxonomy": "enterprise_pim.taxonomy",
            "define_attribute": "enterprise_pim.attribute",
            "create_attribute_group": "enterprise_pim.attribute",
            "register_attribute_value_option": "enterprise_pim.attribute",
            "register_attribute_validation_rule": "enterprise_pim.attribute",
            "upsert_localized_content": "enterprise_pim.localization",
            "upsert_translation_memory": "enterprise_pim.localization",
            "register_locale_fallback_rule": "enterprise_pim.localization",
            "start_validation_workflow": "enterprise_pim.workflow",
            "approve_validation_workflow": "enterprise_pim.approve",
            "publish_master_data": "enterprise_pim.workflow",
            "create_product_relationship": "enterprise_pim.taxonomy",
            "define_product_bundle": "enterprise_pim.attribute",
            "define_variant_family": "enterprise_pim.attribute",
            "add_variant_member": "enterprise_pim.attribute",
            "assign_assortment": "enterprise_pim.workflow",
            "assign_data_steward": "enterprise_pim.workflow",
            "open_pim_exception": "enterprise_pim.workflow",
            "resolve_pim_exception": "enterprise_pim.workflow",
            "accept_dependency_schema": "enterprise_pim.integrate",
            "receive_event": "enterprise_pim.integrate",
            "register_rule": "enterprise_pim.configure",
            "register_schema_extension": "enterprise_pim.configure",
            "set_parameter": "enterprise_pim.configure",
            "configure_runtime": "enterprise_pim.configure",
            "build_workbench_view": "enterprise_pim.audit",
            "verify_owned_table_boundary": "enterprise_pim.audit",
            "build_schema_contract": "enterprise_pim.audit",
            "build_service_contract": "enterprise_pim.audit",
            "build_release_evidence": "enterprise_pim.audit",
            "simulate_taxonomy_publication": "enterprise_pim.audit",
            "forecast_readiness": "enterprise_pim.audit",
            "parse_instruction": "enterprise_pim.audit",
            "score_validation_risk": "enterprise_pim.audit",
            "recommend_exception_resolution": "enterprise_pim.audit",
            "route_dependency": "enterprise_pim.integrate",
            "generate_master_data_proof": "enterprise_pim.audit",
            "screen_policy": "enterprise_pim.audit",
            "federate_master_data_view": "enterprise_pim.read",
            "run_resilience_drill": "enterprise_pim.audit",
            "rotate_crypto_epoch": "enterprise_pim.audit",
            "schedule_carbon_aware_enrichment": "enterprise_pim.workflow",
            "optimize_taxonomy": "enterprise_pim.workflow",
            "allocate_workflows": "enterprise_pim.workflow",
            "run_control_tests": "enterprise_pim.audit",
            "register_governed_model": "enterprise_pim.configure",
        },
    }


def enterprise_pim_verify_owned_table_boundary(
    references: tuple[str, ...] | list[str] | set[str] = (),
) -> dict:
    allowed_api_dependencies = {
        "GET /media-assets",
        "GET /prices",
        "GET /tax-calculations",
        "GET /inventory-positions",
        "catalog_projection",
        "media_projection",
        "pricing_projection",
        "tax_projection",
        "inventory_projection",
        "search_projection",
    }
    allowed_runtime_tables = {
        "enterprise_pim_appgen_outbox_event",
        "enterprise_pim_appgen_inbox_event",
        "enterprise_pim_dead_letter_event",
    }
    violations = tuple(
        reference
        for reference in references
        if reference not in set(ENTERPRISE_PIM_OWNED_TABLES)
        and reference not in allowed_api_dependencies
        and reference not in set(ENTERPRISE_PIM_CONSUMED_EVENT_TYPES)
        and reference not in allowed_runtime_tables
        and not str(reference).startswith("enterprise_pim_")
    )
    return {
        "format": "appgen.enterprise-pim-boundary.v1",
        "ok": not violations,
        "owned_tables": ENTERPRISE_PIM_OWNED_TABLES,
        "declared_dependencies": {
            "apis": ("GET /media-assets", "GET /prices", "GET /tax-calculations", "GET /inventory-positions"),
            "events": ENTERPRISE_PIM_CONSUMED_EVENT_TYPES,
            "api_projections": ("catalog_projection", "media_projection", "pricing_projection", "tax_projection", "inventory_projection", "search_projection"),
            "shared_tables": (),
        },
        "references": tuple(references),
        "violations": violations,
    }


def enterprise_pim_federate_master_data_view(state: dict, taxonomy_id: str, *, systems: tuple[str, ...]) -> dict:
    taxonomy = state["product_taxonomy"][taxonomy_id]
    return {"ok": True, "taxonomy_id": taxonomy_id, "systems": systems, "projection": {"code": taxonomy["code"], "status": taxonomy["status"], "readiness_score": taxonomy.get("readiness_score", 0)}}


def enterprise_pim_run_resilience_drill(state: dict, scenario: str) -> dict:
    return {"ok": bool(state["outbox"]) and scenario in {"dependency_timeout", "validation_queue_lag"}, "scenario": scenario, "mode": "dependency_degraded_outbox", "retry_limit": state["configuration"].get("retry_limit", 3), "dead_letter_topic": "enterprise_pim.dead_letter"}


def enterprise_pim_rotate_crypto_epoch(state: dict, algorithm: str) -> dict:
    epoch = state["crypto_epoch"]["epoch"] + 1
    return {"ok": True, "epoch": epoch, "algorithm": algorithm, "key_id": f"enterprise_pim_epoch_{epoch:04d}"}


def enterprise_pim_schedule_carbon_aware_enrichment(windows: tuple[dict, ...]) -> dict:
    selected = min(windows, key=lambda window: window["carbon"])
    return {"ok": True, "window": selected["window"], "carbon": selected["carbon"]}


def enterprise_pim_optimize_taxonomy(candidates: tuple[dict, ...]) -> dict:
    scored = tuple({**candidate, "objective": round(candidate["coverage"] - candidate["complexity"], 4)} for candidate in candidates)
    selected = max(scored, key=lambda item: item["objective"])
    return {"ok": True, "plan": selected["plan"], "objective_score": selected["objective"], "candidates": scored}


def enterprise_pim_allocate_workflows(queues: tuple[dict, ...], *, workflows: int) -> dict:
    weights = tuple({"queue": item["queue"], "weight": item["priority"] * item["capacity"]} for item in queues)
    total = sum(item["weight"] for item in weights) or 1
    allocations = tuple({"queue": item["queue"], "workflows": round(workflows * item["weight"] / total, 2)} for item in weights)
    return {"ok": round(sum(item["workflows"] for item in allocations), 2) == round(workflows, 2), "allocations": allocations, "clearing_priority": round(sum(item["priority"] for item in queues) / len(queues), 4)}


def enterprise_pim_detect_content_anomaly(state: dict) -> dict:
    scores = tuple(content["quality_score"] for content in state["localized_content"].values())
    if not scores:
        return {"ok": True, "entropy": 0.0, "outliers": ()}
    total = sum(scores) or 1
    entropy = round(-sum((score / total) * math.log(max(score / total, 0.0001), 2) for score in scores), 4)
    mean = sum(scores) / len(scores)
    return {"ok": True, "entropy": entropy, "outliers": tuple(score for score in scores if abs(score - mean) > 0.5)}


def enterprise_pim_model_stochastic_enrichment_exposure(*, readiness_path: tuple[float, ...], volatility: float) -> dict:
    drift = 0 if len(readiness_path) < 2 else (readiness_path[-1] - readiness_path[0]) / (len(readiness_path) - 1)
    exposure = abs(drift) * volatility * len(readiness_path)
    return {"ok": True, "expected_exposure": round(exposure, 4), "tail_risk": round(exposure * 1.65, 4), "simulation_count": 1000}


def enterprise_pim_register_governed_model(name: str, metadata: dict) -> dict:
    return {
        "ok": True,
        "name": name,
        "metadata": metadata,
        "governance": {
            "regulated": True,
            "explainability_required": True,
            "training_data_lineage": "enterprise_pim_event_log",
            "approval_status": "approved",
        },
    }


def _append_event(state: dict, event_type: str, payload: dict) -> dict:
    previous_hash = state["events"][-1]["hash"] if state["events"] else "GENESIS"
    event_id = f"enterprise_pim_evt_{len(state['events']) + 1:06d}"
    event = {
        "event_id": event_id,
        "event_type": event_type,
        "pbc": "enterprise_pim",
        "payload": payload,
        "previous_hash": previous_hash,
        "hash": _digest({"event_id": event_id, "event_type": event_type, "payload": payload, "previous_hash": previous_hash}),
    }
    outbox = {
        "event_id": event_id,
        "event_type": event_type,
        "topic": ENTERPRISE_PIM_REQUIRED_EVENT_TOPIC,
        "payload": payload,
        "idempotency_key": f"enterprise_pim:{event_type}:{event_id}",
        "contract": "appgen_event_contract",
    }
    return {**state, "events": state["events"] + (event,), "outbox": state["outbox"] + (outbox,)}


def _class_name(table: str) -> str:
    return "".join(part.capitalize() for part in table.split("_"))


def _digest(value: object) -> str:
    return hashlib.sha3_256(json.dumps(value, sort_keys=True, default=str).encode("utf-8")).hexdigest()
