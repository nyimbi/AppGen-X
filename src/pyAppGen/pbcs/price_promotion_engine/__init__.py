"""Price Promotion Engine PBC implementation package."""

from ..source_contract import source_pbc_package_contract

PBC_KEY = "price_promotion_engine"


def implementation_contract() -> dict:
    return source_pbc_package_contract(PBC_KEY)
