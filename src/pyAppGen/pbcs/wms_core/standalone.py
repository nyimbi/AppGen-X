"""Standalone one-PBC application surface for wms_core."""

from __future__ import annotations

from . import repository
from . import routes
from . import ui
from .runtime import wms_core_configure_runtime
from .runtime import wms_core_confirm_pack
from .runtime import wms_core_confirm_putaway
from .runtime import wms_core_confirm_shipment
from .runtime import wms_core_create_pack_task
from .runtime import wms_core_create_pick_wave
from .runtime import wms_core_create_putaway_task
from .runtime import wms_core_empty_state
from .runtime import wms_core_execute_pick
from .runtime import wms_core_generate_shipment_proof
from .runtime import wms_core_receive_event
from .runtime import wms_core_receive_inbound
from .runtime import wms_core_register_bin
from .runtime import wms_core_register_rule
from .runtime import wms_core_register_warehouse
from .runtime import wms_core_route_edge_command
from .runtime import wms_core_run_control_tests
from .runtime import wms_core_set_parameter
from .seed_data import demo_workspace_seed_bundle


def standalone_app_manifest() -> dict:
    """Return the executable standalone-app contribution from the package."""
    return {
        "ok": True,
        "pbc": "wms_core",
        "app": ui.wms_core_standalone_app_contract(),
        "routes": routes.api_route_contracts()["routes"],
        "repository": repository.wms_core_repository_contract(),
        "side_effects": (),
    }


class WmsCoreStandaloneApp:
    """Package-local standalone app that owns the WMS runtime state."""

    def __init__(self, state: dict | None = None):
        self.state = state or wms_core_empty_state()
        self.repository = repository.WmsCoreRepository(self.state)

    def _commit(self, result: dict) -> dict:
        if result.get("state") is not None:
            self.state = result["state"]
            self.repository.state = self.state
        return result

    def bootstrap(self, *, tenant: str = "tenant_demo") -> dict:
        bundle = demo_workspace_seed_bundle(tenant=tenant)
        self._commit(wms_core_configure_runtime(self.state, bundle["configuration"]))
        for name, value in bundle["parameters"].items():
            self._commit(wms_core_set_parameter(self.state, name, value))
        self._commit(wms_core_register_rule(self.state, bundle["rule"]))
        self._commit(wms_core_register_warehouse(self.state, bundle["warehouse"]))
        for bin_location in bundle["bins"]:
            self._commit(wms_core_register_bin(self.state, bin_location))
        for event in bundle["projection_events"]:
            self._commit(wms_core_receive_event(self.state, event))
        return {
            "ok": True,
            "tenant": tenant,
            "state": self.state,
            "repository": self.repository.read_model(tenant),
            "side_effects": (),
        }

    def load_demo_workspace(self, *, tenant: str = "tenant_demo") -> dict:
        bundle = demo_workspace_seed_bundle(tenant=tenant)
        self.bootstrap(tenant=tenant)
        self._commit(wms_core_receive_inbound(self.state, bundle["receipt"]))
        putaway = self._commit(
            wms_core_create_putaway_task(
                self.state,
                bundle["receipt"]["receipt_id"],
                item_id=bundle["receipt"]["item_id"],
                quantity=bundle["receipt"]["quantity"],
            )
        )
        self._commit(
            wms_core_confirm_putaway(
                self.state,
                putaway["task"]["task_id"],
                confirmed_by="standalone.supervisor",
            )
        )
        self._commit(wms_core_create_pick_wave(self.state, bundle["wave"]))
        first_order = bundle["wave"]["orders"][0]
        self._commit(
            wms_core_execute_pick(
                self.state,
                bundle["wave"]["wave_id"],
                first_order["order_id"],
                picked_quantity=first_order["quantity"],
                operator="picker.demo",
            )
        )
        pack_id = f"pack_{tenant}_001"
        self._commit(
            wms_core_create_pack_task(
                self.state,
                pack_id,
                order_id=first_order["order_id"],
                weight=14.2,
                dimensions=(40, 28, 22),
            )
        )
        self._commit(wms_core_confirm_pack(self.state, pack_id, station="pack_01", label_id=f"lbl_{tenant}_001"))
        shipment_id = f"ship_{tenant}_001"
        self._commit(
            wms_core_confirm_shipment(
                self.state,
                shipment_id,
                order_id=first_order["order_id"],
                carrier="swiftline",
                dock_door="door_out_01",
            )
        )
        edge_route = wms_core_route_edge_command(bundle["edge_command"], rails=bundle["edge_rails"])
        shipment_proof = wms_core_generate_shipment_proof(
            self.state,
            shipment_id,
            disclosure=("shipment_id", "order_id", "carrier", "dock_door"),
        )
        controls = wms_core_run_control_tests(self.state)
        return {
            "ok": controls["ok"] and shipment_proof["ok"] and edge_route["ok"],
            "tenant": tenant,
            "workbench": self.render_workbench(tenant=tenant),
            "repository": self.repository.read_model(tenant),
            "edge_route": edge_route,
            "shipment_proof": shipment_proof,
            "controls": controls,
            "side_effects": (),
        }

    def render_workbench(
        self,
        *,
        tenant: str,
        principal_permissions: tuple[str, ...] | None = None,
    ) -> dict:
        permissions = principal_permissions or tuple(
            sorted(set(ui.wms_core_ui_contract()["action_permissions"].values()))
        )
        return ui.wms_core_render_standalone_app(
            self.state,
            tenant=tenant,
            principal_permissions=permissions,
        )

    def release_snapshot(self) -> dict:
        from . import release_evidence

        return release_evidence.build_release_evidence()


def smoke_test() -> dict:
    """Exercise the standalone app surface end-to-end."""
    app = WmsCoreStandaloneApp()
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
    """Exercise bootstrap and rendering without release recursion."""
    app = WmsCoreStandaloneApp()
    loaded = app.load_demo_workspace()
    rendered = app.render_workbench(tenant="tenant_demo")
    return {
        "ok": loaded["ok"] and rendered["ok"] and rendered["workbench"]["cards"][0]["value"] >= 1,
        "manifest": standalone_app_manifest(),
        "loaded": loaded,
        "rendered": rendered,
        "side_effects": (),
    }
