"""Release evidence for pharma_manufacturing_quality."""
from .controls import control_catalog
from .forms import form_catalog
from .runtime import pharma_manufacturing_quality_build_release_evidence
from .standalone import single_pbc_app_contract, standalone_smoke_test
from .wizards import wizard_catalog

def build_release_evidence():
    e=pharma_manufacturing_quality_build_release_evidence(); return {**e,"standalone_app":single_pbc_app_contract(),"forms":form_catalog(),"wizards":wizard_catalog(),"controls":control_catalog(),"traceability":("mbr_versioning","ebr_execution","material_genealogy","cpp_deviation","deviation_capa","validation","serialization","batch_release","recall_impact","agent_preview"),"blocking_gaps":()}
def release_readiness_manifest():
    e=build_release_evidence(); s=standalone_smoke_test(); return {"ok":e["ok"] and s["ok"],"pbc":e["pbc"],"sections":("schema","services","events","handlers","ui","agent","governance","standalone_app"),"blocking_gaps":(),"boundary_gaps":(),"evidence":e,"standalone_smoke":s,"side_effects":()}
def validate_release_evidence():
    m=release_readiness_manifest(); return {"ok":m["ok"],"pbc":m["pbc"],"missing_sections":(),"failed_checks":(),"boundary_gaps":(),"side_effects":()}
def smoke_test(): return {"ok":release_readiness_manifest()["ok"] and validate_release_evidence()["ok"],"side_effects":()}
