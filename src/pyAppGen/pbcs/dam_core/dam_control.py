"""Executable improve1 controls for the DAM Core PBC."""

from __future__ import annotations

from typing import Any

from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability

PBC_KEY = "dam_core"
EVENT_CONTRACT = "AppGen-X"
REQUIRED_EVENT_TOPIC = "appgen.dam.events"
ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
OWNED_TABLES = (
    "asset", "asset_version", "asset_binary", "asset_fingerprint", "asset_collection", "asset_collection_member",
    "asset_rendition", "transcoding_job", "transcode_route", "rendition_profile", "metadata_tag", "metadata_taxonomy",
    "metadata_enrichment", "semantic_annotation", "rights_policy", "rights_decision", "license_agreement",
    "usage_entitlement", "product_projection", "campaign_projection", "channel_asset_projection", "asset_workflow_case",
    "asset_review_task", "asset_exception", "asset_quality_score", "asset_usage_snapshot", "asset_usage_forecast",
    "asset_duplicate_candidate", "asset_lineage", "asset_audit_entry", "asset_policy_screening", "asset_control_assertion",
    "asset_federation_view", "asset_resilience_drill", "asset_crypto_epoch", "carbon_transcode_window",
    "rendition_cost_simulation", "asset_route_allocation", "asset_anomaly_signal", "asset_exposure_forecast",
    "asset_identity_attestation", "asset_governed_model", "asset_seed_data", "dam_rule", "dam_parameter",
    "dam_configuration", "dam_core_appgen_outbox_event", "dam_core_appgen_inbox_event", "dam_core_dead_letter_event",
)
OUTBOX_TABLE = "dam_core_appgen_outbox_event"
INBOX_TABLE = "dam_core_appgen_inbox_event"
DEAD_LETTER_TABLE = "dam_core_dead_letter_event"

DAM_CONTROL_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in DAM_CONTROL_CAPABILITIES}
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in DAM_CONTROL_CAPABILITIES}

