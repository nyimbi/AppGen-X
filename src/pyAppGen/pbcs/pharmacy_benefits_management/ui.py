from .controls import control_catalog
from .domain_depth import DOMAIN_ADVANCED_CAPABILITIES, DOMAIN_EDGE_CASES, DOMAIN_OPERATIONS, DOMAIN_OWNED_TABLES, DOMAIN_PARAMETERS, DOMAIN_RULES, domain_capability_surface_contract
from .forms import form_catalog
from .wizards import wizard_catalog
PBC_KEY="pharmacy_benefits_management"
def pharmacy_benefits_management_ui_contract():
    s=domain_capability_surface_contract(); return {"ok":True,"pbc":PBC_KEY,"fragments":("PharmacyBenefitsManagementWorkbench","PharmacyBenefitsManagementDetail","PharmacyBenefitsManagementAssistantPanel","PharmacyBenefitsManagementFormularyDesk","PharmacyBenefitsManagementClaimConsole","PharmacyBenefitsManagementRebateWorkbench"),"configuration_editor":True,"stream_engine_picker_visible":False,"action_permissions":("pharmacy_benefits_management.read","pharmacy_benefits_management.create","pharmacy_benefits_management.update","pharmacy_benefits_management.approve","pharmacy_benefits_management.admin"),"role_boards":("formulary_versions","coverage_rules","prior_authorizations","claim_edits","networks","rebates","utilization_review","affordability"),"forms":form_catalog()["forms"],"wizards":wizard_catalog()["wizards"],"controls":control_catalog()["controls"],"full_capability_surface":{"operation_actions":DOMAIN_OPERATIONS,"rule_editors":DOMAIN_RULES,"parameter_editors":DOMAIN_PARAMETERS,"advanced_panels":DOMAIN_ADVANCED_CAPABILITIES,"table_browsers":DOMAIN_OWNED_TABLES,"edge_case_queues":DOMAIN_EDGE_CASES,"agent_tools":tuple(f"{PBC_KEY}_skills.{op}" for op in DOMAIN_OPERATIONS),"navigation_sections":("overview","configuration","pa","claims","rebates","clinical","release_evidence"),"coverage":s["coverage"]},"side_effects":()}
def pharmacy_benefits_management_render_workbench():
    ui=pharmacy_benefits_management_ui_contract(); full=ui["full_capability_surface"]; return {"ok":True,"pbc":PBC_KEY,"route":f"/workbench/pbcs/{PBC_KEY}","role_boards":ui["role_boards"],"operation_actions":full["operation_actions"],"table_browsers":full["table_browsers"],"forms":tuple(f["id"] for f in ui["forms"]),"wizards":tuple(w["id"] for w in ui["wizards"]),"exception_queues":full["edge_case_queues"],"side_effects":()}
def smoke_test(): return {"ok":pharmacy_benefits_management_ui_contract()["ok"] and pharmacy_benefits_management_render_workbench()["ok"],"side_effects":()}


# Improve1 PBM benefits control UI extension.
from .benefits_control import improve1_benefits_control_contract as _improve1_benefits_control_contract

_PBM_BASE_UI_CONTRACT = pharmacy_benefits_management_ui_contract
_PBM_BASE_RENDER_WORKBENCH = pharmacy_benefits_management_render_workbench


def pharmacy_benefits_management_ui_contract():
    ui = dict(_PBM_BASE_UI_CONTRACT())
    control = _improve1_benefits_control_contract()
    ui.update({"ok": ui.get("ok") is True and control["ok"], "benefits_control_contract": control, "benefits_control_panels": tuple(item["evidence"]["ui_surface"] for item in control["capabilities"]), "benefits_control_service_actions": tuple(item["evidence"]["service_api"] for item in control["capabilities"]), "stream_engine_picker_visible": False})
    return ui


def pharmacy_benefits_management_render_workbench():
    workbench = dict(_PBM_BASE_RENDER_WORKBENCH())
    control = _improve1_benefits_control_contract()
    workbench.update({"ok": workbench.get("ok") is True and control["ok"], "benefits_control_panels": tuple(item["evidence"]["ui_surface"] for item in control["capabilities"]), "benefits_control_service_actions": tuple(item["evidence"]["service_api"] for item in control["capabilities"]), "benefits_control_agent_tools": tuple(f"pharmacy_benefits_management.skills.{item['slug']}" for item in control["capabilities"])})
    return workbench
