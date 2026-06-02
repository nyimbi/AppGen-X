"""Service contract for the insurance_claims_policy PBC."""

from __future__ import annotations

from .services import service_operation_contracts

PBC_KEY = "insurance_claims_policy"


def build_service_contract() -> dict:
    contracts = service_operation_contracts()
    return {
        "format": "appgen.insurance-claims-policy-service-contract.v1",
        "ok": contracts["ok"],
        "pbc": PBC_KEY,
        "command_methods": contracts["command_operations"],
        "query_methods": contracts["query_operations"],
        "shared_table_access": False,
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
        "contracts": contracts["contracts"],
        "side_effects": (),
    }


def insurance_claims_policy_build_service_contract() -> dict:
    return build_service_contract()


def validate_service_contract() -> dict:
    contract = build_service_contract()
    return {
        "ok": contract["ok"] and bool(contract["command_methods"]) and bool(contract["query_methods"]) and contract["shared_table_access"] is False,
        "contract": contract,
        "side_effects": (),
    }


def smoke_test() -> dict:
    return validate_service_contract()
