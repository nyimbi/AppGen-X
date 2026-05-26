"""Cross Border Trade PBC implementation package."""

from ..source_contract import source_pbc_package_contract
from .runtime import CROSS_BORDER_TRADE_ALLOWED_DATABASE_BACKENDS
from .runtime import CROSS_BORDER_TRADE_OWNED_TABLES
from .runtime import CROSS_BORDER_TRADE_RUNTIME_CAPABILITY_KEYS
from .runtime import CROSS_BORDER_TRADE_STANDARD_FEATURE_KEYS
from .runtime import cross_border_trade_build_api_contract
from .runtime import cross_border_trade_build_workbench_view
from .runtime import cross_border_trade_classify_product
from .runtime import cross_border_trade_configure_runtime
from .runtime import cross_border_trade_empty_state
from .runtime import cross_border_trade_file_customs_declaration
from .runtime import cross_border_trade_permissions_contract
from .runtime import cross_border_trade_quote_landed_cost
from .runtime import cross_border_trade_receive_event
from .runtime import cross_border_trade_register_rule
from .runtime import cross_border_trade_register_schema_extension
from .runtime import cross_border_trade_runtime_capabilities
from .runtime import cross_border_trade_runtime_smoke
from .runtime import cross_border_trade_screen_export_control
from .runtime import cross_border_trade_set_parameter
from .runtime import cross_border_trade_verify_owned_table_boundary
from .ui import CROSS_BORDER_TRADE_UI_FRAGMENT_KEYS
from .ui import cross_border_trade_render_workbench
from .ui import cross_border_trade_ui_contract

PBC_KEY = "cross_border_trade"


def implementation_contract() -> dict:
    runtime = cross_border_trade_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "ok": True,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": cross_border_trade_ui_contract(),
        "api_contract": cross_border_trade_build_api_contract(),
        "permissions_contract": cross_border_trade_permissions_contract(),
        "owned_tables": CROSS_BORDER_TRADE_OWNED_TABLES,
        "allowed_database_backends": CROSS_BORDER_TRADE_ALLOWED_DATABASE_BACKENDS,
    }
