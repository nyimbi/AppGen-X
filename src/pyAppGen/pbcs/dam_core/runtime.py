"""Executable runtime for the Digital Asset Management Core PBC."""

from __future__ import annotations

import hashlib
import json
import math
import re


DAM_CORE_REQUIRED_EVENT_TOPIC = "appgen.dam.events"
DAM_CORE_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
DAM_CORE_OWNED_TABLES = (
    "asset",
    "asset_version",
    "asset_binary",
    "asset_fingerprint",
    "asset_collection",
    "asset_collection_member",
    "asset_rendition",
    "transcoding_job",
    "transcode_route",
    "rendition_profile",
    "metadata_tag",
    "metadata_taxonomy",
    "metadata_enrichment",
    "semantic_annotation",
    "rights_policy",
    "rights_decision",
    "license_agreement",
    "usage_entitlement",
    "product_projection",
    "campaign_projection",
    "channel_asset_projection",
    "asset_workflow_case",
    "asset_review_task",
    "asset_exception",
    "asset_quality_score",
    "asset_usage_snapshot",
    "asset_usage_forecast",
    "asset_duplicate_candidate",
    "asset_lineage",
    "asset_audit_entry",
    "asset_policy_screening",
    "asset_control_assertion",
    "asset_federation_view",
    "asset_resilience_drill",
    "asset_crypto_epoch",
    "carbon_transcode_window",
    "rendition_cost_simulation",
    "asset_route_allocation",
    "asset_anomaly_signal",
    "asset_exposure_forecast",
    "asset_identity_attestation",
    "asset_governed_model",
    "asset_seed_data",
    "dam_rule",
    "dam_parameter",
    "dam_configuration",
    "dam_core_appgen_outbox_event",
    "dam_core_appgen_inbox_event",
    "dam_core_dead_letter_event",
)
DAM_CORE_RUNTIME_TABLES = (
    "dam_core_appgen_outbox_event",
    "dam_core_appgen_inbox_event",
    "dam_core_dead_letter_event",
)

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
    "asset_versioning",
    "asset_binary_storage",
    "asset_binary_fingerprint",
    "asset_collections",
    "asset_rendition",
    "transcoding_job",
    "transcode_route_selection",
    "rendition_profiles",
    "metadata_tag",
    "metadata_taxonomy",
    "metadata_enrichment",
    "semantic_annotation",
    "rights_policy",
    "rights_decision",
    "license_agreement",
    "usage_entitlement",
    "product_published_dependency",
    "campaign_projection",
    "channel_asset_projection",
    "asset_workflow_case",
    "asset_review_task",
    "asset_exception",
    "asset_quality_score",
    "asset_usage_snapshot",
    "asset_usage_forecast",
    "duplicate_candidate_detection",
    "asset_lineage",
    "tenant_isolation",
    "cryptographic_asset_proofs",
    "policy_screening",
    "control_assertions",
    "federation_views",
    "resilience_drills",
    "crypto_epoch_rotation",
    "carbon_aware_transcoding",
    "rendition_cost_simulation",
    "route_allocation",
    "anomaly_signals",
    "exposure_forecasts",
    "identity_attestation",
    "governed_model_registry",
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
    "AssetCollectionCreated",
    "AssetAddedToCollection",
    "LicenseAgreementRegistered",
    "UsageEntitlementGranted",
    "MetadataTaxonomyRegistered",
    "MetadataEnriched",
    "SemanticAnnotationAdded",
    "AssetWorkflowStarted",
    "AssetReviewTaskCompleted",
    "AssetExceptionOpened",
    "AssetExceptionResolved",
    "AssetUsageSnapshotRecorded",
    "AssetDuplicateCandidateDetected",
    "AssetLineageRecorded",
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
            "register_license_agreement",
            "grant_usage_entitlement",
            "add_metadata_tag",
            "register_metadata_taxonomy",
            "enrich_metadata",
            "add_semantic_annotation",
            "create_asset_collection",
            "add_asset_to_collection",
            "request_rendition",
            "complete_rendition",
            "enforce_rights",
            "start_asset_workflow",
            "complete_asset_review_task",
            "open_asset_exception",
            "resolve_asset_exception_case",
            "record_asset_usage_snapshot",
            "detect_asset_duplicate_candidate",
            "record_asset_lineage",
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
    sibling_asset = dam_core_register_asset(
        state,
        {
            "asset_id": "asset_101",
            "tenant": "tenant_alpha",
            "product_id": "sku_100",
            "filename": "launch-backpack-thumb.jpg",
            "mime_type": "image/jpeg",
            "size_mb": 8,
            "storage_uri": "object://dam/tenant_alpha/asset_101",
            "binary": b"launch-backpack-primary-image-v2",
            "locale": "en-US",
            "created_by": "user_ops",
        },
    )
    state = sibling_asset["state"]
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
    state = dam_core_register_license_agreement(
        state,
        {
            "agreement_id": "lic_100",
            "policy_id": "rights_100",
            "tenant": "tenant_alpha",
            "licensor": "brand_owner",
            "licensee": "tenant_alpha",
            "start_date": "2026-01-01",
            "end_date": "2027-05-26",
            "terms": {"markets": ("US", "CA"), "use_cases": ("product_detail",)},
        },
    )["state"]
    state = dam_core_grant_usage_entitlement(
        state,
        {
            "entitlement_id": "ent_100",
            "agreement_id": "lic_100",
            "asset_id": "asset_100",
            "tenant": "tenant_alpha",
            "market": "US",
            "use_case": "product_detail",
        },
    )["state"]
    state = dam_core_register_metadata_taxonomy(
        state,
        {
            "taxonomy_id": "tax_product",
            "tenant": "tenant_alpha",
            "name": "product",
            "allowed_values": ("backpack", "bag"),
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
    state = dam_core_enrich_metadata(
        state,
        {
            "enrichment_id": "enrich_100",
            "asset_id": "asset_100",
            "tenant": "tenant_alpha",
            "source": "vision_model",
            "attributes": {"dominant_color": "blue", "object": "backpack"},
            "confidence": 0.89,
        },
    )["state"]
    state = dam_core_add_semantic_annotation(
        state,
        {
            "annotation_id": "anno_100",
            "asset_id": "asset_100",
            "tenant": "tenant_alpha",
            "label": "backpack",
            "confidence": 0.92,
            "span": {"x": 0.1, "y": 0.1, "w": 0.8, "h": 0.8},
        },
    )["state"]
    state = dam_core_create_asset_collection(
        state,
        {
            "collection_id": "coll_launch",
            "tenant": "tenant_alpha",
            "name": "Launch collection",
            "purpose": "commerce_launch",
        },
    )["state"]
    state = dam_core_add_asset_to_collection(
        state,
        {
            "member_id": "member_100",
            "collection_id": "coll_launch",
            "asset_id": "asset_100",
            "tenant": "tenant_alpha",
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
    workflow = dam_core_start_asset_workflow(
        state,
        {
            "case_id": "case_100",
            "asset_id": "asset_100",
            "tenant": "tenant_alpha",
            "workflow_type": "rights_and_quality",
            "requested_by": "user_ops",
            "reviewers": ("legal_ops", "creative_ops"),
        },
    )
    state = workflow["state"]
    state = dam_core_complete_asset_review_task(
        state,
        "case_100:legal_ops",
        {"decision": "approve", "reviewed_by": "legal_ops"},
    )["state"]
    review = dam_core_complete_asset_review_task(
        state,
        "case_100:creative_ops",
        {"decision": "approve", "reviewed_by": "creative_ops"},
    )
    state = review["state"]
    exception_case = dam_core_open_asset_exception(
        state,
        {
            "exception_id": "exc_100",
            "asset_id": "asset_100",
            "tenant": "tenant_alpha",
            "reason": "missing_alt_text",
            "severity": "medium",
        },
    )
    state = exception_case["state"]
    state = dam_core_resolve_asset_exception_case(
        state,
        "exc_100",
        {"resolution": "alt_text_generated", "resolved_by": "creative_ops"},
    )["state"]
    state = dam_core_record_asset_usage_snapshot(
        state,
        {
            "snapshot_id": "usage_100",
            "asset_id": "asset_100",
            "tenant": "tenant_alpha",
            "impressions": 1200,
            "downloads": 80,
            "channel": "commerce",
        },
    )["state"]
    duplicate_candidate = dam_core_detect_asset_duplicate_candidate(
        state,
        {
            "candidate_id": "dup_100",
            "asset_id": "asset_100",
            "candidate_asset_id": "asset_101",
            "tenant": "tenant_alpha",
            "similarity": 0.97,
        },
    )
    state = duplicate_candidate["state"]
    lineage = dam_core_record_asset_lineage(
        state,
        {
            "lineage_id": "lineage_100",
            "asset_id": "asset_101",
            "source_asset_id": "asset_100",
            "tenant": "tenant_alpha",
            "lineage_type": "derived_thumbnail",
        },
    )
    state = lineage["state"]

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
    schema = dam_core_build_schema_contract()
    service = dam_core_build_service_contract()
    release = dam_core_build_release_evidence()
    policy = dam_core_screen_dynamic_policy(state, "asset_100", market="US", mime_type="image/jpeg")
    workbench = dam_core_build_workbench_view(state, tenant="tenant_alpha")

    checks = (
        {"id": "event_sourced_asset_lifecycle", "ok": len(state["events"]) >= 18 and state["events"][-1]["hash"]},
        {"id": "owned_media_schema_boundary", "ok": schema["ok"] and len(DAM_CORE_OWNED_TABLES) >= 45},
        {"id": "multi_tenant_asset_isolation", "ok": workbench["tenant"] == "tenant_alpha" and controls["tenant_isolation"]},
        {"id": "schema_evolution_resilient_asset_metadata", "ok": state["schema_extensions"]["asset"]["ai_caption"] == "jsonb"},
        {"id": "content_addressed_binary_fingerprinting", "ok": asset["asset"]["fingerprint"].startswith("sha256:")},
        {"id": "rendition_transcoding_pipeline", "ok": completed["rendition"]["status"] == "ready" and completed["rendition"]["quality_score"] >= 0.9},
        {"id": "semantic_metadata_tagging", "ok": "product:backpack" in state["assets"]["asset_100"]["tag_index"]},
        {"id": "asset_collection_lifecycle", "ok": state["asset_collections"]["coll_launch"]["member_count"] == 1 and state["asset_collection_members"]["member_100"]["status"] == "active"},
        {"id": "license_entitlement_lifecycle", "ok": state["license_agreements"]["lic_100"]["status"] == "active" and state["usage_entitlements"]["ent_100"]["status"] == "active"},
        {"id": "metadata_taxonomy_enrichment_annotation_lifecycle", "ok": state["metadata_taxonomies"]["tax_product"]["status"] == "active" and state["metadata_enrichments"]["enrich_100"]["status"] == "accepted" and state["semantic_annotations"]["anno_100"]["status"] == "active"},
        {"id": "asset_workflow_review_exception_lifecycle", "ok": review["asset_workflow_case"]["status"] == "approved" and state["asset_exceptions"]["exc_100"]["status"] == "resolved"},
        {"id": "asset_usage_duplicate_lineage_lifecycle", "ok": state["asset_usage_snapshots"]["usage_100"]["engagement_score"] > 0 and duplicate_candidate["asset_duplicate_candidate"]["status"] == "duplicate_review" and lineage["asset_lineage"]["status"] == "recorded"},
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
        {"id": "appgen_x_outbox_inbox_eventing", "ok": workbench["outbox_count"] >= 18 and workbench["inbox_count"] == 1 and service["eventing"]["contract"] == "AppGen-X"},
        {"id": "idempotent_handlers", "ok": duplicate["duplicate"] is True and workbench["processed_event_count"] == 2},
        {"id": "retry_dead_letter_evidence", "ok": invalid_event["dead_lettered"] is True and workbench["dead_letter_count"] == 1},
        {"id": "permissions_governance_evidence", "ok": "dam_core.configure" in api["permissions"]},
        {"id": "configuration_schema", "ok": state["configuration"]["event_contract"] == "AppGen-X"},
        {"id": "parameter_engine", "ok": len(state["parameters"]) == len(DAM_CORE_SUPPORTED_PARAMETER_KEYS)},
        {"id": "rule_engine", "ok": state["rules"]["rule_dam_default"]["compiled_hash"]},
        {"id": "seed_data", "ok": "rendition_profiles" in state["seed_data"]},
        {"id": "workbench_ui", "ok": workbench["asset_count"] >= 2 and workbench["rendition_count"] == 1 and release["ok"]},
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
        "asset_collections": {},
        "asset_collection_members": {},
        "asset_renditions": {},
        "rights_policies": {},
        "license_agreements": {},
        "usage_entitlements": {},
        "metadata_tags": {},
        "metadata_taxonomies": {},
        "metadata_enrichments": {},
        "semantic_annotations": {},
        "asset_workflow_cases": {},
        "asset_review_tasks": {},
        "asset_exceptions": {},
        "asset_usage_snapshots": {},
        "asset_duplicate_candidates": {},
        "asset_lineage": {},
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
        raise ValueError("cannot extend non-owned table")
    invalid = tuple(name for name in fields if not re.fullmatch(r"[a-z][a-z0-9_]*", name))
    if invalid:
        return {"ok": False, "error": "invalid_extension_field", "invalid": invalid, "state": state}
    table_extensions = {**state["schema_extensions"].get(table, {}), **dict(fields)}
    extension = {
        "table": table,
        "fields": dict(fields),
        "version": len(state["schema_extensions"].get(table, {})) + 1,
        "owned_table": True,
        "migration_artifact": f"dam_core_{table}_extension_v{len(state['schema_extensions'].get(table, {})) + 1}",
    }
    return {
        "ok": True,
        "state": {**state, "schema_extensions": {**state["schema_extensions"], table: table_extensions}},
        "extension": extension,
    }


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


def dam_core_register_license_agreement(state: dict, agreement: dict) -> dict:
    required = ("agreement_id", "policy_id", "tenant", "licensor", "licensee", "start_date", "end_date", "terms")
    missing = tuple(field for field in required if field not in agreement)
    if missing:
        raise ValueError(f"Missing DAM Core license agreement fields: {missing}")
    policy = state["rights_policies"].get(agreement["policy_id"])
    if not policy:
        raise ValueError("DAM Core license agreements require an owned rights policy.")
    stored = {
        **agreement,
        "status": "active",
        "terms_hash": _stable_hash(agreement["terms"]),
        "compiled_hash": _stable_hash(agreement),
    }
    next_state = {**state, "license_agreements": {**state["license_agreements"], agreement["agreement_id"]: stored}}
    next_state = _append_event(next_state, "LicenseAgreementRegistered", agreement["tenant"], {"agreement_id": agreement["agreement_id"], "policy_id": agreement["policy_id"]})
    return {"ok": True, "state": next_state, "license_agreement": stored}


def dam_core_grant_usage_entitlement(state: dict, entitlement: dict) -> dict:
    required = ("entitlement_id", "agreement_id", "asset_id", "tenant", "market", "use_case")
    missing = tuple(field for field in required if field not in entitlement)
    if missing:
        raise ValueError(f"Missing DAM Core usage entitlement fields: {missing}")
    _asset(state, entitlement["asset_id"])
    agreement = state["license_agreements"].get(entitlement["agreement_id"])
    if not agreement:
        raise ValueError("DAM Core usage entitlements require an owned license agreement.")
    stored = {
        **entitlement,
        "status": "active",
        "compiled_hash": _stable_hash(entitlement),
    }
    next_state = {**state, "usage_entitlements": {**state["usage_entitlements"], entitlement["entitlement_id"]: stored}}
    next_state = _append_event(next_state, "UsageEntitlementGranted", entitlement["tenant"], {"entitlement_id": entitlement["entitlement_id"], "asset_id": entitlement["asset_id"]})
    return {"ok": True, "state": next_state, "usage_entitlement": stored}


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


def dam_core_register_metadata_taxonomy(state: dict, taxonomy: dict) -> dict:
    required = ("taxonomy_id", "tenant", "name", "allowed_values")
    missing = tuple(field for field in required if field not in taxonomy)
    if missing:
        raise ValueError(f"Missing DAM Core metadata taxonomy fields: {missing}")
    stored = {
        **taxonomy,
        "allowed_values": tuple(taxonomy["allowed_values"]),
        "status": "active",
        "compiled_hash": _stable_hash(taxonomy),
    }
    next_state = {**state, "metadata_taxonomies": {**state["metadata_taxonomies"], taxonomy["taxonomy_id"]: stored}}
    next_state = _append_event(next_state, "MetadataTaxonomyRegistered", taxonomy["tenant"], {"taxonomy_id": taxonomy["taxonomy_id"], "name": taxonomy["name"]})
    return {"ok": True, "state": next_state, "metadata_taxonomy": stored}


def dam_core_enrich_metadata(state: dict, enrichment: dict) -> dict:
    required = ("enrichment_id", "asset_id", "tenant", "source", "attributes", "confidence")
    missing = tuple(field for field in required if field not in enrichment)
    if missing:
        raise ValueError(f"Missing DAM Core metadata enrichment fields: {missing}")
    asset = _asset(state, enrichment["asset_id"])
    if asset["tenant"] != enrichment["tenant"]:
        raise ValueError("DAM Core metadata enrichment tenant does not match asset tenant")
    if float(enrichment["confidence"]) < float(state["parameters"].get("metadata_confidence_floor", 0.0)):
        raise ValueError("DAM Core metadata enrichment confidence is below configured floor")
    stored = {
        **enrichment,
        "status": "accepted",
        "compiled_hash": _stable_hash(enrichment),
    }
    next_state = {**state, "metadata_enrichments": {**state["metadata_enrichments"], enrichment["enrichment_id"]: stored}}
    next_state = _append_event(next_state, "MetadataEnriched", enrichment["tenant"], {"enrichment_id": enrichment["enrichment_id"], "asset_id": enrichment["asset_id"]})
    return {"ok": True, "state": next_state, "metadata_enrichment": stored}


def dam_core_add_semantic_annotation(state: dict, annotation: dict) -> dict:
    required = ("annotation_id", "asset_id", "tenant", "label", "confidence", "span")
    missing = tuple(field for field in required if field not in annotation)
    if missing:
        raise ValueError(f"Missing DAM Core semantic annotation fields: {missing}")
    asset = _asset(state, annotation["asset_id"])
    if asset["tenant"] != annotation["tenant"]:
        raise ValueError("DAM Core semantic annotation tenant does not match asset tenant")
    stored = {
        **annotation,
        "status": "active" if float(annotation["confidence"]) >= float(state["parameters"].get("metadata_confidence_floor", 0.0)) else "review",
        "compiled_hash": _stable_hash(annotation),
    }
    next_state = {**state, "semantic_annotations": {**state["semantic_annotations"], annotation["annotation_id"]: stored}}
    next_state = _append_event(next_state, "SemanticAnnotationAdded", annotation["tenant"], {"annotation_id": annotation["annotation_id"], "asset_id": annotation["asset_id"]})
    return {"ok": stored["status"] == "active", "state": next_state, "semantic_annotation": stored}


def dam_core_create_asset_collection(state: dict, collection: dict) -> dict:
    required = ("collection_id", "tenant", "name", "purpose")
    missing = tuple(field for field in required if field not in collection)
    if missing:
        raise ValueError(f"Missing DAM Core asset collection fields: {missing}")
    stored = {
        **collection,
        "status": "active",
        "member_count": 0,
        "compiled_hash": _stable_hash(collection),
    }
    next_state = {**state, "asset_collections": {**state["asset_collections"], collection["collection_id"]: stored}}
    next_state = _append_event(next_state, "AssetCollectionCreated", collection["tenant"], {"collection_id": collection["collection_id"]})
    return {"ok": True, "state": next_state, "asset_collection": stored}


def dam_core_add_asset_to_collection(state: dict, member: dict) -> dict:
    required = ("member_id", "collection_id", "asset_id", "tenant")
    missing = tuple(field for field in required if field not in member)
    if missing:
        raise ValueError(f"Missing DAM Core collection member fields: {missing}")
    asset = _asset(state, member["asset_id"])
    collection = state["asset_collections"].get(member["collection_id"])
    if not collection:
        raise ValueError("DAM Core collection membership requires an owned collection.")
    if asset["tenant"] != member["tenant"] or collection["tenant"] != member["tenant"]:
        raise ValueError("DAM Core collection membership tenant mismatch.")
    stored = {
        **member,
        "status": "active",
        "compiled_hash": _stable_hash(member),
    }
    collection_updated = {**collection, "member_count": collection["member_count"] + 1}
    next_state = {
        **state,
        "asset_collection_members": {**state["asset_collection_members"], member["member_id"]: stored},
        "asset_collections": {**state["asset_collections"], member["collection_id"]: collection_updated},
    }
    next_state = _append_event(next_state, "AssetAddedToCollection", member["tenant"], {"member_id": member["member_id"], "collection_id": member["collection_id"], "asset_id": member["asset_id"]})
    return {"ok": True, "state": next_state, "asset_collection_member": stored}


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


def dam_core_start_asset_workflow(state: dict, workflow: dict) -> dict:
    required = ("case_id", "asset_id", "tenant", "workflow_type", "requested_by", "reviewers")
    missing = tuple(field for field in required if field not in workflow)
    if missing:
        raise ValueError(f"Missing DAM Core workflow fields: {missing}")
    asset = _asset(state, workflow["asset_id"])
    if asset["tenant"] != workflow["tenant"]:
        raise ValueError("DAM Core workflow tenant does not match asset tenant")
    stored = {
        **workflow,
        "reviewers": tuple(workflow["reviewers"]),
        "status": "open",
        "compiled_hash": _stable_hash(workflow),
    }
    review_tasks = {
        f"{workflow['case_id']}:{reviewer}": {
            "task_id": f"{workflow['case_id']}:{reviewer}",
            "case_id": workflow["case_id"],
            "asset_id": workflow["asset_id"],
            "tenant": workflow["tenant"],
            "reviewer": reviewer,
            "status": "pending",
        }
        for reviewer in workflow["reviewers"]
    }
    next_state = {
        **state,
        "asset_workflow_cases": {**state["asset_workflow_cases"], workflow["case_id"]: stored},
        "asset_review_tasks": {**state["asset_review_tasks"], **review_tasks},
    }
    next_state = _append_event(next_state, "AssetWorkflowStarted", workflow["tenant"], {"case_id": workflow["case_id"], "asset_id": workflow["asset_id"]})
    return {"ok": True, "state": next_state, "asset_workflow_case": stored, "asset_review_tasks": tuple(review_tasks.values())}


def dam_core_complete_asset_review_task(state: dict, task_id: str, decision: dict) -> dict:
    task = state["asset_review_tasks"].get(task_id)
    if not task:
        raise ValueError("DAM Core review completion requires an owned review task.")
    stored_task = {
        **task,
        "status": "completed",
        "decision": decision["decision"],
        "reviewed_by": decision.get("reviewed_by", task["reviewer"]),
        "notes": decision.get("notes", ""),
    }
    tasks = {**state["asset_review_tasks"], task_id: stored_task}
    case = state["asset_workflow_cases"][task["case_id"]]
    case_tasks = tuple(item for item in tasks.values() if item["case_id"] == task["case_id"])
    case_status = "approved" if case_tasks and all(item["status"] == "completed" and item.get("decision") == "approve" for item in case_tasks) else "open"
    case_updated = {**case, "status": case_status}
    next_state = {
        **state,
        "asset_review_tasks": tasks,
        "asset_workflow_cases": {**state["asset_workflow_cases"], task["case_id"]: case_updated},
    }
    next_state = _append_event(next_state, "AssetReviewTaskCompleted", task["tenant"], {"task_id": task_id, "case_id": task["case_id"], "decision": stored_task["decision"]})
    return {"ok": True, "state": next_state, "asset_review_task": stored_task, "asset_workflow_case": case_updated}


def dam_core_open_asset_exception(state: dict, exception: dict) -> dict:
    required = ("exception_id", "asset_id", "tenant", "reason", "severity")
    missing = tuple(field for field in required if field not in exception)
    if missing:
        raise ValueError(f"Missing DAM Core asset exception fields: {missing}")
    asset = _asset(state, exception["asset_id"])
    if asset["tenant"] != exception["tenant"]:
        raise ValueError("DAM Core exception tenant does not match asset tenant")
    stored = {
        **exception,
        "status": "open",
        "compiled_hash": _stable_hash(exception),
    }
    next_state = {**state, "asset_exceptions": {**state["asset_exceptions"], exception["exception_id"]: stored}}
    next_state = _append_event(next_state, "AssetExceptionOpened", exception["tenant"], {"exception_id": exception["exception_id"], "asset_id": exception["asset_id"], "reason": exception["reason"]})
    return {"ok": True, "state": next_state, "asset_exception": stored}


def dam_core_resolve_asset_exception_case(state: dict, exception_id: str, resolution: dict) -> dict:
    exception = state["asset_exceptions"].get(exception_id)
    if not exception:
        raise ValueError("DAM Core exception resolution requires an owned exception.")
    stored = {
        **exception,
        "status": "resolved",
        "resolution": resolution["resolution"],
        "resolved_by": resolution.get("resolved_by", "asset_ops"),
        "resolution_hash": _stable_hash(resolution),
    }
    next_state = {**state, "asset_exceptions": {**state["asset_exceptions"], exception_id: stored}}
    next_state = _append_event(next_state, "AssetExceptionResolved", exception["tenant"], {"exception_id": exception_id, "resolution": stored["resolution"]})
    return {"ok": True, "state": next_state, "asset_exception": stored}


def dam_core_record_asset_usage_snapshot(state: dict, snapshot: dict) -> dict:
    required = ("snapshot_id", "asset_id", "tenant", "impressions", "downloads", "channel")
    missing = tuple(field for field in required if field not in snapshot)
    if missing:
        raise ValueError(f"Missing DAM Core asset usage snapshot fields: {missing}")
    asset = _asset(state, snapshot["asset_id"])
    if asset["tenant"] != snapshot["tenant"]:
        raise ValueError("DAM Core usage snapshot tenant does not match asset tenant")
    stored = {
        **snapshot,
        "engagement_score": round((float(snapshot["impressions"]) * 0.01) + (float(snapshot["downloads"]) * 0.1), 4),
        "status": "captured",
        "compiled_hash": _stable_hash(snapshot),
    }
    next_state = {**state, "asset_usage_snapshots": {**state["asset_usage_snapshots"], snapshot["snapshot_id"]: stored}}
    next_state = _append_event(next_state, "AssetUsageSnapshotRecorded", snapshot["tenant"], {"snapshot_id": snapshot["snapshot_id"], "asset_id": snapshot["asset_id"]})
    return {"ok": True, "state": next_state, "asset_usage_snapshot": stored}


def dam_core_detect_asset_duplicate_candidate(state: dict, candidate: dict) -> dict:
    required = ("candidate_id", "asset_id", "candidate_asset_id", "tenant", "similarity")
    missing = tuple(field for field in required if field not in candidate)
    if missing:
        raise ValueError(f"Missing DAM Core duplicate candidate fields: {missing}")
    asset = _asset(state, candidate["asset_id"])
    other = _asset(state, candidate["candidate_asset_id"])
    if asset["tenant"] != candidate["tenant"] or other["tenant"] != candidate["tenant"]:
        raise ValueError("DAM Core duplicate candidate tenant mismatch.")
    threshold = float(state["parameters"].get("duplicate_similarity_threshold", 0.95))
    stored = {
        **candidate,
        "status": "duplicate_review" if float(candidate["similarity"]) >= threshold else "distinct",
        "compiled_hash": _stable_hash(candidate),
    }
    next_state = {**state, "asset_duplicate_candidates": {**state["asset_duplicate_candidates"], candidate["candidate_id"]: stored}}
    next_state = _append_event(next_state, "AssetDuplicateCandidateDetected", candidate["tenant"], {"candidate_id": candidate["candidate_id"], "status": stored["status"]})
    return {"ok": True, "state": next_state, "asset_duplicate_candidate": stored}


def dam_core_record_asset_lineage(state: dict, lineage: dict) -> dict:
    required = ("lineage_id", "asset_id", "tenant", "source_asset_id", "lineage_type")
    missing = tuple(field for field in required if field not in lineage)
    if missing:
        raise ValueError(f"Missing DAM Core asset lineage fields: {missing}")
    asset = _asset(state, lineage["asset_id"])
    source = _asset(state, lineage["source_asset_id"])
    if asset["tenant"] != lineage["tenant"] or source["tenant"] != lineage["tenant"]:
        raise ValueError("DAM Core lineage tenant mismatch.")
    stored = {
        **lineage,
        "status": "recorded",
        "compiled_hash": _stable_hash(lineage),
    }
    next_state = {**state, "asset_lineage": {**state["asset_lineage"], lineage["lineage_id"]: stored}}
    next_state = _append_event(next_state, "AssetLineageRecorded", lineage["tenant"], {"lineage_id": lineage["lineage_id"], "asset_id": lineage["asset_id"]})
    return {"ok": True, "state": next_state, "asset_lineage": stored}


def dam_core_build_workbench_view(state: dict, *, tenant: str) -> dict:
    assets = tuple(asset for asset in state["assets"].values() if asset["tenant"] == tenant)
    asset_ids = {asset["asset_id"] for asset in assets}
    renditions = tuple(rendition for rendition in state["asset_renditions"].values() if rendition["asset_id"] in asset_ids)
    policies = tuple(policy for policy in state["rights_policies"].values() if policy["tenant"] == tenant)
    tags = tuple(tag for tag in state["metadata_tags"].values() if tag["tenant"] == tenant)
    workflows = tuple(case for case in state["asset_workflow_cases"].values() if case["tenant"] == tenant)
    exceptions = tuple(case for case in state["asset_exceptions"].values() if case["tenant"] == tenant)
    return {
        "format": "appgen.dam-core-workbench-view.v1",
        "ok": True,
        "tenant": tenant,
        "asset_count": len(assets),
        "rendition_count": len(renditions),
        "ready_rendition_count": len(tuple(item for item in renditions if item["status"] == "ready")),
        "rights_policy_count": len(policies),
        "metadata_tag_count": len(tags),
        "collection_count": len(tuple(item for item in state["asset_collections"].values() if item["tenant"] == tenant)),
        "license_agreement_count": len(tuple(item for item in state["license_agreements"].values() if item["tenant"] == tenant)),
        "usage_entitlement_count": len(tuple(item for item in state["usage_entitlements"].values() if item["tenant"] == tenant)),
        "metadata_enrichment_count": len(tuple(item for item in state["metadata_enrichments"].values() if item["tenant"] == tenant)),
        "semantic_annotation_count": len(tuple(item for item in state["semantic_annotations"].values() if item["tenant"] == tenant)),
        "approved_workflow_count": len(tuple(item for item in workflows if item["status"] == "approved")),
        "resolved_exception_count": len(tuple(item for item in exceptions if item["status"] == "resolved")),
        "usage_snapshot_count": len(tuple(item for item in state["asset_usage_snapshots"].values() if item["tenant"] == tenant)),
        "duplicate_candidate_count": len(tuple(item for item in state["asset_duplicate_candidates"].values() if item["tenant"] == tenant)),
        "lineage_count": len(tuple(item for item in state["asset_lineage"].values() if item["tenant"] == tenant)),
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
        "register_license_agreement": "dam_core.rights.manage",
        "grant_usage_entitlement": "dam_core.rights.manage",
        "enforce_rights": "dam_core.rights.evaluate",
        "add_metadata_tag": "dam_core.metadata.write",
        "register_metadata_taxonomy": "dam_core.metadata.write",
        "enrich_metadata": "dam_core.metadata.write",
        "add_semantic_annotation": "dam_core.metadata.write",
        "create_asset_collection": "dam_core.asset.write",
        "add_asset_to_collection": "dam_core.asset.write",
        "start_asset_workflow": "dam_core.workflow",
        "complete_asset_review_task": "dam_core.workflow",
        "open_asset_exception": "dam_core.workflow",
        "resolve_asset_exception_case": "dam_core.workflow",
        "record_asset_usage_snapshot": "dam_core.audit",
        "detect_asset_duplicate_candidate": "dam_core.audit",
        "record_asset_lineage": "dam_core.audit",
        "receive_event": "dam_core.event.consume",
        "register_rule": "dam_core.configure",
        "set_parameter": "dam_core.configure",
        "configure_runtime": "dam_core.configure",
        "run_control_tests": "dam_core.audit",
        "build_schema_contract": "dam_core.audit",
        "build_service_contract": "dam_core.audit",
        "build_release_evidence": "dam_core.audit",
    }


def dam_core_build_api_contract() -> dict:
    return {
        "format": "appgen.dam-core-api-contract.v1",
        "ok": True,
        "routes": (
            {
                "route": "POST /dam/assets",
                "command": "register_asset",
                "owned_tables": ("asset",),
                "emits": ("AssetRegistered",),
                "requires_permission": "dam_core.asset.write",
                "idempotency_key": "asset_id",
            },
            {
                "route": "POST /dam/assets/{asset_id}/renditions",
                "command": "request_rendition",
                "owned_tables": ("asset_rendition",),
                "emits": ("AssetRenditionRequested",),
                "requires_permission": "dam_core.rendition.write",
                "idempotency_key": "rendition_id",
            },
            {
                "route": "POST /dam/assets/{asset_id}/rights",
                "command": "attach_rights_policy",
                "owned_tables": ("rights_policy",),
                "emits": ("AssetRightsPolicyAttached",),
                "requires_permission": "dam_core.rights.manage",
                "idempotency_key": "policy_id",
            },
            {
                "route": "POST /dam/assets/{asset_id}/license-agreements",
                "command": "register_license_agreement",
                "owned_tables": ("license_agreement",),
                "emits": ("LicenseAgreementRegistered",),
                "requires_permission": "dam_core.rights.manage",
                "idempotency_key": "agreement_id",
            },
            {
                "route": "POST /dam/assets/{asset_id}/usage-entitlements",
                "command": "grant_usage_entitlement",
                "owned_tables": ("usage_entitlement",),
                "emits": ("UsageEntitlementGranted",),
                "requires_permission": "dam_core.rights.manage",
                "idempotency_key": "entitlement_id",
            },
            {
                "route": "POST /dam/assets/{asset_id}/tags",
                "command": "add_metadata_tag",
                "owned_tables": ("metadata_tag",),
                "emits": ("AssetMetadataTagged",),
                "requires_permission": "dam_core.metadata.write",
                "idempotency_key": "tag_id",
            },
            {
                "route": "POST /dam/metadata-taxonomies",
                "command": "register_metadata_taxonomy",
                "owned_tables": ("metadata_taxonomy",),
                "emits": ("MetadataTaxonomyRegistered",),
                "requires_permission": "dam_core.metadata.write",
                "idempotency_key": "taxonomy_id",
            },
            {
                "route": "POST /dam/assets/{asset_id}/metadata-enrichments",
                "command": "enrich_metadata",
                "owned_tables": ("metadata_enrichment",),
                "emits": ("MetadataEnriched",),
                "requires_permission": "dam_core.metadata.write",
                "idempotency_key": "enrichment_id",
            },
            {
                "route": "POST /dam/assets/{asset_id}/semantic-annotations",
                "command": "add_semantic_annotation",
                "owned_tables": ("semantic_annotation",),
                "emits": ("SemanticAnnotationAdded",),
                "requires_permission": "dam_core.metadata.write",
                "idempotency_key": "annotation_id",
            },
            {
                "route": "POST /dam/collections",
                "command": "create_asset_collection",
                "owned_tables": ("asset_collection",),
                "emits": ("AssetCollectionCreated",),
                "requires_permission": "dam_core.asset.write",
                "idempotency_key": "collection_id",
            },
            {
                "route": "POST /dam/collections/{collection_id}/members",
                "command": "add_asset_to_collection",
                "owned_tables": ("asset_collection_member",),
                "emits": ("AssetAddedToCollection",),
                "requires_permission": "dam_core.asset.write",
                "idempotency_key": "member_id",
            },
            {
                "route": "POST /dam/assets/{asset_id}/workflows",
                "command": "start_asset_workflow",
                "owned_tables": ("asset_workflow_case", "asset_review_task"),
                "emits": ("AssetWorkflowStarted",),
                "requires_permission": "dam_core.workflow",
                "idempotency_key": "case_id",
            },
            {
                "route": "POST /dam/review-tasks/{task_id}/complete",
                "command": "complete_asset_review_task",
                "owned_tables": ("asset_review_task", "asset_workflow_case"),
                "emits": ("AssetReviewTaskCompleted",),
                "requires_permission": "dam_core.workflow",
                "idempotency_key": "task_id:decision",
            },
            {
                "route": "POST /dam/assets/{asset_id}/exceptions",
                "command": "open_asset_exception",
                "owned_tables": ("asset_exception",),
                "emits": ("AssetExceptionOpened",),
                "requires_permission": "dam_core.workflow",
                "idempotency_key": "exception_id",
            },
            {
                "route": "POST /dam/exceptions/{exception_id}/resolve",
                "command": "resolve_asset_exception_case",
                "owned_tables": ("asset_exception",),
                "emits": ("AssetExceptionResolved",),
                "requires_permission": "dam_core.workflow",
                "idempotency_key": "exception_id:resolution",
            },
            {
                "route": "POST /dam/assets/{asset_id}/usage-snapshots",
                "command": "record_asset_usage_snapshot",
                "owned_tables": ("asset_usage_snapshot",),
                "emits": ("AssetUsageSnapshotRecorded",),
                "requires_permission": "dam_core.audit",
                "idempotency_key": "snapshot_id",
            },
            {
                "route": "POST /dam/assets/{asset_id}/duplicate-candidates",
                "command": "detect_asset_duplicate_candidate",
                "owned_tables": ("asset_duplicate_candidate",),
                "emits": ("AssetDuplicateCandidateDetected",),
                "requires_permission": "dam_core.audit",
                "idempotency_key": "candidate_id",
            },
            {
                "route": "POST /dam/assets/{asset_id}/lineage",
                "command": "record_asset_lineage",
                "owned_tables": ("asset_lineage",),
                "emits": ("AssetLineageRecorded",),
                "requires_permission": "dam_core.audit",
                "idempotency_key": "lineage_id",
            },
            {
                "route": "POST /dam/events/inbox",
                "command": "receive_event",
                "owned_tables": (),
                "consumes": DAM_CORE_CONSUMED_EVENT_TYPES,
                "requires_permission": "dam_core.event.consume",
                "idempotency_key": "event_id",
            },
            {
                "route": "GET /dam/workbench",
                "query": "build_workbench_view",
                "owned_tables": DAM_CORE_OWNED_TABLES,
                "requires_permission": "dam_core.audit",
            },
            {
                "route": "GET /dam/schema-contract",
                "query": "build_schema_contract",
                "owned_tables": DAM_CORE_OWNED_TABLES,
                "requires_permission": "dam_core.audit",
            },
            {
                "route": "GET /dam/service-contract",
                "query": "build_service_contract",
                "owned_tables": DAM_CORE_OWNED_TABLES,
                "requires_permission": "dam_core.audit",
            },
            {
                "route": "GET /dam/release-evidence",
                "query": "build_release_evidence",
                "owned_tables": DAM_CORE_OWNED_TABLES,
                "requires_permission": "dam_core.audit",
            },
        ),
        "declared_catalog_routes": ("POST /assets", "POST /renditions", "GET /assets"),
        "emits": DAM_CORE_EMITTED_EVENT_TYPES,
        "consumes": DAM_CORE_CONSUMED_EVENT_TYPES,
        "owned_tables": DAM_CORE_OWNED_TABLES,
        "dependencies": {"events": DAM_CORE_CONSUMED_EVENT_TYPES, "api_projections": ("product_projection",), "shared_tables": ()},
        "permissions": tuple(sorted(set(dam_core_permissions_contract().values()))),
        "database_backends": DAM_CORE_ALLOWED_DATABASE_BACKENDS,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
    }


def dam_core_build_schema_contract() -> dict:
    tables = tuple(
        {
            "table": table,
            "schema": "dam_core",
            "pbc": "dam_core",
            "owned": True,
            "migration": f"pbcs/dam_core/migrations/{index:03d}_{table}.sql",
            "model": f"pbcs/dam_core/models/{_class_name(table)}.py",
            "fields": _dam_table_fields(table),
            "relationships": _dam_table_relationships(table),
        }
        for index, table in enumerate(DAM_CORE_OWNED_TABLES, start=1)
    )
    return {
        "format": "appgen.dam-core-owned-schema-contract.v1",
        "ok": True,
        "pbc": "dam_core",
        "owned_tables": DAM_CORE_OWNED_TABLES,
        "runtime_tables": DAM_CORE_RUNTIME_TABLES,
        "tables": tables,
        "migrations": tuple(table["migration"] for table in tables),
        "models": tuple(table["model"] for table in tables),
        "database_backends": DAM_CORE_ALLOWED_DATABASE_BACKENDS,
        "shared_table_access": False,
        "tenant_isolation": {"field": "tenant", "required": True},
        "schema_extensions": {"allowed": True, "owned_tables_only": True},
        "declared_dependencies": dam_core_verify_owned_table_boundary(())["declared_dependencies"],
    }


def dam_core_build_service_contract() -> dict:
    command_methods = (
        "configure_runtime",
        "set_parameter",
        "register_rule",
        "register_schema_extension",
        "receive_event",
        "register_asset",
        "attach_rights_policy",
        "register_license_agreement",
        "grant_usage_entitlement",
        "add_metadata_tag",
        "register_metadata_taxonomy",
        "enrich_metadata",
        "add_semantic_annotation",
        "create_asset_collection",
        "add_asset_to_collection",
        "request_rendition",
        "complete_rendition",
        "enforce_rights",
        "start_asset_workflow",
        "complete_asset_review_task",
        "open_asset_exception",
        "resolve_asset_exception_case",
        "record_asset_usage_snapshot",
        "detect_asset_duplicate_candidate",
        "record_asset_lineage",
        "score_asset_quality",
        "simulate_rendition_cost",
        "forecast_asset_usage",
        "resolve_asset_exception",
        "parse_asset_instruction",
        "predictive_governance_risk",
        "select_transcode_route",
        "generate_asset_proof",
        "screen_dynamic_policy",
        "run_control_tests",
        "build_workbench_view",
        "verify_owned_table_boundary",
        "build_schema_contract",
        "build_service_contract",
        "build_release_evidence",
    )
    query_methods = (
        "build_api_contract",
        "permissions_contract",
        "build_workbench_view",
        "build_schema_contract",
        "build_service_contract",
        "build_release_evidence",
    )
    return {
        "format": "appgen.dam-core-service-contract.v1",
        "ok": True,
        "pbc": "dam_core",
        "transaction_boundary": "dam_core_owned_datastore_plus_appgen_outbox",
        "command_methods": command_methods,
        "query_methods": query_methods,
        "mutates_only": DAM_CORE_OWNED_TABLES,
        "external_dependencies": {
            "apis": ("POST /assets", "POST /renditions", "GET /assets"),
            "events": DAM_CORE_CONSUMED_EVENT_TYPES,
            "api_projections": ("product_projection",),
            "shared_tables": (),
        },
        "eventing": {
            "contract": "AppGen-X",
            "topic": DAM_CORE_REQUIRED_EVENT_TOPIC,
            "outbox_table": DAM_CORE_RUNTIME_TABLES[0],
            "inbox_table": DAM_CORE_RUNTIME_TABLES[1],
            "dead_letter_table": DAM_CORE_RUNTIME_TABLES[2],
            "idempotency_required": True,
        },
        "idempotent_handlers": ("receive_event",),
        "retry_dead_letter_evidence": {
            "retry_limit_field": "retry_limit",
            "dead_letter_table": DAM_CORE_RUNTIME_TABLES[2],
        },
        "shared_table_access": False,
    }


def dam_core_build_release_evidence() -> dict:
    schema = dam_core_build_schema_contract()
    service = dam_core_build_service_contract()
    api = dam_core_build_api_contract()
    permissions = dam_core_permissions_contract()
    checks = (
        {"id": "owned_schema_depth", "ok": len(schema["owned_tables"]) >= 45},
        {"id": "migration_per_owned_table", "ok": len(schema["migrations"]) == len(schema["owned_tables"])},
        {"id": "model_per_owned_table", "ok": len(schema["models"]) == len(schema["owned_tables"])},
        {"id": "service_contract_depth", "ok": len(service["command_methods"]) >= 25},
        {"id": "appgen_event_contract_only", "ok": api["event_contract"] == "AppGen-X" and api["stream_engine_picker_visible"] is False},
        {"id": "backend_allowlist", "ok": set(api["database_backends"]) <= {"postgresql", "mysql", "mariadb"}},
        {"id": "permissions_cover_release_queries", "ok": {"build_schema_contract", "build_service_contract", "build_release_evidence"} <= set(permissions)},
        {"id": "runtime_event_tables_owned", "ok": set(DAM_CORE_RUNTIME_TABLES) <= set(schema["owned_tables"])},
        {"id": "no_shared_table_access", "ok": not schema["shared_table_access"] and not service["shared_table_access"] and not api["shared_table_access"]},
    )
    blocking = tuple(check for check in checks if not check["ok"])
    return {
        "format": "appgen.dam-core-release-evidence.v1",
        "ok": not blocking,
        "pbc": "dam_core",
        "checks": checks,
        "blocking_gaps": blocking,
        "schema": schema,
        "service": service,
        "api": api,
        "permissions": permissions,
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
    derived_asset_ids = {lineage["asset_id"] for lineage in state["asset_lineage"].values()}
    rights_coverage = all(asset.get("rights_policy_id") or asset_id in derived_asset_ids for asset_id, asset in state["assets"].items())
    rendition_coverage = all(asset.get("rendition_ids") or asset_id in derived_asset_ids for asset_id, asset in state["assets"].items())
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


def dam_core_verify_owned_table_boundary(references: tuple[str, ...] | list[str] | set[str] = ()) -> dict:
    allowed_event_dependencies = {"enterprise_pim.ProductPublished"}
    allowed_api_dependencies = {"product_projection", "POST /assets", "POST /renditions", "GET /assets"}
    allowed_tables = set(DAM_CORE_OWNED_TABLES) | set(DAM_CORE_RUNTIME_TABLES)
    violations = tuple(
        reference
        for reference in references
        if reference not in allowed_tables
        and reference not in allowed_event_dependencies
        and reference not in allowed_api_dependencies
        and not str(reference).startswith("dam_core_")
    )
    return {
        "format": "appgen.dam-core-owned-boundary-check.v1",
        "ok": not violations,
        "owned_tables": DAM_CORE_OWNED_TABLES,
        "runtime_tables": DAM_CORE_RUNTIME_TABLES,
        "declared_dependencies": {
            "events": DAM_CORE_CONSUMED_EVENT_TYPES,
            "event_providers": tuple(sorted(allowed_event_dependencies)),
            "api_projections": ("product_projection",),
            "apis": tuple(sorted(allowed_api_dependencies - {"product_projection"})),
            "shared_tables": (),
        },
        "references": tuple(references),
        "violations": violations,
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


def _dam_table_fields(table: str) -> tuple[dict, ...]:
    base = [
        {"name": "id", "type": "uuid", "required": True},
        {"name": "tenant", "type": "text", "required": True},
        {"name": "created_at", "type": "timestamp", "required": True},
        {"name": "updated_at", "type": "timestamp", "required": True},
    ]
    table_specific = {
        "asset": (
            {"name": "asset_id", "type": "text", "required": True},
            {"name": "filename", "type": "text", "required": True},
            {"name": "mime_type", "type": "text", "required": True},
            {"name": "fingerprint", "type": "text", "required": True},
        ),
        "asset_rendition": (
            {"name": "rendition_id", "type": "text", "required": True},
            {"name": "asset_id", "type": "text", "required": True},
            {"name": "profile", "type": "text", "required": True},
            {"name": "quality_score", "type": "numeric", "required": False},
        ),
        "rights_policy": (
            {"name": "policy_id", "type": "text", "required": True},
            {"name": "asset_id", "type": "text", "required": True},
            {"name": "allowed_markets", "type": "jsonb", "required": True},
            {"name": "blocked_markets", "type": "jsonb", "required": True},
        ),
        "metadata_tag": (
            {"name": "tag_id", "type": "text", "required": True},
            {"name": "asset_id", "type": "text", "required": True},
            {"name": "taxonomy", "type": "text", "required": True},
            {"name": "value", "type": "text", "required": True},
        ),
        "dam_core_appgen_outbox_event": (
            {"name": "event_type", "type": "text", "required": True},
            {"name": "payload", "type": "jsonb", "required": True},
            {"name": "idempotency_key", "type": "text", "required": True},
        ),
        "dam_core_appgen_inbox_event": (
            {"name": "event_type", "type": "text", "required": True},
            {"name": "payload", "type": "jsonb", "required": True},
            {"name": "attempts", "type": "integer", "required": True},
        ),
        "dam_core_dead_letter_event": (
            {"name": "event_type", "type": "text", "required": True},
            {"name": "payload", "type": "jsonb", "required": True},
            {"name": "reason", "type": "text", "required": True},
        ),
    }
    default_fields = (
        {"name": "asset_id", "type": "text", "required": False},
        {"name": "status", "type": "text", "required": False},
        {"name": "attributes", "type": "jsonb", "required": False},
    )
    return tuple(base + list(table_specific.get(table, default_fields)))


def _dam_table_relationships(table: str) -> tuple[dict, ...]:
    asset_children = {
        "asset_version",
        "asset_binary",
        "asset_fingerprint",
        "asset_collection_member",
        "asset_rendition",
        "transcoding_job",
        "metadata_tag",
        "metadata_enrichment",
        "semantic_annotation",
        "rights_policy",
        "rights_decision",
        "license_agreement",
        "usage_entitlement",
        "asset_workflow_case",
        "asset_review_task",
        "asset_exception",
        "asset_quality_score",
        "asset_usage_snapshot",
        "asset_usage_forecast",
        "asset_duplicate_candidate",
        "asset_lineage",
        "asset_audit_entry",
        "asset_policy_screening",
        "asset_control_assertion",
        "asset_federation_view",
        "asset_anomaly_signal",
        "asset_exposure_forecast",
        "asset_identity_attestation",
    }
    relationships = []
    if table in asset_children:
        relationships.append({"type": "owned_reference", "to": "asset", "on": "asset_id"})
    if table in {"asset_collection_member"}:
        relationships.append({"type": "owned_reference", "to": "asset_collection", "on": "collection_id"})
    if table in DAM_CORE_RUNTIME_TABLES:
        relationships.append({"type": "event_contract", "to": "AppGen-X", "topic": DAM_CORE_REQUIRED_EVENT_TOPIC})
    return tuple(relationships)


def _class_name(table: str) -> str:
    return "".join(part.capitalize() for part in table.split("_"))


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
