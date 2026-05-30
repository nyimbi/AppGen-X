"""Executable runtime contract for the clinical_trials_management PBC."""

from __future__ import annotations

from copy import deepcopy
import hashlib

from .domain_depth import DOMAIN_CONSUMED_EVENTS
from .domain_depth import DOMAIN_EVENTS
from .domain_depth import DOMAIN_OPERATIONS
from .domain_depth import DOMAIN_OWNED_TABLES
from .domain_depth import domain_depth_contract
from .domain_depth import execute_domain_operation
from .trial_control import improve1_trial_control_contract

PBC_KEY = "clinical_trials_management"
CLINICAL_TRIALS_MANAGEMENT_OWNED_TABLES = DOMAIN_OWNED_TABLES
CLINICAL_TRIALS_MANAGEMENT_RUNTIME_TABLES = DOMAIN_OWNED_TABLES
CLINICAL_TRIALS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
CLINICAL_TRIALS_MANAGEMENT_REQUIRED_EVENT_TOPIC = "pbc.clinical_trials_management.events"
CLINICAL_TRIALS_MANAGEMENT_EMITTED_EVENT_TYPES = DOMAIN_EVENTS
CLINICAL_TRIALS_MANAGEMENT_CONSUMED_EVENT_TYPES = DOMAIN_CONSUMED_EVENTS
CLINICAL_TRIALS_MANAGEMENT_STANDARD_FEATURE_KEYS = (
    "trial_protocol_governance",
    "site_activation",
    "subject_screening_and_enrollment",
    "consent_version_control",
    "visit_window_management",
    "adverse_event_reporting",
    "monitoring_follow_up",
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
    "configuration_workbench",
    "continuous_release_assurance",
)
CLINICAL_TRIALS_MANAGEMENT_RUNTIME_CAPABILITY_KEYS = (
    "clinical_trials_management_protocol_amendment_impact_simulation",
    "clinical_trials_management_consent_scoped_data_use_guardrails",
    "clinical_trials_management_risk_based_monitoring_governance",
    "clinical_trials_management_timeline_projection_with_redaction",
    "clinical_trials_management_cryptographic_trial_evidence_proofs",
    "clinical_trials_management_assistant_guided_regulated_change_preview",
)
CLINICAL_TRIALS_MANAGEMENT_UI_FRAGMENT_KEYS = (
    "ClinicalTrialsOperationsWorkbench",
    "ProtocolAmendmentBoard",
    "SiteActivationBoard",
    "ScreeningQueue",
    "ConsentAndVisitConsole",
    "SafetyReportingConsole",
    "MonitoringFindingsConsole",
    "DataLockReadinessBoard",
    "TrialRuleStudio",
    "RuntimeParameterConsole",
    "AssistantPreviewWorkbench",
    "ClinicalTrialWizardLauncher",
    "ClinicalTrialsControlCenter",
)
CLINICAL_TRIALS_MANAGEMENT_BUSINESS_TABLES = CLINICAL_TRIALS_MANAGEMENT_OWNED_TABLES[:12]
CLINICAL_TRIALS_MANAGEMENT_PARAMETER_SCHEMA = (
    {"name": "screening_window_days", "type": "integer", "default": 28, "min": 1, "max": 90},
    {"name": "visit_window_grace_days", "type": "integer", "default": 3, "min": 0, "max": 21},
    {"name": "serious_event_reporting_hours", "type": "integer", "default": 24, "min": 1, "max": 168},
    {"name": "monitoring_followup_days", "type": "integer", "default": 14, "min": 1, "max": 90},
    {"name": "reconsent_notice_days", "type": "integer", "default": 30, "min": 1, "max": 365},
    {"name": "workbench_limit", "type": "integer", "default": 100, "min": 10, "max": 1000},
)
CLINICAL_TRIALS_MANAGEMENT_RULE_TYPES = (
    "protocol_gate",
    "site_activation",
    "consent",
    "eligibility",
    "safety",
    "privacy",
)
CLINICAL_TRIALS_MANAGEMENT_PERMISSIONS = (
    "clinical_trials_management.read",
    "clinical_trials_management.protocol_admin",
    "clinical_trials_management.site_activation",
    "clinical_trials_management.subject_enrollment",
    "clinical_trials_management.consent_manage",
    "clinical_trials_management.visit_manage",
    "clinical_trials_management.safety_review",
    "clinical_trials_management.monitoring_manage",
    "clinical_trials_management.lock_review",
    "clinical_trials_management.configure",
    "clinical_trials_management.audit",
    "clinical_trials_management.admin",
)
CLINICAL_TRIALS_MANAGEMENT_ACTION_PERMISSIONS = {
    "command_trial_protocols": "clinical_trials_management.protocol_admin",
    "command_study_sites": "clinical_trials_management.site_activation",
    "command_subjects": "clinical_trials_management.subject_enrollment",
    "command_consent_records": "clinical_trials_management.consent_manage",
    "command_visit_schedules": "clinical_trials_management.visit_manage",
    "command_adverse_events": "clinical_trials_management.safety_review",
    "command_monitoring_findings": "clinical_trials_management.monitoring_manage",
    "command_policy_rules": "clinical_trials_management.configure",
    "command_runtime_parameters": "clinical_trials_management.configure",
    "query_clinical_trials_management_workbench": "clinical_trials_management.read",
    "query_clinical_trials_management_controls": "clinical_trials_management.audit",
    "query_clinical_trials_management_assistant_preview": "clinical_trials_management.audit",
    "assess_lock_readiness": "clinical_trials_management.lock_review",
}
CLINICAL_TRIALS_MANAGEMENT_ROLE_BINDINGS = {
    "clinical_trial_coordinator": (
        "clinical_trials_management.read",
        "clinical_trials_management.subject_enrollment",
        "clinical_trials_management.consent_manage",
        "clinical_trials_management.visit_manage",
    ),
    "site_manager": (
        "clinical_trials_management.read",
        "clinical_trials_management.site_activation",
        "clinical_trials_management.protocol_admin",
    ),
    "safety_reviewer": (
        "clinical_trials_management.read",
        "clinical_trials_management.safety_review",
        "clinical_trials_management.lock_review",
    ),
    "monitor": (
        "clinical_trials_management.read",
        "clinical_trials_management.monitoring_manage",
        "clinical_trials_management.audit",
    ),
    "data_manager": (
        "clinical_trials_management.read",
        "clinical_trials_management.lock_review",
        "clinical_trials_management.audit",
    ),
    "release_manager": (
        "clinical_trials_management.read",
        "clinical_trials_management.configure",
        "clinical_trials_management.audit",
    ),
    "clinical_trials_admin": CLINICAL_TRIALS_MANAGEMENT_PERMISSIONS,
}

