"""Package-local persistence for the standalone Price Promotion Engine application."""
from __future__ import annotations
import json, sqlite3
from pathlib import Path
from typing import Any
from . import runtime, seed_data
PBC_KEY='price_promotion_engine'
STATE_TABLE='price_promotion_engine_runtime_state'; FORM_TABLE='price_promotion_engine_form_submission'; WORKFLOW_TABLE='price_promotion_engine_workflow_run'; CONTROL_TABLE='price_promotion_engine_control_execution'; AGENT_TABLE='price_promotion_engine_agent_session'; READ_MODEL_TABLE='price_promotion_engine_workbench_read_model'
_SCHEMA=f"""
CREATE TABLE IF NOT EXISTS {STATE_TABLE} (tenant TEXT PRIMARY KEY, state_json TEXT NOT NULL, updated_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS {FORM_TABLE} (submission_id TEXT PRIMARY KEY, tenant TEXT NOT NULL, form_key TEXT NOT NULL, action TEXT NOT NULL, subject_id TEXT, payload_json TEXT NOT NULL, result_json TEXT NOT NULL, created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS {WORKFLOW_TABLE} (workflow_run_id TEXT PRIMARY KEY, tenant TEXT NOT NULL, wizard_key TEXT NOT NULL, subject_id TEXT, status TEXT NOT NULL, context_json TEXT NOT NULL, result_json TEXT NOT NULL, created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS {CONTROL_TABLE} (control_run_id TEXT PRIMARY KEY, tenant TEXT NOT NULL, control_key TEXT NOT NULL, allowed INTEGER NOT NULL, result_json TEXT NOT NULL, created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS {AGENT_TABLE} (session_id TEXT PRIMARY KEY, tenant TEXT NOT NULL, skill_name TEXT NOT NULL, scope TEXT NOT NULL, requires_confirmation INTEGER NOT NULL, payload_json TEXT NOT NULL, result_json TEXT NOT NULL, created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS {READ_MODEL_TABLE} (read_model_id TEXT PRIMARY KEY, tenant TEXT NOT NULL, price_rule_count INTEGER NOT NULL, promotion_count INTEGER NOT NULL, decision_count INTEGER NOT NULL, approved_promotion_count INTEGER NOT NULL, coupon_redemption_count INTEGER NOT NULL, settlement_count INTEGER NOT NULL, payload_json TEXT NOT NULL, updated_at TEXT NOT NULL);
"""
def _json(v:Any)->str: return json.dumps(v, sort_keys=True, default=lambda o: tuple(sorted(o)) if isinstance(o,set) else str(o))
def _load(v:str|None)->Any: return None if v is None else json.loads(v)
def _now()->str: return 'local-harness-clock'
class PricePromotionEngineStandaloneRepository:
    def __init__(self,database_path=':memory:'):
        self.database_path=database_path
        if database_path!=':memory:': Path(database_path).expanduser().resolve().parent.mkdir(parents=True,exist_ok=True)
        self.connection=sqlite3.connect(database_path); self.connection.row_factory=sqlite3.Row; self.apply_migrations()
    def close(self): self.connection.close()
    def apply_migrations(self): self.connection.executescript(_SCHEMA); self.connection.commit(); return (STATE_TABLE,FORM_TABLE,WORKFLOW_TABLE,CONTROL_TABLE,AGENT_TABLE,READ_MODEL_TABLE)
    def load_state(self,tenant):
        row=self.connection.execute(f'SELECT state_json FROM {STATE_TABLE} WHERE tenant=?',(tenant,)).fetchone()
        if not row: return runtime.price_promotion_engine_empty_state()
        state=_load(row['state_json']); state['handled_events']=set(state.get('handled_events',())) if not isinstance(state.get('handled_events'),set) else state.get('handled_events'); return state
    def save_state(self,tenant,state):
        serial={**state,'handled_events':tuple(sorted(state.get('handled_events',())))}
        self.connection.execute(f'INSERT INTO {STATE_TABLE} VALUES (?,?,?) ON CONFLICT(tenant) DO UPDATE SET state_json=excluded.state_json, updated_at=excluded.updated_at',(tenant,_json(serial),_now()))
        self._sync_read_model(tenant,state); self.connection.commit(); return {'ok':True,'tenant':tenant}
    def _sync_read_model(self,tenant,state):
        view=runtime.price_promotion_engine_build_workbench_view(state,tenant=tenant) if state.get('configuration') else {'ok':True,'tenant':tenant}
        row={'read_model_id':f'{tenant}:workbench','tenant':tenant,'price_rule_count':int(view.get('price_rule_count',0)),'promotion_count':int(view.get('promotion_count',0)),'decision_count':int(view.get('price_decision_count',view.get('decision_count',0))),'approved_promotion_count':int(view.get('approved_promotion_count',0)),'coupon_redemption_count':int(view.get('coupon_redemption_count',0)),'settlement_count':int(view.get('promotion_settlement_count',0)),'payload_json':_json(view),'updated_at':_now()}
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
        norm={**c,'supported_currencies':tuple(c.get('supported_currencies',())),'supported_regions':tuple(c.get('supported_regions',())),'pricing_calendars':tuple(c.get('pricing_calendars',()))}
        r=runtime.price_promotion_engine_configure_runtime(self.load_state(t),norm); self._form(t,'PriceConfigurationForm','configure_runtime',None,c,r); return self._result(t,r)
    def set_parameter(self,t,n,v): r=runtime.price_promotion_engine_set_parameter(self.load_state(t),n,v); self._form(t,'PriceParameterForm','set_parameter',n,{'name':n,'value':v},r); return self._result(t,r)
    def register_rule(self,t,rule):
        norm={**rule,'allowed_currencies':tuple(rule.get('allowed_currencies',())),'allowed_regions':tuple(rule.get('allowed_regions',())),'allowed_segments':tuple(rule.get('allowed_segments',()))}
        r=runtime.price_promotion_engine_register_rule(self.load_state(t),norm); self._form(t,'PricePolicyRuleForm','register_rule',rule.get('rule_id'),rule,r); return self._result(t,r)
    def receive_event(self,t,e): r=runtime.price_promotion_engine_receive_event(self.load_state(t),e); self._form(t,'PriceEventInboxForm','receive_event',e.get('event_id'),e,r); return self._result(t,r)
    def register_price_rule(self,t,c): r=runtime.price_promotion_engine_register_price_rule(self.load_state(t),c); self._form(t,'PriceRuleForm','register_price_rule',c.get('price_rule_id'),c,r); return self._result(t,r)
    def register_price_agreement(self,t,c): r=runtime.price_promotion_engine_register_price_agreement(self.load_state(t),c); self._form(t,'PriceAgreementForm','register_price_agreement',c.get('agreement_id'),c,r); return self._result(t,r)
    def register_promotion(self,t,c): r=runtime.price_promotion_engine_register_promotion(self.load_state(t),c); self._form(t,'PromotionForm','register_promotion',c.get('promotion_id'),c,r); return self._result(t,r)
    def approve_promotion(self,t,promotion_id,approved_by): r=runtime.price_promotion_engine_approve_promotion(self.load_state(t),promotion_id,approved_by=approved_by); self._workflow(t,'PromotionApprovalWizard',promotion_id,{'approved_by':approved_by},r); return self._result(t,r)
    def register_loyalty_tier(self,t,c): r=runtime.price_promotion_engine_register_loyalty_tier(self.load_state(t),c); self._form(t,'LoyaltyTierForm','register_loyalty_tier',c.get('tier_id'),c,r); return self._result(t,r)
    def quote_price(self,t,c): r=runtime.price_promotion_engine_quote_price(self.load_state(t),c); self._workflow(t,'PriceQuoteWizard',c.get('decision_id'),c,r); return self._result(t,r)
    def redeem_coupon(self,t,decision_id,coupon_code): r=runtime.price_promotion_engine_redeem_coupon(self.load_state(t),decision_id,coupon_code); self._workflow(t,'CouponRedemptionWizard',decision_id,{'coupon_code':coupon_code},r); return self._result(t,r)
    def plan_trade_promotion(self,t,c): r=runtime.price_promotion_engine_plan_trade_promotion(self.load_state(t),c); self._workflow(t,'TradePromotionWizard',c.get('plan_id'),c,r); return self._result(t,r)
    def open_price_exception(self,t,c): r=runtime.price_promotion_engine_open_price_exception(self.load_state(t),c); self._workflow(t,'PriceExceptionWizard',c.get('exception_id'),c,r); return self._result(t,r)
    def accrue_promotion(self,t,decision_id,promotion_id): r=runtime.price_promotion_engine_accrue_promotion(self.load_state(t),decision_id,promotion_id); self._workflow(t,'PromotionSettlementWizard',decision_id,{'promotion_id':promotion_id},r); return self._result(t,r)
    def settle_promotion(self,t,accrual_id,settled_amount,settled_by): r=runtime.price_promotion_engine_settle_promotion(self.load_state(t),accrual_id,settled_amount=settled_amount,settled_by=settled_by); self._workflow(t,'PromotionSettlementWizard',accrual_id,{'settled_amount':settled_amount},r); return self._result(t,r)
    def run_control_tests(self,t): r=runtime.price_promotion_engine_build_release_evidence(); self._control(t,'price_release_controls',r); self.connection.commit(); return r
    def run_agent_skill(self,t,skill,payload):
        from . import agent
        plan=agent.document_instruction_plan(payload.get('document'),payload.get('instructions')); r={'ok':plan['ok'],'skill_name':skill,'plan':plan,'requires_confirmation':True}; n=self.connection.execute(f'SELECT COUNT(*) FROM {AGENT_TABLE}').fetchone()[0]; self.connection.execute(f'INSERT INTO {AGENT_TABLE} VALUES (?,?,?,?,?,?,?,?)',(f'agent_{n+1:05d}',t,skill,payload.get('scope','pricing'),1,_json(payload),_json(r),_now())); self.connection.commit(); return r
    def build_workbench(self,t): st=self.load_state(t); return {'ok':True,**runtime.price_promotion_engine_build_workbench_view(st,tenant=t),'activity_counts':self.activity_counts(t),'read_model':self.read_model(t)}
    def read_model(self,t):
        row=self.connection.execute(f'SELECT * FROM {READ_MODEL_TABLE} WHERE tenant=?',(t,)).fetchone()
        if not row: return {'ok':False,'tenant':t,'reason':'read_model_not_found'}
        d=dict(row); d['payload']=_load(d.pop('payload_json')); d['ok']=True; return d
    def activity_counts(self,t): return {'forms':self.connection.execute(f'SELECT COUNT(*) FROM {FORM_TABLE} WHERE tenant=?',(t,)).fetchone()[0],'workflows':self.connection.execute(f'SELECT COUNT(*) FROM {WORKFLOW_TABLE} WHERE tenant=?',(t,)).fetchone()[0],'controls':self.connection.execute(f'SELECT COUNT(*) FROM {CONTROL_TABLE} WHERE tenant=?',(t,)).fetchone()[0],'agent_sessions':self.connection.execute(f'SELECT COUNT(*) FROM {AGENT_TABLE} WHERE tenant=?',(t,)).fetchone()[0]}
    def seed_demo_workspace(self,tenant='tenant_demo'):
        b=seed_data.standalone_seed_bundle(tenant=tenant); self.configure_runtime(tenant,b['configuration']); [self.set_parameter(tenant,k,v) for k,v in b['parameters'].items()]; [self.register_rule(tenant,r) for r in b['rules']]; [self.receive_event(tenant,e) for e in b['events']]; self.register_price_rule(tenant,b['price_rule']); self.register_price_agreement(tenant,b['price_agreement']); self.register_promotion(tenant,b['promotion']); self.approve_promotion(tenant,b['promotion']['promotion_id'],'pricing_manager'); self.register_loyalty_tier(tenant,b['loyalty_tier']); quote=self.quote_price(tenant,b['quote']); redemption=self.redeem_coupon(tenant,b['quote']['decision_id'],b['promotion']['code']); self.plan_trade_promotion(tenant,b['trade_promotion_plan']); self.open_price_exception(tenant,b['price_exception']); accrual=self.accrue_promotion(tenant,b['quote']['decision_id'],b['promotion']['promotion_id']); self.settle_promotion(tenant,accrual['promotion_accrual']['accrual_id'],accrual['promotion_accrual']['accrual_amount'],'trade_finance'); controls=self.run_control_tests(tenant); agent=self.run_agent_skill(tenant,'price_promotion_engine.document_instruction_intake',{'document':b['document'],'instructions':b['instructions'],'scope':'seed'}); return {'ok':quote['ok'] and redemption['ok'] and controls['ok'] and agent['ok'],'tenant':tenant,'bundle':b,'workbench':self.build_workbench(tenant)}

def standalone_repository_contract(): return {'format':'appgen.price-promotion-engine-standalone-repository.v1','ok':True,'pbc':PBC_KEY,'repository_class':'PricePromotionEngineStandaloneRepository','local_harness_backend':'sqlite3','deployment_database_backends':runtime.PRICE_PROMOTION_ENGINE_ALLOWED_DATABASE_BACKENDS,'tables':(STATE_TABLE,FORM_TABLE,WORKFLOW_TABLE,CONTROL_TABLE,AGENT_TABLE,READ_MODEL_TABLE),'side_effects':()}
def standalone_repository_smoke_test():
    repo=PricePromotionEngineStandaloneRepository()
    try:
        seeded=repo.seed_demo_workspace(); return {'ok':seeded['ok'] and repo.read_model('tenant_demo')['ok'],'seeded':seeded,'contract':standalone_repository_contract(),'side_effects':()}
    finally: repo.close()
