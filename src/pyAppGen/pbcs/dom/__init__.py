"""Distributed Order Management PBC implementation package."""

from ..source_contract import source_pbc_package_contract
from .runtime import DOM_RUNTIME_CAPABILITY_KEYS
from .runtime import DOM_STANDARD_FEATURE_KEYS
from .runtime import dom_apply_inventory_allocation
from .runtime import dom_apply_tax_projection
from .runtime import dom_build_workbench_view
from .runtime import dom_capture_order
from .runtime import dom_configure_runtime
from .runtime import dom_confirm_order_shipped
from .runtime import dom_create_fulfillment_plan
from .runtime import dom_empty_state
from .runtime import dom_price_order
from .runtime import dom_register_rule
from .runtime import dom_runtime_capabilities
from .runtime import dom_runtime_smoke
from .runtime import dom_screen_fraud
from .runtime import dom_set_parameter
from .runtime import dom_upsert_customer_projection
from .runtime import dom_verify_order
from .ui import DOM_UI_FRAGMENT_KEYS
from .ui import dom_render_workbench
from .ui import dom_ui_contract

PBC_KEY = "dom"


def implementation_contract() -> dict:
    runtime = dom_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": dom_ui_contract(),
    }