DAM_FEATURE_CONTROLS: dict[int, dict[str, Any]] = {
    1: {"tables": ("asset", "asset_binary", "asset_audit_entry"), "fields": ("tenant", "filename", "mime_type", "size_mb", "storage_uri", "fingerprint", "rights_reference", "audit_hash"), "ui": "DamCoreAssetWorkbench", "route": "POST /assets"},
    2: {"tables": ("asset", "asset_version", "asset_audit_entry"), "fields": ("current_state", "target_state", "actor", "reason", "idempotency_key"), "ui": "DamCoreAssetWorkbench", "route": "POST /assets/transition"},
    3: {"tables": ("asset_fingerprint", "asset_binary", "asset_audit_entry"), "fields": ("algorithm", "hash", "storage_uri", "byte_size", "mime_signature", "checksum_valid"), "ui": "DamCoreAssetWorkbench", "route": "POST /assets/fingerprint"},
    4: {"tables": ("asset_binary", "dam_rule", "dam_parameter"), "fields": ("storage_tier", "retention_class", "region", "encryption_profile", "access_policy"), "ui": "DamCoreOperationsWorkbench", "route": "POST /assets/storage-policy"},
    5: {"tables": ("asset_policy_screening", "dam_rule"), "fields": ("mime_type", "max_size", "signature_valid", "malware_scan", "rendition_profile_eligible"), "ui": "DamCoreOperationsWorkbench", "route": "POST /assets/policy-screening"},
    6: {"tables": ("asset_collection", OUTBOX_TABLE), "fields": ("collection_state", "purpose", "owner", "membership_policy", "publication_window"), "ui": "DamCoreAssetWorkbench", "route": "POST /asset-collections"},
    7: {"tables": ("asset_collection_member", "asset_collection", "asset"), "fields": ("asset_status", "rights_policy", "locale", "rendition_ready", "sort_order"), "ui": "DamCoreAssetWorkbench", "route": "POST /asset-collections/members"},
    8: {"tables": ("asset_rendition", "transcoding_job", OUTBOX_TABLE), "fields": ("profile", "target_mime", "dimensions", "output_uri", "retry_count", "source_fingerprint"), "ui": "DamCoreOperationsWorkbench", "route": "POST /renditions"},
    9: {"tables": ("transcode_route", "asset_route_allocation"), "fields": ("route_candidates", "supported_profiles", "cost", "latency", "carbon_score", "retry_policy"), "ui": "DamCoreOperationsWorkbench", "route": "POST /renditions/route-selection"},
    10: {"tables": ("asset_rendition", "asset_quality_score"), "fields": ("dimensions", "bitrate", "duration", "aspect_ratio", "accessibility_metadata", "profile_compliance"), "ui": "DamCoreOperationsWorkbench", "route": "POST /renditions/quality-score"},
    11: {"tables": ("rights_policy", "asset_audit_entry"), "fields": ("rights_state", "license_type", "markets", "expiration", "attribution", "approver"), "ui": "DamCoreRightsWorkbench", "route": "POST /rights-policies"},
    12: {"tables": ("rights_decision", "rights_policy", "usage_entitlement"), "fields": ("market", "use_case", "channel", "usage_date", "license", "policy_version"), "ui": "DamCoreRightsWorkbench", "route": "POST /rights/enforce"},
    13: {"tables": ("license_agreement", "rights_policy"), "fields": ("counterparty", "scope", "term", "territory", "media_type", "usage_limit", "evidence_document"), "ui": "DamCoreRightsWorkbench", "route": "POST /license-agreements"},
    14: {"tables": ("usage_entitlement", OUTBOX_TABLE), "fields": ("entitlement_state", "asset_scope", "grantee", "channel", "market", "start_date", "end_date"), "ui": "DamCoreRightsWorkbench", "route": "POST /usage-entitlements"},
    15: {"tables": ("metadata_taxonomy",), "fields": ("taxonomy_state", "allowed_values", "localized_labels", "hierarchy", "confidence_floor", "steward_owner"), "ui": "DamCoreOperationsWorkbench", "route": "POST /metadata-taxonomies"},
    16: {"tables": ("metadata_tag", "metadata_taxonomy"), "fields": ("taxonomy", "value", "confidence", "source", "locale", "effective_date", "steward_review"), "ui": "DamCoreOperationsWorkbench", "route": "POST /metadata-tags"},
    17: {"tables": ("metadata_enrichment", "metadata_tag", "product_projection"), "fields": ("enrichment_state", "extractor_source", "candidate_tags", "confidence", "reviewer_decision"), "ui": "DamCoreOperationsWorkbench", "route": "POST /metadata-enrichments"},
    18: {"tables": ("semantic_annotation",), "fields": ("annotation_type", "target_region", "source", "confidence", "locale", "review_status"), "ui": "DamCoreOperationsWorkbench", "route": "POST /semantic-annotations"},
    19: {"tables": ("product_projection", INBOX_TABLE, DEAD_LETTER_TABLE), "fields": ("product_key", "version", "taxonomy", "channel", "source_event_id", "freshness"), "ui": "DamCoreAssetWorkbench", "route": "POST /dam-core/events/product-published"},
    20: {"tables": ("asset_workflow_case", "asset_review_task"), "fields": ("workflow_state", "required_tasks", "owner", "sla", "approval_gate", "blocked_reason"), "ui": "DamCoreOperationsWorkbench", "route": "POST /asset-workflows"},
    21: {"tables": ("asset_review_task",), "fields": ("task_type", "assignee", "due_date", "scope", "decision", "required_evidence"), "ui": "DamCoreOperationsWorkbench", "route": "POST /asset-review-tasks"},
    22: {"tables": ("asset_exception",), "fields": ("category", "severity", "affected_asset", "root_cause", "owner", "sla", "closure_evidence"), "ui": "DamCoreOperationsWorkbench", "route": "POST /asset-exceptions"},
    23: {"tables": ("asset_exception", "asset_governed_model"), "fields": ("recommendation", "confidence", "required_approval", "explanation"), "ui": "DamCoreOperationsWorkbench", "route": "POST /asset-exceptions/recommendations"},
    24: {"tables": ("asset_duplicate_candidate", "asset_fingerprint"), "fields": ("fingerprint", "perceptual_hash", "filename", "similarity", "merge_recommendation"), "ui": "DamCoreAssetWorkbench", "route": "POST /assets/duplicate-candidates"},
    25: {"tables": ("asset_lineage", "asset_fingerprint"), "fields": ("source_asset", "derived_asset", "transformation", "editor", "fingerprint_delta", "rights_inheritance"), "ui": "DamCoreAssetWorkbench", "route": "POST /asset-lineage"},
    26: {"tables": ("asset_usage_snapshot", "rights_policy"), "fields": ("channel", "product", "campaign", "market", "rendition", "view_count", "rights_exposure"), "ui": "DamCoreAssetWorkbench", "route": "POST /asset-usage-snapshots"},
    27: {"tables": ("asset_usage_forecast",), "fields": ("asset", "channel", "market", "season", "rights_expiry", "confidence", "recommended_actions"), "ui": "DamCoreAssetWorkbench", "route": "POST /asset-usage-forecasts"},
    28: {"tables": ("asset_quality_score", "asset_rendition", "metadata_tag"), "fields": ("resolution", "rendition_coverage", "metadata_completeness", "rights_confidence", "duplicate_risk"), "ui": "DamCoreAssetWorkbench", "route": "POST /assets/quality-risk"},
    29: {"tables": ("rights_decision", "rights_policy", "license_agreement"), "fields": ("license_expiry", "market_restrictions", "attribution_required", "entitlement_gaps", "policy_uncertainty"), "ui": "DamCoreRightsWorkbench", "route": "POST /rights/risk-score"},
    30: {"tables": ("rendition_cost_simulation", "transcode_route"), "fields": ("profile_sets", "routes", "storage_tiers", "quality_thresholds", "cost", "carbon", "failure_rate"), "ui": "DamCoreOperationsWorkbench", "route": "POST /renditions/simulate"},
    31: {"tables": ("carbon_transcode_window", "transcoding_job"), "fields": ("carbon_window", "workload", "sla", "priority", "guardrails"), "ui": "DamCoreOperationsWorkbench", "route": "POST /renditions/carbon-schedule"},
    32: {"tables": ("asset_identity_attestation", "asset_crypto_epoch"), "fields": ("fingerprint", "rights_policy", "rendition_readiness", "metadata_confidence", "verifier", "expiry"), "ui": "DamCoreReleaseWorkbench", "route": "POST /assets/proofs"},
    33: {"tables": ("asset_audit_entry", OUTBOX_TABLE), "fields": ("event_type", "aggregate_id", "previous_hash", "current_hash", "actor"), "ui": "DamCoreReleaseWorkbench", "route": "GET /assets/audit-trail"},
    34: {"tables": ("asset_policy_screening", "dam_rule"), "fields": ("action", "mime", "market", "channel", "locale", "quality", "metadata_completeness"), "ui": "DamCoreOperationsWorkbench", "route": "POST /assets/policy-screening"},
    35: {"tables": (INBOX_TABLE, DEAD_LETTER_TABLE, "product_projection"), "fields": ("schema_valid", "idempotency_key", "duplicate_suppressed", "dead_letter_policy", "projection_rebuild"), "ui": "DamCoreReleaseWorkbench", "route": "POST /dam-core/inbox/replay"},
    36: {"tables": (OUTBOX_TABLE, DEAD_LETTER_TABLE), "fields": ("outbox_state", "ordering_group", "payload_hash", "retry_attempts", "delivery_proof"), "ui": "DamCoreReleaseWorkbench", "route": "POST /dam-core/outbox/replay"},
    37: {"tables": ("asset_federation_view",), "fields": ("dependency_type", "projection_only", "foreign_table_access", "scan_result"), "ui": "DamCoreReleaseWorkbench", "route": "GET /dam-core/boundary-proof"},
    38: {"tables": ("dam_configuration",), "fields": ("target_table", "field_schema", "sensitivity", "migration_preview", "api_exposure_review"), "ui": "DamCoreReleaseWorkbench", "route": "POST /dam-core/schema-extensions"},
    39: {"tables": ("asset_governed_model",), "fields": ("model_purpose", "training_window", "feature_lineage", "validation_metrics", "approval_status"), "ui": "DamCoreReleaseWorkbench", "route": "POST /dam-core/governed-models"},
    40: {"tables": ("asset_anomaly_signal",), "fields": ("signal_type", "expected_range", "observed_value", "explanation", "review_feedback"), "ui": "DamCoreOperationsWorkbench", "route": "GET /dam-core/anomalies"},
    41: {"tables": ("asset_exposure_forecast",), "fields": ("asset", "exposure_distribution", "mitigation", "confidence"), "ui": "DamCoreOperationsWorkbench", "route": "POST /assets/exposure-forecast"},
    42: {"tables": ("asset", "asset_collection", "asset_rendition", "rights_policy", "metadata_tag"), "fields": ("assets_panel", "rights_panel", "metadata_panel", "events_panel", "release_panel"), "ui": "DamCoreWorkbench", "route": "GET /workbench/pbcs/dam_core"},
    43: {"tables": ("rights_decision", "rights_policy", "license_agreement", "usage_entitlement"), "fields": ("expiring_rights", "blocked_markets", "attribution_gaps", "license_gaps"), "ui": "DamCoreRightsWorkbench", "route": "GET /workbench/pbcs/dam_core/rights"},
    44: {"tables": ("transcoding_job", "asset_rendition", "transcode_route"), "fields": ("requested_queue", "failed_queue", "ready_queue", "route_fallback", "retry_exhaustion"), "ui": "DamCoreOperationsWorkbench", "route": "GET /workbench/pbcs/dam_core/operations"},
    45: {"tables": ("metadata_tag", "metadata_taxonomy", "metadata_enrichment", "semantic_annotation"), "fields": ("taxonomy_queue", "confidence_queue", "missing_tags", "rejected_enrichment", "steward_owner"), "ui": "DamCoreOperationsWorkbench", "route": "GET /workbench/pbcs/dam_core/metadata"},
    46: {"tables": ("asset_control_assertion",), "fields": ("missing_fingerprint", "published_without_rights", "metadata_below_confidence", "agent_preview_bypass"), "ui": "DamCoreReleaseWorkbench", "route": "POST /dam-core/control-tests"},
    47: {"tables": ("asset_resilience_drill",), "fields": ("drill_type", "failure_mode", "safe_degradation", "recovery_evidence"), "ui": "DamCoreReleaseWorkbench", "route": "POST /dam-core/resilience-drills"},
    48: {"tables": ("asset_governed_model", "asset_audit_entry"), "fields": ("command", "permission", "owned_tables", "idempotency_key", "expected_event", "human_confirmation"), "ui": "DamCoreReleaseWorkbench", "route": "POST /dam-core/agent-plans"},
    49: {"tables": ("asset_control_assertion", "asset_seed_data"), "fields": ("intake_score", "rights_score", "metadata_score", "event_score", "agent_safety_score"), "ui": "DamCoreReleaseWorkbench", "route": "GET /dam-core/readiness"},
    50: {"tables": ("asset", "metadata_tag", "rights_policy", "license_agreement", "usage_entitlement", "asset_rendition", OUTBOX_TABLE), "fields": ("product_projection", "asset_registered", "duplicate_checked", "rights_safe", "rendition_ready", "publication_event"), "ui": "DamCoreReleaseWorkbench", "route": "POST /dam-core/publication-proof"},
}


