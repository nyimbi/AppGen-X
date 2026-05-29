"""Standalone one-PBC application composition for federated_iam."""

from __future__ import annotations

from . import agent
from . import events
from . import manifest
from . import permissions
from . import routes
from . import seed_data
from . import services
from . import ui


PBC_KEY = "federated_iam"


def create_standalone_app(granted_permissions: tuple[str, ...] | None = None) -> dict:
    """Create a deterministic standalone app bundle for this PBC."""
    seeded = seed_data.build_seed_state()
    effective_permissions = tuple(granted_permissions or manifest.PBC_MANIFEST["permissions"])
    service = services.FederatedIamService(
        state=seeded["state"],
        granted_permissions=effective_permissions,
    )
    workbench = ui.federated_iam_render_workbench(
        service.state,
        tenant="tenant_seed_alpha",
        principal_permissions=effective_permissions,
    )
    route_manifest = routes.api_route_contracts()
    chatbot = agent.composed_agent_contribution()
    return {
        "ok": seeded["ok"] and route_manifest["ok"] and chatbot["ok"] and workbench["ok"],
        "pbc": PBC_KEY,
        "manifest": manifest.PBC_MANIFEST,
        "service_manifest": services.service_operation_manifest(),
        "routes": route_manifest,
        "ui_contract": ui.federated_iam_ui_contract(),
        "workbench": workbench,
        "permissions": permissions.access_profile(effective_permissions),
        "agent": chatbot,
        "events": events.event_contract_manifest(),
        "seed": seeded,
        "install": seed_data.standalone_install_plan(),
        "service": service,
        "side_effects": (),
    }


def standalone_manifest() -> dict:
    """Return the serializable standalone app manifest without service instances."""
    app = create_standalone_app()
    return {
        "ok": app["ok"],
        "pbc": app["pbc"],
        "routes": app["routes"]["routes"],
        "ui_fragments": app["ui_contract"]["fragments"],
        "workflow_routes": tuple(item["route"] for item in app["ui_contract"]["workflow_routes"]),
        "seed_summary": app["seed"]["summary"],
        "chatbot": app["agent"]["chatbot"],
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Exercise the standalone one-PBC composition surface."""
    app = create_standalone_app()
    manifest_view = standalone_manifest()
    service = app["service"]
    query = service.execute("build_workbench_view", {"tenant": "tenant_seed_alpha"})
    return {
        "ok": app["ok"] and manifest_view["ok"] and query["ok"],
        "app": app,
        "manifest": manifest_view,
        "query": query,
        "side_effects": (),
    }
