"""Forms for the standalone Subscription Billing PBC."""

PBC_KEY = "subscription_billing"
FORM_DEFINITIONS = (
    {"form_id": "billing_configuration", "action": "configure_runtime", "required_fields": ("database_backend", "event_topic", "retry_limit", "default_currency", "supported_currencies", "supported_regions", "billing_calendars", "default_timezone", "invoice_approval_mode", "workbench_limit")},
    {"form_id": "plan_catalog", "action": "register_plan", "required_fields": ("plan_id", "tenant", "family", "name", "currency", "region", "billing_period", "base_price", "usage_rate", "included_units", "status")},
    {"form_id": "trial_period", "action": "start_trial", "required_fields": ("trial_id", "tenant", "customer_id", "plan_id", "start_date", "end_date", "region", "currency")},
    {"form_id": "subscription", "action": "create_subscription", "required_fields": ("subscription_id", "tenant", "customer_id", "plan_id", "start_date", "renewal_date", "region", "currency", "seats")},
    {"form_id": "usage_meter", "action": "record_usage", "required_fields": ("usage_id", "tenant", "subscription_id", "meter_name", "quantity", "occurred_at")},
    {"form_id": "invoice", "action": "generate_invoice", "required_fields": ("subscription_id", "period")},
    {"form_id": "credit_memo", "action": "issue_credit_memo", "required_fields": ("invoice_id", "amount", "reason")},
    {"form_id": "payment_application", "action": "apply_payment_to_invoice", "required_fields": ("invoice_id", "payment_event_id", "amount")},
    {"form_id": "subscription_change", "action": "change_subscription_plan", "required_fields": ("subscription_id", "target_plan_id", "effective_date", "reason")},
    {"form_id": "dunning_notice", "action": "create_dunning_notice", "required_fields": ("subscription_id", "reason")},
    {"form_id": "document_instruction_intake", "action": "assistant_document_intake", "required_fields": ("document_text", "instructions")},
)


def subscription_billing_form_catalog():
    return {"ok": True, "pbc": PBC_KEY, "forms": FORM_DEFINITIONS, "form_ids": tuple(item["form_id"] for item in FORM_DEFINITIONS), "side_effects": ()}


def subscription_billing_validate_form_payload(form_id, payload=None):
    supplied = dict(payload or {})
    form = next((item for item in FORM_DEFINITIONS if item["form_id"] == form_id), None)
    if form is None:
        return {"ok": False, "pbc": PBC_KEY, "form_id": form_id, "unknown_form": True, "missing_fields": (), "side_effects": ()}
    missing = tuple(field for field in form["required_fields"] if field not in supplied or supplied[field] in (None, ""))
    return {"ok": not missing, "pbc": PBC_KEY, "form_id": form_id, "missing_fields": missing, "payload_keys": tuple(sorted(supplied)), "side_effects": ()}


def smoke_test():
    catalog = subscription_billing_form_catalog()
    valid = subscription_billing_validate_form_payload("document_instruction_intake", {"document_text": "create invoice", "instructions": "bill subscription"})
    invalid = subscription_billing_validate_form_payload("subscription", {"subscription_id": "sub_demo"})
    return {"ok": catalog["ok"] and valid["ok"] and not invalid["ok"], "catalog": catalog, "valid": valid, "invalid": invalid, "side_effects": ()}
