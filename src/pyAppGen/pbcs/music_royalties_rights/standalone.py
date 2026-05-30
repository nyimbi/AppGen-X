"""Standalone music royalties and rights application."""
from __future__ import annotations
from dataclasses import dataclass, field
from hashlib import sha256
from typing import Any
from .agent import chatbot_interface_contract, composed_agent_contribution, datastore_crud_plan, document_instruction_plan
from .controls import control_catalog, evaluate_control
from .forms import form_catalog
from .runtime import MUSIC_ROYALTIES_RIGHTS_ALLOWED_DATABASE_BACKENDS, MUSIC_ROYALTIES_RIGHTS_CONSUMED_EVENT_TYPES, MUSIC_ROYALTIES_RIGHTS_EMITTED_EVENT_TYPES, MUSIC_ROYALTIES_RIGHTS_OWNED_TABLES, MUSIC_ROYALTIES_RIGHTS_REQUIRED_EVENT_TOPIC, music_royalties_rights_build_api_contract, music_royalties_rights_build_schema_contract, music_royalties_rights_build_service_contract, music_royalties_rights_configure_runtime, music_royalties_rights_empty_state, music_royalties_rights_permissions_contract, music_royalties_rights_receive_event, music_royalties_rights_register_rule, music_royalties_rights_runtime_smoke, music_royalties_rights_set_parameter
from .ui import music_royalties_rights_render_workbench, music_royalties_rights_ui_contract
from .wizards import wizard_catalog
PBC_KEY="music_royalties_rights"
def _digest(value:Any)->str: return sha256(repr(value).encode("utf-8")).hexdigest()
@dataclass
class MusicRoyaltiesRightsStandaloneApp:
    tenant:str="tenant-music-001"; state:dict=field(default_factory=music_royalties_rights_empty_state)
    works:dict[str,dict]=field(default_factory=dict); recordings:dict[str,dict]=field(default_factory=dict); splits:dict[str,dict]=field(default_factory=dict); licenses:dict[str,dict]=field(default_factory=dict); usage:dict[str,dict]=field(default_factory=dict); statements:dict[str,dict]=field(default_factory=dict); disputes:dict[str,dict]=field(default_factory=dict)
    def configure(self,database_backend="postgresql"):
        cfg=music_royalties_rights_configure_runtime(self.state,{"database_backend":database_backend,"event_topic":MUSIC_ROYALTIES_RIGHTS_REQUIRED_EVENT_TOPIC}); self.state=cfg["state"]
        for n,v in (("duplicate_confidence_review",.85),("recording_match_floor",.8),("minimum_payout",25),("reserve_release_days",180),("statement_close_lag_days",45)):
            r=music_royalties_rights_set_parameter(self.state,n,v); self.state=r["state"]
        for rule in ("duplicate_work_review_required","split_versions_must_balance","recording_work_match_required","license_must_be_active_for_usage","agent_mutations_require_confirmation"):
            r=music_royalties_rights_register_rule(self.state,{"rule_id":rule,"scope":"royalties"}); self.state=r["state"]
        ev=music_royalties_rights_receive_event(self.state,{"event_type":MUSIC_ROYALTIES_RIGHTS_CONSUMED_EVENT_TYPES[0],"idempotency_key":"music-policy-001"}); self.state=ev["state"]
        return {"ok":cfg["ok"] and ev["ok"],"side_effects":()}
    def create_work(self,work_id,title,alternate_titles,contributors,iswc=None,duplicate_confidence=0,reviewed=False):
        ctl=evaluate_control("duplicate_work_review_required",{"duplicate_confidence":duplicate_confidence,"reviewed":reviewed}); ok=bool(title) and bool(contributors) and ctl["ok"]
        w={"id":work_id,"title":title,"alternate_titles":alternate_titles,"contributors":contributors,"iswc":iswc,"duplicate_confidence":duplicate_confidence,"status":"registered" if ok else "review_blocked","blockers":ctl["failures"]}; self.works[work_id]=w; return {"ok":ok,"work":w,"side_effects":()}
    def approve_split(self,split_id,work_id,writer_share,publisher_share,effective_from,reason):
        ctl=evaluate_control("split_versions_must_balance",{"writer_share":writer_share,"publisher_share":publisher_share}); ok=work_id in self.works and ctl["ok"] and bool(reason)
        s={"id":split_id,"work_id":work_id,"writer_share":writer_share,"publisher_share":publisher_share,"effective_from":effective_from,"reason":reason,"status":"approved" if ok else "blocked"}; self.splits[split_id]=s; return {"ok":ok,"split":s,"side_effects":()}
    def register_recording(self,recording_id,isrc,work_id,match_confidence,family="original",neighboring_rights=()):
        ctl=evaluate_control("recording_work_match_required",{"match_confidence":match_confidence}); ok=bool(isrc) and work_id in self.works and ctl["ok"]
        r={"id":recording_id,"isrc":isrc,"work_id":work_id,"match_confidence":match_confidence,"family":family,"neighboring_rights":neighboring_rights,"status":"linked" if ok else "match_review"}; self.recordings[recording_id]=r; return {"ok":ok,"recording":r,"side_effects":()}
    def approve_license(self,license_id,work_id,grant_type,territory,term_start,term_end,fee,active=True):
        ok=work_id in self.works and active and term_start < term_end and grant_type in {"mechanical","performance","sync","master","print","promo"}
        l={"id":license_id,"work_id":work_id,"grant_type":grant_type,"territory":territory,"term_start":term_start,"term_end":term_end,"fee":fee,"active":active,"status":"active" if ok else "blocked"}; self.licenses[license_id]=l; return {"ok":ok,"license":l,"side_effects":()}
    def ingest_usage(self,usage_id,source_type,fingerprint,recording_id,units,revenue,license_id,matched=True):
        lic=self.licenses.get(license_id,{}); ctl=evaluate_control("license_must_be_active_for_usage",{"license_active":lic.get("active")}); ok=recording_id in self.recordings and bool(fingerprint) and ctl["ok"]
        u={"id":usage_id,"source_type":source_type,"fingerprint":fingerprint,"recording_id":recording_id,"units":units,"revenue":revenue,"license_id":license_id,"matched":matched,"status":"normalized" if ok and matched else "unmatched"}; self.usage[usage_id]=u; return {"ok":ok and matched,"usage":u,"side_effects":()}
    def calculate_statement(self,statement_id,period,usage_ids,split_id,beneficiary_complete=True,tax_profile_current=True,advance_balance=0,reserve_percent=0.0):
        split=self.splits[split_id]; gross=sum(self.usage[u]["revenue"] for u in usage_ids); reserve=round(gross*reserve_percent,2); recoup=min(advance_balance,gross-reserve); withholding_ctl=evaluate_control("beneficiary_tax_profile_required",{"beneficiary_complete":beneficiary_complete,"tax_profile_current":tax_profile_current}); unmatched=any(not self.usage[u]["matched"] for u in usage_ids); unmatched_ctl=evaluate_control("unmatched_usage_cannot_be_final_payable",{"unmatched":unmatched,"final_payable":True})
        ok=withholding_ctl["ok"] and unmatched_ctl["ok"] and split["status"]=="approved"; payable=round(max(0,gross-reserve-recoup),2) if ok else 0
        st={"id":statement_id,"period":period,"usage_ids":usage_ids,"split_id":split_id,"gross":gross,"reserve":reserve,"recouped":recoup,"payable":payable,"status":"approved" if ok else "blocked","trace_hash":_digest((usage_ids,split_id,gross,reserve,recoup))}; self.statements[statement_id]=st; return {"ok":ok,"statement":st,"side_effects":()}
    def open_dispute(self,dispute_id,dispute_type,contested_object,evidence):
        ok=dispute_type in {"ownership","split","statement","license","society_conflict"} and bool(evidence); d={"id":dispute_id,"type":dispute_type,"contested_object":contested_object,"evidence":evidence,"status":"under_review" if ok else "incomplete"}; self.disputes[dispute_id]=d; return {"ok":ok,"dispute":d,"side_effects":()}
    def assistant_music_action_preview(self,document,instruction,confirmed=False):
        ctl=evaluate_control("agent_mutations_require_confirmation",{"confirmed":confirmed}); plan=document_instruction_plan(document,instruction); crud=datastore_crud_plan("update",table="music_royalties_rights_musical_work",payload={"instruction":instruction}); return {"ok":plan["ok"] and crud["ok"] and ctl["ok"],"control":ctl,"document_plan":plan,"crud_preview":crud,"requires_confirmation":not confirmed,"side_effects":()}
    def app_contract(self):
        return {"format":"appgen.music-royalties-rights.standalone-app.v1","ok":True,"pbc":PBC_KEY,"owned_tables":MUSIC_ROYALTIES_RIGHTS_OWNED_TABLES,"database_backends":MUSIC_ROYALTIES_RIGHTS_ALLOWED_DATABASE_BACKENDS,"event_contract":"AppGen-X","stream_engine_picker_visible":False,"schema":music_royalties_rights_build_schema_contract(),"services":music_royalties_rights_build_service_contract(),"routes":music_royalties_rights_build_api_contract(),"permissions":music_royalties_rights_permissions_contract(),"ui":music_royalties_rights_ui_contract(),"workbench":music_royalties_rights_render_workbench(),"forms":form_catalog(),"wizards":wizard_catalog(),"controls":control_catalog(),"agent":chatbot_interface_contract(),"composed_agent":composed_agent_contribution(),"dsl":{"pbc":PBC_KEY,"skills_namespace":f"{PBC_KEY}_skills","single_pbc_app":True},"side_effects":()}
    def run_demo(self):
        cfg=self.configure(); bad=self.create_work("W0","Harbor",(),(),duplicate_confidence=.9); work=self.create_work("W1","Harbor",("The Harbor",),("Writer",),"T-1",.9,True); split_bad=self.approve_split("S0","W1",60,60,"2026-01","bad"); split=self.approve_split("S1","W1",50,50,"2026-01","original"); rec_bad=self.register_recording("R0","ISRC", "W1", .5); rec=self.register_recording("R1","ISRC1","W1",.95); lic_bad=self.approve_license("L0","W1","sync","US",10,5,100,True); lic=self.approve_license("L1","W1","sync","US",1,10,1000,True); usage_bad=self.ingest_usage("U0","DSP","fp0","R1",100,50,"L1",False); usage=self.ingest_usage("U1","DSP","fp1","R1",1000,500,"L1",True); stmt_bad=self.calculate_statement("ST0","2026-Q1",("U1",),"S1",False,True); stmt=self.calculate_statement("ST1","2026-Q1",("U1",),"S1",True,True,100,.1); dispute=self.open_dispute("D1","statement","ST1",("email",)); agent_bad=self.assistant_music_action_preview("cue sheet","update splits",False); agent=self.assistant_music_action_preview("cue sheet","update splits",True)
        checks=(cfg["ok"],bad["ok"] is False,work["ok"],split_bad["ok"] is False,split["ok"],rec_bad["ok"] is False,rec["ok"],lic_bad["ok"] is False,lic["ok"],usage_bad["ok"] is False,usage["ok"],stmt_bad["ok"] is False,stmt["ok"],dispute["ok"],agent_bad["ok"] is False,agent["ok"])
        return {"ok":all(checks),"app_contract":self.app_contract(),"side_effects":()}
def single_pbc_app_contract(): return MusicRoyaltiesRightsStandaloneApp().app_contract()
def standalone_smoke_test():
    app=MusicRoyaltiesRightsStandaloneApp(); demo=app.run_demo(); runtime=music_royalties_rights_runtime_smoke(); contract=single_pbc_app_contract(); return {"ok":demo["ok"] and runtime["ok"] and contract["ok"] and bool(MUSIC_ROYALTIES_RIGHTS_EMITTED_EVENT_TYPES),"demo":demo,"runtime":runtime,"contract":contract,"side_effects":()}
