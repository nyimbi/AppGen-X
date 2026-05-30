"""Schema-contract wrapper for gaming_casino_operations."""

from __future__ import annotations

from .runtime import gaming_casino_operations_build_schema_contract


def build_schema_contract() -> dict:
    return gaming_casino_operations_build_schema_contract()


def smoke_test() -> dict:
    contract = build_schema_contract()
    return {"ok": contract["ok"], "contract": contract, "side_effects": ()}
