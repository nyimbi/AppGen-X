"""Executable configuration, parameter, and rule contract for the EAM PBC."""

from __future__ import annotations

import hashlib

from .runtime import EAM_ALLOWED_DATABASE_BACKENDS
from .runtime import EAM_EVENT_CONTRACT
from .runtime import EAM_FORBIDDEN_EVENTING_FIELDS
from .runtime import EAM_REQUIRED_CONFIGURATION_FIELDS
from .runtime import EAM_REQUIRED_EVENT_TOPIC
from .runtime import EAM_REQUIRED_RULE_FIELDS
from .runtime import EAM_SUPPORTED_PARAMETERS


PBC_KEY = "eam"
EAM_RULE_TYPES = ("maintenance", "strategy", "safety", "spares", "reliability", "vendor")
EAM_ALLOWED_WORK_TYPES = ("preventive", "predictive", "corrective", "calibration", "shutdown", "statutory")
EAM_ALLOWED_RULE_STATUSES = ("draft", "active", "inactive")

CONFIG_SCHEMA = (
    {"key": "database_backend", "required": True, "type": "string", "allowed": EAM_ALLOWED_DATABASE_BACKENDS},
    {"key": "event_topic", "required": True, "type": "string", "allowed": (EAM_REQUIRED_EVENT_TOPIC,)},
    {"key": "retry_limit", "required": True, "type": "integer", "min": 1, "max": 10},
    {"key": "allowed_sites", "required": True, "type": "tuple"},
    {"key": "allowed_priorities", "required": True, "type": "tuple"},
    {"key": "allowed_work_types", "required": True, "type": "tuple"},
    {"key": "allowed_permit_types", "required": True, "type": "tuple"},
    {"key": "default_timezone", "required": True, "type": "string"},
    {"key": "workbench_limit", "required": True, "type": "integer", "min": 1, "max": 500},
)

PARAMETER_SCHEMA = (
    {
        "key": "default_pm_interval_days",
        "type": "integer",
        "default": 30,
        "min": 1,
        "max": 3650,
        "scope": "planning",
        "label": "Default PM Interval",
    },
    {
        "key": "failure_risk_threshold",
        "type": "number",
        "default": 0.65,
        "min": 0.0,
        "max": 1.0,
        "scope": "reliability",
        "label": "Failure Risk Threshold",
    },
    {
        "key": "mttr_target_hours",
        "type": "number",
        "default": 6.0,
        "min": 0.1,
        "max": 720.0,
        "scope": "reliability",
        "label": "MTTR Target",
    },
    {
        "key": "criticality_weight",
        "type": "number",
        "default": 0.4,
        "min": 0.0,
        "max": 1.0,
        "scope": "prioritization",
        "label": "Criticality Weight",
    },
    {
        "key": "safety_risk_threshold",
        "type": "number",
        "default": 0.7,
        "min": 0.0,
        "max": 1.0,
        "scope": "safety",
        "label": "Safety Risk Threshold",
    },
    {
        "key": "retention_days",
        "type": "integer",
        "default": 365,
        "min": 1,
        "max": 3650,
        "scope": "operations",
        "label": "Evidence Retention Days",
    },
)

RULE_SCHEMA = (
    {
        "rule_id": "eam.asset_readiness_gate",
        "tenant": "tenant_alpha",
        "rule_type": "maintenance",
        "eligible_work_types": ("preventive", "predictive", "corrective"),
        "allowed_sites": ("plant_east", "plant_west"),
        "status": "active",
        "criticality_classes": ("A", "B", "C"),
        "condition": "asset_readiness_gate",
    },
    {
        "rule_id": "eam.plan_release_gate",
        "tenant": "tenant_alpha",
        "rule_type": "strategy",
        "eligible_work_types": ("preventive", "predictive", "calibration"),
        "allowed_sites": ("plant_east", "plant_west"),
        "status": "active",
        "condition": "plan_release_gate",
    },
    {
        "rule_id": "eam.permit_required_for_execution",
        "tenant": "tenant_alpha",
        "rule_type": "safety",
        "eligible_work_types": ("corrective", "shutdown", "statutory"),
        "allowed_sites": ("plant_east", "plant_west"),
        "status": "active",
        "condition": "permit_required_for_execution",
    },
    {
        "rule_id": "eam.spare_projection_freshness",
        "tenant": "tenant_alpha",
        "rule_type": "spares",
        "eligible_work_types": EAM_ALLOWED_WORK_TYPES,
        "allowed_sites": ("plant_east", "plant_west"),
        "status": "active",
        "condition": "projection_freshness",
    },
    {
        "rule_id": "eam.vendor_documentation_gate",
        "tenant": "tenant_alpha",
        "rule_type": "vendor",
        "eligible_work_types": ("shutdown", "statutory", "corrective"),
        "allowed_sites": ("plant_east", "plant_west"),
        "status": "active",
        "condition": "vendor_documentation_gate",
    },
)


def _parameter_index() -> dict[str, dict]:
    return {item["key"]: item for item in PARAMETER_SCHEMA}


