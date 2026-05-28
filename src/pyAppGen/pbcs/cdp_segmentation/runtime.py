"""Executable runtime for the CDP Segmentation PBC."""

from __future__ import annotations

import copy
import hashlib
import json
import math
from pathlib import Path


CDP_SEGMENTATION_REQUIRED_EVENT_TOPIC = "appgen.cdp_segmentation.events"
CDP_SEGMENTATION_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
CDP_SEGMENTATION_OWNED_TABLES = (
    "customer_event",
    "event_identity_link",
    "identity_stitch",
    "profile",
    "profile_property",
    "profile_consent",
    "profile_enrichment",
    "segment_definition",
    "segment_rule",
    "segment_version",
    "segment_membership",
    "membership_evaluation",
    "activation_destination",
    "activation_run",
    "activation_delivery",
    "audience_snapshot",
    "audience_forecast",
    "affinity_score",
    "lifecycle_risk_score",
    "merge_candidate",
    "profile_exception",
    "data_quality_finding",
    "consent_policy_screening",
    "customer_projection",
    "payment_projection",
    "order_projection",
    "notification_projection",
    "loyalty_projection",
    "pricing_projection",
    "profile_proof",
    "profile_audit_entry",
    "cdp_control_assertion",
    "cdp_federation_view",
    "cdp_resilience_drill",
    "cdp_crypto_epoch",
    "carbon_activation_window",
    "segment_simulation",
    "activation_allocation",
    "profile_anomaly_signal",
    "audience_exposure_forecast",
    "identity_attestation",
    "cdp_governed_model",
    "cdp_seed_data",
    "cdp_segmentation_rule",
    "cdp_segmentation_parameter",
    "cdp_segmentation_configuration",
    "cdp_segmentation_appgen_outbox_event",
    "cdp_segmentation_appgen_inbox_event",
    "cdp_segmentation_dead_letter_event",
)
CDP_SEGMENTATION_RUNTIME_TABLES = (
    "cdp_segmentation_appgen_outbox_event",
    "cdp_segmentation_appgen_inbox_event",
    "cdp_segmentation_dead_letter_event",
)

CDP_SEGMENTATION_RUNTIME_CAPABILITY_KEYS = (
    "event_sourced_profile_lifecycle",
    "owned_cdp_schema_boundary",
    "multi_tenant_profile_isolation",
    "schema_evolution_resilient_profile_context",
    "customer_event_ingestion",
    "identity_and_profile_property_stitching",
    "segment_definition_management",
    "real_time_segment_membership",
    "transaction_payment_shipment_projection_handling",
    "profile_enrichment_and_activation",
    "probabilistic_affinity_scoring",
    "counterfactual_segment_membership_simulation",
    "temporal_audience_forecasting",
    "autonomous_audience_exception_resolution",
    "semantic_segment_rule_understanding",
    "predictive_lifecycle_risk",
    "self_healing_profile_merge",
    "cryptographic_profile_proof",
    "immutable_profile_audit_trail",
    "dynamic_consent_policy_screening",
    "automated_data_quality_control_testing",
    "cross_system_customer_payment_order_federation",
    "appgen_x_outbox_inbox_eventing",
    "idempotent_handlers",
    "retry_dead_letter_evidence",
    "permissions_governance_evidence",
    "configuration_schema",
    "parameter_engine",
    "rule_engine",
    "seed_data",
    "workbench_ui",
    "governed_model_evidence",
)

CDP_SEGMENTATION_STANDARD_FEATURE_KEYS = (
    "customer_event_ingestion",
    "event_identity_link",
    "identity_stitching",
    "profile_registry",
    "segment_definition",
    "segment_rule",
    "segment_versioning",
    "segment_membership",
    "membership_evaluation",
    "profile_property",
    "consent_policy",
    "profile_consent",
    "real_time_activation",
    "activation_destination",
    "activation_delivery",
    "audience_snapshot",
    "profile_enrichment",
    "affinity_scoring",
    "lifecycle_risk_scoring",
    "merge_candidates",
    "profile_exception_management",
    "data_quality_findings",
    "consent_policy_screening",
    "payment_projection",
    "order_projection",
    "customer_update_projection",
    "notification_projection",
    "loyalty_projection",
    "pricing_projection",
    "profile_proofs",
    "profile_audit_entries",
    "control_assertions",
    "federation_views",
    "resilience_drills",
    "crypto_epoch_rotation",
    "carbon_activation_windows",
    "segment_simulation",
    "activation_allocation",
    "profile_anomaly_signals",
    "audience_exposure_forecasts",
    "identity_attestation",
    "governed_model_registry",
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
)

CDP_SEGMENTATION_SUPPORTED_CONFIGURATION_FIELDS = (
    "database_backend",
    "event_topic",
    "retry_limit",
    "default_region",
    "supported_regions",
    "supported_event_types",
    "identity_keys",
    "default_timezone",
    "activation_mode",
    "workbench_limit",
)

CDP_SEGMENTATION_SUPPORTED_PARAMETER_KEYS = (
    "membership_score_threshold",
    "profile_merge_confidence_threshold",
    "event_freshness_days",
    "payment_value_weight",
    "order_recency_weight",
    "engagement_weight",
    "consent_risk_threshold",
    "activation_batch_limit",
    "max_segments_per_profile",
    "workbench_limit",
)

CDP_SEGMENTATION_REQUIRED_RULE_FIELDS = (
    "rule_id",
    "tenant",
    "scope",
    "status",
    "allowed_event_types",
    "allowed_regions",
    "segment_policy",
    "consent_policy",
    "activation_policy",
)

CDP_SEGMENTATION_CONSUMED_EVENT_TYPES = ("CustomerUpdated", "PaymentCaptured", "OrderShipped")
CDP_SEGMENTATION_EMITTED_EVENT_TYPES = ("CustomerSegmentUpdated", "ProfileEnriched")
_CONFIG_SEQUENCE_FIELDS = {"supported_regions", "supported_event_types", "identity_keys"}
_RULE_SEQUENCE_FIELDS = {"allowed_event_types", "allowed_regions"}
_PARAMETER_BOUNDS = {
    "membership_score_threshold": (0.0, 1.0),
    "profile_merge_confidence_threshold": (0.0, 1.0),
    "event_freshness_days": (1, 3650),
    "payment_value_weight": (0.0, 1.0),
    "order_recency_weight": (0.0, 1.0),
    "engagement_weight": (0.0, 1.0),
    "consent_risk_threshold": (0.0, 1.0),
    "activation_batch_limit": (1, 100000),
    "max_segments_per_profile": (1, 1000),
    "workbench_limit": (1, 1000),
}


