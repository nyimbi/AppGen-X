"""Executable service contract for bank_payments_clearing."""

from __future__ import annotations

from . import services


PBC_KEY = "bank_payments_clearing"


def build_service_contract() -> dict:
    manifest = services.service_operation_manifest()
    contracts = services.service_operation_contracts()
    return {
        "format": "appgen.bank-payments-clearing-service-contract.v2",
        "ok": manifest["ok"] and contracts["ok"],
        "pbc": PBC_KEY,
        "service_class": manifest["service_class"],
        "command_operations": manifest["command_operations"],
        "query_operations": manifest["query_operations"],
        "workflow_operations": manifest["workflow_operations"],
        "contracts": contracts["contracts"],
        "event_contract": manifest["event_contract"],
        "transaction_boundary": "owned_datastore_plus_outbox",
        "shared_table_access": False,
        "side_effects": (),
    }


SERVICE_CONTRACT = build_service_contract()


def validate_service_contract() -> dict:
    contract = build_service_contract()
    invalid_tables = tuple(
        table
        for item in contract["contracts"]
        for table in item["owned_tables"] + item["read_tables"]
        if not table.startswith(f"{PBC_KEY}_")
    )
    return {
        "ok": contract["ok"]
        and not invalid_tables
        and contract["shared_table_access"] is False
        and contract["event_contract"]["event_contract"] == "AppGen-X",
        "pbc": PBC_KEY,
        "invalid_tables": invalid_tables,
        "side_effects": (),
    }


def smoke_test() -> dict:
    validation = validate_service_contract()
    return {"ok": validation["ok"], "validation": validation, "side_effects": ()}
