"""A JSON backend for the Studio, served from the Python contracts.

The Studio frontend had no backend. Every panel was populated from a local
TypeScript catalog module, so the panel and the platform could disagree and
nothing would notice. `studio.py` asserted the "integration" by reading the
frontend's own source text and checking for substrings, which is the coupling
inverted: Python reading TypeScript to decide whether Python is wired up.

This module serves the panels from the contracts that already exist. It is a
plain WSGI application, so it runs under the Flask the package already depends
on, and a test can drive it without a browser. Each route returns a payload with
a `format` field so a consumer can assert the shape it read.

The catalogs are read at request time rather than baked into the bundle, which
is the whole point: a change to a contract reaches the Studio on reload, and the
Studio has nothing of its own to drift.
"""

from __future__ import annotations

import json
from functools import lru_cache
from typing import Any, Callable

from . import design_tokens, form_designer, studio, targets

STUDIO_API_FORMAT = "appgen.studio-api.v1"


def studio_api_manifest() -> dict:
    """Return the routes the Studio backend serves.

    A single source for the route table means the frontend's client and the
    server cannot disagree about what exists, and the smoke test can iterate it
    rather than hardcoding a list. `STUDIO_API_ROUTES` is that source; the WSGI
    app and the framework-free responder both read it, so adding a route is one
    edit rather than three.
    """
    routes = STUDIO_API_ROUTES
    return {
        "format": STUDIO_API_FORMAT,
        "routes": tuple(
            {"path": path, "handler": getattr(handler, "__name__", type(handler).__name__)}
            for path, handler in routes.items()
        ),
        "paths": tuple(routes),
    }


@lru_cache(maxsize=1)
def studio_workspace_payload() -> dict:
    """Return the Studio workspace, the contract the panels are built from.

    The workspace is a pure function of the sample source and costs tens of
    seconds to compute (it runs the LSP, designer-sync, and graph suites), so it
    is cached. A request-time recomputation would make the Studio's first paint
    a minute long for a result that cannot have changed.
    """
    workspace = studio.studio_workspace()
    return {
        "format": STUDIO_API_FORMAT,
        "ok": True,
        "workspace": _jsonable(workspace),
    }


def studio_semantic_service_payload() -> dict:
    """Return the shared-semantics bridge the editor and designers sit on.

    The panel showed a TypeScript list of service names and designer surfaces.
    The workspace already computes the real ones (its `semantic_service`
    section), so this slices that cached result rather than recomputing a
    contract that costs a minute.
    """
    workspace = studio_workspace_payload()["workspace"]
    return {
        "format": STUDIO_API_FORMAT,
        "ok": True,
        "semantic_service": workspace["semantic_service"],
    }


def component_palette_payload() -> dict:
    """Return the component palette the designer offers.

    The Python palette is the one the generator binds against; the Studio's
    TypeScript catalog was a second, unrelated list of invented names. The
    groups carry the toolbox's ordering and headings, so the panel renders the
    platform's grouping rather than recomputing one from a flat list.
    """
    palette = form_designer.component_palette()
    return {
        "format": STUDIO_API_FORMAT,
        "ok": True,
        "components": _jsonable(palette),
        "categories": _jsonable(form_designer.palette_categories()),
        "groups": _jsonable(form_designer.palette_category_groups()),
    }


def component_packages_payload() -> dict:
    """Return the third-party component suites a design package can install."""
    suites = form_designer.THIRD_PARTY_COMPONENT_SUITES
    return {
        "format": STUDIO_API_FORMAT,
        "ok": True,
        "packages": _jsonable(suites),
    }


def target_capabilities_payload() -> dict:
    """Return the device and platform capabilities a target can use.

    The Studio's device panel listed capabilities in TypeScript. The platform
    already states them per target, so the panel reads them here instead.
    """
    return {
        "format": STUDIO_API_FORMAT,
        "ok": True,
        "targets": _jsonable(targets.target_catalog()),
        "mobile": _jsonable(targets.mobile_capability_contract()),
        "desktop": _jsonable(targets.desktop_capability_contract()),
    }


def design_tokens_payload() -> dict:
    """Return the design tokens, so the Studio reads the one source."""
    return {
        "format": STUDIO_API_FORMAT,
        "ok": True,
        "themes": tuple(design_tokens.theme_names()),
        "tokens": _jsonable(design_tokens.load_tokens()),
    }


