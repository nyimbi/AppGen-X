"""Owned schema contract for the insurance_claims_policy PBC."""

from __future__ import annotations

from .config import ALLOWED_DATABASE_BACKENDS
from .models import MODELS
from .models import OWNED_SCHEMA
from .models import OWNED_TABLES

PBC_KEY = "insurance_claims_policy"


def build_schema_contract() -> dict:
    table_contracts = tuple(
        {
            "logical_table": model["logical_table"],
            "table": model["table"],
            "fields": tuple(field["name"] for field in model["fields"]),
            "field_contracts": model["fields"],
            "relationships": model["relationships"],
            "owned_by": PBC_KEY,
        }
        for model in MODELS
    )
    return {
        "format": "appgen.insurance-claims-policy-owned-schema-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "schema": OWNED_SCHEMA,
        "tables": table_contracts,
        "migrations": ({"path": "migrations/001_initial.sql", "operation": "create_owned_tables", "backend_allowlist": ALLOWED_DATABASE_BACKENDS},),
        "models": tuple({"class_name": model["class_name"], "table": model["table"], "fields": tuple(field["name"] for field in model["fields"])} for model in MODELS),
        "datastore_backends": ALLOWED_DATABASE_BACKENDS,
        "database_backends": ALLOWED_DATABASE_BACKENDS,
        "shared_table_access": False,
        "owned_tables": OWNED_TABLES,
        "side_effects": (),
    }


def insurance_claims_policy_build_schema_contract() -> dict:
    return build_schema_contract()


def validate_schema_contract() -> dict:
    contract = build_schema_contract()
    invalid_tables = tuple(table for table in contract["owned_tables"] if not table.startswith(f"{PBC_KEY}_"))
    return {
        "ok": contract["ok"] and len(contract["tables"]) == len(MODELS) and not invalid_tables,
        "contract": contract,
        "invalid_tables": invalid_tables,
        "side_effects": (),
    }


def smoke_test() -> dict:
    return validate_schema_contract()
