"""Executable invoice-to-cash workflow slice for the ar_credit PBC."""

from __future__ import annotations

import hashlib

from .runtime import AR_CREDIT_OWNED_TABLES
from .runtime import ar_credit_apply_cash
from .runtime import ar_credit_calculate_aging
from .runtime import ar_credit_create_dunning_plan
from .runtime import ar_credit_generate_customer_statement
from .runtime import ar_credit_issue_invoice
from .runtime import ar_credit_onboard_customer
from .runtime import ar_credit_parse_remittance
from .runtime import ar_credit_record_unapplied_cash
from .runtime import ar_credit_verify_customer_identity


AR_CREDIT_IMPLEMENTED_BACKLOG_ITEMS = (
    "customer_credit_onboarding_evidence_pack",
    "invoice_issuance_completeness_gate",
    "semantic_remittance_intake_and_cash_application",
    "collections_follow_up_workspace",
)

AR_CREDIT_WORKFLOW_OPERATIONS = (
    "review_credit_onboarding",
    "execute_customer_onboarding",
    "review_invoice_readiness",
    "execute_invoice_issuance",
    "execute_receipt_application",
    "build_collections_follow_up",
)


def ar_credit_review_credit_onboarding(customer: dict | None) -> dict:
    """Review onboarding evidence before customer activation."""
    candidate = dict(customer or {})
    required = ("customer_id", "tenant", "name", "terms", "risk_signals", "identity", "requested_limit")
    missing_fields = tuple(field for field in required if not candidate.get(field))
    terms = dict(candidate.get("terms") or {})
    term_blockers = tuple(
        field
        for field in ("net_days",)
        if terms.get(field) in (None, "")
    )
    identity_review = ar_credit_verify_customer_identity(candidate.get("identity") or {})
    graph_degree = len(tuple(candidate.get("beneficial_owners") or ())) + (1 if candidate.get("parent") else 0)
    default_probability = _risk_probability(candidate.get("risk_signals") or {}, graph_degree=graph_degree)
    requested_limit = round(float(candidate.get("requested_limit") or 0.0), 2)
    recommended_limit = round(max(0.0, requested_limit * (1 - min(default_probability, 0.75) * 0.55)), 2)
    blockers = []
    if missing_fields:
        blockers.extend({"code": f"missing_{field}", "field": field} for field in missing_fields)
    if term_blockers:
        blockers.extend({"code": f"missing_terms_{field}", "field": field} for field in term_blockers)
    if identity_review["ok"] is not True:
        blockers.append({"code": "identity_not_verified", "field": "identity"})
    activation_decision = "approve" if not blockers and default_probability <= 0.45 else "manual_review"
    review = {
        "ok": True,
        "ready": not blockers,
        "customer_id": candidate.get("customer_id"),
        "tenant": candidate.get("tenant"),
        "missing_fields": tuple(missing_fields),
        "blockers": tuple(blockers),
        "requested_limit": requested_limit,
        "recommended_limit": recommended_limit,
        "default_probability": default_probability,
        "risk_grade": _risk_grade(default_probability),
        "activation_decision": activation_decision,
        "identity_review": identity_review,
        "required_tables": (
            "ar_customer",
            "ar_customer_credit_profile",
            "ar_customer_payment_terms",
            "ar_customer_risk_signal",
            "ar_credit_decision",
        ),
        "event_contract": "AppGen-X",
        "shared_table_access": False,
        "audit_proof": _digest(
            {
                "customer_id": candidate.get("customer_id"),
                "tenant": candidate.get("tenant"),
                "requested_limit": requested_limit,
                "recommended_limit": recommended_limit,
                "default_probability": default_probability,
                "identity_ok": identity_review["ok"],
            }
        ),
    }
    return review


