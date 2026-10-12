"""A generated app's `views.py` must execute.

`write_view_file` is the only writer of a generated app's `views.py`, and the
file is imported at startup: it does `from app.models import *`, names
`hide_list` at class-body level three times (`show_exclude_columns`,
`add_exclude_columns`, `edit_exclude_columns`), and registers every view through
`appbuilder.add_view`. A module-level name that does not resolve raises at
import, so the whole app fails to start.

`hide_list` is not written by the emitter; it arrives through the copied
support file (`pyAppGen/view_mixins.py:9`, copied verbatim by
`copy_support_files`). That coupling is invisible from either file alone, and
nothing asserted it: `tests/test_main.py` checks that `views.py` *contains*
certain strings, which passes whether or not the module can be imported.

This is the same gap the model emitter shipped four defects through, one file
over. The check executes the artifact rather than reading it: it writes the
real `models.py`, `views.py` and support files, stands up the `app` package the
header imports from, and execs the module.

Note what this check does *not* cover: naming a column the mapper does not have
is silent, so exec passes with that defect present (verified: restoring the
pre-fix name-mapping leaves this check at 147/147). That is
`test_generated_views_name_real_attributes.py`'s job. The two are complementary,
and each canaries on its own defect.
"""

from __future__ import annotations

import sys
import types

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

from pyAppGen import gen
from pyAppGen.pbc import IMPLEMENTED_PBC_KEYS

from test_generated_models_are_importable import (
    _install_mixin_stub,
    _schema_for,
)

_install_mixin_stub()


def _app_package(output_dir) -> types.ModuleType:
    """Stand up the `app` package the generated header imports from.

    The header does `from app.models import *`, `from app.view_mixins import *`,
    `from app import appbuilder`, and `from app.extensions import ...`. Each is
    supplied from the real emitted file where one exists, so a failure is the
    emitter's rather than the harness's.
    """
    app_package = sys.modules["app"]
    app_package.__path__ = [str(output_dir)]

    models = types.ModuleType("app.models")
    exec(
        compile((output_dir / "models.py").read_text(), "app/models.py", "exec"),
        models.__dict__,
    )
    sys.modules["app.models"] = models
    setattr(app_package, "models", models)

    # `view_mixins.py` is the copied support file and the only source of
    # `hide_list`. Its own imports may not resolve here (it pulls flask_babel),
    # so a failure to exec it is tolerated only when `hide_list` still lands:
    # that is the name the generated views actually need.
    view_mixins = types.ModuleType("app.view_mixins")
    try:
        exec(
            compile(
                (output_dir / "view_mixins.py").read_text(),
                "app/view_mixins.py",
                "exec",
            ),
            view_mixins.__dict__,
        )
    except Exception:  # noqa: BLE001 - tolerated, and safe: see below
        # Tolerating an import failure here cannot hide the thing that matters.
        # `hide_list` is the only name the generated views need from this file,
        # and it arrives through the star import, so a file that fails to import
        # leaves the name absent and the views module raises `NameError: name
        # 'hide_list' is not defined` — which names the problem. The canary test
        # below exercises exactly that path. The reason to tolerate at all is
        # that this file's own imports are not the subject under test.
        pass
    sys.modules["app.view_mixins"] = view_mixins
    setattr(app_package, "view_mixins", view_mixins)

    extensions = types.ModuleType("app.extensions")
    setattr(extensions, "before_save_row", lambda _table, row: row)
    setattr(extensions, "after_save_row", lambda _table, _row: None)
    sys.modules["app.extensions"] = extensions

    builder_module = types.ModuleType("app.appbuilder")

    class _Builder:
        class app:
            config = {"SQLALCHEMY_DATABASE_URI": "sqlite://"}

        def add_view(self, *args, **kwargs):
            return None

        def add_separator(self, *args, **kwargs):
            return None

    setattr(builder_module, "appbuilder", _Builder())
    sys.modules["app.appbuilder"] = builder_module
    setattr(app_package, "appbuilder", builder_module.appbuilder)
    return app_package


def _execute_views(key: str, tmp_path):
    """Write a generated app's files for ``key`` and exec its `views.py`."""
    schema = _schema_for(key)
    gen.engine = create_engine("sqlite://")
    gen.metadata = schema.to_metadata()
    gen.Base = declarative_base()

    gen.write_model_file(tmp_path, schema)
    gen.write_view_file(tmp_path, schema)
    gen.copy_support_files(tmp_path)
    _app_package(tmp_path)

    module = types.ModuleType(f"app.views.{key}")
    source = (tmp_path / "views.py").read_text()
    exec(compile(source, "app/views.py", "exec"), module.__dict__)
    return module


@pytest.mark.parametrize("key", IMPLEMENTED_PBC_KEYS)
def test_the_generated_views_module_executes(key: str, tmp_path) -> None:
    """A module-level name that does not resolve makes the app unstartable."""
    module = _execute_views(key, tmp_path)
    views = [
        name
        for name, value in vars(module).items()
        if isinstance(value, type) and name.endswith("ModelView")
    ]
    assert views, f"{key} defined no view classes, so the exec proves nothing"


def test_the_exec_check_canaries_against_a_missing_module_level_name(tmp_path) -> None:
    """Point the check at the defect's own shape and confirm it fails.

    `hide_list` is the one name the generated views need from the copied support
    file. Removing it from the copy must make the module raise `NameError`,
    which proves the check is executing the real artifact and not a stub.
    """
    original = gen.copy_support_files

    def copy_without_hide_list(output_dir):
        original(output_dir)
        path = output_dir / "view_mixins.py"
        text = path.read_text()
        target = "hide_list = ['created_by', 'changed_by', 'created_on', 'changed_on']"
        assert target in text, "canary target not found in view_mixins.py"
        path.write_text(text.replace(target, ""))

    gen.copy_support_files = copy_without_hide_list
    try:
        with pytest.raises(NameError, match="hide_list"):
            _execute_views("dam_core", tmp_path)
    finally:
        gen.copy_support_files = original


def test_the_exec_check_is_blind_to_a_wrong_column_name(tmp_path, monkeypatch) -> None:
    """Exec cannot see the silent defect, and this records that boundary.

    Restoring the pre-fix name-mapping leaves `views.py` naming a column the
    mapper does not have. The module still executes, because FAB drops the name
    at request time rather than at import. Asserting the blindness keeps the two
    gates from being collapsed into one on the assumption that either would do.
    """
    from pyAppGen.gen import underscore

    def prefix_only(column):
        if column.references is not None:
            return underscore(column.references[0])
        return underscore(column.name)

    monkeypatch.setattr(gen, "_model_attribute_name", prefix_only)
    module = _execute_views("dom", tmp_path)
    views = [
        name
        for name, value in vars(module).items()
        if isinstance(value, type) and name.endswith("ModelView")
    ]
    assert views, "the module stopped executing, so this boundary changed"
