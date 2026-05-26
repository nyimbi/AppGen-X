"""Time and Labor PBC implementation package."""

from ..source_contract import source_pbc_package_contract
from .runtime import TIME_LABOR_ALLOWED_DATABASE_BACKENDS
from .runtime import TIME_LABOR_CONSUMED_EVENT_TYPES
from .runtime import TIME_LABOR_EMITTED_EVENT_TYPES
from .runtime import TIME_LABOR_OWNED_TABLES
from .runtime import TIME_LABOR_REQUIRED_EVENT_TOPIC
from .runtime import TIME_LABOR_RUNTIME_CAPABILITY_KEYS
from .runtime import TIME_LABOR_STANDARD_FEATURE_KEYS
from .runtime import time_labor_approve_labor_summary
from .runtime import time_labor_build_api_contract
from .runtime import time_labor_build_workbench_view
from .runtime import time_labor_calculate_time_entry
from .runtime import time_labor_configure_runtime
from .runtime import time_labor_create_shift
from .runtime import time_labor_empty_state
from .runtime import time_labor_permissions_contract
from .runtime import time_labor_record_absence
from .runtime import time_labor_record_clock_event
from .runtime import time_labor_receive_event
from .runtime import time_labor_register_rule
from .runtime import time_labor_register_schema_extension
from .runtime import time_labor_runtime_capabilities
from .runtime import time_labor_runtime_smoke
from .runtime import time_labor_set_parameter
from .runtime import time_labor_upsert_employee_projection
from .runtime import time_labor_verify_owned_table_boundary
from .ui import TIME_LABOR_UI_FRAGMENT_KEYS
from .ui import time_labor_render_workbench
from .ui import time_labor_ui_contract

PBC_KEY = "time_labor"


def implementation_contract() -> dict:
    runtime = time_labor_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": time_labor_ui_contract(),
        "api_contract": time_labor_build_api_contract(),
        "permissions_contract": time_labor_permissions_contract(),
        "owned_tables": TIME_LABOR_OWNED_TABLES,
        "allowed_database_backends": TIME_LABOR_ALLOWED_DATABASE_BACKENDS,
    }