def ar_credit_execute_customer_onboarding(state: dict, customer: dict | None) -> dict:
    """Execute onboarding only when the evidence pack is complete."""
    review = ar_credit_review_credit_onboarding(customer)
    if review["ready"] is not True:
        return {
            "ok": False,
            "error": "customer_not_ready",
            "state": state,
            "review": review,
            "blockers": review["blockers"],
            "side_effects": (),
        }
    candidate = dict(customer or {})
    enriched = {
        **candidate,
        "credit_limit": review["recommended_limit"],
        "audit_proof": review["audit_proof"],
        "risk_grade": review["risk_grade"],
    }
    result = ar_credit_onboard_customer(state, enriched)
    return {
        **result,
        "review": review,
        "side_effects": (),
    }


def ar_credit_review_invoice_readiness(state: dict, invoice: dict | None) -> dict:
    """Evaluate invoice issuance readiness against customer, credit, and billing evidence."""
    candidate = dict(invoice or {})
    customer_id = candidate.get("customer_id")
    customer = state.get("customers", {}).get(customer_id)
    customer_identity = (
        dict((customer or {}).get("identity") or {})
        or dict(state.get("customer_identity_projections", {}).get(customer_id) or {})
    )
    lines = tuple(candidate.get("lines") or ())
    tax = dict(candidate.get("tax") or {})
    obligations = tuple(candidate.get("performance_obligations") or ())
    subtotal = round(sum(float(line["quantity"]) * float(line["unit_price"]) for line in lines), 2) if lines else 0.0
    tax_amount = round(float(tax.get("amount") or 0.0), 2)
    projected_total = round(subtotal + tax_amount, 2)
    existing_exposure = round(
        sum(
            float(existing.get("open_amount") or 0.0)
            for existing in state.get("invoices", {}).values()
            if existing.get("customer_id") == customer_id
        ),
        2,
    )
    credit_limit = float((customer or {}).get("credit_limit") or candidate.get("credit_limit") or 0.0)
    credit_buffer = float(state.get("parameters", {}).get("credit_limit_buffer", 0.0) or 0.0)
    allowed_exposure = round(credit_limit * (1 + credit_buffer), 2)
    obligation_total = round(sum(float(item.get("allocation") or 0.0) for item in obligations), 2)
    delivery_required = bool(candidate.get("delivery_confirmation_required"))
    delivery_present = bool(candidate.get("delivery_confirmation"))
    checks = (
        {
            "check": "customer_active",
            "passed": bool(customer and customer.get("status") == "active"),
            "detail": customer_id,
        },
        {
            "check": "identity_verified",
            "passed": ar_credit_verify_customer_identity(customer_identity)["ok"],
            "detail": customer_identity.get("did") or customer_identity.get("customer_id"),
        },
        {
            "check": "line_items_present",
            "passed": bool(lines) and subtotal > 0,
            "detail": len(lines),
        },
        {
            "check": "tax_evidence_present",
            "passed": bool(tax.get("jurisdiction")) and tax_amount >= 0,
            "detail": tax.get("jurisdiction"),
        },
        {
            "check": "performance_obligations_present",
            "passed": bool(obligations) and obligation_total > 0,
            "detail": obligation_total,
        },
        {
            "check": "due_date_valid",
            "passed": bool(candidate.get("invoice_date")) and bool(candidate.get("due_date")) and candidate.get("due_date") >= candidate.get("invoice_date"),
            "detail": (candidate.get("invoice_date"), candidate.get("due_date")),
        },
        {
            "check": "credit_limit_available",
            "passed": allowed_exposure == 0.0 or existing_exposure + projected_total <= allowed_exposure,
            "detail": {"projected_exposure": round(existing_exposure + projected_total, 2), "allowed_exposure": allowed_exposure},
        },
        {
            "check": "delivery_evidence_present",
            "passed": (not delivery_required) or delivery_present,
            "detail": delivery_required,
        },
    )
    blockers = tuple(
        {
            "code": check["check"],
            "detail": check["detail"],
        }
        for check in checks
        if check["passed"] is not True
    )
    normalized_invoice = {
        **candidate,
        "subtotal": subtotal,
        "total": projected_total,
    }
    return {
        "ok": True,
        "ready": not blockers,
        "invoice_id": candidate.get("invoice_id"),
        "customer_id": customer_id,
        "checks": checks,
        "blockers": blockers,
        "projected_total": projected_total,
        "normalized_invoice": normalized_invoice,
        "required_tables": (
            "ar_customer",
            "ar_customer_credit_profile",
            "ar_invoice",
            "ar_invoice_line",
            "ar_invoice_tax",
            "ar_invoice_performance_obligation",
            "ar_delivery_confirmation",
        ),
        "event_contract": "AppGen-X",
        "shared_table_access": False,
    }


