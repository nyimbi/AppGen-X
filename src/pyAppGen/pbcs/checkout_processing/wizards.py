"""Package-local guided wizards for the Checkout Processing workbench."""

from __future__ import annotations

from .forms import checkout_processing_form_catalog


CHECKOUT_PROCESSING_WIZARDS = (
    {
        "wizard_id": "first_checkout",
        "title": "First checkout run",
        "goal": "Take a cart from intake to successful completion.",
        "steps": (
            {"step_id": "open_cart", "label": "Open cart", "form_id": "cart_intake", "operation": "command_carts"},
            {"step_id": "validate_shipping", "label": "Validate shipping", "form_id": "shipping_validation", "operation": "command_checkout"},
            {"step_id": "handoff_pricing", "label": "Apply pricing", "form_id": "pricing_handoff", "operation": "command_checkout"},
            {"step_id": "capture_payment", "label": "Capture payment", "form_id": "payment_capture", "operation": "command_payment_captures"},
        ),
    },
    {
        "wizard_id": "exception_recovery",
        "title": "Exception recovery",
        "goal": "Recover blocked sessions without violating inventory, payment, or risk controls.",
        "steps": (
            {"step_id": "inspect_dead_letter", "label": "Inspect event backlog", "form_id": "document_instruction_intake", "operation": "query_checkout_processing_controls"},
            {"step_id": "apply_fix", "label": "Generate bounded fix plan", "form_id": "document_instruction_intake", "operation": "query_checkout_processing_assistant_preview"},
            {"step_id": "recheck_release", "label": "Re-run controls", "form_id": "document_instruction_intake", "operation": "query_checkout_processing_controls"},
        ),
    },
    {
        "wizard_id": "release_readiness",
        "title": "Release readiness",
        "goal": "Review package-local evidence before promoting the checkout slice.",
        "steps": (
            {"step_id": "inspect_controls", "label": "Inspect control center", "form_id": "document_instruction_intake", "operation": "query_checkout_processing_controls"},
            {"step_id": "inspect_routes", "label": "Inspect route coverage", "form_id": "document_instruction_intake", "operation": "query_checkout_processing_workbench"},
            {"step_id": "confirm_assistant_guardrails", "label": "Confirm assistant previews", "form_id": "document_instruction_intake", "operation": "query_checkout_processing_assistant_preview"},
        ),
    },
    {
        "wizard_id": "assistant_change_preview",
        "title": "Assistant-guided change preview",
        "goal": "Turn an uploaded checkout note into a preview-only CRUD plan.",
        "steps": (
            {"step_id": "capture_document", "label": "Capture note", "form_id": "document_instruction_intake", "operation": "query_checkout_processing_assistant_preview"},
            {"step_id": "review_permissions", "label": "Review permission", "form_id": "document_instruction_intake", "operation": "query_checkout_processing_controls"},
            {"step_id": "review_mutation_preview", "label": "Review CRUD preview", "form_id": "document_instruction_intake", "operation": "query_checkout_processing_assistant_preview"},
        ),
    },
)


def checkout_processing_wizard_catalog() -> dict:
    """Return the guided wizard registry for this PBC."""
    forms = checkout_processing_form_catalog()
    form_ids = set(forms["form_ids"])
    missing_form_bindings = tuple(
        f"{wizard['wizard_id']}:{step['step_id']}"
        for wizard in CHECKOUT_PROCESSING_WIZARDS
        for step in wizard["steps"]
        if step["form_id"] not in form_ids
    )
    return {
        "ok": bool(CHECKOUT_PROCESSING_WIZARDS) and not missing_form_bindings,
        "pbc": "checkout_processing",
        "wizards": CHECKOUT_PROCESSING_WIZARDS,
        "wizard_ids": tuple(item["wizard_id"] for item in CHECKOUT_PROCESSING_WIZARDS),
        "missing_form_bindings": missing_form_bindings,
        "side_effects": (),
    }


def checkout_processing_plan_wizard(wizard_id: str, context: dict | None = None) -> dict:
    """Return a guided step plan with lightweight readiness hints."""
    wizard = next((item for item in CHECKOUT_PROCESSING_WIZARDS if item["wizard_id"] == wizard_id), None)
    if wizard is None:
        return {"ok": False, "reason": "unknown_wizard", "wizard_id": wizard_id, "side_effects": ()}

    supplied = dict(context or {})
    planned_steps = []
    for position, step in enumerate(wizard["steps"], start=1):
        blocked_by = ()
        if wizard_id == "first_checkout" and step["step_id"] != "open_cart" and not supplied.get("cart_id"):
            blocked_by = ("cart_id",)
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
        "pbc": "checkout_processing",
        "wizard_id": wizard_id,
        "goal": wizard["goal"],
        "steps": tuple(planned_steps),
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Exercise wizard catalog and a plan."""
    catalog = checkout_processing_wizard_catalog()
    plan = checkout_processing_plan_wizard("assistant_change_preview", {"cart_id": "cart_100"})
    return {
        "ok": catalog["ok"] and plan["ok"] and bool(plan["steps"]),
        "catalog": catalog,
        "plan": plan,
        "side_effects": (),
    }
