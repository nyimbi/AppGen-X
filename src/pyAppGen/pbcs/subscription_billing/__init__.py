"""Subscription Billing PBC implementation package."""

from ..source_contract import source_pbc_package_contract
from .runtime import SUBSCRIPTION_BILLING_ALLOWED_DATABASE_BACKENDS
from .runtime import SUBSCRIPTION_BILLING_API_ROUTES
from .runtime import SUBSCRIPTION_BILLING_CONSUMED_EVENT_TYPES
from .runtime import SUBSCRIPTION_BILLING_EMITTED_EVENT_TYPES
from .runtime import SUBSCRIPTION_BILLING_OWNED_TABLES
from .runtime import SUBSCRIPTION_BILLING_REQUIRED_EVENT_TOPIC
from .runtime import SUBSCRIPTION_BILLING_RUNTIME_CAPABILITY_KEYS
from .runtime import SUBSCRIPTION_BILLING_RUNTIME_TABLES
from .runtime import SUBSCRIPTION_BILLING_SCHEMA_TABLES
from .runtime import SUBSCRIPTION_BILLING_STANDARD_FEATURE_KEYS
from .runtime import subscription_billing_build_api_contract
from .runtime import subscription_billing_build_release_evidence
from .runtime import subscription_billing_build_schema_contract
from .runtime import subscription_billing_build_service_contract
from .runtime import subscription_billing_build_workbench_view
from .runtime import subscription_billing_configure_runtime
from .runtime import subscription_billing_create_dunning_notice
from .runtime import subscription_billing_create_subscription
from .runtime import subscription_billing_empty_state
from .runtime import subscription_billing_generate_invoice
from .runtime import subscription_billing_run_control_tests
from .runtime import subscription_billing_receive_event
from .runtime import subscription_billing_record_usage
from .runtime import subscription_billing_register_plan
from .runtime import subscription_billing_register_rule
from .runtime import subscription_billing_register_schema_extension
from .runtime import subscription_billing_renew_subscription
from .runtime import subscription_billing_permissions_contract
from .runtime import subscription_billing_runtime_capabilities
from .runtime import subscription_billing_runtime_smoke
from .runtime import subscription_billing_score_revenue_exposure
from .runtime import subscription_billing_set_parameter
from .runtime import subscription_billing_simulate_proration_quote
from .runtime import subscription_billing_ui_binding_contract
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
        "schema_contract": subscription_billing_build_schema_contract(),
        "service_contract": subscription_billing_build_service_contract(),
        "release_evidence_contract": subscription_billing_build_release_evidence(),
        "ui_binding_contract": subscription_billing_ui_binding_contract(),
        "permissions_contract": subscription_billing_permissions_contract(),
        "owned_tables": SUBSCRIPTION_BILLING_OWNED_TABLES,
        "runtime_tables": SUBSCRIPTION_BILLING_RUNTIME_TABLES,
        "schema_tables": SUBSCRIPTION_BILLING_SCHEMA_TABLES,
        "allowed_database_backends": SUBSCRIPTION_BILLING_ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": SUBSCRIPTION_BILLING_REQUIRED_EVENT_TOPIC,
        "consumes": SUBSCRIPTION_BILLING_CONSUMED_EVENT_TYPES,
        "emits": SUBSCRIPTION_BILLING_EMITTED_EVENT_TYPES,
    }
