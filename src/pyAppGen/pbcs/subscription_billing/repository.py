"""Package-local persistence for the standalone Subscription Billing app."""
from __future__ import annotations
import json, sqlite3
from pathlib import Path
from typing import Any
from . import runtime, seed_data
PBC_KEY="subscription_billing"
STATE_TABLE="subscription_billing_runtime_state"; FORM_TABLE="subscription_billing_form_submission"; WORKFLOW_TABLE="subscription_billing_workflow_run"; CONTROL_TABLE="subscription_billing_control_execution"; AGENT_TABLE="subscription_billing_agent_session"; READ_MODEL_TABLE="subscription_billing_workbench_read_model"
_SCHEMA=f"""
CREATE TABLE IF NOT EXISTS {STATE_TABLE} (tenant TEXT PRIMARY KEY, state_json TEXT NOT NULL, updated_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS {FORM_TABLE} (submission_id TEXT PRIMARY KEY, tenant TEXT NOT NULL, form_key TEXT NOT NULL, action TEXT NOT NULL, subject_id TEXT, payload_json TEXT NOT NULL, result_json TEXT NOT NULL, created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS {WORKFLOW_TABLE} (workflow_run_id TEXT PRIMARY KEY, tenant TEXT NOT NULL, wizard_key TEXT NOT NULL, subject_id TEXT, status TEXT NOT NULL, context_json TEXT NOT NULL, result_json TEXT NOT NULL, created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS {CONTROL_TABLE} (control_run_id TEXT PRIMARY KEY, tenant TEXT NOT NULL, control_key TEXT NOT NULL, allowed INTEGER NOT NULL, result_json TEXT NOT NULL, created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS {AGENT_TABLE} (session_id TEXT PRIMARY KEY, tenant TEXT NOT NULL, skill_name TEXT NOT NULL, scope TEXT NOT NULL, requires_confirmation INTEGER NOT NULL, payload_json TEXT NOT NULL, result_json TEXT NOT NULL, created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS {READ_MODEL_TABLE} (read_model_id TEXT PRIMARY KEY, tenant TEXT NOT NULL, subscription_count INTEGER NOT NULL, invoice_count INTEGER NOT NULL, paid_invoice_count INTEGER NOT NULL, usage_count INTEGER NOT NULL, credit_memo_count INTEGER NOT NULL, payment_application_count INTEGER NOT NULL, entitlement_count INTEGER NOT NULL, revenue_schedule_count INTEGER NOT NULL, exception_count INTEGER NOT NULL, payload_json TEXT NOT NULL, updated_at TEXT NOT NULL);
"""
def _default(v:Any):
    if isinstance(v,set): return sorted(v)
    return str(v)
def _json(v:Any)->str: return json.dumps(v, sort_keys=True, default=_default)
def _load(v:str|None)->Any:
    data=None if v is None else json.loads(v)
    if isinstance(data,dict) and isinstance(data.get('handled_events'),list): data['handled_events']=set(data['handled_events'])
    return data
