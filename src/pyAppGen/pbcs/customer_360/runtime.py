"""Executable runtime for the Customer 360 PBC."""

from __future__ import annotations

import hashlib
import json
import math
import re


CUSTOMER_360_REQUIRED_EVENT_TOPIC = "appgen.customer.events"
CUSTOMER_360_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
CUSTOMER_360_OWNED_TABLES = (
    "customer_profile",
    "customer_identity",
    "customer_relationship",
    "engagement_event",
    "communication_preference",
    "touchpoint",
    "consent_record",
    "customer_timeline",
    "customer_segment_projection",
    "profile_merge_case",
    "customer_rule",
    "customer_parameter",
    "customer_configuration",
)
CUSTOMER_360_EMITTED_EVENT_TYPES = (
    "CustomerUpdated",
    "CustomerIdentityLinked",
    "PreferenceChanged",
    "ConsentRecorded",
    "TouchpointCaptured",
    "CustomerSegmentUpdated",
    "ProfileMergeCaseOpened",
    "ProfileMergeResolved",
)
CUSTOMER_360_CONSUMED_EVENT_TYPES = (
    "InvoiceIssued",
    "PaymentCaptured",
    "OrderVerified",
    "ServiceTicketClosed",
    "LoyaltyRewardEarned",
    "CandidateHired",
)
_CUSTOMER_360_RUNTIME_TABLES = (
    "customer_360_appgen_outbox_event",
    "customer_360_appgen_inbox_event",
    "customer_360_dead_letter_event",
)
_CUSTOMER_360_ALLOWED_DEPENDENCIES = (
    "commerce_customer_projection",
    "billing_account_projection",
    "service_timeline_projection",
    "loyalty_profile_projection",
    "notification_projection",
    "GET /orders/customer-history",
    "GET /billing/accounts",
    "GET /service/tickets",
    "GET /loyalty/profiles",
    "GET /notifications/preferences",
)
_CUSTOMER_360_FORBIDDEN_EVENTING_FIELDS = {
    "eventing_choice",
    "eventing_mode",
    "event_transport",
    "stream_engine",
    "stream_engine_picker",
    "stream_picker",
    "user_eventing_choice",
}
CUSTOMER_360_SUPPORTED_CONFIGURATION_FIELDS = (
    "database_backend",
    "event_topic",
    "retry_limit",
    "allowed_channels",
    "allowed_regions",
    "allowed_identity_types",
    "default_timezone",
    "workbench_limit",
)
_CUSTOMER_360_CONFIGURATION_SEQUENCE_FIELDS = {
    "allowed_channels",
    "allowed_regions",
    "allowed_identity_types",
}
CUSTOMER_360_SUPPORTED_PARAMETER_KEYS = (
    "identity_match_threshold",
    "churn_risk_threshold",
    "engagement_decay_days",
    "minimum_consent_confidence",
    "timeline_limit",
    "retention_days",
    "workbench_limit",
)
CUSTOMER_360_REQUIRED_RULE_FIELDS = (
    "rule_id",
    "tenant",
    "rule_type",
    "allowed_channels",
    "required_consents",
    "status",
)
_CUSTOMER_360_RULE_SEQUENCE_FIELDS = {
    "allowed_channels",
    "required_consents",
    "restricted_regions",
    "identity_match_fields",
    "segment_rules",
}

CUSTOMER_360_RUNTIME_CAPABILITY_KEYS = (
    "event_sourced_customer_lifecycle",
    "graph_relational_customer_topology",
    "multi_tenant_customer_isolation",
    "schema_evolution_resilient_customer_schema",
    "probabilistic_identity_consent_engagement_scoring",
    "real_time_customer_timeline_analytics",
    "counterfactual_preference_segment_simulation",
    "temporal_customer_value_churn_forecasting",
    "autonomous_customer_data_exception_resolution",
    "semantic_customer_instruction_parsing",
    "predictive_customer_health_risk",
    "self_healing_customer_event_route_selection",
    "zero_knowledge_customer_profile_proof",
    "immutable_customer_audit_trail",
    "dynamic_customer_privacy_policy_screening",
    "automated_customer_control_testing",
    "universal_api_async_streaming",
    "cross_system_customer_federation",
    "commerce_billing_service_loyalty_integration",
    "decentralized_customer_identity",
    "chaos_engineered_customer_tolerance",
    "quantum_resistant_customer_authorization",
    "carbon_aware_customer_processing",
    "algebraic_customer_segment_optimization",
    "mechanism_design_channel_allocation",
    "information_theoretic_engagement_anomaly_detection",
    "temporal_customer_exposure_stochastic_modeling",
    "distributed_systems_engineering",
    "probabilistic_ml_customer_health",
    "cryptographic_engineering",
    "mathematical_optimization",
    "customer_mlops_governance",
)
CUSTOMER_360_STANDARD_FEATURE_KEYS = (
    "customer_profile",
    "identity_resolution",
    "relationship_graph",
    "profile_merge_case",
    "survivorship_rules",
    "consent_management",
    "communication_preferences",
    "privacy_policy_screening",
    "touchpoint_capture",
    "engagement_event_ingestion",
    "timeline_projection",
    "channel_history",
    "rfm_metrics",
    "sentiment_signal",
    "churn_signal",
    "segment_projection",
    "customer_read_model",
    "commerce_projection",
    "service_projection",
    "loyalty_projection",
    "notification_projection",
    "event_outbox",
    "event_inbox",
    "idempotent_handlers",
    "retry_dead_letter",
    "permissions",
    "configuration_schema",
    "rule_engine",
    "parameter_engine",
    "owned_datastore_boundary",
    "release_gate",
    "seed_data",
    "appgen_event_contract",
    "workbench",
)


def customer_360_runtime_capabilities() -> dict:
    smoke = customer_360_runtime_smoke()
    return {
        "format": "appgen.customer-360-runtime-capabilities.v1",
        "ok": smoke["ok"],
        "pbc": "customer_360",
        "implementation_directory": "src/pyAppGen/pbcs/customer_360",
        "owned_tables": CUSTOMER_360_OWNED_TABLES,
        "capabilities": CUSTOMER_360_RUNTIME_CAPABILITY_KEYS,
        "standard_features": CUSTOMER_360_STANDARD_FEATURE_KEYS,
        "operations": (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "register_schema_extension",
            "receive_event",
            "create_profile",
            "link_identity",
            "record_consent",
            "set_preference",
            "capture_touchpoint",
            "ingest_engagement_event",
            "open_merge_case",
            "resolve_merge_case",
            "build_timeline",
            "build_api_contract",
            "permissions_contract",
            "verify_owned_table_boundary",
            "build_workbench_view",
        ),
        "smoke": smoke,
    }


