"""Package-local guided wizards for the Professional Services Automation workbench."""

from __future__ import annotations

from .forms import professional_services_automation_form_catalog


PROFESSIONAL_SERVICES_AUTOMATION_WIZARDS = (
    {
        "wizard_id": "engagement_launch",
        "title": "Launch engagement",
        "goal": "Take a new engagement from intake through SOW grounding and staffing readiness.",
        "permission": "professional_services_automation.create",
        "steps": (
            {
                "step_id": "intake_engagement",
                "label": "Capture engagement",
                "form_id": "engagement_intake",
                "operation": "create_engagement",
            },
            {
                "step_id": "ground_sow",
                "label": "Parse SOW",
                "form_id": "sow_semantic_intake",
                "operation": "register_statement_of_work",
            },
            {
                "step_id": "prepare_staffing",
                "label": "Open staffing request",
                "form_id": "staffing_request",
                "operation": "open_staffing_request",
            },
        ),
    },
    {
        "wizard_id": "margin_recovery",
        "title": "Recover margin leakage",
        "goal": "Review time, scope, and billing blockers before margin degrades further.",
        "permission": "professional_services_automation.approve",
        "steps": (
            {
                "step_id": "review_time",
                "label": "Review time and expense",
                "form_id": "time_and_expense_review",
                "operation": "capture_time_entry",
            },
            {
                "step_id": "run_gate",
                "label": "Run billing gate",
                "form_id": "billing_readiness_gate",
                "operation": "run_billing_readiness",
            },
            {
                "step_id": "simulate_leakage",
                "label": "Simulate leakage",
                "form_id": "billing_readiness_gate",
                "operation": "simulate_margin_leakage",
            },
        ),
    },
    {
        "wizard_id": "delivery_risk_triage",
        "title": "Delivery risk triage",
        "goal": "Assess delivery risk and route remediation before milestone or acceptance failures occur.",
        "permission": "professional_services_automation.update",
        "steps": (
            {
                "step_id": "inspect_staffing",
                "label": "Inspect staffing gaps",
                "form_id": "staffing_request",
                "operation": "assign_staff",
            },
            {
                "step_id": "check_acceptance",
                "label": "Check billing and acceptance",
                "form_id": "billing_readiness_gate",
                "operation": "record_client_acceptance",
            },
            {
                "step_id": "score_risk",
                "label": "Score delivery risk",
                "form_id": "time_and_expense_review",
                "operation": "score_delivery_risk",
            },
        ),
    },
    {
        "wizard_id": "assistant_change_preview",
        "title": "Assistant-guided change preview",
        "goal": "Turn a client note into a package-owned CRUD and change-control preview without mutating data.",
        "permission": "professional_services_automation.read",
        "steps": (
            {
                "step_id": "capture_document",
                "label": "Capture source note",
                "form_id": "document_instruction_preview",
                "operation": "parse_document_instruction",
            },
            {
                "step_id": "preview_crud",
                "label": "Preview CRUD plan",
                "form_id": "document_instruction_preview",
                "operation": "parse_document_instruction",
            },
            {
                "step_id": "route_change_control",
                "label": "Route change control",
                "form_id": "document_instruction_preview",
                "operation": "resolve_engagement_exception",
            },
        ),
    },
)



def professional_services_automation_wizard_catalog() -> dict:
    """Return the guided wizard registry for this PBC."""
    forms = professional_services_automation_form_catalog()
    form_ids = set(forms["form_ids"])
    missing_form_bindings = tuple(
        f"{wizard['wizard_id']}:{step['step_id']}"
        for wizard in PROFESSIONAL_SERVICES_AUTOMATION_WIZARDS
        for step in wizard["steps"]
        if step["form_id"] not in form_ids
    )
    return {
        "ok": bool(PROFESSIONAL_SERVICES_AUTOMATION_WIZARDS) and not missing_form_bindings,
        "pbc": "professional_services_automation",
        "wizards": PROFESSIONAL_SERVICES_AUTOMATION_WIZARDS,
        "wizard_ids": tuple(item["wizard_id"] for item in PROFESSIONAL_SERVICES_AUTOMATION_WIZARDS),
        "missing_form_bindings": missing_form_bindings,
        "side_effects": (),
    }



def professional_services_automation_plan_wizard(wizard_id: str, context: dict | None = None) -> dict:
    """Return a guided step plan with lightweight readiness hints."""
    wizard = next((item for item in PROFESSIONAL_SERVICES_AUTOMATION_WIZARDS if item["wizard_id"] == wizard_id), None)
    if wizard is None:
        return {"ok": False, "reason": "unknown_wizard", "wizard_id": wizard_id, "side_effects": ()}

    supplied = dict(context or {})
    planned_steps = []
    for position, step in enumerate(wizard["steps"], start=1):
        blocked_by = ()
        if step["step_id"] != "intake_engagement" and not supplied.get("engagement_id"):
            blocked_by = ("engagement_id",)
        if wizard_id == "margin_recovery" and step["step_id"] == "run_gate" and supplied.get("open_scope_exceptions", 0) > 0:
            blocked_by = ("open_scope_exceptions",)
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
        "pbc": "professional_services_automation",
        "wizard_id": wizard_id,
        "goal": wizard["goal"],
        "steps": tuple(planned_steps),
        "side_effects": (),
    }



def smoke_test() -> dict:
    """Exercise wizard catalog and a plan."""
    catalog = professional_services_automation_wizard_catalog()
    plan = professional_services_automation_plan_wizard(
        "assistant_change_preview",
        {"engagement_id": "eng_smoke", "open_scope_exceptions": 0},
    )
    return {
        "ok": catalog["ok"] and plan["ok"] and bool(plan["steps"]),
        "catalog": catalog,
        "plan": plan,
        "side_effects": (),
    }
