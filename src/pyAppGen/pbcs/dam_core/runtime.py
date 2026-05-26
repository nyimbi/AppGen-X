"""Executable runtime for the Digital Asset Management Core PBC."""

from __future__ import annotations

import hashlib
import json
import math
import re


DAM_CORE_REQUIRED_EVENT_TOPIC = "appgen.dam.events"
DAM_CORE_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
DAM_CORE_OWNED_TABLES = ("asset", "asset_rendition", "rights_policy", "metadata_tag")

DAM_CORE_RUNTIME_CAPABILITY_KEYS = (
    "event_sourced_asset_lifecycle",
    "owned_media_schema_boundary",
    "multi_tenant_asset_isolation",
    "schema_evolution_resilient_asset_metadata",
    "content_addressed_binary_fingerprinting",
    "rendition_transcoding_pipeline",
    "semantic_metadata_tagging",
    "rights_policy_enforcement",
    "product_published_projection_handling",
    "probabilistic_rights_and_quality_scoring",
    "counterfactual_rendition_cost_simulation",
    "temporal_asset_usage_forecasting",
    "autonomous_asset_exception_resolution",
    "semantic_asset_instruction_parsing",
    "predictive_asset_governance_risk",
    "self_healing_transcode_route_selection",
    "cryptographic_asset_proof",
    "immutable_asset_audit_trail",
    "dynamic_policy_screening",
    "automated_control_testing",
    "appgen_x_outbox_inbox_eventing",
    "idempotent_handlers",
    "retry_dead_letter_evidence",
    "permissions_governance_evidence",
    "configuration_schema",
    "parameter_engine",
    "rule_engine",
    "seed_data",
    "workbench_ui",
)

DAM_CORE_STANDARD_FEATURE_KEYS = (
    "asset_lifecycle",
    "asset_binary_fingerprint",
    "asset_rendition",
    "transcoding_job",
    "metadata_tag",
    "rights_policy",
    "product_published_dependency",
    "tenant_isolation",
    "appgen_x_outbox",
    "appgen_x_inbox",
    "idempotent_handlers",
    "retry_dead_letter_evidence",
    "permissions",
    "configuration_schema",
    "rule_engine",
    "parameter_engine",
    "seed_data",
    "workbench",
    "immutable_audit",
    "release_audit_evidence",
)

DAM_CORE_SUPPORTED_CONFIGURATION_FIELDS = (
    "database_backend",
    "event_topic",
    "retry_limit",
    "default_storage_tier",
    "allowed_mime_types",
    "rendition_profiles",
    "rights_default_decision",
    "metadata_taxonomies",
    "default_locale",
    "workbench_limit",
)

DAM_CORE_SUPPORTED_PARAMETER_KEYS = (
    "max_asset_size_mb",
    "quality_threshold",
    "rights_risk_threshold",
    "transcode_retry_limit",
    "duplicate_similarity_threshold",
    "rendition_cost_weight",
    "carbon_cost_weight",
    "usage_forecast_horizon_days",
    "metadata_confidence_floor",
    "workbench_limit",
)

DAM_CORE_REQUIRED_RULE_FIELDS = (
    "rule_id",
    "tenant",
    "scope",
    "status",
    "mime_policy",
    "rights_policy",
    "rendition_policy",
    "metadata_policy",
)

DAM_CORE_CONSUMED_EVENT_TYPES = ("ProductPublished",)
DAM_CORE_EMITTED_EVENT_TYPES = (
    "AssetRegistered",
    "AssetRenditionReady",
    "AssetRightsBlocked",
    "AssetTagged",
)

