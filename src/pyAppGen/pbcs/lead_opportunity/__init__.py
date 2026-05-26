"""Lead Opportunity PBC implementation package."""

from .manifest import PBC_MANIFEST

from ..source_contract import source_pbc_package_contract
from ..source_contract import source_package_metadata
from ..source_contract import validate_source_package_metadata
from ..source_contract import source_registration_plan
from .runtime import LEAD_OPPORTUNITY_ALLOWED_DATABASE_BACKENDS
from .runtime import LEAD_OPPORTUNITY_CONSUMED_EVENT_TYPES
from .runtime import LEAD_OPPORTUNITY_EMITTED_EVENT_TYPES
from .runtime import LEAD_OPPORTUNITY_OWNED_TABLES
from .runtime import LEAD_OPPORTUNITY_REQUIRED_EVENT_TOPIC
from .runtime import LEAD_OPPORTUNITY_RUNTIME_TABLES
from .runtime import LEAD_OPPORTUNITY_RUNTIME_CAPABILITY_KEYS
from .runtime import LEAD_OPPORTUNITY_STANDARD_FEATURE_KEYS
from .runtime import lead_opportunity_advance_opportunity
from .runtime import lead_opportunity_build_api_contract
from .runtime import lead_opportunity_build_release_evidence
from .runtime import lead_opportunity_build_schema_contract
from .runtime import lead_opportunity_build_service_contract
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
        "schema_contract": lead_opportunity_build_schema_contract(),
        "service_contract": lead_opportunity_build_service_contract(),
        "release_evidence_contract": lead_opportunity_build_release_evidence(),
        "permissions_contract": lead_opportunity_permissions_contract(),
        "owned_tables": LEAD_OPPORTUNITY_OWNED_TABLES,
        "runtime_tables": LEAD_OPPORTUNITY_RUNTIME_TABLES,
        "allowed_database_backends": LEAD_OPPORTUNITY_ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": LEAD_OPPORTUNITY_REQUIRED_EVENT_TOPIC,
        "consumes": LEAD_OPPORTUNITY_CONSUMED_EVENT_TYPES,
        "emits": LEAD_OPPORTUNITY_EMITTED_EVENT_TYPES,
        "boundary_contract": lead_opportunity_verify_owned_table_boundary(LEAD_OPPORTUNITY_OWNED_TABLES),
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


def package_metadata_manifest() -> dict:
    """Return package identity, artifacts, and discovery metadata."""
    return source_package_metadata(PBC_KEY, register_pbc(), implementation_contract())


def validate_package_metadata() -> dict:
    """Validate package metadata without mutating catalog state."""
    return validate_source_package_metadata(package_metadata_manifest())


def package_discovery_plan(existing_catalog: dict | None = None) -> dict:
    """Return side-effect-free package discovery and registration evidence."""
    metadata_validation = validate_package_metadata()
    registration = registration_plan(existing_catalog=existing_catalog)
    return {
        "format": "appgen.pbc-source-package-discovery-plan.v1",
        "ok": metadata_validation["ok"] and registration["ok"],
        "pbc": PBC_KEY,
        "metadata_validation": metadata_validation,
        "registration": registration,
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Exercise package metadata validation and discovery planning."""
    discovery = package_discovery_plan()
    return {
        "ok": discovery["ok"],
        "discovery": discovery,
        "side_effects": (),
    }

