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


@pytest.fixture(scope="module")
def built_spa(tmp_path_factory):
    """Generate a real app and build its SPA. Skips without a toolchain."""
    studio_modules = REPO_ROOT / "appgen-frontend" / "node_modules"
    if not (studio_modules / ".bin" / "vite").exists():
        pytest.skip("no installed frontend toolchain to borrow")

    root = tmp_path_factory.mktemp("render") / "app"
    dsl = pbc_composition_dsl(COMPOSITION, app_name="LegoLedger")
    schema = schema_from_dsl(dsl, source_name="lego.appgen")
    generate_app_from_schema(schema, root)

    project = root.parent
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
def rendered(built_spa):
    """Serve the built SPA with a stub API and yield a browser page factory."""
    payload = _workbench_payloads(built_spa)

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

        def log_message(self, *args):  # noqa: D102 - silence the test server
            pass

    server = ThreadingHTTPServer(
        ("127.0.0.1", 0),
        partial(Handler, payload=payload, directory=str(built_spa / "dist")),
    )
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    with playwright_api.sync_playwright() as driver:
        browser = driver.chromium.launch()
        page = browser.new_page()
        page.goto(f"http://127.0.0.1:{server.server_port}/", wait_until="networkidle")
        try:
            yield page, payload
        finally:
            browser.close()
            server.shutdown()
            thread.join(timeout=5)


def _workbench_payloads(project: Path) -> dict:
    """Return the real workbench payloads the generator embedded.

    The generator writes them into `app/pbc_workbench.py`; reading them back
    means the browser is served exactly what the backend would serve.
    """
    import ast
    import re

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


def test_the_workbench_actually_renders(rendered):
    """A blank page must fail. This is the assertion the dict gates cannot make."""
    page, payload = rendered
    root = page.locator("#root")
    assert root.count() == 1
    assert root.inner_text().strip(), "the SPA rendered nothing"


def test_the_first_workbench_shows_its_own_pbc(rendered):
    page, payload = rendered
    first = payload[COMPOSITION[0]]
    text = page.locator("#root").inner_text()
    assert first["label"] in text
    assert first["pbc"] in text


def test_owned_tables_appear_as_real_rows(rendered):
    """The tables must be rendered, not merely counted."""
    page, payload = rendered
    first = payload[COMPOSITION[0]]
    body = page.locator("#root").inner_text()
    for table in first["owned_tables"][:5]:
        assert table in body, table
    rows = page.locator("table.appgen-table tbody tr")
    assert rows.count() >= len(first["owned_tables"])


def test_api_routes_appear_with_their_methods(rendered):
    page, payload = rendered
    first = payload[COMPOSITION[0]]
    body = page.locator("#root").inner_text()
    for api in first["apis"][:3]:
        assert api["route"] in body, api["route"]
    assert page.locator("table.appgen-table").count() >= 2


def test_the_shared_kit_classes_are_on_the_page(rendered):
    """The render must come through the kit, not from private markup."""
    page, _ = rendered
    for selector in (".appgen-workbench", ".appgen-table", ".appgen-card", ".appgen-nav-rail"):
        assert page.locator(selector).count() > 0, selector


def test_the_shell_navigates_to_another_workbench(rendered):
    """Clicking a rail item must swap the rendered workbench."""
    page, payload = rendered
    second = payload[COMPOSITION[1]]
    page.get_by_role("button", name=second["label"]).first.click()
    page.wait_for_timeout(300)
    assert second["pbc"] in page.locator("#root").inner_text()


def test_every_workbench_renders_without_error(rendered):
    page, payload = rendered
    for key in COMPOSITION:
        entry = payload[key]
        page.get_by_role("button", name=entry["label"]).first.click()
        page.wait_for_timeout(250)
        body = page.locator("#root").inner_text()
        assert entry["owned_tables"][0] in body, key
        assert "Could not load" not in body, key
