"""Standalone one-PBC application surface for facility_energy_management."""
from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
from typing import Any

from .agent import chatbot_interface_contract, composed_agent_contribution, datastore_crud_plan, document_instruction_plan
from .controls import control_catalog, evaluate_control
from .forms import form_catalog
from .runtime import (
    FACILITY_ENERGY_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
    FACILITY_ENERGY_MANAGEMENT_CONSUMED_EVENT_TYPES,
    FACILITY_ENERGY_MANAGEMENT_EMITTED_EVENT_TYPES,
    FACILITY_ENERGY_MANAGEMENT_OWNED_TABLES,
    FACILITY_ENERGY_MANAGEMENT_REQUIRED_EVENT_TOPIC,
    facility_energy_management_build_api_contract,
    facility_energy_management_build_schema_contract,
    facility_energy_management_build_service_contract,
    facility_energy_management_configure_runtime,
    facility_energy_management_empty_state,
    facility_energy_management_permissions_contract,
    facility_energy_management_receive_event,
    facility_energy_management_register_rule,
    facility_energy_management_runtime_smoke,
    facility_energy_management_set_parameter,
)
from .ui import facility_energy_management_render_workbench, facility_energy_management_ui_contract
from .wizards import wizard_catalog

PBC_KEY = "facility_energy_management"


def _digest(value: Any) -> str:
    return sha256(repr(value).encode("utf-8")).hexdigest()


