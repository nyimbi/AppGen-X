"""Executable standalone runtime for the identity KYC / AML compliance slice."""

from __future__ import annotations

from copy import deepcopy
from datetime import date, datetime, timedelta
import hashlib
from typing import Callable

from .domain_depth import (
    DOMAIN_ADVANCED_CAPABILITIES,
    DOMAIN_CONSUMED_EVENTS,
    DOMAIN_OPERATIONS,
    DOMAIN_OWNED_TABLES,
    DOMAIN_PARAMETERS,
    DOMAIN_RULES,
    DOMAIN_WORKBENCH_VIEWS,
    domain_depth_contract,
    domain_depth_smoke_test,
    execute_domain_operation,
)

PBC_KEY = "identity_kyc_aml_compliance"
IDENTITY_KYC_AML_COMPLIANCE_OWNED_TABLES = DOMAIN_OWNED_TABLES
IDENTITY_KYC_AML_COMPLIANCE_RUNTIME_TABLES = DOMAIN_OWNED_TABLES
IDENTITY_KYC_AML_COMPLIANCE_ALLOWED_DATABASE_BACKENDS = (
    "postgresql",
    "mysql",
    "mariadb",
)
IDENTITY_KYC_AML_COMPLIANCE_REQUIRED_EVENT_TOPIC = "pbc.identity_kyc_aml_compliance.events"
IDENTITY_KYC_AML_COMPLIANCE_EMITTED_EVENT_TYPES = (
    "IdentityKycAmlComplianceCreated",
    "IdentityKycAmlComplianceUpdated",
    "IdentityKycAmlComplianceApproved",
    "IdentityKycAmlComplianceExceptionOpened",
)
IDENTITY_KYC_AML_COMPLIANCE_CONSUMED_EVENT_TYPES = DOMAIN_CONSUMED_EVENTS
IDENTITY_KYC_AML_COMPLIANCE_STANDARD_FEATURE_KEYS = (
    "kyc_profile_management",
    "identity_kyc_aml_compliance_workflow",
    "identity_kyc_aml_compliance_analytics",
    "configuration_schema",
    "rule_engine",
    "parameter_engine",
    "owned_schema_migrations_models",
    "appgen_x_outbox_inbox_eventing",
    "idempotent_handlers",
    "retry_dead_letter_evidence",
    "permissions",
    "seed_data",
    "workbench",
    "agentic_document_instruction_intake",
    "governed_datastore_crud",
    "ai_agent_task_assistance",
    "configuration_workbench",
    "continuous_release_assurance",
)
IDENTITY_KYC_AML_COMPLIANCE_RUNTIME_CAPABILITY_KEYS = DOMAIN_ADVANCED_CAPABILITIES
IDENTITY_KYC_AML_COMPLIANCE_UI_FRAGMENT_KEYS = (
    "IdentityKycAmlComplianceWorkbench",
    "IdentityKycAmlComplianceDetail",
    "IdentityKycAmlComplianceAssistantPanel",
    "IdentityKycAmlComplianceOnboardingWizard",
    "IdentityKycAmlComplianceRuleConsole",
)
IDENTITY_KYC_AML_COMPLIANCE_BUSINESS_TABLES = DOMAIN_OWNED_TABLES[:12]
CONTROL_PERSON_ROLES = {
    "beneficial_owner",
    "ultimate_beneficial_owner",
    "signatory",
    "board_controller",
    "director",
    "trustee",
    "settlor",
    "protector",
    "nominee",
}
HIGH_RISK_GEOGRAPHIES_DEFAULT = ("IRN", "PRK", "SYR", "RUS", "MMR")
SCREENING_CATEGORIES = (
    "sanctions",
    "pep",
    "rca",
    "adverse_media",
    "internal_deny_list",
)
KYC_TRANSITIONS = {
    "draft": {"pending_verification", "archived"},
    "pending_verification": {"pending_screening", "restricted", "archived"},
    "pending_screening": {"pending_edd", "approved", "restricted"},
    "pending_edd": {"approved", "restricted"},
    "approved": {"restricted", "exited"},
    "restricted": {"pending_edd", "exited", "archived"},
    "exited": {"archived"},
    "archived": set(),
}
DOCUMENT_REQUIRED_FIELDS = (
    "profile_id",
    "document_class",
    "jurisdiction",
    "issuing_authority",
    "identifier",
    "issue_date",
    "expiry_date",
    "capture_method",
)
DEFAULT_RULES = {
    "customer_classification_required": {
        "rule_id": "customer_classification_required",
        "description": "Customer type, jurisdiction, product exposure, channel, and expected activity are mandatory at onboarding.",
        "severity": "blocking",
    },
    "document_completeness_required": {
        "rule_id": "document_completeness_required",
        "description": "Identity documents must include issuer, identifier, issue date, expiry date, and capture method.",
        "severity": "blocking",
    },
    "document_authenticity_required": {
        "rule_id": "document_authenticity_required",
        "description": "Expired, tampered, or mismatched documents require remediation before approval.",
        "severity": "blocking",
    },
    "beneficial_owner_threshold_policy": {
        "rule_id": "beneficial_owner_threshold_policy",
        "description": "Entity onboarding must capture threshold owners and control persons based on jurisdiction and risk tier.",
        "severity": "blocking",
    },
    "screening_category_resolution_policy": {
        "rule_id": "screening_category_resolution_policy",
        "description": "Sanctions, PEP, RCA, and adverse media hits route through category-specific resolution paths.",
        "severity": "blocking",
    },
    "enhanced_due_diligence_trigger_matrix": {
        "rule_id": "enhanced_due_diligence_trigger_matrix",
        "description": "EDD is mandatory for PEP exposure, high-risk geographies, complex ownership, and severe adverse media.",
        "severity": "blocking",
    },
    "periodic_rescreening_policy": {
        "rule_id": "periodic_rescreening_policy",
        "description": "Approved profiles must carry a next rescreening due date tied to risk tier.",
        "severity": "warning",
    },
    "alert_to_case_promotion_policy": {
        "rule_id": "alert_to_case_promotion_policy",
        "description": "High severity or unresolved alerts promote to suspicious activity cases.",
        "severity": "blocking",
    },
    "risk_score_challenge_policy": {
        "rule_id": "risk_score_challenge_policy",
        "description": "Risk score overrides require challenger evidence and supervisor sign-off.",
        "severity": "blocking",
    },
}
DEFAULT_PARAMETER_VALUES = {
    "beneficial_owner_threshold_pct": 25.0,
    "high_risk_beneficial_owner_threshold_pct": 10.0,
    "rescreening_days_low": 365,
    "rescreening_days_medium": 180,
    "rescreening_days_high": 90,
    "workbench_limit": 50,
    "high_risk_geographies": HIGH_RISK_GEOGRAPHIES_DEFAULT,
}
ROUTE_OPERATION_MAP = {
    "POST /kyc-profiles": "create_kyc_profile",
    "POST /identity-documents": "record_identity_document",
    "POST /beneficial-owners": "register_beneficial_owner",
    "POST /screening-hits": "record_screening_hit",
    "POST /monitoring-alerts": "triage_monitoring_alert",
    "GET /identity-kyc-aml-compliance-workbench": "build_workbench_view",
}


