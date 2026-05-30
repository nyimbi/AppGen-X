"""Standalone one-PBC application surface for Mining Operations Management."""

from __future__ import annotations

import hashlib
from copy import deepcopy

from . import agent
from . import controls
from . import forms
from . import runtime
from . import ui
from . import wizards
from .domain_depth import execute_domain_operation
from .routes import dispatch_standalone_route
from .routes import standalone_route_contracts


PBC_KEY = "mining_operations_management"

DEFAULT_CONFIGURATION = {
    "database_backend": "postgresql",
    "event_topic": runtime.MINING_OPERATIONS_MANAGEMENT_REQUIRED_EVENT_TOPIC,
    "default_policy": "mining_operations_default",
    "retry_limit": 5,
    "confirmation_required_for_mutation": True,
    "workbench_limit": 24,
}

DEFAULT_PARAMETERS = {
    "quality_score_floor": 0.62,
    "materiality_threshold": 0.12,
    "approval_sla_hours": 4,
    "risk_threshold": 0.7,
    "forecast_horizon_days": 14,
    "workbench_limit": 24,
}

DEFAULT_RULES = (
    {
        "rule_id": "mine_plan_policy.default",
        "scope": "mine_plan_policy",
        "status": "active",
        "requires_shift_targets": True,
        "requires_plan_hierarchy": True,
    },
    {
        "rule_id": "dispatch_assignment.default",
        "scope": "haulage_cycle_policy",
        "status": "active",
        "closed_route_blocks_assignment": True,
        "approved_area_match_required": True,
    },
    {
        "rule_id": "ore_boundary.default",
        "scope": "ore_quality_policy",
        "status": "active",
        "destination_change_requires_approval": True,
        "stockpile_lineage_required": True,
    },
)

PROJECTION_KEYS = (
    "mine_plans",
    "blast_packets",
    "shift_targets",
    "fleet_assets",
    "dispatch_assignments",
    "ore_boundary_decisions",
    "stockpile_movements",
    "geotech_access_zones",
    "shift_handovers",
)


def _digest(value: object) -> str:
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()


def _normalize_iterable(value) -> tuple:
    if value is None:
        return ()
    if isinstance(value, (list, tuple)):
        return tuple(value)
    return (value,)


def _base_state() -> dict:
    state = runtime.mining_operations_management_empty_state()
    for key in PROJECTION_KEYS:
        state[key] = {}
    return state


def standalone_documentation_presence() -> dict:
    return {
        "ok": True,
        "required_docs": ("SPECIFICATION.md", "improve1.md", "implementation-plan.md", "RELEASE_EVIDENCE.md"),
        "side_effects": (),
    }


