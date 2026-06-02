"""Executable model contracts for the bank_payments_clearing PBC."""

from __future__ import annotations

from .schema_contract import build_schema_contract


PBC_KEY = "bank_payments_clearing"


def build_model_contracts() -> tuple[dict, ...]:
    schema = build_schema_contract()
    return tuple(
        {
            "class_name": model["class_name"],
            "table": model["table"],
            "fields": model["fields"],
            "module": "models.py",
            "owned_by": PBC_KEY,
            "shared_table_access": False,
        }
        for model in schema["models"]
    )


MODEL_CONTRACTS = build_model_contracts()


def instantiate_model(table: str, payload: dict | None = None) -> dict:
    payload = dict(payload or {})
    contract = next((item for item in MODEL_CONTRACTS if item["table"] == table), None)
    if contract is None:
        return {"ok": False, "reason": "unknown_table", "table": table, "side_effects": ()}
    record = {field: payload.get(field) for field in contract["fields"]}
    record["table"] = table
    return {"ok": True, "model": contract, "record": record, "side_effects": ()}


def model_manifest() -> dict:
    return {
        "ok": bool(MODEL_CONTRACTS),
        "pbc": PBC_KEY,
        "models": MODEL_CONTRACTS,
        "tables": tuple(contract["table"] for contract in MODEL_CONTRACTS),
        "side_effects": (),
    }


def database_model_contract() -> dict:
    schema = build_schema_contract()
    return {
        "ok": model_manifest()["ok"] and schema["ok"],
        "pbc": PBC_KEY,
        "models": MODEL_CONTRACTS,
        "shared_table_access": False,
        "database_backends": schema["database_backends"],
        "migration_files": tuple(item["path"] for item in schema["migrations"]),
        "side_effects": (),
    }


def smoke_test() -> dict:
    sample = instantiate_model(
        "bank_payments_clearing_payment_instruction",
        {"instruction_id": "pay_smoke", "state": "drafted"},
    )
    return {
        "ok": model_manifest()["ok"] and database_model_contract()["ok"] and sample["ok"],
        "sample": sample,
        "side_effects": (),
    }
