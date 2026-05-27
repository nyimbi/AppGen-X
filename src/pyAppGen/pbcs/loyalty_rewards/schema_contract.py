"""Generated owned schema evidence for the loyalty_rewards PBC."""

from __future__ import annotations

from .runtime import LOYALTY_REWARDS_ALLOWED_DATABASE_BACKENDS
from .runtime import LOYALTY_REWARDS_OWNED_TABLES
from .runtime import LOYALTY_REWARDS_RUNTIME_TABLES
from .runtime import loyalty_rewards_build_schema_contract


PBC_KEY = "loyalty_rewards"


def _owned_table_name(table: str) -> str:
    return table if table.startswith(f"{PBC_KEY}_") else f"{PBC_KEY}_{table}"


def _class_name(table: str) -> str:
    logical = table.removeprefix(f"{PBC_KEY}_")
    return "".join(part.capitalize() for part in logical.split("_"))


def _field_descriptor(name: str) -> dict:
    return {
        "name": name,
        "type": "decimal" if name in {"balance", "liability_amount", "monetary_value"} else "string",
        "required": name not in {"source_ref"},
        "primary_key": name.endswith("_id") and name not in {"account_id"},
        "nullable": name in {"source_ref"},
    }


def _relationship_descriptor(relationship: dict) -> dict:
    return {
        "field": relationship["from_field"],
        "source_table": _owned_table_name(relationship["from_table"]),
        "target_table": _owned_table_name(relationship["to_table"]),
        "target_column": relationship["to_field"],
        "cardinality": relationship["type"],
        "ownership": "same_pbc",
    }


def build_schema_contract() -> dict:
    """Return generated owned schema, migration, model, and runtime-table evidence."""
    runtime = loyalty_rewards_build_schema_contract()
    tables = tuple(
        {
            "logical_table": table["table"],
            "owned_table": _owned_table_name(table["table"]),
            "fields": tuple(_field_descriptor(field) for field in table["fields"]),
            "relationships": tuple(
                _relationship_descriptor(relationship)
                for relationship in runtime["relationships"]
                if relationship["from_table"] == table["table"]
            ),
        }
        for table in runtime["tables"]
    )
    runtime_tables = tuple(
        {
            "logical_table": table["table"],
            "owned_table": table["table"],
            "fields": tuple(_field_descriptor(field) for field in table["fields"]),
            "relationships": (),
            "event_contract": "AppGen-X",
        }
        for table in runtime["runtime_tables"]
    )
    relationships = tuple(relationship for table in tables for relationship in table["relationships"])
    return {
        "format": "appgen.loyalty-rewards-owned-schema-contract.v1",
        "ok": runtime["ok"] is True and tuple(item["logical_table"] for item in tables) == LOYALTY_REWARDS_OWNED_TABLES,
        "pbc": PBC_KEY,
        "owned_tables": tuple(table["owned_table"] for table in tables),
        "runtime_tables": tuple(table["owned_table"] for table in runtime_tables),
        "tables": tables,
        "runtime_table_descriptors": runtime_tables,
        "relationships": relationships,
        "migrations": tuple(item["path"] for item in runtime["migrations"]),
        "models": tuple(
            {
                "class_name": f"LoyaltyRewards{_class_name(table['logical_table'])}",
                "table": table["owned_table"],
                "fields": table["fields"],
                "relationships": table["relationships"],
            }
            for table in tables
        ),
        "generated_artifacts": runtime["generated_artifacts"],
        "database_backends": LOYALTY_REWARDS_ALLOWED_DATABASE_BACKENDS,
        "datastore_backends": LOYALTY_REWARDS_ALLOWED_DATABASE_BACKENDS,
        "shared_table_access": False,
        "tenant_isolation": {"field": "tenant", "required": True},
        "declared_dependencies": {
            "apis": ("payment_projection", "promotion_projection", "customer_segment_projection"),
            "events": ("PaymentCaptured", "PromotionApplied"),
            "api_projections": ("payment_projection", "promotion_projection", "customer_segment_projection"),
            "shared_tables": (),
        },
    }


SCHEMA_CONTRACT = build_schema_contract()


def validate_schema_contract() -> dict:
    """Validate owned table, migration, model, and datastore evidence."""
    contract = build_schema_contract()
    owned_tables = tuple(contract.get("owned_tables", ()))
    runtime_tables = tuple(contract.get("runtime_tables", ()))
    model_tables = tuple(model["table"] for model in contract.get("models", ()))
    migration_paths = tuple(contract.get("migrations", ()))
    allowed_backends = {"postgresql", "mysql", "mariadb"}
    invalid_tables = tuple(table for table in owned_tables + runtime_tables if not table.startswith(f"{PBC_KEY}_"))
    missing_models = tuple(table for table in owned_tables if table not in model_tables)
    invalid_relationships = tuple(
        relationship for relationship in contract.get("relationships", ()) if not relationship["target_table"].startswith(f"{PBC_KEY}_")
    )
    invalid_backends = tuple(backend for backend in contract.get("database_backends", ()) if backend not in allowed_backends)
    return {
        "ok": contract.get("ok") is True
        and bool(owned_tables)
        and set(LOYALTY_REWARDS_RUNTIME_TABLES) <= set(runtime_tables)
        and len(migration_paths) == len(LOYALTY_REWARDS_OWNED_TABLES)
        and not invalid_tables
        and not missing_models
        and not invalid_relationships
        and not invalid_backends
        and contract.get("shared_table_access") is False,
        "pbc": PBC_KEY,
        "owned_tables": owned_tables,
        "runtime_tables": runtime_tables,
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
