"""CDP Segmentation PBC implementation package."""

from .manifest import PBC_MANIFEST

from ..source_contract import source_pbc_package_contract
from ..source_contract import source_package_metadata
from ..source_contract import validate_source_package_metadata
from ..source_contract import source_registration_plan
from .release_evidence import build_release_evidence as package_build_release_evidence
from .runtime import CDP_SEGMENTATION_ALLOWED_DATABASE_BACKENDS
from .runtime import CDP_SEGMENTATION_OWNED_TABLES
from .runtime import CDP_SEGMENTATION_RUNTIME_TABLES
from .runtime import CDP_SEGMENTATION_RUNTIME_CAPABILITY_KEYS
from .runtime import CDP_SEGMENTATION_STANDARD_FEATURE_KEYS
from .runtime import cdp_segmentation_activate_segment
from .runtime import cdp_segmentation_allocate_activation
from .runtime import cdp_segmentation_detect_profile_anomaly
from .runtime import cdp_segmentation_federate_customer_view
from .runtime import cdp_segmentation_forecast_audience
from .runtime import cdp_segmentation_build_api_contract
from .runtime import cdp_segmentation_build_release_evidence
from .runtime import cdp_segmentation_build_schema_contract
from .runtime import cdp_segmentation_build_service_contract
from .runtime import cdp_segmentation_build_workbench_view
from .runtime import cdp_segmentation_configure_runtime
from .runtime import cdp_segmentation_define_segment
from .runtime import cdp_segmentation_empty_state
from .runtime import cdp_segmentation_evaluate_segments
from .runtime import cdp_segmentation_generate_profile_proof
from .runtime import cdp_segmentation_heal_profile_merge
from .runtime import cdp_segmentation_ingest_customer_event
from .runtime import cdp_segmentation_parse_segment_rule
from .runtime import cdp_segmentation_permissions_contract
from .runtime import cdp_segmentation_receive_event
from .runtime import cdp_segmentation_register_rule
from .runtime import cdp_segmentation_register_schema_extension
from .runtime import cdp_segmentation_register_governed_model
from .runtime import cdp_segmentation_resolve_audience_exception
from .runtime import cdp_segmentation_runtime_capabilities
from .runtime import cdp_segmentation_runtime_smoke
from .runtime import cdp_segmentation_run_data_quality_controls
from .runtime import cdp_segmentation_score_lifecycle_risk
from .runtime import cdp_segmentation_screen_consent_policy
from .runtime import cdp_segmentation_set_parameter
from .runtime import cdp_segmentation_simulate_segment_membership
from .runtime import cdp_segmentation_upsert_profile_property
from .runtime import cdp_segmentation_verify_owned_table_boundary
from .ui import CDP_SEGMENTATION_UI_FRAGMENT_KEYS
from .ui import cdp_segmentation_render_standalone_app
from .ui import cdp_segmentation_render_workbench
from .ui import cdp_segmentation_standalone_app_contract
from .ui import cdp_segmentation_ui_contract
from .standalone import CdpSegmentationStandaloneApp
from .standalone import standalone_app_manifest
from .standalone import standalone_route_contracts

PBC_KEY = 'cdp_segmentation'


def implementation_contract() -> dict:
    runtime = cdp_segmentation_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime['capabilities']))
    return {
        **contract,
        'standard_features': runtime['standard_features'],
        'advanced_runtime': runtime,
        'ui_contract': cdp_segmentation_ui_contract(),
        'api_contract': cdp_segmentation_build_api_contract(),
        'schema_contract': cdp_segmentation_build_schema_contract(),
        'service_contract': cdp_segmentation_build_service_contract(),
        'release_evidence_contract': package_build_release_evidence(),
        'permissions_contract': cdp_segmentation_permissions_contract(),
        'owned_tables': CDP_SEGMENTATION_OWNED_TABLES,
        'runtime_tables': CDP_SEGMENTATION_RUNTIME_TABLES,
        'allowed_database_backends': CDP_SEGMENTATION_ALLOWED_DATABASE_BACKENDS,
        'standalone_app_contract': cdp_segmentation_standalone_app_contract(),
        'standalone_app_manifest': standalone_app_manifest(),
        'standalone_routes': standalone_route_contracts(),
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
        'format': 'appgen.pbc-source-package-discovery-plan.v1',
        'ok': metadata_validation['ok'] and registration['ok'],
        'pbc': PBC_KEY,
        'metadata_validation': metadata_validation,
        'registration': registration,
        'side_effects': (),
    }


def smoke_test() -> dict:
    """Exercise package metadata validation and discovery planning."""
    discovery = package_discovery_plan()
    return {
        'ok': discovery['ok'],
        'discovery': discovery,
        'side_effects': (),
    }
