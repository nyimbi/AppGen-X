"""Package manifest for the professional_services_automation PBC."""

from __future__ import annotations

PBC_KEY_LITERAL = 'professional_services_automation'

from .runtime import PROFESSIONAL_SERVICES_AUTOMATION_CONSUMED_EVENT_TYPES
from .runtime import PROFESSIONAL_SERVICES_AUTOMATION_EMITTED_EVENT_TYPES
from .runtime import PROFESSIONAL_SERVICES_AUTOMATION_STANDARD_FEATURE_KEYS
from .runtime import professional_services_automation_build_api_contract
from .runtime import professional_services_automation_runtime_capabilities


_RUNTIME_CAPABILITIES = professional_services_automation_runtime_capabilities()
_API_CONTRACT = professional_services_automation_build_api_contract()

PBC_MANIFEST = {
    "pbc": "professional_services_automation",
    "label": "Professional Services Automation",
    "mesh": "relationship",
    "description": "Standalone PSA package for engagements, SOWs, staffing, time, billing readiness, utilization, margin, and delivery risk operations.",
    "datastore_backend": "postgresql",
    "tables": (
        "client_engagement",
        "statement_of_work",
        "engagement_staffing",
        "delivery_milestone",
        "billable_time_entry",
        "billing_milestone",
        "utilization_snapshot",
        "engagement_margin",
    ),
    "apis": _API_CONTRACT["routes"],
    "emits": PROFESSIONAL_SERVICES_AUTOMATION_EMITTED_EVENT_TYPES,
    "consumes": PROFESSIONAL_SERVICES_AUTOMATION_CONSUMED_EVENT_TYPES,
    "template": "standalone_one_pbc_app",
    "ui_fragments": (
        "ProfessionalServicesAutomationWorkbench",
        "ProfessionalServicesAutomationDetail",
        "ProfessionalServicesAutomationAssistantPanel",
    ),
    "permissions": (
        "professional_services_automation.read",
        "professional_services_automation.create",
        "professional_services_automation.update",
        "professional_services_automation.approve",
        "professional_services_automation.admin",
    ),
    "configuration": (
        "PROFESSIONAL_SERVICES_AUTOMATION_DATABASE_URL",
        "PROFESSIONAL_SERVICES_AUTOMATION_EVENT_TOPIC",
        "PROFESSIONAL_SERVICES_AUTOMATION_RETRY_LIMIT",
        "PROFESSIONAL_SERVICES_AUTOMATION_DEFAULT_POLICY",
    ),
    "capabilities": tuple(_RUNTIME_CAPABILITIES["capabilities"]),
    "standard_features": PROFESSIONAL_SERVICES_AUTOMATION_STANDARD_FEATURE_KEYS,
    "workflows": tuple(
        operation
        for operation in _RUNTIME_CAPABILITIES["operations"]
        if operation
        and not operation.startswith("build_")
        and operation not in {"permissions_contract", "verify_owned_table_boundary"}
    ),
    "analytics": (
        "psa_utilization_forecast",
        "psa_margin_variance",
        "psa_delivery_risk_score",
        "psa_billing_blocker_age",
    ),
    "advanced_capabilities": tuple(_RUNTIME_CAPABILITIES["capabilities"]),
    "domain_advanced_capabilities": tuple(_RUNTIME_CAPABILITIES["domain_advanced_capabilities"]),
    "migrations": ("migrations/001_initial.sql",),
    "seed_data": ("seed_data.py",),
    "tests": (
        "tests/test_contract.py",
        "tests/test_standalone.py",
    ),
    "docs": (
        "SPECIFICATION.md",
        "README.md",
        "implementation-plan.md",
        "implementation-status.md",
        "RELEASE_EVIDENCE.md",
    ),
    "version": "1.0.0",
}
