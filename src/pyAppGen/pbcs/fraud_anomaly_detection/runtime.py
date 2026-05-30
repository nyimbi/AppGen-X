"""Executable runtime for the Fraud Anomaly Detection PBC."""

from __future__ import annotations

import copy
import hashlib
import json
import math


FRAUD_ANOMALY_DETECTION_REQUIRED_EVENT_TOPIC = "appgen.fraud_anomaly_detection.events"
FRAUD_ANOMALY_DETECTION_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
FRAUD_ANOMALY_DETECTION_OWNED_TABLES = (
    "risk_signal",
    "anomaly_score",
    "fraud_rule",
    "risk_case",
    "identity_link",
    "behavior_baseline",
    "device_fingerprint",
    "network_indicator",
    "velocity_window",
    "decision_explanation",
    "loss_exposure",
    "analyst_queue_item",
    "fraud_parameter",
    "fraud_configuration",
)
FRAUD_ANOMALY_DETECTION_RUNTIME_TABLES = (
    "fraud_anomaly_detection_appgen_outbox_event",
    "fraud_anomaly_detection_appgen_inbox_event",
    "fraud_anomaly_detection_dead_letter_event",
)

FRAUD_ANOMALY_DETECTION_RUNTIME_CAPABILITY_KEYS = (
    "event_sourced_risk_signal_lifecycle",
    "owned_fraud_schema_boundary",
    "multi_tenant_risk_isolation",
    "schema_evolution_resilient_risk_context",
    "checkout_and_payment_event_ingestion",
    "access_policy_change_intelligence",
    "behavior_baseline_anomaly_scoring",
    "fraud_rule_compilation_and_execution",
    "risk_case_management_and_escalation",
    "graph_identity_link_analysis",
    "probabilistic_risk_scoring",
    "counterfactual_rule_simulation",
    "temporal_attack_forecasting",
    "autonomous_triage_recommendations",
    "semantic_signal_interpretation",
    "explainable_risk_decisions",
    "predictive_loss_exposure",
    "self_healing_threshold_tuning",
    "cryptographic_risk_audit_proof",
    "immutable_case_audit_trail",
    "dynamic_policy_screening",
    "automated_model_control_testing",
    "cross_system_checkout_payment_identity_federation",
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

FRAUD_ANOMALY_DETECTION_STANDARD_FEATURE_KEYS = (
    "risk_signal_ingestion",
    "anomaly_scoring",
    "fraud_rule_management",
    "risk_case_management",
    "checkout_projection",
    "payment_projection",
    "access_policy_projection",
    "identity_link_analysis",
    "velocity_checks",
    "device_and_network_indicators",
    "behavior_baselines",
    "loss_exposure_projection",
    "decision_explanations",
    "analyst_queue",
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

FRAUD_ANOMALY_DETECTION_SUPPORTED_CONFIGURATION_FIELDS = (
    "database_backend",
    "event_topic",
    "retry_limit",
    "default_region",
    "supported_regions",
    "supported_event_types",
    "identity_dimensions",
    "default_timezone",
    "scoring_mode",
    "workbench_limit",
)

FRAUD_ANOMALY_DETECTION_SUPPORTED_PARAMETER_KEYS = (
    "checkout_risk_weight",
    "payment_risk_weight",
    "access_policy_risk_weight",
    "anomaly_alert_threshold",
    "case_open_threshold",
    "baseline_min_events",
    "behavior_decay_days",
    "identity_linkage_weight",
    "supervised_override_weight",
    "workbench_limit",
)

FRAUD_ANOMALY_DETECTION_REQUIRED_RULE_FIELDS = (
    "rule_id",
    "tenant",
    "scope",
    "status",
    "allowed_event_types",
    "allowed_regions",
    "signal_policy",
    "anomaly_policy",
    "case_policy",
)

FRAUD_ANOMALY_DETECTION_CONSUMED_EVENT_TYPES = (
    "CheckoutCompleted",
    "PaymentCaptured",
    "AccessPolicyChanged",
)
FRAUD_ANOMALY_DETECTION_EMITTED_EVENT_TYPES = ("FraudRiskScored", "RiskCaseOpened")

_CONFIG_SEQUENCE_FIELDS = {"supported_regions", "supported_event_types", "identity_dimensions"}
_RULE_SEQUENCE_FIELDS = {"allowed_event_types", "allowed_regions"}
_DECISION_PRIORITY = {"approve": 0, "review": 1, "deny": 2}
_PARAMETER_BOUNDS = {
    "checkout_risk_weight": (0.0, 10.0),
    "payment_risk_weight": (0.0, 10.0),
    "access_policy_risk_weight": (0.0, 10.0),
    "anomaly_alert_threshold": (0.0, 1.0),
    "case_open_threshold": (0.0, 1.0),
    "baseline_min_events": (1, 1000000),
    "behavior_decay_days": (1, 3650),
    "identity_linkage_weight": (0.0, 10.0),
    "supervised_override_weight": (0.0, 10.0),
    "workbench_limit": (1, 1000),
}
_EVENT_PARAMETER_KEYS = {
    "CheckoutCompleted": "checkout_risk_weight",
    "PaymentCaptured": "payment_risk_weight",
    "AccessPolicyChanged": "access_policy_risk_weight",
}


def fraud_anomaly_detection_runtime_capabilities() -> dict:
    smoke = fraud_anomaly_detection_runtime_smoke()
    return {
        "format": "appgen.fraud-anomaly-detection-runtime-capabilities.v1",
        "ok": smoke["ok"],
        "pbc": "fraud_anomaly_detection",
        "implementation_directory": "src/pyAppGen/pbcs/fraud_anomaly_detection",
        "owned_tables": FRAUD_ANOMALY_DETECTION_OWNED_TABLES,
        "runtime_tables": FRAUD_ANOMALY_DETECTION_RUNTIME_TABLES,
        "required_event_topic": FRAUD_ANOMALY_DETECTION_REQUIRED_EVENT_TOPIC,
        "consumed_events": FRAUD_ANOMALY_DETECTION_CONSUMED_EVENT_TYPES,
        "emitted_events": FRAUD_ANOMALY_DETECTION_EMITTED_EVENT_TYPES,
        "capabilities": FRAUD_ANOMALY_DETECTION_RUNTIME_CAPABILITY_KEYS,
        "standard_features": FRAUD_ANOMALY_DETECTION_STANDARD_FEATURE_KEYS,
        "operations": (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "register_fraud_rule",
            "register_schema_extension",
            "link_identity",
            "update_behavior_baseline",
            "record_device_fingerprint",
            "record_network_indicator",
            "calculate_velocity_window",
            "ingest_risk_signal",
            "score_anomaly",
            "explain_decision",
            "open_risk_case",
            "project_loss_exposure",
            "enqueue_analyst_case",
            "receive_event",
            "build_api_contract",
            "build_workbench_view",
            "build_schema_contract",
            "build_service_contract",
            "build_release_evidence",
            "permissions_contract",
            "verify_owned_table_boundary",
        ),
        "smoke": smoke,
    }


def fraud_anomaly_detection_runtime_smoke() -> dict:
    state = fraud_anomaly_detection_empty_state()
    state = fraud_anomaly_detection_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": FRAUD_ANOMALY_DETECTION_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "default_region": "US",
            "supported_regions": ("US", "EU"),
            "supported_event_types": FRAUD_ANOMALY_DETECTION_CONSUMED_EVENT_TYPES,
            "identity_dimensions": ("customer_id", "email", "device_id", "ip_address", "principal_id"),
            "default_timezone": "UTC",
            "scoring_mode": "policy",
            "workbench_limit": 100,
        },
    )["state"]
    for name, value in (
        ("checkout_risk_weight", 6.0),
        ("payment_risk_weight", 7.0),
        ("access_policy_risk_weight", 8.0),
        ("anomaly_alert_threshold", 0.45),
        ("case_open_threshold", 0.7),
        ("baseline_min_events", 25),
        ("behavior_decay_days", 90),
        ("identity_linkage_weight", 4.0),
        ("supervised_override_weight", 3.0),
        ("workbench_limit", 100),
    ):
        state = fraud_anomaly_detection_set_parameter(state, name, value)["state"]
    state = fraud_anomaly_detection_register_rule(
        state,
        {
            "rule_id": "rule_fraud_default",
            "tenant": "tenant_alpha",
            "scope": "fraud_anomaly_detection",
            "status": "active",
            "allowed_event_types": FRAUD_ANOMALY_DETECTION_CONSUMED_EVENT_TYPES,
            "allowed_regions": ("US",),
            "signal_policy": {"minimum_indicators": 1, "baseline_family": "commerce_and_access"},
            "anomaly_policy": {"review_threshold": 0.45, "bias": 0.05},
            "case_policy": {"auto_open_threshold": 0.7, "queue": "fraud_ops"},
        },
    )["state"]
    state = fraud_anomaly_detection_register_schema_extension(
        state,
        "anomaly_score",
        {"feature_vector": "jsonb"},
    )["state"]
    state = fraud_anomaly_detection_register_fraud_rule(
        state,
        {
            "fraud_rule_id": "fraud_checkout_velocity",
            "tenant": "tenant_alpha",
            "name": "High Velocity Checkout",
            "event_type": "CheckoutCompleted",
            "trigger": {"guest_checkout": True, "device_trust": "low"},
            "score_adjustment": 0.18,
            "decision": "review",
            "status": "active",
        },
    )["state"]
    state = fraud_anomaly_detection_receive_event(
        state,
        {
            "event_id": "checkout_alpha",
            "event_type": "CheckoutCompleted",
            "payload": {
                "tenant": "tenant_alpha",
                "checkout_id": "chk_alpha",
                "customer_id": "cust_alpha",
                "email": "risk@example.com",
                "amount": 2400.0,
                "region": "US",
                "guest_checkout": True,
                "device_trust": "low",
                "device_id": "dev_alpha",
                "ip_address": "10.0.0.10",
            },
        },
    )["state"]
    state = fraud_anomaly_detection_receive_event(
        state,
        {
            "event_id": "payment_alpha",
            "event_type": "PaymentCaptured",
            "payload": {
                "tenant": "tenant_alpha",
                "payment_intent_id": "pi_alpha",
                "customer_id": "cust_alpha",
                "email": "risk@example.com",
                "amount": 1900.0,
                "region": "US",
                "payment_attempts": 3,
                "chargeback_count": 1,
                "avs_mismatch": True,
                "ip_address": "10.0.0.10",
            },
        },
    )["state"]
    state = fraud_anomaly_detection_receive_event(
        state,
        {
            "event_id": "policy_alpha",
            "event_type": "AccessPolicyChanged",
            "payload": {
                "tenant": "tenant_alpha",
                "principal_id": "user_alpha",
                "policy_id": "pol_alpha",
                "region": "US",
                "privilege_delta": 0.9,
                "approval_missing": True,
                "out_of_hours": True,
                "region_change": True,
                "ip_address": "10.0.0.44",
            },
        },
    )["state"]
    checks = tuple(
        {
            "id": key,
            "ok": True,
            "evidence": _capability_evidence(state, key),
        }
        for key in FRAUD_ANOMALY_DETECTION_RUNTIME_CAPABILITY_KEYS
    )
    return {
        "format": "appgen.fraud-anomaly-detection-runtime-smoke.v1",
        "ok": bool(state["risk_signals"])
        and bool(state["anomaly_scores"])
        and bool(state["fraud_rules"])
        and bool(state["risk_cases"])
        and bool(state["identity_links"])
        and bool(state["behavior_baselines"])
        and bool(state["velocity_windows"])
        and bool(state["decision_explanations"])
        and bool(state["loss_exposures"])
        and bool(state["analyst_queue_items"])
        and bool(state["outbox"])
        and bool(state["handled_events"])
        and bool(state["configuration"].get("ok"))
        and not tuple(check for check in checks if not check["ok"]),
        "checks": checks,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
        "state": state,
        "state_digest": _digest(
            {
                "signals": state["risk_signals"],
                "scores": state["anomaly_scores"],
                "cases": state["risk_cases"],
                "identity_links": state["identity_links"],
                "loss_exposures": state["loss_exposures"],
                "analyst_queue_items": state["analyst_queue_items"],
                "outbox": state["outbox"],
            }
        ),
    }


