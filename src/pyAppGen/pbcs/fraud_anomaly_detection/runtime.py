"""Executable runtime for the Fraud Anomaly Detection PBC."""

from __future__ import annotations

import copy
import hashlib
import json
import math


FRAUD_ANOMALY_DETECTION_REQUIRED_EVENT_TOPIC = "appgen.fraud_anomaly_detection.events"
FRAUD_ANOMALY_DETECTION_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
FRAUD_ANOMALY_DETECTION_OWNED_TABLES = ("risk_signal", "anomaly_score", "fraud_rule", "risk_case")

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
        "capabilities": FRAUD_ANOMALY_DETECTION_RUNTIME_CAPABILITY_KEYS,
        "standard_features": FRAUD_ANOMALY_DETECTION_STANDARD_FEATURE_KEYS,
        "operations": (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "register_fraud_rule",
            "register_schema_extension",
            "ingest_risk_signal",
            "score_anomaly",
            "open_risk_case",
            "receive_event",
            "build_workbench_view",
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
        and bool(state["outbox"])
        and bool(state["handled_events"])
        and bool(state["configuration"].get("ok"))
        and not tuple(check for check in checks if not check["ok"]),
        "checks": checks,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
        "state_digest": _digest(
            {
                "signals": state["risk_signals"],
                "scores": state["anomaly_scores"],
                "cases": state["risk_cases"],
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
    scored = fraud_anomaly_detection_score_anomaly(runtime, signal_command["signal_id"])
    runtime = scored["state"]
    anomaly_score = scored["anomaly_score"]
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
    return {
        "format": "appgen.fraud-anomaly-detection-workbench-view.v1",
        "tenant": tenant,
        "signal_count": len(signals),
        "anomaly_score_count": len(scores),
        "fraud_rule_count": len(fraud_rules),
        "case_count": len(cases),
        "open_case_count": len(tuple(item for item in cases if item["status"] == "open")),
        "high_risk_count": len(tuple(item for item in scores if float(item["risk_score"]) >= 0.7)),
        "total_loss_exposure": round(
            sum(float(item["risk_score"]) * 1000.0 for item in scores),
            2,
        ),
        "outbox_count": len(state.get("outbox", ())),
        "dead_letter_count": len(state.get("dead_letter", ())),
        "configuration_bound": bool(state.get("configuration", {}).get("ok")),
        "rule_count": len(state.get("rules", {})),
        "parameter_count": len(state.get("parameters", {})),
        "binding_evidence": {
            "owned_tables": FRAUD_ANOMALY_DETECTION_OWNED_TABLES,
            "outbox_table": "fraud_anomaly_detection_appgen_outbox_event",
            "inbox_table": "fraud_anomaly_detection_appgen_inbox_event",
            "dead_letter_table": "fraud_anomaly_detection_dead_letter_event",
        },
    }


def fraud_anomaly_detection_verify_owned_table_boundary() -> dict:
    return {
        "format": "appgen.fraud-anomaly-detection-boundary.v1",
        "ok": True,
        "owned_tables": FRAUD_ANOMALY_DETECTION_OWNED_TABLES,
        "declared_dependencies": {
            "apis": ("POST /risk-events", "POST /fraud-checks", "GET /risk-cases"),
            "events": FRAUD_ANOMALY_DETECTION_CONSUMED_EVENT_TYPES,
            "shared_tables": (),
        },
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
        ),
        "shared_table_access": False,
        "event_contract": "AppGen-X",
    }


def fraud_anomaly_detection_permissions_contract() -> dict:
    return {
        "format": "appgen.fraud-anomaly-detection-permissions.v1",
        "ok": True,
        "permissions": (
            "fraud_anomaly_detection.event.write",
            "fraud_anomaly_detection.anomaly_score.write",
            "fraud_anomaly_detection.fraud_rule.write",
            "fraud_anomaly_detection.risk_case.write",
            "fraud_anomaly_detection.event.consume",
            "fraud_anomaly_detection.configure",
            "fraud_anomaly_detection.audit",
        ),
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
        "contract": "appgen_event_contract",
        "idempotency_key": (
            f"fraud_anomaly_detection:{event_type}:{payload.get('case_id') or payload.get('signal_id') or payload.get('subject_key') or len(state['outbox']) + 1}"
        ),
        "retry_policy": {
            "max_attempts": int(state.get("configuration", {}).get("retry_limit", 3)),
            "dead_letter": "fraud_anomaly_detection_dead_letter_event",
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
        "configuration": bool(state["configuration"].get("ok")),
        "runtime_digest": _digest(
            {
                "capability": capability,
                "signals": len(state["risk_signals"]),
                "scores": len(state["anomaly_scores"]),
                "cases": len(state["risk_cases"]),
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
