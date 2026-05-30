"""Standalone one-PBC application for maritime_shipping_operations."""
from __future__ import annotations
from dataclasses import dataclass, field
from hashlib import sha256
from typing import Any
from .agent import chatbot_interface_contract, composed_agent_contribution, datastore_crud_plan, document_instruction_plan
from .controls import control_catalog, evaluate_control
from .forms import form_catalog
from .runtime import (
    MARITIME_SHIPPING_OPERATIONS_ALLOWED_DATABASE_BACKENDS, MARITIME_SHIPPING_OPERATIONS_CONSUMED_EVENT_TYPES,
    MARITIME_SHIPPING_OPERATIONS_EMITTED_EVENT_TYPES, MARITIME_SHIPPING_OPERATIONS_OWNED_TABLES,
    MARITIME_SHIPPING_OPERATIONS_REQUIRED_EVENT_TOPIC, maritime_shipping_operations_build_api_contract,
    maritime_shipping_operations_build_schema_contract, maritime_shipping_operations_build_service_contract,
    maritime_shipping_operations_configure_runtime, maritime_shipping_operations_empty_state,
    maritime_shipping_operations_permissions_contract, maritime_shipping_operations_receive_event,
    maritime_shipping_operations_register_rule, maritime_shipping_operations_runtime_smoke,
    maritime_shipping_operations_set_parameter,
)
from .ui import maritime_shipping_operations_render_workbench, maritime_shipping_operations_ui_contract
from .wizards import wizard_catalog
PBC_KEY = "maritime_shipping_operations"

def _digest(value: Any) -> str:
    return sha256(repr(value).encode("utf-8")).hexdigest()

