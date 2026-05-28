"""Package manifest for the executable healthcare claims adjudication slice."""

# Audit trace key: 'claims_adjudication_healthcare'

from __future__ import annotations

from .config import PERMISSIONS
from .models import BUSINESS_TABLES
from .runtime import CLAIMS_ADJUDICATION_HEALTHCARE_RUNTIME_CAPABILITY_KEYS
from .runtime import CLAIMS_ADJUDICATION_HEALTHCARE_STANDARD_FEATURE_KEYS

PBC_MANIFEST = {
    "pbc": "claims_adjudication_healthcare",
    "label": "Healthcare Claims Adjudication",
    "description": "Healthcare claim intake, line adjudication, denials, appeals, payment integrity, and governed adjudication operations.",
    "mesh": "finops",
    "template": "domain-workbench",
    "version": "1.1.0",
    "datastore_backend": "postgresql",
    "tables": tuple(table.removeprefix("claims_adjudication_healthcare_") for table in BUSINESS_TABLES),
    "migrations": ("migrations/001_initial.sql",),
    "tests": (
        "tests/test_contract.py",
        "tests/test_executable_slice.py",
    ),
    "docs": (
        "README.md",
        "implementation-plan.md",
        "implementation-status.md",
        "RELEASE_EVIDENCE.md",
    ),
    "apis": (
        "POST /health-claims",
        "POST /claim-lines",
        "POST /coding-reviews",
        "POST /benefit-rules",
        "POST /denials",
        "POST /appeals",
        "POST /document-instructions",
        "GET /claims-adjudication-healthcare-workbench",
    ),
    "emits": (
        "ClaimsAdjudicationHealthcareCreated",
        "ClaimsAdjudicationHealthcareUpdated",
        "ClaimsAdjudicationHealthcareApproved",
        "ClaimsAdjudicationHealthcareExceptionOpened",
    ),
    "consumes": ("PolicyChanged", "AuditEventSealed", "OperationalKpiChanged"),
    "permissions": PERMISSIONS,
    "ui_fragments": (
        "ClaimsAdjudicationHealthcareWorkbench",
        "ClaimsAdjudicationHealthcareClaimDetail",
        "ClaimsAdjudicationHealthcareAssistantPanel",
    ),
    "workflows": (
        "claims_adjudication_healthcare_claim_intake_wizard",
        "claims_adjudication_healthcare_appeal_packet_wizard",
        "claims_adjudication_healthcare_duplicate_review_wizard",
    ),
    "configuration": (
        "CLAIMS_ADJUDICATION_HEALTHCARE_DATABASE_URL",
        "CLAIMS_ADJUDICATION_HEALTHCARE_EVENT_TOPIC",
        "CLAIMS_ADJUDICATION_HEALTHCARE_RETRY_LIMIT",
        "CLAIMS_ADJUDICATION_HEALTHCARE_DEFAULT_POLICY",
    ),
    "analytics": (
        "claims_queue_metrics",
        "denial_and_appeal_metrics",
        "payment_integrity_metrics",
    ),
    "standard_features": CLAIMS_ADJUDICATION_HEALTHCARE_STANDARD_FEATURE_KEYS,
    "advanced_capabilities": CLAIMS_ADJUDICATION_HEALTHCARE_RUNTIME_CAPABILITY_KEYS,
    "capabilities": CLAIMS_ADJUDICATION_HEALTHCARE_STANDARD_FEATURE_KEYS
    + CLAIMS_ADJUDICATION_HEALTHCARE_RUNTIME_CAPABILITY_KEYS,
    "seed_data": ("seed_data.py",),
}
