from __future__ import annotations

from .runtime import capital_projects_delivery_build_schema_contract


def model_contracts():
    return capital_projects_delivery_build_schema_contract()["models"]


def database_backed_model_manifest():
    models = model_contracts()
    return {
        "ok": True,
        "models": models,
        "database_backed": all(model["database_backed"] for model in models),
        "side_effects": (),
    }
