"""Executable seed-data contract for the time_labor PBC."""
from __future__ import annotations
from .runtime import TIME_LABOR_REQUIRED_EVENT_TOPIC
PBC_KEY="time_labor"
DEFAULT_CONFIGURATION={"database_backend":"postgresql","event_topic":TIME_LABOR_REQUIRED_EVENT_TOPIC,"retry_limit":3,"default_timezone":"UTC","allowed_clock_sources":("mobile","kiosk","badge"),"allowed_absence_types":("vacation","sick","personal"),"workbench_limit":75}
DEFAULT_PARAMETERS={"standard_daily_hours":8,"weekly_overtime_threshold":40,"break_minutes":30,"rounding_interval_minutes":15,"geofence_radius_meters":150,"shift_swap_window_hours":24,"absence_notice_hours":8,"approval_sla_hours":24,"exception_escalation_hours":4,"workbench_limit":75}
DEFAULT_RULE={"rule_id":"time_labor.standard_shift.default","tenant":"tenant_demo","rule_type":"time","eligible_roles":("warehouse_associate","supervisor"),"absence_entitlements":{"vacation":80,"sick":40,"personal":16},"status":"active"}
def demo_workspace_seed_bundle(tenant:str="tenant_demo")->dict:
 employee={"employee_id":f"emp_{tenant}_001","tenant":tenant,"role":"warehouse_associate","status":"active","site":"dc_01","identity":{"did":f"did:appgen:{tenant}:employee","issuer":"trusted_registry","status":"active"}}
 shift={"shift_id":f"shift_{tenant}_001","tenant":tenant,"employee_id":employee["employee_id"],"site":"dc_01","cost_center":"fulfillment","job":"picker","start":"08:00","end":"17:00"}
 clock_in={"event_id":f"clock_{tenant}_in","source":"mobile","kind":"in","time":"08:00","distance_meters":25}
 clock_out={"event_id":f"clock_{tenant}_out","source":"mobile","kind":"out","time":"17:00","distance_meters":20}
 absence={"absence_id":f"abs_{tenant}_001","tenant":tenant,"employee_id":employee["employee_id"],"absence_type":"vacation","hours":8,"period":"2026-W22"}
 projection_events=({"event_id":f"emp_{tenant}_created","event_type":"EmployeeCreated","payload":employee},{"event_id":f"role_{tenant}_changed","event_type":"RoleChanged","payload":{"tenant":tenant,"employee_id":employee["employee_id"],"role":employee["role"]}})
 seed_rows=({"table":"time_labor_employee_projection","rows":({"tenant":tenant,"employee_id":employee["employee_id"],"status":"active"},)},{"table":"time_labor_shift","rows":({"tenant":tenant,"shift_id":shift["shift_id"],"status":"scheduled"},)},{"table":"time_labor_clock_event","rows":({"tenant":tenant,"event_id":clock_in["event_id"],"status":"accepted"},{"tenant":tenant,"event_id":clock_out["event_id"],"status":"accepted"})},{"table":"time_labor_absence","rows":({"tenant":tenant,"absence_id":absence["absence_id"],"status":"recorded"},)},{"table":"time_labor_time_rule","rows":({"tenant":tenant,"record_id":DEFAULT_RULE["rule_id"],"status":"active"},)},{"table":"time_labor_time_parameter","rows":tuple({"tenant":tenant,"record_id":k,"status":"configured"} for k in DEFAULT_PARAMETERS)},{"table":"time_labor_time_configuration","rows":({"tenant":tenant,"record_id":f"cfg_{tenant}","status":"configured"},)})
 return {"tenant":tenant,"configuration":dict(DEFAULT_CONFIGURATION),"parameters":dict(DEFAULT_PARAMETERS),"rule":{**DEFAULT_RULE,"tenant":tenant},"employee":employee,"shift":shift,"clock_events":(clock_in,clock_out),"absence":absence,"projection_events":projection_events,"seed_rows":seed_rows}
SEED_DATA=demo_workspace_seed_bundle()["seed_rows"]
def seed_plan(tenant:str="tenant_demo")->dict:
 b=demo_workspace_seed_bundle(tenant); return {"ok":bool(b["seed_rows"]),"pbc":PBC_KEY,"tables":tuple(dict.fromkeys(x["table"] for x in b["seed_rows"])),"rows":b["seed_rows"],"configuration":b["configuration"],"parameters":b["parameters"],"side_effects":()}
def validate_seed_data(tenant:str="tenant_demo")->dict:
 p=seed_plan(tenant); invalid_tables=tuple(x["table"] for x in p["rows"] if not x.get("table","").startswith(f"{PBC_KEY}_")); invalid_rows=tuple(r for x in p["rows"] for r in x.get("rows",()) if not r.get("tenant") or not any(k in r for k in ("employee_id","shift_id","event_id","absence_id","record_id"))); return {"ok":p["ok"] and not invalid_tables and not invalid_rows,"pbc":PBC_KEY,"plan":p,"invalid_tables":invalid_tables,"invalid_rows":invalid_rows,"side_effects":()}
def smoke_test()->dict:
 b=demo_workspace_seed_bundle(); v=validate_seed_data(); return {"ok":v["ok"] and b["employee"]["role"]=="warehouse_associate","bundle":b,"validation":v,"side_effects":()}