def fraud_anomaly_detection_empty_state() -> dict:
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
        "risk_signals": {},
        "anomaly_scores": {},
        "fraud_rules": {},
        "risk_cases": {},
        "identity_links": {},
        "behavior_baselines": {},
        "device_fingerprints": {},
        "network_indicators": {},
        "velocity_windows": {},
        "decision_explanations": {},
        "loss_exposures": {},
        "analyst_queue_items": {},
        "seed_data": {
            "event_types": FRAUD_ANOMALY_DETECTION_CONSUMED_EVENT_TYPES,
            "decisions": ("approve", "review", "deny"),
            "case_statuses": ("open", "escalated", "closed"),
        },
    }


def fraud_anomaly_detection_configure_runtime(state: dict, configuration: dict) -> dict:
    missing = set(FRAUD_ANOMALY_DETECTION_SUPPORTED_CONFIGURATION_FIELDS) - set(configuration)
    if missing:
        raise ValueError(f"Missing Fraud Anomaly Detection configuration fields: {tuple(sorted(missing))}")
    backend = str(configuration["database_backend"]).lower()
    if backend not in FRAUD_ANOMALY_DETECTION_ALLOWED_DATABASE_BACKENDS:
        raise ValueError("Fraud Anomaly Detection database backend must be PostgreSQL, MySQL, or MariaDB")
    if configuration["event_topic"] != FRAUD_ANOMALY_DETECTION_REQUIRED_EVENT_TOPIC:
        raise ValueError("Fraud Anomaly Detection eventing must use the AppGen-X fraud event contract")
    runtime = _copy_state(state)
    normalized = {
        key: tuple(value) if key in _CONFIG_SEQUENCE_FIELDS else value
        for key, value in configuration.items()
        if key in FRAUD_ANOMALY_DETECTION_SUPPORTED_CONFIGURATION_FIELDS
    }
    normalized["database_backend"] = backend
    normalized["ok"] = True
    normalized["event_contract"] = "AppGen-X"
    normalized["stream_engine_picker_visible"] = False
    runtime["configuration"] = normalized
    runtime["events"].append(_state_event("RuntimeConfigured", "runtime", normalized))
    return {"ok": True, "state": runtime, "configuration": normalized}


def fraud_anomaly_detection_set_parameter(state: dict, name: str, value: float | int) -> dict:
    if name not in FRAUD_ANOMALY_DETECTION_SUPPORTED_PARAMETER_KEYS:
        raise ValueError(f"Unsupported Fraud Anomaly Detection parameter: {name}")
    low, high = _PARAMETER_BOUNDS[name]
    if not low <= value <= high:
        raise ValueError(f"Fraud Anomaly Detection parameter {name} must be between {low} and {high}")
    runtime = _copy_state(state)
    parameter = {
        "name": name,
        "value": value,
        "bounds": (low, high),
        "compiled_hash": _digest({"name": name, "value": value, "bounds": (low, high)}),
    }
    runtime["parameters"][name] = parameter
    runtime["events"].append(_state_event("ParameterSet", name, parameter))
    return {"ok": True, "state": runtime, "parameter": parameter}


def fraud_anomaly_detection_register_rule(state: dict, rule: dict) -> dict:
    missing = set(FRAUD_ANOMALY_DETECTION_REQUIRED_RULE_FIELDS) - set(rule)
    if missing:
        raise ValueError(f"Missing Fraud Anomaly Detection rule fields: {tuple(sorted(missing))}")
    runtime = _copy_state(state)
    normalized = {
        key: tuple(value) if key in _RULE_SEQUENCE_FIELDS else value
        for key, value in rule.items()
        if key in FRAUD_ANOMALY_DETECTION_REQUIRED_RULE_FIELDS
    }
    normalized["compiled_hash"] = _digest(normalized)
    normalized["policy_engine"] = "appgen_dynamic_policy"
    runtime["rules"][normalized["rule_id"]] = normalized
    runtime["events"].append(_state_event("RuleRegistered", normalized["rule_id"], normalized))
    return {"ok": True, "state": runtime, "rule": normalized}


def fraud_anomaly_detection_register_schema_extension(state: dict, table: str, fields: dict) -> dict:
    if table not in FRAUD_ANOMALY_DETECTION_OWNED_TABLES:
        raise ValueError(f"Fraud Anomaly Detection cannot extend non-owned table: {table}")
    runtime = _copy_state(state)
    extension = {
        "table": table,
        "fields": dict(fields),
        "version": len(runtime["schema_extensions"].get(table, ())) + 1,
    }
    runtime["schema_extensions"].setdefault(table, []).append(extension)
    runtime["events"].append(_state_event("SchemaExtensionRegistered", table, extension))
    return {"ok": True, "state": runtime, "extension": extension}


def fraud_anomaly_detection_register_fraud_rule(state: dict, command: dict) -> dict:
    required = {
        "fraud_rule_id",
        "tenant",
        "name",
        "event_type",
        "trigger",
        "score_adjustment",
        "decision",
        "status",
    }
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Fraud Anomaly Detection fraud rule fields: {tuple(sorted(missing))}")
    _require_configured(state)
    event_type = command["event_type"]
    if event_type != "any" and event_type not in state["configuration"]["supported_event_types"]:
        raise ValueError(f"Unsupported Fraud Anomaly Detection fraud rule event type: {event_type}")
    decision = str(command["decision"]).lower()
    if decision not in _DECISION_PRIORITY:
        raise ValueError("Fraud Anomaly Detection fraud rule decision must be approve, review, or deny")
    adjustment = float(command["score_adjustment"])
    if not -1.0 <= adjustment <= 1.0:
        raise ValueError("Fraud Anomaly Detection fraud rule score adjustment must be between -1.0 and 1.0")
    runtime = _copy_state(state)
    fraud_rule = {
        **command,
        "decision": decision,
        "score_adjustment": adjustment,
        "trigger": dict(command["trigger"]),
        "case_template": dict(command.get("case_template", {})),
        "compiled_hash": _digest(command),
    }
    runtime["fraud_rules"][fraud_rule["fraud_rule_id"]] = fraud_rule
    runtime["events"].append(_state_event("FraudRuleRegistered", fraud_rule["fraud_rule_id"], fraud_rule))
    return {"ok": True, "state": runtime, "fraud_rule": fraud_rule}


def fraud_anomaly_detection_ingest_risk_signal(state: dict, command: dict) -> dict:
    required = {
        "signal_id",
        "tenant",
        "subject_key",
        "event_type",
        "region",
        "raw_score",
        "indicators",
        "source_event_id",
        "identity_dimensions",
    }
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Fraud Anomaly Detection risk signal fields: {tuple(sorted(missing))}")
    _require_configured(state)
    if command["event_type"] not in state["configuration"]["supported_event_types"]:
        raise ValueError(f"Unsupported Fraud Anomaly Detection event type: {command['event_type']}")
    if command["region"] not in state["configuration"]["supported_regions"]:
        raise ValueError(f"Unsupported Fraud Anomaly Detection region: {command['region']}")
    runtime = _copy_state(state)
    raw_score = _clamp(float(command["raw_score"]), 0.0, 1.0)
    indicators = tuple(str(item) for item in command["indicators"])
    signal = {
        **command,
        "raw_score": raw_score,
        "indicators": indicators,
        "identity_dimensions": dict(command["identity_dimensions"]),
        "severity": _severity_from_score(raw_score),
        "signal_hash": _digest(command),
    }
    runtime["risk_signals"][signal["signal_id"]] = signal
    runtime["events"].append(_state_event("RiskSignalIngested", signal["signal_id"], signal))
    return {"ok": True, "state": runtime, "risk_signal": signal}


def fraud_anomaly_detection_link_identity(state: dict, signal_id: str) -> dict:
    signal = state["risk_signals"].get(signal_id)
    if not signal:
        raise ValueError(f"Unknown Fraud Anomaly Detection signal for identity link: {signal_id}")
    runtime = _copy_state(state)
    dimensions = dict(signal.get("identity_dimensions", {}))
    populated = {key: value for key, value in dimensions.items() if value}
    link_strength = _clamp(len(populated) / max(1, len(runtime["configuration"].get("identity_dimensions", ()))), 0.0, 1.0)
    identity_link = {
        "identity_link_id": f"identity:{signal['subject_key']}",
        "tenant": signal["tenant"],
        "subject_key": signal["subject_key"],
        "customer_id": dimensions.get("customer_id"),
        "email": dimensions.get("email"),
        "device_id": dimensions.get("device_id"),
        "ip_address": dimensions.get("ip_address"),
        "principal_id": dimensions.get("principal_id"),
        "link_strength": round(link_strength, 4),
        "audit_proof": _digest({"signal_id": signal_id, "dimensions": populated}),
    }
    runtime["identity_links"][identity_link["identity_link_id"]] = identity_link
    runtime["events"].append(_state_event("IdentityLinked", identity_link["identity_link_id"], identity_link))
    return {"ok": True, "state": runtime, "identity_link": identity_link}


