"""A generated app must ship a real SPA, not a stub.

The generator used to emit per-framework toy files (`frontends/react/src/App.jsx`
listing table names) with no build, no client, and no way to reach the API. The
SPA is now a Vite + React + TypeScript app that builds, and its typed client is
generated from the same composition plan the Flask views are built from, so the
shell cannot offer a screen the backend does not serve.

These tests generate a real three-PBC app and check the emitted tree, the
generated contract, and that the client reads its routes from that contract
rather than hardcoding them.
"""

import json
import re
import subprocess
from pathlib import Path

import pytest

from pyAppGen.dsl import schema_from_dsl
from pyAppGen.gen import generate_app_from_schema
from pyAppGen.pbc import pbc_composition_dsl

REPO_ROOT = Path(__file__).resolve().parents[2]
COMPOSITION = ("dam_core", "gl_core", "ar_credit")
SPA_TEMPLATE = REPO_ROOT / "src" / "pyAppGen" / "spa_templates"


@pytest.fixture(scope="module")
def generated_app(tmp_path_factory):
    output = tmp_path_factory.mktemp("spa") / "app"
    dsl = pbc_composition_dsl(COMPOSITION, app_name="LegoLedger")
    schema = schema_from_dsl(dsl, source_name="lego.appgen")
    generate_app_from_schema(schema, output)
    return output


def _contract(generated_app: Path) -> str:
    return (generated_app.parent / "src" / "appgen.generated.ts").read_text(encoding="utf-8")


def _exported_array(source: str, name: str) -> list:
    """Read a `export const NAME: readonly T[] = [...]` literal out of the module.

    The module is TypeScript, but the literal itself is JSON, so the array is
    extracted by brace matching rather than by importing.
    """
    marker = f"export const {name}: readonly"
    start = source.index(marker)
    # The type annotation carries its own brackets (`readonly TableSpec[]`), so
    # the literal starts at the first `[` after the `=`.
    equals = source.index("=", start)
    bracket = source.index("[", equals)
    depth = 0
    for offset, char in enumerate(source[bracket:], start=bracket):
        if char == "[":
            depth += 1
        elif char == "]":
            depth -= 1
            if depth == 0:
                return json.loads(source[bracket : offset + 1])
    raise AssertionError(f"unterminated array for {name}")


def test_spa_tree_is_emitted(generated_app):
    root = generated_app.parent
    for name in ("index.html", "vite.config.ts", "tsconfig.json", "package.json", "FRONTEND.md"):
        assert (root / name).is_file(), name
    for name in ("main.tsx", "App.tsx", "Workbench.tsx", "api.ts", "appgen.css", "appgen.generated.ts"):
        assert (root / "src" / name).is_file(), name


def test_spa_does_not_clobber_the_project_readme(generated_app):
    """The scaffold's README describes the app; the SPA's must not overwrite it."""
    readme = (generated_app.parent / "README.md").read_text(encoding="utf-8")
    assert "frontend" not in readme.splitlines()[0].lower()
    assert (generated_app.parent / "FRONTEND.md").is_file()


def test_spa_resolves_the_shared_kit(generated_app):
    """The SPA must consume the emitted kit, not a private copy."""
    root = generated_app.parent
    tsconfig = json.loads((root / "tsconfig.json").read_text(encoding="utf-8"))
    assert tsconfig["compilerOptions"]["paths"]["@appgen/ui-kit"] == ["app/ui_kit/index.ts"]
    assert "app/ui_kit" in tsconfig["include"]

    vite = (root / "vite.config.ts").read_text(encoding="utf-8")
    assert "'/app/ui_kit/index.ts'" in vite
    assert "'/app/ui_kit/components.css'" in vite

    # The kit the SPA points at must be the one the generator emitted.
    assert (generated_app / "ui_kit" / "index.ts").is_file()


def test_contract_lists_the_composition_workbenches(generated_app):
    workbenches = _exported_array(_contract(generated_app), "WORKBENCHES")
    assert {entry["pbc"] for entry in workbenches} == set(COMPOSITION)
    for entry in workbenches:
        assert entry["route"] == f"/workbench/pbcs/{entry['pbc']}"
        assert entry["label"] and entry["mesh"]


def test_contract_tables_carry_the_served_route(generated_app):
    tables = _exported_array(_contract(generated_app), "TABLES")
    assert tables, "a generated app must declare its tables to the SPA"
    for table in tables:
        assert table["route"].startswith("/api/v1/")
        assert table["route"].endswith("/")
        assert table["primaryKey"]
        assert isinstance(table["columns"], list) and table["columns"]


def test_client_reads_routes_from_the_generated_contract(generated_app):
    """A hardcoded route in the client is the drift this prevents."""
    api = (generated_app.parent / "src" / "api.ts").read_text(encoding="utf-8")
    assert "from './appgen.generated'" in api
    assert "/api/v1/" not in api, "the client must not hardcode a server route"
    assert "/workbench/pbcs/" not in api, "the client must not hardcode a workbench route"
    assert "${workbench.route}/workbench.json" in api


def test_app_shell_navigates_only_over_generated_screens(generated_app):
    app = (generated_app.parent / "src" / "App.tsx").read_text(encoding="utf-8")
    assert "from './appgen.generated'" in app
    assert "WORKBENCHES" in app and "TABLES" in app


def test_generated_typescript_parses_as_a_module(generated_app):
    """The emitted contract must be well-formed, not merely plausible.

    `ast.parse` is not available for TypeScript, so the check is structural:
    every exported declaration is terminated and the file has no unbalanced
    braces, which is what a truncated write would produce.
    """
    source = _contract(generated_app)
    assert source.count("{") == source.count("}")
    assert source.count("[") == source.count("]")
    for declaration in ("APP_NAME", "API_BASE", "TABLES", "WORKBENCHES"):
        assert re.search(rf"export const {declaration}\b", source), declaration


def test_spa_type_checks_and_builds(generated_app):
    """The real gate: `tsc && vite build` must succeed on the emitted tree.

    Skipped when the repository has no installed toolchain, because a missing
    `node_modules` is a checkout condition, not a defect in the generated app.
    """
    root = generated_app.parent
    studio_modules = REPO_ROOT / "appgen-frontend" / "node_modules"
    if not (studio_modules / ".bin" / "tsc").exists():
        pytest.skip("no installed frontend toolchain to borrow")

    link = root / "node_modules"
    if not link.exists():
        link.symlink_to(studio_modules)

    tsc = subprocess.run(
        [str(link / ".bin" / "tsc"), "--noEmit"],
        cwd=root,
        capture_output=True,
        text=True,
    )
    assert tsc.returncode == 0, tsc.stdout + tsc.stderr

    build = subprocess.run(
        [str(link / ".bin" / "vite"), "build"],
        cwd=root,
        capture_output=True,
        text=True,
    )
    assert build.returncode == 0, build.stdout + build.stderr

    css = "\n".join(path.read_text(encoding="utf-8") for path in (root / "dist" / "assets").glob("*.css"))
    assert ".appgen-button" in css
    assert ".appgen-workbench" in css
    assert "--appgen-primary" in css

    js = "\n".join(path.read_text(encoding="utf-8") for path in (root / "dist" / "assets").glob("*.js"))
    for key in COMPOSITION:
        assert key in js, key