def configuration_manifest():
    """Return required configuration keys, bounded parameters, and executable rules."""
    return {
        "ok": bool(CONFIG_SCHEMA) and len(PARAMETER_SCHEMA) == len(EAM_SUPPORTED_PARAMETERS) and bool(RULE_SCHEMA),
        "pbc": PBC_KEY,
        "schema": CONFIG_SCHEMA,
        "required_keys": required_keys(),
        "allowed_database_backends": EAM_ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": EAM_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "parameter_schema": PARAMETER_SCHEMA,
        "rule_schema": RULE_SCHEMA,
        "required_rule_fields": EAM_REQUIRED_RULE_FIELDS,
        "side_effects": (),
    }


def required_keys():
    """Return configuration keys that must be supplied by an installer."""
    return tuple(item["key"] for item in CONFIG_SCHEMA if item.get("required"))


def _default_configuration() -> dict:
    return {
        "database_backend": "postgresql",
        "event_topic": EAM_REQUIRED_EVENT_TOPIC,
        "retry_limit": 3,
        "allowed_sites": ("plant_east", "plant_west"),
        "allowed_priorities": ("low", "medium", "high", "critical"),
        "allowed_work_types": EAM_ALLOWED_WORK_TYPES,
        "allowed_permit_types": ("electrical", "confined_space", "hot_work", "isolation"),
        "default_timezone": "UTC",
        "workbench_limit": 100,
    }


