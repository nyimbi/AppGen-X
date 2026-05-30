"""Package manifest for the food_safety_quality_compliance PBC."""

from .slice_app import DOMAIN_OPERATIONS
from .slice_app import DOMAIN_PARAMETERS
from .slice_app import DOMAIN_RULES
from .slice_app import OWNED_TABLES
from .slice_app import PBC_KEY
from .slice_app import ROUTES
from .slice_app import RUNTIME_CAPABILITY_KEYS
from .slice_app import STANDARD_FEATURE_KEYS
from .slice_app import UI_FRAGMENT_KEYS
from .slice_app import WORKFLOWS

PBC_MANIFEST = {
    "pbc": PBC_KEY,
    "label": "Food Safety Quality Compliance",
    "description": "HACCP plans, critical control points, inspections, recalls, supplier audits, quality holds, and regulatory evidence.",
    "mesh": "opsmfg",
    "template": "asset",
    "version": "1.1.0",
    "datastore_backend": "postgresql",
    "tables": tuple(table.removeprefix(f"{PBC_KEY}_") for table in OWNED_TABLES[:-3]),
    "capabilities": STANDARD_FEATURE_KEYS + RUNTIME_CAPABILITY_KEYS,
    "standard_features": STANDARD_FEATURE_KEYS,
    "advanced_capabilities": RUNTIME_CAPABILITY_KEYS,
    "apis": ROUTES,
    "emits": (
        "FoodSafetyQualityComplianceCreated",
        "FoodSafetyQualityComplianceUpdated",
        "FoodSafetyQualityComplianceApproved",
        "FoodSafetyQualityComplianceExceptionOpened",
    ),
    "consumes": ("PolicyChanged", "AuditEventSealed", "OperationalKpiChanged"),
    "permissions": (
        f"{PBC_KEY}.read",
        f"{PBC_KEY}.create",
        f"{PBC_KEY}.update",
        f"{PBC_KEY}.approve",
        f"{PBC_KEY}.admin",
    ),
    "configuration": (
        "FOOD_SAFETY_QUALITY_COMPLIANCE_DATABASE_URL",
        "FOOD_SAFETY_QUALITY_COMPLIANCE_EVENT_TOPIC",
        "FOOD_SAFETY_QUALITY_COMPLIANCE_RETRY_LIMIT",
        "FOOD_SAFETY_QUALITY_COMPLIANCE_DEFAULT_POLICY",
    ),
    "workflows": WORKFLOWS,
    "docs": ("README.md", "SPECIFICATION.md", "RELEASE_EVIDENCE.md", "implementation-status.md"),
    "migrations": ("migrations/001_initial.sql",),
    "tests": ("tests/test_contract.py", "tests/test_slice_app.py"),
    "seed_data": ("seed_data.py",),
    "ui_fragments": UI_FRAGMENT_KEYS,
    "rules": DOMAIN_RULES,
    "parameters": DOMAIN_PARAMETERS,
    "operations": DOMAIN_OPERATIONS,
}
