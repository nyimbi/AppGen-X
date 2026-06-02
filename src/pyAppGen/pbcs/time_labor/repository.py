"""Repository and read-model contract for the standalone time_labor package."""
from __future__ import annotations
from .runtime import TIME_LABOR_ALLOWED_DATABASE_BACKENDS,TIME_LABOR_OWNED_TABLES,TIME_LABOR_REQUIRED_EVENT_TOPIC,time_labor_build_workbench_view
FORM_BINDINGS=(
 {"form":"shift_planning_form","owned_table":"shift","repository_method":"schedule_console","writes":("shift","shift_assignment","schedule_bid")},
 {"form":"clock_event_form","owned_table":"clock_event","repository_method":"clock_console","writes":("clock_event","clock_exception","clock_source_route")},
 {"form":"time_entry_calculation_form","owned_table":"time_entry","repository_method":"time_entry_console","writes":("time_entry","time_entry_line","overtime_bucket","premium_calculation")},
 {"form":"absence_request_form","owned_table":"absence","repository_method":"absence_console","writes":("absence","absence_balance","absence_approval")},
 {"form":"labor_approval_form","owned_table":"labor_summary","repository_method":"approval_console","writes":("labor_summary","labor_summary_line","approval_task")},
 {"form":"time_governance_form","owned_table":"time_rule","repository_method":"governance_console","writes":("time_rule","time_parameter","time_configuration","time_schema_extension")},
)
READ_MODELS=({"key":"schedule","repository_method":"schedule_console"},{"key":"clock","repository_method":"clock_console"},{"key":"time_entry","repository_method":"time_entry_console"},{"key":"absence","repository_method":"absence_console"},{"key":"approval","repository_method":"approval_console"},{"key":"governance","repository_method":"governance_console"})
def time_labor_repository_contract()->dict:
 return {"format":"appgen.time-labor-repository-contract.v1","ok":bool(FORM_BINDINGS) and bool(READ_MODELS),"pbc":"time_labor","database_backends":TIME_LABOR_ALLOWED_DATABASE_BACKENDS,"required_event_topic":TIME_LABOR_REQUIRED_EVENT_TOPIC,"owned_tables":TIME_LABOR_OWNED_TABLES,"form_bindings":FORM_BINDINGS,"read_models":READ_MODELS,"shared_table_access":False,"side_effects":()}
class TimeLaborRepository:
 def __init__(self,state:dict): self.state=state
 def schedule_console(self,tenant:str)->dict:
  shifts=tuple(x for x in self.state.get("shifts",{}).values() if x.get("tenant")==tenant); return {"shift_count":len(shifts),"scheduled_count":len(tuple(x for x in shifts if x.get("status")=="scheduled")),"shifts":shifts}
 def clock_console(self,tenant:str)->dict:
  events=tuple(x for x in self.state.get("clock_events",{}).values() if x.get("tenant")==tenant); return {"clock_event_count":len(events),"exception_count":len(tuple(x for x in events if x.get("status")=="exception")),"clock_events":events}
 def time_entry_console(self,tenant:str)->dict:
  entries=tuple(x for x in self.state.get("time_entries",{}).values() if x.get("tenant")==tenant); return {"entry_count":len(entries),"hours":round(sum(x.get("hours",0) for x in entries),2),"overtime_hours":round(sum(x.get("overtime_hours",0) for x in entries),2),"entries":entries}
 def absence_console(self,tenant:str)->dict:
  absences=tuple(x for x in self.state.get("absences",{}).values() if x.get("tenant")==tenant); return {"absence_count":len(absences),"absence_hours":round(sum(x.get("hours",0) for x in absences),2),"absences":absences}
 def approval_console(self,tenant:str)->dict:
  summaries=tuple(x for x in self.state.get("summaries",{}).values() if x.get("tenant")==tenant); return {"summary_count":len(summaries),"approved_count":len(tuple(x for x in summaries if x.get("status")=="approved")),"approved_hours":round(sum(x.get("approved_hours",0) for x in summaries),2),"summaries":summaries}
 def governance_console(self,tenant:str)->dict:
  return {"tenant":tenant,"rule_count":len(self.state.get("rules",{})),"parameter_count":len(self.state.get("parameters",{})),"configuration_bound":bool(self.state.get("configuration",{}).get("ok")),"inbox_count":len(self.state.get("inbox",())),"outbox_count":len(self.state.get("outbox",())),"dead_letter_count":len(self.state.get("dead_letter",()))}
 def form_binding_plan(self,form_key:str)->dict:
  binding=next((x for x in FORM_BINDINGS if x["form"]==form_key),None); return {"ok":binding is not None,"form":form_key,"binding":binding,"database_backends":TIME_LABOR_ALLOWED_DATABASE_BACKENDS,"event_contract":"AppGen-X","side_effects":()}
 def read_model(self,tenant:str)->dict:
  return {"ok":True,"tenant":tenant,"schedule":self.schedule_console(tenant),"clock":self.clock_console(tenant),"time_entry":self.time_entry_console(tenant),"absence":self.absence_console(tenant),"approval":self.approval_console(tenant),"governance":self.governance_console(tenant),"workbench":time_labor_build_workbench_view(self.state,tenant=tenant),"side_effects":()}
repository_contract=time_labor_repository_contract
def smoke_test()->dict:
 state={"shifts":{"s":{"tenant":"tenant_demo","shift_id":"s","status":"scheduled"}},"clock_events":{},"time_entries":{"e":{"tenant":"tenant_demo","hours":8,"overtime_hours":0}},"absences":{},"summaries":{},"rules":{},"parameters":{},"configuration":{"ok":True},"inbox":(),"outbox":(),"dead_letter":()}; repo=TimeLaborRepository(state); rm=repo.read_model("tenant_demo"); binding=repo.form_binding_plan("shift_planning_form"); contract=time_labor_repository_contract(); return {"ok":contract["ok"] and rm["schedule"]["shift_count"]==1 and rm["time_entry"]["hours"]==8 and binding["ok"],"contract":contract,"read_model":rm,"binding":binding,"side_effects":()}
