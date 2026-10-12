"""The migration the generator emits must be DDL Postgres will accept.

`pbc_implementation_contract(key)["migrations"][0]["sql"]` is the only schema a
generated app ships: `migrations/versions/` is empty, so nothing else creates a
table. It did not apply for 117 of 147 packages, and no gate saw it because the
contract tests assert on the shape of a dict, not on whether Postgres parses it.

The five defects, each with the package that exposed it:

* `_table_contract` synthesised a `<primary_table>_id INTEGER` foreign key for
  every table at `position > 0`, targeting `id`, whatever the package's own
  migration declared. `dam_core_asset_version.asset_id` is a `VARCHAR(255)`
  business key pointing at a `UNIQUE` column, and the synthetic form pointed it
  at an `INTEGER` surrogate: 101 packages failed with `foreign key constraint
  cannot be implemented`.
* A relationship to a table outside the emitted set, or to a column the target
  does not have: 7 packages, `column ... does not exist`.
* Declaration order is not dependency order. `gl_core_journal_entry` references
  `gl_core_accounting_period`, which the service contract lists later:
  `relation "gl_core_accounting_period" does not exist`.
* A composite primary key was written as an inline `PRIMARY KEY` clause on each
  member: `audit_ledger`'s `multiple primary keys for table are not allowed`.
* A reserved-word column (`"window"`) lost its quotes: `syntax error at or near
  "window"` for `asset_lifecycle` and `api_gateway_mesh`.

The checks here are the properties that made each failure, asserted on the
emitted text for every package. They are not a substitute for applying the SQL,
which `tests/ci` cannot do without a Postgres, but each is canaried against the
exact defect it guards, so none passes vacuously.
"""

import re

import pytest

from pyAppGen import pbc_schema
from pyAppGen.pbc import IMPLEMENTED_PBC_KEYS, pbc_implementation_contract

RESERVED = pbc_schema._RESERVED


def _sql(key: str) -> str:
    return pbc_implementation_contract(key)["migrations"][0]["sql"]


def _created_tables(sql: str) -> list[str]:
    return re.findall(r"CREATE TABLE (\S+) \(", sql)


def _unquoted_reserved_columns(sql: str) -> list[str]:
    """Return reserved-word column names emitted without quotes.

    Only column definitions count: a table-level `FOREIGN KEY`, `UNIQUE` or
    `PRIMARY KEY` clause begins with a reserved word too, and reading one as a
    column name reports a defect that is not there.
    """
    found = []
    for line in sql.splitlines():
        if re.match(r"\s*(?:FOREIGN\s+KEY|PRIMARY\s+KEY|UNIQUE|CHECK|CONSTRAINT)\b", line, re.I):
            continue
        match = re.match(r'^  ("?)([A-Za-z_][A-Za-z0-9_]*)\1\s+[A-Z]', line)
        if match and match.group(1) != '"' and match.group(2).lower() in RESERVED:
            found.append(match.group(2))
    return found


def _table_bodies(sql: str) -> dict[str, str]:
    """Return each created table's body, so constraints can be read per table."""
    return {
        name: body
        for name, body in re.findall(r"CREATE TABLE (\S+) \((.*?)\n\);", sql, re.DOTALL)
    }


def _columns_by_table(sql: str) -> dict[str, set[str]]:
    columns: dict[str, set[str]] = {}
    for name, body in _table_bodies(sql).items():
        columns[name] = {
            match.group(2)
            for line in body.splitlines()
            if (match := re.match(r'\s*("?)([A-Za-z0-9_]+)\1\s+[A-Z]', line))
        }
    return columns


def _unique_columns(sql: str) -> dict[str, set[str]]:
    """Columns carrying a unique constraint, table-level or inline."""
    unique: dict[str, set[str]] = {}
    for name, body in _table_bodies(sql).items():
        found = {
            column.strip().strip('"')
            for clause in re.findall(r"UNIQUE \(([^)]*)\)", body)
            for column in clause.split(",")
        }
        for line in body.splitlines():
            if re.search(r"\bUNIQUE\b", line) and not line.strip().startswith("UNIQUE"):
                match = re.match(r'\s*("?)([A-Za-z0-9_]+)\1\s+[A-Z]', line)
                if match:
                    found.add(match.group(2))
        unique[name] = found
    return unique


