"""Generated owned schema evidence for the cdp_segmentation PBC."""

from __future__ import annotations

from .runtime import CDP_SEGMENTATION_ALLOWED_DATABASE_BACKENDS
from .runtime import CDP_SEGMENTATION_OWNED_TABLES
from .runtime import CDP_SEGMENTATION_RUNTIME_TABLES
from .runtime import cdp_segmentation_build_schema_contract


PBC_KEY = "cdp_segmentation"


def _owned_table_name(table: str) -> str:
    return table if table.startswith(f"{PBC_KEY}_") else f"{PBC_KEY}_{table}"


def _class_name(table: str) -> str:
    logical = table.removeprefix(f"{PBC_KEY}_")
    return "".join(part.capitalize() for part in logical.split("_"))


def _field_descriptor(field: dict) -> dict:
    return {
        "name": field["name"],
        "type": field.get("type", "text"),
        "required": bool(field.get("required", False)),
        "primary_key": field["name"] == "id",
        "nullable": not bool(field.get("required", False)),
    }


def _relationship_descriptor(source_table: str, relationship: dict) -> dict:
    target = relationship.get("to")
    if target == "AppGen-X":
        return {
            "field": "event_contract",
            "source_table": _owned_table_name(source_table),
            "target_table": "AppGen-X",
            "target_column": "event_contract",
            "cardinality": "event-contract",
            "ownership": "appgen_event_contract",
        }
    return {
        "field": relationship.get("on", "record_id"),
        "source_table": _owned_table_name(source_table),
        "target_table": _owned_table_name(str(target)),
        "target_column": relationship.get("on", "record_id"),
        "cardinality": relationship.get("type", "owned_reference"),
        "ownership": "same_pbc",
    }


def build_schema_contract() -> dict:
    """Return generated owned schema, migration, and model evidence."""
    runtime = cdp_segmentation_build_schema_contract()
    tables = tuple(
        {
            "logical_table": table["table"],
            "owned_table": _owned_table_name(table["table"]),
            "fields": tuple(_field_descriptor(field) for field in table["fields"]),
            "relationships": tuple(
                _relationship_descriptor(table["table"], relationship)
                for relationship in table.get("relationships", ())
            ),
        }
        for table in runtime["tables"]
    )
    relationships = tuple(
        relationship
        for table in tables
        for relationship in table["relationships"]
        if relationship["ownership"] == "same_pbc"
    )
    return {
        "format": "appgen.cdp-segmentation-owned-schema-contract.v1",
        "ok": runtime["ok"] is True and len(tables) == len(CDP_SEGMENTATION_OWNED_TABLES),
        "pbc": PBC_KEY,
        "owned_tables": tuple(table["owned_table"] for table in tables),
        "runtime_tables": CDP_SEGMENTATION_RUNTIME_TABLES,
        "tables": tables,
        "relationships": relationships,
        "migrations": tuple(runtime["migrations"]),
        "models": tuple(
            {
                "class_name": f"CdpSegmentation{_class_name(table['logical_table'])}",
                "table": table["owned_table"],
                "fields": table["fields"],
                "relationships": table["relationships"],
            }
            for table in tables
        ),
        "database_backends": CDP_SEGMENTATION_ALLOWED_DATABASE_BACKENDS,
        "shared_table_access": False,
        "tenant_isolation": runtime["tenant_isolation"],
        "schema_extensions": runtime["schema_extensions"],
        "declared_dependencies": runtime["declared_dependencies"],
    }


SCHEMA_CONTRACT = build_schema_contract()


def validate_schema_contract() -> dict:
    """Validate owned table, migration, model, and datastore evidence."""
    contract = build_schema_contract()
    owned_tables = tuple(contract.get("owned_tables", ()))
    model_tables = tuple(model["table"] for model in contract.get("models", ()))
    migration_paths = tuple(contract.get("migrations", ()))
    allowed_backends = {"postgresql", "mysql", "mariadb"}
    invalid_tables = tuple(table for table in owned_tables if not table.startswith(f"{PBC_KEY}_"))
    missing_models = tuple(table for table in owned_tables if table not in model_tables)
    invalid_relationships = tuple(
        relationship
        for relationship in contract.get("relationships", ())
        if not relationship["target_table"].startswith(f"{PBC_KEY}_")
    )
    invalid_backends = tuple(
        backend for backend in contract.get("database_backends", ()) if backend not in allowed_backends
    )
    return {
        "ok": contract.get("ok") is True
        and len(owned_tables) >= 45
        and set(CDP_SEGMENTATION_RUNTIME_TABLES) <= set(owned_tables)
        and len(migration_paths) == len(CDP_SEGMENTATION_OWNED_TABLES)
        and not invalid_tables
        and not missing_models
        and not invalid_relationships
        and not invalid_backends
        and contract.get("shared_table_access") is False,
        "pbc": PBC_KEY,
        "owned_tables": owned_tables,
        "model_tables": model_tables,
        "migration_paths": migration_paths,
        "invalid_tables": invalid_tables,
        "missing_models": missing_models,
        "invalid_relationships": invalid_relationships,
        "invalid_backends": invalid_backends,
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Exercise schema validation side-effect-free."""
    return validate_schema_contract()
