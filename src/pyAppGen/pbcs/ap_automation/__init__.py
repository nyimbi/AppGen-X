"""Accounts Payable Automation PBC implementation package."""

from ..source_contract import source_pbc_package_contract
from .runtime import AP_AUTOMATION_ALLOWED_DATABASE_BACKENDS
from .runtime import AP_AUTOMATION_CONSUMED_EVENT_TYPES
from .runtime import AP_AUTOMATION_EMITTED_EVENT_TYPES
from .runtime import AP_AUTOMATION_OWNED_TABLES
from .runtime import AP_AUTOMATION_REQUIRED_EVENT_TOPIC
from .runtime import AP_AUTOMATION_STANDARD_FEATURE_KEYS
from .runtime import AP_AUTOMATION_RUNTIME_CAPABILITY_KEYS
from .runtime import ap_automation_align_contract_terms
from .runtime import ap_automation_analyze_discount_counterfactual
from .runtime import ap_automation_build_api_contract
from .runtime import ap_automation_build_workbench_view
from .runtime import ap_automation_capture_invoice
from .runtime import ap_automation_configure_runtime
from .runtime import ap_automation_detect_fraud_information_shift
from .runtime import ap_automation_empty_state
from .runtime import ap_automation_execute_payment
from .runtime import ap_automation_federate_cross_border_payment
from .runtime import ap_automation_forecast_cash_flow
from .runtime import ap_automation_integrate_supply_chain_finance
from .runtime import ap_automation_issue_purchase_order
from .runtime import ap_automation_match_invoice
from .runtime import ap_automation_model_temporal_liquidity
from .runtime import ap_automation_negotiate_dynamic_discount
from .runtime import ap_automation_onboard_vendor
from .runtime import ap_automation_optimize_algebraic_routing
from .runtime import ap_automation_optimize_payment_route
from .runtime import ap_automation_record_goods_receipt
from .runtime import ap_automation_register_governed_model
from .runtime import ap_automation_register_rule
from .runtime import ap_automation_register_schema_extension
from .runtime import ap_automation_receive_event
from .runtime import ap_automation_resolve_exception
from .runtime import ap_automation_rotate_crypto_epoch
from .runtime import ap_automation_run_control_tests
from .runtime import ap_automation_run_resilience_drill
from .runtime import ap_automation_permissions_contract
from .runtime import ap_automation_runtime_capabilities
from .runtime import ap_automation_runtime_smoke
from .runtime import ap_automation_schedule_carbon_aware_settlement
from .runtime import ap_automation_schedule_payments
from .runtime import ap_automation_score_vendor_risk
from .runtime import ap_automation_screen_vendor_network
from .runtime import ap_automation_set_parameter
from .runtime import ap_automation_submit_e_invoice
from .runtime import ap_automation_validate_tax_proof
from .runtime import ap_automation_verify_formal_invariants
from .runtime import ap_automation_verify_owned_table_boundary
from .runtime import ap_automation_verify_vendor_identity
from .ui import AP_AUTOMATION_UI_FRAGMENT_KEYS
from .ui import ap_automation_render_workbench
from .ui import ap_automation_ui_contract

PBC_KEY = "ap_automation"


def implementation_contract() -> dict:
    runtime = ap_automation_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": ap_automation_ui_contract(),
        "api_contract": ap_automation_build_api_contract(),
        "permissions_contract": ap_automation_permissions_contract(),
        "owned_tables": AP_AUTOMATION_OWNED_TABLES,
        "allowed_database_backends": AP_AUTOMATION_ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": AP_AUTOMATION_REQUIRED_EVENT_TOPIC,
        "consumes": AP_AUTOMATION_CONSUMED_EVENT_TYPES,
        "emits": AP_AUTOMATION_EMITTED_EVENT_TYPES,
    }
