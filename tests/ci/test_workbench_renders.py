"""Render the generated workbench in a real browser and assert on the DOM.

Every other UI check in this repository inspects a contract dict: that a key
exists, that a colour string is `44px`, that a template mentions a class. None
of them has ever seen a pixel. A gate that reads a dict cannot tell a rendered
workbench from a blank page, which is why the declared-but-unmounted route
survived as long as it did.

These tests build the generated SPA, serve it with a stub API returning a real
workbench payload, and assert on what the browser actually renders: the PBC's
owned tables, its API routes, and its cards. The stub exists because the point
is the frontend's rendering, not the Flask app; the payload it serves is the
real one the generator emitted.

Skipped when Playwright or its browser is unavailable, since that is a checkout
condition rather than a defect.
"""

import json
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import pytest

from pyAppGen.dsl import schema_from_dsl
from pyAppGen.gen import generate_app_from_schema
from pyAppGen.pbc import pbc_composition_dsl

REPO_ROOT = Path(__file__).resolve().parents[2]
COMPOSITION = ("dam_core", "gl_core", "ar_credit")

playwright_api = pytest.importorskip("playwright.sync_api", reason="playwright is not installed")


def _build_spa(root: Path, *, break_workbench: bool) -> Path:
    """Generate an app and build its SPA. Skips without a toolchain.

    `break_workbench` replaces the emitted `Workbench.tsx` with a component that
    renders an empty shell. That is the canary for the gate below: a render gate
    that has never been watched fail is not evidence, and this is the cheapest
    input that should make every DOM assertion here fail.
    """
    studio_modules = REPO_ROOT / "appgen-frontend" / "node_modules"
    if not (studio_modules / ".bin" / "vite").exists():
        pytest.skip("no installed frontend toolchain to borrow")

    dsl = pbc_composition_dsl(COMPOSITION, app_name="LegoLedger")
    schema = schema_from_dsl(dsl, source_name="lego.appgen")
    generate_app_from_schema(schema, root)

    project = root.parent
    if break_workbench:
        (project / "src" / "Workbench.tsx").write_text(
            "/** Canary: a workbench that renders nothing. */\n"
            "export function Workbench() {\n"
            "  return <div id=\"canary-blank\" />\n"
            "}\n",
            encoding="utf-8",
        )

    link = project / "node_modules"
    if not link.exists():
        link.symlink_to(studio_modules)

    import subprocess

    build = subprocess.run(
        [str(link / ".bin" / "vite"), "build"],
        cwd=project,
        capture_output=True,
        text=True,
    )
    assert build.returncode == 0, build.stdout + build.stderr
    return project


@pytest.fixture(scope="module")
def built_spa(tmp_path_factory):
    """Generate a real app and build its SPA."""
    return _build_spa(tmp_path_factory.mktemp("render") / "app", break_workbench=False)


@pytest.fixture(scope="module")
def driver():
    """Own the single Playwright context for this module.

    The sync API refuses to open a second context on a thread that already has
    one, so the healthy build and the canary build share this rather than each
    opening their own.
    """
    with playwright_api.sync_playwright() as playwright:
        yield playwright


def _serve(project: Path, playwright):
    """Serve a built SPA with a stub API and yield a browser page and payload."""
    payload = _workbench_payloads(project)

    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *args, payload=None, directory=None, **kwargs):
            self._payload = payload or {}
            super().__init__(*args, directory=directory, **kwargs)

        def do_GET(self):  # noqa: N802 - stdlib hook name
            route = self.path.split("?", 1)[0]
            if route.endswith("/workbench.json"):
                key = route.split("/")[-2]
                body = json.dumps(self._payload.get(key, {"ok": False, "pbc": key})).encode()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                return
            if route.startswith("/api/v1/"):
                body = b"[]"
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                return
            if route == "/static/appgen-theme.css":
                self.send_response(200)
                self.send_header("Content-Type", "text/css")
                self.end_headers()
                self.wfile.write(b":root { --appgen-primary: #0f766e; }")
                return
            return super().do_GET()

        def log_message(self, format: str, *args: object) -> None:
            """Silence the test server; the base class writes to stderr."""

    server = ThreadingHTTPServer(
        ("127.0.0.1", 0),
        partial(Handler, payload=payload, directory=str(project / "dist")),
    )
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    browser = playwright.chromium.launch()
    page = browser.new_page()
    # The workbench renders from a payload the page already has, so anything
    # slower than a couple of seconds is a defect rather than a slow machine.
    # The default 30s also made the canary below spend three minutes waiting on
    # markup a blank template never produces.
    page.set_default_timeout(2500)
    page.goto(f"http://127.0.0.1:{server.server_port}/", wait_until="networkidle")
    try:
        yield page, payload
    finally:
        browser.close()
        server.shutdown()
        thread.join(timeout=5)