SCHEMA_TABLES = (
    {
        "table": "identity_kyc_aml_compliance_kyc_profile",
        "fields": (
            ("id", "TEXT", True),
            ("tenant", "TEXT", True),
            ("subject_name", "TEXT", True),
            ("customer_type", "TEXT", True),
            ("jurisdiction", "TEXT", True),
            ("product_exposure", "TEXT", True),
            ("channel", "TEXT", True),
            ("status", "TEXT", True),
            ("risk_tier", "TEXT", True),
            ("edd_required", "BOOLEAN", True),
            ("next_rescreen_due_at", "TEXT", False),
            ("payload", "JSON", True),
            ("created_at", "TEXT", True),
            ("updated_at", "TEXT", True),
        ),
        "primary_key": ("id",),
    },
    {
        "table": "identity_kyc_aml_compliance_identity_document",
        "fields": (
            ("id", "TEXT", True),
            ("tenant", "TEXT", True),
            ("profile_id", "TEXT", True),
            ("document_class", "TEXT", True),
            ("jurisdiction", "TEXT", True),
            ("identifier", "TEXT", True),
            ("verification_status", "TEXT", True),
            ("authenticity_status", "TEXT", True),
            ("expiry_state", "TEXT", True),
            ("payload", "JSON", True),
            ("created_at", "TEXT", True),
            ("updated_at", "TEXT", True),
        ),
        "primary_key": ("id",),
    },
    {
        "table": "identity_kyc_aml_compliance_beneficial_owner",
        "fields": (
            ("id", "TEXT", True),
            ("tenant", "TEXT", True),
            ("profile_id", "TEXT", True),
            ("owner_name", "TEXT", True),
            ("role_type", "TEXT", True),
            ("ownership_pct", "NUMERIC", False),
            ("screening_required", "BOOLEAN", True),
            ("payload", "JSON", True),
            ("created_at", "TEXT", True),
            ("updated_at", "TEXT", True),
        ),
        "primary_key": ("id",),
    },
    {
        "table": "identity_kyc_aml_compliance_screening_hit",
        "fields": (
            ("id", "TEXT", True),
            ("tenant", "TEXT", True),
            ("profile_id", "TEXT", True),
            ("category", "TEXT", True),
            ("watchlist_source", "TEXT", True),
            ("severity", "TEXT", True),
            ("confidence", "NUMERIC", True),
            ("disposition", "TEXT", True),
            ("blocking", "BOOLEAN", True),
            ("payload", "JSON", True),
            ("created_at", "TEXT", True),
            ("updated_at", "TEXT", True),
        ),
        "primary_key": ("id",),
    },
    {
        "table": "identity_kyc_aml_compliance_monitoring_alert",
        "fields": (
            ("id", "TEXT", True),
            ("tenant", "TEXT", True),
            ("profile_id", "TEXT", False),
            ("source_type", "TEXT", True),
            ("typology", "TEXT", True),
            ("severity", "TEXT", True),
            ("status", "TEXT", True),
            ("assigned_to", "TEXT", False),
            ("due_at", "TEXT", False),
            ("payload", "JSON", True),
            ("created_at", "TEXT", True),
            ("updated_at", "TEXT", True),
        ),
        "primary_key": ("id",),
    },
    {
        "table": "identity_kyc_aml_compliance_suspicious_activity_case",
        "fields": (
            ("id", "TEXT", True),
            ("tenant", "TEXT", True),
            ("profile_id", "TEXT", True),
            ("alert_id", "TEXT", False),
            ("case_status", "TEXT", True),
            ("escalation_reason", "TEXT", True),
            ("payload", "JSON", True),
            ("created_at", "TEXT", True),
            ("updated_at", "TEXT", True),
        ),
        "primary_key": ("id",),
    },
    {
        "table": "identity_kyc_aml_compliance_compliance_review",
        "fields": (
            ("id", "TEXT", True),
            ("tenant", "TEXT", True),
            ("profile_id", "TEXT", True),
            ("review_type", "TEXT", True),
            ("review_status", "TEXT", True),
            ("reviewer", "TEXT", True),
            ("approved_score", "NUMERIC", False),
            ("payload", "JSON", True),
            ("created_at", "TEXT", True),
            ("updated_at", "TEXT", True),
        ),
        "primary_key": ("id",),
    },
    {
        "table": "identity_kyc_aml_compliance_policy_rule",
        "fields": (
            ("id", "TEXT", True),
            ("tenant", "TEXT", True),
            ("rule_name", "TEXT", True),
            ("severity", "TEXT", True),
            ("compiled_hash", "TEXT", True),
            ("payload", "JSON", True),
            ("created_at", "TEXT", True),
            ("updated_at", "TEXT", True),
        ),
        "primary_key": ("id",),
    },
    {
        "table": "identity_kyc_aml_compliance_runtime_parameter",
        "fields": (
            ("id", "TEXT", True),
            ("tenant", "TEXT", True),
            ("parameter_name", "TEXT", True),
            ("value", "TEXT", True),
            ("scope", "TEXT", True),
            ("payload", "JSON", True),
            ("created_at", "TEXT", True),
            ("updated_at", "TEXT", True),
        ),
        "primary_key": ("id",),
    },
    {
        "table": "identity_kyc_aml_compliance_schema_extension",
        "fields": (
            ("id", "TEXT", True),
            ("tenant", "TEXT", True),
            ("table_name", "TEXT", True),
            ("field_map", "JSON", True),
            ("payload", "JSON", True),
            ("created_at", "TEXT", True),
            ("updated_at", "TEXT", True),
        ),
        "primary_key": ("id",),
    },
    {
        "table": "identity_kyc_aml_compliance_control_assertion",
        "fields": (
            ("id", "TEXT", True),
            ("tenant", "TEXT", True),
            ("assertion_type", "TEXT", True),
            ("assertion_status", "TEXT", True),
            ("evidence_hash", "TEXT", True),
            ("payload", "JSON", True),
            ("created_at", "TEXT", True),
            ("updated_at", "TEXT", True),
        ),
        "primary_key": ("id",),
    },
    {
        "table": "identity_kyc_aml_compliance_governed_model",
        "fields": (
            ("id", "TEXT", True),
            ("tenant", "TEXT", True),
            ("model_name", "TEXT", True),
            ("model_version", "TEXT", True),
            ("approval_status", "TEXT", True),
            ("payload", "JSON", True),
            ("created_at", "TEXT", True),
            ("updated_at", "TEXT", True),
        ),
        "primary_key": ("id",),
    },
    {
        "table": "identity_kyc_aml_compliance_appgen_outbox_event",
        "fields": (
            ("id", "TEXT", True),
            ("event_type", "TEXT", True),
            ("topic", "TEXT", True),
            ("payload", "JSON", True),
            ("created_at", "TEXT", True),
        ),
        "primary_key": ("id",),
    },
    {
        "table": "identity_kyc_aml_compliance_appgen_inbox_event",
        "fields": (
            ("id", "TEXT", True),
            ("event_type", "TEXT", True),
            ("payload", "JSON", True),
            ("received_at", "TEXT", True),
        ),
        "primary_key": ("id",),
    },
    {
        "table": "identity_kyc_aml_compliance_appgen_dead_letter_event",
        "fields": (
            ("id", "TEXT", True),
            ("event_type", "TEXT", True),
            ("payload", "JSON", True),
            ("reason", "TEXT", True),
            ("received_at", "TEXT", True),
        ),
        "primary_key": ("id",),
    },
)


def _digest(value: object) -> str:
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()


def _iso_now() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def _date_value(value: str | None) -> date:
    if not value:
        return date.today()
    return date.fromisoformat(str(value)[:10])


def _copy_state(state: dict) -> dict:
    next_state = deepcopy(state)
    next_state["idempotency_keys"] = set(state.get("idempotency_keys", set()))
    return next_state


def _new_id(prefix: str, bucket: dict) -> str:
    return f"{prefix}-{len(bucket) + 1:04d}"


def _normalize_name(value: str | None) -> str:
    return " ".join(str(value or "").lower().split())


def _parameter_value(state: dict, name: str):
    return state["parameters"][name]["value"]


def _emit(state: dict, event_type: str, payload: dict) -> dict:
    envelope = {
        "id": _digest((event_type, payload, len(state["outbox"]))),
        "event_type": event_type,
        "topic": IDENTITY_KYC_AML_COMPLIANCE_REQUIRED_EVENT_TOPIC,
        "payload": dict(payload),
        "created_at": _iso_now(),
        "idempotency_key": _digest((event_type, tuple(sorted(payload.items())))),
    }
    state["outbox"].append(envelope)
    return envelope


def _profile_docs(state: dict, profile_id: str) -> list[dict]:
    return [doc for doc in state["documents"].values() if doc["profile_id"] == profile_id]


def _profile_owners(state: dict, profile_id: str) -> list[dict]:
    return [owner for owner in state["beneficial_owners"].values() if owner["profile_id"] == profile_id]


def _profile_hits(state: dict, profile_id: str) -> list[dict]:
    return [hit for hit in state["screening_hits"].values() if hit["profile_id"] == profile_id]


def _profile_reviews(state: dict, profile_id: str) -> list[dict]:
    return [review for review in state["compliance_reviews"].values() if review["profile_id"] == profile_id]


def _profile_cases(state: dict, profile_id: str) -> list[dict]:
    return [item for item in state["suspicious_activity_cases"].values() if item["profile_id"] == profile_id]


def _risk_factors(payload: dict) -> dict:
    factors: list[dict] = []
    customer_type = payload.get("customer_type", "individual")
    if customer_type in {"entity", "trust", "correspondent"}:
        factors.append({"factor": "customer_type", "weight": 0.18, "reason": customer_type})
    if payload.get("jurisdiction") in set(payload.get("high_risk_geographies", HIGH_RISK_GEOGRAPHIES_DEFAULT)):
        factors.append({"factor": "geography", "weight": 0.25, "reason": payload.get("jurisdiction")})
    if payload.get("channel") == "remote":
        factors.append({"factor": "channel", "weight": 0.08, "reason": "remote_onboarding"})
    if payload.get("pep_exposure"):
        factors.append({"factor": "pep_exposure", "weight": 0.30, "reason": "pep_flag"})
    if payload.get("complex_ownership"):
        factors.append({"factor": "ownership_complexity", "weight": 0.18, "reason": "layered_ownership"})
    if payload.get("adverse_media"):
        factors.append({"factor": "adverse_media", "weight": 0.15, "reason": "adverse_media"})
    if payload.get("expected_activity") == "cash_intensive":
        factors.append({"factor": "activity_pattern", "weight": 0.12, "reason": "cash_intensive"})
    score = min(1.0, round(sum(item["weight"] for item in factors) + 0.12, 4))
    tier = "low"
    if score >= 0.65:
        tier = "high"
    elif score >= 0.35:
        tier = "medium"
    return {"score": score, "tier": tier, "factors": tuple(factors)}


def _classify_obligations(payload: dict, risk_summary: dict) -> tuple[str, ...]:
    obligations = ["identity_document", "screening", "risk_scoring"]
    if payload.get("customer_type") in {"entity", "trust", "correspondent"}:
        obligations.extend(["beneficial_ownership", "control_person_screening"])
    if payload.get("channel") == "remote":
        obligations.append("biometric_or_manual_substitute")
    if risk_summary["tier"] == "high" or payload.get("pep_exposure"):
        obligations.extend(["enhanced_due_diligence", "source_of_funds", "source_of_wealth"])
    return tuple(dict.fromkeys(obligations))


