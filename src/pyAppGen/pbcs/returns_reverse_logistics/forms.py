"""Forms for the standalone Returns Reverse Logistics PBC."""
PBC_KEY = "returns_reverse_logistics"
FORM_DEFINITIONS = (
    {"form_id": "returns_configuration", "action": "configure_runtime", "required_fields": ("database_backend", "event_topic", "retry_limit", "default_currency", "supported_carriers", "supported_dispositions")},
    {"form_id": "return_rule", "action": "register_rule", "required_fields": ("rule_id", "tenant", "scope", "status", "eligibility_policy", "label_policy", "inspection_policy", "credit_policy")},
    {"form_id": "return_authorization", "action": "authorize_return", "required_fields": ("return_id", "rma", "tenant", "order_id", "payment_id", "customer_id", "reason", "requested_at")},
    {"form_id": "return_label", "action": "create_return_label", "required_fields": ("label_id", "return_id", "tenant", "origin", "destination", "package_weight_kg")},
    {"form_id": "return_receipt", "action": "record_return_receipt", "required_fields": ("receipt_id", "return_id", "tenant", "received_at", "receiving_site", "package_condition")},
    {"form_id": "inspection_grade", "action": "record_inspection_grade", "required_fields": ("inspection_id", "return_id", "tenant", "condition_score", "completeness_score", "packaging_intact")},
    {"form_id": "credit_adjustment", "action": "issue_credit_adjustment", "required_fields": ("adjustment_id", "return_id", "tenant")},
    {"form_id": "refund_exchange_resolution", "action": "register_exchange_resolution", "required_fields": ("return_id", "resolution_mode")},
    {"form_id": "carrier_claim", "action": "open_carrier_claim", "required_fields": ("return_id", "claim_reason")},
    {"form_id": "exception_case", "action": "open_exception_case", "required_fields": ("return_id", "exception_type", "severity", "owner")},
    {"form_id": "document_instruction_intake", "action": "assistant_document_intake", "required_fields": ("document_text", "instructions")},
)

def returns_reverse_logistics_form_catalog():
    return {"ok": True, "pbc": PBC_KEY, "forms": FORM_DEFINITIONS, "form_ids": tuple(item["form_id"] for item in FORM_DEFINITIONS), "side_effects": ()}

def returns_reverse_logistics_validate_form_payload(form_id, payload=None):
    supplied = dict(payload or {})
    form = next((item for item in FORM_DEFINITIONS if item["form_id"] == form_id), None)
    if form is None:
        return {"ok": False, "pbc": PBC_KEY, "form_id": form_id, "unknown_form": True, "missing_fields": (), "side_effects": ()}
    missing = tuple(field for field in form["required_fields"] if field not in supplied or supplied[field] in (None, ""))
    return {"ok": not missing, "pbc": PBC_KEY, "form_id": form_id, "missing_fields": missing, "payload_keys": tuple(sorted(supplied)), "side_effects": ()}

def smoke_test():
    catalog = returns_reverse_logistics_form_catalog()
    valid = returns_reverse_logistics_validate_form_payload("document_instruction_intake", {"document_text": "RMA request", "instructions": "authorize return"})
    invalid = returns_reverse_logistics_validate_form_payload("return_authorization", {"return_id": "ret_demo"})
    return {"ok": catalog["ok"] and valid["ok"] and not invalid["ok"], "catalog": catalog, "valid": valid, "invalid": invalid, "side_effects": ()}
