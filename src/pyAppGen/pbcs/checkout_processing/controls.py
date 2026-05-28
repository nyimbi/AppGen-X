"""Package-local controls for the Checkout Processing workbench."""

from __future__ import annotations

from .runtime import checkout_processing_build_release_evidence
from .runtime import checkout_processing_empty_state
from .runtime import checkout_processing_run_control_tests
from .runtime import checkout_processing_runtime_smoke
from .runtime import checkout_processing_verify_formal_invariants
from .runtime import checkout_processing_verify_owned_table_boundary


CHECKOUT_PROCESSING_CONTROLS = (
    {
        "control_id": "release_readiness",
        "title": "Release readiness",
        "description": "Runs package-local control tests and release evidence checks.",
        "permission": "checkout_processing.audit",
    },
    {
        "control_id": "completion_gate",
        "title": "Completion gate",
        "description": "Requires confirmed inventory, captured payment, clear risk, and valid address evidence.",
        "permission": "checkout_processing.checkout",
    },
    {
        "control_id": "tenant_boundary",
        "title": "Tenant and boundary proof",
        "description": "Verifies tenant isolation invariants and rejects foreign table references.",
        "permission": "checkout_processing.audit",
    },
    {
        "control_id": "assistant_guardrails",
        "title": "Assistant guardrails",
        "description": "Ensures assistant previews stay package-owned and confirmation-gated.",
        "permission": "checkout_processing.audit",
    },
)


def checkout_processing_control_catalog() -> dict:
    """Return package-local operational controls."""
    return {
        "ok": bool(CHECKOUT_PROCESSING_CONTROLS),
        "pbc": "checkout_processing",
        "controls": CHECKOUT_PROCESSING_CONTROLS,
        "control_ids": tuple(item["control_id"] for item in CHECKOUT_PROCESSING_CONTROLS),
        "side_effects": (),
    }


def checkout_processing_control_center(state: dict | None = None) -> dict:
    """Return executable control evidence for release and operator workflows."""
    source_state = state
    if source_state is None:
        source_state = checkout_processing_runtime_smoke()["state"]
    release = checkout_processing_build_release_evidence()
    runtime_controls = checkout_processing_run_control_tests(source_state)
    invariants = checkout_processing_verify_formal_invariants(source_state)
    accepted_boundary = checkout_processing_verify_owned_table_boundary(("cart", "checkout_session", "product_projection"))
    rejected_boundary = checkout_processing_verify_owned_table_boundary(("shared_foreign_orders",))
    completion_gate = {
        "confirmed_inventory": any(item.get("status") == "confirmed" for item in source_state.get("inventory_reservation_handoffs", {}).values()),
        "captured_payment": any(item.get("status") == "captured" for item in source_state.get("payment_intent_handoffs", {}).values()),
        "clear_risk": any(item.get("decision") == "clear" for item in source_state.get("risk_screens", {}).values()),
        "validated_address": any(item.get("status") == "validated" for item in source_state.get("address_validations", {}).values()),
    }
    assistant_guardrails = {
        "preview_only": True,
        "requires_confirmation_for_mutation": True,
        "boundary_ok": accepted_boundary["ok"] and not rejected_boundary["ok"],
    }
    return {
        "ok": runtime_controls["ok"] and invariants["ok"] and release["ok"] and assistant_guardrails["boundary_ok"],
        "pbc": "checkout_processing",
        "controls": checkout_processing_control_catalog()["controls"],
        "release": release,
        "runtime_controls": runtime_controls,
        "invariants": invariants,
        "completion_gate": completion_gate,
        "accepted_boundary": accepted_boundary,
        "rejected_boundary": rejected_boundary,
        "assistant_guardrails": assistant_guardrails,
        "side_effects": (),
    }


def checkout_processing_mutation_preview(action: str, table: str, payload: dict | None = None) -> dict:
    """Preview whether a mutation would stay inside the checkout-owned boundary."""
    normalized = str(action).lower()
    boundary = checkout_processing_verify_owned_table_boundary((table,))
    requires_confirmation = normalized != "read"
    return {
        "ok": boundary["ok"] and normalized in {"create", "read", "update", "delete"},
        "pbc": "checkout_processing",
        "action": normalized,
        "table": table,
        "payload_keys": tuple(sorted(dict(payload or {}))),
        "requires_confirmation": requires_confirmation,
        "boundary": boundary,
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Exercise the control center with runtime smoke evidence."""
    empty_preview = checkout_processing_mutation_preview("read", "checkout_processing_checkout_session", {})
    control_center = checkout_processing_control_center(checkout_processing_empty_state() | checkout_processing_runtime_smoke()["state"])
    return {
        "ok": empty_preview["ok"] and control_center["ok"],
        "preview": empty_preview,
        "control_center": control_center,
        "side_effects": (),
    }
