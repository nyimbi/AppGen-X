"""Generated service evidence for the checkout_processing PBC."""

from __future__ import annotations

from .runtime import checkout_processing_build_service_contract


SERVICE_CONTRACT = checkout_processing_build_service_contract()


def build_service_contract():
    """Return generated command, eventing, and handler evidence."""
    return dict(SERVICE_CONTRACT)


def validate_service_contract():
    contract = build_service_contract()
    finalization_commands = {"confirm_inventory_reservation", "authorize_payment_intent", "capture_payment_intent"}
    return {
        "ok": contract["ok"]
        and contract.get("shared_table_access") is False
        and finalization_commands <= set(contract["command_methods"]),
        "contract": contract,
        "side_effects": (),
    }


def smoke_test():
    return validate_service_contract()
