"""Package-local persistence for the standalone Talent Onboarding application."""
from __future__ import annotations
import json, sqlite3
from pathlib import Path
from typing import Any
from . import runtime, seed_data
PBC_KEY='talent_onboarding'; STATE_TABLE='talent_onboarding_runtime_state'; FORM_TABLE='talent_onboarding_form_submission'; WORKFLOW_TABLE='talent_onboarding_workflow_run'; CONTROL_TABLE='talent_onboarding_control_execution'; AGENT_TABLE='talent_onboarding_agent_session'; READ_MODEL_TABLE='talent_onboarding_workbench_read_model'
_SCHEMA=f"""
CREATE TABLE IF NOT EXISTS {STATE_TABLE} (tenant TEXT PRIMARY KEY, state_json TEXT NOT NULL, updated_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS {FORM_TABLE} (submission_id TEXT PRIMARY KEY, tenant TEXT NOT NULL, form_key TEXT NOT NULL, action TEXT NOT NULL, subject_id TEXT, payload_json TEXT NOT NULL, result_json TEXT NOT NULL, created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS {WORKFLOW_TABLE} (workflow_run_id TEXT PRIMARY KEY, tenant TEXT NOT NULL, wizard_key TEXT NOT NULL, subject_id TEXT, status TEXT NOT NULL, context_json TEXT NOT NULL, result_json TEXT NOT NULL, created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS {CONTROL_TABLE} (control_run_id TEXT PRIMARY KEY, tenant TEXT NOT NULL, control_key TEXT NOT NULL, allowed INTEGER NOT NULL, result_json TEXT NOT NULL, created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS {AGENT_TABLE} (session_id TEXT PRIMARY KEY, tenant TEXT NOT NULL, skill_name TEXT NOT NULL, scope TEXT NOT NULL, requires_confirmation INTEGER NOT NULL, payload_json TEXT NOT NULL, result_json TEXT NOT NULL, created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS {READ_MODEL_TABLE} (read_model_id TEXT PRIMARY KEY, tenant TEXT NOT NULL, requisition_count INTEGER NOT NULL, candidate_count INTEGER NOT NULL, hired_count INTEGER NOT NULL, provisioned_count INTEGER NOT NULL, check_count INTEGER NOT NULL, offer_count INTEGER NOT NULL, completed_task_count INTEGER NOT NULL, payload_json TEXT NOT NULL, updated_at TEXT NOT NULL);
"""
def _json(v:Any)->str: return json.dumps(v, sort_keys=True)
def _load(v:str|None)->Any: return None if v is None else json.loads(v)
def _now()->str: return 'local-harness-clock'
class TalentOnboardingStandaloneRepository:
    def __init__(self,database_path=':memory:'):
        self.database_path=database_path
        if database_path!=':memory:': Path(database_path).expanduser().resolve().parent.mkdir(parents=True,exist_ok=True)
        self.connection=sqlite3.connect(database_path); self.connection.row_factory=sqlite3.Row; self.apply_migrations()
    def close(self): self.connection.close()
    def apply_migrations(self): self.connection.executescript(_SCHEMA); self.connection.commit(); return (STATE_TABLE,FORM_TABLE,WORKFLOW_TABLE,CONTROL_TABLE,AGENT_TABLE,READ_MODEL_TABLE)
    def load_state(self,t):
        row=self.connection.execute(f'SELECT state_json FROM {STATE_TABLE} WHERE tenant=?',(t,)).fetchone(); return _load(row['state_json']) if row else runtime.talent_onboarding_empty_state()
    def save_state(self,t,state): self.connection.execute(f'INSERT INTO {STATE_TABLE} VALUES (?,?,?) ON CONFLICT(tenant) DO UPDATE SET state_json=excluded.state_json, updated_at=excluded.updated_at',(t,_json(state),_now())); self._sync_read_model(t,state); self.connection.commit(); return {'ok':True,'tenant':t}
    def _sync_read_model(self,t,state):
        req=tuple(i for i in state.get('requisitions',{}).values() if i.get('tenant')==t); cand=tuple(i for i in state.get('candidates',{}).values() if i.get('tenant')==t); checks=tuple(i for i in state.get('checks',{}).values() if i.get('tenant')==t); offers=tuple(i for i in state.get('offers',{}).values() if i.get('tenant')==t); tasks=tuple(i for i in state.get('tasks',{}).values() if i.get('tenant')==t)
        payload=runtime.talent_onboarding_build_workbench_view(state,tenant=t) if state.get('configuration') else {'ok':True,'tenant':t}
        row={'read_model_id':f'{t}:workbench','tenant':t,'requisition_count':len(req),'candidate_count':len(cand),'hired_count':len(tuple(i for i in cand if i.get('stage')=='hired')),'provisioned_count':len(tuple(i for i in cand if i.get('status')=='provisioned')),'check_count':len(checks),'offer_count':len(offers),'completed_task_count':len(tuple(i for i in tasks if i.get('status')=='completed')),'payload_json':_json(payload),'updated_at':_now()}
        self.connection.execute(f'DELETE FROM {READ_MODEL_TABLE} WHERE tenant=?',(t,)); self.connection.execute(f"INSERT INTO {READ_MODEL_TABLE} ({', '.join(row)}) VALUES ({', '.join('?' for _ in row)})",tuple(row.values()))
    def _insert(self,table,prefix,fields): n=self.connection.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0]; self.connection.execute(f"INSERT INTO {table} VALUES ({', '.join('?' for _ in range(len(fields)+1))})",(f'{prefix}_{n+1:05d}',*fields))
    def _form(self,t,k,a,s,p,r): self._insert(FORM_TABLE,'form',(t,k,a,s,_json(p),_json(r),_now()))
    def _workflow(self,t,k,s,c,r): self._insert(WORKFLOW_TABLE,'workflow',(t,k,s,'completed' if r.get('ok') else 'blocked',_json(c),_json(r),_now()))
    def _control(self,t,k,r): self._insert(CONTROL_TABLE,'control',(t,k,int(bool(r.get('ok'))),_json(r),_now()))
    def _result(self,t,r):
        if r.get('ok') is True and 'state' in r: self.save_state(t,r['state'])
        return r
    def configure_runtime(self,t,c): norm={**c,'allowed_countries':tuple(c.get('allowed_countries',())),'allowed_candidate_sources':tuple(c.get('allowed_candidate_sources',())),'allowed_check_providers':tuple(c.get('allowed_check_providers',())),'allowed_task_types':tuple(c.get('allowed_task_types',()))}; r=runtime.talent_onboarding_configure_runtime(self.load_state(t),norm); self._form(t,'TalentConfigurationForm','configure_runtime',None,c,r); return self._result(t,r)
    def set_parameter(self,t,n,v): r=runtime.talent_onboarding_set_parameter(self.load_state(t),n,v); self._form(t,'TalentParameterForm','set_parameter',n,{'name':n,'value':v},r); return self._result(t,r)
    def register_rule(self,t,rule): r=runtime.talent_onboarding_register_rule(self.load_state(t),rule); self._form(t,'TalentRuleForm','register_rule',rule.get('rule_id'),rule,r); return self._result(t,r)
    def create_job_requisition(self,t,p): r=runtime.talent_onboarding_create_job_requisition(self.load_state(t),p); self._form(t,'RequisitionForm','create_job_requisition',p.get('requisition_id'),p,r); return self._result(t,r)
    def create_candidate(self,t,p): r=runtime.talent_onboarding_create_candidate(self.load_state(t),p); self._form(t,'CandidateForm','create_candidate',p.get('candidate_id'),p,r); return self._result(t,r)
    def advance_candidate_stage(self,t,candidate_id,stage,actor): r=runtime.talent_onboarding_advance_candidate_stage(self.load_state(t),candidate_id,stage=stage,actor=actor); self._workflow(t,'CandidatePipelineWizard',candidate_id,{'stage':stage},r); return self._result(t,r)
    def record_background_check(self,t,p): r=runtime.talent_onboarding_record_background_check(self.load_state(t),p); self._form(t,'BackgroundCheckForm','record_background_check',p.get('check_id'),p,r); return self._result(t,r)
    def extend_offer(self,t,candidate_id,p): r=runtime.talent_onboarding_extend_offer(self.load_state(t),candidate_id,p); self._form(t,'OfferForm','extend_offer',p.get('offer_id'),p,r); return self._result(t,r)
    def accept_offer(self,t,candidate_id,accepted_by): r=runtime.talent_onboarding_accept_offer(self.load_state(t),candidate_id,accepted_by=accepted_by); self._workflow(t,'OfferAcceptanceWizard',candidate_id,{'accepted_by':accepted_by},r); return self._result(t,r)
    def create_onboarding_task(self,t,candidate_id,p): r=runtime.talent_onboarding_create_onboarding_task(self.load_state(t),candidate_id,p); self._form(t,'OnboardingTaskForm','create_onboarding_task',p.get('task_id'),p,r); return self._result(t,r)
    def complete_onboarding_task(self,t,task_id,completed_by): r=runtime.talent_onboarding_complete_onboarding_task(self.load_state(t),task_id,completed_by=completed_by); self._workflow(t,'OnboardingCompletionWizard',task_id,{'completed_by':completed_by},r); return self._result(t,r)
    def provision_employee(self,t,candidate_id,provisioned_by): r=runtime.talent_onboarding_provision_employee(self.load_state(t),candidate_id,provisioned_by=provisioned_by); self._workflow(t,'EmployeeProvisioningWizard',candidate_id,{'provisioned_by':provisioned_by},r); return self._result(t,r)
    def run_control_tests(self,t): r=runtime.talent_onboarding_run_control_tests(self.load_state(t)); self._control(t,'talent_release_controls',r); self.connection.commit(); return r
    def generate_candidate_proof(self,t,candidate_id,disclosure): r=runtime.talent_onboarding_generate_candidate_proof(self.load_state(t),candidate_id,disclosure=tuple(disclosure)); self._control(t,'candidate_proof',r); self.connection.commit(); return r
    def run_agent_skill(self,t,skill,payload):
        from . import agent
        plan=agent.document_instruction_plan(payload.get('document'),payload.get('instructions')); r={'ok':plan['ok'],'skill_name':skill,'plan':plan,'requires_confirmation':True}; n=self.connection.execute(f'SELECT COUNT(*) FROM {AGENT_TABLE}').fetchone()[0]; self.connection.execute(f'INSERT INTO {AGENT_TABLE} VALUES (?,?,?,?,?,?,?,?)',(f'agent_{n+1:05d}',t,skill,payload.get('scope','talent'),1,_json(payload),_json(r),_now())); self.connection.commit(); return r
    def build_workbench(self,t): st=self.load_state(t); return {'ok':True,**runtime.talent_onboarding_build_workbench_view(st,tenant=t),'activity_counts':self.activity_counts(t),'read_model':self.read_model(t)}
    def read_model(self,t):
        row=self.connection.execute(f'SELECT * FROM {READ_MODEL_TABLE} WHERE tenant=?',(t,)).fetchone()
        if not row: return {'ok':False,'tenant':t,'reason':'read_model_not_found'}
        d=dict(row); d['payload']=_load(d.pop('payload_json')); d['ok']=True; return d
    def activity_counts(self,t): return {'forms':self.connection.execute(f'SELECT COUNT(*) FROM {FORM_TABLE} WHERE tenant=?',(t,)).fetchone()[0],'workflows':self.connection.execute(f'SELECT COUNT(*) FROM {WORKFLOW_TABLE} WHERE tenant=?',(t,)).fetchone()[0],'controls':self.connection.execute(f'SELECT COUNT(*) FROM {CONTROL_TABLE} WHERE tenant=?',(t,)).fetchone()[0],'agent_sessions':self.connection.execute(f'SELECT COUNT(*) FROM {AGENT_TABLE} WHERE tenant=?',(t,)).fetchone()[0]}
    def seed_demo_workspace(self,tenant='tenant_demo'):
        b=seed_data.standalone_seed_bundle(tenant=tenant); self.configure_runtime(tenant,b['configuration']); [self.set_parameter(tenant,k,v) for k,v in b['parameters'].items()]; [self.register_rule(tenant,r) for r in b['rules']]; self.create_job_requisition(tenant,b['requisition']); self.create_candidate(tenant,b['candidate']); self.advance_candidate_stage(tenant,b['candidate']['candidate_id'],'interview','recruiter_1'); self.record_background_check(tenant,b['background_check']); self.extend_offer(tenant,b['candidate']['candidate_id'],b['offer']); self.accept_offer(tenant,b['candidate']['candidate_id'],'candidate'); self.create_onboarding_task(tenant,b['candidate']['candidate_id'],b['task']); self.complete_onboarding_task(tenant,b['task']['task_id'],'hr_ops'); self.provision_employee(tenant,b['candidate']['candidate_id'],'hr_ops'); controls=self.run_control_tests(tenant); proof=self.generate_candidate_proof(tenant,b['candidate']['candidate_id'],('candidate_id','requisition_id','stage')); agent=self.run_agent_skill(tenant,'talent_onboarding.document_instruction_intake',{'document':b['document'],'instructions':b['instructions'],'scope':'seed'}); return {'ok':controls['ok'] and proof['ok'] and agent['ok'],'tenant':tenant,'bundle':b,'workbench':self.build_workbench(tenant)}
def standalone_repository_contract(): return {'format':'appgen.talent-onboarding-standalone-repository.v1','ok':True,'pbc':PBC_KEY,'repository_class':'TalentOnboardingStandaloneRepository','local_harness_backend':'sqlite3','deployment_database_backends':runtime.TALENT_ONBOARDING_ALLOWED_DATABASE_BACKENDS,'tables':(STATE_TABLE,FORM_TABLE,WORKFLOW_TABLE,CONTROL_TABLE,AGENT_TABLE,READ_MODEL_TABLE),'side_effects':()}
def standalone_repository_smoke_test():
    repo=TalentOnboardingStandaloneRepository()
    try:
        seeded=repo.seed_demo_workspace(); return {'ok':seeded['ok'] and repo.read_model('tenant_demo')['ok'],'seeded':seeded,'contract':standalone_repository_contract(),'side_effects':()}
    finally: repo.close()
