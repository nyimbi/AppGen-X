"""Package-local forms for the Clinical Trials Management workbench."""

from __future__ import annotations


CLINICAL_TRIALS_MANAGEMENT_FORM_DEFINITIONS = (
    {
        "form_id": "protocol_amendment_intake",
        "title": "Register protocol or amendment",
        "route": "POST /api/pbc/clinical_trials_management/trial-protocols",
        "operation": "command_trial_protocols",
        "permission": "clinical_trials_management.protocol_admin",
        "owned_tables": ("clinical_trials_management_trial_protocol",),
        "fields": (
            {"name": "tenant", "type": "string", "required": True},
            {"name": "protocol_id", "type": "string", "required": True},
            {"name": "protocol_code", "type": "string", "required": True},
            {"name": "version", "type": "integer", "required": True},
            {
                "name": "status",
                "type": "enum",
                "required": True,
                "choices": ("draft", "approved", "active", "amended", "closed"),
            },
            {"name": "phase", "type": "enum", "required": True, "choices": ("I", "II", "III", "IV")},
            {"name": "amendment_reason", "type": "string", "required": False},
        ),
    },
    {
        "form_id": "site_activation_review",
        "title": "Activate study site",
        "route": "POST /api/pbc/clinical_trials_management/study-sites",
        "operation": "command_study_sites",
        "permission": "clinical_trials_management.site_activation",
        "owned_tables": ("clinical_trials_management_study_site",),
        "fields": (
            {"name": "tenant", "type": "string", "required": True},
            {"name": "site_id", "type": "string", "required": True},
            {"name": "protocol_id", "type": "string", "required": True},
            {"name": "site_number", "type": "string", "required": True},
            {"name": "country", "type": "string", "required": True},
            {"name": "principal_investigator", "type": "string", "required": True},
            {"name": "ethics_approval", "type": "boolean", "required": True},
            {"name": "contract_executed", "type": "boolean", "required": True},
            {"name": "training_complete", "type": "boolean", "required": True},
            {"name": "delegation_log_ready", "type": "boolean", "required": True},
        ),
    },
    {
        "form_id": "subject_screening_and_enrollment",
        "title": "Screen and enroll subject",
        "route": "POST /api/pbc/clinical_trials_management/subjects",
        "operation": "command_subjects",
        "permission": "clinical_trials_management.subject_enrollment",
        "owned_tables": ("clinical_trials_management_subject",),
        "fields": (
            {"name": "tenant", "type": "string", "required": True},
            {"name": "subject_id", "type": "string", "required": True},
            {"name": "protocol_id", "type": "string", "required": True},
            {"name": "site_id", "type": "string", "required": True},
            {"name": "screening_number", "type": "string", "required": True},
            {"name": "eligibility_evidence_complete", "type": "boolean", "required": True},
            {"name": "exclusion_clear", "type": "boolean", "required": True},
            {"name": "consent_id", "type": "string", "required": False},
            {"name": "enrollment_requested", "type": "boolean", "required": True},
        ),
    },
    {
        "form_id": "consent_recording",
        "title": "Record informed consent",
        "route": "POST /api/pbc/clinical_trials_management/consent-records",
        "operation": "command_consent_records",
        "permission": "clinical_trials_management.consent_manage",
        "owned_tables": ("clinical_trials_management_consent_record",),
        "fields": (
            {"name": "tenant", "type": "string", "required": True},
            {"name": "consent_id", "type": "string", "required": True},
            {"name": "subject_id", "type": "string", "required": True},
            {"name": "protocol_id", "type": "string", "required": True},
            {"name": "site_id", "type": "string", "required": True},
            {"name": "consent_version", "type": "integer", "required": True},
            {"name": "language", "type": "string", "required": True},
            {
                "name": "status",
                "type": "enum",
                "required": True,
                "choices": ("current", "withdrawn", "expired"),
            },
            {"name": "signed_on", "type": "string", "required": True},
        ),
    },
    {
        "form_id": "visit_readiness",
        "title": "Schedule or complete visit",
        "route": "POST /api/pbc/clinical_trials_management/visit-schedules",
        "operation": "command_visit_schedules",
        "permission": "clinical_trials_management.visit_manage",
        "owned_tables": ("clinical_trials_management_visit_schedule",),
        "fields": (
            {"name": "tenant", "type": "string", "required": True},
            {"name": "visit_id", "type": "string", "required": True},
            {"name": "subject_id", "type": "string", "required": True},
            {"name": "protocol_id", "type": "string", "required": True},
            {"name": "site_id", "type": "string", "required": True},
            {"name": "visit_code", "type": "string", "required": True},
            {
                "name": "visit_type",
                "type": "enum",
                "required": True,
                "choices": ("screening", "baseline", "treatment", "follow_up", "end_of_study"),
            },
            {"name": "target_day", "type": "integer", "required": True},
            {"name": "actual_day", "type": "integer", "required": False},
        ),
    },
    {
        "form_id": "serious_event_reporting",
        "title": "Report adverse event",
        "route": "POST /api/pbc/clinical_trials_management/adverse-events",
        "operation": "command_adverse_events",
        "permission": "clinical_trials_management.safety_review",
        "owned_tables": ("clinical_trials_management_adverse_event",),
        "fields": (
            {"name": "tenant", "type": "string", "required": True},
            {"name": "adverse_event_id", "type": "string", "required": True},
            {"name": "subject_id", "type": "string", "required": True},
            {"name": "protocol_id", "type": "string", "required": True},
            {"name": "site_id", "type": "string", "required": True},
            {
                "name": "seriousness",
                "type": "enum",
                "required": True,
                "choices": ("non_serious", "serious"),
            },
            {"name": "grade", "type": "enum", "required": True, "choices": ("1", "2", "3", "4", "5")},
            {
                "name": "expectedness",
                "type": "enum",
                "required": True,
                "choices": ("expected", "unexpected"),
            },
            {"name": "reported_within_hours", "type": "integer", "required": False},
        ),
    },
    {
        "form_id": "monitoring_finding_intake",
        "title": "Open monitoring finding",
        "route": "POST /api/pbc/clinical_trials_management/monitoring-findings",
        "operation": "command_monitoring_findings",
        "permission": "clinical_trials_management.monitoring_manage",
        "owned_tables": ("clinical_trials_management_monitoring_finding",),
        "fields": (
            {"name": "tenant", "type": "string", "required": True},
            {"name": "finding_id", "type": "string", "required": True},
            {"name": "protocol_id", "type": "string", "required": True},
            {"name": "site_id", "type": "string", "required": True},
            {
                "name": "severity",
                "type": "enum",
                "required": True,
                "choices": ("minor", "major", "critical"),
            },
            {
                "name": "finding_type",
                "type": "enum",
                "required": True,
                "choices": ("consent", "eligibility", "source_data", "drug_accountability", "safety"),
            },
            {"name": "owner", "type": "string", "required": True},
        ),
    },
    {
        "form_id": "policy_rule_editor",
        "title": "Update trial policy rule",
        "route": "POST /api/pbc/clinical_trials_management/policy-rules",
        "operation": "command_policy_rules",
        "permission": "clinical_trials_management.configure",
        "owned_tables": ("clinical_trials_management_clinical_trials_management_policy_rule",),
        "fields": (
            {"name": "tenant", "type": "string", "required": True},
            {"name": "rule_id", "type": "string", "required": True},
            {
                "name": "rule_type",
                "type": "enum",
                "required": True,
                "choices": ("protocol_gate", "site_activation", "consent", "eligibility", "safety", "privacy"),
            },
            {"name": "condition", "type": "string", "required": True},
            {"name": "status", "type": "enum", "required": True, "choices": ("draft", "active", "retired")},
        ),
    },
    {
        "form_id": "runtime_parameter_editor",
        "title": "Update trial runtime parameter",
        "route": "POST /api/pbc/clinical_trials_management/runtime-parameters",
        "operation": "command_runtime_parameters",
        "permission": "clinical_trials_management.configure",
        "owned_tables": ("clinical_trials_management_clinical_trials_management_runtime_parameter",),
        "fields": (
            {"name": "tenant", "type": "string", "required": True},
            {
                "name": "name",
                "type": "enum",
                "required": True,
                "choices": (
                    "screening_window_days",
                    "visit_window_grace_days",
                    "serious_event_reporting_hours",
                    "monitoring_followup_days",
                    "reconsent_notice_days",
                    "workbench_limit",
                ),
            },
            {"name": "value", "type": "integer", "required": True},
        ),
    },
    {
        "form_id": "document_instruction_intake",
        "title": "Assistant document intake",
        "route": "POST /api/pbc/clinical_trials_management/assistant/document-preview",
        "operation": "query_clinical_trials_management_assistant_preview",
        "permission": "clinical_trials_management.audit",
        "owned_tables": (
            "clinical_trials_management_trial_protocol",
            "clinical_trials_management_study_site",
            "clinical_trials_management_subject",
            "clinical_trials_management_consent_record",
            "clinical_trials_management_visit_schedule",
            "clinical_trials_management_adverse_event",
            "clinical_trials_management_monitoring_finding",
            "clinical_trials_management_clinical_trials_management_policy_rule",
            "clinical_trials_management_clinical_trials_management_runtime_parameter",
        ),
        "fields": (
            {"name": "document_text", "type": "text", "required": True},
            {"name": "instructions", "type": "text", "required": True},
            {
                "name": "target_entity",
                "type": "enum",
                "required": True,
                "choices": (
                    "trial_protocol",
                    "study_site",
                    "subject",
                    "consent_record",
                    "visit_schedule",
                    "adverse_event",
                    "monitoring_finding",
                    "policy_rule",
                    "runtime_parameter",
                ),
            },
            {"name": "requested_action", "type": "enum", "required": True, "choices": ("create", "read", "update", "delete")},
        ),
    },
)


