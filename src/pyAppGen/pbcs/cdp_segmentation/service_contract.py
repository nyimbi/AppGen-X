"""Generated service evidence for the cdp_segmentation PBC."""

from __future__ import annotations

from .runtime import cdp_segmentation_build_service_contract


def build_service_contract() -> dict:
    """Return generated command, eventing, and handler evidence."""
    return cdp_segmentation_build_service_contract()


SERVICE_CONTRACT = build_service_contract()