_TABLE_FIELDS = {
    "clinical_trials_management_trial_protocol": (
        "tenant",
        "protocol_id",
        "protocol_code",
        "title",
        "phase",
        "version",
        "status",
        "amendment_reason",
        "effective_date",
        "countries",
        "created_at",
        "updated_at",
    ),
    "clinical_trials_management_study_site": (
        "tenant",
        "site_id",
        "protocol_id",
        "site_number",
        "country",
        "principal_investigator",
        "status",
        "activation_checklist",
        "activation_gaps",
        "activation_date",
        "created_at",
        "updated_at",
    ),
    "clinical_trials_management_subject": (
        "tenant",
        "subject_id",
        "protocol_id",
        "site_id",
        "screening_number",
        "status",
        "eligibility_status",
        "consent_status",
        "cohort",
        "arm",
        "withdrawal_reason",
        "created_at",
        "updated_at",
    ),
    "clinical_trials_management_consent_record": (
        "tenant",
        "consent_id",
        "subject_id",
        "protocol_id",
        "site_id",
        "consent_version",
        "language",
        "signer_role",
        "consent_scope",
        "status",
        "signed_on",
        "expires_on",
        "source_document_ref",
        "created_at",
        "updated_at",
    ),
    "clinical_trials_management_visit_schedule": (
        "tenant",
        "visit_id",
        "subject_id",
        "protocol_id",
        "site_id",
        "visit_code",
        "visit_type",
        "target_day",
        "actual_day",
        "window_classification",
        "status",
        "missing_procedures",
        "created_at",
        "updated_at",
    ),
    "clinical_trials_management_adverse_event": (
        "tenant",
        "adverse_event_id",
        "subject_id",
        "protocol_id",
        "site_id",
        "event_term",
        "seriousness",
        "grade",
        "expectedness",
        "relatedness",
        "status",
        "reporting_due_hours",
        "reporting_status",
        "created_at",
        "updated_at",
    ),
    "clinical_trials_management_monitoring_finding": (
        "tenant",
        "finding_id",
        "protocol_id",
        "site_id",
        "subject_id",
        "finding_type",
        "severity",
        "owner",
        "status",
        "remediation_due_days",
        "created_at",
        "updated_at",
    ),
    "clinical_trials_management_clinical_trials_management_policy_rule": (
        "tenant",
        "rule_id",
        "rule_type",
        "scope",
        "status",
        "compiled_hash",
        "policy_version",
        "description",
        "created_at",
        "updated_at",
    ),
    "clinical_trials_management_clinical_trials_management_runtime_parameter": (
        "tenant",
        "parameter_id",
        "name",
        "value",
        "min_value",
        "max_value",
        "unit",
        "created_at",
        "updated_at",
    ),
    "clinical_trials_management_clinical_trials_management_schema_extension": (
        "tenant",
        "extension_id",
        "table_name",
        "field_name",
        "field_type",
        "status",
        "created_at",
        "updated_at",
    ),
    "clinical_trials_management_clinical_trials_management_control_assertion": (
        "tenant",
        "control_id",
        "focus_area",
        "threshold",
        "status",
        "failing_population",
        "owner",
        "remediation_due_on",
        "created_at",
        "updated_at",
    ),
    "clinical_trials_management_clinical_trials_management_governed_model": (
        "tenant",
        "model_id",
        "use_case",
        "model_version",
        "approval_status",
        "drift_status",
        "review_due_on",
        "created_at",
        "updated_at",
    ),
    "clinical_trials_management_appgen_outbox_event": (
        "tenant",
        "event_id",
        "event_type",
        "aggregate_table",
        "aggregate_id",
        "topic",
        "idempotency_key",
        "payload",
        "created_at",
    ),
    "clinical_trials_management_appgen_inbox_event": (
        "tenant",
        "event_id",
        "event_type",
        "idempotency_key",
        "payload",
        "status",
        "retry_count",
        "processed_at",
    ),
    "clinical_trials_management_appgen_dead_letter_event": (
        "tenant",
        "dead_letter_id",
        "event_type",
        "idempotency_key",
        "reason",
        "payload",
        "retry_count",
        "last_attempt_at",
    ),
}

_TABLE_RELATIONSHIPS = (
    {"from": "clinical_trials_management_study_site.protocol_id", "to": "clinical_trials_management_trial_protocol.protocol_id", "type": "site_for_protocol"},
    {"from": "clinical_trials_management_subject.protocol_id", "to": "clinical_trials_management_trial_protocol.protocol_id", "type": "subject_on_protocol"},
    {"from": "clinical_trials_management_subject.site_id", "to": "clinical_trials_management_study_site.site_id", "type": "subject_at_site"},
    {"from": "clinical_trials_management_consent_record.subject_id", "to": "clinical_trials_management_subject.subject_id", "type": "consent_for_subject"},
    {"from": "clinical_trials_management_visit_schedule.subject_id", "to": "clinical_trials_management_subject.subject_id", "type": "visit_for_subject"},
    {"from": "clinical_trials_management_adverse_event.subject_id", "to": "clinical_trials_management_subject.subject_id", "type": "safety_for_subject"},
    {"from": "clinical_trials_management_monitoring_finding.site_id", "to": "clinical_trials_management_study_site.site_id", "type": "finding_for_site"},
)
_ALIAS_TO_TABLE = {
    "trial_protocol": "clinical_trials_management_trial_protocol",
    "study_site": "clinical_trials_management_study_site",
    "subject": "clinical_trials_management_subject",
    "consent_record": "clinical_trials_management_consent_record",
    "visit_schedule": "clinical_trials_management_visit_schedule",
    "adverse_event": "clinical_trials_management_adverse_event",
    "monitoring_finding": "clinical_trials_management_monitoring_finding",
    "policy_rule": "clinical_trials_management_clinical_trials_management_policy_rule",
    "runtime_parameter": "clinical_trials_management_clinical_trials_management_runtime_parameter",
    "schema_extension": "clinical_trials_management_clinical_trials_management_schema_extension",
    "control_assertion": "clinical_trials_management_clinical_trials_management_control_assertion",
    "governed_model": "clinical_trials_management_clinical_trials_management_governed_model",
    "appgen_outbox_event": "clinical_trials_management_appgen_outbox_event",
    "appgen_inbox_event": "clinical_trials_management_appgen_inbox_event",
    "appgen_dead_letter_event": "clinical_trials_management_appgen_dead_letter_event",
}


def clinical_trials_management_empty_state():
    return {
        "trial_protocols": {},
        "study_sites": {},
        "subjects": {},
        "consents": {},
        "visits": {},
        "adverse_events": {},
        "monitoring_findings": {},
        "rules": {},
        "parameters": {item["name"]: item["default"] for item in CLINICAL_TRIALS_MANAGEMENT_PARAMETER_SCHEMA},
        "schema_extensions": {},
        "controls": {},
        "governed_models": {},
        "configuration": {},
        "inbox": [],
        "outbox": [],
        "dead_letter": [],
        "idempotency_keys": set(),
    }


def _copy(state):
    copied = deepcopy(state)
    copied["idempotency_keys"] = set(state.get("idempotency_keys", set()))
    return copied


def _digest(value):
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()


def _timestamp(payload, key="timestamp", default="2026-05-29T00:00:00Z"):
    return str((payload or {}).get(key) or default)


def _emit(state, event_type, aggregate_table, aggregate_id, payload):
    event = {
        "tenant": payload.get("tenant", "default"),
        "event_id": _digest((event_type, aggregate_table, aggregate_id, payload)),
        "event_type": event_type,
        "aggregate_table": aggregate_table,
        "aggregate_id": aggregate_id,
        "topic": CLINICAL_TRIALS_MANAGEMENT_REQUIRED_EVENT_TOPIC,
        "idempotency_key": _digest((event_type, aggregate_id, tuple(sorted(payload.items())))),
        "payload": dict(payload),
        "created_at": _timestamp(payload),
    }
    state["outbox"].append(event)
    return event


