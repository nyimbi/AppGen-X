"""Generated service evidence for the price_promotion_engine PBC."""

from __future__ import annotations

from .runtime import price_promotion_engine_build_service_contract


SERVICE_CONTRACT = price_promotion_engine_build_service_contract()


def build_service_contract():
    """Return generated command, eventing, and handler evidence."""
    return dict(SERVICE_CONTRACT)


def validate_service_contract():
    contract = build_service_contract()
    return {
        "ok": contract["ok"]
        and contract["shared_table_access"] is False
        and "receive_event" in contract["idempotent_handlers"]
        and {"approve_promotion", "redeem_coupon"} <= set(contract["command_methods"]),
        "contract": contract,
        "side_effects": (),
    }


def smoke_test():
    return validate_service_contract()
