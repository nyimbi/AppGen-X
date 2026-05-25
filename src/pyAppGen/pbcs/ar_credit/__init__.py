"""Accounts Receivable and Credit PBC implementation package."""

from ..source_contract import source_pbc_package_contract

PBC_KEY = "ar_credit"


def implementation_contract() -> dict:
    return source_pbc_package_contract(PBC_KEY)
