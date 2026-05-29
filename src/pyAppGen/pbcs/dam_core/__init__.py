"""Digital Asset Management Core PBC implementation package."""

from .manifest import PBC_MANIFEST

from ..source_contract import source_pbc_package_contract
from ..source_contract import source_package_metadata
from ..source_contract import source_registration_plan
from ..source_contract import validate_source_package_metadata
from .release_evidence import build_release_evidence as dam_core_build_release_evidence
from .release_evidence import build_release_evidence as package_build_release_evidence
from .runtime import DAM_CORE_ALLOWED_DATABASE_BACKENDS
from .runtime import DAM_CORE_OWNED_TABLES
from .runtime import DAM_CORE_RUNTIME_TABLES
from .runtime import DAM_CORE_RUNTIME_CAPABILITY_KEYS
from .runtime import DAM_CORE_STANDARD_FEATURE_KEYS
from .runtime import dam_core_add_asset_to_collection
from .runtime import dam_core_add_metadata_tag
from .runtime import dam_core_add_semantic_annotation
from .runtime import dam_core_attach_rights_policy
from .runtime import dam_core_build_api_contract
from .runtime import dam_core_build_schema_contract
from .runtime import dam_core_build_service_contract
from .runtime import dam_core_build_workbench_view
from .runtime import dam_core_complete_rendition
from .runtime import dam_core_complete_asset_review_task
from .runtime import dam_core_configure_runtime
from .runtime import dam_core_create_asset_collection
from .runtime import dam_core_detect_asset_duplicate_candidate
from .runtime import dam_core_enrich_metadata
from .runtime import dam_core_empty_state
from .runtime import dam_core_enforce_rights
from .runtime import dam_core_grant_usage_entitlement
from .runtime import dam_core_open_asset_exception
from .runtime import dam_core_permissions_contract
from .runtime import dam_core_receive_event
from .runtime import dam_core_record_asset_lineage
from .runtime import dam_core_record_asset_usage_snapshot
from .runtime import dam_core_register_asset
from .runtime import dam_core_register_license_agreement
from .runtime import dam_core_register_metadata_taxonomy
from .runtime import dam_core_register_rule
from .runtime import dam_core_register_schema_extension
from .runtime import dam_core_resolve_asset_exception_case
from .runtime import dam_core_request_rendition
from .runtime import dam_core_runtime_capabilities
from .runtime import dam_core_runtime_smoke
from .runtime import dam_core_set_parameter
from .runtime import dam_core_start_asset_workflow
from .runtime import dam_core_verify_owned_table_boundary
from .ui import DAM_CORE_UI_FRAGMENT_KEYS
from .ui import dam_core_render_workbench
from .ui import dam_core_render_standalone_app
from .ui import dam_core_standalone_app_contract
from .ui import dam_core_ui_contract
from .standalone import DamCoreStandaloneApp
from .standalone import standalone_app_manifest

PBC_KEY = "dam_core"


def implementation_contract() -> dict:
    runtime = dam_core_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": dam_core_ui_contract(),
        "api_contract": dam_core_build_api_contract(),
        "schema_contract": dam_core_build_schema_contract(),
        "service_contract": dam_core_build_service_contract(),
        "release_evidence_contract": package_build_release_evidence(),
        "permissions_contract": dam_core_permissions_contract(),
        "owned_tables": DAM_CORE_OWNED_TABLES,
        "runtime_tables": DAM_CORE_RUNTIME_TABLES,
        "allowed_database_backends": DAM_CORE_ALLOWED_DATABASE_BACKENDS,
        "standalone_app_contract": dam_core_standalone_app_contract(),
        "standalone_app_manifest": standalone_app_manifest(),
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
