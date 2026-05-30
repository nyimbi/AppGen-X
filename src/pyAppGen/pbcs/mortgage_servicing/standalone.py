"""Standalone mortgage servicing application."""
from __future__ import annotations
from dataclasses import dataclass, field
from hashlib import sha256
from typing import Any
from .agent import chatbot_interface_contract, composed_agent_contribution, datastore_crud_plan, document_instruction_plan
from .controls import control_catalog, evaluate_control
from .forms import form_catalog
from .runtime import MORTGAGE_SERVICING_ALLOWED_DATABASE_BACKENDS, MORTGAGE_SERVICING_CONSUMED_EVENT_TYPES, MORTGAGE_SERVICING_EMITTED_EVENT_TYPES, MORTGAGE_SERVICING_OWNED_TABLES, MORTGAGE_SERVICING_REQUIRED_EVENT_TOPIC, mortgage_servicing_build_api_contract, mortgage_servicing_build_schema_contract, mortgage_servicing_build_service_contract, mortgage_servicing_configure_runtime, mortgage_servicing_empty_state, mortgage_servicing_permissions_contract, mortgage_servicing_receive_event, mortgage_servicing_register_rule, mortgage_servicing_runtime_smoke, mortgage_servicing_set_parameter
from .ui import mortgage_servicing_render_workbench, mortgage_servicing_ui_contract
from .wizards import wizard_catalog
PBC_KEY="mortgage_servicing"

def _digest(value: Any) -> str: return sha256(repr(value).encode("utf-8")).hexdigest()

