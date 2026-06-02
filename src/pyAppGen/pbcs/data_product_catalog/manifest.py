"""Package manifest for the data_product_catalog PBC."""
from __future__ import annotations

from .blueprint import (
    ADVANCED_CAPABILITIES,
    ALLOWED_DATABASE_BACKENDS,
    CONSUMED_EVENTS,
    DESCRIPTION,
    EMITTED_EVENTS,
    LOGICAL_TABLES,
    PBC_KEY,
    PERMISSIONS,
    RUNTIME_CAPABILITIES,
    STANDARD_FEATURES,
    UI_FRAGMENTS,
    VERSION,
    WORKBENCH_VIEWS,
)
from .domain_depth import DOMAIN_OPERATIONS

PBC_MANIFEST = {
    # Source-audit trace key: 'data_product_catalog'
    "pbc": PBC_KEY,
    "label": "Data Product Catalog",
    "mesh": "platform",
    "description": DESCRIPTION,
    "version": VERSION,
    "datastore_backend": ALLOWED_DATABASE_BACKENDS[0],
    "tables": LOGICAL_TABLES,
    "apis": tuple(
        spec["route"]["method"] + " " + spec["route"]["path"]
        for spec in (
            {"route": {"method": "POST", "path": "/data-products"}},
            {"route": {"method": "POST", "path": "/data-contracts"}},
            {"route": {"method": "POST", "path": "/quality-signals"}},
            {"route": {"method": "POST", "path": "/access-requests"}},
            {"route": {"method": "GET", "path": "/data-product-catalog-workbench"}},
        )
    ),
    "operations": DOMAIN_OPERATIONS,
    "emits": EMITTED_EVENTS,
    "consumes": CONSUMED_EVENTS,
    "template": None,
    "ui_fragments": UI_FRAGMENTS,
    "workbench_views": WORKBENCH_VIEWS,
    "permissions": PERMISSIONS,
    "configuration": (
        "DATA_PRODUCT_CATALOG_DATABASE_URL",
        "DATA_PRODUCT_CATALOG_EVENT_TOPIC",
        "DATA_PRODUCT_CATALOG_RETRY_LIMIT",
        "DATA_PRODUCT_CATALOG_DEFAULT_POLICY",
    ),
    "migrations": ("migrations/001_initial.sql",),
    "seed_data": ("seed_data.py",),
    "tests": ("tests/test_contract.py",),
    "docs": (
        "README.md",
        "SPECIFICATION.md",
        "implementation-plan.md",
        "implementation-status.md",
        "RELEASE_EVIDENCE.md",
    ),
    "capabilities": STANDARD_FEATURES + RUNTIME_CAPABILITIES,
    "standard_features": STANDARD_FEATURES,
    "advanced_capabilities": RUNTIME_CAPABILITIES,
    "domain_advanced_capabilities": ADVANCED_CAPABILITIES,
    "workflows": (
        "data_product_onboarding",
        "contract_publication",
        "access_review",
        "certification_readiness",
        "incident_response",
        "change_impact_analysis",
    ),
    "analytics": (
        "catalog_adoption_score",
        "quality_drift_signal",
        "contract_change_impact",
        "policy_access_recommendation",
    ),
}