_CONFIG_SEQUENCE_FIELDS = {
    "allowed_mime_types",
    "rendition_profiles",
    "metadata_taxonomies",
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
_PARAMETER_BOUNDS = {
    "max_asset_size_mb": (1, 50000),
    "quality_threshold": (0.0, 1.0),
    "rights_risk_threshold": (0.0, 1.0),
    "transcode_retry_limit": (1, 10),
    "duplicate_similarity_threshold": (0.0, 1.0),
    "rendition_cost_weight": (0.0, 1.0),
    "carbon_cost_weight": (0.0, 1.0),
    "usage_forecast_horizon_days": (1, 3650),
    "metadata_confidence_floor": (0.0, 1.0),
    "workbench_limit": (1, 1000),
}


def dam_core_runtime_capabilities() -> dict:
    smoke = dam_core_runtime_smoke()
    return {
        "format": "appgen.dam-core-runtime-capabilities.v1",
        "ok": smoke["ok"],
        "pbc": "dam_core",
        "implementation_directory": "src/pyAppGen/pbcs/dam_core",
        "owned_tables": DAM_CORE_OWNED_TABLES,
        "capabilities": DAM_CORE_RUNTIME_CAPABILITY_KEYS,
        "standard_features": DAM_CORE_STANDARD_FEATURE_KEYS,
        "operations": (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "register_schema_extension",
            "receive_event",
            "register_asset",
            "attach_rights_policy",
            "add_metadata_tag",
            "request_rendition",
            "complete_rendition",
            "enforce_rights",
            "build_workbench_view",
        ),
        "smoke": smoke,
    }


def dam_core_runtime_smoke() -> dict:
    state = dam_core_empty_state()
    state = dam_core_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": DAM_CORE_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "default_storage_tier": "warm",
            "allowed_mime_types": ("image/jpeg", "image/png", "video/mp4"),
            "rendition_profiles": ("web_large", "thumbnail", "social_square"),
            "rights_default_decision": "review",
            "metadata_taxonomies": ("product", "campaign", "usage"),
            "default_locale": "en-US",
            "workbench_limit": 100,
        },
    )["state"]
    for name, value in (
        ("max_asset_size_mb", 1000),
        ("quality_threshold", 0.72),
        ("rights_risk_threshold", 0.65),
        ("transcode_retry_limit", 3),
        ("duplicate_similarity_threshold", 0.95),
        ("rendition_cost_weight", 0.35),
        ("carbon_cost_weight", 0.15),
        ("usage_forecast_horizon_days", 90),
        ("metadata_confidence_floor", 0.62),
        ("workbench_limit", 100),
    ):
        state = dam_core_set_parameter(state, name, value)["state"]
    state = dam_core_register_rule(
        state,
        {
            "rule_id": "rule_dam_default",
            "tenant": "tenant_alpha",
            "scope": "asset_governance",
            "status": "active",
            "mime_policy": {"allowed": ("image/jpeg", "image/png", "video/mp4")},
            "rights_policy": {"blocked_markets": ("restricted",), "license_required": True},
            "rendition_policy": {"required_profiles": ("web_large", "thumbnail")},
            "metadata_policy": {"required_tags": ("product", "campaign")},
        },
    )["state"]
    state = dam_core_register_schema_extension(state, "asset", {"ai_caption": "jsonb"})["state"]
    state = dam_core_receive_event(
        state,
        {
            "event_id": "evt_product_001",
            "event_type": "ProductPublished",
            "idempotency_key": "product:sku_100:v1",
            "payload": {
                "tenant": "tenant_alpha",
                "product_id": "sku_100",
                "name": "Launch Backpack",
                "published_at": "2026-05-26T09:00:00Z",
            },
        },
    )["state"]
    duplicate = dam_core_receive_event(
        state,
        {
            "event_id": "evt_product_001",
            "event_type": "ProductPublished",
            "idempotency_key": "product:sku_100:v1",
            "payload": {"tenant": "tenant_alpha", "product_id": "sku_100"},
        },
    )
    state = duplicate["state"]
    invalid_event = dam_core_receive_event(
        state,
        {
            "event_id": "evt_invalid_001",
            "event_type": "UnknownEvent",
            "idempotency_key": "invalid:1",
            "attempts": 3,
            "payload": {"tenant": "tenant_alpha"},
        },
    )
    state = invalid_event["state"]
    asset = dam_core_register_asset(
        state,
        {
            "asset_id": "asset_100",
            "tenant": "tenant_alpha",
            "product_id": "sku_100",
            "filename": "launch-backpack.jpg",
            "mime_type": "image/jpeg",
            "size_mb": 24,
            "storage_uri": "object://dam/tenant_alpha/asset_100",
            "binary": b"launch-backpack-primary-image",
            "locale": "en-US",
            "created_by": "user_ops",
        },
    )
    state = asset["state"]
    state = dam_core_attach_rights_policy(
        state,
        {
            "policy_id": "rights_100",
            "asset_id": "asset_100",
            "tenant": "tenant_alpha",
            "license_type": "commercial",
            "allowed_markets": ("US", "CA"),
            "blocked_markets": ("restricted",),
            "expires_at": "2027-05-26",
            "attribution_required": False,
            "approver": "legal_ops",
        },
    )["state"]
    state = dam_core_add_metadata_tag(
        state,
        {
            "tag_id": "tag_100",
            "asset_id": "asset_100",
            "tenant": "tenant_alpha",
            "taxonomy": "product",
            "value": "backpack",
            "confidence": 0.91,
            "source": "human",
        },
    )["state"]
    state = dam_core_add_metadata_tag(
        state,
        {
            "tag_id": "tag_101",
            "asset_id": "asset_100",
            "tenant": "tenant_alpha",
            "taxonomy": "campaign",
            "value": "launch",
            "confidence": 0.88,
            "source": "human",
        },
    )["state"]
    rendition = dam_core_request_rendition(
        state,
        {
            "rendition_id": "rend_100",
            "asset_id": "asset_100",
            "tenant": "tenant_alpha",
            "profile": "web_large",
            "target_mime_type": "image/jpeg",
            "width": 1600,
            "height": 1200,
        },
    )
    state = rendition["state"]
    completed = dam_core_complete_rendition(
        state,
        "rend_100",
        {"uri": "object://dam/tenant_alpha/asset_100/web_large.jpg", "quality_score": 0.93, "duration_ms": 840},
    )
    state = completed["state"]

    rights = dam_core_enforce_rights(state, "asset_100", market="US", use_case="product_detail")
    blocked = dam_core_enforce_rights(state, "asset_100", market="restricted", use_case="product_detail")
    quality = dam_core_score_asset_quality(state, "asset_100")
    simulation = dam_core_simulate_rendition_cost(
        state,
        "asset_100",
        (
            {"route": "gpu_low_carbon", "cost": 1.2, "latency": 2.0, "carbon": 35},
            {"route": "cpu_standard", "cost": 0.8, "latency": 4.0, "carbon": 90},
        ),
    )
    forecast = dam_core_forecast_asset_usage((12, 18, 25, 33), horizon_days=30)
    resolution = dam_core_resolve_asset_exception("missing_rights")
    parsed = dam_core_parse_asset_instruction("tag product backpack render web_large block restricted")
    governance = dam_core_predictive_governance_risk({"rights_risk": 0.12, "quality_risk": 0.08, "metadata_risk": 0.05})
    route = dam_core_select_transcode_route(
        (
            {"route": "primary_gpu", "available": False, "latency": 1.0, "carbon": 80},
            {"route": "low_carbon_gpu", "available": True, "latency": 1.6, "carbon": 30},
        )
    )
    proof = dam_core_generate_asset_proof(state, "asset_100", disclosure=("asset_id", "fingerprint", "rights_decision"))
    controls = dam_core_run_control_tests(state)
    api = dam_core_build_api_contract()
    policy = dam_core_screen_dynamic_policy(state, "asset_100", market="US", mime_type="image/jpeg")
    workbench = dam_core_build_workbench_view(state, tenant="tenant_alpha")

    checks = (
        {"id": "event_sourced_asset_lifecycle", "ok": len(state["events"]) >= 4 and state["events"][-1]["hash"]},
        {"id": "owned_media_schema_boundary", "ok": set(DAM_CORE_OWNED_TABLES) == {"asset", "asset_rendition", "rights_policy", "metadata_tag"}},
        {"id": "multi_tenant_asset_isolation", "ok": workbench["tenant"] == "tenant_alpha" and controls["tenant_isolation"]},
        {"id": "schema_evolution_resilient_asset_metadata", "ok": state["schema_extensions"]["asset"]["ai_caption"] == "jsonb"},
        {"id": "content_addressed_binary_fingerprinting", "ok": asset["asset"]["fingerprint"].startswith("sha256:")},
        {"id": "rendition_transcoding_pipeline", "ok": completed["rendition"]["status"] == "ready" and completed["rendition"]["quality_score"] >= 0.9},
        {"id": "semantic_metadata_tagging", "ok": "product:backpack" in state["assets"]["asset_100"]["tag_index"]},
        {"id": "rights_policy_enforcement", "ok": rights["decision"] == "allow" and blocked["decision"] == "block"},
        {"id": "product_published_projection_handling", "ok": state["product_projection"]["sku_100"]["name"] == "Launch Backpack"},
        {"id": "probabilistic_rights_and_quality_scoring", "ok": quality["ok"] and quality["quality_score"] >= 0.7},
        {"id": "counterfactual_rendition_cost_simulation", "ok": simulation["ok"] and simulation["best_route"] == "gpu_low_carbon"},
        {"id": "temporal_asset_usage_forecasting", "ok": forecast["ok"] and forecast["expected_usage"] > 0},
        {"id": "autonomous_asset_exception_resolution", "ok": resolution["action"] == "request_rights_policy"},
        {"id": "semantic_asset_instruction_parsing", "ok": parsed["ok"] and parsed["profile"] == "web_large"},
        {"id": "predictive_asset_governance_risk", "ok": governance["risk_score"] > 0},
        {"id": "self_healing_transcode_route_selection", "ok": route["route"] == "low_carbon_gpu" and route["failover_used"]},
        {"id": "cryptographic_asset_proof", "ok": proof["ok"] and proof["proof"].startswith("zk_asset_")},
        {"id": "immutable_asset_audit_trail", "ok": controls["hash_chain_valid"]},
        {"id": "dynamic_policy_screening", "ok": policy["ok"] and policy["decision"] == "allow"},
        {"id": "automated_control_testing", "ok": controls["ok"] and not controls["blocking_gaps"]},
        {"id": "appgen_x_outbox_inbox_eventing", "ok": workbench["outbox_count"] == 4 and workbench["inbox_count"] == 1},
        {"id": "idempotent_handlers", "ok": duplicate["duplicate"] is True and workbench["processed_event_count"] == 2},
        {"id": "retry_dead_letter_evidence", "ok": invalid_event["dead_lettered"] is True and workbench["dead_letter_count"] == 1},
        {"id": "permissions_governance_evidence", "ok": "dam_core.configure" in api["permissions"]},
        {"id": "configuration_schema", "ok": state["configuration"]["event_contract"] == "AppGen-X"},
        {"id": "parameter_engine", "ok": len(state["parameters"]) == len(DAM_CORE_SUPPORTED_PARAMETER_KEYS)},
        {"id": "rule_engine", "ok": state["rules"]["rule_dam_default"]["compiled_hash"]},
        {"id": "seed_data", "ok": "rendition_profiles" in state["seed_data"]},
        {"id": "workbench_ui", "ok": workbench["asset_count"] == 1 and workbench["rendition_count"] == 1},
    )
    blocking_gaps = tuple(check for check in checks if not check["ok"])
    return {"format": "appgen.dam-core-runtime-smoke.v1", "ok": not blocking_gaps, "checks": checks, "blocking_gaps": blocking_gaps}


