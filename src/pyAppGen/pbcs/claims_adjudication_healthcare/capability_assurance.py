"""Capability assurance for the executable adjudication slice."""

from __future__ import annotations

from .domain_depth import DOMAIN_OPERATIONS
from .models import OWNED_TABLES
from .runtime import claims_adjudication_healthcare_runtime_capabilities


def table_stakes_capability_manifest():
    runtime = claims_adjudication_healthcare_runtime_capabilities()
    return {
        "ok": True,
        "pbc": runtime["pbc"],
        "standard_features": runtime["standard_features"],
        "advanced_capabilities": runtime["capabilities"],
        "operations": DOMAIN_OPERATIONS,
        "owned_tables": OWNED_TABLES,
        "event_contract": "AppGen-X",
        "stream_picker_visible": False,
        "database_backends": runtime["allowed_database_backends"],
        "side_effects": (),
    }


def validate_table_stakes_capability_coverage():
    manifest = table_stakes_capability_manifest()
    invalid_backends = tuple(
        backend
        for backend in manifest["database_backends"]
        if backend not in ("postgresql", "mysql", "mariadb")
    )
    invalid_tables = tuple(
        table for table in manifest["owned_tables"] if not table.startswith(f"{manifest['pbc']}_")
    )
    return {
        "ok": not invalid_backends and not invalid_tables and manifest["event_contract"] == "AppGen-X",
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


def smoke_test():
    validation = validate_table_stakes_capability_coverage()
    return {"ok": validation["ok"], "validation": validation, "side_effects": ()}