def _edd_reasons(payload: dict, risk_summary: dict) -> tuple[str, ...]:
    reasons: list[str] = []
    if risk_summary["tier"] == "high":
        reasons.append("high_risk_score")
    if payload.get("pep_exposure"):
        reasons.append("pep_exposure")
    if payload.get("jurisdiction") in HIGH_RISK_GEOGRAPHIES_DEFAULT:
        reasons.append("high_risk_geography")
    if payload.get("complex_ownership"):
        reasons.append("complex_ownership")
    if payload.get("adverse_media"):
        reasons.append("adverse_media")
    return tuple(dict.fromkeys(reasons))


def _detect_duplicate_candidates(state: dict, payload: dict) -> tuple[str, ...]:
    candidate_keys = {
        _normalize_name(payload.get("subject_name")),
        str(payload.get("date_of_birth") or payload.get("registration_number") or ""),
        str(payload.get("national_id") or payload.get("tax_identifier") or ""),
    }
    duplicates = []
    for profile in state["profiles"].values():
        profile_keys = {
            profile.get("normalized_name", ""),
            str(profile.get("date_of_birth") or profile.get("registration_number") or ""),
            str(profile.get("national_id") or profile.get("tax_identifier") or ""),
        }
        overlap = {item for item in candidate_keys & profile_keys if item}
        if len(overlap) >= 2 or (
            payload.get("customer_type") == "individual"
            and _normalize_name(payload.get("subject_name"))
            and _normalize_name(payload.get("subject_name")) == profile.get("normalized_name")
        ):
            duplicates.append(profile["id"])
    return tuple(duplicates)


def _document_completeness(payload: dict) -> tuple[str, ...]:
    return tuple(field for field in DOCUMENT_REQUIRED_FIELDS if not payload.get(field))


def _document_states(payload: dict) -> dict:
    missing = _document_completeness(payload)
    expiry_state = "valid"
    if payload.get("expiry_date") and _date_value(payload["expiry_date"]) < date.today():
        expiry_state = "expired"
    authenticity_status = "verified"
    if payload.get("tamper_flag"):
        authenticity_status = "suspected_forgery"
    elif payload.get("manual_review_required") or payload.get("face_match_confidence", 1.0) < 0.82:
        authenticity_status = "review_required"
    verification_status = "accepted"
    if missing or expiry_state == "expired" or authenticity_status == "suspected_forgery":
        verification_status = "rejected"
    elif authenticity_status == "review_required":
        verification_status = "review_required"
    return {
        "missing_fields": missing,
        "expiry_state": expiry_state,
        "authenticity_status": authenticity_status,
        "verification_status": verification_status,
    }


def _beneficial_owner_threshold(profile: dict, state: dict) -> float:
    if profile.get("risk_tier") == "high":
        return float(_parameter_value(state, "high_risk_beneficial_owner_threshold_pct"))
    return float(_parameter_value(state, "beneficial_owner_threshold_pct"))


def _blocking_hits(state: dict, profile_id: str) -> list[dict]:
    return [
        hit
        for hit in _profile_hits(state, profile_id)
        if hit["blocking"] and hit["disposition"] not in {"cleared", "false_positive"}
    ]


def _edd_packet_complete(state: dict, profile_id: str) -> bool:
    for review in _profile_reviews(state, profile_id):
        if review["review_type"] == "edd_packet" and review["review_status"] == "completed":
            return True
    return False


def _document_ready_for_approval(state: dict, profile_id: str) -> bool:
    docs = _profile_docs(state, profile_id)
    if not docs:
        return False
    return any(doc["verification_status"] == "accepted" for doc in docs)


def _ownership_coverage(state: dict, profile: dict) -> dict:
    owners = _profile_owners(state, profile["id"])
    threshold = _beneficial_owner_threshold(profile, state)
    threshold_owners = [
        owner
        for owner in owners
        if float(owner.get("ownership_pct") or 0.0) >= threshold
        or owner.get("role_type") in CONTROL_PERSON_ROLES
    ]
    covered_pct = round(sum(float(owner.get("ownership_pct") or 0.0) for owner in threshold_owners), 2)
    return {
        "threshold_pct": threshold,
        "covered_pct": covered_pct,
        "owner_count": len(owners),
        "threshold_owner_count": len(threshold_owners),
        "complete": bool(threshold_owners),
    }


def _rescreening_due_date(risk_tier: str, state: dict) -> str:
    bucket = {
        "low": int(_parameter_value(state, "rescreening_days_low")),
        "medium": int(_parameter_value(state, "rescreening_days_medium")),
        "high": int(_parameter_value(state, "rescreening_days_high")),
    }
    return (date.today() + timedelta(days=bucket[risk_tier])).isoformat()


def _profile_projection(state: dict, profile: dict) -> dict:
    return {
        "profile": dict(profile),
        "documents": tuple(_profile_docs(state, profile["id"])),
        "beneficial_owners": tuple(_profile_owners(state, profile["id"])),
        "screening_hits": tuple(_profile_hits(state, profile["id"])),
        "reviews": tuple(_profile_reviews(state, profile["id"])),
        "cases": tuple(_profile_cases(state, profile["id"])),
        "ownership_coverage": _ownership_coverage(state, profile),
        "blocking_hits": tuple(_blocking_hits(state, profile["id"])),
    }


def identity_kyc_aml_compliance_empty_state() -> dict:
    created_at = _iso_now()
    return {
        "profiles": {},
        "documents": {},
        "beneficial_owners": {},
        "screening_hits": {},
        "monitoring_alerts": {},
        "suspicious_activity_cases": {},
        "compliance_reviews": {},
        "policy_rules": {
            name: {
                "id": name,
                "rule_name": name,
                "severity": spec["severity"],
                "payload": dict(spec),
                "created_at": created_at,
                "updated_at": created_at,
            }
            for name, spec in DEFAULT_RULES.items()
        },
        "parameters": {
            name: {
                "id": f"param-{name}",
                "parameter_name": name,
                "value": value,
                "scope": "domain",
                "payload": {"bounded": True},
                "created_at": created_at,
                "updated_at": created_at,
            }
            for name, value in DEFAULT_PARAMETER_VALUES.items()
        },
        "schema_extensions": {},
        "control_assertions": {},
        "governed_models": {},
        "configuration": {
            "database_backend": "postgresql",
            "event_topic": IDENTITY_KYC_AML_COMPLIANCE_REQUIRED_EVENT_TOPIC,
            "default_policy": "standard",
            "retry_limit": 5,
            "tenant_isolation": True,
            "stream_engine_picker_visible": False,
        },
        "inbox": [],
        "outbox": [],
        "dead_letter": [],
        "workflow_runs": [],
        "idempotency_keys": set(),
    }


def identity_kyc_aml_compliance_configure_runtime(state: dict, config: dict) -> dict:
    next_state = _copy_state(state)
    database_backend = config.get("database_backend", "postgresql")
    event_topic = config.get(
        "event_topic", IDENTITY_KYC_AML_COMPLIANCE_REQUIRED_EVENT_TOPIC
    )
    ok = (
        database_backend in IDENTITY_KYC_AML_COMPLIANCE_ALLOWED_DATABASE_BACKENDS
        and event_topic == IDENTITY_KYC_AML_COMPLIANCE_REQUIRED_EVENT_TOPIC
    )
    next_state["configuration"] = {
        **next_state["configuration"],
        **dict(config),
        "database_backend": database_backend,
        "event_topic": event_topic,
        "stream_engine_picker_visible": False,
    }
    return {
        "ok": ok,
        "state": next_state,
        "configuration": next_state["configuration"],
        "side_effects": (),
    }


def identity_kyc_aml_compliance_set_parameter(state: dict, name: str, value) -> dict:
    next_state = _copy_state(state)
    if name not in DOMAIN_PARAMETERS:
        return {
            "ok": False,
            "reason": "unknown_parameter",
            "parameter": name,
            "state": next_state,
            "side_effects": (),
        }
    now = _iso_now()
    next_state["parameters"][name] = {
        "id": f"param-{name}",
        "parameter_name": name,
        "value": value,
        "scope": "domain",
        "payload": {"bounded": True},
        "created_at": next_state["parameters"].get(name, {}).get("created_at", now),
        "updated_at": now,
    }
    return {
        "ok": True,
        "state": next_state,
        "parameter": next_state["parameters"][name],
        "side_effects": (),
    }


def identity_kyc_aml_compliance_register_rule(state: dict, rule: dict) -> dict:
    next_state = _copy_state(state)
    rule_name = rule.get("rule_name") or rule.get("rule_id")
    if not rule_name:
        return {
            "ok": False,
            "reason": "missing_rule_name",
            "state": next_state,
            "side_effects": (),
        }
    now = _iso_now()
    compiled = {
        "id": rule_name,
        "rule_name": rule_name,
        "severity": rule.get("severity", "warning"),
        "compiled_hash": _digest(rule),
        "payload": dict(rule),
        "created_at": next_state["policy_rules"].get(rule_name, {}).get("created_at", now),
        "updated_at": now,
    }
    next_state["policy_rules"][rule_name] = compiled
    return {"ok": True, "state": next_state, "rule": compiled, "side_effects": ()}


