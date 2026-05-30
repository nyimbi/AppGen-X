"""Standalone one-PBC application surface for procurement_sourcing."""

from __future__ import annotations

from . import repository
from . import routes
from . import ui
from .runtime import procurement_sourcing_approve_requisition
from .runtime import procurement_sourcing_capture_bid
from .runtime import procurement_sourcing_configure_runtime
from .runtime import procurement_sourcing_create_contract
from .runtime import procurement_sourcing_create_requisition
from .runtime import procurement_sourcing_create_rfq
from .runtime import procurement_sourcing_empty_state
from .runtime import procurement_sourcing_generate_supplier_compliance_proof
from .runtime import procurement_sourcing_issue_purchase_order
from .runtime import procurement_sourcing_receive_event
from .runtime import procurement_sourcing_register_rule
from .runtime import procurement_sourcing_register_schema_extension
from .runtime import procurement_sourcing_route_purchase_order
from .runtime import procurement_sourcing_run_control_tests
from .runtime import procurement_sourcing_score_suppliers
from .runtime import procurement_sourcing_screen_policy
from .runtime import procurement_sourcing_select_supplier
from .runtime import procurement_sourcing_set_parameter
from .seed_data import demo_workspace_seed_bundle


def standalone_app_manifest() -> dict:
    """Return the executable standalone-app contribution from the package."""
    return {
        "ok": True,
        "pbc": "procurement_sourcing",
        "app": ui.procurement_sourcing_standalone_app_contract(),
        "routes": routes.api_route_contracts()["routes"],
        "repository": repository.procurement_sourcing_repository_contract(),
        "side_effects": (),
    }


class ProcurementSourcingStandaloneApp:
    """Package-local standalone app that owns the procurement runtime state."""

    def __init__(self, state: dict | None = None):
        self.state = state or procurement_sourcing_empty_state()
        self.repository = repository.ProcurementSourcingRepository(self.state)

    def _commit(self, result: dict) -> dict:
        if result.get("state") is not None:
            self.state = result["state"]
            self.repository.state = self.state
        return result

    def bootstrap(self, *, tenant: str = "tenant_demo") -> dict:
        bundle = demo_workspace_seed_bundle(tenant=tenant)
        self._commit(procurement_sourcing_configure_runtime(self.state, bundle["configuration"]))
        for name, value in bundle["parameters"].items():
            self._commit(procurement_sourcing_set_parameter(self.state, name, value))
        self._commit(procurement_sourcing_register_rule(self.state, bundle["rule"]))
        self._commit(
            procurement_sourcing_register_schema_extension(
                self.state,
                "procurement_sourcing_rfq",
                {"sustainability_payload": "jsonb", "supplier_identity_payload": "jsonb"},
            )
        )
        for event in bundle["projection_events"]:
            self._commit(procurement_sourcing_receive_event(self.state, event))
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
        requisition = self._commit(procurement_sourcing_create_requisition(self.state, bundle["requisition"]))
        self._commit(
            procurement_sourcing_approve_requisition(
                self.state,
                requisition["requisition"]["requisition_id"],
                approver="procurement.manager",
            )
        )
        self._commit(
            procurement_sourcing_create_rfq(
                self.state,
                bundle["rfq_id"],
                requisition_id=bundle["requisition"]["requisition_id"],
                suppliers=bundle["suppliers"],
            )
        )
        for bid in bundle["bids"]:
            self._commit(procurement_sourcing_capture_bid(self.state, bundle["rfq_id"], bid))
        scores = procurement_sourcing_score_suppliers(self.state, bundle["rfq_id"])
        selection = self._commit(
            procurement_sourcing_select_supplier(
                self.state,
                bundle["rfq_id"],
                award_id=bundle["award_id"],
            )
        )
        contract = self._commit(
            procurement_sourcing_create_contract(
                self.state,
                bundle["contract_id"],
                award_id=selection["award"]["award_id"],
                term_months=12,
            )
        )
        purchase_order = self._commit(
            procurement_sourcing_issue_purchase_order(
                self.state,
                bundle["po_id"],
                contract_id=contract["contract"]["contract_id"],
                quantity=bundle["requisition"]["quantity"],
                amount=selection["award"]["amount"],
            )
        )
        policy = procurement_sourcing_screen_policy(
            self.state,
            purchase_order["purchase_order"]["po_id"],
            restricted_suppliers=("supplier_sanctioned",),
        )
        route = procurement_sourcing_route_purchase_order(
            purchase_order["purchase_order"],
            rails=(
                {"route": "supplier_api", "available": False, "latency": 1},
                {"route": "appgen_outbox", "available": True, "latency": 3},
            ),
        )
        proof = procurement_sourcing_generate_supplier_compliance_proof(
            self.state,
            selection["award"]["supplier_id"],
            disclosure=("supplier_id", "risk", "quality"),
        )
        controls = procurement_sourcing_run_control_tests(self.state)
        return {
            "ok": controls["ok"] and policy["ok"] and route["ok"] and proof["ok"] and scores["ok"],
            "tenant": tenant,
            "workbench": self.render_workbench(tenant=tenant),
            "repository": self.repository.read_model(tenant),
            "scores": scores,
            "policy": policy,
            "route": route,
            "supplier_compliance_proof": proof,
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
            sorted(set(ui.procurement_sourcing_ui_contract()["action_permissions"].values()))
        )
        return ui.procurement_sourcing_render_standalone_app(
            self.state,
            tenant=tenant,
            principal_permissions=permissions,
        )

    def release_snapshot(self) -> dict:
        from . import release_evidence

        return release_evidence.build_release_evidence()


def smoke_test() -> dict:
    """Exercise the standalone app surface end-to-end."""
    app = ProcurementSourcingStandaloneApp()
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
    app = ProcurementSourcingStandaloneApp()
    loaded = app.load_demo_workspace()
    rendered = app.render_workbench(tenant="tenant_demo")
    return {
        "ok": loaded["ok"] and rendered["ok"] and rendered["workbench"]["cards"][0]["value"] >= 1,
        "manifest": standalone_app_manifest(),
        "loaded": loaded,
        "rendered": rendered,
        "side_effects": (),
    }
