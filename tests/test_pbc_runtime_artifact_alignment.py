from __future__ import annotations

import importlib
from pathlib import Path

from pyAppGen.pbc import PBC_CATALOG


def _runtime_owned_tables(key: str) -> set[str]:
    package = importlib.import_module(f"pyAppGen.pbcs.{key}")
    capabilities = getattr(package, f"{key}_runtime_capabilities")()
    return {
        table if table.startswith(f"{key}_") else f"{key}_{table}"
        for table in capabilities.get("owned_tables", ())
    }


def test_every_pbc_runtime_table_has_package_artifacts() -> None:
    """Every runtime-owned table must be materialized in package artifacts."""
    for key in PBC_CATALOG:
        expected_tables = _runtime_owned_tables(key)
        schema = importlib.import_module(f"pyAppGen.pbcs.{key}.schema_contract")
        models = importlib.import_module(f"pyAppGen.pbcs.{key}.models")

        schema_contract = schema.build_schema_contract()
        model_manifest = models.model_manifest()
        migration_sql = (
            Path("src/pyAppGen/pbcs") / key / "migrations" / "001_initial.sql"
        ).read_text()

        assert expected_tables <= set(schema_contract["owned_tables"]), key
        assert expected_tables <= set(model_manifest["model_tables"]), key
        assert model_manifest["ok"] is True, key
        assert not model_manifest["cross_pbc_relationships"], key
        assert all(f"CREATE TABLE {table}" in migration_sql for table in expected_tables), key


def test_pbc_package_datastores_remain_allowed() -> None:
    allowed = {"postgresql", "mysql", "mariadb"}

    for key in PBC_CATALOG:
        schema = importlib.import_module(f"pyAppGen.pbcs.{key}.schema_contract")
        schema_contract = schema.build_schema_contract()

        backends = set(
            schema_contract.get("database_backends")
            or schema_contract.get("datastore_backends")
            or ()
        )
        assert backends <= allowed, key
        assert schema_contract.get("shared_table_access") is False, key
