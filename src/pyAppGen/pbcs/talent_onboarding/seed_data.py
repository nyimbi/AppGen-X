"""Executable seed-data contract for the talent_onboarding PBC."""

PBC_KEY = 'talent_onboarding'
SEED_DATA = ({'table': 'talent_onboarding_job_requisition', 'rows': ({'code': 'TALENT_ONBOARDING-001', 'status': 'active'},)}, {'table': 'talent_onboarding_job_requisition_approval', 'rows': ({'code': 'TALENT_ONBOARDING-002', 'status': 'active'},)})


def seed_plan():
    """Return deterministic seed rows without applying them."""
    tables = tuple(dict.fromkeys(item['table'] for item in SEED_DATA))
    return {
        'ok': bool(SEED_DATA),
        'pbc': PBC_KEY,
        'tables': tables,
        'rows': SEED_DATA,
        'side_effects': (),
    }


def validate_seed_data():
    """Validate seed ownership and minimum row shape."""
    invalid_tables = tuple(
        item['table'] for item in SEED_DATA if not item.get('table', '').startswith(f'{PBC_KEY}_')
    )
    invalid_rows = tuple(
        row
        for item in SEED_DATA
        for row in item.get('rows', ())
        if not row.get('code') or not row.get('status')
    )
    plan = seed_plan()
    return {
        'ok': plan['ok'] and not invalid_tables and not invalid_rows,
        'pbc': PBC_KEY,
        'plan': plan,
        'invalid_tables': invalid_tables,
        'invalid_rows': invalid_rows,
        'side_effects': (),
    }


def smoke_test():
    """Exercise seed validation without writing rows."""
    return validate_seed_data()



def standalone_seed_bundle(*, tenant='tenant_demo'):
    return {'pbc':PBC_KEY,'tenant':tenant,'configuration':{'database_backend':'postgresql','event_topic':'appgen.talent.events','retry_limit':3,'allowed_countries':('US','CA'),'allowed_candidate_sources':('referral','career_site','agency'),'allowed_check_providers':('trusted_screen',),'allowed_task_types':('identity','equipment','policy','training'),'default_timezone':'UTC','workbench_limit':100},'parameters':{'minimum_match_score':0.7,'offer_expiry_days':7,'onboarding_sla_days':5,'background_check_confidence_threshold':0.85,'retention_days':365,'candidate_review_sla_days':3,'interview_panel_size':3,'offer_approval_threshold':0.8,'workbench_limit':100},'rules':({'rule_id':'talent.demo.hiring','tenant':tenant,'rule_type':'hiring','eligible_worker_types':('employee',),'allowed_countries':('US',),'required_candidate_consents':('privacy','screening'),'allowed_stages':('applied','screen','interview','offer','hired'),'required_check_types':('identity','criminal'),'task_templates':('identity','equipment','policy'),'status':'active'},),'requisition':{'requisition_id':'req_demo_100','tenant':tenant,'title':'Operations Analyst','department':'Operations','manager_employee_id':'mgr_100','country':'US','location':'NYC','worker_type':'employee','headcount':1,'budget':120000},'candidate':{'candidate_id':'cand_demo_100','tenant':tenant,'requisition_id':'req_demo_100','name':'Ada Worker','source':'referral','country':'US','skills':('operations','analytics'),'match_score':0.86,'consents':('privacy','screening'),'identity':{'did':'did:appgen:cand-demo-100','issuer':'trusted_registry','status':'active'}},'background_check':{'check_id':'check_demo_100','tenant':tenant,'candidate_id':'cand_demo_100','provider':'trusted_screen','check_type':'identity','confidence':0.93,'result':'clear'},'offer':{'offer_id':'offer_demo_100','salary':95000,'currency':'USD','start_date':'2026-06-15','expires_in_days':7},'task':{'task_id':'task_demo_100','task_type':'identity','assignee':'hr_ops','due_in_days':3},'document':'Candidate packet for Ada Worker, clear background check, accepted offer, identity onboarding task.','instructions':'Create candidate, advance to interview and offer, accept offer, complete onboarding task, provision employee.'}