class MiningOperationsManagementStandaloneApp:
    """Deterministic standalone app for mine-plan-to-shift workflows."""

    def __init__(self, *, initial_state: dict | None = None) -> None:
        self.state = _base_state() if initial_state is None else deepcopy(initial_state)

    def configure(self, config: dict | None = None) -> dict:
        result = runtime.mining_operations_management_configure_runtime(
            self.state,
            {**DEFAULT_CONFIGURATION, **dict(config or {})},
        )
        self.state = result["state"]
        return {
            "ok": result["ok"],
            "pbc": PBC_KEY,
            "configuration": result["configuration"],
            "side_effects": (),
        }

    def register_defaults(self) -> dict:
        configured = self.configure()
        steps = [configured]
        for name, value in DEFAULT_PARAMETERS.items():
            result = runtime.mining_operations_management_set_parameter(self.state, name, value)
            self.state = result["state"]
            steps.append(result)
        for rule in DEFAULT_RULES:
            result = runtime.mining_operations_management_register_rule(self.state, rule)
            self.state = result["state"]
            steps.append(result)
        return {
            "ok": all(step["ok"] for step in steps),
            "pbc": PBC_KEY,
            "configured": configured["configuration"],
            "parameter_count": len(DEFAULT_PARAMETERS),
            "rule_count": len(DEFAULT_RULES),
            "side_effects": (),
        }

    def submit_form(self, form_id: str, payload: dict | None = None) -> dict:
        payload = dict(payload or {})
        form = forms.mining_operations_management_get_form(form_id).get("form")
        validation = forms.mining_operations_management_validate_form_payload(form_id, payload)
        if form is None or not validation["ok"]:
            return {
                "ok": False,
                "pbc": PBC_KEY,
                "form_id": form_id,
                "validation": validation,
                "side_effects": (),
            }

        operation = form["operation"]
        domain_plan = execute_domain_operation(operation, payload)
        projection_name = form["projection"]
        projection = dict(self.state.get(projection_name, {}))
        record_id_field = form["record_id_field"]
        record_id = str(payload.get(record_id_field) or f"{form_id}_{len(projection) + 1:04d}")
        record = {
            "record_id": record_id,
            "tenant": payload.get("tenant", "default"),
            "form_id": form_id,
            "operation": operation,
            "target_table": form["target_table"],
            "owned_tables": form["owned_tables"],
            "payload": {
                **payload,
                "approved_areas": _normalize_iterable(payload.get("approved_areas")),
                "allowed_equipment": _normalize_iterable(payload.get("allowed_equipment")),
                "open_issues": _normalize_iterable(payload.get("open_issues")),
            },
            "domain_plan": domain_plan,
            "status": payload.get("status", "recorded"),
            "sequence": len(projection) + 1,
            "evidence_hash": _digest((form_id, record_id, payload, domain_plan.get("evidence_hash"))),
        }
        projection[record_id] = record
        self.state[projection_name] = projection
        self.state["records"][record_id] = record
        self.state["outbox"].append(
            {
                "event_type": domain_plan.get("emitted_event", runtime.MINING_OPERATIONS_MANAGEMENT_EMITTED_EVENT_TYPES[0]),
                "topic": runtime.MINING_OPERATIONS_MANAGEMENT_REQUIRED_EVENT_TOPIC,
                "idempotency_key": domain_plan.get("idempotency_key", _digest((form_id, record_id))),
                "payload": {
                    "form_id": form_id,
                    "record_id": record_id,
                    "tenant": record["tenant"],
                    "target_table": record["target_table"],
                },
            }
        )
        return {
            "ok": True,
            "pbc": PBC_KEY,
            "form_id": form_id,
            "record": record,
            "validation": validation,
            "side_effects": (),
        }

    def plan_wizard(self, wizard_id: str, context: dict | None = None) -> dict:
        return wizards.mining_operations_management_plan_wizard(wizard_id, context)

    def control_center(self) -> dict:
        return controls.mining_operations_management_control_center(self.state)

    def build_workbench(self, tenant: str = "default") -> dict:
        def _values(name: str) -> tuple[dict, ...]:
            return tuple(
                item
                for item in self.state.get(name, {}).values()
                if item.get("tenant", "default") == tenant
            )

        mine_plans = _values("mine_plans")
        blast_packets = _values("blast_packets")
        shift_targets = _values("shift_targets")
        fleet_assets = _values("fleet_assets")
        dispatch_assignments = _values("dispatch_assignments")
        ore_boundary_decisions = _values("ore_boundary_decisions")
        stockpile_movements = _values("stockpile_movements")
        geotech_access_zones = _values("geotech_access_zones")
        shift_handovers = _values("shift_handovers")
        return {
            "ok": True,
            "pbc": PBC_KEY,
            "tenant": tenant,
            "plan_count": len(mine_plans),
            "blast_packet_count": len(blast_packets),
            "pending_blast_clearance_count": len(
                tuple(
                    item
                    for item in blast_packets
                    if not item["payload"].get("clearance_confirmed")
                    or item["payload"].get("re_entry_status") != "released"
                )
            ),
            "shift_target_count": len(shift_targets),
            "fleet_asset_count": len(fleet_assets),
            "dispatch_assignment_count": len(dispatch_assignments),
            "ore_boundary_decision_count": len(ore_boundary_decisions),
            "stockpile_movement_count": len(stockpile_movements),
            "stockpile_tonnes_delta": round(
                sum(float(item["payload"].get("tonnes_delta", 0.0)) for item in stockpile_movements),
                2,
            ),
            "blocked_area_count": len(
                tuple(item for item in geotech_access_zones if item["payload"].get("access_state") == "blocked")
            ),
            "conditional_area_count": len(
                tuple(item for item in geotech_access_zones if item["payload"].get("access_state") == "conditional")
            ),
            "open_handover_count": len(
                tuple(item for item in shift_handovers if item["payload"].get("status") == "open")
            ),
            "outbox_count": len(self.state.get("outbox", ())),
            "risk_flags": tuple(
                dict.fromkeys(
                    list(
                        tuple(
                            "blast_clearance_hold"
                            for item in blast_packets
                            if not item["payload"].get("clearance_confirmed")
                        )
                    )
                    + list(
                        tuple(
                            "blocked_ground"
                            for item in geotech_access_zones
                            if item["payload"].get("access_state") == "blocked"
                        )
                    )
                )
            ),
            "side_effects": (),
        }


