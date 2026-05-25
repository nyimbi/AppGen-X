"""Talent Onboarding PBC implementation package."""

from ..source_contract import source_pbc_package_contract
from .runtime import TALENT_ONBOARDING_RUNTIME_CAPABILITY_KEYS
from .runtime import TALENT_ONBOARDING_STANDARD_FEATURE_KEYS
from .runtime import talent_onboarding_accept_offer
from .runtime import talent_onboarding_advance_candidate_stage
from .runtime import talent_onboarding_build_workbench_view
from .runtime import talent_onboarding_complete_onboarding_task
from .runtime import talent_onboarding_configure_runtime
from .runtime import talent_onboarding_create_candidate
from .runtime import talent_onboarding_create_job_requisition
from .runtime import talent_onboarding_create_onboarding_task
from .runtime import talent_onboarding_empty_state
from .runtime import talent_onboarding_extend_offer
from .runtime import talent_onboarding_provision_employee
from .runtime import talent_onboarding_record_background_check
from .runtime import talent_onboarding_register_rule
from .runtime import talent_onboarding_runtime_capabilities
from .runtime import talent_onboarding_runtime_smoke
from .runtime import talent_onboarding_set_parameter
from .ui import TALENT_ONBOARDING_UI_FRAGMENT_KEYS
from .ui import talent_onboarding_render_workbench
from .ui import talent_onboarding_ui_contract

PBC_KEY = "talent_onboarding"


def implementation_contract() -> dict:
    runtime = talent_onboarding_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": talent_onboarding_ui_contract(),
    }
