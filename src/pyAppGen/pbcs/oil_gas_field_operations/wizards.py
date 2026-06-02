"""Package-local guided wizards for the Oil and Gas Field Operations workbench."""

from __future__ import annotations

from .forms import oil_gas_field_operations_form_catalog


OIL_GAS_FIELD_OPERATIONS_WIZARDS = (
    {
        "wizard_id": "pad_startup_and_surveillance",
        "title": "Pad startup and surveillance",
        "goal": "Bring a route or pad online with well hierarchy, production, and ticket coverage.",
        "steps": (
            {"step_id": "register_well", "label": "Register well hierarchy", "form_id": "well_hierarchy_intake", "operation": "create_well"},
            {"step_id": "capture_day", "label": "Capture daily production", "form_id": "daily_production_capture", "operation": "record_production_reading"},
            {"step_id": "open_ticket", "label": "Open field ticket if required", "form_id": "field_ticket_triage", "operation": "review_field_ticket"},
        ),
    },
    {
        "wizard_id": "morning_production_review",
        "title": "Morning production review",
        "goal": "Summarize deferred production, invalid tests, integrity issues, and high-priority field tickets by route.",
        "steps": (
            {"step_id": "refresh_day", "label": "Refresh daily capture", "form_id": "daily_production_capture", "operation": "record_production_reading"},
            {"step_id": "review_exceptions", "label": "Inspect field exceptions", "form_id": "field_ticket_triage", "operation": "review_field_ticket"},
            {"step_id": "generate_brief", "label": "Generate morning brief", "form_id": "morning_review_request", "operation": "query_oil_gas_field_operations_assistant_preview"},
        ),
    },
    {
        "wizard_id": "workover_readiness",
        "title": "Workover readiness",
        "goal": "Assemble a workover pack with decline evidence, lift failure mode, permits, and barrier status.",
        "steps": (
            {"step_id": "capture_decline", "label": "Capture latest production", "form_id": "daily_production_capture", "operation": "record_production_reading"},
            {"step_id": "capture_ticket", "label": "Capture failure evidence", "form_id": "field_ticket_triage", "operation": "review_field_ticket"},
            {"step_id": "prepare_pack", "label": "Prepare workover pack", "form_id": "workover_readiness_pack", "operation": "approve_workover_plan"},
        ),
    },
    {
        "wizard_id": "hse_boundary_response",
        "title": "HSE boundary response",
        "goal": "Log, contain, and escalate reportable field HSE events without losing route context.",
        "steps": (
            {"step_id": "log_event", "label": "Log HSE event", "form_id": "hse_boundary_event", "operation": "simulate_hse_event"},
            {"step_id": "triage_ticket", "label": "Open linked field ticket", "form_id": "field_ticket_triage", "operation": "review_field_ticket"},
            {"step_id": "confirm_controls", "label": "Confirm operational controls", "form_id": "morning_review_request", "operation": "query_oil_gas_field_operations_controls"},
        ),
    },
    {
        "wizard_id": "release_readiness",
        "title": "Release readiness",
        "goal": "Review package-local controls, docs, routes, and assistant guardrails before release.",
        "steps": (
            {"step_id": "inspect_controls", "label": "Inspect controls", "form_id": "morning_review_request", "operation": "query_oil_gas_field_operations_controls"},
            {"step_id": "inspect_routes", "label": "Inspect app surface", "form_id": "morning_review_request", "operation": "query_workbench"},
            {"step_id": "inspect_assistant", "label": "Inspect assistant preview", "form_id": "morning_review_request", "operation": "query_oil_gas_field_operations_assistant_preview"},
        ),
    },
)


def oil_gas_field_operations_wizard_catalog() -> dict:
    """Return the guided wizard registry for this PBC."""
    forms = oil_gas_field_operations_form_catalog()
    form_ids = set(forms["form_ids"])
    missing_form_bindings = tuple(
        f"{wizard['wizard_id']}:{step['step_id']}"
        for wizard in OIL_GAS_FIELD_OPERATIONS_WIZARDS
        for step in wizard["steps"]
        if step["form_id"] not in form_ids
    )
    return {
        "ok": bool(OIL_GAS_FIELD_OPERATIONS_WIZARDS) and not missing_form_bindings,
        "pbc": "oil_gas_field_operations",
        "wizards": OIL_GAS_FIELD_OPERATIONS_WIZARDS,
        "wizard_ids": tuple(item["wizard_id"] for item in OIL_GAS_FIELD_OPERATIONS_WIZARDS),
        "missing_form_bindings": missing_form_bindings,
        "side_effects": (),
    }


def oil_gas_field_operations_plan_wizard(wizard_id: str, context: dict | None = None) -> dict:
    """Return a guided step plan with lightweight readiness hints."""
    wizard = next((item for item in OIL_GAS_FIELD_OPERATIONS_WIZARDS if item["wizard_id"] == wizard_id), None)
    if wizard is None:
        return {"ok": False, "reason": "unknown_wizard", "wizard_id": wizard_id, "side_effects": ()}

    supplied = dict(context or {})
    planned_steps = []
    for position, step in enumerate(wizard["steps"], start=1):
        blocked_by = ()
        if wizard_id in {"morning_production_review", "workover_readiness", "hse_boundary_response"} and position > 1 and not supplied.get("well_id"):
            blocked_by = ("well_id",)
        if wizard_id == "morning_production_review" and step["step_id"] == "generate_brief" and not supplied.get("production_date"):
            blocked_by = ("production_date",)
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
        "pbc": "oil_gas_field_operations",
        "wizard_id": wizard_id,
        "goal": wizard["goal"],
        "steps": tuple(planned_steps),
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Exercise wizard catalog and a plan."""
    catalog = oil_gas_field_operations_wizard_catalog()
    plan = oil_gas_field_operations_plan_wizard(
        "morning_production_review",
        {"well_id": "WELL-7H", "production_date": "2026-05-29"},
    )
    return {
        "ok": catalog["ok"] and plan["ok"] and bool(plan["steps"]),
        "catalog": catalog,
        "plan": plan,
        "side_effects": (),
    }
