"""Package manifest for the CDP Segmentation PBC."""

from __future__ import annotations

from .runtime import CDP_SEGMENTATION_CONSUMED_EVENT_TYPES
from .runtime import CDP_SEGMENTATION_EMITTED_EVENT_TYPES
from .runtime import CDP_SEGMENTATION_OWNED_TABLES
from .runtime import CDP_SEGMENTATION_RUNTIME_CAPABILITY_KEYS
from .runtime import CDP_SEGMENTATION_STANDARD_FEATURE_KEYS
from .runtime import cdp_segmentation_build_api_contract
from .runtime import cdp_segmentation_runtime_capabilities
from .ui import CDP_SEGMENTATION_UI_FRAGMENT_KEYS


PBC_KEY = 'cdp_segmentation'

PBC_MANIFEST = {
    "pbc": "cdp_segmentation",
    "label": "Customer Data Platform Segmentation",
    "mesh": "relationship",
    "description": (
        "Customer event ingestion, identity stitching, governed profiles, "
        "consent-aware real-time segmentation, activations, analytics, proofs, "
        "federation, controls, resilience, and AppGen-X event orchestration."
    ),
    "datastore_backend": "postgresql",
    "tables": CDP_SEGMENTATION_OWNED_TABLES,
    "apis": tuple(route["route"] for route in cdp_segmentation_build_api_contract()["routes"]),
    "emits": CDP_SEGMENTATION_EMITTED_EVENT_TYPES,
    "consumes": CDP_SEGMENTATION_CONSUMED_EVENT_TYPES,
    "template": "crm",
    "ui_fragments": CDP_SEGMENTATION_UI_FRAGMENT_KEYS,
    "permissions": tuple(sorted(cdp_segmentation_build_api_contract()["permissions"])),
    "configuration": (
        "CDP_SEGMENTATION_DATABASE_URL",
        "CDP_SEGMENTATION_EVENT_TOPIC",
        "CDP_SEGMENTATION_RETRY_LIMIT",
        "CDP_SEGMENTATION_DEFAULT_REGION",
        "CDP_SEGMENTATION_DEFAULT_TIMEZONE",
        "CDP_SEGMENTATION_ACTIVATION_MODE",
    ),
    "capabilities": tuple(f"cdp_segmentation.{table}" for table in CDP_SEGMENTATION_OWNED_TABLES),
    "standard_features": CDP_SEGMENTATION_STANDARD_FEATURE_KEYS,
    "workflows": cdp_segmentation_runtime_capabilities()["operations"],
    "analytics": (
        "segment_membership_rate",
        "activation_delivery_rate",
        "profile_merge_confidence",
        "lifecycle_risk",
        "consent_risk",
        "audience_forecast",
        "profile_anomaly_rate",
        "customer_segment_updated_throughput",
        "profile_enriched_throughput",
    ),
    "advanced_capabilities": CDP_SEGMENTATION_RUNTIME_CAPABILITY_KEYS,
    "migrations": ("migrations/001_initial.sql",),
    "seed_data": ("seed_data.py",),
    "tests": ("tests/test_contract.py", "tests/test_execution.py"),
    "docs": (
        "README.md",
        "implementation-plan.md",
        "implementation-status.md",
        "RELEASE_EVIDENCE.md",
        "SPECIFICATION.md",
    ),
}
