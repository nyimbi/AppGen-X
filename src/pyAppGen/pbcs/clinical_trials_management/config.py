"""Executable configuration, parameter, and rule contract for the clinical_trials_management PBC."""

from __future__ import annotations

import hashlib

from .runtime import CLINICAL_TRIALS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS
from .runtime import CLINICAL_TRIALS_MANAGEMENT_PARAMETER_SCHEMA
from .runtime import CLINICAL_TRIALS_MANAGEMENT_REQUIRED_EVENT_TOPIC
from .runtime import CLINICAL_TRIALS_MANAGEMENT_RULE_TYPES


PBC_KEY = "clinical_trials_management"
CONFIG_SCHEMA = (
    {"key": "CLINICAL_TRIALS_MANAGEMENT_DATABASE_URL", "required": True, "source": "environment"},
    {"key": "CLINICAL_TRIALS_MANAGEMENT_EVENT_TOPIC", "required": True, "source": "environment"},
    {"key": "CLINICAL_TRIALS_MANAGEMENT_DEFAULT_TIMEZONE", "required": True, "source": "environment"},
    {"key": "CLINICAL_TRIALS_MANAGEMENT_DEFAULT_JURISDICTION", "required": True, "source": "environment"},
    {"key": "CLINICAL_TRIALS_MANAGEMENT_ALLOWED_LANGUAGES", "required": False, "source": "environment"},
    {"key": "CLINICAL_TRIALS_MANAGEMENT_RETRY_LIMIT", "required": False, "source": "environment"},
    {"key": "CLINICAL_TRIALS_MANAGEMENT_WORKBENCH_LIMIT", "required": False, "source": "environment"},
)
RULE_SCHEMA = (
    {"rule_id": f"{PBC_KEY}.active_protocol_required", "condition": "active_protocol_required", "effect": "allow_when_true", "scope": "protocol_gate", "rule_type": "protocol_gate"},
    {"rule_id": f"{PBC_KEY}.site_activation_evidence_complete", "condition": "site_activation_evidence_complete", "effect": "allow_when_true", "scope": "site_activation", "rule_type": "site_activation"},
    {"rule_id": f"{PBC_KEY}.consent_version_matches_protocol", "condition": "consent_version_matches_protocol", "effect": "allow_when_true", "scope": "consent", "rule_type": "consent"},
    {"rule_id": f"{PBC_KEY}.eligibility_evidence_complete", "condition": "eligibility_evidence_complete", "effect": "allow_when_true", "scope": "eligibility", "rule_type": "eligibility"},
    {"rule_id": f"{PBC_KEY}.serious_event_reporting_within_sla", "condition": "serious_event_reporting_within_sla", "effect": "allow_when_true", "scope": "safety", "rule_type": "safety"},
    {"rule_id": f"{PBC_KEY}.subject_view_redaction_required", "condition": "subject_view_redaction_required", "effect": "allow_when_true", "scope": "privacy", "rule_type": "privacy"},
)


def configuration_manifest() -> dict:
    """Return configuration keys, bounded parameters, and executable rules."""
    return {
        "ok": bool(CONFIG_SCHEMA) and bool(CLINICAL_TRIALS_MANAGEMENT_PARAMETER_SCHEMA) and bool(RULE_SCHEMA),
        "pbc": PBC_KEY,
        "schema": CONFIG_SCHEMA,
        "required_keys": required_keys(),
        "allowed_database_backends": CLINICAL_TRIALS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": CLINICAL_TRIALS_MANAGEMENT_REQUIRED_EVENT_TOPIC,
        "parameter_schema": CLINICAL_TRIALS_MANAGEMENT_PARAMETER_SCHEMA,
        "rule_schema": RULE_SCHEMA,
        "side_effects": (),
    }


def required_keys() -> tuple[str, ...]:
    return tuple(item["key"] for item in CONFIG_SCHEMA if item.get("required"))


def validate_configuration(values: dict | None = None) -> dict:
    """Validate supplied configuration values without reading process state."""
    supplied = dict(
        values
        or {
            "CLINICAL_TRIALS_MANAGEMENT_DATABASE_URL": "postgresql://clinical-trials",
            "CLINICAL_TRIALS_MANAGEMENT_EVENT_TOPIC": CLINICAL_TRIALS_MANAGEMENT_REQUIRED_EVENT_TOPIC,
            "CLINICAL_TRIALS_MANAGEMENT_DEFAULT_TIMEZONE": "UTC",
            "CLINICAL_TRIALS_MANAGEMENT_DEFAULT_JURISDICTION": "US",
        }
    )
    missing = tuple(key for key in required_keys() if not supplied.get(key))
    known = {item["key"] for item in CONFIG_SCHEMA}
    unknown = tuple(sorted(key for key in supplied if key not in known))
    invalid_event_topic = supplied.get("CLINICAL_TRIALS_MANAGEMENT_EVENT_TOPIC") != CLINICAL_TRIALS_MANAGEMENT_REQUIRED_EVENT_TOPIC
    return {
        "ok": not missing and not unknown and not invalid_event_topic,
        "pbc": PBC_KEY,
        "missing": missing,
        "unknown": unknown,
        "invalid_event_topic": invalid_event_topic,
        "required_keys": required_keys(),
        "side_effects": (),
    }