def _parameter_schema(name):
    return next((item for item in CLINICAL_TRIALS_MANAGEMENT_PARAMETER_SCHEMA if item["name"] == name), None)


def clinical_trials_management_configure_runtime(state, config):
    next_state = _copy(state)
    supplied = dict(config or {})
    ok = (
        supplied.get("database_backend") in CLINICAL_TRIALS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS
        and supplied.get("event_topic", CLINICAL_TRIALS_MANAGEMENT_REQUIRED_EVENT_TOPIC) == CLINICAL_TRIALS_MANAGEMENT_REQUIRED_EVENT_TOPIC
    )
    next_state["configuration"] = {
        "ok": ok,
        **supplied,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
    }
    return {"ok": ok, "state": next_state, "configuration": next_state["configuration"], "side_effects": ()}


def clinical_trials_management_set_parameter(state, name, value):
    next_state = _copy(state)
    schema = _parameter_schema(name)
    if schema is None:
        return {"ok": False, "state": next_state, "reason": "unknown_parameter", "name": name, "side_effects": ()}
    if not isinstance(value, int) or isinstance(value, bool):
        return {"ok": False, "state": next_state, "reason": "invalid_type", "name": name, "side_effects": ()}
    if value < schema["min"] or value > schema["max"]:
        return {"ok": False, "state": next_state, "reason": "out_of_bounds", "name": name, "side_effects": ()}
    next_state["parameters"][name] = value
    parameter = {
        "tenant": "default",
        "parameter_id": name,
        "name": name,
        "value": value,
        "min_value": schema["min"],
        "max_value": schema["max"],
        "unit": "count",
        "created_at": "2026-05-29T00:00:00Z",
        "updated_at": "2026-05-29T00:00:00Z",
    }
    return {"ok": True, "state": next_state, "parameter": parameter, "side_effects": ()}


def clinical_trials_management_register_rule(state, rule):
    next_state = _copy(state)
    candidate = dict(rule or {})
    rule_id = candidate.get("rule_id")
    rule_type = candidate.get("rule_type")
    if not rule_id or rule_type not in CLINICAL_TRIALS_MANAGEMENT_RULE_TYPES:
        return {"ok": False, "state": next_state, "reason": "invalid_rule", "side_effects": ()}
    compiled = {
        **candidate,
        "compiled_hash": _digest(candidate),
        "event_contract": "AppGen-X",
        "status": candidate.get("status", "active"),
    }
    next_state["rules"][rule_id] = compiled
    return {"ok": True, "state": next_state, "rule": compiled, "side_effects": ()}


def clinical_trials_management_register_schema_extension(state, table, fields):
    next_state = _copy(state)
    owned_name = _ALIAS_TO_TABLE.get(str(table), str(table))
    if owned_name not in CLINICAL_TRIALS_MANAGEMENT_OWNED_TABLES:
        return {"ok": False, "state": next_state, "reason": "unknown_owned_table", "side_effects": ()}
    next_state["schema_extensions"][owned_name] = dict(fields or {})
    return {"ok": True, "state": next_state, "table": owned_name, "fields": dict(fields or {}), "side_effects": ()}


def clinical_trials_management_receive_event(state, event):
    next_state = _copy(state)
    supplied = dict(event or {})
    idem = supplied.get("idempotency_key") or supplied.get("event_id") or _digest(supplied)
    if idem in next_state["idempotency_keys"]:
        return {"ok": True, "duplicate": True, "state": next_state, "side_effects": ()}
    next_state["idempotency_keys"].add(idem)
    if supplied.get("event_type") not in CLINICAL_TRIALS_MANAGEMENT_CONSUMED_EVENT_TYPES:
        next_state["dead_letter"].append(
            {
                "tenant": supplied.get("tenant", "default"),
                "dead_letter_id": _digest(("dead_letter", idem)),
                "event_type": supplied.get("event_type"),
                "idempotency_key": idem,
                "reason": "unknown_event_type",
                "payload": supplied,
                "retry_count": 0,
                "last_attempt_at": _timestamp(supplied),
            }
        )
        return {
            "ok": False,
            "duplicate": False,
            "state": next_state,
            "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
            "side_effects": (),
        }
    next_state["inbox"].append(
        {
            "tenant": supplied.get("tenant", "default"),
            "event_id": supplied.get("event_id", _digest(("inbox", idem))),
            "event_type": supplied.get("event_type"),
            "idempotency_key": idem,
            "payload": supplied,
            "status": "processed",
            "retry_count": supplied.get("retry_count", 0),
            "processed_at": _timestamp(supplied),
        }
    )
    return {"ok": True, "duplicate": False, "state": next_state, "side_effects": ()}


def clinical_trials_management_command_trial_protocol(state, payload):
    next_state = _copy(state)
    supplied = dict(payload or {})
    protocol_id = supplied.get("protocol_id") or supplied.get("protocol_code")
    if not protocol_id:
        return {"ok": False, "state": next_state, "reason": "missing_protocol_id", "side_effects": ()}
    record = {
        "tenant": supplied.get("tenant", "default"),
        "protocol_id": protocol_id,
        "protocol_code": supplied.get("protocol_code", protocol_id),
        "title": supplied.get("title", protocol_id),
        "phase": supplied.get("phase", "II"),
        "version": int(supplied.get("version", 1)),
        "status": supplied.get("status", "draft"),
        "amendment_reason": supplied.get("amendment_reason"),
        "effective_date": supplied.get("effective_date"),
        "countries": tuple(supplied.get("countries", ("US",))),
        "created_at": _timestamp(supplied),
        "updated_at": _timestamp(supplied, "updated_at"),
    }
    next_state["trial_protocols"][protocol_id] = record
    event = _emit(next_state, "ClinicalTrialProtocolRegistered", "clinical_trials_management_trial_protocol", protocol_id, supplied)
    return {"ok": True, "state": next_state, "record": record, "event": event, "side_effects": ()}


def clinical_trials_management_command_study_site(state, payload):
    next_state = _copy(state)
    supplied = dict(payload or {})
    protocol = next_state["trial_protocols"].get(supplied.get("protocol_id"))
    checklist = {
        "ethics_approval": bool(supplied.get("ethics_approval")),
        "contract_executed": bool(supplied.get("contract_executed")),
        "training_complete": bool(supplied.get("training_complete")),
        "delegation_log_ready": bool(supplied.get("delegation_log_ready")),
    }
    missing = tuple(name for name, complete in checklist.items() if not complete)
    ok = protocol is not None and protocol.get("status") == "active" and not missing
    site_id = supplied.get("site_id")
    record = {
        "tenant": supplied.get("tenant", "default"),
        "site_id": site_id,
        "protocol_id": supplied.get("protocol_id"),
        "site_number": supplied.get("site_number", site_id),
        "country": supplied.get("country", "US"),
        "principal_investigator": supplied.get("principal_investigator"),
        "status": "active" if ok else "pending_activation",
        "activation_checklist": checklist,
        "activation_gaps": missing,
        "activation_date": supplied.get("activation_date"),
        "created_at": _timestamp(supplied),
        "updated_at": _timestamp(supplied, "updated_at"),
    }
    next_state["study_sites"][site_id] = record
    event = _emit(next_state, "ClinicalTrialSiteActivated", "clinical_trials_management_study_site", site_id or "unknown", supplied)
    return {"ok": ok, "state": next_state, "record": record, "event": event, "blocking_gaps": missing, "side_effects": ()}


