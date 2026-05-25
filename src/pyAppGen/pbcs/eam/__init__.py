"""Enterprise Asset Management PBC implementation package."""

from ..source_contract import source_pbc_package_contract

PBC_KEY = "eam"


def implementation_contract() -> dict:
    return source_pbc_package_contract(PBC_KEY)
