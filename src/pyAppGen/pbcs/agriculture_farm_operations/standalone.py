"""Standalone one-PBC application surface for agriculture_farm_operations."""

from __future__ import annotations

from . import routes, ui
from .agent import composed_agent_contribution, datastore_crud_plan, document_instruction_plan
from .permissions import permission_manifest
from .runtime import AGRICULTURE_FARM_OPERATIONS_REQUIRED_EVENT_TOPIC
from .services import AgricultureFarmOperationsService, service_operation_contracts

DEFAULT_CONFIGURATION = {
    "database_backend": "postgresql",
    "event_topic": AGRICULTURE_FARM_OPERATIONS_REQUIRED_EVENT_TOPIC,
    "retry_limit": 5,
    "default_region": "east-africa",
    "calendar_profile": "seasonal",
    "workbench_limit": 100,
}
DEFAULT_PARAMETERS = {
    "workbench_limit": 100,
    "risk_threshold": 0.6,
    "window_alert_threshold_days": 3,
    "approval_sla_hours": 24,
}
DEFAULT_RULE = {
    "rule_id": "agriculture_farm_operations.crop_plan.release_gate",
    "tenant": "tenant_demo",
    "scope": "crop_plan",
    "status": "active",
    "required_readiness_checks": ("soil_fit", "fertility_ready", "equipment_ready", "crew_assigned"),
}


def standalone_app_manifest() -> dict:
    return {
        "ok": True,
        "pbc": "agriculture_farm_operations",
        "app": ui.agriculture_farm_operations_standalone_app_contract(),
        "routes": routes.api_route_contracts()["routes"],
        "service": service_operation_contracts(),
        "side_effects": (),
    }


class AgricultureFarmOperationsStandaloneApp:
    def __init__(self, state: dict | None = None):
        self.service = AgricultureFarmOperationsService(state=state)

    @property
    def state(self) -> dict:
        return self.service.state

    def dispatch(self, method: str, path: str, payload: dict | None = None) -> dict:
        return routes.dispatch_route(method, path, payload, service=self.service)

    def bootstrap(self, *, tenant: str = "tenant_demo") -> dict:
        self.dispatch(
            "POST",
            "/api/pbc/agriculture_farm_operations/runtime/configuration",
            {"configuration": DEFAULT_CONFIGURATION},
        )
        for name, value in DEFAULT_PARAMETERS.items():
            self.dispatch(
                "POST",
                "/api/pbc/agriculture_farm_operations/runtime/parameters",
                {"name": name, "value": value},
            )
        self.dispatch(
            "POST",
            "/api/pbc/agriculture_farm_operations/runtime/rules",
            {"rule": {**DEFAULT_RULE, "tenant": tenant}},
        )
        self.dispatch(
            "POST",
            "/api/pbc/agriculture_farm_operations/events/inbox",
            {
                "envelope": {
                    "event_type": "PolicyChanged",
                    "event_id": f"policy-{tenant}",
                    "payload": {"tenant": tenant, "policy": "crop-plan-release"},
                }
            },
        )
        return {"ok": True, "tenant": tenant, "state": self.state, "side_effects": ()}

    def load_demo_workspace(self, *, tenant: str = "tenant_demo") -> dict:
        self.bootstrap(tenant=tenant)
        self.dispatch(
            "POST",
            "/api/pbc/agriculture_farm_operations/fields",
            {
                "field": {
                    "tenant": tenant,
                    "field_id": f"field-{tenant}",
                    "code": "FIELD-001",
                    "name": "North Farm",
                    "region": "east-africa",
                    "acreage": 180,
                    "management_zones": ("north-block", "south-block"),
                }
            },
        )
        self.dispatch(
            "POST",
            "/api/pbc/agriculture_farm_operations/crop-plans",
            {
                "tenant": tenant,
                "field_id": f"field-{tenant}",
                "management_zone": "north-block",
                "crop": "maize",
                "season": "long_rains",
                "market_year": 2026,
                "planting_date": "2026-04-24",
                "planned_start": "2026-04-24",
                "planned_end": "2026-09-15",
                "planting_window": {
                    "start": "2026-04-10",
                    "optimal_start": "2026-04-20",
                    "optimal_end": "2026-05-05",
                    "latest": "2026-05-15",
                    "minimum_soil_temperature_c": 12,
                    "maximum_frost_risk": 0.2,
                    "minimum_rainfall_outlook_mm": 20,
                    "requires_irrigation_ready": True,
                },
                "conditions": {
                    "soil_temperature_c": 15,
                    "frost_risk": 0.05,
                    "rainfall_outlook_mm": 22,
                },
                "readiness": {
                    "soil_fit": True,
                    "fertility_ready": True,
                    "equipment_ready": True,
                    "crew_assigned": True,
                    "irrigation_ready": True,
                },
            },
        )
        return {
            "ok": True,
            "tenant": tenant,
            "workbench": self.render_workbench(tenant=tenant),
            "side_effects": (),
        }

    def assistant_workspace(self, *, tenant: str = "tenant_demo") -> dict:
        return {
            "ok": True,
            "tenant": tenant,
            "agent": composed_agent_contribution(),
            "document_plan": document_instruction_plan(
                "Scout note: use north-block for maize.",
                "Create a crop-plan draft.",
                {"tenant": tenant, "field_id": f"field-{tenant}", "crop": "maize", "season": "long_rains"},
            ),
            "crud_plan": datastore_crud_plan(
                "create",
                table="agriculture_farm_operations_crop_plan",
                payload={"tenant": tenant, "field_id": f"field-{tenant}"},
            ),
            "side_effects": (),
        }

    def render_workbench(self, *, tenant: str, principal_permissions: tuple[str, ...] | None = None) -> dict:
        permissions = principal_permissions or permission_manifest()["permissions"]
        return ui.agriculture_farm_operations_render_standalone_app(
            self.state,
            tenant=tenant,
            principal_permissions=permissions,
        )

    def release_snapshot(self) -> dict:
        from . import release_evidence

        return release_evidence.build_release_evidence()


def smoke_test() -> dict:
    app = AgricultureFarmOperationsStandaloneApp()
    loaded = app.load_demo_workspace()
    rendered = app.render_workbench(tenant="tenant_demo")
    assistant = app.assistant_workspace()
    release_snapshot = app.release_snapshot()
    return {
        "ok": loaded["ok"]
        and rendered["ok"]
        and rendered["workbench"]["cards"][0]["value"] >= 1
        and assistant["ok"]
        and release_snapshot["ok"],
        "manifest": standalone_app_manifest(),
        "loaded": loaded,
        "rendered": rendered,
        "assistant": assistant,
        "release_snapshot": release_snapshot,
        "side_effects": (),
    }