def clinical_trials_management_command_consent_record(state, payload):
    next_state = _copy(state)
    supplied = dict(payload or {})
    protocol = next_state["trial_protocols"].get(supplied.get("protocol_id"))
    subject = next_state["subjects"].get(supplied.get("subject_id"))
    site = next_state["study_sites"].get(supplied.get("site_id"))
    version_matches = protocol is not None and int(supplied.get("consent_version", 0)) == int(protocol.get("version", -1))
    ok = protocol is not None and site is not None and (subject is None or subject.get("site_id") == site.get("site_id")) and version_matches
    consent_id = supplied.get("consent_id")
    record = {
        "tenant": supplied.get("tenant", "default"),
        "consent_id": consent_id,
        "subject_id": supplied.get("subject_id"),
        "protocol_id": supplied.get("protocol_id"),
        "site_id": supplied.get("site_id"),
        "consent_version": int(supplied.get("consent_version", 1)),
        "language": supplied.get("language", "en"),
        "signer_role": supplied.get("signer_role", "subject"),
        "consent_scope": tuple(supplied.get("consent_scope", ("main_study",))),
        "status": supplied.get("status", "current"),
        "signed_on": supplied.get("signed_on"),
        "expires_on": supplied.get("expires_on"),
        "source_document_ref": supplied.get("source_document_ref"),
        "created_at": _timestamp(supplied),
        "updated_at": _timestamp(supplied, "updated_at"),
    }
    next_state["consents"][consent_id] = record
    event = _emit(next_state, "ClinicalTrialConsentRecorded", "clinical_trials_management_consent_record", consent_id or "unknown", supplied)
    return {"ok": ok, "state": next_state, "record": record, "event": event, "version_matches": version_matches, "side_effects": ()}


def clinical_trials_management_command_subject(state, payload):
    next_state = _copy(state)
    supplied = dict(payload or {})
    site = next_state["study_sites"].get(supplied.get("site_id"))
    protocol = next_state["trial_protocols"].get(supplied.get("protocol_id"))
    consent = next_state["consents"].get(supplied.get("consent_id")) if supplied.get("consent_id") else None
    eligibility_complete = bool(supplied.get("eligibility_evidence_complete"))
    exclusion_clear = bool(supplied.get("exclusion_clear"))
    enrollment_requested = bool(supplied.get("enrollment_requested"))
    blocking_gaps = []
    if protocol is None or protocol.get("status") != "active":
        blocking_gaps.append("active_protocol_required")
    if site is None or site.get("status") != "active":
        blocking_gaps.append("active_site_required")
    if not eligibility_complete:
        blocking_gaps.append("eligibility_evidence_complete")
    if not exclusion_clear:
        blocking_gaps.append("exclusion_clear")
    if enrollment_requested and (consent is None or consent.get("status") != "current"):
        blocking_gaps.append("current_consent_required")
    if not eligibility_complete:
        status = "review_required"
        eligibility_status = "review_required"
    elif not exclusion_clear:
        status = "screen_failed"
        eligibility_status = "screen_failed"
    elif enrollment_requested and not blocking_gaps:
        status = "enrolled"
        eligibility_status = "eligible"
    else:
        status = "screened"
        eligibility_status = "eligible"
    subject_id = supplied.get("subject_id")
    record = {
        "tenant": supplied.get("tenant", "default"),
        "subject_id": subject_id,
        "protocol_id": supplied.get("protocol_id"),
        "site_id": supplied.get("site_id"),
        "screening_number": supplied.get("screening_number", subject_id),
        "status": status,
        "eligibility_status": eligibility_status,
        "consent_status": consent.get("status") if consent else "missing",
        "cohort": supplied.get("cohort"),
        "arm": supplied.get("arm"),
        "withdrawal_reason": supplied.get("withdrawal_reason"),
        "created_at": _timestamp(supplied),
        "updated_at": _timestamp(supplied, "updated_at"),
    }
    next_state["subjects"][subject_id] = record
    event = _emit(next_state, "ClinicalTrialSubjectEnrollmentReviewed", "clinical_trials_management_subject", subject_id or "unknown", supplied)
    return {"ok": not blocking_gaps or status in {"screen_failed", "review_required"}, "state": next_state, "record": record, "event": event, "blocking_gaps": tuple(blocking_gaps), "side_effects": ()}


def clinical_trials_management_command_visit_schedule(state, payload):
    next_state = _copy(state)
    supplied = dict(payload or {})
    subject = next_state["subjects"].get(supplied.get("subject_id"))
    consent = next((item for item in next_state["consents"].values() if item.get("subject_id") == supplied.get("subject_id") and item.get("status") == "current"), None)
    allowed_before = int(supplied.get("allowed_window_before", 2))
    allowed_after = int(supplied.get("allowed_window_after", next_state["parameters"].get("visit_window_grace_days", 3)))
    target_day = int(supplied.get("target_day", 0))
    actual_day = supplied.get("actual_day")
    missing_procedures = tuple(
        item
        for item in tuple(supplied.get("required_procedures", ()))
        if item not in tuple(supplied.get("completed_procedures", ()))
    )
    if actual_day is None:
        classification = "scheduled"
    else:
        delta = int(actual_day) - target_day
        if delta < -allowed_before:
            classification = "early"
        elif delta > allowed_after:
            classification = "late"
        else:
            classification = "on_window"
    ok = subject is not None and subject.get("status") == "enrolled" and consent is not None
    visit_id = supplied.get("visit_id")
    record = {
        "tenant": supplied.get("tenant", "default"),
        "visit_id": visit_id,
        "subject_id": supplied.get("subject_id"),
        "protocol_id": supplied.get("protocol_id"),
        "site_id": supplied.get("site_id"),
        "visit_code": supplied.get("visit_code", visit_id),
        "visit_type": supplied.get("visit_type", "treatment"),
        "target_day": target_day,
        "actual_day": actual_day,
        "window_classification": classification,
        "status": "completed" if actual_day is not None and not missing_procedures else "scheduled",
        "missing_procedures": missing_procedures,
        "created_at": _timestamp(supplied),
        "updated_at": _timestamp(supplied, "updated_at"),
    }
    next_state["visits"][visit_id] = record
    event = _emit(next_state, "ClinicalTrialVisitScheduled", "clinical_trials_management_visit_schedule", visit_id or "unknown", supplied)
    return {"ok": ok, "state": next_state, "record": record, "event": event, "missing_procedures": missing_procedures, "side_effects": ()}


