"""Forms for the standalone Payment Orchestration PBC."""

PBC_KEY = "payment_orchestration"
FORM_DEFINITIONS = (
    {"form_id": "payment_configuration", "action": "configure_runtime", "required_fields": ("database_backend", "event_topic", "retry_limit", "default_currency", "supported_currencies", "supported_regions", "supported_methods", "settlement_windows", "default_timezone", "workbench_limit")},
    {"form_id": "payment_gateway", "action": "register_gateway", "required_fields": ("gateway_id", "tenant", "provider", "regions", "currencies", "methods", "latency_ms", "fee_bps", "authorization_rate", "settlement_risk", "capacity", "carbon_score", "status")},
    {"form_id": "payment_token", "action": "tokenize_payment_method", "required_fields": ("token_id", "tenant", "customer_id", "method_type", "network", "issuer_country", "vault_ref")},
    {"form_id": "payment_intent", "action": "create_payment_intent", "required_fields": ("intent_id", "tenant", "checkout_id", "customer_id", "amount", "currency", "region", "token_id")},
    {"form_id": "payment_capture", "action": "capture_payment", "required_fields": ("intent_id", "amount")},
    {"form_id": "payment_refund", "action": "refund_payment", "required_fields": ("intent_id", "amount", "reason")},
    {"form_id": "payment_dispute", "action": "open_dispute", "required_fields": ("intent_id", "amount", "reason")},
    {"form_id": "document_instruction_intake", "action": "assistant_document_intake", "required_fields": ("document_text", "instructions")},
)


def payment_orchestration_form_catalog():
    return {"ok": True, "pbc": PBC_KEY, "forms": FORM_DEFINITIONS, "form_ids": tuple(item["form_id"] for item in FORM_DEFINITIONS), "side_effects": ()}


def payment_orchestration_validate_form_payload(form_id, payload=None):
    supplied = dict(payload or {})
    form = next((item for item in FORM_DEFINITIONS if item["form_id"] == form_id), None)
    if not form:
        return {"ok": False, "pbc": PBC_KEY, "form_id": form_id, "missing_fields": (), "unknown_form": True, "side_effects": ()}
    missing = tuple(field for field in form["required_fields"] if field not in supplied or supplied[field] in (None, ""))
    return {"ok": not missing, "pbc": PBC_KEY, "form_id": form_id, "missing_fields": missing, "payload_keys": tuple(sorted(supplied)), "side_effects": ()}


def smoke_test():
    valid = payment_orchestration_validate_form_payload("document_instruction_intake", {"document_text": "capture payment pi_demo", "instructions": "capture payment"})
    invalid = payment_orchestration_validate_form_payload("payment_gateway", {"gateway_id": "gateway_demo"})
    catalog = payment_orchestration_form_catalog()
    return {"ok": catalog["ok"] and valid["ok"] and not invalid["ok"], "catalog": catalog, "valid": valid, "invalid": invalid, "side_effects": ()}
