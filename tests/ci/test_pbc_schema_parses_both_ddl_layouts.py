"""The migration parser must read both DDL layouts the packages ship.

`pbc_schema` is the control that reads each package's real columns from its own
`001_initial.sql`, and it split a table body on newlines. 70 of 147 packages put
one column per line and parsed correctly; the other 77 put the whole
`CREATE TABLE` on one line, so the body arrived as a single statement, `_COLUMN`
matched its leading `id TEXT`, and the remaining columns were dropped without a
word. A `banking_core_accounts_deposit_account` therefore had no account number
and no currency, and `clinical_care_coordination_patient_care_plan` had no
patient and no plan.

The failure was silent in the direction that looks clean: a one-column table
parses, so nothing raised and no gate saw a missing column. These tests hold the
parser to both layouts, and to the comma-in-parentheses cases that a naive
comma split would break instead.
"""

import re

import pytest

from pyAppGen import pbc_schema
from pyAppGen.pbc import IMPLEMENTED_PBC_KEYS

ENVELOPE = {
    "id",
    "tenant",
    "code",
    "status",
    "version",
    "payload",
    "created_at",
    "updated_at",
}


def test_a_single_line_table_body_keeps_every_column() -> None:
    """A one-line `CREATE TABLE` must yield all its columns, not its first.

    This is the exact shape 77 packages write and the parser read as one
    statement. `id TEXT` matched `_COLUMN` and the other seven names vanished.
    """
    parsed = pbc_schema.parse_migration(
        "CREATE TABLE t (id TEXT PRIMARY KEY, tenant TEXT NOT NULL, code TEXT, "
        "status TEXT, version INTEGER, payload JSON, created_at TEXT, updated_at TEXT);"
    )
    assert [field["name"] for field in parsed["t"]["fields"]] == [
        "id",
        "tenant",
        "code",
        "status",
        "version",
        "payload",
        "created_at",
        "updated_at",
    ]


def test_a_multi_line_table_body_still_parses() -> None:
    """The layout the newline split was written against must not regress."""
    parsed = pbc_schema.parse_migration(
        "CREATE TABLE t (\n"
        "  id INTEGER PRIMARY KEY NOT NULL,\n"
        "  tenant VARCHAR(255) NOT NULL,\n"
        "  filename VARCHAR(255) NOT NULL\n"
        ");"
    )
    assert [field["name"] for field in parsed["t"]["fields"]] == [
        "id",
        "tenant",
        "filename",
    ]


def test_a_type_width_comma_is_not_a_column_separator() -> None:
    """`NUMERIC(10, 2)` carries a comma; a depth-zero split keeps it whole.

    A comma split that ignored parentheses would cut this column in two and
    invent a column named `2)`.
    """
    parsed = pbc_schema.parse_migration(
        "CREATE TABLE t (amount NUMERIC(10, 2) NOT NULL, note TEXT);"
    )
    assert [field["name"] for field in parsed["t"]["fields"]] == ["amount", "note"]
    assert parsed["t"]["fields"][0]["type"] == "decimal"


def test_a_table_level_primary_key_comma_is_not_a_column_separator() -> None:
    """`PRIMARY KEY (a, b)` is one constraint, and its columns stay one key."""
    parsed = pbc_schema.parse_migration(
        "CREATE TABLE t (a TEXT, b TEXT, PRIMARY KEY (a, b));"
    )
    assert [field["name"] for field in parsed["t"]["fields"]] == ["a", "b"]
    assert all(field["primary_key"] for field in parsed["t"]["fields"])


@pytest.mark.parametrize("key", IMPLEMENTED_PBC_KEYS)
def test_no_package_parses_to_single_column_tables(key: str) -> None:
    """No package's migration may collapse to one-column tables.

    A real envelope table has eight columns and a real domain table has more
    than one, so a package whose every parsed table carries a lone `id` is the
    newline split dropping the rest. This is the platform-wide form of the
    defect, and it fails for any layout a future generator writes.
    """
    schema = pbc_schema.owned_schema(key)
    if not schema:
        pytest.skip(f"{key} ships no parseable migration")
    collapsed = [
        name for name, table in schema.items() if len(table["fields"]) <= 1
    ]
    assert not collapsed, f"{key} parsed these tables to a single column: {collapsed}"


@pytest.mark.parametrize("key", IMPLEMENTED_PBC_KEYS)
def test_a_package_that_names_real_columns_parses_them(key: str) -> None:
    """Where a migration names columns beyond the envelope, they must survive.

    The envelope is the same eight names everywhere, so a package whose parsed
    columns are *only* those eight either has an envelope-only migration or had
    its real ones dropped. The two are told apart by reading the file: if the
    raw SQL names a column the envelope does not, the parse must return it.
    """
    schema = pbc_schema.owned_schema(key)
    if not schema:
        pytest.skip(f"{key} ships no parseable migration")

    parsed = {field["name"] for table in schema.values() for field in table["fields"]}
    beyond = parsed - ENVELOPE
    if beyond:
        return

    raw = pbc_schema.migration_path(key).read_text(encoding="utf-8")
    declared = set(re.findall(r"[A-Za-z_][A-Za-z0-9_]*\s+(?:TEXT|VARCHAR|INTEGER|JSON|TIMESTAMP)", raw))
    names_in_sql = {
        match.split()[0]
        for match in declared
    } - ENVELOPE - {"TABLE", "SCHEMA", "IF", "NOT", "EXISTS"}
    assert not names_in_sql, (
        f"{key} parses no column beyond the envelope but its migration names "
        f"{sorted(names_in_sql)}"
    )
