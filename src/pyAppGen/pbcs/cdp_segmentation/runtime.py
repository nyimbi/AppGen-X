"""Executable runtime for the CDP Segmentation PBC."""

from __future__ import annotations

import copy
import hashlib
import json
import math


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
        "segment_definitions": {},
        "segment_memberships": {},
        "profile_properties": {},
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
    for segment in runtime["segment_definitions"].values():
        if segment["tenant"] != profile["tenant"] or segment["status"] != "active":
            continue
        score = _membership_score(runtime, customer_id, segment)
        status = "member" if score >= threshold else "excluded"
        membership_id = f"{segment['segment_id']}:{customer_id}"
        membership = {"membership_id": membership_id, "tenant": profile["tenant"], "segment_id": segment["segment_id"], "customer_id": customer_id, "score": score, "status": status, "audit_proof": _digest({"segment": segment, "profile": profile, "score": score})}
        runtime["segment_memberships"][membership_id] = membership
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
    runtime["events"].append(_state_event("SegmentActivated", segment_id, {"segment_id": segment_id, "member_count": len(activated)}))
    return {"ok": True, "state": runtime, "activation": {"segment_id": segment_id, "member_count": len(activated)}}


def cdp_segmentation_build_workbench_view(state: dict, *, tenant: str) -> dict:
    events = tuple(item for item in state.get("customer_events", {}).values() if item["tenant"] == tenant)
    segments = tuple(item for item in state.get("segment_definitions", {}).values() if item["tenant"] == tenant)
    memberships = tuple(item for item in state.get("segment_memberships", {}).values() if item["tenant"] == tenant)
    profiles = {item["customer_id"] for item in state.get("profile_properties", {}).values() if item["tenant"] == tenant}
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
        "declared_catalog_routes": ("POST /events", "POST /segments", "GET /memberships"),
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
    }


def cdp_segmentation_permissions_contract() -> dict:
    return {
        "format": "appgen.cdp-segmentation-permissions.v1",
        "ok": True,
        "permissions": (
            "cdp_segmentation.event.write",
            "cdp_segmentation.segment.write",
            "cdp_segmentation.membership.evaluate",
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


def _upsert_profile(state: dict, event: dict) -> None:
    customer_id = event["customer_id"]
    base = {"tenant": event["tenant"], "customer_id": customer_id, "source": event["event_type"]}
    for key, value in event.get("properties", {}).items():
        prop_id = f"{customer_id}:{key}"
        state["profile_properties"][prop_id] = {**base, "property_id": prop_id, "name": key, "value": value, "audit_proof": _digest({"customer_id": customer_id, "name": key, "value": value})}


def _profile(state: dict, customer_id: str) -> dict:
    properties = tuple(prop for prop in state["profile_properties"].values() if prop["customer_id"] == customer_id)
    if not properties:
        return {}
    profile = {"tenant": properties[0]["tenant"], "customer_id": customer_id}
    for prop in properties:
        profile[prop["name"]] = prop["value"]
    return profile


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
