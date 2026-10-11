"""The generated PBC package must carry the block, not a placeholder.

Every generator emits a per-PBC package into the app it builds. That package is
what an operator reads to learn what the block does: its tables, its commands,
its events, its configuration. It described none of them. Each table was given
the same `code`/`status`/`version` stub regardless of the package's migration,
and the workbench rendered three cards describing the contract's own shape
(`owned_binding`, `state_keys`, `permission_count`) rather than the panels the
block mounts or the events it emits.

These tests generate a real three-PBC app and execute the emitted package the
way an installer would, asserting the content is the package's own.
"""

import importlib.util
import sys
from pathlib import Path

import pytest

from pyAppGen.dsl import schema_from_dsl
from pyAppGen.gen import generate_app_from_schema
from pyAppGen.pbc import pbc_composition_dsl, pbc_implementation_contract

COMPOSITION = ("dam_core", "gl_core", "ar_credit")
STUB_FIELDS = {"id", "code", "status", "version", "created_at", "updated_at"}


@pytest.fixture(scope="module")
def generated_app(tmp_path_factory):
    output = tmp_path_factory.mktemp("pbc-package") / "app"
    dsl = pbc_composition_dsl(COMPOSITION, app_name="LegoLedger")
    schema = schema_from_dsl(dsl, source_name="lego.appgen")
    generate_app_from_schema(schema, output)
    return output


def _load(package_dir: Path, name: str):
    """Import one emitted module by path, without a package on `sys.path`."""
    path = package_dir / f"{name}.py"
    assert path.is_file(), path
    module_name = f"_pbc_surface_{package_dir.name}_{name}"
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec and spec.loader, path
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    try:
        spec.loader.exec_module(module)
    finally:
        sys.modules.pop(module_name, None)
    return module


def test_every_owned_table_carries_its_migrations_columns(generated_app):
    """A table described by `code`/`status`/`version` is a table not described.

    `dam_core` owns 49 tables; the emitter gave each one the same six-column
    stub, so the generated app declared a digital-asset schema and named none of
    its columns. The columns now come from the package's own migration.
    """
    for key in COMPOSITION:
        contract = pbc_implementation_contract(key)
        tables = contract["owned_schema"]["tables"]
        assert tables, key

        stub_tables = [
            table["owned_table"]
            for table in tables
            if {field["name"] for field in table["fields"]} <= STUB_FIELDS
        ]
        assert not stub_tables, (key, stub_tables[:5])

        for table in tables:
            assert table["fields"], table["owned_table"]
            for field in table["fields"]:
                assert field["name"], table["owned_table"]
                assert field.get("type"), (table["owned_table"], field)


def test_models_use_the_migrations_column_names(generated_app):
    """The ORM the app ships must describe the same columns as the migration."""
    for key in COMPOSITION:
        contract = pbc_implementation_contract(key)
        for model in contract["models"]:
            names = {field["name"] for field in model["fields"]}
            assert names, model["table"]
            assert not names <= STUB_FIELDS, (key, model["table"], sorted(names))


def test_the_emitted_workbench_renders_the_packages_own_surface(generated_app):
    """The generated `ui.py` must render the block, not the contract's shape.

    The three cards it used to return (`owned_binding`, `state_keys`,
    `permission_count`) are properties of the contract dict. They read the same
    for a digital-asset library and an accounts-receivable ledger. The cards now
    count what the package declares, and the payload carries the declarations
    themselves.
    """
    for key in COMPOSITION:
        module = _load(generated_app / "pbcs" / key, "ui")
        rendered = module.render_workbench_fragment({"tab": "assets"}, tenant="test")

        assert rendered["ok"] is True, key
        assert rendered["pbc"] == key
        assert rendered["panels"], key
        assert rendered["routes"], key
        assert rendered["configuration"]["required_fields"], key
        assert rendered["rules"]["rule_types"], key
        assert rendered["events"]["emits"], key
        assert rendered["action_permissions"], key

        # Every card names a real count, not a placeholder string.
        for card in rendered["cards"]:
            assert card["key"] and card["label"], (key, card)
            assert isinstance(card["value"], int), (key, card)

        # The surfaces must be the package's, not a generic default.
        source = module.UI
        assert len(rendered["panels"]) == len(source["panels"]), key
        assert rendered["events"]["emits"] == tuple(source["event_surfaces"]["emits"]), key


def test_the_emitted_workbench_reports_unauthorised_actions(generated_app):
    """A caller granted nothing must be shown every action as unavailable.

    The permission surface is what makes the workbench actionable rather than
    decorative, so an empty grant has to name what it withholds.
    """
    for key in COMPOSITION:
        module = _load(generated_app / "pbcs" / key, "ui")
        nothing = module.render_workbench_fragment(tenant="test")
        everything = module.render_workbench_fragment(
            tenant="test",
            principal_permissions=tuple(module.UI["action_permissions"].values()),
        )

        assert len(nothing["unauthorized_actions"]) == len(module.UI["action_permissions"]), key
        assert everything["unauthorized_actions"] == (), key


def test_the_emitted_workbench_smoke_is_green(generated_app):
    """The emitted package's own smoke test must pass on the real contract."""
    for key in COMPOSITION:
        module = _load(generated_app / "pbcs" / key, "ui")
        smoke = module.smoke_test()

        assert smoke["ok"] is True, (key, smoke)
        assert smoke["side_effects"] == (), key
        assert smoke["configuration"]["required_fields"], key
        assert smoke["rules"]["rule_types"], key
        assert smoke["events"]["emits"], key


def test_the_emitted_workbench_is_not_the_placeholder_cards(generated_app):
    """Canary: the placeholder *cards* must be gone from every emitted module.

    This is the assertion that would have caught the stub. It matches the card
    tuples, not the bare names: `state_keys` survives as a payload key because
    the workbench still reports the state it was handed, and matching the name
    alone would fail on the fixed module and pass on the broken one.
    """
    for key in COMPOSITION:
        text = (generated_app / "pbcs" / key / "ui.py").read_text(encoding="utf-8")
        for placeholder in (
            "{'key': 'owned_binding'",
            "{'key': 'state_keys'",
            "{'key': 'permission_count', 'value': len(tuple(principal_permissions))",
        ):
            assert placeholder not in text, (key, placeholder)
