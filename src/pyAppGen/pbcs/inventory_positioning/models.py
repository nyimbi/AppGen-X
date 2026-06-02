"""Owned model metadata for the inventory_positioning PBC."""

from __future__ import annotations

from .schema_contract import SCHEMA_CONTRACT
from .schema_contract import build_schema_contract


PBC_KEY = "inventory_positioning"
OWNED_SCHEMA = build_schema_contract()
MODEL_REGISTRY = tuple(
    {
        "class_name": model["class_name"],
        "table": model["table"],
        "fields": tuple(model["fields"]),
    }
    for model in OWNED_SCHEMA["models"]
)


def model_manifest() -> dict:
    return {
        "ok": OWNED_SCHEMA["ok"] and bool(MODEL_REGISTRY),
        "pbc": PBC_KEY,
        "owned_schema": OWNED_SCHEMA,
        "models": MODEL_REGISTRY,
        "side_effects": (),
    }


def smoke_test() -> dict:
    manifest = model_manifest()
    return {
        "ok": manifest["ok"]
        and len(manifest["models"]) == len(OWNED_SCHEMA["owned_tables"])
        and all(model["table"].startswith(PBC_KEY + "_") for model in manifest["models"]),
        "manifest": manifest,
        "side_effects": (),
    }