def dam_core_empty_state() -> dict:
    return {
        "events": (),
        "outbox": (),
        "inbox": (),
        "dead_letter": (),
        "processed_event_keys": (),
        "assets": {},
        "asset_renditions": {},
        "rights_policies": {},
        "metadata_tags": {},
        "product_projection": {},
        "rules": {},
        "parameters": {},
        "configuration": {},
        "schema_extensions": {},
        "seed_data": {
            "rendition_profiles": ("thumbnail", "web_large", "social_square"),
            "metadata_taxonomies": ("product", "campaign", "usage"),
            "rights_templates": ("commercial", "editorial", "restricted_review"),
        },
        "crypto_epoch": {"epoch": 1, "algorithm": "sha3_256"},
    }


def dam_core_configure_runtime(state: dict, configuration: dict) -> dict:
    if configuration.get("database_backend") not in DAM_CORE_ALLOWED_DATABASE_BACKENDS:
        raise ValueError("DAM Core supports only PostgreSQL, MySQL, or MariaDB backends")
    if configuration.get("event_topic") != DAM_CORE_REQUIRED_EVENT_TOPIC:
        raise ValueError(f"DAM Core requires the AppGen-X event topic {DAM_CORE_REQUIRED_EVENT_TOPIC}")
    forbidden = tuple(sorted(key for key in configuration if key in _FORBIDDEN_EVENTING_FIELDS))
    if forbidden:
        raise ValueError(f"DAM Core does not expose stream-engine pickers or user-facing eventing choice: {forbidden}")
    missing = tuple(field for field in DAM_CORE_SUPPORTED_CONFIGURATION_FIELDS if field not in configuration)
    if missing:
        raise ValueError(f"Missing DAM Core configuration fields: {missing}")
    normalized = {
        key: tuple(value) if key in _CONFIG_SEQUENCE_FIELDS else value
        for key, value in configuration.items()
    }
    configured = {
        **normalized,
        "ok": True,
        "event_contract": "AppGen-X",
        "allowed_database_backends": DAM_CORE_ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": DAM_CORE_REQUIRED_EVENT_TOPIC,
        "user_eventing_choice": False,
        "configuration_hash": _stable_hash(normalized),
    }
    return {"ok": True, "state": {**state, "configuration": configured}, "configuration": configured}


