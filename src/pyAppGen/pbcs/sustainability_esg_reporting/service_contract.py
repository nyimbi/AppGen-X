"""Service contract for the sustainability_esg_reporting PBC."""
from __future__ import annotations

from .slice_app import build_service_contract as _build_service_contract


def build_service_contract() -> dict:
    return _build_service_contract()


def sustainability_esg_reporting_build_service_contract() -> dict:
    return build_service_contract()


def validate_service_contract() -> dict:
    contract = build_service_contract()
    return {
        'ok': contract['ok'] and bool(contract['command_methods']) and bool(contract['query_methods']) and contract['shared_table_access'] is False,
        'contract': contract,
        'side_effects': (),
    }


def smoke_test() -> dict:
    return validate_service_contract()