def _now()->str: return "local-harness-clock"
class SubscriptionBillingStandaloneRepository:
    def __init__(self,database_path=':memory:'):
        self.database_path=database_path
        if database_path != ':memory:': Path(database_path).expanduser().resolve().parent.mkdir(parents=True, exist_ok=True)
        self.connection=sqlite3.connect(database_path); self.connection.row_factory=sqlite3.Row; self.apply_migrations()
    def close(self): self.connection.close()
    def apply_migrations(self): self.connection.executescript(_SCHEMA); self.connection.commit(); return (STATE_TABLE,FORM_TABLE,WORKFLOW_TABLE,CONTROL_TABLE,AGENT_TABLE,READ_MODEL_TABLE)
    def load_state(self,tenant):
        row=self.connection.execute(f"SELECT state_json FROM {STATE_TABLE} WHERE tenant=?",(tenant,)).fetchone()
        return _load(row['state_json']) if row else runtime.subscription_billing_empty_state()
    def save_state(self,tenant,state):
        self.connection.execute(f"INSERT INTO {STATE_TABLE} VALUES (?,?,?) ON CONFLICT(tenant) DO UPDATE SET state_json=excluded.state_json, updated_at=excluded.updated_at",(tenant,_json(state),_now()))
        self._sync_read_model(tenant,state); self.connection.commit(); return {'ok':True,'tenant':tenant}
    def _sync_read_model(self,tenant,state):
        view=runtime.subscription_billing_build_workbench_view(state,tenant=tenant) if state.get('configuration') else {'ok':True,'tenant':tenant}
        row={'read_model_id':f'{tenant}:workbench','tenant':tenant,'subscription_count':int(view.get('subscription_count',0)),'invoice_count':int(view.get('invoice_count',0)),'paid_invoice_count':int(view.get('paid_invoice_count',0)),'usage_count':int(view.get('usage_count',0)),'credit_memo_count':int(view.get('credit_memo_count',0)),'payment_application_count':int(view.get('payment_application_count',0)),'entitlement_count':int(view.get('entitlement_count',0)),'revenue_schedule_count':int(view.get('revenue_schedule_count',0)),'exception_count':int(view.get('exception_count',0)),'payload_json':_json(view),'updated_at':_now()}
        self.connection.execute(f"DELETE FROM {READ_MODEL_TABLE} WHERE tenant=?",(tenant,)); self.connection.execute(f"INSERT INTO {READ_MODEL_TABLE} ({', '.join(row)}) VALUES ({', '.join('?' for _ in row)})",tuple(row.values()))
    def _insert(self,table,prefix,fields):
        n=self.connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]; self.connection.execute(f"INSERT INTO {table} VALUES ({', '.join('?' for _ in range(len(fields)+1))})",(f'{prefix}_{n+1:05d}',*fields))
    def _form(self,t,k,a,s,p,r): self._insert(FORM_TABLE,'form',(t,k,a,s,_json(p),_json(r),_now()))
    def _workflow(self,t,k,s,c,r): self._insert(WORKFLOW_TABLE,'workflow',(t,k,s,'completed' if r.get('ok') else 'blocked',_json(c),_json(r),_now()))
    def _control(self,t,k,r): self._insert(CONTROL_TABLE,'control',(t,k,int(bool(r.get('ok'))),_json(r),_now()))
    def _result(self,t,r):
        if 'state' in r: self.save_state(t,r['state'])
        return r
    def configure_runtime(self,t,c): r=runtime.subscription_billing_configure_runtime(self.load_state(t),c); self._form(t,'billing_configuration','configure_runtime',None,c,r); return self._result(t,r)
    def set_parameter(self,t,n,v): r=runtime.subscription_billing_set_parameter(self.load_state(t),n,v); self._form(t,'billing_parameter','set_parameter',n,{'name':n,'value':v},r); return self._result(t,r)
    def register_rule(self,t,rule): r=runtime.subscription_billing_register_rule(self.load_state(t),rule); self._form(t,'billing_rule','register_rule',rule.get('rule_id'),rule,r); return self._result(t,r)
    def register_plan(self,t,p): r=runtime.subscription_billing_register_plan(self.load_state(t),p); self._form(t,'plan_catalog','register_plan',p.get('plan_id'),p,r); return self._result(t,r)
    def start_trial(self,t,c): r=runtime.subscription_billing_start_trial(self.load_state(t),c); self._workflow(t,'subscription_launch',c.get('trial_id'),c,r); return self._result(t,r)
    def create_subscription(self,t,c): r=runtime.subscription_billing_create_subscription(self.load_state(t),c); self._form(t,'subscription','create_subscription',c.get('subscription_id'),c,r); return self._result(t,r)
    def add_subscription_addon(self,t,a): r=runtime.subscription_billing_add_subscription_addon(self.load_state(t),a); self._workflow(t,'subscription_launch',a.get('subscription_id'),a,r); return self._result(t,r)
    def record_usage(self,t,u): r=runtime.subscription_billing_record_usage(self.load_state(t),u); self._form(t,'usage_meter','record_usage',u.get('usage_id'),u,r); return self._result(t,r)
    def generate_invoice(self,t,subscription_id,period): r=runtime.subscription_billing_generate_invoice(self.load_state(t),subscription_id,period=period); self._workflow(t,'usage_to_invoice',subscription_id,{'period':period},r); return self._result(t,r)
    def issue_credit_memo(self,t,invoice_id,amount,reason): r=runtime.subscription_billing_issue_credit_memo(self.load_state(t),invoice_id,amount=amount,reason=reason); self._form(t,'credit_memo','issue_credit_memo',invoice_id,{'amount':amount,'reason':reason},r); return self._result(t,r)
    def apply_payment_to_invoice(self,t,invoice_id,payment_event_id,amount): r=runtime.subscription_billing_apply_payment_to_invoice(self.load_state(t),invoice_id,payment_event_id=payment_event_id,amount=amount); self._form(t,'payment_application','apply_payment_to_invoice',invoice_id,{'payment_event_id':payment_event_id,'amount':amount},r); return self._result(t,r)
    def grant_entitlement(self,t,subscription_id,entitlement_key,scope): r=runtime.subscription_billing_grant_entitlement(self.load_state(t),subscription_id,entitlement_key=entitlement_key,scope=scope); self._workflow(t,'usage_to_invoice',subscription_id,{'entitlement_key':entitlement_key,'scope':scope},r); return self._result(t,r)
    def recognize_revenue(self,t,invoice_id,period): r=runtime.subscription_billing_recognize_revenue(self.load_state(t),invoice_id,period=period); self._workflow(t,'usage_to_invoice',invoice_id,{'period':period},r); return self._result(t,r)
    def change_subscription_plan(self,t,subscription_id,target_plan_id,effective_date,reason): r=runtime.subscription_billing_change_subscription_plan(self.load_state(t),subscription_id,target_plan_id=target_plan_id,effective_date=effective_date,reason=reason); self._form(t,'subscription_change','change_subscription_plan',subscription_id,{'target_plan_id':target_plan_id,'effective_date':effective_date,'reason':reason},r); return self._result(t,r)
    def open_billing_exception(self,t,subscription_id,exception_type,severity,description): r=runtime.subscription_billing_open_billing_exception(self.load_state(t),subscription_id,exception_type=exception_type,severity=severity,description=description); self._workflow(t,'credit_and_dunning',subscription_id,{'exception_type':exception_type,'severity':severity,'description':description},r); return self._result(t,r)
    def resolve_billing_exception(self,t,exception_id,resolution): r=runtime.subscription_billing_resolve_billing_exception(self.load_state(t),exception_id,resolution=resolution); self._workflow(t,'credit_and_dunning',exception_id,{'resolution':resolution},r); return self._result(t,r)
    def create_dunning_notice(self,t,subscription_id,reason): r=runtime.subscription_billing_create_dunning_notice(self.load_state(t),subscription_id,reason=reason); self._form(t,'dunning_notice','create_dunning_notice',subscription_id,{'reason':reason},r); return self._result(t,r)
    def cancel_subscription(self,t,subscription_id,effective_date,reason): r=runtime.subscription_billing_cancel_subscription(self.load_state(t),subscription_id,effective_date=effective_date,reason=reason); self._workflow(t,'subscription_change',subscription_id,{'effective_date':effective_date,'reason':reason},r); return self._result(t,r)
    def receive_event(self,t,e,simulate_failure=False): r=runtime.subscription_billing_receive_event(self.load_state(t),e,simulate_failure=simulate_failure); self._form(t,'billing_event_inbox','receive_event',e.get('event_id'),{**e,'simulate_failure':simulate_failure},r); return self._result(t,r) if r.get('state') else r
    def run_control_tests(self,t): r=runtime.subscription_billing_run_control_tests(self.load_state(t)); self._control(t,'billing_release_controls',r); self.connection.commit(); return r
    def run_agent_skill(self,t,skill,payload):
        from . import agent
        plan=agent.document_instruction_plan(payload.get('document'),payload.get('instructions')); r={'ok':plan['ok'],'skill_name':skill,'plan':plan,'requires_confirmation':True}; self._insert(AGENT_TABLE,'agent',(t,skill,payload.get('scope','subscription'),1,_json(payload),_json(r),_now())); self.connection.commit(); return r
    def build_workbench(self,t): return {'ok':True,**runtime.subscription_billing_build_workbench_view(self.load_state(t),tenant=t),'activity_counts':self.activity_counts(t),'read_model':self.read_model(t)}
    def read_model(self,t):
        row=self.connection.execute(f"SELECT * FROM {READ_MODEL_TABLE} WHERE tenant=?",(t,)).fetchone()
        if not row: return {'ok':False,'tenant':t,'reason':'read_model_not_found'}
        d=dict(row); d['payload']=_load(d.pop('payload_json')); d['ok']=True; return d
    def activity_counts(self,t): return {'forms':self.connection.execute(f"SELECT COUNT(*) FROM {FORM_TABLE} WHERE tenant=?",(t,)).fetchone()[0],'workflows':self.connection.execute(f"SELECT COUNT(*) FROM {WORKFLOW_TABLE} WHERE tenant=?",(t,)).fetchone()[0],'controls':self.connection.execute(f"SELECT COUNT(*) FROM {CONTROL_TABLE} WHERE tenant=?",(t,)).fetchone()[0],'agent_sessions':self.connection.execute(f"SELECT COUNT(*) FROM {AGENT_TABLE} WHERE tenant=?",(t,)).fetchone()[0]}
    def seed_demo_workspace(self,tenant='tenant_demo'):
        b=seed_data.standalone_seed_bundle(tenant); self.configure_runtime(tenant,b['configuration']); [self.set_parameter(tenant,k,v) for k,v in b['parameters'].items()]; self.register_rule(tenant,b['rule']); [self.register_plan(tenant,p) for p in b['plans']]; self.start_trial(tenant,b['trial']); self.create_subscription(tenant,b['subscription']); self.add_subscription_addon(tenant,b['addon']); self.record_usage(tenant,b['usage']); invoice=self.generate_invoice(tenant,b['subscription']['subscription_id'],b['period']); invoice_id=invoice['invoice']['invoice_id']; self.issue_credit_memo(tenant,invoice_id,b['credit']['amount'],b['credit']['reason']); self.apply_payment_to_invoice(tenant,invoice_id,b['payment_event_id'],invoice['invoice']['amount']); self.grant_entitlement(tenant,b['subscription']['subscription_id'],b['entitlement_key'],tenant); self.recognize_revenue(tenant,invoice_id,b['period']); self.change_subscription_plan(tenant,b['subscription']['subscription_id'],b['change']['target_plan_id'],b['change']['effective_date'],b['change']['reason']); exc=self.open_billing_exception(tenant,b['subscription']['subscription_id'],b['exception']['exception_type'],b['exception']['severity'],b['exception']['description']); self.resolve_billing_exception(tenant,exc['exception']['exception_id'],'accepted'); self.create_dunning_notice(tenant,b['subscription']['subscription_id'],b['dunning_reason']); self.receive_event(tenant,{'event_id':'payment_capture_demo','event_type':'PaymentCaptured','payload':{'tenant':tenant,'invoice_id':invoice_id,'amount':invoice['invoice']['amount'],'currency':'USD'}}); self.receive_event(tenant,{'event_id':'payment_retry_demo','event_type':'PaymentCaptured','payload':{'tenant':tenant,'invoice_id':invoice_id,'amount':invoice['invoice']['amount'],'currency':'USD'}},simulate_failure=True); self.cancel_subscription(tenant,b['subscription']['subscription_id'],'2026-03-01','customer_request'); controls=self.run_control_tests(tenant); agent=self.run_agent_skill(tenant,'subscription_billing.document_instruction_intake',{'document':b['document'],'instructions':b['instructions'],'scope':'seed'}); return {'ok':controls['ok'] and agent['ok'],'tenant':tenant,'bundle':b,'workbench':self.build_workbench(tenant)}

def standalone_repository_contract(): return {'format':'appgen.subscription-billing-standalone-repository.v1','ok':True,'pbc':PBC_KEY,'repository_class':'SubscriptionBillingStandaloneRepository','local_harness_backend':'sqlite3','deployment_database_backends':runtime.SUBSCRIPTION_BILLING_ALLOWED_DATABASE_BACKENDS,'tables':(STATE_TABLE,FORM_TABLE,WORKFLOW_TABLE,CONTROL_TABLE,AGENT_TABLE,READ_MODEL_TABLE),'side_effects':()}
def standalone_repository_smoke_test():
    repo=SubscriptionBillingStandaloneRepository()
    try:
        seeded=repo.seed_demo_workspace(); return {'ok':seeded['ok'] and repo.read_model('tenant_demo')['ok'],'seeded':seeded,'contract':standalone_repository_contract(),'side_effects':()}
    finally: repo.close()
