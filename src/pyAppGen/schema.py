"""Canonical application schema model and source adapters.

The generator should not care whether a schema came from DBML, SQL DDL,
PonyORM-style entity declarations, or a live database.  This module provides
that stable intermediate representation.
"""

from __future__ import annotations

import ast
import hashlib
import json
import re
import textwrap
from dataclasses import dataclass
from dataclasses import field
from pathlib import Path
from typing import Iterable

from sqlalchemy import BigInteger
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import LargeBinary
from sqlalchemy import MetaData
from sqlalchemy import Numeric
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy import Text
from sqlalchemy import Time
from sqlalchemy import create_engine


SUPPORTED_PLATFORM_TARGETS = ("web", "pwa", "mobile", "desktop", "chatbot")
PLATFORM_TARGET_ALIASES = {
    "browser": "web",
    "spa": "web",
    "progressive_web_app": "pwa",
    "progressive_web": "pwa",
    "bot": "chatbot",
    "bots": "chatbot",
}
SUPPORTED_DATABASE_DIALECTS = (
    "sqlite",
    "postgresql",
    "mysql",
    "mariadb",
    "mssql",
    "oracle",
    "cockroachdb",
)
SUPPORTED_SCHEMA_SOURCES = (
    {
        "kind": "dbml",
        "extensions": (".dbml",),
        "entrypoint": "schema_from_dbml",
        "command": "appgen --dbml schema.dbml --writedir app",
    },
    {
        "kind": "sql",
        "extensions": (".sql", ".ddl"),
        "entrypoint": "schema_from_sql",
        "command": "appgen --sql schema.sql --writedir app",
    },
    {
        "kind": "ponyorm",
        "extensions": (".py",),
        "entrypoint": "schema_from_ponyorm",
        "command": "appgen --pony entities.py --writedir app",
    },
    {
        "kind": "database",
        "extensions": (),
        "entrypoint": "schema_from_database_url",
        "command": "appgen --database-url postgresql+psycopg2://user@host/db --writedir app",
        "url_dialects": SUPPORTED_DATABASE_DIALECTS,
        "sqlalchemy_driver_urls": True,
    },
    {
        "kind": "dsl",
        "extensions": (".ag", ".ags", ".appgen"),
        "entrypoint": "schema_from_dsl_file",
        "command": "appgen --dsl app.appgen --writedir app",
    },
)


def normalize_platform_targets(
    value: str | Iterable[str] | None,
    *,
    default: tuple[str, ...] = SUPPORTED_PLATFORM_TARGETS,
) -> tuple[tuple[str, ...], tuple[str, ...]]:
    """Normalize platform target app options into supported targets and unknowns."""
    if value is None:
        return default, ()
    if isinstance(value, str):
        raw_items: Iterable[str] = value.split(",")
    else:
        raw_items = value

    targets: list[str] = []
    unknown: list[str] = []
    for raw_item in raw_items:
        item = str(raw_item).strip().lower().replace("-", "_")
        if not item:
            continue
        target = PLATFORM_TARGET_ALIASES.get(item, item)
        if target not in SUPPORTED_PLATFORM_TARGETS:
            unknown.append(str(raw_item).strip())
            continue
        if target not in targets:
            targets.append(target)
    return tuple(targets), tuple(unknown)


@dataclass(frozen=True)
class ColumnSchema:
    """A portable column definition."""

    name: str
    type_name: str = "string"
    nullable: bool = True
    primary_key: bool = False
    unique: bool = False
    default: str | None = None
    references: tuple[str, str] | None = None
    hidden: bool = False
    searchable: bool = False
    derived: bool = False
    expression: str | None = None
    source_group: str | None = None


@dataclass(frozen=True)
class RelationSchema:
    """A portable relationship between two tables."""

    source_table: str
    source_column: str
    target_table: str
    target_column: str = "id"
    name: str | None = None
    cardinality: str = "many-to-one"


@dataclass(frozen=True)
class ViewSectionSchema:
    """A named low-code view section or tab."""

    name: str
    fields: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class FormComponentSchema:
    """A Delphi-style component placed on a generated form canvas."""

    name: str
    component: str
    field: str | None = None
    x: int = 0
    y: int = 0
    w: int = 4
    h: int = 1