@pytest.fixture(scope="module")
def rendered(built_spa, driver):
    """Serve the built SPA with a stub API and yield a browser page factory."""
    yield from _serve(built_spa, driver)


def _workbench_payloads(project: Path) -> dict:
    """Return the real workbench payloads the generator embedded.

    The generator writes them into `app/pbc_workbench.py`; reading them back
    means the browser is served exactly what the backend would serve.
    """
    import ast

    source = (project / "app" / "pbc_workbench.py").read_text(encoding="utf-8")
    marker = "WORKBENCHES = "
    start = source.index(marker) + len(marker)
    # The literal is a single `repr` line, so it ends at the newline that closes
    # it. Brace matching would be wrong here: the payload nests dicts and the
    # string values contain braces.
    end = source.index("\n", start)
    payload = ast.literal_eval(source[start:end])

    rendered = {}
    for entry in payload["workbenches"]:
        rendered[entry["pbc"]] = {
            "format": "appgen.generated-pbc-workbench-render.v1",
            "ok": True,
            "pbc": entry["pbc"],
            "label": entry["label"],
            "mesh": entry["mesh"],
            "tenant": "test",
            "route": entry["route"],
            "fragments": list(entry["fragments"]),
            "workbench_view": entry["workbench_view"],
            "binds_to": entry["binds_to"],
            "owned_tables": list(entry["owned_tables"]),
            "apis": [dict(api) for api in entry["apis"]],
            "permissions_bound": [],
            "cards": [
                {"key": "owned_tables", "label": "Owned tables", "value": len(entry["owned_tables"])},
                {"key": "api_routes", "label": "Command and query APIs", "value": len(entry["apis"])},
                {"key": "permissions", "label": "Bound permissions", "value": len(entry["permissions"])},
                {"key": "outbox", "label": "Event outbox", "value": entry["outbox_table"]},
                {"key": "dead_letter", "label": "Dead-letter queue", "value": entry["dead_letter_table"]},
            ],
        }
    return rendered


def _select(page, payload, key: str) -> None:
    """Click the rail item for `key` and wait for its workbench to render.

    The page is shared across this module and the shell remembers which
    workbench is showing, so a test that assumes a particular PBC must select it
    rather than rely on the order the tests happen to run in.
    """
    entry = payload[key]
    page.get_by_role("button", name=entry["label"]).first.click()
    page.wait_for_timeout(300)
    assert entry["owned_tables"][0] in page.locator(".appgen-workbench").inner_text(), key


def test_the_workbench_actually_renders(rendered):
    """A workbench region with nothing in it must fail.

    Asserting on `#root` alone is not enough: the shell's nav rail renders the
    workbench labels whether or not the workbench itself renders, so the first
    version of this test passed on a page whose workbench body was empty. The
    assertion is scoped to the layout the workbench mounts inside, which is the
    region a broken template leaves blank.
    """
    page, payload = rendered
    root = page.locator("#root")
    assert root.count() == 1

    _select(page, payload, COMPOSITION[0])
    layout = page.locator(".appgen-workbench")
    assert layout.count() == 1, "the workbench layout did not mount"

    first = payload[COMPOSITION[0]]
    assert first["owned_tables"], "the payload carries no owned tables to assert on"
    assert first["owned_tables"][0] in layout.inner_text(), "the workbench region rendered nothing"


def test_the_first_workbench_shows_its_own_pbc(rendered):
    page, payload = rendered
    first = payload[COMPOSITION[0]]
    _select(page, payload, COMPOSITION[0])
    layout = page.locator(".appgen-workbench")
    assert layout.count() == 1, "the workbench layout did not mount"
    text = layout.inner_text()
    assert first["label"] in text
    assert first["pbc"] in text


def test_owned_tables_appear_as_real_rows(rendered):
    """The tables must be rendered, not merely counted."""
    page, payload = rendered
    first = payload[COMPOSITION[0]]
    # Without this the loop below and the count comparison both hold on an
    # empty list, so the test passed on a workbench that rendered no tables.
    assert first["owned_tables"], "the payload carries no owned tables to assert on"
    _select(page, payload, COMPOSITION[0])
    body = page.locator(".appgen-workbench").inner_text()
    for table in first["owned_tables"][:5]:
        assert table in body, table
    rows = page.locator("table.appgen-table tbody tr")
    assert rows.count() >= len(first["owned_tables"])