def parameter_manifest() -> dict:
    return {
        "ok": bool(CLINICAL_TRIALS_MANAGEMENT_PARAMETER_SCHEMA),
        "pbc": PBC_KEY,
        "parameters": CLINICAL_TRIALS_MANAGEMENT_PARAMETER_SCHEMA,
        "side_effects": (),
    }


def set_parameter(current_parameters: dict | None = None, key: str = "workbench_limit", value=None) -> dict:
    """Apply one bounded parameter change without mutating caller state."""
    schema = next((item for item in CLINICAL_TRIALS_MANAGEMENT_PARAMETER_SCHEMA if item["name"] == key), None)
    if schema is None:
        return {"ok": False, "accepted": False, "reason": "unknown_parameter", "key": key, "side_effects": ()}
    candidate = schema["default"] if value is None else value
    if not isinstance(candidate, int) or isinstance(candidate, bool):
        return {"ok": False, "accepted": False, "reason": "invalid_type", "key": key, "side_effects": ()}
    if candidate < schema["min"] or candidate > schema["max"]:
        return {"ok": False, "accepted": False, "reason": "out_of_bounds", "key": key, "side_effects": ()}
    updated = dict(current_parameters or {})
    updated[key] = candidate
    return {
        "ok": True,
        "accepted": True,
        "pbc": PBC_KEY,
        "key": key,
        "value": candidate,
        "parameters": updated,
        "side_effects": (),
    }


def rule_manifest() -> dict:
    return {"ok": bool(RULE_SCHEMA), "pbc": PBC_KEY, "rules": RULE_SCHEMA, "side_effects": ()}


def compile_rule(rule: dict) -> dict:
    """Compile a rule into a deterministic side-effect-free rule contract."""
    candidate = dict(rule)
    if candidate.get("rule_type") not in CLINICAL_TRIALS_MANAGEMENT_RULE_TYPES:
        return {"ok": False, "compiled": False, "reason": "unknown_rule_type", "side_effects": ()}
    known_conditions = {item["condition"] for item in RULE_SCHEMA}
    if candidate.get("condition") not in known_conditions:
        return {"ok": False, "compiled": False, "reason": "unknown_condition", "side_effects": ()}
    compiled_hash = hashlib.sha256(f"{PBC_KEY}:{tuple(sorted(candidate.items()))}".encode("utf-8")).hexdigest()
    return {
        "ok": True,
        "compiled": True,
        "pbc": PBC_KEY,
        "rule": candidate,
        "compiled_hash": compiled_hash,
        "side_effects": (),
    }


def evaluate_rule(compiled_rule: dict, context: dict | None = None) -> dict:
    """Evaluate one compiled rule against supplied context."""
    if not compiled_rule.get("compiled"):
        return {"ok": False, "allowed": False, "reason": "rule_not_compiled", "side_effects": ()}
    supplied = dict(context or {})
    condition = compiled_rule["rule"]["condition"]
    if condition == "active_protocol_required":
        allowed = supplied.get("protocol_status") == "active"
    elif condition == "site_activation_evidence_complete":
        allowed = all(bool(supplied.get(key)) for key in ("ethics_approval", "contract_executed", "training_complete", "delegation_log_ready"))
    elif condition == "consent_version_matches_protocol":
        allowed = supplied.get("consent_version") == supplied.get("protocol_version")
    elif condition == "eligibility_evidence_complete":
        allowed = bool(supplied.get("eligibility_evidence_complete")) and bool(supplied.get("exclusion_clear"))
    elif condition == "serious_event_reporting_within_sla":
        allowed = supplied.get("reported_within_hours", 0) <= supplied.get("serious_event_reporting_hours", 24)
    elif condition == "subject_view_redaction_required":
        allowed = supplied.get("view_mode", "redacted") == "redacted"
    else:
        allowed = False
    return {
        "ok": True,
        "allowed": allowed,
        "pbc": PBC_KEY,
        "rule_id": compiled_rule["rule"].get("rule_id"),
        "condition": condition,
        "scope": compiled_rule["rule"].get("scope"),
        "side_effects": (),
    }


def governance_smoke_test() -> dict:
    configuration = validate_configuration()
    parameter = set_parameter({}, "serious_event_reporting_hours", 24)
    compiled_rule = compile_rule(RULE_SCHEMA[0])
    rule_decision = evaluate_rule(compiled_rule, {"protocol_status": "active"})
    return {
        "ok": configuration["ok"] and parameter["ok"] and compiled_rule["ok"] and rule_decision["ok"] and rule_decision["allowed"],
        "configuration": configuration,
        "parameter": parameter,
        "compiled_rule": compiled_rule,
        "rule_decision": rule_decision,
        "side_effects": (),
    }


def smoke_test() -> dict:
    return governance_smoke_test()
