"""Generated service evidence for the predictive_demand PBC."""

from __future__ import annotations

from .runtime import predictive_demand_build_service_contract

SERVICE_CONTRACT = predictive_demand_build_service_contract()


def build_service_contract():
    """Return generated command, eventing, and handler evidence."""
    return dict(SERVICE_CONTRACT)
