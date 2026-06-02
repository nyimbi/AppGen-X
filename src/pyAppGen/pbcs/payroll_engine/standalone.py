"""Standalone one-PBC application surface for payroll_engine."""
from __future__ import annotations
from . import repository,routes,ui
from .runtime import payroll_engine_allocate_benefit,payroll_engine_apply_deduction,payroll_engine_calculate_payslip,payroll_engine_configure_runtime,payroll_engine_create_payroll_run,payroll_engine_empty_state,payroll_engine_generate_payroll_proof,payroll_engine_ingest_labor_hours,payroll_engine_post_payroll_run,payroll_engine_prepare_payroll_filing,payroll_engine_register_rule,payroll_engine_register_schema_extension,payroll_engine_route_payment_or_filing,payroll_engine_run_control_tests,payroll_engine_screen_policy,payroll_engine_set_parameter,payroll_engine_upsert_worker_projection
from .seed_data import demo_workspace_seed_bundle
def standalone_app_manifest()->dict:
 return {"ok":True,"pbc":"payroll_engine","app":ui.payroll_engine_standalone_app_contract(),"routes":routes.api_route_contracts()["routes"],"repository":repository.payroll_engine_repository_contract(),"side_effects":()}
class PayrollEngineStandaloneApp:
 def __init__(self,state:dict|None=None): self.state=state or payroll_engine_empty_state(); self.repository=repository.PayrollEngineRepository(self.state)
 def _commit(self,result:dict)->dict:
  if result.get("state") is not None: self.state=result["state"]; self.repository.state=self.state
  return result
 def bootstrap(self,*,tenant:str="tenant_demo")->dict:
  b=demo_workspace_seed_bundle(tenant); self._commit(payroll_engine_configure_runtime(self.state,b["configuration"]));
  for n,v in b["parameters"].items(): self._commit(payroll_engine_set_parameter(self.state,n,v))
  self._commit(payroll_engine_register_rule(self.state,b["rule"])); self._commit(payroll_engine_register_schema_extension(self.state,"payslip",{"proof_payload":"jsonb","retro_payload":"jsonb"})); self._commit(payroll_engine_upsert_worker_projection(self.state,b["worker"])); return {"ok":True,"tenant":tenant,"state":self.state,"repository":self.repository.read_model(tenant),"side_effects":()}
 def load_demo_workspace(self,*,tenant:str="tenant_demo")->dict:
  b=demo_workspace_seed_bundle(tenant); self.bootstrap(tenant=tenant); run=self._commit(payroll_engine_create_payroll_run(self.state,b["run"])); self._commit(payroll_engine_ingest_labor_hours(self.state,b["labor"])); payslip=self._commit(payroll_engine_calculate_payslip(self.state,run["payroll_run"]["run_id"],b["worker"]["employee_id"])); self._commit(payroll_engine_apply_deduction(self.state,payslip["payslip_id"],b["deduction"])); self._commit(payroll_engine_allocate_benefit(self.state,payslip["payslip_id"],b["benefit"])); posted=self._commit(payroll_engine_post_payroll_run(self.state,run["payroll_run"]["run_id"],approved_by="payroll.manager")); filing=self._commit(payroll_engine_prepare_payroll_filing(self.state,f"filing_{tenant}_001",run_id=posted["payroll_run"]["run_id"],jurisdiction="US-FED",channel="eftps")); policy=payroll_engine_screen_policy(self.state,posted["payroll_run"]["run_id"],restricted_countries=("restricted",)); route=payroll_engine_route_payment_or_filing({"event_id":f"pay_{tenant}_001"},rails=({"route":"bank_api","available":False,"latency":1},{"route":"appgen_outbox","available":True,"latency":3})); proof=payroll_engine_generate_payroll_proof(self.state,payslip["payslip_id"],disclosure=("payslip_id","employee_id","gross_pay","net_pay")); controls=payroll_engine_run_control_tests(self.state); return {"ok":controls["ok"] and policy["ok"] and route["ok"] and proof["ok"] and filing["ok"],"tenant":tenant,"workbench":self.render_workbench(tenant=tenant),"repository":self.repository.read_model(tenant),"policy":policy,"payment_route":route,"payroll_proof":proof,"controls":controls,"side_effects":()}
 def render_workbench(self,*,tenant:str,principal_permissions:tuple[str,...]|None=None)->dict:
  permissions=principal_permissions or tuple(sorted(set(ui.payroll_engine_ui_contract()["action_permissions"].values()))); return ui.payroll_engine_render_standalone_app(self.state,tenant=tenant,principal_permissions=permissions)
 def release_snapshot(self)->dict:
  from . import release_evidence
  return release_evidence.build_release_evidence()
def smoke_test()->dict:
 app=PayrollEngineStandaloneApp(); loaded=app.load_demo_workspace(); rendered=app.render_workbench(tenant="tenant_demo"); release=app.release_snapshot(); return {"ok":loaded["ok"] and rendered["ok"] and rendered["workbench"]["cards"][0]["value"]>=1 and release["ok"],"manifest":standalone_app_manifest(),"loaded":loaded,"rendered":rendered,"release_snapshot":release,"side_effects":()}
def workbench_smoke_test()->dict:
 app=PayrollEngineStandaloneApp(); loaded=app.load_demo_workspace(); rendered=app.render_workbench(tenant="tenant_demo"); return {"ok":loaded["ok"] and rendered["ok"] and rendered["workbench"]["cards"][0]["value"]>=1,"manifest":standalone_app_manifest(),"loaded":loaded,"rendered":rendered,"side_effects":()}