def ar_credit_execute_invoice_issuance(state: dict, invoice: dict | None) -> dict:
    """Issue an invoice only after the readiness gate passes."""
    readiness = ar_credit_review_invoice_readiness(state, invoice)
    if readiness["ready"] is not True:
        return {
            "ok": False,
            "error": "invoice_not_ready",
            "state": state,
            "readiness": readiness,
            "blockers": readiness["blockers"],
            "side_effects": (),
        }
    result = ar_credit_issue_invoice(state, readiness["normalized_invoice"])
    return {
        **result,
        "readiness": readiness,
        "side_effects": (),
    }


def ar_credit_execute_receipt_application(state: dict, receipt: dict | None) -> dict:
    """Parse remittance and either apply cash or triage unapplied value."""
    candidate = dict(receipt or {})
    remittance = dict(candidate.get("remittance") or {})
    if not remittance and candidate.get("remittance_text"):
        remittance = ar_credit_parse_remittance(str(candidate.get("remittance_text")))
    invoice_id = remittance.get("invoice_id")
    invoice = state.get("invoices", {}).get(invoice_id)
    if not remittance.get("ok") or not invoice:
        triage = ar_credit_record_unapplied_cash(
            state,
            {
                "receipt_id": candidate["receipt_id"],
                "tenant": candidate["tenant"],
                "amount": round(float(candidate["amount"]), 2),
                "currency": candidate["currency"],
                "reason": "missing_or_unmatched_remittance",
            },
        )
        return {
            "ok": True,
            "decision": "record_unapplied_cash",
            "state": triage["state"],
            "remittance": remittance,
            "unapplied_cash": triage["unapplied_cash"],
            "required_tables": ("ar_unapplied_cash", "ar_cash_pool", "ar_credit_appgen_outbox_event"),
            "event_contract": "AppGen-X",
            "shared_table_access": False,
            "side_effects": (),
        }

    receipt_amount = round(float(candidate["amount"]), 2)
    open_amount = round(float(invoice["open_amount"]), 2)
    if receipt_amount > open_amount:
        applied_receipt = {
            **candidate,
            "amount": open_amount,
            "remittance": {**remittance, "amount": open_amount, "confidence": max(remittance.get("confidence", 0.4), 0.99)},
        }
        applied = ar_credit_apply_cash(state, applied_receipt)
        excess_amount = round(receipt_amount - open_amount, 2)
        excess = ar_credit_record_unapplied_cash(
            applied["state"],
            {
                "receipt_id": f"{candidate['receipt_id']}_excess",
                "tenant": candidate["tenant"],
                "amount": excess_amount,
                "currency": candidate["currency"],
                "reason": "overpayment",
            },
        )
        return {
            "ok": True,
            "decision": "apply_and_record_excess",
            "state": excess["state"],
            "applied": applied,
            "excess_unapplied_cash": excess["unapplied_cash"],
            "required_tables": (
                "ar_cash_receipt",
                "ar_cash_application",
                "ar_invoice",
                "ar_unapplied_cash",
                "ar_cash_pool",
            ),
            "event_contract": "AppGen-X",
            "shared_table_access": False,
            "side_effects": (),
        }

    applied = ar_credit_apply_cash(
        state,
        {
            **candidate,
            "remittance": remittance,
        },
    )
    return {
        **applied,
        "remittance": remittance,
        "required_tables": ("ar_cash_receipt", "ar_cash_application", "ar_invoice", "ar_cash_pool"),
        "event_contract": "AppGen-X",
        "shared_table_access": False,
        "side_effects": (),
    }


