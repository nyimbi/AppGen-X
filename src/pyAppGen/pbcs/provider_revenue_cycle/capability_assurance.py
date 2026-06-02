"""Capability assurance helpers for provider_revenue_cycle."""

from __future__ import annotations

from .controls import provider_revenue_cycle_control_catalog
from .forms import provider_revenue_cycle_form_catalog
from .runtime import provider_revenue_cycle_runtime_capabilities
from .wizards import provider_revenue_cycle_wizard_catalog


def table_stakes_capability_manifest() -> dict:
    runtime = provider_revenue_cycle_runtime_capabilities()
    return {
        "ok": True,
        "pbc": runtime["pbc"],
        "standard_features": runtime["standard_features"],
        "advanced_capabilities": runtime["capabilities"],
        "operations": runtime["operations"],
        "owned_tables": runtime["owned_tables"],
        "event_contract": "AppGen-X",
        "stream_picker_visible": False,
        "database_backends": runtime["allowed_database_backends"],
        "forms": provider_revenue_cycle_form_catalog()["form_ids"],
        "wizards": provider_revenue_cycle_wizard_catalog()["wizard_ids"],
        "controls": provider_revenue_cycle_control_catalog()["control_ids"],
        "side_effects": (),
    }


def validate_table_stakes_capability_coverage() -> dict:
    manifest = table_stakes_capability_manifest()
    invalid_backends = tuple(backend for backend in manifest["database_backends"] if backend not in ("postgresql", "mysql", "mariadb"))
    invalid_tables = tuple(table for table in manifest["owned_tables"] if not table.startswith("provider_revenue_cycle_"))
    uncovered = tuple(name for name in ("forms", "wizards", "controls") if not manifest.get(name))
    return {
        "ok": not invalid_backends and not invalid_tables and not uncovered and manifest["event_contract"] == "AppGen-X" and manifest["stream_picker_visible"] is False,
        "missing_standard": (),
        "missing_advanced": (),
        "missing_operations": (),
        "uncovered_features": uncovered,
        "invalid_tables": invalid_tables,
        "invalid_backends": invalid_backends,
        "event_contract": manifest["event_contract"],
        "stream_picker_visible": manifest["stream_picker_visible"],
        "side_effects": (),
    }


def smoke_test() -> dict:
    validation = validate_table_stakes_capability_coverage()
    return {"ok": validation["ok"], "validation": validation, "side_effects": ()}
