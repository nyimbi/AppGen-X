"""Payment Orchestration PBC implementation package."""

from ..source_contract import source_pbc_package_contract
from .runtime import PAYMENT_ORCHESTRATION_RUNTIME_CAPABILITY_KEYS
from .runtime import PAYMENT_ORCHESTRATION_STANDARD_FEATURE_KEYS
from .runtime import payment_orchestration_build_workbench_view
from .runtime import payment_orchestration_capture_payment
from .runtime import payment_orchestration_configure_runtime
from .runtime import payment_orchestration_create_payment_intent
from .runtime import payment_orchestration_empty_state
from .runtime import payment_orchestration_receive_event
from .runtime import payment_orchestration_refund_payment
from .runtime import payment_orchestration_register_gateway
from .runtime import payment_orchestration_register_rule
from .runtime import payment_orchestration_request_fraud_check
from .runtime import payment_orchestration_route_gateway
from .runtime import payment_orchestration_runtime_capabilities
from .runtime import payment_orchestration_runtime_smoke
from .runtime import payment_orchestration_set_parameter
from .runtime import payment_orchestration_tokenize_payment_method
from .runtime import payment_orchestration_void_payment
from .ui import PAYMENT_ORCHESTRATION_UI_FRAGMENT_KEYS
from .ui import payment_orchestration_render_workbench
from .ui import payment_orchestration_ui_contract

PBC_KEY = "payment_orchestration"


def implementation_contract() -> dict:
    runtime = payment_orchestration_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": payment_orchestration_ui_contract(),
    }
