"""UI contracts for music_royalties_rights."""
from .controls import control_catalog
from .domain_depth import DOMAIN_ADVANCED_CAPABILITIES, DOMAIN_EDGE_CASES, DOMAIN_OPERATIONS, DOMAIN_OWNED_TABLES, DOMAIN_PARAMETERS, DOMAIN_RULES, domain_capability_surface_contract
from .forms import form_catalog
from .wizards import wizard_catalog
PBC_KEY="music_royalties_rights"
def music_royalties_rights_ui_contract():
    s=domain_capability_surface_contract(); return {"ok":True,"pbc":PBC_KEY,"fragments":("MusicRoyaltiesRightsWorkbench","MusicRoyaltiesRightsDetail","MusicRoyaltiesRightsAssistantPanel","MusicRoyaltiesRightsRepertoireDesk","MusicRoyaltiesRightsStatementConsole","MusicRoyaltiesRightsDisputeBoard"),"configuration_editor":True,"stream_engine_picker_visible":False,"action_permissions":("music_royalties_rights.read","music_royalties_rights.create","music_royalties_rights.update","music_royalties_rights.approve","music_royalties_rights.admin"),"role_boards":("repertoire_identity","splits_and_chain_of_title","recording_linkage","license_approval","usage_ingestion","statement_runs","payments_and_recoupment","disputes"),"forms":form_catalog()["forms"],"wizards":wizard_catalog()["wizards"],"controls":control_catalog()["controls"],"full_capability_surface":{"operation_actions":DOMAIN_OPERATIONS,"rule_editors":DOMAIN_RULES,"parameter_editors":DOMAIN_PARAMETERS,"advanced_panels":DOMAIN_ADVANCED_CAPABILITIES,"table_browsers":DOMAIN_OWNED_TABLES,"edge_case_queues":DOMAIN_EDGE_CASES,"agent_tools":tuple(f"{PBC_KEY}_skills.{op}" for op in DOMAIN_OPERATIONS),"navigation_sections":("overview","repertoire","licenses","usage","statements","payments","disputes","release_evidence"),"coverage":s["coverage"]},"side_effects":()}
def music_royalties_rights_render_workbench():
    ui=music_royalties_rights_ui_contract(); full=ui["full_capability_surface"]; return {"ok":True,"pbc":PBC_KEY,"route":f"/workbench/pbcs/{PBC_KEY}","role_boards":ui["role_boards"],"operation_actions":full["operation_actions"],"table_browsers":full["table_browsers"],"forms":tuple(f["id"] for f in ui["forms"]),"wizards":tuple(w["id"] for w in ui["wizards"]),"exception_queues":full["edge_case_queues"],"side_effects":()}
def smoke_test(): return {"ok":music_royalties_rights_ui_contract()["ok"] and music_royalties_rights_render_workbench()["ok"],"side_effects":()}


# Improve1 music royalties control UI extension.
from .royalties_rights_control import improve1_royalties_rights_control_contract as _improve1_royalties_rights_control_contract

_MUSIC_ROYALTIES_RIGHTS_BASE_UI_CONTRACT = music_royalties_rights_ui_contract
_MUSIC_ROYALTIES_RIGHTS_BASE_RENDER_WORKBENCH = music_royalties_rights_render_workbench


def music_royalties_rights_ui_contract():
    ui = dict(_MUSIC_ROYALTIES_RIGHTS_BASE_UI_CONTRACT())
    control = _improve1_royalties_rights_control_contract()
    panels = tuple(item["evidence"]["ui_surface"] for item in control["capabilities"])
    service_actions = tuple(item["evidence"]["service_api"] for item in control["capabilities"])
    ui.update({
        "ok": ui.get("ok") is True and control["ok"],
        "royalties_rights_control_contract": control,
        "royalties_rights_control_panels": panels,
        "royalties_rights_control_service_actions": service_actions,
        "stream_engine_picker_visible": False,
    })
    return ui


def music_royalties_rights_render_workbench():
    workbench = dict(_MUSIC_ROYALTIES_RIGHTS_BASE_RENDER_WORKBENCH())
    control = _improve1_royalties_rights_control_contract()
    workbench.update({
        "ok": workbench.get("ok") is True and control["ok"],
        "royalties_rights_control_panels": tuple(item["evidence"]["ui_surface"] for item in control["capabilities"]),
        "royalties_rights_control_service_actions": tuple(item["evidence"]["service_api"] for item in control["capabilities"]),
        "royalties_rights_control_agent_tools": tuple(f"music_royalties_rights.skills.{item['slug']}" for item in control["capabilities"]),
    })
    return workbench