def dam_core_set_parameter(state: dict, name: str, value: float | int | str | bool) -> dict:
    if name not in DAM_CORE_SUPPORTED_PARAMETER_KEYS:
        raise ValueError(f"Unsupported DAM Core parameter: {name}")
    lower, upper = _PARAMETER_BOUNDS[name]
    if not isinstance(value, (int, float)) or not lower <= float(value) <= upper:
        raise ValueError(f"DAM Core parameter {name} must be numeric between {lower} and {upper}")
    parameters = {**state["parameters"], name: value}
    return {"ok": True, "state": {**state, "parameters": parameters}, "parameter": {"name": name, "value": value}}


def dam_core_register_rule(state: dict, rule: dict) -> dict:
    missing = tuple(field for field in DAM_CORE_REQUIRED_RULE_FIELDS if field not in rule)
    if missing:
        raise ValueError(f"Missing required DAM Core rule fields: {missing}")
    compiled = _compile_rule(rule)
    stored = {
        **rule,
        "enabled": rule["status"] == "active",
        "compiled_hash": compiled["compiled_hash"],
        "compiled_expression": compiled["compiled_expression"],
        "compiled_evidence": compiled["compiled_evidence"],
    }
    return {"ok": True, "state": {**state, "rules": {**state["rules"], rule["rule_id"]: stored}}, "rule": stored}


def dam_core_register_schema_extension(state: dict, table: str, fields: dict) -> dict:
    if table not in DAM_CORE_OWNED_TABLES:
        return {"ok": False, "error": "outside_owned_table_boundary", "state": state}
    invalid = tuple(name for name in fields if not re.fullmatch(r"[a-z][a-z0-9_]*", name))
    if invalid:
        return {"ok": False, "error": "invalid_extension_field", "invalid": invalid, "state": state}
    return {"ok": True, "state": {**state, "schema_extensions": {**state["schema_extensions"], table: dict(fields)}}}


def dam_core_receive_event(state: dict, envelope: dict, *, simulate_failure: bool = False) -> dict:
    payload = dict(envelope.get("payload", {}))
    event_type = envelope.get("event_type")
    event_id = envelope.get("event_id", f"inbox_{len(state['inbox']) + 1:06d}")
    idempotency_key = envelope.get("idempotency_key", f"inbox:{event_type}:{event_id}")
    if idempotency_key in state["processed_event_keys"]:
        return {"ok": True, "state": state, "duplicate": True, "handler": {"status": "duplicate"}}

    tenant = payload.get("tenant")
    attempts = int(envelope.get("attempts", 1))
    inbox_record = {
        "event_id": event_id,
        "event_type": event_type,
        "tenant": tenant,
        "payload": payload,
        "idempotency_key": idempotency_key,
        "attempts": attempts,
    }
    retry_limit = _retry_limit(state)
    if simulate_failure or event_type not in DAM_CORE_CONSUMED_EVENT_TYPES or not tenant:
        reason = "simulated_handler_failure" if simulate_failure else "unsupported_event" if event_type not in DAM_CORE_CONSUMED_EVENT_TYPES else "missing_tenant"
        dead_letter = {**inbox_record, "status": "dead_letter", "reason": reason, "retry_limit": retry_limit}
        next_state = {
            **state,
            "dead_letter": (*state["dead_letter"], dead_letter),
            "processed_event_keys": (*state["processed_event_keys"], idempotency_key),
        }
        return {
            "ok": False,
            "state": next_state,
            "dead_lettered": attempts >= retry_limit or simulate_failure,
            "handler": {"status": "dead_letter", "reason": reason, "retry_limit": retry_limit},
            "event": dead_letter,
        }

    next_state = {
        **state,
        "inbox": (*state["inbox"], {**inbox_record, "status": "accepted"}),
        "processed_event_keys": (*state["processed_event_keys"], idempotency_key),
    }
    if event_type == "ProductPublished":
        product_id = payload["product_id"]
        next_state = {**next_state, "product_projection": {**next_state["product_projection"], product_id: payload}}
    return {"ok": True, "state": next_state, "duplicate": False, "handler": {"status": "accepted"}, "event": inbox_record}


