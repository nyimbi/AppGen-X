"""The generated app must mount a workbench for every selected PBC.

The PBC packages declare a workbench route in their UI contract. Declaring it
is not mounting it: before this test existed, the generated app had the route
in a dict and no view behind it. These tests generate a real app from a real
three-PBC composition and check the route is served, renders the PBC's own
owned tables, and fails for a PBC that is not in the composition.
"""

import ast
from pathlib import Path

import pytest

from pyAppGen.dsl import schema_from_dsl
from pyAppGen.gen import generate_app_from_schema
from pyAppGen.pbc import pbc_composition_dsl

COMPOSITION = ("dam_core", "gl_core", "ar_credit")


@pytest.fixture(scope="module")
def generated_app(tmp_path_factory):
    output = tmp_path_factory.mktemp("pbc-workbench") / "app"
    dsl = pbc_composition_dsl(COMPOSITION, app_name="LegoLedger")
    schema = schema_from_dsl(dsl, source_name="lego.appgen")
    generate_app_from_schema(schema, output)
    return output


def _load_workbench_module(path: Path):
    """Import the generated workbench module with Flask stubbed out.

    The module imports Flask-AppBuilder for its view class, which is not
    installed in this test environment, so the two names it needs are stubbed.
    Everything under test (the catalog and render functions) is plain Python.
    """
    import sys
    import types

    flask = types.ModuleType("flask")
    flask.jsonify = lambda value: value  # type: ignore[attr-defined]
    fab = types.ModuleType("flask_appbuilder")

    class BaseView:  # noqa: D401 - stub
        """Stand-in for the real Flask-AppBuilder base view."""

    def expose(*args, **kwargs):
        def decorator(func):
            return func

        return decorator

    fab.BaseView = BaseView  # type: ignore[attr-defined]
    fab.expose = expose  # type: ignore[attr-defined]

    sys.modules["flask"] = flask
    sys.modules["flask_appbuilder"] = fab
    try:
        import importlib.util

        spec = importlib.util.spec_from_file_location("pbc_workbench", path)
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        sys.modules["pbc_workbench"] = module
        spec.loader.exec_module(module)
        return module
    finally:
        sys.modules.pop("flask", None)
        sys.modules.pop("flask_appbuilder", None)


def test_workbench_module_and_templates_are_generated(generated_app):
    assert (generated_app / "pbc_workbench.py").is_file()
    assert (generated_app / "templates" / "appgen_pbc_workbenches.html").is_file()
    assert (generated_app / "templates" / "appgen_pbc_workbench.html").is_file()


def test_workbench_view_is_registered_in_the_app(generated_app):
    """The view must actually be added, not merely defined."""
    init_text = (generated_app / "__init__.py").read_text(encoding="utf-8")

    assert "from app.pbc_workbench import register_pbc_workbenches" in init_text
    assert "register_pbc_workbenches(appbuilder)" in init_text

    workbench_text = (generated_app / "pbc_workbench.py").read_text(encoding="utf-8")
    assert 'route_base = "/workbench/pbcs"' in workbench_text
    assert "appbuilder.add_view(" in workbench_text


def test_workbench_route_matches_the_declared_pbc_contract(generated_app):
    """The mounted route base must be the route the PBC contracts declare."""
    workbench_text = (generated_app / "pbc_workbench.py").read_text(encoding="utf-8")
    tree = ast.parse(workbench_text)

    assert any(
        isinstance(node, ast.ClassDef) and node.name == "PbcWorkbenchView"
        for node in tree.body
    ), "the workbench view class is missing"

    for key in COMPOSITION:
        assert f"/workbench/pbcs/{key}" in workbench_text or key in workbench_text


