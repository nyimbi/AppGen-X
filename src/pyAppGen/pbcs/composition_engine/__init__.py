"""Composition Engine PBC implementation package."""

from ..source_contract import source_pbc_package_contract
from .runtime import COMPOSITION_ENGINE_ALLOWED_DATABASE_BACKENDS
from .runtime import COMPOSITION_ENGINE_CONSUMED_EVENT_TYPES
from .runtime import COMPOSITION_ENGINE_EMITTED_EVENT_TYPES
from .runtime import COMPOSITION_ENGINE_OWNED_TABLES
from .runtime import COMPOSITION_ENGINE_REQUIRED_EVENT_TOPIC
from .runtime import COMPOSITION_ENGINE_RUNTIME_CAPABILITY_KEYS
from .runtime import COMPOSITION_ENGINE_STANDARD_FEATURE_KEYS
from .runtime import composition_engine_build_api_contract
from .runtime import composition_engine_bind_layout
from .runtime import composition_engine_build_workbench_view
from .runtime import composition_engine_configure_runtime
from .runtime import composition_engine_create_workspace
from .runtime import composition_engine_empty_state
from .runtime import composition_engine_generate_composition_dsl
from .runtime import composition_engine_permissions_contract
from .runtime import composition_engine_plan_package_registration
from .runtime import composition_engine_publish_composition
from .runtime import composition_engine_receive_event
from .runtime import composition_engine_register_component
from .runtime import composition_engine_register_rule
from .runtime import composition_engine_register_schema_extension
from .runtime import composition_engine_register_ui_fragment
from .runtime import composition_engine_runtime_capabilities
from .runtime import composition_engine_runtime_smoke
from .runtime import composition_engine_select_pbc
from .runtime import composition_engine_set_parameter
from .runtime import composition_engine_validate_composition_plan
from .runtime import composition_engine_verify_owned_table_boundary
from .ui import COMPOSITION_ENGINE_UI_FRAGMENT_KEYS
from .ui import composition_engine_render_workbench
from .ui import composition_engine_ui_contract

PBC_KEY = "composition_engine"


def implementation_contract() -> dict:
    runtime = composition_engine_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": composition_engine_ui_contract(),
        "api_contract": composition_engine_build_api_contract(),
        "permissions_contract": composition_engine_permissions_contract(),
        "owned_tables": COMPOSITION_ENGINE_OWNED_TABLES,
        "allowed_database_backends": COMPOSITION_ENGINE_ALLOWED_DATABASE_BACKENDS,
    }
