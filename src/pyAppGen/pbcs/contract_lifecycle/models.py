"""Owned model metadata for the contract_lifecycle PBC."""

from .application import MODELS, PBC_KEY, owned_table_contracts, schema_contract

OWNED_SCHEMA = {
    "schema": PBC_KEY,
    "table_prefix": f"{PBC_KEY}_",
    "tables": owned_table_contracts(),
}


def model_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "schema": OWNED_SCHEMA,
        "models": MODELS,
        "owned_tables": tuple(item["owned_table"] for item in OWNED_SCHEMA["tables"]),
    }


def validate_models() -> dict:
    manifest = model_manifest()
    invalid = tuple(model for model in manifest["models"] if not model["table"].startswith(f"{PBC_KEY}_"))
    return {"ok": manifest["ok"] and not invalid, "invalid_models": invalid, "manifest": manifest}


def smoke_test() -> dict:
    contract = schema_contract()
    validation = validate_models()
    return {
        "ok": contract["ok"] and validation["ok"] and len(contract["tables"]) == len(MODELS),
        "schema_contract": contract,
        "validation": validation,
    }
