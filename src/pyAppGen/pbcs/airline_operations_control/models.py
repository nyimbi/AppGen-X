"""Model metadata helpers for airline_operations_control."""

from __future__ import annotations

from .runtime import airline_operations_control_build_schema_contract


def model_contracts():
    return airline_operations_control_build_schema_contract()["models"]


def model_manifest() -> dict:
    models = model_contracts()
    return {
        "ok": bool(models),
        "pbc": "airline_operations_control",
        "models": models,
        "model_names": tuple(model["class_name"] for model in models),
        "side_effects": (),
    }
