"""Every view module the generator emits must be mounted in the app.

A generated app's `__init__.py` is the copied support file
(`pyAppGen/init.py`), and it is the only place a generated view reaches the
running app: the module defines `register_<name>(appbuilder)`, and `__init__.py`
imports it and calls it. A module that is emitted but never called is dead
weight, and worse, it is a *screen the product documents and the app does not
serve*.

Measured on a real generated app before this test existed: 70 modules defined a
`register_<name>(appbuilder)` mount, and 68 were called. The two orphans were
`code_review.py` (59 KB, a code-review cockpit with a workbench and a release
gate) and `i18n.py` (24 KB, the localization screen). Both ship in every
generated app with their templates; nothing mounted either, and no other code
path called them, so the screens were unreachable in fact while reachable in
principle.

The coupling is invisible from either side alone: `init.py` is a static,
hand-maintained file copied verbatim (`gen.py:copy_support_files`), and the
emitters that write the modules live thousands of lines away in `gen.py`. Adding
a module without adding its mount is silent, which is how these two survived.

The check reads the *generated* app, not the template, so it exercises the
emitter-and-template pair the way the app consumes them.
"""

from __future__ import annotations

import ast
import shutil
from pathlib import Path

import pytest

from pyAppGen.dsl import schema_from_dsl
from pyAppGen.gen import generate_app_from_schema
from pyAppGen.pbc import pbc_composition_dsl

COMPOSITION = ("dam_core", "gl_core", "ar_credit")

# Below this the scan is not looking at a real app, so a pass would be vacuous.
_MIN_MOUNTS = 50


@pytest.fixture(scope="module")
def generated_app(tmp_path_factory) -> Path:
    output = tmp_path_factory.mktemp("app-mounts") / "app"
    dsl = pbc_composition_dsl(COMPOSITION, app_name="LegoLedger")
    schema = schema_from_dsl(dsl, source_name="lego.appgen")
    generate_app_from_schema(schema, output)
    return output


def _mount_functions(app_dir: Path) -> dict[str, str]:
    """Map each `register_<name>(appbuilder)` to the module that defines it.

    Only the mount convention counts: a function whose first parameter is
    `appbuilder`. That is what distinguishes a view registration from a
    build-time validator such as `register_generated_pbc_package(manifest)`,
    which shares the name prefix and is correctly never called at startup.
    """
    mounts: dict[str, str] = {}
    for path in sorted(app_dir.glob("*.py")):
        if path.name == "__init__.py":
            continue
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except SyntaxError:
            continue
        for node in tree.body:
            if not isinstance(node, ast.FunctionDef) or not node.name.startswith("register_"):
                continue
            args = [arg.arg for arg in node.args.args]
            if args[:1] == ["appbuilder"]:
                mounts.setdefault(node.name, path.name)
    return mounts


def _unwired_mounts(app_dir: Path) -> list[str]:
    """Mount functions the app defines but never calls from `__init__.py`."""
    init_text = (app_dir / "__init__.py").read_text(encoding="utf-8")
    return sorted(
        name
        for name in _mount_functions(app_dir)
        if f"{name}(appbuilder)" not in init_text
    )


def test_the_scan_finds_the_mounts_it_claims_to_check(generated_app) -> None:
    """Guard against a vacuous pass: an empty scan would satisfy the next test."""
    mounts = _mount_functions(generated_app)
    assert len(mounts) >= _MIN_MOUNTS, (
        f"found only {len(mounts)} mount functions; the scan is not seeing the app"
    )
    # A known-wired mount must be visible to the scanner, or the scanner is blind.
    assert "register_openapi" in mounts
    assert "register_openapi" not in _unwired_mounts(generated_app)


def test_every_mount_function_is_wired(generated_app) -> None:
    """An emitted view module with no mount is a screen the app does not serve."""
    unwired = _unwired_mounts(generated_app)
    assert unwired == [], (
        "these modules define a register_<name>(appbuilder) mount but __init__.py "
        f"never calls it, so their views are unreachable: {unwired}"
    )


def test_the_two_orphans_that_motivated_this_check_are_mounted(generated_app) -> None:
    """Name the defect this closes, so a regression is unambiguous."""
    init_text = (generated_app / "__init__.py").read_text(encoding="utf-8")
    for module, name in (
        ("code_review", "register_code_review"),
        ("i18n", "register_i18n"),
    ):
        assert (generated_app / f"{module}.py").is_file(), module
        assert f"from app.{module} import {name}" in init_text, name
        assert f"{name}(appbuilder)" in init_text, name


def test_the_wiring_check_canaries_against_an_unwired_mount(
    generated_app, tmp_path
) -> None:
    """Point the check at its own defect and confirm it fails.

    Strip one mount call from a copy of the generated `__init__.py`; the check
    must report exactly that function. A green result from a check that has
    never been watched fail is not evidence.
    """
    app_dir = tmp_path / "app"
    shutil.copytree(generated_app, app_dir)
    init_path = app_dir / "__init__.py"
    text = init_path.read_text(encoding="utf-8")
    target = "register_code_review(appbuilder)\n"
    assert target in text, "canary target not found in the generated __init__.py"
    init_path.write_text(text.replace(target, ""))

    assert _unwired_mounts(app_dir) == ["register_code_review"]
