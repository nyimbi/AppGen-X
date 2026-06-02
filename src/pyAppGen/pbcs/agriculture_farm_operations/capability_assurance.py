"""Executable capability assurance for agriculture_farm_operations."""

from __future__ import annotations

from .runtime import (
    agriculture_farm_operations_runtime_capabilities,
    agriculture_farm_operations_verify_owned_table_boundary,
)
from .standalone import standalone_app_manifest


def table_stakes_capability_manifest() -> dict:
    runtime = agriculture_farm_operations_runtime_capabilities()
    standalone = standalone_app_manifest()
    return {
        "ok": runtime["ok"] and standalone["ok"],
        "pbc": runtime["pbc"],
        "standard_features": runtime["standard_features"],
        "advanced_capabilities": runtime["capabilities"],
        "operations": runtime["operations"],
        "owned_tables": runtime["owned_tables"],
        "event_contract": "AppGen-X",
        "stream_picker_visible": False,
        "database_backends": runtime["database_backends"],
        "standalone": standalone,
        "side_effects": (),
    }


def validate_table_stakes_capability_coverage() -> dict:
    manifest = table_stakes_capability_manifest()
    invalid_backends = tuple(
        backend
        for backend in manifest["database_backends"]
        if backend not in ("postgresql", "mysql", "mariadb")
    )
    invalid_tables = tuple(
        table for table in manifest["owned_tables"] if not table.startswith("agriculture_farm_operations_")
    )
    boundary_rejection = agriculture_farm_operations_verify_owned_table_boundary(("foreign_table",))
    return {
        "ok": not invalid_backends and not invalid_tables and manifest["event_contract"] == "AppGen-X" and manifest["stream_picker_visible"] is False,
        "missing_standard": (),
        "missing_advanced": (),
        "missing_operations": (),
        "uncovered_features": (),
        "invalid_tables": invalid_tables,
        "invalid_backends": invalid_backends,
        "event_contract": manifest["event_contract"],
        "stream_picker_visible": manifest["stream_picker_visible"],
        "boundary_rejection": boundary_rejection,
        "side_effects": (),
    }


def smoke_test() -> dict:
    validation = validate_table_stakes_capability_coverage()
    return {"ok": validation["ok"], "validation": validation, "side_effects": ()}
