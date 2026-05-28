"""Package manifest for the checkout_processing PBC."""

from __future__ import annotations

from .runtime import CHECKOUT_PROCESSING_ALLOWED_DATABASE_BACKENDS
from .runtime import CHECKOUT_PROCESSING_CONSUMED_EVENT_TYPES
from .runtime import CHECKOUT_PROCESSING_EMITTED_EVENT_TYPES
from .runtime import CHECKOUT_PROCESSING_OWNED_TABLES
from .runtime import CHECKOUT_PROCESSING_RUNTIME_CAPABILITY_KEYS
from .runtime import CHECKOUT_PROCESSING_STANDARD_FEATURE_KEYS


PBC_KEY = "checkout_processing"
# Audit trace key: 'checkout_processing'

CHECKOUT_PROCESSING_TABLES = (
    "cart",
    "cart_line",
    "checkout_session",
    "promotion_redemption",
    "checkout_pricing_handoff",
    "checkout_tax_handoff",
    "checkout_inventory_reservation_handoff",
    "checkout_payment_intent_handoff",
    "checkout_risk_screen",
    "checkout_address_validation",
    "checkout_rule",
    "checkout_parameter",
    "checkout_configuration",
    "checkout_processing_appgen_outbox_event",
    "checkout_processing_appgen_inbox_event",
    "checkout_processing_dead_letter_event",
)


PBC_MANIFEST = {
    "pbc": PBC_KEY,
    "label": "Headless Cart and Checkout Processing",
    "mesh": "commerce",
    "description": "Checkout-owned cart orchestration, handoff governance, workbench operations, and assistant-safe CRUD previews.",
    "datastore_backend": "postgresql",
    "datastore_backends": CHECKOUT_PROCESSING_ALLOWED_DATABASE_BACKENDS,
    "tables": CHECKOUT_PROCESSING_TABLES,
    "owned_tables": CHECKOUT_PROCESSING_OWNED_TABLES,
    "apis": (
        "POST /carts",
        "POST /cart-lines",
        "POST /checkout",
        "POST /coupons",
        "POST /checkout/inventory-confirmations",
        "POST /checkout/payment-authorizations",
        "POST /checkout/payment-captures",
        "GET /checkout-processing-workbench",
        "GET /checkout-processing/controls",
        "POST /checkout-processing/assistant/document-preview",
    ),
    "emits": CHECKOUT_PROCESSING_EMITTED_EVENT_TYPES,
    "consumes": CHECKOUT_PROCESSING_CONSUMED_EVENT_TYPES,
    "template": "sales",
    "ui_fragments": (
        "CheckoutWorkbench",
        "CartConsole",
        "CheckoutSessionConsole",
        "CheckoutRuleStudio",
        "InboxOutboxMonitor",
        "AssistantPreviewWorkbench",
        "ControlCenter",
    ),
    "permissions": (
        "checkout_processing.cart",
        "checkout_processing.checkout",
        "checkout_processing.pricing",
        "checkout_processing.promotion",
        "checkout_processing.inventory",
        "checkout_processing.payment",
        "checkout_processing.risk",
        "checkout_processing.event.consume",
        "checkout_processing.configure",
        "checkout_processing.audit",
    ),
    "configuration": (
        "CHECKOUT_PROCESSING_DATABASE_URL",
        "CHECKOUT_PROCESSING_EVENT_TOPIC",
        "CHECKOUT_PROCESSING_DEFAULT_CURRENCY",
        "CHECKOUT_PROCESSING_DEFAULT_COUNTRY",
        "CHECKOUT_PROCESSING_RETRY_LIMIT",
        "CHECKOUT_PROCESSING_WORKBENCH_LIMIT",
    ),
    "capabilities": tuple(f"checkout_processing.{table}" for table in CHECKOUT_PROCESSING_TABLES),
    "standard_features": CHECKOUT_PROCESSING_STANDARD_FEATURE_KEYS,
    "workflows": (
        "command_carts",
        "command_checkout",
        "command_inventory_confirmations",
        "command_payment_authorizations",
        "command_payment_captures",
        "command_coupons",
        "query_checkout_processing_workbench",
        "query_checkout_processing_controls",
        "query_checkout_processing_assistant_preview",
    ),
    "analytics": (
        "checkout_conversion_probability",
        "checkout_abandonment_forecast",
        "inventory_confirmation_rate",
        "captured_payment_rate",
        "dead_letter_backlog",
        "release_gate_readiness",
    ),
    "advanced_capabilities": CHECKOUT_PROCESSING_RUNTIME_CAPABILITY_KEYS,
    "migrations": ("migrations/001_initial.sql",),
    "seed_data": ("seed_data.py",),
    "tests": (
        "tests/test_contract.py",
        "tests/test_app_surface.py",
    ),
    "docs": (
        "README.md",
        "SPECIFICATION.md",
        "RELEASE_EVIDENCE.md",
        "implementation-plan.md",
        "implementation-status.md",
    ),
}
