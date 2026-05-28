"""Service contract for the customer_success_management PBC."""
from __future__ import annotations

from .slice_app import build_service_contract as _build_service_contract


def build_service_contract() -> dict:
    return _build_service_contract()


def customer_success_management_build_service_contract() -> dict:
    return build_service_contract()


def validate_service_contract() -> dict:
    contract = build_service_contract()
    return {
        "ok": contract["ok"]
        and bool(contract["command_methods"])
        and bool(contract["query_methods"])
        and contract["shared_table_access"] is False,
        "contract": contract,
        "side_effects": (),
    }


def smoke_test() -> dict:
    validation = validate_service_contract()
    return {"ok": validation["ok"], "validation": validation, "side_effects": ()}
