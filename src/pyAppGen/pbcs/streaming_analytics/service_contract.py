"""Generated service evidence for the streaming_analytics PBC."""

from __future__ import annotations

from .runtime import streaming_analytics_build_service_contract

PBC_KEY = "streaming_analytics"


SERVICE_CONTRACT = {
    **streaming_analytics_build_service_contract(),
    "pbc": PBC_KEY,
    "shared_table_access": False,
}


def build_service_contract() -> dict:
    """Return generated command, eventing, and handler evidence."""
    return dict(SERVICE_CONTRACT)


def smoke_test() -> dict:
    """Exercise the generated service contract side-effect-free."""
    contract = build_service_contract()
    return {
        "ok": contract["ok"] and bool(contract["command_methods"]) and bool(contract["query_methods"]),
        "contract": contract,
        "side_effects": (),
    }