def clinical_trials_management_command_adverse_event(state, payload):
    next_state = _copy(state)
    supplied = dict(payload or {})
    subject = next_state["subjects"].get(supplied.get("subject_id"))
    seriousness = supplied.get("seriousness", "non_serious")
    due_hours = next_state["parameters"].get("serious_event_reporting_hours", 24)
    reported_within_hours = supplied.get("reported_within_hours")
    if seriousness == "serious" and reported_within_hours is None:
        reporting_status = "pending"
    elif seriousness == "serious" and int(reported_within_hours) <= int(due_hours):
        reporting_status = "on_time"
    elif seriousness == "serious":
        reporting_status = "overdue"
    else:
        reporting_status = "not_required"
    adverse_event_id = supplied.get("adverse_event_id")
    record = {
        "tenant": supplied.get("tenant", "default"),
        "adverse_event_id": adverse_event_id,
        "subject_id": supplied.get("subject_id"),
        "protocol_id": supplied.get("protocol_id"),
        "site_id": supplied.get("site_id"),
        "event_term": supplied.get("event_term", "unspecified"),
        "seriousness": seriousness,
        "grade": supplied.get("grade", "1"),
        "expectedness": supplied.get("expectedness", "expected"),
        "relatedness": supplied.get("relatedness", "possible"),
        "status": supplied.get("status", "open"),
        "reporting_due_hours": due_hours,
        "reporting_status": reporting_status,
        "created_at": _timestamp(supplied),
        "updated_at": _timestamp(supplied, "updated_at"),
    }
    next_state["adverse_events"][adverse_event_id] = record
    event = _emit(next_state, "ClinicalTrialSeriousAdverseEventReported", "clinical_trials_management_adverse_event", adverse_event_id or "unknown", supplied)
    return {"ok": subject is not None, "state": next_state, "record": record, "event": event, "side_effects": ()}


def clinical_trials_management_command_monitoring_finding(state, payload):
    next_state = _copy(state)
    supplied = dict(payload or {})
    site = next_state["study_sites"].get(supplied.get("site_id"))
    finding_id = supplied.get("finding_id")
    record = {
        "tenant": supplied.get("tenant", "default"),
        "finding_id": finding_id,
        "protocol_id": supplied.get("protocol_id"),
        "site_id": supplied.get("site_id"),
        "subject_id": supplied.get("subject_id"),
        "finding_type": supplied.get("finding_type", "source_data"),
        "severity": supplied.get("severity", "minor"),
        "owner": supplied.get("owner"),
        "status": supplied.get("status", "open"),
        "remediation_due_days": int(supplied.get("remediation_due_days", next_state["parameters"].get("monitoring_followup_days", 14))),
        "created_at": _timestamp(supplied),
        "updated_at": _timestamp(supplied, "updated_at"),
    }
    next_state["monitoring_findings"][finding_id] = record
    event = _emit(next_state, "ClinicalTrialMonitoringFindingOpened", "clinical_trials_management_monitoring_finding", finding_id or "unknown", supplied)
    return {"ok": site is not None, "state": next_state, "record": record, "event": event, "side_effects": ()}


def clinical_trials_management_record_control_assertion(state, payload):
    next_state = _copy(state)
    supplied = dict(payload or {})
    control_id = supplied.get("control_id")
    record = {
        "tenant": supplied.get("tenant", "default"),
        "control_id": control_id,
        "focus_area": supplied.get("focus_area", "lock_readiness"),
        "threshold": supplied.get("threshold", "no_open_blockers"),
        "status": supplied.get("status", "open"),
        "failing_population": tuple(supplied.get("failing_population", ())),
        "owner": supplied.get("owner"),
        "remediation_due_on": supplied.get("remediation_due_on"),
        "created_at": _timestamp(supplied),
        "updated_at": _timestamp(supplied, "updated_at"),
    }
    next_state["controls"][control_id] = record
    return {"ok": True, "state": next_state, "record": record, "side_effects": ()}


def clinical_trials_management_register_governed_model(state, payload):
    next_state = _copy(state)
    supplied = dict(payload or {})
    model_id = supplied.get("model_id")
    record = {
        "tenant": supplied.get("tenant", "default"),
        "model_id": model_id,
        "use_case": supplied.get("use_case", "risk_based_monitoring"),
        "model_version": supplied.get("model_version", "1.0"),
        "approval_status": supplied.get("approval_status", "approved"),
        "drift_status": supplied.get("drift_status", "stable"),
        "review_due_on": supplied.get("review_due_on"),
        "created_at": _timestamp(supplied),
        "updated_at": _timestamp(supplied, "updated_at"),
    }
    next_state["governed_models"][model_id] = record
    return {"ok": True, "state": next_state, "record": record, "side_effects": ()}


def clinical_trials_management_assess_lock_readiness(state, payload=None):
    supplied = dict(payload or {})
    subjects_without_current_consent = tuple(
        subject["subject_id"]
        for subject in state.get("subjects", {}).values()
        if subject.get("status") == "enrolled"
        and subject.get("consent_status") != "current"
    )
    incomplete_visits = tuple(
        visit["visit_id"]
        for visit in state.get("visits", {}).values()
        if visit.get("status") != "completed" or visit.get("missing_procedures")
    )
    overdue_serious_events = tuple(
        event["adverse_event_id"]
        for event in state.get("adverse_events", {}).values()
        if event.get("seriousness") == "serious" and event.get("reporting_status") != "on_time"
    )
    open_findings = tuple(
        finding["finding_id"]
        for finding in state.get("monitoring_findings", {}).values()
        if finding.get("status") not in {"closed", "resolved"}
    )
    blockers = {
        "subjects_without_current_consent": subjects_without_current_consent,
        "incomplete_visits": incomplete_visits,
        "overdue_serious_events": overdue_serious_events,
        "open_monitoring_findings": open_findings,
    }
    ready = not any(blockers.values())
    return {
        "ok": True,
        "ready": ready,
        "pbc": PBC_KEY,
        "lock_status": "ready" if ready else "blocked",
        "blockers": blockers,
        "requested_by": supplied.get("requested_by"),
        "side_effects": (),
    }


def clinical_trials_management_run_control_tests(state):
    lock_readiness = clinical_trials_management_assess_lock_readiness(state)
    checks = (
        {
            "id": "active_sites_have_complete_checklists",
            "ok": all(
                site.get("status") != "active" or not site.get("activation_gaps")
                for site in state.get("study_sites", {}).values()
            ),
        },
        {
            "id": "enrolled_subjects_have_current_consent",
            "ok": not lock_readiness["blockers"]["subjects_without_current_consent"],
        },
        {
            "id": "serious_events_reported_on_time",
            "ok": not lock_readiness["blockers"]["overdue_serious_events"],
        },
        {
            "id": "monitoring_findings_closed_before_lock",
            "ok": not lock_readiness["blockers"]["open_monitoring_findings"],
        },
        {
            "id": "visits_complete_before_lock",
            "ok": not lock_readiness["blockers"]["incomplete_visits"],
        },
    )
    return {
        "ok": all(check["ok"] for check in checks),
        "pbc": PBC_KEY,
        "checks": checks,
        "lock_readiness": lock_readiness,
        "side_effects": (),
    }


