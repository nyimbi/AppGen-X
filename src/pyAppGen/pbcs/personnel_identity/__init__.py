"""Personnel Identity PBC implementation package."""

from ..source_contract import source_pbc_package_contract
from .runtime import PERSONNEL_IDENTITY_RUNTIME_CAPABILITY_KEYS
from .runtime import PERSONNEL_IDENTITY_STANDARD_FEATURE_KEYS
from .runtime import personnel_identity_assign_role
from .runtime import personnel_identity_build_org_chart
from .runtime import personnel_identity_build_workbench_view
from .runtime import personnel_identity_configure_runtime
from .runtime import personnel_identity_create_employee
from .runtime import personnel_identity_empty_state
from .runtime import personnel_identity_register_department
from .runtime import personnel_identity_register_rule
from .runtime import personnel_identity_runtime_capabilities
from .runtime import personnel_identity_runtime_smoke
from .runtime import personnel_identity_set_parameter
from .runtime import personnel_identity_transition_employee_status
from .runtime import personnel_identity_upsert_identity_attribute
from .ui import PERSONNEL_IDENTITY_UI_FRAGMENT_KEYS
from .ui import personnel_identity_render_workbench
from .ui import personnel_identity_ui_contract

PBC_KEY = "personnel_identity"


def implementation_contract() -> dict:
    runtime = personnel_identity_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": personnel_identity_ui_contract(),
    }
