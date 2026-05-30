"""Model contracts for provider_revenue_cycle."""

from __future__ import annotations

from .runtime import provider_revenue_cycle_build_schema_contract


def model_contracts():
    return provider_revenue_cycle_build_schema_contract()["models"]