@dataclass
class MaritimeShippingOperationsStandaloneApp:
    tenant: str = "tenant-maritime-001"
    state: dict = field(default_factory=maritime_shipping_operations_empty_state)
    vessels: dict[str, dict] = field(default_factory=dict)
    voyages: dict[str, dict] = field(default_factory=dict)
    bookings: dict[str, dict] = field(default_factory=dict)
    charters: dict[str, dict] = field(default_factory=dict)
    port_calls: dict[str, dict] = field(default_factory=dict)
    claims: dict[str, dict] = field(default_factory=dict)
    bunkers: dict[str, dict] = field(default_factory=dict)
    obligations: dict[str, dict] = field(default_factory=dict)

    def configure(self, database_backend: str = "postgresql") -> dict:
        configured = maritime_shipping_operations_configure_runtime(self.state, {"database_backend": database_backend, "event_topic": MARITIME_SHIPPING_OPERATIONS_REQUIRED_EVENT_TOPIC})
        self.state = configured["state"]
        for name, value in (("min_schedule_buffer_hours", 12), ("reefer_alert_celsius", 2), ("laytime_warning_percent", 80), ("demurrage_escalation_usd", 25000), ("bunker_variance_percent", 8), ("carbon_speedup_threshold", 0.12)):
            result = maritime_shipping_operations_set_parameter(self.state, name, value); self.state = result["state"]
        for rule in (
            {"rule_id":"vessel_ready_before_publish","scope":"voyage"}, {"rule_id":"capacity_cutoff_screening_before_booking","scope":"booking"}, {"rule_id":"sof_required_for_laytime","scope":"port_call"}, {"rule_id":"rob_and_sulfur_before_bunker","scope":"bunker"}, {"rule_id":"obligations_before_document_release","scope":"compliance"},
        ):
            registered=maritime_shipping_operations_register_rule(self.state, rule); self.state=registered["state"]
        received=maritime_shipping_operations_receive_event(self.state, {"event_type": MARITIME_SHIPPING_OPERATIONS_CONSUMED_EVENT_TYPES[0], "idempotency_key":"maritime-policy-001"})
        self.state=received["state"]
        return {"ok": configured["ok"] and received["ok"], "side_effects": ()}

    def register_vessel(self, vessel_id: str, imo: str, safe_manning_valid: bool, certificates_valid: bool, cargo_gear_ready: bool) -> dict:
        ready = safe_manning_valid and certificates_valid and cargo_gear_ready
        vessel={"id":vessel_id,"imo":imo,"safe_manning_valid":safe_manning_valid,"certificates_valid":certificates_valid,"cargo_gear_ready":cargo_gear_ready,"readiness":"ready" if ready else "blocked"}
        self.vessels[vessel_id]=vessel
        return {"ok": ready, "vessel": vessel, "side_effects": ()}

    def create_voyage(self, voyage_id: str, vessel_id: str, service_string: str, trade_lane: str, legs: tuple[dict, ...]) -> dict:
        vessel=self.vessels[vessel_id]
        ordered=all(legs[i]["seq"] < legs[i+1]["seq"] for i in range(len(legs)-1)) if len(legs)>1 else True
        ok=vessel["readiness"]=="ready" and ordered
        voyage={"id":voyage_id,"vessel_id":vessel_id,"service_string":service_string,"trade_lane":trade_lane,"legs":legs,"status":"published" if ok else "blocked","delay_buckets":{},"events":(("voyage_published", voyage_id),) if ok else ()}
        self.voyages[voyage_id]=voyage
        return {"ok": ok, "voyage": voyage, "emitted_event":"MaritimeShippingOperationsCreated" if ok else None, "side_effects": ()}

    def propagate_leg_delay(self, voyage_id: str, leg_seq: int, delay_hours: int, reason: str) -> dict:
        voyage=dict(self.voyages[voyage_id]); adjusted=[]
        for leg in voyage["legs"]:
            row=dict(leg)
            if row["seq"] >= leg_seq:
                row["revised_eta_hour"] = row.get("revised_eta_hour", row.get("eta_hour", 0)) + delay_hours
            adjusted.append(row)
        voyage["legs"]=tuple(adjusted); voyage["delay_buckets"][reason]=voyage["delay_buckets"].get(reason,0)+delay_hours; voyage["events"]=voyage.get("events",())+(("schedule_slipped", reason, delay_hours),)
        self.voyages[voyage_id]=voyage
        return {"ok": True, "voyage": voyage, "emitted_event":"MaritimeShippingOperationsUpdated", "side_effects": ()}

    def create_booking(self, booking_id: str, voyage_id: str, leg_seq: int, shipper: str, consignee: str, teu: int, weight: float, commodity: str, dg_class: str|None=None, reefer_setpoint: float|None=None) -> dict:
        existing_teu=sum(b["teu"] for b in self.bookings.values() if b["voyage_id"]==voyage_id and b["leg_seq"]==leg_seq and b["status"] in {"accepted","conditional"})
        capacity=1000
        special_missing=bool(dg_class) and commodity != "dangerous_goods" or reefer_setpoint is not None and teu <= 0
        ok=existing_teu+teu <= capacity and not special_missing and "restricted" not in (shipper.lower(), consignee.lower())
        booking={"id":booking_id,"voyage_id":voyage_id,"leg_seq":leg_seq,"shipper":shipper,"consignee":consignee,"teu":teu,"weight":weight,"commodity":commodity,"dg_class":dg_class,"reefer_setpoint":reefer_setpoint,"status":"accepted" if ok else "waitlisted_or_blocked","bill_status":"draft","cutoffs":{"docs":"open","vgm":"open","hazardous":"open"}}
        self.bookings[booking_id]=booking
        return {"ok": ok, "booking": booking, "side_effects": ()}

    def issue_bill(self, booking_id: str, freight_term: str, originals: int, release_mode: str) -> dict:
        booking=dict(self.bookings[booking_id])
        ok=booking["status"]=="accepted" and originals >= 0 and release_mode in {"original","telex","seaway"}
        booking.update({"freight_term":freight_term,"originals":originals,"release_mode":release_mode,"bill_status":"issued" if ok else "blocked"})
        self.bookings[booking_id]=booking
        return {"ok": ok, "booking": booking, "side_effects": ()}

    def validate_stowage(self, booking_id: str, bay: str, discharge_sequence: int, segregation_clear: bool, lashing_ready: bool, reefer_plug: bool=True) -> dict:
        booking=dict(self.bookings[booking_id])
        ok=segregation_clear and lashing_ready and (booking.get("reefer_setpoint") is None or reefer_plug)
        booking["stowage"]={"bay_row_tier":bay,"discharge_sequence":discharge_sequence,"segregation_clear":segregation_clear,"lashing_ready":lashing_ready,"reefer_plug":reefer_plug,"status":"feasible" if ok else "blocked"}
        self.bookings[booking_id]=booking
        return {"ok": ok, "booking": booking, "side_effects": ()}

    def register_charter(self, charter_id: str, voyage_id: str, load_rate: float, discharge_rate: float, demurrage_rate: float, shex_shinc: str) -> dict:
        charter={"id":charter_id,"voyage_id":voyage_id,"load_rate":load_rate,"discharge_rate":discharge_rate,"demurrage_rate":demurrage_rate,"shex_shinc":shex_shinc,"clause_version":1}
        self.charters[charter_id]=charter
        return {"ok": load_rate>0 and discharge_rate>0 and demurrage_rate>0, "charter": charter, "side_effects": ()}

    def capture_port_call(self, port_call_id: str, voyage_id: str, port: str, terminal: str, berth_window: tuple[int,int], events: tuple[tuple[str,int], ...]) -> dict:
        names=[e[0] for e in events]
        required={"nor_tendered","all_fast","cargo_ops_start","cargo_ops_stop","final_line"}
        ok=required.issubset(names) and berth_window[0] < berth_window[1]
        call={"id":port_call_id,"voyage_id":voyage_id,"port":port,"terminal":terminal,"berth_window":berth_window,"events":events,"timezone":"local+utc","status":"complete" if ok else "incomplete"}
        self.port_calls[port_call_id]=call
        return {"ok": ok, "port_call": call, "side_effects": ()}

    def compute_laytime_and_claim(self, claim_id: str, charter_id: str, port_call_id: str, allowed_hours: float, responsible_party: str) -> dict:
        call=self.port_calls[port_call_id]; charter=self.charters[charter_id]
        ev=dict(call["events"]); used=max(0, ev.get("cargo_ops_stop",0)-ev.get("cargo_ops_start",0))
        excess=max(0, used-allowed_hours); amount=round(excess/24*charter["demurrage_rate"],2)
        ok=call["status"]=="complete"
        claim={"id":claim_id,"charter_id":charter_id,"port_call_id":port_call_id,"used_hours":used,"allowed_hours":allowed_hours,"demurrage_amount":amount,"responsible_party":responsible_party,"dossier":("sof","charter_clause","weather_log"),"status":"draft" if ok else "blocked"}
        self.claims[claim_id]=claim
        return {"ok": ok, "claim": claim, "side_effects": ()}

    def plan_bunkers(self, bunker_id: str, voyage_id: str, uplift_port: str, grade: str, quantity: float, departure_rob: float, required_burn: float, sulfur_context: str, speedup: bool=False) -> dict:
        arrival_rob=departure_rob+quantity-required_burn
        emissions=round(required_burn*(3.114 if grade != "lng" else 2.75)*(1.12 if speedup else 1.0),2)
        ok=arrival_rob>=50 and sulfur_context in {"global_cap","eca_compliant"}
        bunker={"id":bunker_id,"voyage_id":voyage_id,"uplift_port":uplift_port,"grade":grade,"quantity":quantity,"departure_rob":departure_rob,"arrival_rob":arrival_rob,"required_burn":required_burn,"sulfur_context":sulfur_context,"emissions_tonnes":emissions,"status":"approved" if ok else "blocked"}
        self.bunkers[bunker_id]=bunker
        return {"ok": ok, "bunker": bunker, "side_effects": ()}

    def register_obligation(self, obligation_id: str, voyage_id: str, obligation_type: str, due_hour: int, screening_clear: bool, closure_evidence: str|None=None) -> dict:
        ok=screening_clear and bool(closure_evidence)
        obligation={"id":obligation_id,"voyage_id":voyage_id,"obligation_type":obligation_type,"due_hour":due_hour,"screening_clear":screening_clear,"closure_evidence":closure_evidence,"status":"closed" if ok else "open_or_blocked"}
        self.obligations[obligation_id]=obligation
        return {"ok": ok, "obligation": obligation, "side_effects": ()}

    def simulate_recovery(self, voyage_id: str, option: str, speed_delta: float=0.0) -> dict:
        voyage=self.voyages[voyage_id]
        customer_impact={"skip_call": "high", "speed_up": "low", "berth_swap": "medium"}.get(option,"medium")
        bunker_cost_delta=round(abs(speed_delta)*12000,2)
        carbon_delta=round(abs(speed_delta)*0.08,3)
        return {"ok": True, "mutates_live_records": False, "option": option, "voyage_id": voyage_id, "customer_impact": customer_impact, "bunker_cost_delta": bunker_cost_delta, "carbon_delta": carbon_delta, "facts_used": (voyage["service_string"], voyage["trade_lane"]), "side_effects": ()}

    def assistant_maritime_action_preview(self, document: str, instruction: str) -> dict:
        plan=document_instruction_plan(document, instruction)
        crud=datastore_crud_plan("update", table="maritime_shipping_operations_voyage", payload={"instruction":instruction})
        return {"ok": plan["ok"] and crud["ok"], "document_plan":plan, "crud_preview":crud, "requires_confirmation":True, "affected_events":("voyage_schedule_slipped","booking_amended"), "side_effects": ()}

    def app_contract(self) -> dict:
        return {"format":"appgen.maritime-shipping-operations.standalone-app.v1","ok":True,"pbc":PBC_KEY,"owned_tables":MARITIME_SHIPPING_OPERATIONS_OWNED_TABLES,"database_backends":MARITIME_SHIPPING_OPERATIONS_ALLOWED_DATABASE_BACKENDS,"event_contract":"AppGen-X","stream_engine_picker_visible":False,"schema":maritime_shipping_operations_build_schema_contract(),"services":maritime_shipping_operations_build_service_contract(),"routes":maritime_shipping_operations_build_api_contract(),"permissions":maritime_shipping_operations_permissions_contract(),"ui":maritime_shipping_operations_ui_contract(),"workbench":maritime_shipping_operations_render_workbench(),"forms":form_catalog(),"wizards":wizard_catalog(),"controls":control_catalog(),"agent":chatbot_interface_contract(),"composed_agent":composed_agent_contribution(),"dsl":{"pbc":PBC_KEY,"skills_namespace":f"{PBC_KEY}_skills","single_pbc_app":True},"side_effects": ()}

    def run_demo(self) -> dict:
        cfg=self.configure()
        vessel_bad=self.register_vessel("VES-BAD","IMO000",False,True,True)
        vessel=self.register_vessel("VES-001","IMO1234567",True,True,True)
        voyage=self.create_voyage("VOY-001","VES-001","EAF-MED","Mombasa-Mediterranean",({"seq":1,"from":"MBA","to":"JED","eta_hour":100},{"seq":2,"from":"JED","to":"PIR","eta_hour":220}))
        delay=self.propagate_leg_delay("VOY-001",1,18,"congestion")
        booking=self.create_booking("BKG-001","VOY-001",1,"shipper-a","consignee-a",20,24000,"dry_goods")
        dg_bad=self.create_booking("BKG-DG","VOY-001",1,"shipper-a","consignee-a",2,4000,"dry_goods",dg_class="3")
        bill=self.issue_bill("BKG-001","prepaid",3,"original")
        stow=self.validate_stowage("BKG-001","12-04-82",2,True,True)
        charter=self.register_charter("CHTR-001","VOY-001",5000,4500,30000,"SHINC")
        call_bad=self.capture_port_call("CALL-BAD","VOY-001","MBA","T1",(10,20),(('nor_tendered',11),))
        call=self.capture_port_call("CALL-001","VOY-001","MBA","T1",(10,20),(('nor_tendered',11),('all_fast',12),('cargo_ops_start',14),('cargo_ops_stop',70),('final_line',75)))
        claim=self.compute_laytime_and_claim("CLM-001","CHTR-001","CALL-001",48,"terminal")
        bunker_bad=self.plan_bunkers("BNK-BAD","VOY-001","MBA","hsfo",10,20,60,"global_cap")
        bunker=self.plan_bunkers("BNK-001","VOY-001","MBA","vlsfo",400,120,360,"eca_compliant",speedup=True)
        obligation_bad=self.register_obligation("OBL-BAD","VOY-001","sanctions",80,False,None)
        obligation=self.register_obligation("OBL-001","VOY-001","customs_manifest",80,True,"manifest accepted")
        simulation=self.simulate_recovery("VOY-001","speed_up",1.5)
        assistant=self.assistant_maritime_action_preview("shipping instruction", "revise ETA and notify bookings")
        checks=(cfg["ok"], vessel_bad["ok"] is False, vessel["ok"], voyage["ok"], delay["ok"], booking["ok"], dg_bad["ok"] is False, bill["ok"], stow["ok"], charter["ok"], call_bad["ok"] is False, call["ok"], claim["ok"], bunker_bad["ok"] is False, bunker["ok"], obligation_bad["ok"] is False, obligation["ok"], simulation["ok"] and simulation["mutates_live_records"] is False, assistant["ok"])
        return {"ok": all(checks), "vessel_bad":vessel_bad,"dg_bad":dg_bad,"call_bad":call_bad,"bunker_bad":bunker_bad,"obligation_bad":obligation_bad,"claim":claim,"simulation":simulation,"assistant":assistant,"app_contract":self.app_contract(),"side_effects": ()}

def single_pbc_app_contract() -> dict:
    return MaritimeShippingOperationsStandaloneApp().app_contract()

def standalone_smoke_test() -> dict:
    app=MaritimeShippingOperationsStandaloneApp(); demo=app.run_demo(); runtime=maritime_shipping_operations_runtime_smoke(); contract=single_pbc_app_contract()
    return {"ok": demo["ok"] and runtime["ok"] and contract["ok"] and bool(MARITIME_SHIPPING_OPERATIONS_EMITTED_EVENT_TYPES) and contract["stream_engine_picker_visible"] is False, "demo":demo,"runtime":runtime,"contract":contract,"side_effects": ()}
