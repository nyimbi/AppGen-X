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


# Improve1 PBM benefits release evidence extension.
from .benefits_control import improve1_benefits_control_contract as _improve1_benefits_control_contract

_BASE_BUILD_RELEASE_EVIDENCE = build_release_evidence
_BASE_RELEASE_READINESS_MANIFEST = release_readiness_manifest
_BASE_VALIDATE_RELEASE_EVIDENCE = validate_release_evidence


def build_release_evidence():
    evidence = dict(_BASE_BUILD_RELEASE_EVIDENCE())
    control = _improve1_benefits_control_contract()
    evidence["ok"] = bool(evidence.get("ok")) and control["ok"]
    evidence["benefits_control"] = control
    evidence["traceability"] = tuple(dict.fromkeys(tuple(evidence.get("traceability", ())) + ("improve1_benefits_control", "tests/test_domain_behavior.py")))
    evidence["blocking_gaps"] = tuple(evidence.get("blocking_gaps", ())) + tuple(control.get("blocking_gaps", ()))
    return evidence


def release_readiness_manifest():
    manifest = dict(_BASE_RELEASE_READINESS_MANIFEST())
    control = _improve1_benefits_control_contract()
    manifest["ok"] = bool(manifest.get("ok")) and control["ok"]
    manifest["benefits_control"] = control
    manifest["blocking_gaps"] = tuple(manifest.get("blocking_gaps", ())) + tuple(control.get("blocking_gaps", ()))
    return manifest


def validate_release_evidence():
    validation = dict(_BASE_VALIDATE_RELEASE_EVIDENCE())
    control = _improve1_benefits_control_contract()
    validation["ok"] = bool(validation.get("ok")) and control["ok"]
    validation["benefits_control"] = control
    validation["failed_checks"] = tuple(validation.get("failed_checks", ())) + tuple(control.get("blocking_gaps", ()))
    return validation
