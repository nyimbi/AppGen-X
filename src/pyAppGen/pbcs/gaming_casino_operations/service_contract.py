"""Service-contract wrapper for gaming_casino_operations."""

from __future__ import annotations

from .runtime import gaming_casino_operations_build_service_contract


def build_service_contract() -> dict:
    return gaming_casino_operations_build_service_contract()


def smoke_test() -> dict:
    contract = build_service_contract()
    return {"ok": contract["ok"], "contract": contract, "side_effects": ()}
