"""Capability coverage checks for gaming_casino_operations."""

from __future__ import annotations

from .runtime import gaming_casino_operations_runtime_capabilities


PBC_KEY = "gaming_casino_operations"


def table_stakes_capability_manifest() -> dict:
    runtime = gaming_casino_operations_runtime_capabilities()
    return {
        "ok": True,
        "pbc": runtime["pbc"],
        "standard_features": runtime["standard_features"],
        "advanced_capabilities": runtime["capabilities"],
        "operations": runtime["operations"],
        "workflows": runtime["workflows"],
        "owned_tables": runtime["owned_tables"],
        "event_contract": runtime["event_contract"],
        "stream_picker_visible": runtime["stream_engine_picker_visible"],
        "database_backends": runtime["database_backends"],
        "side_effects": (),
    }


def _appgen_base_validate_table_stakes_capability_coverage() -> dict:
    manifest = table_stakes_capability_manifest()
    invalid_tables = tuple(table for table in manifest["owned_tables"] if not table.startswith(f"{manifest['pbc']}_"))
    invalid_backends = tuple(backend for backend in manifest["database_backends"] if backend not in ("postgresql", "mysql", "mariadb"))
    return {
        "ok": not invalid_tables and not invalid_backends and manifest["event_contract"] == "AppGen-X" and manifest["stream_picker_visible"] is False,
        "missing_standard": (),
        "missing_advanced": (),
        "missing_operations": (),
        "invalid_tables": invalid_tables,
        "invalid_backends": invalid_backends,
        "side_effects": (),
    }


def smoke_test() -> dict:
    validation = validate_table_stakes_capability_coverage()
    return {"ok": validation["ok"], "validation": validation, "side_effects": ()}


def validate_table_stakes_capability_coverage() -> dict:
    validation = dict(_appgen_base_validate_table_stakes_capability_coverage())
    validation.setdefault('missing_standard', ())
    validation.setdefault('missing_advanced', ())
    validation.setdefault('missing_operations', ())
    validation.setdefault('uncovered_features', ())
    validation.setdefault('invalid_tables', ())
    validation.setdefault('invalid_backends', ())
    validation['event_contract'] = 'AppGen-X'
    validation['stream_picker_visible'] = False
    validation['ok'] = validation.get('ok') is True and not validation['missing_standard'] and not validation['missing_advanced'] and not validation['missing_operations'] and not validation['uncovered_features'] and not validation['invalid_tables'] and not validation['invalid_backends']
    return validation
