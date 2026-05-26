"""Notifications PBC implementation package."""

from ..source_contract import source_pbc_package_contract
from .runtime import NOTIFICATIONS_ALLOWED_DATABASE_BACKENDS
from .runtime import NOTIFICATIONS_OWNED_TABLES
from .runtime import NOTIFICATIONS_RUNTIME_CAPABILITY_KEYS
from .runtime import NOTIFICATIONS_STANDARD_FEATURE_KEYS
from .runtime import notifications_build_api_contract
from .runtime import notifications_build_workbench_view
from .runtime import notifications_configure_runtime
from .runtime import notifications_empty_state
from .runtime import notifications_permissions_contract
from .runtime import notifications_receive_event
from .runtime import notifications_record_delivery_attempt
from .runtime import notifications_register_channel
from .runtime import notifications_register_rule
from .runtime import notifications_register_template
from .runtime import notifications_runtime_capabilities
from .runtime import notifications_runtime_smoke
from .runtime import notifications_send_message
from .runtime import notifications_set_parameter
from .runtime import notifications_verify_owned_table_boundary
from .ui import NOTIFICATIONS_UI_FRAGMENT_KEYS
from .ui import notifications_render_workbench
from .ui import notifications_ui_contract

PBC_KEY = "notifications"


def implementation_contract() -> dict:
    runtime = notifications_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": notifications_ui_contract(),
        "api_contract": notifications_build_api_contract(),
        "permissions_contract": notifications_permissions_contract(),
        "owned_tables": NOTIFICATIONS_OWNED_TABLES,
        "allowed_database_backends": NOTIFICATIONS_ALLOWED_DATABASE_BACKENDS,
    }
