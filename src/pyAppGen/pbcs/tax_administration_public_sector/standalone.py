"""Standalone public sector tax administration application contract."""
from __future__ import annotations
from dataclasses import dataclass, field
from hashlib import sha256
from typing import Any
from .agent import chatbot_interface_contract, composed_agent_contribution, datastore_crud_plan, document_instruction_plan
from .controls import control_catalog, evaluate_control
from .forms import form_catalog
from .runtime import *
from .ui import tax_administration_public_sector_render_workbench, tax_administration_public_sector_ui_contract
from .wizards import wizard_catalog

PBC_KEY = "tax_administration_public_sector"
def _digest(value: Any) -> str: return sha256(repr(value).encode('utf-8')).hexdigest()

@dataclass
class TaxAdministrationPublicSectorStandaloneApp:
    tenant: str = "tenant-tax-001"
    state: dict = field(default_factory=tax_administration_public_sector_empty_state)
    accounts: dict[str, dict] = field(default_factory=dict)
    registrations: dict[str, dict] = field(default_factory=dict)
    obligations: dict[str, dict] = field(default_factory=dict)
    filings: dict[str, dict] = field(default_factory=dict)
    assessments: dict[str, dict] = field(default_factory=dict)
    payments: dict[str, dict] = field(default_factory=dict)
    refunds: dict[str, dict] = field(default_factory=dict)
    notices: dict[str, dict] = field(default_factory=dict)
    audits: dict[str, dict] = field(default_factory=dict)
    appeals: dict[str, dict] = field(default_factory=dict)
    collections: dict[str, dict] = field(default_factory=dict)

    def configure(self, database_backend="postgresql"):
        cfg = tax_administration_public_sector_configure_runtime(self.state, {"database_backend": database_backend, "event_topic": TAX_ADMINISTRATION_PUBLIC_SECTOR_REQUIRED_EVENT_TOPIC}); self.state = cfg["state"]
        for name, value in (("filing_grace_days", 7),("refund_risk_threshold", .7),("collection_approval_threshold", 10000),("assistant_confirmation_required", True)):
            res = tax_administration_public_sector_set_parameter(self.state, name, value); self.state = res["state"]
        for rule_id in ("identity_has_legal_basis","registration_roles_supported","return_period_not_duplicate","assessment_has_statutory_basis","refund_screening_complete","enforcement_prerequisites_clear","agent_mutations_require_confirmation"):
            res = tax_administration_public_sector_register_rule(self.state, {"rule_id": rule_id, "scope":"public_revenue"}); self.state = res["state"]
        inbound = tax_administration_public_sector_receive_event(self.state, {"event_type": TAX_ADMINISTRATION_PUBLIC_SECTOR_CONSUMED_EVENT_TYPES[0], "idempotency_key":"tax-policy-001"}); self.state=inbound["state"]
        return {"ok": cfg["ok"] and inbound["ok"], "side_effects": ()}

    def register_taxpayer_identity(self, account_id, legal_name, legal_form, residency, tin=None, provisional_identifier=None):
        ctl=evaluate_control("identity_has_legal_basis", locals())
        row={"id":account_id,"tenant":self.tenant,"legal_name":legal_name,"legal_form":legal_form,"residency":residency,"tin":tin,"provisional_identifier":provisional_identifier,"status":"identified" if ctl["ok"] else "blocked","blockers":ctl["failures"]}
        self.accounts[account_id]=row; return {"ok":ctl["ok"],"account":row,"side_effects":()}

    def approve_registration_roles(self, registration_id, account_id, roles, start_date="2026-01-01"):
        ctl=evaluate_control("registration_roles_supported", {"roles": roles})
        row={"id":registration_id,"tenant":self.tenant,"account_id":account_id,"roles":tuple(roles),"start_date":start_date,"status":"approved" if ctl["ok"] else "blocked","blockers":ctl["failures"]}
        self.registrations[registration_id]=row; return {"ok":account_id in self.accounts and ctl["ok"],"registration":row,"side_effects":()}

    def derive_filing_obligation(self, obligation_id, account_id, tax_type, period, frequency, due_date=None):
        ctl=evaluate_control("obligation_due_date_valid", locals())
        row={"id":obligation_id,"tenant":self.tenant,"account_id":account_id,"tax_type":tax_type,"period":period,"frequency":frequency,"due_date":due_date,"status":"open" if ctl["ok"] else "incomplete","blockers":ctl["failures"]}
        self.obligations[obligation_id]=row; return {"ok":account_id in self.accounts and ctl["ok"],"obligation":row,"side_effects":()}

    def intake_return(self, filing_id, account_id, period, channel="api", duplicate=False, amendment_reason=None, amount=0):
        ctl=evaluate_control("return_period_not_duplicate", {"duplicate": duplicate, "amendment_reason": amendment_reason})
        row={"id":filing_id,"tenant":self.tenant,"account_id":account_id,"period":period,"channel":channel,"amount":amount,"amendment_reason":amendment_reason,"status":"accepted" if ctl["ok"] else "rejected","blockers":ctl["failures"]}
        self.filings[filing_id]=row; return {"ok":account_id in self.accounts and ctl["ok"],"filing":row,"side_effects":()}

    def raise_assessment(self, assessment_id, account_id, assessment_type, amount, period, statutory_authority=None):
        ctl=evaluate_control("assessment_has_statutory_basis", locals())
        row={"id":assessment_id,"tenant":self.tenant,"account_id":account_id,"assessment_type":assessment_type,"amount":amount,"period":period,"statutory_authority":statutory_authority,"status":"posted" if ctl["ok"] else "blocked","blockers":ctl["failures"]}
        self.assessments[assessment_id]=row; return {"ok":account_id in self.accounts and ctl["ok"],"assessment":row,"side_effects":()}

    def allocate_payment(self, payment_id, account_id, payment_reference, amount, allocation_rule=None, suspense_reason=None):
        ctl=evaluate_control("payment_allocation_explainable", locals())
        row={"id":payment_id,"tenant":self.tenant,"account_id":account_id,"payment_reference":payment_reference,"amount":amount,"allocation_rule":allocation_rule,"suspense_reason":suspense_reason,"status":"allocated" if ctl["ok"] else "suspense","blockers":ctl["failures"]}
        self.payments[payment_id]=row; return {"ok":account_id in self.accounts and ctl["ok"],"payment":row,"side_effects":()}

    def review_refund(self, refund_id, account_id, claim_amount, bank_verified=False, offset_checked=False, risk_reviewed=False, approval_chain=None):
        ctl=evaluate_control("refund_screening_complete", {"bank_verified":bank_verified,"offset_checked":offset_checked,"risk_reviewed":risk_reviewed,"approval_chain":approval_chain})
        row={"id":refund_id,"tenant":self.tenant,"account_id":account_id,"claim_amount":claim_amount,"status":"approved" if ctl["ok"] else "blocked","blockers":ctl["failures"]}
        self.refunds[refund_id]=row; return {"ok":account_id in self.accounts and ctl["ok"],"refund":row,"side_effects":()}

    def serve_notice(self, notice_id, account_id, template_version, statutory_citation, delivery_channel, served_on=None):
        ctl=evaluate_control("notice_service_evidence_present", locals())
        row={"id":notice_id,"tenant":self.tenant,"account_id":account_id,"template_version":template_version,"statutory_citation":statutory_citation,"delivery_channel":delivery_channel,"served_on":served_on,"status":"served" if ctl["ok"] else "service_blocked","blockers":ctl["failures"]}
        self.notices[notice_id]=row; return {"ok":account_id in self.accounts and ctl["ok"],"notice":row,"side_effects":()}

    def open_audit_case(self, audit_id, account_id, trigger, risk_factors, materiality_score, sensitive=False, supervisor_approval=None):
        ctl=evaluate_control("audit_selection_explainable", locals())
        row={"id":audit_id,"tenant":self.tenant,"account_id":account_id,"trigger":trigger,"risk_factors":tuple(risk_factors or ()),"materiality_score":materiality_score,"status":"open" if ctl["ok"] else "blocked","blockers":ctl["failures"]}
        self.audits[audit_id]=row; return {"ok":account_id in self.accounts and ctl["ok"],"audit":row,"side_effects":()}

    def lodge_appeal(self, appeal_id, account_id, challenged_decision, date_served, date_received, grounds, completeness=None):
        ctl=evaluate_control("appeal_timeliness_checked", locals())
        row={"id":appeal_id,"tenant":self.tenant,"account_id":account_id,"challenged_decision":challenged_decision,"date_served":date_served,"date_received":date_received,"grounds":grounds,"completeness":completeness,"stay_collection":ctl["ok"],"status":"accepted" if ctl["ok"] else "deficient","blockers":ctl["failures"]}
        self.appeals[appeal_id]=row; return {"ok":account_id in self.accounts and ctl["ok"],"appeal":row,"side_effects":()}

    def issue_collection_action(self, action_id, account_id, debt_reference, service_evidence=False, appeal_clear=False, approval_threshold_met=False, legal_hold=False):
        ctl=evaluate_control("enforcement_prerequisites_clear", locals())
        row={"id":action_id,"tenant":self.tenant,"account_id":account_id,"debt_reference":debt_reference,"status":"issued" if ctl["ok"] else "blocked","blockers":ctl["failures"]}
        self.collections[action_id]=row; return {"ok":account_id in self.accounts and ctl["ok"],"collection_action":row,"side_effects":()}

    def simulate_debt_treatment(self, account_id, debt_age_days, balance, appeal_active=False):
        stage="hold" if appeal_active else "enforcement" if debt_age_days>120 and balance>10000 else "demand"
        return {"ok":account_id in self.accounts,"mutates_live_records":False,"stage":stage,"evidence_hash":_digest((account_id,debt_age_days,balance,appeal_active)),"side_effects":()}

    def assistant_tax_action_preview(self, document, instruction, confirmed=False):
        ctl=evaluate_control("agent_mutations_require_confirmation", {"confirmed":confirmed})
        doc=document_instruction_plan(document, instruction); crud=datastore_crud_plan("create", table="tax_administration_public_sector_taxpayer_account", payload={"instruction":instruction})
        return {"ok":doc["ok"] and crud["ok"] and ctl["ok"],"document_plan":doc,"crud_preview":crud,"control":ctl,"requires_confirmation":not confirmed,"side_effects":()}

    def app_contract(self):
        return {"format":"appgen.tax-administration-public-sector.standalone-app.v1","ok":True,"pbc":PBC_KEY,"owned_tables":TAX_ADMINISTRATION_PUBLIC_SECTOR_OWNED_TABLES,"database_backends":TAX_ADMINISTRATION_PUBLIC_SECTOR_ALLOWED_DATABASE_BACKENDS,"event_contract":"AppGen-X","stream_engine_picker_visible":False,"schema":tax_administration_public_sector_build_schema_contract(),"services":tax_administration_public_sector_build_service_contract(),"routes":tax_administration_public_sector_build_api_contract(),"permissions":tax_administration_public_sector_permissions_contract(),"ui":tax_administration_public_sector_ui_contract(),"workbench":tax_administration_public_sector_render_workbench(),"forms":form_catalog(),"wizards":wizard_catalog(),"controls":control_catalog(),"agent":chatbot_interface_contract(),"composed_agent":composed_agent_contribution(),"dsl":{"pbc":PBC_KEY,"skills_namespace":f"{PBC_KEY}_skills","single_pbc_app":True},"side_effects":()}

    def run_demo(self):
        cfg=self.configure(); bad_id=self.register_taxpayer_identity("T0","Acme",None,"KE"); acct=self.register_taxpayer_identity("T1","Acme Ltd","company","KE",tin="TIN-1")
        bad_reg=self.approve_registration_roles("R0","T1",()); reg=self.approve_registration_roles("R1","T1",("income_tax","vat"))
        bad_ob=self.derive_filing_obligation("O0","T1","VAT","2026-01","monthly"); ob=self.derive_filing_obligation("O1","T1","VAT","2026-01","monthly","2026-02-20")
        bad_ret=self.intake_return("F0","T1","2026-01",duplicate=True); ret=self.intake_return("F1","T1","2026-01",amount=1000)
        bad_ass=self.raise_assessment("A0","T1","self",1000,"2026-01"); ass=self.raise_assessment("A1","T1","self",1000,"2026-01","VAT Act")
        bad_pay=self.allocate_payment("P0","T1","PAY",1000); pay=self.allocate_payment("P1","T1","PAY",1000,"oldest_debt_first")
        bad_ref=self.review_refund("RF0","T1",100); ref=self.review_refund("RF1","T1",100,True,True,True,("maker","checker"))
        bad_notice=self.serve_notice("N0","T1","v1","VAT Act","portal"); notice=self.serve_notice("N1","T1","v1","VAT Act","portal","2026-03-01")
        bad_audit=self.open_audit_case("AU0","T1","risk",(),50); audit=self.open_audit_case("AU1","T1","risk",("underpayment",),50)
        bad_appeal=self.lodge_appeal("AP0","T1","A1","2026-03-01","2026-03-10","grounds"); appeal=self.lodge_appeal("AP1","T1","A1","2026-03-01","2026-03-10","grounds","complete")
        bad_coll=self.issue_collection_action("C0","T1","A1",True,False,True); coll=self.issue_collection_action("C1","T1","A1",True,True,True)
        scenario=self.simulate_debt_treatment("T1",150,20000); agent_bad=self.assistant_tax_action_preview("return","create",False); agent=self.assistant_tax_action_preview("return","create",True)
        checks=(cfg["ok"], bad_id["ok"] is False, acct["ok"], bad_reg["ok"] is False, reg["ok"], bad_ob["ok"] is False, ob["ok"], bad_ret["ok"] is False, ret["ok"], bad_ass["ok"] is False, ass["ok"], bad_pay["ok"] is False, pay["ok"], bad_ref["ok"] is False, ref["ok"], bad_notice["ok"] is False, notice["ok"], bad_audit["ok"] is False, audit["ok"], bad_appeal["ok"] is False, appeal["ok"], bad_coll["ok"] is False, coll["ok"], scenario["mutates_live_records"] is False, agent_bad["ok"] is False, agent["ok"])
        return {"ok":all(checks),"app_contract":self.app_contract(),"side_effects":()}

def single_pbc_app_contract(): return TaxAdministrationPublicSectorStandaloneApp().app_contract()
def standalone_smoke_test():
    app=TaxAdministrationPublicSectorStandaloneApp(); demo=app.run_demo(); runtime=tax_administration_public_sector_runtime_smoke(); contract=single_pbc_app_contract()
    return {"ok":demo["ok"] and runtime["ok"] and contract["ok"] and bool(TAX_ADMINISTRATION_PUBLIC_SECTOR_EMITTED_EVENT_TYPES),"demo":demo,"runtime":runtime,"contract":contract,"side_effects":()}
