"""Package-local guided wizards for the Nonprofit Program Impact workbench."""

from __future__ import annotations

from .forms import nonprofit_program_impact_form_catalog


PBC_KEY = "nonprofit_program_impact"


NONPROFIT_PROGRAM_IMPACT_WIZARDS = (
    {
        "wizard_id": "program_design_to_baseline",
        "title": "Program design to baseline",
        "goal": "Define theory of change, beneficiary targeting, and initial targets before delivery starts.",
        "steps": (
            {"step_id": "define_program", "label": "Define program portfolio", "form_id": "program_portfolio_setup", "operation": "create_program"},
            {"step_id": "enroll_anchor_cohort", "label": "Enroll anchor cohort", "form_id": "beneficiary_enrollment", "operation": "enroll_beneficiary"},
            {"step_id": "record_baseline", "label": "Record baseline outcome", "form_id": "outcome_follow_up", "operation": "record_outcome_observation"},
        ),
    },
    {
        "wizard_id": "beneficiary_service_journey",
        "title": "Beneficiary service journey",
        "goal": "Take one beneficiary from eligibility and consent through service delivery and follow-up.",
        "steps": (
            {"step_id": "enroll_beneficiary", "label": "Enroll beneficiary", "form_id": "beneficiary_enrollment", "operation": "enroll_beneficiary"},
            {"step_id": "record_service", "label": "Record service delivery", "form_id": "service_delivery_capture", "operation": "record_service_episode"},
            {"step_id": "observe_outcome", "label": "Observe outcome", "form_id": "outcome_follow_up", "operation": "record_outcome_observation"},
        ),
    },
    {
        "wizard_id": "donor_reporting_cycle",
        "title": "Donor reporting cycle",
        "goal": "Move from verified outcomes and evidence into a frozen donor report.",
        "steps": (
            {"step_id": "refresh_outcomes", "label": "Refresh outcome window", "form_id": "outcome_follow_up", "operation": "record_outcome_observation"},
            {"step_id": "quality_check", "label": "Preview assistant narrative", "form_id": "assistant_document_intake", "operation": "assistant_preview"},
            {"step_id": "freeze_report", "label": "Freeze donor report", "form_id": "donor_report_freeze", "operation": "freeze_donor_report"},
        ),
    },
    {
        "wizard_id": "assistant_change_preview",
        "title": "Assistant-guided change preview",
        "goal": "Turn a narrative memo into a bounded preview before any governed mutation.",
        "steps": (
            {"step_id": "capture_document", "label": "Capture narrative", "form_id": "assistant_document_intake", "operation": "assistant_preview"},
            {"step_id": "review_boundary", "label": "Review owned-table boundary", "form_id": "assistant_document_intake", "operation": "assistant_preview"},
            {"step_id": "confirm_governance", "label": "Confirm governed action", "form_id": "assistant_document_intake", "operation": "assistant_preview"},
        ),
    },
)


def nonprofit_program_impact_wizard_catalog() -> dict:
    """Return the guided wizard registry for this PBC."""
    forms = nonprofit_program_impact_form_catalog()
    form_ids = set(forms["form_ids"])
    missing_form_bindings = tuple(
        f"{wizard['wizard_id']}:{step['step_id']}"
        for wizard in NONPROFIT_PROGRAM_IMPACT_WIZARDS
        for step in wizard["steps"]
        if step["form_id"] not in form_ids
    )
    return {
        "ok": bool(NONPROFIT_PROGRAM_IMPACT_WIZARDS) and not missing_form_bindings,
        "pbc": PBC_KEY,
        "wizards": NONPROFIT_PROGRAM_IMPACT_WIZARDS,
        "wizard_ids": tuple(item["wizard_id"] for item in NONPROFIT_PROGRAM_IMPACT_WIZARDS),
        "missing_form_bindings": missing_form_bindings,
        "side_effects": (),
    }


def nonprofit_program_impact_plan_wizard(wizard_id: str, context: dict | None = None) -> dict:
    """Return a guided step plan with lightweight readiness hints."""
    wizard = next((item for item in NONPROFIT_PROGRAM_IMPACT_WIZARDS if item["wizard_id"] == wizard_id), None)
    if wizard is None:
        return {"ok": False, "reason": "unknown_wizard", "wizard_id": wizard_id, "side_effects": ()}

    supplied = dict(context or {})
    planned_steps = []
    for position, step in enumerate(wizard["steps"], start=1):
        blocked_by = ()
        if wizard_id == "program_design_to_baseline" and step["step_id"] != "define_program" and not supplied.get("program_id"):
            blocked_by = ("program_id",)
        if wizard_id == "beneficiary_service_journey":
            if step["step_id"] != "enroll_beneficiary" and not supplied.get("beneficiary_id"):
                blocked_by = ("beneficiary_id",)
            if step["step_id"] == "observe_outcome" and not supplied.get("episode_id"):
                blocked_by = tuple(dict.fromkeys(blocked_by + ("episode_id",)))
        if wizard_id == "donor_reporting_cycle":
            if step["step_id"] == "refresh_outcomes" and not supplied.get("program_id"):
                blocked_by = ("program_id",)
            if step["step_id"] == "freeze_report" and not supplied.get("report_id"):
                blocked_by = tuple(dict.fromkeys(blocked_by + ("report_id",)))
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
        "pbc": PBC_KEY,
        "wizard_id": wizard_id,
        "goal": wizard["goal"],
        "steps": tuple(planned_steps),
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Exercise wizard catalog and a plan."""
    catalog = nonprofit_program_impact_wizard_catalog()
    plan = nonprofit_program_impact_plan_wizard(
        "donor_reporting_cycle",
        {"program_id": "PROGRAM-001", "report_id": "REPORT-001"},
    )
    return {
        "ok": catalog["ok"] and plan["ok"] and bool(plan["steps"]),
        "catalog": catalog,
        "plan": plan,
        "side_effects": (),
    }
