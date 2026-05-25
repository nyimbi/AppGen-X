"""Federated Identity and Access PBC implementation package."""

from ..source_contract import source_pbc_package_contract

PBC_KEY = "federated_iam"


def implementation_contract() -> dict:
    return source_pbc_package_contract(PBC_KEY)
