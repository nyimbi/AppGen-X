"""Composition Engine PBC implementation package."""

from .manifest import PBC_MANIFEST

from ..source_contract import source_pbc_package_contract
from ..source_contract import source_package_metadata
from ..source_contract import validate_source_package_metadata
from ..source_contract import source_registration_plan
from .runtime import COMPOSITION_ENGINE_ALLOWED_DATABASE_BACKENDS
from .runtime import COMPOSITION_ENGINE_CONSUMED_EVENT_TYPES
from .runtime import COMPOSITION_ENGINE_EMITTED_EVENT_TYPES
from .runtime import COMPOSITION_ENGINE_OWNED_TABLES
from .runtime import COMPOSITION_ENGINE_REQUIRED_EVENT_TOPIC
from .runtime import COMPOSITION_ENGINE_RUNTIME_TABLES
from .runtime import COMPOSITION_ENGINE_RUNTIME_CAPABILITY_KEYS
from .runtime import COMPOSITION_ENGINE_STANDARD_FEATURE_KEYS
from .runtime import composition_engine_build_api_contract
from .runtime import composition_engine_build_artifact_lineage
from .runtime import composition_engine_build_control_center
from .runtime import composition_engine_build_documentation_matrix
from .runtime import composition_engine_build_release_evidence
from .runtime import composition_engine_build_release_notes
from .runtime import composition_engine_build_schema_contract
from .runtime import composition_engine_build_security_review
from .runtime import composition_engine_build_service_contract
from .runtime import composition_engine_build_smoke_plan
from .runtime import composition_engine_bind_layout
from .runtime import composition_engine_build_workbench_view
from .runtime import composition_engine_configure_runtime
from .runtime import composition_engine_create_workspace
from .runtime import composition_engine_empty_state
from .runtime import composition_engine_agent_competency_catalog
from .runtime import composition_engine_assistant_document_preview
from .runtime import composition_engine_generate_composition_dsl
from .runtime import composition_engine_permissions_contract
from .runtime import composition_engine_plan_package_registration
from .runtime import composition_engine_plan_crud_action
from .runtime import composition_engine_publish_composition
from .runtime import composition_engine_receive_event
from .runtime import composition_engine_register_component
from .runtime import composition_engine_register_rule
from .runtime import composition_engine_register_schema_extension
from .runtime import composition_engine_register_ui_fragment
from .runtime import composition_engine_release_rehearsal
from .runtime import composition_engine_route_agent_intent
from .runtime import composition_engine_runtime_capabilities
from .runtime import composition_engine_runtime_smoke
from .runtime import composition_engine_preview_selection_impact
from .runtime import composition_engine_select_pbc
from .runtime import composition_engine_set_parameter
from .runtime import composition_engine_validate_composition_plan
from .runtime import composition_engine_verify_owned_table_boundary
from .forms import composition_engine_form_catalog
from .forms import composition_engine_get_form
from .forms import composition_engine_validate_form_payload
from .wizards import composition_engine_wizard_catalog
from .wizards import composition_engine_plan_wizard
from .controls import composition_engine_control_catalog
from .controls import composition_engine_control_center
from .controls import composition_engine_mutation_preview
from .ui import COMPOSITION_ENGINE_UI_FRAGMENT_KEYS
from .ui import composition_engine_render_workbench
from .ui import composition_engine_ui_contract
from .agent import agent_skill_manifest
from .agent import chatbot_interface_contract

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
        "schema_contract": composition_engine_build_schema_contract(),
        "service_contract": composition_engine_build_service_contract(),
        "release_evidence_contract": composition_engine_build_release_evidence(),
        "permissions_contract": composition_engine_permissions_contract(),
        "agent_contract": agent_skill_manifest(),
        "chatbot_contract": chatbot_interface_contract(),
        "forms": composition_engine_form_catalog(),
        "wizards": composition_engine_wizard_catalog(),
        "controls": composition_engine_control_catalog(),
        "owned_tables": COMPOSITION_ENGINE_OWNED_TABLES,
        "runtime_tables": COMPOSITION_ENGINE_RUNTIME_TABLES,
        "allowed_database_backends": COMPOSITION_ENGINE_ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": COMPOSITION_ENGINE_REQUIRED_EVENT_TOPIC,
        "consumes": COMPOSITION_ENGINE_CONSUMED_EVENT_TYPES,
        "emits": COMPOSITION_ENGINE_EMITTED_EVENT_TYPES,
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