def mining_operations_management_standalone_app_contract() -> dict:
    route_manifest = standalone_route_contracts()
    form_catalog = forms.mining_operations_management_form_catalog()
    wizard_catalog = wizards.mining_operations_management_wizard_catalog()
    control_catalog = controls.mining_operations_management_control_catalog()
    ui_blueprint = ui.mining_operations_management_standalone_workbench_blueprint()
    agent_contract = agent.chatbot_interface_contract()
    return {
        "format": "appgen.mining-operations-management-standalone-app.v1",
        "ok": all(
            item.get("ok") is True
            for item in (route_manifest, form_catalog, wizard_catalog, control_catalog, ui_blueprint, agent_contract)
        ),
        "pbc": PBC_KEY,
        "app_class": "MiningOperationsManagementStandaloneApp",
        "routes": route_manifest,
        "forms": form_catalog,
        "wizards": wizard_catalog,
        "controls": control_catalog,
        "ui": ui_blueprint,
        "agent": agent_contract,
        "documentation": standalone_documentation_presence(),
        "side_effects": (),
    }


def mining_operations_management_bootstrap_standalone_app() -> dict:
    app = MiningOperationsManagementStandaloneApp()
    registered = app.register_defaults()
    return {
        "ok": registered["ok"],
        "pbc": PBC_KEY,
        "app": app,
        "contract": mining_operations_management_standalone_app_contract(),
        "side_effects": (),
    }


def mining_operations_management_standalone_smoke() -> dict:
    bundle = mining_operations_management_bootstrap_standalone_app()
    app = bundle["app"]
    plan = dispatch_standalone_route(
        "POST",
        "/app/mining-operations-management/forms/mine-plan-hierarchy-intake",
        {
            "tenant": "tenant-smoke",
            "plan_id": "plan_smoke",
            "plan_period": "2026-W22",
            "mining_method": "open_pit",
            "pit_phase": "Phase-2",
            "bench_or_stope": "Bench-4505",
            "planned_tonnes": 180000,
            "planned_grade": 1.72,
            "ore_destination": "crusher",
        },
        app=app,
    )
    fleet = dispatch_standalone_route(
        "POST",
        "/app/mining-operations-management/forms/fleet-capability-card",
        {
            "tenant": "tenant-smoke",
            "fleet_asset_id": "truck_smoke",
            "equipment_class": "truck",
            "payload_band": "220t",
            "approved_areas": ("PB-05", "PB-06"),
            "availability_state": "available",
            "fuel_type": "diesel",
        },
        app=app,
    )
    dispatch = dispatch_standalone_route(
        "POST",
        "/app/mining-operations-management/forms/dispatch-assignment",
        {
            "tenant": "tenant-smoke",
            "dispatch_id": "dispatch_smoke",
            "shift_id": "shift_smoke",
            "fleet_asset_id": "truck_smoke",
            "mining_area": "PB-05",
            "route_status": "open",
            "material_destination": "crusher",
            "queue_length": 2,
        },
        app=app,
    )
    controls_view = dispatch_standalone_route(
        "GET",
        "/app/mining-operations-management/controls",
        app=app,
    )
    workbench = dispatch_standalone_route(
        "GET",
        "/app/mining-operations-management/workbench",
        {"tenant": "tenant-smoke"},
        app=app,
    )
    rendered = ui.mining_operations_management_render_standalone_workbench(workbench["result"])
    return {
        "ok": bundle["contract"]["ok"]
        and plan["ok"]
        and fleet["ok"]
        and dispatch["ok"]
        and controls_view["ok"]
        and workbench["ok"]
        and rendered["ok"],
        "contract": bundle["contract"],
        "plan": plan,
        "fleet": fleet,
        "dispatch": dispatch,
        "controls": controls_view,
        "workbench": workbench,
        "rendered": rendered,
        "side_effects": (),
    }
