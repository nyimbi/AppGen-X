"""Inventory Positioning PBC implementation package."""

from ..source_contract import source_pbc_package_contract
from .runtime import INVENTORY_POSITIONING_RUNTIME_CAPABILITY_KEYS
from .runtime import INVENTORY_POSITIONING_STANDARD_FEATURE_KEYS
from .runtime import inventory_positioning_allocate_inventory
from .runtime import inventory_positioning_build_workbench_view
from .runtime import inventory_positioning_calculate_availability
from .runtime import inventory_positioning_configure_runtime
from .runtime import inventory_positioning_empty_state
from .runtime import inventory_positioning_post_goods_receipt
from .runtime import inventory_positioning_release_allocation
from .runtime import inventory_positioning_register_item
from .runtime import inventory_positioning_register_node
from .runtime import inventory_positioning_register_rule
from .runtime import inventory_positioning_runtime_capabilities
from .runtime import inventory_positioning_runtime_smoke
from .runtime import inventory_positioning_set_parameter
from .ui import INVENTORY_POSITIONING_UI_FRAGMENT_KEYS
from .ui import inventory_positioning_render_workbench
from .ui import inventory_positioning_ui_contract

PBC_KEY = "inventory_positioning"


def implementation_contract() -> dict:
    runtime = inventory_positioning_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": inventory_positioning_ui_contract(),
    }
