"""Model contracts for the environment_health_safety PBC."""

from .standalone import build_schema_contract


def model_contracts():
    return build_schema_contract()["models"]