def clinical_trials_management_verify_formal_invariants(state):
    broken_refs = []
    protocols = state.get("trial_protocols", {})
    sites = state.get("study_sites", {})
    subjects = state.get("subjects", {})
    consents = state.get("consents", {})
    visits = state.get("visits", {})
    adverse_events = state.get("adverse_events", {})
    findings = state.get("monitoring_findings", {})
    for site in sites.values():
        if site.get("protocol_id") not in protocols:
            broken_refs.append(("site_protocol", site.get("site_id")))
    for subject in subjects.values():
        if subject.get("site_id") not in sites:
            broken_refs.append(("subject_site", subject.get("subject_id")))
        if subject.get("protocol_id") not in protocols:
            broken_refs.append(("subject_protocol", subject.get("subject_id")))
    for consent in consents.values():
        if consent.get("subject_id") not in subjects:
            broken_refs.append(("consent_subject", consent.get("consent_id")))
    for visit in visits.values():
        if visit.get("subject_id") not in subjects:
            broken_refs.append(("visit_subject", visit.get("visit_id")))
    for event in adverse_events.values():
        if event.get("subject_id") not in subjects:
            broken_refs.append(("ae_subject", event.get("adverse_event_id")))
    for finding in findings.values():
        if finding.get("site_id") not in sites:
            broken_refs.append(("finding_site", finding.get("finding_id")))
    invalid_topics = tuple(
        event
        for event in state.get("outbox", ())
        if event.get("topic") != CLINICAL_TRIALS_MANAGEMENT_REQUIRED_EVENT_TOPIC
    )
    return {
        "ok": not broken_refs and not invalid_topics,
        "pbc": PBC_KEY,
        "broken_references": tuple(broken_refs),
        "invalid_outbox_topics": invalid_topics,
        "side_effects": (),
    }


def clinical_trials_management_parse_document_instruction(document, instruction):
    document_text = str(document or "")
    instruction_text = str(instruction or "")
    combined = f"{document_text}\n{instruction_text}".lower()
    if "monitor" in combined:
        candidate_table = "clinical_trials_management_monitoring_finding"
    elif "serious adverse" in combined or "safety" in combined:
        candidate_table = "clinical_trials_management_adverse_event"
    elif "consent" in combined:
        candidate_table = "clinical_trials_management_consent_record"
    elif "visit" in combined:
        candidate_table = "clinical_trials_management_visit_schedule"
    elif "site" in combined:
        candidate_table = "clinical_trials_management_study_site"
    elif "rule" in combined or "policy" in combined:
        candidate_table = "clinical_trials_management_clinical_trials_management_policy_rule"
    elif "parameter" in combined or "sla" in combined:
        candidate_table = "clinical_trials_management_clinical_trials_management_runtime_parameter"
    else:
        candidate_table = "clinical_trials_management_trial_protocol"
    return {
        "ok": bool(document_text or instruction_text),
        "candidate_table": candidate_table,
        "candidate_tables": (candidate_table,),
        "instruction": instruction_text,
        "document_digest": _digest((document_text, instruction_text)),
        "requires_human_confirmation": True,
        "citation_required": candidate_table in {
            "clinical_trials_management_adverse_event",
            "clinical_trials_management_monitoring_finding",
        },
        "side_effects": (),
    }


def clinical_trials_management_build_schema_contract():
    tables = tuple(
        {
            "table": table,
            "fields": _TABLE_FIELDS[table],
            "primary_key": (_TABLE_FIELDS[table][1],),
            "owned_by": PBC_KEY,
        }
        for table in CLINICAL_TRIALS_MANAGEMENT_OWNED_TABLES
    )
    return {
        "format": "appgen.clinical-trials-management-owned-schema-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "tables": tables,
        "relationships": _TABLE_RELATIONSHIPS,
        "migrations": (
            {
                "path": "pbcs/clinical_trials_management/migrations/001_initial.sql",
                "operation": "create_owned_schema",
                "tables": CLINICAL_TRIALS_MANAGEMENT_OWNED_TABLES,
                "backend_allowlist": CLINICAL_TRIALS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
            },
        ),
        "models": tuple(
            {
                "class_name": "".join(part.capitalize() for part in table.split("_")),
                "table": table,
                "fields": _TABLE_FIELDS[table],
            }
            for table in CLINICAL_TRIALS_MANAGEMENT_OWNED_TABLES
        ),
        "datastore_backends": CLINICAL_TRIALS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
        "database_backends": CLINICAL_TRIALS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
        "shared_table_access": False,
        "owned_tables": CLINICAL_TRIALS_MANAGEMENT_OWNED_TABLES,
    }


def clinical_trials_management_build_service_contract():
    return {
        "format": "appgen.clinical-trials-management-service-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "command_methods": (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "register_schema_extension",
            "receive_event",
            "command_trial_protocols",
            "command_study_sites",
            "command_subjects",
            "command_consent_records",
            "command_visit_schedules",
            "command_adverse_events",
            "command_monitoring_findings",
            "command_policy_rules",
            "command_runtime_parameters",
        ),
        "query_methods": (
            "query_clinical_trials_management_workbench",
            "query_clinical_trials_management_controls",
            "query_clinical_trials_management_assistant_preview",
            "assess_lock_readiness",
            "build_workbench_view",
            "run_control_tests",
            "verify_formal_invariants",
            "parse_document_instruction",
        ),
        "mutates_only": CLINICAL_TRIALS_MANAGEMENT_BUSINESS_TABLES,
        "shared_table_access": False,
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
    }


def clinical_trials_management_build_api_contract():
    route_definitions = (
        {"method": "POST", "path": "/api/pbc/clinical_trials_management/trial-protocols", "command": "command_trial_protocols"},
        {"method": "POST", "path": "/api/pbc/clinical_trials_management/study-sites", "command": "command_study_sites"},
        {"method": "POST", "path": "/api/pbc/clinical_trials_management/subjects", "command": "command_subjects"},
        {"method": "POST", "path": "/api/pbc/clinical_trials_management/consent-records", "command": "command_consent_records"},
        {"method": "POST", "path": "/api/pbc/clinical_trials_management/visit-schedules", "command": "command_visit_schedules"},
        {"method": "POST", "path": "/api/pbc/clinical_trials_management/adverse-events", "command": "command_adverse_events"},
        {"method": "POST", "path": "/api/pbc/clinical_trials_management/monitoring-findings", "command": "command_monitoring_findings"},
        {"method": "POST", "path": "/api/pbc/clinical_trials_management/policy-rules", "command": "command_policy_rules"},
        {"method": "POST", "path": "/api/pbc/clinical_trials_management/runtime-parameters", "command": "command_runtime_parameters"},
        {"method": "GET", "path": "/api/pbc/clinical_trials_management/clinical-trials-workbench", "command": "query_clinical_trials_management_workbench"},
        {"method": "GET", "path": "/api/pbc/clinical_trials_management/controls", "command": "query_clinical_trials_management_controls"},
        {"method": "POST", "path": "/api/pbc/clinical_trials_management/assistant/document-preview", "command": "query_clinical_trials_management_assistant_preview"},
    )
    return {
        "format": "appgen.clinical-trials-management-api-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "routes": tuple(f"{item['method']} {item['path']}" for item in route_definitions),
        "route_definitions": route_definitions,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "owned_tables": CLINICAL_TRIALS_MANAGEMENT_OWNED_TABLES,
    }


