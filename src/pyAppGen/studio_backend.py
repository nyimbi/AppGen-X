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
    rather than hardcoding a list.
    """
    routes = {
        "/api/studio/workspace": studio_workspace_payload,
        "/api/studio/components": component_palette_payload,
        "/api/studio/packages": component_packages_payload,
        "/api/studio/targets": target_capabilities_payload,
        "/api/studio/tokens": design_tokens_payload,
    }
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

    for path, handler in (
        ("/api/studio/workspace", studio_workspace_payload),
        ("/api/studio/components", component_palette_payload),
        ("/api/studio/packages", component_packages_payload),
        ("/api/studio/targets", target_capabilities_payload),
        ("/api/studio/tokens", design_tokens_payload),
    ):

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
    routes = {
        "/api/studio/workspace": studio_workspace_payload,
        "/api/studio/components": component_palette_payload,
        "/api/studio/packages": component_packages_payload,
        "/api/studio/targets": target_capabilities_payload,
        "/api/studio/tokens": design_tokens_payload,
        "/api/studio/manifest": studio_api_manifest,
    }
    handler = routes.get(path)
    if handler is None:
        return 404, json.dumps({"format": STUDIO_API_FORMAT, "ok": False, "reason": "unknown_route"})
    return 200, json.dumps(handler(), default=str)
