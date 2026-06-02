"""Package-local persistence for the standalone Payment Orchestration app."""
from __future__ import annotations
import json, sqlite3
from pathlib import Path
from typing import Any
from . import runtime, seed_data
PBC_KEY="payment_orchestration"
STATE_TABLE="payment_orchestration_runtime_state"; FORM_TABLE="payment_orchestration_form_submission"; WORKFLOW_TABLE="payment_orchestration_workflow_run"; CONTROL_TABLE="payment_orchestration_control_execution"; AGENT_TABLE="payment_orchestration_agent_session"; READ_MODEL_TABLE="payment_orchestration_workbench_read_model"
_SCHEMA=f"""
CREATE TABLE IF NOT EXISTS {STATE_TABLE} (tenant TEXT PRIMARY KEY, state_json TEXT NOT NULL, updated_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS {FORM_TABLE} (submission_id TEXT PRIMARY KEY, tenant TEXT NOT NULL, form_key TEXT NOT NULL, action TEXT NOT NULL, subject_id TEXT, payload_json TEXT NOT NULL, result_json TEXT NOT NULL, created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS {WORKFLOW_TABLE} (workflow_run_id TEXT PRIMARY KEY, tenant TEXT NOT NULL, wizard_key TEXT NOT NULL, subject_id TEXT, status TEXT NOT NULL, context_json TEXT NOT NULL, result_json TEXT NOT NULL, created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS {CONTROL_TABLE} (control_run_id TEXT PRIMARY KEY, tenant TEXT NOT NULL, control_key TEXT NOT NULL, allowed INTEGER NOT NULL, result_json TEXT NOT NULL, created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS {AGENT_TABLE} (session_id TEXT PRIMARY KEY, tenant TEXT NOT NULL, skill_name TEXT NOT NULL, scope TEXT NOT NULL, requires_confirmation INTEGER NOT NULL, payload_json TEXT NOT NULL, result_json TEXT NOT NULL, created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS {READ_MODEL_TABLE} (read_model_id TEXT PRIMARY KEY, tenant TEXT NOT NULL, intent_count INTEGER NOT NULL, captured_count INTEGER NOT NULL, settlement_count INTEGER NOT NULL, payout_count INTEGER NOT NULL, refund_count INTEGER NOT NULL, dispute_count INTEGER NOT NULL, payload_json TEXT NOT NULL, updated_at TEXT NOT NULL);
"""
def _json(v:Any)->str: return json.dumps(v, sort_keys=True, default=str)
def _load(v:str|None)->Any: return None if v is None else json.loads(v)
def _now()->str: return "local-harness-clock"
class PaymentOrchestrationStandaloneRepository:
    def __init__(self,database_path=":memory:"):
        self.database_path=database_path
        if database_path != ":memory:": Path(database_path).expanduser().resolve().parent.mkdir(parents=True, exist_ok=True)
        self.connection=sqlite3.connect(database_path); self.connection.row_factory=sqlite3.Row; self.apply_migrations()
    def close(self): self.connection.close()
    def apply_migrations(self): self.connection.executescript(_SCHEMA); self.connection.commit(); return (STATE_TABLE,FORM_TABLE,WORKFLOW_TABLE,CONTROL_TABLE,AGENT_TABLE,READ_MODEL_TABLE)
    def load_state(self,tenant):
        row=self.connection.execute(f"SELECT state_json FROM {STATE_TABLE} WHERE tenant=?",(tenant,)).fetchone()
        return _load(row["state_json"]) if row else runtime.payment_orchestration_empty_state()
    def save_state(self,tenant,state):
        self.connection.execute(f"INSERT INTO {STATE_TABLE} VALUES (?,?,?) ON CONFLICT(tenant) DO UPDATE SET state_json=excluded.state_json, updated_at=excluded.updated_at",(tenant,_json(state),_now()))
        self._sync_read_model(tenant,state); self.connection.commit(); return {"ok":True,"tenant":tenant}
    def _sync_read_model(self,tenant,state):
        view=runtime.payment_orchestration_build_workbench_view(state,tenant=tenant) if state.get("configuration") else {"ok":True,"tenant":tenant}
        row={"read_model_id":f"{tenant}:workbench","tenant":tenant,"intent_count":int(view.get("intent_count",0)),"captured_count":int(view.get("captured_count",0)),"settlement_count":int(view.get("settlement_count",0)),"payout_count":int(view.get("payout_count",0)),"refund_count":int(view.get("refund_count",0)),"dispute_count":int(view.get("dispute_count",0)),"payload_json":_json(view),"updated_at":_now()}
        self.connection.execute(f"DELETE FROM {READ_MODEL_TABLE} WHERE tenant=?",(tenant,)); self.connection.execute(f"INSERT INTO {READ_MODEL_TABLE} ({', '.join(row)}) VALUES ({', '.join('?' for _ in row)})",tuple(row.values()))
    def _insert(self,table,prefix,fields):
        n=self.connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]; self.connection.execute(f"INSERT INTO {table} VALUES ({', '.join('?' for _ in range(len(fields)+1))})",(f"{prefix}_{n+1:05d}",*fields))
    def _form(self,t,k,a,s,p,r): self._insert(FORM_TABLE,"form",(t,k,a,s,_json(p),_json(r),_now()))
    def _workflow(self,t,k,s,c,r): self._insert(WORKFLOW_TABLE,"workflow",(t,k,s,"completed" if r.get("ok") else "blocked",_json(c),_json(r),_now()))
    def _control(self,t,k,r): self._insert(CONTROL_TABLE,"control",(t,k,int(bool(r.get("ok"))),_json(r),_now()))
    def _result(self,t,r):
        if r.get("ok") is True and "state" in r: self.save_state(t,r["state"])
        return r
    def configure_runtime(self,t,c): r=runtime.payment_orchestration_configure_runtime(self.load_state(t),c); self._form(t,"payment_configuration","configure_runtime",None,c,r); return self._result(t,r)
    def set_parameter(self,t,n,v): r=runtime.payment_orchestration_set_parameter(self.load_state(t),n,v); self._form(t,"payment_parameter","set_parameter",n,{"name":n,"value":v},r); return self._result(t,r)
    def register_rule(self,t,rule): r=runtime.payment_orchestration_register_rule(self.load_state(t),rule); self._form(t,"payment_rule","register_rule",rule.get("rule_id"),rule,r); return self._result(t,r)
    def receive_event(self,t,e): r=runtime.payment_orchestration_receive_event(self.load_state(t),e); self._form(t,"payment_event_inbox","receive_event",e.get("event_id"),e,r); return self._result(t,r)
    def register_gateway(self,t,g): r=runtime.payment_orchestration_register_gateway(self.load_state(t),g); self._form(t,"payment_gateway","register_gateway",g.get("gateway_id"),g,r); return self._result(t,r)
    def tokenize_payment_method(self,t,token): r=runtime.payment_orchestration_tokenize_payment_method(self.load_state(t),token); self._form(t,"payment_token","tokenize_payment_method",token.get("token_id"),token,r); return self._result(t,r)
    def create_payment_intent(self,t,intent): r=runtime.payment_orchestration_create_payment_intent(self.load_state(t),intent); self._form(t,"payment_intent","create_payment_intent",intent.get("intent_id"),intent,r); return self._result(t,r)
    def route_gateway(self,t,intent_id): r=runtime.payment_orchestration_route_gateway(self.load_state(t),intent_id); self._workflow(t,"payment_acceptance_setup",intent_id,{},r); return self._result(t,r)
    def request_fraud_check(self,t,intent_id): r=runtime.payment_orchestration_request_fraud_check(self.load_state(t),intent_id); self._workflow(t,"authorize_capture_settle",intent_id,{},r); return self._result(t,r)
    def capture_payment(self,t,intent_id,amount): r=runtime.payment_orchestration_capture_payment(self.load_state(t),intent_id,amount=amount); self._workflow(t,"authorize_capture_settle",intent_id,{"amount":amount},r); return self._result(t,r)
    def settle_payment(self,t,intent_id,settlement_reference): r=runtime.payment_orchestration_settle_payment(self.load_state(t),intent_id,settlement_reference=settlement_reference); self._workflow(t,"authorize_capture_settle",intent_id,{"settlement_reference":settlement_reference},r); return self._result(t,r)
    def schedule_payout(self,t,intent_id,payout_account): r=runtime.payment_orchestration_schedule_payout(self.load_state(t),intent_id,payout_account=payout_account); self._workflow(t,"authorize_capture_settle",intent_id,{"payout_account":payout_account},r); return self._result(t,r)
    def refund_payment(self,t,intent_id,amount,reason): r=runtime.payment_orchestration_refund_payment(self.load_state(t),intent_id,amount=amount,reason=reason); self._workflow(t,"refund_and_dispute_resolution",intent_id,{"amount":amount,"reason":reason},r); return self._result(t,r)
    def open_dispute(self,t,intent_id,amount,reason,evidence=()): r=runtime.payment_orchestration_open_dispute(self.load_state(t),intent_id,amount=amount,reason=reason,evidence=tuple(evidence)); self._workflow(t,"refund_and_dispute_resolution",intent_id,{"amount":amount,"reason":reason,"evidence":tuple(evidence)},r); return self._result(t,r)
    def resolve_dispute(self,t,dispute_id,decision,resolution_notes): r=runtime.payment_orchestration_resolve_dispute(self.load_state(t),dispute_id,decision=decision,resolution_notes=resolution_notes); self._workflow(t,"refund_and_dispute_resolution",dispute_id,{"decision":decision},r); return self._result(t,r)
    def generate_payment_proof(self,t,intent_id,disclosure): r=runtime.payment_orchestration_generate_payment_proof(self.load_state(t),intent_id,disclosure=tuple(disclosure)); self._control(t,"payment_proof",r); self.connection.commit(); return r
    def run_control_tests(self,t): r=runtime.payment_orchestration_run_control_tests(self.load_state(t)); self._control(t,"payment_release_controls",r); self.connection.commit(); return r
    def run_agent_skill(self,t,skill,payload):
        from . import agent
        plan=agent.document_instruction_plan(payload.get("document"),payload.get("instructions")); r={"ok":plan["ok"],"skill_name":skill,"plan":plan,"requires_confirmation":True}; self._insert(AGENT_TABLE,"agent",(t,skill,payload.get("scope","payment"),1,_json(payload),_json(r),_now())); self.connection.commit(); return r
    def build_workbench(self,t): return {"ok":True,**runtime.payment_orchestration_build_workbench_view(self.load_state(t),tenant=t),"activity_counts":self.activity_counts(t),"read_model":self.read_model(t)}
    def read_model(self,t):
        row=self.connection.execute(f"SELECT * FROM {READ_MODEL_TABLE} WHERE tenant=?",(t,)).fetchone()
        if not row: return {"ok":False,"tenant":t,"reason":"read_model_not_found"}
        d=dict(row); d["payload"]=_load(d.pop("payload_json")); d["ok"]=True; return d
    def activity_counts(self,t): return {"forms":self.connection.execute(f"SELECT COUNT(*) FROM {FORM_TABLE} WHERE tenant=?",(t,)).fetchone()[0],"workflows":self.connection.execute(f"SELECT COUNT(*) FROM {WORKFLOW_TABLE} WHERE tenant=?",(t,)).fetchone()[0],"controls":self.connection.execute(f"SELECT COUNT(*) FROM {CONTROL_TABLE} WHERE tenant=?",(t,)).fetchone()[0],"agent_sessions":self.connection.execute(f"SELECT COUNT(*) FROM {AGENT_TABLE} WHERE tenant=?",(t,)).fetchone()[0]}
    def seed_demo_workspace(self,tenant="tenant_demo"):
        b=seed_data.standalone_seed_bundle(tenant); self.configure_runtime(tenant,b["configuration"]); [self.set_parameter(tenant,k,v) for k,v in b["parameters"].items()]; self.register_rule(tenant,b["rule"]); self.register_gateway(tenant,b["gateway"]); self.receive_event(tenant,b["checkout_event"]); self.tokenize_payment_method(tenant,b["token"]); self.create_payment_intent(tenant,b["intent"]); self.route_gateway(tenant,b["intent"]["intent_id"]); self.request_fraud_check(tenant,b["intent"]["intent_id"]); self.receive_event(tenant,b["fraud_event"]); captured=self.capture_payment(tenant,b["intent"]["intent_id"],b["intent"]["amount"]); settled=self.settle_payment(tenant,b["intent"]["intent_id"],b["settlement_reference"]); payout=self.schedule_payout(tenant,b["intent"]["intent_id"],b["payout_account"]); refund=self.refund_payment(tenant,b["intent"]["intent_id"],b["refund"]["amount"],b["refund"]["reason"]); dispute=self.open_dispute(tenant,b["intent"]["intent_id"],b["dispute"]["amount"],b["dispute"]["reason"],b["dispute"]["evidence"]); resolved=self.resolve_dispute(tenant,dispute["dispute"]["dispute_id"],"merchant_won","evidence accepted"); controls=self.run_control_tests(tenant); proof=self.generate_payment_proof(tenant,b["intent"]["intent_id"],("intent_id","amount","currency","status")); agent=self.run_agent_skill(tenant,"payment_orchestration.document_instruction_intake",{"document":b["document"],"instructions":b["instructions"],"scope":"seed"}); return {"ok":captured["ok"] and settled["ok"] and payout["ok"] and refund["ok"] and dispute["ok"] and resolved["ok"] and controls["ok"] and proof["ok"] and agent["ok"],"tenant":tenant,"bundle":b,"workbench":self.build_workbench(tenant)}

def standalone_repository_contract(): return {"format":"appgen.payment-orchestration-standalone-repository.v1","ok":True,"pbc":PBC_KEY,"repository_class":"PaymentOrchestrationStandaloneRepository","local_harness_backend":"sqlite3","deployment_database_backends":runtime.PAYMENT_ORCHESTRATION_ALLOWED_DATABASE_BACKENDS,"tables":(STATE_TABLE,FORM_TABLE,WORKFLOW_TABLE,CONTROL_TABLE,AGENT_TABLE,READ_MODEL_TABLE),"side_effects":()}
def standalone_repository_smoke_test():
    repo=PaymentOrchestrationStandaloneRepository()
    try:
        seeded=repo.seed_demo_workspace(); return {"ok":seeded["ok"] and repo.read_model("tenant_demo")["ok"],"seeded":seeded,"contract":standalone_repository_contract(),"side_effects":()}
    finally: repo.close()
