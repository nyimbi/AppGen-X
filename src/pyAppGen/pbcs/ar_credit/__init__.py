"""Accounts Receivable and Credit PBC implementation package."""

from ..source_contract import source_pbc_package_contract
from .runtime import AR_CREDIT_RUNTIME_CAPABILITY_KEYS
from .runtime import ar_credit_apply_cash
from .runtime import ar_credit_build_api_contract
from .runtime import ar_credit_detect_cash_application_anomaly
from .runtime import ar_credit_empty_state
from .runtime import ar_credit_extend_credit
from .runtime import ar_credit_federate_cross_border_receivable
from .runtime import ar_credit_forecast_revenue_to_cash
from .runtime import ar_credit_integrate_invoice_finance
from .runtime import ar_credit_issue_invoice
from .runtime import ar_credit_model_temporal_receivable
from .runtime import ar_credit_negotiate_payment_terms
from .runtime import ar_credit_onboard_customer
from .runtime import ar_credit_optimize_algebraic_collection
from .runtime import ar_credit_optimize_collection_strategy
from .runtime import ar_credit_parse_remittance
from .runtime import ar_credit_record_delivery_confirmation
from .runtime import ar_credit_register_governed_model
from .runtime import ar_credit_register_schema_extension
from .runtime import ar_credit_resolve_dispute
from .runtime import ar_credit_rotate_crypto_epoch
from .runtime import ar_credit_route_collection
from .runtime import ar_credit_run_control_tests
from .runtime import ar_credit_run_resilience_drill
from .runtime import ar_credit_runtime_capabilities
from .runtime import ar_credit_runtime_smoke
from .runtime import ar_credit_schedule_carbon_aware_collection
from .runtime import ar_credit_score_customer_default
from .runtime import ar_credit_screen_customer_network
from .runtime import ar_credit_submit_e_invoice
from .runtime import ar_credit_verify_customer_identity
from .runtime import ar_credit_verify_formal_invariants
from .runtime import ar_credit_verify_revenue_proof

PBC_KEY = "ar_credit"


def implementation_contract() -> dict:
    runtime = ar_credit_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "advanced_runtime": runtime,
    }
