"""Warehouse Management Core PBC implementation package."""

from ..source_contract import source_pbc_package_contract
from .runtime import WMS_CORE_RUNTIME_CAPABILITY_KEYS
from .runtime import WMS_CORE_STANDARD_FEATURE_KEYS
from .runtime import wms_core_build_workbench_view
from .runtime import wms_core_configure_runtime
from .runtime import wms_core_confirm_pack
from .runtime import wms_core_confirm_putaway
from .runtime import wms_core_confirm_shipment
from .runtime import wms_core_create_pack_task
from .runtime import wms_core_create_pick_wave
from .runtime import wms_core_create_putaway_task
from .runtime import wms_core_empty_state
from .runtime import wms_core_execute_pick
from .runtime import wms_core_receive_inbound
from .runtime import wms_core_register_bin
from .runtime import wms_core_register_rule
from .runtime import wms_core_register_warehouse
from .runtime import wms_core_runtime_capabilities
from .runtime import wms_core_runtime_smoke
from .runtime import wms_core_set_parameter
from .ui import WMS_CORE_UI_FRAGMENT_KEYS
from .ui import wms_core_render_workbench
from .ui import wms_core_ui_contract

PBC_KEY = "wms_core"


def implementation_contract() -> dict:
    runtime = wms_core_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": wms_core_ui_contract(),
    }
