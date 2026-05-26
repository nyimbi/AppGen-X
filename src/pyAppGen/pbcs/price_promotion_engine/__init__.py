"""Price Promotion Engine PBC implementation package."""

from ..source_contract import source_pbc_package_contract
from .runtime import PRICE_PROMOTION_ENGINE_ALLOWED_DATABASE_BACKENDS
from .runtime import PRICE_PROMOTION_ENGINE_OWNED_TABLES
from .runtime import PRICE_PROMOTION_ENGINE_RUNTIME_CAPABILITY_KEYS
from .runtime import PRICE_PROMOTION_ENGINE_STANDARD_FEATURE_KEYS
from .runtime import price_promotion_engine_apply_promotion
from .runtime import price_promotion_engine_build_api_contract
from .runtime import price_promotion_engine_build_workbench_view
from .runtime import price_promotion_engine_configure_runtime
from .runtime import price_promotion_engine_empty_state
from .runtime import price_promotion_engine_permissions_contract
from .runtime import price_promotion_engine_quote_price
from .runtime import price_promotion_engine_receive_event
from .runtime import price_promotion_engine_register_loyalty_tier
from .runtime import price_promotion_engine_register_price_rule
from .runtime import price_promotion_engine_register_promotion
from .runtime import price_promotion_engine_register_rule
from .runtime import price_promotion_engine_register_schema_extension
from .runtime import price_promotion_engine_runtime_capabilities
from .runtime import price_promotion_engine_runtime_smoke
from .runtime import price_promotion_engine_set_parameter
from .runtime import price_promotion_engine_verify_owned_table_boundary
from .ui import PRICE_PROMOTION_ENGINE_UI_FRAGMENT_KEYS
from .ui import price_promotion_engine_render_workbench
from .ui import price_promotion_engine_ui_contract

PBC_KEY = "price_promotion_engine"


def implementation_contract() -> dict:
    runtime = price_promotion_engine_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": price_promotion_engine_ui_contract(),
        "api_contract": price_promotion_engine_build_api_contract(),
        "permissions_contract": price_promotion_engine_permissions_contract(),
        "owned_tables": PRICE_PROMOTION_ENGINE_OWNED_TABLES,
        "allowed_database_backends": PRICE_PROMOTION_ENGINE_ALLOWED_DATABASE_BACKENDS,
    }
