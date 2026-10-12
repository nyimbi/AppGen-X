"""The ORM model file the generator emits must be a module Python can run.

`write_model_file` (`gen.py:511`) is the only thing that writes a generated
app's `models.py`, and the whole app depends on it: `app/views.py` does
`from app.models import *`, and `flask fab create-db` calls
`Model.metadata.create_all(engine)` over exactly these classes. Nothing in
`tests/` named `generate_model_code` or `write_model_file`, so four defects in
that one emitter path shipped to all 147 packages and no gate saw any of them.
Measured before the repair: **0 of 147** emitted modules executed.

The four defects, each with the input that exposed it:

* The column type was a *string*: the emitter lower-cased a dialect-compiled
  spelling and passed it through `map_pgsql_datatypes`, a legacy Postgres-only
  mapper. SQLite (which `generate_app_from_schema` binds during generation)
  prints `DATETIME`, which fell through every branch and came back as the
  lowercase `datetime`, so the file asked for the *module*: `Column(datetime,
  ...)` raises `ArgumentError`. `numeric(18, 4)`, `serial`, and `character
  varying(255)` came back as themselves, and `BigInteger`/`Currency` as names
  the file's own import header never imports.
* `timestamp` returned `"DateTime, server_default=text('NOW())'"`, whose
  parentheses never balance. The emitted file is a `SyntaxError`.
* Every primary key was written `autoincrement=True`. SQLAlchemy infers that for
  a single integer key and declines it otherwise, which is right in both cases;
  stating it breaks a TEXT key (313 tables, `Column type TEXT ... is not
  compatible with autoincrement=True`) and a composite integer key (5 tables,
  `Only one Column may be marked autoincrement=True` under Postgres).
* A column named `metadata` became a class attribute of that name, which the
  Declarative API reserves: `InvalidRequestError` at class-creation time, so
  `dom_order_channel_context` made the whole module unimportable.

Each check below is canaried against the defect's own shape, so none passes
vacuously. The module is executed with a stand-in for `app.model_mixins` (see
`_MIXIN_STAND_IN`) because the real one imports `Markup` from Flask, which the
FAB 5.2.2 installed on this machine no longer exports; the stand-in supplies the
same names so an exec failure is the emitter's, not the harness's.
"""

from __future__ import annotations

import ast
import sys

import pytest
import sqlalchemy.dialects.postgresql as pg
from sqlalchemy import Column, Integer, Text, create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.schema import CreateTable

from pyAppGen import gen
from pyAppGen.pbc import IMPLEMENTED_PBC_KEYS, pbc_implementation_contract
from pyAppGen.schema import AppSchema, ColumnSchema, TableSchema

# `generate_model_code` returns only the class bodies; `write_model_file`
# prepends this header. Reproduce it rather than importing it, so the harness
# compiles the artifact the app ships and not a fragment of it. The header text
# is asserted against `write_model_file` itself in
# `test_the_harness_header_matches_the_writer`.
_HEADER = (
    "from sqlalchemy import (Column, Integer, BigInteger, String, ForeignKey, "
    "DateTime, Boolean, Float, Text, Date, Time, Numeric, Interval, Enum, "
    "LargeBinary, JSON)\n"
    "from sqlalchemy.orm import relationship, backref\n"
    "from sqlalchemy.ext.associationproxy import association_proxy\n"
    "from flask_appbuilder import Model\n\n"
    "from app.model_mixins import *\n"
    "Base = Model\n\n"
)

_MIXIN_STAND_IN = """
from datetime import datetime, date, time, timedelta
from sqlalchemy import Column, String, Text, text
from sqlalchemy.dialects.postgresql import *


class RefTypeMixin:
    # Faithful to `pyAppGen/model_mixins.py:146`, which declares these four as
    # real columns. A stand-in of `pass` would under-report the mapper's
    # properties, so a view naming `name` would read as a defect when it is the
    # mixin supplying it.
    name = Column(String(100), unique=True, nullable=False, index=True)
    code = Column(String(20), default="0000", index=True)
    description = Column(String(100))
    notes = Column(Text, default="")


class TransientMixin:
    pass


class PlaceMixin:
    pass


class DocMixin:
    pass


class PersonMixin:
    pass
"""


def _schema_for(key: str) -> AppSchema:
    """Rebuild the AppSchema `generate_app_from_schema` would hand the emitter.

    The contract's owned tables are the source the generator reads, so building
    the schema from anything else would test a different input than production.
    """
    contract = pbc_implementation_contract(key)
    tables = []
    for table in contract["owned_schema"]["tables"]:
        columns = tuple(
            ColumnSchema(
                name=field["name"],
                type_name=field["type"],
                nullable=not field.get("required", False),
                primary_key=bool(field.get("primary_key")),
            )
            for field in table["fields"]
        )
        tables.append(TableSchema(name=table["owned_table"], columns=columns))
    return AppSchema(app_name=key, tables=tuple(tables))


def _emitted_source(key: str) -> str:
    """Return the exact text `write_model_file` writes for ``key``."""
    schema = _schema_for(key)
    gen.engine = create_engine("sqlite://")
    gen.metadata = schema.to_metadata()
    gen.Base = declarative_base()
    return _HEADER + gen.generate_model_code(schema)


