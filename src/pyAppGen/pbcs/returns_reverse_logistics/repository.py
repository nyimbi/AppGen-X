"""Package-local persistence for the standalone Returns Reverse Logistics app."""
from __future__ import annotations
import json, sqlite3
from pathlib import Path
from typing import Any
from . import runtime, seed_data
PBC_KEY="returns_reverse_logistics"
STATE_TABLE="returns_reverse_logistics_runtime_state"; FORM_TABLE="returns_reverse_logistics_form_submission"; WORKFLOW_TABLE="returns_reverse_logistics_workflow_run"; CONTROL_TABLE="returns_reverse_logistics_control_execution"; AGENT_TABLE="returns_reverse_logistics_agent_session"; READ_MODEL_TABLE="returns_reverse_logistics_workbench_read_model"
_SCHEMA=f"""
CREATE TABLE IF NOT EXISTS {STATE_TABLE} (tenant TEXT PRIMARY KEY, state_json TEXT NOT NULL, updated_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS {FORM_TABLE} (submission_id TEXT PRIMARY KEY, tenant TEXT NOT NULL, form_key TEXT NOT NULL, action TEXT NOT NULL, subject_id TEXT, payload_json TEXT NOT NULL, result_json TEXT NOT NULL, created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS {WORKFLOW_TABLE} (workflow_run_id TEXT PRIMARY KEY, tenant TEXT NOT NULL, wizard_key TEXT NOT NULL, subject_id TEXT, status TEXT NOT NULL, context_json TEXT NOT NULL, result_json TEXT NOT NULL, created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS {CONTROL_TABLE} (control_run_id TEXT PRIMARY KEY, tenant TEXT NOT NULL, control_key TEXT NOT NULL, allowed INTEGER NOT NULL, result_json TEXT NOT NULL, created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS {AGENT_TABLE} (session_id TEXT PRIMARY KEY, tenant TEXT NOT NULL, skill_name TEXT NOT NULL, scope TEXT NOT NULL, requires_confirmation INTEGER NOT NULL, payload_json TEXT NOT NULL, result_json TEXT NOT NULL, created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS {READ_MODEL_TABLE} (read_model_id TEXT PRIMARY KEY, tenant TEXT NOT NULL, return_count INTEGER NOT NULL, label_count INTEGER NOT NULL, receipt_count INTEGER NOT NULL, inspection_count INTEGER NOT NULL, credit_count INTEGER NOT NULL, customer_status_count INTEGER NOT NULL, exception_count INTEGER NOT NULL, dead_letter_count INTEGER NOT NULL, payload_json TEXT NOT NULL, updated_at TEXT NOT NULL);
"""
def _json(v:Any)->str: return json.dumps(v, sort_keys=True, default=str)
def _load(v:str|None)->Any: return None if v is None else json.loads(v)
def _now()->str: return "local-harness-clock"
class ReturnsReverseLogisticsStandaloneRepository:
    def __init__(self,database_path=':memory:'):
        self.database_path=database_path
        if database_path != ':memory:': Path(database_path).expanduser().resolve().parent.mkdir(parents=True, exist_ok=True)
        self.connection=sqlite3.connect(database_path); self.connection.row_factory=sqlite3.Row; self.apply_migrations()
    def close(self): self.connection.close()
    def apply_migrations(self): self.connection.executescript(_SCHEMA); self.connection.commit(); return (STATE_TABLE,FORM_TABLE,WORKFLOW_TABLE,CONTROL_TABLE,AGENT_TABLE,READ_MODEL_TABLE)
    def load_state(self,tenant):
        row=self.connection.execute(f"SELECT state_json FROM {STATE_TABLE} WHERE tenant=?",(tenant,)).fetchone()
        return _load(row['state_json']) if row else runtime.returns_reverse_logistics_empty_state()
    def save_state(self,tenant,state):
        self.connection.execute(f"INSERT INTO {STATE_TABLE} VALUES (?,?,?) ON CONFLICT(tenant) DO UPDATE SET state_json=excluded.state_json, updated_at=excluded.updated_at",(tenant,_json(state),_now()))
        self._sync_read_model(tenant,state); self.connection.commit(); return {'ok':True,'tenant':tenant}
    def _sync_read_model(self,tenant,state):
        view=runtime.returns_reverse_logistics_build_workbench_view(state,tenant=tenant) if state.get('configuration') else {'ok':True,'tenant':tenant}
        row={'read_model_id':f'{tenant}:workbench','tenant':tenant,'return_count':int(view.get('return_count',0)),'label_count':int(view.get('label_count',0)),'receipt_count':int(view.get('receipt_count',0)),'inspection_count':int(view.get('inspection_count',0)),'credit_count':int(view.get('credit_count',0)),'customer_status_count':int(view.get('customer_status_count',0)),'exception_count':int(view.get('exception_count',0)),'dead_letter_count':int(view.get('dead_letter_count',0)),'payload_json':_json(view),'updated_at':_now()}
        self.connection.execute(f"DELETE FROM {READ_MODEL_TABLE} WHERE tenant=?",(tenant,)); self.connection.execute(f"INSERT INTO {READ_MODEL_TABLE} ({', '.join(row)}) VALUES ({', '.join('?' for _ in row)})",tuple(row.values()))
    def _insert(self,table,prefix,fields):
        n=self.connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]; self.connection.execute(f"INSERT INTO {table} VALUES ({', '.join('?' for _ in range(len(fields)+1))})",(f'{prefix}_{n+1:05d}',*fields))
    def _form(self,t,k,a,s,p,r): self._insert(FORM_TABLE,'form',(t,k,a,s,_json(p),_json(r),_now()))
    def _workflow(self,t,k,s,c,r): self._insert(WORKFLOW_TABLE,'workflow',(t,k,s,'completed' if r.get('ok') else 'blocked',_json(c),_json(r),_now()))
    def _control(self,t,k,r): self._insert(CONTROL_TABLE,'control',(t,k,int(bool(r.get('ok'))),_json(r),_now()))
    def _result(self,t,r):
        if 'state' in r: self.save_state(t,r['state'])
        return r
    def configure_runtime(self,t,c): r=runtime.returns_reverse_logistics_configure_runtime(self.load_state(t),c); self._form(t,'returns_configuration','configure_runtime',None,c,r); return self._result(t,r)
    def set_parameter(self,t,n,v): r=runtime.returns_reverse_logistics_set_parameter(self.load_state(t),n,v); self._form(t,'returns_parameter','set_parameter',n,{'name':n,'value':v},r); return self._result(t,r)
    def register_rule(self,t,rule): r=runtime.returns_reverse_logistics_register_rule(self.load_state(t),rule); self._form(t,'return_rule','register_rule',rule.get('rule_id'),rule,r); return self._result(t,r)
    def receive_event(self,t,e): r=runtime.returns_reverse_logistics_receive_event(self.load_state(t),e); self._form(t,'return_event_inbox','receive_event',e.get('event_id'),e,r); return self._result(t,r)
    def authorize_return(self,t,p): r=runtime.returns_reverse_logistics_authorize_return(self.load_state(t),p); self._form(t,'return_authorization','authorize_return',p.get('return_id'),p,r); return self._result(t,r)
    def create_return_label(self,t,p): r=runtime.returns_reverse_logistics_create_return_label(self.load_state(t),p); self._form(t,'return_label','create_return_label',p.get('label_id'),p,r); return self._result(t,r)
    def record_return_receipt(self,t,p): r=runtime.returns_reverse_logistics_record_return_receipt(self.load_state(t),p); self._workflow(t,'receipt_inspection_disposition',p.get('return_id'),p,r); return self._result(t,r)
    def record_inspection_grade(self,t,p): r=runtime.returns_reverse_logistics_record_inspection_grade(self.load_state(t),p); self._workflow(t,'receipt_inspection_disposition',p.get('return_id'),p,r); return self._result(t,r)
    def resolve_disposition(self,t,return_id,destination_site='restock_dc'): r=runtime.returns_reverse_logistics_resolve_disposition(self.load_state(t),return_id,destination_site=destination_site); self._workflow(t,'receipt_inspection_disposition',return_id,{'destination_site':destination_site},r); return self._result(t,r)
    def issue_credit_adjustment(self,t,p): r=runtime.returns_reverse_logistics_issue_credit_adjustment(self.load_state(t),p); self._form(t,'credit_adjustment','issue_credit_adjustment',p.get('adjustment_id'),p,r); return self._result(t,r)
    def register_exchange_resolution(self,t,return_id,resolution_mode): r=runtime.returns_reverse_logistics_register_exchange_resolution(self.load_state(t),return_id,resolution_mode=resolution_mode); self._workflow(t,'refund_exchange_and_claim',return_id,{'resolution_mode':resolution_mode},r); return self._result(t,r)
    def open_carrier_claim(self,t,return_id,claim_reason): r=runtime.returns_reverse_logistics_open_carrier_claim(self.load_state(t),return_id,claim_reason=claim_reason); self._form(t,'carrier_claim','open_carrier_claim',return_id,{'claim_reason':claim_reason},r); return self._result(t,r)
    def open_exception_case(self,t,return_id,exception_type,severity,owner): r=runtime.returns_reverse_logistics_open_exception_case(self.load_state(t),return_id,exception_type=exception_type,severity=severity,owner=owner); self._form(t,'exception_case','open_exception_case',return_id,{'exception_type':exception_type,'severity':severity,'owner':owner},r); return self._result(t,r)
    def generate_return_proof(self,t,return_id,disclosure):
        r=runtime.returns_reverse_logistics_generate_return_proof(self.load_state(t),return_id,disclosure=tuple(disclosure)); r={'ok': bool(r.get('proof_hash')), **r}; self._control(t,'return_proof',r); self.connection.commit(); return r
    def run_control_tests(self,t): r=runtime.returns_reverse_logistics_run_control_tests(self.load_state(t)); self._control(t,'returns_release_controls',r); self.connection.commit(); return r
    def run_agent_skill(self,t,skill,payload):
        from . import agent
        plan=agent.document_instruction_plan(payload.get('document'),payload.get('instructions')); r={'ok':plan['ok'],'skill_name':skill,'plan':plan,'requires_confirmation':True}; self._insert(AGENT_TABLE,'agent',(t,skill,payload.get('scope','returns'),1,_json(payload),_json(r),_now())); self.connection.commit(); return r
    def build_workbench(self,t): return {'ok':True,**runtime.returns_reverse_logistics_build_workbench_view(self.load_state(t),tenant=t),'activity_counts':self.activity_counts(t),'read_model':self.read_model(t)}
    def read_model(self,t):
        row=self.connection.execute(f"SELECT * FROM {READ_MODEL_TABLE} WHERE tenant=?",(t,)).fetchone()
        if not row: return {'ok':False,'tenant':t,'reason':'read_model_not_found'}
        d=dict(row); d['payload']=_load(d.pop('payload_json')); d['ok']=True; return d
    def activity_counts(self,t): return {'forms':self.connection.execute(f"SELECT COUNT(*) FROM {FORM_TABLE} WHERE tenant=?",(t,)).fetchone()[0],'workflows':self.connection.execute(f"SELECT COUNT(*) FROM {WORKFLOW_TABLE} WHERE tenant=?",(t,)).fetchone()[0],'controls':self.connection.execute(f"SELECT COUNT(*) FROM {CONTROL_TABLE} WHERE tenant=?",(t,)).fetchone()[0],'agent_sessions':self.connection.execute(f"SELECT COUNT(*) FROM {AGENT_TABLE} WHERE tenant=?",(t,)).fetchone()[0]}
    def seed_demo_workspace(self,tenant='tenant_demo'):
        b=seed_data.standalone_seed_bundle(tenant); self.configure_runtime(tenant,b['configuration']); [self.set_parameter(tenant,k,v) for k,v in b['parameters'].items()]; self.register_rule(tenant,b['rule']); self.receive_event(tenant,b['order_event']); self.receive_event(tenant,b['payment_event']); self.receive_event(tenant,b['invalid_event']); self.authorize_return(tenant,b['return_authorization']); self.create_return_label(tenant,b['label']); self.record_return_receipt(tenant,b['receipt']); self.record_inspection_grade(tenant,b['inspection']); self.resolve_disposition(tenant,b['return_authorization']['return_id']); credit=self.issue_credit_adjustment(tenant,b['credit']); self.register_exchange_resolution(tenant,b['return_authorization']['return_id'],b['resolution_mode']); self.open_carrier_claim(tenant,b['return_authorization']['return_id'],b['claim_reason']); self.open_exception_case(tenant,b['return_authorization']['return_id'],b['exception']['exception_type'],b['exception']['severity'],b['exception']['owner']); controls=self.run_control_tests(tenant); proof=self.generate_return_proof(tenant,b['return_authorization']['return_id'],('return_id','order_id','status')); agent=self.run_agent_skill(tenant,'returns_reverse_logistics.document_instruction_intake',{'document':b['document'],'instructions':b['instructions'],'scope':'seed'}); return {'ok':credit['ok'] and controls['ok'] and proof['ok'] and agent['ok'],'tenant':tenant,'bundle':b,'workbench':self.build_workbench(tenant)}

def standalone_repository_contract(): return {'format':'appgen.returns-reverse-logistics-standalone-repository.v1','ok':True,'pbc':PBC_KEY,'repository_class':'ReturnsReverseLogisticsStandaloneRepository','local_harness_backend':'sqlite3','deployment_database_backends':runtime.RETURNS_REVERSE_LOGISTICS_ALLOWED_DATABASE_BACKENDS,'tables':(STATE_TABLE,FORM_TABLE,WORKFLOW_TABLE,CONTROL_TABLE,AGENT_TABLE,READ_MODEL_TABLE),'side_effects':()}
def standalone_repository_smoke_test():
    repo=ReturnsReverseLogisticsStandaloneRepository()
    try:
        seeded=repo.seed_demo_workspace(); return {'ok':seeded['ok'] and repo.read_model('tenant_demo')['ok'],'seeded':seeded,'contract':standalone_repository_contract(),'side_effects':()}
    finally: repo.close()
