"""Workflow Orchestration PBC implementation package."""

from .manifest import PBC_MANIFEST

from ..source_contract import source_pbc_package_contract
from ..source_contract import source_package_metadata
from ..source_contract import validate_source_package_metadata
from ..source_contract import source_registration_plan
from .runtime import WORKFLOW_ORCHESTRATION_ALLOWED_DATABASE_BACKENDS
from .runtime import WORKFLOW_ORCHESTRATION_CONSUMED_EVENT_TYPES
from .runtime import WORKFLOW_ORCHESTRATION_EMITTED_EVENT_TYPES
from .runtime import WORKFLOW_ORCHESTRATION_OWNED_TABLES
from .runtime import WORKFLOW_ORCHESTRATION_REQUIRED_EVENT_TOPIC
from .runtime import WORKFLOW_ORCHESTRATION_RUNTIME_CAPABILITY_KEYS
from .runtime import WORKFLOW_ORCHESTRATION_RUNTIME_TABLES
from .runtime import WORKFLOW_ORCHESTRATION_STANDARD_FEATURE_KEYS
from .runtime import workflow_orchestration_build_api_contract
from .runtime import workflow_orchestration_build_release_evidence
from .runtime import workflow_orchestration_build_schema_contract
from .runtime import workflow_orchestration_build_service_contract
from .runtime import workflow_orchestration_build_workbench_view
from .runtime import workflow_orchestration_append_audit_entry
from .runtime import workflow_orchestration_assign_human_task
from .runtime import workflow_orchestration_capture_metric_snapshot
from .runtime import workflow_orchestration_complete_workflow
from .runtime import workflow_orchestration_configure_runtime
from .runtime import workflow_orchestration_correlate_event
from .runtime import workflow_orchestration_define_workflow
from .runtime import workflow_orchestration_empty_state
from .runtime import workflow_orchestration_execute_compensation
from .runtime import workflow_orchestration_open_exception_case
from .runtime import workflow_orchestration_permissions_contract
from .runtime import workflow_orchestration_publish_workflow_version
from .runtime import workflow_orchestration_record_approval_decision
from .runtime import workflow_orchestration_record_completion_proof
from .runtime import workflow_orchestration_record_policy_screening
from .runtime import workflow_orchestration_record_simulation_run
from .runtime import workflow_orchestration_record_step_result
from .runtime import workflow_orchestration_receive_event
from .runtime import workflow_orchestration_register_escalation_rule
from .runtime import workflow_orchestration_register_governed_model_evidence
from .runtime import workflow_orchestration_register_integration_endpoint
from .runtime import workflow_orchestration_register_retry_policy
from .runtime import workflow_orchestration_register_rule
from .runtime import workflow_orchestration_register_schema_extension
from .runtime import workflow_orchestration_register_sla_policy
from .runtime import workflow_orchestration_register_transition_guard
from .runtime import workflow_orchestration_runtime_capabilities
from .runtime import workflow_orchestration_runtime_smoke
from .runtime import workflow_orchestration_schedule_timer
from .runtime import workflow_orchestration_set_parameter
from .runtime import workflow_orchestration_signal_instance
from .runtime import workflow_orchestration_start_instance
from .runtime import workflow_orchestration_ui_binding_contract
from .runtime import workflow_orchestration_verify_owned_table_boundary
from .ui import WORKFLOW_ORCHESTRATION_UI_FRAGMENT_KEYS
from .ui import workflow_orchestration_render_workbench
from .ui import workflow_orchestration_ui_contract

PBC_KEY = "workflow_orchestration"


def implementation_contract() -> dict:
    runtime = workflow_orchestration_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "owned_tables": WORKFLOW_ORCHESTRATION_OWNED_TABLES,
        "runtime_tables": WORKFLOW_ORCHESTRATION_RUNTIME_TABLES,
        "allowed_database_backends": WORKFLOW_ORCHESTRATION_ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": WORKFLOW_ORCHESTRATION_REQUIRED_EVENT_TOPIC,
        "consumes": WORKFLOW_ORCHESTRATION_CONSUMED_EVENT_TYPES,
        "emits": WORKFLOW_ORCHESTRATION_EMITTED_EVENT_TYPES,
        "api_contract": workflow_orchestration_build_api_contract(),
        "schema_contract": workflow_orchestration_build_schema_contract(),
        "service_contract": workflow_orchestration_build_service_contract(),
        "release_evidence_contract": workflow_orchestration_build_release_evidence(),
        "permissions_contract": workflow_orchestration_permissions_contract(),
        "advanced_runtime": runtime,
        "ui_contract": workflow_orchestration_ui_contract(),
        "ui_binding_contract": workflow_orchestration_ui_binding_contract(),
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
