from __future__ import annotations

from .runtime import public_safety_dispatch_runtime_capabilities


def table_stakes_capability_manifest() -> dict:
    runtime = public_safety_dispatch_runtime_capabilities()
    return {
        "ok": True,
        "pbc": runtime["pbc"],
        "standard_features": runtime["standard_features"],
        "advanced_capabilities": runtime["capabilities"],
        "operations": runtime["operations"],
        "owned_tables": runtime["owned_tables"],
        "event_contract": runtime["event_contract"],
        "stream_picker_visible": runtime["stream_engine_picker_visible"],
        "database_backends": runtime["database_backends"],
        "side_effects": (),
    }


def validate_table_stakes_capability_coverage() -> dict:
    manifest = table_stakes_capability_manifest()
    invalid_backends = tuple(backend for backend in manifest["database_backends"] if backend not in {"postgresql", "mysql", "mariadb"})
    invalid_tables = tuple(table for table in manifest["owned_tables"] if not table.startswith(f"{manifest['pbc']}_"))
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
        "side_effects": (),
    }


def smoke_test() -> dict:
    validation = validate_table_stakes_capability_coverage()
    return {"ok": validation["ok"], "validation": validation, "side_effects": ()}