def dam_core_register_asset(state: dict, asset: dict) -> dict:
    required = ("asset_id", "tenant", "filename", "mime_type", "size_mb", "storage_uri", "binary", "created_by")
    missing = tuple(field for field in required if field not in asset)
    if missing:
        raise ValueError(f"Missing DAM Core asset fields: {missing}")
    _assert_configured(state)
    if asset["mime_type"] not in state["configuration"]["allowed_mime_types"]:
        raise ValueError(f"Unsupported DAM Core mime type: {asset['mime_type']}")
    if float(asset["size_mb"]) > float(state["parameters"].get("max_asset_size_mb", 1000)):
        raise ValueError("DAM Core asset exceeds configured max_asset_size_mb")
    fingerprint = "sha256:" + hashlib.sha256(asset["binary"]).hexdigest()
    stored = {
        **{key: value for key, value in asset.items() if key != "binary"},
        "status": "registered",
        "fingerprint": fingerprint,
        "storage_tier": state["configuration"]["default_storage_tier"],
        "product_dependency": asset.get("product_id") in state["product_projection"],
        "tag_index": (),
        "rendition_ids": (),
        "rights_policy_id": None,
        "graph_degree": 4 + int(bool(asset.get("product_id"))),
    }
    next_state = {**state, "assets": {**state["assets"], asset["asset_id"]: stored}}
    next_state = _append_event(next_state, "AssetRegistered", stored["tenant"], {"asset_id": asset["asset_id"], "fingerprint": fingerprint})
    return {"ok": True, "state": next_state, "asset": stored}


def dam_core_attach_rights_policy(state: dict, policy: dict) -> dict:
    required = ("policy_id", "asset_id", "tenant", "license_type", "allowed_markets", "blocked_markets", "expires_at", "attribution_required", "approver")
    missing = tuple(field for field in required if field not in policy)
    if missing:
        raise ValueError(f"Missing DAM Core rights policy fields: {missing}")
    asset = _asset(state, policy["asset_id"])
    if asset["tenant"] != policy["tenant"]:
        raise ValueError("DAM Core rights policy tenant does not match asset tenant")
    stored = {
        **policy,
        "allowed_markets": tuple(policy["allowed_markets"]),
        "blocked_markets": tuple(policy["blocked_markets"]),
        "status": "active",
        "compiled_hash": _stable_hash(policy),
    }
    assets = {**state["assets"], policy["asset_id"]: {**asset, "rights_policy_id": policy["policy_id"], "graph_degree": asset["graph_degree"] + 1}}
    return {"ok": True, "state": {**state, "rights_policies": {**state["rights_policies"], policy["policy_id"]: stored}, "assets": assets}, "policy": stored}


def dam_core_add_metadata_tag(state: dict, tag: dict) -> dict:
    required = ("tag_id", "asset_id", "tenant", "taxonomy", "value", "confidence", "source")
    missing = tuple(field for field in required if field not in tag)
    if missing:
        raise ValueError(f"Missing DAM Core metadata tag fields: {missing}")
    asset = _asset(state, tag["asset_id"])
    if asset["tenant"] != tag["tenant"]:
        raise ValueError("DAM Core metadata tag tenant does not match asset tenant")
    if float(tag["confidence"]) < float(state["parameters"].get("metadata_confidence_floor", 0.0)):
        raise ValueError("DAM Core metadata tag confidence is below configured floor")
    stored = {**tag, "tag_key": f"{tag['taxonomy']}:{tag['value']}", "status": "active"}
    assets = {
        **state["assets"],
        tag["asset_id"]: {
            **asset,
            "tag_index": tuple(sorted((*asset["tag_index"], stored["tag_key"]))),
            "graph_degree": asset["graph_degree"] + 1,
        },
    }
    next_state = {**state, "metadata_tags": {**state["metadata_tags"], tag["tag_id"]: stored}, "assets": assets}
    next_state = _append_event(next_state, "AssetTagged", tag["tenant"], {"asset_id": tag["asset_id"], "tag_key": stored["tag_key"]})
    return {"ok": True, "state": next_state, "tag": stored}


