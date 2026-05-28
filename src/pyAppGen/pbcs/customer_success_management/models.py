"""Owned model metadata for the customer_success_management PBC."""
from __future__ import annotations

from .slice_app import PBC_KEY, build_models_contract, build_schema_contract

MODELS = build_models_contract()["models"]
OWNED_SCHEMA = {
    "schema": PBC_KEY,
    "table_prefix": f"{PBC_KEY}_",
    "tables": build_schema_contract()["tables"],
}


def model_manifest() -> dict:
    return {"ok": True, "pbc": PBC_KEY, "models": MODELS, "side_effects": ()}


def build_owned_schema() -> dict:
    return {"ok": True, "pbc": PBC_KEY, **OWNED_SCHEMA, "side_effects": ()}


def smoke_test() -> dict:
    manifest = model_manifest()
    schema = build_owned_schema()
    return {
        "ok": manifest["ok"] and schema["ok"] and len(manifest["models"]) >= 20,
        "manifest": manifest,
        "schema": schema,
        "side_effects": (),
    }
