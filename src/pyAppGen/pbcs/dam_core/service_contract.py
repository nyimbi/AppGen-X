"""Generated service evidence for the dam_core PBC."""

from __future__ import annotations

from . import services
from .runtime import dam_core_build_service_contract as _runtime_build_service_contract


def build_service_contract() -> dict:
    """Return generated command, eventing, and handler evidence."""
    contract = dict(_runtime_build_service_contract())
    operation_manifest = services.service_operation_manifest()
    contract.update(
        {
            "package_service_class": operation_manifest["service_class"],
            "package_operations": operation_manifest["operations"],
            "package_command_operations": operation_manifest["command_operations"],
            "package_query_operations": operation_manifest["query_operations"],
            "package_outbox_table": operation_manifest["outbox_table"],
        }
    )
    return contract


SERVICE_CONTRACT = build_service_contract()
