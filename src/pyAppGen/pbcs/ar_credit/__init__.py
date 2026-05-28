"""Accounts Receivable and Credit PBC implementation package."""

from .manifest import PBC_MANIFEST

from ..source_contract import source_pbc_package_contract
from ..source_contract import source_package_metadata
from ..source_contract import validate_source_package_metadata
from ..source_contract import source_registration_plan
from .runtime import AR_CREDIT_ALLOWED_DATABASE_BACKENDS
from .runtime import AR_CREDIT_CONSUMED_EVENT_TYPES
from .runtime import AR_CREDIT_EMITTED_EVENT_TYPES
from .runtime import AR_CREDIT_OWNED_TABLES
from .runtime import AR_CREDIT_REQUIRED_EVENT_TOPIC
from .runtime import AR_CREDIT_STANDARD_FEATURE_KEYS
from .runtime import AR_CREDIT_RUNTIME_CAPABILITY_KEYS
from .runtime import ar_credit_apply_cash
from .runtime import ar_credit_build_api_contract
from .runtime import ar_credit_build_release_evidence
from .runtime import ar_credit_build_schema_contract
from .runtime import ar_credit_build_service_contract
from .runtime import ar_credit_build_workbench_view
from .runtime import ar_credit_calculate_aging
from .runtime import ar_credit_configure_runtime
from .runtime import ar_credit_create_credit_memo
from .runtime import ar_credit_create_dunning_plan
from .runtime import ar_credit_detect_cash_application_anomaly
from .runtime import ar_credit_empty_state
from .runtime import ar_credit_extend_credit
from .runtime import ar_credit_federate_cross_border_receivable
from .runtime import ar_credit_forecast_revenue_to_cash
from .runtime import ar_credit_generate_customer_statement
from .runtime import ar_credit_integrate_invoice_finance
from .runtime import ar_credit_issue_invoice
from .runtime import ar_credit_issue_refund
from .runtime import ar_credit_model_temporal_receivable
from .runtime import ar_credit_negotiate_payment_terms
from .runtime import ar_credit_onboard_customer
from .runtime import ar_credit_optimize_algebraic_collection
from .runtime import ar_credit_optimize_collection_strategy
from .runtime import ar_credit_parse_remittance
from .runtime import ar_credit_permissions_contract
from .runtime import ar_credit_receive_event
from .runtime import ar_credit_record_delivery_confirmation
from .runtime import ar_credit_record_unapplied_cash
from .runtime import ar_credit_recognize_revenue_schedule
from .runtime import ar_credit_register_governed_model
from .runtime import ar_credit_register_rule
from .runtime import ar_credit_register_schema_extension
from .runtime import ar_credit_resolve_dispute
from .runtime import ar_credit_rotate_crypto_epoch
from .runtime import ar_credit_route_collection
from .runtime import ar_credit_run_control_tests
from .runtime import ar_credit_run_resilience_drill
from .runtime import ar_credit_runtime_capabilities
from .runtime import ar_credit_runtime_smoke
from .runtime import ar_credit_schedule_carbon_aware_collection
from .runtime import ar_credit_schedule_collection_action
from .runtime import ar_credit_score_customer_default
from .runtime import ar_credit_screen_customer_network
from .runtime import ar_credit_set_parameter
from .runtime import ar_credit_submit_e_invoice
from .runtime import ar_credit_verify_customer_identity
from .runtime import ar_credit_verify_formal_invariants
from .runtime import ar_credit_verify_owned_table_boundary
from .runtime import ar_credit_verify_revenue_proof
from .runtime import ar_credit_write_off_receivable
from .receivables_workflows import AR_CREDIT_IMPLEMENTED_BACKLOG_ITEMS
from .receivables_workflows import AR_CREDIT_WORKFLOW_OPERATIONS
from .receivables_workflows import ar_credit_build_collections_follow_up
from .receivables_workflows import ar_credit_execute_customer_onboarding
from .receivables_workflows import ar_credit_execute_invoice_issuance
from .receivables_workflows import ar_credit_execute_receipt_application
from .receivables_workflows import ar_credit_review_credit_onboarding
from .receivables_workflows import ar_credit_review_invoice_readiness
from .receivables_workflows import ar_credit_workflow_release_evidence
from .ui import AR_CREDIT_UI_FRAGMENT_KEYS
from .ui import ar_credit_render_workbench
from .ui import ar_credit_ui_contract

PBC_KEY = "ar_credit"


def implementation_contract() -> dict:
    runtime = ar_credit_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": ar_credit_ui_contract(),
        "api_contract": ar_credit_build_api_contract(),
        "schema_contract": ar_credit_build_schema_contract(),
        "service_contract": ar_credit_build_service_contract(),
        "release_evidence_contract": ar_credit_build_release_evidence(),
        "permissions_contract": ar_credit_permissions_contract(),
        "owned_tables": AR_CREDIT_OWNED_TABLES,
        "allowed_database_backends": AR_CREDIT_ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": AR_CREDIT_REQUIRED_EVENT_TOPIC,
        "consumes": AR_CREDIT_CONSUMED_EVENT_TYPES,
        "emits": AR_CREDIT_EMITTED_EVENT_TYPES,
        "workflow_operations": AR_CREDIT_WORKFLOW_OPERATIONS,
        "implemented_backlog_items": AR_CREDIT_IMPLEMENTED_BACKLOG_ITEMS,
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