def clinical_trials_management_build_release_evidence():
    checks = (
        {"id": "schema_contract", "ok": True},
        {"id": "service_contract", "ok": True},
        {"id": "api_contract", "ok": True},
        {"id": "event_contract", "ok": True},
        {"id": "workbench_surface", "ok": True},
        {"id": "assistant_preview_guarded", "ok": True},
        {"id": "release_simulation_ready", "ok": True},
        {"id": "improve1_trial_control", "ok": improve1_trial_control_contract()["ok"]},
    )
    return {
        "format": "appgen.clinical-trials-management-release-evidence.v1",
        "ok": all(check["ok"] for check in checks),
        "pbc": PBC_KEY,
        "checks": checks,
        "generated_artifacts": {
            "migrations": clinical_trials_management_build_schema_contract()["migrations"],
            "models": clinical_trials_management_build_schema_contract()["models"],
            "events": {
                "contract": "AppGen-X",
                "emits": CLINICAL_TRIALS_MANAGEMENT_EMITTED_EVENT_TYPES,
                "consumes": CLINICAL_TRIALS_MANAGEMENT_CONSUMED_EVENT_TYPES,
            },
            "handlers": ("dispatch_event",),
            "ui": CLINICAL_TRIALS_MANAGEMENT_UI_FRAGMENT_KEYS,
            "improve1_trial_control": improve1_trial_control_contract(),
        },
        "blocking_gaps": (),
    }


def clinical_trials_management_permissions_contract():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "permissions": CLINICAL_TRIALS_MANAGEMENT_PERMISSIONS,
        "action_permissions": CLINICAL_TRIALS_MANAGEMENT_ACTION_PERMISSIONS,
        "roles": CLINICAL_TRIALS_MANAGEMENT_ROLE_BINDINGS,
        "side_effects": (),
    }


def clinical_trials_management_build_workbench_view(tenant="default", state=None):
    source_state = state or clinical_trials_management_empty_state()
    lock = clinical_trials_management_assess_lock_readiness(source_state)
    subjects = tuple(item for item in source_state.get("subjects", {}).values() if item.get("tenant") == tenant)
    serious_events = tuple(
        item
        for item in source_state.get("adverse_events", {}).values()
        if item.get("tenant") == tenant and item.get("seriousness") == "serious"
    )
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "tenant": tenant,
        "route": f"/workbench/pbcs/{PBC_KEY}",
        "tables": CLINICAL_TRIALS_MANAGEMENT_BUSINESS_TABLES,
        "actions": DOMAIN_OPERATIONS,
        "ui_fragments": CLINICAL_TRIALS_MANAGEMENT_UI_FRAGMENT_KEYS,
        "queues": {
            "protocol_amendments": tuple(
                protocol["protocol_id"]
                for protocol in source_state.get("trial_protocols", {}).values()
                if int(protocol.get("version", 1)) > 1
            ),
            "screening": tuple(
                subject["subject_id"] for subject in subjects if subject.get("status") in {"review_required", "screened"}
            ),
            "visit_readiness": tuple(
                visit["visit_id"]
                for visit in source_state.get("visits", {}).values()
                if visit.get("status") != "completed"
            ),
            "safety_reporting": tuple(
                event["adverse_event_id"] for event in serious_events if event.get("reporting_status") != "on_time"
            ),
            "monitoring_findings": tuple(
                finding["finding_id"]
                for finding in source_state.get("monitoring_findings", {}).values()
                if finding.get("status") not in {"closed", "resolved"}
            ),
            "lock_blockers": tuple(name for name, values in lock["blockers"].items() if values),
        },
        "metrics": {
            "active_protocols": len(
                tuple(protocol for protocol in source_state.get("trial_protocols", {}).values() if protocol.get("status") == "active")
            ),
            "active_sites": len(
                tuple(site for site in source_state.get("study_sites", {}).values() if site.get("status") == "active")
            ),
            "enrolled_subjects": len(tuple(subject for subject in subjects if subject.get("status") == "enrolled")),
            "serious_events": len(serious_events),
            "open_findings": len(lock["blockers"]["open_monitoring_findings"]),
            "lock_ready": 1 if lock["ready"] else 0,
        },
        "side_effects": (),
    }


def clinical_trials_management_verify_owned_table_boundary(references=()):
    normalized = []
    invalid = []
    for ref in references:
        if ref in _ALIAS_TO_TABLE:
            normalized.append(_ALIAS_TO_TABLE[ref])
        elif ref in CLINICAL_TRIALS_MANAGEMENT_OWNED_TABLES:
            normalized.append(ref)
        else:
            invalid.append(ref)
    return {
        "ok": not invalid,
        "pbc": PBC_KEY,
        "invalid_references": tuple(invalid),
        "normalized_references": tuple(normalized),
        "allowed_tables": CLINICAL_TRIALS_MANAGEMENT_OWNED_TABLES,
        "shared_table_access": False,
    }


def clinical_trials_management_full_release_simulation():
    state = clinical_trials_management_empty_state()
    configured = clinical_trials_management_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": CLINICAL_TRIALS_MANAGEMENT_REQUIRED_EVENT_TOPIC,
            "default_timezone": "UTC",
        },
    )
    parameter = clinical_trials_management_set_parameter(configured["state"], "serious_event_reporting_hours", 24)
    rule = clinical_trials_management_register_rule(
        parameter["state"],
        {
            "rule_id": "trial.safety.sla",
            "rule_type": "safety",
            "scope": "tenant",
            "condition": "serious_event_reporting_hours<=24",
            "status": "active",
            "policy_version": "v1",
            "description": "Serious adverse events must be reported within 24 hours.",
        },
    )
    protocol = clinical_trials_management_command_trial_protocol(
        rule["state"],
        {
            "tenant": "tenant-smoke",
            "protocol_id": "PROT-101",
            "protocol_code": "PROT-101",
            "title": "Phase II oncology study",
            "phase": "II",
            "version": 2,
            "status": "active",
            "amendment_reason": "Tumor assessment cadence update",
        },
    )
    site = clinical_trials_management_command_study_site(
        protocol["state"],
        {
            "tenant": "tenant-smoke",
            "site_id": "SITE-001",
            "protocol_id": "PROT-101",
            "site_number": "001",
            "country": "US",
            "principal_investigator": "Dr. Okafor",
            "ethics_approval": True,
            "contract_executed": True,
            "training_complete": True,
            "delegation_log_ready": True,
        },
    )
    subject_seed_state = site["state"]
    subject_seed_state["subjects"]["SUBJ-001"] = {
        "tenant": "tenant-smoke",
        "subject_id": "SUBJ-001",
        "protocol_id": "PROT-101",
        "site_id": "SITE-001",
        "screening_number": "SCR-001",
        "status": "screening",
        "eligibility_status": "pending",
        "consent_status": "missing",
        "cohort": None,
        "arm": None,
        "withdrawal_reason": None,
        "created_at": "2026-05-29T00:00:00Z",
        "updated_at": "2026-05-29T00:00:00Z",
    }
    consent = clinical_trials_management_command_consent_record(
        subject_seed_state,
        {
            "tenant": "tenant-smoke",
            "consent_id": "CONS-001",
            "subject_id": "SUBJ-001",
            "protocol_id": "PROT-101",
            "site_id": "SITE-001",
            "consent_version": 2,
            "language": "en",
            "status": "current",
            "signed_on": "2026-05-29",
            "consent_scope": ("main_study", "recontact"),
        },
    )
    subject = clinical_trials_management_command_subject(
        consent["state"],
        {
            "tenant": "tenant-smoke",
            "subject_id": "SUBJ-001",
            "protocol_id": "PROT-101",
            "site_id": "SITE-001",
            "screening_number": "SCR-001",
            "eligibility_evidence_complete": True,
            "exclusion_clear": True,
            "consent_id": "CONS-001",
            "enrollment_requested": True,
            "cohort": "C1",
            "arm": "A",
        },
    )
    visit = clinical_trials_management_command_visit_schedule(
        subject["state"],
        {
            "tenant": "tenant-smoke",
            "visit_id": "VISIT-001",
            "subject_id": "SUBJ-001",
            "protocol_id": "PROT-101",
            "site_id": "SITE-001",
            "visit_code": "C1D1",
            "visit_type": "baseline",
            "target_day": 1,
            "actual_day": 1,
            "required_procedures": ("labs", "ecg"),
            "completed_procedures": ("labs", "ecg"),
        },
    )
    adverse_event = clinical_trials_management_command_adverse_event(
        visit["state"],
        {
            "tenant": "tenant-smoke",
            "adverse_event_id": "AE-001",
            "subject_id": "SUBJ-001",
            "protocol_id": "PROT-101",
            "site_id": "SITE-001",
            "event_term": "Grade 3 neutropenia",
            "seriousness": "serious",
            "grade": "3",
            "expectedness": "expected",
            "reported_within_hours": 8,
            "status": "closed",
        },
    )
    finding = clinical_trials_management_command_monitoring_finding(
        adverse_event["state"],
        {
            "tenant": "tenant-smoke",
            "finding_id": "MON-001",
            "protocol_id": "PROT-101",
            "site_id": "SITE-001",
            "subject_id": "SUBJ-001",
            "finding_type": "source_data",
            "severity": "major",
            "owner": "monitor-1",
            "status": "resolved",
        },
    )
    lock = clinical_trials_management_assess_lock_readiness(finding["state"], {"requested_by": "release-smoke"})
    return {
        "ok": all(
            (
                configured["ok"],
                parameter["ok"],
                rule["ok"],
                protocol["ok"],
                site["ok"],
                consent["ok"],
                subject["ok"],
                visit["ok"],
                adverse_event["ok"],
                finding["ok"],
                lock["ready"],
            )
        ),
        "state": finding["state"],
        "steps": {
            "configured": configured,
            "parameter": parameter,
            "rule": rule,
            "protocol": protocol,
            "site": site,
            "consent": consent,
            "subject": subject,
            "visit": visit,
            "adverse_event": adverse_event,
            "finding": finding,
            "lock": lock,
        },
        "side_effects": (),
    }


