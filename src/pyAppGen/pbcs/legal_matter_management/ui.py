"""UI fragments for the legal_matter_management PBC."""
PBC_KEY = 'legal_matter_management'
UI_FRAGMENTS = ('LegalMatterManagementWorkbench', 'LegalMatterManagementDetail', 'LegalMatterManagementAssistantPanel')


def legal_matter_management_ui_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'fragments': UI_FRAGMENTS, 'workbench_view': UI_FRAGMENTS[0], 'configuration_editor': True, 'action_permissions': ('legal_matter_management.read', 'legal_matter_management.create', 'legal_matter_management.update', 'legal_matter_management.approve', 'legal_matter_management.admin'), 'stream_engine_picker_visible': False, 'side_effects': ()}


def legal_matter_management_render_workbench(state=None):
    return {'ok': True, 'pbc': PBC_KEY, 'view': UI_FRAGMENTS[0], 'panels': ('overview','records','rules','agent'), 'configuration_editor': True, 'action_permissions': ('legal_matter_management.read', 'legal_matter_management.create', 'legal_matter_management.update', 'legal_matter_management.approve', 'legal_matter_management.admin'), 'side_effects': ()}


def smoke_test():
    return {'ok': legal_matter_management_ui_contract()['ok'] and legal_matter_management_render_workbench()['ok'], 'side_effects': ()}

# Full UI capability surface bound to the world-class domain-depth contract.
from .domain_depth import ui_capability_surface_contract as legal_matter_management_ui_capability_surface_contract
from .domain_depth import domain_capability_surface_contract as legal_matter_management_domain_capability_surface_contract

_BASE_LEGAL_MATTER_MANAGEMENT_UI_CONTRACT = legal_matter_management_ui_contract
_BASE_LEGAL_MATTER_MANAGEMENT_RENDER_WORKBENCH = legal_matter_management_render_workbench


def legal_matter_management_ui_contract():
    base = dict(_BASE_LEGAL_MATTER_MANAGEMENT_UI_CONTRACT())
    full = legal_matter_management_ui_capability_surface_contract()
    return {
        **base,
        'ok': base.get('ok') is True and full['ok'],
        'full_capability_surface': full,
        'operation_actions': full['operation_actions'],
        'rule_editors': full['rule_editors'],
        'parameter_editors': full['parameter_editors'],
        'advanced_panels': full['advanced_panels'],
        'edge_case_queues': full['edge_case_queues'],
        'table_browsers': full['table_browsers'],
        'navigation_sections': full['navigation_sections'],
    }


def legal_matter_management_render_workbench(state=None):
    base = dict(_BASE_LEGAL_MATTER_MANAGEMENT_RENDER_WORKBENCH(state=state))
    full = legal_matter_management_ui_capability_surface_contract()
    return {
        **base,
        'ok': base.get('ok') is True and full['ok'],
        'panels': tuple(dict.fromkeys(tuple(base.get('panels', ())) + full['navigation_sections'])),
        'operation_actions': full['operation_actions'],
        'advanced_panels': full['advanced_panels'],
        'edge_case_queues': full['edge_case_queues'],
        'table_browsers': full['table_browsers'],
        'agent_tools': full['agent_tools'],
    }

from .controls import control_catalog
from .forms import form_catalog
from .wizards import wizard_catalog

_BASE_LEGAL_MATTER_MANAGEMENT_UI_CONTRACT_WITH_DEPTH = legal_matter_management_ui_contract

def legal_matter_management_ui_contract():
    base = dict(_BASE_LEGAL_MATTER_MANAGEMENT_UI_CONTRACT_WITH_DEPTH())
    full = dict(base.get('full_capability_surface', {}))
    full['forms'] = form_catalog()['forms']
    full['wizards'] = wizard_catalog()['wizards']
    full['controls'] = control_catalog()['controls']
    full['navigation_sections'] = tuple(dict.fromkeys(tuple(full.get('navigation_sections', ())) + ('intake','conflicts','holds','deadlines','filings','privilege','spend','settlement')))
    return {**base, 'ok': base.get('ok') is True and len(full['forms']) >= 8 and len(full['wizards']) >= 7 and len(full['controls']) >= 7, 'full_capability_surface': full, 'navigation_sections': full['navigation_sections']}

def legal_matter_management_standalone_ui_contract():
    ui = legal_matter_management_ui_contract()
    full = ui['full_capability_surface']
    return {'ok': ui['ok'] and len(full['forms']) >= 8 and len(full['wizards']) >= 7 and len(full['controls']) >= 7, 'pbc': PBC_KEY, 'single_pbc_app_route': f'/apps/{PBC_KEY}', 'forms': full['forms'], 'wizards': full['wizards'], 'controls': full['controls'], 'assistant_panel': 'LegalMatterManagementAssistantPanel', 'side_effects': ()}

_BASE_LEGAL_MATTER_MANAGEMENT_SMOKE_WITH_DEPTH = smoke_test
def smoke_test():
    return {'ok': _BASE_LEGAL_MATTER_MANAGEMENT_SMOKE_WITH_DEPTH()['ok'] and legal_matter_management_standalone_ui_contract()['ok'], 'side_effects': ()}