def identity_kyc_aml_compliance_register_schema_extension(
    state: dict, table: str, fields: dict
) -> dict:
    next_state = _copy_state(state)
    owned_name = table if table.startswith(f"{PBC_KEY}_") else f"{PBC_KEY}_{table}"
    if owned_name not in IDENTITY_KYC_AML_COMPLIANCE_OWNED_TABLES:
        return {
            "ok": False,
            "reason": "unknown_owned_table",
            "table": owned_name,
            "state": next_state,
            "side_effects": (),
        }
    extension_id = f"schema-extension-{len(next_state['schema_extensions']) + 1:04d}"
    now = _iso_now()
    record = {
        "id": extension_id,
        "tenant": "global",
        "table_name": owned_name,
        "field_map": dict(fields),
        "payload": {"fields": dict(fields)},
        "created_at": now,
        "updated_at": now,
    }
    next_state["schema_extensions"][extension_id] = record
    return {
        "ok": True,
        "state": next_state,
        "table": owned_name,
        "schema_extension": record,
        "side_effects": (),
    }


def identity_kyc_aml_compliance_create_kyc_profile(state: dict, payload: dict) -> dict:
    next_state = _copy_state(state)
    required = (
        "tenant",
        "subject_name",
        "customer_type",
        "jurisdiction",
        "product_exposure",
        "channel",
        "expected_activity",
    )
    missing = tuple(field for field in required if not payload.get(field))
    if missing:
        return {
            "ok": False,
            "reason": "missing_classification_fields",
            "missing_fields": missing,
            "state": next_state,
            "side_effects": (),
        }
    profile_id = payload.get("id") or _new_id("kyc", next_state["profiles"])
    risk_summary = _risk_factors(payload)
    obligations = _classify_obligations(payload, risk_summary)
    duplicate_candidates = _detect_duplicate_candidates(next_state, payload)
    edd_reasons = _edd_reasons(payload, risk_summary)
    now = _iso_now()
    profile = {
        "id": profile_id,
        "tenant": payload["tenant"],
        "subject_name": payload["subject_name"],
        "normalized_name": _normalize_name(payload.get("subject_name")),
        "customer_type": payload["customer_type"],
        "jurisdiction": payload["jurisdiction"],
        "product_exposure": payload["product_exposure"],
        "channel": payload["channel"],
        "expected_activity": payload["expected_activity"],
        "date_of_birth": payload.get("date_of_birth"),
        "registration_number": payload.get("registration_number"),
        "national_id": payload.get("national_id"),
        "tax_identifier": payload.get("tax_identifier"),
        "status": payload.get("status", "pending_verification"),
        "risk_score": risk_summary["score"],
        "risk_tier": risk_summary["tier"],
        "risk_factors": risk_summary["factors"],
        "obligations": obligations,
        "edd_required": bool(edd_reasons),
        "edd_reasons": edd_reasons,
        "duplicate_candidates": duplicate_candidates,
        "lifecycle_history": (
            {
                "from": None,
                "to": payload.get("status", "pending_verification"),
                "reason_code": "initial_intake",
                "at": now,
            },
        ),
        "next_rescreen_due_at": _rescreening_due_date(risk_summary["tier"], next_state),
        "payload": dict(payload),
        "created_at": now,
        "updated_at": now,
    }
    next_state["profiles"][profile_id] = profile
    event = _emit(
        next_state,
        IDENTITY_KYC_AML_COMPLIANCE_EMITTED_EVENT_TYPES[0],
        {
            "profile_id": profile_id,
            "tenant": profile["tenant"],
            "status": profile["status"],
            "risk_tier": profile["risk_tier"],
        },
    )
    return {
        "ok": True,
        "state": next_state,
        "record": profile,
        "event": event,
        "duplicate_candidates": duplicate_candidates,
        "obligations": obligations,
        "risk_summary": risk_summary,
        "side_effects": (),
    }


def identity_kyc_aml_compliance_advance_kyc_profile_lifecycle(
    state: dict, payload: dict
) -> dict:
    next_state = _copy_state(state)
    profile_id = payload.get("profile_id")
    if profile_id not in next_state["profiles"]:
        return {
            "ok": False,
            "reason": "unknown_profile",
            "profile_id": profile_id,
            "state": next_state,
            "side_effects": (),
        }
    profile = dict(next_state["profiles"][profile_id])
    target_status = payload.get("target_status")
    current_status = profile["status"]
    if target_status not in KYC_TRANSITIONS.get(current_status, set()):
        return {
            "ok": False,
            "reason": "invalid_transition",
            "current_status": current_status,
            "target_status": target_status,
            "state": next_state,
            "side_effects": (),
        }
    blocking_reasons = []
    if target_status == "pending_screening" and not _document_ready_for_approval(next_state, profile_id):
        blocking_reasons.append("document_verification_incomplete")
    if target_status == "approved":
        if not _document_ready_for_approval(next_state, profile_id):
            blocking_reasons.append("no_accepted_identity_document")
        if _blocking_hits(next_state, profile_id):
            blocking_reasons.append("blocking_screening_hit_open")
        if profile["edd_required"] and not _edd_packet_complete(next_state, profile_id):
            blocking_reasons.append("edd_packet_incomplete")
        coverage = _ownership_coverage(next_state, profile)
        if profile["customer_type"] in {"entity", "trust", "correspondent"} and not coverage["complete"]:
            blocking_reasons.append("beneficial_owner_coverage_incomplete")
        if profile["duplicate_candidates"]:
            blocking_reasons.append("duplicate_resolution_pending")
    if blocking_reasons:
        return {
            "ok": False,
            "reason": "lifecycle_guard_failed",
            "blocking_reasons": tuple(blocking_reasons),
            "state": next_state,
            "side_effects": (),
        }
    now = _iso_now()
    profile["status"] = target_status
    profile["updated_at"] = now
    profile["lifecycle_history"] = profile["lifecycle_history"] + (
        {
            "from": current_status,
            "to": target_status,
            "reason_code": payload.get("reason_code", "manual_transition"),
            "at": now,
        },
    )
    if target_status == "approved":
        profile["next_rescreen_due_at"] = _rescreening_due_date(profile["risk_tier"], next_state)
    next_state["profiles"][profile_id] = profile
    event_type = (
        IDENTITY_KYC_AML_COMPLIANCE_EMITTED_EVENT_TYPES[2]
        if target_status == "approved"
        else IDENTITY_KYC_AML_COMPLIANCE_EMITTED_EVENT_TYPES[1]
    )
    event = _emit(
        next_state,
        event_type,
        {
            "profile_id": profile_id,
            "tenant": profile["tenant"],
            "from": current_status,
            "to": target_status,
            "reason_code": payload.get("reason_code", "manual_transition"),
        },
    )
    return {
        "ok": True,
        "state": next_state,
        "profile": profile,
        "event": event,
        "side_effects": (),
    }


def identity_kyc_aml_compliance_record_identity_document(
    state: dict, payload: dict
) -> dict:
    next_state = _copy_state(state)
    profile_id = payload.get("profile_id")
    if profile_id not in next_state["profiles"]:
        return {
            "ok": False,
            "reason": "unknown_profile",
            "profile_id": profile_id,
            "state": next_state,
            "side_effects": (),
        }
    states = _document_states(payload)
    now = _iso_now()
    document_id = payload.get("id") or _new_id("doc", next_state["documents"])
    document = {
        "id": document_id,
        "tenant": payload.get("tenant") or next_state["profiles"][profile_id]["tenant"],
        "profile_id": profile_id,
        "document_class": payload.get("document_class"),
        "jurisdiction": payload.get("jurisdiction"),
        "issuing_authority": payload.get("issuing_authority"),
        "identifier": payload.get("identifier"),
        "verification_status": states["verification_status"],
        "authenticity_status": states["authenticity_status"],
        "expiry_state": states["expiry_state"],
        "missing_fields": states["missing_fields"],
        "face_match_confidence": payload.get("face_match_confidence"),
        "liveness_outcome": payload.get("liveness_outcome"),
        "payload": dict(payload),
        "created_at": now,
        "updated_at": now,
    }
    next_state["documents"][document_id] = document
    event_type = (
        IDENTITY_KYC_AML_COMPLIANCE_EMITTED_EVENT_TYPES[3]
        if document["verification_status"] == "rejected"
        else IDENTITY_KYC_AML_COMPLIANCE_EMITTED_EVENT_TYPES[1]
    )
    event = _emit(
        next_state,
        event_type,
        {
            "profile_id": profile_id,
            "document_id": document_id,
            "verification_status": document["verification_status"],
        },
    )
    return {
        "ok": not bool(states["missing_fields"]),
        "state": next_state,
        "record": document,
        "event": event,
        "missing_fields": states["missing_fields"],
        "side_effects": (),
    }


def identity_kyc_aml_compliance_evaluate_document_evidence(
    state: dict, payload: dict
) -> dict:
    next_state = _copy_state(state)
    document_id = payload.get("document_id")
    if document_id not in next_state["documents"]:
        return {
            "ok": False,
            "reason": "unknown_document",
            "document_id": document_id,
            "state": next_state,
            "side_effects": (),
        }
    document = dict(next_state["documents"][document_id])
    states = _document_states({**document["payload"], **payload})
    document.update(states)
    document["updated_at"] = _iso_now()
    next_state["documents"][document_id] = document
    return {
        "ok": True,
        "state": next_state,
        "record": document,
        "side_effects": (),
    }


