"""Every column a generated view names must be a mapper property.

`generate_view_code` and `write_api_file` write FAB views whose
`list_columns`, `show_columns`, `add_columns`, `edit_columns`,
`search_columns` and `include_columns` are lists of *attribute names*. FAB
resolves each one against the SQLAlchemy mapper: `SQLAInterface.list_columns`
is a dict keyed by the mapper property name (`interface.py:65`:
`self.list_columns[col_name] = obj.__mapper__.columns[col_name]`), and a name
the mapper does not have is dropped from the view.

That failure is silent. The view answers HTTP 200, the other columns render,
and the missing one is simply absent from the table and the form. Measured
2026-10-12 against FAB 5.2.2 with a real app: `list_columns` naming the
database column `metadata` rendered every other field and returned 200 while
the value never appeared.

`hasattr` cannot guard it. `dom_order_channel_context.metadata` is reserved by
the Declarative API, so the model emitter writes the attribute as `metadata_`
while keeping the database column name via `Column('metadata', ...)`. On the
model class `hasattr(Ctx, 'metadata')` is **True** and resolves to SQLAlchemy's
own `MetaData` object, so a `hasattr` check passes and the column is still
blank.

`_model_attribute_name` is the single name-mapping the view, API, GraphQL and
dashboard emitters all read. It now routes through `_declarative_attribute_name`,
the same helper the model emitter uses, so the two cannot drift. This gate holds
that: it parses the emitted view and API source, reads each class's
`SQLAInterface(Model)` target, and asserts every column name in every column
list is a property of that model's mapper.
"""

from __future__ import annotations

import ast
import types

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

from pyAppGen import gen
from pyAppGen.pbc import IMPLEMENTED_PBC_KEYS

# `tests/ci` has no `__init__.py`, so pytest puts this directory on `sys.path`
# and the sibling is importable as a top-level module. Its helpers are the ones
# this gate needs: the exact header the writer prepends, the mixin stand-in, and
# the contract-derived schema, all of which must match production.
from test_generated_models_are_importable import (
    _HEADER,
    _install_mixin_stub,
    _schema_for,
)

# The assignments FAB reads as column lists. `show_exclude_columns` and friends
# hold names too, but they name what to *remove*, so a stale name there is inert
# rather than data-losing, and FAB accepts a module-level `hide_list` name for
# them (which is why they are excluded: they are often not literals at all).
_COLUMN_ATTRIBUTES = frozenset(
    {
        "list_columns",
        "show_columns",
        "add_columns",
        "edit_columns",
        "search_columns",
        "include_columns",
        "order_columns",
        "exclude_columns",
    }
)


def _literal_names(node: ast.expr) -> list[str] | None:
    """Flatten a column-list expression into the names it contains.

    The emitter writes these as `['a', 'b'] + ['c']`, so the value is an `Add`
    chain rather than one literal. Anything else (a bare name like
    `hide_list`) is not statically resolvable and is skipped by the caller.
    """
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        left = _literal_names(node.left)
        right = _literal_names(node.right)
        if left is None or right is None:
            return None
        return left + right
    try:
        value = ast.literal_eval(node)
    except (ValueError, SyntaxError):
        return None
    if isinstance(value, (list, tuple)):
        return [item for item in value if isinstance(item, str)]
    return None


def _emitted_views(key: str, tmp_path) -> tuple[dict[str, set[str]], list[tuple[str, str, str]]]:
    """Return the mapper properties per model, and every column name emitted.

    The schema is the contract's, and the model source is the exact text
    `write_model_file` writes, so the properties are the ones the generated app
    actually has at runtime.
    """
    schema = _schema_for(key)
    gen.engine = create_engine("sqlite://")
    gen.metadata = schema.to_metadata()
    gen.Base = declarative_base()

    module = types.ModuleType(f"_models_{key}")
    source = _HEADER + gen.generate_model_code(schema)
    exec(compile(source, f"<models {key}>", "exec"), module.__dict__)
    properties = {
        name: {prop.key for prop in obj.__mapper__.attrs}
        for name, obj in vars(module).items()
        if hasattr(obj, "__mapper__")
    }

    # `write_api_file` writes to disk rather than returning text, so the API
    # half is read back from a real write. `generate_view_code` returns text.
    gen.write_api_file(tmp_path, schema)
    api_text = (tmp_path / "api.py").read_text()

    emitted: list[tuple[str, str, str]] = []
    for text in (gen.generate_view_code(schema), api_text):
        tree = ast.parse(text)
        for node in ast.walk(tree):
            if not isinstance(node, ast.ClassDef):
                continue
            model = _interface_target(node)
            if model not in properties:
                continue
            for statement in node.body:
                if not isinstance(statement, ast.Assign):
                    continue
                targets = {
                    target.id for target in statement.targets if isinstance(target, ast.Name)
                }
                if not targets & _COLUMN_ATTRIBUTES:
                    continue
                for name in _literal_names(statement.value) or []:
                    emitted.append((node.name, model, name))
    return properties, emitted