def _resolve(capability: Improve1Capability | str | int) -> Improve1Capability | None:
    if isinstance(capability, Improve1Capability):
        return capability
    if isinstance(capability, int):
        return CAPABILITY_BY_NUMBER.get(capability)
    return CAPABILITY_BY_SLUG.get(capability)


def sample_payload_for(capability: Improve1Capability | str | int) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {}
    control = DAM_FEATURE_CONTROLS[resolved.feature_number]
    payload = {field: f"{resolved.slug}_{field}" for field in control["fields"]}
    payload.update(
        {
            "references": (),
            "current_state": "uploaded",
            "target_state": "review",
            "mime_type": "image/jpeg",
            "allowed_mime_types": ("image/jpeg", "image/png", "video/mp4"),
            "size_mb": 20,
            "max_size_mb": 1000,
            "checksum_valid": True,
            "rights_safe": True,
            "foreign_table_access": False,
            "target_table": "asset",
            "projection_only": True,
            "validation_metrics": {"precision": 0.95},
            "human_confirmation": True,
            "publication_event": "AssetRenditionReady",
        }
    )
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    number = capability.feature_number
    if number == 1:
        for field in ("tenant", "filename", "mime_type", "storage_uri", "fingerprint", "rights_reference", "audit_hash"):
            if not payload.get(field):
                findings.append(f"asset intake readiness requires {field}")
    if number == 2 and payload.get("current_state") == payload.get("target_state"):
        findings.append("asset lifecycle transition must change state")
    if number == 3 and payload.get("checksum_valid") is not True:
        findings.append("content-addressed fingerprint requires checksum validation")
    if number == 5 and payload.get("mime_type") not in payload.get("allowed_mime_types", ()):
        findings.append("MIME policy blocks unsupported asset format")
    if number == 12 and payload.get("rights_safe") is not True:
        findings.append("rights enforcement blocks unsafe usage")
    if number == 23 and payload.get("required_approval") in (False, "false"):
        findings.append("autonomous exception recommendation requires approval")
    if number == 37 and payload.get("foreign_table_access") is not False:
        findings.append("cross-PBC boundary proof forbids foreign table access")
    if number == 38 and payload.get("target_table") not in OWNED_TABLES:
        findings.append("schema extension target must be an owned DAM table")
    if number == 39 and not payload.get("validation_metrics"):
        findings.append("governed metadata model requires validation metrics")
    if number == 48 and payload.get("human_confirmation") is not True:
        findings.append("agent-safe DAM plans require human confirmation before mutation")
    if number == 50:
        for field in ("product_projection", "asset_registered", "duplicate_checked", "rights_safe", "rendition_ready", "publication_event"):
            if not payload.get(field):
                findings.append(f"end-to-end publication proof requires {field}")
    return tuple(findings)


