"""Streaming Analytics PBC implementation package."""

from ..source_contract import source_pbc_package_contract
from .runtime import STREAMING_ANALYTICS_ALLOWED_DATABASE_BACKENDS
from .runtime import STREAMING_ANALYTICS_OWNED_TABLES
from .runtime import STREAMING_ANALYTICS_RUNTIME_CAPABILITY_KEYS
from .runtime import STREAMING_ANALYTICS_STANDARD_FEATURE_KEYS
from .runtime import streaming_analytics_build_api_contract
from .runtime import streaming_analytics_build_workbench_view
from .runtime import streaming_analytics_configure_runtime
from .runtime import streaming_analytics_create_dashboard_projection
from .runtime import streaming_analytics_define_window
from .runtime import streaming_analytics_empty_state
from .runtime import streaming_analytics_ingest_metric_event
from .runtime import streaming_analytics_permissions_contract
from .runtime import streaming_analytics_receive_event
from .runtime import streaming_analytics_register_metric_stream
from .runtime import streaming_analytics_register_rule
from .runtime import streaming_analytics_register_schema_extension
from .runtime import streaming_analytics_runtime_capabilities
from .runtime import streaming_analytics_runtime_smoke
from .runtime import streaming_analytics_set_parameter
from .runtime import streaming_analytics_verify_owned_table_boundary
from .ui import STREAMING_ANALYTICS_UI_FRAGMENT_KEYS
from .ui import streaming_analytics_render_workbench
from .ui import streaming_analytics_ui_contract

PBC_KEY = "streaming_analytics"


def implementation_contract() -> dict:
    runtime = streaming_analytics_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": streaming_analytics_ui_contract(),
        "api_contract": streaming_analytics_build_api_contract(),
        "permissions_contract": streaming_analytics_permissions_contract(),
        "owned_tables": STREAMING_ANALYTICS_OWNED_TABLES,
        "allowed_database_backends": STREAMING_ANALYTICS_ALLOWED_DATABASE_BACKENDS,
    }
