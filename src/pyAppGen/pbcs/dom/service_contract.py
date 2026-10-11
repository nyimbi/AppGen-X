"""Generated service evidence for the dom PBC."""

from __future__ import annotations

from . import services
from .runtime import dom_build_service_contract as _runtime_build_service_contract


def build_service_contract() -> dict:
    """Return generated command, eventing, and handler evidence.

    The domain command surface is the runtime contract's, which covers every
    owned-table mutation and advanced operation. The standalone application
    facade is reported alongside it rather than in place of it, so a facade
    method list can never shrink the contract's command depth.
    """
    contract = dict(_runtime_build_service_contract())
    operation_manifest = services.service_operation_manifest()
    standalone = operation_manifest["standalone_service"]
    contract.update(
        {
            "pbc": "dom",
            "shared_table_access": False,
            "package_service_class": operation_manifest["service_class"],
            "package_operations": operation_manifest["operations"],
            "package_command_operations": operation_manifest["command_operations"],
            "package_query_operations": operation_manifest["query_operations"],
            "package_outbox_table": operation_manifest["outbox_table"],
            "package_service_methods": standalone["service_methods"],
        }
    )
    return contract


SERVICE_CONTRACT = build_service_contract()
