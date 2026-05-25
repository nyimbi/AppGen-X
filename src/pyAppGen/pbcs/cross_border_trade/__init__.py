"""Cross Border Trade PBC implementation package."""

from ..source_contract import source_pbc_package_contract

PBC_KEY = "cross_border_trade"


def implementation_contract() -> dict:
    return source_pbc_package_contract(PBC_KEY)
