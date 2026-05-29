"""Standalone one-PBC app composition for energy_grid_operations."""

from __future__ import annotations

from .agent import standalone_agent_workspace_contract
from .models import standalone_model_contract
from .routes import dispatch_standalone_route, standalone_route_contracts
from .seed_data import demo_workspace_seed
from .services import EnergyGridOperationsService, standalone_service_operation_contracts
from .ui import energy_grid_operations_render_standalone_app, energy_grid_operations_standalone_app_contract


def standalone_app_manifest() -> dict:
    models = standalone_model_contract()
    services = standalone_service_operation_contracts()
    routes = standalone_route_contracts()
    ui = energy_grid_operations_standalone_app_contract()
    agent = standalone_agent_workspace_contract()
    return {
        "format": "appgen.energy-grid-operations-standalone-app.v2",
        "ok": all(item.get("ok") is True for item in (models, services, routes, ui, agent)),
        "pbc": "energy_grid_operations",
        "models": models,
        "services": services,
        "routes": routes,
        "ui": ui,
        "agent": agent,
        "side_effects": (),
    }


class EnergyGridOperationsStandaloneApp:
    """Package-local standalone grid operations app backed by in-memory owned state."""

    def __init__(self, state: dict | None = None):
        self.service = EnergyGridOperationsService(state=state)

    @property
    def state(self) -> dict:
        return self.service.state

    def dispatch(self, method: str, path: str, payload: dict | None = None) -> dict:
        return dispatch_standalone_route(method, path, payload, service=self.service)

    def bootstrap(self, *, tenant: str = "tenant_demo") -> dict:
        seed = demo_workspace_seed(tenant=tenant)
        self.dispatch("POST", "/api/pbc/energy_grid_operations/runtime/configuration", {"configuration": seed["configuration"]})
        for parameter in seed["parameters"]:
            self.dispatch("POST", "/api/pbc/energy_grid_operations/runtime/parameters", parameter)
        for rule in seed["rules"]:
            self.dispatch("POST", "/api/pbc/energy_grid_operations/runtime/rules", {"rule": rule})
        self.dispatch(
            "POST",
            "/api/pbc/energy_grid_operations/events/inbox",
            {
                "envelope": {
                    "event_type": "OperationalKpiChanged",
                    "event_id": f"kpi-{tenant}",
                    "payload": {"tenant": tenant, "risk_threshold": 0.7},
                }
            },
        )
        return {"ok": True, "tenant": tenant, "state": self.state, "side_effects": ()}

    def load_demo_workspace(self, *, tenant: str = "tenant_demo") -> dict:
        seed = demo_workspace_seed(tenant=tenant)
        self.bootstrap(tenant=tenant)
        for item in seed["records"]:
            route = item["route"]
            if route.startswith(("POST ", "GET ")):
                method, path = route.split(" ", 1)
                self.dispatch(method, path, item["payload"])
            else:
                self.service.execute(route, item["payload"])
        rendered = self.render_workbench(tenant=tenant)
        return {"ok": rendered["ok"], "tenant": tenant, "rendered": rendered, "side_effects": ()}

    def render_workbench(self, *, tenant: str, principal_permissions: tuple[str, ...] | None = None) -> dict:
        return energy_grid_operations_render_standalone_app(
            self.state,
            tenant=tenant,
            principal_permissions=principal_permissions,
        )

    def release_snapshot(self) -> dict:
        from . import release_evidence

        return release_evidence.build_release_evidence()

    def close(self) -> None:
        self.service.close()


def smoke_test() -> dict:
    app = EnergyGridOperationsStandaloneApp()
    loaded = app.load_demo_workspace()
    rendered = app.render_workbench(tenant="tenant_demo")
    release_snapshot = app.release_snapshot()
    return {
        "ok": loaded["ok"]
        and rendered["ok"]
        and rendered["workbench"]["cards"][0]["value"] >= 1
        and release_snapshot["ok"],
        "manifest": standalone_app_manifest(),
        "loaded": loaded,
        "rendered": rendered,
        "release_snapshot": release_snapshot,
        "side_effects": (),
    }


def workbench_smoke_test() -> dict:
    app = EnergyGridOperationsStandaloneApp()
    loaded = app.load_demo_workspace()
    rendered = app.render_workbench(tenant="tenant_demo")
    return {
        "ok": loaded["ok"] and rendered["ok"] and rendered["workbench"]["cards"][0]["value"] >= 1,
        "manifest": standalone_app_manifest(),
        "loaded": loaded,
        "rendered": rendered,
        "side_effects": (),
    }
