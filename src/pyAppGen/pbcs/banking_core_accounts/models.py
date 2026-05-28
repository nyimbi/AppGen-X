"""Database-backed model surfaces for banking_core_accounts."""
from __future__ import annotations

from dataclasses import dataclass

from .lifecycle import LIFECYCLE_STATES
from .runtime import banking_core_accounts_build_schema_contract


@dataclass(frozen=True)
class DepositAccountRow:
    id: str
    tenant: str
    account_number: str
    customer_id: str
    product_code: str
    currency: str
    lifecycle_state: str
    maker_checker_required: bool
    last_transition_reason: str | None = None


@dataclass(frozen=True)
class DepositAccountTransitionRow:
    account_id: str
    from_state: str | None
    to_state: str
    actor_id: str
    approver_id: str | None = None
    reason: str | None = None


def lifecycle_model_manifest():
    schema = banking_core_accounts_build_schema_contract()
    return {
        "ok": True,
        "models": (
            {
                "name": "DepositAccountRow",
                "table": "banking_core_accounts_deposit_account",
                "fields": tuple(DepositAccountRow.__dataclass_fields__),
                "allowed_lifecycle_states": LIFECYCLE_STATES,
            },
            {
                "name": "DepositAccountTransitionRow",
                "table": "banking_core_accounts_deposit_account",
                "fields": tuple(DepositAccountTransitionRow.__dataclass_fields__),
                "allowed_lifecycle_states": LIFECYCLE_STATES,
            },
        ),
        "schema_models": schema["models"],
        "side_effects": (),
    }


def model_contracts():
    return banking_core_accounts_build_schema_contract()["models"]
