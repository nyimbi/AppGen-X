"""Personnel Identity PBC implementation package."""

from ..source_contract import source_pbc_package_contract
from .runtime import PERSONNEL_IDENTITY_ALLOWED_DATABASE_BACKENDS
from .runtime import PERSONNEL_IDENTITY_CONSUMED_EVENT_TYPES
from .runtime import PERSONNEL_IDENTITY_EMITTED_EVENT_TYPES
from .runtime import PERSONNEL_IDENTITY_OWNED_TABLES
from .runtime import PERSONNEL_IDENTITY_REQUIRED_EVENT_TOPIC
from .runtime import PERSONNEL_IDENTITY_RUNTIME_CAPABILITY_KEYS
from .runtime import PERSONNEL_IDENTITY_STANDARD_FEATURE_KEYS
from .runtime import personnel_identity_assign_role
from .runtime import personnel_identity_build_api_contract
from .runtime import personnel_identity_build_org_chart
from .runtime import personnel_identity_build_release_evidence
from .runtime import personnel_identity_build_schema_contract
from .runtime import personnel_identity_build_service_contract
from .runtime import personnel_identity_build_workbench_view
from .runtime import personnel_identity_configure_runtime
from .runtime import personnel_identity_create_employee
from .runtime import personnel_identity_empty_state
from .runtime import personnel_identity_permissions_contract
from .runtime import personnel_identity_receive_event
from .runtime import personnel_identity_register_department
from .runtime import personnel_identity_register_rule
from .runtime import personnel_identity_register_schema_extension
from .runtime import personnel_identity_runtime_capabilities
from .runtime import personnel_identity_runtime_smoke
from .runtime import personnel_identity_set_parameter
from .runtime import personnel_identity_transition_employee_status
from .runtime import personnel_identity_upsert_identity_attribute
from .runtime import personnel_identity_verify_owned_table_boundary
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
        "owned_tables": PERSONNEL_IDENTITY_OWNED_TABLES,
        "allowed_database_backends": PERSONNEL_IDENTITY_ALLOWED_DATABASE_BACKENDS,
        "api_contract": personnel_identity_build_api_contract(),
        "schema_contract": personnel_identity_build_schema_contract(),
        "service_contract": personnel_identity_build_service_contract(),
        "release_evidence_contract": personnel_identity_build_release_evidence(),
        "permissions_contract": personnel_identity_permissions_contract(),
        "required_event_topic": PERSONNEL_IDENTITY_REQUIRED_EVENT_TOPIC,
        "consumes": PERSONNEL_IDENTITY_CONSUMED_EVENT_TYPES,
        "emits": PERSONNEL_IDENTITY_EMITTED_EVENT_TYPES,
        "advanced_runtime": runtime,
        "ui_contract": personnel_identity_ui_contract(),
    }
