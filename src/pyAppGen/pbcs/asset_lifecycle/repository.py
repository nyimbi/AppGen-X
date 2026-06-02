"""Package-local persistence for the standalone Asset Lifecycle application."""
from __future__ import annotations
import json, sqlite3
from pathlib import Path
from typing import Any
from . import runtime, seed_data
PBC_KEY='asset_lifecycle'
STATE_TABLE='asset_lifecycle_runtime_state'; FORM_TABLE='asset_lifecycle_form_submission'; WORKFLOW_TABLE='asset_lifecycle_workflow_run'; CONTROL_TABLE='asset_lifecycle_control_execution'; AGENT_TABLE='asset_lifecycle_agent_session'; READ_MODEL_TABLE='asset_lifecycle_workbench_read_model'
_SCHEMA=f"""
CREATE TABLE IF NOT EXISTS {STATE_TABLE} (tenant TEXT PRIMARY KEY, state_json TEXT NOT NULL, updated_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS {FORM_TABLE} (submission_id TEXT PRIMARY KEY, tenant TEXT NOT NULL, form_key TEXT NOT NULL, action TEXT NOT NULL, subject_id TEXT, payload_json TEXT NOT NULL, result_json TEXT NOT NULL, created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS {WORKFLOW_TABLE} (workflow_run_id TEXT PRIMARY KEY, tenant TEXT NOT NULL, wizard_key TEXT NOT NULL, subject_id TEXT, status TEXT NOT NULL, context_json TEXT NOT NULL, result_json TEXT NOT NULL, created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS {CONTROL_TABLE} (control_run_id TEXT PRIMARY KEY, tenant TEXT NOT NULL, control_key TEXT NOT NULL, allowed INTEGER NOT NULL, result_json TEXT NOT NULL, created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS {AGENT_TABLE} (session_id TEXT PRIMARY KEY, tenant TEXT NOT NULL, skill_name TEXT NOT NULL, scope TEXT NOT NULL, requires_confirmation INTEGER NOT NULL, payload_json TEXT NOT NULL, result_json TEXT NOT NULL, created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS {READ_MODEL_TABLE} (read_model_id TEXT PRIMARY KEY, tenant TEXT NOT NULL, asset_count INTEGER NOT NULL, in_service_count INTEGER NOT NULL, retired_count INTEGER NOT NULL, net_book_value REAL NOT NULL, pending_schedule_revisions INTEGER NOT NULL, payload_json TEXT NOT NULL, updated_at TEXT NOT NULL);
"""
def _json(v:Any)->str: return json.dumps(v, sort_keys=True)
def _load(v:str|None)->Any: return None if v is None else json.loads(v)
def _now()->str: return 'local-harness-clock'
class AssetLifecycleStandaloneRepository:
    """Persists a one-PBC fixed asset workspace with forms, workflows, controls, and agent sessions."""
    def __init__(self,database_path=':memory:'):
        self.database_path=database_path
        if database_path!=':memory:': Path(database_path).expanduser().resolve().parent.mkdir(parents=True,exist_ok=True)
        self.connection=sqlite3.connect(database_path); self.connection.row_factory=sqlite3.Row; self.apply_migrations()
    def close(self): self.connection.close()
    def apply_migrations(self): self.connection.executescript(_SCHEMA); self.connection.commit(); return (STATE_TABLE,FORM_TABLE,WORKFLOW_TABLE,CONTROL_TABLE,AGENT_TABLE,READ_MODEL_TABLE)
    def load_state(self,tenant):
        row=self.connection.execute(f'SELECT state_json FROM {STATE_TABLE} WHERE tenant=?',(tenant,)).fetchone()
        return _load(row['state_json']) if row else runtime.asset_lifecycle_empty_state()
    def save_state(self,tenant,state):
        self.connection.execute(f'INSERT INTO {STATE_TABLE} VALUES (?,?,?) ON CONFLICT(tenant) DO UPDATE SET state_json=excluded.state_json, updated_at=excluded.updated_at',(tenant,_json(state),_now()))
        self._sync_read_model(tenant,state); self.connection.commit(); return {'ok':True,'tenant':tenant}
    def _sync_read_model(self,tenant,state):
        view=runtime.asset_lifecycle_build_workbench_view(state,tenant=tenant) if state.get('configuration') else {'ok':True,'tenant':tenant,'asset_count':0,'in_service_count':0,'retired_count':0,'net_book_value':0,'pending_schedule_revisions':0}
        row={'read_model_id':f'{tenant}:workbench','tenant':tenant,'asset_count':int(view.get('asset_count',0)),'in_service_count':int(view.get('in_service_count',0)),'retired_count':int(view.get('retired_count',0)),'net_book_value':float(view.get('net_book_value',0.0)),'pending_schedule_revisions':int(view.get('pending_schedule_revisions',0)),'payload_json':_json(view),'updated_at':_now()}
        self.connection.execute(f'DELETE FROM {READ_MODEL_TABLE} WHERE tenant=?',(tenant,)); self.connection.execute(f"INSERT INTO {READ_MODEL_TABLE} ({', '.join(row)}) VALUES ({', '.join('?' for _ in row)})",tuple(row.values()))
    def _insert(self,table,prefix,fields):
        n=self.connection.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0]; self.connection.execute(f"INSERT INTO {table} VALUES ({', '.join('?' for _ in range(len(fields)+1))})",(f'{prefix}_{n+1:05d}',*fields))
    def _form(self,t,k,a,s,p,r): self._insert(FORM_TABLE,'form',(t,k,a,s,_json(p),_json(r),_now()))
    def _workflow(self,t,k,s,c,r): self._insert(WORKFLOW_TABLE,'workflow',(t,k,s,'completed' if r.get('ok') else 'blocked',_json(c),_json(r),_now()))
    def _control(self,t,k,r): self._insert(CONTROL_TABLE,'control',(t,k,int(bool(r.get('ok'))),_json(r),_now()))
    def _result(self,t,r):
        if r.get('ok') is True and 'state' in r: self.save_state(t,r['state'])
        return r
    def configure_runtime(self,t,c): r=runtime.asset_lifecycle_configure_runtime(self.load_state(t),c); self._form(t,'AssetConfigurationForm','configure_runtime',None,c,r); return self._result(t,r)
    def set_parameter(self,t,k,v): r=runtime.asset_lifecycle_set_parameter(self.load_state(t),k,v); self._form(t,'AssetParameterForm','set_parameter',k,{'key':k,'value':v},r); return self._result(t,r)
    def register_rule(self,t,rule): r=runtime.asset_lifecycle_register_rule(self.load_state(t),rule); self._form(t,'AssetRuleForm','register_rule',rule.get('rule_id'),rule,r); return self._result(t,r)
    def receive_event(self,t,e): r=runtime.asset_lifecycle_receive_event(self.load_state(t),e); self._form(t,'AssetEventInboxForm','receive_event',e.get('event_id'),e,r); return self._result(t,r)
    def register_asset(self,t,a):
        norm={**a,'components':tuple(a.get('components',()))}; r=runtime.asset_lifecycle_register_asset(self.load_state(t),norm); self._form(t,'AssetRegisterForm','register_asset',a.get('asset_id'),a,r); return self._result(t,r)
    def place_asset_in_service(self,t,asset_id,service_date): r=runtime.asset_lifecycle_place_asset_in_service(self.load_state(t),asset_id,service_date=service_date); self._workflow(t,'PlaceInServiceWizard',asset_id,{'service_date':service_date},r); return self._result(t,r)
    def build_depreciation_schedule(self,t,asset_id,method='straight_line'): r=runtime.asset_lifecycle_build_depreciation_schedule(self.load_state(t),asset_id,method=method); self._workflow(t,'DepreciationScheduleWizard',asset_id,{'method':method},r); return self._result(t,r)
    def run_depreciation(self,t,run_id,period): r=runtime.asset_lifecycle_run_depreciation(self.load_state(t),run_id=run_id,period=period); self._workflow(t,'DepreciationRunWizard',run_id,{'period':period},r); return self._result(t,r)
    def transfer_asset(self,t,asset_id,location,cost_center,approved_by): r=runtime.asset_lifecycle_transfer_asset(self.load_state(t),asset_id,location=location,cost_center=cost_center,approved_by=approved_by); self._workflow(t,'AssetTransferWizard',asset_id,{'location':location,'cost_center':cost_center},r); return self._result(t,r)
    def revalue_asset(self,t,asset_id,fair_value,approved_by): r=runtime.asset_lifecycle_revalue_asset(self.load_state(t),asset_id,fair_value=fair_value,approved_by=approved_by); self._workflow(t,'ValuationWizard',asset_id,{'fair_value':fair_value},r); return self._result(t,r)
    def impair_asset(self,t,asset_id,recoverable_amount,approved_by): r=runtime.asset_lifecycle_impair_asset(self.load_state(t),asset_id,recoverable_amount=recoverable_amount,approved_by=approved_by); self._workflow(t,'ValuationWizard',asset_id,{'recoverable_amount':recoverable_amount},r); return self._result(t,r)
    def record_maintenance_adjustment(self,t,asset_id,useful_life_delta_months,evidence): r=runtime.asset_lifecycle_record_maintenance_adjustment(self.load_state(t),asset_id,useful_life_delta_months=useful_life_delta_months,evidence=evidence); self._workflow(t,'MaintenanceAdjustmentWizard',asset_id,{'useful_life_delta_months':useful_life_delta_months,'evidence':evidence},r); return self._result(t,r)
    def retire_asset(self,t,asset_id,proceeds,approved_by): r=runtime.asset_lifecycle_retire_asset(self.load_state(t),asset_id,proceeds=proceeds,approved_by=approved_by); self._workflow(t,'AssetRetirementWizard',asset_id,{'proceeds':proceeds},r); return self._result(t,r)
    def generate_asset_audit_proof(self,t,asset_id,disclosure): r=runtime.asset_lifecycle_generate_asset_audit_proof(self.load_state(t),asset_id,disclosure=tuple(disclosure)); self._control(t,'asset_audit_proof',r); self.connection.commit(); return r
    def run_control_tests(self,t): r=runtime.asset_lifecycle_run_control_tests(self.load_state(t)); self._control(t,'asset_release_controls',r); self.connection.commit(); return r
    def run_agent_skill(self,t,skill,payload):
        from . import agent
        plan=agent.document_instruction_plan(payload.get('document'),payload.get('instructions')); r={'ok':plan['ok'],'skill_name':skill,'plan':plan,'requires_confirmation':True}; n=self.connection.execute(f'SELECT COUNT(*) FROM {AGENT_TABLE}').fetchone()[0]; self.connection.execute(f'INSERT INTO {AGENT_TABLE} VALUES (?,?,?,?,?,?,?,?)',(f'agent_{n+1:05d}',t,skill,payload.get('scope','asset'),1,_json(payload),_json(r),_now())); self.connection.commit(); return r
    def build_workbench(self,t): st=self.load_state(t); return {'ok':True,**runtime.asset_lifecycle_build_workbench_view(st,tenant=t),'activity_counts':self.activity_counts(t),'read_model':self.read_model(t)}
    def read_model(self,t):
        row=self.connection.execute(f'SELECT * FROM {READ_MODEL_TABLE} WHERE tenant=?',(t,)).fetchone()
        if not row: return {'ok':False,'tenant':t,'reason':'read_model_not_found'}
        d=dict(row); d['payload']=_load(d.pop('payload_json')); d['ok']=True; return d
    def activity_counts(self,t): return {'forms':self.connection.execute(f'SELECT COUNT(*) FROM {FORM_TABLE} WHERE tenant=?',(t,)).fetchone()[0],'workflows':self.connection.execute(f'SELECT COUNT(*) FROM {WORKFLOW_TABLE} WHERE tenant=?',(t,)).fetchone()[0],'controls':self.connection.execute(f'SELECT COUNT(*) FROM {CONTROL_TABLE} WHERE tenant=?',(t,)).fetchone()[0],'agent_sessions':self.connection.execute(f'SELECT COUNT(*) FROM {AGENT_TABLE} WHERE tenant=?',(t,)).fetchone()[0]}
    def seed_demo_workspace(self,tenant='tenant_demo'):
        b=seed_data.standalone_seed_bundle(tenant=tenant); self.configure_runtime(tenant,b['configuration']); [self.set_parameter(tenant,k,v) for k,v in b['parameters'].items()]; [self.register_rule(tenant,r) for r in b['rules']]; [self.receive_event(tenant,e) for e in b['events']]; self.register_asset(tenant,b['asset']); self.place_asset_in_service(tenant,b['asset']['asset_id'],b['service_date']); self.build_depreciation_schedule(tenant,b['asset']['asset_id'],b['depreciation_method']); self.run_depreciation(tenant,b['depreciation_run']['run_id'],b['depreciation_run']['period']); self.transfer_asset(tenant,b['asset']['asset_id'],b['transfer']['location'],b['transfer']['cost_center'],b['transfer']['approved_by']); self.record_maintenance_adjustment(tenant,b['asset']['asset_id'],b['maintenance_adjustment']['useful_life_delta_months'],b['maintenance_adjustment']['evidence']); self.build_depreciation_schedule(tenant,b['asset']['asset_id'],b['depreciation_method']); controls=self.run_control_tests(tenant); proof=self.generate_asset_audit_proof(tenant,b['asset']['asset_id'],('asset_id','status','book_value','location')); agent=self.run_agent_skill(tenant,'asset_lifecycle.document_instruction_intake',{'document':b['document'],'instructions':b['instructions'],'scope':'seed'}); return {'ok':controls['ok'] and proof['ok'] and agent['ok'],'tenant':tenant,'bundle':b,'workbench':self.build_workbench(tenant)}

def standalone_repository_contract(): return {'format':'appgen.asset-lifecycle-standalone-repository.v1','ok':True,'pbc':PBC_KEY,'repository_class':'AssetLifecycleStandaloneRepository','local_harness_backend':'sqlite3','deployment_database_backends':runtime.ASSET_LIFECYCLE_ALLOWED_DATABASE_BACKENDS,'tables':(STATE_TABLE,FORM_TABLE,WORKFLOW_TABLE,CONTROL_TABLE,AGENT_TABLE,READ_MODEL_TABLE),'side_effects':()}
def standalone_repository_smoke_test():
    repo=AssetLifecycleStandaloneRepository()
    try:
        seeded=repo.seed_demo_workspace(); return {'ok':seeded['ok'] and repo.read_model('tenant_demo')['ok'],'seeded':seeded,'contract':standalone_repository_contract(),'side_effects':()}
    finally: repo.close()
