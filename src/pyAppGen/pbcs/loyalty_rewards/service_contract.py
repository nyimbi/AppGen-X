"""Generated service evidence for the loyalty_rewards PBC."""

from __future__ import annotations

from .runtime import loyalty_rewards_build_service_contract


def build_service_contract() -> dict:
    """Return generated command, eventing, and handler evidence."""
    return loyalty_rewards_build_service_contract()


SERVICE_CONTRACT = build_service_contract()
