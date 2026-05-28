"""API Gateway Mesh PBC implementation package."""

from .manifest import PBC_MANIFEST

from ..source_contract import source_pbc_package_contract
from ..source_contract import source_package_metadata
from ..source_contract import validate_source_package_metadata
from ..source_contract import source_registration_plan
from .runtime import API_GATEWAY_MESH_ALLOWED_DATABASE_BACKENDS
from .runtime import API_GATEWAY_MESH_CONSUMED_EVENT_TYPES
from .runtime import API_GATEWAY_MESH_EMITTED_EVENT_TYPES
from .runtime import API_GATEWAY_MESH_OWNED_TABLES
from .runtime import API_GATEWAY_MESH_REQUIRED_EVENT_TOPIC
from .runtime import API_GATEWAY_MESH_RUNTIME_CAPABILITY_KEYS
from .runtime import API_GATEWAY_MESH_STANDARD_FEATURE_KEYS
from .runtime import api_gateway_mesh_apply_rate_limit
from .runtime import api_gateway_mesh_build_api_contract
from .runtime import api_gateway_mesh_build_route_publication_safety_case
from .runtime import api_gateway_mesh_build_release_evidence
from .runtime import api_gateway_mesh_build_schema_contract
from .runtime import api_gateway_mesh_build_service_map
from .runtime import api_gateway_mesh_build_service_contract
from .runtime import api_gateway_mesh_build_workbench_view
from .runtime import api_gateway_mesh_analyze_route_collisions
from .runtime import api_gateway_mesh_configure_runtime
from .runtime import api_gateway_mesh_empty_state
from .runtime import api_gateway_mesh_permissions_contract
from .runtime import api_gateway_mesh_publish_route
from .runtime import api_gateway_mesh_receive_event
from .runtime import api_gateway_mesh_record_health
from .runtime import api_gateway_mesh_record_traffic_sample
from .runtime import api_gateway_mesh_register_mtls_identity
from .runtime import api_gateway_mesh_register_rule
from .runtime import api_gateway_mesh_register_schema_extension
from .runtime import api_gateway_mesh_register_service
from .runtime import api_gateway_mesh_runtime_capabilities
from .runtime import api_gateway_mesh_runtime_smoke
from .runtime import api_gateway_mesh_set_parameter
from .runtime import api_gateway_mesh_verify_owned_table_boundary
from .ui import API_GATEWAY_MESH_UI_FRAGMENT_KEYS
from .ui import api_gateway_mesh_render_workbench
from .ui import api_gateway_mesh_ui_contract
from .agent import incident_triage_preview
from .agent import route_publication_readiness_preview

PBC_KEY = "api_gateway_mesh"


def implementation_contract() -> dict:
    runtime = api_gateway_mesh_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": api_gateway_mesh_ui_contract(),
        "api_contract": api_gateway_mesh_build_api_contract(),
        "schema_contract": api_gateway_mesh_build_schema_contract(),
        "service_contract": api_gateway_mesh_build_service_contract(),
        "release_evidence_contract": api_gateway_mesh_build_release_evidence(),
        "permissions_contract": api_gateway_mesh_permissions_contract(),
        "owned_tables": API_GATEWAY_MESH_OWNED_TABLES,
        "allowed_database_backends": API_GATEWAY_MESH_ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": API_GATEWAY_MESH_REQUIRED_EVENT_TOPIC,
        "consumes": API_GATEWAY_MESH_CONSUMED_EVENT_TYPES,
        "emits": API_GATEWAY_MESH_EMITTED_EVENT_TYPES,
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
