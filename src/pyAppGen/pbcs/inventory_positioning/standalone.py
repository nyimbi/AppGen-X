"""Standalone one-PBC application shell for inventory_positioning."""

from __future__ import annotations

from .agent import composed_agent_contribution
from .permissions import permission_manifest
from .routes import api_route_contracts
from .routes import dispatch_route
from .seed_data import STANDALONE_BOOTSTRAP
from .services import InventoryPositioningService
from .ui import inventory_positioning_render_workbench
from .ui import inventory_positioning_ui_contract


PBC_KEY = "inventory_positioning"


def standalone_app_contract() -> dict:
    routes = api_route_contracts()
    ui_contract = inventory_positioning_ui_contract()
    permissions = permission_manifest()
    agent = composed_agent_contribution()
    return {
        "ok": routes["ok"] and ui_contract["ok"] and permissions["ok"] and agent["ok"],
        "pbc": PBC_KEY,
        "name": "Inventory Positioning Standalone App",
        "runtime": "in_memory_single_pbc",
        "service_class": "InventoryPositioningService",
        "routes": routes["routes"],
        "ui_fragments": ui_contract["fragments"],
        "permissions": permissions["permissions"],
        "agent_namespace": agent["single_agent_skill_namespace"],
        "seed_bootstrap": STANDALONE_BOOTSTRAP,
        "side_effects": (),
    }


class InventoryPositioningStandaloneApp:
    """Execute the PBC as a package-local standalone app."""

    def __init__(self) -> None:
        self.service = InventoryPositioningService()

    @property
    def state(self) -> dict:
        return self.service.state

    def bootstrap(self) -> dict:
        self.service.configure_runtime(dict(STANDALONE_BOOTSTRAP["configuration"]))
        for name, value in STANDALONE_BOOTSTRAP["parameters"]:
            self.service.set_parameter({"name": name, "value": value})
        for rule in STANDALONE_BOOTSTRAP["rules"]:
            self.service.register_rule(dict(rule))
        for item in STANDALONE_BOOTSTRAP["items"]:
            self.service.register_item(dict(item))
        for node in STANDALONE_BOOTSTRAP["nodes"]:
            self.service.register_node(dict(node))
        for receipt in STANDALONE_BOOTSTRAP["receipts"]:
            self.service.post_goods_receipt(dict(receipt))
        return {"ok": True, "state": self.service.state, "side_effects": ()}

    def dispatch(self, method: str, path: str, payload: dict | None = None) -> dict:
        return dispatch_route(method, path, payload, service=self.service)

    def render_workbench(self, tenant: str, principal_permissions: tuple[str, ...]) -> dict:
        return inventory_positioning_render_workbench(self.service.state, tenant=tenant, principal_permissions=principal_permissions)


def smoke_test() -> dict:
    app = InventoryPositioningStandaloneApp()
    bootstrap = app.bootstrap()
    workbench = app.render_workbench("tenant_alpha", permission_manifest()["permissions"])
    allocation = app.dispatch(
        "POST",
        "/inventory/allocations",
        {
            "allocation_id": "alloc_standalone_001",
            "tenant": "tenant_alpha",
            "order_id": "order_001",
            "item_id": "sku_100",
            "quantity": 20.0,
            "demand_class": "standard",
        },
    )
    release = app.dispatch(
        "POST",
        "/inventory/allocations/alloc_standalone_001/release",
        {"reason": "customer_request"},
    )
    return {
        "ok": standalone_app_contract()["ok"] and bootstrap["ok"] and workbench["ok"] and allocation["ok"] and release["ok"],
        "contract": standalone_app_contract(),
        "bootstrap": bootstrap,
        "workbench": workbench,
        "allocation": allocation,
        "release": release,
        "side_effects": (),
    }
