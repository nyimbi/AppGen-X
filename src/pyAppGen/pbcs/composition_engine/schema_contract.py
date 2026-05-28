"""Owned schema evidence for the composition_engine PBC."""

from __future__ import annotations

from .runtime import composition_engine_build_schema_contract


SCHEMA_CONTRACT = {
    **composition_engine_build_schema_contract(),
    "pbc": "composition_engine",
}


def build_schema_contract() -> dict:
    """Return owned schema and runtime-table evidence."""
    return dict(SCHEMA_CONTRACT)


def validate_schema_contract() -> dict:
    """Validate schema shape, ownership, and eventing constraints."""
    contract = build_schema_contract()
    invalid_runtime_tables = tuple(
        item["table"] for item in contract["runtime_tables"] if not item["table"].startswith("composition_engine_")
    )
    return {
        "ok": contract["ok"]
        and bool(contract["tables"])
        and bool(contract["models"])
        and contract["required_event_topic"] == "appgen.composition.events"
        and contract["shared_table_access"] is False
        and not invalid_runtime_tables,
        "pbc": "composition_engine",
        "contract": contract,
        "invalid_runtime_tables": invalid_runtime_tables,
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Exercise schema evidence readiness side-effect-free."""
    validation = validate_schema_contract()
    return {
        "ok": validation["ok"],
        "validation": validation,
        "side_effects": (),
    }