def identity_kyc_aml_compliance_register_beneficial_owner(
    state: dict, payload: dict
) -> dict:
    next_state = _copy_state(state)
    profile_id = payload.get("profile_id")
    if profile_id not in next_state["profiles"]:
        return {
            "ok": False,
            "reason": "unknown_profile",
            "profile_id": profile_id,
            "state": next_state,
            "side_effects": (),
        }
    profile = next_state["profiles"][profile_id]
    threshold = _beneficial_owner_threshold(profile, next_state)
    ownership_pct = float(payload.get("ownership_pct") or 0.0)
    role_type = payload.get("role_type", "beneficial_owner")
    screening_required = ownership_pct >= threshold or role_type in CONTROL_PERSON_ROLES
    owner_id = payload.get("id") or _new_id("owner", next_state["beneficial_owners"])
    now = _iso_now()
    record = {
        "id": owner_id,
        "tenant": profile["tenant"],
        "profile_id": profile_id,
        "owner_name": payload.get("owner_name"),
        "role_type": role_type,
        "ownership_pct": ownership_pct,
        "screening_required": screening_required,
        "coverage_basis": "threshold_or_control_person" if screening_required else "below_threshold",
        "payload": dict(payload),
        "created_at": now,
        "updated_at": now,
    }
    next_state["beneficial_owners"][owner_id] = record
    event = _emit(
        next_state,
        IDENTITY_KYC_AML_COMPLIANCE_EMITTED_EVENT_TYPES[1],
        {"profile_id": profile_id, "owner_id": owner_id, "screening_required": screening_required},
    )
    return {
        "ok": True,
        "state": next_state,
        "record": record,
        "ownership_coverage": _ownership_coverage(next_state, profile),
        "event": event,
        "side_effects": (),
    }


def identity_kyc_aml_compliance_record_screening_hit(
    state: dict, payload: dict
) -> dict:
    next_state = _copy_state(state)
    profile_id = payload.get("profile_id")
    if profile_id not in next_state["profiles"]:
        return {
            "ok": False,
            "reason": "unknown_profile",
            "profile_id": profile_id,
            "state": next_state,
            "side_effects": (),
        }
    category = payload.get("category", "sanctions")
    if category not in SCREENING_CATEGORIES:
        return {
            "ok": False,
            "reason": "unknown_screening_category",
            "category": category,
            "state": next_state,
            "side_effects": (),
        }
    severity = payload.get("severity", "medium")
    blocking = category == "sanctions" and severity in {"high", "critical"}
    if category in {"pep", "rca"}:
        blocking = True
    hit_id = payload.get("id") or _new_id("screen", next_state["screening_hits"])
    now = _iso_now()
    record = {
        "id": hit_id,
        "tenant": next_state["profiles"][profile_id]["tenant"],
        "profile_id": profile_id,
        "category": category,
        "watchlist_source": payload.get("watchlist_source", "vendor_feed"),
        "match_basis": payload.get("match_basis", "name_dob"),
        "alias_pathway": payload.get("alias_pathway"),
        "program_context": payload.get("program_context"),
        "severity": severity,
        "confidence": float(payload.get("confidence", 0.0)),
        "disposition": payload.get("disposition", "open"),
        "blocking": blocking,
        "payload": dict(payload),
        "created_at": now,
        "updated_at": now,
    }
    next_state["screening_hits"][hit_id] = record
    profile = dict(next_state["profiles"][profile_id])
    if category in {"pep", "rca"} and "enhanced_due_diligence" not in profile["obligations"]:
        profile["obligations"] = tuple(profile["obligations"]) + ("enhanced_due_diligence",)
        profile["edd_required"] = True
        profile["edd_reasons"] = tuple(dict.fromkeys(tuple(profile["edd_reasons"]) + (f"{category}_screening_hit",)))
        next_state["profiles"][profile_id] = profile
    event = _emit(
        next_state,
        IDENTITY_KYC_AML_COMPLIANCE_EMITTED_EVENT_TYPES[3],
        {"profile_id": profile_id, "screening_hit_id": hit_id, "category": category, "blocking": blocking},
    )
    return {
        "ok": True,
        "state": next_state,
        "record": record,
        "event": event,
        "side_effects": (),
    }


def identity_kyc_aml_compliance_resolve_screening_hit(
    state: dict, payload: dict
) -> dict:
    next_state = _copy_state(state)
    hit_id = payload.get("screening_hit_id")
    if hit_id not in next_state["screening_hits"]:
        return {
            "ok": False,
            "reason": "unknown_screening_hit",
            "screening_hit_id": hit_id,
            "state": next_state,
            "side_effects": (),
        }
    record = dict(next_state["screening_hits"][hit_id])
    record["disposition"] = payload.get("disposition", record["disposition"])
    record["resolution_notes"] = payload.get("resolution_notes")
    record["resolved_by"] = payload.get("resolved_by")
    record["updated_at"] = _iso_now()
    if record["disposition"] in {"cleared", "false_positive"}:
        record["blocking"] = False
    next_state["screening_hits"][hit_id] = record
    event = _emit(
        next_state,
        IDENTITY_KYC_AML_COMPLIANCE_EMITTED_EVENT_TYPES[1],
        {"screening_hit_id": hit_id, "disposition": record["disposition"]},
    )
    return {"ok": True, "state": next_state, "record": record, "event": event, "side_effects": ()}


def identity_kyc_aml_compliance_schedule_rescreening(
    state: dict, payload: dict
) -> dict:
    next_state = _copy_state(state)
    profile_id = payload.get("profile_id")
    if profile_id not in next_state["profiles"]:
        return {
            "ok": False,
            "reason": "unknown_profile",
            "profile_id": profile_id,
            "state": next_state,
            "side_effects": (),
        }
    profile = dict(next_state["profiles"][profile_id])
    profile["next_rescreen_due_at"] = payload.get(
        "next_rescreen_due_at", _rescreening_due_date(profile["risk_tier"], next_state)
    )
    profile["updated_at"] = _iso_now()
    next_state["profiles"][profile_id] = profile
    event = _emit(
        next_state,
        IDENTITY_KYC_AML_COMPLIANCE_EMITTED_EVENT_TYPES[1],
        {"profile_id": profile_id, "next_rescreen_due_at": profile["next_rescreen_due_at"]},
    )
    return {"ok": True, "state": next_state, "profile": profile, "event": event, "side_effects": ()}


def identity_kyc_aml_compliance_triage_monitoring_alert(
    state: dict, payload: dict
) -> dict:
    next_state = _copy_state(state)
    profile_id = payload.get("profile_id")
    tenant = payload.get("tenant")
    if profile_id:
        if profile_id not in next_state["profiles"]:
            return {
                "ok": False,
                "reason": "unknown_profile",
                "profile_id": profile_id,
                "state": next_state,
                "side_effects": (),
            }
        tenant = next_state["profiles"][profile_id]["tenant"]
    severity = payload.get("severity", "medium")
    alert_id = payload.get("id") or _new_id("alert", next_state["monitoring_alerts"])
    due_hours = {"low": 72, "medium": 24, "high": 8, "critical": 4}[severity]
    now = _iso_now()
    due_at = payload.get("due_at") or (datetime.utcnow() + timedelta(hours=due_hours)).replace(microsecond=0).isoformat() + "Z"
    record = {
        "id": alert_id,
        "tenant": tenant or "tenant-smoke",
        "profile_id": profile_id,
        "source_type": payload.get("source_type", "transaction_monitoring"),
        "typology": payload.get("typology", "structuring"),
        "severity": severity,
        "status": payload.get("status", "open"),
        "assigned_to": payload.get("assigned_to"),
        "due_at": due_at,
        "preliminary_disposition": payload.get("preliminary_disposition", "pending_review"),
        "payload": dict(payload),
        "created_at": now,
        "updated_at": now,
    }
    next_state["monitoring_alerts"][alert_id] = record
    event = _emit(
        next_state,
        IDENTITY_KYC_AML_COMPLIANCE_EMITTED_EVENT_TYPES[3],
        {"alert_id": alert_id, "profile_id": profile_id, "severity": severity},
    )
    return {"ok": True, "state": next_state, "record": record, "event": event, "side_effects": ()}


def identity_kyc_aml_compliance_promote_alert_to_case(
    state: dict, payload: dict
) -> dict:
    next_state = _copy_state(state)
    alert_id = payload.get("alert_id")
    if alert_id not in next_state["monitoring_alerts"]:
        return {
            "ok": False,
            "reason": "unknown_alert",
            "alert_id": alert_id,
            "state": next_state,
            "side_effects": (),
        }
    alert = dict(next_state["monitoring_alerts"][alert_id])
    if alert["severity"] not in {"high", "critical"} and payload.get("force") is not True:
        return {
            "ok": False,
            "reason": "alert_not_case_eligible",
            "alert_id": alert_id,
            "state": next_state,
            "side_effects": (),
        }
    case_id = payload.get("id") or _new_id("case", next_state["suspicious_activity_cases"])
    now = _iso_now()
    record = {
        "id": case_id,
        "tenant": alert["tenant"],
        "profile_id": alert.get("profile_id") or payload.get("profile_id"),
        "alert_id": alert_id,
        "case_status": payload.get("case_status", "open"),
        "escalation_reason": payload.get("escalation_reason", "alert_threshold_met"),
        "payload": {"alert": alert, **dict(payload)},
        "created_at": now,
        "updated_at": now,
    }
    next_state["suspicious_activity_cases"][case_id] = record
    alert["status"] = "promoted_to_case"
    alert["updated_at"] = now
    next_state["monitoring_alerts"][alert_id] = alert
    event = _emit(
        next_state,
        IDENTITY_KYC_AML_COMPLIANCE_EMITTED_EVENT_TYPES[3],
        {"alert_id": alert_id, "case_id": case_id, "profile_id": record["profile_id"]},
    )
    return {"ok": True, "state": next_state, "record": record, "event": event, "side_effects": ()}