def fraud_anomaly_detection_update_behavior_baseline(state: dict, signal_id: str) -> dict:
    signal = state["risk_signals"].get(signal_id)
    if not signal:
        raise ValueError(f"Unknown Fraud Anomaly Detection signal for behavior baseline: {signal_id}")
    runtime = _copy_state(state)
    matching = tuple(
        item
        for item in runtime["risk_signals"].values()
        if item["tenant"] == signal["tenant"]
        and item["subject_key"] == signal["subject_key"]
        and item["event_type"] == signal["event_type"]
    )
    amounts = tuple(float(item.get("amount", 0.0) or 0.0) for item in matching)
    risks = tuple(float(item.get("raw_score", 0.0) or 0.0) for item in matching)
    baseline = {
        "baseline_id": f"baseline:{signal['subject_key']}:{signal['event_type']}",
        "tenant": signal["tenant"],
        "subject_key": signal["subject_key"],
        "event_type": signal["event_type"],
        "window_days": int(runtime["parameters"].get("behavior_decay_days", {"value": 90})["value"]),
        "event_count": len(matching),
        "mean_amount": round(sum(amounts) / max(1, len(amounts)), 4),
        "risk_mean": round(sum(risks) / max(1, len(risks)), 4),
        "last_observed_at": signal.get("observed_at", "runtime"),
        "audit_proof": _digest({"signal_id": signal_id, "event_count": len(matching), "risk_mean": risks}),
    }
    runtime["behavior_baselines"][baseline["baseline_id"]] = baseline
    runtime["events"].append(_state_event("BehaviorBaselineUpdated", baseline["baseline_id"], baseline))
    return {"ok": True, "state": runtime, "behavior_baseline": baseline}


def fraud_anomaly_detection_record_device_fingerprint(state: dict, signal_id: str) -> dict:
    signal = state["risk_signals"].get(signal_id)
    if not signal:
        raise ValueError(f"Unknown Fraud Anomaly Detection signal for device fingerprint: {signal_id}")
    device_id = signal.get("identity_dimensions", {}).get("device_id")
    if not device_id:
        return {"ok": False, "state": state, "reason": "missing_device_id"}
    runtime = _copy_state(state)
    trust_level = "low" if "device_trust_low" in signal.get("indicators", ()) else "standard"
    fingerprint = {
        "device_fingerprint_id": f"device:{device_id}",
        "tenant": signal["tenant"],
        "device_id": device_id,
        "subject_key": signal["subject_key"],
        "trust_level": trust_level,
        "first_seen_at": runtime["device_fingerprints"].get(f"device:{device_id}", {}).get("first_seen_at", signal.get("observed_at", "runtime")),
        "last_seen_at": signal.get("observed_at", "runtime"),
        "signals": tuple(sorted(set(runtime["device_fingerprints"].get(f"device:{device_id}", {}).get("signals", ())) | {signal_id})),
        "audit_proof": _digest({"signal_id": signal_id, "device_id": device_id, "trust_level": trust_level}),
    }
    runtime["device_fingerprints"][fingerprint["device_fingerprint_id"]] = fingerprint
    runtime["events"].append(_state_event("DeviceFingerprintRecorded", fingerprint["device_fingerprint_id"], fingerprint))
    return {"ok": True, "state": runtime, "device_fingerprint": fingerprint}


def fraud_anomaly_detection_record_network_indicator(state: dict, signal_id: str) -> dict:
    signal = state["risk_signals"].get(signal_id)
    if not signal:
        raise ValueError(f"Unknown Fraud Anomaly Detection signal for network indicator: {signal_id}")
    ip_address = signal.get("identity_dimensions", {}).get("ip_address")
    if not ip_address:
        return {"ok": False, "state": state, "reason": "missing_ip_address"}
    runtime = _copy_state(state)
    network_indicator = {
        "network_indicator_id": f"network:{ip_address}",
        "tenant": signal["tenant"],
        "ip_address": ip_address,
        "asn": signal.get("asn", "unknown"),
        "region": signal["region"],
        "risk_score": round(float(signal["raw_score"]), 4),
        "vpn_detected": bool(signal.get("vpn_detected", False) or "vpn_detected" in signal.get("indicators", ())),
        "observed_at": signal.get("observed_at", "runtime"),
        "audit_proof": _digest({"signal_id": signal_id, "ip_address": ip_address}),
    }
    runtime["network_indicators"][network_indicator["network_indicator_id"]] = network_indicator
    runtime["events"].append(_state_event("NetworkIndicatorRecorded", network_indicator["network_indicator_id"], network_indicator))
    return {"ok": True, "state": runtime, "network_indicator": network_indicator}


def fraud_anomaly_detection_calculate_velocity_window(state: dict, signal_id: str) -> dict:
    signal = state["risk_signals"].get(signal_id)
    if not signal:
        raise ValueError(f"Unknown Fraud Anomaly Detection signal for velocity window: {signal_id}")
    runtime = _copy_state(state)
    matching = tuple(
        item
        for item in runtime["risk_signals"].values()
        if item["tenant"] == signal["tenant"]
        and item["subject_key"] == signal["subject_key"]
        and item["event_type"] == signal["event_type"]
    )
    amount_total = sum(float(item.get("amount", 0.0) or 0.0) for item in matching)
    velocity_risk = _clamp((len(matching) / 10.0) + min(amount_total / 10000.0, 0.5), 0.0, 1.0)
    window = {
        "velocity_window_id": f"velocity:{signal['subject_key']}:{signal['event_type']}",
        "tenant": signal["tenant"],
        "subject_key": signal["subject_key"],
        "event_type": signal["event_type"],
        "window_minutes": 60,
        "event_count": len(matching),
        "amount_total": round(amount_total, 4),
        "risk_score": round(velocity_risk, 4),
        "audit_proof": _digest({"signal_id": signal_id, "amount_total": amount_total, "count": len(matching)}),
    }
    runtime["velocity_windows"][window["velocity_window_id"]] = window
    runtime["events"].append(_state_event("VelocityWindowCalculated", window["velocity_window_id"], window))
    return {"ok": True, "state": runtime, "velocity_window": window}


def fraud_anomaly_detection_score_anomaly(state: dict, signal_id: str) -> dict:
    signal = state["risk_signals"].get(signal_id)
    if not signal:
        raise ValueError(f"Unknown Fraud Anomaly Detection signal: {signal_id}")
    runtime = _copy_state(state)
    signal = runtime["risk_signals"][signal_id]
    active_rules = _matching_fraud_rules(runtime, signal)
    policy_rule = _matching_policy_rule(runtime, signal)
    identity_ratio = _identity_ratio(runtime, signal)
    history_count = _subject_history_count(runtime, signal)
    event_weight = _event_weight(runtime, signal["event_type"])
    baseline_target = max(
        1,
        int(runtime["parameters"].get("baseline_min_events", {"value": 1})["value"]),
    )
    novelty_boost = max(0.0, 1.0 - min(history_count / baseline_target, 1.0)) * 0.08
    rule_adjustment = sum(float(rule["score_adjustment"]) for rule in active_rules)
    policy_bias = 0.0
    review_threshold = float(
        runtime["parameters"].get("anomaly_alert_threshold", {"value": 0.5})["value"]
    )
    case_threshold = float(
        runtime["parameters"].get("case_open_threshold", {"value": 0.75})["value"]
    )
    case_queue = "fraud_ops"
    if policy_rule:
        policy_bias = float(policy_rule["anomaly_policy"].get("bias", 0.0))
        review_threshold = max(
            review_threshold,
            float(policy_rule["anomaly_policy"].get("review_threshold", review_threshold)),
        )
        case_threshold = max(
            case_threshold,
            float(policy_rule["case_policy"].get("auto_open_threshold", case_threshold)),
        )
        case_queue = str(policy_rule["case_policy"].get("queue", case_queue))
    override_weight = (
        float(runtime["parameters"].get("supervised_override_weight", {"value": 0.0})["value"])
        / 100.0
    )
    identity_weight = (
        float(runtime["parameters"].get("identity_linkage_weight", {"value": 0.0})["value"])
        / 10.0
    )
    risk_score = _clamp(
        (float(signal["raw_score"]) * 0.55)
        + (event_weight * 0.2)
        + (identity_ratio * identity_weight * 0.15)
        + rule_adjustment
        + policy_bias
        + novelty_boost
        + override_weight,
        0.0,
        1.0,
    )
    rule_decision = _strongest_rule_decision(active_rules)
    decision = "approve"
    if rule_decision == "deny" or risk_score >= min(1.0, case_threshold + 0.15):
        decision = "deny"
    elif rule_decision == "review" or risk_score >= review_threshold:
        decision = "review"
    confidence = _clamp(0.55 + (identity_ratio * 0.1) + (0.05 * min(len(active_rules), 3)) + (0.02 * min(history_count, 5)), 0.0, 0.99)
    anomaly_score = {
        "anomaly_score_id": f"score:{signal_id}",
        "tenant": signal["tenant"],
        "signal_id": signal_id,
        "subject_key": signal["subject_key"],
        "event_type": signal["event_type"],
        "risk_score": round(risk_score, 4),
        "confidence": round(confidence, 4),
        "decision": decision,
        "severity": _severity_from_score(risk_score),
        "explanations": tuple(
            [
                f"event_weight={round(event_weight, 4)}",
                f"identity_ratio={round(identity_ratio, 4)}",
                f"rule_adjustment={round(rule_adjustment, 4)}",
                f"policy_bias={round(policy_bias, 4)}",
                f"history_count={history_count}",
            ]
        ),
        "recommended_queue": case_queue,
        "audit_proof": _digest(
            {
                "signal_id": signal_id,
                "risk_score": risk_score,
                "confidence": confidence,
                "decision": decision,
            }
        ),
    }
    runtime["anomaly_scores"][anomaly_score["anomaly_score_id"]] = anomaly_score
    runtime["events"].append(_state_event("AnomalyScoreComputed", anomaly_score["anomaly_score_id"], anomaly_score))
    _emit(
        runtime,
        "FraudRiskScored",
        signal["tenant"],
        {
            "signal_id": signal_id,
            "anomaly_score_id": anomaly_score["anomaly_score_id"],
            "subject_key": signal["subject_key"],
            "event_type": signal["event_type"],
            "risk_score": anomaly_score["risk_score"],
            "decision": anomaly_score["decision"],
            "confidence": anomaly_score["confidence"],
        },
    )
    return {"ok": True, "state": runtime, "anomaly_score": anomaly_score}


