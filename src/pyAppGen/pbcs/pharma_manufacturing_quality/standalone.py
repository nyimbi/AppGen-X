"""Standalone pharma manufacturing quality application."""
from __future__ import annotations
from dataclasses import dataclass, field
from hashlib import sha256
from typing import Any
from .agent import chatbot_interface_contract, composed_agent_contribution, datastore_crud_plan, document_instruction_plan
from .controls import control_catalog, evaluate_control
from .forms import form_catalog
from .runtime import PHARMA_MANUFACTURING_QUALITY_ALLOWED_DATABASE_BACKENDS, PHARMA_MANUFACTURING_QUALITY_CONSUMED_EVENT_TYPES, PHARMA_MANUFACTURING_QUALITY_EMITTED_EVENT_TYPES, PHARMA_MANUFACTURING_QUALITY_OWNED_TABLES, PHARMA_MANUFACTURING_QUALITY_REQUIRED_EVENT_TOPIC, pharma_manufacturing_quality_build_api_contract, pharma_manufacturing_quality_build_schema_contract, pharma_manufacturing_quality_build_service_contract, pharma_manufacturing_quality_configure_runtime, pharma_manufacturing_quality_empty_state, pharma_manufacturing_quality_permissions_contract, pharma_manufacturing_quality_receive_event, pharma_manufacturing_quality_register_rule, pharma_manufacturing_quality_runtime_smoke, pharma_manufacturing_quality_set_parameter
from .ui import pharma_manufacturing_quality_render_workbench, pharma_manufacturing_quality_ui_contract
from .wizards import wizard_catalog
PBC_KEY="pharma_manufacturing_quality"
def _digest(value:Any)->str: return sha256(repr(value).encode("utf-8")).hexdigest()
@dataclass
class PharmaManufacturingQualityStandaloneApp:
    tenant:str="tenant-pharma-001"; state:dict=field(default_factory=pharma_manufacturing_quality_empty_state)
    mbrs:dict[str,dict]=field(default_factory=dict); batches:dict[str,dict]=field(default_factory=dict); deviations:dict[str,dict]=field(default_factory=dict); capas:dict[str,dict]=field(default_factory=dict); validations:dict[str,dict]=field(default_factory=dict); serials:dict[str,dict]=field(default_factory=dict); releases:dict[str,dict]=field(default_factory=dict)
    def configure(self,database_backend="postgresql"):
        cfg=pharma_manufacturing_quality_configure_runtime(self.state,{"database_backend":database_backend,"event_topic":PHARMA_MANUFACTURING_QUALITY_REQUIRED_EVENT_TOPIC}); self.state=cfg["state"]
        for n,v in (("cpp_review_sla_hours",24),("major_deviation_due_days",30),("capa_effectiveness_days",90),("serialization_order_strict",True),("release_requires_qa",True)):
            r=pharma_manufacturing_quality_set_parameter(self.state,n,v); self.state=r["state"]
        for rule in ("active_mbr_required","ebr_steps_require_signatures","cpp_excursion_opens_deviation","major_deviation_requires_root_cause","release_requires_complete_quality_checklist"):
            r=pharma_manufacturing_quality_register_rule(self.state,{"rule_id":rule,"scope":"gmp"}); self.state=r["state"]
        ev=pharma_manufacturing_quality_receive_event(self.state,{"event_type":PHARMA_MANUFACTURING_QUALITY_CONSUMED_EVENT_TYPES[0],"idempotency_key":"pharma-policy-001"}); self.state=ev["state"]
        return {"ok":cfg["ok"] and ev["ok"],"side_effects":()}
    def approve_mbr(self,mbr_id,product,strength,version,effective,critical_parameters):
        ok=bool(product) and bool(version) and bool(critical_parameters); m={"id":mbr_id,"product":product,"strength":strength,"version":version,"effective":effective,"critical_parameters":critical_parameters,"status":"active" if ok else "draft"}; self.mbrs[mbr_id]=m; return {"ok":ok,"mbr":m,"side_effects":()}
    def start_batch(self,batch_id,mbr_id,input_lots,equipment_projection,training_clear=True):
        ctl=evaluate_control("active_mbr_required",{"mbr_active":self.mbrs.get(mbr_id,{}).get("status")=="active"}); ok=ctl["ok"] and bool(input_lots) and equipment_projection.get("qualified") and training_clear
        b={"id":batch_id,"mbr_id":mbr_id,"input_lots":input_lots,"equipment_projection":equipment_projection,"training_clear":training_clear,"steps":[],"status":"in_process" if ok else "blocked_start"}; self.batches[batch_id]=b; return {"ok":ok,"batch":b,"side_effects":()}
    def execute_step(self,batch_id,step,expected,actual,low,high,performed_by,verified_by):
        sig=evaluate_control("ebr_steps_require_signatures",{"performed_by":performed_by,"verified_by":verified_by}); cpp=evaluate_control("cpp_excursion_opens_deviation",{"actual":actual,"low":low,"high":high}); ok=sig["ok"] and cpp["ok"]
        row={"step":step,"expected":expected,"actual":actual,"range":(low,high),"performed_by":performed_by,"verified_by":verified_by,"status":"accepted" if ok else "deviation_required"}; self.batches[batch_id]["steps"].append(row)
        if not cpp["ok"]: self.open_deviation(f"DEV-{batch_id}-{step}",batch_id,"process","major","CPP excursion",None)
        return {"ok":ok,"step":row,"side_effects":()}
    def open_deviation(self,deviation_id,batch_id,category,severity,containment,root_cause):
        ctl=evaluate_control("major_deviation_requires_root_cause",{"severity":severity,"root_cause":root_cause}); d={"id":deviation_id,"batch_id":batch_id,"category":category,"severity":severity,"containment":containment,"root_cause":root_cause,"status":"closed" if ctl["ok"] else "investigation_open"}; self.deviations[deviation_id]=d; return {"ok":ctl["ok"],"deviation":d,"side_effects":()}
    def create_capa(self,capa_id,deviation_id,corrective,preventive,effectiveness_evidence):
        ctl=evaluate_control("capa_requires_effectiveness",{"effectiveness_evidence":effectiveness_evidence}); ok=deviation_id in self.deviations and ctl["ok"]; c={"id":capa_id,"deviation_id":deviation_id,"corrective":corrective,"preventive":preventive,"effectiveness_evidence":effectiveness_evidence,"status":"closed" if ok else "open"}; self.capas[capa_id]=c; return {"ok":ok,"capa":c,"side_effects":()}
    def execute_validation(self,protocol_id,validation_type,criteria_passed,deviations=()):
        ok=criteria_passed and not deviations; v={"id":protocol_id,"validation_type":validation_type,"criteria_passed":criteria_passed,"deviations":deviations,"status":"approved" if ok else "failed_or_deviation"}; self.validations[protocol_id]=v; return {"ok":ok,"validation":v,"side_effects":()}
    def record_serialization(self,event_id,batch_id,serial,event_type,sequence):
        duplicate=any(s["serial"]==serial and s["event_type"]!="decommission" for s in self.serials.values()); ctl=evaluate_control("duplicate_serial_rejected",{"duplicate_active_serial":duplicate and event_type=="commission"}); ok=not duplicate or event_type!="commission"; e={"id":event_id,"batch_id":batch_id,"serial":serial,"event_type":event_type,"sequence":sequence,"status":"accepted" if ok and ctl["ok"] else "rejected"}; self.serials[event_id]=e; return {"ok":e["status"]=="accepted","serialization_event":e,"side_effects":()}
    def release_batch(self,release_id,batch_id,tests_passed,labels_reconciled,qa_approval):
        open_devs=tuple(d for d in self.deviations.values() if d["batch_id"]==batch_id and d["status"]!="closed"); serial_ok=any(s["batch_id"]==batch_id and s["status"]=="accepted" for s in self.serials.values()); checklist={"batch_record":bool(self.batches[batch_id]["steps"]),"tests":tests_passed,"deviations":not open_devs,"labels":labels_reconciled,"serialization":serial_ok,"qa":qa_approval}; ctl=evaluate_control("release_requires_complete_quality_checklist",{"checklist":checklist}); r={"id":release_id,"batch_id":batch_id,"checklist":checklist,"status":"released" if ctl["ok"] else "blocked","open_deviations":open_devs}; self.releases[release_id]=r; return {"ok":ctl["ok"],"release":r,"side_effects":()}
    def trace_recall_impact(self,input_lot):
        affected=tuple(bid for bid,b in self.batches.items() if input_lot in b["input_lots"]); serials=tuple(s["serial"] for s in self.serials.values() if s["batch_id"] in affected); return {"ok":True,"input_lot":input_lot,"affected_batches":affected,"serials":serials,"side_effects":()}
    def assistant_pharma_action_preview(self,document,instruction,confirmed=False):
        ctl=evaluate_control("agent_mutations_require_confirmation",{"confirmed":confirmed}); plan=document_instruction_plan(document,instruction); crud=datastore_crud_plan("update",table="pharma_manufacturing_quality_pharma_batch",payload={"instruction":instruction}); return {"ok":plan["ok"] and crud["ok"] and ctl["ok"],"control":ctl,"document_plan":plan,"crud_preview":crud,"requires_confirmation":not confirmed,"side_effects":()}
    def app_contract(self): return {"format":"appgen.pharma-manufacturing-quality.standalone-app.v1","ok":True,"pbc":PBC_KEY,"owned_tables":PHARMA_MANUFACTURING_QUALITY_OWNED_TABLES,"database_backends":PHARMA_MANUFACTURING_QUALITY_ALLOWED_DATABASE_BACKENDS,"event_contract":"AppGen-X","stream_engine_picker_visible":False,"schema":pharma_manufacturing_quality_build_schema_contract(),"services":pharma_manufacturing_quality_build_service_contract(),"routes":pharma_manufacturing_quality_build_api_contract(),"permissions":pharma_manufacturing_quality_permissions_contract(),"ui":pharma_manufacturing_quality_ui_contract(),"workbench":pharma_manufacturing_quality_render_workbench(),"forms":form_catalog(),"wizards":wizard_catalog(),"controls":control_catalog(),"agent":chatbot_interface_contract(),"composed_agent":composed_agent_contribution(),"dsl":{"pbc":PBC_KEY,"skills_namespace":f"{PBC_KEY}_skills","single_pbc_app":True},"side_effects":()}
    def run_demo(self):
        cfg=self.configure(); mbr=self.approve_mbr("MBR1","Tablet","10mg","v1",True,{"temp":(20,30)}); bad_batch=self.start_batch("B0","NO",("LOT1",),{"qualified":True}); batch=self.start_batch("B1","MBR1",("LOT1",),{"qualified":True}); bad_step=self.execute_step("B1","mix","25C",40,20,30,"op","qa"); dev=self.open_deviation("DEV2","B1","process","major","hold","operator error"); capa_bad=self.create_capa("C0","DEV2","fix","prevent",None); capa=self.create_capa("C1","DEV2","fix","prevent","no recurrence"); val_bad=self.execute_validation("V0","process",False); val=self.execute_validation("V1","process",True); ser=self.record_serialization("S1","B1","SER1","commission",1); ser_bad=self.record_serialization("S2","B1","SER1","commission",2); rel_bad=self.release_batch("R0","B1",True,True,True); self.deviations["DEV2"]["status"]="closed"
        for _dev in self.deviations.values():
            if _dev["batch_id"]=="B1": _dev["status"]="closed"
        rel=self.release_batch("R1","B1",True,True,True); recall=self.trace_recall_impact("LOT1"); agent_bad=self.assistant_pharma_action_preview("ebr","update batch",False); agent=self.assistant_pharma_action_preview("ebr","update batch",True)
        checks=(cfg["ok"],mbr["ok"],bad_batch["ok"] is False,batch["ok"],bad_step["ok"] is False,dev["ok"],capa_bad["ok"] is False,capa["ok"],val_bad["ok"] is False,val["ok"],ser["ok"],ser_bad["ok"] is False,rel_bad["ok"] is False,rel["ok"],recall["ok"],agent_bad["ok"] is False,agent["ok"])
        return {"ok":all(checks),"app_contract":self.app_contract(),"side_effects":()}
def single_pbc_app_contract(): return PharmaManufacturingQualityStandaloneApp().app_contract()
def standalone_smoke_test():
    app=PharmaManufacturingQualityStandaloneApp(); demo=app.run_demo(); runtime=pharma_manufacturing_quality_runtime_smoke(); contract=single_pbc_app_contract(); return {"ok":demo["ok"] and runtime["ok"] and contract["ok"] and bool(PHARMA_MANUFACTURING_QUALITY_EMITTED_EVENT_TYPES),"demo":demo,"runtime":runtime,"contract":contract,"side_effects":()}