@dataclass
class FacilityEnergyManagementStandaloneApp:
    """Side-effect-free app shell proving this PBC can run by itself."""

    tenant: str = "tenant-fem-001"
    state: dict = field(default_factory=facility_energy_management_empty_state)
    meters: dict[str, dict] = field(default_factory=dict)
    load_profiles: dict[str, dict] = field(default_factory=dict)
    tariffs: dict[str, dict] = field(default_factory=dict)
    schedules: dict[str, dict] = field(default_factory=dict)
    baselines: dict[str, dict] = field(default_factory=dict)
    demand_events: dict[str, dict] = field(default_factory=dict)
    optimizations: dict[str, dict] = field(default_factory=dict)
    investigations: dict[str, dict] = field(default_factory=dict)

    def configure(self, database_backend: str = "postgresql") -> dict:
        configured = facility_energy_management_configure_runtime(
            self.state,
            {"database_backend": database_backend, "event_topic": FACILITY_ENERGY_MANAGEMENT_REQUIRED_EVENT_TOPIC},
        )
        self.state = configured["state"]
        for name, value in (
            ("residual_tolerance_percent", 3.0),
            ("peak_alert_kw", 750),
            ("minimum_notice_minutes", 30),
            ("comfort_band_f", (68, 76)),
            ("rebound_limit_kw", 120),
        ):
            param = facility_energy_management_set_parameter(self.state, name, value)
            self.state = param["state"]
        for rule in (
            {"rule_id": "critical_loads_excluded", "scope": "demand_response", "effect": "block_unsafe_shed"},
            {"rule_id": "baseline_windows_do_not_overlap", "scope": "baseline", "effect": "block_approval"},
            {"rule_id": "manual_overrides_expire", "scope": "schedule", "effect": "auto_revert"},
        ):
            registered = facility_energy_management_register_rule(self.state, rule)
            self.state = registered["state"]
        received = facility_energy_management_receive_event(
            self.state,
            {
                "event_type": FACILITY_ENERGY_MANAGEMENT_CONSUMED_EVENT_TYPES[0],
                "idempotency_key": "policy-energy-001",
                "payload": {"policy": "summer_peak_program"},
            },
        )
        self.state = received["state"]
        return {"ok": configured["ok"] and received["ok"], "configuration": configured["configuration"], "side_effects": ()}

    def commission_meter(self, meter_id: str, parent_meter_id: str | None = None, **payload: Any) -> dict:
        record = {
            "id": meter_id,
            "tenant": self.tenant,
            "parent_meter_id": parent_meter_id,
            "meter_role": payload.get("meter_role", "submeter" if parent_meter_id else "utility_main"),
            "service_account": payload.get("service_account", "UTIL-ACCT-001"),
            "premise_id": payload.get("premise_id", "CAMPUS-01"),
            "tariff_eligibility": tuple(payload.get("tariff_eligibility", ("tou", "demand_response"))),
            "heartbeat_minutes": payload.get("heartbeat_minutes", 15),
            "health_status": payload.get("health_status", "healthy"),
            "criticality": payload.get("criticality", "normal"),
            "calibration_evidence_uri": payload.get("calibration_evidence_uri", "evidence://calibration/current"),
        }
        record["rollup_key"] = _digest((meter_id, parent_meter_id, record["service_account"]))
        self.meters[meter_id] = record
        return {"ok": True, "meter": record, "owned_table": f"{PBC_KEY}_energy_meter", "side_effects": ()}

    def record_interval_profile(self, profile_id: str, meter_id: str, intervals: tuple[dict, ...], **payload: Any) -> dict:
        missing = tuple(item for item in intervals if item.get("quality") == "missing")
        estimated = tuple(item for item in intervals if item.get("quality") == "estimated")
        profile = {
            "id": profile_id,
            "tenant": self.tenant,
            "meter_id": meter_id,
            "timezone": payload.get("timezone", "America/New_York"),
            "interval_minutes": payload.get("interval_minutes", 15),
            "channel": payload.get("channel", "kWh"),
            "intervals": intervals,
            "missing_count": len(missing),
            "estimated_count": len(estimated),
            "provenance_code": payload.get("provenance_code", "bms_interval_import"),
            "dst_handling": payload.get("dst_handling", "timezone_aware_wall_clock"),
        }
        self.load_profiles[profile_id] = profile
        return {"ok": meter_id in self.meters and profile["interval_minutes"] in (5, 10, 15, 30, 60), "profile": profile, "side_effects": ()}

    def create_tariff_signal(self, tariff_id: str, **payload: Any) -> dict:
        tariff = {
            "id": tariff_id,
            "season_calendar": payload.get("season_calendar", {"summer": ("Jun", "Sep"), "winter": ("Oct", "May")}),
            "time_bands": tuple(payload.get("time_bands", ("off_peak", "shoulder", "on_peak"))),
            "holiday_overrides": tuple(payload.get("holiday_overrides", ("federal",))),
            "ratchet_percent": payload.get("ratchet_percent", 80),
            "contract_demand_kw": payload.get("contract_demand_kw", 900),
            "coincident_peak_window": payload.get("coincident_peak_window", "weekday 14:00-18:00"),
        }
        self.tariffs[tariff_id] = tariff
        return {"ok": True, "tariff": tariff, "side_effects": ()}

    def define_equipment_schedule(self, schedule_id: str, equipment_group: str, **payload: Any) -> dict:
        schedule = {
            "id": schedule_id,
            "equipment_group": equipment_group,
            "hierarchy_level": payload.get("hierarchy_level", "building"),
            "parent_schedule_id": payload.get("parent_schedule_id"),
            "occupied_hours": payload.get("occupied_hours", ("Mon-Fri 07:00-19:00",)),
            "holiday_calendar": payload.get("holiday_calendar", "federal"),
            "weather_thresholds": payload.get("weather_thresholds", {"pre_cool_f": 88, "pre_heat_f": 32}),
            "lock_windows": tuple(payload.get("lock_windows", ("maintenance Sun 01:00-04:00",))),
            "critical_zone": payload.get("critical_zone", False),
        }
        self.schedules[schedule_id] = schedule
        return {"ok": True, "schedule": schedule, "side_effects": ()}

    def approve_baseline(self, baseline_id: str, scope: str, **payload: Any) -> dict:
        overlap = any(item["scope"] == scope and item["status"] == "active" for item in self.baselines.values())
        baseline = {
            "id": baseline_id,
            "scope": scope,
            "version": payload.get("version", 1),
            "method": payload.get("method", "weather_normalized_degree_day"),
            "weather_source": payload.get("weather_source", "NOAA"),
            "effective_window": payload.get("effective_window", ("2026-01-01", "2026-12-31")),
            "reviewer": payload.get("reviewer", "energy_controller"),
            "status": "blocked" if overlap else "active",
            "overlap_detected": overlap,
        }
        self.baselines[baseline_id] = baseline
        return {"ok": not overlap, "baseline": baseline, "side_effects": ()}

    def open_demand_response_event(self, event_id: str, baseline_id: str, eligible_assets: tuple[str, ...], **payload: Any) -> dict:
        protected = tuple(asset for asset in eligible_assets if self.meters.get(asset, {}).get("criticality") in ("life_safety", "critical"))
        event = {
            "id": event_id,
            "baseline_id": baseline_id,
            "eligible_assets": tuple(asset for asset in eligible_assets if asset not in protected),
            "protected_assets": protected,
            "shed_capacity_kw": payload.get("shed_capacity_kw", 180),
            "state": "planned",
            "timeline": ("planned",),
            "rebound_plan": payload.get("rebound_plan", "stage fans then chillers over 45 minutes"),
        }
        self.demand_events[event_id] = event
        return {"ok": baseline_id in self.baselines and not protected, "event": event, "side_effects": ()}

    def dispatch_demand_response(self, event_id: str) -> dict:
        event = dict(self.demand_events[event_id])
        event["state"] = "settled"
        event["timeline"] = ("planned", "notified", "acknowledged", "active", "completed", "settled")
        event["settlement"] = {"baseline_id": event["baseline_id"], "measured_reduction_kw": min(event["shed_capacity_kw"], 165), "rebound_peak_limited": True}
        self.demand_events[event_id] = event
        return {"ok": True, "event": event, "side_effects": ()}

    def run_optimization(self, optimization_id: str, profile_id: str, tariff_id: str, schedule_id: str) -> dict:
        guardrail = evaluate_control("comfort_safety_guardrail")
        optimization = {
            "id": optimization_id,
            "profile_id": profile_id,
            "tariff_id": tariff_id,
            "schedule_id": schedule_id,
            "command_boundary": "approval_gated_handoff",
            "recommendations": (
                {"type": "setpoint", "change": "+2F during on_peak", "requires_approval": True},
                {"type": "schedule", "change": "pre-cool before coincident peak window", "requires_approval": True},
                {"type": "load_shed", "change": "shed noncritical plug load", "requires_approval": True},
            ),
            "guardrail_ok": guardrail["ok"],
        }
        self.optimizations[optimization_id] = optimization
        return {"ok": all(key in collection for key, collection in ((profile_id, self.load_profiles), (tariff_id, self.tariffs), (schedule_id, self.schedules))) and guardrail["ok"], "optimization": optimization, "side_effects": ()}

    def open_investigation_case_pack(self, case_id: str, profile_id: str, schedule_id: str, tariff_id: str) -> dict:
        case = {
            "id": case_id,
            "profile_id": profile_id,
            "schedule_id": schedule_id,
            "tariff_id": tariff_id,
            "suspected_causes": ("after_hours_runtime", "baseload_creep", "stuck_setpoint"),
            "links": {"meter_context": profile_id, "schedule_state": schedule_id, "tariff_band": tariff_id},
            "next_action": "review tenant exception and fan schedule override",
        }
        self.investigations[case_id] = case
        return {"ok": True, "case_pack": case, "side_effects": ()}

    def assistant_preview(self, document: str, instruction: str) -> dict:
        plan = document_instruction_plan(document, instruction)
        crud = datastore_crud_plan("create", table=f"{PBC_KEY}_energy_optimization", payload={"instruction": instruction})
        return {"ok": plan["ok"] and crud["ok"], "document_plan": plan, "crud_preview": crud, "requires_confirmation": True, "side_effects": ()}

    def app_contract(self) -> dict:
        return {
            "format": "appgen.facility-energy-management.standalone-app.v1",
            "ok": True,
            "pbc": PBC_KEY,
            "owned_tables": FACILITY_ENERGY_MANAGEMENT_OWNED_TABLES,
            "database_backends": FACILITY_ENERGY_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
            "schema": facility_energy_management_build_schema_contract(),
            "services": facility_energy_management_build_service_contract(),
            "routes": facility_energy_management_build_api_contract(),
            "permissions": facility_energy_management_permissions_contract(),
            "ui": facility_energy_management_ui_contract(),
            "workbench": facility_energy_management_render_workbench(),
            "forms": form_catalog(),
            "wizards": wizard_catalog(),
            "controls": control_catalog(),
            "agent": chatbot_interface_contract(),
            "composed_agent": composed_agent_contribution(),
            "dsl": {"pbc": PBC_KEY, "skills_namespace": f"{PBC_KEY}_skills", "single_pbc_app": True},
            "side_effects": (),
        }

    def run_demo(self) -> dict:
        configured = self.configure()
        main = self.commission_meter("MTR-MAIN", meter_role="utility_main")
        floor = self.commission_meter("MTR-FLR-01", parent_meter_id="MTR-MAIN", meter_role="floor_submeter")
        tenant = self.commission_meter("MTR-TENANT-01", parent_meter_id="MTR-FLR-01", meter_role="tenant_submeter")
        critical = self.commission_meter("MTR-LIFE-01", parent_meter_id="MTR-MAIN", criticality="life_safety")
        intervals = tuple({"at": f"2026-07-01T{hour:02d}:00:00", "kwh": 40 + hour, "kw": 120 + hour * 4, "quality": "observed"} for hour in range(8, 12))
        profile = self.record_interval_profile("LP-001", "MTR-MAIN", intervals)
        tariff = self.create_tariff_signal("TARIFF-TOU-2026")
        schedule = self.define_equipment_schedule("SCH-HVAC-01", "AHU-1")
        baseline = self.approve_baseline("BASE-2026", "campus-01")
        blocked_dr = self.open_demand_response_event("DR-BLOCKED", "BASE-2026", ("MTR-LIFE-01",))
        demand = self.open_demand_response_event("DR-001", "BASE-2026", ("MTR-FLR-01", "MTR-TENANT-01"))
        dispatched = self.dispatch_demand_response("DR-001")
        optimization = self.run_optimization("OPT-001", "LP-001", "TARIFF-TOU-2026", "SCH-HVAC-01")
        case = self.open_investigation_case_pack("CASE-001", "LP-001", "SCH-HVAC-01", "TARIFF-TOU-2026")
        assistant = self.assistant_preview("tenant complaint and utility peak memo", "create optimization plan and demand response case")
        checks = (
            configured["ok"], main["ok"], floor["ok"], tenant["ok"], critical["ok"], profile["ok"], tariff["ok"],
            schedule["ok"], baseline["ok"], blocked_dr["ok"] is False, demand["ok"], dispatched["ok"], optimization["ok"], case["ok"], assistant["ok"],
        )
        return {"ok": all(checks), "blocked_critical_load_dispatch": blocked_dr, "dispatch": dispatched, "optimization": optimization, "case_pack": case, "assistant": assistant, "app_contract": self.app_contract(), "side_effects": ()}


def single_pbc_app_contract() -> dict:
    return FacilityEnergyManagementStandaloneApp().app_contract()


def standalone_smoke_test() -> dict:
    app = FacilityEnergyManagementStandaloneApp()
    demo = app.run_demo()
    runtime = facility_energy_management_runtime_smoke()
    contract = single_pbc_app_contract()
    event_ok = set(FACILITY_ENERGY_MANAGEMENT_EMITTED_EVENT_TYPES) and contract["event_contract"] == "AppGen-X"
    return {
        "ok": demo["ok"] and runtime["ok"] and contract["ok"] and event_ok and contract["stream_engine_picker_visible"] is False,
        "demo": demo,
        "runtime": runtime,
        "contract": contract,
        "side_effects": (),
    }
