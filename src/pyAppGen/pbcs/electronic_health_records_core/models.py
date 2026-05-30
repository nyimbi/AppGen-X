"""Model contracts for electronic health records core."""
from __future__ import annotations

from .runtime import electronic_health_records_core_build_schema_contract


def model_contracts():
    return electronic_health_records_core_build_schema_contract()["models"]
