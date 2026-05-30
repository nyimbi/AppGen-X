"""Standalone one-PBC Travel Management app."""
from __future__ import annotations
from dataclasses import dataclass, field
from .agent import chatbot_interface_contract, composed_agent_contribution, datastore_crud_plan, document_instruction_plan
from .controls import control_catalog, evaluate_control
from .forms import form_catalog
from .runtime import *
from .ui import travel_management_render_workbench, travel_management_ui_contract
from .wizards import wizard_catalog

PBC_KEY = "travel_management"

@dataclass
class TravelManagementStandaloneApp:
    tenant: str = "tenant-travel-001"
    state: dict = field(default_factory=travel_management_empty_state)
    profiles: dict = field(default_factory=dict)
    policies: dict = field(default_factory=dict)
    trips: dict = field(default_factory=dict)
    approvals: dict = field(default_factory=dict)
    intents: dict = field(default_factory=dict)
    bookings: dict = field(default_factory=dict)
    itinerary: dict = field(default_factory=dict)
    duty_alerts: dict = field(default_factory=dict)
    disruptions: dict = field(default_factory=dict)
    unused_tickets: dict = field(default_factory=dict)
    expense_links: dict = field(default_factory=dict)
    carbon_records: dict = field(default_factory=dict)

    def configure(self, database_backend="postgresql"):
        cfg = travel_management_configure_runtime(self.state, {"database_backend": database_backend, "event_topic": TRAVEL_MANAGEMENT_REQUIRED_EVENT_TOPIC}); self.state = cfg["state"]
        for name, value in (("advance_booking_days", 14), ("hotel_rate_limit", 250), ("risk_alert_threshold", "high"), ("unused_ticket_warning_days", 30), ("approval_amount_limit", 5000)):
            res = travel_management_set_parameter(self.state, name, value); self.state = res["state"]
        inbound = travel_management_receive_event(self.state, {"event_type": TRAVEL_MANAGEMENT_CONSUMED_EVENT_TYPES[0], "idempotency_key": "employee-projection-001"}); self.state = inbound["state"]
        return {"ok": cfg["ok"] and inbound["ok"], "side_effects": ()}

    def upsert_traveler_profile(self, traveler_ref, contact_methods, emergency_contact, documents, preferences=(), accessibility_needs=(), notification_consent=True):
        facts = locals(); ctl = evaluate_control("traveler_profile_complete", facts)
        row = {"traveler_ref": traveler_ref, "tenant": self.tenant, "contact_methods": tuple(contact_methods or ()), "emergency_contact": emergency_contact, "documents": tuple(documents or ()), "preferences": tuple(preferences or ()), "accessibility_needs": tuple(accessibility_needs or ()), "notification_consent": notification_consent, "completeness": "complete" if ctl["ok"] else "incomplete", "blockers": ctl["missing"]}
        self.profiles[traveler_ref] = row; return {"ok": ctl["ok"], "profile": row, "side_effects": ()}

    def define_policy(self, policy_id, effective_from, employee_group, region, fare_class, hotel_cap, advance_booking_days=14, risk_rules=()):
        facts = locals(); ctl = evaluate_control("policy_version_applicable", facts)
        row = {"policy_id": policy_id, "tenant": self.tenant, "effective_from": effective_from, "employee_group": employee_group, "region": region, "fare_class": fare_class, "hotel_cap": hotel_cap, "advance_booking_days": advance_booking_days, "risk_rules": tuple(risk_rules or ()), "state": "active" if ctl["ok"] else "blocked", "blockers": ctl["missing"]}
        self.policies[policy_id] = row; return {"ok": ctl["ok"], "policy": row, "side_effects": ()}

    def request_trip(self, trip_id, traveler_ref, purpose, destinations, start_date, end_date, budget, risk_level, policy_version, visa_required=False, document_ready=True):
        facts = locals(); ready = evaluate_control("trip_request_ready", facts)
        risk = evaluate_control("high_risk_destination_requires_mitigation", {"risk_level": risk_level, "mitigation_plan": None, "risk_approver": None})
        ok = traveler_ref in self.profiles and policy_version in self.policies and ready["ok"] and (risk_level not in ("high", "critical") or document_ready)
        blockers = ready["missing"] + (() if ok else ("profile_policy_or_risk_evidence",))
        row = {"trip_id": trip_id, "tenant": self.tenant, "traveler_ref": traveler_ref, "purpose": purpose, "destinations": tuple(destinations or ()), "start_date": start_date, "end_date": end_date, "budget": budget, "risk_level": risk_level, "policy_version": policy_version, "visa_required": visa_required, "document_ready": document_ready, "state": "submitted" if ok else "blocked", "risk_control": risk, "blockers": blockers}
        self.trips[trip_id] = row; return {"ok": ok, "trip": row, "side_effects": ()}

    def route_approval(self, trip_id, approvers, rationale, emergency_lane=False, delegations=()):
        facts = locals(); ctl = evaluate_control("approval_graph_complete", facts)
        row = {"trip_id": trip_id, "tenant": self.tenant, "approvers": tuple(approvers or ()), "delegations": tuple(delegations or ()), "rationale": rationale, "emergency_lane": emergency_lane, "state": "approved" if ctl["ok"] else "blocked", "blockers": ctl["missing"]}
        self.approvals[trip_id] = row
        if ctl["ok"] and trip_id in self.trips: self.trips[trip_id]["state"] = "approved"
        return {"ok": trip_id in self.trips and ctl["ok"], "approval": row, "side_effects": ()}

    def create_booking_intent(self, intent_id, trip_id, constraints, booking_deadline, preferred_suppliers=(), option_set=()):
        ctl = evaluate_control("booking_intent_approved_trip", locals())
        approved = self.trips.get(trip_id, {}).get("state") == "approved"
        row = {"intent_id": intent_id, "tenant": self.tenant, "trip_id": trip_id, "constraints": dict(constraints or {}), "preferred_suppliers": tuple(preferred_suppliers or ()), "booking_deadline": booking_deadline, "option_set": tuple(option_set or ()), "state": "compared" if approved and ctl["ok"] else "blocked", "blockers": ctl["missing"] + (() if approved else ("approved_trip",))}
        self.intents[intent_id] = row; return {"ok": approved and ctl["ok"], "intent": row, "side_effects": ()}

    def record_air_booking(self, booking_id, trip_id, fare_class, route, ticket_deadline, refundability, ticket_number=None):
        ctl = evaluate_control("air_booking_policy_ready", locals())
        row = {"booking_id": booking_id, "kind": "air", "tenant": self.tenant, "trip_id": trip_id, "fare_class": fare_class, "route": tuple(route or ()), "ticket_deadline": ticket_deadline, "refundability": refundability, "ticket_number": ticket_number, "state": "booked" if ctl["ok"] else "blocked", "blockers": ctl["missing"]}
        self.bookings[booking_id] = row; return {"ok": trip_id in self.trips and ctl["ok"], "booking": row, "side_effects": ()}

    def record_hotel_booking(self, booking_id, trip_id, property_name, nightly_rate, location_safety, cancellation_window, accessibility=()):
        ctl = evaluate_control("hotel_booking_policy_ready", {"nightly_rate": nightly_rate, "location_safety": location_safety, "cancellation_window": cancellation_window})
        cap = next(iter(self.policies.values()), {}).get("hotel_cap", nightly_rate)
        ok = trip_id in self.trips and ctl["ok"] and nightly_rate <= cap
        row = {"booking_id": booking_id, "kind": "hotel", "tenant": self.tenant, "trip_id": trip_id, "property": property_name, "nightly_rate": nightly_rate, "location_safety": location_safety, "cancellation_window": cancellation_window, "accessibility": tuple(accessibility or ()), "state": "booked" if ok else "exception_required", "blockers": ctl["missing"] + (() if nightly_rate <= cap else ("hotel_rate_cap",))}
        self.bookings[booking_id] = row; return {"ok": ok, "booking": row, "side_effects": ()}

    def ingest_itinerary(self, item_id, trip_id, kind, local_start, local_end, timezone, confirmation, source_evidence, confirmed=False):
        ctl = evaluate_control("itinerary_requires_confirmation", {"confirmed": confirmed})
        row = {"item_id": item_id, "tenant": self.tenant, "trip_id": trip_id, "kind": kind, "local_start": local_start, "local_end": local_end, "timezone": timezone, "confirmation": confirmation, "source_evidence": source_evidence, "state": "confirmed" if ctl["ok"] else "confirmation_required", "blockers": ctl["missing"]}
        self.itinerary[item_id] = row; return {"ok": trip_id in self.trips and ctl["ok"], "itinerary_item": row, "side_effects": ()}

    def open_duty_alert(self, alert_id, trip_id, severity, contact_attempts, escalation_owner, acknowledged=False):
        ctl = evaluate_control("duty_of_care_requires_contact_plan", locals())
        row = {"alert_id": alert_id, "tenant": self.tenant, "trip_id": trip_id, "severity": severity, "contact_attempts": tuple(contact_attempts or ()), "escalation_owner": escalation_owner, "acknowledged": acknowledged, "state": "open" if ctl["ok"] else "blocked", "blockers": ctl["missing"]}
        self.duty_alerts[alert_id] = row; return {"ok": trip_id in self.trips and ctl["ok"], "alert": row, "side_effects": ()}

    def open_disruption(self, case_id, trip_id, source, severity, affected_items, options, selected_option, rationale):
        ctl = evaluate_control("disruption_requires_counterfactuals", locals())
        row = {"case_id": case_id, "tenant": self.tenant, "trip_id": trip_id, "source": source, "severity": severity, "affected_items": tuple(affected_items or ()), "options": tuple(options or ()), "selected_option": selected_option, "rationale": rationale, "state": "triaged" if ctl["ok"] else "blocked", "blockers": ctl["missing"]}
        self.disruptions[case_id] = row; return {"ok": trip_id in self.trips and ctl["ok"], "disruption": row, "side_effects": ()}

    def track_unused_ticket(self, ticket_id, traveler_ref, supplier, value, currency, expiration, owner, reuse_eligibility=True):
        ctl = evaluate_control("unused_ticket_requires_expiration_owner", locals())
        row = {"ticket_id": ticket_id, "tenant": self.tenant, "traveler_ref": traveler_ref, "supplier": supplier, "value": value, "currency": currency, "expiration": expiration, "owner": owner, "reuse_eligibility": reuse_eligibility, "state": "available" if ctl["ok"] else "owner_required", "blockers": ctl["missing"]}
        self.unused_tickets[ticket_id] = row; return {"ok": traveler_ref in self.profiles and ctl["ok"], "ticket": row, "side_effects": ()}

    def link_expense_handoff(self, handoff_id, trip_id, approved_budget, booking_refs, expected_categories, per_diem=False, mileage=False):
        trip_state = self.trips.get(trip_id, {}).get("state")
        ctl = evaluate_control("expense_handoff_requires_completed_trip", {"trip_state": trip_state, "approved_budget": approved_budget, "booking_refs": booking_refs, "expected_categories": expected_categories})
        row = {"handoff_id": handoff_id, "tenant": self.tenant, "trip_id": trip_id, "approved_budget": approved_budget, "booking_refs": tuple(booking_refs or ()), "expected_categories": tuple(expected_categories or ()), "per_diem": per_diem, "mileage": mileage, "state": "ready" if ctl["ok"] else "blocked", "blockers": ctl["missing"]}
        self.expense_links[handoff_id] = row; return {"ok": trip_id in self.trips and ctl["ok"], "handoff": row, "side_effects": ()}

    def record_carbon(self, record_id, trip_id, mode, estimate_kg, assumptions, confidence):
        ctl = evaluate_control("carbon_comparison_requires_assumptions", locals())
        row = {"record_id": record_id, "tenant": self.tenant, "trip_id": trip_id, "mode": mode, "estimate_kg": estimate_kg, "assumptions": tuple(assumptions or ()), "confidence": confidence, "state": "comparable" if ctl["ok"] else "blocked", "blockers": ctl["missing"]}
        self.carbon_records[record_id] = row; return {"ok": trip_id in self.trips and ctl["ok"], "carbon": row, "side_effects": ()}

    def complete_trip(self, trip_id):
        ok = trip_id in self.trips and self.trips[trip_id].get("state") in ("approved", "in_trip", "booked")
        if ok: self.trips[trip_id]["state"] = "completed"
        return {"ok": ok, "trip": self.trips.get(trip_id), "side_effects": ()}

    def assistant_preview(self, document, instruction, confirmed=False):
        ctl = evaluate_control("agent_mutations_require_confirmation", {"confirmed": confirmed})
        doc = document_instruction_plan(document, instruction)
        crud = datastore_crud_plan("create", table="travel_management_travel_request", payload={"instruction": instruction})
        return {"ok": doc["ok"] and crud["ok"] and ctl["ok"], "document_plan": doc, "crud_preview": crud, "requires_confirmation": not confirmed, "side_effects": ()}

    def app_contract(self):
        return {"format":"appgen.travel-management.standalone-app.v1", "ok": True, "pbc": PBC_KEY, "database_backends": TRAVEL_MANAGEMENT_ALLOWED_DATABASE_BACKENDS, "event_contract":"AppGen-X", "stream_engine_picker_visible": False, "owned_tables": TRAVEL_MANAGEMENT_OWNED_TABLES, "schema": travel_management_build_schema_contract(), "services": travel_management_build_service_contract(), "routes": travel_management_build_api_contract(), "permissions": travel_management_permissions_contract(), "ui": travel_management_ui_contract(), "workbench": travel_management_render_workbench(), "forms": form_catalog(), "wizards": wizard_catalog(), "controls": control_catalog(), "agent": chatbot_interface_contract(), "composed_agent": composed_agent_contribution(), "dsl": {"pbc": PBC_KEY, "skills_namespace": f"{PBC_KEY}_skills", "single_pbc_app": True}, "side_effects": ()}

    def run_demo(self):
        checks = [self.configure()["ok"]]
        checks.append(self.upsert_traveler_profile("T1", ("sms", "email"), "E1", ("passport",), notification_consent=True)["ok"])
        checks.append(self.define_policy("POL1", "2026-01-01", "employee", "EMEA", "economy", 250)["ok"])
        checks.append(self.request_trip("TRIP-bad", "T1", "client", ("NBO",), "2026-06-10", "2026-06-12", 2200, "low", "missing")["ok"] is False)
        checks.append(self.request_trip("TRIP1", "T1", "client", ("NBO", "LHR"), "2026-06-10", "2026-06-12", 2200, "medium", "POL1")["ok"])
        checks.append(self.route_approval("TRIP1", ("manager", "budget_owner"), "client revenue trip")["ok"])
        checks.append(self.create_booking_intent("BI1", "TRIP1", {"fare":"economy"}, "2026-06-01", ("preferred_air",), ("option-a",))["ok"])
        checks.append(self.record_air_booking("AIR1", "TRIP1", "economy", ("NBO", "LHR"), "2026-06-02", "changeable", "TKT1")["ok"])
        checks.append(self.record_hotel_booking("HOTEL-bad", "TRIP1", "Central", 400, "safe", "24h")["ok"] is False)
        checks.append(self.record_hotel_booking("HOTEL1", "TRIP1", "Central", 220, "safe", "24h")["ok"])
        checks.append(self.ingest_itinerary("IT-bad", "TRIP1", "air", "09:00", "16:00", "Africa/Nairobi", "TKT1", "email", False)["ok"] is False)
        checks.append(self.ingest_itinerary("IT1", "TRIP1", "air", "09:00", "16:00", "Africa/Nairobi", "TKT1", "email", True)["ok"])
        checks.append(self.open_duty_alert("DOC1", "TRIP1", "high", ("sms",), "security") ["ok"])
        checks.append(self.open_disruption("DIS1", "TRIP1", "airline", "medium", ("IT1",), ("reroute", "hotel_extend"), "reroute", "arrives before meeting")["ok"])
        checks.append(self.track_unused_ticket("UT1", "T1", "preferred_air", 450, "USD", "2026-12-01", "travel_desk")["ok"])
        checks.append(self.record_carbon("CAR1", "TRIP1", "air", 840, ("carrier factor",), "medium")["ok"])
        checks.append(self.link_expense_handoff("EXP-bad", "TRIP1", 2200, ("AIR1",), ("air",))["ok"] is False)
        checks.append(self.complete_trip("TRIP1")["ok"])
        checks.append(self.link_expense_handoff("EXP1", "TRIP1", 2200, ("AIR1", "HOTEL1"), ("air", "hotel"), per_diem=True)["ok"])
        checks.append(self.assistant_preview("itinerary pdf", "create itinerary item", False)["ok"] is False)
        checks.append(self.assistant_preview("itinerary pdf", "create itinerary item", True)["ok"])
        return {"ok": all(checks), "contract": self.app_contract(), "side_effects": ()}

def single_pbc_app_contract(): return TravelManagementStandaloneApp().app_contract()
def standalone_smoke_test():
    app = TravelManagementStandaloneApp(); demo = app.run_demo(); runtime = travel_management_runtime_smoke(); contract = single_pbc_app_contract()
    return {"ok": demo["ok"] and runtime["ok"] and contract["ok"], "demo": demo, "runtime": runtime, "contract": contract, "side_effects": ()}
