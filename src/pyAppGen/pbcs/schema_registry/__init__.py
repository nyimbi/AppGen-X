"""Schema Registry PBC implementation package."""

from ..source_contract import source_pbc_package_contract
from .runtime import SCHEMA_REGISTRY_RUNTIME_CAPABILITY_KEYS
from .runtime import SCHEMA_REGISTRY_STANDARD_FEATURE_KEYS
from .runtime import schema_registry_build_workbench_view
from .runtime import schema_registry_configure_runtime
from .runtime import schema_registry_define_compatibility_rule
from .runtime import schema_registry_empty_state
from .runtime import schema_registry_publish_contract_projection
from .runtime import schema_registry_record_contract_violation
from .runtime import schema_registry_register_consumer_binding
from .runtime import schema_registry_register_rule
from .runtime import schema_registry_register_subject
from .runtime import schema_registry_run_compatibility_check
from .runtime import schema_registry_runtime_capabilities
from .runtime import schema_registry_runtime_smoke
from .runtime import schema_registry_set_parameter
from .runtime import schema_registry_submit_schema_version
from .runtime import schema_registry_validate_payload
from .ui import SCHEMA_REGISTRY_UI_FRAGMENT_KEYS
from .ui import schema_registry_render_workbench
from .ui import schema_registry_ui_contract

PBC_KEY = "schema_registry"


def implementation_contract() -> dict:
    runtime = schema_registry_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": schema_registry_ui_contract(),
    }
