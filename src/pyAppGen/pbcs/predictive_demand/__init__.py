"""Predictive Demand PBC implementation package."""

from ..source_contract import source_pbc_package_contract
from .runtime import PREDICTIVE_DEMAND_ALLOWED_DATABASE_BACKENDS
from .runtime import PREDICTIVE_DEMAND_OWNED_TABLES
from .runtime import PREDICTIVE_DEMAND_RUNTIME_CAPABILITY_KEYS
from .runtime import PREDICTIVE_DEMAND_STANDARD_FEATURE_KEYS
from .runtime import predictive_demand_build_api_contract
from .runtime import predictive_demand_build_workbench_view
from .runtime import predictive_demand_configure_runtime
from .runtime import predictive_demand_create_forecast_run
from .runtime import predictive_demand_empty_state
from .runtime import predictive_demand_ingest_demand_signal
from .runtime import predictive_demand_permissions_contract
from .runtime import predictive_demand_publish_forecast_result
from .runtime import predictive_demand_receive_event
from .runtime import predictive_demand_register_forecast_model
from .runtime import predictive_demand_register_rule
from .runtime import predictive_demand_register_schema_extension
from .runtime import predictive_demand_runtime_capabilities
from .runtime import predictive_demand_runtime_smoke
from .runtime import predictive_demand_set_parameter
from .runtime import predictive_demand_verify_owned_table_boundary
from .ui import PREDICTIVE_DEMAND_UI_FRAGMENT_KEYS
from .ui import predictive_demand_render_workbench
from .ui import predictive_demand_ui_contract

PBC_KEY = "predictive_demand"


def implementation_contract() -> dict:
    runtime = predictive_demand_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": predictive_demand_ui_contract(),
        "api_contract": predictive_demand_build_api_contract(),
        "permissions_contract": predictive_demand_permissions_contract(),
        "owned_tables": PREDICTIVE_DEMAND_OWNED_TABLES,
        "allowed_database_backends": PREDICTIVE_DEMAND_ALLOWED_DATABASE_BACKENDS,
    }
