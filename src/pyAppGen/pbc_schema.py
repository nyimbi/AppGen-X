"""Read a PBC's owned tables from its own migration.

Every PBC package ships `migrations/001_initial.sql`, and that file is the one
place a package states its real columns and their types. The generated
implementation contract used to ignore it and emit `code`/`status`/`version`
for every table, so a `dam_core` app declared 49 tables and gave all of them the
same three fields.

The migration is the source of truth here rather than `runtime.py`, because the
packages disagree on the shape of their schema contract: some carry typed field
dicts, most carry bare column names, and the SQL is the only surface that is
both typed and uniform across all of them.

The parse is deliberately narrow. These files are machine-written by the same
generator, so the grammar is a fixed subset: `CREATE TABLE`, comma-separated
column definitions (68 packages write every table one column per line, 77 write
every table on a single line, and 2 mix the two, so the split is on commas at
parenthesis depth zero, not on newlines), and table-level `PRIMARY KEY`,
`FOREIGN KEY` and `UNIQUE` constraints. A multi-word type (`DOUBLE PRECISION`),
an inline `UNIQUE`, and a quoted reserved-word identifier are all read. Anything
outside that subset is skipped rather than guessed at.
"""

from __future__ import annotations

import re
from collections.abc import Iterable
from functools import lru_cache
from pathlib import Path

__all__ = (
    "PACKAGE_ROOT",
    "fields_for",
    "migration_path",
    "normalize_type",
    "owned_schema",
    "parse_migration",
    "quote_identifier",
)

PACKAGE_ROOT = Path(__file__).resolve().parent / "pbcs"
MIGRATION_NAME = "001_initial.sql"

_CREATE_TABLE = re.compile(
    r"CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?([A-Za-z0-9_]+)\s*\((.*?)\)\s*;",
    re.DOTALL | re.IGNORECASE,
)
_COLUMN = re.compile(
    r'^("?)([A-Za-z0-9_]+)\1\s+([A-Za-z]+(?:\s+(?:PRECISION|VARYING|WITH(?:OUT)?\s+TIME\s+ZONE))?(?:\s*\([0-9,\s]+\))?)',
    re.IGNORECASE,
)
_TABLE_PRIMARY_KEY = re.compile(r"PRIMARY\s+KEY\s*\(([^)]*)\)", re.IGNORECASE)
_TABLE_FOREIGN_KEY = re.compile(
    r"FOREIGN\s+KEY\s*\(([^)]*)\)\s*REFERENCES\s+([A-Za-z0-9_]+)\s*\(([^)]*)\)",
    re.IGNORECASE,
)
# Table-level `UNIQUE (a, b)`. Not `UNIQUE` inside a column definition: the
# lookbehind rejects a preceding word character, so `ticket_id VARCHAR(255) NOT
# NULL UNIQUE,` does not read as a table constraint, and `UNIQUE (a)` after a
# comma does. 293 tables across the catalog carry one, and 787 parsed foreign
# keys target a column that is unique but not the primary key, so a foreign key
# re-emitted against that column needs the constraint to exist.
_TABLE_UNIQUE = re.compile(r"(?<![A-Za-z0-9_])UNIQUE\s*\(([^)]*)\)", re.IGNORECASE)
_INLINE_UNIQUE = re.compile(r"\bUNIQUE\b", re.IGNORECASE)

# Identifiers that are reserved words and must stay quoted in emitted DDL.
# `asset_lifecycle` and `api_gateway_mesh` name a column `"window"`; the
# generator dropped the quotes and the statement died with
# `syntax error at or near "window"`.
_RESERVED = frozenset(
    {
        "all", "and", "any", "array", "as", "asc", "between", "both", "case",
        "cast", "check", "column", "constraint", "cross", "current_date",
        "current_time", "current_timestamp", "current_user", "default", "desc",
        "distinct", "do", "else", "end", "except", "exists", "false", "foreign",
        "from", "full", "grant", "group", "having", "in", "inner", "intersect",
        "into", "is", "join", "key", "leading", "left", "like", "limit",
        "natural", "not", "null", "offset", "on", "only", "or", "order", "outer",
        "over", "partition", "primary", "range", "references", "right", "role",
        "rows", "select", "session", "similar", "some", "table", "then", "time",
        "to", "trailing", "true", "union", "unique", "user", "using", "values",
        "when", "where", "window", "with",
    }
)


def quote_identifier(name: str) -> str:
    """Quote an identifier that is a reserved word or not plain lowercase.

    Everything the packages emit is lower snake_case, so the common case is a
    no-op; only the handful of reserved-word names change shape.
    """
    if name in _RESERVED or not re.fullmatch(r"[a-z_][a-z0-9_]*", name):
        return f'"{name}"'
    return name


# Table-level constraints to skip. These are keywords, so the match is on the
# keyword boundary rather than on a name prefix: a column named `check_id`,
# `checksum`, `keywords`, or `index_id` begins with a constraint word and was
# silently dropped by a `startswith` test. 40 columns across 18 packages were
# lost that way, and the descriptor then reported those tables as missing the
# very column that named them.
_CONSTRAINT_KEYWORD = re.compile(
    r"^(?:FOREIGN\s+KEY|PRIMARY\s+KEY|CONSTRAINT|UNIQUE|CHECK|KEY|INDEX)\b",
    re.IGNORECASE,
)