@dataclass(frozen=True)
class ViewSchema:
    """A low-code view declaration."""

    name: str
    table: str
    fields: tuple[str, ...] = field(default_factory=tuple)
    sections: tuple[ViewSectionSchema, ...] = field(default_factory=tuple)
    components: tuple[FormComponentSchema, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class FlowStepSchema:
    """One transition in a low-code workflow."""

    source: str
    target: str


@dataclass(frozen=True)
class FlowSchema:
    """A low-code workflow declaration."""

    name: str
    steps: tuple[FlowStepSchema, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class PermissionSchema:
    """Actions a role can perform on a resource."""

    resource: str
    actions: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class RoleSchema:
    """A low-code role declaration."""

    name: str
    permissions: tuple[PermissionSchema, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class RuleConditionSchema:
    """One low-code business rule condition or decision branch."""

    field: str
    operator: str
    values: tuple[str, ...] = field(default_factory=tuple)
    message: str | None = None
    action: str | None = None


@dataclass(frozen=True)
class RuleSchema:
    """A low-code business rule declaration for a table."""

    name: str
    table: str
    conditions: tuple[RuleConditionSchema, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class EnumSchema:
    """A portable domain vocabulary for lookup/select fields."""

    name: str
    values: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class LLMProviderSchema:
    """A generated LLM provider configuration contract."""

    name: str
    provider: str = "openai"
    mode: str = "api"
    model: str | None = None
    endpoint: str | None = None
    api_key: str | None = None


@dataclass(frozen=True)
class AgentSchema:
    """A generated agentic workflow contract."""

    name: str
    provider: str | None = None
    goal: str | None = None
    tools: tuple[str, ...] = field(default_factory=tuple)
    memory: str = "session"
    max_steps: int = 8


@dataclass(frozen=True)
class TableSchema:
    """A portable table definition."""

    name: str
    columns: tuple[ColumnSchema, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class AppSchema:
    """Portable app schema shared by all importers and generators."""

    tables: tuple[TableSchema, ...] = field(default_factory=tuple)
    relations: tuple[RelationSchema, ...] = field(default_factory=tuple)
    source: str | None = None
    app_name: str | None = None
    app_options: dict[str, str] = field(default_factory=dict)
    views: tuple[ViewSchema, ...] = field(default_factory=tuple)
    flows: tuple[FlowSchema, ...] = field(default_factory=tuple)
    roles: tuple[RoleSchema, ...] = field(default_factory=tuple)
    rules: tuple[RuleSchema, ...] = field(default_factory=tuple)
    enums: tuple[EnumSchema, ...] = field(default_factory=tuple)
    llm_providers: tuple[LLMProviderSchema, ...] = field(default_factory=tuple)
    agents: tuple[AgentSchema, ...] = field(default_factory=tuple)

    def table(self, name: str) -> TableSchema:
        for table in self.tables:
            if table.name == name:
                return table
        raise KeyError(name)

    def source_profile(self) -> dict:
        """Return stable source provenance and normalized schema fingerprints."""
        table_signatures = tuple(
            {
                "table": table.name,
                "fields": tuple(column.name for column in table.columns),
                "primary_keys": tuple(column.name for column in table.columns if column.primary_key),
                "required_fields": tuple(
                    column.name for column in table.columns if not column.nullable and not column.primary_key
                ),
                "unique_fields": tuple(column.name for column in table.columns if column.unique),
            }
            for table in self.tables
        )
        relation_signatures = tuple(
            {
                "source": f"{relation.source_table}.{relation.source_column}",
                "target": f"{relation.target_table}.{relation.target_column}",
                "cardinality": relation.cardinality,
            }
            for relation in self.relations
        )
        enum_signatures = tuple(
            {
                "enum": enum.name,
                "values": tuple(enum.values),
            }
            for enum in self.enums
        )
        profile = {
            "format": "appgen.schema-source-profile.v1",
            "source": self.source,
            "source_kind": schema_source_kind(self.source),
            "counts": {
                "tables": len(self.tables),
                "fields": sum(len(table.columns) for table in self.tables),
                "relations": len(self.relations),
                "enums": len(self.enums),
            },
            "table_signatures": table_signatures,
            "relation_signatures": relation_signatures,
            "enum_signatures": enum_signatures,
            "canonical_contract": "AppSchema",
        }
        fingerprint_payload = {
            "source_kind": profile["source_kind"],
            "counts": profile["counts"],
            "table_signatures": table_signatures,
            "relation_signatures": relation_signatures,
            "enum_signatures": enum_signatures,
        }
        profile["fingerprint"] = hashlib.sha256(
            json.dumps(fingerprint_payload, sort_keys=True, default=list).encode("utf-8")
        ).hexdigest()[:16]
        return profile

    def to_metadata(self) -> MetaData:
        metadata = MetaData()
        table_names = {table.name for table in self.tables}
        relation_by_column = {
            (relation.source_table, relation.source_column): relation
            for relation in self.relations
            if relation.target_table in table_names
        }
        enum_by_name = {enum.name: enum for enum in self.enums}

        for table in self.tables:
            columns = []
            for column in table.columns:
                if column.derived:
                    continue
                relation = relation_by_column.get((table.name, column.name))
                args = []
                if relation is not None:
                    args.append(ForeignKey(f"{relation.target_table}.{relation.target_column}"))
                column_type = (
                    SQLAlchemyEnum(
                        *enum_by_name[column.type_name].values,
                        name=f"{column.type_name.lower()}_enum",
                    )
                    if column.type_name in enum_by_name
                    else sqlalchemy_type(column.type_name)
                )
                columns.append(
                    Column(
                        column.name,
                        column_type,
                        *args,
                        primary_key=column.primary_key,
                        nullable=column.nullable,
                        unique=column.unique,
                    )
                )
            Table(table.name, metadata, *columns)
        return metadata


def schema_source_kind(source: str | None) -> str:
    """Return the supported source family for a schema origin."""
    if not source:
        return "canonical"
    lowered = source.lower()
    scheme_match = re.match(r"^(?P<dialect>[a-z][a-z0-9_+.-]*):\/\/", lowered)
    if scheme_match:
        dialect = scheme_match.group("dialect").split("+", 1)[0]
        if dialect in SUPPORTED_DATABASE_DIALECTS:
            return "database"
    if lowered.endswith(".dbml"):
        return "dbml"
    if lowered.endswith((".sql", ".ddl")):
        return "sql"
    if lowered.endswith(".py"):
        return "ponyorm"
    if lowered.endswith((".ags", ".ag", ".appgen")):
        return "dsl"
    return "canonical"


def schema_source_contract() -> dict:
    """Return the canonical schema source families AppGen can generate from."""
    sources = tuple(
        dict(source, url_dialects=tuple(source.get("url_dialects", ())))
        for source in SUPPORTED_SCHEMA_SOURCES
    )
    source_kinds = tuple(source["kind"] for source in sources)
    return {
        "format": "appgen.schema-source-contract.v1",
        "canonical_contract": "AppSchema",
        "sources": sources,
        "source_kinds": source_kinds,
        "database_url_dialects": SUPPORTED_DATABASE_DIALECTS,
        "sqlalchemy_driver_urls": True,
        "ok": {"dbml", "sql", "ponyorm", "database"} <= set(source_kinds),
    }


def schema_from_database_url(database_url: str) -> AppSchema:
    engine = create_engine(database_url)
    metadata = MetaData()
    metadata.reflect(bind=engine)
    return schema_from_metadata(metadata, source=database_url)


def schema_from_metadata(metadata: MetaData, *, source: str | None = None) -> AppSchema:
    tables: list[TableSchema] = []
    relations: list[RelationSchema] = []
    enums: list[EnumSchema] = []
    enum_names: set[str] = set()

    for table in metadata.sorted_tables:
        columns: list[ColumnSchema] = []
        unique_columns = _metadata_unique_columns(table)
        for column in table.columns:
            reference = next(iter(column.foreign_keys), None)
            references = None
            if reference is not None:
                references = (reference.column.table.name, reference.column.name)
                relations.append(
                    RelationSchema(
                        source_table=table.name,
                        source_column=column.name,
                        target_table=reference.column.table.name,
                        target_column=reference.column.name,
                    )
                )
            type_name = _metadata_column_type(column, metadata)
            enum_values = tuple(getattr(column.type, "enums", ()) or ())
            if enum_values and type_name not in enum_names:
                enums.append(EnumSchema(type_name, enum_values))
                enum_names.add(type_name)
            columns.append(
                ColumnSchema(
                    name=column.name,
                    type_name=type_name,
                    nullable=column.nullable,
                    primary_key=column.primary_key,
                    unique=bool(column.unique) or column.name in unique_columns,
                    default=_metadata_column_default(column),
                    references=references,
                )
            )
        tables.append(TableSchema(name=table.name, columns=tuple(columns)))

    return AppSchema(
        tables=tuple(tables),
        relations=tuple(relations),
        source=source,
        enums=tuple(enums),
    )


def schema_from_dbml(path: str | Path) -> AppSchema:
    from pydbml import PyDBML

    parsed = PyDBML(Path(path))
    tables: list[TableSchema] = []
    relations: list[RelationSchema] = []
    enums = tuple(
        EnumSchema(
            enum.name,
            tuple(getattr(item, "name", str(item)) for item in getattr(enum, "items", ())),
        )
        for enum in getattr(parsed, "enums", ())
    )

    for table in parsed.tables:
        columns: list[ColumnSchema] = []
        refs = _dbml_refs_for_table(table)
        unique_index_columns = _dbml_single_column_unique_indexes(table)
        for column in table.columns:
            ref = refs.get(column.name)
            primary_key = bool(getattr(column, "pk", False))
            columns.append(
                ColumnSchema(
                    name=column.name,
                    type_name=str(column.type),
                    nullable=not bool(getattr(column, "not_null", False)) and not primary_key,
                    primary_key=primary_key,
                    unique=bool(getattr(column, "unique", False)) or column.name in unique_index_columns,
                    default=_dbml_default(column),
                    references=ref,
                )
            )
            if ref is not None:
                relations.append(
                    RelationSchema(
                        source_table=table.name,
                        source_column=column.name,
                        target_table=ref[0],
                        target_column=ref[1],
                    )
                )
        tables.append(TableSchema(name=table.name, columns=tuple(columns)))

    return AppSchema(
        tables=tuple(tables),
        relations=tuple(relations),
        source=str(path),
        enums=enums,
    )


def schema_from_sql(path: str | Path) -> AppSchema:
    sql = Path(path).read_text()
    tables: list[TableSchema] = []
    relations: list[RelationSchema] = []
    named_enums = _sql_named_enums(sql)
    enums: list[EnumSchema] = list(named_enums.values())
    enum_names: set[str] = set(named_enums)

    for match in re.finditer(
        r"create\s+table\s+(?:if\s+not\s+exists\s+)?(?P<name>[\w\".]+)\s*\((?P<body>.*?)\)\s*;",
        sql,
        flags=re.IGNORECASE | re.DOTALL,
    ):
        table_name = _clean_identifier(match.group("name").split(".")[-1])
        parts = _split_sql_list(match.group("body"))
        columns: dict[str, ColumnSchema] = {}
        table_primary_keys: set[str] = set()
        table_unique_columns: set[str] = set()

        for part in parts:
            constraint = _strip_sql_constraint_name(part)
            lowered = constraint.strip().lower()
            if lowered.startswith("primary key"):
                table_primary_keys.update(_constraint_columns(constraint))
                continue
            if lowered.startswith("foreign key"):
                source_columns = _constraint_column_list(constraint)
                target = _sql_reference_target(constraint)
                if target:
                    target_table, target_columns = target
                    for index, source_column in enumerate(source_columns):
                        target_column = target_columns[index] if index < len(target_columns) else target_columns[0]
                        existing = columns.get(source_column)
                        columns[source_column] = _with_reference(
                            existing or ColumnSchema(source_column),
                            target_table,
                            target_column,
                        )
                        relations.append(
                            RelationSchema(
                                source_table=table_name,
                                source_column=source_column,
                                target_table=target_table,
                                target_column=target_column,
                            )
                        )
                continue
            if lowered.startswith("unique "):
                unique_columns = _constraint_columns(constraint)
                if len(unique_columns) == 1:
                    table_unique_columns.update(unique_columns)
                continue
            if lowered.startswith("check "):
                enum = _sql_check_enum(table_name, constraint)
                if enum is not None and enum.name not in enum_names:
                    enums.append(enum)
                    enum_names.add(enum.name)
                continue

            column = _parse_sql_column(part)
            if column is not None:
                enum = _sql_check_enum(table_name, part)
                if enum is not None:
                    if enum.name not in enum_names:
                        enums.append(enum)
                        enum_names.add(enum.name)
                    column = _with_type(column, enum.name)
                elif column.type_name in named_enums:
                    column = _with_type(column, column.type_name)
                columns[column.name] = column
                if column.references is not None:
                    relations.append(
                        RelationSchema(
                            source_table=table_name,
                            source_column=column.name,
                            target_table=column.references[0],
                            target_column=column.references[1],
                        )
                    )

        if table_primary_keys:
            for name in table_primary_keys:
                if name in columns:
                    existing = columns[name]
                    columns[name] = ColumnSchema(
                        name=existing.name,
                        type_name=existing.type_name,
                        nullable=False,
                        primary_key=True,
                        unique=existing.unique,
                        default=existing.default,
                        references=existing.references,
                        hidden=existing.hidden,
                        searchable=existing.searchable,
                        derived=existing.derived,
                        expression=existing.expression,
                        source_group=existing.source_group,
                    )

        for name in table_unique_columns:
            if name in columns:
                columns[name] = _with_unique(columns[name])

        tables.append(TableSchema(table_name, tuple(columns.values())))

    tables = _apply_sql_unique_indexes(sql, tables)
    tables, alter_relations = _apply_sql_alter_constraints(sql, tables)
    relations.extend(alter_relations)

    return AppSchema(
        tables=tuple(tables),
        relations=tuple(relations),
        source=str(path),
        enums=tuple(enums),
    )


def schema_from_ponyorm(path: str | Path) -> AppSchema:
    tree = ast.parse(textwrap.dedent(Path(path).read_text()), filename=str(path))
    entity_names = {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, ast.ClassDef) and _looks_like_pony_entity(node)
    }
    enum_values = {
        node.name: _python_enum_values(node)
        for node in ast.walk(tree)
        if isinstance(node, ast.ClassDef) and _looks_like_python_enum(node)
    }
    enums = tuple(
        EnumSchema(name, values)
        for name, values in enum_values.items()
        if values
    )
    tables: list[TableSchema] = []
    relations: list[RelationSchema] = []
    set_relations: dict[tuple[str, str], str] = {}

    for node in ast.walk(tree):
        if not isinstance(node, ast.ClassDef) or node.name not in entity_names:
            continue
        composite_primary_key = _pony_composite_key_fields(node)
        columns: list[ColumnSchema] = []
        for statement in node.body:
            if not isinstance(statement, ast.Assign) or len(statement.targets) != 1:
                continue
            target = statement.targets[0]
            if not isinstance(target, ast.Name) or not isinstance(statement.value, ast.Call):
                continue
            call_name = _call_name(statement.value.func)
            if call_name == "Set":
                target_entity = _pony_set_target(statement.value, entity_names)
                if target_entity is not None:
                    set_relations[(node.name, target_entity)] = target.id
                continue
            if call_name not in {"PrimaryKey", "Required", "Optional"}:
                continue
            type_name, target_entity = _pony_call_type(statement.value, entity_names, enum_values)
            if target_entity is not None:
                column_name = f"{target.id}_id"
                columns.append(
                    ColumnSchema(
                        name=column_name,
                        type_name="int",
                        nullable=call_name == "Optional",
                        primary_key=target.id in composite_primary_key,
                        references=(target_entity, "id"),
                    )
                )
                relations.append(
                    RelationSchema(
                        source_table=node.name,
                        source_column=column_name,
                        target_table=target_entity,
                    )
                )
                continue
            columns.append(
                ColumnSchema(
                    name=target.id,
                    type_name=type_name,
                    nullable=call_name == "Optional",
                    primary_key=call_name == "PrimaryKey" or target.id in composite_primary_key,
                    unique=_pony_kw_bool(statement.value, "unique"),
                    default=_pony_kw_value(statement.value, "default"),
                )
            )
        if not any(column.primary_key for column in columns):
            columns.insert(0, ColumnSchema("id", "int", nullable=False, primary_key=True))
        tables.append(TableSchema(node.name, tuple(columns)))

    table_names = {table.name for table in tables}
    existing_foreign_pairs = {
        (relation.source_table, relation.target_table)
        for relation in relations
    }
    association_pairs = set()
    for source, target in set_relations:
        if source not in table_names or target not in table_names:
            continue
        if (target, source) not in set_relations:
            continue
        if (source, target) in existing_foreign_pairs or (target, source) in existing_foreign_pairs:
            continue
        association_pairs.add(tuple(sorted((source, target))))

    for left, right in sorted(association_pairs):
        table_name = f"{_snake_name(left)}_{_snake_name(right)}"
        left_column = f"{_snake_name(left)}_id"
        right_column = f"{_snake_name(right)}_id"
        tables.append(
            TableSchema(
                table_name,
                (
                    ColumnSchema(
                        left_column,
                        "int",
                        nullable=False,
                        primary_key=True,
                        references=(left, "id"),
                    ),
                    ColumnSchema(
                        right_column,
                        "int",
                        nullable=False,
                        primary_key=True,
                        references=(right, "id"),
                    ),
                ),
            )
        )
        relations.extend(
            (
                RelationSchema(
                    source_table=table_name,
                    source_column=left_column,
                    target_table=left,
                    cardinality="many-to-many",
                ),
                RelationSchema(
                    source_table=table_name,
                    source_column=right_column,
                    target_table=right,
                    cardinality="many-to-many",
                ),
            )
        )

    return AppSchema(tables=tuple(tables), relations=tuple(relations), source=str(path), enums=enums)


def load_schema(path: str | Path, *, source_type: str | None = None) -> AppSchema:
    path = Path(path)
    source_type = (source_type or path.suffix.lstrip(".")).lower()
    if source_type in {"ag", "ags", "appgen", "dsl"}:
        from .dsl import schema_from_dsl_file

        return schema_from_dsl_file(path)
    if source_type == "dbml":
        return schema_from_dbml(path)
    if source_type in {"sql", "ddl"}:
        return schema_from_sql(path)
    if source_type in {"py", "pony", "ponyorm"}:
        return schema_from_ponyorm(path)
    raise ValueError(f"Unsupported schema source type: {source_type}")


def sqlalchemy_type(type_name: str):
    normalized = type_name.lower().strip()
    if normalized.endswith("[]"):
        return Text()
    normalized = normalized.split("(", 1)[0]
    if normalized in {"int", "integer", "serial", "smallint"}:
        return Integer()
    if normalized in {"bigint", "bigserial"}:
        return BigInteger()
    if normalized in {"bool", "boolean"}:
        return Boolean()
    if normalized in {"float", "real", "double", "double precision"}:
        return Float()
    if normalized in {"decimal", "numeric", "money"}:
        return Numeric()
    if normalized in {"text", "longtext", "mediumtext"}:
        return Text()
    if normalized in {"json", "jsonb"}:
        return Text()
    if normalized in {"date"}:
        return Date()
    if normalized in {"datetime", "timestamp", "timestamptz"}:
        return DateTime()
    if normalized in {"time"}:
        return Time()
    if normalized in {"blob", "binary", "bytea"}:
        return LargeBinary()
    return String()


def _dbml_refs_for_table(table) -> dict[str, tuple[str, str]]:
    refs: dict[str, tuple[str, str]] = {}
    for ref in table.get_refs():
        if getattr(ref.table1, "name", ref.table1) == table.name:
            target_table = getattr(ref.table2, "name", ref.table2)
            for source_column, target_column in zip(ref.col1, ref.col2):
                refs[source_column.name] = (target_table, target_column.name)
    return refs


def _dbml_single_column_unique_indexes(table) -> set[str]:
    unique_columns: set[str] = set()
    for index in getattr(table, "indexes", ()) or ():
        if not bool(getattr(index, "unique", False)):
            continue
        subject_names = tuple(getattr(index, "subject_names", ()) or ())
        if len(subject_names) == 1:
            unique_columns.add(str(subject_names[0]))
    return unique_columns


def _metadata_unique_columns(table) -> set[str]:
    unique_columns: set[str] = set()
    for constraint in getattr(table, "constraints", ()):
        if constraint.__class__.__name__ != "UniqueConstraint":
            continue
        columns = tuple(getattr(constraint, "columns", ()))
        if len(columns) == 1:
            unique_columns.add(columns[0].name)
    for index in getattr(table, "indexes", ()) or ():
        if not bool(getattr(index, "unique", False)):
            continue
        columns = tuple(getattr(index, "columns", ()))
        if len(columns) == 1:
            unique_columns.add(columns[0].name)
    return unique_columns


def _metadata_column_type(column, metadata: MetaData) -> str:
    enum_values = tuple(getattr(column.type, "enums", ()) or ())
    if enum_values:
        return getattr(column.type, "name", None) or _sql_enum_name(column.table.name, column.name)
    if getattr(metadata, "bind", None) is not None:
        return column.type.compile(dialect=metadata.bind.dialect)
    return column.type.__class__.__name__


def _metadata_column_default(column) -> str | None:
    if column.default is not None:
        return _clean_default_text(getattr(column.default, "arg", column.default))
    if column.server_default is not None:
        return _clean_default_text(getattr(column.server_default, "arg", column.server_default))
    return None


def _clean_default_text(value) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    while text.startswith("(") and text.endswith(")") and _balanced_wrapping_parens(text):
        text = text[1:-1].strip()
    postgres_cast = re.fullmatch(
        r"'(?P<value>(?:''|[^'])*)'::(?P<type>[\w\s\".]+(?:\[\])?)",
        text,
        flags=re.IGNORECASE,
    )
    if postgres_cast:
        return postgres_cast.group("value").replace("''", "'")
    postgres_quoted_cast = re.fullmatch(
        r'"(?P<value>(?:""|[^"])*)"::(?P<type>[\w\s\".]+(?:\[\])?)',
        text,
        flags=re.IGNORECASE,
    )
    if postgres_quoted_cast:
        return postgres_quoted_cast.group("value").replace('""', '"')
    if text.startswith("'") and text.endswith("'"):
        return text[1:-1].replace("''", "'")
    if text.startswith('"') and text.endswith('"'):
        return text[1:-1].replace('""', '"')
    return text


def _balanced_wrapping_parens(text: str) -> bool:
    depth = 0
    for index, char in enumerate(text):
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0 and index != len(text) - 1:
                return False
        if depth < 0:
            return False
    return depth == 0


def _dbml_default(column) -> str | None:
    value = getattr(column, "default", None)
    if value is None:
        return None
    return _clean_default_text(value)


def _split_sql_list(body: str) -> list[str]:
    parts: list[str] = []
    current: list[str] = []
    depth = 0
    for char in body:
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        if char == "," and depth == 0:
            part = "".join(current).strip()
            if part:
                parts.append(part)
            current = []
        else:
            current.append(char)
    part = "".join(current).strip()
    if part:
        parts.append(part)
    return parts


def _parse_sql_column(part: str) -> ColumnSchema | None:
    tokens = part.strip().split()
    if len(tokens) < 2:
        return None
    name = _clean_identifier(tokens[0])
    type_name = _sql_column_type_name(part)
    lowered = part.lower()
    primary_key = "primary key" in lowered
    nullable = "not null" not in lowered and not primary_key
    unique = " unique" in f" {lowered}"
    default = _sql_default(part)
    references = None
    ref = re.search(r"references\s+([\w\".]+)\s*\(([^)]+)\)", part, flags=re.IGNORECASE)
    if ref:
        references = (
            _clean_identifier(ref.group(1).split(".")[-1]),
            _clean_identifier(ref.group(2).split(",")[0]),
        )
    return ColumnSchema(
        name=name,
        type_name=type_name,
        nullable=nullable,
        primary_key=primary_key,
        unique=unique,
        default=default,
        references=references,
    )


def _sql_column_type_name(part: str) -> str:
    """Return the declared type from a column definition."""
    stripped = part.strip()
    match = re.match(r"(?P<name>\"(?:\"\"|[^\"])+\"|`[^`]+`|'[^']+'|[A-Za-z_][A-Za-z0-9_]*)\s+(?P<rest>.*)", stripped, flags=re.S)
    if not match:
        return "string"
    rest = match.group("rest").strip()
    boundary = re.search(
        r"\s+(not\s+null|null|primary\s+key|unique|default|check|references|constraint)\b",
        rest,
        flags=re.IGNORECASE,
    )
    type_text = rest[: boundary.start()].strip() if boundary else rest
    return _clean_sql_type_identifier(type_text)


def _sql_named_enums(sql: str) -> dict[str, EnumSchema]:
    """Return PostgreSQL CREATE TYPE ... AS ENUM declarations keyed by type."""
    enums: dict[str, EnumSchema] = {}
    for match in re.finditer(
        r"create\s+type\s+(?P<name>[\w\".]+)\s+as\s+enum\s*\((?P<values>.*?)\)\s*;",
        sql,
        flags=re.IGNORECASE | re.DOTALL,
    ):
        enum_name = _clean_sql_type_identifier(match.group("name"))
        values = tuple(
            _sql_literal_value(value)
            for value in _split_sql_list(match.group("values"))
            if value.strip()
        )
        enums[enum_name] = EnumSchema(enum_name, values)
    return enums


def _apply_sql_alter_constraints(
    sql: str, tables: list[TableSchema]
) -> tuple[list[TableSchema], list[RelationSchema]]:
    table_map = {table.name: table for table in tables}
    updated = {table.name: {column.name: column for column in table.columns} for table in tables}
    relations: list[RelationSchema] = []

    for match in re.finditer(
        r"alter\s+table\s+(?:only\s+)?(?P<table>[\w\".]+)\s+add\s+(?:constraint\s+[\w\"`']+\s+)?(?P<constraint>.*?);",
        sql,
        flags=re.IGNORECASE | re.DOTALL,
    ):
        table_name = _clean_identifier(match.group("table").split(".")[-1])
        if table_name not in updated:
            continue
        constraint = match.group("constraint").strip()
        lowered = constraint.lower()
        if lowered.startswith("primary key"):
            for column_name in _constraint_columns(constraint):
                if column_name in updated[table_name]:
                    updated[table_name][column_name] = _with_primary_key(updated[table_name][column_name])
            continue
        if lowered.startswith("unique "):
            unique_columns = _constraint_columns(constraint)
            if len(unique_columns) == 1:
                column_name = next(iter(unique_columns))
                if column_name in updated[table_name]:
                    updated[table_name][column_name] = _with_unique(updated[table_name][column_name])
            continue
        if lowered.startswith("foreign key"):
            target = _sql_reference_target(constraint)
            if not target:
                continue
            target_table, target_columns = target
            for index, source_column in enumerate(_constraint_column_list(constraint)):
                if source_column not in updated[table_name]:
                    continue
                target_column = target_columns[index] if index < len(target_columns) else target_columns[0]
                updated[table_name][source_column] = _with_reference(
                    updated[table_name][source_column],
                    target_table,
                    target_column,
                )
                relations.append(
                    RelationSchema(
                        source_table=table_name,
                        source_column=source_column,
                        target_table=target_table,
                        target_column=target_column,
                    )
                )

    return [
        TableSchema(table.name, tuple(updated[table.name].values()))
        for table in tables
        if table.name in table_map
    ], relations


def _apply_sql_unique_indexes(sql: str, tables: list[TableSchema]) -> list[TableSchema]:
    updated = {table.name: {column.name: column for column in table.columns} for table in tables}
    for match in re.finditer(
        r"create\s+unique\s+index\s+(?:if\s+not\s+exists\s+)?[\w\"`']+\s+on\s+(?P<table>[\w\".]+)(?:\s+using\s+\w+)?\s*\((?P<columns>[^)]+)\)\s*;",
        sql,
        flags=re.IGNORECASE | re.DOTALL,
    ):
        table_name = _clean_identifier(match.group("table").split(".")[-1])
        if table_name not in updated:
            continue
        columns = tuple(_clean_identifier(value.strip().split()[0]) for value in _split_sql_list(match.group("columns")))
        if len(columns) != 1:
            continue
        column_name = columns[0]
        if column_name in updated[table_name]:
            updated[table_name][column_name] = _with_unique(updated[table_name][column_name])
    return [
        TableSchema(table.name, tuple(updated[table.name].values()))
        for table in tables
    ]


def _constraint_columns(part: str) -> set[str]:
    return set(_constraint_column_list(part))


def _constraint_column_list(part: str) -> tuple[str, ...]:
    match = re.search(r"\(([^)]+)\)", part)
    if not match:
        return ()
    return tuple(_clean_identifier(value) for value in _split_sql_list(match.group(1)))


def _sql_reference_target(part: str) -> tuple[str, tuple[str, ...]] | None:
    match = re.search(
        r"references\s+([\w\".]+)\s*\(([^)]+)\)",
        part,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if not match:
        return None
    return (
        _clean_identifier(match.group(1).split(".")[-1]),
        tuple(_clean_identifier(value) for value in _split_sql_list(match.group(2))),
    )


def _clean_identifier(value: str) -> str:
    return value.strip().strip('"').strip("`").strip("'")


def _clean_sql_type_identifier(value: str) -> str:
    cleaned = value.strip()
    if "." in cleaned:
        cleaned = cleaned.split(".")[-1]
    return _clean_identifier(cleaned)


def _strip_sql_constraint_name(part: str) -> str:
    match = re.match(
        r"\s*constraint\s+[\w\"`']+\s+(?P<body>.*)",
        part,
        flags=re.IGNORECASE | re.DOTALL,
    )
    return match.group("body").strip() if match else part.strip()


def _sql_default(part: str) -> str | None:
    match = re.search(
        r"\bdefault\s+(?P<value>'(?:''|[^'])*'|\"(?:\"\"|[^\"])*\"|[A-Za-z_][A-Za-z0-9_]*(?:\([^)]*\))?|[-+]?[0-9]+(?:\.[0-9]+)?)",
        part,
        flags=re.IGNORECASE,
    )
    if not match:
        return None
    return _clean_default_text(match.group("value").strip())


def _sql_check_enum(table_name: str, part: str) -> EnumSchema | None:
    match = re.search(
        r"(?:check\s*)?\(?\s*(?P<column>[\w\"`']+)\s+in\s*\((?P<values>[^)]*)\)",
        part,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if not match:
        return None
    values = tuple(
        _sql_literal_value(value)
        for value in _split_sql_list(match.group("values"))
        if value.strip()
    )
    if not values:
        return None
    column_name = _clean_identifier(match.group("column"))
    return EnumSchema(_sql_enum_name(table_name, column_name), values)


def _sql_literal_value(value: str) -> str:
    value = value.strip()
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1].replace("''", "'")
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1].replace('""', '"')
    return value


def _sql_enum_name(table_name: str, column_name: str) -> str:
    return "".join(
        part.capitalize()
        for part in re.split(r"[^A-Za-z0-9]+", f"{table_name}_{column_name}")
        if part
    )


def _with_type(column: ColumnSchema, type_name: str) -> ColumnSchema:
    return ColumnSchema(
        name=column.name,
        type_name=type_name,
        nullable=column.nullable,
        primary_key=column.primary_key,
        unique=column.unique,
        default=column.default,
        references=column.references,
        hidden=column.hidden,
        searchable=column.searchable,
        derived=column.derived,
        expression=column.expression,
        source_group=column.source_group,
    )


def _with_unique(column: ColumnSchema) -> ColumnSchema:
    return ColumnSchema(
        name=column.name,
        type_name=column.type_name,
        nullable=column.nullable,
        primary_key=column.primary_key,
        unique=True,
        default=column.default,
        references=column.references,
        hidden=column.hidden,
        searchable=column.searchable,
        derived=column.derived,
        expression=column.expression,
        source_group=column.source_group,
    )


def _with_primary_key(column: ColumnSchema) -> ColumnSchema:
    return ColumnSchema(
        name=column.name,
        type_name=column.type_name,
        nullable=False,
        primary_key=True,
        unique=column.unique,
        default=column.default,
        references=column.references,
        hidden=column.hidden,
        searchable=column.searchable,
        derived=column.derived,
        expression=column.expression,
        source_group=column.source_group,
    )


def _with_reference(
    column: ColumnSchema, target_table: str, target_column: str
) -> ColumnSchema:
    return ColumnSchema(
        name=column.name,
        type_name=column.type_name,
        nullable=column.nullable,
        primary_key=column.primary_key,
        unique=column.unique,
        default=column.default,
        references=(target_table, target_column),
        hidden=column.hidden,
        searchable=column.searchable,
        derived=column.derived,
        expression=column.expression,
        source_group=column.source_group,
    )


def _looks_like_pony_entity(node: ast.ClassDef) -> bool:
    return any(_call_name(base) == "Entity" for base in node.bases)


def _looks_like_python_enum(node: ast.ClassDef) -> bool:
    return any(_call_name(base) == "Enum" for base in node.bases)


def _python_enum_values(node: ast.ClassDef) -> tuple[str, ...]:
    values: list[str] = []
    for statement in node.body:
        if not isinstance(statement, ast.Assign) or len(statement.targets) != 1:
            continue
        target = statement.targets[0]
        if not isinstance(target, ast.Name):
            continue
        if target.id.startswith("_"):
            continue
        if isinstance(statement.value, ast.Constant):
            values.append(str(statement.value.value))
        else:
            values.append(target.id)
    return tuple(values)


def _call_name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    if isinstance(node, ast.Constant):
        return str(node.value)
    return ""


def _pony_call_type(
    call: ast.Call,
    entity_names: Iterable[str],
    enum_values: dict[str, tuple[str, ...]] | None = None,
) -> tuple[str, str | None]:
    if not call.args:
        return "string", None
    first = call.args[0]
    enum_names = set(enum_values or {})
    type_text = _python_type_text(first)
    type_name = type_text.split(".")[-1]
    if type_name in entity_names:
        return "int", type_name
    if type_name in enum_names:
        return type_name, None
    if isinstance(first, ast.Constant) and isinstance(first.value, str):
        if first.value in entity_names:
            return "int", first.value
        if first.value in enum_names:
            return first.value, None
        return first.value, None
    return _python_type_name(type_text), None


def _pony_set_target(call: ast.Call, entity_names: Iterable[str]) -> str | None:
    if not call.args:
        return None
    first = call.args[0]
    if isinstance(first, ast.Name) and first.id in entity_names:
        return first.id
    if isinstance(first, ast.Constant) and isinstance(first.value, str) and first.value in entity_names:
        return first.value
    return None


def _pony_composite_key_fields(node: ast.ClassDef) -> set[str]:
    fields: set[str] = set()
    for statement in node.body:
        if not isinstance(statement, ast.Expr) or not isinstance(statement.value, ast.Call):
            continue
        if _call_name(statement.value.func) != "PrimaryKey":
            continue
        for arg in statement.value.args:
            name = _pony_attribute_name(arg)
            if name is not None:
                fields.add(name)
    return fields


def _pony_attribute_name(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    return None


def _snake_name(value: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", value).lower()


def _python_type_text(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        parent = _python_type_text(node.value)
        return f"{parent}.{node.attr}" if parent else node.attr
    if isinstance(node, ast.Constant):
        return str(node.value)
    return ""


def _python_type_name(name: str) -> str:
    normalized = name.split(".")[-1]
    return {
        "str": "string",
        "int": "int",
        "float": "float",
        "bool": "bool",
        "datetime": "datetime",
        "date": "date",
        "time": "time",
        "Decimal": "decimal",
        "LongStr": "text",
        "Json": "json",
        "bytes": "binary",
        "buffer": "binary",
        "UUID": "string",
    }.get(normalized, normalized or "string")


def _pony_kw_bool(call: ast.Call, name: str) -> bool:
    for keyword in call.keywords:
        if keyword.arg == name and isinstance(keyword.value, ast.Constant):
            return bool(keyword.value.value)
    return False


def _pony_kw_value(call: ast.Call, name: str) -> str | None:
    for keyword in call.keywords:
        if keyword.arg != name:
            continue
        return _python_literal_value(keyword.value)
    return None


def _python_literal_value(node: ast.AST) -> str | None:
    if isinstance(node, ast.Constant):
        if node.value is None:
            return None
        return str(node.value)
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        value = _python_literal_value(node.operand)
        return f"-{value}" if value is not None else None
    return None