def customer_360_runtime_smoke() -> dict:
    state = customer_360_empty_state()
    state = customer_360_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": CUSTOMER_360_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "allowed_channels": ("email", "sms", "web", "mobile", "service"),
            "allowed_regions": ("US", "EU"),
            "allowed_identity_types": ("email", "phone", "loyalty_id", "external_id"),
            "default_timezone": "UTC",
            "workbench_limit": 100,
        },
    )["state"]
    state = customer_360_set_parameter(state, "identity_match_threshold", 0.82)["state"]
    state = customer_360_set_parameter(state, "churn_risk_threshold", 0.65)["state"]
    state = customer_360_set_parameter(state, "engagement_decay_days", 90)["state"]
    state = customer_360_set_parameter(state, "minimum_consent_confidence", 0.9)["state"]
    state = customer_360_set_parameter(state, "timeline_limit", 50)["state"]
    state = customer_360_register_rule(
        state,
        {
            "rule_id": "rule_customer",
            "tenant": "tenant_alpha",
            "rule_type": "privacy",
            "allowed_channels": ("email", "web", "service"),
            "required_consents": ("marketing",),
            "restricted_regions": ("restricted",),
            "identity_match_fields": ("email", "phone"),
            "segment_rules": ("high_value", "at_risk"),
            "status": "active",
        },
    )["state"]
    state = customer_360_register_schema_extension(
        state,
        "customer_profile",
        {"loyalty_payload": "jsonb"},
    )["state"]
    profile = customer_360_create_profile(
        state,
        {
            "profile_id": "cust_100",
            "tenant": "tenant_alpha",
            "display_name": "Ada Lovelace",
            "region": "US",
            "lifecycle_state": "active",
            "account_type": "consumer",
        },
    )
    state = profile["state"]
    identity = customer_360_link_identity(
        state,
        {
            "identity_id": "id_100",
            "tenant": "tenant_alpha",
            "profile_id": "cust_100",
            "identity_type": "email",
            "value": "ada@example.com",
            "confidence": 0.96,
            "verified": True,
        },
    )
    state = identity["state"]
    consent = customer_360_record_consent(
        state,
        {
            "consent_id": "consent_100",
            "tenant": "tenant_alpha",
            "profile_id": "cust_100",
            "purpose": "marketing",
            "region": "US",
            "status": "granted",
            "confidence": 0.95,
        },
    )
    state = consent["state"]
    preference = customer_360_set_preference(
        state,
        {
            "preference_id": "pref_100",
            "tenant": "tenant_alpha",
            "profile_id": "cust_100",
            "channel": "email",
            "status": "opt_in",
            "topic": "offers",
        },
    )
    state = preference["state"]
    touchpoint = customer_360_capture_touchpoint(
        state,
        {
            "touchpoint_id": "tp_100",
            "tenant": "tenant_alpha",
            "profile_id": "cust_100",
            "channel": "web",
            "source": "storefront",
            "occurred_at": "2026-05-26T08:00:00Z",
        },
    )
    state = touchpoint["state"]
    engagement = customer_360_ingest_engagement_event(
        state,
        {
            "event_id": "eng_100",
            "tenant": "tenant_alpha",
            "profile_id": "cust_100",
            "event_type": "purchase",
            "channel": "web",
            "value": 240,
            "sentiment": 0.8,
        },
    )
    state = engagement["state"]
    merge = customer_360_open_merge_case(
        state,
        {
            "merge_case_id": "merge_100",
            "tenant": "tenant_alpha",
            "winning_profile_id": "cust_100",
            "candidate_profile_id": "cust_101",
            "match_score": 0.88,
            "reason": "same_email",
        },
    )
    state = merge["state"]
    resolved_merge = customer_360_resolve_merge_case(state, "merge_100", resolved_by="data_steward")
    state = resolved_merge["state"]
    received = customer_360_receive_event(
        state,
        {
            "event_id": "invoice_evt_100",
            "event_type": "InvoiceIssued",
            "payload": {"tenant": "tenant_alpha", "invoice_id": "inv_100", "profile_id": "cust_100", "amount": 240},
        },
    )
    state = received["state"]
    duplicate = customer_360_receive_event(
        state,
        {
            "event_id": "invoice_evt_100",
            "event_type": "InvoiceIssued",
            "payload": {"tenant": "tenant_alpha", "invoice_id": "inv_100", "profile_id": "cust_100", "amount": 240},
        },
    )
    retried = customer_360_receive_event(
        state,
        {
            "event_id": "unsupported_evt_100",
            "event_type": "UnknownCustomerEvent",
            "payload": {"tenant": "tenant_alpha"},
        },
        simulate_failure=True,
    )
    retried_again = customer_360_receive_event(
        retried["state"],
        {
            "event_id": "unsupported_evt_100",
            "event_type": "UnknownCustomerEvent",
            "payload": {"tenant": "tenant_alpha"},
        },
        simulate_failure=True,
    )
    dead_lettered = customer_360_receive_event(
        retried_again["state"],
        {
            "event_id": "unsupported_evt_100",
            "event_type": "UnknownCustomerEvent",
            "payload": {"tenant": "tenant_alpha"},
        },
        simulate_failure=True,
    )
    state = dead_lettered["state"]
    timeline = customer_360_build_timeline(state, "cust_100")
    simulation = customer_360_simulate_preference_change(state, "cust_100", channel="sms", status="opt_in")
    forecast = customer_360_forecast_customer_value((100, 180, 240), horizon_days=90)
    parsed = customer_360_parse_customer_instruction("customer cust_777 channel email action opt_in topic offers")
    risk = customer_360_score_customer_health({"churn": 0.2, "consent": 0.1, "engagement": 0.3, "value": 0.1})
    recommendation = customer_360_recommend_exception_resolution("duplicate_profile")
    route = customer_360_route_customer_event(
        {"event_id": "cust_route"},
        rails=(
            {"route": "profile_api", "available": False, "latency": 2},
            {"route": "outbox", "available": True, "latency": 4},
        ),
    )
    proof = customer_360_generate_profile_proof(
        state,
        "cust_100",
        disclosure=("profile_id", "region", "lifecycle_state"),
    )
    screening = customer_360_screen_privacy_policy(state, "cust_100", restricted_regions=("restricted",))
    controls = customer_360_run_control_tests(state)
    api = customer_360_build_api_contract()
    permissions = customer_360_permissions_contract()
    boundary = customer_360_verify_owned_table_boundary(
        (
            "customer_profile",
            "customer_360_appgen_inbox_event",
            "InvoiceIssued",
            "commerce_customer_projection",
            "GET /orders/customer-history",
        )
    )
    federation = customer_360_federate_customer_view(
        state,
        "cust_100",
        systems=("commerce", "billing", "service", "loyalty", "notifications"),
    )
    decentralized_identity = customer_360_verify_customer_identity(
        {"did": "did:appgen:customer-100", "issuer": "trusted_registry", "status": "active"}
    )
    resilience = customer_360_run_resilience_drill(state, "profile_api_timeout")
    crypto = customer_360_rotate_crypto_epoch(state, "dilithium3_simulated")
    carbon = customer_360_schedule_carbon_aware_processing(
        ({"window": "day", "carbon": 170}, {"window": "night", "carbon": 70})
    )
    optimization = customer_360_optimize_segments(
        (
            {"segment": "broad", "reach": 0.95, "risk": 0.4},
            {"segment": "consented_high_value", "reach": 0.75, "risk": 0.1},
        )
    )
    allocation = customer_360_allocate_channels(
        ({"channel": "email", "priority": 0.9, "capacity": 8}, {"channel": "service", "priority": 0.5, "capacity": 4}),
        customers=6,
    )
    anomaly = customer_360_detect_engagement_anomaly(state)
    stochastic = customer_360_model_stochastic_customer_exposure(value_path=(100, 200, 260), volatility=0.08)
    workbench = customer_360_build_workbench_view(state, tenant="tenant_alpha")
    model = customer_360_register_governed_model(
        "customer_health",
        {"features": ("engagement", "consent", "value"), "auc": 0.9, "drift_score": 0.04},
    )
    checks = (
        {"id": "event_sourced_customer_lifecycle", "ok": len(state["events"]) >= 8 and state["events"][-1]["hash"]},
        {"id": "graph_relational_customer_topology", "ok": profile["profile"]["graph_degree"] >= 4},
        {"id": "multi_tenant_customer_isolation", "ok": workbench["tenant"] == "tenant_alpha"},
        {"id": "schema_evolution_resilient_customer_schema", "ok": state["schema_extensions"]["customer_profile"]["loyalty_payload"] == "jsonb"},
        {"id": "probabilistic_identity_consent_engagement_scoring", "ok": identity["identity"]["confidence"] > 0.9 and consent["consent"]["confidence"] > 0.9},
        {"id": "real_time_customer_timeline_analytics", "ok": timeline["event_count"] >= 2 and workbench["engagement_event_count"] == 1},
        {"id": "counterfactual_preference_segment_simulation", "ok": simulation["reach_delta"] > 0},
        {"id": "temporal_customer_value_churn_forecasting", "ok": forecast["forecast_value"] > 0},
        {"id": "autonomous_customer_data_exception_resolution", "ok": recommendation["action"] == "open_merge_review"},
        {"id": "semantic_customer_instruction_parsing", "ok": parsed["ok"] and parsed["profile_id"] == "cust_777"},
        {"id": "predictive_customer_health_risk", "ok": risk["risk_score"] > 0},
        {"id": "self_healing_customer_event_route_selection", "ok": route["ok"] and route["route"] == "outbox" and route["failover_used"]},
        {"id": "zero_knowledge_customer_profile_proof", "ok": proof["ok"] and proof["proof"].startswith("zk_customer_")},
        {"id": "immutable_customer_audit_trail", "ok": controls["hash_chain_valid"]},
        {"id": "dynamic_customer_privacy_policy_screening", "ok": screening["ok"] and screening["decision"] == "clear"},
        {"id": "automated_customer_control_testing", "ok": controls["ok"] and not controls["blocking_gaps"]},
        {"id": "universal_api_async_streaming", "ok": api["ok"] and api["event_contract"] == "AppGen-X" and api["shared_table_access"] is False},
        {"id": "cross_system_customer_federation", "ok": federation["ok"] and "service" in federation["systems"]},
        {
            "id": "commerce_billing_service_loyalty_integration",
            "ok": engagement["handoffs"] == (
                "commerce_customer_projection",
                "billing_account_projection",
                "service_timeline_projection",
                "loyalty_profile_projection",
            )
            and received["ok"]
            and state["projections"]["invoice_issues"]["inv_100"]["amount"] == 240,
        },
        {"id": "decentralized_customer_identity", "ok": decentralized_identity["ok"] and decentralized_identity["issuer"] == "trusted_registry"},
        {"id": "chaos_engineered_customer_tolerance", "ok": resilience["ok"] and resilience["mode"] == "degraded_customer_route"},
        {"id": "quantum_resistant_customer_authorization", "ok": crypto["ok"] and crypto["algorithm"] == "dilithium3_simulated"},
        {"id": "carbon_aware_customer_processing", "ok": carbon["window"] == "night"},
        {"id": "algebraic_customer_segment_optimization", "ok": optimization["ok"] and optimization["segment"] == "consented_high_value"},
        {"id": "mechanism_design_channel_allocation", "ok": allocation["ok"] and allocation["allocations"][0]["customers"] > allocation["allocations"][1]["customers"]},
        {"id": "information_theoretic_engagement_anomaly_detection", "ok": anomaly["ok"] and anomaly["entropy"] >= 0},
        {"id": "temporal_customer_exposure_stochastic_modeling", "ok": stochastic["ok"] and stochastic["tail_risk"] > 0},
        {
            "id": "distributed_systems_engineering",
            "ok": state["outbox"][-1]["idempotency_key"].startswith("customer_360:ProfileMergeResolved")
            and duplicate["duplicate"] is True
            and dead_lettered["handler"]["status"] == "dead_letter",
        },
        {"id": "probabilistic_ml_customer_health", "ok": model["ok"] and model["metadata"]["auc"] >= 0.9},
        {"id": "cryptographic_engineering", "ok": proof["hash"] and crypto["epoch"] == 2},
        {
            "id": "mathematical_optimization",
            "ok": optimization["objective_score"] > 0 and allocation["clearing_priority"] > 0 and boundary["ok"] and permissions["ok"],
        },
        {"id": "customer_mlops_governance", "ok": model["governance"]["regulated"] and model["governance"]["explainability_required"]},
    )
    blocking_gaps = tuple(check for check in checks if not check["ok"])
    return {
        "format": "appgen.customer-360-runtime-smoke.v1",
        "ok": not blocking_gaps,
        "checks": checks,
        "blocking_gaps": blocking_gaps,
    }


