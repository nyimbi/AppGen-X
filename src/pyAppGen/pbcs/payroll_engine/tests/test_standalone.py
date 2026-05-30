"""Standalone and repository smoke tests for payroll_engine."""
from __future__ import annotations
from ..repository import PayrollEngineRepository,payroll_engine_repository_contract
from ..standalone import PayrollEngineStandaloneApp,smoke_test
from ..ui import payroll_engine_standalone_app_contract
def test_standalone_manifest_repository_and_smoke():
 c=payroll_engine_standalone_app_contract(); rc=payroll_engine_repository_contract(); s=smoke_test(); assert c["ok"] is True; assert rc["ok"] is True; assert s["ok"] is True; assert c["forms"]; assert c["wizards"]; assert c["controls"]; assert rc["form_bindings"]
def test_standalone_app_can_execute_gross_to_net_flow():
 app=PayrollEngineStandaloneApp(); loaded=app.load_demo_workspace(tenant="tenant_standalone"); rendered=app.render_workbench(tenant="tenant_standalone"); repo=PayrollEngineRepository(app.state).read_model("tenant_standalone"); binding=PayrollEngineRepository(app.state).form_binding_plan("filing_payment_form"); assert loaded["ok"] is True; assert rendered["ok"] is True; assert rendered["workbench"]["cards"][0]["value"]==1; assert rendered["shell"]["app_id"]=="payroll_engine_one_pbc_app"; assert repo["run"]["posted_count"]==1; assert repo["worker"]["worker_count"]==1; assert repo["payslip"]["payslip_count"]==1; assert repo["deduction_benefit"]["deduction_count"]==1; assert repo["deduction_benefit"]["benefit_count"]==1; assert repo["filing"]["prepared_count"]==1; assert binding["ok"] is True; assert loaded["payment_route"]["route"]=="appgen_outbox"; assert loaded["payroll_proof"]["proof"].startswith("zk_payroll_")
