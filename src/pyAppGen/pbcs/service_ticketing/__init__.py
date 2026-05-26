"""Service Ticketing PBC implementation package."""

from ..source_contract import source_pbc_package_contract
from .runtime import SERVICE_TICKETING_ALLOWED_DATABASE_BACKENDS
from .runtime import SERVICE_TICKETING_OWNED_TABLES
from .runtime import SERVICE_TICKETING_RUNTIME_CAPABILITY_KEYS
from .runtime import SERVICE_TICKETING_STANDARD_FEATURE_KEYS
from .runtime import service_ticketing_assign_ticket
from .runtime import service_ticketing_build_api_contract
from .runtime import service_ticketing_build_workbench_view
from .runtime import service_ticketing_configure_runtime
from .runtime import service_ticketing_create_sla_policy
from .runtime import service_ticketing_empty_state
from .runtime import service_ticketing_open_ticket
from .runtime import service_ticketing_permissions_contract
from .runtime import service_ticketing_receive_event
from .runtime import service_ticketing_record_escalation
from .runtime import service_ticketing_register_rule
from .runtime import service_ticketing_register_schema_extension
from .runtime import service_ticketing_resolve_ticket
from .runtime import service_ticketing_runtime_capabilities
from .runtime import service_ticketing_runtime_smoke
from .runtime import service_ticketing_set_parameter
from .runtime import service_ticketing_verify_owned_table_boundary
from .ui import SERVICE_TICKETING_UI_FRAGMENT_KEYS
from .ui import service_ticketing_render_workbench
from .ui import service_ticketing_ui_contract

PBC_KEY = "service_ticketing"


def implementation_contract() -> dict:
    runtime = service_ticketing_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": service_ticketing_ui_contract(),
        "api_contract": service_ticketing_build_api_contract(),
        "permissions_contract": service_ticketing_permissions_contract(),
        "owned_tables": SERVICE_TICKETING_OWNED_TABLES,
        "allowed_database_backends": SERVICE_TICKETING_ALLOWED_DATABASE_BACKENDS,
    }