def validate_configuration(values=None):
    """Validate supplied configuration values without reading process state."""
    supplied = {**_default_configuration(), **dict(values or {})}
    missing = tuple(key for key in required_keys() if supplied.get(key) in (None, "", ()))
    unknown = tuple(sorted(key for key in supplied if key not in {item["key"] for item in CONFIG_SCHEMA}))
    forbidden = tuple(field for field in EAM_FORBIDDEN_EVENTING_FIELDS if field in supplied)
    invalid = []
    for field in CONFIG_SCHEMA:
        key = field["key"]
        value = supplied.get(key)
        if key in ("database_backend", "event_topic") and value not in field["allowed"]:
            invalid.append((key, value))
        if field["type"] == "integer" and (not isinstance(value, int) or isinstance(value, bool)):
            invalid.append((key, value))
        if field["type"] == "tuple" and not isinstance(value, tuple):
            invalid.append((key, value))
        if field["type"] == "integer" and isinstance(value, int):
            if value < field.get("min", value) or value > field.get("max", value):
                invalid.append((key, value))
    return {
        "ok": not missing and not unknown and not forbidden and not invalid,
        "pbc": PBC_KEY,
        "missing": missing,
        "unknown": unknown,
        "forbidden": forbidden,
        "invalid": tuple(invalid),
        "required_keys": required_keys(),
        "event_contract": EAM_EVENT_CONTRACT,
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def parameter_manifest():
    """Return bounded runtime parameters understood by this PBC."""
    return {
        "ok": tuple(item["key"] for item in PARAMETER_SCHEMA) == EAM_SUPPORTED_PARAMETERS,
        "pbc": PBC_KEY,
        "parameters": PARAMETER_SCHEMA,
        "supported_parameters": EAM_SUPPORTED_PARAMETERS,
        "side_effects": (),
    }


def set_parameter(current_parameters=None, key="default_pm_interval_days", value=None):
    """Apply one bounded parameter change without mutating caller state."""
    schema = _parameter_index().get(key)
    if schema is None:
        return {"ok": False, "accepted": False, "reason": "unknown_parameter", "key": key, "side_effects": ()}
    candidate = schema["default"] if value is None else value
    if schema["type"] == "integer" and (not isinstance(candidate, int) or isinstance(candidate, bool)):
        return {"ok": False, "accepted": False, "reason": "invalid_type", "key": key, "side_effects": ()}
    if schema["type"] == "number" and (not isinstance(candidate, (int, float)) or isinstance(candidate, bool)):
        return {"ok": False, "accepted": False, "reason": "invalid_type", "key": key, "side_effects": ()}
    if float(candidate) < schema["min"] or float(candidate) > schema["max"]:
        return {"ok": False, "accepted": False, "reason": "out_of_bounds", "key": key, "side_effects": ()}
    updated = dict(current_parameters or {})
    updated[key] = candidate
    compiled_hash = hashlib.sha3_256(f"{PBC_KEY}:{key}:{candidate}".encode("utf-8")).hexdigest()
    return {
        "ok": True,
        "accepted": True,
        "pbc": PBC_KEY,
        "key": key,
        "value": candidate,
        "parameters": updated,
        "scope": schema["scope"],
        "compiled_hash": compiled_hash,
        "side_effects": (),
    }


def rule_manifest():
    """Return declarative maintenance rules supported by this PBC."""
    return {
        "ok": bool(RULE_SCHEMA),
        "pbc": PBC_KEY,
        "rules": RULE_SCHEMA,
        "required_fields": EAM_REQUIRED_RULE_FIELDS,
        "rule_types": EAM_RULE_TYPES,
        "allowed_statuses": EAM_ALLOWED_RULE_STATUSES,
        "side_effects": (),
    }


def compile_rule(rule):
    """Compile a rule into a deterministic side-effect-free rule contract."""
    candidate = dict(rule)
    if any(field in candidate for field in EAM_FORBIDDEN_EVENTING_FIELDS):
        return {"ok": False, "compiled": False, "reason": "stream_engine_picker_disallowed", "side_effects": ()}
    missing = tuple(field for field in EAM_REQUIRED_RULE_FIELDS if field not in candidate)
    if missing:
        return {"ok": False, "compiled": False, "reason": "missing_required_fields", "missing": missing, "side_effects": ()}
    if candidate.get("rule_type") not in EAM_RULE_TYPES:
        return {"ok": False, "compiled": False, "reason": "unknown_rule_type", "side_effects": ()}
    if candidate.get("status") not in EAM_ALLOWED_RULE_STATUSES:
        return {"ok": False, "compiled": False, "reason": "invalid_status", "side_effects": ()}
    eligible_work_types = tuple(candidate.get("eligible_work_types", ()))
    if not eligible_work_types or any(work_type not in EAM_ALLOWED_WORK_TYPES for work_type in eligible_work_types):
        return {"ok": False, "compiled": False, "reason": "invalid_work_types", "side_effects": ()}
    raw = f"{PBC_KEY}:{tuple(sorted(candidate.items(), key=lambda item: item[0]))}"
    compiled_hash = hashlib.sha3_256(raw.encode("utf-8")).hexdigest()
    return {
        "ok": True,
        "compiled": True,
        "pbc": PBC_KEY,
        "rule": candidate,
        "compiled_hash": compiled_hash,
        "compile_evidence": {
            "hash_algorithm": "sha3_256",
            "required_fields": EAM_REQUIRED_RULE_FIELDS,
            "required_event_topic": EAM_REQUIRED_EVENT_TOPIC,
            "event_contract": EAM_EVENT_CONTRACT,
        },
        "side_effects": (),
    }


def evaluate_rule(compiled_rule, context=None):
    """Evaluate one compiled rule against supplied context."""
    if not compiled_rule.get("compiled"):
        return {"ok": False, "allowed": False, "reason": "rule_not_compiled", "side_effects": ()}
    supplied = dict(context or {})
    rule = compiled_rule["rule"]
    allowed = True
    allowed = allowed and bool(supplied.get("tenant", rule["tenant"]))
    allowed = allowed and supplied.get("database_backend", "postgresql") in EAM_ALLOWED_DATABASE_BACKENDS
    allowed = allowed and supplied.get("event_contract", EAM_EVENT_CONTRACT) == EAM_EVENT_CONTRACT
    if supplied.get("site"):
        allowed = allowed and supplied["site"] in tuple(rule.get("allowed_sites", ()))
    if supplied.get("work_type"):
        allowed = allowed and supplied["work_type"] in tuple(rule.get("eligible_work_types", ()))
    if rule["rule_type"] == "safety":
        allowed = allowed and supplied.get("has_permit", True)
    if rule["rule_type"] == "spares":
        allowed = allowed and supplied.get("projection_fresh", True)
    if rule["rule_type"] == "vendor":
        allowed = allowed and supplied.get("vendor_acknowledged", True)
    return {
        "ok": True,
        "allowed": allowed,
        "pbc": PBC_KEY,
        "rule_id": rule.get("rule_id"),
        "rule_type": rule.get("rule_type"),
        "condition": rule.get("condition"),
        "scope": rule.get("scope", rule.get("rule_type")),
        "side_effects": (),
    }


def governance_smoke_test():
    """Exercise configuration, parameter, and domain rule behavior together."""
    configuration = validate_configuration()
    parameter = set_parameter({}, "default_pm_interval_days", 30)
    domain_parameter = set_parameter({}, "failure_risk_threshold", 0.65)
    compiled_rule = compile_rule(RULE_SCHEMA[0])
    rule_decision = evaluate_rule(
        compiled_rule,
        {
            "tenant": "tenant_alpha",
            "site": "plant_east",
            "work_type": "preventive",
            "database_backend": "postgresql",
            "event_contract": EAM_EVENT_CONTRACT,
        },
    )
    return {
        "ok": configuration["ok"] and parameter["ok"] and domain_parameter["ok"] and compiled_rule["ok"] and rule_decision["allowed"],
        "configuration": configuration,
        "parameter": parameter,
        "domain_parameter": domain_parameter,
        "compiled_rule": compiled_rule,
        "rule_decision": rule_decision,
        "side_effects": (),
    }


def smoke_test():
    """Exercise configuration, rules, and parameters using synthetic values."""
    governance = governance_smoke_test()
    return {
        **governance["configuration"],
        "ok": governance["ok"],
        "parameter": governance["parameter"],
        "domain_parameter": governance["domain_parameter"],
        "compiled_rule": governance["compiled_rule"],
        "rule_decision": governance["rule_decision"],
        "side_effects": (),
    }
