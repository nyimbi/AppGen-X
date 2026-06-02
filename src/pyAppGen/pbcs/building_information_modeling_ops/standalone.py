"""Standalone one-PBC application surface for building_information_modeling_ops."""

from __future__ import annotations

from . import routes
from . import ui
from .agent import assistant_help, datastore_crud_plan, document_instruction_plan
from .config import governance_smoke_test
from .permissions import authorize, permission_manifest
from .runtime import (
    BUILDING_INFORMATION_MODELING_OPS_REQUIRED_EVENT_TOPIC,
    building_information_modeling_ops_build_release_evidence,
)
from .services import BuildingInformationModelingOpsService, service_operation_manifest

DEFAULT_CONFIGURATION = {
    "database_backend": "postgresql",
    "event_topic": BUILDING_INFORMATION_MODELING_OPS_REQUIRED_EVENT_TOPIC,
    "retry_limit": 5,
    "default_policy": "federation_release",
}
DEFAULT_PARAMETERS = {
    "quality_score_floor": 0.8,
    "materiality_threshold": 0.15,
    "approval_sla_hours": 48,
    "risk_threshold": 0.25,
    "forecast_horizon_days": 14,
    "workbench_limit": 100,
}
DEFAULT_RULE = {
    "rule_id": "building_information_modeling_ops.release_gate",
    "scope": "federation_release",
    "status": "active",
    "required_issue_purposes": ("shared", "construction", "record", "handover"),
    "coordinate_tolerance_mm": 25.0,
    "rotation_tolerance_degrees": 0.5,
}
DEFAULT_PROJECT_COORDINATES = {
    "coordinate_basis": "project-grid-a",
    "survey_point": {"x": 1000, "y": 2000, "z": 15},
    "project_base_point": {"x": 995, "y": 1995, "z": 15},
    "true_north_degrees": 12.0,
    "elevation_datum": "msl",
    "unit_scale": 1.0,
}
DEFAULT_MODEL_PACKAGES = (
    {
        "model_id": "MODEL-A",
        "version_id": "VER-A1",
        "discipline": "architectural",
        "authoring_party": "Design Studio",
        "coordinate_basis": "project-grid-a",
        "survey_point": {"x": 1002, "y": 2003, "z": 15},
        "project_base_point": {"x": 997, "y": 1996, "z": 15},
        "true_north_degrees": 12.1,
        "elevation_datum": "msl",
        "unit_scale": 1.0,
        "issue_purpose": "shared",
        "spatial_coverage": ("tower-a", "levels-01-05"),
        "lod_target": "LOD-300",
        "approval_state": "approved",
        "checksum": "sha256:ver-a1",
    },
    {
        "model_id": "MODEL-S",
        "version_id": "VER-S1",
        "discipline": "structural",
        "authoring_party": "Structural Partners",
        "coordinate_basis": "project-grid-a",
        "survey_point": {"x": 1001, "y": 2001, "z": 15},
        "project_base_point": {"x": 996, "y": 1996, "z": 15},
        "true_north_degrees": 12.0,
        "elevation_datum": "msl",
        "unit_scale": 1.0,
        "issue_purpose": "construction",
        "spatial_coverage": ("tower-a", "levels-01-05"),
        "lod_target": "LOD-350",
        "approval_state": "approved",
        "checksum": "sha256:ver-s1",
    },
)


def _permission_for_action(action: str) -> str:
    permission_by_action = {
        "create": "building_information_modeling_ops.create",
        "update": "building_information_modeling_ops.update",
        "delete": "building_information_modeling_ops.admin",
        "approve": "building_information_modeling_ops.approve",
    }
    return permission_by_action.get(action, "building_information_modeling_ops.read")


def standalone_app_manifest() -> dict:
    service = service_operation_manifest()
    ui_contract = ui.building_information_modeling_ops_ui_contract()
    return {
        "ok": True,
        "pbc": "building_information_modeling_ops",
        "app": ui_contract,
        "routes": routes.api_route_contracts()["contracts"],
        "service": service,
        "permissions": permission_manifest(),
        "assistant": {
            "help": assistant_help(),
            "document_instruction_planning": True,
            "datastore_crud_planning": True,
        },
        "release_ready": building_information_modeling_ops_build_release_evidence()["ok"],
        "side_effects": (),
    }


