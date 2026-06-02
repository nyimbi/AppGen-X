from __future__ import annotations

from .standalone import build_schema_contract


def model_contracts():
    return build_schema_contract()["models"]