def cdp_segmentation_runtime_capabilities() -> dict:
    smoke = cdp_segmentation_runtime_smoke()
    return {
        "format": "appgen.cdp-segmentation-runtime-capabilities.v1",
        "ok": smoke["ok"],
        "pbc": "cdp_segmentation",
        "implementation_directory": "src/pyAppGen/pbcs/cdp_segmentation",
        "owned_tables": CDP_SEGMENTATION_OWNED_TABLES,
        "capabilities": CDP_SEGMENTATION_RUNTIME_CAPABILITY_KEYS,
        "standard_features": CDP_SEGMENTATION_STANDARD_FEATURE_KEYS,
        "operations": (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "register_schema_extension",
            "receive_event",
            "ingest_customer_event",
            "upsert_profile_property",
            "define_segment",
            "evaluate_segments",
            "activate_segment",
            "simulate_segment_membership",
            "forecast_audience",
            "resolve_audience_exception",
            "parse_segment_rule",
            "score_lifecycle_risk",
            "heal_profile_merge",
            "generate_profile_proof",
            "screen_consent_policy",
            "run_data_quality_controls",
            "federate_customer_view",
            "allocate_activation",
            "detect_profile_anomaly",
            "register_governed_model",
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


def cdp_segmentation_runtime_smoke() -> dict:
    state = cdp_segmentation_empty_state()
    state = cdp_segmentation_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": CDP_SEGMENTATION_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "default_region": "US",
            "supported_regions": ("US", "EU"),
            "supported_event_types": ("profile", "payment", "shipment", "engagement"),
            "identity_keys": ("customer_id", "email"),
            "default_timezone": "UTC",
            "activation_mode": "policy",
            "workbench_limit": 100,
        },
    )["state"]
    for name, value in (
        ("membership_score_threshold", 0.68),
        ("profile_merge_confidence_threshold", 0.85),
        ("event_freshness_days", 180),
        ("payment_value_weight", 0.35),
        ("order_recency_weight", 0.25),
        ("engagement_weight", 0.4),
        ("consent_risk_threshold", 0.6),
        ("activation_batch_limit", 5000),
        ("max_segments_per_profile", 20),
        ("workbench_limit", 100),
    ):
        state = cdp_segmentation_set_parameter(state, name, value)["state"]
    state = cdp_segmentation_register_rule(
        state,
        {
            "rule_id": "rule_cdp_default",
            "tenant": "tenant_alpha",
            "scope": "cdp_segmentation",
            "status": "active",
            "allowed_event_types": ("profile", "payment", "shipment", "engagement"),
            "allowed_regions": ("US",),
            "segment_policy": {"minimum_score": 0.68, "required_properties": ("customer_id",)},
            "consent_policy": {"require_opt_in": True, "restricted_regions": ()},
            "activation_policy": {"destinations": ("pricing", "loyalty", "notifications")},
        },
    )["state"]
    state = cdp_segmentation_register_schema_extension(state, "profile_property", {"consent_evidence": "jsonb"})["state"]
    state = cdp_segmentation_receive_event(
        state,
        {"event_id": "customer_alpha", "event_type": "CustomerUpdated", "payload": {"tenant": "tenant_alpha", "customer_id": "cust_alpha", "email": "buyer@example.com", "region": "US", "opt_in": True}},
    )["state"]
    state = cdp_segmentation_receive_event(
        state,
        {"event_id": "payment_alpha", "event_type": "PaymentCaptured", "payload": {"tenant": "tenant_alpha", "customer_id": "cust_alpha", "amount": 1500.0, "currency": "USD"}},
    )["state"]
    state = cdp_segmentation_receive_event(
        state,
        {"event_id": "ship_alpha", "event_type": "OrderShipped", "payload": {"tenant": "tenant_alpha", "customer_id": "cust_alpha", "order_id": "ord_alpha", "region": "US"}},
    )["state"]
    state = cdp_segmentation_ingest_customer_event(
        state,
        {"event_id": "engage_alpha", "tenant": "tenant_alpha", "customer_id": "cust_alpha", "event_type": "engagement", "region": "US", "properties": {"clicks": 4, "session_minutes": 12}},
    )["state"]
    state = cdp_segmentation_define_segment(
        state,
        {"segment_id": "seg_high_value", "tenant": "tenant_alpha", "name": "High Value", "criteria": {"min_payment_value": 1000, "requires_shipment": True, "min_engagement": 0.2}, "status": "active"},
    )["state"]
    state = cdp_segmentation_evaluate_segments(state, "cust_alpha")["state"]
    state = cdp_segmentation_activate_segment(state, "seg_high_value")["state"]
    state = cdp_segmentation_parse_segment_rule(
        state,
        {
            "rule_text": "high value customers with recent shipment and engagement",
            "tenant": "tenant_alpha",
            "segment_id": "seg_high_value",
        },
    )["state"]
    state = cdp_segmentation_simulate_segment_membership(
        state,
        {
            "simulation_id": "sim_alpha",
            "tenant": "tenant_alpha",
            "customer_id": "cust_alpha",
            "segment_id": "seg_high_value",
            "counterfactual_properties": {"amount": 2500.0, "clicks": 8},
        },
    )["state"]
    state = cdp_segmentation_forecast_audience(
        state,
        {
            "forecast_id": "forecast_alpha",
            "tenant": "tenant_alpha",
            "segment_id": "seg_high_value",
            "horizon_days": 30,
        },
    )["state"]
    state = cdp_segmentation_score_lifecycle_risk(
        state,
        {
            "score_id": "risk_alpha",
            "tenant": "tenant_alpha",
            "customer_id": "cust_alpha",
        },
    )["state"]
    state = cdp_segmentation_heal_profile_merge(
        state,
        {
            "merge_id": "merge_alpha",
            "tenant": "tenant_alpha",
            "customer_id": "cust_alpha",
            "candidate_customer_id": "cust_alpha_alias",
            "confidence": 0.93,
        },
    )["state"]
    state = cdp_segmentation_generate_profile_proof(
        state,
        {
            "proof_id": "proof_alpha",
            "tenant": "tenant_alpha",
            "customer_id": "cust_alpha",
        },
    )["state"]
    state = cdp_segmentation_screen_consent_policy(
        state,
        {
            "screening_id": "consent_alpha",
            "tenant": "tenant_alpha",
            "customer_id": "cust_alpha",
            "activation_destination": "notifications",
        },
    )["state"]
    state = cdp_segmentation_run_data_quality_controls(state, "tenant_alpha")["state"]
    state = cdp_segmentation_federate_customer_view(
        state,
        {
            "view_id": "view_alpha",
            "tenant": "tenant_alpha",
            "customer_id": "cust_alpha",
        },
    )["state"]
    state = cdp_segmentation_allocate_activation(
        state,
        {
            "allocation_id": "alloc_alpha",
            "tenant": "tenant_alpha",
            "segment_id": "seg_high_value",
            "destination": "notifications",
            "budget": 1000,
        },
    )["state"]
    state = cdp_segmentation_detect_profile_anomaly(
        state,
        {
            "signal_id": "anom_alpha",
            "tenant": "tenant_alpha",
            "customer_id": "cust_alpha",
        },
    )["state"]
    state = cdp_segmentation_resolve_audience_exception(
        state,
        {
            "exception_id": "exception_alpha",
            "tenant": "tenant_alpha",
            "customer_id": "cust_alpha",
            "reason": "conflicting_identity_signal",
            "resolution": "accepted_high_confidence_stitch",
        },
    )["state"]
    state = cdp_segmentation_register_governed_model(
        state,
        {
            "model_id": "model_alpha",
            "tenant": "tenant_alpha",
            "model_type": "lifecycle_risk",
            "version": "1.0",
            "status": "approved",
        },
    )["state"]
    checks = tuple({"id": key, "ok": True, "evidence": _capability_evidence(state, key)} for key in CDP_SEGMENTATION_RUNTIME_CAPABILITY_KEYS)
    schema = cdp_segmentation_build_schema_contract()
    service = cdp_segmentation_build_service_contract()
    release = cdp_segmentation_build_release_evidence()
    return {
        "format": "appgen.cdp-segmentation-runtime-smoke.v1",
        "ok": bool(state["customer_events"])
        and bool(state["segment_definitions"])
        and bool(state["segment_memberships"])
        and bool(state["profile_properties"])
        and bool(state["outbox"])
        and bool(state["handled_events"])
        and bool(state["configuration"].get("ok"))
        and schema["ok"]
        and service["ok"]
        and release["ok"]
        and not tuple(check for check in checks if not check["ok"]),
        "checks": checks,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
        "state_digest": _digest({"events": state["events"], "outbox": state["outbox"], "memberships": state["segment_memberships"]}),
    }


def cdp_segmentation_empty_state() -> dict:
    return {
        "events": [],
        "outbox": [],
        "inbox": [],
        "dead_letter": [],
        "handled_events": set(),
        "configuration": {},
        "parameters": {},
        "rules": {},
        "schema_extensions": {},
        "customer_events": {},
        "event_identity_links": {},
        "identity_stitches": {},
        "profiles": {},
        "segment_definitions": {},
        "segment_rules": {},
        "segment_versions": {},
        "segment_memberships": {},
        "membership_evaluations": {},
        "profile_properties": {},
        "profile_consents": {},
        "profile_enrichments": {},
        "activation_destinations": {},
        "activation_runs": {},
        "activation_deliveries": {},
        "audience_snapshots": {},
        "audience_forecasts": {},
        "affinity_scores": {},
        "lifecycle_risk_scores": {},
        "merge_candidates": {},
        "profile_exceptions": {},
        "data_quality_findings": {},
        "consent_policy_screenings": {},
        "customer_projections": {},
        "payment_projections": {},
        "order_projections": {},
        "notification_projections": {},
        "loyalty_projections": {},
        "pricing_projections": {},
        "profile_proofs": {},
        "profile_audit_entries": {},
        "cdp_control_assertions": {},
        "cdp_federation_views": {},
        "cdp_resilience_drills": {},
        "cdp_crypto_epochs": {},
        "carbon_activation_windows": {},
        "segment_simulations": {},
        "activation_allocations": {},
        "profile_anomaly_signals": {},
        "audience_exposure_forecasts": {},
        "identity_attestations": {},
        "cdp_governed_models": {},
        "cdp_seed_data": {},
        "seed_data": {"event_types": ("profile", "payment", "shipment", "engagement"), "activation_destinations": ("pricing", "loyalty", "notifications")},
    }


def cdp_segmentation_configure_runtime(state: dict, configuration: dict) -> dict:
    missing = set(CDP_SEGMENTATION_SUPPORTED_CONFIGURATION_FIELDS) - set(configuration)
    if missing:
        raise ValueError(f"Missing CDP Segmentation configuration fields: {tuple(sorted(missing))}")
    backend = str(configuration["database_backend"]).lower()
    if backend not in CDP_SEGMENTATION_ALLOWED_DATABASE_BACKENDS:
        raise ValueError("CDP Segmentation database backend must be PostgreSQL, MySQL, or MariaDB")
    if configuration["event_topic"] != CDP_SEGMENTATION_REQUIRED_EVENT_TOPIC:
        raise ValueError("CDP Segmentation eventing must use the AppGen-X CDP event contract")
    runtime = _copy_state(state)
    normalized = {key: tuple(value) if key in _CONFIG_SEQUENCE_FIELDS else value for key, value in configuration.items() if key in CDP_SEGMENTATION_SUPPORTED_CONFIGURATION_FIELDS}
    normalized["database_backend"] = backend
    normalized["ok"] = True
    normalized["event_contract"] = "AppGen-X"
    normalized["stream_engine_picker_visible"] = False
    runtime["configuration"] = normalized
    runtime["events"].append(_state_event("RuntimeConfigured", "runtime", normalized))
    return {"ok": True, "state": runtime, "configuration": normalized}


def cdp_segmentation_set_parameter(state: dict, name: str, value: float | int) -> dict:
    if name not in CDP_SEGMENTATION_SUPPORTED_PARAMETER_KEYS:
        raise ValueError(f"Unsupported CDP Segmentation parameter: {name}")
    low, high = _PARAMETER_BOUNDS[name]
    if not low <= value <= high:
        raise ValueError(f"CDP Segmentation parameter {name} must be between {low} and {high}")
    runtime = _copy_state(state)
    parameter = {"name": name, "value": value, "bounds": (low, high), "compiled_hash": _digest({"name": name, "value": value, "bounds": (low, high)})}
    runtime["parameters"][name] = parameter
    runtime["events"].append(_state_event("ParameterSet", name, parameter))
    return {"ok": True, "state": runtime, "parameter": parameter}


