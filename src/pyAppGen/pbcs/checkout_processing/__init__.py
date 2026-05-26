"""Checkout Processing PBC implementation package."""

from ..source_contract import source_pbc_package_contract
from .runtime import CHECKOUT_PROCESSING_REQUIRED_EVENT_TOPIC
from .runtime import CHECKOUT_PROCESSING_RUNTIME_CAPABILITY_KEYS
from .runtime import CHECKOUT_PROCESSING_STANDARD_FEATURE_KEYS
from .runtime import checkout_processing_allocate_promotion_value
from .runtime import checkout_processing_add_cart_line
from .runtime import checkout_processing_apply_coupon
from .runtime import checkout_processing_apply_tax_handoff
from .runtime import checkout_processing_build_api_contract
from .runtime import checkout_processing_build_workbench_view
from .runtime import checkout_processing_complete_checkout
from .runtime import checkout_processing_configure_runtime
from .runtime import checkout_processing_create_cart
from .runtime import checkout_processing_create_payment_intent
from .runtime import checkout_processing_detect_checkout_anomaly
from .runtime import checkout_processing_empty_state
from .runtime import checkout_processing_federate_checkout_view
from .runtime import checkout_processing_forecast_abandonment
from .runtime import checkout_processing_generate_checkout_proof
from .runtime import checkout_processing_model_stochastic_checkout_exposure
from .runtime import checkout_processing_open_checkout_session
from .runtime import checkout_processing_optimize_checkout_path
from .runtime import checkout_processing_parse_instruction
from .runtime import checkout_processing_predictive_risk_score
from .runtime import checkout_processing_receive_event
from .runtime import checkout_processing_register_governed_model
from .runtime import checkout_processing_register_rule
from .runtime import checkout_processing_register_schema_extension
from .runtime import checkout_processing_reserve_inventory_handoff
from .runtime import checkout_processing_resolve_checkout_exception
from .runtime import checkout_processing_rotate_crypto_epoch
from .runtime import checkout_processing_route_checkout
from .runtime import checkout_processing_run_control_tests
from .runtime import checkout_processing_run_resilience_drill
from .runtime import checkout_processing_runtime_capabilities
from .runtime import checkout_processing_runtime_smoke
from .runtime import checkout_processing_score_conversion_probability
from .runtime import checkout_processing_screen_checkout_policy
from .runtime import checkout_processing_screen_risk
from .runtime import checkout_processing_select_carbon_aware_fulfillment
from .runtime import checkout_processing_set_parameter
from .runtime import checkout_processing_simulate_counterfactual_checkout
from .runtime import checkout_processing_validate_shipping_address
from .runtime import checkout_processing_verify_formal_invariants
from .ui import CHECKOUT_PROCESSING_UI_FRAGMENT_KEYS
from .ui import checkout_processing_render_workbench
from .ui import checkout_processing_ui_contract

PBC_KEY = "checkout_processing"


def implementation_contract() -> dict:
    runtime = checkout_processing_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": checkout_processing_ui_contract(),
    }
