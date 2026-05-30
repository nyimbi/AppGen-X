"""Package-local guided wizards for the Mining Operations Management workbench."""

from __future__ import annotations

from .forms import mining_operations_management_form_catalog


PBC_KEY = "mining_operations_management"

MINING_OPERATIONS_MANAGEMENT_WIZARDS = (
    {
        "wizard_id": "weekly_plan_to_shift",
        "title": "Weekly plan to shift board",
        "goal": "Convert an approved plan hierarchy into a governed shift board with fleet readiness.",
        "steps": (
            {
                "step_id": "capture_plan_hierarchy",
                "label": "Capture plan hierarchy",
                "form_id": "mine_plan_hierarchy_intake",
                "operation": "create_mine_plan",
                "required_context": (),
            },
            {
                "step_id": "publish_shift_targets",
                "label": "Publish shift targets",
                "form_id": "shift_target_board",
                "operation": "review_extraction_shift",
                "required_context": ("plan_id",),
            },
            {
                "step_id": "confirm_fleet_boundary",
                "label": "Confirm fleet boundary",
                "form_id": "fleet_capability_card",
                "operation": "simulate_fleet_asset",
                "required_context": ("shift_id",),
            },
            {
                "step_id": "assign_dispatch_board",
                "label": "Assign dispatch board",
                "form_id": "dispatch_assignment",
                "operation": "approve_haulage_cycle",
                "required_context": ("shift_id", "fleet_asset_id"),
            },
        ),
    },
    {
        "wizard_id": "blast_clearance_gate",
        "title": "Blast clearance gate",
        "goal": "Prepare and release a drill-and-blast packet with geotechnical and re-entry checks.",
        "steps": (
            {
                "step_id": "capture_blast_packet",
                "label": "Capture blast packet",
                "form_id": "blast_readiness_packet",
                "operation": "record_pit_block",
                "required_context": (),
            },
            {
                "step_id": "review_geotech_restrictions",
                "label": "Review geotech restrictions",
                "form_id": "geotech_conditional_access",
                "operation": "review_mining_operations_management_policy_rule",
                "required_context": ("blast_packet_id",),
            },
            {
                "step_id": "handover_release_window",
                "label": "Handover release window",
                "form_id": "shift_handover_note",
                "operation": "create_mining_operations_management_control_assertion",
                "required_context": ("blast_packet_id", "shift_id"),
            },
        ),
    },
    {
        "wizard_id": "ore_to_plant_nomination",
        "title": "Ore to plant nomination",
        "goal": "Move boundary decisions into stockpile and plant-feed-ready evidence.",
        "steps": (
            {
                "step_id": "capture_boundary_call",
                "label": "Capture boundary call",
                "form_id": "ore_boundary_decision",
                "operation": "create_ore_quality",
                "required_context": (),
            },
            {
                "step_id": "record_stockpile_lineage",
                "label": "Record stockpile lineage",
                "form_id": "stockpile_movement",
                "operation": "record_stockpile",
                "required_context": ("boundary_decision_id",),
            },
            {
                "step_id": "handover_nomination_risk",
                "label": "Handover nomination risk",
                "form_id": "shift_handover_note",
                "operation": "create_mining_operations_management_control_assertion",
                "required_context": ("stockpile_id", "shift_id"),
            },
        ),
    },
    {
        "wizard_id": "wet_weather_dispatch_recovery",
        "title": "Wet-weather dispatch recovery",
        "goal": "Re-plan dispatch safely when weather, water, or ground conditions change.",
        "steps": (
            {
                "step_id": "review_access_state",
                "label": "Review access state",
                "form_id": "geotech_conditional_access",
                "operation": "review_mining_operations_management_policy_rule",
                "required_context": (),
            },
            {
                "step_id": "refresh_shift_targets",
                "label": "Refresh shift targets",
                "form_id": "shift_target_board",
                "operation": "review_extraction_shift",
                "required_context": ("area_id",),
            },
            {
                "step_id": "reassign_dispatch",
                "label": "Reassign dispatch",
                "form_id": "dispatch_assignment",
                "operation": "approve_haulage_cycle",
                "required_context": ("shift_id", "fleet_asset_id"),
            },
        ),
    },
)


def mining_operations_management_wizard_catalog() -> dict:
    forms = mining_operations_management_form_catalog()
    form_ids = set(forms["form_ids"])
    missing_form_bindings = tuple(
        f"{wizard['wizard_id']}:{step['step_id']}"
        for wizard in MINING_OPERATIONS_MANAGEMENT_WIZARDS
        for step in wizard["steps"]
        if step["form_id"] not in form_ids
    )
    return {
        "format": "appgen.mining-operations-management-wizard-catalog.v1",
        "ok": bool(MINING_OPERATIONS_MANAGEMENT_WIZARDS) and not missing_form_bindings,
        "pbc": PBC_KEY,
        "wizards": MINING_OPERATIONS_MANAGEMENT_WIZARDS,
        "wizard_ids": tuple(item["wizard_id"] for item in MINING_OPERATIONS_MANAGEMENT_WIZARDS),
        "missing_form_bindings": missing_form_bindings,
        "side_effects": (),
    }


def mining_operations_management_plan_wizard(wizard_id: str, context: dict | None = None) -> dict:
    wizard = next((item for item in MINING_OPERATIONS_MANAGEMENT_WIZARDS if item["wizard_id"] == wizard_id), None)
    if wizard is None:
        return {"ok": False, "reason": "unknown_wizard", "wizard_id": wizard_id, "side_effects": ()}

    supplied = dict(context or {})
    steps = []
    for position, step in enumerate(wizard["steps"], start=1):
        required_context = tuple(step.get("required_context", ()))
        blocked_by = tuple(name for name in required_context if supplied.get(name) in {None, "", ()})
        steps.append(
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
        "steps": tuple(steps),
        "side_effects": (),
    }


def smoke_test() -> dict:
    catalog = mining_operations_management_wizard_catalog()
    plan = mining_operations_management_plan_wizard(
        "weekly_plan_to_shift",
        {"plan_id": "plan_smoke", "shift_id": "shift_smoke", "fleet_asset_id": "truck_smoke"},
    )
    return {
        "ok": catalog["ok"] and plan["ok"] and bool(plan["steps"]),
        "catalog": catalog,
        "plan": plan,
        "side_effects": (),
    }