def clinical_trials_management_form_catalog() -> dict:
    """Return the package-local clinical trials form registry."""
    forms = tuple(CLINICAL_TRIALS_MANAGEMENT_FORM_DEFINITIONS)
    return {
        "ok": bool(forms),
        "pbc": "clinical_trials_management",
        "forms": forms,
        "form_ids": tuple(item["form_id"] for item in forms),
        "side_effects": (),
    }


def clinical_trials_management_get_form(form_id: str) -> dict:
    """Return one form definition by identifier."""
    form = next((item for item in CLINICAL_TRIALS_MANAGEMENT_FORM_DEFINITIONS if item["form_id"] == form_id), None)
    return {
        "ok": form is not None,
        "pbc": "clinical_trials_management",
        "form": form,
        "side_effects": (),
    }


def clinical_trials_management_validate_form_payload(form_id: str, payload: dict | None = None) -> dict:
    """Validate a clinical trials form payload against required fields and enum choices."""
    form = clinical_trials_management_get_form(form_id).get("form")
    if form is None:
        return {"ok": False, "accepted": False, "reason": "unknown_form", "form_id": form_id, "side_effects": ()}

    supplied = dict(payload or {})
    missing = tuple(
        field["name"]
        for field in form["fields"]
        if field.get("required") and supplied.get(field["name"]) in {None, ""}
    )
    invalid_choices = tuple(
        field["name"]
        for field in form["fields"]
        if field.get("type") == "enum"
        and supplied.get(field["name"]) not in {None, *field.get("choices", ())}
    )
    invalid_booleans = tuple(
        field["name"]
        for field in form["fields"]
        if field.get("type") == "boolean"
        and field["name"] in supplied
        and not isinstance(supplied[field["name"]], bool)
    )
    return {
        "ok": not missing and not invalid_choices and not invalid_booleans,
        "accepted": not missing and not invalid_choices and not invalid_booleans,
        "pbc": "clinical_trials_management",
        "form_id": form_id,
        "missing": missing,
        "invalid_choices": invalid_choices,
        "invalid_booleans": invalid_booleans,
        "payload_keys": tuple(sorted(supplied)),
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Exercise one happy-path form validation."""
    catalog = clinical_trials_management_form_catalog()
    validation = clinical_trials_management_validate_form_payload(
        "document_instruction_intake",
        {
            "document_text": "Amendment memo: protocol version 3 requires re-consent before Visit 4.",
            "instructions": "Update the protocol record and list impacted consents.",
            "target_entity": "trial_protocol",
            "requested_action": "update",
        },
    )
    return {
        "ok": catalog["ok"] and validation["ok"],
        "catalog": catalog,
        "validation": validation,
        "side_effects": (),
    }