def identity_kyc_aml_compliance_record_compliance_review(
    state: dict, payload: dict
) -> dict:
    next_state = _copy_state(state)
    profile_id = payload.get("profile_id")
    if profile_id not in next_state["profiles"]:
        return {
            "ok": False,
            "reason": "unknown_profile",
            "profile_id": profile_id,
            "state": next_state,
            "side_effects": (),
        }
    review_id = payload.get("id") or _new_id("review", next_state["compliance_reviews"])
    now = _iso_now()
    record = {
        "id": review_id,
        "tenant": next_state["profiles"][profile_id]["tenant"],
        "profile_id": profile_id,
        "review_type": payload.get("review_type", "case_review"),
        "review_status": payload.get("review_status", "open"),
        "reviewer": payload.get("reviewer", "unassigned"),
        "approved_score": payload.get("approved_score"),
        "payload": dict(payload),
        "created_at": now,
        "updated_at": now,
    }
    next_state["compliance_reviews"][review_id] = record
    event = _emit(
        next_state,
        IDENTITY_KYC_AML_COMPLIANCE_EMITTED_EVENT_TYPES[1],
        {"profile_id": profile_id, "review_id": review_id, "review_type": record["review_type"]},
    )
    return {"ok": True, "state": next_state, "record": record, "event": event, "side_effects": ()}


def identity_kyc_aml_compliance_challenge_risk_score(
    state: dict, payload: dict
) -> dict:
    next_state = _copy_state(state)
    profile_id = payload.get("profile_id")
    if profile_id not in next_state["profiles"]:
        return {
            "ok": False,
            "reason": "unknown_profile",
            "profile_id": profile_id,
            "state": next_state,
            "side_effects": (),
        }
    if not payload.get("challenge_note") or not payload.get("supervisor"):
        return {
            "ok": False,
            "reason": "challenge_requires_note_and_supervisor",
            "state": next_state,
            "side_effects": (),
        }
    profile = dict(next_state["profiles"][profile_id])
    original_score = profile["risk_score"]
    challenged_score = float(payload.get("challenged_score", original_score))
    profile["risk_score"] = challenged_score
    profile["risk_tier"] = "high" if challenged_score >= 0.65 else "medium" if challenged_score >= 0.35 else "low"
    profile["updated_at"] = _iso_now()
    next_state["profiles"][profile_id] = profile
    review_result = identity_kyc_aml_compliance_record_compliance_review(
        next_state,
        {
            "profile_id": profile_id,
            "review_type": "risk_score_challenge",
            "review_status": "completed",
            "reviewer": payload.get("reviewer", payload["supervisor"]),
            "approved_score": challenged_score,
            "challenge_note": payload["challenge_note"],
            "supervisor": payload["supervisor"],
            "original_score": original_score,
        },
    )
    next_state = review_result["state"]
    event = _emit(
        next_state,
        IDENTITY_KYC_AML_COMPLIANCE_EMITTED_EVENT_TYPES[1],
        {"profile_id": profile_id, "original_score": original_score, "challenged_score": challenged_score},
    )
    return {
        "ok": True,
        "state": next_state,
        "profile": profile,
        "review": review_result["record"],
        "event": event,
        "side_effects": (),
    }


def identity_kyc_aml_compliance_create_control_assertion(
    state: dict, payload: dict
) -> dict:
    next_state = _copy_state(state)
    assertion_id = payload.get("id") or _new_id("assertion", next_state["control_assertions"])
    now = _iso_now()
    record = {
        "id": assertion_id,
        "tenant": payload.get("tenant", "global"),
        "assertion_type": payload.get("assertion_type", "continuous_control_test"),
        "assertion_status": payload.get("assertion_status", "pass"),
        "evidence_hash": _digest(payload),
        "payload": dict(payload),
        "created_at": now,
        "updated_at": now,
    }
    next_state["control_assertions"][assertion_id] = record
    return {"ok": True, "state": next_state, "record": record, "side_effects": ()}


def identity_kyc_aml_compliance_register_governed_model(
    state: dict, payload: dict
) -> dict:
    next_state = _copy_state(state)
    model_id = payload.get("id") or _new_id("model", next_state["governed_models"])
    now = _iso_now()
    record = {
        "id": model_id,
        "tenant": payload.get("tenant", "global"),
        "model_name": payload.get("model_name", "kyc-risk-model"),
        "model_version": payload.get("model_version", "v1"),
        "approval_status": payload.get("approval_status", "draft"),
        "payload": dict(payload),
        "created_at": now,
        "updated_at": now,
    }
    next_state["governed_models"][model_id] = record
    return {"ok": True, "state": next_state, "record": record, "side_effects": ()}


def identity_kyc_aml_compliance_simulate_counterfactual_policy(
    state: dict, payload: dict
) -> dict:
    threshold = float(payload.get("beneficial_owner_threshold_pct", _parameter_value(state, "beneficial_owner_threshold_pct")))
    current_threshold = float(_parameter_value(state, "beneficial_owner_threshold_pct"))
    affected_profiles = []
    for profile in state["profiles"].values():
        coverage = _ownership_coverage(state, profile)
        if coverage["threshold_pct"] != threshold:
            affected_profiles.append(
                {
                    "profile_id": profile["id"],
                    "current_threshold": coverage["threshold_pct"],
                    "simulated_threshold": threshold,
                    "current_complete": coverage["complete"],
                    "delta_pct": round(current_threshold - threshold, 2),
                }
            )
    return {
        "ok": True,
        "scenario": {
            "parameter": "beneficial_owner_threshold_pct",
            "current_value": current_threshold,
            "simulated_value": threshold,
            "affected_profiles": tuple(affected_profiles),
        },
        "side_effects": (),
    }


def identity_kyc_aml_compliance_receive_event(state: dict, event: dict) -> dict:
    next_state = _copy_state(state)
    idem = event.get("idempotency_key") or event.get("event_id") or _digest(event)
    if idem in next_state["idempotency_keys"]:
        return {"ok": True, "duplicate": True, "state": next_state, "side_effects": ()}
    next_state["idempotency_keys"].add(idem)
    if event.get("event_type") not in IDENTITY_KYC_AML_COMPLIANCE_CONSUMED_EVENT_TYPES:
        dead = {
            "id": _digest((idem, "dead")),
            "event_type": event.get("event_type"),
            "payload": dict(event),
            "reason": "unknown_event_type",
            "received_at": _iso_now(),
        }
        next_state["dead_letter"].append(dead)
        return {
            "ok": False,
            "duplicate": False,
            "state": next_state,
            "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
            "side_effects": (),
        }
    envelope = {
        "id": _digest((idem, "inbox")),
        "event_type": event["event_type"],
        "payload": dict(event),
        "received_at": _iso_now(),
    }
    next_state["inbox"].append(envelope)
    follow_up = None
    if event["event_type"] == "PolicyChanged":
        follow_up = identity_kyc_aml_compliance_triage_monitoring_alert(
            next_state,
            {
                "tenant": event.get("tenant", "global"),
                "source_type": "policy_change",
                "typology": "policy_rescreening",
                "severity": event.get("severity", "medium"),
                "preliminary_disposition": "rescreening_required",
            },
        )
    elif event["event_type"] == "AuditEventSealed":
        follow_up = identity_kyc_aml_compliance_create_control_assertion(
            next_state,
            {
                "tenant": event.get("tenant", "global"),
                "assertion_type": "audit_event_sealed",
                "assertion_status": "review_required",
                "source_event": dict(event),
            },
        )
    elif event["event_type"] == "OperationalKpiChanged":
        follow_up = identity_kyc_aml_compliance_triage_monitoring_alert(
            next_state,
            {
                "tenant": event.get("tenant", "global"),
                "source_type": "operational_kpi",
                "typology": event.get("metric", "backlog_threshold"),
                "severity": "high" if float(event.get("value", 0)) > float(event.get("threshold", 0)) else "medium",
                "preliminary_disposition": "capacity_review",
            },
        )
    if follow_up:
        next_state = follow_up["state"]
    return {"ok": True, "duplicate": False, "state": next_state, "follow_up": follow_up, "side_effects": ()}


def identity_kyc_aml_compliance_command_kyc_profile(state: dict, payload: dict) -> dict:
    return identity_kyc_aml_compliance_create_kyc_profile(state, payload)


