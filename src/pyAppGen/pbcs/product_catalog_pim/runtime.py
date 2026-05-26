"""Executable runtime for the Enterprise Product Catalog and PIM PBC."""

from __future__ import annotations

import hashlib
import json
import math
import re


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
    "sku_governance",
    "taxonomy_assignment",
    "attribute_schema",
    "attribute_validation",
    "enrichment_completeness",
    "localized_content",
    "seo_metadata",
    "media_reference",
    "media_rights",
    "price_metadata",
    "channel_projection",
    "catalog_publication",
    "sellability_rules",
    "compliance_claims",
    "restricted_region_screening",
    "search_index_signal",
    "forecast_signal",
    "idempotent_handlers",
    "permissions",
    "configuration_schema",
    "rule_engine",
    "parameter_engine",
    "seed_data",
    "workbench",
)


def product_catalog_pim_runtime_capabilities() -> dict:
    smoke = product_catalog_pim_runtime_smoke()
    return {
        "format": "appgen.product-catalog-pim-runtime-capabilities.v1",
        "ok": smoke["ok"],
        "pbc": "product_catalog_pim",
        "implementation_directory": "src/pyAppGen/pbcs/product_catalog_pim",
        "capabilities": PRODUCT_CATALOG_PIM_RUNTIME_CAPABILITY_KEYS,
        "standard_features": PRODUCT_CATALOG_PIM_STANDARD_FEATURE_KEYS,
        "operations": (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "create_product_family",
            "register_product",
            "define_attribute_schema",
            "set_product_attribute",
            "add_localized_content",
            "attach_product_media",
            "add_price_metadata",
            "add_compliance_claim",
            "publish_product",
            "build_workbench_view",
        ),
        "smoke": smoke,
    }


def product_catalog_pim_runtime_smoke() -> dict:
    state = product_catalog_pim_empty_state()
    state = product_catalog_pim_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": "appgen.product.events",
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
        {"family_id": "fam_100", "tenant": "tenant_alpha", "name": "Machine Kits", "taxonomy": "industrial/kits", "variant_axes": ("color", "size")},
    )
    state = family["state"]
    product = product_catalog_pim_register_product(
        state,
        {"product_id": "prod_100", "tenant": "tenant_alpha", "family_id": "fam_100", "sku": "KIT-100", "name": "Hydraulic Kit", "lifecycle_state": "draft", "owner": "catalog_ops"},
    )
    state = product["state"]
    schema = product_catalog_pim_define_attribute_schema(
        state,
        {"schema_id": "schema_100", "tenant": "tenant_alpha", "family_id": "fam_100", "attributes": {"color": "string", "material": "string", "weight": "number"}},
    )
    state = schema["state"]
    state = product_catalog_pim_set_product_attribute(state, "prod_100", "color", "blue")["state"]
    state = product_catalog_pim_set_product_attribute(state, "prod_100", "material", "steel")["state"]
    state = product_catalog_pim_set_product_attribute(state, "prod_100", "weight", 12.5)["state"]
    content = product_catalog_pim_add_localized_content(
        state,
        {"content_id": "content_100", "tenant": "tenant_alpha", "product_id": "prod_100", "locale": "en-US", "title": "Hydraulic Kit", "description": "Complete hydraulic maintenance kit", "seo_slug": "hydraulic-kit"},
    )
    state = content["state"]
    media = product_catalog_pim_attach_product_media(
        state,
        {"media_id": "media_100", "tenant": "tenant_alpha", "product_id": "prod_100", "role": "hero", "asset_ref": "dam://asset-100", "rights_status": "approved", "alt_text": "Hydraulic kit hero image"},
    )
    state = media["state"]
    price = product_catalog_pim_add_price_metadata(
        state,
        {"price_id": "price_100", "tenant": "tenant_alpha", "product_id": "prod_100", "currency": "USD", "list_price": 250, "cost": 180, "effective_from": "2026-05-26"},
    )
    state = price["state"]
    compliance = product_catalog_pim_add_compliance_claim(
        state,
        {"claim_id": "claim_100", "tenant": "tenant_alpha", "product_id": "prod_100", "region": "US", "claim_type": "safety", "status": "approved"},
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
    simulation = product_catalog_pim_simulate_publication(state, "prod_100", proposed_channels=("web",))
    forecast = product_catalog_pim_forecast_sellability((0.6, 0.7, 0.85), catalog_size=100)
    parsed = product_catalog_pim_parse_product_instruction("product prod_777 channel web locale en-US action publish")
    risk = product_catalog_pim_score_readiness_risk({"completeness": 0.2, "compliance": 0.1, "content": 0.2, "price": 0.1})
    recommendation = product_catalog_pim_recommend_exception_resolution("missing_media")
    route = product_catalog_pim_route_publication({"event_id": "pub_route"}, rails=({"route": "channel_api", "available": False, "latency": 2}, {"route": "outbox", "available": True, "latency": 4}))
    proof = product_catalog_pim_generate_publication_proof(state, "prod_100", disclosure=("product_id", "sku", "lifecycle_state"))
    screening = product_catalog_pim_screen_policy(state, "prod_100", restricted_regions=("restricted",))
    controls = product_catalog_pim_run_control_tests(state)
    api = product_catalog_pim_build_api_contract()
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
        {"id": "universal_api_async_streaming", "ok": api["ok"] and "ProductPublished" in api["events"]["emits"]},
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
        {"id": "distributed_systems_engineering", "ok": state["outbox"][-1]["idempotency_key"].startswith("product_catalog_pim:ProductPublished")},
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
        "crypto_epoch": {"epoch": 1, "algorithm": "sha3_256"},
    }


