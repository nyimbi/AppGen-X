"""Customer 360 PBC implementation package."""

from ..source_contract import source_pbc_package_contract

PBC_KEY = "customer_360"


def implementation_contract() -> dict:
    return source_pbc_package_contract(PBC_KEY)
