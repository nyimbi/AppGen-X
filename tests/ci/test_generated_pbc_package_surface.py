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

import importlib
import importlib.util
import re
import sys
from pathlib import Path

import pytest

from pyAppGen.dsl import schema_from_dsl
from pyAppGen.gen import _pbc_package_file_contents, generate_app_from_schema
from pyAppGen.pbc import (
    IMPLEMENTED_PBC_KEYS,
    pbc_composition_dsl,
    pbc_implementation_contract,
)

COMPOSITION = ("dam_core", "gl_core", "ar_credit")
STUB_FIELDS = {"id", "code", "status", "version", "created_at", "updated_at"}


@pytest.fixture(scope="module")
def generated_app(tmp_path_factory):
    output = tmp_path_factory.mktemp("pbc-package") / "app"
    dsl = pbc_composition_dsl(COMPOSITION, app_name="LegoLedger")
    schema = schema_from_dsl(dsl, source_name="lego.appgen")
    generate_app_from_schema(schema, output)
    return output


@pytest.fixture(scope="module")
def emitted_package_root(tmp_path_factory):
    """Every emitted PBC package, written the way `generate_app_from_schema` writes it.

    The other fixtures in this file sample three keys, because a full
    `generate_app_from_schema` over all 147 takes over two minutes. The three
    fidelity assertions below are per-package and independent, so the whole
    corpus is cheap when only the package files are written: the emitter is a
    pure function of the contract and runs in about four seconds for 147 keys.
    That matters because the defects this file exists to catch were per-package
    (a numbered permission in seventeen packages, a doubled table prefix in one),
    and a three-key sample is a gate over 2% of the surface it names.
    """
    root = tmp_path_factory.mktemp("emitted-packages") / "app"
    (root / "pbcs").mkdir(parents=True)
    (root / "pbcs" / "__init__.py").write_text(
        '"""Generated PBC package namespace."""\n', encoding="utf-8"
    )
    for key in IMPLEMENTED_PBC_KEYS:
        contract = pbc_implementation_contract(key)
        assert contract["ok"], key
        package = root / "pbcs" / key
        package.mkdir()
        (package / "__init__.py").write_text("")
        for relative, content in _pbc_package_file_contents(contract).items():
            path = package / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
    return root


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


def _load_package_module(app_root: Path, key: str, name: str):
    """Import an emitted module through a synthetic package chain.

    `routes.py` and `services.py` import each other relatively
    (`from .services import ...`), so loading them by file path fails with
    "attempted relative import with no known parent package". The chain is
    registered by hand from `pbcs/` downward rather than by putting the app root
    on `sys.path`: the app's own `__init__.py` imports `flask_appbuilder.SQLA`,
    which this machine's FAB 5.2.2 no longer exports, so importing
    `app.pbcs.<key>` would fail on an unrelated version skew before reaching the
    module under test.
    """
    chain = [("pbcs", app_root / "pbcs"), (f"pbcs.{key}", app_root / "pbcs" / key)]
    for module_name, directory in chain:
        cached = sys.modules.get(module_name)
        if cached is not None and list(getattr(cached, "__path__", ())) == [str(directory)]:
            continue
        # A different fixture's app root may already own this synthetic name; the
        # cache is keyed by name, not by directory, so it is re-registered rather
        # than skipped, or the import below resolves against the wrong tree.
        spec = importlib.util.spec_from_file_location(
            module_name, directory / "__init__.py", submodule_search_locations=[str(directory)]
        )
        assert spec and spec.loader, directory
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
    return importlib.import_module(f"pbcs.{key}.{name}")


def _purge(key: str) -> None:
    """Drop an emitted package's modules from the import cache.

    `_load_package_module` caches under the real module name, so a test that
    rewrites an emitted file and re-imports it would otherwise read the stale
    module and the canary would pass against the unpatched code.
    """
    prefix = f"pbcs.{key}"
    for module_name in [m for m in sys.modules if m == prefix or m.startswith(f"{prefix}.")]:
        del sys.modules[module_name]
    importlib.invalidate_caches()


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


def _source_route_surface(key: str) -> set[tuple[str, str]]:
    """The `(method, path)` set the package's own `routes.py` dispatches.

    This is the surface the package's `dispatch_route` walks, and the one the
    emitted app must carry. The comparison is on `(method, path)` alone, not the
    permission: seventeen packages write a numbered placeholder
    (`ar_credit.query.13`) into their `routes.py` and the emitted app replaces it
    with the runtime's semantic one, which is the correction, not a drift.

    Both sides are normalized to the bare path. The package's `routes.py` writes
    some paths prefixed (`/api/pbc/ar_credit/ar/customers`) and some not, while
    the emitted file is uniformly prefixed, so comparing raw paths reports a
    mismatch on 106 of 147 keys that is a string prefix and nothing else.
    """
    module = importlib.import_module(f"pyAppGen.pbcs.{key}.routes")
    return {
        (contract["method"], _bare_path(key, contract["path"]))
        for contract in module.api_route_contracts()["contracts"]
    }