def _interface_target(node: ast.ClassDef) -> str | None:
    """Return the model class named by `datamodel = SQLAInterface(Model)`.

    The interface is bound in the class body rather than as a base, so the class
    bases say nothing about which model the view reads.
    """
    for child in ast.walk(node):
        if isinstance(child, ast.Call) and getattr(child.func, "id", "") == "SQLAInterface":
            if child.args and isinstance(child.args[0], ast.Name):
                return child.args[0].id
    return None


_install_mixin_stub()


@pytest.mark.parametrize("key", IMPLEMENTED_PBC_KEYS)
def test_every_emitted_column_is_a_mapper_property(key: str, tmp_path) -> None:
    """A name the mapper does not have is a column the view silently drops."""
    properties, emitted = _emitted_views(key, tmp_path)
    assert emitted, f"{key} emitted no column lists at all, so this proves nothing"
    unknown = sorted(
        {(view, model, name) for view, model, name in emitted if name not in properties[model]}
    )
    assert not unknown, f"{key} names columns the mapper does not have: {unknown[:10]}"


def test_the_check_reads_a_real_volume_of_columns(tmp_path) -> None:
    """Guard against the filter matching nothing and reporting a clean zero.

    A gate whose discovery is wrong passes forever. This asserts the measured
    set is large enough to be the real one: 147 packages, each with several
    views and several column lists.
    """
    total = sum(
        len(_emitted_views(key, tmp_path / key)[1]) for key in IMPLEMENTED_PBC_KEYS
    )
    assert total > 100_000, f"only {total} column names measured; the discovery is too narrow"


def test_the_reserved_name_is_the_attribute_not_the_column(tmp_path) -> None:
    """The one reserved column must be emitted as `metadata_`, not `metadata`.

    This is the defect's own shape, asserted directly so the parametrized test
    above cannot pass by the table being absent from the measured set.
    """
    properties, emitted = _emitted_views("dom", tmp_path)
    assert "DomOrderChannelContext" in properties
    assert "metadata_" in properties["DomOrderChannelContext"]
    assert "metadata" not in properties["DomOrderChannelContext"]
    named = {name for _, model, name in emitted if model == "DomOrderChannelContext"}
    assert "metadata_" in named
    assert "metadata" not in named


def test_the_view_check_canaries_against_the_prefix_mapping(monkeypatch, tmp_path) -> None:
    """Point the check at the pre-fix mapping and confirm it reports the defect.

    Exit 0 from a check that has never been watched fail is not evidence. The
    canary restores `_model_attribute_name`'s old body (no reserved-name
    suffix) while leaving the model emitter correct, which is exactly the state
    the defect shipped in, and requires the check to name it.
    """
    from pyAppGen.gen import underscore

    def prefix_only(column):
        if column.references is not None:
            return underscore(column.references[0])
        return underscore(column.name)

    monkeypatch.setattr(gen, "_model_attribute_name", prefix_only)
    properties, emitted = _emitted_views("dom", tmp_path)
    unknown = {(view, model, name) for view, model, name in emitted if name not in properties[model]}
    assert unknown, "the check does not see a view naming a non-property column"
    # Every hit must be the reserved column on the one table that has it, and
    # both emitters must contribute: the model view and the REST API class.
    assert {name for _, _, name in unknown} == {"metadata"}
    assert {model for _, model, _ in unknown} == {"DomOrderChannelContext"}
    views_hit = {view for view, _, _ in unknown if view.endswith("ModelView")}
    api_hit = {view for view, _, _ in unknown if view.endswith("RestApi")}
    assert views_hit, "the canary did not reach the view emitter"
    assert api_hit, "the canary did not reach the API emitter"


def test_the_declarative_attribute_mapping_has_one_definition() -> None:
    """The model emitter and the name mapper must share one mapping.

    They diverged once, which is how a view came to name a column the model had
    renamed. Asserting the shared helper is used on both sides keeps a future
    edit from re-splitting them.
    """
    import inspect

    model_source = inspect.getsource(gen.generate_model_code)
    name_source = inspect.getsource(gen._model_attribute_name)
    assert "_declarative_attribute_name" in model_source
    assert "_declarative_attribute_name" in name_source
    assert gen._declarative_attribute_name("metadata") == "metadata_"
    assert gen._declarative_attribute_name("tenant") == "tenant"