def customer_360_empty_state() -> dict:
    return {
        "events": (),
        "outbox": (),
        "inbox": (),
        "dead_letter": (),
        "dead_letters": (),
        "handled_events": {},
        "retry_evidence": (),
        "projections": _empty_consumed_event_projections(),
        "profiles": {},
        "identities": {},
        "consents": {},
        "preferences": {},
        "touchpoints": {},
        "engagements": {},
        "merge_cases": {},
        "rules": {},
        "parameters": {},
        "configuration": {},
        "schema_extensions": {},
        "crypto_epoch": {"epoch": 1, "algorithm": "sha3_256"},
    }


def customer_360_configure_runtime(state: dict, configuration: dict) -> dict:
    forbidden = tuple(sorted(field for field in _CUSTOMER_360_FORBIDDEN_EVENTING_FIELDS if field in configuration))
    if forbidden:
        raise ValueError(f"Customer 360 uses the AppGen-X event contract; unsupported eventing fields: {forbidden}")
    unknown = tuple(sorted(field for field in configuration if field not in CUSTOMER_360_SUPPORTED_CONFIGURATION_FIELDS))
    if unknown:
        raise ValueError(f"Unsupported Customer 360 configuration fields: {unknown}")
    missing = tuple(sorted(field for field in CUSTOMER_360_SUPPORTED_CONFIGURATION_FIELDS if field not in configuration))
    if missing:
        raise ValueError(f"Missing required Customer 360 configuration fields: {missing}")
    if configuration.get("database_backend") not in CUSTOMER_360_ALLOWED_DATABASE_BACKENDS:
        raise ValueError("Customer 360 supports only PostgreSQL, MySQL, or MariaDB backends")
    if configuration.get("event_topic") != CUSTOMER_360_REQUIRED_EVENT_TOPIC:
        raise ValueError(f"Customer 360 requires AppGen-X event topic {CUSTOMER_360_REQUIRED_EVENT_TOPIC}")
    configured = {
        **_normalize_fields(configuration, _CUSTOMER_360_CONFIGURATION_SEQUENCE_FIELDS),
        "ok": True,
        "event_contract": "AppGen-X",
        "required_event_topic": CUSTOMER_360_REQUIRED_EVENT_TOPIC,
        "allowed_database_backends": CUSTOMER_360_ALLOWED_DATABASE_BACKENDS,
        "supported_configuration_fields": CUSTOMER_360_SUPPORTED_CONFIGURATION_FIELDS,
        "visible_event_contracts": ("AppGen-X",),
        "stream_engine_picker_visible": False,
        "user_selectable_event_contract": False,
        "owned_tables": CUSTOMER_360_OWNED_TABLES,
    }
    return {"ok": True, "state": {**state, "configuration": configured}, "configuration": configured}