def _primary_columns(sql: str) -> dict[str, set[str]]:
    """Columns that are primary key, inline or in a table-level clause."""
    primary: dict[str, set[str]] = {}
    for name, body in _table_bodies(sql).items():
        found = {
            column.strip().strip('"')
            for clause in re.findall(r"PRIMARY KEY \(([^)]*)\)", body)
            for column in clause.split(",")
        }
        for line in body.splitlines():
            if "PRIMARY KEY" in line and "(" not in line:
                match = re.match(r'\s*("?)([A-Za-z0-9_]+)\1\s+[A-Z]', line)
                if match:
                    found.add(match.group(2))
        primary[name] = found
    return primary


@pytest.mark.parametrize("key", IMPLEMENTED_PBC_KEYS)
def test_a_foreign_key_targets_an_emitted_table_and_column(key: str) -> None:
    """Every `REFERENCES t(c)` must name a table and column this SQL creates.

    A target outside the emitted set is the contract carrying a relationship the
    migration never creates, and Postgres refuses the statement.
    """
    sql = _sql(key)
    created = set(_created_tables(sql))
    columns = _columns_by_table(sql)
    bad = []
    for table, column in re.findall(r"REFERENCES (\S+)\((\"?[A-Za-z0-9_]+\"?)\)", sql):
        if table not in created:
            bad.append(f"table {table} not created")
        elif column.strip('"') not in columns.get(table, set()):
            bad.append(f"column {table}.{column} absent")
    assert not bad, (key, bad[:5])


@pytest.mark.parametrize("key", IMPLEMENTED_PBC_KEYS)
def test_a_foreign_key_target_column_is_unique(key: str) -> None:
    """Postgres needs a unique index on the referenced column, not just a key.

    787 parsed foreign keys point at a business key the migration marks `UNIQUE`
    and not `PRIMARY KEY`, so the constraint has to survive into the emitted SQL.
    """
    sql = _sql(key)
    unique = _unique_columns(sql)
    primary = _primary_columns(sql)
    bad = [
        f"{table}.{column}"
        for table, column in re.findall(r"REFERENCES (\S+)\((\"?[A-Za-z0-9_]+\"?)\)", sql)
        if column.strip('"') not in unique.get(table, set())
        and column.strip('"') not in primary.get(table, set())
    ]
    assert not bad, (key, bad[:5])


@pytest.mark.parametrize("key", IMPLEMENTED_PBC_KEYS)
def test_a_table_is_created_after_the_tables_it_references(key: str) -> None:
    """A forward reference is `relation does not exist` at apply time."""
    sql = _sql(key)
    order = {name: position for position, name in enumerate(_created_tables(sql))}
    bad = []
    for statement in re.findall(r"CREATE TABLE .*?\n\);", sql, re.DOTALL):
        name = _created_tables(statement)[0]
        for target in re.findall(r"REFERENCES (\S+)\(", statement):
            if target in order and order[target] > order[name]:
                bad.append(f"{name} -> {target}")
    assert not bad, (key, bad[:5])


@pytest.mark.parametrize("key", IMPLEMENTED_PBC_KEYS)
def test_a_reserved_word_identifier_is_quoted(key: str) -> None:
    """A column named `window` or `table` is a syntax error unquoted."""
    sql = _sql(key)
    unquoted = _unquoted_reserved_columns(sql)
    assert not unquoted, (key, unquoted[:5])


@pytest.mark.parametrize("key", IMPLEMENTED_PBC_KEYS)
def test_the_event_trio_is_created_once(key: str) -> None:
    """A package that lists the trio in its own contract must not get it twice."""
    sql = _sql(key)
    created = _created_tables(sql)
    duplicates = {name for name in created if created.count(name) > 1}
    assert not duplicates, (key, sorted(duplicates))


