"""Standalone one-PBC application surface for capital_projects_delivery."""

from __future__ import annotations

from . import routes
from . import ui
from .release_evidence import build_release_evidence
from .runtime import CAPITAL_PROJECTS_DELIVERY_REQUIRED_EVENT_TOPIC
from .services import CapitalProjectsDeliveryService

DEFAULT_CONFIGURATION = {
    "database_backend": "postgresql",
    "event_topic": CAPITAL_PROJECTS_DELIVERY_REQUIRED_EVENT_TOPIC,
    "reporting_calendar": "monthly",
    "default_phase": "idea",
    "default_policy": "strict-stage-gate",
}
DEFAULT_PARAMETERS = {
    "workbench_limit": 50,
    "approval_sla_hours": 48,
    "risk_threshold": 0.65,
    "gate_blocker_threshold": 1,
}
DEFAULT_RULE = {
    "rule_id": "capital_projects_delivery.stage_gate_policy",
    "scope": "stage_gate",
    "severity": "blocking",
    "requires_adjacent_transition": True,
    "requires_gate_checklist": True,
}


def standalone_app_manifest() -> dict:
    return {
        "ok": True,
        "pbc": "capital_projects_delivery",
        "app": ui.capital_projects_delivery_standalone_app_contract(),
        "routes": routes.api_route_contracts()["routes"],
        "workflows": tuple(item["name"] for item in ui.capital_projects_delivery_ui_contract()["workflows"]),
        "service": CapitalProjectsDeliveryService().build_single_pbc_app_contract({})["result"],
        "side_effects": (),
    }


class CapitalProjectsDeliveryStandaloneApp:
    """Package-local standalone app that owns the capital-project runtime state."""

    def __init__(self, state: dict | None = None):
        self.service = CapitalProjectsDeliveryService(state=state)

    @property
    def state(self) -> dict:
        return self.service.state

    def dispatch(self, route: str, payload: dict | None = None) -> dict:
        return routes.dispatch_route(route, payload, service=self.service)

    def bootstrap(self, *, tenant: str = "tenant_demo") -> dict:
        self.service.configure_runtime(DEFAULT_CONFIGURATION)
        for name, value in DEFAULT_PARAMETERS.items():
            self.service.set_parameter({"name": name, "value": value})
        self.service.register_rule({**DEFAULT_RULE, "tenant": tenant})
        self.service.receive_event({
            "event_type": "PolicyChanged",
            "event_id": f"policy-{tenant}",
            "payload": {"tenant": tenant, "policy": "strict-stage-gate"},
        })
        return {"ok": True, "tenant": tenant, "state": self.state, "side_effects": ()}

    def load_demo_workspace(self, *, tenant: str = "tenant_demo") -> dict:
        self.bootstrap(tenant=tenant)
        self.dispatch(
            "POST /capital-projects",
            {
                "tenant": tenant,
                "code": f"PRJ-{tenant.upper()}",
                "name": "Standalone Capital Project",
                "reported_at": "2026-05-30",
            },
        )
        self.dispatch(
            "POST /capital-projects/{project_id}/gate-checklists",
            {
                "project_id": f"PRJ-{tenant.upper()}",
                "criteria_status": {
                    "business_case_defined": True,
                    "sponsorship_assigned": True,
                },
                "updated_by": "standalone-app",
                "updated_at": "2026-05-30",
            },
        )
        self.dispatch(
            "POST /capital-projects/{project_id}/gate-approvals",
            {
                "project_id": f"PRJ-{tenant.upper()}",
                "target_stage": "screening",
                "approver_role": "project_sponsor",
                "approved_by": "sponsor.user",
                "approved_at": "2026-05-30",
            },
        )
        return {
            "ok": True,
            "tenant": tenant,
            "workbench": self.render_workbench(tenant=tenant),
            "side_effects": (),
        }

    def render_workbench(self, *, tenant: str, principal_permissions: tuple[str, ...] | None = None) -> dict:
        permissions = principal_permissions or tuple(ui.ACTION_PERMISSIONS.values())
        return ui.capital_projects_delivery_render_standalone_app(self.state, tenant=tenant, principal_permissions=permissions)

    def release_snapshot(self) -> dict:
        return build_release_evidence()


def smoke_test() -> dict:
    app = CapitalProjectsDeliveryStandaloneApp()
    loaded = app.load_demo_workspace()
    rendered = app.render_workbench(tenant="tenant_demo")
    release_snapshot = app.release_snapshot()
    return {
        "ok": loaded["ok"] and rendered["ok"] and rendered["workbench"]["summary_cards"][0]["value"] >= 1 and release_snapshot["ok"],
        "manifest": standalone_app_manifest(),
        "loaded": loaded,
        "rendered": rendered,
        "release_snapshot": release_snapshot,
        "side_effects": (),
    }
