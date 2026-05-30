"""Package-local forms for the standalone ar_credit workbench."""

from __future__ import annotations


AR_CREDIT_FORM_DEFINITIONS = (
    {
        "form_id": "customer_credit_onboarding",
        "title": "Customer credit onboarding",
        "route": "POST /api/pbc/ar_credit/ar/customers",
        "operation": "command_ar_customers",
        "permission": "ar_credit.customer",
        "payload_key": "customer",
        "owned_tables": (
            "ar_customer",
            "ar_customer_graph",
            "ar_customer_credit_profile",
            "ar_customer_payment_terms",
            "ar_credit_decision",
        ),
        "fields": (
            {"name": "tenant", "type": "string", "required": True},
            {"name": "customer_id", "type": "string", "required": True},
            {"name": "name", "type": "string", "required": True},
            {"name": "requested_limit", "type": "number", "required": True},
            {"name": "parent", "type": "string", "required": False},
            {"name": "beneficial_owners", "type": "list", "required": False},
            {"name": "terms", "type": "json", "required": True},
            {"name": "risk_signals", "type": "json", "required": True},
            {"name": "identity", "type": "json", "required": True},
        ),
    },
    {
        "form_id": "invoice_issuance",
        "title": "Invoice issuance gate",
        "route": "POST /api/pbc/ar_credit/ar/invoices",
        "operation": "command_ar_invoices",
        "permission": "ar_credit.invoice",
        "payload_key": "invoice",
        "owned_tables": (
            "ar_invoice",
            "ar_invoice_line",
            "ar_invoice_tax",
            "ar_invoice_performance_obligation",
        ),
        "fields": (
            {"name": "tenant", "type": "string", "required": True},
            {"name": "invoice_id", "type": "string", "required": True},
            {"name": "customer_id", "type": "string", "required": True},
            {"name": "currency", "type": "enum", "required": True, "choices": ("USD", "EUR", "KES")},
            {"name": "invoice_date", "type": "date", "required": True},
            {"name": "due_date", "type": "date", "required": True},
            {"name": "tax", "type": "json", "required": True},
            {"name": "lines", "type": "json", "required": True},
            {"name": "performance_obligations", "type": "json", "required": True},
        ),
    },
    {
        "form_id": "cash_receipt_application",
        "title": "Cash receipt application",
        "route": "POST /api/pbc/ar_credit/ar/cash-applications",
        "operation": "command_ar_cash_applications",
        "permission": "ar_credit.cash",
        "payload_key": "receipt",
        "owned_tables": (
            "ar_cash_receipt",
            "ar_cash_application",
            "ar_unapplied_cash",
            "ar_cash_pool",
        ),
        "fields": (
            {"name": "tenant", "type": "string", "required": True},
            {"name": "receipt_id", "type": "string", "required": True},
            {"name": "customer_id", "type": "string", "required": False},
            {"name": "currency", "type": "enum", "required": True, "choices": ("USD", "EUR", "KES")},
            {"name": "amount", "type": "number", "required": True},
            {"name": "remittance_text", "type": "text", "required": False},
            {"name": "remittance", "type": "json", "required": False},
        ),
    },
    {
        "form_id": "collections_follow_up",
        "title": "Collections follow-up",
        "route": "POST /api/pbc/ar_credit/ar/collections",
        "operation": "command_ar_collections",
        "permission": "ar_credit.collection",
        "payload_key": None,
        "owned_tables": (
            "ar_collection_action",
            "ar_dunning_notice",
            "ar_statement",
            "ar_invoice",
        ),
        "fields": (
            {"name": "customer_id", "type": "string", "required": True},
            {"name": "as_of", "type": "date", "required": True},
            {"name": "channel", "type": "enum", "required": False, "choices": ("portal", "api", "email")},
            {"name": "note", "type": "text", "required": False},
        ),
    },
)


def ar_credit_form_catalog() -> dict:
    forms = tuple(AR_CREDIT_FORM_DEFINITIONS)
    return {
        "ok": bool(forms),
        "pbc": "ar_credit",
        "forms": forms,
        "form_ids": tuple(item["form_id"] for item in forms),
        "side_effects": (),
    }


def ar_credit_get_form(form_id: str) -> dict:
    form = next((item for item in AR_CREDIT_FORM_DEFINITIONS if item["form_id"] == form_id), None)
    return {
        "ok": form is not None,
        "pbc": "ar_credit",
        "form": form,
        "side_effects": (),
    }


def ar_credit_validate_form_payload(form_id: str, payload: dict | None = None) -> dict:
    form = ar_credit_get_form(form_id).get("form")
    if form is None:
        return {
            "ok": False,
            "accepted": False,
            "reason": "unknown_form",
            "form_id": form_id,
            "side_effects": (),
        }

    supplied = dict(payload or {})
    missing = tuple(
        field["name"]
        for field in form["fields"]
        if field.get("required") and supplied.get(field["name"]) in (None, "")
    )
    invalid_choices = tuple(
        field["name"]
        for field in form["fields"]
        if field.get("type") == "enum"
        and supplied.get(field["name"]) not in (None, *field.get("choices", ()))
    )
    return {
        "ok": not missing and not invalid_choices,
        "accepted": not missing and not invalid_choices,
        "pbc": "ar_credit",
        "form_id": form_id,
        "missing": missing,
        "invalid_choices": invalid_choices,
        "payload_keys": tuple(sorted(supplied)),
        "side_effects": (),
    }


def ar_credit_prepare_form_submission(form_id: str, payload: dict | None = None) -> dict:
    form = ar_credit_get_form(form_id).get("form")
    validation = ar_credit_validate_form_payload(form_id, payload)
    if form is None:
        return validation
    method, path = form["route"].split(" ", 1)
    record = dict(payload or {})
    body = {form["payload_key"]: record} if form.get("payload_key") else record
    return {
        "ok": validation["ok"],
        "pbc": "ar_credit",
        "form": form,
        "method": method,
        "path": path,
        "payload": body,
        "validation": validation,
        "side_effects": (),
    }


def smoke_test() -> dict:
    catalog = ar_credit_form_catalog()
    validation = ar_credit_validate_form_payload(
        "customer_credit_onboarding",
        {
            "tenant": "tenant_demo",
            "customer_id": "cust-demo",
            "name": "Demo Buyer",
            "requested_limit": 1200,
            "terms": {"net_days": 30},
            "risk_signals": {"payment_latency": 0.04},
            "identity": {"did": "did:appgen:cust-demo", "issuer": "trusted_registry", "status": "active"},
        },
    )
    prepared = ar_credit_prepare_form_submission(
        "collections_follow_up",
        {"customer_id": "cust-demo", "as_of": "2026-06-30"},
    )
    return {
        "ok": catalog["ok"] and validation["ok"] and prepared["ok"],
        "catalog": catalog,
        "validation": validation,
        "prepared": prepared,
        "side_effects": (),
    }
