"""Owned schema evidence for the standalone master_data_governance slice."""
from __future__ import annotations

from .standalone import TABLE_SPECS
from .standalone import standalone_model_contract

PBC_KEY = "master_data_governance"



def build_schema_contract():
    model_contract = standalone_model_contract()
    tables = tuple(
        {
            "logical_table": spec.table.removeprefix(f"{PBC_KEY}_"),
            "owned_table": spec.table,
            "category": spec.category,
            "description": spec.description,
            "fields": next(item["fields"] for item in model_contract["tables"] if item["table"] == spec.table),
            "relationships": (),
        }
        for spec in TABLE_SPECS
    )
    models = tuple(
        {
            "class_name": "".join(part.capitalize() for part in spec.table.split("_")),
            "table": spec.table,
            "fields": next(item["fields"] for item in model_contract["tables"] if item["table"] == spec.table),
            "relationships": (),
        }
        for spec in TABLE_SPECS
    )
    return {
        "format": "appgen.master-data-governance-owned-schema-contract.v1",
        "ok": model_contract["ok"],
        "pbc": PBC_KEY,
        "tables": tables,
        "models": models,
        "owned_tables": model_contract["table_keys"],
        "migrations": ("migrations/001_initial.sql",),
        "database_backends": ("postgresql", "mysql", "mariadb", "sqlite"),
        "shared_table_access": False,
        "side_effects": (),
    }



def master_data_governance_build_schema_contract():
    return build_schema_contract()



def validate_schema_contract():
    contract = build_schema_contract()
    invalid_tables = tuple(item["owned_table"] for item in contract["tables"] if not item["owned_table"].startswith(f"{PBC_KEY}_"))
    return {"ok": contract["ok"] and not invalid_tables and bool(contract["models"]), "contract": contract, "invalid_tables": invalid_tables, "side_effects": ()}



def smoke_test():
    return validate_schema_contract()
