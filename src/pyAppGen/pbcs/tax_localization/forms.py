"""Package-local forms for the tax_localization standalone workbench."""

from __future__ import annotations


TAX_LOCALIZATION_FORM_DEFINITIONS = (
    {
        "form_id": "jurisdiction_registration",
        "title": "Register jurisdiction",
        "route": "POST /api/pbc/tax_localization/tax/jurisdictions",
        "operation": "command_tax_jurisdictions",
        "permission": "tax_localization.jurisdiction",
        "writes_table": "tax_localization_tax_jurisdiction",
        "fields": (
            {"name": "tenant", "type": "string", "required": True},
            {"name": "jurisdiction_id", "type": "string", "required": True},
            {"name": "country", "type": "string", "required": True},
            {"name": "region", "type": "string", "required": True},
            {"name": "locality", "type": "string", "required": True},
            {"name": "currency", "type": "enum", "required": True, "choices": ("USD", "EUR", "KES", "GBP")},
            {"name": "filing_frequency", "type": "enum", "required": True, "choices": ("monthly", "quarterly", "annual")},
        ),
    },
    {
        "form_id": "tax_rule_authoring",
        "title": "Author tax rule",
        "route": "POST /api/pbc/tax_localization/tax/rules",
        "operation": "command_tax_rules",
        "permission": "tax_localization.rule_admin",
        "writes_table": "tax_localization_tax_rule",
        "fields": (
            {"name": "tenant", "type": "string", "required": True},
            {"name": "rule_id", "type": "string", "required": True},
            {"name": "jurisdiction_id", "type": "string", "required": True},
            {"name": "tax_type", "type": "enum", "required": True, "choices": ("sales_tax", "vat", "gst", "withholding_tax")},
            {"name": "product_class", "type": "string", "required": True},
            {"name": "rate", "type": "number", "required": True},
            {"name": "effective_from", "type": "date", "required": True},
        ),
    },
    {
        "form_id": "tax_quote_request",
        "title": "Calculate tax quote",
        "route": "POST /api/pbc/tax_localization/tax/quotes",
        "operation": "command_tax_quotes",
        "permission": "tax_localization.calculate",
        "writes_table": "tax_localization_tax_calculation",
        "fields": (
            {"name": "tenant", "type": "string", "required": True},
            {"name": "quote_id", "type": "string", "required": True},
            {"name": "jurisdiction_id", "type": "string", "required": True},
            {"name": "customer_id", "type": "string", "required": True},
            {"name": "order_id", "type": "string", "required": True},
            {"name": "line_count", "type": "number", "required": True},
        ),
    },
    {
        "form_id": "invoice_tax_recording",
        "title": "Record invoice tax",
        "route": "POST /api/pbc/tax_localization/tax/invoices/{id}/tax-records",
        "operation": "command_tax_invoices_id_tax_records",
        "permission": "tax_localization.invoice",
        "writes_table": "tax_localization_invoice_tax_record",
        "fields": (
            {"name": "invoice_id", "type": "string", "required": True},
            {"name": "calculation_id", "type": "string", "required": True},
            {"name": "tenant", "type": "string", "required": True},
            {"name": "tax_total", "type": "number", "required": True},
        ),
    },
    {
        "form_id": "filing_preparation",
        "title": "Prepare tax filing",
        "route": "POST /api/pbc/tax_localization/tax/filings",
        "operation": "command_tax_filings",
        "permission": "tax_localization.file",
        "writes_table": "tax_localization_tax_filing",
        "fields": (
            {"name": "filing_id", "type": "string", "required": True},
            {"name": "tenant", "type": "string", "required": True},
            {"name": "jurisdiction_id", "type": "string", "required": True},
            {"name": "period", "type": "string", "required": True},
            {"name": "approved_by", "type": "string", "required": True},
        ),
    },
    {
        "form_id": "assistant_document_intake",
        "title": "Assistant document intake",
        "route": "/assistant/pbc/tax_localization/preview",
        "operation": "assistant_preview",
        "permission": "tax_localization.audit",
        "writes_table": "tax_localization_tax_policy_rule",
        "fields": (
            {"name": "document_text", "type": "text", "required": True},
            {"name": "instructions", "type": "text", "required": True},
            {"name": "target_entity", "type": "enum", "required": True, "choices": ("tax_rule", "tax_parameter", "tax_configuration", "exemption_certificate", "tax_filing")},
            {"name": "requested_action", "type": "enum", "required": True, "choices": ("create", "read", "update", "delete")},
        ),
    },
)


def tax_localization_form_catalog() -> dict:
    forms = tuple(TAX_LOCALIZATION_FORM_DEFINITIONS)
    return {
        "ok": bool(forms),
        "pbc": "tax_localization",
        "forms": forms,
        "form_ids": tuple(item["form_id"] for item in forms),
        "side_effects": (),
    }


def tax_localization_get_form(form_id: str) -> dict:
    form = next((item for item in TAX_LOCALIZATION_FORM_DEFINITIONS if item["form_id"] == form_id), None)
    return {
        "ok": form is not None,
        "pbc": "tax_localization",
        "form": form,
        "side_effects": (),
    }


def tax_localization_validate_form_payload(form_id: str, payload: dict | None = None) -> dict:
    form = tax_localization_get_form(form_id).get("form")
    if form is None:
        return {"ok": False, "accepted": False, "reason": "unknown_form", "form_id": form_id, "side_effects": ()}

    supplied = dict(payload or {})
    missing = tuple(
        field["name"]
        for field in form["fields"]
        if field.get("required") and supplied.get(field["name"]) in {None, ""}
    )
    invalid_choices = tuple(
        field["name"]
        for field in form["fields"]
        if field.get("type") == "enum"
        and supplied.get(field["name"]) not in {None, *field.get("choices", ())}
    )
    return {
        "ok": not missing and not invalid_choices,
        "accepted": not missing and not invalid_choices,
        "pbc": "tax_localization",
        "form_id": form_id,
        "missing": missing,
        "invalid_choices": invalid_choices,
        "payload_keys": tuple(sorted(supplied)),
        "side_effects": (),
    }


def smoke_test() -> dict:
    catalog = tax_localization_form_catalog()
    validation = tax_localization_validate_form_payload(
        "assistant_document_intake",
        {
            "document_text": "California local rule update for exemption handling.",
            "instructions": "Update the filing rule to enforce the local exemption review.",
            "target_entity": "tax_rule",
            "requested_action": "update",
        },
    )
    return {
        "ok": catalog["ok"] and validation["ok"],
        "catalog": catalog,
        "validation": validation,
        "side_effects": (),
    }
