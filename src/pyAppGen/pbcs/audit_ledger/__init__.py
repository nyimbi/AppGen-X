"""Audit Ledger PBC implementation package."""

from ..source_contract import source_pbc_package_contract
from .runtime import AUDIT_LEDGER_ALLOWED_DATABASE_BACKENDS
from .runtime import AUDIT_LEDGER_CONSUMED_EVENT_TYPES
from .runtime import AUDIT_LEDGER_EMITTED_EVENT_TYPES
from .runtime import AUDIT_LEDGER_OWNED_TABLES
from .runtime import AUDIT_LEDGER_REQUIRED_EVENT_TOPIC
from .runtime import AUDIT_LEDGER_RUNTIME_CAPABILITY_KEYS
from .runtime import AUDIT_LEDGER_STANDARD_FEATURE_KEYS
from .runtime import audit_ledger_build_api_contract
from .runtime import audit_ledger_build_release_evidence
from .runtime import audit_ledger_build_schema_contract
from .runtime import audit_ledger_build_service_contract
from .runtime import audit_ledger_assert_control
from .runtime import audit_ledger_build_workbench_view
from .runtime import audit_ledger_configure_runtime
from .runtime import audit_ledger_define_retention_policy
from .runtime import audit_ledger_empty_state
from .runtime import audit_ledger_prepare_forensic_export
from .runtime import audit_ledger_publish_audit_projection
from .runtime import audit_ledger_record_access_evidence
from .runtime import audit_ledger_record_audit_event
from .runtime import audit_ledger_permissions_contract
from .runtime import audit_ledger_receive_event
from .runtime import audit_ledger_register_rule
from .runtime import audit_ledger_register_schema_extension
from .runtime import audit_ledger_runtime_capabilities
from .runtime import audit_ledger_runtime_smoke
from .runtime import audit_ledger_set_parameter
from .runtime import audit_ledger_verify_owned_table_boundary
from .runtime import audit_ledger_verify_signature_chain
from .ui import AUDIT_LEDGER_UI_FRAGMENT_KEYS
from .ui import audit_ledger_render_workbench
from .ui import audit_ledger_ui_contract

PBC_KEY = "audit_ledger"


def implementation_contract() -> dict:
    runtime = audit_ledger_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "owned_tables": AUDIT_LEDGER_OWNED_TABLES,
        "allowed_database_backends": AUDIT_LEDGER_ALLOWED_DATABASE_BACKENDS,
        "api_contract": audit_ledger_build_api_contract(),
        "schema_contract": audit_ledger_build_schema_contract(),
        "service_contract": audit_ledger_build_service_contract(),
        "release_evidence_contract": audit_ledger_build_release_evidence(),
        "permissions_contract": audit_ledger_permissions_contract(),
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": audit_ledger_ui_contract(),
        "required_event_topic": AUDIT_LEDGER_REQUIRED_EVENT_TOPIC,
        "emits": AUDIT_LEDGER_EMITTED_EVENT_TYPES,
        "consumes": AUDIT_LEDGER_CONSUMED_EVENT_TYPES,
    }
