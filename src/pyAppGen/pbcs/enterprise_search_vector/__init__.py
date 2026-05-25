"""Enterprise Search Vector PBC implementation package."""

from ..source_contract import source_pbc_package_contract

PBC_KEY = "enterprise_search_vector"


def implementation_contract() -> dict:
    return source_pbc_package_contract(PBC_KEY)
