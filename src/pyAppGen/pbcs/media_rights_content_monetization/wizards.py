"""Package-local guided wizards for the Media Rights and Content Monetization workbench."""

from __future__ import annotations

from .forms import media_rights_content_monetization_form_catalog


MEDIA_RIGHTS_CONTENT_MONETIZATION_WIZARDS = (
    {
        "wizard_id": "rights_clearance_launch",
        "title": "Rights clearance to launch",
        "goal": "Move a title from chain-of-title intake to a launchable territory-platform window.",
        "steps": (
            {"step_id": "capture_asset", "label": "Capture rights asset", "form_id": "rights_asset_grant_intake", "operation": "create_rights_asset"},
            {"step_id": "capture_agreement", "label": "Capture agreement", "form_id": "license_agreement_scope_review", "operation": "record_license_agreement"},
            {"step_id": "set_territories", "label": "Set territory carve-outs", "form_id": "territory_hierarchy_override", "operation": "record_territory_restriction"},
            {"step_id": "open_window", "label": "Open launch window", "form_id": "distribution_window_amendment", "operation": "review_distribution_window"},
        ),
    },
    {
        "wizard_id": "window_amendment_and_holdback",
        "title": "Window amendment and holdback",
        "goal": "Amend a live or pending window without losing traceable version history.",
        "steps": (
            {"step_id": "review_scope", "label": "Review agreement scope", "form_id": "license_agreement_scope_review", "operation": "record_license_agreement"},
            {"step_id": "amend_window", "label": "Amend window", "form_id": "distribution_window_amendment", "operation": "review_distribution_window"},
            {"step_id": "review_market_exceptions", "label": "Review territory overrides", "form_id": "territory_hierarchy_override", "operation": "record_territory_restriction"},
        ),
    },
    {
        "wizard_id": "monthly_close_and_royalty",
        "title": "Monthly close and royalty preview",
        "goal": "Normalize usage, validate monetization eligibility, and preview the payable waterfall.",
        "steps": (
            {"step_id": "normalize_usage", "label": "Normalize usage", "form_id": "usage_ingestion_normalization", "operation": "approve_usage_record"},
            {"step_id": "preview_waterfall", "label": "Preview royalty waterfall", "form_id": "royalty_waterfall_preview", "operation": "simulate_royalty_statement"},
            {"step_id": "review_control_center", "label": "Review controls", "form_id": "assistant_document_intake", "operation": "control_center"},
        ),
    },
    {
        "wizard_id": "assistant_conflict_triage",
        "title": "Assistant conflict triage",
        "goal": "Turn rights memos or legal notes into a preview-only remediation plan.",
        "steps": (
            {"step_id": "capture_document", "label": "Capture legal memo", "form_id": "assistant_document_intake", "operation": "assistant_preview"},
            {"step_id": "review_overlap_controls", "label": "Review overlap controls", "form_id": "assistant_document_intake", "operation": "control_center"},
            {"step_id": "review_window_fix", "label": "Review amendment wizard", "form_id": "distribution_window_amendment", "operation": "review_distribution_window"},
        ),
    },
)


def media_rights_content_monetization_wizard_catalog() -> dict:
    """Return the guided wizard registry for this PBC."""
    forms = media_rights_content_monetization_form_catalog()
    form_ids = set(forms["form_ids"])
    missing_form_bindings = tuple(
        f"{wizard['wizard_id']}:{step['step_id']}"
        for wizard in MEDIA_RIGHTS_CONTENT_MONETIZATION_WIZARDS
        for step in wizard["steps"]
        if step["form_id"] not in form_ids
    )
    return {
        "ok": bool(MEDIA_RIGHTS_CONTENT_MONETIZATION_WIZARDS) and not missing_form_bindings,
        "pbc": "media_rights_content_monetization",
        "wizards": MEDIA_RIGHTS_CONTENT_MONETIZATION_WIZARDS,
        "wizard_ids": tuple(item["wizard_id"] for item in MEDIA_RIGHTS_CONTENT_MONETIZATION_WIZARDS),
        "missing_form_bindings": missing_form_bindings,
        "side_effects": (),
    }



def media_rights_content_monetization_plan_wizard(wizard_id: str, context: dict | None = None) -> dict:
    """Return a guided step plan with lightweight readiness hints."""
    wizard = next((item for item in MEDIA_RIGHTS_CONTENT_MONETIZATION_WIZARDS if item["wizard_id"] == wizard_id), None)
    if wizard is None:
        return {"ok": False, "reason": "unknown_wizard", "wizard_id": wizard_id, "side_effects": ()}

    supplied = dict(context or {})
    planned_steps = []
    for position, step in enumerate(wizard["steps"], start=1):
        blocked_by = ()
        if wizard_id == "rights_clearance_launch":
            if step["step_id"] != "capture_asset" and not supplied.get("asset_id"):
                blocked_by = ("asset_id",)
            if step["step_id"] == "open_window" and not supplied.get("agreement_id"):
                blocked_by = tuple(dict.fromkeys(blocked_by + ("agreement_id",)))
        if wizard_id == "monthly_close_and_royalty" and step["step_id"] == "preview_waterfall" and not supplied.get("share_id"):
            blocked_by = ("share_id",)
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
        "pbc": "media_rights_content_monetization",
        "wizard_id": wizard_id,
        "goal": wizard["goal"],
        "steps": tuple(planned_steps),
        "side_effects": (),
    }



def smoke_test() -> dict:
    """Exercise wizard catalog and a plan."""
    catalog = media_rights_content_monetization_wizard_catalog()
    plan = media_rights_content_monetization_plan_wizard(
        "rights_clearance_launch",
        {"asset_id": "asset_001", "agreement_id": "lic_001"},
    )
    return {
        "ok": catalog["ok"] and plan["ok"] and bool(plan["steps"]),
        "catalog": catalog,
        "plan": plan,
        "side_effects": (),
    }
