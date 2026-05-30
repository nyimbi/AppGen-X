"""Generated owned schema evidence for the sustainability_esg_reporting PBC."""
from __future__ import annotations

from .slice_app import build_schema_contract as _build_schema_contract

SCHEMA_CONTRACT = _build_schema_contract()


def build_schema_contract() -> dict:
    return _build_schema_contract()


def sustainability_esg_reporting_build_schema_contract() -> dict:
    return build_schema_contract()


def validate_schema_contract() -> dict:
    contract = build_schema_contract()
    return {
        'ok': contract['ok'] and len(contract['owned_tables']) >= 24 and contract['shared_table_access'] is False,
        'contract': contract,
        'side_effects': (),
    }


def smoke_test() -> dict:
    return validate_schema_contract()