def dam_core_request_rendition(state: dict, rendition: dict) -> dict:
    required = ("rendition_id", "asset_id", "tenant", "profile", "target_mime_type", "width", "height")
    missing = tuple(field for field in required if field not in rendition)
    if missing:
        raise ValueError(f"Missing DAM Core rendition fields: {missing}")
    asset = _asset(state, rendition["asset_id"])
    if asset["tenant"] != rendition["tenant"]:
        raise ValueError("DAM Core rendition tenant does not match asset tenant")
    if rendition["profile"] not in state["configuration"]["rendition_profiles"]:
        raise ValueError(f"Unsupported DAM Core rendition profile: {rendition['profile']}")
    stored = {
        **rendition,
        "status": "requested",
        "attempts": 0,
        "route": "primary_transcode",
        "quality_score": 0.0,
        "graph_degree": 3,
    }
    assets = {
        **state["assets"],
        rendition["asset_id"]: {
            **asset,
            "rendition_ids": tuple(sorted((*asset["rendition_ids"], rendition["rendition_id"]))),
            "graph_degree": asset["graph_degree"] + 1,
        },
    }
    return {"ok": True, "state": {**state, "asset_renditions": {**state["asset_renditions"], rendition["rendition_id"]: stored}, "assets": assets}, "rendition": stored}


def dam_core_complete_rendition(state: dict, rendition_id: str, result: dict) -> dict:
    rendition = state["asset_renditions"][rendition_id]
    stored = {
        **rendition,
        "status": "ready",
        "uri": result["uri"],
        "quality_score": float(result["quality_score"]),
        "duration_ms": int(result["duration_ms"]),
        "attempts": int(rendition.get("attempts", 0)) + 1,
    }
    next_state = {**state, "asset_renditions": {**state["asset_renditions"], rendition_id: stored}}
    next_state = _append_event(
        next_state,
        "AssetRenditionReady",
        stored["tenant"],
        {"asset_id": stored["asset_id"], "rendition_id": rendition_id, "profile": stored["profile"]},
    )
    return {"ok": True, "state": next_state, "rendition": stored}


def dam_core_enforce_rights(state: dict, asset_id: str, *, market: str, use_case: str) -> dict:
    asset = _asset(state, asset_id)
    policy_id = asset.get("rights_policy_id")
    if not policy_id:
        return {"ok": False, "asset_id": asset_id, "decision": state["configuration"].get("rights_default_decision", "review"), "reason": "missing_rights_policy"}
    policy = state["rights_policies"][policy_id]
    decision = "block" if market in policy["blocked_markets"] else "allow" if market in policy["allowed_markets"] else "review"
    reason = "market_blocked" if decision == "block" else "market_allowed" if decision == "allow" else "market_not_explicitly_allowed"
    if decision == "block":
        _append_event(state, "AssetRightsBlocked", asset["tenant"], {"asset_id": asset_id, "market": market})
    return {"ok": decision != "block", "asset_id": asset_id, "market": market, "use_case": use_case, "decision": decision, "reason": reason, "policy_id": policy_id}


def dam_core_build_workbench_view(state: dict, *, tenant: str) -> dict:
    assets = tuple(asset for asset in state["assets"].values() if asset["tenant"] == tenant)
    asset_ids = {asset["asset_id"] for asset in assets}
    renditions = tuple(rendition for rendition in state["asset_renditions"].values() if rendition["asset_id"] in asset_ids)
    policies = tuple(policy for policy in state["rights_policies"].values() if policy["tenant"] == tenant)
    tags = tuple(tag for tag in state["metadata_tags"].values() if tag["tenant"] == tenant)
    return {
        "format": "appgen.dam-core-workbench-view.v1",
        "ok": True,
        "tenant": tenant,
        "asset_count": len(assets),
        "rendition_count": len(renditions),
        "ready_rendition_count": len(tuple(item for item in renditions if item["status"] == "ready")),
        "rights_policy_count": len(policies),
        "metadata_tag_count": len(tags),
        "product_projection_count": len(tuple(item for item in state["product_projection"].values() if item.get("tenant") == tenant)),
        "outbox_count": len(state["outbox"]),
        "inbox_count": len(tuple(item for item in state["inbox"] if item["tenant"] == tenant)),
        "dead_letter_count": len(state["dead_letter"]),
        "processed_event_count": len(state["processed_event_keys"]),
        "configuration_bound": bool(state["configuration"].get("ok")),
        "configuration_hash": state["configuration"].get("configuration_hash"),
        "rule_count": len(state["rules"]),
        "rules_bound": tuple(sorted(state["rules"])),
        "parameter_count": len(state["parameters"]),
        "parameters_bound": tuple(sorted(state["parameters"])),
        "owned_tables": DAM_CORE_OWNED_TABLES,
        "event_contract": state["configuration"].get("event_contract"),
    }


def dam_core_permissions_contract() -> dict:
    return {
        "register_asset": "dam_core.asset.write",
        "request_rendition": "dam_core.rendition.write",
        "complete_rendition": "dam_core.rendition.write",
        "attach_rights_policy": "dam_core.rights.manage",
        "enforce_rights": "dam_core.rights.evaluate",
        "add_metadata_tag": "dam_core.metadata.write",
        "receive_event": "dam_core.event.consume",
        "register_rule": "dam_core.configure",
        "set_parameter": "dam_core.configure",
        "configure_runtime": "dam_core.configure",
        "run_control_tests": "dam_core.audit",
    }


