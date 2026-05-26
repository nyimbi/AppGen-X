"""Quality Assurance PBC implementation package."""

from ..source_contract import source_pbc_package_contract
from .runtime import QUALITY_ASSURANCE_ALLOWED_DATABASE_BACKENDS
from .runtime import QUALITY_ASSURANCE_CONSUMED_EVENT_TYPES
from .runtime import QUALITY_ASSURANCE_EMITTED_EVENT_TYPES
from .runtime import QUALITY_ASSURANCE_OWNED_TABLES
from .runtime import QUALITY_ASSURANCE_REQUIRED_EVENT_TOPIC
from .runtime import QUALITY_ASSURANCE_RUNTIME_CAPABILITY_KEYS
from .runtime import QUALITY_ASSURANCE_STANDARD_FEATURE_KEYS
from .runtime import quality_assurance_build_api_contract
from .runtime import quality_assurance_build_workbench_view
from .runtime import quality_assurance_configure_runtime
from .runtime import quality_assurance_create_inspection_plan
from .runtime import quality_assurance_create_quality_hold
from .runtime import quality_assurance_disposition_nonconformance
from .runtime import quality_assurance_empty_state
from .runtime import quality_assurance_permissions_contract
from .runtime import quality_assurance_raise_nonconformance
from .runtime import quality_assurance_receive_event
from .runtime import quality_assurance_record_inspection_result
from .runtime import quality_assurance_register_rule
from .runtime import quality_assurance_register_schema_extension
from .runtime import quality_assurance_release_quality_hold
from .runtime import quality_assurance_runtime_capabilities
from .runtime import quality_assurance_runtime_smoke
from .runtime import quality_assurance_set_parameter
from .runtime import quality_assurance_verify_owned_table_boundary
from .ui import QUALITY_ASSURANCE_UI_FRAGMENT_KEYS
from .ui import quality_assurance_render_workbench
from .ui import quality_assurance_ui_contract

PBC_KEY = "quality_assurance"


def implementation_contract() -> dict:
    runtime = quality_assurance_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "owned_tables": QUALITY_ASSURANCE_OWNED_TABLES,
        "allowed_database_backends": QUALITY_ASSURANCE_ALLOWED_DATABASE_BACKENDS,
        "api_contract": quality_assurance_build_api_contract(),
        "permissions_contract": quality_assurance_permissions_contract(),
        "advanced_runtime": runtime,
        "ui_contract": quality_assurance_ui_contract(),
    }
