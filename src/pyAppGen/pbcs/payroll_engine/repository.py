"""Repository and read-model contract for the standalone payroll_engine package."""
from __future__ import annotations
from .runtime import PAYROLL_ENGINE_ALLOWED_DATABASE_BACKENDS,PAYROLL_ENGINE_OWNED_TABLES,PAYROLL_ENGINE_REQUIRED_EVENT_TOPIC,payroll_engine_build_workbench_view
FORM_BINDINGS=({"form":"payroll_run_form","owned_table":"payroll_run","repository_method":"run_console","writes":("payroll_run","payroll_run_worker","payroll_run_approval")},{"form":"worker_pay_profile_form","owned_table":"worker_pay_profile","repository_method":"worker_console","writes":("worker_projection","worker_pay_profile","worker_bank_instruction")},{"form":"payslip_calculation_form","owned_table":"payslip","repository_method":"payslip_console","writes":("payslip","payslip_line","gross_pay_component")},{"form":"deduction_benefit_form","owned_table":"deduction","repository_method":"deduction_benefit_console","writes":("deduction","benefit_allocation","employer_contribution")},{"form":"filing_payment_form","owned_table":"payroll_filing","repository_method":"filing_console","writes":("payroll_filing","payment_instruction","journal_request_projection")},{"form":"payroll_governance_form","owned_table":"payroll_rule","repository_method":"governance_console","writes":("payroll_rule","payroll_parameter","payroll_configuration","payroll_schema_extension")})
READ_MODELS=({"key":"run","repository_method":"run_console"},{"key":"worker","repository_method":"worker_console"},{"key":"payslip","repository_method":"payslip_console"},{"key":"deduction_benefit","repository_method":"deduction_benefit_console"},{"key":"filing","repository_method":"filing_console"},{"key":"governance","repository_method":"governance_console"})
def payroll_engine_repository_contract()->dict:
 return {"format":"appgen.payroll-engine-repository-contract.v1","ok":bool(FORM_BINDINGS) and bool(READ_MODELS),"pbc":"payroll_engine","database_backends":PAYROLL_ENGINE_ALLOWED_DATABASE_BACKENDS,"required_event_topic":PAYROLL_ENGINE_REQUIRED_EVENT_TOPIC,"owned_tables":PAYROLL_ENGINE_OWNED_TABLES,"form_bindings":FORM_BINDINGS,"read_models":READ_MODELS,"shared_table_access":False,"side_effects":()}
class PayrollEngineRepository:
 def __init__(self,state:dict): self.state=state
 def run_console(self,tenant:str)->dict:
  runs=tuple(x for x in self.state.get("payroll_runs",{}).values() if x.get("tenant")==tenant); return {"run_count":len(runs),"posted_count":len(tuple(x for x in runs if x.get("status")=="posted")),"runs":runs}
 def worker_console(self,tenant:str)->dict:
  workers=tuple(x for x in self.state.get("workers",{}).values() if x.get("tenant")==tenant); return {"worker_count":len(workers),"workers":workers}
 def payslip_console(self,tenant:str)->dict:
  payslips=tuple(x for x in self.state.get("payslips",{}).values() if x.get("tenant")==tenant); return {"payslip_count":len(payslips),"gross_pay_total":round(sum(x.get("gross_pay",0) for x in payslips),2),"net_pay_total":round(sum(x.get("net_pay",0) for x in payslips),2),"payslips":payslips}
 def deduction_benefit_console(self,tenant:str)->dict:
  deductions=tuple(x for x in self.state.get("deductions",{}).values() if x.get("tenant")==tenant); benefits=tuple(x for x in self.state.get("benefit_allocations",{}).values() if x.get("tenant")==tenant); return {"deduction_count":len(deductions),"benefit_count":len(benefits),"deductions":deductions,"benefits":benefits}
 def filing_console(self,tenant:str)->dict:
  filings=tuple(x for x in self.state.get("filings",{}).values() if x.get("tenant")==tenant); return {"filing_count":len(filings),"prepared_count":len(tuple(x for x in filings if x.get("status")=="prepared")),"filings":filings}
 def governance_console(self,tenant:str)->dict:
  return {"tenant":tenant,"rule_count":len(self.state.get("rules",{})),"parameter_count":len(self.state.get("parameters",{})),"configuration_bound":bool(self.state.get("configuration",{}).get("ok")),"inbox_count":len(self.state.get("inbox",())),"outbox_count":len(self.state.get("outbox",())),"dead_letter_count":len(self.state.get("dead_letter",()))}
 def form_binding_plan(self,form_key:str)->dict:
  binding=next((x for x in FORM_BINDINGS if x["form"]==form_key),None); return {"ok":binding is not None,"form":form_key,"binding":binding,"database_backends":PAYROLL_ENGINE_ALLOWED_DATABASE_BACKENDS,"event_contract":"AppGen-X","side_effects":()}
 def read_model(self,tenant:str)->dict:
  return {"ok":True,"tenant":tenant,"run":self.run_console(tenant),"worker":self.worker_console(tenant),"payslip":self.payslip_console(tenant),"deduction_benefit":self.deduction_benefit_console(tenant),"filing":self.filing_console(tenant),"governance":self.governance_console(tenant),"workbench":payroll_engine_build_workbench_view(self.state,tenant=tenant),"side_effects":()}
repository_contract=payroll_engine_repository_contract
def smoke_test()->dict:
 state={"payroll_runs":{"r":{"tenant":"tenant_demo","status":"posted"}},"workers":{"e":{"tenant":"tenant_demo"}},"payslips":{"p":{"tenant":"tenant_demo","gross_pay":1000,"net_pay":750}},"deductions":{},"benefit_allocations":{},"filings":{},"rules":{},"parameters":{},"configuration":{"ok":True},"inbox":(),"outbox":(),"dead_letter":()}; repo=PayrollEngineRepository(state); rm=repo.read_model("tenant_demo"); binding=repo.form_binding_plan("payslip_calculation_form"); contract=payroll_engine_repository_contract(); return {"ok":contract["ok"] and rm["run"]["posted_count"]==1 and rm["payslip"]["net_pay_total"]==750 and binding["ok"],"contract":contract,"read_model":rm,"binding":binding,"side_effects":()}
