"""Generated service evidence for the enterprise_search_vector PBC."""

from __future__ import annotations

from .runtime import enterprise_search_vector_build_service_contract


def build_service_contract() -> dict:
    """Return generated command, eventing, and handler evidence."""
    return enterprise_search_vector_build_service_contract()


SERVICE_CONTRACT = build_service_contract()
