"""Idempotent inbound event handlers for the gl_core PBC."""

from __future__ import annotations

from .events import EVENT_CONTRACT


_HANDLER_BEHAVIOR = {
    "InvoiceApproved": {
        "function": "handle_invoice_approved",
        "projection": "invoice_approval_projection",
        "journal_intent": "accrual_candidate",
    },
    "PaymentCaptured": {
        "function": "handle_payment_captured",
        "projection": "payment_capture_projection",
        "journal_intent": "cash_receipt_candidate",
    },
    "PayrollPosted": {
        "function": "handle_payroll_posted",
        "projection": "payroll_posting_projection",
        "journal_intent": "payroll_settlement_candidate",
    },
    "AssetDepreciated": {
        "function": "handle_asset_depreciated",
        "projection": "asset_depreciation_projection",
        "journal_intent": "depreciation_candidate",
    },
    "TaxCalculated": {
        "function": "handle_tax_calculated",
        "projection": "tax_calculation_projection",
        "journal_intent": "tax_accrual_candidate",
    },
}
HANDLER_CONTRACTS = tuple(
    {
        "event_type": event_type,
        "function": behavior["function"],
        "projection": behavior["projection"],
        "journal_intent": behavior["journal_intent"],
        "idempotency_key": f"gl_core:{event_type}:{{event_id}}",
        "retry_policy": EVENT_CONTRACT["retry_policy"],
        "dead_letter_table": EVENT_CONTRACT["dead_letter_table"],
        "side_effect_boundary": "owned_tables_or_declared_api_calls",
    }
    for event_type, behavior in _HANDLER_BEHAVIOR.items()
)
_PROCESSED_KEYS = set()


def handler_manifest():
    """Return handler retry, idempotency, and dead-letter evidence."""
    return {
        "ok": bool(HANDLER_CONTRACTS),
        "pbc": "gl_core",
        "handlers": HANDLER_CONTRACTS,
        "event_types": tuple(item["event_type"] for item in HANDLER_CONTRACTS),
        "idempotency_keys": tuple(item["idempotency_key"] for item in HANDLER_CONTRACTS),
        "retry_policies": tuple(item["retry_policy"] for item in HANDLER_CONTRACTS),
        "dead_letter_tables": tuple(item["dead_letter_table"] for item in HANDLER_CONTRACTS),
        "side_effects": (),
    }


def dispatch_event(event):
    """Process one event envelope idempotently."""
    event_type = event.get("event_type")
    event_id = event.get("event_id")
    payload = dict(event.get("payload", {}))
    handler = next((item for item in HANDLER_CONTRACTS if item["event_type"] == event_type), None)
    if handler is None:
        return {"handled": False, "reason": "unregistered_event", "side_effects": ()}
    key = handler["idempotency_key"].format(event_id=event_id)
    if key in _PROCESSED_KEYS:
        return {"handled": True, "duplicate": True, "idempotency_key": key, "side_effects": ()}
    _PROCESSED_KEYS.add(key)
    projection = {
        "projection": handler["projection"],
        "tenant": payload.get("tenant", "tenant_demo"),
        "source_id": payload.get("invoice_id")
        or payload.get("payment_id")
        or payload.get("payroll_run_id")
        or payload.get("asset_id")
        or payload.get("tax_record_id")
        or event_id,
        "journal_intent": handler["journal_intent"],
    }
    return {
        "handled": True,
        "duplicate": False,
        "idempotency_key": key,
        "retry_policy": handler["retry_policy"],
        "dead_letter_table": handler["dead_letter_table"],
        "projection": projection,
        "side_effects": (),
    }


def smoke_test():
    """Exercise handler idempotency, retry, and dead-letter metadata."""
    manifest = handler_manifest()
    if not HANDLER_CONTRACTS:
        return {"ok": False, "manifest": manifest, "side_effects": ()}
    first = HANDLER_CONTRACTS[0]
    event = {
        "event_type": first["event_type"],
        "event_id": f"smoke-{len(_PROCESSED_KEYS)}",
        "payload": {"tenant": "tenant_smoke", "invoice_id": "inv-smoke"},
    }
    first_result = dispatch_event(event)
    duplicate_result = dispatch_event(event)
    unknown_result = dispatch_event({"event_type": "UnknownEvent", "event_id": event["event_id"]})
    return {
        "ok": manifest["ok"]
        and first_result.get("handled") is True
        and first_result.get("duplicate") is False
        and duplicate_result.get("duplicate") is True
        and unknown_result.get("handled") is False
        and bool(first_result.get("retry_policy"))
        and bool(first_result.get("dead_letter_table")),
        "manifest": manifest,
        "first_result": first_result,
        "duplicate_result": duplicate_result,
        "unknown_result": unknown_result,
        "side_effects": (),
    }
