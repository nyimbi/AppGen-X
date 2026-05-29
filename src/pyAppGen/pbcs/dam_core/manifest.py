"""Package manifest for the dam_core PBC."""

from __future__ import annotations

from .runtime import DAM_CORE_CONSUMED_EVENT_TYPES
from .runtime import DAM_CORE_EMITTED_EVENT_TYPES
from .runtime import DAM_CORE_OWNED_TABLES
from .runtime import DAM_CORE_STANDARD_FEATURE_KEYS
from .runtime import dam_core_build_api_contract
from .runtime import dam_core_permissions_contract
from .runtime import dam_core_runtime_capabilities


def _declared_capabilities() -> tuple[str, ...]:
    priority_tables = (
        "asset",
        "asset_rendition",
        "rights_policy",
        "metadata_tag",
        "asset_collection",
        "license_agreement",
        "usage_entitlement",
        "metadata_taxonomy",
        "asset_workflow_case",
        "asset_exception",
        "asset_usage_snapshot",
        "asset_lineage",
    )
    return tuple(f"dam_core.{table}" for table in priority_tables)


_RUNTIME_CAPABILITIES = dam_core_runtime_capabilities()
_API_CONTRACT = dam_core_build_api_contract()

PBC_MANIFEST = {
    # Source-audit trace key: 'dam_core'
    "pbc": "dam_core",
    "label": "Digital Asset Management Core",
    "mesh": "content",
    "description": "Standalone DAM package for asset lifecycle, rendition orchestration, metadata governance, rights, and workbench operations.",
    "datastore_backend": "postgresql",
    "tables": DAM_CORE_OWNED_TABLES,
    "apis": _API_CONTRACT["declared_catalog_routes"],
    "emits": DAM_CORE_EMITTED_EVENT_TYPES,
    "consumes": DAM_CORE_CONSUMED_EVENT_TYPES,
    "template": "standalone_one_pbc_app",
    "ui_fragments": (
        "DamCoreWorkbench",
        "DamCoreAssetWorkbench",
        "DamCoreRightsWorkbench",
        "DamCoreOperationsWorkbench",
    ),
    "permissions": tuple(sorted(set(dam_core_permissions_contract().values()))),
    "configuration": (
        "database_backend",
        "event_topic",
        "retry_limit",
        "default_storage_tier",
        "allowed_mime_types",
        "rendition_profiles",
        "rights_default_decision",
        "metadata_taxonomies",
        "default_locale",
        "workbench_limit",
    ),
    "capabilities": _declared_capabilities(),
    "standard_features": DAM_CORE_STANDARD_FEATURE_KEYS,
    "workflows": tuple(
        operation
        for operation in _RUNTIME_CAPABILITIES["operations"]
        if operation
        and not operation.startswith("build_")
        and operation not in {"permissions_contract", "verify_owned_table_boundary"}
    ),
    "analytics": (
        "asset_readiness",
        "rendition_pipeline_latency",
        "rights_risk_exposure",
        "metadata_quality",
        "duplicate_review_backlog",
        "workflow_clearance_rate",
    ),
    "advanced_capabilities": _RUNTIME_CAPABILITIES["capabilities"],
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
}
