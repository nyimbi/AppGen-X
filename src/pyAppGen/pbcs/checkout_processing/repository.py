"""Package-local persistence for the standalone Checkout Processing application."""
from __future__ import annotations
import json, sqlite3
from pathlib import Path
from typing import Any
from . import runtime, seed_data
PBC_KEY='checkout_processing'
STATE_TABLE='checkout_processing_runtime_state'; FORM_TABLE='checkout_processing_form_submission'; WORKFLOW_TABLE='checkout_processing_workflow_run'; CONTROL_TABLE='checkout_processing_control_execution'; AGENT_TABLE='checkout_processing_agent_session'; READ_MODEL_TABLE='checkout_processing_workbench_read_model'
_SCHEMA=f"""
CREATE TABLE IF NOT EXISTS {STATE_TABLE} (tenant TEXT PRIMARY KEY, state_json TEXT NOT NULL, updated_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS {FORM_TABLE} (submission_id TEXT PRIMARY KEY, tenant TEXT NOT NULL, form_key TEXT NOT NULL, action TEXT NOT NULL, subject_id TEXT, payload_json TEXT NOT NULL, result_json TEXT NOT NULL, created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS {WORKFLOW_TABLE} (workflow_run_id TEXT PRIMARY KEY, tenant TEXT NOT NULL, wizard_key TEXT NOT NULL, subject_id TEXT, status TEXT NOT NULL, context_json TEXT NOT NULL, result_json TEXT NOT NULL, created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS {CONTROL_TABLE} (control_run_id TEXT PRIMARY KEY, tenant TEXT NOT NULL, control_key TEXT NOT NULL, allowed INTEGER NOT NULL, result_json TEXT NOT NULL, created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS {AGENT_TABLE} (session_id TEXT PRIMARY KEY, tenant TEXT NOT NULL, skill_name TEXT NOT NULL, scope TEXT NOT NULL, requires_confirmation INTEGER NOT NULL, payload_json TEXT NOT NULL, result_json TEXT NOT NULL, created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS {READ_MODEL_TABLE} (read_model_id TEXT PRIMARY KEY, tenant TEXT NOT NULL, cart_count INTEGER NOT NULL, cart_line_count INTEGER NOT NULL, completed_checkout_count INTEGER NOT NULL, confirmed_inventory_count INTEGER NOT NULL, captured_payment_count INTEGER NOT NULL, promotion_redemption_count INTEGER NOT NULL, payload_json TEXT NOT NULL, updated_at TEXT NOT NULL);
"""
def _json(v:Any)->str: return json.dumps(v, sort_keys=True, default=str)
def _load(v:str|None)->Any: return None if v is None else json.loads(v)
def _now()->str: return 'local-harness-clock'
class CheckoutProcessingStandaloneRepository:
    """Persists a one-PBC checkout workspace with forms, workflows, controls, and agent sessions."""
    def __init__(self,database_path=':memory:'):
        self.database_path=database_path
        if database_path!=':memory:': Path(database_path).expanduser().resolve().parent.mkdir(parents=True,exist_ok=True)
        self.connection=sqlite3.connect(database_path); self.connection.row_factory=sqlite3.Row; self.apply_migrations()
    def close(self): self.connection.close()
    def apply_migrations(self): self.connection.executescript(_SCHEMA); self.connection.commit(); return (STATE_TABLE,FORM_TABLE,WORKFLOW_TABLE,CONTROL_TABLE,AGENT_TABLE,READ_MODEL_TABLE)
    def load_state(self,tenant):
        row=self.connection.execute(f'SELECT state_json FROM {STATE_TABLE} WHERE tenant=?',(tenant,)).fetchone()
        return _load(row['state_json']) if row else runtime.checkout_processing_empty_state()
    def save_state(self,tenant,state):
        self.connection.execute(f'INSERT INTO {STATE_TABLE} VALUES (?,?,?) ON CONFLICT(tenant) DO UPDATE SET state_json=excluded.state_json, updated_at=excluded.updated_at',(tenant,_json(state),_now()))
        self._sync_read_model(tenant,state); self.connection.commit(); return {'ok':True,'tenant':tenant}
    def _sync_read_model(self,tenant,state):
        view=runtime.checkout_processing_build_workbench_view(state,tenant=tenant) if state.get('configuration') else {'ok':True,'tenant':tenant}
        row={'read_model_id':f'{tenant}:workbench','tenant':tenant,'cart_count':int(view.get('cart_count',0)),'cart_line_count':int(view.get('cart_line_count',0)),'completed_checkout_count':int(view.get('completed_checkout_count',0)),'confirmed_inventory_count':int(view.get('confirmed_inventory_count',0)),'captured_payment_count':int(view.get('captured_payment_count',0)),'promotion_redemption_count':int(view.get('promotion_redemption_count',0)),'payload_json':_json(view),'updated_at':_now()}
        self.connection.execute(f'DELETE FROM {READ_MODEL_TABLE} WHERE tenant=?',(tenant,)); self.connection.execute(f"INSERT INTO {READ_MODEL_TABLE} ({', '.join(row)}) VALUES ({', '.join('?' for _ in row)})",tuple(row.values()))
    def _insert(self,table,prefix,fields):
        n=self.connection.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0]; self.connection.execute(f"INSERT INTO {table} VALUES ({', '.join('?' for _ in range(len(fields)+1))})",(f'{prefix}_{n+1:05d}',*fields))
    def _form(self,t,k,a,s,p,r): self._insert(FORM_TABLE,'form',(t,k,a,s,_json(p),_json(r),_now()))
    def _workflow(self,t,k,s,c,r): self._insert(WORKFLOW_TABLE,'workflow',(t,k,s,'completed' if r.get('ok') else 'blocked',_json(c),_json(r),_now()))
    def _control(self,t,k,r): self._insert(CONTROL_TABLE,'control',(t,k,int(bool(r.get('ok'))),_json(r),_now()))
    def _result(self,t,r):
        if r.get('ok') is True and 'state' in r: self.save_state(t,r['state'])
        return r
    def configure_runtime(self,t,c):
        norm={**c,'supported_shipping_options':tuple(c.get('supported_shipping_options',())),'supported_payment_methods':tuple(c.get('supported_payment_methods',()))}
        r=runtime.checkout_processing_configure_runtime(self.load_state(t),norm); self._form(t,'CheckoutConfigurationForm','configure_runtime',None,c,r); return self._result(t,r)
    def set_parameter(self,t,n,v): r=runtime.checkout_processing_set_parameter(self.load_state(t),n,v); self._form(t,'CheckoutParameterForm','set_parameter',n,{'name':n,'value':v},r); return self._result(t,r)
    def register_rule(self,t,rule): r=runtime.checkout_processing_register_rule(self.load_state(t),rule); self._form(t,'CheckoutRuleForm','register_rule',rule.get('rule_id'),rule,r); return self._result(t,r)
    def receive_event(self,t,e): r=runtime.checkout_processing_receive_event(self.load_state(t),e); self._form(t,'CheckoutEventInboxForm','receive_event',e.get('event_id'),e,r); return self._result(t,r)
    def create_cart(self,t,c): r=runtime.checkout_processing_create_cart(self.load_state(t),c); self._form(t,'CartForm','create_cart',c.get('cart_id'),c,r); return self._result(t,r)
    def add_cart_line(self,t,l): r=runtime.checkout_processing_add_cart_line(self.load_state(t),l); self._form(t,'CartLineForm','add_cart_line',l.get('line_id'),l,r); return self._result(t,r)
    def apply_coupon(self,t,cart_id,coupon): r=runtime.checkout_processing_apply_coupon(self.load_state(t),cart_id,coupon); self._workflow(t,'PromotionRedemptionWizard',cart_id,coupon,r); return self._result(t,r)
    def validate_shipping_address(self,t,cart_id,address): r=runtime.checkout_processing_validate_shipping_address(self.load_state(t),cart_id,address); self._workflow(t,'ShippingAddressWizard',cart_id,address,r); return self._result(t,r)
    def open_checkout_session(self,t,s): r=runtime.checkout_processing_open_checkout_session(self.load_state(t),s); self._workflow(t,'CheckoutSessionWizard',s.get('session_id'),s,r); return self._result(t,r)
    def apply_pricing_handoff(self,t,session_id,h): r=runtime.checkout_processing_apply_pricing_handoff(self.load_state(t),session_id,h); self._workflow(t,'PricingTaxHandoffWizard',session_id,h,r); return self._result(t,r)
    def apply_tax_handoff(self,t,session_id,h): r=runtime.checkout_processing_apply_tax_handoff(self.load_state(t),session_id,h); self._workflow(t,'PricingTaxHandoffWizard',session_id,h,r); return self._result(t,r)
    def reserve_inventory_handoff(self,t,session_id,h): r=runtime.checkout_processing_reserve_inventory_handoff(self.load_state(t),session_id,h); self._workflow(t,'InventoryReservationWizard',session_id,h,r); return self._result(t,r)
    def confirm_inventory_reservation(self,t,session_id): r=runtime.checkout_processing_confirm_inventory_reservation(self.load_state(t),session_id); self._workflow(t,'InventoryReservationWizard',session_id,{},r); return self._result(t,r)
    def screen_risk(self,t,session_id,signals): r=runtime.checkout_processing_screen_risk(self.load_state(t),session_id,signals); self._workflow(t,'RiskScreenWizard',session_id,signals,r); return self._result(t,r)
    def create_payment_intent(self,t,session_id,p): r=runtime.checkout_processing_create_payment_intent(self.load_state(t),session_id,p); self._workflow(t,'PaymentIntentWizard',session_id,p,r); return self._result(t,r)
    def authorize_payment_intent(self,t,session_id,authorization_id): r=runtime.checkout_processing_authorize_payment_intent(self.load_state(t),session_id,authorization_id=authorization_id); self._workflow(t,'PaymentIntentWizard',session_id,{'authorization_id':authorization_id},r); return self._result(t,r)
    def capture_payment_intent(self,t,session_id,capture_id): r=runtime.checkout_processing_capture_payment_intent(self.load_state(t),session_id,capture_id=capture_id); self._workflow(t,'PaymentIntentWizard',session_id,{'capture_id':capture_id},r); return self._result(t,r)
    def complete_checkout(self,t,session_id): r=runtime.checkout_processing_complete_checkout(self.load_state(t),session_id); self._workflow(t,'CheckoutCompletionWizard',session_id,{},r); return self._result(t,r)
    def generate_checkout_proof(self,t,session_id,disclosure): r=runtime.checkout_processing_generate_checkout_proof(self.load_state(t),session_id,disclosure=tuple(disclosure)); self._control(t,'checkout_proof',r); self.connection.commit(); return r
    def run_control_tests(self,t): r=runtime.checkout_processing_run_control_tests(self.load_state(t)); self._control(t,'checkout_release_controls',r); self.connection.commit(); return r
    def run_agent_skill(self,t,skill,payload):
        from . import agent
        plan=agent.document_instruction_plan(payload.get('document'),payload.get('instructions')); r={'ok':plan['ok'],'skill_name':skill,'plan':plan,'requires_confirmation':True}; n=self.connection.execute(f'SELECT COUNT(*) FROM {AGENT_TABLE}').fetchone()[0]; self.connection.execute(f'INSERT INTO {AGENT_TABLE} VALUES (?,?,?,?,?,?,?,?)',(f'agent_{n+1:05d}',t,skill,payload.get('scope','checkout'),1,_json(payload),_json(r),_now())); self.connection.commit(); return r
    def build_workbench(self,t): st=self.load_state(t); return {'ok':True,**runtime.checkout_processing_build_workbench_view(st,tenant=t),'activity_counts':self.activity_counts(t),'read_model':self.read_model(t)}
    def read_model(self,t):
        row=self.connection.execute(f'SELECT * FROM {READ_MODEL_TABLE} WHERE tenant=?',(t,)).fetchone()
        if not row: return {'ok':False,'tenant':t,'reason':'read_model_not_found'}
        d=dict(row); d['payload']=_load(d.pop('payload_json')); d['ok']=True; return d
    def activity_counts(self,t): return {'forms':self.connection.execute(f'SELECT COUNT(*) FROM {FORM_TABLE} WHERE tenant=?',(t,)).fetchone()[0],'workflows':self.connection.execute(f'SELECT COUNT(*) FROM {WORKFLOW_TABLE} WHERE tenant=?',(t,)).fetchone()[0],'controls':self.connection.execute(f'SELECT COUNT(*) FROM {CONTROL_TABLE} WHERE tenant=?',(t,)).fetchone()[0],'agent_sessions':self.connection.execute(f'SELECT COUNT(*) FROM {AGENT_TABLE} WHERE tenant=?',(t,)).fetchone()[0]}
    def seed_demo_workspace(self,tenant='tenant_demo'):
        b=seed_data.standalone_seed_bundle(tenant=tenant); self.configure_runtime(tenant,b['configuration']); [self.set_parameter(tenant,k,v) for k,v in b['parameters'].items()]; [self.register_rule(tenant,r) for r in b['rules']]; [self.receive_event(tenant,e) for e in b['events']]; self.create_cart(tenant,b['cart']); self.add_cart_line(tenant,b['cart_line']); self.apply_coupon(tenant,b['cart']['cart_id'],b['coupon']); self.validate_shipping_address(tenant,b['cart']['cart_id'],b['address']); self.open_checkout_session(tenant,b['session']); self.apply_pricing_handoff(tenant,b['session']['session_id'],b['pricing_handoff']); self.apply_tax_handoff(tenant,b['session']['session_id'],b['tax_quote']); self.reserve_inventory_handoff(tenant,b['session']['session_id'],b['inventory_reservation']); self.confirm_inventory_reservation(tenant,b['session']['session_id']); self.screen_risk(tenant,b['session']['session_id'],b['risk_signals']); self.create_payment_intent(tenant,b['session']['session_id'],b['payment_intent']); self.authorize_payment_intent(tenant,b['session']['session_id'],'auth_demo_100'); self.capture_payment_intent(tenant,b['session']['session_id'],'capture_demo_100'); completed=self.complete_checkout(tenant,b['session']['session_id']); controls=self.run_control_tests(tenant); proof=self.generate_checkout_proof(tenant,b['session']['session_id'],('session_id','order_id','status','total')); agent=self.run_agent_skill(tenant,'checkout_processing.document_instruction_intake',{'document':b['document'],'instructions':b['instructions'],'scope':'seed'}); return {'ok':completed['ok'] and controls['ok'] and proof['ok'] and agent['ok'],'tenant':tenant,'bundle':b,'workbench':self.build_workbench(tenant)}

def standalone_repository_contract(): return {'format':'appgen.checkout-processing-standalone-repository.v1','ok':True,'pbc':PBC_KEY,'repository_class':'CheckoutProcessingStandaloneRepository','local_harness_backend':'sqlite3','deployment_database_backends':runtime.CHECKOUT_PROCESSING_ALLOWED_DATABASE_BACKENDS,'tables':(STATE_TABLE,FORM_TABLE,WORKFLOW_TABLE,CONTROL_TABLE,AGENT_TABLE,READ_MODEL_TABLE),'side_effects':()}
def standalone_repository_smoke_test():
    repo=CheckoutProcessingStandaloneRepository()
    try:
        seeded=repo.seed_demo_workspace(); return {'ok':seeded['ok'] and repo.read_model('tenant_demo')['ok'],'seeded':seeded,'contract':standalone_repository_contract(),'side_effects':()}
    finally: repo.close()
