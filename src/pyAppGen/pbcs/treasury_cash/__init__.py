"""Treasury and Cash Management PBC implementation package."""

from ..source_contract import source_pbc_package_contract

PBC_KEY = "treasury_cash"


def implementation_contract() -> dict:
    return source_pbc_package_contract(PBC_KEY)
