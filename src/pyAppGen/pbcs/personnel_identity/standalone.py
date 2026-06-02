"""Standalone one-PBC application surface for personnel_identity."""

from __future__ import annotations

from . import repository
from . import routes
from . import ui
from .runtime import personnel_identity_assign_role
from .runtime import personnel_identity_configure_runtime
from .runtime import personnel_identity_create_employee
from .runtime import personnel_identity_empty_state
from .runtime import personnel_identity_generate_eligibility_proof
from .runtime import personnel_identity_receive_event
from .runtime import personnel_identity_register_department
from .runtime import personnel_identity_register_rule
from .runtime import personnel_identity_register_schema_extension
from .runtime import personnel_identity_route_provisioning
from .runtime import personnel_identity_run_control_tests
from .runtime import personnel_identity_screen_policy
from .runtime import personnel_identity_score_access_risk
from .runtime import personnel_identity_set_parameter
from .runtime import personnel_identity_transition_employee_status
from .runtime import personnel_identity_upsert_identity_attribute
from .seed_data import demo_workspace_seed_bundle


def standalone_app_manifest() -> dict:
    """Return the executable standalone-app contribution from the package."""
    return {"ok": True, "pbc": "personnel_identity", "app": ui.personnel_identity_standalone_app_contract(), "routes": routes.api_route_contracts()["routes"], "repository": repository.personnel_identity_repository_contract(), "side_effects": ()}


class PersonnelIdentityStandaloneApp:
    """Package-local standalone app that owns personnel identity runtime state."""

    def __init__(self, state: dict | None = None):
        self.state = state or personnel_identity_empty_state()
        self.repository = repository.PersonnelIdentityRepository(self.state)

    def _commit(self, result: dict) -> dict:
        if result.get("state") is not None:
            self.state = result["state"]
            self.repository.state = self.state
        return result

    def bootstrap(self, *, tenant: str = "tenant_demo") -> dict:
        bundle = demo_workspace_seed_bundle(tenant=tenant)
        self._commit(personnel_identity_configure_runtime(self.state, bundle["configuration"]))
        for name, value in bundle["parameters"].items():
            self._commit(personnel_identity_set_parameter(self.state, name, value))
        self._commit(personnel_identity_register_rule(self.state, bundle["rule"]))
        self._commit(personnel_identity_register_schema_extension(self.state, "personnel_employee", {"credential_payload": "jsonb", "privacy_payload": "jsonb"}))
        for event in bundle["projection_events"]:
            self._commit(personnel_identity_receive_event(self.state, event))
        return {"ok": True, "tenant": tenant, "state": self.state, "repository": self.repository.read_model(tenant), "side_effects": ()}

    def load_demo_workspace(self, *, tenant: str = "tenant_demo") -> dict:
        bundle = demo_workspace_seed_bundle(tenant=tenant)
        self.bootstrap(tenant=tenant)
        self._commit(personnel_identity_register_department(self.state, bundle["department"]))
        self._commit(personnel_identity_create_employee(self.state, bundle["manager"]))
        employee = self._commit(personnel_identity_create_employee(self.state, bundle["employee"]))
        self._commit(personnel_identity_transition_employee_status(self.state, employee["employee"]["employee_id"], status="active", changed_by="people.ops"))
        self._commit(personnel_identity_assign_role(self.state, employee["employee"]["employee_id"], role="employee_self_service", scope="global", assigned_by="iam.admin"))
        for name, value, assurance in bundle["attributes"]:
            self._commit(personnel_identity_upsert_identity_attribute(self.state, employee["employee"]["employee_id"], name, value, assurance=assurance))
        risk = personnel_identity_score_access_risk(self.state, employee["employee"]["employee_id"])
        policy = personnel_identity_screen_policy(self.state, employee["employee"]["employee_id"], restricted_roles=("payroll_admin",))
        provisioning_route = personnel_identity_route_provisioning({"provisioning_id": f"prov_{tenant}_001"}, rails=({"route": "directory_api", "available": False, "latency": 1}, {"route": "appgen_outbox", "available": True, "latency": 3}))
        proof = personnel_identity_generate_eligibility_proof(self.state, employee["employee"]["employee_id"], disclosure=("employee_id", "department_id", "status", "worker_type"))
        controls = personnel_identity_run_control_tests(self.state)
        return {"ok": controls["ok"] and policy["ok"] and provisioning_route["ok"] and proof["ok"] and risk["ok"], "tenant": tenant, "workbench": self.render_workbench(tenant=tenant), "repository": self.repository.read_model(tenant), "risk": risk, "policy": policy, "provisioning_route": provisioning_route, "eligibility_proof": proof, "controls": controls, "side_effects": ()}

    def render_workbench(self, *, tenant: str, principal_permissions: tuple[str, ...] | None = None) -> dict:
        permissions = principal_permissions or tuple(sorted(set(ui.personnel_identity_ui_contract()["action_permissions"].values())))
        return ui.personnel_identity_render_standalone_app(self.state, tenant=tenant, principal_permissions=permissions)

    def release_snapshot(self) -> dict:
        from . import release_evidence

        return release_evidence.build_release_evidence()


def smoke_test() -> dict:
    """Exercise the standalone app surface end-to-end."""
    app = PersonnelIdentityStandaloneApp()
    loaded = app.load_demo_workspace()
    rendered = app.render_workbench(tenant="tenant_demo")
    release_snapshot = app.release_snapshot()
    return {"ok": loaded["ok"] and rendered["ok"] and rendered["workbench"]["cards"][1]["value"] >= 1 and release_snapshot["ok"], "manifest": standalone_app_manifest(), "loaded": loaded, "rendered": rendered, "release_snapshot": release_snapshot, "side_effects": ()}


def workbench_smoke_test() -> dict:
    """Exercise bootstrap and rendering without release recursion."""
    app = PersonnelIdentityStandaloneApp()
    loaded = app.load_demo_workspace()
    rendered = app.render_workbench(tenant="tenant_demo")
    return {"ok": loaded["ok"] and rendered["ok"] and rendered["workbench"]["cards"][1]["value"] >= 1, "manifest": standalone_app_manifest(), "loaded": loaded, "rendered": rendered, "side_effects": ()}
