"""Fraud Anomaly Detection PBC implementation package."""

from ..source_contract import source_pbc_package_contract

PBC_KEY = "fraud_anomaly_detection"


def implementation_contract() -> dict:
    return source_pbc_package_contract(PBC_KEY)