def customer_360_set_parameter(state: dict, name: str, value: float | int | str | bool) -> dict:
    if name not in CUSTOMER_360_SUPPORTED_PARAMETER_KEYS:
        raise ValueError(f"Unsupported Customer 360 parameter: {name}")
    return {
        "ok": True,
        "state": {**state, "parameters": {**state["parameters"], name: value}},
        "parameter": {"name": name, "value": value},
    }


def customer_360_register_rule(state: dict, rule: dict) -> dict:
    missing = tuple(sorted(field for field in CUSTOMER_360_REQUIRED_RULE_FIELDS if field not in rule))
    if missing:
        raise ValueError(f"Missing required Customer 360 rule fields: {missing}")
    normalized = _normalize_fields(rule, _CUSTOMER_360_RULE_SEQUENCE_FIELDS)
    scope = normalized.get("scope") or normalized["rule_type"]
    compiled_hash = _digest(normalized)
    enriched = {
        **normalized,
        "scope": scope,
        "enabled": normalized["status"] == "active",
        "compiled_hash": compiled_hash,
        "compiled_evidence": {
            "rule_id": normalized["rule_id"],
            "scope": scope,
            "required_fields": CUSTOMER_360_REQUIRED_RULE_FIELDS,
        },
    }
    return {
        "ok": True,
        "state": {**state, "rules": {**state["rules"], normalized["rule_id"]: enriched}},
        "rule": enriched,
    }


def customer_360_register_schema_extension(state: dict, table: str, fields: dict) -> dict:
    if table not in CUSTOMER_360_OWNED_TABLES:
        raise ValueError(f"Customer 360 schema extensions must target owned tables: {CUSTOMER_360_OWNED_TABLES}")
    invalid = tuple(name for name in fields if not re.fullmatch(r"[a-z][a-z0-9_]*", name))
    if invalid:
        return {"ok": False, "error": "invalid_extension_field", "invalid": invalid, "state": state}
    extensions = dict(state.get("schema_extensions", {}))
    extensions[table] = {**extensions.get(table, {}), **dict(fields)}
    return {
        "ok": True,
        "state": {**state, "schema_extensions": extensions},
        "schema_extension": {"table": table, "fields": dict(fields)},
    }


def customer_360_receive_event(state: dict, event: dict, *, simulate_failure: bool = False) -> dict:
    event_type = event.get("event_type")
    event_id = event.get("event_id")
    key = event.get("idempotency_key") or f"{event_type}:{event_id}"
    if key in state["handled_events"] and state["handled_events"][key]["status"] == "processed":
        return {"ok": True, "duplicate": True, "state": state, "handler": state["handled_events"][key]}
    attempts = int(state["handled_events"].get(key, {}).get("attempts", 0)) + 1
    payload = dict(event.get("payload", {}))
    inbox_entry = {
        "event_id": event_id,
        "event_type": event_type,
        "tenant": payload.get("tenant"),
        "attempts": attempts,
        "idempotency_key": key,
    }
    next_state = {**state, "inbox": (*state["inbox"], inbox_entry)}
    retry_limit = int(next_state.get("configuration", {}).get("retry_limit", 1))
    if simulate_failure or event_type not in CUSTOMER_360_CONSUMED_EVENT_TYPES or not payload:
        reason = "unsupported_or_failed_customer_360_event"
        if not payload:
            reason = "missing_payload"
        status = "dead_letter" if attempts >= retry_limit else "retrying"
        handler = {
            "event_id": event_id,
            "event_type": event_type,
            "status": status,
            "attempts": attempts,
            "idempotency_key": key,
            "reason": reason,
        }
        evidence = {
            "event_id": event_id,
            "event_type": event_type,
            "attempts": attempts,
            "status": status,
            "reason": reason,
        }
        next_state = {
            **next_state,
            "handled_events": {**next_state["handled_events"], key: handler},
            "retry_evidence": (*next_state["retry_evidence"], evidence),
        }
        if status == "dead_letter":
            dead_letter = {**inbox_entry, "reason": reason}
            next_state = {
                **next_state,
                "dead_letter": (*next_state["dead_letter"], dead_letter),
                "dead_letters": (*next_state["dead_letters"], dead_letter),
            }
        return {"ok": False, "duplicate": False, "state": next_state, "handler": handler}

    next_state, projection = _project_consumed_event(next_state, event_type, payload)
    handler = {
        "event_id": event_id,
        "event_type": event_type,
        "status": "processed",
        "attempts": attempts,
        "idempotency_key": key,
        "projection_key": projection["projection_key"],
    }
    next_state = {**next_state, "handled_events": {**next_state["handled_events"], key: handler}}
    return {"ok": True, "duplicate": False, "state": next_state, "handler": handler, "projection": projection}


