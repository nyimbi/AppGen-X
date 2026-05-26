"""Schema Registry PBC implementation package."""

from .manifest import PBC_MANIFEST

from ..source_contract import source_pbc_package_contract
from ..source_contract import source_registration_plan
from .runtime import SCHEMA_REGISTRY_ALLOWED_DATABASE_BACKENDS
from .runtime import SCHEMA_REGISTRY_CONSUMED_EVENT_TYPES
from .runtime import SCHEMA_REGISTRY_EMITTED_EVENT_TYPES
from .runtime import SCHEMA_REGISTRY_OWNED_TABLES
from .runtime import SCHEMA_REGISTRY_REQUIRED_EVENT_TOPIC
from .runtime import SCHEMA_REGISTRY_RUNTIME_CAPABILITY_KEYS
from .runtime import SCHEMA_REGISTRY_STANDARD_FEATURE_KEYS
from .runtime import schema_registry_build_api_contract
from .runtime import schema_registry_build_release_evidence
from .runtime import schema_registry_build_schema_contract
from .runtime import schema_registry_build_service_contract
from .runtime import schema_registry_build_workbench_view
from .runtime import schema_registry_configure_runtime
from .runtime import schema_registry_define_compatibility_rule
from .runtime import schema_registry_empty_state
from .runtime import schema_registry_permissions_contract
from .runtime import schema_registry_publish_contract_projection
from .runtime import schema_registry_receive_event
from .runtime import schema_registry_record_contract_violation
from .runtime import schema_registry_register_consumer_binding
from .runtime import schema_registry_register_rule
from .runtime import schema_registry_register_schema_extension
from .runtime import schema_registry_register_subject
from .runtime import schema_registry_run_compatibility_check
from .runtime import schema_registry_runtime_capabilities
from .runtime import schema_registry_runtime_smoke
from .runtime import schema_registry_set_parameter
from .runtime import schema_registry_submit_schema_version
from .runtime import schema_registry_validate_payload
from .runtime import schema_registry_verify_owned_table_boundary
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
        "api_contract": schema_registry_build_api_contract(),
        "schema_contract": schema_registry_build_schema_contract(),
        "service_contract": schema_registry_build_service_contract(),
        "release_evidence_contract": schema_registry_build_release_evidence(),
        "permissions_contract": schema_registry_permissions_contract(),
        "owned_tables": SCHEMA_REGISTRY_OWNED_TABLES,
        "allowed_database_backends": SCHEMA_REGISTRY_ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": SCHEMA_REGISTRY_REQUIRED_EVENT_TOPIC,
        "consumes": SCHEMA_REGISTRY_CONSUMED_EVENT_TYPES,
        "emits": SCHEMA_REGISTRY_EMITTED_EVENT_TYPES,
    }


def register_pbc() -> dict:
    """Return this PBC manifest without mutating global catalog state."""
    return dict(PBC_MANIFEST)


def registration_plan(existing_catalog: dict | None = None) -> dict:
    """Return a side-effect-free registration plan for this PBC package."""
    return source_registration_plan(
        PBC_KEY,
        register_pbc(),
        existing_catalog=existing_catalog,
    )
