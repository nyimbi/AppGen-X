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
    "/api/studio/semantic-service",
    "/api/studio/designer",
    "/api/studio/data-services",
    "/api/studio/inspector",
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


def test_the_palette_carries_the_strings_the_toolbox_renders() -> None:
    """The toolbox renders what the panel shows, so every tile needs a label.

    A component without a display name renders as a bare class name, and a
    component missing from a group renders nowhere at all. Both are holes in
    the toolbox, so both are asserted here rather than discovered in a browser.
    """
    payload = studio_backend.component_palette_payload()
    components = payload["components"]
    assert all(component["label"] for component in components), "a component has no display label"
    assert all(component["description"] for component in components), "a component has no description"
    assert all(component["size"].count(" x ") == 1 for component in components), "a component has no W x H size"
    assert all(component["icon"].startswith("fa-") for component in components)

    grouped = [name for group in payload["groups"] for name in group["components"]]
    assert sorted(grouped) == sorted(component["component"] for component in components), (
        "the groups do not cover the palette exactly once"
    )
    assert all(group["label"] and group["icon"] for group in payload["groups"])


def test_the_palette_groups_follow_the_platforms_order() -> None:
    """The toolbox's ordering is the platform's, not a dict's iteration order."""
    groups = form_designer.palette_category_groups()
    declared = [group["category"] for group in groups]
    assert declared[: len(form_designer.PALETTE_CATEGORY_ORDER)] == list(form_designer.PALETTE_CATEGORY_ORDER)
    assert all(group["components"] for group in groups), "a group with no components would render an empty heading"


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


def test_the_semantic_panel_serves_the_workspaces_own_report() -> None:
    """The bridge is a slice of the workspace, not a second list to keep in sync."""
    payload = studio_backend.studio_semantic_service_payload()
    workspace = studio_backend.studio_workspace_payload()["workspace"]
    assert payload["semantic_service"] == workspace["semantic_service"]
    assert payload["semantic_service"]["services"], "the bridge declares no services"
    assert payload["semantic_service"]["designer_surfaces"], "the bridge declares no surfaces"


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
    """
    from pathlib import Path

    source = Path(__file__).resolve().parents[2] / "appgen-frontend" / "src"
    client = source / "studioApi.ts"
    assert client.is_file(), "the typed Studio client is missing"
    client_text = client.read_text(encoding="utf-8")
    for route in ROUTES:
        assert route in client_text, f"the client does not call {route}"

    panels = {
        "ComponentPalette.tsx": "loadComponentPalette",
        "PackageManager.tsx": "loadComponentPackages",
        "DeviceApiWorkbench.tsx": "loadTargetCapabilities",
        "SemanticServicePanel.tsx": "loadSemanticService",
        "DesignerCanvas.tsx": "loadDesigner",
        "DataServiceWorkbench.tsx": "loadDataServices",
        "InspectorPanel.tsx": "loadInspector",
    }
    for name, loader in panels.items():
        text = (source / name).read_text(encoding="utf-8")
        assert "from './studioApi'" in text, f"{name} does not import the client"
        assert loader in text, f"{name} does not call {loader}"
        assert "Catalog'" not in text, f"{name} still imports a local catalog"


def test_no_panel_reads_a_local_catalog() -> None:
    """The catalogs are gone, so a panel cannot quietly grow a new one.

    Seven panels used to render from TypeScript lists the platform knew nothing
    about. Deleting them is not enough on its own: a `*Catalog.ts` under `src/`
    is how the drift came back last time, so its return is a failure.
    """
    from pathlib import Path

    source = Path(__file__).resolve().parents[2] / "appgen-frontend" / "src"
    catalogs = sorted(path.name for path in source.glob("*Catalog.ts"))
    assert catalogs == [], f"local catalogs returned: {catalogs}"


def test_the_designer_serves_the_projected_form_and_the_real_graph() -> None:
    """The canvas drew a hardcoded invoice; it must draw the projected one.

    The form is the designer-sync projection of the sample DSL, and the graph is
    the livebindings contract's. Both are asserted against their own source so a
    canvas that renders a fixture again fails here.
    """
    from pyAppGen import dsl, form_designer, studio

    payload = studio_backend.studio_designer_payload()
    projection = studio.designer_sync_report_dsl(studio.SAMPLE_DSL)["projections"]["form_designer"]
    assert payload["form"]["views"] == studio_backend._jsonable(projection["views"])
    assert payload["binding_graph"] == studio_backend._jsonable(form_designer.livebindings_graph_contract())
    assert payload["binding_graph"]["edges"], "the binding graph has no edges"
    assert dsl.semantic_model_dsl(studio.SAMPLE_DSL)["views"], "the sample DSL projects no views"


def test_every_designer_lane_names_the_contract_it_renders() -> None:
    """A lane's `format` is the evidence it renders something published.

    The lanes used to be hardcoded lists of tracks, tokens, and scene nodes. A
    lane that renders items must name a contract, and that contract must be one
    the platform serves, so a lane cannot display invented content.
    """
    payload = studio_backend.studio_designer_payload()
    lanes = payload["lanes"]
    assert {lane["lane"] for lane in lanes} == {"timeline", "style", "scene"}
    for lane in lanes:
        assert lane["format"].startswith("appgen."), lane["lane"]
        assert lane["items"], f"{lane['lane']} renders no items"
        assert lane["operations"], f"{lane['lane']} declares no operations"


def test_the_data_workbench_serves_the_platforms_lanes() -> None:
    """The six lanes are the platform's, and each capability carries a contract."""
    payload = studio_backend.studio_data_services_payload()
    assert [lane["lane"] for lane in payload["lanes"]] == [
        "Source",
        "Query",
        "Publish",
        "Embedded DB",
        "Resilience",
        "Security",
    ]
    assert payload["decision"] == "approved"
    for lane in payload["lanes"]:
        assert lane["capabilities"], f"{lane['lane']} has no capabilities"
        for capability in lane["capabilities"]:
            assert capability["format"].startswith("appgen."), capability["key"]
            assert capability["evidence"], capability["key"]
    assert payload["readiness"]["phases"], "the readiness contract declares no phases"


def test_the_inspector_serves_the_registered_editors() -> None:
    """Every registered component needs all four editor kinds, or a panel is empty."""
    payload = studio_backend.studio_inspector_payload()
    assert payload["registries"], "no component registers editors"
    for registry in payload["registries"]:
        for kind in ("property_editors", "event_editors", "component_editors", "custom_designers"):
            assert registry[kind], f"{registry['component']} registers no {kind}"
    assert payload["grouping"], "no property grouping"
    assert payload["readiness"]["components"], "the readiness contract lists no components"