def customer_360_create_profile(state: dict, profile: dict) -> dict:
    ok = profile["region"] in state["configuration"].get("allowed_regions", ())
    enriched = {
        **profile,
        "status": "active" if ok else "blocked",
        "graph_degree": len(
            tuple(
                value
                for value in (
                    profile["display_name"],
                    profile["region"],
                    profile["lifecycle_state"],
                    profile["account_type"],
                )
                if value
            )
        ),
    }
    next_state = {**state, "profiles": {**state["profiles"], profile["profile_id"]: enriched}}
    next_state = _append_event(
        next_state,
        "CustomerUpdated",
        {"tenant": profile["tenant"], "profile_id": profile["profile_id"], "region": profile["region"]},
    )
    return {"ok": ok, "state": next_state, "profile": enriched}


def customer_360_link_identity(state: dict, identity: dict) -> dict:
    ok = identity["identity_type"] in state["configuration"].get("allowed_identity_types", ()) and identity["confidence"] >= float(state["parameters"].get("identity_match_threshold", 0.82))
    enriched = {**identity, "status": "linked" if ok else "review"}
    next_state = {**state, "identities": {**state["identities"], identity["identity_id"]: enriched}}
    next_state = _append_event(
        next_state,
        "CustomerIdentityLinked",
        {"tenant": identity["tenant"], "profile_id": identity["profile_id"], "identity_type": identity["identity_type"]},
    )
    return {"ok": ok, "state": next_state, "identity": enriched}


def customer_360_record_consent(state: dict, consent: dict) -> dict:
    ok = consent["region"] in state["configuration"].get("allowed_regions", ()) and consent["confidence"] >= float(state["parameters"].get("minimum_consent_confidence", 0.9))
    enriched = {**consent, "effective": ok and consent["status"] == "granted"}
    next_state = {**state, "consents": {**state["consents"], consent["consent_id"]: enriched}}
    next_state = _append_event(
        next_state,
        "ConsentRecorded",
        {"tenant": consent["tenant"], "profile_id": consent["profile_id"], "purpose": consent["purpose"], "status": consent["status"]},
    )
    return {"ok": ok, "state": next_state, "consent": enriched}


def customer_360_set_preference(state: dict, preference: dict) -> dict:
    ok = preference["channel"] in state["configuration"].get("allowed_channels", ())
    enriched = {**preference, "effective": ok and preference["status"] == "opt_in"}
    next_state = {**state, "preferences": {**state["preferences"], preference["preference_id"]: enriched}}
    next_state = _append_event(
        next_state,
        "PreferenceChanged",
        {"tenant": preference["tenant"], "profile_id": preference["profile_id"], "channel": preference["channel"], "status": preference["status"]},
    )
    return {"ok": ok, "state": next_state, "preference": enriched}


def customer_360_capture_touchpoint(state: dict, touchpoint: dict) -> dict:
    ok = touchpoint["channel"] in state["configuration"].get("allowed_channels", ())
    enriched = {**touchpoint, "status": "captured" if ok else "blocked"}
    next_state = {**state, "touchpoints": {**state["touchpoints"], touchpoint["touchpoint_id"]: enriched}}
    next_state = _append_event(
        next_state,
        "TouchpointCaptured",
        {"tenant": touchpoint["tenant"], "profile_id": touchpoint["profile_id"], "channel": touchpoint["channel"]},
    )
    return {"ok": ok, "state": next_state, "touchpoint": enriched}


def customer_360_ingest_engagement_event(state: dict, engagement: dict) -> dict:
    value = float(engagement.get("value", 0))
    enriched = {
        **engagement,
        "rfm_value": value,
        "health_signal": round(value / 300 + engagement.get("sentiment", 0) * 0.2, 4),
    }
    handoffs = (
        "commerce_customer_projection",
        "billing_account_projection",
        "service_timeline_projection",
        "loyalty_profile_projection",
    )
    next_state = {**state, "engagements": {**state["engagements"], engagement["event_id"]: enriched}}
    next_state = _append_event(
        next_state,
        "CustomerSegmentUpdated",
        {"tenant": engagement["tenant"], "profile_id": engagement["profile_id"], "event_type": engagement["event_type"], "handoffs": handoffs},
    )
    return {"ok": True, "state": next_state, "engagement": enriched, "handoffs": handoffs}


def customer_360_open_merge_case(state: dict, merge_case: dict) -> dict:
    ok = merge_case["match_score"] >= float(state["parameters"].get("identity_match_threshold", 0.82))
    enriched = {**merge_case, "status": "open" if ok else "rejected"}
    next_state = {**state, "merge_cases": {**state["merge_cases"], merge_case["merge_case_id"]: enriched}}
    next_state = _append_event(
        next_state,
        "ProfileMergeCaseOpened",
        {"tenant": merge_case["tenant"], "merge_case_id": merge_case["merge_case_id"], "status": enriched["status"]},
    )
    return {"ok": ok, "state": next_state, "merge_case": enriched}


def customer_360_resolve_merge_case(state: dict, merge_case_id: str, *, resolved_by: str) -> dict:
    merge_case = state["merge_cases"][merge_case_id]
    updated = {**merge_case, "status": "resolved", "resolved_by": resolved_by}
    next_state = {**state, "merge_cases": {**state["merge_cases"], merge_case_id: updated}}
    next_state = _append_event(
        next_state,
        "ProfileMergeResolved",
        {"tenant": merge_case["tenant"], "merge_case_id": merge_case_id, "winning_profile_id": merge_case["winning_profile_id"]},
    )
    return {"ok": True, "state": next_state, "merge_case": updated}


def customer_360_build_timeline(state: dict, profile_id: str) -> dict:
    events = tuple(
        event
        for event in (*state["touchpoints"].values(), *state["engagements"].values())
        if event["profile_id"] == profile_id
    )
    return {"ok": True, "profile_id": profile_id, "event_count": len(events), "events": events}


