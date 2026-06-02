"""Accounts Payable Automation PBC implementation package."""

from .manifest import PBC_MANIFEST

from ..source_contract import source_package_metadata
from ..source_contract import source_pbc_package_contract
from ..source_contract import source_registration_plan
from ..source_contract import validate_source_package_metadata
from .controls import control_contract
from .forms import form_contract
from .forms import render_form
from .repository import repository_contract
from .repository import build_demo_state as repository_demo_state
from .runtime import AP_AUTOMATION_ALLOWED_DATABASE_BACKENDS
from .runtime import AP_AUTOMATION_CONSUMED_EVENT_TYPES
from .runtime import AP_AUTOMATION_EMITTED_EVENT_TYPES
from .runtime import AP_AUTOMATION_OWNED_TABLES
from .runtime import AP_AUTOMATION_REQUIRED_EVENT_TOPIC
from .runtime import AP_AUTOMATION_RUNTIME_CAPABILITY_KEYS
from .runtime import AP_AUTOMATION_STANDARD_FEATURE_KEYS
from .runtime import ap_automation_align_contract_terms
from .runtime import ap_automation_analyze_discount_counterfactual
from .runtime import ap_automation_build_api_contract
from .runtime import ap_automation_build_release_evidence
from .runtime import ap_automation_build_schema_contract
from .runtime import ap_automation_build_service_contract
from .runtime import ap_automation_build_workbench_view
from .runtime import ap_automation_capture_invoice
from .runtime import ap_automation_configure_runtime
from .runtime import ap_automation_create_approval_task
from .runtime import ap_automation_create_payment_batch
from .runtime import ap_automation_detect_fraud_information_shift
from .runtime import ap_automation_empty_state
from .runtime import ap_automation_execute_payment
from .runtime import ap_automation_extract_invoice_artifact
from .runtime import ap_automation_federate_cross_border_payment
from .runtime import ap_automation_forecast_cash_flow
from .runtime import ap_automation_generate_remittance_advice
from .runtime import ap_automation_integrate_supply_chain_finance
from .runtime import ap_automation_issue_purchase_order
from .runtime import ap_automation_match_invoice
from .runtime import ap_automation_model_temporal_liquidity
from .runtime import ap_automation_negotiate_dynamic_discount
from .runtime import ap_automation_onboard_vendor
from .runtime import ap_automation_optimize_algebraic_routing
from .runtime import ap_automation_optimize_payment_route
from .runtime import ap_automation_permissions_contract
from .runtime import ap_automation_receive_event
from .runtime import ap_automation_reconcile_vendor_statement
from .runtime import ap_automation_record_goods_receipt
from .runtime import ap_automation_register_governed_model
from .runtime import ap_automation_register_rule
from .runtime import ap_automation_register_schema_extension
from .runtime import ap_automation_register_vendor_tax_profile
from .runtime import ap_automation_resolve_exception
from .runtime import ap_automation_rotate_crypto_epoch
from .runtime import ap_automation_run_control_tests
from .runtime import ap_automation_run_resilience_drill
from .runtime import ap_automation_runtime_capabilities
from .runtime import ap_automation_runtime_smoke
from .runtime import ap_automation_schedule_carbon_aware_settlement
from .runtime import ap_automation_schedule_payments
from .runtime import ap_automation_score_vendor_risk
from .runtime import ap_automation_screen_vendor_network
from .runtime import ap_automation_set_parameter
from .runtime import ap_automation_submit_e_invoice
from .runtime import ap_automation_validate_tax_proof
from .runtime import ap_automation_validate_vendor_bank_account
from .runtime import ap_automation_verify_formal_invariants
from .runtime import ap_automation_verify_owned_table_boundary
from .runtime import ap_automation_verify_vendor_identity
from .ui import AP_AUTOMATION_UI_FRAGMENT_KEYS
from .ui import ap_automation_render_workbench
from .ui import ap_automation_ui_contract
from .wizards import execute_wizard
from .wizards import plan_wizard
from .wizards import wizard_contract

PBC_KEY = "ap_automation"


def implementation_contract() -> dict:
    runtime = ap_automation_runtime_capabilities()
    repository = repository_contract()
    forms = form_contract()
    wizards = wizard_contract()
    controls = control_contract()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": ap_automation_ui_contract(),
        "api_contract": ap_automation_build_api_contract(),
        "schema_contract": ap_automation_build_schema_contract(),
        "service_contract": ap_automation_build_service_contract(),
        "release_evidence_contract": ap_automation_build_release_evidence(),
        "permissions_contract": ap_automation_permissions_contract(),
        "repository_contract": repository,
        "forms_contract": forms,
        "wizard_contract": wizards,
        "control_contract": controls,
        "owned_tables": AP_AUTOMATION_OWNED_TABLES,
        "allowed_database_backends": AP_AUTOMATION_ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": AP_AUTOMATION_REQUIRED_EVENT_TOPIC,
        "consumes": AP_AUTOMATION_CONSUMED_EVENT_TYPES,
        "emits": AP_AUTOMATION_EMITTED_EVENT_TYPES,
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
