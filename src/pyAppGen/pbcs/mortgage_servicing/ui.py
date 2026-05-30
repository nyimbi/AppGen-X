"""UI contracts for mortgage_servicing."""
from __future__ import annotations
from .controls import control_catalog
from .domain_depth import DOMAIN_ADVANCED_CAPABILITIES, DOMAIN_EDGE_CASES, DOMAIN_OPERATIONS, DOMAIN_OWNED_TABLES, DOMAIN_PARAMETERS, DOMAIN_RULES, domain_capability_surface_contract
from .forms import form_catalog
from .wizards import wizard_catalog
PBC_KEY="mortgage_servicing"

def mortgage_servicing_ui_contract():
    surface=domain_capability_surface_contract()
    return {"ok":True,"pbc":PBC_KEY,"fragments":("MortgageServicingWorkbench","MortgageServicingDetail","MortgageServicingAssistantPanel","MortgageServicingPaymentConsole","MortgageServicingLossMitigationBoard","MortgageServicingInvestorReportingDesk"),"configuration_editor":True,"stream_engine_picker_visible":False,"action_permissions":("mortgage_servicing.read","mortgage_servicing.create","mortgage_servicing.update","mortgage_servicing.approve","mortgage_servicing.admin"),"role_boards":("boarding_and_transfer","payment_and_suspense","escrow_and_notices","delinquency_and_collections","loss_mitigation","foreclosure_controls","investor_reporting","exception_triage"),"forms":form_catalog()["forms"],"wizards":wizard_catalog()["wizards"],"controls":control_catalog()["controls"],"full_capability_surface":{"operation_actions":DOMAIN_OPERATIONS,"rule_editors":DOMAIN_RULES,"parameter_editors":DOMAIN_PARAMETERS,"advanced_panels":DOMAIN_ADVANCED_CAPABILITIES,"table_browsers":DOMAIN_OWNED_TABLES,"edge_case_queues":DOMAIN_EDGE_CASES,"agent_tools":tuple(f"{PBC_KEY}_skills.{op}" for op in DOMAIN_OPERATIONS),"navigation_sections":("overview","boarding","cash","escrow","borrower_assistance","foreclosure","investor","release_evidence"),"coverage":surface["coverage"]},"side_effects":()}

def mortgage_servicing_render_workbench():
    ui=mortgage_servicing_ui_contract(); full=ui["full_capability_surface"]
    return {"ok":True,"pbc":PBC_KEY,"route":f"/workbench/pbcs/{PBC_KEY}","role_boards":ui["role_boards"],"operation_actions":full["operation_actions"],"table_browsers":full["table_browsers"],"forms":tuple(f["id"] for f in ui["forms"]),"wizards":tuple(w["id"] for w in ui["wizards"]),"exception_queues":full["edge_case_queues"],"side_effects":()}

def smoke_test(): return {"ok":mortgage_servicing_ui_contract()["ok"] and mortgage_servicing_render_workbench()["ok"],"side_effects":()}
