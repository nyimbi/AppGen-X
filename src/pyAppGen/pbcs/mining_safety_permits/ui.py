"""UI contracts for mining_safety_permits."""
from __future__ import annotations
from .controls import control_catalog
from .domain_depth import DOMAIN_ADVANCED_CAPABILITIES, DOMAIN_EDGE_CASES, DOMAIN_OPERATIONS, DOMAIN_OWNED_TABLES, DOMAIN_PARAMETERS, DOMAIN_RULES, domain_capability_surface_contract
from .forms import form_catalog
from .wizards import wizard_catalog
PBC_KEY = "mining_safety_permits"

def mining_safety_permits_ui_contract():
    surface = domain_capability_surface_contract()
    return {"ok": True, "pbc": PBC_KEY, "fragments": ("MiningSafetyPermitsWorkbench","MiningSafetyPermitsDetail","MiningSafetyPermitsAssistantPanel","MiningSafetyPermitsAreaControlBoard","MiningSafetyPermitsPermitConsole","MiningSafetyPermitsRegulatoryPackViewer"), "configuration_editor": True, "stream_engine_picker_visible": False, "action_permissions": ("mining_safety_permits.read","mining_safety_permits.create","mining_safety_permits.update","mining_safety_permits.approve","mining_safety_permits.admin"), "role_boards": ("area_control","permit_to_work","isolation_and_lockout","confined_space_and_gas","ground_control","blasting_and_reentry","shift_handover","incidents_and_regulatory_packs","agent_safety_assistant"), "forms": form_catalog()["forms"], "wizards": wizard_catalog()["wizards"], "controls": control_catalog()["controls"], "full_capability_surface": {"operation_actions": DOMAIN_OPERATIONS, "rule_editors": DOMAIN_RULES, "parameter_editors": DOMAIN_PARAMETERS, "advanced_panels": DOMAIN_ADVANCED_CAPABILITIES, "table_browsers": DOMAIN_OWNED_TABLES, "edge_case_queues": DOMAIN_EDGE_CASES, "agent_tools": tuple(f"{PBC_KEY}_skills.{op}" for op in DOMAIN_OPERATIONS), "navigation_sections": ("overview","area_control","permit_console","critical_controls","incident_prevention","regulatory_evidence","release_evidence"), "coverage": surface["coverage"]}, "side_effects": ()}

def mining_safety_permits_render_workbench():
    ui = mining_safety_permits_ui_contract(); full = ui["full_capability_surface"]
    return {"ok": True, "pbc": PBC_KEY, "route": f"/workbench/pbcs/{PBC_KEY}", "role_boards": ui["role_boards"], "operation_actions": full["operation_actions"], "table_browsers": full["table_browsers"], "forms": tuple(f["id"] for f in ui["forms"]), "wizards": tuple(w["id"] for w in ui["wizards"]), "exception_queues": full["edge_case_queues"], "side_effects": ()}

def smoke_test():
    ui = mining_safety_permits_ui_contract(); wb = mining_safety_permits_render_workbench()
    return {"ok": ui["ok"] and wb["ok"] and len(ui["forms"]) >= 8 and len(ui["wizards"]) >= 6, "side_effects": ()}
