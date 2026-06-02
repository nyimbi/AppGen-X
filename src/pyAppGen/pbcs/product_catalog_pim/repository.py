"""Package-local persistence for the standalone Product Catalog PIM application."""
from __future__ import annotations
import json, sqlite3
from pathlib import Path
from typing import Any
from . import runtime, seed_data
PBC_KEY='product_catalog_pim'
STATE_TABLE='product_catalog_pim_runtime_state'; FORM_TABLE='product_catalog_pim_form_submission'; WORKFLOW_TABLE='product_catalog_pim_workflow_run'; CONTROL_TABLE='product_catalog_pim_control_execution'; AGENT_TABLE='product_catalog_pim_agent_session'; READ_MODEL_TABLE='product_catalog_pim_workbench_read_model'
_SCHEMA=f"""
CREATE TABLE IF NOT EXISTS {STATE_TABLE} (tenant TEXT PRIMARY KEY, state_json TEXT NOT NULL, updated_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS {FORM_TABLE} (submission_id TEXT PRIMARY KEY, tenant TEXT NOT NULL, form_key TEXT NOT NULL, action TEXT NOT NULL, subject_id TEXT, payload_json TEXT NOT NULL, result_json TEXT NOT NULL, created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS {WORKFLOW_TABLE} (workflow_run_id TEXT PRIMARY KEY, tenant TEXT NOT NULL, wizard_key TEXT NOT NULL, subject_id TEXT, status TEXT NOT NULL, context_json TEXT NOT NULL, result_json TEXT NOT NULL, created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS {CONTROL_TABLE} (control_run_id TEXT PRIMARY KEY, tenant TEXT NOT NULL, control_key TEXT NOT NULL, allowed INTEGER NOT NULL, result_json TEXT NOT NULL, created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS {AGENT_TABLE} (session_id TEXT PRIMARY KEY, tenant TEXT NOT NULL, skill_name TEXT NOT NULL, scope TEXT NOT NULL, requires_confirmation INTEGER NOT NULL, payload_json TEXT NOT NULL, result_json TEXT NOT NULL, created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS {READ_MODEL_TABLE} (read_model_id TEXT PRIMARY KEY, tenant TEXT NOT NULL, family_count INTEGER NOT NULL, product_count INTEGER NOT NULL, published_product_count INTEGER NOT NULL, publication_count INTEGER NOT NULL, media_count INTEGER NOT NULL, average_completeness REAL NOT NULL, payload_json TEXT NOT NULL, updated_at TEXT NOT NULL);
"""
def _json(v:Any)->str: return json.dumps(v, sort_keys=True)
def _load(v:str|None)->Any: return None if v is None else json.loads(v)
def _now()->str: return 'local-harness-clock'
class ProductCatalogPimStandaloneRepository:
    """Persists a one-PBC product catalog workspace with forms, workflows, controls, and agent sessions."""
    def __init__(self,database_path=':memory:'):
        self.database_path=database_path
        if database_path!=':memory:': Path(database_path).expanduser().resolve().parent.mkdir(parents=True,exist_ok=True)
        self.connection=sqlite3.connect(database_path); self.connection.row_factory=sqlite3.Row; self.apply_migrations()
    def close(self): self.connection.close()
    def apply_migrations(self): self.connection.executescript(_SCHEMA); self.connection.commit(); return (STATE_TABLE,FORM_TABLE,WORKFLOW_TABLE,CONTROL_TABLE,AGENT_TABLE,READ_MODEL_TABLE)
    def load_state(self,tenant):
        row=self.connection.execute(f'SELECT state_json FROM {STATE_TABLE} WHERE tenant=?',(tenant,)).fetchone()
        return _load(row['state_json']) if row else runtime.product_catalog_pim_empty_state()
    def save_state(self,tenant,state):
        self.connection.execute(f'INSERT INTO {STATE_TABLE} VALUES (?,?,?) ON CONFLICT(tenant) DO UPDATE SET state_json=excluded.state_json, updated_at=excluded.updated_at',(tenant,_json(state),_now()))
        self._sync_read_model(tenant,state); self.connection.commit(); return {'ok':True,'tenant':tenant}
    def _sync_read_model(self,tenant,state):
        view=runtime.product_catalog_pim_build_workbench_view(state,tenant=tenant) if state.get('configuration') else {'ok':True,'tenant':tenant,'family_count':0,'product_count':0,'published_product_count':0,'publication_count':0,'media_count':0,'average_completeness':0.0}
        row={'read_model_id':f'{tenant}:workbench','tenant':tenant,'family_count':int(view.get('family_count',0)),'product_count':int(view.get('product_count',0)),'published_product_count':int(view.get('published_product_count',0)),'publication_count':int(view.get('publication_count',0)),'media_count':int(view.get('media_count',0)),'average_completeness':float(view.get('average_completeness',0.0)),'payload_json':_json(view),'updated_at':_now()}
        self.connection.execute(f'DELETE FROM {READ_MODEL_TABLE} WHERE tenant=?',(tenant,)); self.connection.execute(f"INSERT INTO {READ_MODEL_TABLE} ({', '.join(row)}) VALUES ({', '.join('?' for _ in row)})",tuple(row.values()))
    def _insert(self,table,prefix,fields):
        n=self.connection.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0]; self.connection.execute(f"INSERT INTO {table} VALUES ({', '.join('?' for _ in range(len(fields)+1))})",(f'{prefix}_{n+1:05d}',*fields))
    def _form(self,t,k,a,s,p,r): self._insert(FORM_TABLE,'form',(t,k,a,s,_json(p),_json(r),_now()))
    def _workflow(self,t,k,s,c,r): self._insert(WORKFLOW_TABLE,'workflow',(t,k,s,'completed' if r.get('ok') else 'blocked',_json(c),_json(r),_now()))
    def _control(self,t,k,r): self._insert(CONTROL_TABLE,'control',(t,k,int(bool(r.get('ok'))),_json(r),_now()))
    def _result(self,t,r):
        if 'state' in r:
            self.save_state(t,r['state'])
        return r
    def configure_runtime(self,t,c):
        seq=('allowed_channels','allowed_locales','allowed_media_roles','allowed_regions'); norm={**c,**{k:tuple(c.get(k,())) for k in seq}}
        r=runtime.product_catalog_pim_configure_runtime(self.load_state(t),norm); self._form(t,'ProductConfigurationForm','configure_runtime',None,c,r); return self._result(t,r)
    def set_parameter(self,t,n,v): r=runtime.product_catalog_pim_set_parameter(self.load_state(t),n,v); self._form(t,'ProductParameterForm','set_parameter',n,{'name':n,'value':v},r); return self._result(t,r)
    def register_rule(self,t,rule):
        norm={**rule,'allowed_channels':tuple(rule.get('allowed_channels',())),'allowed_locales':tuple(rule.get('allowed_locales',())),'required_attributes':tuple(rule.get('required_attributes',())),'required_media_roles':tuple(rule.get('required_media_roles',())),'restricted_regions':tuple(rule.get('restricted_regions',()))}
        r=runtime.product_catalog_pim_register_rule(self.load_state(t),norm); self._form(t,'ProductRuleForm','register_rule',rule.get('rule_id'),rule,r); return self._result(t,r)
    def receive_event(self,t,e): r=runtime.product_catalog_pim_receive_event(self.load_state(t),e); self._form(t,'ProductEventInboxForm','receive_event',e.get('event_id'),e,r); return self._result(t,r)
    def create_product_family(self,t,f):
        norm={**f,'variant_axes':tuple(f.get('variant_axes',()))}; r=runtime.product_catalog_pim_create_product_family(self.load_state(t),norm); self._form(t,'ProductFamilyForm','create_product_family',f.get('family_id'),f,r); return self._result(t,r)
    def register_product(self,t,p): r=runtime.product_catalog_pim_register_product(self.load_state(t),p); self._form(t,'ProductMasterForm','register_product',p.get('product_id'),p,r); return self._result(t,r)
    def define_attribute_schema(self,t,s):
        norm={**s,'attributes':tuple(s.get('attributes',()))}; r=runtime.product_catalog_pim_define_attribute_schema(self.load_state(t),norm); self._form(t,'AttributeSchemaForm','define_attribute_schema',s.get('schema_id'),s,r); return self._result(t,r)
    def set_product_attribute(self,t,product_id,name,value): r=runtime.product_catalog_pim_set_product_attribute(self.load_state(t),product_id,name,value); self._form(t,'ProductAttributeForm','set_product_attribute',product_id,{'name':name,'value':value},r); return self._result(t,r)
    def add_localized_content(self,t,c): r=runtime.product_catalog_pim_add_localized_content(self.load_state(t),c); self._form(t,'LocalizedContentForm','add_localized_content',c.get('content_id'),c,r); return self._result(t,r)
    def attach_product_media(self,t,m): r=runtime.product_catalog_pim_attach_product_media(self.load_state(t),m); self._form(t,'ProductMediaForm','attach_product_media',m.get('media_id'),m,r); return self._result(t,r)
    def add_price_metadata(self,t,p): r=runtime.product_catalog_pim_add_price_metadata(self.load_state(t),p); self._form(t,'ProductPriceForm','add_price_metadata',p.get('price_id'),p,r); return self._result(t,r)
    def add_compliance_claim(self,t,c): r=runtime.product_catalog_pim_add_compliance_claim(self.load_state(t),c); self._form(t,'ComplianceClaimForm','add_compliance_claim',c.get('claim_id'),c,r); return self._result(t,r)
    def publish_product(self,t,product_id,channels,locales,published_by): r=runtime.product_catalog_pim_publish_product(self.load_state(t),product_id,channels=tuple(channels),locales=tuple(locales),published_by=published_by); self._workflow(t,'CatalogPublicationWizard',product_id,{'channels':channels,'locales':locales},r); return self._result(t,r)
    def generate_publication_proof(self,t,product_id,disclosure): r=runtime.product_catalog_pim_generate_publication_proof(self.load_state(t),product_id,disclosure=tuple(disclosure)); self._control(t,'publication_proof',r); self.connection.commit(); return r
    def run_control_tests(self,t): r=runtime.product_catalog_pim_run_control_tests(self.load_state(t)); self._control(t,'catalog_release_controls',r); self.connection.commit(); return r
    def run_agent_skill(self,t,skill,payload):
        from . import agent
        plan=agent.document_instruction_plan(payload.get('document'),payload.get('instructions')); r={'ok':plan['ok'],'skill_name':skill,'plan':plan,'requires_confirmation':True}; n=self.connection.execute(f'SELECT COUNT(*) FROM {AGENT_TABLE}').fetchone()[0]; self.connection.execute(f'INSERT INTO {AGENT_TABLE} VALUES (?,?,?,?,?,?,?,?)',(f'agent_{n+1:05d}',t,skill,payload.get('scope','catalog'),1,_json(payload),_json(r),_now())); self.connection.commit(); return r
    def build_workbench(self,t): st=self.load_state(t); return {'ok':True,**runtime.product_catalog_pim_build_workbench_view(st,tenant=t),'activity_counts':self.activity_counts(t),'read_model':self.read_model(t)}
    def read_model(self,t):
        row=self.connection.execute(f'SELECT * FROM {READ_MODEL_TABLE} WHERE tenant=?',(t,)).fetchone()
        if not row: return {'ok':False,'tenant':t,'reason':'read_model_not_found'}
        d=dict(row); d['payload']=_load(d.pop('payload_json')); d['ok']=True; return d
    def activity_counts(self,t): return {'forms':self.connection.execute(f'SELECT COUNT(*) FROM {FORM_TABLE} WHERE tenant=?',(t,)).fetchone()[0],'workflows':self.connection.execute(f'SELECT COUNT(*) FROM {WORKFLOW_TABLE} WHERE tenant=?',(t,)).fetchone()[0],'controls':self.connection.execute(f'SELECT COUNT(*) FROM {CONTROL_TABLE} WHERE tenant=?',(t,)).fetchone()[0],'agent_sessions':self.connection.execute(f'SELECT COUNT(*) FROM {AGENT_TABLE} WHERE tenant=?',(t,)).fetchone()[0]}
    def seed_demo_workspace(self,tenant='tenant_demo'):
        b=seed_data.standalone_seed_bundle(tenant=tenant); self.configure_runtime(tenant,b['configuration']); [self.set_parameter(tenant,k,v) for k,v in b['parameters'].items()]; [self.register_rule(tenant,r) for r in b['rules']]; [self.receive_event(tenant,e) for e in b['events']]; self.create_product_family(tenant,b['family']); self.register_product(tenant,b['product']); self.define_attribute_schema(tenant,b['attribute_schema']); [self.set_product_attribute(tenant,b['product']['product_id'],k,v) for k,v in b['attributes'].items()]; self.add_localized_content(tenant,b['content']); self.attach_product_media(tenant,b['media']); self.add_price_metadata(tenant,b['price']); self.add_compliance_claim(tenant,b['compliance_claim']); published=self.publish_product(tenant,b['product']['product_id'],b['publication']['channels'],b['publication']['locales'],'catalog_manager_1'); controls=self.run_control_tests(tenant); proof=self.generate_publication_proof(tenant,b['product']['product_id'],('product_id','sku','lifecycle_state','completeness')); agent=self.run_agent_skill(tenant,'product_catalog_pim.document_instruction_intake',{'document':b['document'],'instructions':b['instructions'],'scope':'seed'}); return {'ok':published['ok'] and controls['ok'] and proof['ok'] and agent['ok'],'tenant':tenant,'bundle':b,'workbench':self.build_workbench(tenant)}

def standalone_repository_contract(): return {'format':'appgen.product-catalog-pim-standalone-repository.v1','ok':True,'pbc':PBC_KEY,'repository_class':'ProductCatalogPimStandaloneRepository','local_harness_backend':'sqlite3','deployment_database_backends':runtime.PRODUCT_CATALOG_PIM_ALLOWED_DATABASE_BACKENDS,'tables':(STATE_TABLE,FORM_TABLE,WORKFLOW_TABLE,CONTROL_TABLE,AGENT_TABLE,READ_MODEL_TABLE),'side_effects':()}
def standalone_repository_smoke_test():
    repo=ProductCatalogPimStandaloneRepository()
    try:
        seeded=repo.seed_demo_workspace(); return {'ok':seeded['ok'] and repo.read_model('tenant_demo')['ok'],'seeded':seeded,'contract':standalone_repository_contract(),'side_effects':()}
    finally: repo.close()
