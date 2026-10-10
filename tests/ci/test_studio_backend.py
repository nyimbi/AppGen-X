"""The Studio must read the Python contracts, not a local copy of them.

The frontend had no backend: every panel was populated from a TypeScript catalog
module, and `studio.py` certified the "integration" by reading the frontend's
own source text. A panel and the platform it claims to configure could therefore
disagree, and the only thing that would notice was a substring check.

These tests drive the backend without a browser and assert it serves the real
contracts, so a panel wired to it cannot show a component the generator does not
know, or a package suite that does not exist.
"""

import json

import pytest

from pyAppGen import form_designer, studio_backend

ROUTES = (
    "/api/studio/workspace",
    "/api/studio/components",
    "/api/studio/packages",
    "/api/studio/targets",
    "/api/studio/tokens",
)


@pytest.mark.parametrize("path", ROUTES)
def test_every_route_answers_with_its_format(path: str) -> None:
    status, body = studio_backend.studio_api_response(path)
    assert status == 200, path
    payload = json.loads(body)
    assert payload["format"] == studio_backend.STUDIO_API_FORMAT
    assert payload["ok"] is True


def test_unknown_route_is_a_named_404() -> None:
    status, body = studio_backend.studio_api_response("/api/studio/nope")
    assert status == 404
    assert json.loads(body)["reason"] == "unknown_route"


def test_the_manifest_lists_exactly_the_routes_that_answer() -> None:
    """The route table is one source, so the client cannot invent a route."""
    manifest = studio_backend.studio_api_manifest()
    assert set(manifest["paths"]) == set(ROUTES)
    for path in manifest["paths"]:
        status, _ = studio_backend.studio_api_response(path)
        assert status == 200, path


def test_the_component_panel_reads_the_generators_own_palette() -> None:
    """A Studio component the generator cannot bind is the defect this closes."""
    payload = studio_backend.component_palette_payload()
    served = {component["component"] for component in payload["components"]}
    generated = {component["component"] for component in form_designer.component_palette()}
    assert served == generated
    assert served, "the palette is empty"


def test_the_package_panel_reads_real_suites() -> None:
    payload = studio_backend.component_packages_payload()
    served = {package["id"] for package in payload["packages"]}
    real = {package["id"] for package in form_designer.THIRD_PARTY_COMPONENT_SUITES}
    assert served == real
    assert served


def test_the_device_panel_reads_the_target_contracts() -> None:
    payload = studio_backend.target_capabilities_payload()
    assert payload["mobile"]["ok"] is True
    assert payload["desktop"]["ok"] is True
    assert payload["mobile"]["permissions"], "the mobile contract declares no permissions"
    assert payload["targets"], "no targets are catalogued"


def test_the_token_panel_serves_the_canonical_file() -> None:
    from pyAppGen import design_tokens

    payload = studio_backend.design_tokens_payload()
    assert payload["tokens"] == design_tokens.load_tokens()
    assert payload["themes"]


def test_the_workspace_panel_serves_the_studio_contract() -> None:
    from pyAppGen import studio

    payload = studio_backend.studio_workspace_payload()
    assert payload["workspace"]["format"] == studio.studio_workspace()["format"]


def test_every_payload_serialises() -> None:
    """A contract that cannot be JSON-encoded is a 500 the client cannot read."""
    for path in ROUTES:
        status, body = studio_backend.studio_api_response(path)
        assert status == 200
        json.loads(body)


def test_the_flask_app_serves_the_api_and_the_built_frontend() -> None:
    """One process serves both, so the client's relative routes resolve."""
    app = studio_backend.studio_api_app()
    client = app.test_client()
    for path in ROUTES:
        response = client.get(path)
        assert response.status_code == 200, path
        assert response.is_json, path
    assert client.get("/api/studio/manifest").is_json


def test_the_frontend_reads_the_backend_rather_than_a_local_catalog() -> None:
    """The panels must call the API, not import a TypeScript catalog.

    This is the inverse of the old check: instead of Python grepping the
    frontend's text for a string it hoped to find, the frontend is asserted to
    reach the backend that exists. A panel that keeps its own catalog is the
    drift the backend was built to end.

    The package and device panels are ported here. The component palette still
    reads its local catalog, because the browser smoke harness drives it through
    a `Device` category and a storage search that the Python palette does not
    carry; porting it means porting those fixtures first, which is its own
    change.
    """
    from pathlib import Path

    source = Path(__file__).resolve().parents[2] / "appgen-frontend" / "src"
    client = source / "studioApi.ts"
    assert client.is_file(), "the typed Studio client is missing"
    client_text = client.read_text(encoding="utf-8")
    for route in ROUTES:
        assert route in client_text, f"the client does not call {route}"

    panels = {
        "PackageManager.tsx": "loadComponentPackages",
        "DeviceApiWorkbench.tsx": "loadTargetCapabilities",
    }
    for name, loader in panels.items():
        text = (source / name).read_text(encoding="utf-8")
        assert "from './studioApi'" in text, f"{name} does not import the client"
        assert loader in text, f"{name} does not call {loader}"
        assert "Catalog'" not in text, f"{name} still imports a local catalog"