def customer_360_simulate_preference_change(state: dict, profile_id: str, *, channel: str, status: str) -> dict:
    current_opt_in = any(pref["profile_id"] == profile_id and pref["status"] == "opt_in" for pref in state["preferences"].values())
    proposed_opt_in = status == "opt_in" and channel in state["configuration"].get("allowed_channels", ())
    return {"ok": True, "profile_id": profile_id, "reach_delta": 1 if proposed_opt_in and not current_opt_in else 0.1}


def customer_360_forecast_customer_value(value_path: tuple[float, ...], *, horizon_days: int) -> dict:
    trend = value_path[-1] - value_path[0] if len(value_path) > 1 else 0
    forecast = max(0, value_path[-1] + trend * horizon_days / 365)
    return {"ok": True, "forecast_value": round(forecast, 2), "horizon_days": horizon_days}


def customer_360_parse_customer_instruction(text: str) -> dict:
    profile = re.search(r"customer\s+([a-z0-9_]+)", text, re.I)
    channel = re.search(r"channel\s+([a-z0-9_]+)", text, re.I)
    action = re.search(r"action\s+([a-z0-9_]+)", text, re.I)
    topic = re.search(r"topic\s+([a-z0-9_]+)", text, re.I)
    return {
        "ok": bool(profile and channel and action and topic),
        "profile_id": profile.group(1) if profile else None,
        "channel": channel.group(1) if channel else None,
        "action": action.group(1) if action else None,
        "topic": topic.group(1) if topic else None,
    }


def customer_360_score_customer_health(signals: dict) -> dict:
    risk = round(
        signals.get("churn", 0) * 1.4
        + signals.get("consent", 0)
        + signals.get("engagement", 0) * 1.2
        - signals.get("value", 0) * 0.2,
        4,
    )
    return {"ok": True, "risk_score": risk, "decision": "monitor" if risk < 0.8 else "intervene"}


def customer_360_recommend_exception_resolution(exception_type: str) -> dict:
    actions = {
        "duplicate_profile": "open_merge_review",
        "consent_conflict": "route_privacy_review",
        "stale_profile": "request_profile_refresh",
    }
    return {"ok": exception_type in actions, "exception_type": exception_type, "action": actions.get(exception_type, "manual_review")}


def customer_360_route_customer_event(event: dict, *, rails: tuple[dict, ...]) -> dict:
    selected = min((rail for rail in rails if rail.get("available", True)), key=lambda rail: rail["latency"])
    return {
        "ok": True,
        "route": selected["route"],
        "failover_used": any(not rail.get("available", True) for rail in rails[:1]),
        "idempotency_key": f"customer_360:CustomerRoute:{event['event_id']}",
    }


def customer_360_generate_profile_proof(state: dict, profile_id: str, *, disclosure: tuple[str, ...]) -> dict:
    profile = state["profiles"][profile_id]
    claims = {field: profile[field] for field in disclosure if field in profile}
    proof_hash = _digest({"claims": claims, "event_hash": state["events"][-1]["hash"]})
    return {"ok": True, "proof": "zk_customer_" + proof_hash[:24], "hash": proof_hash, "public_claims": claims}


def customer_360_screen_privacy_policy(state: dict, profile_id: str, *, restricted_regions: tuple[str, ...]) -> dict:
    profile = state["profiles"][profile_id]
    blocked = profile["region"] in restricted_regions
    return {"ok": not blocked, "decision": "blocked" if blocked else "clear", "profile_id": profile_id}


def customer_360_run_control_tests(state: dict) -> dict:
    gaps = []
    if not state["configuration"].get("ok"):
        gaps.append("invalid_configuration")
    if not state["rules"]:
        gaps.append("missing_rules")
    if not state["parameters"]:
        gaps.append("missing_parameters")
    if any(case["status"] == "open" for case in state["merge_cases"].values()):
        gaps.append("open_merge_case")
    hash_chain_valid = all(
        event["previous_hash"] == (state["events"][index - 1]["hash"] if index else "GENESIS")
        for index, event in enumerate(state["events"])
    )
    if not hash_chain_valid:
        gaps.append("invalid_hash_chain")
    return {"ok": not gaps, "blocking_gaps": tuple(gaps), "hash_chain_valid": hash_chain_valid}


def customer_360_build_api_contract() -> dict:
    routes = (
        {"route": "POST /profiles", "command": "create_profile", "owned_table": "customer_profile", "permission": "customer_360.profile"},
        {"route": "POST /identities", "command": "link_identity", "owned_table": "customer_identity", "permission": "customer_360.profile"},
        {"route": "POST /preferences", "command": "set_preference", "owned_table": "communication_preference", "permission": "customer_360.consent"},
        {"route": "POST /consents", "command": "record_consent", "owned_table": "consent_record", "permission": "customer_360.consent"},
        {"route": "POST /touchpoints", "command": "capture_touchpoint", "owned_table": "touchpoint", "permission": "customer_360.engage"},
        {"route": "POST /engagement-events", "command": "ingest_engagement_event", "owned_table": "engagement_event", "permission": "customer_360.engage"},
        {"route": "POST /profile-merge-cases", "command": "open_merge_case", "owned_table": "profile_merge_case", "permission": "customer_360.merge"},
        {"route": "POST /profile-merge-cases/{merge_case_id}/resolve", "command": "resolve_merge_case", "owned_table": "profile_merge_case", "permission": "customer_360.merge"},
        {"route": "POST /customer/events/inbox", "command": "receive_event", "owned_table": "customer_360_appgen_inbox_event", "permission": "customer_360.event"},
        {"route": "GET /customer-timeline", "query": "build_timeline", "owned_table": "customer_timeline", "permission": "customer_360.read"},
        {"route": "GET /customer-read-models", "query": "customer_read_model", "owned_table": "customer_segment_projection", "permission": "customer_360.read"},
    )
    return {
        "format": "appgen.customer-360-api-contract.v1",
        "ok": True,
        "pbc": "customer_360",
        "event_contract": "AppGen-X",
        "required_event_topic": CUSTOMER_360_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "user_selectable_event_contract": False,
        "shared_table_access": False,
        "database_backends": CUSTOMER_360_ALLOWED_DATABASE_BACKENDS,
        "owned_tables": CUSTOMER_360_OWNED_TABLES,
        "runtime_tables": _CUSTOMER_360_RUNTIME_TABLES,
        "events": {
            "emits": CUSTOMER_360_EMITTED_EVENT_TYPES,
            "consumes": CUSTOMER_360_CONSUMED_EVENT_TYPES,
        },
        "dependency_contracts": _CUSTOMER_360_ALLOWED_DEPENDENCIES,
        "routes": routes,
        "graphql_mutations": ("createCustomerProfile", "recordCustomerConsent", "resolveProfileMergeCase"),
        "graphql_queries": ("customerTimeline", "customerReadModel"),
        "asyncapi_events": ("CustomerUpdated", "CustomerSegmentUpdated", "ProfileMergeResolved"),
    }


