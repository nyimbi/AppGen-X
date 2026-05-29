"""Standalone one-PBC application surface for transportation_management."""

from __future__ import annotations

from . import repository
from . import routes
from . import ui
from .runtime import transportation_management_configure_runtime
from .runtime import transportation_management_confirm_delivery
from .runtime import transportation_management_confirm_inbound_arrival
from .runtime import transportation_management_create_shipment
from .runtime import transportation_management_dispatch_shipment
from .runtime import transportation_management_empty_state
from .runtime import transportation_management_generate_delivery_proof
from .runtime import transportation_management_plan_route
from .runtime import transportation_management_receive_event
from .runtime import transportation_management_record_tracking_event
from .runtime import transportation_management_register_carrier
from .runtime import transportation_management_register_rule
from .runtime import transportation_management_register_schema_extension
from .runtime import transportation_management_route_telematics_event
from .runtime import transportation_management_run_control_tests
from .runtime import transportation_management_screen_policy
from .runtime import transportation_management_select_carrier
from .runtime import transportation_management_set_parameter
from .seed_data import demo_workspace_seed_bundle


def standalone_app_manifest() -> dict:
    """Return the executable standalone-app contribution from the package."""
    return {
        "ok": True,
        "pbc": "transportation_management",
        "app": ui.transportation_management_standalone_app_contract(),
        "routes": routes.api_route_contracts()["routes"],
        "repository": repository.transportation_management_repository_contract(),
        "side_effects": (),
    }


class TransportationManagementStandaloneApp:
    """Package-local standalone app that owns the TMS runtime state."""

    def __init__(self, state: dict | None = None):
        self.state = state or transportation_management_empty_state()
        self.repository = repository.TransportationManagementRepository(self.state)

    def _commit(self, result: dict) -> dict:
        if result.get("state") is not None:
            self.state = result["state"]
            self.repository.state = self.state
        return result

    def bootstrap(self, *, tenant: str = "tenant_demo") -> dict:
        bundle = demo_workspace_seed_bundle(tenant=tenant)
        self._commit(transportation_management_configure_runtime(self.state, bundle["configuration"]))
        for name, value in bundle["parameters"].items():
            self._commit(transportation_management_set_parameter(self.state, name, value))
        self._commit(transportation_management_register_rule(self.state, bundle["rule"]))
        self._commit(
            transportation_management_register_schema_extension(
                self.state,
                "shipment",
                {"telematics_payload": "jsonb", "temperature_payload": "jsonb"},
            )
        )
        for carrier in bundle["carriers"]:
            self._commit(transportation_management_register_carrier(self.state, carrier))
        for event in bundle["projection_events"]:
            self._commit(transportation_management_receive_event(self.state, event))
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
        shipment = self._commit(transportation_management_create_shipment(self.state, bundle["shipment"]))
        selection = self._commit(transportation_management_select_carrier(self.state, shipment["shipment"]["shipment_id"]))
        route = self._commit(
            transportation_management_plan_route(
                self.state,
                shipment["shipment"]["shipment_id"],
                distance_miles=bundle["distance_miles"],
                stops=bundle["stops"],
            )
        )
        dispatched = self._commit(
            transportation_management_dispatch_shipment(
                self.state,
                shipment["shipment"]["shipment_id"],
                tender_id=f"tender_{tenant}_001",
            )
        )
        tracking = self._commit(
            transportation_management_record_tracking_event(
                self.state,
                dispatched["shipment"]["shipment_id"],
                bundle["tracking_event"],
            )
        )
        self._commit(
            transportation_management_confirm_inbound_arrival(
                self.state,
                dispatched["shipment"]["shipment_id"],
                facility="SFO",
            )
        )
        delivered = self._commit(
            transportation_management_confirm_delivery(
                self.state,
                dispatched["shipment"]["shipment_id"],
                proof_id=f"proof_{tenant}_001",
            )
        )
        policy = transportation_management_screen_policy(self.state, delivered["shipment"]["shipment_id"], restricted_carriers=("carrier_suspended",))
        telematics_route = transportation_management_route_telematics_event(
            bundle["tracking_event"],
            rails=(
                {"route": "carrier_api", "available": False, "latency": 1},
                {"route": "appgen_outbox", "available": True, "latency": 3},
            ),
        )
        proof = transportation_management_generate_delivery_proof(
            self.state,
            delivered["shipment"]["shipment_id"],
            disclosure=("shipment_id", "carrier_id", "status", "proof_id"),
        )
        controls = transportation_management_run_control_tests(self.state)
        return {
            "ok": controls["ok"] and policy["ok"] and telematics_route["ok"] and proof["ok"] and route["ok"] and tracking["ok"],
            "tenant": tenant,
            "workbench": self.render_workbench(tenant=tenant),
            "repository": self.repository.read_model(tenant),
            "selection": selection,
            "policy": policy,
            "telematics_route": telematics_route,
            "delivery_proof": proof,
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
            sorted(set(ui.transportation_management_ui_contract()["action_permissions"].values()))
        )
        return ui.transportation_management_render_standalone_app(
            self.state,
            tenant=tenant,
            principal_permissions=permissions,
        )

    def release_snapshot(self) -> dict:
        from . import release_evidence

        return release_evidence.build_release_evidence()


def smoke_test() -> dict:
    """Exercise the standalone app surface end-to-end."""
    app = TransportationManagementStandaloneApp()
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
    app = TransportationManagementStandaloneApp()
    loaded = app.load_demo_workspace()
    rendered = app.render_workbench(tenant="tenant_demo")
    return {
        "ok": loaded["ok"] and rendered["ok"] and rendered["workbench"]["cards"][0]["value"] >= 1,
        "manifest": standalone_app_manifest(),
        "loaded": loaded,
        "rendered": rendered,
        "side_effects": (),
    }
