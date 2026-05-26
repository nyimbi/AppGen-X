"""Digital Asset Management Core PBC implementation package."""

from ..source_contract import source_pbc_package_contract
from .runtime import DAM_CORE_ALLOWED_DATABASE_BACKENDS
from .runtime import DAM_CORE_OWNED_TABLES
from .runtime import DAM_CORE_RUNTIME_TABLES
from .runtime import DAM_CORE_RUNTIME_CAPABILITY_KEYS
from .runtime import DAM_CORE_STANDARD_FEATURE_KEYS
from .runtime import dam_core_add_metadata_tag
from .runtime import dam_core_attach_rights_policy
from .runtime import dam_core_build_api_contract
from .runtime import dam_core_build_release_evidence
from .runtime import dam_core_build_schema_contract
from .runtime import dam_core_build_service_contract
from .runtime import dam_core_build_workbench_view
from .runtime import dam_core_complete_rendition
from .runtime import dam_core_configure_runtime
from .runtime import dam_core_empty_state
from .runtime import dam_core_enforce_rights
from .runtime import dam_core_permissions_contract
from .runtime import dam_core_receive_event
from .runtime import dam_core_register_asset
from .runtime import dam_core_register_rule
from .runtime import dam_core_register_schema_extension
from .runtime import dam_core_request_rendition
from .runtime import dam_core_runtime_capabilities
from .runtime import dam_core_runtime_smoke
from .runtime import dam_core_set_parameter
from .runtime import dam_core_verify_owned_table_boundary
from .ui import DAM_CORE_UI_FRAGMENT_KEYS
from .ui import dam_core_render_workbench
from .ui import dam_core_ui_contract

PBC_KEY = "dam_core"


def implementation_contract() -> dict:
    runtime = dam_core_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": dam_core_ui_contract(),
        "api_contract": dam_core_build_api_contract(),
        "schema_contract": dam_core_build_schema_contract(),
        "service_contract": dam_core_build_service_contract(),
        "release_evidence_contract": dam_core_build_release_evidence(),
        "permissions_contract": dam_core_permissions_contract(),
        "owned_tables": DAM_CORE_OWNED_TABLES,
        "runtime_tables": DAM_CORE_RUNTIME_TABLES,
        "allowed_database_backends": DAM_CORE_ALLOWED_DATABASE_BACKENDS,
    }
