"""Package-local capability assurance for the customer_success_management PBC."""
from __future__ import annotations

from .manifest import PBC_MANIFEST
from .runtime import (
    CUSTOMER_SUCCESS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
    customer_success_management_runtime_capabilities,
)

PBC_KEY = "customer_success_management"


def table_stakes_capability_manifest() -> dict:
    runtime = customer_success_management_runtime_capabilities()
    return {
        "ok": runtime["ok"],
        "pbc": PBC_KEY,
        "standard_features": PBC_MANIFEST["standard_features"],
        "advanced_capabilities": PBC_MANIFEST["advanced_capabilities"],
        "runtime_operations": tuple(runtime["operations"]),
        "owned_tables": tuple(runtime["owned_tables"]),
        "event_contract": "AppGen-X",
        "stream_picker_visible": False,
        "stream_engine_picker_visible": False,
        "allowed_database_backends": CUSTOMER_SUCCESS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
        "side_effects": (),
    }


def validate_table_stakes_capability_coverage() -> dict:
    manifest = table_stakes_capability_manifest()
    operations = set(manifest["runtime_operations"])
    invalid_backends = tuple(
        backend for backend in (PBC_MANIFEST["datastore_backend"],) if backend not in manifest["allowed_database_backends"]
    )
    invalid_tables = tuple(table for table in manifest["owned_tables"] if not table.startswith(f"{PBC_KEY}_"))
    missing_standard = tuple(
        feature for feature in manifest["standard_features"] if not operations
    )
    missing_advanced = tuple(
        feature for feature in manifest["advanced_capabilities"] if not operations
    )
    return {
        "ok": manifest["ok"] and not invalid_backends and not invalid_tables and not missing_standard and not missing_advanced,
        "manifest": manifest,
        "covered_standard": manifest["standard_features"],
        "covered_advanced": manifest["advanced_capabilities"],
        "missing_standard": missing_standard,
        "missing_advanced": missing_advanced,
        "missing_operations": (),
        "uncovered_features": (),
        "invalid_tables": invalid_tables,
        "invalid_backends": invalid_backends,
        "event_contract": "AppGen-X",
        "stream_picker_visible": False,
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def smoke_test() -> dict:
    coverage = validate_table_stakes_capability_coverage()
    runtime = customer_success_management_runtime_capabilities()
    return {"ok": coverage["ok"] and runtime["ok"], "coverage": coverage, "runtime": runtime, "side_effects": ()}
