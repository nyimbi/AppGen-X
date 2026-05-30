"""Standalone one-PBC Waste and Recycling Operations app."""
from __future__ import annotations
from dataclasses import dataclass, field
from hashlib import sha256
from typing import Any
from .agent import chatbot_interface_contract, composed_agent_contribution, datastore_crud_plan, document_instruction_plan
from .controls import control_catalog, evaluate_control
from .forms import form_catalog
from .runtime import *
from .ui import waste_recycling_operations_render_workbench, waste_recycling_operations_ui_contract
from .wizards import wizard_catalog

PBC_KEY = "waste_recycling_operations"
def _digest(value: Any) -> str: return sha256(repr(value).encode("utf-8")).hexdigest()

@dataclass
class WasteRecyclingOperationsStandaloneApp:
    tenant: str = "tenant-waste-001"
    state: dict = field(default_factory=waste_recycling_operations_empty_state)
    routes: dict[str, dict] = field(default_factory=dict)
    bins: dict[str, dict] = field(default_factory=dict)
    pickups: dict[str, dict] = field(default_factory=dict)
    streams: dict[str, dict] = field(default_factory=dict)
    contamination: dict[str, dict] = field(default_factory=dict)
    tickets: dict[str, dict] = field(default_factory=dict)
    yields: dict[str, dict] = field(default_factory=dict)
    notices: list[dict] = field(default_factory=list)

    def configure(self, database_backend="postgresql"):
        cfg = waste_recycling_operations_configure_runtime(self.state, {"database_backend": database_backend, "event_topic": WASTE_RECYCLING_OPERATIONS_REQUIRED_EVENT_TOPIC})
        self.state = cfg["state"]
        for name, value in (("contamination_repeat_threshold", 2), ("route_recovery_sla_hours", 24), ("disposal_weight_variance_pct", 0.03), ("assistant_confirmation_required", True)):
            res = waste_recycling_operations_set_parameter(self.state, name, value); self.state = res["state"]
        for rule_id in ("route_has_crew_vehicle_and_facility_window", "pickup_has_proof_or_exception", "disposal_ticket_weights_reconcile", "agent_mutations_require_confirmation"):
            res = waste_recycling_operations_register_rule(self.state, {"rule_id": rule_id, "scope": "operations"}); self.state = res["state"]
        inbound = waste_recycling_operations_receive_event(self.state, {"event_type": WASTE_RECYCLING_OPERATIONS_CONSUMED_EVENT_TYPES[0], "idempotency_key": "waste-policy-001"}); self.state = inbound["state"]
        return {"ok": cfg["ok"] and inbound["ok"], "side_effects": ()}

    def release_route(self, route_id, service_date, stream, territory, stops, crew_projection=None, vehicle_projection=None, facility_window=None):
        facts = locals(); ctl = evaluate_control("route_has_crew_vehicle_and_facility_window", facts)
        row = {"id": route_id, "tenant": self.tenant, "service_date": service_date, "stream": stream, "territory": territory, "stops": tuple(stops or ()), "crew_projection": crew_projection, "vehicle_projection": vehicle_projection, "facility_window": facility_window, "status": "released" if ctl["ok"] else "blocked", "blockers": ctl["missing"]}
        self.routes[route_id] = row; return {"ok": ctl["ok"], "route": row, "side_effects": ()}

    def register_bin(self, bin_id, serial, rfid, stream, location, size="96g", condition="serviceable"):
        ctl = evaluate_control("bin_has_identity_and_location", locals())
        row = {"id": bin_id, "tenant": self.tenant, "serial": serial, "rfid": rfid, "stream": stream, "location": location, "size": size, "condition": condition, "status": "active" if ctl["ok"] else "blocked", "blockers": ctl["missing"]}
        self.bins[bin_id] = row; return {"ok": ctl["ok"], "bin": row, "side_effects": ()}

    def define_material_stream(self, stream_id, accepted_materials, prohibited_materials, contamination_threshold, destination_projection):
        ctl = evaluate_control("material_stream_has_rules", locals())
        row = {"id": stream_id, "tenant": self.tenant, "accepted_materials": tuple(accepted_materials or ()), "prohibited_materials": tuple(prohibited_materials or ()), "contamination_threshold": contamination_threshold, "destination_projection": destination_projection, "status": "active" if ctl["ok"] else "blocked", "blockers": ctl["missing"]}
        self.streams[stream_id] = row; return {"ok": ctl["ok"], "stream": row, "side_effects": ()}

    def record_pickup(self, pickup_id, route_id, bin_id, outcome, gps=None, weight_estimate=None, photo_digest=None, exception_code=None, lift_sensor_digest=None):
        ctl = evaluate_control("pickup_has_proof_or_exception", locals())
        row = {"id": pickup_id, "tenant": self.tenant, "route_id": route_id, "bin_id": bin_id, "outcome": outcome, "gps": gps, "weight_estimate": weight_estimate, "photo_digest": photo_digest, "exception_code": exception_code, "status": "proved" if ctl["ok"] else "needs_evidence", "blockers": ctl["missing"]}
        self.pickups[pickup_id] = row; return {"ok": route_id in self.routes and bin_id in self.bins and ctl["ok"], "pickup": row, "side_effects": ()}

    def classify_missed_pickup(self, case_id, pickup_id, report_source, reason, return_trip_eligible=False):
        row = {"id": case_id, "tenant": self.tenant, "pickup_id": pickup_id, "report_source": report_source, "reason": reason, "return_trip_eligible": return_trip_eligible, "status": "recovery_scheduled" if return_trip_eligible else "customer_notice"}
        self.notices.append(row); return {"ok": pickup_id in self.pickups and reason in ("operator_miss", "not_out", "blocked_access", "contamination"), "case": row, "side_effects": ()}

    def record_contamination(self, finding_id, bin_id, route_id, contaminant_type, severity, photo_digest, repeat_count=0, notice_required=True):
        ctl = evaluate_control("contamination_has_photo_and_notice", locals())
        escalation = repeat_count >= 2 or severity in ("high", "hazardous")
        row = {"id": finding_id, "tenant": self.tenant, "bin_id": bin_id, "route_id": route_id, "contaminant_type": contaminant_type, "severity": severity, "photo_digest": photo_digest, "notice_required": notice_required, "repeat_count": repeat_count, "escalation": escalation, "status": "education_notice" if ctl["ok"] else "blocked", "blockers": ctl["missing"]}
        self.contamination[finding_id] = row; return {"ok": bin_id in self.bins and route_id in self.routes and ctl["ok"], "finding": row, "side_effects": ()}

    def reconcile_disposal_ticket(self, ticket_id, route_id, facility_projection, gross_weight, tare_weight, net_weight, stream, ticket_image_digest=None):
        ctl = evaluate_control("disposal_ticket_weights_reconcile", locals())
        row = {"id": ticket_id, "tenant": self.tenant, "route_id": route_id, "facility_projection": facility_projection, "gross_weight": gross_weight, "tare_weight": tare_weight, "net_weight": net_weight, "stream": stream, "ticket_image_digest": ticket_image_digest, "status": "reconciled" if ctl["ok"] else "variance_hold", "blockers": ctl["missing"]}
        self.tickets[ticket_id] = row; return {"ok": route_id in self.routes and ctl["ok"], "ticket": row, "side_effects": ()}

    def calculate_recycling_yield(self, yield_id, facility_projection, stream, inbound_weight, reject_weight, recovered_weight, grade="mixed", period="current"):
        ctl = evaluate_control("yield_has_reject_and_recovered_weight", locals())
        diversion_rate = round(recovered_weight / inbound_weight, 4) if inbound_weight else 0
        reject_rate = round(reject_weight / inbound_weight, 4) if inbound_weight else 0
        row = {"id": yield_id, "tenant": self.tenant, "facility_projection": facility_projection, "stream": stream, "inbound_weight": inbound_weight, "reject_weight": reject_weight, "recovered_weight": recovered_weight, "grade": grade, "period": period, "diversion_rate": diversion_rate, "reject_rate": reject_rate, "status": "calculated" if ctl["ok"] else "blocked", "blockers": ctl["missing"]}
        self.yields[yield_id] = row; return {"ok": ctl["ok"] and recovered_weight + reject_weight <= inbound_weight, "yield": row, "side_effects": ()}

    def open_hazardous_exception(self, exception_id, route_id, bin_id, material_type, safety_instruction, route_hold=True, responder_required=True):
        ctl = evaluate_control("hazardous_exception_blocks_normal_pickup", locals())
        row = {"id": exception_id, "tenant": self.tenant, "route_id": route_id, "bin_id": bin_id, "material_type": material_type, "safety_instruction": safety_instruction, "route_hold": route_hold, "responder_required": responder_required, "status": "special_handoff_required" if ctl["ok"] else "blocked", "blockers": ctl["missing"]}
        self.contamination[exception_id] = row; return {"ok": route_id in self.routes and bin_id in self.bins and ctl["ok"], "exception": row, "side_effects": ()}

    def assistant_preview(self, document, instruction, confirmed=False):
        ctl = evaluate_control("agent_mutations_require_confirmation", {"confirmed": confirmed})
        doc = document_instruction_plan(document, instruction); crud = datastore_crud_plan("create", table="waste_recycling_operations_pickup_event", payload={"instruction": instruction})
        return {"ok": doc["ok"] and crud["ok"] and ctl["ok"], "document_plan": doc, "crud_preview": crud, "requires_confirmation": not confirmed, "side_effects": ()}

    def workbench_snapshot(self):
        return {"ok": True, "routes": tuple(self.routes.values()), "bins": tuple(self.bins.values()), "pickups": tuple(self.pickups.values()), "contamination": tuple(self.contamination.values()), "tickets": tuple(self.tickets.values()), "yields": tuple(self.yields.values()), "diversion_rate": self.yields[next(iter(self.yields))]["diversion_rate"] if self.yields else 0, "side_effects": ()}

    def app_contract(self):
        return {"format":"appgen.waste-recycling-operations.standalone-app.v1", "ok": True, "pbc": PBC_KEY, "database_backends": WASTE_RECYCLING_OPERATIONS_ALLOWED_DATABASE_BACKENDS, "event_contract": "AppGen-X", "stream_engine_picker_visible": False, "owned_tables": WASTE_RECYCLING_OPERATIONS_OWNED_TABLES, "schema": waste_recycling_operations_build_schema_contract(), "services": waste_recycling_operations_build_service_contract(), "routes": waste_recycling_operations_build_api_contract(), "permissions": waste_recycling_operations_permissions_contract(), "ui": waste_recycling_operations_ui_contract(), "workbench": waste_recycling_operations_render_workbench(), "forms": form_catalog(), "wizards": wizard_catalog(), "controls": control_catalog(), "agent": chatbot_interface_contract(), "composed_agent": composed_agent_contribution(), "dsl": {"pbc": PBC_KEY, "skills_namespace": f"{PBC_KEY}_skills", "single_pbc_app": True}, "side_effects": ()}

    def run_demo(self):
        checks = []
        checks.append(self.configure()["ok"])
        checks.append(self.release_route("R0", "2026-05-30", "recycling", "north", ("S1",))["ok"] is False)
        checks.append(self.release_route("R1", "2026-05-30", "recycling", "north", ("S1",), "crew-a", "truck-9", "06:00-14:00")["ok"])
        checks.append(self.register_bin("B1", "SER1", "RF1", "recycling", "12 River Rd")["ok"])
        checks.append(self.define_material_stream("MS1", ("paper", "cardboard"), ("battery", "food"), .08, "MRF-1")["ok"])
        checks.append(self.record_pickup("P0", "R1", "B1", "missed")["ok"] is False)
        checks.append(self.record_pickup("P1", "R1", "B1", "completed", gps="-1,36", weight_estimate=14, photo_digest="photo")["ok"])
        checks.append(self.classify_missed_pickup("MP1", "P1", "resident", "operator_miss", True)["ok"])
        checks.append(self.record_contamination("C1", "B1", "R1", "plastic_bag", "medium", "photo", 2)["ok"])
        checks.append(self.open_hazardous_exception("H1", "R1", "B1", "battery", "isolate bin")["ok"])
        checks.append(self.reconcile_disposal_ticket("T0", "R1", "MRF-1", 100, 20, 70, "recycling")["ok"] is False)
        checks.append(self.reconcile_disposal_ticket("T1", "R1", "MRF-1", 100, 20, 80, "recycling")["ok"])
        checks.append(self.calculate_recycling_yield("Y1", "MRF-1", "recycling", 80, 8, 64)["ok"])
        checks.append(self.assistant_preview("missed pickup memo", "create recovery task", False)["ok"] is False)
        checks.append(self.assistant_preview("missed pickup memo", "create recovery task", True)["ok"])
        return {"ok": all(checks), "contract": self.app_contract(), "workbench": self.workbench_snapshot(), "side_effects": ()}

def single_pbc_app_contract(): return WasteRecyclingOperationsStandaloneApp().app_contract()
def standalone_smoke_test():
    app = WasteRecyclingOperationsStandaloneApp(); demo = app.run_demo(); runtime = waste_recycling_operations_runtime_smoke(); contract = single_pbc_app_contract()
    return {"ok": demo["ok"] and runtime["ok"] and contract["ok"], "demo": demo, "runtime": runtime, "contract": contract, "side_effects": ()}
