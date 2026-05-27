"""Generated service evidence for the streaming_analytics PBC."""

from __future__ import annotations

from .runtime import streaming_analytics_build_service_contract


def build_service_contract() -> dict:
    """Return generated command, eventing, and handler evidence."""
    return streaming_analytics_build_service_contract()


SERVICE_CONTRACT = build_service_contract()