def studio_designer_payload() -> dict:
    """Return the design surface: the form, its bindings, and the visual lanes.

    The designer canvas drew a hardcoded invoice and a hardcoded binding list,
    so it showed a form the platform had not projected and links the binding
    designer had not validated. Everything here comes from the contracts that
    already describe those surfaces, and each lane carries the `format` of the
    contract it renders so a lane cannot claim evidence it does not have.

    The form projection is sliced from the cached workspace: it is the same
    projection, and the workspace is a cached pure function of the sample source.
    """
    form = studio_workspace_payload()["workspace"]["form_designer"]
    graph = form_designer.livebindings_graph_contract()
    return {
        "format": STUDIO_API_FORMAT,
        "ok": True,
        "form": _jsonable(form),
        "binding_graph": _jsonable(graph),
        "binding_families": _jsonable(form_designer.binding_designer_family_contract()),
        "lanes": _jsonable(_designer_lanes()),
    }


def _designer_lanes() -> tuple[dict, ...]:
    """Return the visual lanes, each reading its own contract for its format.

    A lane's `format` is taken from the contract rather than written here, so a
    lane that renders nothing the platform publishes is not expressible.
    """
    timeline = form_designer.cross_target_animation_timeline_contract()
    cascade = form_designer.cross_target_style_cascade_contract()
    resources = form_designer.cross_target_style_resource_contract()
    scene = form_designer.cross_target_3d_scene_contract()
    effects = form_designer.cross_target_effects_pipeline_contract()
    return (
        {
            "lane": "timeline",
            "label": "Timeline",
            "icon": "animation",
            "format": timeline["format"],
            "items": [
                {"name": track["id"], "value": track["interpolation"], "detail": track["property"]}
                for track in timeline["tracks"]
            ],
            "operations": tuple(timeline["operations"]),
        },
        {
            "lane": "style",
            "label": "Style Tokens",
            "icon": "style",
            "format": resources["format"],
            "items": [
                {"name": layer["layer"], "value": f"order {layer['order']}", "detail": "cascade layer"}
                for layer in cascade["layers"]
            ],
            "operations": tuple(cascade["operations"]),
            "tokens": tuple(cascade["tokens"]),
            "states": tuple(resources["states"]),
            "targets": tuple(resources["targets"]),
        },
        {
            "lane": "scene",
            "label": "3D Scene",
            "icon": "viewport3d",
            "format": scene["format"],
            "items": [
                {"name": node["id"], "value": node["kind"], "detail": "scene node"}
                for node in scene["scene_graph"]
            ],
            "operations": tuple(scene["tools"]),
            "import_formats": tuple(scene["import_formats"]),
            "effects": tuple(effects["effects"]),
            "effects_format": effects["format"],
        },
    )


def studio_data_services_payload() -> dict:
    """Return the data and service tooling, grouped into its design lanes.

    The workbench listed eight capabilities written in TypeScript, each with a
    prose description of what it would do. The platform has sixty-odd real data
    contracts; this serves them grouped by the lane they belong to, and the
    panel renders the platform's lanes rather than its own list.
    """
    tooling = form_designer.rad_data_tooling_workbench()
    contract = tooling["contract"]
    readiness = tooling["readiness"]
    return {
        "format": STUDIO_API_FORMAT,
        "ok": tooling["ok"],
        "decision": tooling["decision"],
        "blocking_gaps": _jsonable(tooling["blocking_gaps"]),
        "readiness": {
            "format": readiness["format"],
            "ok": readiness["ok"],
            "phases": tuple(
                {"phase": phase["phase"], "ok": phase["ok"], "steps": tuple(phase["pipeline"])}
                for phase in readiness["phases"]
            ),
            "blocking_gaps": _jsonable(readiness["blocking_gaps"]),
        },
        "lanes": _jsonable(_data_service_lanes(tooling, contract)),
    }


def _data_service_lanes(tooling: dict, contract: dict) -> tuple[dict, ...]:
    """Return the data tooling grouped by design lane.

    Each entry names the contract it renders and takes its `format` from that
    contract, so a lane cannot point at a payload the platform does not serve.
    """
    def entry(key: str, source: dict) -> dict:
        value = source[key]
        return {"key": key, "format": value.get("format", ""), "evidence": value}

    lanes = (
        ("Source", "database", ("schema_browser", "driver_matrix", "connection_pooling")),
        (
            "Query",
            "query",
            ("query_designer", "parameter_binding", "query_plan_visualizer", "sql_authoring_safety", "stored_procedures"),
        ),
        (
            "Publish",
            "api",
            ("server_methods", "resources", "service_versioning", "service_telemetry", "service_tests"),
        ),
        ("Embedded DB", "dataset", ("local_database", "local_maintenance", "dataset_designer", "data_modules")),
        (
            "Resilience",
            "workflow",
            (
                "connection_failover",
                "offline_sync",
                "offline_replay",
                "replication_monitor",
                "change_capture_lineage",
                "migration_rehearsal",
            ),
        ),
        ("Security", "lock", ("service_security",)),
    )
    sources = {**tooling, **contract}
    return tuple(
        {
            "lane": lane,
            "icon": icon,
            "capabilities": tuple(entry(key, sources) for key in keys),
        }
        for lane, icon, keys in lanes
    )


