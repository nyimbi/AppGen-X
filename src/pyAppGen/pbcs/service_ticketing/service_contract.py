"""Service contract evidence for the service_ticketing PBC."""

from __future__ import annotations

from .runtime import service_ticketing_build_service_contract


def build_service_contract() -> dict:
    """Return generated command, eventing, and handler evidence."""
    return dict(service_ticketing_build_service_contract())


SERVICE_CONTRACT = build_service_contract()