# SQL type to the canonical lowercase vocabulary the rest of the generator
# uses. The raw type is kept alongside it so nothing is lost on the way back
# out to SQL.
_TYPE_MAP = (
    ("BIGSERIAL", "integer"),
    ("SERIAL", "integer"),
    ("BIGINT", "integer"),
    ("SMALLINT", "integer"),
    ("INTEGER", "integer"),
    ("INT", "integer"),
    ("TIMESTAMPTZ", "datetime"),
    ("TIMESTAMP", "datetime"),
    ("DATETIME", "datetime"),
    ("DATE", "datetime"),
    ("TIME", "datetime"),
    ("BOOLEAN", "boolean"),
    ("BOOL", "boolean"),
    ("JSONB", "json"),
    ("JSON", "json"),
    ("NUMERIC", "decimal"),
    ("DECIMAL", "decimal"),
    ("MONEY", "decimal"),
    ("REAL", "decimal"),
    ("DOUBLE", "decimal"),
    ("FLOAT", "decimal"),
    ("TEXT", "text"),
    ("UUID", "text"),
    ("VARCHAR", "text"),
    ("CHAR", "text"),
)


def migration_path(key: str) -> Path:
    """Return the migration file for ``key``."""
    return PACKAGE_ROOT / key / "migrations" / MIGRATION_NAME


def normalize_type(sql_type: str) -> str:
    """Map a SQL type to the generator's canonical lowercase vocabulary."""
    upper = sql_type.upper()
    for prefix, canonical in _TYPE_MAP:
        if upper.startswith(prefix):
            return canonical
    return "string"


def _split_columns(body: str) -> list[str]:
    """Split a table body into column definitions.

    The packages write their DDL two ways. 68 put every ``CREATE TABLE`` on
    several lines; 77 put every one on a single line, and 2 mix the two within
    one file. Splitting on newlines reads the single-line shape as one
    statement, so ``_COLUMN`` matches its leading ``id TEXT`` and silently drops
    the other seven columns, which is how a
    `clinical_care_coordination_patient_care_plan` came to have no patient and
    no plan.

    A split on commas at parenthesis depth zero reads both. A type's own width
    carries a comma (`NUMERIC(10, 2)`) and a table-level `PRIMARY KEY (a, b)`
    does too, so depth is tracked rather than assumed absent; the newline split
    was exact only for the layout it was written against.
    """
    statements: list[str] = []
    depth = 0
    current: list[str] = []
    for character in body:
        if character == "(":
            depth += 1
        elif character == ")":
            depth -= 1
        if character == "," and depth == 0:
            statements.append("".join(current))
            current = []
            continue
        current.append(character)
    statements.append("".join(current))
    return [statement.strip() for statement in statements if statement.strip()]


def parse_migration(text: str) -> dict[str, dict]:
    """Parse ``CREATE TABLE`` statements into owned-table contracts.

    Returns:
        A mapping of physical table name to ``{"fields": tuple[dict, ...],
        "relationships": tuple[dict, ...], "unique": tuple[tuple[str, ...], ...]}``.
        A table with no parsable columns is omitted rather than returned empty.
    """
    tables: dict[str, dict] = {}
    for table_name, body in _CREATE_TABLE.findall(text):
        statements = _split_columns(body)
        composite_pk = {
            name.strip()
            for match in _TABLE_PRIMARY_KEY.findall(body)
            for name in match.split(",")
        }
        # A composite key sets `primary_key` on each of its columns but only one
        # may carry the inline `PRIMARY KEY` clause, so the members are recorded
        # here and the emitter writes a single table-level constraint instead.
        composite_members = tuple(name for name in composite_pk if name)
        foreign_keys = _TABLE_FOREIGN_KEY.findall(body)
        unique_keys = tuple(
            tuple(column.strip() for column in match.split(",") if column.strip())
            for match in _TABLE_UNIQUE.findall(body)
        )
        fields: list[dict] = []
        for statement in statements:
            if _CONSTRAINT_KEYWORD.match(statement):
                continue
            match = _COLUMN.match(statement)
            if not match:
                continue
            name, sql_type = match.group(2), match.group(3)
            upper = statement.upper()
            fields.append(
                {
                    "name": name,
                    "type": normalize_type(sql_type),
                    "sql_type": sql_type.upper(),
                    "primary_key": "PRIMARY KEY" in upper or name in composite_pk,
                    "required": "NOT NULL" in upper or "PRIMARY KEY" in upper or name in composite_pk,
                    "unique": bool(_INLINE_UNIQUE.search(statement)),
                }
            )
        if not fields:
            continue
        relationships = tuple(
            {
                "field": column.strip(),
                "target_table": target.strip(),
                "target_column": target_column.strip(),
                "cardinality": "many-to-one",
                "ownership": "same_pbc",
            }
            for columns, target, target_column in foreign_keys
            for column in columns.split(",")
        )
        tables[table_name] = {
            "fields": tuple(fields),
            "relationships": relationships,
            "composite_primary_key": composite_members,
            "unique": unique_keys,
        }
    return tables


@lru_cache(maxsize=None)
def _cached_parse(key: str) -> dict[str, dict]:
    path = migration_path(key)
    if not path.is_file():
        return {}
    return parse_migration(path.read_text(encoding="utf-8"))


def owned_schema(key: str) -> dict[str, dict]:
    """Return the parsed owned tables for one PBC, or ``{}`` when absent.

    An absent migration is a real gap, but it is reported by the contract that
    consumes this rather than raised here, so a missing file degrades to the
    caller's own fallback instead of breaking catalog assembly.
    """
    return _cached_parse(key)


def fields_for(key: str, candidates: Iterable[str]) -> tuple[dict, ...]:
    """Return the columns of the first candidate name the migration declares.

    A logical table name and the package's own physical name for the same table
    are not always equal, so callers pass every name the table might be known
    by and take the first that exists.
    """
    tables = owned_schema(key)
    for candidate in candidates:
        table = tables.get(candidate)
        if table and table["fields"]:
            return table["fields"]
    return ()
