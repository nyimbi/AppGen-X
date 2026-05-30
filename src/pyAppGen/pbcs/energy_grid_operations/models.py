"""Executable model metadata for the energy_grid_operations PBC."""

from __future__ import annotations

from .runtime import (
    ENERGY_GRID_OPERATIONS_OWNED_TABLES,
    PBC_KEY,
    energy_grid_operations_build_schema_contract,
)


def model_manifest() -> dict:
    schema = energy_grid_operations_build_schema_contract()
    return {
        "ok": schema["ok"],
        "pbc": PBC_KEY,
        "models": schema["models"],
        "table_count": len(schema["tables"]),
        "owned_tables": ENERGY_GRID_OPERATIONS_OWNED_TABLES,
        "side_effects": (),
    }


def database_model_contract() -> dict:
    schema = energy_grid_operations_build_schema_contract()
    return {
        "format": "appgen.energy-grid-operations-database-model-contract.v2",
        "ok": schema["ok"],
        "pbc": PBC_KEY,
        "tables": schema["tables"],
        "models": schema["models"],
        "shared_table_access": False,
        "side_effects": (),
    }


def standalone_model_contract() -> dict:
    schema = energy_grid_operations_build_schema_contract()
    return {
        "format": "appgen.energy-grid-operations-standalone-model-contract.v2",
        "ok": schema["ok"],
        "pbc": PBC_KEY,
        "storage": "in_memory_owned_state",
        "tables": tuple(item["table"] for item in schema["tables"]),
        "event_tables": tuple(table for table in ENERGY_GRID_OPERATIONS_OWNED_TABLES if table.endswith("event")),
        "side_effects": (),
    }


def model_contracts() -> tuple[dict, ...]:
    return database_model_contract()["models"]


def smoke_test() -> dict:
    manifest = model_manifest()
    standalone = standalone_model_contract()
    return {
        "ok": manifest["ok"] and standalone["ok"] and len(manifest["models"]) >= 10,
        "manifest": manifest,
        "standalone": standalone,
        "side_effects": (),
    }
