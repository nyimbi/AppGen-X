"""Fraud Anomaly Detection PBC implementation package."""

from .manifest import PBC_MANIFEST

from ..source_contract import source_pbc_package_contract
from ..source_contract import source_package_metadata
from ..source_contract import validate_source_package_metadata
from ..source_contract import source_registration_plan
from .runtime import FRAUD_ANOMALY_DETECTION_ALLOWED_DATABASE_BACKENDS
from .runtime import FRAUD_ANOMALY_DETECTION_CONSUMED_EVENT_TYPES
from .runtime import FRAUD_ANOMALY_DETECTION_EMITTED_EVENT_TYPES
from .runtime import FRAUD_ANOMALY_DETECTION_OWNED_TABLES
from .runtime import FRAUD_ANOMALY_DETECTION_REQUIRED_EVENT_TOPIC
from .runtime import FRAUD_ANOMALY_DETECTION_RUNTIME_CAPABILITY_KEYS
from .runtime import FRAUD_ANOMALY_DETECTION_RUNTIME_TABLES
from .runtime import FRAUD_ANOMALY_DETECTION_STANDARD_FEATURE_KEYS
from .runtime import fraud_anomaly_detection_build_api_contract
from .runtime import fraud_anomaly_detection_build_release_evidence
from .runtime import fraud_anomaly_detection_build_schema_contract
from .runtime import fraud_anomaly_detection_build_service_contract
from .runtime import fraud_anomaly_detection_build_workbench_view
from .runtime import fraud_anomaly_detection_calculate_velocity_window
from .runtime import fraud_anomaly_detection_configure_runtime
from .runtime import fraud_anomaly_detection_empty_state
from .runtime import fraud_anomaly_detection_enqueue_analyst_case
from .runtime import fraud_anomaly_detection_explain_decision
from .runtime import fraud_anomaly_detection_ingest_risk_signal
from .runtime import fraud_anomaly_detection_link_identity
from .runtime import fraud_anomaly_detection_open_risk_case
from .runtime import fraud_anomaly_detection_permissions_contract
from .runtime import fraud_anomaly_detection_project_loss_exposure
from .runtime import fraud_anomaly_detection_receive_event
from .runtime import fraud_anomaly_detection_record_device_fingerprint
from .runtime import fraud_anomaly_detection_record_network_indicator
from .runtime import fraud_anomaly_detection_register_fraud_rule
from .runtime import fraud_anomaly_detection_register_rule
from .runtime import fraud_anomaly_detection_register_schema_extension
from .runtime import fraud_anomaly_detection_runtime_capabilities
from .runtime import fraud_anomaly_detection_runtime_smoke
from .runtime import fraud_anomaly_detection_score_anomaly
from .runtime import fraud_anomaly_detection_set_parameter
from .runtime import fraud_anomaly_detection_update_behavior_baseline
from .runtime import fraud_anomaly_detection_verify_owned_table_boundary
from .ui import FRAUD_ANOMALY_DETECTION_UI_FRAGMENT_KEYS
from .ui import fraud_anomaly_detection_render_workbench
from .ui import fraud_anomaly_detection_ui_contract
from .ui import fraud_anomaly_detection_forms_contract
from .ui import fraud_anomaly_detection_wizards_contract
from .ui import fraud_anomaly_detection_controls_contract
from .app_surface import app_surface_smoke_test
from .app_surface import document_instruction_fraud_anomaly_detection_plan
from .app_surface import single_pbc_fraud_anomaly_detection_app_contract

PBC_KEY = "fraud_anomaly_detection"


def implementation_contract() -> dict:
    runtime = fraud_anomaly_detection_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": fraud_anomaly_detection_ui_contract(),
        "single_pbc_app": single_pbc_fraud_anomaly_detection_app_contract(),
        "app_surface_smoke": app_surface_smoke_test(),
        "api_contract": fraud_anomaly_detection_build_api_contract(),
        "schema_contract": fraud_anomaly_detection_build_schema_contract(),
        "service_contract": fraud_anomaly_detection_build_service_contract(),
        "release_evidence_contract": fraud_anomaly_detection_build_release_evidence(),
        "permissions_contract": fraud_anomaly_detection_permissions_contract(),
        "owned_tables": FRAUD_ANOMALY_DETECTION_OWNED_TABLES,
        "runtime_tables": FRAUD_ANOMALY_DETECTION_RUNTIME_TABLES,
        "allowed_database_backends": FRAUD_ANOMALY_DETECTION_ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": FRAUD_ANOMALY_DETECTION_REQUIRED_EVENT_TOPIC,
        "emits": FRAUD_ANOMALY_DETECTION_EMITTED_EVENT_TYPES,
        "consumes": FRAUD_ANOMALY_DETECTION_CONSUMED_EVENT_TYPES,
        "boundary_contract": fraud_anomaly_detection_verify_owned_table_boundary(),
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
