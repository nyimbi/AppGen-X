"""Owned model metadata for the clinical_trials_management PBC."""

from __future__ import annotations

from .runtime import clinical_trials_management_build_schema_contract


def model_contracts():
    """Return owned model contracts derived from the package schema contract."""
    return clinical_trials_management_build_schema_contract()["models"]


def model_catalog() -> dict:
    """Return a keyed lookup of clinical-trials-owned models."""
    models = tuple(model_contracts())
    return {
        "ok": bool(models),
        "pbc": "clinical_trials_management",
        "models": models,
        "by_table": {model["table"]: model for model in models},
        "by_class_name": {model["class_name"]: model for model in models},
        "side_effects": (),
    }