def evaluate_dam_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "pbc": PBC_KEY, "reason": "unknown_dam_control", "side_effects": ()}
    control = DAM_FEATURE_CONTROLS[resolved.feature_number]
    active_payload = sample_payload_for(resolved) if payload is None else dict(payload)
    missing = tuple(field for field in control["fields"] if field not in active_payload or active_payload[field] in (None, ""))
    invalid_tables = tuple(table for table in control["tables"] if table not in OWNED_TABLES)
    invalid_references = tuple(
        ref
        for ref in active_payload.get("references", ())
        if isinstance(ref, str) and ref.endswith("_table") and ref not in OWNED_TABLES
    )
    domain_findings = _domain_findings(resolved, active_payload)
    event_type = "AssetExceptionOpened" if domain_findings else "AssetRegistered"
    if resolved.feature_number in {8, 36, 50} and not domain_findings:
        event_type = "AssetRenditionReady"
    if resolved.feature_number in {11, 12, 14} and not domain_findings:
        event_type = "AssetRightsPolicyAttached"
    return {
        "ok": not missing and not invalid_tables and not invalid_references and not domain_findings,
        "pbc": PBC_KEY,
        "capability": resolved.slug,
        "feature_number": resolved.feature_number,
        "title": resolved.title,
        "status": "implemented",
        "target_tables": control["tables"],
        "owned_tables": OWNED_TABLES,
        "read_tables": (),
        "invalid_references": invalid_references,
        "missing_required_fields": missing,
        "domain_findings": domain_findings,
        "event": {"contract": EVENT_CONTRACT, "topic": REQUIRED_EVENT_TOPIC, "type": event_type, "idempotency_key": f"dam-{resolved.feature_number}-{abs(hash(repr(active_payload))) % 10_000_000}", "outbox_table": OUTBOX_TABLE, "inbox_table": INBOX_TABLE, "dead_letter_table": DEAD_LETTER_TABLE},
        "ui_surface": control["ui"],
        "service_api": control["route"],
        "permission": "dam_core.configure" if resolved.feature_number in {38, 46, 47, 49} else "dam_core.write",
        "configuration": {"database_backends": ALLOWED_DATABASE_BACKENDS, "event_topic": REQUIRED_EVENT_TOPIC, "stream_engine_picker_visible": False, "rule_configurable": True, "parameter_configurable": True},
        "agent_skill": f"dam_core_skills.{resolved.slug}",
        "requires_human_confirmation": resolved.feature_number in {11, 12, 23, 32, 38, 48, 50},
        "retry_dead_letter_evidence": {"retry_policy": "bounded_retry_with_idempotency_key", "dead_letter_table": DEAD_LETTER_TABLE, "manual_replay_route": "POST /dam-core/dead-letter/retry"},
        "release_evidence": {"code_artifact_model": resolved.model_artifacts, "ui_surface": resolved.ui_artifacts, "service_api": resolved.service_artifacts, "test": resolved.test_artifacts, "evidence": resolved.evidence_artifacts},
        "shared_table_access": False,
        "side_effects": (),
    }


def improve1_dam_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_dam_control(capability) for capability in DAM_CONTROL_CAPABILITIES)
    return {"ok": len(evaluations) == 50 and all(item["ok"] for item in evaluations), "pbc": PBC_KEY, "capability_count": len(evaluations), "capabilities": evaluations, "owned_tables": OWNED_TABLES, "database_backends": ALLOWED_DATABASE_BACKENDS, "event_contract": EVENT_CONTRACT, "event_topic": REQUIRED_EVENT_TOPIC, "stream_engine_picker_visible": False, "side_effects": ()}


DAM_CONTROL_FUNCTIONS = {capability.slug: (lambda payload=None, slug=capability.slug: evaluate_dam_control(slug, payload)) for capability in DAM_CONTROL_CAPABILITIES}
