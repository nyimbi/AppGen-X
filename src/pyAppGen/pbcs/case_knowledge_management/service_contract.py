"""Service contract for the case_knowledge_management PBC."""

from __future__ import annotations

from .runtime import case_knowledge_management_build_service_contract


def build_service_contract() -> dict:
    return case_knowledge_management_build_service_contract()


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
    return validate_service_contract()