def _bare_path(key: str, path: str) -> str:
    """Strip the `/api/pbc/<key>` prefix a route may or may not carry."""
    prefix = f"/api/pbc/{key}"
    return path[len(prefix):] if path.startswith(prefix) else path


def _emitted_route_surface(app_root: Path, key: str) -> set[tuple[str, str]]:
    """The `(method, path)` set the generated `routes.py` declares, bare."""
    module = _load_package_module(app_root, key, "routes")
    surface = set()
    for row in module.ROUTES:
        surface.add((row["method"], _bare_path(key, row["path"])))
    return surface


def test_the_generated_route_surface_is_the_packages_own(generated_app):
    """The emitted app must dispatch the package's routes, not the literal's.

    The generator used to synthesize the route surface from the hand-maintained
    catalog literal: a generated `dam_core` app exposed 3 routes with
    `dam_core.command.1`-style permissions while the package declares 34 with
    `dam_core.asset.write`-style ones, and `gl_core` shipped `/temporal-ledger`
    and `/audit-proofs`, neither of which any runtime command implements. The
    emitted surface now comes from the package's own `routes.py`, so it must
    equal that package's route set exactly.
    """
    for key in COMPOSITION:
        emitted = _emitted_route_surface(generated_app, key)
        source = _source_route_surface(key)
        assert emitted == source, (
            key,
            sorted(source - emitted)[:5],
            sorted(emitted - source)[:5],
        )


def test_no_generated_route_carries_a_numbered_permission(generated_app):
    """A `dam_core.command.3` permission is a placeholder, not a grant.

    Seventeen packages wrote numbered permissions into their `routes.py`. The
    emitted app replaces each with the semantic permission the package's runtime
    declares for the same route, so no generated permission may end in an
    integer.
    """
    numbered = re.compile(r"\.(command|query)\.\d+$")
    for key in COMPOSITION:
        module = _load_package_module(generated_app, key, "routes")
        offenders = [row["permission"] for row in module.ROUTES if numbered.search(row["permission"])]
        assert not offenders, (key, offenders[:5])


def test_the_generated_operations_carry_the_packages_scope_and_event(generated_app):
    """Each emitted operation must own the tables and emit the event the package says.

    The generator used to give every command the package's whole table set and
    assign events by `position % len(emitted)`, so a generated `dam_core` app
    claimed every command wrote all 49 tables. The emitted `services.py` now
    carries the package's per-operation scope and event, and its own
    `service_operation_contracts()` gate must report `ok`.
    """
    for key in COMPOSITION:
        module = _load_package_module(generated_app, key, "services")
        contract = module.service_operation_contracts()
        assert contract["ok"] is True, (key, contract["ok"])
        assert contract["contracts"], key

        by_path = {}
        for item in contract["contracts"]:
            by_path[(item["method"], item["path"])] = item

        routes = _load_package_module(generated_app, key, "routes")
        for row in routes.ROUTES:
            operation = by_path[(row["method"], row["path"])]
            if operation["operation_kind"] == "command":
                assert operation["owned_tables"], (key, row["path"])
                assert operation["emitted_event"], (key, row["path"])
            else:
                assert operation["read_tables"], (key, row["path"])
                assert operation["emitted_event"] is None, (key, row["path"])
            for table in operation["owned_tables"] + operation["read_tables"]:
                assert table.startswith(f"{key}_"), (key, row["path"], table)


def _numbered_permissions(root: Path, key: str) -> list[str]:
    """The numbered placeholder permissions one emitted package carries.

    Read through the corpus predicate, so the canary exercises the same code the
    gate runs rather than a stricter restatement of it.
    """
    return [
        permission
        for offender_key, _, permission in _numbered_permission_offenders(root)
        if offender_key == key
    ]


def test_the_corpus_gate_fails_on_a_planted_numbered_permission(emitted_package_root):
    """Canary: a numbered permission planted anywhere in the corpus must fail.

    The corpus gate's whole point is coverage beyond the three-key composition,
    so the canary plants the defect in a package the composition does not use
    (`notifications`) and asserts the corpus predicate sees it. The patch goes to
    the emitted copy under `tmp_path` and is restored from the in-memory original,
    not with `git checkout`, so a failure mid-canary cannot revert real work.
    """
    key = "notifications"
    assert key not in COMPOSITION, "the canary must sit outside the three-key fixture"
    path = emitted_package_root / "pbcs" / key / "routes.py"
    original = path.read_text(encoding="utf-8")
    match = re.search(r"('permission': ')([^']+)(')", original)
    assert match, "canary target not found; the patch would be a no-op"
    assert not re.compile(r"\.(command|query)\.\d+$").search(match.group(2)), (
        "the planted package already carries a numbered permission"
    )
    planted = (
        original[: match.start(2)]
        + f"{key}.command.7"
        + original[match.end(2):]
    )
    assert planted != original, "the patch did not apply"
    try:
        path.write_text(planted, encoding="utf-8")
        _purge(key)
        assert _numbered_permissions(emitted_package_root, key) == [f"{key}.command.7"], (
            "the corpus predicate missed a planted numbered permission"
        )
    finally:
        path.write_text(original, encoding="utf-8")
        _purge(key)
    assert _numbered_permissions(emitted_package_root, key) == [], "the canary did not restore"


