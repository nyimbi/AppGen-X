"""Service contract for the contract_lifecycle PBC."""

from .application import PBC_KEY, service_contract


def build_service_contract():
    return service_contract()


def contract_lifecycle_build_service_contract():
    return build_service_contract()


def validate_service_contract():
    contract = build_service_contract()
    return {
        "ok": contract["ok"]
        and bool(contract["command_methods"])
        and bool(contract["query_methods"])
        and contract["shared_table_access"] is False,
        "contract": contract,
    }


def smoke_test():
    return validate_service_contract()
