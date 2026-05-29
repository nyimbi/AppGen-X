"""Guided AP workflow wizards for the standalone Accounts Payable slice."""

from __future__ import annotations

from .forms import form_contract
from .repository import build_demo_state
from .runtime import ap_automation_capture_invoice
from .runtime import ap_automation_create_payment_batch
from .runtime import ap_automation_execute_payment
from .runtime import ap_automation_generate_remittance_advice
from .runtime import ap_automation_onboard_vendor
from .runtime import ap_automation_receive_event
from .runtime import ap_automation_reconcile_vendor_statement
from .runtime import ap_automation_register_vendor_tax_profile
from .runtime import ap_automation_schedule_payments
from .runtime import ap_automation_screen_vendor_network
from .runtime import ap_automation_validate_vendor_bank_account


WIZARD_DEFINITIONS = (
    {
        "wizard_id": "vendor_onboarding_wizard",
        "title": "Vendor Readiness Wizard",
        "forms": ("vendor_onboarding",),
        "steps": (
            "capture_vendor_master",
            "approve_vendor",
            "validate_bank_account",
            "register_tax_profile",
            "screen_vendor_network",
        ),
        "completion_action": "onboard_vendor",
    },
    {
        "wizard_id": "invoice_capture_wizard",
        "title": "Invoice Intake Wizard",
        "forms": ("invoice_capture",),
        "steps": (
            "capture_invoice",
            "validate_duplicate_controls",
            "surface_match_queue",
        ),
        "completion_action": "capture_invoice",
    },
    {
        "wizard_id": "payment_release_wizard",
        "title": "Payment Release Wizard",
        "forms": ("payment_batch_release",),
        "steps": (
            "schedule_payments",
            "create_batch",
            "execute_payment",
            "generate_remittance_advice",
        ),
        "completion_action": "execute_payment",
    },
    {
        "wizard_id": "vendor_statement_wizard",
        "title": "Statement Reconciliation Wizard",
        "forms": ("vendor_statement_reconciliation",),
        "steps": (
            "load_vendor_statement",
            "reconcile_statement",
            "raise_exceptions",
        ),
        "completion_action": "reconcile_vendor_statement",
    },
)


def wizard_contract() -> dict:
    """Return the wizard surface that stitches AP forms into guided workflows."""
    forms = {form["form_id"] for form in form_contract()["forms"]}
    return {
        "format": "appgen.ap-automation-wizards.v1",
        "ok": bool(WIZARD_DEFINITIONS) and all(set(item["forms"]) <= forms for item in WIZARD_DEFINITIONS),
        "pbc": "ap_automation",
        "wizards": WIZARD_DEFINITIONS,
        "side_effects": (),
    }


def plan_wizard(wizard_id: str, *, tenant: str) -> dict:
    """Plan a wizard without mutating state."""
    definition = next((wizard for wizard in WIZARD_DEFINITIONS if wizard["wizard_id"] == wizard_id), None)
    return {
        "ok": definition is not None,
        "tenant": tenant,
        "wizard": dict(definition) if definition else None,
        "side_effects": (),
    }


def execute_wizard(wizard_id: str, state: dict, payload: dict) -> dict:
    """Execute a guided AP workflow against the in-package runtime."""
    if wizard_id == "vendor_onboarding_wizard":
        vendor_result = ap_automation_onboard_vendor(state, payload["vendor"])
        state = vendor_result["state"]
        state = ap_automation_receive_event(state, payload["approval_event"])["state"]
        state = ap_automation_validate_vendor_bank_account(state, payload["bank_account"])["state"]
        state = ap_automation_register_vendor_tax_profile(state, payload["tax_profile"])["state"]
        screening = ap_automation_screen_vendor_network(
            state,
            payload["vendor"]["vendor_id"],
            sanction_entities=tuple(payload.get("sanction_entities", ())),
        )
        return {
            "ok": screening["ok"],
            "wizard_id": wizard_id,
            "state": screening["state"],
            "result": screening,
            "side_effects": (),
        }
    if wizard_id == "invoice_capture_wizard":
        result = ap_automation_capture_invoice(state, payload["invoice"])
        return {
            "ok": result["ok"],
            "wizard_id": wizard_id,
            "state": result["state"],
            "result": result,
            "side_effects": (),
        }
    if wizard_id == "payment_release_wizard":
        scheduled = ap_automation_schedule_payments(
            state,
            tenant=payload["tenant"],
            liquidity_forecast=tuple(payload["liquidity_forecast"]),
            risk_limit=float(payload.get("risk_limit", 0.7)),
        )
        state = scheduled["state"]
        selected = tuple(
            payment["payment_id"]
            for payment in scheduled["payments"]
            if payment["status"] == "scheduled"
        )
        batch = ap_automation_create_payment_batch(
            state,
            {
                "tenant": payload["tenant"],
                "payment_ids": selected,
                "batch_id": payload.get("batch_id", "batch_wizard_1"),
            },
        )
        state = batch["state"]
        payment = ap_automation_execute_payment(
            state,
            selected[0],
            rails=tuple(payload["rails"]),
        )
        state = payment["state"]
        advice = ap_automation_generate_remittance_advice(
            state,
            selected[0],
            delivery_channel=payload.get("delivery_channel", "portal"),
        )
        return {
            "ok": scheduled["ok"] and batch["ok"] and payment["ok"] and advice["ok"],
            "wizard_id": wizard_id,
            "state": advice["state"],
            "result": {
                "schedule": scheduled,
                "batch": batch,
                "payment": payment,
                "advice": advice,
            },
            "side_effects": (),
        }
    if wizard_id == "vendor_statement_wizard":
        result = ap_automation_reconcile_vendor_statement(state, payload["statement"])
        return {
            "ok": result["ok"],
            "wizard_id": wizard_id,
            "state": result["state"],
            "result": result,
            "side_effects": (),
        }
    return {"ok": False, "wizard_id": wizard_id, "reason": "unknown_wizard", "side_effects": ()}


def smoke_test() -> dict:
    """Exercise planning plus one guided payment-release run."""
    state = build_demo_state(include_release=False)
    plan = plan_wizard("payment_release_wizard", tenant="tenant_repo")
    executed = execute_wizard(
        "payment_release_wizard",
        state,
        {
            "tenant": "tenant_repo",
            "liquidity_forecast": (5000, 4900, 4800),
            "risk_limit": 0.7,
            "batch_id": "batch_wizard_repo",
            "delivery_channel": "portal",
            "rails": (
                {"rail": "instant_bank_api", "cost": 5, "latency": 2, "fx_rate": 1.0, "available": False},
                {"rail": "ach", "cost": 1, "latency": 24, "fx_rate": 1.0, "available": True},
            ),
        },
    )
    return {
        "ok": wizard_contract()["ok"] and plan["ok"] and executed["ok"],
        "contract": wizard_contract(),
        "plan": plan,
        "executed": executed,
        "side_effects": (),
    }