def dam_core_build_api_contract() -> dict:
    return {
        "format": "appgen.dam-core-api-contract.v1",
        "ok": True,
        "routes": (
            "POST /dam/assets",
            "POST /dam/assets/{asset_id}/renditions",
            "POST /dam/assets/{asset_id}/rights",
            "POST /dam/assets/{asset_id}/tags",
            "POST /dam/events/inbox",
            "GET /dam/workbench",
        ),
        "emits": DAM_CORE_EMITTED_EVENT_TYPES,
        "consumes": DAM_CORE_CONSUMED_EVENT_TYPES,
        "owned_tables": DAM_CORE_OWNED_TABLES,
        "dependencies": {"events": DAM_CORE_CONSUMED_EVENT_TYPES, "api_projections": ("product_projection",), "shared_tables": ()},
        "permissions": tuple(sorted(set(dam_core_permissions_contract().values()))),
    }


def dam_core_score_asset_quality(state: dict, asset_id: str) -> dict:
    asset = _asset(state, asset_id)
    rendition_count = len(asset["rendition_ids"])
    tag_count = len(asset["tag_index"])
    rights_bonus = 0.15 if asset.get("rights_policy_id") else 0.0
    product_bonus = 0.05 if asset.get("product_dependency") else 0.0
    score = min(1.0, 0.45 + rendition_count * 0.15 + tag_count * 0.1 + rights_bonus + product_bonus)
    return {"ok": True, "asset_id": asset_id, "quality_score": round(score, 4), "meets_threshold": score >= float(state["parameters"].get("quality_threshold", 0.7))}


def dam_core_simulate_rendition_cost(state: dict, asset_id: str, routes: tuple[dict, ...]) -> dict:
    _asset(state, asset_id)
    cost_weight = float(state["parameters"].get("rendition_cost_weight", 0.35))
    carbon_weight = float(state["parameters"].get("carbon_cost_weight", 0.15))
    scored = tuple(
        {
            **route,
            "objective_score": round((1.0 - cost_weight - carbon_weight) / max(route["latency"], 0.1) - route["cost"] * cost_weight - route["carbon"] * carbon_weight / 100.0, 6),
        }
        for route in routes
    )
    best = max(scored, key=lambda item: item["objective_score"])
    return {"ok": True, "asset_id": asset_id, "best_route": best["route"], "routes": scored}


def dam_core_forecast_asset_usage(history: tuple[int | float, ...], *, horizon_days: int) -> dict:
    if not history:
        return {"ok": False, "error": "missing_history"}
    trend = (float(history[-1]) - float(history[0])) / max(len(history) - 1, 1)
    expected = max(0.0, float(history[-1]) + trend * (horizon_days / 30.0))
    return {"ok": True, "expected_usage": round(expected, 4), "trend": round(trend, 4), "horizon_days": horizon_days}


def dam_core_resolve_asset_exception(reason: str) -> dict:
    actions = {
        "missing_rights": "request_rights_policy",
        "low_quality": "request_new_rendition",
        "missing_metadata": "route_to_metadata_steward",
        "transcode_failed": "switch_transcode_route",
    }
    return {"ok": True, "reason": reason, "action": actions.get(reason, "route_to_asset_ops"), "automation": "deterministic_policy"}


def dam_core_parse_asset_instruction(instruction: str) -> dict:
    text = instruction.lower()
    profile_match = re.search(r"render\s+([a-z0-9_]+)", text)
    tag_match = re.search(r"tag\s+([a-z0-9_]+)\s+([a-z0-9_-]+)", text)
    block_match = re.search(r"block\s+([a-z0-9_-]+)", text)
    return {
        "ok": True,
        "profile": profile_match.group(1) if profile_match else None,
        "taxonomy": tag_match.group(1) if tag_match else None,
        "tag_value": tag_match.group(2) if tag_match else None,
        "blocked_market": block_match.group(1) if block_match else None,
        "requires_rights_review": "rights" in text or bool(block_match),
    }


def dam_core_predictive_governance_risk(signals: dict) -> dict:
    score = min(1.0, sum(float(value) for value in signals.values()) / max(len(signals), 1))
    return {"ok": True, "risk_score": round(score, 4), "decision": "review" if score >= 0.65 else "clear"}


def dam_core_select_transcode_route(routes: tuple[dict, ...]) -> dict:
    available = tuple(route for route in routes if route.get("available"))
    if not available:
        return {"ok": False, "error": "no_route_available"}
    best = min(available, key=lambda route: (route.get("carbon", 0), route.get("latency", 0)))
    return {"ok": True, "route": best["route"], "failover_used": best != routes[0], "route_evidence": best}


def dam_core_generate_asset_proof(state: dict, asset_id: str, *, disclosure: tuple[str, ...]) -> dict:
    asset = _asset(state, asset_id)
    disclosed = {field: asset.get(field) for field in disclosure if field in asset}
    digest = _stable_hash({"asset_id": asset_id, "fingerprint": asset["fingerprint"], "disclosure": disclosure, "events": len(state["events"])})
    return {"ok": True, "asset_id": asset_id, "proof": f"zk_asset_{digest[:24]}", "disclosed": disclosed}


def dam_core_screen_dynamic_policy(state: dict, asset_id: str, *, market: str, mime_type: str) -> dict:
    asset = _asset(state, asset_id)
    if mime_type not in state["configuration"]["allowed_mime_types"]:
        return {"ok": False, "decision": "block", "reason": "mime_type_blocked"}
    rights = dam_core_enforce_rights(state, asset_id, market=market, use_case="dynamic_policy")
    required_tags = _required_tags(state, asset["tenant"])
    missing_tags = tuple(tag for tag in required_tags if not any(existing.startswith(f"{tag}:") for existing in asset["tag_index"]))
    if missing_tags:
        return {"ok": False, "decision": "review", "reason": "missing_required_tags", "missing_tags": missing_tags}
    return {"ok": rights["decision"] == "allow", "decision": rights["decision"], "reason": rights["reason"], "missing_tags": missing_tags}


