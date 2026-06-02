"""Executable seed-data contract for the payroll_engine PBC."""
from __future__ import annotations
from .runtime import PAYROLL_ENGINE_REQUIRED_EVENT_TOPIC
PBC_KEY="payroll_engine"
DEFAULT_CONFIGURATION={"database_backend":"postgresql","event_topic":PAYROLL_ENGINE_REQUIRED_EVENT_TOPIC,"retry_limit":3,"default_currency":"USD","allowed_countries":("US","CA"),"allowed_filing_channels":("eftps","state_api"),"workbench_limit":75}
DEFAULT_PARAMETERS={"standard_period_hours":40,"overtime_multiplier":1.5,"supplemental_rate":0.22,"rounding_precision":2,"net_pay_floor":0,"filing_materiality_threshold":100,"approval_amount_threshold":10000,"off_cycle_approval_threshold":5000,"retro_lookback_periods":6,"workbench_limit":75}
DEFAULT_RULE={"rule_id":"payroll_engine.us.biweekly","tenant":"tenant_demo","rule_type":"pay","eligible_worker_types":("employee",),"allowed_countries":("US",),"deduction_limit_percent":0.5,"benefit_classes":("medical","retirement"),"status":"active"}
def demo_workspace_seed_bundle(tenant:str="tenant_demo")->dict:
 worker={"employee_id":f"emp_{tenant}_001","tenant":tenant,"worker_type":"employee","country":"US","salary_per_period":0,"hourly_rate":40,"currency":"USD","identity":{"did":f"did:appgen:{tenant}:worker","issuer":"trusted_registry","status":"active"}}
 run={"run_id":f"run_{tenant}_2026w22","tenant":tenant,"period":"2026-W22","country":"US","legal_entity":"entity_us","pay_group":"biweekly"}
 labor={"labor_event_id":f"labor_{tenant}_001","tenant":tenant,"employee_id":worker["employee_id"],"period":run["period"],"approved_hours":45,"overtime_hours":5}
 deduction={"deduction_id":f"ded_{tenant}_001","deduction_type":"retirement","amount":120}
 benefit={"benefit_id":f"ben_{tenant}_001","benefit_type":"medical","employee_amount":80,"employer_amount":240}
 seed_rows=({"table":"payroll_engine_worker_projection","rows":({"tenant":tenant,"employee_id":worker["employee_id"],"status":"active"},)},{"table":"payroll_engine_payroll_run","rows":({"tenant":tenant,"run_id":run["run_id"],"status":"posted"},)},{"table":"payroll_engine_labor_hours","rows":({"tenant":tenant,"labor_event_id":labor["labor_event_id"],"employee_id":worker["employee_id"]},)},{"table":"payroll_engine_payslip","rows":({"tenant":tenant,"payslip_id":f"payslip_{run['run_id']}_{worker['employee_id']}","status":"calculated"},)},{"table":"payroll_engine_payroll_rule","rows":({"tenant":tenant,"record_id":DEFAULT_RULE["rule_id"],"status":"active"},)},{"table":"payroll_engine_payroll_parameter","rows":tuple({"tenant":tenant,"record_id":k,"status":"configured"} for k in DEFAULT_PARAMETERS)},{"table":"payroll_engine_payroll_configuration","rows":({"tenant":tenant,"record_id":f"cfg_{tenant}","status":"configured"},)})
 return {"tenant":tenant,"configuration":dict(DEFAULT_CONFIGURATION),"parameters":dict(DEFAULT_PARAMETERS),"rule":{**DEFAULT_RULE,"tenant":tenant},"worker":worker,"run":run,"labor":labor,"deduction":deduction,"benefit":benefit,"seed_rows":seed_rows}
SEED_DATA=demo_workspace_seed_bundle()["seed_rows"]
def seed_plan(tenant:str="tenant_demo")->dict:
 bundle=demo_workspace_seed_bundle(tenant); return {"ok":bool(bundle["seed_rows"]),"pbc":PBC_KEY,"tables":tuple(dict.fromkeys(x["table"] for x in bundle["seed_rows"])),"rows":bundle["seed_rows"],"configuration":bundle["configuration"],"parameters":bundle["parameters"],"side_effects":()}
def validate_seed_data(tenant:str="tenant_demo")->dict:
 p=seed_plan(tenant); invalid_tables=tuple(x["table"] for x in p["rows"] if not x.get("table","").startswith(f"{PBC_KEY}_")); invalid_rows=tuple(r for x in p["rows"] for r in x.get("rows",()) if not r.get("tenant") or not any(k in r for k in ("employee_id","run_id","labor_event_id","payslip_id","record_id"))); return {"ok":p["ok"] and not invalid_tables and not invalid_rows,"pbc":PBC_KEY,"plan":p,"invalid_tables":invalid_tables,"invalid_rows":invalid_rows,"side_effects":()}
def smoke_test()->dict:
 b=demo_workspace_seed_bundle(); v=validate_seed_data(); return {"ok":v["ok"] and b["worker"]["country"]=="US","bundle":b,"validation":v,"side_effects":()}
