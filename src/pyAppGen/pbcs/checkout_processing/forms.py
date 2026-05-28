"""Package-local forms for the Checkout Processing workbench."""

from __future__ import annotations


CHECKOUT_PROCESSING_FORM_DEFINITIONS = (
    {
        "form_id": "cart_intake",
        "title": "Open cart",
        "route": "POST /api/pbc/checkout_processing/carts",
        "operation": "command_carts",
        "permission": "checkout_processing.cart",
        "owned_tables": ("checkout_processing_cart", "checkout_processing_cart_line"),
        "fields": (
            {"name": "tenant", "type": "string", "required": True},
            {"name": "cart_id", "type": "string", "required": True},
            {"name": "customer_id", "type": "string", "required": True},
            {"name": "channel", "type": "enum", "required": True, "choices": ("web", "mobile", "support")},
            {"name": "currency", "type": "enum", "required": True, "choices": ("USD", "EUR", "KES")},
            {"name": "market", "type": "string", "required": True},
        ),
    },
    {
        "form_id": "shipping_validation",
        "title": "Validate shipping",
        "route": "POST /api/pbc/checkout_processing/checkout",
        "operation": "command_checkout",
        "permission": "checkout_processing.checkout",
        "owned_tables": ("checkout_processing_checkout_address_validation", "checkout_processing_checkout_session"),
        "fields": (
            {"name": "cart_id", "type": "string", "required": True},
            {"name": "country", "type": "string", "required": True},
            {"name": "region", "type": "string", "required": False},
            {"name": "postal_code", "type": "string", "required": True},
            {"name": "shipping_option", "type": "enum", "required": True, "choices": ("standard", "express", "pickup")},
        ),
    },
    {
        "form_id": "pricing_handoff",
        "title": "Apply pricing handoff",
        "route": "POST /api/pbc/checkout_processing/checkout",
        "operation": "command_checkout",
        "permission": "checkout_processing.pricing",
        "owned_tables": ("checkout_processing_checkout_pricing_handoff", "checkout_processing_checkout_tax_handoff"),
        "fields": (
            {"name": "session_id", "type": "string", "required": True},
            {"name": "pricing_basis", "type": "enum", "required": True, "choices": ("projected_catalog", "repriced_quote")},
            {"name": "pricing_handoff_id", "type": "string", "required": True},
            {"name": "tax_calculation_id", "type": "string", "required": False},
        ),
    },
    {
        "form_id": "payment_capture",
        "title": "Capture payment",
        "route": "POST /api/pbc/checkout_processing/payment-captures",
        "operation": "command_payment_captures",
        "permission": "checkout_processing.payment",
        "owned_tables": ("checkout_processing_checkout_payment_intent_handoff", "checkout_processing_checkout_session"),
        "fields": (
            {"name": "session_id", "type": "string", "required": True},
            {"name": "payment_intent_id", "type": "string", "required": True},
            {"name": "capture_id", "type": "string", "required": True},
            {"name": "operator_note", "type": "string", "required": False},
        ),
    },
    {
        "form_id": "document_instruction_intake",
        "title": "Assistant document intake",
        "route": "POST /api/pbc/checkout_processing/assistant/document-preview",
        "operation": "query_checkout_processing_assistant_preview",
        "permission": "checkout_processing.audit",
        "owned_tables": (
            "checkout_processing_checkout_rule",
            "checkout_processing_checkout_parameter",
            "checkout_processing_checkout_configuration",
            "checkout_processing_checkout_session",
        ),
        "fields": (
            {"name": "document_text", "type": "text", "required": True},
            {"name": "instructions", "type": "text", "required": True},
            {
                "name": "target_entity",
                "type": "enum",
                "required": True,
                "choices": ("checkout_rule", "checkout_parameter", "checkout_configuration", "checkout_session"),
            },
            {"name": "requested_action", "type": "enum", "required": True, "choices": ("create", "read", "update", "delete")},
        ),
    },
)


def checkout_processing_form_catalog() -> dict:
    """Return the package-local workbench form registry."""
    forms = tuple(CHECKOUT_PROCESSING_FORM_DEFINITIONS)
    return {
        "ok": bool(forms),
        "pbc": "checkout_processing",
        "forms": forms,
        "form_ids": tuple(item["form_id"] for item in forms),
        "side_effects": (),
    }


def checkout_processing_get_form(form_id: str) -> dict:
    """Return one form definition by identifier."""
    form = next((item for item in CHECKOUT_PROCESSING_FORM_DEFINITIONS if item["form_id"] == form_id), None)
    return {
        "ok": form is not None,
        "pbc": "checkout_processing",
        "form": form,
        "side_effects": (),
    }


def checkout_processing_validate_form_payload(form_id: str, payload: dict | None = None) -> dict:
    """Validate a form payload against required fields and enum choices."""
    form = checkout_processing_get_form(form_id).get("form")
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
        "pbc": "checkout_processing",
        "form_id": form_id,
        "missing": missing,
        "invalid_choices": invalid_choices,
        "payload_keys": tuple(sorted(supplied)),
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Exercise one happy-path form validation."""
    catalog = checkout_processing_form_catalog()
    validation = checkout_processing_validate_form_payload(
        "document_instruction_intake",
        {
            "document_text": "Promo memo: SAVE15 only for web carts in US.",
            "instructions": "Update the rule to keep SAVE15 web-only.",
            "target_entity": "checkout_rule",
            "requested_action": "update",
        },
    )
    return {
        "ok": catalog["ok"] and validation["ok"],
        "catalog": catalog,
        "validation": validation,
        "side_effects": (),
    }
