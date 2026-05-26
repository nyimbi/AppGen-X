"""Lead Opportunity PBC implementation package."""

from ..source_contract import source_pbc_package_contract
from .runtime import LEAD_OPPORTUNITY_ALLOWED_DATABASE_BACKENDS
from .runtime import LEAD_OPPORTUNITY_OWNED_TABLES
from .runtime import LEAD_OPPORTUNITY_RUNTIME_CAPABILITY_KEYS
from .runtime import LEAD_OPPORTUNITY_STANDARD_FEATURE_KEYS
from .runtime import lead_opportunity_advance_opportunity
from .runtime import lead_opportunity_build_api_contract
from .runtime import lead_opportunity_build_workbench_view
from .runtime import lead_opportunity_configure_runtime
from .runtime import lead_opportunity_create_account_hierarchy
from .runtime import lead_opportunity_create_lead
from .runtime import lead_opportunity_create_opportunity
from .runtime import lead_opportunity_empty_state
from .runtime import lead_opportunity_permissions_contract
from .runtime import lead_opportunity_qualify_lead
from .runtime import lead_opportunity_receive_event
from .runtime import lead_opportunity_record_sales_activity
from .runtime import lead_opportunity_register_rule
from .runtime import lead_opportunity_register_schema_extension
from .runtime import lead_opportunity_runtime_capabilities
from .runtime import lead_opportunity_runtime_smoke
from .runtime import lead_opportunity_set_parameter
from .runtime import lead_opportunity_verify_owned_table_boundary
from .runtime import lead_opportunity_win_opportunity
from .ui import LEAD_OPPORTUNITY_UI_FRAGMENT_KEYS
from .ui import lead_opportunity_render_workbench
from .ui import lead_opportunity_ui_contract

PBC_KEY = "lead_opportunity"


def implementation_contract() -> dict:
    runtime = lead_opportunity_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": lead_opportunity_ui_contract(),
        "api_contract": lead_opportunity_build_api_contract(),
        "permissions_contract": lead_opportunity_permissions_contract(),
        "owned_tables": LEAD_OPPORTUNITY_OWNED_TABLES,
        "allowed_database_backends": LEAD_OPPORTUNITY_ALLOWED_DATABASE_BACKENDS,
    }
