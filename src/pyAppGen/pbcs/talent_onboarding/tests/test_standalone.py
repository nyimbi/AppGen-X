"""Focused standalone one-PBC tests for talent_onboarding."""
from pathlib import Path
from .. import agent, release_evidence, routes, services, standalone, ui
from ..repository import TalentOnboardingStandaloneRepository

def test_repository_persists_seeded_talent_workspace():
    repo=TalentOnboardingStandaloneRepository()
    try:
        seeded=repo.seed_demo_workspace(); workbench=repo.build_workbench('tenant_demo'); read_model=repo.read_model('tenant_demo'); proof=repo.generate_candidate_proof('tenant_demo','cand_demo_100',('candidate_id','requisition_id','stage'))
        assert seeded['ok'] is True; assert workbench['ok'] is True; assert read_model['ok'] is True; assert proof['ok'] is True
        assert read_model['requisition_count']==1; assert read_model['candidate_count']==1; assert read_model['hired_count']==1; assert read_model['provisioned_count']==1; assert read_model['completed_task_count']==1
    finally: repo.close()

def test_standalone_routes_ui_agent_and_release_surface():
    service=services.TalentOnboardingStandaloneService()
    try:
        seed_route=routes.dispatch_standalone_route('POST','/app/talent-onboarding/demo-workspace',{'tenant':'tenant_route_test'},service=service)
        workbench=routes.dispatch_standalone_route('GET','/app/talent-onboarding/workbench',{'tenant':'tenant_route_test'},service=service)
        proof=routes.dispatch_standalone_route('POST','/app/talent-onboarding/proofs',{'tenant':'tenant_route_test','candidate_id':'cand_demo_100'},service=service)
        rendered=ui.talent_onboarding_render_standalone_workbench(workbench['result']['result'])
        document_plan=agent.document_instruction_plan('candidate packet','offer accept onboard provision')
        crud_plan=agent.datastore_crud_plan('create','talent_onboarding_candidate',{'candidate_id':'cand_demo_100'})
        app_contract=standalone.talent_onboarding_standalone_app_contract(); smoke=standalone.talent_onboarding_standalone_app_smoke(); evidence=release_evidence.build_release_evidence()
        assert seed_route['ok'] is True; assert workbench['ok'] is True; assert proof['ok'] is True; assert rendered['ok'] is True
        assert document_plan['wizard_candidates']; assert crud_plan['route_candidates']; assert app_contract['ok'] is True; assert smoke['ok'] is True; assert evidence['standalone_app']['ok'] is True; assert evidence['standalone_repository']['ok'] is True
    finally: service.close()

def test_package_local_docs_exist_for_release_evidence():
    base=Path(__file__).resolve().parent.parent
    for name in ('README.md','RELEASE_EVIDENCE.md','repository.py','standalone.py'):
        assert (base/name).exists() is True
