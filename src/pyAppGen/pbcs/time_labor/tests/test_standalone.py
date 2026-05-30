"""Standalone and repository smoke tests for time_labor."""
from __future__ import annotations
from ..repository import TimeLaborRepository,time_labor_repository_contract
from ..standalone import TimeLaborStandaloneApp,smoke_test
from ..ui import time_labor_standalone_app_contract
def test_standalone_manifest_repository_and_smoke():
 c=time_labor_standalone_app_contract(); rc=time_labor_repository_contract(); s=smoke_test(); assert c["ok"] is True; assert rc["ok"] is True; assert s["ok"] is True; assert c["forms"]; assert c["wizards"]; assert c["controls"]; assert rc["form_bindings"]
def test_standalone_app_can_execute_shift_to_approved_hours_flow():
 app=TimeLaborStandaloneApp(); loaded=app.load_demo_workspace(tenant="tenant_standalone"); rendered=app.render_workbench(tenant="tenant_standalone"); repo=TimeLaborRepository(app.state).read_model("tenant_standalone"); binding=TimeLaborRepository(app.state).form_binding_plan("labor_approval_form"); assert loaded["ok"] is True; assert rendered["ok"] is True; assert rendered["workbench"]["cards"][0]["value"]==1; assert rendered["shell"]["app_id"]=="time_labor_one_pbc_app"; assert repo["schedule"]["shift_count"]==1; assert repo["clock"]["clock_event_count"]==2; assert repo["time_entry"]["hours"]==8.5; assert repo["absence"]["absence_count"]==1; assert repo["approval"]["approved_count"]==1; assert binding["ok"] is True; assert loaded["clock_route"]["route"]=="appgen_outbox"; assert loaded["hours_proof"]["proof"].startswith("zk_hours_")