class BuildingInformationModelingOpsStandaloneApp:
    """Package-local executable app wrapper for the BIM federation slice."""

    def __init__(self, state: dict | None = None):
        self.service = BuildingInformationModelingOpsService(state=state)

    @property
    def state(self) -> dict:
        return self.service.state

    def dispatch(self, route: str, payload: dict | None = None) -> dict:
        contract = routes.dispatch_route(route, payload)
        if not contract["ok"]:
            return contract
        result = getattr(self.service, contract["operation"])(payload or {})
        return {
            **contract,
            "result": result,
            "state": self.state,
            "side_effects": (),
        }

    def bootstrap(self, *, tenant: str = "tenant_demo") -> dict:
        self.service.configure_runtime(DEFAULT_CONFIGURATION)
        for name, value in DEFAULT_PARAMETERS.items():
            self.service.set_parameter({"name": name, "value": value})
        self.service.register_rule({**DEFAULT_RULE, "tenant": tenant})
        return {
            "ok": True,
            "tenant": tenant,
            "configuration": DEFAULT_CONFIGURATION,
            "governance": governance_smoke_test(),
            "side_effects": (),
        }

    def load_demo_workspace(self, *, tenant: str = "tenant_demo") -> dict:
        self.bootstrap(tenant=tenant)
        self.dispatch(
            "POST /federations/project-coordinates",
            {"tenant": tenant, **DEFAULT_PROJECT_COORDINATES},
        )
        for package in DEFAULT_MODEL_PACKAGES:
            self.dispatch(
                "POST /federations/model-packages",
                {"tenant": tenant, **package},
            )
        federation = self.dispatch(
            "POST /federations/assemblies",
            {
                "tenant": tenant,
                "federation_id": "FED-01",
                "version_ids": tuple(package["version_id"] for package in DEFAULT_MODEL_PACKAGES),
                "intended_use": "coordination",
            },
        )
        return {
            "ok": federation["result"]["ok"],
            "tenant": tenant,
            "federation": federation["result"],
            "workbench": self.render_workbench(),
            "side_effects": (),
        }

    def plan_document_instruction(
        self,
        document: str,
        instruction: str,
        *,
        actor: dict | None = None,
    ) -> dict:
        action = "create" if "create" in instruction.lower() else "read"
        return {
            "ok": True,
            "plan": document_instruction_plan(document, instruction),
            "authorization": authorize(_permission_for_action(action), actor=actor),
            "side_effects": (),
        }

    def plan_datastore_crud(
        self,
        action: str,
        *,
        table: str | None = None,
        payload: dict | None = None,
        actor: dict | None = None,
    ) -> dict:
        plan = datastore_crud_plan(action, table=table, payload=payload)
        return {
            "ok": plan["ok"],
            "plan": plan,
            "authorization": authorize(_permission_for_action(action), actor=actor),
            "side_effects": (),
        }

    def render_workbench(self, filters: dict | None = None) -> dict:
        query = self.service.query_workbench(filters or {})
        ui_contract = ui.building_information_modeling_ops_ui_contract()
        return {
            "ok": query["ok"] and ui_contract["ok"],
            "app": ui_contract,
            "workbench": query["workbench"],
            "filters": query["filters"],
            "side_effects": (),
        }

    def release_snapshot(self) -> dict:
        from .release_evidence import build_release_evidence

        return build_release_evidence()


def smoke_test() -> dict:
    app = BuildingInformationModelingOpsStandaloneApp()
    loaded = app.load_demo_workspace()
    document_plan = app.plan_document_instruction(
        "Issued for coordination transmittal.",
        "Create a reviewed federation release checklist.",
    )
    crud_plan = app.plan_datastore_crud(
        "create",
        table="building_information_modeling_ops_model_version",
        payload={"version_id": "VER-A2"},
    )
    release = app.release_snapshot()
    return {
        "ok": loaded["ok"]
        and loaded["workbench"]["ok"]
        and loaded["workbench"]["workbench"]["kpis"]["active_federations"] == 1
        and document_plan["ok"]
        and crud_plan["ok"]
        and release["ok"],
        "manifest": standalone_app_manifest(),
        "loaded": loaded,
        "document_plan": document_plan,
        "crud_plan": crud_plan,
        "release": release,
        "side_effects": (),
    }
