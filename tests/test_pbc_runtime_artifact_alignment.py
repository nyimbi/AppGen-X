"""A PBC's package artifacts must agree with its own runtime.

A package names its owned tables in four places: `*_runtime_capabilities()`
(what runs), `build_schema_contract()` (the schema evidence), `models.py` (the
model evidence), and `migrations/001_initial.sql` (the DDL). When the enterprise
domain-depth wave added tables to the runtime, it left one or more of the other
three behind in twenty packages. `vendor_supplier_360` advertised 11 owned tables
in its schema and model evidence and 32 in its runtime. That is a package
contradicting itself, which is what this file catches.

The drift came in three shapes:

- Seventeen packages left `runtime.build_schema_contract()` and both evidence
  modules at the base count. The runtime builder is now the one source: it folds
  in `domain_depth_contract()['owned_tables']`, and `schema_contract.py` and
  `models.py` derive from it.
- `defense_readiness_logistics`, `donor_grant_fundraising`, and
  `field_service_management` left domain tables out of `001_initial.sql`, so the
  package declared tables it never created.
- `case_knowledge_management` carried the tables but exposed neither
  `model_manifest()` nor `model_contracts()`, so a consumer reading the
  convention's name saw nothing.

Three corrections to the original check, each of which had made it report the
wrong thing:

- It read `models.model_manifest()`, a convention of the first 47 packages. The
  eighty-one newer packages expose `model_contracts()`; the check now accepts
  either and fails only when a package exposes neither.
- It key-prefixed the runtime names but compared them against the raw contract
  and model names, so a package whose surfaces are identically *unprefixed*
  (`dam_core`, `composition_engine`) failed on spelling alone.
- It demanded the event trio in the package migration. `_migration_sql` creates
  `*_appgen_outbox_event`/`inbox`/`dead_letter_event` centrally for every
  selected PBC, so the trio is a platform concern and is exempt here.
"""

from __future__ import annotations

import importlib
import re
from pathlib import Path

import pytest

from pyAppGen.pbc import PBC_CATALOG

# The platform creates these for every PBC in `_migration_sql`, so a package
# migration that omits them is not a package defect.
EVENT_PLUMBING = frozenset(
    {"appgen_outbox_event", "appgen_inbox_event", "appgen_dead_letter_event", "dead_letter_event"}
)

_SOURCE_ROOT = Path(__file__).resolve().parents[1] / "src" / "pyAppGen" / "pbcs"


def _prefixed(key: str, name: str) -> str:
    return name if name.startswith(f"{key}_") else f"{key}_{name}"


def _bare(key: str, name: str) -> str:
    return name[len(key) + 1 :] if name.startswith(f"{key}_") else name


def _runtime_owned_tables(key: str) -> set[str]:
    package = importlib.import_module(f"pyAppGen.pbcs.{key}")
    capabilities = getattr(package, f"{key}_runtime_capabilities")()
    return {_prefixed(key, table) for table in capabilities.get("owned_tables", ())}


def _domain_tables(key: str) -> set[str]:
    """Runtime-owned tables excluding the centrally created event trio."""
    return {table for table in _runtime_owned_tables(key) if _bare(key, table) not in EVENT_PLUMBING}


def _schema_contract_tables(key: str) -> set[str]:
    schema = importlib.import_module(f"pyAppGen.pbcs.{key}.schema_contract")
    contract = schema.build_schema_contract()
    return {_prefixed(key, table) for table in (contract.get("owned_tables") or ())}


def _model_surface(key: str) -> tuple[set[str] | None, bool | None, tuple | None]:
    """Return (tables, ok, cross_pbc_relationships) from whichever surface exists.

    `ok` and `cross_pbc_relationships` are the alignment evidence `model_manifest`
    publishes; a package on the newer `model_contracts` surface carries neither,
    so both come back `None` and the caller skips those assertions.
    """
    models = importlib.import_module(f"pyAppGen.pbcs.{key}.models")
    if hasattr(models, "model_manifest"):
        manifest = models.model_manifest()
        tables = manifest.get("model_tables") or tuple(
            entry.get("owned_table") or entry.get("table")
            for entry in manifest.get("models", ())
            if isinstance(entry, dict)
        )
        return (
            {_prefixed(key, table) for table in tables if table},
            manifest.get("ok"),
            manifest.get("cross_pbc_relationships"),
        )
    if hasattr(models, "model_contracts"):
        tables = tuple(
            entry.get("owned_table") or entry.get("table")
            for entry in models.model_contracts()
            if isinstance(entry, dict)
        )
        return {_prefixed(key, table) for table in tables if table}, None, None
    return None, None, None


def _migration_tables(key: str) -> set[str]:
    path = _SOURCE_ROOT / key / "migrations" / "001_initial.sql"
    text = path.read_text(encoding="utf-8") if path.is_file() else ""
    return {
        _prefixed(key, table)
        for table in re.findall(r"CREATE TABLE (?:IF NOT EXISTS )?([A-Za-z0-9_]+)", text)
    }


@pytest.mark.parametrize("key", PBC_CATALOG)
def test_runtime_tables_appear_in_the_schema_contract(key: str) -> None:
    """`build_schema_contract()` must name every table the runtime owns."""
    missing = _domain_tables(key) - _schema_contract_tables(key)
    assert not missing, f"{key} schema_contract omits runtime-owned tables: {sorted(missing)}"


@pytest.mark.parametrize("key", PBC_CATALOG)
def test_runtime_tables_appear_in_the_package_models(key: str) -> None:
    """`models.py` must name every table the runtime owns."""
    tables, ok, cross_pbc = _model_surface(key)
    assert tables is not None, f"{key} models expose neither model_manifest() nor model_contracts()"
    missing = _domain_tables(key) - tables
    assert not missing, f"{key} models omit runtime-owned tables: {sorted(missing)}"
    if ok is not None:
        assert ok is True, f"{key} model_manifest reports ok=False"
    if cross_pbc is not None:
        assert not cross_pbc, f"{key} model_manifest reports cross-PBC relationships"


@pytest.mark.parametrize("key", PBC_CATALOG)
def test_runtime_tables_are_migrated(key: str) -> None:
    """The package migration must create every table the runtime owns.

    The event trio is exempt: `_migration_sql` creates it centrally.
    """
    missing = _domain_tables(key) - _migration_tables(key)
    assert not missing, f"{key} migration omits runtime-owned tables: {sorted(missing)}"


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
