"""Returns and Reverse Logistics PBC implementation package."""

from ..source_contract import source_pbc_package_contract

PBC_KEY = "returns_reverse_logistics"


def implementation_contract() -> dict:
    return source_pbc_package_contract(PBC_KEY)