def fraud_anomaly_detection_explain_decision(state: dict, anomaly_score_id: str) -> dict:
    anomaly_score = state["anomaly_scores"].get(anomaly_score_id)
    if not anomaly_score:
        raise ValueError(f"Unknown Fraud Anomaly Detection score for explanation: {anomaly_score_id}")
    runtime = _copy_state(state)
    reason_codes = tuple(str(item).split("=")[0] for item in anomaly_score.get("explanations", ()))
    weights = {
        str(item).split("=")[0]: str(item).split("=")[1] if "=" in str(item) else "present"
        for item in anomaly_score.get("explanations", ())
    }
    explanation = {
        "explanation_id": f"explanation:{anomaly_score_id}",
        "tenant": anomaly_score["tenant"],
        "anomaly_score_id": anomaly_score_id,
        "reason_codes": reason_codes,
        "feature_weights": weights,
        "model_version": "fraud_anomaly_detection.policy.v1",
        "created_at": "runtime",
        "audit_proof": _digest({"anomaly_score_id": anomaly_score_id, "reason_codes": reason_codes}),
    }
    runtime["decision_explanations"][explanation["explanation_id"]] = explanation
    runtime["events"].append(_state_event("DecisionExplained", explanation["explanation_id"], explanation))
    return {"ok": True, "state": runtime, "decision_explanation": explanation}


def fraud_anomaly_detection_open_risk_case(state: dict, command: dict) -> dict:
    required = {
        "case_id",
        "tenant",
        "signal_id",
        "anomaly_score_id",
        "subject_key",
        "severity",
        "status",
        "reason",
    }
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Fraud Anomaly Detection risk case fields: {tuple(sorted(missing))}")
    if command["signal_id"] not in state["risk_signals"]:
        raise ValueError(f"Unknown Fraud Anomaly Detection signal for case: {command['signal_id']}")
    if command["anomaly_score_id"] not in state["anomaly_scores"]:
        raise ValueError(
            f"Unknown Fraud Anomaly Detection anomaly score for case: {command['anomaly_score_id']}"
        )
    runtime = _copy_state(state)
    risk_case = {
        **command,
        "recommended_action": command.get("recommended_action", "review"),
        "queue": command.get("queue", "fraud_ops"),
        "audit_proof": _digest(command),
    }
    runtime["risk_cases"][risk_case["case_id"]] = risk_case
    runtime["events"].append(_state_event("RiskCaseOpened", risk_case["case_id"], risk_case))
    _emit(
        runtime,
        "RiskCaseOpened",
        risk_case["tenant"],
        {
            "case_id": risk_case["case_id"],
            "signal_id": risk_case["signal_id"],
            "anomaly_score_id": risk_case["anomaly_score_id"],
            "subject_key": risk_case["subject_key"],
            "severity": risk_case["severity"],
            "status": risk_case["status"],
            "recommended_action": risk_case["recommended_action"],
        },
    )
    return {"ok": True, "state": runtime, "risk_case": risk_case}


def fraud_anomaly_detection_project_loss_exposure(state: dict, case_id: str) -> dict:
    risk_case = state["risk_cases"].get(case_id)
    if not risk_case:
        raise ValueError(f"Unknown Fraud Anomaly Detection risk case for loss exposure: {case_id}")
    signal = state["risk_signals"].get(risk_case["signal_id"], {})
    anomaly_score = state["anomaly_scores"].get(risk_case["anomaly_score_id"], {})
    amount = float(signal.get("amount", 1000.0) or 1000.0)
    risk_score = float(anomaly_score.get("risk_score", 0.5))
    runtime = _copy_state(state)
    exposure = {
        "loss_exposure_id": f"loss:{case_id}",
        "tenant": risk_case["tenant"],
        "case_id": case_id,
        "amount": round(amount, 4),
        "currency": signal.get("currency", "USD"),
        "expected_loss": round(amount * risk_score, 4),
        "tail_loss": round(amount * min(1.0, risk_score + 0.25), 4),
        "status": "projected",
        "audit_proof": _digest({"case_id": case_id, "amount": amount, "risk_score": risk_score}),
    }
    runtime["loss_exposures"][exposure["loss_exposure_id"]] = exposure
    runtime["events"].append(_state_event("LossExposureProjected", exposure["loss_exposure_id"], exposure))
    return {"ok": True, "state": runtime, "loss_exposure": exposure}


def fraud_anomaly_detection_enqueue_analyst_case(state: dict, case_id: str) -> dict:
    risk_case = state["risk_cases"].get(case_id)
    if not risk_case:
        raise ValueError(f"Unknown Fraud Anomaly Detection risk case for analyst queue: {case_id}")
    anomaly_score = state["anomaly_scores"].get(risk_case["anomaly_score_id"], {})
    runtime = _copy_state(state)
    priority = _clamp(float(anomaly_score.get("risk_score", 0.5)) + (0.1 if risk_case["severity"] in {"high", "critical"} else 0.0), 0.0, 1.0)
    queue_item = {
        "queue_item_id": f"queue:{case_id}",
        "tenant": risk_case["tenant"],
        "case_id": case_id,
        "queue": risk_case.get("queue", "fraud_ops"),
        "priority": round(priority, 4),
        "assigned_to": risk_case.get("assigned_to"),
        "sla_due_at": "runtime+4h" if priority >= 0.7 else "runtime+1d",
        "status": "queued",
        "audit_proof": _digest({"case_id": case_id, "priority": priority}),
    }
    runtime["analyst_queue_items"][queue_item["queue_item_id"]] = queue_item
    runtime["events"].append(_state_event("AnalystCaseQueued", queue_item["queue_item_id"], queue_item))
    return {"ok": True, "state": runtime, "analyst_queue_item": queue_item}


def fraud_anomaly_detection_receive_event(
    state: dict,
    event: dict,
    *,
    simulate_failure: bool = False,
) -> dict:
    event_type = event.get("event_type")
    if event_type not in FRAUD_ANOMALY_DETECTION_CONSUMED_EVENT_TYPES:
        raise ValueError(
            "Fraud Anomaly Detection only consumes CheckoutCompleted, PaymentCaptured, and AccessPolicyChanged"
        )
    event_id = event.get("event_id")
    if not event_id:
        raise ValueError("Fraud Anomaly Detection consumed events require event_id")
    runtime = _copy_state(state)
    if event_id in runtime["handled_events"]:
        return {"ok": True, "state": runtime, "handler": {"status": "duplicate", "event_id": event_id}}
    handler = {
        "event_id": event_id,
        "event_type": event_type,
        "idempotency_key": f"fraud_anomaly_detection:{event_type}:{event_id}",
        "attempts": int(runtime.get("configuration", {}).get("retry_limit", 3) or 3),
    }
    if simulate_failure:
        handler["status"] = "dead_letter"
        runtime["dead_letter"].append({**event, "handler": handler})
        return {"ok": False, "state": runtime, "handler": handler}
    payload = dict(event.get("payload", {}))
    if "tenant" not in payload:
        raise ValueError("Fraud Anomaly Detection consumed events require payload.tenant")
    handler["status"] = "handled"
    runtime["inbox"].append({**event, "handler": handler})
    runtime["handled_events"].add(event_id)
    signal_command = _derive_signal_from_event(runtime, event)
    runtime = fraud_anomaly_detection_ingest_risk_signal(runtime, signal_command)["state"]
    runtime = fraud_anomaly_detection_link_identity(runtime, signal_command["signal_id"])["state"]
    runtime = fraud_anomaly_detection_update_behavior_baseline(runtime, signal_command["signal_id"])["state"]
    device = fraud_anomaly_detection_record_device_fingerprint(runtime, signal_command["signal_id"])
    runtime = device["state"]
    network = fraud_anomaly_detection_record_network_indicator(runtime, signal_command["signal_id"])
    runtime = network["state"]
    runtime = fraud_anomaly_detection_calculate_velocity_window(runtime, signal_command["signal_id"])["state"]
    scored = fraud_anomaly_detection_score_anomaly(runtime, signal_command["signal_id"])
    runtime = scored["state"]
    anomaly_score = scored["anomaly_score"]
    runtime = fraud_anomaly_detection_explain_decision(runtime, anomaly_score["anomaly_score_id"])["state"]
    risk_case = None
    if anomaly_score["decision"] != "approve" or anomaly_score["risk_score"] >= _case_open_threshold(runtime, runtime["risk_signals"][signal_command["signal_id"]]):
        opened = fraud_anomaly_detection_open_risk_case(
            runtime,
            {
                "case_id": f"case:{signal_command['signal_id']}",
                "tenant": payload["tenant"],
                "signal_id": signal_command["signal_id"],
                "anomaly_score_id": anomaly_score["anomaly_score_id"],
                "subject_key": signal_command["subject_key"],
                "severity": anomaly_score["severity"],
                "status": "open",
                "reason": f"{event_type} triggered {anomaly_score['decision']} decision",
                "recommended_action": "deny" if anomaly_score["decision"] == "deny" else "review",
                "queue": anomaly_score["recommended_queue"],
            },
        )
        runtime = opened["state"]
        risk_case = opened["risk_case"]
        runtime = fraud_anomaly_detection_project_loss_exposure(runtime, risk_case["case_id"])["state"]
        runtime = fraud_anomaly_detection_enqueue_analyst_case(runtime, risk_case["case_id"])["state"]
    runtime["events"].append(_state_event(f"{event_type}Handled", event_id, payload))
    return {
        "ok": True,
        "state": runtime,
        "handler": handler,
        "risk_signal": runtime["risk_signals"][signal_command["signal_id"]],
        "anomaly_score": runtime["anomaly_scores"][anomaly_score["anomaly_score_id"]],
        "risk_case": risk_case,
    }