def test_api_routes_appear_with_their_methods(rendered):
    page, payload = rendered
    first = payload[COMPOSITION[0]]
    assert first["apis"], "the payload carries no API routes to assert on"
    _select(page, payload, COMPOSITION[0])
    body = page.locator(".appgen-workbench").inner_text()
    for api in first["apis"][:3]:
        assert api["route"] in body, api["route"]
    assert page.locator("table.appgen-table").count() >= 2


def test_the_shared_kit_classes_are_on_the_page(rendered):
    """The render must come through the kit, not from private markup."""
    page, payload = rendered
    _select(page, payload, COMPOSITION[0])
    for selector in (".appgen-workbench", ".appgen-table", ".appgen-card", ".appgen-nav-rail"):
        assert page.locator(selector).count() > 0, selector


def test_the_shell_navigates_to_another_workbench(rendered):
    """Clicking a rail item must swap the rendered workbench."""
    page, payload = rendered
    second = payload[COMPOSITION[1]]
    page.get_by_role("button", name=second["label"]).first.click()
    page.wait_for_timeout(300)
    assert second["pbc"] in page.locator(".appgen-workbench").inner_text()


def test_every_workbench_renders_without_error(rendered):
    page, payload = rendered
    for key in COMPOSITION:
        _select(page, payload, key)
        body = page.locator(".appgen-workbench").inner_text()
        assert "Could not load" not in body, key


def _axe_source() -> Path | None:
    """Return the installed axe-core bundle, or None when it is absent."""
    candidate = REPO_ROOT / "appgen-frontend" / "node_modules" / "axe-core" / "axe.min.js"
    return candidate if candidate.exists() else None


def test_the_rendered_workbench_has_no_serious_accessibility_violations(rendered):
    """A workbench a screen reader cannot use is not world class.

    The kit is built on accessible primitives, but the claim only holds if
    something checks the assembled page. axe runs against the DOM the browser
    actually built, at the two impact levels that block a user rather than the
    two that merely annoy.

    Skipped when axe-core is not installed, since that is a checkout condition
    rather than a defect.
    """
    axe = _axe_source()
    if axe is None:
        pytest.skip("axe-core is not installed")

    page, payload = rendered
    page.add_script_tag(path=str(axe))
    for key in COMPOSITION:
        entry = payload[key]
        page.get_by_role("button", name=entry["label"]).first.click()
        page.wait_for_timeout(250)
        result = page.evaluate(
            "async () => await axe.run(document, "
            "{ resultTypes: ['violations'] })"
        )
        blocking = [
            violation
            for violation in result["violations"]
            if violation["impact"] in ("serious", "critical")
        ]
        assert not blocking, (
            f"{key}: " + "; ".join(
                f"{violation['id']} ({violation['impact']}) on "
                f"{len(violation['nodes'])} node(s)" for violation in blocking
            )
        )


@pytest.fixture(scope="module")
def rendered_broken(tmp_path_factory, driver):
    """Build the same app with a Workbench that renders an empty shell."""
    project = _build_spa(tmp_path_factory.mktemp("canary") / "app", break_workbench=True)
    yield from _serve(project, driver)


def test_the_render_gate_fails_on_a_workbench_that_renders_nothing(rendered_broken):
    """Canary the gate: point the gate's own assertions at a blank workbench.

    A DOM assertion is worth its green only once it has been seen red, so this
    runs the assertions above, unmodified, against a build whose `Workbench.tsx`
    renders an empty shell. What must happen is that at least one of them
    raises: if all of them pass on a page with no workbench in it, they are not
    reading the workbench.

    The shell's nav rail still lists the workbench labels, which is why the
    canary does not simply assert a blank page and why every assertion below
    that reads the page reads the workbench region rather than `#root`. The one
    assertion left out is `test_the_shell_navigates_to_another_workbench`: the
    nav is not part of the workbench template, so a blank workbench correctly
    leaves it passing.
    """
    page, payload = rendered_broken
    assert page.locator("#canary-blank").count() == 1, "the broken template was not the one built"

    gate_assertions = (
        test_the_workbench_actually_renders,
        test_the_first_workbench_shows_its_own_pbc,
        test_owned_tables_appear_as_real_rows,
        test_api_routes_appear_with_their_methods,
        test_the_shared_kit_classes_are_on_the_page,
        test_every_workbench_renders_without_error,
    )
    survived = []
    for assertion in gate_assertions:
        try:
            assertion((page, payload))
        except (AssertionError, playwright_api.Error):
            # Either shape is the gate failing, which is what the canary wants.
            # A locator for markup the broken template never renders raises the
            # Playwright timeout, and an assertion on a value it never produced
            # raises AssertionError.
            continue
        survived.append(assertion.__name__)

    assert not survived, f"these passed on a blank workbench, so they prove nothing: {survived}"
