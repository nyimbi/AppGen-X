"""Standalone one-PBC application surface for fleet_mobility_operations."""
from __future__ import annotations
from dataclasses import dataclass, field
from hashlib import sha256
from typing import Any
from .agent import chatbot_interface_contract, composed_agent_contribution, datastore_crud_plan, document_instruction_plan
from .controls import control_catalog, evaluate_control
from .forms import form_catalog
from .runtime import (
    FLEET_MOBILITY_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
    FLEET_MOBILITY_OPERATIONS_CONSUMED_EVENT_TYPES,
    FLEET_MOBILITY_OPERATIONS_EMITTED_EVENT_TYPES,
    FLEET_MOBILITY_OPERATIONS_OWNED_TABLES,
    FLEET_MOBILITY_OPERATIONS_REQUIRED_EVENT_TOPIC,
    fleet_mobility_operations_build_api_contract,
    fleet_mobility_operations_build_schema_contract,
    fleet_mobility_operations_build_service_contract,
    fleet_mobility_operations_configure_runtime,
    fleet_mobility_operations_empty_state,
    fleet_mobility_operations_permissions_contract,
    fleet_mobility_operations_receive_event,
    fleet_mobility_operations_register_rule,
    fleet_mobility_operations_runtime_smoke,
    fleet_mobility_operations_set_parameter,
)
from .ui import fleet_mobility_operations_render_workbench, fleet_mobility_operations_ui_contract
from .wizards import wizard_catalog
PBC_KEY = "fleet_mobility_operations"

def _digest(value: Any) -> str:
    return sha256(repr(value).encode("utf-8")).hexdigest()

