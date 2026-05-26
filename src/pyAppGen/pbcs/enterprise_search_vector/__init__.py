"""Enterprise Search Vector PBC implementation package."""

from .manifest import PBC_MANIFEST

from ..source_contract import source_pbc_package_contract
from ..source_contract import source_registration_plan
from .runtime import ENTERPRISE_SEARCH_VECTOR_ALLOWED_DATABASE_BACKENDS
from .runtime import ENTERPRISE_SEARCH_VECTOR_OWNED_TABLES
from .runtime import ENTERPRISE_SEARCH_VECTOR_RUNTIME_CAPABILITY_KEYS
from .runtime import ENTERPRISE_SEARCH_VECTOR_RUNTIME_TABLES
from .runtime import ENTERPRISE_SEARCH_VECTOR_STANDARD_FEATURE_KEYS
from .runtime import enterprise_search_vector_build_api_contract
from .runtime import enterprise_search_vector_build_release_evidence
from .runtime import enterprise_search_vector_build_schema_contract
from .runtime import enterprise_search_vector_build_service_contract
from .runtime import enterprise_search_vector_build_workbench_view
from .runtime import enterprise_search_vector_configure_runtime
from .runtime import enterprise_search_vector_create_index
from .runtime import enterprise_search_vector_empty_state
from .runtime import enterprise_search_vector_ingest_document
from .runtime import enterprise_search_vector_permissions_contract
from .runtime import enterprise_search_vector_query
from .runtime import enterprise_search_vector_receive_event
from .runtime import enterprise_search_vector_refresh_index
from .runtime import enterprise_search_vector_record_feedback
from .runtime import enterprise_search_vector_register_rule
from .runtime import enterprise_search_vector_register_schema_extension
from .runtime import enterprise_search_vector_run_embedding_job
from .runtime import enterprise_search_vector_runtime_capabilities
from .runtime import enterprise_search_vector_runtime_smoke
from .runtime import enterprise_search_vector_set_parameter
from .runtime import enterprise_search_vector_verify_owned_table_boundary
from .ui import ENTERPRISE_SEARCH_VECTOR_UI_FRAGMENT_KEYS
from .ui import enterprise_search_vector_render_workbench
from .ui import enterprise_search_vector_ui_contract

PBC_KEY = "enterprise_search_vector"


def implementation_contract() -> dict:
    runtime = enterprise_search_vector_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": enterprise_search_vector_ui_contract(),
        "api_contract": enterprise_search_vector_build_api_contract(),
        "schema_contract": enterprise_search_vector_build_schema_contract(),
        "service_contract": enterprise_search_vector_build_service_contract(),
        "release_evidence": enterprise_search_vector_build_release_evidence(),
        "permissions_contract": enterprise_search_vector_permissions_contract(),
        "owned_tables": ENTERPRISE_SEARCH_VECTOR_OWNED_TABLES,
        "runtime_tables": ENTERPRISE_SEARCH_VECTOR_RUNTIME_TABLES,
        "allowed_database_backends": ENTERPRISE_SEARCH_VECTOR_ALLOWED_DATABASE_BACKENDS,
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