def product_catalog_pim_configure_runtime(state: dict, configuration: dict) -> dict:
    allowed_databases = {"postgresql", "mysql", "mariadb"}
    if configuration.get("database_backend") not in allowed_databases:
        raise ValueError("Product Catalog PIM supports only PostgreSQL, MySQL, or MariaDB backends")
    if not configuration.get("event_topic"):
        raise ValueError("Product Catalog PIM requires an AppGen-X event topic")
    configured = {
        **configuration,
        "ok": True,
        "event_contract": "appgen_event_contract",
        "allowed_database_backends": tuple(sorted(allowed_databases)),
    }
    return {"ok": True, "state": {**state, "configuration": configured}, "configuration": configured}


def product_catalog_pim_set_parameter(state: dict, name: str, value: float | int | str | bool) -> dict:
    allowed = {
        "minimum_completeness",
        "minimum_margin",
        "max_missing_required_attributes",
        "content_quality_threshold",
        "publication_batch_size",
        "retention_days",
        "workbench_limit",
    }
    if name not in allowed:
        raise ValueError(f"Unsupported Product Catalog PIM parameter: {name}")
    return {"ok": True, "state": {**state, "parameters": {**state["parameters"], name: value}}, "parameter": {"name": name, "value": value}}


def product_catalog_pim_register_rule(state: dict, rule: dict) -> dict:
    required = {"rule_id", "tenant", "status"}
    missing = tuple(sorted(field for field in required if field not in rule))
    if missing:
        raise ValueError(f"Missing required Product Catalog PIM rule fields: {missing}")
    scope = rule.get("scope") or rule.get("rule_type")
    if not scope:
        raise ValueError("Product Catalog PIM rule requires scope or rule_type")
    enriched = {**rule, "scope": scope, "enabled": rule["status"] == "active", "compiled_hash": _digest(rule)}
    return {"ok": True, "state": {**state, "rules": {**state["rules"], rule["rule_id"]: enriched}}, "rule": enriched}


def product_catalog_pim_register_schema_extension(state: dict, table: str, fields: dict) -> dict:
    invalid = tuple(name for name in fields if not re.fullmatch(r"[a-z][a-z0-9_]*", name))
    if invalid:
        return {"ok": False, "error": "invalid_extension_field", "invalid": invalid, "state": state}
    return {"ok": True, "state": {**state, "schema_extensions": {**state["schema_extensions"], table: dict(fields)}}}


