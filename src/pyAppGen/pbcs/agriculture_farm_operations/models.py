"""Model and schema helpers for the agriculture_farm_operations standalone slice."""

from __future__ import annotations

from .runtime import agriculture_farm_operations_build_schema_contract


def model_contracts():
    return agriculture_farm_operations_build_schema_contract()["models"]


def standalone_model_contract() -> dict:
    schema = agriculture_farm_operations_build_schema_contract()
    models = schema["models"]
    field_model = next(item for item in models if item["table"] == "agriculture_farm_operations_field")
    crop_plan_model = next(item for item in models if item["table"] == "agriculture_farm_operations_crop_plan")
    return {
        "ok": schema["ok"],
        "pbc": "agriculture_farm_operations",
        "entities": (field_model, crop_plan_model),
        "all_models": models,
        "side_effects": (),
    }


def smoke_test() -> dict:
    contract = standalone_model_contract()
    return {
        "ok": contract["ok"] and len(contract["entities"]) == 2 and bool(contract["all_models"]),
        "contract": contract,
        "side_effects": (),
    }
