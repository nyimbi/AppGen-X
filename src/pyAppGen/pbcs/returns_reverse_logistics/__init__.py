"""Returns and Reverse Logistics PBC implementation package."""

from ..source_contract import source_pbc_package_contract
from .runtime import RETURNS_REVERSE_LOGISTICS_ALLOWED_DATABASE_BACKENDS
from .runtime import RETURNS_REVERSE_LOGISTICS_OWNED_TABLES
from .runtime import RETURNS_REVERSE_LOGISTICS_RUNTIME_CAPABILITY_KEYS
from .runtime import RETURNS_REVERSE_LOGISTICS_STANDARD_FEATURE_KEYS
from .runtime import returns_reverse_logistics_authorize_return
from .runtime import returns_reverse_logistics_build_api_contract
from .runtime import returns_reverse_logistics_build_workbench_view
from .runtime import returns_reverse_logistics_configure_runtime
from .runtime import returns_reverse_logistics_create_return_label
from .runtime import returns_reverse_logistics_empty_state
from .runtime import returns_reverse_logistics_issue_credit_adjustment
from .runtime import returns_reverse_logistics_permissions_contract
from .runtime import returns_reverse_logistics_receive_event
from .runtime import returns_reverse_logistics_record_inspection_grade
from .runtime import returns_reverse_logistics_register_rule
from .runtime import returns_reverse_logistics_register_schema_extension
from .runtime import returns_reverse_logistics_runtime_capabilities
from .runtime import returns_reverse_logistics_runtime_smoke
from .runtime import returns_reverse_logistics_set_parameter
from .runtime import returns_reverse_logistics_verify_owned_table_boundary
from .ui import RETURNS_REVERSE_LOGISTICS_UI_FRAGMENT_KEYS
from .ui import returns_reverse_logistics_render_workbench
from .ui import returns_reverse_logistics_ui_contract

PBC_KEY = "returns_reverse_logistics"


def implementation_contract() -> dict:
    runtime = returns_reverse_logistics_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": returns_reverse_logistics_ui_contract(),
        "api_contract": returns_reverse_logistics_build_api_contract(),
        "permissions_contract": returns_reverse_logistics_permissions_contract(),
        "owned_tables": RETURNS_REVERSE_LOGISTICS_OWNED_TABLES,
        "allowed_database_backends": RETURNS_REVERSE_LOGISTICS_ALLOWED_DATABASE_BACKENDS,
        "shared_table_access": False,
    }
