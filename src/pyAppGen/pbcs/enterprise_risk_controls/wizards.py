"""Package-local guided wizards for the Enterprise Risk Controls workbench."""

from __future__ import annotations

from .forms import enterprise_risk_controls_form_catalog


ENTERPRISE_RISK_CONTROLS_WIZARDS = (
    {
        "wizard_id": "risk_intake",
        "title": "Risk intake and treatment",
        "goal": "Take a risk from registration through assessment and initial control design.",
        "steps": (
            {
                "step_id": "register_risk",
                "label": "Register risk",
                "form_id": "risk_registration",
                "operation": "register_risk",
            },
            {
                "step_id": "assess_risk",
                "label": "Assess posture",
                "form_id": "risk_assessment",
                "operation": "assess_inherent_risk",
            },
            {
                "step_id": "define_control",
                "label": "Define control",
                "form_id": "control_definition",
                "operation": "define_control",
            },
        ),
    },
    {
        "wizard_id": "control_gap_response",
        "title": "Control gap response",
        "goal": "Respond to a failed or weak control with testing, attestation, and remediation.",
        "steps": (
            {
                "step_id": "schedule_test",
                "label": "Schedule test",
                "form_id": "control_test_plan",
                "operation": "schedule_control_test",
            },
            {
                "step_id": "record_attestation",
                "label": "Capture attestation",
                "form_id": "attestation_campaign",
                "operation": "record_attestation",
            },
            {
                "step_id": "open_remediation",
                "label": "Open remediation",
                "form_id": "remediation_issue",
                "operation": "open_remediation",
            },
        ),
    },
    {
        "wizard_id": "committee_readout",
        "title": "Committee readout",
        "goal": "Prepare evidence and decision material for risk committee review.",
        "steps": (
            {
                "step_id": "refresh_assessment",
                "label": "Refresh assessment",
                "form_id": "risk_assessment",
                "operation": "assess_inherent_risk",
            },
            {
                "step_id": "refresh_attestation",
                "label": "Refresh attestation",
                "form_id": "attestation_campaign",
                "operation": "record_attestation",
            },
            {
                "step_id": "assemble_packet",
                "label": "Assemble assurance packet",
                "form_id": "assurance_packet",
                "operation": "generate_assurance_packet",
            },
        ),
    },
    {
        "wizard_id": "assistant_change_preview",
        "title": "Assistant-guided change preview",
        "goal": "Turn an uploaded policy note or audit instruction into a preview-only CRUD plan.",
        "steps": (
            {
                "step_id": "capture_document",
                "label": "Capture document",
                "form_id": "document_instruction_intake",
                "operation": "query_enterprise_risk_controls_assistant_preview",
            },
            {
                "step_id": "review_controls",
                "label": "Review controls",
                "form_id": "document_instruction_intake",
                "operation": "query_enterprise_risk_controls_controls",
            },
            {
                "step_id": "review_preview",
                "label": "Review mutation preview",
                "form_id": "document_instruction_intake",
                "operation": "query_enterprise_risk_controls_assistant_preview",
            },
        ),
    },
)


def enterprise_risk_controls_wizard_catalog() -> dict:
    """Return the guided wizard registry for this PBC."""
    forms = enterprise_risk_controls_form_catalog()
    form_ids = set(forms["form_ids"])
    missing_form_bindings = tuple(
        f"{wizard['wizard_id']}:{step['step_id']}"
        for wizard in ENTERPRISE_RISK_CONTROLS_WIZARDS
        for step in wizard["steps"]
        if step["form_id"] not in form_ids
    )
    return {
        "ok": bool(ENTERPRISE_RISK_CONTROLS_WIZARDS) and not missing_form_bindings,
        "pbc": "enterprise_risk_controls",
        "wizards": ENTERPRISE_RISK_CONTROLS_WIZARDS,
        "wizard_ids": tuple(item["wizard_id"] for item in ENTERPRISE_RISK_CONTROLS_WIZARDS),
        "missing_form_bindings": missing_form_bindings,
        "side_effects": (),
    }


def enterprise_risk_controls_plan_wizard(wizard_id: str, context: dict | None = None) -> dict:
    """Return a guided step plan with lightweight readiness hints."""
    wizard = next((item for item in ENTERPRISE_RISK_CONTROLS_WIZARDS if item["wizard_id"] == wizard_id), None)
    if wizard is None:
        return {"ok": False, "reason": "unknown_wizard", "wizard_id": wizard_id, "side_effects": ()}

    supplied = dict(context or {})
    planned_steps = []
    for position, step in enumerate(wizard["steps"], start=1):
        blocked_by = ()
        if wizard_id == "risk_intake" and step["step_id"] != "register_risk" and not supplied.get("risk_code"):
            blocked_by = ("risk_code",)
        if wizard_id == "control_gap_response" and step["step_id"] != "schedule_test" and not supplied.get("control_code"):
            blocked_by = ("control_code",)
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
        "pbc": "enterprise_risk_controls",
        "wizard_id": wizard_id,
        "goal": wizard["goal"],
        "steps": tuple(planned_steps),
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Exercise wizard catalog and a plan."""
    catalog = enterprise_risk_controls_wizard_catalog()
    plan = enterprise_risk_controls_plan_wizard("assistant_change_preview", {"risk_code": "RISK-100"})
    return {
        "ok": catalog["ok"] and plan["ok"] and bool(plan["steps"]),
        "catalog": catalog,
        "plan": plan,
        "side_effects": (),
    }
