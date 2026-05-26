"""Production Control PBC implementation package."""

from ..source_contract import source_pbc_package_contract
from .runtime import PRODUCTION_CONTROL_RUNTIME_CAPABILITY_KEYS
from .runtime import PRODUCTION_CONTROL_STANDARD_FEATURE_KEYS
from .runtime import production_control_build_workbench_view
from .runtime import production_control_complete_production_order
from .runtime import production_control_configure_runtime
from .runtime import production_control_confirm_operation
from .runtime import production_control_create_production_order
from .runtime import production_control_define_routing_step
from .runtime import production_control_empty_state
from .runtime import production_control_record_downtime
from .runtime import production_control_register_rule
from .runtime import production_control_register_work_center
from .runtime import production_control_runtime_capabilities
from .runtime import production_control_runtime_smoke
from .runtime import production_control_schedule_order
from .runtime import production_control_set_parameter
from .runtime import production_control_start_operation
from .ui import PRODUCTION_CONTROL_UI_FRAGMENT_KEYS
from .ui import production_control_render_workbench
from .ui import production_control_ui_contract

PBC_KEY = "production_control"


def implementation_contract() -> dict:
    runtime = production_control_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": production_control_ui_contract(),
    }
