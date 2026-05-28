"""Schema contract wrapper for case_knowledge_management."""

from __future__ import annotations

from .models import build_schema_contract as _build_schema_contract


def build_schema_contract() -> dict:
    return _build_schema_contract()


def case_knowledge_management_build_schema_contract() -> dict:
    return build_schema_contract()


def validate_schema_contract() -> dict:
    contract = build_schema_contract()
    return {
        "ok": contract["ok"]
        and contract["shared_table_access"] is False
        and bool(contract["tables"])
        and bool(contract["models"]),
        "contract": contract,
        "side_effects": (),
    }


def smoke_test() -> dict:
    return validate_schema_contract()
