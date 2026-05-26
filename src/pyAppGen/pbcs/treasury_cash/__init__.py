"""Treasury and Cash Management PBC implementation package."""

from ..source_contract import source_pbc_package_contract
from .runtime import TREASURY_CASH_ALLOWED_DATABASE_BACKENDS
from .runtime import TREASURY_CASH_CONSUMED_EVENT_TYPES
from .runtime import TREASURY_CASH_EMITTED_EVENT_TYPES
from .runtime import TREASURY_CASH_OWNED_TABLES
from .runtime import TREASURY_CASH_REQUIRED_EVENT_TOPIC
from .runtime import TREASURY_CASH_RUNTIME_CAPABILITY_KEYS
from .runtime import TREASURY_CASH_STANDARD_FEATURE_KEYS
from .runtime import treasury_cash_build_api_contract
from .runtime import treasury_cash_build_cash_position
from .runtime import treasury_cash_build_workbench_view
from .runtime import treasury_cash_capture_bank_balance
from .runtime import treasury_cash_configure_runtime
from .runtime import treasury_cash_empty_state
from .runtime import treasury_cash_forecast_cash
from .runtime import treasury_cash_ingest_bank_statement
from .runtime import treasury_cash_optimize_liquidity
from .runtime import treasury_cash_permissions_contract
from .runtime import treasury_cash_receive_event
from .runtime import treasury_cash_reconcile_statement
from .runtime import treasury_cash_register_bank_account
from .runtime import treasury_cash_register_rule
from .runtime import treasury_cash_register_schema_extension
from .runtime import treasury_cash_runtime_capabilities
from .runtime import treasury_cash_runtime_smoke
from .runtime import treasury_cash_set_parameter
from .runtime import treasury_cash_verify_owned_table_boundary
from .ui import TREASURY_CASH_UI_FRAGMENT_KEYS
from .ui import treasury_cash_render_workbench
from .ui import treasury_cash_ui_contract

PBC_KEY = "treasury_cash"


def implementation_contract() -> dict:
    runtime = treasury_cash_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": treasury_cash_ui_contract(),
        "api_contract": treasury_cash_build_api_contract(),
        "permissions_contract": treasury_cash_permissions_contract(),
        "owned_tables": TREASURY_CASH_OWNED_TABLES,
        "allowed_database_backends": TREASURY_CASH_ALLOWED_DATABASE_BACKENDS,
    }
