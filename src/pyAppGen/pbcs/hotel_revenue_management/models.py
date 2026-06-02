"""Owned model metadata for hotel_revenue_management."""

from __future__ import annotations

from .runtime import hotel_revenue_management_build_schema_contract
from .runtime import PBC_KEY


OWNED_SCHEMA = hotel_revenue_management_build_schema_contract()


def model_contracts() -> tuple[dict, ...]:
    return OWNED_SCHEMA["models"]


def owned_model_manifest() -> dict:
    return {
        "ok": OWNED_SCHEMA["ok"],
        "pbc": PBC_KEY,
        "models": OWNED_SCHEMA["models"],
        "owned_tables": OWNED_SCHEMA["owned_tables"],
        "side_effects": (),
    }