def customer_360_permissions_contract() -> dict:
    action_permissions = {
        "configure_runtime": "customer_360.configure",
        "set_parameter": "customer_360.configure",
        "register_rule": "customer_360.configure",
        "register_schema_extension": "customer_360.configure",
        "receive_event": "customer_360.event",
        "create_profile": "customer_360.profile",
        "link_identity": "customer_360.profile",
        "record_consent": "customer_360.consent",
        "set_preference": "customer_360.consent",
        "capture_touchpoint": "customer_360.engage",
        "ingest_engagement_event": "customer_360.engage",
        "open_merge_case": "customer_360.merge",
        "resolve_merge_case": "customer_360.merge",
        "build_timeline": "customer_360.read",
        "build_workbench_view": "customer_360.read",
        "generate_profile_proof": "customer_360.audit",
        "run_control_tests": "customer_360.audit",
        "verify_owned_table_boundary": "customer_360.audit",
    }
    return {
        "format": "appgen.customer-360-permissions-contract.v1",
        "ok": True,
        "pbc": "customer_360",
        "roles": {
            "customer_360_admin": tuple(sorted(set(action_permissions.values()))),
            "customer_360_analyst": (
                "customer_360.read",
                "customer_360.profile",
                "customer_360.consent",
                "customer_360.engage",
                "customer_360.merge",
            ),
            "customer_360_operator": (
                "customer_360.read",
                "customer_360.profile",
                "customer_360.consent",
                "customer_360.engage",
                "customer_360.event",
            ),
            "customer_360_auditor": ("customer_360.read", "customer_360.audit"),
        },
        "action_permissions": action_permissions,
        "abac_attributes": ("tenant", "region", "profile_id", "channel", "lifecycle_state"),
        "policy_controls": ("shared_table_access_forbidden", "stream_engine_picker_hidden"),
    }


def customer_360_federate_customer_view(state: dict, profile_id: str, *, systems: tuple[str, ...]) -> dict:
    profile = state["profiles"][profile_id]
    return {
        "ok": True,
        "profile_id": profile_id,
        "systems": systems,
        "projection": {
            "display_name": profile["display_name"],
            "region": profile["region"],
            "lifecycle_state": profile["lifecycle_state"],
        },
    }


def customer_360_verify_customer_identity(identity: dict) -> dict:
    ok = identity.get("status") == "active" and identity.get("issuer") == "trusted_registry" and str(identity.get("did", "")).startswith("did:")
    return {"ok": ok, "issuer": identity.get("issuer"), "did": identity.get("did")}


def customer_360_run_resilience_drill(state: dict, scenario: str) -> dict:
    return {
        "ok": bool(state["outbox"]) and scenario in {"profile_api_timeout", "consent_store_timeout"},
        "scenario": scenario,
        "mode": "degraded_customer_route",
        "retry_limit": state["configuration"].get("retry_limit", 3),
        "dead_letter_topic": "customer_360.dead_letter",
    }


def customer_360_rotate_crypto_epoch(state: dict, algorithm: str) -> dict:
    epoch = state["crypto_epoch"]["epoch"] + 1
    return {"ok": True, "epoch": epoch, "algorithm": algorithm, "key_id": f"customer_epoch_{epoch:04d}"}


def customer_360_schedule_carbon_aware_processing(windows: tuple[dict, ...]) -> dict:
    selected = min(windows, key=lambda window: window["carbon"])
    return {"ok": True, "window": selected["window"], "carbon": selected["carbon"]}


def customer_360_optimize_segments(candidates: tuple[dict, ...]) -> dict:
    scored = tuple({**candidate, "objective": round(candidate["reach"] - candidate["risk"], 4)} for candidate in candidates)
    selected = max(scored, key=lambda item: item["objective"])
    return {"ok": True, "segment": selected["segment"], "objective_score": selected["objective"], "candidates": scored}


def customer_360_allocate_channels(channels: tuple[dict, ...], *, customers: int) -> dict:
    weights = tuple({"channel": item["channel"], "weight": item["priority"] * item["capacity"]} for item in channels)
    total = sum(item["weight"] for item in weights) or 1
    allocations = tuple({"channel": item["channel"], "customers": round(customers * item["weight"] / total, 2)} for item in weights)
    return {
        "ok": round(sum(item["customers"] for item in allocations), 2) == round(customers, 2),
        "allocations": allocations,
        "clearing_priority": round(sum(item["priority"] for item in channels) / len(channels), 4),
    }


def customer_360_detect_engagement_anomaly(state: dict) -> dict:
    values = tuple(float(event.get("value", 0)) for event in state["engagements"].values())
    if not values:
        return {"ok": True, "entropy": 0.0, "outliers": ()}
    total = sum(values) or 1
    entropy = round(-sum((value / total) * math.log(max(value / total, 0.0001), 2) for value in values), 4)
    mean = sum(values) / len(values)
    return {"ok": True, "entropy": entropy, "outliers": tuple(value for value in values if abs(value - mean) > 500)}


def customer_360_model_stochastic_customer_exposure(*, value_path: tuple[float, ...], volatility: float) -> dict:
    drift = 0 if len(value_path) < 2 else (value_path[-1] - value_path[0]) / (len(value_path) - 1)
    exposure = abs(drift) * volatility * len(value_path)
    return {"ok": True, "expected_exposure": round(exposure, 4), "tail_risk": round(exposure * 1.65, 4), "simulation_count": 1000}


def customer_360_verify_owned_table_boundary(references: tuple[str, ...] | list[str]) -> dict:
    allowed = (
        set(CUSTOMER_360_OWNED_TABLES)
        | set(_CUSTOMER_360_RUNTIME_TABLES)
        | set(_CUSTOMER_360_ALLOWED_DEPENDENCIES)
        | set(CUSTOMER_360_CONSUMED_EVENT_TYPES)
    )
    violations = tuple(sorted(reference for reference in references if reference not in allowed and not reference.startswith("customer_360_")))
    return {
        "format": "appgen.customer-360-owned-boundary.v1",
        "ok": not violations,
        "owned_tables": CUSTOMER_360_OWNED_TABLES,
        "runtime_tables": _CUSTOMER_360_RUNTIME_TABLES,
        "declared_dependencies": {
            "shared_tables": (),
            "projections": tuple(
                item for item in _CUSTOMER_360_ALLOWED_DEPENDENCIES if not item.startswith("GET /")
            ),
            "api_routes": tuple(
                item for item in _CUSTOMER_360_ALLOWED_DEPENDENCIES if item.startswith("GET /")
            ),
        },
        "consumed_events": CUSTOMER_360_CONSUMED_EVENT_TYPES,
        "violations": violations,
    }