def _install_mixin_stub() -> None:
    """Put a stand-in `app.model_mixins` on `sys.modules`.

    The emitted header does `from app.model_mixins import *`, which is the
    generated app's own module and does not exist here. The real
    `pyAppGen/model_mixins.py` cannot stand in either: it imports `Markup` from
    Flask, which the FAB 5.2.2 installed on this machine no longer exports. The
    stub supplies the names the emitted module actually resolves through the
    star import, so an exec failure is the emitter's rather than the harness's.
    """
    if "app.model_mixins" in sys.modules:
        return
    import types

    app_package = sys.modules.setdefault("app", types.ModuleType("app"))
    mixins = types.ModuleType("app.model_mixins")
    exec(compile(_MIXIN_STAND_IN, "<app.model_mixins>", "exec"), mixins.__dict__)
    sys.modules["app.model_mixins"] = mixins
    setattr(app_package, "model_mixins", mixins)


def _execute(source: str, name: str) -> tuple[dict, str | None]:
    """Exec ``source`` with the mixin surface, returning the namespace or error.

    Returns ``(namespace, None)`` on success and ``({}, "Kind: message")`` on
    failure, so a caller can report the defect without a traceback.
    """
    _install_mixin_stub()
    namespace: dict = {}
    try:
        exec(compile(source, f"<{name}>", "exec"), namespace)
    except Exception as exc:
        return {}, f"{type(exc).__name__}: {exc}"
    return namespace, None


def _problems(key: str) -> list[str]:
    """Return every way ``key``'s emitted model module fails, empty if it works."""
    try:
        source = _emitted_source(key)
    except Exception as exc:
        return [f"emit:{type(exc).__name__}: {exc}"]

    problems: list[str] = []
    try:
        ast.parse(source)
    except SyntaxError as exc:
        return [f"parse:{exc.msg} line {exc.lineno}"]

    namespace, error = _execute(source, key)
    if error is not None:
        return [f"exec:{error}"]

    base = namespace.get("Base")
    if base is None:
        return ["exec:no Base in the emitted namespace"]
    for table_name, table in base.metadata.tables.items():
        try:
            CreateTable(table).compile(dialect=pg.dialect())
        except Exception as exc:
            problems.append(f"ddl:{table_name}:{type(exc).__name__}: {exc}")
    return problems


_CACHE: dict[str, list[str]] = {}


def _cached(key: str) -> list[str]:
    """Emit and execute ``key`` once per session.

    Rebuilding the contract for all 147 keys takes ~12s and the emit on top of
    that is the bulk of the run, so each key is measured once and the three
    parametrized checks below read the same result.
    """
    if key not in _CACHE:
        _CACHE[key] = _problems(key)
    return _CACHE[key]


@pytest.mark.parametrize("key", IMPLEMENTED_PBC_KEYS)
def test_the_emitted_model_module_parses(key: str) -> None:
    """A generated `models.py` that is a `SyntaxError` cannot be imported at all."""
    problems = [problem for problem in _cached(key) if problem.startswith("parse:")]
    assert not problems, (key, problems)


@pytest.mark.parametrize("key", IMPLEMENTED_PBC_KEYS)
def test_the_emitted_model_module_executes(key: str) -> None:
    """Executing the module is what `from app.models import *` does.

    A type name the header does not import, or a class attribute the Declarative
    API reserves, raises here and nowhere earlier.
    """
    problems = [
        problem
        for problem in _cached(key)
        if problem.startswith(("exec:", "emit:"))
    ]
    assert not problems, (key, problems)


@pytest.mark.parametrize("key", IMPLEMENTED_PBC_KEYS)
def test_the_emitted_model_ddl_compiles(key: str) -> None:
    """`flask fab create-db` runs `create_all`, so the DDL has to compile.

    Compiled against the Postgres dialect rather than the SQLite one generation
    binds, because Postgres is what a generated app deploys against and the
    composite-key `autoincrement` error only surfaces there.
    """
    problems = [problem for problem in _cached(key) if problem.startswith("ddl:")]
    assert not problems, (key, problems[:3])


def test_the_emitted_module_is_not_vacuously_empty() -> None:
    """Guard the checks above against an emitter that returns nothing.

    Every parametrized check passes on an empty string, so the suite would go
    green if `generate_model_code` ever returned `""`. The three reference PBCs
    must emit a class for each of their owned tables.
    """
    for key in ("dam_core", "gl_core", "ar_credit"):
        contract = pbc_implementation_contract(key)
        owned = {table["owned_table"] for table in contract["owned_schema"]["tables"]}
        tree = ast.parse(_emitted_source(key))
        emitted = {node.name for node in tree.body if isinstance(node, ast.ClassDef)}
        assert len(emitted) >= len(owned), (key, len(emitted), len(owned))


