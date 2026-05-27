"""Service evidence for the audit_ledger PBC."""

from __future__ import annotations

from .runtime import audit_ledger_build_service_contract

SERVICE_CONTRACT = {
    **audit_ledger_build_service_contract(),
    "pbc": "audit_ledger",
    "shared_table_access": False,
}


def build_service_contract() -> dict:
    """Return command, query, dependency, and boundary evidence."""
    return dict(SERVICE_CONTRACT)
