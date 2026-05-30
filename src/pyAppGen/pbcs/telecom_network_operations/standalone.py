"""Standalone Telecom Network Operations application contract."""
from __future__ import annotations
from dataclasses import dataclass, field
from hashlib import sha256
from typing import Any
from .agent import chatbot_interface_contract, composed_agent_contribution, datastore_crud_plan, document_instruction_plan
from .controls import control_catalog, evaluate_control
from .forms import form_catalog
from .runtime import *
from .ui import telecom_network_operations_render_workbench, telecom_network_operations_ui_contract
from .wizards import wizard_catalog

PBC_KEY = "telecom_network_operations"
def _digest(value: Any) -> str: return sha256(repr(value).encode('utf-8')).hexdigest()

@dataclass
class TelecomNetworkOperationsStandaloneApp:
    tenant: str = "tenant-telecom-001"
    state: dict = field(default_factory=telecom_network_operations_empty_state)
    sites: dict[str, dict] = field(default_factory=dict)
    cells: dict[str, dict] = field(default_factory=dict)
    circuits: dict[str, dict] = field(default_factory=dict)
    alarms: dict[str, dict] = field(default_factory=dict)
    incidents: dict[str, dict] = field(default_factory=dict)
    cases: dict[str, dict] = field(default_factory=dict)
    windows: dict[str, dict] = field(default_factory=dict)
    sla: dict[str, dict] = field(default_factory=dict)
    capacity: dict[str, dict] = field(default_factory=dict)

    def configure(self, database_backend="postgresql"):
        cfg=telecom_network_operations_configure_runtime(self.state,{"database_backend":database_backend,"event_topic":TELECOM_NETWORK_OPERATIONS_REQUIRED_EVENT_TOPIC}); self.state=cfg["state"]
        for name,value in (("alarm_correlation_window_minutes",15),("sla_breach_warning_minutes",30),("capacity_headroom_floor",.15),("assistant_confirmation_required",True)):
            res=telecom_network_operations_set_parameter(self.state,name,value); self.state=res["state"]
        for rule_id in ("site_has_geospatial_identity","alarm_is_normalized","maintenance_has_rollback","sla_clock_exclusion_approved","capacity_headroom_positive","agent_mutations_require_confirmation"):
            res=telecom_network_operations_register_rule(self.state,{"rule_id":rule_id,"scope":"noc"}); self.state=res["state"]
        inbound=telecom_network_operations_receive_event(self.state,{"event_type":TELECOM_NETWORK_OPERATIONS_CONSUMED_EVENT_TYPES[0],"idempotency_key":"telecom-policy-001"}); self.state=inbound["state"]
        return {"ok": cfg["ok"] and inbound["ok"], "side_effects": ()}

    def register_site(self, site_id, site_code, latitude, longitude, site_type, access_restrictions=None):
        ctl=evaluate_control("site_has_geospatial_identity", locals())
        row={"id":site_id,"tenant":self.tenant,"site_code":site_code,"latitude":latitude,"longitude":longitude,"site_type":site_type,"access_restrictions":access_restrictions,"status":"active" if ctl["ok"] else "blocked","blockers":ctl["failures"]}
        self.sites[site_id]=row; return {"ok":ctl["ok"],"site":row,"side_effects":()}

    def model_radio_cell(self, cell_id, site_id, technology, sector, carrier="n78", band="3500", pci_or_psc="100"):
        ctl=evaluate_control("radio_cell_has_parent_site", locals())
        row={"id":cell_id,"tenant":self.tenant,"site_id":site_id,"technology":technology,"sector":sector,"carrier":carrier,"band":band,"pci_or_psc":pci_or_psc,"status":"modeled" if ctl["ok"] else "blocked","blockers":ctl["failures"]}
        self.cells[cell_id]=row; return {"ok":site_id in self.sites and ctl["ok"],"cell":row,"side_effects":()}

    def register_circuit_path(self, circuit_id, a_end, z_end, route_membership, protected=True, service_class="enterprise"):
        ctl=evaluate_control("circuit_path_has_endpoints", locals())
        row={"id":circuit_id,"tenant":self.tenant,"a_end":a_end,"z_end":z_end,"route_membership":tuple(route_membership or ()),"protected":protected,"service_class":service_class,"status":"active" if ctl["ok"] else "blocked","blockers":ctl["failures"]}
        self.circuits[circuit_id]=row; return {"ok":ctl["ok"],"circuit":row,"side_effects":()}

    def normalize_alarm(self, alarm_id, raw_vendor_code, normalized_family, severity, probable_cause, object_class, target_id=None):
        ctl=evaluate_control("alarm_is_normalized", locals())
        row={"id":alarm_id,"tenant":self.tenant,"raw_vendor_code":raw_vendor_code,"normalized_family":normalized_family,"severity":severity,"probable_cause":probable_cause,"object_class":object_class,"target_id":target_id,"status":"raised" if ctl["ok"] else "quarantine","blockers":ctl["failures"]}
        self.alarms[alarm_id]=row; return {"ok":ctl["ok"],"alarm":row,"side_effects":()}

    def correlate_root_cause(self, correlation_id, parent_alarm_id, child_alarm_ids):
        ctl=evaluate_control("root_cause_correlation_has_parent", {"parent":parent_alarm_id})
        row={"id":correlation_id,"tenant":self.tenant,"parent_alarm_id":parent_alarm_id,"child_alarm_ids":tuple(child_alarm_ids),"suppressed_count":len(tuple(child_alarm_ids)),"status":"correlated" if ctl["ok"] else "blocked","blockers":ctl["failures"]}
        self.alarms[correlation_id]=row; return {"ok":parent_alarm_id in self.alarms and ctl["ok"],"correlation":row,"side_effects":()}

    def declare_outage(self, incident_id, state, bridge_commander, impacted_services, restoration_eta=None):
        ctl=evaluate_control("outage_declaration_complete", locals())
        row={"id":incident_id,"tenant":self.tenant,"state":state,"bridge_commander":bridge_commander,"impacted_services":tuple(impacted_services or ()),"restoration_eta":restoration_eta,"status":"war_room" if ctl["ok"] else "draft","blockers":ctl["failures"]}
        self.incidents[incident_id]=row; return {"ok":ctl["ok"],"incident":row,"side_effects":()}

    def approve_maintenance_window(self, window_id, mop_version, rollback_plan, scope, freeze_window=False, freeze_exception=False):
        ctl=evaluate_control("maintenance_has_rollback", locals())
        row={"id":window_id,"tenant":self.tenant,"mop_version":mop_version,"rollback_plan":rollback_plan,"scope":tuple(scope or ()),"freeze_window":freeze_window,"status":"approved" if ctl["ok"] else "blocked","blockers":ctl["failures"]}
        self.windows[window_id]=row; return {"ok":ctl["ok"],"window":row,"side_effects":()}

    def calculate_sla_impact(self, impact_id, case_id, excluded=False, exclusion_approved=False, reason=None):
        ctl=evaluate_control("sla_clock_exclusion_approved", locals())
        row={"id":impact_id,"tenant":self.tenant,"case_id":case_id,"excluded":excluded,"exclusion_approved":exclusion_approved,"reason":reason,"clock_state":"excluded" if excluded and ctl["ok"] else "running","status":"calculated" if ctl["ok"] else "blocked","blockers":ctl["failures"]}
        self.sla[impact_id]=row; return {"ok":ctl["ok"],"sla":row,"side_effects":()}

    def record_capacity_snapshot(self, segment_id, installed, reserved, used, emergency_headroom=False, capacity_class="radio"):
        ctl=evaluate_control("capacity_headroom_positive", locals())
        utilization=round((used+reserved)/installed,4) if installed else 0
        row={"id":segment_id,"tenant":self.tenant,"installed":installed,"reserved":reserved,"used":used,"capacity_class":capacity_class,"utilization":utilization,"status":"healthy" if ctl["ok"] else "overcommitted","blockers":ctl["failures"]}
        self.capacity[segment_id]=row; return {"ok":ctl["ok"],"capacity":row,"side_effects":()}

    def open_assurance_case(self, case_id, incident_id, severity, customer_impact, dispatch_status="monitor"):
        row={"id":case_id,"tenant":self.tenant,"incident_id":incident_id,"severity":severity,"customer_impact":customer_impact,"dispatch_status":dispatch_status,"status":"open"}
        self.cases[case_id]=row; return {"ok":incident_id in self.incidents,"case":row,"side_effects":()}

    def capture_field_evidence(self, evidence_id, case_id, evidence_digest=None, closure_note=None):
        ctl=evaluate_control("field_evidence_traceable", locals())
        row={"id":evidence_id,"tenant":self.tenant,"case_id":case_id,"evidence_digest":evidence_digest,"closure_note":closure_note,"status":"accepted" if ctl["ok"] else "blocked","blockers":ctl["failures"]}
        self.cases[evidence_id]=row; return {"ok":case_id in self.cases and ctl["ok"],"evidence":row,"side_effects":()}

    def simulate_reroute_playbook(self, circuit_id, alternate_paths):
        return {"ok":circuit_id in self.circuits and bool(alternate_paths),"mutates_live_records":False,"circuit_id":circuit_id,"eligible_paths":tuple(alternate_paths),"evidence_hash":_digest((circuit_id,tuple(alternate_paths))),"side_effects":()}

    def assistant_alarm_triage_preview(self, document, instruction, confirmed=False):
        ctl=evaluate_control("agent_mutations_require_confirmation", {"confirmed":confirmed})
        doc=document_instruction_plan(document,instruction); crud=datastore_crud_plan("create", table="telecom_network_operations_network_incident", payload={"instruction":instruction})
        return {"ok":doc["ok"] and crud["ok"] and ctl["ok"],"document_plan":doc,"crud_preview":crud,"control":ctl,"requires_confirmation":not confirmed,"side_effects":()}

    def app_contract(self):
        return {"format":"appgen.telecom-network-operations.standalone-app.v1","ok":True,"pbc":PBC_KEY,"owned_tables":TELECOM_NETWORK_OPERATIONS_OWNED_TABLES,"database_backends":TELECOM_NETWORK_OPERATIONS_ALLOWED_DATABASE_BACKENDS,"event_contract":"AppGen-X","stream_engine_picker_visible":False,"schema":telecom_network_operations_build_schema_contract(),"services":telecom_network_operations_build_service_contract(),"routes":telecom_network_operations_build_api_contract(),"permissions":telecom_network_operations_permissions_contract(),"ui":telecom_network_operations_ui_contract(),"workbench":telecom_network_operations_render_workbench(),"forms":form_catalog(),"wizards":wizard_catalog(),"controls":control_catalog(),"agent":chatbot_interface_contract(),"composed_agent":composed_agent_contribution(),"dsl":{"pbc":PBC_KEY,"skills_namespace":f"{PBC_KEY}_skills","single_pbc_app":True},"side_effects":()}

    def run_demo(self):
        cfg=self.configure(); bad_site=self.register_site("S0","SITE",None,36.8,"macro"); site=self.register_site("S1","SITE-1",-1.2,36.8,"macro")
        bad_cell=self.model_radio_cell("C0","missing","5G","A"); cell=self.model_radio_cell("C1","S1","5G","A")
        bad_circuit=self.register_circuit_path("CK0","A",None,()); circuit=self.register_circuit_path("CK1","S1","POP1",("fiber-1","agg-1"),True)
        bad_alarm=self.normalize_alarm("AL0","RAW",None,"critical","loss","cell"); alarm=self.normalize_alarm("AL1","RAW","transport_loss","critical","fiber_cut","circuit","CK1")
        bad_corr=self.correlate_root_cause("COR0",None,("AL1",)); corr=self.correlate_root_cause("COR1","AL1",("AL2","AL3"))
        bad_outage=self.declare_outage("I0","declared",None,("svc",)); outage=self.declare_outage("I1","declared","noc-chief",("enterprise-vpn",),"30m")
        bad_window=self.approve_maintenance_window("MW0","MOP1",None,("S1",)); window=self.approve_maintenance_window("MW1","MOP1","rollback to protected path",("S1",))
        bad_sla=self.calculate_sla_impact("SLA0","CASE1",True,False); sla=self.calculate_sla_impact("SLA1","CASE1",True,True,"planned work exclusion")
        bad_capacity=self.record_capacity_snapshot("CAP0",100,80,40); capacity=self.record_capacity_snapshot("CAP1",100,20,40)
        case=self.open_assurance_case("CASE1","I1","P1","500 enterprise circuits")
        bad_evidence=self.capture_field_evidence("FE0","CASE1"); evidence=self.capture_field_evidence("FE1","CASE1","photo-hash","splice complete")
        playbook=self.simulate_reroute_playbook("CK1",("alt-1",)); agent_bad=self.assistant_alarm_triage_preview("alarms","create outage",False); agent=self.assistant_alarm_triage_preview("alarms","create outage",True)
        checks=(cfg["ok"],bad_site["ok"] is False,site["ok"],bad_cell["ok"] is False,cell["ok"],bad_circuit["ok"] is False,circuit["ok"],bad_alarm["ok"] is False,alarm["ok"],bad_corr["ok"] is False,corr["ok"],bad_outage["ok"] is False,outage["ok"],bad_window["ok"] is False,window["ok"],bad_sla["ok"] is False,sla["ok"],bad_capacity["ok"] is False,capacity["ok"],case["ok"],bad_evidence["ok"] is False,evidence["ok"],playbook["mutates_live_records"] is False,agent_bad["ok"] is False,agent["ok"])
        return {"ok":all(checks),"app_contract":self.app_contract(),"side_effects":()}

def single_pbc_app_contract(): return TelecomNetworkOperationsStandaloneApp().app_contract()
def standalone_smoke_test():
    app=TelecomNetworkOperationsStandaloneApp(); demo=app.run_demo(); runtime=telecom_network_operations_runtime_smoke(); contract=single_pbc_app_contract()
    return {"ok":demo["ok"] and runtime["ok"] and contract["ok"] and bool(TELECOM_NETWORK_OPERATIONS_EMITTED_EVENT_TYPES),"demo":demo,"runtime":runtime,"contract":contract,"side_effects":()}