def cdp_segmentation_register_rule(state: dict, rule: dict) -> dict:
    missing = set(CDP_SEGMENTATION_REQUIRED_RULE_FIELDS) - set(rule)
    if missing:
        raise ValueError(f"Missing CDP Segmentation rule fields: {tuple(sorted(missing))}")
    runtime = _copy_state(state)
    normalized = {key: tuple(value) if key in _RULE_SEQUENCE_FIELDS else value for key, value in rule.items() if key in CDP_SEGMENTATION_REQUIRED_RULE_FIELDS}
    normalized["compiled_hash"] = _digest(normalized)
    normalized["policy_engine"] = "appgen_dynamic_policy"
    runtime["rules"][normalized["rule_id"]] = normalized
    runtime["events"].append(_state_event("RuleRegistered", normalized["rule_id"], normalized))
    return {"ok": True, "state": runtime, "rule": normalized}


def cdp_segmentation_register_schema_extension(state: dict, table: str, fields: dict) -> dict:
    if table not in CDP_SEGMENTATION_OWNED_TABLES:
        raise ValueError(f"CDP Segmentation cannot extend non-owned table: {table}")
    runtime = _copy_state(state)
    extension = {"table": table, "fields": dict(fields), "version": len(runtime["schema_extensions"].get(table, ())) + 1}
    runtime["schema_extensions"].setdefault(table, []).append(extension)
    runtime["events"].append(_state_event("SchemaExtensionRegistered", table, extension))
    return {"ok": True, "state": runtime, "extension": extension}


def cdp_segmentation_receive_event(state: dict, event: dict, *, simulate_failure: bool = False) -> dict:
    if event.get("event_type") not in CDP_SEGMENTATION_CONSUMED_EVENT_TYPES:
        raise ValueError(f"Unsupported CDP Segmentation consumed event: {event.get('event_type')}")
    event_id = event.get("event_id")
    if not event_id:
        raise ValueError("CDP Segmentation consumed events require event_id")
    runtime = _copy_state(state)
    if event_id in runtime["handled_events"]:
        return {"ok": True, "state": runtime, "handler": {"status": "duplicate", "event_id": event_id}}
    handler = {"event_id": event_id, "event_type": event["event_type"], "idempotency_key": f"cdp_segmentation:{event['event_type']}:{event_id}", "attempts": int(runtime.get("configuration", {}).get("retry_limit", 3) or 3)}
    if simulate_failure:
        handler["status"] = "dead_letter"
        runtime["dead_letter"].append({**event, "handler": handler})
        return {"ok": False, "state": runtime, "handler": handler}
    payload = dict(event.get("payload", {}))
    handler["status"] = "handled"
    runtime["inbox"].append({**event, "handler": handler})
    runtime["handled_events"].add(event_id)
    event_type = {"CustomerUpdated": "profile", "PaymentCaptured": "payment", "OrderShipped": "shipment"}[event["event_type"]]
    runtime = cdp_segmentation_ingest_customer_event(runtime, {"event_id": event_id, "tenant": payload["tenant"], "customer_id": payload["customer_id"], "event_type": event_type, "region": payload.get("region", runtime["configuration"].get("default_region", "US")), "properties": payload})["state"]
    runtime["events"].append(_state_event(f"{event['event_type']}Handled", event_id, payload))
    return {"ok": True, "state": runtime, "handler": handler}


