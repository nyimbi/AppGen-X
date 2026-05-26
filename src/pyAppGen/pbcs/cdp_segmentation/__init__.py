"""CDP Segmentation PBC implementation package."""

from ..source_contract import source_pbc_package_contract
from .runtime import CDP_SEGMENTATION_ALLOWED_DATABASE_BACKENDS
from .runtime import CDP_SEGMENTATION_OWNED_TABLES
from .runtime import CDP_SEGMENTATION_RUNTIME_TABLES
from .runtime import CDP_SEGMENTATION_RUNTIME_CAPABILITY_KEYS
from .runtime import CDP_SEGMENTATION_STANDARD_FEATURE_KEYS
from .runtime import cdp_segmentation_activate_segment
from .runtime import cdp_segmentation_build_api_contract
from .runtime import cdp_segmentation_build_release_evidence
from .runtime import cdp_segmentation_build_schema_contract
from .runtime import cdp_segmentation_build_service_contract
from .runtime import cdp_segmentation_build_workbench_view
from .runtime import cdp_segmentation_configure_runtime
from .runtime import cdp_segmentation_define_segment
from .runtime import cdp_segmentation_empty_state
from .runtime import cdp_segmentation_evaluate_segments
from .runtime import cdp_segmentation_ingest_customer_event
from .runtime import cdp_segmentation_permissions_contract
from .runtime import cdp_segmentation_receive_event
from .runtime import cdp_segmentation_register_rule
from .runtime import cdp_segmentation_register_schema_extension
from .runtime import cdp_segmentation_runtime_capabilities
from .runtime import cdp_segmentation_runtime_smoke
from .runtime import cdp_segmentation_set_parameter
from .runtime import cdp_segmentation_upsert_profile_property
from .runtime import cdp_segmentation_verify_owned_table_boundary
from .ui import CDP_SEGMENTATION_UI_FRAGMENT_KEYS
from .ui import cdp_segmentation_render_workbench
from .ui import cdp_segmentation_ui_contract

PBC_KEY = "cdp_segmentation"


def implementation_contract() -> dict:
    runtime = cdp_segmentation_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": cdp_segmentation_ui_contract(),
        "api_contract": cdp_segmentation_build_api_contract(),
        "schema_contract": cdp_segmentation_build_schema_contract(),
        "service_contract": cdp_segmentation_build_service_contract(),
        "release_evidence_contract": cdp_segmentation_build_release_evidence(),
        "permissions_contract": cdp_segmentation_permissions_contract(),
        "owned_tables": CDP_SEGMENTATION_OWNED_TABLES,
        "runtime_tables": CDP_SEGMENTATION_RUNTIME_TABLES,
        "allowed_database_backends": CDP_SEGMENTATION_ALLOWED_DATABASE_BACKENDS,
    }
