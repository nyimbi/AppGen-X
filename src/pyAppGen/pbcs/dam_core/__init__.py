"""Digital Asset Management Core PBC implementation package."""

from ..source_contract import source_pbc_package_contract

PBC_KEY = "dam_core"


def implementation_contract() -> dict:
    return source_pbc_package_contract(PBC_KEY)
