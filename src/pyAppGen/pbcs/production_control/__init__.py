"""Production Control PBC implementation package."""

from ..source_contract import source_pbc_package_contract

PBC_KEY = "production_control"


def implementation_contract() -> dict:
    return source_pbc_package_contract(PBC_KEY)