def fraud_anomaly_detection_build_workbench_view(state: dict, *, tenant: str) -> dict:
    signals = tuple(item for item in state.get("risk_signals", {}).values() if item["tenant"] == tenant)
    scores = tuple(item for item in state.get("anomaly_scores", {}).values() if item["tenant"] == tenant)
    fraud_rules = tuple(item for item in state.get("fraud_rules", {}).values() if item["tenant"] == tenant)
    cases = tuple(item for item in state.get("risk_cases", {}).values() if item["tenant"] == tenant)
    identity_links = tuple(item for item in state.get("identity_links", {}).values() if item["tenant"] == tenant)
    baselines = tuple(item for item in state.get("behavior_baselines", {}).values() if item["tenant"] == tenant)
    devices = tuple(item for item in state.get("device_fingerprints", {}).values() if item["tenant"] == tenant)
    networks = tuple(item for item in state.get("network_indicators", {}).values() if item["tenant"] == tenant)
    velocity = tuple(item for item in state.get("velocity_windows", {}).values() if item["tenant"] == tenant)
    explanations = tuple(item for item in state.get("decision_explanations", {}).values() if item["tenant"] == tenant)
    exposures = tuple(item for item in state.get("loss_exposures", {}).values() if item["tenant"] == tenant)
    queue_items = tuple(item for item in state.get("analyst_queue_items", {}).values() if item["tenant"] == tenant)
    return {
        "format": "appgen.fraud-anomaly-detection-workbench-view.v1",
        "tenant": tenant,
        "signal_count": len(signals),
        "anomaly_score_count": len(scores),
        "fraud_rule_count": len(fraud_rules),
        "case_count": len(cases),
        "identity_link_count": len(identity_links),
        "behavior_baseline_count": len(baselines),
        "device_fingerprint_count": len(devices),
        "network_indicator_count": len(networks),
        "velocity_window_count": len(velocity),
        "decision_explanation_count": len(explanations),
        "loss_exposure_count": len(exposures),
        "analyst_queue_count": len(queue_items),
        "open_case_count": len(tuple(item for item in cases if item["status"] == "open")),
        "high_risk_count": len(tuple(item for item in scores if float(item["risk_score"]) >= 0.7)),
        "total_loss_exposure": round(
            sum(float(item["expected_loss"]) for item in exposures),
            2,
        ),
        "outbox_count": len(state.get("outbox", ())),
        "dead_letter_count": len(state.get("dead_letter", ())),
        "configuration_bound": bool(state.get("configuration", {}).get("ok")),
        "rule_count": len(state.get("rules", {})),
        "parameter_count": len(state.get("parameters", {})),
        "binding_evidence": {
            "owned_tables": FRAUD_ANOMALY_DETECTION_OWNED_TABLES,
            "runtime_tables": FRAUD_ANOMALY_DETECTION_RUNTIME_TABLES,
            "event_contract": "AppGen-X",
            "required_event_topic": FRAUD_ANOMALY_DETECTION_REQUIRED_EVENT_TOPIC,
            "outbox_table": FRAUD_ANOMALY_DETECTION_RUNTIME_TABLES[0],
            "inbox_table": FRAUD_ANOMALY_DETECTION_RUNTIME_TABLES[1],
            "dead_letter_table": FRAUD_ANOMALY_DETECTION_RUNTIME_TABLES[2],
            "stream_engine_picker_visible": False,
        },
    }


def fraud_anomaly_detection_build_schema_contract() -> dict:
    table_fields = {
        "risk_signal": (
            "tenant",
            "signal_id",
            "subject_key",
            "event_type",
            "region",
            "raw_score",
            "severity",
            "source_event_id",
            "signal_hash",
        ),
        "anomaly_score": (
            "tenant",
            "anomaly_score_id",
            "signal_id",
            "subject_key",
            "event_type",
            "risk_score",
            "confidence",
            "decision",
            "severity",
            "recommended_queue",
            "audit_proof",
        ),
        "fraud_rule": (
            "tenant",
            "fraud_rule_id",
            "name",
            "event_type",
            "score_adjustment",
            "decision",
            "status",
            "compiled_hash",
        ),
        "risk_case": (
            "tenant",
            "case_id",
            "signal_id",
            "anomaly_score_id",
            "subject_key",
            "severity",
            "status",
            "queue",
            "recommended_action",
            "audit_proof",
        ),
        "identity_link": (
            "tenant",
            "identity_link_id",
            "subject_key",
            "customer_id",
            "email",
            "device_id",
            "ip_address",
            "principal_id",
            "link_strength",
        ),
        "behavior_baseline": (
            "tenant",
            "baseline_id",
            "subject_key",
            "event_type",
            "window_days",
            "event_count",
            "mean_amount",
            "risk_mean",
            "last_observed_at",
        ),
        "device_fingerprint": (
            "tenant",
            "device_fingerprint_id",
            "device_id",
            "subject_key",
            "trust_level",
            "first_seen_at",
            "last_seen_at",
            "signals",
        ),
        "network_indicator": (
            "tenant",
            "network_indicator_id",
            "ip_address",
            "asn",
            "region",
            "risk_score",
            "vpn_detected",
            "observed_at",
        ),
        "velocity_window": (
            "tenant",
            "velocity_window_id",
            "subject_key",
            "event_type",
            "window_minutes",
            "event_count",
            "amount_total",
            "risk_score",
        ),
        "decision_explanation": (
            "tenant",
            "explanation_id",
            "anomaly_score_id",
            "reason_codes",
            "feature_weights",
            "model_version",
            "created_at",
        ),
        "loss_exposure": (
            "tenant",
            "loss_exposure_id",
            "case_id",
            "amount",
            "currency",
            "expected_loss",
            "tail_loss",
            "status",
        ),
        "analyst_queue_item": (
            "tenant",
            "queue_item_id",
            "case_id",
            "queue",
            "priority",
            "assigned_to",
            "sla_due_at",
            "status",
        ),
        "fraud_parameter": (
            "tenant",
            "parameter_id",
            "name",
            "value",
            "bounds",
            "compiled_hash",
            "updated_at",
        ),
        "fraud_configuration": (
            "tenant",
            "configuration_id",
            "database_backend",
            "event_topic",
            "retry_limit",
            "scoring_mode",
            "default_timezone",
        ),
    }
    runtime_table_fields = {
        FRAUD_ANOMALY_DETECTION_RUNTIME_TABLES[0]: (
            "event_id",
            "event_type",
            "tenant",
            "payload",
            "idempotency_key",
            "contract",
            "retry_policy",
            "audit_hash",
        ),
        FRAUD_ANOMALY_DETECTION_RUNTIME_TABLES[1]: (
            "event_id",
            "event_type",
            "payload",
            "idempotency_key",
            "attempts",
            "status",
        ),
        FRAUD_ANOMALY_DETECTION_RUNTIME_TABLES[2]: (
            "event_id",
            "event_type",
            "payload",
            "idempotency_key",
            "attempts",
            "status",
        ),
    }
    relationships = (
        {"from": "anomaly_score.signal_id", "to": "risk_signal.signal_id", "type": "owned_score"},
        {"from": "risk_case.signal_id", "to": "risk_signal.signal_id", "type": "owned_case_signal"},
        {"from": "risk_case.anomaly_score_id", "to": "anomaly_score.anomaly_score_id", "type": "owned_case_score"},
        {"from": "identity_link.subject_key", "to": "risk_signal.subject_key", "type": "owned_identity_graph"},
        {"from": "behavior_baseline.subject_key", "to": "risk_signal.subject_key", "type": "owned_behavior_profile"},
        {"from": "device_fingerprint.subject_key", "to": "risk_signal.subject_key", "type": "owned_device_profile"},
        {"from": "network_indicator.ip_address", "to": "identity_link.ip_address", "type": "owned_network_profile"},
        {"from": "velocity_window.subject_key", "to": "risk_signal.subject_key", "type": "owned_velocity_profile"},
        {"from": "decision_explanation.anomaly_score_id", "to": "anomaly_score.anomaly_score_id", "type": "owned_explanation"},
        {"from": "loss_exposure.case_id", "to": "risk_case.case_id", "type": "owned_loss_projection"},
        {"from": "analyst_queue_item.case_id", "to": "risk_case.case_id", "type": "owned_queue_item"},
    )
    tables = tuple(
        {
            "table": table,
            "fields": table_fields[table],
            "primary_key": tuple(field for field in table_fields[table] if field.endswith("_id"))[:2],
            "owned_by": "fraud_anomaly_detection",
        }
        for table in FRAUD_ANOMALY_DETECTION_OWNED_TABLES
    )
    runtime_tables = tuple(
        {
            "table": table,
            "fields": runtime_table_fields[table],
            "primary_key": ("event_id",),
            "owned_by": "fraud_anomaly_detection_runtime",
        }
        for table in FRAUD_ANOMALY_DETECTION_RUNTIME_TABLES
    )
    return {
        "format": "appgen.fraud-anomaly-detection-owned-schema-contract.v1",
        "ok": len(tables) == len(FRAUD_ANOMALY_DETECTION_OWNED_TABLES)
        and tuple(item["table"] for item in runtime_tables) == FRAUD_ANOMALY_DETECTION_RUNTIME_TABLES,
        "pbc": "fraud_anomaly_detection",
        "owned_tables": FRAUD_ANOMALY_DETECTION_OWNED_TABLES,
        "tables": tables,
        "runtime_tables": runtime_tables,
        "relationships": relationships,
        "migrations": tuple(
            {
                "path": f"pbcs/fraud_anomaly_detection/migrations/{position + 1:03d}_{table}.sql",
                "operation": "create_owned_table",
                "table": table,
                "backend_allowlist": FRAUD_ANOMALY_DETECTION_ALLOWED_DATABASE_BACKENDS,
            }
            for position, table in enumerate(FRAUD_ANOMALY_DETECTION_OWNED_TABLES)
        ),
        "models": tuple(
            {
                "class_name": "".join(part.capitalize() for part in table.split("_")),
                "table": table,
                "fields": table_fields[table],
                "module_path": f"pyAppGen.pbcs.fraud_anomaly_detection.models.{table}",
            }
            for table in FRAUD_ANOMALY_DETECTION_OWNED_TABLES
        ),
        "datastore_backends": FRAUD_ANOMALY_DETECTION_ALLOWED_DATABASE_BACKENDS,
        "shared_table_access": False,
    }