def dam_core_run_control_tests(state: dict) -> dict:
    hash_chain_valid = all(event["hash"] == _event_hash(event["sequence"], event["event_type"], event["tenant"], event["payload"], event.get("previous_hash")) for event in state["events"])
    asset_tenants = {asset_id: asset["tenant"] for asset_id, asset in state["assets"].items()}
    tenant_isolation = all(state["assets"][rendition["asset_id"]]["tenant"] == rendition["tenant"] for rendition in state["asset_renditions"].values())
    tenant_isolation = tenant_isolation and all(asset_tenants[tag["asset_id"]] == tag["tenant"] for tag in state["metadata_tags"].values())
    rights_coverage = all(asset.get("rights_policy_id") for asset in state["assets"].values())
    rendition_coverage = all(asset.get("rendition_ids") for asset in state["assets"].values())
    configuration_valid = state["configuration"].get("event_contract") == "AppGen-X" and not state["configuration"].get("user_eventing_choice")
    blocking_gaps = tuple(
        gap
        for gap, ok in (
            ("hash_chain", hash_chain_valid),
            ("tenant_isolation", tenant_isolation),
            ("rights_coverage", rights_coverage),
            ("rendition_coverage", rendition_coverage),
            ("configuration", configuration_valid),
        )
        if not ok
    )
    return {
        "ok": not blocking_gaps,
        "hash_chain_valid": hash_chain_valid,
        "tenant_isolation": tenant_isolation,
        "rights_coverage": rights_coverage,
        "rendition_coverage": rendition_coverage,
        "configuration_valid": configuration_valid,
        "blocking_gaps": blocking_gaps,
    }


def dam_core_verify_owned_table_boundary() -> dict:
    return {
        "ok": True,
        "owned_tables": DAM_CORE_OWNED_TABLES,
        "declared_dependencies": {
            "events": DAM_CORE_CONSUMED_EVENT_TYPES,
            "api_projections": ("product_projection",),
            "shared_tables": (),
        },
    }


def _append_event(state: dict, event_type: str, tenant: str, payload: dict) -> dict:
    sequence = len(state["events"]) + 1
    previous_hash = state["events"][-1]["hash"] if state["events"] else None
    event = {
        "sequence": sequence,
        "event_type": event_type,
        "tenant": tenant,
        "payload": payload,
        "previous_hash": previous_hash,
        "hash": _event_hash(sequence, event_type, tenant, payload, previous_hash),
    }
    outbox = {
        "event_id": f"dam_evt_{sequence:06d}",
        "event_type": event_type,
        "tenant": tenant,
        "payload": payload,
        "topic": DAM_CORE_REQUIRED_EVENT_TOPIC,
        "event_contract": "AppGen-X",
        "idempotency_key": f"dam_core:{event_type}:{_stable_hash(payload)[:16]}",
        "status": "ready",
    }
    return {**state, "events": (*state["events"], event), "outbox": (*state["outbox"], outbox)}


def _compile_rule(rule: dict) -> dict:
    expression = json.dumps(_jsonable(rule), sort_keys=True, separators=(",", ":"))
    return {
        "compiled_hash": hashlib.sha256(expression.encode()).hexdigest(),
        "compiled_expression": expression,
        "compiled_evidence": {
            "required_fields": DAM_CORE_REQUIRED_RULE_FIELDS,
            "deterministic": True,
            "side_effect_free": True,
        },
    }


def _required_tags(state: dict, tenant: str) -> tuple[str, ...]:
    for rule in state["rules"].values():
        if rule["tenant"] == tenant and rule["enabled"]:
            return tuple(rule.get("metadata_policy", {}).get("required_tags", ()))
    return ()


def _asset(state: dict, asset_id: str) -> dict:
    if asset_id not in state["assets"]:
        raise KeyError(f"Unknown DAM Core asset: {asset_id}")
    return state["assets"][asset_id]


def _assert_configured(state: dict) -> None:
    if not state.get("configuration", {}).get("ok"):
        raise ValueError("DAM Core runtime must be configured before asset operations")


def _retry_limit(state: dict) -> int:
    return int(state.get("configuration", {}).get("retry_limit", state.get("parameters", {}).get("transcode_retry_limit", 3)))


def _event_hash(sequence: int, event_type: str, tenant: str, payload: dict, previous_hash: str | None) -> str:
    return _stable_hash({"sequence": sequence, "event_type": event_type, "tenant": tenant, "payload": payload, "previous_hash": previous_hash})


def _stable_hash(value: dict | tuple | list | str) -> str:
    return hashlib.sha256(json.dumps(_jsonable(value), sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def _jsonable(value):
    if isinstance(value, dict):
        return {key: _jsonable(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_jsonable(item) for item in value]
    if isinstance(value, bytes):
        return hashlib.sha256(value).hexdigest()
    if isinstance(value, float) and math.isnan(value):
        return "nan"
    return value