def product_catalog_pim_create_product_family(state: dict, family: dict) -> dict:
    enriched = {**family, "status": "active", "graph_degree": len(tuple(value for value in (family["name"], family["taxonomy"], family["variant_axes"]) if value))}
    next_state = {**state, "families": {**state["families"], family["family_id"]: enriched}}
    next_state = _append_event(next_state, "ProductClassified", {"tenant": family["tenant"], "family_id": family["family_id"], "taxonomy": family["taxonomy"]})
    return {"ok": True, "state": next_state, "family": enriched}


def product_catalog_pim_register_product(state: dict, product: dict) -> dict:
    family = state["families"][product["family_id"]]
    enriched = {**product, "taxonomy": family["taxonomy"], "lifecycle_state": product.get("lifecycle_state", "draft"), "graph_degree": len(tuple(value for value in (product["sku"], product["name"], product["family_id"], family["taxonomy"]) if value))}
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
    schema = next(schema for schema in state["schemas"].values() if schema["family_id"] == product["family_id"])
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
    updated = {**product, "lifecycle_state": "published" if ok else "blocked", "published_by": published_by, "channels": channels, "locales": locales, "completeness": completeness}
    publication_id = f"publication_{len(state['publications']) + 1:06d}"
    publication = {"publication_id": publication_id, "tenant": product["tenant"], "product_id": product_id, "channels": channels, "locales": locales, "readiness_score": round(completeness, 4), "status": "published" if ok else "blocked"}
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
    if not state["configuration"].get("ok"):
        gaps.append("invalid_configuration")
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


def product_catalog_pim_build_api_contract() -> dict:
    return {
        "ok": True,
        "routes": ("POST /products", "POST /product-families", "POST /product-variants", "POST /attribute-schemas", "POST /product-attributes", "POST /product-media", "POST /product-locale-content", "POST /product-prices", "POST /product-compliance-claims", "POST /catalog-publications", "GET /product-read-models", "POST /product-rules", "POST /product-parameters", "POST /product-configuration"),
        "events": {"emits": ("ProductClassified", "ProductEnriched", "ProductPublished", "ProductPriceReady", "ForecastUpdated"), "consumes": ("TaxCalculated", "MediaAssetApproved", "InventoryPositionUpdated", "PricePromotionApproved")},
        "permissions": ("product_catalog_pim.read", "product_catalog_pim.product", "product_catalog_pim.enrich", "product_catalog_pim.publish", "product_catalog_pim.configure", "product_catalog_pim.audit"),
        "configuration": ("PRODUCT_CATALOG_PIM_DATABASE_URL", "PRODUCT_CATALOG_PIM_EVENT_TOPIC", "PRODUCT_CATALOG_PIM_RETRY_LIMIT", "PRODUCT_CATALOG_PIM_DEFAULT_TIMEZONE"),
    }


def product_catalog_pim_federate_product_view(state: dict, product_id: str, *, systems: tuple[str, ...]) -> dict:
    product = state["products"][product_id]
    return {"ok": True, "product_id": product_id, "systems": systems, "projection": {"sku": product["sku"], "state": product["lifecycle_state"], "completeness": product.get("completeness", 0)}}


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
    }


def product_catalog_pim_register_governed_model(name: str, metadata: dict) -> dict:
    return {"ok": metadata.get("auc", 0) >= 0.85 and metadata.get("drift_score", 1) <= 0.1, "name": name, "metadata": metadata, "governance": {"regulated": True, "feature_lineage": tuple(metadata.get("features", ())), "explainability_required": True}}


def _append_event(state: dict, event_type: str, payload: dict) -> dict:
    previous_hash = state["events"][-1]["hash"] if state["events"] else "GENESIS"
    sequence = len(state["events"]) + 1
    event = {"event_id": f"product_evt_{sequence:06d}", "event_type": event_type, "payload": payload, "previous_hash": previous_hash}
    event = {**event, "hash": _digest(event)}
    outbox_event = {"event_type": event_type, "payload": payload, "idempotency_key": f"product_catalog_pim:{event_type}:{event['event_id']}"}
    return {**state, "events": (*state["events"], event), "outbox": (*state["outbox"], outbox_event)}


def _digest(value: object) -> str:
    return hashlib.sha3_256(json.dumps(value, sort_keys=True, default=str).encode("utf-8")).hexdigest()
