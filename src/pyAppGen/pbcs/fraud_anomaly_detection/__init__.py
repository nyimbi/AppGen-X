"""Fraud Anomaly Detection PBC implementation package."""

from ..source_contract import source_pbc_package_contract
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
from .runtime import fraud_anomaly_detection_configure_runtime
from .runtime import fraud_anomaly_detection_empty_state
from .runtime import fraud_anomaly_detection_ingest_risk_signal
from .runtime import fraud_anomaly_detection_open_risk_case
from .runtime import fraud_anomaly_detection_permissions_contract
from .runtime import fraud_anomaly_detection_receive_event
from .runtime import fraud_anomaly_detection_register_fraud_rule
from .runtime import fraud_anomaly_detection_register_rule
from .runtime import fraud_anomaly_detection_register_schema_extension
from .runtime import fraud_anomaly_detection_runtime_capabilities
from .runtime import fraud_anomaly_detection_runtime_smoke
from .runtime import fraud_anomaly_detection_score_anomaly
from .runtime import fraud_anomaly_detection_set_parameter
from .runtime import fraud_anomaly_detection_verify_owned_table_boundary
from .ui import FRAUD_ANOMALY_DETECTION_UI_FRAGMENT_KEYS
from .ui import fraud_anomaly_detection_render_workbench
from .ui import fraud_anomaly_detection_ui_contract

PBC_KEY = "fraud_anomaly_detection"


def implementation_contract() -> dict:
    runtime = fraud_anomaly_detection_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": fraud_anomaly_detection_ui_contract(),
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
