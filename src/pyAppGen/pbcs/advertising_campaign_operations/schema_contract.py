"""Schema contract wrapper for the advertising campaign standalone slice."""

from __future__ import annotations

from .models import DOMAIN_MODELS
from .runtime import advertising_campaign_operations_build_schema_contract


def build_schema_contract() -> dict:
    schema_contract = advertising_campaign_operations_build_schema_contract()
    return {
        **schema_contract,
        "domain_models": DOMAIN_MODELS,
    }
