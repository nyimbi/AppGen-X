"""Generated service evidence for the notifications PBC."""

from __future__ import annotations

from .runtime import notifications_build_service_contract


def build_service_contract() -> dict:
    """Return generated command, eventing, and handler evidence."""
    return notifications_build_service_contract()


SERVICE_CONTRACT = build_service_contract()
