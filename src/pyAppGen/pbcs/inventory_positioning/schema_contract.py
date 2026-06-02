"""Owned schema contract and migration evidence for inventory_positioning."""

from __future__ import annotations

from pathlib import Path
import re

from .runtime import INVENTORY_POSITIONING_OWNED_TABLES
from .runtime import inventory_positioning_build_schema_contract as runtime_build_schema_contract


PBC_KEY = "inventory_positioning"
MIGRATION_PATH = Path(__file__).with_name("migrations") / "001_initial.sql"


def _migration_sql() -> str:
    return MIGRATION_PATH.read_text(encoding="utf-8")


def _tables_in_migration(sql: str) -> tuple[str, ...]:
    return tuple(re.findall(r"CREATE TABLE\s+([a-zA-Z0-9_]+)\s*\(", sql, re.IGNORECASE))


def build_schema_contract() -> dict:
    runtime_schema = runtime_build_schema_contract()
    sql = _migration_sql()
    tables_in_sql = set(_tables_in_migration(sql))
    owned_tables = tuple(item["table"] for item in runtime_schema["tables"])
    missing_from_migration = tuple(table for table in owned_tables if table not in tables_in_sql)
    migration_coverage = tuple(
        {
            "table": table,
            "path": "migrations/001_initial.sql",
            "covered": table in tables_in_sql,
        }
        for table in owned_tables
    )
    return {
        **runtime_schema,
        "pbc": PBC_KEY,
        "owned_tables": owned_tables,
        "migration_files": ("migrations/001_initial.sql",),
        "migration_coverage": migration_coverage,
        "missing_from_migration": missing_from_migration,
        "migration_sql_present": bool(sql.strip()),
        "ok": runtime_schema["ok"] and not missing_from_migration and bool(sql.strip()),
    }


SCHEMA_CONTRACT = build_schema_contract()


def smoke_test() -> dict:
    contract = build_schema_contract()
    return {
        "ok": contract["ok"]
        and len(contract["owned_tables"]) == len(INVENTORY_POSITIONING_OWNED_TABLES)
        and not contract["missing_from_migration"],
        "contract": contract,
        "side_effects": (),
    }
