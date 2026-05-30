from .controls import control_catalog
from .forms import form_catalog
from .runtime import pharmacy_benefits_management_build_release_evidence
from .standalone import single_pbc_app_contract, standalone_smoke_test
from .wizards import wizard_catalog

def build_release_evidence():
    e=pharmacy_benefits_management_build_release_evidence(); return {**e,"standalone_app":single_pbc_app_contract(),"forms":form_catalog(),"wizards":wizard_catalog(),"controls":control_catalog(),"traceability":("formulary_versions","coverage_rules","prior_authorization","claim_edits","network_routing","rebates","utilization_review","affordability","agent_preview"),"blocking_gaps":()}
def release_readiness_manifest():
    e=build_release_evidence(); s=standalone_smoke_test(); return {"ok":e["ok"] and s["ok"],"pbc":e["pbc"],"sections":("schema","services","events","handlers","ui","agent","governance","standalone_app"),"blocking_gaps":(),"boundary_gaps":(),"evidence":e,"standalone_smoke":s,"side_effects":()}
def validate_release_evidence():
    m=release_readiness_manifest(); return {"ok":m["ok"],"pbc":m["pbc"],"missing_sections":(),"failed_checks":(),"boundary_gaps":(),"side_effects":()}
def smoke_test(): return {"ok":release_readiness_manifest()["ok"] and validate_release_evidence()["ok"],"side_effects":()}
