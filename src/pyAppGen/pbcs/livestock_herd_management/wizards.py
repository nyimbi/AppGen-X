"""Package-local guided wizards for the Livestock Herd Management standalone slice."""

from __future__ import annotations

from .forms import livestock_herd_management_form_catalog


PBC_KEY = "livestock_herd_management"


LIVESTOCK_HERD_MANAGEMENT_WIZARDS = (
    {
        "wizard_id": "new_arrival_onboarding",
        "title": "New arrival onboarding",
        "goal": "Register incoming livestock with traceability, quarantine, and herd-group placement evidence.",
        "steps": (
            {"step_id": "register_identity", "label": "Register identity", "form_id": "animal_registry_intake", "operation": "register_animal"},
            {"step_id": "open_quarantine", "label": "Open quarantine", "form_id": "movement_biosecurity_and_quarantine", "operation": "record_movement_and_biosecurity"},
            {"step_id": "assign_group", "label": "Assign herd group", "form_id": "herd_group_assignment", "operation": "assign_herd_group"},
            {"step_id": "seed_traceability", "label": "Seed traceability lot", "form_id": "movement_biosecurity_and_quarantine", "operation": "record_movement_and_biosecurity"},
        ),
    },
    {
        "wizard_id": "breed_to_calve",
        "title": "Breed to calve",
        "goal": "Capture breeding, pregnancy, calving, and offspring linkage with genetics evidence.",
        "steps": (
            {"step_id": "record_service", "label": "Record service", "form_id": "breeding_cycle", "operation": "record_breeding_cycle"},
            {"step_id": "confirm_pregnancy", "label": "Confirm pregnancy", "form_id": "breeding_cycle", "operation": "record_breeding_cycle"},
            {"step_id": "record_calving", "label": "Record calving", "form_id": "calving_and_offspring", "operation": "record_calving_event"},
            {"step_id": "review_welfare", "label": "Review dam welfare", "form_id": "welfare_mortality_and_yield", "operation": "record_welfare_and_yield"},
        ),
    },
    {
        "wizard_id": "health_campaign",
        "title": "Health campaign",
        "goal": "Coordinate treatments, vaccinations, withdrawal windows, and welfare interventions.",
        "steps": (
            {"step_id": "capture_case", "label": "Capture health case", "form_id": "health_treatment_and_vaccination", "operation": "record_health_intervention"},
            {"step_id": "apply_treatment", "label": "Apply treatment", "form_id": "health_treatment_and_vaccination", "operation": "record_health_intervention"},
            {"step_id": "schedule_booster", "label": "Schedule booster", "form_id": "health_treatment_and_vaccination", "operation": "record_health_intervention"},
            {"step_id": "review_release", "label": "Review withdrawal release", "form_id": "welfare_mortality_and_yield", "operation": "record_welfare_and_yield"},
        ),
    },
    {
        "wizard_id": "pasture_to_productivity",
        "title": "Pasture to productivity",
        "goal": "Balance feed, paddock usage, weights, and product yield for a herd cohort.",
        "steps": (
            {"step_id": "set_ration", "label": "Set ration", "form_id": "feed_and_grazing_plan", "operation": "record_feed_and_grazing_plan"},
            {"step_id": "assign_paddock", "label": "Assign paddock", "form_id": "feed_and_grazing_plan", "operation": "record_feed_and_grazing_plan"},
            {"step_id": "record_weight", "label": "Record weight", "form_id": "welfare_mortality_and_yield", "operation": "record_welfare_and_yield"},
            {"step_id": "record_yield", "label": "Record yield", "form_id": "welfare_mortality_and_yield", "operation": "record_welfare_and_yield"},
        ),
    },
    {
        "wizard_id": "movement_release",
        "title": "Movement release",
        "goal": "Approve a compliant move only after quarantine, biosecurity, and traceability checks pass.",
        "steps": (
            {"step_id": "check_biosecurity", "label": "Check biosecurity", "form_id": "movement_biosecurity_and_quarantine", "operation": "record_movement_and_biosecurity"},
            {"step_id": "verify_traceability", "label": "Verify traceability", "form_id": "movement_biosecurity_and_quarantine", "operation": "record_movement_and_biosecurity"},
            {"step_id": "issue_permit", "label": "Issue permit", "form_id": "movement_biosecurity_and_quarantine", "operation": "record_movement_and_biosecurity"},
        ),
    },
    {
        "wizard_id": "assistant_change_preview",
        "title": "Assistant-guided CRUD preview",
        "goal": "Translate livestock notes into bounded CRUD previews without mutating data.",
        "steps": (
            {"step_id": "capture_instruction", "label": "Capture instruction", "form_id": "assistant_change_preview", "operation": "assistant_crud_preview"},
            {"step_id": "review_boundary", "label": "Review owned boundary", "form_id": "assistant_change_preview", "operation": "assistant_crud_preview"},
            {"step_id": "review_confirmation", "label": "Review confirmation gate", "form_id": "assistant_change_preview", "operation": "assistant_crud_preview"},
        ),
    },
)


def livestock_herd_management_wizard_catalog() -> dict:
    """Return the guided standalone wizard registry for livestock workflows."""
    forms = livestock_herd_management_form_catalog()
    form_ids = set(forms["form_ids"])
    missing_form_bindings = tuple(
        f"{wizard['wizard_id']}:{step['step_id']}"
        for wizard in LIVESTOCK_HERD_MANAGEMENT_WIZARDS
        for step in wizard["steps"]
        if step["form_id"] not in form_ids
    )
    return {
        "ok": bool(LIVESTOCK_HERD_MANAGEMENT_WIZARDS) and not missing_form_bindings,
        "pbc": PBC_KEY,
        "wizards": LIVESTOCK_HERD_MANAGEMENT_WIZARDS,
        "wizard_ids": tuple(item["wizard_id"] for item in LIVESTOCK_HERD_MANAGEMENT_WIZARDS),
        "missing_form_bindings": missing_form_bindings,
        "side_effects": (),
    }


def livestock_herd_management_plan_wizard(wizard_id: str, context: dict | None = None) -> dict:
    """Return a guided wizard plan with simple livestock readiness gates."""
    wizard = next((item for item in LIVESTOCK_HERD_MANAGEMENT_WIZARDS if item["wizard_id"] == wizard_id), None)
    if wizard is None:
        return {"ok": False, "reason": "unknown_wizard", "wizard_id": wizard_id, "side_effects": ()}

    supplied = dict(context or {})
    planned_steps = []
    for position, step in enumerate(wizard["steps"], start=1):
        blocked_by = ()
        if wizard_id == "breed_to_calve" and step["step_id"] != "record_service" and not supplied.get("animal_id"):
            blocked_by = ("animal_id",)
        if wizard_id == "movement_release" and step["step_id"] == "issue_permit" and supplied.get("quarantine_status") == "open":
            blocked_by = ("quarantine_release",)
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
    """Exercise wizard catalog and a movement release plan."""
    catalog = livestock_herd_management_wizard_catalog()
    plan = livestock_herd_management_plan_wizard(
        "movement_release",
        {"animal_id": "cow-101", "quarantine_status": "released"},
    )
    return {
        "ok": catalog["ok"] and plan["ok"] and bool(plan["steps"]),
        "catalog": catalog,
        "plan": plan,
        "side_effects": (),
    }