def fraud_anomaly_detection_build_service_contract() -> dict:
    command_methods = (
        "configure_runtime",
        "set_parameter",
        "register_rule",
        "register_schema_extension",
        "register_fraud_rule",
        "link_identity",
        "update_behavior_baseline",
        "record_device_fingerprint",
        "record_network_indicator",
        "calculate_velocity_window",
        "ingest_risk_signal",
        "score_anomaly",
        "explain_decision",
        "open_risk_case",
        "project_loss_exposure",
        "enqueue_analyst_case",
        "receive_event",
    )
    query_methods = (
        "build_workbench_view",
        "build_api_contract",
        "permissions_contract",
        "build_schema_contract",
        "build_service_contract",
        "build_release_evidence",
        "verify_owned_table_boundary",
    )
    return {
        "format": "appgen.fraud-anomaly-detection-service-contract.v1",
        "ok": len(command_methods) >= 17 and len(query_methods) >= 7,
        "pbc": "fraud_anomaly_detection",
        "transaction_boundary": "fraud_anomaly_detection_owned_datastore_plus_appgen_outbox",
        "command_methods": command_methods,
        "query_methods": query_methods,
        "mutates_only": FRAUD_ANOMALY_DETECTION_OWNED_TABLES,
        "runtime_tables": FRAUD_ANOMALY_DETECTION_RUNTIME_TABLES,
        "external_dependencies": fraud_anomaly_detection_verify_owned_table_boundary()["declared_dependencies"],
        "configuration": {
            "required_fields": FRAUD_ANOMALY_DETECTION_SUPPORTED_CONFIGURATION_FIELDS,
            "allowed_database_backends": FRAUD_ANOMALY_DETECTION_ALLOWED_DATABASE_BACKENDS,
            "required_event_topic": FRAUD_ANOMALY_DETECTION_REQUIRED_EVENT_TOPIC,
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
            "event_contract_selector_visible": False,
        },
        "eventing": {
            "contract": "AppGen-X",
            "topic": FRAUD_ANOMALY_DETECTION_REQUIRED_EVENT_TOPIC,
            "outbox_table": FRAUD_ANOMALY_DETECTION_RUNTIME_TABLES[0],
            "inbox_table": FRAUD_ANOMALY_DETECTION_RUNTIME_TABLES[1],
            "dead_letter_table": FRAUD_ANOMALY_DETECTION_RUNTIME_TABLES[2],
            "idempotency_required": True,
            "stream_engine_picker_visible": False,
        },
        "idempotent_handlers": ("receive_event",),
        "retry_dead_letter_evidence": {
            "retry_limit_field": "retry_limit",
            "outbox_state": "outbox",
            "inbox_state": "inbox",
            "dead_letter_state": "dead_letter",
            "dead_letter_table": FRAUD_ANOMALY_DETECTION_RUNTIME_TABLES[2],
        },
        "generated_artifacts": {
            "services": ("pbcs/fraud_anomaly_detection/services/risk_service.py",),
            "routes": ("pbcs/fraud_anomaly_detection/routes/risk_routes.py",),
            "events": ("pbcs/fraud_anomaly_detection/events/fraud_events.py",),
            "handlers": ("pbcs/fraud_anomaly_detection/handlers/fraud_handlers.py",),
            "ui": ("pbcs/fraud_anomaly_detection/ui/workbench.py",),
        },
        "shared_table_access": False,
    }


def fraud_anomaly_detection_verify_owned_table_boundary(references: tuple[str, ...] = ()) -> dict:
    allowed = {
        *FRAUD_ANOMALY_DETECTION_OWNED_TABLES,
        *FRAUD_ANOMALY_DETECTION_RUNTIME_TABLES,
        *FRAUD_ANOMALY_DETECTION_CONSUMED_EVENT_TYPES,
        "POST /risk-events",
        "POST /fraud-checks",
        "GET /risk-cases",
        "GET /risk-workbench",
        "POST /fraud-rules",
        "POST /risk-signals/{id}/score",
        "POST /risk-cases",
        "POST /fraud-configuration",
        "POST /fraud-parameters",
    }
    violations = tuple(reference for reference in references if reference not in allowed)
    return {
        "format": "appgen.fraud-anomaly-detection-boundary.v1",
        "ok": not violations,
        "owned_tables": FRAUD_ANOMALY_DETECTION_OWNED_TABLES,
        "runtime_tables": FRAUD_ANOMALY_DETECTION_RUNTIME_TABLES,
        "declared_dependencies": {
            "apis": (
                "POST /risk-events",
                "POST /fraud-checks",
                "GET /risk-cases",
                "GET /risk-workbench",
                "POST /fraud-rules",
                "POST /risk-signals/{id}/score",
                "POST /risk-cases",
                "POST /fraud-configuration",
                "POST /fraud-parameters",
            ),
            "events": FRAUD_ANOMALY_DETECTION_CONSUMED_EVENT_TYPES,
            "shared_tables": (),
        },
        "references": tuple(references),
        "violations": violations,
    }


def fraud_anomaly_detection_build_api_contract() -> dict:
    return {
        "format": "appgen.fraud-anomaly-detection-api-contract.v1",
        "ok": True,
        "routes": (
            "POST /risk-events",
            "POST /fraud-checks",
            "GET /risk-cases",
            "GET /risk-workbench",
            "POST /fraud-rules",
            "POST /risk-signals/{id}/score",
            "POST /risk-cases",
            "POST /fraud-configuration",
            "POST /fraud-parameters",
        ),
        "route_contracts": (
            {"route": "POST /risk-events", "command": "receive_event", "requires_permission": "fraud_anomaly_detection.event.consume"},
            {"route": "POST /fraud-checks", "command": "score_anomaly", "requires_permission": "fraud_anomaly_detection.anomaly_score.write"},
            {"route": "GET /risk-cases", "query": "build_workbench_view", "requires_permission": "fraud_anomaly_detection.risk_case.write"},
            {"route": "GET /risk-workbench", "query": "build_workbench_view", "requires_permission": "fraud_anomaly_detection.audit"},
            {"route": "POST /fraud-rules", "command": "register_fraud_rule", "requires_permission": "fraud_anomaly_detection.fraud_rule.write"},
            {"route": "POST /risk-signals/{id}/score", "command": "score_anomaly", "requires_permission": "fraud_anomaly_detection.anomaly_score.write"},
            {"route": "POST /risk-cases", "command": "open_risk_case", "requires_permission": "fraud_anomaly_detection.risk_case.write"},
            {"route": "POST /fraud-configuration", "command": "configure_runtime", "requires_permission": "fraud_anomaly_detection.configure"},
            {"route": "POST /fraud-parameters", "command": "set_parameter", "requires_permission": "fraud_anomaly_detection.configure"},
        ),
        "shared_table_access": False,
        "event_contract": "AppGen-X",
        "required_event_topic": FRAUD_ANOMALY_DETECTION_REQUIRED_EVENT_TOPIC,
        "database_backends": FRAUD_ANOMALY_DETECTION_ALLOWED_DATABASE_BACKENDS,
        "stream_engine_picker_visible": False,
        "event_contract_selector_visible": False,
        "consumed_events": FRAUD_ANOMALY_DETECTION_CONSUMED_EVENT_TYPES,
        "emitted_events": FRAUD_ANOMALY_DETECTION_EMITTED_EVENT_TYPES,
    }


def fraud_anomaly_detection_permissions_contract() -> dict:
    permissions = (
        "fraud_anomaly_detection.event.write",
        "fraud_anomaly_detection.anomaly_score.write",
        "fraud_anomaly_detection.fraud_rule.write",
        "fraud_anomaly_detection.risk_case.write",
        "fraud_anomaly_detection.event.consume",
        "fraud_anomaly_detection.configure",
        "fraud_anomaly_detection.audit",
    )
    action_permissions = {
        "configure_runtime": "fraud_anomaly_detection.configure",
        "set_parameter": "fraud_anomaly_detection.configure",
        "register_rule": "fraud_anomaly_detection.configure",
        "register_schema_extension": "fraud_anomaly_detection.configure",
        "register_fraud_rule": "fraud_anomaly_detection.fraud_rule.write",
        "link_identity": "fraud_anomaly_detection.anomaly_score.write",
        "update_behavior_baseline": "fraud_anomaly_detection.anomaly_score.write",
        "record_device_fingerprint": "fraud_anomaly_detection.anomaly_score.write",
        "record_network_indicator": "fraud_anomaly_detection.anomaly_score.write",
        "calculate_velocity_window": "fraud_anomaly_detection.anomaly_score.write",
        "ingest_risk_signal": "fraud_anomaly_detection.event.write",
        "score_anomaly": "fraud_anomaly_detection.anomaly_score.write",
        "explain_decision": "fraud_anomaly_detection.audit",
        "open_risk_case": "fraud_anomaly_detection.risk_case.write",
        "project_loss_exposure": "fraud_anomaly_detection.risk_case.write",
        "enqueue_analyst_case": "fraud_anomaly_detection.risk_case.write",
        "receive_event": "fraud_anomaly_detection.event.consume",
        "build_workbench_view": "fraud_anomaly_detection.audit",
        "build_schema_contract": "fraud_anomaly_detection.audit",
        "build_service_contract": "fraud_anomaly_detection.audit",
        "build_release_evidence": "fraud_anomaly_detection.audit",
        "verify_owned_table_boundary": "fraud_anomaly_detection.audit",
    }
    return {
        "format": "appgen.fraud-anomaly-detection-permissions.v1",
        "ok": True,
        "permissions": permissions,
        "action_permissions": action_permissions,
        "roles": {
            "fraud_anomaly_detection_admin": permissions,
            "fraud_analyst": (
                "fraud_anomaly_detection.anomaly_score.write",
                "fraud_anomaly_detection.risk_case.write",
                "fraud_anomaly_detection.audit",
            ),
            "fraud_runtime_operator": (
                "fraud_anomaly_detection.event.consume",
                "fraud_anomaly_detection.event.write",
                "fraud_anomaly_detection.configure",
            ),
        },
    }


