"""Service contract facade for the multi_sided_market PBC."""

from __future__ import annotations

from .runtime import multi_sided_market_build_service_contract

PBC_KEY = "multi_sided_market"

SERVICE_CONTRACT = {
    **multi_sided_market_build_service_contract(),
    "pbc": PBC_KEY,
    "shared_table_access": False,
}


def build_service_contract():
    return dict(SERVICE_CONTRACT)


def validate_service_contract():
    contract = build_service_contract()
    return {
        "ok": contract["ok"]
        and contract["pbc"] == PBC_KEY
        and contract["shared_table_access"] is False
        and contract["transaction_boundary"] == "owned_datastore_plus_outbox"
        and bool(contract["command_methods"]),
        "contract": contract,
        "side_effects": (),
    }


def smoke_test():
    return validate_service_contract()
