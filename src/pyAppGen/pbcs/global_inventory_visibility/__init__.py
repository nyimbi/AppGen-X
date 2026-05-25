"""Global Inventory Visibility PBC implementation package."""

from ..source_contract import source_pbc_package_contract

PBC_KEY = "global_inventory_visibility"


def implementation_contract() -> dict:
    return source_pbc_package_contract(PBC_KEY)