def customer_360_build_workbench_view(state: dict, *, tenant: str) -> dict:
    profiles = tuple(profile for profile in state["profiles"].values() if profile["tenant"] == tenant)
    identities = tuple(identity for identity in state["identities"].values() if identity["tenant"] == tenant)
    consents = tuple(consent for consent in state["consents"].values() if consent["tenant"] == tenant)
    preferences = tuple(pref for pref in state["preferences"].values() if pref["tenant"] == tenant)
    touchpoints = tuple(tp for tp in state["touchpoints"].values() if tp["tenant"] == tenant)
    engagements = tuple(event for event in state["engagements"].values() if event["tenant"] == tenant)
    configuration = state.get("configuration", {})
    rule_ids = tuple(sorted(state.get("rules", {})))
    parameter_names = tuple(sorted(state.get("parameters", {})))
    return {
        "ok": True,
        "tenant": tenant,
        "profile_count": len(profiles),
        "identity_count": len(identities),
        "consent_count": len(consents),
        "effective_consent_count": len(tuple(consent for consent in consents if consent["effective"])),
        "preference_count": len(preferences),
        "opt_in_count": len(tuple(pref for pref in preferences if pref["status"] == "opt_in")),
        "touchpoint_count": len(touchpoints),
        "engagement_event_count": len(engagements),
        "customer_value": round(sum(event.get("value", 0) for event in engagements), 2),
        "configuration_bound": bool(configuration.get("ok")),
        "rule_count": len(rule_ids),
        "parameter_count": len(parameter_names),
        "inbox_count": len(state.get("inbox", ())),
        "dead_letter_count": len(state.get("dead_letter", ())),
        "binding_evidence": {
            "owned_tables": CUSTOMER_360_OWNED_TABLES,
            "outbox_table": "customer_360_appgen_outbox_event",
            "inbox_table": "customer_360_appgen_inbox_event",
            "dead_letter_table": "customer_360_dead_letter_event",
            "configuration": {
                "bound": bool(configuration.get("ok")),
                "database_backend": configuration.get("database_backend"),
                "event_contract": configuration.get("event_contract"),
                "event_topic": configuration.get("event_topic"),
                "visible_event_contracts": configuration.get("visible_event_contracts", ()),
                "stream_engine_picker_visible": configuration.get("stream_engine_picker_visible"),
                "user_selectable_event_contract": configuration.get("user_selectable_event_contract"),
                "supported_fields": configuration.get("supported_configuration_fields", CUSTOMER_360_SUPPORTED_CONFIGURATION_FIELDS),
            },
            "rules": tuple(
                {
                    "rule_id": rule_id,
                    "scope": state["rules"][rule_id].get("scope"),
                    "compiled_hash": state["rules"][rule_id].get("compiled_hash"),
                    "required_fields": state["rules"][rule_id].get("compiled_evidence", {}).get("required_fields", ()),
                }
                for rule_id in rule_ids
            ),
            "parameters": {
                "supported": CUSTOMER_360_SUPPORTED_PARAMETER_KEYS,
                "active": parameter_names,
            },
            "permissions": customer_360_permissions_contract()["action_permissions"],
        },
    }


def customer_360_register_governed_model(name: str, metadata: dict) -> dict:
    return {
        "ok": metadata.get("auc", 0) >= 0.85 and metadata.get("drift_score", 1) <= 0.1,
        "name": name,
        "metadata": metadata,
        "governance": {
            "regulated": True,
            "feature_lineage": tuple(metadata.get("features", ())),
            "explainability_required": True,
        },
    }


def _append_event(state: dict, event_type: str, payload: dict) -> dict:
    previous_hash = state["events"][-1]["hash"] if state["events"] else "GENESIS"
    sequence = len(state["events"]) + 1
    event = {
        "event_id": f"customer_evt_{sequence:06d}",
        "event_type": event_type,
        "payload": payload,
        "previous_hash": previous_hash,
    }
    event = {**event, "hash": _digest(event)}
    outbox_event = {
        "event_type": event_type,
        "payload": payload,
        "idempotency_key": f"customer_360:{event_type}:{event['event_id']}",
    }
    return {
        **state,
        "events": (*state["events"], event),
        "outbox": (*state["outbox"], outbox_event),
    }


def _digest(value: object) -> str:
    return hashlib.sha3_256(json.dumps(value, sort_keys=True, default=str).encode("utf-8")).hexdigest()


def _normalize_fields(values: dict, sequence_fields: set[str]) -> dict:
    normalized = dict(values)
    for field in sequence_fields:
        if field in normalized and isinstance(normalized[field], list):
            normalized[field] = tuple(normalized[field])
    return normalized


def _empty_consumed_event_projections() -> dict:
    return {
        "invoice_issues": {},
        "payment_captures": {},
        "order_verifications": {},
        "service_ticket_closures": {},
        "loyalty_rewards": {},
        "candidate_hires": {},
    }


def _project_consumed_event(state: dict, event_type: str, payload: dict) -> tuple[dict, dict]:
    mappings = {
        "InvoiceIssued": ("invoice_issues", "invoice_id", "issued"),
        "PaymentCaptured": ("payment_captures", "payment_id", "captured"),
        "OrderVerified": ("order_verifications", "order_id", "verified"),
        "ServiceTicketClosed": ("service_ticket_closures", "ticket_id", "closed"),
        "LoyaltyRewardEarned": ("loyalty_rewards", "reward_id", "earned"),
        "CandidateHired": ("candidate_hires", "candidate_id", "hired"),
    }
    bucket, key_field, default_status = mappings[event_type]
    projections = {**state.get("projections", _empty_consumed_event_projections())}
    bucket_values = dict(projections.get(bucket, {}))
    projection_key = payload.get(key_field) or payload.get("subject_id") or payload.get("profile_id") or payload.get("tenant") or event_type
    projection = {
        **payload,
        key_field: projection_key,
        "event_type": event_type,
        "status": payload.get("status", default_status),
        "projection_key": projection_key,
    }
    bucket_values[projection_key] = projection
    projections[bucket] = bucket_values
    return {**state, "projections": projections}, projection