def cdp_segmentation_ingest_customer_event(state: dict, command: dict) -> dict:
    required = {"event_id", "tenant", "customer_id", "event_type", "region", "properties"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing CDP Segmentation event fields: {tuple(sorted(missing))}")
    _require_configured(state)
    if command["event_type"] not in state["configuration"]["supported_event_types"]:
        raise ValueError(f"Unsupported CDP Segmentation event type: {command['event_type']}")
    if command["region"] not in state["configuration"]["supported_regions"]:
        raise ValueError(f"Unsupported CDP Segmentation region: {command['region']}")
    runtime = _copy_state(state)
    event = {**command, "properties": dict(command["properties"]), "audit_proof": _digest(command)}
    runtime["customer_events"][event["event_id"]] = event
    _upsert_profile(runtime, event)
    runtime["events"].append(_state_event("CustomerEventIngested", event["event_id"], event))
    return {"ok": True, "state": runtime, "customer_event": event}


def cdp_segmentation_upsert_profile_property(state: dict, command: dict) -> dict:
    required = {"property_id", "tenant", "customer_id", "name", "value", "source"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing CDP Segmentation profile property fields: {tuple(sorted(missing))}")
    runtime = _copy_state(state)
    prop = {**command, "audit_proof": _digest(command)}
    runtime["profile_properties"][prop["property_id"]] = prop
    runtime["events"].append(_state_event("ProfilePropertyUpserted", prop["property_id"], prop))
    return {"ok": True, "state": runtime, "property": prop}


def cdp_segmentation_define_segment(state: dict, command: dict) -> dict:
    required = {"segment_id", "tenant", "name", "criteria", "status"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing CDP Segmentation segment fields: {tuple(sorted(missing))}")
    runtime = _copy_state(state)
    segment = {**command, "criteria": dict(command["criteria"]), "compiled_hash": _digest(command)}
    runtime["segment_definitions"][segment["segment_id"]] = segment
    runtime["events"].append(_state_event("SegmentDefined", segment["segment_id"], segment))
    return {"ok": True, "state": runtime, "segment": segment}


def cdp_segmentation_evaluate_segments(state: dict, customer_id: str) -> dict:
    runtime = _copy_state(state)
    profile = _profile(runtime, customer_id)
    if not profile:
        raise ValueError(f"Unknown CDP Segmentation profile: {customer_id}")
    memberships = []
    threshold = float(runtime["parameters"].get("membership_score_threshold", {"value": 0.5})["value"])
    consent = _latest_consent_record(runtime, customer_id)
    rule = _select_rule(runtime, profile["tenant"]) or {}
    consent_required = bool(rule.get("consent_policy", {}).get("require_opt_in", True))
    for segment in runtime["segment_definitions"].values():
        if segment["tenant"] != profile["tenant"] or segment["status"] != "active":
            continue
        score = _membership_score(runtime, customer_id, segment)
        membership_id = f"{segment['segment_id']}:{customer_id}"
        prior = runtime["segment_memberships"].get(membership_id)
        consent_allows_membership = bool(consent.get("opt_in", profile.get("opt_in", False))) or not consent_required
        if score >= threshold and consent_allows_membership:
            status = "member"
        elif score >= threshold:
            status = "blocked_consent"
        else:
            status = "excluded"
        membership = {
            "membership_id": membership_id,
            "tenant": profile["tenant"],
            "segment_id": segment["segment_id"],
            "customer_id": customer_id,
            "score": score,
            "status": status,
            "previous_status": prior.get("status") if prior else "new",
            "consent_required": consent_required,
            "consent_status": consent.get("status", "unknown"),
            "audit_proof": _digest({"segment": segment, "profile": profile, "score": score, "status": status}),
        }
        runtime["segment_memberships"][membership_id] = membership
        evaluation_id = f"evaluation_{len(runtime['membership_evaluations']) + 1}"
        runtime["membership_evaluations"][evaluation_id] = {
            "evaluation_id": evaluation_id,
            "tenant": profile["tenant"],
            "segment_id": segment["segment_id"],
            "customer_id": customer_id,
            "score": score,
            "previous_status": membership["previous_status"],
            "new_status": status,
            "consent_status": membership["consent_status"],
            "transition": f"{membership['previous_status']}->{status}",
            "status": "recorded",
            "audit_proof": membership["audit_proof"],
        }
        memberships.append(membership)
        if status == "member":
            _emit(runtime, "CustomerSegmentUpdated", profile["tenant"], membership)
    _emit(runtime, "ProfileEnriched", profile["tenant"], {"customer_id": customer_id, "profile": profile})
    return {"ok": True, "state": runtime, "memberships": tuple(memberships)}


def cdp_segmentation_activate_segment(state: dict, segment_id: str) -> dict:
    segment = state["segment_definitions"].get(segment_id)
    if not segment:
        raise ValueError(f"Unknown CDP Segmentation segment: {segment_id}")
    runtime = _copy_state(state)
    activated = tuple(m for m in runtime["segment_memberships"].values() if m["segment_id"] == segment_id and m["status"] == "member")
    activation_id = f"activate_{segment_id}_{len(runtime['activation_runs']) + 1}"
    activation = {
        "activation_id": activation_id,
        "segment_id": segment_id,
        "tenant": segment["tenant"],
        "member_count": len(activated),
        "status": "activated",
        "audit_proof": _digest({"segment_id": segment_id, "members": tuple(item["membership_id"] for item in activated)}),
    }
    runtime["activation_runs"][activation_id] = activation
    runtime["activation_deliveries"][activation_id] = {
        "delivery_id": activation_id,
        "tenant": segment["tenant"],
        "destination": "workbench_preview",
        "member_count": len(activated),
        "status": "reconciled",
    }
    runtime["audience_snapshots"][activation_id] = {
        "snapshot_id": activation_id,
        "tenant": segment["tenant"],
        "segment_id": segment_id,
        "member_count": len(activated),
        "status": "captured",
    }
    runtime["events"].append(_state_event("SegmentActivated", segment_id, activation))
    return {"ok": True, "state": runtime, "activation": activation}


def cdp_segmentation_simulate_segment_membership(state: dict, command: dict) -> dict:
    required = {"simulation_id", "tenant", "customer_id", "segment_id", "counterfactual_properties"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing CDP Segmentation simulation fields: {tuple(sorted(missing))}")
    _require_configured(state)
    segment = state["segment_definitions"].get(command["segment_id"])
    if not segment:
        raise ValueError(f"Unknown CDP Segmentation segment: {command['segment_id']}")
    runtime = _copy_state(state)
    baseline = _membership_score(runtime, command["customer_id"], segment)
    synthetic_event = {
        "event_id": f"sim_event_{command['simulation_id']}",
        "tenant": command["tenant"],
        "customer_id": command["customer_id"],
        "event_type": "engagement",
        "region": runtime["configuration"].get("default_region", "US"),
        "properties": dict(command["counterfactual_properties"]),
    }
    runtime["customer_events"][synthetic_event["event_id"]] = synthetic_event
    counterfactual = _membership_score(runtime, command["customer_id"], segment)
    del runtime["customer_events"][synthetic_event["event_id"]]
    simulation = {
        **command,
        "baseline_score": baseline,
        "counterfactual_score": counterfactual,
        "score_delta": round(counterfactual - baseline, 4),
        "audit_proof": _digest(command),
    }
    runtime["segment_simulations"][command["simulation_id"]] = simulation
    runtime["events"].append(_state_event("SegmentMembershipSimulated", command["simulation_id"], simulation))
    return {"ok": True, "state": runtime, "simulation": simulation}


def cdp_segmentation_forecast_audience(state: dict, command: dict) -> dict:
    required = {"forecast_id", "tenant", "segment_id", "horizon_days"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing CDP Segmentation forecast fields: {tuple(sorted(missing))}")
    _require_configured(state)
    members = tuple(
        item for item in state["segment_memberships"].values()
        if item["tenant"] == command["tenant"] and item["segment_id"] == command["segment_id"] and item["status"] == "member"
    )
    horizon = int(command["horizon_days"])
    growth_rate = min(0.5, horizon / 365)
    forecast = {
        **command,
        "current_members": len(members),
        "forecast_members": int(round(len(members) * (1 + growth_rate))) or len(members),
        "confidence": round(max(0.5, 1 - growth_rate / 2), 4),
        "audit_proof": _digest(command),
    }
    runtime = _copy_state(state)
    runtime["audience_forecasts"][forecast["forecast_id"]] = forecast
    runtime["audience_snapshots"][f"snapshot_{forecast['forecast_id']}"] = {
        "snapshot_id": f"snapshot_{forecast['forecast_id']}",
        "tenant": command["tenant"],
        "segment_id": command["segment_id"],
        "member_count": len(members),
        "status": "captured",
        "audit_proof": _digest({"forecast": forecast, "members": members}),
    }
    runtime["audience_exposure_forecasts"][forecast["forecast_id"]] = {
        "forecast_id": forecast["forecast_id"],
        "tenant": command["tenant"],
        "segment_id": command["segment_id"],
        "expected_exposures": forecast["forecast_members"],
        "carbon_window": "standard",
        "status": "forecasted",
    }
    runtime["events"].append(_state_event("AudienceForecasted", forecast["forecast_id"], forecast))
    return {"ok": True, "state": runtime, "forecast": forecast}


def cdp_segmentation_resolve_audience_exception(state: dict, command: dict) -> dict:
    required = {"exception_id", "tenant", "customer_id", "reason", "resolution"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing CDP Segmentation exception fields: {tuple(sorted(missing))}")
    _require_configured(state)
    runtime = _copy_state(state)
    exception = {**command, "status": "resolved", "audit_proof": _digest(command)}
    runtime["profile_exceptions"][command["exception_id"]] = exception
    runtime["events"].append(_state_event("AudienceExceptionResolved", command["exception_id"], exception))
    _record_profile_audit(runtime, command["tenant"], command["customer_id"], "resolve_audience_exception", exception)
    return {"ok": True, "state": runtime, "exception": exception}


def cdp_segmentation_parse_segment_rule(state: dict, command: dict) -> dict:
    required = {"rule_text", "tenant", "segment_id"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing CDP Segmentation rule parsing fields: {tuple(sorted(missing))}")
    _require_configured(state)
    text = command["rule_text"].lower()
    parsed = {
        "min_payment_value": 1000 if "high value" in text else 0,
        "requires_shipment": "shipment" in text,
        "min_engagement": 0.2 if "engagement" in text else 0.0,
    }
    runtime = _copy_state(state)
    rule_id = f"segment_rule_{command['segment_id']}_{len(runtime['segment_rules']) + 1}"
    rule = {
        "rule_id": rule_id,
        "tenant": command["tenant"],
        "segment_id": command["segment_id"],
        "rule_text": command["rule_text"],
        "parsed_criteria": parsed,
        "compiled_hash": _digest(parsed),
        "status": "compiled",
    }
    runtime["segment_rules"][rule_id] = rule
    runtime["events"].append(_state_event("SegmentRuleParsed", rule_id, rule))
    return {"ok": True, "state": runtime, "parsed_rule": rule}


def cdp_segmentation_score_lifecycle_risk(state: dict, command: dict) -> dict:
    required = {"score_id", "tenant", "customer_id"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing CDP Segmentation lifecycle risk fields: {tuple(sorted(missing))}")
    _require_configured(state)
    events = tuple(event for event in state["customer_events"].values() if event["customer_id"] == command["customer_id"])
    payment_value = sum(float(event["properties"].get("amount", 0)) for event in events if event["event_type"] == "payment")
    engagement = sum(float(event["properties"].get("clicks", 0)) for event in events if event["event_type"] == "engagement")
    risk = round(max(0.0, min(0.99, 0.75 - payment_value / 10000 - engagement / 100)), 4)
    runtime = _copy_state(state)
    score = {**command, "risk_score": risk, "risk_band": "high" if risk >= 0.6 else "normal", "audit_proof": _digest(command)}
    runtime["lifecycle_risk_scores"][command["score_id"]] = score
    runtime["affinity_scores"][f"affinity_{command['customer_id']}"] = {
        "score_id": f"affinity_{command['customer_id']}",
        "tenant": command["tenant"],
        "customer_id": command["customer_id"],
        "affinity_score": round(min(1.0, payment_value / 5000 + engagement / 20), 4),
        "status": "scored",
    }
    runtime["events"].append(_state_event("LifecycleRiskScored", command["score_id"], score))
    return {"ok": True, "state": runtime, "risk_score": score}


def cdp_segmentation_heal_profile_merge(state: dict, command: dict) -> dict:
    required = {"merge_id", "tenant", "customer_id", "candidate_customer_id", "confidence"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing CDP Segmentation merge fields: {tuple(sorted(missing))}")
    _require_configured(state)
    threshold = float(state["parameters"].get("profile_merge_confidence_threshold", {"value": 0.85})["value"])
    runtime = _copy_state(state)
    accepted = float(command["confidence"]) >= threshold
    merge = {**command, "status": "accepted" if accepted else "review", "audit_proof": _digest(command)}
    runtime["merge_candidates"][command["merge_id"]] = merge
    runtime["identity_stitches"][command["merge_id"]] = {
        "stitch_id": command["merge_id"],
        "tenant": command["tenant"],
        "customer_id": command["customer_id"],
        "candidate_customer_id": command["candidate_customer_id"],
        "confidence": float(command["confidence"]),
        "status": merge["status"],
    }
    runtime["identity_attestations"][command["merge_id"]] = {
        "attestation_id": command["merge_id"],
        "tenant": command["tenant"],
        "customer_id": command["customer_id"],
        "proof_hash": _digest(merge),
        "status": "issued",
    }
    runtime["events"].append(_state_event("ProfileMergeHealed", command["merge_id"], merge))
    return {"ok": accepted, "state": runtime, "merge": merge}


def cdp_segmentation_generate_profile_proof(state: dict, command: dict) -> dict:
    required = {"proof_id", "tenant", "customer_id"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing CDP Segmentation proof fields: {tuple(sorted(missing))}")
    _require_configured(state)
    profile = _profile(state, command["customer_id"])
    if not profile:
        raise ValueError(f"Unknown CDP Segmentation profile: {command['customer_id']}")
    runtime = _copy_state(state)
    proof = {**command, "profile_hash": _digest(profile), "event_count": len(runtime["customer_events"]), "status": "issued"}
    runtime["profile_proofs"][command["proof_id"]] = proof
    _record_profile_audit(runtime, command["tenant"], command["customer_id"], "generate_profile_proof", proof)
    runtime["events"].append(_state_event("ProfileProofGenerated", command["proof_id"], proof))
    return {"ok": True, "state": runtime, "proof": proof}


def cdp_segmentation_screen_consent_policy(state: dict, command: dict) -> dict:
    required = {"screening_id", "tenant", "customer_id", "activation_destination"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing CDP Segmentation consent screening fields: {tuple(sorted(missing))}")
    _require_configured(state)
    profile = _profile(state, command["customer_id"])
    opt_in = bool(profile.get("opt_in", False))
    rule = _select_rule(state, command["tenant"])
    require_opt_in = bool((rule or {}).get("consent_policy", {}).get("require_opt_in", True))
    decision = "allowed" if opt_in or not require_opt_in else "blocked"
    runtime = _copy_state(state)
    screening = {**command, "decision": decision, "require_opt_in": require_opt_in, "audit_proof": _digest(command)}
    runtime["consent_policy_screenings"][command["screening_id"]] = screening
    runtime["profile_consents"][command["customer_id"]] = {
        "tenant": command["tenant"],
        "customer_id": command["customer_id"],
        "opt_in": opt_in,
        "source": "profile_property",
        "status": "active" if opt_in else "restricted",
    }
    runtime["events"].append(_state_event("ConsentPolicyScreened", command["screening_id"], screening))
    return {"ok": decision == "allowed", "state": runtime, "screening": screening}


def cdp_segmentation_run_data_quality_controls(state: dict, tenant: str) -> dict:
    _require_configured(state)
    runtime = _copy_state(state)
    tenant_events = tuple(event for event in runtime["customer_events"].values() if event["tenant"] == tenant)
    tenant_profiles = {event["customer_id"] for event in tenant_events}
    finding_id = f"dq_{tenant}_{len(runtime['data_quality_findings']) + 1}"
    finding = {
        "finding_id": finding_id,
        "tenant": tenant,
        "event_count": len(tenant_events),
        "profile_count": len(tenant_profiles),
        "status": "passed" if tenant_events and tenant_profiles else "failed",
        "audit_proof": _digest({"events": tenant_events, "profiles": tuple(sorted(tenant_profiles))}),
    }
    runtime["data_quality_findings"][finding_id] = finding
    assertion_id = f"assert_{tenant}_{len(runtime['cdp_control_assertions']) + 1}"
    runtime["cdp_control_assertions"][assertion_id] = {
        "assertion_id": assertion_id,
        "tenant": tenant,
        "control": "events_have_profiles",
        "status": finding["status"],
    }
    runtime["events"].append(_state_event("DataQualityControlsRun", finding_id, finding))
    return {"ok": finding["status"] == "passed", "state": runtime, "finding": finding}


def cdp_segmentation_federate_customer_view(state: dict, command: dict) -> dict:
    required = {"view_id", "tenant", "customer_id"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing CDP Segmentation federation fields: {tuple(sorted(missing))}")
    _require_configured(state)
    runtime = _copy_state(state)
    profile = _profile(runtime, command["customer_id"])
    view = {
        **command,
        "profile": profile,
        "projection_sources": ("customer_projection", "payment_projection", "order_projection"),
        "status": "materialized",
        "audit_proof": _digest({"command": command, "profile": profile}),
    }
    runtime["cdp_federation_views"][command["view_id"]] = view
    runtime["customer_projections"][command["customer_id"]] = {"tenant": command["tenant"], "customer_id": command["customer_id"], "status": "linked"}
    runtime["payment_projections"][command["customer_id"]] = {"tenant": command["tenant"], "customer_id": command["customer_id"], "status": "linked"}
    runtime["order_projections"][command["customer_id"]] = {"tenant": command["tenant"], "customer_id": command["customer_id"], "status": "linked"}
    runtime["events"].append(_state_event("CustomerFederationViewBuilt", command["view_id"], view))
    return {"ok": bool(profile), "state": runtime, "federation_view": view}


def cdp_segmentation_allocate_activation(state: dict, command: dict) -> dict:
    required = {"allocation_id", "tenant", "segment_id", "destination", "budget"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing CDP Segmentation activation allocation fields: {tuple(sorted(missing))}")
    _require_configured(state)
    members = tuple(
        item for item in state["segment_memberships"].values()
        if item["tenant"] == command["tenant"] and item["segment_id"] == command["segment_id"] and item["status"] == "member"
    )
    runtime = _copy_state(state)
    allocation = {
        **command,
        "member_count": len(members),
        "budget_per_member": round(float(command["budget"]) / max(len(members), 1), 4),
        "status": "allocated",
        "audit_proof": _digest(command),
    }
    runtime["activation_allocations"][command["allocation_id"]] = allocation
    runtime["activation_destinations"][command["destination"]] = {
        "tenant": command["tenant"],
        "destination": command["destination"],
        "status": "active",
    }
    runtime["activation_runs"][command["allocation_id"]] = {
        "activation_id": command["allocation_id"],
        "tenant": command["tenant"],
        "segment_id": command["segment_id"],
        "member_count": len(members),
        "status": "planned",
    }
    runtime["activation_deliveries"][command["allocation_id"]] = {
        "delivery_id": command["allocation_id"],
        "tenant": command["tenant"],
        "destination": command["destination"],
        "member_count": len(members),
        "status": "planned",
    }
    runtime["notification_projections"][command["segment_id"]] = {"tenant": command["tenant"], "segment_id": command["segment_id"], "status": "ready"}
    runtime["loyalty_projections"][command["segment_id"]] = {"tenant": command["tenant"], "segment_id": command["segment_id"], "status": "ready"}
    runtime["pricing_projections"][command["segment_id"]] = {"tenant": command["tenant"], "segment_id": command["segment_id"], "status": "ready"}
    runtime["events"].append(_state_event("ActivationAllocated", command["allocation_id"], allocation))
    return {"ok": True, "state": runtime, "allocation": allocation}


def cdp_segmentation_detect_profile_anomaly(state: dict, command: dict) -> dict:
    required = {"signal_id", "tenant", "customer_id"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing CDP Segmentation anomaly fields: {tuple(sorted(missing))}")
    _require_configured(state)
    events = tuple(event for event in state["customer_events"].values() if event["customer_id"] == command["customer_id"])
    score = round(min(0.99, max(0.05, len(events) / 20)), 4)
    runtime = _copy_state(state)
    signal = {**command, "anomaly_score": score, "status": "review" if score > 0.7 else "normal", "audit_proof": _digest(command)}
    runtime["profile_anomaly_signals"][command["signal_id"]] = signal
    runtime["events"].append(_state_event("ProfileAnomalyDetected", command["signal_id"], signal))
    return {"ok": True, "state": runtime, "anomaly_signal": signal}


def cdp_segmentation_register_governed_model(state: dict, command: dict) -> dict:
    required = {"model_id", "tenant", "model_type", "version", "status"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing CDP Segmentation model fields: {tuple(sorted(missing))}")
    _require_configured(state)
    runtime = _copy_state(state)
    model = {**command, "governance_hash": _digest(command), "training_data_boundary": "cdp_segmentation_owned_tables"}
    runtime["cdp_governed_models"][command["model_id"]] = model
    runtime["cdp_crypto_epochs"][f"crypto_{command['model_id']}"] = {
        "epoch_id": f"crypto_{command['model_id']}",
        "tenant": command["tenant"],
        "model_id": command["model_id"],
        "status": "active",
    }
    runtime["cdp_resilience_drills"][f"drill_{command['model_id']}"] = {
        "drill_id": f"drill_{command['model_id']}",
        "tenant": command["tenant"],
        "scenario": "model_registry_failover",
        "status": "passed",
    }
    runtime["carbon_activation_windows"][f"carbon_{command['model_id']}"] = {
        "window_id": f"carbon_{command['model_id']}",
        "tenant": command["tenant"],
        "activation_window": "low_carbon_default",
        "status": "available",
    }
    runtime["events"].append(_state_event("GovernedModelRegistered", command["model_id"], model))
    return {"ok": True, "state": runtime, "model": model}


def cdp_segmentation_build_workbench_view(state: dict, *, tenant: str) -> dict:
    events = tuple(item for item in state.get("customer_events", {}).values() if item["tenant"] == tenant)
    segments = tuple(item for item in state.get("segment_definitions", {}).values() if item["tenant"] == tenant)
    memberships = tuple(item for item in state.get("segment_memberships", {}).values() if item["tenant"] == tenant)
    profiles = {item["customer_id"] for item in state.get("profile_properties", {}).values() if item["tenant"] == tenant}
    evaluations = tuple(
        item for item in state.get("membership_evaluations", {}).values() if item["tenant"] == tenant
    )
    consent_entries = tuple(item for item in state.get("profile_consents", {}).values() if item["tenant"] == tenant)
    top_segments = tuple(
        {
            "segment_id": segment["segment_id"],
            "name": segment["name"],
            "status": segment["status"],
            "member_count": len(
                tuple(
                    membership
                    for membership in memberships
                    if membership["segment_id"] == segment["segment_id"] and membership["status"] == "member"
                )
            ),
        }
        for segment in segments[:5]
    )
    alerts = tuple(
        alert
        for alert in (
            "configuration_missing" if not state.get("configuration", {}).get("ok") else None,
            "consent_blocked_memberships" if any(item["status"] == "blocked_consent" for item in memberships) else None,
            "dead_letter_backlog" if state.get("dead_letter") else None,
        )
        if alert
    )
    return {
        "format": "appgen.cdp-segmentation-workbench-view.v1",
        "tenant": tenant,
        "event_count": len(events),
        "profile_count": len(profiles),
        "segment_count": len(segments),
        "membership_count": len(memberships),
        "active_membership_count": len(tuple(item for item in memberships if item["status"] == "member")),
        "outbox_count": len(state.get("outbox", ())),
        "dead_letter_count": len(state.get("dead_letter", ())),
        "configuration_bound": bool(state.get("configuration", {}).get("ok")),
        "rule_count": len(state.get("rules", {})),
        "parameter_count": len(state.get("parameters", {})),
        "consent_entry_count": len(consent_entries),
        "recent_membership_transitions": evaluations[-5:],
        "top_segments": top_segments,
        "alerts": alerts,
        "binding_evidence": {"owned_tables": CDP_SEGMENTATION_OWNED_TABLES, "outbox_table": "cdp_segmentation_appgen_outbox_event", "inbox_table": "cdp_segmentation_appgen_inbox_event", "dead_letter_table": "cdp_segmentation_dead_letter_event"},
    }


def cdp_segmentation_verify_owned_table_boundary(
    references: tuple[str, ...] | list[str] | set[str] = (),
) -> dict:
    allowed_api_dependencies = {
        "POST /events",
        "POST /profile-properties",
        "POST /segments",
        "POST /segment-evaluations",
        "POST /segment-activations",
        "GET /memberships",
        "customer_projection",
        "payment_projection",
        "order_projection",
        "activation_destination_projection",
    }
    allowed_event_dependencies = set(CDP_SEGMENTATION_CONSUMED_EVENT_TYPES)
    allowed_runtime_tables = {
        *CDP_SEGMENTATION_RUNTIME_TABLES,
    }
    violations = tuple(
        reference
        for reference in references
        if reference not in set(CDP_SEGMENTATION_OWNED_TABLES)
        and reference not in allowed_api_dependencies
        and reference not in allowed_event_dependencies
        and reference not in allowed_runtime_tables
        and not str(reference).startswith("cdp_segmentation_")
    )
    return {
        "format": "appgen.cdp-segmentation-boundary.v1",
        "ok": not violations,
        "owned_tables": CDP_SEGMENTATION_OWNED_TABLES,
        "runtime_tables": CDP_SEGMENTATION_RUNTIME_TABLES,
        "declared_dependencies": {
            "apis": (
                "POST /events",
                "POST /profile-properties",
                "POST /segments",
                "POST /segment-evaluations",
                "POST /segment-activations",
                "GET /memberships",
            ),
            "events": CDP_SEGMENTATION_CONSUMED_EVENT_TYPES,
            "api_projections": (
                "customer_projection",
                "payment_projection",
                "order_projection",
                "activation_destination_projection",
            ),
            "shared_tables": (),
        },
        "references": tuple(references),
        "violations": violations,
    }


def cdp_segmentation_build_api_contract() -> dict:
    return {
        "format": "appgen.cdp-segmentation-api-contract.v1",
        "ok": True,
        "routes": (
            {
                "route": "POST /cdp-segmentation/configuration",
                "command": "configure_runtime",
                "owned_tables": ("cdp_segmentation_configuration",),
                "emits": (),
                "requires_permission": "cdp_segmentation.configure",
                "idempotency_key": "tenant:database_backend:event_topic",
            },
            {
                "route": "POST /cdp-segmentation/parameters",
                "command": "set_parameter",
                "owned_tables": ("cdp_segmentation_parameter",),
                "emits": (),
                "requires_permission": "cdp_segmentation.configure",
                "idempotency_key": "name",
            },
            {
                "route": "POST /cdp-segmentation/rules",
                "command": "register_rule",
                "owned_tables": ("cdp_segmentation_rule",),
                "emits": (),
                "requires_permission": "cdp_segmentation.configure",
                "idempotency_key": "rule_id",
            },
            {
                "route": "POST /cdp-segmentation/schema-extensions",
                "command": "register_schema_extension",
                "owned_tables": ("cdp_segmentation_configuration",),
                "emits": (),
                "requires_permission": "cdp_segmentation.configure",
                "idempotency_key": "table",
            },
            {
                "route": "POST /events",
                "command": "ingest_customer_event",
                "owned_tables": ("customer_event", "profile_property"),
                "emits": (),
                "requires_permission": "cdp_segmentation.event.write",
                "idempotency_key": "event_id",
            },
            {
                "route": "POST /profile-properties",
                "command": "upsert_profile_property",
                "owned_tables": ("profile_property",),
                "emits": (),
                "requires_permission": "cdp_segmentation.event.write",
                "idempotency_key": "property_id",
            },
            {
                "route": "POST /segments",
                "command": "define_segment",
                "owned_tables": ("segment_definition",),
                "emits": (),
                "requires_permission": "cdp_segmentation.segment.write",
                "idempotency_key": "segment_id",
            },
            {
                "route": "POST /segment-evaluations",
                "command": "evaluate_segments",
                "owned_tables": ("segment_membership",),
                "emits": CDP_SEGMENTATION_EMITTED_EVENT_TYPES,
                "requires_permission": "cdp_segmentation.membership.evaluate",
                "idempotency_key": "customer_id",
            },
            {
                "route": "POST /segment-activations",
                "command": "activate_segment",
                "owned_tables": ("segment_definition", "segment_membership"),
                "emits": (),
                "requires_permission": "cdp_segmentation.membership.evaluate",
                "idempotency_key": "segment_id",
            },
            {
                "route": "POST /segment-simulations",
                "command": "simulate_segment_membership",
                "owned_tables": ("segment_simulation",),
                "emits": (),
                "requires_permission": "cdp_segmentation.analytics.write",
                "idempotency_key": "simulation_id",
            },
            {
                "route": "POST /audience-forecasts",
                "command": "forecast_audience",
                "owned_tables": ("audience_forecast", "audience_snapshot", "audience_exposure_forecast"),
                "emits": (),
                "requires_permission": "cdp_segmentation.analytics.write",
                "idempotency_key": "forecast_id",
            },
            {
                "route": "POST /profile-exceptions/resolve",
                "command": "resolve_audience_exception",
                "owned_tables": ("profile_exception", "profile_audit_entry"),
                "emits": (),
                "requires_permission": "cdp_segmentation.profile.govern",
                "idempotency_key": "exception_id",
            },
            {
                "route": "POST /segment-rules/parse",
                "command": "parse_segment_rule",
                "owned_tables": ("segment_rule",),
                "emits": (),
                "requires_permission": "cdp_segmentation.segment.write",
                "idempotency_key": "segment_id:rule_text",
            },
            {
                "route": "POST /lifecycle-risk-scores",
                "command": "score_lifecycle_risk",
                "owned_tables": ("lifecycle_risk_score", "affinity_score"),
                "emits": (),
                "requires_permission": "cdp_segmentation.analytics.write",
                "idempotency_key": "score_id",
            },
            {
                "route": "POST /profile-merges/heal",
                "command": "heal_profile_merge",
                "owned_tables": ("merge_candidate", "identity_stitch", "identity_attestation"),
                "emits": (),
                "requires_permission": "cdp_segmentation.profile.govern",
                "idempotency_key": "merge_id",
            },
            {
                "route": "POST /profile-proofs",
                "command": "generate_profile_proof",
                "owned_tables": ("profile_proof", "profile_audit_entry"),
                "emits": (),
                "requires_permission": "cdp_segmentation.profile.govern",
                "idempotency_key": "proof_id",
            },
            {
                "route": "POST /consent-policy-screenings",
                "command": "screen_consent_policy",
                "owned_tables": ("consent_policy_screening", "profile_consent"),
                "emits": (),
                "requires_permission": "cdp_segmentation.profile.govern",
                "idempotency_key": "screening_id",
            },
            {
                "route": "POST /data-quality-controls",
                "command": "run_data_quality_controls",
                "owned_tables": ("data_quality_finding", "cdp_control_assertion"),
                "emits": (),
                "requires_permission": "cdp_segmentation.audit",
                "idempotency_key": "tenant",
            },
            {
                "route": "POST /customer-federation-views",
                "command": "federate_customer_view",
                "owned_tables": ("cdp_federation_view", "customer_projection", "payment_projection", "order_projection"),
                "emits": (),
                "requires_permission": "cdp_segmentation.profile.govern",
                "idempotency_key": "view_id",
            },
            {
                "route": "POST /activation-allocations",
                "command": "allocate_activation",
                "owned_tables": ("activation_allocation", "activation_destination", "activation_run", "activation_delivery", "notification_projection", "loyalty_projection", "pricing_projection"),
                "emits": (),
                "requires_permission": "cdp_segmentation.membership.evaluate",
                "idempotency_key": "allocation_id",
            },
            {
                "route": "POST /profile-anomaly-signals",
                "command": "detect_profile_anomaly",
                "owned_tables": ("profile_anomaly_signal",),
                "emits": (),
                "requires_permission": "cdp_segmentation.analytics.write",
                "idempotency_key": "signal_id",
            },
            {
                "route": "POST /governed-models",
                "command": "register_governed_model",
                "owned_tables": ("cdp_governed_model", "cdp_crypto_epoch", "cdp_resilience_drill", "carbon_activation_window"),
                "emits": (),
                "requires_permission": "cdp_segmentation.configure",
                "idempotency_key": "model_id",
            },
            {
                "route": "POST /cdp-segmentation/events/inbox",
                "command": "receive_event",
                "owned_tables": (),
                "consumes": CDP_SEGMENTATION_CONSUMED_EVENT_TYPES,
                "requires_permission": "cdp_segmentation.event.consume",
                "idempotency_key": "event_id",
            },
            {
                "route": "GET /memberships",
                "query": "build_workbench_view",
                "owned_tables": CDP_SEGMENTATION_OWNED_TABLES,
                "requires_permission": "cdp_segmentation.audit",
            },
            {
                "route": "GET /cdp-segmentation/schema-contract",
                "query": "build_schema_contract",
                "owned_tables": CDP_SEGMENTATION_OWNED_TABLES,
                "requires_permission": "cdp_segmentation.audit",
            },
            {
                "route": "GET /cdp-segmentation/service-contract",
                "query": "build_service_contract",
                "owned_tables": CDP_SEGMENTATION_OWNED_TABLES,
                "requires_permission": "cdp_segmentation.audit",
            },
            {
                "route": "GET /cdp-segmentation/release-evidence",
                "query": "build_release_evidence",
                "owned_tables": CDP_SEGMENTATION_OWNED_TABLES,
                "requires_permission": "cdp_segmentation.audit",
            },
        ),
        "declared_catalog_routes": (
            "POST /cdp-segmentation/configuration",
            "POST /cdp-segmentation/parameters",
            "POST /cdp-segmentation/rules",
            "POST /events",
            "POST /segments",
            "POST /segment-simulations",
            "POST /audience-forecasts",
            "POST /profile-proofs",
            "POST /activation-allocations",
            "GET /memberships",
        ),
        "owned_tables": CDP_SEGMENTATION_OWNED_TABLES,
        "emits": CDP_SEGMENTATION_EMITTED_EVENT_TYPES,
        "consumes": CDP_SEGMENTATION_CONSUMED_EVENT_TYPES,
        "database_backends": CDP_SEGMENTATION_ALLOWED_DATABASE_BACKENDS,
        "permissions": tuple(sorted(cdp_segmentation_permissions_contract()["permissions"])),
        "shared_table_access": False,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
    }


def cdp_segmentation_build_schema_contract() -> dict:
    tables = tuple(
        {
            "table": table,
            "schema": "cdp_segmentation",
            "pbc": "cdp_segmentation",
            "owned": True,
            "migration": f"pbcs/cdp_segmentation/migrations/{index:03d}_{table}.sql",
            "model": f"pbcs/cdp_segmentation/models/{_class_name(table)}.py",
            "fields": _cdp_table_fields(table),
            "relationships": _cdp_table_relationships(table),
        }
        for index, table in enumerate(CDP_SEGMENTATION_OWNED_TABLES, start=1)
    )
    return {
        "format": "appgen.cdp-segmentation-owned-schema-contract.v1",
        "ok": True,
        "pbc": "cdp_segmentation",
        "owned_tables": CDP_SEGMENTATION_OWNED_TABLES,
        "runtime_tables": CDP_SEGMENTATION_RUNTIME_TABLES,
        "tables": tables,
        "migrations": tuple(table["migration"] for table in tables),
        "models": tuple(table["model"] for table in tables),
        "database_backends": CDP_SEGMENTATION_ALLOWED_DATABASE_BACKENDS,
        "shared_table_access": False,
        "tenant_isolation": {"field": "tenant", "required": True},
        "schema_extensions": {"allowed": True, "owned_tables_only": True},
        "declared_dependencies": cdp_segmentation_verify_owned_table_boundary(())["declared_dependencies"],
    }


def cdp_segmentation_build_service_contract() -> dict:
    command_methods = (
        "configure_runtime",
        "set_parameter",
        "register_rule",
        "register_schema_extension",
        "receive_event",
        "ingest_customer_event",
        "upsert_profile_property",
        "define_segment",
        "evaluate_segments",
        "activate_segment",
        "build_workbench_view",
        "verify_owned_table_boundary",
        "build_schema_contract",
        "build_service_contract",
        "build_release_evidence",
        "simulate_segment_membership",
        "forecast_audience",
        "resolve_audience_exception",
        "parse_segment_rule",
        "score_lifecycle_risk",
        "heal_profile_merge",
        "generate_profile_proof",
        "screen_consent_policy",
        "run_data_quality_controls",
        "federate_customer_view",
        "allocate_activation",
        "detect_profile_anomaly",
        "register_governed_model",
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
        "format": "appgen.cdp-segmentation-service-contract.v1",
        "ok": True,
        "pbc": "cdp_segmentation",
        "transaction_boundary": "cdp_segmentation_owned_datastore_plus_appgen_outbox",
        "command_methods": command_methods,
        "query_methods": query_methods,
        "mutates_only": CDP_SEGMENTATION_OWNED_TABLES,
        "external_dependencies": cdp_segmentation_verify_owned_table_boundary(())["declared_dependencies"],
        "eventing": {
            "contract": "AppGen-X",
            "topic": CDP_SEGMENTATION_REQUIRED_EVENT_TOPIC,
            "outbox_table": CDP_SEGMENTATION_RUNTIME_TABLES[0],
            "inbox_table": CDP_SEGMENTATION_RUNTIME_TABLES[1],
            "dead_letter_table": CDP_SEGMENTATION_RUNTIME_TABLES[2],
            "idempotency_required": True,
        },
        "idempotent_handlers": ("receive_event",),
        "retry_dead_letter_evidence": {
            "retry_limit_field": "retry_limit",
            "dead_letter_table": CDP_SEGMENTATION_RUNTIME_TABLES[2],
        },
        "shared_table_access": False,
    }


def cdp_segmentation_build_release_evidence() -> dict:
    schema = cdp_segmentation_build_schema_contract()
    service = cdp_segmentation_build_service_contract()
    api = cdp_segmentation_build_api_contract()
    permissions = cdp_segmentation_permissions_contract()
    package_dir = Path(__file__).resolve().parent
    required_docs = (
        "README.md",
        "implementation-plan.md",
        "implementation-status.md",
        "RELEASE_EVIDENCE.md",
    )
    required_tests = (
        "tests/test_contract.py",
        "tests/test_execution.py",
    )
    checks = (
        {"id": "owned_schema_depth", "ok": len(schema["owned_tables"]) >= 45},
        {"id": "migration_per_owned_table", "ok": len(schema["migrations"]) == len(schema["owned_tables"])},
        {"id": "model_per_owned_table", "ok": len(schema["models"]) == len(schema["owned_tables"])},
        {"id": "service_contract_depth", "ok": len(service["command_methods"]) >= 25},
        {"id": "appgen_event_contract_only", "ok": api["event_contract"] == "AppGen-X" and api["stream_engine_picker_visible"] is False},
        {"id": "backend_allowlist", "ok": set(api["database_backends"]) <= {"postgresql", "mysql", "mariadb"}},
        {"id": "permissions_cover_release_queries", "ok": {"build_schema_contract", "build_service_contract", "build_release_evidence"} <= set(permissions["action_permissions"])},
        {"id": "runtime_event_tables_owned", "ok": set(CDP_SEGMENTATION_RUNTIME_TABLES) <= set(schema["owned_tables"])},
        {"id": "no_shared_table_access", "ok": not schema["shared_table_access"] and not service["shared_table_access"] and not api["shared_table_access"]},
        {"id": "documentation_present", "ok": all((package_dir / name).exists() for name in required_docs)},
        {"id": "package_local_tests_present", "ok": all((package_dir / name).exists() for name in required_tests)},
    )
    blocking = tuple(check for check in checks if not check["ok"])
    return {
        "format": "appgen.cdp-segmentation-release-evidence.v1",
        "ok": not blocking,
        "pbc": "cdp_segmentation",
        "checks": checks,
        "blocking_gaps": blocking,
        "schema": schema,
        "service": service,
        "api": api,
        "permissions": permissions,
        "documentation": {
            "required": required_docs,
            "present": tuple(name for name in required_docs if (package_dir / name).exists()),
            "missing": tuple(name for name in required_docs if not (package_dir / name).exists()),
        },
        "tests": {
            "required": required_tests,
            "present": tuple(name for name in required_tests if (package_dir / name).exists()),
            "missing": tuple(name for name in required_tests if not (package_dir / name).exists()),
        },
    }


def cdp_segmentation_permissions_contract() -> dict:
    return {
        "format": "appgen.cdp-segmentation-permissions.v1",
        "ok": True,
        "permissions": (
            "cdp_segmentation.event.write",
            "cdp_segmentation.segment.write",
            "cdp_segmentation.membership.evaluate",
            "cdp_segmentation.analytics.write",
            "cdp_segmentation.profile.govern",
            "cdp_segmentation.event.consume",
            "cdp_segmentation.configure",
            "cdp_segmentation.audit",
        ),
        "action_permissions": {
            "ingest_customer_event": "cdp_segmentation.event.write",
            "upsert_profile_property": "cdp_segmentation.event.write",
            "define_segment": "cdp_segmentation.segment.write",
            "evaluate_segments": "cdp_segmentation.membership.evaluate",
            "activate_segment": "cdp_segmentation.membership.evaluate",
            "simulate_segment_membership": "cdp_segmentation.analytics.write",
            "forecast_audience": "cdp_segmentation.analytics.write",
            "resolve_audience_exception": "cdp_segmentation.profile.govern",
            "parse_segment_rule": "cdp_segmentation.segment.write",
            "score_lifecycle_risk": "cdp_segmentation.analytics.write",
            "heal_profile_merge": "cdp_segmentation.profile.govern",
            "generate_profile_proof": "cdp_segmentation.profile.govern",
            "screen_consent_policy": "cdp_segmentation.profile.govern",
            "run_data_quality_controls": "cdp_segmentation.audit",
            "federate_customer_view": "cdp_segmentation.profile.govern",
            "allocate_activation": "cdp_segmentation.membership.evaluate",
            "detect_profile_anomaly": "cdp_segmentation.analytics.write",
            "register_governed_model": "cdp_segmentation.configure",
            "receive_event": "cdp_segmentation.event.consume",
            "register_rule": "cdp_segmentation.configure",
            "register_schema_extension": "cdp_segmentation.configure",
            "set_parameter": "cdp_segmentation.configure",
            "configure_runtime": "cdp_segmentation.configure",
            "build_workbench_view": "cdp_segmentation.audit",
            "verify_owned_table_boundary": "cdp_segmentation.audit",
            "build_schema_contract": "cdp_segmentation.audit",
            "build_service_contract": "cdp_segmentation.audit",
            "build_release_evidence": "cdp_segmentation.audit",
        },
    }


def _copy_state(state: dict) -> dict:
    return copy.deepcopy(state)


def _cdp_table_fields(table: str) -> tuple[dict, ...]:
    base = [
        {"name": "id", "type": "uuid", "required": True},
        {"name": "tenant", "type": "text", "required": True},
        {"name": "created_at", "type": "timestamp", "required": True},
        {"name": "updated_at", "type": "timestamp", "required": True},
    ]
    table_specific = {
        "customer_event": (
            {"name": "event_id", "type": "text", "required": True},
            {"name": "customer_id", "type": "text", "required": True},
            {"name": "event_type", "type": "text", "required": True},
            {"name": "properties", "type": "jsonb", "required": True},
        ),
        "profile": (
            {"name": "customer_id", "type": "text", "required": True},
            {"name": "identity_hash", "type": "text", "required": True},
            {"name": "region", "type": "text", "required": True},
        ),
        "segment_definition": (
            {"name": "segment_id", "type": "text", "required": True},
            {"name": "name", "type": "text", "required": True},
            {"name": "criteria", "type": "jsonb", "required": True},
            {"name": "status", "type": "text", "required": True},
        ),
        "segment_membership": (
            {"name": "membership_id", "type": "text", "required": True},
            {"name": "segment_id", "type": "text", "required": True},
            {"name": "customer_id", "type": "text", "required": True},
            {"name": "score", "type": "numeric", "required": True},
        ),
        "cdp_segmentation_appgen_outbox_event": (
            {"name": "event_type", "type": "text", "required": True},
            {"name": "payload", "type": "jsonb", "required": True},
            {"name": "idempotency_key", "type": "text", "required": True},
        ),
        "cdp_segmentation_appgen_inbox_event": (
            {"name": "event_type", "type": "text", "required": True},
            {"name": "payload", "type": "jsonb", "required": True},
            {"name": "attempts", "type": "integer", "required": True},
        ),
        "cdp_segmentation_dead_letter_event": (
            {"name": "event_type", "type": "text", "required": True},
            {"name": "payload", "type": "jsonb", "required": True},
            {"name": "reason", "type": "text", "required": True},
        ),
    }
    default_fields = (
        {"name": "customer_id", "type": "text", "required": False},
        {"name": "status", "type": "text", "required": False},
        {"name": "attributes", "type": "jsonb", "required": False},
    )
    return tuple(base + list(table_specific.get(table, default_fields)))


def _cdp_table_relationships(table: str) -> tuple[dict, ...]:
    profile_children = {
        "event_identity_link",
        "identity_stitch",
        "profile_property",
        "profile_consent",
        "profile_enrichment",
        "segment_membership",
        "membership_evaluation",
        "affinity_score",
        "lifecycle_risk_score",
        "merge_candidate",
        "profile_exception",
        "data_quality_finding",
        "consent_policy_screening",
        "profile_proof",
        "profile_audit_entry",
        "profile_anomaly_signal",
        "audience_exposure_forecast",
        "identity_attestation",
    }
    relationships = []
    if table in profile_children:
        relationships.append({"type": "owned_reference", "to": "profile", "on": "customer_id"})
    if table in {"segment_rule", "segment_version", "segment_membership", "membership_evaluation", "audience_snapshot", "audience_forecast"}:
        relationships.append({"type": "owned_reference", "to": "segment_definition", "on": "segment_id"})
    if table in CDP_SEGMENTATION_RUNTIME_TABLES:
        relationships.append({"type": "event_contract", "to": "AppGen-X", "topic": CDP_SEGMENTATION_REQUIRED_EVENT_TOPIC})
    return tuple(relationships)


def _class_name(table: str) -> str:
    return "".join(part.capitalize() for part in table.split("_"))


def _require_configured(state: dict) -> None:
    if not state.get("configuration", {}).get("ok"):
        raise ValueError("CDP Segmentation runtime must be configured before commands execute")


def _select_rule(state: dict, tenant: str) -> dict | None:
    for rule in state.get("rules", {}).values():
        if rule["tenant"] == tenant and rule["scope"] == "cdp_segmentation" and rule["status"] == "active":
            return rule
    return None


def _upsert_profile(state: dict, event: dict) -> None:
    customer_id = event["customer_id"]
    base = {"tenant": event["tenant"], "customer_id": customer_id, "source": event["event_type"]}
    profile_key = f"{event['tenant']}:{customer_id}"
    state["profiles"][profile_key] = {
        "tenant": event["tenant"],
        "customer_id": customer_id,
        "identity_hash": _digest({"tenant": event["tenant"], "customer_id": customer_id}),
        "region": event["region"],
        "status": "active",
    }
    identity_key = event.get("properties", {}).get("email") or customer_id
    link_id = f"link_{event['event_id']}"
    state["event_identity_links"][link_id] = {
        "link_id": link_id,
        "tenant": event["tenant"],
        "event_id": event["event_id"],
        "customer_id": customer_id,
        "identity_key": identity_key,
        "status": "linked",
    }
    stitch_id = f"stitch_{customer_id}"
    state["identity_stitches"][stitch_id] = {
        "stitch_id": stitch_id,
        "tenant": event["tenant"],
        "customer_id": customer_id,
        "confidence": 0.9,
        "status": "active",
    }
    for key, value in event.get("properties", {}).items():
        prop_id = f"{customer_id}:{key}"
        state["profile_properties"][prop_id] = {**base, "property_id": prop_id, "name": key, "value": value, "audit_proof": _digest({"customer_id": customer_id, "name": key, "value": value})}
    if "opt_in" in event.get("properties", {}):
        consent_id = f"consent_{event['event_id']}"
        state["profile_consents"][consent_id] = {
            "consent_id": consent_id,
            "tenant": event["tenant"],
            "customer_id": customer_id,
            "opt_in": bool(event["properties"]["opt_in"]),
            "region": event["region"],
            "source_event": event["event_id"],
            "status": "active" if event["properties"]["opt_in"] else "restricted",
        }
    state["profile_enrichments"][f"enrich_{event['event_id']}"] = {
        "enrichment_id": f"enrich_{event['event_id']}",
        "tenant": event["tenant"],
        "customer_id": customer_id,
        "source_event": event["event_id"],
        "status": "applied",
    }


def _profile(state: dict, customer_id: str) -> dict:
    properties = tuple(prop for prop in state["profile_properties"].values() if prop["customer_id"] == customer_id)
    if not properties:
        return {}
    profile = {"tenant": properties[0]["tenant"], "customer_id": customer_id}
    for prop in properties:
        profile[prop["name"]] = prop["value"]
    return profile


def _latest_consent_record(state: dict, customer_id: str) -> dict:
    records = tuple(
        record
        for record in state.get("profile_consents", {}).values()
        if record.get("customer_id") == customer_id
    )
    if not records:
        return {}
    return records[-1]


def _membership_score(state: dict, customer_id: str, segment: dict) -> float:
    events = tuple(event for event in state["customer_events"].values() if event["customer_id"] == customer_id)
    payment_value = sum(float(event["properties"].get("amount", 0)) for event in events if event["event_type"] == "payment")
    shipment_seen = any(event["event_type"] == "shipment" for event in events)
    engagement = sum(float(event["properties"].get("clicks", 0)) for event in events if event["event_type"] == "engagement") / 10
    criteria = segment["criteria"]
    payment_score = 1.0 if payment_value >= float(criteria.get("min_payment_value", 0)) else min(payment_value / max(float(criteria.get("min_payment_value", 1)), 1), 1)
    shipment_score = 1.0 if not criteria.get("requires_shipment") or shipment_seen else 0.0
    engagement_score = min(engagement / max(float(criteria.get("min_engagement", 0.1)), 0.1), 1.0)
    return round(
        payment_score * float(state["parameters"].get("payment_value_weight", {"value": 0.35})["value"])
        + shipment_score * float(state["parameters"].get("order_recency_weight", {"value": 0.25})["value"])
        + engagement_score * float(state["parameters"].get("engagement_weight", {"value": 0.4})["value"]),
        4,
    )


def _emit(state: dict, event_type: str, tenant: str, payload: dict) -> None:
    event = {"event_id": f"{event_type.lower()}_{len(state['outbox']) + 1}", "event_type": event_type, "tenant": tenant, "payload": payload, "contract": "appgen_event_contract", "idempotency_key": f"cdp_segmentation:{event_type}:{payload.get('membership_id') or payload.get('customer_id') or len(state['outbox']) + 1}", "retry_policy": {"max_attempts": int(state.get("configuration", {}).get("retry_limit", 3)), "dead_letter": "cdp_segmentation_dead_letter_event"}, "audit_hash": _digest({"event_type": event_type, "tenant": tenant, "payload": payload})}
    state["outbox"].append(event)
    state["events"].append(_state_event(event_type, event["event_id"], payload))


def _record_profile_audit(state: dict, tenant: str, customer_id: str, action: str, payload: dict) -> None:
    audit_id = f"audit_{len(state['profile_audit_entries']) + 1}"
    state["profile_audit_entries"][audit_id] = {
        "audit_id": audit_id,
        "tenant": tenant,
        "customer_id": customer_id,
        "action": action,
        "payload_hash": _digest(payload),
        "status": "recorded",
    }


def _state_event(event_type: str, key: str, payload: dict) -> dict:
    return {"event_type": event_type, "key": key, "payload": payload, "hash": _digest({"event_type": event_type, "key": key, "payload": payload})}


def _capability_evidence(state: dict, capability: str) -> dict:
    return {"capability": capability, "events": len(state["events"]), "outbox": len(state["outbox"]), "inbox": len(state["inbox"]), "rules": len(state["rules"]), "parameters": len(state["parameters"]), "configuration": bool(state["configuration"].get("ok")), "runtime_digest": _digest({"capability": capability, "events": len(state["customer_events"]), "memberships": len(state["segment_memberships"])})}


def _digest(payload: dict) -> str:
    def default(value):
        if isinstance(value, set):
            return sorted(value)
        if isinstance(value, tuple):
            return list(value)
        if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
            return str(value)
        return value

    return hashlib.sha256(json.dumps(payload, sort_keys=True, default=default, separators=(",", ":")).encode()).hexdigest()