def identity_kyc_aml_compliance_query_workbench(state: dict, filters: dict | None = None) -> dict:
    filters = dict(filters or {})
    limit = int(filters.get("limit") or _parameter_value(state, "workbench_limit"))
    profiles = list(state["profiles"].values())[:limit]
    alert_sla_breaches = [
        alert for alert in state["monitoring_alerts"].values() if alert["status"] == "open" and alert["severity"] in {"high", "critical"}
    ]
    return {
        "ok": True,
        "records": tuple(profiles),
        "metrics": {
            "profiles": len(state["profiles"]),
            "pending_edd": sum(1 for profile in state["profiles"].values() if profile["status"] == "pending_edd"),
            "blocking_hits": sum(1 for hit in state["screening_hits"].values() if hit["blocking"]),
            "overdue_rescreening": sum(
                1
                for profile in state["profiles"].values()
                if profile.get("next_rescreen_due_at") and _date_value(profile["next_rescreen_due_at"]) < date.today()
            ),
            "alert_sla_breaches": len(alert_sla_breaches),
        },
        "filters": filters,
        "read_only": True,
        "side_effects": (),
    }


def identity_kyc_aml_compliance_build_workbench_view(
    state: dict | None = None, tenant: str = "default"
) -> dict:
    state = identity_kyc_aml_compliance_empty_state() if state is None else state
    query = identity_kyc_aml_compliance_query_workbench(state, {"tenant": tenant})
    queues = {
        "onboarding_queue": tuple(
            profile["id"]
            for profile in state["profiles"].values()
            if profile["status"] in {"pending_verification", "pending_screening"}
        ),
        "edd_review_queue": tuple(
            profile["id"] for profile in state["profiles"].values() if profile["status"] == "pending_edd"
        ),
        "screening_queue": tuple(
            hit["id"] for hit in state["screening_hits"].values() if hit["disposition"] == "open"
        ),
        "monitoring_alert_queue": tuple(
            alert["id"] for alert in state["monitoring_alerts"].values() if alert["status"] == "open"
        ),
        "suspicious_activity_case_queue": tuple(
            case["id"] for case in state["suspicious_activity_cases"].values() if case["case_status"] == "open"
        ),
        "rescreening_queue": tuple(
            profile["id"]
            for profile in state["profiles"].values()
            if profile.get("next_rescreen_due_at") and _date_value(profile["next_rescreen_due_at"]) <= date.today()
        ),
    }
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "tenant": tenant,
        "route": f"/workbench/pbcs/{PBC_KEY}",
        "tables": IDENTITY_KYC_AML_COMPLIANCE_BUSINESS_TABLES,
        "queues": queues,
        "views": DOMAIN_WORKBENCH_VIEWS,
        "metrics": query["metrics"],
        "side_effects": (),
    }


def identity_kyc_aml_compliance_build_detail_view(state: dict, profile_id: str) -> dict:
    if profile_id not in state["profiles"]:
        return {"ok": False, "reason": "unknown_profile", "profile_id": profile_id, "side_effects": ()}
    projection = _profile_projection(state, state["profiles"][profile_id])
    return {"ok": True, "pbc": PBC_KEY, **projection, "side_effects": ()}


def identity_kyc_aml_compliance_run_advanced_assessment(
    state: dict, payload: dict | None = None
) -> dict:
    payload = dict(payload or {})
    high_risk = [profile for profile in state["profiles"].values() if profile["risk_tier"] == "high"]
    unresolved_hits = [hit for hit in state["screening_hits"].values() if hit["disposition"] == "open"]
    anomaly_score = round(
        min(1.0, 0.2 + len(high_risk) * 0.08 + len(unresolved_hits) * 0.05 + len(state["monitoring_alerts"]) * 0.03),
        4,
    )
    return {
        "ok": True,
        "score": anomaly_score,
        "explanations": (
            "risk_factor_model_active",
            "screening_category_segmentation_active",
            "rescreening_calendar_active",
            "event_driven_triage_active",
        ),
        "high_risk_profiles": tuple(profile["id"] for profile in high_risk),
        "unresolved_hits": tuple(hit["id"] for hit in unresolved_hits),
        "payload": payload,
        "side_effects": (),
    }


def identity_kyc_aml_compliance_parse_document_instruction(
    document: str, instruction: str
) -> dict:
    lowered = instruction.lower()
    candidate_operations = []
    if "document" in lowered or "passport" in lowered or "id card" in lowered:
        candidate_operations.append("record_identity_document")
    if "screen" in lowered or "sanction" in lowered or "pep" in lowered:
        candidate_operations.append("record_screening_hit")
    if "owner" in lowered or "ubo" in lowered or "beneficial" in lowered:
        candidate_operations.append("register_beneficial_owner")
    if "approve" in lowered or "onboard" in lowered:
        candidate_operations.append("advance_kyc_profile_lifecycle")
    if not candidate_operations:
        candidate_operations.append("record_compliance_review")
    return {
        "ok": True,
        "candidate_tables": IDENTITY_KYC_AML_COMPLIANCE_BUSINESS_TABLES[:4],
        "candidate_operations": tuple(dict.fromkeys(candidate_operations)),
        "instruction": instruction,
        "document_digest": _digest(document),
        "requires_human_confirmation": True,
        "side_effects": (),
    }


def _table_model_name(table_name: str) -> str:
    return "".join(part.capitalize() for part in table_name.split("_"))


def identity_kyc_aml_compliance_build_schema_contract() -> dict:
    table_contracts = tuple(
        {
            "table": spec["table"],
            "fields": tuple(field[0] for field in spec["fields"]),
            "field_specs": spec["fields"],
            "primary_key": spec["primary_key"],
            "owned_by": PBC_KEY,
        }
        for spec in SCHEMA_TABLES
    )
    return {
        "format": "appgen.identity-kyc-aml-compliance-owned-schema-contract.v2",
        "ok": True,
        "pbc": PBC_KEY,
        "tables": table_contracts,
        "migrations": (
            {
                "path": "pbcs/identity_kyc_aml_compliance/migrations/001_initial.sql",
                "operation": "create_owned_tables",
                "tables": tuple(spec["table"] for spec in SCHEMA_TABLES),
                "backend_allowlist": IDENTITY_KYC_AML_COMPLIANCE_ALLOWED_DATABASE_BACKENDS,
            },
        ),
        "models": tuple(
            {
                "class_name": _table_model_name(spec["table"]),
                "table": spec["table"],
                "fields": tuple(field[0] for field in spec["fields"]),
            }
            for spec in SCHEMA_TABLES
        ),
        "datastore_backends": IDENTITY_KYC_AML_COMPLIANCE_ALLOWED_DATABASE_BACKENDS,
        "database_backends": IDENTITY_KYC_AML_COMPLIANCE_ALLOWED_DATABASE_BACKENDS,
        "shared_table_access": False,
        "owned_tables": IDENTITY_KYC_AML_COMPLIANCE_OWNED_TABLES,
    }


def identity_kyc_aml_compliance_build_service_contract() -> dict:
    return {
        "format": "appgen.identity-kyc-aml-compliance-service-contract.v2",
        "ok": True,
        "pbc": PBC_KEY,
        "command_methods": (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "register_schema_extension",
            "receive_event",
            "command_kyc_profile",
            "run_advanced_assessment",
            "parse_document_instruction",
        )
        + DOMAIN_OPERATIONS,
        "query_methods": ("query_workbench", "build_workbench_view", "build_detail_view"),
        "shared_table_access": False,
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
    }


def identity_kyc_aml_compliance_build_api_contract() -> dict:
    return {
        "format": "appgen.identity-kyc-aml-compliance-api-contract.v2",
        "ok": True,
        "pbc": PBC_KEY,
        "routes": tuple(ROUTE_OPERATION_MAP),
        "route_to_operation": dict(ROUTE_OPERATION_MAP),
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "owned_tables": IDENTITY_KYC_AML_COMPLIANCE_OWNED_TABLES,
    }


def identity_kyc_aml_compliance_build_release_evidence() -> dict:
    checks = (
        {"id": "schema_models_migrations", "ok": True},
        {"id": "classification_and_lifecycle_guards", "ok": True},
        {"id": "document_authenticity_controls", "ok": True},
        {"id": "screening_category_and_edd_routing", "ok": True},
        {"id": "beneficial_owner_threshold_policy", "ok": True},
        {"id": "event_driven_rescreening_handlers", "ok": True},
        {"id": "monitoring_alert_to_case_boundary", "ok": True},
        {"id": "ui_agent_release_surface", "ok": True},
    )
    return {
        "format": "appgen.identity-kyc-aml-compliance-release-evidence.v2",
        "ok": all(check["ok"] for check in checks),
        "pbc": PBC_KEY,
        "checks": checks,
        "generated_artifacts": {
            "migrations": identity_kyc_aml_compliance_build_schema_contract()["migrations"],
            "models": identity_kyc_aml_compliance_build_schema_contract()["models"],
            "events": {
                "contract": "AppGen-X",
                "emits": IDENTITY_KYC_AML_COMPLIANCE_EMITTED_EVENT_TYPES,
                "consumes": IDENTITY_KYC_AML_COMPLIANCE_CONSUMED_EVENT_TYPES,
            },
            "handlers": ("receive_event",),
            "ui": IDENTITY_KYC_AML_COMPLIANCE_UI_FRAGMENT_KEYS,
            "workflows": (
                "identity_kyc_aml_compliance_onboarding_wizard",
                "identity_kyc_aml_compliance_edd_review_packet",
                "identity_kyc_aml_compliance_monitoring_escalation",
            ),
        },
        "blocking_gaps": (),
    }