@dataclass
class MortgageServicingStandaloneApp:
    tenant:str="tenant-mortgage-001"; state:dict=field(default_factory=mortgage_servicing_empty_state)
    loans:dict[str,dict]=field(default_factory=dict); escrows:dict[str,dict]=field(default_factory=dict); payments:dict[str,dict]=field(default_factory=dict); statements:dict[str,dict]=field(default_factory=dict); loss_cases:dict[str,dict]=field(default_factory=dict); foreclosure:dict[str,dict]=field(default_factory=dict); reports:dict[str,dict]=field(default_factory=dict); exceptions:list[dict]=field(default_factory=list)
    def configure(self, database_backend="postgresql"):
        cfg=mortgage_servicing_configure_runtime(self.state,{"database_backend":database_backend,"event_topic":MORTGAGE_SERVICING_REQUIRED_EVENT_TOPIC}); self.state=cfg["state"]
        for n,v in (("grace_days",15),("suspense_age_limit",30),("escrow_cushion_months",2),("loss_mit_review_days",30),("foreclosure_referral_min_days",120)):
            r=mortgage_servicing_set_parameter(self.state,n,v); self.state=r["state"]
        for rule in ("boarding_requires_complete_terms","payment_waterfall_must_balance","partial_payment_goes_to_suspense","foreclosure_referral_blocks_on_protections","agent_mutations_require_confirmation"):
            r=mortgage_servicing_register_rule(self.state,{"rule_id":rule,"scope":"servicing"}); self.state=r["state"]
        ev=mortgage_servicing_receive_event(self.state,{"event_type":MORTGAGE_SERVICING_CONSUMED_EVENT_TYPES[0],"idempotency_key":"mortgage-policy-001"}); self.state=ev["state"]
        return {"ok":cfg["ok"] and ev["ok"],"side_effects":()}
    def board_loan(self, loan_id, note_terms, due_date, interest_method, escrow_flag, investor, borrower, property_ref):
        facts={"note_terms":note_terms,"due_date":due_date,"interest_method":interest_method,"investor":investor,"borrower":borrower,"property":property_ref}; ctl=evaluate_control("boarding_requires_complete_terms",facts)
        loan={"id":loan_id,"tenant":self.tenant,**facts,"escrow_flag":escrow_flag,"state":"performing" if ctl["ok"] else "boarding_blocked","paid_through_date":due_date,"upb":float(note_terms.get("principal",0)) if isinstance(note_terms,dict) else 0,"blockers":ctl["failures"]}
        self.loans[loan_id]=loan; return {"ok":ctl["ok"],"loan":loan,"side_effects":()}
    def reconcile_transfer(self, loan_id, trial_balance, payment_history_total, escrow_ledger, suspense, open_items):
        variance=round(trial_balance-payment_history_total-escrow_ledger-suspense,2); ctl=evaluate_control("transfer_variance_blocks_statement",{"variance":variance})
        loan=dict(self.loans[loan_id]); loan.update({"transfer_variance":variance,"transfer_open_items":open_items,"first_statement_hold":not ctl["ok"]}); self.loans[loan_id]=loan
        if not ctl["ok"]: self.exceptions.append({"type":"transfer_variance","loan_id":loan_id})
        return {"ok":ctl["ok"],"loan":loan,"side_effects":()}
    def apply_payment(self, payment_id, loan_id, amount, due_amount, source="ach", reversal_of=None):
        if amount < due_amount:
            allocations={"suspense":amount}; applied_to_balance=False
        else:
            allocations={"interest":round(due_amount*.35,2),"escrow":round(due_amount*.2,2),"principal":round(amount-round(due_amount*.55,2),2)}; applied_to_balance=True
        balance=evaluate_control("payment_waterfall_must_balance",{"amount":amount,"allocations":allocations}); partial=evaluate_control("partial_payment_goes_to_suspense",{"amount":amount,"due_amount":due_amount,"applied_to_balance":applied_to_balance})
        ok=balance["ok"] and partial["ok"]; p={"id":payment_id,"loan_id":loan_id,"amount":amount,"due_amount":due_amount,"source":source,"allocations":allocations,"reversal_of":reversal_of,"status":"applied" if ok and applied_to_balance else "suspense" if ok else "blocked"}
        self.payments[payment_id]=p; return {"ok":ok,"payment":p,"side_effects":()}
    def run_escrow_analysis(self, escrow_id, loan_id, tax_projection, insurance_projection, monthly_escrow, status="open"):
        annual=tax_projection+insurance_projection; cushion=round(annual/12*2,2); projected=round(monthly_escrow*12-annual,2); shortage=max(0, cushion-projected); surplus=max(0, projected-cushion); ok=status=="open"
        e={"id":escrow_id,"loan_id":loan_id,"status":status,"annual_disbursement":annual,"cushion":cushion,"projected_balance":projected,"shortage":round(shortage,2),"surplus":round(surplus,2),"analysis_status":"approved" if ok else "blocked"}; self.escrows[escrow_id]=e
        return {"ok":ok,"escrow":e,"side_effects":()}
    def generate_statement(self, statement_id, loan_id, period, due_amount, bankruptcy=False, disclosure_set=("periodic_statement",)):
        loan=self.loans[loan_id]; ok=not loan.get("first_statement_hold") and not bankruptcy and bool(disclosure_set)
        st={"id":statement_id,"loan_id":loan_id,"period":period,"due_amount":due_amount,"disclosure_set":disclosure_set,"status":"generated" if ok else "suppressed","suppression_reason":"bankruptcy_or_transfer_hold" if not ok else None}; self.statements[statement_id]=st
        return {"ok":ok,"statement":st,"side_effects":()}
    def open_loss_mitigation(self, case_id, loan_id, hardship, required_docs, received_docs, investor_rules=("modification","forbearance","deferral")):
        missing=tuple(d for d in required_docs if d not in received_docs); status="complete" if not missing else "incomplete"; options=() if missing else investor_rules
        case={"id":case_id,"loan_id":loan_id,"hardship":hardship,"required_docs":required_docs,"received_docs":received_docs,"missing_docs":missing,"eligible_options":options,"status":status}; self.loss_cases[case_id]=case
        return {"ok":not missing,"case":case,"side_effects":()}
    def evaluate_foreclosure_referral(self, milestone_id, loan_id, delinquency_days, notices_complete, bankruptcy=False, protected_status=False, active_loss_mitigation=False, investor_approval=False):
        ctl=evaluate_control("foreclosure_referral_blocks_on_protections",{"bankruptcy":bankruptcy,"protected_status":protected_status,"active_loss_mitigation":active_loss_mitigation,"notice_gap":not notices_complete})
        ok=delinquency_days>=120 and investor_approval and ctl["ok"]; m={"id":milestone_id,"loan_id":loan_id,"delinquency_days":delinquency_days,"notices_complete":notices_complete,"investor_approval":investor_approval,"status":"referred" if ok else "blocked","blockers":ctl["failures"]}; self.foreclosure[milestone_id]=m
        return {"ok":ok,"milestone":m,"side_effects":()}
    def build_investor_report(self, report_id, pool, loan_ids, scheduled_balance, actual_balance, remittance):
        variance=round(actual_balance-scheduled_balance,2); r={"id":report_id,"pool":pool,"loan_ids":loan_ids,"scheduled_balance":scheduled_balance,"actual_balance":actual_balance,"variance":variance,"remittance":remittance,"status":"ready" if abs(variance)<1 else "exception"}; self.reports[report_id]=r
        return {"ok":r["status"]=="ready","report":r,"side_effects":()}
    def assistant_mortgage_action_preview(self, document, instruction, confirmed=False):
        ctl=evaluate_control("agent_mutations_require_confirmation",{"confirmed":confirmed}); plan=document_instruction_plan(document,instruction); crud=datastore_crud_plan("update",table="mortgage_servicing_mortgage_loan",payload={"instruction":instruction})
        return {"ok":plan["ok"] and crud["ok"] and ctl["ok"],"control":ctl,"document_plan":plan,"crud_preview":crud,"requires_confirmation":not confirmed,"side_effects":()}
    def app_contract(self):
        return {"format":"appgen.mortgage-servicing.standalone-app.v1","ok":True,"pbc":PBC_KEY,"owned_tables":MORTGAGE_SERVICING_OWNED_TABLES,"database_backends":MORTGAGE_SERVICING_ALLOWED_DATABASE_BACKENDS,"event_contract":"AppGen-X","stream_engine_picker_visible":False,"schema":mortgage_servicing_build_schema_contract(),"services":mortgage_servicing_build_service_contract(),"routes":mortgage_servicing_build_api_contract(),"permissions":mortgage_servicing_permissions_contract(),"ui":mortgage_servicing_ui_contract(),"workbench":mortgage_servicing_render_workbench(),"forms":form_catalog(),"wizards":wizard_catalog(),"controls":control_catalog(),"agent":chatbot_interface_contract(),"composed_agent":composed_agent_contribution(),"dsl":{"pbc":PBC_KEY,"skills_namespace":f"{PBC_KEY}_skills","single_pbc_app":True},"side_effects":()}
    def run_demo(self):
        cfg=self.configure(); bad=self.board_loan("L-BAD",{},None,None,False,None,None,None); loan=self.board_loan("L1",{"principal":300000},"2026-06-01","30/360",True,"FNMA","Borrower","Property"); transfer_bad=self.reconcile_transfer("L1",300000,299000,500,0,()); transfer_ok=self.reconcile_transfer("L1",300000,299500,500,0,()); partial=self.apply_payment("P0","L1",500,1800); full=self.apply_payment("P1","L1",1900,1800); escrow=self.run_escrow_analysis("E1","L1",3600,1200,450); stmt=self.generate_statement("S1","L1","2026-06",1800); lm_bad=self.open_loss_mitigation("LM0","L1","hardship",("paystub","bank"),("paystub",)); lm=self.open_loss_mitigation("LM1","L1","hardship",("paystub",),("paystub",)); fc_bad=self.evaluate_foreclosure_referral("F0","L1",130,True,active_loss_mitigation=True,investor_approval=True); fc=self.evaluate_foreclosure_referral("F1","L1",130,True,investor_approval=True); report_bad=self.build_investor_report("R0","POOL",("L1",),300000,299000,1000); report=self.build_investor_report("R1","POOL",("L1",),300000,300000,1000); agent_bad=self.assistant_mortgage_action_preview("doc","update hardship",False); agent=self.assistant_mortgage_action_preview("doc","update hardship",True)
        checks=(cfg["ok"],bad["ok"] is False,loan["ok"],transfer_bad["ok"] is False,transfer_ok["ok"],partial["payment"]["status"]=="suspense",full["ok"],escrow["ok"],stmt["ok"],lm_bad["ok"] is False,lm["ok"],fc_bad["ok"] is False,fc["ok"],report_bad["ok"] is False,report["ok"],agent_bad["ok"] is False,agent["ok"])
        return {"ok":all(checks),"app_contract":self.app_contract(),"agent":agent,"side_effects":()}

def single_pbc_app_contract(): return MortgageServicingStandaloneApp().app_contract()
def standalone_smoke_test():
    app=MortgageServicingStandaloneApp(); demo=app.run_demo(); runtime=mortgage_servicing_runtime_smoke(); contract=single_pbc_app_contract(); return {"ok":demo["ok"] and runtime["ok"] and contract["ok"] and bool(MORTGAGE_SERVICING_EMITTED_EVENT_TYPES),"demo":demo,"runtime":runtime,"contract":contract,"side_effects":()}
