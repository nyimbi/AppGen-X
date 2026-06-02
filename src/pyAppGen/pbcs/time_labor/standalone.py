"""Standalone one-PBC application surface for time_labor."""
from __future__ import annotations
from . import repository,routes,ui
from .runtime import time_labor_approve_labor_summary,time_labor_calculate_time_entry,time_labor_configure_runtime,time_labor_create_shift,time_labor_empty_state,time_labor_generate_hours_proof,time_labor_receive_event,time_labor_record_absence,time_labor_record_clock_event,time_labor_register_rule,time_labor_register_schema_extension,time_labor_route_clock_source,time_labor_run_control_tests,time_labor_screen_policy,time_labor_set_parameter
from .seed_data import demo_workspace_seed_bundle
def standalone_app_manifest()->dict:
 return {"ok":True,"pbc":"time_labor","app":ui.time_labor_standalone_app_contract(),"routes":routes.api_route_contracts()["routes"],"repository":repository.time_labor_repository_contract(),"side_effects":()}
class TimeLaborStandaloneApp:
 def __init__(self,state:dict|None=None): self.state=state or time_labor_empty_state(); self.repository=repository.TimeLaborRepository(self.state)
 def _commit(self,result:dict)->dict:
  if result.get("state") is not None: self.state=result["state"]; self.repository.state=self.state
  return result
 def bootstrap(self,*,tenant:str="tenant_demo")->dict:
  b=demo_workspace_seed_bundle(tenant); self._commit(time_labor_configure_runtime(self.state,b["configuration"]));
  for n,v in b["parameters"].items(): self._commit(time_labor_set_parameter(self.state,n,v))
  self._commit(time_labor_register_rule(self.state,b["rule"])); self._commit(time_labor_register_schema_extension(self.state,"shift",{"fatigue_payload":"jsonb","geofence_payload":"jsonb"}))
  for e in b["projection_events"]: self._commit(time_labor_receive_event(self.state,e))
  return {"ok":True,"tenant":tenant,"state":self.state,"repository":self.repository.read_model(tenant),"side_effects":()}
 def load_demo_workspace(self,*,tenant:str="tenant_demo")->dict:
  b=demo_workspace_seed_bundle(tenant); self.bootstrap(tenant=tenant); shift=self._commit(time_labor_create_shift(self.state,b["shift"]));
  for event in b["clock_events"]: self._commit(time_labor_record_clock_event(self.state,shift["shift"]["shift_id"],event))
  entry=self._commit(time_labor_calculate_time_entry(self.state,shift["shift"]["shift_id"])); absence=self._commit(time_labor_record_absence(self.state,b["absence"])); summary=self._commit(time_labor_approve_labor_summary(self.state,f"summary_{tenant}_001",employee_id=b["employee"]["employee_id"],period="2026-W22",approved_by="manager.demo"))
  policy=time_labor_screen_policy(self.state,shift["shift"]["shift_id"],restricted_sites=("blocked_site",)); route=time_labor_route_clock_source(b["clock_events"][0],rails=({"route":"kiosk_api","available":False,"latency":1},{"route":"appgen_outbox","available":True,"latency":3})); proof=time_labor_generate_hours_proof(self.state,summary["summary"]["summary_id"],disclosure=("summary_id","employee_id","approved_hours","overtime_hours")); controls=time_labor_run_control_tests(self.state)
  return {"ok":controls["ok"] and policy["ok"] and route["ok"] and proof["ok"] and entry["ok"] and absence["ok"],"tenant":tenant,"workbench":self.render_workbench(tenant=tenant),"repository":self.repository.read_model(tenant),"policy":policy,"clock_route":route,"hours_proof":proof,"controls":controls,"side_effects":()}
 def render_workbench(self,*,tenant:str,principal_permissions:tuple[str,...]|None=None)->dict:
  permissions=principal_permissions or tuple(sorted(set(ui.time_labor_ui_contract()["action_permissions"].values()))); return ui.time_labor_render_standalone_app(self.state,tenant=tenant,principal_permissions=permissions)
 def release_snapshot(self)->dict:
  from . import release_evidence
  return release_evidence.build_release_evidence()
def smoke_test()->dict:
 app=TimeLaborStandaloneApp(); loaded=app.load_demo_workspace(); rendered=app.render_workbench(tenant="tenant_demo"); release=app.release_snapshot(); return {"ok":loaded["ok"] and rendered["ok"] and rendered["workbench"]["cards"][0]["value"]>=1 and release["ok"],"manifest":standalone_app_manifest(),"loaded":loaded,"rendered":rendered,"release_snapshot":release,"side_effects":()}
def workbench_smoke_test()->dict:
 app=TimeLaborStandaloneApp(); loaded=app.load_demo_workspace(); rendered=app.render_workbench(tenant="tenant_demo"); return {"ok":loaded["ok"] and rendered["ok"] and rendered["workbench"]["cards"][0]["value"]>=1,"manifest":standalone_app_manifest(),"loaded":loaded,"rendered":rendered,"side_effects":()}