def ar_credit_build_collections_follow_up(state: dict, *, customer_id: str, as_of: str) -> dict:
    """Assemble aging, dunning, and statement evidence for one customer."""
    customer = state.get("customers", {}).get(customer_id)
    if customer is None:
        return {
            "ok": False,
            "reason": "unknown_customer",
            "customer_id": customer_id,
            "side_effects": (),
        }
    tenant = customer["tenant"]
    aging = ar_credit_calculate_aging(state, tenant=tenant, as_of=as_of)
    statement = ar_credit_generate_customer_statement(state, customer_id=customer_id, as_of=as_of)
    dunning = ar_credit_create_dunning_plan(state, tenant=tenant, as_of=as_of)
    customer_invoice_ids = {
        invoice["invoice_id"]
        for invoice in state.get("invoices", {}).values()
        if invoice.get("customer_id") == customer_id
    }
    customer_notices = tuple(
        notice for notice in dunning["notices"] if notice["invoice_id"] in customer_invoice_ids
    )
    max_days_past_due = max((notice["days_past_due"] for notice in customer_notices), default=0)
    recommended_action = (
        "schedule_collections_call"
        if max_days_past_due > 30
        else "send_statement"
        if statement["statement"]["open_balance"] > 0
        else "monitor"
    )
    return {
        "ok": True,
        "customer_id": customer_id,
        "tenant": tenant,
        "as_of": as_of,
        "aging": aging,
        "statement": statement["statement"],
        "dunning_notices": customer_notices,
        "recommended_action": recommended_action,
        "required_tables": (
            "ar_invoice",
            "ar_statement",
            "ar_dunning_notice",
            "ar_collection_action",
        ),
        "event_contract": "AppGen-X",
        "shared_table_access": False,
        "side_effects": (),
    }


def ar_credit_workflow_release_evidence() -> dict:
    """Return release evidence for the implemented AR workflow slice."""
    return {
        "ok": True,
        "pbc": "ar_credit",
        "implemented_backlog_items": AR_CREDIT_IMPLEMENTED_BACKLOG_ITEMS,
        "workflow_operations": AR_CREDIT_WORKFLOW_OPERATIONS,
        "generated_artifacts": {
            "credit_onboarding": {
                "operation": "review_credit_onboarding",
                "owned_tables": ("ar_customer", "ar_customer_credit_profile", "ar_credit_decision"),
            },
            "invoice_readiness": {
                "operation": "review_invoice_readiness",
                "owned_tables": ("ar_invoice", "ar_invoice_line", "ar_invoice_tax", "ar_invoice_performance_obligation"),
            },
            "receipt_application": {
                "operation": "execute_receipt_application",
                "owned_tables": ("ar_cash_receipt", "ar_cash_application", "ar_unapplied_cash", "ar_cash_pool"),
            },
            "collections_follow_up": {
                "operation": "build_collections_follow_up",
                "owned_tables": ("ar_statement", "ar_dunning_notice", "ar_collection_action", "ar_invoice"),
            },
        },
        "owned_tables": AR_CREDIT_OWNED_TABLES,
        "event_contract": "AppGen-X",
        "shared_table_access": False,
        "side_effects": (),
    }


def _risk_probability(signals: dict, *, graph_degree: int) -> float:
    raw = (
        float(signals.get("sanction_hits", 0.0)) * 0.65
        + float(signals.get("payment_latency", 0.0)) * 0.25
        + float(signals.get("industry_stress", 0.0)) * 0.35
        + graph_degree * 0.03
        + 0.02
    )
    return round(max(0.01, min(0.99, raw)), 4)


def _risk_grade(probability: float) -> str:
    if probability <= 0.1:
        return "A"
    if probability <= 0.2:
        return "B"
    if probability <= 0.35:
        return "C"
    if probability <= 0.5:
        return "D"
    return "E"


def _digest(payload: object) -> str:
    return hashlib.sha256(repr(payload).encode("utf-8")).hexdigest()