def studio_inspector_payload() -> dict:
    """Return the object inspector's editor registries and their readiness.

    The inspector listed nine editors written in TypeScript against a
    hardcoded grid. The platform registers property, event, component, and
    custom-designer editors per component; this serves those registrations so
    the panel shows the editors the platform would actually open.
    """
    inspector = form_designer.object_inspector_workbench()
    readiness = inspector["readiness"]
    return {
        "format": STUDIO_API_FORMAT,
        "ok": inspector["ok"],
        "decision": inspector["decision"],
        "blocking_gaps": _jsonable(inspector["blocking_gaps"]),
        "registries": _jsonable(inspector["editor_registries"]),
        "grouping": _jsonable(inspector["property_grouping"]),
        "diagnostics": _jsonable(inspector["diagnostics"]),
        "action_registry": _jsonable(inspector["action_registry"]),
        "readiness": {
            "format": readiness["format"],
            "ok": readiness["ok"],
            "components": tuple(readiness["components"]),
            "final_state": _jsonable(readiness["final_state"]),
            "phases": tuple(
                {"phase": phase["phase"], "ok": phase["ok"], "steps": len(phase["pipeline"])}
                for phase in readiness["phases"]
            ),
            "checks": tuple({"id": check["id"], "ok": check["ok"]} for check in readiness["checks"]),
            "blocking_gaps": _jsonable(readiness["blocking_gaps"]),
        },
    }


def _jsonable(value: Any) -> Any:
    """Return a JSON-serialisable copy of a contract.

    The contracts are tuples and dataclasses in places, and a tuple becomes a
    JSON array on its own but a dataclass does not. Anything with `__dict__` is
    expanded; anything else is returned as-is for `json.dumps` to handle or
    reject, so a contract that cannot be serialised fails loudly here rather
    than as a 500 the client cannot read.
    """
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    if hasattr(value, "__dict__"):
        return {str(key): _jsonable(item) for key, item in vars(value).items()}
    return value


STUDIO_API_ROUTES: dict[str, Callable[[], dict]] = {
    "/api/studio/workspace": studio_workspace_payload,
    "/api/studio/components": component_palette_payload,
    "/api/studio/packages": component_packages_payload,
    "/api/studio/targets": target_capabilities_payload,
    "/api/studio/tokens": design_tokens_payload,
    "/api/studio/semantic-service": studio_semantic_service_payload,
    "/api/studio/designer": studio_designer_payload,
    "/api/studio/data-services": studio_data_services_payload,
    "/api/studio/inspector": studio_inspector_payload,
}


def studio_api_app() -> Callable:
    """Return a WSGI application serving the Studio API and the built frontend.

    The frontend is served from `appgen-frontend/dist` when it has been built,
    so one process serves both the API and the SPA. When it has not been built,
    the API still answers and the root returns a short message saying so, since
    a missing build is a checkout condition rather than a server fault.
    """
    from pathlib import Path

    from flask import Flask, jsonify, send_from_directory

    app = Flask(__name__)
    dist = Path(__file__).resolve().parents[2] / "appgen-frontend" / "dist"

    for path, handler in STUDIO_API_ROUTES.items():

        def _view(_handler=handler):
            return jsonify(_handler())

        app.add_url_rule(path, endpoint=handler.__name__, view_func=_view)

    @app.get("/api/studio/manifest")
    def _manifest():
        return jsonify(studio_api_manifest())

    @app.get("/")
    def _root():
        index = dist / "index.html"
        if index.exists():
            return send_from_directory(dist, "index.html")
        return (
            jsonify(
                {
                    "format": STUDIO_API_FORMAT,
                    "ok": False,
                    "reason": "frontend_not_built",
                    "hint": "cd appgen-frontend && npm install && npm run build",
                }
            ),
            503,
        )

    @app.get("/<path:asset>")
    def _asset(asset: str):
        candidate = dist / asset
        if candidate.is_file():
            return send_from_directory(dist, asset)
        # Unknown paths fall through to the SPA so client-side routing works.
        return send_from_directory(dist, "index.html")

    return app


def studio_api_response(path: str) -> tuple[int, str]:
    """Return `(status, body)` for a Studio API path, without a web framework.

    The WSGI app needs Flask; this does not, so a test can exercise the payloads
    and their serialisation in an environment where Flask is absent, and a
    static host can prerender them.
    """
    routes = {**STUDIO_API_ROUTES, "/api/studio/manifest": studio_api_manifest}
    handler = routes.get(path)
    if handler is None:
        return 404, json.dumps({"format": STUDIO_API_FORMAT, "ok": False, "reason": "unknown_route"})
    return 200, json.dumps(handler(), default=str)