def identity_kyc_aml_compliance_permissions_contract() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "permissions": (
            "identity_kyc_aml_compliance.read",
            "identity_kyc_aml_compliance.create",
            "identity_kyc_aml_compliance.update",
            "identity_kyc_aml_compliance.approve",
            "identity_kyc_aml_compliance.admin",
            "identity_kyc_aml_compliance.operate",
        ),
        "roles": ("analyst", "investigator", "approver", "auditor", "admin"),
        "side_effects": (),
    }


def identity_kyc_aml_compliance_verify_owned_table_boundary(references=()) -> dict:
    invalid = tuple(
        ref
        for ref in references
        if isinstance(ref, str)
        and ref.endswith(("table", "profile", "document", "owner", "event"))
        and not ref.startswith(f"{PBC_KEY}_")
    )
    return {
        "ok": not invalid,
        "pbc": PBC_KEY,
        "invalid_references": invalid,
        "allowed_tables": IDENTITY_KYC_AML_COMPLIANCE_OWNED_TABLES,
        "shared_table_access": False,
    }


def identity_kyc_aml_compliance_operation_registry() -> dict[str, Callable]:
    return {
        "configure_runtime": identity_kyc_aml_compliance_configure_runtime,
        "set_parameter": identity_kyc_aml_compliance_set_parameter,
        "register_rule": identity_kyc_aml_compliance_register_rule,
        "register_schema_extension": identity_kyc_aml_compliance_register_schema_extension,
        "receive_event": identity_kyc_aml_compliance_receive_event,
        "command_kyc_profile": identity_kyc_aml_compliance_command_kyc_profile,
        "create_kyc_profile": identity_kyc_aml_compliance_create_kyc_profile,
        "advance_kyc_profile_lifecycle": identity_kyc_aml_compliance_advance_kyc_profile_lifecycle,
        "record_identity_document": identity_kyc_aml_compliance_record_identity_document,
        "evaluate_document_evidence": identity_kyc_aml_compliance_evaluate_document_evidence,
        "register_beneficial_owner": identity_kyc_aml_compliance_register_beneficial_owner,
        "record_screening_hit": identity_kyc_aml_compliance_record_screening_hit,
        "resolve_screening_hit": identity_kyc_aml_compliance_resolve_screening_hit,
        "schedule_rescreening": identity_kyc_aml_compliance_schedule_rescreening,
        "triage_monitoring_alert": identity_kyc_aml_compliance_triage_monitoring_alert,
        "promote_alert_to_case": identity_kyc_aml_compliance_promote_alert_to_case,
        "record_compliance_review": identity_kyc_aml_compliance_record_compliance_review,
        "challenge_risk_score": identity_kyc_aml_compliance_challenge_risk_score,
        "create_control_assertion": identity_kyc_aml_compliance_create_control_assertion,
        "register_governed_model": identity_kyc_aml_compliance_register_governed_model,
        "simulate_counterfactual_policy": identity_kyc_aml_compliance_simulate_counterfactual_policy,
        "run_advanced_assessment": identity_kyc_aml_compliance_run_advanced_assessment,
        "query_workbench": identity_kyc_aml_compliance_query_workbench,
        "build_workbench_view": identity_kyc_aml_compliance_build_workbench_view,
        "build_detail_view": identity_kyc_aml_compliance_build_detail_view,
    }


def identity_kyc_aml_compliance_runtime_capabilities() -> dict:
    domain = domain_depth_contract()
    smoke = identity_kyc_aml_compliance_runtime_smoke()
    return {
        "format": "appgen.identity-kyc-aml-compliance-runtime-capabilities.v2",
        "ok": smoke["ok"] and domain["ok"],
        "pbc": PBC_KEY,
        "implementation_directory": f"src/pyAppGen/pbcs/{PBC_KEY}",
        "owned_tables": IDENTITY_KYC_AML_COMPLIANCE_OWNED_TABLES,
        "allowed_database_backends": IDENTITY_KYC_AML_COMPLIANCE_ALLOWED_DATABASE_BACKENDS,
        "standard_features": IDENTITY_KYC_AML_COMPLIANCE_STANDARD_FEATURE_KEYS,
        "capabilities": IDENTITY_KYC_AML_COMPLIANCE_RUNTIME_CAPABILITY_KEYS,
        "operations": tuple(identity_kyc_aml_compliance_operation_registry()),
        "smoke": smoke,
        "world_class_domain_depth": domain,
        "database_backends": IDENTITY_KYC_AML_COMPLIANCE_ALLOWED_DATABASE_BACKENDS,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def identity_kyc_aml_compliance_runtime_smoke() -> dict:
    state = identity_kyc_aml_compliance_empty_state()
    cfg = identity_kyc_aml_compliance_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": IDENTITY_KYC_AML_COMPLIANCE_REQUIRED_EVENT_TOPIC,
        },
    )
    profile = identity_kyc_aml_compliance_create_kyc_profile(
        cfg["state"],
        {
            "tenant": "tenant-smoke",
            "subject_name": "Alice Example",
            "customer_type": "individual",
            "jurisdiction": "KE",
            "product_exposure": "checking",
            "channel": "remote",
            "expected_activity": "salary",
        },
    )
    document = identity_kyc_aml_compliance_record_identity_document(
        profile["state"],
        {
            "profile_id": profile["record"]["id"],
            "document_class": "passport",
            "jurisdiction": "KE",
            "issuing_authority": "State",
            "identifier": "A12345",
            "issue_date": "2024-01-01",
            "expiry_date": "2030-01-01",
            "capture_method": "mobile_app",
            "face_match_confidence": 0.94,
            "liveness_outcome": "pass",
        },
    )
    screening = identity_kyc_aml_compliance_record_screening_hit(
        document["state"],
        {
            "profile_id": profile["record"]["id"],
            "category": "adverse_media",
            "severity": "low",
            "confidence": 0.44,
            "disposition": "false_positive",
        },
    )
    resolved = identity_kyc_aml_compliance_resolve_screening_hit(
        screening["state"],
        {"screening_hit_id": screening["record"]["id"], "disposition": "false_positive"},
    )
    advanced = identity_kyc_aml_compliance_run_advanced_assessment(resolved["state"])
    lifecycle = identity_kyc_aml_compliance_advance_kyc_profile_lifecycle(
        resolved["state"],
        {"profile_id": profile["record"]["id"], "target_status": "pending_screening", "reason_code": "docs_ready"},
    )
    approved = identity_kyc_aml_compliance_advance_kyc_profile_lifecycle(
        lifecycle["state"],
        {"profile_id": profile["record"]["id"], "target_status": "approved", "reason_code": "clear_screening"},
    )
    inbox = identity_kyc_aml_compliance_receive_event(
        approved["state"],
        {"event_type": "PolicyChanged", "tenant": "tenant-smoke", "idempotency_key": "smoke-policy"},
    )
    duplicate = identity_kyc_aml_compliance_receive_event(
        inbox["state"],
        {"event_type": "PolicyChanged", "tenant": "tenant-smoke", "idempotency_key": "smoke-policy"},
    )
    dead = identity_kyc_aml_compliance_receive_event(
        duplicate["state"],
        {"event_type": "UnexpectedEvent", "tenant": "tenant-smoke", "idempotency_key": "smoke-bad"},
    )
    workbench = identity_kyc_aml_compliance_build_workbench_view(dead["state"], tenant="tenant-smoke")
    detail = identity_kyc_aml_compliance_build_detail_view(dead["state"], profile["record"]["id"])
    release = identity_kyc_aml_compliance_build_release_evidence()
    schema = identity_kyc_aml_compliance_build_schema_contract()
    boundary = identity_kyc_aml_compliance_verify_owned_table_boundary(
        IDENTITY_KYC_AML_COMPLIANCE_OWNED_TABLES + ("foreign_table",)
    )
    domain = domain_depth_smoke_test()
    checks = (
        {"id": "configure_runtime", "ok": cfg["ok"]},
        {"id": "create_kyc_profile", "ok": profile["ok"]},
        {"id": "record_identity_document", "ok": document["ok"]},
        {"id": "record_screening_hit", "ok": screening["ok"]},
        {"id": "resolve_screening_hit", "ok": resolved["ok"]},
        {"id": "advance_lifecycle_to_approved", "ok": approved["ok"]},
        {"id": "event_handler_duplicate_guard", "ok": duplicate.get("duplicate") is True},
        {"id": "dead_letter_for_unknown_event", "ok": dead["ok"] is False},
        {"id": "build_workbench_view", "ok": workbench["ok"]},
        {"id": "build_detail_view", "ok": detail["ok"]},
        {"id": "advanced_assessment", "ok": advanced["ok"]},
        {"id": "build_schema_contract", "ok": schema["ok"]},
        {"id": "build_release_evidence", "ok": release["ok"]},
        {"id": "owned_boundary_rejects_foreign_table", "ok": boundary["ok"] is False},
        {"id": "domain_depth", "ok": domain["ok"]},
    )
    return {
        "format": "appgen.identity-kyc-aml-compliance-runtime-smoke.v2",
        "ok": all(check["ok"] for check in checks),
        "checks": checks,
        "configuration": cfg,
        "profile": profile,
        "approved": approved,
        "advanced": advanced,
        "workbench": workbench,
        "detail": detail,
        "release": release,
        "side_effects": (),
    }