def test_the_fidelity_gate_fails_on_a_planted_route(generated_app):
    """Canary: a generated route the package does not declare must fail the gate.

    The gate compares two sets read from two different modules, so a planted
    extra route in the emitted `routes.py` is exactly the shape of the defect it
    exists to catch (the literal's phantom `/temporal-ledger`). The patch is
    applied to the emitted copy under `tmp_path`, not the package source, so it
    cannot leak; the target is asserted present so a no-op patch cannot pass.
    """
    key = "gl_core"
    path = generated_app / "pbcs" / key / "routes.py"
    original = path.read_text(encoding="utf-8")
    target = (
        "    {'method': 'GET', 'path': '/api/pbc/gl_core/gl/workbench',"
        " 'handler': 'query_gl_workbench', 'permission': 'gl_core.audit'},\n"
    )
    assert target in original, "canary target not found; the patch would be a no-op"
    planted = original.replace(
        target,
        target
        + "    {'method': 'GET', 'path': '/api/pbc/gl_core/gl/temporal-ledger',"
        " 'handler': 'query_gl_temporal_ledger', 'permission': 'gl_core.read'},\n",
        1,
    )
    assert planted != original, "the patch did not apply"
    try:
        path.write_text(planted, encoding="utf-8")
        _purge(key)
        emitted = _emitted_route_surface(generated_app, key)
        assert emitted != _source_route_surface(key), "the gate missed a planted route"
    finally:
        path.write_text(original, encoding="utf-8")
        _purge(key)


def test_every_emitted_package_carries_its_own_route_surface(emitted_package_root):
    """All 147 packages, not the three a full app generation can afford.

    The per-package fidelity defects were not confined to the composition the
    three-key fixture happens to use: seventeen packages wrote a numbered
    permission, and the doubled table prefix appeared in exactly one. A gate over
    a three-key sample is a gate over 2% of the surface it claims to cover, so
    the whole corpus is checked here.
    """
    mismatched = []
    for key in IMPLEMENTED_PBC_KEYS:
        emitted = _emitted_route_surface(emitted_package_root, key)
        source = _source_route_surface(key)
        if emitted != source:
            mismatched.append((key, sorted(source - emitted)[:3], sorted(emitted - source)[:3]))
    assert not mismatched, mismatched[:5]


def _numbered_permission_offenders(root: Path) -> list[tuple[str, str, str]]:
    """Every numbered placeholder permission in the emitted corpus.

    The gate and its canary both call this, so the canary cannot pass by
    reimplementing the predicate more strictly than the gate runs it.
    """
    numbered = re.compile(r"\.(command|query)\.\d+$")
    offenders = []
    for key in IMPLEMENTED_PBC_KEYS:
        module = _load_package_module(root, key, "routes")
        for row in module.ROUTES:
            if numbered.search(row["permission"]):
                offenders.append((key, row["path"], row["permission"]))
    return offenders


def test_no_emitted_package_carries_a_numbered_permission(emitted_package_root):
    """The placeholder permission must be gone from every package, not three.

    Seventeen packages wrote `{key}.command.N` / `{key}.query.N` into their own
    `routes.py`. A permission the package never declared cannot be granted, so a
    numbered one is a button nobody can press; the emitted app must name the
    runtime's semantic permission instead.
    """
    offenders = _numbered_permission_offenders(emitted_package_root)
    assert not offenders, offenders[:5]


def test_every_emitted_package_scope_and_event_is_its_own(emitted_package_root):
    """Every emitted operation must satisfy the facade's own invariant, all 147.

    The emitted `services.py` validates that a command owns tables and reads
    none with a non-empty event, and that a query reads tables and owns none with
    no event. Its `service_operation_contracts()["ok"]` is that validation run on
    itself, and every scope entry must name a table the app actually emits
    (`<key>_`-prefixed), because the generated migration creates only the
    contract's tables.
    """
    failures = []
    for key in IMPLEMENTED_PBC_KEYS:
        module = _load_package_module(emitted_package_root, key, "services")
        contract = module.service_operation_contracts()
        if contract["ok"] is not True:
            failures.append((key, "ok", contract["ok"]))
            continue
        for item in contract["contracts"]:
            if item["operation_kind"] == "command":
                if not item["owned_tables"] or item["read_tables"] or not item["emitted_event"]:
                    failures.append((key, item["path"], "command scope"))
            else:
                if not item["read_tables"] or item["owned_tables"] or item["emitted_event"] is not None:
                    failures.append((key, item["path"], "query scope"))
            for table in item["owned_tables"] + item["read_tables"]:
                if not table.startswith(f"{key}_"):
                    failures.append((key, item["path"], table))
    assert not failures, failures[:5]
