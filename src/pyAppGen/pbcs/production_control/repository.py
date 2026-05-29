"""Package-local persistence for the standalone Production Control application."""
from __future__ import annotations
import json, sqlite3
from pathlib import Path
from typing import Any
from . import runtime, seed_data
PBC_KEY='production_control'
STATE_TABLE='production_control_runtime_state'; FORM_TABLE='production_control_form_submission'; WORKFLOW_TABLE='production_control_workflow_run'; CONTROL_TABLE='production_control_control_execution'; AGENT_TABLE='production_control_agent_session'; READ_MODEL_TABLE='production_control_workbench_read_model'
_SCHEMA=f"""
CREATE TABLE IF NOT EXISTS {STATE_TABLE} (tenant TEXT PRIMARY KEY, state_json TEXT NOT NULL, updated_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS {FORM_TABLE} (submission_id TEXT PRIMARY KEY, tenant TEXT NOT NULL, form_key TEXT NOT NULL, action TEXT NOT NULL, subject_id TEXT, payload_json TEXT NOT NULL, result_json TEXT NOT NULL, created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS {WORKFLOW_TABLE} (workflow_run_id TEXT PRIMARY KEY, tenant TEXT NOT NULL, wizard_key TEXT NOT NULL, subject_id TEXT, status TEXT NOT NULL, context_json TEXT NOT NULL, result_json TEXT NOT NULL, created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS {CONTROL_TABLE} (control_run_id TEXT PRIMARY KEY, tenant TEXT NOT NULL, control_key TEXT NOT NULL, allowed INTEGER NOT NULL, result_json TEXT NOT NULL, created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS {AGENT_TABLE} (session_id TEXT PRIMARY KEY, tenant TEXT NOT NULL, skill_name TEXT NOT NULL, scope TEXT NOT NULL, requires_confirmation INTEGER NOT NULL, payload_json TEXT NOT NULL, result_json TEXT NOT NULL, created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS {READ_MODEL_TABLE} (read_model_id TEXT PRIMARY KEY, tenant TEXT NOT NULL, work_center_count INTEGER NOT NULL, order_count INTEGER NOT NULL, completed_order_count INTEGER NOT NULL, operation_count INTEGER NOT NULL, downtime_minutes REAL NOT NULL, completed_qty REAL NOT NULL, payload_json TEXT NOT NULL, updated_at TEXT NOT NULL);
"""
def _json(v:Any)->str: return json.dumps(v, sort_keys=True)
def _load(v:str|None)->Any: return None if v is None else json.loads(v)
def _now()->str: return 'local-harness-clock'
class ProductionControlStandaloneRepository:
    def __init__(self,database_path=':memory:'):
        self.database_path=database_path
        if database_path!=':memory:': Path(database_path).expanduser().resolve().parent.mkdir(parents=True,exist_ok=True)
        self.connection=sqlite3.connect(database_path); self.connection.row_factory=sqlite3.Row; self.apply_migrations()
    def close(self): self.connection.close()
    def apply_migrations(self): self.connection.executescript(_SCHEMA); self.connection.commit(); return (STATE_TABLE,FORM_TABLE,WORKFLOW_TABLE,CONTROL_TABLE,AGENT_TABLE,READ_MODEL_TABLE)
    def load_state(self,tenant):
        row=self.connection.execute(f'SELECT state_json FROM {STATE_TABLE} WHERE tenant=?',(tenant,)).fetchone()
        return _load(row['state_json']) if row else runtime.production_control_empty_state()
    def save_state(self,tenant,state):
        self.connection.execute(f'INSERT INTO {STATE_TABLE} VALUES (?,?,?) ON CONFLICT(tenant) DO UPDATE SET state_json=excluded.state_json, updated_at=excluded.updated_at',(tenant,_json(state),_now()))
        self._sync_read_model(tenant,state); self.connection.commit(); return {'ok':True,'tenant':tenant}
    def _sync_read_model(self,tenant,state):
        centers=tuple(i for i in state.get('work_centers',{}).values() if i.get('tenant')==tenant); orders=tuple(i for i in state.get('orders',{}).values() if i.get('tenant')==tenant); steps=tuple(i for i in state.get('routing_steps',{}).values() if i.get('tenant')==tenant); downtime=tuple(i for i in state.get('downtime_events',{}).values() if i.get('tenant')==tenant)
        payload=runtime.production_control_build_workbench_view(state,tenant=tenant) if state.get('configuration') else {'ok':True,'tenant':tenant}
        row={'read_model_id':f'{tenant}:workbench','tenant':tenant,'work_center_count':len(centers),'order_count':len(orders),'completed_order_count':len(tuple(o for o in orders if o.get('status')=='completed')),'operation_count':len(steps),'downtime_minutes':float(sum(i.get('minutes',0) for i in downtime)),'completed_qty':float(sum(o.get('completed_qty',0) for o in orders)),'payload_json':_json(payload),'updated_at':_now()}
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
        seq=('allowed_sites','allowed_work_center_types','allowed_downtime_reasons','allowed_production_routes'); norm={**c,**{k:tuple(c.get(k,())) for k in seq}}
        r=runtime.production_control_configure_runtime(self.load_state(t),norm); self._form(t,'ProductionConfigurationForm','configure_runtime',None,c,r); return self._result(t,r)
    def set_parameter(self,t,n,v): r=runtime.production_control_set_parameter(self.load_state(t),n,v); self._form(t,'ProductionParameterForm','set_parameter',n,{'name':n,'value':v},r); return self._result(t,r)
    def register_rule(self,t,rule): r=runtime.production_control_register_rule(self.load_state(t),rule); self._form(t,'ProductionRuleForm','register_rule',rule.get('rule_id'),rule,r); return self._result(t,r)
    def receive_event(self,t,e): r=runtime.production_control_receive_event(self.load_state(t),e); self._form(t,'ProductionEventInboxForm','receive_event',e.get('event_id'),e,r); return self._result(t,r)
    def register_work_center(self,t,w): r=runtime.production_control_register_work_center(self.load_state(t),w); self._form(t,'WorkCenterForm','register_work_center',w.get('work_center_id'),w,r); return self._result(t,r)
    def create_production_order(self,t,o): r=runtime.production_control_create_production_order(self.load_state(t),o); self._form(t,'ProductionOrderForm','create_production_order',o.get('order_id'),o,r); return self._result(t,r)
    def define_routing_step(self,t,s): r=runtime.production_control_define_routing_step(self.load_state(t),s); self._form(t,'RoutingStepForm','define_routing_step',s.get('step_id'),s,r); return self._result(t,r)
    def schedule_order(self,t,order_id,scheduled_by): r=runtime.production_control_schedule_order(self.load_state(t),order_id,scheduled_by=scheduled_by); self._workflow(t,'ScheduleAndDispatchWizard',order_id,{'order_id':order_id},r); return self._result(t,r)
    def start_operation(self,t,step_id,started_by): r=runtime.production_control_start_operation(self.load_state(t),step_id,started_by=started_by); self._workflow(t,'OperationExecutionWizard',step_id,{'step_id':step_id},r); return self._result(t,r)
    def record_material_consumption(self,t,p): r=runtime.production_control_record_material_consumption(self.load_state(t),p); self._form(t,'MaterialConsumptionForm','record_material_consumption',p.get('consumption_id'),p,r); return self._result(t,r)
    def book_labor_time(self,t,p): r=runtime.production_control_book_labor_time(self.load_state(t),p); self._form(t,'LaborBookingForm','book_labor_time',p.get('booking_id'),p,r); return self._result(t,r)
    def book_machine_time(self,t,p): r=runtime.production_control_book_machine_time(self.load_state(t),p); self._form(t,'MachineBookingForm','book_machine_time',p.get('booking_id'),p,r); return self._result(t,r)
    def record_downtime(self,t,p): r=runtime.production_control_record_downtime(self.load_state(t),p); self._form(t,'DowntimeForm','record_downtime',p.get('downtime_id'),p,r); return self._result(t,r)
    def record_quality_gate_result(self,t,p): r=runtime.production_control_record_quality_gate_result(self.load_state(t),p); self._form(t,'QualityGateForm','record_quality_gate_result',p.get('gate_id'),p,r); return self._result(t,r)
    def record_scrap_rework(self,t,p): r=runtime.production_control_record_scrap_rework(self.load_state(t),p); self._form(t,'ScrapReworkForm','record_scrap_rework',p.get('scrap_rework_id'),p,r); return self._result(t,r)
    def confirm_operation(self,t,step_id,**kw): r=runtime.production_control_confirm_operation(self.load_state(t),step_id,**kw); self._workflow(t,'OperationConfirmationWizard',step_id,kw,r); return self._result(t,r)
    def complete_production_order(self,t,order_id,completed_by): r=runtime.production_control_complete_production_order(self.load_state(t),order_id,completed_by=completed_by); self._workflow(t,'ProductionCompletionWizard',order_id,{'order_id':order_id},r); return self._result(t,r)
    def run_control_tests(self,t): r=runtime.production_control_run_control_tests(self.load_state(t)); self._control(t,'production_release_controls',r); self.connection.commit(); return r
    def generate_completion_proof(self,t,order_id,disclosure): r=runtime.production_control_generate_completion_proof(self.load_state(t),order_id,disclosure=tuple(disclosure)); self._control(t,'completion_proof',r); self.connection.commit(); return r
    def run_agent_skill(self,t,skill,payload):
        from . import agent
        plan=agent.document_instruction_plan(payload.get('document'),payload.get('instructions')); r={'ok':plan['ok'],'skill_name':skill,'plan':plan,'requires_confirmation':True}; n=self.connection.execute(f'SELECT COUNT(*) FROM {AGENT_TABLE}').fetchone()[0]; self.connection.execute(f'INSERT INTO {AGENT_TABLE} VALUES (?,?,?,?,?,?,?,?)',(f'agent_{n+1:05d}',t,skill,payload.get('scope','production'),1,_json(payload),_json(r),_now())); self.connection.commit(); return r
    def build_workbench(self,t): st=self.load_state(t); return {'ok':True,**runtime.production_control_build_workbench_view(st,tenant=t),'activity_counts':self.activity_counts(t),'read_model':self.read_model(t)}
    def read_model(self,t):
        row=self.connection.execute(f'SELECT * FROM {READ_MODEL_TABLE} WHERE tenant=?',(t,)).fetchone()
        if not row: return {'ok':False,'tenant':t,'reason':'read_model_not_found'}
        d=dict(row); d['payload']=_load(d.pop('payload_json')); d['ok']=True; return d
    def activity_counts(self,t): return {'forms':self.connection.execute(f'SELECT COUNT(*) FROM {FORM_TABLE} WHERE tenant=?',(t,)).fetchone()[0],'workflows':self.connection.execute(f'SELECT COUNT(*) FROM {WORKFLOW_TABLE} WHERE tenant=?',(t,)).fetchone()[0],'controls':self.connection.execute(f'SELECT COUNT(*) FROM {CONTROL_TABLE} WHERE tenant=?',(t,)).fetchone()[0],'agent_sessions':self.connection.execute(f'SELECT COUNT(*) FROM {AGENT_TABLE} WHERE tenant=?',(t,)).fetchone()[0]}
    def seed_demo_workspace(self,tenant='tenant_demo'):
        b=seed_data.standalone_seed_bundle(tenant=tenant); self.configure_runtime(tenant,b['configuration']); [self.set_parameter(tenant,k,v) for k,v in b['parameters'].items()]; [self.register_rule(tenant,r) for r in b['rules']]; [self.receive_event(tenant,e) for e in b['events']]; self.register_work_center(tenant,b['work_center']); self.create_production_order(tenant,b['production_order']); self.define_routing_step(tenant,b['routing_step']); self.schedule_order(tenant,b['production_order']['order_id'],'scheduler_1'); self.start_operation(tenant,b['routing_step']['step_id'],'operator_1'); self.record_material_consumption(tenant,b['material_consumption']); self.book_labor_time(tenant,b['labor_booking']); self.book_machine_time(tenant,b['machine_booking']); self.record_downtime(tenant,b['downtime']); self.record_quality_gate_result(tenant,b['quality_gate']); self.record_scrap_rework(tenant,b['scrap_rework']); self.confirm_operation(tenant,b['routing_step']['step_id'],good_qty=9,scrap_qty=1,labor_hours=2,machine_hours=2.3,confirmed_by='operator_1'); self.complete_production_order(tenant,b['production_order']['order_id'],'supervisor_1'); controls=self.run_control_tests(tenant); proof=self.generate_completion_proof(tenant,b['production_order']['order_id'],('order_id','item','completed_qty')); agent=self.run_agent_skill(tenant,'production_control.document_instruction_intake',{'document':b['document'],'instructions':b['instructions'],'scope':'seed'}); return {'ok':controls['ok'] and proof['ok'] and agent['ok'],'tenant':tenant,'bundle':b,'workbench':self.build_workbench(tenant)}

def standalone_repository_contract(): return {'format':'appgen.production-control-standalone-repository.v1','ok':True,'pbc':PBC_KEY,'repository_class':'ProductionControlStandaloneRepository','local_harness_backend':'sqlite3','deployment_database_backends':runtime.PRODUCTION_CONTROL_ALLOWED_DATABASE_BACKENDS,'tables':(STATE_TABLE,FORM_TABLE,WORKFLOW_TABLE,CONTROL_TABLE,AGENT_TABLE,READ_MODEL_TABLE),'side_effects':()}
def standalone_repository_smoke_test():
    repo=ProductionControlStandaloneRepository()
    try:
        seeded=repo.seed_demo_workspace(); return {'ok':seeded['ok'] and repo.read_model('tenant_demo')['ok'],'seeded':seeded,'contract':standalone_repository_contract(),'side_effects':()}
    finally: repo.close()