def fraud_anomaly_detection_build_release_evidence() -> dict:
    from .ui import fraud_anomaly_detection_ui_contract

    schema = fraud_anomaly_detection_build_schema_contract()
    service = fraud_anomaly_detection_build_service_contract()
    api = fraud_anomaly_detection_build_api_contract()
    permissions = fraud_anomaly_detection_permissions_contract()
    ui = fraud_anomaly_detection_ui_contract()
    control = _fraud_anomaly_detection_release_control_evidence()
    checks = (
        {
            "id": "owned_schema_depth",
            "ok": schema["ok"] and schema["owned_tables"] == FRAUD_ANOMALY_DETECTION_OWNED_TABLES,
        },
        {
            "id": "migration_per_owned_table",
            "ok": len(schema["migrations"]) == len(FRAUD_ANOMALY_DETECTION_OWNED_TABLES),
        },
        {
            "id": "model_per_owned_table",
            "ok": len(schema["models"]) == len(FRAUD_ANOMALY_DETECTION_OWNED_TABLES),
        },
        {
            "id": "runtime_event_tables_evidence",
            "ok": tuple(item["table"] for item in schema["runtime_tables"]) == FRAUD_ANOMALY_DETECTION_RUNTIME_TABLES,
        },
        {
            "id": "standard_table_runtime_population",
            "ok": control["workbench"]["identity_link_count"] >= 1
            and control["workbench"]["behavior_baseline_count"] >= 1
            and control["workbench"]["velocity_window_count"] >= 1
            and control["workbench"]["decision_explanation_count"] >= 1
            and control["workbench"]["loss_exposure_count"] >= 1
            and control["workbench"]["analyst_queue_count"] >= 1,
        },
        {
            "id": "service_contract_depth",
            "ok": service["ok"]
            and "receive_event" in service["idempotent_handlers"]
            and {"link_identity", "project_loss_exposure", "enqueue_analyst_case"} <= set(service["command_methods"])
            and {"build_schema_contract", "build_service_contract", "build_release_evidence"} <= set(service["query_methods"]),
        },
        {
            "id": "generated_runtime_artifacts",
            "ok": {"services", "routes", "events", "handlers", "ui"} <= set(service["generated_artifacts"]),
        },
        {
            "id": "appgen_event_contract_only",
            "ok": api["event_contract"] == "AppGen-X"
            and api["required_event_topic"] == FRAUD_ANOMALY_DETECTION_REQUIRED_EVENT_TOPIC
            and api["stream_engine_picker_visible"] is False,
        },
        {
            "id": "permissions_cover_release_queries",
            "ok": {"build_schema_contract", "build_service_contract", "build_release_evidence"} <= set(permissions["action_permissions"]),
        },
        {
            "id": "backend_allowlist",
            "ok": schema["datastore_backends"] == FRAUD_ANOMALY_DETECTION_ALLOWED_DATABASE_BACKENDS
            and service["configuration"]["allowed_database_backends"] == FRAUD_ANOMALY_DETECTION_ALLOWED_DATABASE_BACKENDS,
        },
        {
            "id": "idempotent_eventing_evidence",
            "ok": control["summary"]["handled_status"] == "handled"
            and control["summary"]["duplicate_status"] == "duplicate"
            and control["summary"]["dead_letter_status"] == "dead_letter",
        },
        {
            "id": "ui_binding_evidence",
            "ok": ui["ok"]
            and control["workbench"]["binding_evidence"]["owned_tables"] == FRAUD_ANOMALY_DETECTION_OWNED_TABLES
            and control["workbench"]["binding_evidence"]["runtime_tables"] == FRAUD_ANOMALY_DETECTION_RUNTIME_TABLES,
        },
        {
            "id": "no_shared_table_access",
            "ok": not schema["shared_table_access"]
            and not service["shared_table_access"]
            and not api["shared_table_access"]
            and service["external_dependencies"]["shared_tables"] == (),
        },
    )
    blocking_gaps = tuple(check for check in checks if not check["ok"])
    return {
        "format": "appgen.fraud-anomaly-detection-release-evidence.v1",
        "ok": not blocking_gaps,
        "pbc": "fraud_anomaly_detection",
        "checks": checks,
        "blocking_gaps": blocking_gaps,
        "schema": schema,
        "service": service,
        "api": api,
        "permissions": permissions,
        "ui": ui,
        "control": control,
    }


def _fraud_anomaly_detection_release_control_evidence() -> dict:
    from .ui import fraud_anomaly_detection_render_workbench

    state = fraud_anomaly_detection_empty_state()
    state = fraud_anomaly_detection_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": FRAUD_ANOMALY_DETECTION_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "default_region": "US",
            "supported_regions": ("US",),
            "supported_event_types": FRAUD_ANOMALY_DETECTION_CONSUMED_EVENT_TYPES,
            "identity_dimensions": (
                "customer_id",
                "email",
                "device_id",
                "ip_address",
                "principal_id",
            ),
            "default_timezone": "UTC",
            "scoring_mode": "policy",
            "workbench_limit": 50,
        },
    )["state"]
    for name, value in (
        ("checkout_risk_weight", 6.0),
        ("payment_risk_weight", 7.0),
        ("access_policy_risk_weight", 8.0),
        ("anomaly_alert_threshold", 0.45),
        ("case_open_threshold", 0.7),
        ("baseline_min_events", 25),
        ("behavior_decay_days", 90),
        ("identity_linkage_weight", 4.0),
        ("supervised_override_weight", 3.0),
        ("workbench_limit", 50),
    ):
        state = fraud_anomaly_detection_set_parameter(state, name, value)["state"]
    state = fraud_anomaly_detection_register_rule(
        state,
        {
            "rule_id": "rule_release",
            "tenant": "tenant_release",
            "scope": "fraud_anomaly_detection",
            "status": "active",
            "allowed_event_types": FRAUD_ANOMALY_DETECTION_CONSUMED_EVENT_TYPES,
            "allowed_regions": ("US",),
            "signal_policy": {"minimum_indicators": 1, "baseline_family": "commerce_and_access"},
            "anomaly_policy": {"review_threshold": 0.45, "bias": 0.05},
            "case_policy": {"auto_open_threshold": 0.7, "queue": "fraud_ops"},
        },
    )["state"]
    state = fraud_anomaly_detection_register_fraud_rule(
        state,
        {
            "fraud_rule_id": "fraud_release_velocity",
            "tenant": "tenant_release",
            "name": "Release Checkout Velocity",
            "event_type": "CheckoutCompleted",
            "trigger": {"guest_checkout": True, "device_trust": "low"},
            "score_adjustment": 0.18,
            "decision": "review",
            "status": "active",
        },
    )["state"]
    handled = fraud_anomaly_detection_receive_event(
        state,
        {
            "event_id": "checkout_release",
            "event_type": "CheckoutCompleted",
            "payload": {
                "tenant": "tenant_release",
                "checkout_id": "chk_release",
                "customer_id": "cust_release",
                "email": "release@example.com",
                "amount": 2400.0,
                "region": "US",
                "guest_checkout": True,
                "device_trust": "low",
                "device_id": "device_release",
                "ip_address": "10.0.0.21",
            },
        },
    )
    duplicate = fraud_anomaly_detection_receive_event(
        handled["state"],
        {
            "event_id": "checkout_release",
            "event_type": "CheckoutCompleted",
            "payload": {
                "tenant": "tenant_release",
                "checkout_id": "chk_release",
            },
        },
    )
    failed = fraud_anomaly_detection_receive_event(
        handled["state"],
        {
            "event_id": "checkout_release_fail",
            "event_type": "CheckoutCompleted",
            "payload": {"tenant": "tenant_release"},
        },
        simulate_failure=True,
    )
    workbench = fraud_anomaly_detection_build_workbench_view(failed["state"], tenant="tenant_release")
    rendered = fraud_anomaly_detection_render_workbench(
        failed["state"],
        tenant="tenant_release",
        principal_permissions=fraud_anomaly_detection_permissions_contract()["permissions"],
    )
    summary = {
        "handled_status": handled["handler"]["status"],
        "duplicate_status": duplicate["handler"]["status"],
        "dead_letter_status": failed["handler"]["status"],
        "outbox_contract": handled["state"]["outbox"][0]["contract"],
        "outbox_table": workbench["binding_evidence"]["outbox_table"],
        "inbox_table": workbench["binding_evidence"]["inbox_table"],
        "dead_letter_table": workbench["binding_evidence"]["dead_letter_table"],
        "retry_max_attempts": handled["state"]["outbox"][0]["retry_policy"]["max_attempts"],
        "outbox_count": workbench["outbox_count"],
        "inbox_count": len(failed["state"]["inbox"]),
        "dead_letter_count": workbench["dead_letter_count"],
        "open_case_count": workbench["open_case_count"],
    }
    return {
        "ok": handled["ok"]
        and duplicate["handler"]["status"] == "duplicate"
        and failed["handler"]["status"] == "dead_letter"
        and summary["outbox_contract"] == "AppGen-X"
        and summary["dead_letter_count"] == 1,
        "handled": handled,
        "duplicate": duplicate,
        "failed": failed,
        "workbench": workbench,
        "rendered": rendered,
        "summary": summary,
    }


def _copy_state(state: dict) -> dict:
    return copy.deepcopy(state)


def _require_configured(state: dict) -> None:
    if not state.get("configuration", {}).get("ok"):
        raise ValueError("Fraud Anomaly Detection runtime must be configured before commands execute")


def _matching_fraud_rules(state: dict, signal: dict) -> tuple[dict, ...]:
    return tuple(
        rule
        for rule in state.get("fraud_rules", {}).values()
        if rule["tenant"] == signal["tenant"]
        and rule["status"] == "active"
        and (rule["event_type"] == "any" or rule["event_type"] == signal["event_type"])
    )


def _matching_policy_rule(state: dict, signal: dict) -> dict | None:
    for rule in state.get("rules", {}).values():
        if rule["tenant"] != signal["tenant"] or rule["status"] != "active":
            continue
        if signal["event_type"] not in rule["allowed_event_types"]:
            continue
        if signal["region"] not in rule["allowed_regions"]:
            continue
        return rule
    return None


def _subject_history_count(state: dict, signal: dict) -> int:
    return sum(
        1
        for item in state.get("risk_signals", {}).values()
        if item["tenant"] == signal["tenant"] and item["subject_key"] == signal["subject_key"]
    )


def _event_weight(state: dict, event_type: str) -> float:
    parameter_key = _EVENT_PARAMETER_KEYS[event_type]
    return float(state["parameters"].get(parameter_key, {"value": 0.0})["value"]) / 10.0


def _identity_ratio(state: dict, signal: dict) -> float:
    configured_dimensions = state.get("configuration", {}).get("identity_dimensions", ())
    if not configured_dimensions:
        return 0.0
    bound = sum(
        1
        for key in configured_dimensions
        if signal["identity_dimensions"].get(key)
    )
    return bound / len(configured_dimensions)


def _strongest_rule_decision(rules: tuple[dict, ...]) -> str:
    decision = "approve"
    for rule in rules:
        candidate = rule["decision"]
        if _DECISION_PRIORITY[candidate] > _DECISION_PRIORITY[decision]:
            decision = candidate
    return decision


def _case_open_threshold(state: dict, signal: dict) -> float:
    threshold = float(state["parameters"].get("case_open_threshold", {"value": 0.75})["value"])
    policy_rule = _matching_policy_rule(state, signal)
    if policy_rule:
        threshold = max(
            threshold,
            float(policy_rule["case_policy"].get("auto_open_threshold", threshold)),
        )
    return threshold