@dataclass
class FleetMobilityOperationsStandaloneApp:
    tenant: str = "tenant-fleet-001"
    state: dict = field(default_factory=fleet_mobility_operations_empty_state)
    vehicles: dict[str, dict] = field(default_factory=dict)
    drivers: dict[str, dict] = field(default_factory=dict)
    assignments: dict[str, dict] = field(default_factory=dict)
    telematics: list[dict] = field(default_factory=list)
    routes: dict[str, dict] = field(default_factory=dict)
    maintenance: dict[str, dict] = field(default_factory=dict)
    incidents: dict[str, dict] = field(default_factory=dict)
    fuel: dict[str, dict] = field(default_factory=dict)

    def configure(self, database_backend: str = "postgresql") -> dict:
        configured = fleet_mobility_operations_configure_runtime(self.state, {"database_backend": database_backend, "event_topic": FLEET_MOBILITY_OPERATIONS_REQUIRED_EVENT_TOPIC})
        self.state = configured["state"]
        for name, value in (("minimum_rest_hours", 10), ("telematics_fresh_minutes", 20), ("ev_min_soc_percent", 35), ("assignment_sla_minutes", 15), ("fuel_variance_percent", 12)):
            param = fleet_mobility_operations_set_parameter(self.state, name, value); self.state = param["state"]
        for rule in (
            {"rule_id": "driver_rest_required", "scope": "assignment", "effect": "block_overlap"},
            {"rule_id": "vehicle_readiness_required", "scope": "dispatch", "effect": "block_unready_vehicle"},
            {"rule_id": "device_messages_quarantined", "scope": "telematics", "effect": "dead_letter_bad_payload"},
        ):
            registered = fleet_mobility_operations_register_rule(self.state, rule); self.state = registered["state"]
        received = fleet_mobility_operations_receive_event(self.state, {"event_type": FLEET_MOBILITY_OPERATIONS_CONSUMED_EVENT_TYPES[0], "idempotency_key": "fleet-policy-001"})
        self.state = received["state"]
        return {"ok": configured["ok"] and received["ok"], "side_effects": ()}

    def register_vehicle(self, vehicle_id: str, **payload: Any) -> dict:
        vehicle = {"id": vehicle_id, "tenant": self.tenant, "depot": payload.get("depot", "DEPOT-A"), "vehicle_class": payload.get("vehicle_class", "van"), "registration_status": payload.get("registration_status", "current"), "fuel_or_soc": payload.get("fuel_or_soc", 80), "telematics_fresh": payload.get("telematics_fresh", True), "open_maintenance": payload.get("open_maintenance", False), "open_safety_event": payload.get("open_safety_event", False), "ev": payload.get("ev", False)}
        vehicle["readiness"] = self._readiness(vehicle)["verdict"]
        self.vehicles[vehicle_id] = vehicle
        return {"ok": True, "vehicle": vehicle, "side_effects": ()}

    def register_driver(self, driver_id: str, **payload: Any) -> dict:
        driver = {"id": driver_id, "license_class": payload.get("license_class", "commercial"), "medical_current": payload.get("medical_current", True), "training_current": payload.get("training_current", True), "last_shift_end_hour": payload.get("last_shift_end_hour", 0)}
        self.drivers[driver_id] = driver
        return {"ok": True, "driver": driver, "side_effects": ()}

    def _readiness(self, vehicle: dict) -> dict:
        blockers = []
        if vehicle.get("registration_status") != "current": blockers.append("registration")
        if vehicle.get("fuel_or_soc", 0) < 25: blockers.append("energy")
        if vehicle.get("telematics_fresh") is not True: blockers.append("telematics")
        if vehicle.get("open_maintenance"): blockers.append("maintenance")
        if vehicle.get("open_safety_event"): blockers.append("safety")
        return {"verdict": "ready" if not blockers else "blocked", "blockers": tuple(blockers)}

    def validate_assignment(self, assignment_id: str, driver_id: str, vehicle_id: str, route_id: str, shift_start_hour: int, shift_end_hour: int) -> dict:
        driver = self.drivers[driver_id]; vehicle = self.vehicles[vehicle_id]; readiness = self._readiness(vehicle)
        overlap = any(a["driver_id"] == driver_id and not (shift_end_hour <= a["shift_start_hour"] or shift_start_hour >= a["shift_end_hour"]) for a in self.assignments.values())
        rest_ok = shift_start_hour - driver.get("last_shift_end_hour", 0) >= 10
        credential_ok = driver.get("medical_current") and driver.get("training_current")
        blockers = tuple(reason for reason, failed in (("overlap", overlap), ("rest_window", not rest_ok), ("credential", not credential_ok), ("vehicle_readiness", readiness["verdict"] != "ready")) if failed)
        assignment = {"id": assignment_id, "driver_id": driver_id, "vehicle_id": vehicle_id, "route_id": route_id, "shift_start_hour": shift_start_hour, "shift_end_hour": shift_end_hour, "status": "approved" if not blockers else "blocked", "blockers": blockers}
        self.assignments[assignment_id] = assignment
        return {"ok": not blockers, "assignment": assignment, "side_effects": ()}

    def ingest_telematics(self, event: dict) -> dict:
        known = event.get("vehicle_id") in self.vehicles
        sane = event.get("event_time", 0) <= event.get("received_at", 0) + 5 and event.get("event_time", 0) >= event.get("received_at", 0) - 86400
        idem = event.get("idempotency_key") or _digest(event)
        duplicate = any(item.get("idempotency_key") == idem for item in self.telematics)
        accepted = known and sane and not duplicate
        record = {**event, "idempotency_key": idem, "state": "accepted" if accepted else "quarantined", "reason": None if accepted else "unknown_device_or_timestamp_or_duplicate"}
        self.telematics.append(record)
        return {"ok": accepted, "telematics_event": record, "side_effects": ()}

    def plan_route(self, route_id: str, vehicle_id: str, driver_id: str, stops: tuple[dict, ...]) -> dict:
        route = {"id": route_id, "vehicle_id": vehicle_id, "driver_id": driver_id, "stops": stops, "eta_projection": tuple({**stop, "risk": "on_time"} for stop in stops), "completion_confidence": 0.92}
        self.routes[route_id] = route
        return {"ok": vehicle_id in self.vehicles and driver_id in self.drivers, "route": route, "side_effects": ()}

    def reproject_route(self, route_id: str, delay_minutes: int) -> dict:
        route = dict(self.routes[route_id])
        route["eta_projection"] = tuple({**stop, "delay_minutes": delay_minutes, "risk": "late" if delay_minutes > 15 else "watch"} for stop in route["stops"])
        route["completion_confidence"] = max(0.1, route["completion_confidence"] - delay_minutes / 100)
        self.routes[route_id] = route
        return {"ok": True, "route": route, "emitted_event": "FleetRouteReprojected", "side_effects": ()}

    def create_maintenance_horizon(self, vehicle_id: str, due_in_days: int, **payload: Any) -> dict:
        horizon = {"vehicle_id": vehicle_id, "due_in_days": due_in_days, "odometer_due": payload.get("odometer_due", 120000), "parts_ready": payload.get("parts_ready", True), "bay_capacity": payload.get("bay_capacity", True), "dispatch_hold": due_in_days <= 7 or not payload.get("parts_ready", True)}
        self.maintenance[vehicle_id] = horizon
        if horizon["dispatch_hold"]:
            self.vehicles[vehicle_id]["open_maintenance"] = True; self.vehicles[vehicle_id]["readiness"] = self._readiness(self.vehicles[vehicle_id])["verdict"]
        return {"ok": True, "maintenance_horizon": horizon, "side_effects": ()}

    def reconcile_fuel(self, transaction_id: str, vehicle_id: str, amount: float, odometer_delta: float, geofence_ok: bool = True) -> dict:
        abnormal = amount > max(1, odometer_delta) * 0.25 or not geofence_ok
        record = {"id": transaction_id, "vehicle_id": vehicle_id, "amount": amount, "odometer_delta": odometer_delta, "geofence_ok": geofence_ok, "status": "exception" if abnormal else "matched"}
        self.fuel[transaction_id] = record
        return {"ok": not abnormal, "fuel_transaction": record, "side_effects": ()}

    def open_incident(self, incident_id: str, vehicle_id: str, driver_id: str, severity: str = "roadside_breakdown") -> dict:
        incident = {"id": incident_id, "vehicle_id": vehicle_id, "driver_id": driver_id, "severity": severity, "timeline": ("opened", "contained", "replacement_dispatched"), "state": "contained"}
        self.incidents[incident_id] = incident
        self.vehicles[vehicle_id]["open_safety_event"] = True; self.vehicles[vehicle_id]["readiness"] = self._readiness(self.vehicles[vehicle_id])["verdict"]
        return {"ok": True, "incident": incident, "side_effects": ()}

    def assistant_replan_preview(self, document: str, instruction: str) -> dict:
        plan = document_instruction_plan(document, instruction)
        crud = datastore_crud_plan("update", table=f"{PBC_KEY}_route_plan", payload={"instruction": instruction})
        return {"ok": plan["ok"] and crud["ok"], "document_plan": plan, "crud_preview": crud, "requires_confirmation": True, "side_effects": ()}

    def app_contract(self) -> dict:
        return {"format": "appgen.fleet-mobility-operations.standalone-app.v1", "ok": True, "pbc": PBC_KEY, "owned_tables": FLEET_MOBILITY_OPERATIONS_OWNED_TABLES, "database_backends": FLEET_MOBILITY_OPERATIONS_ALLOWED_DATABASE_BACKENDS, "event_contract": "AppGen-X", "stream_engine_picker_visible": False, "schema": fleet_mobility_operations_build_schema_contract(), "services": fleet_mobility_operations_build_service_contract(), "routes": fleet_mobility_operations_build_api_contract(), "permissions": fleet_mobility_operations_permissions_contract(), "ui": fleet_mobility_operations_ui_contract(), "workbench": fleet_mobility_operations_render_workbench(), "forms": form_catalog(), "wizards": wizard_catalog(), "controls": control_catalog(), "agent": chatbot_interface_contract(), "composed_agent": composed_agent_contribution(), "dsl": {"pbc": PBC_KEY, "skills_namespace": f"{PBC_KEY}_skills", "single_pbc_app": True}, "side_effects": ()}

    def run_demo(self) -> dict:
        cfg = self.configure(); ready = self.register_vehicle("VEH-READY", fuel_or_soc=78); ev = self.register_vehicle("VEH-EV", ev=True, fuel_or_soc=18); driver = self.register_driver("DRV-001", last_shift_end_hour=1)
        route = self.plan_route("ROUTE-001", "VEH-READY", "DRV-001", ({"stop": "A", "eta": "09:00"}, {"stop": "B", "eta": "10:00"}))
        assignment = self.validate_assignment("ASN-001", "DRV-001", "VEH-READY", "ROUTE-001", 12, 20)
        blocked_assignment = self.validate_assignment("ASN-EV", "DRV-001", "VEH-EV", "ROUTE-002", 21, 23)
        telemetry = self.ingest_telematics({"vehicle_id": "VEH-READY", "event_time": 100, "received_at": 101, "latitude": 1.0, "longitude": 2.0, "idempotency_key": "TEL-001"})
        duplicate = self.ingest_telematics({"vehicle_id": "VEH-READY", "event_time": 100, "received_at": 101, "idempotency_key": "TEL-001"})
        reprojection = self.reproject_route("ROUTE-001", 22)
        maintenance = self.create_maintenance_horizon("VEH-READY", 5)
        fuel = self.reconcile_fuel("FUEL-001", "VEH-READY", 15, 120)
        incident = self.open_incident("INC-001", "VEH-READY", "DRV-001")
        assistant = self.assistant_replan_preview("breakdown and route slippage note", "propose replacement route and driver")
        checks = (cfg["ok"], ready["ok"], ev["ok"], driver["ok"], route["ok"], assignment["ok"], blocked_assignment["ok"] is False, telemetry["ok"], duplicate["ok"] is False, reprojection["ok"], maintenance["ok"], fuel["ok"], incident["ok"], assistant["ok"])
        return {"ok": all(checks), "blocked_assignment": blocked_assignment, "duplicate_telematics": duplicate, "reprojection": reprojection, "incident": incident, "assistant": assistant, "app_contract": self.app_contract(), "side_effects": ()}

def single_pbc_app_contract() -> dict:
    return FleetMobilityOperationsStandaloneApp().app_contract()
def standalone_smoke_test() -> dict:
    app = FleetMobilityOperationsStandaloneApp(); demo = app.run_demo(); runtime = fleet_mobility_operations_runtime_smoke(); contract = single_pbc_app_contract()
    return {"ok": demo["ok"] and runtime["ok"] and contract["ok"] and bool(FLEET_MOBILITY_OPERATIONS_EMITTED_EVENT_TYPES) and contract["stream_engine_picker_visible"] is False, "demo": demo, "runtime": runtime, "contract": contract, "side_effects": ()}