def test_a_reserved_declarative_name_keeps_its_database_column() -> None:
    """`dom_order_channel_context.metadata` is the only reserved-name column.

    The fix renames the *attribute* and names the column positionally, so the
    table still has a `metadata` column. A fix that renamed the column instead
    would silently change the schema, so both halves are asserted.
    """
    source = _emitted_source("dom")
    assert "metadata_ = Column('metadata'" in source, (
        "the attribute must carry the suffix while the column keeps its name"
    )
    namespace, error = _execute(source, "dom")
    assert error is None, error
    table = namespace["Base"].metadata.tables["dom_order_channel_context"]
    assert "metadata" in table.columns, sorted(table.columns.keys())
    assert hasattr(table.columns["metadata"], "name")


def test_the_harness_header_matches_the_writer(tmp_path) -> None:
    """The header above is a copy of `write_model_file`'s; copies drift.

    If the writer's import list grows and this file's does not, the checks here
    would pass on a module the app cannot run. Rather than read the writer's
    source (which splits the import list across two `f.write` calls), write the
    real file and compare its head.
    """
    schema = _schema_for("gl_core")
    gen.engine = create_engine("sqlite://")
    gen.metadata = schema.to_metadata()
    gen.Base = declarative_base()
    gen.write_model_file(tmp_path, schema)
    written = (tmp_path / "models.py").read_text()
    assert written.startswith(_HEADER), (
        "`write_model_file`'s header no longer matches this file's _HEADER; "
        f"the checks here would test a module the app does not ship.\n"
        f"written head: {written[: len(_HEADER) + 40]!r}"
    )


def _exec_module(body: str) -> str | None:
    """Exec a bare class body against a fresh declarative base; None if it works."""
    base = declarative_base()
    namespace = {"Base": base, "Column": Column, "Integer": Integer, "Text": Text}
    try:
        exec(compile(body, "<canary>", "exec"), namespace)
    except Exception as exc:
        return f"{type(exc).__name__}: {exc}"
    for table in base.metadata.tables.values():
        try:
            CreateTable(table).compile(dialect=pg.dialect())
        except Exception as exc:
            return f"{type(exc).__name__}: {exc}"
    return None


def test_the_exec_check_canaries_on_a_leaked_type_name() -> None:
    """The `datetime` module leak: `Column(datetime, ...)` raises at exec."""
    failure = _exec_module(
        "class A(Base):\n"
        "    __tablename__ = 'a'\n"
        "    id = Column(Integer, primary_key=True)\n"
        "    seen_at = Column(datetime, nullable=False)\n"
    )
    assert failure is not None and failure.startswith("NameError"), failure


def test_the_exec_check_canaries_on_a_reserved_attribute() -> None:
    """A class attribute named `metadata` raises before any DDL is reached."""
    failure = _exec_module(
        "class B(Base):\n"
        "    __tablename__ = 'b'\n"
        "    id = Column(Integer, primary_key=True)\n"
        "    metadata = Column(Text, nullable=False)\n"
    )
    assert failure is not None and failure.startswith("InvalidRequestError"), failure


def test_the_ddl_check_canaries_on_a_text_primary_key_autoincrement() -> None:
    """A TEXT key with a stated `autoincrement=True` is the 313-table defect."""
    failure = _exec_module(
        "class C(Base):\n"
        "    __tablename__ = 'c'\n"
        "    code = Column(Text, primary_key=True, nullable=False, autoincrement=True)\n"
    )
    assert failure is not None and "autoincrement" in failure, failure


def test_the_ddl_check_canaries_on_a_composite_autoincrement_key() -> None:
    """Two stated autoincrements is `Only one Column may be marked` on Postgres."""
    failure = _exec_module(
        "class D(Base):\n"
        "    __tablename__ = 'd'\n"
        "    a = Column(Integer, primary_key=True, autoincrement=True)\n"
        "    b = Column(Integer, primary_key=True, autoincrement=True)\n"
    )
    assert failure is not None and "Only one Column" in failure, failure


def test_the_type_expression_maps_the_subclass_chain_correctly() -> None:
    """`Float ⊂ Numeric` and `Text ⊂ String`, so the narrower type is tested first.

    An ordering slip here is invisible in the counts: the whole catalog's
    `decimal` columns would silently become `Float` and every `text` column
    `String`, and every check above would still pass.
    """
    from sqlalchemy import BigInteger, Float, Numeric, String

    def expression(type_object):
        column = Column("probe", type_object)
        return gen._fab_type_expression(column)

    assert expression(BigInteger()) == "BigInteger"
    assert expression(Float()) == "Float"
    assert expression(Numeric(18, 4)) == "Numeric"
    assert expression(Text()) == "Text"
    assert expression(String(255)) == "String"


def test_the_emitter_no_longer_calls_the_legacy_type_mapper() -> None:
    """`map_pgsql_datatypes` returns dialect spellings, not Python names.

    Re-introducing it is how the defect arrived, so its absence is asserted
    rather than left to review.
    """
    import inspect

    source = inspect.getsource(gen)
    assert "map_pgsql_datatypes" not in source.replace(
        "`map_pgsql_datatypes`, a legacy Postgres-only string mapper", ""
    ), "the legacy string mapper is back in the emitter path"