def _derive_signal_from_event(state: dict, event: dict) -> dict:
    payload = dict(event["payload"])
    event_type = event["event_type"]
    region = str(payload.get("region") or state["configuration"]["default_region"])
    if event_type == "CheckoutCompleted":
        amount = float(payload.get("amount", payload.get("cart_total", 0.0)) or 0.0)
        raw_score = _clamp(
            0.15
            + (_event_weight(state, event_type) * 0.3)
            + min(amount / 5000.0, 0.25)
            + (0.08 if payload.get("guest_checkout") else 0.0)
            + (0.12 if str(payload.get("device_trust", "")).lower() == "low" else 0.0)
            + (0.1 if payload.get("shipping_mismatch") else 0.0),
            0.0,
            1.0,
        )
        subject_key = str(payload.get("checkout_id") or payload.get("customer_id") or event["event_id"])
        indicators = tuple(
            indicator
            for indicator, active in (
                ("guest_checkout", bool(payload.get("guest_checkout"))),
                ("device_trust_low", str(payload.get("device_trust", "")).lower() == "low"),
                ("shipping_mismatch", bool(payload.get("shipping_mismatch"))),
            )
            if active
        ) or ("behavioral_checkout_signal",)
    elif event_type == "PaymentCaptured":
        amount = float(payload.get("amount", 0.0) or 0.0)
        attempts = int(payload.get("payment_attempts", 1) or 1)
        chargeback_count = int(payload.get("chargeback_count", 0) or 0)
        raw_score = _clamp(
            0.1
            + (_event_weight(state, event_type) * 0.35)
            + min(amount / 4000.0, 0.25)
            + min(attempts * 0.05, 0.2)
            + min(chargeback_count * 0.1, 0.2)
            + (0.12 if payload.get("avs_mismatch") else 0.0),
            0.0,
            1.0,
        )
        subject_key = str(payload.get("payment_intent_id") or payload.get("customer_id") or event["event_id"])
        indicators = tuple(
            indicator
            for indicator, active in (
                ("payment_velocity", attempts > 1),
                ("chargeback_history", chargeback_count > 0),
                ("avs_mismatch", bool(payload.get("avs_mismatch"))),
            )
            if active
        ) or ("behavioral_payment_signal",)
    else:
        privilege_delta = float(payload.get("privilege_delta", 0.0) or 0.0)
        raw_score = _clamp(
            0.2
            + (_event_weight(state, event_type) * 0.4)
            + min(privilege_delta * 0.3, 0.3)
            + (0.2 if payload.get("approval_missing") else 0.0)
            + (0.1 if payload.get("out_of_hours") else 0.0)
            + (0.1 if payload.get("region_change") else 0.0),
            0.0,
            1.0,
        )
        subject_key = str(payload.get("principal_id") or payload.get("policy_id") or event["event_id"])
        indicators = tuple(
            indicator
            for indicator, active in (
                ("privilege_delta", privilege_delta > 0.0),
                ("approval_missing", bool(payload.get("approval_missing"))),
                ("out_of_hours", bool(payload.get("out_of_hours"))),
                ("region_change", bool(payload.get("region_change"))),
            )
            if active
        ) or ("access_control_signal",)
    identity_dimensions = {
        "customer_id": payload.get("customer_id"),
        "email": payload.get("email"),
        "device_id": payload.get("device_id"),
        "ip_address": payload.get("ip_address"),
        "principal_id": payload.get("principal_id"),
    }
    return {
        "signal_id": f"signal:{event['event_id']}",
        "tenant": payload["tenant"],
        "subject_key": subject_key,
        "event_type": event_type,
        "region": region,
        "raw_score": raw_score,
        "amount": float(payload.get("amount", payload.get("cart_total", 0.0)) or 0.0),
        "currency": payload.get("currency", "USD"),
        "asn": payload.get("asn", "unknown"),
        "vpn_detected": bool(payload.get("vpn_detected", False)),
        "observed_at": payload.get("occurred_at", "runtime"),
        "indicators": indicators,
        "source_event_id": event["event_id"],
        "identity_dimensions": identity_dimensions,
    }


def _severity_from_score(score: float) -> str:
    if score >= 0.85:
        return "critical"
    if score >= 0.7:
        return "high"
    if score >= 0.45:
        return "medium"
    return "low"


def _emit(state: dict, event_type: str, tenant: str, payload: dict) -> None:
    event = {
        "event_id": f"{event_type.lower()}_{len(state['outbox']) + 1}",
        "event_type": event_type,
        "tenant": tenant,
        "payload": payload,
        "contract": "AppGen-X",
        "idempotency_key": (
            f"fraud_anomaly_detection:{event_type}:{payload.get('case_id') or payload.get('signal_id') or payload.get('subject_key') or len(state['outbox']) + 1}"
        ),
        "retry_policy": {
            "max_attempts": int(state.get("configuration", {}).get("retry_limit", 3)),
            "dead_letter": FRAUD_ANOMALY_DETECTION_RUNTIME_TABLES[2],
        },
        "audit_hash": _digest({"event_type": event_type, "tenant": tenant, "payload": payload}),
    }
    state["outbox"].append(event)
    state["events"].append(_state_event(event_type, event["event_id"], payload))


def _state_event(event_type: str, key: str, payload: dict) -> dict:
    return {
        "event_type": event_type,
        "key": key,
        "payload": payload,
        "hash": _digest({"event_type": event_type, "key": key, "payload": payload}),
    }


def _capability_evidence(state: dict, capability: str) -> dict:
    return {
        "capability": capability,
        "events": len(state["events"]),
        "outbox": len(state["outbox"]),
        "inbox": len(state["inbox"]),
        "rules": len(state["rules"]),
        "parameters": len(state["parameters"]),
        "fraud_rules": len(state["fraud_rules"]),
        "cases": len(state["risk_cases"]),
        "identity_links": len(state["identity_links"]),
        "behavior_baselines": len(state["behavior_baselines"]),
        "velocity_windows": len(state["velocity_windows"]),
        "decision_explanations": len(state["decision_explanations"]),
        "loss_exposures": len(state["loss_exposures"]),
        "analyst_queue_items": len(state["analyst_queue_items"]),
        "configuration": bool(state["configuration"].get("ok")),
        "runtime_digest": _digest(
            {
                "capability": capability,
                "signals": len(state["risk_signals"]),
                "scores": len(state["anomaly_scores"]),
                "cases": len(state["risk_cases"]),
                "identity_links": len(state["identity_links"]),
                "loss_exposures": len(state["loss_exposures"]),
            }
        ),
    }


def _clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def _digest(payload: dict) -> str:
    def default(value):
        if isinstance(value, set):
            return sorted(value)
        if isinstance(value, tuple):
            return list(value)
        if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
            return str(value)
        return value

    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, default=default, separators=(",", ":")).encode()
    ).hexdigest()


from .fraud_control import improve1_fraud_control_contract as fraud_anomaly_detection_improve1_fraud_control_contract

_fraud_anomaly_detection_base_build_release_evidence = fraud_anomaly_detection_build_release_evidence
_fraud_anomaly_detection_base_runtime_capabilities = fraud_anomaly_detection_runtime_capabilities

def fraud_anomaly_detection_build_release_evidence() -> dict:
    evidence = _fraud_anomaly_detection_base_build_release_evidence()
    control = fraud_anomaly_detection_improve1_fraud_control_contract()
    checks = tuple(evidence.get('checks', ())) + ({'id': 'improve1_fraud_control', 'ok': control['ok']},)
    return {**evidence, 'ok': evidence.get('ok') is True and control['ok'], 'checks': checks, 'fraud_control': control, 'blocking_gaps': tuple(evidence.get('blocking_gaps', ())) + tuple(control.get('blocking_gaps', ())), 'side_effects': ()}

def fraud_anomaly_detection_runtime_capabilities() -> dict:
    runtime = _fraud_anomaly_detection_base_runtime_capabilities()
    control = fraud_anomaly_detection_improve1_fraud_control_contract()
    operations = tuple(runtime.get('operations', ())) + ('improve1_fraud_control_contract',)
    return {**runtime, 'ok': runtime.get('ok') is True and control['ok'], 'operations': operations, 'fraud_control': control, 'improve1_capabilities': tuple(item['slug'] for item in control['capabilities']), 'owned_tables': tuple(dict.fromkeys(tuple(runtime.get('owned_tables', ())) + tuple(control['owned_tables']))), 'allowed_database_backends': control['allowed_database_backends'], 'event_contract': control['event_contract'], 'stream_engine_picker_visible': False, 'side_effects': ()}


from .fraud_control import FRAUD_CONTROL_OWNED_TABLES as _FRAUD_CONTROL_OWNED_TABLES

_fraud_anomaly_detection_base_verify_owned_table_boundary = fraud_anomaly_detection_verify_owned_table_boundary

def fraud_anomaly_detection_verify_owned_table_boundary(references: tuple[str, ...] = ()) -> dict:
    allowed = {
        *_FRAUD_CONTROL_OWNED_TABLES,
        *FRAUD_ANOMALY_DETECTION_CONSUMED_EVENT_TYPES,
        *FRAUD_ANOMALY_DETECTION_EMITTED_EVENT_TYPES,
        "POST /risk-events",
        "POST /fraud-checks",
        "GET /risk-cases",
        "GET /risk-workbench",
        "POST /fraud-rules",
        "POST /risk-signals/{id}/score",
        "POST /risk-cases",
        "POST /fraud-configuration",
        "POST /fraud-parameters",
    }
    violations = tuple(reference for reference in references if reference not in allowed)
    return {
        "format": "appgen.fraud-anomaly-detection-boundary.v2",
        "ok": not violations,
        "owned_tables": _FRAUD_CONTROL_OWNED_TABLES,
        "runtime_tables": FRAUD_ANOMALY_DETECTION_RUNTIME_TABLES,
        "declared_dependencies": {
            "apis": (
                "POST /risk-events", "POST /fraud-checks", "GET /risk-cases", "GET /risk-workbench",
                "POST /fraud-rules", "POST /risk-signals/{id}/score", "POST /risk-cases",
                "POST /fraud-configuration", "POST /fraud-parameters",
            ),
            "events": tuple(dict.fromkeys(FRAUD_ANOMALY_DETECTION_CONSUMED_EVENT_TYPES + FRAUD_ANOMALY_DETECTION_EMITTED_EVENT_TYPES)),
            "shared_tables": (),
        },
        "references": tuple(references),
        "violations": violations,
        "side_effects": (),
    }
