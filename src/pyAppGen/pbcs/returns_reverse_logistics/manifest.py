"""Package manifest for the returns_reverse_logistics PBC."""

from .runtime import RETURNS_REVERSE_LOGISTICS_API_SURFACES
from .runtime import RETURNS_REVERSE_LOGISTICS_CONSUMED_EVENT_TYPES
from .runtime import RETURNS_REVERSE_LOGISTICS_EMITTED_EVENT_TYPES
from .runtime import RETURNS_REVERSE_LOGISTICS_OWNED_TABLES
from .runtime import RETURNS_REVERSE_LOGISTICS_RUNTIME_CAPABILITY_KEYS
from .runtime import RETURNS_REVERSE_LOGISTICS_RUNTIME_TABLES
from .runtime import RETURNS_REVERSE_LOGISTICS_STANDARD_FEATURE_KEYS

_BUSINESS_TABLES = tuple(table for table in RETURNS_REVERSE_LOGISTICS_OWNED_TABLES if table not in RETURNS_REVERSE_LOGISTICS_RUNTIME_TABLES)

PBC_MANIFEST = {
    "pbc": 'returns_reverse_logistics',
    "label": "Returns RMA and Reverse Logistics",
    "mesh": "commerce",
    "description": "Return authorization, reverse routing, receiving, inspection, disposition, credit, refund, exchange, repair, restock, carrier claim, exception, and customer-status orchestration.",
    "datastore_backend": "postgresql",
    "tables": _BUSINESS_TABLES,
    "apis": RETURNS_REVERSE_LOGISTICS_API_SURFACES,
    "emits": RETURNS_REVERSE_LOGISTICS_EMITTED_EVENT_TYPES,
    "consumes": RETURNS_REVERSE_LOGISTICS_CONSUMED_EVENT_TYPES,
    "template": None,
    "ui_fragments": (
        "ReturnsReverseLogisticsWorkbench",
        "ReturnAuthorizationConsole",
        "ReturnEligibilityPanel",
        "ReturnLabelConsole",
        "CarrierHandoffBoard",
        "ReceivingInspectionWorkbench",
        "DispositionDecisionBoard",
        "CreditAdjustmentConsole",
        "RefundExchangeResolutionPanel",
        "RecoveryOperationsPanel",
        "CarrierClaimsPanel",
        "ReturnExceptionBoard",
        "ReturnConfigurationPanel",
    ),
    "permissions": (
        "returns_reverse_logistics.authorize",
        "returns_reverse_logistics.label",
        "returns_reverse_logistics.inspect",
        "returns_reverse_logistics.adjust",
        "returns_reverse_logistics.event.consume",
        "returns_reverse_logistics.configure",
        "returns_reverse_logistics.audit",
        "returns_reverse_logistics.exception",
        "returns_reverse_logistics.claim",
    ),
    "configuration": (
        "RETURNS_REVERSE_LOGISTICS_DATABASE_URL",
        "RETURNS_REVERSE_LOGISTICS_EVENT_TOPIC",
        "RETURNS_REVERSE_LOGISTICS_RETRY_LIMIT",
        "RETURNS_REVERSE_LOGISTICS_DEFAULT_CURRENCY",
        "RETURNS_REVERSE_LOGISTICS_SUPPORTED_CARRIERS",
        "RETURNS_REVERSE_LOGISTICS_SUPPORTED_DISPOSITIONS",
    ),
    "capabilities": tuple(f"returns_reverse_logistics.{table}" for table in _BUSINESS_TABLES),
    "standard_features": RETURNS_REVERSE_LOGISTICS_STANDARD_FEATURE_KEYS,
    "workflows": (
        "command_returns",
        "command_labels",
        "command_receipts",
        "command_inspection_grades",
        "command_dispositions",
        "command_credit_adjustments",
        "command_refund_exchange",
        "command_carrier_claims",
        "query_returns_reverse_logistics_workbench",
    ),
    "analytics": (
        "authorization_rate",
        "eligibility_score",
        "route_margin",
        "return_cycle_time",
        "inspection_recovery_rate",
        "credit_accuracy",
        "carrier_claim_recovery",
        "landed_cost_accuracy",
        "return_authorized_throughput",
        "credit_adjustment_issued_throughput",
    ),
    "advanced_capabilities": RETURNS_REVERSE_LOGISTICS_RUNTIME_CAPABILITY_KEYS,
    "migrations": ("migrations/001_initial.sql",),
    "seed_data": ("seed_data.py",),
    "tests": ("tests/test_contract.py",),
    "docs": ("RELEASE_EVIDENCE.md", "SPECIFICATION.md"),
}