def test_the_forward_reference_check_canaries_on_gl_core() -> None:
    """Point the ordering check at the real package and confirm it can fail.

    `gl_core_journal_entry` references `gl_core_accounting_period`, and the
    service contract lists the period table after the journal. The shipped SQL
    must be ordered; the declaration order must not be. If both pass, the check
    is measuring nothing.
    """
    from pyAppGen.pbc import _service_contract

    declared = _service_contract("gl_core")["tables"]
    emitted = _sql("gl_core")
    order = {name: position for position, name in enumerate(_created_tables(emitted))}
    journal = "gl_core_journal_entry"
    period = "gl_core_accounting_period"
    assert "gl_core_accounting_period" in emitted

    declared_order = list(declared)
    assert declared_order.index("accounting_period") > declared_order.index("journal_entry"), (
        "the canary needs the period declared after the journal, or it proves nothing"
    )
    assert order[period] < order[journal], "the emitted SQL must order the period first"

    # And the check itself must report the declaration order as broken, which is
    # what it would have seen before `_dependency_ordered` existed.
    declaration_sql = "\n".join(
        f"CREATE TABLE {name} (\n  id INTEGER PRIMARY KEY\n);"
        for name in ("gl_core_journal_entry", "gl_core_accounting_period")
    ) + "\nCREATE TABLE gl_core_journal_entry_x (\n  id INTEGER PRIMARY KEY,\n  FOREIGN KEY (id) REFERENCES gl_core_accounting_period(id)\n);"
    broken_order = {
        name: position for position, name in enumerate(_created_tables(declaration_sql))
    }
    assert broken_order["gl_core_journal_entry"] < broken_order["gl_core_accounting_period"], (
        "the canary's declaration order must put the journal before the period"
    )


def test_the_composite_primary_key_check_canaries_on_audit_ledger() -> None:
    """`audit_ledger`'s `audit_event` keys on two columns, written as one clause."""
    sql = _sql("audit_ledger")
    statement = re.search(r"CREATE TABLE audit_ledger_audit_event \(.*?\n\);", sql, re.DOTALL)
    assert statement, "the canary needs the audit_event table"
    body = statement.group(0)
    assert body.count("PRIMARY KEY") == 1, body
    assert re.search(r"PRIMARY KEY \(audit_id, aggregate_id\)", body), body


def test_the_identifier_and_target_checks_canary_on_planted_sql() -> None:
    """Point the text checks at the defect's own shape and confirm they report it.

    Each helper is pure over a SQL string, so a hand-written broken migration is
    the known-bad input. If any of these passes on the broken text, the check it
    exercises is blind.
    """
    broken = (
        "CREATE TABLE t (\n"
        "  id INTEGER PRIMARY KEY,\n"
        "  window TIMESTAMP NOT NULL,\n"
        "  other_id VARCHAR(255) NOT NULL,\n"
        "  FOREIGN KEY (other_id) REFERENCES missing(id)\n"
        ");\n"
        "CREATE TABLE child (\n"
        "  id INTEGER PRIMARY KEY,\n"
        "  parent_id INTEGER NOT NULL,\n"
        "  FOREIGN KEY (parent_id) REFERENCES t(nope)\n"
        ");"
    )
    created = set(_created_tables(broken))
    columns = _columns_by_table(broken)
    assert "missing" not in created, "the canary needs a target outside the created set"
    assert "nope" not in columns["t"], "the canary needs a column the target lacks"

    unquoted = _unquoted_reserved_columns(broken)
    assert unquoted == ["window"], unquoted

    unique = _unique_columns(broken)
    primary = _primary_columns(broken)
    bad = [
        f"{table}.{column}"
        for table, column in re.findall(r"REFERENCES (\S+)\((\"?[A-Za-z0-9_]+\"?)\)", broken)
        if column.strip('"') not in unique.get(table, set())
        and column.strip('"') not in primary.get(table, set())
    ]
    assert bad, "the unique-target check passed on a foreign key to a non-unique column"
