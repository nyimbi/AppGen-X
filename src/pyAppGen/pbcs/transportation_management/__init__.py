"""Transportation Management PBC implementation package."""

from ..source_contract import source_pbc_package_contract
from .runtime import TRANSPORTATION_MANAGEMENT_RUNTIME_CAPABILITY_KEYS
from .runtime import TRANSPORTATION_MANAGEMENT_STANDARD_FEATURE_KEYS
from .runtime import transportation_management_build_workbench_view
from .runtime import transportation_management_calculate_eta
from .runtime import transportation_management_configure_runtime
from .runtime import transportation_management_confirm_delivery
from .runtime import transportation_management_create_shipment
from .runtime import transportation_management_dispatch_shipment
from .runtime import transportation_management_empty_state
from .runtime import transportation_management_plan_route
from .runtime import transportation_management_record_tracking_event
from .runtime import transportation_management_register_carrier
from .runtime import transportation_management_register_rule
from .runtime import transportation_management_runtime_capabilities
from .runtime import transportation_management_runtime_smoke
from .runtime import transportation_management_select_carrier
from .runtime import transportation_management_set_parameter
from .ui import TRANSPORTATION_MANAGEMENT_UI_FRAGMENT_KEYS
from .ui import transportation_management_render_workbench
from .ui import transportation_management_ui_contract

PBC_KEY = "transportation_management"


def implementation_contract() -> dict:
    runtime = transportation_management_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": transportation_management_ui_contract(),
    }
