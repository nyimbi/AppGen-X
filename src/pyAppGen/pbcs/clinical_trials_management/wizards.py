"""Package-local guided wizards for the Clinical Trials Management workbench."""

from __future__ import annotations

from .forms import clinical_trials_management_form_catalog


CLINICAL_TRIALS_MANAGEMENT_WIZARDS = (
    {
        "wizard_id": "protocol_and_site_startup",
        "title": "Protocol and site startup",
        "goal": "Move an approved protocol to an active, activation-ready site.",
        "steps": (
            {"step_id": "register_protocol", "label": "Register or amend protocol", "form_id": "protocol_amendment_intake", "operation": "command_trial_protocols"},
            {"step_id": "tune_rules", "label": "Confirm trial rules", "form_id": "policy_rule_editor", "operation": "command_policy_rules"},
            {"step_id": "activate_site", "label": "Activate site", "form_id": "site_activation_review", "operation": "command_study_sites"},
        ),
    },
    {
        "wizard_id": "subject_enrollment",
        "title": "Subject enrollment",
        "goal": "Record consent, evaluate eligibility, and enroll without violating site or consent gates.",
        "steps": (
            {"step_id": "record_consent", "label": "Record consent", "form_id": "consent_recording", "operation": "command_consent_records"},
            {"step_id": "review_screening", "label": "Review screening packet", "form_id": "subject_screening_and_enrollment", "operation": "command_subjects"},
            {"step_id": "confirm_windows", "label": "Confirm visit windows", "form_id": "runtime_parameter_editor", "operation": "command_runtime_parameters"},
        ),
    },
    {
        "wizard_id": "visit_and_safety_follow_up",
        "title": "Visit and safety follow-up",
        "goal": "Close a visit, assess deviations, and handle safety escalation with audit evidence.",
        "steps": (
            {"step_id": "capture_visit", "label": "Capture visit readiness", "form_id": "visit_readiness", "operation": "command_visit_schedules"},
            {"step_id": "report_safety", "label": "Report adverse event", "form_id": "serious_event_reporting", "operation": "command_adverse_events"},
            {"step_id": "open_monitoring_issue", "label": "Open monitoring issue", "form_id": "monitoring_finding_intake", "operation": "command_monitoring_findings"},
        ),
    },
    {
        "wizard_id": "data_lock_readiness",
        "title": "Data lock readiness",
        "goal": "Inspect blockers before declaring the trial ready for lock.",
        "steps": (
            {"step_id": "inspect_controls", "label": "Inspect controls", "form_id": "document_instruction_intake", "operation": "query_clinical_trials_management_controls"},
            {"step_id": "review_lock_blockers", "label": "Review workbench blockers", "form_id": "document_instruction_intake", "operation": "query_clinical_trials_management_workbench"},
            {"step_id": "draft_remediation", "label": "Draft remediation plan", "form_id": "document_instruction_intake", "operation": "query_clinical_trials_management_assistant_preview"},
        ),
    },
    {
        "wizard_id": "assistant_change_preview",
        "title": "Assistant-guided change preview",
        "goal": "Turn a monitoring memo or protocol note into a governed CRUD preview.",
        "steps": (
            {"step_id": "capture_document", "label": "Capture document", "form_id": "document_instruction_intake", "operation": "query_clinical_trials_management_assistant_preview"},
            {"step_id": "review_permission", "label": "Review permission", "form_id": "document_instruction_intake", "operation": "query_clinical_trials_management_controls"},
            {"step_id": "review_mutation_preview", "label": "Review preview", "form_id": "document_instruction_intake", "operation": "query_clinical_trials_management_assistant_preview"},
        ),
    },
)


def clinical_trials_management_wizard_catalog() -> dict:
    """Return the guided wizard registry for this PBC."""
    forms = clinical_trials_management_form_catalog()
    form_ids = set(forms["form_ids"])
    missing_form_bindings = tuple(
        f"{wizard['wizard_id']}:{step['step_id']}"
        for wizard in CLINICAL_TRIALS_MANAGEMENT_WIZARDS
        for step in wizard["steps"]
        if step["form_id"] not in form_ids
    )
    return {
        "ok": bool(CLINICAL_TRIALS_MANAGEMENT_WIZARDS) and not missing_form_bindings,
        "pbc": "clinical_trials_management",
        "wizards": CLINICAL_TRIALS_MANAGEMENT_WIZARDS,
        "wizard_ids": tuple(item["wizard_id"] for item in CLINICAL_TRIALS_MANAGEMENT_WIZARDS),
        "missing_form_bindings": missing_form_bindings,
        "side_effects": (),
    }


def clinical_trials_management_plan_wizard(wizard_id: str, context: dict | None = None) -> dict:
    """Return a guided wizard plan with lightweight readiness hints."""
    wizard = next((item for item in CLINICAL_TRIALS_MANAGEMENT_WIZARDS if item["wizard_id"] == wizard_id), None)
    if wizard is None:
        return {"ok": False, "reason": "unknown_wizard", "wizard_id": wizard_id, "side_effects": ()}

    supplied = dict(context or {})
    planned_steps = []
    for position, step in enumerate(wizard["steps"], start=1):
        blocked_by = ()
        if wizard_id == "protocol_and_site_startup" and step["step_id"] == "activate_site" and not supplied.get("protocol_id"):
            blocked_by = ("protocol_id",)
        if wizard_id == "subject_enrollment" and step["step_id"] != "record_consent" and not supplied.get("site_id"):
            blocked_by = ("site_id",)
        if wizard_id == "visit_and_safety_follow_up" and step["step_id"] != "capture_visit" and not supplied.get("subject_id"):
            blocked_by = ("subject_id",)
        planned_steps.append(
            {
                **step,
                "position": position,
                "ready": not blocked_by,
                "blocked_by": blocked_by,
            }
        )
    return {
        "ok": True,
        "pbc": "clinical_trials_management",
        "wizard_id": wizard_id,
        "goal": wizard["goal"],
        "steps": tuple(planned_steps),
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Exercise wizard catalog and a guided plan."""
    catalog = clinical_trials_management_wizard_catalog()
    plan = clinical_trials_management_plan_wizard("subject_enrollment", {"site_id": "SITE-01"})
    return {
        "ok": catalog["ok"] and plan["ok"] and bool(plan["steps"]),
        "catalog": catalog,
        "plan": plan,
        "side_effects": (),
    }
