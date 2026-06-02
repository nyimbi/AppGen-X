"""Guided workflows for the tax_localization standalone workbench."""

from __future__ import annotations

from .forms import tax_localization_form_catalog


TAX_LOCALIZATION_WIZARDS = (
    {
        "wizard_id": "jurisdiction_onboarding",
        "title": "Jurisdiction onboarding",
        "goal": "Register a jurisdiction, install rules, and make it filing-ready.",
        "steps": (
            {"step_id": "register_jurisdiction", "label": "Register jurisdiction", "form_id": "jurisdiction_registration", "operation": "command_tax_jurisdictions"},
            {"step_id": "author_rule", "label": "Author active rule", "form_id": "tax_rule_authoring", "operation": "command_tax_rules"},
            {"step_id": "confirm_filing_setup", "label": "Confirm filing setup", "form_id": "filing_preparation", "operation": "command_tax_filings"},
        ),
    },
    {
        "wizard_id": "quote_to_invoice",
        "title": "Quote to invoice tax",
        "goal": "Calculate tax, validate evidence, and lock the invoice tax record.",
        "steps": (
            {"step_id": "calculate_quote", "label": "Calculate quote", "form_id": "tax_quote_request", "operation": "command_tax_quotes"},
            {"step_id": "review_assistant", "label": "Review assistant guidance", "form_id": "assistant_document_intake", "operation": "assistant_preview"},
            {"step_id": "record_invoice_tax", "label": "Record invoice tax", "form_id": "invoice_tax_recording", "operation": "command_tax_invoices_id_tax_records"},
        ),
    },
    {
        "wizard_id": "filing_close",
        "title": "Filing close",
        "goal": "Prepare the filing, run controls, and route for authorized submission.",
        "steps": (
            {"step_id": "prepare_filing", "label": "Prepare filing", "form_id": "filing_preparation", "operation": "command_tax_filings"},
            {"step_id": "run_controls", "label": "Run release controls", "form_id": "assistant_document_intake", "operation": "control_center"},
            {"step_id": "preview_authority_route", "label": "Preview authority route", "form_id": "assistant_document_intake", "operation": "assistant_preview"},
        ),
    },
    {
        "wizard_id": "authority_notice_response",
        "title": "Authority notice response",
        "goal": "Capture the notice, assemble evidence, and prepare a bounded remediation plan.",
        "steps": (
            {"step_id": "ingest_notice", "label": "Ingest authority notice", "form_id": "assistant_document_intake", "operation": "assistant_preview"},
            {"step_id": "inspect_boundary", "label": "Inspect package controls", "form_id": "assistant_document_intake", "operation": "control_center"},
            {"step_id": "prepare_response", "label": "Prepare response plan", "form_id": "assistant_document_intake", "operation": "assistant_preview"},
        ),
    },
)


def tax_localization_wizard_catalog() -> dict:
    forms = tax_localization_form_catalog()
    form_ids = set(forms["form_ids"])
    missing_form_bindings = tuple(
        f"{wizard['wizard_id']}:{step['step_id']}"
        for wizard in TAX_LOCALIZATION_WIZARDS
        for step in wizard["steps"]
        if step["form_id"] not in form_ids
    )
    return {
        "ok": bool(TAX_LOCALIZATION_WIZARDS) and not missing_form_bindings,
        "pbc": "tax_localization",
        "wizards": TAX_LOCALIZATION_WIZARDS,
        "wizard_ids": tuple(item["wizard_id"] for item in TAX_LOCALIZATION_WIZARDS),
        "missing_form_bindings": missing_form_bindings,
        "side_effects": (),
    }


def tax_localization_plan_wizard(wizard_id: str, context: dict | None = None) -> dict:
    wizard = next((item for item in TAX_LOCALIZATION_WIZARDS if item["wizard_id"] == wizard_id), None)
    if wizard is None:
        return {"ok": False, "reason": "unknown_wizard", "wizard_id": wizard_id, "side_effects": ()}

    supplied = dict(context or {})
    planned_steps = []
    for position, step in enumerate(wizard["steps"], start=1):
        blocked_by = ()
        if wizard_id == "jurisdiction_onboarding" and step["step_id"] != "register_jurisdiction" and not supplied.get("jurisdiction_id"):
            blocked_by = ("jurisdiction_id",)
        if wizard_id == "quote_to_invoice" and step["step_id"] == "record_invoice_tax" and not supplied.get("calculation_id"):
            blocked_by = ("calculation_id",)
        if wizard_id == "filing_close" and step["step_id"] != "prepare_filing" and not supplied.get("filing_id"):
            blocked_by = ("filing_id",)
        planned_steps.append({**step, "position": position, "ready": not blocked_by, "blocked_by": blocked_by})
    return {
        "ok": True,
        "pbc": "tax_localization",
        "wizard_id": wizard_id,
        "goal": wizard["goal"],
        "steps": tuple(planned_steps),
        "side_effects": (),
    }


def smoke_test() -> dict:
    catalog = tax_localization_wizard_catalog()
    plan = tax_localization_plan_wizard("quote_to_invoice", {"calculation_id": "quote_100"})
    return {
        "ok": catalog["ok"] and plan["ok"] and bool(plan["steps"]),
        "catalog": catalog,
        "plan": plan,
        "side_effects": (),
    }
