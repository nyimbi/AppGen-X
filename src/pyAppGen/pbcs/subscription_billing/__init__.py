"""Subscription Billing PBC implementation package."""

from ..source_contract import source_pbc_package_contract
from .runtime import SUBSCRIPTION_BILLING_ALLOWED_DATABASE_BACKENDS
from .runtime import SUBSCRIPTION_BILLING_API_ROUTES
from .runtime import SUBSCRIPTION_BILLING_EMITTED_EVENT_TYPES
from .runtime import SUBSCRIPTION_BILLING_OWNED_TABLES
from .runtime import SUBSCRIPTION_BILLING_RUNTIME_CAPABILITY_KEYS
from .runtime import SUBSCRIPTION_BILLING_STANDARD_FEATURE_KEYS
from .runtime import subscription_billing_build_api_contract
from .runtime import subscription_billing_build_workbench_view
from .runtime import subscription_billing_configure_runtime
from .runtime import subscription_billing_create_dunning_notice
from .runtime import subscription_billing_create_subscription
from .runtime import subscription_billing_empty_state
from .runtime import subscription_billing_generate_invoice
from .runtime import subscription_billing_receive_event
from .runtime import subscription_billing_record_usage
from .runtime import subscription_billing_register_plan
from .runtime import subscription_billing_register_rule
from .runtime import subscription_billing_register_schema_extension
from .runtime import subscription_billing_renew_subscription
from .runtime import subscription_billing_permissions_contract
from .runtime import subscription_billing_runtime_capabilities
from .runtime import subscription_billing_runtime_smoke
from .runtime import subscription_billing_set_parameter
from .runtime import subscription_billing_verify_owned_table_boundary
from .ui import SUBSCRIPTION_BILLING_UI_FRAGMENT_KEYS
from .ui import subscription_billing_render_workbench
from .ui import subscription_billing_ui_contract

PBC_KEY = "subscription_billing"


def implementation_contract() -> dict:
    runtime = subscription_billing_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": subscription_billing_ui_contract(),
        "api_contract": subscription_billing_build_api_contract(),
        "permissions_contract": subscription_billing_permissions_contract(),
        "owned_tables": SUBSCRIPTION_BILLING_OWNED_TABLES,
        "allowed_database_backends": SUBSCRIPTION_BILLING_ALLOWED_DATABASE_BACKENDS,
    }
