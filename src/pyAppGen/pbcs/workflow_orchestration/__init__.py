"""Workflow Orchestration PBC implementation package."""

from ..source_contract import source_pbc_package_contract
from .runtime import WORKFLOW_ORCHESTRATION_RUNTIME_CAPABILITY_KEYS
from .runtime import WORKFLOW_ORCHESTRATION_STANDARD_FEATURE_KEYS
from .runtime import workflow_orchestration_build_workbench_view
from .runtime import workflow_orchestration_complete_workflow
from .runtime import workflow_orchestration_configure_runtime
from .runtime import workflow_orchestration_define_workflow
from .runtime import workflow_orchestration_empty_state
from .runtime import workflow_orchestration_execute_compensation
from .runtime import workflow_orchestration_record_step_result
from .runtime import workflow_orchestration_register_rule
from .runtime import workflow_orchestration_register_schema_extension
from .runtime import workflow_orchestration_runtime_capabilities
from .runtime import workflow_orchestration_runtime_smoke
from .runtime import workflow_orchestration_schedule_timer
from .runtime import workflow_orchestration_set_parameter
from .runtime import workflow_orchestration_signal_instance
from .runtime import workflow_orchestration_start_instance
from .ui import WORKFLOW_ORCHESTRATION_UI_FRAGMENT_KEYS
from .ui import workflow_orchestration_render_workbench
from .ui import workflow_orchestration_ui_contract

PBC_KEY = "workflow_orchestration"


def implementation_contract() -> dict:
    runtime = workflow_orchestration_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": workflow_orchestration_ui_contract(),
    }
