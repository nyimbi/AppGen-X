"""Enterprise Asset Management PBC implementation package."""

from ..source_contract import source_pbc_package_contract
from .runtime import EAM_RUNTIME_CAPABILITY_KEYS
from .runtime import EAM_STANDARD_FEATURE_KEYS
from .runtime import eam_build_workbench_view
from .runtime import eam_complete_work_order
from .runtime import eam_configure_runtime
from .runtime import eam_create_maintenance_plan
from .runtime import eam_create_safety_permit
from .runtime import eam_create_work_order
from .runtime import eam_empty_state
from .runtime import eam_issue_spare_part
from .runtime import eam_record_condition_reading
from .runtime import eam_record_meter_reading
from .runtime import eam_register_equipment
from .runtime import eam_register_rule
from .runtime import eam_runtime_capabilities
from .runtime import eam_runtime_smoke
from .runtime import eam_schedule_work_order
from .runtime import eam_set_parameter
from .ui import EAM_UI_FRAGMENT_KEYS
from .ui import eam_render_workbench
from .ui import eam_ui_contract

PBC_KEY = "eam"


def implementation_contract() -> dict:
    runtime = eam_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": eam_ui_contract(),
    }