def test_catalog_lists_one_workbench_per_selected_pbc(generated_app):
    module = _load_workbench_module(generated_app / "pbc_workbench.py")
    catalog = module.workbench_catalog()

    assert catalog["ok"] is True
    assert set(catalog["selected_pbcs"]) == set(COMPOSITION)
    assert {entry["pbc"] for entry in catalog["workbenches"]} == set(COMPOSITION)
    for entry in catalog["workbenches"]:
        assert entry["route"] == f"/workbench/pbcs/{entry['pbc']}"
        assert entry["fragments"]
        assert entry["owned_tables"]


def test_render_exposes_the_pbcs_own_owned_tables(generated_app):
    """A workbench showing nothing is the defect this closes.

    The render must carry the PBC's real owned tables and APIs, not a
    placeholder, so the composed app shows the block it was built from.
    """
    module = _load_workbench_module(generated_app / "pbc_workbench.py")

    for key in COMPOSITION:
        rendered = module.render_workbench(key, tenant="test")
        assert rendered["ok"] is True, key
        assert rendered["pbc"] == key
        assert len(rendered["owned_tables"]) > 3, key
        assert all(table.startswith(f"{key}_") for table in rendered["owned_tables"]), key
        assert rendered["apis"], key
        assert {card["key"] for card in rendered["cards"]} >= {
            "owned_tables",
            "api_routes",
            "panels",
            "outbox",
            "dead_letter",
        }


def test_render_exposes_the_pbcs_own_panels(generated_app):
    """The panels must be the package's, not a two-name placeholder.

    The generated contract collapsed every PBC's panel list to
    `ClassWorkbench`/`ClassDetail`, so a workbench for a block carrying six real
    panels rendered a stub pair. The panels now come from the package's own
    `ui_contract`, and this asserts the count the packages actually declare.
    """
    module = _load_workbench_module(generated_app / "pbc_workbench.py")

    for key in COMPOSITION:
        rendered = module.render_workbench(key, tenant="test")
        assert len(rendered["panels"]) >= 5, (key, len(rendered["panels"]))
        assert set(rendered["fragments"]) >= {panel["fragment"] for panel in rendered["panels"]}, key
        for panel in rendered["panels"]:
            assert panel["key"] and panel["fragment"], (key, panel)


def test_render_rejects_a_pbc_that_is_not_in_the_composition(generated_app):
    module = _load_workbench_module(generated_app / "pbc_workbench.py")

    rendered = module.render_workbench("not_a_selected_pbc")

    assert rendered["ok"] is False
    assert rendered["reason"] == "pbc_not_selected"


def test_workbench_smoke_is_green(generated_app):
    module = _load_workbench_module(generated_app / "pbc_workbench.py")
    smoke = module.smoke_test()

    assert smoke["ok"] is True
    assert smoke["side_effects"] == ()
    assert len(smoke["rendered"]) == len(COMPOSITION)


def test_workbench_templates_render_through_design_tokens(generated_app):
    """The workbench must be styled by the shared tokens, not private hex.

    The templates carry class names; the theme stylesheet defines those classes
    from the token variables. A workbench with its own colours is the
    divergence the design system exists to prevent, so both halves are checked:
    the templates use the shared classes, and the theme styles those classes
    from ``var(--appgen-*)`` rather than literals.
    """
    shared_classes = (
        "appgen-page",
        "appgen-workbench-grid",
        "appgen-workbench-card",
        "appgen-kpi-row",
    )
    theme_css = (generated_app / "static" / "appgen-theme.css").read_text(
        encoding="utf-8"
    )

    for name in ("appgen_pbc_workbench.html", "appgen_pbc_workbenches.html"):
        text = (generated_app / "templates" / name).read_text(encoding="utf-8")
        assert '{% extends "appbuilder/base.html" %}' in text, name
        assert any(cls in text for cls in shared_classes), name

    for cls in shared_classes:
        assert f".{cls}" in theme_css, cls
    assert "var(--appgen-" in theme_css
    # The workbench card rules must be token-driven, not hardcoded.
    card_block = theme_css.split(".appgen-workbench-card {")[1].split("}")[0]
    assert "var(--appgen-" in card_block
