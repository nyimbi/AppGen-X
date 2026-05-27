"""Generated owned schema evidence for the schema_registry PBC."""

from .domain_schema import LOGICAL_TABLES
from .domain_schema import RUNTIME_TABLE_NAMES
from .domain_schema import class_name_for
from .domain_schema import fields_for
from .domain_schema import migration_path_for
from .domain_schema import owned_table
from .domain_schema import relationships_for
from .domain_schema import supported_backends
from .runtime import SCHEMA_REGISTRY_REQUIRED_EVENT_TOPIC


def _table_contract(table: str) -> dict:
    return {
        "logical_table": table,
        "owned_table": owned_table(table),
        "fields": fields_for(table),
        "relationships": relationships_for(table),
    }


def _model_contract(table: str) -> dict:
    return {
        "class_name": class_name_for(table),
        "table": owned_table(table),
        "fields": fields_for(table),
        "relationships": relationships_for(table),
    }


SCHEMA_CONTRACT = {
    "format": "appgen.schema-registry-owned-schema-contract.v1",
    "ok": True,
    "pbc": "schema_registry",
    "owned_tables": tuple(owned_table(table) for table in LOGICAL_TABLES),
    "logical_owned_tables": LOGICAL_TABLES,
    "tables": tuple(_table_contract(table) for table in LOGICAL_TABLES),
    "runtime_tables": tuple(_table_contract(table) for table in RUNTIME_TABLE_NAMES),
    "relationships": tuple(relationship for table in LOGICAL_TABLES for relationship in relationships_for(table)),
    "migrations": (migration_path_for("schema_subject"),),
    "migration_plan": tuple(
        {"path": migration_path_for(table), "operation": "create_owned_table", "table": owned_table(table)}
        for table in LOGICAL_TABLES
    ),
    "models": tuple(_model_contract(table) for table in LOGICAL_TABLES),
    "allowed_prefixes": (
        "schema_",
        "compatibility_",
        "consumer_",
        "producer_",
        "validation_",
        "payload_",
        "contract_",
        "gateway_",
        "audit_",
        "composition_",
        "workflow_",
        "route_",
        "access_",
        "package_",
        "pbc_",
        "carbon_",
    ),
    "datastore_backends": supported_backends(),
    "database_backends": supported_backends(),
    "required_event_topic": SCHEMA_REGISTRY_REQUIRED_EVENT_TOPIC,
    "event_contract": "AppGen-X",
    "shared_table_access": False,
    "schema_extensions": {"allowed": True, "owned_tables_only": True},
    "declared_dependencies": {
        "apis": (
            "GET /gateway/routes",
            "GET /identity/policies",
            "POST /audit/contract-events",
            "POST /composition/contracts",
        ),
        "events": ("PbcDeployed", "EventContractProposed", "RoutePublished", "AccessPolicyChanged", "PackageRegistrationRequested"),
        "shared_tables": (),
    },
}


def build_schema_contract():
    """Return generated owned schema, migration, and model evidence."""
    return dict(SCHEMA_CONTRACT)


def validate_schema_contract():
    """Validate owned table, migration, model, and datastore evidence."""
    contract = build_schema_contract()
    pbc = contract["pbc"]
    owned_tables = tuple(contract.get("owned_tables", ()))
    model_tables = tuple(
        model.get("table")
        for model in contract.get("models", ())
        if isinstance(model, dict) and model.get("table")
    )
    migration_paths = tuple(contract.get("migrations", ()))
    allowed_backends = {"postgresql", "mysql", "mariadb"}
    invalid_tables = tuple(table for table in owned_tables if not table.startswith(f"{pbc}_"))
    missing_models = tuple(table for table in owned_tables if table not in model_tables)
    invalid_backends = tuple(backend for backend in contract.get("database_backends", ()) if backend not in allowed_backends)
    thin_tables = tuple(table["owned_table"] for table in contract["tables"] if len(table["fields"]) < 6)
    return {
        "ok": contract.get("ok") is True
        and len(owned_tables) >= 45
        and bool(migration_paths)
        and not invalid_tables
        and not missing_models
        and not invalid_backends
        and not thin_tables
        and contract.get("shared_table_access") is False,
        "pbc": pbc,
        "owned_tables": owned_tables,
        "model_tables": model_tables,
        "migration_paths": migration_paths,
        "invalid_tables": invalid_tables,
        "missing_models": missing_models,
        "invalid_backends": invalid_backends,
        "thin_tables": thin_tables,
        "side_effects": (),
    }


def smoke_test():
    """Exercise schema validation side-effect-free."""
    return validate_schema_contract()
