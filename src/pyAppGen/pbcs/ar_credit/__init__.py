"""Accounts Receivable and Credit PBC implementation package."""

from ..source_contract import source_pbc_package_contract
from .runtime import AR_CREDIT_STANDARD_FEATURE_KEYS
from .runtime import AR_CREDIT_RUNTIME_CAPABILITY_KEYS
from .runtime import ar_credit_apply_cash
from .runtime import ar_credit_build_api_contract
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
from .runtime import ar_credit_verify_revenue_proof
from .runtime import ar_credit_write_off_receivable
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
    }
