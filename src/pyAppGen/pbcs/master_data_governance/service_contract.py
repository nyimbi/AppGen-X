"""Service contract for the standalone master_data_governance slice."""
from __future__ import annotations

from .standalone import standalone_service_operation_contracts

PBC_KEY = "master_data_governance"



def build_service_contract():
    manifest = standalone_service_operation_contracts()
    return {
        "format": "appgen.master-data-governance-service-contract.v1",
        "ok": manifest["ok"],
        "pbc": PBC_KEY,
        "command_methods": manifest["command_operations"],
        "query_methods": manifest["query_operations"],
        "shared_table_access": False,
        "transaction_boundary": "package_local_sqlite_plus_outbox",
        "event_contract": "AppGen-X",
        "store_contract": manifest["store_contract"],
        "side_effects": (),
    }



def master_data_governance_build_service_contract():
    return build_service_contract()



def validate_service_contract():
    contract = build_service_contract()
    return {
        "ok": contract["ok"] and bool(contract["command_methods"]) and bool(contract["query_methods"]) and contract["shared_table_access"] is False,
        "contract": contract,
        "side_effects": (),
    }



def smoke_test():
    return validate_service_contract()