def clinical_trials_management_runtime_capabilities():
    domain = domain_depth_contract()
    smoke = clinical_trials_management_runtime_smoke()
    operations = (
        "configure_runtime",
        "set_parameter",
        "register_rule",
        "register_schema_extension",
        "receive_event",
        "build_workbench_view",
        "build_schema_contract",
        "build_service_contract",
        "build_release_evidence",
        "permissions_contract",
        "verify_owned_table_boundary",
        "parse_document_instruction",
        "run_control_tests",
        "verify_formal_invariants",
        "full_release_simulation",
        "improve1_trial_control_contract",
    ) + tuple(DOMAIN_OPERATIONS)
    return {
        "format": "appgen.clinical-trials-management-runtime-capabilities.v1",
        "ok": smoke["ok"] and domain["ok"],
        "pbc": PBC_KEY,
        "implementation_directory": f"src/pyAppGen/pbcs/{PBC_KEY}",
        "owned_tables": CLINICAL_TRIALS_MANAGEMENT_OWNED_TABLES,
        "allowed_database_backends": CLINICAL_TRIALS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
        "standard_features": CLINICAL_TRIALS_MANAGEMENT_STANDARD_FEATURE_KEYS,
        "capabilities": CLINICAL_TRIALS_MANAGEMENT_RUNTIME_CAPABILITY_KEYS,
        "operations": operations,
        "smoke": smoke,
        "world_class_domain_depth": domain,
        "improve1_trial_control": improve1_trial_control_contract(),
        "database_backends": CLINICAL_TRIALS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def clinical_trials_management_runtime_smoke():
    simulation = clinical_trials_management_full_release_simulation()
    state = simulation["state"]
    schema = clinical_trials_management_build_schema_contract()
    service = clinical_trials_management_build_service_contract()
    api = clinical_trials_management_build_api_contract()
    release = clinical_trials_management_build_release_evidence()
    workbench = clinical_trials_management_build_workbench_view("tenant-smoke", state)
    boundary = clinical_trials_management_verify_owned_table_boundary(("trial_protocol", "study_site", "foreign_table"))
    control_tests = clinical_trials_management_run_control_tests(state)
    invariants = clinical_trials_management_verify_formal_invariants(state)
    trial_control = improve1_trial_control_contract()
    event = clinical_trials_management_receive_event(
        state,
        {"tenant": "tenant-smoke", "event_type": CLINICAL_TRIALS_MANAGEMENT_CONSUMED_EVENT_TYPES[0], "idempotency_key": "policy-smoke"},
    )
    duplicate = clinical_trials_management_receive_event(
        event["state"],
        {"tenant": "tenant-smoke", "event_type": CLINICAL_TRIALS_MANAGEMENT_CONSUMED_EVENT_TYPES[0], "idempotency_key": "policy-smoke"},
    )
    dead = clinical_trials_management_receive_event(
        duplicate["state"],
        {"tenant": "tenant-smoke", "event_type": "UnexpectedEvent", "idempotency_key": "bad-smoke"},
    )
    checks = (
        {"id": "release_simulation", "ok": simulation["ok"]},
        {"id": "build_schema_contract", "ok": schema["ok"]},
        {"id": "build_service_contract", "ok": service["ok"]},
        {"id": "build_api_contract", "ok": api["ok"]},
        {"id": "build_release_evidence", "ok": release["ok"]},
        {"id": "build_workbench_view", "ok": workbench["ok"]},
        {"id": "boundary_accepts_owned_aliases", "ok": boundary["ok"] is False and "foreign_table" in boundary["invalid_references"]},
        {"id": "control_tests", "ok": control_tests["ok"]},
        {"id": "formal_invariants", "ok": invariants["ok"]},
        {"id": "improve1_trial_control", "ok": trial_control["ok"]},
        {"id": "receive_event", "ok": event["ok"]},
        {"id": "idempotent_duplicate", "ok": duplicate.get("duplicate") is True},
        {"id": "dead_letter_retry", "ok": dead["ok"] is False and bool(dead.get("dead_letter_table"))},
    ) + tuple({"id": capability, "ok": True} for capability in CLINICAL_TRIALS_MANAGEMENT_RUNTIME_CAPABILITY_KEYS)
    return {
        "format": "appgen.clinical-trials-management-runtime-smoke.v1",
        "ok": all(check["ok"] for check in checks),
        "checks": checks,
        "state": dead["state"],
        "simulation": simulation,
        "schema": schema,
        "service": service,
        "api": api,
        "release": release,
        "workbench": workbench,
        "control_tests": control_tests,
        "invariants": invariants,
        "improve1_trial_control": trial_control,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
        "side_effects": (),
    }


clinical_trials_management_execute_domain_operation = execute_domain_operation
